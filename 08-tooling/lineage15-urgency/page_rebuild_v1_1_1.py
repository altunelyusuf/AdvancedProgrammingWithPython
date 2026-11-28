#!/usr/bin/env python3
"""page_rebuild 1.1.1 (over 1.1.0: builder 4.18.5, whose comment guard ignores script text). 1.1.0 (over 1.0.0: the concepts the clean drops by EXTRA are added to the page's XMETAIDS; with --data-ready the page data of the next version already exists (regenerated from newer sources by the page-data builder) and is used as it is; the ontology files pinned are then the newest of each part in the chapter folder). 1.0.0 (Lineage15, story ST15_Pages_Ch1_9, 2026-11-27): rebuilds the page of one chapter on template 9.58.0 from the chapter's newest page data, through the
existing page builder (sen0414_ch02_page_build_v4_18_5.py, the generic builder over chapter number), then applies the meta clean of page_meta_clean_v1_0_0 and writes the page as the
next version of the chapter. The page data is copied to the next version under its own name (data unchanged; the version in the file is raised).
CME standards files are read from a scratch folder holding the files at the digests the page data records (recovered from the CME history by digest, because the pinned commit is not in the clone).
Usage: page_rebuild_v1_1_1.py NN [--data-ready]"""
import glob, json, os, re, shutil, subprocess, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
T = os.path.join(R, "08-tooling"); sys.path.insert(0, T)
import page_meta_clean_v1_0_0 as M
nn = sys.argv[1]; ch = "ch" + nn
sv = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", p)[0]]
pages = sorted(glob.glob(f"{R}/03-materials/{ch}/page/sen0414_{ch}_page_v*.html"), key=sv); cur = sv(pages[-1])
datas = sorted(glob.glob(f"{T}/{ch}-page/page_data_v*.json"), key=sv); dcur = datas[-1]
new = [cur[0], cur[1] + 1, 0]; pv = "%d_%d_%d" % tuple(new)
dnew = f"{T}/{ch}-page/page_data_v{pv}.json"
READY = "--data-ready" in sys.argv
if READY:
    assert os.path.exists(dnew), "no regenerated data " + dnew; d = json.load(open(dnew, encoding="utf-8")); assert d["_version"].replace(".", "_") == pv
else:
    if os.path.exists(dnew): sys.exit("refusing to overwrite " + dnew)
    d = json.load(open(dcur, encoding="utf-8")); d["_version"] = pv.replace("_", ".")
    json.dump(d, open(dnew, "w", encoding="utf-8"), ensure_ascii=False)
# CME standards at the recorded digests
import hashlib
pin = f"/tmp/cmepin_{nn}"; os.makedirs(pin, exist_ok=True)
for st in d["course"]["corpus"]["standards"]:
    path = st["folder"] + "/" + st["path"]; got = False
    for r in subprocess.run(["git", "-C", "/home/claude/cme", "log", "--all", "--format=%h", "--", path], capture_output=True, text=True).stdout.split():
        b = subprocess.run(["git", "-C", "/home/claude/cme", "show", f"{r}:{path}"], capture_output=True).stdout
        if hashlib.sha256(b).hexdigest() == st["sha256"]:
            dest = os.path.join(pin, path); os.makedirs(os.path.dirname(dest), exist_ok=True); open(dest, "wb").write(b); got = True; break
    if not got: sys.exit("standards file at the recorded digest not found: " + path)
scr = f"/tmp/rb_{nn}"; shutil.rmtree(scr, ignore_errors=True); os.makedirs(scr)
oldh = open(pages[-1], encoding="utf8").read()
names = dict(re.findall(r'data-kind="chapter" data-name="sen0414_ch\d\d_(domain_tbox|domain_abox|document)_v([\d_]+)\.ttl"', oldh))
names.update(dict(re.findall(r'data-kind="research" data-name="sen0414_ch\d\d_(research)_v([\d_]+)\.ttl"', oldh)))
if READY:
    for part in ("domain_tbox", "domain_abox", "document", "research"):
        fs = sorted(glob.glob(f"{R}/03-materials/{ch}/rdodi/sen0414_{ch}_{part}_v*.ttl"), key=sv); names[part] = re.findall(r"_v([\d_]+)\.ttl", fs[-1])[0]
pinv = ",".join("%s=%s" % (k, names[k]) for k in ("domain_tbox", "domain_abox", "document", "research"))
env = dict(os.environ, CH_ONT_PIN=pinv, PAGE_TEMPLATE="course_page_template_v9_58_0.html", PAGE_VER=pv, PAGE_SCRATCH=scr, CME_REPO=pin)
r = subprocess.run([sys.executable, f"{T}/sen0414_ch02_page_build_v4_18_5.py", nn], env=env, capture_output=True, text=True)
if r.returncode: sys.exit("builder failed:\n" + r.stdout[-800:] + r.stderr[-1500:])
out = f"{scr}/sen0414_{ch}_page_v{pv}.html"
h = open(out, encoding="utf8").read()
h, rep = M.clean(h, ch); h, ids = M.exclude(h, ch)
for _c, _i in sorted(M.EXTRA):   # a concept whose written questions the clean drops (EXTRA) is also left out of the generated exams and drills, so the page asks no question the bank no longer has
    if _c == ch and 'XMETAIDS=new Set([' in h and "'%s'" % _i not in h.split('XMETAIDS=new Set([',1)[1].split(']',1)[0]: h = h.replace('XMETAIDS=new Set([', "XMETAIDS=new Set(['%s'," % _i, 1)

dst = f"{R}/03-materials/{ch}/page/sen0414_{ch}_page_v{pv}.html"; open(dst, "w", encoding="utf8").write(h)
shutil.copy(f"{scr}/corpus_manifest_v{pv}.json", f"{T}/{ch}-page/corpus_manifest_v{pv}.json")
print(nn, pv, "pin", pinv, "lambda", len(re.findall("lambda", h, re.I)), "tab", h.count("Slide source code"), "open", h.count("Open result and answers"), "meta removed", len(rep), "excluded nodes", ids)
