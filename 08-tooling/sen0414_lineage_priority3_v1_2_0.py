#!/usr/bin/env python3
"""sen0414_lineage_priority3 v1_2_0 - change route (rulings G104, G125, G136) for the OWNER DECISION of 2026-10-23 16:06 Istanbul, relayed by the course coordinator and recorded as a priority input:
chapters 7, 8 and 9 are urgent for next week and chapter 6 drops behind them; after them all chapters are retrofitted to the standard in order, starting with chapter 1, and after that the remaining chapters are built.
Events, one new register file each (the caller validates and commits and pushes each alone):  change | retract | backlog PREV | fill PREV
  change   - ChangeRequest ex:CR2_Priority3 (Pending) and ImpactAssessment ex:IA2_Priority3 with the measured facts (what exists for chapter 9) and the estimates.
  retract  - StageRevision from the Backlog stage: retracts ex:Out2_BacklogR3; status LS_Objectived.
  backlog  - Backlog output ex:Out2_BacklogR4: every item re-admitted; chapter 9 deck and page stories, tasks and criteria added to Iter_18 (cloned from chapter 8's, states reset); every open story re-scored with WSJF as dated records
             (chapters 7, 8, 9 time criticality 20, chapter 6 page 8, the repairs still first); the follow-on retrofit and build work PLANNED, not started (one planned story per chapter, with estimates); the exclusion lifted for chapter 9; ScopeChange; CR Accepted.
  fill     - closedAtCommit of ex:Out2_BacklogR4.
v1.1.0 (over 1.0.0, which produced 2.165.0 and 2.166.0): the planned stories sit in a container of the second lineage, ex:Backlog2 (v1.0.0 put them in the first lineage's backlog, which the validator refused as an open item of a wound-down lineage), and name the executor on the hook.
v1.2.0 (over 1.1.0, whose container ex:Backlog2 the validator took for a register root and refused): MODE=none leaves the planned stories without a container; MODE=iter puts them in a planned, unstarted iteration ex:Iter_19.
Usage: sen0414_lineage_priority3_v1_2_0.py EVENT [PREV_COMMIT]"""
__version__ = "1.2.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S; lit = W.lit; now = W.now
CR = "ex:CR2_Priority3"; IA = "ex:IA2_Priority3"; REV = "ex:Revision_Lineage2_Backlog4"
OLD = "ex:Out2_BacklogR3"; NEW = "ex:Out2_BacklogR4"
WHEN = "Friday 2026-10-23 16:06 Istanbul (13:06 UTC)"
OWNER = ("OWNER DECISION of %s, relayed by the course coordinator and recorded as relayed (content, not a verbatim quotation), a priority input: SEN0414 chapters 7, 8 and 9 are urgent for next week; chapter 6 drops behind them. "
         "After they are finished, return to ALL chapters starting with chapter 1 (retrofit to the standard: deck, chapter-code manifest, page), and after that build all remaining chapters. "
         "The coordinator's direction: add chapter 9 (deck, manifest, page) to Iter_18; check what exists for chapter 9; re-rank dated (chapters 7, 8, 9 deck and page ahead of the chapter 6 page, the repairs still first); plan the follow-on as planned work with estimates, not started now. "
         "The owner's standing rule that repairs re-rank the open items also holds." % WHEN)
FACTS = ("MEASURED FACTS (the lineage agent, 2026-10-23, from the repository). CHAPTER 9 (Regular Expressions): research exists (03-materials/ch09/rdodi: document v1_0_0 and v1_0_1, domain TBox, ABox and SHACL, research v1_0_0); an old deck exists only as 08-tooling/ch09-deck/sen0414_ch09_deck_v1_0_0.pptx with its generator, examples and checks (03-materials/ch09 holds no deck); "
         "the old page exists as 03-materials/ch09/page/sen0414_ch09_page_v9_28_0.html (and 9_17_0, 9_18_0, 9_19_0): no chapter-code tab, no panel level, no declared standard, the character-set declaration at byte 9293; no chapter-code manifest exists. "
         "So chapter 9 needs a new deck (as a new file in 03-materials/ch09), its chapter-code manifest, then a new page, exactly as chapters 6, 7 and 8. "
         "OTHER CHAPTERS: chapters 1 to 5 and 10 to 24 have research, an old deck and an old page of the same kind (chapter 25, threads, has research, one deck file and one page file); none has a chapter-code manifest. "
         "ESTIMATES (the register's own, from the controlled chapters 6 to 8 of this iteration: a deck rebuild about 5.0 h of one executor session, a page rebuild about 4.0 h, the controller's control about 1.0 h per chapter): a retrofit of one chapter is about 10.0 h of work, "
         "about 9.0 h of it by executors; the 21 chapters 1 to 5 and 10 to 25 are about 210 h in all, about 70 h of wall time with three executor sessions in parallel (a deck session, a page session, a second chapter's deck session; the 2-core machine and the controller's control are the limit). "
         "Chapters still lacking research, deck or page after the retrofits are built from scratch at about 12.0 h each (research 3.0 h, deck 5.0 h, page 4.0 h); their list is measured when the retrofits finish.")
RANKING = ("Ranking after the owner decision (WSJF, inputs from observable facts): the repairs still rank first (a repair outranks the work it blocks); then the chapter 7, 8 and 9 pages (time criticality 20: next week), the chapter 9 deck first because the chapter 9 page depends on it; "
           "the chapter 6 page drops to time criticality 8. The deck of chapter 9 is a prerequisite and starts at once, in parallel with the repairs, although its own score is below the pages' (a dependency orders starts before a score does).")
OPEN = {  # sid: (bv, tc, rr, size, why)
    "ST_Std_TemplateFix": (8, 20, 20, 1.5, "the repair of the template; unchanged"),
    "ST_Std_Runner":      (5, 13, 13, 1.0, "the repair of the runner; unchanged"),
    "ST_Std_Charset":     (8, 20, 20, 1.0, "unchanged"),
    "ST_Std_DeckTools":   (13, 20, 8, 1.5, "unchanged"),
    "ST_Std_PageTools":   (13, 20, 13, 9.0, "unchanged"),
    "ST_Std_Deck_Ch06":   (20, 8, 3, 5.5, "chapter 6 drops behind chapters 7, 8 and 9 by the owner decision: time criticality 8"),
    "ST_Std_Page_Ch06":   (20, 8, 3, 4.0, "chapter 6 drops behind chapters 7, 8 and 9 by the owner decision: time criticality 8"),
    "ST_Std_Deck_Ch07":   (20, 20, 3, 5.5, "chapter 7 is urgent for next week by the owner decision: time criticality 20"),
    "ST_Std_Page_Ch07":   (20, 20, 3, 4.0, "chapter 7 is urgent for next week by the owner decision: time criticality 20; the first page to build"),
    "ST_Std_Deck_Ch08":   (20, 20, 3, 5.5, "chapter 8 is urgent for next week by the owner decision: time criticality 20"),
    "ST_Std_Page_Ch08":   (20, 20, 3, 4.0, "chapter 8 is urgent for next week by the owner decision: time criticality 20; the second page"),
    "ST_Std_Deck_Ch09":   (20, 20, 13, 5.5, "chapter 9 is urgent for next week by the owner decision: time criticality 20; risk reduction 13 because the chapter 9 page depends on this deck"),
    "ST_Std_Page_Ch09":   (20, 20, 3, 4.0, "chapter 9 is urgent for next week by the owner decision: time criticality 20; the third page, after its deck"),
}
CHAPS = ["%02d" % i for i in list(range(1, 6)) + list(range(10, 26))]


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Owner priority decision: chapters 7, 8 and 9 first for next week, chapter 6 behind them; then all chapters retrofitted from chapter 1, then the remaining chapters built"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope2 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(OWNER + " The scope grows by chapter 9 (deck, manifest, page), which the exclusion ex:Excl2_NoRebuild still holds out, and by planned, not started, work for the other chapters. Pending until the ScopeChange that records it."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the owner priority decision changes: chapter 9 enters Iter_18, the open stories are re-ranked, the follow-on is planned"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage2 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACTS + " " + RANKING + " WHAT MOVES: the Backlog stage is revised once more (stories, criteria and tasks added; the digest moves); tasks already Done stay Done and are not re-dated; the two repair tasks already begun are not touched; "
                    "the page builds keep their dependencies on the repairs' verification; the follow-on stories are planned and unscored (scored when their iteration is planned), start nothing, and are admitted only as planned work. Not in the plan: any edit of a committed file."))
    return t + cr + ia, "ChangeRequest ex:CR2_Priority3 (Pending) and ImpactAssessment ex:IA2_Priority3 for the owner decision of 2026-10-23 16:06 Istanbul (chapters 7, 8, 9 urgent, chapter 6 behind; then retrofit all chapters from chapter 1, then build the remaining): what exists for chapter 9, the estimates; no stage changed."


def ev_retract(t):
    t = S.set_status(t, "LS_Objectived")
    reason = (OWNER + " Stories, criteria and tasks are added to the closed Backlog stage, which moves its digest (G117, G125 route 2): a StageRevision from the Backlog stage; the change request ex:CR2_Priority3 and the impact assessment ex:IA2_Priority3 were recorded first. "
              "This version retracts the Backlog output ex:Out2_BacklogR3 and rebuilds nothing; the next version closes the Backlog stage again as ex:Out2_BacklogR4 and re-admits every item without re-dating it; a third version fills the commit. The retracted output stays as history (L-112).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the second lineage from the Backlog stage: the owner priority decision of 2026-10-23 16:06 Istanbul"@en ;\n'
         '    backlog:revisesLineage ex:Lineage2 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n'
         '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    return t + b, "StageRevision of the second lineage from the Backlog stage (G125 route 2) for the owner priority decision of 2026-10-23 16:06 Istanbul: the Backlog output Out2_BacklogR3 is retracted; nothing is rebuilt in this version."


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def sub9(s):
    for a, b in (("Strings and Text Editing", "Regular Expressions"), ("Ch08", "Ch09"), ("ch08", "ch09"), ("chapter 8", "chapter 9"), ("Chapter 8", "Chapter 9")):
        s = s.replace(a, b)
    return s


def clone9(t, name8, n):
    i, j = blk(t, name8); b = sub9(t[i:j])
    b = re.sub(r'backlog:hasState backlog:Done ; backlog:startedAt "[^"]*"\^\^xsd:dateTime ; backlog:finishedAt "[^"]*"\^\^xsd:dateTime ; backlog:hasEvidence [^;]*;', 'backlog:hasState backlog:%s ;' % ("Ready" if "TaskType_Build" in b else "Proposed"), b, count=1)
    b = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt "[^"]*"\^\^xsd:dateTime', "backlog:hasState backlog:Ready", b, count=1)
    b = b.replace("backlog:hasPriorityScore ex:Score3R_ST_Std_Deck_Ch09", "backlog:hasPriorityScore ex:Score4_ST_Std_Deck_Ch09").replace("backlog:hasPriorityScore ex:Score3R_ST_Std_Page_Ch09", "backlog:hasPriorityScore ex:Score4_ST_Std_Page_Ch09")
    return b


def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision ;.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = S.set_status(t, "LS_Backlogged"); n = now()
    cnt = len(re.findall(r"admittedByOutput ex:Out2_BacklogR3\b", t)); assert cnt >= 40, cnt
    t = re.sub(r"admittedByOutput ex:Out2_BacklogR3\b", "admittedByOutput " + NEW, t)
    L = []
    # chapter 9, cloned from chapter 8 (the clone is taken before any score link is changed)
    names8 = ["ST_Std_Deck_Ch08", "ST_Std_Page_Ch08", "TK_Std_Deck_Ch08_Build", "TK_Std_Deck_Ch08_Verify", "TK_Std_Page_Ch08_Build", "TK_Std_Page_Ch08_Verify", "AC2S_Deck_Ch08", "AC2S_Page_Ch08"]
    cl = {x: clone9(t, x, n) for x in names8}
    note9 = lambda kind: lit(OWNER + " " + FACTS + " This story is the chapter 9 %s." % kind)
    for x, b in cl.items():
        if x.startswith("ST_"):
            b = re.sub(r'backlog:hasAuditNote ".*?" \.\s*$', lambda m: "backlog:hasAuditNote " + note9("deck" if "Deck" in x else "page") + " .\n", b, flags=re.S)
        L.append("\n" + b.rstrip("\n") + "\n")
    # dependencies of the chapter 9 page build: the repairs and the regression check as for the other pages
    L.append("ex:TK_Std_Page_Ch09_Build backlog:dependsOn ex:TK_Std_TemplateFix_Verify, ex:TK_Std_Runner_Verify, ex:TK_Std_Regress, ex:TK_Std_Charset_Verify .\n")
    L.append('ex:TK_Std_Page_Ch09_Build backlog:hasAuditNote %s .\n' % lit("REPAIR (ex:CR2_Repair2): build the page on the repaired template course_page_template_v9_52_2.html with the page builder sen0414_page_build_v4_18_1.py (and the page-data builder v2_25_0), not on 9.52.1, and run the page tests through the runner sen0414_page_test_run_v1_1_0.py, which runs 9.36.0. Released only after the template repair and the runner repair are controlled and the regression check is Done."))
    L.append('ex:TK_Std_Deck_Ch09_Build backlog:hasAuditNote %s .\n' % lit("Chapter 9 facts for this task: the old deck is 08-tooling/ch09-deck/sen0414_ch09_deck_v1_0_0.pptx (with its generator, examples and checks in that folder); the research is 03-materials/ch09/rdodi (document v1_0_1, domain ABox and TBox, research v1_0_0); the old page is 03-materials/ch09/page/sen0414_ch09_page_v9_28_0.html. The new deck is a new file in 03-materials/ch09; use the chapter's stories (08-tooling/sen0414_ch09_stories_v1_0_0.py) and diagrams where they exist."))
    # ranking: relink the existing open stories' scores
    for sid, (bv, tc, rr, size, why) in OPEN.items():
        if sid in ("ST_Std_Deck_Ch09", "ST_Std_Page_Ch09"):
            continue
        i, j = blk(t, sid); b = t[i:j]
        m = re.search(r"backlog:hasPriorityScore ex:(Score3R_%s)\b" % sid, b); assert m, sid
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:Score4_%s" % sid, 1) + t[j:]
    for sid, (bv, tc, rr, size, why) in OPEN.items():
        val = (bv + tc + rr) / size
        L.append('ex:Score4_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. Re-scored on %s UTC after the owner decision of %s (ex:CR2_Priority3). %s Inputs from observable facts: job size is the sum of the story's task estimates in this register; time criticality 20 = next week's class or work that blocks it, 13 = blocks later work, 8 = later in the order. %s. The earlier record is kept as history." % (
                bv, tc, rr, size, val, n, WHEN, RANKING, why))))
    # chapter 9 refinement and planning
    for x in ("ST_Std_Deck_Ch09", "ST_Std_Page_Ch09", "TK_Std_Deck_Ch09_Build", "TK_Std_Deck_Ch09_Verify", "TK_Std_Page_Ch09_Build", "TK_Std_Page_Ch09_Verify"):
        L.append('ex:Refine4_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_18 ;\n    backlog:hasRefinementOutcome %s .\n' % (
            x, x, x, n, lit("Refined by the lineage agent from the owner decision of %s (ex:CR2_Priority3) and the measured facts of ex:IA2_Priority3: criterion with tools and versions, dependencies, a brief to be generated from the register; startable when its dependencies are Done." % WHEN)))
    for sid, tks in (("ST_Std_Deck_Ch09", ("TK_Std_Deck_Ch09_Build", "TK_Std_Deck_Ch09_Verify")), ("ST_Std_Page_Ch09", ("TK_Std_Page_Ch09_Build", "TK_Std_Page_Ch09_Verify"))):
        L.append('ex:Plan4_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 18"@en ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_18 ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec2S_P, ex:Scen2S_P_Passes, ex:Scen2S_P_NotClaimed .\n' % (sid, sid, n, sid, ", ".join("ex:" + x for x in tks)))
    L.append("ex:Obj2_StdDecks backlog:metricMovableBy ex:ST_Std_Deck_Ch09 .\nex:Obj2_StdPages backlog:metricMovableBy ex:ST_Std_Page_Ch09 .\n")
    L.append("ex:Iter_18 backlog:hasMember ex:ST_Std_Deck_Ch09, ex:ST_Std_Page_Ch09, ex:TK_Std_Deck_Ch09_Build, ex:TK_Std_Deck_Ch09_Verify, ex:TK_Std_Page_Ch09_Build, ex:TK_Std_Page_Ch09_Verify .\n")
    # the follow-on: planned, not started
    MODE = os.environ.get('MODE', 'none')
    if MODE == 'iter':
        L.append('\nex:Iter_19 a backlog:Iteration ; rdfs:label "Iteration 19 (planned, not started): the retrofit of chapters 1 to 5 and 10 to 25 to the standard, and the build of the remaining chapters"@en ; backlog:hasIdentifier "Iter_19" ; backlog:belongsToLineage ex:Lineage2 ;\n    backlog:hasDurationSource "PLANNED, NOT STARTED: no start, end or sprint goal is set; the iteration is planned with its own ceremony when the owner releases it after chapters 7, 8 and 9 (ex:CR2_Priority3)." .\n')
    L.append('\nex:AC2F_Retrofit a backlog:AcceptanceCriterion ; rdfs:label "A retrofitted chapter has a deck that meets the deck standard, its chapter-code manifest and a page that meets the page standard"@en ; backlog:belongsToLineage ex:Lineage2 ;\n'
             '    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS2_DeckStdCheck, ex:TS2_DeckOverlap, ex:TS2_PageTest36 ;\n    backlog:measuredWithVersion "deck standard check v1_0_0; deck overlap check v1_0_0; page test 9.36.0 through runner v1_1_0; template 9.52.2; builder 4.18.1; the versions then current when the chapter is planned into an iteration" ;\n'
             '    backlog:satisfiedByArtifact "the new files cited by SHA-256, the controller\'s own runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC2S_D_Passes, ex:TC2S_D_NotClaimed .\n' % lit(
                 "PLANNED, NOT STARTED (ex:CR2_Priority3). Given the old deck and old page of the chapter and its research, when the deck is rebuilt as a new file (deck standard check and overlap check pass, every element D1 to D12), the chapter-code manifest written from the deck, and the page rebuilt as a new file on the repaired template (page test 9.36.0 passes, the chapter-code tab equal to the manifest), then the chapter is retrofitted; the controller re-runs every check; no committed file is edited."))
    for c in CHAPS:
        sid = "ST_Plan_Retrofit_Ch%s" % c
        est = "Estimate: deck rebuild 5.0 h, page rebuild 4.0 h (executor sessions), control 1.0 h (controller): 10.0 h; order: chapters 1 to 5, then 10 to 25, each after the chapters 7, 8 and 9 are finished. PLANNED, NOT STARTED: no task is made, no score is given and no work begins until the chapter is planned into an iteration and released."
        L.append('\nex:%(s)s a backlog:Story ; rdfs:label "Retrofit chapter %(n)d to the standard: deck, chapter-code manifest and page (planned)"@en ; backlog:hasIdentifier "%(s)s" ;\n    backlog:hasTitle "Retrofit chapter %(n)d to the standard (planned)" ;\n'
                 '    backlog:belongsToLineage ex:Lineage2 ; @@CONT@@backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput %(o)s ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
                 '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "chapter %(n)d taught from a deck and a page that meet the written standard, with the slide code runnable in the page" ; backlog:soThat "every chapter of the course is taught from decks and pages that meet the same written standard" ;\n'
                 '    backlog:satisfiesDeliverable ex:Del2_StdDecks, ex:Del2_StdPages ; backlog:pursuesObjective ex:Obj2_StdDecks, ex:Obj2_StdPages ; backlog:hasAcceptanceCriterion ex:AC2F_Retrofit ;\n'
                 '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n    backlog:hasState backlog:Proposed ;\n'
                 '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned." ;\n    backlog:hasAuditNote %(note)s .\n' % dict(s=sid, n=int(c), o=NEW, note=lit(OWNER + " " + est)))
    L.append('\nex:ST_Plan_Remaining a backlog:Story ; rdfs:label "Build all remaining chapters to the standard (planned)"@en ; backlog:hasIdentifier "ST_Plan_Remaining" ;\n    backlog:hasTitle "Build all remaining chapters to the standard (planned)" ;\n'
             '    backlog:belongsToLineage ex:Lineage2 ; @@CONT@@backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput %s ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
             '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "every remaining chapter of the course built as research, deck, chapter-code manifest and page that meet the written standard" ; backlog:soThat "no chapter of the course is left outside the standard" ;\n'
             '    backlog:satisfiesDeliverable ex:Del2_StdDecks, ex:Del2_StdPages ; backlog:pursuesObjective ex:Obj2_StdDecks, ex:Obj2_StdPages ; backlog:hasAcceptanceCriterion ex:AC2F_Retrofit ;\n'
             '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n    backlog:hasState backlog:Proposed ;\n'
             '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned." ;\n    backlog:hasAuditNote %s .\n' % (NEW, lit(
                 OWNER + " Estimate: about 12.0 h per chapter built from scratch (research 3.0 h, deck 5.0 h, page 4.0 h) plus 1.0 h of control; the list of chapters still lacking research, deck or page is measured when the retrofits finish. PLANNED, NOT STARTED.")))
    L.append("ex:Obj2_StdDecks backlog:metricMovableBy %s .\nex:Obj2_StdPages backlog:metricMovableBy %s .\n" % (", ".join("ex:ST_Plan_Retrofit_Ch%s" % c for c in CHAPS + []) + ", ex:ST_Plan_Remaining", ", ".join("ex:ST_Plan_Retrofit_Ch%s" % c for c in CHAPS) + ", ex:ST_Plan_Remaining"))
    L.append('ex:Excl2_NoRebuild rdfs:comment %s .\n' % lit("Lifted on %s for chapter 9, ONLY for the NEW files of its deck, chapter-code manifest and page (ex:CR2_Priority3, the owner decision): no existing deck, research run or page of chapter 9 is changed. The follow-on retrofit and build stories are PLANNED, NOT STARTED: this note lifts nothing for them; each is lifted by its own record when the chapter is planned into an iteration." % WHEN))
    L.append('ex:SC2_Priority3 a backlog:ScopeChange ;\n    rdfs:label "Chapter 9 admitted into the iteration, and the follow-on retrofit and build work admitted as planned work"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope2 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:ST_Std_Deck_Ch09, ex:ST_Std_Page_Ch09, %s, ex:ST_Plan_Remaining ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        CR, ", ".join("ex:ST_Plan_Retrofit_Ch%s" % c for c in CHAPS), lit(OWNER + " Chapter 9 is admitted for work now; the others are admitted as planned, unscored, unstarted work.")))
    t, k = re.subn(r'(ex:CR2_Priority3 a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR2_Priority3 rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC2_Priority3; it was Pending before. The owner decision is the direction."@en .\n' % n[:10])
    t += "\n" + "".join(L).replace("@@CONT@@", "backlog:memberOfContainer ex:Iter_19 ; " if MODE == "iter" else "")
    out = ('\nex:Out2_BacklogR4 a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the second lineage, rebuilt by the stage revision for the owner priority decision of 2026-10-23 16:06"@en ;\n    backlog:belongsToLineage ex:Lineage2 ;\n'
           '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out2_ObjectiveR1 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % S.digest(t, "Backlog")
    return t + out, "second lineage, Backlog stage rebuilt for the owner priority decision of 2026-10-23 16:06: chapter 9 deck and page added to Iter_18, every open story re-scored (chapters 7, 8, 9 ahead of the chapter 6 page, repairs first), the retrofit of chapters 1 to 5 and 10 to 25 and the build of the remaining chapters planned (not started, with estimates), ScopeChange, change request Accepted."


def ev_fill(t, prev):
    t = W.fill_re(t, NEW, prev)
    return t, "closedAtCommit of the rebuilt Backlog output Out2_BacklogR4 set to the commit that closed it (%s); the revision is complete and no work is begun in this version." % prev


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); arg = sys.argv[2] if len(sys.argv) > 2 else None
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, arg), "fill": lambda: ev_fill(t, arg)}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
