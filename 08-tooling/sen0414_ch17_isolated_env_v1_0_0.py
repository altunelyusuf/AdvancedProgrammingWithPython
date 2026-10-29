#!/usr/bin/env python3
"""The isolated environment in which the executed claims of chapter 17 (PDF and Word Documents) run (new file, 2026-10-29, TK_Ret_Ch17_Research).

Why it exists: the claims of the chapter's data module were recorded under Python 3.14.6 with pypdf 6.20.1, python-docx 1.2.0, pdfminer.six 20260107, Pillow 12.3.0, cryptography 50.0.2
and lxml 6.1.3 installed. The execution checks run each claim under whatever python3.14 is on the path of the machine that runs them; on a machine whose python3.14 has none of these
packages every claim fails with ModuleNotFoundError: No module named 'pypdf' (the controller's pre-run of 2026-10-25), and a machine whose python3.14 holds other versions would print other
versions. So the claims carry their own environment: this module builds, once per machine and per Python, a virtual environment that holds the 10 pinned packages below and nothing else
(it does not see the packages of the interpreter that built it), installs them with no network from the wheels committed in 03-materials/ch17/assets (pypdf and python-docx, as before)
and 03-materials/ch17/assets/env_wheels_v1_0_0 (the other eight, ASSETS_PROVENANCE_v1_0_2.md), refuses a wheel whose SHA-256 differs from the one recorded here, checks the installed list
against the pins and pip check, and runs the claim's code in it. Four of the wheels are built for Linux x86_64 (cffi, cryptography, lxml, Pillow); on another platform the builder stops with a
message saying so, and the claims then reproduce on Linux x86_64 only.

The code of a claim is not changed: out(code) runs exec(code, {}) and prints repr of the variable out, exactly what the checks did in the interpreter itself; run(code) runs a
behaviour's code with the same flags the checks use and passes its output and exit code on. Time limits are not part of this module; a claim that waits is the claim's own.
Public functions:
  python()  -> path of the environment's interpreter (built on first use)
  out(code) -> a value whose repr is the repr of the variable out after running code in the environment
  run(code) -> runs code in the environment; its stdout and stderr are passed on and the process exits with its exit code
  describe() -> the environment's package list, for the record"""
__version__ = "1.0.0"
import fcntl, hashlib, os, platform, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "03-materials", "ch17", "assets")
EXTRA = os.path.join(ASSETS, "env_wheels_v1_0_0")
SHA256 = {'pypdf-6.20.1-py3-none-any.whl': 'aa5a55ddcffdc5e5ab291d5decb23f6383f4e56f8e3263dc39af41fff03885ad', 'python_docx-1.2.0-py3-none-any.whl': '3fd478f3250fbbbfd3b94fe1e985955737c145627498896a8a6bf81f4baf66c7', 'cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl': 'b0431303acaea1089ad4b3e9ce4e6518193def1118d4073ca848635ee4ea2e96', 'charset_normalizer-3.5.2-py3-none-any.whl': 'b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685', 'cryptography-50.0.2-cp311-abi3-manylinux_2_34_x86_64.whl': '9dab55f57c74c3cad24c323bacbbd04be4705ba6eb0d92e920b1fc4837ed5079', 'lxml-6.1.3-cp314-cp314-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl': 'a7eb78ba28b187e1e9203a55c60fcf70df2d22cb205fe6d51b9383d6097419f0', 'pdfminer_six-20260107-py3-none-any.whl': '366585ba97e80dffa8f00cebe303d2f381884d8637af4ce422f1df3ef38111a9', 'pillow-12.3.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl': '251bf95b67017e27b13d82f5b326234ca62d70f9cf4c2b9032de2358a3b12c7b', 'pycparser-3.12-py3-none-any.whl': 'a076f3f489b39b43ed13563a1dafe42447445bec2e294154ec5c57fcdda4c85e', 'typing_extensions-4.16.0-py3-none-any.whl': '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8'}
PINS = ['cffi==2.1.1', 'charset-normalizer==3.5.2', 'cryptography==50.0.2', 'lxml==6.1.3', 'pdfminer.six==20260107', 'pillow==12.3.0', 'pycparser==3.12', 'pypdf==6.20.1', 'python-docx==1.2.0', 'typing-extensions==4.16.0']
WANT = dict(p.split("==") for p in PINS)


def _digest():
    h = hashlib.sha256()
    for w in sorted(SHA256):
        h.update(w.encode()); h.update(SHA256[w].encode())
    h.update(sys.version.encode())
    return h.hexdigest()[:16]


def _wheel_path(w):
    for d in (ASSETS, EXTRA):
        p = os.path.join(d, w)
        if os.path.exists(p):
            return p
    raise RuntimeError("wheel %s is not in %s or %s" % (w, ASSETS, EXTRA))


def _packages(py):
    r = subprocess.run([py, "-m", "pip", "list", "--format=freeze"], capture_output=True, text=True)
    return {l.split("==")[0].lower().replace("_", "-"): l.split("==")[1] for l in r.stdout.split() if "==" in l}


def _build(target):
    if not (sys.platform == "linux" and platform.machine() == "x86_64"):
        raise RuntimeError("the committed wheels of cffi, cryptography, lxml and Pillow are for Linux x86_64; this machine is %s %s" % (sys.platform, platform.machine()))
    for w, want in SHA256.items():
        got = hashlib.sha256(open(_wheel_path(w), "rb").read()).hexdigest()
        if got != want:
            raise RuntimeError("wheel %s has SHA-256 %s, recorded %s" % (w, got, want))
    part = target + ".partial"
    shutil.rmtree(part, ignore_errors=True)
    subprocess.run([sys.executable, "-m", "venv", part], check=True, capture_output=True)
    py = os.path.join(part, "bin", "python")
    cmd = [py, "-m", "pip", "install", "--no-index", "--no-deps", "--disable-pip-version-check"] + [_wheel_path(w) for w in sorted(SHA256)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError("the isolated environment could not be built from the committed wheels: " + r.stderr[-400:])
    got = _packages(py)
    got.pop("pip", None)
    if got != WANT:
        raise RuntimeError("the isolated environment holds %s, expected %s" % (got, WANT))
    chk = subprocess.run([py, "-m", "pip", "check"], capture_output=True, text=True)
    if chk.returncode:
        raise RuntimeError("pip check on the isolated environment: " + chk.stdout[-400:])
    v = subprocess.run([py, "-c", "import pypdf, docx, pdfminer, PIL, cryptography, lxml.etree; print(pypdf.__version__, pdfminer.__version__, PIL.__version__, cryptography.__version__)"], capture_output=True, text=True).stdout.strip()
    if v != "6.20.1 20260107 12.3.0 50.0.2":
        raise RuntimeError("the libraries in the isolated environment report %r" % v)
    shutil.rmtree(target, ignore_errors=True)
    os.rename(part, target)
    # a virtual environment records its own location in its scripts only; the interpreter is found through pyvenv.cfg, so the rename is safe
    open(os.path.join(target, "READY"), "w").write("pypdf 6.20.1, python-docx 1.2.0, pdfminer.six 20260107, Pillow 12.3.0, cryptography 50.0.2, lxml 6.1.3 and 4 more pinned packages; Python %s\n" % sys.version.split()[0])


def python():
    target = os.path.join(tempfile.gettempdir(), "sen0414_ch17_env_" + _digest())
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


_OUT = "g = {}\nexec(%s, g)\nprint(repr(g['out']))"


class _Raw(str):
    def __repr__(self):
        return str.__str__(self)


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
