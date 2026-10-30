#!/usr/bin/env python3
"""sen0414_lineage_control_urgent v1_0_0 - records the lineage agent's control of the urgent Chapter 8 box on bridge-verified evidence, the Owner's later time box, the executor's deck-check result and the Chapter 7 repair item.
A NEW file; ONE new register file (newest + 1 minor) from `record`.
  draft OUT.ttl           the TestEvidence nodes (command: sen0414_control_urgent_v1_0_0.py CHECK) and the ArtifactEvidence nodes, no evidenceVerified (the bridge sets it)
  record BRIDGE.ttl       the Done records of the groups whose evidence the bridge verified; the others are held and named.   Environment: CTL_START_DECKCHECK (UTC, ISO) = real start of the control of the deck check.
Groups (a task or story is Done only when every group of its story is verified):
  deckcheck -> TK_U8_Deck_Check, TK_U8_Deck_Check_Verify        deck -> TK_U8_Deck_Build, TK_U8_Deck_Verify   (story ST_U8_Deck needs both)
  ctl91     -> TK_U8_Page_Ctl91                                  page -> TK_U8_Page_Build, TK_U8_Page_Verify    (story ST_U8_Page needs both)"""
import hashlib, os, re, sys, datetime
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#")
CTL = "08-tooling/sen0414_control_urgent_v1_0_0.py"
D = "03-materials/ch08/"
G = {"deckcheck": (["TK_U8_Deck_Check", "TK_U8_Deck_Check_Verify"], "AC2U_Deck_Ch08", ["08-tooling/sen0414_deck_standard_check_v1_1_0.py", "08-tooling/sen0414_deck_standard_check_fixtures_v1_1_0.py"],
                   "the new deck standard check v1_1_0: selftest 312 element checks and 0 mismatches, 13 of 13 elements PASS on the Chapter 8 deck v2.1.0, and the controller's mutation probes fail in the expected element"),
     "deck": (["TK_U8_Deck_Build", "TK_U8_Deck_Verify"], "AC2U_Deck_Ch08", [D + "SEN0414_Ch08_Strings_3e_v2_1_0.pptx", D + "page/chapter_code_ch08_v1_1_0.json"],
              "the Chapter 8 deck v2.1.0: the controller's own checks C1-C8 and the new deck standard check on the controller's re-runs"),
     "ctl91": (["TK_U8_Page_Ctl91"], "AC2U_Page_Ch08", [D + "page/sen0414_ch08_page_v9_91_0.html"],
               "the page v9_91_0: the controller's Playground width probe at 1366, 1400 and 390 px and the fifth run of page test 9.37.0"),
     "page": (["TK_U8_Page_Build", "TK_U8_Page_Verify"], "AC2U_Page_Ch08", [D + "page/sen0414_ch08_page_v9_92_1.html"],
              "the page v9_92_1: five direct runs of page test 9.37.0, page test 9.38.0, the leak probe seeds 1-5, the Playground width probe and the story-layout probe, each from a kept log of the controller's own run")}
STORY = {"ST_U8_Deck": ["deckcheck", "deck"], "ST_U8_Page": ["ctl91", "page"]}
eid = lambda c: "Ev8_Ctl_" + c
fid = lambda c, i: "Ev8_CtlFile_%s_%d" % (c, i)
OWNER_BOX = ("OWNER DECISION of 2026-10-30 about 08:15 Istanbul (relayed by the course coordinator, recorded as relayed): the time box of the urgent box moves to the start of his SEN0414 class, 14:00 Istanbul = 2026-10-30T11:00:00Z. "
             "The earlier time box (2026-10-30T03:00:00Z) is kept in the earlier versions of this register and in the note said openly there; the end of the box is now this later time, recorded as his decision with this reason.")
EXEC_NOTE = ("RESULT OF THE EXECUTOR SEN0414-U8-deckcheck-ch08 (real start 2026-10-30T05:13:09Z, report 05:18Z; commit d8bbb28, new files 08-tooling/sen0414_deck_standard_check_v1_1_0.py and sen0414_deck_standard_check_fixtures_v1_1_0.py), recorded as reported: "
             "selftest 312 element checks over 24 fixtures, 0 mismatches, exit 0; on the Chapter 8 deck v2.1.0 SUMMARY PASS=13 FAIL=0 NOT_MEASURED=0; on the Chapter 7 deck v2.0.0 FAIL in D3 (slides 5, 7, 24, 27), D5 and M1 (the deck still has the '>>>' prompts and WHO/WHAT labels). "
             "The executor disclosed that the D5 fact traces are mechanical and can be fooled (slide 21 'reason' matched 'since 3.6', slide 53 'who' matched 'In September') and that D3 sees that a result visual stands with the code, not that it is the output of that code.")
CTL_NOTE = ("CONTROL OF THE DECK CHECK (the lineage agent's own re-runs, 2026-10-30, logs in 08-tooling/control-u8-logs): the selftest re-run exits 0 with 312 element checks and 0 mismatches; the check re-run on the Chapter 8 deck v2.1.0 prints SUMMARY PASS=13 FAIL=0 NOT_MEASURED=0; "
            "the controller's own mutation probes on copies of the deck (the log control_deckcheck_mutations_run1.log): a story picture removed gives D5 FAIL, a 40-word prose box gives D2 FAIL, a 120-character code line gives D12 FAIL, one changed code character gives M1 FAIL (with the manifest given), as expected; "
            "the human read of the four story slides (21, 50, 53, 66) that the mechanical D5 cannot replace: each tells who, when, where, what and why and the means in sentences (slide 21 Eric V. Smith, PEP 498, 1 August 2015, peps.python.org, to keep text and values together, f-strings since 3.6; slide 50 nine companies, 19 February 1991, Mountain View, one table of numbers; "
            "slide 53 Ken Thompson and Rob Pike, September 1992, a New Jersey diner, one to four bytes and ASCII unchanged; slide 66 Larry Tesler with Tim Mott, 1973, Xerox PARC in Palo Alto, select-hold-insert). The check still cannot prove a result visual is that code's output; the render of all 72 slides read by the controller showed no overlap or unreadable text.")
CH07 = ("CHAPTER 7 DECK (found by the new check, recorded as a repair item and ranked behind the exams by the coordinator's instruction of 2026-10-30): the Chapter 7 deck v2.0.0 fails D3 (slides 5, 7, 24, 27), D5 and M1 under the new check because it still has the '>>>' prompts and WHO/WHAT labels; it needs a v2.1.0 rebuilt to the standard. "
        "Not begun, not scored; it joins the retrofit stories and is ranked after the exam path.")


def utc(x):
    return datetime.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S").astimezone().astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)
def sha(f):
    return hashlib.sha256(open(os.path.join(W.REPO, f), "rb").read()).hexdigest()
def draft(out):
    L = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    for c, (tasks, ac, files, what) in G.items():
        L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" .\n' % (eid(c), W.lit("Control by the lineage agent: " + what), ac, c, CTL, CTL, c))
        for i, f in enumerate(files):
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:attestsCriterion ex:%s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), ac, f, sha(f)))
    open(out, "w", encoding="utf-8").write("".join(L))
def record(bridge):
    g = rdflib.Graph(); g.parse(bridge, format="turtle"); vd = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        vd[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), utc(str(g.value(ev, B.verifiedAt))), str(g.value(ev, B.hasVerificationMethod)))
    src = W.newest(); t = open(src, encoding="utf-8").read(); n = W.now(); add = []; done = []; held = []
    ok = {c: bool(vd.get(eid(c)) and vd[eid(c)][0] and all(vd.get(fid(c, i)) and vd[fid(c, i)][0] for i in range(len(G[c][2])))) for c in G}
    # the Owner's later time box (functional property: the value is replaced in this new version)
    for u in ("Urgent_1", "Urgent_2"):
        i, j = blk(t, u); b = t[i:j]
        nb = re.sub(r'backlog:urgencyTimeBoxUntil "2026-10-30T03:00:00Z"\^\^<http://www.w3.org/2001/XMLSchema#dateTime>', 'backlog:urgencyTimeBoxUntil "2026-10-30T11:00:00Z"^^<http://www.w3.org/2001/XMLSchema#dateTime>', b, count=1)
        assert nb != b, u
        t = t[:i] + nb + t[j:]; add.append("ex:%s backlog:hasAuditNote %s .\n" % (u, W.lit(OWNER_BOX)))
    add.append("ex:Iter_U8 backlog:hasAuditNote %s .\n" % W.lit(OWNER_BOX))
    add.append("ex:AC2U_Deck_Ch08 backlog:hasAuditNote %s .\n" % W.lit(EXEC_NOTE))
    for k in ("TK_U8_Deck_Check", "TK_U8_Deck_Check_Verify", "ST_U8_Deck"):
        add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(EXEC_NOTE))); add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(CTL_NOTE)))
    # Chapter 7: a repair item, not begun
    add.append('\nex:ST_Ch07_DeckRebuild a backlog:Story ; rdfs:label "Rebuild the Chapter 7 deck to the standard (v2.1.0), found by the new deck check"@en ; backlog:hasIdentifier "ST_Ch07_DeckRebuild" ;\n    backlog:hasTitle "Rebuild the Chapter 7 deck to the standard (v2.1.0)" ;\n'
               '    backlog:belongsToLineage ex:Lineage2 ; backlog:responsible ex:Executor_ClaudeCodeSession ; backlog:admittedByOutput ex:Out2_BacklogR12 ;\n    backlog:hasInvestmentCategory backlog:Cat_Compliance ;\n'
               '    backlog:asRole "SEN0414 instructor" ; backlog:wantsCapability "the Chapter 7 deck without prompts and without label words, passing the deck standard check v1_1_0 in every element" ; backlog:soThat "Chapter 7 is taught from a deck that meets the same written standard as Chapter 8" ;\n'
               '    backlog:satisfiesDeliverable ex:Del2_StdDecks ; backlog:pursuesObjective ex:Obj2_StdDecks ; backlog:hasAcceptanceCriterion ex:AC2F_Retrofit ;\n    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ;\n'
               '    backlog:hasState backlog:Proposed ;\n    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked behind the exams by the coordinator\'s instruction of 2026-10-30; scored and decomposed into tasks when it is planned." ;\n    backlog:hasAuditNote %s .\n' % W.lit(CH07))
    ctl_s = os.path.getmtime(os.path.join(W.REPO, "08-tooling/control-u8-logs/control_deckcheck_selftest_run1.log"))
    ctl_start = datetime.datetime.fromtimestamp(ctl_s, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    for sid, groups in STORY.items():
        if not all(ok[c] for c in groups):
            held += [sid] + [k for c in groups for k in G[c][0]]; continue
        fin = max(vd[eid(c)][1] for c in groups)
        evs = []
        for c in groups: evs += [eid(c)] + [fid(c, i) for i in range(len(G[c][2]))]
        ev = ", ".join("ex:" + x for x in evs)
        for c in groups:
            add.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:%s ;\n    backlog:evidenceVerified true ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid(c), W.lit("Control by the lineage agent: " + G[c][3]), G[c][1], c, CTL, W.lit(vd[eid(c)][2]), CTL, c, vd[eid(c)][1]))
            for i, f in enumerate(G[c][2]):
                add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:%s ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), G[c][1], f, sha(f), W.lit(vd[fid(c, i)][2]), vd[fid(c, i)][1]))
        for c in groups:
            for k in G[c][0]:
                i, j = blk(t, k); b = t[i:j]
                if "backlog:hasState backlog:Ready" in b:
                    nb = b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (ctl_start, fin, ev), 1)
                    add.append('ex:Begin8C_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " started by the controller"), k, ctl_start, W.lit("The controller began its own re-run of the deck check at the instant of its first kept log.")))
                else:
                    nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:startedAt %s ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, ev), b, count=1)
                assert nb != b, k
                t = t[:i] + nb + t[j:]
                add.append('ex:%s backlog:lastAuditedAt "%s"^^xsd:dateTime .\n' % (k, fin))
                add.append('ex:Harness8_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence %s .\n' % (k, W.lit("Control checks for " + k), k, ", ".join("ex:" + eid(x) for x in groups)))
                add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on its own re-runs, verified by backlog_evidence_bridge_v1_1_0 at %s UTC; evidence %s." % (fin, ", ".join(evs)))))
                add.append('ex:Complete8C_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller's verdict"), k, fin, W.lit("Done on the controller's own re-runs, verified by the evidence bridge; the executor's report alone was not taken as the result.")))
                done.append(k)
        i, j = blk(t, sid); b = t[i:j]
        nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:startedAt %s ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, fin, ev), b, count=1)
        assert nb != b, sid
        t = t[:i] + nb + t[j:]; done.append(sid)
        add.append('ex:Complete8C_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (sid, W.lit(sid + " completed: its tasks are Done"), sid, fin, W.lit("All tasks of the story are Done on the controller's evidence.")))
    add.append("ex:Lineage2 backlog:hasAuditNote %s .\n" % W.lit("RANKING after the controller's verdicts (%s UTC): done now %s; held %s. The Chapter 7 deck rebuild (ST_Ch07_DeckRebuild) is a new repair item ranked behind the exam path; the exam lineage's box 2 (the midterm first) comes next once the interruptions are resolved and resumed." % (n, ", ".join(done) or "none", ", ".join(held) or "none")))
    out = W.write_new(src, t + "\n" + "".join(add), "Urgent Chapter 8 box: the Owner's later time box (11:00Z), the deck-check result and the controller's verdicts on bridge-verified evidence: Done %s%s; Chapter 7 deck rebuild recorded as a repair item." % (", ".join(done) or "none", ("; held: " + ", ".join(held)) if held else ""))
    print(os.path.basename(out), "done:", done, "held:", held)
if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2])
    else: record(sys.argv[2])
