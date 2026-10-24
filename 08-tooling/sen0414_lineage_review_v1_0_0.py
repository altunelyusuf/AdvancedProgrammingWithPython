#!/usr/bin/env python3
"""sen0414_lineage_review v1_0_0 - the review ceremony of Iteration 18 of the second lineage, in ONE new register version (modelled on the sibling's review of its iterations).
For each story of Iter_18 whose every task is Done on bridge-verified evidence: the story goes Done by T_Complete (finishedAt = its last task's finish, startedAt = its own start or its first task's start), execution
modality, a test harness of the story whose evidence is the verified evidence of its tasks, the story's own evidence links and an audit note. One SprintReviewCeremony (reviews the planning ceremony PC2_Iter_18; closesStory;
no closesIteration, because Iter_18 still has open members) and one MetricObservation for each objective the Done stories move (Obj2_StdDecks, Obj2_StdPages), whose value THIS RUN MEASURES (the deck standard check and the
deck overlap check on the newest decks; the page checks of the evidence bridge, run now, on the newest pages). The open stories are RE-SCORED after the completions (a score older than the latest completion is stale).
The criteria of the two pages carry an audit note naming the tool versions actually used (template 9.52.2, builder 4.18.1), which supersede the versions their committed text names.
Usage: sen0414_lineage_review_v1_0_0.py   (writes one new version; the caller validates, then commits)"""
__version__ = "1.0.0"
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rdflib
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
T = os.path.join(W.REPO, "08-tooling")
DECKS = {"06": "03-materials/ch06/SEN0414_Ch06_Lists_3e_v3_0_0.pptx", "07": "03-materials/ch07/SEN0414_Ch07_Dictionaries_3e_v2_0_0.pptx", "08": "03-materials/ch08/SEN0414_Ch08_Strings_3e_v2_0_0.pptx"}
PAGES = {"07": "03-materials/ch07/page/sen0414_ch07_page_v9_90_0.html", "08": "03-materials/ch08/page/sen0414_ch08_page_v9_90_0.html"}
RESCORE_OPEN = ["ST_Std_Deck_Ch09", "ST_Std_Page_Ch06", "ST_Std_Page_Ch09"]


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def run(*a):
    r = subprocess.run(list(a), cwd=W.REPO, capture_output=True, text=True); return r.returncode, r.stdout + r.stderr


def measure():
    decks = {}
    for n, d in DECKS.items():
        rc1, o1 = run(sys.executable, os.path.join(T, "sen0414_deck_standard_check_v1_0_0.py"), n, d); rc2, o2 = run(sys.executable, os.path.join(T, "sen0414_deck_overlap_check_v1_0_0.py"), d)
        m = re.search(r"SUMMARY PASS=(\d+) FAIL=(\d+) NOT_MEASURED=(\d+)", o1)
        decks[n] = (rc1 == 0 and rc2 == 0 and bool(m) and m.groups() == ("13", "0", "0") and "RESULT CLEAN" in o2, "%s; overlap %s" % (m.group(0) if m else "no summary", o2.strip().splitlines()[-1]))
    pages = {}
    for n in PAGES:
        rc, o = run(sys.executable, os.path.join(T, "sen0414_control_iter18_v1_3_0.py"), "page" + n)
        pages[n] = (rc == 0, o.strip().splitlines()[-1])
    return decks, pages


def main():
    src = W.newest(); t = open(src, encoding="utf-8").read(); g = rdflib.Graph(); g.parse(src, format="turtle")
    decks, pages = measure(); at = W.now(); RC = "RC2_Iter_18"; PC = "PC2_Iter_18"; assert ("ex:%s a backlog:SprintPlanningCeremony" % PC) in t
    mem = [str(x).split("#")[1] for x in g.objects(E.Iter_18, B.hasMember)]
    stories = [m for m in mem if m.startswith("ST_")]; closed = []; L = []
    for sid in sorted(stories):
        i, j = blk(t, sid); b = t[i:j]
        if "backlog:hasState backlog:Done" in b:
            continue
        tks = re.findall(r"ex:(TK_\w+)", re.search(r"backlog:decomposesInto ([^;.]*)[;.]", b).group(1))
        tb = {k: t[blk(t, k)[0]:blk(t, k)[1]] for k in tks}
        if not all("backlog:hasState backlog:Done" in v for v in tb.values()):
            continue
        fin = max(re.findall(r'finishedAt "([^"]*)"', "".join(tb.values()))); sts = re.findall(r'startedAt "([^"]*)"', "".join(tb.values()))
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b)
        if m:
            old, st = m.group(0), m.group(1)
        else:
            old = "backlog:hasState backlog:Ready"; assert old in b, sid; st = min(sts)
        assert st <= fin, sid
        ev = sorted({e for k in tks for e in re.findall(r"ex:(Ev2_\w+)", " ".join(re.findall(r"backlog:hasEvidence ([^;]*);", tb[k])))}); assert ev, sid
        t = t[:i] + b.replace(old, 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (st, fin, at), 1) + t[j:]
        note = "Story %s: every task is Done on bridge-verified evidence, recorded in the register versions named in the tasks' audit notes." % sid
        if not m:
            note += " The story never had its own T_Start (it was Ready while its task was controlled); its start is its first task's start, %s UTC." % st
        L.append('ex:Complete2R_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (
            sid, W.lit(sid + " completed at the review"), sid, at, W.lit("Done at the review ex:%s on %s UTC: every task of the story (%d) is Done; the last task finished %s UTC. %s" % (RC, at, len(tks), fin, note))))
        L.append('ex:Harness2R_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (sid, W.lit("Checks run for " + sid), sid, ", ".join("ex:" + e for e in ev)))
        L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (sid, ", ".join("ex:" + e for e in ev), W.lit("Closed %s UTC at the review ex:%s. %s" % (at, RC, note))))
        closed.append(sid)
    assert closed, "no story to close"
    left = [s for s in stories if s not in closed and "backlog:hasState backlog:Done" not in t[blk(t, s)[0]:blk(t, s)[1]]]; assert left
    L.append('ex:%s a backlog:SprintReviewCeremony ; rdfs:label %s@en ; backlog:ceremonyFor ex:Iter_18 ; backlog:reviewsCeremony ex:%s ;\n    backlog:closesStory %s ; backlog:heldAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s@en .\n' % (
        RC, W.lit("Review of iteration 18: the stories whose tasks are all Done"), PC, ", ".join("ex:" + s for s in closed), at,
        W.lit("Held %s UTC by the lineage agent, on the controlled work of the iteration: %s are closed, each with all its tasks Done on bridge-verified evidence. The iteration is NOT closed: %s are still open (the chapter 9 deck is being built, the chapter 6 and 9 pages follow); nothing is carried over by this review. The readings of the two objectives are the observations taken at this review." % (at, ", ".join(closed), ", ".join(left)))))
    nd = sum(1 for v in decks.values() if v[0]); np_ = sum(1 for v in pages.values() if v[0])
    obs = {"Obj2_StdDecks": ("Met2_StdDecks", nd, "Measured in this run (%s UTC): the deck standard check v1_0_0 and the deck overlap check v1_0_0 on the newest decks of chapters 6, 7 and 8: %s." % (at, "; ".join("chapter %s %s (%s)" % (n, "passes" if v[0] else "FAILS", v[1]) for n, v in decks.items()))),
           "Obj2_StdPages": ("Met2_StdPages", np_, "Measured in this run (%s UTC): the control checks page07 and page08 (sen0414_control_iter18_v1_3_0.py), which re-read the serial page-test runs 9.36.0 and 9.34.0 under the shared lock, the charset, comments and manifest equality of the newest pages: %s. The page of chapter 6 is not built yet, so it is not counted." % (at, "; ".join("chapter %s %s (%s)" % (n, "passes" if v[0] else "FAILS", v[1]) for n, v in pages.items())))}
    for o, (met, val, meth) in obs.items():
        L.append('ex:ObsR2_%s a backlog:MetricObservation ; rdfs:label "Reading at the review of iteration 18"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony ex:%s ;\n    backlog:hasObservationMethod %s .\n' % (o, met, o, val, at, RC, W.lit(meth)))
    for c in ("07", "08"):
        L.append('ex:AC2S_Page_Ch%s backlog:hasAuditNote %s .\n' % (c, W.lit("Tool versions actually used (controlled, register 2.170.0 and the control of this page): the page was built on the template 9.52.2 with the builder 4.18.1 and the page-data builder 2.25.0, read through the runner v1_1_0; the template 9.52.1 and the builder 4.18.0 named in this criterion's text produce a page with text above the header and are superseded by the repair (ex:CR2_Repair2). The criterion's elements were all measured on the page as built; recorded %s UTC at the review." % at)))
    for sid in RESCORE_OPEN:
        i, j = blk(t, sid); b = t[i:j]; m = re.search(r"backlog:hasPriorityScore ex:(Score7_%s)\b" % sid, b); assert m, sid
        k0 = t.index("\nex:Score7_%s a" % sid) + 1; r0 = t[k0:t.find("\nex:", k0 + 1)]
        q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0); assert q, sid
        bv, tc, rr, size = int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4)); val = (bv + tc + rr) / size
        t = t[:i] + b.replace(m.group(0), "backlog:hasPriorityScore ex:Score8_%s" % sid, 1) + t[j:]
        L.append('ex:Score8_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (sid, val, at, W.lit(
            "WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. RE-RUN on %s UTC after the review closed %s: the record ex:Score7_%s predates those completions. Inputs unchanged." % (bv, tc, rr, size, val, at, ", ".join(closed), sid))))
    out = W.write_new(src, t + "\n" + "".join(L), "Review ceremony of Iteration 18: the stories whose tasks are all Done are closed (%s); the readings of Obj2_StdDecks (%d) and Obj2_StdPages (%d) measured at the review; the iteration stays open; the open stories are re-scored." % (", ".join(closed), nd, np_))
    print(os.path.basename(out), "closed:", closed, "decks", nd, "pages", np_)


if __name__ == "__main__":
    main()
