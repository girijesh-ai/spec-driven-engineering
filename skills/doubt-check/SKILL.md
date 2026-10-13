---
name: doubt-check
description: Use when a non-trivial decision made mid-work (a design choice, a root-cause conclusion, a claim that a criterion is met) is about to have more work built on it and hasn't been challenged by anyone but its author — a fresh-context adversarial check before it hardens.
---

# doubt-check
Status: draft

## Overview

The agent that made a decision is the worst-placed to find its flaws: its
context is full of the reasoning that led there. This skill hands the
decision, stripped of that reasoning, to a fresh subagent whose only job
is to find what's wrong with it. Adapted from addyosmani/agent-skills'
`doubt-driven-development`.

Sits between `implement` and `review-code`: `review-code` checks a
finished diff; this checks one decision while it's still cheap to change.

## When to use

- A design choice other steps will build on (a data shape, an interface,
  a concurrency approach)
- A root-cause conclusion from `debug-systematically` before the fix lands
- A claim that a Success Criterion is met when the evidence is indirect

Skip for: decisions already covered by an approved spec, and anything
cheap to reverse.

## Process

1. **Claim.** Write the decision in 2-3 lines: what you decided and what
   it's supposed to achieve.
2. **Extract.** Gather the artifact (the code, schema, or conclusion) and
   the contract it must satisfy — the relevant spec Success Criteria, or
   the bug's red-capable command. Leave out your reasoning, alternatives
   you rejected, and how confident you are.
3. **Doubt.** Dispatch a fresh subagent with only the claim, artifact, and
   contract, and this instruction: "Find what is wrong with this. Do not
   validate it. List concrete failure cases, each with the input or
   condition that triggers it." Use a strong model for this subagent.
4. **Reconcile.** For each objection: **accept** (change the decision) or
   **refute** with evidence — a command run, a line of code, a criterion.
   "I think it's fine" is not a refutation.
5. **Stop** when a cycle produces nothing actionable, or after 3 cycles.
   Two cycles in a row with nothing actionable means further doubting is
   theatre — stop and proceed.

**Cross-model escalation.** For a decision that is high-risk and still
contested after reconciling, offer to run step 3 again on a different
model tier. Always offer it in that case and let the user decide; never
skip the offer silently.

## Output

```markdown
## Doubt check: <claim, one line>
Cycles: N
- Objection: <failure case> → accepted: <change made> | refuted: <evidence>
Result: decision kept | decision changed to <...>
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Passing your reasoning to the doubter | Send claim, artifact, and contract only — reasoning invites agreement |
| Asking the doubter to "review" or "check" | Ask it to find what's wrong; a validator finds reasons to agree |
| Refuting an objection with an opinion | Refute with a command, a line, or a criterion — or accept it |
| Running cycles until one comes back clean | Cap at 3; two empty cycles in a row means stop |

## Next

Return to the skill that was running (`implement`, `debug-systematically`,
`spec-from-idea`) with the decision kept or changed.
