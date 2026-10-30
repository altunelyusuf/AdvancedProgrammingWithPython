#!/usr/bin/env python3
"""sen0414_lineage_urgent v1_0_0 - the urgency ceremony for the owner's emergency of 2026-10-30 02:28 Istanbul (2026-10-29T23:28Z): finish the Chapter 8 deck and page before 06:00 Istanbul (03:00Z).
One call writes ONE new register file (the newest + 1 minor): the urgent items (two stories, five tasks, their criteria, cases, scores, refinements; none admitted by a scope change and none
planned through change management) and then, through the framework's own recorder (backlog_urgency v1_0_0), one UrgentInterruption for each running lineage (the materials lineage holds its
started items Suspended; the exam lineage has no started item and is paused by the same record). The caller validates (backlog_validate_v1_17_0.py), commits and pushes.
Usage: sen0414_lineage_urgent_v1_0_0.py declare"""
__version__ = "1.0.0"
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W

URG = "/home/claude/altunelyusuf/backlog-roadmap-framework/03-tooling/backlog_urgency_v1_0_0.py"
NS = "http://example.org/sen0414-slides-lineage#"
WHEN = "2026-10-30 02:28 Istanbul (2026-10-29T23:28Z)"
HEAD = ("OWNER EMERGENCY INSTRUCTION of " + WHEN + ", relayed by the course coordinator and recorded as relayed (content, not a verbatim quotation): today, Friday 2026-10-30, he teaches SEN0414 Chapter 8 "
        "Strings at 14:00 Istanbul. The Chapter 8 slides and the interactive page must be finished before 06:00 Istanbul (03:00Z); he needs at least one hour to review them. 'Stop all other work and concentrate to finish them first.' ")
OWNER_DECK = (HEAD + "His complaints about the deck, from his review of the sibling course's Chapter 6 deck, to be applied to the same standard here: "
              "slides only mention concepts and a reader cannot understand a concept from the slides alone, while the interactive page explains it well with visualisations; the speaker notes are too limited; the 5N1K "
              "(who, what, when, where, why, how) is useful but labels such as 'WHAT:' are annoying, it must be human storytelling; no lambda unless the subject teaches lambda; Python source must be indented per the Python standard; "
              "no '>>>' prompts (copying is tiresome); the code examples of the slides must match one page tab, in slide order.")
OWNER_PAGE = (HEAD + "For the page: every diagram gets a full-screen option and a user-resizable panel (zoom stays, controls never cover the diagram); the code examples of the slides are reachable as one page tab in slide order; "
              "no lambda unless the subject teaches lambda; the page and the deck are matched.")
OWNER = (HEAD + "Ranked by him: (A) the deck first, (B) the page. Several agents may work in parallel. " + OWNER_DECK[len(HEAD):] + " " + OWNER_PAGE[len(HEAD):] +
         " The exam lineage's tasks and all other chapter work wait; Chapters 9 and later stay paused; the exam executors' committed results stay and are controlled later.")
RULE = ("Route: this is an URGENT INTERRUPTION (framework ruling G158), not change management: the urgent items are not admitted by any scope change, the running lineages are paused by the recorded interruption "
        "(started items Suspended and named as held), the interruption ends when the urgent items are Done or Cancelled, and each lineage resumes with an impact assessment.")

COMMON = """- You are an EXECUTOR session. You do the one task below. You do not start, finish or record any other task.
- You do NOT touch the register (07-lineage). The lineage agent writes it, records your start and runs the control after you report.
- A committed file is never edited: every output is a new file with a new version number. No existing tool, test, template, check, deck, page, research file or bank is edited. New checks are new files with fixtures of known answer.
- A FAILING RESULT IS NEVER WORKED AROUND. NOT_MEASURED, CANNOT_RUN and a skip are not passes. Report every result exactly as printed, and never weaken a gate.
- STOP and report to the coordinator, without working around it, if: the task cannot be satisfied without editing a committed file; a check fails and you cannot fix it within your task; or anything in this brief contradicts what you find."""

DECK_NOTE = """URGENT. Build the Chapter 8 (Strings and Text Editing) deck v2.1.0 as NEW files: `03-materials/ch08/SEN0414_Ch08_Strings_3e_v2_1_0.pptx`, its generator as new files named v2_1_0 in `08-tooling/ch08-deck/` (the v2_0_0 files stay as committed), and the chapter-code manifest `03-materials/ch08/page/chapter_code_ch08_v1_1_0.json`. The Owner teaches this chapter today at 14:00 Istanbul. HARD STOP: report by 01:50 UTC (date -u) with whatever is finished; say plainly what is not finished. Commit and push every verified step at once.
FIRST (within about 40 minutes of your start): write, commit and push the manifest v1_1_0 with the code examples of the new deck in slide order, each by NAME (same structure as v1_0_0). The page is built from it and waits for it. After you push it, its examples change only by a new version (v1_1_1) that you announce in your report.
THE OWNER'S COMPLAINTS about the deck v2.0.0, which this version must remove. The controller measured v2.0.0 with python-pptx on the monospace shapes: 295 code lines, of which only 2 are indented; 92 lines carry a '>>>' or '...' prompt; 3 lambdas; speaker notes average 26 words (longest 42). Required:
1. A reader must be able to understand every concept from the slides alone. The interactive page explains the chapter well with visualisations: bring that teaching into the deck. For each concept: what it is and why it exists in short full sentences, an everyday analogy, a drawn diagram or native chart that shows how it works (reuse and adapt the page's diagrams and explanations: `03-materials/ch08/page/sen0414_ch08_page_v9_91_0.html`, `08-tooling/ch08-page/page_data_v9_91_0.json`, `08-tooling/sen0414_ch08_diagrams_v*.py`, the research in `03-materials/ch08/rdodi/`), then the code, then its executed result as a visualisation. No text box over 30 words; short sentences or bullets; no long paragraphs.
2. Python source on the slides is indented per the Python standard: four spaces per level, a body line is indented deeper than its header line, no tabs, no flattened one-liners of compound statements; code lines are never wrapped (widen the block instead); coloured and commented so a student can read it. Every code box compiles with ast.parse (the only exception is a box that shows a deliberate error, which says so on the slide and in the manifest).
3. No '>>>' and no '...' prompt anywhere on a slide or in notes (the one exception is the small brand-mark text box '>>>' in the corner of each content slide, the deck's logo that the existing deck standard check uses to tell dividers from content slides; keep it exactly as in v2.0.0, it is not code and sits in no code box): show the program as a script that can be copied, and show its output separately as the result visual. Every result shown is produced by really running the code (run the examples and keep the output file, as `examples_run_v1_0_0.py` did for v2.0.0; new files).
4. No lambda anywhere (the chapter does not teach it): use a def function or a method reference such as str.lower.
5. 5N1K as human storytelling: each story slide tells who, what, when, where, why and how in natural sentences with real names, dates and places, a real picture (free-licence, with provenance in the assets file) and a live link. NO labels: v2.0.0 starts each line with 'WHO ', 'WHAT ', 'WHEN ', 'WHERE ', 'WHY ', 'HOW ' (and the Owner dislikes forms such as 'WHAT:' as well); no line of any slide or note may start with those words in capitals or carry them followed by a colon or dash, and no heading spells out the six questions. Tell the story as connected sentences.
6. Speaker notes: short but useful, 40 to 60 words on every slide except title and divider slides (25 to 60): short sentences that say what to tell, one example to give and one question to ask the class. Not thin, not paragraphs.
7. The code examples of the slides, in slide order, are exactly one page tab: the manifest lists them by name in that order and its code equals the deck's code boxes (the existing deck standard check measures this; keep it passing).
8. Keep every element of the existing deck standard (checks `08-tooling/sen0414_deck_standard_check_v1_0_0.py` D1 to D12 and `08-tooling/sen0414_deck_overlap_check_v1_0_0.py`, run unchanged): numbered slides, native chart objects (no chart pictures), a resources slide with real links (community, seminal works, tutorials, videos), one colour scheme with no dark/light switching, dividers that name their concepts, analogies for the key concepts, real pictures for the stories.
9. NEW CHECKS as NEW FILES with fixtures of known answer (do not edit the existing checks): `08-tooling/sen0414_deck_teaching_check_v1_0_0.py` with the elements T1 indentation, T2 no lambda, T3 no 5N1K label words, T4 no prompts, T5 notes length, T6 every code box compiles. Fixtures in `08-tooling/fixtures/deck_teaching_v1_0_0/` (a generated deck that is clean and one generated deck per defect, each with its expected result) and a self-test that proves each element fails on its defect and passes on the clean fixture. Run it on your deck and report the verbatim output together with the existing checks'.
Estimated 1.5 to 1.75 hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun)."""

DECK_VERIFY_NOTE = ("Control by the lineage agent on its OWN re-runs, never the executor's tool: the existing deck standard check v1_0_0 and overlap check v1_0_0 on the new deck; the controller's own checks of indentation (every line after a header line ending in a colon is indented deeper, "
                    "multiples of four spaces, no tabs), prompts, lambda, label words, notes length (40 to 60 words), compile of every code box, and the manifest against the deck's code boxes in slide order; the slides rendered to images and read slide by slide; the executor's "
                    "check run once more on its fixtures. A failing result is a result, not a pass. Estimated 0.5 hours.")

PAGE_NOTE = """URGENT. Build the Chapter 8 (Strings and Text Editing) page as a NEW file `03-materials/ch08/page/sen0414_ch08_page_v9_92_0.html`, through the real template and builder, on a NEW template file `08-tooling/course_page_template_v9_53_0.html` (a copy of 9.52.4 plus the changes below; the older templates and the pages built from them stay as committed), with its own page data, corpus manifest, starter files and builder files as NEW files under the v9_92_0 / v9_53_0 names. The Owner teaches this chapter today at 14:00 Istanbul. HARD STOP: report by 01:50 UTC (date -u) with whatever is finished; say plainly what is not finished. Commit and push every verified step at once.
The newest page is v9_91_0 (template 9.52.4). Its content, story pictures and Playground are accepted; start from them.
CHANGES REQUIRED:
1. EVERY DIAGRAM of the page (every drawn figure, chart, graph, tree or map the page shows, in every tab and in the detail card) gets a FULL-SCREEN option and a USER-RESIZABLE panel. The zoom in/out that exists stays. The controls sit in a toolbar beside or above the figure and NEVER cover the figure (measure their rectangles against the figure's). Full screen works with the Fullscreen API and falls back to a fixed overlay where the API is missing; Escape and a visible button leave it. The panel is resizable by dragging a handle with mouse and touch and by keys, within the screen, and the figure refits to the new size. The page stays usable on phones and fills large screens, the text-size control stays.
2. THE SLIDE CODE AS ONE PAGE TAB, IN SLIDE ORDER: the chapter-code tab of the page lists the examples of the new deck by NAME in the deck's slide order and each runs in the page with its result shown. The deck's manifest `03-materials/ch08/page/chapter_code_ch08_v1_1_0.json` will appear in the repository (git pull); do not guess its content and do not build the chapter-code tab before it exists (until then do items 1 and 3 and the tests). The page's code equals the manifest's code, name for name and in order (page test feature P11 measures this).
3. NO LAMBDA anywhere in the page's code (chapter-code tab, Playground starter, exercises, exam items, the answers): the chapter does not teach lambda; use a def function or a method reference such as str.lower. NO '>>>' PROMPTS in the code the student copies.
4. PAGE AND DECK MATCHED: same example names and order, same terms, same analogies and story names, same colour scheme as far as the page allows.
5. NEW TEST as a NEW FILE (never edit page test 9.37.0 or 9.34.0): page test 9.38.0 over 9.37.0 with features for item 1 (each diagram has a full-screen control and a resizable panel; the controls' rectangles do not intersect the figure's; full screen toggles on and off; a resize changes the panel size and the figure refits) and item 3 (no lambda in any code of the page), each with a fixture of known answer (a page without the feature fails). Run the old and the new tests on your final file once each under `flock /tmp/page_test.lock` (about nine minutes each; the machine has two cores shared with other sessions; the controller repeats the page test several times itself, so you need not) and report every result exactly as printed; the Chapter 6 page was unstable at the main-thread bound of test 9.37.0 (a FAIL at 210 ms, a PASS, two crashes, a FAIL at 406/2): a FAIL stays a FAIL, never retry until green without reporting every run.
6. Also run, on the final file, the leak probe v1_3_0 (seeds 1 to 5), the Playground width probe (a new file for v9_92_0 over `08-tooling/ch08-page/playground_width_check_v9_91_0.py`), the story-layout probe and the chapter check Page/Ch08, exactly as the controls of the earlier pages did, and report their output.
Estimated 1.75 hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun)."""

PAGE_VERIFY_NOTE = ("Control by the lineage agent on its OWN re-runs: the leak probe v1_3_0 (seeds 1 to 5) and the story-layout probe on the exact built file, the Playground width probe at 390, 1366 and 1400 px, the page test 9.37.0 at least five runs under the page-test lock, the page test 9.38.0 and the chapter check Page/Ch08, "
                    "the controller's own check that every diagram has a full-screen control and a resizable panel and that no control covers a figure, no lambda and no prompt in the page's code, and the chapter-code tab against the deck's manifest. A failing run is a result, not a pass: NOT_MEASURED and CANNOT_RUN are not passes. Estimated 1.2 hours.")

CTL91_NOTE = ("Control by the lineage agent on its own re-runs of the page v9_91_0 that the held repair (ex:TK_CI5_Page_Ch08_Repair) needs and that the earlier control left incomplete: the Playground width probe (a result of v9_91_0), the fifth run of the page test 9.37.0 / chapter check Page/Ch08 "
              "(four runs exist: one FAIL under load at 406 passed and 2 failed, three PASS), printed exactly as they come. The record that sets the held repair tasks Done is written at the resume of the paused lineage, not during the pause. Estimated 0.4 hours.")


def lit(s): return W.lit(s)


def story(sid, title, want, ac, tasks, deliv, obj, score, size, owner):
    return (f'ex:{sid} a backlog:Story ; rdfs:label {lit(title)}@en ; backlog:hasIdentifier "{sid}" ; backlog:hasTitle {lit(title)} ;\n'
            f'    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_U8 ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
            f'    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
            f'    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability {lit(want)} ; backlog:soThat "the instructor can teach Chapter 8 today at 14:00 Istanbul from a deck and a page that meet the written standard and teach on their own" ;\n'
            f'    backlog:satisfiesDeliverable ex:{deliv} ; backlog:pursuesObjective ex:{obj} ; backlog:hasAcceptanceCriterion ex:{ac} ;\n'
            f'    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n'
            f'    backlog:decomposesInto {", ".join("ex:" + t for t in tasks)} ;\n'
            f'    backlog:hasState backlog:Ready ; backlog:hasPriorityScore ex:{score} ;\n'
            f'    backlog:hasAuditNote {lit(owner)} ,\n        {lit(RULE)} .\n')


def task(tid, title, ttype, cat, note, deps=(), dod="ex:DoD"):
    d = (f'    backlog:dependsOn {", ".join("ex:" + x for x in deps)} ;\n') if deps else ""
    return (f'ex:{tid} a backlog:ExecutionTask ; rdfs:label {lit(title)}@en ; backlog:hasIdentifier "{tid}" ; backlog:hasTitle {lit(title)} ;\n'
            f'    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_U8 ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
            f'    backlog:hasInvestmentCategory backlog:{cat} ; backlog:hasTaskType backlog:{ttype} ; backlog:effectiveDefinitionOfDone {dod} ; backlog:hasState backlog:Ready ;\n{d}'
            f'    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n'
            f'    backlog:hasAuditNote {lit(note)} .\n')


def score(name, sid, bv, tc, rr, size, t):
    v = (bv + tc + rr) / size
    return (f'ex:{name} a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n'
            f'    backlog:hasScoreValue "{v:.2f}"^^xsd:decimal ; backlog:scoredAt "{t}"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n'
            f'    backlog:hasScoreRationale {lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Urgent item (%s): the Owner teaches Chapter 8 at 14:00 Istanbul and needs the deliverable before 06:00 Istanbul; time criticality is the maximum of the scale; the inputs come from the Owner's instruction, not from a guess." % (bv, tc, rr, size, v, "ex:" + sid))} .\n')


def criterion(ac, label, text, tools):
    return (f'ex:{ac} a backlog:AcceptanceCriterion ; rdfs:label {lit(label)}@en ; backlog:belongsToLineage ex:Lineage2 ;\n'
            f'    backlog:hasGherkinText {lit(text)} ;\n'
            f'    backlog:measuredWithTool {tools} ;\n'
            f'    backlog:measuredWithVersion "existing checks run unchanged (deck standard check v1_0_0, deck overlap check v1_0_0, page test 9.37.0, page test 9.34.0, leak probe v1_3_0, chapter check v1_1_0) and the new checks of this emergency (deck teaching check v1_0_0, page test 9.38.0), each with its fixtures of known answer; Playwright 1.56.0; python-pptx 1.0.2" ;\n'
            f'    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the controller\'s own runs" ;\n'
            f'    backlog:coveredByCase ex:TC2U_{ac.split('_')[1]}_Passes .\n')


def build():
    src = W.newest(); t0 = open(src, encoding="utf-8").read(); now = W.now()
    deck_ac = ("Emergency of " + WHEN + ": given the deck v2.0.0 of Chapter 8, when the new deck v2.1.0 is built as new files, then ALL of: (1) the deck standard check v1_0_0 and the deck overlap check v1_0_0 run unchanged report every element met; "
               "(2) the deck teaching check v1_0_0 (new file, with fixtures of known answer) reports T1 to T6 met; the controller's own independent checks agree: no code line with a '>>>' or '...' prompt, no lambda, every body line indented deeper than its header line in multiples of four spaces, "
               "no label words WHO/WHAT/WHEN/WHERE/WHY/HOW on any slide or note, every speaker note of 40 to 60 words (title and divider slides 25 to 60), every code box compiles; (3) the chapter-code manifest v1_1_0 lists the code boxes in slide order by name and equals them; "
               "(4) the slides are rendered and read: each concept is taught on the slide (what, why, an analogy, a visual), each code example has its executed result as a visual; (5) no committed file is edited; results as printed; an element that fails is named failing and the criterion has no passing result.")
    page_ac = ("Emergency of " + WHEN + ": given the page v9_91_0 of Chapter 8 and the new deck, when the new page v9_92_0 is built as new files on a new template, then ALL of: (1) the controller runs the page test 9.37.0 at least five times on the final file under the page-test lock and every run is printed (a FAIL is a FAIL); "
               "(2) the page test 9.38.0 (new file, with fixtures of known answer) reports that every diagram has a full-screen control and a resizable panel, that no control covers a figure, and that no code of the page has a lambda; the controller's own independent check agrees; "
               "(3) the chapter-code tab lists the new deck's examples by name in slide order and equals the manifest v1_1_0 (page test feature P11); (4) the leak probe v1_3_0 (seeds 1 to 5), the Playground width probe at 390, 1366 and 1400 px, the story-layout probe and the chapter check Page/Ch08 report as printed; "
               "(5) no committed file is edited; NOT_MEASURED and CANNOT_RUN are not passes; an element that fails is named failing and the criterion has no passing result.")
    out = []
    out.append(criterion("AC2U_Deck_Ch08", "The new Chapter 8 deck teaches on its own, is indented, has no prompts, no lambda and no label words, with notes of 40 to 60 words", deck_ac, "ex:TS2_DeckStdCheck, ex:TS2_DeckOverlap"))
    out.append(criterion("AC2U_Page_Ch08", "The new Chapter 8 page has a full-screen option and a resizable panel for every diagram, the deck's code as one tab in slide order, and no lambda", page_ac, "ex:TS2_PageTest36, ex:TS2_ChapterCheck"))
    for ac, lab, dc in (("AC2U_Deck_Ch08", "Run the emergency checks on the new deck and require no failure and no skip", "Deck"), ("AC2U_Page_Ch08", "Run the emergency checks on the new page and require no failure and no skip", "Page")):
        out.append(f'ex:TC2U_{ac.split("_")[1]}_Passes a backlog:TestCase ; rdfs:label {lit(lab)}@en ; backlog:belongsToLineage ex:Lineage2 ;\n'
                   f'    backlog:exercisesCriterion ex:{ac} ; backlog:coversScenario ex:Scen2S_{"D" if dc == "Deck" else "P"}_Passes ; backlog:runsOnData ex:Data2S_{"D" if dc == "Deck" else "P"}_Passing ;\n'
                   f'    backlog:hasCaseText "Run the checks of the criterion over the new files on the controller\'s own machine; they report no failure and exit 0, or the failing elements are named." .\n')
    out.append(story("ST_U8_Deck", "URGENT: the Chapter 8 deck v2.1.0 teaches each concept on its own, with indented code, no prompts and no lambda", "the deck of Chapter 8 teaches each concept on the slides themselves, with story slides told as human storytelling and fuller speaker notes", "AC2U_Deck_Ch08", ["TK_U8_Deck_Build", "TK_U8_Deck_Verify"], "Del2_StdDecks", "Obj2_StdDecks", "Score1_ST_U8_Deck", 1.75, OWNER_DECK))
    out.append(story("ST_U8_Page", "URGENT: the Chapter 8 page v9.92.0 has full-screen and resizable diagrams, the deck's code as one tab, and no lambda", "the page of Chapter 8 lets every diagram go full screen and be resized, lists the deck's code as one tab in slide order and has no lambda", "AC2U_Page_Ch08", ["TK_U8_Page_Ctl91", "TK_U8_Page_Build", "TK_U8_Page_Verify"], "Del2_StdPages", "Obj2_StdPages", "Score1_ST_U8_Page", 2.0, OWNER_PAGE))
    out.append(task("TK_U8_Deck_Build", "Build the Chapter 8 deck v2.1.0 and its code manifest v1_1_0 as new files (urgent)", "TaskType_Build", "Cat_NewCapability", DECK_NOTE))
    out.append(task("TK_U8_Deck_Verify", "Verify the Chapter 8 deck v2.1.0 on the controller's own re-runs (urgent)", "TaskType_Verify", "Cat_Compliance", DECK_VERIFY_NOTE, ["TK_U8_Deck_Build"]))
    out.append(task("TK_U8_Page_Ctl91", "Complete the control of the page v9_91_0 that the held repair needs (urgent, controller)", "TaskType_Verify", "Cat_Compliance", CTL91_NOTE))
    out.append(task("TK_U8_Page_Build", "Build the Chapter 8 page v9_92_0 on a new template as new files (urgent)", "TaskType_Build", "Cat_NewCapability", PAGE_NOTE))
    out.append(task("TK_U8_Page_Verify", "Verify the Chapter 8 page v9_92_0 on the controller's own re-runs (urgent)", "TaskType_Verify", "Cat_Compliance", PAGE_VERIFY_NOTE, ["TK_U8_Page_Build", "TK_U8_Page_Ctl91"]))
    out.append(score("Score1_ST_U8_Deck", "ST_U8_Deck", 20, 20, 5, 1.75, now))
    out.append(score("Score1_ST_U8_Page", "ST_U8_Page", 20, 20, 5, 2.0, now))
    for sid in ("ST_U8_Deck", "ST_U8_Page"):
        out.append(f'ex:Refine8_{sid} a backlog:RefinementEvent ; rdfs:label "Refinement that made {sid} ready"@en ;\n    backlog:refines ex:{sid} ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "{now}"^^xsd:dateTime ;\n'
                   f'    backlog:refinedBy backlog:Builder ;\n    backlog:hasRefinementOutcome {lit("Refined by the lineage agent from the Owner's instruction of " + WHEN + ": criterion with its checks, tasks with their requirements, estimates, a brief to be generated from the register. Startable at once; an urgent item is not planned into an iteration.")} .\n')
    tasks = ["TK_U8_Deck_Build", "TK_U8_Deck_Verify", "TK_U8_Page_Ctl91", "TK_U8_Page_Build", "TK_U8_Page_Verify"]
    for tk in tasks:
        out.append(f'ex:Refine8_{tk} a backlog:RefinementEvent ; rdfs:label "Refinement that made {tk} ready"@en ;\n    backlog:refines ex:{tk} ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "{now}"^^xsd:dateTime ;\n'
                   f'    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_U8 ;\n    backlog:hasRefinementOutcome {lit("Refined by the lineage agent from the Owner's instruction of " + WHEN + ": the requirements in the task text, the checks that will control it, an estimate; the brief is generated from the register where an executor does the work.")} .\n')
    members = ["ST_U8_Deck", "ST_U8_Page"] + tasks
    out.append(f'ex:Iter_U8 a backlog:Iteration ; rdfs:label "Urgent box: the Chapter 8 deck and page for today\'s class"@en ; backlog:hasIdentifier "Iter_U8" ; backlog:belongsToLineage ex:Lineage2 ;\n'
               f'    backlog:iterationStart "{now}"^^xsd:dateTime ; backlog:iterationEnd "2026-10-30T03:00:00"^^xsd:dateTime ;\n'
               f'    backlog:hasDurationSource {lit("Stated by the Owner, not proposed: the box ends at 06:00 Istanbul (03:00Z) on 2026-10-30 because he needs one hour to review before teaching Chapter 8 at 14:00 Istanbul. Estimates (G120, not measurements): deck 1.75 h, page 2.0 h, run in parallel by two executors; controls 0.5 h and 1.2 h plus 0.4 h for the held page v9_91_0.")} ;\n'
               f'    backlog:hasSprintGoal {lit("The Chapter 8 deck v2.1.0 and page v9_92_0 are finished as new files that teach on their own, meet the written standard and the Owner\'s complaints of 2026-10-30, and are controlled on the controller\'s own re-runs, so that the Owner can review them before 06:00 Istanbul.")} ;\n'
               f'    backlog:hasMember {", ".join("ex:" + m for m in members)} .\n')
    out.append(f'ex:PC8_Iter_U8 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of the urgent Chapter 8 box"@en ; backlog:ceremonyFor ex:Iter_U8 ; backlog:heldAt "{now}"^^xsd:dateTime ; backlog:hasWorkKind backlog:WorkKind_Planning ;\n'
               f'    backlog:includesPlanningEvent ex:Plan8_ST_U8_Deck, ex:Plan8_ST_U8_Page ;\n    rdfs:comment "Held {now} UTC by the lineage agent on the Owner\'s emergency instruction: the two urgent stories and their tasks are committed to this box; no executor has started."@en .\n')
    for sid, tks, k in (("ST_U8_Deck", ["TK_U8_Deck_Build", "TK_U8_Deck_Verify"], "D"), ("ST_U8_Page", ["TK_U8_Page_Ctl91", "TK_U8_Page_Build", "TK_U8_Page_Verify"], "P")):
        out.append(f'ex:Plan8_{sid} a backlog:PlanningEvent ; rdfs:label "Planning of {sid} into the urgent box"@en ; backlog:belongsToLineage ex:Lineage2 ;\n'
                   f'    backlog:plannedAt "{now}"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_U8 ;\n'
                   f'    backlog:plansItem ex:{sid} ; backlog:producesTask {", ".join("ex:" + x for x in tks)} ;\n    backlog:refinementProduces ex:Spec2S_{k}, ex:Scen2S_{k}_Passes, ex:Scen2S_{k}_NotClaimed .\n')
    for l in ("Lineage2", "Lineage4"):
        out.append(f'ex:{l} backlog:hasAuditNote {lit(OWNER)} .\n')
    text = t0 + "\n" + "\n".join(out)
    return W.write_new(src, text, "Urgency ceremony for the Owner's emergency of " + WHEN + " (Chapter 8 deck and page before 06:00 Istanbul): urgent stories ST_U8_Deck and ST_U8_Page with their tasks, criteria and scores; one UrgentInterruption for the materials lineage (its started items held Suspended) and one for the exam lineage; none of the urgent items is admitted by a scope change.")


def main():
    if sys.argv[1:] != ["declare"]:
        sys.exit(__doc__)
    out = build(); print(os.path.basename(out))
    until = "2026-10-30T03:00:00Z"
    reason = ("Owner's emergency of " + WHEN + ": the Chapter 8 deck and page must be finished before 06:00 Istanbul (03:00Z) because he teaches Chapter 8 at 14:00 Istanbul today and needs an hour to review; "
              "all other work, including the exam lineage's tasks and Chapters 9 and later, waits.")
    for lin in ("Lineage2", "Lineage4"):
        cmd = [sys.executable, URG, "declare", out, "--lineage", NS + lin, "--reason", reason, "--until", until,
               "--urgent", NS + "ST_U8_Deck", "--urgent", NS + "ST_U8_Page", "--urgent", NS + "TK_U8_Deck_Build", "--urgent", NS + "TK_U8_Deck_Verify",
               "--urgent", NS + "TK_U8_Page_Ctl91", "--urgent", NS + "TK_U8_Page_Build", "--urgent", NS + "TK_U8_Page_Verify"]
        r = subprocess.run(cmd, capture_output=True, text=True); print(r.stdout.strip(), r.stderr.strip())
        if r.returncode: sys.exit(r.returncode)


if __name__ == "__main__":
    main()
