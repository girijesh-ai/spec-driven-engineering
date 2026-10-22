# Upstream findings: what to adapt from mattpocock/skills and addyosmani/agent-skills

Date: 2026-10-12. Status: **decided and implemented in 2.0.0** except item 15 (see the checklist at the bottom).

Re-checked line by line against the same upstream versions on 2026-10-22. Rows marked
*(corrected 2026-10-22)* were wrong or incomplete; the [addendum](#addendum-2026-10-22-re-check-against-source)
at the end lists the fixes and where our skills drifted from upstream.

Compared against: this repo at `plugin.json` 1.1.0 (17 skills, `main` @ `152b7b7`).

| Source | Version read | Released | Shape |
|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | v1.3.1 | 2026-10-04 | 27 promoted skills, many 7–40 lines; composable, no owned process |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 0.6.12 | 2026-10-03 | 25 skills, 200–400 lines each; lifecycle spine + evals, hooks, personas |

Tags used below: **M** = mattpocock, **A** = agent-skills, **both** = both sources independently
point the same way (strongest signal).

How to use this doc: mark the [Decisions for review](#decisions-for-review) checklist at the
bottom. Everything above it is the evidence behind each line.

---

## 1. Where we stand

**Our edge — neither source has it.** Measurable Success Criteria & Evals traced from spec → plan
step → `review-code`'s primary axis → `finish-branch`.
- M's `to-spec` has user stories, implementation and testing decisions, but no measurable criteria;
  its `code-review` Spec axis checks "requirements", not evals.
- A's specs ask for "specific, testable conditions", but plan tasks invent their own acceptance
  criteria with no link back to the spec, and "Manual check" is an allowed verification.

Keep this as the spine's identity. Every adaptation below should plug *into* the eval thread, not
replace it.

**Also ahead:** `review-code` (full-file reads, caller grep, resource/failure-path audit) is deeper
than both M's `code-review` and A's `code-review-and-quality`. `debug-systematically`'s "fix at the
root — grep every caller" step exists in neither.

**Our gaps, in short:**
- No measurement of our own skills — A has three eval tiers + CI; we have structural validation only
  and no CI at all.
- No mechanical guards — "never weaken an assertion" is prose only.
- Thinner debugging, interviewing and planning heuristics than both sources.
- No persistent vocabulary or decision records (ADRs); definitions die inside each spec.

---

## 2. Themes, ranked

### Tier 1 — fits the spine, high value, low structural risk

#### 1. `debug-systematically` (both)

| From | Technique | Note |
|---|---|---|
| M | **Phase 1 = build a feedback loop.** Done only when there is *one command*, already run, that is **red-capable** (asserts the user's exact symptom), deterministic, fast, agent-runnable. "No red-capable command, no Phase 2." | Sharper completion criterion than our "get a reliable repro" |
| M | 10 ways to build a loop (failing test, curl script, CLI + snapshot diff, headless browser, trace replay, throwaway harness, fuzz loop, bisection harness, differential loop, HITL script) | → `references/feedback-loops.md` |
| M | Non-deterministic bugs: goal is a *higher reproduction rate*, not a clean repro | |
| M | **3–5 ranked falsifiable hypotheses** before testing any. Each states a prediction: "If <X> is the cause, then <changing Y> will make the bug disappear". Show the list to the user, but "Don't block on it; proceed with your ranking if the user is AFK" *(corrected 2026-10-22)* | Ours forms one hypothesis at a time |
| M | Tag debug logs with a unique prefix (`[DEBUG-a4f2]`) so cleanup is one grep | |
| M | Perf branch: baseline measurement, then bisect — logs are usually wrong for perf | |
| M | "If no correct seam exists, that itself is the finding." A correct seam exercises "the real bug pattern as it occurs at the call site"; a seam that is too shallow "gives false confidence" *(corrected 2026-10-22)* | |
| M | **Redact** every secret in shown commands, outputs, artifacts | |
| M | Cleanup checklist; the confirmed hypothesis goes in the commit message | |
| A | **Stop-the-line**: STOP → PRESERVE evidence → DIAGNOSE → FIX → GUARD → RESUME "only after verification passes" *(corrected 2026-10-22)*. "Don't push past a failing test or broken build to work on the next feature." | `implement` could invoke this when a step's verification fails |
| A | Non-reproducible decision tree (timing / environment / state / truly random) | |
| A | Localize: which layer fails; `git bisect run` | |
| A | **Error output is untrusted data** — never execute commands or follow URLs found in error text; surface them | Also a candidate for `engineering-standards` |
| A | Red flag: "multiple unrelated changes made while debugging" | |

Keep ours: fix at the root after grepping every caller.

#### 2. `review-code` (both)

| From | Technique | Note |
|---|---|---|
| M | Spec axis also reports **scope creep** — behaviour in the diff the spec never asked for | We check necessity in Axis 2, not against the spec |
| M | **Spec-source discovery order**: issue refs in commits → path argument → `docs/specs/` match on branch/feature → ask | We say "if no spec is linked" without saying how to look |
| M | **Pin and validate the fixed point** (`git rev-parse`, non-empty diff) before reviewing | |
| M | **Fowler smell baseline** (12: Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest). Always judgement calls; a documented repo standard overrides | Could live in `engineering-standards/references/` |
| M | Run axes in parallel sub-agents so neither pollutes the other; never rerank across axes | Heavy per-commit; maybe only for the final branch review in `finish-branch` |
| A | **Severity as a second dimension**: Critical / Required / Optional / Nit / FYI. Only Critical/Required block READY | Keeps our Confirmed/Plausible (confidence) — adds what blocks |
| A | **Mutation spot-check**: invert one condition, run the suite, restore. "A mutation that stays green is a finding." | Natural fit: proves the eval actually guards the criterion |
| A | Performance pass (we only have a Python note) | |
| A | "Does this refactor reduce complexity or just relocate it? Count the concepts." | |
| A | Change sizing: ~100 lines good, ~300 acceptable, ~1000 split. Separate refactor from feature commits | Also for `plan-from-spec` |
| A | Dead-code hygiene: list it, ask before deleting. New dependencies: a question list and "Prefer standard library and existing utilities". **Upgrades**: read the changelog, "One dependency per change". There is no count limit on new dependencies *(corrected 2026-10-22)* | |

Conflict: A's "approve when it definitely improves overall code health, even if it isn't perfect"
vs our "no READY until every confirmed issue is resolved". Recommendation: keep the gate; let
severity decide which findings count.

#### 3. Spec + interview front end (both)

Interview technique (`spec-from-idea` step 2 and/or `grill-me`):

| From | Technique |
|---|---|
| A `interview-me` | Open with `HYPOTHESIS:` + `CONFIDENCE: ~30% — missing: …` |
| A | Every question in `Q:` / `GUESS:` form — never ask without your guess |
| A | "Want vs should-want" probe on buzzword answers: "If you didn't have to justify this to anyone, what would you actually want?" |
| A | **Stop test**: "Can I predict the user's reaction to the next three questions I would ask?" |
| A | "Not a yes" list: "Whatever you think", "Sounds good", "Sure, let's go" |
| A | 6-line restate before moving on: Outcome / User / Why now / Success / Constraint / Out of scope |
| M `grilling` | Each question carries a recommended answer (`➡️`) |
| M | **Facts are the agent's job** (look them up, dispatch a sub-agent); **decisions are the user's** |
| M | Explicit confirmation gate before acting |

Convergence: **every question carries the agent's recommendation/guess**. Ours doesn't.
Divergence: M asks in numbered rounds over the "frontier"; A asks one at a time (as we do).

Spec template additions (`spec-from-idea`):

| From | Section / rule |
|---|---|
| A | **Assumptions** block — "ASSUMPTIONS I'M MAKING: … → Correct me now or I'll proceed" |
| A | **Boundaries** — Always / Ask first / Never |
| A | **Commands** — the project's build, test, lint and dev commands, "with flags, not just tool names". Our per-criterion `Check:` command is our own adaptation of this, not A's rule *(corrected 2026-10-22)* |
| A | "Reframe instructions as success criteria" ("faster" → "LCP < 2.5s") — we already do this |
| A | Living spec: change the spec first, then the code |
| A | Stop after writing the spec; plan in a later turn |
| M | Testing decisions: name the seams — highest seam possible, fewest seams, confirm with the user |
| M | No file paths or code in the spec (they go stale); exception for decision-rich prototype snippets |

#### 4. `plan-from-spec` (both)

| From | Technique |
|---|---|
| M | **Wide refactor = expand / migrate in batches / contract.** When one mechanical change breaks thousands of call sites, no vertical slice lands green: add the new form beside the old, migrate in batches sized by blast radius, then delete the old |
| M | Prefactor first: "make the change easy, then make the easy change" |
| M | Each step sized to fit one fresh context window |
| A | Sizing table XS–XL; split when >3 acceptance bullets, "and" in the title, or two subsystems |
| A | **Risk-first ordering** — high-risk steps early |
| A | Checkpoints every 2–3 steps |
| A | **Never overwrite an incomplete plan** — stop and ask |
| A | Parallelization notes: safe / sequential / needs coordination |

Already ours: dependencies ("Depends on" = M's blocking edges), tracer bullets, traced verification, reuse.

#### 5. `test-driven-development` (both)

| From | Technique |
|---|---|
| M | **Tautological test** anti-pattern: expected value recomputed the way the code does (`expect(add(a,b)).toBe(a+b)`) |
| M | **Horizontal slicing** anti-pattern: writing all tests first |
| M | Mock only at **system boundaries** (external APIs, time, randomness); SDK-style interfaces over generic fetchers |
| M | Test only at **pre-agreed seams** — for us, sourced from the plan step, not a fresh prompt |
| A | Discover the stack's test command first — never assume `npm test` |
| A | Double ladder: Real > Fake > Stub > Mock |
| A | Reproduction test written by a sub-agent "without knowledge of the fix" |
| A | Verification includes "no tests were skipped" and "coverage hasn't decreased" |

Already ours, stricter: "delete means delete", fail-for-the-right-reason, never weaken an assertion.

#### 6. `implement` + `finish-branch` hygiene (both)

| From | Target | Technique |
|---|---|---|
| A | implement | `NOTICED BUT NOT TOUCHING: … → Want me to create tasks for these?` |
| A | implement | Tripwire: >100 lines written without running tests |
| A | implement | Rollback-friendly: don't delete and replace in the same commit; keep it compilable |
| M | implement | Cadence: typecheck and single test files often, full suite once at the end |
| M `pr` | finish-branch | PR body: **Summary** as the smallest visual (pseudocode, call tree, file tree, Mermaid, shaped diff) |
| M `pr` | finish-branch | **Evidence** before/after — maps directly onto our Success Criteria results |
| M `pr` | finish-branch | **Merge Danger** — one-way or two-way door, blast radius |
| A | finish-branch | Change summary with "THINGS I DIDN'T TOUCH (intentionally)" and potential concerns |
| A | finish-branch | Rollback plan + acknowledged risks before GO |

Credit: M's `pr` Summary visuals come from Dex Horthy's `show-me` (HumanLayer).

#### 7. `handoff` (both) + phase boundaries (M)

| From | Technique |
|---|---|
| M | Redact secrets / PII |
| M | Reference artifacts (specs, plans, ADRs, commits) by path — don't duplicate them |
| M | Optional argument: what the next session is for; tailor the doc to it |
| A | Record working-tree state and uncommitted changes, the exact verification commands and their results, and open approvals |
| A | "Do not infer approval from a previous conversation unless the durable artifact records it" |
| M | **Phase-boundary tree** for `dev-workflow`: continue → clear → handoff → subagent → compact (compact is the default, not the first reach). Handoff is narrow: only when something must travel (new harness, new directory, colleague, mid-phase side task) |

Decision: M saves handoffs to the OS temp dir; ours implies in-repo.

#### 8. Cross-skill call phrasing (M)

M found a skill named in prose ("run the `/grilling` skill") does not reliably load it. Operative
calls are now phrased **"Call the Skill tool with `grilling`"**; two skills = two calls, said so.
Ours say "invoke `review-code`". Mechanical sweep across all skills. (Router prose that just names
skills for a human, like `dev-workflow`'s table, stays as plain labels.)

---

### Tier 2 — bigger moves, each needs a decision

#### 9. Measure our own skills (A)

A runs three tiers:

| Tier | Checks | Runs |
|---|---|---|
| 1 Structural | frontmatter, required sections, 500-line cap, 1024-char description | CI |
| 2 Trigger/routing | each positive prompt ranks its skill in top_k; negatives go to their `owner`; description collision ≥0.75 cosine = error | CI (TF-IDF, no deps) |
| 3 Behavioral | `claude -p` runs the skill on fixtures in a throwaway repo; a second `claude -p` grades the trace against `expectations[]` | on demand |
| Plugin evals | `claude plugin eval . --no-publish`: does Claude Code's real router fire the skill, with/without-plugin delta | on demand |

Case schema (condensed):
```json
{"skill_name":"using-agent-skills",
 "trigger":{"positive":[{"prompt":"Which skill should I use for this task?","top_k":3}],
            "negative":[{"prompt":"Debug the null pointer crash in checkout","owner":"debugging-and-error-recovery"}]},
 "evals":[{"id":1,"prompt":"...","expected_output":"...","files":["..."],
   "expectations":["The chosen skill matches the decision tree", "..."]}]}
```

Plugin-eval lessons A recorded: firing is stochastic (5/7 runs); pin `--model` and the Claude Code
version; ≥10-turn budget; one description clause ("applies even when the diff is pasted inline")
moved fires from 7/27 to 21/27.

Estimated effort for our 17 skills:
- Plugin evals (`experimental.evals` in `plugin.json` + 4–6 case dirs): ~half a day, no code.
- Tier 2 trigger/collision eval in Python + GitHub Actions: 1–2 days. Real collision risk for us:
  implement / test-driven-development, review-code / engineering-standards,
  grill-me / domain-modeling / spec-from-idea.
- Tier 3 behavioral + pressure cases: 3–5 days + tokens. This *is* the "formal pressure-testing"
  follow-up our CLAUDE.md already names.

#### 10. Floor guard (A `constraint-driven-development`)

A diff-scoped script (merge-base → working tree + untracked) that flags, on added lines:
new suppressions (`istanbul ignore`, `nosemgrep`, …), stubs, skipped tests, deleted test files,
removed assertions in surviving test files, and a loosened threshold, removed rule or new exception
row in `CONSTRAINTS.md`. A's stubs include an empty `catch {}` and `TODO`; its suppressions include
`gitleaks:allow` and `Stryker disable`. Our `floor_guard.py` covers none of the `CONSTRAINTS.md` moves
(it skips `*.md`) and none of those four patterns *(corrected 2026-10-22)*. Exit 0/1/2,
"never let a 2 read as a 0"; reports rule + location, never secret values. "Tightening the bar
should be silent; loosening it should be loud."

Why it matters for us: the cheapest road to a green Success Criterion is to weaken the test. This
makes that mechanical instead of prose. Optional companion: a project `CONSTRAINTS.md` (Floor;
Enforced with numbers — Rule / Checked by / Runs at; Measured-not-enforced ratchets; Exceptions
with owner and expiry).

#### 11. Rationalizations + Verification sections (A)

Every A skill except `using-agent-skills` and `idea-refine` (exempt in `scripts/lib/skill-lint.js:87`) *(corrected 2026-10-22)* has `| Rationalization | Reality |` (the agent's own excuse, quoted, then rebutted),
a Red Flags list, and a Verification evidence checklist; their linter enforces it. Ours has
`| Mistake | Fix |`, which describes behaviour rather than pre-empting the excuse. Option: add both
sections to the discipline skills (spec-from-idea, implement, review-code, TDD,
debug-systematically) and enforce in `scripts/validate.py`.
Counterpoint (M `writing-for-agents`, "Negation"): naming the forbidden behaviour primes it;
prompt the positive target instead.

#### 12. `codebase-architecture` (both)

| From | Technique |
|---|---|
| M | **Deletion test**: imagine deleting the module — if complexity vanishes it was a pass-through; if it reappears across N callers it was earning its keep |
| M | "One adapter means a hypothetical seam. Two adapters means a real one." |
| M | The interface is the test surface |
| M | Dependency categories decide the test strategy: in-process / local-substitutable / remote-but-owned (ports & adapters) / true external (mock) |
| M | Replace, don't layer: delete old shallow-module tests once interface tests exist |
| M | **Design it twice**: 3+ sub-agents each produce a radically different interface under a different constraint, then compare on depth, locality, seam placement — could upgrade `spec-from-idea`'s "2–3 approaches" |
| A | Hyrum's Law; one error format everywhere; idempotency-key rules (atomic claim, payload hash, in-flight duplicate behaviour) |

#### 13. Persistent vocabulary and decisions (both)

- M `domain-modeling`: repo-level `GLOSSARY.md` (created lazily, no implementation detail), challenge
  terms against it, cross-check claims against code, **offer an ADR only when hard to reverse +
  surprising without context + a real trade-off**.
- A `documentation-and-adrs`: ADR template (Status / Context / Decision / Alternatives / Consequences),
  supersede never delete, match the repo's existing convention.

Today our `domain-modeling` writes definitions into one spec; they don't outlive it.

#### 14. New supporting-skill candidates

| Candidate | From | What | Fit |
|---|---|---|---|
| doubt-check | A `doubt-driven-development` | Fresh-context adversarial check of a non-trivial decision mid-work: CLAIM (2–3 lines, kept by the author) → EXTRACT (artifact + contract only: "Do NOT pass the CLAIM") → DOUBT ("Do NOT validate") → RECONCILE (contract misread / valid + actionable / valid trade-off, documented / noise) → STOP on trivial or already-considered findings, or after 3 cycles, then escalate to the user. "Doubt theater" = 2+ cycles of substantive findings with none accepted: "Stop and escalate". Cannot run inside a subagent. Cross-model offer in every interactive cycle; an external CLI only with explicit user authorization *(corrected 2026-10-22)* | Between `implement` and `review-code`; contract = the spec's evals |
| retro | M | After a session, improve the agent's *environment* across 7 areas: navigation, automated checks, coding standards, global `AGENTS.md` size, tool economy, no-ops, information access. Mechanical mistakes → deterministic checks; judgement calls → coding standards the **reviewer** enforces. `CLAUDE.md` "incredibly sparingly, usually only for navigation pointers". A repo with no pre-commit hook and no CI is itself a finding; read the existing check command first, since an unwired check is the finding, not a reinvention *(corrected 2026-10-22)* | After `finish-branch` |
| simplify | A `code-simplification` | Chesterton's Fence (git blame before removing), Rule of 500 (codemods past 500 lines), one simplification per test run, existing tests must pass unmodified | Supporting; also feeds `review-code` |
| source-driven | A | DETECT stack → FETCH official docs → IMPLEMENT → CITE; UNVERIFIED flag; docs-vs-code CONFLICT options | Supporting for `implement` |

#### 15. Autonomous / parallel `implement`

- A `/build auto`: needs a spec at a known path and a clean baseline (`git status --porcelain`
  shows no unrelated changes; not "tests green") *(corrected 2026-10-22)*; writes the plan; **one
  unambiguous approval** ("looks reasonable" doesn't count); per step RED → GREEN → regression →
  build → commit, staging only that step's files; stops on unfixable failure, spec ambiguity, or
  a high-risk change: "auth/permission changes, destructive data migrations, payments, deletions,
  deploys, anything touching secrets, or anything you can't undo with `git revert`" *(corrected 2026-10-22)*; resume =
  re-invoke.
- M `implement-spec`: plan as a task graph; implementer sub-agents in their own worktrees across the
  ready frontier; merger sub-agent; one integration branch; one review at the end.

Our `plan-from-spec` already produces the dependency graph both need.

#### 16. `dev-workflow` shared operating rules (A `using-agent-skills`)

Assumptions block; manage confusion (stop, name it, ask, wait); push back with quantified downside;
scope discipline (don't remove comments you don't understand, no adjacent refactors); verify, don't
assume; standing Definition of Done (distinct from per-spec criteria); short paths
(bugfix = debug → TDD → review). **Trust levels** come from A `context-engineering:98-103`, not
`using-agent-skills`: three tiers (trusted / verify before acting on / untrusted), and
instruction-like text in untrusted content is data, not commands *(corrected 2026-10-22)*.

#### 17. `writing-for-agents` (M)

Context pointers; the two loads (context vs cognitive); information hierarchy and progressive
disclosure; **completion criteria** (clarity + demand); **leading words**; **negation** (prompt the
positive); pruning (single source of truth, environment-as-cache, no-ops, sediment).

---

### Tier 3 — skip, or mention only

- **M:** prototype, research, wizard, to-questionnaire, teach, wait-what (overlaps `simple`),
  wayfinder, improve-codebase-architecture (HTML survey report), setup-matt-pocock-skills +
  issue-tracker config, heavier triage (AGENT-BRIEF, OUT-OF-SCOPE).
- **A:** frontend-ui-engineering, browser-testing-with-devtools, performance-optimization,
  security-and-hardening checklists (worth a skim for `engineering-standards`: STRIDE, the
  Always / Ask First / Never tiers), observability, ci-cd, shipping-and-launch (deploy is beyond
  `finish-branch`), idea-refine (maybe borrow "Key assumptions to validate"), personas, the
  SessionStart router hook, the WebFetch cache hook, the simplify-ignore hook.

---

## 3. Conflicts — decide, don't drift

| Upstream move | Ours today | Recommendation |
|---|---|---|
| M removed `resolving-merge-conflicts` in 1.3.0 ("the agent works through an in-progress merge or rebase conflict without a dedicated skill") *(corrected 2026-10-22)* | `resolve-merge-conflicts`, dry-run proven on smolagents | Keep |
| M: "refactoring is not part of the loop" (moved to review) | red-green-refactor | Keep ours |
| M: grilling in rounds over a frontier; A: one at a time | one at a time | Keep one at a time; add recommendation/guess per question |
| A: "Manual check" allowed as verification | "never test manually" | Keep ours |
| A: DAMP over DRY in tests | `engineering-standards` DRY ("The moment the same block appears a second time, extract it") *(corrected 2026-10-22)* has no test exemption | Adopt a test exemption — real gap |
| A: approve when code health improves | READY only when no confirmed issue | Keep the gate; severity decides which findings block |
| M: user-invoked vs model-invoked split | all model-invoked (the spine calls itself) | Skip |
| A: SessionStart hook injecting the router | native routing | Skip — A leaves it unwired itself; "never run two routers" |
| M: no em-dashes anywhere | ~200 in SKILL.md files | Skip unless wanted |

## 4. Repo hygiene worth copying

- `CHANGELOG.md` — we have none, while README describes verified version bumps.
- CI workflow (validate, tests, trigger eval, `claude plugin validate`, install smoke test).
- A record of rejected ideas so they aren't re-proposed: M's `.out-of-scope/`, or A's
  `evals/skill-impact.md` ledger (rejected changes + eval evidence).
- Defensive quoting of `description` frontmatter (M had 6 skills drop from discovery over a bare
  `: `). Checked: all 17 of ours parse as YAML today.

## 5. Constraints any adaptation must respect

- Flat `skills/<name>/`; material over 100 lines in `references/*.md`.
- Descriptions stay "Use when…" trigger-first.
- Docs keep the four sections; new skills start `**Status:** draft` until dry-run.
- `scripts/validate.py` stays green; semver bump in `plugin.json`.
- Credit both upstreams (and Dex Horthy for the PR template) in README Credits.

---

## Appendix A — mattpocock/skills v1.3.1, per skill

| Upstream skill | Lines | Maps to ours | Notes |
|---|---|---|---|
| ask-matt (+ PHASE-BOUNDARIES) | 95 + 55 | dev-workflow | User-invoked router over main flow, on-ramps, standalones; phase-boundary tree |
| grill-with-docs / grill-me / grilling | 7 / 7 / 28 | grill-me | Wrappers over one `grilling` primitive (rounds, frontier, facts vs decisions) |
| to-spec | 75 | spec-from-idea | No interview, synthesizes the conversation; seams; publishes to issue tracker |
| to-tickets | 105 | plan-from-spec | Tracer-bullet tickets with blocking edges; expand–contract for wide refactors |
| implement | 15 | implement | Thin: tdd at agreed seams, typecheck often, code-review, commit |
| implement-spec | 40 | — | Parallel worktree implementers across the frontier (graduated in 1.3.0) |
| tdd (+ tests.md, mocking.md) | 38 + 136 | test-driven-development | Seams, tautological + horizontal anti-patterns, mock at boundaries |
| diagnosing-bugs | 138 | debug-systematically | Feedback-loop-first, 6 phases, redact |
| code-review | 87 | review-code | Standards + Spec axes as parallel sub-agents, Fowler baseline |
| pr | 170 | finish-branch | PR body template (graduated in 1.3.0) |
| retro | 44 | — | Environment improvements after a session (graduated in 1.3.0) |
| codebase-design (+ DEEPENING, DESIGN-IT-TWICE) | 114 + 81 | codebase-architecture | Deep-module vocabulary, dependency categories, design it twice |
| improve-codebase-architecture | 71 + 123 | — | Hot-spot-scoped survey, HTML report, then grilling |
| domain-modeling (+ formats) | 74 + 107 | domain-modeling | GLOSSARY.md + ADRs |
| handoff | 16 | handoff | Temp dir, suggested skills, reference don't duplicate, redact |
| writing-for-agents (+ SKILL-MECHANICS) | 81 + 22 | writing-for-agents | See theme 17 |
| triage | 112 + 312 | triage-issues | Triage roles mapped to tracker labels, agent brief |
| prototype, research, wizard, wayfinder, teach, to-questionnaire, wait-what, setup-matt-pocock-skills | — | — | Tier 3 |

CHANGELOG highlights 1.1.0 → 1.3.1:
- 1.1.0: `to-prd` → `to-spec`; `to-plan` + `to-issues` merged into `to-tickets`; `code-review`
  promoted with the Fowler baseline; grilling gains a confirmation gate and facts vs decisions.
- 1.2.0: shipped as a Claude Code plugin; Codex metadata (`agents/openai.yaml`) beside every skill;
  grilling moves to rounds; `writing-great-skills` → `writing-for-agents` (breaking, no alias);
  six skills removed.
- 1.2.3: `diagnosing-bugs` redacts secrets; Claude-specific tool names dropped from sub-agent steps.
- 1.3.0: `implement-spec`, `pr`, `retro` graduated; `resolving-merge-conflicts` removed;
  `CONTEXT.md` → `GLOSSARY.md`; em-dashes removed repo-wide; "Call the Skill tool with x" convention.
- 1.3.1: `ask-matt` routing fix (diagnosing-bugs → retro, not improve-codebase-architecture).

## Appendix B — addyosmani/agent-skills 0.6.12, per skill

| Upstream skill | Maps to ours | Verdict |
|---|---|---|
| using-agent-skills | dev-workflow | We lack the shared operating rules (theme 16) |
| interview-me | grill-me, spec-from-idea | We lack hypothesis/confidence, Q/GUESS, stop test (theme 3) |
| idea-refine | spec-from-idea step 3 | Divergent ideation + assumption audit; optional |
| spec-driven-development | spec-from-idea | We lack Assumptions, Boundaries, Commands, living spec (theme 3) |
| constraint-driven-development (+ floor-guard) | engineering-standards (partly) | We lack a written project bar and a mechanical guard (theme 10) |
| planning-and-task-breakdown | plan-from-spec | We lack sizing, risk-first, checkpoints, never-overwrite (theme 4) |
| incremental-implementation | implement | We lack NOTICED BUT NOT TOUCHING, tripwire, rollback rules (theme 6) |
| test-driven-development | test-driven-development | We lack stack discovery, double ladder, sub-agent repro; DAMP conflicts with our DRY |
| context-engineering | handoff, writing-for-agents | Restartable session boundaries, trust levels, context budget |
| source-driven-development | — | New-skill candidate (theme 14) |
| doubt-driven-development | — | New-skill candidate (theme 14) |
| debugging-and-error-recovery | debug-systematically | Stop-the-line, non-repro tree, untrusted error output (theme 1) |
| code-review-and-quality | review-code | Severity, mutation check, sizing, perf (theme 2) |
| code-simplification | engineering-standards (preventive only) | New-skill candidate (theme 14) |
| api-and-interface-design | codebase-architecture, engineering-standards | Hyrum's Law, error consistency, idempotency (theme 12) |
| git-workflow-and-versioning | engineering-standards, finish-branch | Didn't-touch summary, semver/changelog rules |
| documentation-and-adrs | — | Theme 13 |
| deprecation-and-migration | engineering-standards (backward compat) | Expand/contract with a tested down path; "destructive last and alone" |
| security-and-hardening | engineering-standards | STRIDE first; Always / Ask First / Never tiers |
| shipping-and-launch | finish-branch | Mostly out of scope; rollback plan is portable. "Acknowledged risks" and "rollback plan is mandatory before any GO" are in `.claude/commands/ship.md:52,70`, not this skill *(corrected 2026-10-22)* |
| frontend-ui, browser-testing, performance, observability, ci-cd | — | Tier 3 |

Infrastructure:
- **Evals**: theme 9. Plugin evals registered via `"experimental": {"evals": "evals/plugin"}` in
  `plugin.json`; graders are `tool_used` (did it fire, unscored), `regex`, and `llm` rubrics.
- **Hooks**: none registered by the plugin. `session-start.sh` (inject the router) is deliberately
  unwired on Claude Code and Codex; WebFetch cache and simplify-ignore hooks are opt-in.
- **Personas** (`agents/`): code-reviewer, test-engineer, security-auditor, web-performance-auditor.
  Rule: the user or a slash command orchestrates; "personas do not invoke personas"; max depth 1.
- **Skill anatomy**: required Overview, When to Use, Common Rationalizations, Red Flags,
  Verification; descriptions put "what" first, then "Use when"; 500-line cap.
- **docs/comparison.md**: compares itself with Superpowers and mattpocock/skills; advises taking
  individual skills from other packs, never running two routers at once.

---

## Decisions for review

Decided 2026-10-12. `[x]` = accepted, `[-]` = rejected / deferred. Each accepted line gets
`— done <sha>` as it lands, so this list is the tracker for what is left.

**Tier 1**
- [x] 1. debug-systematically: feedback-loop-first + stop-the-line + untrusted error output + redact — done 32703ae, 536feb6
- [x] 2. review-code: scope creep, spec discovery, fixed point, severity, mutation check, smells — done d4aa33c, 31278a8
- [x] 3a. Interview: recommendation/guess per question, hypothesis/confidence, stop test — done 3793d64, 31278a8
- [x] 3b. Spec template: Assumptions, Boundaries, Commands, living spec, testing seams — done 3793d64
- [x] 4. plan-from-spec: expand–contract, prefactor, sizing, risk-first, never overwrite — done c5cab61
- [x] 5. test-driven-development: tautological + horizontal anti-patterns, mock at boundaries, stack discovery — done 42edd5c
- [x] 6. implement / finish-branch: NOTICED BUT NOT TOUCHING, PR template (Evidence, Merge Danger) — done 42edd5c, c2bb5c5
- [x] 7. handoff: redact, reference-don't-duplicate, working-tree + verification + approvals; phase-boundary tree — done a8dafb4
- [x] 8. "Call the Skill tool with x" sweep — done efec46f (plus the call sites in each skill's own commit)

**Tier 2**
- [x] 9. Evals: **plugin evals only** this pass; trigger/collision eval, CI eval step and behavioral tier deferred. Was: plugin evals → trigger/collision eval + CI → behavioral/pressure cases — done 31278a8, 536feb6
- [x] 10. Floor-guard script (± CONSTRAINTS.md) — done d4aa33c
- [x] 11. **Both sections** (Rationalizations + Red Flags + Verification), despite M's negation counterpoint. Was: Rationalizations + Verification sections, enforced by validate.py — done efec46f (sections added in 3793d64, 42edd5c, d4aa33c, 32703ae)
- [x] 12. codebase-architecture: deletion test, adapter rule, dependency categories, design it twice — done 103797a
- [x] 13. GLOSSARY.md + ADRs — done 103797a
- [x] 14. **All four** new skills, shipped as draft. Was: New skills: doubt-check / retro / simplify / source-driven (pick any) — done be375fd — `simplify` shipped as `simplify-code` (name clash)
- [-] 15. Deferred to its own spec: see [tickets proposal](2026-10-12-tickets-and-parallel-implement.md). Was: Autonomous or parallel implement mode
- [x] 16. dev-workflow shared operating rules + trust levels — done a8dafb4
- [x] 17. writing-for-agents deepening — done efec46f

**Conflicts** (accept = take the recommendation in §3)
- [x] Keep resolve-merge-conflicts — done no change needed
- [x] Keep refactor inside the TDD loop — done no change needed
- [x] Keep one-question-at-a-time — done no change needed; guesses added in 3793d64
- [x] Keep "never test manually" — done no change needed
- [x] Add DAMP test exemption to engineering-standards DRY — done d4aa33c
- [x] Skip user/model-invoked split, SessionStart router, em-dash ban — done recorded in docs/out-of-scope.md, 1249adc

**Hygiene**
- [x] CHANGELOG.md — done 1249adc
- [x] CI workflow — done 1249adc
- [x] Rejected-ideas record (`.out-of-scope/` or ledger) — done 1249adc (`docs/out-of-scope.md`)

## Addendum, 2026-10-13: over-engineering in specs and plans

Re-read agent-skills 0.6.12 for anything that keeps specs and plans small (PR #7).

| Idea | Source | Outcome |
|---|---|---|
| "What is the simplest thing that could work?"; three similar lines beat a premature abstraction; no abstraction before the third use | `incremental-implementation` Rule 0 | Taken: minimal approach in `spec-from-idea`, third-copy rule in `engineering-standards` |
| Over-built vs simple examples (event bus for one notification, factory for two components, form builder for three forms) | `incremental-implementation` | Taken: table in `engineering-standards` Necessity |
| "Would a staff engineer say 'why didn't you just…'?" | `incremental-implementation` | Taken: `engineering-standards`, `spec-from-idea` Verification |
| "Not Doing (and Why)" list, naming tempting cuts | `idea-refine` | Taken: Non-Goals carry a reason and list tempting cuts |
| No performance work without evidence of a problem | `performance-optimization` | Taken: `spec-from-idea` rationalization row |
| "Code is a liability" | `deprecation-and-migration` | Already covered by the "unused flexibility" row |
| MVP: one job, time-box, "if it's not embarrassing you over-built" | `idea-refine/refinement-criteria.md` | Not taken: product scoping, not engineering design. Revisit if an idea-stage skill is added |
| Phase 0 capability map for bundled requests | `spec-driven-development` | Not taken here: it splits big requests, the opposite problem |

## Addendum, 2026-10-22: re-check against source

A line-by-line re-check of A 0.6.12 and M v1.3.1, plus what each upstream added since (A 0.6.13,
M main at 47 commits past v1.3.1). The rows above marked *(corrected 2026-10-22)* fix the
research's own misreads. The tables below compare our skills with upstream. They are the
checklist for re-reviewing the 2.0 skills.

Action: **fix** = our skill should change; **decide** = a real choice for the owner; **skip** =
noted, no change. Rows marked *unverified* came from a subagent and were not re-read at the line.

Upstream paths: `dd` = A `skills/doubt-driven-development/SKILL.md`, `cr` = A
`skills/code-review-and-quality/SKILL.md`, `fg` = A `skills/floor-guard/SKILL.md`, `diag` = M
`skills/diagnosing-bugs/SKILL.md`, `pb` = M `skills/dev-workflow/PHASE-BOUNDARIES.md`. Ours are under
`skills/<name>/SKILL.md` unless named.

### B. Where our skills drifted from upstream

**High**

| Item | Upstream | Ours | Action |
|---|---|---|---|
| doubt-check sends the claim to the doubter. Upstream: "Do NOT pass the CLAIM" | `dd:106` | `doubt-check:38-39, 67` | fix |
| doubt-check theatre rule is inverted: ours stops after 2 empty cycles and proceeds; upstream calls it theatre when substantive findings are all dismissed, and escalates | `dd:185-191, 215` | `doubt-check:45-47, 70` | fix |
| doubt-check reconcile has only accept / refute; upstream has 4 classes, including "valid trade-off, documented" | `dd:172-177` | `doubt-check:42-44` | fix |
| doubt-check offers cross-model only when high-risk and contested; upstream offers it every interactive cycle, and needs explicit authorization for an external CLI | `dd:116, 124, 164` | `doubt-check:49-52` | decide |
| doubt-check has no "cannot run inside a subagent" caveat | `dd:44-47` | none | fix |
| doubt-check skip clause ("decisions already covered by an approved spec") conflicts with its own trigger "a claim that a criterion is met" | n/a | `doubt-check:25, 27-28` | fix |
| retro routes judgement to `CLAUDE.md` first, and its example row uses `CLAUDE.md`. Upstream: coding standards the reviewer enforces; `CLAUDE.md` "incredibly sparingly" | M `retro:19, 35, 41` | `retro:38-39, 53-54` | fix |
| retro "no guardrail" is per item; upstream's is repo-level (no pre-commit, no CI), and an existing but unwired check is the finding | M `retro:18` | `retro:41-42` | fix |
| retro covers 2 of upstream's 7 areas, and doesn't order by severity | M `retro:17-25` | `retro` Process | decide |
| dev-workflow phase table: "Compact — context is full mid-phase" and "Subagent — a side task whose result is small" contradict upstream. Compact is not the first reach and never mid-phase; subagent = AFK-able work; continue = the next phase needs this context as a primary source | `pb:5, 21, 23, 36, 38-40` | `dev-workflow:78-86` | fix |
| review-code runs before commit, but diffs HEAD against merge-base, so uncommitted work is unseen | M `docs/engineering/code-review.md:74-76` | `review-code:20, 41-43` | fix |
| review-code mutation check doesn't say to restore the file from a copy or to name the missing test case | `cr:164` | `review-code:58-62` | fix |
| floor guard skips `*.md`, so `CONSTRAINTS.md` threshold, rule and exception changes go unseen | `fg:97, 140-163` | `floor_guard.py:81, 203-204` | fix |
| floor guard STUB misses empty `catch {}` and `TODO`; suppressions miss `gitleaks:allow`, `Stryker disable`, `biome-ignore` | `fg:89` | `floor_guard.py:51-55` | fix |
| implement commits, then writes `Status: done <sha>` into the plan, leaving the tree dirty. A stages the status update in the same commit | A `commands/build.md:35` | `implement:73-79` | fix |
| implement has no clean-baseline check before starting | A `commands/build.md:32` | `implement:34-38` | fix |
| plan-from-spec has no plan-approval gate before implementing | A `planning-and-task-breakdown:253`; M `to-tickets:56` | `plan-from-spec` | fix |
| writing-for-agents has no "leading words" rule | M `writing-for-agents:61-72` | none | fix |
| writing-for-agents says to cut cognitive load; upstream: "Not a cost to minimise" | M `writing-for-agents:25` | `writing-for-agents:44-47` | decide |

**Medium**

| Item | Upstream | Ours | Action |
|---|---|---|---|
| debug-systematically: hypotheses carry no falsifiable prediction | `diag:92-96` | `debug-systematically` | fix |
| debug-systematically: no re-run on the original, un-minimised scenario | `diag:128` | `debug-systematically` | fix |
| debug-systematically: no shallow-seam criterion, no AFK escape, no "can't build a loop" escalation | `diag:55, 98, 118` | `debug-systematically` | fix |
| debug-systematically: missing red flags "the failing test is probably wrong" and "it works now" | A `debugging-and-error-recovery` red flags | `debug-systematically` | fix |
| tdd: full suite not run before done; ad-hoc path doesn't confirm the seam; call-count and side-channel red flags missing | A `test-driven-development`; M `tdd` | `tdd` | fix |
| simplify-code: no "scope to what changed", "separate PR", "follow project conventions", "don't over-simplify", "don't weaken error handling" | A `code-simplification:44-59, 92-103, 159, 185, 314, 329` | `simplify-code` | fix |
| source-driven: no "ask when the version is ambiguous", no UNVERIFIED when docs are silent, no outbound-endpoint rule, no citation per pattern | A `source-driven-development:61, 114, 123, 143` | `source-driven` | fix |
| source-driven skip clause "copy a local pattern" lets an unverified local pattern through | n/a | `source-driven:25-26` | decide |
| spec-from-idea: no non-interactive guard; the stop test has no exit when the interview fails | A `interview-me:36, 140, 218` | `spec-from-idea` | fix |
| review-code: doesn't skip what tooling already enforces | M `code-review:41, 64` | `review-code` Step 7 | fix |
| review-code: smells not scoped to the diff with a cited hunk; no size exemption for deletions; no deferral path; no presumptive blockers | `cr:398`; M `code-review` | `review-code` | decide |
| review-code: "more than one new dependency is a finding" is stricter than upstream, which limits upgrades, not additions | `cr:285-297` | `review-code:134-135` | decide |
| validate.py discipline-section check doesn't strip fenced code blocks, so a heading inside a code sample counts | n/a | `scripts/validate.py` | fix |
| *Unverified:* 8 prose hand-offs remain where a Skill-tool call is meant | n/a | several | check |
| *Unverified:* domain-modeling batching rule and 5-section ADR differ from upstream | M `domain-modeling` | `domain-modeling` | check |
| *Unverified:* handoff names no location and no re-verify step | M `handoff` | `handoff` | check |
| *Unverified:* idempotency rules from api-and-interface-design were dropped | A `api-and-interface-design:156-215` | none | check |

**Deliberate, no action:** red-green-refactor kept; one question at a time (reason in
`docs/out-of-scope.md:16`); the "approve when health improves" gate; both rationalization and
mistake sections; retro model-invoked; simplify-code's characterization tests and its
exported-symbol ask (both go beyond upstream).

### C. The dispatch proposal

These apply to [tickets-and-parallel-implement](2026-10-12-tickets-and-parallel-implement.md)
(R2) and to the spec built from it.

| Item | Upstream | R2 | Action |
|---|---|---|---|
| R2 never engages A's anti-pattern C: a sequential orchestrator that paraphrases. "Each hand-off summarizes context — accumulated drift", doubles token cost, "Loses the human checkpoints". Also "Sequential slash commands run by user" as the preferred shape | A `references/orchestration-patterns.md:316-326, 353` | whole proposal | decide |
| A subagent can't spawn subagents, so an implementer subagent can't run `review-code` subagents or `doubt-check`. A's route is `skills:` frontmatter on a plugin agent, which ignores `hooks`, `mcpServers` and `permissionMode` | A `orchestration-patterns.md:164`; `dd:44-47` | not addressed | fix |
| The "what's missing" table is stale: context-window fit, size and durable status already exist | ours `plan-from-spec:62, 120, 123` | `:53-61` | fix |
| "Tests green" baseline credited to `/build`; `/build` checks `git status --porcelain` | A `commands/build.md:32` | `:96` | fix |
| Trust levels credited to `using-agent-skills`; they are in `context-engineering` | A `context-engineering:98-103` | `:101` | fix |
| Doubt rounds misread (see the corrected doubt-check row above) | `dd:185-215` | `:104` | fix |
| Stop rule narrowed to unfixable failures; `/build` also stops on high-risk changes | A `commands/build.md:39` | `:107` | fix |
| Depth limit credited to M; M has no depth rule | n/a | `:109` | fix |
| No per-unit regression and build step between units | A `commands/build.md:35` | not in R2 | fix |
| A reviewer built from a persona file gives balanced verdicts | A `agents/code-reviewer.md:64, 81` | reviewer subagent | decide |
| Model choice "belongs to the harness"; R2's sonnet/opus tiers deviate and don't say so | A `context-engineering:137` | tier table | decide |
| Since v1.3.1, M runs both review sub-agents "together, in the foreground, and aggregate the reports they return" | M `code-review/SKILL.md:60` | reviewer step | decide |
| Since v1.3.1, M puts recursion guards out of scope: "The harness should be responsible" | M `.out-of-scope/subagent-recursion.md:3-7` | depth rule | skip |
| Since 0.6.12, A runs `/review` and `/test` in the main session, not a subagent | A `docs/agents.md:39` | reviewer step | decide |
| Since v1.3.1, M `implement` fetches the ticket and states its title first | M `implement:9` | unit start | fix |

### D. Small upstream additions worth taking

| Item | Upstream | Ours | Action |
|---|---|---|---|
| Word each question so "yes" accepts the recommended answer | M `grilling:24` | `grill-me`, `spec-from-idea` | fix |
| Give each test seam a one-line note: what it catches, what it misses | M `tdd:24` | `tdd`, `spec-from-idea` Testing Seams | fix |
| Diff against a pristine copy to prove a mutation landed | M `diagnosing-bugs:125` | `review-code` mutation check | fix |
| Pasting the trigger clause inline raised TDD firing from 6/24 to 19/24, but test-before-fix held in 2 of 4 runs with the plugin and 0 of 3 without. Firing is not following: evals should check order, not only the trigger | A `evals/README.md:55` | `evals/` | fix |
| Compose existing skills before adding a new one | M `.out-of-scope/new-skills.md:9` | `CLAUDE.md` | decide |
| No `AskUserQuestion` in grilling | M `.out-of-scope/native-question-tool.md` | `grill-me` | decide |
| A new rule needs an observed failure behind it | M `SCOPE.md:9` | `CLAUDE.md` | decide |
