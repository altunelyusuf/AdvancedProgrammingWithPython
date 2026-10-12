#!/usr/bin/env python3
"""Chapter 15: runs one EZSheets program, the chapter's operations in a row, under every installed 3.14 patch release (3.14.0 to
3.14.6, `uv python install 3.14.N`) and, for comparison, under 3.13 and 3.12, and records what each printed. It answers the question
chapter 13 and chapter 14 answered with a difference: does anything the chapter teaches change between the patch releases of Python
3.14? A second table runs one session under three releases of ezsheets (2024.8.9, 2025.11.11, 2026.4.28) on Python 3.14.6, because the
chapter prints '30' where the newest releases return the integer 30.
Google is not reached: the program uses the stand-in for Google's API that sen0414_ch15_thirdparty_v1_0_0.py carries (class G), so
what is compared is the library and the interpreter, not Google. ezsheets is installed for each run by uv (`uv run --with
ezsheets==VERSION`), no project is read, and python runs in isolated mode.
Usage: sen0414_ch15_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch15-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch15-page", "interpreter_record_v1_0_0.json")
FAKE = re.search(r"FAKE = r'''(.*?)'''\n", open(os.path.join(HERE, "sen0414_ch15_thirdparty_v1_0_0.py"), encoding="utf-8").read(), re.S).group(1)
PROG = FAKE + r'''
import sys, os, tempfile, pickle, warnings, time, collections
os.chdir(tempfile.mkdtemp())
warnings.simplefilter('error')
g = install()
ss = ezsheets.Spreadsheet(); ss.title = 'Compare'; sheet = ss.sheets[0]
sheet['A1'] = 'Name'; sheet['B1'] = 'Age'; sheet['A2'] = 'Alice'; sheet['B2'] = 30
print(sys.version.split()[0].rsplit('.', 1)[0] + '.x', ezsheets.__version__)
print(ss.sheetTitles, repr(sheet['A1']), repr(sheet[2, 1]), repr(sheet['A9']), repr(sheet['B2']))
print(ezsheets.convertAddress('A2'), ezsheets.convertAddress(1, 2), ezsheets.getColumnLetterOf(999), ezsheets.getColumnNumberOf('ZZZ'))
print(repr(ss.Sheet('Spam')), type(ss.createSheet('Eggs')).__name__, ss.sheetTitles)
rows = [['PRE-MINE', 'Al Sweigart', '1000000000'], ['Al Sweigart', 'Miles Bron', '19116'], ['Miles Bron', 'not_a_scammer', '118']]
sheet.updateRows(rows); sheet.rowCount = 3
acc = {}
for row in sheet.getRows():
    s, r, a = row[0], row[1], int(row[2]); acc.setdefault(r, 0)
    if s != 'PRE-MINE': acc.setdefault(s, 0); acc[s] -= a
    acc[r] += a
print(acc, sum(acc.values()))
sleeps = []; time.sleep = sleeps.append; ezsheets.IGNORE_QUOTA = False; g.fail = [(429, 'RESOURCE_EXHAUSTED')] * 20
try:
    ezsheets.Spreadsheet()
except Exception as e:
    print(type(e).__name__, len(g.log), sleeps)
print(pickle.DEFAULT_PROTOCOL, ezsheets.getIdFromUrl('https://docs.google.com/spreadsheets/d/ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ab'))
try:
    ss.id = 'x'
except AttributeError as e:
    print(e)
print(sys.version.split()[0] in ('3.14.0', '3.14.1', '3.14.2', '3.14.3', '3.14.4', '3.14.5', '3.14.6') or 'older interpreter')
'''
SESSION = FAKE + r'''
g = install(); sheet = ezsheets.Spreadsheet().sheets[0]
sheet['A2'] = 'Alice'; sheet['B2'] = 30
print(ezsheets.__version__, repr(sheet['B2']), type(sheet['B2']).__name__)
'''
def uv(v, prog, extra):
    return subprocess.run(["uv", "run", "--no-project", "--python", v] + extra + ["python", "-I", "-c", prog], capture_output=True, text=True, timeout=900)
rows = []
for v in ("3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.13", "3.12"):
    r = uv(v, PROG, ["--with", "ezsheets==2026.4.28"])
    first = subprocess.run(["uv", "run", "--no-project", "--python", v, "python", "-I", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True, timeout=300).stdout.strip()
    rows.append([first, r.stdout.strip() if r.returncode == 0 else "FAILED: " + (r.stderr.strip().splitlines() or ["?"])[-1]])
    print(rows[-1][0], "ok" if r.returncode == 0 else "FAILED")
body = [re.sub(r"(?m)^\d (ABCDEF)", r"N \1", r[1].split("\n", 1)[1].rsplit("\n", 1)[0]) for r in rows]
proto = {r[0]: re.search(r"(?m)^(\d) ABCDEF", r[1]).group(1) for r in rows}
rel = []
for ver in ("2024.8.9", "2025.11.11", "2026.4.28"):
    r = uv("3.14.6", SESSION, ["--with", "ezsheets==" + ver])
    rel.append(r.stdout.strip() if r.returncode == 0 else "FAILED: " + (r.stderr.strip().splitlines() or ["?"])[-1]); print(rel[-1])
json.dump({"_version": "1.0.0", "program": PROG.strip(), "rows": ["%s | %s" % (r[0], r[1].replace("\n", " / ")) for r in rows],
           "all_bodies_equal_with_the_pickle_protocol_masked": len(set(body)) == 1, "pickle_default_protocol": proto, "ezsheets_releases_on_3.14.6": rel,
           "_note": "Run on %s with each interpreter installed by uv and ezsheets 2026.4.28, against the stand-in for Google's API of sen0414_ch15_thirdparty_v1_0_0.py (Google was not reached), every warning an error. The first line of each output names the series; the last line says whether the interpreter is one of the seven 3.14 releases; the one value that differs between series is pickle.DEFAULT_PROTOCOL (5 from 3.14, 4 before), which is the protocol of the token files ezsheets writes. The second table is the cell session under three releases of ezsheets on Python 3.14.6: the stand-in keeps cells as text, so the difference between '30' and 30 is made by the library's own cache." % datetime.date.today().isoformat()}, open(OUT, "w"), indent=1)
print("all bodies equal with the pickle protocol masked:", len(set(body)) == 1, proto)
