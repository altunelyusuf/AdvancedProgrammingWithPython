"""Shared by the chapter 22 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with warnings off, with PYTHONPATH and BROWSER removed and with the folder of the book's
online materials (the zip the four fetching programs read) named in CH22_CACHE, so that the zip is downloaded once per machine and checked
against its SHA-256 every time. A program that saves a picture calls keep(), which copies the file into the folder named by CH22_KEEP when that
variable is set; the runner sets it to ch22-deck/images when it records, and the program check sets it to a temporary folder when it runs the
program again, to compare the pictures byte by byte. The interpreter given is the uv Python 3.14.6 of the chapter 22 research environment
(/home/claude/venv314_ch22_latest: pytesseract 0.3.13, Pillow 12.3.0, NumPy 2.5.4, opencv-python-headless 5.0.0.93, PyAutoGUI 0.9.54) with the real Tesseract 5.3.4
of Ubuntu 24.04 on the PATH. NO PROGRAM OF THIS CHAPTER REACHES A PERSON OR A SERVICE except the download of the publisher's zip of online materials (cached in
CH22_CACHE); the screen programs run on a virtual X display (Xvfb): a local stand-in for a screen, nobody sees the picture."""
__version__ = "1.0.0"
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("CH22_CACHE_DIR", "/home/claude/ch22_cache")


def run_program(py, code, inputs=(), needs=(), keep=None):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("BROWSER", None)
    env.pop("DISPLAY", None)
    env["CH22_CACHE"] = CACHE
    if keep:
        env["CH22_KEEP"] = keep
    else:
        env.pop("CH22_KEEP", None)
    return subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=900)
