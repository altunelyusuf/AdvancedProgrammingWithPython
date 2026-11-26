import sys
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD
from rdflib.namespace import OWL
B=Namespace("http://example.org/backlog#"); EX=Namespace("http://example.org/sen0414-ch1215corr-lineage#")
ONT=URIRef("http://example.org/sen0414-ch1215corr-lineage")
prev,new="1.23.0","1.24.0"
g=Graph(); g.parse("sen0414_ch1215corr_lineage_v1_23_0.ttl")
for p in (OWL.versionInfo,OWL.versionIRI,OWL.priorVersion):
    for x in list(g.objects(ONT,p)): g.remove((ONT,p,x))
g.add((ONT,OWL.versionInfo,Literal(new))); g.add((ONT,OWL.versionIRI,URIRef(str(ONT)+"/"+new))); g.add((ONT,OWL.priorVersion,URIRef(str(ONT)+"/"+prev)))
g.add((ONT,RDFS.comment,Literal(new+" (2026-11-26): Final observations of the 22 objectives, measured from the final files (logs in 08-tooling/lineage12-closure, 08-tooling/lineage12-opening and the chapter logs folders). Three objective definitions are found wrong against the plan and carry an appended correction note (Obj12_Balloons target 104 counted two non-example keys of each examples file; Obj12_RdodiFiles and Obj12_OutsideFiles count files the mission itself plans). The review records of the four chapters are written (REVIEW_RECORD_chNN_Lineage12_v1_0_0.md).",lang="en")))
O={ # id: (value, comment)
"ExamFiles":(0,"No exam or mock-exam file in the diff from the commit before the mission stage (guard_listing_v1_0_0.log). The word exam in the path matches only examples_* code files."),
"LabFiles":(0,"No lab library, session or handout file changed (guard_listing_v1_0_0.log)."),
"OtherChapterFiles":(0,"No file under chapters 1 to 11 or 16 to 25 changed (guard_listing_v1_0_0.log)."),
"OutsideFiles":(1,"One file outside the allowed folders: 03-materials/sen0414_page_shapes_v1_0_0.ttl, the shape the Owner's run-in-order ruling needs, planned in register 1.5.0. Read by the letter the target 0 is not met; the file is the planned enforcement of a ruling (correction note on the objective)."),
"RdodiFiles":(4,"Existing rdodi files modified or deleted: 0. Four new own-version files were added, the lambda-free domain A-boxes the mission plans (ch12 1.0.3, ch13 1.0.4, ch14 1.0.4, ch15 1.0.5). Read by the letter (any diff entry) the target 0 is not met (correction note on the objective)."),
"OwnVersions":(0,"One page per chapter in the tree (9.100.0, 9.102.0, 9.104.0, 9.106.0); older drafts removed, kept in git history; version check exit 0 (own_versions_check_v1_0_0.log)."),
"RunOrderMenu":(4,"The newest page A-box of chapters 12 to 15 conforms to PageRunInOrderMenuShape (runorder_shape_v1_0_0.log)."),
"ContentChanged":(0,"Content compare logs of the four chapters are clean; changes are only those a ruling forces (analogy rows to plain meanings, notes corrected where the code or sources did not support them)."),
"Balloons":(96,"Every code slide has an explanation balloon and at least two result balloons: 23, 24, 24 and 25 slides (deck_counts_v1_0_0.log). The target 104 counted the keys of the four examples_out files, each of which holds two keys that are not examples; the decks hold 96 examples, so 104 cannot be reached by any deck (correction note on the objective)."),
"CodeInPage":(0,"Material check condition code-in-page: failed 0 of 52, 55, 52 and 57 frames (material_ch*.log)."),
"CodeParses":(0,"Material check condition code-parses: failed 0 of 52, 55, 52 and 57 frames (material_ch*.log)."),
"DeckAnalogies":(0,"No slide carries the marker Everyday picture or ANALOGY in the four decks (deck_counts_v1_0_0.log)."),
"DeckStandard":(0,"Deck standard 1.3.0: 0 failing conditions on each of the four decks (deck_standard_ch*.log)."),
"MaterialConditions":(0,"cme_material_check 1.0.2 on the newest deck and page of each chapter: 8 of 8 pass, 0 failing (material_ch*.log)."),
"NoteWords":(0,"Condition notes-words failed 0 of 48, 51, 51 and 53 slides (material_ch*.log)."),
"PageAnalogies":(0,"The words Everyday picture, analogy and analogies appear 0 times in the newest page of each chapter (page_analogy_words_v1_0_0.log)."),
"PageLambda":(0,"Material check condition no-lambda: 0 occurrences on each of the four pages (material_ch*.log)."),
"PagesPassing":(4,"Full page test 9.42.0, 0 failed: chapter 12 page 9.100.0 (414), chapter 13 page 9.102.0 (416), chapter 14 page 9.104.0 (416), chapter 15 page 9.106.0 (416); test key, not the instructor's."),
"ReaderNotes":(0,"Reader-notes check 1.0.0 exits 0, RESULT CLEAN on the four decks (reader_notes_ch*.log)."),
"ReviewVerdicts":(48,"Four review records REVIEW_RECORD_chNN_Lineage12_v1_0_0.md with 12 verdict lines each (11 accept, 1 accept with limits per chapter). Made by the building agent, not independent."),
"SpecRuns":(4,"The generic builder 2.10.0 built the newest deck of each chapter from spec_v3_2_0 (ch12), spec_v3_1_0 (ch13, ch14, ch15) without error."),
"StoryProse":(0,"Story-prose check 1.0.0: RESULT CLEAN on the four decks (story_prose_ch*.log)."),
"MissionLecture":(4,"Chapters 12 to 15 each pass the objectives of the goals G12_DeckReads, G12_PageRuns and G12_Released as observed here, read with the correction notes on three objectives."),
}
for k,(v,c) in O.items():
    o=EX["Obj12_"+k]; m=EX["Metric_Obj12_"+k]
    assert (o,None,None) in g and (m,None,None) in g,k
    ob=EX["Obs9_Obj12_"+k]
    g.add((ob,RDF.type,B.MetricObservation)); g.add((ob,B.observationFor,o)); g.add((ob,B.observesMetric,m))
    g.add((ob,B.hasObservedValue,Literal(float(v),datatype=XSD.double)))
    g.add((ob,B.observedAt,Literal("2026-11-26T14:00:00+00:00",datatype=XSD.dateTime)))
    g.add((ob,B.observedDuringCeremony,Literal(True)))
    g.add((ob,B.hasObservationMethod,Literal(str(next(g.objects(o,B.hasMeasurementQuery))))))
    g.add((ob,RDFS.label,Literal("Final observation of 2026-11-26: "+str(next(g.objects(o,RDFS.label))).split(":")[0],lang="en")))
    g.add((ob,RDFS.comment,Literal(c,lang="en")))
corr={"Balloons":"Correction note 2026-11-26 (appended; the target value stays as written): the target 104 was planned from the keys of the examples_out files, which hold 25, 26, 26 and 27 keys including two that are not examples; the four decks hold 23, 24, 24 and 25 = 96 examples, so the intent (every example has balloons) is met at 96 of 96.",
"RdodiFiles":"Correction note 2026-11-26 (appended): the query counts any diff entry; the mission plans a lambda-free A-box per chapter, which is added as a new own-version file beside the old one (as Lineage10 did). Intent (no existing research-artifact file changed) is met: 0 existing files modified or deleted; 4 files added.",
"OutsideFiles":"Correction note 2026-11-26 (appended): the page-shapes file planned in register 1.5.0 lies outside the listed folders; it is the enforcement of the run-in-order ruling. Intent (nothing unplanned changed outside the folders) is met: 1 planned file."}
for k,c in corr.items(): g.add((EX["Obj12_"+k],RDFS.comment,Literal(c,lang="en")))
for p,n in [("backlog",B),("ex",EX),("owl",OWL),("rdfs",RDFS)]: g.bind(p,n)
g.serialize("sen0414_ch1215corr_lineage_v1_24_0.ttl",format="turtle")
