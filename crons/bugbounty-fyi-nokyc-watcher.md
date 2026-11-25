---
id: bugbounty-fyi-nokyc-watcher
enabled: true
mode: task
schedule:
  kind: interval
  every: 12h
timeout_secs: 7200
delivery:
  - chat_id: <YOUR_CHAT_ID>
---
Idle check for new no-KYC bug bounties on bugbounty.fyi (user order 2026-11-23: when there is no bounty work running, re-check this directory for new programs).

Each run:
1. Fetch https://bugbounty.fyi/programs?kind=bounty&sort=recent&nokyc=true with Camoufox (~/workspace/camoufox/venv/bin/python ~/workspace/camoufox/cfx.py, JS-heavy page, use --wait-ms 12000). Extract the program slugs from the results table in order (top 50, most recently changed first).
2. Diff against the baseline at ~/workspace/bug-bounties/bugbounty-fyi-seen.json (field "slugs").
3. If NO new slug: stay silent, change nothing, do not message the user.
4. If there ARE new slugs: for each new program, open its bugbounty.fyi program page (https://bugbounty.fyi/programs/<slug>) and verify live from its "At a glance" section: pays cash, no identity check to get paid, no fee to submit, top reward, platform, scope size, and what is new (new program vs new scope). Skip anything that turns out to require KYC or a fee.
5. Update bugbounty-fyi-seen.json with the new full top-50 slug list and today's date.
6. Report to this chat in Indonesian, terse, no em-dash: the new programs only, newest first, each with name, platform, top reward, what is new, and its program link. One line per program plus one line saying they are queued, not hunted.
7. Do NOT start hunting any of them. Hunting starts only on the user's go-ahead. Do not edit MEMORY.md; log the run to ~/memory/YYYY-MM-DD.md only when something new was found.
