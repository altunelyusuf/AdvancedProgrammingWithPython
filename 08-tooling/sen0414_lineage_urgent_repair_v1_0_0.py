#!/usr/bin/env python3
"""sen0414_lineage_urgent_repair v1_0_0 - register event of the urgent Chapter 8 box after the first controls (a NEW file; writes ONE new register file, newest + 1 minor).
Event 'repair': records the real start of the controller's tasks (TK_U8_Deck_Verify, TK_U8_Page_Verify), the controller's findings as printed (so far), the OWNER'S RULING of 2026-10-30 about 03:40 Istanbul (new check files that recognise
monospace code boxes and story slides without label words are allowed beside the old deck standard check; the old checks stay unchanged; new checks need fixtures of known answer), the REPAIR task TK_U8_Deck_Check with its control task
(new urgent items of the story ST_U8_Deck, added to both open urgent interruptions as urgent items), the re-ranking that the repair causes, and says openly that the time box of the urgent box ended at 03:00 UTC.
Usage: sen0414_lineage_urgent_repair_v1_0_0.py repair"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
lit = W.lit
LOGS = "08-tooling/control-u8-logs"
START_PAGE_VERIFY = "2026-10-30T04:48:12"; START_DECK_VERIFY = "2026-10-30T04:52:24"
RULING = ("OWNER RULING of 2026-10-30 about 03:40 Istanbul (relayed by the course coordinator, recorded as relayed): new check files beside the old deck standard check, which recognise code boxes by their monospace font and story slides without label words, are allowed; "
          "the old checks stay unchanged and keep printing what they print; the new checks must have fixtures of known answer.")
FINDINGS_DECK = ("CONTROL OF THE DECK v2.1.0 (the lineage agent's own re-runs, 2026-10-30 04:5x UTC, logs in " + LOGS + "): the controller's own check (sen0414_control_urgent_deck_v1_0_0.py, selftest PASS) C1 to C8 PASS on 72 slides and 24 code boxes (no prompt, no lambda, indentation, no label words, notes 40 to 60 words, every code box compiles, slides numbered, manifest equals the code boxes in order); "
                 "the deck overlap check v1_0_0: CLEAN (0 findings); the deck teaching check v1_0_0: T1 to T6 PASS, selftest PASS with 8 fixtures; deck_notes_check PASS (72 slides); deck_fit_check: 0 frames overflowing, 0 overlapping pairs; "
                 "deck_layout_check: 1 item to look at (slide 43, a label text box 'width 20' whose box reaches x 10.05 in on a 10.00 in slide; to be judged on the rendered slide). "
                 "THE OLD DECK STANDARD CHECK v1_0_0 RUN UNCHANGED PRINTS: D2 FAIL (longest box 66 words on slide 65, 14 boxes over 30 words) and M1 FAIL ('0 of 0 deck code slides', 24 manifest examples); D3, D5 and D12 NOT_MEASURED; D1, D4, D6 to D11 PASS (PASS=8 FAIL=2 NOT_MEASURED=3). "
                 "ROOT CAUSE, read from the deck: all 14 boxes over 30 words are monospace code boxes (a code box of 66 words is the listing of an example), and the old check finds code boxes by '>>>' paragraphs and story slides by WHO/WHAT labels, which the Owner forbade; the deck keeps only the corner '>>>' brand mark. "
                 "The failing elements are named failing here; they are NOT_MEASURED and failing because of the old check's detection, not shown to be defects of the deck, and they are not passes. Under the Owner's ruling the elements are to be measured by a new check file; the criterion's element (1) stays unmet until that check exists and reports.")
FINDINGS_PAGE = ("CONTROL OF THE PAGE v9_92_1 (the lineage agent's own re-runs, 2026-10-30, logs in 08-tooling/ch08-page/logs_u8): the chapter check Page/Ch08 on v9_92_1 with page test 9.37.0, run 2 (run 1 of the stopped agent was cut off and left no result; its log is kept): RESULT FAIL, 406 features passed and 2 failed; "
                 "the failed feature is 'main-thread budget through the whole session' (load task median 95 ms, after load 322 ms over 6 long tasks, bound 200 ms), a load-dependent measure: the controller's validator and other sessions' page tests shared the two cores at that time. A FAIL stays a FAIL. All other parts of the run PASS, among them P1 to P12 (P2: the chapter-code tab lists 24 examples in the deck's order). "
                 "The five direct runs of page test 9.37.0 under the page-test lock, the leak probe v1_3_0 and the render of the 72 slides are queued behind the lock (other sessions' tests hold it in turn); their results are recorded when they exist.")
CRIT_NOTE = ("Element (1) of this criterion names the deck standard check v1_0_0 run unchanged. On the Owner's ruling of 2026-10-30 about 03:40 Istanbul the elements it cannot measure for a deck with monospace code boxes and unlabelled story slides are measured by a new check file (sen0414_deck_standard_check_v1_1_0.py, task TK_U8_Deck_Check, fixtures of known answer); "
             "the old check's printed result stays on record: D2 FAIL, M1 FAIL, D3 D5 D12 NOT_MEASURED. The criterion has no passing result until the new check reports for every element.")
TIMEBOX = ("TIME BOX, said openly: the urgent box ended at 2026-10-30T03:00:00 UTC (06:00 Istanbul) and the urgent work is not Done; the validator reports the two urgent interruptions open past their time box and the two urgent stories committed to a closed iteration. "
           "The framework's way out is to finish and resolve, or to have the Owner record a later time box with the reason; the lineage agent does not record that for him. He uses the delivered deck and page in class at 14:00 Istanbul (11:00 UTC), and the coordinator is asked for his word on a later time box.")
TASK_CHECK = ("Build the new deck standard check v1_1_0 (monospace code boxes, story slides without label words) with fixtures of known answer",
              "URGENT repair, on the Owner's ruling of 2026-10-30 about 03:40 Istanbul. Build a NEW file `08-tooling/sen0414_deck_standard_check_v1_1_0.py` that measures the same elements as `08-tooling/sen0414_deck_standard_check_v1_0_0.py` (D1 to D12 and M1; read its docstring and code first; v1_0_0 stays as committed and unchanged) but detects the things the Owner no longer allows to be marked by '>>>' and by label words: "
              "(a) a CODE BOX is a text shape whose runs are all in a monospace font (Courier New, Consolas or any font whose name contains 'mono'), and a shape whose whole text is '>>>' in the top 12 per cent of the slide is the deck's brand mark and is not a code box; "
              "(b) D2 (no text box over 30 words) is applied to boxes that are not code boxes; code boxes are measured by D12 (no code line wraps: every line fits the box width at the font size) and D3 (explanation beside the code, and an executed result shown as a visual: define from the deck's own construction how the result visual is recognised, for example a picture, chart or table placed with the code box, and write the rule in the docstring); "
              "(c) M1 compares the manifest `03-materials/ch08/page/chapter_code_ch08_v1_1_0.json` with the code boxes in slide order, text and order; "
              "(d) a STORY SLIDE is recognised without label words: define the rule from how the deck marks its story slides (read `08-tooling/ch08-deck/` and the slides) and write it in the docstring BEFORE the first run; D5 then requires of each story slide a real picture (a picture shape), a live link (a hyperlink on the slide) and the six facts of the story (who, what, when, where, why, how) told as sentences, without labels: decide how a check can see them (named person, a year or date, a place, a reason word, a means) and say what it cannot see. "
              "Deliver also `08-tooling/sen0414_deck_standard_check_fixtures_v1_1_0.py` (builds small decks with python-pptx) and a `--selftest` that prints expected and actual for every fixture and exits 0 only when all are as expected: for each element at least one deck built to pass and one built to fail (a 66-word code box must PASS D2 and a 66-word text box must FAIL it; a monospace code box with a wrapped line must FAIL D12; a story slide without picture must FAIL D5; a manifest with a swapped pair must FAIL M1; a deck without a code box must report NOT_MEASURED for D3, D12 and M1). "
              "Run the new check on `03-materials/ch08/SEN0414_Ch08_Strings_3e_v2_1_0.pptx` and on the Chapter 7 deck (newest in `03-materials/ch07/`) and print both outputs verbatim. Report a failing element as failing with the slide numbers; do NOT edit the deck, the manifest or any committed file to make an element pass. If the Chapter 8 deck fails an element for a real reason, say what repair it needs and stop. "
              "Do not use the old check's wording to excuse anything: NOT_MEASURED and CANNOT_RUN are not passes. HARD STOP: report within 90 minutes of your start; a half result with its failures named is worth more than silence.")
TASK_CHECK_V = ("Verify the new deck standard check on the controller's own re-runs", "Control by the lineage agent on its own re-runs: the selftest exits 0 with every fixture as expected, the check on the Chapter 8 deck v2.1.0 prints every element, the lineage agent adds one fixture of its own for each element that the executor's fixtures did not cover, nothing committed was edited; an incomplete run is a result, not a pass.")


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def start(t, tid, at, L, note):
    i, j = blk(t, tid); b = t[i:j]
    assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b, tid
    t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % at, 1) + t[j:]
    L.append('ex:Begin8T_%s a backlog:TransitionEvent ; rdfs:label "%s started"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (tid, tid, tid, at, lit(note)))
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (tid, lit("Work begun %s UTC. Lineage agent's control (no executor, no brief)." % at)))
    return t


def main():
    assert sys.argv[1:2] == ["repair"], __doc__
    src = W.newest(); t = open(src, encoding="utf-8").read(); n = W.now(); L = []
    assert "ex:TK_U8_Deck_Check a" not in t, "already done"
    t = start(t, "TK_U8_Deck_Verify", START_DECK_VERIFY, L, "Control work begun by the lineage agent at %s UTC with its first kept log (the controller's own check of the deck, its selftest); no executor, no brief. The record is written at %s UTC, after the real start, which the logs witness." % (START_DECK_VERIFY, n))
    t = start(t, "TK_U8_Page_Verify", START_PAGE_VERIFY, L, "Control work begun by the lineage agent at %s UTC with the chapter check Page/Ch08 on the page v9_92_1 (page test 9.37.0); no executor, no brief. The record is written at %s UTC, after the real start, which the log witnesses." % (START_PAGE_VERIFY, n))
    L.append("ex:Mission2 backlog:hasAuditNote %s .\n" % lit(RULING))
    L.append("ex:ST_U8_Deck backlog:hasAuditNote %s .\n" % lit(FINDINGS_DECK))
    L.append("ex:TK_U8_Deck_Verify backlog:hasAuditNote %s .\n" % lit(FINDINGS_DECK))
    L.append("ex:ST_U8_Page backlog:hasAuditNote %s .\n" % lit(FINDINGS_PAGE))
    L.append("ex:TK_U8_Page_Verify backlog:hasAuditNote %s .\n" % lit(FINDINGS_PAGE))
    L.append("ex:AC2U_Deck_Ch08 backlog:hasAuditNote %s .\n" % lit(CRIT_NOTE))
    L.append("ex:Iter_U8 backlog:hasAuditNote %s .\n" % lit(TIMEBOX))
    L.append("ex:Urgent_1 backlog:hasAuditNote %s .\nex:Urgent_2 backlog:hasAuditNote %s .\n" % (lit(TIMEBOX), lit(TIMEBOX)))
    # the repair task and its control
    lab, note = TASK_CHECK; lv, notev = TASK_CHECK_V
    for tid, label, typ, cat, deps, text_ in (("TK_U8_Deck_Check", lab, "Build", "Cat_Compliance", [], note + " Estimated 1.5 hours (an estimate, G120)."),
                                              ("TK_U8_Deck_Check_Verify", lv, "Verify", "Cat_Compliance", ["TK_U8_Deck_Check"], notev + " Estimated 0.5 hours (an estimate, G120).")):
        L.append('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_U8 ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
                 '    backlog:hasInvestmentCategory backlog:%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n%s'
                 '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n' % (
                     tid, lit(label), tid, lit(label), cat, typ, ("    backlog:dependsOn %s ;\n" % ", ".join("ex:" + d for d in deps)) if deps else "", lit(text_)))
        L.append('ex:Refine8b_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_U8 ;\n'
                 '    backlog:hasRefinementOutcome "Refined by the lineage agent from the controller\'s findings on the deck v2.1.0 and the Owner\'s ruling of 2026-10-30 about 03:40 Istanbul: requirements in the task text, the control that follows, an estimate; the brief is generated from the register." .\n' % (tid, tid, tid, n))
    L.append("ex:ST_U8_Deck backlog:decomposesInto ex:TK_U8_Deck_Check, ex:TK_U8_Deck_Check_Verify .\nex:Iter_U8 backlog:hasMember ex:TK_U8_Deck_Check, ex:TK_U8_Deck_Check_Verify .\n"
             )
    for u in ("Urgent_1", "Urgent_2"):
        L.append("ex:%s backlog:urgentItem ex:TK_U8_Deck_Check, ex:TK_U8_Deck_Check_Verify .\n" % u)
    L.append('ex:Plan8b_ST_U8_Deck a backlog:PlanningEvent ; rdfs:label "Planning of the deck check repair into the urgent box"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_U8 ;\n    backlog:plansItem ex:ST_U8_Deck ; backlog:producesTask ex:TK_U8_Deck_Check, ex:TK_U8_Deck_Check_Verify ;\n    backlog:refinementProduces ex:Spec2S_D, ex:Scen2S_D_Passes, ex:Scen2S_D_NotClaimed .\n' % n)
    # the re-ranking that the repair causes
    L.append('ex:Score2_ST_U8_Deck a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
        (20 + 20 + 13) / 3.8, n, lit("WSJF = (business value 20 + time criticality 20 + risk reduction 13) / job size 3.8 h = %.2f. Re-score after the controller's findings (the repair task of the new deck check, 1.5 h, and its control, 0.5 h, join the original 1.8 h): the deck cannot be Done until the check exists and reports, so risk reduction rises from 5 to 13 (without the check the deck's standard cannot be measured at all). Scored %s UTC." % ((20 + 20 + 13) / 3.8, n))))
    t = t.replace("backlog:hasPriorityScore ex:Score1_ST_U8_Deck", "backlog:hasPriorityScore ex:Score2_ST_U8_Deck", 1)
    L.append("ex:Lineage2 backlog:hasAuditNote %s .\n" % lit("RANKING after the controller's findings (%s UTC): the repair re-ranks the open urgent items. 1 the new deck standard check (TK_U8_Deck_Check; it blocks the deck), 2 the controller's page runs of page test 9.37.0 on v9_92_1 (five direct runs) with the leak probe and the render of the 72 slides, 3 the controller's check of the new deck check, 4 the held control of the page v9_91_0 (fifth run of 9.37.0 and the Playground width probe; the page used in class is v9_92_1). The held items of the interrupted lineages stay held until the urgent items are Done." % n))
    out = W.write_new(src, t + "\n" + "".join(L), "Urgent Chapter 8 box after the controller's first findings: the controller's real starts, the findings as printed (deck: own checks and teaching check PASS, the old standard check FAIL in D2 and M1 and NOT_MEASURED in D3, D5, D12 because it cannot see monospace code boxes; page: chapter check FAIL on the load-dependent main-thread budget, 406 passed, 2 failed), the Owner's ruling on new check files, the repair task TK_U8_Deck_Check with its control, the re-ranking, and the missed time box said openly.")
    print(os.path.basename(out))


if __name__ == "__main__":
    main()
