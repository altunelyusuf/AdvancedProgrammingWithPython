#!/usr/bin/env python3
"""Writes pywheels_v1_0_0.json and 03-materials/ch23/assets/ASSETS_PROVENANCE_v1_0_0.md for chapter 23. The chapter 23 page embeds no wheel and loads no Pyodide package:
none of the chapter's examples can run in a browser (no mouse, keyboard, X server or program to start). Usage: pywheels_make_v1_0_0.py"""
import os, json
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "..", "03-materials", "ch23", "assets"); os.makedirs(A, exist_ok=True)
boot = ("import os, sys\n_cwd0 = os.getcwd()\ndef _before_run():\n    os.chdir(_cwd0)\n    sys.set_int_max_str_digits(4300)\n")
json.dump({"_version": "1.0.0", "wheels": [], "pyodide_packages": [], "boot_python": boot,
  "_note": "The chapter 23 page embeds no wheel and loads no Pyodide package. PyAutoGUI needs a platform it supports (Windows, macOS, or Linux with an X server and python3-xlib), a mouse and keyboard to control and programs to start; a browser's Python offers none of them (its platform is 'emscripten'), so every example of the chapter is shown as recorded. The page's own playground uses only the standard library. The boot snippet resets the working directory and the integer-to-text digit limit before every program, as the chapter 19 to 22 pages do."},
  open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
open(os.path.join(A, "ASSETS_PROVENANCE_v1_0_0.md"), "w").write("""# Chapter 23 page assets - provenance and licences (v1.0.0)

The chapter 23 page runs the page's own playground in the browser (Pyodide 0.28.2, CPython 3.13.2). **No wheel, no Pyodide package and no book file is embedded.**
A browser has no mouse or keyboard to control, no X server and no way to start programs, so every example of the chapter is shown as recorded, not run.

| item | on the page? | licence | why |
|---|---|---|---|
| six PNG pictures (spiral, mouseInfo, screen, located, frame, typed) | yes, as recorded pictures, SHA-256 checked when the page is made | drawn or captured by the research programs on a virtual X display (Xvfb, not a real screen) with Pillow 12.3.0 under Python 3.14.6, from windows and shapes written for the course; the MouseInfo window shows MouseInfo 0.1.3 (a Tk window) and the others show Tk windows of the study; the course's own licence applies; the licence of MouseInfo's window look for a picture of it is not established, an open question of low risk | the page shows what the recorded programs drew or captured |
| PyAutoGUI 0.9.54, PyScreeze 1.0.1, PyMsgBox 2.0.1, pyperclip 1.11.0, MouseInfo 0.1.3, python3-xlib, PyTweening, PyGetWindow, OpenCV 5.0.0.93 | no | not redistributed | they need a supported platform and a display; the page cannot run them |
| the book's online materials (a zip of 7,759,877 bytes with spiralDraw.py and others) | no | **open question**: the licence of the zip and of its files is not established | the example that runs spiralDraw.py is shown as recorded |
| Xvfb, openbox, xdotool, xev, xterm, ImageMagick | no | not redistributed | programs of the machine the research ran on |

Library versions differ between the recording and the browser (the browser has none of the packages above).
""")
print("0 wheels")
