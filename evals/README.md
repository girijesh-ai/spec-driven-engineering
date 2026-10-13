# Plugin evals

Behavioural checks for the skills, run by Claude Code's own eval harness
(`claude plugin eval`). Each case gives a fresh Claude a prompt with this
plugin loaded and grades two things:

- **Did the right skill fire?** A `tool_used: Skill` grader, marked
  `arm: with-only`. It's reported, not scored, when a no-plugin baseline
  arm runs.
- **Did the skill's key behaviour show up?** `regex` and `llm` graders
  against the final message or the whole trace.

| Case | Skill | Checks |
|---|---|---|
| `spec-interview` | spec-from-idea | Classification, hypothesis + confidence, one question with a `GUESS:`, no code |
| `spec-right-size` | spec-from-idea | Sizes a small internal feature to its stated scale; recommends the minimal approach, no queue/cache/background job |
| `plan-traces-criteria` | plan-from-spec | Steps cite SC-n with commands, are sized, risky step early |
| `implement-ad-hoc` | implement | Announces "no spec/plan found", writes the test first |
| `review-no-spec` | review-code | Reports no spec, finds the pool leak on the early return with blocking severity |
| `debug-loop-first` | debug-systematically | Reproduces before fixing, finds the real cause instead of the user's `flush()` theory |
| `grill-one-question` | grill-me | One plan-challenging question with a guess, then stops |

## Running

From the repo root:

```
claude plugin eval . --no-publish --model sonnet
```

- Firing is stochastic: keep the default 3 runs per case, and pin
  `--model` and the Claude Code version when comparing results over time.
- `implement-ad-hoc` and `debug-loop-first` build a small repo with
  `scaffold.sh` and need to run tests, so they need
  `--scaffold --allow-tools Write Edit Bash`. Bash in evals needs an OS
  sandbox (`bubblewrap` and `socat` on Linux); without one the harness
  refuses the run. With only `--allow-tools Write Edit` they still show
  whether the skill fires, but their test-first / reproduce-first graders
  fail because nothing can run.
- One case: `--case spec-interview`. `--case` takes one glob and doesn't
  expand braces.
- A full run is roughly 6 cases × 3 runs × 2 arms (with and without the
  plugin) at about $0.10 each. Results land in `evals/results/` (ignored by
  git).

## Readings so far

Single runs (`--runs 1`/`2 --ablation none`) on 2026-10-12, Claude Code
2.1.296, default model. Indicative only — not enough runs to call a rate.

| Case | Fired (all runs) | Outcome (latest version) | Notes |
|---|---|---|---|
| spec-interview | 2/2 | 1/1 | First run bundled four sub-questions under one `Q:`; skill now says one question is one decision |
| plan-traces-criteria | 1/1 | 1/1 | |
| implement-ad-hoc | 4/6 | 0/4 | Didn't fire until the description named small one-off changes. Outcome blocked: Bash fails in the sandbox here (see below) |
| review-no-spec | 3/4 | 1/1 | Didn't fire on an inline diff until the description named it |
| debug-loop-first | 3/4 | 0/3 | Didn't fire in an empty workspace (case fixed with a scaffold). With Bash failing, it fixed the right bug by reading the code but skipped the reproduction; skill now says to stop and ask in that case |
| grill-one-question | 4/4 | 1/2 | Failures: trailing follow-up asks after the `GUESS:`; skill now says to end there |

With `bubblewrap` 0.4.0 and `socat` installed (RHEL 8), the sandbox starts
but every Bash call inside it fails with `bwrap: Can't create file at
/usr/bin/git: Permission denied`, so the two scaffolded cases can't run
their tests on that host. Their trigger graders are still meaningful;
their outcome graders need a host where sandboxed Bash works.
