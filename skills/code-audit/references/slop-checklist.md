# AI-code slop checklist

Patterns coding agents tend to leave behind that `engineering-standards`
doesn't already name. Lens 2 applies every row; Lens 1's rules for
swallowed errors, mocks, logging and secrets stay in
`engineering-standards` and aren't repeated here.

Each row still needs a concrete case before it becomes a finding.

| Pattern | Why it hurts | How to spot it |
|---|---|---|
| **Invented API**: a parameter, method, module or CLI flag the installed version doesn't have (`json.dumps(obj, sort=True)`; the real one is `sort_keys`) | Fails only when that line runs, often on an untested error path | For each unfamiliar call, check the installed version: run it with `python3 -B -c`, read the package source, or call the Skill tool with `source-driven` |
| **Missing target**: an import, file path, env var or config key that nothing in the repo defines | Breaks at import or at the first request that reaches it | `git grep` the name; for paths, `test -e`; for env vars, grep the deploy and config files |
| **Declared, never used dependency**: in `requirements*.txt`, `pyproject.toml`, `package.json` or `go.mod`, with no import anywhere | Install time, attack surface and upgrade work for nothing | For each declared package, `git grep` its import name (it can differ from the package name: `PyYAML` → `yaml`) |
| **Placeholder left in**: a function returning a fixed value, `pass` or `...` bodies, `# TODO: implement`, sample or fake data in a non-test path | The feature looks done and silently isn't | `git grep -nE 'TODO|FIXME|NotImplemented|placeholder|dummy|fake_|sample_'` outside tests, then read each hit |
| **Silent default for required data**: `.get(key, {})`, `or []`, `?? ""` on a value the code can't work without | A missing field turns into wrong output instead of an error | Read each default on payloads, config and database rows; ask what happens when the key is absent |
| **Test that can't fail**: no assertion, `assert True`, asserting a value copied from the current output, or catching the exception the test should expect | Green suite, untested code | Read each test of risky logic; break the code it covers in your head (or with `python3 -B`) and ask whether the test would go red |
| **Versioned copy**: `*_v2`, `*_new`, `*_old`, `*_backup`, `*copy*` beside the original, both still imported | Two live versions of one rule drift apart | `git ls-files | rg -i '_(v[0-9]+|new|old|backup)\b|copy'`, then grep both names for callers |
| **Second way to do one thing**: a file using its own HTTP client, logger, date library, config loader or error type when the repo already has one | Every reader has to learn both; fixes land in one and miss the other | Note the repo's choice for each concern from the Map step; grep for the others (`requests` vs `httpx`, `print` vs the logger) |
| **History comment**: "now we…", "updated to fix…", "changed from X to Y", "as requested" | Describes the edit, not the code; wrong after the next change | `git grep -niE '# *(now|updated|changed|fixed|as requested|new:)'` and the same for `//` |
| **README that lies**: a documented command, flag, endpoint or feature that doesn't exist | New users follow it and fail | Try each command in the README with `--help`, or grep for each endpoint and flag it names |
