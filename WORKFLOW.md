# Workflow - the 4-agent loop

## The loop (every hunter run, in order)

0. **Scope freeze + web recon (web programs only).** Read the program
   policy, write `scope.md` + `allowlist.txt`, then run Beacon Levels
   1-2 per `agents/WEB-RECON.md` on hunt compute box into `<program>/recon/`
   (`live.txt`, `urls.txt`, `params.txt`, `js-endpoints.txt`).
   Skip for repo-only hunts. RESEARCHER triages the recon files
   at Level 3. No host outside the allowlist is ever touched.
1. **HEAD + ticket check.** `git ls-remote` the target repo HEAD.
   Check each of your filed reports via the program's public desk/API
   (status, tier, award). A status change or a tier/award is a win:
   report it.
2. **Next area.** Take the first item from
   `scripts/xingchi-areas.json` `queue`, move it to `done`, save.
   Queue empty: re-hunt the oldest `done` area only if a new HEAD
   shipped since it was hunted. Otherwise report "queue empty, HEAD
   unchanged" and stop.
3. **RESEARCHER hunts** (`agents/RESEARCHER.md`). Driver:
   `scripts/xingchi-hunt.py --area <slug> --files <files> --grep
   '<regex>' --focus '<what to hunt>'`. Output:
   `leads-xingchi/<slug>.md`. At most 3 candidates, Minor class
   only. Never invent a bug; dead ends are reported as dead ends.
4. **RESEARCHER verifies** each candidate with exact code excerpts,
   YES/NO per candidate. Drop anything not real.
5. **ORCHESTRATOR dedups** (`agents/ORCHESTRATOR.md`). Search the
   public desk for each survivor, read full bodies of close hits.
   Same root cause or same vulnerable code path = duplicate, drop
   it. Known desk duplicate families live in `xingchi-hunt.py`
   (`KNOWN_DESK_FAMILIES`); your own filed tickets in
   `KNOWN_FILED`.
5b. **DEVILS-ADVOCATE gate** (`agents/DEVILS-ADVOCATE.md`). A <CODER_MODEL>
   call per surviving candidate batch (<ADVOCATE_PROVIDER> helper, role file as
   system) argues the team's side (intended, reviewed before,
   audit-documented, no impact) and kills or downgrades before BUILDER.
   Only SURVIVE candidates reach BUILDER. If all die, the pass closes 0/0.
6. **BUILDER proves** (`agents/BUILDER.md`). One subagent per
   surviving candidate, one at a time, on the hunt compute box.
   Live fork PoC with exact commands, exact output, exit codes,
   written to `leads-minor/<slug>-poc.md`. For web candidates, BUILDER
   uses the Level 4 toolkit in `agents/WEB-RECON.md` (ffuf rate-limited,
   Dalfox, gowitness, interactsh only where allowed, soft-404 baseline
   first). Anything not confirmed
   live is dropped. Clean up scratch dirs, seeds and caches after
   the run.
7. **AUDITOR audits and files** (`agents/AUDITOR.md`). A fresh
   subagent per PoC independently re-runs the reproduction and the
   control, re-checks dedup, writes the audit with sections A-M
   and exactly one verdict: READY / CONDITIONALLY READY / NOT READY.
   On READY or CONDITIONALLY READY it files the report itself via
   the browser session (public, Minor, one at a time, max 2 per
   run). On NOT READY it sends findings to BUILDER once,
   re-verifies the fix independently, then re-issues the verdict.
   Never file NOT READY.
8. **Receipt check.** Verify every filing yourself via the public
   API (ticket New, public) and record ID + URL. If the browser
   sign-in fails unattended, do NOT file: draft stays ready, report
   "ready to file, needs sign-in".

## Gates (a candidate dies unless it passes all of them)

- **In scope:** host is on the program allowlist (`scope.md` +
  `allowlist.txt` per `agents/WEB-RECON.md` Step 0). Out-of-scope host
  kills the candidate even if a tool or model suggested it.
- **Real:** researcher verification says YES on exact code.
- **Novel:** not a duplicate of any filed ticket or known desk family.
- **Proven:** BUILDER PoC reproduces it live on a fork.
- **Intended:** the intent check passes. Evidence the team did NOT
  intend this behaviour must come from design docs, audit answers
  or code comments. "The code does this" is not evidence. If the
  team has ever seen, reviewed, audited or dismissed the mechanism,
  do not file. Audit findings the team never classified are a red
  flag, not a green light.
- **Audited:** AUDITOR verdict READY or CONDITIONALLY READY after
  independent re-run + control + dedup.

## Watchers (every 12h, silent unless something is new)

- `bugbounty-fyi-nokyc-watcher`: fetch the no-KYC program list,
  diff slugs against `data/bugbounties/bugbounty-fyi-seen.json`.
  New slugs get live-verified (cash payout, no identity check, no
  fee, top reward, platform, scope, what is new). Verified programs
  go to the queue. Never start hunting from a watcher run.
- `no-kyc-program-watcher`: fetch the directory snapshot, diff
  against `data/bugbounties/programs.json`. Added/changed programs
  get filtered (direct submission, non-platform, no KYC, no
  deposit) and live-verified on their program page before they
  enter `data/bugbounties/no-kyc-shortlist.md`.

## Stop-loss and queue discipline

- One program, one full pass. 0 reportable findings means the
  program is CLOSED. Reopen only on new scope, new code, or a new
  HEAD.
- Hunt novel mechanisms only: things in no audit or known issue,
  unaudited inter-contract interactions, live-only conditions, or
  code new since the last audit.
- Never chase a rejected report's twin. A rejection that says
  "known/intended behaviour, reviewed before" kills the whole
  family, not just that ticket.
- The queue is the only source of what to hunt next. Do not hunt
  off-queue because a link looked interesting.

## Report voice and filing

- One professional ethical hacker, English, neat human writing.
  No agent/subagent talk, no em-dash.
- Contact block comes from `skills-local/local-bounty-reporting/templates/report.md`
  (fill your own email + payout addresses there).
- Public reports only, at the severity the PoC proves.
- Filing happens from the operator chat via the browser session, never
  from inside the hunt compute box (no session there).
- A failed script still becomes a report if the bug is evidenced;
  disclose the limitation in the report.
- PoC size limits apply per platform (e.g. some cap the PoC text
  field); paste the PoC into the form when it fits, upload as a
  file when it does not.

## Run report (every hunter run reports this)

Report IDs + raw URLs for anything filed, status changes/wins if
any, and for runs with no filing: which area was hunted, what the
researcher found, and why each candidate died (not real /
duplicate + ticket ID / PoC failed / audit NOT READY + top
finding). Terse, no fluff.
