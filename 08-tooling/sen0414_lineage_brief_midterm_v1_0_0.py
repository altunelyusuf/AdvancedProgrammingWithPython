#!/usr/bin/env python3
"""sen0414_lineage_brief_midterm v1_0_0 - writes the executor briefs of the Friday-standard work for SEN0414 chapters 1 to 7 (chapter 8 is done).
One brief per chapter (deck + manifest + page together). Facts are read from the repository at run time (newest files, measured logs).
Usage: sen0414_lineage_brief_midterm_v1_0_0.py [OUTDIR]   (default 08-tooling/briefs/midterm/r1)"""
__version__ = "1.0.0"
import glob, json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.dirname(here)
TITLE = {"01": "Python Basics", "02": "Flow Control", "03": "Loops", "04": "Functions", "05": "Debugging", "06": "Lists", "07": "Dictionaries"}
HOURS = {"01": 4.5, "02": 3.5, "03": 3.5, "04": 4.0, "05": 4.0, "06": 3.0, "07": 4.5}
def newest(pat):
    f = sorted(glob.glob(os.path.join(repo, pat)), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]] if re.findall(r"_v(\d+)_(\d+)_(\d+)", p) else [0])
    return os.path.relpath(f[-1], repo) if f else "(none)"
def nextv(p):
    m = re.search(r"_v(\d+)_(\d+)_(\d+)", p); return "v%s_%d_0" % (m.group(1), int(m.group(2)) + 1) if m else "?"
def gap(n):
    out = []
    for lg, tag in (("control-u8-logs/deckcheck_ch01_08/deckcheck_ch%s_run1.log" % n, "deck check v1.1.0"), ("control-u8-logs/fitgap_ch01_08/controller_deck_ch%s.log" % n, "controller C1-C8")):
        p = os.path.join(here, lg)
        if os.path.exists(p):
            for l in open(p, encoding="utf-8", errors="replace"):
                if l.startswith(("[FAIL]", "D3 FAIL", "D5 FAIL", "M1 FAIL", "D2 FAIL", "SUMMARY")): out.append("- %s: %s" % (tag, l.strip()[:230]))
    return "\n".join(out)
COMMON = """## Why this work exists
The Owner (12:13 and 12:26 Istanbul, 2026-11-01, recorded as relayed): the slides and the interactive page of the midterm chapters must reach the quality of the Chapter 8 work of Friday 2026-10-30, and the slide code must match the page's Chapter Examples tab. 'Simplify the tasks of the agents to concentrate on the issues we have solved on Friday, and pass the useless effort spent to remeasure the already succeeded parts.'

## The Friday fixes, and only these (copy how Chapter 8 did each; do not invent a new method)
1. No `>>>` and no `...` prompt in any slide code box, note or page code the student copies. (The small brand-mark text box `>>>` in the corner of content slides stays exactly as it is.) Show a script; show its output separately as the result visual. Every result shown comes from really running the code.
2. No lambda anywhere (slides, notes, manifest, page chapter-code tab, Playground starter, exercises, exam items, answers) unless the chapter teaches lambda (it does not unless its research says so; if you find it does, STOP and tell the coordinator). Use a def function or a method reference.
3. Python indented per the standard: four spaces per level, a body line deeper than its header, no tabs, no one-line compound statements, no wrapped lines (widen the box). Every box compiles (`ast.parse`); a deliberate-error box says so on the slide and in the manifest.
4. The slides teach alone: for every concept, short full sentences (no text box over 30 words), an everyday analogy, a drawn diagram or native chart, the code, and its executed result as a visual. The page already explains well with visualisations: bring that teaching into the deck.
5. 5N1K as storytelling: who, what, when, where, why and how as connected natural sentences with real names, dates and places, a real free-licence picture (provenance in the assets file) and a live link. No label words (WHO, WHAT, ...) at line starts, no `WHAT:` forms, no heading that spells out the six questions.
6. Speaker notes 40 to 60 words on every slide (title and divider slides 25 to 60): what to tell, one example, one question for the class.
7. Slide code = one page tab: the new manifest `chapter_code_chNN_<new>.json` lists the deck's code boxes by NAME in slide order; the page's Chapter Examples tab equals it in text and order. PUSH THE MANIFEST FIRST (within about 45 minutes of your start); after that its examples change only by a new manifest version you announce.
8. Page on template `08-tooling/course_page_template_v9_53_1.html` (the Chapter 8 template: full screen and a user-resizable panel for EVERY diagram, controls never covering a figure, zoom and text-size kept) with a Lecture tab matching the deck (as the Chapter 8 page v9_92_1 has), clean layout, usable on phones.

## How to work (reuse, do not rebuild)
- Chapter 8 is your model: deck `03-materials/ch08/SEN0414_Ch08_Strings_3e_v2_1_0.pptx` and its generator `08-tooling/ch08-deck/` (v2_1_0 files), manifest `03-materials/ch08/page/chapter_code_ch08_v1_1_0.json`, page `03-materials/ch08/page/sen0414_ch08_page_v9_92_1.html` with its data `08-tooling/ch08-page/` (page_data_v9_92_1.json, corpus_manifest_v9_92_1.json, playground_width_check_v9_92_0.py, diag_audit_run_v9_92_0.py, fixtures_9_38_0) and the page builders it used (read the git log `git log --oneline | grep -i "chapter 8"` and the commits of tasks TK_U8_Deck_Build and TK_U8_Page_Build to see exactly what was changed).
- Existing tools, all unchanged and reused: deck check `08-tooling/sen0414_deck_standard_check_v1_1_0.py`, teaching check `08-tooling/sen0414_deck_teaching_check_v1_0_0.py`, overlap check `08-tooling/sen0414_deck_overlap_check_v1_0_0.py`, page tests `08-tooling/sen0414_page_test_v9_37_0.py` and `v9_38_0.py` (under `flock /tmp/page_test.lock`), leak probe v1_3_0, story-layout probe, chapter check `08-tooling/sen0414_lineage_chapter_check_v1_2_0.py`. New files for this chapter (generator, data, manifest, page) are NEW versions; no committed file is edited. Gates are never weakened; NOT_MEASURED and CANNOT_RUN are not passes.
- Do NOT re-measure what already passes and do not write new checks. Fix the failing items below; then run the existing gates ONCE on your final files and report the output exactly as printed (a FAIL stays a FAIL; if the page test fails, fix the cause and run again, reporting every run).
- Content that already passes (research, stories, pictures, analogies, diagrams, quiz, resources) is kept and adapted, not re-created.

## Rules of an executor
- You are an EXECUTOR session. Do the one task below. You do NOT touch the register (07-lineage); the lineage agent records your start and controls your result by its own re-runs.
- First `git pull --rebase --autostash` in /home/claude/AdvancedProgrammingWithPython. You commit ONLY your own new files (your chapter's folders and your own new tool files named with your chapter), never `git add -A`; message ends with the task identifier in parentheses; before each push `git pull --rebase --autostash`, and on a rejected push pull --rebase and push again (never force). Commit and push each verified step at once: the repository is the only record if the container restarts.
- Several executors run at the same time on 2 shared cores and a small disk (about 1.1 GB free): no heavy parallel runs; page tests only under `flock /tmp/page_test.lock`; delete your own scratch and temporary folders as soon as you no longer need them; STOP and report if free space falls under 0.8 GB.
- Wait inside your turn for results; never schedule a wake-up. Never invent a term, fact or source. No personal data of students.
- STOP and report, without working around it, if: the task needs a committed file edited; a gate fails and you cannot fix it within your task; anything here contradicts what you find.
- Final report to the coordinator: commit SHAs, new files, the verbatim output of every gate you ran, achieved / not achieved in plain words.
"""
def brief(n):
    deck = newest("03-materials/ch%s/SEN0414_Ch%s_*.pptx" % (n, n)); page = newest("03-materials/ch%s/page/sen0414_ch%s_page_v*.html" % (n, n)); man = newest("03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (n, n))
    nd, np_, nm = nextv(deck), nextv(page), nextv(man)
    return """# Brief for the executor session SEN0414-MS-ch%(n)s

Task TK_MS_Ch%(n)s_Build (story ST_MS_Ch%(n)s), written by the lineage agent for the Owner's midterm scope. Executor session name: **SEN0414-MS-ch%(n)s**. Estimated %(h)s hours of agent work (an estimate: nobody has witnessed a start; the real start is recorded at work begun).

## The task
**Bring SEN0414 Chapter %(n)s (%(t)s) to the Chapter 8 Friday standard: new deck, new manifest, new page, as new files.**
- Newest now: deck `%(deck)s`, page `%(page)s`, manifest `%(man)s`.
- Build: the deck as the next version above the newest deck (`%(nd)s` in its name; the generator under `08-tooling/ch%(n)s-deck/` as new files), the manifest `chapter_code_ch%(n)s_%(nm)s.json`, then the page `03-materials/ch%(n)s/page/sen0414_ch%(n)s_page_%(np)s.html` with its page data, corpus manifest and builder files as new files, on template v9_53_1. Order: deck and manifest first (push the manifest early), then the page built from the manifest.

## Measured gap of the newest deck (the lineage agent's runs of 2026-11-01; fix exactly these, nothing more is asked to be re-measured)
%(gap)s
Also check by reading, not by a new tool: the page's own code (chapter-code tab, Playground starter, exercises, exam items) for `>>>` and lambda; the page does not yet have full screen or a resizable panel on every diagram (template v9_53_1 gives it) and its chapter-code tab does not equal the deck code in slide order.

## Done means (the lineage agent will run these itself on your files, once each plus the repeated page test)
- deck check v1_1_0: SUMMARY PASS=13 FAIL=0; teaching check T1 to T6 met; overlap check CLEAN; controller checks: no prompt, no lambda, indentation, no label words, notes 40 to 60 words, compile, numbered, manifest equals the deck code.
- page test 9.38.0 and 9.37.0 pass on the final page, the leak probe, Playground width probe, story-layout probe and chapter check as for Chapter 8; page code equals the manifest, name for name, in order.

%(common)s""" % dict(n=n, t=TITLE[n], h=HOURS[n], deck=deck, page=page, man=man, nd=nd, np=np_, nm=nm, gap=gap(n) or "- (see the measured logs in 08-tooling/control-u8-logs/)", common=COMMON)
if __name__ == "__main__":
    out = os.path.join(repo, sys.argv[1] if len(sys.argv) > 1 else "08-tooling/briefs/midterm/r1"); os.makedirs(out, exist_ok=True)
    idx = ["# Midterm scope: briefs for chapters 1 to 7 (chapter 8 is done)\n", "| Chapter | Session | Hours | File |", "|---|---|---|---|"]
    for n in sorted(TITLE):
        fn = "BRIEF_TK_MS_Ch%s_Build.md" % n; open(os.path.join(out, fn), "w", encoding="utf-8").write(brief(n))
        idx.append("| %s %s | SEN0414-MS-ch%s | %s | %s |" % (n, TITLE[n], n, HOURS[n], fn))
    open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n"); print("\n".join(idx))
