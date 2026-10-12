"""Shared by the chapter 16 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with warnings off (as sen0414_ch16_corpus_base_v1_0_0.py runs them), with PYTHONPATH
removed and with its own temporary folder as the working directory (every program's first lines do os.chdir(tempfile.mkdtemp())).
The interpreter given is the uv Python 3.14.6 of this chapter's build (/home/claude/venv314), whose sqlite3 module links SQLite 3.53.1;
the standard library is all a program needs. Two programs are LIVE: they read the book's own database sweigartcats.db, which they
fetch from nostarch.com on the first run, keep in the system temp folder, check against a sha256 beginning 41f0d0b5bc2e and copy
into a temporary folder before opening (a file whose hash differs stops the program, so the run is refused)."""
__version__ = "1.0.0"
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def run_program(py, code, inputs=(), needs=()):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("BROWSER", None)
    return subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=300)
