#!/usr/bin/env python3
"""sen0414_lineage_work_begun_urgent v1_1_0 - records 'work begun' for the urgent repair task TK_U8_Deck_Check at the real instant the coordinator reports (a NEW file; one new register version).
Usage: sen0414_lineage_work_begun_urgent_v1_1_0.py ISO_UTC     e.g. 2026-10-30T05:13:09"""
__version__ = "1.1.0"
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
k = "TK_U8_Deck_Check"; s = "SEN0414-U8-deckcheck-ch08"; at = sys.argv[1]
assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d", at)
src = W.newest(); t = open(src, encoding="utf-8").read(); wrote = W.now(); assert at <= wrote
i = t.index("\nex:%s a backlog:" % k) + 1; j = t.find("\nex:", i + 1); b = t[i:j]
assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b
t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % at, 1) + t[j:]
bf = "08-tooling/briefs/urgent/r2/BRIEF_%s.md" % k; sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
L = ['\nex:EI8_%s a backlog:ExecutorInstance ; rdfs:label "Executor session %s"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ;\n    rdfs:comment "Started at the real instant the coordinator reported; retired when the session reports."@en .\n' % (k, s, W.lit("brief of register %s (sen0414_lineage_brief_urgent_v1_1_0), session %s" % (os.path.basename(src), s)), at),
     'ex:Brief8_%s a backlog:ExecutorBrief ; rdfs:label "Brief of %s"@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:AC2U_Deck_Ch08 ; backlog:briefedExecutorInstance ex:EI8_%s ;\n    rdfs:comment %s@en .\n' % (k, k, k, k, W.lit("Generated from register %s and passed unedited by the coordinator; file %s, SHA-256 %s." % (os.path.basename(src), bf, sha))),
     'ex:Begin8T_%s a backlog:TransitionEvent ; rdfs:label "%s started"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, k, k, at, W.lit("Work begun at %s UTC. Executor session %s, brief %s. Written at %s UTC after the real start, which the coordinator reported from the container clock. The lineage agent does not do this work." % (at, s, bf, wrote))),
     'ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Work begun %s UTC. Executor session %s." % (at, s)))]
print(os.path.basename(W.write_new(src, t + "\n" + "".join(L), "Work begun on the urgent repair task %s at %s UTC (executor session %s)." % (k, at, s))))
