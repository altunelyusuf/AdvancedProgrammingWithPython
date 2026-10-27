// A "python" command that runs under Pyodide 0.28.2 (CPython 3.13), the interpreter of the page template 9.52.4, set up the way the chapter 15 page sets it up at start: Pyodide's own packages
// named in pywheels_v9_95_0.json (ssl, protobuf, cryptography, requests, ...) loaded first, the 14 pure-Python wheels of 03-materials/ch15/assets unpacked into site-packages, then the page's boot program
// (it installs the stand-in module google_standin and defines _before_run). It understands exactly what the page-data builder 2.25.0 asks of its interpreter: `--version` and `-c CODE [ARG...]`.
// Used so the recorded results of the page's observed programs come from the page's own runtime. Needs node and the npm package pyodide@0.28.2 on NODE_PATH.
// Usage: node pyodide_python_v1_0_0.js WHEEL_DIR PYWHEELS.json (--version | -c CODE [ARG...])
const fs = require('fs'), path = require('path');
(async () => {
  const wheelDir = process.argv[2], pw = JSON.parse(fs.readFileSync(process.argv[3], 'utf8')), rest = process.argv.slice(4);
  const { loadPyodide } = require('pyodide');
  const py = await loadPyodide({ stdout: () => {}, stderr: () => {} });
  if (rest[0] === '--version') { console.log('Python ' + py.runPython("import sys; sys.version.split()[0]") + ' (Pyodide ' + py.version + ')'); return; }
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
