#!/usr/bin/env python3
"""Update installed ThoughtLine skills from GitHub, the matching way for how they were installed.

    plugin   `claude plugin list` shows thoughtline -> the plugin manager's own update
    symlink  the skill directory, or a skill in it, is a symlink -> git pull in that clone
    copy     plain folders -> fetch upstream, back up changed folders, copy the new ones in

Dry run by default: reports what would change. --apply makes the changes.

    python3 thoughtline_update.py [--apply] [--ref main] [--repo URL] [--root DIR ...]
           [--only-installed] [--overwrite-local]
    exit 0 = up to date, or applied   exit 1 = error   exit 2 = updates available (dry run)
"""
import argparse, hashlib, json, shutil, subprocess, sys, tempfile, time
from pathlib import Path

REPO = "https://github.com/rohit-cpd/thoughtLine.git"
PLUGIN = "thoughtline@thoughtline-skills"
RECORD = ".thoughtline-install.json"
# The same roots project-state-brief searches for its validator. Widen the list; don't change it.
ROOTS = ["~/.claude/skills", "~/.agents/skills", "~/.copilot/skills", "~/.cursor/skills",
         ".claude/skills", ".agents/skills", ".github/skills", ".cursor/skills"]
# Outside every skill root on purpose: a harness that scans nested folders for SKILL.md would
# load a backup inside one as a duplicate skill.
BACKUPS = Path("~/.thoughtline/backups").expanduser()
# Names this library used before renaming. Reported only, never moved: a folder of the same name
# could belong to something else, and only the user can tell.
RETIRED = {"research-skill": "simple-dev-script", "phase-closeout": "phase-transition",
           "save-ai-plans": "notes-plans", "save-ai-discussions": "notes-discussions",
           "save-ai-backlog": "notes-backlogs", "save-ai-generated-references": "notes-references",
           "save-ai-generated-architecture": "notes-architecture"}


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        return subprocess.CompletedProcess(cmd, 127, "", f"{cmd[0]}: not found")


def tree_hash(d):
    h = hashlib.sha256()
    for p in sorted(d.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and p.name != ".DS_Store":
            h.update(str(p.relative_to(d)).encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def fetch(repo, ref, into):
    r = run(["git", "clone", "--quiet", "--depth", "1", "--branch", ref, repo, str(into)])
    if r.returncode:
        sys.exit(f"could not fetch {repo} at {ref}: {r.stderr.strip()}")
    skills = {p.parent.name: p.parent for p in (into / "skills").glob("*/SKILL.md")}
    if not skills:  # a wrong repo or ref must not read as "everything was removed upstream"
        sys.exit(f"{repo} at {ref} has no skills/*/SKILL.md — stopping")
    return run(["git", "-C", str(into), "rev-parse", "HEAD"]).stdout.strip(), skills


def find_installs(roots, names):
    seen, found = set(), []
    for r in roots:
        base = Path(r).expanduser()
        for d in (base, base / "thoughtline" / "skills"):   # second: older skills-dir plugin layout
            if not d.is_dir() or d.resolve() in seen:
                continue
            record = load_record(d)
            ours = [n for n in sorted(set(names) | set(record.get("skills", {})))
                    if (d / n / "SKILL.md").is_file()]
            if ours:
                seen.add(d.resolve())
                found.append((d, ours, record))
    return found


def load_record(d):
    try:
        return json.loads((d / RECORD).read_text())
    except (OSError, ValueError):
        return {}


def symlink_clone(d, ours):
    # shortcut: assumes every symlinked skill in one directory points into the same clone —
    # check each link's toplevel separately if mixed layouts ever show up
    link = d if d.is_symlink() else next((d / n for n in ours if (d / n).is_symlink()), None)
    if link is None:
        return None
    top = run(["git", "-C", str(link.resolve()), "rev-parse", "--show-toplevel"])
    return Path(top.stdout.strip()) if top.returncode == 0 else Path(link.resolve())


def plan_copy(d, ours, record, upstream, only_installed):
    tracked, before = record.get("skills", {}), set(record.get("upstream_skills", []))
    plan = []
    for name, src in sorted(upstream.items()):
        if name not in ours:
            # absent on purpose if it existed upstream at the last update and still isn't here
            if not only_installed and (not before or name not in before):
                plan.append(("add", name))
            continue
        cur = tree_hash(d / name)
        if cur == tree_hash(src):
            continue
        plan.append(("locally modified" if name in tracked and tracked[name] != cur else "update",
                     name))
    plan += [("removed upstream", n) for n in ours if n not in upstream and n in tracked]
    plan += [(f"retired name (now {new})", old) for old, new in RETIRED.items()
             if (d / old / "SKILL.md").is_file() and old not in tracked]
    return plan


def apply_copy(d, plan, upstream, record, commit, args, stamp):
    backup = BACKUPS / stamp / str(d.resolve()).strip("/").replace("/", "__")
    tracked = dict(record.get("skills", {}))
    for action, name in plan:
        if action.startswith("retired") or (action == "locally modified"
                                            and not args.overwrite_local):
            continue  # reported, left in place; a kept local edit keeps its old baseline
        if (d / name).exists():
            backup.mkdir(parents=True, exist_ok=True)
            shutil.move(str(d / name), str(backup / name))
        if action == "removed upstream":
            tracked.pop(name, None)
            continue
        shutil.copytree(upstream[name], d / name)
        tracked[name] = tree_hash(d / name)
    for name in upstream:  # first run: no baseline yet, so take what is installed now
        if (d / name).is_dir():
            tracked.setdefault(name, tree_hash(d / name))
    (d / RECORD).write_text(json.dumps({
        "repo": args.repo, "ref": args.ref, "commit": commit, "updated_at": stamp,
        "upstream_skills": sorted(upstream), "skills": tracked}, indent=2) + "\n")
    return backup if backup.exists() else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true", help="make the changes (default: report)")
    ap.add_argument("--ref", default="main", help="branch or tag to update to")
    ap.add_argument("--repo", default=REPO, help="repository to update from")
    ap.add_argument("--root", action="append", help="skill directory to check (repeatable)")
    ap.add_argument("--only-installed", action="store_true", help="never add a skill not installed")
    ap.add_argument("--overwrite-local", action="store_true", help="replace locally edited skills")
    args = ap.parse_args()
    stamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    pending = False

    if run(["claude", "plugin", "list"]).stdout.count("thoughtline"):
        print(f"plugin install (Claude Code) — updated by: claude plugin update {PLUGIN}")
        if args.apply:
            r = run(["claude", "plugin", "update", PLUGIN])
            print("  " + (r.stdout or r.stderr).strip().replace("\n", "\n  "))

    with tempfile.TemporaryDirectory() as tmp:
        commit, upstream = fetch(args.repo, args.ref, Path(tmp) / "src")
        print(f"upstream: {args.repo} @ {args.ref} ({commit[:7]}), {len(upstream)} skills")
        installs = find_installs(args.root or ROOTS, upstream)
        if not installs:
            print("no copied or symlinked install found in:", ", ".join(args.root or ROOTS))
        for d, ours, record in installs:
            clone = symlink_clone(d, ours)
            if clone:
                run(["git", "-C", str(clone), "fetch", "--quiet"])
                behind = run(["git", "-C", str(clone), "rev-list", "--count", "HEAD..@{u}"])
                dirty = run(["git", "-C", str(clone), "status", "--porcelain"]).stdout.strip()
                state = (f"{behind.stdout.strip()} commit(s) behind" if behind.returncode == 0
                         else "no upstream branch to compare against")
                print(f"\n{d} — symlink into {clone}: {state}"
                      + (", has uncommitted changes" if dirty else ""))
                if behind.returncode == 0 and behind.stdout.strip() != "0":
                    pending = True
                    if args.apply and not dirty:
                        r = run(["git", "-C", str(clone), "pull", "--ff-only"])
                        print("  " + ("pulled" if r.returncode == 0 else r.stderr.strip()))
                    elif args.apply:
                        print("  skipped — commit or stash those changes, then run again")
                continue
            plan = plan_copy(d, ours, record, upstream, args.only_installed)
            print(f"\n{d} — copy, {len(ours)} ThoughtLine skill(s)"
                  + ("" if record else " — no install record yet: local edits can't be told "
                     "from upstream changes, so anything replaced is backed up"))
            for action, name in plan:
                print(f"  {action:<16} {name}")
            # retired names are reported, never acted on — they must not read as a pending update
            if not [a for a, _ in plan if not a.startswith("retired")]:
                print("  up to date")
                continue
            pending = True
            if args.apply:
                backup = apply_copy(d, plan, upstream, record, commit, args, stamp)
                print(f"  applied{f'; previous versions moved to {backup}' if backup else ''}")

    if args.apply and pending:
        print("\nRestart your tool so it rescans skills — this session still has the old ones.")
    return 2 if pending and not args.apply else 0


if __name__ == "__main__":
    sys.exit(main())
