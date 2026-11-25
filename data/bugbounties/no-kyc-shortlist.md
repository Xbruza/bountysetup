# No-KYC / No-Deposit Bug Bounty Shortlist

Verified live 2026-11-20 ~03:30 WIB. Source: bug-bounties.as93.net directory
(3,398 programs, generated 2026-11-19) filtered to direct submission
(non-platform), then live-verified. Directory max_payout values proved
STALE twice (LayerZero $15M -> live $3.5M; Filecoin $150k -> moved to
Immunefi) — never trust directory figures without a live check.
Re-scan 2026-11-20 ~17:35 WIB: directory data UNCHANGED (same generated
timestamp 2026-11-19T11:51:29Z, 0 added/removed/changed, byte-identical).
Re-filter of the unchanged data found 2 NEW verified entries (Bitcoin.de,
CoinJar) + 1 PARTIAL (Kraken, intake unconfirmed) that the first pass
missed.
Re-scan 2026-11-21 07:01 WIB: directory CHANGED (generated
2026-11-20T12:47:36Z, 3,399 programs, +1 added: ClosedLoop AI, 0 removed,
1,929 changed = tranco_rank only, 0 substantive). ClosedLoop AI
live-verified 07:01 WIB: NOT a bounty — page states "does not currently
operate a bug bounty program and does not offer monetary rewards",
recognition-only VDP (security@closedloop.sh, scope *.closedloop.sh).
Rejected, not added. Snapshot replaced.

## VERIFIED — direct submission, no platform, no KYC mentioned, no deposit

### 0. MNX — up to $100,000, paid in USDC (verified live 2026-11-20 ~10:05 WIB) — TOP PICK by ceiling
- Submit: email bounty@mnx.fi, subject "MNX security report", report in
  email body (plain text/Markdown), NEVER attachments (they never open
  them). PoC code pasted in email; if too long, secret GitHub gist or a
  private repo (only links they follow).
- Rewards: Critical = 10% of directly affected funds, min $25,000, max
  $100,000. High = $5,000–$25,000. Medium ($1,000–$5,000) and Low
  ($250–$1,000) rewards PAUSED since Sep 25, 2026 — only Critical/High
  pay now. Paid in USDC, aim to pay within 14 days of confirmation.
  No KYC mentioned anywhere on the page; payment requires "any
  applicable payment requirements, which we will disclose to the
  researcher" — open question, could include identity checks.
- Scope: mainnet contracts on MegaETH mainnet (chain ID 4326) — shared
  contracts MarginBank, LiquidityVault, AccountManager, SignatureVerifier,
  MNXMinimalForwarder, Guardian, MarginMath, GlobalIndexUpdater,
  OracleFactory + every market open for trading (Perpetual, IsolatedTrader,
  IsolatedADL, Evaluator, FundingOracle, price oracle). Source public:
  github.com/mnx-markets/contracts. Plus app/API: mnx.fi, app.mnx.fi,
  api.app.mnx.fi + backend (matching, collateral, oracle publishing,
  settlement) + signing services + production deployment.
- Priority targets: unauthorized withdrawals/transfers/trades, signing
  credential exposure, admin bypass, priv esc, unauthorized
  builds/deployments/upgrades, matching/balance/settlement manipulation,
  forged/replayed signatures, margin/funding/fees/liquidation/ADL
  accounting, oracle validation bypass.
- Dedup baseline: Centennial Systems audit Jun 23–Jul 23 2026 (commit
  8f4cebe4, differential review) — its findings are known/ineligible.
  Private known-issues register: 92 entries, commitments JSON published
  (SHA-256 hashes verifiable without disclosure). Vault-depositor-path
  reports currently INELIGIBLE (vault closed to external depositors;
  known vault vulns to be fixed before opening). DoS/griefing/gas not
  paid. Public portfolio/referral/builder/health endpoints intentionally
  unauthenticated (not eligible).
- Paid bounties so far: Sep 24 2026 $500 Low, Oct 20 2026 $250
  discretionary Low. Program in beta, terms may change.
- Testing: local deployments/forks for PoC; read-only chain inspection
  OK; prod app/API low-volume non-destructive checks with own accounts
  only; no live exploit trades, no moving funds, no DoS.
- Critical priority: initial report with asset + impact + credible attack
  path reserves priority even without full PoC.
- URL: https://docs.mnx.fi/security/bug-bounty

### 1. WalletConnect — TOP PICK (fits the 4-agent contract-hunting stack)
- Submit: form at https://walletconnect.network/security
- Contact: security@walletconnect.com (security.txt live, safe harbor full)
- Scope: smart contracts on Ethereum / Optimism / Base / Solana
  (StakeWeight contract, token contracts; deployment addresses at
  github.com/WalletConnect/contracts DEPLOYMENT_ADDRESSES.md) + frontend
  wallet-draining vulns on staking.walletconnect.network
- Rewards: by severity/impact, no fixed max published; contract + drainer
  frontend vulns eligible for "significantly higher rewards"
- No KYC mentioned anywhere in security.txt. No deposit (researchers never
  deposit anywhere — Immunefi "vault" is the program's own funds).

### 2. Socket — simplest, small payouts, web-app scope
- Submit: email security@socket.dev (safe harbor full)
- Bounty schedule (live on socket.dev/security/disclosure): $50-100 minor,
  $500-1000 real problem, $1000+ really bad
- Scope: socket.dev + subdomains, socketusercontent.com (their npm
  supply-chain scanner web app — NOT smart contracts)
- No KYC mentioned. No platform.

### 3. Web3 Foundation — discretionary, infra scope
- Submit: email security-report@web3.foundation (PGP key published)
- Rewards: "at the sole and absolute discretion of W3F", no amounts
  published, no KYC mentioned
- Scope: W3F programs/services/servers/network/infrastructure;
  W3F websites OUT of scope
- No platform, no deposit.

### 4. SpectroCoin — up to $15,000, paid in BTC/ETH (verified live 2026-11-20 ~10:00 WIB)
- Submit: email (directory: technical@spectrocoin.com; program page
  confirms email submission, "Report bug" button)
- Rewards: Critical $4,000–$15,000, High $1,000–$4,000, Medium
  $200–$1,000, Low up to $200; NO maximum cap stated. Paid in BTC/ETH —
  include your BTC/ETH address in the report. Sanctions exclusion only,
  no KYC mentioned.
- Scope: all SpectroCoin services — iOS/Android apps, Wallet, API,
  Merchant Tools, Cards, Exchange. Classes named: CSRF, XSS, code
  injection, RCE, privilege escalation, auth bypass, clickjacking,
  sensitive data leakage. Web/app scope, NOT smart contracts.
- URL: https://spectrocoin.com/bug-bounty.html

### 5. Shakepay — up to $5,000 CAD/month, paid in BTC/Interac (verified live 2026-11-20 ~10:00 WIB)
- Submit: email bugbounty@shakepay.com (PGP key published; report must
  include a CVSSv3 vector)
- Rewards: Severe up to $4,000 CAD, Moderate up to $1,000 CAD, Low up
  to $50 CAD, $5 CAD if no vuln but they changed code anyway. Max
  $5,000 CAD/month. Paid in Bitcoin or Interac e-transfer.
- Scope: shakepay.com, api.shakepay.com, Android/iOS apps. No KYC
  mentioned. Page is in French (legal.shakepay.com).
- URL: https://legal.shakepay.com/bug-bounty-program

### 6. Bitcoin.de — NEW, discretionary rewards, direct email (verified live 2026-11-20 ~17:35 WIB)
- Submit: email bugs2026@bitcoin.de, or the form on the program page
- Rewards: discretionary, "rate depends on the size and relevance of the
  safety leaks", no amounts published. No KYC mentioned anywhere on the
  page. No deposit.
- Scope: bitcoin.de platform (German BTC marketplace). No vuln classes
  listed; report exact URL + steps + screenshot.
- Page live (HTTP 200, 17.6 KB) at time of check.
- URL: https://www.bitcoin.de/en/bug-bounty

### 7. CoinJar — NEW, Bitcoin rewards, direct form (verified live 2026-11-20 ~17:35 WIB)
- Submit: form on the program page, or email security@coinjar.com
- Rewards: Bitcoin, no amounts published ("offers Bitcoin rewards to
  anyone who discovers a new vulnerability"). No KYC mentioned anywhere
  on the page. No deposit. Report must include a BTC address for payout.
- Scope: CoinJar code/platform. Classes named: XSS, CSRF, RCE,
  clickjacking, code injection, sensitive data leaks. DoS, social
  engineering, third-party software, physical access, usability issues
  ineligible. Must use own account if account access is needed.
- Page live (HTTP 200, 109 KB) at time of check.
- URL: https://www.coinjar.com/bounty

### 8. National Compute — Critical $10,000+, High $1,000, Medium $250, paid by PayPal (verified live 2026-11-22 ~03:28 WIB, user-supplied for the queue)
- Submit: email security@nationalcompute.com, English, one root cause per message. Also in /.well-known/security.txt. Safe harbor for rule-following research.
- Rewards: Critical $10,000 minimum (more at discretion, no stated ceiling), High $1,000, Medium $250, Low no reward. Paid in USD by PayPal, or platform credits at 1.5x. One reward per root cause. First report of a root cause (by mail arrival) wins.
- Payout gate: tax paperwork before any payment (W-9 US, W-8BEN otherwise) + must be lawfully payable (not sanctioned, not in an unpayable jurisdiction). No KYC/ID check mentioned for hunting or submitting. Staff/contractors (past 12 months) + households ineligible.
- Scope: nationalcompute.com + console.nationalcompute.com (console, /login, REST API /api, MCP server /mcp, docs center); auth.nationalcompute.com (sign-in, account creation, OAuth endpoints); docs/access hosts (hosts, not words); workspaces (own workspace); Grafana (own org); clusters/nodes/VM grants (own tenancy, node-level testing incl. container/VM escape). Other orgs' data: never. Third-party services: no.
- Rules: test only what you own (max 5 test accounts, named in report); stop at proof; leave nothing behind; no volume (under 5 req/s per host, rate-limit burst max 100 vs own account); no social engineering. Authenticated probing needs own test accounts (sign-up on the sign-in page).
- Known/accepted (NOT findings): org API token scopes narrow nothing; emailed sign-in link signs in whoever opens it within 24h; sessions have no age limit (30 days without use); OAuth tokens keep refreshing after sign-out by design; Grafana /bootdata, /swagger, /api/health public by design; old IdP paths redirect/404; one shared signing key across issuers is public by design (but a wrongly-accepted token IS a finding); deploy.nationalcompute.com (Argo CD) sign-in page + /swagger.json + settings + /api/version public (secrets/repos/apps/clusters/credentials on them ARE findings).
- URL: https://docs.nationalcompute.com/bug-bounty/
- Queue: after Inverse Finance pass 3 (running) and the Mantis queue (Flex, Monolith, Stake DAO). Workspace: ~/workspace/national-compute/scope.md

## PARTIAL — direct but NOT no-KYC

### BugEx / BYDFi — platform, KYC reserved, web/app scope (checked 2026-11-20 ~09:51 WIB)
- Program page: https://bugex.ai/programs/bydfi (JS app, needs ~15s render)
- BYDFi: crypto exchange (2020, 1M+ users, 190+ countries; spot, perps, copy trading, bots)
- Bounty $10–$15,670, BEMIX points: LOW 1-7pts $10/pt, MEDIUM 8-14pts $100/pt, HIGH 15-21pts $200/pt, CRITICAL 22-30pts $1,500/pt
- Scope: *.bydfi.com web + iOS/Android apps. NO smart contracts.
- SLA: first response 24h, triage 3d, resolution 30d, payment 14d
- Submission needs BugEx account ("Log in as a human hacker"); rules behind login
- KYC: BugEx Terms §4 reserves the right to REQUIRE identity verification (KYC) at its sole discretion — NOT guaranteed no-KYC. No deposit mentioned. Platform explicitly defines an "AI Agent" role (operators responsible for agent submissions) — fits the agent setup.
- Verdict: small ceiling, web/app hunting (different skill set from contract hunts), KYC possible. User sent the link 09:51 WIB, asked to check only.

### Ethereum Foundation — up to $1,000,000, but identity proof required
- Submit: own form bbp-form.ethereum.org (live, "Open for submissions")
- Max: up to $1,000,000 (Low $2k / Medium $10k / High $50k / Critical $1M
  caps shown on page; Glamsterdam multipliers active)
- Rules: "Local laws require us to ask for proof of your identity" —
  identity proof required for awards. Sanctions lists excluded.
- Scope: protocol spec, execution/consensus clients (Geth, Reth,
  Nethermind, Besu, Erigon, Lighthouse, Prysm, Teku...), Solidity/Vyper
  compilers, deposit contract. Very hard scope, no app-level bugs.

### Kraken — PARTIAL, likely direct but intake/rewards unconfirmed (checked 2026-11-20 ~17:35 WIB)
- Program page live: https://www.kraken.com/features/security/bug-bounty
  (policy preamble only in fetched text, no reward table, no visible
  submission form). Old HackerOne program hackerone.com/krakenfx is 404
  (dead). Directory lists contact bugbounty@kraken.com with bounty
  rewards. A live-checked list (Invadel, Nov 16, 2026) claims Kraken is
  self-hosted, paid in BTC, top reward $1,500,000 — NOT confirmed from
  Kraken's own page.
- Verdict: promising (major exchange, platform program dead, own page
  live) but do NOT hunt until a live-browser render confirms the
  submission channel and reward tiers. If confirmed direct, it would be
  the highest-ceiling no-KYC program after MNX.

## DEAD / MOVED TO PLATFORM — do not pitch as no-KYC

- LayerZero: gitbook bounty page 404 (docs moved); live program is on
  Immunefi, max $3,500,000, KYC required, PoC required.
- Filecoin: security.filecoin.io says email reports are NO LONGER eligible
  for monetary rewards — must use Immunefi.
- Across Protocol: docs bounty page now renders only the API Reference
  landing (page gone); email bugs@umaproject.org unverified.
- Polygon: submission via HackerOne (platform).
- Exodus: HackerOne program (hackerone.com/exodus), $100 min / $100,000
  max per HackerOne; directory $18,000 figure stale. Platform, not
  direct.
- Crypto.com: HackerOne (hackerone.com/crypto), up to $2,000,000.
  Platform, not direct.
- Coinbase: HackerOne for Web2 (up to $15,000 Critical, Extreme tier up
  to $1,000,000) + Cantina for Web3 smart contracts (up to $5,000,000).
  Platform, not direct.
- Bybit: HackerOne (hackerone.com/bybit_fintech), Low $50-600 / Medium
  $600-1,500 / High $1,500-5,000 / Critical $5,000-10,000 (Web2); Web3
  Critical up to $100,000. Platform, not direct.
- Stoa (stoadex.com): paid bug bounty ENDED 17 Nov 2026, no cash rewards
  anymore. Reports still welcome via GitHub private advisory only, valid
  findings credited by name or anonymously in the security review. Scope:
  own contracts on Elysium and Robinhood Chain + app (harmful-transaction
  issues). Credit only, not worth hunting for money. Checked live
  2026-11-20 ~21:51 WIB.

## Notes
- Full directory snapshot: ~/workspace/bug-bounties/programs.json
- 697 direct (non-platform) bounty programs exist in the directory;
  crypto-ish subset was 68, mostly noise (banks, exchanges' homepages,
  dead Medium posts). The 4 above are the live-verified ones worth
  joining. Re-run the filter if a new program is needed.
