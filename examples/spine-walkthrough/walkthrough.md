# Walkthrough: the spine, end to end

This narrates how [spec.md](spec.md) and [plan.md](plan.md) flow through
`implement`, `review-code`, and `finish-branch`. It is an **illustrative
worked example** — it shows the artifacts and the shape of each stage's
output, not a live upstream run (that's what [../smolagents/](../smolagents/)
is). The point is to make the Success Criteria & Evals thread visible from idea
to landed change.

## 1. spec-from-idea → the spec

`spec-from-idea` classified this as **architectural** (it changes an interface
other code depends on) and produced [spec.md](spec.md). The load-bearing part
is **Success Criteria & Evals**: six pass/fail checks, each one runnable — no
"test manually," no "works correctly." That list is the contract every later
stage is measured against.

## 2. plan-from-spec → the plan

`plan-from-spec` turned the spec into [plan.md](plan.md): four dependency-
ordered steps, each carrying a **Verification** line traced to a specific
criterion. Coverage is explicit — SC3→step 1, SC1/SC5→step 2, SC2/SC4→step 3,
SC6→step 4. A step with no linked criterion would signal that either the step
is unnecessary or the spec is missing a check; here every step maps.

## 3. implement → code, one step at a time

`implement` executes the plan step by step, calling `test-driven-development`
at each seam:

- **Step 1 (Red→Green→Refactor):** write `test_backoff_delay_ranges` first — it
  fails (no `retry.py` yet). Add `backoff_delay`/`should_retry`. Test goes
  green. This step's verification (SC3) is now checkable and passes.
- **Steps 2–3:** the stub-transport tests for SC1, SC5, SC2, SC4 are written
  before the loop exists, watched to fail for the right reason, then made to
  pass with the minimum code.
- **Reuse check:** `should_retry` imports the existing `TRANSIENT_STATUSES`
  constant instead of redefining it (the plan's reuse note).

Before each commit, `implement` runs `review-code` — not just once at the end.

## 4. review-code → the two-axis report

This is the artifact `review-code` produces. **Axis 1 (spec compliance) is
primary**, and it is checked against exactly the spec's list:

```
### Spec compliance (Axis 1)
- SC1 (503,503,200 → 200, 3 calls) ........ met — test_retries_transient
- SC2 (400 not retried) ................... met — test_no_retry_on_4xx
- SC3 (backoff ranges, total < 4s) ........ met — test_backoff_delay_ranges
- SC4 (exhaustion propagates, 4 calls) .... met — test_raises_after_max
- SC5 (POST not retried by default) ....... met — test_no_retry_non_idempotent
- SC6 (entrypoint signature unchanged) .... met — git diff clean; test_sync green

### Standards & architecture (Axis 2)
- retry.py is a deep, pure module (no I/O) — timing/policy testable. Good.
- necessity: bounded ~30-line loop, no speculative config. Good.
- one confirmed nit: jitter used an unseeded global RNG — flagged, fixed to an
  injected `rng` so SC3 is deterministic.

### Verdict
READY — no confirmed issues; every spec criterion met.
```

Because Axis 1 is per-criterion, "done" is not a judgment call — it is the six
evals passing. If a spec were absent, this section would instead read **"Spec
axis skipped — no spec found"** and Axis 2 would still run in full.

## 5. finish-branch → landing it

`finish-branch` confirmed every Success Criterion was met (not "mostly"), then
wrote the commit/PR description from the spec's **Context** and **Goals** (the
"why") and the plan's steps (the "what") — not from memory:

```
Retry transient failures in metadata-sync HTTP client

Nightly metadata-sync failed ~3% of runs on transient upstream 5xx/timeouts,
paging on-call for a manual re-run. Adds bounded exponential-backoff retry for
idempotent methods on a fixed transient-status set; permanent and
non-idempotent failures still fast-fail. Entrypoint unchanged.

Success criteria SC1–SC6 met (see spec). Tests: tests/sync/test_retry.py.
```

## The thread, in one line

Six measurable evals were written **once** in the spec, carried as per-step
verifications in the plan, used as the per-step acceptance bar in `implement`,
and became the primary axis of the review — the same six checks, all the way
through. That thread is what `spec-driven-engineering` exists to keep intact.
