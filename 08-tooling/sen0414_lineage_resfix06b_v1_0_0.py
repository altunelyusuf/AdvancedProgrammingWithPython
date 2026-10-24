#!/usr/bin/env python3
"""sen0414_lineage_resfix06b v1_0_0 - change route (rulings G104, G125, G136) widening the repair of the chapter 6 research (ex:CR2_ResFix06): the executor of TK_Std_ResearchCh06 stopped without changes by its brief's stop condition and found that the gate findings Stage4.cov and Stage4.sub are measured on
the chapter 6 PAGE ABox (03-materials/ch06/page/sen0414_ch06_page_abox_v1_3_0.ttl), which a research v2_1_0 cannot move; the 2 mismatches of the execution checks come from the old data module. The criterion of the story is restated (the repair also yields a NEW page ABox and a new page-ABox builder version), the task keeps its start and gets a
second executor session, the verify task is restated, the open stories are re-scored.
Events, one new register file each:  change | retract | backlog PREV | fill PREV
Usage: sen0414_lineage_resfix06b_v1_0_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S; lit = W.lit; now = W.now
CR = "ex:CR2_ResFix06B"; IA = "ex:IA2_ResFix06B"; REV = "ex:Revision_Lineage2_Backlog7"
OLD = "ex:Out2_BacklogR6"; NEW = "ex:Out2_BacklogR7"
ST = "ST_Std_ResearchCh06"; TK = "TK_Std_ResearchCh06"; TKV = "TK_Std_ResearchCh06_Verify"; AC = "AC2R_ResearchCh06"
DIRECTION = ("Direction of the course coordinator, 2026-10-24, recorded as relayed: the executor SEN0414-I18-research-ch06 stopped without changes by the brief's stop condition and found the fact that settles the choice; do not wait for the owner; widen the repair by the change route (option A): the task also produces a NEW page ABox version for chapter 6 built by a new page-ABox builder version, besides the research v2_1_0 data module and files; check that the new page ABox describes the NEW page, and whether chapter 9 has the same exposure. The owner's standing rule that work the lineage enforces but the actual work misses is dealt with, that a lineage never waits on unrelated questions, and that gaps are said openly, also holds.")
FACTS = ("MEASURED FACTS (the executor's report; the lineage agent read the gates script and the files on 2026-10-24): the gates script 08-tooling/sen0414_rdodi_gates_v1_1_1.py runs its Stage 4 on the newest 03-materials/chNN/page/sen0414_chNN_page_abox_v*.ttl when one exists (line 20), and skips Stage 4 when none exists. "
         "Chapter 6 has such a page ABox (sen0414_ch06_page_abox_v1_3_0.ttl, committed 0097aae, 2026-09-30, built by sen0414_page_abox_build_v1_1_7/8); chapters 7, 8 and 9 have none, which is why their Research checks pass. "
         "The findings of the executor's run: Stage4.cov 'hollow instantiation: 11 typed individuals lack label+content' = CO1-CO5, Layout, Header, Sidebar, Main, GroupedTopBar, SectionTree (a label but no skos:definition or dcterms:source); Stage4.sub '152 individuals not substantive' = page individuals s_* (58), w_* (57), wv_* (24) and structural ones, each with fewer than five words of content. "
         "A research v2_1_0 cannot move these gates. The 2 execution-check mismatches (17 classes missing from the TBox, 11 individuals missing from the ABox) come from the old data module sen0414_ch06_rdodi_data_v2_0_0.py (it carries the old v1_0_0 TAX/BODY); chapter 7 v1_3_0 fixed the same kind of drift by taking TAX/BODY from the chapter corpus (sen0414_ch06_corpus_v1_0_0.py). "
         "The page ABox of v1_3_0 describes the OLD page (v9_28_0 line); the page of chapter 6 is now v9_90_0 on template 9.52.2, so the NEW page ABox must describe the new page. Chapter 9: the page of chapter 9 v9_90_0 has no page ABox, Stage 4 is skipped and Research/Ch09 passes; it has the same exposure only if a page ABox is ever added for it, which is not planned. "
         "The finding is a gap of the chapter 6 research set (research files plus the page ABox) that predates iteration 18; it belongs to element (4) of the chapter 6 page criterion; it is repaired, not waived.")
GH = ("Owner-directed repair (ex:CR2_ResFix06 widened by ex:CR2_ResFix06B). Given the chapter 6 research set (data module v2_0_0, page ABox v1_3_0: gates Stage4.cov 11 hollow typed individuals, Stage4.sub 152 individuals not substantive; execution checks: 2 mismatches), "
      "when (A) a NEW data module 08-tooling/sen0414_ch06_rdodi_data_v2_1_0.py is written from v2_0_0 with TAX and BODY taken from the chapter corpus sen0414_ch06_corpus_v1_0_0.py as chapter 7 v1_3_0 did, and the chapter 6 files are rebuilt from it by the generic builder (sen0414_rdodi_build_v1_2_0.py) as 03-materials/ch06/rdodi/sen0414_ch06_{document,domain_tbox,domain_abox,domain_shacl,research}_v2_1_0.*, "
      "and (B) a NEW page-ABox builder version 08-tooling/sen0414_page_abox_build_v1_1_9.py (older versions stay) builds a NEW page ABox 03-materials/ch06/page/sen0414_ch06_page_abox_v1_4_0.ttl that describes the NEW page 03-materials/ch06/page/sen0414_ch06_page_v9_90_0.html (its menus, tabs, panels, widgets and the chapter-code examples as they are in that page), "
      "then ALL of: (1) every new file is new and every committed file (the v2_0_0 and v1_0_0 research files, page ABox v1_3_0, the page, the deck, the manifest, the older builders) is byte-identical; "
      "(2) every typed individual of the new research ABox and of the new page ABox has a label, a skos:definition and a dcterms:source where the gates ask for them, and content of at least five words that is substantive by the gate, written from the book's chapter 6, the deck, the page and the existing content, with nothing invented; no individual, class, link or source of the old files is dropped without a stated reason; "
      "(3) the chapter check Research/Ch06 (python3 08-tooling/sen0414_lineage_chapter_check_v1_1_0.py Research/Ch06) ends exit 0 with 'RESULT Research/Ch06: PASS': the gates 'OVERALL: PASS' with Stage4.A, B, cov, sub, src and Cross.B passing on the NEW page ABox, HermiT consistent, the execution checks with 0 mismatches; "
      "(4) the chapter 6 deck, page and chapter-code manifest are not changed (the page file keeps its SHA-256), and Page/Ch06 under the chapter check still ends PASS; "
      "(5) Research/Ch07, Research/Ch08 and Research/Ch09 still end PASS; no committed file is edited; results as printed, measured by the controller by its own re-runs.")
NOTE_T = ("SUPERSEDES the instructions above (ex:CR2_ResFix06B): the first session stopped without changes by its stop condition and found that the gate findings are measured on the chapter 6 PAGE ABox, which a research file cannot move. The task is widened (option A) and is done by a new session on the same task. "
          "Do BOTH: (A) the research v2_1_0 set: write the NEW data module 08-tooling/sen0414_ch06_rdodi_data_v2_1_0.py from v2_0_0 with TAX and BODY from the chapter corpus 08-tooling/sen0414_ch06_corpus_v1_0_0.py (the way chapter 7 v1_3_0 and chapter 8 v1_0_2 did) and build the five files v2_1_0 into 03-materials/ch06/rdodi with the generic builder 08-tooling/sen0414_rdodi_build_v1_2_0.py, so that the execution checks have 0 mismatches; "
          "(B) the page ABox: write the NEW builder 08-tooling/sen0414_page_abox_build_v1_1_9.py from v1_1_8 (read it first and say what you changed) and build the NEW 03-materials/ch06/page/sen0414_ch06_page_abox_v1_4_0.ttl so that it describes the NEW page sen0414_ch06_page_v9_90_0.html (read the page, its page data and the manifest); give the 11 hollow individuals (CO1-CO5, Layout, Header, Sidebar, Main, GroupedTopBar, SectionTree) a skos:definition and a dcterms:source, and every s_*, w_*, wv_* and structural individual a content text of at least five words, taken from the page's own text and the book, nothing invented. "
          "Find the root cause of each finding before editing; fix them in the data and the builder, never in a gate or a check. Verify with python3 08-tooling/sen0414_lineage_chapter_check_v1_1_0.py Research/Ch06 (must end PASS), and Research/Ch07, Research/Ch08, Research/Ch09, Page/Ch06 (must still end PASS), keeping every log in 08-tooling/ch06-research/logs_iter18/. "
          "Do not touch the deck, the page, its manifest or any committed file. Run the Java reasoner one run at a time (2 shared cores). Commit and push each verified step. Report the commit SHAs, the new files and the verbatim output of every check; say what failed if anything.")
NOTE_V = ("Controller task, restated (ex:CR2_ResFix06B): require every committed file byte-identical (v2_0_0 and v1_0_0 research files, page ABox v1_3_0, the page v9_90_0, the deck, the manifest, the older builders); re-run the chapter checks Research/Ch06 (must PASS with Stage 4 on the NEW page ABox), Research/Ch07, Research/Ch08, Research/Ch09 and Page/Ch06 on the controller's own runs; "
          "diff the concept names of v2_0_0 and v2_1_0; check that the new page ABox describes the new page (its tabs, panels, widgets and 25-example-class chapter code against the page and the manifest); run the evidence bridge and record the result, Done or NOT MET, no waiver.")


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Widen the repair of the chapter 6 research: the gate findings are measured on the page ABox of chapter 6, so the repair also yields a new page ABox and a new page-ABox builder version"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(DIRECTION + " The scope does not move outward in deliverables: the page ABox of chapter 6 is a file of the chapter the pages criterion already names (element 4)."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What widening the chapter 6 research repair changes, with the facts measured before it is planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACTS + " WHAT MOVES: the Backlog stage is revised once more; the criterion of ex:ST_Std_ResearchCh06 is restated (research v2_1_0 plus the new page ABox v1_4_0 and the new builder v1_1_9; the tools list gains the builder); the task ex:TK_Std_ResearchCh06 keeps its start of 2026-10-24T21:09:42 UTC (a T_Start cannot be repeated) and a second executor instance is recorded at the real start of the new session, with a new brief; "
                    "its job size grows from 3.0 to 6.0 h; the controller task is restated; the open stories are re-scored; the exclusion note is extended to the new page ABox of chapter 6 and its builder (new files only). The verify task of the chapter 6 page keeps its dependency. Not in the plan: any edit of a committed file, a change of a gate or check, a waiver, a change of chapter 9."))
    return t + cr + ia, "ChangeRequest ex:CR2_ResFix06B (Pending) and ImpactAssessment ex:IA2_ResFix06B: the gate findings of the chapter 6 research are measured on its page ABox; the repair is widened to a new page ABox and a new builder version; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (DIRECTION + " The criterion of a story, a task note and the test cases change, which moves the digest of the lineage's closed Backlog stage (G117, G125 route 2): a StageRevision from the Backlog stage, never from the Mission; the change request ex:CR2_ResFix06B and the impact assessment ex:IA2_ResFix06B were recorded first. "
              "This version retracts the Backlog output ex:Out2_BacklogR6 and rebuilds nothing; the next version closes the Backlog stage again as ex:Out2_BacklogR7 and re-admits every item, the Done tasks and the started task included, without re-dating them; a third version fills the commit. The retracted output and its digest stay as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: the repair of the chapter 6 research widened to its page ABox"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) widening the chapter 6 research repair: the Backlog output Out2_BacklogR6 is retracted; nothing is rebuilt in this version."


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now()
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR6\b", t)); assert cnt >= 80, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR6\b", "admittedByOutput " + NEW, t)
    L = []
    open_st = []
    for sid in ("ST_Std_Deck_Ch09", "ST_Std_Page_Ch06", "ST_Std_Page_Ch09", "ST_Std_PageTest37", "ST_Std_ResearchCh06"):
        i, j = blk(t, sid); b = t[i:j]; m = re.search(r"backlog:hasPriorityScore ex:(Score\d+_%s)\b" % sid, b); assert m, sid
        r0 = t[blk(t, m.group(1))[0]:blk(t, m.group(1))[1]]
        q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0); assert q, sid
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:Score12_%s" % sid, 1) + t[j:]
        if sid == "ST_Std_ResearchCh06":
            open_st.append((sid, 13, 25, 13, 6.0, "the job size doubled (the page ABox of chapter 6 is part of the repair) and the page it blocks is the class's; ranked before the verify task of the chapter 6 page"))
        else:
            open_st.append((sid, int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4)), "Inputs unchanged; re-run because the Backlog output moved and a repair story was widened"))
    for sid, bv, tc, rr, size, why in open_st:
        val = (bv + tc + rr) / size
        L.append('ex:Score12_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Re-scored on %s UTC under the owner's rule that repairs re-rank the open work (ex:CR2_ResFix06B): %s. The earlier record is kept as history." % (bv, tc, rr, size, val, n, why))))
    # restate the criterion: text, tools, versions, cases
    i, j = blk(t, AC); b = t[i:j]
    b2 = re.sub(r'backlog:hasGherkinText "[^\n]*?" ;\n', lambda m: "backlog:hasGherkinText %s ;\n" % lit(GH), b, count=1)
    assert b2 != b
    b2 = b2.replace("backlog:measuredWithTool ex:TS2_ChapterCheck, ex:TS2_RdodiGates ;", "backlog:measuredWithTool ex:TS2_ChapterCheck, ex:TS2_RdodiGates, ex:TS2_PageAboxBuild ;"); assert "TS2_PageAboxBuild" in b2
    b2 = re.sub(r'backlog:measuredWithVersion "[^\n]*?" ;\n', lambda m: "backlog:measuredWithVersion %s ;\n" % lit(W.VER + "; chapter check 1.1.0, RDODI gates 1.1.1, RDODI checks 1.2.0, generic builder 1.2.0, page-ABox builder 1.1.9 (new file over 1.1.8) (Python 3.14, HermiT)"), b2, count=1)
    b2 = b2.replace("backlog:coveredByCase ex:TC2R6_Passes, ex:TC2R6_NotClaimed .", "backlog:coveredByCase ex:TC2R6_Passes, ex:TC2R6_NotClaimed, ex:TC2R6B_PageAbox .")
    assert "TC2R6B_PageAbox" in b2
    t = t[:i] + b2 + t[j:]
    L.append('ex:TS2_PageAboxBuild a backlog:ToolScript ; rdfs:label "page-ABox builder v1_1_9 (new file over v1_1_8; builds the page ABox of the chapter from the new page)"@en ; backlog:scriptFileName "sen0414_page_abox_build_v1_1_9.py" ; backlog:acceptsGraphPath false .\n')
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (AC, lit("RESTATED %s UTC (ex:CR2_ResFix06B, StageRevision %s): the criterion now covers the research v2_1_0 set AND the new page ABox v1_4_0 built by the new builder v1_1_9, because the gate findings are measured on the page ABox. Every other element is as before." % (n, REV.split(":")[1]))))
    L.append("""
ex:TC2R6B_PageAbox a backlog:TestCase ; rdfs:label "Run the chapter check on the new page ABox and require every committed file byte-identical"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:exercisesCriterion ex:%(a)s ; backlog:coversScenario ex:Scen2S_P_Passes ; backlog:runsOnData ex:Data2R6B_PageAbox ;
    backlog:hasCaseText "Stage 4 of the gates (A, B, cov, sub, src, Cross.B) passes on sen0414_ch06_page_abox_v1_4_0.ttl; the page ABox v1_3_0, the page v9_90_0, the deck and the manifest keep their SHA-256; Page/Ch06 under the chapter check still ends PASS." .
ex:Data2R6B_PageAbox a backlog:TestData ; rdfs:label "The new page ABox of chapter 6 and its builder"@en ; backlog:belongsToLineage ex:Lineage2 ;
    backlog:hasFixtureState "The committed sen0414_ch06_page_abox_v1_4_0.ttl and sen0414_page_abox_build_v1_1_9.py, with the page and its manifest as they are." .
""" % dict(a=AC))
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (TK, lit("RESTATED %s UTC (ex:CR2_ResFix06B): " % n + NOTE_T)))
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (TKV, lit("RESTATED %s UTC (ex:CR2_ResFix06B): " % n + NOTE_V)))
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (ST, lit("RESTATED %s UTC (ex:CR2_ResFix06B): the story's job size is 6.0 h and its criterion covers the page ABox of chapter 6. The first executor session on the task stopped without changes by its stop condition and reported the cause; it is not a failure of the work. %s" % (n, FACTS))))
    for x in (ST, TK, TKV):
        L.append('ex:Refine7_%s a backlog:RefinementEvent ; rdfs:label "Re-refinement of %s after the executor\'s finding"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_18 ;\n    backlog:hasRefinementOutcome %s .\n'
                 % (x, x, x, n, lit("Re-refined by the lineage agent from the executor's report (ex:CR2_ResFix06B, ex:IA2_ResFix06B): the criterion and the task text now cover the page ABox; a new brief is generated from the register.")))
    L.append('ex:Excl2_NoRebuild rdfs:comment "Lifted on %s UTC (ex:CR2_ResFix06B), for chapter 6 only, ALSO for the NEW page ABox file sen0414_ch06_page_abox_v1_4_0.ttl and the NEW builder file sen0414_page_abox_build_v1_1_9.py: no existing page ABox, page, deck or research file of chapter 6 is changed. Nothing else is lifted by this note."@en .\n' % n)
    L.append('ex:SC2_ResFix06B a backlog:ScopeChange ;\n    rdfs:label "The chapter 6 research repair widened to the new page ABox"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, ST, lit(DIRECTION + " The boundary does not move outward in deliverables; the widened repair is admitted as the owner's standing rule requires.")))
    t, k = re.subn(r'(ex:CR2_ResFix06B a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR2_ResFix06B rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_ResFix06B; it was Pending before. The coordinator\'s direction is the direction; the owner is not waited for."@en .\n' % n[:10])
    t += "\n" + "".join(L)
    out = ('\nex:Out2_BacklogR7 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt for the widened repair of the chapter 6 research"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % S.digest(t, "Backlog")
    return t + out, "second lineage, Backlog stage rebuilt for the widened chapter 6 research repair: criterion and task restated (research v2_1_0 plus the new page ABox and builder), controller task restated, open stories re-scored, ScopeChange, change request Accepted, every item re-admitted."


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR7 set to the commit that closed it (%s); the revision is complete and no work is begun in this version." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
