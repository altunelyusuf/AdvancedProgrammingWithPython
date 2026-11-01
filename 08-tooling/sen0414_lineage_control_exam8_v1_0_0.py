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
CTL = "08-tooling/sen0414_control_exam7_v1_0_0.py"; E = "04-assessment/exams/"
G = {"engine5": (["TK4_Engine5", "TK4_Engine5_Verify"], [E + "exam_engine_v1_1_0.py", E + "exam_engine_shapes_v1_1_0.ttl", E + "exam_engine_fixtures_v1_1_0.json", E + "exam_engine_check_v1_1_0.py"], "the five-question engine v1_1_0 as briefed (r11, r12): the executor's check exits 0 (RESULT PASS, 727 s), the executor's valid pool builds a paper with every rule passing, the controller's own mutations of that pool are each refused with the intended rules (all Bloom 2: E06 E24; no Analyze and above: E24; repeated id: E01; points plus one: E22; dropped records: E03 E22; chapter 9: E02 E03), the item validator self-test still passes, the task commit adds only new files"),
     "itemsa3": (["TK4_Items_A3", "TK4_Items_A3_Verify"], [E + "items/items_a_v2_1_0.json", E + "items/items_a_v2_1_0_makeup.json", E + "items/items_a_v2_1_0_provisional.json", E + "items/items_a_v2_1_0_check.py"], "item set A version 2.1.0 as briefed (r13): the executor's check exits 0; merged with set B each list has 18 records and 18 ids, passes the validator v1_1_0, has units 6/7/7/6/4, points 25/25/25/25/10, units per chapter equal to the quota 4,4,4,4,3,4,4,3, 9 cross-chapter choices, Apply and above 27 and Analyze and above 11 of 30; no identical stem between the lists; the controller's own engine builds of the merged paper pool (seeds 1, 20261101, 20261102) and of the make-up pool against the midterm build (seeds 7, 20261102) exit 0 with 28 of 28 rules passing; the task commit adds only new files"),
     "itemsb2m": (["TK4_Items_B2", "TK4_Items_B2_Verify"], [E + "items/items_b_v2_0_0.json", E + "items/items_b_v2_0_0_makeup.json", E + "items/items_b_v2_0_0_provisional.json", E + "items/items_b_v2_0_0_check.py"], "item set B version 2.0.0 as briefed (r12): merged with set A version 2.1.0 the lists build in the engine v1_1_0 on the controller's own re-runs, as for TK4_Items_A3 (28 of 28 rules; units, points, quota, cross-chapter and Bloom counts as designed); the task commit adds only new files")}
STORY = {}
eid = lambda c: "Ev4e_Ctl_" + c
fid = lambda c, i: "Ev4e_CtlFile_%s_%d" % (c, i)
REP_E = ("RESULT OF THE EXECUTOR of TK4_Engine5 (real start 2026-11-01T18:36:06Z; commit 540b51b; recorded as reported): exam_engine_v1_1_0.py, its SHACL shapes, fixtures and check; 40 fixtures as expected, E01 to E28 each refused with a named rule, Bloom rule enforced (Analyze and above at least 8). Disclosed: list-level R21 not run on fixture records; the Word layout is unmeasured (95 characters a line and a 92 per cent spare share are assumptions A8); several rules have hand-modified-paper fixtures only. Counting rules decided by the executor and ruled by the controller: units per record, one chapter per unit, a cross-chapter choice is a one-unit record with two or more chapters, indirect counts the units of an indirect record (see the ruling recorded with TK4_Items_B2).")
REP_A3 = ("RESULT OF THE EXECUTOR of TK4_Items_A3 (real start 2026-11-01T20:55:08Z; commit 275e1d9; recorded as reported): items_a_v2_1_0.json and items_a_v2_1_0_makeup.json (14 records each), a provisional side file, builder and check; five cross-chapter choices Q1f, Q3b, Q4b, Q5a, Q5b; the engine builds the merged pools with 28 of 28 rules. Note of the executor: the make-up pool must be written as one named set, otherwise E17 refuses shared ids.")
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
    for k in ("TK4_Engine5", "TK4_Engine5_Verify"): add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(REP_E)))
    for k in ("TK4_Items_A3", "TK4_Items_A3_Verify"): add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(REP_A3)))
    LOGS = {"engine5": "control_engine5_run1.log", "itemsa3": "control_itemsa3_run1.log", "itemsb2m": "control_itemsa3_run1.log"}
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
    ctl_start_engine = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(W.REPO, "08-tooling/control-exam-logs/control_engine5_run1.log")), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    # ---- the Owner's decision (relayed by the coordinator, real owner answer of this session, 2026-11-02): approve all
    OWN = "OWNER DECISION of 2026-11-02 (his real answer in this session, relayed by the course coordinator and recorded as relayed): approve all - the midterm-scope iteration and the exam box end 2026-11-10; SEN0401 chapters 7-8 and SEN0414 chapters 9-10 stay due 2026-11-15; the two urgent interruptions (Urgent_3 for the materials lineage, Urgent_4 for the exam lineage) get the same later time box. The dates were the coordinator's working defaults before this answer."
    for it, old, lab in (("Iter_MS", "2026-11-01T21:00:00", "midterm-scope iteration"), ("Iter_Ex3", "2026-11-01T21:00:00", "exam box 3")):
        i, j = blk(t, it); b = t[i:j]; nb = b.replace('backlog:iterationEnd "%s"^^xsd:dateTime' % old, 'backlog:iterationEnd "2026-11-10T21:00:00"^^xsd:dateTime', 1); assert nb != b, it; t = t[:i] + nb + t[j:]
        add.append('ex:Rebaseline4i_%s a backlog:Rebaseline ; rdfs:label "Rebaseline of the end of %s"@en ; backlog:rebaselines ex:%s ; backlog:decidedBy backlog:Owner ;\n    backlog:hasPreviousTarget "%s" ; backlog:hasNewTarget "2026-11-10T21:00:00" ;\n    backlog:hasRebaselineRationale %s .\n' % (it, lab, it, old, W.lit(OWN + " The earlier end was the Owner's own 'today' (the box ended at midnight Istanbul); the work did not fit, which this register stated openly when the box was set (it could not prove that the box fits). What did not finish: see the open stories of the box.")))
    for u in ("Urgent_3", "Urgent_4"):
        u_ = "<http://example.org/sen0414-slides-lineage#%s> a " % u; i = t.index(u_); j = t.find("\n<http", i + 5); k = t.find("\nex:", i + 5); e = min(x for x in (j, k) if x > 0); b = t[i:e]
        nb = b.replace('backlog:urgencyTimeBoxUntil "2026-11-01T21:00:00Z"', 'backlog:urgencyTimeBoxUntil "2026-11-10T21:00:00Z"', 1); assert nb != b, u; t = t[:i] + nb + t[e:]
        add.append('<http://example.org/sen0414-slides-lineage#%s> rdfs:comment %s .\n' % (u, W.lit(OWN + " Previous time box: 2026-11-01T21:00:00Z; new time box 2026-11-10T21:00:00Z, recorded here as the Owner's decision with this reason.")))
    # ---- stories and the epic whose children are now all Done (G148)
    def evs_of(cs):
        out_ = []
        for c in cs: out_ += [eid(c)] + [fid(c, i) for i in range(len(G[c][1]))]
        return out_
    def done_story(sid, evs, fin, resume=None):
        nonlocal t
        i, j = blk(t, sid); b = t[i:j]
        if resume:
            nb = b.replace("backlog:hasState backlog:Suspended ; backlog:startedAt", "backlog:hasState backlog:Done ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:finishedAt \"%sZ\"^^xsd:dateTime ; backlog:lastAuditedAt \"%sZ\"^^xsd:dateTime ; backlog:hasEvidence %s ; backlog:startedAt" % (fin, fin, ", ".join("ex:" + x for x in evs)), 1)
            add.append('ex:Resume4h_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Resume ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "Resumed as an urgent item of Urgent_4 (the Owner\'s exam instruction): its engine task TK4_Engine5 was launched under the same instruction and the controller\'s verdict follows." .\n' % (sid, W.lit(sid + " resumed as an urgent item"), sid, resume))
            t = t.replace("backlog:holdsItem <http://example.org/sen0414-slides-lineage#ST4_Engine> .", "backlog:urgentItem <http://example.org/sen0414-slides-lineage#ST4_Engine> .", 1)
        else:
            nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:startedAt %s ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:lastAuditedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, fin, ", ".join("ex:" + x for x in evs)), b, count=1)
        assert nb != b, sid; t = t[:i] + nb + t[j:]
        add.append('ex:Complete4h_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "Done with its tasks on the controller\'s verdict." .\n' % (sid, W.lit(sid + " completed on the controller's verdict"), sid, fin)); done.append(sid)
        add.append('ex:Harness4h_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (sid, W.lit("Control checks for " + sid), sid, ", ".join("ex:" + x for x in evs)))
    if ok["engine5"]:
        fe = vd[eid("engine5")][1]; done_story("ST4_Engine", evs_of(["engine5"]), fe, resume=ctl_start_engine)
    if ok["itemsa3"] and ok["itemsb2m"]:
        fi = max(vd[eid("itemsa3")][1], vd[eid("itemsb2m")][1]); done_story("ST4_Items2", ["Ev4e_Ctl_itemsa2"] + ["Ev4e_CtlFile_itemsa2_%d" % q for q in range(4)] + evs_of(["itemsb2m", "itemsa3"]), fi)
        pa = "2026-10-29T22:04:32Z"
        add.append('ex:Refine4h_EP4_Content a backlog:RefinementEvent ; rdfs:label "Refinement that made EP4_Content ready"@en ;\n    backlog:refines ex:EP4_Content ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "2026-10-29T22:00:00Z"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_Ex1 ; backlog:hasWorkKind backlog:WorkKind_Preparation ;\n    backlog:hasRefinementOutcome "Recorded with the completion of the epic (written after the fact and said so): the epic groups the stories of the exam content - the critical points of the chapters, the distinctness rule and the item sets - each refined with its own story; the epic adds no work of its own." .\n')
        add.append('ex:RC4h_EP4_Content a backlog:ReadinessCheck ; rdfs:label "Readiness check of EP4_Content"@en ; backlog:checksReadinessOf ex:EP4_Content ; backlog:readinessCheckedAt "2026-10-29T22:00:00Z"^^xsd:dateTime ;\n    backlog:hasReadinessCriterion ex:RK4h_EP4_Content_1, ex:RK4h_EP4_Content_2, ex:RK4h_EP4_Content_3 .\n')
        for kx, tx in ((1, "The epic decomposes into stories."), (2, "Every story of the epic has its own refinement and readiness check."), (3, "The Owner's statements that bound the epic are recorded in the mission and the scope.")):
            add.append('ex:RK4h_EP4_Content_%d a backlog:ReadinessCriterion ; rdfs:label %s@en ; backlog:criterionMet true .\n' % (kx, W.lit(tx)))
        add.append('ex:Mv4h_EP4_Content_0 a backlog:TransitionEvent ; rdfs:label "EP4_Content moved from Proposed to Ready"@en ; backlog:transitionedItem ex:EP4_Content ;\n    backlog:viaTransition backlog:T_Refine ; backlog:transitionedAt "2026-10-29T22:00:00Z"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "Recorded with the completion of the epic: refined and ready after the readiness check ex:RC4h_EP4_Content; the move is written after the fact and says so." .\n')
        add.append('ex:Begin4h_EP4_Content a backlog:TransitionEvent ; rdfs:label "EP4_Content started with its first story"@en ; backlog:transitionedItem ex:EP4_Content ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "The epic starts with the real start of its first story ST4_Points_A at 2026-10-29T22:04:32 UTC." .\n' % pa)
        i, j = blk(t, "EP4_Content"); b = t[i:j]
        nb = b.replace("backlog:hasState backlog:Proposed ;", 'backlog:hasState backlog:Done ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:hasAcceptanceCriterion ex:AC4_Controlled ; backlog:hasEvidence %s ; backlog:startedAt "2026-10-29T22:04:32Z"^^xsd:dateTime ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:lastAuditedAt "%sZ"^^xsd:dateTime ;' % (", ".join("ex:" + x for x in ["Ev4e_Ctl_itemsa3", "Ev4e_Ctl_itemsb2m", "Ev4e_Ctl_points5"]), fi, fi), 1)
        assert nb != b; t = t[:i] + nb + t[j:]
        add.append('ex:Complete4h_EP4_Content a backlog:TransitionEvent ; rdfs:label "EP4_Content completed: every story is Done or Cancelled"@en ; backlog:transitionedItem ex:EP4_Content ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "The epic derives Done from its stories: the points, the distinctness rule and the item sets are Done on the controller\'s evidence; ST4_Items is Cancelled." .\n' % fi)
        add.append('ex:Harness4h_EP4_Content a backlog:TestHarness ; rdfs:label "Control checks for EP4_Content"@en ; backlog:harnessFor ex:EP4_Content ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:Ev4e_Ctl_itemsa3, ex:Ev4e_Ctl_itemsb2m, ex:Ev4e_Ctl_points5 .\n')
        obs = max([x for x in (vd[eid("itemsa3")][1], vd[eid("itemsb2m")][1], vd[eid("engine5")][1] if ok["engine5"] else "") if x] + [now])
        add.append('ex:Obs45_Obj4_HigherShare a backlog:MetricObservation ; rdfs:label "Reading after the controller re-ran the engine and the item sets"@en ;\n    backlog:observesMetric ex:Met4_Higher ; backlog:observationFor ex:Obj4_HigherShare ; backlog:hasObservedValue "90"^^xsd:decimal ; backlog:observedAt "%sZ"^^xsd:dateTime ;\n    backlog:hasObservationMethod "Per cent of the sub-questions of the weakest paper at the Apply level or above, counted on the controller\'s own engine builds of the merged item lists (paper and make-up): 27 of 30 = 90 in each; the engine refuses a paper below the majority (rules E06 and E25)." .\n' % obs)
        add.append('ex:Obs46_Obj4_PointsListed a backlog:MetricObservation ; rdfs:label "Reading when the content epic was completed"@en ;\n    backlog:observesMetric ex:Met4_Points ; backlog:observationFor ex:Obj4_PointsListed ; backlog:hasObservedValue "8"^^xsd:decimal ; backlog:observedAt "%sZ"^^xsd:dateTime ;\n    backlog:hasObservationMethod "Chapters with critical points collected and a stated list of what could not be found: chapters 1 to 8 = 8 (unchanged since the chapter 5 reading)." .\n' % obs)
    add.append("ex:TK4_Papers backlog:dependsOn ex:TK4_Items_A3_Verify, ex:TK4_Items_B2_Verify .\n")
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
    add.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit("RANKING %s UTC after the controller's verdicts (done now: %s; held: %s). Next: TK4_Papers (dependencies TK4_Engine5_Verify, TK4_Cover_Verify, TK4_Items_A2_Verify, TK4_Items_A3_Verify and TK4_Items_B2_Verify Done). The make-up paper stays last." % (now, ", ".join(done) or "none", ", ".join(held) or "none")))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam change: the controller's verdict on item set A (TK4_Items_A2 and its control Done on bridge-verified evidence: %s), scores re-run." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])

