#!/usr/bin/env python3
"""sen0414_lineage_resfix06 v1_0_0 - change route (rulings G104, G125, G136) for a finding of the controller on the first chapter 6 page run (measured 2026-10-24): the chapter check Research/Ch06, which the criterion of the chapter 6 page names in its element (4),
fails on the chapter 6 research v2_0_0 (gates Stage4.cov and Stage4.sub, 2 mismatches of the execution checks). The gap predates iteration 18 and is not caused by the page; it is repaired in its own story, ranked before the verify task of the chapter 6 page.
Events, one new register file each (the caller validates and commits and pushes each alone):  change | retract | backlog PREV | fill PREV
  change   - ChangeRequest ex:CR2_ResFix06 (Pending) and ImpactAssessment ex:IA2_ResFix06 with the measured facts.
  retract  - StageRevision from the Backlog stage: retracts ex:Out2_BacklogR5; status LS_Objectived.
  backlog  - Backlog output ex:Out2_BacklogR6; every admitted item re-admitted; the story ST_Std_ResearchCh06 with its criterion, executor task and controller task; the verify task of the chapter 6 page depends on the controller task; the exclusion lifted for the NEW research files of chapter 6 only; the open stories re-scored; ScopeChange; the change request Accepted.
  fill     - closedAtCommit of ex:Out2_BacklogR6.
Usage: sen0414_lineage_resfix06_v1_0_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S; lit = W.lit; now = W.now
CR = "ex:CR2_ResFix06"; IA = "ex:IA2_ResFix06"; REV = "ex:Revision_Lineage2_Backlog6"
OLD = "ex:Out2_BacklogR5"; NEW = "ex:Out2_BacklogR6"
ST = "ST_Std_ResearchCh06"; TK = "TK_Std_ResearchCh06"; TKV = "TK_Std_ResearchCh06_Verify"; AC = "AC2R_ResearchCh06"
DIRECTION = ("Direction of the course coordinator, 2026-10-24, recorded as relayed: the executor of the chapter 6 page reports that the chapter check Research/Ch06 fails on the research v2_0_0 and asks whether this belongs to the page criterion or is a separate gap; "
             "proceed at once with the research repair by the change route, a new research data version with its own story ranked before the verify task of the chapter 6 page. The owner's standing rule that work the lineage enforces but the actual work misses must be dealt with, and that gaps are said openly, also holds.")
FACTS = ("MEASURED FACTS (the executor of the chapter 6 page, log 08-tooling/ch06-page/logs_iter18/chapter_check_Research_Ch06_run1.log, commit ae0ba44; the lineage agent read the log and the files on 2026-10-24): "
         "the chapter check Research/Ch06 ends 'RESULT Research/Ch06: FAIL' on the chapter 6 research v2_0_0 (08-tooling/sen0414_ch06_rdodi_data_v2_0_0.py, committed 98c1609, 2026-09). The gates (sen0414_rdodi_gates_v1_1_1.py) end 'OVERALL: FAIL (2)': "
         "Stage4.cov 'hollow instantiation: 11 typed individuals lack label+content' and Stage4.sub '152 individuals not substantive (e.g. s_MembershipOperators: 2 words (<5))'; HermiT is consistent. "
         "The execution checks (sen0414_rdodi_checks_v1_2_0.py on sen0414_ch06_rdodi_data_v2_0_0) end with 77 checks and 2 mismatches: the class list of the TBox and the individual list of the ABox of the data module differ from the ones the checks expect. "
         "The chapter checks of chapters 7 and 8 pass. The failure is therefore not caused by the page work: it is a gap of the chapter 6 research that existed before iteration 18 (the chapter check covered chapters 7 to 12 only until its version 1_1_0 of this iteration reached chapter 6); "
         "it belongs to the criterion element (4) of the page criterion ('the chapter checks that exist for the chapter pass'), which is why the chapter 6 page cannot be Done on it, and it is repaired in its own story, not waived.")
GH = ("Owner-directed repair (ex:CR2_ResFix06). Given the chapter 6 research v2_0_0 (gates: Stage4.cov 11 hollow typed individuals, Stage4.sub 152 individuals not substantive; execution checks: 2 mismatches), "
      "when a NEW data module 08-tooling/sen0414_ch06_rdodi_data_v2_1_0.py is written from v2_0_0 and the chapter 6 files are rebuilt from it by the generic builder (newest sen0414_rdodi_build_v1_2_0.py) as 03-materials/ch06/rdodi/sen0414_ch06_{document,domain_tbox,domain_abox,domain_shacl,research}_v2_1_0.* , then ALL of: "
      "(1) the new files are new and every v2_0_0 and v1_0_0 file of chapter 6 is byte-identical; "
      "(2) every typed individual of the chapter 6 ABox has a label and a content text, and every individual's content is substantive by the gate (at least five words), written from the book's chapter 6 and the existing content, with nothing invented; no individual, class, link or source is dropped; "
      "(3) the chapter check Research/Ch06 (python3 08-tooling/sen0414_lineage_chapter_check_v1_1_0.py Research/Ch06) ends exit 0 with 'RESULT Research/Ch06: PASS', the gates 'OVERALL: PASS', HermiT consistent and the execution checks with 0 mismatches; "
      "(4) the chapter 6 deck and the chapter 6 page (concepts, names, example numbers) are not changed by the repair: the chapter-code manifest and the deck code boxes are untouched, and a diff of the concept names of v2_0_0 and v2_1_0 is given; "
      "(5) the chapter checks Research/Ch07, Research/Ch08 and Research/Ch09 still end PASS (the gates are unchanged); no committed file is edited; results as printed, measured by the controller by its own re-runs.")
NOTE_T = ("Write the NEW data module 08-tooling/sen0414_ch06_rdodi_data_v2_1_0.py from sen0414_ch06_rdodi_data_v2_0_0.py (read it, its builder 08-tooling/sen0414_rdodi_build_v1_2_0.py, the gates sen0414_rdodi_gates_v1_1_1.py and the checks sen0414_rdodi_checks_v1_2_0.py first; the way chapters 7 (v1_3_0) and 8 (v1_0_2) pass them is the guide). "
          "Run the chapter check first and read both gate findings and the 2 mismatches of the execution checks: find the root cause of each (the 11 typed individuals without label and content, the 152 individuals whose content has fewer than five words, the TBox class list and ABox individual list the checks expect) and fix them in the data, not in a gate or a check. "
          "Content comes from the book's chapter 6 and the existing concept texts; do not invent facts, sources or code. Build the files as v2_1_0 into 03-materials/ch06/rdodi with the generic builder, keep the v2_0_0 files byte-identical, and run: "
          "python3 08-tooling/sen0414_lineage_chapter_check_v1_1_0.py Research/Ch06 (must end PASS), and Research/Ch07, Research/Ch08, Research/Ch09 (must still end PASS), keeping every log in 08-tooling/ch06-research/logs_iter18/. "
          "Do not touch the chapter 6 deck, the page or its manifest. Machine: 2 cores shared; run the Java reasoner checks one at a time. Report the commit SHAs, the new files and the verbatim output of every check, and say what failed if anything.")
NOTE_V = ("Controller task (the lineage agent): require the v2_0_0 and v1_0_0 files of chapter 6 byte-identical; re-run the chapter checks Research/Ch06 (must PASS), Research/Ch07, Research/Ch08 and Research/Ch09 on the controller's own runs; diff the concept names of v2_0_0 and v2_1_0; "
          "check the deck code boxes and the chapter-code manifest of chapter 6 unchanged; run the evidence bridge and record the result, Done or NOT MET, no waiver.")


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The chapter check Research/Ch06 fails on the chapter 6 research v2_0_0: a repair story with a new research data version, ranked before the verify task of the chapter 6 page"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(DIRECTION + " The scope does not move outward in deliverables: the chapter 6 research is a file of the chapter the pages criterion already names (element 4); what is added is one repair story with a build task and a controller task."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the repair of the chapter 6 research changes in the iteration, with the facts measured before it is planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACTS + " WHAT MOVES: the Backlog stage of the second lineage is revised once more (a story, a criterion, test cases and two tasks are added; the exclusion on rebuilding is lifted for the NEW research files of chapter 6 only; the digest moves); "
                    "the tasks already Done stay Done and are not re-dated; the verify task of the chapter 6 page gains the dependency on the controller task of this repair, so the chapter 6 page cannot be Done before the research check passes; "
                    "the chapter 6 page build task is not blocked; the pages of chapters 7, 8 and 9 and the chapter 9 research are not affected; the open stories are re-scored. Not in the plan: any edit of a committed file, any change of a gate or check, any waiver."))
    return t + cr + ia, "ChangeRequest ex:CR2_ResFix06 (Pending) and ImpactAssessment ex:IA2_ResFix06: the chapter check Research/Ch06 fails on the chapter 6 research v2_0_0 (a gap that predates iteration 18); a repair story with a new research data version; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (DIRECTION + " A story, a criterion and tasks are added to the lineage's closed Backlog stage and one dependency and one exclusion note are added, which moves its digest (G117, G125 route 2): a StageRevision from the Backlog stage, never from the Mission; the change request ex:CR2_ResFix06 and the impact assessment ex:IA2_ResFix06 were recorded first. "
              "This version retracts the Backlog output ex:Out2_BacklogR5 and rebuilds nothing; the next version closes the Backlog stage again as ex:Out2_BacklogR6 and re-admits every item, the Done tasks included, without re-dating them; a third version fills the commit. The retracted output and its digest stay as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: the repair of the chapter 6 research"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) for the repair of the chapter 6 research: the Backlog output Out2_BacklogR5 is retracted; nothing is rebuilt in this version."


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now()
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR5\b", t)); assert cnt >= 80, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR5\b", "admittedByOutput " + NEW, t)
    L = []
    open_st = []
    for sid in ("ST_Std_Deck_Ch09", "ST_Std_Page_Ch06", "ST_Std_Page_Ch09", "ST_Std_PageTest37"):
        i, j = blk(t, sid); b = t[i:j]; m = re.search(r"backlog:hasPriorityScore ex:(Score\d+_%s)\b" % sid, b); assert m, sid
        r0 = t[blk(t, m.group(1))[0]:blk(t, m.group(1))[1]]
        q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0); assert q, sid
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:Score11_%s" % sid, 1) + t[j:]
        open_st.append((sid, int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4)), "Inputs unchanged; re-run because the Backlog output moved and a repair story entered the ranking"))
    open_st.append((ST, 13, 20, 8, 3.0, "the chapter 6 page cannot be Done while the research check of its chapter fails (element 4 of its criterion); it is a repair, so it is ranked before the verify task of the chapter 6 page and before the stories it blocks"))
    for sid, bv, tc, rr, size, why in open_st:
        val = (bv + tc + rr) / size
        L.append('ex:Score11_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Re-scored on %s UTC under the owner's rule that repairs re-rank the open work (ex:CR2_ResFix06): %s. The earlier record is kept as history." % (bv, tc, rr, size, val, n, why))))
    L.append("""
ex:TC2R6_Passes a backlog:TestCase ; rdfs:label "Run the chapter checks Research/Ch06, Ch07, Ch08 and Ch09; the controller re-runs them"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(a)s ; backlog:coversScenario ex:Scen2S_P_Passes ; backlog:runsOnData ex:Data2R6_Passing ;
    backlog:hasCaseText "python3 08-tooling/sen0414_lineage_chapter_check_v1_1_0.py Research/Ch06 ends exit 0 with PASS (gates OVERALL PASS, HermiT consistent, 0 mismatches); Research/Ch07, Research/Ch08, Research/Ch09 still PASS." .
ex:TC2R6_NotClaimed a backlog:TestCase ; rdfs:label "Run the chapter check on the committed v2_0_0 data and require it to fail"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(a)s ; backlog:coversScenario ex:Scen2S_P_NotClaimed ; backlog:runsOnData ex:Data2R6_Failing ;
    backlog:hasCaseText "The gates run on the committed v2_0_0 files (which stay byte-identical) still end FAIL with the two findings: the old files are history and are not made to pass." .
ex:Data2R6_Passing a backlog:TestData ; rdfs:label "The new v2_1_0 files of chapter 6 and the data module"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The committed v2_1_0 files in 03-materials/ch06/rdodi and sen0414_ch06_rdodi_data_v2_1_0.py." .
ex:Data2R6_Failing a backlog:TestData ; rdfs:label "The committed v2_0_0 files of chapter 6"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The v2_0_0 files, unchanged." .
""" % dict(a=AC))
    L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS2_ChapterCheck, ex:TS2_RdodiGates ;\n    backlog:measuredWithVersion %s ;\n'
             '    backlog:satisfiedByArtifact "the new data module and the v2_1_0 files cited by SHA-256, the logs of the controller\'s own runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC2R6_Passes, ex:TC2R6_NotClaimed .\n' % (
                 AC, lit("The chapter 6 research passes the chapter check Research/Ch06 on a new data version, and the chapter checks of the other chapters still pass"), lit(GH),
                 lit(W.VER + "; chapter check 1.1.0, RDODI gates 1.1.1, RDODI checks 1.2.0, generic builder 1.2.0 (Python 3.14, HermiT)")))
    L.append(('\nex:%(s)s a backlog:Story ; rdfs:label %(t)s@en ; backlog:hasIdentifier "%(s)s" ;\n    backlog:hasTitle %(t)s ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_18 ; backlog:admittedByOutput %(n)s ;\n    backlog:hasInvestmentCategory backlog:Cat_Maintenance ;\n'
              '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability %(w)s ; backlog:soThat "the chapter 6 page can be controlled against every check that exists for its chapter" ;\n'
              '    backlog:satisfiesDeliverable ex:Del2_StdPages ; backlog:pursuesObjective ex:Obj2_StdPages ; backlog:hasAcceptanceCriterion ex:%(ac)s ;\n'
              '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n    backlog:decomposesInto ex:%(tk)s, ex:%(tv)s ;\n    backlog:hasState backlog:Ready ;\n'
              '    backlog:hasPriorityScore ex:Score11_%(s)s ; backlog:standsAlone true ;\n    backlog:hasAuditNote %(note)s .\n') % dict(
                  s=ST, t=lit("Repair: the chapter 6 research passes the chapter check on a new data version"), n=NEW,
                  w=lit("a chapter 6 research whose individuals all have a label and a substantive content text, passing the gates and the execution checks"), ac=AC, tk=TK, tv=TKV, note=lit(DIRECTION + " " + FACTS)))
    for tid, title, ttype, deps, sess, est, hrs, note in (
            (TK, "Repair the chapter 6 research as a new data version v2_1_0: labels and content for every individual, gates and execution checks pass", "Build", [], "SEN0414-I18-research-ch06", "T0", 3.0, NOTE_T),
            (TKV, "Control the chapter 6 research: the chapter checks Research/Ch06 to Ch09 on the controller's own runs", "Verify", [TK], "the lineage agent", "after the research repair", 0.5, NOTE_V)):
        L.append(W.task_block(tid, title, ttype, deps, sess, est, hrs, note).replace(W.NEWB, NEW))
    c = "06"
    vi, vj = blk(t, "TK_Std_Page_Ch06_Verify"); vb = t[vi:vj]
    m = re.search(r"backlog:dependsOn ([^;]*);", vb); assert m
    t = t[:vi] + vb.replace(m.group(0), "backlog:dependsOn %s, ex:%s ;" % (m.group(1).strip(), TKV), 1) + t[vj:]
    L.append('ex:TK_Std_Page_Ch06_Build backlog:hasAuditNote %s .\n' % lit("Re-planned %s UTC (ex:CR2_ResFix06): the failing chapter check Research/Ch06 is not caused by your page; it is repaired by the task ex:%s. This task is not blocked; the verify task of the page waits for the research check to pass." % (n, TK)))
    for x in (ST, TK, TKV):
        L.append('ex:Refine6_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_18 ;\n    backlog:hasRefinementOutcome %s .\n'
                 % (x, x, x, n, lit("Refined by the lineage agent from the executor's log of the chapter check (ex:CR2_ResFix06, ex:IA2_ResFix06): criterion with tools and versions, dependencies, the measured findings, and a brief to be generated from the register.")))
    L.append('ex:Plan6_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 18"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_18 ;\n    backlog:plansItem ex:%s ; backlog:producesTask ex:%s, ex:%s ;\n    backlog:refinementProduces ex:Spec2S_P, ex:Scen2S_P_Passes, ex:Scen2S_P_NotClaimed .\n' % (ST, ST, n, ST, TK, TKV))
    L.append("ex:Obj2_StdPages backlog:metricMovableBy ex:%s .\n" % ST)
    L.append("ex:Iter_18 backlog:hasMember ex:%s, ex:%s, ex:%s .\n" % (ST, TK, TKV))
    L.append('ex:Excl2_NoRebuild rdfs:comment "Lifted on %s UTC for chapter 6 research, ONLY for the NEW files of the research repair (data module v2_1_0 and the v2_1_0 ontology and document files of chapter 6; ex:CR2_ResFix06): no existing research, deck or page file of chapter 6 is changed. Nothing else is lifted by this note."@en .\n' % n)
    L.append('ex:SC2_ResFix06 a backlog:ScopeChange ;\n    rdfs:label "One research repair story and its tasks admitted into the scope"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, ST, lit(DIRECTION + " The boundary does not move outward in deliverables; the repair story is admitted as the owner's standing rule requires.")))
    t, k = re.subn(r'(ex:CR2_ResFix06 a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR2_ResFix06 rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_ResFix06; it was Pending before. The coordinator\'s direction is the direction; the owner is not waited for."@en .\n' % n[:10])
    t += "\n" + "".join(L)
    out = ('\nex:Out2_BacklogR6 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt by the stage revision for the repair of the chapter 6 research"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % S.digest(t, "Backlog")
    return t + out, "second lineage, Backlog stage rebuilt for the repair of the chapter 6 research: one repair story with criterion, executor task and controller task; the verify task of the chapter 6 page depends on the controller task; the exclusion lifted for the new research files of chapter 6 only; the open stories re-scored; ScopeChange; change request Accepted; every item re-admitted."


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR6 set to the commit that closed it (%s); the revision is complete and no work is begun in this version." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
