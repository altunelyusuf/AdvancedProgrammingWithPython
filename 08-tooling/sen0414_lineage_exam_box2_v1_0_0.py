#!/usr/bin/env python3
"""sen0414_lineage_exam_box2 v1_0_0 - the exam lineage (Lineage4), box 2: the MIDTERM first. A NEW file; it writes ONE new register file (newest + 1 minor).
Event 'plan' (after the urgent interruption of the exam lineage is resumed): records the Owner's decisions of 2026-10-30 as statements of the mission, admits the story ST4_DesignRev (the design revised to those decisions)
and the story ST4_MakeUp (the make-up paper, ranked last), promotes the Proposed stories ST4_Distinct, ST4_Items and ST4_Engine to Ready with tasks and scores, opens box 2 (Iter_Ex2) with its planning ceremony,
refinements, readiness checks and control activity, and records the new ranking: the midterm first, the make-up paper after the midterm path has had its dry run.
Nothing is begun here: work begun is recorded at the real start of each executor session, by its own later version.
Usage: sen0414_lineage_exam_box2_v1_0_0.py plan"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
lit = W.lit
IT = "Iter_Ex2"; OUTB = "ex:Out4_Backlog"
E = "04-assessment/exams/"
OWNER = ("OWNER DECISIONS 2026-10-30 (relayed by the course coordinator, recorded as relayed): the exam is a physical printed paper and a sitting is 60 minutes; code on paper is read-and-choose plus fill-the-blank, no free writing; "
         "the interactive pages' questions are visible to the students before the sitting, so they are seeds only and are never copied (similarity method for SEN0414: the share of the new item's 4-word sequences found in the seed; a copy at 0.50 or more with the same answer, or at 0.80 or more whatever the answer); "
         "the chapters are 1 to 8 without chapter 5 (debugging is not examinable); the answer sheet is a separate bubble grid that reuses the SEN0401 sheet and reader (sen0401 repository, 08-tooling/exam); the midterm comes first and the make-up paper can wait. "
         "STILL OPEN, asked of the Owner one at a time by the coordinator: the number of items per paper (assumed 30), the Bloom reading (assumed Apply and up), the weight of each chapter (assumed 4,5,5,5,4,4,3 items).")
COMMON = ("Deliverables are NEW files under " + E + " (a committed file is never edited; every new version is a new file from its first save); nothing under 03-materials, no deck, page or research file is changed (exclusion Excl4_ChapterWork); no personal data of students; no term the course does not use. "
          "The Owner's decisions of 2026-10-30 (relayed): physical printed paper; one sitting is 60 minutes; code on paper is read-and-choose plus fill-the-blank and nothing is written freely; the interactive pages' questions are visible to the students, so they are seeds and are never copied; "
          "chapters 1, 2, 3, 4, 6, 7, 8 (chapter 5 is out); the answer sheet is a separate bubble grid that reuses the SEN0401 sheet and reader (read-only, in /home/claude/sen0401/08-tooling/exam/: sen0401_exam_answersheet_v1_0_0.py is the sheet with its layout and renderer, sen0401_exam_answersheet_v1_1_0.py is the reader; never edit them). "
          "Assumptions the Owner has not yet answered, to be marked as assumptions and kept easy to change: 30 items per paper, the Bloom reading Apply and up, items per chapter 4,5,5,5,4,4,3. The midterm is made first; nothing is built for the make-up paper in this box. "
          "The controller re-runs the checks; an incomplete run is a result, not a pass. Report the verbatim output of every check.")

TASKS = {
 "TK4_Distinct_Build": ("Build the near-copy rule for exam items: the 4-word-sequence method, its SHACL shape and its fixtures of known answer", "Build", "Cat_Compliance", [], 3.0, "ST4_Distinct",
  "Build the near-copy rule of the Owner's ruling of 2026-10-30. Method (design section 2.1 of " + E + "exam_design_v1_0_0.md states it; this task builds it): normalise (lower case; words are runs of letters, digits and underscore); the text of an item is its stem, its code listing and its options joined; "
  "C(new, seed) is the share of the new item's 4-word sequences that also occur in the seed; an item is a near copy of a seed when C is at least 0.50 and the correct answers are equal as normalised text, or when C is at least 0.80 whatever the answer. "
  "The seeds ('page-visible set', what a student can open before the sitting) are every item of the newest question_bank_v*.json and of quiz_v1_0_0.json in 08-tooling/chNN-page for chapters 01 to 08 (all eight, chapter 5 too, because students can open it) and every listing of the newest chapter-code manifest 03-materials/chNN/page/chapter_code_chNN_v*.json; "
  "a listing that equals a seed listing after whitespace is a copy unless a change of case alters what it prints (decide by running both). The rule also applies between two papers (the make-up repeats no item of the midterm). "
  "Deliver, as NEW files: (1) " + E + "exam_nocopy_v1_0_0.py, a library and a command line: given an items file (a JSON list of item records with id, stem, code, options, answer as in section 2 of the design) it prints per item the largest C, the seed it matches, whether the answers are equal, and the verdict, and exits 0 only when no item is a near copy; "
  "(2) " + E + "exam_nocopy_shapes_v1_0_0.ttl, the ruling as SHACL (a shape over the RDF description of a measured item that refuses a near copy); a ruling is never kept as prose; "
  "(3) " + E + "exam_nocopy_fixtures_v1_0_0.json and " + E + "exam_nocopy_fixtures_check_v1_0_0.py: fixtures of known answer, namely the five variants of design section 2.1 (identical, one word changed, stem rewritten and options kept, stem rewritten and two options swapped, a new angle) with the values the design states (1.000, 0.942, 0.871, 0.786, 0.000) "
  "and their verdicts, plus a pair with C between 0.50 and 0.80 and different answers (not a copy), a pair with C of 0.80 or more and different answers (a copy), a listing copy that differs by whitespace only (a copy), a listing that differs by case and prints differently (not a copy), and a between-papers pair; "
  "the check prints expected and actual for every fixture, runs the SHACL on a conforming and a violating graph, and exits 0 only when every one is as expected. If a value you measure differs from the design's table, say so plainly in the report and do not edit the design. "
  "Do not depend on the SEN0401 similarity files (another method on other items); you may read them for ideas."),
 "TK4_Distinct_Verify": ("Verify the near-copy rule on the controller's own re-runs", "Verify", "Cat_Compliance", ["TK4_Distinct_Build"], 0.5, "ST4_Distinct",
  "Control by the lineage agent on its own re-runs: the fixtures check exits 0 and prints the five values of the design, the SHACL conforms on the conforming graph and refuses the violating one, the command line refuses a planted copy of a page item and accepts a planted new item, no chapter file changed, everything committed; an incomplete run is a result, not a pass."),
 "TK4_DesignRev": ("Revise the design of the paper to the Owner's decisions of 2026-10-30 and build the item validator", "Build", "Cat_NewCapability", [], 3.0, "ST4_DesignRev",
  "The design " + E + "exam_design_v1_0_0.md/.json was controlled and stays as committed. Revise it as NEW files " + E + "exam_design_v1_1_0.md and exam_design_v1_1_0.json (the same top-level keys as v1_0_0 plus owner_decisions and supersedes, each decision with a reason) so that it follows the Owner's decisions. "
  "(1) Code on paper is read-and-choose plus fill-the-blank: keep predict-the-output by choosing one of four printed outputs, find-the-faulty-line by choosing a line number, complete the blank from a numbered bank, order the lines; nothing is written freely. "
  "Decide the short-answer items (v1_0_0 assumed two hand-marked ones): the recommended default is none, because nothing is written freely and every answer is then read by the machine; if you keep any, say why. "
  "(2) The answer sheet is a separate bubble grid that REUSES the SEN0401 sheet and reader. Read them, run them on a sample specification in a scratch folder outside the repository, and replace sections 7 and 9 of v1_0_0 (own geometry, digit rows, thresholds) by the sheet's own: state the sheet's unit kinds (choice, match, order, bank, human as the sheet module defines them), map every kept SEN0414 item type onto one of them, "
  "say which answers the reader reads and which it holds for a person, and state how the SEN0414 repository obtains the modules (recommended: a byte-identical vendored copy in 08-tooling with its SHA-256 recorded, compared with the source at control; say what a changed source would mean). Where v1_0_0 needed a unit kind the sheet does not have (digit rows), change the item type so that it does not need it, with the reason. "
  "(3) Re-do the blueprint arithmetic (items per type, answer time at most 90 per cent of 60 minutes, Bloom at Apply and up above 50 per cent, letters evenly spread, page budget) for the revised types and show the sums. "
  "(4) Add the item validator as NEW files: " + E + "exam_item_check_v1_0_0.py (library and command line: checks a JSON list of item records against the item model of section 2: required fields, unique ids, chapters among 1,2,3,4,6,7,8, every source exists, Bloom 1 to 6, course_point links that resolve to an entry of " + E + "critical_points_ch01_04_v1_0_0.json or critical_points_ch06_08_v1_0_0.json, answer inside the options, no overlapping options, no 'all of the above' or 'none of the above', listing at most 12 lines and no wrapped line within the declared width, only the kept types) "
  "and " + E + "exam_item_check_fixtures_v1_0_0.json with fixtures of known answer (a valid item of each kept type, and one defective item for each rule, each with its expected verdict); the validator prints expected and actual for each fixture in its self-test and exits 0 only when all are as expected. "
  "(5) Put the Owner's still-open questions (items per paper, Bloom reading, chapter weights) in the design with your recommended default and what each answer would change. "
  "(6) Write " + E + "exam_design_check_v1_1_0.py (a NEW file over the v1_0_0 check, which stays unchanged) with the same assertions on the new design plus: every item type maps onto a sheet unit kind that exists in the SEN0401 sheet module (read from the module), no item type needs free writing."),
 "TK4_DesignRev_Verify": ("Verify the revised design and the item validator on the controller's own re-runs", "Verify", "Cat_Compliance", ["TK4_DesignRev"], 0.5, "ST4_DesignRev",
  "Control by the lineage agent on its own re-runs: the design check v1_1_0 exits 0, the item validator self-test exits 0 and refuses each planted defect, the claims about the SEN0401 sheet and reader are re-checked by building a sample sheet from a specification, the blueprint sums are recomputed, no committed file changed; an incomplete run is a result, not a pass."),
 "TK4_Items_A": ("Author the midterm item pool for chapters 1 to 4 from the critical points, with seeds, enhancements and the near-copy measure", "Build", "Cat_NewCapability", ["TK4_Distinct_Verify", "TK4_DesignRev_Verify"], 4.0, "ST4_Items",
  "Author the midterm item pool for chapters 1, 2, 3 and 4 as " + E + "exam_items_pool_ch01_04_v1_0_0.json (a JSON list of item records as in section 2 of " + E + "exam_design_v1_1_0.json) and " + E + "exam_items_pool_ch01_04_report_v1_0_0.md. Pool sizes: chapter 1: 6 items, chapter 2: 8, chapter 3: 8, chapter 4: 8 (the engine picks 4,5,5,5 of them, so the pool is larger than the paper), "
  "of which at least 3 name two or more chapters within 1 to 4 and at least 4 are indirect (a consequence, an exception or a reason, with indirect_form). Each item tests an entry of " + E + "critical_points_ch01_04_v1_0_0.json (course_point link '<file>#<position from 0>'), cites sources that exist (deck slide, speaker note, corpus passage or story), carries its Bloom level and, where it grew from a page item, its seed_item link '<bank path>#<position from 0>' (otherwise 'none'). "
  "At least 60 per cent of the items are at Bloom 3 or above. Use only the kept types and the code tasks of the revised design (predict by choosing one of four printed outputs, find the faulty line, complete a blank from a numbered bank, order). Page-interactive questions are seeds only: an item grows from a seed by a new angle, a cross-chapter link, a reasoning step or a changed code case, and the report states which for every item. "
  "Run the item validator (exam_item_check_v1_0_0.py) and the near-copy tool (exam_nocopy_v1_0_0.py) on the file and print both outputs in the report; both must exit 0, and an item either one refuses is rewritten, not excused."),
 "TK4_Items_A_Verify": ("Verify the item pool of chapters 1 to 4 on the controller's own re-runs", "Verify", "Cat_Compliance", ["TK4_Items_A"], 0.5, "ST4_Items",
  "Control by the lineage agent on its own re-runs: the item validator and the near-copy tool exit 0 on the pool, the pool sizes and the cross-chapter, indirect and Bloom counts are recomputed, every cited source and course point exists, a sample of items is read for correctness of the keyed answer by running the code of the code items; an incomplete run is a result, not a pass."),
 "TK4_Items_B": ("Author the midterm item pool for chapters 6 to 8 and the cross-group synthesis items", "Build", "Cat_NewCapability", ["TK4_Distinct_Verify", "TK4_DesignRev_Verify"], 4.5, "ST4_Items",
  "Author the midterm item pool for chapters 6, 7 and 8 and the synthesis items between the two groups of chapters as " + E + "exam_items_pool_ch06_08_v1_0_0.json and " + E + "exam_items_pool_ch06_08_report_v1_0_0.md (records as in section 2 of " + E + "exam_design_v1_1_0.json). Pool sizes: chapter 6: 6 items, chapter 7: 6, chapter 8: 5, "
  "and at least 8 synthesis items that need one chapter from 1 to 4 and one from 6 to 8 (they list both chapters; their course points come from both " + E + "critical_points_ch01_04_v1_0_0.json and " + E + "critical_points_ch06_08_v1_0_0.json), of which at least 4 are indirect (a consequence, an exception or a reason, with indirect_form). "
  "Everything else of the chapters 1 to 4 pool task applies: each item tests a critical point (course_point link), cites existing sources, carries its Bloom level and its seed_item link or 'none', at least 60 per cent are at Bloom 3 or above, only the kept types and code tasks of the revised design, page questions are seeds only, the report states the enhancement made for every item, "
  "and the item validator and the near-copy tool are run on the file and both exit 0."),
 "TK4_Items_B_Verify": ("Verify the item pool of chapters 6 to 8 and the synthesis items on the controller's own re-runs", "Verify", "Cat_Compliance", ["TK4_Items_B"], 0.5, "ST4_Items",
  "Control by the lineage agent on its own re-runs: the item validator and the near-copy tool exit 0 on the pool, the pool sizes and the synthesis, indirect and Bloom counts are recomputed, every cited source and course point exists, a sample of items is read for correctness of the keyed answer by running the code of the code items; an incomplete run is a result, not a pass."),
 "TK4_Engine_Core": ("Build the exam assembler for the midterm: blueprint rules as SHACL, letters, banks, forms A and B, sheet specification, with fixtures of known answer", "Build", "Cat_NewCapability", ["TK4_DesignRev_Verify", "TK4_Distinct_Verify"], 5.0, "ST4_Engine",
  "Build the assembler of the general exam engine as NEW files: " + E + "exam_engine_v1_0_0.py (library and command line), " + E + "exam_engine_shapes_v1_0_0.ttl (the blueprint rules as SHACL; a ruling is never kept as prose), " + E + "exam_engine_fixtures_v1_0_0.json and " + E + "exam_engine_check_v1_0_0.py. "
  "Input: a pool of item records (the format of " + E + "exam_design_v1_1_0.json) and the design's blueprint (30 items, items per chapter 4,5,5,5,4,4,3, types per the revised design: assumptions, read from the design file and not hard-coded). Output for a seed: a paper of the blueprint's size in two forms A and B (same item at every position's type; options and the order inside blocks of equal type differ), "
  "a build record (the seed, the pool file and its SHA-256, the design version, the rule results), the printed answer key data (letter or bank number, points, reason) and the sheet specification in the format of the SEN0401 sheet module's specification (units of the kinds choice, match, order, bank; read the module, do not copy it into the repository in this task). "
  "Rules the engine enforces and the SHACL states (each with a fixture that must be refused): items per chapter equal the quota; type counts equal the blueprint; answer time at most 90 per cent of 60 minutes; share at Bloom 3 or above above 50 per cent; counts of the correct letters differ by at most one and no letter is the key of four items in a row, in each form after shuffling; "
  "at least 9 cross-chapter items and 6 indirect items (numbers read from the design); fill-in banks have more entries than gaps, are a seeded permutation (the seed stored), are not in gap order, gaps of one item have different keys and no bank number is the key of three gaps in a row; item ids unique; every item passes the item validator and the near-copy tool; the make-up paper repeats no item of the midterm. "
  "The fixtures include a synthetic pool that must give a paper (the check prints the rule results of that paper) and, for every rule, a pool that must be refused with the rule named. All fixture data is synthetic and marked so; use no real pool of this course in the fixtures. The check exits 0 only when every fixture is as expected. "
  "Do not render a printed paper in this task (the next box does)."),
 "TK4_Engine_Core_Verify": ("Verify the exam assembler on the controller's own re-runs", "Verify", "Cat_Compliance", ["TK4_Engine_Core"], 0.5, "ST4_Engine",
  "Control by the lineage agent on its own re-runs: the engine check exits 0, each planted rule violation is refused with its rule named, the SHACL conforms on the accepted paper's description and refuses the violating one, the sheet specification is accepted by the SEN0401 sheet module when a sample sheet is built from it in a scratch folder, no committed file changed; an incomplete run is a result, not a pass."),
}
STORIES = {  # id: (title, wants, tasks, epic, deliverable, objective, risk reduction, size, existing)
 "ST4_Distinct": (None, None, ["TK4_Distinct_Build", "TK4_Distinct_Verify"], "EP4_Content", "Del4_Items", "Obj4_NothingOut", 13, 3.5, True),
 "ST4_DesignRev": ("The paper design revised to the Owner's decisions of 2026-10-30", "the design of the paper revised to the Owner's decisions (read-and-choose code, the SEN0401 answer sheet and reader reused) and a validator of the item model", ["TK4_DesignRev", "TK4_DesignRev_Verify"], "EP4_Engine", "Del4_Design", "Obj4_SheetsGraded", 8, 3.5, False),
 "ST4_Items": (None, None, ["TK4_Items_A", "TK4_Items_A_Verify", "TK4_Items_B", "TK4_Items_B_Verify"], "EP4_Content", "Del4_Items", "Obj4_HigherShare", 5, 9.5, True),
 "ST4_Engine": (None, None, ["TK4_Engine_Core", "TK4_Engine_Core_Verify"], "EP4_Engine", "Del4_Engine", "Obj4_HigherShare", 5, 5.5, True),
}
NOTES_RANK = ("RANKING 2026-10-30 (the lineage agent, after the controls of box 1 and the end of the urgent interruption): the MIDTERM is made first. Order of the open exam items by their scores and dependencies: 1 the near-copy rule (the Owner ranked it first among the later stories), 2 the revised design (it fixes the sheet and the code types the engine and the items depend on), "
              "3 the item pools of chapters 1 to 4 and 6 to 8 and the assembler (after 1 and 2), then the printed paper, key and sheet of the midterm, the reading and grading tool, and the dry run of the midterm path (Proposed, planned in the next box); the make-up paper comes last, after the dry run of the midterm path. "
              "Nothing is built for the make-up paper in box 2. The Owner has the limited token budget in mind: executors are started only when their dependencies are Done.")


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def task_block(tid):
    label, typ, cat, deps, est, story, note = TASKS[tid]
    return ('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:%s ; backlog:admittedByOutput %s ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
            '    backlog:hasInvestmentCategory backlog:%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n%s'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n') % (
        tid, lit(label), tid, lit(label), IT, OUTB, cat, typ, ("    backlog:dependsOn %s ;\n" % ", ".join("ex:" + d for d in deps)) if deps else "",
        lit(note + (" " + COMMON if typ == "Build" else "") + " Estimated %.1f hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun)." % est))


def plan(t):
    assert "ex:%s a backlog:Iteration" % IT not in t, "box 2 already planned"
    n = W.now(); L = []; members = []; plans = []
    # the Owner's decisions as a statement of the mission, and the ranking as a note of the lineage
    L.append("ex:Mission4 backlog:hasAuditNote %s .\n" % lit(OWNER))
    L.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % lit(NOTES_RANK + " Recorded %s UTC." % n))
    # new stories
    t_new = {}
    for sid, (title, wants, tks, ep, dl, ob, rr, size, existing) in STORIES.items():
        if existing:
            i, j = blk(t, sid); b = t[i:j]
            pat = re.compile(r'backlog:hasState backlog:Proposed ;\s*backlog:notYetScoreable true ; backlog:hasScoreabilityReason "[^"]*" \.')
            assert pat.search(b), sid
            nb = pat.sub(lambda m: 'backlog:memberOfContainer ex:%s ; backlog:decomposesInto %s ;\n    backlog:hasState backlog:Ready ;\n    backlog:hasPriorityScore ex:Score4b_%s .' % (IT, ", ".join("ex:" + k for k in tks), sid), b, count=1)
            t = t[:i] + nb + t[j:]
        else:
            L.append('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ;\n    backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:%s ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput %s ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
                     '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability %s ; backlog:soThat "the printed exam is built on the Owner\'s decisions of 2026-10-30: read-and-choose code, a reused answer sheet and reader, no copy of a page question" ;\n'
                     '    backlog:satisfiesDeliverable ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion ex:AC4_Controlled ;\n    backlog:coversEntity ex:DE4_ExamPaper ; backlog:coversStage backlog:Stage_Creation ;\n    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n'
                     '    backlog:decomposesInto %s ;\n    backlog:hasState backlog:Ready ;\n    backlog:hasPriorityScore ex:Score4b_%s .\n' % (sid, lit(title), sid, lit(title), IT, OUTB, lit(wants), dl, ob, ", ".join("ex:" + k for k in tks), sid))
            L.append("ex:%s backlog:decomposesInto ex:%s .\nex:%s backlog:metricMovableBy ex:%s .\n" % (ep, sid, ob, sid))
        members += [sid] + tks; plans.append((sid, tks))
        for tk in tks: L.append(task_block(tk))
        val = (20 + 20 + rr) / size
        L.append('ex:Score4b_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value 20 + time criticality 20 + risk reduction %d) / job size %.1f h = %.2f. Time criticality 20: the midterm sitting is the week of 2026-11-02, so the midterm path is worked first and the make-up paper after it. Risk reduction %d: %s. Job size is the sum of the story's task estimates. Scored %s UTC at the planning of box 2 of the exam lineage." % (
                rr, size, val, rr, {"ST4_Distinct": "the Owner ranked this rule first among the later stories and every item depends on it, since a copied page question gives the students who practised an unearned advantage",
                                    "ST4_DesignRev": "the engine, the items and the sheet all depend on the code types and on the reused answer sheet being fixed",
                                    "ST4_Items": "the pool is the content of the paper, and it is the largest unknown", "ST4_Engine": "the assembler makes the blueprint rules checkable before any paper is printed"}[sid], n))))
    # the make-up paper: admitted, ranked last, not in the box
    L.append('\nex:ST4_MakeUp a backlog:Story ; rdfs:label "The make-up paper, built after the midterm path has had its dry run"@en ; backlog:hasIdentifier "ST4_MakeUp" ;\n    backlog:hasTitle "The make-up paper, built after the midterm path has had its dry run" ;\n'
             '    backlog:belongsToLineage ex:Lineage4 ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput %s ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
             '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "the make-up paper with its printed key and answer sheet, repeating no item of the midterm, built with the same engine, items check and sheet" ; backlog:soThat "a student who misses the midterm sits an equivalent paper" ;\n'
             '    backlog:satisfiesDeliverable ex:Del4_Papers ; backlog:pursuesObjective ex:Obj4_PapersBuilt ; backlog:hasAcceptanceCriterion ex:AC4_Controlled ;\n    backlog:coversEntity ex:DE4_ExamPaper ; backlog:coversStage backlog:Stage_Creation ;\n    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n'
             '    backlog:hasState backlog:Proposed ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked last by the Owner (the make-up paper can wait); scored and decomposed into tasks after the dry run of the midterm path." .\n' % OUTB)
    L.append("ex:EP4_Engine backlog:decomposesInto ex:ST4_MakeUp .\nex:Obj4_PapersBuilt backlog:metricMovableBy ex:ST4_MakeUp .\n")
    for sid in ("ST4_Papers", "ST4_Grader", "ST4_DryRun", "ST4_Items"):
        L.append("ex:%s backlog:hasAuditNote %s .\n" % (sid, lit("From %s UTC this story serves the MIDTERM first (Owner, 2026-10-30); the make-up paper is the story ST4_MakeUp, ranked last. %s" % (n, "Its tasks are made at the planning of the box after box 2." if sid != "ST4_Items" else "Box 2 plans the item pools of the midterm."))))
    mem = ", ".join("ex:" + m for m in members)
    L.append('\nex:%s a backlog:Iteration ; rdfs:label "Box 2 of the exam lineage: the near-copy rule, the revised design, the midterm item pools and the assembler"@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-11-01T09:00:00"^^xsd:dateTime ;\n'
             '    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal "The rule that refuses copies of page questions, the design revised to the Owner\'s decisions with the item validator, the midterm item pools of all seven chapters and the assembler that checks the blueprint are built and controlled, so that the printed midterm, its key and sheet, the grading tool and the dry run can be planned next." ;\n    backlog:hasMember %s .\n' % (
        IT, IT, n, lit("Proposed by the lineage agent on %s: the start is the instant of the planning ceremony; the box ends before the midterm week begins (2026-11-02); the next box is planned after the controls of this one. Estimates: near-copy rule 3.0 h, design revision 3.0 h, item pools 4.0 h and 4.5 h, assembler 5.0 h, controls 0.5 h each; at most three executors at once, the later ones only when their dependencies are Done." % n), mem))
    L.append('\nex:PC4_%s a backlog:SprintPlanningCeremony ; rdfs:label "Planning of box 2 of the exam lineage"@en ; backlog:ceremonyFor ex:%s ; backlog:heldAt "%s"^^xsd:dateTime ; backlog:hasWorkKind backlog:WorkKind_Planning ;\n    backlog:includesPlanningEvent %s ;\n'
             '    rdfs:comment %s@en .\n' % (IT, IT, n, ", ".join("ex:Plan4b_" + s for s, _ in plans), lit("Held %s UTC by the lineage agent: four stories and their ten tasks are committed to this box; the stories of the printed paper, the grading tool and the dry run wait as Proposed, and the make-up paper is ranked last. No executor has started." % n)))
    for sid, tks in plans:
        L.append('ex:Plan4b_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into box 2"@en ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec4, ex:Scen4_Sound, ex:Scen4_Refused .\n' % (sid, sid, n, IT, sid, ", ".join("ex:" + k for k in tks)))
    for m in members:
        L.append('ex:Refine4b_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:%s ; backlog:hasWorkKind backlog:WorkKind_Preparation ;\n    backlog:hasRefinementOutcome %s .\n' % (m, m, m, n, IT, lit("Refined by the lineage agent from the mission, the scope and the Owner's decisions of 2026-10-30: deliverable path, criterion, estimate, a brief to be generated from the register; startable when its dependencies are Done.")))
        L.append('ex:RC4b_%s a backlog:ReadinessCheck ; rdfs:label "Readiness check of %s"@en ; backlog:checksReadinessOf ex:%s ; backlog:readinessCheckedAt "%s"^^xsd:dateTime ;\n    backlog:hasReadinessCriterion ex:RK4b_%s_1, ex:RK4b_%s_2, ex:RK4b_%s_3 .\n' % (m, m, m, n, m, m, m))
        for k, txt in ((1, "The deliverable, its place and its check are written in the item."), (2, "Every dependency of the item is Done or is a task of the same story that precedes it."), (3, "The Owner's statements that bound the item are recorded in the mission and the scope.")):
            L.append('ex:RK4b_%s_%d a backlog:ReadinessCriterion ; rdfs:label %s@en ; backlog:criterionMet true .\n' % (m, k, lit(txt)))
        L.append('ex:Mv4b_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Refine ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (
            m, lit("%s moved to Ready" % m), m, n, lit("Recorded at the planning of box 2 of the exam lineage: refined (ex:Refine4b_%s) and ready after the readiness check ex:RC4b_%s; no executor has started." % (m, m))))
    L.append('\nex:ACT4_Control2 a backlog:ControlActivity ; rdfs:label "Controller re-runs of the box-2 deliverables"@en ; backlog:plannedInBox ex:%s ; backlog:hasWorkKind backlog:WorkKind_Control ;\n    rdfs:comment "Planned %s UTC: after each executor reports, the lineage agent re-runs the checks named in the Verify task of the item and records the run; the box review waits for the runs." .\n' % (IT, n))
    return t + "\n" + "".join(L), "Exam lineage, box 2 planned for the MIDTERM: the Owner's decisions of 2026-10-30 recorded, the story of the revised design and the story of the make-up paper (ranked last) admitted, the near-copy rule, the item pools and the assembler promoted to Ready with ten tasks, scores and the ranking; no executor has started."


def main():
    assert sys.argv[1:2] == ["plan"], __doc__
    src = W.newest(); t = open(src, encoding="utf-8").read()
    nt, comment = plan(t)
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
