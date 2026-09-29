"""Third iteration of the SEN0414 slide lineage: the rework of chapter 3 as a lecture, on the owner's feedback of 2026-09-29.
New work is new stories - no ruling binds work already started, and chapter 3's closed stories stay as they were. What happened to the two
done stories is read from the "rework" part of sen0414_slides_progress_v*.json (the newest), never composed here."""
__version__ = "1.0.0"
import glob, json, os

_pf = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0414_slides_progress_v*.json")), key=lambda x: [int(v) for v in os.path.splitext(x.rsplit("_v", 1)[1])[0].split("_")])
RW = json.load(open(_pf[-1])).get("rework", {"started": {}, "done": {}, "start_notes": {}}) if _pf else {"started": {}, "done": {}, "start_notes": {}}
PLANNED_AT_3 = "2026-09-29T05:54:00"   # the owner's message, 08:54 Istanbul, read from the message's own timestamp
KINDS = {"Deck": ("ReworkDeck", "Rework of the chapter 3 deck as a lecture", "the chapter 3 deck reworked as a lecture - a narrative in the speaker notes, click-by-click builds, and traces, number lines and pair diagrams drawn from executed specifications", "Obj_DecksRenewed", "Deck", (20, 20, 8, 5), "ex:ST_Deck_Ch03"),
         "Page": ("ReworkPage", "Rework of the chapter 3 page to share the deck's visuals", "the chapter 3 page showing the same executed visuals as the deck, each tested in the browser", "Obj_PagesBuilt", "Page", (13, 20, 5, 3), "ex:ST_Page_Ch03, ex:ST_ReworkDeck_Ch03")}
WHY = ("Components reused from the same kind of story in chapters 1 and 2, whose scores the owner approved; they were not approved again for this rework, so they are a proposal to the owner "
       "(L-116), not an approval. Time criticality is set by the class at 14:00 Istanbul on 2026-10-02.")
OUTCOME = {"Deck": "Settled: the deck is a lecture. Each slide has a talk track in its notes; an argument builds click by click; a process is drawn as a trace, a number line or pair lanes from a specification that was executed, never typed; every specification is re-run by the deck's check, and the programs the traces come from are re-run by the program check.",
           "Page": "Settled: the page draws the deck's specifications - traces with a stepper and run selector, number lines, pairs - behind the existing Visualise button, and its browser test steps through every pass of every run and counts every value and pair."}
TOOL = {"Deck": "08-tooling/ch03-deck: deck_check_v1_0_1.py, program_check_v1_0_0.py and visual_check_v1_0_0.py under Python 3.14.4",
        "Page": "08-tooling/sen0414_page_test_v9_6_0.py in headless Chromium; rdodi-ecosystem/07-pedagogy-professional-stage/02-gates/enriched_acceptance_v1_0_0.py; RDODI Stage 4 gates"}
CLOSE = {"Deck": "Closed on the deck check, the program check, the visual check and their three refused fixtures. Times read from the clock.",
         "Page": "Closed on the page's browser tests, its refused fixture and its acceptance gates. The Courseware attestation, the owner's, is pending and not claimed; the Stage 4 navigation gate fails as it did on the previous page and is not claimed. Times read from the clock."}

STORY = '''
ex:ST_%(sid)s_Ch03 a backlog:Story ; rdfs:label "%(label)s"@en ; backlog:hasIdentifier "ST_%(sid)s_Ch03" ; backlog:hasTitle "%(label)s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;
    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "%(what)s" ; backlog:soThat "a lecture teaches the concepts with a narrative and visuals, not with code listings" ;
    backlog:satisfiesDeliverable ex:Del_%(kind)s_Ch03 ; backlog:pursuesObjective ex:%(obj)s ; backlog:hasAcceptanceCriterion ex:AC_Chapter ;
    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;
    backlog:dependsOn %(dep)s ;
    backlog:hasState backlog:%(state)s ; backlog:memberOfContainer ex:Iter_3 ;
    backlog:hasPriorityScore ex:Score_%(sid)s ;
    backlog:decomposesInto ex:TK_%(sid)s_Build, ex:TK_%(sid)s_Verify .
ex:Score_%(sid)s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;
    backlog:hasScoreValue "%(v).2f"^^xsd:decimal ; backlog:scoredAt "%(t)s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;
    backlog:hasScoreRationale "WSJF = (business value %(bv)d + time criticality %(tc)d + risk reduction %(rr)d) / job size %(js)d, %(why)s" .
ex:Plan_%(sid)s a backlog:PlanningEvent ; rdfs:label "Planning of %(label)s into the third iteration"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:plannedAt "%(t)s"^^xsd:dateTime ; backlog:plannedBy backlog:Owner ; backlog:plannedInto ex:Iter_3 ;
    backlog:plansItem ex:ST_%(sid)s_Ch03 ; backlog:producesTask ex:TK_%(sid)s_Build, ex:TK_%(sid)s_Verify .
ex:Refine_%(sid)s a backlog:RefinementEvent ; rdfs:label "Refinement that made %(label)s ready"@en ;
    backlog:refines ex:ST_%(sid)s_Ch03 ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%(t)s"^^xsd:dateTime ;
    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:Iter_3 ; backlog:hasRefinementOutcome "%(o)s" .
'''
TASK = '''ex:TK_%(sid)s_%(tk)s a backlog:ExecutionTask ; rdfs:label "%(label)s: %(tkl)s"@en ; backlog:hasIdentifier "TK_%(sid)s_%(tk)s" ; backlog:hasTitle "%(tk)s %(label)s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:%(tstate)s ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_%(tk)s ; backlog:effectiveDefinitionOfDone ex:DoD ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story's score; scoring both would double-count." ;
    backlog:hasAuditNote "%(note)s" .
'''
CLOSED = '''
ex:Start_%(sid)s a backlog:TransitionEvent ; rdfs:label "%(label)s started"@en ; backlog:transitionedItem ex:ST_%(sid)s_Ch03 ;
    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%(st)s"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "%(sn)s" .
ex:Ev_%(sid)s a backlog:TestEvidence ; rdfs:label "Checks for %(label)s"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:attestsCriterion ex:AC_Chapter ; backlog:evidenceVerified true ; backlog:hasTestId "%(sid)s/Ch03" ;
    backlog:hasTestSpec "%(spec)s" ; backlog:hasVerificationMethod "Checks run over the artefacts as published in %(rel)s." ;
    backlog:verifiedByTool "%(tool)s" ; backlog:verifiedAt "%(fin)s"^^xsd:dateTime .
ex:Harness_%(sid)s a backlog:TestHarness ; rdfs:label "Checks for %(label)s"@en ;
    backlog:harnessFor ex:ST_%(sid)s_Ch03 ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:Ev_%(sid)s .
ex:Complete_%(sid)s a backlog:TransitionEvent ; rdfs:label "%(label)s completed"@en ;
    backlog:transitionedItem ex:ST_%(sid)s_Ch03 ; backlog:viaTransition backlog:T_Complete ;
    backlog:transitionedAt "%(cl)s"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "%(tn)s" .
'''


def rework_story(k):
    sid, label, what, obj, kind, (bv, tc, rr, js), dep = KINDS[k]; done = k in RW["done"]; d = RW["done"].get(k)
    state = ('Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ;\n    backlog:hasEvidence ex:Ev_%s ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (RW["started"][k], d["finished"], d["closed"], sid)) if done else "Ready"
    tstate = ('Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence ex:Ev_%s' % (RW["started"][k], d["finished"], sid)) if done else "Ready"
    t = STORY % dict(sid=sid, label=label, what=what, kind=kind, obj=obj, dep=dep, state=state, bv=bv, tc=tc, rr=rr, js=js, v=(bv + tc + rr) / js, t=PLANNED_AT_3, why=WHY, o=OUTCOME[k])
    for tk, tkl, note in (("Build", "build", "Build it."), ("Verify", "verify", "Run the checks and require the stale fixtures refused.")):
        t += TASK % dict(sid=sid, tk=tk, tkl=tkl, label=label, tstate=tstate, note=note)
    if done:
        t += CLOSED % dict(sid=sid, label=label, st=RW["started"][k], sn=RW["start_notes"][k], spec=d["spec"], rel=d["release"], fin=d["finished"], cl=d["closed"], tool=TOOL[k], tn=CLOSE[k])
    return t


OTHERS = '''
ex:ST_ReworkOthers_Ch01_02_04 a backlog:Story ; rdfs:label "Rework of the decks and pages of chapters 1, 2 and 4 with the same teaching devices"@en ; backlog:hasIdentifier "ST_ReworkOthers_Ch01_02_04" ;
    backlog:hasTitle "Rework of chapters 1, 2 and 4 as lectures" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;
    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "the decks and pages of chapters 1, 2 and 4 reworked with the teaching devices proposed in 03-materials/sen0414_teaching_devices_proposal_v1_0.md" ;
    backlog:soThat "every chapter is taught as a lecture, not from code listings" ;
    backlog:pursuesObjective ex:Obj_DecksRenewed ; backlog:hasAcceptanceCriterion ex:AC_Chapter ;
    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;
    backlog:dependsOn ex:ST_ReworkDeck_Ch03, ex:ST_ReworkPage_Ch03 ;
    backlog:hasState backlog:Proposed ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Not planned: the owner asked for it once chapter 3 has reached a maturity level he judges, which he has not yet done." .
'''

ITER3 = '''
ex:Iter_3 a backlog:Iteration ; rdfs:label "Third iteration: chapter 3 reworked as a lecture, before the class of 2 October"@en ;
    backlog:hasIdentifier "Iter_3" ; backlog:belongsToLineage ex:Lineage ;
    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-10-02T11:00:00"^^xsd:dateTime ;
    backlog:hasDurationSource "Owner, 2026-09-29 (the message's own timestamp, 08:54 Istanbul): rework chapter 3's deck and page. The owner gave no date, so the period runs to SEN0414's next class, 14:00 Istanbul on Friday 2026-10-02, as the second iteration does - taken from the course timetable, not chosen for the work." ;
    backlog:hasSprintGoal "Chapter 3's deck and page reworked as a lecture and shared visuals, ready to present; the other chapters wait for the owner's judgement." ;
    backlog:hasMember %s .
'''
SESSION3 = '''
ex:Session_Iter3 a backlog:RegisterSession ; rdfs:label "The session that reworked chapter 3 as a lecture, in the third iteration"@en ;
    backlog:sessionFor ex:Backlog ; backlog:sessionConductedBy "claude-code-course-materials-session" ;
    backlog:sessionStartedAt "%s"^^xsd:dateTime ; backlog:sessionEndedAt "%s"^^xsd:dateTime ;
    backlog:stateVerifiedAtStart true ;
    backlog:hasSessionScopeNote "Ran the discipline ceremony first from the files on GitHub (governance at Ontologies 087b9c2, knowledge base 2.32.0, OE discipline 2.12.1, lineage discipline 70.0.0), then planned the rework of chapter 3 into the third iteration on the owner's feedback, reworked its deck and page, and wrote the teaching-device taxonomy as a proposal to the owner." ;
    backlog:changedItem ex:ST_ReworkDeck_Ch03, ex:ST_ReworkPage_Ch03, ex:ST_ReworkOthers_Ch01_02_04 .
'''
FINDINGS = '''
ex:Finding_DecksReadAsListings a backlog:RetrospectiveFinding ;
    rdfs:label "The chapter 3 deck read as source-code listings and had little to look at"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Deck_Ch03, ex:ST_ReworkDeck_Ch03, ex:ST_ReworkPage_Ch03 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner's feedback of 2026-09-29: the decks lack the narrative the pages carry, are in effect source-code listings and so are not useful for a course, above all for theory, and use few visualisations, although PowerPoint offers many facilities to make a lecture interesting. The deck builder took every example and output from the executed research record, which made every slide correct and checked but gave it no argument: a slide was a program and its result, and the page's visuals - which only the page had - were never drawn on a slide." ;
    backlog:hasRemedy "Chapter 3's deck was rebuilt as version 2.0.0, a lecture of 30 slides: a talk track in every slide's notes; 76 click-by-click builds and fade transitions; predict-first and retrieval slides; and traces, number lines and pair lanes drawn as native shapes. Each drawn value comes from a specification produced by running code, and the page draws the same specifications, so the two cannot differ. A new check, visual_check_v1_0_0.py, re-runs the specifications and refuses a slide whose value differs, and requires each visual to be complete and its program to be one the program check re-runs. The other chapters are not touched until the owner judges chapter 3 mature." .

ex:Proposal_TeachingDevices a backlog:RetrospectiveFinding ;
    rdfs:label "Proposal to the owner: a taxonomy of teaching devices for decks and pages"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_ReworkDeck_Ch03, ex:ST_ReworkPage_Ch03, ex:ST_ReworkOthers_Ch01_02_04 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner proposed building a taxonomy of the features a lecture can use and adapting them to pages and concepts, with the visuals shared between slides and interactive pages. Which device suits which kind of content, and which RDODI widget primitive and discourse feature each one corresponds to, are not settled by the evidence: RDODI's own detection of the ordered-argument feature is marked interpretive." ;
    backlog:hasRemedy "Written as a proposal, not a ruling (L-116), in 03-materials/sen0414_teaching_devices_proposal_v1_0.md: 14 devices, each with its purpose, RDODI pairing, PowerPoint form and page form; a rule for choosing a device by content kind; and the obligations that come with a device. Chapter 3 was built with 12 of them. Awaiting the owner: the pairings, whether devices 7 and 14 need a slide form, and when chapter 3 counts as mature." .

ex:Finding_Ch03PageNameClashes a backlog:RetrospectiveFinding ;
    rdfs:label "Two names in the new page visuals clashed with names already in the template, and the page test found both"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_ReworkPage_Ch03 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The first page 9.6.0 build passed the page's visual tests but failed two existing ones. The new trace stepper was named traceShow, replacing the Lab's function of that name, so the Step through tab stopped working and its test timed out; and the imported-names visual used the class chip, which the test 'subject screens carry no repeated lists' counts as a repeated list, so it failed with the page showing no such list." ;
    backlog:hasRemedy "The stepper's functions were renamed vtraceShow and vtraceMove and the class became nmchip; the page 9.6.0 had not been released, so it was rebuilt under the same version and every check re-run. The template and the test remain forks of shared tooling, to be consolidated by CME." .

ex:Finding_Ch03PageChecksOneFlaky a backlog:RetrospectiveFinding ;
    rdfs:label "One check failed on one run of the final chapter 3 page and passed when the same build was run again"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_ReworkPage_Ch03 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "Of two runs of page test 9.6.0 over the final build, the first failed 'agents rank by meaning (sentence embeddings)' (12 cited passages) and every other check passed; the second passed all 50. The build had not changed between them. The check waits on the embedding model, which the page loads over the network; the cause of the one failure was not determined." ;
    backlog:hasRemedy "Not remedied. The record states the failed run and the passing run; the check is a candidate for a longer wait in a later test version." .

ex:Finding_Ch03Stage4SameAsBefore a backlog:RetrospectiveFinding ;
    rdfs:label "The chapter 3 page 9.6.0 gets the same Stage 4 verdicts as page 9.5.0"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_ReworkPage_Ch03 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "RDODI's navigation-affordance gate reports the same patterns realised but not declared (tooltip, table of contents, focus indicator, current-location indicator) and one declared but not found (primary navigation) on page 9.6.0 as on page 9.5.0; its router gate passes. The new visuals changed no navigation." ;
    backlog:hasRemedy "Not remedied and not claimed as passed, as in the earlier finding on Stage 4's gates: the cause lies in the page ABox builder and template, a change to shared tooling and a ruling for the owner." .
'''


def rework_block(end_time):
    """The whole third iteration: stories, the story for the other chapters, the iteration, the session and the findings."""
    members = ["ex:ST_%s_Ch03" % KINDS[k][0] for k in ("Deck", "Page")]
    t = "".join(rework_story(k) for k in ("Deck", "Page")) + OTHERS + FINDINGS
    t += ITER3 % (PLANNED_AT_3, ", ".join(members))
    t += SESSION3 % (PLANNED_AT_3, end_time)
    return t
