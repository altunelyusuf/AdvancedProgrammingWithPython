#!/usr/bin/env python3
"""register_step 1.1.0 (adds the optional EXTRA.ttl; 1.0.0 was used for registers 1.6.0 to 1.9.0) (Lineage13, 2026-11-26): writes the next merged register file of Lineage13 from the newest one(s). A lineage's own script, disclosed (a tool gap handed to BRSF with the others).
Modes:  register_step_v1_1_0.py merge OUT_VERSION COMMENT MOVES.json      all delta files 1.0.0..1.5.0 -> one merged file (hasState, hasLineageStatus, hasMissionOutcome, checkpointDate, hasForecastDate,
                                                                               hasForecastRationale, hasTargetValue, metricTarget, expectedValue take their latest value; everything else is kept)
        register_step_v1_1_0.py step  OUT_VERSION COMMENT MOVES.json [EXTRA.ttl]   newest merged file -> next merged file (git rm of the old one by the caller); EXTRA.ttl is added as it is
MOVES.json: {"set": [[subject, predicate, object, kind]], "add": [[subject, predicate, object, kind]]}   kind: iri | text | date | datetime; subject and object (iri) as ex:Name or backlog:Name.
'set' replaces every value of the predicate on the subject; 'add' adds one."""
import glob, json, os, re, sys
from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, OWL, XSD, DCTERMS
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(R, "07-lineage"); P = "sen0414_ch1620corr_lineage_v"
EX = Namespace("http://example.org/sen0414-ch1620corr-lineage#"); BK = Namespace("http://example.org/backlog#")
ONT = URIRef("http://example.org/sen0414-ch1620corr-lineage")
LATEST = [BK.hasState, BK.hasLineageStatus, BK.hasMissionOutcome, BK.checkpointDate, BK.hasForecastDate, BK.hasForecastRationale, BK.hasTargetValue, BK.metricTarget, BK.expectedValue]
ver = lambda f: tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", f).groups())
def term(s, kind=None):
    if kind is None or kind == "iri":
        return EX[s[3:]] if s.startswith("ex:") else BK[s[8:]]
    if kind == "date": return Literal(s, datatype=XSD.date)
    if kind == "datetime": return Literal(s, datatype=XSD.dateTime)
    return Literal(s, lang="en") if kind == "texten" else Literal(s)
mode, outv, comment, movesf = sys.argv[1:5]
extra = sys.argv[5] if len(sys.argv) > 5 else None   # optional Turtle file whose statements are added (planning events, tasks)
moves = json.load(open(movesf))
files = sorted(glob.glob(os.path.join(D, P + "*.ttl")), key=ver)
g = Graph(); comments = []
if mode == "merge":
    for f in files:
        h = Graph(); h.parse(f)
        comments += [str(o) for o in h.objects(ONT, RDFS.comment)]
        for s, p in {(s, p) for s, p, o in h if p in LATEST}:
            g.remove((s, p, None))
        for t in h:
            if t[0] != ONT: g.add(t)
else:
    g.parse(files[-1]); comments = [str(o) for o in g.objects(ONT, RDFS.comment)]
    g.remove((ONT, None, None))
prior = ver(files[-1])
if extra: g.parse(extra, format="turtle")
for s, p, o, k in moves.get("set", []):
    g.remove((term(s), term(p), None)); g.add((term(s), term(p), term(o, k)))
for s, p, o, k in moves.get("add", []):
    g.add((term(s), term(p), term(o, k)))
g.add((ONT, RDF.type, OWL.Ontology)); g.add((ONT, RDFS.label, Literal("Fresh narrow lineage: SEN0414 Chapters 16 to 20 corrections", lang="en")))
g.add((ONT, DCTERMS.identifier, Literal("sen0414_ch1620corr_lineage")))
for c in comments + [comment]: g.add((ONT, RDFS.comment, Literal(c, lang="en")))
g.add((ONT, OWL.versionInfo, Literal(outv))); g.add((ONT, OWL.versionIRI, URIRef(str(ONT) + "/" + outv)))
g.add((ONT, OWL.priorVersion, URIRef(str(ONT) + "/%d.%d.%d" % prior)))
g.bind("backlog", BK); g.bind("ex", EX); g.bind("rdfs", RDFS); g.bind("owl", OWL); g.bind("xsd", XSD); g.bind("dcterms", DCTERMS)
out = os.path.join(D, P + outv.replace(".", "_") + ".ttl")
if os.path.exists(out): sys.exit("refusing to overwrite " + out)
g.serialize(out, format="turtle"); print("wrote", out, len(g), "statements")
if mode == "merge":
    for f in files: print("merged:", os.path.basename(f))
