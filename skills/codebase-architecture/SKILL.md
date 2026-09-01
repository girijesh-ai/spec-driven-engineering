---
name: codebase-architecture
description: Use when planning a non-trivial change's file/module structure, or reviewing whether a change's boundaries are sound — checks module depth, interface width, and layer-boundary violations, independent of SOLID-level class design.
---

# codebase-architecture
Status: stable

## Overview

Feeds `plan-from-spec` (before code exists, to plan sound boundaries) and
`review-code` (after code exists, to check they held). Where
`engineering-standards`' SOLID section is about a single class or function's
responsibilities, this skill is about the shape of modules and the
boundaries between them — a different, complementary lens.

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
caller, the module isn't hiding anything.

## Process

1. **For plan-from-spec:** before finalizing which files a step touches,
   check whether the natural boundary is a new module (if the concern is
   genuinely new) or an addition to an existing one (if it's a natural
   extension of something that already exists) — don't default to "new
   file" or "add to the biggest existing file" without checking which is
   deeper.
2. **For review-code:** for each new or changed module, ask the module
   depth and interface width questions above. Flag any layer-boundary
   import that crosses a documented boundary the wrong direction.
3. **Don't propose unrelated refactoring.** If an existing file has a real
   architecture problem outside the current change's scope, note it — don't
   silently expand the diff to fix it.

## Common mistakes

| Mistake | Fix |
|---|---|
| Adding a new file for every new function | Check whether it's a natural extension of an existing deep module first |
| A module with 10+ public methods, most used by only one caller | That's several narrower interfaces wearing one name — split it |
| A shared/lower-layer module importing something project-specific | Boundary violation — add an abstraction, don't import across it |
| Fixing an unrelated architecture problem while reviewing this change | Note it, don't silently expand scope — flag it as a separate follow-up |

## Next

Findings feed into `plan-from-spec`'s file list, or `review-code`'s Axis 2
findings.
