#!/usr/bin/env python3
"""Writes pywheels_v1_0_0.json and 03-materials/ch17/assets/ASSETS_PROVENANCE_v1_0_0.md for chapter 17 from the wheels committed in
03-materials/ch17/assets (downloaded from PyPI with pip on 2026-10-12: pypdf 6.20.1 and python-docx 1.2.0, the versions the research ran).
The licence of each wheel is read from its METADATA. Usage: pywheels_make_v1_0_0.py"""
import os, json, zipfile, hashlib, re, glob
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "..", "03-materials", "ch17", "assets")
wheels = []
for f in sorted(glob.glob(os.path.join(A, "*.whl"))):
    b = open(f, "rb").read(); z = zipfile.ZipFile(f); md = z.read([n for n in z.namelist() if n.endswith("METADATA")][0]).decode()
    name = re.search(r"^Name: (.*)$", md, re.M).group(1); ver = re.search(r"^Version: (.*)$", md, re.M).group(1)
    lic = re.search(r"^License-Expression: (.*)$", md, re.M) or re.search(r"^License: (.*)$", md, re.M)
    wheels.append({"file": os.path.basename(f), "sha256": hashlib.sha256(b).hexdigest(), "project": "https://pypi.org/project/%s/%s/" % (name, ver), "licence": lic.group(1)})
boot = ("import os\n_cwd0 = os.getcwd()\ndef _before_run():\n    os.chdir(_cwd0)\n")
pk = ["lxml", "pillow", "cryptography", "typing-extensions"]
json.dump({"_version": "1.0.0", "wheels": wheels, "pyodide_packages": pk, "boot_python": boot,
  "_note": "Pure-Python wheels the chapter 17 page embeds (template 9.45.0 unpacks them in the page's Python worker) so that pypdf and python-docx run in the browser; Pyodide 0.28.2's own distribution has neither, but it has the packages in pyodide_packages (lxml 6.0.0, Pillow 11.3.0, cryptography 45.0.5, typing_extensions 4.14.1), which the page loads first; the research ran lxml 6.1.3, Pillow 12.3.0 and cryptography 50.0.2. Downloaded from PyPI with pip on 2026-10-12; the page-data builder refuses a file whose SHA-256 differs from the one recorded here. pdfminer.six is not embedded (6.6 MB of character-map data), so the one example that uses it is shown as recorded. boot_python defines _before_run(), which the Python worker calls before every program and which puts the working folder back as it was at start."},
  open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
rows = "\n".join("| %s | %s | %s | %s |" % (w["file"], w["project"], w["licence"], w["sha256"]) for w in wheels)
open(os.path.join(A, "ASSETS_PROVENANCE_v1_0_0.md"), "w").write("""# Chapter 17 page assets - provenance and licences (v1.0.0)

The chapter 17 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). Pyodide's own package list has neither pypdf nor
python-docx, so the page embeds the two pure-Python wheels below and unpacks them into the browser's Python when it starts (page template 9.45.0;
page-data builder 2.15.0 reads them through 08-tooling/ch17-page/pywheels_v1_0_0.json and refuses a file whose SHA-256 differs from the one
recorded there). The page loads these packages from Pyodide's own distribution first: lxml (6.0.0), Pillow (11.3.0), cryptography (45.0.5)
and typing_extensions (4.14.1); the research ran lxml 6.1.3, Pillow 12.3.0 and cryptography 50.0.2, the page's examples were checked in the
browser against the stored results. pdfminer.six (MIT) is not embedded: its wheel is 6.6 MB of character-map data, so its one example is shown as recorded.

Downloaded on 2026-10-12 from PyPI with pip (the proxy of the build machine); neither wheel was changed.

| file | project page | licence | SHA-256 |
|---|---|---|---|
%s

Both licences (BSD-3-Clause, MIT) allow redistribution with the licence text, which is inside each wheel's dist-info. No file of the book's online
materials is embedded: every example of the chapter builds its own PDF and Word files in memory or in a temporary folder.
Photographs: none; the chapter's stories carry no photograph (see 08-tooling/ch17-page/stories_img_v1_0_0.json).
""" % rows)
print(len(wheels), "wheels")
