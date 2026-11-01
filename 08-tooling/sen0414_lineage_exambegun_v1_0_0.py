#!/usr/bin/env python3
"""sen0414_lineage_exambegun v1_0_0 - records 'work begun' for exam-lineage tasks at the real instants the coordinator gives (date -u), after the start gate says READY. Same method as the begun step of sen0414_lineage_midterm_v1_0_0.py.
Usage: sen0414_lineage_exambegun_v1_0_0.py TK4_Cover=15:40:01 TK4_Design2=15:40:02 ...   (UTC times of 2026-11-01)"""
__version__ = "1.0.0"
import hashlib, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
lit = W.lit
GATE = "/home/claude/altunelyusuf/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py"
STORY = {"TK4_Design2": "ST4_DesignRev2", "TK4_ItemRules2": "ST4_DesignRev2", "TK4_Cover": "ST4_Cover", "TK4_Engine5": "ST4_Engine5", "TK4_Items_A2": "ST4_Items2", "TK4_Items_B2": "ST4_Items2", "TK4_Papers": "ST4_Papers"}
SESS = {"TK4_Design2": "SEN0414-EX-design2", "TK4_ItemRules2": "SEN0414-EX-itemrules2", "TK4_Cover": "SEN0414-EX-cover", "TK4_Engine5": "SEN0414-EX-engine5", "TK4_Items_A2": "SEN0414-EX-items-a2", "TK4_Items_B2": "SEN0414-EX-items-b2", "TK4_Papers": "SEN0414-EX-papers"}
BR = "08-tooling/briefs/exam/r10"
src = W.newest(); t = open(src, encoding="utf-8").read(); L = []; started = set()
def blk(name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1); return i, (len(t) if j < 0 else j)
args = [a.split("=") for a in sys.argv[1:]]; assert args, __doc__
gf = src + ".gate.tmp"; open(gf, "w", encoding="utf-8").write(t)
try:
    for k, hh in args:
        r = subprocess.run([sys.executable, GATE, gf, "--lineage", "Lineage4", "--item", k], capture_output=True, text=True)
        assert "VERDICT     : READY" in r.stdout, k + ": " + r.stdout[-400:]
finally:
    os.remove(gf)
for k, hh in args:
    at = "2026-11-01T" + hh; s = SESS[k]; sid = STORY[k]
    i, j = blk(k); b = t[i:j]; assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b, k
    t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % at, 1) + t[j:]
    if sid not in started:
        i, j = blk(sid); b = t[i:j]
        if "backlog:hasState backlog:Ready" in b:
            t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % at, 1) + t[j:]
            L.append(f'ex:Begin4e_{sid} a backlog:TransitionEvent ; rdfs:label "{sid} started with its first task"@en ; backlog:transitionedItem ex:{sid} ; backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "{at}"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote "The story starts with the real start of its first task {k} at {at} UTC." .\n')
        started.add(sid)
    bf = "%s/BRIEF_%s.md" % (BR, k); sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
    L.append(f'ex:EI_4e_{k} a backlog:ExecutorInstance ; rdfs:label "Executor session {s}"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion {lit("brief %s (sen0414_lineage_brief_exam5_v1_2_0), session %s" % (bf, s))} ; backlog:instantiatedAt "{at}"^^xsd:dateTime ;\n    rdfs:comment "Started at the real instant the coordinator gave (date -u); retired when the session reports."@en .\n')
    L.append(f'ex:Brief_4e_{k} a backlog:ExecutorBrief ; rdfs:label "Brief of {k}"@en ; backlog:briefFor ex:{k} ; backlog:briefCriterion ex:AC4_Controlled ; backlog:briefedExecutorInstance ex:EI_4e_{k} ;\n    rdfs:comment {lit("Passed unedited by the coordinator; file %s, SHA-256 %s." % (bf, sha))}@en .\n')
    L.append(f'ex:Begin4e_{k} a backlog:TransitionEvent ; rdfs:label "{k} started by executor session {s}"@en ; backlog:transitionedItem ex:{k} ; backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "{at}"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote {lit("Work begun at %s UTC after the start gate said READY; the task is an urgent item of Urgent_4. Executor session %s, brief %s. The record was written after the real start; the real instant is the one the coordinator gave from date -u. The lineage agent does not do this work." % (at, s, bf))} .\n')
    L.append(f'ex:{k} backlog:hasAuditNote "Work begun {at} UTC by executor session {s}." .\n')
print(os.path.basename(W.write_new(src, t + "\n" + "".join(L), "Work begun on " + ", ".join(k for k, _ in args) + " (exam executors, real starts from the coordinator); stories InProgress.")))
