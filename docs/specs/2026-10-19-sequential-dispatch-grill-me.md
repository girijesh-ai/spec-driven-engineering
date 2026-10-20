# grill-me log: sequential dispatch

The questions asked on 2026-10-19 before writing
[`2026-10-19-sequential-dispatch.md`](2026-10-19-sequential-dispatch.md),
with each answer and the decision it led to. The wording of each `Q:` and
`GUESS:` is as asked.

## Decisions

| # | Decision | Changed the proposal? |
|---|---|---|
| 1 | Units are Markdown files in the repo | Confirmed |
| 2 | One branch, one PR at the end | Confirmed |
| 3 | Escalation to `opus` is automatic; 2 failures on `opus` stop the run | Confirmed, stop rule added |
| 4 | Pause after every 3 units and before any high-risk unit | Confirmed |
| 5 | No separate test writer for tier-L units in v1 | Confirmed, after discussion |
| 6 | Dispatch mode switches on automatically | Changed (guess was "only when asked") |
| 7 | Claude Code uses `sonnet` and `opus` only; OpenCode gets two agent definitions | Changed (proposal had `haiku` for S) |
| 8 | Dispatch only for plans with 3+ units | New |
| 9 | Approach C: plan is the index, unit files hold the detail | Changed (guess was A) |

## Questions

**1. Q:** Where should each unit's file live: as a Markdown file in the repo
(`docs/plans/<topic>/units/NN-slug.md`), or as a GitHub issue?
**GUESS:** As a file in the repo. Files work the same in OpenCode and
offline, and need no GitHub access or permissions. Each file's `Status:`
line (`todo` → `done <sha>`) is also what lets a stopped run pick up where
it left off.
**Answer:** agree.

**2. Q:** When the units are all done, should the work land as one branch
with one PR, or as one PR per unit?
**GUESS:** One branch with one PR at the end. Each unit is already its own
commit, so any one can be reverted on its own. Many success criteria only
pass once several units are in. A PR per unit would also give reviewers
5–8 separate reviews instead of one.
**Answer:** agree.

**3. Q:** When a unit fails its check twice and gets re-run one tier up,
should the jump to opus (the strongest and most expensive model) happen
automatically, or stop and ask you first?
**GUESS:** Automatically, with a hard stop after it. Asking mid-run would
break the "one approval, then it runs" flow. A unit that then fails twice
on opus stops the run and asks, so the extra cost is at most two opus
attempts per unit.
**Answer:** agree.

**4. Q:** Should the run pause for you to look at the work after every 3
units, or only before units marked high-risk?
**GUESS:** After every 3 units, and also before any high-risk unit.
Riskiest units run first, so the risk rule alone would wave through a long
tail of low-risk units unseen. On 5–8 units, that's 1–2 pauses.
**Answer:** agree.

**5. Q:** For the hardest units (tier L), should a separate agent write the
failing test first, without seeing the code, or should that be left out of
v1?
**GUESS:** Leave it out of v1. The floor guard and the mutation spot-check
(the reviewer breaks the code and confirms the test goes red) already cover
a weak test. Add it if the dry run shows a tautological test (one that
passes whatever the code does) getting through on an L unit.
**Answer:** "yes, For the hardest units (tier L), should a separate agent
write the failing test first". This took four follow-up questions to
settle; see the note below. Final answer: rely on the existing checks in
v1.

**6. Q:** Should `implement` run in dispatch mode only when you ask for it,
or automatically whenever the plan has units?
**GUESS:** Only when you ask, because we don't yet know whether it costs
fewer tokens than a single session on a typical plan.
**Answer:** No, it should switch on automatically. Use only sonnet and
opus on Claude Code, and whatever is available on OpenCode. This gave
decisions 6 and 7.

**7. Q:** Should dispatch mode switch on for every plan, including one with
only 1 or 2 units?
**GUESS:** Only for plans with 3 or more units. With 1 or 2 units, the
context never grows enough for a fresh start to help, but each unit still
pays for re-reading and its own reviewer.
**Answer:** agree.

**8. Q:** Can the plan step itself be the unit (approach A), instead of
writing a separate file per unit?
**GUESS:** Yes, go with A. It avoids two records of status that can
disagree.
**Answer:** The user pushed back: spec → plan → units should stay in sync
to avoid drift, and focused units improve quality. That led to approach C.

**9. Q:** Should units be split this way, with the plan as a
one-line-per-unit index that owns `Status`, `Depends on`, `Satisfies` and
`Tier`, and each unit file holding only the detail?
**GUESS:** Yes, C. No field exists in two places, so nothing can drift.
Resume still reads one file, the plan.
**Answer:** agree C.

The three design sections and the Success Criteria table were then each
shown and agreed.

## Note for the reader check

Two questions did not land in one read, and the colleague check should
take that into account:

- **Q5** got an answer that repeated the question, which could mean yes to
  the question or yes to the guess. It took four follow-up questions to
  settle.
- **Q6** was asked three times, because the reply raised two points first:
  whether dispatch is still sequential, and what "cost" meant (tokens).
  The first GUESS said "dispatch spends more agents" without saying that
  meant tokens.
