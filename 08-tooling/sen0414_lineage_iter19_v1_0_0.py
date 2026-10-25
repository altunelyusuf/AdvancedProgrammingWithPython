#!/usr/bin/env python3
"""sen0414_lineage_iter19 v1_0_0 - change route: PLAN Iteration 19 of the second lineage (the retrofit of chapters 1 to 5 to the written standard), as released by the owner's decision of 2026-10-23 (ex:CR2_Priority3: after chapters 7, 8 and 9, return to ALL chapters starting with chapter 1) and the course coordinator's direction of 2026-10-25 (close Iter_18, then plan and start the retrofit from chapter 1 by the change route, re-rank the open items, brief the executors, do not wait for the owner).
What the planning does (facts measured by the lineage agent on 2026-10-25, see FACTS): the five retrofit stories of chapters 1 to 5 become Ready, scored (WSJF) and decomposed into six tasks each (deck build, deck verify, page build, research set and page ABox, research verify, page verify);
chapters 10 to 25, the remaining-chapters story and the Cross.B gap story move to a new unstarted Iter_20 (they stay planned, unscored); the planned retrofit criterion is restated and one criterion is added for the research set (the chapter check Research/ChNN fails for every chapter 1 to 5 on the page ABox, the same defect chapter 6 had).
No rebaseline is written (an owner decision). No work is begun by this route: work begun is recorded at the real start of each executor session.
Events, one new register file each:  change | retract | backlog PREV | fill PREV.   Usage: sen0414_lineage_iter19_v1_0_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.0.0"
import datetime, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S; lit = W.lit; now = W.now
CR = "ex:CR2_Iter19"; IA = "ex:IA2_Iter19"; REV = "ex:Revision_Lineage2_Backlog9"
OLD = "ex:Out2_BacklogR8"; NEW = "ex:Out2_BacklogR9"
CH = {"01": "Python Basics", "02": "Flow Control", "03": "Loops", "04": "Functions", "05": "Debugging"}
TC = {"01": 20, "02": 16, "03": 13, "04": 10, "05": 8}            # time criticality: the owner's order of chapters
DECKFAIL = {"01": 8, "02": 8, "03": 8, "04": 8, "05": 9}          # deck standard elements failing, measured
RESFAIL = {"01": 2, "02": 2, "03": 2, "04": 2, "05": 2}           # research gates failing (Stage4.cov, Stage4.sub), measured
EST = {"Deck_Build": 5.0, "Deck_Verify": 0.5, "Page_Build": 3.5, "Research": 4.0, "Research_Verify": 0.5, "Page_Verify": 1.0}
SIZE = sum(EST.values())
FACT = {
    "01": "CHAPTER 1 (Python Basics) as it stands: research 03-materials/ch01/rdodi (document v1_2_0, domain TBox v1_1_1, ABox v1_1_1, SHACL v1_0_1, research v1_1_0; there is NO data module for chapter 1 in 08-tooling, only the corpus sen0414_ch01_corpus_v1_2_0.py: write the data module like chapter 7 v1_3_0 from the corpus); newest deck 03-materials/ch01/SEN0414_Ch01_PythonBasics_3e_v3_0_0.pptx (builder deck_build_v3_0_0.py in 08-tooling/ch01-deck/); newest page 03-materials/ch01/page/sen0414_ch01_page_v9_28_0.html with page ABox v9_4_2; stories 08-tooling/sen0414_ch01_stories_v1_0_0.py; the first-program example of the old deck is 08-tooling/ch01-deck/first_program_v1_0_1.py.",
    "02": "CHAPTER 2 (Flow Control) as it stands: research 03-materials/ch02/rdodi (document v1_2_0, domain TBox and ABox v1_1_0, SHACL v1_0_0, research v1_1_0; data module 08-tooling/sen0414_ch02_rdodi_data_v1_0_1.py, corpus v1_0_0); newest deck 03-materials/ch02/SEN0414_Ch02_FlowControl_3e_v3_0_0.pptx (builder deck_build_v3_0_0.py in 08-tooling/ch02-deck/); newest page 03-materials/ch02/page/sen0414_ch02_page_v9_28_0.html with page ABox v9_4_2; stories 08-tooling/sen0414_ch02_stories_v1_0_0.py.",
    "03": "CHAPTER 3 (Loops) as it stands: research 03-materials/ch03/rdodi (document v1_2_0, domain TBox and ABox v1_1_0, SHACL v1_0_0, research v1_2_0; data module 08-tooling/sen0414_ch03_rdodi_data_v1_0_0.py, corpus v1_0_0); newest deck 03-materials/ch03/SEN0414_Ch03_Loops_3e_v4_0_0.pptx (builder deck_build_v4_0_0.py in 08-tooling/ch03-deck/); newest page 03-materials/ch03/page/sen0414_ch03_page_v9_28_0.html with page ABox v1_5_0; stories 08-tooling/sen0414_ch03_stories_v1_0_0.py.",
    "04": "CHAPTER 4 (Functions) as it stands: research 03-materials/ch04/rdodi (document v1_2_0, domain TBox and ABox v1_1_0, SHACL v1_0_0, research v1_1_0; data module 08-tooling/sen0414_ch04_rdodi_data_v1_0_0.py, corpus v1_0_0); newest deck 03-materials/ch04/SEN0414_Ch04_Functions_3e_v2_0_0.pptx (builder deck_build_v2_0_0.py in 08-tooling/ch04-deck/); newest page 03-materials/ch04/page/sen0414_ch04_page_v9_28_0.html with page ABox v1_5_0; stories 08-tooling/sen0414_ch04_stories_v1_0_0.py.",
    "05": "CHAPTER 5 (Debugging) as it stands: research 03-materials/ch05/rdodi (document v1_2_0, domain TBox and ABox v1_1_0, SHACL v1_0_0, research v1_1_0; data module 08-tooling/sen0414_ch05_rdodi_data_v1_0_0.py, corpus v1_0_0); newest deck 03-materials/ch05/SEN0414_Ch05_Debugging_3e_v2_0_0.pptx (builder deck_build_v2_0_0.py in 08-tooling/ch05-deck/); newest page 03-materials/ch05/page/sen0414_ch05_page_v9_28_0.html with page ABox v1_3_0; stories 08-tooling/sen0414_ch05_stories_v1_0_0.py.",
}
DIRECTION = ("Direction of the course coordinator, 2026-10-25, recorded as relayed: close the Iteration 18 review, then plan and start the Iteration 19 retrofit from chapter 1 by the change route: re-rank the open items, generate the briefs, give the executor briefs to start; do not wait for the owner. "
             "The owner's decision of Friday 2026-10-23 16:06 Istanbul (13:06 UTC) (ex:CR2_Priority3), recorded as relayed, is the release: after chapters 7, 8 and 9 are finished, return to ALL chapters starting with chapter 1 (retrofit to the standard: deck, chapter-code manifest, page). Chapters 7, 8 and 9 and the repairs are finished and controlled (register 2.201.0).")
FACTS = ("MEASURED FACTS (the lineage agent, 2026-10-25, from the repository; logs 08-tooling/control-iter19-logs/): "
         "(1) DECKS: the deck standard check v1_0_0 on the newest deck of each chapter 1 to 5 prints FAILING: chapter 1 fails D1, D2, D3, D4, D5, D7, D10, D11 (8 of 13; M1 not measured, no manifest); chapter 2 the same 8; chapter 3 the same 8; chapter 4 the same 8; chapter 5 fails those 8 and D12 (9). Every chapter 1 to 5 has NO chapter-code manifest (03-materials/chNN/page has none) and the deck overlap check v1_0_0 ends FINDINGS on every one (5, 4, 6, 5 and 3 findings for chapters 1 to 5). "
         "(2) RESEARCH: the chapter check Research/Ch01 to Research/Ch05 each ends 'OVERALL: FAIL (2)': Stage1 to Stage3 PASS, Stage4.cov FAIL (hollow typed individuals of the page ABox: 10, 10, 10, 11, 11) and Stage4.sub FAIL (individuals not substantive: 80, 81, 85, 78, 91), Cross.B CANNOT_RUN. It is the defect that chapter 6 had (ex:CR2_ResFix06); for chapters 1 to 5 the research is therefore part of the retrofit, not an extra. "
         "(3) THE CHAPTER CHECK does not cover chapters 1 to 5 for Deck and Page: Deck/Ch01 and Deck/Ch02 end in an assertion, Deck/Ch03 and Deck/Ch04 in a missing build script, Deck/Ch05 in StopIteration; Page/Ch01 starts a browser test outside the lock and was stopped. They are the chapters it was never written for (it covers 6 to 12 and chapter 6 partly). The controller measures chapters 1 to 5 with the deck standard check, the deck overlap check, the page test 9.37.0 and 9.34.0 under the runner v1_1_0, and the chapter check Research/ChNN; adding Deck and Page cases to the chapter check is not part of this plan (a change to a committed tool; a new tool version would be a new item). "
         "(4) PAGES: the newest pages of chapters 1 to 5 are v9_28_0 (template 9.50.0, old standard); they have no chapter-code tab. The rebuilt pages follow the pages of chapters 6 to 9 (v9_90_0, template 9.52.2, builder 4.18.1, page-data builder 2.25.0, page test 9.37.0, runner v1_1_0). "
         "(5) PRECEDENT: chapter 9 (deck 2026-10-24 19:37 to 19:58; page 20:05 to 23:54) and chapter 6 (page, then the research repair, which took three executor sessions because the second dropped seven individuals of the old set without saying so: the controller compares the individual sets of the old and new files, and an executor must too). The first story photograph of the chapter 9 page fills the viewport height, so the story text starts below the fold: the retrofit pages must show the story text without scrolling past a full-height photograph (noted at the Iter_18 review). "
         "(6) ESTIMATES (G120: estimates, not measurements): deck build 5.0 h, deck verify 0.5 h, page build 3.5 h, research set and page ABox 4.0 h, research verify 0.5 h, page verify 1.0 h: 14.5 h per chapter, 72.5 h for the five; the machine has 2 cores and browser tests run one at a time, so the executor sessions of different chapters overlap only in the deck and research builds.")
GAPS = ("GAPS SAID OPENLY: (a) the metrics Met2_StdDecks and Met2_StdPages count the decks and pages of chapters 6, 7 and 8 (target 3) and read 3 and 3 at the Iter_18 review; the retrofit of chapters 1 to 5 moves no number of those metrics, and a metric for it has not been defined: defining one is a change of the Objective stage, held back for the owner's decision on the objective; until then the Iter_19 review reports the chapters retrofitted as an observation of the existing objectives with the method text stating what was counted. "
        "(b) Cross.B of the research gates still cannot run (ex:ST_Plan_Gap_CrossB); the research criterion of the retrofit therefore says: Cross.B must not FAIL, CANNOT_RUN is reported and is not a pass. "
        "(c) The chapter check of this register does not cover Deck and Page of chapters 1 to 5 (fact 3). "
        "(d) The end of Iter_19 is the proposed end of seven days (G9); a rebaseline is an owner decision, and 72.5 h of estimated work in seven days depends on how many executor sessions run side by side (the plan: decks and research of different chapters in parallel, browser tests serially); the plan does not promise that all five chapters finish inside it, and a chapter that is not Done at the review is said to be not Done and is carried by the change route, not hidden.")
GOAL = ("The decks, the chapter-code manifests and the interactive pages of chapters 1 to 5 are rebuilt as new files that meet the written teaching-material standard (the deck standard D1 to D12, measured by the independent deck check and overlap check; the page standard P1 to P11, measured by the page test 9.37.0 and 9.34.0), the research set and the page ABox of each chapter pass the chapter check Research/ChNN on the new page, "
        "the slide code of each chapter appears in the same order in the chapter-code tab of its page and runs there, chapter 1 first, then 2, 3, 4 and 5; every file is verified by the lineage agent's own re-runs on the evidence bridge. Each unit that fails is named failing and is not Done. No existing file, gate, test or threshold is edited. Frozen at the planning ceremony.")
GH_RES = ("Given the research set and the page ABox of chapter N as they stand (the chapter check Research/ChNN ends 'OVERALL: FAIL (2)': Stage4.cov and Stage4.sub fail on the page ABox) and the NEW page of the chapter (the page-build task of the same chapter, Done and controlled), "
          "when (A) a NEW data module 08-tooling/sen0414_chNN_rdodi_data_vX_Y_Z.py is written from the chapter corpus and the existing research files (no individual, class, link or source of the old files is dropped without a stated reason; nothing is invented) and the chapter files are rebuilt from it by the generic builder (sen0414_rdodi_build_v1_2_0.py) as NEW versioned files in 03-materials/chNN/rdodi, and (B) a NEW page-ABox builder version file where needed (the newest is sen0414_page_abox_build_v1_1_9.py; older versions stay) builds a NEW page ABox 03-materials/chNN/page/sen0414_chNN_page_abox_vX_Y_Z.ttl that describes the NEW page (its menus, tabs, panels, widgets and chapter-code examples as they are in that page), "
          "then ALL of: (1) every new file is new and every committed file (the older research files, page ABoxes, the deck, the page, the manifest, the builders) is byte-identical; "
          "(2) every typed individual of the new research ABox and of the new page ABox has a label, a definition and a source where the gates ask for them, and content of at least five words that is substantive by the gate, written from the book's chapter, the deck, the page and the existing content; the set of individuals, classes, links and sources of the old files is a subset of the new files' or each missing one has a stated reason (the controller compares the sets); "
          "(3) the chapter check Research/ChNN ends exit 0 with 'RESULT Research/ChNN: PASS': the gates 'OVERALL: PASS' with Stage4.A, B, cov, sub and src passing on the NEW page ABox, HermiT consistent, the execution checks with 0 mismatches; Cross.B must not FAIL; it reports CANNOT_RUN (0 hybrid chains) and is reported openly as such and NOT counted as a pass (tracked by the planned story ex:ST_Plan_Gap_CrossB); "
          "(4) the deck, the page and the manifest of the chapter are not changed (the page file keeps its SHA-256) and the page test 9.37.0 still ends exit 0 on the page; "
          "(5) the chapter checks Research/Ch06 to Research/Ch09 and the Research checks of the chapters retrofitted before still end PASS; no committed file is edited; results as printed, measured by the controller by its own re-runs.")


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def first_note(t, name):
    i, j = blk(t, name); m = re.search(r'backlog:hasAuditNote "((?:[^"\\]|\\.)*)"', t[i:j]); assert m, name
    return m.group(1).replace('\\"', '"').replace("\\\\", "\\")


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Plan Iteration 19: the retrofit of chapters 1 to 5 to the written standard, with the research set of each chapter, and move the later chapters to a new Iteration 20"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(DIRECTION + " The scope does not move outward: the planned stories of the retrofit were admitted at the owner's decision (ex:CR2_Priority3); this change plans them, adds the tasks, one criterion for the research set and a new unstarted iteration for the later chapters."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What planning Iteration 19 changes, with the facts measured before it is planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACTS + " " + GAPS + " WHAT MOVES: the Backlog stage is revised once more (G125 route 2). Iter_19 gets its start (the planning ceremony), its end (seven days, G9), its sprint goal, the five stories of chapters 1 to 5 (Ready, scored) and 30 tasks; the stories of chapters 10 to 25, the remaining-chapters story and the Cross.B gap story move to the new unstarted Iter_20; "
                    "the planned retrofit criterion ex:AC2F_Retrofit is restated (planned into Iter_19; the page test 9.37.0; the manifest) and ex:AC2F_RetrofitResearch is added; the exclusion ex:Excl2_NoRebuild is lifted for the NEW files of chapters 1 to 5 only. "
                    "RE-RANKING of the open items (WSJF: business value 20; time criticality 20, 16, 13, 10, 8 in the owner's order of chapters; risk reduction = the number of deck-standard elements and research gates measured failing; job size 14.5 h): the order is chapter 1, 2, 3, 4, 5; inside a chapter the order of the dependencies (deck, deck control, page, research set and page ABox, research control, page control); the Iter_20 stories stay Proposed and unscored, in the owner's order (chapters 10 to 25, the remaining chapters), the Cross.B gap after a decision on what a hybrid chain of this course is. "
                    "Not in the plan: a rebaseline, a waiver, an edit of a gate or test, a new metric."))
    return t + cr + ia, "ChangeRequest ex:CR2_Iter19 (Pending) and ImpactAssessment ex:IA2_Iter19: plan the retrofit of chapters 1 to 5 as Iteration 19 and move the later chapters to a new Iteration 20; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (DIRECTION + " Stories become Ready with scores and tasks, a criterion is added and another restated, and stories move between iterations: the closed Backlog stage's digest moves (G117, G125 route 2): a StageRevision from the Backlog stage, never from the Mission; the change request " + CR[3:] + " and the impact assessment " + IA[3:] + " were recorded first. "
              "This version retracts the Backlog output ex:Out2_BacklogR8 and rebuilds nothing; the next version closes the Backlog stage again as ex:Out2_BacklogR9 and re-admits every item without re-dating any; a third version fills the commit. The retracted output and its digest stay as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: Iteration 19 planned for the retrofit of chapters 1 to 5, the later chapters moved to Iteration 20"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) for the planning of Iteration 19: the Backlog output Out2_BacklogR8 is retracted; nothing is rebuilt in this version."


def task_block(ch, key, label, typ, cat, state_note, deps, audit, sess, start_note):
    tid = "TK_Ret_Ch%s_%s" % (ch, key)
    return tid, ('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
                 '    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_19 ; backlog:admittedByOutput %s ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
                 '    backlog:hasInvestmentCategory backlog:%s ; backlog:hasTaskType backlog:%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n'
                 '    backlog:dependsOn %s ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n') % (
        tid, lit(label), tid, lit(label), NEW, cat, typ, ", ".join(deps), lit(audit + " Planned session %s; estimated %.1f hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun). %s" % (sess, EST[key], start_note)))


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now(); L = []
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR8\b", t)); assert cnt >= 80, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR8\b", "admittedByOutput " + NEW, t)
    end = (datetime.datetime.strptime(n, "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
    deck_note = first_note(t, "TK_Std_Deck_Ch09_Build"); page_note = first_note(t, "TK_Std_Page_Ch09_Build")
    deck_note = deck_note[:deck_note.index(" Planned session")]; page_note = page_note[:page_note.index(" Planned session")]
    REPAIRED = ["TK_Std_TemplateFix_Verify", "TK_Std_Runner_Verify", "TK_Std_Regress", "TK_Std_Charset_Verify", "TK_Std_PageTest37_Verify"]
    for x in REPAIRED + ["TK_Std_DeckCheck", "TK_Std_ResearchCh06_Verify"]:
        assert ("\nex:%s a backlog:ExecutionTask" % x) in t, x
    members = []; plans = []
    for ch, title in CH.items():
        sid = "ST_Plan_Retrofit_Ch" + ch; tk = {}
        base = "ex:TK_Ret_Ch%s_" % ch
        facts = FACT[ch]
        dn = deck_note.replace("chapter 9 (Regular Expressions)", "chapter %d (%s)" % (int(ch), title)).replace("chapter 9", "chapter %d" % int(ch)).replace("ch09", "ch" + ch)
        dn = dn.replace("Build the deck of chapter", "RETROFIT: build the deck of chapter", 1)
        pn = page_note.replace("template 9.52.1 with the page builder v4_18_0", "template 9.52.2 (08-tooling/course_page_template_v9_52_2.html) with the page builder v4_18_1 (08-tooling/sen0414_page_build_v4_18_1.py)").replace("page tests 9.36.0 and 9.34.0 (the runner sen0414_page_test_run_v1_0_0.py)", "page tests 9.37.0 and 9.34.0 (the runner sen0414_page_test_run_v1_1_0.py; PAGE_TEST_FILE=sen0414_page_test_v9_37_0.py for 9.37.0)").replace("page test 9.36.0", "page test 9.37.0")
        pn = pn.replace("chapter 9 (Regular Expressions)", "chapter %d (%s)" % (int(ch), title)).replace("chapter 9", "chapter %d" % int(ch)).replace("ch09", "ch" + ch).replace("(above 9_28_0)", "(above 9_28_0; the pages of chapters 6 to 9 are v9_90_0)")
        pn = "RETROFIT: " + pn
        rs = ("Make the research set of chapter %d (%s) pass the chapter check Research/Ch%s on a NEW data version and a NEW page ABox that describes the NEW page. Read the criterion (ex:AC2F_RetrofitResearch) and the precedent of chapter 6 first (commits 0064873, 12b4bd1, f18e3da, 86d4946, c1d3615; the data module 08-tooling/sen0414_ch06_rdodi_data_v2_2_0.py; the page-ABox builder 08-tooling/sen0414_page_abox_build_v1_1_9.py; the chapter 7 data module v1_3_0 for the way a data module is made from a corpus). "
              "The lesson of chapter 6: a second session dropped seven individuals of the old set and said nothing was removed; before you report, compare the sets of individuals, classes, links, sources and labels of the OLD and the NEW files with a script and list every difference with its reason. Nothing is invented: content comes from the book's chapter, the deck, the page and the existing files. "
              "A committed file is never edited. STOP and report if the task cannot be satisfied without editing a committed file, a gate, a test or a threshold beyond the named new files. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); Cross.B CANNOT_RUN is reported as such and is not a pass. The machine has 2 cores: no build beside a browser test." % (int(ch), title, ch))
        specs = [("Deck_Build", "Rebuild the deck of chapter %d (%s) against the deck standard and give it its chapter-code manifest" % (int(ch), title), "TaskType_Build", "Cat_NewCapability", ["ex:TK_Std_DeckCheck"], dn, "SEN0414-I19-deck-ch" + ch, "Starts first in the chapter: the later tasks depend on its control."),
                 ("Deck_Verify", "Verify the deck of chapter %d against the deck standard" % int(ch), "TaskType_Verify", "Cat_Compliance", [base + "Deck_Build", "ex:TK_Std_DeckCheck"],
                  "Run the deck standard check v1_0_0 and the deck overlap check v1_0_0 for chapter %d, the manifest equality (M1), and read the deck slide by slide, rendering every slide to an image for visual review (the reading by the three roles of the owner's preference - teaching academician, reviewing faculty specialist, student - is recorded as a reading, not as a tool result); record every result as printed: Done or NOT MET, no waiver." % int(ch), "SEN0414-lineage (control)", ""),
                 ("Page_Build", "Rebuild the page of chapter %d (%s) on the new template with the chapter-code tab" % (int(ch), title), "TaskType_Build", "Cat_NewCapability", [base + "Deck_Verify"] + ["ex:" + x for x in REPAIRED], pn, "SEN0414-I19-page-ch" + ch, "Starts when the deck of the chapter is controlled."),
                 ("Research", "Make the research set and the page ABox of chapter %d (%s) pass the chapter check on the new page" % (int(ch), title), "TaskType_Build", "Cat_Maintenance", [base + "Page_Build", "ex:TK_Std_ResearchCh06_Verify"], rs, "SEN0414-I19-research-ch" + ch, "Starts when the page of the chapter is controlled (the page ABox describes the new page); the research set itself may be prepared earlier but its page ABox is built last."),
                 ("Research_Verify", "Verify the research set and the page ABox of chapter %d" % int(ch), "TaskType_Verify", "Cat_Compliance", [base + "Research"],
                  "Run the chapter check Research/Ch%s and the RDODI gates on the controller's own account, compare the sets of individuals, classes, links, sources and labels of the old and the new files (a difference without a stated reason is NOT MET), check that every committed file is byte-identical, that the page file keeps its SHA-256, and that Research/Ch06 to Research/Ch09 still end PASS; record every result as printed: Done or NOT MET, no waiver." % ch, "SEN0414-lineage (control)", ""),
                 ("Page_Verify", "Verify the page of chapter %d against the page standard" % int(ch), "TaskType_Verify", "Cat_Compliance", [base + "Page_Build", base + "Research_Verify", "ex:TK_Std_PageTest37_Verify"],
                  "Re-run serially, under the lock, the page tests 9.37.0 and 9.34.0 on the controller's own account (fixture-checked tool), the manifest equality (the chapter-code tab equals the deck's code, text and order), the charset, comment and manifest checks, the four story pictures embedded with their licences recorded; open the page at 390, 768 and 1366 px and look at every tab, including that the story text is reachable without scrolling past a full-height photograph; record every result as printed: Done or NOT MET, no waiver.", "SEN0414-lineage (control)", "")]
        tks = []
        for key, label, typ, cat, deps, audit, sess, sn in specs:
            tid, blkx = task_block(ch, key, label, typ, cat, "", deps, audit, sess, sn)
            tks.append("ex:" + tid); L.append(blkx)
            if key in ("Deck_Build", "Page_Build", "Research"):
                L.append('ex:%s backlog:hasAuditNote %s .\n' % (tid, lit("Facts for this task, measured 2026-10-25 UTC by the lineage agent: " + facts + " " + FACTS)))
        members += [sid] + [x[3:] for x in tks]
        # story: Ready, scored, decomposed
        i, j = blk(t, sid); b = t[i:j]
        old = 'backlog:hasState backlog:Proposed ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned." ;'
        assert old in b, sid
        b = b.replace(old, 'backlog:decomposesInto %s ;\n    backlog:hasState backlog:Ready ;\n    backlog:hasPriorityScore ex:Score16_%s ;' % (", ".join(tks), sid))
        b = b.replace(" (planned)", "").replace("backlog:memberOfContainer ex:Iter_19", "backlog:memberOfContainer ex:Iter_19")
        b = b.replace("backlog:hasAcceptanceCriterion ex:AC2F_Retrofit ;", "backlog:hasAcceptanceCriterion ex:AC2F_Retrofit, ex:AC2F_RetrofitResearch ;")
        t = t[:i] + b + t[j:]
        rr = DECKFAIL[ch] + RESFAIL[ch]; val = (20 + TC[ch] + rr) / SIZE
        L.append('ex:Score16_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value 20 + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Inputs from observable facts: job size is the sum of the story's task estimates in this register (%s); time criticality %d = place %d in the owner's order of chapters (20 = first, then 16, 13, 10, 8); risk reduction %d = the deck-standard elements (%d) and research gates (%d) measured failing on 2026-10-25 UTC. Scored on %s UTC at the planning of Iteration 19 (ex:CR2_Iter19); the earlier planned-and-unscored state is history." % (
                TC[ch], rr, SIZE, val, ", ".join("%s %.1f h" % (k, v) for k, v in EST.items()), TC[ch], int(ch), rr, DECKFAIL[ch], RESFAIL[ch], n))))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (sid, lit("PLANNED INTO ITERATION 19 on %s UTC (ex:CR2_Iter19, planning ceremony ex:PC2_Iter_19): Ready, scored, decomposed into six tasks (deck build, deck verify, page build, research set and page ABox, research verify, page verify). %s %s No executor has started; work begun is recorded at the real start of each executor session." % (n, FACT[ch], GAPS))))
        plans.append('ex:Plan2R_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 19"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_19 ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec2S_D, ex:Scen2S_D_Passes, ex:Scen2S_D_NotClaimed, ex:Spec2S_P, ex:Scen2S_P_Passes, ex:Scen2S_P_NotClaimed .\n' % (sid, sid, n, sid, ", ".join(tks)))
    # Iter_19 and Iter_20
    i, j = blk(t, "Iter_19")
    t = t[:i] + ('ex:Iter_19 a backlog:Iteration ; rdfs:label "Iteration 19: the chapter 1 to 5 decks, pages and research sets brought to the written standard"@en ; backlog:hasIdentifier "Iter_19" ; backlog:belongsToLineage ex:Lineage2 ;\n'
                 '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n') % (
        n, end, lit("Proposed by the lineage agent on %s: the start is the instant of the planning ceremony ex:PC2_Iter_19; the length is 7 days, constant (G9) - a stipulation, not a measurement (the class cadence). Justification of the work inside it (estimates, G120): 14.5 h per chapter (%s), 72.5 h for chapters 1 to 5; the heavy part is the browser tests, serial on the two cores; decks and research sets of different chapters may be built side by side. This is NOT a promise that all five chapters finish inside the seven days (gap d of ex:IA2_Iter19); chapter 1 first, and each chapter ships as soon as it is controlled." % (n, ", ".join("%s %.1f h" % (k, v) for k, v in EST.items()))),
        lit(GOAL), ", ".join("ex:" + m for m in members)) + t[j:]
    moved = ["ST_Plan_Retrofit_Ch%02d" % k for k in range(10, 26)] + ["ST_Plan_Remaining", "ST_Plan_Gap_CrossB"]
    for sid in moved:
        i, j = blk(t, sid); b = t[i:j]; assert "backlog:memberOfContainer ex:Iter_19" in b, sid
        t = t[:i] + b.replace("backlog:memberOfContainer ex:Iter_19", "backlog:memberOfContainer ex:Iter_20", 1) + t[j:]
        L.append('ex:%s backlog:hasAuditNote "Moved from the planned Iteration 19 to the new unstarted Iteration 20 on %s UTC (ex:CR2_Iter19): Iteration 19 is the retrofit of chapters 1 to 5. Still PLANNED, NOT STARTED, Proposed and unscored." .\n' % (sid, n))
    L.append('\nex:Iter_20 a backlog:Iteration ; rdfs:label "Iteration 20 (planned, not started): the retrofit of chapters 10 to 25, the build of the remaining chapters and the Cross.B gap"@en ; backlog:hasIdentifier "Iter_20" ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasDurationSource "PLANNED, NOT STARTED: no start, end or sprint goal is set; the iteration is planned with its own ceremony after the Iteration 19 review (ex:CR2_Iter19)." .\n')
    L.append('\nex:PC2_Iter_19 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 19: the chapter 1 to 5 retrofit"@en ; backlog:ceremonyFor ex:Iter_19 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (
        n, ", ".join("ex:Plan2R_ST_Plan_Retrofit_Ch" + c for c in CH), lit("Held %s UTC by the lineage agent, after the review that closed Iteration 18 (ex:RC2_Iter_18B) and on the direction of the course coordinator (ex:CR2_Iter19): the five stories and their 30 tasks are committed to this iteration, whose goal is frozen at its start. No executor has started; work begun is recorded at the real start of each executor session, with its brief." % n)))
    L.extend("\n" + p for p in plans)
    L.append('\nex:PB2S_Iter_19 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 19 when it was planned"@en ; backlog:baselineFor ex:Iter_19 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (n, n, end))
    # criteria
    i, j = blk(t, "AC2F_Retrofit"); b = t[i:j]; assert "PLANNED, NOT STARTED (ex:CR2_Priority3). Given" in b
    b = b.replace("PLANNED, NOT STARTED (ex:CR2_Priority3). Given", "Planned into Iteration 19 (ex:CR2_Iter19). Given", 1)
    b = b.replace("the controller re-runs every check; no committed file is edited.", "the controller re-runs every check (the deck standard check, the deck overlap check, the page test 9.37.0 and 9.34.0 under the runner v1_1_0; the chapter check covers Research only for chapters 1 to 5); the chapter-code manifest 03-materials/chNN/page/chapter_code_chNN_v1_0_0.json equals the deck's code boxes (text and order); the research set is the criterion ex:AC2F_RetrofitResearch; no committed file is edited.", 1)
    t = t[:i] + b + t[j:]
    L.append('ex:AC2F_Retrofit backlog:hasAuditNote %s .\n' % lit("RESTATED %s UTC (ex:CR2_Iter19): the criterion is planned into Iteration 19 for chapters 1 to 5; it names how the controller measures them (the chapter check covers Research only for these chapters, fact 3 of ex:IA2_Iter19) and states the manifest element; the research set is a criterion of its own, ex:AC2F_RetrofitResearch. For chapters 10 to 25 and the remaining chapters it stays planned and is restated again when they are planned." % n))
    L.append('\nex:AC2F_RetrofitResearch a backlog:AcceptanceCriterion ; rdfs:label "The research set and the page ABox of a retrofitted chapter pass the chapter check Research on a new data version and the new page"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS2_RdodiGates, ex:TS2_ChapterCheck, ex:TS2_PageAboxBuild ;\n    backlog:measuredWithVersion "chapter check v1_1_0; RDODI gates v1_1_1; RDODI checks v1_2_0; generic builder v1_2_0; page-ABox builder v1_1_9 (or a newer new-file version); the page test 9.37.0; Python 3.14, HermiT" ;\n    backlog:satisfiedByArtifact "the new files cited by SHA-256, the controller\'s own runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC2R6_Passes, ex:TC2R6_NotClaimed, ex:TC2R6B_PageAbox .\n' % lit(GH_RES))
    L.append('ex:Excl2_NoRebuild rdfs:comment "Lifted on %s UTC (ex:CR2_Iter19) for chapters 1 to 5, ONLY for the NEW files of their decks, chapter-code manifests, pages, research sets, data modules and page ABoxes (the retrofit of Iteration 19): no existing deck, research run, page or page ABox of these chapters is changed. Chapters 10 to 25 and the remaining chapters stay excluded; each is lifted by its own record when it is planned into an iteration."@en .\n' % n)
    L.append('ex:SC2_Iter19 a backlog:ScopeChange ;\n    rdfs:label "Thirty tasks and one criterion admitted for the retrofit of chapters 1 to 5 in Iter_19; the later chapters move to Iter_20"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, ", ".join("ex:" + m for m in members if m.startswith("TK_")), lit(DIRECTION + " The boundary does not move outward in deliverables; the stories were admitted by the owner's decision, these are their tasks.")))
    t, k = re.subn(r'(ex:CR2_Iter19 a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR2_Iter19 rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_Iter19; it was Pending before. The release is the owner\'s decision of 2026-10-23 (ex:CR2_Priority3) and the coordinator\'s direction; the owner is not waited for."@en .\n' % n[:10])
    t += "\n" + "".join(L)
    out = ('\nex:Out2_BacklogR9 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt for the planning of Iteration 19 and the new Iteration 20"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % S.digest(t, "Backlog")
    return t + out, "second lineage, Backlog stage rebuilt: Iteration 19 planned (chapters 1 to 5: five Ready scored stories, 30 tasks, ceremony, baseline, goal), the later chapters moved to the new unstarted Iteration 20, the retrofit criterion restated and the research criterion added, the exclusion lifted for the new files of chapters 1 to 5, ScopeChange, change request Accepted, every item re-admitted."


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR9 set to the commit that closed it (%s); the revision is complete and no work is begun in this version." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
