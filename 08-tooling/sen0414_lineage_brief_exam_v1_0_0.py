#!/usr/bin/env python3
"""sen0414_lineage_brief_exam v1_0_0 - renders the executor briefs of the exam lineage (ex:Lineage4) from the register. The coordinator passes a brief unedited; the register's note on 'work begun' names the same session.
A brief names only its own session and only its own requirements: no other session, no other lineage's work.
Usage: sen0414_lineage_brief_exam_v1_0_0.py TASK|ALL [OUTDIR]      (default 08-tooling/briefs/exam/r1; INDEX.md lists the session and whether the task can start now)"""
__version__ = "1.0.0"
import glob, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
SESS = {"TK4_Points_A": "SEN0414-EX-points-ch01-04", "TK4_Points_B": "SEN0414-EX-points-ch06-08", "TK4_Design": "SEN0414-EX-design"}
RULES = """- You are an EXECUTOR session. You do the one task below. You do not start, finish or record any other task.
- You do NOT touch the register (07-lineage). The lineage agent writes it, records your start and runs the control after you report.
- A committed file is never edited: every output is a new file with a new version number. No existing tool, test, template, deck, page, research file or bank is edited.
- A FAILING RESULT IS NEVER WORKED AROUND. NOT_MEASURED, CANNOT_RUN and a skip are not passes. Report every result exactly as printed.
- STOP and report to the coordinator, without working around it, if: the task cannot be satisfied without editing a committed file; a check fails and you cannot fix it within your task; or anything in this brief contradicts what you find.
- First `git pull --rebase --autostash` in /home/claude/AdvancedProgrammingWithPython. Commit your work to main with a clear message that ENDS with the task identifier in parentheses, for example `(TK4_Points_A)` (the controller finds your commits by it); no force push; pull --rebase before push. Commit and push each verified step at once: the repository (committed and pushed work) is the only record if a container restarts.
- The machine has 2 cores shared with other sessions: do not start heavy parallel runs; delete stale temporary folders of your own older than 60 minutes (the root disk is small).
- Never write or keep personal data of students; any example student, sheet or name is synthetic and says so.
- Never invent a term, a fact or a source: if the course does not say it, you do not write it. Where you cannot find something, say so plainly in the place the task names for it.
- Your final report to the coordinator: the commit SHAs, the new files, and the verbatim output of every check you ran; say what failed or could not be found, if anything."""
ASSETS = """- decks of the chapters: `03-materials/chNN/SEN0414_ChNN_*_3e_vX_Y_Z.pptx` (take the newest version of each chapter; speaker notes are in the slides' notes pages; read with python-pptx under the SYSTEM `python3`);
- corpus and stories of the chapters: `08-tooling/sen0414_chNN_corpus_v*.py` and `08-tooling/sen0414_chNN_stories_v*.py` (newest of each); research files: `03-materials/chNN/rdodi/`; chapter-code manifests: `03-materials/chNN/page/chapter_code_chNN_v1_0_0.json`;
- the interactive pages' exam engine: `08-tooling/template_exam_v9_19_0.js` and the exam code in the page template `08-tooling/course_page_template_v9_52_4.html` (17 item types: mcq, multi, judge, match, order, repair, blank, cloze, predict, program, short, write, ask, string, graph, object, sparql; exam codes M- and F-; about 19 to 20 questions; chapter specific);
- the Exam desk `08-tooling/sen0414_exam_desk_v2_2_0.html` (builder `08-tooling/sen0414_exam_desk_build_v2_2_0.py`), the release tool `08-tooling/sen0414_exam_release_v1_0_0.py`, the exam tests `08-tooling/sen0414_exam_test_v1_1_0.py` and `08-tooling/sen0414_exam_questions_test_v1_0_0.py`;
- the chapter question banks: `08-tooling/chNN-page/question_bank_v1_1_0.json` (967 multiple-choice items for chapters 1 to 8; correct letters spread evenly; only 403 of them (42 per cent) at Apply or Analyze, none at Evaluate or Create; no fill-in and no open items) with their make and check tools in the same folders;
- the assessment ontology `04-assessment/sen0414_assessment_v1_0_0.ttl` (weights only: midterm 30 per cent; no items).
Nothing exists yet that: marks the critical points the instructor stressed; builds a paper across chapters; lays out a printed paper, a printed key or an answer sheet; reads or grades a handed-in paper."""


def text(g, s, p):
    return " ".join(str(o) for o in g.objects(s, p))


def state(g, x):
    return str(g.value(E[x], B.hasState)).split("#")[1]


def one(g, ver, tid, out):
    t = E[tid]; assert (t, None, None) in g, tid
    deps = sorted(str(x).split("#")[1] for x in g.objects(t, B.dependsOn))
    blocked = [d for d in deps if state(g, d) != "Done"]
    story = next(s for s in g.subjects(B.decomposesInto, t) if (s, rdflib.RDF.type, B.Story) in g)
    crit = next(g.objects(story, B.hasAcceptanceCriterion))
    lin = E.Lineage4; mis = E.Mission4; sc = E.Scope4
    notes = [str(n) for n in g.objects(t, B.hasAuditNote) if not str(n).startswith("Work begun")]
    owner = [str(n) for n in g.objects(mis, B.hasAuditNote)]
    L = ["# Brief for the executor session %s" % SESS[tid], "",
         "Generated from the register %s. Task %s (state in the register: %s). Executor session name: **%s**. The register's note on 'work begun' for this task names this session." % (ver, tid, state(g, tid), SESS[tid]), "",
         "## Why this work exists (the Owner's mission, accepted 2026-10-29)", text(g, mis, B.hasMissionStatement), "",
         "The Owner's statements that bound the work (recorded in the register):"] + ["- " + n for n in owner[:2]] + ["",
         "## Rules of an executor", RULES, ""]
    if blocked:
        L += ["## Do not start until", "Task(s) %s are Done in the register (the lineage agent controls them and tells the coordinator)." % ", ".join(blocked), ""]
    L += ["## The task", "**%s**" % text(g, t, rdflib.RDFS.label), ""] + [n + "\n" for n in notes] + ["Depends on: %s" % (", ".join(deps) or "nothing"), "",
          "## The story it belongs to", "**%s**" % text(g, story, B.hasTitle), "",
          "## The criterion it satisfies (%s)" % str(crit).split("#")[1], text(g, crit, B.hasGherkinText), "",
          "## What the scope includes and excludes", text(g, sc, B.hasScopeStatementText), "",
          "## What exists now", ASSETS, "",
          "## Order of work", "You work alone on your task. Your own estimate in the task text is an estimate; report a delay as soon as you know it. When you have committed and pushed, report to the coordinator; the lineage agent then controls your files on its own re-runs, and only after that control is the task Done."]
    open(os.path.join(out, "BRIEF_%s.md" % tid), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return ("no, after %s" % ", ".join(blocked)) if blocked else "yes, now"


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "ALL"
    out = os.path.join(REPO, sys.argv[2] if len(sys.argv) > 2 else "08-tooling/briefs/exam/r1"); os.makedirs(out, exist_ok=True)
    key = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
    src = sorted(glob.glob(os.path.join(REPO, "07-lineage", "sen0414_slides_lineage_v*.ttl")), key=key)[-1]
    g = rdflib.Graph(); g.parse(src, format="turtle"); ver = os.path.basename(src)
    todo = [k for k in SESS if only in ("ALL", k)]; assert todo, only
    idx = ["# Executor briefs of the exam lineage (generated from %s)\n" % ver, "| Task | Executor session | Can start |", "|---|---|---|"]
    for k in todo:
        idx.append("| %s | %s | %s |" % (k, SESS[k], one(g, ver, k, out)))
    open(os.path.join(out, "INDEX.md" if only == "ALL" else "INDEX_%s.md" % only), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print(out, len(todo), "briefs from", ver); print("\n".join(idx[3:]))


if __name__ == "__main__":
    main()
