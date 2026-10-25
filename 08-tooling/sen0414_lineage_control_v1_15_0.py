#!/usr/bin/env python3
"""sen0414_lineage_control v1_15_0 (over v1_14_0, which stays as committed: the page control script is v1_4_0) (over v1_13_0, which stays as committed: the research control script is v1_1_0, which controls chapters 2 and 5) (over v1_12_0, which stays as committed: adds the research checks researchNN for TK_Ret_ChNN_Research and TK_Ret_ChNN_Research_Verify, control script sen0414_control_iter19_research_v1_1_0.py, and the Page_Verify task of a chapter, which REUSES the evidence of its page check already recorded) (over v1_11_0, which stays as committed: the page control script is v1_3_0) (over v1_10_0, which stays as committed: adds the page checks pageNN for TK_Ret_ChNN_Page_Build, control script sen0414_control_iter19_page_v1_4_0.py) (over v1_9_0, which stays as committed: adds the checks of the error-first deck repairs deckfix01, deckfix03, deckfix04 for TK_Ret_ChNN_Deck_Fix and deckfixall for TK_Ret_ErrFirst_Verify, control script sen0414_control_iter19_deckfix_v1_0_0.py; the control script is chosen per check) - records, in ONE new register version, that the lineage agent CONTROLLED executor results of Iter_18 of the second lineage (G136, G137, the evidence bridge).
  draft OUT.ttl                 the TestEvidence and ArtifactEvidence nodes before the bridge (no evidenceVerified); the TestEvidence command is 08-tooling/sen0414_control_iter18_v1_0_0.py CHECK
  record BRIDGE.ttl [TASK...]   the tasks whose evidence the bridge verified go Done (a task is held when any of its evidence was not verified or a dependency is not Done); finishedAt = the bridge's clock.
  note TASK TEXT                (record only) adds an audit note naming a measured result on a task that is NOT Done
v1.9.0 (over 1.8.0, which stays as committed and recorded the decks of chapters 1 to 3): the control script is sen0414_control_iter19_v1_1_0.py (story-picture assertion corrected); the start of a Verify task that was Ready is accepted (v1.8.0 already did).
v1.8.0 (over 1.7.0, which stays as committed): the controls of Iter_19: the decks of chapters 1 to 5 (control script sen0414_control_iter19_v1_0_0.py, checks deck01 .. deck05), the files and the label are read at run time (the label from 08-tooling/control-iter19-logs/label_CHECK.txt, written by the controller after viewing the result); the checks to record are given by the environment variable CHECKS; every open story is re-scored after the completions (Score N to N+1).
v1.5.0 (over 1.4.0, which stays as committed): the chapter 9 deck (control script v1_4_0); the re-score relinks Score8_ to Score9_.
v1.4.0 (over 1.3.0, which stays as committed): the chapter 8 page (control script v1_3_0); the re-score relinks Score8_ to Score7_.
v1.3.0 (over 1.2.0, which stays as committed): the tasks, check and files are those of the chapter 7 page (control script v1_2_0); the re-score relinks Score8_ to Score8_.
v1.2.0 (over 1.1.0, which stays as committed): the tasks, checks and files are those of the template repair, the runner repair and the regression (control script v1_1_0); the re-score relinks the open stories from Score8_ to Score8_, reading each input from the Score8_ rationale, with the three changed inputs named in OVERRIDE.
v1.1.0 (over 1.0.0, whose output the validator refused with 35 L2/L3 violations): a Done task also gets its TestHarness, lastAuditedAt, and a T_Complete transition when it had a T_Start; the open stories are RE-SCORED after the completions (a score older than the most recent completion is stale, BP-D11), the inputs re-read from the register state.
Verify tasks are the controller's; a Build task is Done only after the controller's own re-run of its criterion passed."""
__version__ = "1.15.0"
import hashlib, os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#"); EX = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
CTL = "08-tooling/sen0414_control_iter19_v1_1_0.py"
CTLX = "08-tooling/sen0414_control_iter19_deckfix_v1_0_0.py"


CTLP = "08-tooling/sen0414_control_iter19_page_v1_4_0.py"


CTLR = "08-tooling/sen0414_control_iter19_research_v1_1_0.py"
REUSE = {"TK_Ret_Ch%s_Page_Verify" % n: ("page" + n, "research" + n) for n in ("01", "02", "03", "04", "05")}      # task: (check whose evidence is already in the register, the check that releases it)


def ctl(c):
    return CTLX if c.startswith("deckfix") else CTLP if c.startswith("page") else CTLR if c.startswith("research") else CTL

LOGD = os.path.join(W.REPO, "08-tooling", "control-iter19-logs")
CHECKS = [c for c in os.environ.get("CHECKS", "").split(",") if c]
TASKS = {}
for _n in ("01", "02", "03", "04", "05"):
    for _k in ("Deck_Build", "Deck_Verify"):
        if "deck" + _n in CHECKS:
            TASKS["TK_Ret_Ch%s_%s" % (_n, _k)] = ("deck" + _n, "AC2F_Retrofit")
    if "deckfix" + _n in CHECKS:
        TASKS["TK_Ret_Ch%s_Deck_Fix" % _n] = ("deckfix" + _n, "AC2R_ErrFirst")
for _n in ("01", "02", "03", "04", "05"):
    if "page" + _n in CHECKS:
        TASKS["TK_Ret_Ch%s_Page_Build" % _n] = ("page" + _n, "AC2F_Retrofit")
for _n in ("01", "02", "03", "04", "05"):
    if "research" + _n in CHECKS:
        TASKS["TK_Ret_Ch%s_Research" % _n] = ("research" + _n, "AC2F_RetrofitResearch"); TASKS["TK_Ret_Ch%s_Research_Verify" % _n] = ("research" + _n, "AC2F_RetrofitResearch")
if "deckfixall" in CHECKS:
    TASKS["TK_Ret_ErrFirst_Verify"] = ("deckfixall", "AC2R_ErrFirst")


def newest(pat):
    import glob
    key = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.[a-z]+$", p).groups()]
    return os.path.relpath(sorted(glob.glob(os.path.join(W.REPO, pat)), key=key)[-1], W.REPO)


FILES = {"deck" + n: [newest("03-materials/ch%s/SEN0414_Ch%s_*.pptx" % (n, n)), newest("03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (n, n))] for n in ("01", "02", "03", "04", "05") if "deck" + n in CHECKS}
FILES.update({"deckfix" + n: [newest("03-materials/ch%s/SEN0414_Ch%s_*.pptx" % (n, n)), newest("03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (n, n))] for n in ("01", "03", "04") if "deckfix" + n in CHECKS})
FILES.update({"page" + n: [newest("03-materials/ch%s/page/sen0414_ch%s_page_v9_9*.html" % (n, n)), newest("03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (n, n))] for n in ("01", "02", "03", "04", "05") if "page" + n in CHECKS})
FILES.update({"research" + n: [newest("03-materials/ch%s/rdodi/sen0414_ch%s_research_v*.ttl" % (n, n)), newest("03-materials/ch%s/page/sen0414_ch%s_page_abox_v*.ttl" % (n, n))] for n in ("01", "02", "03", "04", "05") if "research" + n in CHECKS})
FILES["deckfixall"] = [newest("03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (n, n)) for n in ("01", "03", "04")] if "deckfixall" in CHECKS else []
LABEL = {c: open(os.path.join(LOGD, "label_%s.txt" % c), encoding="utf-8").read().strip() for c in CHECKS}
OVERRIDE = {}


def eid(c):
    return "Ev2_Ctl_" + c


def fid(c, i):
    return "Ev2_CtlFile_%s_%d" % (c, i)


def draft(out):
    L = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    crit = {}
    for k, (c, a) in TASKS.items():
        crit.setdefault(c, []).append(a)
    for c in CHECKS:
        cr = ", ".join("ex:" + a for a in sorted(set(crit[c])))
        L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" .\n' % (eid(c), W.lit("Control by the lineage agent: " + LABEL[c]), cr, c, ctl(c), ctl(c), c))
        for i, f in enumerate(FILES[c]):
            h = hashlib.sha256(open(os.path.join(W.REPO, f), "rb").read()).hexdigest()
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:attestsCriterion %s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n' % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), cr, f, h))
    open(out, "w", encoding="utf-8").write("".join(L))


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i)
    return i, (len(t) if j < 0 else j)


def utc(x):
    # the bridge writes the machine's LOCAL clock without a zone; the register's times are UTC (v1.1.0 converts: the earlier tools of this line copied the local reading)
    import datetime
    return datetime.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S").astimezone().astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def verdicts(p):
    g = rdflib.Graph(); g.parse(p, format="turtle"); o = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        o[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), utc(str(g.value(ev, B.verifiedAt))), str(g.value(ev, B.hasVerificationMethod)))
    return o


def record(bridge, only, notes):
    vd = verdicts(bridge); src = W.newest(); t = open(src, encoding="utf-8").read(); add = []; done = []; held = []
    crit = {}
    for k, (c, a) in TASKS.items():
        crit.setdefault(c, []).append(a)
    for c in CHECKS:
        v = vd.get(eid(c)); fs = [vd.get(fid(c, i)) for i in range(len(FILES[c]))]
        good = bool(v and v[0] and all(x and x[0] for x in fs))
        if not good:
            continue
        cr = ", ".join("ex:" + a for a in sorted(set(crit[c])))
        add.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion %s ;\n    backlog:evidenceVerified true ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                   % (eid(c), W.lit("Control by the lineage agent: " + LABEL[c]), cr, c, ctl(c), W.lit(v[2]), v[1]))
        for i, f in enumerate(FILES[c]):
            h = hashlib.sha256(open(os.path.join(W.REPO, f), "rb").read()).hexdigest(); x = fs[i]
            add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion %s ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                       % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), cr, f, h, W.lit(x[2]), x[1]))
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    ready = set()
    for k in (only or list(TASKS)):
        if k in REUSE:
            pc, rc_ = REUSE[k]; assert (EX[eid(pc)], B.hasState, None) or True
            i, j = blk(t, k); b = t[i:j]
            deps = re.findall(r"ex:(TK_\w+)", " ".join(re.findall(r"backlog:dependsOn ([^;]*);", b)))
            if any(d not in ready and (EX[d], B.hasState, B.Done) not in g for d in deps) or "ex:" + eid(pc) not in t:
                held.append(k); continue
            import time; time.sleep(2); st_ = vd[eid(rc_)][1]; fin = W.now(); assert fin > st_; ev = ", ".join("ex:" + x for x in [eid(pc)] + [fid(pc, n) for n in range(2)])
            st0 = "backlog:hasState backlog:Ready" if "backlog:hasState backlog:Ready" in b else "backlog:hasState backlog:Proposed"; assert st0 in b, k
            nb = b.replace(st0, 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (st_, fin, ev), 1)
            t = t[:i] + nb + t[j:]; ready.add(k); done.append(k)
            add.append('ex:%s backlog:lastAuditedAt "%s"^^xsd:dateTime .\n' % (k, fin))
            add.append('ex:Harness2_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:%s .\n' % (k, W.lit("Control checks for " + k), k, eid(pc)))
            add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on %s UTC: the page of the chapter measured against the page standard by the controller\'s own serial runs, recorded in the evidence ex:%s (the page check of the page-build task), released now that the research set of the chapter is controlled (ex:%s)." % (fin, eid(pc), eid(rc_)))))
            continue
        c, a = TASKS[k]
        if eid(c) not in {x.split("#")[-1] for x in vd if vd[x][0]} or not (vd.get(eid(c)) and vd[eid(c)][0] and all(vd.get(fid(c, i)) and vd[fid(c, i)][0] for i in range(len(FILES[c])))):
            held.append(k); continue
        i, j = blk(t, k); b = t[i:j]
        deps = re.findall(r"ex:(TK_\w+)", " ".join(re.findall(r"backlog:dependsOn ([^;]*);", b)))
        if any(d not in ready and (EX[d], B.hasState, B.Done) not in g for d in deps):
            held.append(k); continue
        fin = vd[eid(c)][1]; ev = ", ".join("ex:" + x for x in [eid(c)] + [fid(c, n) for n in range(len(FILES[c]))])
        if "backlog:hasState backlog:InProgress ; backlog:startedAt" in b:
            nb = re.sub(r'backlog:hasState backlog:InProgress ; backlog:startedAt ("[^"]*"\^\^xsd:dateTime)', lambda m: 'backlog:hasState backlog:Done ; backlog:startedAt %s ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (m.group(1), fin, ev), b, count=1)
        else:
            st0 = "backlog:hasState backlog:Ready" if "backlog:hasState backlog:Ready" in b else "backlog:hasState backlog:Proposed"
            assert st0 in b, k
            nb = b.replace(st0, 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (start_of(c, fin), fin, ev), 1)
        assert nb != b, k
        t = t[:i] + nb + t[j:]; ready.add(k); done.append(k)
        add.append('ex:%s backlog:lastAuditedAt "%s"^^xsd:dateTime .\n' % (k, fin))
        add.append('ex:Harness2_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:%s .\n' % (k, W.lit("Control checks for " + k), k, eid(c)))
        if "ex:Begin2T_%s a backlog:TransitionEvent" % k in t:
            add.append('ex:Complete2T_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller's verdict"), k, fin, W.lit("Done on the controller's own re-run, verified by the evidence bridge (ex:%s); the executor's report alone was not taken as the result." % eid(c))))
        add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on %s UTC: %s. Evidence ex:%s, verified by backlog_evidence_bridge_v1_1_0." % (fin, LABEL[c], eid(c)))))
    if done:
        ts = max([vd[eid(TASKS[k][0])][1] for k in done if k in TASKS] or ["0"]); n2 = W.now(); assert n2 > ts
        for sid in sorted(set(re.findall(r"\nex:(ST_\w+) a backlog:Story", t))):
            i = t.index("\nex:%s a backlog:Story" % sid) + 1; j = t.find("\nex:", i + 1); b = t[i:j]
            m = re.search(r"backlog:hasPriorityScore ex:Score(\d+)_%s\b" % sid, b)
            if not m or "backlog:hasState backlog:Done" in b:
                continue
            kk = int(m.group(1)); k0 = t.index("\nex:Score%d_%s a" % (kk, sid)) + 1; r0 = t[k0:t.find("\nex:", k0 + 1)]
            q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0); assert q, sid
            bv, tc, rr, size = int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4)); why = "Inputs unchanged."
            if sid in OVERRIDE:
                rr, why = OVERRIDE[sid]
            nb = b.replace(m.group(0), "backlog:hasPriorityScore ex:Score%d_%s" % (kk + 1, sid), 1); t = t[:i] + nb + t[j:]
            val = (bv + tc + rr) / size
            add.append('ex:Score%d_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (kk + 1, sid, val, n2, W.lit(
                "WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. RE-RUN on %s UTC after the controller's completions (%s): the record ex:Score%d_%s predates them (a score older than the latest completion is stale). %s" % (bv, tc, rr, size, val, n2, ", ".join(done), kk, sid, why))))
    for k, txt in notes:
        add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit(txt)))
    assert done or notes, "nothing to record"
    out = W.write_new(src, t + "\n" + "".join(add), "Control by the lineage agent, on bridge-verified evidence: Done %s%s%s." % (", ".join(done) or "none", ("; held: " + ", ".join(held)) if held else "", ("; findings noted on " + ", ".join(k for k, _ in notes)) if notes else ""))
    print(os.path.basename(out), "done:", done, "held:", held)


def start_of(c, fin):
    # the controller's own start: the clock reading of the first control run, given in env CTL_START (UTC, from the creation time of the controller's scratch folder).
    s = os.environ.get("CTL_START_" + c) or os.environ.get("CTL_START"); assert s and s < fin, "set CTL_START (UTC) to the clock reading of the first control run"
    return s


def main():
    if sys.argv[1] == "draft":
        draft(sys.argv[2]); return
    a = sys.argv[3:]; notes = []; only = []
    i = 0
    while i < len(a):
        if a[i] == "note":
            notes.append((a[i + 1], a[i + 2])); i += 3
        else:
            only.append(a[i]); i += 1
    record(sys.argv[2], only, notes)


if __name__ == "__main__":
    main()
