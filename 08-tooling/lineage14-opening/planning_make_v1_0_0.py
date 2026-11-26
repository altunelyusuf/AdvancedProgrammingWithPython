#!/usr/bin/env python3
"""planning_make 1.0.0 (Lineage14, 2026-11-26): writes the planning stage file (register 1.5.0): five packages, five iterations, iteration 1 planned with typed tasks. A lineage's own script, disclosed."""
import sys
Q=lambda s:s.replace('"','\\"')
EXE="ex:Executor_ClaudeCodeSession"
IT=[("1","21","2026-11-26T17:40:00","2026-11-26T23:59:00"),("2","22","2026-11-27T00:00:00","2026-11-27T05:59:00"),("3","23","2026-11-27T06:00:00","2026-11-27T11:59:00"),("4","24","2026-11-27T12:00:00","2026-11-27T17:59:00"),("5","25","2026-11-27T18:00:00","2026-11-27T23:59:00")]
NAME={"21":"Making Graphs and Manipulating Images","22":"Recognizing Text in Images","23":"Controlling the Keyboard and Mouse","24":"Text-to-Speech and Speech Recognition","25":"Threads"}
PK={n:[f"Spec_{n}",f"Deck_{n}",f"Page_{n}",f"Release_{n}"] for n in NAME}
PK["25"]+=["Measure_Links","Measure_MatchingCode","Measure_PageTest","Measure_StoryRepeat","OwnVersions","Guards"]
DEL={n:[f"{k}_{n}" for k in ("Spec","Deck","Reader","NoAnalogies","Page","PageCode","ReleaseRecord")] for n in NAME}
DEL["25"]+=["OwnVersion","Measures"]
o=['''@prefix backlog: <http://example.org/backlog#> .
@prefix ex:      <http://example.org/sen0414-ch2125corr-lineage#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<http://example.org/sen0414-ch2125corr-lineage> a owl:Ontology ;
    rdfs:label "Fresh narrow lineage: SEN0414 Chapters 21 to 25 corrections"@en ;
    owl:versionInfo "1.5.0" ; owl:versionIRI <http://example.org/sen0414-ch2125corr-lineage/1.5.0> ;
    owl:priorVersion <http://example.org/sen0414-ch2125corr-lineage/1.4.0> ; dcterms:identifier "sen0414_ch2125corr_lineage" ;
    rdfs:comment "1.5.0 (2026-11-26): Planning stage of Lineage14: five packages (one per chapter, the last also carrying the measurement and closing stories), five time-boxed iterations that match them, and the planning of the first iteration only (refinement, planning events, typed tasks). Iterations 2 to 5 are planned when they start, by small steps. Dates are forecasts, never deadlines."@en .

ex:Lineage14 backlog:hasAuditNote "2026-11-26: the lineage status was not advanced stage by stage while the chain was built (Mission, Scope, Goal, Objective, Backlog); the commits of 1.0.0 to 1.4.0 are the witness of that order. The status pointer (one value, moved in place) and the story and task states are moved in the next merged register, because a delta file only adds statements and a second value would break the single-value rules; until then the lineage pointer still reads Opened and every item reads Proposed." .
''']
for i,n,s,e in IT:
    o.append(f'''ex:It14_{i} a backlog:Iteration ; backlog:hasIdentifier "It14_{i}" ; backlog:belongsToLineage ex:Lineage14 ; backlog:memberOfContainer ex:Backlog14 ;
    backlog:iterationStart "{s}"^^xsd:dateTime ; backlog:iterationEnd "{e}"^^xsd:dateTime ;
    rdfs:label "Iteration {i}: chapter {n}{' and the closing stories' if n=='25' else ''}"@en ;
    rdfs:comment "Time box matching package P14_Ch{n}. The dates are a forecast set to fit the objective checkpoints (2026-11-28) and are not a measurement; nothing waits for them and a passed date invalidates nothing."@en .
''')
for i,n,s,e in IT:
    o.append(f'''ex:P14_Ch{n} a backlog:Package ; backlog:belongsToLineage ex:Lineage14 ; backlog:memberOfContainer ex:Backlog14 ; backlog:hasIdentifier "P14_Ch{n}" ;
    backlog:hasPackageVersion "Ch{n}-corr-1.0.0" ; backlog:targetsIteration ex:It14_{i} ;
''')
    for d in DEL[n]: o.append(f"    backlog:deliversDeliverable ex:Del14_{d} ;\n")
    o.append(f'    rdfs:label "Chapter {n} ({NAME[n]}) corrected{" and the lineage closed" if n=="25" else ""}"@en .\n')
for i,n,s,e in IT:
    for st in PK[n]: o.append(f"ex:ST14_{st} backlog:memberOfContainer ex:P14_Ch{n} .\n")
    o.append(f"ex:P14_Ch{n} backlog:memberOfContainer ex:It14_{i} .\n")
n="21"
PLAN=[
(f"Spec_{n}","Concern_Data","The examples, result visuals, words and plan of the first-version deck are the data the spec must carry over unchanged in meaning.",[
 ("SystemAnalysis","Cat_Maintenance","Read the chapter 21 first-version builder, examples and stories and list what the spec and the chapter-code manifest must carry"),
 ("Implementation","Cat_Maintenance","Write the chapter 21 spec for the generic builder 2.10.0 with its examples, result visuals, words and plan"),
 ("Verification","Cat_Maintenance","Run the generic builder on the spec, compare the story and example entries with the first-version deck and save the build log")],[(2,1),(3,2)]),
(f"Deck_{n}","Concern_Interaction","The deck must teach one thing per slide and carry the reader's notes and balloons.",[
 ("Implementation","Cat_Maintenance","Write the chapter 21 words, notes and balloons so that notes speak to the reader, with no analogy, prompt or lambda"),
 ("Verification","Cat_Maintenance","Build the deck, run the deck checks and the material check and save the logs"),
 ("Validation","Cat_Maintenance","Read the deck as the academician, the faculty reviewer and the undergraduate reader and correct what the reading finds")],[(2,1),(3,2)]),
(f"Page_{n}","Concern_Interaction","The page must run the slide code unchanged and in order, and carry the run-in-order menu item.",[
 ("SystemAnalysis","Cat_Maintenance","Read the chapter 21 manifest, page template and lambda-free A-box maker and list what the run-in-order item and the A-box need"),
 ("Implementation","Cat_Maintenance","Build the chapter 21 page with a lambda-free A-box, the Slide code tab and the run-in-order menu item as a new version"),
 ("Verification","Cat_Maintenance","Run the page-shapes check and the full page test and save the logs")],[(2,1),(3,2)]),
(f"Release_{n}","Concern_Data","The verdicts of the three roles are records that must be complete per condition.",[
 ("Validation","Cat_Maintenance","Record the verdicts of the academician, the faculty reviewer and the undergraduate reader on each reviewed condition"),
 ("Transition","Cat_Maintenance","Name the released versions, run the version check and write the release record")],[(2,1)])]
for sid,conc,outc,tasks,deps in PLAN:
    s=f"ex:ST14_{sid}"
    o.append(f'''{s} backlog:hasApplicableConcern backlog:{conc} .
ex:RE14_{sid} a backlog:RefinementEvent ; backlog:belongsToLineage ex:Lineage14 ; backlog:refines {s} ; backlog:addressesConcern backlog:{conc} ;
    backlog:refinedAt "2026-11-26T17:40:00"^^xsd:dateTime ; backlog:hasRefinementOutcome "{Q(outc)} Acceptance criterion and typed tasks written; sizing left to the iteration." ;
    rdfs:label "Refinement of {sid}"@en .
ex:PE14_{sid} a backlog:PlanningEvent ; backlog:belongsToLineage ex:Lineage14 ; backlog:plansItem {s} ; backlog:plannedInto ex:It14_1 ; backlog:plannedAt "2026-11-26T17:40:00"^^xsd:dateTime ; rdfs:label "Planning of {sid} into iteration 1"@en .
''')
    for k,(tt,cat,lab) in enumerate(tasks,1):
        t=f"ex:TK14_{sid}_{k}"
        o.append(f'''ex:PE14_{sid} backlog:producesTask {t} .
{s} backlog:decomposesInto {t} .
{t} a backlog:ExecutionTask ; backlog:belongsToLineage ex:Lineage14 ; backlog:hasIdentifier "TK14_{sid}_{k}" ; backlog:hasState backlog:Proposed ; backlog:appliesDefinitionOfDone ex:DoD14 ;
    backlog:hasTaskType backlog:Task_{tt} ; backlog:responsible {EXE} ; backlog:hasInvestmentCategory backlog:{cat} ;
    backlog:memberOfContainer ex:It14_1 ; rdfs:label "{Q(lab)}"@en .
''')
    for a,b in deps: o.append(f"ex:TK14_{sid}_{a} backlog:dependsOn ex:TK14_{sid}_{b} .\n")
o.append("ex:TK14_Deck_21_1 backlog:dependsOn ex:TK14_Spec_21_3 .\nex:TK14_Page_21_1 backlog:dependsOn ex:TK14_Deck_21_2 .\nex:TK14_Release_21_1 backlog:dependsOn ex:TK14_Page_21_3 .\n")
open(sys.argv[1],"w").write("".join(o))
