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
CTL = "08-tooling/sen0414_control_exam4_v1_0_0.py"; E = "04-assessment/exams/"
G = {"points5": (["TK4_Points5", "TK4_Points5_Verify"], [E + "critical_points_ch05_v1_0_0.json", E + "critical_points_ch05_not_found_v1_0_0.md"], "the critical points of chapter 5 as briefed: the controller re-ran the structure and source checks of the points files for chapter 5 (exactly the keys, chapter 5, at least 4 points, every source file and place exists, the not-found list exists), spot-checked slide-based points against the deck v3_1_0, and found only new files in the task commit"),
     "itemrules2": (["TK4_ItemRules2", "TK4_ItemRules2_Verify"], [E + "exam_item_check_v1_1_0.py", E + "exam_item_check_fixtures_v1_1_0.json"], "the item validator v1_1_0 as briefed: both self-tests (v1_0_0 and v1_1_0) pass, the 66 fixtures are present, and the controller's own mutations of a valid item are each caught by the intended rule (R05, R24, R22, R23, R19, R21, R01); the task commit adds only new files")}
STORY = {"ST4_Points5": ["points5"], "ST4_DesignRev2": ["itemrules2"]}
eid = lambda c: "Ev4e_Ctl_" + c
fid = lambda c, i: "Ev4e_CtlFile_%s_%d" % (c, i)
REP_P = ("RESULT OF THE EXECUTOR of TK4_Points5 (real start 2026-11-01T17:14:35Z; commit 3ecf1d4; recorded as reported): critical_points_ch05_v1_0_0.json with 44 points and critical_points_ch05_not_found_v1_0_0.md. 21 of the 44 rest on corpus or story only (not on the deck); the newer chapter 5 deck is not committed yet, so the points name deck v3.1.0 and must be re-checked when it commits.")
REP_I = ("RESULT OF THE EXECUTOR of TK4_ItemRules2 (real start 2026-11-01T17:14:35Z; commit fe726d3; recorded as reported): exam_item_check_v1_1_0.py and exam_item_check_fixtures_v1_1_0.json with 66 fixtures; self-tests of v1_0_0 and v1_1_0 PASS; rules R19 to R24 added, R15 retired. Open points the executor named: the shape of the match and order records (per premise or one record) is settled in the briefs of TK4_Engine5 and TK4_Items_A2; chapter 5 items cannot pass R06 and R07 before the points file is controlled (it is now); the 24 abbreviation full forms are standard expansions not checked against the course.")
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
    for k in ("TK4_Points5", "TK4_Points5_Verify", "ST4_Points5"): add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(REP_P)))
    for k in ("TK4_ItemRules2", "TK4_ItemRules2_Verify"): add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(REP_I)))
    LOGS = {"points5": "control_points5_run1.log", "itemrules2": "control_itemrules2_run1.log"}
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
    for sid, groups in STORY.items():
        kids = {"ST4_Points5": ["TK4_Points5", "TK4_Points5_Verify"], "ST4_DesignRev2": ["TK4_Design2", "TK4_Design2_Verify", "TK4_ItemRules2", "TK4_ItemRules2_Verify"]}[sid]
        if not all(ok[c] for c in groups): held.append(sid); continue
        fin = max(vd[eid(c)][1] for c in groups); evs = []
        for c in groups: evs += [eid(c)] + [fid(c, i) for i in range(len(G[c][1]))]
        if sid == "ST4_DesignRev2": evs = ["Ev4e_Ctl_design2"] + ["Ev4e_CtlFile_design2_%d" % i for i in range(3)] + evs
        i, j = blk(t, sid); b = t[i:j]
        nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:startedAt %s ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:lastAuditedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, fin, ", ".join("ex:" + x for x in evs)), b, count=1)
        assert nb != b, sid; t = t[:i] + nb + t[j:]
        add.append('ex:Complete4f_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "Done with its tasks on the controller\'s verdict." .\n' % (sid, W.lit(sid + " completed on the controller's verdict"), sid, fin)); done.append(sid)
        add.append('ex:Harness4f_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (sid, W.lit("Control checks for " + sid), sid, ", ".join("ex:" + x for x in evs)))
    obsT = max(vd[eid(c)][1] for c in G if ok[c]) if any(ok.values()) else now
    if ok["points5"]:
        add.append('ex:Obs44_Obj4_PointsListed a backlog:MetricObservation ; rdfs:label "Reading after the controller re-ran the checks (ST4_Points5)"@en ;\n    backlog:observesMetric ex:Met4_Points ; backlog:observationFor ex:Obj4_PointsListed ; backlog:hasObservedValue "8"^^xsd:decimal ; backlog:observedAt "%sZ"^^xsd:dateTime ;\n    backlog:hasObservationMethod "Chapters with critical points collected and a stated list of what could not be found, read after the controller\'s own re-runs of the chapter 5 task: the seven earlier chapters plus chapter 5 = 8 (the target of 7 was set before chapter 5 entered the exams)." .\n' % max(obsT, now))
    if ok["itemrules2"] and ok["points5"]:
        add.append('ex:Finding_DesignPapersMetric a backlog:RetrospectiveFinding ;\n    rdfs:label "The design story was asserted to move the papers metric and cannot"@en ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:relatesToWorkItem ex:ST4_DesignRev2 ; backlog:hasFindingScope backlog:Scope_Methodology ;\n    backlog:hasRootCause %s ;\n    backlog:hasRemedy %s .\n' % (W.lit("The story ST4_DesignRev2 was asserted (version 2.353.0) as able to move the objective Obj4_PapersBuilt. Its deliverables are the design v1_2_0 and the item validator v1_1_0, which are inputs of a paper, not a paper; no complete printed paper with its key exists, so the metric cannot move by it and the reading stays 0. The assertion was the lineage agent's and repeats the error recorded for ST4_Cover."), W.lit("The reading stays 0 and is recorded as 0 (Obs44_Obj4_PapersBuilt). The metric is moved by ST4_Papers; ST4_Engine and ST4_Items2 are inputs of it and are read the same way when they reach Done.")))
        add.append('ex:Obs44_Obj4_PapersBuilt a backlog:MetricObservation ; rdfs:label "Reading after the controller re-ran the checks (ST4_DesignRev2)"@en ;\n    backlog:observesMetric ex:Met4_Papers ; backlog:observationFor ex:Obj4_PapersBuilt ; backlog:hasObservedValue "0"^^xsd:decimal ; backlog:observedAt "%sZ"^^xsd:dateTime ;\n    backlog:hasObservationMethod "No complete printed paper with its key exists yet: 0 (the cover renderer, the design and the item validator are parts, not a paper)." .\n' % max(obsT, now))
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
    add.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit("RANKING %s UTC after the controller's verdicts (done now: %s; held: %s): ST4_Points5 and ST4_DesignRev2 Done. Next: ST4_Engine (TK4_Engine5, dependency TK4_ItemRules2_Verify Done) and ST4_Items2 (TK4_Items_A2, dependencies TK4_ItemRules2_Verify and TK4_Points5_Verify Done), then ST4_Papers. The make-up paper stays last." % (now, ", ".join(done) or "none", ", ".join(held) or "none")))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam change: the controller's verdicts on the chapter 5 critical points and the item validator v1_1_0 (TK4_Points5, TK4_ItemRules2 and their controls, ST4_Points5 and ST4_DesignRev2 Done on bridge-verified evidence: %s), scores re-run." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])

