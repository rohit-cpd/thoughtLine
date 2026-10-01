---
name: project-start
description: >-
  Runs once per project: lays down the folders no other skill owns
  (research_repository/, data/, files/, .gitignore, AGENTS.md), then hands off.
  Name it to "start a new project", "scaffold the project", or "add the notes
  system to this repo". Not for starting a new phase inside an existing project —
  that is `phase-context`.
disable-model-invocation: true
---

# Project Start

Runs once, at the beginning of a project — or once when adopting this system into a repo that
already exists. Creates only what no other skill owns, then stops and hands off.

**Never destructive.** This skill creates missing things. It does not move, rename, overwrite or
delete anything already present. If something exists, it is left alone and reported.

## Step 0 — Detect the mode, and confirm

Look at the target directory before writing anything.

| Found | Mode | Behaviour |
|---|---|---|
| Empty, or only a `README`/`.git` | **new** | Create the full skeleton |
| Existing code, or any of the folders below | **adopt** | Create only what is missing; touch nothing else |

**Adopt is the common case** — most people add this system to a repo that already has work in it.
Treat it as the default assumption unless the directory is genuinely bare.

Then show the user exactly what you intend to create, as a list of paths, and get a go-ahead.
Creating structure inside someone's repository is not something to do on inference.

### Guards — stop rather than proceed

- **`AGENTS.md` or `CLAUDE.md` already exists** → do not overwrite either. Show the additions
  this system needs and let the user merge them.
- **`Notes/` already exists with documents in it** → do not touch it. That may be an unarchived
  phase; say so and point at `phase-transition`. Creating a fresh phase over it merges two phases
  into one folder, after which no boundary can separate them.
- **A folder exists under a different name** (`notebook/` or `notebooks/` rather than
  `research_repository/`; `docs/` doing the job of `Notes/`) → **ask, do not create a second one.**
  Two folders for one purpose is worse than an unconventional name.

## Step 0.5 — Ask what kind of work is coming (new mode only)

Only in **new** mode — in **adopt** mode the project already has its own history and code-skill
usage, so asking would be noise. Ask once, before creating anything. It decides nothing about what
gets scaffolded (Step 1 creates the same folders either way) — only which code skill to point the
user to once they start writing something.

1. **Research first, or straight to production?**
   - *Research first* — quick, exploratory work in `research_repository/`, tested before anything
     is built for real.
   - *Production* — building the real thing directly, no exploratory stage first.
2. **Which language?**

Route the answer, and tell the user which skill applies — **don't invoke it yet**; there is no
code to write during scaffolding:

| Stage | Python | Any other language |
|---|---|---|
| Research | `simple-dev-notebook` | `simple-dev-script` |
| Production | `production-code-python` | `production-grade-implementation` |

If the language fits neither skill well, say so plainly and note that writing a language-native
equivalent skill is a supported pattern, not a last resort.

**A one-time framing question, not a constraint.** A project can mix languages or move from
research to production later; each invocation picks the skill that fits that moment.

## Step 1 — Create the directories

```
data/raw/                  source data; no phase ever writes here
data/reference/            lookup tables, schemas, fixtures
files/                     project-wide constants: certs, templates, static docs
research_repository/       research; phases accumulate here
research_repository/data/  all run output, keyed by phase and run id
```

Add a one-line `research_repository/README.md` that will become the phase index.

**Do not create:**

- `Project_Intent/` files — those are the user's, and a placeholder there reads as intent that
  isn't. Offer to draft `Project_Overview.md` from what they tell you; write nothing unprompted.
- `research_repository/common/` — it appears only when a *second* phase needs the same helper.
- `src/`, `backend/`, `frontend/` or any production folder — an empty production folder signals
  intent that does not exist yet. Production code gets a home when something real needs one.
- Any phase folder — `phase-context` starts the first phase (step 3).

## Step 2 — `.gitignore`

`research_repository/data/` must be ignored **from day one**. Retrofitting it after a hundred run
folders are already in git history means rewriting history or living with a bloated repo.

If `.gitignore` exists, **append only the lines that are missing** — never rewrite it.

```gitignore
# run output — regenerable, can be large
research_repository/data/
```

Add language-specific entries only if the repo has no coverage for them already
(`__pycache__/`, `.ipynb_checkpoints/`, `.env`). Do not impose a full boilerplate ignore file on a
repo that already has one.

## Step 3 — `AGENTS.md`

Copy [TEMPLATE_AGENTS.md](TEMPLATE_AGENTS.md) to the project root as `AGENTS.md`, substituting the
project name in the title. Every supported harness reads it: Codex, Copilot and Cursor read
`AGENTS.md` natively, and Claude Code reads it directly from v2.1.277.

**Then write a one-line `CLAUDE.md` beside it**, containing only:

```
@AGENTS.md
```

That covers Claude Code installs older than v2.1.277, which read `CLAUDE.md` and ignore
`AGENTS.md` entirely. The import never loads the content twice on any version, so it is safe to
leave in place indefinitely — drop it only when every user of the project is known to be current.

**Read the template's own header first** — it flags which rules are opinionated defaults (the
write-scope and no-code-changes-unless-asked rules) so the user can confirm or change them rather
than inherit them silently.

If either file already exists, show what this system needs added and let the user merge it.

## Step 4 — Hand off, don't continue

Stop here. Tell the user what to run next, in this order:

> Structure created: `<list of paths>`. Nothing else was touched. Next:
> 1. `project-knowledge` (initialize) — creates `Project_Context/` and seeds it from whatever
>    already documents this project
> 2. `phase-context` — creates `Notes/` and defines the first phase

**Do not run those yourself.** They own those folders, and each needs its own instruction under
the write-scope rule. `project-knowledge` goes first so `Key_Decisions.md` exists before
`INHERITED.md` would link to it.

If the user has no `Project_Intent/Project_Overview.md`, mention it once here — it is the entry
point a cold session reads first, and a project without one is harder to pick up later. Offer;
do not write.

## Hard rules

- **Create only. Never move, rename, overwrite or delete.**
- **Never scaffold a folder because it might be needed** — `common/`, production folders and
  `Project_Intent/` files all appear when something real requires them, not before.
- **Never create a second folder for a job an existing folder already does.** Ask instead.
- **Confirm the path list before writing.** One wrong assumption about the project root scatters
  directories through someone's repo.
