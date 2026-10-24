#!/usr/bin/env python3
"""sen0414_lineage_retest37 v1_0_0 - change route (rulings G104, G125, G136) for a finding of the controller's reading of the first chapter 6 page run, measured on 2026-10-24:
the page test 9.36.0 reads the result of a chapter-code example before the example has finished (it accepts the placeholder text 'Running...' as a result), and it flags an example whose own expected
result is an error message (chapter 6, example 2, the book's IndexError demonstration). The sibling course restated its page criteria on a corrected test 9.37.0 (new file); this register does the same on its own corrected file.
Events, one new register file each (the caller validates and commits and pushes each alone):  change | retract | backlog PREV | fill PREV
  change   - ChangeRequest ex:CR2_Retest37 (Pending) and ImpactAssessment ex:IA2_Retest37 with the measured facts.
  retract  - StageRevision from the Backlog stage: retracts ex:Out2_BacklogR4; status LS_Objectived.
  backlog  - Backlog output ex:Out2_BacklogR5; every admitted item re-admitted; the story ST_Std_PageTest37 with its criterion, executor task and controller task; the criteria of the chapter 6 and chapter 9 pages restated on 9.37.0;
             the verify tasks of those pages depend on the controller task; the open stories re-scored; ScopeChange; the change request Accepted.
  fill     - closedAtCommit of ex:Out2_BacklogR5.
Usage: sen0414_lineage_retest37_v1_0_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S; lit = W.lit; now = W.now
CR = "ex:CR2_Retest37"; IA = "ex:IA2_Retest37"; REV = "ex:Revision_Lineage2_Backlog5"
OLD = "ex:Out2_BacklogR4"; NEW = "ex:Out2_BacklogR5"
ST = "ST_Std_PageTest37"; TK = "TK_Std_PageTest37"; TKV = "TK_Std_PageTest37_Verify"; AC = "AC2R_PageTest37"
DIRECTION = ("Direction of the course coordinator, 2026-10-24, recorded as relayed: the known race in page test 9.36.0 (the chapter-code step reads an example's result while it still shows 'Running...') may hit the SEN0414 pages; the sibling course restated its page criteria on a corrected test 9.37.0; "
             "decide by the change route, without waiting for the owner, whether the chapter 6 and chapter 9 page criteria should name a corrected SEN0414 test, only if the executors actually hit it; disclose in one line. The owner's standing rule that work the lineage enforces but the actual work misses must be dealt with also holds.")
FACTS = ("MEASURED FACTS (the lineage agent, 2026-10-24, Playwright 1.56.0, Chromium 1366x768): the executor of the chapter 6 page ran the page test 9.36.0 on its page (commit ff8dedf, log 08-tooling/ch06-page/logs_iter18/page_test_9_36_0_run1.log): exit with the feature "
         "'P2 every chapter-code example opens in the editor, runs in the page ... and shows a visualised result' FAILING with 2 defects out of 24 examples: '2 Lists of lists and a wrong index' and '24 Coin Flip Streaks: result is text, not a visualisation'. The lineage agent's own probe of the same page (first example of a session: the page loads Python on the first run, 3.7 s) "
         "shows the cause of both: the test waits only until the result element holds ANY text (line 1597 of sen0414_page_test_v9_36_0.py: textContent length above 0 or an svg/canvas/img/table) and then reads after 300 ms; the page writes the placeholder 'Running...' into that element when Run is clicked, so a result "
         "slower than about 0.5 s is read as the text 'Running...' with no visual (examples 2 and 24 read exactly that: {t: 'Running...', v: false}); once the placeholder is gone the same examples show 'code -> Python -> lines in a result card (3716 ms and 622 ms) same result as on the slide' with the visual present. "
         "The second cause is separate: the test flags a result whose first 160 characters contain 'Error:' (line 1600), and chapter 6 example 2 is the book's IndexError demonstration, whose recorded expected result in the deck's manifest ends 'IndexError: list index out of range' and which the page reproduces ('same result as on the slide'); "
         "the pages of chapters 7 and 8 passed because their error demonstrations print the error name without a colon. The sibling's corrected file (/home/claude/sen0401/08-tooling/sen0401_page_test_v9_37_0.py, controlled in its register) changes only the wait for the placeholder; it does not touch the second cause. "
         "Pages that passed 9.36.0 (chapters 7 and 8) are unchanged and stay valid.")
GH = ("Owner-directed repair (ex:CR2_Retest37). Given the page test 9.36.0 (it reads a chapter-code result while the placeholder 'Running...' is shown, and flags an example whose recorded expected result is itself an error message), "
      "when the NEW file 08-tooling/sen0414_page_test_v9_37_0.py is made from 9.36.0, then ALL of: (1) the file is new and 9.36.0 and 9.34.0 are byte-identical; (2) the ONLY differences from 9.36.0 are: the version line and a comment naming this change; the wait in the P2 chapter-code step, which after Run waits until the result element no longer shows the placeholder "
      "'Running...' (three dots or the ellipsis character) and holds text or a visual, same 90 s bound; and the error check of that step, which flags 'Traceback', 'NameError' or 'Error:' in a result only when the same text is NOT part of the example's recorded expected result in the manifest; every other feature, threshold and message is that of 9.36.0 (a diff proves it); "
      "(3) run through the runner v1_1_0 with PAGE_TEST_FILE=sen0414_page_test_v9_37_0.py, the page of chapter 7 v9_90_0 and the page of chapter 8 v9_90_0 end exit 0 with no failed feature and the same widgets and features as under 9.36.0, and the page of chapter 6 v9_90_0 ends exit 0 with no failed feature (examples 2 and 24 now read their final results); "
      "(4) four fixtures (scratch pages or manifests outside the repository) prove the check: a result that stays text-only fails; a real crash (a Python error that is NOT in the example's recorded expected result) fails; a slow visual (result shown after the placeholder, later than 0.5 s) passes; an example whose recorded expected result is itself an error message and whose page shows it passes; "
      "(5) no committed file is edited; results as printed, measured by the controller from the files and by its own page-test runs, serially under the shared lock.")
NOTE_T = ("Write the NEW file 08-tooling/sen0414_page_test_v9_37_0.py from sen0414_page_test_v9_36_0.py (which stays byte-identical; read it first). Change ONLY: (a) __version__ = \"9.37.0\" and a comment line naming this change (ex:CR2_Retest37); "
          "(b) in the P2 chapter-code run step (the loop over CCI that clicks [data-cc-run], about line 1597), replace the wait with one that returns true when the result element [data-cc-result] exists, its trimmed text is NOT the placeholder matched by /^Running(\\.\\.\\.|\\u2026)$/ and it holds text or an svg/canvas/img/table (same 90000 ms bound), keep the 300 ms pause and the read; "
          "(c) in the same step, flag a result for 'Traceback|NameError|Error:' only when the matched text does not occur in the example's recorded expected result (CCI[i] carries the manifest example; use its 'expected' field, normalised for whitespace) - an example whose expected result is itself an error message, such as chapter 6 example 2, is then judged by its visual and by 'same result as on the slide' like any other. "
          "The sibling's file /home/claude/sen0401/08-tooling/sen0401_page_test_v9_37_0.py shows change (b) (read-only source, never edited; its first line of the diff against its 9.36.0 is the guide). Prove: (1) the diff of your file against 9.36.0 shows exactly (a), (b), (c); (2) run it through the runner sen0414_page_test_run_v1_1_0.py with PAGE_TEST_FILE=sen0414_page_test_v9_37_0.py on the pages of chapters 6, 7 and 8 v9_90_0, one run at a time under flock /tmp/page_test.lock, and keep every log; "
          "(3) build four fixtures outside the repository (text-only result, real crash, slow visual after 1.5 s, expected error message equal to the recorded result) and show: text-only fails, crash fails, slow visual passes, expected error passes, each with its log; "
          "(4) do not edit any committed file; report the commit SHAs, the new files and the verbatim output of every run, and say what failed if anything.")
NOTE_V = ("Controller task (the lineage agent): re-run the diff of 9.37.0 against 9.36.0 and require exactly the three changes; run the page tests 9.37.0 and 9.34.0 through the runner v1_1_0 on the pages of chapters 6, 7 and 8, one at a time under the shared lock, with the controller's own logs; require no failed feature; "
          "re-run the four fixtures (text-only fails, real crash fails, slow visual passes, expected error passes); check that 9.36.0 and 9.34.0 are byte-identical; run the evidence bridge and record the result, Done or NOT MET, no waiver.")


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Page test 9.36.0 reads a chapter-code result before it has finished and flags an expected error message: a corrected SEN0414 page test 9.37.0 for the chapter 6 and chapter 9 page criteria"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(DIRECTION + " The scope does not move outward: the page tests are files the scope already names (ex:Del2_StdTools); what is added is one repair story with a build task and a controller task, and the restatement of two page criteria on the corrected test."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the corrected page test changes in the iteration, with the facts measured before it is planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACTS + " WHAT MOVES: the Backlog stage of the second lineage is revised once more (a story, a criterion, test cases and two tasks are added; the criteria of the pages of chapters 6 and 9 name the page test 9.37.0 instead of 9.36.0; the digest moves); "
                    "the tasks already Done stay Done and are not re-dated; the pages of chapters 7 and 8 are not affected (Done on 9.36.0, with no placeholder read and no error example); the verify tasks of the chapter 6 and chapter 9 pages gain the dependency on the controller task of the corrected test; "
                    "the build tasks of those pages are not blocked (their executors run on); the open stories are re-scored. Not in the plan: any edit of a committed file or of the page test 9.36.0."))
    return t + cr + ia, "ChangeRequest ex:CR2_Retest37 (Pending) and ImpactAssessment ex:IA2_Retest37: the page test 9.36.0 reads a chapter-code result while it shows 'Running...' and flags an expected error message (measured on the chapter 6 page); a corrected test 9.37.0 for the chapter 6 and chapter 9 page criteria; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (DIRECTION + " A story, a criterion and tasks are added to the lineage's closed Backlog stage and two criteria are restated, which moves its digest (G117, G125 route 2): a StageRevision from the Backlog stage, never from the Mission; the change request ex:CR2_Retest37 and the impact assessment ex:IA2_Retest37 were recorded first. "
              "This version retracts the Backlog output ex:Out2_BacklogR4 and rebuilds nothing; the next version closes the Backlog stage again as ex:Out2_BacklogR5 and re-admits every item, the Done tasks included, without re-dating them; a third version fills the commit. The retracted output and its digest stay as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: the corrected page test 9.37.0 and the restated criteria of the chapter 6 and chapter 9 pages"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) for the corrected page test 9.37.0: the Backlog output Out2_BacklogR4 is retracted; nothing is rebuilt in this version."


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now()
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR4\b", t)); assert cnt >= 80, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR4\b", "admittedByOutput " + NEW, t)
    L = []
    # re-score the open stories (inputs read from their latest record) and score the new story
    open_st = []
    for sid in ("ST_Std_Deck_Ch09", "ST_Std_Page_Ch06", "ST_Std_Page_Ch09"):
        i, j = blk(t, sid); b = t[i:j]; m = re.search(r"backlog:hasPriorityScore ex:(Score\d+_%s)\b" % sid, b); assert m, sid
        r0 = t[blk(t, m.group(1))[0]:blk(t, m.group(1))[1]]
        q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0); assert q, sid
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:Score10_%s" % sid, 1) + t[j:]
        open_st.append((sid, int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4)), "Inputs unchanged; re-run because the Backlog output moved and a new story outranks them."))
    open_st.append((ST, 13, 20, 13, 1.5, "the corrected page test releases the control of the chapter 6 and chapter 9 pages, which the class of next week waits for; it is a repair, so it outranks the work it blocks"))
    for sid, bv, tc, rr, size, why in open_st:
        val = (bv + tc + rr) / size
        L.append('ex:Score10_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Re-scored on %s UTC under the owner's rule that repairs re-rank the open work (ex:CR2_Retest37): %s. The earlier record is kept as history." % (bv, tc, rr, size, val, n, why))))
    L.append('''
ex:TC2T_Passes a backlog:TestCase ; rdfs:label "Run the corrected page test on the pages of chapters 6, 7 and 8; the controller re-runs them"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(a)s ; backlog:coversScenario ex:Scen2S_P_Passes ; backlog:runsOnData ex:Data2T_Passing ;
    backlog:hasCaseText "The pages of chapters 6, 7 and 8 v9_90_0 under 9.37.0 through the runner v1_1_0: exit 0, no failed feature, the chapter 6 examples 2 and 24 read their final results." .
ex:TC2T_NotClaimed a backlog:TestCase ; rdfs:label "Run the corrected page test on scratch pages that must fail"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(a)s ; backlog:coversScenario ex:Scen2S_P_NotClaimed ; backlog:runsOnData ex:Data2T_Failing ;
    backlog:hasCaseText "Fixtures: a text-only result and a real crash fail the P2 run feature; a slow visual and an expected error message pass it." .
ex:Data2T_Passing a backlog:TestData ; rdfs:label "Pages of chapters 6, 7 and 8 v9_90_0 and the new test file"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The committed pages and the new file sen0414_page_test_v9_37_0.py." .
ex:Data2T_Failing a backlog:TestData ; rdfs:label "Scratch pages outside the repository with an unexpected error and with a result stuck on the placeholder"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "Two scratch pages made from a committed page, outside the repository." .
''' % dict(a=AC))
    L.append('ex:TS2_PageTest37 a backlog:ToolScript ; rdfs:label "page test 9.37.0 (Playwright 1.56.0; new file over 9.36.0: the wait in the chapter-code run step and its error check corrected, every other feature unchanged)"@en ; backlog:scriptFileName "sen0414_page_test_v9_37_0.py" ; backlog:acceptsGraphPath false .\n')
    tools = "ex:TS2_PageTest37, ex:TS2_PageTest36, ex:TS2_PageTest34"
    L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n'
             '    backlog:satisfiedByArtifact "the new file cited by SHA-256, the logs of the controller\'s own runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC2T_Passes, ex:TC2T_NotClaimed .\n' % (
                 AC, lit("The corrected page test 9.37.0 waits for the finished result of a chapter-code example and judges an expected error message by the recorded result, and every other feature is unchanged"), lit(GH), tools,
                 lit(W.VER + "; page test 9.37.0 (new file over 9.36.0), 9.36.0 and 9.34.0 (Playwright 1.56.0); runner 1.1.0 with PAGE_TEST_FILE")))
    L.append(('\nex:%(s)s a backlog:Story ; rdfs:label %(t)s@en ; backlog:hasIdentifier "%(s)s" ;\n    backlog:hasTitle %(t)s ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_18 ; backlog:admittedByOutput %(n)s ;\n    backlog:hasInvestmentCategory backlog:Cat_Maintenance ;\n'
              '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability %(w)s ; backlog:soThat "the chapter pages are measured on the finished result of every example, not on the placeholder" ;\n'
              '    backlog:satisfiesDeliverable ex:Del2_StdTools ; backlog:pursuesObjective ex:Obj2_StdPages ; backlog:hasAcceptanceCriterion ex:%(ac)s ;\n'
              '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n    backlog:decomposesInto ex:%(tk)s, ex:%(tv)s ;\n    backlog:hasState backlog:Ready ;\n'
              '    backlog:hasPriorityScore ex:Score10_%(s)s ; backlog:standsAlone true ;\n    backlog:hasAuditNote %(note)s .\n') % dict(
                  s=ST, t=lit("Repair: the page test waits for the finished result of a chapter-code example and judges an expected error message by the recorded result"), n=NEW,
                  w=lit("a page test that does not fail a page for reading a result too early or for an error message the book itself shows"), ac=AC, tk=TK, tv=TKV, note=lit(DIRECTION + " " + FACTS)))
    for tid, title, ttype, deps, sess, est, hrs, note in (
            (TK, "Make the page test 9.37.0: wait for the finished result and judge an expected error message by the recorded result", "Build", [], "SEN0414-I18-pagetest37", "T0", 0.5, NOTE_T),
            (TKV, "Control the corrected page test: the diff, the three pages, the two scratch pages that must fail", "Verify", [TK], "the lineage agent", "after the page test", 0.75, NOTE_V)):
        L.append(W.task_block(tid, title, ttype, deps, sess, est, hrs, note).replace(W.NEWB, NEW))
    # restate the criteria of the chapter 6 and chapter 9 pages on 9.37.0
    for c in ("06", "09"):
        i, j = blk(t, "AC2S_Page_Ch%s" % c); b = t[i:j]
        nb = b.replace("page test 9.36.0", "page test 9.37.0").replace("ex:TS2_PageTest36", "ex:TS2_PageTest37"); assert nb != b and nb.count("9.37.0") == b.count("9.36.0"), c
        t = t[:i] + nb + t[j:]
        L.append('ex:AC2S_Page_Ch%s backlog:hasAuditNote %s .\n' % (c, lit("RESTATED %s UTC (ex:CR2_Retest37, StageRevision %s): the criterion names the page test 9.37.0 where it named 9.36.0 (text and tool); 9.37.0 is the 9.36.0 with the wait for the finished result and the error check corrected; the page test 9.34.0 is unchanged. Every other element is as before." % (n, REV.split(":")[1]))))
        vi, vj = blk(t, "TK_Std_Page_Ch%s_Verify" % c); vb = t[vi:vj]
        assert "backlog:dependsOn ex:TK_Std_Page_Ch%s_Build ;" % c in vb, c
        t = t[:vi] + vb.replace("backlog:dependsOn ex:TK_Std_Page_Ch%s_Build ;" % c, "backlog:dependsOn ex:TK_Std_Page_Ch%s_Build, ex:%s ;" % (c, TKV), 1) + t[vj:]
        L.append('ex:TK_Std_Page_Ch%s_Build backlog:hasAuditNote %s .\n' % (c, lit("Re-planned %s UTC (ex:CR2_Retest37): the criterion now names the page test 9.37.0 (new file by the task ex:%s). Run 9.36.0 as before and say what it prints; the controller measures the page under 9.37.0 and 9.34.0, so a P2 run defect that is a result read as 'Running...' or an expected error message is not yours to chase. This task is not blocked." % (n, TK))))
    for x in (ST, TK, TKV):
        L.append('ex:Refine5_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_18 ;\n    backlog:hasRefinementOutcome %s .\n'
                 % (x, x, x, n, lit("Refined by the lineage agent from the controller's measurement of 2026-10-24 (ex:CR2_Retest37, ex:IA2_Retest37): criterion with tools and versions, dependencies, the measured cause, and a brief to be generated from the register.")))
    L.append('ex:Plan5_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 18"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_18 ;\n    backlog:plansItem ex:%s ; backlog:producesTask ex:%s, ex:%s ;\n    backlog:refinementProduces ex:Spec2S_P, ex:Scen2S_P_Passes, ex:Scen2S_P_NotClaimed .\n' % (ST, ST, n, ST, TK, TKV))
    L.append("ex:Obj2_StdPages backlog:metricMovableBy ex:%s .\n" % ST)
    L.append("ex:Iter_18 backlog:hasMember ex:%s, ex:%s, ex:%s .\n" % (ST, TK, TKV))
    L.append('ex:SC2_Retest37 a backlog:ScopeChange ;\n    rdfs:label "One page-test repair story and its tasks admitted into the scope"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, ST, lit(DIRECTION + " The boundary does not move outward in deliverables (ex:Del2_StdTools names the page-test tools); the repair story is admitted as the owner's standing rule requires.")))
    t, k = re.subn(r'(ex:CR2_Retest37 a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR2_Retest37 rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_Retest37; it was Pending before. The coordinator\'s direction is the direction; the owner is not waited for."@en .\n' % n[:10])
    t += "\n" + "".join(L)
    out = ('\nex:Out2_BacklogR5 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt by the stage revision for the corrected page test 9.37.0"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % S.digest(t, "Backlog")
    return t + out, "second lineage, Backlog stage rebuilt for the corrected page test 9.37.0: one repair story with criterion, executor task and controller task; the criteria of the chapter 6 and chapter 9 pages restated on 9.37.0; their verify tasks depend on the controller task; the open stories re-scored; ScopeChange; change request Accepted; every item re-admitted."


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR5 set to the commit that closed it (%s); the revision is complete and no work is begun in this version." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
