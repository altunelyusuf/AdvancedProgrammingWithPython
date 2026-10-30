#!/usr/bin/env python3
"""sen0414_lineage_control_exam v1_1_0 (over v1_0_0, which stays as committed: adds the T_Start/T_Complete transitions, the Done stories and the re-score of the open stories) - records the controller's evidence for the exam lineage (Lineage4).
  draft CHECKS OUT.ttl      CHECKS = comma list of points_a, points_b, design: TestEvidence (command: sen0414_control_exam_v1_0_0.py CHECK) and ArtifactEvidence nodes, no evidenceVerified
  record CHECKS BRIDGE.ttl  the Build task of each check whose evidence the bridge verified goes Done (finishedAt = the bridge's clock), then its Verify task (started at env CTL_START, the clock of the controller's first run)
The bridge (backlog_evidence_bridge_v1_1_0.py) runs: python3 08-tooling/sen0414_control_exam_v1_0_0.py CHECK  (the system python3 reads the decks)."""
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
CTL = "08-tooling/sen0414_control_exam_v1_0_0.py"
E = "04-assessment/exams/"
INFO = {"points_a": ("TK4_Points_A", [E + "critical_points_ch01_04_v1_0_0.json", E + "critical_points_ch01_04_not_found_v1_0_0.md"], "the critical points of chapters 1 to 4: structure, sources and places re-checked by the controller (every point cites an existing file and place, the not-found list has a section per chapter, no chapter file changed, everything committed)"),
        "points_b": ("TK4_Points_B", [E + "critical_points_ch06_08_v1_0_0.json", E + "critical_points_ch06_08_not_found_v1_0_0.md"], "the critical points of chapters 6 to 8: structure, sources and places re-checked by the controller (every point cites an existing file and place, the not-found list has a section per chapter, no chapter file changed, everything committed)"),
        "design": ("TK4_Design", [E + "exam_design_v1_0_0.md", E + "exam_design_v1_0_0.json"], "the design of the paper: keys, decisions with reasons, the 17 engine types kept or dropped, blueprint arithmetic, answer sheet and grading parts re-checked by the controller")}
STORY = {"points_a": "ST4_Points_A", "points_b": "ST4_Points_B", "design": "ST4_Design"}
eid = lambda c: "Ev4_Ctl_" + c
fid = lambda c, i: "Ev4_CtlFile_%s_%d" % (c, i)
def draft(checks, out):
    L = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    for c in checks:
        L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" .\n' % (eid(c), W.lit("Control by the lineage agent: " + INFO[c][2]), c, CTL, CTL, c))
        for i, f in enumerate(INFO[c][1]):
            h = hashlib.sha256(open(os.path.join(W.REPO, f), "rb").read()).hexdigest()
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), f, h))
    open(out, "w", encoding="utf-8").write("".join(L))
def utc(x):
    return datetime.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S").astimezone().astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i)
    return i, (len(t) if j < 0 else j)
def record(checks, bridge):
    g = rdflib.Graph(); g.parse(bridge, format="turtle"); vd = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        vd[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), utc(str(g.value(ev, B.verifiedAt))), str(g.value(ev, B.hasVerificationMethod)))
    src = W.newest(); t = open(src, encoding="utf-8").read(); add = []; done = []; held = []
    start = os.environ["CTL_START"]
    for c in checks:
        tk = INFO[c][0]; vk = tk + "_Verify"; n = len(INFO[c][1])
        ok = vd.get(eid(c)) and vd[eid(c)][0] and all(vd.get(fid(c, i)) and vd[fid(c, i)][0] for i in range(n))
        if not ok:
            held += [tk, vk]; continue
        fin = vd[eid(c)][1]; assert start < fin
        ev = ", ".join("ex:" + x for x in [eid(c)] + [fid(c, i) for i in range(n)])
        add.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid(c), W.lit("Control by the lineage agent: " + INFO[c][2]), c, CTL, W.lit(vd[eid(c)][2]), CTL, c, fin))
        for i, f in enumerate(INFO[c][1]):
            h = hashlib.sha256(open(os.path.join(W.REPO, f), "rb").read()).hexdigest()
            add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), f, h, W.lit(vd[fid(c, i)][2]), vd[fid(c, i)][1]))
        for k in (tk, vk):
            i, j = blk(t, k); b = t[i:j]
            if k == tk:
                nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:startedAt %s ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, ev), b, count=1)
            else:
                nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (start, fin, ev), 1)
            assert nb != b, k
            t = t[:i] + nb + t[j:]
            add.append('ex:%s backlog:lastAuditedAt "%s"^^xsd:dateTime .\n' % (k, fin))
            add.append('ex:Harness4_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:%s .\n' % (k, W.lit("Control checks for " + k), k, eid(c)))
            add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on %s UTC: %s. Evidence ex:%s, verified by backlog_evidence_bridge_v1_1_0." % (fin, INFO[c][2], eid(c)))))
            done.append(k)
            if k == vk:
                add.append('ex:Begin4T_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started by the controller"), k, start, W.lit("The controller began its own re-run of the build task's check.")))
            add.append('ex:Complete4T_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller's verdict"), k, fin, W.lit("Done on the controller's own re-run, verified by the evidence bridge (ex:%s); the executor's report alone was not taken as the result." % eid(c))))
        sid = STORY[c]; i, j = blk(t, sid); b = t[i:j]
        nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:startedAt %s ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, fin, ev), b, count=1)
        assert nb != b, sid
        t = t[:i] + nb + t[j:]; done.append(sid)
        add.append('ex:Complete4T_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (sid, W.lit(sid + " completed: both of its tasks are Done"), sid, fin, W.lit("Both tasks of the story are Done on the controller's evidence.")))
    if done:
        n2 = W.now(); 
        for sid in sorted(set(re.findall(r"\nex:(ST\w+) a backlog:Story", t))):
            i = t.index("\nex:%s a backlog:Story" % sid) + 1; j = t.find("\nex:", i + 1); b = t[i:j]
            m = re.search(r"backlog:hasPriorityScore ex:Score(\d+)_%s\b" % sid, b)
            if not m or "backlog:hasState backlog:Done" in b:
                continue
            kk = int(m.group(1)); k0 = t.index("\nex:Score%d_%s a" % (kk, sid)) + 1; r0 = t[k0:t.find("\nex:", k0 + 1)]
            q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0); assert q, sid
            bv, tc, rr, size = int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4))
            t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:Score%d_%s" % (kk + 1, sid), 1) + t[j:]
            val = (bv + tc + rr) / size
            add.append('ex:Score%d_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (kk + 1, sid, val, n2, W.lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. RE-RUN on %s UTC after the controller's completions (%s): the earlier record predates them. Inputs unchanged." % (bv, tc, rr, size, val, n2, ", ".join(done)))))
    out = W.write_new(src, t + "\n" + "".join(add), "Control by the lineage agent on bridge-verified evidence: Done %s%s." % (", ".join(done) or "none", ("; held: " + ", ".join(held)) if held else ""))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2].split(","), sys.argv[3])
    else: record(sys.argv[2].split(","), sys.argv[3])
