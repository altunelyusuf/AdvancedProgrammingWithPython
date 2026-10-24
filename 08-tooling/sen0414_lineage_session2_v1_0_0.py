#!/usr/bin/env python3
"""sen0414_lineage_session2 v1_0_0 - records in ONE new register version that a SECOND executor session has really started on a task that is already InProgress (the first session stopped without changes by its stop condition;
a T_Start cannot be repeated, so the task keeps its state and its first start): an ExecutorInstance for the new session at the clock reading of the writer (UTC), the ExecutorBrief of the new brief (file and SHA-256), and an audit note on the task.
Run it ONLY at the real start of the session (ruling G113, G120, G136, G137). Usage: sen0414_lineage_session2_v1_0_0.py TASK SESSION BRIEF_RELATIVE_PATH CHANGE_REQUEST"""
__version__ = "1.0.0"
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W


def main():
    k, sess, bf, cr = sys.argv[1:5]
    src = W.newest(); t = open(src, encoding="utf-8").read()
    i = t.index("\nex:%s a backlog:" % k) + 1; j = t.find("\nex:", i + 1); b = t[i:j]
    assert "backlog:hasState backlog:InProgress" in b, k + " is not InProgress"
    sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
    m = re.search(r"hasAcceptanceCriterion ex:(\w+)", t[t.index("decomposesInto ex:%s" % k) - 3000:t.index("decomposesInto ex:%s" % k) + 200][::1]) 
    ac = re.findall(r"hasAcceptanceCriterion ex:(\w+)", t[:t.index("decomposesInto ex:%s" % k)])[-1]
    now = W.now()
    L = ['\nex:EI2_%s_S2 a backlog:ExecutorInstance ; rdfs:label "Executor session %s (second session on %s)"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s@en .\n' % (
            k, sess, k, W.lit("brief of register %s (sen0414_lineage_brief_v1_6_0), session %s" % (os.path.basename(src), sess)), now,
            W.lit("Started at the clock reading of the writer, taken when the coordinator reported the real start of the session. The first session on the task stopped without changes by its stop condition."))]
    L.append('ex:Brief2_%s_S2 a backlog:ExecutorBrief ; rdfs:label "Brief of %s for the second session"@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI2_%s_S2 ;\n    rdfs:comment %s@en .\n' % (
        k, k, k, ac, k, W.lit("Generated from register %s by sen0414_lineage_brief_v1_6_0.py and passed unedited by the coordinator; file %s, SHA-256 %s. The first brief (file 08-tooling/briefs/iter18/BRIEF_%s.md) stays as history." % (os.path.basename(src), bf, sha, k))))
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Second executor session %s started at %s UTC on this task, which stays InProgress with its first start (a start is not repeated): the first session stopped without changes by its stop condition and reported the cause; the task was widened by ex:%s. ExecutorInstance ex:EI2_%s_S2, brief SHA-256 %s." % (sess, now, cr, k, sha))))
    out = W.write_new(src, t + "\n" + "".join(L), "Second executor session %s started on %s at %s UTC (the task stays InProgress; its first session stopped without changes): executor instance, brief with SHA-256, audit note." % (sess, k, now))
    print(now, os.path.basename(out))


if __name__ == "__main__":
    main()
