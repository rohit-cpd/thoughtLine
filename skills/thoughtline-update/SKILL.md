---
name: thoughtline-update
description: >-
  Updates an installed copy of the ThoughtLine skills to the latest version on GitHub, the
  matching way for how it was installed — the plugin manager's own update for a plugin install,
  `git pull` for a symlinked clone, a backed-up re-copy for copied folders. Name it to "update
  thoughtline", "pull the latest skills", "check for skill updates". Reports first and changes
  nothing until you confirm. Not for starting a project (`project-start`), and never touches a
  project's own files — only skill install folders.
disable-model-invocation: true
---

# ThoughtLine Update

Brings an installed copy of these skills up to date with
[github.com/rohit-cpd/thoughtLine](https://github.com/rohit-cpd/thoughtLine). The work is done by
`scripts/thoughtline_update.py`, bundled with this skill; this file is how to run it safely.

## Write scope

**Runs only when the user names it.** It carries `disable-model-invocation: true` for the same
reason the lifecycle skills do: it rewrites files, so inference is the wrong trigger. "Update" said
in passing is not an instruction to run this.

Touches **ThoughtLine's own skill folders only**, inside the skill directories listed below. Never
another skill sharing the same directory, never a project's files, never `Notes/`,
`Project_Intent/`, `Project_Context/` or `Archive/`. The project's agent instructions may narrow
this scope; nothing widens it.

**Nothing is deleted.** A replaced or retired skill folder is moved to
`~/.thoughtline/backups/<timestamp>/` — outside every skill directory, because a harness that scans
nested folders would load a backup kept inside one as a duplicate skill.

## How it was installed decides how it updates

| Found | Method | What `--apply` does |
|---|---|---|
| `claude plugin list` shows `thoughtline` | plugin | runs `claude plugin update thoughtline@thoughtline-skills` |
| the skill directory, or a skill folder in it, is a symlink | symlink | `git pull --ff-only` in the clone it points at — **skipped** if that clone has uncommitted changes |
| plain folders | copy | fetches upstream, moves each changed folder to the backup, copies the new one in |

A Copilot plugin install is not detected — update it through Copilot's own plugin commands.
[Unverified which command that is.]

Searched: `~/.claude/skills`, `~/.agents/skills`, `~/.copilot/skills`, `~/.cursor/skills`, and the
same four under the current project (`.claude/skills`, `.agents/skills`, `.github/skills`,
`.cursor/skills`) — each also as `<dir>/thoughtline/skills`, the older skills-directory plugin
layout. A directory counts as an install only if it holds at least one ThoughtLine skill folder.

## Procedure

1. **Locate the script** the way `project-state-brief` locates its validator: this skill's base
   directory if the harness reported one, otherwise

   ```
   find ~/.agents ~/.claude ~/.copilot ~/.cursor .agents .claude .github .cursor -maxdepth 8 \
        -path '*thoughtline-update*' -name thoughtline_update.py 2>/dev/null | head -1
   ```

2. **Dry run first, every time.** `python3 <script>` reports, per install, what would change.
   Exit `0` up to date · `2` updates available · `1` error.
3. **Show the report and ask.** Name every skill that would be added, replaced or moved out, and
   every one flagged as locally modified. Nothing runs past this point without a yes. **A yes does
   not carry over** — if other work happens before it's answered, dry-run again and re-ask;
   upstream may have moved.
4. **Apply.** `python3 <script> --apply`, plus whichever flags the answer called for (below).
5. **Report** what changed and where the backup is, then tell the user to **restart their tool** —
   skills are scanned at startup, so the update is not live in the current session.

## What the report says, and how to change the default

| Line | Meaning | On `--apply` | To change it |
|---|---|---|---|
| `update` | changed upstream, untouched locally | replaced; old folder backed up | — |
| `add` | in upstream, not installed here | added | `--only-installed` — for a partial install, such as only the code skills |
| `locally modified` | edited here since the last update | **kept** | `--overwrite-local` — the edits go to the backup |
| `removed upstream` | installed by an earlier update, gone upstream | moved to the backup | — |
| `retired name` | an old ThoughtLine name, e.g. `research-skill` | **left alone** — reported only | remove it by hand once you've confirmed it is this library's |

**The first update of a copied install can't tell your edits from upstream's.** Spotting a local
edit needs the record the script writes on every apply — `.thoughtline-install.json` in the skill
directory. Before the first apply there's no record, so every difference reads as `update`. That is
why everything replaced is backed up, and why the report says so.

**A partial install stays partial.** Once recorded, a skill that existed upstream but wasn't
installed is treated as deliberately left out and not offered again; only skills new upstream since
the last update are added.

`--ref <tag or branch>` updates to a specific release instead of `main`. `--repo <url>` updates from
a fork.

## Hard rules

- **Dry run before every apply, and ask in between.** The report is the gate.
- **Never touch a folder that isn't a ThoughtLine skill**, even in the same directory — the user's
  other skills live there too.
- **Never delete. Move to the backup.**
- **Never force.** A symlinked clone with uncommitted changes is skipped and reported, never reset;
  a locally modified skill is kept unless the user says otherwise.
- **If the fetch finds no skills, stop.** A wrong repo or ref must not read as "everything was
  removed upstream" — the script refuses on its own, and that refusal is not an error to work
  around.
