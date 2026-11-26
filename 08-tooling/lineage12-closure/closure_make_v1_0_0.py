from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD
from rdflib.namespace import OWL
B=Namespace("http://example.org/backlog#"); EX=Namespace("http://example.org/sen0414-ch1215corr-lineage#")
ONT=URIRef("http://example.org/sen0414-ch1215corr-lineage")
g=Graph(); g.parse("sen0414_ch1215corr_lineage_v1_24_0.ttl")
for p in (OWL.versionInfo,OWL.versionIRI,OWL.priorVersion):
    for x in list(g.objects(ONT,p)): g.remove((ONT,p,x))
g.add((ONT,OWL.versionInfo,Literal("1.25.0"))); g.add((ONT,OWL.versionIRI,URIRef(str(ONT)+"/1.25.0"))); g.add((ONT,OWL.priorVersion,URIRef(str(ONT)+"/1.24.0")))
g.add((ONT,RDFS.comment,Literal("1.25.0 (2026-11-26): Closure. All stories and tasks Done; 22 objectives observed (1.24.0), three with appended correction notes (Balloons, RdodiFiles, OutsideFiles). Per the Owner's ruling of 2026-11-26 no confirmation is needed once the conditions hold; they hold. Outcome Out_Achieved. Closure report: 07-lineage/CLOSURE_REPORT_sen0414_ch1215corr_lineage_Lineage12_v1_0_0.md. The archive step goes in the next release.",lang="en")))
for x in list(g.objects(EX.Lineage12,B.hasLineageStatus)): g.remove((EX.Lineage12,B.hasLineageStatus,x))
for x in list(g.objects(EX.Mission12,B.hasMissionOutcome)): g.remove((EX.Mission12,B.hasMissionOutcome,x))
g.add((EX.Lineage12,B.hasLineageStatus,B.LS_Achieved)); g.add((EX.Mission12,B.hasMissionOutcome,B.Out_Achieved))
c=EX.ClosureReport12
g.add((c,RDF.type,B.ClosureReport)); g.add((c,RDFS.label,Literal("Closure report: SEN0414 chapters 12 to 15 corrections",lang="en")))
g.add((c,B.closesForMission,EX.Mission12)); g.add((c,B.belongsToLineage,EX.Lineage12))
g.add((c,B.reportGeneratedAt,Literal("2026-11-26T14:30:00Z",datatype=XSD.dateTime))); g.add((c,B.closureCommittedAt,Literal("01875e3")))
g.add((c,B.hasClosureSummary,Literal("Full achievement of the work. 22 objectives observed on 2026-11-26: specs run 4 (4), failing material and deck-standard conditions 0 and 0, pages passing the full page test 4 (4; 414, 416, 416, 416 features), run-in-order menu on 4 of 4 pages, review verdicts 48 (48), analogy slides 0, page lambda 0, older page drafts 0 (baseline 24), content changed beyond a ruling 0. Three objective definitions differ from their letter and carry appended correction notes: balloons 96 against a miscounted target 104, rdodi 4 new planned A-box files and 0 existing changed, 1 planned shapes file outside the folders. Limits: reviews made by the building agent, decks and pages not opened by the Owner, rendering with LibreOffice only, recorded Python 3.13.18, test key, links and picture credits not re-checked, lineage tooling owed to BRSF. Full account in 07-lineage/CLOSURE_REPORT_sen0414_ch1215corr_lineage_Lineage12_v1_0_0.md.",lang="en")))
for o in g.subjects(RDF.type,B.Objective): g.add((c,B.reportsOnObjective,o))
for p,n in [("backlog",B),("ex",EX),("owl",OWL),("rdfs",RDFS)]: g.bind(p,n)
g.serialize("sen0414_ch1215corr_lineage_v1_25_0.ttl",format="turtle")
