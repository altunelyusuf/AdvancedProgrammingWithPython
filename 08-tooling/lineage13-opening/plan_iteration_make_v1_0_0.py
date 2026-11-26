#!/usr/bin/env python3
"""plan_iteration_make 1.0.0 (Lineage13, 2026-11-26): writes the planning delta (refinement events, planning events, typed tasks) of one iteration as a Turtle file for register_step_v1_1_0.py.
Usage: plan_iteration_make_v1_0_0.py ITERATION_NUMBER OUT.ttl PLAN.json
PLAN.json: [[story_id, concern, outcome_sentence, [[task_type, category, label], ...], [[later_task_no, earlier_task_no], ...]], ...]  and optional cross-story dependencies as ["dep", "TK13_a_1", "TK13_b_2"]."""
import json, sys
Q = lambda s: s.replace('"', '\\"')
import os
it, out, planf = sys.argv[1], sys.argv[2], sys.argv[3]; AT = os.environ.get("PLAN_AT", "2026-11-26T17:10:00")
plan = json.load(open(planf))
o = ['@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-ch1620corr-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n']
for item in plan:
    if item[0] == "dep":
        o.append(f"ex:{item[1]} backlog:dependsOn ex:{item[2]} .\n"); continue
    sid, conc, outc, tasks, deps = item; s = f"ex:ST13_{sid}"
    o.append(f'''{s} backlog:hasApplicableConcern backlog:{conc} .
ex:RE13_{sid} a backlog:RefinementEvent ; backlog:belongsToLineage ex:Lineage13 ; backlog:refines {s} ; backlog:addressesConcern backlog:{conc} ;
    backlog:refinedAt "{AT}"^^xsd:dateTime ; backlog:hasRefinementOutcome "{Q(outc)} Acceptance criterion and typed tasks written; sizing left to the iteration." ;
    rdfs:label "Refinement of {sid}"@en .
ex:PE13_{sid} a backlog:PlanningEvent ; backlog:belongsToLineage ex:Lineage13 ; backlog:plansItem {s} ; backlog:plannedInto ex:It13_{it} ; backlog:plannedAt "{AT}"^^xsd:dateTime ; rdfs:label "Planning of {sid} into iteration {it}"@en .
''')
    for k, (tt, cat, lab) in enumerate(tasks, 1):
        t = f"ex:TK13_{sid}_{k}"
        o.append(f'''ex:PE13_{sid} backlog:producesTask {t} .
{s} backlog:decomposesInto {t} .
{t} a backlog:ExecutionTask ; backlog:belongsToLineage ex:Lineage13 ; backlog:hasIdentifier "TK13_{sid}_{k}" ; backlog:hasState backlog:Proposed ; backlog:appliesDefinitionOfDone ex:DoD13 ;
    backlog:hasTaskType backlog:Task_{tt} ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:hasInvestmentCategory backlog:{cat} ;
    backlog:memberOfContainer ex:It13_{it} ; rdfs:label "{Q(lab)}"@en .
''')
    for a, b in deps: o.append(f"ex:TK13_{sid}_{a} backlog:dependsOn ex:TK13_{sid}_{b} .\n")
open(out, "w").write("".join(o))
