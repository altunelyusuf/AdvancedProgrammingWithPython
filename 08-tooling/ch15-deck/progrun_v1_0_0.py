"""Shared by the chapter 15 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with input() replaced by an echoing function (the shim of chapters 10-14), with
warnings off (as sen0414_ch15_corpus_base_v1_0_0.py runs them), with PYTHONPATH removed and with CH15_FIX set to the folder of the
two committed CSV exports (08-tooling/ch15-page/fixtures) that the three fixture-based programs read. The interpreter given must
hold ezsheets, google-api-python-client and httplib2 (the interpreter of this chapter's build is /home/claude/venv314_ezsheets,
Python 3.14.6, ezsheets 2026.4.28). No program reaches Google or the network: the programs that open a spreadsheet run against the
stand-in class G that their first lines define."""
__version__ = "1.0.0"
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.normpath(os.path.join(HERE, "..", "ch15-page", "fixtures"))
PRE = "import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print(v)\n    return v\nbuiltins.input = _input\n"


def run_program(py, code, inputs=(), needs=()):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env["CH15_FIX"] = FIX
    env.pop("BROWSER", None)
    return subprocess.run([py, "-W", "ignore", "-c", PRE % list(inputs) + code], capture_output=True, text=True, env=env, timeout=300)
