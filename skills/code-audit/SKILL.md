---
name: code-audit
description: Use when inheriting a repo, before trusting a large or AI-written PR or branch, or when asked to audit a codebase, folder or PR for bugs, over-engineering, AI-code slop or structural problems — a read-only, ranked report with a fix for each finding.
---

# code-audit
Status: draft

## Overview

Audits a scope like the senior engineer who just inherited it and will be
paged when it breaks: correct, safe, holds at the expected load, tested,
lean, well-structured. Three subagents each look through one **lens**; the
main session confirms every finding in the code and writes one numbered
report. It changes no file. The finding shape and the check-before-report
rules adapt `ponytail-audit` (DietrichGebert/ponytail, MIT).

Not `review-code`: that skill gates one diff against its spec and returns
READY or NEEDS FIXES. This one has no spec check and no ship verdict. Run
both when you want both.

## When to use

- Inheriting a repo or a folder nobody on the team wrote
- A large or AI-written PR or branch, before trusting it
- "Audit this", "what can I delete", "is this over-engineered"

## Process

1. **Pin the scope.** The user names it: a repo, a folder, a branch, or a
   PR (number or link). Nothing named: the whole repo.
   - **PR or branch:** get the diff (`gh pr diff <n>`, or
     `git diff <base>...<branch>`). The scope is the diff plus the code it
     touches: callers of every changed function (grep them), the functions
     it calls, and their tests. Read other branches with `git show
     <ref>:<path>` and `git log`; stay on the checked-out branch.
   - **Repo or folder:** the main flows end to end.

   **Record** `git status --porcelain` now. Done when you can state the
   scope in one sentence.

2. **Map.** Read the README, build and deploy config, the dependency list,
   the entry points (main, routes, handlers, jobs, CLI commands) and the
   tests. Trace where data comes in, what is stored, what goes out. Write a
   **Map note** of at most 15 lines: what the code does, the expected load
   (one person running a script, or many users and processes at once; say
   which you assumed), the main flows with paths, and the risky areas
   (auth, money, data writes, concurrency, shared interfaces). Big scope:
   name the parts you will go deep on and the parts you won't read.

3. **Pick each lens's model** from the Map note:

   | The scope contains | Lens on `opus` |
   |---|---|
   | auth, money, data writes or migrations, concurrency (locks, jobs, shared state) | Lens 1 |
   | an interface imported by 2+ services or packages | Lens 3 |
   | none of the above | none |

   Every other lens gets no `model`, so it runs on the session model.
   Lens 2 is never pinned. Write one line per lens, with the reason:
   `Lens 1: opus (scope writes orders to SQLite in app/storage/)`. These
   lines open the report. On OpenCode, which can't pick a model per call,
   say so once and run every lens on the session model.

4. **Dispatch the three lenses in one message**, one Agent call each, with
   `model: "opus"` only where step 3 says so. Each brief holds the Map
   note, the scope (paths, or the diff range), the lens's row below
   (the lens makes its own Skill calls), and ends: "Read only: use Read,
   Grep, Glob and read-only Bash (git log, git diff, git grep, git show). Run code
   only in a form that writes nothing (`python3 -B`). Change no file.
   Return candidate findings, each
   with `path:line`, the concrete case (this input or situation leads to
   this wrong result), and the smallest fix. Return none rather than a
   finding without a concrete case."

   | Lens | Checks |
   |---|---|
   | **1. Correctness** | Call the Skill tool with `engineering-standards` and apply Error handling, Security and Testing. Call the Skill tool with `review-code` and apply only its Step 4 (caller impact) and Step 5 (resource and failure-path audit); give no verdict. Also: wrong results and missed edge cases (empty, zero, last item, rounding, time zones); the same rule applied differently in two places; scale at the expected load (check-then-write races, a query per item, lists that only grow, per-process state that must be shared); risky logic (a branch, a parser, money, security, a data write) with no test that fails when it breaks |
   | **2. Lean and slop** | Call the Skill tool with `engineering-standards` and apply Necessity and simplicity, DRY and SOLID. Also: delete (dead code, unused options and config, speculative features); reuse (two helpers doing one job: name the one to keep); stdlib (a dependency or hand-written code doing what the standard library does); yagni (an interface with one implementation, a wrapper that only forwards calls); merge (near-copies that must change together); split (one function doing unrelated jobs, split by job, never by line count). Then read `references/slop-checklist.md` (pass its full path) and apply every row |
   | **3. Structure** | Call the Skill tool with `codebase-architecture` and apply its Core checks to the scope's main modules: depth, interface width, layer direction, information hiding, the deletion test. Name the layers you inferred if the project documents none |

   Done when all three have returned.

5. **Confirm every candidate yourself.** A lens's finding is a lead until
   you have read the lines that prove it. For each one:
   - **Re-read** the cited lines and check the concrete case holds: the
     caller exists, the value can really be empty, the path really runs.
   - **Grep the whole tree** before calling code unused, including tests,
     fixtures, config, and names built as strings or looked up
     dynamically (`getattr`, `globals()[...]`, registries, reflection).
   - **Call the Skill tool with `source-driven`** when the finding depends
     on a library's exact behaviour (a parameter, a default, a version
     change), and keep it only if the docs for the installed version back
     it.
   - **Merge** duplicates across lenses into one finding.

   Drop what you can't confirm. Keep at most 20, and count the smaller
   ones you cut for the report's `Cut:` line. Done when every kept finding has a re-read line behind it.

6. **Write the report** in plain words: short sentences, a technical term
   glossed the first time. Use this shape:

   ```markdown
   Lens 1: <opus|session model> (<reason>) · Lens 2: session model · Lens 3: <opus|session model> (<reason>)

   **What this <repo|change> does:** 2-3 sentences. Load assumed: <...>.

   ### Must fix        (bug, security hole, data loss, breaks at the expected load)
   ### Should fix      (risky code with no test, real slowness, duplication, mixed jobs, code that shouldn't exist, a structural problem)
   ### Nice to have    (small speed-ups, shorter forms)

   1. **Orders land on the wrong day** (`billing/close_day.py:40-52`)
      - **What this is:** At midnight this job bills all orders of that day.
      - **Problem:** It takes "today" from the server clock in UTC, so an order at 00:30 in Berlin bills a day early.
      - **Fix:** `datetime.now(ZoneInfo("Europe/Berlin")).date()`. One line.
      - **If we skip it:** Late orders show the wrong date; accounting fixes them by hand.

   Verdict: <healthy, or what to fix first>
   Lean: -<N> lines, -<M> dependencies possible.     (only when lean findings exist)
   Cut: <N> smaller findings left out.               (only when N > 0)
   Not checked: <parts not read or not run>
   ```

   The Map note stays in the briefs; the report's opening lines carry
   what the reader needs from it.

   Number findings across all groups so the user can say "fix 2 and 5".
   Skip empty groups. Each of the four parts is one or two sentences.
   Prefer a fix that deletes code; never propose a layer, framework or
   config the problem doesn't need. Nothing found: the lens lines, `What
   this ... does`, then `Healthy. Nothing to fix.` and one line on what you
   checked.

7. **Prove it was read-only.** Run `git status --porcelain` again; it
   matches step 1's output. Then end with: "Say which numbers to fix."
   Write the report to `docs/audits/YYYY-MM-DD-<scope>.md` only when the
   user asks; it's the one file this skill may create.

## Fixing what the user picks

Route each picked finding: a behaviour change or a bug goes to the Skill
tool with `implement` (test-first, reviewed); same behaviour with less
code goes to the Skill tool with `simplify-code`. The audit report is the
input; the audit itself never edits.

## Common mistakes

| Mistake | Fix |
|---|---|
| Reporting a lens's finding without reading the line | Re-read it and state the concrete case; a lead isn't a finding |
| Calling code dead after one grep for its name | Grep for string and dynamic lookups too; a registry keeps code alive |
| A finding with "consider" and no failure | Name the input that breaks it, or drop it |
| Pinning `opus` on every lens "to be safe" | Pin only where step 3's table says so, and print the reason |
| A finding about style or taste | Drop it; findings name a wrong result, a risk, a cost or code that shouldn't exist |
| Giving READY / NEEDS FIXES | That's `review-code`; this report ends with `Verdict:` and `Not checked:` |
| Fixing a finding mid-audit | Finish the report; fixes go through `implement` or `simplify-code` |

## Next

The user picks findings → `implement` or `simplify-code`, per the
routing above. Before merging any of those fixes, `review-code`.
