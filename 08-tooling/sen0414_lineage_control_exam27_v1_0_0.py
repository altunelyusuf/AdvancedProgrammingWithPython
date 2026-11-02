#!/usr/bin/env python3
"""sen0414_lineage_control_exam27 v1_0_0 (made from sen0414_lineage_control_exam23_v1_0_0.py) - records the lineage agent's control of TK4_Rev_Papers (parts 1 to 4) and TK4_Rev_EngineFix, each with its verification, on bridge-verified evidence. ONE new register file. The designed files live in the private CME repository, so the evidence nodes name the controller and its kept logs (both in this repository); the logs print the SHA-256 of the controlled CME files.
  draft OUT.ttl      TestEvidence (command: sen0414_control_exam25_v1_0_0.py MODE) and ArtifactEvidence nodes
  record BRIDGE.ttl  Done records of the tasks, the four Papers executors (instances, briefs, starts), the audit notes, re-run scores"""
__version__ = "1.0.0"
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
CTL = "08-tooling/sen0414_control_exam25_v1_0_0.py"
LD = "08-tooling/control-exam-logs/"
G = {"revfix": ([CTL, LD + "control_revfix_run3.log", LD + "control_revfix_measure_run1.log", LD + "control_revfix_sheetcheck_run1.log"], "the corrections version of the printed midterm in the private CME repository (commit ac82656, only new files; the files the Owner printed are untouched by SHA-256); my own controller: the build files equal the first version's byte for byte (7 of 7), my own conversion of the new paper .docx gives 5 pages with the same text as the committed PDF, type 10.0 pt or larger, no cover overshoot, last-page slack 333 pt (page 2 has 20.7 pt), 30 answer spaces, no sub-question split, all 14 key letters print the correct option text, the marking tool gives 110 and 0; the new sheet has 2 pages, 31 places, the office-number header on both pages and no words 'form code', the row F line equal to the paper's sentence, no orphan line, the footer inside the margin line, the 13 tips; my own reruns of the executor's measure v1_1_0 (PASS 40, NOT_MEASURED 1 = Word, INFO 3) and sheet check v2_2_0 (61 of 61 PASS)")}
GROUPS = [dict(key="revfix", tasks=["TK4_RevFix_Build", "TK4_RevFix_Verify"], ctrls=["revfix"], start="2026-11-02T13:58:09", finish="2026-11-02T14:12:54", vstart="2026-11-02T14:19:39")]
eid = lambda c: "Ev4g_Ctl_" + c
fid = lambda c, i: "Ev4g_CtlFile_%s_%d" % (c, i)
def utc(x): return datetime.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S").astimezone().astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)
def sha(f): return hashlib.sha256(open(os.path.join(W.REPO, f), "rb").read()).hexdigest()
def draft(out):
    L = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    for c, (files, what) in G.items():
        L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" .\n' % (eid(c), W.lit("Control by the lineage agent: " + what), c, CTL, CTL, c))
        for i, f in enumerate(files):
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), f, sha(f)))
    open(out, "w", encoding="utf-8").write("".join(L))
REPS = {"revfix": "RESULT OF THE EXECUTOR of TK4_RevFix_Build (real start 2026-11-02T13:58:09Z; CME commit ac82656 at 14:12:54Z; recorded as reported): the corrections version in papers_r18_revfix (paper v2 .docx and PDF, sheet v2, wording file v1_1_0, sheet module v2.2.0, docx renderer v1.2.0, measure v1.1.0): the sheet header reads 'Office number 10100. Do not fill it.', the line above row F is the paper's own sentence, answer labels at 10 pt, 4f moved to page 4 so the last question page has 333 pt of slack (page 2 has 20.7 pt), cover overshoot 0.00 pt, the footer box inside the margin line, no orphan line; the build files are byte-equal to the first version's, so the key is the first version's key. NOT CONTROLLED, said openly: Microsoft Word (page 2 has only 20.7 pt, so question 1e may flow to page 3; the executor's line-spacing sweep stays at 5 pages up to x1.10 in LibreOffice). OWNER WORDING POINT (the sheet wording file v1_1_0): 'Office number 10100. Do not fill it.' and the row F sentence are the lineage agent's defaults, implemented as written."}
def record(bridge):
    g = rdflib.Graph(); g.parse(bridge, format="turtle"); vd = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        vd[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), utc(str(g.value(ev, B.verifiedAt))), str(g.value(ev, B.hasVerificationMethod)))
    src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); add = []; done = []; held = []
    for c, (files, what) in G.items():
        ok = bool(vd.get(eid(c)) and vd[eid(c)][0] and all(vd.get(fid(c, i)) and vd[fid(c, i)][0] for i in range(len(files))))
        if not ok: held.append(c); continue
        fin = vd[eid(c)][1]
        add.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" ;\n    backlog:verifiedAt "%sZ"^^xsd:dateTime .\n' % (eid(c), W.lit("Control by the lineage agent: " + what), c, CTL, W.lit(vd[eid(c)][2]), CTL, c, fin))
        for i, f in enumerate(files):
            add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%sZ"^^xsd:dateTime .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), f, sha(f), W.lit(vd[fid(c, i)][2]), fin))
    assert not held, held
    for gr in GROUPS:
        cs = gr["ctrls"]; evs = [x for c in cs for x in [eid(c)] + [fid(c, i) for i in range(len(G[c][0]))]]; ev = ", ".join("ex:" + x for x in evs)
        fin = max(vd[eid(c)][1] for c in cs); vstart = gr["vstart"]; FIN = gr["finish"]; assert FIN < vstart < min(vd[eid(c)][1] for c in cs), (gr["key"], FIN, vstart)
        add.append("ex:%s backlog:hasAuditNote %s .\n" % (gr["tasks"][0], W.lit(REPS[gr["key"]])))
        for n_, k in enumerate(gr["tasks"]):
            i, j = blk(t, k); b = t[i:j]
            if n_ == 0:
                s0, f0 = gr["start"], FIN
                if "backlog:hasState backlog:InProgress ; backlog:startedAt" in b:
                    nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:startedAt %s ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), FIN, ev), b, count=1)
                else:
                    nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%sZ"^^xsd:dateTime ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (s0, FIN, ev), 1)
                    add.append('ex:Begin5g_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started"), k, s0, W.lit("Work begun at the real instant the coordinator gave (parts 1 to 3 at 12:52:24Z, part 4 at 13:01:18Z); recorded after the delivery, under the Owner's order of 15:43 Istanbul to record the pause and the work later; the record was written after the real start.")))
                tfin = FIN
            else:
                nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%sZ"^^xsd:dateTime ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (vstart, fin, ev), 1); tfin = fin
                add.append('ex:Begin5g_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started"), k, vstart, W.lit("Started by the lineage agent at the instant it issued the controller run that wrote the kept log (the executor's report was read first). The control of parts 1 to 3 of Papers was first run at 13:06Z, before part 4 reported; this record is the control of the finished whole.")))
            assert nb != b, k
            t = t[:i] + nb + t[j:]
            add.append('ex:%s backlog:lastAuditedAt "%sZ"^^xsd:dateTime .\n' % (k, tfin))
            add.append('ex:Harness5g_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (k, W.lit("Control checks for " + k), k, ", ".join("ex:" + eid(c) for c in cs)))
            add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on its own re-runs, verified by backlog_evidence_bridge_v1_1_0 at %s UTC; evidence %s." % (fin, ", ".join(evs)))))
            add.append('ex:Complete5g_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller's verdict"), k, tfin, W.lit("Done on the lineage agent's own re-runs, verified by the evidence bridge.")))
            done.append(k)
    for _sid in ('ST4_RevFix', 'ST4_Rev'):
        pass
    for s2 in sorted(set(re.findall(r"\nex:(ST\w*?_\w+) a backlog:Story", t))):
        i, j = blk(t, s2); b = t[i:j]
        m = re.search(r"backlog:hasPriorityScore ex:Score(\d+[a-z]?)_%s\b" % s2, b)
        if not m or "backlog:hasState backlog:Done" in b or "backlog:hasState backlog:Cancelled" in b: continue
        kk = m.group(1)
        if ("\nex:Score%s_%s a" % (kk, s2)) not in t: continue
        k0 = t.index("\nex:Score%s_%s a" % (kk, s2)) + 1; r0 = t[k0:t.find("\nex:", k0 + 1)]
        q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0)
        if not q: continue
        nk = (kk[:-1] + chr(ord(kk[-1]) + 1)) if kk[-1].isalpha() else str(int(kk) + 1); nid = "Score%s_%s" % (nk, s2)
        if ("ex:" + nid + " a ") in t: continue
        bv, tc, rrr, size_ = int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4)); val = (bv + tc + rrr) / size_
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:" + nid, 1) + t[j:]
        add.append('ex:%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%sZ"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (nid, val, now, W.lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. RE-RUN on %s UTC after the controller's completions (%s): the earlier record predates them. Inputs unchanged." % (bv, tc, rrr, size_, val, now, ", ".join(done)))))
    fin = max(vd[eid(c)][1] for c in G); evs = [x for c in G for x in [eid(c)] + [fid(c, i) for i in range(len(G[c][0]))]]; ev = ", ".join("ex:" + x for x in evs)
    for sid in ("ST4_RevFix", "ST4_Rev"):
        i, j = blk(t, sid); b = t[i:j]
        nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:startedAt %s ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:lastAuditedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, fin, ev), b, count=1); assert nb != b, sid
        t = t[:i] + nb + t[j:]
        add.append('ex:Complete5g_%s a backlog:TransitionEvent ; rdfs:label "%s completed on the controller\'s verdict"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "Done with its tasks, on the lineage agent\'s own re-runs." .\n' % (sid, sid, sid, fin))
        add.append('ex:Harness5g_%s a backlog:TestHarness ; rdfs:label "Control checks for %s"@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:%s .\n' % (sid, sid, sid, eid("revfix")))
    add.append('ex:Obs70b_Obj7_PrintFlaws a backlog:MetricObservation ; rdfs:label "Reading after the corrections version was controlled"@en ;\n    backlog:observesMetric ex:Met7_PrintFlaws ; backlog:observationFor ex:Obj7_PrintFlaws ; backlog:hasObservedValue "0"^^xsd:decimal ; backlog:observedAt "%sZ"^^xsd:dateTime ;\n    backlog:hasObservationMethod "Counted by the lineage agent from its own control (kept log control_revfix_run3.log) and its reruns of the measure tool v1_1_0 (PASS 40, no FAIL, no RISK): header, row F line, labels under 10 pt, cover overshoot above 0.1 pt, footer box, orphan line and last-page slack under 40 pt: 0 of the 7 remain. Word is NOT_MEASURED." .\n' % fin)
    add.append('ex:Obs50c_Obj5_Corrections a backlog:MetricObservation ; rdfs:label "Reading after the single form was built and controlled"@en ;\n    backlog:observesMetric ex:Met5_Corrections ; backlog:observationFor ex:Obj5_Corrections ; backlog:hasObservedValue "6"^^xsd:decimal ; backlog:observedAt "%sZ"^^xsd:dateTime ;\n    backlog:hasObservationMethod "Counted by the controller from its own re-runs on the built single form: answer places (30 answer spaces, 31 sheet places), legal copy and directions (docx check, sheet wording), scope (items controlled), plain sentences (validator R01 to R29 on the items), tips page and stem rule (13 tips word for word, stems 10 to 20 words), penalty (five sentences, marking tool 110 and 0 with the exact fractions): 6 of 6." .\n' % fin)
    add.append("ex:ST4_Rev backlog:hasAuditNote %s .\n" % W.lit("STATE %s UTC: Done. Every task of the story is Done and the repair task TK4_RevFix_Build, the child that was still to come, is Done and controlled; the objective of the six corrections is read once, at 6." % now))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam: TK4_RevFix_Build controlled and Done with its verification; ST4_RevFix and ST4_Rev Done (%s)." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
