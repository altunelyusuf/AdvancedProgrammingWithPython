#!/usr/bin/env python3
"""sen0414_lineage_extend v1_0_0 - writes the next version of the SEN0414 slide lineage from the
newest one on disk, never editing the old file.

What it does, each step derived from a ruling or a validator finding, none stipulated:
  1. Aligns the register header with BP-D7 (owl:versionIRI + owl:priorVersion; the validator's L1
     refused the previous version because the header named no version IRI).
  2. Admits the chapters the owner's 2026-10-12 ruling brought into scope but the register never
     admitted - 12, 15-18, 20-23 - as the same three deliverables and three stories every other
     chapter has (Deck, Research, Page), Proposed, with one recorded ScopeChange decided by the
     Owner. Targets rise from 16 to 25 (24 chapters of the 3rd edition + multithreading).
  3. Names the Executor on every open item (validator L2), as the agentic-sdlc register does.
It does NOT record any item as started or Done: chapters 7-12 were built outside the register and
backfilling them would be the act the lineage discipline forbids (G23); that gap is disclosed in
the version comment instead.
"""
__version__ = "1.0.0"
import glob, json, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.path.join(REPO, "07-lineage")
INV = os.environ.get("SEN0414_INVENTORY", "/home/claude/Ontologies/automate-python-book-3e/00-source-inventory/source_inventory_v1_0_0.json")
NEW_CHAPTERS = (12, 15, 16, 17, 18, 20, 21, 22, 23)
KIND = [("Deck", "Deck", "the renewed lecture deck, restyled with PowerPoint's capabilities and rewritten to the edition it rests on", "Obj_DecksRenewed"),
        ("Research", "Research", "an RDODI four-stage research run on the chapter's subject, with its pedagogy stage and Courseware profile", "Obj_ResearchRecorded"),
        ("Page", "Page", "an interactive page for the chapter, enriched with the research results", "Obj_PagesBuilt")]
EXEC = "ex:Executor_ClaudeCodeSession"


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+_\d+_\d+)\.ttl$", p).group(1).split("_")]


def main():
    files = sorted(glob.glob(os.path.join(LIN, "sen0414_slides_lineage_v*.ttl")), key=ver)
    src = files[-1]
    cur = ".".join(map(str, ver(src)))
    nxt = ".".join(map(str, [ver(src)[0], ver(src)[1] + 1, 0]))
    out = os.path.join(LIN, "sen0414_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
    if os.path.exists(out):
        sys.exit("refusing to overwrite " + out)
    t = open(src, encoding="utf-8").read()
    title = {r["chapter"]: r["title"] for r in json.load(open(INV))["chapters"]}

    # 1. header
    base = "http://example.org/sen0414-slides-lineage"
    t, n = re.subn(r'owl:versionInfo "%s" ;' % re.escape(cur),
                   'owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; owl:priorVersion <%s/%s> ;' % (nxt, base, nxt, base, cur), t, count=1)
    assert n == 1, "header not found"
    comment = ('%s (2026-10-12): the register now admits the chapters the owner brought into scope on 2026-10-12 and never admitted - 12, 15-18 and 20-23 - '
               'as the same three deliverables and three stories as every other chapter, Proposed, recorded as one Owner-decided ScopeChange; the targets of the three counted '
               'objectives rise from 16 to 25 (24 chapters of the 3rd edition and multithreading from the 2nd). The header now carries owl:versionIRI and owl:priorVersion, which '
               'the validator\'s L1 had refused in %s, and every open item names its Executor (validator L2, refused in %s as well). DISCLOSED, NOT FIXED: chapters 7-12 are built, '
               'registered in the materials register and pushed, but their stories here are still Proposed because they were built before this register planned them; recording '
               'them Done now would be backfilling closed work that was never planned (G23) and the order check would name each as planned late. Whether they are recorded as such, '
               'or answered by a restart, is the owner\'s ruling and is not taken by this version. Chapters 13 onward are admitted before their work begins, which is what keeps them '
               'from the same gap.' % (nxt, cur, cur))
    t = t.replace('dcterms:identifier "sen0414_slides_lineage" ;', 'dcterms:identifier "sen0414_slides_lineage" ;\n    rdfs:comment "%s"@en ;' % comment.replace('"', "'"), 1)

    # 2. counted targets and area measures
    for o in ("Renewed decks passing the chapter check", "Chapters with a completed rdodi run", "Chapters with an interactive page carrying their research"):
        t = t.replace('"%s: from 0 to 16"' % o, '"%s: from 0 to 25"' % o)
    assert t.count('backlog:hasTargetValue "16"^^xsd:decimal') == 3
    t = t.replace('backlog:hasTargetValue "16"^^xsd:decimal', 'backlog:hasTargetValue "25"^^xsd:decimal')
    assert t.count('"16 chapters, each with') == 3
    t = t.replace('"16 chapters, each with', '"25 subjects (the 24 chapters of the 3rd edition and multithreading from the 2nd), each with')

    # 3. new deliverables and stories, appended
    L = ["\n#################################################################\n#  %s: chapters admitted by the owner's 2026-10-12 ruling\n#################################################################\n" % nxt]
    admitted = []
    for n_ in NEW_CHAPTERS:
        src_ = "3rd edition, chapter %d: %s" % (n_, title[n_])
        for k, label, what, obj in KIND:
            d, s = "Del_%s_Ch%02d" % (k, n_), "ST_%s_Ch%02d" % (k, n_)
            L.append('ex:%s a backlog:ScopeDeliverable ;\n    rdfs:label "%s for 3rd edition, chapter %d"@en ;\n    backlog:derivesFromMissionClause "every SEN0414 lecture deck teaches what the textbook teaches"^^xsd:string ;\n'
                     '    backlog:hasDeliverableText "%s, grounded in %s." ;\n    backlog:deliverableForArea ex:Area_%s ;\n    backlog:hasScopeLayer backlog:Layer_Product ;\n    backlog:hasProductScopeKind backlog:Kind_Functional .\n\n'
                     % (d, label, n_, what[0].upper() + what[1:], src_, k))
            dep = ""
            if k == "Deck" or k == "Page":
                dep = '    backlog:dependsOn ex:ST_Research_Ch%02d ;\n' % n_
            L.append('ex:%s a backlog:Story ; rdfs:label "%s: %s"@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle "%s for 3rd edition, chapter %d" ;\n'
                     '    backlog:belongsToLineage ex:Lineage ; backlog:memberOfContainer ex:Backlog ; backlog:admittedByOutput ex:Out_Backlog ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
                     '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "%s" ; backlog:soThat "students are taught from the edition they read, on researched ground" ;\n'
                     '    backlog:satisfiesDeliverable ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion ex:AC_Chapter ;\n'
                     '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n%s'
                     '    backlog:hasState backlog:Proposed ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned." .\n\n'
                     % (s, k, src_, s, k, n_, what, d, obj, dep))
            L.append("ex:Scope backlog:requiresDeliverable ex:%s .\nex:EP_%s backlog:decomposesInto ex:%s .\nex:%s backlog:metricMovableBy ex:%s .\n\n" % (d, k, s, obj, s))
            admitted.append(s)
    L.append('ex:SC_Chapters12_15to18_20to23 a backlog:ScopeChange ;\n    rdfs:label "Scope grown to the chapters the owner lifted from exclusion on 2026-10-12"@en ;\n    backlog:changesScope ex:Scope ;\n'
             '    backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n'
             '    backlog:hasScopeChangeRationale "The owner ruled on 2026-10-12 (recorded in ex:Excl_CommandLine and ex:Excl_Untaught) that chapter 12 and chapters 15-18 and 20-23 are renewed in the same chapter-by-chapter run. The boundary moved outward by nine chapters of three deliverables each; the cost is named rather than absorbed: the three counted objectives\' targets rise from 16 to 25, so the mission is not reached until all twenty-five subjects have a deck, a research run and a page. Nothing was traded away; the chapters already in scope keep their order." .\n\n'
             % ", ".join("ex:" + s for s in admitted))

    # 4. Executor on every open item (after the new stories exist)
    L.append('ex:Executor_ClaudeCodeSession a owl:NamedIndividual , backlog:Executor_SingleAgent ;\n    rdfs:label "Claude Code session - the AI-agent executor of this course package\'s own work"@en ;\n'
             '    rdfs:comment "One non-human executing party with no standing team membership, the same identity the framework\'s own A-Box calls its default AI-agent Executor (DefaultExecutor); the owner approves and teaches, the session performs the build." ;\n'
             '    rdfs:seeAlso <http://example.org/fixture-autofix#DefaultExecutor> .\n\n')
    body = t + "".join(L)
    g = rdflib.Graph(); g.parse(data=body, format="turtle")
    B = rdflib.Namespace("http://example.org/backlog#")
    EX = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
    open_items = sorted({s for s in g.subjects(B.hasState, B.Proposed)} | {s for s in g.subjects(B.hasState, B.Ready)} | {s for s in g.subjects(B.hasState, B.InProgress)})
    L2 = ["# Open items name their Executor (validator L2)\n"] + ["<%s> backlog:responsible %s .\n" % (s, EXEC) for s in open_items if str(s).startswith(str(EX)) and not list(g.objects(s, B.responsible))]
    body += "".join(L2)
    g2 = rdflib.Graph(); g2.parse(data=body, format="turtle")
    open(out, "w", encoding="utf-8").write(body)
    print("%s: %d triples (was %d); %d stories admitted; %d open items now name an Executor" % (os.path.basename(out), len(g2), len(rdflib.Graph().parse(src)), len(admitted), len(L2) - 1))


if __name__ == "__main__":
    main()
