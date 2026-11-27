#!/usr/bin/env python3
"""seed_make 1.0.0 (Lineage15, 2026-11-27): writes the seed delta of the urgent lineage Lineage15 (the lineage subject, six urgent stories, their typed tasks)
as Turtle for register_step_v1_1_0.py (EXTRA.ttl). The urgency itself is recorded afterwards by BRSF's own tool backlog_urgency (G158, G195b): this file only names what is urgent.
Usage: seed_make_v1_0_0.py OUT.ttl"""
import sys
Q = lambda s: s.replace('"', '\\"')
AT = "2026-11-27T16:00:00"
STORIES = [
 ("Pages_Ch1_9", "Rebuild the pages of chapters 1 to 9 on template 9.56.0 so that no lambda remains and the Slide source code tab, open exam answers and metadata-free questions are present",
  "Given the pages of chapters 1 to 9 that still carry lambda strings When they are rebuilt from their page builders on template 9.56.0 Then no lambda string remains in any page, the Slide source code tab runs every slide example, the exam result and answers open after finishing and no question or node is about book metadata",
  "the nine page files, their build logs and the page-test logs"),
 ("Exam_Open", "Decide and apply where corrections stay open (exam review, practice drill) and issue the page test 9.43.0 for it",
  "Given the page test 9.42.0 that folds corrections until opened When the owner's rulings on exam answers are applied and a new page test version states the ruling Then the test and the pages agree and the result is kept as a log",
  "page test 9_43_0 and its run logs"),
 ("Page_Ch25", "Give the chapter 25 page the Slide source code tab, open exam answers and a lambda-free A-box",
  "Given the chapter 25 page without a Lab code tab When it is rebuilt on template 9.56.0 with a lambda-free A-box Then the Slide source code tab runs the deck examples, the exam answers open and no lambda remains",
  "the chapter 25 page file and its test log"),
 ("Sources_Clean", "Remove the metadata nodes and questions from the chapter corpora, generators and domain A-boxes that still carry them",
  "Given the corpora, generators and domain A-boxes of chapters 1 to 25 When the metadata nodes and questions are removed at their source Then a rebuild of any page yields no metadata question without a post-build clean-up",
  "new versions of the corpora, generators and A-boxes with a scan log"),
 ("Decks_CodeSlides", "Bring the code slides of the decks of chapters 1 to 10 and 12 to 25 to the chapter 11 standard: a goal line, meaning, reason and idea balloons, a watch-out and a predict prompt, with no slide added",
  "Given the 513 code slides of the other 24 decks When each code slide carries the goal line, the meaning, reason and idea balloons, a watch-out and a predict prompt and the speaker notes address the reader Then the deck checks pass with the same number of slides",
  "the new deck versions and their check logs"),
 ("Rollout_Reverify", "Re-verify under the route the 23 pages built before the urgency was declared (slide source code tab, open exam answers, no metadata)",
  "Given the 23 pages released as the urgent rollout of 2026-11-27 before this route existed When each page is opened, its examples run and its exam answers opened Then the result of every page is kept as a log and every failure is named",
  "the re-verification logs of the 23 pages"),
]
o = ['@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-ch2125corr-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n']
o.append('ex:Lineage15 a backlog:Lineage ;\n    rdfs:label "Urgent lineage: slide source code tab and code-slide standard for all SEN0414 chapters"@en ;\n    backlog:hasProfile backlog:Profile_AAL ;\n    backlog:lineageArchived false ;\n    backlog:lineageOrdinal 15 ;\n    backlog:hasLineageStatus backlog:LS_Opened ;\n    backlog:hasAuditNote "Seed of 2026-11-27: opened by the urgency declaration (G195 b) on the owner\'s rulings of 2026-11-27 for all chapters (a Slide source code tab on every page, open exam answers, no metadata questions, the chapter 11 code-slide standard). Work was built before this route was set (23 pages and the chapter 11 deck and page, commit e7ce395): it is named in story Rollout_Reverify and recorded as a bypass, not backfilled."@en .\n')
for sid, lab, gh, art in STORIES:
    s = f"ex:ST15_{sid}"; tk = [f"ex:TK15_{sid}_1", f"ex:TK15_{sid}_2"]
    o.append(f'''{s} a backlog:Story ; rdfs:label "{Q(lab)}"@en ; backlog:hasIdentifier "ST15_{sid}" ; backlog:belongsToLineage ex:Lineage15 ;
    backlog:hasState backlog:Proposed ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:hasInvestmentCategory backlog:Cat_Maintenance ;
    backlog:appliesDefinitionOfDone ex:DoD14 ; backlog:hasApplicableConcern backlog:Concern_Interaction ; backlog:hasAcceptanceCriterion ex:AC15_{sid} ;
    backlog:decomposesInto {", ".join(tk)} ; backlog:standsAlone true ; backlog:notYetScoreable true ;
    backlog:hasScoreabilityReason "Scored at planning, when the urgent lineage's packages and sprints are cut." .
ex:AC15_{sid} a backlog:AcceptanceCriterion ; rdfs:label "{Q(lab)}: acceptance"@en ; backlog:belongsToLineage ex:Lineage15 ;
    backlog:hasGherkinText "{Q(gh)}" ; backlog:satisfiedByArtifact "{Q(art)}" .
''')
    for k, (tt, lbl) in enumerate([("Build", "Build"), ("Verify", "Verify on the executor's own re-run from the files")], 1):
        o.append(f'''ex:TK15_{sid}_{k} a backlog:ExecutionTask ; rdfs:label "{lbl}: {Q(lab)}"@en ; backlog:hasIdentifier "TK15_{sid}_{k}" ; backlog:belongsToLineage ex:Lineage15 ;
    backlog:hasState backlog:Proposed ; backlog:appliesDefinitionOfDone ex:DoD14 ; backlog:hasTaskType backlog:Task_{"Implementation" if tt=="Build" else "Verification"} ;
    backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:hasInvestmentCategory backlog:Cat_Maintenance .
''')
    o.append(f"ex:TK15_{sid}_2 backlog:dependsOn ex:TK15_{sid}_1 .\n")
open(sys.argv[1], "w").write("".join(o))
