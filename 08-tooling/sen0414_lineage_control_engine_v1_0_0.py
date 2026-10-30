#!/usr/bin/env python3
"""sen0414_lineage_control_engine v1_0_0 (made from sen0414_lineage_control_exam2_v1_0_0.py) - records the lineage agent's control of the first two executors of box 2 of the exam lineage (Lineage4) on bridge-verified evidence, the Owner's answer of 2026-10-30 about 10:20 Istanbul (30 items per paper),
that the Bloom reading and the chapter weights are NOT yet answered, and the executors' results as reported. A NEW file; ONE new register file. Same method as sen0414_lineage_control_urgent_v1_0_0.py.
  draft OUT.ttl      TestEvidence (command: sen0414_control_exam2_v1_0_0.py CHECK) and ArtifactEvidence nodes
  record BRIDGE.ttl  Done records of the verified groups (a group = a story with its two tasks)"""
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
CTL = "08-tooling/sen0414_control_exam2_v1_1_0.py"; E = "04-assessment/exams/"
G = {"engine": (["TK4_Engine_Core", "TK4_Engine_Core_Verify"], "AC4_Controlled", [E + "exam_engine_v1_0_0.py", E + "exam_engine_shapes_v1_0_0.ttl", E + "exam_engine_fixtures_v1_0_0.json", E + "exam_engine_fixtures_build_v1_0_0.py", E + "exam_engine_check_v1_0_0.py"],
                "the exam assembler as briefed (r5): the executor's check re-run exits 0 (22 fixtures as expected, every rule E01-E19 refused with its fixture, same seed same paper, 54 sheet units accepted by the SEN0401 sheet module) and the controller's own pairs (valid pool builds, same seed twice identical, a pool without chapter 8 refused with E03)")}
STORY = {"ST4_Engine": ["engine"]}
eid = lambda c: "Ev4d_Ctl_" + c
fid = lambda c, i: "Ev4d_CtlFile_%s_%d" % (c, i)
NOTE_ENG = ("RESULT OF THE EXECUTOR of TK4_Engine_Core (real start 2026-10-30T08:53:24Z; commit 1cc2daf; recorded as reported): exam_engine_v1_0_0.py, exam_engine_shapes_v1_0_0.ttl (rules E01 to E19), exam_engine_fixtures_v1_0_0.json, exam_engine_fixtures_build_v1_0_0.py (an extra file the brief did not name), exam_engine_check_v1_0_0.py; the check (about 130 s) shows 22 fixtures as expected, a refusal fixture for every rule, identical forms for the same seed and pool, key data of 100 points per form, a sheet specification of 54 units (bank 15, choice 21, match 10, order 8) accepted by the SEN0401 sheet module in memory (2 pages). "
            "Disclosed by the executor: the paper-level fixtures E07, E08, E12 to E15, E18 and E19 are met by construction (a hand-altered valid paper run through SHACL), E07's fixture names E07 and E08 and E15's names E13, E14 and E15; unreadable pool items are dropped silently before E02; the engine does not enforce 100 total points on a real pool; the indirect minimum is read from the design's decision text with a regex; the Bloom reading is one constant (A1, threshold 3). NOT_MEASURED: a real pool, printing, the reader on SEN0414 sheets.")
GAP = ("CONTROLLER FINDING (own pairs, log control_engine_own_pairs_run1.log): the engine enforces the majority at Bloom 3 or higher (threshold 3, which is the Owner's 'B and C', Apply and above) but NOT his second clause, 'at least 8 of the 30 items at Analyze or above (Bloom 4 or higher)': a pool whose every Bloom 4 and 5 item was set to Bloom 3, so that the paper has 0 items at Analyze and above and 21 of 30 at Apply and above, was built with exit 0 and no refusal. "
       "The engine was briefed on the r5 brief, written before his reading; the rule is a new requirement and is made a repair task, TK4_Engine_Bloom, with its control, in the same story; the Core task is Done for what it was briefed to do, and the story stays in progress.")
TASK_B = ("Make the exam assembler enforce the Owner's Bloom rule: at least 8 of the 30 items at Bloom 4 or higher, as a SHACL rule with a fixture refused", "Build", 
          "Add the Owner's second Bloom clause to the exam engine as NEW files (the committed v1_0_0 files stay): exam_engine_v1_1_0.py, exam_engine_shapes_v1_1_0.ttl, exam_engine_fixtures_v1_1_0.json (the v1_0_0 fixtures plus new ones) and exam_engine_check_v1_1_0.py in 04-assessment/exams. "
          "The Owner's word (relayed, about 10:30 Istanbul on 2026-10-30): 'B and C, but at least 8 work-out-why' per 30-item paper: Apply and above (Bloom 3 or higher) is the majority of the paper AND at least 8 of its 30 items are at Bloom 4 or higher, counted on the whole paper (the minimum 8 is read from a new field of the design or a named constant, never buried in code, and is marked in every build record). "
          "A new rule (the next number after E19) is stated in SHACL and refuses a paper that has fewer than 8 items at Bloom 4 or higher; the assembler's choice of items must be able to meet it when the pool allows (the pool-choice step counts both clauses), and refuses with the rule named when the pool cannot. "
          "Fixtures: a pool that gives a paper with 8 or more at Bloom 4 or higher (accepted), a pool whose paper would have 7 (refused, rule named), a pool with 0 (refused), and one with exactly 8 (accepted); all synthetic and marked so. The check prints the counts of Bloom 3 or higher and of Bloom 4 or higher of every accepted paper, recomputed without SHACL. "
          "Run the v1_0_0 check as well to show nothing it covered is lost. Estimated 1.0 hours (an estimate, G120).")
TASK_V = ("Verify the Bloom clause of the exam assembler on the controller's own re-runs", "Verify", "Control by the lineage agent on its own re-runs: the v1_1_0 check exits 0, a pool with 0 and a pool with 7 items at Bloom 4 or higher are refused with the new rule named, one with 8 is accepted, the v1_0_0 fixtures still give their verdicts, no committed file changed; an incomplete run is a result, not a pass. Estimated 0.4 hours (an estimate, G120).")
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
    for k in ("TK4_Engine_Core", "TK4_Engine_Core_Verify", "ST4_Engine"):
        add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(NOTE_ENG))); add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(GAP)))
    nb_ = W.now()
    add.append('ex:Finding_EngineBloomClause a backlog:RetrospectiveFinding ;\n    rdfs:label "The engine enforces the Bloom majority but not the Owner\'s minimum of 8 at Analyze and above"@en ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:relatesToWorkItem ex:ST4_Engine ; backlog:hasFindingScope backlog:Scope_Methodology ;\n    backlog:hasRootCause %s ;\n    backlog:hasRemedy %s .\n' % (
        W.lit(GAP), W.lit("The repair task TK4_Engine_Bloom with its control TK4_Engine_Bloom_Verify (new files, v1_1_0) makes the engine enforce the second clause; the item-pool briefs (r6) already carry the rule with their shares, so the pools are built to meet it; the task is ranked first in the box because a paper the engine accepts without it would break the Owner's rule.")))
    for tid, (label, typ, text_) in (("TK4_Engine_Bloom", TASK_B[:2] + (TASK_B[2],)), ("TK4_Engine_Bloom_Verify", TASK_V[:2] + (TASK_V[2],))):
        dep = "TK4_Engine_Core_Verify" if tid == "TK4_Engine_Bloom" else "TK4_Engine_Bloom"
        add.append('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:Iter_Ex2 ; backlog:admittedByOutput ex:Out4_Backlog ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
                   '    backlog:hasInvestmentCategory backlog:%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n    backlog:dependsOn ex:%s ;\n'
                   '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n' % (
                       tid, W.lit(label), tid, W.lit(label), "Cat_NewCapability" if typ == "Build" else "Cat_Compliance", typ, dep, W.lit(text_)))
        add.append('ex:Refine4c_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_Ex2 ; backlog:hasWorkKind backlog:WorkKind_Preparation ;\n    backlog:hasRefinementOutcome "Refined by the lineage agent from the controller\'s finding on the engine and the Owner\'s Bloom rule: requirements in the task text, a control, an estimate; the brief is generated from the register." .\n' % (tid, tid, tid, nb_))
        add.append('ex:RC4c_%s a backlog:ReadinessCheck ; rdfs:label "Readiness check of %s"@en ; backlog:checksReadinessOf ex:%s ; backlog:readinessCheckedAt "%s"^^xsd:dateTime ;\n    backlog:hasReadinessCriterion ex:RK4c_%s_1, ex:RK4c_%s_2, ex:RK4c_%s_3 .\n' % (tid, tid, tid, nb_, tid, tid, tid))
        for kx, txt in ((1, "The deliverable, its place and its check are written in the item."), (2, "Every dependency of the item is Done or is a task of the same story that precedes it."), (3, "The Owner's statements that bound the item are recorded in the mission and the scope.")):
            add.append('ex:RK4c_%s_%d a backlog:ReadinessCriterion ; rdfs:label %s@en ; backlog:criterionMet true .\n' % (tid, kx, W.lit(txt)))
        add.append('ex:Mv4c_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Refine ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (tid, W.lit(tid + " moved to Ready"), tid, nb_, W.lit("Recorded at the repair planning after the controller's finding on the engine: refined (ex:Refine4c_%s) and ready after the readiness check ex:RC4c_%s; no executor has started." % (tid, tid))))
    add.append('ex:Plan4c_Engine_Bloom a backlog:PlanningEvent ; rdfs:label "Planning of the engine repair into box 2"@en ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_Ex2 ;\n    backlog:plansItem ex:ST4_Engine ; backlog:producesTask ex:TK4_Engine_Bloom, ex:TK4_Engine_Bloom_Verify ;\n    backlog:refinementProduces ex:Spec4, ex:Scen4_Sound, ex:Scen4_Refused .\n' % nb_)
    add.append("ex:PC4_Iter_Ex2 backlog:includesPlanningEvent ex:Plan4c_Engine_Bloom .\n")
    add.append("ex:ST4_Engine backlog:decomposesInto ex:TK4_Engine_Bloom, ex:TK4_Engine_Bloom_Verify .\nex:Iter_Ex2 backlog:hasMember ex:TK4_Engine_Bloom, ex:TK4_Engine_Bloom_Verify .\n")
    ctl_s = os.path.getmtime(os.path.join(W.REPO, "08-tooling/control-exam-logs/control_engine_check_run1.log"))
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
    add.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit("RANKING after the controller's verdict on the engine (%s UTC): done now %s; held %s. Ranked first in the box: TK4_Engine_Bloom (the engine must enforce the Owner's second Bloom clause), then the item pools TK4_Items_A and TK4_Items_B (already running or next by the coordinator's launch order); the chapter weights remain the lineage agent's default until the Owner answers." % (n, ", ".join(done) or "none", ", ".join(held) or "none")))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam lineage box 2: the controller's verdict on the exam engine (TK4_Engine_Core and its control Done on bridge-verified evidence), the finding that the engine does not enforce the Owner's minimum of 8 at Analyze and above, and the repair task TK4_Engine_Bloom with its control: Done %s%s." % (", ".join(done) or "none", ("; held: " + ", ".join(held)) if held else ""))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
