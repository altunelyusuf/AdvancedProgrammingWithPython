#!/usr/bin/env python3
"""sen0414_lineage_resfix06c v1_0_0 - change route (rulings G104, G125, G136): the criterion AC2R_ResearchCh06 (which this register wrote, ex:CR2_ResFix06B) names Cross.B among the gate checks that must pass on the new page ABox. The controller measured (and the executor reported) that Cross.B prints CANNOT_RUN ('hybrid chains: 0 checked, 0 broken') for the chapter 6 research set, and the gates end 'OVERALL: PASS' with it;
the check cannot be satisfied by this task because the research and page ABoxes of the course hold no hybrid chains for it to check. The criterion is restated (Cross.B must not FAIL; CANNOT_RUN is reported openly and is not counted as a pass), and the gap is tracked as a planned story of Iter_19 (ex:ST_Plan_Gap_CrossB), not waived silently.
The planned retrofit criterion AC2F_Retrofit is restated on the page test 9.37.0 in the same version (it still names 9.36.0, which the owner's chapters no longer use).
Events, one new register file each:  change | retract | backlog PREV | fill PREV.   Usage: sen0414_lineage_resfix06c_v1_0_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S; lit = W.lit; now = W.now
CR = "ex:CR2_ResFix06C"; IA = "ex:IA2_ResFix06C"; REV = "ex:Revision_Lineage2_Backlog8"
OLD = "ex:Out2_BacklogR7"; NEW = "ex:Out2_BacklogR8"
ST = "ST_Std_ResearchCh06"; TK = "TK_Std_ResearchCh06"; TKV = "TK_Std_ResearchCh06_Verify"; AC = "AC2R_ResearchCh06"
DIRECTION = ("Direction of the course coordinator, 2026-10-25, recorded as relayed: the research repair of chapter 6 is not met by its own account on one point, Cross.B prints CANNOT_RUN while the criterion text says Cross.B passing; decide by the discipline without waiting for the owner: if the criterion text cannot be met by this task and the check has never run for any chapter, record it as a pre-existing gap of the gates, tracked as a work item that the lineage enforces but the work cannot satisfy, and restate the criterion by the change route with disclosure, not silently waived. The owner's standing rule that work the lineage enforces but the actual work misses must be dealt with also holds.")
FACTS = ("MEASURED FACTS (executor logs 08-tooling/ch06-research/logs_iter18/gates_ch06_partA_run1.log, gates_ch06_partA_run2.log, gates_ch06_partB_run1.log, chapter_check_Research_Ch06_run1.log, and the controller's own run of the chapter check Research/Ch06 on 2026-10-25): the gates end 'OVERALL: PASS' and print '[CANNOT_RUN ] Cross.B: hybrid chains: 0 checked, 0 broken'; "
         "Stage4.A, B, cov, sub and src PASS on the new page ABox v1_4_0. Cross.B is evaluated only inside Stage 4, that is only for a chapter that has a page ABox; no chapter had one passing it before (chapters 7 to 9 have none, chapter 6's v1_3_0 failed Stage 4 on other checks), so the check has never produced a measured result in this course. "
         "It reports CANNOT_RUN because no hybrid chain (a chain that crosses the research document, the domain ontology and the page ABox) exists in any chapter's files for it to check; building such chains is work on the research design of the course, outside the repair of the findings of ex:CR2_ResFix06 and ex:CR2_ResFix06B. "
         "The criterion text this register wrote ('Cross.B passing') is therefore unsatisfiable by the task as it stands; the executor did not fake it and reported it openly.")
GH = ("Owner-directed repair (ex:CR2_ResFix06 widened by ex:CR2_ResFix06B, restated by ex:CR2_ResFix06C). Given the chapter 6 research set (data module v2_0_0, page ABox v1_3_0: gates Stage4.cov 11 hollow typed individuals, Stage4.sub 152 individuals not substantive; execution checks: 2 mismatches), "
      "when (A) a NEW data module 08-tooling/sen0414_ch06_rdodi_data_v2_1_0.py is written from v2_0_0 with TAX and BODY taken from the chapter corpus sen0414_ch06_corpus_v1_0_0.py as chapter 7 v1_3_0 did, and the chapter 6 files are rebuilt from it by the generic builder (sen0414_rdodi_build_v1_2_0.py) as 03-materials/ch06/rdodi/sen0414_ch06_{document,domain_tbox,domain_abox,domain_shacl,research}_v2_1_0.*, "
      "and (B) a NEW page-ABox builder version 08-tooling/sen0414_page_abox_build_v1_1_9.py (older versions stay) builds a NEW page ABox 03-materials/ch06/page/sen0414_ch06_page_abox_v1_4_0.ttl that describes the NEW page 03-materials/ch06/page/sen0414_ch06_page_v9_90_0.html (its menus, tabs, panels, widgets and the chapter-code examples as they are in that page), "
      "then ALL of: (1) every new file is new and every committed file (the v2_0_0 and v1_0_0 research files, page ABox v1_3_0, the page, the deck, the manifest, the older builders) is byte-identical; "
      "(2) every typed individual of the new research ABox and of the new page ABox has a label, a skos:definition and a dcterms:source where the gates ask for them, and content of at least five words that is substantive by the gate, written from the book's chapter 6, the deck, the page and the existing content, with nothing invented; no individual, class, link or source of the old files is dropped without a stated reason; "
      "(3) the chapter check Research/Ch06 (python3 08-tooling/sen0414_lineage_chapter_check_v1_1_0.py Research/Ch06) ends exit 0 with 'RESULT Research/Ch06: PASS': the gates 'OVERALL: PASS' with Stage4.A, B, cov, sub and src passing on the NEW page ABox, HermiT consistent, the execution checks with 0 mismatches; "
      "Cross.B must not FAIL; it reports CANNOT_RUN (0 hybrid chains) and is reported openly as such and NOT counted as a pass (the gap is tracked by the planned story ex:ST_Plan_Gap_CrossB); "
      "(4) the chapter 6 deck, page and chapter-code manifest are not changed (the page file keeps its SHA-256), and Page/Ch06 under the chapter check still ends PASS; "
      "(5) Research/Ch07, Research/Ch08 and Research/Ch09 still end PASS; no committed file is edited; results as printed, measured by the controller by its own re-runs.")
GAP_AC = ("PLANNED, NOT STARTED (ex:CR2_ResFix06C). Given the chapter research, domain ontology and page ABox of a chapter, when hybrid chains (chains that cross the research document, the domain ontology and the page ABox) are modelled in the chapter's new ABox files as new files, "
          "then the gate Cross.B (sen0414_rdodi_gates_v1_1_1.py, gate_provenance) checks a number of chains above zero and finds none broken, and prints PASS instead of CANNOT_RUN; the controller re-runs the chapter check; no committed file is edited.")
GAP_NOTE = (DIRECTION + " " + FACTS + " PLANNED, NOT STARTED: no task is made, no score is given and no work begins until the story is planned into an iteration and released; it is planned after the chapters 7, 8 and 9 and the retrofit order of ex:CR2_Priority3, because it needs a decision on what a hybrid chain of this course is.")


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Restate the criterion of the chapter 6 research repair: Cross.B cannot run (no hybrid chains exist), so it must not fail but is not a pass; track the gap as a planned story"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(DIRECTION + " The scope does not move outward: one planned story is added to the unstarted Iter_19 and two criteria are restated."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What restating the Cross.B element changes, with the facts measured before it is planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACTS + " WHAT MOVES: the Backlog stage is revised once more; element (3) of ex:AC2R_ResearchCh06 is restated (Cross.B must not FAIL; CANNOT_RUN is reported and not counted as a pass); the planned retrofit criterion ex:AC2F_Retrofit names the page test 9.37.0 instead of 9.36.0; one planned story ex:ST_Plan_Gap_CrossB with its criterion enters the unstarted Iter_19, Proposed and unscored; "
                    "the open stories are re-scored with unchanged inputs. The research repair keeps its tasks and its start; it is controlled after this revision against the restated criterion. Not in the plan: a waiver, an edit of a gate, building hybrid chains now."))
    return t + cr + ia, "ChangeRequest ex:CR2_ResFix06C (Pending) and ImpactAssessment ex:IA2_ResFix06C: Cross.B of the chapter 6 research criterion cannot run (no hybrid chains in any chapter); restate the criterion, track the gap; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (DIRECTION + " A criterion is restated, a second criterion is restated and a planned story enters the closed Backlog stage, which moves its digest (G117, G125 route 2): a StageRevision from the Backlog stage, never from the Mission; the change request ex:CR2_ResFix06C and the impact assessment ex:IA2_ResFix06C were recorded first. "
              "This version retracts the Backlog output ex:Out2_BacklogR7 and rebuilds nothing; the next version closes the Backlog stage again as ex:Out2_BacklogR8 and re-admits every item without re-dating any; a third version fills the commit. The retracted output and its digest stay as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: the Cross.B element of the chapter 6 research criterion restated and the gap tracked"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) restating the Cross.B element: the Backlog output Out2_BacklogR7 is retracted; nothing is rebuilt in this version."


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now()
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR7\b", t)); assert cnt >= 80, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR7\b", "admittedByOutput " + NEW, t)
    L = []
    for sid in ("ST_Std_Page_Ch06", "ST_Std_Page_Ch09", "ST_Std_PageTest37", "ST_Std_ResearchCh06"):
        i, j = blk(t, sid); b = t[i:j]; m = re.search(r"backlog:hasPriorityScore ex:(Score\d+_%s)\b" % sid, b); assert m, sid
        r0 = t[blk(t, m.group(1))[0]:blk(t, m.group(1))[1]]
        q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0); assert q, sid
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:Score13_%s" % sid, 1) + t[j:]
        bv, tc, rr, size = int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4)); val = (bv + tc + rr) / size
        L.append('ex:Score13_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Re-run on %s UTC because the Backlog output moved (ex:CR2_ResFix06C); inputs unchanged. The earlier record is kept as history." % (bv, tc, rr, size, val, n))))
    # restate AC2R_ResearchCh06 element (3)
    i, j = blk(t, AC); b = t[i:j]
    old = "with Stage4.A, B, cov, sub, src and Cross.B passing on the NEW page ABox"
    assert old in b or "Stage4.A, B, cov, sub and src passing" in b
    new_gh = GH
    b2 = re.sub(r'backlog:hasGherkinText "[^\n]*?" ;\n', lambda m: "backlog:hasGherkinText %s ;\n" % lit(new_gh), b, count=1)
    assert b2 != b
    t = t[:i] + b2 + t[j:]
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (AC, lit("RESTATED %s UTC (ex:CR2_ResFix06C, StageRevision %s): element (3) no longer says Cross.B passing: Cross.B must not FAIL and its CANNOT_RUN (0 hybrid chains) is reported openly and is not counted as a pass; the gap is tracked by the planned story ex:ST_Plan_Gap_CrossB. Every other element is as before. %s" % (n, REV.split(":")[1], FACTS))))
    # restate AC2F_Retrofit on 9.37.0
    i, j = blk(t, "AC2F_Retrofit"); b = t[i:j]
    nb = b.replace("page test 9.36.0", "page test 9.37.0").replace("ex:TS2_PageTest36", "ex:TS2_PageTest37"); assert nb != b
    t = t[:i] + nb + t[j:]
    L.append('ex:AC2F_Retrofit backlog:hasAuditNote %s .\n' % lit("RESTATED %s UTC (ex:CR2_ResFix06C): the planned retrofit criterion names the page test 9.37.0 where it named 9.36.0 (text and tool), as the criteria of the chapter 6 and 9 pages do since ex:CR2_Retest37. Still PLANNED, NOT STARTED." % n))
    # the planned gap story
    L.append('\nex:AC2F_CrossB a backlog:AcceptanceCriterion ; rdfs:label "The gate Cross.B measures hybrid chains of a chapter: above zero checked, none broken"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS2_RdodiGates, ex:TS2_ChapterCheck ;\n    backlog:measuredWithVersion "RDODI gates v1_1_1; chapter check v1_1_0; the versions then current when the story is planned into an iteration" ;\n    backlog:satisfiedByArtifact "the new files cited by SHA-256, the controller\'s own runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC2R6C_CrossB, ex:TC2R6C_CrossBNot .\n' % lit(GAP_AC))
    L.append("""
ex:TC2R6C_CrossB a backlog:TestCase ; rdfs:label "Run the chapter check and read Cross.B: chains checked above zero, none broken"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:AC2F_CrossB ; backlog:coversScenario ex:Scen2S_P_Passes ; backlog:runsOnData ex:Data2R6C_CrossB ;
    backlog:hasCaseText "Cross.B prints PASS with a number of chains above zero and none broken for the chapter's research and page ABox files." .
ex:TC2R6C_CrossBNot a backlog:TestCase ; rdfs:label "A chapter whose Cross.B still prints CANNOT_RUN is not claimed as met"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:AC2F_CrossB ; backlog:coversScenario ex:Scen2S_P_NotClaimed ; backlog:runsOnData ex:Data2R6C_CrossB ;
    backlog:hasCaseText "CANNOT_RUN is reported as CANNOT_RUN and is never counted as a pass." .
ex:Data2R6C_CrossB a backlog:TestData ; rdfs:label "The chapter research, domain ontology and page ABox files of a chapter"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The files of the chapter as they are when the story is planned." .
""")
    L.append(('\nex:ST_Plan_Gap_CrossB a backlog:Story ; rdfs:label "Make the gate Cross.B measurable: model the hybrid chains of a chapter (planned)"@en ; backlog:hasIdentifier "ST_Plan_Gap_CrossB" ;\n    backlog:hasTitle "Make the gate Cross.B measurable: model the hybrid chains of a chapter (planned)" ;\n'
              '    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_19 ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput %s ;\n    backlog:hasInvestmentCategory backlog:Cat_Maintenance ;\n'
              '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "the research gates to measure the hybrid chains of a chapter instead of reporting CANNOT_RUN" ; backlog:soThat "no gate element of a chapter\'s research set stays unmeasured" ;\n'
              '    backlog:satisfiesDeliverable ex:Del2_StdPages ; backlog:pursuesObjective ex:Obj2_StdPages ; backlog:hasAcceptanceCriterion ex:AC2F_CrossB ;\n'
              '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n    backlog:hasState backlog:Proposed ;\n'
              '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned." ;\n    backlog:hasAuditNote %s .\n') % (NEW, lit(GAP_NOTE)))
    L.append("ex:Obj2_StdPages backlog:metricMovableBy ex:ST_Plan_Gap_CrossB .\n")
    L.append('ex:SC2_ResFix06C a backlog:ScopeChange ;\n    rdfs:label "A planned story for the Cross.B gap admitted into the unstarted Iter_19"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:ST_Plan_Gap_CrossB ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, lit(DIRECTION + " The boundary does not move outward in deliverables; the planned story is Proposed and unscored.")))
    t, k = re.subn(r'(ex:CR2_ResFix06C a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR2_ResFix06C rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_ResFix06C; it was Pending before. The coordinator\'s direction is the direction; the owner is not waited for."@en .\n' % n[:10])
    t += "\n" + "".join(L)
    out = ('\nex:Out2_BacklogR8 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt for the restated Cross.B element and the tracked gate gap"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % S.digest(t, "Backlog")
    return t + out, "second lineage, Backlog stage rebuilt: element (3) of the chapter 6 research criterion restated (Cross.B must not fail, CANNOT_RUN is not a pass), the planned retrofit criterion restated on 9.37.0, the gate gap tracked as a planned story of Iter_19, open stories re-scored, ScopeChange, change request Accepted, every item re-admitted."


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR8 set to the commit that closed it (%s); the revision is complete and no work is begun in this version." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
