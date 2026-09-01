# Architect persona: `writing-for-agents`

Real governance/standards work against
[`huggingface/smolagents`](https://github.com/huggingface/smolagents),
using the skill an Architect reaches for when the question is "are our
own rules any good," not "does this feature work."

## The target: the real `AGENTS.md`

```markdown
# Contributor Guidelines
- Follow OOP principles
- Be Pythonic: follow Python best practices and idiomatic patterns
- Write unit tests for new functionality
```

Three bullets, sitting at the repo root — the actual file any AI
coding agent (or new human contributor) reads first.

## Applying the skill's own rules, not vibes

1. **"Follow OOP principles" states a goal, not a rule.** Nothing about
   it is checkable — an agent reading this has no way to self-verify.
2. **"Be Pythonic: follow Python best practices" is circular** — it
   defines "Pythonic" as "Python best practices" without saying what
   those are.
3. **"Write unit tests for new functionality"** is the closest of the
   three to checkable (a test exists or it doesn't), but doesn't say
   where or how to run them.

## The finding that makes this more than a style nitpick

Checked whether the codebase actually has a real, enforced definition of
"Pythonic" and "tested" sitting nearby — it does, one file away, and
`AGENTS.md` never mentions either:

- `pyproject.toml`'s `[tool.ruff]` config: `line-length = 119`,
  `lint.select = ["E", "F", "I", "W"]` — the *actual, enforced* meaning
  of "Pythonic" for this repo.
- `CONTRIBUTING.md` documents `make quality` (runs that config) and
  `make test` — commands that already exist and already work.

**`AGENTS.md` restates vague versions of rules that `CONTRIBUTING.md`
already states precisely, and never links to it.** That's a violation of
this skill's own "cross-reference by name" rule — not a hypothetical
one, a real gap between two files in the same repo.

## Proposed rewrite

```diff
 # Contributor Guidelines
-- Follow OOP principles
-- Be Pythonic: follow Python best practices and idiomatic patterns
-- Write unit tests for new functionality
+- New agent/tool/model types extend the existing base class (`Tool`,
+  `Model`, `MultiStepAgent`) rather than reimplementing its interface.
+- Run `make quality` before opening a PR — enforces this repo's actual
+  style rules (`pyproject.toml`'s `[tool.ruff]` config: 119-char lines,
+  `E`/`F`/`I`/`W` rule sets).
+- New public functions/classes get a test in the matching
+  `tests/test_<module>.py`. Run `make test` locally before opening a PR
+  (full details: `CONTRIBUTING.md`).
```

Every line is now either directly checkable (a command that passes or
fails) or points at the file that already has the real answer, instead
of restating a vague paraphrase of it.

## What this demonstrates

The Architect persona isn't about writing more code — it's about noticing
that the document meant to onboard every future contributor (human or
agent) says nothing an agent could actually check itself against, while
the *real* answer already exists two files away, unlinked. That's exactly
the kind of gap that compounds silently: every future AI-assisted PR
against this repo reads `AGENTS.md`, gets vague guidance, and never
discovers `make quality` exists until CI fails.
