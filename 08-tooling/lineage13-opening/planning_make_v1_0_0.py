#!/usr/bin/env python3
"""planning_make 1.0.0 (Lineage13, 2026-11-26): writes the planning stage file (register 1.5.0): five packages, five iterations, iteration 1 planned with typed tasks. A lineage's own script, disclosed."""
import sys
Q=lambda s:s.replace('"','\\"')
EXE="ex:Executor_ClaudeCodeSession"
IT=[("1","16","2026-11-26T17:10:00","2026-11-26T23:59:00"),("2","17","2026-11-27T00:00:00","2026-11-27T05:59:00"),("3","18","2026-11-27T06:00:00","2026-11-27T11:59:00"),("4","19","2026-11-27T12:00:00","2026-11-27T17:59:00"),("5","20","2026-11-27T18:00:00","2026-11-27T23:59:00")]
NAME={"16":"SQLite Databases","17":"PDF and Word Documents","18":"CSV, JSON and XML","19":"Time and Scheduling","20":"Email, Texts and Push Notifications"}
PK={"16":["Page_16","Release_16","Measure_StoryRepeat"],"17":["Page_17","Release_17"],"18":["Spec_18","Deck_18","Page_18","Release_18","Measure_Links"],"19":["Spec_19","Deck_19","Page_19","Release_19"],
    "20":["Spec_20","Deck_20","Page_20","Release_20","Measure_MatchingCode","Measure_PageTest","OwnVersions","Guards"]}
DEL={"16":["NoAnalogies_16","Page_16","PageCode_16","ReleaseRecord_16","Measures"],"17":["NoAnalogies_17","Page_17","PageCode_17","ReleaseRecord_17"],
 "18":["Spec_18","Deck_18","Reader_18","NoAnalogies_18","Page_18","PageCode_18","ReleaseRecord_18"],"19":["Spec_19","Deck_19","Reader_19","NoAnalogies_19","Page_19","PageCode_19","ReleaseRecord_19"],
 "20":["Spec_20","Deck_20","Reader_20","NoAnalogies_20","Page_20","PageCode_20","ReleaseRecord_20","OwnVersion"]}
o=['''@prefix backlog: <http://example.org/backlog#> .
@prefix ex:      <http://example.org/sen0414-ch1620corr-lineage#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<http://example.org/sen0414-ch1620corr-lineage> a owl:Ontology ;
    rdfs:label "Fresh narrow lineage: SEN0414 Chapters 16 to 20 corrections"@en ;
    owl:versionInfo "1.5.0" ; owl:versionIRI <http://example.org/sen0414-ch1620corr-lineage/1.5.0> ;
    owl:priorVersion <http://example.org/sen0414-ch1620corr-lineage/1.4.0> ; dcterms:identifier "sen0414_ch1620corr_lineage" ;
    rdfs:comment "1.5.0 (2026-11-26): Planning stage of Lineage13: five packages (one per chapter, the last also carrying the closing stories), five time-boxed iterations that match them, and the planning of the first iteration only (refinement, planning events, typed tasks). Iterations 2 to 5 are planned when they start, by small steps. Dates are forecasts, never deadlines."@en .

ex:Lineage13 backlog:hasAuditNote "2026-11-26: the lineage status was not advanced stage by stage while the chain was built (Mission, Scope, Goal, Objective, Backlog); the commits of 1.0.0 to 1.4.0 are the witness of that order. The status pointer (one value, moved in place) and the story and task states are moved in the next merged register, because a delta file only adds statements and a second value would break the single-value rules; until then the lineage pointer still reads Opened and every item reads Proposed." .
''']
for i,n,s,e in IT:
    o.append(f'''ex:It13_{i} a backlog:Iteration ; backlog:hasIdentifier "It13_{i}" ; backlog:belongsToLineage ex:Lineage13 ; backlog:memberOfContainer ex:Backlog13 ;
    backlog:iterationStart "{s}"^^xsd:dateTime ; backlog:iterationEnd "{e}"^^xsd:dateTime ;
    rdfs:label "Iteration {i}: chapter {n}{' and the closing stories' if n=='20' else ''}"@en ;
    rdfs:comment "Time box matching package P13_Ch{n}. The dates are a forecast set to fit the objective checkpoints (2026-11-28) and are not a measurement; nothing waits for them and a passed date invalidates nothing."@en .
''')
for i,n,s,e in IT:
    o.append(f'''ex:P13_Ch{n} a backlog:Package ; backlog:belongsToLineage ex:Lineage13 ; backlog:memberOfContainer ex:Backlog13 ; backlog:hasIdentifier "P13_Ch{n}" ;
    backlog:hasPackageVersion "Ch{n}-corr-1.0.0" ; backlog:targetsIteration ex:It13_{i} ;
''')
    for d in DEL[n]: o.append(f"    backlog:deliversDeliverable ex:Del13_{d} ;\n")
    o.append(f'    rdfs:label "Chapter {n} ({NAME[n]}) corrected{" and the lineage closed" if n=="20" else ""}"@en .\n')
for i,n,s,e in IT:
    for st in PK[n]: o.append(f"ex:ST13_{st} backlog:memberOfContainer ex:P13_Ch{n} .\n")
    o.append(f"ex:P13_Ch{n} backlog:memberOfContainer ex:It13_{i} .\n")
# iteration 1 planning
PLAN=[
("Page_16","Concern_Interaction","The page must run the slide code unchanged and in order, and carry the run-in-order menu item.",[
 ("SystemAnalysis","Cat_Maintenance","Read the chapter 16 page, manifest, page template and lambda-free A-box maker and list what the run-in-order item and the A-box need"),
 ("Implementation","Cat_Maintenance","Build the chapter 16 page with a lambda-free A-box, the Slide code tab and the run-in-order menu item as a new version"),
 ("Verification","Cat_Maintenance","Run the page-shapes check and the full page test and save the logs")],[(2,1),(3,2)]),
("Release_16","Concern_Data","The verdicts of the three roles are records that must be complete per condition.",[
 ("Validation","Cat_Maintenance","Record the verdicts of the academician, the faculty reviewer and the undergraduate reader on each reviewed condition"),
 ("Transition","Cat_Maintenance","Name the released versions, run the version check and write the release record")],[(2,1)]),
("Measure_StoryRepeat","Concern_Data","The story's names and links are the data compared across chapters.",[
 ("SystemAnalysis","Cat_LineageGovernance","Run the story-repeat check for chapters 1 to 25 and list every hit for chapters 16 to 20"),
 ("Verification","Cat_LineageGovernance","Read each hit against the other chapter and record it as a different story or a candidate for the Owner")],[(2,1)])]
for sid,conc,outc,tasks,deps in PLAN:
    s=f"ex:ST13_{sid}"
    o.append(f'''{s} backlog:hasApplicableConcern backlog:{conc} .
ex:RE13_{sid} a backlog:RefinementEvent ; backlog:belongsToLineage ex:Lineage13 ; backlog:refines {s} ; backlog:addressesConcern backlog:{conc} ;
    backlog:refinedAt "2026-11-26T17:10:00"^^xsd:dateTime ; backlog:hasRefinementOutcome "{Q(outc)} Acceptance criterion and typed tasks written; sizing left to the iteration." ;
    rdfs:label "Refinement of {sid}"@en .
ex:PE13_{sid} a backlog:PlanningEvent ; backlog:belongsToLineage ex:Lineage13 ; backlog:plansItem {s} ; backlog:plannedInto ex:It13_1 ; backlog:plannedAt "2026-11-26T17:10:00"^^xsd:dateTime ; rdfs:label "Planning of {sid} into iteration 1"@en .
''')
    for k,(tt,cat,lab) in enumerate(tasks,1):
        t=f"ex:TK13_{sid}_{k}"
        o.append(f'''ex:PE13_{sid} backlog:producesTask {t} .
{s} backlog:decomposesInto {t} .
{t} a backlog:ExecutionTask ; backlog:belongsToLineage ex:Lineage13 ; backlog:hasIdentifier "TK13_{sid}_{k}" ; backlog:hasState backlog:Proposed ; backlog:appliesDefinitionOfDone ex:DoD13 ;
    backlog:hasTaskType backlog:Task_{tt} ; backlog:responsible {EXE} ; backlog:hasInvestmentCategory backlog:{cat} ;
    backlog:memberOfContainer ex:It13_1 ; rdfs:label "{Q(lab)}"@en .
''')
    for a,b in deps: o.append(f"ex:TK13_{sid}_{a} backlog:dependsOn ex:TK13_{sid}_{b} .\n")
o.append("ex:TK13_Release_16_1 backlog:dependsOn ex:TK13_Page_16_3 .\nex:TK13_Release_16_1 backlog:dependsOn ex:TK13_Measure_StoryRepeat_2 .\n")
open(sys.argv[1],"w").write("".join(o))
