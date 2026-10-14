"""Shared by the chapter 25 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with warnings off, with PYTHONPATH and BROWSER removed, with stdin closed and with CH25_KEEP set to a folder when a picture
is to be kept: a program that saves a picture calls done(), which writes the file into the folder named by CH25_KEEP when that variable is set; the runner sets it to
ch25-deck/images when it records, and the program check sets it to a temporary folder when it runs the program again, to compare the pictures byte by byte. The interpreter
given is the uv Python 3.14.6 of the chapter 25 research environment (/home/claude/venv314_ch25_latest: requests 2.34.2 and beautifulsoup4 4.15.0). The two downloader
programs start an HTTP server of their own on 127.0.0.1 (a local stand-in for xkcd.com, which is never contacted); the others use the standard library only. A program
that waits prints nothing that depends on how long it took: its timings are read from the research record, never measured again."""
__version__ = "1.0.0"
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def run_program(py, code, inputs=(), needs=(), keep=None):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("BROWSER", None)
    if keep:
        env["CH25_KEEP"] = keep
    else:
        env.pop("CH25_KEEP", None)
    return subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=900, stdin=subprocess.DEVNULL)
