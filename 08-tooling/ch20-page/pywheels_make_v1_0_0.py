#!/usr/bin/env python3
"""Writes pywheels_v1_0_0.json and 03-materials/ch20/assets/ASSETS_PROVENANCE_v1_0_0.md for chapter 20. The chapter 20 page embeds no wheel: the examples that
run in the browser use only the standard library, plus the Pyodide package ssl (the standard library's ssl module, which Pyodide ships as a separate
package and the chapter's examples import). ezgmail (GPLv3+) and Google's client library (a 16.8 MB wheel) are not embedded. Usage: pywheels_make_v1_0_0.py"""
import os, json
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "..", "03-materials", "ch20", "assets"); os.makedirs(A, exist_ok=True)
boot = ("import os, sys\n_cwd0 = os.getcwd()\ndef _before_run():\n    os.chdir(_cwd0)\n    sys.set_int_max_str_digits(4300)\n")
json.dump({"_version": "1.0.0", "wheels": [], "pyodide_packages": ["ssl"], "boot_python": boot,
  "_note": "The chapter 20 page embeds no wheel. It asks Pyodide for its ssl package (the standard library module that smtplib and the chapter's programs import) and resets the working directory and the integer-to-text digit limit before every program, as the chapter 19 page does (template 9.48.0)."},
  open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
open(os.path.join(A, "ASSETS_PROVENANCE_v1_0_0.md"), "w").write("""# Chapter 20 page assets - provenance and licences (v1.0.0)

The chapter 20 page runs the chapter's Python in the browser (Pyodide 0.28.2, CPython 3.13.2). **No wheel and no book file is embedded.**

| item | on the page? | licence | why |
|---|---|---|---|
| Python standard library (email, imaplib, smtplib, json, secrets, hmac, ...) | yes, as Pyodide ships it | Python Software Foundation licence | the examples that run use it |
| Pyodide package `ssl` | yes, loaded from the Pyodide distribution (the same CDN as Pyodide) | Python Software Foundation licence | smtplib and the chapter's programs import ssl |
| ezgmail 2026.4.28 | no | GPLv3+ (PyPI classifier and metadata; published as a source distribution of 31,345 bytes, no wheel) | a copyleft licence; the course does not ship it inside a page, and it needs Google's client library |
| google-api-python-client 2.201.0 | no | Apache-2.0 | its wheel is 16,812,656 bytes, more than the 16 MB a page may hold |
| requests 2.34.2, aiosmtpd 1.4.6 | no | Apache-2.0 (requests), Apache-2.0 (aiosmtpd) | they need sockets and threads, which a browser's Python does not have |

The research and the deck ran these packages under Python 3.14.6 (08-tooling/ch20-page/third_party_record_v1_0_0.json). The 36 examples that need them are shown on the
page as recorded, not run, each with its reason (08-tooling/ch20-page/standin_v1_0_0.json). No file of the book's online materials is embedded (the zip has no file for
chapter 20). Photographs: see 08-tooling/ch20-page/stories_img_v1_0_0.json (none used).
""")
print("0 wheels")
