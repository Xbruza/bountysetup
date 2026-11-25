# WEB-RECON - Beacon L1-L5 annex for the bounty orchestrator

Source: https://aibugbounty.beacon.host/ ("Bug bounty with AI").
Added 2026-11-26. This annex adds a web recon pipeline to the 4-agent
loop. It does not replace the loop. Code-repo hunts (XE) skip it.
Smart-contract hunts use it only when the program has a live web surface.

## When it applies

- APPLIES: program with a live web app or API in scope (Minara, Cygnus,
  Sperax web, Proton web, any future no-KYC web program).
- SKIP: repo-only hunts (XE), contract-only hunts with no web surface.
- NEVER: production agents running unsupervised. Level 5 tools run only
  in a lab, staging copy, or local checkout. Shannon executes real
  exploits: never against production, never against a live program host.

## Step 0 - Scope freeze (before any tool)

No recon runs before this file exists:

`~/workspace/<program>/scope.md` plus `~/workspace/<program>/allowlist.txt`

`allowlist.txt` holds one in-scope root per line, nothing else.
`scope.md` quotes: in-scope roots, out-of-scope list, rate limits,
whether crawling, automated scanning, OOB callbacks, and credentialed
testing are allowed, tier table, disclosure policy, submission channel.

Rules:
- A related subdomain not listed in scope is OUT until the program
  says otherwise.
- Never hand a model a target and ask it to "go hunt". The allowlist
  exists first, then the model helps organise.
- Every later step filters back to the allowlist. Historical URLs
  wander into other brands, expired apps, and third-party CDNs: drop
  them.

Step 0 checklist:
- [ ] Written scope on file, with out-of-bounds list
- [ ] Single allowlist of in-scope roots, nothing else scanned
- [ ] Rate limit decided before any crawl or fuzz

## Level 1 - Map the surface

Tools (all on InstaBox momomuse, never on the Hatch VM):
subfinder, assetfinder, Amass, dnsx, httpx, naabu.

```bash
subfinder -d in-scope.example -o subs.txt
assetfinder --subs-only in-scope.example
amass enum -d in-scope.example
cat subs.txt | dnsx -silent -a -resp -o resolved.txt
cat resolved.txt | httpx -title -status-code -tech-detect -o live.txt
naabu -list resolved.txt -o ports.txt
```

Rules: passive enum first. naabu only if the policy clearly allows
port scanning. Resolve first, probe second. A name that does not
resolve is not a live target. Save one live-host file and reuse it.

Outputs in `~/workspace/<program>/recon/`:
`subs.txt`, `resolved.txt`, `live.txt`, `ports.txt` (only if allowed).

Level 1 checklist:
- [ ] Scope file and allowlist exist
- [ ] Live hosts resolved and probed, no out-of-scope names touched

## Level 2 - Collect URLs, params, JS

Tools: katana, waybackurls, gau, waymore, ParamSpider, Arjun, gf,
LinkFinder.

```bash
katana -u https://in-scope.example -o crawl.txt
cat domains.txt | waybackurls > wayback.txt
gau in-scope.example --subs
waymore -i in-scope.example -mode U
paramspider -d in-scope.example
arjun -u https://in-scope.example/endpoint --ratelimit 2
cat urls.txt | gf xss
python3 linkfinder.py -i https://in-scope.example/app.js -o cli
```

Rules: Arjun sends many requests, always rate-limited, only on
allowed endpoints. Historical URLs may be dead or out of scope:
filter before visiting. gf patterns are hints, not findings.
LinkFinder extracts links, it does not test them. Keep only
endpoints on in-scope hosts.

Outputs in `~/workspace/<program>/recon/`:
`urls.txt`, `params.txt`, `js-endpoints.txt`.

Level 2 checklist:
- [ ] URL list holds only in-scope hosts
- [ ] Separate file of JS and parameterized URLs exists
- [ ] Rate limit set before crawling or fuzzing params

## Level 3 - AI triage at the desk

Tools: Ollama (local, preferred), ReconAIzer, BurpGPT, Burp AT,
Nuclei `-ai`.

```bash
ollama run MODEL
nuclei -l live.txt -rate-limit 30 -o nuclei-hits.txt
nuclei -u https://in-scope.example -ai "look for exposed env or git files"
```

Rules:
- This is the highest-value AI step: feed a model a slice of the URL
  list or a JS file and ask it to group, label, and flag leftovers.
- Local model when the data is sensitive. Cloud model only with
  cookies, tokens, session data, and customer data stripped first.
- Never paste tokens, session cookies, or customer data into a
  third-party chat.
- Nuclei AI: read the generated template before any wider run.
- Every model suggestion is unverified until reproduced by hand.
- RESEARCHER is the Level 3 agent in this system: it triages the
  recon files and hands BUILDER at most 3 candidates with exact
  file, endpoint, and reproduction steps. It never invents hosts,
  paths, or severity.

Level 3 checklist:
- [ ] Known which data goes to a cloud model and which stays local
- [ ] No tokens, cookies, or customer data pasted to a third party
- [ ] Every model suggestion treated as unverified until reproduced

## Level 4 - Hunt in scope

Tools: ffuf, Dalfox, gowitness, interactsh, Nuclei templates.

```bash
ffuf -u https://in-scope.example/FUZZ -w wordlist.txt -rate 20
cat urls.txt | dalfox scan
gowitness scan single --url "https://in-scope.example" --write-db
interactsh-client
```

Rules:
- Rate limit on every fuzzer and scanner. Watch for wildcard
  responses so 10,000 fake hits are not recorded.
- Soft-404 baseline first (two bogus paths per host, record status,
  length, body hash). No path is "found" until it differs from the
  control. See local-claude-bughunter step 0.
- Dalfox only where XSS testing is allowed. interactsh only where
  OOB testing is allowed and a hypothesis already needs a callback.
- Record the exact command, the time, and the response that mattered.
  A model cannot invent it later.
- BUILDER owns Level 4 in this system (see BUILDER.md Part B web
  annex). A scanner hit is a lead, never proof: reproduce it live
  before it becomes a candidate.

Level 4 checklist:
- [ ] Every target in this level is in the written scope
- [ ] Rate limit set on fuzzers and scanners
- [ ] Finding reproduced by hand before write-up

## Level 5 - Agents and source review, last and only in a safe place

Tools: PentestGPT, hackingBuddyGPT, Strix, Shannon, Vulnhuntr.

```bash
strix --target ./app-directory
npx @keygraph/shannon@latest start -u https://your-app.com -r /path/to/your/repo
vulnhuntr -r /path/to/in-scope/repo/
```

Rules:
- Agents plan, run tools, and write a draft report. Treat them like
  a junior on day one: sandbox, hard scope, approval step, read
  everything they did.
- Lab, CTF, staging copy, or local checkout only. Never production.
- Never point an agent at a live program host unsupervised.
- Strix findings are leads, never proof. Vulnhuntr is Python
  codebases only. Shannon needs Docker, Node 22+, and your own model
  key, and its docs say it executes real exploits.
- AUDITOR still independently re-runs the reproduction and the
  control, re-checks dedup and intent, and issues the verdict.
  No agent output files itself.

Level 5 checklist:
- [ ] Agent runs in a lab, VM, or staging app allowed to test
- [ ] Written authorization and hard allowlist before it starts
- [ ] Full log reviewed, finding reproduced by hand

## Workflow order (web programs)

1. Read the policy and freeze the scope (Step 0).
2. Map the surface (Level 1).
3. Collect URLs, params, JS (Level 2).
4. Triage with AI, preferably local (Level 3, RESEARCHER).
5. Test, still in scope (Level 4, BUILDER).
6. Agents last, only in a safe place (Level 5, optional).
7. Write the report like a human who used a typist (AUDITOR gate,
   then file). Reproduce, save raw evidence, messy notes first,
   model drafts the clean version from verified notes only.

## Report prompts (copy, then tighten)

Triage a URL list, read JS for endpoints, draft a Nuclei idea,
explain a captured request, turn verified notes into a report draft,
keep an agent on a leash: use the Beacon prompt templates verbatim
from https://aibugbounty.beacon.host/, with in-scope.example swapped
for a host on the allowlist. Hard rule in every prompt: do not invent
hosts, steps, or severity. Do not paste secrets.

## What not to file

- A scanner hit not reproduced, including Nuclei, Burp Scanner,
  Dalfox, or an agent "proof".
- A model monologue with no request and response.
- Anything on an out-of-scope host, even if a tool or model
  suggested it.
- Destructive or OOB activity the policy forbids, described as if
  it were fine.
- Customer data, live session tokens, or other people's accounts
  in attachments.

## Install

Install script: `~/workspace/bounty-hunter/scripts/install-web-recon.sh`.
Run it on InstaBox momomuse only, never on the Hatch VM. It installs
the Go tools to `~/go/bin` (already on PATH there) plus Arjun via
pipx. Verify with `scripts/verify-web-recon.sh` or the version
commands in the script header. Re-run after a box rebuild.
