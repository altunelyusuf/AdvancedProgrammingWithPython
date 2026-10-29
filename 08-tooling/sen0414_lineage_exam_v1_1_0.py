#!/usr/bin/env python3
"""sen0414_lineage_exam v1_1_0 (a NEW file over v1_0_0, which stays as committed and opened lineage 4) - the stage events of the exam lineage ex:Lineage4:
scope PREV | goal PREV | objective PREV | backlog PREV | fill STAGE HASH     (PREV = the commit that closed the previous stage; one stage per call, one register version per call; the caller validates, commits and pushes each alone).
Nothing is begun here: work begun is recorded at the real start of each executor session, by its own later version."""
__version__ = "1.1.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
import sen0414_lineage_exam_v1_0_0 as X
lit = W.lit
DT = '"%s"^^xsd:dateTime'

# ------------------------------------------------------------------ helpers
def fill_prev(t, stage, commit):
    pat = re.compile(r'(ex:Out4_%s a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"' % stage, re.S)
    assert pat.search(t), "no PENDING on Out4_" + stage
    return pat.sub(lambda m: m.group(1) + '"%s"' % commit, t, count=1)

CL = {  # the clauses of the accepted mission wording, each a verbatim substring of it
    "paper": "two printed paper exams, the midterm and a make-up exam, each a sitting of 60 minutes over the chapters the instructor fixes before the sitting",
    "key": "each with its answer key",
    "engine": "built with the interactive pages' exam engine, extended to a general engine for cross-chapter, synthesis and indirect questions",
    "types": "with question types and styles that suit a physical printed paper",
    "quality": "Their items need the course's own knowledge, put the majority at the higher levels of Bloom's taxonomy, spread the correct letters evenly, randomise fill-in option banks and invent no terms",
    "points": "They revive the critical points the instructor explained in the course, from the slides, speaker notes, corpus and stories",
    "methods": "Methods reduce the printed pages and the mistakes made in giving answers",
    "grading": "a reliable method reads, assesses and grades each student's paper",
}
for v in CL.values():
    assert v in X.STATEMENT, v

# ------------------------------------------------------------------ SCOPE
SCOPE_TEXT = ("IN: the two printed exams of SEN0414, the midterm and a make-up exam, one sitting of 60 minutes each, over the chapters the Owner fixes (his statement of 2026-10-29: the final list is due 2026-10-30; chapter 5, Debugging, is out). "
              "(1) The critical points the instructor explained in the course, collected from the decks, speaker notes, corpus and stories of the chapters, with a plain list of what could not be found, for the Owner to answer. "
              "(2) The design of the paper: the item model and the question types that suit print, the blueprint across chapters and Bloom levels, the layout that saves pages, the answer sheet and the rules that reduce mistakes in giving answers, and the method to read, assess and grade a paper. "
              "(3) A general exam engine that assembles both papers, their printed answer keys and their answer sheets from the chapter question banks and new items, across chapters. "
              "(4) New items (cross-chapter, synthesis, indirect, fill-in with randomised option banks) that need the course's own knowledge and put the majority at the higher Bloom levels. "
              "(5) A tool that reads, assesses and grades a handed-in answer sheet, tested on synthetic sheets only. "
              "OUT: any change to the decks, pages or research sets of the chapters (the chapter lineage's work); interactive HTML delivery of the exams; QTI and CATS export; any personal data of students; items on chapter 5 or any chapter the Owner leaves out; the sitting itself and the grading of real students' papers, which are the instructor's own acts.")
AREA = "Area4_Exam"
DELIV = [
    ("Del4_Points", "points", "The critical points of the course, collected, with the list of what could not be found", "The critical points the instructor explained in the course are collected from the decks, speaker notes, corpus and stories of the exam chapters, each with its source (file and place) and its chapter, and a separate plain list states every point that could not be found or confirmed, so that the Owner can be asked."),
    ("Del4_Design", "types", "The design of the paper: item types for print, blueprint, layout, answer sheet and error-reducing rules", "A written design fixes the item model, the question types and styles that suit a printed paper, the blueprint of each paper across chapters and Bloom levels, the page-saving layout for a 60-minute sitting, the answer sheet, and the rules that reduce mistakes in giving answers."),
    ("Del4_Engine", "engine", "A general exam engine that works across chapters", "A tool built on the interactive pages' item machinery assembles an exam from the chapter banks and new items across chapters, balances chapters, Bloom levels and correct letters, randomises fill-in option banks, and refuses an item that breaks a convention."),
    ("Del4_Items", "quality", "New items that meet the conventions", "New cross-chapter, synthesis, indirect and fill-in items exist for the exam chapters; each needs the course's own knowledge, names its source, its Bloom level and its critical point, and invents no term; together with the banks they put the majority of each paper at the higher Bloom levels and spread the correct letters evenly."),
    ("Del4_Papers", "paper", "The two printed papers", "The midterm and the make-up paper exist as printable documents over the chapters the Owner fixed, each fits a 60-minute sitting, and the two cover the same chapters with different items."),
    ("Del4_Keys", "key", "The printed answer key of each paper", "Each paper has its own printed answer key with the correct answers, the points and the reason for each answer."),
    ("Del4_Methods", "methods", "Fewer printed pages and fewer answering mistakes", "The papers use the page-saving and error-reducing methods of the design, and the number of printed pages per student and the rules applied are stated for each paper."),
    ("Del4_Grading", "grading", "A reliable way to read, assess and grade each student's paper", "A method and a tool read a handed-in answer sheet, mark every answer it can read with certainty, flag every answer it cannot, grade against the printed key, and are tested on synthetic filled sheets only."),
]
EXCL = [
    ("Excl4_ChapterWork", "Any change to the decks, interactive pages or research sets of the chapters: that work belongs to the chapter lineage (ex:Lineage2) and its own project.", "The chapters are taught and examined from what the chapter lineage controls; changing them here would change the subject of the exam and compete with the other lineage for the same files."),
    ("Excl4_Digital", "Interactive-HTML delivery of the exams and the QTI and CATS export.", "The Owner ruled on 2026-10-28 14:31 'Physical printed paper exams'; the earlier default of QTI and CATS export was dropped on 2026-10-29."),
    ("Excl4_Ch5AndOthers", "Items on chapter 5 (Debugging) and on any chapter the Owner leaves out of the final list.", "The Owner stated on 2026-10-29 that chapter 5 is not in the scope of the exams and that he fixes the final chapter list on 2026-10-30."),
    ("Excl4_StudentData", "Any personal data of students, in items, sheets, tests or logs.", "The standing convention for the course materials: synthetic stand-ins only."),
]

def ev_scope(t, prev):
    t = fill_prev(t, "Mission", prev); t = X.set_status4(t, "LS_Scoped")
    L = ['\nex:%s a backlog:ScopeArea ;\n    rdfs:label "The two printed exams of SEN0414"@en ;\n    backlog:belongsToLineage ex:Lineage4 ;\n'
         '    backlog:areaLocation "04-assessment/exams (the exam work of this lineage, new) and 08-tooling (the engine and grader tools, new files); the chapters themselves are read, not changed" ;\n'
         '    backlog:areaMeasure "2 papers, 2 printed answer keys, 1 engine, 1 grading method, the critical points of the exam chapters" ;\n    backlog:hasScopeLayer backlog:Layer_Work .\n' % AREA]
    for i, k, label, text in DELIV:
        L.append('\nex:%s a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:derivesFromMissionClause %s^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n'
                 '    backlog:deliverableForArea ex:%s ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n' % (i, lit(label), lit(CL[k]), lit(text), AREA))
    for i, what, why in EXCL:
        L.append('\nex:%s a backlog:ScopeExclusion ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:excludesConcern %s ;\n    backlog:hasExclusionRationale %s ;\n    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .\n' % (i, lit(what.split(":")[0].split(" (")[0][:90]), lit(what), lit(why)))
    L.append('\nex:Scope4 a backlog:ScopeStatement ;\n    rdfs:label "The two printed SEN0414 exams, their keys and their grading, over the chapters the Owner fixes"@en ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:scopeForMission ex:Mission4 ;\n'
             '    backlog:hasIntentOrigin backlog:IOrigin_OwnerStated ; backlog:scopeCompletionState backlog:Proposed ;\n    backlog:hasScopeStatementText %s ;\n    backlog:coversArea ex:%s ;\n    backlog:hasScopeExclusion %s ;\n'
             '    backlog:producedByStage ex:Out4_Scope ;\n    backlog:requiresDeliverable %s .\n' % (lit(SCOPE_TEXT), AREA, ", ".join("ex:" + e[0] for e in EXCL), ", ".join("ex:" + d[0] for d in DELIV)))
    ents = [("DE4_ExamPaper", "Exam paper - the printed paper of one sitting"), ("DE4_QuestionItem", "Question item - one question with its answer and source"), ("DE4_AnswerKey", "Answer key - the printed correct answers of one paper"), ("DE4_AnswerSheet", "Answer sheet - the sheet a student fills in")]
    L.append('\nex:Blueprint4 a backlog:Blueprint ;\n    rdfs:label "What the exam work is about"@en ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:blueprintFor ex:Scope4 ;\n    backlog:hasDomainEntity %s .\n' % ", ".join("ex:" + e for e, _ in ents))
    for e, lab in ents:
        L.append('ex:%s a backlog:DomainEntity ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 .\n' % (e, lit(lab)))
    reasons = {"ActiveUse": "The sitting and the live grading of real students' papers are the instructor's own acts and are outside this lineage; the lineage delivers the paper, the key and the grading method.",
               "SuspensionException": "A withdrawn item or a re-sit is handled by building the make-up paper; no separate handling is planned.",
               "Termination": "Archiving of used papers is not planned in this lineage."}
    for e, lab in ents:
        for st, human in (("ActiveUse", "active use"), ("SuspensionException", "suspension or exception"), ("Termination", "termination")):
            L.append('ex:Gap4_%s_%s a backlog:BlueprintGap ; rdfs:label "No coverage planned for %s at the %s stage"@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:gapForEntity ex:%s ; backlog:gapForStage backlog:Stage_%s ; backlog:hasGapReason %s .\n' % (e[4:], st, lab.split(" - ")[0].lower(), human, e, st, lit(reasons[st])))
    t += "".join(L)
    return t + X.output(t, "Scope").replace("ex:Out4_Scope a", "ex:Out4_Scope a", 1), "Exam lineage, Scope stage closed: the two printed exams, the engine, the critical points, the design, the items, the keys, the methods and the grading as deliverables; interactive delivery, QTI/CATS, student data and chapters 5 and others out; Owner statements on the chapter list recorded in the mission."

# ------------------------------------------------------------------ GOAL
GOALS = [
    ("G4_PapersExist", "The two printed exams and their printed keys exist", "Facing_Mission", "", "GoalOrigin_New", "Derived from the mission and the scope: the outcome is two printed papers with their printed keys.", ["Del4_Papers", "Del4_Keys"]),
    ("G4_ItemsSound", "Every item needs the course's own knowledge and the papers meet the exam conventions", "Facing_Scope", "", "GoalOrigin_New", "Derived from the scope deliverables on the critical points, the engine and the items: the mission names the conventions (course knowledge, higher Bloom levels, even letters, randomised banks, no invented terms).", ["Del4_Points", "Del4_Engine", "Del4_Items"]),
    ("G4_GradingReliable", "A handed-in paper can be read, assessed and graded reliably", "Facing_Scope", "", "GoalOrigin_New", "Derived from the scope deliverables on the design, the methods and the grading.", ["Del4_Design", "Del4_Methods", "Del4_Grading"]),
    ("G4_ReadyForSittings", "Each paper is complete before its sitting", "Facing_Containment", "", "GoalOrigin_New", "Derived from the Owner's time facts: the midterm is next week (the week of 2026-11-02), the make-up exam follows; a paper that is not ready on time is not delivered.", ["Del4_Papers"]),
    ("G4_NothingOutOfBounds", "No chapter work, digital delivery or student data enters the exam work", "Facing_Exclusion", "\n    backlog:guardsExclusion ex:Excl4_ChapterWork, ex:Excl4_Digital, ex:Excl4_Ch5AndOthers, ex:Excl4_StudentData ;", "GoalOrigin_New", "Derived from the exclusions of the scope: the work stays inside its boundary.", []),
]

def ev_goal(t, prev):
    t = fill_prev(t, "Scope", prev); t = X.set_status4(t, "LS_Goaled")
    L = []
    for i, label, f, g, origin, why, dels in GOALS:
        L.append('\nex:%s a backlog:Goal ;\n    rdfs:label %s@en ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:derivesFromScope ex:Scope4 ; backlog:goalCoversArea ex:%s ;%s\n'
                 '    backlog:contributesToMission ex:Mission4 ; backlog:hasGoalFacing backlog:%s ; backlog:hasGoalOrigin backlog:%s ;\n'
                 '    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;\n    backlog:hasGoalRationale %s ;\n    backlog:producedByStage ex:Out4_Goal .\n' % (i, lit(label), AREA, g, f, origin, lit(why)))
    L.append('''
ex:Spec4 a backlog:Specification ;
    rdfs:label "What a sound exam paper is"@en ; backlog:belongsToLineage ex:Lineage4 ; backlog:specifiesGoal ex:G4_ItemsSound ;
    backlog:hasSpecificationText "A paper is sound when every item names its chapter, its source (slide, speaker note, corpus passage or story) and its Bloom level; its answer is determined by the course's content and not by a term the course does not use; more than half of its items are at the Apply level or above; the correct letters of its multiple-choice items are spread evenly over the letters; the option banks of its fill-in items are in random order; and a reader who only has the printed key can mark every answer." ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out4_Goal .
ex:Scen4_Sound a backlog:TestScenario ; rdfs:label "A paper that meets every convention is accepted"@en ; backlog:belongsToLineage ex:Lineage4 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec4 ;
    backlog:hasScenarioText "Given an assembled paper whose items name chapter, source and Bloom level, when the engine's convention check runs, then it reports more than half of the items at Apply or above, the correct letters within one item of an even spread, and no item without a source." .
ex:Scen4_Refused a backlog:TestScenario ; rdfs:label "An item that breaks a convention is refused"@en ; backlog:belongsToLineage ex:Lineage4 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec4 ;
    backlog:hasScenarioText "Given an item with no source, or whose answer rests on a term the course does not use, when the engine's convention check runs, then the item is refused and named." .
ex:Model4_UseCase a backlog:ModelArtifact ; rdfs:label "Who uses the exam work"@en ; backlog:belongsToLineage ex:Lineage4 ;
    backlog:hasModelKind backlog:Kind_UseCaseDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The instructor fixes the chapter list, answers the questions about the critical points that could not be found, prints the paper, its key and the answer sheets, runs the sitting and grades the handed-in sheets with the tool; the executors build the points, the design, the engine, the items and the grading tool; the lineage agent controls each result on its own re-runs." ;
    backlog:describesItem ex:G4_PapersExist .
''')
    t += "".join(L)
    return t + X.output(t, "Goal"), "Exam lineage, Goal stage closed: five goals derived from the scope (papers exist, items sound, grading reliable, ready for the sittings, nothing out of bounds)."

# ------------------------------------------------------------------ OBJECTIVE
OBJS = [
    ("Obj4_PapersBuilt", "G4_PapersExist", "Met4_Papers", "printed exam papers with their printed answer key", 0, 2, "Dir_Increase", "Counted from the files in 04-assessment/exams after the controller has re-run the paper checks.", "no paper exists yet"),
    ("Obj4_HigherShare", "G4_ItemsSound", "Met4_Higher", "per cent of the items of the weakest paper that are at the Apply level or above", 42, 51, "Dir_Increase", "Computed by the engine's convention check over each assembled paper; the baseline is the share in the chapter banks of chapters 1 to 8 (403 of 967 items at Apply or Analyze, none at Evaluate or Create).", "the banks read 42 per cent and no paper is assembled yet"),
    ("Obj4_PointsListed", "G4_ItemsSound", "Met4_Points", "exam chapters whose critical points are collected with a stated list of what could not be found", 0, 7, "Dir_Increase", "Counted from the critical-points files after the controller has re-run the check of their structure and sources; the Owner's chapter list may change the target.", "no critical-points file exists yet"),
    ("Obj4_SheetsGraded", "G4_GradingReliable", "Met4_Sheets", "per cent of synthetic filled answer sheets that the grading tool grades exactly as the hand-made key does, with every unreadable mark flagged", 0, 100, "Dir_Increase", "Computed from a controller run of the tool over a set of synthetic sheets made with known marks, including smudged and double marks.", "no grading tool exists yet"),
    ("Obj4_OnTime", "G4_ReadyForSittings", "Met4_Ready", "papers complete before their sitting", 0, 2, "Dir_Increase", "Counted at the sitting dates the Owner gives; the midterm is the week of 2026-11-02.", "no paper is complete yet"),
    ("Obj4_NothingOut", "G4_NothingOutOfBounds", "Met4_Out", "files of the chapters (decks, pages, research sets) changed by the exam lineage", 0, 0, "Dir_Hold", "Computed from git: files under 03-materials changed by commits of this lineage's tasks.", "no task has run yet"),
]

def ev_objective(t, prev):
    t = fill_prev(t, "Goal", prev); t = X.set_status4(t, "LS_Objectived"); n = W.now(); L = []
    for i, g, m, what, b, tg, d, q, base in OBJS:
        L.append('''
ex:%s a backlog:Objective ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 ;
    backlog:contributesToGoal ex:%s ; backlog:fillsScope ex:Scope4 ; backlog:hasSuccessMetric ex:%s ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "%d"^^xsd:decimal ; backlog:hasTargetValue "%d"^^xsd:decimal ; backlog:hasTargetDirection backlog:%s ;
    backlog:hasCheckpoint ex:CP4_%s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out4_Objective .
ex:%s a backlog:Metric ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage4 .
ex:CP4_%s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the controller has re-run the checks"@en ;
    backlog:checkpointCondition "Taken after the controller's own re-runs, so the value is read from verified facts and not from an executor's report." ;
    backlog:expectedValue "%d"^^xsd:decimal .
ex:Obs40_%s a backlog:MetricObservation ; rdfs:label "Baseline, before any work"@en ;
    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
''' % (i, lit("%s: from %d to %d" % (what[0].upper() + what[1:], b, tg)), g, m, lit(q), b, tg, d, i, m, lit(what), i, tg, i, m, i, b, n, lit("Baseline at the Objective stage of the exam lineage: " + base + ".")))
    t += "".join(L)
    return t + X.output(t, "Objective"), "Exam lineage, Objective stage closed: six objectives with metrics, baselines and targets (papers built, higher-level share, critical points listed, sheets graded, ready on time, no chapter file changed)."

# ------------------------------------------------------------------ BACKLOG
IT = "Iter_Ex1"; OUTB = "ex:Out4_Backlog"
TASKS = {
    "TK4_Points_A": ("Collect the critical points of chapters 1 to 4 from the decks, speaker notes, corpus and stories, and list what could not be found", "Build", "Cat_NewCapability", [], 3.0, "ST4_Points_A"),
    "TK4_Points_A_Verify": ("Verify the critical points of chapters 1 to 4 on the controller's own re-runs", "Verify", "Cat_Compliance", ["TK4_Points_A"], 0.5, "ST4_Points_A"),
    "TK4_Points_B": ("Collect the critical points of chapters 6 to 8 from the decks, speaker notes, corpus and stories, and list what could not be found", "Build", "Cat_NewCapability", [], 3.0, "ST4_Points_B"),
    "TK4_Points_B_Verify": ("Verify the critical points of chapters 6 to 8 on the controller's own re-runs", "Verify", "Cat_Compliance", ["TK4_Points_B"], 0.5, "ST4_Points_B"),
    "TK4_Design": ("Write the design of the paper: item model, question types for print, blueprint, page-saving layout, answer sheet, error-reducing rules and the grading method", "Build", "Cat_NewCapability", [], 4.0, "ST4_Design"),
    "TK4_Design_Verify": ("Verify the design of the paper on the controller's own re-runs", "Verify", "Cat_Compliance", ["TK4_Design"], 0.5, "ST4_Design"),
}
STORIES = {
    "ST4_Points_A": ("Critical points of chapters 1 to 4", "the critical points the instructor explained in chapters 1 to 4, collected with their sources, and a plain list of what could not be found", ["TK4_Points_A", "TK4_Points_A_Verify"], "EP4_Content", "Del4_Points", "Obj4_PointsListed", 3, 3.5),
    "ST4_Points_B": ("Critical points of chapters 6 to 8", "the critical points the instructor explained in chapters 6 to 8, collected with their sources, and a plain list of what could not be found", ["TK4_Points_B", "TK4_Points_B_Verify"], "EP4_Content", "Del4_Points", "Obj4_PointsListed", 3, 3.5),
    "ST4_Design": ("Design of the paper", "a written design of the item model, the question types for print, the blueprint, the page-saving layout, the answer sheet, the error-reducing rules and the grading method", ["TK4_Design", "TK4_Design_Verify"], "EP4_Design", "Del4_Design", "Obj4_SheetsGraded", 3, 4.5),
}
COVERS = {"ST4_Engine": ["DE4_ExamPaper"], "ST4_Items": ["DE4_QuestionItem"], "ST4_Papers": ["DE4_ExamPaper", "DE4_AnswerKey"], "ST4_Grader": ["DE4_AnswerSheet"], "ST4_DryRun": ["DE4_AnswerSheet"]}
LATER = [  # box 2 and later: carried as Proposed stories; their tasks are made when the box is planned, after the chapter list is fixed
    ("ST4_Engine", "The general exam engine", "a general exam engine that assembles both papers, keys and answer sheets across chapters", "EP4_Engine", "Del4_Engine", "Obj4_HigherShare"),
    ("ST4_Items", "New items across chapters", "new cross-chapter, synthesis, indirect and fill-in items that meet the conventions", "EP4_Content", "Del4_Items", "Obj4_HigherShare"),
    ("ST4_Papers", "The two papers and their printed keys", "the midterm and the make-up paper with their printed answer keys, within a 60-minute sitting", "EP4_Engine", "Del4_Papers", "Obj4_PapersBuilt"),
    ("ST4_Grader", "The grading tool", "a tool that reads, assesses and grades a handed-in answer sheet and flags what it cannot read", "EP4_Grading", "Del4_Grading", "Obj4_SheetsGraded"),
    ("ST4_DryRun", "Dry run of the whole exam path", "a dry run: both papers printed, synthetic sheets filled, read, graded and checked against the keys", "EP4_Grading", "Del4_Methods", "Obj4_SheetsGraded"),
]
NOTE_COMMON = ("Deliverable under 04-assessment/exams/ (new files only, named with a version); nothing under 03-materials, no deck, page or research file is changed (exclusion Excl4_ChapterWork); no personal data of students; no term the course does not use; the Owner's statements: chapter 5 is out, the final chapter list is fixed on 2026-10-30, two exams (midterm and make-up), 60 minutes each, physical printed paper, a printed answer key per exam. "
               "Every new version of any file, including your own tools, is a new file from its first save. The controller re-runs the checks; an incomplete run is a result, not a pass.")
NOTES = {
    "TK4_Points_A": "Read the decks (03-materials/chNN/SEN0414_ChNN_*.pptx, newest version), their speaker notes, the chapter corpus (08-tooling/sen0414_chNN_corpus_v*.py, newest) and the stories (08-tooling/sen0414_chNN_stories_v*.py, newest) of chapters 1, 2, 3 and 4. Collect the critical points the instructor explained: a point is critical when the deck stresses it (title, repeated, warning, 'remember', error teaching), the speaker notes explain it at length, or the corpus or a story ties it to a common mistake. Write 04-assessment/exams/critical_points_ch01_04_v1_0_0.json (a list of objects with exactly these keys: chapter (integer), point (one plain sentence), why_critical (one plain sentence), source_file (a path in the repository that exists), place (for a .pptx the slide number as an integer, and for a speaker note the same slide number; for a corpus or stories file the quoted fragment, at most 120 characters, that appears in the file), evidence_kind (one of slide, speaker_note, corpus, story)) and 04-assessment/exams/critical_points_ch01_04_not_found_v1_0_0.md: a plain list, per chapter, of what you looked for and could not find or could not confirm as the instructor's own emphasis, written as questions the Owner can answer in one line each. Do not invent a point; every point cites a place that exists. ",
    "TK4_Points_B": "Read the decks (03-materials/chNN/SEN0414_ChNN_*.pptx, newest version), their speaker notes, the chapter corpus (08-tooling/sen0414_chNN_corpus_v*.py, newest) and the stories (08-tooling/sen0414_chNN_stories_v*.py, newest) of chapters 6, 7 and 8 (chapter 5 is out of the exams). Collect the critical points the instructor explained: a point is critical when the deck stresses it (title, repeated, warning, 'remember', error teaching), the speaker notes explain it at length, or the corpus or a story ties it to a common mistake. Write 04-assessment/exams/critical_points_ch06_08_v1_0_0.json (a list of objects with exactly these keys: chapter (integer), point (one plain sentence), why_critical (one plain sentence), source_file (a path in the repository that exists), place (for a .pptx the slide number as an integer, and for a speaker note the same slide number; for a corpus or stories file the quoted fragment, at most 120 characters, that appears in the file), evidence_kind (one of slide, speaker_note, corpus, story)) and 04-assessment/exams/critical_points_ch06_08_not_found_v1_0_0.md: a plain list, per chapter, of what you looked for and could not find or could not confirm as the instructor's own emphasis, written as questions the Owner can answer in one line each. Do not invent a point; every point cites a place that exists. ",
    "TK4_Design": "Write the design of the two papers as 04-assessment/exams/exam_design_v1_0_0.md (a design document the engine and the grading tool are built from) and the machine-readable parts as 04-assessment/exams/exam_design_v1_0_0.json. The machine-readable part is ONE JSON object with exactly these top-level keys: decisions (a list of objects with keys topic, decision, reason), item_types_kept (a list of objects with keys type, why; every type is one of mcq, multi, judge, match, order, repair, blank, cloze, predict, program, short, write, ask, string, graph, object, sparql), item_types_dropped (same shape), blueprint (an object with keys items (integer), minutes (60), share_apply_or_above (a number between 0 and 100), letters (an object A, B, C, D to counts), chapters (an object chapter number to item count), types (an object type to item count), cross_chapter_items (integer)), page_budget (an object with keys pages_per_student, sheets_per_student, reasoning), answer_sheet (an object with keys layout, mark_style, geometry (an object with markers, cell_mm, resolution_dpi), student_id_line, version_mark), grading (an object with keys read_by_machine, read_by_hand, unreadable_rule, double_mark_rule, key_application, second_check). It decides, with a reason for each decision: (1) the item model (fields: id, chapters, source, Bloom level, critical point, type, stem, options or blanks, answer, points, reason) and the question types and styles that suit a physical printed paper and a 60-minute sitting (restrict the 17 types of the interactive pages' exam engine to those that can be answered on paper and graded reliably: say which are kept and which are dropped, and why); (2) the blueprint of a paper across chapters, Bloom levels and item types, with cross-chapter, synthesis and indirect questions, majority at the Apply level or above, correct letters spread evenly, fill-in option banks randomised; (3) methods to reduce the printed pages (layout, shared stems, compact code, one answer sheet, a page budget for 60 minutes) with the page count you expect; (4) methods to reduce mistakes in giving answers (answer sheet design, one mark style, numbering, check boxes, no ambiguous options, instructions printed once, a student-ID line, version marks that tie sheet to paper); (5) a reliable method to read, assess and grade each student's paper (what is read by machine from a scan or photograph, what by hand, how an unreadable or double mark is flagged, how the key is applied, how a result is checked twice), with the answer-sheet geometry it needs (marker positions, cell sizes, resolution) so a tool can be built from it. Base it on what exists: the exam engine of the interactive pages (08-tooling/template_exam_v9_19_0.js and the page template 9.52.4 exam code), the Exam desk (08-tooling/sen0414_exam_desk_v2_2_0.html), the release tool (08-tooling/sen0414_exam_release_v1_0_0.py), the chapter banks (08-tooling/chNN-page/question_bank_v1_1_0.json) and the assessment ontology (04-assessment/sen0414_assessment_v1_0_0.ttl): say what you reuse and what is new. ",
}
VERIFY_NOTE = "Control by the lineage agent on its own re-runs of the structure and sources check (every point cites an existing file and place; the not-found list exists; no chapter file changed; everything committed); an incomplete run is a result, not a pass."
VERIFY_NOTE_D = "Control by the lineage agent on its own re-runs: the design files exist and parse, every decision has a reason, the kept item types are a subset of the engine's types, the blueprint numbers add up (majority at Apply or above, letters evenly spread, page budget), the grading method states its geometry; no chapter file changed; everything committed; an incomplete run is a result, not a pass."

def task_block(tid):
    label, typ, cat, deps, est, story = TASKS[tid]
    audit = (NOTES.get(tid) or (VERIFY_NOTE_D if tid.startswith("TK4_Design") else VERIFY_NOTE)) + (" " + NOTE_COMMON if tid in NOTES else "")
    return ('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:%s ; backlog:admittedByOutput %s ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
            '    backlog:hasInvestmentCategory backlog:%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Ready ;\n%s'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n') % (
        tid, lit(label), tid, lit(label), IT, OUTB, cat, typ, ("    backlog:dependsOn %s ;\n" % ", ".join("ex:" + d for d in deps)) if deps else "", lit(audit + " Estimated %.1f hours (an estimate, G120: nobody has witnessed a start; the real start is recorded at work begun)." % est))

def ev_backlog(t, prev):
    t = fill_prev(t, "Objective", prev); t = X.set_status4(t, "LS_Backlogged"); n = W.now(); L = []
    start = n
    L.append('\nex:Init4_Exams a backlog:Initiative ; rdfs:label "Examine SEN0414 with two printed exams"@en ; backlog:hasIdentifier "Init4_Exams" ; backlog:hasTitle "The two printed exams" ;\n'
             '    backlog:belongsToLineage ex:Lineage4 ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput %s ; backlog:hasState backlog:Proposed ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasInitiativeKind backlog:InitKind_Development ;\n'
             '    backlog:producesIncrement "two printed papers with printed keys and a grading tool" ;\n    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:appliesDefinitionOfDone ex:DoD ; backlog:coversEntity ex:DE4_ExamPaper ;\n    backlog:pursuesObjective ex:Obj4_PapersBuilt ; backlog:hasApplicableConcern backlog:Concern_Data ;\n'
             '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored at planning, through its stories." ;\n    backlog:decomposesInto ex:EP4_Content, ex:EP4_Design, ex:EP4_Engine, ex:EP4_Grading .\n' % OUTB)
    EPS = {"EP4_Content": ("Exam content", "DE4_QuestionItem", "Obj4_PointsListed"), "EP4_Design": ("Exam design", "DE4_ExamPaper", "Obj4_SheetsGraded"), "EP4_Engine": ("Exam engine and papers", "DE4_ExamPaper", "Obj4_PapersBuilt"), "EP4_Grading": ("Grading the papers", "DE4_AnswerSheet", "Obj4_SheetsGraded")}
    kids = {e: [] for e in EPS}
    for sid, (title, wants, tks, ep, dl, ob, rr, size) in STORIES.items(): kids[ep].append(sid)
    for sid, title, wants, ep, dl, ob in LATER: kids[ep].append(sid)
    for e, (label, ent, ob) in EPS.items():
        L.append('\nex:%s a backlog:Epic ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput %s ; backlog:hasState backlog:Proposed ;\n'
                 '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:appliesDefinitionOfDone ex:DoD ;\n    backlog:coversEntity ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasApplicableConcern backlog:Concern_Data ;\n'
                 '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked through its stories\' scores at planning." ;\n    backlog:decomposesInto %s .\n' % (e, lit(label), e, lit(label), OUTB, ent, ob, ", ".join("ex:" + k for k in kids[e])))
    L.append('\nex:AC4_Controlled a backlog:AcceptanceCriterion ; rdfs:label "An exam deliverable is accepted only on the controller\'s own re-runs"@en ; backlog:belongsToLineage ex:Lineage4 ;\n'
             '    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS4_Control ;\n    backlog:measuredWithVersion "sen0414_control_exam_v1_0_0.py (written by the lineage agent as controller tooling before the first control)" ;\n    backlog:satisfiedByArtifact "the controller\'s logs under 08-tooling/control-exam-logs and the files named by the task" .\n' % lit(
                 "Given the files an executor committed for an exam task, when the controller re-runs the structure and source checks of the task (files exist and parse, every cited source exists, every decision has a reason, no file under 03-materials changed, everything committed), then the checks print no failure and exit 0 - and an incomplete run is a result, not a pass; the executor's own report is not evidence."))
    L.append('ex:TS4_Control a backlog:ToolScript ; rdfs:label "exam control script (the controller\'s structure and source checks of the exam deliverables)"@en ; backlog:scriptFileName "sen0414_control_exam_v1_0_0.py" ; backlog:acceptsGraphPath false .\n')
    members = []; plans = []
    for sid, (title, wants, tks, ep, dl, ob, rr, size) in STORIES.items():
        L.append('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ;\n    backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:memberOfContainer ex:%s ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput %s ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
                 '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability %s ; backlog:soThat "the two printed exams are built from the course\'s own critical points, on a design that fits a 60-minute paper sitting and can be graded reliably" ;\n'
                 '    backlog:satisfiesDeliverable ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion ex:AC4_Controlled ;\n    backlog:coversEntity ex:DE4_ExamPaper ; backlog:coversStage backlog:Stage_Creation ;\n    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n'
                 '    backlog:decomposesInto %s ;\n    backlog:hasState backlog:Ready ;\n    backlog:hasPriorityScore ex:Score4_%s .\n' % (sid, lit(title), sid, lit(title), IT, OUTB, lit(wants), dl, ob, ", ".join("ex:" + k for k in tks), sid))
        members += [sid] + tks; plans.append((sid, tks))
        for tk in tks: L.append(task_block(tk))
        val = (20 + 20 + rr) / size
        L.append('ex:Score4_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
            sid, val, n, lit("WSJF = (business value 20 + time criticality 20 + risk reduction %d) / job size %.1f h = %.2f. Time criticality 20: the midterm sitting is the week of 2026-11-02 and the Owner ordered the exam scope first until 2026-11-01; risk reduction %d: the work removes an unknown that every later exam task depends on (what the instructor stressed, how the paper is built and graded). Job size is the sum of the story's task estimates. Scored on %s UTC at the Backlog stage of the exam lineage." % (rr, size, val, rr, n))))
    for sid, title, wants, ep, dl, ob in LATER:
        L.append('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ;\n    backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage4 ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput %s ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
                 '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability %s ; backlog:soThat "the two printed exams are built from the course\'s own critical points, on a design that fits a 60-minute paper sitting and can be graded reliably" ;\n'
                 '    backlog:satisfiesDeliverable ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion ex:AC4_Controlled ;\n    backlog:coversEntity %s ; backlog:coversStage backlog:Stage_Creation ;\n    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n    backlog:hasState backlog:Proposed ;\n'
                 '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored and decomposed into tasks when its box is planned, after the design is controlled and the Owner has fixed the chapter list (2026-10-30)." .\n' % (sid, lit(title), sid, lit(title), OUTB, lit(wants), dl, ob, ", ".join("ex:" + c for c in COVERS[sid])))
    # box, ceremonies, planning, refinement, readiness, controls
    mem = ", ".join("ex:" + m for m in members)
    L.append('\nex:%s a backlog:Iteration ; rdfs:label "Box 1 of the exam lineage: the critical points and the design of the paper"@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-10-31T09:00:00"^^xsd:dateTime ;\n'
             '    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal "The critical points of the exam chapters are collected with a plain list of what could not be found, and the design of the paper (item model, question types for print, blueprint, layout, answer sheet, error-reducing rules, grading method) is written and controlled, so that the engine, the items and the grading tool of the next box can be built from it." ;\n    backlog:hasMember %s .\n' % (
        IT, IT, start, lit("Proposed by the lineage agent on %s: the start is the instant of the planning ceremony; the box is short on purpose (two days) because the midterm sitting is the week of 2026-11-02 and the Owner fixes the chapter list on 2026-10-30; the next box is planned after the controls of this one. Estimates: points 3.0 h each, design 4.0 h, controls 0.5 h each; at most three executors at once." % n), mem))
    L.append('\nex:PC4_%s a backlog:SprintPlanningCeremony ; rdfs:label "Planning of box 1 of the exam lineage"@en ; backlog:ceremonyFor ex:%s ; backlog:heldAt "%s"^^xsd:dateTime ; backlog:hasWorkKind backlog:WorkKind_Planning ;\n    backlog:includesPlanningEvent %s ;\n'
             '    rdfs:comment %s@en .\n' % (IT, IT, n, ", ".join("ex:Plan4_" + s for s, _ in plans), lit("Held %s UTC by the lineage agent: three stories and their six tasks are committed to this box; the other five stories wait as Proposed until the design is controlled and the chapter list is fixed. No executor has started." % n)))
    for sid, tks in plans:
        L.append('ex:Plan4_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into box 1"@en ; backlog:belongsToLineage ex:Lineage4 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec4, ex:Scen4_Sound, ex:Scen4_Refused .\n' % (sid, sid, n, IT, sid, ", ".join("ex:" + k for k in tks)))
    for m in members:
        L.append('ex:Refine4_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:%s ; backlog:hasWorkKind backlog:WorkKind_Preparation ;\n    backlog:hasRefinementOutcome %s .\n' % (m, m, m, n, IT, lit("Refined by the lineage agent from the mission, the scope and the Owner statements: deliverable path, criterion, estimate, a brief to be generated from the register; startable when its dependencies are Done.")))
        L.append('ex:RC4_%s a backlog:ReadinessCheck ; rdfs:label "Readiness check of %s"@en ; backlog:checksReadinessOf ex:%s ; backlog:readinessCheckedAt "%s"^^xsd:dateTime ;\n    backlog:hasReadinessCriterion ex:RK4_%s_1, ex:RK4_%s_2, ex:RK4_%s_3 .\n' % (m, m, m, n, m, m, m))
        for k, txt in ((1, "The deliverable, its place and its check are written in the item."), (2, "Every dependency of the item is Done or is a task of the same story that precedes it."), (3, "The Owner's statements that bound the item are recorded in the mission and the scope.")):
            L.append('ex:RK4_%s_%d a backlog:ReadinessCriterion ; rdfs:label %s@en ; backlog:criterionMet true .\n' % (m, k, lit(txt)))
    L.append('\nex:ACT4_Control1 a backlog:ControlActivity ; rdfs:label "Controller re-runs of the box-1 deliverables"@en ; backlog:plannedInBox ex:%s ; backlog:hasWorkKind backlog:WorkKind_Control ;\n    rdfs:comment "Planned %s UTC: after each executor reports, the lineage agent re-runs the structure and source checks (sen0414_control_exam_v1_0_0.py) and records the run; the box review waits for the runs." .\n' % (IT, n))
    L.append('ex:%s backlog:hasAuditNote %s .\n' % ("Lineage4", lit("RANKING (%s UTC): until 2026-11-01 the exam scope is worked first. The executors of this lineage start before the executors of the chapter lineage; CI-5 stays as chapter work in ex:Lineage2 (maintained by a different project) and is not suspended." % n)))
    for m in members:
        for k, (via, a_, b_) in enumerate((("T_Refine", "Proposed", "Ready"),)):
            L.append('ex:Mv4_%s_%d a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:%s ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (
                m, k, lit("%s moved from %s to %s" % (m, a_, b_)), m, via, n, lit("Recorded at the Backlog stage of the exam lineage: refined (%s) and ready after the readiness check ex:RC4_%s; no executor has started." % (n, m) if b_ == "Ready" else "Recorded at the Backlog stage of the exam lineage: refinement event ex:Refine4_%s." % m)))
    pursued = {}
    for sid, (title, wants, tks, ep, dl, ob, rr, size) in STORIES.items(): pursued.setdefault(ob, []).append(sid)
    for sid, title, wants, ep, dl, ob in LATER: pursued.setdefault(ob, []).append(sid)
    for e, (label, ent, ob) in EPS.items(): pursued.setdefault(ob, []).append(e)
    pursued.setdefault("Obj4_PapersBuilt", []).append("Init4_Exams")
    for ob, xs in pursued.items():
        L.append('ex:%s backlog:metricMovableBy %s .\n' % (ob, ", ".join("ex:" + x for x in xs)))
    t += "".join(L)
    out = ('\n%s a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the exam lineage"@en ;\n    backlog:belongsToLineage ex:Lineage4 ;\n    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out4_Objective ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (OUTB, X.digest(t, "Backlog"))
    return t + out, "Exam lineage, Backlog stage closed: three stories with six tasks (critical points of chapters 1 to 4 and 6 to 8, design of the paper) Ready in box 1, five later stories Proposed; criterion, readiness checks, planned control, deployment plan; Out4_Backlog closes the stage."

def ev_fill(t, stage, commit):
    t = fill_prev(t, stage, commit)
    return t, "closedAtCommit of the %s stage output of the exam lineage set to the commit that closed it (%s)." % (stage, commit)

def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read(); a = sys.argv[2:]
    fn = {"scope": lambda: ev_scope(t, a[0]), "goal": lambda: ev_goal(t, a[0]), "objective": lambda: ev_objective(t, a[0]), "backlog": lambda: ev_backlog(t, a[0]), "fill": lambda: ev_fill(t, a[0], a[1])}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(W.write_new(src, nt, comment)))

if __name__ == "__main__":
    main()
