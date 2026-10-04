"""Executes every shell session and every whole program of an examples module under the interpreter given, and writes the
result as JSON, so that a slide can only ever show output that Python really produced.

A session is run exactly the way ch02-deck/deck_check_v1_0_1.py re-runs it from the finished slides: one namespace per
session, each line evaluated, a statement executed and recorded as null, an exception recorded as 'Name: message'. A
session line that PRINTS instead of evaluating is refused, because the deck check compares the printed form with the
value and would reject the slide; printing belongs in a program, not in a session.

A program is run with input() replaced by a function that echoes the prompt and the typed line, so the transcript on the
slide is the transcript a student sees. The shape of the output file ('_programs' -> name -> {code, runs}) is the one
ch03-deck/program_check_v1_0_0.py reads, so that check re-runs every program against the finished deck unchanged.

2.1.0 adds programs that are MEANT to fail. Chapter 2 and chapter 3 both teach by showing what Python prints when a
program is wrong - an unassigned name, a program that stops itself with sys.exit - and such a program exits with a
status that 2.0.0 refused. A program whose entry carries a third element "mayfail" may exit with any status, and its
error output is recorded line by line so that the slide can show the real message; program_fail_check_v1_0_0.py then
re-runs those programs against the finished deck.
2.0.0 generalised ch06-deck/examples_run_v1_0_0.py, which could only import one fixed module name, into a runner that
takes the examples module as an argument and is therefore shared by the chapter 1, 2 and 3 deck folders.
Usage: examples_run_v2_1_0.py <python> <examples_module.py> <out.json>
"""
__version__ = "2.1.0"
import importlib.util, json, os, subprocess, sys, tempfile

TMP = tempfile.mkdtemp(prefix="sen0414_programs_")

PY, MOD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
_spec = importlib.util.spec_from_file_location("_examples", os.path.abspath(MOD))
_ex = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_ex)
EX, PROGRAMS = _ex.EX, getattr(_ex, "PROGRAMS", {})

SESSION = """import contextlib, io, json, sys
ns = {}; out = []
for src in json.loads(sys.argv[1]):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            try: got = repr(eval(src, ns))
            except SyntaxError: exec(src, ns); got = None
    except BaseException as e: got = '%s: %s' % (type(e).__name__, e)
    assert not buf.getvalue(), ('a session line printed; put it in a program instead', src)
    out.append([src, got])
print(json.dumps(out))
"""
PRE = ("import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print('\\x01' + prompt + '\\x02' + v + '\\x03')\n"
       "    return v\nbuiltins.input = _input\n")

out = {"_version": __version__,
       "_python": subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip(),
       "_examples": os.path.basename(MOD)}
for k, lines in EX.items():
    r = subprocess.run([PY, "-c", SESSION, json.dumps(lines)], capture_output=True, text=True)
    assert r.returncode == 0, (k, r.stderr[-800:])
    out[k] = json.loads(r.stdout)
    assert out[k][-1][1] is not None, ("a session must end with an expression, so the card ends with a value", k)
out["_programs"] = {}
for name, entry in PROGRAMS.items():
    code, runs = entry[0], entry[1]
    mayfail = len(entry) > 2 and entry[2] == "mayfail"
    rec = {"code": code, "runs": [], "mayfail": mayfail}
    for inputs in runs:
        # a program that needs no typed input is run from a real file named after itself, so that the file name and the
        # line numbers in any error report are the ones a student would see; a program that reads input is run with -c,
        # with input() replaced, which is also how ch03-deck/program_check_v1_0_0.py re-runs it
        if inputs:
            r = subprocess.run([PY, "-c", PRE % inputs + code], capture_output=True, text=True, timeout=60)
        else:
            open(os.path.join(TMP, name), "w").write(code)
            r = subprocess.run([PY, name], capture_output=True, text=True, timeout=60, cwd=TMP)
        raw = r.stdout.rstrip("\n")
        lines = []
        for ln in raw.split("\n"):
            if "\x01" in ln:
                pr, rest = ln.replace("\x01", "").split("\x02", 1); lines.append([[pr, False], [rest.replace("\x03", ""), True]])
            else: lines.append([[ln, False]])
        err = [l for l in r.stderr.rstrip("\n").split("\n") if l.strip()]
        rec["runs"].append({"inputs": inputs, "transcript": raw.replace("\x01", "").replace("\x02", "").replace("\x03", ""),
                            "lines": lines, "exit": r.returncode, "stderr": r.stderr.strip(), "errlines": err,
                            "errlast": err[-1] if err else ""})
        assert mayfail or r.returncode == 0, (name, inputs, r.stderr[-400:])
        assert not mayfail or r.returncode != 0, (name, inputs, "declared mayfail but exited cleanly")
    out["_programs"][name] = rec
json.dump(out, open(OUT, "w"), indent=1, ensure_ascii=False)
print("written", OUT, "-", len(EX), "sessions,", sum(len(v) for k, v in EX.items()), "session lines,",
      len(out["_programs"]), "programs (", sum(1 for r in out["_programs"].values() if r["mayfail"]), "of them expected to fail ),",
      sum(len(r["runs"]) for r in out["_programs"].values()), "program runs, under Python", out["_python"])
