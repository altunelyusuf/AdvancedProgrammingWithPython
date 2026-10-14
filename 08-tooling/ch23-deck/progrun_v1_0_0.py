"""Shared by the chapter 23 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with warnings off, with PYTHONPATH and BROWSER removed, with DISPLAY removed (every program starts its OWN
virtual X display, Xvfb, so that nothing is ever sent to the screen of this machine) and with stdin closed. A program that saves a picture calls done(),
which copies the file into the folder named by CH23_KEEP when that variable is set; the runner sets it to ch23-deck/images when it records, and the
program check sets it to a temporary folder when it runs the program again, to compare the pictures byte by byte. The interpreter given is the uv Python
3.14.6 of the chapter 23 research environment (/home/claude/venv314_ch23_latest: PyAutoGUI 0.9.54, PyScreeze 1.0.1, PyMsgBox 2.0.1, PyTweening 1.2.0,
PyGetWindow 0.0.9, MouseInfo 0.1.3, pyperclip 1.11.0, python3-xlib 0.15, Pillow 12.3.0, NumPy 2.5.4, opencv-python-headless 5.0.0.93) with Xvfb, openbox,
xdotool, xclip, xterm, xrandr, xprintidle and scrot of Ubuntu 24.04 on the PATH. NO PROGRAM OF THIS CHAPTER REACHES A PERSON OR A SERVICE; the programs run on a
virtual X display: a local stand-in for a screen, nobody sees the picture."""
__version__ = "1.0.0"
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("CH23_CACHE_DIR", "/home/claude/ch23_cache")


def run_program(py, code, inputs=(), needs=(), keep=None):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("BROWSER", None)
    env.pop("DISPLAY", None)
    env["CH23_CACHE"] = CACHE
    if keep:
        env["CH23_KEEP"] = keep
    else:
        env.pop("CH23_KEEP", None)
    return subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=900, stdin=subprocess.DEVNULL)
