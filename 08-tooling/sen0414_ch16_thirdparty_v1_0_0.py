#!/usr/bin/env python3
"""Chapter 16 (SQLite Databases): runs the chapter's own programs, whole, under the given interpreter, and writes or checks their
recorded output.
What is fetched at run time and kept in a cache directory (CH16_CACHE, default the system temp directory): the chapter page
(https://automatetheboringstuff.com/3e/chapter16.html, its sha256 is compared with the chapterDigest of the book's own chapter
ontology), the zip of the 3rd edition's online materials (No Starch Press) that holds sweigartcats.db (sha256 41f0d0b5bc2e...), and the
official Linux build of the sqlite3 command-line shell, release 3.54.0 (SHA3-256 checked against the value on sqlite.org/download.html).
None of those files is stored in the repository. Environment variables CH16_DB and CH16_SQLITE3 name a local copy instead.
Not executed here: the three GUI apps, the Windows and macOS installation of the shell, a real power cut, a database on a network
file system. A line that starts with MEASURED is a timing; it is recorded and is not compared by the check.
Usage: sen0414_ch16_thirdparty_v1_0_0.py write|check <python>
Record: 08-tooling/ch16-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import json, os, subprocess, sys, tempfile
MODE, PY = sys.argv[1], sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch16-page", "third_party_record_v1_0_0.json")
GET = r'''import os, io, zipfile, hashlib, shutil, tempfile, urllib.request, html, re, json
UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0'
CACHE = os.environ.get('CH16_CACHE') or tempfile.gettempdir()
def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=120).read()
def chapter():
    p = os.path.join(CACHE, 'ch16_chapter.html')
    if not os.path.exists(p):
        open(p + '.part', 'wb').write(fetch('https://automatetheboringstuff.com/3e/chapter16.html')); os.replace(p + '.part', p)
    return open(p, 'rb').read()
def materials():
    p = os.path.join(CACHE, 'ch16_materials.zip')
    if not os.path.exists(p):
        open(p + '.part', 'wb').write(fetch('https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip')); os.replace(p + '.part', p)
    return p
def real_db():
    p = os.environ.get('CH16_DB') or os.path.join(CACHE, 'ch16_sweigartcats_41f0d0b5.db')
    if not os.path.exists(p):
        open(p + '.part', 'wb').write(zipfile.ZipFile(materials()).read('Automate_the_Boring_Stuff_3e_onlinematerials/sweigartcats.db')); os.replace(p + '.part', p)
    assert hashlib.sha256(open(p, 'rb').read()).hexdigest().startswith('41f0d0b5bc2e')
    return p
def cli():
    p = os.environ.get('CH16_SQLITE3') or os.path.join(CACHE, 'ch16_sqlite3_3540000')
    if not os.path.exists(p):
        z = fetch('https://sqlite.org/2026/sqlite-tools-linux-x64-3540000.zip')
        assert hashlib.sha3_256(z).hexdigest() == '283ee891049f180c74f56bab4fbcbc96e9acf3b3218a8b0d72771569a9cb8246'
        open(p + '.part', 'wb').write(zipfile.ZipFile(io.BytesIO(z)).read('sqlite3')); os.chmod(p + '.part', 0o755); os.replace(p + '.part', p)
    return p
def work(name='sweigartcats.db'):
    d = tempfile.mkdtemp(); shutil.copy(real_db(), os.path.join(d, name)); os.chdir(d); return d
def pres():
    h = chapter().decode('utf-8')
    return [html.unescape(re.sub(r'<[^>]+>', '', x)) for x in re.findall(r'<pre\b[^>]*>.*?</pre>', h, re.S)]
'''
REPLAY = r'''import sys, gc, contextlib
PRES = pres()
def parse(block):
    lines = block.rstrip('\n').split('\n'); items = []; cur = None
    def complete(t):
        try: compile(t + '\n', '<s>', 'single'); return True
        except SyntaxError as e:
            m = str(e)
            return not ('unterminated' in m or 'never closed' in m or 'EOF' in m or 'expected an indented' in m)
    for ln in lines:
        if ln.startswith('>>> ') or ln == '>>>':
            cur = {'src': ln[4:], 'out': [], 'open': True}; items.append(cur)
            if complete(cur['src']): cur['open'] = False
            continue
        if ln.startswith('...'):
            if cur is not None:
                cur['src'] += '\n' + ln[4:]
                if ln.strip() == '...': cur['open'] = False
                continue
        if cur is not None and cur['open']:
            sep = '' if cur['src'].endswith(' ') or ln.startswith(' ') else ' '
            cur['src'] += sep + ln
            if complete(cur['src']): cur['open'] = False
            continue
        if cur is not None: cur['out'].append(ln)
    return items
def norm(t): return re.sub(r'\s+', '', t)
def match(expected, got):
    e = norm('\n'.join(expected)); g = norm(got)
    e = re.sub(r'0x[0-9A-Fa-f]+', '0xADDR', e); g = re.sub(r'0x[0-9A-Fa-f]+', '0xADDR', g)
    if '3.xx.xx' in e: return 'placeholder'
    if '--snip--' in e:
        a, b = e.split('--snip--', 1)
        return 'match' if g.startswith(a) and g.endswith(b) else 'differs'
    return 'match' if e == g else 'differs'
d = work(); shipped = real_db(); ns = {'__name__': '__main__'}; rows = []
for bi in range(0, 44):
    if bi in (10, 30, 36):
        gc.collect()
        for f in ('sweigartcats.db', 'sweigartcats.db-journal'):
            if os.path.exists(f): os.remove(f)
        shutil.copy(shipped, 'sweigartcats.db')
    for it in parse(PRES[bi]):
        src = it['src']; buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(src + '\n', '<chapter>', 'single'), ns)
            got = buf.getvalue()
        except BaseException as e:
            got = buf.getvalue() + 'EXC %s: %s' % (type(e).__name__, e)
        exp = [l.replace('❶', '') for l in it['out']]
        rows.append((bi, src, '\n'.join(exp), got.rstrip('\n'), match(exp, got)))
from collections import Counter
c = Counter(r[4] for r in rows)
print('statements', len(rows), dict(sorted(c.items())))
for bi, src, exp, got, v in rows:
    if v != 'match':
        one = lambda s: re.sub(r'\s+', ' ', s)[:90]
        print('block %d %s | %s | printed: %s | got: %s' % (bi, v, one(src), one(exp), one(got)))
'''
PTY = r'''import pty, select, signal, time
def session(cmd, lines, delay=0.5):
    pid, fd = pty.fork()
    if pid == 0:
        os.execve(cmd[0], cmd, dict(os.environ, TERM='dumb'))
    out = b''
    def drain(t=delay):
        nonlocal out
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.05)
            if r:
                try: d = os.read(fd, 4096)
                except OSError: return
                if not d: return
                out += d
    drain(1.5)
    for ln in lines:
        os.write(fd, (ln + '\n').encode()); drain()
    os.write(fd, b'.quit\n'); drain(0.5)
    for _ in range(30):
        try: p, st = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError: break
        if p: break
        time.sleep(0.1)
    else:
        os.kill(pid, signal.SIGKILL); os.waitpid(pid, 0)
    return out.decode(errors='replace')
'''
PROGS = [
 ("The interpreter, the SQLite library it links and the shell of release 3.54.0", GET + r'''import sys, sqlite3
c = sqlite3.connect(':memory:')
print(sys.version.split()[0], 'sqlite', sqlite3.sqlite_version, 'threadsafety', sqlite3.threadsafety, 'has version attr:', hasattr(sqlite3, 'version'))
print(subprocess.run([cli(), '--version'], capture_output=True, text=True).stdout.strip()) if False else None
import subprocess
print(subprocess.run([cli(), '--version'], capture_output=True, text=True).stdout.split()[:2])
'''),
 ("The chapter page: size, sha256 against the chapterDigest of the book's chapter ontology, and what it holds", GET + r'''h = chapter(); d = hashlib.sha256(h).hexdigest()
P = pres(); t = h.decode('utf-8')
repl = [p for p in P if p.lstrip().startswith('>>>')]
print(len(h), d, d == 'b861ab3300b167a8ecb9c5882052315f3362cc74477f647462eb6d198b5b39a4')
print('pre blocks', len(P), 'interactive', len(repl), 'figures', sorted(set(re.findall(r'Figure 16-\d+', html.unescape(re.sub(r'<[^>]+>', '', t))))), 'images', len(re.findall(r'<img\b', t)), 'tables', len(re.findall(r'<table\b', t)))
print('statements', sum(1 for p in repl for ln in p.split('\n') if ln.startswith('>>> ')))
'''),
 ("The online materials of the 3rd edition: the zip and the two database files in it", GET + r'''p = materials(); b = open(p, 'rb').read()
z = zipfile.ZipFile(p)
print(len(b), hashlib.sha256(b).hexdigest())
for n in sorted(z.namelist()):
    if n.endswith('.db'):
        x = z.read(n); print(n.split('/')[-1], len(x), hashlib.sha256(x).hexdigest())
print(len([n for n in z.namelist() if not n.endswith('/')]), 'files')
'''),
 ("The shipped sweigartcats.db: what is in it", GET + r'''import sqlite3
work(); c = sqlite3.connect('file:sweigartcats.db?mode=ro', uri=True)
print(c.execute('SELECT count(*) FROM cats').fetchone(), c.execute('SELECT count(*) FROM vaccinations').fetchone(), c.execute('PRAGMA page_size').fetchone(), c.execute('PRAGMA journal_mode').fetchone(), c.execute('PRAGMA integrity_check').fetchone())
for r in c.execute('SELECT name, sql FROM sqlite_schema ORDER BY rowid'): print(r)
print(c.execute('SELECT rowid, * FROM cats WHERE rowid IN (1, 2, 3, 29)').fetchall())
print(c.execute("SELECT rowid, name FROM cats WHERE name LIKE '%y'").fetchall().__len__(), c.execute("SELECT rowid, name FROM cats WHERE name LIKE '%y' AND name = 'Trey'").fetchall())
print(c.execute('SELECT min(weight_kg), max(weight_kg), min(birthdate), max(birthdate) FROM cats').fetchone())
print(c.execute("SELECT count(DISTINCT fur) FROM cats").fetchone(), c.execute("SELECT fur, count(*) FROM cats GROUP BY fur ORDER BY count(*) DESC, fur LIMIT 3").fetchall())
'''),
 ("Every statement of the chapter's 44 interactive listings, replayed in order on Python and the shipped database, against the printed output", GET + REPLAY),
 ("A listing as the page wraps it: a line break inside a single-quoted string is a SyntaxError", r'''src = "import sqlite3\nconn = sqlite3.connect(':memory:')\nconn.execute('CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL,\nbirthdate TEXT, fur TEXT, weight_kg REAL) STRICT')\n"
try:
    exec(compile(src, '<listing>', 'exec'))
except SyntaxError as e:
    print(type(e).__name__, e.msg)
src2 = src.replace(',\nbirthdate', ', birthdate')
exec(compile(src2, '<listing>', 'exec')); print('joined line runs')
'''),
 ("The sqlite3 shell of release 3.54.0 with the chapter's session typed into standard input", GET + r'''import subprocess
os.chdir(tempfile.mkdtemp())
run = lambda s, *a: subprocess.run([cli(), 'example.db', *a], input=s, capture_output=True, text=True)
r = run("CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL,\nbirthdate TEXT, fur TEXT, weight_kg REAL) STRICT;\nINSERT INTO cats VALUES ('Zophie', '2021-01-24', 'gray tabby', 4.7);\nSELECT * from cats;\n.tables\n.headers on\nSELECT * from cats;\n")
print(r.stdout.rstrip('\n').split('\n'), r.returncode, repr(r.stderr))
print(run("SELECT * from cats\n").stdout.split('\n'))
print(run('.mode\n').stdout.strip())
print(run('.dump\n').stdout.split('\n')[:4])
'''),
 ("The same shell in a terminal (a pseudo-terminal): banner, prompt and result format", GET + PTY + r'''os.chdir(tempfile.mkdtemp())
t = session([cli(), 'example.db'], ['CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL,', 'birthdate TEXT, fur TEXT, weight_kg REAL) STRICT;', "INSERT INTO cats VALUES ('Zophie', '2021-01-24', 'gray tabby', 4.7);", 'SELECT * from cats', ';', '.tables', '.headers on', 'SELECT * from cats;'])
print(re.sub(r'\x1b\[[0-9;]*m', '', t).replace('\r', ''))
'''),
 ("python -m sqlite3 as a shell, with the chapter's statements on standard input", r'''import subprocess, sys, tempfile, os
os.chdir(tempfile.mkdtemp())
r = subprocess.run([sys.executable, '-m', 'sqlite3', 'example.db'], input="CREATE TABLE IF NOT EXISTS cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT;\nINSERT INTO cats VALUES ('Zophie', '2021-01-24', 'gray tabby', 4.7);\nSELECT * from cats;\n.version\n", capture_output=True, text=True)
print(r.returncode, r.stdout.split('\n'), r.stderr.split('\n')[:2])
v = subprocess.run([sys.executable, '-m', 'sqlite3', '-v'], capture_output=True, text=True); print(v.stdout.strip())
'''),
 ("The chapter's index claims, measured: 300000 rows, a scan against a search, and the price in inserts", r'''import sqlite3, time, random
c = sqlite3.connect(':memory:', isolation_level=None)
c.execute('CREATE TABLE cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT')
random.seed(1); rows = [('n%d' % random.randrange(10**6), '2020-01-01', 'x', 1.0) for _ in range(300000)]
c.execute('BEGIN'); t = time.perf_counter(); c.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', rows); plain = time.perf_counter() - t; c.execute('COMMIT')
def look():
    s = time.perf_counter()
    for i in range(50): c.execute('SELECT * FROM cats WHERE name = ?', ['n%d' % i]).fetchall()
    return (time.perf_counter() - s) / 50
scan = look(); c.execute('CREATE INDEX idx_name ON cats (name)'); seek = look()
d = sqlite3.connect(':memory:', isolation_level=None)
d.execute('CREATE TABLE cats (name TEXT NOT NULL, birthdate TEXT, fur TEXT, weight_kg REAL) STRICT'); d.execute('CREATE INDEX idx_name ON cats (name)'); d.execute('CREATE INDEX idx_birthdate ON cats (birthdate)')
d.execute('BEGIN'); t = time.perf_counter(); d.executemany('INSERT INTO cats VALUES (?, ?, ?, ?)', rows); indexed = time.perf_counter() - t; d.execute('COMMIT')
print('lookup faster by more than 100 times:', scan / seek > 100, '| inserts slower with two indexes:', indexed > plain)
print('MEASURED scan %.2f ms, search %.4f ms, ratio %.0f; 300000 inserts %.2f s plain, %.2f s with two indexes (%.1f times)' % (scan * 1000, seek * 1000, scan / seek, plain, indexed, indexed / plain))
'''),
 ("The chapter's claim that an in-memory database is much faster, measured on 2000 single inserts", r'''import sqlite3, time, os, tempfile
os.chdir(tempfile.mkdtemp())
def go(name, level, many=False):
    c = sqlite3.connect(name, isolation_level=level); c.execute('CREATE TABLE t (a INTEGER, b TEXT) STRICT')
    t = time.perf_counter()
    if level is None:
        for i in range(2000): c.execute('INSERT INTO t VALUES (?, ?)', (i, 'x'))
    else:
        for i in range(2000): c.execute('INSERT INTO t VALUES (?, ?)', (i, 'x'))
        c.commit()
    return time.perf_counter() - t
mem_auto = go(':memory:', None); file_auto = go('a.db', None); mem_one = go(':memory:', ''); file_one = go('b.db', '')
print('autocommit: file slower than memory:', file_auto > mem_auto, '| one transaction: file within 3 times of memory:', file_one < 3 * mem_one + 0.05)
print('MEASURED 2000 inserts, autocommit: memory %.3f s, file %.3f s; one transaction: memory %.4f s, file %.4f s' % (mem_auto, file_auto, mem_one, file_one))
'''),
 ("The chapter's limit, many simultaneous writers: 100 and then 1000 processes insert 5 rows each into one file, rollback journal and WAL", r'''import sqlite3, time, os, tempfile, multiprocessing as mp
os.chdir(tempfile.mkdtemp())
def writer(path, k, q):
    err = 0
    c = sqlite3.connect(path, timeout=60, isolation_level=None)
    for j in range(5):
        try: c.execute('INSERT INTO t VALUES (?, ?)', (k, j))
        except sqlite3.OperationalError: err += 1
    q.put(err)
def trial(mode, n=100):
    path = mode + str(n) + '.db'; c = sqlite3.connect(path, isolation_level=None)
    c.execute('PRAGMA journal_mode=' + mode.replace('1000', '')); c.execute('CREATE TABLE t (w INTEGER, j INTEGER) STRICT'); c.close()
    ctx = mp.get_context('fork'); q = ctx.Queue(); ps = [ctx.Process(target=writer, args=(path, k, q)) for k in range(n)]
    t = time.perf_counter(); [p.start() for p in ps]; errs = sum(q.get() for _ in ps); [p.join() for p in ps]; dt = time.perf_counter() - t
    c = sqlite3.connect(path); n_rows = c.execute('SELECT count(*) FROM t').fetchone()[0]
    return n_rows, errs, dt
small = {m: trial(m, 100) for m in ('DELETE', 'WAL')}
print('100 writers, rows and errors:', {m: (r[0], r[1]) for m, r in small.items()})
big = {m: trial(m, 1000) for m in ('DELETE', 'WAL')}
print('1000 writers, rows plus errors equal 5000:', {m: r[0] + r[1] == 5000 for m, r in big.items()})
print('MEASURED 100 writers: ' + ', '.join('%s %d rows %d errors %.2f s' % (m, r[0], r[1], r[2]) for m, r in small.items()) + '; 1000 writers: ' + ', '.join('%s %d rows %d errors %.2f s' % (m, r[0], r[1], r[2]) for m, r in big.items()))
'''),
 ("connect() with positional arguments after the first, the old version attributes and the default adapters under -W error", r'''import sqlite3, warnings, datetime
res = []
for label, f in (('connect positional timeout', lambda: sqlite3.connect(':memory:', 5.0)), ('sqlite3.version', lambda: sqlite3.version), ('date adapter', lambda: sqlite3.connect(':memory:').execute('SELECT ?', (datetime.date(2035, 10, 31),)).fetchone())):
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        try: f(); res.append((label, 'no warning'))
        except Exception as e: res.append((label, type(e).__name__, str(e)[:70]))
for r in res: print(r)
'''),
]
def run(code):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1"); env.pop("PYTHONPATH", None)
    r = subprocess.run([PY, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=900, cwd=tempfile.mkdtemp())
    o = (r.stdout if r.returncode == 0 else r.stdout + "FAILED: " + (r.stderr.strip().splitlines() or ["?"])[-1]).rstrip("\n")
    import re
    return re.sub(r"0x[0-9a-f]{6,}", "0x...", o)   # the address of an object differs from run to run
out = [{"what": w, "code": c, "output": run(c)} for w, c in PROGS]
strip = lambda s: "\n".join(l for l in s.split("\n") if not l.startswith("MEASURED"))
if MODE == "write":
    ver = subprocess.run([PY, "-c", "import sys, sqlite3; print(sys.version.split()[0], 'sqlite', sqlite3.sqlite_version)"], capture_output=True, text=True).stdout.strip()
    json.dump({"_version": "1.0.0", "_note": "Recorded by sen0414_ch16_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter named in the field python. The chapter page, the online materials and the shell are fetched at run time and not kept in the repository. A line that starts with MEASURED is a timing on the machine of the day.", "python": ver, "items": out}, open(REC, "w"), indent=1, ensure_ascii=False)
    print("recorded", len(out), "programs to", REC)
    for o in out:
        if "FAILED" in o["output"]: print("  FAILED:", o["what"], "|", o["output"][-200:])
else:
    old = json.load(open(REC))["items"]; bad = [a["what"] for a, b in zip(old, out) if strip(a["output"]) != strip(b["output"]) or a["code"] != b["code"]]
    print("%d programs; %d differ" % (len(out), len(bad)))
    for b in bad: print("  DIFFERS", b)
    sys.exit(1 if bad else 0)
