"""Shared by the chapter 18 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with warnings off (as sen0414_ch18_corpus_base_v1_0_0.py runs them), with PYTHONPATH
removed and with its own temporary folder as the working directory (every program's first lines do os.chdir(tempfile.mkdtemp())).
The interpreter given is the uv Python 3.14.6 of the chapter 18 research environment (/home/claude/venv314_ch18_latest: pypdf 6.20.1,
python-docx 1.2.0, pdfminer.six 20260107, Pillow 12.3.0, cryptography 50.0.2). Two programs are LIVE: they read a file the book ships
(Recursion_Chapter1.pdf, demo.docx), which they fetch from nostarch.com on the first run, keep in the system temp folder, check against
its sha256 and copy into a temporary folder before opening (a file whose hash differs stops the program, so the run is refused)."""
__version__ = "1.0.0"
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def run_program(py, code, inputs=(), needs=()):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("BROWSER", None)
    return subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=300)
