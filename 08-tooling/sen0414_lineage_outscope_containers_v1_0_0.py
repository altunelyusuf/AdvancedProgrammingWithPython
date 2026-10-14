#!/usr/bin/env python3
"""sen0414_lineage_outscope_containers v1_0_0 - records, in a NEW version of the slides lineage register, an epic or the initiative as Done once every
member it decomposes into is Done in the register. Start and finish are the earliest start and latest finish of its members, read from the register;
nothing else is added.  Usage: sen0414_lineage_outscope_containers_v1_0_0.py ID...   (e.g. EP_Deck EP_Research EP_Page, later Init_Slides)
Refuses an item whose members are not all Done.
"""
__version__ = "1.0.0"
import os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_outscope_v1_1_0 as M
B, EX = M.B, M.EX


def main():
    ids = sys.argv[1:]
    src = M.newest(); t = open(src, encoding="utf-8").read()
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    add = []
    for i in ids:
        ms = list(g.objects(EX[i], B.decomposesInto))
        assert ms and all((m, B.hasState, B.Done) in g for m in ms), "%s has members that are not Done" % i
        st = min(str(g.value(m, B.startedAt)) for m in ms); fi = max(str(g.value(m, B.finishedAt)) for m in ms)
        pat = re.compile(r"^(ex:%s a backlog:\w+.*?)backlog:hasState backlog:Proposed ;" % re.escape(i), re.S | re.M)
        assert pat.search(t), i
        t = pat.sub(lambda m: m.group(1) + "backlog:hasState backlog:Done ;", t, count=1)
        add.append('ex:%s backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime .\n' % (i, st, fi))
    nxt, cur = M.next_version(src)
    out = M.write_new(src, t + "\n" + "".join(add), nxt, cur, "%s recorded Done: every member they decompose into is Done in this register; start and finish are the members' earliest start and latest finish." % ", ".join(ids))
    print(os.path.basename(out))


if __name__ == "__main__":
    main()
