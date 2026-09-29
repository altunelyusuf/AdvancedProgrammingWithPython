"""Fourth iteration of the SEN0414 slide lineage: chapter 5 (planned here; its research, deck and page stories are the generic chapter stories of
sen0414_slides_backlog_v1_5_0.py) and the page-template feedback the owner gave on 2026-09-29 (10:00 Istanbul). New work is new stories - no ruling
binds work already started, and the closed stories of chapters 1-4 stay as they were. What happened to the template story is read from the "iter4" part
of sen0414_slides_progress_v*.json (the newest), never composed here."""
__version__ = "1.1.0"
# 1.1.0: adds the second review story of 2026-09-29 (14:01 Istanbul): page 9.9.0 - SPARQL samples load on selection, formatted agent answers, a quiz that covers every concept and builds questions on request.
import glob, json, os

_pf = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0414_slides_progress_v*.json")), key=lambda x: [int(v) for v in os.path.splitext(x.rsplit("_v", 1)[1])[0].split("_")])
_P = json.load(open(_pf[-1])) if _pf else {}
IT = _P.get("iter4", {"started": {}, "done": {}, "start_notes": {}})
PLANNED_AT_4 = "2026-09-29T07:00:00"   # the owner's message, 10:00 Istanbul, as noted when it arrived; the earliest chapter 5 file is stamped 07:13:03
WHY = ("Components reused from the same kind of story in chapters 1 and 2, whose scores the owner approved; they were not approved again for this story, so they are a proposal to the owner "
       "(L-116), not an approval. Time criticality is set by the class at 14:00 Istanbul on 2026-10-02.")
K_TEMPLATE = ("Template", "Page template 9.7.0 from the owner's feedback on the pages", "the interactive page template changed as the owner asked - no Next-step button, no space wasted above the Lab and Maps views, code areas that use the free space - with a Lecture tab carrying the deck's talk track and a Resources tab of checked links and labelled searches", "Obj_PagesBuilt", "Page", (13, 20, 8, 5), "ex:ST_Page_Ch05")
K_REVIEW = ("Review", "Deck 1.0.1 and page 9.8.0 from the owner's review of chapter 5", "the chapter 5 deck opening in PowerPoint without repair, examples that fill the code when chosen, Step through that starts on the first Step, and a Code pipeline with a choice of examples", "Obj_PagesBuilt", "Page", (13, 20, 8, 3), "ex:ST_Page_Ch05")
OUTCOME_REVIEW = "Settled: the deck's paragraph properties are in the order PowerPoint requires, checked by a new structure check; choosing an example fills the code in the Playground, the Code Lab, Step through and the Code pipeline; Step through traces on the first Step; the Code pipeline offers examples and runs on demand."
OUTCOME = "Settled: the concept section shows a static example with no button; the sub-page heading and view notes fold into the tab row; code areas take the free height; a Lecture tab shows the deck's talk track with jumps to the concepts and visuals; a Resources tab lists links whose pages were opened and read, with a labelled search for every concept. Applied to the chapter 5 page only: the pages of chapters 1 to 4 stay as published until the owner judges."
TOOL = "08-tooling/sen0414_page_test_v9_7_0.py in headless Chromium on the chapter 5 page; 08-tooling/template_patch_v9_7_0.py regenerates the template from 9.6.0"
CLOSE = "Closed on the page's browser tests, which cover every feature the story names. The published chapter 3 page and the pages of chapters 1, 2 and 4 were not changed. Times read from the clock."

STORY = '''
ex:ST_%(sid)s_Ch05 a backlog:Story ; rdfs:label "%(label)s"@en ; backlog:hasIdentifier "ST_%(sid)s_Ch05" ; backlog:hasTitle "%(label)s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;
    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "%(what)s" ; backlog:soThat "a lecture teaches the concepts with a narrative and visuals, not with code listings" ;
    backlog:satisfiesDeliverable ex:Del_%(kind)s_Ch05 ; backlog:pursuesObjective ex:%(obj)s ; backlog:hasAcceptanceCriterion ex:AC_Chapter ;
    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;
    backlog:hasState backlog:%(state)s ; backlog:memberOfContainer ex:Iter_4 ;
    backlog:hasPriorityScore ex:Score_%(sid)s ;
    backlog:decomposesInto ex:TK_%(sid)s_Build, ex:TK_%(sid)s_Verify .
ex:Score_%(sid)s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;
    backlog:hasScoreValue "%(v).2f"^^xsd:decimal ; backlog:scoredAt "%(t)s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;
    backlog:hasScoreRationale "WSJF = (business value %(bv)d + time criticality %(tc)d + risk reduction %(rr)d) / job size %(js)d, %(why)s" .
ex:Plan_%(sid)s a backlog:PlanningEvent ; rdfs:label "Planning of %(label)s into the fourth iteration"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:plannedAt "%(t)s"^^xsd:dateTime ; backlog:plannedBy backlog:Owner ; backlog:plannedInto ex:Iter_4 ;
    backlog:plansItem ex:ST_%(sid)s_Ch05 ; backlog:producesTask ex:TK_%(sid)s_Build, ex:TK_%(sid)s_Verify .
ex:Refine_%(sid)s a backlog:RefinementEvent ; rdfs:label "Refinement that made %(label)s ready"@en ;
    backlog:refines ex:ST_%(sid)s_Ch05 ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%(t)s"^^xsd:dateTime ;
    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:Iter_4 ; backlog:hasRefinementOutcome "%(o)s" .
'''
TASK = '''ex:TK_%(sid)s_%(tk)s a backlog:ExecutionTask ; rdfs:label "%(label)s: %(tkl)s"@en ; backlog:hasIdentifier "TK_%(sid)s_%(tk)s" ; backlog:hasTitle "%(tk)s %(label)s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:%(tstate)s ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_%(tk)s ; backlog:effectiveDefinitionOfDone ex:DoD ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story's score; scoring both would double-count." ;
    backlog:hasAuditNote "%(note)s" .
'''
CLOSED = '''
ex:Start_%(sid)s a backlog:TransitionEvent ; rdfs:label "%(label)s started"@en ; backlog:transitionedItem ex:ST_%(sid)s_Ch05 ;
    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%(st)s"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "%(sn)s" .
ex:Ev_%(sid)s a backlog:TestEvidence ; rdfs:label "Checks for %(label)s"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:attestsCriterion ex:AC_Chapter ; backlog:evidenceVerified true ; backlog:hasTestId "%(sid)s/Ch05" ;
    backlog:hasTestSpec "%(spec)s" ; backlog:hasVerificationMethod "Checks run over the artefacts as published in %(rel)s." ;
    backlog:verifiedByTool "%(tool)s" ; backlog:verifiedAt "%(fin)s"^^xsd:dateTime .
ex:Harness_%(sid)s a backlog:TestHarness ; rdfs:label "Checks for %(label)s"@en ;
    backlog:harnessFor ex:ST_%(sid)s_Ch05 ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:Ev_%(sid)s .
ex:Complete_%(sid)s a backlog:TransitionEvent ; rdfs:label "%(label)s completed"@en ;
    backlog:transitionedItem ex:ST_%(sid)s_Ch05 ; backlog:viaTransition backlog:T_Complete ;
    backlog:transitionedAt "%(cl)s"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "%(tn)s" .
'''



TOOL_REVIEW = "08-tooling/ch05-deck/structure_check_v1_0_0.py, deck_check_v1_0_1.py, program_check_v1_0_0.py and visual_check_v1_1_0.py under Python 3.14.4; 08-tooling/sen0414_page_test_v9_8_0.py in headless Chromium"
CLOSE_REVIEW = "Closed on the deck's four checks and the page's browser tests and refused fixture. That the deck opens in PowerPoint without repair is inferred from the schema order, not observed: PowerPoint could not be run here. Times read from the clock."
FINDINGS_REVIEW = '''
ex:Finding_Ch05PowerPointRepair a backlog:RetrospectiveFinding ;
    rdfs:label "PowerPoint offered to repair the chapter 5 deck on opening"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Deck_Ch05, ex:ST_Review_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner reported an error about the content on opening deck 1.0.0, and a repair that removed part of the file. The deck's text boxes built from several runs (the 'On the page' footers and similar) carried a paragraph-properties element after a run; the file format requires it first in the paragraph, and PowerPoint repairs the part when it is not. No deck check looked at the file's structure: all of them read values, so the deck was correct in every value they compared and still malformed. The same fault is in the released decks of chapter 1 (20 paragraphs), chapter 2 (23), chapter 3 (29 in 1.0.0, 25 in 2.0.0) and chapter 4 (7); the owner has reported it only for chapter 5." ;
    backlog:hasRemedy "Deck 1.0.1 of chapter 5: a build step removes the misplaced elements (64, all repeats of the paragraph's first) and a new structure check refuses a deck with any (42 paragraphs in 1.0.0, 0 in 1.0.1). That it now opens cleanly is inferred, not observed. Proposed to the owner (L-116), not done: the same repair for the released decks of chapters 1 to 4, as new versions, which would replace the decks the owner is using or has yet to review." .

ex:Finding_Ch05ExampleSelectors a backlog:RetrospectiveFinding ;
    rdfs:label "The page made the learner press a second button after choosing an example, or before stepping"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch05, ex:ST_Review_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner's review: a chosen example did not fill the code until Load example was pressed; Step through did nothing until Trace was pressed; the Code pipeline had no examples to choose from. The template built each of these as a two-step control (choose or edit, then press) and its tests pressed both buttons, so they could not see the extra step." ;
    backlog:hasRemedy "Template 9.8.0 and page 9.8.0: choosing an example fills the code in the Playground, the Code Lab, Step through and the Code pipeline; the Load and Trace buttons are gone; the first Step, Back, First or Play traces, and a change of code or input traces again; the pipeline runs when a stage or Next stage is pressed. The page test now chooses and steps without the extra press, and runs every example of both new lists. Found while testing: chosen examples with the same program kept the earlier step position, so choosing an example now always restarts, and duplicate programs are left out of the lists. Applied to the chapter 5 page only, as with 9.7.0." .
'''

K_REVIEW2 = ("Review2", "Page 9.9.0 from the owner's second review of chapter 5", "the SPARQL console loading a sample as soon as it is chosen, agent answers laid out for reading, and a quiz that covers the whole chapter and makes new questions when the learner asks", "Obj_PagesBuilt", "Page", (13, 20, 8, 3), "ex:ST_Page_Ch05")
OUTCOME_REVIEW2 = "Settled: choosing a SPARQL sample fills the query with no second press; agent answers have a lead sentence, bullet points, coloured code words, an example block and related-concept links; a question builder makes a question of any of four kinds on demand, for any part of the chapter or one for every concept, with a coverage line. Applied to the chapter 5 page only."
TOOL_REVIEW2 = "08-tooling/sen0414_page_test_v9_9_0.py in headless Chromium on the chapter 5 page; 08-tooling/template_patch_v9_9_0.py regenerates the template from 9.8.0"
CLOSE_REVIEW2 = "Closed on the page's browser tests and refused fixture. The generated questions are built by templates from the chapter's data, not written by a model, and are not part of the page ABox or the acceptance gates. Times read from the clock."
FINDINGS_REVIEW2 = '''
ex:Finding_Ch05SparqlTwoStep a backlog:RetrospectiveFinding ;
    rdfs:label "The SPARQL console still needed a second press after choosing a sample"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch05, ex:ST_Review2_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner's review: choosing a sample query did nothing until Load sample was pressed. Version 9.8.0 removed the Load button from four other selectors but the SPARQL console was not among the controls listed, so the same two-step design stayed in it; the test pressed the button and so could not see it." ;
    backlog:hasRemedy "Template 9.9.0: the sample list fills the query on change and the button is gone; the test now selects and asserts the text without a press. The other selectors were checked for a remaining Load or Trace button: none." .

ex:Finding_Ch05UnreadableAnswers a backlog:RetrospectiveFinding ;
    rdfs:label "Agent answers were one long run of text"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch05, ex:ST_Review2_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner's review: answers were long running text; formatting, paragraphs, bullets, code snippets and colours would help. The composer joined the retrieved passages into one paragraph and the page printed it as plain text, and the earlier tests compared only the words." ;
    backlog:hasRemedy "Template 9.9.0: the first passage is a lead sentence, the others bullet points, source marks are numbered, Python words in answers are coloured as in the code areas, an example asked for is shown as a code block with its output, related concepts are chips that open the concept, and text from a live model (Markdown) is rendered as paragraphs, lists and code blocks. What the answer says is unchanged: the same passages, laid out. Found while testing: an asked-for example was missing when none of the retrieved passages had one, so the agent's own concepts are now searched for an example." .

ex:Finding_Ch05QuizScope a backlog:RetrospectiveFinding ;
    rdfs:label "The quiz covered the five objectives with eleven items, not the chapter"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch05, ex:ST_Review2_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner's review: the quiz should cover the scope, and questions should be built when the user asks. The authored quiz has 11 items and the acceptance gates check that it assesses each of the five objectives; nothing checked how much of the chapter's 46 concepts it touched, and it touched few." ;
    backlog:hasRemedy "Template 9.9.0 adds a question builder under the authored items: a scope (whole chapter, one subject, one sub-subject or one concept) and a kind (predict the output, name the concept, place it in the taxonomy, pick a kind of), a New question button, a button that makes one question for every concept, a score, and a line saying how many concepts have been asked about and answered rightly. The test builds all 111 possible questions of the 46 concepts and checks options and answers. Limits stated to the owner: the questions are filled from the chapter's data by templates, not written by a model or a person, so their wording is plain and their distractors come from neighbouring concepts; they are not in the page ABox and the acceptance gates do not see them; the authored quiz still maps only to the objectives CO1 to CO5. Proposed (L-116), awaiting the owner: an authored item bank per concept, and asking a live model for questions when the browser has one." .
'''


def template_story(K=None, OUTCOME=OUTCOME, TOOL=TOOL, CLOSE=CLOSE):
    K = K or K_TEMPLATE; key = K[0]
    sid, label, what, obj, kind, (bv, tc, rr, js), dep = K; done = key in IT["done"]; d = IT["done"].get(key)
    state = ('Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ;\n    backlog:hasEvidence ex:Ev_%s ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (IT["started"][key], d["finished"], d["closed"], sid)) if done else "Ready"
    tstate = ('Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence ex:Ev_%s' % (IT["started"][key], d["finished"], sid)) if done else "Ready"
    t = STORY % dict(sid=sid, label=label, what=what, kind=kind, obj=obj, dep=dep, state=state, bv=bv, tc=tc, rr=rr, js=js, v=(bv + tc + rr) / js, t=(IT["started"][key] if key != "Template" else PLANNED_AT_4), why=WHY, o=OUTCOME)
    for tk, tkl, note in (("Build", "build", "Build it."), ("Verify", "verify", "Run the checks on the chapter 5 page.")):
        t += TASK % dict(sid=sid, tk=tk, tkl=tkl, label=label, tstate=tstate, note=note)
    if done:
        t += CLOSED % dict(sid=sid, label=label, st=IT["started"][key], sn=IT["start_notes"][key], spec=d["spec"], rel=d["release"], fin=d["finished"], cl=d["closed"], tool=TOOL, tn=CLOSE)
    return t


ITER4 = '''
ex:Iter_4 a backlog:Iteration ; rdfs:label "Fourth iteration: chapter 5 and the page template feedback, before the class of 2 October"@en ;
    backlog:hasIdentifier "Iter_4" ; backlog:belongsToLineage ex:Lineage ;
    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-10-02T11:00:00"^^xsd:dateTime ;
    backlog:hasDurationSource "Owner, 2026-09-29 (10:00 Istanbul): build the next chapter of SEN0414 with the enhancements he named. The owner gave no date, so the period runs to SEN0414's next class, 14:00 Istanbul on Friday 2026-10-02, as the second and third iterations do - taken from the course timetable, not chosen for the work." ;
    backlog:hasSprintGoal "Chapter 5 researched, its deck built as a lecture and its page built on the revised template, ready to present; chapters 1, 2 and 4 wait for the owner's judgement." ;
    backlog:hasMember %s .
'''
SESSION4 = '''
ex:Session_Iter4 a backlog:RegisterSession ; rdfs:label "The session that built chapter 5 with the owner's enhancements, in the fourth iteration"@en ;
    backlog:sessionFor ex:Backlog ; backlog:sessionConductedBy "claude-code-course-materials-session" ;
    backlog:sessionStartedAt "%s"^^xsd:dateTime ; backlog:sessionEndedAt "%s"^^xsd:dateTime ;
    backlog:stateVerifiedAtStart true ;
    backlog:hasSessionScopeNote "Ran the discipline ceremony first from the files on GitHub (governance at Ontologies 087b9c2, knowledge base 2.32.0, OE discipline 2.12.1, lineage discipline 70.0.0), and re-read both discipline files at the release from governance 432507d, where they were byte-identical to the ceremony's (sha ee2052c9 and 7860dc89), then planned chapter 5 and the page-template feedback into the fourth iteration on the owner's request, built chapter 5's research record, lecture deck and page, and revised the page template as the owner asked; wrote version 1.1 of the teaching-device proposal; then, on the owner's review, repaired the deck (1.0.1) and the page (9.8.0); then, on his second review, page 9.9.0." ;
    backlog:changedItem ex:ST_Research_Ch05, ex:ST_Deck_Ch05, ex:ST_Page_Ch05, ex:ST_Template_Ch05, ex:ST_Review_Ch05, ex:ST_Review2_Ch05 .
'''

FINDINGS4 = '''
ex:Finding_Ch05OwnerPageFeedback a backlog:RetrospectiveFinding ;
    rdfs:label "The owner found the Next-step button useless and the Lab and Maps views short of room"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Template_Ch05, ex:ST_Page_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner's feedback of 2026-09-29: the Next step button in a concept section is not a walk-through, it only reveals one more line, and almost every section has one; the Lab and Maps views waste space at the top of the sub-page, which limits the work area and causes fit problems; the code space is limited even when there is unused space. Cause in the template: a concept section was drawn as a two-item list with a button; every sub-page repeated its heading and a note above the content; code areas had fixed heights." ;
    backlog:hasRemedy "Template 9.7.0 (08-tooling/course_page_template_v9_7_0.html, made from 9.6.0 by template_patch_v9_7_0.py): a concept section shows its example as code with no button; the heading is hidden under the tab row and the notes fold into an About fold; code areas grow to their text and the playground takes the free height. Measured in a 1400x900 window the concept map now starts 154 pixels from the top instead of 288. Applied to the chapter 5 page only; the pages of chapters 1 to 4 are not changed until the owner judges. The evaluation stepper of an example that has several reductions is a different control and was kept." .

ex:Proposal_Ch05Opportunities a backlog:RetrospectiveFinding ;
    rdfs:label "Proposal to the owner: what else could be done with visualisations, animations, simulations and external links"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Deck_Ch05, ex:ST_Page_Ch05, ex:ST_Template_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner asked on 2026-09-29 whether there are other opportunities, especially for visualisations, animations, simulations and external links to supportive material, discussions and YouTube videos. What the evidence settles: a debugger simulator, a logging-level matrix and an exception climb can be drawn from executed specifications on both slides and page (built in chapter 5); a talk track on the page and links from slide to page are cheap. What it does not settle: which videos and discussions are worth recommending, because this environment cannot open YouTube or Stack Overflow and so cannot read what a video says or judge a thread." ;
    backlog:hasRemedy "Built in chapter 5: three new visual kinds on deck and page, a Lecture tab, slide footers that link to the page sections, a Resources tab of links whose pages were opened and read (14), and a labelled search on YouTube, Stack Overflow and discuss.python.org for every concept (searches, not recommendations). Proposed, not built, awaiting the owner: (1) video and discussion links supplied and checked by the owner, for which the Resources file already has a place; (2) a live debugger in the page, which needs a Python that supports tracing in the browser and is a larger story; (3) simulations for the earlier chapters' concepts (a scope simulator for chapter 4, a call-stack simulator for recursion), which follow the owner's judgement of the rework. Recorded in 03-materials/sen0414_teaching_devices_proposal_v1_1.md as devices 15 to 21." .

ex:Finding_Ch05VersionDependentExample a backlog:RetrospectiveFinding ;
    rdfs:label "One example printed True under Python 3.14.4 and False in the browser, and the page test found it"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch05, ex:ST_Research_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The example for remote attach asked whether sys has the name remote_exec, which Python 3.14 added. Its stored result, recorded under 3.14.4, was True; the page runs examples in Pyodide, whose Python is older, and printed False. The page test 'edited code really runs' failed on it, as did the page's own built-in checks and the Code Lab." ;
    backlog:hasRemedy "The page example was changed to a check that holds in both (callable of sys.breakpointhook, True since Python 3.7); the research record, its document and the page were rebuilt, and the deck keeps the remote_exec check because the deck's checks run under 3.14.4. A page example must print the same in the browser's Python as in the build interpreter; the chapter's concept text about attaching to a running process is unchanged and cited (Galindo Salgado, Wozniski and Stojanovic, 2024)." .

ex:Finding_Ch05FirstPageRefused a backlog:RetrospectiveFinding ;
    rdfs:label "The acceptance gate refused the first chapter 5 page: an objective had no quiz item"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The Courseware profile's assessment-rigor and Bloom-coverage gates reported that objective CO1 (raise an exception with a message and read the traceback of one nobody handles) was assessed by no item; the first quiz had ten items for CO2 to CO5. A related defect surfaced when the added item first held a line break: the page ABox writer puts a question into a Turtle string literal without escaping line breaks, so the ABox failed to parse." ;
    backlog:hasRemedy "A CO1 item at the Apply level was added (11 items) and its answer confirmed by running the function under Python 3.14.4; the question was written on one line. The ABox writer was not changed: a fix is a change to shared tooling and is left for the owner's ruling, and a question with a line break stays a known hazard." .

ex:Finding_Ch05VerifiedAtWrongArgument a backlog:RetrospectiveFinding ;
    rdfs:label "The research builder was given a version where it wants a time, then a local time where the record uses UTC"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Research_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The builder's second argument is the time the sources were verified. In a rebuild it was given 1.0.0, so the record held an invalid time (the page data build failed on it); the next rebuild took the clock's reading, which was Istanbul time, while the lineage records UTC, so the record claimed a verification three hours in the future. The builder accepts either value without complaint." ;
    backlog:hasRemedy "The record was rebuilt with the UTC clock reading (08:06:45) and every gate, check and the page re-run. Not remedied in the builder: it should refuse a value that is not a time; a change to shared tooling, left for the owner's ruling." .

ex:Finding_Ch05DeckCheckInterpreter a backlog:RetrospectiveFinding ;
    rdfs:label "The deck check refused a correct slide because it ran under the wrong Python"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Deck_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The first build ran the expression check with the system Python (3.11) because that interpreter has the libraries the check needs; a slide that shows a 3.14 feature was refused. The check does not report which interpreter it ran under." ;
    backlog:hasRemedy "The build script runs every deck check under the interpreter the course teaches (3.14.4), and the chapter 3 and 4 decks were confirmed to pass under it. The check should print the interpreter's version; left for a later version." .

ex:Finding_Ch05CitationRuleHyphen a backlog:RetrospectiveFinding ;
    rdfs:label "The reference gate does not read a hyphenated surname as a citation"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Research_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "RDODI's Stage3.F pattern for a citation, a capitalised surname followed by a year in parentheses, does not match Hatfield-Dodds (2021), the author of PEP 678, so a sentence that cited only that source was reported as uncited." ;
    backlog:hasRemedy "The sentence also cites the Python Software Foundation (2026), which the gate reads; the gate itself is RDODI's and is not changed here. Reported so the pattern can be widened." .

ex:Finding_Ch05Stage4SameAsBefore a backlog:RetrospectiveFinding ;
    rdfs:label "The chapter 5 page gets the same Stage 4 verdicts as the pages of chapters 3 and 4"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "RDODI's proposed coverage and substance gates and its navigation gate fail on the chapter 5 page as on the published chapter 3 and 4 pages (typed individuals without label and content, individuals of fewer than five words, hybrid chains not checkable); parse, shapes and source validity pass." ;
    backlog:hasRemedy "Not remedied and not claimed as passed, as in the earlier findings on Stage 4: the cause lies in the page ABox builder and template, a change to shared tooling and a ruling for the owner." .

ex:Finding_Ch05TagsNotPushed a backlog:RetrospectiveFinding ;
    rdfs:label "The release commit lands on the main branch but its tag cannot be pushed"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "On the releases this session has made so far the publisher pushed the main branch, which succeeded, and then the release tag, which the repository refused with HTTP 403 for the credential the session holds; a rerun then reported the release as already published. The release commit is on the main branch; the tag was not on the remote." ;
    backlog:hasRemedy "Not remedied here. The owner can push the release tags (sen0414-v2.31.0 is the newest) with a credential that may create tags, or allow this credential to." .
'''


def iter4_block(end_time, chapter_members):
    members = chapter_members + ["ex:ST_Template_Ch05"] + (["ex:ST_Review_Ch05"] if "Review" in IT["done"] else []) + (["ex:ST_Review2_Ch05"] if "Review2" in IT["done"] else [])
    t = template_story() + FINDINGS4
    if "Review" in IT["done"]:
        t += template_story(K_REVIEW, OUTCOME_REVIEW, TOOL_REVIEW, CLOSE_REVIEW) + FINDINGS_REVIEW
    if "Review2" in IT["done"]:
        t += template_story(K_REVIEW2, OUTCOME_REVIEW2, TOOL_REVIEW2, CLOSE_REVIEW2) + FINDINGS_REVIEW2
    t += ITER4 % (PLANNED_AT_4, ", ".join(members))
    t += SESSION4 % (PLANNED_AT_4, end_time)
    return t
