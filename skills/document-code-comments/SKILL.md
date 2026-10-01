---
name: document-code-comments
description: >-
  Use when asked to add or improve comments, docstrings or API documentation
  **inside source files** - "add comments", "write docstrings", "document this
  function for maintainers". **Output: edited source files, nothing else.** Not
  for a separate markdown document about existing code (that is
  `notes-references`, which writes a file) and not for explaining code in chat
  (answer directly - no skill needed). "Explain this module" matches all three,
  so ask which output is wanted rather than guessing.
---

# Document Code Comments

Make a package understandable to another engineer **without changing behaviour**. Document
ownership, wiring and contracts — not line-by-line narration.

Ordinary documentation craft is assumed, not restated: comments explain *why*, docstrings on public
symbols, each language's own convention (module docstrings in Python, `//!` in Rust, JSDoc tags in
TS, package comments in Go). What follows is what gets this wrong in practice.

## Write scope

**This edits source files, and only on an explicit instruction to do so.** A documentation pass
still shows up in `git diff`, so it is a code change regardless of how harmless it looks. If code
looks under-documented and nobody asked, say so in one line and move on — offer, don't write.

Never writes `Notes/`, `Project_Intent/`, `Project_Context/` or `Archive/`. A separate markdown
document *about* the code is `notes-references`, not this skill. The project's agent instructions
may narrow
this scope; nothing widens it.

## Match the repo before matching this skill

**Open an existing well-documented file in the repo and follow it.** Its conventions win over
anything here — a file documented in a style nothing else in the codebase uses is worse than one
left alone. Never impose a shape the language or repo does not already use.

## Where to start, and when to stop

Documentation has diminishing returns, and this skill is easy to over-apply. In order:

1. **Entry points** — what a reader opens first.
2. **Public API** — anything another module, package or service calls.
3. **Traps and invariants** — the places where the obvious change breaks something.
4. **Internal helpers** — a single purpose line each, if their name is not enough.

**Stop when a new engineer could navigate the package without you.** Not when every symbol has a
docstring. Coverage is not the goal: a file with a good header and three well-placed why-comments
is better documented than one where every function carries a paragraph.

**Do not document dead code.** Delete it, or mark it deprecated with what replaced it.

## The file header — the most valuable thing here

One per non-trivial source file, where "non-trivial" means a file whose role a reader could not
infer from its name and its public symbols.

```
One-line purpose: what this file owns.

Key dependencies
    Name each important one and WHY it is needed — not just what it is. Call out lazy
    imports and any collision or shim reason explicitly.

Exports and consumers
    Public symbols, and who calls them. State what is intentionally internal or test-only.
    This is where consumer information belongs — not in each function's docs.

Flow
    The real sequence this file participates in. Name it for what it is:
    `Process flow`, `Decision flow`, `Request flow`, `Graph structure`, `Tool-call flow`.

Known limits (optional)
    Intentional stubs, unused fields, soft rules someone will mistake for bugs.
```

A good header names **consumers**, **non-goals** ("this deliberately does not handle X"), and any
collision trap. It is file-specific — **a header copy-pasted between files is worse than none.**

## The three rules that get broken

1. **Never restate what the signature already declares.** In a typed language the parameter type
   is in the signature; repeating it creates a second version that drifts out of date.
2. **Do not document the call graph per function.** "Called by" lists duplicate what any editor's
   find-usages answers instantly, go stale the moment a caller is added, and require a repo-wide
   search to write correctly. Consumer information belongs in the file header, once.
3. **Only include an example you have actually run**, or that the test suite executes. An example
   that no longer works is worse than none, because it reads as verified.

Two things worth documenting that people leave out: **side effects** — files, network, DB, logs,
caches, env, or explicitly *none* — and **complexity**, but only when non-obvious (tree recursion,
nested scans, hidden quadratics).

## Workflow

```
- [ ] Read an existing well-documented file; match its conventions
- [ ] Inventory the public entry points
- [ ] Write or refresh each file header (dependencies / exports / flow)
- [ ] Document the public API contracts
- [ ] Add why-only comments at traps and invariants
- [ ] Delete comments that are now wrong
- [ ] Confirm the diff changes no behaviour
```

### Accuracy pass (required)

Documentation that is confidently wrong is worse than none. Before finishing, verify:

- Side effects match the real I/O
- Flow descriptions match the actual control flow
- Named consumers really do import the symbol
- Every example runs
- Nothing claims a constraint the code does not enforce

Where you cannot verify a claim, **leave it out or mark it unverified** — never assert it.

## Graph and orchestrator modules

State machines, workflow DAGs, agent graphs and pipeline orchestrators need more than prose — a
reader cannot reconstruct routing from paragraphs. Read
[GRAPH_MODULES.md](GRAPH_MODULES.md) when documenting one. Ignore it otherwise.

## Related

Governs *how* code is commented, not what the code should look like — see
`production-grade-implementation`/`production-code-python` or
`simple-dev-notebook`/`simple-dev-script` for structure, and `writing-tests` for tests. If the
project maintains `Project_Context/System_Understanding.md`, point maintainers there for the
system-level view rather than reproducing it in a file header.
