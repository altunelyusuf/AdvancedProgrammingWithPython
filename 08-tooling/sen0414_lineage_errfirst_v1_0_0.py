#!/usr/bin/env python3
"""sen0414_lineage_errfirst v1_0_0 - change route (rulings G104, G125, G136) for a finding of the controller's reading of the first chapter 3 page run of Iteration 19, measured on 2026-10-25:
the page test 9.37.0 fails its P2 chapter-code run feature on a retrofit page for ONE example whose recorded expected result BEGINS with an error name (chapter 3 example 17, chapter 1 example 14; chapter 4 example 17 is the third by the same rule).
Root cause (read from the files, not assumed): the template 9.52.2 function ccVisual draws no chart for an output that begins with an error (regex ^(\\w*Error|Traceback|Stopped after)); the page shows the text of the error, which is the right result for the example (it equals the slide);
the test 9.37.0 (line 1604 to 1606) lets an expected error name pass the error-name check but then requires a visual for the same result; the examples of chapters 6 to 9 that show an error print it AFTER an ordinary line, so the template drew their chart and they passed.
Decision by the rules (the owner's: every example's executed result is shown as a visualisation; no gate, test or template is edited or weakened; a failing result is not worked around): the content of the three decks is corrected by NEW deck and manifest versions - the first line of the recorded result is an ordinary result, the error message follows.
Events, one new register file each (the caller validates and commits and pushes each alone):  change | retract | backlog PREV | fill PREV.   Usage: sen0414_lineage_errfirst_v1_0_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S; lit = W.lit; now = W.now
CR = "ex:CR2_ErrFirst"; IA = "ex:IA2_ErrFirst"; REV = "ex:Revision_Lineage2_Backlog10"
OLD = "ex:Out2_BacklogR9"; NEW = "ex:Out2_BacklogR10"
ST = "ST_Ret_ErrFirstFix"; AC = "AC2R_ErrFirst"; VER = "TK_Ret_ErrFirst_Verify"
FIX = {"01": ("Python Basics", "14 'Errors that teach'", "4.0.0", "4.1.0"), "03": ("Loops", "17 'A module that cannot be found'", "5.0.0", "5.1.0"), "04": ("Functions", "17 'UnboundLocalError'", "3.0.0", "3.1.0")}
DIRECTION = ("Direction of the course coordinator, 2026-10-25, recorded as relayed (executor SEN0414-I19-page-ch03 stopped with a failure of the page test 9.37.0, commits 2afb447 and 9801f99): find the root cause, decide by the rules without waiting for the owner among a new deck/manifest version, a new template version or a test finding; "
             "no gate edited or weakened, a failing result is not worked around; use the change route and re-rank; disclose that 9.37.0 failed on a new chapter. The owner's standing rules that repairs re-rank the open items and that every example's executed result is shown as a visualisation also hold.")
FACTS = ("MEASURED FACTS (the lineage agent, 2026-10-25): (1) the executor of the chapter 3 page reports 9.34.0 PASS (382 features, 0 failed) and 9.37.0 FAIL on the single feature P2 'every chapter-code example opens in the editor, runs in the page ... and shows a visualised result': '22 of 22 examples ran; 1 defects 17 A module that cannot be found: result is text, not a visualisation'; "
         "the executor of the chapter 1 page, still running, has the same single defect on example 14 'Errors that teach' (its log 08-tooling/ch01-page/logs_iter19/page_test_9_37_0_run1_full_output.log); the chapter 2 page passes the feature. "
         "(2) CAUSE, read from the files: the recorded expected result of chapter 3 example 17 in 03-materials/ch03/page/chapter_code_ch03_v1_0_0.json is 'ModuleNotFoundError - No module named nosuchmodule' on its FIRST line; the template 9.52.2 function ccVisual (in every v9_90_0 page) sets err = /^(\\w*Error|Traceback|Stopped after)/ on the trimmed output and draws no chart then, so the page shows the text (which equals the slide, correct); "
         "the page test 9.37.0 (lines 1604 to 1606 of sen0414_page_test_v9_37_0.py) tests the error name only with the pattern 'Traceback|NameError|Error:' (a colon), so the form 'ModuleNotFoundError -' is not seen as an error, and for 'ValueError: ...' (chapter 1 example 14) the name passes as expected but the next line still demands a visual; an expected error that is the FIRST line therefore always fails. "
         "Why chapters 6 to 9 passed: every example of theirs that shows an error prints it after an ordinary line (chapter 6 example 2 'e 3' then IndexError; chapter 1 examples 9, 10 and 11 print ordinary lines first and pass); the change request ex:CR2_Retest37 built 9.37.0 on the chapter 6 case. "
         "(3) A scan of all five retrofit manifests (03-materials/ch0[1-5]/page/chapter_code_ch0N_v1_0_0.json) for a recorded result whose first line matches the template's pattern finds exactly three: chapter 1 example 14, chapter 3 example 17, chapter 4 example 17 ('UnboundLocalError NameError'); chapters 2 and 5 have none. "
         "(4) The executor of the chapter 3 page added 08-tooling/ch03-deck/examples_out_v3_0_0.json (a new file, committed in 2afb447, input of the page-data builder): the controller checked it - 22 examples, ids equal to the manifest's in order, the code of every example equal to the manifest's, no committed file modified. "
         "(5) The three options: a TEST change (accept text for an expected error) would weaken a gate that was just controlled; a TEMPLATE change (draw a chart for an expected error) would make a new template version that the pages of chapters 1 to 5 and 6 to 9 are not built on; neither is chosen. The decks' content is the free variable: the owner's rule shows every executed result as a visualisation, and an error example is better taught with a visible line before the error message. "
         "DISCLOSURE: the page test 9.37.0 failed on a new chapter. It is a FINDING about the interplay of the test and the template (an expected error as the first line cannot satisfy the test); it is reported openly, the test and the template are not edited, and the finding is not worked around.")
GH = ("Given the decks 4.0.0 (chapter 1), 5.0.0 (chapter 3) and 3.0.0 (chapter 4), controlled as Done, whose chapter-code manifests 1.0.0 record, for chapter 1 example 14, chapter 3 example 17 and chapter 4 example 17, a result that BEGINS with an error name (the template draws text, not a visualisation, and the page test 9.37.0 fails the P2 run feature), "
      "when for each of the three chapters a NEW deck version (4.1.0, 5.1.0, 3.1.0) is built as a new file with a NEW manifest 03-materials/chNN/page/chapter_code_chNN_v1_1_0.json in which only that example is changed - its code prints an ordinary result line first and the error message after it, the slide shows the same code and result and the explanation clue is kept - then ALL of: "
      "(1) every file is new and every committed file is byte-identical; (2) the deck standard check v1_0_0 prints 13 of 13 PASS including M1, and the deck overlap check v1_0_0 prints CLEAN, on each new deck; (3) the new manifest differs from 1.0.0 in that one example only (code and expected), every other example, name, order and concept link identical, and equals the deck's code boxes (M1); "
      "(4) every example of the manifest run now under Python 3.13 prints its recorded expected result, and in no manifest of chapters 1 to 5 does the first line of a recorded result match ^(\\w*Error|Traceback|Stopped after) (the controller scans all five); (5) the controller renders the changed slide and reads it; "
      "(6) the pages of chapters 1, 3 and 4 are built on the manifests 1.1.0 and the controller's page test 9.37.0 on them ends with no failed feature (that is the criterion of their page-build tasks); no gate, test or template is edited.")
NOTE_FIX = ("RETROFIT REPAIR: build a NEW version of the deck of chapter %(ch)s (%(name)s), %(new)s over the controlled %(old)s, and a NEW chapter-code manifest 03-materials/ch%(ch)s/page/chapter_code_ch%(ch)s_v1_1_0.json, changing ONLY example %(ex)s. "
            "The cause: the recorded result of that example begins with an error message; the page template draws no chart for an output that begins with an error, so the page test 9.37.0 fails its P2 run feature for it (the page shows the error text, which equals the slide). "
            "The change: edit the example's code so that it first prints an ordinary result line (a value, a type, a count - something the example's lesson uses) and prints the error message after it, so the recorded result's FIRST line is not an error name; the error message stays in the result and on the slide, and the explanation clue on the slide is updated to match. "
            "Do it by a NEW version of the deck generator and of the example data (new files over the ones of the controlled deck; read how the controlled deck 08-tooling/ch%(ch)s-deck/ was built), not by editing a committed file. Change nothing else: every other slide, example, name, order, concept link, story and picture is that of the controlled deck. "
            "Prove, and report as printed: the deck standard check v1_0_0 on the new deck (13 of 13 PASS including M1); the deck overlap check v1_0_0 (CLEAN); a script comparing manifest 1.0.0 and 1.1.0 that lists every difference (exactly the one example); every example of the new manifest run under /usr/bin/python3.13 prints its recorded result; a scan that no recorded first line of the manifest matches ^(\\\\w*Error|Traceback|Stopped after); the generator's self-check. "
            "Do not touch the page, the page data or any research file: the page-build executor of this chapter rebuilds the page on the new manifest after the lineage agent controls your deck. A committed file is never edited; STOP and report if the task cannot be satisfied without editing one, a gate, a test, a template or a threshold. Report commit SHAs and the verbatim output of every run, and say what failed if anything.")
NOTE_VER = ("Controller task (the lineage agent): for chapters 1, 3 and 4 run the deck standard check and the deck overlap check on the new decks (13 of 13 including M1; CLEAN), compare the manifests 1.0.0 and 1.1.0 (exactly the named example differs), run every example under Python 3.13, scan the five chapters' manifests (1.1.0 where it exists, else 1.0.0) for a recorded first line that begins with an error name (none may), render and read the changed slide of each deck, "
            "check by git that no file committed before this change is modified; run the evidence bridge and record the result, Done or NOT MET, no waiver. The pages of chapters 1, 3 and 4 are then rebuilt on the new manifests by their page-build tasks and controlled by the page criteria.")


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Page test 9.37.0 fails on an example whose recorded result begins with an error message (chapters 1, 3 and 4): new deck and manifest versions with the error shown after an ordinary result line"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(DIRECTION + " The scope does not move outward: the retrofit of chapters 1 to 5 is the scope; what is added is one repair story with three deck-fix tasks and a controller task."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the error-first repair changes in the iteration, with the facts measured before it is planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACTS + " WHAT MOVES: the Backlog stage is revised once more (G125 route 2): one story, one criterion, test cases and four tasks are added to Iteration 19; the page-verify tasks of chapters 1, 3 and 4 gain the dependency on the controller task; "
                    "the deck-verify tasks already Done stay Done and are not re-dated (the controlled decks 4.0.0, 5.0.0 and 3.0.0 stay as history); the page-build tasks of chapters 1, 3 and 4 are in progress and are re-briefed: they are controlled only on the manifest 1.1.0 (chapter 3 and 1 after their executors rebuild); chapters 2 and 5 are not affected. "
                    "RE-RANKING (WSJF, the owner's rule that repairs re-rank the open items): the repair story, which blocks the control of the pages of chapters 1, 3 and 4, ranks first; the five chapter stories are re-scored with the risk reduction of chapters 1, 3 and 4 raised by the measured defect. Not in the plan: a waiver, an edit of a gate, test or template, a rebaseline."))
    return t + cr + ia, "ChangeRequest ex:CR2_ErrFirst (Pending) and ImpactAssessment ex:IA2_ErrFirst: the page test 9.37.0 fails on a chapter-code example whose recorded result begins with an error message (chapters 3, 1 and 4); decision: new deck and manifest versions; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (DIRECTION + " A story, a criterion, test cases and four tasks are added to the closed Backlog stage and the dependencies and scores of open items move: its digest moves (G117, G125 route 2): a StageRevision from the Backlog stage, never from the Mission; the change request and the impact assessment were recorded first. "
              "This version retracts the Backlog output ex:Out2_BacklogR9 and rebuilds nothing; the next version closes the Backlog stage again as ex:Out2_BacklogR10 and re-admits every item without re-dating any; a third version fills the commit. The retracted output and its digest stay as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: the error-first repair of the decks of chapters 1, 3 and 4"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) for the error-first repair: the Backlog output Out2_BacklogR9 is retracted; nothing is rebuilt in this version."


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now(); L = []
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR9\b", t)); assert cnt >= 100, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR9\b", "admittedByOutput " + NEW, t)
    # re-score the five chapter stories (inputs read from their latest record)
    for ch in ("01", "02", "03", "04", "05"):
        sid = "ST_Plan_Retrofit_Ch" + ch; i, j = blk(t, sid); b = t[i:j]
        m = re.search(r"backlog:hasPriorityScore ex:Score(\d+)_%s\b" % sid, b); assert m, sid
        r0 = t[blk(t, "Score%s_%s" % (m.group(1), sid))[0]:blk(t, "Score%s_%s" % (m.group(1), sid))[1]]
        q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0); assert q, sid
        bv, tc, rr, size = int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4))
        extra = 1 if ch in FIX else 0; rr2 = rr + extra; val = (bv + tc + rr2) / size; nn = int(m.group(1)) + 1
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:Score%d_%s" % (nn, sid), 1) + t[j:]
        L.append('ex:Score%d_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            nn, sid, val, n, lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Re-scored on %s UTC under the owner's rule that repairs re-rank the open work (ex:CR2_ErrFirst): %s" % (
                bv, tc, rr2, size, val, n, ("risk reduction %d -> %d (the measured defect: the chapter's manifest has an example whose result begins with an error message, which fails the page test 9.37.0)." % (rr, rr2)) if extra else "inputs unchanged; re-run because the Backlog output moved and the repair story outranks it."))))
    # the new story, criterion, cases, tasks
    tasks = ["TK_Ret_Ch%s_Deck_Fix" % c for c in FIX] + [VER]
    L.append('''
ex:TC2E_Passes a backlog:TestCase ; rdfs:label "Run the deck checks and the example runs on the new decks of chapters 1, 3 and 4; the controller re-runs them"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(a)s ; backlog:coversScenario ex:Scen2S_D_Passes ; backlog:runsOnData ex:Data2E_Passing ;
    backlog:hasCaseText "The deck standard check prints 13 of 13 PASS including M1 and the overlap check CLEAN on each new deck; the manifests 1.1.0 differ from 1.0.0 in one example each; every example runs under Python 3.13 to its recorded result; no recorded first line of chapters 1 to 5 begins with an error name." .
ex:TC2E_NotClaimed a backlog:TestCase ; rdfs:label "Scan the committed manifests 1.0.0 and require the scan to find the three examples"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(a)s ; backlog:coversScenario ex:Scen2S_D_NotClaimed ; backlog:runsOnData ex:Data2E_Failing ;
    backlog:hasCaseText "The scan over the committed manifests 1.0.0 of chapters 1 to 5 finds chapter 1 example 14, chapter 3 example 17 and chapter 4 example 17, and the page test 9.37.0 on the chapter 3 page fails the P2 run feature on example 17 (the executor's log and the controller's re-run): the scan is not a tool that passes everything." .
ex:Data2E_Passing a backlog:TestData ; rdfs:label "The new decks and manifests 1.1.0 of chapters 1, 3 and 4"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The committed new decks and manifests; the controlled decks and manifests 1.0.0 as history." .
ex:Data2E_Failing a backlog:TestData ; rdfs:label "The committed manifests 1.0.0 of chapters 1 to 5 and the chapter 3 page v9_90_0"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "Committed files, unchanged." .
''' % dict(a=AC))
    L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS2_DeckStdCheck, ex:TS2_DeckOverlap, ex:TS2_PageTest37 ;\n'
             '    backlog:measuredWithVersion "deck standard check v1_0_0; deck overlap check v1_0_0; page test 9.37.0 through runner v1_1_0; Python 3.13 for the example runs" ;\n    backlog:satisfiedByArtifact "the new files cited by SHA-256, the controller\'s own runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC2E_Passes, ex:TC2E_NotClaimed .\n' % (
                 AC, lit("No chapter-code example of chapters 1 to 5 has a recorded result that begins with an error message, so that the page shows every result as a visualisation and the page test 9.37.0 is not failed by it"), lit(GH)))
    L.append(('\nex:%(s)s a backlog:Story ; rdfs:label %(t)s@en ; backlog:hasIdentifier "%(s)s" ;\n    backlog:hasTitle %(t)s ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_19 ; backlog:admittedByOutput %(n)s ;\n    backlog:hasInvestmentCategory backlog:Cat_Maintenance ;\n'
              '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability %(w)s ; backlog:soThat "every example of the chapter shows its executed result as a visualisation on the page, as the deck does" ;\n'
              '    backlog:satisfiesDeliverable ex:Del2_StdDecks ; backlog:pursuesObjective ex:Obj2_StdDecks ; backlog:hasAcceptanceCriterion ex:%(ac)s ;\n'
              '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n    backlog:decomposesInto %(tk)s ;\n    backlog:hasState backlog:Ready ;\n'
              '    backlog:hasPriorityScore ex:Score1_%(s)s ; backlog:standsAlone true ;\n    backlog:hasAuditNote %(note)s .\n') % dict(
                  s=ST, t=lit("Repair: the decks of chapters 1, 3 and 4 show the error message of an error example after an ordinary result line"), n=NEW,
                  w=lit("an error example whose recorded result starts with an ordinary line, so the page can draw it"), ac=AC, tk=", ".join("ex:" + x for x in tasks), note=lit(DIRECTION + " " + FACTS)))
    val = (20 + 20 + 3) / 3.5
    L.append('ex:Score1_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
        ST, val, n, lit("WSJF = (business value 20 + time criticality 20 + risk reduction 3) / job size 3.5 h = %.2f. Business value 20 and time criticality 20 as chapter 1, the first of the owner's chapters, which it blocks; risk reduction 3 = the three examples measured failing; job size = three deck fixes of 1.0 h and the control of 0.5 h (estimates, G120). Scored on %s UTC (ex:CR2_ErrFirst): a repair outranks the work it blocks." % (val, n))))
    for c, (name, ex, old, new) in FIX.items():
        tid = "TK_Ret_Ch%s_Deck_Fix" % c
        note = NOTE_FIX % dict(ch=c, name=name, new=new, old=old, ex=ex)
        L.append(W.task_block(tid, "Repair the deck of chapter %d (%s): the result of example %s shows an ordinary line before the error message" % (int(c), name, ex.split()[0]), "Build", ["TK_Ret_Ch%s_Deck_Verify" % c], "SEN0414-I19-deckfix-ch" + c, "T0", 1.0, note).replace(W.NEWB, NEW).replace(W.ITER, "ex:Iter_19"))
    L.append(W.task_block(VER, "Control the repaired decks of chapters 1, 3 and 4 and the scan of the manifests of chapters 1 to 5", "Verify", ["TK_Ret_Ch%s_Deck_Fix" % c for c in FIX], "the lineage agent", "after the deck fixes", 0.5, NOTE_VER).replace(W.NEWB, NEW).replace(W.ITER, "ex:Iter_19"))
    # the page-verify tasks of chapters 1, 3, 4 wait for the controller task; the page builds are re-briefed (notes)
    for c in FIX:
        vi, vj = blk(t, "TK_Ret_Ch%s_Page_Verify" % c); vb = t[vi:vj]
        m = re.search(r"backlog:dependsOn ([^;]*);", vb); assert m, c
        t = t[:vi] + vb.replace(m.group(0), "backlog:dependsOn %s, ex:%s ;" % (m.group(1).strip(), VER), 1) + t[vj:]
        L.append('ex:TK_Ret_Ch%s_Page_Build backlog:hasAuditNote %s .\n' % (c, lit("Re-planned %s UTC (ex:CR2_ErrFirst): the page is controlled only on the chapter-code manifest 1.1.0 of the repaired deck (new file by the task ex:TK_Ret_Ch%s_Deck_Fix, controlled by ex:%s). The page test 9.37.0 on the first page failed its P2 run feature on the example whose result begins with an error message; this is a finding about the interplay of test and template, not yours to chase, and no gate, test or template is to be edited. When the lineage agent tells the coordinator that the deck is controlled, rebuild the page as a NEW page version file on the manifest 1.1.0 and run 9.37.0 and 9.34.0 again." % (n, c, VER))))
    for x in [ST] + tasks:
        L.append('ex:Refine5_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_19 ;\n    backlog:hasRefinementOutcome %s .\n'
                 % (x, x, x, n, lit("Refined by the lineage agent from the controller's measurement of 2026-10-25 (ex:CR2_ErrFirst, ex:IA2_ErrFirst): criterion with tools and versions, dependencies, the measured cause, and a brief to be generated from the register.")))
    L.append('ex:Plan5_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 19"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_19 ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec2S_D, ex:Scen2S_D_Passes, ex:Scen2S_D_NotClaimed .\n' % (ST, ST, n, ST, ", ".join("ex:" + x for x in tasks)))
    L.append("ex:Iter_19 backlog:hasMember ex:%s, %s .\n" % (ST, ", ".join("ex:" + x for x in tasks)))
    L.append('ex:SC2_ErrFirst a backlog:ScopeChange ;\n    rdfs:label "One repair story and its four tasks admitted into the scope"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, ST, lit(DIRECTION + " The boundary does not move outward in deliverables (the decks of chapters 1, 3 and 4 are in the retrofit scope); the repair story is admitted as the owner's standing rule requires.")))
    t, k = re.subn(r'(ex:CR2_ErrFirst a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR2_ErrFirst rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_ErrFirst; it was Pending before. The coordinator\'s direction is the direction; the owner is not waited for."@en .\n' % n[:10])
    t += "\n" + "".join(L)
    out = ('\n%s a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt by the stage revision for the error-first repair of the decks of chapters 1, 3 and 4"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (NEW, S.digest(t, "Backlog"))
    return t + out, "second lineage, Backlog stage rebuilt for the error-first repair: one repair story with criterion, three deck-fix tasks and a controller task; the page-verify tasks of chapters 1, 3 and 4 depend on the controller task; the page builds re-briefed by note; the chapter stories re-scored; ScopeChange; change request Accepted; every item re-admitted."


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR10 set to the commit that closed it (%s); the revision is complete and no work is begun in this version." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
