#!/usr/bin/env python3
"""The isolated environment in which the executed claims of chapter 15 (Google Sheets) run (new file, 2026-10-27, TK_Ret_Ch15_Research).

Why it exists: the claims of the chapter's data module were recorded under Python 3.14.6 with ezsheets 2026.4.28, google-api-python-client 2.201.0, google-auth 2.61.0
and the packages that go with them installed. The execution checks run each claim under whatever python3.14 is on the path of the machine that runs them; on a machine whose
python3.14 has none of these packages the claims that use the library fail with ModuleNotFoundError, and a machine whose python3.14 holds other versions would print other versions.
So the claims carry their own environment: this module builds, once per machine and per Python, a virtual environment that holds the 26 pinned packages below and nothing else
(it does not see the packages of the interpreter that built it), installs them with no network from the wheels committed in 03-materials/ch15/assets (the 14 wheels of
ASSETS_PROVENANCE_v1_0_0.md) and 03-materials/ch15/assets/env_wheels_v1_0_0 (the 12 of ASSETS_PROVENANCE_v1_0_2.md), refuses a wheel whose SHA-256 differs from the one recorded
here, checks the installed list against the pins, and runs the claim's code in it. Three of the wheels are built for Linux x86_64 (cffi, cryptography, protobuf); on another
platform the builder stops with a message saying so.

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
ASSETS = os.path.join(os.path.dirname(HERE), "03-materials", "ch15", "assets")
EXTRA = os.path.join(ASSETS, "env_wheels_v1_0_0")
SHA256 = {'ezsheets-2026.4.28-py3-none-any.whl': 'd6680fc5095fce09feda754ca430eb710dcec41728b665fdaea7326fcdf95ea3', 'google_api_core-2.42.0-py3-none-any.whl': 'b1bdf4f72dc4f910736ce4ba49038352effbbc309579215107649b22973a1317', 'google_api_python_client-2.201.0-py3-none-any.whl': '4b2de61537fd1e48c6ade72ac630d09a8139f9ac72bd70cf145e0d4ad7fe70ae', 'google_auth-2.61.0-py3-none-any.whl': 'ca60266a37475ae68b63bac007272f46094b3d571abe92aded329b6cfb568025', 'google_auth_httplib2-0.4.4-py3-none-any.whl': 'bbe5d7b2401bb3a4017f4720e1e91bd273ab9a2bb60b84e65edbc0de127852da', 'google_auth_oauthlib-1.5.0-py3-none-any.whl': '71625fdea21c6c03217eb9ff13741c3096e6d257ebca0ad084dbd6e9f4aa4ef4', 'googleapis_common_protos-1.75.5-py3-none-any.whl': 'd7285525c23039db98f2463e6d5a4f9b958b94d497f03a844ece3259c4e72d5d', 'httplib2-0.32.0-py3-none-any.whl': 'dc6705cacdf3fb0a2aba7629fa33c90fd93e30035db0c157325826be177e4816', 'oauthlib-4.0.0-py3-none-any.whl': '624c28c13a0a59cabf9747dfa52af63be3e512a7f2714df16e91b5b3a145e6cd', 'proto_plus-1.29.0-py3-none-any.whl': '8acd070469a7aaf43f440b022ef9757c8cac1a9f866e933f59ae98669ddc6c8b', 'pyasn1-0.6.4-py3-none-any.whl': 'deda9277cfd454080ec40b207fb6df82206a3a2688735233cdcd8d3d565f088b', 'pyasn1_modules-0.4.2-py3-none-any.whl': '29253a9207ce32b64c3ac6600edc75368f98473906e8fd1043bd6b5b1de2c14a', 'requests_oauthlib-2.0.0-py2.py3-none-any.whl': '7dd8a5c40426b779b0868c404bdef9768deccf22749cde15852df527e6269b36', 'uritemplate-4.2.0-py3-none-any.whl': '962201ba1c4edcab02e60f9a0d3821e82dfc5d2d6662a21abd533879bdb8a686', 'certifi-2026.10.23-py3-none-any.whl': 'e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1', 'cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl': 'b0431303acaea1089ad4b3e9ce4e6518193def1118d4073ca848635ee4ea2e96', 'charset_normalizer-3.5.2-py3-none-any.whl': 'b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685', 'cryptography-50.0.2-cp311-abi3-manylinux_2_34_x86_64.whl': '9dab55f57c74c3cad24c323bacbbd04be4705ba6eb0d92e920b1fc4837ed5079', 'idna-3.20-py3-none-any.whl': 'ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c', 'opentelemetry_api-1.45.1-py3-none-any.whl': 'b31553efa588ae44bc306f863c785c5333a9ecc091248c6ee68b4b6c87fdedfb', 'protobuf-7.36.2-cp310-abi3-manylinux2014_x86_64.whl': '89f23aa53c24553a2416fd4fd1ec06f74fa42b14b546d8883128813f775bbfd2', 'pycparser-3.12-py3-none-any.whl': 'a076f3f489b39b43ed13563a1dafe42447445bec2e294154ec5c57fcdda4c85e', 'pyparsing-3.3.3-py3-none-any.whl': 'ece8c00a69cf01b45d0b1dedabb469c90d8caf996d4fda40f147627a122849a4', 'requests-2.34.2-py3-none-any.whl': '2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0', 'typing_extensions-4.16.0-py3-none-any.whl': '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8', 'urllib3-2.8.0-py3-none-any.whl': '0cf3cae568d36aa9576b28dfb35f11328f1cb974ca7647d9475ebb86c75ac6e3'}
PINS = ['certifi==2026.10.23', 'cffi==2.1.1', 'charset-normalizer==3.5.2', 'cryptography==50.0.2', 'ezsheets==2026.4.28', 'google-api-core==2.42.0', 'google-api-python-client==2.201.0', 'google-auth==2.61.0', 'google-auth-httplib2==0.4.4', 'google-auth-oauthlib==1.5.0', 'googleapis-common-protos==1.75.5', 'httplib2==0.32.0', 'idna==3.20', 'oauthlib==4.0.0', 'opentelemetry-api==1.45.1', 'proto-plus==1.29.0', 'protobuf==7.36.2', 'pyasn1==0.6.4', 'pyasn1-modules==0.4.2', 'pycparser==3.12', 'pyparsing==3.3.3', 'requests==2.34.2', 'requests-oauthlib==2.0.0', 'typing-extensions==4.16.0', 'uritemplate==4.2.0', 'urllib3==2.8.0']
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
        raise RuntimeError("the committed wheels of cffi, cryptography and protobuf are for Linux x86_64; this machine is %s %s" % (sys.platform, platform.machine()))
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
    v = subprocess.run([py, "-c", "import ezsheets, googleapiclient, google.auth, httplib2; print(ezsheets.__version__)"], capture_output=True, text=True).stdout.strip()
    if v != "2026.4.28":
        raise RuntimeError("ezsheets in the isolated environment reports %r" % v)
    shutil.rmtree(target, ignore_errors=True)
    os.rename(part, target)
    # a virtual environment records its own location in its scripts only; the interpreter is found through pyvenv.cfg, so the rename is safe
    open(os.path.join(target, "READY"), "w").write("ezsheets 2026.4.28 and 25 pinned packages; Python %s\n" % sys.version.split()[0])


def python():
    target = os.path.join(tempfile.gettempdir(), "sen0414_ch15_env_" + _digest())
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
