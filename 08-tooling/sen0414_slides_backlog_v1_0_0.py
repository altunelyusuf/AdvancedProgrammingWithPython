"""Backlog stage of the SEN0414 slide lineage: admission only. Every item Proposed; no task yet -
tasks are produced by planning, and only for what is planned into an iteration."""
from sen0414_slides_stages_v1_0_0 import CHAPTERS, KIND, cid

OBJ = {"Deck": "Obj_DecksRenewed", "Research": "Obj_ResearchRecorded", "Page": "Obj_PagesBuilt"}


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
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:Proposed ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;
    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "%s" ; backlog:soThat "students are taught from the edition they read, on researched ground" ;
    backlog:satisfiesDeliverable ex:Del_%s_%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion ex:AC_Chapter ;
    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;%s
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored at planning, when the owner sets business value and time criticality." .
''' % (k, cid(n), label, src, k, cid(n), label, src.split(":")[0], what, k, cid(n), OBJ[k], dep))
    return "".join(L)
