# OpenCode

**Status:** stable

How to install and run this catalog on [OpenCode](https://opencode.ai) —
with no dependency on Claude Code. The 16 skills are plain
`skills/<name>/SKILL.md` files; OpenCode reads them natively. All you add
is a config pointer to them plus six thin slash-command wrappers for the
spine.

The spine is unchanged:

```
spec-from-idea -> plan-from-spec -> implement -> review-code -> finish-branch
```

If it's unclear where to start, use `/dev-workflow`.

## Prerequisites

- OpenCode installed (`opencode --version` works). See
  [opencode.ai/docs](https://opencode.ai/docs).
- A configured model (a provider in `~/.config/opencode/opencode.json`,
  or `/connect` in the TUI).
- A clone of this repo somewhere stable. The examples use
  `~/src/spec-driven-engineering` — substitute your own path.

```
git clone https://github.com/girijesh-ai/spec-driven-engineering.git \
  ~/src/spec-driven-engineering
```

## Install

Two config surfaces, independent of each other:

- **Skills** — point `skills.paths` at the clone's `skills/` directory.
  OpenCode scans it recursively for `**/SKILL.md`. No copy, no symlink;
  `git pull` updates it live.
- **Commands** — copy the six wrapper `.md` files into an OpenCode
  `command/` directory. There is no `command.paths` config, so wrappers
  must physically live in a scanned directory. They are tiny and change
  rarely, so a copy is fine.

Pick global (every project on the machine) or per-project.

### Global install (recommended)

**Skills.** Add a `skills` key to your global config at
`~/.config/opencode/opencode.json`. If the file already exists, **merge**
this key in — do not overwrite your existing `model`, `provider`, `mcp`,
etc. Create the file with just this if it doesn't exist:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["~/src/spec-driven-engineering/skills"]
  }
}
```

`skills.paths` accepts `~/` and absolute paths. (If you script the merge,
`jq '.skills = {paths: ["~/src/spec-driven-engineering/skills"]}'` adds
the key without touching the rest.)

**Commands.** Copy the six wrappers into the global command directory:

```
mkdir -p ~/.config/opencode/command
cp ~/src/spec-driven-engineering/.opencode/command/*.md \
  ~/.config/opencode/command/
```

This yields clean names — `/spec-from-idea`, `/plan-from-spec`,
`/implement`, `/review-code`, `/finish-branch`, `/dev-workflow`. (The
command name is the file's path below `command/`, so the wrappers must
sit directly in `command/`, not in a subfolder under it.)

Restart OpenCode. Config is not hot-reloaded.

### Per-project install

Scope the catalog to one project instead of the whole machine.

In that project's `opencode.json` (create it if needed):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["~/src/spec-driven-engineering/skills"]
  }
}
```

Relative paths are resolved from the config file, so a git submodule at
`vendor/spec-driven-engineering` works as
`"paths": ["vendor/spec-driven-engineering/skills"]`.

Then copy the wrappers into the project command directory:

```
mkdir -p .opencode/command
cp ~/src/spec-driven-engineering/.opencode/command/*.md .opencode/command/
```

Restart OpenCode.

### Quick check without installing

To try the catalog without editing any config, just open the clone
itself — its committed `opencode.json` already points `skills.paths` at
`./skills`, and `.opencode/command/` holds the wrappers:

```
cd ~/src/spec-driven-engineering
opencode
```

Type `/` in the TUI; the six spine commands appear. This only works while
your working directory is inside the clone.

## It's working if

Run this from a real project directory (not your bare home directory —
OpenCode's project-local scan keys off the git worktree, so `$HOME` is a
degenerate case):

```
opencode debug skill > /tmp/sk.json
grep -c '"name":' /tmp/sk.json
grep '"name": "spec-from-idea"' /tmp/sk.json
```

**Redirect to a file — do not pipe `opencode debug skill` straight into
`grep`.** The command emits a large JSON blob and can exit before a pipe
is fully drained, so `... | grep -c` reports a truncated, fluctuating
count. Writing to a file first is reliable.

Expected: the first count is large (every skill OpenCode can see), and
the second prints `"name": "spec-from-idea"`. To confirm the catalog is
loading from your clone and not a stale duplicate:

```
opencode debug skill 2>/tmp/dw.log > /tmp/sk.json
grep '"location"' /tmp/sk.json | grep spec-from-idea   # -> your clone's path
grep -c 'duplicate skill name' /tmp/dw.log             # -> 0
```

A non-zero duplicate count means the catalog is wired up more than once
(e.g. a leftover symlink *and* `skills.paths`) — remove one.

In the TUI, type `/` and the six spine commands appear. Or run one
headless: `opencode run --command dev-workflow "..."` should print
`→ Skill "dev-workflow"` and act on it.

A skill that does not show up: check the file is named `SKILL.md`
(uppercase), its frontmatter has `name` + `description`, and it is not
denied in `permission.skill`.

## Use

| You're here | Run |
|---|---|
| Unsure which skill | `/dev-workflow` |
| Idea, nothing written down | `/spec-from-idea $ARGUMENTS` |
| Spec exists, no plan | `/plan-from-spec $ARGUMENTS` |
| Plan exists, writing code | `/implement $ARGUMENTS` |
| About to commit or open a PR | `/review-code` |
| Review returned READY | `/finish-branch` |

Supporting skills (`engineering-standards`, `test-driven-development`,
`domain-modeling`, `codebase-architecture`, `debug-systematically`,
`resolve-merge-conflicts`, `triage-issues`, `grill-me`, `handoff`,
`writing-for-agents`) have no slash command. The agent loads them via
the `skill` tool when a spine skill names them, or when you ask.

`implement` and `review-code` still work without an upstream spec. They
must say so out loud ("no spec/plan found — proceeding ad-hoc" /
"spec axis skipped — no spec found").

Use OpenCode's built-in **Plan** agent (Tab) for `spec-from-idea` /
`plan-from-spec` / `grill-me` if you want a read-only pass first. Switch
back to **Build** before `/implement`.

## Updating

`skills.paths` reads the clone live, so `git pull` in the clone updates
every skill. Restart OpenCode afterwards.

The copied command wrappers are the one thing that doesn't auto-update.
They are stable — six one-line files that just say "load skill X" — so a
release rarely touches them. If one changes, re-copy:

```
cp ~/src/spec-driven-engineering/.opencode/command/*.md \
  ~/.config/opencode/command/
```

## What this is not

OpenCode "plugins" (`opencode.json` → `plugin: [...]`) are JS/TS event
hooks, not skill packs. This catalog is skills + command wrappers + a
config pointer. Do not `opencode plugin install` this repo.

This catalog also ships as a Claude Code plugin — see the root
[README](README.md) `## Install`. Both harnesses read the same `skills/`
directory; neither depends on the other.

## Uninstall

- **Global:** drop the `skills` key from
  `~/.config/opencode/opencode.json`, and
  `rm ~/.config/opencode/command/{spec-from-idea,plan-from-spec,implement,review-code,finish-branch,dev-workflow}.md`.
- **Per-project:** drop the `skills` key from the project's
  `opencode.json` and remove the copied wrappers from
  `.opencode/command/`.

Restart OpenCode.
