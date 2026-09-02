---
name: engineering-standards
description: Use when writing or reviewing any non-trivial code — naming, function design, error handling, testing, security, logging, and SOLID/DRY checks that apply regardless of language. Referenced by implement and review-code rather than invoked on its own.
---

# engineering-standards
Status: stable

## Overview

The language-agnostic checklist `implement` writes against and `review-code`
reviews against. See `references/python.md` for the Python-specific
appendix (exact conventions: dataclasses, pathlib, logging setup).

## Naming

- Self-documenting. If a variable needs a comment to explain it, rename it
  instead.
- Functions: verb phrases (`compute_score`, `validate_input`).
- Booleans: `is_`/`has_`/`should_`/`can_` prefix.
- No abbreviations except universal ones (`url`, `id`, `api`, `db`).

## Functions

- One responsibility. If describing it needs "and," split it.
- Max meaningful indentation depth: 3. Flatten with early returns.
- Keep under ~40 lines; extract helpers past that.
- No boolean-trap parameters (`process(data, true, false)`) — named
  parameters or an enum instead.

## Data

- Structured types (dataclass/struct/record/TypedDict) for anything crossing
  a function boundary as a public interface — never a raw dict/map for that.
- Public signatures fully typed.
- Constants named and centralized — never inline magic values repeated in
  more than one place.
- Prefer immutable types where the value won't change.

## Error handling

- Never silently swallow an exception. At minimum: log it with full
  context, then re-raise or return a typed error.
- Validate at system boundaries (user input, external APIs, queue
  messages). Trust internal code.
- Distinguish programmer errors (raise immediately) from operational errors
  (return a typed result, or log and continue).
- Catch specific exception types. A bare catch-all without logging the full
  error loses the information needed to debug it later.
- Never convert a specific exception into a generic one — the caller loses
  diagnostic information.

## Comments and docs

- Default: no comments. Code should read clearly without them.
- Only comment the WHY when it's non-obvious: a hidden constraint, a bug
  workaround, an invariant that isn't visible from the code itself.
- Never comment WHAT the code does — that's what naming is for.

## Testing

- Test behavior, not implementation — tests should survive refactoring.
- Never mock the unit under test, only its external dependencies (network,
  DB, third-party APIs).
- Never weaken an assertion to make a test pass; fix the underlying bug.
- Every test runnable in isolation — no shared mutable state between tests.
- Tests needing external services get a marker/tag and are excluded from
  the default fast run.

## Security

- Validate and sanitize all external input before use.
- Never build a shell command or a SQL query by string interpolation — use
  the parameterized/list-argument form.
- Secrets come from environment variables or a secrets manager, never from
  code or a file committed to version control.
- Log at INFO or below by default. Never log credentials, tokens, PII, or
  full request/response bodies.
- Principle of least privilege — request only the permissions actually
  needed.

## Logging

- One logger per module, named after the module — never a hardcoded string.
- Structured messages with the relevant values attached, not just prose.
- Levels: DEBUG (dev-only internal state), INFO (normal operational
  events), WARNING (unexpected but recoverable), ERROR (an operation
  failed), CRITICAL (system-level failure).
- Never use bare console/print output for operational logging in production
  code paths.

## Git

- Commit messages: imperative mood, one logical change per commit, passes
  its own tests standalone.
- Never commit generated files, build artifacts, or dependency caches.

## SOLID (applied at every level: functions, classes, modules, services)

| Principle | The check |
|---|---|
| **S**ingle Responsibility | Can you name ONE reason this unit would need to change? If it mixes business logic, storage, and formatting, split it. |
| **O**pen/Closed | Can the next likely feature be added without editing this unit? Repeated `if type == "A"` chains across the codebase mean: define an interface, register implementations, stop editing the dispatcher. |
| **L**iskov Substitution | Can every subtype/implementation replace the base with zero caller changes? A subclass raising `NotImplementedError` on a base method, or narrowing what it accepts, is a broken hierarchy — fix the hierarchy, not the caller. |
| **I**nterface Segregation | Does every consumer of this interface use every method on it? An interface with unused stub methods across implementors should be split into narrower ones. |
| **D**ependency Inversion | Does business logic import concrete infrastructure (an HTTP client, a specific DB driver, a specific vendor SDK) directly? It shouldn't — inject an abstraction, wire the concrete implementation at the entry point. |

## DRY

- Grep before writing — build second, search first.
- A constant, threshold, or validation rule defined in two places is a
  future inconsistency bug. One authoritative source, imported everywhere
  else.
- The moment the same block appears a second time, extract it — three
  occurrences means the extraction was already overdue.

## Necessity and simplicity

- Before writing anything, ask whether it needs to exist at all. A
  speculative feature not required by the spec's Goals is scope creep, not
  thoroughness.
- No unrequested abstractions: no interface with a single implementation,
  no config for a value that will never change, no parameter added for a
  hypothetical future caller.
- Climb the ladder before writing new code: does stdlib already do this?
  Does a native platform feature cover it? Does an already-installed
  dependency solve it? Only write new code once those are ruled out.
- The simplest correct solution wins. Code that needs more comments to
  explain than the code it replaces is a regression, not an improvement.

## Layer boundaries and backward compatibility

- Dependency *direction* across a layer boundary is
  `codebase-architecture`'s check, not this one — flag a wrong-direction
  import there. Backward compatibility, below, is this skill's.
- Public interfaces (return keys, exported function signatures, registered
  names looked up by string) are additive-only. Removing or renaming
  breaks callers you can't enumerate — deprecate for one cycle, then
  remove (see `references/python.md` for the concrete pattern).
- Never read configuration or environment variables directly inside deep
  logic — route through the config-loading layer so the source of truth
  stays auditable.

## Quick reference for review-code

When reviewing, check in this order: naming/functions → error handling →
security → SOLID/DRY → necessity/simplicity → backward compatibility
(dependency direction is `codebase-architecture`'s check). A change can be
fully correct and standards-compliant and still be over-engineered —
necessity is its own check, not a byproduct of the others. A change can
look clean at the diff level and still fail every one of these once read in
full-file context — see `review-code` for that process.
