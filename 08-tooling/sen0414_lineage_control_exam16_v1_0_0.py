#!/usr/bin/env python3
"""sen0414_lineage_control_exam16 v1_0_0 (made from sen0414_lineage_control_exam14_v1_0_0.py) - records the lineage agent's control of TK4_Rev_Valid, TK4_Rev_Valid_Verify, TK4_Rev_Sheet and TK4_Rev_Sheet_Verify and the start of the Ch04 repair round on bridge-verified evidence. ONE new register file. The designed files live in the private CME repository, so the evidence nodes name the controller and its kept log (both in this repository); the log prints the SHA-256 of the controlled CME files.
  draft OUT.ttl      TestEvidence (command: sen0414_control_exam13_v1_0_0.py revdesign) and ArtifactEvidence nodes
  record BRIDGE.ttl  Done records of the two tasks, the harness, the audit notes, re-run scores"""
__version__ = "1.0.0"
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
CTL = "08-tooling/sen0414_control_exam15_v1_0_0.py"
LOGS = {"revvalid": "08-tooling/control-exam-logs/control_revvalid_run1.log", "revsheet": "08-tooling/control-exam-logs/control_revsheet_run1.log"}
G = {"revvalid": (["TK4_Rev_Valid", "TK4_Rev_Valid_Verify"], [CTL, LOGS["revvalid"]], "the item validator v1.2.0 and the taught vocabulary in the private CME repository: the executor's commit 0da99d1 adds only 12 new files, the self-test reruns with 39 fixtures and RESULT PASS, R02 to R24 give the same failures as v1.1.0 on 6 item files and 66 fixtures, the vocabulary (3461 entries) rebuilds to the same bytes and misses capitalize, fromkeys and lambda while holding print, len, range, append, my own extraction of the eight latest decks agrees, the failure list of the midterm list is recomputed (R25 11, R26 1, R27 2, R28 18, R29 0), four mutations are caught"),
     "revsheet": (["TK4_Rev_Sheet", "TK4_Rev_Sheet_Verify"], [CTL, LOGS["revsheet"]], "the answer sheet v2.0.0 in the private CME repository: the executor's commit 9f74ac1 adds only 27 new files, its sheet check reruns with 43 of 43 PASS, my own reading of the PDFs finds 2 pages, page 2 without circles, all glyphs inside the margins (rightmost 552.76 pt), type 10 point or larger, 298 circles and a printed label for each of the 31 places, the layout holds 31 places, and the tips-page capacity is measured (10 tips of 25 words, 15 of 20 words, 26 of 12 words)")}
FINISH = {"revvalid": "2026-11-02T10:54:41", "revsheet": "2026-11-02T11:02:17"}
VSTART = {"revvalid": "2026-11-02T11:13:20", "revsheet": "2026-11-02T11:17:55"}
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
REPS = {"revvalid": "RESULT OF THE EXECUTOR of TK4_Rev_Valid (real start 2026-11-02T10:48:23Z; CME commit 0da99d1 at 10:54:41Z; recorded as reported): validator exam_item_check_v1_2_0.py with R01 to R24 unchanged and new R25 to R29 (39 fixtures), taught-vocabulary builder and vocabulary of 3461 entries from the latest deck of each chapter 1 to 8, the failure list of the midterm list. TIMING, said openly: the task began at 10:48:23Z before its dependency TK4_Rev_Design_Verify was Done in the register (that control finished at 10:51:26Z). FOR THE ITEMS EXECUTOR: R20 (unchanged, not weakened) allows a tip of at most 20 words, so a tip of 21 to 25 words fails R20; the binding limit is the capacity of the tips page (see the sheet control). The record field answer_format is the optional 23rd field and R28 requires it; SEN0414_ROOT names the repository that holds 03-materials for the validator.",
        "revsheet": "RESULT OF THE EXECUTOR of TK4_Rev_Sheet (real start 2026-11-02T10:48:23Z; CME commit 9f74ac1 at 11:02:17Z; recorded as reported): answer sheet v2.0.0 as two pages (answer grid with a place for each of the 31 places, tips page without bubbles), reader copies, audit and check (43 of 43 PASS), printed rules wrapped inside the margins (rightmost glyph 552.76 pt; the unwrapped rule 5 line at 632.8 pt is caught). TIMING, said openly: the task began at 10:48:23Z before its dependency TK4_Rev_Design_Verify was Done in the register. FINDINGS OF THE CONTROL for the Owner and the Papers task: (1) the tips page holds only 10 tips of 25 words, 15 of 20 words or 26 of 12 words, so the 18 tips of the midterm list do not fit unless each is about 12 words or fewer; the sheet refuses an overflow and does not clip; (2) the legal-copy sentence of the design, printed word for word on the answer sheet, says these pages are the official answers while the sheet is only for faster checking, which contradicts itself when read on the sheet; a sheet wording that points to the question pages is needed (an Owner wording point); (3) the cost sentence for question 5 applies the penalty to the bonus question (an Owner point); (4) a sheet with a unit answered by hand does not fit page 1 (not form A)."}
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
    BR = "08-tooling/briefs/midterm/r3/BRIEF_TK_MS_Ch04_Build_Repair.md"
    add.append('ex:EI_MS_TK_MS_Ch04_Repair a backlog:ExecutorInstance ; rdfs:label "Executor session SEN0414-MS-ch04 (repair round)"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion "brief %s, session SEN0414-MS-ch04" ; backlog:instantiatedAt "2026-11-02T10:52:45Z"^^xsd:dateTime ;\n    rdfs:comment "Started at the real instant the coordinator gave (date -u); retired when the session reports."@en .\n' % BR)
    add.append('ex:Brief_MS_TK_MS_Ch04_Repair a backlog:ExecutorBrief ; rdfs:label "Brief of the repair round of TK_MS_Ch04_Build"@en ; backlog:briefFor ex:TK_MS_Ch04_Build ; backlog:briefCriterion ex:AC2M_Ch04 ; backlog:briefedExecutorInstance ex:EI_MS_TK_MS_Ch04_Repair ;\n    rdfs:comment "Passed unedited by the coordinator; file %s, SHA-256 %s."@en .\n' % (BR, sha(BR)))
    note = "REPAIR ROUND started 2026-11-02T10:52:45Z (real instant given by the coordinator), executor session SEN0414-MS-ch04, brief %s: the controller's runs of page test 9.38.0 on page v9_92_1 failed 414/2 on D5 (the word lambda in 25 places); page test 9.37.0 passed 406/0. The task stays InProgress; the repair is a second round of the same task, not a new task." % BR
    add.append("ex:TK_MS_Ch04_Build backlog:hasAuditNote %s .\nex:ST_MS_Ch04 backlog:hasAuditNote %s .\n" % (W.lit(note), W.lit(note)))
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
    out = W.write_new(src, t + "\n" + "".join(add), "Exam revision: TK4_Rev_Valid and TK4_Rev_Sheet controlled and Done with their verifications (%s); Ch04 repair round started." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
