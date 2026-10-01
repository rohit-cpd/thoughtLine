---
name: git-commit-conventions
description: >-
  Use when the user asks to commit changes, write a commit message, open a
  PR, write a PR description, squash/clean up commits, or write a changelog
  entry from a diff. Drafts messages that match the repo's actual commit
  history and describe what's really in the diff. Not for deciding what code
  changes to make - this skill only covers how completed changes are
  described and packaged for version control.
---

# Git Commit Conventions

When the user wants a commit message, PR description, or changelog entry written, ground it in
the actual diff and the repo's real history — never invent what changed or impose a generic
format the repo doesn't use. Applies to any repo/language.

## When to use
- User says "commit this", "write a commit message", "commit my changes", "open a PR", "write a
  PR description", "squash these", or similar, about changes that already exist.
- Not for deciding what the code change itself should be — that belongs to the build and
  refactor skills (`production-grade-implementation`, `production-code-python`,
  `simple-dev-notebook`, `simple-dev-script`, `refactoring`, `writing-tests`).

## Before writing anything
1. Look at the actual diff (`git diff` / `git status`), not just the user's description of it —
   the message must match what really changed.
2. Check recent history (`git log --oneline -20`) for the repo's real convention: Conventional
   Commits (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `test:`), plain imperative summaries,
   ticket-id prefixes, or something else. Match whatever is already there — don't impose a
   different format on an established repo.

## Commit message (default format, if no repo convention is detected)
- Summary line: imperative present tense, ≤ 72 characters — "Fix null check on empty cart", not
  "Fixed..." or "Fixes...".
- Blank line, then a body explaining **why**, not what — the diff already shows what; the message
  earns its keep by giving context the diff can't (motivation, what was tried and rejected, what
  this unblocks).
- Wrap the body at roughly 72-100 columns.
- If the repo uses Conventional Commits, match the detected prefix and scope exactly instead of
  the format above.

## Scope discipline
- One logical change per commit. If the diff bundles unrelated changes (a fix plus an unrelated
  formatting sweep), say so and offer to split it rather than writing one message that glosses
  over both.
- Don't claim things the diff doesn't support — e.g. don't write "adds tests" unless test files
  actually changed. Read the diff; don't infer from the request text alone.
- Reference an issue/ticket number only if the user supplies one or it's clearly implied by repo
  convention (e.g. present in the branch name) — never fabricate one.

## PR descriptions
Cover, in order: what changed and why, a short list of the notable changes, how it was verified
(tests run, manual steps taken), and explicit callouts for anything risky or breaking. If the repo
has `.github/PULL_REQUEST_TEMPLATE.md` (or similar), fill that template instead of inventing a new
shape.

## Safety
- Never include secrets, tokens, or credentials that appear in the diff inside the commit message
  or PR body, even to explain what was removed.

## Notes
- This skill drafts the message/description. Actually running `git commit`, pushing, or opening
  the PR still needs the user's explicit go-ahead unless they clearly asked for that too.
