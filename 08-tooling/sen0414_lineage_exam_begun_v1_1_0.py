#!/usr/bin/env python3
"""sen0414_lineage_exam_begun v1_1_0 - records the real start of exam-lineage tasks (ex:Lineage4): each task goes Ready -> InProgress with startedAt = the instant the coordinator gave (env NOW, UTC, no zone suffix),
after the start gate (backlog_execution_ready) answered READY for the lineage and the task. A TransitionEvent (T_Start) naming the executor session, its executor instance and its brief (SHA-256 of the file) are recorded;
the parent story goes InProgress with the first start; the lineage status is LS_InProgress. A NEW file over sen0414_lineage_exam_begun_v1_0_0.py (which serves box 1): box 2 (Iter_Ex2) and the briefs of sen0414_lineage_brief_exam_v1_3_0 (r4).
Usage: NOW=2026-10-29T20:30:00 BRIEFS=08-tooling/briefs/exam/r1 sen0414_lineage_exam_begun_v1_0_0.py TASK [TASK ...]"""
__version__ = "1.1.0"
import hashlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
import sen0414_lineage_exam_v1_0_0 as X
import sen0414_lineage_brief_exam_v1_3_0 as BR
GATE = "/home/claude/altunelyusuf/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py"
BRIEFS = os.environ.get("BRIEFS", "08-tooling/briefs/exam/r4"); NOTE = os.environ.get("NOTE", "")


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1
    j = t.find("\nex:", i)
    return i, (len(t) if j < 0 else j)


def main():
    tasks = sys.argv[1:]; assert tasks, __doc__
    src = W.newest(); t = open(src, encoding="utf-8").read()
    for k in tasks:
        assert k in BR.SESS, k
        i, j = blk(t, k); b = t[i:j]
        assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b and "memberOfContainer ex:Iter_Ex2" in b, k + " is not a Ready, unstarted task of Iter_Ex2"
        for d in re.findall(r"ex:(TK4_\w+)", " ".join(re.findall(r"backlog:dependsOn ([^;]*);", b))):
            di, dj = blk(t, d)
            assert "backlog:hasState backlog:Done" in t[di:dj], k + " has a dependency that is not Done: " + d
        assert os.path.exists(os.path.join(W.REPO, BRIEFS, "BRIEF_%s.md" % k)), "no brief generated for " + k
    gf = src + ".gate.tmp"; open(gf, "w", encoding="utf-8").write(t)
    try:
        for k in tasks:
            r = subprocess.run([sys.executable, GATE, gf, "--lineage", "Lineage4", "--item", k], capture_output=True, text=True)
            assert "VERDICT     : READY" in r.stdout, k + " is not READY: " + r.stdout[-300:]
    finally:
        os.remove(gf)
    now = os.environ.get("NOW") or W.now(); L = []; parents = {}
    for k in tasks:
        i, j = blk(t, k); b = t[i:j]
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        s = BR.SESS[k]; bf = os.path.join(BRIEFS, "BRIEF_%s.md" % k); sha = hashlib.sha256(open(os.path.join(W.REPO, bf), "rb").read()).hexdigest()
        par = next(x for x in re.findall(r"\nex:(ST4_\w+) a backlog:Story", t) if re.search(r"decomposesInto[^;]*ex:%s\b" % k, t[blk(t, x)[0]:blk(t, x)[1]]))
        parents.setdefault(par, []).append(k)
        L.append('ex:Begin4T_%s a backlog:TransitionEvent ; rdfs:label "%s started by executor session %s"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (
            k, k, s, k, now, W.lit("Work begun at %s UTC inside the box ex:Iter_Ex2, after the start gate said READY and after the readiness check. Executor session: %s, started with the brief generated from the register (%s). The lineage agent does not do this work. %s" % (now, s, bf, NOTE))))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (k, W.lit("Work begun %s UTC by the executor session %s (transition ex:Begin4T_%s). %s" % (now, s, k, NOTE))))
        L.append('ex:EI4_%s a backlog:ExecutorInstance ; rdfs:label "Executor session %s"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s@en .\n' % (
            k, s, W.lit("brief of register %s (sen0414_lineage_brief_exam_v1_0_0), session %s" % (os.path.basename(src), s)), now, W.lit("Started at the instant the coordinator gave as the real start of the session; retired when the session reports.")))
        L.append('ex:Brief4_%s a backlog:ExecutorBrief ; rdfs:label "Brief of %s"@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:AC4_Controlled ; backlog:briefedExecutorInstance ex:EI4_%s ;\n    rdfs:comment %s@en .\n' % (
            k, k, k, k, W.lit("Generated from register %s by sen0414_lineage_brief_exam_v1_0_0.py and passed unedited by the coordinator; file %s, SHA-256 %s. %s" % (os.path.basename(src), bf, sha, NOTE))))
    for sid, ks in parents.items():
        i, j = blk(t, sid); b = t[i:j]
        if "backlog:hasState backlog:InProgress" in b:
            continue
        assert "backlog:hasState backlog:Ready" in b, sid
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        L.append('ex:Begin4T_%s a backlog:TransitionEvent ; rdfs:label "%s started with its first task"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (
            sid, sid, sid, now, W.lit("The story starts with the real start of its first task(s) %s at %s UTC." % (", ".join(ks), now))))
    t = X.set_status4(t, "LS_InProgress")
    out = W.write_new(src, t + "\n" + "".join(L), "Work begun at %s UTC inside the box Iter_Ex2 of the exam lineage: %s; each start is a recorded T_Start naming its executor session, with its executor instance and brief; the stories and the lineage are InProgress." % (now, ", ".join(tasks)))
    print(now, os.path.basename(out))


if __name__ == "__main__":
    main()
