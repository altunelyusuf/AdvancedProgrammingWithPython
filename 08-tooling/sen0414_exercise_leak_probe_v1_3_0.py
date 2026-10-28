#!/usr/bin/env python3
"""sen0414_exercise_leak_probe v1_3_0 (wrapper, a NEW file) - runs the probe sen0414_exercise_leak_probe_v1_3_0.js, which takes the Python worker from the TEMPLATE FILE itself, on the programs of a PAGE's data
(made by sen0414_exercise_leak_pagedata_v1_0_0.py) for several seeds. Exit 0 only when every seed prints PASS.
Usage: sen0414_exercise_leak_probe_v1_3_0.py NODE_PATH_DIR WORK_DIR TEMPLATE.html PAGE.html ROUNDS PROBES SEED [SEED...]"""
import os, subprocess, sys
nodep, work, tpl, page, rounds, probes = sys.argv[1:7]; seeds = sys.argv[7:]; here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(work, exist_ok=True)
prog = os.path.join(work, "programs.json")
r = subprocess.run([sys.executable, os.path.join(here, "sen0414_exercise_leak_pagedata_v1_0_0.py"), page, prog], capture_output=True, text=True); print(r.stdout.strip(), r.stderr[-300:]); rc = r.returncode
for sd in seeds:
    out = os.path.join(work, "leak_%s_%s.json" % (os.path.basename(tpl)[:-5], sd))
    r = subprocess.run(["node", os.path.join(here, "sen0414_exercise_leak_probe_v1_3_0.js"), tpl, page, prog, out, rounds, probes, sd], env=dict(os.environ, NODE_PATH=nodep), capture_output=True, text=True, timeout=3000)
    print((r.stdout.strip() or r.stderr[-300:])); rc |= (r.returncode != 0) or ("FAIL" in r.stdout)
sys.exit(1 if rc else 0)
