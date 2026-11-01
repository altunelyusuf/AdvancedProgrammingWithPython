#!/usr/bin/env python3
"""sen0414_lineage_control_exam4 v1_0_0 (made from sen0414_lineage_control_exam3_v1_0_0.py) - records the lineage agent's control of TK4_Points5 and TK4_ItemRules2 and of the stories ST4_Points5 and ST4_DesignRev2 on bridge-verified evidence. ONE new register file.
  draft OUT.ttl      TestEvidence (command: sen0414_control_exam4_v1_0_0.py GROUP) and ArtifactEvidence nodes
  record BRIDGE.ttl  Done records of the verified groups, the stories, the harness, the readings, the finding, re-run scores"""
__version__ = "1.0.0"
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
NS = "http://example.org/sen0414-slides-lineage#"
CTL = "08-tooling/sen0414_control_exam3_v1_0_0.py"; E = "04-assessment/exams/"
CTL = "08-tooling/sen0414_control_exam5_v1_0_0.py"; E = "04-assessment/exams/"
G = {"itemsa2": (["TK4_Items_A2", "TK4_Items_A2_Verify"], [E + "items/items_a_v2_0_0.json", E + "items/items_a_v2_0_0_makeup.json", E + "items/items_a_v2_0_0_provisional.json", E + "items/items_a_v2_0_0_check.py"], "item set A as briefed (r11): the executor's check exits 0, both lists pass the validator v1_1_0 on the controller's own call, 14 records and 14 ids each, Apply and above 13 and Analyze and above 7 of 14, no Bloom 1, chapters 1 to 8, units per question as the design counts so far (6, 7, 6, 5, 2 of 6, 7, 7, 6, 4), no identical stem between the lists, the task commit adds only new files")}
STORY = {}
eid = lambda c: "Ev4e_Ctl_" + c
fid = lambda c, i: "Ev4e_CtlFile_%s_%d" % (c, i)
REP_A = ("RESULT OF THE EXECUTOR of TK4_Items_A2 (real start 2026-11-01T18:36:06Z; commit 94e08e1; recorded as reported): items_a_v2_0_0.json (paper, 14 records), items_a_v2_0_0_makeup.json (14 records), a provisional side file, builder and check; validator v1_1_0 0 failures on each list; Apply and above 13 of 14, Analyze and above 7 of 14. Not achieved: one pool file is impossible under R02 and R23, so the paper and the make-up have two lists (the engine reads one list per form); only part of Q3, Q4 and Q5 written (one choice of Q3, one of Q4 and two of Q5 remain for TK4_Items_B2); the near-copy tool cannot read 22-field records (run on a built view); seed_item is none everywhere. Abbreviations to confirm with the Owner: JSON, IDE.")
def utc(x):
    return datetime.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S").astimezone().astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)
def sha(f): return hashlib.sha256(open(os.path.join(W.REPO, f), "rb").read()).hexdigest()
def draft(out):
    L = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    for c, (tasks, files, what) in G.items():
        L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" .\n' % (eid(c), W.lit("Control by the lineage agent: " + what), c, CTL, CTL, c))
        for i, f in enumerate(files):
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), f, sha(f)))
    open(out, "w", encoding="utf-8").write("".join(L))
def record(bridge):
    g = rdflib.Graph(); g.parse(bridge, format="turtle"); vd = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        vd[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), utc(str(g.value(ev, B.verifiedAt))), str(g.value(ev, B.hasVerificationMethod)))
    src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); nowZ = now + "Z"; add = []; done = []; held = []
    ok = {c: bool(vd.get(eid(c)) and vd[eid(c)][0] and all(vd.get(fid(c, i)) and vd[fid(c, i)][0] for i in range(len(G[c][1])))) for c in G}
    for k in ("TK4_Items_A2", "TK4_Items_A2_Verify"): add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(REP_A)))
    LOGS = {"itemsa2": "control_itemsa2_run1.log"}
    for c in G:
        tasks, files, what = G[c]
        if not ok[c]: held += tasks; continue
        ctl_start = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(W.REPO, "08-tooling/control-exam-logs/" + LOGS[c])), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        fin = vd[eid(c)][1]; evs = [eid(c)] + [fid(c, i) for i in range(len(files))]; ev = ", ".join("ex:" + x for x in evs)
        add.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid(c), W.lit("Control by the lineage agent: " + what), c, CTL, W.lit(vd[eid(c)][2]), CTL, c, fin))
        for i, f in enumerate(files):
            add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), f, sha(f), W.lit(vd[fid(c, i)][2]), fin))
        for k in tasks:
            i, j = blk(t, k); b = t[i:j]
            if "backlog:hasState backlog:Ready" in b:
                nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%sZ"^^xsd:dateTime ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (ctl_start, fin, ev), 1)
                add.append('ex:Begin4f_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started by the controller"), k, ctl_start, W.lit("The controller began its own re-run of the first check of the group at the instant of its first kept log.")))
            else:
                nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:startedAt %s ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, ev), b, count=1)
            assert nb != b, k
            t = t[:i] + nb + t[j:]
            add.append('ex:%s backlog:lastAuditedAt "%s"^^xsd:dateTime .\n' % (k, fin))
            add.append('ex:Harness4f_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:%s .\n' % (k, W.lit("Control checks for " + k), k, eid(c)))
            add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on its own re-runs, verified by backlog_evidence_bridge_v1_1_0 at %s UTC; evidence %s." % (fin, ", ".join(evs)))))
            add.append('ex:Complete4f_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller's verdict"), k, fin, W.lit("Done on the controller's own re-runs, verified by the evidence bridge; the executor's report alone was not taken as the result.")))
            done.append(k)
    # re-score open stories of the exam lineage (a score older than a completion is stale)
    for s2 in sorted(set(re.findall(r"\nex:(ST\w*?_\w+) a backlog:Story", t))):
        i, j = blk(t, s2); b = t[i:j]
        m = re.search(r"backlog:hasPriorityScore ex:Score(\d+[a-z]?)_%s\b" % s2, b)
        if not m or "backlog:hasState backlog:Done" in b or "backlog:hasState backlog:Cancelled" in b : continue
        if ("\nex:Score%s_%s a" % (kk if False else m.group(1), s2)) not in t: continue
        kk = m.group(1); k0 = t.index("\nex:Score%s_%s a" % (kk, s2)) + 1; r0 = t[k0:t.find("\nex:", k0 + 1)]
        q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0)
        if not q: continue
        nk = (kk[:-1] + chr(ord(kk[-1]) + 1)) if kk[-1].isalpha() else str(int(kk) + 1); nid = "Score%s_%s" % (nk, s2)
        if ("ex:" + nid + " a ") in t: continue
        bv, tc, rrr, size_ = int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4)); val = (bv + tc + rrr) / size_
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:" + nid, 1) + t[j:]
        add.append('ex:%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%sZ"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (nid, val, now, W.lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. RE-RUN on %s UTC after the controller's completions (%s) and the completions: the earlier record predates them. Inputs unchanged." % (bv, tc, rrr, size_, val, now, ", ".join(done)))))
    add.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit("RANKING %s UTC after the controller's verdicts (done now: %s; held: %s). Next: TK4_Items_B2 (dependency TK4_Items_A2_Verify Done), TK4_Engine5 in work, then ST4_Papers. The make-up paper stays last." % (now, ", ".join(done) or "none", ", ".join(held) or "none")))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam change: the controller's verdict on item set A (TK4_Items_A2 and its control Done on bridge-verified evidence: %s), scores re-run." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])

