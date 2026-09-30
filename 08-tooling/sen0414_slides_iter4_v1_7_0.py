"""Fourth iteration of the SEN0414 slide lineage: chapter 5 (planned here; its research, deck and page stories are the generic chapter stories of
sen0414_slides_backlog_v1_5_0.py) and the page-template feedback the owner gave on 2026-09-29 (10:00 Istanbul). New work is new stories - no ruling
binds work already started, and the closed stories of chapters 1-4 stay as they were. What happened to the template story is read from the "iter4" part
of sen0414_slides_progress_v*.json (the newest), never composed here."""
__version__ = "1.7.0"
# 1.7.0: adds the build of the question types, the mock exams and the live-model choice asked for on 2026-09-30 (14:21 Istanbul, 11:21 UTC), with the disposition of every item asked.
# 1.6.0: adds the build of the proposals of 2026-09-30 (12:41 Istanbul, 09:41 UTC) that were ready, the work-arounds, and the items parked with their reasons.
# 1.5.0: adds the enrichment of the pages after the owner's review of 2026-09-30 (10:15 Istanbul, 07:15 UTC): clickable references, a page-wide search, a check on the local model's replies, and the proposals for further features.
# 1.4.0: adds the return to chapters 1 to 4 - the owner's message of 2026-09-29 (20:19 Istanbul, 17:19 UTC): written question banks for their pages and the pages rebuilt on template 9.11.0 - and its findings.
# 1.3.0: adds chapter 6 (Lists) to the fourth iteration - the owner's "Yes, proceed" of 2026-09-29 (17:51 Istanbul, 14:51 UTC) on the plan to build the next chapter - and the findings of that work.
# 1.2.0: adds the three stories the owner approved on 2026-09-29 (14:27 Istanbul): the written question bank, the live-model question, and the repair of the chapter 1-4 decks and pages.
# 1.1.0: adds the second review story of 2026-09-29 (14:01 Istanbul): page 9.9.0 - SPARQL samples load on selection, formatted agent answers, a quiz that covers every concept and builds questions on request.
import glob, json, os

_pf = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0414_slides_progress_v*.json")), key=lambda x: [int(v) for v in os.path.splitext(x.rsplit("_v", 1)[1])[0].split("_")])
_P = json.load(open(_pf[-1])) if _pf else {}
IT = _P.get("iter4", {"started": {}, "done": {}, "start_notes": {}})
PLANNED_AT_6 = "2026-09-29T14:51:00"   # the owner's message, 17:51 Istanbul, as timestamped on arrival
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

K_BANK = ("Bank", "A written question bank for the chapter 5 page", "a written item for every concept of chapter 5, with the answers of its programs checked by running them, offered by the page's question builder", "Obj_PagesBuilt", "Page", (13, 20, 8, 5), "ex:ST_Page_Ch05")
K_LIVE = ("Live", "A live-model question in the chapter 5 page's question builder", "a button that asks the page's language model for a new question from the chapter text and shows it only when it is well formed and, if it has code, when the code prints the marked answer", "Obj_PagesBuilt", "Page", (8, 20, 8, 3), "ex:ST_Page_Ch05")
K_REPAIR = ("Repair", "Repair of the chapter 1 to 4 decks and pages", "the released decks of chapters 1 to 4 opening in PowerPoint without repair, and their pages rebuilt on the current page template", "Obj_PagesBuilt", "Page", (13, 20, 8, 5), "ex:ST_Page_Ch05")
OUTCOME_BANK = "Settled: 73 written items cover all 46 concepts of chapter 5; the question builder offers them and asks for them first when it asks one question for every concept."
OUTCOME_LIVE = "Settled: the builder has an Ask the live model button; a question is shown only when well formed and, if it carries code, when the code prints the marked answer."
OUTCOME_REPAIR = "Settled: the decks of chapters 1 to 4 are new versions without the misplaced paragraph properties; the pages of chapters 1 to 4 are rebuilt on the current template (9.10). Earlier versions of every file stay as published."
TOOL_BANK = "08-tooling/ch05-page/question_bank_check_v1_0_0.py under Python 3.14.4; 08-tooling/sen0414_page_test_v9_10_0.py in headless Chromium"
TOOL_LIVE = "08-tooling/sen0414_page_test_v9_10_0.py in headless Chromium, with a stand-in for the language model"
TOOL_REPAIR = "08-tooling/ch05-deck/ooxml_fix_v1_0_0.py and structure_check_v1_0_0.py, 08-tooling/ch02-deck/deck_check_v1_0_1.py under Python 3.14.4; 08-tooling/sen0414_page_test_v9_10_0.py in headless Chromium on all five pages"
CLOSE_BANK = "Closed on the bank's checker and the page's browser tests and refused fixture. The bank's items are outside the page ABox and the acceptance gates. Times read from the clock."
CLOSE_LIVE = "Closed on the page's browser tests with a stand-in for the model. No real model was run: headless Chromium here has no WebGPU. Times read from the clock."
CLOSE_REPAIR = "Closed on the decks' checks and the pages' browser tests. That PowerPoint opens the decks without repair is inferred from the schema order, not observed. Times read from the clock."
FINDINGS_R3 = '''
ex:Finding_Ch05DeckFaultInFourDecks a backlog:RetrospectiveFinding ;
    rdfs:label "The PowerPoint repair fault was in every released deck; the owner approved the repair"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Repair_Ch05, ex:ST_Review_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The fault found in the chapter 5 deck (a paragraph-properties element after a run) was also in the released decks of chapters 1 to 4 (20, 23, 25 and 7 paragraphs); their checks read values, not structure. The owner approved the repair on 2026-09-29 and asked that the pages be repaired with the decks." ;
    backlog:hasRemedy "New versions of the four decks made from the released ones by the same repair step, with the structure check finding none; run text and notes read back identical. Rebuilding the pages of chapters 1 to 4 on the current template also removed the Next-step button and the two-step selectors from them. The released files stay in the repository." .

ex:Finding_Ch05BrowserPythonDifferences a backlog:RetrospectiveFinding ;
    rdfs:label "The page's Python differed from a terminal in three ways that the bank's checks found"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Bank_Ch05, ex:ST_Repair_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "Re-running the bank's programs in the page (Pyodide) showed: (1) text written to the error stream, which logging's default handler and warnings use, was not shown; (2) the logging set-up of an earlier run stayed, so a program calling basicConfig printed nothing; (3) an item on a feature of Python 3.14 could not run in the page's older Python (the same fault as the earlier remote-attach example). Separately the chapter 3 page's own input-reading example ran forever under Step through because nobody types, and a reloaded conversation lost the layout of its answers." ;
    backlog:hasRemedy "Template 9.10.0: the page's Python shows the error stream with the output, starts every run with a clean logging set-up, does not offer a program that reads the keyboard in Step through, and gives reloaded answers their layout. The bank item was rewritten to name the function instead of running it, and one that runs in both was added. The bank's checker runs under 3.14 and cannot see a difference in the page's Python; the page test now re-runs every item there." .

ex:Finding_Ch05AboxOverwrite a backlog:RetrospectiveFinding ;
    rdfs:label "The page ABox builder would have overwritten the released chapter 3 and 4 ABoxes"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Repair_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The builder writes its file under a fixed name (version 1_0_0). Rebuilding the pages of chapters 3 and 4 rewrote the released files with different content (the steps widgets no longer exist), which the versioning rule forbids; it was seen in the change list before release." ;
    backlog:hasRemedy "The two files were restored from the repository; builder 1.1.8 takes the file's version from ABOX_VER and the rebuilt ABoxes of chapters 1 to 4 are new files (1.1.0). The ABox of chapter 5 is unchanged and still 1.0.0." .

ex:Finding_Ch05LiveModelUntested a backlog:RetrospectiveFinding ;
    rdfs:label "The live-model question was tested with a stand-in, not a model"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Live_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The page's language model runs in the browser and needs WebGPU, which headless Chromium here lacks, so no real model wrote a question. What is verified is the page's handling of the model's reply." ;
    backlog:hasRemedy "Not remedied here. The owner can try the button in a browser with WebGPU (Agents, then the live model switch) and judge the questions; the reply is refused when malformed or when its code does not print its marked answer. A question without code is not checked by running anything and is labelled so." .
'''

FINDINGS_CH6 = '''
ex:Finding_Ch06NewVisualKinds a backlog:RetrospectiveFinding ;
    rdfs:label "The chapter 6 deck needed thirteen visual kinds the page did not have"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Deck_Ch06, ex:ST_Page_Ch06 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "Lists are taught with pictures no earlier chapter needed (indexes on boxes, slices, before-and-after lanes, two names reaching one object, a sort key row, a loop that changes the list it walks, the Matrix frames, a histogram). The deck draws each from an executed specification; the page template knew only the kinds of chapters 1 to 5, so the first page build of chapter 6 stopped at the first new one." ;
    backlog:hasRemedy "Template 9.11.0 (08-tooling/course_page_template_v9_11_0.html, made from 9.10.0 by template_patch_v9_11_0.py) draws all thirteen kinds from the same specifications, each with the interaction its spec supports, and the page test checks each drawn value against the spec (a changed histogram count and a changed lane item were both refused). The record builder 2.5.0 knows the new kinds. The deck-only framing slide is not drawn on the page." .

ex:Finding_Ch06TemplateDefects a backlog:RetrospectiveFinding ;
    rdfs:label "Building chapter 6 on template 9.10.0 showed four defects that chapters 1 to 5 had not exposed"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch06 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "(1) A visual attached to a sub-subject was never offered, because only subjects and concepts asked for one; seven of chapter 6's are on sub-subjects. (2) The range and pairs diagrams had no zoom bar, against the rule that every diagram has one. (3) The agents of chapter 6 all showed the robot icon, as their roles had no icon. (4) The page's own check that the Ordering agent answers 'what is sort method?' failed because its own section ranked tenth. The matrix blocks also failed the accessibility rule for scrollable regions." ;
    backlog:hasRemedy "Template 9.11.0: sub-subjects offer their visual, range and pairs are wrapped in the shared zoom bar, the roles have icons, an agent's own section whose label is in the question gets a small ranking boost (a page-wide change that also moved chapter 5's answer wording), and the matrix blocks are focusable. Chapter 5 was rebuilt on 9.11.0 and passes with two added checks. Chapters 1 to 4 stay on 9.10.0 and do not have these fixes." .

ex:Finding_Ch06ChapterVersusBook a backlog:RetrospectiveFinding ;
    rdfs:label "The book's printed error message for list.index does not appear under Python 3.14.4"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Research_Ch06 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The chapter prints ValueError: 'howdy howdy howdy' is not in list for a value missing from a list; Python 3.14.4 prints list.index(x): x not in list. Every other printed output checked reproduced exactly." ;
    backlog:hasRemedy "Recorded in the research record (finding F2, the index section and F8) and taught as the current message. Limits of the reading: the book's page was read through a fetch tool that returns a summary, not the raw page, so statements that the chapter does not present a topic, the Magic 8 Ball answer list and the indentation of the Matrix program's counter rest on that tool; the record makes no claim about the book's indentation and states only that the placement decides whether a stream ends." .

ex:Finding_Ch06QuizAndBankScope a backlog:RetrospectiveFinding ;
    rdfs:label "Chapter 6 was given a written question bank from the start"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch06 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner's review of chapter 5 asked that the quiz cover the scope and approved a written bank; chapter 6 has 58 concepts, so the rule of one written item per concept and two for each concept with an executed example gave 99 items, not the 70 first planned." ;
    backlog:hasRemedy "99 written items with 37 programs run under Python 3.14.4 and, in the bank's checker, under 3.11, 3.12 and 3.13 (111 runs) with the same output, then re-run in the page's own Python by the page test. In 28 of the 99 items the right option is the longest, which is not a gate and is reported." .
'''


K_RETURN = ("Return", "Written question banks for the chapter 1 to 4 pages, and those pages on template 9.11.0", "a written item for every concept of chapters 1 to 4, with the answers of its programs checked by running them, and the four pages rebuilt on the current template so that they carry the bank and the fixes made since 9.10", "Obj_PagesBuilt", "Page", (13, 20, 8, 5), "ex:ST_Page_Ch05")
OUTCOME_RETURN = "Settled: 61, 54, 69 and 74 written items cover all 33, 32, 37 and 41 concepts of chapters 1 to 4; the four pages are version 9.11.0 and offer them in the question builder."
TOOL_RETURN = "08-tooling/ch0N-page/question_bank_check_v1_0_0.py (N = 1 to 4) under Python 3.14.4; 08-tooling/sen0414_page_test_v9_11_1.py in headless Chromium on all four pages; 08-tooling/sen0414_rdodi_gates_v1_1_1.py"
CLOSE_RETURN = "Closed on the banks' checkers and the pages' browser tests and refused fixtures. The banks' items are outside the page ABoxes and the acceptance gates. The Lecture and Resources tabs are still missing from the pages of chapters 1 to 4. Times read from the clock."
FINDINGS_R4 = '''
ex:Finding_Ret14TestErrorText a backlog:RetrospectiveFinding ;
    rdfs:label "The page test refused a correct bank answer once the error stream was shown with the output"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Return_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "Since template 9.10.0 the page's Python prints an uncaught error's whole text (for example TypeError followed by a message) with the output. The test compared that text with the marked answer, the class name alone, so the chapter 4 item on a positional-only parameter was reported as a mismatch although the answer was right." ;
    backlog:hasRemedy "sen0414_page_test_v9_11_1.py accepts an answer that is the error class the printed text starts with. All four pages then passed. The chapter 5 and 6 pages were not re-tested with it; their banks have no such item that failed." .

ex:Finding_Ret14GatesFileNames a backlog:RetrospectiveFinding ;
    rdfs:label "The Stage 4 gate script looked for the chapter 1 files under a version they do not have"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Return_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The script built every RDODI file name with version 1_0_0; chapter 1's files are 1_0_1, so its run stopped with a missing file, which no earlier run had shown because chapter 1 had not been checked with it." ;
    backlog:hasRemedy "sen0414_rdodi_gates_v1_1_1.py takes the newest file of each part. All four chapters then give the same verdicts as chapters 3 to 6: coverage and substance fail, hybrid chains cannot be run; not claimed." .

ex:Finding_Ret14FixtureNeedsRunnableOutput a backlog:RetrospectiveFinding ;
    rdfs:label "The stale-result fixture was not refused on chapter 3 when it altered an example that reads the keyboard"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Return_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The fixture appends a character to the first stored output in the page. In chapter 3 that is the output of an example that calls input(); such an example is not re-run by the page's checks, so nothing was refused and the fixture could not show the checks work." ;
    backlog:hasRemedy "For chapter 3 every stored output was altered instead; the page then refused the same three features and one more (the evaluation steps). A better fixture would choose the first output of an example that is re-run; left for a later version." .

ex:Finding_Ret14BankScope a backlog:RetrospectiveFinding ;
    rdfs:label "The banks of chapters 1 to 4 are written and checked, not reviewed by the owner or in a class"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Return_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The 258 items were written by model agents from the chapters' research records and checked by running their programs (in the page's Python too) and by a check of coverage, distinct options and answer positions; in 28, 16, 30 and 29 items the right option is the longest, reported, not a gate. Their wording and difficulty have not been judged by the owner or by students." ;
    backlog:hasRemedy "Not remedied here. The owner can read the banks (08-tooling/ch0N-page/question_bank_v1_0_0.json) and mark items to change. The items are outside the page ABoxes and the acceptance gates, as for chapters 5 and 6; the Lecture and Resources tabs of these four pages remain a proposal." .
'''


K_ENRICH = ("Enrich", "Clickable references, a page-wide search and grounded replies on the pages of chapters 1 to 6", "the references in an agent's answer opening their source passages, a search over the whole page, and the local language model unable to put unsupported sentences into an answer", "Obj_PagesBuilt", "Page", (13, 20, 8, 5), "ex:ST_Page_Ch05")
OUTCOME_ENRICH = "Settled: template 9.12.0 - every reference in an answer opens its passage in the detail card; a search button, the / key and Ctrl+K search concepts, definitions, code and, on request, the book, course and research passages; the local model's unsupported sentences are removed. All six pages are rebuilt on it."
TOOL_ENRICH = "08-tooling/template_patch_v9_12_0.py; 08-tooling/sen0414_page_test_v9_12_0.py in headless Chromium on all six pages; 08-tooling/sen0414_rdodi_gates_v1_1_1.py"
CLOSE_ENRICH = "Closed on the pages' browser tests and refused fixtures. The check on the model's reply compares words with the passages; it does not decide whether a sentence is true. The tag push is still refused. Times read from the clock."
FINDINGS_R5 = '''
ex:Finding_Enrich_DeadReferences a backlog:RetrospectiveFinding ;
    rdfs:label "The references in an agent's answer led nowhere"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Enrich_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner's review of the chapter 2 Structure agent: the numbers [1] to [6] in an answer and the source labels below it were plain text. Only a passage tied to a section of the page had a small Go button; a passage of the book, the course or the research record has no section, so it had nothing to go to. The pages had been tested for the presence of the sources, not for what happens when one is chosen." ;
    backlog:hasRemedy "Template 9.12.0: each [n] and each source chip is a button that opens the passage in the detail card - its kind, file, full text, the concepts it mentions as links, a link to its section when it has one, and a search for it - and marks the chip in the answer. The test clicks a chip and an inline reference on every page. The card overlays the right edge of the page, as for concepts, so a reference under it can be reached after closing it (Esc)." .

ex:Finding_Enrich_InventedAnswer a backlog:RetrospectiveFinding ;
    rdfs:label "The small local model invented an answer instead of using its passages"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Enrich_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "With the live model on (a 360-million-parameter model, run in the browser) the answer to how an if statement is constructed began with 'At the top of this page you would find a section labelled if statement': the model ignored the numbered passages it was given and described the page. Small models follow the instruction to answer only from the context unreliably; the page passed every sentence on to the reader." ;
    backlog:hasRemedy "The reply is checked against the passages: a sentence whose content words are not found in them is removed, a reply left with nothing is replaced by the passages' own sentences, and the answer says so. The check compares words, not meaning: a sentence made of the passages' words that says something false would pass, and the test used a stand-in for the model, not a real one. A question about how something is written now also shows the concept's worked example, or its written form when it has no executed example." .

ex:Finding_Enrich_NoSearch a backlog:RetrospectiveFinding ;
    rdfs:label "The pages had no search"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Enrich_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "Every page offers navigation by explorer, tabs and agents, but none looked things up by a word; the owner noticed it was missing on all of them. Nothing in the specification of the page template listed search, and the acceptance gates do not ask for it." ;
    backlog:hasRemedy "A Search button in the title bar, the / key and Ctrl+K open a search over concepts (name, definition, code) that answers at once, and, on request, over the book, course and research passages; Enter goes to the first result; Esc closes it. Not searched: the lecture slides and the resource lists." .

ex:Finding_Enrich_ThinContent a backlog:RetrospectiveFinding ;
    rdfs:label "Some how-to-write questions cannot be answered well from the corpus"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Enrich_Ch05, ex:ST_Research_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "For an if statement the chapter ontology holds a definition and the line if name == 'Alice': and the book ontology holds one sentence; nothing says that the block is indented, that a colon ends the line, or how elif and else attach. A retrieval answer can only be as complete as its passages." ;
    backlog:hasRemedy "Not remedied here. A syntax fact for each construct (its form, an indented block, the parts it may have) would be added to the chapter records and ontologies and the pages rebuilt; proposed with the other enrichments (L-116), awaiting the owner." .
'''

PROPOSALS_ENRICH = "Proposed for the owner (L-116), ranked by expected benefit and cost, from research on retrieval practice and spaced repetition, on citation in answers grounded in sources, and on interactive programming books such as Runestone: (1) progress: mark a section understood, show what has been visited, resume where the reader left off; (2) a review queue that brings back wrongly answered questions after a delay; (3) code exercises with a check - fix the bug, fill the blank, and Parsons problems (put lines in order); (4) a link for every section and a working back button; (5) a copy button on every code block; (6) the reader's own notes and highlights, kept in the browser and exportable; (7) a print style and a one-page cheat sheet per chapter; (8) a way to mark an agent's answer as wrong or unhelpful and export those marks to the instructor; (9) the syntax facts the corpus lacks."

PROP_FINDING = '''
ex:Finding_Enrich_Proposals a backlog:RetrospectiveFinding ;
    rdfs:label "Common features of interactive course pages that these pages still lack"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Enrich_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner asked what other common, useful features are missing and for best practices. The template was checked: it has no link per section and no back button, no record of progress, no print style, no bookmarks or notes, and no way to mark an answer as unhelpful; it has text size, zoom, saved conversations and a question builder." ;
    backlog:hasRemedy "%s Not built; awaiting the owner's choice." .
'''


K_GROW = ("Grow", "Progress, review, links, notes, cheat sheet, marks and code exercises on the pages of chapters 1 to 6", "the proposed features of the pages that could be built now, work-arounds for those that could not, and the rest parked with the reason", "Obj_PagesBuilt", "Page", (13, 20, 8, 5), "ex:ST_Page_Ch05")
OUTCOME_GROW = "Settled: template 9.13.0 carries progress, a review queue, links and a back button, copy buttons, notes, a print style and cheat sheet, marks on answers and generated code exercises; chapters 1 to 4 have resource lists and chapter 3 a Lecture tab. All six pages are rebuilt on it."
TOOL_GROW = "08-tooling/template_patch_v9_13_0.py; 08-tooling/sen0414_page_test_v9_13_0.py in headless Chromium on all six pages; 08-tooling/ch03-page/lecture_from_notes_v1_0_0.py; the resource lists were written by model agents that opened every link"
CLOSE_GROW = "Closed on the pages' browser tests and refused fixtures. Marks, notes, progress and the review queue stay in the reader's browser and are copied out by the reader; nothing is sent. Times read from the clock."
FINDINGS_R6 = '''
ex:Finding_Grow_Parked a backlog:RetrospectiveFinding ;
    rdfs:label "Proposals and open items parked, with the reason for each"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Grow_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner asked to build the proposals that were ready and to find work-arounds or park the rest. Parked: (1) fix-the-bug exercises written by hand, and the syntax facts of each construct - both are authored content in the chapter records, which the RDODI runs own, and the pages would be rebuilt after; (2) the Lecture tabs of chapters 1, 2 and 4 - the speaker notes of those decks are source citations, not a talk track, so a lecture would have to be written and the decks reissued; (3) highlights inside text - notes were built instead; (4) the live model tried with a real model - this environment has no WebGPU; (5) the release tags - the credential is refused with 403; (6) the attestation of the pages - the owner's; (7) opening the repaired decks in PowerPoint - not observable here; (8) the Stage 4 coverage, substance and hybrid-chain gates - they fail identically on every chapter and lie in shared tooling, a ruling for the owner." ;
    backlog:hasRemedy "Not remedied here. Work-arounds built instead: exercises are generated from the executed examples of the chapter and from the bank's programs that raise an error, checked by running them; a chapter 3 lecture was read back from its deck's notes; marks and notes are copied out by the reader because the page has no server." .

ex:Finding_Grow_Limits a backlog:RetrospectiveFinding ;
    rdfs:label "What the new features do not do"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Grow_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "Progress, notes, the review queue and marks live in the reader's browser only: a different browser or a cleared profile starts empty, and the instructor sees nothing unless the reader copies the marks out. The 'make it run' exercise is offered only where a chapter has a program that raises an error (5, 0, 2, 4, 2 and 1 in chapters 1 to 6; chapter 2 has none) and accepts any change after which no error is raised. A fill-in-the-blank is made from a token whose blanking makes the program fail, so a blank inside an expression that is never evaluated is not chosen. The chapter 3 lecture drops the sentences that address a lecturer, so a paragraph can begin part-way through a sequence. The resource lists of chapters 1 to 4 were written by model agents that opened every page; the section anchors of chapter 3's links were not tested and, if wrong, open the right page at its top." ;
    backlog:hasRemedy "Stated to the owner. Possible next steps: a shared store for marks (needs a service), authored exercises, and a talk track for the decks of chapters 1, 2 and 4." .

ex:Finding_Grow_TestFindings a backlog:RetrospectiveFinding ;
    rdfs:label "Three defects the new tests found before release"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Grow_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "(1) The exercises' output area had the same element name as the Expert questions view, so both answered to it; (2) copy buttons placed beside the example programs of a concept section broke the rule that a section carries no button beyond its example's own; (3) a fill-in-the-blank on a token in an expression that is never evaluated (False in True or False) accepted anything." ;
    backlog:hasRemedy "Names made distinct; copy buttons kept to code blocks outside the concept sections' examples and the Playground; the blank is chosen only from tokens whose removal makes the program fail, checked by running it. The pages of chapter 5 and 6 were tested with the same test file." .
'''

K_ASSESS = ("Assess", "Ten question types with corrections, mock midterm and final exams, and the live-model choice on the pages of chapters 1 to 6", "the question types the pages can mark by rule, exams built from them on the fly, and the better in-browser model the RDODI experiments kept", "Obj_PagesBuilt", "Page", (13, 20, 8, 5), "ex:ST_Page_Ch05")
OUTCOME_ASSESS = "Settled: template 9.14.0 marks ten question types and answers each with a correction, builds a midterm-style and a final-style exam from a code, and chooses the coder model of the RDODI experiments where the device's memory allows. All six pages are rebuilt on it."
TOOL_ASSESS = "08-tooling/template_patch_v9_14_0.py; 08-tooling/sen0414_page_test_v9_14_0.py in headless Chromium on all six pages; the WebLLM 0.2.85 package's own model list (npm) for the model names and their memory needs"
CLOSE_ASSESS = "Closed on the pages' browser tests and refused fixtures. The live model itself was not run: this environment has no WebGPU, so only the choice of model and the handling of its reply (tested with a stand-in) are verified. Exam results stay in the reader's browser. Times read from the clock."
FINDINGS_R7 = '''
ex:Finding_Assess_Dispositions a backlog:RetrospectiveFinding ;
    rdfs:label "What was asked on 2026-09-30 at 14:21, item by item, and what became of each"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Assess_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "Five things were asked. (1) A better in-browser model, following the RDODI experiments: built as far as it can be checked - the coder model those experiments kept is the default where the device's memory allows, the small one otherwise, chosen by a box; the names and memory needs were read from the WebLLM 0.2.85 package; the model was not run here (no WebGPU). (2) Other question types the page can process: built, ten in all. (3) Fill in the blank and testing with feedback for corrections, for code: built - typed blanks in definitions, blanks in code marked by running the program, output prediction, write the code, make it run, each answered with the right result and an explanation. (4) The same for narrative work: built as the short answer, marked against the key ideas of a model answer, with a comment by the live model on request; it cannot judge reasoning, and the page says so. (5) Midterm and final level exams built on the fly for a chapter: built, with an exam code that gives the same exam again." ;
    backlog:hasRemedy "Nothing left unbuilt from this request. Stated limits are in the next finding." .

ex:Finding_Assess_Limits a backlog:RetrospectiveFinding ;
    rdfs:label "What the question types and exams do not do"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Assess_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The point values (1 to 3 per question), the sizes (14 and 19 questions), the times (40 and 75 minutes), the levels asked in each exam and the rule that a repaired program must keep 70% of its lines are stipulations of this build, chosen because no rule of the course fixes them; they are shown on the page as practice defaults and are the owner's to rule on. The short answer is a match against five key words of the model answer: a wrong answer that uses the right words can pass and a right answer in other words can fail. A 'write the code' question needs the construct named in the question and refuses an answer that contains the result itself. A 'make it run' question accepts any change that stops the error while most of the program stays. Put the lines in order gives credit for lines already in place, so an exam left untouched scores about 1 to 3%. Chapters 1 to 6 differ in what they can carry: chapter 2 has no program that raises an error and chapter 5 has hardly a number to change. Exam attempts are kept in the reader's browser only; the lecturer sees nothing. The questions are generated for practice and are not the lecturer's own exam." ;
    backlog:hasRemedy "Stated to the owner. Possible next steps: the owner's rulings on the stipulations, authored exam questions in the chapter records, and a shared store for attempts (needs a service)." .

ex:Finding_Assess_TestFindings a backlog:RetrospectiveFinding ;
    rdfs:label "Two defects that reached the built pages before this work, and how they were found"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Assess_Ch05 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "(1) Since 9.9.0 the heading of the question builder showed the text U0001F9E9 in place of its emoji: a Python-style escape sat inside a JavaScript string. No test looked at the heading, so this is a real gap in the tests, not a safeguard working; found by reading the built page while writing the new views, and now tested. (2) The 9.13.0 'make it run' exercise accepted an empty program, and a program with its lines deleted, as solved. The 9.13.0 tests only tried a working fix and a wrong one, so this too was a gap; found when the exam's marking of the same kind of question was written, and fixed in both places." ;
    backlog:hasRemedy "Both fixed in 9.14.0 and covered by tests." .
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
ex:Iter_4 a backlog:Iteration ; rdfs:label "Fourth iteration: chapters 5 and 6 and the page template feedback, before the class of 2 October"@en ;
    backlog:hasIdentifier "Iter_4" ; backlog:belongsToLineage ex:Lineage ;
    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-10-02T11:00:00"^^xsd:dateTime ;
    backlog:hasDurationSource "Owner, 2026-09-29 (10:00 Istanbul): build the next chapter of SEN0414 with the enhancements he named. The owner gave no date, so the period runs to SEN0414's next class, 14:00 Istanbul on Friday 2026-10-02, as the second and third iterations do - taken from the course timetable, not chosen for the work." ;
    backlog:hasSprintGoal "Chapters 5 and 6 researched, their decks built as lectures and their pages built on the revised template, ready to present; the decks and pages of chapters 1 to 4 repaired." ;
    backlog:hasMember %s .
'''
SESSION4 = '''
ex:Session_Iter4 a backlog:RegisterSession ; rdfs:label "The session that built chapter 5 with the owner's enhancements, in the fourth iteration"@en ;
    backlog:sessionFor ex:Backlog ; backlog:sessionConductedBy "claude-code-course-materials-session" ;
    backlog:sessionStartedAt "%s"^^xsd:dateTime ; backlog:sessionEndedAt "%s"^^xsd:dateTime ;
    backlog:stateVerifiedAtStart true ;
    backlog:hasSessionScopeNote "Ran the discipline ceremony first from the files on GitHub (governance at Ontologies 087b9c2, knowledge base 2.32.0, OE discipline 2.12.1, lineage discipline 70.0.0), and re-read both discipline files at the release from governance 432507d, where they were byte-identical to the ceremony's (sha ee2052c9 and 7860dc89), then planned chapter 5 and the page-template feedback into the fourth iteration on the owner's request, built chapter 5's research record, lecture deck and page, and revised the page template as the owner asked; wrote version 1.1 of the teaching-device proposal; then, on the owner's review, repaired the deck (1.0.1) and the page (9.8.0); then, on his second review, page 9.9.0; then, on his approval of three proposals, a written question bank, a live-model question and the repair of the decks and pages of chapters 1 to 4." ;
    backlog:changedItem ex:ST_Research_Ch05, ex:ST_Deck_Ch05, ex:ST_Page_Ch05, ex:ST_Template_Ch05, ex:ST_Review_Ch05, ex:ST_Review2_Ch05, ex:ST_Bank_Ch05, ex:ST_Live_Ch05, ex:ST_Repair_Ch05, ex:ST_Return_Ch05, ex:ST_Enrich_Ch05, ex:ST_Grow_Ch05, ex:ST_Assess_Ch05 .
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
    members = chapter_members + ["ex:ST_Template_Ch05"] + (["ex:ST_Review_Ch05"] if "Review" in IT["done"] else []) + (["ex:ST_Review2_Ch05"] if "Review2" in IT["done"] else []) + ["ex:ST_%s_Ch05" % k for k in ("Bank", "Live", "Repair", "Return", "Enrich", "Grow", "Assess") if k in IT["done"]]
    t = template_story() + FINDINGS4
    if "Review" in IT["done"]:
        t += template_story(K_REVIEW, OUTCOME_REVIEW, TOOL_REVIEW, CLOSE_REVIEW) + FINDINGS_REVIEW
    if "Review2" in IT["done"]:
        t += template_story(K_REVIEW2, OUTCOME_REVIEW2, TOOL_REVIEW2, CLOSE_REVIEW2) + FINDINGS_REVIEW2
    for K, O, T, C in ((K_BANK, OUTCOME_BANK, TOOL_BANK, CLOSE_BANK), (K_LIVE, OUTCOME_LIVE, TOOL_LIVE, CLOSE_LIVE), (K_REPAIR, OUTCOME_REPAIR, TOOL_REPAIR, CLOSE_REPAIR), (K_RETURN, OUTCOME_RETURN, TOOL_RETURN, CLOSE_RETURN), (K_ENRICH, OUTCOME_ENRICH, TOOL_ENRICH, CLOSE_ENRICH), (K_GROW, OUTCOME_GROW, TOOL_GROW, CLOSE_GROW), (K_ASSESS, OUTCOME_ASSESS, TOOL_ASSESS, CLOSE_ASSESS)):
        if K[0] in IT["done"]:
            t += template_story(K, O, T, C)
    if "Repair" in IT["done"]:
        t += FINDINGS_R3
    if any(k in _P.get("done", {}) for k in ("Research_6", "Deck_6", "Page_6")):
        t += FINDINGS_CH6
    if "Return" in IT["done"]:
        t += FINDINGS_R4
    if "Enrich" in IT["done"]:
        t += FINDINGS_R5 + PROP_FINDING % PROPOSALS_ENRICH
    if "Grow" in IT["done"]:
        t += FINDINGS_R6
    if "Assess" in IT["done"]:
        t += FINDINGS_R7
    t += ITER4 % (PLANNED_AT_4, ", ".join(members))
    t += SESSION4 % (PLANNED_AT_4, end_time)
    return t
