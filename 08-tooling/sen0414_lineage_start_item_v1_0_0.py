#!/usr/bin/env python3
"""sen0414_lineage_start_item v1_0_0 - records that one planned story of the SEN0414 slide lineage has been started, in a new version of the register.

Usage: sen0414_lineage_start_item_v1_0_0.py KIND CHAPTER "start time (UTC ISO)" "note: what the time is read from"
The story goes Ready -> InProgress with startedAt, its build task InProgress, and a TransitionEvent (T_Start) is recorded, as for every earlier chapter.
Refuses a story that is not Ready, or whose dependency is not Done (the framework's own start guard).
"""
__version__ = "1.0.0"
import glob, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.path.join(REPO, "07-lineage")
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+_\d+_\d+)\.ttl$", p).group(1).split("_")]


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


kind, ch, at, note = sys.argv[1:5]
cid = "Threads" if ch == "T" else "Ch%02d" % int(ch)
sid = "%s_%s" % (kind, cid); st = "ST_" + sid; tk = "TK_%s_Build" % sid
files = sorted(glob.glob(os.path.join(LIN, "sen0414_slides_lineage_v*.ttl")), key=ver)
src = files[-1]; cur = ".".join(map(str, ver(src)))
nxt = ".".join(map(str, [ver(src)[0], ver(src)[1] + 1, 0]))
out = os.path.join(LIN, "sen0414_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
assert not os.path.exists(out)
g = rdflib.Graph(); g.parse(src)
assert (EX[st], B.hasState, B.Ready) in g, st + " is not Ready"
for d in g.objects(EX[st], B.dependsOn):
    assert (d, B.hasState, B.Done) in g, "dependency %s is not Done" % d
t = open(src, encoding="utf-8").read()
m = re.search(r"ex:%s a backlog:Story.*?\n\n" % re.escape(st), t, re.S); blk = m.group(0)
nb = blk.replace("backlog:hasState backlog:Ready ;", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime ;' % at); assert nb != blk
t = t.replace(blk, nb)
m = re.search(r"ex:%s a backlog:ExecutionTask.*?\n\n?(?=ex:|\Z)" % re.escape(tk), t, re.S); blk = m.group(0)
nb = blk.replace("backlog:hasState backlog:Proposed ;", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime ;' % at); assert nb != blk
t = t.replace(blk, nb)
lab = "%s for %s" % (kind, cid)
t += ('\nex:Start_%s a backlog:TransitionEvent ; rdfs:label "%s started"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;\n    backlog:hasTransitionNote "%s" .\n' % (sid, lab, st, at, esc(note)))
t = re.sub(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(cur),
           'owl:versionInfo "%s" ; owl:versionIRI <http://example.org/sen0414-slides-lineage/%s> ; owl:priorVersion <http://example.org/sen0414-slides-lineage/%s> ;' % (nxt, nxt, cur), t, count=1)
t = t.replace('dcterms:identifier "sen0414_slides_lineage" ;', 'dcterms:identifier "sen0414_slides_lineage" ;\n    rdfs:comment "%s (%s): %s started."@en ;' % (nxt, at[:10], lab), 1)
rdflib.Graph().parse(data=t, format="turtle")
open(out, "w", encoding="utf-8").write(t)
print(os.path.basename(out))
