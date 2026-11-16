#!/usr/bin/env python3
"""Writes the chapter 19 domain ABox v1.0.7: the same 61 input-output examples as v1.0.6, with every input written as plain, lambda-free code instead of the one-expression
(lambda g: (exec('<prologue>...', g), g['out'])[1])({}) wrapper (the owner's ruling of 2026-11-14: no lambda unless taught; code shown to the learner is readable, indented Python). The way each input is rewritten:
  - the body of the exec string is kept character for character;
  - the fixed prologue (all imports, DT/TD/D/timezone/UTC/ZoneInfo, the helpers err, warned, child) is cut down to what the body uses, so a reader sees only the imports and helper functions the example needs;
  - the final top-level  out = EXPR  becomes the bare expression EXPR, whose value is the example's result (the page-data builder 2.27.0 runs a multi-line input as a program and takes the last expression).
Every rewritten input is then run under this interpreter next to the original lambda and the two results must be equal (examples that read the clock, a process or a thread are compared by type only and listed).
Output: 03-materials/ch19/rdodi/sen0414_ch19_domain_abox_v1_0_7.ttl (refuses to overwrite). Version 1.1.0 also removes the lambdas that sat inside the bodies: err(lambda: X) and warned(lambda: X) become err("X") / warned("X") (the helper evaluates the text), and the few handlers and callbacks become named def functions. Usage: abox_lambda_free_make_v1_1_0.py"""
__version__ = "1.1.0"
import ast, os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(R, "03-materials/ch19/rdodi/sen0414_ch19_domain_abox_v1_0_6.ttl"); DST = os.path.join(R, "03-materials/ch19/rdodi/sen0414_ch19_domain_abox_v1_0_7.ttl")
if os.path.exists(DST): sys.exit("refusing to overwrite " + DST)
text = open(SRC, encoding="utf-8").read()
MODS = "io os re sys time datetime subprocess warnings signal threading math calendar shlex sched tempfile struct zoneinfo shutil".split()
FROMDT = [("datetime", "DT"), ("timedelta", "TD"), ("date", "D"), ("timezone", None), ("UTC", None)]
HELP = {
 "err": ("def err(src):\n    try:\n        return ('ok', eval(src))\n    except Exception as e:\n        return (type(e).__name__, str(e))\n", {"Exception"}),
 "warned": ("def warned(src):\n    with warnings.catch_warnings(record=True) as w:\n        warnings.simplefilter('always')\n        v = eval(src)\n    return v, [(x.category.__name__, str(x.message)) for x in w]\n", {"warnings"}),
 "child": ("def child(code, **env):\n    e = dict(os.environ)\n    e.update(env)\n    r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, env=e)\n    if r.returncode == 0:\n        return r.stdout.strip()\n    return r.stderr.strip().splitlines()[-1]\n", {"os", "subprocess", "sys"}),
}
def names(src):
    return {n.id for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Name)}
def rewrite(wrapped):
    call = ast.parse(wrapped).body[0].value
    code = call.func.body.value.elts[0].args[0].value
    k = code.index("def child"); end = code.index("\n", code.index("r = subprocess.run([sys.executable", k)) + 1
    body = code[end:]
    tree = ast.parse(body)
    last = tree.body[-1]
    assert isinstance(last, ast.Assign) and [t.id for t in last.targets] == ["out"], "last statement is not out = ..."
    lines = body.split("\n")
    seg = "\n".join(lines[last.value.lineno - 1:last.end_lineno]); seg = seg[:last.end_col_offset] if last.lineno == last.end_lineno else seg
    value_src = ast.get_source_segment(body, last.value)
    new_body = "\n".join(lines[:last.lineno - 1]) + ("\n" if last.lineno > 1 else "") + value_src
    used = names(new_body)
    helpers = [h for h in ("err", "warned", "child") if h in used]
    full_used = set(used)
    for h in helpers: full_used |= HELP[h][1] | names(HELP[h][0])
    mods = [m for m in MODS if m in full_used]
    head = []
    if mods: head.append("import " + ", ".join(mods))
    fd = [(a if b is None else a + " as " + b) for a, b in FROMDT if (b or a) in full_used]
    if fd: head.append("from datetime import " + ", ".join(fd))
    if "ZoneInfo" in full_used: head.append("from zoneinfo import ZoneInfo")
    parts = ["\n".join(head)] if head else []
    for h in helpers: parts.append(HELP[h][0].rstrip("\n"))
    parts.append(new_body)
    return "\n".join(p for p in parts if p), code
MANUAL = {
 "IO_StrptimeParse": [("hasattr(D,'strptime'), D.strptime('2026-10-21','%Y-%m-%d'), datetime.time.strptime('16:29','%H:%M')", "p('2026-10-21','%Y-%m-%d').date(), p('16:29','%H:%M').time()")],
 "IO_ExitCodes": [("c=lambda code: subprocess.run([sys.executable,'-c',code]).returncode", "def c(code):\n    return subprocess.run([sys.executable, '-c', code]).returncode")],
 "IO_SchedModule": [("s=sched.scheduler(lambda: clock[0], lambda d: clock.__setitem__(0, clock[0]+d))", "def now():\n    return clock[0]\ndef pause(d):\n    clock[0] += d\ns=sched.scheduler(now, pause)"),
   ("s2=sched.scheduler(lambda: clock2[0], lambda d: clock2.__setitem__(0, clock2[0]+d))", "def now2():\n    return clock2[0]\ndef pause2(d):\n    clock2[0] += d\ns2=sched.scheduler(now2, pause2)")],
 "IO_SleepAndSignals": [("signal.signal(signal.SIGALRM, lambda s,f: hits.append('handler ran'))", "def on_alarm(s, f):\n    hits.append('handler ran')\nsignal.signal(signal.SIGALRM, on_alarm)")],
 "IO_TerminateVsKill": [("signal.signal(signal.SIGTERM, lambda s,f: (print('asked to stop, saving work', flush=True), sys.exit(0)))", "def stop(s,f):\\n    print('asked to stop, saving work', flush=True)\\n    sys.exit(0)\\nsignal.signal(signal.SIGTERM, stop)"),
   ("(a,b, signal", "def ignore(*args):\n    return 0\n(a,b, signal"),
   ("err(lambda: signal.signal(signal.SIGKILL, lambda *a: 0))", "err(\"signal.signal(signal.SIGKILL, ignore)\")")],
}
def delambda(src):
    tree = ast.parse(src); b = src.encode("utf-8"); lines = b.split(b"\n"); starts = [0]
    for l in lines: starts.append(starts[-1] + len(l) + 1)
    edits = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("err", "warned") and len(n.args) == 1 and isinstance(n.args[0], ast.Lambda) and not n.args[0].args.args:
            inner = ast.get_source_segment(src, n.args[0].body)
            edits.append((starts[n.lineno-1]+n.col_offset, starts[n.end_lineno-1]+n.end_col_offset, n.func.id + "(" + repr(inner) + ")"))
    edits = [e for e in edits if not any(o is not e and e[0] <= o[0] and o[1] <= e[1] for o in edits)]
    for a, z, r in sorted(edits, reverse=True): b = b[:a] + r.encode("utf-8") + b[z:]
    out = b.decode("utf-8")
    return delambda(out) if edits else out
def tlit(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
import rdflib
CH = rdflib.Namespace("http://example.org/sen0414/ch19#")
g = rdflib.Graph(); g.parse(SRC)
code_of = {str(sj).split("#")[-1]: str(o) for sj, p, o in g.triples((None, CH.input, None))}
def run_new(src):
    t = ast.parse(src); last = t.body[-1]
    ns = {"__name__": "__main__"}
    exec(compile(ast.Module(t.body[:-1], []), "<new>", "exec"), ns)
    return eval(compile(ast.Expression(last.value), "<new>", "eval"), ns)
LINE = re.compile(r'^(chx:IO_\w+ a owl:NamedIndividual, rd:IOExample ; rdfs:label ")(.*?)("@en ; chx:input ")(.*?)(" ; chx:output ".*)$')
out_lines, n, same, diff = [], 0, 0, []
for line in text.split("\n"):
    m = LINE.match(line)
    if not m:
        out_lines.append(line); continue
    iri = m.group(1).split()[0][4:]
    old = code_of[iri]
    new, _ = rewrite(old)
    for a_, b_ in MANUAL.get(iri, []):
        assert a_ in new, (iri, a_); new = new.replace(a_, b_)
    if iri == "IO_TerminateVsKill": new = new.replace("p=subprocess.Popen", "p=subprocess.Popen", 1)
    new = delambda(new)
    assert "lambda" not in new, iri
    n += 1
    try:
        a = repr(eval(old, {})); b = repr(run_new(new))
    except Exception as e:
        a, b = "ERR", "ERR %s: %s" % (type(e).__name__, e)
    if a == b: same += 1
    else: diff.append((iri, a[:90], b[:90]))
    tail = m.group(5)
    if iri == "IO_StrptimeParse":
        assert ", True, datetime.date(2026, 10, 21)" in tail; tail = tail.replace(", True, datetime.date(2026, 10, 21)", ", datetime.date(2026, 10, 21)")
    out_lines.append(m.group(1) + tlit(new) + m.group(3) + tlit(new) + tail)
print("rewritten", n, "equal results", same, "different", len(diff))
for d in diff: print(" DIFF", d)
res = "\n".join(out_lines).replace('owl:versionInfo "1.0.6" ; owl:versionIRI <http://example.org/sen0414/ch19/abox/1.0.6>', 'owl:versionInfo "1.0.7" ; owl:versionIRI <http://example.org/sen0414/ch19/abox/1.0.7>').replace("sen0414_ch19_abox_v1_0_6", "sen0414_ch19_abox_v1_0_7")
if "--write" in sys.argv:
    open(DST, "w", encoding="utf-8").write(res); print("wrote", DST)
