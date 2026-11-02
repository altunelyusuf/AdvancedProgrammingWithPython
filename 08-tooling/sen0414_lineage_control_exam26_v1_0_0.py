#!/usr/bin/env python3
"""sen0414_lineage_control_exam26 v1_0_0 (made from sen0414_lineage_control_exam23_v1_0_0.py) - records the lineage agent's control of TK4_Rev_Papers (parts 1 to 4) and TK4_Rev_EngineFix, each with its verification, on bridge-verified evidence. ONE new register file. The designed files live in the private CME repository, so the evidence nodes name the controller and its kept logs (both in this repository); the logs print the SHA-256 of the controlled CME files.
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
G = {"revpapers": ([CTL, LD + "control_revpapers_run3.log"], "parts 1 to 3 of the Papers task in the private CME repository: the four commits 738161d, 6df5b6d, 60eb5a3 and fb504ab add only new files; my own rebuild with engine v1_2_1 (seed 1) gives E01 to E34 all PASS and the committed key, paper, sheet specification and authored files byte for byte, and the controlled engine v1_2_0 gives the same key; my own LibreOffice conversion of the paper gives 5 pages (cover and 4), type 9.5 pt or larger; all 14 choice units print the key letter's option text; the real sheet has 2 pages, 31 labels, the wording-file sentence, no circles on page 2 and the 13 tips word for word; the marking tool on the real key gives 110 for all right and 0 for all blank; no exam file is in the public repository"),
     "revmeasure": ([CTL, LD + "control_revmeasure_run1.log"], "part 4 of the Papers task (measurement and delivery proof, CME commit 2a62393): the commit adds only new files; the executor's log has PASS 29, FAIL 2, RISK 1, NOT_MEASURED 1 printed as they came; my own measures agree: the paper PDF is the controlled file (SHA-256 ace81060e1dee431) with 5 pages, 2 cover glyphs past the margin by 0.50 pt, 849 body glyphs at 9.5 pt, slack of the last question page 11.5 pt; my own hand score of the executor's mixed reading is 1817/42 and equals the tool"),
     "reveng2": ([CTL, LD + "control_reveng2_run1.log", LD + "control_reveng2_check_run1.log"], "engine v1_2_1 in the private CME repository (commit a45b086, only new files): SHA-256 f5c8e432d70db1abaf6eba3a68f68b5fff05aaf51db9e018be42af75976ee0b1, the file the parts 1 to 3 were built with; my own niced rerun of its check (967 seconds, kept log) gives RESULT PASS with 676 OK and 0 MISMATCH; the seven changed verdicts of the older suites are exactly the listed ones, each a refusal that now also names E02 (the validator v1_2_0 reports the same defect), none weakened; the engine differs from v1_2_0 by 31 changed lines (the validator for E02 and the sheet wording for E33)")}
GROUPS = [dict(key="papers", tasks=["TK4_Rev_Papers", "TK4_Rev_Papers_Verify"], ctrls=["revpapers", "revmeasure"], start="2026-11-02T12:52:24", finish="2026-11-02T13:32:26", vstart="2026-11-02T13:54:24"),
          dict(key="engfix", tasks=["TK4_Rev_EngineFix", "TK4_Rev_EngineFix_Verify"], ctrls=["reveng2"], start="2026-11-02T12:15:39", finish="2026-11-02T13:25:39", vstart="2026-11-02T13:26:20")]
eid = lambda c: "Ev4f_Ctl_" + c
fid = lambda c, i: "Ev4f_CtlFile_%s_%d" % (c, i)
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
REPS = {"papers": "RESULT OF THE FOUR EXECUTORS of TK4_Rev_Papers (real starts 2026-11-02T12:52:24Z for parts 1 to 3 and 13:01:18Z for part 4; CME commits 738161d and 6df5b6d (part 1, build and sheet), fb504ab (part 2, paper), 60eb5a3 (part 3, key), 2a62393 (part 4, measure) at 13:32:26Z; recorded as reported): the one paper of 5 pages (cover and 4 question pages), 30 answer spaces, its key of 3 pages and the answer sheet of 2 pages; the marking tool gives 110, 0 and 1817/42 on the real key. The Owner chose at 16:50 Istanbul (13:50Z) to PRINT THE PDF NOW and not to re-export from Word. NOT CONTROLLED, said openly: the paper in Microsoft Word (the last question page has 11.5 pt of slack, a safe margin is about 40 pt: if Word adds a sixth page the committed PDF is the file to print); the answer keys of the match, order and bank units were not read against the printed paper by the controller beyond the engine checks and the marking tool. KNOWN FLAWS, for the corrections version (story ST4_RevFix): the header 'form code 10100' of the sheet that students never fill; the line above row F reads 'Give the code of one bank word'; the 30 answer labels and format sentences are set at 9.5 pt; the cover has 3 glyphs 0.55 pt past the margin; the sheet footer box ends 0.40 pt below the margin line (no ink does); an orphan 'it.' on sheet page 1; the slack of the last question page.",
        "engfix": "RESULT OF THE EXECUTOR of TK4_Rev_EngineFix (real start 2026-11-02T12:15:39Z; CME commit a45b086 at 13:25:39Z; recorded as reported): engine v1.2.1 (the item validator v1_2_0 wired in for E02; E33 checks the sheet wording file's sentence), its shapes, 87 fixtures and check with the full log, and real builds for seeds 1, 2 and 3, each with E01 to E34 PASS; seven verdicts of older suites changed and are listed in the check (all because of the validator in E02). The engine file was already in use by the parts 1 to 3 of Papers before this control; its SHA-256 is unchanged, so no part was rebuilt."}
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
                    add.append('ex:Begin5f_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started"), k, s0, W.lit("Work begun at the real instant the coordinator gave (parts 1 to 3 at 12:52:24Z, part 4 at 13:01:18Z); recorded after the delivery, under the Owner's order of 15:43 Istanbul to record the pause and the work later; the record was written after the real start.")))
                tfin = FIN
            else:
                nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%sZ"^^xsd:dateTime ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (vstart, fin, ev), 1); tfin = fin
                add.append('ex:Begin5f_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started"), k, vstart, W.lit("Started by the lineage agent at the instant it issued the controller run that wrote the kept log (the executor's report was read first). The control of parts 1 to 3 of Papers was first run at 13:06Z, before part 4 reported; this record is the control of the finished whole.")))
            assert nb != b, k
            t = t[:i] + nb + t[j:]
            add.append('ex:%s backlog:lastAuditedAt "%sZ"^^xsd:dateTime .\n' % (k, tfin))
            add.append('ex:Harness5f_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (k, W.lit("Control checks for " + k), k, ", ".join("ex:" + eid(c) for c in cs)))
            add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on its own re-runs, verified by backlog_evidence_bridge_v1_1_0 at %s UTC; evidence %s." % (fin, ", ".join(evs)))))
            add.append('ex:Complete5f_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller's verdict"), k, tfin, W.lit("Done on the lineage agent's own re-runs, verified by the evidence bridge.")))
            done.append(k)
    # the four executors of Papers
    BR = "08-tooling/briefs/exam/"; base = BR + "r15/BRIEF_TK4_Rev_Papers.md"; adds = BR + "r16/ADDENDUM_TK4_Rev_Papers.md"
    PARTS = [("1", "1_Build", "12:52:24"), ("2", "2_Paper", "12:52:24"), ("3", "3_Key", "12:52:24"), ("4", "4_Measure", "13:01:18")]
    for num, nm, hh in PARTS:
        bf = BR + "r17/BRIEF_TK4_Rev_Papers_%s.md" % nm; sess = "SEN0414-EX-rev-papers-" + num; at = "2026-11-02T" + hh
        add.append('ex:EI_4f_Papers_%s a backlog:ExecutorInstance ; rdfs:label "Executor session %s"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ;\n    rdfs:comment "Started at the real instant the coordinator gave (date -u); retired when the session reported."@en .\n' % (num, sess, W.lit("brief %s (part %s of 4 of the Papers task; the whole-task brief %s SHA-256 %s and its addendum %s SHA-256 %s stand behind it), session %s" % (bf, num, base, sha(base), adds, sha(adds), sess)), at))
        add.append('ex:Brief_4f_Papers_%s a backlog:ExecutorBrief ; rdfs:label "Brief of Papers part %s"@en ; backlog:briefFor ex:TK4_Rev_Papers ; backlog:briefCriterion ex:AC4_Controlled ; backlog:briefedExecutorInstance ex:EI_4f_Papers_%s ;\n    rdfs:comment %s@en .\n' % (num, num, num, W.lit("Written by the lineage agent in 10 minutes at the Owner's order to split the Papers task for parallel agents; file %s, SHA-256 %s." % (bf, sha(bf)))))
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
    add.append("ex:ST4_Rev backlog:hasAuditNote %s .\n" % W.lit("STATE %s UTC: every task of the story is Done (Design, Valid, Sheet, Items, Engine, Score, SheetText, EngineFix, Papers and their verifications). The story stays InProgress on purpose: the printed exam has the known flaws listed on TK4_Rev_Papers, which the story ST4_RevFix repairs in a corrections version; the objective of the six corrections is read once, after that repair." % now))
    OD = "OWNER DECISION of 2026-11-02 16:52 Istanbul (13:52Z), relayed by the coordinator and recorded as relayed: the floor is at 0 on the whole paper, for both exams. This is the printed default of SEN0414 (rule A4 of the marking tool), so the paper, key and sheet need no change; it settles the stipulation B2b (blind mean A2 0, A3 9.63, A4 4.33 of 110). Still open for the Owner, asked one at a time: the penalty on the bonus question Q5, the tip limit (12 words implemented, 25 in the design), the page budget and the sheet wording."
    for k_ in ("TK4_Rev_Score", "ST4_Rev", "TK4_Rev_Papers"):
        add.append("ex:%s backlog:hasAuditNote %s .\n" % (k_, W.lit(OD)))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam revision: TK4_Rev_Papers (parts 1 to 4) and TK4_Rev_EngineFix controlled and Done with their verifications (%s)." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
