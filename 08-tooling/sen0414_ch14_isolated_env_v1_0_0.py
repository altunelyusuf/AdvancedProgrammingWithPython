#!/usr/bin/env python3
"""The isolated environment in which the executed claims of chapter 14 (Excel Spreadsheets) run (new file, 2026-10-27, TK_Ret_Ch14_Research).

Why it exists: the claims of the chapter's data module were recorded under Python 3.14.6 with openpyxl 3.1.5 as the only package installed
beside Python (the chapter's own premise: no Pillow, no defusedxml, no lxml). The execution checks run each claim under whatever
python3.14 is on the path of the machine that runs them; on a machine whose python3.14 has no openpyxl, 97 of 108 claims fail with
ModuleNotFoundError, and on a machine whose python3.14 has Pillow or defusedxml the claims about their absence would fail. So the claims
carry their own environment: this module builds, once per machine and per Python, a virtual environment that holds openpyxl 3.1.5 and
et_xmlfile 2.0.0 and nothing else (it does not see the packages of the interpreter that built it), installs both from the wheels
committed in 03-materials/ch14/assets (no network), checks the result, and runs the claim's code in it.

The code of a claim is not changed: out(code) runs exec(code, {}) and prints repr of the variable out, exactly what the checks
did in the interpreter itself; run(code) runs a behaviour's code with the same flags the checks use and passes its output and exit code on.
Public functions:
  python()  -> path of the environment's interpreter (built on first use)
  out(code) -> a value whose repr is the repr of the variable out after running code in the environment
  run(code) -> runs code in the environment; its stdout and stderr are passed on and the process exits with its exit code
  describe() -> the environment's package list, for the record"""
__version__ = "1.0.0"
import fcntl, hashlib, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "03-materials", "ch14", "assets")
WHEELS = ["et_xmlfile-2.0.0-py3-none-any.whl", "openpyxl-3.1.5-py2.py3-none-any.whl"]
PINS = ["et_xmlfile==2.0.0", "openpyxl==3.1.5"]
WANT = {"et-xmlfile": "2.0.0", "openpyxl": "3.1.5"}


def _digest():
    h = hashlib.sha256()
    for w in WHEELS:
        h.update(open(os.path.join(ASSETS, w), "rb").read())
    h.update(sys.version.encode())
    return h.hexdigest()[:16]


def _packages(py):
    r = subprocess.run([py, "-m", "pip", "list", "--format=freeze"], capture_output=True, text=True)
    return {l.split("==")[0].lower().replace("_", "-"): l.split("==")[1] for l in r.stdout.split() if "==" in l}


def _build(target):
    part = target + ".partial"
    shutil.rmtree(part, ignore_errors=True)
    subprocess.run([sys.executable, "-m", "venv", part], check=True, capture_output=True)
    py = os.path.join(part, "bin", "python")
    cmd = [py, "-m", "pip", "install", "--no-index", "--find-links", ASSETS, "--no-deps", "--disable-pip-version-check"] + PINS
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError("the isolated environment could not be built from the committed wheels: " + r.stderr[-400:])
    got = _packages(py)
    got.pop("pip", None)
    if got != WANT:
        raise RuntimeError("the isolated environment holds %s, expected %s" % (got, WANT))
    v = subprocess.run([py, "-c", "import openpyxl; print(openpyxl.__version__)"], capture_output=True, text=True).stdout.strip()
    if v != "3.1.5":
        raise RuntimeError("openpyxl in the isolated environment reports %r" % v)
    shutil.rmtree(target, ignore_errors=True)
    os.rename(part, target)
    # a virtual environment records its own location in its scripts only; the interpreter is found through pyvenv.cfg, so the rename is safe
    open(os.path.join(target, "READY"), "w").write("openpyxl 3.1.5, et_xmlfile 2.0.0; Python %s\n" % sys.version.split()[0])


def python():
    target = os.path.join(tempfile.gettempdir(), "sen0414_ch14_env_" + _digest())
    py = os.path.join(target, "bin", "python")
    if os.path.exists(os.path.join(target, "READY")) and os.path.exists(py):
        return py
    with open(target + ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        if not (os.path.exists(os.path.join(target, "READY")) and os.path.exists(py)):
            _build(target)
    return py


def describe():
    py = python()
    return "interpreter %s\n%s" % (py, subprocess.run([py, "-m", "pip", "list"], capture_output=True, text=True).stdout)


class _Raw(str):
    def __repr__(self):
        return str.__str__(self)


_OUT = "g = {}\nexec(%s, g)\nprint(repr(g['out']))"


def out(code):
    r = subprocess.run([python(), "-c", _OUT % repr(code)], capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr)
        sys.exit(1)
    return _Raw(r.stdout.strip())


def run(code):
    r = subprocess.run([python(), "-W", "ignore::SyntaxWarning", "-c", code], capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    sys.exit(r.returncode)


if __name__ == "__main__":
    print(describe())
