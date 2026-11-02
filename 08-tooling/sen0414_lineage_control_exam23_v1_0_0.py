#!/usr/bin/env python3
"""sen0414_lineage_control_exam23 v1_0_0 (made from sen0414_lineage_control_exam21_v1_0_0.py) - records the lineage agent's control of TK4_Rev_Score and TK4_Rev_Score_Verify on bridge-verified evidence. ONE new register file. The designed files live in the private CME repository, so the evidence nodes name the controller and its kept log (both in this repository); the log prints the SHA-256 of the controlled CME files.
  draft OUT.ttl      TestEvidence (command: sen0414_control_exam13_v1_0_0.py revdesign) and ArtifactEvidence nodes
  record BRIDGE.ttl  Done records of the two tasks, the harness, the audit notes, re-run scores"""
__version__ = "1.0.0"
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
CTL = "08-tooling/sen0414_control_exam22_v1_0_0.py"
LOGS = {"revscore": "08-tooling/control-exam-logs/control_revscore_run1.log"}
G = {"revscore": (["TK4_Rev_Score", "TK4_Rev_Score_Verify"], [CTL, LOGS["revscore"]], "the marking tool v1.0.0 in the private CME repository: the executor's commit 4e30b87 adds only 7 new files, its check reruns niced with 21 of 21 PASS, the blind proof reruns with my own seed (777, 6000 sheets) and every row agrees with the exact value, on a real key built from items_v3_0_0.json (engine with the validator wired in, my own process only) my own hand scores agree with the tool: a mixed sheet 565/14, all right 110, all blank 0, all wrong -622/21 under no floor and 0 under the paper floor, a doubled row is held; the blind .md and .log are the same bytes")}
FINISH = {"revscore": "2026-11-02T12:27:01"}
VSTART = {"revscore": "2026-11-02T12:37:34"}
eid = lambda c: "Ev4e_Ctl_" + c
fid = lambda c, i: "Ev4e_CtlFile_%s_%d" % (c, i)
def utc(x): return datetime.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S").astimezone().astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
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
REPS = {"revscore": "RESULT OF THE EXECUTOR of TK4_Rev_Score (real start 2026-11-02T12:15:39Z; CME commit 4e30b87 at 12:27:01Z; recorded as reported): marking tool v1.0.0 (wrong answer costs points/(k-1), blank 0, paper floor A4 by default, held units listed, the A1 to A4 alternatives and two Q5 variants carried), check 21 of 21, blind proof on 20,000 sheets (A2 mean 0 within error, no penalty gives the choice units a 25.1 per cent advantage). GAPS said openly by the executor and the controller: no key from the real items yet at the time (engine v1.2.0 refused them by E02; TK4_Rev_EngineFix runs), so the tool must be rerun on the first real key (Papers); no printed or scanned sheet measured. NOTE of the controller: the engine reorders the records inside a question for the paper, so the points of a sheet unit follow its position on the paper, not the record id; the tool reads them from the key, which is right. OPEN FOR THE OWNER (figures confirmed by the executor's tables): the floor B2b (mean blind score A2 0, A3 9.63, A4 4.33 of 110) and the penalty on the bonus question Q5."}
def record(bridge):
    g = rdflib.Graph(); g.parse(bridge, format="turtle"); vd = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        vd[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), utc(str(g.value(ev, B.verifiedAt))), str(g.value(ev, B.hasVerificationMethod)))
    src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); add = []; done = []; held = []
    for c in G:
        tasks, files, what = G[c]; LOG = LOGS[c]; FINISH_DESIGN = FINISH[c]
        ok = bool(vd.get(eid(c)) and vd[eid(c)][0] and all(vd.get(fid(c, i)) and vd[fid(c, i)][0] for i in range(len(files))))
        add.append("ex:%s backlog:hasAuditNote %s .\n" % (tasks[0], W.lit(REPS[c])))
        if not ok: held += tasks; continue
        fin = vd[eid(c)][1]; evs = [eid(c)] + [fid(c, i) for i in range(len(files))]; ev = ", ".join("ex:" + x for x in evs)
        vstart = VSTART[c]; assert FINISH_DESIGN < vstart < fin, (c, FINISH_DESIGN, vstart, fin)
        add.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" ;\n    backlog:verifiedAt "%sZ"^^xsd:dateTime .\n' % (eid(c), W.lit("Control by the lineage agent: " + what), c, CTL, W.lit(vd[eid(c)][2]), CTL, c, fin))
        for i, f in enumerate(files):
            add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%sZ"^^xsd:dateTime .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), f, sha(f), W.lit(vd[fid(c, i)][2]), fin))
        for n_, k in enumerate(tasks):
            i, j = blk(t, k); b = t[i:j]
            if n_ == 0:
                nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:startedAt %s ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), FINISH_DESIGN, ev), b, count=1); tfin = FINISH_DESIGN
            else:
                nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%sZ"^^xsd:dateTime ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (vstart, fin, ev), 1); tfin = fin
                add.append('ex:Begin5d_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started"), k, vstart, W.lit("Started by the lineage agent at the instant it issued the controller run that wrote the kept log (the executor's report was read first).")))
            assert nb != b, k
            t = t[:i] + nb + t[j:]
            add.append('ex:%s backlog:lastAuditedAt "%sZ"^^xsd:dateTime .\n' % (k, tfin))
            add.append('ex:Harness5d_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:%s .\n' % (k, W.lit("Control checks for " + k), k, eid(c)))
            add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on its own re-runs, verified by backlog_evidence_bridge_v1_1_0 at %s UTC; evidence %s." % (fin, ", ".join(evs)))))
            add.append('ex:Complete5d_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller's verdict"), k, tfin, W.lit("Done on the lineage agent's own re-runs, verified by the evidence bridge.")))
            done.append(k)
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
    out = W.write_new(src, t + "\n" + "".join(add), "Exam revision: TK4_Rev_Score controlled and Done with its verification (%s)." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
