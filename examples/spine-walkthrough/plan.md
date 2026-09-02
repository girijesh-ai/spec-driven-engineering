# Plan: Retry transient failures in the metadata-sync HTTP client

> Illustrative plan — the artifact `plan-from-spec` produces. In a real run
> this lives at `docs/plans/2026-09-02-metadata-sync-retry.md`. Every step's
> Verification is traced back to a Success Criterion in [spec.md](spec.md).

## Source spec

[spec.md](spec.md) (in a real run: `docs/specs/2026-09-02-metadata-sync-retry.md`)

## Critical files

- `src/sync/retry.py` — new. Pure backoff/decision helpers (no I/O), so the
  timing and transient/idempotency policy are testable without a network.
- `src/sync/http_client.py` — `HttpClient.request` gains the retry loop; public
  signature unchanged.
- `tests/sync/test_retry.py` — new. Encodes SC1–SC5 as stub-transport tests.
- `tests/test_sync.py` — existing; must pass unmodified (SC6).

## Steps

### 1. Backoff + decision helpers
- Depends on: none
- Touches: `src/sync/retry.py`, `tests/sync/test_retry.py`
- Verification: **SC3** — `backoff_delay(attempt, rng)` returns values in the
  specified jittered ranges and the max-retry path sums `< 4s`. Also unit-covers
  `should_retry(method, status)` for the transient set and idempotency policy
  (this is what SC2/SC5 lean on in later steps).

### 2. Retry loop around the transport
- Depends on: step 1
- Touches: `src/sync/http_client.py`, `tests/sync/test_retry.py`
- Verification: **SC1** (`[503,503,200]` → 200, 3 calls) and **SC5**
  (`POST [503]` → 1 call), via stub-transport tests.

### 3. Fast-fail and error propagation
- Depends on: step 2
- Touches: `src/sync/http_client.py`, `tests/sync/test_retry.py`
- Verification: **SC2** (`[400]` → 1 call, surfaced) and **SC4** (four `503`s,
  `max_retries=3` → error raised, 4 calls).

### 4. Wire into the job, prove callers unaffected
- Depends on: step 3
- Touches: `src/sync/http_client.py` (default `max_retries=3`)
- Verification: **SC6** — `git diff` shows `sync_metadata()`'s signature
  unchanged; `tests/test_sync.py` passes with no edits.

## Reuse

`should_retry` reuses the existing `TRANSIENT_STATUSES` constant already in
`http_client.py` — do not define a second copy (DRY).
