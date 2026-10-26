const fs=require('fs');
(async()=>{const {loadPyodide}=require('pyodide');const py=await loadPyodide();
await py.runPythonAsync(`import sys, io, ast
def _run(src, inp):
    _o = io.StringIO(); ns = {'__name__': '__main__'}; old = sys.stdout; sys.stdout = _o
    try:
        t = ast.parse(src)
        if t.body and isinstance(t.body[-1], ast.Expr):
            last = ast.Expression(t.body.pop().value); exec(compile(t, '<code>', 'exec'), ns); v = eval(compile(last, '<code>', 'eval'), ns)
            if v is not None: print(repr(v))
        else: exec(compile(t, '<code>', 'exec'), ns)
    except Exception as e: print(type(e).__name__ + ': ' + str(e))
    finally: sys.stdout = old
    return _o.getvalue().rstrip()
`);
const inp=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));const run=py.globals.get('_run');
const [v,o]=inp.codes.map(x=>x[1]);
console.log('1 original, fresh      :',run(o,''));
console.log('2 variant chr(____)    :',run(v,''));
console.log('3 original, after 2    :',run(o,''));
console.log('expected               :',inp.outs['Import result']);
})();
