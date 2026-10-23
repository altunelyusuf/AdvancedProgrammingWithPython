import os,re,subprocess,sys,tempfile
TOOL="/home/claude/AdvancedProgrammingWithPython/08-tooling"; REPO=os.path.dirname(TOOL)
PY="/home/claude/venv314/bin/python"
n=sys.argv[1]; pv=sys.argv[2]; test=sys.argv[3]
d=tempfile.mkdtemp(prefix="page_test_")
r=subprocess.run([sys.executable,os.path.join(TOOL,"sen0414_page_key_substitute_v1_0_0.py"),n,pv,d],capture_output=True,text=True); print(r.stdout+r.stderr)
env=dict(os.environ,PAGE=os.path.join(d,"page.html"),RESULTS=os.path.join(d,"results.json"),PAGE_VER=pv,KEY=os.path.join(d,"test_key.json"),PYTHONDONTWRITEBYTECODE="1")
r=subprocess.run([PY,os.path.join(TOOL,test),n],capture_output=True,text=True,env=env,cwd=REPO)
print(r.stdout+r.stderr); print("exit",r.returncode)
