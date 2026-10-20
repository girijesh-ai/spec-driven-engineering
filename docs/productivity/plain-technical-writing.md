# plain-technical-writing

**Status:** stable

## What it does

One writing standard for anything a person on the team reads: specs,
plans, interview questions, handoffs, PR descriptions, ADRs, glossary
entries. Plain words, short sentences, the point first, and each term
explained the first time it appears. It keeps every number, command, file
path, and `SC-n` ID. It adds a diagram where a flow would otherwise take a
paragraph: Mermaid in files, ASCII in chat.

## When to reach for it

- You don't call it yourself most of the time: `spec-from-idea`,
  `plan-from-spec`, `grill-me`, `handoff`, `finish-branch`, and
  `domain-modeling` call it before they write.
- Call it directly when writing a project doc, README section, or PR
  description outside those skills.
- Not for text an agent reads to act (`SKILL.md`, `CLAUDE.md`): that's
  `writing-for-agents`. Not for rewriting an existing dense doc for
  non-engineers: that's `simple`.

## Common questions

**Doesn't simpler mean less exact?**
No. What goes is the padding: inflated words ("leverage", "robust"),
hedge stacks, and points buried in clauses. Every number, command, path,
ID, and edge case stays. "Handles errors" is a failure; "on a 5xx it
retries 3 times, then fails the job" is the target.

**Why keep jargon instead of replacing it?**
The reader will meet the term again in the code and on the team. The term
stays, with a short gloss the first time: "idempotent (safe to run twice;
the second run changes nothing)".

**How was it proven?**
On the sequential-dispatch spec and its `grill-me` session
(`docs/specs/2026-10-19-sequential-dispatch.md` and its `-grill-me.md`
log). The author and a colleague outside the work read both in one pass,
with every number, command, and `SC-n` intact. The log records the two
questions that needed follow-ups.

## It's working if

- Reading only the first sentence of each section tells the story.
- No word from the swap list in `references/patterns.md` is left.
- Every number, command, path, and `SC-n` from the draft is still there.
- A reader new to the work asks no "what does this mean?" questions.
