#!/usr/bin/env python3
"""sen0414_control_exam v1_0_0 - the controller's structure and source checks of the exam deliverables (lineage 4). Controller tooling written by the lineage agent; the executors do not run it.
Usage: sen0414_control_exam_v1_0_0.py points_a | points_b | design        Exit 0 only when every assertion holds; an incomplete run is a result, not a pass.
Checks: the files named by the task exist and parse; every critical point cites an existing source and, for a slide or speaker note, an existing slide; a quoted fragment of a corpus or story point appears in the file;
the not-found list exists and has an entry per chapter; for the design: every decision has a reason, the kept item types are known and not dropped at the same time, the blueprint adds up (items, letters, chapters, types, share at Apply or above above 50),
the page budget and the answer-sheet geometry and the grading method are stated; no file under 03-materials is touched by the task's commits, no committed file is modified by them, and everything is committed."""
__version__ = "1.0.0"
import glob, json, os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = "04-assessment/exams"
KINDS = {"slide", "speaker_note", "corpus", "story"}
TYPES = set("mcq multi judge match order repair blank cloze predict program short write ask string graph object sparql".split())
BAD = []


def sh(*a):
    return subprocess.run(list(a), cwd=REPO, capture_output=True, text=True).stdout


def check(ok, what, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", what, ("  " + detail) if detail else ""))
    if not ok:
        BAD.append(what)


def newest(pat):
    fs = sorted(glob.glob(os.path.join(REPO, pat)), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]] if re.findall(r"_v(\d+)_(\d+)_(\d+)", p) else [0])
    return fs[-1] if fs else None


def deck_slides(path, cache={}):
    if path not in cache:
        from pptx import Presentation
        cache[path] = Presentation(path)
    return cache[path]


def points(tag, chapters):
    f = os.path.join(REPO, EX, "critical_points_%s_v1_0_0.json" % tag); nf = os.path.join(REPO, EX, "critical_points_%s_not_found_v1_0_0.md" % tag)
    check(os.path.exists(f), "the critical-points file exists", f)
    check(os.path.exists(nf), "the not-found list exists", nf)
    if not os.path.exists(f):
        return
    try:
        data = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        check(False, "the critical-points file parses", str(e)); return
    check(isinstance(data, list) and len(data) >= 4 * len(chapters), "a list with at least 4 points per chapter", "%d points" % (len(data) if isinstance(data, list) else -1))
    keys = {"chapter", "point", "why_critical", "source_file", "place", "evidence_kind"}
    bad = [i for i, d in enumerate(data) if not isinstance(d, dict) or set(d) != keys]
    check(not bad, "every point has exactly the keys %s" % sorted(keys), "bad: %s" % bad[:5])
    data = [d for d in data if isinstance(d, dict) and set(d) == keys]
    check(set(d["chapter"] for d in data) == set(chapters), "the chapters are exactly %s" % chapters, "found %s" % sorted(set(d["chapter"] for d in data)))
    check(all(d["evidence_kind"] in KINDS for d in data), "evidence_kind is one of %s" % sorted(KINDS))
    miss = [d["source_file"] for d in data if not os.path.exists(os.path.join(REPO, d["source_file"]))]
    check(not miss, "every source_file exists", "missing: %s" % miss[:5])
    badp = []
    for d in data:
        fp = os.path.join(REPO, d["source_file"])
        if not os.path.exists(fp):
            continue
        if d["evidence_kind"] in ("slide", "speaker_note"):
            try:
                n = len(deck_slides(fp).slides)
                if not (isinstance(d["place"], int) and 1 <= d["place"] <= n):
                    badp.append((d["source_file"], d["place"]))
                elif d["evidence_kind"] == "speaker_note" and not deck_slides(fp).slides[d["place"] - 1].has_notes_slide:
                    badp.append((d["source_file"], d["place"], "no notes"))
            except Exception as e:
                badp.append((d["source_file"], str(e)[:60]))
        else:
            txt = open(fp, encoding="utf-8", errors="replace").read()
            frag = str(d["place"])
            norm = lambda s: re.sub(r"\s+", " ", s)
            if len(frag) > 120 or norm(frag) not in norm(txt):
                badp.append((d["source_file"], frag[:40]))
    check(not badp, "every place exists (slide in range, notes present, fragment found in the file)", "bad: %s" % badp[:5])
    if os.path.exists(nf):
        md = open(nf, encoding="utf-8").read()
        check(all(re.search(r"(?i)chapter\s*0?%d\b" % c, md) for c in chapters), "the not-found list has a section for every chapter", "")
    tid = "TK4_Points_A" if tag.startswith("ch01") else "TK4_Points_B"
    commits(tid)


def design():
    f = os.path.join(REPO, EX, "exam_design_v1_0_0.json"); m = os.path.join(REPO, EX, "exam_design_v1_0_0.md")
    check(os.path.exists(m), "the design document exists", m); check(os.path.exists(f), "the design data exists", f)
    if not os.path.exists(f):
        return
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        check(False, "the design data parses", str(e)); return
    top = {"decisions", "item_types_kept", "item_types_dropped", "blueprint", "page_budget", "answer_sheet", "grading"}
    check(isinstance(d, dict) and top <= set(d), "the top-level keys are present", "missing: %s" % sorted(top - set(d)) if isinstance(d, dict) else "not an object")
    if not (isinstance(d, dict) and top <= set(d)):
        return
    check(len(d["decisions"]) >= 8 and all(isinstance(x, dict) and x.get("topic") and x.get("decision") and x.get("reason") for x in d["decisions"]), "at least 8 decisions, each with topic, decision and reason", "%d" % len(d["decisions"]))
    kept = [x.get("type") for x in d["item_types_kept"]]; dropped = [x.get("type") for x in d["item_types_dropped"]]
    check(kept and set(kept) <= TYPES and set(dropped) <= TYPES, "kept and dropped types are types of the page exam engine", "kept %s dropped %s" % (kept, dropped))
    check(not (set(kept) & set(dropped)) and set(kept) | set(dropped) == TYPES, "every one of the 17 engine types is either kept or dropped, none both", "undecided: %s" % sorted(TYPES - set(kept) - set(dropped)))
    check(all(x.get("why") for x in d["item_types_kept"] + d["item_types_dropped"]), "every kept or dropped type has a reason")
    b = d["blueprint"]
    try:
        n = b["items"]; lt = b["letters"]; ch = b["chapters"]; ty = b["types"]
        check(b["minutes"] == 60, "the blueprint is for 60 minutes")
        check(sum(lt.values()) > 0 and max(lt.values()) - min(lt.values()) <= 1, "the correct letters are spread evenly (counts differ by at most 1)", str(lt))
        check(sum(ch.values()) == n, "the chapter counts add up to the items", "%s vs %s" % (sum(ch.values()), n))
        check(sum(ty.values()) == n and set(ty) <= set(kept), "the type counts add up to the items and use only kept types", "%s vs %s" % (sum(ty.values()), n))
        check(50 < b["share_apply_or_above"] <= 100, "more than half of the items are at Apply or above", str(b["share_apply_or_above"]))
        check(isinstance(b["cross_chapter_items"], int) and b["cross_chapter_items"] >= 1, "cross-chapter items are planned")
    except Exception as e:
        check(False, "the blueprint has the required numbers", repr(e))
    p = d["page_budget"]
    check(isinstance(p.get("pages_per_student"), (int, float)) and p.get("reasoning"), "the page budget states pages per student and its reasoning")
    a = d["answer_sheet"]; g = a.get("geometry", {})
    check(all(a.get(k) for k in ("layout", "mark_style", "student_id_line", "version_mark")) and all(g.get(k) for k in ("markers", "cell_mm", "resolution_dpi")), "the answer sheet states layout, mark style, ID line, version mark and geometry")
    gr = d["grading"]
    check(all(gr.get(k) for k in ("read_by_machine", "read_by_hand", "unreadable_rule", "double_mark_rule", "key_application", "second_check")), "the grading method states every part")
    md = open(m, encoding="utf-8").read()
    check(len(md) > 4000 and all(w in md.lower() for w in ("reuse", "new", "page", "mistake", "grad")), "the design document is substantial and says what is reused and what is new", "%d chars" % len(md))
    commits("TK4_Design")


def commits(tid):
    cs = [c for c in sh("git", "log", "--format=%H", "--grep", tid).split()]
    check(bool(cs), "the task's commits exist (message names %s)" % tid, "%d commits" % len(cs))
    touched, modified = set(), set()
    for c in cs:
        for line in sh("git", "show", "--name-status", "--format=", c).splitlines():
            st, _, path = line.partition("\t")
            touched.add(path)
            if st.startswith("M"):
                modified.add(path)
    check(not [p for p in touched if p.startswith("03-materials/")], "no file under 03-materials is touched by the task's commits", str([p for p in touched if p.startswith("03-materials/")][:3]))
    check(not modified, "no committed file is modified by the task's commits (new versions are new files)", str(sorted(modified)[:3]))
    st = sh("git", "status", "--short", "--", EX)
    check(not st.strip(), "everything under %s is committed" % EX, st.strip()[:100])


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else ""
    if what == "points_a":
        points("ch01_04", [1, 2, 3, 4])
    elif what == "points_b":
        points("ch06_08", [6, 7, 8])
    elif what == "design":
        design()
    else:
        raise SystemExit(__doc__)
    print("RESULT %s %s (%d failed assertion(s))" % (what, "FAIL" if BAD else "PASS", len(BAD)))
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
