# Bounty Hunter — Orchestrator Skeleton

A self-contained bug bounty hunting system: a 5-agent loop hunts one
program at a time, an advocate argues the team's side before any PoC
is built, and an independent auditor gates every filing. This repo is
the **skeleton only**: every role, the loop, the gates, the hard rules,
and the tooling. No credentials, no model names, no programs, no
schedules. Fill in the `<PLACEHOLDER>`s and it runs.

## Architecture

```
queue (data/bugbounties/bounty-queue.md)
        |
        v
ORCHESTRATOR (you, the main agent)
  0. scope freeze + web recon (agents/WEB-RECON.md)
  1. HEAD check + filed-report status check
  2. next area from scripts/xingchi-areas.json
  3. RESEARCHER hunts (agents/RESEARCHER.md)
  4. RESEARCHER verifies (max 3 candidates)
  5. ORCHESTRATOR dedups vs the program's public desk
  5b. DEVILS-ADVOCATE gate (agents/DEVILS-ADVOCATE.md)
  6. BUILDER proves on a fork (agents/BUILDER.md)
  7. AUDITOR re-runs + files (agents/AUDITOR.md)
        |
        v
report filed + receipt verified + lesson logged (LESSONS.md)
```

Roles, not products: each role is one LLM reached through an
OpenAI-compatible API. RESEARCHER hunts, DEVILS-ADVOCATE tries to kill
each candidate from the team's side, BUILDER proves, AUDITOR verifies
and files, ORCHESTRATOR (you) decides. One coder subagent at a time,
no races. Max 2 filings per hunter run.

## Contents

| Path | What it is |
|---|---|
| `agents/` | Role briefs: ORCHESTRATOR, RESEARCHER, DEVILS-ADVOCATE, BUILDER, AUDITOR, WEB-RECON (Beacon L1-L5 web recon annex). |
| `WORKFLOW.md` | The loop, gates, watchers, stop-loss rules, report voice. |
| `LESSONS.md` | Learning-loop template: kill-list + triage-outcome entries. Log every outcome the same day. |
| `scripts/` | `xingchi-hunt.py` (researcher driver), `xingchi-areas.json` (area queue template), `camoufox/cfx.py` (JS-heavy page fetcher), `install-web-recon.sh` + `verify-web-recon.sh` (Beacon tooling setup). |
| `skills/` | Reference skill repos as git submodules: claude-bughunter, reverse-skill, bug-hunter, agentic-bug-hunter, cybermes, strix. Clone with `git clone --recurse-submodules`. Their internal model catalogs are upstream defaults, not your configured models. |
| `skills-local/` | Local skill wrappers: bounty-reporting (report SOP + template), bounty-roi (go/no-go math), agentic-bug-hunter, bug-hunter, claude-bughunter, xingchi-hunter, cybersec-glossary. |
| `connectors/` | API helpers + docs: mantis (filing platform), packet (coder LLM), xingchiapi (researcher LLM). Keys live in your vault, never in files. |
| `data/bugbounties/` | Empty templates: queue, shortlist, directory-seen file. Fill them with your own programs. |
| `leads*/` | Empty output dirs (NOTE.md explains each format). |
| `WORKFLOW.md` | The loop, gates, stop-loss rules, report voice. |

## Prerequisites

1. **A bounty program to hunt.** No-KYC, no-fee only: any program that
   charges a submission fee/deposit or requires identity/KYC to get
   paid is skipped, including whole platforms that do.
2. **Three LLM API keys** (OpenAI-compatible), stored in your secure
   vault, one per role: researcher, advocate, coder, auditor/planner.
   No max-tokens cap on helper calls (long PoCs and audits get cut off
   otherwise). Fill the model IDs into the connector helpers and the
   agent briefs where you see `<RESEARCHER_MODEL>`,
   `<ADVOCATE_MODEL>`, `<CODER_MODEL_ID>`, `<PLANNER_MODEL>`,
   `<AUDITOR_MODEL>`.
3. **Hunt compute box**: a machine/VM you control where PoCs run
   (the BUILDER's fork + repro). The hunter itself runs on your main
   agent host; heavy builds go to the hunt box. Never run PoCs on
   mainnet, never move funds.
4. **Email account** for report contact + sign-in codes, and a payout
   setup per program (SOL/EVM addresses, PayPal) if the program asks.
   Fill `<YOUR_REPORT_EMAIL>`, `<YOUR_SOL_PAYOUT_ADDRESS>`,
   `<YOUR_EVM_PAYOUT_ADDRESS>`.
5. **Python 3.12+** and `git`. The `xingchi-hunt.py` driver is
   stdlib only. Cybermes/Strix need their own deps (see their READMEs).

## Install

1. Clone with submodules:
   `git clone --recurse-submodules <repo-url>` or
   `git submodule update --init --recursive` after a plain clone.
   The six repos under `skills/` are submodules pinned to the
   commits this setup was verified against; their upstreams:
   `https://github.com/elementalsouls/Claude-BugHunter`,
   `https://github.com/zhaoxuya520/reverse-skill`,
   `https://github.com/capture0x/Bug-Hunter`,
   `https://github.com/awarexone/Agentic-Bug-Hunter`,
   `https://github.com/Zyrexnn/Cybermes`,
   `https://github.com/usestrix/strix`.
2. Fill every `<PLACEHOLDER>` in `agents/`, `scripts/`,
   `connectors/` and `skills-local/local-bounty-reporting/templates/report.md`:
   `<YOUR_BOUNTY_USERNAME>`, `<YOUR_GITHUB_HANDLE>`,
   `<YOUR_MANTIS_HANDLE>`, `<YOUR_LOGIN_EMAIL>`,
   `<YOUR_REPORT_EMAIL>`, `<YOUR_PAYPAL_EMAIL>`,
   `<YOUR_SOL_PAYOUT_ADDRESS>`, `<YOUR_EVM_PAYOUT_ADDRESS>`,
   `<YOUR_CHAT_ID>`, `<RESEARCHER_MODEL>`, `<ADVOCATE_MODEL>`,
   `<CODER_MODEL_ID>`, `<PLANNER_MODEL>`, `<AUDITOR_MODEL>`,
   `<YOUR_FILED_TICKET_IDS>`, `<ADVOCATE_ENDPOINT>`,
   `<PLANNER_PROVIDER>`, `<YOUR_COMPUTE_BOX>`.
   Search the tree for `<` to confirm none are left.
3. Store the LLM keys in your vault and wire the connector helpers
   (`connectors/packet/bin/packet.py`,
   `connectors/xingchiapi/bin/xingchi.py`,
   `connectors/mantis/bin/mantis.py`) to them. Test each with its
   `models` / `whoami` command before the first hunt. Wire your own
   advocate + planner providers the same way (the role files name
   only `<ADVOCATE_MODEL>` / `<PLANNER_PROVIDER>`, never a vendor).
4. Clone the target repo for your first program into the path your
   hunter expects (default `~/workspace/<program>/repo`, see
   `scripts/xingchi-hunt.py`). Pin the HEAD you hunt and re-check it
   every run (`git ls-remote ... HEAD`).
5. Seed the queue: add your first program to
   `data/bugbounties/bounty-queue.md` (format in the file) and set
   its scope in a per-program `scope.md` + `allowlist.txt`
   (see `agents/WEB-RECON.md` Step 0).
6. Scheduling is yours: this repo ships **no cron jobs and no
   schedules**. If you want watchers (new-program watch) or a
   scheduled hunter, create them in your own scheduler from the
   `WORKFLOW.md` watcher + loop descriptions.

## First-run verification (dry run, files nothing)

1. `python3 -m py_compile scripts/xingchi-hunt.py connectors/*/bin/*.py`
   (must exit 0).
2. `python3 scripts/xingchi-hunt.py --help` (argparse works, no API call).
3. `python3 -c "import json; json.load(open('scripts/xingchi-areas.json'))"`
   (queue parses, areas listed, done empty).
4. `grep -r "sk-\|hai_t[f]-\|pk_liv[e]_" . ; grep -ri "kim[i]\|deepsee[k]\|gp[t]-6\|gl[m]" agents/ scripts/ connectors/ skills-local/`
   (must return nothing: no secrets, no model names in your own config.
   Bracket trick keeps the check itself from containing the strings.
   The `skills/` folder ships upstream repos verbatim; their internal
   model catalogs are upstream defaults, not your configured models.)
5. Run one hunter cycle with filing DISABLED (comment out the filing
   step in the AUDITOR brief for the dry run) and confirm a lead file
   lands in `leads-xingchi/` and the report names the area hunted
   and why each candidate lived or died.

## Hard rules (do not soften these)

- No-KYC, no-fee programs only. Any program that charges a
  submission fee/deposit or requires identity/KYC to get paid is
  skipped, including whole platforms that do (a per-report stake on
  every program is a fee).
- In-scope only, verification only, your own accounts only.
  Local fork PoCs only. Never mainnet, never move funds, never
  touch other users' data.
- Intent check before filing: if the team has ever seen, reviewed,
  audited or dismissed the mechanism, do NOT hunt or file it. No
  gray-zone bets. An audit finding the team never classified is a
  red flag, not a green light.
- File only on AUDITOR verdict READY (or CONDITIONALLY READY).
  One remediation round max. Never file NOT READY.
- Max 2 filings per hunter run. Public reports only, unless the
  program's own policy says otherwise.
- Stop-loss: a program that closes 0/0 after a full pass is closed.
  Reopen only on new scope or a fresh HEAD.
- Report voice: one professional ethical hacker, English, neat
  human writing. No agent/subagent talk, no em-dash.
- Never paste or store secrets. Keys live in the vault; helpers
  read them through the approved credential flow only.

## Deliberately excluded

- All credentials, keys, tokens, session data, wallet keys.
- All model names (roles only; you pick your own models).
- Personal identity: emails, handles, payout addresses, chat IDs.
- Cron jobs and schedules (yours to create, see step 6 above).
- Program-specific data: queues, scopes, leads, tickets, audits.
- The live target repo clone (clone it fresh, step 4 above).
- Python venvs, `__pycache__`, `.git` dirs, and the 185 MB
  Cybermes knowledge corpora (restore per step 1).

## Troubleshooting

- Helper 403s: the stored key lacks access for that endpoint.
  Reconnect that provider with the right key type (see the
  connector's CONNECTOR.md), never paste a key into a file.
- Filing blocked on sign-in: the browser session expired. The
  AUDITOR must NOT file; the draft stays ready and the run reports
  "ready to file, needs sign-in".
- Submission rate-limited ("too many reports"): wait ~19 minutes
  and retry in the same window. Never blindly retry an uncertain
  submission; check the account page + public desk first.
- Hunter says "queue empty, HEAD unchanged": correct, it stops.
  It resumes automatically when a new HEAD ships or you add areas.
