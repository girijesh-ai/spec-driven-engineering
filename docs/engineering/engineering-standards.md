# engineering-standards

**Status:** stable

## What it does

The concrete, language-agnostic checklist behind `implement` and
`review-code`: naming, function design, structured data, error handling,
testing, security, logging, git hygiene, SOLID, DRY, and layer boundaries.
A Python-specific appendix (`references/python.md`) carries the exact
conventions (dataclasses, `pathlib`, `logging.getLogger(__name__)`,
deprecation pattern) for Python codebases.

## When to reach for it

- Not usually invoked directly — `implement` writes against it and
  `review-code` reviews against it.
- Worth reading directly when setting conventions for a new codebase, or
  when a review finding needs the underlying principle spelled out for a
  teammate.

## Common questions

**Why generalize instead of keeping this Python-specific?**
So the same standards skill works across any codebase this repo's spine
touches — the principles (SOLID, DRY, boundary discipline) aren't
Python-specific even though the original conventions this was drawn from
were written for Python work.

**Where do exact Python conventions live, then?**
`references/python.md` — dataclasses, logging setup, pathlib, the
deprecation-over-deletion pattern with `warnings.warn`.

**What if a codebase's existing conventions conflict with something here?**
Existing, established codebase conventions win for consistency within that
codebase — this checklist is the default for new decisions, not a mandate
to rewrite what's already there.

## It's working if

- `review-code` findings cite a specific line from this checklist instead
  of a vague "this feels off."
- Python-specific findings point at `references/python.md`'s concrete
  pattern rather than restating the general principle from scratch.
