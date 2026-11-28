#!/usr/bin/env python3
"""<RESEARCHER_MODEL> hunter agent: second-opinion bug hunter.

<RESEARCHER_MODEL> (via custom.xingchiapi) hunts one target area, Muse
verifies everything before it is filed. <RESEARCHER_MODEL> NEVER files, never grades,
never touches the network. Output is a candidate list only.

Usage:
  python3 xingchi-hunt.py --area api-pagination --files docs/api.md api/handler.go \
      --grep 'since|offset|limit|400|ParseInt|parsePagination' \
      --focus 'docs/api.md claims vs handler behaviour mismatches'

Output: <program>/leads-xingchi/<area>.md (raw <RESEARCHER_MODEL> reply +
usage), printed summary to stdout.
"""
import argparse
import json
import os
import re
import subprocess
import sys

REPO = os.path.expanduser(os.environ.get("TARGET_REPO", "~/workspace/<program>/repo"))
OUTDIR = os.path.expanduser(os.environ.get("HUNT_OUTDIR", "~/workspace/<program>/leads-xingchi"))
XINGCHI = os.path.join(os.path.dirname(__file__), "..", "connectors", "xingchiapi", "bin", "xingchi.py")
RESEARCHER = os.path.join(os.path.dirname(__file__), "..", "agents", "RESEARCHER.md")

KNOWN_FILED = (
    "<YOUR_FILED_TICKETS: ticket-id + one-line root cause each, "
    "comma-separated. Same root cause = duplicate, never propose it again.>"
)

# Desk families already reported by OTHER researchers: same root cause = duplicate.
# <RESEARCHER_MODEL> must not propose anything in these families.
KNOWN_DESK_FAMILIES = (
    "<TICKET-ID> lease status / lease claim report 'not found' when node unreachable; "
    "<TICKET-ID> Go client read helpers swallow HTTP status, zero values feed signing and user verdicts (GetBalances/GetPending/GetProviders/GetLeases/GetVM/getJSON); "
    "<TICKET-ID> GetChain ignores HTTP status, xe send signs an open block; "
    "<TICKET-ID> getJSON root: receive/providers/balance false emptiness on 429/5xx; "
    "<TICKET-ID> xe ssh treats a 404 lease as present; "
    "<TICKET-ID> CLI double-pays on blind retry after ambiguous SubmitBlock failure."
)

PROMPT = """You are a bug hunter for the <PROGRAM> bug bounty (<TARGET_REPO>, HEAD <SHA>).
Target area: {area}
Focus: {focus}

Code excerpts (file:line, may be truncated):
```
{excerpts}
```

Rules:
- Find at most 3 NEW candidates (validation gaps, wrong exit codes, display mislabels, docs-vs-code mismatches, silent fallbacks). Claim the severity the evidence supports; no High/Critical claims without a concrete exploit path.
- Each candidate: file:line, root cause in one paragraph, exact observable behaviour, impact in one line, and why it is NOT a duplicate of any known report below.
- Do NOT propose anything in the same root-cause family as a known report.
- If nothing new is found, say so plainly with the dead ends checked. Never invent a bug.
- Output plain text, no markdown tables, no fluff.
- Deliver in your RESEARCHER report format (Part A section 12): for each candidate give the Opportunity, Requirement Analysis (which scope rule it satisfies), Technical Research (exact code path), Competitive Intelligence (nearest known tickets + why it differs), Winning Strategy (why this candidate over others), Development Blueprint (the PoC handoff for BUILDER: exact reproduction steps, control case, what to record), Risk Assessment, Acceptance Criteria, Sources (file:line), and Handoff.

Already filed / known (do not re-report):
{known}

Already reported by OTHER researchers, same root cause = duplicate (do not propose anything in these families):
{known_families}
"""


def excerpts_for(files, pattern, max_lines=200):
    rx = re.compile(pattern) if pattern else None
    out = []
    for rel in files:
        path = os.path.join(REPO, rel)
        if not os.path.isfile(path):
            out.append(f"[{rel}: file not found]")
            continue
        with open(path, errors="replace") as f:
            lines = f.readlines()
        if rx is None:
            take = lines[:max_lines]
            out.append(f"--- {rel} (first {len(take)} lines) ---")
            out.extend(f"{i+1}:{l.rstrip()}" for i, l in enumerate(take))
        else:
            hits = [i for i, l in enumerate(lines) if rx.search(l)]
            out.append(f"--- {rel} ({len(hits)} matches for /{pattern}/) ---")
            shown = 0
            for i in hits:
                if shown >= max_lines:
                    out.append(f"... {len(hits) - shown} more matches, truncated")
                    break
                for j in range(max(0, i - 2), min(len(lines), i + 3)):
                    out.append(f"{j+1}:{lines[j].rstrip()}")
                out.append("...")
                shown += 1
    text = "\n".join(out)
    return text[:20000]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--area", required=True, help="slug, also the output filename")
    p.add_argument("--files", nargs="+", required=True, help="repo-relative files to read")
    p.add_argument("--grep", default="", help="regex; only matching lines (+2 ctx) are sent")
    p.add_argument("--focus", default="validation gaps and inconsistencies", help="what to hunt for")
    p.add_argument("--max-tokens", type=int, default=None, help="cap output tokens; omit for no cap")
    p.add_argument("--no-researcher", action="store_true", help="do NOT send RESEARCHER.md as instructions")
    args = p.parse_args()

    instructions = None
    if not args.no_researcher:
        with open(RESEARCHER) as f:
            instructions = f.read()
        print(f"[hunt] researcher role loaded: {len(instructions)} chars", file=sys.stderr)

    ex = excerpts_for(args.files, args.grep or None)
    prompt = PROMPT.format(area=args.area, focus=args.focus, excerpts=ex,
                          known=KNOWN_FILED, known_families=KNOWN_DESK_FAMILIES)
    print(f"[hunt] area={args.area} files={len(args.files)} prompt_chars={len(prompt)}", file=sys.stderr)

    cmd = [sys.executable, XINGCHI, "chat", "--prompt", prompt]
    if args.max_tokens is not None:
        cmd += ["--max-tokens", str(args.max_tokens)]
    if instructions:
        cmd += ["--instructions", instructions]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        print(r.stderr[-2000:], file=sys.stderr)
        sys.exit(f"xingchi call failed rc={r.returncode}")
    try:
        out = json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit("xingchi returned non-JSON output:\n" + r.stdout[-2000:])
    content = out.get("content") or ""
    usage = out.get("usage") or {}

    os.makedirs(OUTDIR, exist_ok=True)
    path = os.path.join(OUTDIR, args.area + ".md")
    with open(path, "w") as f:
        f.write(f"# <RESEARCHER_MODEL> hunt: {args.area}\n\n")
        f.write(f"Focus: {args.focus}\nFiles: {', '.join(args.files)}\n")
        f.write(f"Grep: {args.grep or '(whole file heads)'}\n")
        f.write(f"Model: {out.get('model')} status: {out.get('status')} usage: {json.dumps(usage)}\n\n")
        f.write("## <RESEARCHER_MODEL> reply (raw, UNVERIFIED - Muse must dedup + PoC before filing)\n\n")
        f.write(content if content else "(empty reply)\n")
    print(f"[hunt] wrote {path} chars={len(content)} usage={json.dumps(usage)}")
    print("=" * 60)
    print(content if content else "(empty reply - <RESEARCHER_MODEL> returned nothing)")


if __name__ == "__main__":
    main()
