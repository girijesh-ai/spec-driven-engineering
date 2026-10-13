---
name: grill-me
description: Use when a plan, spec, or design decision feels shaky and needs to be pressure-tested before committing to it — a relentless interview that keeps pushing until every branch of the decision is resolved, not just the happy path.
---

# grill-me
Status: stable

## Overview

A standalone pressure-test, or a step invoked mid-`spec-from-idea` when a
particular section (usually Approach or Success Criteria) feels
under-examined. The goal is to surface the question that would embarrass
the plan later, now, while it's still cheap to answer.

## When to use

- A spec or plan is about to be approved and something about it feels
  hand-wavy, but it's not clear what
- A design decision was made quickly and needs a real check before other
  work builds on top of it
- Before `plan-from-spec` on anything architectural, if `spec-from-idea`'s
  own self-review pass didn't fully resolve the Open Questions section

## This is a live interview, not a solo exercise

Ask one question, then stop and wait for the actual answer — never answer
on the requester's behalf. Self-answering defeats the point: this skill
exists to surface what the requester hasn't thought through, not what the
agent guesses they'd say. This holds even under a general bias toward not
stopping for clarifying questions (an autonomous or background mode,
Auto Mode's default) — this skill's whole purpose is to stop and ask, and
that's exactly the kind of skill-level signal such a bias is meant to
defer to.

If no live answer is actually available (a genuinely unattended run,
nobody to respond), do not fake the interview. Say so explicitly —
"grill-me needs a live answer here; running unattended, so this question
is logged as unresolved" — and list every unanswered question under Open
Questions/Non-Goals rather than presenting a self-resolved interview as
if it were real.

## Process

1. **Start from the plan/spec as written**, not from scratch. Read it
   fully first.
2. **Ask the question that breaks the happy path**, not the question that
   confirms it. "What happens when X is empty/absent/concurrent/huge?"
   beats "does this handle X?" Every question carries your own
   recommended answer: `Q: <question>` / `GUESS: <your answer and why>`.
   One question means one decision, not several bundled under one `Q:`.
   End the message at the `GUESS:` — no "and if so, also tell me…"
   follow-ups; those are the next questions, asked after this answer.
   The requester reacts to a concrete position faster than to an open
   question, and a wrong guess surfaces the gap just as well.
3. **Look up facts, ask about decisions.** If the code, docs, or a quick
   experiment can answer it, find out yourself (or dispatch a subagent)
   and state what you found. Only decisions go to the requester.
4. **Follow every "we'll handle that later" to its actual answer.**
   "Later" is not an answer — either resolve it now or move it explicitly
   to Open Questions/Non-Goals with a stated reason.
5. **Keep going past the first satisfying answer.** One good answer often
   hides the next unexamined branch. Stop when you can predict the
   requester's answer to your next three questions — not when the first
   few felt resolved.
6. **Summarize what changed, then get an explicit yes.** List every
   question that led to a real change in the spec/plan, and every one that
   confirmed the original was right. "Sounds good", "sure", "whatever you
   think" are not a yes — ask which change they disagree with.

## Common mistakes

| Mistake | Fix |
|---|---|
| Asking questions the plan already answers | Read fully first — grilling should surface new gaps, not restate the document |
| Accepting "we'll handle that later" without pinning it down | Push for a specific resolution or an explicit, reasoned deferral |
| Stopping after the first round of questions | Keep going until a round produces nothing new, not until it produces something comfortable |
| Grilling implementation details in a spec that hasn't settled its goals yet | Grill the goals/approach first — implementation questions are premature if the goal itself is still shaky |
| Asking an open question with no position of your own | Attach a `GUESS:` — it's not answering for them, it's giving them something to push against |
| Asking the requester something the repo could answer | Facts are yours to look up; only decisions go to them |
| Answering your own question instead of asking the requester | Stop after each question and wait for the real answer — self-answering isn't grilling, it's narrating |
| Treating a "don't stop for questions" bias as overriding this skill | It doesn't — a skill signaling it needs to ask is exactly the case such a bias is meant to defer to |

## Next

Resolved answers go back into the spec/plan being pressure-tested.
