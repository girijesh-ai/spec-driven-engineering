---
name: codebase-architecture
description: Use when planning a non-trivial change's file/module structure, or reviewing whether a change's boundaries are sound — the structural lens on modules and boundaries, distinct from SOLID-level class design.
---

# codebase-architecture
Status: stable

## Overview

Feeds `plan-from-spec` (before code exists, to plan sound boundaries) and
`review-code` (after code exists, to check they held).
`engineering-standards` covers a unit's *responsibilities* (SOLID, at any
level) and backward compatibility; this skill owns the *structural* lens —
module depth, interface width, and which direction dependencies may flow
across a layer boundary. Complementary, not overlapping.

## When to use

- Deciding which files/modules a plan step should touch or create
- Reviewing whether a change introduced a new dependency that crosses a
  layer it shouldn't
- A file or module has grown large enough that "what does this actually do"
  no longer has a one-sentence answer

## Core checks

**Module depth.** A good module has a simple interface hiding real
complexity — a deep module. A module whose interface is nearly as complex
as its implementation (many parameters, many public methods, callers need
to understand internals to use it correctly) is shallow, and shallow
modules multiply complexity instead of hiding it. Prefer fewer, deeper
modules over many shallow ones.

**Interface width.** For each module/class under review: can you answer
"what does it do, how do you use it, what does it depend on" without
reading its internals? If not, the boundary is leaking. Can the internals
change without breaking callers? If not, it's not really an interface, it's
exposed implementation.

**Layer boundaries.** Dependencies flow one direction (see the layer table
in a project's own CLAUDE.md/docs if one exists, or establish one before
this skill is first used on a new codebase). A lower layer importing from a
higher one, or a shared utility importing something project-specific, is a
boundary violation — not a style nit, a maintainability risk that compounds.

**Information hiding.** A module's internal representation (data
structures, algorithm choice, storage details) should not leak into how
callers use it. If changing an internal detail requires touching every
caller, the module isn't hiding anything. Hyrum's Law applies: with
enough callers, every observable behaviour — ordering, timing, error text
— becomes depended on. Decide what's contract and say so; treat the rest
as something callers will lean on anyway.

**Deletion test.** Imagine deleting the module and inlining it into its
callers. If complexity vanishes, it was a pass-through — remove it. If the
same logic reappears across several callers, it was earning its keep.

**Seams and adapters.** One adapter behind an interface is a hypothetical
seam; two adapters (say, a real one and a test fake) make it a real one.
Don't add an interface until the second implementation exists or a test
needs it.

**The interface is the test surface.** Tests attach at a module's public
interface, not its internals. How a dependency is reached decides the
test strategy:

| Dependency | Test with |
|---|---|
| In-process (pure code, same process) | The real thing |
| Local and substitutable (SQLite, temp files, in-memory queue) | A real local instance |
| Remote but yours (your other service) | Ports and adapters: an interface with a fake adapter |
| Truly external (vendor API, payment provider) | A mock at the boundary |

When new interface-level tests cover what old tests of a shallow
module's internals did, delete the old tests — replace, don't layer.

**Contracts across the boundary.** One error format for the whole API
surface, not one per endpoint. Operations a caller may retry (payments,
writes over a network) take an idempotency key: claim it atomically,
store a hash of the payload with it, and define what a duplicate request
does while the first is still in flight.

## Process

1. **For plan-from-spec:** before finalizing which files a step touches,
   check whether the natural boundary is a new module (if the concern is
   genuinely new) or an addition to an existing one (if it's a natural
   extension of something that already exists) — don't default to "new
   file" or "add to the biggest existing file" without checking which is
   deeper.
2. **Design it twice only when it's hard to change later**: a public
   API, or an interface crossing a module or service boundary with
   callers you don't control. Everything else gets one design, checked
   with the depth and deletion tests above. When it applies, dispatch 2
   subagents (3 for a public API), each under a different constraint:
   smallest possible surface; optimised for the commonest caller; and
   ports-and-adapters only if a second adapter exists or a test needs
   one. Compare them on depth, locality of change, and where the seams
   fall. If the comparison changes the spec's approach, stop and update
   the spec with the user before planning further.
3. **For review-code:** for each new or changed module, ask the module
   depth and interface width questions above. Flag any layer-boundary
   import that crosses a documented boundary the wrong direction.
4. **Don't propose unrelated refactoring.** If an existing file has a real
   architecture problem outside the current change's scope, note it — don't
   silently expand the diff to fix it.

## Common mistakes

| Mistake | Fix |
|---|---|
| Adding a new file for every new function | Check whether it's a natural extension of an existing deep module first |
| A module with 10+ public methods, most used by only one caller | That's several narrower interfaces wearing one name — split it |
| A shared/lower-layer module importing something project-specific | Boundary violation — add an abstraction, don't import across it |
| An interface with one implementation "for flexibility" | One adapter is a hypothetical seam — inline it until a second one exists |
| Fanning out design-it-twice for an internal helper | One design; the depth and deletion tests are enough when callers are yours to change |
| A wrapper module that only forwards calls | Apply the deletion test; if nothing reappears in callers, delete it |
| Fixing an unrelated architecture problem while reviewing this change | Note it, don't silently expand scope — flag it as a separate follow-up |

## Next

Findings feed into `plan-from-spec`'s file list, or `review-code`'s Axis 2
findings.
