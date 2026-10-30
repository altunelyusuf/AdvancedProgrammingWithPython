#!/usr/bin/env python3
"""sen0414_lineage_control_exam2 v1_0_0 - records the lineage agent's control of the first two executors of box 2 of the exam lineage (Lineage4) on bridge-verified evidence, the Owner's answer of 2026-10-30 about 10:20 Istanbul (30 items per paper),
that the Bloom reading and the chapter weights are NOT yet answered, and the executors' results as reported. A NEW file; ONE new register file. Same method as sen0414_lineage_control_urgent_v1_0_0.py.
  draft OUT.ttl      TestEvidence (command: sen0414_control_exam2_v1_0_0.py CHECK) and ArtifactEvidence nodes
  record BRIDGE.ttl  Done records of the verified groups (a group = a story with its two tasks)"""
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
CTL = "08-tooling/sen0414_control_exam2_v1_0_0.py"; E = "04-assessment/exams/"
G = {"distinct": (["TK4_Distinct_Build", "TK4_Distinct_Verify"], "AC4_Controlled", [E + "exam_nocopy_v1_0_0.py", E + "exam_nocopy_shapes_v1_0_0.ttl", E + "exam_nocopy_fixtures_v1_0_0.json", E + "exam_nocopy_fixtures_check_v1_0_0.py"],
                 "the near-copy rule: the executor's fixtures check exits 0 (all fixtures as expected) and the controller's own pairs (own implementation of the 4-word share, the 0.50 and 0.80 boundaries with equal and different answers, real seeds copied verbatim, an unrelated text) agree"),
     "designrev": (["TK4_DesignRev", "TK4_DesignRev_Verify"], "AC4_Controlled", [E + "exam_design_v1_1_0.md", E + "exam_design_v1_1_0.json", E + "exam_design_check_v1_1_0.py", E + "exam_item_check_v1_0_0.py", E + "exam_item_check_fixtures_v1_0_0.json"],
                   "the revised design v1_1_0: the executor's design check and item validator selftest exit 0, and the controller's own arithmetic over the blueprint (30 items, 2950 of 3240 s, 100 points, letters, Bloom) and own defective items agree")}
STORY = {"ST4_Distinct": ["distinct"], "ST4_DesignRev": ["designrev"]}
eid = lambda c: "Ev4b_Ctl_" + c
fid = lambda c, i: "Ev4b_CtlFile_%s_%d" % (c, i)
OWNER_ITEMS = ("OWNER ANSWER of 2026-10-30 about 10:20 Istanbul (relayed by the course coordinator, recorded as relayed): the number of items per SEN0414 paper is 30. The split across chapters 1, 2, 3, 4, 6, 7 and 8 as 4, 5, 5, 5, 4, 4, 3 is the lineage agent's default and is NOT yet his word. "
               "The Bloom reading (Apply and up; the executor's blueprint has Apply and up = 21 of 30 = 70 per cent, Analyze and up = 10 of 30 = 33 per cent, which would fail a majority reading) is NOT yet answered by the Owner; the coordinator asks him next.")
NOTES = {"TK4_Distinct_Build": ["RESULT OF THE EXECUTOR SEN0414-EX-nocopy (real start 2026-10-30T07:11:35Z; commit 0d01be4; recorded as reported): exam_nocopy_v1_0_0.py, exam_nocopy_shapes_v1_0_0.ttl (SHACL), fixtures and a fixtures check; 'RESULT: all fixtures as expected', exit 0 (40 PASS, 0 FAIL); the five design values 1.000, 0.942, 0.871, 0.786, 0.000 all matched; the five variants against 1,216 real seeds give the same verdicts; the SHACL shape agrees with the library on 15 fixture cases. Decisions the brief left open, made by the executor: the newest quiz_v*.json per chapter instead of quiz_v1_0_0; the banks' 'code' fields also count as seed listings; texts under 4 words give C 0; the other paper's items become seeds. Nothing was run on a real exam draft."],
         "TK4_DesignRev": ["RESULT OF THE EXECUTOR SEN0414-EX-designrev (real start 2026-10-30T07:11:35Z; commits f937cde and 097a253; recorded as reported): exam_design_v1_1_0.md and .json, exam_design_check_v1_1_0.py (43 checks PASS), exam_item_check_v1_0_0.py (rules R01 to R18) with 25 fixtures (selftest PASS 25 of 25); six kept types (mcq, predict, match, order, blank, cloze), short written dropped; 30 items, 2950 s of 3240 s; Bloom 2, 7, 11, 8, 2, 0 (Apply and up 70 per cent; Analyze and up 10 of 30 fails a majority). NOT_MEASURED, stated by the executor and not passes: a scanned or photographed sheet, a 180-degree rotation, the sheet thresholds on SEN0414 sheets, the 150 dpi frame; the page count of 4 is an estimate. Open owner questions Q1 to Q6 of the executor include the sheet title 'SEN0401 answer sheet' that the reused sheet prints."]}
def utc(x):
    return datetime.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S").astimezone().astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)
def sha(f):
    return hashlib.sha256(open(os.path.join(W.REPO, f), "rb").read()).hexdigest()
def draft(out):
    L = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    for c, (tasks, ac, files, what) in G.items():
        L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" .\n' % (eid(c), W.lit("Control by the lineage agent: " + what), ac, c, CTL, CTL, c))
        for i, f in enumerate(files):
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:%s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), ac, f, sha(f)))
    open(out, "w", encoding="utf-8").write("".join(L))
def record(bridge):
    g = rdflib.Graph(); g.parse(bridge, format="turtle"); vd = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        vd[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), utc(str(g.value(ev, B.verifiedAt))), str(g.value(ev, B.hasVerificationMethod)))
    src = W.newest(); t = open(src, encoding="utf-8").read(); n = W.now(); add = []; done = []; held = []
    ok = {c: bool(vd.get(eid(c)) and vd[eid(c)][0] and all(vd.get(fid(c, i)) and vd[fid(c, i)][0] for i in range(len(G[c][2])))) for c in G}
    for k, notes in NOTES.items():
        for nn in notes: add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(nn)))
    add.append("ex:Mission4 backlog:hasAuditNote %s .\n" % W.lit(OWNER_ITEMS))
    n0 = W.now()
    add.append('ex:Finding_DesignRevSheetsMetric a backlog:RetrospectiveFinding ;\n    rdfs:label "The design revision was asserted to move the sheets metric and cannot"@en ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:relatesToWorkItem ex:ST4_DesignRev ; backlog:hasFindingScope backlog:Scope_Methodology ;\n    backlog:hasRootCause %s ;\n    backlog:hasRemedy %s .\n' % (
        W.lit("The story ST4_DesignRev was asserted (box 2 planning, version 2.341.0) as able to move the objective Obj4_SheetsGraded (per cent of synthetic sheets graded exactly by the grading tool). Its deliverable is a revised design and two checks; no grading tool exists, so the metric cannot move by it and the reading after the story is 0, as before. The assertion was the lineage agent's, made because the design fixes the sheet that the tool will read; it confused deciding the sheet with grading it."),
        W.lit("The reading stays 0 and is recorded as 0 (not as progress). The metric is moved by the grader story ST4_Grader, which is planned after the item pools and the engine; the next planning of the exam lineage ties Obj4_SheetsGraded to that story's tasks and does not count the design revision as a mover of it. The design revision keeps its value as the input of the sheet and the grader.")))
    add.append('ex:Obs41_Obj4_NothingOut a backlog:MetricObservation ; rdfs:label "Reading after the controller re-ran the checks (ST4_Distinct, ST4_DesignRev)"@en ;\n    backlog:observesMetric ex:Met4_Out ; backlog:observationFor ex:Obj4_NothingOut ; backlog:hasObservedValue "0"^^xsd:decimal ; backlog:observedAt "%s"^^xsd:dateTime ;\n    backlog:hasObservationMethod %s .\n' % (n0, W.lit("The three commits of the two executors (0d01be4, f937cde, 097a253) touch only files under 04-assessment/exams, read with git show --stat by the controller; and the design check's own test 'nothing changed under 03-materials' passes: 0 chapter files changed by the exam lineage.")))
    add.append('ex:Obs42_Obj4_SheetsGraded a backlog:MetricObservation ; rdfs:label "Reading after the controller re-ran the checks (ST4_DesignRev)"@en ;\n    backlog:observesMetric ex:Met4_Sheets ; backlog:observationFor ex:Obj4_SheetsGraded ; backlog:hasObservedValue "0"^^xsd:decimal ; backlog:observedAt "%s"^^xsd:dateTime ;\n    backlog:hasObservationMethod %s .\n' % (n0, W.lit("No grading tool for SEN0414 sheets exists yet and no synthetic sheet has been graded: 0. The revised design reuses the SEN0401 sheet and reader; the sheet thresholds on SEN0414 sheets, a scanned or photographed sheet and a 180-degree rotation are NOT_MEASURED, not passes.")))
    ctl_s = os.path.getmtime(os.path.join(W.REPO, "08-tooling/control-exam-logs/control_exam_noc_fixtures_check_v1_0_0.py_run1.log"))
    ctl_start = datetime.datetime.fromtimestamp(ctl_s, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    for sid, groups in STORY.items():
        if not all(ok[c] for c in groups):
            held += [sid] + [k for c in groups for k in G[c][0]]; continue
        fin = max(vd[eid(c)][1] for c in groups)
        evs = []
        for c in groups: evs += [eid(c)] + [fid(c, i) for i in range(len(G[c][2]))]
        ev = ", ".join("ex:" + x for x in evs)
        for c in groups:
            add.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:%s ;\n    backlog:evidenceVerified true ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid(c), W.lit("Control by the lineage agent: " + G[c][3]), G[c][1], c, CTL, W.lit(vd[eid(c)][2]), CTL, c, vd[eid(c)][1]))
            for i, f in enumerate(G[c][2]):
                add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:%s ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), G[c][1], f, sha(f), W.lit(vd[fid(c, i)][2]), vd[fid(c, i)][1]))
        for c in groups:
            for k in G[c][0]:
                i, j = blk(t, k); b = t[i:j]
                if "backlog:hasState backlog:Ready" in b:
                    nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (ctl_start, fin, ev), 1)
                    add.append('ex:Begin8C_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started by the controller"), k, ctl_start, W.lit("The controller began its own re-run of the first check of the group at the instant of its first kept log.")))
                else:
                    nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:startedAt %s ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, ev), b, count=1)
                assert nb != b, k
                t = t[:i] + nb + t[j:]
                add.append('ex:%s backlog:lastAuditedAt "%s"^^xsd:dateTime .\n' % (k, fin))
                add.append('ex:Harness8_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (k, W.lit("Control checks for " + k), k, ", ".join("ex:" + eid(x) for x in groups)))
                add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on its own re-runs, verified by backlog_evidence_bridge_v1_1_0 at %s UTC; evidence %s." % (fin, ", ".join(evs)))))
                add.append('ex:Complete8C_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller's verdict"), k, fin, W.lit("Done on the controller's own re-runs, verified by the evidence bridge; the executor's report alone was not taken as the result.")))
                done.append(k)
        i, j = blk(t, sid); b = t[i:j]
        nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:startedAt %s ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, fin, ev), b, count=1)
        assert nb != b, sid
        t = t[:i] + nb + t[j:]; done.append(sid)
        add.append('ex:Harness8_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (sid, W.lit("Checks run for " + sid), sid, ev))
        add.append('ex:Complete8C_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (sid, W.lit(sid + " completed: its tasks are Done"), sid, fin, W.lit("All tasks of the story are Done on the controller's evidence.")))
    n2 = W.now()
    for sid in sorted(set(re.findall(r"\nex:(ST\w+) a backlog:Story", t))):
        i = t.index("\nex:%s a backlog:Story" % sid) + 1; j = t.find("\nex:", i + 1); b = t[i:j]
        m = re.search(r"backlog:hasPriorityScore ex:Score(\d+[a-z]?)_%s\b" % sid, b)
        if not m or "backlog:hasState backlog:Done" in b:
            continue
        kk = m.group(1); nk = (kk[:-1] + chr(ord(kk[-1]) + 1)) if kk[-1].isalpha() else str(int(kk) + 1); k0 = t.index("\nex:Score%s_%s a" % (kk, sid)) + 1; r0 = t[k0:t.find("\nex:", k0 + 1)]
        q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0); assert q, sid
        bv, tc, rr, size = int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4))
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:Score%s_%s" % (nk, sid), 1) + t[j:]
        val = (bv + tc + rr) / size
        add.append('ex:Score%s_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (nk, sid, val, n2, W.lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. RE-RUN on %s UTC after the controller's completions (%s): the earlier record predates them. Inputs unchanged." % (bv, tc, rr, size, val, n2, ", ".join(done)))))
    add.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit("RANKING after the controller's verdicts (%s UTC): done now %s; held %s. Next in the midterm path: the engine core (TK4_Engine_Core) and the two item pools (TK4_Items_A, TK4_Items_B), whose dependencies are now Done; the Bloom reading and the chapter weights are still the lineage agent's assumptions until the Owner answers." % (n, ", ".join(done) or "none", ", ".join(held) or "none")))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam lineage box 2: the Owner's answer (30 items per paper), the Bloom reading and the weights not yet answered, the controller's verdicts on bridge-verified evidence: Done %s%s." % (", ".join(done) or "none", ("; held: " + ", ".join(held)) if held else ""))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
