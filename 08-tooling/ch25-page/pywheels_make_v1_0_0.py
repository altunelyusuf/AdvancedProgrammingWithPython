#!/usr/bin/env python3
"""Writes pywheels_v1_0_0.json and 03-materials/ch25/assets/ASSETS_PROVENANCE_v1_0_0.md for the Threads page (file slot 25). The page embeds no wheel and loads no Pyodide package:
the research's examples start child interpreters, a local HTTP server and process pools, none of which a browser's Python can do, and a browser's Python cannot start a thread. Usage: pywheels_make_v1_0_0.py"""
import os, json
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "..", "03-materials", "ch25", "assets"); os.makedirs(A, exist_ok=True)
boot = ("import os, sys\n_cwd0 = os.getcwd()\ndef _before_run():\n    os.chdir(_cwd0)\n    sys.set_int_max_str_digits(4300)\n")
json.dump({"_version": "1.0.0", "wheels": [], "pyodide_packages": [], "boot_python": boot,
  "_note": "The Threads page embeds no wheel and loads no Pyodide package. The research's examples start other interpreters (the standard, free-threaded, 3.13, 3.12 and 3.11 builds), a local HTTP server, process pools and threads; a browser's Python (its platform is 'emscripten') cannot start programs (OSError: emscripten does not support processes) and cannot start a thread (RuntimeError: can't start new thread), so every example of the chapter is shown as recorded. The page's own playground uses only the standard library and does not start a thread. The boot snippet resets the working directory and the integer-to-text digit limit before every program, as the chapter 19 to 24 pages do."},
  open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
open(os.path.join(A, "ASSETS_PROVENANCE_v1_0_0.md"), "w").write("""# Threads page assets - provenance and licences (v1.0.0)

The Threads page (file slot 25, material of the 2nd edition's chapter 17) runs the page's own playground in the browser (Pyodide 0.28.2, CPython 3.13.2). **No wheel, no Pyodide package and no book file is embedded.**
A browser's Python cannot start programs or threads, so every example of the chapter is shown as recorded, not run.

| item | on the page? | licence | why |
|---|---|---|---|
| one PNG picture (skipped.png: the comics a downloader skipped) | yes, as a recorded picture, SHA-256 checked when the page is made | drawn by the deck's program fixedCut_v1_0_0.py with a small PNG writer written for the course (no Pillow) from a run against a local stand-in server; the course's own licence applies | the page shows what the recorded program drew |
| requests 2.34.2, beautifulsoup4 4.15.0 | no | not redistributed | the downloader examples need sockets and a server, which a browser's Python does not have |
| the free-threaded and other interpreter builds (3.14.6t, 3.13, 3.12, 3.11) | no | not redistributed | programs of the machine the research ran on |
| the book's online materials | no | **open question**: the licence of the book's downloadable files is not established | the page embeds no file of them |
| xkcd.com | no | never contacted | a local HTTP server on 127.0.0.1 stood in for it; no comic was fetched or shown |

Library and interpreter versions differ between the recording and the browser (the browser has Python 3.13.2 and none of the packages above).
""")
print("0 wheels")
