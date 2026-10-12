#!/usr/bin/env python3
"""Chapter 16: runs one sqlite3 program, the chapter's operations in a row, under every installed 3.14 patch release (3.14.0 to 3.14.6,
`uv python install 3.14.N`) and, for comparison, under 3.13, 3.12 and 3.11, and records what each printed. It answers the question
chapters 13 to 15 answered with a difference: does anything the chapter teaches change between the patch releases of Python 3.14, and
between 3.14 and the releases before it? The SQLite library each interpreter links is part of the answer, because it is not the same
one: it is recorded for every release.
The program needs the shipped sweigartcats.db (fetched and checked by the helper code of sen0414_ch16_thirdparty_v1_0_0.py, kept in
the system temp directory) for the one step that dumps it. python runs in isolated mode, each interpreter by `uv run --no-project`.
Usage: sen0414_ch16_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch16-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch16-page", "interpreter_record_v1_0_0.json")
GET = re.search(r"GET = r'''(.*?)'''\n", open(os.path.join(HERE, "sen0414_ch16_thirdparty_v1_0_0.py"), encoding="utf-8").read(), re.S).group(1)
PROG = GET + r'''
import sys, sqlite3, warnings, gc, datetime
d = work()
res = {}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except Exception as e: v = type(e).__name__ + ': ' + str(e)[:60]
        gc.collect()
    return [v, sorted({x.category.__name__ for x in seen})]
res['series'] = sys.version.split()[0].rsplit('.', 1)[0] + '.x'
res['sqlite'] = sqlite3.sqlite_version
res['version attribute'] = hasattr(sqlite3, 'version')
_x = sqlite3.connect(':memory:'); res['autocommit attribute'] = hasattr(_x, 'autocommit'); _x.close()
_x = sqlite3.connect(':memory:'); res['isolation_level default'] = repr(_x.isolation_level); _x.close()
def one(f, *a, **k):
    m = sqlite3.connect(':memory:', *a, **k)
    try: return f(m)
    finally: m.close()
res['positional timeout'] = w(lambda: (sqlite3.connect(':memory:', 5.0).close(), 'ok')[1])
res['named placeholder with a sequence'] = w(lambda: one(lambda m: m.execute('SELECT :a', [1]).fetchone()))
res['date adapter'] = w(lambda: one(lambda m: m.execute('SELECT ?', (datetime.date(2035, 10, 31),)).fetchone()))
res['unclosed connection'] = w(lambda: (sqlite3.connect(':memory:'), 'made')[1])
_x = sqlite3.connect(':memory:'); res['autocommit attribute'] = hasattr(_x, 'autocommit'); _x.close()
c = sqlite3.connect(':memory:', isolation_level=None)
c.execute('CREATE TABLE cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')
c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', [('Zophie', '2021-01-24', 'black', 5.6), ('Miguel', '2016-12-24', 'siamese', 6.2)])
res['strict: a row with only a name is stored'] = c.execute("INSERT INTO cats (name) VALUES ('x')").rowcount
def bad():
    try: c.execute("INSERT INTO cats VALUES ('y', 1, 2, 'heavy')")
    except sqlite3.IntegrityError as e: return str(e)
res['strict refusal'] = bad()
res['rowid and star'] = [[x[0] for x in c.execute('SELECT * FROM cats').description], c.execute('SELECT rowid, name FROM cats LIMIT 1').fetchone()]
res['iterdump of a small database'] = w(lambda: len(list(c.iterdump())))
def shipped_dump():
    s = sqlite3.connect('sweigartcats.db')
    try: return len(list(s.iterdump()))
    finally: s.close()
res['iterdump of the shipped database'] = w(shipped_dump)
def fk():
    s = sqlite3.connect('sweigartcats.db', isolation_level=None)
    try:
        s.execute('PRAGMA foreign_keys = ON'); s.execute('INSERT INTO vaccinations VALUES (?, ?, ?, ?)', ('rabies', '2023-06-06', 'Dr. Echo', 1)); return 'inserted'
    finally: s.close()
res['foreign key on rowid'] = w(fk)
k = sqlite3.connect('sweigartcats.db', isolation_level=None)
res['shipped counts'] = [k.execute('SELECT count(*) FROM cats').fetchone()[0], k.execute('SELECT count(*) FROM vaccinations').fetchone()[0]]
res['like y'] = len(k.execute("SELECT rowid, name FROM cats WHERE name LIKE '%y'").fetchall())
res['index and plan'] = [r[3] for r in c.execute("EXPLAIN QUERY PLAN SELECT * FROM cats WHERE name = 'Zophie'")]
if res['autocommit attribute']:
    a = sqlite3.connect('sweigartcats.db', autocommit=True)
    a.execute('BEGIN'); a.execute("INSERT INTO cats VALUES ('Temp', '2024-01-01', 'x', 1)"); a.rollback()
    res['autocommit=True rollback leaves the row'] = a.execute("SELECT count(*) FROM cats WHERE name = 'Temp'").fetchone()[0]; a.close()
else:
    res['autocommit=True rollback leaves the row'] = 'no attribute'
for key in sorted(res): print(key, '=', json.dumps(res[key], ensure_ascii=False))
'''
def uv(v, prog):
    return subprocess.run(["uv", "run", "--no-project", "--python", v, "python", "-I", "-c", prog], capture_output=True, text=True, timeout=900, env={k: x for k, x in os.environ.items() if k != "UV_NATIVE_TLS"})
rows = []; parsed = {}
for v in ("3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.13", "3.12", "3.11"):
    r = uv(v, PROG)
    first = subprocess.run(["uv", "run", "--no-project", "--python", v, "python", "-I", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True, timeout=300, env={k: x for k, x in os.environ.items() if k != "UV_NATIVE_TLS"}).stdout.strip()
    out = r.stdout.strip() if r.returncode == 0 else "FAILED: " + (r.stderr.strip().splitlines() or ["?"])[-1]
    rows.append([first, out]); print(first, "ok" if r.returncode == 0 else out)
    if r.returncode == 0: parsed[first] = dict(l.split(" = ", 1) for l in out.split("\n"))
keys = sorted(next(iter(parsed.values())))
differ = {k: {v: p.get(k) for v, p in parsed.items()} for k in keys if len({p.get(k) for p in parsed.values()}) > 1 and k != "series"}
same = [k for k in keys if k not in differ and k != "series"]
sqlite_by = {v: json.loads(p["sqlite"]) for v, p in parsed.items()}
json.dump({"_version": "1.0.0", "program_after_the_helper_code": PROG[len(GET):].strip(), "interpreters": sorted(parsed), "sqlite_library_by_interpreter": sqlite_by,
           "items_that_differ_between_interpreters": differ, "items_equal_in_all": same,
           "rows": ["%s | %s" % (r[0], r[1].replace("\n", " / ")) for r in rows],
           "_note": "Run on %s with each interpreter installed by uv; python runs in isolated mode. The SQLite library an interpreter links is the one of its build (see sqlite_library_by_interpreter), not a choice of this script. Each warning is recorded, not turned into an error. Python 3.11 is included because the chapter says STRICT's SQLite version is 'used by Python 3.11 and later'." % datetime.date.today().isoformat()},
          open(OUT, "w"), indent=1, ensure_ascii=False)
print("interpreters:", len(parsed), "| items that differ:", sorted(differ), "| equal in all:", len(same))
print(sqlite_by)
