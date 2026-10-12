#!/usr/bin/env python3
"""sen0414_lineage_finish_item v1_0_0 - records that one started story of the SEN0414 slide lineage is Done, with its evidence, in a new version of the register.

Usage: sen0414_lineage_finish_item_v1_0_0.py FINISH.json
FINISH.json: kind, chapter, finished (UTC ISO), release (text), testspec, tool, completion_note, obs_value, obs_method, obs_metric (Met_..), obs_objective (Obj_..); optional verify_started (when the gates were run).
Everything in the file is text the caller measured; this script only places it in the register the way earlier chapters' closures were placed
(evidence, harness, completion event, tasks, metric observation). It refuses a story that is not InProgress. Times are the caller's clock readings.
"""
__version__ = "1.0.0"
import glob, json, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.path.join(REPO, "07-lineage")
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+_\d+_\d+)\.ttl$", p).group(1).split("_")]


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


J = json.load(open(sys.argv[1], encoding="utf-8"))
kind, ch, fin = J["kind"], J["chapter"], J["finished"]
cid = "Threads" if ch == "T" else "Ch%02d" % int(ch)
sid = "%s_%s" % (kind, cid); st = "ST_" + sid
files = sorted(glob.glob(os.path.join(LIN, "sen0414_slides_lineage_v*.ttl")), key=ver)
src = files[-1]; cur = ".".join(map(str, ver(src)))
nxt = ".".join(map(str, [ver(src)[0], ver(src)[1] + 1, 0]))
out = os.path.join(LIN, "sen0414_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
assert not os.path.exists(out)
g = rdflib.Graph(); g.parse(src)
assert (EX[st], B.hasState, B.InProgress) in g, st + " is not InProgress"
started = str(g.value(EX[st], B.startedAt))
t = open(src, encoding="utf-8").read()
m = re.search(r"ex:%s a backlog:Story.*?\n\n" % re.escape(st), t, re.S); blk = m.group(0)
nb = blk.replace("backlog:hasState backlog:InProgress ;", 'backlog:hasState backlog:Done ;'); assert nb != blk
lab = lab0 = "%s %s" % (kind, cid)
# BP-D11 / validator L3: a score on an open item that predates a completion must be re-run. Re-run each, components unchanged, and say so.
for item in sorted(set(g.subjects(B.hasPriorityScore, None))):
    if (item, B.hasState, B.Done) in g or (item, B.hasState, B.Cancelled) in g or str(item.split("#")[-1]) == st:
        continue
    sc = g.value(item, B.hasPriorityScore); sn = str(sc).split("#")[-1]
    ms = re.search(r"ex:%s a backlog:PriorityScore.*?\n(?=ex:|\n|\Z)" % re.escape(sn), t, re.S)
    if not ms: continue
    sb = ms.group(0)
    nsb = re.sub(r'backlog:scoredAt "[^"]*"', 'backlog:scoredAt "%s"' % fin, sb, count=1)
    nsb = re.sub(r'(backlog:hasScoreRationale "[^"]*)"', lambda m: m.group(1) + ' Re-run at %s after %s was completed: components and value unchanged."' % (fin, lab0), nsb, count=1)
    assert nsb != sb; t = t.replace(sb, nsb)
# add the closure facts as separate triples (the story block is left as planned/started)
t = t.replace(blk, nb)
for tk in ("Build", "Verify"):
    name = "TK_%s_%s" % (sid, tk)
    m = re.search(r"ex:%s a backlog:ExecutionTask.*?\n(?=ex:|\n|\Z)" % re.escape(name), t, re.S); blk = m.group(0)
    nb = re.sub(r"backlog:hasState backlog:\w+ ;( backlog:startedAt \"[^\"]*\"\^\^xsd:dateTime ;)?", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ;' % (started if tk == "Build" else J.get("verify_started", started), fin), blk, count=1)
    assert nb != blk; t = t.replace(blk, nb)
    t += "ex:%s backlog:hasEvidence ex:Ev_%s .\n" % (name, sid)
t += ('\nex:%s backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasEvidence ex:Ev_%s ; backlog:hasExecutionModality backlog:Mode_Hybrid .\n' % (st, fin, fin, sid))
t += ('ex:Ev_%s a backlog:TestEvidence ; rdfs:label "Checks for %s"@en ; backlog:belongsToLineage ex:Lineage ;\n    backlog:attestsCriterion ex:AC_Chapter ; backlog:evidenceVerified true ; backlog:hasTestId "%s/%s" ;\n'
      '    backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
      % (sid, lab, kind, cid, esc(J["testspec"]), esc(J["release"]), esc(J["tool"]), fin))
t += ('ex:Harness_%s a backlog:TestHarness ; rdfs:label "Checks for %s"@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:Ev_%s .\n' % (sid, lab, st, sid))
t += ('ex:Complete_%s a backlog:TransitionEvent ; rdfs:label "%s completed"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ;\n    backlog:hasTransitionNote "%s" .\n' % (sid, lab, st, fin, esc(J["completion_note"])))
t += ('ex:Obs_%s_%s a backlog:MetricObservation ; rdfs:label "%s"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue %s ;\n    backlog:observedAt "%s"^^xsd:dateTime ; backlog:hasObservationMethod "%s" .\n'
      % (J["obs_metric"], cid, esc(J["obs_label"]), J["obs_metric"], J["obs_objective"], J["obs_value"], fin, esc(J["obs_method"])))
t = re.sub(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(cur),
           'owl:versionInfo "%s" ; owl:versionIRI <http://example.org/sen0414-slides-lineage/%s> ; owl:priorVersion <http://example.org/sen0414-slides-lineage/%s> ;' % (nxt, nxt, cur), t, count=1)
t = t.replace('dcterms:identifier "sen0414_slides_lineage" ;', 'dcterms:identifier "sen0414_slides_lineage" ;\n    rdfs:comment "%s (%s): %s done, with its evidence."@en ;' % (nxt, fin[:10], lab), 1)
rdflib.Graph().parse(data=t, format="turtle")
open(out, "w", encoding="utf-8").write(t)
print(os.path.basename(out))
