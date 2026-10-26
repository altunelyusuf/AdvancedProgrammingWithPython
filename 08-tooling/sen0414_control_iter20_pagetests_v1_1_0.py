#!/usr/bin/env python3
"""sen0414_control_iter20_pagetests v1_1_0 (over v1_0_0, which stays as committed: the NEW page is the newest page file of the chapter, v9_95_0 or above - the chapter 11 page was repaired to v9_96_0; the earlier page is still the newest below v9_95_0) (a NEW file over sen0414_control_iter19_pagetests_v1_4_0.py, which stays as committed) - the lineage agent's own page runs for the Iter_20 page controls of chapters 10 to 25 (G136, G137: the controller re-runs, never trusts the executor's log).
Usage: sen0414_control_iter20_pagetests_v1_0_0.py NN [storyfit | TAGS]     TAGS = t37,t34,t34_old (a comma list: run only those)
Runs, serially and each under `flock /tmp/page_test.lock`, the page test 9.37.0 and 9.34.0 on the new page v9_95_0 and 9.34.0 on the chapter's earlier newest page (the newest page file below v9_95_0); logs control-iter20-logs/p37_chNN_t37.log, _t34.log, _t34_old.log. With 'storyfit' it runs the story-layout probe v1_0_0 (the one rule: photograph lower than the viewport, narrative paragraph within the first screen of the story, every story at 1366x768, 1400x900 and 390x844) and writes p37_chNN_storyfit.log; exit 0 only when every story passes."""
__version__ = "1.1.0"
import glob, os, re, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(T); LOGS = os.path.join(T, "control-iter20-logs")
RUN = os.path.join(T, "sen0414_page_test_run_v1_1_0.py")
def PV(n):
    vs = []
    for f in glob.glob(os.path.join(REPO, "03-materials/ch%s/page/sen0414_ch%s_page_v*.html" % (n, n))):
        m = re.search(r"_page_v(\d+)_(\d+)_(\d+)\.html$", f); v = tuple(int(x) for x in m.groups())
        if v >= (9, 95, 0): vs.append(v)
    return "%d_%d_%d" % max(vs)


def old_ver(n):
    vs = []
    for f in glob.glob(os.path.join(REPO, "03-materials/ch%s/page/sen0414_ch%s_page_v*.html" % (n, n))):
        m = re.search(r"_page_v(\d+)_(\d+)_(\d+)\.html$", f); v = tuple(int(x) for x in m.groups())
        if v < (9, 95, 0): vs.append(v)
    return "%d_%d_%d" % max(vs)


def runs(n, only=None):
    os.makedirs(LOGS, exist_ok=True)
    for tag, test, ver in (("t37", "sen0414_page_test_v9_37_0.py", PV(n)), ("t34", "sen0414_page_test_v9_34_0.py", PV(n)), ("t34_old", "sen0414_page_test_v9_34_0.py", old_ver(n))):
        if only and tag not in only: continue
        lf = os.path.join(LOGS, "p37_ch%s_%s.log" % (n, tag))
        with open(lf, "w", encoding="utf-8") as f:
            r = subprocess.run(["flock", "/tmp/page_test.lock", "python3", RUN, n, ver], env=dict(os.environ, PAGE_TEST_FILE=test), stdout=f, stderr=subprocess.STDOUT, cwd=REPO)
        print(tag, "exit", r.returncode, flush=True)


def storyfit(n):
    page = os.path.join(REPO, "03-materials/ch%s/page/sen0414_ch%s_page_v%s.html" % (n, n, PV(n)))
    r = subprocess.run(["flock", "/tmp/page_test.lock", "python3", os.path.join(T, "sen0414_story_layout_probe_v1_0_0.py"), page, os.path.join(LOGS, "p37_ch%s_storyfit.log" % n)], cwd=REPO)
    sys.exit(r.returncode)


if __name__ == "__main__":
    n = sys.argv[1]
    storyfit(n) if len(sys.argv) > 2 and sys.argv[2] == "storyfit" else runs(n, sys.argv[2].split(",") if len(sys.argv) > 2 else None)
