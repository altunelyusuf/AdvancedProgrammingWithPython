"""Lineage13 closure (register 1.37.0 -> 1.38.0). Run from 07-lineage with the rdflib venv."""
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD
from rdflib.namespace import OWL
B=Namespace("http://example.org/backlog#"); EX=Namespace("http://example.org/sen0414-ch1620corr-lineage#")
ONT=URIRef("http://example.org/sen0414-ch1620corr-lineage")
g=Graph(); g.parse("sen0414_ch1620corr_lineage_v1_37_0.ttl")
for p in (OWL.versionInfo,OWL.versionIRI,OWL.priorVersion):
    for x in list(g.objects(ONT,p)): g.remove((ONT,p,x))
g.add((ONT,OWL.versionInfo,Literal("1.38.0"))); g.add((ONT,OWL.versionIRI,URIRef(str(ONT)+"/1.38.0"))); g.add((ONT,OWL.priorVersion,URIRef(str(ONT)+"/1.37.0")))
g.add((ONT,RDFS.comment,Literal("1.38.0 (2026-11-26): Closure of Lineage13 by partial achievement. All stories and tasks Done; 26 objectives observed (1.37.0), 25 at target, ContentChanged not at target by the letter (5 changes no ruling forces, all recorded-paragraph wordings). Per the Owner's ruling of 2026-11-26 no confirmation is needed once the conditions hold; they hold. Outcome Out_Achieved with the partial reading stated in the closure report: 07-lineage/CLOSURE_REPORT_sen0414_ch1620corr_lineage_Lineage13_v1_0_0.md. The archive step goes in the next release.",lang="en")))
for x in list(g.objects(EX.Lineage13,B.hasLineageStatus)): g.remove((EX.Lineage13,B.hasLineageStatus,x))
for x in list(g.objects(EX.Mission13,B.hasMissionOutcome)): g.remove((EX.Mission13,B.hasMissionOutcome,x))
g.add((EX.Lineage13,B.hasLineageStatus,B.LS_Achieved)); g.add((EX.Mission13,B.hasMissionOutcome,B.Out_Achieved))
c=EX.ClosureReport13
g.add((c,RDF.type,B.ClosureReport)); g.add((c,RDFS.label,Literal("Closure report: SEN0414 chapters 16 to 20 corrections",lang="en")))
g.add((c,B.closesForMission,EX.Mission13)); g.add((c,B.belongsToLineage,EX.Lineage13))
g.add((c,B.reportGeneratedAt,Literal("2026-11-26T19:45:00Z",datatype=XSD.dateTime))); g.add((c,B.closureCommittedAt,Literal("01e7548")))
g.add((c,B.hasClosureSummary,Literal("Partial achievement: 25 of 26 objectives at target on 2026-11-26. Decks of chapters 16 to 20: two result balloons on 117 of 117 code slides, analogy slides 0, think-of phrases 0, deck-standard, fit, reader-note, story-prose and material findings 0. Pages: 5 of 5 pass the full page test (100/207, 95/208, 95/207, 90/208, 91/208 widgets/features, 0 failed), 5 page A-boxes conform, run-in-order item on 5 of 5, lambda 0, analogy words 0, older drafts 0 (baseline 38). Release records 5, review verdicts 60, spec runs 5 (target 3), four formerly unmeasured items measured. Guards: exam, lab, other-chapter, outside and existing-rdodi files changed 0 (274 files, 0 modified). NOT at target: content changed beyond a ruling is 5 by the letter (recorded-paragraph wordings of chapters 16, 17, 19; chapter 18 also carries three corrected descriptions of linked pages). NOT achieved here: comparison of chapter code with the lab libraries (not in this repository, recorded for the lab lineage). Limits: reviews made by the building agent, materials not opened by the Owner, LibreOffice rendering only, Python 3.13.18, test key, links only partly re-read, lineage scripts owed to BRSF. Chapters 21 to 25, then the early chapters, are queued lineages. Full account in 07-lineage/CLOSURE_REPORT_sen0414_ch1620corr_lineage_Lineage13_v1_0_0.md.",lang="en")))
for o in g.subjects(RDF.type,B.Objective): g.add((c,B.reportsOnObjective,o))
for p,n in [("backlog",B),("ex",EX),("owl",OWL),("rdfs",RDFS)]: g.bind(p,n)
g.serialize("sen0414_ch1620corr_lineage_v1_38_0.ttl",format="turtle")
