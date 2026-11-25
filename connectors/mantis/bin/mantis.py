#!/usr/bin/env python3
"""Mantis remote MCP client (custom.mantis).

Transport is curl, not urllib: the VM egress proxy truncates large chunked
responses under urllib's http.client (IncompleteRead on the 76 KB tools/list),
while curl fetches them intact. Auth is the bearer token stored in the
custom.mantis connection; only the hsurr: surrogate ever leaves this file,
and it travels in a 0600 curl config file, never on a command line.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import DynamicCredentialError, dynamic_credential_entry

PROVIDER = "custom.mantis"
ENDPOINT = "https://mantis.inverse.finance/mcp"
# Verified live against tools/list 2026-11-22 (59 tools). Only these are
# callable; anything the server adds later stays blocked until reviewed.
ALLOWED_TOOLS: set[str] = {
    "list_bounties",
    "get_bounty",
    "get_hunter",
    "list_hunter_reviews",
    "whoami",
    "get_hunter_profile",
    "list_my_submissions",
    "get_submission",
    "list_messages",
    "list_status_history",
    "submit_report",
    "send_message",
    "add_submission_followup",
}
PROTOCOLS = {"2025-11-25", "2025-06-18", "2025-03-26"}


class McpError(RuntimeError):
    """A transport or protocol failure with no automatic replay."""


class Client:
    def __init__(self):
        endpoint = urllib.parse.urlsplit(ENDPOINT)
        if (
            not PROVIDER.startswith("custom.")
            or endpoint.scheme != "https"
            or not endpoint.hostname
            or endpoint.port not in (None, 443)
        ):
            raise McpError("Configure a registered provider and its fixed HTTPS endpoint")
        self.host = endpoint.hostname
        self.session = None
        self.protocol = "2025-11-25"
        self.sequence = 0
        self._surrogate = None

    def _bearer(self):
        """Surrogate only; Sentinel swaps it for the real token on egress."""
        if self._surrogate is None:
            entry = dynamic_credential_entry(PROVIDER, "access_token")
            self._surrogate = str(entry["surrogate"]).strip()
            if not self._surrogate.startswith("hsurr:"):
                raise McpError("credential surrogate malformed")
        return self._surrogate

    def send(self, method, params, *, notification=False):
        self.sequence += 1
        request_id = None if notification else self.sequence
        body = {"jsonrpc": "2.0", "method": method, "params": params}
        if request_id is not None:
            body["id"] = request_id
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": self.protocol,
        }
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        try:
            headers["Authorization"] = f"Bearer {self._bearer()}"
        except DynamicCredentialError:
            # No credential registered yet: pre-auth tools (initialize,
            # tools/list, list_bounties, get_bounty, get_hunter,
            # list_hunter_reviews, auth_*) still work; anything needing auth
            # fails with the server's own 401.
            pass
        status, resp_headers, resp_body = self._curl_post(
            json.dumps(body).encode(), headers
        )
        if status != 200 and status != 202:
            raise McpError(f"MCP returned HTTP {status}; the operation was not replayed")
        session = resp_headers.get("mcp-session-id")
        if session:
            if not all(33 <= ord(c) <= 126 for c in session):
                raise McpError("MCP server returned an invalid session header")
            self.session = session
        if notification:
            if status != 202:
                raise McpError("MCP server did not accept the initialization notification")
            return None
        return self.read_result(resp_body, request_id)

    @staticmethod
    def _curl_post(data, headers):
        tmpdir = tempfile.mkdtemp(prefix="mantis-mcp-")
        cfg = os.path.join(tmpdir, "curlrc")
        out = os.path.join(tmpdir, "body")
        hdrs = os.path.join(tmpdir, "headers")
        try:
            lines = [
                f'url = "{ENDPOINT}"',
                "request = POST",
                "silent = true",
                "show-error = true",
                "max-time = 60",
                f'output = "{out}"',
                f'dump-header = "{hdrs}"',
            ]
            for key, value in headers.items():
                lines.append(f'header = "{key}: {value}"')
            Path(cfg).write_text("\n".join(lines) + "\n")
            os.chmod(cfg, 0o600)
            with open(os.path.join(tmpdir, "data"), "wb") as fh:
                fh.write(data)
            proc = subprocess.run(
                ["curl", "-K", cfg, "--data-binary", f"@{tmpdir}/data"],
                capture_output=True, text=True, timeout=90,
            )
            if proc.returncode != 0:
                raise McpError(f"curl failed: {proc.stderr.strip()[:300]}")
            resp_headers = {}
            status = 200
            for line in Path(hdrs).read_text(errors="replace").splitlines():
                if line.upper().startswith("HTTP/"):
                    # Last status line wins (proxy may add interim ones).
                    try:
                        status = int(line.split()[1])
                    except (IndexError, ValueError):
                        pass
                elif ":" in line:
                    k, v = line.split(":", 1)
                    resp_headers[k.strip().lower()] = v.strip()
            return status, resp_headers, Path(out).read_bytes()
        finally:
            for name in ("curlrc", "body", "headers", "data"):
                try:
                    os.unlink(os.path.join(tmpdir, name))
                except OSError:
                    pass
            try:
                os.rmdir(tmpdir)
            except OSError:
                pass

    @staticmethod
    def decode(payload, request_id):
        message = json.loads(payload)
        if not isinstance(message, dict):
            raise McpError("MCP returned an invalid JSON-RPC message")
        if "error" in message and message.get("jsonrpc") != "2.0":
            # Plain error object without a JSON-RPC envelope (Mantis
            # returns this for auth failures).
            err = message["error"]
            detail = err.get("message", err) if isinstance(err, dict) else err
            raise McpError(f"MCP returned an error: {detail}; the operation was not replayed")
        if message.get("jsonrpc") != "2.0":
            raise McpError("MCP returned an invalid JSON-RPC message")
        if type(message.get("id")) is not int or message["id"] != request_id:
            return None
        if "error" in message:
            raise McpError(
                f"MCP returned a JSON-RPC error: {message['error']}; the operation was not replayed"
            )
        if not isinstance(message.get("result"), dict):
            raise McpError("MCP returned no result object")
        return message["result"]

    @classmethod
    def read_result(cls, body, request_id):
        text = body.decode("utf-8", errors="replace")
        if text.lstrip().startswith("{"):
            result = cls.decode(text.encode(), request_id)
            if result is None:
                raise McpError("MCP returned the wrong request ID")
            return result
        data = []
        for line in text.splitlines():
            line = line.rstrip("\r")
            if line.startswith("data:"):
                data.append(line[5:].lstrip(" "))
            elif not line and data:
                result = cls.decode("\n".join(data).encode(), request_id)
                data.clear()
                if result is not None:
                    return result
        raise McpError("MCP event stream ended before the matching result")

    def initialize(self):
        result = self.send("initialize", {
            "protocolVersion": self.protocol,
            "capabilities": {},
            "clientInfo": {"name": "muse-custom-connector", "version": "1"},
        })
        protocol = result.get("protocolVersion")
        capabilities = result.get("capabilities")
        if (
            not isinstance(protocol, str)
            or protocol not in PROTOCOLS
            or not isinstance(capabilities, dict)
            or not isinstance(capabilities.get("tools"), dict)
        ):
            raise McpError("MCP server did not negotiate a supported tool protocol")
        self.protocol = protocol
        self.send("notifications/initialized", {}, notification=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    listing = subparsers.add_parser("list-tools")
    listing.add_argument("--cursor")
    calling = subparsers.add_parser("call-tool")
    calling.add_argument("--name", required=True)
    calling.add_argument("--arguments-file", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "call-tool":
        if args.name not in ALLOWED_TOOLS:
            parser.error("Inspect this operation's schema and add its exact name to ALLOWED_TOOLS")
        arguments = json.loads(args.arguments_file.read_bytes())
        if not isinstance(arguments, dict):
            parser.error("arguments must be a JSON object")
    client = Client()
    client.initialize()
    if args.command == "list-tools":
        result = client.send("tools/list", {"cursor": args.cursor} if args.cursor else {})
    else:
        result = client.send("tools/call", {"name": args.name, "arguments": arguments})
    print(json.dumps(result, ensure_ascii=False))
    return 1 if result.get("isError") else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (McpError, DynamicCredentialError, ValueError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
