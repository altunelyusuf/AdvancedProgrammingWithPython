#!/usr/bin/env python3
"""objective_make 1.0.0 (Lineage14, 2026-11-26): writes the objective stage file of the register from a table (a lineage's own script, disclosed in the stage comment).
Usage: objective_make_v1_0_0.py OUT.ttl"""
import sys
FC = "2026-11-28"
RAT = ("A forecast, not a deadline. backlog_date_plan could not predict it: this register has no box with effort yet. The date is read from the delivered pace of Lineage13: "
       "five chapters from its mission commit (2026-11-26 about 17:00 Istanbul) to closure the same evening, about three hours, the chapters having decks already; "
       "chapters 21 to 25 start from first-version decks and need a spec and a chapter-code manifest each, taken as twice the work, about six hours from 2026-11-26 20:30, "
       "times the default buffer of 1.5, then the next midnight UTC. To be discussed with the Owner before it is final.")
# key, goal, label, kind, query, base, target, dir, unit
O = [
("MissionLecture","G14_Mission","Chapters 21 to 25 that pass every objective of goals G14_DeckReads, G14_PageRuns and G14_Released, so a lecturer can teach and a student learn from them: 0 -> 5","Meas_Derived",
 "Count of chapters for which the objectives of goals G14_DeckReads, G14_PageRuns and G14_Released are all at target, derived from the observations in the register.",0,5,"Increase","chapter"),
("SpecRuns","G14_Build","Chapter specs that the generic builder runs for chapters 21 to 25: 0 -> 5","Meas_Counted",
 "Count of chapters 21 to 25 whose newest deck is built by the generic builder chapter_deck_build_v2_10_0.py from a folder 08-tooling/chNN-deck/spec_* without error (today 0: none of the five has a spec folder; the first-version per-chapter builders deck_build_v1_0_0.py are not the generic builder).",0,5,"Increase","spec"),
("DeckStandard","G14_DeckReads","Failing conditions of deck standard 1.3.0 on the five decks: 0 held, first read at the deck stage","Meas_Counted",
 "Sum of FAIL conditions printed by sen0414_deck_standard_check_v1_3_0.py on the newest deck and chapter-code manifest of chapters 21 to 25 (65 conditions, 13 per chapter). Today the check cannot run, because no chapter-code manifest exists; the held figure 0 is first read when the manifest exists; read again after every re-cut.",0,0,"Hold","condition"),
("FitOverlaps","G14_DeckReads","Overlapping text-frame pairs refused by the fit check on the five decks: 0 held","Meas_Counted",
 "Sum of the pair(s) of text frames overlapping printed by the fit check (deckchecks_runner.sh) on the newest decks of chapters 21 to 25 (today 0, 0, 0, 0, 0; log gap_measure.log).",0,0,"Hold","pair"),
("ReaderNotes","G14_DeckReads","Reader-note findings (presenter directions, missing connection, think-of statements) on the five decks: 79 -> 0","Meas_Counted",
 "Sum of findings printed by sen0414_reader_notes_check_v1_0_0.py on the newest decks of chapters 21 to 25 (today 12, 15, 21, 14, 17; log gap_measure.log).",79,0,"Decrease","finding"),
("StoryProse","G14_DeckReads","Story-prose findings on the five decks: 0 held","Meas_Counted",
 "Sum of findings printed by sen0414_story_prose_check_v1_0_0.py on the newest decks of chapters 21 to 25 (today 0); read again after every re-cut.",0,0,"Hold","finding"),
("Balloons","G14_DeckReads","Code examples whose slide lacks two result balloons on the five decks: 42 -> 0","Meas_Counted",
 "Count of examples (11, 8, 7, 8, 8 = 42, read from the examples_out_v1_0_0.json file of each first-version deck, which holds three keys that are not examples) whose code slide does not carry two result balloons, read from the shape names of the deck (today 42: no deck has them). The count is read again against each chapter's chapter-code manifest once it exists, and a correction note is appended if the manifest holds another number.",42,0,"Decrease","slide"),
("DeckAnalogies","G14_DeckReads","Everyday-analogy slides on the five decks: 0 held","Meas_Counted",
 "Count of slides whose text carries the title or marker Everyday picture(s) or ANALOGY, read from the newest decks of chapters 21 to 25 (today 0, 0, 0, 0, 0).",0,0,"Hold","slide"),
("PhraseHits","G14_DeckReads","Think-of kind phrases in slide text and notes of the five decks: 3 -> 0","Meas_Counted",
 "Count of hits of the phrase scan (think of, imagine, just like, is like a, are like, as if, picture a, whole words) in slide text and notes of the newest decks of chapters 21 to 25 (today 1, 0, 2, 0, 0; log gap_measure.log).",3,0,"Decrease","hit"),
("DeckPrompts","G14_DeckReads","Prompt marks '>>>' in the slide text of the five decks: 228 -> 0","Meas_Counted",
 "Count of occurrences of '>>>' in the text of the slides of the newest decks of chapters 21 to 25 (today 67, 39, 39, 38, 45 = 228 occurrences in the first-version decks, of which 26 per deck are a lone mark on every slide and the rest are prompt lines of code; 130 lone marks and 98 prompt lines).",228,0,"Decrease","occurrence"),
("RunInOrder","G14_PageRuns","Pages with a top menu item that runs the slide examples in order: 0 -> 5","Meas_Counted",
 "Count of newest pages of chapters 21 to 25 whose page opens an item that runs the slide examples in slide order, read from the page file and its page test (today 0 occurrences in each of the five).",0,5,"Increase","page"),
("PageAbox","G14_PageRuns","Pages with a page A-box that conforms to the page shapes: 0 -> 5","Meas_Counted",
 "Count of chapters 21 to 25 whose page A-box file, of the same version as the newest page, conforms to 03-materials/sen0414_page_shapes_v1_0_0.ttl under pyshacl (today 0: no page A-box file exists in any of the five chapter folders).",0,5,"Increase","page"),
("PagesPassing","G14_PageRuns","Pages that pass the page test on the current pipeline: 0 -> 5","Meas_Counted",
 "Count of chapters 21 to 25 whose newest page passes sen0414_page_test_run_v1_1_0.py with 0 failed features, the log kept beside the page (today 0: no log of the current pipeline exists for any of the five).",0,5,"Increase","page"),
("CodeParses","G14_PageRuns","Page frames whose code does not parse: 229 -> 0","Meas_Counted",
 "Sum of the frames the material check (condition code-parses) counts as failed on the newest page of chapters 21 to 25 (today 47, 44, 46, 45 and 47 of 47, 44, 46, 51 and 47 frames; logs material_ch*.log).",229,0,"Decrease","frame"),
("PageLambda","G14_PageRuns","Lambda words in the pages: 1915 -> 0","Meas_Counted",
 "Sum of page_occurrences printed by the material check (condition no-lambda) on the newest page of chapters 21 to 25 (today 227, 188, 1163, 175 and 162; logs material_ch*.log).",1915,0,"Decrease","word"),
("PageAnalogies","G14_PageRuns","Analogy words in the page text: 0 held","Meas_Counted",
 "Count of the words Everyday picture and analogy in the visible text of the newest page of chapters 21 to 25 (today 0).",0,0,"Hold","word"),
("MaterialConditions","G14_Released","Failing conditions of the material check on the five decks and pages: 30 -> 0","Meas_Counted",
 "Sum of FAIL conditions printed by cme_material_check_v1_0_2.py on the newest deck and page of chapters 21 to 25 (today 6 per chapter = 30 of 40; logs material_ch*.log).",30,0,"Decrease","condition"),
("ReviewVerdicts","G14_Released","Review verdicts recorded for the five chapters: 0 -> 60","Meas_Counted",
 "Count of verdict lines (academician, faculty reviewer, undergraduate reader; 4 conditions each) in the five REVIEW_RECORD_chNN files of this lineage (today 0).",0,60,"Increase","verdict"),
("ReleaseRecords","G14_Released","Release records written before the release of each chapter: 0 -> 5","Meas_Counted",
 "Count of reports/REPORT_Lineage14_chNN_release_and_review files (NN 21 to 25) that exist with every check log named in them (today 0).",0,5,"Increase","record"),
("OwnVersions","G14_Released","Older page drafts left beside the newest page: 12 -> 0","Meas_Counted",
 "Count of 03-materials/chNN/page/sen0414_chNN_page_v*.html files other than the newest, NN 21 to 25 (today 3, 3, 3, 3, 0).",12,0,"Decrease","file"),
("Unmeasured","G14_Known","Named unmeasured items given a recorded measurement: 0 -> 4","Meas_Counted",
 "Count of the four items named in the mission and scope (page test on the current pipeline, matching code of chapter code, page and lab libraries, links and pictures of chapters 21 to 25, story repeat over chapters 21 to 25) that have a measurement log under 08-tooling/lineage14-*/ made on the final files (today 0; the first read of the story-repeat log in lineage14-opening is of the old pages and does not count).",0,4,"Increase","item"),
("OutsideFiles","G14_Contained","Changed files outside the allowed folders: 0 held","Meas_Counted",
 "Count of files in git diff --name-only from the commit of the objective stage to the head that lie outside 03-materials/ch21..ch25 (except rdodi), 08-tooling, 07-lineage and reports.",0,0,"Hold","file"),
("ContentChanged","G14_Guard_Content","Content changes that no ruling forces: 0 held","Meas_Judged",
 "Count of changes the faculty reviewer and the owner find, reading each re-cut deck and page against the earlier deck and page of its chapter, that no ruling forces. A recorded paragraph whose wording changes because the recording interpreter changed is counted (Lineage13 counted five).",0,0,"Hold","change"),
("ExamFiles","G14_Guard_ExamWork","Changed exam files: 0 held","Meas_Counted",
 "Count of changed files in git diff whose path names exam or mock-exam material.",0,0,"Hold","file"),
("OtherChapterFiles","G14_Guard_OtherChapters","Changed files of chapters 1 to 20: 0 held","Meas_Counted",
 "Count of changed files in git diff under 03-materials/ch01..ch20.",0,0,"Hold","file"),
("LabFiles","G14_Guard_LabMaterials","Changed lab files: 0 held","Meas_Counted",
 "Count of changed files in git diff whose path names a lab library, session or handout.",0,0,"Hold","file"),
("RdodiFiles","G14_Guard_Rdodi","Existing files under the chapters' rdodi folders modified or deleted: 0 held","Meas_Counted",
 "Count of files in git diff --name-status from the commit of the objective stage to the head with status M or D under 03-materials/ch21..ch25/rdodi (added files are not counted).",0,0,"Hold","file"),
]
H = '''@prefix backlog: <http://example.org/backlog#> .
@prefix ex:      <http://example.org/sen0414-ch2125corr-lineage#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<http://example.org/sen0414-ch2125corr-lineage> a owl:Ontology ;
    rdfs:label "Fresh narrow lineage: SEN0414 Chapters 21 to 25 corrections"@en ;
    owl:versionInfo "1.3.0" ; owl:versionIRI <http://example.org/sen0414-ch2125corr-lineage/1.3.0> ;
    owl:priorVersion <http://example.org/sen0414-ch2125corr-lineage/1.2.0> ; dcterms:identifier "sen0414_ch2125corr_lineage" ;
    rdfs:comment """1.3.0 (2026-11-26): Objective stage only (one stage per version). Each goal is measured by objectives (%d in all), each metric derived from its goal, each with a counted, derived or judged measurement and a query that reads it, a baseline measured on 2026-11-26 (logs gap_measure.log, gap_measure_pages.log and material_ch*.log in 08-tooling/lineage14-opening/) and a baseline observation. Objectives whose figure is met by absence carry the direction Hold. Lessons of Lineage13 taken: no target is a count of something that can be miscounted (the balloon objective counts the examples that lack balloons, 42 today, down to 0; an objective that cannot be read yet says so in its query); the rdodi objective counts existing files modified or deleted; the allowed folders of the outside-files objective are listed in its query; the judged content objective names the recorded-paragraph case Lineage13 counted. CORRECTION OF THE MISSION STAGE 1.0.0 (appended, never edited): it said that the slide text holds '>>>' prompts 67, 39, 39, 38 and 45 times; those are occurrences of the three characters, of which 26 per deck are a lone mark shape on every slide and the rest are prompt lines of code (41, 13, 13, 12 and 19). The new objective DeckPrompts counts all of them. The objectives are written by the table script 08-tooling/lineage14-opening/objective_make_v1_0_0.py, the lineage's own script (a BRSF handover is owed with the others)."""@en .

''' % len(O)
out=[H]
for k,g,lab,kind,q,b,t,d,u in O:
    out.append(f'''ex:Metric_Obj14_{k} a backlog:Metric ; backlog:belongsToLineage ex:Lineage14 ;
    backlog:metricBaseline "{b}"^^xsd:integer ; backlog:metricTarget "{t}"^^xsd:integer ; backlog:metricUnit "{u}" ;
    rdfs:label "{lab}"@en .
ex:CP14_{k} a backlog:ObjectiveCheckpoint ; backlog:checkpointDate "{FC}T00:00:00Z"^^xsd:dateTime ; backlog:expectedValue "{t}"^^xsd:decimal .
ex:Obj14_{k} a backlog:Objective ;
    rdfs:label "{lab}"@en ;
    backlog:belongsToLineage ex:Lineage14 ; backlog:objectiveForGoal ex:{g} ; backlog:contributesToGoal ex:{g} ;
    backlog:fillsScope ex:Scope14 ;
    backlog:hasMetric ex:Metric_Obj14_{k} ; backlog:hasSuccessMetric ex:Metric_Obj14_{k} ;
    backlog:hasMeasurementKind backlog:{kind} ; backlog:hasMeasurementQuery "{q}" ;
    backlog:hasBaselineValue "{b}"^^xsd:decimal ; backlog:hasTargetValue "{t}"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_{d} ;
    backlog:hasCheckpoint ex:CP14_{k} ;
    backlog:hasForecastDate "{FC}"^^xsd:date ; backlog:hasForecastRationale "{RAT}" ;
    backlog:hasIntentOrigin backlog:IOrigin_SessionDrafted ; backlog:decidedBy backlog:Owner .
ex:Obs0_Obj14_{k} a backlog:MetricObservation ; rdfs:label "Baseline of 2026-11-26: {lab.rsplit(":",1)[0]}"@en ;
    backlog:observesMetric ex:Metric_Obj14_{k} ; backlog:observationFor ex:Obj14_{k} ; backlog:hasObservedValue "{b}"^^xsd:decimal ;
    backlog:observedAt "2026-11-26T14:00:00Z"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "{q}" .
''')
open(sys.argv[1],"w").write("".join(out))
