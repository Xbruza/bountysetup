# <RESEARCHER_MODEL> Hunter (local-xingchi-hunter)

Second-opinion bug hunter for XE Bounty. <RESEARCHER_MODEL> <MODEL>.1-sol hunts, Muse verifies. Never the other way round.

## Roles
- **<RESEARCHER_MODEL> (hunter):** reads code excerpts for one target area, proposes at most 3 NEW Minor-class candidates. Fresh eyes, different failure modes from Muse's own hunts.
- **Muse (verifier):** dedup-checks every candidate against the desk API, runs a live PoC (local node / binary, throwaway accounts), writes the report draft, files via browser. No <RESEARCHER_MODEL> output is filed verbatim or unverified.

## Tool
`~/workspace/xe-bounty/xingchi-hunt.py` — calls the stored custom.xingchiapi connection via `~/workspace/custom-connectors/custom.xingchiapi/bin/xingchi.py` (Responses API, UA claude-code/2.0.0, model <MODEL>.1-sol, max-tokens 8000). Output lands in `~/workspace/xe-bounty/leads-xingchi/<area>.md` with the raw reply marked UNVERIFIED plus usage.

Usage:
```bash
python3 ~/workspace/xe-bounty/xingchi-hunt.py --area <slug> --files <repo-rel paths...> \
  --grep '<regex>' --focus '<what to hunt>'
```
`--grep` sends only matching lines (+2 context), keeps prompts small. Omit it to send file heads.

## 3-AGENT SYSTEM (user order 2026-11-20 ~01:27 WIB)
- RESEARCHER (<RESEARCHER_MODEL> <MODEL>.1-sol): role file `~/workspace/xe-bounty/agents/RESEARCHER.md` = user's MASTER SYSTEM ROLE v1.0 verbatim + XE adaptation + full skill pack (local-bounty-reporting + local-agentic-bug-hunter SKILL.md verbatim, 38,704 bytes total). Sent as `instructions` on every hunt (xingchi.py `--instructions`, default in xingchi-hunt.py). Delivers Bounty Intelligence Report (Part A §12 format) with PoC handoff to BUILDER.
- ORCHESTRATOR (Muse): `agents/ORCHESTRATOR.md` — picks area, dedups, dispatches BUILDER, files, reports.
- BUILDER (Muse subagent): `agents/BUILDER.md` — live PoC only, one candidate at a time.
- First run under the new system 2026-11-20 ~01:30 WIB cli-receive-mint: 0 candidates, researcher correctly killed all 3 leads as XE-8572/XE-12954/XE-0121/XE-17819 families and gave a bounded follow-up; orchestrator checked full cmdReceive/cmdMint bodies — success output is conditional on SubmitBlock success, no distinct defect, area closed. Cost 12,531 tokens.

## Rules
- One area per run. Small, targeted excerpts only; <RESEARCHER_MODEL> billing is inflated (tiny prompts billed thousands of tokens), user authorized heavy use 2026-11-19, but do not send whole files.
- The prompt carries the known-filed list (XE-16797, XE-16935, XE-18358, XE-18453, XE-18874, XE-18990, old 4, XE-18076). <RESEARCHER_MODEL> must not re-propose those families, and never any SSE re-validation variant.
- Empty reply = no finding, not a failure to retry blindly. One retry max with a smaller prompt, then move on.
- After a run: Muse reads the output file, dedups each candidate (desk search), PoCs the survivors, files the confirmed ones public Minor. Unconfirmed candidates stay in the file, marked as such.
- <RESEARCHER_MODEL> never files, never grades, never touches the network, never sees secrets. No keys in prompts.

## Areas already hunted by Muse (do not re-run blindly)
M1 wallet/CLI/SDK, M2 node API/chat, M3 DAO/statechain, M4 desk/web, N1 VM/lease/cert, N2 gossip/sync/vote, N3 ledger/amounts/fees. Pick fresh angles: docs-vs-code drift, CLI help-text drift, error-message consistency, web UI validation.
