#!/usr/bin/env python3
"""objective_make 1.0.0 (Lineage13, 2026-11-26): writes the objective stage file of the register from a table.
Usage: objective_make_v1_0_0.py OUT.ttl   (a lineage's own script, disclosed in the stage comment)."""
import sys
FC = "2026-11-28"
RAT = ("A forecast, not a deadline. backlog_date_plan 1.5.0 could not predict it: this register has no box with effort yet and Lineage12's archive has no "
       "pair of consecutive boxes with effort (the tool refused). The date is read from the delivered pace of Lineage12: four chapters from the mission commit "
       "(2026-11-26 08:39 Istanbul) to closure the same day, about eight hours; five chapters, two of them needing less work, about eight hours from 2026-11-26 17:00, "
       "times the tool's default buffer of 1.5, then the next midnight UTC. To be discussed with the Owner before it is final.")
Q5 = "chapters 16 to 20"
# key, goal, label, kind, query, base, target, dir, unit
O = [
("MissionLecture","G13_Mission","Chapters 16 to 20 that pass every objective of goals G13_DeckReads, G13_PageRuns and G13_Released, so a lecturer can teach and a student learn from them: 0 -> 5","Meas_Derived",
 "Count of chapters for which the objectives of goals G13_DeckReads, G13_PageRuns and G13_Released are all at target, derived from the observations in the register.",0,5,"Increase","chapter"),
("SpecRuns","G13_Build","Chapter specs that the generic builder runs for chapters 16 to 20: 0 -> 5","Meas_Counted",
 "Count of chapters 16 to 20 whose newest deck is built by the generic builder chapter_deck_build_v2_10_0.py from a folder 08-tooling/chNN-deck/spec_* without error (today 0: none of the five has a spec folder).",0,5,"Increase","spec"),
("DeckStandard","G13_DeckReads","Failing conditions of deck standard 1.3.0 on the five decks: 0 held","Meas_Counted",
 "Sum of FAIL conditions printed by sen0414_deck_standard_check_v1_3_0.py on the newest deck and chapter-code manifest of chapters 16 to 20 (today 0 of 65, 13 per chapter); read again after every re-cut.",0,0,"Hold","condition"),
("FitOverlaps","G13_DeckReads","Overlapping text-frame pairs refused by the fit check on the five decks: 4 -> 0","Meas_Counted",
 "Sum of the pair(s) of text frames overlapping printed by the fit check (deckchecks_runner.sh) on the newest decks of chapters 16 to 20 (today 0, 0, 2, 2, 0).",4,0,"Decrease","pair"),
("ReaderNotes","G13_DeckReads","Reader-note findings (presenter directions, missing connection, think-of statements) on the five decks: 188 -> 0","Meas_Counted",
 "Sum of findings printed by sen0414_reader_notes_check_v1_0_0.py on the newest decks of chapters 16 to 20 (today 0, 0, 94, 49, 45).",188,0,"Decrease","finding"),
("StoryProse","G13_DeckReads","Story-prose findings on the five decks: 0 held","Meas_Counted",
 "Sum of findings printed by sen0414_story_prose_check_v1_0_0.py on the newest decks of chapters 16 to 20 (today 0); read again after every re-cut.",0,0,"Hold","finding"),
("Balloons","G13_DeckReads","Code slides with one story balloon and two result balloons on the five decks: 53 -> 117","Meas_Counted",
 "Count of code slides (25, 28, 27, 18, 19 = 117, the examples of each chapter's manifest) that carry two result balloons, read from the shape names of the deck (today 25 + 28 + 0 + 0 + 0 = 53).",53,117,"Increase","slide"),
("DeckAnalogies","G13_DeckReads","Everyday-analogy slides on the five decks: 25 -> 0","Meas_Counted",
 "Count of slides whose text carries the title or marker Everyday picture(s) or ANALOGY, read from the newest decks of chapters 16 to 20 (today 0, 0, 9, 8, 8).",25,0,"Decrease","slide"),
("PhraseHits","G13_DeckReads","Think-of kind phrases in slide text and notes of the five decks: 8 -> 0","Meas_Counted",
 "Count of hits of the phrase scan (think of, imagine, just like, is like a, are like, as if, picture a) in slide text and notes of the newest decks of chapters 16 to 20 (today 0, 0, 5, 3, 0; log phrase_scan_v1_0_0.log).",8,0,"Decrease","hit"),
("RunInOrder","G13_PageRuns","Pages with a top menu item that runs the slide examples in order: 0 -> 5","Meas_Counted",
 "Count of newest pages of chapters 16 to 20 whose page opens an item that runs the slide examples in slide order, read from the page file and its page test (today 0 occurrences in each of the five).",0,5,"Increase","page"),
("PageAbox","G13_PageRuns","Pages with a page A-box that conforms to the page shapes: 0 -> 5","Meas_Counted",
 "Count of chapters 16 to 20 whose page A-box file, of the same version as the newest page, conforms to 03-materials/sen0414_page_shapes_v1_0_0.ttl under pyshacl (today 0: chapters 16 and 18 have an older A-box that does not conform; chapters 17, 19 and 20 have none).",0,5,"Increase","page"),
("PagesPassing","G13_PageRuns","Pages that pass the page test on the current pipeline: 0 -> 5","Meas_Counted",
 "Count of chapters 16 to 20 whose newest page passes sen0414_page_test_run_v1_1_0.py with 0 failed features, the log kept beside the page (today 0: no log of the current pipeline exists for any of the five).",0,5,"Increase","page"),
("CodeParses","G13_PageRuns","Page frames whose code does not parse: 0 held","Meas_Counted",
 "Sum of the frames the material check (condition code-parses) counts as failed on the newest page of chapters 16 to 20 (today 0 of 135).",0,0,"Hold","frame"),
("PageLambda","G13_PageRuns","Lambda words in the pages: 0 held","Meas_Counted",
 "Sum of page_occurrences printed by the material check (condition no-lambda) on the newest page of chapters 16 to 20 (today 0).",0,0,"Hold","word"),
("PageAnalogies","G13_PageRuns","Analogy words in the page text: 0 held","Meas_Counted",
 "Count of the words Everyday picture and analogy in the visible text of the newest page of chapters 16 to 20 (today 0).",0,0,"Hold","word"),
("MaterialConditions","G13_Released","Failing conditions of the material check on the five decks and pages: 0 held","Meas_Counted",
 "Sum of FAIL conditions printed by cme_material_check_v1_0_2.py on the newest deck and page of chapters 16 to 20 (today 0 of 40, 8 per chapter).",0,0,"Hold","condition"),
("ReviewVerdicts","G13_Released","Review verdicts recorded for the five chapters: 0 -> 60","Meas_Counted",
 "Count of verdict lines (academician, faculty reviewer, undergraduate reader; 4 conditions each) in the five REVIEW_RECORD_chNN files of this lineage (today 0).",0,60,"Increase","verdict"),
("ReleaseRecords","G13_Released","Release records written before the release of each chapter: 0 -> 5","Meas_Counted",
 "Count of reports/REPORT_Lineage13_chNN_release_and_review files (NN 16 to 20) that exist with every check log named in them (today 0).",0,5,"Increase","record"),
("OwnVersions","G13_Released","Older page drafts left beside the newest page: 38 -> 0","Meas_Counted",
 "Count of 03-materials/chNN/page/sen0414_chNN_page_v*.html files other than the newest, NN 16 to 20 (today 8, 6, 9, 7, 8).",38,0,"Decrease","file"),
("Unmeasured","G13_Known","Named unmeasured items given a recorded measurement: 0 -> 4","Meas_Counted",
 "Count of the four items named in the mission (page test on the current pipeline, matching code of chapter code, page and lab libraries, links and pictures of chapters 18 to 20, story repeat over chapters 16 to 20) that have a measurement log under 08-tooling/lineage13-*/ (today 0).",0,4,"Increase","item"),
("OutsideFiles","G13_Contained","Changed files outside the allowed folders: 0 held","Meas_Counted",
 "Count of files in git diff --name-only from the commit of the objective stage to the head that lie outside 03-materials/ch16..ch20 (except rdodi), 08-tooling, 07-lineage and reports.",0,0,"Hold","file"),
("ContentChanged","G13_Guard_Content","Content changes that no ruling forces: 0 held","Meas_Judged",
 "Count of changes the faculty reviewer and the owner find, reading each re-cut deck against the earlier deck of its chapter, that no ruling forces.",0,0,"Hold","change"),
("ExamFiles","G13_Guard_ExamWork","Changed exam files: 0 held","Meas_Counted",
 "Count of changed files in git diff whose path names exam or mock-exam material.",0,0,"Hold","file"),
("OtherChapterFiles","G13_Guard_OtherChapters","Changed files of chapters 1 to 15 and 21 to 25: 0 held","Meas_Counted",
 "Count of changed files in git diff under 03-materials/ch01..ch15 and ch21..ch25.",0,0,"Hold","file"),
("LabFiles","G13_Guard_LabMaterials","Changed lab files: 0 held","Meas_Counted",
 "Count of changed files in git diff whose path names a lab library, session or handout.",0,0,"Hold","file"),
("RdodiFiles","G13_Guard_Rdodi","Existing files under the chapters' rdodi folders modified or deleted: 0 held","Meas_Counted",
 "Count of files in git diff --name-status from the commit of the objective stage to the head with status M or D under 03-materials/ch16..ch20/rdodi (added files are not counted).",0,0,"Hold","file"),
]
G = ["Mission","Build","DeckReads","PageRuns","Released","Known","Contained","Guard_Content","Guard_ExamWork","Guard_OtherChapters","Guard_LabMaterials","Guard_Rdodi"]
H = '''@prefix backlog: <http://example.org/backlog#> .
@prefix ex:      <http://example.org/sen0414-ch1620corr-lineage#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<http://example.org/sen0414-ch1620corr-lineage> a owl:Ontology ;
    rdfs:label "Fresh narrow lineage: SEN0414 Chapters 16 to 20 corrections"@en ;
    owl:versionInfo "1.3.0" ; owl:versionIRI <http://example.org/sen0414-ch1620corr-lineage/1.3.0> ;
    owl:priorVersion <http://example.org/sen0414-ch1620corr-lineage/1.2.0> ; dcterms:identifier "sen0414_ch1620corr_lineage" ;
    rdfs:comment """1.3.0 (2026-11-26): Objective stage only (one stage per version). Each goal is measured by objectives (%d in all), each metric derived from its goal, each with a counted, derived or judged measurement and a query that reads it, a baseline measured on 2026-11-26 (logs in 08-tooling/lineage13-opening/; the balloon, own-version, spec and page counts from the files named in each query) and a baseline observation. Objectives whose figure is met by absence carry the direction Hold: their figure is read at every observation and can rise. The balloon target is the real count of code slides (117 = 25 + 28 + 27 + 18 + 19); the rdodi objective counts existing files modified or deleted, so new files there are allowed by this objective only where the scope allows them; the allowed folders of the outside-files objective are listed in its query. The objectives are written by the table script 08-tooling/lineage13-opening/objective_make_v1_0_0.py, a lineage's own script, disclosed. Checkpoint dates are forecasts, never deadlines. The goals of 1.2.0 already carry their origin and decider."""@en .

''' % len(O)
out=[H]
for k,g,lab,kind,q,b,t,d,u in O:
    out.append(f'''ex:Metric_Obj13_{k} a backlog:Metric ; backlog:belongsToLineage ex:Lineage13 ;
    backlog:metricBaseline "{b}"^^xsd:integer ; backlog:metricTarget "{t}"^^xsd:integer ; backlog:metricUnit "{u}" ;
    rdfs:label "{lab}"@en .
ex:CP13_{k} a backlog:ObjectiveCheckpoint ; backlog:checkpointDate "{FC}T00:00:00Z"^^xsd:dateTime ; backlog:expectedValue "{t}"^^xsd:decimal .
ex:Obj13_{k} a backlog:Objective ;
    rdfs:label "{lab}"@en ;
    backlog:belongsToLineage ex:Lineage13 ; backlog:objectiveForGoal ex:{g} ; backlog:contributesToGoal ex:{g} ;
    backlog:fillsScope ex:Scope13 ;
    backlog:hasMetric ex:Metric_Obj13_{k} ; backlog:hasSuccessMetric ex:Metric_Obj13_{k} ;
    backlog:hasMeasurementKind backlog:{kind} ; backlog:hasMeasurementQuery "{q}" ;
    backlog:hasBaselineValue "{b}"^^xsd:decimal ; backlog:hasTargetValue "{t}"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_{d} ;
    backlog:hasCheckpoint ex:CP13_{k} ;
    backlog:hasForecastDate "{FC}"^^xsd:date ; backlog:hasForecastRationale "{RAT}" ;
    backlog:hasIntentOrigin backlog:IOrigin_SessionDrafted ; backlog:decidedBy backlog:Owner .
ex:Obs0_Obj13_{k} a backlog:MetricObservation ; rdfs:label "Baseline of 2026-11-26: {lab.rsplit(":",1)[0]}"@en ;
    backlog:observesMetric ex:Metric_Obj13_{k} ; backlog:observationFor ex:Obj13_{k} ; backlog:hasObservedValue "{b}"^^xsd:decimal ;
    backlog:observedAt "2026-11-26T14:00:00Z"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "{q}" .
''')
open(sys.argv[1],"w").write("".join(out))
