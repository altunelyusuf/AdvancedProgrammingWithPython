"""Shared by the chapter 19 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with warnings off (as sen0414_ch19_corpus_base_v1_0_0.py runs them), with PYTHONPATH
removed and with its own temporary folder as the working directory (every program's first lines do os.chdir(tempfile.mkdtemp())).
The interpreter given is the uv Python 3.14.6 of the chapter 19 research environment (/home/claude/venv314_ch19_latest: schedule 1.2.2,
tzdata 2026.5, pyperclip 1.11.0, playsound3 3.3.2). No program of this chapter is LIVE: none reads the network or a fetched file; the
clock, the zone and the child programs are fixed or are Python itself (see examples_v1_0_0.py)."""
__version__ = "1.0.0"
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def run_program(py, code, inputs=(), needs=()):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("BROWSER", None)
    return subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=300)
