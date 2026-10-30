#!/usr/bin/env python3
"""sen0414_lineage_work_begun_urgent v1_0_0 - records 'work begun' for the urgent Chapter 8 tasks at the REAL instants the coordinator reports (from date -u), as one new register file.
Each executor task (TK_U8_Deck_Build, TK_U8_Page_Build) goes Ready -> InProgress with startedAt = the given instant, a T_Start TransitionEvent that names its executor session, an ExecutorInstance and the ExecutorBrief
(file and SHA-256). The controller's own task (TK_U8_Page_Ctl91) is started by the lineage agent without a brief. The parent story goes InProgress with its first task.
If the record is written later than the real start, the note says so (the clock of writing is stated beside the real instant).
Usage: sen0414_lineage_work_begun_urgent_v1_0_0.py TASK=ISO_UTC [TASK=ISO_UTC ...]      e.g.  TK_U8_Deck_Build=2026-10-30T00:12:03"""
__version__ = "1.0.0"
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W

SESS = {"TK_U8_Deck_Build": "SEN0414-U8-deck-ch08", "TK_U8_Page_Build": "SEN0414-U8-page-ch08"}
STORY = {"TK_U8_Deck_Build": "ST_U8_Deck", "TK_U8_Page_Build": "ST_U8_Page", "TK_U8_Page_Ctl91": "ST_U8_Page"}
BRIEFS = "08-tooling/briefs/urgent/r1"


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)


def main():
    args = dict(a.split("=", 1) for a in sys.argv[1:]); assert args, __doc__
    src = W.newest(); t = open(src, encoding="utf-8").read(); wrote = W.now(); L = []; started_story = {}
    for k, at in sorted(args.items(), key=lambda kv: kv[1]):
        assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d", at), at
        assert at <= wrote, "a start instant in the future: " + at
        i, j = blk(t, k); b = t[i:j]; assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b, k + " is not a Ready, unstarted task"
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % at, 1) + t[j:]
        late = "" if wrote[:19] == at else " The record was written at %s UTC, after the real start; the real instant is the one given here, as reported by the coordinator from date -u." % wrote
        if k in SESS:
            s = SESS[k]; bf = "%s/BRIEF_%s.md" % (BRIEFS, k); sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
            note = "Work begun at %s UTC after the urgent interruption was recorded. Executor session: %s, started with the brief generated from the register (%s).%s The lineage agent does not do this work." % (at, s, bf, late)
            L.append('ex:EI8_%s a backlog:ExecutorInstance ; rdfs:label "Executor session %s"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s@en .\n' % (
                k, s, W.lit("brief of register %s (sen0414_lineage_brief_urgent_v1_0_0), session %s" % (os.path.basename(src), s)), at, W.lit("Started at the real instant the coordinator reported; retired when the session reports.")))
            L.append('ex:Brief8_%s a backlog:ExecutorBrief ; rdfs:label "Brief of %s"@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI8_%s ;\n    rdfs:comment %s@en .\n' % (
                k, k, k, "AC2U_Deck_Ch08" if "Deck" in k else "AC2U_Page_Ch08", k, W.lit("Generated from register %s by sen0414_lineage_brief_urgent_v1_0_0.py and passed unedited by the coordinator; file %s, SHA-256 %s." % (os.path.basename(src), bf, sha))))
        else:
            note = "Control work begun by the lineage agent at %s UTC (its own re-runs of the page v9_91_0; no executor, no brief).%s" % (at, late)
        L.append('ex:Begin8T_%s a backlog:TransitionEvent ; rdfs:label "%s started"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, k, k, at, W.lit(note)))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Work begun %s UTC. %s" % (at, ("Executor session " + SESS[k] + ".") if k in SESS else "Lineage agent's control."))))
        sid = STORY[k]
        if sid not in started_story:
            si, sj = blk(t, sid); sb = t[si:sj]
            if "backlog:hasState backlog:Ready" in sb:
                t = t[:si] + sb.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % at, 1) + t[sj:]
                L.append('ex:Begin8T_%s a backlog:TransitionEvent ; rdfs:label "%s started with its first task"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (sid, sid, sid, at, W.lit("The story starts with the real start of its first task %s at %s UTC." % (k, at))))
            started_story[sid] = k
    out = W.write_new(src, t + "\n" + "".join(L), "Work begun on the urgent Chapter 8 tasks %s, each as a recorded T_Start at the real instant the coordinator reported, with executor instance and brief where an executor does the work." % ", ".join("%s at %s UTC" % kv for kv in sorted(args.items())))
    print(os.path.basename(out))


if __name__ == "__main__":
    main()
