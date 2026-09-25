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
# Started items, at the clock time each began. The kick-off was declared by the owner.
STARTED = {("Research", 1): "2026-09-24T20:26:42", ("Deck", 1): "2026-09-24T20:55:01", ("Research", 2): "2026-09-24T21:17:28", ("Page", 1): "2026-09-24T21:26:47", ("Page", 2): "2026-09-25T00:16:20", ("Deck", 2): "2026-09-25T00:20:02"}
# Re-scoring after the latest completion (BP-D11), at the clock time it was done; components unchanged.
RESCORED_AT = "2026-09-25T06:13:08"

# Finished items and the evidence each closed on. Times from the clock or from commits only.
DONE = {("Research", 1): {"finished": "2026-09-24T20:47:21", "closed": "2026-09-24T20:50:04", "release": "sen0414-v2.7.0 (e49e8f6)",
    "spec": "RDODI procedure v1.6.0, Stages 1-3 for chapter 1, gates run with RDODI's own validator functions where it has them: Stage1.A-B, Stage2.A and C, Stage3.A, B, E.cov, E.sub, F and src, all PASS; Stage1.C-E, Stage2.B (HermiT, consistent), D-H and Stage3.C, D, E (coverage 27/27), G and H run as direct checks because the validator does not implement them - all PASS."}, ("Deck", 1): {"finished": "2026-09-24T21:00:46", "closed": "2026-09-24T21:01:30", "release": "the release carrying 03-materials/ch01/SEN0414_Ch01_PythonBasics_3e.pptx",
    "spec": "08-tooling/ch01-deck/deck_check.py re-ran all 19 examples shown on the renewed deck under Python 3.14.4, one shell session per slide: 0 mismatches. The fixture fixture_stale.pptx - the same deck with 0.1 + 0.2 shown as 0.3 - was refused, naming slide 10. Slides built by deck.js, which takes every output from examples_out.json, produced by executing the examples rather than typing them. Rendered and inspected; four layout faults fixed before closing. The course still conforms to every CME shape with the new materials described."},
    ("Research", 2): {"finished": "2026-09-24T21:22:23", "closed": "2026-09-24T21:22:40", "release": "sen0414-v2.9.0 (b4b107b)",
    "spec": "RDODI procedure v1.6.0, Stages 1-3 for chapter 2, built by the generic builder 08-tooling/sen0414_rdodi_build_v1_0_0.py from 08-tooling/sen0414_ch02_rdodi_data_v1_0_0.py, all gates PASS on the first run: Stage1.A-B, Stage2.A, C and H, Stage3.A, B, F, E.cov, E.sub and src with RDODI's own validator functions; Stage1.C-E, Stage2.B (HermiT consistent), D-G and Stage3.C-E (coverage 22/25 = 0.88), G and H as direct checks."},
    ("Deck", 2): {"finished": "2026-09-25T00:21:53", "closed": "2026-09-25T00:22:07", "release": "the release carrying 03-materials/ch02/SEN0414_Ch02_FlowControl_3e.pptx",
    "spec": "08-tooling/ch02-deck/deck_check.py re-ran all 17 expressions on the deck under Python 3.14.4, and program_check.py re-ran both whole programs with the six inputs the slides show: 0 mismatches. Two fixtures refused, each naming what it broke: an expression result edited on slide 6, and a program transcript edited on slide 10. Building the second fixture exposed a weakness in the new program check - a result's words also occur in the program's own code on the slide - fixed by requiring the whole transcript sequence."},
    ("Page", 1): {"finished": "2026-09-25T06:12:58", "closed": "2026-09-25T06:13:08", "release": "the release carrying the chapter 1 page",
    "spec": "08-tooling/sen0414_page_test_v2_0_0.py exercised every widget and feature of the chapter 1 page in headless Chromium at 2026-09-25T06:12:58 - every widget passed, every executable example printed via Pyodide exactly what the build interpreter printed, 0 console errors, 0 WCAG 2 AA violations - and a fixture with one stored value altered was refused. RDODI Stage 4 and every automated pedagogy gate pass. The Courseware profile's pedagogical-soundness attestation is the owner's, is not part of this story's definition of done, and is recorded as pending, not claimed."},
    ("Page", 2): {"finished": "2026-09-25T06:12:58", "closed": "2026-09-25T06:13:08", "release": "the release carrying the chapter 2 page",
    "spec": "08-tooling/sen0414_page_test_v2_0_0.py exercised every widget and feature of the chapter 2 page in headless Chromium at 2026-09-25T06:12:58 - every widget passed, every executable example printed via Pyodide exactly what the build interpreter printed, 0 console errors, 0 WCAG 2 AA violations - and a fixture with one stored value altered was refused. RDODI Stage 4 and every automated pedagogy gate pass. The Courseware profile's pedagogical-soundness attestation is the owner's, is not part of this story's definition of done, and is recorded as pending, not claimed."}}

REFINED = {
    "Research": "Settled: RDODI's four-stage procedure v1.6.0 on the chapter's subject, with its Pedagogy and Professional Standards stage and the Courseware profile; the research record lists every source a later claim rests on.",
    "Deck": "Settled: rewritten from the 3rd edition's chapter and the research record, restyled with PowerPoint's own capabilities, every code example run under current Python before it is shown, and the deck described as a teaching material aligned to the outcomes it serves.",
    "Page": "Settled: one interactive page for the chapter, carrying the research results; published as a page students can open, and described as a teaching material.",
}

OBJ = {"Deck": "Obj_DecksRenewed", "Research": "Obj_ResearchRecorded", "Page": "Obj_PagesBuilt"}


def planned_tail(k, n):
    if n not in PLANNED:
        return 'backlog:hasState backlog:Proposed ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned."'
    if (k, n) in DONE:
        d = DONE[(k, n)]
        state = ('Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ;\n'
                 '    backlog:hasEvidence ex:Ev_%s_%s ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (STARTED[(k, n)], d["finished"], d["closed"], k, cid(n)))
    else:
        state = ('InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % STARTED[(k, n)]) if (k, n) in STARTED else 'Ready'
    return ('backlog:hasState backlog:' + state + ' ; backlog:memberOfContainer ex:Iter_1 ;\n    backlog:hasPriorityScore ex:Score_%s_%s ;\n'
            '    backlog:decomposesInto ex:TK_%s_%s_Build, ex:TK_%s_%s_Verify' % (k, cid(n), k, cid(n), k, cid(n)))


def start_block(k, n):
    if (k, n) not in STARTED or (k, n) == ("Research", 1): return ""  # chapter 1's research started at the kick-off, recorded there
    return '''
ex:Start_%s_%s a backlog:TransitionEvent ; rdfs:label "%s %s started"@en ; backlog:transitionedItem ex:ST_%s_%s ;
    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "%s" .
''' % (k, cid(n), k, cid(n), k, cid(n), STARTED[(k, n)], (
        "Started once its dependency, the chapter's research, was Done. Time read from the clock." if (k, n) != ("Page", 1) else
        "The start was not recorded when the work began. This is its provable lower bound: the commit time of sen0414-v2.9.1, the last release before any page work - bounded, not composed."))


REFINE2_TAIL = """
    backlog:refines ex:ST_Page_%(c)s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%(cl)s"^^xsd:dateTime ;
    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:Iter_1 ;
    backlog:hasRefinementOutcome "RDODI's Pedagogy and Professional Standards stage runs its gates over an interactive page's ABox and HTML (its README: --page, --html), so it belongs to the page story, not the research story where the first refinement put it." """


def closure_block(k, n):
    if (k, n) not in DONE: return ""
    d = DONE[(k, n)]; c = cid(n)
    return '''
ex:Ev_%(k)s_%(c)s a backlog:TestEvidence ; rdfs:label "Checks for %(k)s %(c)s"@en ; backlog:belongsToLineage ex:Lineage ;
    backlog:attestsCriterion ex:AC_Chapter ; backlog:evidenceVerified true ; backlog:hasTestId "%(k)s/%(c)s" ;
    backlog:hasTestSpec "%(spec)s" ; backlog:hasVerificationMethod "Gates run over the artefacts as published in %(rel)s." ;
    backlog:verifiedByTool "%(tool)s" ; backlog:verifiedAt "%(fin)s"^^xsd:dateTime .
ex:Harness_%(k)s_%(c)s a backlog:TestHarness ; rdfs:label "Checks for %(k)s %(c)s"@en ;
    backlog:harnessFor ex:ST_%(k)s_%(c)s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:Ev_%(k)s_%(c)s .
ex:Obs1_%(k)s_%(c)s a backlog:MetricObservation ; rdfs:label "%(k)s count read after %(c)s closed"@en ;
    backlog:observesMetric ex:%(met)s ; backlog:observationFor ex:%(obj)s ;
    backlog:hasObservedValue "%(count)d"^^xsd:decimal ; backlog:observedAt "%(cl)s"^^xsd:dateTime ;
    backlog:hasObservationMethod "%(obsnote)s" .
ex:Complete_%(k)s_%(c)s a backlog:TransitionEvent ; rdfs:label "%(k)s %(c)s completed"@en ;
    backlog:transitionedItem ex:ST_%(k)s_%(c)s ; backlog:viaTransition backlog:T_Complete ;
    backlog:transitionedAt "%(cl)s"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "%(tnote)s" .
%(extra)s
''' % dict(k=k, c=c, spec=d["spec"], rel=d["release"], fin=d["finished"], cl=d["closed"],
                met={"Research": "Met_ResearchRecorded", "Deck": "Met_DecksRenewed", "Page": "Met_PagesBuilt"}[k], obj=OBJ[k],
                obsnote=("Counted chapters whose Stages 1-3 artefacts are published and pass their gates: %s." % ", ".join("chapter %d" % m for (kk, m) in DONE if kk == "Research" and m <= n) if k == "Research" else ("Counted renewed decks passing the chapter check: %s." % ", ".join("chapter %d" % m for (kk, m) in DONE if kk == "Deck" and m <= n)) if k == "Deck" else ("Counted interactive pages passing their browser tests and Stage 4 gates: %s." % ", ".join("chapter %d" % m for (kk, m) in DONE if kk == "Page" and m <= n))),
                count=len([1 for (kk, m) in DONE if kk == k and m <= n]),
                tool=("rdodi-ecosystem/02-gates/rdodi_pipeline_validator_v1_6_0.py, pyshacl, owlready2 HermiT" if k == "Research" else ("08-tooling/ch%02d-deck/deck_check.py under Python 3.14.4" % n) if k == "Deck" else "08-tooling/sen0414_page_test_v2_0_0.py in headless Chromium, RDODI Stage 4 and pedagogy gates"),
                tnote=("Closed on Stages 1-3 of the RDODI procedure. The pedagogy stage, which this story's refinement placed here, runs over a page artefact - its gates take the page's ABox and HTML - so it moves to the chapter's page story; recorded in Refine2_Research_%s rather than claimed here." % c) if k == "Research" else ("Closed on the deck check and its refused fixture. Times read from the clock." if k == "Deck" else "Closed on the page's browser tests, its refused fixture and its Stage 4 gates. The Courseware attestation, the owner's, is pending and not claimed. Times read from the clock."),
                extra=(("ex:Obs1_Untaught_%s a backlog:MetricObservation ; rdfs:label \"No renewal item for an untaught chapter, read after the %s deck closed\"@en ; backlog:observesMetric ex:Met_UntaughtWork ; backlog:observationFor ex:Obj_NoUntaughtWork ; backlog:hasObservedValue \"0\"^^xsd:decimal ; backlog:observedAt \"%s\"^^xsd:dateTime ; backlog:hasObservationMethod \"Counted renewal items for chapters outside the scope - command-line programs, untaught chapters, the GUI decks: none.\" ." % (c, c, d["closed"])) if k == "Deck" else "") + ((("ex:Refine2_Research_%s a backlog:RefinementEvent ; rdfs:label \"Pedagogy stage moved to the page story\"@en ;" % c) + REFINE2_TAIL.replace("%(c)s", c).replace("%(cl)s", d["closed"]) + " .") if k == "Research" else ""))


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
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:%(tstate)s ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Build ; backlog:effectiveDefinitionOfDone ex:DoD ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story's score; scoring both would double-count." ;%(dep)s
    backlog:hasAuditNote "Build it." .
ex:TK_%(k)s_%(c)s_Verify a backlog:ExecutionTask ; rdfs:label "%(k)s for %(c)s: verify"@en ; backlog:hasIdentifier "TK_%(k)s_%(c)s_Verify" ; backlog:hasTitle "Verify %(k)s %(c)s" ;
    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:%(tstate)s ;
    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Verify ; backlog:effectiveDefinitionOfDone ex:DoD ;
    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story's score; scoring both would double-count." ;%(dep)s
    backlog:hasAuditNote "Run the chapter check and require the stale fixture refused." .
''' % dict(k=k, c=c, bv=bv, tc=tc, rr=rr, js=js, v=(bv + tc + rr) / js, t=(RESCORED_AT if (RESCORED_AT and (k, n) not in DONE) else PLANNED_AT), o=REFINED[k],
          tstate=(('Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence ex:Ev_%s_%s' % (STARTED[(k, n)], DONE[(k, n)]["finished"], k, c)) if (k, n) in DONE else 'Proposed'),
          dep=("" if k == "Research" else "\n    backlog:dependsOn ex:ST_Research_%s ;" % c))


ITER = '''
ex:Iter_1 a backlog:Iteration ; rdfs:label "First iteration: chapters 1 and 2, before the class of 25 September"@en ;
    backlog:hasIdentifier "Iter_1" ; backlog:belongsToLineage ex:Lineage ;
    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-09-25T11:00:00"^^xsd:dateTime ;
    backlog:hasDurationSource "Owner, 2026-09-24: chapter 1, and chapter 2 added at approval, ready for SEN0414's class at 14:00 Istanbul on 2026-09-25." ;
    backlog:hasSprintGoal "Chapters 1 and 2 researched, their decks renewed and their interactive pages built, ready to present." ;
    backlog:hasMember %s .
'''


FEEDBACK = """
ex:Finding_PageFreeze a backlog:RetrospectiveFinding ;
    rdfs:label "The chapter pages froze the browser: heavy work ran on the page's own thread"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch01, ex:ST_Page_Ch02 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner reported the page freezing and the computer becoming unresponsive. Measured in Chromium before any change, on the version 4.0.1 page: the first agent question blocked the page's thread for 19.0 s in a single task - the 250 passages were embedded on that thread - Python's first run for 0.7 s and a 3-million-step program for 1.1 s, and an endless program would have blocked it for ever, with no way to stop it. The language model also loaded and generated on the page's thread; on a machine whose GPU also drives the display, WebGPU work of that size can starve the whole desktop, which fits a computer - not only a tab - going unresponsive, though that part could not be reproduced here without a GPU." ;
    backlog:hasRemedy "Version 5 moves each kind of heavy work to its own Web Worker and leaves the page's thread only to send messages: Python runs as CPython (Pyodide) in a worker, and a program still running after 15 s is stopped by ending that worker, after which a fresh one starts; Oxigraph, the corpus, the embedding model and all ranking run in a second worker; the language model loads and generates in a third, through WebLLM's own worker engine. All three are classic workers, because a module worker built from a blob failed to start on a page opened as a file while a classic one could still load its library - both measured. Where workers are not allowed, the page falls back to its previous in-page behaviour. Measured after the change, same machine, same four operations: 0 ms of main-thread blocking in each. At 2026-09-25T13:31:49 every check in 08-tooling/sen0414_page_test_v5_0_0.py passed on both pages - every version 4 check, no main-thread task over 200 ms through the whole session, and an endless loop stopped at 15 s while the menu kept answering, with Python working again afterwards; 0 console errors; a stale-value fixture refused on each. Python now reports CPython 3.13.2, so error messages match standard Python again." .

ex:Finding_WebLLMImportPath a backlog:RetrospectiveFinding ;
    rdfs:label "The live LLM failed to load for the owner: its import went through an unpinned redirect"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch01, ex:ST_Page_Ch02 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner reported the chapter 1 page's status line: knowledge graph and semantic search ready, live LLM failed - it could not fetch https://esm.run/@mlc-ai/web-llm. The page imported WebLLM through esm.run, as RDODI's template does; esm.run is not a host of its own but an unpinned redirect to cdn.jsdelivr.net. The graph and embedding libraries, loaded from cdn.jsdelivr.net directly, succeeded in the same browser, so the failure was the redirect host, not the network. Checked the same day: every embedded corpus file matches its declared hash, and every URL the page loads from - Brython, Oxigraph, transformers.js and its model, WebLLM and both model variants' weights and libraries - answered." ;
    backlog:hasRemedy "WebLLM is imported from cdn.jsdelivr.net/npm/@mlc-ai/web-llm@0.2.85/+esm, pinned, and the model variant is chosen from the GPU's features - the 16-bit build only where the adapter supports shader-f16, otherwise the 32-bit build - both listed in that version's own model table. Pages re-issued as v4.0.1; at 2026-09-25T12:06:20 every version 4 check passed again on both, with the import proven to resolve and expose the engine in a browser. Generation itself remains unverifiable here for want of a WebGPU adapter. RDODI's template imports the same way and should be told." .

ex:Finding_AgentsOnRdodiToolkit a backlog:RetrospectiveFinding ;
    rdfs:label "The chapter pages' agents moved onto RDODI's default toolkit"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch01, ex:ST_Page_Ch02 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "The owner required the agents to consume the page's HTML corpus and the book and course ontologies through an in-page LLM library or tools, pointing to RDODI's template for the right ones. Version 3's agents read only their slice of the page data. RDODI's own interactive template, lcw_kb_interactive v0.109.0, uses Oxigraph 0.5.9 for SPARQL, transformers.js with all-MiniLM-L6-v2 for embeddings, and WebLLM with SmolLM2-360M for generation." ;
    backlog:hasRemedy "Pages rebuilt as version 4 on that same toolkit, loaded the way the template loads it. Each page embeds, as Turtle with file names and hashes, the book's chapter ontology at the commit SEN0414's textbook part pins (automate-python-book-3e v0.20.0, 89f68596), the course ontology - profile, outcomes, textbook and materials - and the chapter's ontology, document and research record. On a question the agent loads them into Oxigraph, reads its own slice by SPARQL, ranks every passage from the book, course, chapter, research and the page's own text by meaning with its own slice favoured, and answers from the top passages with numbered citations and a 'how I found this' trace of the query and ranking. Generation uses WebLLM when the browser has WebGPU, Claude when the page is published on claude.ai, and the retrieved passages themselves otherwise. Off-topic questions are refused below a measured threshold: on this corpus off-topic questions scored 0.11 to 0.24 and on-topic ones 0.42 to 0.72, so 0.33. At 2026-09-25T11:31:42 every check in 08-tooling/sen0414_page_test_v4_0_0.py passed on both pages: all version 3 rules, every widget (33 and 32), a knowledge graph of 9 files (1,902 and 1,515 triples) with passages of all five kinds, semantic ranking with cited sources, a course question reaching the course's outcomes, and the WebGPU check; 0 console errors, 0 WCAG 2 AA violations; a stale-value fixture refused on each. Not verifiable here: WebLLM's own generation, because this sandbox's browser has no WebGPU adapter - the capability check and the fallback were verified, the same limit RDODI's template records." .

ex:Finding_PagesV3OwnerRules a backlog:RetrospectiveFinding ;
    rdfs:label "Chapter 1 and 2 pages rebuilt to the owner's page rules"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch01, ex:ST_Page_Ch02 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "Reviewing SEN0401's Bitcoin in numbers page, which shares this design, the owner found four faults and made them rules for every course page: code on the page must really run - in the published version, running had been replaced by stored results, so edits changed nothing; agents must answer from their own slice of the ontology and corpus - they had given near-identical answers; a menu click must change the main area first, with the detail card only on explicit request; and the tab row must be the sub-menu of the selected top-level item, not a second menu mixed with it. Version 2 of these pages broke the last three as well." ;
    backlog:hasRemedy "Pages rebuilt as version 3 from one course-neutral template, course_page_template_v3_0_0.html, with each course's text in data: Python runs in Brython, which loads as plain scripts and so also works when published; agents receive only their own concepts, relations, computed results and the research findings - asking Claude when published, retrieving and combining sentences when opened as a file; menu, concept, map and taxonomy clicks move the main area, and details open only from the heading's details button or the context menu; one top menu, with each subject's tabs as its sub-menu. Every rule is a browser check in 08-tooling/sen0414_page_test_v3_0_0.py - edited code must print the new result, different questions must get different answers, a menu click must leave the card closed - and at 2026-09-25T10:53:47 both pages passed all of them, every widget included (33 and 32), with 0 console errors and 0 WCAG 2 AA violations; a stale-value fixture was refused on each. Brython is not CPython: every example prints the same result, but error messages are worded differently, and the page says so." .

ex:Finding_ChapterAboxTestName a backlog:RetrospectiveFinding ;
    rdfs:label "The version 2 pages' ABoxes named the version 1 test script"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Page_Ch01, ex:ST_Page_Ch02 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRemedy "The ABox builder now names 08-tooling/sen0414_page_test_v2_0_0.py, the script that ran every version 2 test; both pages' ABoxes re-issued as v2.0.1 with nothing else changed, and the materials record points at them." ;
    backlog:hasRootCause "Found in SEN0401, whose tooling was forked from here: regression-checking it showed each widget's design test attributed to the version 1 page test script. The same was true here - SEN0414's version 2 pages were tested by sen0414_page_test_v2_0_0.py, but their ABoxes named sen0414_page_test_v1_0_0.py." .

ex:Refine3_Page_Ch01 a backlog:RefinementEvent ; rdfs:label "Chapter 1 page re-refined on the owner's review"@en ;
    backlog:refines ex:ST_Page_Ch01 ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "2026-09-24T22:05:38"^^xsd:dateTime ;
    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:Iter_1 ;
    backlog:hasRefinementOutcome "The owner reviewed page v1 and asked for, in his words: an iconised Explorer-style left menu with hierarchical expand and collapse; sub-tabs so the page needs less vertical scrolling; Pyodide embedded, as in RDODI's default interaction, to edit, fill, run and display code, with editable example code; an agent per subject of the chapter; a context-sensitive right-click menu; tooltips; diagrams of the code; the chapter taxonomy; an ontology of the concepts with their relationships; a concept card on the right opened by activating any concept; and connections between related subjects for navigation and jumps. Page v2 is built to that list. The agents are grounded retrieval over the chapter's own ontology and document, stated as such on the page - not language models - because a page in a student-readable repository has no model behind it and RDODI's default console is grounded the same way." .

ex:Finding_Ch01Stage1Metadata a backlog:RetrospectiveFinding ;
    rdfs:label "Chapter 1's research record shipped without its licence and provenance metadata"@en ;
    backlog:belongsToLineage ex:Lineage ; backlog:relatesToWorkItem ex:ST_Research_Ch01 ; backlog:hasFindingScope backlog:Scope_Methodology ;
    backlog:hasRootCause "sen0414_ch01_research_v1_0_0 was written by hand before the generic RDODI builder existed, and the metadata check at the time covered only the three Stage 2 files. When the page rebuild ran every file through one gate runner, the research header was found to lack eight of the ten BP-D24 predicates. In the same pass the owner's review exposed labels the camel-case rule had mangled - 'I o function', 'F string' - in the domain ontology and therefore in the document's section titles." ;
    backlog:hasRemedy "Research re-published as v1.0.1 with the metadata and an rdfs:comment saying why; domain ontology and document re-published as v1.0.1 with the labels fixed at their source; every v1.0.0 file retired in the same release, and every RDODI gate re-run over the new versions - all pass. The research story stays closed: its content did not change, only its header, and the finding says so." .
"""


def backlog_block():
    L = ['''
ex:Backlog a backlog:Backlog ; rdfs:label "Work admitted for renewing SEN0414's chapters"@en ;
    backlog:hasIdentifier "Backlog_SEN0414_Slides" ; backlog:belongsToLineage ex:Lineage ; backlog:isRegisterRoot true ;
    backlog:hasState backlog:InProgress ; backlog:producedByStage ex:Out_Backlog ;
    backlog:appliesDefinitionOfDone ex:DoD ; backlog:hasCommitment ex:Commit ; backlog:hasMember ex:Init_Slides .
ex:Kickoff a backlog:TransitionEvent ; rdfs:label "Kick-off: the owner declared execution begun"@en ;
    backlog:transitionedItem ex:ST_Research_Ch01 ; backlog:viaTransition backlog:T_Start ;
    backlog:transitionedAt "2026-09-24T20:26:42"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;
    backlog:hasTransitionNote "Declared by the owner in the words 'kick off', once planning was complete: six stories scored and refined to Ready, an iteration with a real period and goal ending at SEN0414's class, and the roadmap report naming chapter 1's research as the next startable item - its tie with chapter 2's research broken by teaching order. Time read from the clock." .
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
                L.append(closure_block(k, n))
                L.append(start_block(k, n))
    L.append(FEEDBACK)
    L.append(ITER % (PLANNED_AT, ", ".join("ex:ST_%s_%s" % (k, cid(n)) for k, _, _ in KIND for n in sorted(PLANNED))))
    return "".join(L)
