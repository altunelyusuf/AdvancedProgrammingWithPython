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

  const progs = JSON.parse(fs.readFileSync(process.argv[4],'utf8')).examples;
  const byName = n => progs.find(e => e.name === n);
  const ip = byName('ImagesNeedPillow').code, cc5 = progs.find(e=>e.name.startsWith('CC5 ')).code;
  const tryrun = async (tag, code) => { try { const o = await send(code); console.log(tag, 'OK', String(o).slice(0,120).replace(/\n/g,' | ')); } catch (e) { console.log(tag, 'ERROR', String(e.message||e).slice(-200).replace(/\n/g,' | ')); } };
  await tryrun('cc5 before', cc5);
  const bad = ip.replace("sys.modules[\\'PIL\\'] = _pil", "sys.modules[\\'PIL\\'] = ____");
  console.log('variant differs:', bad !== ip);
  await tryrun('variant', bad);
  await tryrun('real', ip);
  await tryrun('cc5 after', cc5);
  process.exit(0);
})().catch(e => { console.log('CANNOT_RUN', String(e && e.stack || e).slice(0, 600)); process.exit(2); });
