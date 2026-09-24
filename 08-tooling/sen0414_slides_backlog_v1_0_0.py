"""Backlog stage of the SEN0414 slide lineage: admission only. Every item Proposed; no task yet -
tasks are produced by planning, and only for what is planned into an iteration."""
from sen0414_slides_stages_v1_0_0 import CHAPTERS, KIND, cid

# Planning of 2026-09-24, approved by the owner: chapters 1 and 2 in the first iteration, until
# SEN0414's class at 14:00 Istanbul (11:00 UTC) on 2026-09-25. WSJF components are
# (business value, time criticality, risk reduction, job size). Chapter 1's were proposed and
# approved; chapter 2 was added by the owner at approval and takes the same components, since it is
# taught in the same class.
PLANNED_AT = "2026-09-24T20:15:47"
WSJF = {"Research": (13, 20, 13, 3), "Page": (13, 20, 5, 3), "Deck": (20, 20, 8, 5)}
PLANNED = {1, 2}
REFINED = {
    "Research": "Settled: RDODI's four-stage procedure v1.6.0 on the chapter's subject, with its Pedagogy and Professional Standards stage and the Courseware profile; the research record lists every source a later claim rests on.",
    "Deck": "Settled: rewritten from the 3rd edition's chapter and the research record, restyled with PowerPoint's own capabilities, every code example run under current Python before it is shown, and the deck described as a teaching material aligned to the outcomes it serves.",
    "Page": "Settled: one interactive page for the chapter, carrying the research results; published as a page students can open, and described as a teaching material.",
}

OBJ = {"Deck": "Obj_DecksRenewed", "Research": "Obj_ResearchRecorded", "Page": "Obj_PagesBuilt"}


def planned_tail(k, n):
    if n not in PLANNED:
        return 'backlog:hasState backlog:Proposed ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned."'
    return ('backlog:hasState backlog:Ready ; backlog:memberOfContainer ex:Iter_1 ;\n    backlog:hasPriorityScore ex:Score_%s_%s ;\n'
            '    backlog:decomposesInto ex:TK_%s_%s_Build, ex:TK_%s_%s_Verify' % (k, cid(n), k, cid(n), k, cid(n)))


def planned_block(k, n):
    bv, tc, rr, js = WSJF[k]; c = cid(n)
    return '''
ex:Score_%(k)s_%(c)s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;
    backlog:hasScoreValue "%(v).2f"^^xsd:decimal ; backlog:scoredAt "%(t)s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;
    backlog:hasScoreRationale "WSJF = (business value %(bv)d + time criticality %(tc)d + risk reduction %(rr)d) / job size %(js)d, approved by the owner. Time criticality is set by the class at 14:00 Istanbul on 2026-09-25." .
ex:Plan_%(k)s_%(c)s a backlog:PlanningEvent ; rdfs:label "Planning of %(k)s for %(c)s into the first iteration"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:plannedAt "%(t)s"^^xsd:dateTime ; backlog:plannedBy backlog:Owner ; backlog:plannedInto ex:Iter_1 ;
    backlog:plansItem ex:ST_%(k)s_%(c)s ; backlog:producesTask ex:TK_%(k)s_%(c)s_Build, ex:TK_%(k)s_%(c)s_Verify .
ex:Refine_%(k)s_%(c)s a backlog:RefinementEvent ; rdfs:label "Refinement that made %(k)s for %(c)s ready"@en ;
    backlog:refines ex:ST_%(k)s_%(c)s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%(t)s"^^xsd:dateTime ;
    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:Iter_1 ; backlog:hasRefinementOutcome "%(o)s" .
ex:TK_%(k)s_%(c)s_Build a backlog:ExecutionTask ; rdfs:label "%(k)s for %(c)s: build"@en ; backlog:hasIdentifier "TK_%(k)s_%(c)s_Build" ; backlog:hasTitle "Build %(k)s %(c)s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:Proposed ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Build ; backlog:effectiveDefinitionOfDone ex:DoD ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story's score; scoring both would double-count." ;%(dep)s
    backlog:hasAuditNote "Build it." .
ex:TK_%(k)s_%(c)s_Verify a backlog:ExecutionTask ; rdfs:label "%(k)s for %(c)s: verify"@en ; backlog:hasIdentifier "TK_%(k)s_%(c)s_Verify" ; backlog:hasTitle "Verify %(k)s %(c)s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:Proposed ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Verify ; backlog:effectiveDefinitionOfDone ex:DoD ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story's score; scoring both would double-count." ;%(dep)s
    backlog:hasAuditNote "Run the chapter check and require the stale fixture refused." .
''' % dict(k=k, c=c, bv=bv, tc=tc, rr=rr, js=js, v=(bv + tc + rr) / js, t=PLANNED_AT, o=REFINED[k],
          dep=("" if k == "Research" else "\n    backlog:dependsOn ex:ST_Research_%s ;" % c))


ITER = '''
ex:Iter_1 a backlog:Iteration ; rdfs:label "First iteration: chapters 1 and 2, before the class of 25 September"@en ;
    backlog:hasIdentifier "Iter_1" ; backlog:belongsToLineage ex:Lineage ;
    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-09-25T11:00:00"^^xsd:dateTime ;
    backlog:hasDurationSource "Owner, 2026-09-24: chapter 1, and chapter 2 added at approval, ready for SEN0414's class at 14:00 Istanbul on 2026-09-25." ;
    backlog:hasSprintGoal "Chapters 1 and 2 researched, their decks renewed and their interactive pages built, ready to present." ;
    backlog:hasMember %s .
'''


def backlog_block():
    L = ['''
ex:Backlog a backlog:Backlog ; rdfs:label "Work admitted for renewing SEN0414's chapters"@en ;
    backlog:hasIdentifier "Backlog_SEN0414_Slides" ; backlog:belongsToLineage ex:Lineage ; backlog:isRegisterRoot true ;
    backlog:hasState backlog:Proposed ; backlog:producedByStage ex:Out_Backlog ;
    backlog:appliesDefinitionOfDone ex:DoD ; backlog:hasCommitment ex:Commit ; backlog:hasMember ex:Init_Slides .
ex:DoD a backlog:DefinitionOfDone ; rdfs:label "What finished means for a renewed chapter"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasDoDCriterion ex:DoD_CodeRuns, ex:DoD_Sourced, ex:DoD_TruthfulDates .
ex:DoD_CodeRuns a backlog:DoDCriterion ; rdfs:label "Every code example runs as the slide shows"@en ;
    backlog:hasCheckQuery "Extract every code example from the deck and run it under current Python." ;
    backlog:hasExpectedResult "Each prints what its slide shows; a stale example is named and refused." ; backlog:hasCriterionStatus backlog:NotYetEnforceable .
ex:DoD_Sourced a backlog:DoDCriterion ; rdfs:label "Every claim beyond the book has a recorded source"@en ;
    backlog:hasCheckQuery "Compare the deck's and page's claims against the chapter's RDODI research record." ;
    backlog:hasExpectedResult "No claim beyond the edition without a source in the research record." ; backlog:hasCriterionStatus backlog:NotYetEnforceable .
ex:DoD_TruthfulDates a backlog:DoDCriterion ; rdfs:label "Every recorded time is read, never composed"@en ;
    backlog:hasCheckQuery "Compare every start, finish, planning, refinement, scoring and observation time with the clock records and commits." ;
    backlog:hasExpectedResult "None post-dates the commit that carried it; none was written instead of read." ; backlog:hasCriterionStatus backlog:NotYetEnforceable .
ex:Commit a backlog:Commitment ; rdfs:label "This register commits to chapters that teach the book students read"@en ;
    backlog:commitsToGoal ex:G_DecksTeachTheBook ; backlog:commitsToObjective ex:Obj_DecksRenewed ; backlog:commitsToDefinitionOfDone ex:DoD .
ex:Session_Opening a backlog:RegisterSession ; rdfs:label "The session that built this register"@en ;
    backlog:sessionFor ex:Backlog ; backlog:sessionConductedBy "cme-session" ;
    backlog:sessionStartedAt "2026-09-24T19:13:00"^^xsd:dateTime ; backlog:sessionEndedAt "2026-09-24T19:16:12"^^xsd:dateTime ;
    backlog:stateVerifiedAtStart true ;
    backlog:hasSessionScopeNote "Built the slide lineage's stages after SEN0414 was registered, as the owner ordered: register SEN0414, then straight to its chapter 1 slides." ;
    backlog:changedItem ex:Init_Slides .
ex:Init_Slides a backlog:Initiative ; rdfs:label "Renew SEN0414's taught chapters"@en ; backlog:hasIdentifier "Init_Slides" ; backlog:hasTitle "Renew SEN0414's chapters" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:Proposed ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasInitiativeKind backlog:InitKind_Development ;
    backlog:producesIncrement "sen0414 2.6.0 onward - one published increment per renewed chapter" ;
    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:appliesDefinitionOfDone ex:DoD ; backlog:coversEntity ex:DE_Deck ;
    backlog:pursuesObjective ex:Obj_DecksRenewed ; backlog:hasApplicableConcern backlog:Concern_Data ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored at planning, through its stories." ;
    backlog:decomposesInto ex:EP_Deck, ex:EP_Research, ex:EP_Page .
ex:AC_Chapter a backlog:AcceptanceCriterion ; rdfs:label "A chapter item is accepted when its check passes and a stale fixture is refused"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasGherkinText "Given a chapter's published deck, research record and page, when every code example is run under current Python and every claim beyond the book is traced to the research record, then all pass - and a deck carrying one stale example is refused, naming it." ;
    backlog:satisfiedByArtifact "the chapter check, run against the release that carried the chapter" ; backlog:coveredByCase ex:TC_StaleExample .
ex:TC_StaleExample a backlog:TestCase ; rdfs:label "Put a stale example on a deck and require it refused"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:exercisesCriterion ex:AC_Chapter ; backlog:coversScenario ex:Scen_StaleCodeRefused ; backlog:runsOnData ex:Data_Stale ;
    backlog:hasCaseText "Insert an example whose output under current Python differs from the slide, run the chapter check, expect refusal naming it." .
ex:Data_Stale a backlog:TestData ; rdfs:label "One example taken from an earlier edition whose output has changed"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasFixtureState "A single code example with the output its slide shows, chosen so current Python prints something else." .
ex:Model_Class a backlog:ModelArtifact ; rdfs:label "How a renewed chapter is stored"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Design ;
    backlog:declaresState "A chapter has one ResearchRun, one Deck and one InteractivePage. The Deck and the Page each derive from the ResearchRun. The Deck and the Page are teaching materials in 03-materials, each described by learning-object metadata and aligned to the outcomes it serves. A Deck carries CodeExamples, each with the output its slide shows." ;
    backlog:describesItem ex:Init_Slides .
ex:Model_Component a backlog:ModelArtifact ; rdfs:label "What produces a renewed chapter"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:hasModelKind backlog:Kind_ComponentDiagram ; backlog:hasModelLevel backlog:Level_Design ;
    backlog:declaresState "RDODI's four-stage procedure produces the ResearchRun; the textbook ontology and edition supply the content; the deck builder produces the Deck from both; the page builder produces the InteractivePage from the ResearchRun; the chapter check runs examples under current Python and gates publication; the governed publisher releases into the course repository." ;
    backlog:describesItem ex:Init_Slides .
''']
    for k, label, what in KIND:
        L.append('''
ex:EP_%s a backlog:Epic ; rdfs:label "%s for every taught chapter"@en ; backlog:hasIdentifier "EP_%s" ; backlog:hasTitle "%s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:Proposed ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:appliesDefinitionOfDone ex:DoD ;
    backlog:coversEntity ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasApplicableConcern backlog:Concern_Data ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked through its stories' scores at planning." ;
    backlog:decomposesInto %s .
''' % (k, label, k, label, {"Deck": "DE_Deck", "Research": "DE_ResearchRun", "Page": "DE_InteractivePage"}[k], OBJ[k],
       ", ".join("ex:ST_%s_%s" % (k, cid(n)) for n, _ in CHAPTERS)))
        for n, src in CHAPTERS:
            dep = "" if k == "Research" else "\n    backlog:dependsOn ex:ST_Research_%s ;" % cid(n)
            L.append('''
ex:ST_%s_%s a backlog:Story ; rdfs:label "%s: %s"@en ; backlog:hasIdentifier "ST_%s_%s" ; backlog:hasTitle "%s for %s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;
    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "%s" ; backlog:soThat "students are taught from the edition they read, on researched ground" ;
    backlog:satisfiesDeliverable ex:Del_%s_%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion ex:AC_Chapter ;
    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;%s
    %s .
''' % (k, cid(n), label, src, k, cid(n), label, src.split(":")[0], what, k, cid(n), OBJ[k], dep, planned_tail(k, n)))
            if n in PLANNED:
                L.append(planned_block(k, n))
    L.append(ITER % (PLANNED_AT, ", ".join("ex:ST_%s_%s" % (k, cid(n)) for k, _, _ in KIND for n in sorted(PLANNED))))
    return "".join(L)
