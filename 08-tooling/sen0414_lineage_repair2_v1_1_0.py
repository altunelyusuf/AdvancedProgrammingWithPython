#!/usr/bin/env python3
"""sen0414_lineage_repair2 v1_1_0 - change route (rulings G104, G125, G136) for two findings of the lineage agent's control of 2026-10-23 and the owner's standing rule that repairs re-rank the open work:
  (1) the page template 9.52.1 shows about 1,157 characters of its own description as visible text above the page header (root cause: two literal '-->' inside its head comment), which fails two old page-test features;
  (2) the page-test runner sen0414_page_test_run_v1_0_0.py names the page test 9.34.0 and so never runs 9.36.0.
Events, one new register file each (the caller validates and commits and pushes each alone):  change | retract | backlog PREV | fill PREV
  change   - ChangeRequest ex:CR2_Repair2 (Pending) and ImpactAssessment ex:IA2_Repair2 with the measured facts.
  retract  - StageRevision from the Backlog stage: retracts ex:Out2_BacklogR2; status LS_Objectived.
  backlog  - Backlog output ex:Out2_BacklogR3; all admitted items re-admitted; two repair stories with criteria and executor and controller tasks; the page builds and the open regression check depend on the repairs' verification;
             WSJF re-scoring of every open story as dated records (the repairs outrank the work they block); ScopeChange; CR Accepted.
  fill     - closedAtCommit of ex:Out2_BacklogR3.
v1.1.0 (over 1.0.0, which produced 2.160.0 and 2.161.0): the new tasks are admitted by the rebuilt output (v1.0.0 took the earlier output name from the standard writer, which the validator refused: retracted-and-consumed).
Usage: sen0414_lineage_repair2_v1_1_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.1.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S; lit = W.lit; now = W.now
CR = "ex:CR2_Repair2"; IA = "ex:IA2_Repair2"; REV = "ex:Revision_Lineage2_Backlog3"
OLD = "ex:Out2_BacklogR2"; NEW = "ex:Out2_BacklogR3"
OWNER = ("Owner's standing rule (2026-10-23, relayed by the course coordinator and recorded as relayed): \"Repairs should change the priority of the PBIs or the tasks.\" A repair entering the backlog re-ranks the open items with the register's own ranking discipline "
         "(PriorityScore, inputs from observable facts), the ranking is recorded as dated records, starts follow it, and a repair outranks the work it blocks. The course coordinator's direction of the same day: run the change route for both findings now, put the template repair "
         "(a new template version with its own check) and the runner repair ahead of the page builds, re-score dated, release the page builds only after the repairs are controlled; the owner is in class and needs the pages as soon as possible.")
FACTS = ("MEASURED FACTS (the lineage agent, 2026-10-23, Playwright 1.56.0, Chromium, 1400x900; repeatable). FINDING 1, the template: pages built on template 9.52.1 fail two features that 9.34.0 owns and that the shipped pages v9_28_0 and pages built on 9.50.0 from the same page data pass: "
         "'a focused concept starts at the top' (first paragraph 410 px from the top, limit 240; 9.50.0: 210 px) and 'small phone (360px)' (the explorer-drawer check). ROOT CAUSE: the description comment at the head of course_page_template_v9_52_1.html (text carried over from the sibling's 9.52.0 and 9.52.1 descriptions) contains two literal '-->' sequences "
         "(36 comment closers against 34 openers); the first closes the comment at byte 1157, so about 1,157 characters of description prose are rendered as visible text of the page body above the header: the header starts at 190 px instead of 0, every concept sits 200 px lower, and at 360 px the layout of the drawer check changes. "
         "The comment of 9.50.0 is balanced (33 and 33). The character-set rule is not affected (the declaration stays at byte 37). The executor's own chapter 10 log shows both features passing; the lineage agent re-ran the executor's own scratch page file with its own driver and got FAIL on both, "
         "so the difference lies in what the executor's run measured, not in the file (the repair task must state why). FINDING 2, the runner: 08-tooling/sen0414_page_test_run_v1_0_0.py names sen0414_page_test_v9_34_0.py in its code (line 24); a run through it never executes the features P1 to P12 of 9.36.0.")
ST_T = "ST_Std_TemplateFix"; ST_R = "ST_Std_Runner"
TK_T = "TK_Std_Template_R2"; TK_TV = "TK_Std_TemplateFix_Verify"; TK_R = "TK_Std_Runner"; TK_RV = "TK_Std_Runner_Verify"
AC_T = "AC2R_TemplateFix"; AC_R = "AC2R_Runner"
OPEN = {  # open stories at this revision: (business value, time criticality, risk reduction, job size h, why)
    "ST_Std_TemplateFix": (8, 20, 20, 1.5, "the repair of a template that shows its own description as page text; every page built from it would ship the defect and fail two old features; it blocks 3 page builds and is cheapest now, before any page is built"),
    "ST_Std_Runner":      (5, 13, 13, 1.0, "the repair of the runner that never runs the new page test; the page builds and their control need it; it blocks 3 page builds and is independent of the template repair"),
    "ST_Std_Charset":     (8, 20, 20, 1.0, "its tool part is controlled; inputs unchanged"),
    "ST_Std_DeckTools":   (13, 20, 8, 1.5, "controlled; awaits its completion record; inputs unchanged"),
    "ST_Std_PageTools":   (13, 20, 13, 9.0, "template and page test Done; the old-feature regression is open and now depends on the template repair; inputs unchanged"),
    "ST_Std_Deck_Ch06":   (20, 20, 3, 5.5, "controlled; awaits its completion record; inputs unchanged"),
    "ST_Std_Page_Ch06":   (20, 20, 3, 4.0, "the next page, BLOCKED by the two repairs (dependsOn); inputs unchanged, so it ranks below the repairs that release it"),
    "ST_Std_Deck_Ch07":   (20, 13, 3, 5.5, "controlled; inputs unchanged"),
    "ST_Std_Page_Ch07":   (20, 13, 3, 4.0, "blocked by the two repairs; follows chapter 6; inputs unchanged"),
    "ST_Std_Deck_Ch08":   (20, 8, 3, 5.5, "controlled; inputs unchanged"),
    "ST_Std_Page_Ch08":   (20, 8, 3, 4.0, "blocked by the two repairs; follows chapter 7; inputs unchanged"),
}
GH_T = ("Owner-directed repair (ex:CR2_Repair2). Given the template 9.52.1 (its description comment closes early at byte 1157), the page builder v4_18_0 and the page test 9.36.0, when the NEW files course_page_template_v9_52_2.html and sen0414_page_build_v4_18_1.py are made, then ALL of: "
        "(1) the files are new and 9.52.1 and v4_18_0 are byte-identical; (2) in the new template every comment is balanced (the count of '<!--' equals the count of '-->' and no '-->' lies inside a comment), the declaration <meta charset=\"utf-8\"> is still the first child of head below byte 512, and every id and hook of 9.52.1 is kept; "
        "(3) a page built on it has no visible text between <body> and the header (the header starts at 0 px at 1400x900); the builder v4_18_1 refuses a template that breaks (2) or a built page that breaks this; "
        "(4) scratch pages of chapters 1 and 10 built on 9.52.2 run through the page test 9.36.0 and 9.34.0 end exit 0 with no failed feature, including 'a focused concept starts at the top' and 'small phone (360px)', and widgets, features and gates not below the stored result of the shipped page; "
        "(5) the report states why the executor's earlier log of template 9.52.1 showed both features passing; (6) no committed file is edited; results as printed, measured by the controller from the files and by its own page-test runs.")
GH_R = ("Owner-directed repair (ex:CR2_Repair2). Given the runner sen0414_page_test_run_v1_0_0.py (names the page test 9.34.0), when the NEW file sen0414_page_test_run_v1_1_0.py is made, then ALL of: "
        "(1) the file is new and v1_0_0 is byte-identical; (2) by default it runs the page test 9.36.0 (the environment PAGE_TEST_FILE can name another test file, for example 9.34.0), keeps the interface of v1_0_0 (NN and PAGEVER, the key-substituted copy, the TEST key, output outside the repository, exit 0 only when the test exits 0, every widget passes and no [FAIL] line), and also accepts the environment FORCE_STANDARD and a page file outside the repository (PAGE_FILE); "
        "(3) run on the shipped page of chapter 8 v9_28_0 with FORCE_STANDARD=1 it prints the P features and ends non-zero on the measured defects (P11, P12 at byte 9293, the chapter-code P2), and run on a scratch page built from the repaired template it prints the P features passing; (4) no committed file is edited; results as printed, re-run by the controller.")


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Repair: the page template 9.52.1 shows its description as page text and the page-test runner never runs the new page test; repairs re-rank the open work"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(OWNER + " The scope does not move outward: the repairs concern files the scope already names (the new template and the new page-test tools, ex:Del2_StdTools); what is added is two repair stories with controller tasks, a re-scoring of the open stories and dependencies of the page builds on the repairs. Pending until the ScopeChange that records it."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the template and runner repairs change in the iteration, with the facts measured before they are planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACTS + " WHAT MOVES: the Backlog stage of the second lineage is revised once more (a story, criterion, test cases and tasks are added; the digest moves); the tasks already Done stay Done and are not re-dated; "
                    "the page builds of chapters 6, 7 and 8 (Ready, not begun) gain dependencies on the template repair's verification, the runner repair's verification and the open regression check, so they are released only after the repairs are controlled; "
                    "the open stories are re-scored with WSJF (inputs from observable facts) and the starts follow the score: the repairs first. Not in the plan: pages of other chapters built from the same template (reported, not changed); any edit of a committed file."))
    return t + cr + ia, "ChangeRequest ex:CR2_Repair2 (Pending) and ImpactAssessment ex:IA2_Repair2 for two findings of the controller (template 9.52.1 shows its description as page text, root cause two literal comment closers; the runner names page test 9.34.0) and the owner's rule that repairs re-rank the open work; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (OWNER + " Stories, criteria and tasks are added to the lineage's closed Backlog stage, which moves its digest (G117, G125 route 2): a StageRevision from the Backlog stage, never from the Mission; the change request ex:CR2_Repair2 and the impact assessment ex:IA2_Repair2 were recorded first. "
              "This version retracts the Backlog output ex:Out2_BacklogR2 and rebuilds nothing; the next version closes the Backlog stage again as ex:Out2_BacklogR3 and re-admits every item, the Done tasks included, without re-dating them; a third version fills the commit. "
              "The retracted output and its digest stay as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: the template and runner repairs and the re-ranking of the open work"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) for the template and runner repairs: the Backlog output Out2_BacklogR2 is retracted; nothing is rebuilt in this version."


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now()
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR2\b", t)); assert cnt >= 20, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR2\b", "admittedByOutput " + NEW, t)
    L = []
    for sid, (bv, tc, rr, size, why) in OPEN.items():
        val = (bv + tc + rr) / size
        if sid in (ST_T, ST_R):
            continue
        i, j = blk(t, sid); b = t[i:j]
        m = re.search(r"backlog:hasPriorityScore ex:(Score2S_%s)\b" % sid, b); assert m, sid
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:Score3R_%s" % sid, 1) + t[j:]
    for sid, (bv, tc, rr, size, why) in OPEN.items():
        val = (bv + tc + rr) / size
        L.append('ex:Score3R_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Re-scored on %s UTC under the owner's rule that repairs re-rank the open work (ex:CR2_Repair2). "
                             "Inputs from observable facts: job size is the sum of the story's task estimates in this register; time criticality 20 = the class of 2026-10-23 or work that blocks it, 13 = blocks later work, 8 = later in the chapter order; %s. The earlier record is kept as history." % (bv, tc, rr, size, val, n, why))))
    L.append('''
ex:TC2R_Passes a backlog:TestCase ; rdfs:label "Build scratch pages on the repaired template and run the old and the new page tests; the controller re-runs them"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(a)s, ex:%(b)s ; backlog:coversScenario ex:Scen2S_P_Passes ; backlog:runsOnData ex:Data2R_Passing ;
    backlog:hasCaseText "Pages of chapters 1 and 10 built on template 9.52.2: no visible text before the header, the page tests 9.36.0 and 9.34.0 end exit 0 with no failed feature; the runner v1_1_0 runs 9.36.0 and prints the P features." .
ex:TC2R_NotClaimed a backlog:TestCase ; rdfs:label "Run the same checks on the template 9.52.1 and on the old runner and require that they fail"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(a)s, ex:%(b)s ; backlog:coversScenario ex:Scen2S_P_NotClaimed ; backlog:runsOnData ex:Data2R_Failing ;
    backlog:hasCaseText "A page built on template 9.52.1 fails 'a focused concept starts at the top' (410 px against 240) and 'small phone (360px)'; the runner v1_0_0 runs 9.34.0 and prints no P feature." .
ex:Data2R_Passing a backlog:TestData ; rdfs:label "Template 9.52.2, builder 4.18.1, runner 1.1.0 and scratch pages built on them"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The new files and scratch pages of chapters 1 and 10 built on them." .
ex:Data2R_Failing a backlog:TestData ; rdfs:label "Template 9.52.1 and the runner v1_0_0 as they stand"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The committed template 9.52.1 (description comment closing at byte 1157) and the committed runner v1_0_0." .
''' % dict(a=AC_T, b=AC_R))
    tools = "ex:TS2_PageTemplate, ex:TS2_PageBuilder, ex:TS2_PageTest36, ex:TS2_PageTest34"
    for ac, gh, label in ((AC_T, GH_T, "The repaired template 9.52.2 shows no text before the header and the old and new page tests end with no failed feature"),
                          (AC_R, GH_R, "The new runner runs the page test 9.36.0 and ends non-zero on the measured defects of the shipped page")):
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n'
                 '    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the controller\'s own runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC2R_Passes, ex:TC2R_NotClaimed .\n' % (
                     ac, lit(label), lit(gh), tools, lit(W.VER + "; page test 9.36.0 and 9.34.0 (Playwright 1.56.0); page template 9.52.2 and builder 4.18.1 (new files over 9.52.1 and 4.18.0); runner 1.1.0 (new file over 1.0.0)")))
    PAGEFACT = FACTS
    stories = (
        (ST_T, "Repair: the page template shows no text of its own description above the header, with its own check", AC_T, (TK_T, TK_TV), "ex:Del2_StdTools", GH_T),
        (ST_R, "Repair: the page-test runner runs the page test 9.36.0", AC_R, (TK_R, TK_RV), "ex:Del2_StdTools", GH_R),
    )
    for sid, title, ac, tks, deliv, gh in stories:
        L.append(('\nex:%(s)s a backlog:Story ; rdfs:label %(t)s@en ; backlog:hasIdentifier "%(s)s" ;\n    backlog:hasTitle %(t)s ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_18 ; backlog:admittedByOutput %(n)s ;\n    backlog:hasInvestmentCategory backlog:Cat_Maintenance ;\n'
                  '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability %(w)s ; backlog:soThat "the chapter pages show only their content and are measured by the page test that holds the standard" ;\n'
                  '    backlog:satisfiesDeliverable %(d)s ; backlog:pursuesObjective ex:Obj2_StdPages ; backlog:hasAcceptanceCriterion ex:%(ac)s ;\n'
                  '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n    backlog:decomposesInto %(tk)s ;\n    backlog:hasState backlog:Ready ;\n'
                  '    backlog:hasPriorityScore ex:Score3R_%(s)s ; backlog:standsAlone true ;\n    backlog:hasAuditNote %(note)s .\n') % dict(
                      s=sid, t=lit(title), n=NEW, w=lit(title[0].lower() + title[1:]), d=deliv, ac=ac, tk=", ".join("ex:" + x for x in tks), note=lit(OWNER + " " + FACTS)))
    NOTE_T = ("Write the NEW files 08-tooling/course_page_template_v9_52_2.html (from course_page_template_v9_52_1.html, which stays byte-identical) and 08-tooling/sen0414_page_build_v4_18_1.py (from sen0414_page_build_v4_18_0.py, byte-identical). "
              "ROOT CAUSE measured by the lineage agent (repeat it first and print it): the description comment at the head of 9.52.1 contains two literal '-->' sequences (36 closers against 34 openers; the first closes the comment at byte 1157), so about 1,157 characters of description prose are visible text above the header: header at 190 px instead of 0, first paragraph at 410 px instead of 210 on the same data. "
              "Repair: rewrite the comment so no '-->' lies inside it (keep the version history as text), keep everything else of 9.52.1 as it is (charset first in head below byte 512, ids, hooks, behaviour). The builder 4.18.1 differs from 4.18.0 only by the default template 9.52.2 and a guard: it refuses a template whose comment openers and closers differ in number or whose text between <body> and the header is not empty, and keeps the charset guard. "
              "Prove: (a) build scratch pages of chapters 1 and 10 on 9.52.2 (PAGE_SCRATCH and PAGE_DATA_DIR outside the repository; take the page data from the data builder 2.25.0 as before) and show the header at 0 px and no body text before it; (b) show that the guard refuses 9.52.1; "
              "(c) run the page tests 9.34.0 and 9.36.0 on both pages, one at a time, with the TEST key (your own key-substituting driver), and keep the logs: no [FAIL] line; (d) STATE WHY your earlier log of 9.52.1 on chapter 10 showed 'a focused concept starts at the top' and 'small phone' passing while the lineage agent's re-run of your page file failed: build the page again, compare it with the page you tested, and print the difference. "
              "Do not use the new runner or any file of the runner repair. Do not edit any committed file.")
    NOTE_R = ("Write the NEW file 08-tooling/sen0414_page_test_run_v1_1_0.py from sen0414_page_test_run_v1_0_0.py (which stays byte-identical; read it first; it names sen0414_page_test_v9_34_0.py on its line 24). The new runner: by default runs sen0414_page_test_v9_36_0.py (environment PAGE_TEST_FILE names another test file, for example sen0414_page_test_v9_34_0.py); "
              "keeps the interface of v1_0_0 (NN and PAGEVER, the key-substituted copy made by sen0414_page_key_substitute_v1_0_0.py, output outside the repository, exit 0 only when the test exits 0, every widget passes and no [FAIL] line); passes FORCE_STANDARD through; accepts the environment PAGE_FILE, a built page outside the repository, which it key-substitutes in a temporary copy (the page test reads the chapter's page data from 08-tooling/chNN-page/page_data_vPAGEVER.json: state how you provide it without leaving a file in the repository). "
              "Prove: (a) FORCE_STANDARD=1 on the shipped chapter 8 page v9_28_0 prints the P features and ends non-zero on the measured defects (P11, P12 at byte 9293, the chapter-code P2), the same as the logs in 08-tooling/pagetest36-logs; (b) on a scratch page built from any template it prints the P features; (c) the old runner still names 9.34.0 and is unchanged. Keep the logs. Do not edit any committed file.")
    for tid, title, ttype, deps, sess, est, hrs, note in (
            (TK_T, "Make page template 9.52.2 and builder 4.18.1: repair the early closing comment and guard against it", "Build", [], "SEN0414-I18-template-r2", "T0", 1.0, NOTE_T),
            (TK_R, "Write the page-test runner v1_1_0 that runs the page test 9.36.0", "Build", [], "SEN0414-I18-runner", "T0", 1.0, NOTE_R),
            (TK_TV, "Control the template repair: root cause, balanced comments, no text before the header, old and new page tests", "Verify", [TK_T], "the lineage agent", "after the template repair", 0.5,
             "Controller task (the lineage agent): re-run the check of the comments and of the text before the header on the new template and on a freshly built page, build scratch pages of chapters 1 and 10 and run the page tests 9.34.0 and 9.36.0 with the controller's own driver, require no failed feature (including 'a focused concept starts at the top' and 'small phone (360px)'), require that 9.52.1 still fails them, check that the old files are byte-identical, run the evidence bridge, and record the result."),
            (TK_RV, "Control the runner repair: it runs 9.36.0 and fails the shipped page on the measured defects", "Verify", [TK_R], "the lineage agent", "after the runner repair", 0.5,
             "Controller task (the lineage agent): re-run the new runner with FORCE_STANDARD=1 on the shipped chapter 8 page and compare with the baseline logs, run it on a scratch page, check that the old runner is byte-identical and still names 9.34.0, run the evidence bridge, and record the result.")):
        tb = W.task_block(tid, title, ttype, deps, sess, est, hrs, note).replace(W.NEWB, NEW)
        L.append(tb)
    # releases: the page builds and the regression check depend on the repairs
    for tk in ("TK_Std_Page_Ch06_Build", "TK_Std_Page_Ch07_Build", "TK_Std_Page_Ch08_Build"):
        L.append("ex:%s backlog:dependsOn ex:%s, ex:%s, ex:TK_Std_Regress .\n" % (tk, TK_TV, TK_RV))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (tk, lit("REPAIR (ex:CR2_Repair2): build the page on the repaired template course_page_template_v9_52_2.html with the page builder sen0414_page_build_v4_18_1.py (and the page-data builder v2_25_0), not on 9.52.1 (its description comment closes early and shows text above the header), and run the page tests through the runner sen0414_page_test_run_v1_1_0.py, which runs 9.36.0. The task is released only after the template repair and the runner repair are controlled and the regression check TK_Std_Regress is Done.")))
    L.append("ex:TK_Std_Regress backlog:dependsOn ex:%s .\n" % TK_T)
    L.append('ex:TK_Std_Regress backlog:hasAuditNote %s .\n' % lit("Re-planned (ex:CR2_Repair2): the check runs on the repaired template 9.52.2 once the template repair is Done; the measured failure of 9.52.1 is recorded above and is the reason for the repair."))
    for x in (ST_T, ST_R, TK_T, TK_R, TK_TV, TK_RV):
        L.append('ex:Refine3R_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_18 ;\n    backlog:hasRefinementOutcome %s .\n'
                 % (x, x, x, n, lit("Refined by the lineage agent from the controller's findings of 2026-10-23 (ex:CR2_Repair2, ex:IA2_Repair2): criterion with tools and versions, dependencies, the measured root cause or defect, and a brief to be generated from the register.")))
    for sid, tks in ((ST_T, (TK_T, TK_TV)), (ST_R, (TK_R, TK_RV))):
        L.append('ex:Plan3R_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 18"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_18 ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec2S_P, ex:Scen2S_P_Passes, ex:Scen2S_P_NotClaimed .\n' % (sid, sid, n, sid, ", ".join("ex:" + x for x in tks)))
    L.append("ex:Obj2_StdPages backlog:metricMovableBy ex:%s, ex:%s .\n" % (ST_T, ST_R))
    L.append("ex:Iter_18 backlog:hasMember ex:%s, ex:%s, ex:%s, ex:%s, ex:%s, ex:%s .\n" % (ST_T, ST_R, TK_T, TK_R, TK_TV, TK_RV))
    L.append('ex:SC2_Repair2 a backlog:ScopeChange ;\n    rdfs:label "Two repair stories and their tasks admitted into the scope: the template description comment and the page-test runner"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:%s, ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, ST_T, ST_R, lit(OWNER + " The boundary does not move outward in deliverables (ex:Del2_StdTools names the template and the page-test tools); the repair stories are admitted as the owner's standing rule requires.")))
    t, k = re.subn(r'(ex:CR2_Repair2 a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR2_Repair2 rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_Repair2; it was Pending before. The owner\'s rule and the coordinator\'s direction are the direction."@en .\n' % n[:10])
    t += "\n" + "".join(L)
    out = ('\nex:Out2_BacklogR3 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt by the stage revision for the template and runner repairs"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % S.digest(t, "Backlog")
    return t + out, "second lineage, Backlog stage rebuilt for the template and runner repairs: two repair stories with criteria, executor and controller tasks; the page builds and the regression check depend on the repairs' verification; every open story re-scored with WSJF as dated records (the repairs first); ScopeChange; change request Accepted; every item re-admitted."


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR3 set to the commit that closed it (%s); the revision is complete and no repair work is begun in this version." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
