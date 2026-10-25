#!/usr/bin/env python3
"""sen0414_lineage_work_begun v1_6_0 - records in ONE new register version that an executor session has really started on READY Build tasks of Iter_19 (the retrofit of chapters 1 to 5; v1_4_0 did the same for Iter_18) of the second lineage (ruling G113, G120, G136, G137):
each task goes Ready -> InProgress with startedAt = the clock (UTC) at the moment of writing, taken after the start gate (backlog_execution_ready) answered READY for the lineage and for the task;
a TransitionEvent (T_Start) is recorded for it whose note NAMES THE EXECUTOR SESSION (the names of the brief index), an ExecutorInstance for the session and the ExecutorBrief (generated from the register by
sen0414_lineage_brief_v1_0_0.py, file and SHA-256 recorded). The parent story goes InProgress with the first start, with its own TransitionEvent; the lineage status is LS_InProgress (G87).
Run it ONLY at the real start of the session: the clock is the evidence. Refuses a task whose dependencies are not all Done, a task not Ready, an iteration that has not started.
v1.6.0 (over 1.5.0, which stays as committed): the directory of the briefs can be given by the environment variable BRIEFS (the r2 briefs of the page builds are in 08-tooling/briefs/iter19/r2).
v1.5.0 (over 1.4.0): the tasks TK_Ret_ChNN_Deck_Build / Page_Build / Research of Iter_19 (chapters 01 to 05) with the sessions SEN0414-I19-...; the briefs are read from 08-tooling/briefs/iter19; the start time can be given by the environment variable NOW (the time reported by the coordinator, UTC, ISO), else the clock; the environment variable NOTE adds a disclosure to every note.
v1.4.0 (over 1.3.0): the session of TK_Std_ResearchCh06 is added.
v1.3.0 (over 1.2.0): the session of TK_Std_PageTest37 is added.
v1.1.0 (over 1.0.0): the sessions of the repair tasks TK_Std_Template_R2 and TK_Std_Runner are added.
Usage: sen0414_lineage_work_begun_v1_4_0.py TASK [TASK...]"""
__version__ = "1.6.0"
import hashlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
S = W.S
GATE = "/home/claude/altunelyusuf/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"
SESSIONS = {"TK_Ret_Ch%s_%s" % (c, k): "SEN0414-I19-%s-ch%s" % (v, c) for c in ("01", "02", "03", "04", "05") for k, v in (("Deck_Build", "deck"), ("Page_Build", "page"), ("Research", "research"))}
BRIEFS = os.environ.get("BRIEFS", "08-tooling/briefs/iter19")
NOTE = os.environ.get("NOTE", "")


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1
    j = t.find("\nex:", i)
    return i, (len(t) if j < 0 else j)


def deps_of(b):
    return re.findall(r"ex:(TK_\w+)", " ".join(re.findall(r"backlog:dependsOn ([^;]*);", b)))


def main():
    tasks = sys.argv[1:]; assert tasks, __doc__
    src = W.newest(); t = open(src, encoding="utf-8").read()
    for k in tasks:
        assert k in SESSIONS, k
        i, j = blk(t, k); b = t[i:j]
        assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b and "memberOfContainer ex:Iter_19" in b, k + " is not a Ready, unstarted task of Iter_19"
        for d in deps_of(b):
            di, dj = blk(t, d)
            assert "backlog:hasState backlog:Done" in t[di:dj], k + " has a dependency that is not Done: " + d
        bf = os.path.join(W.REPO, BRIEFS, "BRIEF_%s.md" % k)
        assert os.path.exists(bf), "no brief generated for " + k
    gate_file = src + ".gate.tmp"; open(gate_file, "w", encoding="utf-8").write(t)
    try:
        for k in tasks:
            r = subprocess.run([sys.executable, GATE, gate_file, "--lineage", "Lineage2", "--item", k], capture_output=True, text=True)
            assert "VERDICT     : READY" in r.stdout, k + " is not READY: " + r.stdout[-300:]
    finally:
        os.remove(gate_file)
    assert re.search(r'ex:Iter_19 a backlog:Iteration[^\n]*\n[^\n]*iterationStart "', t), "Iter_19 has no start"
    now = os.environ.get("NOW") or W.now(); L = []; parents = {}
    for k in tasks:
        i, j = blk(t, k); b = t[i:j]
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        s = SESSIONS[k]
        bf = os.path.join(BRIEFS, "BRIEF_%s.md" % k); sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
        par = next(x for x in re.findall(r"\nex:(ST_\w+) a backlog:Story", t) if re.search(r"decomposesInto[^;]*ex:%s\b" % k, t[blk(t, x)[0]:blk(t, x)[1]]))
        pi, pj = blk(t, par); ac = re.search(r"hasAcceptanceCriterion ex:(\w+)", t[pi:pj]).group(1)
        parents.setdefault(par, []).append(k)
        L.append('ex:Begin2T_%s a backlog:TransitionEvent ; rdfs:label "%s started by executor session %s"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n'
                 '    backlog:hasTransitionNote %s .\n' % (k, k, s, k, now, W.lit("Work begun at %s UTC inside the started sprint ex:Iter_19, after the start gate said READY. Executor session: %s, started with the brief generated from the register (%s). The lineage agent does not do this work. %s" % (now, s, bf, NOTE))))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Work begun %s UTC by the executor session %s (transition ex:Begin2T_%s). %s" % (now, s, k, NOTE))))
        L.append('ex:EI2_%s a backlog:ExecutorInstance ; rdfs:label "Executor session %s"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s@en .\n' % (
            k, s, W.lit("brief of register %s (sen0414_lineage_brief_retrofit_v1_0_0), session %s" % (os.path.basename(src), s)), now, W.lit("Started at the clock reading of the writer, taken when the coordinator reported the real start of the session; it is retired when the session reports.")))
        L.append('ex:Brief2_%s a backlog:ExecutorBrief ; rdfs:label "Brief of %s"@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI2_%s ;\n    rdfs:comment %s@en .\n' % (
            k, k, k, ac, k, W.lit("Generated from register %s by sen0414_lineage_brief_retrofit_v1_0_0.py and passed unedited by the coordinator; file %s, SHA-256 %s. %s" % (os.path.basename(src), bf, sha, NOTE))))
    for sid, ks in parents.items():
        i, j = blk(t, sid); b = t[i:j]
        if "backlog:hasState backlog:InProgress" in b:
            continue
        assert "backlog:hasState backlog:Ready" in b, sid
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        L.append('ex:Begin2T_%s a backlog:TransitionEvent ; rdfs:label "%s started with its first task"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n'
                 '    backlog:hasTransitionNote %s .\n' % (sid, sid, sid, now, W.lit("The story starts with the real start of its first task(s) %s at %s UTC." % (", ".join(ks), now))))
    t = S.set_status(t, "LS_InProgress")
    out = W.write_new(src, t + "\n" + "".join(L), "Work begun at %s UTC inside the started sprint Iter_19: %s; each start is a recorded T_Start naming its executor session, with its executor instance and brief; the stories and the lineage are InProgress." % (now, ", ".join(tasks)))
    print(now, os.path.basename(out))


if __name__ == "__main__":
    main()
