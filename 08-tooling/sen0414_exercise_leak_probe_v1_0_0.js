// sen0414_exercise_leak_probe v1_0_0 - the controller's probe of the leak found on chapter 14 (2026-10-26): the page runs every program, the probes of its blank exercises included, in the SAME
// Python worker. A probe that fails after a side effect (sys.path.insert, an import, os.chdir, a written file) leaves that state for the next run.
// Method: ONE Pyodide 0.28.2 interpreter with the page worker's _run function (template 9.52.2, copied unchanged); the chapter's examples run in manifest order (baseline, must equal the manifest);
// then ROUNDS rounds in a seeded shuffled order: for each example PROBES probe runs (the code with one token replaced by ____, the way the page's exPickToken does; examples with a while loop are skipped as the page skips them)
// followed by the real run, which must equal the manifest. Reports every real run that differs, and the state left behind (sys.path, new non-library modules, cwd).
// Usage: node sen0414_exercise_leak_probe_v1_0_0.js MANIFEST.json OUT.json ROUNDS PROBES SEED [WHEEL...]   NODE_PATH must hold the pyodide package. RESTORE=1 runs the repaired _run (restores sys.path, new modules, cwd, environ after every run) to test a repair.
const fs = require('fs');
(async () => {
  const { loadPyodide } = require('pyodide');
  const [man, outp, rounds, probes, seed] = [JSON.parse(fs.readFileSync(process.argv[2], 'utf8')), process.argv[3], +process.argv[4], +process.argv[5], +process.argv[6]];
  const py = await loadPyodide();
  const SITE = py.runPython("import sysconfig;sysconfig.get_path('purelib')");
  for (const w of process.argv.slice(7)) py.unpackArchive(new Uint8Array(fs.readFileSync(w)), 'wheel', { extractDir: SITE });
  py.runPython("import importlib;importlib.invalidate_caches()");
  await py.runPythonAsync(`import sys, io, ast, os
def _run0(src, inp):
    _o = io.StringIO()
    ns = {'__name__': '__main__'}
    old = sys.stdout; olde = sys.stderr; sys.stdout = _o; sys.stderr = _o
    try:
        t = ast.parse(src)
        if t.body and isinstance(t.body[-1], ast.Expr):
            last = ast.Expression(t.body.pop().value)
            exec(compile(t, '<code>', 'exec'), ns)
            v = eval(compile(last, '<code>', 'eval'), ns)
            if v is not None: print(repr(v))
        else:
            exec(compile(t, '<code>', 'exec'), ns)
    except Exception as e:
        print(type(e).__name__ + ': ' + str(e))
    finally:
        sys.stdout = old; sys.stderr = olde
    return _o.getvalue().rstrip()
_LIB = tuple(p for p in sys.path if 'python3' in p or 'site-packages' in p or p.endswith('.zip'))
def _run1(src, inp):
    p = list(sys.path); m = set(sys.modules); c = os.getcwd(); e = dict(os.environ)
    try: return _run0(src, inp)
    finally:
        sys.path[:] = p
        for k in set(sys.modules) - m:
            f = getattr(sys.modules.get(k), '__file__', None) or ''
            if not f.startswith(_LIB): sys.modules.pop(k, None)
        try: os.chdir(c)
        except Exception: pass
        os.environ.clear(); os.environ.update(e)
def _state():
    return {'path': len(sys.path), 'cwd': os.getcwd(), 'mods': sorted(k for k, v in list(sys.modules.items()) if not (getattr(v, '__file__', None) or '').startswith(_LIB) and getattr(v, '__file__', None))}
`);
  const run = py.globals.get(process.env.RESTORE ? '_run1' : '_run0'), state = () => py.runPython('import json;json.dumps(_state())');
  let s = seed >>> 0; const rnd = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  const ex = man.examples, base = JSON.parse(state()), res = { python: py.runPython("import sys;sys.version.split()[0]"), restore: !!process.env.RESTORE, baseline_bad: [], leaks: [], rounds_state: [] };
  for (const e of ex) { const g = String(run(e.code, '')).trimEnd(); if (g !== e.expected.trimEnd()) res.baseline_bad.push(e.name); }
  res.after_baseline = JSON.parse(state());
  const TOK = /[A-Za-z_][A-Za-z0-9_]*|\d+/g;
  for (let r = 0; r < rounds; r++) {
    const order = ex.map((_, i) => i).sort(() => rnd() - 0.5);
    for (const i of order) {
      const e = ex[i]; if (/(^|\W)while\b/.test(e.code)) continue;
      const toks = [...e.code.matchAll(TOK)];
      for (let k = 0; k < probes && toks.length; k++) { const t = toks[Math.floor(rnd() * toks.length)]; const code = e.code.slice(0, t.index) + '____' + e.code.slice(t.index + t[0].length); try { run(code, ''); } catch (x) {} }
      const g = String(run(e.code, '')).trimEnd();
      if (g !== e.expected.trimEnd()) res.leaks.push({ round: r, example: e.name, got: g.slice(0, 200), expected: e.expected.slice(0, 200) });
    }
    res.rounds_state.push(JSON.parse(state()));
  }
  res.verdict = (res.baseline_bad.length || res.leaks.length) ? 'FAIL' : 'PASS';
  fs.writeFileSync(outp, JSON.stringify(res, null, 1));
  console.log(res.python, 'restore=' + res.restore, ex.length + ' examples', rounds + ' rounds', probes + ' probes', 'baseline_bad=' + res.baseline_bad.length, 'wrong_real_runs=' + res.leaks.length, 'final state:', JSON.stringify(res.rounds_state[rounds - 1] ? { path: res.rounds_state[rounds - 1].path, cwd: res.rounds_state[rounds - 1].cwd, mods: res.rounds_state[rounds - 1].mods.length } : {}), res.verdict);
})();
