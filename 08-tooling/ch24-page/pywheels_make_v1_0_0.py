#!/usr/bin/env python3
"""Writes pywheels_v1_0_0.json and 03-materials/ch24/assets/ASSETS_PROVENANCE_v1_0_0.md for chapter 24. The chapter 24 page embeds no wheel and loads no Pyodide package:
none of the chapter's examples can run in a browser (no speech engine, no ffmpeg, no pyttsx3, Whisper or yt-dlp, and no way to start a program). Usage: pywheels_make_v1_0_0.py"""
import os, json
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "..", "03-materials", "ch24", "assets"); os.makedirs(A, exist_ok=True)
boot = ("import os, sys\n_cwd0 = os.getcwd()\ndef _before_run():\n    os.chdir(_cwd0)\n    sys.set_int_max_str_digits(4300)\n")
json.dump({"_version": "1.0.0", "wheels": [], "pyodide_packages": [], "boot_python": boot,
  "_note": "The chapter 24 page embeds no wheel and loads no Pyodide package. pyttsx3 needs a speech engine of the machine (eSpeak NG on Linux), openai-whisper needs PyTorch and ffmpeg and yt-dlp needs the network and ffmpeg; a browser's Python (its platform is 'emscripten') cannot start programs and has none of them, so every example of the chapter is shown as recorded. The page's own playground uses only the standard library. The boot snippet resets the working directory and the integer-to-text digit limit before every program, as the chapter 19 to 23 pages do."},
  open(os.path.join(H, "pywheels_v1_0_0.json"), "w"), indent=1)
open(os.path.join(A, "ASSETS_PROVENANCE_v1_0_0.md"), "w").write("""# Chapter 24 page assets - provenance and licences (v1.0.0)

The chapter 24 page runs the page's own playground in the browser (Pyodide 0.28.2, CPython 3.13.2). **No wheel, no Pyodide package, no model file and no book file is embedded.**
A browser has no speech engine, cannot start programs and does not have pyttsx3, Whisper or yt-dlp, so every example of the chapter is shown as recorded, not run.

| item | on the page? | licence | why |
|---|---|---|---|
| five PNG pictures (waves, hello, audio16k, cues, song) | yes, as recorded pictures, SHA-256 checked when the page is made | drawn by the deck's own programs with a small PNG writer written for the course (no Pillow), from audio that eSpeak NG 1.51 spoke through pyttsx3 2.99 and, for audio16k, that ffmpeg 6.1.1 resampled; the course's own licence applies to the drawings; eSpeak NG is GPL-3.0-or-later and the pictures show waveforms of its output only, which is not the program; whether a waveform of GPL software output carries any obligation is an open question of low risk | the page shows what the recorded programs drew |
| pyttsx3 2.99, openai-whisper 20250625, yt-dlp 2026.8.19, torch 2.14.1, NumPy 2.5.4 | no | not redistributed | not available to a browser's Python |
| the Whisper model files (tiny to large-v3, 75 MB to 3 GB) | no | not redistributed | far too large for a page, and not loadable in a browser's Python here |
| eSpeak NG, ffmpeg, aplay | no | not redistributed | programs of the machine the research ran on |
| the book's online materials (a zip of 7,759,877 bytes with 91 files; hello_tts.py is the one that imports pyttsx3) | no | **open question**: the licence of the zip and of its files is not established | the page embeds no file of them |
| LibriVox recordings of the Gettysburg Address on archive.org (the stand-in for YouTube) | no | public-domain recordings, not embedded; the research read their metadata and transcribed them locally | only the recorded results are shown |

Library versions differ between the recording and the browser (the browser has none of the packages above).
""")
print("0 wheels")
