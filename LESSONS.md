# LESSONS.md — learning loop (template)

ORCHESTRATOR step 10: after every triage outcome, append an entry
here the same day (date, program, candidate, verdict, the team's
reason verbatim, rule changed) and patch the agent doc the rule
lives in. Before each hunt, re-read the kill-list below. A lesson
not written down is a lesson that will repeat.

## Kill-list (mechanisms that are dead on arrival)

Format per entry: `<PROGRAM> <CANDIDATE-ID> — <one-line mechanism>:
<why it died (audit finding ID / known issue / prior report / design
doc / triage answer), <date>>`.

<!-- Add killed mechanisms here as hunts close. Example (template, not real):
- <PROGRAM> C1 — <mechanism in one line>: killed, team-seen
  (<audit finding ID / known-issue link / triage answer>), <date>.
-->

## Triage outcomes

Format per entry:

```
### <date> — <PROGRAM> <CANDIDATE-ID> <verdict>
- Outcome: <accepted / rejected / duplicate / invalid / closed 0/0>
- Team's reason (verbatim or close paraphrase): <...>
- Rule changed: <what ORCHESTRATOR/RESEARCHER/AUDITOR doc changed, and how>
```

<!-- Example (template, not real):
### <date> — <PROGRAM> C1 REJECTED
- Outcome: rejected, intended design.
- Team's reason: "<quote>".
- Rule changed: <agent doc> now kills <mechanism family> at the intent check.
-->

## Wins

<!-- Accepted reports go here: program, candidate, severity, payout, date. -->
(none yet)
