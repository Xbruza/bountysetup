#!/usr/bin/env python3
"""Default scripted browser for this workspace: Camoufox (Firefox 158).

Run with the venv python: ~/workspace/camoufox/venv/bin/python cfx.py ...

Rules (standing):
- Camoufox is the DEFAULT for any scripted browsing: page checks, PoC
  verification, scraping, screenshots, JS evaluation.
- Use browser.browse (cloud/device browser) ONLY when a logged-in session
  is needed (e.g. XE filing as <YOUR_BOUNTY_USERNAME>, whose session lives in the cloud
  browser) or the user explicitly asks for the live browser.
- Always ignore_https_errors=True (VPS egress proxy MITM TLS).
- Never download to /tmp (512 MB tmpfs); write screenshots/artifacts
  under ~/workspace/.

Subcommands:
  open <url> [--wait-ms N] [--screenshot PATH] [--text-chars N]
             [--js EXPR] [--timeout-ms N]
      Prints JSON: url, final_url, status, title, text (excerpt), js result.
  check
      Sanity check: webdriver flag + UA + example.com load. Prints JSON.
"""
import argparse
import json
import sys

from camoufox.sync_api import Camoufox


def _open(url, wait_ms=2000, screenshot=None, text_chars=3000, js=None,
          timeout_ms=60000):
    with Camoufox(headless=True) as browser:
        ctx = browser.new_context(ignore_https_errors=True)
        page = ctx.new_page()
        resp = page.goto(url, wait_until="domcontentloaded",
                         timeout=timeout_ms)
        page.wait_for_timeout(wait_ms)
        out = {
            "url": url,
            "final_url": page.url,
            "status": resp.status if resp else None,
            "title": page.title(),
            "text": (page.inner_text("body") or "")[:text_chars],
        }
        if js:
            out["js"] = page.evaluate(js)
        if screenshot:
            page.screenshot(path=screenshot, full_page=False)
            out["screenshot"] = screenshot
        ctx.close()
        return out


def _check():
    with Camoufox(headless=True) as browser:
        ctx = browser.new_context(ignore_https_errors=True)
        page = ctx.new_page()
        page.goto("https://example.com", wait_until="domcontentloaded",
                  timeout=60000)
        out = {
            "webdriver": page.evaluate("navigator.webdriver"),
            "user_agent": page.evaluate("navigator.userAgent"),
            "title": page.title(),
            "loaded": page.title() == "Example Domain",
        }
        ctx.close()
        return out


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("open")
    o.add_argument("url")
    o.add_argument("--wait-ms", type=int, default=2000)
    o.add_argument("--screenshot", default=None)
    o.add_argument("--text-chars", type=int, default=3000)
    o.add_argument("--js", default=None)
    o.add_argument("--timeout-ms", type=int, default=60000)
    sub.add_parser("check")
    args = p.parse_args()
    if args.cmd == "open":
        out = _open(args.url, args.wait_ms, args.screenshot,
                    args.text_chars, args.js, args.timeout_ms)
    else:
        out = _check()
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
