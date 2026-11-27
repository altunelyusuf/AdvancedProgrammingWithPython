#!/usr/bin/env python3
"""chain_make 1.0.0 (Lineage15, 2026-11-27): writes the delta of ONE chain stage of the urgent lineage Lineage15 as Turtle for register_step_v1_1_0.py (EXTRA.ttl),
following the per-stage pattern of Lineage14's makers (scope_make, objective_make, backlog_make). A lineage's own script, disclosed as a tool gap.
Usage: chain_make_v1_0_0.py mission|scope|goal|objective|backlog OUT.ttl"""
import sys
Q = lambda s: s.replace('"', '\\"')
L = "ex:Lineage15"
CL = {"tab": "a Slide source code tab", "open": "exam result and answers open after finishing", "meta": "exam questions about the subject, never about the book",
      "nolam": "no lambda unless the subject teaches it", "deck": "code slides that carry a goal line, meaning, reason and idea balloons, a watch-out and a predict prompt",
      "notes": "notes that speak to the reader"}
MISSION = ("Every chapter of SEN0414 (chapters 1 to 25) has an interactive page with " + CL["tab"] + " that runs the slide code in order, with " + CL["open"] + ", " + CL["meta"] +
           ", and " + CL["nolam"] + ", and a deck with " + CL["deck"] + " and with " + CL["notes"] + ", as the owner ruled on 2026-11-27 and 2026-11-24, with no slide added to any deck and the content of the chapters unchanged.")
ORIGIN = "Owner's rulings of 2026-11-27 (chapter 11 urgency, extended by 'These should be applied to all chapters and submit a handover to CME') and of 2026-11-24 (no everyday analogies, no lambdas unless taught, reader-facing notes), the urgent interruption of Lineage14 recorded in register 1.25.0."
o = ['@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-ch2125corr-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n']
w = o.append
stage = sys.argv[1]
AREAS = [("Pages", "Chapter pages (1 to 25) carry the rulings", "Product", "03-materials/ch01..ch25/page/ newest sen0414_chNN_page_v*.html", "24 of 25 pages have the Slide source code tab and open exam answers; 546 lambda words (ch1-3, 5-9: 369, ch22: 2, ch25: 175)"),
         ("Decks", "Chapter decks (1 to 25) carry the code-slide standard and reader notes", "Product", "03-materials/ch01..ch25/ newest SEN0414_ChNN_*.pptx", "513 code slides of 24 decks lack the standard; 497 of 535 notes of chapters 1-8 address a presenter"),
         ("Sources", "Corpora, generators and domain A-boxes free of the removed forms", "Work", "08-tooling/ and 03-materials/ sources of the pages", "523 source files carry book-metadata nodes or questions (all versions counted)"),
         ("Route", "The record of work built before its route", "Work", "07-lineage register and 08-tooling/lineage15-urgency/", "23 pages and the chapter 11 deck and page built before the urgency declaration (commit e7ce395)")]
DELIV = [("Pages", "Pages_Tab", "Every page (1 to 25) with the Slide source code tab and open exam answers", "Functional", CL["tab"]),
         ("Pages", "Pages_NoLambda", "Every page without lambda words", "NonFunctional", CL["nolam"]),
         ("Pages", "Pages_NoMeta", "Every page with exam questions about the subject only", "Functional", CL["meta"]),
         ("Decks", "Decks_Code", "Every deck with the chapter 11 code-slide standard and no slide added", "Functional", CL["deck"]),
         ("Decks", "Decks_Notes", "Every deck with notes that speak to the reader", "NonFunctional", CL["notes"]),
         ("Sources", "Sources_Clean", "Sources without the removed forms", "Work", CL["meta"]),
         ("Route", "Route_Record", "Re-verification log of the pages built before the route", "Work", CL["tab"])]
OBJ = [  # key, goal, label, kind, query, base, target, dir, unit
 ("PagesTab", "G15_PagesTeach", "Pages with the Slide source code tab: 24 -> 25", "Meas_Counted", "Count of the newest pages of chapters 1 to 25 that contain the text Slide source code (today 24; chapter 25 has none).", 24, 25, "Increase", "page"),
 ("PagesOpen", "G15_PagesTeach", "Pages with the Open result and answers button: 24 -> 25", "Meas_Counted", "Count of the newest pages of chapters 1 to 25 that contain the text Open result and answers (today 24).", 24, 25, "Increase", "page"),
 ("PagesLambda", "G15_PagesTeach", "Lambda words in the newest pages: 546 -> 0", "Meas_Counted", "Sum of case-insensitive occurrences of lambda in the newest page of chapters 1 to 25 (today 546: chapters 1-3 and 5-8 16 each, chapter 9 257, chapter 22 2, chapter 25 175).", 546, 0, "Decrease", "word"),
 ("CodeSlides", "G15_DecksTeach", "Code slides of the 24 other decks without the chapter 11 standard: 513 -> 0", "Meas_Counted", "Count of code slides in the newest decks of chapters 1 to 10 and 12 to 25 that lack a goal line, the three balloons, a watch-out or a predict prompt (today 513, counted in the earlier session).", 513, 0, "Decrease", "slide"),
 ("PresenterNotes", "G15_DecksTeach", "Notes of chapters 1 to 8 that address a presenter: 497 -> 0", "Meas_Counted", "Count of speaker notes of the newest decks of chapters 1 to 8 that carry a presenter direction (today 497 of 535).", 497, 0, "Decrease", "note"),
 ("SourcesMeta", "G15_SourcesClean", "Source files that carry metadata nodes or questions: 523 -> 0", "Meas_Counted", "Count of .py, .json and .ttl files under 08-tooling and 03-materials (outside page files) that contain a name of the metadata set PracticeQuestions, PracticePrograms, WorkingVocabulary, BookCorrections or EditionChange (today 523, all versions; archived versions are not processed, so the target counts the newest versions only).", 523, 0, "Decrease", "file"),
 ("Reverified", "G15_Route", "Pages built before the route that were re-verified under it: 0 -> 23", "Meas_Counted", "Count of the 23 pages of the rollout with a re-verification log kept in 08-tooling/lineage15-urgency/ (today 0).", 0, 23, "Increase", "page"),
 ("ChaptersMeeting", "G15_Mission", "Chapters whose page and deck meet all rulings: 1 -> 25", "Meas_Derived", "Count of chapters for which the objectives PagesTab, PagesOpen, PagesLambda, CodeSlides and PresenterNotes are at target for that chapter, derived from the observations (today 1: chapter 11).", 1, 25, "Increase", "chapter")]
GOALS = [("G15_Mission", "Every chapter can be lectured from and learned from under the rulings of 2026-11-27", "Facing_Mission", "A lecturer and a student find in every chapter of SEN0414 a page that runs the slide code and a deck that explains meaning, reason and idea, as the rulings state.", []),
         ("G15_PagesTeach", "The pages run the slide code, open the exam answers, ask about the subject and teach no lambda", "Facing_Scope", "Every chapter page has the Slide source code tab, shows the exam result and answers after finishing, asks questions about the subject and its code only, and has no lambda unless the chapter teaches it.", ["Pages"]),
         ("G15_DecksTeach", "The decks explain each code slide and speak to the reader", "Facing_Scope", "Every code slide shows its goal line, meaning, reason and idea balloons, a watch-out and a predict prompt, and the notes of every deck speak to the reader, with no slide added.", ["Decks"]),
         ("G15_SourcesClean", "The sources no longer carry the removed forms", "Facing_Scope", "A rebuild of any page from the corpora, generators and A-boxes yields no metadata question or node without a clean-up after the build.", ["Sources"]),
         ("G15_Route", "The work built before its route is recorded and verified under the route", "Facing_Scope", "Every page built before the urgency declaration is re-verified and the record names each result, so no work stands outside the register.", ["Route"])]
if stage == "mission":
    w(f'ex:Mission15 a backlog:Mission ; rdfs:label "Every SEN0414 chapter page and deck meets the rulings of 2026-11-27"@en ;\n    backlog:decidedBy backlog:Owner ; backlog:hasMissionOutcome backlog:Out_InFlight ;\n    backlog:hasMissionOrigin "{Q(ORIGIN)}" ;\n    backlog:hasMissionStatement "{Q(MISSION)}" ;\n    backlog:missionFor ex:Backlog15 .\n')
    w(f"{L} backlog:lineageForMission ex:Mission15 .\n")
elif stage == "scope":
    for k, lab, lay, loc, meas in AREAS:
        w(f'ex:Area15_{k} a backlog:ScopeArea ; backlog:belongsToLineage {L} ; rdfs:label "{Q(lab)}"@en ; backlog:hasScopeLayer backlog:Layer_{lay} ;\n    backlog:areaLocation "{Q(loc)}" ; backlog:areaMeasure "{Q(meas)}" .\n')
    for a, k, lab, kind, clause in DELIV:
        lay = "Work" if kind == "Work" else "Product"
        s = f'ex:Del15_{k} a backlog:ScopeDeliverable ; backlog:belongsToLineage {L} ; backlog:deliverableForArea ex:Area15_{a} ; rdfs:label "{Q(lab)}"@en ; backlog:hasScopeLayer backlog:Layer_{lay} ;'
        if kind != "Work": s += f' backlog:hasProductScopeKind backlog:Kind_{kind} ;'
        w(s + f' backlog:derivesFromMissionClause "{Q(clause)}" .\n')
    EX = [("Content", "Changes to what the chapters teach", "Any change to what a chapter teaches, to its stories or to the meaning of an example, except a change a ruling forces.", "The rulings change form, not content."),
          ("ExamBank", "New exam content", "Writing new exam questions beyond removing questions about book metadata.", "Exam content is its own work; only the metadata questions are removed here."),
          ("LabLibs", "Lab libraries and lab sessions", "Any lab library, lab session or handout.", "Queued as the lab-materials lineage."),
          ("Ch2125", "Chapters 21 to 25 corrections of Lineage14", "Any item that Lineage14's scope already covers.", "Lineage14 is paused, not changed; its scope stays its own.")]
    for k, lab, c, why in EX:
        w(f'ex:Excl15_{k} a backlog:ScopeExclusion ; backlog:belongsToLineage {L} ; backlog:decidedBy backlog:Owner ; rdfs:label "{Q(lab)}"@en ;\n    backlog:excludesConcern "{Q(c)}" ; backlog:hasExclusionRationale "{Q(why)}" ; backlog:hasScopeLayer backlog:Layer_Work .\n')
    al = " , ".join(f"ex:Area15_{k}" for k, *_ in AREAS); dl = " , ".join(f"ex:Del15_{k}" for _, k, *_ in DELIV); el = " , ".join(f"ex:Excl15_{k}" for k, *_ in EX)
    w(f'ex:Scope15 a backlog:ScopeStatement ; backlog:belongsToLineage {L} ; rdfs:label "Chapter pages and decks of SEN0414 (1 to 25) under the rulings of 2026-11-27"@en ;\n    backlog:scopeForMission ex:Mission15 ; backlog:coversArea {al} ;\n    backlog:hasScopeDeliverable {dl} ; backlog:requiresDeliverable {dl} ; backlog:hasScopeExclusion {el} ; backlog:hasIntentOrigin backlog:IOrigin_OwnerStated .\n')
elif stage == "goal":
    for gid, lab, facing, stmt, areas in GOALS:
        s = f'ex:{gid} a backlog:Goal ; rdfs:label "{Q(lab)}"@en ; backlog:belongsToLineage {L} ; backlog:contributesToMission ex:Mission15 ; backlog:decidedBy backlog:Owner ;\n    backlog:derivesFromScope ex:Scope15 ; backlog:goalCompletionState backlog:Proposed ; backlog:goalForMission ex:Mission15 ; backlog:hasGoalFacing backlog:{facing} ;\n    backlog:hasGoalStatement "{Q(stmt)}" ; backlog:hasIntentOrigin backlog:IOrigin_SessionDrafted'
        if areas: s += " ;\n    backlog:goalCoversArea " + " , ".join(f"ex:Area15_{a}" for a in areas)
        w(s + " .\n")
elif stage == "objective":
    FC = "2026-11-30"
    RAT = "A forecast, not a deadline. The urgent box is time-boxed to 2026-11-30 by the declaration of register 1.25.0; the pace of the earlier session (23 pages in one working session) is the only measurement. To be discussed with the Owner before it is final."
    for k, g, lab, kind, q, b, t, d, u in OBJ:
        w(f'''ex:Metric_Obj15_{k} a backlog:Metric ; backlog:belongsToLineage {L} ; backlog:metricBaseline "{b}"^^xsd:integer ; backlog:metricTarget "{t}"^^xsd:integer ; backlog:metricUnit "{u}" ; rdfs:label "{Q(lab)}"@en .
ex:CP15_{k} a backlog:ObjectiveCheckpoint ; backlog:checkpointDate "{FC}T00:00:00Z"^^xsd:dateTime ; backlog:expectedValue "{t}"^^xsd:decimal .
ex:Obj15_{k} a backlog:Objective ; rdfs:label "{Q(lab)}"@en ; backlog:belongsToLineage {L} ; backlog:objectiveForGoal ex:{g} ; backlog:contributesToGoal ex:{g} ; backlog:fillsScope ex:Scope15 ;
    backlog:hasMetric ex:Metric_Obj15_{k} ; backlog:hasSuccessMetric ex:Metric_Obj15_{k} ; backlog:hasMeasurementKind backlog:{kind} ; backlog:hasMeasurementQuery "{Q(q)}" ;
    backlog:hasBaselineValue "{b}"^^xsd:decimal ; backlog:hasTargetValue "{t}"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_{d} ; backlog:hasCheckpoint ex:CP15_{k} ;
    backlog:hasForecastDate "{FC}"^^xsd:date ; backlog:hasForecastRationale "{Q(RAT)}" ; backlog:hasIntentOrigin backlog:IOrigin_SessionDrafted ; backlog:decidedBy backlog:Owner .
ex:Obs0_Obj15_{k} a backlog:MetricObservation ; rdfs:label "Baseline of 2026-11-27: {Q(lab.split(":")[0])}"@en ; backlog:observesMetric ex:Metric_Obj15_{k} ; backlog:observationFor ex:Obj15_{k} ;
    backlog:hasObservedValue "{b}"^^xsd:decimal ; backlog:observedAt "2026-11-27T16:30:00Z"^^xsd:dateTime ; backlog:observedDuringCeremony true ; backlog:hasObservationMethod "{Q(q)}" .
''')
elif stage == "backlog":
    SID = ["Pages_Ch1_9", "Exam_Open", "Page_Ch25", "Sources_Clean", "Decks_CodeSlides", "Rollout_Reverify"]
    OBJS = {"Pages_Ch1_9": ["PagesLambda", "PagesTab", "PagesOpen"], "Exam_Open": ["PagesOpen"], "Page_Ch25": ["PagesTab", "PagesOpen", "PagesLambda"], "Sources_Clean": ["SourcesMeta"],
            "Decks_CodeSlides": ["CodeSlides", "PresenterNotes"], "Rollout_Reverify": ["Reverified"]}
    DEL = {"Pages_Ch1_9": ["Pages_Tab", "Pages_NoLambda", "Pages_NoMeta"], "Exam_Open": ["Pages_Tab"], "Page_Ch25": ["Pages_Tab", "Pages_NoLambda"], "Sources_Clean": ["Sources_Clean"],
           "Decks_CodeSlides": ["Decks_Code", "Decks_Notes"], "Rollout_Reverify": ["Route_Record"]}
    w(f'ex:Backlog15 a backlog:Backlog ; rdfs:label "Urgent backlog: slide source code tab and code-slide standard for all chapters"@en ; backlog:appliesDefinitionOfDone ex:DoD14 ; backlog:backlogForMission ex:Mission15 ;\n    backlog:belongsToLineage {L} ; backlog:hasIdentifier "Backlog_SEN0414_Urgent15" ; backlog:memberOfContainer ex:Register_Ch2125corr ;\n    backlog:hasBacklogMember {" , ".join("ex:ST15_" + s for s in SID)} ; backlog:hasCommitment ex:Commit15 .\n')
    w(f'ex:Commit15 a backlog:Commitment ; rdfs:label "This backlog commits to chapters that meet the rulings of 2026-11-27"@en ; backlog:commitsToDefinitionOfDone ex:DoD14 ; backlog:commitsToGoal ex:G15_Mission ; backlog:commitsToObjective ex:Obj15_ChaptersMeeting .\n')
    for s in SID:
        w(f"ex:ST15_{s} backlog:memberOfContainer ex:Backlog15 ; backlog:pursuesObjective {' , '.join('ex:Obj15_' + x for x in OBJS[s])} ; backlog:satisfiesDeliverable {' , '.join('ex:Del15_' + x for x in DEL[s])} .\n")
else:
    sys.exit(__doc__)
open(sys.argv[2], "w").write("".join(o))
