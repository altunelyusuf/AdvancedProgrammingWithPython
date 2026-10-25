#!/usr/bin/env python3
"""sen0414_lineage_session2 v1_1_0 - records in ONE new register version that a LATER executor session has really started on a task that is already InProgress (an earlier session stopped or reported;
a T_Start cannot be repeated, so the task keeps its state and its first start): an ExecutorInstance for the new session at the real start (UTC), the ExecutorBrief of the new brief (file and SHA-256), and an audit note on the task.
v1.1.0 (over 1.0.0): the ordinal and the suffix of the session are arguments, and the environment NOW (UTC, from the coordinator's report of the real start) names the start when the writer runs within minutes of the report.
Run it ONLY at the real start of the session (ruling G113, G120, G136, G137).
Usage: sen0414_lineage_session2_v1_1_0.py TASK SESSION BRIEF_RELATIVE_PATH CHANGE_REQUEST ORD SUF      (ORD: second|third; SUF: S2|S3)"""
__version__ = "1.1.0"
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W


def main():
    k, sess, bf, cr, ordn, suf = sys.argv[1:7]
    src = W.newest(); t = open(src, encoding="utf-8").read()
    i = t.index("\nex:%s a backlog:" % k) + 1; j = t.find("\nex:", i + 1); b = t[i:j]
    assert "backlog:hasState backlog:InProgress" in b, k + " is not InProgress"
    sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
    ac = re.findall(r"hasAcceptanceCriterion ex:(\w+)", t[:t.index("decomposesInto ex:%s" % k)])[-1]
    now = os.environ.get("NOW") or W.now(); ei = "EI2_%s_%s" % (k, suf); br = "Brief2_%s_%s" % (k, suf)
    L = ['\nex:%s a backlog:ExecutorInstance ; rdfs:label "Executor session %s (%s session on %s)"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s@en .\n' % (
            ei, sess, ordn, k, W.lit("brief of register %s (the brief file named below), session %s" % (os.path.basename(src), sess)), now,
            W.lit("Started at the real start reported by the coordinator. Earlier sessions on this task stopped or reported; the task keeps its first start."))]
    L.append('ex:%s a backlog:ExecutorBrief ; rdfs:label "Brief of %s for the %s session"@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:%s ;\n    rdfs:comment %s@en .\n' % (
        br, k, ordn, k, ac, ei, W.lit("Generated from register %s and passed unedited by the coordinator; file %s, SHA-256 %s. Earlier briefs stay as history." % (os.path.basename(src), bf, sha))))
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("The %s executor session %s started at %s UTC on this task, which stays InProgress with its first start (a start is not repeated); the task was widened by ex:%s. ExecutorInstance ex:%s, brief file %s, SHA-256 %s." % (ordn, sess, now, cr, ei, bf, sha))))
    out = W.write_new(src, t + "\n" + "".join(L), "The %s executor session %s started on %s at %s UTC (the task stays InProgress): executor instance, brief with SHA-256, audit note." % (ordn, sess, k, now))
    print(now, os.path.basename(out))


if __name__ == "__main__":
    main()
