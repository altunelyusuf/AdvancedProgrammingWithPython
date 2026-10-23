#!/usr/bin/env python3
"""Own key-substituting driver (not the runner repair). Usage: drive_test.py NN TESTVER(9_34_0|9_36_0) PAGEFILE DATA_JSON WORKDIR
Builds a scratch mirror of the repository (symlinks) so the test finds page_data_v9_90_0.json for the scratch page, replaces the exam-release public key in a COPY of the page with a TEST key, runs the named test file, prints its tail."""
import json, os, subprocess, sys, shutil, base64
from cryptography.hazmat.primitives.asymmetric import ec
n, tv, page, data, work = sys.argv[1:6]
REPO = "/home/claude/AdvancedProgrammingWithPython"
os.makedirs(work, exist_ok=True)
M = os.path.join(work, "mirror"); shutil.rmtree(M, ignore_errors=True)
os.makedirs(os.path.join(M, "08-tooling")); os.makedirs(os.path.join(M, "03-materials"))
for e in os.listdir(os.path.join(REPO, "03-materials")):
    if e != "ch%s" % n: os.symlink(os.path.join(REPO, "03-materials", e), os.path.join(M, "03-materials", e))
mc = os.path.join(M, "03-materials", "ch%s" % n); os.makedirs(mc)
for e in os.listdir(os.path.join(REPO, "03-materials", "ch%s" % n)):
    if e != "page": os.symlink(os.path.join(REPO, "03-materials", "ch%s" % n, e), os.path.join(mc, e))
mp = os.path.join(mc, "page"); os.makedirs(mp)
for e in os.listdir(os.path.join(REPO, "03-materials", "ch%s" % n, "page")): os.symlink(os.path.join(REPO, "03-materials", "ch%s" % n, "page", e), os.path.join(mp, e))
if os.environ.get("CC_FIXTURE"): shutil.copy(os.environ["CC_FIXTURE"], os.path.join(mp, "chapter_code_ch%s_v0_0_1.json" % n))   # the scratch manifest the page was built with, where the test looks for the deck's manifest
for e in os.listdir(os.path.join(REPO, "08-tooling")):
    if e != "ch%s-page" % n: os.symlink(os.path.join(REPO, "08-tooling", e), os.path.join(M, "08-tooling", e))
cp = os.path.join(M, "08-tooling", "ch%s-page" % n); os.makedirs(cp)
for e in os.listdir(os.path.join(REPO, "08-tooling", "ch%s-page" % n)): os.symlink(os.path.join(REPO, "08-tooling", "ch%s-page" % n, e), os.path.join(cp, e))
shutil.copy(data, os.path.join(cp, "page_data_v9_90_0.json"))
b64u = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode()
key = ec.generate_private_key(ec.SECP256R1()); num = key.private_numbers(); pub = num.public_numbers
jwk = {"kty": "EC", "crv": "P-256", "d": b64u(num.private_value.to_bytes(32, "big")), "x": b64u(pub.x.to_bytes(32, "big")), "y": b64u(pub.y.to_bytes(32, "big"))}
json.dump({"private_jwk": jwk, "note": "TEST-ONLY key"}, open(os.path.join(work, "test_key.json"), "w"))
A, B = ("_zsDxa14DjwKPcKRIclVIdm2WzU5KQJ4mFfSc4K7Fwc", "C112ODgH30Twsw-Lrzvb4YQHF8wRpe8Iqo1KuiSIqvk")
s = open(page, encoding="utf-8").read(); assert A in s and B in s
pf = os.path.join(work, "sen0414_ch%s_page_v9_90_0.html" % n)
open(pf, "w", encoding="utf-8").write(s.replace(A, jwk["x"]).replace(B, jwk["y"]))
# the test measures the load task against the previously shipped page found beside the page under test: put the shipped v9_28_0 page there as the control
shutil.copy(os.path.join(REPO, "03-materials", "ch%s" % n, "page", "sen0414_ch%s_page_v9_28_0.html" % n), os.path.join(work, "sen0414_ch%s_page_v9_28_0.html" % n))
env = dict(os.environ, PAGE=pf, RESULTS=os.path.join(work, "results.json"), PAGE_VER="9_90_0", KEY=os.path.join(work, "test_key.json"), PYTHONDONTWRITEBYTECODE="1")
env.pop("FORCE_STANDARD", None)
print("page tested:", page, "| test:", tv, "| data:", data, flush=True)
r = subprocess.run(["/home/claude/venv314/bin/python", os.path.join(M, "08-tooling", "sen0414_page_test_v%s.py" % tv), n], env=env, cwd=M)
print("EXIT", r.returncode)
sys.exit(r.returncode)
