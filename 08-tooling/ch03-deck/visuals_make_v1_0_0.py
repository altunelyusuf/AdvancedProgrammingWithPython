"""Builds the chapter 3 visual specifications by EXECUTING code under the interpreter it is run with. A specification
is data: the same file is drawn as native shapes by the deck and as SVG by the page, so a slide and the page can never
show different values. Nothing in the output is typed by hand: a trace records what a real run did pass by pass (a line
tracer notes the variables at each pass, the lines the pass reached and the text it printed), a range spec lists the
values range() really makes, and a pairs spec lists what enumerate and zip really return.
Usage: visuals_make_v1_0_0.py <out.json>   (run under the Python the course teaches)"""
__version__ = "1.0.0"
import builtins, contextlib, io, json, platform, sys

# ---- traces -------------------------------------------------------------------------------------------------------
def trace(code, inputs, mark, cond, watch, labels, style, start=None):
    """Run `code` with input() fed from `inputs`. `mark` is a substring of the line that starts each pass (the loop test of a
    while, the first line of a for's block); `cond` an expression evaluated at that line for while loops (else None);
    `watch` the variable names shown; `labels` maps a substring of a source line to what reaching it means for the pass."""
    lines = code.split("\n")
    def find(sub):
        hits = [i + 1 for i, l in enumerate(lines) if sub in l]
        assert len(hits) >= 1, sub
        return hits[0]
    mline = find(mark); sline = find(start or mark); lab = {find(k): v for k, v in labels.items()}
    q = iter(inputs); buf = io.StringIO(); passes = []; cur = [None]
    def fake_input(prompt=""):
        v = next(q); buf.write(prompt + v + "\n"); return v
    def snap(frame):
        vals = []
        for w in watch:
            vals.append(repr(frame.f_locals[w]) if w in frame.f_locals else "")
        c = None
        if cond is not None:
            try: c = bool(eval(cond, frame.f_globals, frame.f_locals))
            except Exception: c = None
        return vals, c
    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<prog>": return None
        if event == "line":
            if frame.f_lineno == sline:
                if cur[0] is not None: cur[0]["out_end"] = buf.tell()
                cur[0] = {"vals": None, "cond": None, "events": [], "out_start": buf.tell(), "out_end": None}
                passes.append(cur[0])
            if frame.f_lineno == mline and cur[0] is not None and cur[0]["vals"] is None:
                cur[0]["vals"], cur[0]["cond"] = snap(frame)
            elif cur[0] is not None and frame.f_lineno in lab:
                cur[0]["events"].append(lab[frame.f_lineno])
        return tracer
    g = {"__name__": "__main__"}; old_input = builtins.input; builtins.input = fake_input
    try:
        sys.settrace(tracer)
        with contextlib.redirect_stdout(buf):
            try: exec(compile(code, "<prog>", "exec"), g)
            except SystemExit: cur[0]["events"].append("program ended by sys.exit()") if cur[0] else None
        sys.settrace(None)
    finally:
        sys.settrace(None); builtins.input = old_input
    if cur[0] is not None and cur[0]["out_end"] is None: cur[0]["out_end"] = buf.tell()
    text = buf.getvalue()
    rows = []
    for i, p in enumerate(passes):
        out = text[p["out_start"]:p["out_end"]].rstrip("\n").replace("\n", " / ")
        rows.append({"n": i + 1, "vals": p["vals"], "cond": p["cond"], "events": p["events"], "out": out})
    tail = text[passes[-1]["out_end"]:] if passes else text
    return {"inputs": inputs, "rows": rows, "printed": text.rstrip("\n").replace("\n", " / ")}

def t_spec(code, runs, mark, cond, watch, labels, style, caption, start=None):
    return {"kind": "trace", "style": style, "code": code, "mark": mark, "cond": cond, "watch": watch, "caption": caption,
            "start": start or mark, "runs": [trace(code, r, mark, cond, watch, labels, style, start) for r in runs]}

# ---- ranges and pairs --------------------------------------------------------------------------------------------
def r_spec(*args):
    r = range(*args); vals = list(r)
    step = r.step; lo = min(min(vals, default=r.start), r.start, r.stop); hi = max(max(vals, default=r.start), r.start, r.stop)
    return {"kind": "range", "call": "range(%s)" % ", ".join(map(str, args)), "start": r.start, "stop": r.stop, "step": step,
            "values": vals, "lo": lo, "hi": hi, "repr": repr(r), "length": len(r)}

def p_spec(call_label, a, b, kind, note):
    res = {"kind": "pairs", "call": call_label, "left": list(a), "right": list(b), "note": note}
    if kind == "enumerate":
        res["pairs"] = [list(x) for x in enumerate(a)]; res["left"] = list(a); res["right"] = list(range(len(a))); res["swap"] = True
        res["reprs"] = [repr(x) for x in enumerate(a)]
    elif kind == "zip":
        res["pairs"] = [list(x) for x in zip(a, b)]; res["reprs"] = [repr(x) for x in zip(a, b)]
        n = len(res["pairs"]); res["leftover"] = {"left": [str(x) for x in list(a)[n:]], "right": [str(x) for x in list(b)[n:]]}
    elif kind == "zipstrict":
        got = []; res["error"] = None
        try:
            for x in zip(a, b, strict=True): got.append(x)
        except ValueError as e: res["error"] = "ValueError: %s" % e
        res["pairs"] = [list(x) for x in got]; res["reprs"] = [repr(x) for x in got]   # the pairs made before the error was raised
        n = min(len(a), len(b)); res["leftover"] = {"left": [str(x) for x in list(a)[n:]], "right": [str(x) for x in list(b)[n:]]}
    return res

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from examples_v1_1_0 import PROGRAMS   # the traced programs and their inputs ARE the deck's programs, so a trace and a transcript can never describe different runs
WAIT, R_WAIT = PROGRAMS["waiting_v1_0_0.py"]; SUM, R_SUM = PROGRAMS["summing_v1_0_0.py"]; SEARCH, R_SEARCH = PROGRAMS["searching_v1_0_0.py"]
LOOPVAR, R_LOOPVAR = PROGRAMS["loopvar_v1_0_0.py"]; FORDEMO, R_FOR = PROGRAMS["forsum_v1_0_0.py"]; GUESS, R_GUESS = PROGRAMS["guessing_v1_0_0.py"]

V = {}
V["WhileStatement"] = t_spec(WAIT, R_WAIT, "while answer != 'yes':", "answer != 'yes'", ["answer"], {"answer = input": "body ran"}, "table",
                             "Each row is one test of the condition, with the value of answer at that moment.")
V["ForStatement"] = t_spec(FORDEMO, R_FOR, "total += n", None, ["n", "total"], {"total += n": "block ran"}, "table",
                           "Each row is one pass of the block: n is assigned the next item, then the block runs. Values are shown as the block starts.")
V["BreakStatement"] = t_spec(SUM, R_SUM, "if entry == ''", None, ["entry", "total"], {"break": "break: leave the loop", "continue": "continue: skip to the next pass", "total += int": "added to total"}, "strip",
                             "Each box is one pass. break ends the loop at once; the pass before it ended by reaching the bottom or by continue.", start="entry = input")
V["ContinueStatement"] = V["BreakStatement"]
V["LoopElseClause"] = t_spec(SEARCH, R_SEARCH, "if word == target", None, ["word"], {"print('found'": "found: break follows", "break": "break: else skipped", "print('not found')": "else ran: nothing was found"}, "strip",
                             "Two runs of the same loop. The else runs only when no pass reaches break.")
V["LoopVariableScope"] = t_spec(LOOPVAR, R_LOOPVAR, "pass", None, ["i"], {}, "table",
                                "i is assigned on every pass and is still there after the loop: the last value, 2.")
V["GuessLoop"] = t_spec(GUESS, R_GUESS, "if guess < secret", None, ["attempt", "guess"], {"print('too low')": "too low", "print('too high')": "too high", "print(f'got it": "got it: break", "print(f'out of guesses": "else ran: out of guesses"}, "table",
                        "Two runs: a win on the third attempt, and three misses that end in the loop else.", start="guess = int(input")
V["RangeStop"] = r_spec(5)
V["RangeStartStop"] = r_spec(12, 16)
V["RangeStep"] = r_spec(0, 10, 2)
V["RangeDescending"] = r_spec(5, -1, -1)
V["LazyRange"] = r_spec(10)
V["EnumerateFunction"] = p_spec("enumerate(['tic', 'tac', 'toe'])", ["tic", "tac", "toe"], [], "enumerate", "enumerate pairs each item with a running count that starts at 0")
V["ZipStrict"] = p_spec("zip('abc', [1, 2])", "abc", [1, 2], "zip", "zip stops at the shortest iterable and quietly drops the rest")
V["ZipStrictError"] = p_spec("zip('abc', [1, 2], strict=True)", "abc", [1, 2], "zipstrict", "strict=True turns the silent truncation into an error")
import random as _random
V["StarImport"] = {"kind": "names", "module": "random", "count": len(_random.__all__), "sample": list(_random.__all__)[:8],
                   "note": "from random import * would bring every name in random.__all__ into the program, with no prefix to say where each came from"}
V["_meta"] = {"version": __version__, "python": platform.python_version(),
              "note": "Executed specifications; drawn by the deck and by the page. ContinueStatement shows the same run as BreakStatement."}
json.dump(V, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
print("written", sys.argv[1], "under Python", platform.python_version(), "-", len(V) - 1, "visuals")
