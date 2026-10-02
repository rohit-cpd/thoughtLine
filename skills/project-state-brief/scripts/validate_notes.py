#!/usr/bin/env python3
"""Validate a project's Notes/ tree against the conventions these skills assume.

Checks what prose can only ask for politely. No dependencies; PyYAML used if present.

    python3 validate_notes.py [project-root]      # default: current directory
    exit 0 = clean, or warnings/notes only
    exit 1 = at least one error

Three channels. ERROR is a defect. WARN is probably a defect. NOTE reports something this script
deliberately does not enforce (archived documents are exempt from the frontmatter rules), so that
an empty report is never read as "checked and clean" for things that were never checked.
"""
import sys, os, re, json
from pathlib import Path

try:
    import yaml
    def parse_fm(text):
        return yaml.safe_load(text) or {}
except ImportError:                                    # tolerant fallback parser
    # This branch must agree with PyYAML on every field the checks below actually read, or the
    # same tree validates differently depending on whether PyYAML happens to be installed — and
    # the disagreement is silent, which is worse than an error. Two list forms both matter,
    # because the bundled EXAMPLE_*.md files use the block form and phase-transition's own
    # templates use the inline one:
    #     companion_docs:            companion_docs: ["a", "b"]
    #       - "a"
    #       - "b"
    def _inline_list(val):
        """`["a", "b"]` -> ['a', 'b']. Frontmatter ids never contain commas, so a plain split is
        sufficient; returns None when val is not an inline list."""
        if not (val.startswith("[") and val.endswith("]")):
            return None
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [x.strip().strip('"\'') for x in inner.split(",") if x.strip()]

    def parse_fm(text):
        out, key = {}, None
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if re.match(r"^\s+-\s", line) and key:              # block list item
                # NOT setdefault: `companion_docs:` with an empty value has already stored None
                # for this key, and setdefault would leave it there — so every item silently
                # vanished and dangling-link checks iterated nothing.
                if not isinstance(out.get(key), list):
                    out[key] = []
                out[key].append(line.split("-", 1)[1].strip().strip('"\''))
                continue
            if line.startswith(" "):                            # nested map: skip
                continue
            m = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
            if not m:
                continue
            key, val = m.group(1), m.group(2).strip()
            inline = _inline_list(val)
            if val in ("", "|", ">", ">-"):   out[key] = None if val == "" else ""
            elif inline is not None:          out[key] = inline
            elif val in ("null", "~"):        out[key] = None
            elif val in ("true", "false"):    out[key] = val == "true"
            else:                             out[key] = val.strip('"\'')
        return out

ITEM_RE = r"^#{2,4}\s+([A-Z]+\d+)\b"   # `### R4 — title`; tolerant of depth and dash. IDs minted
                                      # at a boundary (H1, R12) match this unchanged.
STATUS_KEYWORDS = {"open", "in-progress", "done", "blocked", "dropped", "superseded"}
CLOSED_KEYWORDS = {"done", "dropped", "superseded"}

# notes-backlogs mandates `<keyword> — <note>`: a space-padded em-dash. SEP_CANON is exactly what
# phase-transition's prose says it splits on, and it must stay that way — a validator that quietly
# accepted more than the skill does would pass files the boundary then mis-parses.
#
# SEP_TOLERANT exists only to produce a better message. When the strict parse yields something
# unrecognised, re-splitting on a bare en/em-dash usually recovers a real keyword, which means the
# keyword was never the problem — the separator was. Saying "unrecognised keyword `open – waiting`"
# sends the author to look at the word `open`, which is correct, and they find nothing wrong.
# Bare `-` is deliberately excluded here: it would split `in-progress` at its own hyphen.
SEP_CANON    = r"\s+[—-]{1,2}\s+"       # the spec: em-dash (or hyphen), spaces both sides
SEP_TOLERANT = r"\s*[—–]{1,2}\s*"       # diagnostic only: en-dash too, spaces optional

def status_keyword(status_value, strict=True):
    """The token phase-transition reads: text before the first ` — ` (or the whole value).

    strict=True mirrors what phase-transition actually does. strict=False is used only to
    produce a better diagnostic when the strict parse yields something unrecognised.
    """
    pattern = SEP_CANON if strict else SEP_TOLERANT
    head = re.split(pattern, status_value.strip(), 1)[0]
    return head.strip().strip("`*").strip().lower()

ERRORS, WARNS, NOTES = [], [], []
def err(p, msg):  ERRORS.append((p, msg))
def warn(p, msg): WARNS.append((p, msg))
# NOTE is neither a defect nor a warning: it reports something the validator deliberately does
# not enforce, so that "no output" is never mistaken for "checked and clean". It does not affect
# the exit code and is not counted in the WARN total project-state-brief reports.
def notes_line(p, msg): NOTES.append((p, msg))

# canonical folder name -> filename regex.
# Plans and Architecture are dated immutable snapshots. Discussions, References and Backlogs are
# living documents keyed by topic or area, so their filenames carry no date - it would be wrong
# the first time one was appended to. Recency lives in `updated_at`.
FOLDERS = {
    "Plans":         r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$",
    "Architecture":  r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$",
    # The negative lookahead is load-bearing: a date is made of digits and hyphens, so a plain
    # [a-z0-9-]+ would accept 2026-03-04-topic.md and leave the "never date these" rule unenforced.
    "References":    r"^(?!\d{4}-\d{2}-\d{2})[a-z0-9-]+\.md$",
    "Discussions":   r"^(?!\d{4}-\d{2}-\d{2})[a-z0-9-]+\.md$",
    "Backlogs":      r"^[a-z0-9-]+-backlog\.md$",
}

def read_doc(path):
    text = path.read_text(errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    return parse_fm(m.group(1)), m.group(2)

def derived_initiative(phase_number):
    """phase-context's rule: 'Phase ' + the number with leading zeros stripped ('06' -> 'Phase 6').

    Returns None when phase_number is absent or not numeric, so the check simply does not run
    rather than guessing at a project using some other scheme.
    """
    s = str(phase_number).strip().strip('"\'')
    return f"Phase {int(s)}" if s.isdigit() else None

def latest_closeout(root):
    """The newest Archive/*/CLOSEOUT.md by phase-folder name, or None."""
    arch = root / "Archive"
    if not arch.is_dir():
        return None
    closeouts = sorted(arch.glob("*/CLOSEOUT.md"), key=lambda p: p.parent.name)
    return closeouts[-1] if closeouts else None

def main(root):
    root = Path(root).resolve()
    notes = root / "Notes"
    if not notes.is_dir():
        print(f"no Notes/ under {root} — nothing to validate"); return 0

    # --- current phase ---
    # current_initiative drives two checks: per-document phase attribution, and Project_Context
    # staleness. When PHASE_CONTEXT.md is missing it used to stay None and BOTH silently stopped
    # running — and the missing file is the *normal* state between a phase-transition and the next
    # phase-context, which is exactly when the knowledge files are most likely to be stale. So
    # fall back to the closeout the boundary just wrote, and say which source was used.
    current_initiative = None      # for staleness; may come from the closeout fallback
    doc_initiative = None          # for per-document attribution; ONLY from PHASE_CONTEXT.md
    initiative_source = None
    pc = notes / "PHASE_CONTEXT.md"
    if not pc.exists():
        warn("Notes/", "no PHASE_CONTEXT.md — cannot check that documents belong to this phase")
        cl = latest_closeout(root)
        cfm = read_doc(cl)[0] if cl else None
        if cfm and cfm.get("next_initiative"):
            current_initiative = cfm["next_initiative"]
            initiative_source = f"Archive/{cl.parent.name}/CLOSEOUT.md `next_initiative`"
            notes_line("Notes/",
                       f"phase taken as {current_initiative!r} from {initiative_source} — the "
                       "normal state between a phase-transition and the next phase-context. "
                       "Project_Context staleness IS checked against it; per-document phase "
                       "attribution is not, since documents legitimately predate the new phase.")
        elif (root / "Project_Context").is_dir():
            # Only worth saying when there are knowledge files whose staleness went unchecked.
            warn("Project_Context/",
                 "staleness NOT checked: no PHASE_CONTEXT.md and no Archive/*/CLOSEOUT.md with "
                 "`next_initiative` to fall back on, so there is no current phase to compare "
                 "`last_updated_at_phase` against. Absence of staleness warnings below is not a "
                 "clean bill of health.")
    else:
        fm, _ = read_doc(pc)
        if not fm:
            err("Notes/PHASE_CONTEXT.md", "no frontmatter")
        else:
            current_initiative = doc_initiative = fm.get("initiative")
            initiative_source = "Notes/PHASE_CONTEXT.md"
            if not current_initiative:
                err("Notes/PHASE_CONTEXT.md", "no `initiative` — the phase marker every doc must copy")
            else:
                # phase-context derives `initiative` from `phase_number`; check the derivation
                # rather than trusting a free-form string that every document then copies.
                want = derived_initiative(fm.get("phase_number"))
                if want and current_initiative != want:
                    warn("Notes/PHASE_CONTEXT.md",
                         f"`initiative` is {current_initiative!r} but `phase_number` "
                         f"{str(fm.get('phase_number'))!r} derives {want!r}. phase-context defines "
                         "`initiative` as 'Phase ' + the number with leading zeros stripped. Every "
                         "document in this phase copies this string verbatim, so correcting it "
                         "later means re-tagging all of them — fix it now, or record the "
                         "human-facing name in `aliases` and expect this warning every run.")

    ids, docs = {}, []
    for folder in sorted(os.listdir(notes)):
        d = notes / folder
        if not d.is_dir():
            continue
        canon = folder
        if canon not in FOLDERS:
            # No alias map: this script does not guess which category an unconventional folder
            # name was meant to be. Say plainly that nothing inside it was checked, so the
            # warning is not mistaken for "checked and fine except for the name".
            warn(f"Notes/{folder}/",
                 f"not one of {sorted(FOLDERS)} — **nothing inside it was validated** (no "
                 "frontmatter, `id` or `initiative` checks ran on its documents), and it will "
                 "land under *Unclassified* at the next transition. Rename it to a category "
                 "folder, or accept that its contents are unchecked")
            continue
        pattern = FOLDERS[canon]
        for f in sorted(d.glob("*.md")):
            rel = f"Notes/{folder}/{f.name}"
            if f.name.startswith("EXAMPLE_") or f.name == "README.md":
                continue
            if not re.match(pattern, f.name):
                warn(rel, f"filename does not match the `{canon}/` convention")
            fm, body = read_doc(f)
            if fm is None:
                err(rel, "no frontmatter — invisible to a phase transition")
                continue
            docs.append((rel, canon, fm, body))
            did = fm.get("id")
            if not did:
                err(rel, "no `id`")
            else:
                if did in ids:
                    err(rel, f"duplicate id `{did}` (also {ids[did]})")
                ids[did] = rel
                if did != f.stem:
                    warn(rel, f"`id` ({did}) does not match filename stem ({f.stem})")
            init = fm.get("initiative")
            if not init:
                err(rel, "no `initiative` — this document disappears when the phase is archived")
            elif doc_initiative and init != doc_initiative:
                err(rel, f"`initiative` is {init!r} but this phase is {doc_initiative!r} "
                         "— a leftover from an unarchived phase, or a typo")

    # --- link integrity ---
    # phase-transition step 5b/5c instructs writing `companion_docs: ["<the closeout's id>"]` onto
    # carried-forward backlogs and the archive index — a pointer at a document that, by design, has
    # just moved into Archive/. Resolving targets against Notes/ alone made every project past its
    # first boundary emit that warning forever, which trains the reader to ignore the whole class.
    # So resolve against the archive too, and warn only on a genuinely dangling link.
    archived_ids = {}
    arch = root / "Archive"
    if arch.is_dir():
        for p in sorted(arch.rglob("*.md")):
            afm = read_doc(p)[0]
            aid = afm.get("id") if afm else None
            # Fall back to the stem so a frontmatter-less archived document is still resolvable;
            # CLOSEOUT.md carries a real `id` ("phase-05-closeout") and is found by it.
            archived_ids.setdefault(aid or p.stem, str(p.relative_to(root)))

    for rel, canon, fm, _ in docs:
        for field in ("companion_docs", "depends_on", "blocks", "supersedes", "superseded_by"):
            v = fm.get(field)
            for target in ([v] if isinstance(v, str) else (v or [])):
                if not target or target in ids:
                    continue
                if target in archived_ids:
                    continue          # resolved in the archive — the documented convention
                if "/" in target:
                    # A topic continuing across a phase boundary points `supersedes` at its
                    # archived predecessor by PATH, not id, because topic slugs repeat per phase
                    # (Notes/Discussions/retry-strategy.md exists again in the next phase). Check
                    # the path instead of treating it as a dangling id.
                    if not (root / target).exists():
                        warn(rel, f"`{field}` points at path `{target}`, which does not exist")
                    continue
                warn(rel, f"`{field}` points at `{target}`, which is not a document in Notes/ "
                          "and was not found in Archive/ either — the link is dangling")

    # --- backlog integrity ---
    for rel, canon, fm, body in docs:
        if canon != "Backlogs":
            continue
        # An item written at the wrong heading depth matches neither ITEM_RE nor the loose-prose
        # splitter below (both anchored to ^#{2,4}), so it is not counted, not carried at a
        # boundary, and produces no signal at all — a worse failure than loose prose, which at
        # least errors. Catch it before anything else parses the body.
        for depth_re, what in ((r"^(#)\s+([A-Z]+\d+)\b", "H1 (`#`)"),
                               (r"^(#{5,})\s+([A-Z]+\d+)\b", "H5 or deeper")):
            for hashes, iid in re.findall(depth_re, body, re.M):
                err(rel, f"item `{iid}` is written as {what} — items must be `###` (`##`–`####` "
                         "is tolerated). At this depth it matches neither the item parser nor "
                         "the loose-prose check, so it is invisible: never counted, never "
                         "carried at a phase boundary, and silent about it.")

        item_ids = re.findall(ITEM_RE, body, re.M)
        seen = set()
        for i in item_ids:
            if i in seen:
                err(rel, f"item `{i}` appears twice — IDs are never reused")
            seen.add(i)
        if not item_ids:
            err(rel, "no items parsed — headings are not `### <ID> — <title>`, so every backlog "
                     "check below was skipped. Silence here is not a pass.")
        nxt = fm.get("next_item_id")
        if not nxt:
            err(rel, "no `next_item_id` — IDs will get reused")
        elif item_ids:
            m = re.match(r"^([A-Z]+)(\d+)$", str(nxt))
            nums = [int(re.match(r"^[A-Z]+(\d+)$", i).group(1)) for i in item_ids]
            if m and int(m.group(2)) <= max(nums):
                err(rel, f"`next_item_id` is {nxt} but item {m.group(1)}{max(nums)} already exists")
        for block in re.split(r"^#{2,4}\s+", body, flags=re.M)[1:]:
            head = block.split("\n", 1)[0].strip()
            rest = block.split("\n", 1)[1] if "\n" in block else ""
            if not re.match(r"^[A-Z]+\d+\b", head):    # not an `### <ID>` item
                # loose prose in a backlog is invisible to a phase transition and lost at the
                # boundary — this is the §0.3 failure. HTML comments don't count.
                prose = re.sub(r"<!--.*?-->", "", rest, flags=re.S).strip()
                if prose:
                    err(rel, f"section `{head[:50]}` has body text but no `### <ID>` heading — "
                             "loose prose in a backlog is dropped at the next boundary. Give it "
                             "an item ID, or move it out of the backlog.")
                continue
            status_match = re.search(r"\*\*Status:\*\*\s*(.+)", block)
            if "**Status:**" not in block:
                err(rel, f"item `{head}` has no Status")
            elif not status_match:
                err(rel, f"item `{head}` has a `**Status:**` label with nothing after it on the "
                         "same line")
            else:
                line = status_match.group(1)
                # new format: `<keyword> — <short note>`. phase-transition reads only the keyword
                # (text before the first ` — `); a line that passes a looser check and fails the
                # carry rule is worse than one that fails both.
                kw = status_keyword(line)
                if kw not in STATUS_KEYWORDS:
                    # Retry with the tolerant separator. If that recovers a real keyword, the
                    # keyword was never the problem — the separator was — so say so.
                    loose = status_keyword(line, strict=False)
                    if loose in STATUS_KEYWORDS:
                        warn(rel, f"item `{head[:60]}` status keyword `{loose}` is valid, but the "
                                  "separator before the note is not: phase-transition splits on a "
                                  "space-padded em-dash (` — `), so this line parses as "
                                  f"`{kw[:30]}` instead. Write `{loose} — <note>`.")
                    else:
                        warn(rel, f"item `{head[:60]}` status keyword is `{kw[:30]}` — must be one of "
                                  f"{sorted(STATUS_KEYWORDS)} before any ` — ` note")

    # --- carried-forward items actually arrived ---
    # Read the ARCHIVED source backlogs directly, never the closeout's "Carried forward" list:
    # the closeout is a document the transition itself wrote, so an item dropped there passes
    # silently. This mirrors phase-transition Step 5 "Verify in both directions" (2026-08-29).
    if arch.is_dir():
        closeouts = sorted(arch.glob("*/CLOSEOUT.md"), key=lambda p: p.parent.name)
        if closeouts:
            latest = closeouts[-1]
            _, cbody = read_doc(latest)
            cbody = cbody or ""
            aband = re.search(r"##\s*\d*\.?\s*Deliberately abandoned(.*?)(?=\n##\s|\Z)", cbody, re.S)
            abandoned = set(re.findall(r"`?([A-Z]+\d+)`?", aband.group(1))) if aband else set()

            present = set()
            for rel, canon, fm, body in docs:
                if canon == "Backlogs":
                    present |= set(re.findall(ITEM_RE, body, re.M))

            # Match a backlog by EITHER its folder or its own filename. Globbing only
            # `*[Bb]acklog*/*.md` meant a phase that tracked deferred work as `*-backlog.md`
            # files inside References/ matched nothing — and this whole block, the one check
            # that catches an item dropped at the boundary, passed in silence.
            sources = sorted({p for p in latest.parent.rglob("*.md")
                              if "backlog" in p.name.lower() or "backlog" in p.parent.name.lower()})
            if not sources:
                notes_line(f"Archive/{latest.parent.name}/",
                           "no backlog file found in this archive, so the backward carry-forward "
                           "check did not run. If the phase tracked deferred work under another "
                           "name, an item dropped at the boundary would not be caught here.")
            for src in sources:
                _, sbody = read_doc(src)
                for block in re.split(r"^#{2,4}\s+", sbody or "", flags=re.M)[1:]:
                    m = re.match(r"^([A-Z]+\d+)\b", block.split("\n", 1)[0].strip())
                    if not m:
                        continue
                    iid = m.group(1)
                    sm = re.search(r"\*\*Status:\*\*\s*(.+)", block)
                    kw = status_keyword(sm.group(1)) if sm else "open"
                    if kw in CLOSED_KEYWORDS:
                        continue
                    if iid not in present and iid not in abandoned:
                        err(f"Archive/{latest.parent.name}/{src.parent.name}/{src.name}",
                            f"`{iid}` was still open in the archived backlog, is in no current "
                            "backlog, and is not under the closeout's *Deliberately abandoned* "
                            "— dropped at the boundary")

    # --- archived-tree coverage, and the closeout's own counts ---
    # The archive is immutable, so its documents are deliberately NOT held to the frontmatter
    # rules enforced above for Notes/ — a phase archived before this library existed will never
    # comply and there is nothing to fix. But silence there reads as a pass, so report the
    # coverage as a note, and use the same scan to check the two counts the closeout carries
    # (nothing else consumes them, so a wrong value would otherwise never surface).
    if arch.is_dir():
        for cl in sorted(arch.glob("*/CLOSEOUT.md"), key=lambda p: p.parent.name):
            phase_dir = cl.parent
            # Every .md in the archive except the closeout and the _Summary/ chronologies,
            # which phase-transition writes itself and does not inventory.
            archived = [p for p in sorted(phase_dir.rglob("*.md"))
                        if p != cl and "_Summary" not in p.relative_to(phase_dir).parts]
            no_fm = [p for p in archived if read_doc(p)[0] is None]
            if no_fm:
                notes_line(f"Archive/{phase_dir.name}/",
                           f"{len(no_fm)} of {len(archived)} archived documents have no "
                           "frontmatter (not an error — the archive is immutable and predates "
                           "or bypassed the convention; recorded so the silence is not read "
                           "as a pass)")

            cfm, _ = read_doc(cl)
            if not cfm:
                continue
            inv = cfm.get("documents_inventoried")
            unatt = cfm.get("documents_unattributed")
            try:
                inv = int(inv) if inv is not None else None
                unatt = int(unatt) if unatt is not None else None
            except (TypeError, ValueError):
                warn(f"Archive/{phase_dir.name}/CLOSEOUT.md",
                     "`documents_inventoried` / `documents_unattributed` are not integers")
                continue
            if inv is not None and inv != len(archived):
                warn(f"Archive/{phase_dir.name}/CLOSEOUT.md",
                     f"`documents_inventoried` is {inv} but {len(archived)} documents are in the "
                     "archive (excluding CLOSEOUT.md and _Summary/) — step 3's count check and "
                     "this field disagree")
            if unatt is not None:
                if inv is not None and unatt > inv:
                    err(f"Archive/{phase_dir.name}/CLOSEOUT.md",
                        f"`documents_unattributed` ({unatt}) exceeds `documents_inventoried` "
                        f"({inv}) — it counts a subset of them")
                # The invert-error signature: the field counts documents batch-attributed under
                # Step 1's "most/all lack frontmatter" rule. Those documents are exactly the ones
                # with no frontmatter. A positive count with none of them present means the field
                # was filled from the §9 "Unclassified" list instead, which it explicitly is not.
                if unatt > len(no_fm):
                    warn(f"Archive/{phase_dir.name}/CLOSEOUT.md",
                         f"`documents_unattributed` is {unatt} but only {len(no_fm)} archived "
                         "documents lack frontmatter. This field counts documents batch-attributed "
                         "under Step 1's 'most/all lack frontmatter' rule — NOT the §9 "
                         "'Unclassified' list, which is listed there and never counted here.")

    # --- Project_Context staleness ---
    ctx = root / "Project_Context"
    if ctx.is_dir() and current_initiative:
        for f in sorted(ctx.glob("*.md")):
            fm, _ = read_doc(f)
            if not fm:
                warn(f"Project_Context/{f.name}", "no frontmatter — staleness cannot be checked")
                continue
            at = fm.get("last_updated_at_phase")
            if not at:
                warn(f"Project_Context/{f.name}", "no `last_updated_at_phase`")
            elif at == "Seeding Phase":
                pass   # sentinel from project-knowledge `initialize` — no phase yet, not stale
            elif at != current_initiative:
                warn(f"Project_Context/{f.name}", f"last updated at {at!r}, current phase is {current_initiative!r}")

    # --- report ---
    for label, items in (("ERROR", ERRORS), ("WARN", WARNS), ("NOTE", NOTES)):
        if items:
            print(f"\n{label} ({len(items)})")
            for p, m in items:
                print(f"  {p}\n      {m}")
    if not ERRORS and not WARNS:
        print("clean" if not NOTES else "clean (notes only)")
    print(f"\n{len(ERRORS)} error(s), {len(WARNS)} warning(s), {len(NOTES)} note(s)")
    return 1 if ERRORS else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
