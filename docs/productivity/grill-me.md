# grill-me

**Status:** stable

## What it does

A relentless interview against a plan, spec, or design decision — asking
the questions that break the happy path, pushing every "we'll handle that
later" to a real resolution, and continuing past the first comfortable
answer until a round of questions surfaces nothing new.

## When to reach for it

- A spec or plan is about to be approved but something feels hand-wavy.
- A quick design decision needs a real check before other work depends on
  it.
- `spec-from-idea`'s Open Questions section didn't fully resolve during its
  own self-review.

## Common questions

**How is this different from spec-from-idea's own clarifying questions?**
`spec-from-idea` asks what's needed to write the spec in the first place.
`grill-me` pressure-tests a spec/plan that already exists, looking
specifically for what would embarrass it later.

**When does grilling stop?**
When a round of questions produces nothing new — not when the first few
answers feel satisfying.

**Under an autonomous/background mode that's biased against stopping for
questions, does grill-me still ask?**
Yes — a live interview is the entire point of this skill, so it's exactly
the kind of skill-level signal such a bias is meant to defer to. If truly
nobody is available to answer (a genuinely unattended run), it says so
explicitly and logs the question as unresolved rather than answering on
the requester's behalf.

## It's working if

- Every "we'll handle that later" in the reviewed document either got
  resolved or became an explicit, reasoned Non-Goal/Open Question.
- The summary lists both what changed and what got confirmed as already
  right.
- No question was ever answered by the agent on the requester's
  behalf — each one either got a real answer or was logged as
  unresolved.
