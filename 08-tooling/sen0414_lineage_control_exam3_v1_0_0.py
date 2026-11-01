#!/usr/bin/env python3
"""sen0414_lineage_control_exam3 v1_0_0 (made from sen0414_lineage_control_engine_v1_0_0.py) - records the lineage agent's control of the first two executors of the exam change (TK4_Design2, TK4_Cover) on bridge-verified evidence, and opens the small task TK4_Points5
(critical points of chapter 5, the blocker found by the design executor). ONE new register file.
  draft OUT.ttl      TestEvidence (command: sen0414_control_exam3_v1_0_0.py CHECK) and ArtifactEvidence nodes
  record BRIDGE.ttl  Done records of the verified groups, then the Points5 story and tasks, urgent items, scores"""
__version__ = "1.0.0"
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
NS = "http://example.org/sen0414-slides-lineage#"
CTL = "08-tooling/sen0414_control_exam3_v1_0_0.py"; E = "04-assessment/exams/"
G = {"design2": (["TK4_Design2", "TK4_Design2_Verify"], [E + "exam_design_v1_2_0.md", E + "exam_design_v1_2_0.json", E + "exam_design_check_v1_2_0.py"],
                 "the five-question design v1_2_0 as briefed (r10): the executor's design check exits 0 and the controller's own recount of the JSON holds (30 sub-questions 6/7/7/6/4, points 25/25/25/25/10, no Bloom 1, Apply and above 27 of 30, Analyze and above 11, chapters 1 to 8, every sub-question asks use, reason or effect), the commit adds only new files"),
     "cover": (["TK4_Cover", "TK4_Cover_Verify"], [E + "exam_cover_v1_0_0.py", E + "exam_cover_check_v1_0_0.py"],
               "the cover page renderer as briefed (r10): the executor's check exits 0 and the controller's own build of midterm form A and make-up form B renders to one page each (LibreOffice), carries no wording of the template's course, has the grade table (four /25 rows, a /10 bonus row, total /100 plus bonus), the template is not in the repository, the commit adds only new files; page 1 of form A read as an image")}
STORY = {"ST4_Cover": ["cover"]}
eid = lambda c: "Ev4e_Ctl_" + c
fid = lambda c, i: "Ev4e_CtlFile_%s_%d" % (c, i)
REP_D = ("RESULT OF THE EXECUTOR of TK4_Design2 (real start 2026-11-01T16:28:08Z; commit bc305be; recorded as reported): exam_design_v1_2_0.md and .json and exam_design_check_v1_2_0.py; check RESULT PASS (38 decisions; 30 sub-questions 6/7/7/6/4; points 25/25/25/25 plus 10 bonus; Apply and above 27 of 30, Analyze and above 11; 6 pages shown necessary, 4 not possible; 31 sheet units, one sheet page). "
         "Defaults taken (the coordinator accepted them and tells the Owner): the bonus adds to the total up to 110; the sheet title is overprinted. BLOCKER reported by the executor: no critical-points file exists for chapter 5, which the item rules need for its 3 sub-questions; opened as the task TK4_Points5. Controller note: the design says 6 pages (cover, four question pages, one sheet page); the Owner's rule is 4 pages if it fits, else 6; the design shows why 4 does not fit.")
REP_C = ("RESULT OF THE EXECUTOR of TK4_Cover (real start 2026-11-01T16:28:08Z; commit bea6a20; recorded as reported): exam_cover_v1_0_0.py (a copy of the SEN0401 renderer plus cover_sen0414) and exam_cover_check_v1_0_0.py; check RESULT PASS (22 PASS lines per build; midterm form A and make-up form B one page each, 5.6 per cent free). "
         "Disclosed by the executor: the first run FAILED (4.1 per cent free) and was fixed by shortening instruction lines, the check not weakened; instruction items 3 and 4 changed; the form letter is in the title line; the outcomes file maps learning outcomes only to chapters 1 (1, 4), 5 (6) and 8 (2), so the default lists 1, 2, 4, 6 for every question and the paper builder must pass its own list per question; program outcomes stay blank. Controller note: the outcomes file maps by the textbook chapters in its source lines, not by the course chapters; the default list is therefore a disclosed stand-in, not a measured mapping.")
SPEC5 = ("Collect the critical points of chapter 5 (Debugging) from the deck, speaker notes, corpus and stories, and list what could not be found", "Build",
         "Chapter 5 now belongs to the exams (the coordinator assumed it in and asked the Owner once), and the design v1_2_0 gives it 3 sub-questions, but no critical-points file exists for it: the chapters 1 to 4 and 6 to 8 have theirs (TK4_Points_A and TK4_Points_B). Write 04-assessment/exams/critical_points_ch05_v1_0_0.json (a list of objects with exactly the keys chapter (the integer 5), point, why_critical, source_file, place, evidence_kind, as in critical_points_ch06_08_v1_0_0.json) and 04-assessment/exams/critical_points_ch05_not_found_v1_0_0.md (a plain list of what you looked for and could not find or confirm as the instructor's own emphasis, as questions the Owner can answer in one line each). "
         "At least 4 points, 8 or more if the chapter supports them; read the newest committed deck of chapter 5 and its speaker notes (03-materials/ch05/SEN0414_Ch05_Debugging_3e_v*.pptx; the chapter-5 build executor is producing a newer deck: use the newest committed at your start and name its version), the corpus 08-tooling/sen0414_ch05_corpus_v*.py and the stories 08-tooling/sen0414_ch05_stories_v*.py (newest of each; if a file does not exist say so in the not-found list), and the chapter's ontology under 03-materials/ch05/rdodi for what the chapter names as common mistakes. A point is critical when the deck stresses it, the notes explain it at length, or the corpus or a story ties it to a common mistake. Every place must exist (slide number in range; notes present; a quoted fragment of at most 120 characters found in the file). New files only; nothing under 03-materials is changed. Estimated 1.0 hours (an estimate, G120).")
VER5 = "Control by the lineage agent on its own re-runs: the structure and source checks of the critical-points files (the file parses with exactly the keys, the chapter is 5, at least 4 points, every source file exists, every place exists, the not-found list has a chapter 5 section), the commit adds only new files, everything committed; an incomplete run is a result, not a pass. Estimated 0.5 hours (an estimate, G120)."
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
    for k in ("TK4_Design2", "TK4_Design2_Verify", "ST4_DesignRev2"): add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(REP_D)))
    for k in ("TK4_Cover", "TK4_Cover_Verify", "ST4_Cover"): add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(REP_C)))
    ctl_start = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(W.REPO, "08-tooling/control-exam-logs/control_design_v1_2_0_run1.log")), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    for c in G:
        tasks, files, what = G[c]
        if not ok[c]: held += tasks; continue
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
    for sid, groups in STORY.items():
        if all(ok[c] for c in groups):
            fin = max(vd[eid(c)][1] for c in groups); evs = []
            for c in groups: evs += [eid(c)] + [fid(c, i) for i in range(len(G[c][1]))]
            i, j = blk(t, sid); b = t[i:j]
            nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:startedAt %s ; backlog:finishedAt "%sZ"^^xsd:dateTime ; backlog:lastAuditedAt "%sZ"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, fin, ", ".join("ex:" + x for x in evs)), b, count=1)
            assert nb != b, sid; t = t[:i] + nb + t[j:]
            add.append('ex:Complete4f_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "Done with its tasks on the controller\'s verdict." .\n' % (sid, W.lit(sid + " completed on the controller's verdict"), sid, fin)); done.append(sid)
            add.append('ex:Finding_CoverPapersMetric a backlog:RetrospectiveFinding ;\n    rdfs:label "The cover page was asserted to move the papers metric and cannot"@en ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:relatesToWorkItem ex:ST4_Cover ; backlog:hasFindingScope backlog:Scope_Methodology ;\n    backlog:hasRootCause %s ;\n    backlog:hasRemedy %s .\n' % (W.lit("The story ST4_Cover was asserted (version 2.353.0) as able to move the objective Obj4_PapersBuilt (printed exam papers with their printed answer key). Its deliverable is the cover page renderer, one page of a paper; no complete paper with its key exists, so the metric cannot move by it and the reading after the story is 0, as before. The assertion was the lineage agent's, made because every paper needs a cover; it confused a part of a paper with a paper."), W.lit("The reading stays 0 and is recorded as 0. The metric is moved by the story ST4_Papers (paper, key and sheet); the stories ST4_DesignRev2, ST4_Engine and ST4_Items2 are inputs of it and are read the same way when they reach Done.")))
            add.append('ex:Harness4f_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (sid, W.lit("Control checks for " + sid), sid, ", ".join("ex:" + eid(c) for c in groups)))
            add.append('ex:Obs43_Obj4_PapersBuilt a backlog:MetricObservation ; rdfs:label "Reading after the controller re-ran the checks (ST4_Cover)"@en ;\n    backlog:observesMetric ex:Met4_Papers ; backlog:observationFor ex:Obj4_PapersBuilt ; backlog:hasObservedValue "0"^^xsd:decimal ; backlog:observedAt "%sZ"^^xsd:dateTime ;\n    backlog:hasObservationMethod "No complete printed paper with its key exists yet: 0 (the cover page renderer, the design and the item rules are parts, not a paper). The cover renderer builds one-page covers for midterm form A and make-up form B; the engine, the items and the paper builder are not built." .\n' % now)
    # ---- the new small task TK4_Points5 (blocker found by the design executor)
    sid = "ST4_Points5"; kids = ["TK4_Points5", "TK4_Points5_Verify"]; size = 1.5; rr = 8; v = (20 + 20 + rr) / size
    add.append('\nex:%s a backlog:Story ; rdfs:label "Critical points of chapter 5 (Debugging)"@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle "Critical points of chapter 5 (Debugging)" ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:Iter_Ex3 ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput ex:Out4_Backlog ;\n'
               '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "the critical points the instructor explained in chapter 5, collected with their sources, and a plain list of what could not be found" ; backlog:soThat "the items of chapter 5 in the printed papers are built from the course\'s own critical points, like those of the other chapters" ;\n'
               '    backlog:satisfiesDeliverable ex:Del4_Points ; backlog:pursuesObjective ex:Obj4_PointsListed ; backlog:hasAcceptanceCriterion ex:AC4_Controlled ;\n    backlog:coversEntity ex:DE4_ExamPaper ; backlog:coversStage backlog:Stage_Creation ;\n    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n    backlog:decomposesInto ex:TK4_Points5, ex:TK4_Points5_Verify ;\n    backlog:hasState backlog:Ready ;\n    backlog:hasPriorityScore ex:Score4f_%s ;\n    backlog:hasAuditNote %s .\n' % (sid, sid, sid, W.lit("Blocker found by the design executor (2026-11-01): the design v1_2_0 gives chapter 5 three sub-questions but no critical-points file exists for it (the Owner's 2026-10-29 exclusion of chapter 5 was replaced by his 'Chapter 1-4 & 5-8' of 2026-11-01). A small file-only task, ranked ahead of the item-rules, engine and item tasks because the items of chapter 5 cite it.")))
    add.append("ex:EP4_Content backlog:decomposesInto ex:%s .\nex:Obj4_PointsListed backlog:metricMovableBy ex:%s .\n" % (sid, sid))
    for k, (title, typ, text_) in (("TK4_Points5", (SPEC5[0], "Build", SPEC5[2])), ("TK4_Points5_Verify", ("Verify the critical points of chapter 5 on the controller's own re-runs", "Verify", VER5))):
        isv = typ == "Verify"
        add.append('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:Iter_Ex3 ; backlog:admittedByOutput ex:Out4_Backlog ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
                   '    backlog:hasInvestmentCategory backlog:%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n%s    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n' % (
                       k, W.lit(title), k, W.lit(title), "Cat_Compliance" if isv else "Cat_NewCapability", typ, "    backlog:dependsOn ex:TK4_Points5 ;\n" if isv else "", W.lit(text_ if isv else "Deliverable: " + text_ + " Executor session SEN0414-EX-points5; brief 08-tooling/briefs/exam/r10/BRIEF_TK4_Points5.md.")))
    for x in (sid,) + tuple(kids):
        add.append('ex:Refine4f_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%sZ"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_Ex3 ; backlog:hasWorkKind backlog:WorkKind_Preparation ;\n    backlog:hasRefinementOutcome "Refined from the design executor\'s blocker report: the file format is that of the existing critical-points files, the checks exist, the estimate and the brief are written." .\n' % (x, x, x, now))
        add.append('ex:RC4f_%s a backlog:ReadinessCheck ; rdfs:label "Readiness check of %s"@en ; backlog:checksReadinessOf ex:%s ; backlog:readinessCheckedAt "%sZ"^^xsd:dateTime ;\n    backlog:hasReadinessCriterion ex:RK4f_%s_1, ex:RK4f_%s_2, ex:RK4f_%s_3 .\n' % (x, x, x, now, x, x, x))
        for kx, tx in ((1, "The deliverable, its place and its check are written in the item."), (2, "Every dependency of the item is Done or a task of the same story that precedes it."), (3, "The Owner's statements that bound the item are recorded in the mission and the scope.")):
            add.append('ex:RK4f_%s_%d a backlog:ReadinessCriterion ; rdfs:label %s@en ; backlog:criterionMet true .\n' % (x, kx, W.lit(tx)))
        add.append('ex:Mv4f_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Refine ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (x, W.lit(x + " moved to Ready"), x, nowZ, W.lit("Refined (ex:Refine4f_%s) and ready after the readiness check ex:RC4f_%s; no executor has started." % (x, x))))
    add.append('ex:Score4f_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%sZ"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (sid, v, now, W.lit("WSJF = (business value 20 + time criticality 20 + risk reduction %d) / job size %.1f h = %.2f. Time criticality 20: the Owner's same-day order. Risk reduction %d: the items of chapter 5 cite this file; without it three sub-questions of every paper have no controlled source, and it blocks the item sets. Scored %s UTC; ranked first: the repair-like blocker re-ranks the open exam items." % (rr, size, v, rr, now))))
    add.append('ex:Plan4f_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into box 3"@en ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:plannedAt "%sZ"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_Ex3 ;\n    backlog:plansItem ex:%s ; backlog:producesTask ex:TK4_Points5, ex:TK4_Points5_Verify ;\n    backlog:refinementProduces ex:Spec4, ex:Scen4_Sound, ex:Scen4_Refused .\n' % (sid, sid, now, sid))
    add.append("ex:PC4_Iter_Ex3 backlog:includesPlanningEvent ex:Plan4f_%s .\nex:Iter_Ex3 backlog:hasMember ex:%s, ex:TK4_Points5, ex:TK4_Points5_Verify .\n" % (sid, sid))
    for m in (sid, "TK4_Points5", "TK4_Points5_Verify"): add.append("<%sUrgent_4> backlog:urgentItem <%s%s> .\n" % (NS, NS, m))
    add.append("ex:TK4_Items_A2 backlog:dependsOn ex:TK4_Points5_Verify .\n")
    # re-score open stories of the exam lineage (a score older than a completion is stale)
    for s2 in sorted(set(re.findall(r"\nex:(ST\w*?_\w+) a backlog:Story", t))):
        i, j = blk(t, s2); b = t[i:j]
        m = re.search(r"backlog:hasPriorityScore ex:Score(\d+[a-z]?)_%s\b" % s2, b)
        if not m or "backlog:hasState backlog:Done" in b or "backlog:hasState backlog:Cancelled" in b or s2 == "ST4_Points5": continue
        if ("\nex:Score%s_%s a" % (kk if False else m.group(1), s2)) not in t: continue
        kk = m.group(1); k0 = t.index("\nex:Score%s_%s a" % (kk, s2)) + 1; r0 = t[k0:t.find("\nex:", k0 + 1)]
        q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0)
        if not q: continue
        nk = (kk[:-1] + chr(ord(kk[-1]) + 1)) if kk[-1].isalpha() else str(int(kk) + 1); nid = "Score%s_%s" % (nk, s2)
        if ("ex:" + nid + " a ") in t: continue
        bv, tc, rrr, size_ = int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4)); val = (bv + tc + rrr) / size_
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:" + nid, 1) + t[j:]
        add.append('ex:%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%sZ"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (nid, val, now, W.lit("WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. RE-RUN on %s UTC after the controller's completions (%s) and the entry of ST4_Points5: the earlier record predates them. Inputs unchanged." % (bv, tc, rrr, size_, val, now, ", ".join(done)))))
    add.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit("RANKING %s UTC after the controller's verdicts (done now: %s; held: %s) and the entry of the blocker task: 1 ST4_Points5 (TK4_Points5, file-only, 1.0 h, no dependency), 2 ST4_DesignRev2 (TK4_ItemRules2 is startable: its dependency TK4_Design2_Verify is Done), then ST4_Engine (TK4_Engine5, after TK4_ItemRules2_Verify), ST4_Items2 (TK4_Items_A2 after TK4_ItemRules2_Verify and TK4_Points5_Verify), ST4_Papers. The make-up paper stays last." % (now, ", ".join(done) or "none", ", ".join(held) or "none")))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam change: the controller's verdicts on the design v1_2_0 and the cover renderer (TK4_Design2, TK4_Cover and their controls Done on bridge-verified evidence: %s), the blocker task TK4_Points5 (critical points of chapter 5) opened and ranked first, scores re-run." % (", ".join(done) or "none"))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
