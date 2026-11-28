# Bounty program queue (template)

One program at a time. When a program closes 0/0, roll to the next
QUEUED program. When the queue is empty, wait for the watcher.
Never hunt off-queue because a link looked interesting.

## Format per entry

```
## N. <PROGRAM NAME> — <platform> (<status>) (<date checked>, <source>)
- URL: <program page>
- Program: <what it is>. Rewards: <tiers>. Submission: <channel>.
  Payout: <currency / conditions>. No KYC, no fee (verify on the page).
- Scope: <contracts / app / repo>. Dedup baseline: <audits, post-mortems>.
- Status: QUEUED | HUNTING | CLOSED 0/0 | FILED | SKIPPED (<reason>).
```

## Queue

<!-- Example entry (template, not a real program):
## 1. <PROGRAM> — self-hosted (QUEUED, not hunted) (checked <date>, <source>)
- URL: <program page>
- Program: <what it is>. Rewards: <tiers>. Submission: <channel>.
  Payout: <currency>. No KYC, no fee stated.
- Scope: <contracts / app>. Dedup baseline: <audits>.
- Status: QUEUED. At hunt start: pull the contract addresses, find
  audits as the dedup baseline, verify the program is still live.
-->

<!-- Add programs below. Skipped programs (fee/KYC/deposit) get an
entry too, marked SKIPPED with the reason, so nobody re-queues them. -->
