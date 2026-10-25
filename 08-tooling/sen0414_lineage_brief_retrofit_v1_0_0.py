#!/usr/bin/env python3
"""sen0414_lineage_brief_retrofit v1_0_0 - generates the executor brief of ONE task (or ALL executor tasks) of Iter_19 (the retrofit of chapters 1 to 5) from the register: the task with all its notes, its story, its criteria with tools and versions, the owner's request, the measured facts, the exclusion with the note that lifts it, the tools by version (each checked for existence now), the files that exist for the chapter, the precedents (chapters 9 and 6, with their commits), and the rules of an executor.
The coordinator passes a brief unedited; the register's note on 'work begun' names the same session. A brief is a rendering of the register at the version it names: nothing in it is hand-written beyond the rules and the tool list, which are constants of this file (the rules are read from sen0414_lineage_brief_v1_7_0.py, which is not imported because it runs on import).
Usage: sen0414_lineage_brief_retrofit_v1_0_0.py TASK|ALL [OUTDIR]     (default 08-tooling/briefs/iter19; INDEX.md lists session and whether the task can start now)"""
__version__ = "1.0.0"
import ast, glob, os, re, subprocess, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
SUM = "08-tooling/briefs/iter19"
CH = {"01": "Python Basics", "02": "Flow Control", "03": "Loops", "04": "Functions", "05": "Debugging"}


def rules():
    tree = ast.parse(open(os.path.join(REPO, "08-tooling", "sen0414_lineage_brief_v1_7_0.py"), encoding="utf-8").read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "RULES":
            return ast.literal_eval(n.value)
    raise SystemExit("RULES not found")


CURRENT = """Use these tool versions (they are the versions the controller measures with; where the register text below names older ones, these supersede it):
- page template **9.52.2** `08-tooling/course_page_template_v9_52_2.html`; page builder **4.18.1** `08-tooling/sen0414_page_build_v4_18_1.py` (it refuses template 9.52.1); page-data builder **2.25.0** `08-tooling/sen0414_page_data_v2_25_0.py`;
- page test **9.37.0** `08-tooling/sen0414_page_test_v9_37_0.py` through the runner **v1_1_0** `08-tooling/sen0414_page_test_run_v1_1_0.py`, run with the SYSTEM `python3` (it needs `cryptography`), `PAGE_TEST_FILE=sen0414_page_test_v9_37_0.py`, and page test 9.34.0 as before; EVERY page test run under `flock /tmp/page_test.lock` (one at a time on the two cores);
- deck standard check v1_0_0 `08-tooling/sen0414_deck_standard_check_v1_0_0.py NN DECK.pptx`, deck overlap check v1_0_0 `08-tooling/sen0414_deck_overlap_check_v1_0_0.py DECK.pptx` (the independent checks; run them, report as printed);
- chapter check v1_1_0 `08-tooling/sen0414_lineage_chapter_check_v1_1_0.py Research/ChNN` covers the research of chapters 1 to 5; its Deck and Page cases do NOT cover chapters 1 to 5 (they crash) and are not run for them: do not repair that tool, report that you did not run them;
- RDODI gates v1_1_1 `08-tooling/sen0414_rdodi_gates_v1_1_1.py`; generic research builder `08-tooling/sen0414_rdodi_build_v1_2_0.py`; page-ABox builder `08-tooling/sen0414_page_abox_build_v1_1_9.py` (older versions stay; write a NEW version file if you need a change);
- the chapter-code manifest of a chapter is `03-materials/chNN/page/chapter_code_chNN_v1_0_0.json` (shape: the manifest of chapter 9 or 6 in 03-materials/ch09/page and ch06/page).
Do NOT use template 9.52.1, builder 4.18.0, runner v1_0_0 or page test 9.36.0 for new work."""
PRECEDENT = ("The finished chapters are the precedent, read them before you start: chapter 9 (deck: 03-materials/ch09/SEN0414_Ch09_*_v2_0_0.pptx with its generator in 08-tooling/ch09-deck/ - deck_build_v2_0_0.py, deck_content_v2_0_0.py, deck_kit_v2_0_0.py, deck_visuals_v2_0_0.py, manifest_selfcheck_v2_0_0.py; page: 03-materials/ch09/page/sen0414_ch09_page_v9_90_0.html with its page_data and corpus manifest in 08-tooling/ch09-page; story pictures embedded with their licences recorded: 08-tooling/sen0414_ch09_stories_v1_0_0.py and the story-image data it uses), "
             "chapters 7 and 8 (the same line), and chapter 6 (page v9_90_0 and the research repair: data module 08-tooling/sen0414_ch06_rdodi_data_v2_2_0.py, page ABox 03-materials/ch06/page/sen0414_ch06_page_abox_v1_4_0.ttl; commits 0064873, 12b4bd1, f18e3da, 86d4946, c1d3615). `git log --oneline -- 03-materials/ch09 08-tooling/ch09-deck 08-tooling/ch09-page` shows how each step was committed. "
             "One lesson from chapter 6: do not drop any individual, class, link or source of the old research files without a stated reason; compare the old and new sets with a script before you report. One layout lesson from chapter 9: the first story photograph must not fill the viewport height, so that the story text is reachable without scrolling past it.")


def text(g, s, p):
    return " ".join(str(o) for o in g.objects(s, p))


def state(g, x):
    return str(g.value(E[x], B.hasState)).split("#")[1]


def sh(*a):
    return subprocess.run(list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()


def exists_now(tool_text):
    paths = re.findall(r"`(08-tooling/[^`\s]+)`", tool_text)
    return [p for p in paths if "NN" not in p and "*" not in p and not glob.glob(os.path.join(REPO, p))]


def assets(ch):
    L = []
    for pat, what in (("03-materials/ch%s/*.pptx" % ch, "decks"), ("03-materials/ch%s/rdodi/*" % ch, "research files"), ("03-materials/ch%s/page/*" % ch, "page files"), ("03-materials/ch%s/assets/*" % ch, "assets"), ("08-tooling/ch%s-deck/*" % ch, "deck builders and checks"),
                      ("08-tooling/sen0414_ch%s_*" % ch, "chapter tools (corpus, data module, stories)")):
        fs = sorted(os.path.relpath(f, REPO) for f in glob.glob(os.path.join(REPO, pat)))
        if what in ("page files", "deck builders and checks") and len(fs) > 14:
            fs = fs[:4] + ["... (%d more)" % (len(fs) - 8)] + fs[-4:]
        L.append("- %s: %s" % (what, ", ".join("`%s`" % f for f in fs) if fs else "none"))
    return "\n".join(L)


def one(g, ver, t_id, sess, ch, kind, out):
    t = E[t_id]; assert (t, None, None) in g, t_id
    deps = sorted(str(x).split("#")[1] for x in g.objects(t, B.dependsOn))
    blocked = [d for d in deps if state(g, d) != "Done"]
    story = next(s for s in g.subjects(B.decomposesInto, t) if (s, rdflib.RDF.type, B.Story) in g)
    crits = [c for c in g.objects(story, B.hasAcceptanceCriterion) if (kind == "research") == str(c).endswith("RetrofitResearch")]
    cr = E.CR2_Iter19; ia = E.IA2_Iter19
    notes = [str(n) for n in g.objects(t, B.hasAuditNote) if not str(n).startswith("Work begun")]
    # the standard text (longest) first, the facts after
    notes.sort(key=lambda s: (s.startswith("Facts for this task"), -len(s)))
    excl = E.Excl2_NoRebuild
    lifts = [str(c) for c in g.objects(excl, rdflib.RDFS.comment) if "chapters 1 to 5" in str(c)]
    L = ["# Brief for the executor session %s" % sess, "",
         "Generated from the register %s. Task %s (state in the register: %s). Chapter %s (%s). Executor session name: **%s**. The register's note on 'work begun' for this task names this session." % (ver, t_id, state(g, t_id), ch, CH[ch], sess), "",
         "## Why this work exists (the owner's request)", text(g, cr, B.hasChangeRequestRationale), "",
         "## Rules of an executor", rules(), "",
         "## The tool versions to use", CURRENT, ""]
    if blocked:
        L += ["## Do not start until", "Task(s) %s are Done in the register (the lineage agent controls them and tells the coordinator)." % ", ".join(blocked), ""]
    L += ["## The task", "**%s**" % text(g, t, rdflib.RDFS.label), ""] + [n + "\n" for n in notes] + ["Depends on: %s" % (", ".join(deps) or "nothing"), "",
          "## The story it belongs to", "**%s**" % text(g, story, B.hasTitle), ""]
    for crit in crits:
        tools = sorted(str(x).split("#")[1] for x in g.objects(crit, B.measuredWithTool))
        L += ["## The criterion it satisfies (%s)" % str(crit).split("#")[1], "**%s**" % text(g, crit, rdflib.RDFS.label), "", text(g, crit, B.hasGherkinText), "",
              "Measured with (register, G136): %s. Versions: %s" % (", ".join("%s (%s)" % (text(g, E[x], B.scriptFileName), x) for x in tools), text(g, crit, B.measuredWithVersion)), ""]
    L += ["## What the scope excludes, and what is lifted for this work",
          "- **%s**: %s" % (text(g, excl, rdflib.RDFS.label), text(g, excl, B.excludesConcern)), "  Lifted for this work: %s" % " | ".join(lifts), "",
          "## What exists for chapter %s now" % ch, assets(ch), "",
          "## Precedents", PRECEDENT, "",
          "## Measured facts, gaps said openly and the plan (impact assessment ex:IA2_Iter19)", text(g, ia, B.hasImpactStatement), "",
          "## Order of work", "Chapter %s of the retrofit: the deck first, then its control by the lineage agent, then the page, then the research set with the page ABox of the new page, then their controls. Chapter 1 is first of the five; chapters 2 to 5 follow in the owner's order, and decks and research sets of different chapters may be built side by side, but browser tests run one at a time under the lock. Your own estimate in the task text is an estimate; report a delay as soon as you know it." % ch]
    open(os.path.join(out, "BRIEF_%s.md" % t_id), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return ("no, after %s" % ", ".join(blocked)) if blocked else "yes, now"


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "ALL"
    out = os.path.join(REPO, sys.argv[2] if len(sys.argv) > 2 else SUM); os.makedirs(out, exist_ok=True)
    key = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
    src = sorted(glob.glob(os.path.join(REPO, "07-lineage", "sen0414_slides_lineage_v*.ttl")), key=key)[-1]
    g = rdflib.Graph(); g.parse(src, format="turtle"); ver = os.path.basename(src)
    todo = [("TK_Ret_Ch%s_%s" % (c, k), "SEN0414-I19-%s-ch%s" % (s, c), c, kind) for c in CH for k, s, kind in (("Deck_Build", "deck", "deck"), ("Page_Build", "page", "page"), ("Research", "research", "research"))]
    todo = [x for x in todo if only in ("ALL", x[0])]; assert todo, only
    idx = ["# Executor briefs of Iteration 19: the retrofit of chapters 1 to 5 (generated from %s)\n" % ver,
           "The Verify tasks have no executor: the lineage agent controls them (re-runs the checks, renders every slide, runs the evidence bridge) after the executors report. Briefs are passed to the executors unedited.\n",
           "| Task | Executor session | Can start |", "|---|---|---|"]
    for tid, sess, c, kind in todo:
        idx.append("| %s | %s | %s |" % (tid, sess, one(g, ver, tid, sess, c, kind, out)))
    open(os.path.join(out, "INDEX.md" if only == "ALL" else "INDEX_%s.md" % only), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print(out, len(todo), "briefs from", ver); print("\n".join(idx[4:]))


if __name__ == "__main__":
    main()
