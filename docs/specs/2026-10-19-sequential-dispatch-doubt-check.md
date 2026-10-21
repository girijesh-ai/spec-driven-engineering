## Doubt check: SC-1 to SC-5 are each checkable with `claude plugin eval`

Each cycle sent a fresh `opus` subagent only the claim, the spec, and the
eval harness facts (Claude Code 2.1.303). Every objection was checked
against the harness source or the repo before it was accepted.

Cycles: 3 (the cap). Commits: `65af924`, `bfcaae7`, `8a5af64`.

### Cycle 1: 22 objections, all accepted

Grouped by the change they led to:

- Objection: SC-1 and SC-4 runs can't write files → accepted: `--allow-tools Write` (plus `Edit Bash` for dispatch cases).
- Objection: SC-4 asks for all 4 units and a pause in one run, but a pause ends a non-interactive run → accepted: split into SC-4a (no pause) and SC-4b (pause).
- Objection: the exit code isn't the result; 2 of 3 passing still exits 1 → accepted: the bar is the report's pass column.
- Objection: `--allow-tools Agent` is a no-op; `Agent` is always granted → accepted: dropped.
- Objection: a commit can't contain its own SHA → accepted: led to decision 1 in cycle 2.
- Objection: "failure" in the escalation rule was undefined → accepted: one attempt whose re-run Verification fails.

### Cycle 2: 15 objections, all accepted

Grouped by the change they led to:

- Objection: SC-2 with `Write` changed the existing case's conditions → accepted: back to the original grant.
- Objection: SC-3 passed when `implement` didn't fire at all → accepted: it must fire and commit each step.
- Objection: SC-4a's exact per-call models broke on escalation → accepted: only the first implementer call per unit is checked.
- Objection: SC-5's exact counts failed a correct run that stopped early → accepted: upper bounds (later reversed in cycle 3).
- Objection: `done <sha>` needs a second commit → accepted: the unit's own commit marks `done`; the message starts with the unit ID (user decision).
- Objection: approval in the prompt wasn't defined → accepted: it counts only when it names the plan file (user decision).

### Cycle 3: 12 objections, 9 accepted, 3 refuted

- Objection: `implement-small-plan` doesn't exist; "4 of 6" was another case's rate → accepted: the spec says which cases the plan writes, and credits `implement-ad-hoc`.
- Objection: SC-2's spec has 3 criteria, so planning goes into units mode with no `Write` and may stop to ask → accepted: without `Write`, `plan-from-spec` prints the index and units instead of asking.
- Objection: SC-5's one-unit plan is below the 3-unit threshold → accepted: a 3-unit plan whose unit 1 fails.
- Objection: SC-5's "stop earlier also passes" lets a run with no escalation pass → accepted: exactly 2 `sonnet` and 1–2 `opus` calls for U01.
- Objection: a call with no `model` runs on the caller's `sonnet` and slips past the checks → accepted: every call names its `model`.
- Objection: reviewer prompts also name the unit file → accepted: implementer descriptions start with `Implement U<NN>`.
- Objection: SC-4b passes a run that pauses for any reason; `Risk` had no values → accepted: `Risk` is `high` or `normal`, and the pause message says unit 2 is high-risk.
- Objection: SC-1 repeats a field as a table cell or heading undetected → accepted: no label in any form.
- Objection: line 177's approval wording can't apply to planning cases → accepted: planning prompts say the spec is approved.
- Objection: file contents (index status, test assertion) can't be graded → refuted: regex graders take a `{source: file, path}` target (harness schema, `Es()` in 2.1.303).
- Objection: "at least 3" and "every call" can't be graded because `count:N` is exact → refuted: `tool_used` takes `min`/`max`, and `input_match` is a JS `RegExp` over the call's input, so lookaheads handle any key order.
- Objection: with no `--threshold`, 2 of 3 can't be read off the report → refuted: the `PASS%` column is runs scoring 1.0 ÷ runs; the spec now says `PASS%` ≥ 67%.

Residual, not fixable with `tool_order` (first occurrences only): SC-5
can't tell `sonnet, opus, sonnet` from `sonnet, sonnet, opus`. The exact
counts narrow it; the plan's grader can add an `llm` check on the trace.

Result: decision changed to the SC-1 to SC-5 text at `8a5af64`.
