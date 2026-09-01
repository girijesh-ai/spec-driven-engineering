# Python appendix to engineering-standards

Concrete conventions for Python codebases. The principles in `SKILL.md`
apply regardless of language; this file is how they translate to Python
specifically.

## Data

```python
from dataclasses import dataclass

@dataclass
class ScoreResult:
    score: float
    reason: str
```

Use `@dataclass` or `TypedDict` for structured data crossing a function
boundary — never a raw `dict` as a public return type. Type-annotate every
public function signature. Use `from __future__ import annotations` for
forward references.

## Error handling

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = risky_call()
except SpecificError:
    logger.exception("risky_call failed", extra={"input_id": input_id})
    raise
```

Use `contextlib.suppress` or explicit `try/finally` for cleanup — never a
bare `except: pass`.

## Logging

```python
logger = logging.getLogger(__name__)
logger.info("Probe complete", extra={"score": 0.12, "n_probes": 400})
```

Always `__name__`, never a hardcoded string. Structured `extra=` payload,
not string-formatted values baked into the message.

## Filesystem

Prefer `pathlib.Path` over `os.path` for filesystem operations.

## Imports

stdlib, then third-party, then internal — separated by blank lines,
alphabetical within each group.

## Deprecation over deletion

```python
import warnings

def old_function_name(...):
    warnings.warn(
        "old_function_name is deprecated; use new_function_name instead. "
        "Will be removed in the next major release.",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_function_name(...)
```

Keep the wrapper for at least one full release cycle. State the migration
path in the warning itself.

## Testing

Prefer `pytest` over `unittest`. Fixtures over `setUp`/`tearDown`. Test file
naming: `test_<module_name>.py`. Mark tests needing external services
(`@pytest.mark.integration`, `@pytest.mark.e2e`) and exclude them from the
default run.

## Performance

- Don't optimize prematurely — write clear code, profile before
  optimizing.
- Prefer generators/`itertools` over materializing large lists.
- Run independent I/O (HTTP, DB, file) concurrently (`asyncio`,
  `ThreadPoolExecutor`) rather than sequentially when it's actually
  independent.
