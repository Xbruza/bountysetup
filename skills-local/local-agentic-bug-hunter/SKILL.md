# Agentic Bug Hunter - bug bounty workflow

AI-powered bug bounty hunting, recon to report. Source: AwareXone `Agentic-Bug-Hunter` (MIT), cloned 2026-11-14 to `~/workspace/tools/agentic-bug-hunter/`. Full upstream material lives under `references/`: the master workflow (`upstream-SKILL.md`, 48KB), the plugin guide (`AGENTS.md`), 9 specialist agent prompts (`references/agents/`), and 24 domain skills (`references/skills/`).

Use this skill for:
- starting a hunt on a new target (recon, scope check, attack surface ranking)
- hunting a specific vuln class (IDOR, SSRF, XSS, auth bypass, race conditions, GraphQL, OAuth, SSTI, business logic, cache poisoning, request smuggling, LLM/AI features)
- auditing source code (web2 or smart contracts) for vulns
- validating a finding before reporting it
- writing a HackerOne / Bugcrowd / Intigriti / Immunefi report
- token and meme-coin audits (rug pull, authority checks, bonding curve, LP attacks)
- chaining bugs A to B to C for higher payout

Don't use for: attacking anything out of scope (see Authorization below), theoretical vuln writeups with no PoC, or credential spraying without an explicit user go-ahead.

## Authorization (hard rule)

**READ FULL SCOPE FIRST.** Verify every asset and domain is owned by the target org or listed in the bounty program scope before touching it. Only hunt targets the user owns, or that are in scope for a program the user is enrolled in. Never probe out-of-scope assets, never spray credentials, never run destructive tests. The user authorizes local session cookies for authorized testing only. If scope is unclear, stop and ask.

## Pipeline

Recon -> Learn -> Hunt -> Validate -> Report. Non-linear: jump back when a lead demands it. One lead at a time; keep a lead board so nothing is lost.

### 1. Recon

```bash
subfinder -d TARGET -silent | anew /tmp/subs.txt
assetfinder --subs-only TARGET | anew /tmp/subs.txt
cat /tmp/subs.txt | dnsx -silent | httpx -silent -status-code -title -tech-detect -o /tmp/live.txt
cat /tmp/live.txt | awk '{print $1}' | katana -d 3 -silent | anew /tmp/urls.txt
echo TARGET | waybackurls | anew /tmp/urls.txt
gau TARGET | anew /tmp/urls.txt
nuclei -l /tmp/live.txt -severity critical,high,medium -silent -o /tmp/nuclei.txt
```

Quick wins checklist: subdomain takeover, exposed `.git` / `.env`, default creds on admin panels, JS secrets, open redirects, CORS misconfig, S3/cloud buckets, GraphQL introspection, Spring actuators, Firebase open read. Fingerprint the stack from cookies and headers (Laravel, WordPress, Express, Next.js, GraphQL). Source recon: `SECURITY.md`, `CHANGELOG.md`, `git log --grep=security`, grep for TODO/FIXME/UNSAFE and dangerous sinks per language (see `references/upstream-SKILL.md` for the grep tables).

External recon tools (subfinder, httpx, nuclei, katana, ffuf, nmap) are not installed by default. Install with `install_tools.sh` from the repo, or use the CLI (below).

### 2. Learn

- Read 3+ disclosed reports for the program (HackerOne Hacktivity, Bugcrowd Crowdstream). Note which vuln classes pay and which get marked duplicate.
- "What changed" method: take a disclosed report, find the fix commit, read the diff, grep the target for the same anti-pattern.
- Threat model: name the crown jewels (money, PII, admin, SSO), map the attack surface (unauthenticated, authenticated, cross-tenant, admin), pick ONE primary target for the session.
- Use the app as a real user for 15+ minutes before hunting. Know the tech stack, auth system, and caching.

### 3. Hunt

One bug class at a time, deep not spray. Crown-jewel thinking: "If I could do ONE thing to this app, what causes the most damage?" Then developer empathy: what shortcut would a tired dev take, where is auth checked, what happens if endpoint B is called without going through endpoint A.

Priority classes (less saturated, higher payout): cache poisoning, business logic, race conditions, OAuth/OIDC chains, CI/CD, mobile APIs, second-order bugs (stored clean, rendered unsafely in admin panel). XSS/SSRF/XXE have the most competition.

Keep session notes: interesting leads, dead ends (don't revisit), anomalies (weird response times, 200s where auth should fail), rabbit holes time-boxed to 15 min each, confirmed bugs.

**A to B bug chaining.** When bug A is confirmed, hunt for B and C nearby. Single bugs pay, chains pay 3-10x more.

| Bug A | Hunt for B | Escalate to C |
|---|---|---|
| IDOR (read) | PUT/DELETE on same endpoint | Full account data manipulation |
| SSRF (any) | Cloud metadata 169.254.169.254 | IAM creds exfil, RCE |
| XSS (stored) | HttpOnly on session cookie? | Session hijack, ATO |
| Open redirect | OAuth redirect_uri accepts your domain | Auth code theft, ATO |
| S3 bucket listing | JS bundles | OAuth client_secret, OAuth chain |
| Rate limit bypass | OTP brute force | ATO |
| GraphQL introspection | Missing field-level auth | Mass PII exfil |
| CORS reflects origin | Credentials included? | Credentialed data theft |
| Host header injection | Password reset poisoning | ATO via reset link |

Protocol: confirm A with a real HTTP request, map sibling endpoints in the same controller, test the same pattern on every sibling, chain if a sibling has a different bug class, quantify ("affects N users", "exposes $X"), report ONE report per chain.

**LLM / AI features (OWASP ASI01-ASI10).** Prompt injection, tool misuse, data exfil, privilege escalation, indirect injection (poisoned docs/URLs the AI reads), excessive agency, model DoS, insecure output, supply chain (compromised MCP servers/plugins), sensitive disclosure. Triage rule: ASI alone is Informational. Must chain to IDOR, exfil, RCE, or ATO for a paid bounty.

**Web3 / smart contracts.** Load `references/skills/web3-audit/SKILL.md` for the 10 contract bug classes and Foundry PoC template, `references/skills/meme-coin-audit/SKILL.md` for rug pull detection. Rust rule: `.unwrap()` panics on encoding paths are NOT attacker-triggerable; only panics on deserialization of network input count.

## THE ONLY QUESTION THAT MATTERS

> "Can an attacker do this RIGHT NOW against a real user who has taken NO unusual actions, and does it cause real harm (stolen money, leaked PII, account takeover, code execution)?"

If NO, stop. Do not write. Do not explore further. Move on. Kill these immediately: "could theoretically allow", attacker needs X+Y+Z preconditions, wrong but harmless, dead code, source maps without secrets, SSRF with DNS-only callback, open redirect alone, "could be used in a chain if" (build the chain first, THEN report).

## Critical rules

1. Read full scope first.
2. No theoretical bugs (see the question above).
3. Kill weak findings fast, run the 7-Question Gate BEFORE writing any report.
4. Validate before writing: check CHANGELOG, design docs, deployment scripts first.
5. One bug class at a time.
6. Verify data isn't already public: check the web UI in incognito before reporting API "leaks".
7. 5-minute rule: nothing after 5 min probing (all 401/403/404), move on.
8. Impact-first hunting: "what's the worst thing if auth was broken?" If nothing valuable, skip the target.
9. Credential leaks need exploitation proof: finding keys isn't enough, prove what they access.
10. Don't over-rely on automation: scans hit WAFs, trigger rate limits, find the same bugs everyone else finds.
11. Business impact over vuln class: severity depends on context, not just the class.
12. One-hour rule: stuck on one target for an hour with no progress, switch context.
13. Two-eye approach: systematic testing plus anomaly detection.

## 4. Validate

### The 7-Question Gate (all 7 must be YES, any NO kills it)

1. Can I exploit this RIGHT NOW with a real PoC (exact HTTP request)?
2. Does it affect a REAL user who took NO unusual actions?
3. Is the impact concrete (money, PII, ATO, RCE)?
4. Is this in scope per the program policy?
5. Did I check Hacktivity/changelog for duplicates?
6. Is this NOT on the always-rejected list?
7. Would a tired triager at 5pm on Friday say "yes, that's a real bug"?

### 4 pre-submission gates

- Gate 0 reality check: bug is real (real HTTP requests, not code reading), in scope, reproducible from scratch, evidence captured.
- Gate 1 impact: answer "what can an attacker DO that they couldn't before?" with a real victim.
- Gate 2 dedup: searched Hacktivity, GitHub issues, last 5 disclosed reports; not a known issue.
- Gate 3 quality: title follows the formula, steps are copy-pasteable, evidence shows actual impact, CVSS matches the program's definitions, fix is one sentence.

### Always rejected (never submit)

Missing CSP/HSTS/security headers, missing SPF/DKIM/DMARC, GraphQL introspection alone, banner/version disclosure without a working CVE exploit, clickjacking on non-sensitive pages, tabnabbing, CSV injection, CORS wildcard without credential exfil PoC, logout CSRF, self-XSS, open redirect alone, OAuth client_secret in mobile app, SSRF DNS-ping only, host header injection alone, no rate limit on non-critical forms, session not invalidated on logout, concurrent sessions, internal IP disclosure, mixed content, weak SSL ciphers, missing HttpOnly/Secure flags alone, broken links, pre-account takeover, autocomplete on password fields. N/A hurts your validity ratio. Informative is neutral. Only submit what passes the 7-Question Gate.

Conditionally valid with a chain: open redirect + OAuth code theft = ATO; clickjacking + sensitive action + PoC; CORS wildcard + credentialed exfil; CSRF + sensitive state change; no rate limit + OTP brute force; SSRF DNS-only + internal access proof; host header injection + password reset poisoning; self-XSS + login CSRF.

## 5. Report

Title formula: `[Bug Class] in [Exact Endpoint/Feature] allows [attacker role] to [impact] [victim scope]`. Good: "IDOR in /api/v2/invoices/{id} allows authenticated user to read any customer's invoice data". Bad: "IDOR vulnerability found".

First paragraph formula: "An [attacker with X access] can [exact action] by [method], resulting in [business harm]. This requires [prerequisites] and leaves [detection/reversibility]."

Structure: Summary (2-3 sentences) -> Steps to Reproduce (exact copy-pasteable HTTP request) -> Supporting Material (screenshot/video, Burp request/response) -> Impact (quantified: N users, $ amount) -> Severity (CVSS 3.1) -> Fix (1-2 sentences). Keep reports under 600 words.

Human tone: start sentences with the impact, not the vuln name. Use "I" and active voice. One concrete example beats three abstract sentences. No em dashes, no "comprehensive / leverage / seamless / ensure".

CVSS 3.1 quick reference: IDOR read PII 6.5 Medium, IDOR write/delete 7.5 High, auth bypass to admin 9.8 Critical, stored XSS 5.4-8.8 Med-High, SQLi data exfil 8.6 High, SSRF cloud metadata 9.1 Critical, race condition double-spend 7.5 High, GraphQL auth bypass 8.7 High, JWT none algorithm 9.1 Critical.

Templates per platform and per vuln class live in `references/skills/report-writing/` and `references/upstream-SKILL.md` (HackerOne and Bugcrowd templates).

## CLI and automation

The repo ships a Python CLI (`bughunter`, PyPI: `agentic-bug-hunter`). Not installed by default; install only when the user asks for a hunt run:

```bash
uv tool install agentic-bug-hunter   # or: pipx install agentic-bug-hunter
bughunter setup                      # connect a free AI provider
bughunter hunt target.com            # recon, find, validate, report
```

Output lands in `~/.bughunter/`. Full recon also needs external tools (subfinder, httpx, nuclei, katana, ffuf, nmap): install with `install_tools.sh` from `~/workspace/tools/agentic-bug-hunter/`. MCP servers in the repo: Burp Suite proxy client and HackerOne public API.

### Specialist agents (prompts in references/agents/)

- `recon-agent`: subdomain enum + live host discovery
- `recon-ranker`: attack surface ranking from recon output + memory
- `validator`: 4-gate checklist on a finding
- `chain-builder`: builds A to B to C exploit chains
- `report-writer`: HackerOne / Bugcrowd / Immunefi reports
- `web3-auditor`: smart contract bug class analysis
- `token-auditor`: meme coin / token rug pull and security analysis
- `credential-hunter`: wordlist + OSINT + breach check; HARD STOPS at spray for a human go/no-go
- `autopilot`: autonomous hunt loop (scope, recon, rank, hunt, validate, report)

For a multi-agent hunt, spawn one subagent per phase or per bug class in parallel and give each its agent prompt from `references/agents/` plus the target and scope.

### Domain skills (references/skills/)

Load the matching one when the task narrows: `bug-bounty` (master workflow), `bb-methodology` (mindset + 5-phase workflow), `web2-recon`, `web2-vuln-classes`, `security-arsenal` (payloads, bypass tables, gf patterns), `web3-audit`, `meme-coin-audit`, `report-writing`, `triage-validation`, `credential-attack`, `mobile-pentest`, `cicd-security`, `graphql-audit`, `mcp-server-audit`, `cloud-pentest`, `bug-chaining`, `llm-redteam`, `omni-killchain`, `pii-hunter`.

## Common pitfalls

1. Hunting without reading scope first, then finding a bug on an out-of-scope asset. Wasted work, zero payout.
2. Reporting a theoretical bug with no PoC. Triagers kill it and it hurts the validity ratio.
3. Submitting a low finding alone instead of chaining it. Open redirect alone is N/A; open redirect plus OAuth code theft is ATO.
4. Spraying tools at a target and drowning in 403s. 5-minute rule: move on.
5. Reading code only, never sending a request. A bug confirmed by code reading alone fails Gate 0.
6. Overclaiming severity. Severity must match the impact described, not the vuln class name.
7. Losing leads. After recon, keep a lead board (target, lead, priority, status) and route each lead to its hunt; surface stale high-priority leads unprompted.
8. Reusing one account to test auth bugs. Always use two test accounts (attacker + victim).

## Verification checklist

- [ ] Scope verified against the program before any request was sent
- [ ] Every finding has a working PoC (exact HTTP request) and evidence
- [ ] 7-Question Gate passed, all 7 YES
- [ ] Dedup checked (Hacktivity, changelog, GitHub issues)
- [ ] Report title follows the formula, under 600 words, fix is one sentence
- [ ] Two test accounts used for auth bugs
- [ ] No out-of-scope asset touched, no destructive test run
