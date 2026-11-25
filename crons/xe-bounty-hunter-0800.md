---
id: xe-bounty-hunter-0800
enabled: true
mode: task
schedule:
  kind: daily
  timezone: Asia/Jakarta
  time: 08:00:00
timeout_secs: 7200
delivery:
  - chat_id: <YOUR_CHAT_ID>
---
# XE Bounty hunter — pagi (4-agent: RESEARCHER + BUILDER + AUDITOR + ORCHESTRATOR)

Four-agent bug hunt on xeprotocol/xe (XE Bounty testnet, account <YOUR_BOUNTY_USERNAME> / GitHub <YOUR_GITHUB_HANDLE>). Max 2 bugs filed per run. Report the result to this chat when done.

## Loop (in order, every run)
1. Check repo HEAD: `git ls-remote https://github.com/xeprotocol/xe HEAD`. Check our filed tickets via public API `curl https://bounty.xe.network/v1/tickets/XE-<id>` for <YOUR_FILED_TICKET_IDS> (status, assessed_tier, award_xe). If any ticket changed status or got a tier/award, say so in the report — that is a win.
2. Pick the next area: read `~/workspace/xe-bounty/xingchi-areas.json`, take the first item from `queue`, move it to `done`, save the file. If the queue is empty, re-hunt the oldest `done` area only if a new HEAD shipped since it was hunted; otherwise report "queue empty, HEAD unchanged" and stop.
3. RESEARCHER hunts: run `python3 ~/workspace/xe-bounty/xingchi-hunt.py --area <slug> --files <repo-relative files> --grep '<regex>' --focus '<what to hunt>'`. The script already carries the known-filed list and the known desk duplicate families (XE-9581, XE-12954, XE-0121, XE-8572, XE-8592, XE-17819) in its prompt. Read its output file in `~/workspace/xe-bounty/leads-xingchi/<slug>.md`.
4. RESEARCHER verifies: for each candidate (max 3), run a focused verification via `~/workspace/custom-connectors/custom.xingchiapi/bin/xingchi.py chat --max-tokens 4000 --prompt '...exact code excerpts... YES/NO per candidate...'`. Drop any candidate <RESEARCHER_MODEL> says is not real.
5. ORCHESTRATOR dedups: search the desk `https://bounty.xe.network/v1/tickets?q=<keywords>&limit=5` for each surviving candidate, read full bodies of close hits. Same root cause / vulnerable code path = duplicate, drop it. Never file SSE re-validation variants (XE-18076), never file N1 micro-mislabels before XE-18358 is triaged, M2-3 parsePagination goes last.
6. BUILDER PoCs survivors: dispatch a Muse subagent per surviving candidate, one at a time, brief = role `~/workspace/xe-bounty/agents/BUILDER.md` (<CODER_MODEL> v4.1 Flash via `~/workspace/custom-connectors/custom.packet/bin/packet.py chat` for implementation help) + candidate spec. BUILDER runs builds, PoCs, and debugging on your hunt compute box via the MCP `shell` tool (<YOUR_COMPUTE_CONNECTOR>, box must be running; wake it first if hibernated). Fallback while the Simular connector is down: build `xe` from HEAD on the local Hatch VM, local loopback node or binary only, throwaway accounts/seeds, no live testnet traffic, no other users. Write the PoC file to `~/workspace/xe-bounty/leads-minor/<slug>-poc.md` (or `leads-xingchi/` for <RESEARCHER_MODEL>-origin candidates) with verdict, exact commands, exact output, exit codes. Drop anything not confirmed live. Clean up scratch dirs, seeds, and toolchain caches after the run (`/tmp` is a 512 MB tmpfs, build under `~/workspace/xe-bounty/.poc-*/`).
6b. AUDITOR audits and files each confirmed PoC: spawn a fresh Muse subagent per PoC, brief = role `~/workspace/xe-bounty/agents/AUDITOR.md` (v2.0: AUDITOR & SUBMISSION OPERATOR) + PoC file + draft file. AUDITOR independently re-runs the reproduction and the control, re-checks dedup, writes `~/workspace/xe-bounty/<slug>-audit.md` with sections A-M and exactly one verdict (READY / CONDITIONALLY READY / NOT READY), then files the report itself via a browser task as <YOUR_BOUNTY_USERNAME> on bounty.xe.network on READY or CONDITIONALLY READY (your dispatch is the authorization: max 2 public Minor per run, PUBLIC only, uncheck "Keep this report private" — it is checked by default, claimed Minor, one at a time). Filing always happens from this chat via the cloud browser task, never from inside the hunt compute box. On NOT READY, it sends findings to BUILDER once, re-verifies the fix independently, then re-issues the verdict. Never file a NOT READY candidate. If the submission is rate-limited ("too many reports from this address"), wait ~19 minutes and retry in the same window; never blindly retry an uncertain submission — check the account page + public API first; never create a duplicate ticket.
7. Verify every receipt yourself via the public API (ticket New, public) and record ID + URL. If the browser sign-in fails unattended (session expired and login needs the user), AUDITOR does NOT file: draft stays ready, report it as "ready to file, needs sign-in".

## Area map (files + focus for step 3)
- web-assets-errors: files `web/assets/wallet.js web/assets/vault.js web/assets/chat.js web/assets/chat-auth.js`, grep `fetch|catch|error|localStorage|JSON.parse`, focus "silent fallbacks, swallowed fetch errors, corrupt-state handling in the web wallet/chat UI".
- cli-receive-mint: files `cmd/xe/main.go`, grep `cmdReceive|cmdMint|GetPending|GetBalances`, focus "receive/mint error paths that turn a failed read into a false success message".
- api-auth: files `api/chat_auth.go client/chat.go web/assets/chat-auth.js`, grep `challenge|sign|expir|valid`, focus "auth challenge handling gaps other than the URL-query issue (XE-16797)".
- dao-ui: files `dao/ui.py dao/templates/decisions.html`, grep `decided|limit|total|page`, focus "counts, caps, and totals shown wrong in the DAO UI".
- node-vm: files `node/node.go node/lease_renew.go`, grep `XCU|XE|refund|earn|cost`, focus "unit mislabels other than the XE-18358 family, only file as follow-up naming XE-18358 if triaged".
- docs-cli-drift: files `docs/cli.md cmd/xe/main.go`, grep `Usage|flag\.`, focus "CLI help/docs claims vs actual flags and defaults".
- core-encoding: files `core/encoding.go`, grep `Unmarshal|offset|Genesis`, focus "decoding gaps with a live caller, not dead code".
- gossip-retry: files `net/gossip.go node/node.go`, grep `retry|backoff|Subscribe`, focus "retry/timeout paths that silently drop work".

## Report to this chat
Ticket IDs + raw URLs for anything filed (code block), status changes/wins if any, and for runs with no filing: which area was hunted, what <RESEARCHER_MODEL> found, and why each candidate died (not real / duplicate + ticket ID / PoC failed / audit NOT READY + top finding). Keep it terse, no fluff, no em-dash. Log the run outcome in the daily log `~/memory/YYYY-MM-DD.md`; do not edit MEMORY.md from this job.
