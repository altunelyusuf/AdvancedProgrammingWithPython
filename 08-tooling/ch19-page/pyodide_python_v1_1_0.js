// A "python" command that runs under Pyodide 0.28.2 (CPython 3.13), the interpreter of the page template 9.52.3, with the four pure-Python wheels of the chapter 19 page
// (playsound3, pyperclip, schedule, tzdata) unpacked from 03-materials/ch19/assets the way the page unpacks them, and the page's boot snippet (pywheels_v1_0_1.json, boot_python) run once, the way the page's worker runs it. It understands exactly what the page-data builder 2.25.0 asks of its interpreter: `--version` and `-c CODE [ARG...]`.
// Used so the recorded results of the page's observed programs come from the page's own runtime. Needs node and the npm package pyodide@0.28.2 on NODE_PATH.
// Version 1.1.0: a program that ends with sys.exit() ends cleanly with its exit code, as python does. Usage: node pyodide_python_v1_1_0.js WHEEL_DIR (--version | -c CODE [ARG...])
const fs = require('fs'), path = require('path');
(async () => {
  const wheelDir = process.argv[2], rest = process.argv.slice(3);
  const { loadPyodide } = require('pyodide');
  const py = await loadPyodide();
  if (rest[0] === '--version') { console.log('Python ' + py.runPython("import sys; sys.version.split()[0]") + ' (Pyodide ' + py.version + ')'); return; }
  const SITE = py.runPython("import sysconfig;sysconfig.get_path('purelib')");
  const PW = JSON.parse(fs.readFileSync(path.join(__dirname, 'pywheels_v1_0_1.json'), 'utf8'));
  for (const w of PW.wheels) py.unpackArchive(new Uint8Array(fs.readFileSync(path.join(wheelDir, w.file))), 'wheel', { extractDir: SITE });
  py.runPython("import importlib;importlib.invalidate_caches()");
  py.runPython(PW.boot_python);
  if (rest[0] !== '-c') { console.error('only --version and -c are supported'); process.exit(2); }
  py.globals.set('_code', rest[1]); py.globals.set('_argv', ['-c'].concat(rest.slice(2)));
  const out = [];
  py.setStdout({ write: (b) => { out.push(Buffer.from(b)); return b.length; } });
  let rc = 0;
  try { rc = py.runPython("import sys\nsys.argv = list(_argv)\n_rc = 0\ntry:\n    exec(compile(_code, '<string>', 'exec'), {'__name__': '__main__'})\nexcept SystemExit as _e:\n    _rc = _e.code if isinstance(_e.code, int) else 0\n    if _e.code is not None and not isinstance(_e.code, int):\n        print(_e.code, file=sys.stderr); _rc = 1\n_rc"); }
  catch (e) { process.stderr.write(String(e) + '\n'); process.exit(1); }
  process.stdout.write(Buffer.concat(out)); process.exitCode = rc;
})();
