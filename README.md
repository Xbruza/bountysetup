# Bounty Hunter - Full Setup

A self-contained bug bounty hunting system: scheduled watchers find
no-KYC programs, a scheduled hunter runs a 4-agent loop against a
target repo, and an auditor gates every filing. Built from a live
system that filed 15+ public Minor reports on the XE testnet bounty
and hunts no-KYC programs only.

No credentials and no model names are in this zip. Everything secret
is a `<PLACEHOLDER>` you fill in yourself. See `WORKFLOW.md` for the
loop, gates and hard rules.

## Architecture

```
watchers (every 12h)                hunter (08:00 + 20:00 daily)
  bugbounty.fyi no-KYC watcher  ->  queue (data/bugbounties/bounty-queue.md)
  directory snapshot watcher    ->  queue
                                        |
                                        v
                              ORCHESTRATOR (this agent)
                                1. HEAD check + ticket status check
                                2. next area from scripts/xingchi-areas.json
                                3. RESEARCHER hunts (agents/RESEARCHER.md)
                                4. researcher verifies (max 3 candidates)
                                5. ORCHESTRATOR dedups vs public desk
                                6. BUILDER proves on a fork (agents/BUILDER.md)
                                7. AUDITOR re-runs + files (agents/AUDITOR.md)
                                        |
                                        v
                              report filed (public, Minor) + receipt verified
```

Roles, not products: each role is one LLM reached through an
OpenAI-compatible API. RESEARCHER hunts, BUILDER proves, AUDITOR
verifies and files, ORCHESTRATOR (you, the main agent) decides.
One coder subagent at a time, no races. Max 2 filings per hunter run.

## Contents

| Path | What it is |
|---|---|
| `crons/` | The 4 cron job definitions. Paste the body into your scheduler. |
| `agents/` | Role briefs: RESEARCHER, BUILDER, AUDITOR, ORCHESTRATOR, WEB-RECON (web recon annex: Step 0 scope freeze + Levels 1-5). |
| `scripts/` | `xingchi-hunt.py` (researcher driver), `xingchi-areas.json` (area queue), `camoufox/cfx.py` (JS-heavy page fetcher for the watcher). |
| `skills/` | Reference skill repos as git submodules: claude-bughunter, reverse-skill, bug-hunter, agentic-bug-hunter, cybermes, strix. Clone with `git clone --recurse-submodules`. Their internal model catalogs are upstream defaults, not your configured models. |
| `skills-local/` | Local skill wrappers: bounty-reporting (report SOP + template), bounty-roi (go/no-go math), agentic-bug-hunter, bug-hunter, claude-bughunter, xingchi-hunter, cybersec-glossary. |
| `connectors/` | API helpers + docs: mantis (filing platform), packet (coder LLM), xingchiapi (researcher LLM). Keys live in your vault, never in files. |
| `data/xe/` | Public desk snapshots (`tickets-*.json`) + regression data for dedup. |
| `data/bugbounties/` | Queue, shortlist, directory snapshot, empty seen-file template. |
| `leads*/` | Empty output dirs (NOTE.md explains each format). |
| `WORKFLOW.md` | The loop, gates, stop-loss rules, report voice. |

## Prerequisites

1. **Bounty platform account** for your target (e.g. XE desk at
   `https://bounty.xe.network`). Logged in through your agent's
   browser; the filing step uses that browser session.
2. **GitHub account** for cloning the target repo and for the
   bounty platform login, if it uses GitHub auth.
3. **Three LLM API keys** (OpenAI-compatible), stored in your secure
   vault, one per role: researcher, coder, auditor/planner. No
   max-tokens cap on helper calls (long PoCs and audits get cut off
   otherwise). Fill the model IDs into the connector helpers and the
   agent briefs where you see `<RESEARCHER_MODEL>`,
   `<CODER_MODEL_ID>`, `<PLANNER_MODEL>`, `<AUDITOR_MODEL>`.
4. **Hunt compute box**: a machine/VM you control where PoCs run
   (the BUILDER's fork + repro). The hunter itself runs on your main
   agent host; heavy builds go to the hunt box. Never run PoCs on
   mainnet, never move funds.
5. **Email account** for report contact + sign-in codes, and a
   payout setup per program (SOL/EVM addresses, PayPal) if the
   program asks. Fill `<YOUR_REPORT_EMAIL>`, `<YOUR_SOL_PAYOUT_ADDRESS>`,
   `<YOUR_EVM_PAYOUT_ADDRESS>`.
6. **Python 3.12+** and `git`. The `xingchi-hunt.py` driver is
   stdlib only. Cybermes/Strix need their own deps (see their READMEs).

## Install

1. Unzip anywhere, e.g. `~/bounty-hunter/`. The paths in the cron
   bodies and scripts assume `~/workspace/` layout; adjust the two
   path roots (`REPO`, `OUTDIR` in `scripts/xingchi-hunt.py`, and
   the `~/workspace/...` paths in `crons/*.md`) to your install root.
2. Clone the target repo for your first program:
   `git clone https://github.com/xeprotocol/xe` into the path your
   hunter expects (default `xe-bounty/xe`). Pin the HEAD you hunt
   and re-check it every run (`git ls-remote ... HEAD`).
3. Clone with submodules (or init them after a plain clone):
   `git clone --recurse-submodules <repo-url>` or
   `git submodule update --init --recursive`.
   The six repos under `skills/` are submodules pinned to the
   commits this setup was verified against; their upstreams:
   `https://github.com/elementalsouls/Claude-BugHunter`,
   `https://github.com/zhaoxuya520/reverse-skill`,
   `https://github.com/capture0x/Bug-Hunter`,
   `https://github.com/awarexone/Agentic-Bug-Hunter`,
   `https://github.com/Zyrexnn/Cybermes`,
   `https://github.com/usestrix/strix`.
4. Fill every `<PLACEHOLDER>` in `agents/`, `scripts/`,
   `connectors/`, `crons/` and `skills-local/local-bounty-reporting/templates/report.md`:
   `<YOUR_BOUNTY_USERNAME>`, `<YOUR_GITHUB_HANDLE>`,
   `<YOUR_MANTIS_HANDLE>`, `<YOUR_LOGIN_EMAIL>`,
   `<YOUR_REPORT_EMAIL>`, `<YOUR_PAYPAL_EMAIL>`,
   `<YOUR_SOL_PAYOUT_ADDRESS>`, `<YOUR_EVM_PAYOUT_ADDRESS>`,
   `<YOUR_CHAT_ID>`, `<RESEARCHER_MODEL>`, `<CODER_MODEL_ID>`,
   `<PLANNER_MODEL>`, `<AUDITOR_MODEL>`, `<YOUR_FILED_TICKET_IDS>`.
   Search the tree for `<` to confirm none are left.
5. Store the three LLM keys in your vault and wire the connector
   helpers (`connectors/packet/bin/packet.py`,
   `connectors/xingchiapi/bin/xingchi.py`,
   `connectors/mantis/bin/mantis.py`) to them. Test each with its
   `models` / `whoami` command before the first hunt.
6. Create the 4 cron jobs from `crons/*.md` (title, schedule,
   timeout 7200s, body as written). Watchers report only when
   something new is found; the hunter reports every run.
7. Seed the dedup data: `data/xe/tickets-*.json` is the public desk
   snapshot from 2026-11-23. Refresh it with a fresh fetch of the
   public ticket list before your first run.

## First-run verification (dry run, files nothing)

1. `python3 -m py_compile scripts/xingchi-hunt.py connectors/*/bin/*.py`
   (must exit 0).
2. `python3 scripts/xingchi-hunt.py --help` (argparse works, no API call).
3. `python3 -c "import json; json.load(open('scripts/xingchi-areas.json'))"`
   (queue parses, 10 areas, done empty).
4. `grep -r "sk-\|hai_t[f]-\|pk_liv[e]_" . ; grep -ri "kim[i]\|deepsee[k]\|gp[t]-6\|gl[m]" agents/ crons/ scripts/ connectors/ skills-local/`
   (must return nothing: no secrets, no model names in your own config.
   Bracket trick keeps the check itself from containing the strings.
   The `skills/` folder ships upstream repos verbatim; their internal
   model catalogs are upstream defaults, not your configured models.)
5. Run one watcher cron manually and confirm it stays silent when
   nothing is new.
6. Run one hunter cycle with filing DISABLED (comment out the filing
   step in the AUDITOR brief for the dry run) and confirm a lead file
   lands in `leads-xingchi/` and the report names the area hunted
   and why each candidate lived or died.

## Hard rules (do not soften these)

- No-KYC, no-fee programs only. Any program that charges a
  submission fee/deposit or requires identity/KYC to get paid is
  skipped, including whole platforms that do (Sherlock charges a
  per-report stake on every program).
- In-scope only, verification only, your own accounts only.
  Local fork PoCs only. Never mainnet, never move funds, never
  touch other users' data.
- Intent check before filing: if the team has ever seen, reviewed,
  audited or dismissed the mechanism, do NOT hunt or file it. No
  gray-zone bets. An audit finding the team never classified is a
  red flag, not a green light.
- File only on AUDITOR verdict READY (or CONDITIONALLY READY).
  One remediation round max. Never file NOT READY.
- Max 2 public Minor filings per hunter run. Public only.
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
- The live XE repo clone (clone it fresh, step 2 above).
- The `dao/` app, Minara/PredictAsiaX manual hunts, PoA and
  make.fun lanes, the LowEndTalk free-stuff watch: separate lanes,
  not part of this hunter.
- Python venvs, `__pycache__`, `.git` dirs, and the 185 MB
  Cybermes knowledge corpora (restore per step 3).

## Troubleshooting

- Helper 403s: the stored key lacks access for that endpoint.
  Reconnect that provider with the right key type (see the
  connector's CONNECTOR.md), never paste a key into a file.
- Filing blocked on sign-in: the browser session expired. The
  AUDITOR must NOT file; the draft stays ready and the run reports
  "ready to file, needs sign-in".
- Submission rate-limited ("too many reports"): wait ~19 minutes
  and retry in the same window. Never blindly retry an uncertain
  submission; check the account page + public API first.
- Hunter says "queue empty, HEAD unchanged": correct, it stops.
  It resumes automatically when a new HEAD ships or you add areas.
