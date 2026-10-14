#!/usr/bin/env python3
"""sen0414_lineage_outscope v1_1_0 - records, in NEW versions of the SEN0414 slides lineage register, the owner's route for work that was
finished before it was planned (backlog-roadmap-framework ruling G105, 2026-10-12): out-scope first, close the finished lineage, a
successor under the same mission takes the out-scoped work in. One call, one new file, one event; the caller commits it alone.

Usage: sen0414_lineage_outscope_v1_1_0.py EVENT [FACTS.json]
EVENT: declare | close | mission | scope | goal | objective | backlog | fill-commit KEY HASH
Nothing is placed in a file that was not computed or read here: stage digests come from the framework's own
backlog_pipeline_verify (state_digest), times from the clock, commits from git, finish dates and hashes from the FACTS file that
sen0414_lineage_git_facts reads out of git and the files themselves. Older register files are never opened for writing.
"""
__version__ = "1.1.0"
import datetime, glob, hashlib, json, os, re, subprocess, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.path.join(REPO, "07-lineage")
FW = "/home/claude/Ontologies/backlog-roadmap-framework"
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
OUT_STORIES = ["ST_%s_Ch%02d" % (k, n) for n in range(7, 13) for k in ("Deck", "Research", "Page")]
OTHER_OPEN = ["ST_ReworkOthers_Ch01_02_04"]
OPEN_CONTAINER_ITEMS = ["EP_Deck", "EP_Research", "EP_Page", "Init_Slides"]


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]


def newest():
    files = sorted(glob.glob(os.path.join(LIN, "sen0414_slides_lineage_v*.ttl")), key=ver)
    return files[-1]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def next_version(src):
    v = ver(src)
    return "%d.%d.0" % (v[0], v[1] + 1), "%d.%d.%d" % tuple(v)


def write_new(src, text, nxt, cur, comment):
    t = re.sub(r'owl:versionInfo "%s" ; owl:versionIRI <[^>]*> ; owl:priorVersion <[^>]*> ;' % re.escape(cur),
               'owl:versionInfo "%s" ; owl:versionIRI <http://example.org/sen0414-slides-lineage/%s> ; owl:priorVersion <http://example.org/sen0414-slides-lineage/%s> ;' % (nxt, nxt, cur), text, count=1)
    assert t != text, "header not found"
    t2 = t.replace('dcterms:identifier "sen0414_slides_lineage" ;', 'dcterms:identifier "sen0414_slides_lineage" ;\n    rdfs:comment "%s (%s): %s"@en ;' % (nxt, now()[:10], esc(comment)), 1)
    assert t2 != t
    out = os.path.join(LIN, "sen0414_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
    assert not os.path.exists(out), out
    rdflib.Graph().parse(data=t2, format="turtle")
    open(out, "w", encoding="utf-8").write(t2)
    return out


def ids(names):
    return ", ".join("ex:" + n for n in names)


# ---------------------------------------------------------------- events
def ev_declare(t):
    """Closure commit 1: the PartialScopeDeclaration, on the live lineage. Removes the asserted state of the register's root container,
    which the rules derive from its members (R1): with the unfinished work out-scoped the derived state is Done, and a container whose
    asserted state disagrees with the derived one is refused."""
    out = OUT_STORIES + OTHER_OPEN + OPEN_CONTAINER_ITEMS
    blk = ('\nex:Gap_OutScope_Ch07_12 a backlog:PartialScopeDeclaration ;\n'
           '    rdfs:label "Out-scoping of the work of this lineage that is not finished"@en ;\n'
           '    backlog:declaresGapFor ex:Lineage ; backlog:decidedBy backlog:Owner ;\n'
           '    backlog:outScopes %s ;\n'
           '    backlog:describesUncoveredScope "The deck, research and page stories of chapters 7 to 12 (18 stories) are finished in the course repository but were never planned, started or recorded here: they were built outside this register, and their stories still read Proposed with no planning event. Recording them Done inside this lineage would be backfilling closed work that was never planned (G23, G105). The story for the rework of the decks and pages of chapters 1, 2 and 4 with the teaching devices is held by the owner until he judges chapter 3 mature, which he has not done; it is unfinished. The three epics and the initiative that group the stories are open while any of those stories is open. All of them leave this lineage unchanged and unfinished, so that this lineage closes with no unfinished work inside it; the successor lineage under the same mission takes them in. Decided by the owner on 2026-10-12 (chapters 7 to 12 are tasks completed before the lineage, to be closed appropriately and kept outside the new scope) and executed on the framework ruling of the same date." .\n') % ids(out)
    t = t.replace("    backlog:hasState backlog:InProgress ; backlog:producedByStage ex:Out_Backlog ;", "    backlog:producedByStage ex:Out_Backlog ;", 1) if "    backlog:hasState backlog:InProgress ; backlog:producedByStage ex:Out_Backlog ;" in t else t
    return t + blk, "the lineage's unfinished work is out-scoped by an owner-decided PartialScopeDeclaration (18 stories of chapters 7-12, the rework story of chapters 1, 2 and 4, three epics, one initiative); the root container's asserted state is dropped because the rules derive it."


def ev_close(t):
    """Closure commit 2: the lineage is Achieved on its finished scope; the succession under the same mission opens the successor lineage."""
    a = 'backlog:lineageForMission ex:Mission ; backlog:lineageOrdinal 1 ; backlog:lineageArchived false ;\n    backlog:hasLineageStatus backlog:LS_InProgress ;'
    assert a in t
    t = t.replace(a, a.replace("LS_InProgress", "LS_Achieved"), 1)
    blk = ('\nex:Lineage2 a backlog:Lineage ;\n    rdfs:label "Second lineage run for the SEN0414 decks: the work finished before it was planned"@en ;\n'
           '    backlog:lineageForMission ex:Mission ; backlog:lineageOrdinal 2 ; backlog:lineageArchived false ;\n'
           '    backlog:adoptsObligationSet backlog:OS_SDLC_v2 ; backlog:adoptionRecordedAtOpen true .\n'
           '\nex:Succession_Ch07_12 a backlog:LineageSuccession ;\n    rdfs:label "Succession that takes in the out-scoped work of chapters 7 to 12"@en ;\n'
           '    backlog:succeedsLineage ex:Lineage ; backlog:successorLineage ex:Lineage2 ;\n    backlog:resolvesGap ex:Gap_OutScope_Ch07_12 ;\n'
           '    backlog:decidedBy backlog:Owner ;\n'
           '    backlog:successionRationale "The first lineage planned and finished chapters 1 to 6 and 13 to 24 with multithreading, each with a planning event before its work and evidence after it. Chapters 7 to 12 were built, tested and pushed before they were planned, so the first lineage can neither record them Done (that would add planning events after the work and move finished-late items) nor close with them still Proposed (closing unfinished work is not allowed). Restarting it would retract five correct stage outputs and answer a bypass that the order check does not find (it reads ORDERED). The owner therefore out-scoped the unfinished and unrecorded work in the previous event, this lineage closes complete on what it finished, and a successor under the same mission opens with the Scope of admitting the finished chapters, recorded now with their real finish dates from git. Cost of waiting: the register keeps stating Proposed for eighteen finished stories; cost of acting: one succession, five stage commits, and evidence re-run for eighteen items; enforcement value forgone: none, the chain of the first lineage stays untouched." .\n')
    return t + blk, "the lineage is Achieved on its finished scope; the succession ex:Succession_Ch07_12 under the same mission opens the successor lineage ex:Lineage2 and resolves the out-scoping declaration."


EVENTS = {"declare": ev_declare, "close": ev_close}


def main():
    ev = sys.argv[1]
    src = newest()
    t = open(src, encoding="utf-8").read()
    nxt, cur = next_version(src)
    if ev in EVENTS:
        nt, comment = EVENTS[ev](t)
    else:
        import sen0414_lineage_outscope_stages_v1_1_0 as stg
        nt, comment = stg.run(ev, t, sys.argv[2:], globals())
    out = write_new(src, nt, nxt, cur, comment)
    print(os.path.basename(out))


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
