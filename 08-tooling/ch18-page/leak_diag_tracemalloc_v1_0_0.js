(async()=>{
const fs=require('fs');const {loadPyodide}=require('pyodide');const py=await loadPyodide();
const man=JSON.parse(fs.readFileSync('/tmp/sen0414_i20_ch18_own/leak/programs.json'));
const code=man.examples.find(e=>e.name==='IterparseClear').code;
const run=(c)=>{try{return py.runPython('repr(eval(compile('+JSON.stringify(c)+',"<c>","eval"),{}))')}catch(e){return 'ERR '+String(e).split('\n').slice(-2)[0]}};
const diag=code.replace("out = (a[0], a[0] == b[0], b[1] > 1.5 * a[1])", "out = (a, b, tracemalloc.is_tracing())");
console.log('fresh real :',run(code));
console.log('probe total(____):',run(code.replace('def total(clear)','def total(____)')));
console.log('tracing after probe:',py.runPython('import tracemalloc;tracemalloc.is_tracing()'), py.runPython('tracemalloc.get_traced_memory()'));
console.log('diag after :',run(diag));
console.log('probe again, then real:',run(code.replace('def total(clear)','def total(____)')), run(code));
})();
