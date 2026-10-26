#!/usr/bin/env python3
"""sen0414_exercise_leak_probe v1_0_0 (wrapper) - runs sen0414_exercise_leak_probe_v1_0_0.js on the chapter-code manifests of chapters.
Usage: sen0414_exercise_leak_probe_v1_0_0.py NODE_PATH_DIR WORK_DIR ROUNDS PROBES SEED CH [CH...]   (RESTORE=1 in the environment tests the repaired _run). Exit 0 only when every chapter PASSes."""
import glob, json, os, subprocess, sys
nodep, work, rounds, probes, seed = sys.argv[1:6]; here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here); os.makedirs(work, exist_ok=True); rc = 0
for ch in sys.argv[6:]:
    m = sorted(glob.glob(os.path.join(root, "03-materials", "ch%02d" % int(ch), "page", "chapter_code_ch%02d_v*.json" % int(ch)))); man = m[-1]; d = json.load(open(man))
    lib = d.get("library") or {}; wl = [os.path.join(root, f) for f in ([lib["file"]] if lib.get("file") else []) + (lib.get("data_files") or [])]
    out = os.path.join(work, "leak_ch%02d%s.json" % (int(ch), "_restore" if os.environ.get("RESTORE") else ""))
    r = subprocess.run(["node", os.path.join(here, "sen0414_exercise_leak_probe_v1_0_0.js"), man, out, rounds, probes, seed] + wl, env=dict(os.environ, NODE_PATH=nodep), capture_output=True, text=True, timeout=1800)
    print("ch%02d" % int(ch), os.path.basename(man), (r.stdout.strip() or r.stderr[-300:])); rc |= r.returncode or ("FAIL" in r.stdout)
sys.exit(1 if rc else 0)
