#!/usr/bin/env python3
"""Writes pywheels_v1_0_0.json and 03-materials/ch19/assets/ASSETS_PROVENANCE_v1_0_0.md for chapter 19 from the wheels committed in
03-materials/ch19/assets (pyperclip 1.11.0, playsound3 3.3.2, tzdata 2026.5 and schedule 1.2.2, the versions the research ran, downloaded from PyPI with pip
on 2026-10-13). The licence of each wheel is read from its METADATA. Usage: pywheels_make_v1_0_0.py"""
import os, json, zipfile, hashlib, re, glob
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "..", "03-materials", "ch19", "assets")
wheels = []
for f in sorted(glob.glob(os.path.join(A, "*.whl"))):
    b = open(f, "rb").read(); z = zipfile.ZipFile(f); md = z.read([n for n in z.namelist() if n.endswith("METADATA")][0]).decode()
    name = re.search(r"^Name: (.*)$", md, re.M).group(1); ver = re.search(r"^Version: (.*)$", md, re.M).group(1)
    lic = re.search(r"^License-Expression: (.*)$", md, re.M) or re.search(r"^License: (.*)$", md, re.M)
    wheels.append({"file": os.path.basename(f), "sha256": hashlib.sha256(b).hexdigest(), "project": "https://pypi.org/project/%s/%s/" % (name, ver), "licence": lic.group(1)})
boot = ("import os, sys\n_cwd0 = os.getcwd()\ndef _before_run():\n    os.chdir(_cwd0)\n    sys.set_int_max_str_digits(4300)\n")
json.dump({"_version": "1.0.0", "wheels": wheels, "pyodide_packages": [], "boot_python": boot,
  "_note": "Pure-Python wheels the chapter 19 page embeds (template 9.48.0 unpacks them in the page's Python worker) so that schedule, pyperclip, playsound3 and the tzdata 2026.5 time zone database run in the browser; the boot snippet also puts the integer-to-text digit limit back to its default before every program, because one example (Profiling by clock) switches it off for the whole Python; Pyodide 0.28.2's own distribution has none of schedule, pyperclip and playsound3 and has tzdata 2025.2, which is not loaded so that the page uses the database of the recording. The page-data builder refuses a file whose SHA-256 differs from the one recorded here."},
  open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
rows = "\n".join("| %s | %s | %s | %s |" % (w["file"], w["project"], w["licence"], w["sha256"]) for w in wheels)
open(os.path.join(A, "ASSETS_PROVENANCE_v1_0_0.md"), "w").write("""# Chapter 19 page assets - provenance and licences (v1.0.0)

The chapter 19 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). Pyodide's own package list has none of schedule, pyperclip
and playsound3, and its tzdata is release 2025.2, so the page embeds the four wheels below (all pure Python or data, no compiled code) and unpacks them into the
browser's Python when it starts (page template 9.48.0; page-data builder 2.17.0 reads them through 08-tooling/ch19-page/pywheels_v1_0_0.json and refuses a
file whose SHA-256 differs from the one recorded there). They are the versions the research ran under Python 3.14.6. The tzdata wheel carries the time
zone database 2026.5 that the stored zone results were printed with.

Downloaded on 2026-10-13 from PyPI with pip (the proxy of the build machine); no wheel was changed.

| file | project page | licence | SHA-256 |
|---|---|---|---|
%s

The licences (MIT for schedule and playsound3, BSD for pyperclip, Apache-2.0 for tzdata) allow redistribution with the licence text, which is inside each
wheel's dist-info. No file of the book's online materials is embedded (calcProd.py, stopwatch.py and simplecountdown.py are written out by the examples
themselves where they are used). Photographs: see 08-tooling/ch19-page/stories_img_v1_0_1.json.
""" % rows)
print(len(wheels), "wheels")
