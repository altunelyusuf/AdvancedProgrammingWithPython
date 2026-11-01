#!/usr/bin/env python3
"""sen0414_lineage_examchange v1_0_0 - records the Owner's exam instruction of 2026-11-01 13:04 Istanbul (relayed) in the exam lineage (Lineage4): the finding with the impact and the as-is fit-gap of the items it supersedes,
the supersession (Cancelled with a rationale) of TK4_Engine_Bloom and TK4_Items_A/B with their stories' tasks, five stories with fourteen tasks (Ready), a new box Iter_Ex3, scores (re-ranking), and the new tasks named as urgent items of the open
interruption Urgent_4 (the Owner's 12:26 'finish both the Midterms and midterm scope work'). ONE new register version.  Usage: sen0414_lineage_examchange_v1_0_0.py record"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
lit = W.lit
assert sys.argv[1:2] == ["record"], __doc__
NS = "http://example.org/sen0414-slides-lineage#"
WORD = ("OWNER INSTRUCTION of 2026-11-01 at 13:04 Istanbul (10:04 UTC), relayed by the course coordinator and recorded as relayed: 'Use the attached page and fill the generic parts appropriately for each of the exams. Categorize the exam into 5 question format with possible number of sub-questions. If possible 4 questions 25 points and 5th Question is 10 points and bonus. "
        "If you can fit overall exam in 4 pages it is fine, otherwise, fit with 6 pages but better formatting and readibility. The abbreviations should be used in full form in their first usage. Never ask memorizing questions and don't force the students to remember a specific terminology. You should support the students with provide tips to remember, if you use a specific term in the exam.' "
        "Read as: (1) page 1 is the cover page from his template; (2) five questions, Q1 to Q4 25 points each, Q5 10 points and a bonus; (3) 4 pages in total, else 6 with better layout; (4) no memorisation item, a tip with every term, abbreviations spelled out at first use (for SEN0414: not syntax trivia, why a construct exists and how it is used matters more than its name). "
        "Accepted by the course coordinator on 2026-11-01 (after the lineage agent's proposal): paper and key as editable .docx; the answer sheet stays a position-exact PDF because the reader needs exact bubble positions (same choice as the SEN0401 owner); chapter 5 assumed in, the Owner asked once; the template stays outside this public repository.")
ROUTE = ("Route: the Owner's same-day order of 12:13/12:26 ('Today we should finish both the Midterms and midterm scope work') already pauses the exam lineage by the urgent interruption Urgent_4. The exam change is the 'Midterms' half of that order, so its stories and tasks are named as URGENT ITEMS of Urgent_4 "
         "(framework ruling G158: urgent items are not admitted by a scope change, and a paused lineage does not carry on except its urgent items). Recorded as a finding with the impact and not as a ChangeRequest, the same route as the cancellation of the Chapter 8 repair. Urgent_4 ends at 2026-11-01T21:00:00Z; the exam chain (about 10 hours on its critical path) cannot be proven to fit, so a later time box needs the Owner's word at the end of the box; until then nothing is waived and no gate is weakened.")
IMPACT = ("IMPACT (lineage agent, 2026-11-01). SUPERSEDED, with the as-is fit-gap: TK4_Engine_Bloom (Ready, never started; asked the v1_1_0 engine to enforce 8 of 30 at Analyze and above on the 30-item single list) is carried by TK4_Engine5, which builds the five-question assembler with that rule; TK4_Items_A and TK4_Items_B (Ready, never started; item pools for the 30-item single list, chapters 1-4 and 6-8) are replaced by TK4_Items_A2 and TK4_Items_B2 "
          "(five question formats, chapters 1-8, no recall, tips, spelled-out abbreviations, asks use/reason/effect), and their story ST4_Items by ST4_Items2. ACCOMPLISHED and kept: the near-copy rule, the critical points of chapters 1-4 and 6-8, the design v1_1_0 (stays as committed), the engine v1.0.0 and its control. FAILED: nothing. IN PROGRESS: ST4_Engine (held; its Core task Done; its Bloom task is cancelled; the story is closed at the resume of the lineage). DUE: new design v1_2_0, item validator v1_1_0, engine v1_1_0, cover, items A2/B2, papers. "
          "CLOSURE STATEMENT: the four cancelled tasks and the cancelled story end CANCELLED, superseded by the items named above; their obligations (near-copy rule, Bloom clauses, sources, controls) are carried by the new tasks and by the briefs r10. The sheet reading: sheet PDF (SEN0401 module), paper and key .docx. Chapter 5 is assumed in (Owner asked once by the coordinator); if he excludes it, only the chapter weights in design v1_2_0 and the pools change.")
# id: (story, title, type, hours, deps, session, note)
T = [
 ("TK4_Design2", "ST4_DesignRev2", "Revise the design of the papers to the five-question structure (design v1_2_0)", "Build", 1.0, [], "SEN0414-EX-design2", "04-assessment/exams/exam_design_v1_2_0.md/.json and exam_design_check_v1_2_0.py as new files: five questions (Q1-Q4 25 points, Q5 10 points bonus), 30 sub-questions, chapters 1-8, Bloom rule by count and by points, page budget 4 pages else 6, item fields question/sub/tip/terms/asks, sheet units, outputs (paper and key .docx, sheet PDF)."),
 ("TK4_ItemRules2", "ST4_DesignRev2", "Item validator v1_1_0 with the new rules: no memorisation, tips, abbreviations, asks use/reason/effect", "Build", 1.2, ["TK4_Design2_Verify"], "SEN0414-EX-itemrules2", "04-assessment/exams/exam_item_check_v1_1_0.py with fixtures of known answer; rules R19-R23 added; v1_0_0 fixtures still pass."),
 ("TK4_Cover", "ST4_Cover", "Cover page for SEN0414 by a copy of the SEN0401 cover renderer, with a thin entry point", "Build", 0.5, [], "SEN0414-EX-cover", "04-assessment/exams/exam_cover_v1_0_0.py and exam_cover_check_v1_0_0.py as new files; midterm form A and make-up form B built; pages counted with LibreOffice; template read-only outside the repository."),
 ("TK4_Engine5", "ST4_Engine5", "Exam engine v1_1_0: five-question assembler with the Bloom clauses enforced", "Build", 2.5, ["TK4_Design2_Verify", "TK4_ItemRules2_Verify"], "SEN0414-EX-engine5", "04-assessment/exams/exam_engine_v1_1_0.py with shapes, fixtures and check as new files; five question blocks, points 25/25/25/25/10, 8 of 30 at Analyze and above, majority at Apply and above, page budget measured, forms A and B; supersedes TK4_Engine_Bloom."),
 ("TK4_Items_A2", "ST4_Items2", "Item set A (provisional until the Owner's question styles arrive)", "Build", 3.0, ["TK4_ItemRules2_Verify"], "SEN0414-EX-items-a2", "04-assessment/exams/items/items_a_v2_0_0.json with check script; five question formats, chapters 1-8; near-copy rule and item validator v1_1_0 pass; provisional marking in a side file."),
 ("TK4_Items_B2", "ST4_Items2", "Item set B (provisional)", "Build", 3.0, ["TK4_Items_A2_Verify"], "SEN0414-EX-items-b2", "04-assessment/exams/items/items_b_v2_0_0.json; no near copy of set A; with set A meets the blueprint for the midterm and the make-up."),
 ("TK4_Papers", "ST4_Papers", "Paper and key as editable .docx, answer sheet as position-exact PDF", "Build", 2.5, ["TK4_Engine5_Verify", "TK4_Cover_Verify", "TK4_Items_A2_Verify"], "SEN0414-EX-papers", "04-assessment/exams/exam_docx_v1_0_0.py; paper and key .docx, sheet PDF from the SEN0401 sheet module; page counts; forms A and B."),
]
STORIES = {  # id: (title, deliverable, objective, entity, rr, new?)
 "ST4_DesignRev2": ("The design of the papers revised to the Owner's statements of 2026-11-01", "Del4_Papers", "Obj4_PapersBuilt", "DE4_ExamPaper", 8, False),
 "ST4_Cover": ("The cover page of the printed papers", "Del4_Papers", "Obj4_PapersBuilt", "DE4_ExamPaper", 3, True),
 "ST4_Engine5": ("The five-question exam engine", "Del4_Engine", "Obj4_HigherShare", "DE4_ExamPaper", 8, True),
 "ST4_Items2": ("New items for the five-question papers, no recall", "Del4_Items", "Obj4_HigherShare", "DE4_QuestionItem", 5, True),
 "ST4_Papers": ("The two papers and their keys: paper and key .docx, answer sheet PDF", "Del4_Papers", "Obj4_PapersBuilt", "DE4_ExamPaper", 5, False),
}
CANCEL = [("TK4_Engine_Bloom", "TK4_Engine5"), ("TK4_Engine_Bloom_Verify", "TK4_Engine5"), ("TK4_Items_A", "TK4_Items_A2"), ("TK4_Items_A_Verify", "TK4_Items_A2"), ("TK4_Items_B", "TK4_Items_B2"), ("TK4_Items_B_Verify", "TK4_Items_B2"), ("ST4_Items", "ST4_Items2")]
VERIFY = "Control by the lineage agent on its own re-runs of the checks named in the brief, the claims recomputed, no committed file changed, everything committed; an incomplete run is a result, not a pass. Estimated 0.5 hours (an estimate, G120)."
src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); nowZ = now + "Z"; out = []
def blk(name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1); return i, (len(t) if j < 0 else j)
def setblk(name, fn):
    global t
    i, j = blk(name); b = t[i:j]; nb = fn(b); assert nb != b, name; t = t[:i] + nb + t[j:]
# 1 notes + finding
for k in ("Mission4", "Scope4", "Lineage4"):
    out.append("ex:%s backlog:hasAuditNote %s .\n" % (k, lit(WORD))); out.append("ex:%s backlog:hasAuditNote %s .\n" % (k, lit(ROUTE)))
out.append('ex:Finding_ExamStructure_20261101 a backlog:RetrospectiveFinding ;\n    rdfs:label "The Owner\'s exam instruction of 2026-11-01 13:04 replaces the single 30-item list by five questions, a cover page and new item rules"@en ;\n'
           '    backlog:belongsToLineage ex:Lineage4 ; backlog:relatesToWorkItem ex:ST4_Engine ; backlog:relatesToWorkItem ex:ST4_Items ; backlog:relatesToWorkItem ex:ST4_Papers ; backlog:hasFindingScope backlog:Scope_Methodology ;\n'
           '    backlog:hasRootCause %s ;\n    backlog:hasRemedy %s .\n' % (lit(WORD + " " + IMPACT), lit(ROUTE)))
# 2 cancellations (Ready items; withdraw)
for k, by in CANCEL:
    setblk(k, lambda b: b.replace("backlog:hasState backlog:Ready", "backlog:hasState backlog:Cancelled ; backlog:hasRationale %s" % lit("Cancelled %s UTC: superseded by %s after the Owner's exam instruction of 2026-11-01 13:04 (see ex:Finding_ExamStructure_20261101 for the as-is fit-gap and the closure statement)." % (now, by)), 1))
    out.append('ex:Cancel4e_%s a backlog:TransitionEvent ; rdfs:label "%s cancelled as superseded"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_WithdrawReady ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, k, k, nowZ, lit("Cancelled as superseded by %s; never started." % by)))
# 3 tasks
byst = {}
for tid, st, title, typ, h, deps, sess, note in T:
    byst.setdefault(st, []).append(tid)
    for vt in (tid, tid + "_Verify"):
        isv = vt.endswith("_Verify")
        lab = ("Verify: " + title) if isv else title
        d = ([tid] if isv else deps)
        nt = (VERIFY if isv else "Deliverable: %s Executor session %s; brief generated from this register (08-tooling/briefs/exam/r10, sen0414_lineage_brief_exam5_v1_2_0.py). Estimated %.1f hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun)." % (note, sess, h))
        out.append('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:Iter_Ex3 ; backlog:admittedByOutput ex:Out4_Backlog ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
                   '    backlog:hasInvestmentCategory backlog:%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n%s'
                   '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n' % (
                       vt, lit(lab), vt, lit(lab), "Cat_Compliance" if isv else "Cat_NewCapability", "Verify" if isv else "Build", ("    backlog:dependsOn %s ;\n" % ", ".join("ex:" + x for x in d)) if d else "", lit(nt)))
        out.append('ex:Refine4e_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_Ex3 ; backlog:hasWorkKind backlog:WorkKind_Preparation ;\n    backlog:hasRefinementOutcome "Refined by the lineage agent from the Owner\'s instruction of 2026-11-01 13:04 and the coordinator\'s acceptance: deliverable paths, checks, estimate in the task text; the brief is generated from the register." .\n' % (vt, vt, vt, now))
        out.append('ex:RC4e_%s a backlog:ReadinessCheck ; rdfs:label "Readiness check of %s"@en ; backlog:checksReadinessOf ex:%s ; backlog:readinessCheckedAt "%s"^^xsd:dateTime ;\n    backlog:hasReadinessCriterion ex:RK4e_%s_1, ex:RK4e_%s_2, ex:RK4e_%s_3 .\n' % (vt, vt, vt, now, vt, vt, vt))
        for kx, tx in ((1, "The deliverable, its place and its check are written in the item."), (2, "Every dependency of the item is Done or is a task of the same story that precedes it, or is a stated task of another story that must be Done before the start."), (3, "The Owner's statements that bound the item are recorded in the mission and the scope.")):
            out.append('ex:RK4e_%s_%d a backlog:ReadinessCriterion ; rdfs:label %s@en ; backlog:criterionMet true .\n' % (vt, kx, lit(tx)))
        out.append('ex:Mv4e_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Refine ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (vt, lit(vt + " moved to Ready"), vt, nowZ, lit("Refined (ex:Refine4e_%s) and ready after the readiness check ex:RC4e_%s; no executor has started." % (vt, vt))))
# 4 stories
size = {s: sum(h + 0.5 for (tid, st, ti, ty, h, de, se, no) in T if st == s) for s in STORIES}
members = []
for sid, (title, dl, ob, ent, rr, new) in STORIES.items():
    kids = []
    for x in byst[sid]: kids += [x, x + "_Verify"]
    members += [sid] + kids
    v = (20 + 20 + rr) / size[sid]
    scid = "Score4e_" + sid
    if new:
        out.append('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:Iter_Ex3 ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput ex:Out4_Backlog ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
                   '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability %s ; backlog:soThat "the midterm and make-up papers follow the Owner\'s five-question structure, are readable, test use and reasoning and not recall, and print in four pages" ;\n'
                   '    backlog:satisfiesDeliverable ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion ex:AC4_Controlled ;\n    backlog:coversEntity ex:%s ; backlog:coversStage backlog:Stage_Creation ;\n    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n    backlog:decomposesInto %s ;\n    backlog:hasState backlog:Ready ;\n    backlog:hasPriorityScore ex:%s ;\n    backlog:hasAuditNote %s .\n' % (
                       sid, lit(title), sid, lit(title), lit(title), dl, ob, ent, ", ".join("ex:" + k for k in kids), scid, lit(WORD)))
        out.append("ex:EP4_Engine backlog:decomposesInto ex:%s .\nex:%s backlog:metricMovableBy ex:%s .\n" % (sid, ob, sid))
    else:
        def fix(b, sid=sid, kids=kids, scid=scid):
            b = b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready ;\n    backlog:memberOfContainer ex:Iter_Ex3 ;\n    backlog:decomposesInto %s ;\n    backlog:hasPriorityScore ex:%s" % (", ".join("ex:" + k for k in kids), scid), 1)
            b = re.sub(r"\n\s*backlog:notYetScoreable true ; backlog:hasScoreabilityReason \"[^\"]*\"", "", b)
            b = re.sub(r"backlog:notYetScoreable true ; backlog:hasScoreabilityReason \"[^\"]*\" ;", "", b)
            b = b.replace(" ; ;", " ;"); b = re.sub(r" ; \.(\s*)$", r" .\1", b)
            return b
        setblk(sid, fix)
    out.append('ex:%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (scid, v, now, lit("WSJF = (business value 20 + time criticality 20 + risk reduction %d) / job size %.1f h = %.2f. Time criticality 20: the Owner's same-day order for the midterm papers (2026-11-01). Job size is the sum of the story's task estimates, build plus 0.5 h control each. Scored %s UTC at the planning of box 3 of the exam lineage; the items TK4_Engine_Bloom, TK4_Items_A and TK4_Items_B are cancelled as superseded, so this is a re-ranking of the open exam items." % (rr, size[sid], v, now))))
    out.append('ex:Refine4e_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_Ex3 ; backlog:hasWorkKind backlog:WorkKind_Preparation ;\n    backlog:hasRefinementOutcome "Refined from the Owner\'s instruction of 2026-11-01 13:04: criterion AC4_Controlled, estimate, tasks with checks, briefs generated from the register." .\n' % (sid, sid, sid, now))
    out.append('ex:RC4e_%s a backlog:ReadinessCheck ; rdfs:label "Readiness check of %s"@en ; backlog:checksReadinessOf ex:%s ; backlog:readinessCheckedAt "%s"^^xsd:dateTime ;\n    backlog:hasReadinessCriterion ex:RK4e_%s_1, ex:RK4e_%s_2, ex:RK4e_%s_3 .\n' % (sid, sid, sid, now, sid, sid, sid))
    for kx, tx in ((1, "The story has an acceptance criterion and tasks with checks."), (2, "Its tasks are Ready or Done."), (3, "The Owner's statements that bound the story are recorded in the mission and the scope.")):
        out.append('ex:RK4e_%s_%d a backlog:ReadinessCriterion ; rdfs:label %s@en ; backlog:criterionMet true .\n' % (sid, kx, lit(tx)))
    out.append('ex:Mv4e_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Refine ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (sid, lit(sid + " moved to Ready"), sid, nowZ, lit("Refined (ex:Refine4e_%s) and ready after the readiness check ex:RC4e_%s; no executor has started." % (sid, sid))))
# 5 box and planning
out.append('\nex:Iter_Ex3 a backlog:Iteration ; rdfs:label "Box 3 of the exam lineage: the five-question papers (urgent, same day)"@en ; backlog:hasIdentifier "Iter_Ex3" ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-11-01T21:00:00"^^xsd:dateTime ;\n'
           '    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (
               now, lit("Stated by the Owner, not proposed: 'Today we should finish both the Midterms and midterm scope work' (2026-11-01, 12:2x Istanbul); the box ends with the urgent time box, midnight Istanbul (21:00Z). The lineage agent cannot prove that it fits: the critical path of the exam chain is about 10 executor-hours (design 1.0, item rules 1.2, items A 3.0, items B 3.0, papers 2.5 plus controls); what does not finish is said openly and moves only by an Owner rebaseline."),
               lit("A cover page, a five-question design, an item validator with the new rules, an engine that enforces the Bloom clauses, provisional item sets A and B and the paper and key as .docx with the answer sheet PDF are built and controlled, ready for the Owner's review."), ", ".join("ex:" + m for m in members)))
out.append('ex:PC4_Iter_Ex3 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of box 3 of the exam lineage"@en ; backlog:ceremonyFor ex:Iter_Ex3 ; backlog:heldAt "%s"^^xsd:dateTime ; backlog:hasWorkKind backlog:WorkKind_Planning ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment "Held %s UTC by the lineage agent on the Owner\'s instruction: five stories and fourteen tasks committed to this box, ranked by their scores; no executor has started."@en .\n' % (now, ", ".join("ex:Plan4e_" + s for s in STORIES), now))
for sid in STORIES:
    kids = []
    for x in byst[sid]: kids += [x, x + "_Verify"]
    out.append('ex:Plan4e_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into box 3"@en ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:Iter_Ex3 ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec4, ex:Scen4_Sound, ex:Scen4_Refused .\n' % (sid, sid, now, sid, ", ".join("ex:" + k for k in kids)))
# 6 urgent items
for m in members:
    out.append("<%sUrgent_4> backlog:urgentItem <%s%s> .\n" % (NS, NS, m))
order = sorted(STORIES, key=lambda s: -(40 + STORIES[s][4]) / size[s])
out.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % lit("RANKING %s UTC (re-ranking after the Owner's exam instruction; the cancelled items leave the ranking): by score, %s. By dependency: Design2 and Cover first (no dependency), then ItemRules2, then Engine5 and Items_A2, then Items_B2, then Papers. The make-up paper (ST4_MakeUp) stays last." % (now, ", ".join("%s (%.2f)" % (s, (40 + STORIES[s][4]) / size[s]) for s in order))))
res = W.write_new(src, t + "\n" + "".join(out), "The Owner's exam instruction of 2026-11-01 13:04 recorded in the exam lineage: finding with impact and as-is fit-gap, TK4_Engine_Bloom and TK4_Items_A/B (with ST4_Items) cancelled as superseded, five stories with fourteen Ready tasks in box Iter_Ex3, scores (re-ranking), the new items named as urgent items of Urgent_4.")
print(os.path.basename(res))
