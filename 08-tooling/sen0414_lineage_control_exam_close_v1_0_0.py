#!/usr/bin/env python3
"""sen0414_lineage_control_exam_close v1_0_0 - completes the exam lineage's box-1 control record that register 2.333.0 (the previous lineage agent's uncommitted work) left with 12 validator violations:
the three Done stories (ST4_Points_A, ST4_Points_B, ST4_Design) state no execution modality (L2), have no test harness derived from their evidence (L3) and their objectives carry no observation dated
after they finished (L3); the epic EP4_Design has all children Done and is still Proposed (G148). Writes ONE new register file (newest + 1 minor) that adds exactly these records; nothing is removed.
The observations are read from the controller's verified facts: seven chapters have critical points (chapters 1 to 4 and 6 to 8: the two bridge-verified points tasks), and no grading tool exists yet (the design only).
Usage: sen0414_lineage_control_exam_close_v1_0_0.py"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W

CASES = {"ST4_Points_A": ("points_a", "Obj4_PointsListed", "Met4_Points", "7", "Chapters with critical points collected and a stated list of what could not be found, read after the controller's own re-runs of both points tasks (chapters 1 to 4 and 6 to 8): 7."),
         "ST4_Points_B": ("points_b", "Obj4_PointsListed", "Met4_Points", "7", None),
         "ST4_Design": ("design", "Obj4_SheetsGraded", "Met4_Sheets", "0", "Per cent of synthetic sheets graded as the key does, read after the controller re-ran the design check: 0, because only the design exists and no grading tool has been built.")}


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def main():
    src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); add = []
    for sid, (c, obj, met, val, meth) in CASES.items():
        i, j = blk(t, sid); b = t[i:j]; assert "backlog:hasState backlog:Done" in b, sid
        assert "hasExecutionModality" not in b and ("pursuesObjective ex:" + obj) in b, sid
        t = t[:i] + b.replace("backlog:hasState backlog:Done", "backlog:hasState backlog:Done ; backlog:hasExecutionModality backlog:Mode_Hybrid", 1) + t[j:]
        ev = re.search(r"backlog:hasEvidence ([^;]*);", b).group(1).strip()
        add.append('ex:Harness4_%s a backlog:TestHarness ; rdfs:label "Checks run for %s"@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (sid, sid, sid, ev))
        if meth:
            add.append('ex:Obs41_%s a backlog:MetricObservation ; rdfs:label "Reading after the controller re-ran the checks (%s)"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%s"^^xsd:decimal ; backlog:observedAt "%s"^^xsd:dateTime ;\n    backlog:hasObservationMethod %s .\n' % (obj, sid, met, obj, val, now, W.lit(meth)))
    i, j = blk(t, "EP4_Design"); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b
    st = re.search(r'ex:ST4_Design a backlog:Story.*?startedAt ("[^"]*"\^\^xsd:dateTime)', t, re.S).group(1)
    evd = re.search(r"ex:ST4_Design a backlog:Story.*?backlog:hasEvidence ([^;]*);", t, re.S).group(1).strip()
    t = t[:i] + b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:Done ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:hasAcceptanceCriterion ex:AC4_Controlled ; backlog:hasEvidence %s ; backlog:startedAt %s ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime' % (evd, st, "2026-10-29T22:46:19", "2026-10-29T22:46:19"), 1) + t[j:]
    ep = "EP4_Design"
    add.append('ex:Harness4_%s a backlog:TestHarness ; rdfs:label "Checks run for %s"@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (ep, ep, ep, evd))
    add.append('ex:Refine4_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "2026-10-29T21:22:44"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_Ex1 ; backlog:hasWorkKind backlog:WorkKind_Preparation ;\n    backlog:hasRefinementOutcome "Recorded with the completion of the epic (2.334.0, written after the fact and said so): the epic groups one story, refined on 2026-10-29T21:22:44 with its story ex:Refine4_ST4_Design; the epic adds no work of its own." .\n' % (ep, ep, ep))
    add.append('ex:RC4_%s a backlog:ReadinessCheck ; rdfs:label "Readiness check of %s"@en ; backlog:checksReadinessOf ex:%s ; backlog:readinessCheckedAt "2026-10-29T21:22:44"^^xsd:dateTime ;\n    backlog:hasReadinessCriterion ex:RK4_%s_1, ex:RK4_%s_2, ex:RK4_%s_3 .\n' % (ep, ep, ep, ep, ep, ep))
    for k, lab in ((1, "The deliverable, its place and its check are written in the item."), (2, "Every dependency of the item is Done or is a task of the same story that precedes it."), (3, "The Owner's statements that bound the item are recorded in the mission and the scope.")):
        add.append('ex:RK4_%s_%d a backlog:ReadinessCriterion ; rdfs:label "%s"@en ; backlog:criterionMet true .\n' % (ep, k, lab))
    add.append('ex:Mv4_%s_0 a backlog:TransitionEvent ; rdfs:label "%s moved from Proposed to Ready"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Refine ; backlog:transitionedAt "2026-10-29T21:22:44"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "Recorded with the completion of the epic: refined (2026-10-29T21:22:44) with its story and ready after the readiness check ex:RC4_%s; the move is written after the fact and says so." .\n' % (ep, ep, ep, ep))
    add.append('ex:Begin4T_%s a backlog:TransitionEvent ; rdfs:label "%s started with its first story"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt %s ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "The epic starts with the real start of its story ST4_Design (and its task TK4_Design) at 2026-10-29T22:04:32 UTC." .\n' % (ep, ep, ep, st))
    add.append('ex:Complete4T_EP4_Design a backlog:TransitionEvent ; rdfs:label "EP4_Design completed: its only story is Done"@en ; backlog:transitionedItem ex:EP4_Design ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "2026-10-29T22:46:19"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "The epic derives Done from its child ST4_Design, which is Done on the controller\'s evidence." .\n')
    add.append('ex:TC4_EP4_Design a backlog:TestCase ; rdfs:label "Re-run the structure and source checks of the design of the paper and require no failure"@en ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:exercisesCriterion ex:AC4_Controlled ; backlog:coversScenario ex:Scen4_Sound ; backlog:runsOnData ex:Data4_DesignFiles ;\n    backlog:hasCaseText "The controller re-runs the design check (sen0414_control_exam_v1_0_0.py design): the files exist and parse, every decision has a reason, the blueprint arithmetic adds up, nothing under 03-materials changed, everything is committed; the check prints no failure and exits 0 (the controller\'s run is the log control_design_run1.log)." .\n')
    add.append('ex:Data4_DesignFiles a backlog:TestData ; rdfs:label "The committed design files of the paper as the executor left them"@en ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:hasFixtureState "The files 04-assessment/exams/exam_design_v1_0_0.md and exam_design_v1_0_0.json as committed by the task TK4_Design, for which the controller\'s design check exits zero." .\n')
    add.append('ex:AC4_Controlled backlog:coveredByCase ex:TC4_EP4_Design .\n')
    for w in ("ST4_Design", "EP4_Design"):
        add.append('ex:Finding_Design_NoMetricMove_%s a backlog:RetrospectiveFinding ;\n    rdfs:label "The design alone does not move the grading metric"@en ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:relatesToWorkItem ex:%s ; backlog:hasFindingScope backlog:Scope_Methodology ;\n    backlog:hasRootCause "The design of the paper is a written design: the objective it is attached to measures the share of synthetic answer sheets the grading tool grades like the key, and no grading tool exists yet, so the value read after the controller\'s re-runs equals the baseline (0). The reading is correct; the attachment of the design to this objective is a modelling choice of the Backlog stage, not a failed attempt." ;\n    backlog:hasRemedy "No change to the design. The metric is moved by the grader and the dry-run stories of the next box (ST4_Grader, ST4_DryRun); the reading after each of them is the observation that counts. The attachment is left as modelled and named here so that a reader does not take the unchanged value for an ineffective repair." .\n' % (w, w))
    out = W.write_new(src, t + "\n" + "".join(x for x in add if x), "Completes the control record of 2.333.0 (the previous lineage agent's uncommitted work): execution modality and derived test harness on the three Done stories of box 1, observations of the two objectives they pursue read after the controller's re-runs, and the epic EP4_Design Done because its only story is Done; nothing removed.")
    print(os.path.basename(out))


if __name__ == "__main__":
    main()
