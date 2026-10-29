#!/usr/bin/env python3
"""Exam lineage 4, event 'ruling': records the Owner's ruling of 2026-10-30 on the interactive pages' questions (a lineage audit note), adds the story ST4_Distinct (Proposed, ranked ahead of ST4_Items) and re-ranks.
Builds on sen0414_lineage_exam_v1_1_0.py (unchanged)."""
import sys, os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("ex11", os.path.join(here, "sen0414_lineage_exam_v1_1_0.py")); X = importlib.util.module_from_spec(sp); sp.loader.exec_module(X)
W = X.W
RULING = ("OWNER RULING 2026-10-30 00:51 Istanbul (relayed by the course coordinator, as recorded, not a verbatim quotation of the Owner's own words beyond the quoted part): 'Interactive page questions are accessible by the students before the exam. "
          "They are chapter subject specific questions, rarely cross-section. It is not wise to use them directly, but they can be a seed for better questions and enhancement iterations.' CONSEQUENCES RECORDED: no exam item is a page item or a near copy of one; "
          "page items are seeds for new, better items built by enhancement iterations, each linked to its seed and to the course points it tests; cross-chapter, synthesis and reasoning items are authored. "
          "This is enforced by a rule in SHACL with a stated similarity method and a fixture of known answer (story ST4_Distinct), ranked ahead of the story of new items (ST4_Items), and the design task (TK4_Design) states the similarity method in its design. "
          "It narrows the deliverable 'Items that meet the conventions' and does not change the mission wording.")
ST = ("ex:ST4_Distinct a backlog:Story ; rdfs:label \"Rule: no exam item is a page item or a near copy\"@en ; backlog:hasIdentifier \"ST4_Distinct\" ;\n"
      "    backlog:hasTitle \"Rule: no exam item is a page item or a near copy\" ;\n"
      "    backlog:belongsToLineage ex:Lineage4 ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput ex:Out4_Backlog ;\n"
      "    backlog:hasInvestmentCategory backlog:Cat_Compliance ;\n"
      "    backlog:asRole \"SEN0414 instructor\" ; backlog:wantsCapability \"a rule, written as SHACL with a stated similarity method and a fixture of known answer, that refuses an exam item which is a page item or a near copy of one, and a link from every exam item to its seed page item and to the course points it tests\" ; backlog:soThat \"students who practised on the interactive pages gain nothing from memory of the page items, and the exam tests the critical points\" ;\n"
      "    backlog:satisfiesDeliverable ex:Del4_Items ; backlog:pursuesObjective ex:Obj4_NothingOut ; backlog:hasAcceptanceCriterion ex:AC4_Controlled ;\n"
      "    backlog:coversEntity ex:DE4_QuestionItem ; backlog:coversStage backlog:Stage_Creation ;\n"
      "    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n"
      "    backlog:hasState backlog:Proposed ;\n"
      "    backlog:notYetScoreable true ; backlog:hasScoreabilityReason \"Ranked first among the later stories by the Owner's ruling of 2026-10-30; scored and decomposed into tasks when its box is planned, after the design (which states the similarity method) is controlled.\" .\n"
      "ex:EP4_Content backlog:decomposesInto ex:ST4_Distinct .\n"
      "ex:Obj4_NothingOut backlog:metricMovableBy ex:ST4_Distinct .\n")
def main():
    src = W.newest(); t = open(src, encoding="utf-8").read(); assert "ST4_Distinct a" not in t
    t += "\nex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit(RULING) + "\n" + ST
    t += "ex:ST4_Items backlog:hasAuditNote %s .\n" % W.lit("RE-RANKED 2026-10-30 by the Owner's ruling on page items: this story now follows ST4_Distinct; its items are authored as new items seeded by page items, never copies of them.")
    print(os.path.basename(W.write_new(src, t, "Owner ruling of 2026-10-30 on page items recorded; story ST4_Distinct added ahead of ST4_Items.")))
main()
