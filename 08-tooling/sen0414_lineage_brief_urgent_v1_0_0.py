#!/usr/bin/env python3
"""sen0414_lineage_brief_urgent v1_0_0 - renders the executor briefs of the urgent Chapter 8 work (ex:ST_U8_Deck, ex:ST_U8_Page) from the newest register. The coordinator passes a brief unedited;
the register's note on 'work begun' names the same session. A brief names only its own session and only its own requirements.
Usage: sen0414_lineage_brief_urgent_v1_0_0.py [OUTDIR]      (default 08-tooling/briefs/urgent/r1; INDEX.md lists session, task and whether it can start now)"""
__version__ = "1.0.0"
import glob, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
SESS = {"TK_U8_Deck_Build": "SEN0414-U8-deck-ch08", "TK_U8_Page_Build": "SEN0414-U8-page-ch08"}
RULES = """- You are an EXECUTOR session. You do the one task below. You do not start, finish or record any other task.
- You do NOT touch the register (07-lineage). The lineage agent writes it, records your start and runs the control after you report.
- A committed file is never edited: every output is a new file with a new version number. No existing tool, test, template, check, deck, page, research file or bank is edited. New checks are new files with fixtures of known answer.
- A FAILING RESULT IS NEVER WORKED AROUND. NOT_MEASURED, CANNOT_RUN and a skip are not passes. Report every result exactly as printed, and never weaken a gate.
- STOP and report to the coordinator, without working around it, if: the task cannot be satisfied without editing a committed file; a check fails and you cannot fix it within your task; or anything in this brief contradicts what you find.
- First `git pull --rebase --autostash` in /home/claude/AdvancedProgrammingWithPython. Commit your work to main with a clear message that ENDS with the task identifier in parentheses, for example `(TK_U8_Deck_Build)` (the controller finds your commits by it); no force push; pull --rebase before push. Commit and push each verified step at once: the repository (committed and pushed work) is the only record if a container restarts.
- The machine has 2 cores shared with other sessions: no heavy parallel runs. Every page test runs under `flock /tmp/page_test.lock` (about nine minutes each). Delete stale temporary folders of your own older than 60 minutes. The root disk is small (about 1.2 GB free): stop and report if free space falls under 0.9 GB.
- Wait inside your turn for results; never schedule a wake-up. If something keeps failing, find the root cause and write it in one sentence before you change anything.
- Never write or keep personal data of students; any example student, sheet or name is synthetic and says so.
- Never invent a term, a fact or a source: if the course does not say it, you do not write it. Where you cannot find something, say so plainly.
- Your final report to the coordinator: the commit SHAs, the new files, and the verbatim output of every check you ran; say what failed or could not be done, if anything. Plain words: achieved / not achieved."""
ASSETS = """- the chapter's deck v2.0.0: `03-materials/ch08/SEN0414_Ch08_Strings_3e_v2_0_0.pptx` (48 slides; read with python-pptx under the SYSTEM `python3`), its generator `08-tooling/ch08-deck/` (deck_build, deck_content, deck_kit, deck_visuals, examples, manifest_selfcheck, build_v2_0_0.sh), its manifest `03-materials/ch08/page/chapter_code_ch08_v1_0_0.json`, assets `03-materials/ch08/assets/` with ASSETS_PROVENANCE_v1_0_0.md;
- the chapter's newest page `03-materials/ch08/page/sen0414_ch08_page_v9_91_0.html` (template `08-tooling/course_page_template_v9_52_4.html`, builders `08-tooling/sen0414_page_build_v4_18_*.py` and `08-tooling/sen0414_page_data_v2_25_*.py`, data `08-tooling/ch08-page/`), the chapter research `03-materials/ch08/rdodi/`, the corpus `08-tooling/sen0414_ch08_corpus_base_v*.py`, stories `08-tooling/sen0414_ch08_stories_v*.py`, diagrams `08-tooling/sen0414_ch08_diagrams_v*.py`;
- the deck checks `08-tooling/sen0414_deck_standard_check_v1_0_0.py`, `08-tooling/sen0414_deck_overlap_check_v1_0_0.py`, `08-tooling/deck_notes_check_v1_0_0.py`, `deck_fit_check_v1_0_0.py`, `deck_layout_check_v1_0_0.py`; the page tests `08-tooling/sen0414_page_test_v9_37_0.py` and `v9_34_0.py` (Playwright 1.56.0; run under `flock /tmp/page_test.lock`), the leak probe `08-tooling/sen0414_exercise_leak_probe_v1_3_*.py`, the story-layout probe `08-tooling/sen0414_story_layout_probe_v*.py`, the width probes in `08-tooling/ch1*-page/`, the chapter check `08-tooling/sen0414_lineage_chapter_check_v*.py`;
- the earlier chapters' pages and decks (Chapters 1 to 7, 9 to 25) show how a finished chapter looks; copy their patterns, never their files' names."""


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
    notes = [str(n) for n in g.objects(t, B.hasAuditNote) if not str(n).startswith("Work begun")]
    owner = sorted(str(n) for n in g.objects(story, B.hasAuditNote) if str(n).startswith("OWNER EMERGENCY"))
    L = ["# Brief for the executor session %s" % SESS[tid], "",
         "Generated from the register %s. Task %s (state in the register: %s). Executor session name: **%s**. The register's note on 'work begun' for this task names this session." % (ver, tid, state(g, tid), SESS[tid]), "",
         "## Why this work exists (the Owner's emergency instruction, recorded in the register)"] + owner + ["",
         "## Rules of an executor", RULES, "",
         "## The task", "**%s**" % text(g, t, rdflib.RDFS.label), ""] + [n + "\n" for n in notes] + ["Depends on: %s" % (", ".join(deps) or "nothing"), "",
         "## The story it belongs to", "**%s**" % text(g, story, B.hasTitle), "",
         "## The criterion it satisfies (%s)" % str(crit).split("#")[1], text(g, crit, B.hasGherkinText), "",
         "## What exists now", ASSETS, "",
         "## Order of work", "You work alone on your task. Report a delay as soon as you know it. When you have committed and pushed, report to the coordinator; the lineage agent then controls your files on its own re-runs, and only after that control is the task Done."]
    open(os.path.join(out, "BRIEF_%s.md" % tid), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return ("no, after %s" % ", ".join(blocked)) if blocked else "yes, now"


def main():
    out = os.path.join(REPO, sys.argv[1] if len(sys.argv) > 1 else "08-tooling/briefs/urgent/r1"); os.makedirs(out, exist_ok=True)
    key = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
    src = sorted(glob.glob(os.path.join(REPO, "07-lineage", "sen0414_slides_lineage_v*.ttl")), key=key)[-1]
    g = rdflib.Graph(); g.parse(src, format="turtle"); ver = os.path.basename(src)
    idx = ["# Executor briefs of the urgent Chapter 8 work (generated from %s)\n" % ver, "| Task | Executor session | Can start |", "|---|---|---|"]
    for k in SESS:
        idx.append("| %s | %s | %s |" % (k, SESS[k], one(g, ver, k, out)))
    open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print(out, len(SESS), "briefs from", ver); print("\n".join(idx[3:]))


if __name__ == "__main__":
    main()
