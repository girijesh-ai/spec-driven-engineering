# Retry transient failures in the metadata-sync HTTP client

> Illustrative spec — the artifact `spec-from-idea` produces for the
> "architectural" tier. In a real run this lives at
> `docs/specs/2026-09-02-metadata-sync-retry.md`. See
> [walkthrough.md](walkthrough.md) for how the rest of the spine consumes it.

## Context

The nightly `metadata-sync` job calls an upstream catalog service over HTTP.
Roughly 3% of runs fail on transient upstream errors (502/503/504 and
connection timeouts); each failure pages on-call and is resolved by a manual
re-run that then succeeds. The transport has no retry, so a single upstream
blip fails the whole job.

## Goals

- Automatically retry transient HTTP failures so a single upstream blip does
  not fail the nightly job.
- Keep permanent failures (4xx, and non-idempotent requests) failing fast —
  retrying them wastes time and can double-apply writes.
- No change to the job's public entrypoint or to any existing caller.

## Non-Goals

- No circuit breaker or global rate limiter (separate concern, separate spec).
- No retry of non-idempotent methods by default (POST/PATCH) — deferred.
- No change to authentication, logging format, or the client's configuration
  surface beyond an optional `max_retries`.

## Approach

Wrap the existing `HttpClient.request` with a bounded exponential-backoff
retry, applied only to idempotent methods (GET/HEAD/PUT/DELETE) and only for a
fixed transient-status set plus connection timeouts. Backoff is
`0.5s * 2**attempt` with ±20% jitter, capped at `max_retries` (default 3).
Chosen over a third-party retry library because the transient set and
idempotency policy are project-specific and the logic is ~30 lines; and over
per-caller retry because callers should not each reimplement it.

## Success Criteria & Evals

Measurable, pass/fail. `review-code` checks the implementation against exactly
this list.

- **SC1** — A request returning `503, 503, 200` succeeds, and the transport is
  called exactly 3 times. *Eval:* unit test stubs the transport with
  `[503, 503, 200]`; assert result status is 200 and `transport.call_count == 3`.
- **SC2** — A `400` is not retried. *Eval:* stub `[400]`; assert
  `transport.call_count == 1` and the 400 is surfaced to the caller.
- **SC3** — Backoff sleeps are `0.5s, 1s, 2s`, each ±20%, and total added sleep
  on the max-retry path is `< 4s`. *Eval:* patch the sleep function; assert the
  three recorded delays fall in `[0.4,0.6], [0.8,1.2], [1.6,2.4]` and sum `< 4`.
- **SC4** — After retries are exhausted (`[503, 503, 503, 503]`, `max_retries=3`)
  the original transport error propagates — it is not swallowed. *Eval:* stub
  four `503`s; assert the transport error is raised and `transport.call_count == 4`.
- **SC5** — A non-idempotent `POST` returning `503` is not retried by default.
  *Eval:* stub `POST [503]`; assert `transport.call_count == 1`.
- **SC6** — The job entrypoint `sync_metadata()` signature is unchanged and all
  existing caller tests pass unmodified. *Eval:* `git diff` shows no change to
  `sync_metadata`'s signature; the existing `tests/test_sync.py` suite passes
  without edits.

## Open Questions

- Should POST retries be opt-in via an idempotency key? Deferred — see
  Non-Goals; revisit only if a caller actually needs it.
