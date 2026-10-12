"""Shared by the chapter 13 deck's runner and program check: how a program of this chapter is run, so that the recording and
the re-run are made the same way. A program runs with input() replaced by an echoing function (the shim of chapters 10-12),
with warnings off (as sen0414_ch13_corpus_base_v1_0_0.py runs them), with the Playwright browsers folder the build gives in
CH13_PW_BROWSERS (Playwright finds the Firefox its `playwright install firefox` put there) and with every PATH folder that
holds a chromedriver left out, so that Selenium Manager takes the Firefox route the chapter shows."""
__version__ = "1.0.0"
import os
import subprocess

PRE = "import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print(v)\n    return v\nbuiltins.input = _input\n"


def run_program(py, code, inputs=()):
    env = dict(os.environ)
    if os.environ.get("CH13_PW_BROWSERS"):
        env["PLAYWRIGHT_BROWSERS_PATH"] = os.environ["CH13_PW_BROWSERS"]
    env["PATH"] = os.pathsep.join(d for d in env.get("PATH", "").split(os.pathsep) if not os.path.exists(os.path.join(d, "chromedriver")))
    return subprocess.run([py, "-W", "ignore", "-c", PRE % list(inputs) + code], capture_output=True, text=True, env=env, timeout=300)
