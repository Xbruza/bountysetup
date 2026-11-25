---
name: local-claude-bughunter
description: Per-class bug-hunt pattern library from elementalsouls/Claude-BugHunter (83 skills, 681 disclosed-report patterns). Use when hunting a specific vuln class and you want the disclosed-report detection patterns, payloads, bypass tables, and chain templates for that class. Load one hunt-* skill at a time by path, on demand.
---

# Claude-BugHunter — per-class hunt pattern library

Source: https://github.com/elementalsouls/Claude-BugHunter, cloned
2026-11-20 to `~/workspace/tools/claude-bughunter/` (7.1 MB, 83 skills,
15 slash commands, 681 disclosed-report patterns across 24 vuln classes).
License: see repo LICENSE / LICENSE-CONTENT.

Use this skill for:
- hunting ONE specific vuln class with disclosed-report patterns (detection,
  payloads, bypasses, chain templates) instead of reasoning from first principles
- picking the next class to try when a target area is dry
- triage-validation, evidence hygiene, and report-writing checklists that go
  beyond the local skills
- the soft-404 baseline (step 0) before any web probing

Don't use for: the hunt pipeline itself (recon, scope, validate, report —
that is `local-agentic-bug-hunter`), writing and filing the report
(`local-bounty-reporting`), or anything outside a program scope the user is
enrolled in.

## Boundaries (no dupe)

- `local-agentic-bug-hunter`: the workflow (recon -> learn -> hunt ->
  validate -> report), the 7-Question Gate, the always-rejected list. The
  Claude-BugHunter master `bug-bounty` skill (77 KB) restates the same
  pipeline and the same gate, so it is NOT pasted anywhere here. Read it
  only if you need its wording: `skills/bug-bounty/SKILL.md`.
- `local-bounty-reporting`: report structure, severity + CVSS calibration,
  dedup procedure, filing, post-filing. Claude-BugHunter's
  `report-writing` / `bugcrowd-reporting` overlap it; use the local skill
  as the authority for XE, use these only for platform-specific format
  questions.
- This skill's NEW value: the 58 per-class `hunt-*` skills, `hunt-dispatch`
  (which class skill to load), `triage-validation`, `evidence-hygiene`,
  and the 681 disclosed-report patterns behind them.

## How to use

Load ONE hunt skill at a time, by path, only when the hunt narrows to that
class. Never paste the whole bundle into a role file or a prompt.

```
~/workspace/tools/claude-bughunter/skills/<name>/SKILL.md
```

`hunt-dispatch` (`skills/hunt-dispatch/SKILL.md`) is the loader: it
fingerprints the target, picks the right class skills, and states the
engagement frame (authorized and scope-bounded; output is a finding, not
an exploit; remediation is the point). Read it first when starting a
per-class hunt on a new target.

## Step 0 — soft-404 baseline (mandatory before any web probing)

Modern SPA/CDN hosts return HTTP 200 with the app shell for paths that do
not exist. A status code proves nothing. Before probing a single path, hit
two independent bogus paths per host (`/zzz-nope-12345`, `/qqq-other-98765`)
and record status + byte length + body hash. That triple is the control.
No path is "found" until its response differs from the control. A 200 that
matches the control hash is a soft 404. Compare bodies, never status codes
alone. (Source: `hunt-dispatch` step 0.)

## Per-class library (grouped; full list under skills/)

Auth & session: hunt-auth-bypass, hunt-ato, hunt-session, hunt-jwt-crypto,
hunt-oauth, hunt-saml, hunt-mfa-bypass, hunt-forgot-password, hunt-brute-force,
hunt-captcha-bypass.
Access control: hunt-idor, hunt-business-logic, hunt-race-condition.
Injection: hunt-sqli, hunt-nosqli, hunt-xss, hunt-ssti, hunt-ssrf, hunt-xxe,
hunt-ldap, hunt-deserialization, hunt-rce, hunt-lfi, hunt-html-injection,
hunt-dom.
Web platform: hunt-cors, hunt-csrf, hunt-clickjacking, hunt-host-header,
hunt-cache-poison, hunt-http-smuggling, hunt-open-redirect,
hunt-file-upload, hunt-websocket, hunt-graphql, hunt-fintech-graphql,
hunt-grpc, hunt-api-misconfig, hunt-shadow-api, hunt-spa-api,
hunt-exceptional-conditions, hunt-misc.
Frameworks: hunt-laravel, hunt-nextjs, hunt-nodejs, hunt-springboot,
hunt-aspnet.
Cloud & infra: hunt-cloud-misconfig, hunt-k8s, hunt-subdomain,
hunt-source-leak, hunt-tls-network, hunt-llm-ai, hunt-rag-vector.
Enterprise: cloud-iam-deep, enterprise-vpn-attack, m365-entra-attack,
okta-attack, vmware-vcenter-attack, hunt-ntlm-info, hunt-sharepoint.
Web3: web3-audit, meme-coin-audit, token-scan (command).

Each hunt-* skill carries: detection patterns from disclosed reports,
payloads and bypass tables, chain templates (A to B to C), and what counts
as proof. Follow its proof bar; a pattern match without a live reproduction
is not a finding.

## Triage & evidence (load when needed)

- `triage-validation/SKILL.md`: the 7-Question Gate plus VRT-aware
  severity, out-of-scope rebuttals.
- `evidence-hygiene/SKILL.md`: PII redaction, what to preserve, what never
  to include in a report.
- `report-writing/SKILL.md`: platform report formats.
- `bb-methodology/SKILL.md`: the 5-phase non-linear workflow and
  critical-thinking framework (overlaps the bug-hunter skill; read only
  when the workflow itself is the question).
- `bb-local-toolkit/SKILL.md`: local tool and wordlist paths.

## Commands (reference only, Claude Code slash commands)

`commands/` holds 15 commands (hunt, recon, scope, surface, intel, triage,
validate, chain, report, autopilot, token-scan, web3-audit, pickup,
remember, memory-gc). They are Claude Code commands, not Muse commands.
Read one only to borrow its checklist, never to invoke it.

## Verification checklist

- [ ] Scope verified against the program before any request was sent
- [ ] Step 0 soft-404 baseline recorded before probing paths
- [ ] One hunt-* skill loaded at a time, by path, for the class being tested
- [ ] Finding reproduced live (exact request + control case), not pattern-only
- [ ] 7-Question Gate passed (see `local-agentic-bug-hunter`)
- [ ] Dedup checked (see `local-bounty-reporting`)
- [ ] No out-of-scope asset touched, no destructive test run
