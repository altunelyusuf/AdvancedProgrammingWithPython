"""Builds the chapter 5 visual specifications by EXECUTING code under the interpreter it is run with. A specification is data: the same
file is drawn as native shapes by the deck and as SVG or HTML by the page, so a slide and the page can never show different values.
Nothing in the output is typed by hand: the trace records what a real run did pass by pass; the debugger record is a line event stream
of a real run (line, call depth, the variables and the call stack at each stop, the text printed so far); the logging matrix is what real
subprocesses printed at each setting; the unwinding record is the frames of a real traceback; the tracebacks are the text a real
interpreter wrote to standard error.
Usage: visuals_make_v1_0_0.py <out.json>   (run under the Python the course teaches)"""
__version__ = "1.0.0"
import contextlib, io, json, logging, os, platform, subprocess, sys, tempfile, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import PROGRAMS
PY = sys.executable

def trace(code, mark, watch, labels, start):
    """One pass begins at the line containing `start`; the variables are noted when the line containing `mark` is about to run."""
    lines = code.split("\n")
    def find(sub):
        hits = [i + 1 for i, l in enumerate(lines) if sub in l]; assert hits, sub; return hits[0]
    mline = find(mark); sline = find(start); lab = {find(k): v for k, v in labels.items()}
    logging.root.handlers[:] = []
    buf = io.StringIO(); passes = []; cur = [None]
    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<prog>": return None
        if event == "line":
            if frame.f_lineno == sline:
                if cur[0] is not None: cur[0]["out_end"] = buf.tell()
                cur[0] = {"vals": None, "events": [], "out_start": buf.tell(), "out_end": None}; passes.append(cur[0])
            if frame.f_lineno == mline and cur[0] is not None and cur[0]["vals"] is None:
                cur[0]["vals"] = [repr(frame.f_locals[w]) if w in frame.f_locals else "" for w in watch]
            elif cur[0] is not None and frame.f_lineno in lab: cur[0]["events"].append(lab[frame.f_lineno])
        return tracer
    g = {"__name__": "__main__"}
    try:
        sys.settrace(tracer)
        with contextlib.redirect_stdout(buf): exec(compile(code, "<prog>", "exec"), g)
    finally: sys.settrace(None)
    if cur[0] is not None and cur[0]["out_end"] is None: cur[0]["out_end"] = buf.tell()
    text = buf.getvalue(); rows = []
    for i, p in enumerate(passes):
        rows.append({"n": i + 1, "vals": p["vals"], "cond": None, "events": p["events"], "out": text[p["out_start"]:p["out_end"]].rstrip("\n").replace("\n", " / ")})
    logging.root.handlers[:] = []
    return {"inputs": [], "rows": rows, "printed": text.rstrip("\n").replace("\n", " / ")}

def t_spec(code, mark, watch, labels, caption, start):
    return {"kind": "trace", "style": "table", "code": code, "mark": mark, "cond": None, "watch": watch, "caption": caption, "start": start, "runs": [trace(code, mark, watch, labels, start)]}

def debugger(code, breakpoints, focus, caption):
    lines = code.rstrip("\n").split("\n"); events = []; buf = io.StringIO()
    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<prog>": return None
        if event == "line":
            stack = []; f = frame
            while f is not None and f.f_code.co_filename == "<prog>": stack.append(f.f_code.co_name); f = f.f_back
            stack.reverse()
            vars_ = [[k, repr(v)] for k, v in frame.f_locals.items() if not k.startswith("__") and not callable(v)]
            events.append({"line": frame.f_lineno, "depth": len(stack), "vars": vars_, "stack": stack, "out": buf.getvalue().rstrip("\n")})
        return tracer
    try:
        sys.settrace(tracer)
        with contextlib.redirect_stdout(buf): exec(compile(code, "<prog>", "exec"), {"__name__": "__main__"})
    finally: sys.settrace(None)
    return {"kind": "debugger", "caption": caption, "focus": focus, "breakpoints": breakpoints, "lines": lines, "events": events, "printed": buf.getvalue().rstrip("\n")}

MESSAGES = [("debug", "DEBUG", 10), ("info", "INFO", 20), ("warning", "WARNING", 30), ("error", "ERROR", 40), ("critical", "CRITICAL", 50)]
def levels():
    calls = "".join("logging.%s('%s message')\n" % (m, m) for m, _, _ in MESSAGES)
    def run(setup, use_stderr=False):
        code = "import logging, sys\n" + setup + calls
        r = subprocess.run([PY, "-c", code], capture_output=True, text=True)
        return (r.stderr if use_stderr else r.stdout).splitlines()
    fmt = "format='%(levelname)s - %(message)s'"
    settings = [("no basicConfig", "", True, "Without basicConfig the threshold is WARNING, and Python writes the messages to standard error with the logger's name, root.")]
    for _, name, _ in MESSAGES:
        settings.append(("level=%s" % name, "logging.basicConfig(level=logging.%s, stream=sys.stdout, %s)\n" % (name, fmt), False,
                         "basicConfig(level=logging.%s): a message is shown when its level is at least %s." % (name, name)))
    settings.append(("disable(CRITICAL)", "logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, %s)\nlogging.disable(logging.CRITICAL)\n" % fmt, False,
                     "logging.disable(logging.CRITICAL) silences CRITICAL and everything below it, whatever level basicConfig set."))
    out = []
    for label, setup, err, note in settings:
        lines = run(setup, err)
        out.append({"label": label, "note": note, "shown": [any(l.endswith(m + " message") for l in lines) for m, _, _ in MESSAGES], "output": lines})
    return {"kind": "levels", "settings": out, "messages": [{"call": "logging.%s('%s message')" % (m, m), "level": n, "num": k} for m, n, k in MESSAGES]}

def unwind():
    code = PROGRAMS["unwinding_v1_0_0.py"][0]; lines = code.rstrip("\n").split("\n")
    g = {}; tb = None
    try: exec(compile(code.split("try:")[0] + "process([{'age': '41'}, {'age': 'abc'}])\n", "<u>", "exec"), g)
    except ValueError as e: tb = e.__traceback__; exc = "%s: %s" % (type(e).__name__, e)
    fr = traceback.extract_tb(tb)                      # outermost first
    src = code.split("try:")[0] + "process([{'age': '41'}, {'age': 'abc'}])\n"; sl = src.split("\n")
    frames = [{"func": f.name, "line": f.lineno, "text": sl[f.lineno - 1].strip()} for f in reversed(fr) if f.filename == "<u>" and f.name != "<module>"]
    hl = next(i + 1 for i, l in enumerate(lines) if l.startswith("except"))
    d = tempfile.mkdtemp(); open(os.path.join(d, "main.py"), "w").write(src)
    r = subprocess.run([PY, "main.py"], cwd=d, capture_output=True, text=True)
    return {"kind": "unwind", "caption": "read_age cannot turn 'abc' into a number. No function on the way up handles the error, so it leaves each in turn until the try around the call catches it.",
            "exc": "ValueError", "frames": frames, "handler": {"func": "<module>", "line": hl, "text": lines[hl - 1].strip()},
            "traceback": r.stderr.replace(d + os.sep, "").rstrip("\n"), "message": exc}

def carets():
    src = "data = {'a': {'b': None}}\nprint(data['a']['b']['c'])\n"; d = tempfile.mkdtemp(); open(os.path.join(d, "main.py"), "w").write(src)
    r = subprocess.run([PY, "main.py"], cwd=d, capture_output=True, text=True)
    return {"kind": "traceback", "code": src, "text": r.stderr.replace(d + os.sep, "").rstrip("\n")}

V = {}
FB = PROGRAMS["factorial_bug_v1_0_0.py"][0]
V["OffByOneRange"] = t_spec(FB, "logging.debug('i is", ["i", "total"], {"total *= i": "block ran"},
                            "Each row is one pass of the loop, with i and total after total *= i has run. The first pass multiplies by 0, and total stays 0 from then on.", "total *= i")
DBG = PROGRAMS["debugdemo_v1_0_0.py"][0]
V["Breakpoint"] = debugger(DBG, [7], "cont", "A recorded run of the program. It stops before each line runs; the values are those at that stop.")
V["ContinueControl"] = debugger(DBG, [2, 7], "cont", "Two breakpoints are set, at lines 2 and 7. Continue runs to the next one.")
V["StepIn"] = debugger(DBG, [6], "in", "Continue runs to the breakpoint at line 6. Step In then moves into add.")
V["StepOver"] = debugger(DBG, [6], "over", "Continue runs to the breakpoint at line 6. Step Over then runs the whole call to add and stops at line 7.")
V["StepOut"] = debugger(DBG, [2], "out", "Continue runs to the breakpoint at line 2, inside add. Step Out then finishes add and stops in main.")
V["LevelThreshold"] = levels()
V["ExceptionUnwinding"] = unwind()
V["FineGrainedLocations"] = carets()
V["_meta"] = {"version": __version__, "python": platform.python_version(), "note": "Executed specifications; drawn by the deck and by the page."}
json.dump(V, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
print("written", sys.argv[1], "under Python", platform.python_version(), "-", len(V) - 1, "visuals")
