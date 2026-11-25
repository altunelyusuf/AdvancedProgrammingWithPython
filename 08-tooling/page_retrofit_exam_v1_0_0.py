#!/usr/bin/env python3
"""page_retrofit_exam 1.0.0 - gives a built chapter page the exam results tab of template 9.54.0 without rebuilding it.
Takes the chapter's latest page, applies template_patch_v9_54_0.py to it, sets the next minor page version in the version marks
(meta name=version and the data's _version), writes the new page, and copies the chapter's page data and corpus manifest to the new
version (with _version set). Everything else in the page stays byte for byte. Prints the lines that changed.
usage: page_retrofit_exam_v1_0_0.py NN"""
import sys, os, re, glob, json, subprocess, difflib
__version__ = "1.0.0"
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.dirname(here)
N = sys.argv[1]
vkey = lambda p: [int(x) for x in re.search(r"_v([\d_]+)\.html$", p).group(1).split("_")]
pages = sorted(glob.glob(os.path.join(repo, "03-materials", "ch%s" % N, "page", "sen0414_ch%s_page_v*.html" % N)), key=vkey)
old = pages[-1]; ov = re.search(r"_v([\d_]+)\.html$", old).group(1).split("_"); nv = [ov[0], str(int(ov[1]) + 1), "0"]
OV, NV = ".".join(ov), ".".join(nv)
new = old.replace("_v" + "_".join(ov) + ".html", "_v" + "_".join(nv) + ".html")
assert not os.path.exists(new), new
tmp = new + ".tmp"
subprocess.check_call([sys.executable, os.path.join(here, "template_patch_v9_54_0.py"), old, tmp], stdout=subprocess.DEVNULL)
s = open(tmp, encoding="utf-8").read(); os.remove(tmp)
for a, b in [('<meta name="version" content="%s">' % OV, '<meta name="version" content="%s">' % NV), ('"_version": "%s"' % OV, '"_version": "%s"' % NV)]:
    assert s.count(a) == 1, (s.count(a), a)
    s = s.replace(a, b)
open(new, "w", encoding="utf-8").write(s)
for kind in ("page_data", "corpus_manifest"):
    f = os.path.join(here, "ch%s-page" % N, "%s_v%s.json" % (kind, "_".join(ov)))
    if os.path.exists(f):
        d = json.load(open(f, encoding="utf-8"))
        if isinstance(d, dict) and "_version" in d: d["_version"] = NV
        json.dump(d, open(os.path.join(here, "ch%s-page" % N, "%s_v%s.json" % (kind, "_".join(nv))), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
o = open(old, encoding="utf-8").read().split("\n"); n = s.split("\n")
ch = [(i, j) for tag, i, _, j, _ in difflib.SequenceMatcher(None, o, n, autojunk=False).get_opcodes() if tag != "equal"]
print("ch%s: %s -> %s; %d changed line block(s); %d -> %d lines" % (N, OV, NV, len(ch), len(o), len(n)))
