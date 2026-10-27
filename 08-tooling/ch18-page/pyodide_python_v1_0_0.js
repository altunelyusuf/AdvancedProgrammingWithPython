// A "python" command that runs under Pyodide 0.28.2 (CPython 3.13), the interpreter of the page template 9.52.3, with the four pure-Python wheels of the chapter 18 page
// (defusedxml 0.7.1, et_xmlfile 2.0.0, openpyxl 3.1.5, xmltodict 1.0.4) unpacked from 03-materials/ch18/assets the way the page unpacks them, and lxml from Pyodide's own
// distribution (data.py_packages). It understands exactly what the page-data builder 2.25.0 asks of its interpreter: `--version` and `-c CODE [ARG...]`.
// Used so the recorded results of the page's observed programs come from the page's own runtime. Needs node and the npm package pyodide@0.28.2 on NODE_PATH.
// Usage: node pyodide_python_v1_0_0.js WHEEL_DIR (--version | -c CODE [ARG...])
const fs = require('fs'), path = require('path');
(async () => {
  const wheelDir = process.argv[2], rest = process.argv.slice(3);
  const { loadPyodide } = require('pyodide');
  const py = await loadPyodide();
  if (rest[0] === '--version') { console.log('Python ' + py.runPython("import sys; sys.version.split()[0]") + ' (Pyodide ' + py.version + ')'); return; }
  const SITE = py.runPython("import sysconfig;sysconfig.get_path('purelib')");
  await py.loadPackage('lxml', { messageCallback: () => {}, errorCallback: (m) => process.stderr.write(m + '\n') });
  for (const w of ['et_xmlfile-2.0.0-py3-none-any.whl', 'openpyxl-3.1.5-py2.py3-none-any.whl', 'defusedxml-0.7.1-py2.py3-none-any.whl', 'xmltodict-1.0.4-py3-none-any.whl'])
    py.unpackArchive(new Uint8Array(fs.readFileSync(path.join(wheelDir, w))), 'wheel', { extractDir: SITE });
  py.runPython("import importlib;importlib.invalidate_caches()");
  if (rest[0] !== '-c') { console.error('only --version and -c are supported'); process.exit(2); }
  py.globals.set('_code', rest[1]); py.globals.set('_argv', ['-c'].concat(rest.slice(2)));
  const out = [];
  py.setStdout({ write: (b) => { out.push(Buffer.from(b)); return b.length; } });
  try { py.runPython("import sys\nsys.argv = list(_argv)\nexec(compile(_code, '<string>', 'exec'), {'__name__': '__main__'})"); }
  catch (e) { process.stderr.write(String(e) + '\n'); process.exit(1); }
  process.stdout.write(Buffer.concat(out));
})();
