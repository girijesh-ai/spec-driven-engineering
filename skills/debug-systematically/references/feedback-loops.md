# Ten ways to build a feedback loop

Step 1 of the loop needs one command that goes red on the user's exact
symptom, runs deterministically, runs fast, and needs no human. Pick the
cheapest shape below that can observe the symptom. (Adapted from
mattpocock/skills' `diagnosing-bugs`.)

| # | Loop | Use when | Red means |
|---|---|---|---|
| 1 | **Failing test** in the project's suite | The bug is reachable through code the suite can call | The assertion encoding the expected behaviour fails |
| 2 | **curl / HTTP script** | The symptom is a wrong response from a running service | Status, header, or body differs from expected (`jq -e`, `grep -q`) |
| 3 | **CLI + snapshot diff** | The symptom is wrong output from a command | `diff expected.txt <(cmd)` is non-empty |
| 4 | **Headless browser** (Playwright, Puppeteer) | The symptom only shows in a rendered page | A selector, text, or console error assertion fails |
| 5 | **Trace / request replay** | You have a recorded failing request, event, or log line | Replaying it reproduces the bad result |
| 6 | **Throwaway harness** | The code is hard to reach through the real entry point | A 20-line script calling the suspect function directly shows the bug |
| 7 | **Fuzz / property loop** | The trigger input is unknown | The loop finds an input that violates the property; save that input |
| 8 | **Bisection harness** | It used to work | `git bisect run <script>` exits non-zero on bad commits |
| 9 | **Differential loop** | A reference exists (old version, other implementation, spec) | Outputs of the two differ for the same input |
| 10 | **Human-in-the-loop script** | The last resort: a step only a person can do | The script automates everything else and prints exactly one question for the human |

## Making a loop good enough

- **Red-capable:** run it now and watch it fail on the symptom the user
  reported, not a neighbouring one.
- **Deterministic:** pin seeds, clocks, and ordering. If it still varies,
  run it N times and report the failure rate — raising that rate is
  progress.
- **Fast:** seconds, not minutes. Narrow the input or call the function
  directly before accepting a slow loop.
- **Agent-runnable:** no interactive prompts, no manual browser clicks
  (except loop 10, which makes the human step explicit).

Keep the loop command in your notes. It becomes the regression test in
step 8, and it's what a handoff doc should carry if the session ends
before the fix.
