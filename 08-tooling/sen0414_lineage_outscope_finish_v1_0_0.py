#!/usr/bin/env python3
"""sen0414_lineage_outscope_finish v1_0_0 - records, in a NEW version of the slides lineage register, that admitted stories of the second lineage
are Done, on the verdicts of backlog_evidence_bridge. Nothing is recorded Done unless the bridge verified its TestEvidence (the exit-0 chapter
check) and every ArtifactEvidence (path and SHA-256), and every story it depends on is Done in the register or in the same call.

  draft  FACTS.json OUT.ttl SID...          the evidence nodes before the bridge (no evidenceVerified), citing the chapter check 1_1_0
  record FACTS.json BRIDGE.ttl SID...       one new register version recording those stories Done
Finish points are git's (the last commit of the cited current files, a .docx rendering apart); start points are git's first commit of any version
of the story's files. A research run repaired into new file versions finishes when the repair finished.
"""
__version__ = "1.0.0"
import json, os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_outscope_v1_1_0 as M
import sen0414_lineage_outscope_backlog_v1_1_0 as bk

CHECK = "08-tooling/sen0414_lineage_chapter_check_v1_1_0.py"
B, EX = M.B, M.EX


def draft(facts_p, out, sids):
    bk.CHECK = CHECK; bk.STORIES = sids
    open(out, "w").write(bk.evidence_draft(json.load(open(facts_p))))


def record(facts_p, bridge_p, sids):
    facts = json.load(open(facts_p)); vd = bk.verdicts(bridge_p)
    src = M.newest(); t = open(src, encoding="utf-8").read()
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    ok = {}
    for sid in sids:
        te, files = bk.ev_ids(sid, len(facts["stories"][sid]["artifacts"]))
        ok[sid] = te in vd and vd[te][0] and all(x in vd and vd[x][0] for x in files)
    for sid in sids:
        for d in re.findall(r"backlog:dependsOn ex:(\w+)", bk.story_block(t, sid).group(0)):
            if not (d in ok and ok[d]) and (EX[d], B.hasState, B.Done) not in g:
                ok[sid] = False
    add, done, kept = [], [], []
    for sid in sids:
        if not ok[sid]:
            kept.append(sid); continue
        f = facts["stories"][sid]; te, files = bk.ev_ids(sid, len(f["artifacts"]))
        m = bk.story_block(t, sid); blk = m.group(0)
        nb = blk.replace("backlog:hasState backlog:Proposed ;", "backlog:hasState backlog:Done ;", 1)
        nb = nb.replace('backlog:hasScoreabilityReason "Scored when its own iteration is planned."', 'backlog:hasScoreabilityReason "Admitted as finished: this story was never planned, so it is not scored."', 1)
        assert nb != blk and "never planned" in nb, sid
        t = t.replace(blk, nb)
        kind, ch = sid.split("_")[1], sid.split("_")[2]
        aud = vd[te][1]
        add.append('ex:%s backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ;\n    backlog:hasEvidence %s .\n'
                   % (sid, f["started"], f["finished"], aud, ", ".join("ex:" + x for x in [te] + files)))
        add.append('ex:Harness2_%s a backlog:TestHarness ; rdfs:label "Chapter check for %s %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence ex:%s .\n' % (sid[3:], kind, ch, sid, te))
        add.append('ex:%s a backlog:TestEvidence ; rdfs:label "Chapter check for %s %s"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission ;\n'
                   '    backlog:evidenceVerified true ; backlog:hasTestId "%s/%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                   % (te, kind, ch, kind, ch, CHECK, bk.esc(vd[te][2]) + (" (the page test ran against a copy of the page carrying a TEST release key: it proves the page logic, not the instructor's real key)" if kind == "Page" else ""),
                      "backlog_evidence_bridge_v1_1_0 with the course repository as workspace", aud))
        for i, a in enumerate(f["artifacts"]):
            add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission ;\n'
                       '    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                       % (files[i], os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], a["path"], a["sha256"], bk.esc(vd[files[i]][2]), vd[files[i]][1]))
        done.append(sid)
    nxt, cur = M.next_version(src)
    out = M.write_new(src, t + "\n" + "".join(add), nxt, cur, "admitted stories recorded Done on bridge-verified evidence: %s%s." % (", ".join(done), ("; held open: " + ", ".join(kept)) if kept else ""))
    print(os.path.basename(out), "done:", done, "kept:", kept)


if __name__ == "__main__":
    if sys.argv[1] == "draft": draft(sys.argv[2], sys.argv[3], sys.argv[4:])
    else: record(sys.argv[2], sys.argv[3], sys.argv[4:])
