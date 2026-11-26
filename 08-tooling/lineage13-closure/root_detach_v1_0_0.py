"""Register root of Lineage13 stops belonging to the lineage (archival partition rule); 1.38.0 -> 1.39.0. Run from 07-lineage."""
from rdflib import Graph, Namespace, URIRef, Literal, RDFS
from rdflib.namespace import OWL
B=Namespace("http://example.org/backlog#"); EX=Namespace("http://example.org/sen0414-ch1620corr-lineage#")
ONT=URIRef("http://example.org/sen0414-ch1620corr-lineage")
g=Graph(); g.parse("sen0414_ch1620corr_lineage_v1_38_0.ttl")
for p in (OWL.versionInfo,OWL.versionIRI,OWL.priorVersion):
    for x in list(g.objects(ONT,p)): g.remove((ONT,p,x))
g.add((ONT,OWL.versionInfo,Literal("1.39.0"))); g.add((ONT,OWL.versionIRI,URIRef(str(ONT)+"/1.39.0"))); g.add((ONT,OWL.priorVersion,URIRef(str(ONT)+"/1.38.0")))
g.add((ONT,RDFS.comment,Literal("1.39.0 (2026-11-26): The register root no longer belongs to the lineage: it keeps only its label, identifier and isRegisterRoot, as the archival partition rule requires (the form of Lineage12 1.27.0); its definition of done and commitment stay on the backlog of Lineage13, and the commitment belongs to the lineage.",lang="en")))
r=EX.Register_Ch1620corr
for p in (B.belongsToLineage,B.hasCommitment,B.appliesDefinitionOfDone):
    for x in list(g.objects(r,p)): g.remove((r,p,x))
g.add((EX.Commit13,B.belongsToLineage,EX.Lineage13))
for p,n in [("backlog",B),("ex",EX),("owl",OWL),("rdfs",RDFS)]: g.bind(p,n)
g.serialize("sen0414_ch1620corr_lineage_v1_39_0.ttl",format="turtle")
