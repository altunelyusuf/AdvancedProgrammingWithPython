"""Shared by the chapter 21 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with warnings off, with PYTHONPATH and BROWSER removed and with the folder of the book's
online materials (the zip the four fetching programs read) named in CH21_CACHE, so that the zip is downloaded once per machine and checked
against its SHA-256 every time. A program that saves a picture calls keep(), which copies the file into the folder named by CH21_KEEP when that
variable is set; the runner sets it to ch21-deck/images when it records, and the program check sets it to a temporary folder when it runs the
program again, to compare the pictures byte by byte. The interpreter given is the uv Python 3.14.6 of the chapter 21 research environment
(/home/claude/venv314_ch21_latest: Pillow 12.3.0, Matplotlib 3.11.2, NumPy 2.5.4, pyperclipimg 0.2.0). NO PROGRAM OF THIS CHAPTER REACHES A
PERSON OR A SERVICE except the download of the publisher's zip of online materials; the clipboard program runs on a virtual X display (Xvfb)
with the real xclip, a local stand-in for a screen: nobody sees the picture."""
__version__ = "1.0.0"
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("CH21_CACHE_DIR", "/home/claude/ch21_cache")


def run_program(py, code, inputs=(), needs=(), keep=None):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("BROWSER", None)
    env.pop("DISPLAY", None)
    env["CH21_CACHE"] = CACHE
    if keep:
        env["CH21_KEEP"] = keep
    else:
        env.pop("CH21_KEEP", None)
    return subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=400)
