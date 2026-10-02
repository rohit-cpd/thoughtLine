# ThoughtLine

**A project-memory system for coding agents.** 21 skills that keep the reasoning behind a project on
disk — what was decided and why, what's still open, how the system actually works — so a new
session, or a new person, can pick it up without archaeology.

The problem it solves is narrow and familiar: the agent explains something well, you both move on,
and three weeks later nobody can reconstruct why the pipeline rejects malformed rows instead of
quarantining them. ThoughtLine writes that down as it happens, under a permission model you control
per operation.

> **Built to the open [Agent Skills](https://agentskills.io/specification) standard** — a directory
> per skill, each with a `SKILL.md`. Claude Code, Codex, GitHub Copilot and Cursor all read that
> format. The skills are written and used against Claude Code; the other three are packaged and
> path-verified but trigger reliability varies by tool and model, since a description that fires
> consistently in one may not in another.

---

## Install

### As a plugin

Claude Code and Copilot CLI read the same marketplace descriptor:

```
/plugin marketplace add rohit-cpd/thoughtLine
/plugin install thoughtline@thoughtline-skills
```

```bash
copilot plugin marketplace add rohit-cpd/thoughtLine
copilot plugin install thoughtline@thoughtline-skills
```

Both read `.claude-plugin/marketplace.json`, which this repo ships listing itself as its own
single-plugin marketplace.

**Codex and Cursor install from their own marketplaces** — Codex from
[`openai/plugins`](https://github.com/openai/plugins), Cursor via `/add-plugin` — and getting listed
there means publishing. Until then, use the copy route below for those two. This repo also ships
`.agents/plugins/marketplace.json` for the cross-tool marketplace format, untested against either.

In Claude Code every skill is then `/thoughtline:<name>` — `/thoughtline:project-start`,
`/thoughtline:notes-plans`, and so on. Auto-update is off by default for third-party
marketplaces, so you get updates when you ask for them with
`claude plugin update thoughtline@thoughtline-skills`.

### By copying the skills in

Works everywhere, with no plugin system involved. Clone first:

```bash
git clone https://github.com/rohit-cpd/thoughtLine.git
cd thoughtLine
```

Then copy the skills to wherever your tool reads them. For **Claude Code**:

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

For **Codex, Copilot and Cursor**:

```bash
mkdir -p ~/.agents/skills
cp -R skills/* ~/.agents/skills/
```

Restart your tool afterwards so it rescans for skills. `~/.agents/skills/` is the cross-tool path and
one copy serves all three. For a single project, use
`.agents/skills/` inside that repo — Codex walks up the tree scanning every one it finds, so a
monorepo can carry skills at the root and in sub-projects. Symlink instead of copying to track
updates: `ln -s "$PWD/skills" ~/.agents/skills`.

---

## Quick start

```
project-start          # once per project — folders, .gitignore, AGENTS.md
project-knowledge      # seeds Project_Context/ from whatever already documents this
phase-context          # defines phase 1
   … do the work; documentation accumulates in Notes/ as you go …
project-state-brief    # "where are we" — read-only, answers from the trail
phase-transition       # archive the phase, carry open work into the next
```

`project-start` writes an `AGENTS.md` into your project, plus a one-line `CLAUDE.md` importing it
for Claude Code installs older than v2.1.277. **That file is what makes the rest work** — it routes
an instruction like "write this up" to the right skill without you naming one. It ships as an
editable template with its three opinionated rules flagged at the top, so you can narrow anything
you disagree with before adopting it. Narrowing works; widening does not.

---

## The part that's different: documentation that writes itself, selectively

Most systems make you ask for every document. The useful middle ground is that *some* writes are
safe to do unprompted and some are not — and that creating a file and updating one are not the same
permission.

| Content | Skill | New file | Update existing |
|---|---|---|---|
| Explaining something that already exists | `notes-references` | **Automatic** | **Automatic** |
| What was decided, and why | `notes-discussions` | Ask | **Automatic** |
| How to build something not yet built | `notes-plans` | Ask | **Automatic** |
| Work deferred, parked, or just completed | `notes-backlogs` | Ask | **Automatic** |
| Components, data flow, how pieces connect | `notes-architecture` | Ask | **Ask** |

The reasoning: a reference describes something that already exists, so writing one can only be
wrong about detail, never about intent — it's cheap to write and cheap to correct. An architecture
document is a claim about how your system *is*, so changing one without asking changes the record.
Plans and backlogs sit between: starting a new one is your call, but letting an existing one drift
out of date is the failure, so keeping it current needs no permission.

Two judgement calls always come back to you: **starting a new discussion log**, because no model can
tell when a conversation has finished, and **which topic file something belongs to** when it's
genuinely borderline.

**Code is never written without an explicit instruction**, including comments and tests.

---

## What it creates

```
Project_Intent/        yours — what the project is meant to be; skills read it, never rewrite it
Project_Context/       maintained — what's currently true: state, system, decisions, timeline, glossary
Notes/                 the working trail for the phase in flight
├── PHASE_CONTEXT.md   this phase's goal, scope, success criteria, open questions
├── INHERITED.md       derived from the last phase's closeout
├── Plans/             dated, immutable; a feature change is a new plan, chained by supersession
├── Architecture/      dated, immutable; each diagram records the commit it reflects
├── References/        one undated file per topic, grown with dated entries
├── Discussions/       one undated log per topic; past entries immutable, reversals appended
└── Backlogs/          one living file per area; stable IDs, never reused, never renumbered
Archive/Phase_NN-slug/ a completed phase, moved intact, with a closeout at its root
research_repository/   exploratory code by phase; all run output under its own data/
```

The split that does the work: `Project_Intent/` is yours and only changes when you say so;
`Project_Context/` is maintained for you. When the two disagree, you get told about it rather than
having one quietly reconciled into the other.

---

## The skills

### Documentation — gated per the table above

| Skill | What it owns |
|---|---|
| `notes-references` | How existing code, data or config actually works, so it isn't re-derived |
| `notes-discussions` | What was decided and why, as a dated log per topic |
| `notes-plans` | How to build something not yet built, with supersession chains |
| `notes-backlogs` | Open and deferred work, with stable IDs that survive phase boundaries |
| `notes-architecture` | Components, data flow, diagrams — the strictest permissions of the five |
| `project-state-brief` | "Where are we" in a fixed cheap read order; read-only, and flags contradictions instead of smoothing them |

### Code — explicit instruction only

| Skill | When |
|---|---|
| `production-code-python` | Building the real thing, Python |
| `production-grade-implementation` | Building the real thing, any other language |
| `simple-dev-notebook` | Exploratory work, Python — flat, readable top to bottom |
| `simple-dev-script` | Exploratory work, any other language |
| `research-to-production-port` | Working research code becoming production for the first time |
| `refactoring` | Restructuring existing code with behaviour held identical against a safety net |
| `writing-tests` | Tests that fail for a real reason, including characterization tests |
| `document-code-comments` | Comments and docstrings inside source files |
| `git-commit-conventions` | Commit messages and PR descriptions grounded in the actual diff |
| `minimal-code-check` | Loaded before writing new code: does this need to exist at all? |

Explore and build are mutually exclusive within a language — if a request is ambiguous between them,
you get asked. `research-to-production-port` sits between the columns: the logic already exists and
works, so it's neither a fresh build nor a refactor, and it ports from one *named run* verified
against that run's recorded output.

### Lifecycle — you name these explicitly

| Skill | What it does |
|---|---|
| `project-start` | Once per project: folders no other skill owns, `.gitignore`, `AGENTS.md` |
| `phase-context` | Defines the phase in flight; scaffolds `Notes/` |
| `phase-transition` | Runs a phase boundary: archive, carry open work forward, write a closeout |
| `project-knowledge` | The documents that outlive every phase |
| `phase-code-carry` | Starts the next phase's code from the previous phase's, without breaking it |

All five carry `disable-model-invocation: true`, so they run only when you name them. They move or
rewrite files across the whole project, and a statement that a phase has ended is not an instruction
to archive it.

A phase boundary is the one moment an append-only trail fails — it records every step but never
states the resulting position. `phase-transition` runs **light by default** (four closeout sections,
minutes) and heavy on request, because a procedure heavy enough to dread is one that gets skipped.
It also never deletes: it *moves* the tree, so there's no window where a partial copy is followed by
a successful delete.

---

## Design notes

**Every skill works on its own.** No skill reads another's bundled files, so any one folder can be
lifted out and used alone. That rules out sharing a common file between skills, and the cost is
real: `simple-dev-notebook` and `simple-dev-script` are deliberate copies that have to be kept in
sync by hand.

**No skill names a single tool.** Write scopes refer to "the project's agent instructions" rather
than one filename, so the same skill reads correctly whether your project has an `AGENTS.md`, a
`CLAUDE.md`, Copilot instructions or Cursor rules. Any of them can narrow a skill's write scope;
none can widen it.

**A machine check, not just prose.** `skills/project-state-brief/scripts/validate_notes.py` catches
what prose can't enforce and a phase boundary later pays for: a document with no `initiative` (and
so invisible when the phase is archived), a duplicate backlog ID, a `next_item_id` that's too low,
an item that was open in the last archived backlog and reached no current one. `project-state-brief`
runs it and reports every error verbatim. It takes the project root as an argument and needs nothing
copied into your project — the skill locates it from the base directory the harness reports, or by
searching the install roots when the harness reports none, and continues without it either way.

**Unverified claims stay marked unverified.** Across every skill, a fact that can't be traced to a
run, a commit or a document is recorded as unverified rather than asserted. These files become the
thing everyone trusts, and an unmarked guess propagates.

---

## License

MIT — see [LICENSE](LICENSE).
