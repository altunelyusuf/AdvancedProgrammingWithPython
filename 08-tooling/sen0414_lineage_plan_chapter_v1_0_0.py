#!/usr/bin/env python3
"""sen0414_lineage_plan_chapter v1_0_0 - plans one chapter's three admitted stories into a new iteration of the SEN0414 slide
lineage and makes them Ready, in a new version of the register; the old version stays.

Usage: sen0414_lineage_plan_chapter_v1_0_0.py CHAPTER ITERATION_NUMBER "OWNER MESSAGE STAMP (UTC ISO)" "end of iteration (UTC ISO)" "source of the end"

Everything is copied from how the register already planned chapter 6 (Iter_4): a planning event, a refinement event, a WSJF score with the
components reused from chapters 1 and 2, a build task and a verify task per story, the story Ready. Nothing is started or Done here: a start is
recorded by its own later version, when the work begins, and a finish by the version after it.
"""
__version__ = "1.0.0"
import glob, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.path.join(REPO, "07-lineage")
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
WSJF = {"Research": (13, 20, 13, 3), "Page": (13, 20, 5, 3), "Deck": (20, 20, 8, 5)}
ORDER = ("Research", "Deck", "Page")


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+_\d+_\d+)\.ttl$", p).group(1).split("_")]


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def main():
    ch, itn, at, end, endsrc = sys.argv[1:6]
    cid = "Threads" if ch == "T" else "Ch%02d" % int(ch)
    files = sorted(glob.glob(os.path.join(LIN, "sen0414_slides_lineage_v*.ttl")), key=ver)
    src = files[-1]
    cur = ".".join(map(str, ver(src)))
    nxt = ".".join(map(str, [ver(src)[0], ver(src)[1] + 1, 0]))
    out = os.path.join(LIN, "sen0414_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
    assert not os.path.exists(out)
    g = rdflib.Graph(); g.parse(src)
    t = open(src, encoding="utf-8").read()
    it = "Iter_%s" % itn
    assert (EX[it], None, None) not in g, it + " exists"
    title = str(g.value(EX["ST_Deck_" + cid], rdflib.RDFS.label)).split(": ", 1)[1]
    ref = {k: str(g.value(EX["Refine_%s_Ch06" % k], B.hasRefinementOutcome)) for k in ORDER}
    L = ["\n#################################################################\n#  %s: %s planned into %s\n#################################################################\n" % (nxt, title, it)]
    members = []
    for k in ORDER:
        sid = "%s_%s" % (k, cid); st = "ST_" + sid
        assert (EX[st], B.hasState, B.Proposed) in g, st + " is not Proposed"
        m = re.search(r"ex:%s a backlog:Story.*?\n\n" % re.escape(st), t, re.S)
        blk = m.group(0)
        nb = blk.replace("backlog:hasState backlog:Proposed ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason \"Scored when its own iteration is planned.\" .",
                         "backlog:hasState backlog:Ready ; backlog:memberOfContainer ex:%s ;\n    backlog:hasPriorityScore ex:Score_%s ;\n    backlog:decomposesInto ex:TK_%s_Build, ex:TK_%s_Verify ." % (it, sid, sid, sid))
        assert nb != blk, st + " block unchanged"
        t = t.replace(blk, nb)
        bv, tc, rr, js = WSJF[k]
        v = (bv + tc + rr) / js
        why = ("Components reused from the same kind of story in chapters 1 and 2, whose scores the owner approved; they were not approved again for this story, so they are a proposal to the owner (L-116), not an approval. "
               "Time criticality is set by the next class, 14:00 Istanbul on 2026-10-16.")
        lab = "%s for %s" % (k, cid)
        L.append('ex:Score_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n'
                 '    backlog:hasScoreRationale "WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %d, %s" .\n' % (sid, v, at, bv, tc, rr, js, why))
        L.append('ex:Plan_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration %s"@en ; backlog:belongsToLineage ex:Lineage ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Owner ; backlog:plannedInto ex:%s ;\n'
                 '    backlog:plansItem ex:%s ; backlog:producesTask ex:TK_%s_Build, ex:TK_%s_Verify .\n' % (sid, lab, itn, at, it, st, sid, sid))
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n'
                 '    backlog:refinedBy backlog:Owner ; backlog:groomsForIteration ex:%s ; backlog:hasRefinementOutcome "%s" .\n' % (sid, lab, st, at, it, esc(ref[k])))
        for tk, tkl, note in (("Build", "build", "Build it."), ("Verify", "verify", "Run the chapter check and require the stale fixture refused.")):
            dep = "" if k == "Research" or tk == "Build" and False else ("; backlog:dependsOn ex:ST_Research_%s " % cid if k != "Research" and tk == "Verify" or k != "Research" and tk == "Build" else "")
            L.append('ex:TK_%s_%s a backlog:ExecutionTask ; rdfs:label "%s: %s"@en ; backlog:hasIdentifier "TK_%s_%s" ; backlog:hasTitle "%s %s" ;\n    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ; backlog:hasState backlog:Proposed ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
                     '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s score; scoring both would double-count." ;\n'
                     '    backlog:hasAuditNote "%s" %s.\n' % (sid, tk, lab, tkl, sid, tk, tk, lab, tk, note, dep))
        members.append(st)
    L.append('ex:%s a backlog:Iteration ; rdfs:label "Iteration %s: %s, before the class of 16 October"@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n'
             '    backlog:hasDurationSource "%s" ;\n    backlog:hasSprintGoal "%s researched, its deck built as a lecture and its page built on the current template, each checked by the course\'s own gates, ready to present." ;\n    backlog:hasMember %s .\n'
             % (it, itn, title, it, at, end, esc(endsrc), title, ", ".join("ex:" + m for m in members)))
    g2 = rdflib.Graph(); g2.parse(data=t + "".join(L), format="turtle")
    body = t + "".join(L)
    body = re.sub(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(cur),
                  'owl:versionInfo "%s" ; owl:versionIRI <http://example.org/sen0414-slides-lineage/%s> ; owl:priorVersion <http://example.org/sen0414-slides-lineage/%s> ;' % (nxt, nxt, cur), body, count=1)
    body = body.replace('dcterms:identifier "sen0414_slides_lineage" ;', 'dcterms:identifier "sen0414_slides_lineage" ;\n    rdfs:comment "%s (%s): %s planned into %s before any work on it: planning, refinement, score, build and verify tasks per story, the stories Ready. Nothing started or Done in this version."@en ;' % (nxt, at[:10], title, it), 1)
    open(out, "w", encoding="utf-8").write(body)
    print(os.path.basename(out), len(g2), "triples")


main()
