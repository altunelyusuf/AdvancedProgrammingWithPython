// Runs the chapter 13 examples under Pyodide 0.28.2 (the page's Python) with the page's own _run function, one after the other in ONE interpreter, in the order of the deck.
// Usage: node pyodide_probe_v2_0_0.js CODES.json OUT.json   (CODES.json = {"python": ..., "codes": [[id, code], ...]})  NODE_PATH must hold the pyodide package.
const fs = require('fs');
(async () => {
  const { loadPyodide } = require('pyodide');
  const py = await loadPyodide();
  await py.runPythonAsync(`import sys, io, ast
def _run(src, inp):
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
`);
  const ver = py.runPython("import sys; sys.version.split()[0]");
  const inp = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const out = {};
  for (const [id, code] of inp.codes) out[id] = py.globals.get('_run')(code, '');
  fs.writeFileSync(process.argv[3], JSON.stringify({ python: ver, out }, null, 1));
  console.log(ver, Object.keys(out).length, 'examples');
})();
