#!/usr/bin/env python3
"""sen0414_lineage_control_exam10 v1_0_0 (made from sen0414_lineage_control_exam8_v1_0_0.py) - records the lineage agent's control of TK4_Papers and TK4_Papers_Verify and of the story ST4_Papers on bridge-verified evidence. ONE new register file.
  draft OUT.ttl      TestEvidence (command: sen0414_control_exam4_v1_0_0.py GROUP) and ArtifactEvidence nodes
  record BRIDGE.ttl  Done records of the verified groups, the stories, the harness, the readings, the finding, re-run scores"""
__version__ = "1.0.0"
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
NS = "http://example.org/sen0414-slides-lineage#"
CTL = "08-tooling/sen0414_control_exam9_v1_0_0.py"; E = "04-assessment/exams/"
G = {"papers": (["TK4_Papers", "TK4_Papers_Verify"], [E + "exam_docx_v1_0_0.py", E + "exam_docx_check_v1_0_0.py"] + [E + "papers_r14/" + f for f in ("midterm_form_A_paper.docx", "midterm_form_A_key.docx", "midterm_form_B_paper.docx", "midterm_form_B_key.docx", "midterm_answersheet.pdf", "makeup_form_A_paper.docx", "makeup_form_A_key.docx", "makeup_answersheet.pdf")], "the exam papers as briefed (r14): the executor's docx check self-test exits 0; the controller rebuilt the midterm (forms A and B) and the make-up (form A) from the committed item lists at seed 20261102 (28 of 28 engine rules), the executor's check ran on those builds with 0 failures (key equals the engine key, key recomputed from the paper text, 5 paper pages plus 1 sheet page on LibreOffice, no split sub-question); the Owner's cover template is not among the tracked files; the commit adds only new files"),}
STORY = {}
eid = lambda c: "Ev4e_Ctl_" + c
fid = lambda c, i: "Ev4e_CtlFile_%s_%d" % (c, i)
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
REP_P = ("RESULT OF THE EXECUTOR of TK4_Papers (real start 2026-11-01T22:04:42Z; commit e7d7821; recorded as reported): exam_docx_v1_0_0.py (editable .docx paper and key, answer sheet from the SEN0401 sheet module), exam_docx_check_v1_0_0.py, the midterm forms A and B and the make-up form A as paper, key and answer sheet in 04-assessment/exams/papers_r14. Disclosed by the executor and confirmed by the controller: 5 pages per paper plus 1 sheet = 6 (the brief's 4 is not met; 6 allowed by the check); NOTHING WAS PRINTED; make-up form B and a two-column key are not built; the item lists are provisional; the cover outcome lines of chapters 2, 3, 4, 6 and 7 and the exam date are blank. Controller findings: the answer-sheet rule 5 text is cut at the right edge in the sheet module of SEN0401 (not edited here); the papers, keys and item lists with answers are committed in a public repository.")
def record(bridge):
    g = rdflib.Graph(); g.parse(bridge, format="turtle"); vd = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        vd[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), utc(str(g.value(ev, B.verifiedAt))), str(g.value(ev, B.hasVerificationMethod)))
    src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); add = []; done = []; held = []
    c = "papers"; tasks, files, what = G[c]
    ok = bool(vd.get(eid(c)) and vd[eid(c)][0] and all(vd.get(fid(c, i)) and vd[fid(c, i)][0] for i in range(len(files))))
    for k in tasks: add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(REP_P)))
    if not ok:
        held = tasks
    else:
        ctl_start = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(W.REPO, "08-tooling/control-exam-logs/control_papers_run1.log")), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        fin = vd[eid(c)][1]; evs = [eid(c)] + [fid(c, i) for i in range(len(files))]; ev = ", ".join("ex:" + x for x in evs)
        add.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid(c), W.lit("Control by the lineage agent: " + what), c, CTL, W.lit(vd[eid(c)][2]), CTL, c, fin))
        for i, f in enumerate(files):
            add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), f, sha(f), W.lit(vd[fid(c, i)][2]), fin))
        for k in tasks:
            i, j = blk(t, k); b = t[i:j]
            if "backlog:hasState backlog:Ready" in b:
                nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%sZ"^^xsd:dateTime ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (ctl_start, fin, ev), 1)
                add.append('ex:Begin4k_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started by the controller"), k, ctl_start, W.lit("The controller began its own re-run at the instant of its first kept log.")))
            else:
                nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:startedAt %s ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, ev), b, count=1)
            assert nb != b, k
            t = t[:i] + nb + t[j:]
            add.append('ex:%s backlog:lastAuditedAt "%sZ"^^xsd:dateTime .\n' % (k, fin))
            add.append('ex:Harness4k_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:%s .\n' % (k, W.lit("Control checks for " + k), k, eid(c)))
            add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on its own re-runs, verified by backlog_evidence_bridge_v1_1_0 at %s UTC; evidence %s." % (fin, ", ".join(evs)))))
            add.append('ex:Complete4k_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller's verdict"), k, fin, W.lit("Done on the controller's own re-runs, verified by the evidence bridge; the executor's report alone was not taken as the result.")))
            done.append(k)
        sid = "ST4_Papers"; i, j = blk(t, sid); b = t[i:j]
        nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:startedAt %s ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:lastAuditedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, fin, ev), b, count=1)
        assert nb != b, sid; t = t[:i] + nb + t[j:]
        add.append('ex:Complete4k_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "Done with its tasks on the controller\'s verdict; the make-up paper beyond form A is the story ST4_MakeUp." .\n' % (sid, W.lit(sid + " completed on the controller's verdict"), sid, fin)); done.append(sid)
        add.append('ex:Harness4k_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (sid, W.lit("Control checks for " + sid), sid, ev))
        add.append('ex:Obs47_Obj4_PapersBuilt a backlog:MetricObservation ; rdfs:label "Reading after the controller re-ran the paper checks (ST4_Papers)"@en ;\n    backlog:observesMetric ex:Met4_Papers ; backlog:observationFor ex:Obj4_PapersBuilt ; backlog:hasObservedValue "2"^^xsd:decimal ; backlog:observedAt "%sZ"^^xsd:dateTime ;\n    backlog:hasObservationMethod "Counted by the metric\'s own query from the files in 04-assessment/exams after the controller re-ran the paper checks: the midterm (forms A and B, each with paper, key and answer sheet) and the make-up (form A with paper, key and answer sheet) = 2 papers with a key, as editable .docx and a sheet PDF. NOT MET in the strict wording: nothing has been printed; make-up form B and a two-column key are not built; the item lists are provisional; the page count is 6, not 4." .\n' % now)
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
    add.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit("RANKING %s UTC after the controller's verdict on the papers (done now: %s; held: %s). The make-up paper beyond form A stays the story ST4_MakeUp, ranked last by the Owner; EP4_Engine stays open for it." % (now, ", ".join(done) or "none", ", ".join(held) or "none")))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam change: the controller's verdict on the papers (TK4_Papers, its control and ST4_Papers: %s)." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
