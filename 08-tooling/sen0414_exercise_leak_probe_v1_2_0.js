// sen0414_exercise_leak_probe v1_2_0 (over v1_1_0, a NEW file; found on chapter 18, 2026-10-27: a probe that fails after tracemalloc.start() leaves tracing on and the next real run of IterparseClear reports another peak, a leak v1_1_0 saw only as a wrong real run, never as a state drift). Added to the interpreter state read after EVERY run: tracemalloc.is_tracing(), the length and the identity of warnings.filters, the recursion limit, the default socket timeout, tempfile.tempdir, the umask, random's seed state is NOT read (a program may seed it) and, for the modules of /lib/ loaded at boot, the identity of every public attribute that existed at boot (so a program that replaces webbrowser.open or a module function is seen); every difference is a state drift. The rest is v1_1_0 unchanged, which stays as committed. (over v1_0_0, a NEW file) - the same leak probe, but the Python worker is TAKEN FROM THE TEMPLATE FILE ITSELF, not from a copy of its _run:
// the text PY_WORKER_SRC of the template is cut out of the file, evaluated as the template does (with the page's own data: py_wheels, py_packages, py_boot), and RUN as the page's worker
// (importScripts and loadPyodide are the only stand-ins: loadPyodide is the node Pyodide 0.28.2 of NODE_PATH, importScripts does nothing). The probe sends the worker the same messages the page sends
// ({id, code, inputs}) and reads the answers it posts back. So a proof of THIS probe is a proof of the real template's worker.
// Method (as v1_0_0): the programs run in order (baseline, must equal the recorded output); then ROUNDS rounds in a seeded shuffled order: for each program PROBES probe runs (one token replaced by
// ____, the way the page's exPickToken does; programs with a while loop are skipped as the page skips them), followed by the real run, which must equal the recorded output.
// Stricter than v1_0_0: the state of the interpreter (sys.path, modules not from /lib/, working folder, os.environ) is read after EVERY run and compared with the state after boot;
// every difference is counted (state_drifts). Verdict PASS only with 0 wrong real runs, 0 wrong baseline and 0 state drifts.
// Usage: node sen0414_exercise_leak_probe_v1_1_0.js TEMPLATE.html PAGE.html PROGRAMS.json OUT.json ROUNDS PROBES SEED     (NODE_PATH holds the pyodide package; PROGRAMS.json = {"examples":[{name,code,expected}]})
const fs = require('fs');
(async () => {
  const [tpl, pagef, progf, outp, rounds, probes, seed] = [process.argv[2], process.argv[3], process.argv[4], process.argv[5], +process.argv[6], +process.argv[7], +process.argv[8]];
  const T = fs.readFileSync(tpl, 'utf8');
  const D = JSON.parse(/<script[^>]*id="data"[^>]*>([\s\S]*?)<\/script>/.exec(fs.readFileSync(pagef, 'utf8'))[1]);
  const man = JSON.parse(fs.readFileSync(progf, 'utf8'));
  const a = T.indexOf('const PY_WORKER_SRC=`'); if (a < 0) throw new Error('PY_WORKER_SRC not found in the template');
  const b = T.indexOf('`;', a + 21); const body = T.slice(a + 21, b);
  const PYWHEELS = (D.py_wheels || []), PYODIDE_BASE = 'https://cdn.jsdelivr.net/pyodide/v0.28.2/full/';
  const workerSrc = new Function('D', 'PYWHEELS', 'PYODIDE_BASE', 'return `' + body + '`')(D, PYWHEELS, PYODIDE_BASE);
  const { loadPyodide } = require('pyodide');
  let PY = null; const posted = []; const self = {};
  const shimLoad = async () => { PY = await loadPyodide(); return PY; };
  new Function('self', 'importScripts', 'loadPyodide', 'postMessage', workerSrc)(self, () => {}, shimLoad, m => posted.push(m));
  let n = 0; const send = async (code) => { const id = 'm' + (++n); await self.onmessage({ data: { id, code, inputs: '' } }); const r = posted.find(x => x.id === id); posted.splice(posted.indexOf(r), 1); if (r.error !== undefined) throw new Error(r.error); return r.out; };
  const t0 = Date.now(); while (!posted.find(x => x.id === 'boot')) { await new Promise(r => setTimeout(r, 50)); if (Date.now() - t0 > 600000) throw new Error('worker boot timeout'); }
  PY.runPython(`import sys, os, json
def _probe_state():
    import tracemalloc, warnings, socket, tempfile
    um = os.umask(0o22); os.umask(um)
    return {'path': list(sys.path), 'cwd': os.getcwd(), 'env': dict(os.environ), 'mods': sorted(k for k, v in list(sys.modules.items()) if (getattr(v, '__file__', None) or '') and not getattr(v, '__file__').startswith('/lib/')),
            'trace': tracemalloc.is_tracing(), 'warn': [repr(f) for f in warnings.filters], 'rec': sys.getrecursionlimit(), 'sock': socket.getdefaulttimeout(), 'tmp': tempfile.tempdir, 'umask': um,
            'attrs': {m: {k: id(v) for k, v in list(getattr(sys.modules[m], '__dict__', {}).items()) if not k.startswith('_')} for m in list(_BOOT_MODS) if m in sys.modules}}
_BOOT_MODS = sorted(k for k, v in list(sys.modules.items()) if (getattr(v, '__file__', None) or '').startswith('/lib/') and '.' not in k)
`);
  const state = () => JSON.parse(PY.runPython('json.dumps(_probe_state())'));
  const init = state(); const drifts = []; let runs = 0;
  const diff = (s, tag) => { const d = []; if (JSON.stringify(s.path) !== JSON.stringify(init.path)) d.push('sys.path ' + init.path.length + '->' + s.path.length); if (s.cwd !== init.cwd) d.push('cwd ' + s.cwd); if (JSON.stringify(s.env) !== JSON.stringify(init.env)) d.push('environ'); if (JSON.stringify(s.mods) !== JSON.stringify(init.mods)) d.push('modules +' + s.mods.filter(x => !init.mods.includes(x)).join(',')); if (s.trace !== init.trace) d.push('tracemalloc tracing ' + s.trace); if (JSON.stringify(s.warn) !== JSON.stringify(init.warn)) d.push('warnings.filters ' + init.warn.length + '->' + s.warn.length); if (s.rec !== init.rec) d.push('recursionlimit ' + s.rec); if (s.sock !== init.sock) d.push('socket timeout'); if (s.tmp !== init.tmp) d.push('tempfile.tempdir'); if (s.umask !== init.umask) d.push('umask'); for (const m of Object.keys(init.attrs)) { const a0 = init.attrs[m], a1 = s.attrs[m] || {}; const ch = Object.keys(a0).filter(k => k in a1 && a1[k] !== a0[k]); if (ch.length) d.push('module ' + m + ' attribute ' + ch.slice(0, 3).join(',')); } if (d.length) drifts.push({ at: tag, what: d.join('; ') }); };
  const run = async (code, tag) => { const o = await send(code); runs++; diff(state(), tag); return o; };
  let s = seed >>> 0; const rnd = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  const ex = man.examples, res = { python: PY.runPython("import sys;sys.version.split()[0]"), template: tpl.split('/').pop(), page: pagef.split('/').pop(), seed, programs: ex.length, rounds, probes, baseline_bad: [], leaks: [] };
  for (const e of ex) { const g = String(await run(e.code, 'baseline ' + e.name)).trimEnd(); if (g !== e.expected.trimEnd()) res.baseline_bad.push(e.name); }
  const TOK = /[A-Za-z_][A-Za-z0-9_]*|\d+/g;
  for (let r = 0; r < rounds; r++) {
    const order = ex.map((_, i) => i).sort(() => rnd() - 0.5);
    for (const i of order) {
      const e = ex[i]; if (/(^|\W)while\b/.test(e.code)) continue;
      const toks = [...e.code.matchAll(TOK)];
      for (let k = 0; k < probes && toks.length; k++) { const t = toks[Math.floor(rnd() * toks.length)]; const code = e.code.slice(0, t.index) + '____' + e.code.slice(t.index + t[0].length); try { await run(code, 'probe ' + e.name); } catch (x) {} }
      const g = String(await run(e.code, 'real ' + e.name)).trimEnd();
      if (g !== e.expected.trimEnd()) res.leaks.push({ round: r, example: e.name, got: g.slice(0, 200), expected: e.expected.slice(0, 200) });
    }
  }
  const fin = state(); res.runs = runs; res.state_drifts = drifts.length; res.first_drifts = drifts.slice(0, 5); res.final = { path: fin.path.length, cwd: fin.cwd, modules_outside_lib: fin.mods.length };
  res.verdict = (res.baseline_bad.length || res.leaks.length || drifts.length) ? 'FAIL' : 'PASS';
  fs.writeFileSync(outp, JSON.stringify(res, null, 1));
  console.log('seed ' + seed, res.template, res.python, res.programs + ' programs', rounds + ' rounds', probes + ' probes', res.runs + ' runs', 'baseline_bad=' + res.baseline_bad.length, 'wrong_real_runs=' + res.leaks.length, 'state_drifts=' + res.state_drifts, 'final:', JSON.stringify(res.final), res.verdict);
  process.exit(0);
})().catch(e => { console.log('CANNOT_RUN', String(e && e.stack || e).slice(0, 600)); process.exit(2); });
