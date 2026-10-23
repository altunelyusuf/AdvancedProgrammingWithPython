#!/usr/bin/env python3
"""sen0414_lineage_control v1_3_0 - records, in ONE new register version, that the lineage agent CONTROLLED executor results of Iter_18 of the second lineage (G136, G137, the evidence bridge).
  draft OUT.ttl                 the TestEvidence and ArtifactEvidence nodes before the bridge (no evidenceVerified); the TestEvidence command is 08-tooling/sen0414_control_iter18_v1_0_0.py CHECK
  record BRIDGE.ttl [TASK...]   the tasks whose evidence the bridge verified go Done (a task is held when any of its evidence was not verified or a dependency is not Done); finishedAt = the bridge's clock.
  note TASK TEXT                (record only) adds an audit note naming a measured result on a task that is NOT Done
v1.3.0 (over 1.2.0, which stays as committed): the tasks, check and files are those of the chapter 7 page (control script v1_2_0); the re-score relinks Score5_ to Score6_.
v1.2.0 (over 1.1.0, which stays as committed): the tasks, checks and files are those of the template repair, the runner repair and the regression (control script v1_1_0); the re-score relinks the open stories from Score5_ to Score5_, reading each input from the Score5_ rationale, with the three changed inputs named in OVERRIDE.
v1.1.0 (over 1.0.0, whose output the validator refused with 35 L2/L3 violations): a Done task also gets its TestHarness, lastAuditedAt, and a T_Complete transition when it had a T_Start; the open stories are RE-SCORED after the completions (a score older than the most recent completion is stale, BP-D11), the inputs re-read from the register state.
Verify tasks are the controller's; a Build task is Done only after the controller's own re-run of its criterion passed."""
__version__ = "1.3.0"
import hashlib, os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
B = rdflib.Namespace("http://example.org/backlog#"); EX = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
CTL = "08-tooling/sen0414_control_iter18_v1_2_0.py"
TASKS = {"TK_Std_Page_Ch07_Build": ("page07", "AC2S_Page_Ch07"), "TK_Std_Page_Ch07_Verify": ("page07", "AC2S_Page_Ch07")}
FILES = {"page07": ["03-materials/ch07/page/sen0414_ch07_page_v9_90_0.html", "03-materials/ch07/page/chapter_code_ch07_v1_0_0.json", "08-tooling/ch07-page/test_results_v9_90_0.json"]}
LABEL = {"page07": "the chapter 7 page v9_90_0: page test 9.36.0 (73 of 73 widgets, no failed feature, P1-P6, P8, P9, P11, P12 present) and 9.34.0 (no failure, widgets and features not below the existing page v9_28_0, skipped and gates not worse) re-run serially under the shared lock through runner v1_1_0; charset at byte 37; comments balanced; the chapter-code tab data equals the manifest (24 examples, order, names, code); chapter check Research/Ch07 PASS; the committed chapter check Page/Ch07 runs the page v9_28_0, so on the new page the same test is the 9.34.0 run; the chapter-code tab opened and run on screen at 1366 and 390 px"}
CHECKS = list(LABEL)
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
        L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s" .\n' % (eid(c), W.lit("Control by the lineage agent: " + LABEL[c]), cr, c, CTL, CTL, c))
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
                   % (eid(c), W.lit("Control by the lineage agent: " + LABEL[c]), cr, c, CTL, W.lit(v[2]), v[1]))
        for i, f in enumerate(FILES[c]):
            h = hashlib.sha256(open(os.path.join(W.REPO, f), "rb").read()).hexdigest(); x = fs[i]
            add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion %s ;\n    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                       % (fid(c, i), W.lit(os.path.basename(f) + " as controlled"), cr, f, h, W.lit(x[2]), x[1]))
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    ready = set()
    for k in (only or list(TASKS)):
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
            assert "backlog:hasState backlog:Proposed" in b, k
            nb = b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:hasEvidence %s' % (start_of(c, fin), fin, ev), 1)
        assert nb != b, k
        t = t[:i] + nb + t[j:]; ready.add(k); done.append(k)
        add.append('ex:%s backlog:lastAuditedAt "%s"^^xsd:dateTime .\n' % (k, fin))
        add.append('ex:Harness2_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:harnessComplete true ; backlog:hasHarnessEvidence ex:%s .\n' % (k, W.lit("Control checks for " + k), k, eid(c)))
        if "ex:Begin2T_%s a backlog:TransitionEvent" % k in t:
            add.append('ex:Complete2T_%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Complete ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, W.lit(k + " completed on the controller's verdict"), k, fin, W.lit("Done on the controller's own re-run, verified by the evidence bridge (ex:%s); the executor's report alone was not taken as the result." % eid(c))))
        add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Controlled by the lineage agent on %s UTC: %s. Evidence ex:%s, verified by backlog_evidence_bridge_v1_1_0." % (fin, LABEL[c], eid(c)))))
    if done:
        ts = max(vd[eid(TASKS[k][0])][1] for k in done); n2 = W.now(); assert n2 > ts
        for m0 in sorted(set(re.findall(r"\nex:Score5_(ST_\w+) a backlog:PriorityScore", t))):
            sid = m0; i = t.index("\nex:%s a backlog:Story" % sid) + 1; j = t.find("\nex:", i + 1); b = t[i:j]
            m = re.search(r"backlog:hasPriorityScore ex:(Score5_%s)\b" % sid, b)
            if not m:
                continue
            k0 = t.index("\nex:Score5_%s a" % sid) + 1; r0 = t[k0:t.find("\nex:", k0 + 1)]
            q = re.search(r"business value (\d+) \+ time criticality (\d+) \+ risk reduction (\d+)\) / job size ([\d.]+) h", r0); assert q, sid
            bv, tc, rr, size = int(q.group(1)), int(q.group(2)), int(q.group(3)), float(q.group(4)); why = "Inputs unchanged."
            if sid in OVERRIDE:
                rr, why = OVERRIDE[sid]
            nb = b.replace(m.group(0), "backlog:hasPriorityScore ex:Score6_%s" % sid, 1); t = t[:i] + nb + t[j:]
            val = (bv + tc + rr) / size
            add.append('ex:Score6_%s a backlog:PriorityScore ; backlog:scoredByMethod backlog:Method_WSJF ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (sid, val, n2, W.lit(
                "WSJF = (business value %d + time criticality %d + risk reduction %d) / job size %.1f h = %.2f. RE-RUN on %s UTC after the controller's completions (%s): the record ex:Score5_%s predates them (a score older than the latest completion is stale). %s" % (bv, tc, rr, size, val, n2, ", ".join(done), sid, why))))
    for k, txt in notes:
        add.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit(txt)))
    assert done or notes, "nothing to record"
    out = W.write_new(src, t + "\n" + "".join(add), "Control by the lineage agent, on bridge-verified evidence: Done %s%s%s." % (", ".join(done) or "none", ("; held: " + ", ".join(held)) if held else "", ("; findings noted on " + ", ".join(k for k, _ in notes)) if notes else ""))
    print(os.path.basename(out), "done:", done, "held:", held)


def start_of(c, fin):
    # the controller's own start: the clock reading of the first control run, given in env CTL_START (UTC, from the creation time of the controller's scratch folder).
    s = os.environ.get("CTL_START"); assert s and s < fin, "set CTL_START (UTC) to the clock reading of the first control run"
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
