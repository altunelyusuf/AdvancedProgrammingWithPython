"""sen0414_lineage_outscope_backlog v1_0_0 - the Backlog stage of the second SEN0414 lineage: its output admits the work the first lineage out-scoped.
Also writes the evidence draft that backlog_evidence_bridge verifies, and merges the bridge's verdicts back as text (the bridge is the only
component that may assert evidenceVerified; nothing here sets it).

  evidence_draft(facts)            -> Turtle with one TestEvidence and one ArtifactEvidence per built file, for every story of chapters 7-12
  run(text, args, ...)             -> the Backlog stage: ARGS = PREV_COMMIT FACTS.json BRIDGE_OUT.ttl
A story becomes Done only when its TestEvidence and every ArtifactEvidence of it were verified by the bridge; any other story is admitted
unchanged, still Proposed, and the objective counts it as not done.
"""
__version__ = "1.0.0"
import json, os, re
import rdflib

B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace("http://example.org/sen0414-slides-lineage#")
CHECK = "08-tooling/sen0414_lineage_chapter_check_v1_0_0.py"
STORIES = ["ST_%s_Ch%02d" % (k, n) for n in range(7, 13) for k in ("Deck", "Research", "Page")]
OTHERS = ["ST_ReworkOthers_Ch01_02_04", "EP_Deck", "EP_Research", "EP_Page", "Init_Slides"]
KINDNAME = {"Deck": "deck", "Research": "research run", "Page": "page"}


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def ev_ids(sid, k):
    return "Ev2_%s" % sid[3:], ["Ev2_%s_File%d" % (sid[3:], i + 1) for i in range(k)]


def evidence_draft(facts):
    """Evidence nodes as they stand BEFORE the bridge: no evidenceVerified. One TestEvidence (the rerunnable chapter check) and one
    ArtifactEvidence per cited file (its path and SHA-256 as read from the file)."""
    L = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0414-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    for sid in STORIES:
        f = facts["stories"][sid]
        kind, ch = sid.split("_")[1], sid.split("_")[2]
        te, files = ev_ids(sid, len(f["artifacts"]))
        L.append('ex:%s a backlog:TestEvidence ; rdfs:label "Chapter check for %s %s"@en ; backlog:attestsCriterion ex:AC_Chapter ;\n'
                 '    backlog:hasTestId "%s/%s" ; backlog:hasTestSpec "%s" ;\n'
                 '    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 running %s %s/%s" .\n' % (te, kind, ch, kind, ch, CHECK, CHECK, kind, ch))
        for i, a in enumerate(f["artifacts"]):
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; backlog:attestsCriterion ex:AC_Chapter ;\n'
                     '    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n' % (files[i], os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], a["path"], a["sha256"]))
    return "".join(L)


def verdicts(bridge_ttl):
    g = rdflib.Graph(); g.parse(bridge_ttl, format="turtle")
    out = {}
    for ev in set(g.subjects(B.evidenceVerified, None)):
        out[str(ev).split("#")[-1]] = (bool(g.value(ev, B.evidenceVerified).toPython()), str(g.value(ev, B.verifiedAt)), str(g.value(ev, B.hasVerificationMethod)))
    return out


def story_block(t, sid):
    m = re.search(r"^ex:%s a backlog:Story.*?\n\n" % re.escape(sid), t, re.S | re.M)
    assert m, sid
    return m


def admit_block(blk, sid):
    n = blk.replace("backlog:admittedByOutput ex:Out_Backlog ;", "backlog:preLineageItem true ; backlog:admittedByOutput ex:Out2_Backlog ;", 1)
    assert n != blk, sid
    return n


def run(t, args, G, output, fill_previous, set_status):
    prev, facts_p, bridge_p = args[0], args[1], args[2]
    facts = json.load(open(facts_p)); vd = verdicts(bridge_p)
    t = fill_previous(t, "Objective", prev)
    t = set_status(t, "LS_Backlogged")
    done, kept = [], []
    add = []
    for sid in STORIES:
        f = facts["stories"][sid]
        te, files = ev_ids(sid, len(f["artifacts"]))
        ok = te in vd and vd[te][0] and all(x in vd and vd[x][0] for x in files)
        m = story_block(t, sid)
        blk = admit_block(m.group(0), sid)
        if ok:
            nb = blk.replace("backlog:hasState backlog:Proposed ;", "backlog:hasState backlog:Done ;", 1)
            nb = nb.replace('backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned." .',
                            'backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Admitted as finished: this story was never planned, so it is not scored." .', 1)
            assert nb.count("Done") >= 1 and "never planned" in nb, sid
            blk = nb
            done.append(sid)
            aud = vd[te][1]
            add.append('ex:%s backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ;\n    backlog:hasEvidence %s .\n'
                       % (sid, f["finished"], aud, ", ".join("ex:" + x for x in [te] + files)))
            kind = sid.split("_")[1]
            ch = sid.split("_")[2]
            add.append('ex:%s a backlog:TestHarness ; rdfs:label "Chapter check for %s %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence ex:%s .\n' % ("Harness2_" + sid[3:], kind, ch, sid, te))
            add.append('ex:%s a backlog:TestEvidence ; rdfs:label "Chapter check for %s %s"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter ;\n'
                       '    backlog:evidenceVerified true ; backlog:hasTestId "%s/%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                       % (te, kind, ch, kind, ch, CHECK, esc(vd[te][2]), "backlog_evidence_bridge_v1_1_0 with the course repository as workspace", vd[te][1]))
            for i, a in enumerate(f["artifacts"]):
                add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter ;\n'
                           '    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                           % (files[i], os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], a["path"], a["sha256"], esc(vd[files[i]][2]), vd[files[i]][1]))
        else:
            kept.append(sid)
        t = t.replace(m.group(0), blk)
    for oid in OTHERS:
        m = re.search(r"^ex:%s a backlog:[A-Za-z]+.*?\n\n" % re.escape(oid), t, re.S | re.M)
        if not m:
            m = re.search(r"^ex:%s a backlog:[A-Za-z]+.*?\n(?=ex:|\n)" % re.escape(oid), t, re.S | re.M)
        assert m, oid
        t = t.replace(m.group(0), admit_block(m.group(0), oid))
    t += "\n" + "".join(add)
    mov = {"Obj2_AdmittedDone": "Deck Research Page", "Obj2_EvidenceVerified": "Deck Research Page", "Obj2_DatesFromGit": "Deck Research Page"}
    for o in mov:
        t += "ex:%s backlog:metricMovableBy %s .\n" % (o, ", ".join("ex:" + s for s in STORIES))
    t += "ex:Obj2_NothingRebuilt backlog:metricMovableBy ex:ST_ReworkOthers_Ch01_02_04 .\n"
    json.dump({"done": done, "kept_open": kept}, open("/tmp/sen0414_backlog_outcome.json", "w"))
    return t + output(t, "Backlog", prev), "second lineage, Backlog stage closed: the first lineage's out-scoped work is admitted (%d stories recorded Done with verified evidence, %d admitted still open, the held rework, three epics and one initiative carried unchanged)." % (len(done), len(kept))
