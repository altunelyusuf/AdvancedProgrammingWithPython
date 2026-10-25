// Runs the chapter 11 examples under Pyodide 0.28.2 (the Python of the page template 9.52.2) with the page's own _run function (copied from the template),
// one after the other in ONE interpreter, in manifest order (as the page's chapter-code tab runs them).
// Usage: node pyodide_probe_v2_0_0.js CODES.json OUT.json   (CODES.json = {"codes": [[name, code], ...]})   NODE_PATH must hold the pyodide package.
const fs = require('fs');
(async () => {
  const { loadPyodide } = require('pyodide');
  const py = await loadPyodide();
  await py.runPythonAsync(`import sys, io, ast
def _run(src, inp):
    _hook = globals().get('_before_run')
    if _hook: _hook()
    import logging; [logging.root.removeHandler(_h) for _h in logging.root.handlers[:]]; logging.root.setLevel(logging.WARNING); logging.disable(logging.NOTSET)
    _o = io.StringIO(); _lines = iter(inp.split(chr(10))) if inp else iter([])
    def _input(prompt=''):
        v = next(_lines, ''); print(str(prompt) + v); return v
    ns = {'input': _input, '__name__': '__main__'}
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
