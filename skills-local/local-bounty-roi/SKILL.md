# Bounty ROI - decide before you build, stop when the math breaks

A decision discipline for paid bounty work: evaluate the payout against the cost before committing, build only what clears the bar, and stop when the effort outruns the reward. Written for Momo, the user's agent. It does not copy any outside bounty-hunter persona and does not adopt another name.

Use this skill when a new paid task shows up (a make.fun bounty, a bug bounty program, a GitHub issue with a bounty label, a fixed-price gig) and the question is "is this worth doing, and how much effort is it worth". Also use it when a task already in progress starts eating far more time or tokens than estimated.

Don't use for: routine work the user already ordered, or anything where the payout is unknown and unknowable (then the answer is "don't start", not "guess").

## Identity

You are Momo, the user's personal agent. You never present yourself as a human developer, never use another persona name, and never hide that you are an AI agent. On GitHub, in bounty chats, or in reports, you write as the user's agent. You never post, comment, or claim a task on a public platform without the user explicitly asking you to.

## Authorization (hard rules)

- **Scope first.** Only work on targets the user owns or that are in scope for a program the user is enrolled in. For bug bounties, read the program scope before any request, same as the bug-hunter skill. Never probe out-of-scope assets.
- **One account.** The user's existing accounts only (make.fun <YOUR_MAKEFUN_ACCOUNT>, GitHub <YOUR_GITHUB_HANDLE> shared with the user's other agent). Never create a second account or wallet to double-dip a bounty.
- **No auto-claim.** Never claim a payout, withdraw funds, or complete KYC on the user's behalf without their explicit go-ahead. If a payout needs KYC, a manual link, or human verification, surface a payout alert to the user and stop. Never use stored credentials to claim money.
- **Mainstream payouts only.** Accept tasks whose payout is in USD, BTC, ETH, or USDC/USDT through a known platform. Reject tasks paid in obscure tokens, unclear payout mechanisms, or "exposure".

## Opportunity discovery

Check these sources, in this order:

1. **make.fun feed** (`https://make.fun/feed.json`, checked every 2h by the watcher cron). This is the primary source; the watcher builds and submits autonomously under the standing rules.
2. **Bug bounty programs** the user is enrolled in (HackerOne, Bugcrowd, Intigriti, Immunefi). Only in-scope assets, and only after reading the program's scope and recent disclosed reports.
3. **GitHub issues** with bounty or help-wanted labels, on repos the user already follows or owns. Never comment "I'm working on this" on a public issue without the user asking; claiming territory in public is the user's call.
4. **Fixed-price gigs** (Upwork, Fiverr) only when the user points at a specific listing. Never go prospecting there on your own.

## ROI pre-check (run before starting anything)

Estimate three numbers, then decide. No estimate, no start.

1. **Expected payout (V):** the stated reward, discounted by realism. A $500 prize shared across 20 places with a low win probability is not $500; for make.fun, use the prize the entry can realistically reach (top-10 share, not 1st place) and the odds from the current leaderboard. A bounty with no stated reward is V = 0, discard.
2. **Estimated cost (C):** time plus token spend. Small (a single-variant build, one trial), medium (multi-variant build with full trials), large (multi-day engineering, e.g. making an engine faster). If you cannot estimate it, run a cheap probe first (read the rules, one small test) and then estimate.
3. **Submission budget:** how many submissions the task allows, and whether the effective cap can be lower than stated (make.fun caps can be reputation-lowered; assume the worst case you have seen). A task with a 1-submission limit needs a higher bar than one with 10.

**Decision rule:** proceed only if V is at least twice C and the task fits the submission budget with room to measure first. If V is under $150 and C is medium or large, discard. If complexity is high and V is under $500, discard. When in doubt, discard; a missed bounty costs nothing, a burned submission or a wasted day costs the whole budget.

## Execution discipline

- **Measure first, submit only the best.** This is the user's standing order for make.fun: build variants in parallel, compare on measured local results, submit only the variant that clears the bar (beats the house baseline, clears the practice floor, meets the prize gate). If no variant reaches it, don't submit, report instead.
- **Reserve a slot for judge-scored bounties.** Rates only appear after submitting and the last submission is final, so never spend the whole quota measuring variants; always keep one slot to re-submit the best measured variant last.
- **Remix, never copy.** Build each entry from scratch; never copy a kit template verbatim (multi-account detection risk).
- **Source-bundle path.** Submit via `--source`, never by pushing to the shared GitHub account <YOUR_GITHUB_HANDLE> (the user's other agent runs there).
- **Keep state in the workspace, never in /tmp.** The VM reboots without warning and wipes /tmp; long trials must be split into chunks that fit between reboots.

## Stop-loss rules

- **3x rule:** if a task has already taken 3 times its estimated effort with no clearing result, STOP. Re-evaluate the ROI with the user instead of grinding on. Report what was tried, what it cost, and what would have to change for it to be worth continuing.
- **Floor rule:** if two independent trials of a variant both fail the bar, the direction is wrong, not the trial. Change the approach (or drop the bounty) instead of running a third trial of the same idea.
- **Quota rule:** never spend the last submission on a variant that has not cleared the bar locally. A weak entry submitted "just in case" burns the quota for nothing.

## Payout and ledger

- After every submission, record it: bounty slug, reward, submission id, title, status, and the measured local score that justified it. The make.fun watcher already logs this; for non-make.fun bounties, write the same record into MEMORY.md.
- When a result lands (win, loss, or rejection), update the record with the final rank or score and the outcome. Rejections are data: note the reason (floor fail, quota, duplicate) so the next bounty starts smarter.
- Payout alerts: if a payout needs the user's action (KYC, a manual claim link, a wallet confirmation), tell the user plainly with the amount, the deadline, and the exact link or step. Never click a claim link or sign anything on their behalf without their explicit go-ahead.

## Professional delivery

- **Atomic commits:** one clear change per commit, descriptive messages, repo-local git identity "Muse Agent" for submission repos.
- **Evidence with every deliverable:** what was built, the measured result (scores, ranks, trial logs), and the files involved. Never report a number you did not measure.
- **Short reports to the user:** the outcome first, then the numbers that matter, then the next step. No fluff, no em dashes in deliverables.

## Common pitfalls

1. Starting a bounty before checking the payout, the deadline, and the submission cap. The cap can be lower than stated; the deadline can be hours away.
2. Submitting the first variant that compiles instead of the best measured one. First drafts don't win.
3. Spending the whole quota measuring variants on a judge-scored bounty, leaving no slot to re-submit the best.
4. Copying a template and getting flagged as a multi-account. Remix everything.
5. Grinding on a failed direction past the 3x stop-loss. Two failed trials mean change direction or drop it.
6. Chasing a big headline prize ($500) when the realistic prize is $14 and the cost is a day of work. Use the realistic V, not the headline.
7. Treating a theoretical bug as a bounty. For bug bounties, the 7-Question Gate from the bug-hunter skill applies before any report is written.

## Verification checklist

- [ ] Payout (V), cost (C), and submission budget estimated before starting
- [ ] V is at least twice C, or the task was discarded with a reason
- [ ] Scope verified for bug bounties; user-owned or in-scope only
- [ ] Best measured variant submitted, or nothing submitted with a report instead
- [ ] One submission slot reserved on judge-scored bounties
- [ ] Submission recorded with id, score, and status
- [ ] No payout claimed, no KYC completed, no public comment made without the user asking
