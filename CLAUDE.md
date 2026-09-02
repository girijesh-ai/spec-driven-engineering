# Repository Rules — spec-driven-engineering

These rules govern this repo, the same way the skills inside it govern the
projects that install them. Apply them to every skill added here.

## Buckets and promotion

`skills/` itself is a **flat namespace** — every skill lives directly at
`skills/<skill-name>/SKILL.md`, never nested under a bucket subdirectory.
This isn't a style choice: Claude Code's plugin loader scans `skills/*/` one
level deep, so a nested `skills/engineering/<name>/` is invisible to it.

Bucket membership (`engineering` vs `productivity`) and promotion status
are tracked in documentation, not directory structure:

- A skill is **promoted** once it has a doc at `docs/<bucket>/<skill-name>.md`
  and is listed in `README.md`. Only promoted skills appear there.
- A skill not yet dry-run on a real task has no `docs/<bucket>/` entry and
  is not listed in `README.md`, even though its `SKILL.md` already exists
  under `skills/` (it has to, for testing) — its `Status: draft` line in
  its own doc, once one exists, is what marks it not yet promoted. Draft
  skills the catalog isn't ready to advertise yet can also be tracked in a
  `docs/in-progress.md` list instead of a `docs/<bucket>/` page.
- Deleting a skill is a two-step move — drop it from `README.md` and
  `docs/<bucket>/` first, remove the `skills/<name>/` directory in a later
  change — never a silent `rm` of both at once.

## Skill quality bar

- Every skill has a `SKILL.md` with YAML frontmatter: `name` (letters,
  numbers, hyphens only) and `description` (third person, starts with
  "Use when...", leads with triggering conditions — a single trailing clause
  naming the outcome is allowed, but never a step-by-step summary of the
  skill's own process, since a workflow-summarizing description becomes a
  shortcut agents take instead of reading the skill body).
- Every promoted skill also has a human-facing doc at
  `docs/<bucket>/<skill-name>.md` with exactly four sections: **What it
  does**, **When to reach for it**, **Common questions**, **It's working
  if**.
- Every skill doc carries a status line — `**Status:** draft` or
  `**Status:** stable` — directly under the title (the bolded form the docs
  use; `scripts/validate.py` enforces it). `stable` requires at least
  one dry run against a real task; before that, it stays `draft` even if
  the content looks finished.
- Heavy reference content (100+ lines: full API/checklist detail) lives in
  `references/*.md` next to the skill, not inline in `SKILL.md`. Keep
  `SKILL.md` itself scannable.

## The spine is load-bearing

`spec-from-idea -> plan-from-spec -> implement -> review-code ->
finish-branch` is this repo's reason to exist. Every other skill either
feeds that chain (produces or consumes the spec/plan artifact) or is
explicitly labeled a supporting skill in `README.md` — never presented as a
peer of the spine.

`implement` and `review-code` soft-require an upstream spec/plan: they work
without one, but must visibly state "no spec/plan found — proceeding
ad-hoc" (or the review equivalent, "spec axis skipped — no spec found")
rather than silently treating a missing spec as passed or irrelevant.

Every spec produced by `spec-from-idea` carries a **Success Criteria &
Evals** section with measurable, pass/fail conditions — not a vague
"test manually" note. `plan-from-spec` carries those evals forward as a
verification step on each plan step. `implement` treats them as the
acceptance bar per step. `review-code`'s primary axis is whether the diff
satisfies them.

## Versioning

- `plugin.json` uses semver.
- Renaming a skill is a breaking change: keep the old name as a one-line
  pointer ("this skill was renamed to X, use that instead") for one release
  cycle before removing it. Never rename and delete in the same change.

## Testing

- v1 validation is a dry run against a real task plus a self-review pass
  (placeholder scan, description matches body, no contradictions) — not
  full subagent pressure-testing.
- Formal pressure-testing (adversarial scenarios run against fresh
  subagents, per the RED-GREEN-REFACTOR method for skill authoring) is a
  known follow-up once the catalog stabilizes, not a v1 requirement.

## Prose

- Write plainly. No filler, no restating what the frontmatter already said,
  no narrating the obvious.
