---
id: no-kyc-program-watcher
enabled: true
mode: task
schedule:
  kind: interval
  every: 12h
timeout_secs: 7200
delivery:
  - chat_id: <YOUR_CHAT_ID>
---
Watch for NEW no-KYC bug bounty programs. Every run:
1. Fetch https://bug-bounties.as93.net/api/programs.json fresh and compare against the saved snapshot at ~/workspace/bug-bounties/programs.json (3,398 programs, generated 2026-11-19T11:51:29Z as of 2026-11-20). Note the `generated` timestamp and counts of added/removed/changed programs.
2. If the directory is unchanged AND no new program qualifies, stay silent: do not send a chat message, just log the check to the daily log ~/memory/YYYY-MM-DD.md.
3. If programs were added or changed: filter to direct submission (non-platform: NOT Immunefi/HackerOne/Bugcrowd/YesWeHack/Intigriti), no KYC mentioned, no deposit required. Skip anything already in ~/workspace/bug-bounties/no-kyc-shortlist.md (WalletConnect, Socket, Web3 Foundation, SpectroCoin, Shakepay, BugEx/BYDFi, Ethereum Foundation, LayerZero, Filecoin, Across, Polygon, Bitcoin.de, CoinJar, Kraken partial, Exodus, Crypto.com, Coinbase, Bybit, Definity, Merkl, MNX).
4. For each surviving candidate, live-verify its program page: submission method (email/form/direct), scope, rewards (amounts + currency; directory max_payout values are unreliable/stale, always verify on the live page), safe harbor, and whether KYC/identity is required at any stage (especially payout).
5. Update ~/workspace/bug-bounties/no-kyc-shortlist.md with the new verified entries (mark NEW with verification time) and replace the snapshot only when the fresh fetch differs. Keep existing entries intact.
6. Report to this chat ONLY when a new verified no-KYC program was found: name, submission method, rewards, scope, program URL. Do NOT start a hunt — the user decides which program to gas. Do not edit MEMORY.md; observations go to the daily log.
Constraints: read-only research (fetches + page reads only). Slow, normal User-Agent, no bursts. Never paste or store secrets.
