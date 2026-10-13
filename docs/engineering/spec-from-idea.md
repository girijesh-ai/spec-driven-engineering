# spec-from-idea

**Status:** stable

## What it does

Turns a raw idea or a paragraph of requirements into a written spec: context,
goals, non-goals, the chosen approach, and — critically — measurable success
criteria. It's the first link in this repo's spine, and every other spine
skill assumes a spec produced this way exists (or explicitly notes that one
doesn't).

## When to reach for it

- You're about to start a feature, subsystem, or any change bigger than a
  one-line fix, and nothing about it is written down yet.
- Someone describes requirements in chat/Slack/a meeting and you need them
  turned into something `plan-from-spec` and `review-code` can actually
  check against later.
- You're not sure if a change is a quick fix or a bigger design problem —
  the skill's classification step (spike / bounded / architectural) settles
  that before any spec-writing effort is spent.

Skip it for typo fixes, one-line config tweaks, or anything already covered
by an existing spec.

## Common questions

**Do I always get a file out of this?**
No. Only the architectural path writes a spec file. Spikes end in a
recommendation; bounded changes end in a short design confirmed in chat.

**What if I don't know the success criteria yet?**
That's a sign the spec isn't finished, not a sign to skip the section. Keep
asking "how would I check this passed" until you have concrete, checkable
answers.

**Why does every question come with a guess attached?**
Reacting to a concrete position is faster than answering an open
question, and a wrong guess exposes the gap just as well. The guess is a
proposal for you to accept or correct, never an answer on your behalf.

**Why number the Success Criteria and attach a command to each?**
Plan steps cite them (`Satisfies: SC-2`), `review-code` runs each command,
and `finish-branch` reports each one's result. A number and a command are
what let every later skill check the same thing.

**How does it avoid over-engineering the design?**
Three ways. It states the expected scale and lifetime first ("~5 users,
under 2k rows, long-lived"), so the design is sized to real numbers. It
always shows the minimal approach and recommends it unless a named Goal
rules it out. And every Goal must trace to something you said or a stated
constraint. A queue or cache with no scale number behind it is a red flag.

**What happens if I skip this and go straight to `implement`?**
`implement` still runs, but it will visibly say "no spec/plan found —
proceeding ad-hoc," and `review-code`'s spec-compliance axis will report
itself skipped rather than silently passing.

## It's working if

- Every spec that comes out has a Success Criteria & Evals section with
  numbered criteria, each naming the command that checks it.
- Nothing reaches `plan-from-spec` on a "sounds good" — approval was an
  explicit yes to a six-line restate and to the chosen approach.
- You can hand the spec to `plan-from-spec` without needing to re-explain
  anything that was already asked and answered during spec-writing.
- Six months later, someone reading the spec file understands why the
  change was made, not just what it changed.
