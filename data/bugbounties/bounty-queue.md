# Bug Bounty Queue (user order 2026-11-22 ~14:31 WIB)

Rule: finish current work 1/1 first. Do NOT start these now. Queue order below, one at a time, no rush, quality over speed, no hallucination.

Current work first: Stake DAO CLOSED 0/0 (pass 1 + pass 2 done 2026-11-22) → National Compute CLOSED 0/0 (pass 1 done ~15:43 WIB) → Guardian RAAC CLOSED 0/0 (pass 1 done ~15:58 WIB) → Cantina Exactly CLOSED 0/0 (pass 1 done ~16:24 WIB) → StoaDEX CLOSED 0/0 (pass 1 done ~16:45 WIB) → Hastra SKIPPED 2026-11-22 ~18:01 WIB by user decision ("Yg ada biaya skip") → Ticko BLOCKED on user's Discord access code. Queue exhausted except Ticko.

## 1. Guardian Defender — RAAC Core Contracts Bounty Contest
- URL: https://defender.guardianaudits.com/contests/01a1a379-b7c1-72d9-8075-5318b386f2e4
- Repo: https://github.com/GuardianOrg/RAAC-Core-Contracts-Bounty-Contest
- Commit in scope: 97587ed3688ff62ab67e292719bbd4a33140b264
- 30-day public vulnerability bounty contest on Guardian Defender for RAAC Core Contracts (LendingPool, StabilityPool, oracles, tokens, math libs).
- Status: CLOSED 2026-11-22 ~15:58 WIB, pass 1 0 fileable Critical (2 candidates + 20 killed leads). Contest ends 2026-12-09T15:00:00Z, Critical only (>20% funds), $100k seasonal pool split equally, KYC required. G1 weak (manager-gated finalizeLiquidation), G2 real but <1%/yr (DEToken interest-on-interest). Security review PDF needs Guardian login (401). No PoCs, nothing filed.

## 2. Cantina — Exactly Bug Bounty
- URL: https://cantina.xyz/bounties/276fd65d-f84d-4be3-8e2a-88f1dc1cd959
- Exactly protocol (fixed/variable rate market) + Exa App (ERC-6900 smart account + card).
- PoC code REQUIRED for High/Critical. Rewards denominated in USD, Critical capped at 10% of economic damage.
- FLAG: KYC REQUIRED to receive a reward (government ID, legal name, country of residence).
- Status: CLOSED 2026-11-22 ~16:24 WIB, pass 1 0 fileable (20 leads killed). Live, Self-Triaged, start 12 Nov 2026, no end date; Max $25,000, Critical $10,000-$25,000, High $5,000-$10,000; DEPOSIT REQUIRED $50; 66 findings already submitted; KYC required. No PoCs, nothing filed.

## 3. StoaDEX — Bug Bounty (CREDIT ONLY, no cash)
- URL: https://stoadex.com/docs/bug-bounty
- FLAG: paid bounty ENDED 17 November 2026. Stoa no longer pays cash rewards. Reports still welcome via GitHub private report; valid findings credited in the security review only, no cash.
- Scope: Stoa's own contracts on Elysium and Robinhood Chain (StoaRouter, venue adapters, StoaPool maker pools, MakerRegistry, FeeDistributor, StoaBuyback, BondRegistry, SpotlightMarket, RugCover, StoaLimitV2, timelock/admin Safe) + the app for harmful-transaction issues.
- Status: CLOSED 2026-11-22 ~16:45 WIB, pass 1 0 fileable (20 killed leads, repo HEAD 90f390fa). Nothing filed, no PoCs.

## 4. Hastra — Bug Bounty (PAID SUBMISSION FEE)
- URL: https://bugbounty.hastra.io/
- FLAG: $10 non-refundable submission fee in USDC.SOL per submission (burn to incinerator wallet). Conflicts with the no-paid rule; flag to user before starting.
- Status: SKIPPED 2026-11-22 ~18:01 WIB by user decision ("Yg ada biaya skip"). Never started, no fee paid.

## 5. Ticko — Bug Bounty (already joined, BLOCKED)
- URL: https://docs.ticko.xyz/resources/ticko-bug-bounty
- Joined 2026-11-19, testnet-only black-box, reports to security@ticko.market direct only.
- BLOCKED: needs the user to claim an access code in Discord #access-code (discord.gg/ticko). Bounded probing only, no grind for Critical without a concrete lead.
- Rewards in USDT: Critical up to 200,000, High 25,000, Medium 3,000, Others 50. KYC/payout verification required for reward. Do NOT test on Mainnet/production.
- Status: QUEUED (blocked on user's Discord access code).

## 6. bugbounty.fyi — fresh no-KYC queue (added 2026-11-23 ~03:20 WIB)
- Source: https://bugbounty.fyi/programs?kind=bounty&sort=recent&nokyc=true — 109 paying programs flagged no-KYC, sorted newest first. Directory facts checked hourly; program policy always wins, verify live before testing.
- Standing filters: gratis (no fee/deposit), no KYC, newest first. Anti-bot posture verified per program: runnable PoC required, local-fork testing only, no mass automated traffic, one human-voice report.
- Order (newest first):
  1. Metric (Immunefi, NEW program live 10 Nov 2026, Critical $500k / High $50k / Med $10k / Low $1k, USDC on Ethereum, KYC explicitly NOT required for payout per policy, runnable PoC always required, scope 4 assets: oracle/periphery/pool-contracts + metric.xyz, audits Zellic Jun 2026 + Sherlock Oct 2026 = dedup baseline, local forks only, no automated traffic). TOP PICK.
  2. Zest Protocol V2 (Immunefi, new scope 10+17 Nov 2026, Critical $100k / High $20k, USDC, no KYC, PoC required, 32 Stacks/Clarity contracts, non-EVM. CAUTION: Immunefi vault holds only ~$150 USDC, payout may be capped by vault balance).
  3. Spark (Immunefi, new scope 17 Nov 2026, Critical contract $5M / High $100k, DAI, no KYC, 385 assets, mature Maker/Spark codebase, heavily eyed).
  4. Sky (Immunefi, new scope, Critical contract $10M / High $100k, DAI+USDS, no KYC, 258 assets, MakerDAO core, heavily eyed).
  5. Twyne (Immunefi, $50k Critical, from $3,000), DAWN USD.infra Vault (Immunefi, $50k), Origin Protocol (Immunefi, new scope, $1M), GMX (Immunefi, $5M), Gnosis Chain (Immunefi, $2M), Synthetix (Immunefi, $100k).
  - Cantina programs in the no-KYC list (Pendle $2M, Morpho $2.5M) NOT verified no-KYC live; Cantina normally requires KYC to receive rewards, verify before hunting.
- Status: Metric pass 1 DONE 2026-11-23 ~03:28 WIB: 0/0 (0 candidates, 114 killed leads: oracle 48, periphery 33, pool 33), CLOSED per stop-loss, nothing filed. Report ~/workspace/metric/leads/hunt1-report.md. Spark pass 1 DONE 2026-11-23 ~04:48 WIB: 0/0 (0 candidates, 33 killed leads: Gnosis 17, ETH/Base/Arb 16), CLOSED per stop-loss, nothing filed. Report ~/workspace/spark/leads/hunt1-report.md. §6 queue EXHAUSTED. Pendle SKIPPED 2026-11-23 ~08:45 WIB (Cantina deposit $100, fee). Morpho SKIPPED 2026-11-23 ~08:5x WIB (Cantina deposit $30 + KYC required for payout: full name, DOB, passport/ID; scope now web-only, all contracts removed 3 Sep 2026). LESSON: Cantina ToS §3(i) mandates KYC + tax form before ANY payout platform-wide, so the directory "No KYC" flag on Cantina programs is unreliable; 43/49 Cantina programs charge a fee/deposit. Zest V2 deprioritized (Immunefi vault ~$150 caps any payout, Clarity hunt not worth it). Watcher (bugbounty-fyi-nokyc-watcher, 12h) waits for new programs. Enzyme Onyx pass 1 DONE 2026-11-23 ~08:35 WIB: 0/0 (0 candidates, 52 killed leads: issuance 20, value/fees 32), CLOSED per stop-loss, nothing filed. DAWN pass 1 DONE 2026-11-23 ~08:20 WIB: 0/0 (0 candidates, 18 killed leads), CLOSED per stop-loss, nothing filed. Report ~/workspace/dawn/leads/hunt1-report.md. BSC feed guards enforced (onlyUpdater, monotonicity, 20% APY cap); Solana vault1 TVL ~$9.91M, share price matches BSC feed within 0.004%; borrower-whitelist NOT directly verified (no IDL). Twyne pass 1 DONE 2026-11-23 ~07:37 WIB: 0/0 (0 candidates, 24 killed leads), CLOSED per stop-loss, nothing filed.
