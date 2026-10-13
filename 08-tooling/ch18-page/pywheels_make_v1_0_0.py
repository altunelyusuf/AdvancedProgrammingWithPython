#!/usr/bin/env python3
"""Writes pywheels_v1_0_0.json and 03-materials/ch18/assets/ASSETS_PROVENANCE_v1_0_0.md for chapter 18 from the wheels committed in
03-materials/ch18/assets (xmltodict 1.0.4 and defusedxml 0.7.1 downloaded from PyPI with pip on 2026-10-12; openpyxl 3.1.5 and et_xmlfile 2.0.0 are the
wheels already committed for chapter 14, byte for byte). The licence of each wheel is read from its METADATA. Usage: pywheels_make_v1_0_0.py"""
import os, json, zipfile, hashlib, re, glob
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "..", "03-materials", "ch18", "assets")
wheels = []
for f in sorted(glob.glob(os.path.join(A, "*.whl"))):
    b = open(f, "rb").read(); z = zipfile.ZipFile(f); md = z.read([n for n in z.namelist() if n.endswith("METADATA")][0]).decode()
    name = re.search(r"^Name: (.*)$", md, re.M).group(1); ver = re.search(r"^Version: (.*)$", md, re.M).group(1)
    lic = re.search(r"^License-Expression: (.*)$", md, re.M) or re.search(r"^License: (.*)$", md, re.M)
    wheels.append({"file": os.path.basename(f), "sha256": hashlib.sha256(b).hexdigest(), "project": "https://pypi.org/project/%s/%s/" % (name, ver), "licence": lic.group(1)})
boot = ("import os\n_cwd0 = os.getcwd()\ndef _before_run():\n    os.chdir(_cwd0)\n")
pk = ["lxml"]
json.dump({"_version": "1.0.0", "wheels": wheels, "pyodide_packages": pk, "boot_python": boot,
  "_note": "Pure-Python wheels the chapter 18 page embeds (template 9.47.0 unpacks them in the page's Python worker) so that xmltodict, defusedxml and openpyxl run in the browser; Pyodide 0.28.2's own distribution has none of them (checked in its pyodide-lock.json), and has lxml 6.0.0, which is loaded from there. The page-data builder refuses a file whose SHA-256 differs from the one recorded here."},
  open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
rows = "\n".join("| %s | %s | %s | %s |" % (w["file"], w["project"], w["licence"], w["sha256"]) for w in wheels)
open(os.path.join(A, "ASSETS_PROVENANCE_v1_0_0.md"), "w").write("""# Chapter 18 page assets - provenance and licences (v1.0.0)

The chapter 18 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). Pyodide's own package list has none of xmltodict,
defusedxml and openpyxl, so the page embeds the four pure-Python wheels below and unpacks them into the browser's Python when it starts (page template
9.47.0; page-data builder 2.16.0 reads them through 08-tooling/ch18-page/pywheels_v1_0_0.json and refuses a file whose SHA-256 differs from the one
recorded there). The page loads lxml (6.0.0) from Pyodide's own distribution; the research ran lxml 6.1.3, and the page's examples were checked in the
browser against the stored results.

Downloaded on 2026-10-12 from PyPI with pip (the proxy of the build machine); no wheel was changed. The openpyxl and et_xmlfile wheels are the files
committed in 03-materials/ch14/assets, byte for byte.

| file | project page | licence | SHA-256 |
|---|---|---|---|
%s

The licences (MIT for xmltodict, openpyxl and et_xmlfile; the Python Software Foundation licence for defusedxml) allow redistribution with the licence text,
which is inside each wheel's dist-info (et_xmlfile also ships LICENCE.python, the Python Software Foundation licence for code derived from the standard
library). No file of the book's online materials is embedded: every example of the chapter builds its own CSV, JSON, XML and workbook files in memory.
Photographs: see 08-tooling/ch18-page/stories_img_v1_0_1.json.
""" % rows)
print(len(wheels), "wheels")
