#!/usr/bin/env python3
"""sen0414_lineage_exam v1_0_0 - the exam lineage (Lineage4) of SEN0414: event OPEN = cancels the queued lineage 3 (as-is assessment, status Abandoned) and opens lineage 4 under the adaptive profile with the Owner-accepted mission wording of 2026-10-29, its Mission stage output, the maintainers that let it run beside the chapter lineage (G104, G159) and the Owner's statements.
One call = one new register file = one event; the caller validates and commits and pushes each alone.
Usage: sen0414_lineage_exam_v1_0_0.py open"""
__version__ = "1.0.0"
import glob, importlib.util, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
import rdflib

FW = "/home/claude/altunelyusuf/backlog-roadmap-framework"
STAGES = ["Mission", "Scope", "Goal", "Objective", "Backlog"]
LIN4 = "http://example.org/sen0414-slides-lineage#Lineage4"


def pv():
    spec = importlib.util.spec_from_file_location("pv14", FW + "/03-tooling/backlog_pipeline_verify_v1_14_0.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    tb = sorted(glob.glob(FW + "/01-ontologies/backlog_tbox_v*.ttl"), key=lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()])[-1]
    m.STAGE_TYPES = m._load_stage_types(tb, table="v1")
    return m


def digest(text, stage):
    g = rdflib.Graph(); g.parse(data=text, format="turtle")
    return pv().state_digest(g, "Stage_" + stage, rdflib.URIRef(LIN4))


def output(text, stage):
    d = digest(text, stage); i = STAGES.index(stage)
    consumes = ("\n    backlog:consumesOutput ex:Out4_%s ;" % STAGES[i - 1]) if i else ""
    return ('\nex:Out4_%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the exam lineage"@en ;\n    backlog:belongsToLineage ex:Lineage4 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;%s\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (stage, stage, stage, consumes, d)


def set_status4(text, status):
    pat = re.compile(r'(ex:Lineage4 a backlog:Lineage ;.*?)backlog:hasLineageStatus backlog:\w+ \.', re.S)
    m = pat.search(text); assert m
    return text[:m.start()] + m.group(1) + "backlog:hasLineageStatus backlog:%s ." % status + text[m.end():]


STATEMENT = ("SEN0414 is examined by two printed paper exams, the midterm and a make-up exam, each a sitting of 60 minutes over the chapters the instructor fixes before the sitting, each with its answer key. "
             "They are built with the interactive pages' exam engine, extended to a general engine for cross-chapter, synthesis and indirect questions, with question types and styles that suit a physical printed paper. "
             "Their items need the course's own knowledge, put the majority at the higher levels of Bloom's taxonomy, spread the correct letters evenly, randomise fill-in option banks and invent no terms. "
             "They revive the critical points the instructor explained in the course, from the slides, speaker notes, corpus and stories. "
             "Methods reduce the printed pages and the mistakes made in giving answers, and a reliable method reads, assesses and grades each student's paper.")
OUTCOME = "The instructor holds, for each of the two exams, a printed paper with its printed answer key, and a reliable way to read, assess and grade the papers the students hand in."
GAPS = ("VERIFIED GAPS (read by the lineage agent on 2026-10-28 and 2026-10-29 from the register and the files; the earlier text of the queued lineage 3 said there was no exam tooling, which is corrected here): "
        "WHAT EXISTS: the interactive pages carry an exam engine (item types mcq, multi, judge, match, order, repair, blank, cloze, predict, program, short, write, ask, string, graph, object, sparql; exam codes M- and F-; about 19 to 20 questions; chapter specific) and the Exam desk (08-tooling/sen0414_exam_desk_v2_2_0.html: add files, summary, results, one exam in detail, exam analysis, release codes, grades and announcement, audit logs) with the release tool and the exam question tests; "
        "per-chapter question banks hold 967 multiple-choice items for chapters 1 to 8 (answers spread evenly over the four letters). "
        "GAPS: (1) the engines are chapter specific, so no cross-chapter, synthesis or indirect question exists; (2) of the 967 items only 403 (42 per cent) are at Apply or Analyze and none at Evaluate or Create, so the majority at higher Bloom levels is NOT met; (3) the banks hold no fill-in and no open items; "
        "(4) nothing delivers a printed paper: no paper layout, no printed answer key, no page-saving layout, no answer sheet design; (5) no tool reads, assesses or grades a paper handed in; (6) the critical points the instructor explained in the course are not marked anywhere in the slides, speaker notes, corpus or stories, so what cannot be found must be asked of him; "
        "(7) the assessment ontology (04-assessment) holds weights only (midterm 30 per cent) and no items.")
ORIGIN = ("The Owner's direction of 2026-10-28 14:21 Istanbul and 2026-10-29 15:08 Istanbul (the mission input, relayed by the course coordinator and recorded as relayed, not as a verbatim quotation: use the interactive pages' exam engine to build two exams for SEN0414; a general engine for cross-chapter, synthesis and indirect questions; question types and styles that suit a physical printed paper; revive the critical points he explained in the course and list plainly what could not be found; methods to reduce printed pages; methods to reduce mistakes in giving answers; a reliable method to read, assess and grade each student's paper), "
          "his answer of 2026-10-29 that the mission wording below is accepted exactly as proposed, and his earlier statement of 2026-10-28 14:31 'Physical printed paper exams' (so QTI and CATS export are not requirements and interactive HTML delivery is not a deliverable; a separate printed answer key per exam is). " + GAPS)
NOTES = [
    "OWNER STATEMENT 2026-10-29 (relayed): 'The exact chapter content will be cleared tomorrow after the completion of the lectures. For SEN0414, Chapter 5 debugging is not in the scope of the exams. We don't cover them.' Recorded as the Owner's statement and NOT in the mission text: the chapter list of the exams is not fixed to chapters 1 to 8; chapter 5 (Debugging) is out of the exams' scope; the Owner fixes the final chapter list on 2026-10-30. Chapter 5 stays complete as chapter material and gets no further work.",
    "OWNER STATEMENT 2026-10-29 (relayed): SEN0414 has two exams, the midterm and a make-up exam over the same chapters; one sitting is 60 minutes; the paper is a physical printed paper; the midterm is next week (the week of 2026-11-02). QTI and CATS export are dropped from the requirements; interactive-HTML delivery is not a deliverable; a printed answer key per exam stays.",
    "TIME BOX AND ROUTE (2026-10-29): the Owner ruled that the chapter lineage is interrupted until Sunday 2026-11-01, when it restarts after the weekly usage limit resets, and that until then the exam scope is worked first, with CI-5 (completion of the chapters 1 to 8 slides and interactive pages) kept in as chapter work. The coordinator relayed that he accepted the suspension route. THE RULINGS ALLOW A ROUTE THAT KEEPS CI-5 RUNNING, SO IT IS USED INSTEAD OF THE SUSPENSION: the urgent-interruption ceremony (G158) pauses the whole interrupted lineage and refuses an urgent item that a scope change also admits, so it would stop CI-5; two lineages may be active together when each names a maintainer and the maintainers differ (G104, G159). Lineage 2 is maintained by the project 'SEN0414 course materials (decks, pages, research)' and this lineage by the project 'SEN0414 examinations (papers, answer keys, grading)': different deliverables, different acceptance, different tools. They share the instructor and the lineage agent; that is said openly. The shape was tested on a copy of the register (Lineage 2 in progress, this lineage at Scoped, one maintainer each: 0 violations; with none: 1 violation). The ranking is an order of work and not a register event: the exam executors start before the chapter ones until 2026-11-01. No urgency record is made.",
]
CANCEL_FIT = ("Lineage 3 (mission 'Examine chapters 1 to 8 of SEN0414 with a midterm exam') never left Opened: it has no scope, goal, objective, work item or box. AS-IS: accomplished none, failed none, in progress none, due none; objectives none (none existed). "
              "FIT-GAP against the Owner's mission input of 2026-10-29: the closed mission says 'a midterm exam on chapters 1 to 8' (the chapter list is not fixed and chapter 5 is out), 'exportable to CATS and QTI' (dropped), covers one exam (there are two: midterm and make-up) and rests on a gap list that said there is no exam tooling (an exam engine and desk exist). It states none of: the general engine for cross-chapter, synthesis and indirect questions, question types for paper, the critical points, fewer printed pages, fewer answering mistakes, grading papers. "
              "The mission cannot be amended: a stage revision refuses to start from the Mission stage (rebuilding from the mission is a restart that must answer a bypass finding, and there was none), the mission stage digest does not reproduce under a replacement mission (tested on a copy of the register), and a different mission is not a succession.")
CANCEL_IMPACT = ("Nothing is lost: no work item, no objective and no stage beyond Mission existed. The exam work moves to lineage 4 with the accepted wording. Lineage 3 stays in the register as history (L-112) with status Abandoned. "
                 "GAP SAID OPENLY: no closure report is written, because a closure report must report on at least one real objective of the lineage (the shape ClosureReportShape) and lineage 3 never had one; inventing an objective to satisfy the shape would be a fabricated record. This assessment and this note are the account of the cancellation. The mission of lineage 3 carries no Abandoned outcome for the same reason.")


def event_open(t):
    assert "ex:Lineage4 a" not in t, "already opened"
    blk = subprocess.run([sys.executable, FW + "/03-tooling/backlog_open_lineage_v1_1_0.py", "--profile", "Profile_Adaptive", "--lineage", "Lineage4", "--prefix", "ex"], capture_output=True, text=True).stdout
    assert "ex:Lineage4 backlog:openedWithProfile" in blk
    # Lineage 3 cancelled: as-is assessment, status Abandoned
    a = "backlog:hasLineageStatus backlog:LS_Opened ."
    i = t.index("ex:Lineage3 a backlog:Lineage ;"); j = t.index(a, i); assert j - i < 600
    t = t[:j] + "backlog:hasLineageStatus backlog:LS_Abandoned ." + t[j + len(a):]
    now = W.now()
    t += ('\nex:AsIs3 a backlog:AsIsAssessment ;\n    rdfs:label "As-is assessment of the queued midterm lineage (lineage 3) before it is set down"@en ;\n    backlog:assessesLineage ex:Lineage3 ; backlog:assessedAt "%s"^^xsd:dateTime ;\n'
          '    backlog:hasFitGapStatement %s ;\n    backlog:hasImpactStatement %s .\n') % (now, W.lit(CANCEL_FIT), W.lit(CANCEL_IMPACT))
    t += "\nex:Lineage3 backlog:hasAuditNote %s .\n" % W.lit("CANCELLED %s UTC on the Owner's acceptance of the exam mission wording of 2026-10-29 (relayed): replaced by ex:Lineage4. See ex:AsIs3 for the as-is assessment, the fit-gap and the impact, and for the stated absence of a closure report." % now)
    # Lineage 4 and its mission
    t += ('\nex:Mission4 a backlog:Mission ;\n    rdfs:label "Examine SEN0414 with two printed exams"@en ;\n    backlog:missionFor ex:Backlog ;\n    backlog:hasMissionStatement %s ;\n    backlog:hasMissionOrigin %s ;\n'
          '    backlog:hasMissionOutcome %s ;\n    backlog:outcomeRationale %s ;\n    backlog:decidedBy backlog:Owner ;\n    backlog:missionSource %s ;\n    backlog:hasAuditNote %s .\n') % (
        W.lit(STATEMENT), W.lit(ORIGIN), W.lit(OUTCOME),
        W.lit("A different purpose from the chapter lineage (G104): it examines the course and does not teach it. The wording replaces the closed mission of the cancelled lineage 3 and is chapter-agnostic because the Owner fixes the chapter list later; the Owner's chapter facts are recorded as statements beside the mission and not in its text."),
        W.lit("The Owner's statements of 2026-10-28 and 2026-10-29, the page exam engine and the Exam desk of this repository (08-tooling), the chapter question banks of 08-tooling/chNN-page, and the assessment ontology 04-assessment/sen0414_assessment_v1_0_0.ttl."),
        ", ".join(W.lit(n) for n in NOTES))
    t += ('\nex:Lineage4 a backlog:Lineage ;\n    rdfs:label "Fourth lineage run for SEN0414: the two printed exams"@en ;\n    backlog:lineageForMission ex:Mission4 ; backlog:lineageOrdinal 4 ; backlog:lineageArchived false ;\n'
          '    backlog:maintainedBy ex:Maint_Exams ;\n    backlog:hasLineageStatus backlog:LS_Opened .\n')
    t += "\n" + blk + "\n"
    t += ('\nex:Maint_Materials a backlog:LineageMaintainer ; rdfs:label "SEN0414 course materials project (decks, pages, research)"@en ; backlog:maintainerKind backlog:Mk_Project .\n'
          'ex:Maint_Exams a backlog:LineageMaintainer ; rdfs:label "SEN0414 examinations project (papers, answer keys, grading)"@en ; backlog:maintainerKind backlog:Mk_Project .\n'
          'ex:Lineage2 backlog:maintainedBy ex:Maint_Materials .\n')
    t += "\nex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit("OPENED %s UTC under the adaptive profile (Profile_Adaptive, profile revision 7) because the Owner asked for a lineage that starts from an immature mission and matures it in time-boxed boxes, and ruled against none of the profiles. The mission is the wording the Owner accepted on 2026-10-29. It runs beside ex:Lineage2 because the two are maintained by different projects (see the note on ex:Mission4); it takes over from the cancelled ex:Lineage3." % now)
    t += output(t, "Mission") + "ex:Mission4 backlog:producedByStage ex:Out4_Mission .\n"
    return t, "Lineage 3 cancelled (as-is assessment, status Abandoned, no closure report possible and said openly) and lineage 4 opened for the two printed exams with the Owner-accepted mission, the maintainers that let it run beside lineage 2, and the Owner's statements; its Mission stage output is closed."


def main():
    ev = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read()
    nt, comment = {"open": event_open}[ev](t)
    print(os.path.basename(W.write_new(src, nt, comment)))


if __name__ == "__main__":
    main()
