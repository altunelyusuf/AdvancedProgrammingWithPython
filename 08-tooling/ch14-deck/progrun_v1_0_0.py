"""Shared by the chapter 14 deck's runner and program check: how a program of this chapter is run, so that the recording and the
re-run are made the same way. A program runs with input() replaced by an echoing function (the shim of chapters 10-13), with
warnings off (as sen0414_ch14_corpus_base_v1_0_0.py runs them), and, when it names a package that is not part of the interpreter
(requests for the program that downloads example3.xlsx, defusedxml for the one that loads an entity bomb), with the folder that
holds that package put on PYTHONPATH for that program only. The folders are given by CH14_EXTRA, joined by the path separator, as
sen0414_ch14_corpus_base_v1_0_0.py takes them; openpyxl 3.1.5 is installed in the interpreter itself."""
__version__ = "1.0.0"
import os
import subprocess

PRE = "import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print(v)\n    return v\nbuiltins.input = _input\n"


def run_program(py, code, inputs=(), needs=()):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    if any(n in ("requests", "defusedxml") for n in needs) and os.environ.get("CH14_EXTRA"):
        env["PYTHONPATH"] = os.environ["CH14_EXTRA"]
    return subprocess.run([py, "-W", "ignore", "-c", PRE % list(inputs) + code], capture_output=True, text=True, env=env, timeout=300)
