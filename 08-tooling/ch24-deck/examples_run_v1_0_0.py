"""Executes every console session, program, chart and table of examples_v1_0_0.py (chapter 24) under the interpreter given and
writes examples_out_v1_0_0.json. A console session runs row by row in one namespace: a row that evaluates records the repr of its
value (nothing for None), one that is a statement records nothing, one that raises records 'Type: message'. A program runs through
progrun_v1_0_0.run_program, so the transcript is what a student sees; its exit code must be 0 and its transcript must not say NOT EXECUTED
(a program that could not do what it says prints that and the runner refuses to record it). NO PROGRAM PLAYS A SOUND: the machine has no sound card, pyttsx3 writes WAV files and the
programs delete them. Every program, the Cuts a slide shows, is run TWICE here and the runner refuses it unless the two transcripts are equal and every picture it saved is byte-identical
(pixel-identical is accepted at check time, but a Cut whose pictures differ between two runs is not placed on a slide). The pictures that programs save with done() are written to images/
beside this file, and each is listed in the recording with its SHA-256. A chart is the value of its expression after its setup ran (both of this chapter read the transcript of a program from
the recording); a table is the same (the table of environments runs four interpreter rows); the deck check runs the same pair again.
The 15 programs of the research corpus are NOT run here: their record of 14 October 2026 is ch24-page/corpus_run_v1_0_0.json.
Usage: examples_run_v1_0_0.py <python> <out.json>   (RESUME_CHARTS=1 keeps the recorded programs and only computes the consoles, charts and tables again; RERUN=a.py,b.py with it records those programs again)"""
__version__ = "1.0.0"
import hashlib, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import CONSOLES, PROGRAMS, CHARTS, TABLES, KIND, EQUIV, SUBSET, STANDKEY, IMAGES
from progrun_v1_0_0 import run_program
PY, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")

SESSION = r'''
import sys, json
rows = json.loads(sys.argv[1]); ns = {}; out = []
for src in rows:
    try:
        try:
            v = eval(src, ns); got = "" if v is None else repr(v)
        except SyntaxError:
            exec(src, ns); got = ""
    except Exception as e:
        got = "%s: %s" % (type(e).__name__, e)
    out.append([src, got])
print(json.dumps(out))
'''
DATA = r'''
import sys, json
ns = {"HERE": sys.argv[3]}; exec(sys.argv[1], ns); print(json.dumps(eval(sys.argv[2], ns)))
'''


def sh(code, *args):
    env = {k: v for k, v in os.environ.items() if k != "DISPLAY"}
    r = subprocess.run([PY, "-W", "ignore", "-c", code, *args], capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL)
    if r.returncode:
        raise SystemExit("REFUSED: %s" % r.stderr[-400:])
    return r.stdout


if os.environ.get("RESUME_CHARTS") and os.path.exists(OUT):
    # resume: the programs and consoles of an earlier run of this very file are kept as recorded; only the charts and tables are computed again
    out = json.load(open(OUT))
    assert "_programs" in out and "_images" in out, "RESUME_CHARTS needs a recording that holds the programs and the pictures"
    for k, rows in CONSOLES.items():
        out[k] = json.loads(sh(SESSION, json.dumps(rows)))
    for nm in out["_programs"]:
        out["_programs"][nm]["kind"] = KIND[nm]
        out["_programs"][nm]["standkey"] = list(STANDKEY.get(nm, ()))
    for nm in [x for x in os.environ.get("RERUN", "").split(",") if x]:
        # re-record only these programs (the others keep their recording); the code of the examples file is the code of the recording
        code, needs, live = PROGRAMS[nm]
        r = run_program(PY, code, (), needs, keep=IMG)
        r2 = run_program(PY, code, (), needs, keep=IMG)
        if r.returncode or r2.returncode or r.stdout != r2.stdout or "NOT EXECUTED" in r.stdout:
            raise SystemExit("REFUSED: program %s: exits %d/%d or transcripts differ:\n%s\n---\n%s" % (nm, r.returncode, r2.returncode, r.stdout, r2.stdout))
        out["_programs"][nm] = {"code": code, "inputs": [], "needs": list(needs), "transcript": r.stdout.rstrip("\n"), "live": live,
                                "kind": KIND[nm], "exit": 0, "standkey": list(STANDKEY.get(nm, ())), "corpus": False}
        print("  re-ran %-32s exit 0  %s  (twice, equal)" % (nm, KIND[nm]), flush=True)
else:
    out = {"_version": __version__, "_python": sh("import platform;print(platform.python_version())").strip(),
           "_packages": sh("import importlib.metadata as m;print('pyttsx3', m.version('pyttsx3'), '| openai-whisper', m.version('openai-whisper'), '| yt-dlp', m.version('yt-dlp'), '| torch', m.version('torch'), '| NumPy', m.version('numpy'))").strip(),
           "_espeak": subprocess.run(["espeak-ng", "--version"], capture_output=True, text=True).stdout.strip().splitlines()[0],
           "_ffmpeg": subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.strip().splitlines()[0]}
    for k, rows in CONSOLES.items():
        out[k] = json.loads(sh(SESSION, json.dumps(rows)))
    os.makedirs(IMG, exist_ok=True)
    for f in os.listdir(IMG):
        os.remove(os.path.join(IMG, f))
    out["_programs"] = {}
    for name, (code, needs, live) in PROGRAMS.items():
        corpus = False
        r = run_program(PY, code, (), needs, keep=IMG)
        if r.returncode:
            raise SystemExit("REFUSED: program %s exited %d: %s" % (name, r.returncode, (r.stderr or r.stdout)[-400:]))
        bad = [l for l in r.stdout.splitlines() if l.startswith("NOT EXECUTED") or "NOT EXECUTED" in l]
        if bad:
            raise SystemExit("REFUSED: program %s printed NOT EXECUTED: %s" % (name, bad[0][:300]))
        if not corpus:
            first = {f: hashlib.sha256(open(os.path.join(IMG, f), "rb").read()).hexdigest() for f in os.listdir(IMG)}
            r2 = run_program(PY, code, (), needs, keep=IMG)
            if r2.returncode or r2.stdout != r.stdout:
                raise SystemExit("REFUSED: program %s printed different transcripts in two runs:\n%s\n---\n%s" % (name, r.stdout, r2.stdout))
            for f, h in first.items():
                if hashlib.sha256(open(os.path.join(IMG, f), "rb").read()).hexdigest() != h and f in IMAGES and IMAGES[f] == name:
                    raise SystemExit("REFUSED: program %s saved a different %s in its second run" % (name, f))
        out["_programs"][name] = {"code": code, "inputs": [], "needs": list(needs), "transcript": r.stdout.rstrip("\n"), "live": live,
                                  "kind": KIND[name], "exit": r.returncode, "standkey": list(STANDKEY.get(name, ())), "corpus": corpus}
        print("  ran %-34s exit %d  %s  (twice, equal)" % (name, r.returncode, KIND[name]), flush=True)
    out["_images"] = {}
    for fn, prog in IMAGES.items():
        p = os.path.join(IMG, fn)
        if not os.path.exists(p):
            raise SystemExit("REFUSED: program %s did not save %s" % (prog, fn))
        b = open(p, "rb").read()
        out["_images"][fn] = {"program": prog, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
        if hashlib.sha256(b).hexdigest()[:12] not in out["_programs"][prog]["transcript"]:
            raise SystemExit("REFUSED: the transcript of %s does not print the hash of %s" % (prog, fn))
    extra = sorted(set(os.listdir(IMG)) - set(IMAGES))
    if extra:
        raise SystemExit("REFUSED: pictures saved but not placed: %r" % extra)
    json.dump(out, open(OUT, "w"), indent=1)

out["_charts"], out["_tables"] = {}, {}
for k, c in CHARTS.items():
    pairs = json.loads(sh(DATA, c["setup"], c["expr"], HERE))
    out["_charts"][k] = {"setup": c["setup"], "expr": c["expr"], "labels": [p[0] for p in pairs], "values": [float(p[1]) for p in pairs]}
for k, t in TABLES.items():
    out["_tables"][k] = {"setup": t["setup"], "expr": t["expr"], "rows": json.loads(sh(DATA, t["setup"], t["expr"], HERE))}
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", sum(len(v) for k, v in out.items() if k in CONSOLES), "console rows,",
      len(out["_programs"]), "programs, all exit 0,", len(out["_images"]), "pictures,", len(out["_charts"]), "chart(s),", len(out["_tables"]), "table(s)")
