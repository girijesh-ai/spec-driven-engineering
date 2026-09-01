# codebase-architecture

**Status:** stable

## What it does

Checks module depth (simple interface, real complexity hidden inside),
interface width (does every consumer need every method, can internals
change without breaking callers), and layer-boundary direction. It's the
module/boundary-shaped complement to `engineering-standards`' class-level
SOLID checks.

## When to reach for it

- Planning which files a change should touch or create (via
  `plan-from-spec`).
- Reviewing whether a change's new dependencies or new modules are sound
  (via `review-code`).
- A file has grown to where "what does this do" doesn't have a one-sentence
  answer anymore.

## Common questions

**How is this different from the SOLID section in engineering-standards?**
SOLID is about a single class or function's responsibilities. This is about
module boundaries and the direction dependencies flow between them — a
different altitude, and both matter.

**What if fixing this means touching code outside the current change?**
Note it as a follow-up, don't silently expand the current diff to fix
something unrelated.

## It's working if

- New modules have a description-and-usage answer that doesn't require
  reading their internals.
- Layer-boundary violations get caught in review before they compound into
  a real untangling problem.
