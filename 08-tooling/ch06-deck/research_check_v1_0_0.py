"""Re-executes, under the interpreter it is run with, every checkable claim of the chapter 6 research data file: the input/output example of each
taxonomy leaf, the CLAIMS, and every behaviour program in BEH against its recorded output. The deck builds on this research, so the build stops when
any of it no longer holds. Usage: research_check_v1_0_0.py   (run under the Python the course teaches)"""
__version__ = "1.0.0"
import os, platform, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sen0414_ch06_rdodi_data_v1_0_0 as R
bad = []; n = 0
for t in R.TAX:
    if t[5]:
        n += 1; got = repr(eval(t[5][0], {}))
        if got != t[5][1]: bad.append(("TAX", t[2], t[5][0][:50], got, t[5][1]))
for e, want in R.CLAIMS:
    n += 1; got = repr(eval(e, {}))
    if got != want: bad.append(("CLAIM", e[:50], got, want))
for title, code, want in R.BEH:
    n += 1; r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True); got = r.stdout.rstrip("\n")
    if got != want or r.returncode: bad.append(("BEH", title, got[:80], want[:80], r.stderr[-120:]))
print("%d research items re-executed under Python %s; %d differ from the record" % (n, platform.python_version(), len(bad)))
for b in bad: print("  DIFFERS", b)
sys.exit(1 if bad else 0)
