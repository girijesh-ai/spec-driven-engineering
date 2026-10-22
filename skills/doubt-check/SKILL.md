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

Skip for: choices the approved spec itself made (pressure-test the spec
with `grill-me` instead), and anything cheap to reverse.

Run it from the main session. A subagent can't start another subagent, so
inside one, say that doubt-check can't run there and hand the decision
back to the main session. Don't fake a fresh context by questioning
yourself.

## Process

1. **Claim.** Write the decision in 2-3 lines: what you decided and what
   it's supposed to achieve. This is for you; the doubter never sees it.
2. **Extract.** Gather the artifact (the code, schema, or conclusion) and
   the contract it must satisfy — the relevant spec Success Criteria, or
   the bug's red-capable command. Leave out your reasoning, alternatives
   you rejected, and how confident you are. If the artifact is too big to
   hold in one read, split it and doubt the parts.
3. **Doubt.** Dispatch a fresh subagent with the artifact and contract
   only, never the claim: a stated conclusion invites agreement. Give it
   this instruction: "Find what is wrong with this. Do not validate it.
   List concrete failure cases, each with the input or condition that
   triggers it, or say you found none." Use a strong model for this
   subagent.
4. **Reconcile.** Re-read the artifact against each objection, then put
   it in the first class that fits:
   - **Contract misread** — the contract you sent was unclear. Fix the
     contract; re-classify next cycle.
   - **Valid, fix it** — change the artifact, then run another cycle.
   - **Valid trade-off** — real, but fixing costs more than accepting.
     Write the trade-off down so the user sees it.
   - **Noise** — correct given context the doubter didn't have. Refute it
     with evidence: a command run, a line of code, a criterion. "I think
     it's fine" is not a refutation.
5. **Stop** when a cycle returns only trivial or already-considered
   objections, or the user says to proceed. After 3 cycles, stop and hand
   it to the user: substantive objections still coming after 3 cycles say
   the decision isn't ready. Don't run a fourth alone.

**Doubt theatre.** Two or more cycles of substantive objections with none
classed "valid, fix it" means you are validating, not doubting. Stop and
escalate to the user; don't proceed on your own say-so.

**Cross-model escalation.** For a decision that is high-risk and still
contested after reconciling, offer to run step 3 again on a different
model tier. Always offer it in that case and let the user decide; never
skip the offer silently.

## Output

```markdown
## Doubt check: <claim, one line>
Cycles: N
- Objection: <failure case> → fixed: <change> | trade-off: <why accepted> | contract misread: <contract fix> | noise: <evidence>
Result: decision kept | decision changed to <...>
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Passing the claim or your reasoning to the doubter | Send artifact and contract only — a conclusion invites agreement |
| Asking the doubter to "review" or "check" | Ask it to find what's wrong; a validator finds reasons to agree |
| Refuting an objection with an opinion | Refute with a command, a line, or a criterion — or accept it |
| Running cycles until one comes back clean | Cap at 3, then hand it to the user |
| Dismissing every objection, cycle after cycle | That's doubt theatre: stop and escalate |
| Running doubt-check inside a subagent | It needs a fresh subagent; hand it back to the main session |

## Next

Return to the skill that was running (`implement`, `debug-systematically`,
`spec-from-idea`) with the decision kept or changed.
