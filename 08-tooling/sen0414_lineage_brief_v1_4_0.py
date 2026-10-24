#!/usr/bin/env python3
"""sen0414_lineage_brief v1_3_0 - generates the executor brief of ONE task (or ALL executor tasks) of Iter_18 from the register: the task, its story, its criterion with tools and versions, the owner's request,
the measured facts, the exclusion with the note that lifts it, the tools by version (each checked for existence now), and the rules of an executor. The coordinator passes a brief unedited; the register's note on
'work begun' names the same session. A brief is a rendering of the register at the version it names: nothing in it is hand-written beyond the rules and the tool list, which are constants of this file.
Modelled on the sibling's brief generator (sen0401_lineage_brief_remedy_v1_2_0.py), written for this register.
v1.1.0 (over 1.0.0): the repair tasks TK_Std_Template_R2 and TK_Std_Runner (ex:CR2_Repair2, ex:IA2_Repair2) are briefed from their own change request and impact assessment; the page-build briefs name the repair dependencies through the register.
v1.2.0 (over 1.1.0): the chapter 9 tasks (owner decision ex:CR2_Priority3) are briefed; the owner-decision change request and impact assessment are used for them.
v1.3.0 (over 1.2.0): after the controlled repairs (register 2.170.0) the page-build briefs name template 9.52.2, builder 4.18.1, runner v1_1_0 and the page test 9.36.0, and carry a CORRECTION block that overrides any mention of template 9.52.1, builder 4.18.0 or runner v1_0_0 in the register text they quote.
v1.4.0 (over 1.3.0): the task TK_Std_PageTest37 (ex:CR2_Retest37, ex:IA2_Retest37) is briefed; its brief carries a block on the 9.37.0 restatement of the chapter 6 and 9 page criteria instead of the page-build correction block. Briefs of other tasks are not regenerated.
Usage: sen0414_lineage_brief_v1_4_0.py TASK|ALL [OUTDIR]     (default 08-tooling/briefs/iter18; INDEX.md lists session, parallel group and whether the task can start now)"""
__version__ = "1.4.0"
import glob, os, re, subprocess, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
SUM = "08-tooling/briefs/iter18"
SIB = "/home/claude/sen0401/08-tooling/"
RULES = """- You are an EXECUTOR session. You do the one task below. You do not start, finish or record any other task.
- You do NOT touch the register (07-lineage). The lineage agent writes it, records your start and runs the control (re-running the checks, rendering every slide, the evidence bridge) after you report.
- A committed file is never edited: every output is a new file with a new version number. The only changes to gates, tests and templates that are allowed are the NEW files named in your task. No existing gate, test, threshold, template or criterion is edited or weakened.
- You never judge your own work with a tool you wrote: the deck check, the page test, the decks and the pages are separate sessions. A FAILING RESULT IS NEVER WORKED AROUND: no skipped feature, no raised timeout, no edited expected value. NOT_MEASURED, CANNOT_RUN and a skip are not passes.
- Report every result exactly as the tool prints it: PASS, FAIL, NOT_MEASURED, CANNOT_RUN.
- STOP and report to the coordinator, without working around it, if: the task cannot be satisfied without editing a committed file, a gate or a test beyond the named new files; a check fails and you cannot fix it within your task; or anything in this brief contradicts what you find.
- First `git pull --rebase --autostash` in /home/claude/AdvancedProgrammingWithPython. Commit your work to main with a clear message (no force push; pull --rebase before push). Commit and push each verified step at once: the repository (committed and pushed work) is the only record if a container restarts; re-verify any untracked half-written file after a restart.
- The machine has 2 cores shared with other sessions: run browser tests one at a time, never a build beside a test; delete stale /tmp/sen0414_page_test_* and other temporary folders of your own older than 60 minutes before a batch of runs (the root disk is small). A flaky main-thread budget failure (no [FAIL] feature line) may be run again up to three times, every run kept as a log; a [FAIL] line is a result.
- Your final report to the coordinator: the commit SHAs, the new files, and the verbatim output of every check you ran; say what failed, if anything.
- Owner's standing teaching-material rules (they are the criteria, not decoration): numbered slides; short sentences, no long paragraphs; explanation beside every code listing; the executed result of code shown as a visualization (native chart, table or drawn diagram); native PowerPoint charts only; an everyday analogy for each key concept; 5N1K stories (who, what, when, where, why, how) with real names, real pictures and live links; a resources slide; short speaker notes; one background scheme for the whole deck; deck and page keep a matching look; the code on the slides is exactly one page tab (the chapter-code tab) in slide order. Pages: tabs and the left tree are synchronised and the tab row is one row, no third tab level, no duplicated lists, a panel level under the groups (one concept per panel), the Playground lists names, not code, the page fits without scrolling on a desktop and adapts to phones, a text-size control, the detail card opens only on request, every diagram is zoomable, code that really runs."""
TOOLS = [("Sibling course tools to port (READ-ONLY sources, never edited)", SIB, "sen0401_deck_standard_check_v1_0_0.py, deck_overlap_check_v1_0_0.py, sen0401_page_test_v9_36_0.py, course_page_template_v9_52_1.html, sen0401_page_build_v4_15_0.py, sen0401_page_data_v2_24_0.py; the chapter-code manifest of the sibling's chapter 5 is /home/claude/sen0401/03-materials/ch05/page/chapter_code_ch05_v1_1_0.json (the shape to follow)"),
         ("Deck builders of the existing decks", "08-tooling/ch06-deck/, ch07-deck/, ch08-deck/", "deck_build / deck_plan / examples / lecture_export / fixtures / checks of each chapter; REVIEW_*.md hold the builder's own weak-spot list; chapter 6's newest deck is also 08-tooling/ch06-deck/sen0414_ch06_deck_v2_0_0.pptx"),
         ("Existing decks", "03-materials/ch06/SEN0414_Ch06_Lists_3e_v2_0_0.pptx; 03-materials/ch07/SEN0414_Ch07_Dictionaries_3e_v1_0_0.pptx; 08-tooling/ch08-deck/sen0414_ch08_deck_v1_0_0.pptx", "python-pptx 1.0.2 is installed in the system python3; the new deck of chapter 8 goes to 03-materials/ch08/"),
         ("Chapter research", "03-materials/ch06/rdodi, ch07/rdodi, ch08/rdodi", "the newest research files (chapter 6 v2_0_0, chapter 7 v1_3_0, chapter 8 v1_0_2): concept lists (the key concepts), stories, sources"),
         ("Page template (newest of this line)", "08-tooling/course_page_template_v9_50_0.html", "the template of the existing pages; 9.52.2 (a new file, made by TK_Std_Template_R2, controlled) is the template for the rebuilt pages; 9.52.1 and 9.50.0 stay byte-identical and must NOT be used (9.52.1 shows text above the header)"),
         ("Page builder / page-data builder (newest of this line)", "08-tooling/sen0414_page_build_v4_17_0.py and sen0414_page_data_v2_24_0.py", "v4_18_1 (08-tooling/sen0414_page_build_v4_18_1.py, controlled; it refuses template 9.52.1) and v2_25_0 are the builders; v4_18_0 must NOT be used for the rebuilt pages; page versions above 9_28_0; the chapter-code manifest of the chapter is read from 03-materials/chNN/page (newest chapter_code_chNN_v*.json)"),
         ("Page test (newest of this line)", "08-tooling/sen0414_page_test_v9_34_0.py", "9.36.0 (a new file, made by TK_Std_PageTest) measures the page standard (a rebuilt page declares <meta name=\"page-standard\" content=\"9.52\">); the runner is 08-tooling/sen0414_page_test_run_v1_1_0.py (it runs 9.36.0; the environment variables FORCE_STANDARD, PAGE_FILE, PAGE_DATA, PAGE_TEST_FILE are described in its docstring; v1_0_0 is the 9.34.0 runner and must NOT be used for new pages; a TEST release key replaces the instructor key, so a pass proves page logic only)"),
         ("Chapter check of the register", "08-tooling/sen0414_lineage_chapter_check_v1_1_0.py", "Research/ChNN | Deck/ChNN | Page/ChNN for chapters 7 to 12 (chapter 6 is not covered by it)"),
         ("RDODI gates / checks", "08-tooling/sen0414_rdodi_gates_v1_1_1.py, sen0414_rdodi_checks_v1_2_0.py", "the research gates the chapter check calls"),
         ("Existing pages", "03-materials/ch06/page/sen0414_ch06_page_v9_28_0.html, ch07/page/sen0414_ch07_page_v9_28_0.html, ch08/page/sen0414_ch08_page_v9_28_0.html", "the pages to rebuild (not edited); their stored results are 08-tooling/chNN-page/test_results_v9_28_0.json (chapter 6 only; read the folder for the others)")]
PRECEDENT = "git log for the chapter folders (03-materials/chNN, 08-tooling/chNN-deck, chNN-page) shows how each earlier deck and page was committed; the sibling course's repository /home/claude/sen0401 holds the finished chapter 5 and 6 work to compare with (read-only)"
DECK_CHAPTER = {"06": "ch06", "07": "ch07", "08": "ch08", "09": "ch09"}


def text(g, s, p):
    return " ".join(str(o) for o in g.objects(s, p))


def state(g, x):
    return str(g.value(E[x], B.hasState)).split("#")[1]


def one(g, ver, t_id, sess, group, out):
    t = E[t_id]; assert (t, None, None) in g, t_id
    deps = sorted(str(x).split("#")[1] for x in g.objects(t, B.dependsOn))
    blocked = [d for d in deps if state(g, d) != "Done"]
    story = next(s for s in g.subjects(B.decomposesInto, t) if (s, rdflib.RDF.type, B.Story) in g)
    crit = next(g.objects(story, B.hasAcceptanceCriterion))
    tools = sorted(str(x).split("#")[1] for x in g.objects(crit, B.measuredWithTool))
    tool_files = ["%s (%s)" % (text(g, E[x], B.scriptFileName), x) for x in tools]
    t37 = str(crit).endswith("AC2R_PageTest37"); rep = str(crit).endswith(("AC2R_TemplateFix", "AC2R_Runner")); ch9 = str(crit).endswith(("AC2S_Deck_Ch09", "AC2S_Page_Ch09")); cr = E.CR2_Retest37 if t37 else (E.CR2_Repair2 if rep else (E.CR2_Priority3 if ch9 else E.CR2_Standard)); ia = E.IA2_Retest37 if t37 else (E.IA2_Repair2 if rep else (E.IA2_Priority3 if ch9 else E.IA2_Standard))
    excl = E.Excl2_NoRebuild
    L = ["# Brief for the executor session %s" % sess, "",
         "Generated from the register %s. Task %s (state in the register: %s). Parallel group: %s." % (ver, t_id, state(g, t_id), group),
         "Executor session name: **%s**. The register's note on 'work begun' for this task names this session." % sess, "",
         "## Why this work exists (the owner's request)", text(g, cr, B.hasChangeRequestRationale), "",
         "## Rules of an executor", RULES, "",
         "## CORRECTION that overrides the register text quoted below (controlled 2026-10-23, register 2.170.0)",
         "Use page template **9.52.2** (`08-tooling/course_page_template_v9_52_2.html`), page builder **4.18.1** (`08-tooling/sen0414_page_build_v4_18_1.py`), page-data builder 2.25.0, the page test **9.36.0** and the runner **v1_1_0** (`08-tooling/sen0414_page_test_run_v1_1_0.py`). Wherever the text below says template 9.52.1, builder 4.18.0 or runner v1_0_0, it is superseded: 9.52.1 closes a comment early and shows text above the header; builder 4.18.1 refuses it. Run the page test one run at a time; a failing main-thread-budget line alone under load may be run again (keep every log); any other [FAIL] is a result.", ""]
    if t37:
        L[-2:] = ["## This task makes the NEW page test 9.37.0 (register %s)" % ver,
                  "Read the page test 9.36.0 (`08-tooling/sen0414_page_test_v9_36_0.py`, never edited) and the sibling's 9.37.0 (`/home/claude/sen0401/08-tooling/sen0401_page_test_v9_37_0.py`, read-only) first. Your file is `08-tooling/sen0414_page_test_v9_37_0.py`; run it through the runner `08-tooling/sen0414_page_test_run_v1_1_0.py` with `PAGE_TEST_FILE=sen0414_page_test_v9_37_0.py`. The pages of chapters 7 and 8 (v9_90_0, template 9.52.2) passed 9.36.0 and must pass 9.37.0 the same way; the page of chapter 6 (v9_90_0, commits a3fde89, ff8dedf, ae0ba44) exposed the defects (log `08-tooling/ch06-page/logs_iter18/page_test_9_36_0_run1.log`). Run page tests one at a time under `flock /tmp/page_test.lock`: the queue is shared with the other executors.", ""]
    if blocked:
        L += ["## Do not start until", "Task(s) %s are Done in the register (the lineage agent controls them and tells the coordinator)." % ", ".join(blocked), ""]
    L += ["## The task", "**%s**" % text(g, t, rdflib.RDFS.label), "", text(g, t, B.hasAuditNote), "", "Depends on: %s" % (", ".join(deps) or "nothing"), "",
          "## The story it belongs to", "**%s**" % text(g, story, B.hasTitle), "",
          "## The criterion it satisfies (%s)" % str(crit).split("#")[1], "**%s**" % text(g, crit, rdflib.RDFS.label), "", text(g, crit, B.hasGherkinText), "",
          "Measured with (register, G136): %s. Versions: %s" % (", ".join(tool_files), text(g, crit, B.measuredWithVersion)), "",
          "## What the scope excludes, and what is lifted for this work",
          "- **%s**: %s" % (text(g, excl, rdflib.RDFS.label), text(g, excl, B.excludesConcern)),
          "  Notes: %s" % " | ".join(str(cm) for cm in g.objects(excl, rdflib.RDFS.comment) if "Lifted" in str(cm)), "",
          "## Tools and gates, by version"]
    for name, path, how in TOOLS:
        paths = [p.strip().rstrip(",;") for p in re.split(r" and |, |; ", path) if "/" in p or p.strip().endswith((".py", ".html", ".pptx"))]
        miss = [p for p in paths if p.startswith(("03-", "08-")) and not glob.glob(os.path.join(REPO, p.rstrip("/")))]
        L.append("- %s: `%s` - %s%s" % (name, path, how, (" (**not found at this path now: %s; it may be a file another task creates**)" % ", ".join(miss)) if miss else ""))
    L += ["", "## Precedents", "- " + PRECEDENT, "",
          "## Measured facts, the written standard and the plan (impact assessment ex:IA2_Standard)", text(g, ia, B.hasImpactStatement), "",
          "## Order of work", "Tooling first: TK_Std_DeckCheck, TK_Std_PageTest and TK_Std_Template (three executors, in parallel, together with the three deck builds). Then the lineage agent verifies; a page build starts only when the template, the page test and the chapter's deck verification are Done in the register. "
          "Chapter 6 first, then 7, then 8; each chapter ships as soon as it is controlled. Your own estimate in the task text is an estimate; report a delay as soon as you know it."]
    open(os.path.join(out, "BRIEF_%s.md" % t_id), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return ("no, after %s" % ", ".join(blocked)) if blocked else "yes, now"


EXEC_TASKS = [("TK_Std_DeckCheck", "SEN0414-I18-deckcheck", "A tooling"), ("TK_Std_PageTest", "SEN0414-I18-pagetest", "A tooling"), ("TK_Std_Template", "SEN0414-I18-template", "A tooling"),
              ("TK_Std_Deck_Ch06_Build", "SEN0414-I18-deck-ch06", "B chapter 6"), ("TK_Std_Deck_Ch07_Build", "SEN0414-I18-deck-ch07", "B chapter 7"), ("TK_Std_Deck_Ch08_Build", "SEN0414-I18-deck-ch08", "B chapter 8"),
              ("TK_Std_Page_Ch06_Build", "SEN0414-I18-page-ch06", "C chapter 6 page"), ("TK_Std_Page_Ch07_Build", "SEN0414-I18-page-ch07", "C chapter 7 page"), ("TK_Std_Page_Ch08_Build", "SEN0414-I18-page-ch08", "C chapter 8 page"),
              ("TK_Std_Deck_Ch09_Build", "SEN0414-I18-deck-ch09", "B chapter 9"), ("TK_Std_Page_Ch09_Build", "SEN0414-I18-page-ch09", "C chapter 9 page"),
              ("TK_Std_Template_R2", "SEN0414-I18-template-r2", "D repair: template"), ("TK_Std_Runner", "SEN0414-I18-runner", "D repair: runner"),
              ("TK_Std_PageTest37", "SEN0414-I18-pagetest37", "D repair: page test 9.37.0")]


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "ALL"
    out = os.path.join(REPO, sys.argv[2] if len(sys.argv) > 2 else SUM); os.makedirs(out, exist_ok=True)
    key = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
    src = sorted(glob.glob(os.path.join(REPO, "07-lineage", "sen0414_slides_lineage_v*.ttl")), key=key)[-1]
    g = rdflib.Graph(); g.parse(src, format="turtle"); ver = os.path.basename(src)
    todo = [x for x in EXEC_TASKS if only in ("ALL", x[0])]
    assert todo, only
    idx = ["# Executor briefs of Iteration 18: the chapter 6, 7 and 8 decks and pages to the written standard (generated from %s)\n" % ver,
           "The Verify and Regress tasks have no executor: the lineage agent controls them (re-runs the checks, renders every slide, runs the evidence bridge) after the executors report. Briefs are passed to the executors unedited.\n",
           "| Task | Executor session | Group | Can start |", "|---|---|---|---|"]
    for tid, sess, grp in todo:
        can = one(g, ver, tid, sess, grp, out)
        idx.append("| %s | %s | %s | %s |" % (tid, sess, grp, can))
    open(os.path.join(out, "INDEX.md" if only == "ALL" else "INDEX_%s.md" % only), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print(out, len(todo), "briefs from", ver); print("\n".join(idx[4:]))


main()
