"""Shared by the chapter 20 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with warnings off (as sen0414_ch20_corpus_base_v1_0_0.py runs them), with PYTHONPATH
removed and with its own temporary folder as the working directory (programs that write files call wd(), which makes one). The
interpreter given is the uv Python 3.14.6 of the chapter 20 research environment (/home/claude/venv314_ch20_latest: ezgmail 2026.4.28,
requests 2.34.2, aiosmtpd 1.4.6, cryptography, google-api-python-client 2.201.0, oauth2client 4.1.3). NO PROGRAM OF THIS CHAPTER REACHES A REAL
SERVICE: the programs that need a server run against a local stand-in on 127.0.0.1 (aiosmtpd for SMTP, a replacement of the HTTP layer of the Google client
library for Gmail, a recorder for ntfy), the others need none; see examples_v1_0_0.py. Moments are made from numbers and zones are named, so a re-run
prints the same text on any day."""
__version__ = "1.0.0"
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def run_program(py, code, inputs=(), needs=()):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("BROWSER", None)
    return subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=300)
