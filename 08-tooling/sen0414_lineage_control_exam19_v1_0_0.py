#!/usr/bin/env python3
"""sen0414_lineage_control_exam19 v1_0_0 (made from sen0414_lineage_control_exam16_v1_0_0.py) - records the lineage agent's control of TK4_Rev_Items and TK4_Rev_Engine (with their verifications) and registers TK4_Rev_EngineFix on bridge-verified evidence. ONE new register file. The designed files live in the private CME repository, so the evidence nodes name the controller and its kept log (both in this repository); the log prints the SHA-256 of the controlled CME files.
  draft OUT.ttl      TestEvidence (command: sen0414_control_exam13_v1_0_0.py revdesign) and ArtifactEvidence nodes
  record BRIDGE.ttl  Done records of the two tasks, the harness, the audit notes, re-run scores"""
__version__ = "1.0.0"
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
CTL = "08-tooling/sen0414_control_exam18_v1_0_0.py"
LOGS = {"revitems": "08-tooling/control-exam-logs/control_revitems_run1.log", "revengine": "08-tooling/control-exam-logs/control_revengine_check_run1.log"}
LOGS2 = {"revengine": "08-tooling/control-exam-logs/control_revengine_run1.log"}
G = {"revitems": (["TK4_Rev_Items", "TK4_Rev_Items_Verify"], [CTL, LOGS["revitems"]], "the single midterm item set items_v3_0_0.json in the private CME repository: the executor's commit 2fa152b adds only 6 new files, the validator v1_2_0 gives RESULT PASS with 0 failures, 18 records and 30 units, points per question 25/25/25/25/10, chapter quotas 4,4,4,4,3,4,4,3 and the unit counts per type equal the design, Bloom minima hold, every stem has 10 to 20 words and one sentence (my own count), 13 tips of at most 12 words, answer_format on every record, capitalize and fromkeys occur nowhere, the answers of the predict items, Q1f, Q5c, Q4b, Q5d, Q2a, Q3a and Q4a were recomputed by running or reading the code, no item set or key is tracked in the public repository"),
     "revengine": (["TK4_Rev_Engine", "TK4_Rev_Engine_Verify"], [CTL, LOGS["revengine"], LOGS2["revengine"]], "the engine v1.2.0 in the private CME repository: the executor's commit 9c17e3e adds only 7 new files, the engine check reruns completely (all suites, kept log), the finding is confirmed (the engine refuses the real items by E02 only because it still calls validator v1_1_0), with validator v1_2_0 wired in my own process the engine builds the real paper with every rule E01 to E34 passing, and the scoring table of the built paper has 30 units whose k, cost points/(k-1) and exact blind gain 0 I recomputed from the items")}
FINISH = {"revitems": "2026-11-02T11:32:38", "revengine": "2026-11-02T11:39:06"}
VSTART = {"revitems": "2026-11-02T11:44:16", "revengine": "2026-11-02T11:40:43"}
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
REPS = {"revitems": "RESULT OF THE EXECUTOR of TK4_Rev_Items (real start 2026-11-02T11:27:50Z; CME commit 2fa152b at 11:32:38Z; recorded as reported): items_v3_0_0.json, 18 records and 30 units, validator v1_2_0 R01-R29 0 failures, stems 10 to 20 words, tips at most 12 words (13 records, 5 none), answer_format on all, capitalize and fromkeys gone, tips page layout fits. FINDING of the executor, confirmed by the controller: engine v1.1.0 and v1.2.0 refuse the new field (rule E02); a repair task TK4_Rev_EngineFix is registered. GUARD GAP found by the controller: the new item-set file name items_v3_0_0.json was not covered by the public repository's .gitignore (patterns named items_a_/items_b_); two patterns were added and committed, no such file was ever tracked.",
        "revengine": "RESULT OF THE EXECUTOR of TK4_Rev_Engine (real start 2026-11-02T10:48:23Z; CME commit 9c17e3e at 11:39:06Z; recorded as reported): engine v1.2.0 with rules E29 to E34, 82 fixtures, the check RESULT PASS (420 OK, 0 mismatches), the v1.1.0 fixtures behave as before, the blind gain recomputed exactly 0 per unit, the four floor alternatives carried. TIMING, said openly: the task began at 10:48:23Z before its dependency TK4_Rev_Design_Verify was Done in the register. FINDINGS OF THE CONTROL: the engine still calls validator v1_1_0 and so refuses the real items by E02 alone; its rule E33 expects the design's legal-copy sentence on the sheet while TK4_Rev_SheetText gives the sheet its own sentence; both are repaired by the new task TK4_Rev_EngineFix (engine v1.2.1), nothing is weakened. The real page count is NOT_MEASURED here (it comes from TK4_Rev_Papers)."}
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
    OWN = "FINDING of the controls of TK4_Rev_Items and TK4_Rev_Engine, recorded 2026-11-02: the engine v1.2.0 refuses the real item set by rule E02 alone (it still calls the item validator v1_1_0) and its rule E33 would refuse a sheet that carries the sheet wording of TK4_Rev_SheetText; with the validator v1_2_0 wired in, the same engine builds the real paper with every rule E01 to E34 passing. Coordinator instruction: tell whether a repair task is needed before Papers (do not weaken E02): yes."
    TASKS = [("TK4_Rev_EngineFix", "Build", "Engine v1.2.1: validator v1.2.0 for E02 and the sheet wording for E33", "Deliverable and checks: see the brief 08-tooling/briefs/exam/r16/BRIEF_TK4_Rev_EngineFix.md (generated by the lineage agent, r16); executor session SEN0414-EX-rev-enginefix; new versioned files in /home/claude/CME/exams/SEN0414, nothing in the public repository; it starts only when TK4_Rev_SheetText_Verify is Done. Estimated 0.7 hours (an estimate, G120). " + OWN, "TK4_Rev_Engine_Verify, ex:TK4_Rev_Items_Verify"),
             ("TK4_Rev_EngineFix_Verify", "Verify", "Verify: engine v1.2.1", "Control by the lineage agent on its own re-runs of the checks named in the brief 08-tooling/briefs/exam/r16/BRIEF_TK4_Rev_EngineFix.md; the claims recomputed on the files in the private CME repository, no existing file changed, everything committed to CME; an incomplete run is a result, not a pass. Estimated 0.4 hours (an estimate, G120).", "TK4_Rev_EngineFix")]
    RD = now
    for k, typ, title, note, dep in TASKS:
        add.append('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:Iter_Ex3 ; backlog:admittedByOutput ex:Out4_Backlog ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n    backlog:hasInvestmentCategory backlog:Cat_Compliance ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n    backlog:dependsOn ex:%s ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n' % (k, W.lit(title), k, W.lit(title), typ, dep, W.lit(note)))
        add.append('ex:Refine5f_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_Ex3 ; backlog:hasWorkKind backlog:WorkKind_Preparation ;\n    backlog:hasRefinementOutcome "Refined from the controls of the items and the engine of 2026-11-02: brief r16, check, estimate and dependencies are written in the item." .\n' % (k, k, k, RD))
        add.append('ex:RC5f_%s a backlog:ReadinessCheck ; rdfs:label "Readiness check of %s"@en ; backlog:checksReadinessOf ex:%s ; backlog:readinessCheckedAt "%s"^^xsd:dateTime ;\n    backlog:hasReadinessCriterion ex:RK5f_%s_1, ex:RK5f_%s_2, ex:RK5f_%s_3 .\n' % (k, k, k, RD, k, k, k))
        for kx, tx in ((1, "The deliverable, its place and its check are written in the item or its brief."), (2, "Every dependency of the item is Done or a task of the same story that precedes it."), (3, "The statements that bound the item are recorded on the story.")):
            add.append('ex:RK5f_%s_%d a backlog:ReadinessCriterion ; rdfs:label %s@en ; backlog:criterionMet true .\n' % (k, kx, W.lit(tx)))
        add.append('ex:Mv5f_%s a backlog:TransitionEvent ; rdfs:label "%s moved to Ready"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Refine ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "Refined (ex:Refine5f_%s) and ready after the readiness check ex:RC5f_%s; no executor has started." .\n' % (k, k, k, RD, k, k))
    marker = "ex:TK4_Rev_SheetText, ex:TK4_Rev_SheetText_Verify ;\n    backlog:hasState backlog:InProgress"
    assert marker in t; t = t.replace(marker, "ex:TK4_Rev_SheetText, ex:TK4_Rev_SheetText_Verify, ex:TK4_Rev_EngineFix, ex:TK4_Rev_EngineFix_Verify ;\n    backlog:hasState backlog:InProgress", 1)
    add.append("ex:Plan5c_ST4_Rev backlog:producesTask ex:TK4_Rev_EngineFix, ex:TK4_Rev_EngineFix_Verify .\nex:Iter_Ex3 backlog:hasMember ex:TK4_Rev_EngineFix, ex:TK4_Rev_EngineFix_Verify .\n")
    i, j = blk(t, "TK4_Rev_Papers"); b_ = t[i:j]; nb_ = b_.replace("ex:TK4_Rev_Items_Verify, ex:TK4_Rev_Engine_Verify ;", "ex:TK4_Rev_Items_Verify, ex:TK4_Rev_Engine_Verify, ex:TK4_Rev_EngineFix_Verify ;", 1); assert nb_ != b_; t = t[:i] + nb_ + t[j:]
    add.append("ex:TK4_Rev_Papers backlog:hasAuditNote %s .\nex:ST4_Rev backlog:hasAuditNote %s .\n" % (W.lit("%s UTC: the task now also depends on TK4_Rev_EngineFix_Verify (engine v1.2.1); its brief addendum names it." % now), W.lit("%s UTC: two more tasks added for the engine finding of the controls (TK4_Rev_EngineFix and its verification, 1.1 hours together, estimates; said openly, the story's job size is not re-estimated)." % now)))
    add.append("".join("<%sUrgent_4> backlog:urgentItem <%s%s> .\n" % ("http://example.org/sen0414-slides-lineage#", "http://example.org/sen0414-slides-lineage#", k_) for k_ in ["TK4_Rev_EngineFix", "TK4_Rev_EngineFix_Verify"]))
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
    out = W.write_new(src, t + "\n" + "".join(add), "Exam revision: TK4_Rev_Items and TK4_Rev_Engine controlled and Done with their verifications (%s); TK4_Rev_EngineFix registered." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
