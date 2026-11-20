import sys, io, contextlib, os, tempfile, importlib.util
def load(path,name):
    sp=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
old=load("examples_v2_0_0.py","old"); new=load("spec_v3_0_0/examples_v3_0_0.py","new")
home=os.getcwd()
def run(e):
    code="\n".join(l for g in e["groups"] for l in g[0]); buf=io.StringIO()
    os.chdir(tempfile.mkdtemp())
    try:
        with contextlib.redirect_stdout(buf): exec(code,{})
    except Exception as ex: buf.write("ERR "+repr(ex))
    os.chdir(home); return buf.getvalue()
bad=0
assert [e["id"] for e in old.EXAMPLES]==[e["id"] for e in new.EXAMPLES]
for a,b in zip(old.EXAMPLES,new.EXAMPLES):
    ra,rb=run(a),run(b)
    if ra!=rb: bad+=1; print("DIFF",a["id"]); print(" old:",ra[:200]); print(" new:",rb[:200])
print("examples",len(new.EXAMPLES),"different",bad)
