"""Final observations of the 26 Lineage13 objectives (register 1.36.0 -> 1.37.0). Run from 07-lineage with the rdflib venv."""
import json
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD
from rdflib.namespace import OWL
B=Namespace("http://example.org/backlog#"); EX=Namespace("http://example.org/sen0414-ch1620corr-lineage#")
ONT=URIRef("http://example.org/sen0414-ch1620corr-lineage"); prev,new="1.36.0","1.37.0"
M=json.load(open("../08-tooling/lineage13-closure/final_measure_v1_0_0.json"))
g=Graph(); g.parse(f"sen0414_ch1620corr_lineage_v{prev.replace('.','_')}.ttl")
for p in (OWL.versionInfo,OWL.versionIRI,OWL.priorVersion):
    for x in list(g.objects(ONT,p)): g.remove((ONT,p,x))
g.add((ONT,OWL.versionInfo,Literal(new))); g.add((ONT,OWL.versionIRI,URIRef(str(ONT)+"/"+new))); g.add((ONT,OWL.priorVersion,URIRef(str(ONT)+"/"+prev)))
g.add((ONT,RDFS.comment,Literal(new+" (2026-11-26): Final observations of the 26 objectives, measured from the final files (final_measure_v1_0_0.py and its log, the final_*.log files of the checks, and the earlier closure logs, all in 08-tooling/lineage13-closure and 08-tooling/lineage13-opening). One objective, ContentChanged, is not at target by the letter and carries an appended correction note; the spec objective is above its target.",lang="en")))
O={
"Balloons":(M["Balloons"],"Every code slide of the five newest decks has two result balloons: 25, 28, 27, 18 and 19 slides (final_measure.log)."),
"CodeParses":(M["CodeParses"],"Material check condition code-parses: failed 0 of 72, 71, 72, 51 and 58 frames (final_material_ch*.log)."),
"ContentChanged":(5,"Reading the chapters against their earlier pages: 5 changes no ruling forces, all wordings of recorded paragraphs that now show the real run in the recording interpreter (chapter 16: 1, chapter 17: 2, chapter 19: 2, counted in the release records). Not 0 by the letter (correction note on the objective)."),
"DeckAnalogies":(M["DeckAnalogies"],"No slide of the five newest decks carries the marker Everyday picture or ANALOGY (final_measure.log)."),
"DeckStandard":(M["DeckStandard"],"Deck standard 1.3.0: 0 failing conditions of 65 (final_deck_standard_ch*.log)."),
"ExamFiles":(0,"No exam or mock-exam file in the diff (guard_listing.log)."),
"FitOverlaps":(M["FitOverlaps"],"Fit check: 0 overlapping text-frame pairs on the five decks (final_fit_ch*.log)."),
"LabFiles":(0,"No lab library, session or handout file changed (guard_listing.log)."),
"MaterialConditions":(M["MaterialConditions"],"cme_material_check 1.0.2 on the newest deck and page of each chapter: 0 failing of 40 (final_material_ch*.log)."),
"MissionLecture":(5,"Chapters 16 to 20 each pass every objective of the goals G13_DeckReads, G13_PageRuns and G13_Released at target (read from the observations above)."),
"OtherChapterFiles":(0,"No file under chapters 1 to 15 or 21 to 25 changed (guard_listing.log)."),
"OutsideFiles":(0,"No file outside the allowed folders changed (guard_listing.log)."),
"OwnVersions":(M["OwnVersions"],"One page per chapter in the tree (9.100.0, 9.100.0, 9.102.0, 9.99.0, 9.101.0); 44 older drafts removed with git; version check exit 0 (own_versions_check.log)."),
"PageAbox":(M["PageAbox"],"The newest page A-box of each chapter conforms to the page shapes under pyshacl (final_shacl_ch*.log)."),
"PageAnalogies":(M["PageAnalogies"],"The words Everyday picture, analogy and analogies appear 0 times in the visible text of the newest pages (final_measure.log)."),
"PageLambda":(M["PageLambda"],"Material check condition no-lambda: 0 occurrences on the five pages (final_material_ch*.log)."),
"PagesPassing":(M["PagesPassing"],"Full page test 9.42.0, 0 failed: 100 widgets/207 features (ch16), 95/208 (ch17), 95/207 (ch18), 90/208 (ch19), 91/208 (ch20) (page_test_collect.log); test key, not the instructor's."),
"PhraseHits":(M["PhraseHits"],"Phrase scan (whole-word patterns) of slide text and notes of the five decks: 0 hits (final_measure.log)."),
"RdodiFiles":(0,"No existing rdodi file modified or deleted (guard_listing.log)."),
"ReaderNotes":(M["ReaderNotes"],"Reader-notes check 1.0.0: RESULT CLEAN on the five decks (final_reader_notes_ch*.log)."),
"ReleaseRecords":(M["ReleaseRecords"],"Five release records exist and every check log named in them exists (final_measure.log)."),
"ReviewVerdicts":(M["ReviewVerdicts"],"Five review records with 12 verdict lines each (11 accept, 1 accept with limits per chapter). Made by the building agent, not independent."),
"RunInOrder":(M["RunInOrder"],"The newest page of each chapter carries the run-in-order menu item, and its page test passes (final_measure.log, page_test_collect.log)."),
"SpecRuns":(M["SpecRuns"],"All five chapters have a spec folder and their newest deck is built by the generic builder 2.10.0 (chapters 18 to 20 re-cut, 16 and 17 rebuilt); above the target 3."),
"StoryProse":(M["StoryProse"],"Story-prose check 1.0.0: RESULT CLEAN on the five decks (final_story_prose_ch*.log)."),
"Unmeasured":(M["Unmeasured"],"Four measurement logs exist: page_test_collect.log, matching_code.log (0 differences in 117 examples; lab libraries are not in this repository), measure_links and story_repeat (08-tooling/lineage13-opening)."),
}
objs={str(o).split("#")[1] for o in g.subjects(RDF.type,B.Objective) if "#Obj13_" in str(o)}
assert objs=={"Obj13_"+k for k in O},objs^{"Obj13_"+k for k in O}
for k,(v,c) in O.items():
    o=EX["Obj13_"+k]; m=EX["Metric_Obj13_"+k]; assert (o,None,None) in g and (m,None,None) in g,k
    ob=EX["Obs9_Obj13_"+k]
    g.add((ob,RDF.type,B.MetricObservation)); g.add((ob,B.observationFor,o)); g.add((ob,B.observesMetric,m))
    g.add((ob,B.hasObservedValue,Literal(float(v),datatype=XSD.double)))
    g.add((ob,B.observedAt,Literal("2026-11-26T19:30:00+00:00",datatype=XSD.dateTime)))
    g.add((ob,B.observedDuringCeremony,Literal(True)))
    g.add((ob,B.hasObservationMethod,Literal(str(next(g.objects(o,B.hasMeasurementQuery))))))
    g.add((ob,RDFS.label,Literal("Final observation of 2026-11-26: "+str(next(g.objects(o,RDFS.label))).split(":")[0],lang="en")))
    g.add((ob,RDFS.comment,Literal(c,lang="en")))
g.add((EX.Obj13_ContentChanged,RDFS.comment,Literal("Correction note 2026-11-26 (appended; the target stays as written): the count is 5 by the letter. The five changes are wordings of recorded paragraphs that show the real run under the recording interpreter instead of a missing-module or earlier-interpreter message; no concept, example or story changed. Chapter 18 also carries three corrected wrong descriptions of linked pages, made after the link check and not counted in the release record. The intent (no content change beyond what a ruling or a fact forces) is met only with this reading, so the objective is reported as not at target.",lang="en")))
g.add((EX.Obj13_SpecRuns,RDFS.comment,Literal("Note 2026-11-26 (appended): observed 5 against target 3 because chapters 16 and 17 were also rebuilt from their spec folders to carry the result balloons.",lang="en")))
for p,n in [("backlog",B),("ex",EX),("owl",OWL),("rdfs",RDFS)]: g.bind(p,n)
g.serialize(f"sen0414_ch1620corr_lineage_v{new.replace('.','_')}.ttl",format="turtle")
