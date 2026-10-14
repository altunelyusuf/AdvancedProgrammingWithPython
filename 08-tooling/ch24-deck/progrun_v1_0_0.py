"""Shared by the chapter 24 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with warnings off, with PYTHONPATH and BROWSER removed, with DISPLAY removed (no program of this chapter uses a display),
and with stdin closed. A program that saves a picture calls done(), which copies the file into the folder named by CH24_KEEP when that variable is set; the runner sets it to
ch24-deck/images when it records, and the program check sets it to a temporary folder when it runs the program again, to compare the pictures byte by byte. The interpreter given is
the uv Python 3.14.6 of the chapter 24 research environment (/home/claude/venv314_ch24_latest: pyttsx3 2.99, openai-whisper 20250625, yt-dlp 2026.8.19, torch 2.14.1+cpu, NumPy 2.5.4)
with eSpeak NG 1.51 and ffmpeg 6.1.1 of Ubuntu 24.04 on the PATH. NO PROGRAM OF THIS CHAPTER PLAYS A SOUND OR REACHES A PERSON: the machine has no sound card, so the speech goes to WAV
files that are deleted when the program ends. The programs that read a public site read archive.org (LibriVox readings in the public domain), which STANDS IN FOR YouTube."""
__version__ = "1.0.0"
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("CH24_CACHE_DIR", "/home/claude/ch24_cache")


def run_program(py, code, inputs=(), needs=(), keep=None):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("BROWSER", None)
    env.pop("DISPLAY", None)
    env["CH24_CACHE"] = CACHE
    if keep:
        env["CH24_KEEP"] = keep
    else:
        env.pop("CH24_KEEP", None)
    return subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=900, stdin=subprocess.DEVNULL)
