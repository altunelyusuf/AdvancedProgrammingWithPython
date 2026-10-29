#!/usr/bin/env python3
"""sen0414_lineage_ci5 v1_1_0 (over v1_0_0, which stays as committed: its change and retract events made registers 2.318.0 and 2.319.0; this version adds to the backlog event the result of the controller's leak-probe measurement of 2026-10-29, which found the page of chapter 8 failing: a page-repair story with two tasks, the research of chapter 8 waits for the repaired page) - change route for the change item CI-5 of the second lineage (ex:Lineage2): the pages of chapters 1 to 9 are MEASURED against the leak probe v1_3_0 and the page test 9.37.0
(nobody has measured them), and the research sets of chapters 7, 8 and 9, which are Done as pre-lineage items without a page ABox (Stage 4 and Cross.B have never run for them), get the retrofit that chapters 10 to 17
have: a research task with the FIRST page ABox and a verify task each. The gap was found by the lineage agent on 2026-10-28 while recording the queued midterm lineage (ex:Lineage3, CI-5 audit note, register 2.312.0);
chapter 9 has the same gap and is not in the exam chapters 1 to 8, but it is in the owner's order of chapters (ex:CR2_Priority3) and is said openly.
Events, one new register file each (the route of ex:CR2_Iter20, G125 route 2):  change | retract | backlog PREV | fill PREV.   Usage: sen0414_lineage_ci5_v1_0_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.1.0"
import datetime, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
import sen0414_lineage_iter20_v1_0_0 as I
import glob as _g, importlib.util as _iu
def _pv12():
    # the digest tool v1_9_0 named by the standard module is no longer in the framework checkout; v1_12_0 is the one the validator v1_17_0 uses (table v1, as for ex:Out3_Mission)
    spec = _iu.spec_from_file_location("pv12", W.FW + "/03-tooling/backlog_pipeline_verify_v1_12_0.py"); m = _iu.module_from_spec(spec); spec.loader.exec_module(m)
    tb = sorted(_g.glob(W.FW + "/01-ontologies/backlog_tbox_v*.ttl"), key=lambda q: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", q).groups()])[-1]
    m.STAGE_TYPES = m._load_stage_types(tb, table="v1"); return m
W.S._pv = _pv12
S = W.S; lit = W.lit; now = W.now; REPO = W.REPO
CR = "ex:CR2_CI5"; IA = "ex:IA2_CI5"; REV = "ex:Revision_Lineage2_Backlog12"
OLD = "ex:Out2_BacklogR11"; NEW = "ex:Out2_BacklogR12"
CHS = {"07": ("Dictionaries and Structuring Data", "Dictionaries"), "08": ("Strings and Text Editing", "Strings"), "09": ("Text Pattern Matching with Regular Expressions", "RegularExpressions")}
EST = {"Research": 4.0, "Research_Verify": 0.5}
MEAS = {"Ch07_09": ("chapters 7, 8 and 9", 1.5), "Ch01_06": ("chapters 1 to 6", 2.0)}
TS = "ex:TS2_LeakProbe13"; AC = "ex:AC2F_PagesMeasured"

DIRECTION = ("Direction of the course coordinator, 2026-10-28, recorded as relayed: the owner wants a midterm exam of chapters 1 to 8 after the current chapters; it is a different mission and waits as a queued lineage (ex:Lineage3); "
             "analyse chapters 1 to 8 first and report the verified gaps. The lineage agent's verified gaps (2.311.0, 2.312.0) became the change item CI-5: chapter work comes first, in this lineage. The owner's decision of Friday 2026-10-23 "
             "(ex:CR2_Priority3) is the release for chapters 7, 8 and 9 and for the return to ALL chapters. The coordinator's direction of 2026-10-29: control the research of chapter 17, record, re-rank, and give the next brief for CI-5.")


def facts(ch):
    def newest(pat):
        return I.newest(pat)
    def v(p):
        m = re.search(r"_v(\d+_\d+_\d+)", p or ""); return m.group(1) if m else "none"
    rd = {k: newest("03-materials/ch%s/rdodi/sen0414_ch%s_%s_v*.ttl" % (ch, ch, k)) for k in ("document", "domain_tbox", "domain_abox", "domain_shacl", "research")}
    pg = newest("03-materials/ch%s/page/sen0414_ch%s_page_v*.html" % (ch, ch)); dk = newest("03-materials/ch%s/SEN0414_Ch%s_*.pptx" % (ch, ch))
    log = os.path.join(I.LOGS, "regr_Research_Ch%s_after_ch17.log" % ch); lg = open(log, encoding="utf-8").read() if os.path.exists(log) else ""
    return ("CHAPTER %d (%s) as it stands (measured 2026-10-29 UTC by the lineage agent): research 03-materials/ch%s/rdodi (document %s, domain TBox %s, ABox %s, SHACL %s, research %s); data module %s; newest deck %s; newest page %s "
            "(template 9.52.2, built in Iteration 18; the page of the chapter is controlled and stays as it is); page ABox: NONE, so the gates' Stage 4 (A, B, cov, sub, src) and Cross.B have never run for the chapter; chapter-code manifest chapter_code_ch%s_v1_0_0.json. "
            "The chapter check Research/Ch%s on the controller's machine (log control-iter20-logs/regr_Research_Ch%s_after_ch17.log, re-run 2026-10-29) ends %s." % (
                int(ch), CHS[ch][0], ch, v(rd["document"]), v(rd["domain_tbox"]), v(rd["domain_abox"]), v(rd["domain_shacl"]), v(rd["research"]), os.path.basename(newest("08-tooling/sen0414_ch%s_rdodi_data_v*.py" % ch) or "none"),
                os.path.basename(dk or "none"), os.path.basename(pg), ch, ch, ch, "RESULT Research/Ch%s: PASS (gates OVERALL PASS, HermiT consistent, execution checks 0 mismatches)" % ch if ("RESULT Research/Ch%s: PASS" % ch) in lg else "not read"))


def research_note(ch):
    t, short = CHS[ch]
    return ("Make the research set of chapter %d (%s) pass the chapter check Research/Ch%s WITH its FIRST page ABox, which describes the controlled page of the chapter (the newest page, v9_90_0, built on template 9.52.2: there is NO new page in this task). "
            "Read the criterion (ex:AC2F_RetrofitResearch20, which this change extends to chapters 7, 8 and 9) and the precedents first: the research tasks of chapters 14 to 17 of this iteration (`git log --oneline -- 03-materials/ch16/page/sen0414_ch16_page_abox_v9_95_0.ttl 08-tooling/ch16-research`; the comparison tool `08-tooling/sen0414_ch16_page_abox_compare_v1_0_0.py` is the model for yours) and the page ABoxes of chapters 1 to 4 of Iteration 19. "
            "DIFFERENCES FROM THE PRECEDENTS: (1) NAME THE PAGE ABOX `03-materials/ch%s/page/sen0414_ch%s_page_abox_v9_90_0.ttl`: it carries the version of the page it describes (the page of chapter %s is v9_90_0 and no page ABox exists yet), as the page ABoxes of chapters 1 to 4 carry theirs; the file must name the page file `sen0414_ch%s_page_v9_90_0.html` inside, and the page must stay byte-identical. "
            "(2) THE RESEARCH FILES ARE NOT REBUILT while the chapter check passes on the controller's machine (nothing is changed for its own sake); if your own run of the execution checks fails on a machine that is the controller's twin (python3.14 on the PATH, no network claims), write a NEW data module and NEW research files by the generic builder and compare old and new by local name. "
            "(3) The page-ABox builder is `08-tooling/sen0414_page_abox_build_v1_1_13.py` (a NEW file v1_1_14 if it stops on a visual kind of your page; never edit v1_1_13); it knows every visual kind of chapters 1 to 9. "
            "(4) Run the chapter checks Research/Ch01 to Research/Ch09 and Research/Ch14 to Research/Ch17 after your commit and report them as printed; the page test 9.37.0 once on the page of your chapter under `flock /tmp/page_test.lock` (never beside another browser test; a known intermittent stall of 9.37.0 at #xefinish, CI-6, is reported with its log and the run repeated, an incomplete run is not a pass). "
            "Nothing is invented: content comes from the book's chapter, the deck, the page and the existing files. A committed file is never edited. STOP and report if the task cannot be satisfied without editing a committed file, a gate, a test or a threshold beyond the named new files. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); Cross.B CANNOT_RUN is reported as such and is not a pass. "
            "Planned session SEN0414-I20-research-ch%s; estimated 4.0 hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun). Starts when the measurement of the page of the chapter (task TK_CI5_Measure_Ch07_09) is controlled and the page is found fit." % (
                int(ch), t, ch, ch, ch, ch, ch, ch))


def repair_note():
    fw = open(os.path.join(REPO, "08-tooling", "briefs", "iter20", "r18", "BRIEF_TK_Ret_Ch17_Page_Build.md"), encoding="utf-8").read()
    gc_hook = fw[fw.index("(3) GUARD:"):fw.index("(4) Leak probe v1_2_0")].strip()
    return ("Repair the page of chapter 8 (Strings and Text Editing) as a NEW page file `03-materials/ch08/page/sen0414_ch08_page_v9_91_0.html` (above the newest page v9_90_0, which stays as committed; build it through the real template and builder on the template 9.52.4 (`08-tooling/course_page_template_v9_52_4.html`, committed by the chapter 18 repair and used by the pages of chapters 15 to 17), with its own page data, manifest use and starter files as NEW files under the v9_91_0 name; the content, the story pictures, the chapter-code tab (24 examples, same code, same order) and the Playground starter of v9_90_0 are accepted as they are: reuse them). "
            "WHY: the controller measured the page v9_90_0 on 2026-10-29 with the exercise leak probe v1_3_0 on the exact page file and the template 9.52.2 it was built from (43 programs, 4 rounds, 4 probes, seeds 1 to 5): 0 baseline errors, 0 wrong real runs, but 670 to 830 STATE DRIFTS on every seed (log `08-tooling/control-iter20-logs/leak_ch08_v9_90_0_template_9_52_2_controller_run_v1_3_0.log`). CAUSE (confirmed by the controller on seed 1): the first drift is `warnings.filters 5->6; module warnings attribute filters` at the program UnrecognizedEscapes (an example whose string literals contain invalid escape sequences: compiling it adds an entry to `warnings.filters`, and the template's restore does not take it away), and every later program, exam item and exercise variant runs with a changed warnings state. The other chapters 1 to 7 and 9 pass the same probe (seeds 1 to 5, 0 drifts). "
            "FIX: put into the page's boot program a guard that takes a copy of `warnings.filters` (and of `warnings._filters_mutated` state where the interpreter has it) at boot and puts it back BEFORE and AFTER every program: wrap the worker's `_restore` once, lazily from the `_before_run` hook (the template runs py_boot BEFORE it defines `_restore`; the template's own restore does not cover the warnings module); never use as module-level names in the boot program the names the template worker defines: _LIBS, _restore, _run, _run_inner, _inlib, _state_x, _CWD0. The chapter opens no file or connection in its programs: say so in the report; keep the garbage-collection hook below only if you find a reason. "
            "The hook of the earlier repairs, as a pattern (add the warnings reset where it says your own reset): " + gc_hook + " "
            "ORDER OF THE CHECKS (the controller's rule from the page failures of chapters 14 to 17): (1) build through the real template and builder; (2) run BOTH the leak probe v1_2_0 AND the leak probe v1_3_0 (`python3 08-tooling/sen0414_exercise_leak_probe_v1_3_0.py NODE_PATH_DIR WORK_DIR TEMPLATE.html PAGE.html 4 4 1 2 3 4 5`, absolute paths for template and page, node modules of Pyodide 0.28.2 as in the chapter 17 page logs) on the template FILE and on the EXACT BUILT PAGE FILE (never a scratch copy), five seeds including 1 and 3: 0 wrong real runs, 0 baseline errors and 0 state drifts for BOTH; keep the logs; NOTHING else is done before both pass; if one fails, commit the log, STOP and report with the counts; (3) then the Playground width check at 1366x768, 1400x900 and 390x844 (the page must not scroll sideways, the editor and its overlay end inside the screen, the text-size control is on screen; precedent `08-tooling/ch17-page/playground_width_check*.py`: copy as a NEW file for this chapter), the story-layout probe on every story, the page tests 9.37.0 (PAGE_TEST_FILE=sen0414_page_test_v9_37_0.py) and 9.34.0, and the chapter check Page/Ch08 if it has the case; run 9.37.0 and the chapter check at least FIVE times each under `flock /tmp/page_test.lock` (the known intermittent stall of 9.37.0 at #xefinish, CI-6, is reported with its log and repeated: an incomplete run is not a pass and is not counted). Report any [FAIL] line as a result. Remove your own finished /tmp/page_test_* folders; stop and report if free disk space falls under 0.9 GB. "
            "Nothing else changes: no existing page, gate, test, threshold or template file is edited; the pictures and their captions (a caption names only what its picture shows; portrait photographs are cropped to landscape) are the owner's rules and stay as in v9_90_0. Planned session SEN0414-I20-page-ch08; the research task of chapter 8 waits for this page: its page ABox describes v9_91_0.")


def measure_note(key):
    what = MEAS[key][0]
    return ("Measure the newest pages of %s against the two checks that did not exist when they were built: (1) the exercise leak probe v1_3_0 (`08-tooling/sen0414_exercise_leak_probe_v1_3_0.py`, the template file the page was built from, seeds 1 to 5: 0 wrong real runs and 0 state drifts) and (2) the page test 9.37.0 under `flock /tmp/page_test.lock` through `sen0414_page_test_run_v1_1_0.py` (completed runs only count; an incomplete run is recorded as printed, never counted as a pass; CI-6 is the known intermittent stall at #xefinish). "
            "It is the CONTROLLER's own measurement (no executor builds anything in it): the logs are committed under control-iter20-logs and the control script `sen0414_control_iter20_pages_v1_0_0.py` re-reads them. A page that fails is named failing and is repaired by a new page version through change management (a new task), never by editing; "
            "the research task of a chapter whose page is found failing waits for the repaired page. Estimated %.1f hours of machine time (an estimate, G120: nobody has witnessed a start; the pages and tests are serial under the page-test lock and share the two cores with other sessions)." % (what, MEAS[key][1]))


def task_block(tid, label, typ, cat, deps, audit, est):
    return ('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_20 ; backlog:admittedByOutput %s ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
            '    backlog:hasInvestmentCategory backlog:%s ; backlog:hasTaskType backlog:%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n'
            '    backlog:dependsOn %s ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n') % (
        tid, lit(label), tid, lit(label), NEW, cat, typ, ", ".join(deps), lit(audit + " Estimated %.1f hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun)." % est))


def story_block(sid, label, wants, crit, tks, score):
    return ('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ;\n    backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_20 ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput %s ;\n    backlog:hasInvestmentCategory backlog:Cat_Compliance ;\n'
            '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability %s ; backlog:soThat "every chapter of the course is taught from decks and pages that meet the same written standard, measured and not assumed" ;\n'
            '    backlog:satisfiesDeliverable ex:Del2_StdPages ; backlog:pursuesObjective ex:Obj2_StdPages ; backlog:hasAcceptanceCriterion %s ;\n    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n'
            '    backlog:decomposesInto %s ;\n    backlog:hasState backlog:Ready ;\n    backlog:hasPriorityScore ex:Score31_%s .\n') % (sid, lit(label), sid, lit(label), NEW, lit(wants), crit, ", ".join(tks), sid)


def ev_change(t):
    gaps = " ".join(facts(c) for c in CHS)
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "CI-5: measure the pages of chapters 1 to 9 and give the research sets of chapters 7, 8 and 9 their first page ABox"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(DIRECTION + " The change supports the mission of this lineage: its sprint goal names the research set and first page ABox of each chapter and the owner's order of chapters includes chapters 7, 8 and 9; the scope does not move outward in deliverables."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What CI-5 changes, with the facts measured before it is planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit("MEASURED FACTS (the lineage agent, 2026-10-28 and 2026-10-29): (1) " + gaps + " (2) The pages of chapters 1 to 9 were controlled before the leak probe v1_2_0/v1_3_0 and the page test 9.37.0 existed in their present form; the exam and exercise builders of the page run every program in one worker, so the leak class found in chapters 14 to 17 can exist in them; it is NOT MEASURED. "
                    "GAPS SAID OPENLY: chapter 9 has the same gap as 7 and 8 but is outside the exam chapters 1 to 8; the gates' Cross.B stays CANNOT_RUN everywhere until the pilot (chapter 6). WHAT MOVES: the Backlog stage is revised once more (G125 route 2): two measurement tasks of the controller (chapters 7 to 9 first, because the research tasks depend on them; chapters 1 to 6 after) and three research tasks with their verify tasks "
                    "(chapters 7, 8, 9) are added to Iter_20 as five stories' worth of Ready, scored items; the criterion ex:AC2F_RetrofitResearch20 is extended to chapters 7, 8 and 9 and ex:AC2F_PagesMeasured is added. RE-RANKING of the open items: the new items rank FIRST: business value 20, time criticality 20 (the chapters of the owner's order that come before chapter 10 and are the chapters of the queued midterm), risk reduction 2 for the research stories (Stage 4 never run) and 1 for the measurement; "
                    "the order is: measurement of chapters 7 to 9, research of chapters 7, 8 and 9 (side by side, at most three executors), measurement of chapters 1 to 6, then the chapter 19 to 25 decks in chapter order, CI-6, CI-1 and CI-3, the Cross.B pilot, the closing review. A repair of a page found failing re-ranks the open items again. The exam lineage (ex:Lineage3) stays queued; this is chapter work."))
    return t + cr + ia, "ChangeRequest ex:CR2_CI5 (Pending) and ImpactAssessment ex:IA2_CI5: measure the pages of chapters 1 to 9; research and first page ABox for chapters 7, 8 and 9; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (DIRECTION + " Stories and tasks are added, a criterion is added and another extended: the closed Backlog stage's digest moves (G117, G125 route 2): a StageRevision from the Backlog stage, never from the Mission; the change request " + CR[3:] + " and the impact assessment " + IA[3:] + " are the basis. "
              "This version retracts the Backlog output " + OLD[3:] + " and rebuilds nothing; the next version closes the Backlog stage again as " + NEW[3:] + " and re-admits every item without re-dating any; a third version fills the commit. The retracted output and its digest stay as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: CI-5, the measurement of the pages of chapters 1 to 9 and the research of chapters 7, 8 and 9"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) for CI-5: the Backlog output Out2_BacklogR11 is retracted; nothing is rebuilt in this version."


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now(); L = []
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR11\b", t)); assert cnt >= 100, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR11\b", "admittedByOutput " + NEW, t)
    members = []; plans = []; stories = []
    # criterion and tool for the measurement
    L.append('ex:TS2_LeakProbe13 a backlog:ToolScript ; rdfs:label "exercise leak probe v1_3_0 (the controller\'s probe: counts None sys.modules entries as drift; over v1_2_0)"@en ; backlog:scriptFileName "sen0414_exercise_leak_probe_v1_3_0.py" ; backlog:acceptsGraphPath false .\n')
    L.append('\n%s a backlog:AcceptanceCriterion ; rdfs:label "The newest pages of chapters 1 to 9 are measured against the leak probe v1_3_0 and the page test 9.37.0, as printed"@en ; backlog:belongsToLineage ex:Lineage2 ;\n'
             '    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s, ex:TS2_PageTest37 ;\n    backlog:measuredWithVersion "leak probe v1_3_0 (Pyodide 0.28.2, 4 rounds, 4 probes, seeds 1 to 5); page test 9.37.0 under the runner v1_1_0; Playwright 1.56.0" ;\n'
             '    backlog:satisfiedByArtifact "the controller\'s logs under 08-tooling/control-iter20-logs, re-read by sen0414_control_iter20_pages_v1_0_0.py and verified by the evidence bridge" .\n' % (AC,
        lit("Given the newest page of each of chapters 1 to 9 (built before the probe and the test existed in their present form), when the controller runs the leak probe v1_3_0 on the exact page file and the template file it was built from (seeds 1 to 5) and the page test 9.37.0 (completed runs; an incomplete run is a result, not a pass), "
            "then every probe seed ends with 0 wrong real runs, 0 baseline errors and 0 state drifts and the page test ends exit 0 with 0 failed features, nothing skipped, OR the page is named FAILING with the printed evidence and a repair task is planned through change management; no page is edited, no gate or test is changed, and nothing is counted as measured that was not run."), TS))
    # the measurement stories and tasks
    base = {}
    for key, (what, est) in MEAS.items():
        tid = "TK_CI5_Measure_" + key; sid = "ST_CI5_Measure_" + key
        deps = ["ex:TK_Std_PageTest37_Verify"] + (["ex:TK_CI5_Measure_Ch07_09"] if False else [])
        L.append(task_block(tid, "Measure the pages of %s against the leak probe v1_3_0 and the page test 9.37.0" % what, "TaskType_Verify", "Cat_Compliance", deps, measure_note(key), est))
        L.append(story_block(sid, "Measure the pages of %s: leak probe v1_3_0 and page test 9.37.0" % what, "the pages of %s measured against the checks of the written standard that did not exist when they were built" % what, AC, ["ex:" + tid], None))
        members += [sid, tid]; stories.append((sid, [tid], 1, est))
    # the repair of the page of chapter 8 (found failing by the leak probe v1_3_0 on 2026-10-29)
    rp = "TK_CI5_Page_Ch08_Repair"; rv = rp + "_Verify"
    L.append(task_block(rp, "Repair the page of chapter 8 (Strings and Text Editing): a new page file that restores the warnings state after every program", "TaskType_Build", "Cat_Maintenance", ["ex:TK_Std_Page_Ch08_Verify"], repair_note(), 3.0))
    L.append(task_block(rv, "Verify the repaired page of chapter 8 on the controller's own re-runs", "TaskType_Verify", "Cat_Compliance", ["ex:" + rp],
                        "Control by the lineage agent on its own re-runs: the leak probes v1_2_0 and v1_3_0 on the exact built page (seeds 1 to 5), the Playground width, the story-layout probe, the page test 9.37.0 and 9.34.0 and the chapter check Page/Ch08 at least five runs where the brief says so, the portrait and caption check; an incomplete run is a result, not a pass.", 1.0))
    L.append(story_block("ST_CI5_Page_Ch08", "Repair the page of chapter 8 so that no program leaves state behind", "the page of chapter 8 free of the state drift that the leak probe v1_3_0 measured, as a new page file", AC, ["ex:" + rp, "ex:" + rv], None))
    members += ["ST_CI5_Page_Ch08", rp, rv]; stories.append(("ST_CI5_Page_Ch08", [rp, rv], 3, 4.0))
    # the research stories and tasks
    for ch, (title, short) in CHS.items():
        sid = "ST_CI5_Research_Ch" + ch; r = "TK_Ret_Ch%s_Research" % ch; v = r + "_Verify"
        mdep = "ex:TK_CI5_Measure_Ch07_09"; pdep = "ex:TK_Std_Page_Ch%s_Verify" % ch
        rn = research_note(ch)
        if ch == "08":
            rn = rn.replace("v9_90_0", "v9_91_0").replace("template 9.52.2", "template 9.52.4").replace("(there is NO new page in this task)", "(the page v9_91_0 is the repair of the page v9_90_0, task TK_CI5_Page_Ch08_Repair, controlled before this task starts: there is NO page build in this task)").replace("the measurement of the page of the chapter (task TK_CI5_Measure_Ch07_09) is controlled and the page is found fit", "the measurement of the pages of chapters 7 to 9 (task TK_CI5_Measure_Ch07_09) and the repaired page of the chapter (task TK_CI5_Page_Ch08_Repair_Verify) are controlled")
        note = rn + " " + I.LESSONS["Research"] + " " + I.LESSONS["all"]
        L.append(task_block(r, "Make the research set and the first page ABox of chapter %d (%s) pass the chapter check on the page of the chapter" % (int(ch), title), "TaskType_Build", "Cat_Maintenance", [mdep, pdep, "ex:TK_Std_ResearchCh06_Verify"] + (["ex:TK_CI5_Page_Ch08_Repair_Verify"] if ch == "08" else []), note, EST["Research"]))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (r, lit("Facts for this task, measured 2026-10-29 UTC by the lineage agent: " + facts(ch) + " " + I.GH_RES)))
        L.append(task_block(v, "Verify the research set and the page ABox of chapter %d" % int(ch), "TaskType_Verify", "Cat_Compliance", ["ex:" + r],
                            "Control by the lineage agent on its own re-runs: the control script sen0414_control_iter20_research (a new version for pages below v9_95_0) and the chapter check Research/Ch%s, the regression Research/Ch01 to Ch09 and Ch14 to Ch17, the old-against-new comparison, nochange, everything committed; Cross.B CANNOT_RUN is not counted as a pass." % ch, EST["Research_Verify"]))
        L.append(story_block(sid, "Research set and first page ABox of chapter %d (%s)" % (int(ch), title), "the research set of chapter %d with its first page ABox, so that the gates' Stage 4 and Cross.B can run for the chapter" % int(ch), "ex:AC2F_RetrofitResearch20", ["ex:" + r, "ex:" + v], None))
        members += [sid, r, v]; stories.append((sid, [r, v], 2, EST["Research"] + EST["Research_Verify"]))
    # scores, planning events, refinement events
    for sid, tks, rr, size in stories:
        val = (20 + 20 + rr) / size
        L.append('ex:Score31_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value 20 + time criticality 20 + risk reduction %d) / job size %.1f h = %.2f. Inputs from observable facts: time criticality 20 = the top place: these are chapters of the owner's order (chapters 7, 8, 9) and the chapters of the queued midterm, and the research tasks depend on the measurement; risk reduction %d = %s; job size is the sum of the story's task estimates in this register. Scored on %s UTC at the change CI-5 (ex:CR2_CI5)." % (
                rr, size, val, rr, "2 for Stage 4 never run (no page ABox)" if rr == 2 else ("3 for a page measured failing (670 to 830 state drifts per seed)" if rr == 3 else "1 for pages never measured against the leak probe and the current page test"), n))))
        plans.append('ex:Plan2C5_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 20 (CI-5)"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_20 ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec2S_P, ex:Scen2S_P_Passes, ex:Scen2S_P_NotClaimed .\n' % (sid, sid, n, sid, ", ".join("ex:" + x for x in tks)))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (sid, lit("PLANNED INTO ITERATION 20 on %s UTC (ex:CR2_CI5): Ready, scored, decomposed. No executor has started; work begun is recorded at the real start of each executor session." % n)))
    for m_ in members:
        L.append('ex:Refine7_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_20 ;\n    backlog:hasRefinementOutcome %s .\n' % (
            m_, m_, m_, n, lit("Refined by the lineage agent from the facts of ex:IA2_CI5: criterion with tools and versions, dependencies, estimates, a brief to be generated from the register where an executor does the work; startable when its dependencies are Done.")))
    L.append('\nex:PC2_Iter_20_CI5 a backlog:SprintPlanningCeremony ; rdfs:label "Re-planning of iteration 20 for CI-5: the measurement of the pages of chapters 1 to 9 and the research of chapters 7, 8 and 9"@en ; backlog:ceremonyFor ex:Iter_20 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (
        n, ", ".join("ex:Plan2C5_" + s[0] for s in stories), lit("Held %s UTC by the lineage agent on the change request ex:CR2_CI5: the items are committed to this iteration, whose goal is unchanged; no executor has started." % n)))
    L.extend("\n" + p for p in plans)
    L.append('ex:Iter_20 backlog:hasMember %s .\n' % ", ".join("ex:" + m_ for m_ in members))
    L.append('%s backlog:hasAuditNote %s .\n' % (IA, lit("MEASURED 2026-10-29 (after the change request and impact assessment of 2.318.0): the controller ran the leak probe v1_3_0 on the exact newest page file of each of chapters 1 to 9 and the template file it was built from (9.52.2), seeds 1 to 5 each (logs control-iter20-logs/leak_chNN_*_v1_3_0.log): chapters 1, 2, 3, 4, 5, 6, 7 and 9 PASS on all five seeds (0 wrong real runs, 0 drifts); chapter 8 FAILS on all five seeds (0 wrong real runs, 670 to 830 state drifts): the example UnrecognizedEscapes leaves an entry in warnings.filters that the template's restore does not remove. A page repair story with two tasks is therefore added in this revision and the research of chapter 8 waits for the repaired page; the page test 9.37.0 on the pages of chapters 1 to 9 is still being measured and a failing page found by it is added by a further change.")))
    L.append('ex:AC2F_RetrofitResearch20 backlog:hasAuditNote %s .\n' % lit("EXTENDED %s UTC (ex:CR2_CI5): the criterion applies also to chapters 7, 8 and 9, whose research sets are Done as pre-lineage items without a page ABox; there the page is the controlled page v9_90_0 (no new page), the page ABox is named for the page it describes (sen0414_chNN_page_abox_v9_90_0.ttl), and the research files are not rebuilt while the chapter check passes. Nothing else changes." % n))
    t += "\n" + "".join(L)
    t, k = re.subn(r'(ex:CR2_CI5 a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m_: m_.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    t += ('\nex:SC2_CI5 a backlog:ScopeChange ;\n    rdfs:label "Two measurement tasks and six research tasks admitted for CI-5 in Iter_20"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n') % (
        CR, ", ".join("ex:" + m_ for m_ in members if m_.startswith("TK_")), lit(DIRECTION + " The boundary does not move outward in deliverables."))
    t += '\nex:CR2_CI5 rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_CI5; it was Pending before. The release is the owner\'s decision of 2026-10-23 (ex:CR2_Priority3) and the coordinator\'s direction; the owner is not waited for."@en .\n' % n[:10]
    out = ('\n%s a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt for CI-5"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (NEW, S.digest(t, "Backlog"))
    return t + out, "second lineage, Backlog stage rebuilt for CI-5: the pages of chapters 1 to 9 to be measured (two tasks) and the research of chapters 7, 8, 9 with the first page ABox (six tasks), Ready, scored, in Iter_20; criterion ex:AC2F_PagesMeasured added, ex:AC2F_RetrofitResearch20 extended; Out2_BacklogR12 closes the stage (commit named in the next version)."


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR12 set to the commit that closed it (%s); the CI-5 revision is complete and no work is begun in this version." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
