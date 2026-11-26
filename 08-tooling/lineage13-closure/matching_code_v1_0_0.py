#!/usr/bin/env python3
"""Lineage13 measure ST13_Measure_MatchingCode (2026-11-26): for chapters 16 to 20, compares the code of every example of the newest chapter-code manifest with (a) the chaptercode block of the newest page data (matched by example name), (b) the code inside the newest page html (as the page embeds it, with or without \\u escapes of non-ASCII characters), (c) the Lab / Playground cell of the newest examples_out file of the deck folder, and looks for lab-library files in the repository. Prints one line per check and a verdict; exit 0 when every difference is listed. Usage: matching_code_v1_0_0.py"""
__version__ = "1.0.0"
import glob, json, os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
key = lambda x: [int(v) for v in re.findall(r"_v(\d+)_(\d+)_(\d+)", x)[-1]]
def newest(pat):
    fs = sorted(glob.glob(os.path.join(R, pat)), key=key)
    return fs[-1]
diffs = 0; total = 0
print("Matching-code measurement, Lineage13 (2026-11-26)")
for n in (16, 17, 18, 19, 20):
    mf = newest("03-materials/ch%d/page/chapter_code_ch%d_v*.json" % (n, n)); man = json.load(open(mf, encoding="utf-8"))
    pd = newest("08-tooling/ch%d-page/page_data_v*.json" % n); cc = json.load(open(pd, encoding="utf-8"))["chaptercode"]
    html = open(newest("03-materials/ch%d/page/sen0414_ch%d_page_v*.html" % (n, n)), encoding="utf-8").read()
    ef = glob.glob(os.path.join(R, "08-tooling/ch%d-deck/examples_out_v*.json" % n)) or glob.glob(os.path.join(R, "08-tooling/ch%d-page/examples_out_v*.json" % n))
    eo = json.load(open(sorted(ef, key=key)[-1], encoding="utf-8")); eo_name = os.path.basename(sorted(ef, key=key)[-1])
    pdc = {e["name"]: e["code"] for e in cc["examples"]}
    ref = "page data names " + cc["file"].split("/")[-1] + (" (the newest manifest)" if cc["file"].endswith(os.path.basename(mf)) else " (NOT the newest manifest)")
    d_pd = d_html = d_eo = 0
    for e in man["examples"]:
        total += 1
        if pdc.get(e["name"]) != e["code"]: d_pd += 1; print("  DIFF page data   ch%d %s" % (n, e["id"]))
        forms = [json.dumps(e["code"], ensure_ascii=a)[1:-1] for a in (False, True)]
        forms += [f.replace("</", "<\\/") for f in forms]
        if not any(f in html for f in forms): d_html += 1; print("  DIFF page html   ch%d %s" % (n, e["id"]))
        cell = eo.get(e["name"])
        if not cell or cell[0][0] != e["code"]: d_eo += 1; print("  DIFF Lab cell    ch%d %s" % (n, e["id"]))
    diffs += d_pd + d_html + d_eo
    print("  " + ref)
    print("chapter %d: manifest %s, %d examples; page data %s differs %d; page html differs %d; Lab/Playground cells (%s) differ %d" % (n, os.path.basename(mf), len(man["examples"]), os.path.basename(pd), d_pd, d_html, eo_name, d_eo))
lab = [p for p in glob.glob(os.path.join(R, "**", "*"), recursive=True) if re.search(r"lab[_-]?(lib|session|handout)", os.path.basename(p), re.I) and os.sep + ".git" + os.sep not in p]
print("lab-library, lab-session or lab-handout files in this repository: %d %s" % (len(lab), [os.path.relpath(p, R) for p in lab]))
print("differences between manifests, pages and Lab cells: %d of %d examples checked in three places" % (diffs, total))
print("lab libraries: not part of this repository, so their code is not compared here; the comparison is recorded for the lab lineage.")
sys.exit(0)
