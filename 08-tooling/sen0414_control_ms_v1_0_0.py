#!/usr/bin/env python3
"""sen0414_control_ms v1_0_0 - the lineage agent's own control of a midterm-scope chapter (run by the evidence bridge as a test command; exit 0 = the controlled facts hold).
Usage: sen0414_control_ms_v1_0_0.py ms01 | ms03 | ms05
Live re-runs: the controller's checks C1-C8 (sen0414_control_urgent_deck_v1_0_0.py), the deck standard check v1_1_0 (13 of 13), the teaching check (T1-T6), the overlap check (clean), every code string of the manifest present in the page's HTML.
Kept logs of the controller's own runs, parsed here (their SHA-256 is recorded with them): page tests 9.38.0 and 9.37.0 (RESULT PASS, failed 0), the leak probe (seeds 1 to 3 PASS), the diagram audit, the Playground width probe and the story-layout probe (no FAIL line, at least one PASS)."""
import glob, json, os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); T = os.path.join(R, "08-tooling"); L = os.path.join(T, "control-ms-logs"); bad = []
C = {"ms01": ("01", "ch01/SEN0414_Ch01_PythonBasics_3e_v4_2_0.pptx", "ch01/page/chapter_code_ch01_v1_2_0.json", "9_93_1", "v4_2_0"),
     "ms03": ("03", "ch03/SEN0414_Ch03_Loops_3e_v5_2_0.pptx", "ch03/page/chapter_code_ch03_v1_2_0.json", "9_92_0", "v5_2_0"),
     "ms05": ("05", "ch05/SEN0414_Ch05_Debugging_3e_v3_1_0.pptx", "ch05/page/chapter_code_ch05_v1_1_0.json", "9_91_0", "v3_1_0")}
def say(ok, w):
    print(("PASS " if ok else "FAIL ") + w)
    if not ok: bad.append(w)
def run(cmd):
    p = subprocess.run(cmd, cwd=T, capture_output=True, text=True); return p.returncode, p.stdout + p.stderr
def log(name):
    p = os.path.join(L, name); return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None
m = sys.argv[1]; ch, deck, man, pv, dv = C[m]; D = "../03-materials/" + deck; M = "../03-materials/" + man
rc, o = run([sys.executable, "sen0414_control_urgent_deck_v1_0_0.py", D, M]); say(rc == 0 and "RESULT PASS" in o, "controller checks C1-C8 exit %d" % rc)
rc, o = run([sys.executable, "sen0414_deck_standard_check_v1_1_0.py", ch, D, M]); say(rc == 0 and "PASS=13 FAIL=0 NOT_MEASURED=0" in o, "deck standard check 13 of 13 exit %d" % rc)
rc, o = run([sys.executable, "sen0414_deck_teaching_check_v1_0_0.py", D]); say(rc == 0 and "PASS=6 FAIL=0 NOT_MEASURED=0" in o, "teaching check T1-T6 exit %d" % rc)
rc, o = run([sys.executable, "sen0414_deck_overlap_check_v1_0_0.py", D]); say(rc == 0 and "CLEAN" in o, "overlap check exit %d" % rc)
ex = json.load(open(os.path.join(R, "03-materials", man))); ex = ex.get("examples", ex)
page = open(os.path.join(R, "03-materials/ch%s/page/sen0414_ch%s_page_v%s.html" % (ch, ch, pv)), encoding="utf-8").read()
miss = [i for i, e in enumerate(ex) if json.dumps(e["code"])[1:-1] not in page and e["code"] not in page]; say(not miss, "every code string of the manifest (%d) is in the page: missing %s" % (len(ex), miss))
for v, n in (("9_38_0", 416), ("9_37_0", 400)):
    s = log("pagetest_%s_ch%s_v%s_ctl1.log" % (v, ch, pv)); f = re.search(r"features passed (\d+), failed (\d+)", s or ""); say(bool(s) and "RESULT: PASS" in s and f and int(f.group(1)) >= n and f.group(2) == "0", "page test %s (controller's run): %s" % (v, f.group(0) if f else "no log"))
s = log("leakprobe_ch%s_v%s_ctl1.log" % (ch, pv)); say(bool(s) and len(re.findall(r" PASS$", s, re.M)) >= 3 and "FAIL" not in s, "leak probe seeds 1-3: %d PASS lines" % len(re.findall(r" PASS$", s or "", re.M)))
for k in ("diagaudit", "playgroundwidth", "storylayout"):
    s = log("%s_ch%s_v%s_ctl1.log" % (k, ch, pv)); say(bool(s) and "FAIL" not in s and ("PASS" in s or "CLEAN" in s or "RESULT" in s), "%s (controller's run): %s" % (k, (s or "no log").strip().splitlines()[-1][:100] if s and s.strip() else "no log"))
print("RESULT " + ("FAIL: " + "; ".join(bad) if bad else "PASS")); sys.exit(1 if bad else 0)
