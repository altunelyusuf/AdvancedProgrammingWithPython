// A "python" command that runs under Pyodide 0.28.2 (CPython 3.13), the interpreter of the page template 9.52.4, set up the way the page sets it up at start: FIRST Pyodide's own package sqlite3 (the template does
// py.loadPackage('sqlite3') before anything else; the first attempt of the chapter 16 page left it out and every recorded result was a ModuleNotFoundError), then the packages and wheels named in the chapter's pywheels file,
// then the page's boot program (it writes the book's database and defines _before_run). It understands exactly what the page-data builder 2.25.0 asks of its interpreter: `--version` and `-c CODE [ARG...]`.
// Derived from 08-tooling/ch15-page/pyodide_python_v1_0_0.js (which stays); needs node and the npm package pyodide@0.28.2 on NODE_PATH.
// Usage: node pyodide_python_v9_95_0.js WHEEL_DIR PYWHEELS.json (--version | -c CODE [ARG...])
const fs = require('fs'), path = require('path');
(async () => {
  const wheelDir = process.argv[2], pw = JSON.parse(fs.readFileSync(process.argv[3], 'utf8')), rest = process.argv.slice(4);
  const { loadPyodide } = require('pyodide');
  const py = await loadPyodide({ stdout: () => {}, stderr: () => {} });
  if (rest[0] === '--version') { console.log('Python ' + py.runPython("import sys; sys.version.split()[0]") + ' (Pyodide ' + py.version + ')'); return; }
  try { await py.loadPackage('sqlite3', { messageCallback: () => {}, errorCallback: (m) => process.stderr.write(m + '\n') }); } catch (e) { process.stderr.write('sqlite3 package: ' + e + '\n'); process.exit(3); }
  const SITE = py.runPython("import sysconfig;sysconfig.get_path('purelib')");
  for (const k of pw.pyodide_packages) await py.loadPackage(k, { messageCallback: () => {}, errorCallback: (m) => process.stderr.write(m + '\n') });
  for (const w of pw.wheels) py.unpackArchive(new Uint8Array(fs.readFileSync(path.join(wheelDir, w.file))), 'wheel', { extractDir: SITE });
  py.runPython("import importlib;importlib.invalidate_caches()");
  py.runPython(pw.boot_python);
  if (rest[0] !== '-c') { console.error('only --version and -c are supported'); process.exit(2); }
  py.globals.set('_code', rest[1]); py.globals.set('_argv', ['-c'].concat(rest.slice(2)));
  const out = [];
  py.setStdout({ write: (b) => { out.push(Buffer.from(b)); return b.length; } });
  try { py.runPython("import sys\nsys.argv = list(_argv)\nexec(compile(_code, '<string>', 'exec'), {'__name__': '__main__'})"); }
  catch (e) { process.stderr.write(String(e) + '\n'); process.exit(1); }
  process.stdout.write(Buffer.concat(out));
})();
