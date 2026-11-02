#!/usr/bin/env python3
"""sen0414_lineage_control_exam12 v1_0_0 (made from sen0414_lineage_control_exam10_v1_0_0.py) - records the Owner's decision of 2026-11-02 (move the exams to the private CME repository), the new tasks TK4_Leak_Move and TK4_Leak_Move_Verify and the control of the guard and of the move on bridge-verified evidence. ONE new register file.
  draft OUT.ttl      TestEvidence (command: sen0414_control_exam4_v1_0_0.py GROUP) and ArtifactEvidence nodes
  record BRIDGE.ttl  Done records of the verified groups, the stories, the harness, the readings, the finding, re-run scores"""
__version__ = "1.0.0"
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
NS = "http://example.org/sen0414-slides-lineage#"
CTL = "08-tooling/sen0414_control_exam11_v1_0_0.py"; E = "04-assessment/exams/"
G = {"leakguard": (["TK4_Leak_Guard", "TK4_Leak_Guard_Verify"], [".gitignore", "08-tooling/sen0414_control_exam11_v1_0_0.py", "08-tooling/control-exam-logs/control_leakguard_run1.log"], "the guard of ST4_Leak: .gitignore ignores new exam answer data (papers folders, item-set versions, keys, builds, sheets, a local exams folder), git check-ignore proves it on eight sample paths, no exam file was added to the tracked tree after the guard, the history is untouched"),
     "leakmove": (["TK4_Leak_Move", "TK4_Leak_Move_Verify"], ["08-tooling/sen0414_control_exam11_v1_0_0.py", "08-tooling/control-exam-logs/control_leakmove_run1.log"], "the move of the exam material (the Owner\'s decision of 2026-11-02): the CME repository is private on the remote, the removal commit only deletes the 31 files of items/ and papers_r14/, none is in the tree of HEAD, every removed file and every other tracked exam file before the removal equals its copy in CME by SHA-256, the Owner\'s cover template is not in CME, the history is untouched (no rewrite)")}
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
OWN = "OWNER DECISION of 2026-11-02 (10:27 Istanbul, relayed by the course coordinator and recorded as relayed): move the exams to the CME repository (private). A copy executor (start 2026-11-02T07:28:00Z) copied the SEN0414 and SEN0401 exam material to /home/claude/CME/exams (commit 709e55e, 307 files, manifest MANIFEST_SHA256_exams_v1_0_0.txt, nothing deleted, the cover template outside every repo). The lineage agent re-hashed source against copy itself and confirmed the remote private, then removed the answer-bearing tracked files from the public tree in a new commit (bd8b499, 31 deleted files, history untouched). A history rewrite is NOT ordered. All new exam artefacts (a Papers re-run, the make-up, the sheet repair) go to /home/claude/CME/exams/SEN0414 and not to this repository; the guard stays. The controllers of the earlier exam tasks read paths that no longer exist here; their results stand as recorded and a re-run reads the CME copy. What stays exposed: the history of this public repository still holds the files and copies taken while it was public."
def record(bridge):
    g = rdflib.Graph(); g.parse(bridge, format="turtle"); vd = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        vd[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), utc(str(g.value(ev, B.verifiedAt))), str(g.value(ev, B.hasVerificationMethod)))
    src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); nowZ = now + "Z"; add = []; done = []; held = []
    START = {"leakguard": "2026-11-01T22:47:51", "leakmove": "2026-11-02T07:35:53"}
    READY = {"leakguard": None, "leakmove": "2026-11-02T07:30:00"}
    for k in ("ST4_Leak", "TK4_Leak_Guard", "TK4_Leak_Guard_Verify"): add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(OWN)))
    mv = ["TK4_Leak_Move", "TK4_Leak_Move_Verify"]
    for k, typ, text_ in ((mv[0], "Build", "Deliverable: a new commit that removes the answer-bearing tracked exam files (04-assessment/exams/items and papers_r14, 31 files) from the public working tree, only after the private CME copy is hash-verified; the history is NOT rewritten (not ordered); new exam artefacts go to /home/claude/CME/exams/SEN0414. Estimated 0.3 hours (an estimate, G120)."), (mv[1], "Verify", "Control by the lineage agent: re-hash every removed file against its CME copy, confirm the CME remote private, confirm the removal commit only deletes, the tree of HEAD holds none of them, the history is untouched, the cover template is not in CME. Estimated 0.2 hours (an estimate, G120).")):
        isv = typ == "Verify"
        add.append('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:Iter_Ex3 ; backlog:admittedByOutput ex:Out4_Backlog ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n    backlog:hasInvestmentCategory backlog:%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n%s    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n' % (k, W.lit(k), k, W.lit(k), "Cat_Compliance", typ, "    backlog:dependsOn ex:%s ;\n" % mv[0] if isv else "", W.lit(text_ + " " + OWN)))
        rd = READY["leakmove"]
        add.append('ex:Refine5b_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_Ex3 ; backlog:hasWorkKind backlog:WorkKind_Preparation ;\n    backlog:hasRefinementOutcome "Refined from the Owner\'s decision of 2026-11-02 (relayed): deliverable, check and estimate are written in the item." .\n' % (k, k, k, rd))
        add.append('ex:RC5b_%s a backlog:ReadinessCheck ; rdfs:label "Readiness check of %s"@en ; backlog:checksReadinessOf ex:%s ; backlog:readinessCheckedAt "%s"^^xsd:dateTime ;\n    backlog:hasReadinessCriterion ex:RK5b_%s_1, ex:RK5b_%s_2, ex:RK5b_%s_3 .\n' % (k, k, k, rd, k, k, k))
        for kx, tx in ((1, "The deliverable, its place and its check are written in the item."), (2, "Every dependency of the item is Done or a task of the same story that precedes it."), (3, "The statements that bound the item are recorded on the story.")):
            add.append('ex:RK5b_%s_%d a backlog:ReadinessCriterion ; rdfs:label %s@en ; backlog:criterionMet true .\n' % (k, kx, W.lit(tx)))
        add.append('ex:Mv5b_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Refine ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " moved to Ready"), k, rd, W.lit("Refined and ready (ex:Refine5b_%s, ex:RC5b_%s); written with the work, at the instant of the Owner\'s decision." % (k, k))))
    t = t.replace("backlog:decomposesInto ex:TK4_Leak_Guard, ex:TK4_Leak_Guard_Verify", "backlog:decomposesInto ex:TK4_Leak_Guard, ex:TK4_Leak_Guard_Verify, ex:TK4_Leak_Move, ex:TK4_Leak_Move_Verify", 1)
    add.append("ex:Plan5a_ST4_Leak backlog:producesTask ex:TK4_Leak_Move, ex:TK4_Leak_Move_Verify .\nex:Iter_Ex3 backlog:hasMember ex:TK4_Leak_Move, ex:TK4_Leak_Move_Verify .\n")
    # the story starts with its first task
    i, j = blk(t, "ST4_Leak"); b = t[i:j]; nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%sZ"^^xsd:dateTime' % START["leakguard"], 1); assert nb != b; t = t[:i] + nb + t[j:]
    add.append('ex:Begin5b_ST4_Leak a backlog:TransitionEvent ; rdfs:label "ST4_Leak started with its first task"@en ; backlog:transitionedItem ex:ST4_Leak ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "The story starts with the guard, committed at %sZ; the guard was written just before the story was registered (said openly in its audit note)." .\n' % (START["leakguard"], START["leakguard"]))
    for c, (tasks, files, what) in G.items():
        ok = bool(vd.get(eid(c)) and vd[eid(c)][0] and all(vd.get(fid(c, i)) and vd[fid(c, i)][0] for i in range(len(files))))
        if not ok: held += tasks; continue
        fin = vd[eid(c)][1]; evs = [eid(c)] + [fid(c, i) for i in range(len(files))]; ev = ", ".join("ex:" + x for x in evs); st = START[c]
        add.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" ;\n    backlog:verifiedAt "%sZ"^^xsd:dateTime .\n' % (eid(c), W.lit("Control by the lineage agent: " + what), c, CTL, W.lit(vd[eid(c)][2]), CTL, c, fin))
        for i, f in enumerate(files):
            add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:attestsCriterion ex:AC4_Controlled ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%sZ"^^xsd:dateTime .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), f, sha(f), W.lit(vd[fid(c, i)][2]), fin))
        for n_, k in enumerate(tasks):
            i, j = blk(t, k); b = t[i:j]
            if c == "leakmove" and n_ == 0: tstart = st
            elif c == "leakmove": tstart = fin
            else: tstart = st if n_ == 0 else fin
            nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%sZ"^^xsd:dateTime ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (tstart, fin, ev), 1); assert nb != b, k
            t = t[:i] + nb + t[j:]
            add.append('ex:Begin5c_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started"), k, tstart, W.lit("Started by the lineage agent (the task was done by the agent itself, then controlled on the bridge-verified re-runs).")))
            add.append('ex:%s backlog:lastAuditedAt "%sZ"^^xsd:dateTime .\n' % (k, fin))
            add.append('ex:Harness5c_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:%s .\n' % (k, W.lit("Control checks for " + k), k, eid(c)))
            add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on its own re-runs, verified by backlog_evidence_bridge_v1_1_0 at %s UTC; evidence %s." % (fin, ", ".join(evs)))))
            add.append('ex:Complete5c_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller\'s verdict"), k, fin, W.lit("Done on the lineage agent\'s own re-runs, verified by the evidence bridge.")))
            done.append(k)
    add.append("ex:ST4_Leak backlog:hasAuditNote %s .\n" % W.lit("STATE %s UTC: the guard and the move are Done and controlled; the story stays open: the history of the public repository still holds the files (a rewrite is not ordered) and the repository is still public; the Owner decides whether and when to close it." % now))
    # re-run the scores of the open stories (Z, to compare with the Z completions)
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
        add.append('ex:%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%sZ"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (nid, val, now, W.lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. RE-RUN on %s UTC after the controller\'s completions (%s): the earlier record predates them. Inputs unchanged." % (bv, tc, rrr, size_, val, now, ", ".join(done)))))
    add.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit("%s UTC: the Owner\'s decision to move the exams to the private CME repository recorded; the guard and the move are Done (held: %s). New exam artefacts go to /home/claude/CME/exams/SEN0414; the guard stays." % (now, ", ".join(held) or "none")))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam change: the Owner\'s decision to move the exams to CME recorded; ST4_Leak started; the guard and the move controlled and Done (%s)." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
