#!/usr/bin/env python3
"""Packet Token Factory helper via the stored custom.packet connection.

Base https://api.packet.ai/v1, OpenAI-compatible chat completions.
Model for BUILDER: <CODER_MODEL_ID> (<CODER_MODEL> v4.1 Flash,
ctx 131k, verified via /models 2026-11-19: also lists <MODEL>
and Qwen2.5 1.5B).
Auth: Bearer key via surrogate (custom.packet). Key lives in the Secure
Vault, never in files, env, logs, or command lines.
Note: the two earlier Packet account keys failed 403 — only the
a Token Factory key has access. If this helper 403s, the stored key
is probably an account key, not a Token Factory key.
"""
import argparse
import json
import sys
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

BASE = "https://api.packet.ai/v1"
ALLOWED = ["api.packet.ai"]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def _req(path, payload=None):
    url = BASE + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if payload is not None else "GET")
    req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, "custom.packet", allowed_hosts=ALLOWED)
    return req


def call(path, payload=None, timeout=120):
    req = _req(path, payload)
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=timeout) as resp:
        return read_json_response(resp)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("models")
    c = sub.add_parser("chat")
    c.add_argument("--model", default="<CODER_MODEL_ID>")
    c.add_argument("--prompt", default="Reply with exactly: TEST OK")
    c.add_argument("--system", default=None, help="system prompt")
    c.add_argument("--max-tokens", type=int, default=None, help="cap output tokens; omit for no cap")
    c.add_argument("--timeout", type=int, default=300)
    args = p.parse_args()
    if args.cmd == "models":
        out = call("/models")
        ids = [m.get("id") for m in out.get("data", [])]
        print(json.dumps({"count": len(ids), "models": ids}))
    else:
        messages = []
        if args.system:
            messages.append({"role": "system", "content": args.system})
        messages.append({"role": "user", "content": args.prompt})
        payload = {"model": args.model, "messages": messages}
        if args.max_tokens is not None:
            payload["max_tokens"] = args.max_tokens
        out = call("/chat/completions", payload, timeout=args.timeout)
        choice = (out.get("choices") or [{}])[0]
        content = ((choice.get("message") or {}).get("content")) or ""
        print(json.dumps({
            "model": out.get("model"),
            "content": content,
            "usage": out.get("usage"),
        }))


if __name__ == "__main__":
    main()
