#!/usr/bin/env python3
"""Writes pywheels_v1_0_0.json and 03-materials/ch22/assets/ASSETS_PROVENANCE_v1_0_0.md for chapter 22 from the wheel committed in 03-materials/ch22/assets
(pytesseract 0.3.13, the version the research ran, downloaded from PyPI with pip on 2026-10-14). The licence is read from its METADATA. Usage: pywheels_make_v1_0_0.py"""
import os, json, zipfile, hashlib, re, glob
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "..", "03-materials", "ch22", "assets")
wheels = []
for f in sorted(glob.glob(os.path.join(A, "*.whl"))):
    b = open(f, "rb").read(); z = zipfile.ZipFile(f); md = z.read([n for n in z.namelist() if n.endswith("METADATA")][0]).decode()
    name = re.search(r"^Name: (.*)$", md, re.M).group(1); ver = re.search(r"^Version: (.*)$", md, re.M).group(1)
    lic = re.search(r"^License-Expression: (.*)$", md, re.M) or re.search(r"^License: (.*)$", md, re.M)
    wheels.append({"file": os.path.basename(f), "sha256": hashlib.sha256(b).hexdigest(), "project": "https://pypi.org/project/%s/%s/" % (name, ver), "licence": lic.group(1)})
boot = ("import os, sys\n_cwd0 = os.getcwd()\ndef _before_run():\n    os.chdir(_cwd0)\n    sys.set_int_max_str_digits(4300)\n")
json.dump({"_version": "1.0.0", "wheels": wheels, "pyodide_packages": ["pillow", "numpy", "packaging"], "boot_python": boot,
  "_note": "The chapter 22 page embeds one pure-Python wheel, pytesseract 0.3.13 (the version the research ran), so that the chapter's programs can import it and the ones that do not start Tesseract run in the browser; there is no Tesseract program in a browser, so every example that reads text from a picture is shown as recorded. Pillow, NumPy and packaging are Pyodide's own packages (OpenCV is not loaded: the two examples that use it are shown as recorded). The page-data builder refuses a wheel whose SHA-256 differs from the one recorded here."},
  open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
rows = "\n".join("| %s (%s) | yes, embedded and unpacked in the browser's Python | %s | so that the chapter's programs can import pytesseract; SHA-256 %s; the builder refuses a file that differs |" % (w["file"], w["project"], w["licence"], w["sha256"]) for w in wheels)
open(os.path.join(A, "ASSETS_PROVENANCE_v1_0_0.md"), "w").write("""# Chapter 22 page assets - provenance and licences (v1.0.0)

The chapter 22 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). There is no Tesseract program, no PyAutoGUI display and no
ImageMagick in a browser, so the examples that read text from a picture, call another program or read the screen are shown as recorded, not run.

| item | on the page? | licence | why |
|---|---|---|---|
%s
| Pyodide packages `pillow` 11.3.0, `numpy` 2.2.5, `packaging` 24.2 | yes, loaded from the Pyodide distribution (the same CDN as Pyodide) | as the upstream projects state (Pillow: MIT-CMU; NumPy: BSD-3-Clause; packaging: Apache-2.0 or BSD-2-Clause); to be re-checked by the owner | the programs' own imports |
| seven PNG pictures (hurts, cleaned, cleanCv, columns, readsLine, germanLine, pagesPicked) | yes, as recorded pictures, SHA-256 checked when the page is made | drawn by the research programs (Pillow 12.3.0, Python 3.14.6) from sentences written for the course and from the study's own text; the course's own licence applies; the programs name the fonts they used (DejaVu, URW Nimbus Roman, URW Z003, IPAGothic), and the licence of those fonts for pictures of their glyphs is an open question | the page shows what the recorded programs drew |
| the book's online materials (a zip of 7,759,877 bytes: ocr-example.png, frankenstein.png, frankenstein_jpn.png, preprocess_ocr.py and others) | no | **open question**: the licence of the zip and of its pictures is not established | the programs that read them are shown as recorded, not run |
| pictures made from the book's pictures (the four-line page, the Frankenstein line, the word boxes, the hyphens, the low-confidence word, the Japanese line, the screen shot) | no | **open question**, same | left out of the page; they stay in the deck, which uses them for teaching only |
| Tesseract 5.3.4, 5.5.3 and 4.1.1, language data files, NAPS2 8.5.1, OCRmyPDF 17.13.0, PyAutoGUI 0.9.54 | no | not redistributed | they are programs of the machine the research ran on; the page cannot start them |

Library versions differ between the recording (Pillow 12.3.0, NumPy 2.5.4) and the browser (Pillow 11.3.0, NumPy 2.2.5): values were compared, not bytes.
""" % rows)
print(len(wheels), "wheels")
