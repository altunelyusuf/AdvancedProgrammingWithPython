"""Chapter 25 deck examples: every console session, whole program (or excerpt), picture, chart and table the lecture deck shows. Nothing here
carries a result; examples_run_v1_0_0.py runs it all under the interpreter given (the uv Python 3.14.6 of the chapter 25 research environment
/home/claude/venv314_ch25_latest: requests 2.34.2 and beautifulsoup4 4.15.0; the rest is the standard library) and records the results. A console group is one
session: its rows run in order in one namespace (the deck check re-runs them per slide, one namespace per slide). Every console row uses the standard library only,
writes no file and reads no clock and no network.

Programs: the 'Cut' programs written for the deck. Each one is a whole program (or a downloader whose book listing is shown as an honest excerpt), small enough
to be run again by the program check. A program that waits (a sleep, a join with a timeout) prints only what does not depend on how long it took: a list, a name, an
error message, a count, or a boolean such as "both threads still alive after 0.5 s". EVERY TIMING OF THE RESEARCH (seconds for a loop, microseconds to start a thread)
is NOT printed by any program here: those figures are read from ch25-page/timing_record_v1_0_0.json, were measured once on 2026-10-14 on a machine whose load average was
below 1.0, and are marked Recorded on their slides; the deck never times them again.
KIND says what a program's output depends on, so that honesty_check can require the matching words on the slide that shows it:
  standin   the output comes from a LOCAL STAND-IN: the book's xkcd downloader run against an HTTP server of this program on 127.0.0.1; xkcd.com is never contacted.
  plain     the output comes from the interpreter alone.
A program whose transcript differs between two runs is refused by the runner, which runs every program twice. The picture the fixed downloader draws is saved by the
program with done() (a PNG written with zlib, no imaging library), named, sized and hashed in the program's own transcript."""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FTPATH = "/root/.local/share/uv/python/cpython-3.14.6+freethreaded-linux-x86_64-gnu/bin/python3.14t"

CONSOLES = {
    "title": ["import platform, sys, threading", "platform.python_version()", "sys._is_gil_enabled()", "threading.current_thread().name",
              "threading.active_count()"],
    "inc": ["import dis", "def inc(): global c; c += 1", "ops = [i.opname for i in dis.get_instructions(inc)][1:-1]", "len(ops)", "ops[:4]"],
    "locals": ["import threading", "tl = threading.local()", "def put(): tl.x = 1", "t = threading.Thread(target=put); t.start(); t.join()", "hasattr(tl, 'x')"],
    "pins": ["import os, sys, sysconfig", "sys._is_gil_enabled()", "sysconfig.get_config_var('Py_GIL_DISABLED')", "os.cpu_count()"],
}

# ---- programs written for the deck (Cuts) ---------------------------------------------------------------------------------------
START = r"""import threading, time
print('Start of program.')
def takeANap():
    time.sleep(0.5)
    print('Wake up!')
threadObj = threading.Thread(target=takeANap)
threadObj.start()
print('End of program.')
threadObj.join()
box = []
def f():
    me = threading.current_thread()
    box.append((me.name, threading.active_count()))
t = threading.Thread(target=f); t.start(); t.join()
main = threading.current_thread()
print(main.name, main is threading.main_thread(), box[0])
"""

ARGS = r"""import threading
def go(sep):
    t = threading.Thread(target=print, kwargs={'sep': sep},
                         args=['Cats', 'Dogs', 'Frogs'])
    t.start(); t.join()
go(' & ')
go('& ')
t = threading.Thread(target=print('Now', 'not later'))
t.start(); t.join()
print('the thread had a target to run:', t.is_alive())
"""

LIFE = r"""import threading
def f(): pass
a = threading.Thread(target=f)
b = threading.Thread(target=f)
c = threading.Thread(target=f, name='copier')
print(a.name, '|', b.name, '|', c.name)
a.start(); a.join()
try:
    a.start()
except RuntimeError as e:
    print('RuntimeError:', e)
def boom():
    raise ValueError('boom')
threading.excepthook = lambda a: print('hook:', repr(a.exc_value))
t = threading.Thread(target=boom); t.start(); t.join()
print('main continues')
"""

JOIN = r"""import threading, time
t = threading.Thread(target=time.sleep, args=[0.6]); t.start()
r = t.join(0.1)
print('join(0.1) returned', r, '| alive:', t.is_alive())
t.join()
print('join() waited | alive:', t.is_alive())
u = threading.Thread(target=print)
try:
    u.join()
except RuntimeError as e:
    print('RuntimeError:', e)
"""

DAEMON = r"""import subprocess, sys, threading, time
tmpl = '''import threading, time
def f():
    time.sleep(0.5); print('late')
threading.Thread(target=f, daemon=%s).start()
print('end')'''
for flag in (True, False):
    r = subprocess.run([sys.executable, '-c', tmpl % flag],
                       capture_output=True, text=True)
    print('daemon=%s prints' % flag, r.stdout.split())
t = threading.Thread(target=time.sleep, args=[0.2]); t.start()
try:
    t.daemon = True
except RuntimeError as e:
    print('RuntimeError:', e)
"""

_SRV = r"""import os, struct, subprocess, sys, tempfile, threading, zlib, http.server
hits = []
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        hits.append(self.path)
        if self.path.startswith('/img/'): body, ct = b'x' * 100, 'image/png'
        else:
            n = self.path.strip('/')
            body = ('<div id="comic"><img src="http://127.0.0.1:%d/img/%s.png"></div>'
                    % (self.server.server_port, n)).encode(); ct = 'text/html'
        self.send_response(200); self.send_header('Content-Type', ct)
        self.send_header('Content-Length', str(len(body))); self.end_headers()
        self.wfile.write(body)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); srv.daemon_threads = True
threading.Thread(target=srv.serve_forever, daemon=True).start()
"""
_LISTING = """LISTING = '''
import requests, os, bs4, threading, sys
BASE = sys.argv[1]
os.makedirs('xkcd', exist_ok=True)
def downloadXkcd(startComic, endComic):
    for urlNumber in range(startComic, endComic):
        res = requests.get(BASE + '/%s' % (urlNumber))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        comicElem = soup.select('#comic img')
        if comicElem == []:
            print('Could not find comic image.')
        else:
            comicUrl = comicElem[0].get('src')
            res = requests.get(comicUrl)
            res.raise_for_status()
            imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
downloadThreads = []
for i in range(0, 140, 10):
    start = i
    end = i + 9
    if start == 0:
        start = 1
    downloadThread = threading.Thread(target=downloadXkcd, args=(start, end))
    downloadThreads.append(downloadThread)
%s    downloadThread.start()
for downloadThread in downloadThreads:
    downloadThread.join()
print('Done.')
'''
"""
_RUN = r"""folder = tempfile.mkdtemp()
r = subprocess.run([sys.executable, '-c', LISTING, 'http://127.0.0.1:%d' % srv.server_port],
                   capture_output=True, text=True, cwd=folder)
pages = sorted(int(p.strip('/')) for p in hits if not p.startswith('/img/'))
saved = len(os.listdir(folder + '/xkcd')) if os.path.isdir(folder + '/xkcd') else 0
print('comic pages requested:', len(pages), '| files saved:', saved)
"""
_PNG = r"""import hashlib
def done(name, rows):
    def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d))
    raw = b''.join(b'\x00' + bytes(c for px in row for c in px) for row in rows)
    data = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', len(rows[0]), len(rows), 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))
    open(name, 'wb').write(data)
    k = os.environ.get('CH25_KEEP')
    if k: open(os.path.join(k, name), 'wb').write(data)
    print('saved %s: %d bytes, sha256 %s' % (name, len(data), hashlib.sha256(data).hexdigest()[:12]))
"""
# the printed listing has no line that starts a thread: the %s of the listing is empty ('' in front of the start line is replaced by a comment-free removal below)
PRINTED = _SRV + _LISTING.replace("%s    downloadThread.start()\n", "") + _RUN + (
    "print('return code:', r.returncode)\n"
    "print(r.stderr.strip().splitlines()[-1])\n")
FIXED = _SRV + _PNG + _LISTING.replace("%s    downloadThread.start()\n", "    downloadThread.start()\n") + _RUN + r"""miss = [n for n in range(1, 140) if n not in pages]
print('never requested:', len(miss), 'numbers, from', miss[0], 'to', miss[-1])
ink = {True: (47, 109, 98), False: (217, 122, 20)}
cell, rows = 22, []
for row in range(14):
    line = []
    for col in range(10):
        n = row * 10 + col
        c = (223, 214, 199) if n == 0 else ink[n in pages]
        line += [c] * (cell - 2) + [(250, 246, 239)] * 2
    rows += [line] * (cell - 2) + [[(250, 246, 239)] * len(line)] * 2
done('skipped.png', rows)
"""

LOST = r"""import threading, time
def trial(use_lock):
    box = [0]; lk = threading.Lock()
    def f():
        if use_lock: lk.acquire()
        v = box[0]; time.sleep(0.05); box[0] = v + 1
        if use_lock: lk.release()
    ts = [threading.Thread(target=f) for _ in range(2)]
    [t.start() for t in ts]; [t.join() for t in ts]
    return box[0]
print('two threads, no lock  :', [trial(False) for _ in range(3)])
print('two threads, with lock:', [trial(True) for _ in range(3)])
"""

LOCK = r"""import threading
box = [0]; lk = threading.Lock()
def f():
    for _ in range(100000):
        with lk: box[0] += 1
ts = [threading.Thread(target=f) for _ in range(4)]
[t.start() for t in ts]; [t.join() for t in ts]
print('4 threads x 100000 with a lock:', box[0])
try:
    with lk: raise ValueError
except ValueError: pass
print('locked after an error in the with block:', lk.locked())
rk = threading.RLock(); lk.acquire(); rk.acquire()
print('second acquire of a Lock, 0.2 s:', lk.acquire(timeout=0.2))
print('second acquire of an RLock     :', rk.acquire(timeout=0.2))
"""

DEAD = r"""import threading, time
a, b = threading.Lock(), threading.Lock()
def f(x, y):
    with x:
        time.sleep(0.1)
        with y: pass
t1 = threading.Thread(target=f, args=(a, b), daemon=True)
t2 = threading.Thread(target=f, args=(b, a), daemon=True)
t1.start(); t2.start(); t1.join(0.5); t2.join(0.5)
print('alive after 0.5 s:', t1.is_alive(), t2.is_alive())
ev, got = threading.Event(), []
def wait():
    ev.wait(); got.append('woke')
w = threading.Thread(target=wait)
w.start(); time.sleep(0.2)
print('before set():', got); ev.set(); w.join()
print('after set()  :', got)
"""

SEM = r"""import threading, time
def trial(limit):
    cur, top, lk = [0], [0], threading.Lock()
    sem = threading.BoundedSemaphore(limit)
    def f():
        with sem:
            with lk:
                cur[0] += 1; top[0] = max(top[0], cur[0])
            time.sleep(0.1)
            with lk: cur[0] -= 1
    ts = [threading.Thread(target=f) for _ in range(6)]
    [t.start() for t in ts]; [t.join() for t in ts]
    return top[0]
print('most threads inside, Semaphore(2):', trial(2))
print('most threads inside, Semaphore(6):', trial(6))
"""

QUEUE = r"""import threading, queue
q, got = queue.Queue(), []
def consumer():
    while (x := q.get()) is not None:
        got.append(x); q.task_done()
    q.task_done()
t = threading.Thread(target=consumer); t.start()
for i in range(5): q.put(i)
q.put(None); q.join(); t.join()
print('consumer received', got)
"""

POOL = r"""import os, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
def f(n):
    time.sleep(0.1 * (3 - n)); return n
with ThreadPoolExecutor(3) as ex:
    print('map          :', list(ex.map(f, [0, 1, 2])))
    fs = [ex.submit(f, n) for n in [0, 1, 2]]
    done = [fu.result() for fu in as_completed(fs)]
    print('as_completed :', done)
def name(i):
    time.sleep(0.05); return threading.current_thread().name
with ThreadPoolExecutor(2, thread_name_prefix='dl') as ex:
    print('worker names :', sorted(set(ex.map(name, range(4)))))
with ThreadPoolExecutor() as ex:
    n = ex._max_workers
    print('default max_workers on', os.cpu_count(), 'CPUs:', n)
"""

POOLERR = r"""import time, concurrent.futures as cf
def bad(): raise ValueError('boom')
with cf.ThreadPoolExecutor(1) as ex:
    fu = ex.submit(bad); time.sleep(0.1)
    print('exception():', repr(fu.exception()))
    try: fu.result()
    except ValueError as e: print('result() raises:', e)
    slow = ex.submit(time.sleep, 0.5)
    try: slow.result(timeout=0.1)
    except TimeoutError:
        print('timeout=0.1: TimeoutError | done:', slow.done())
ex = cf.ThreadPoolExecutor(1)
fs = [ex.submit(time.sleep, 0.2) for _ in range(5)]
time.sleep(0.05)
ex.shutdown(wait=True, cancel_futures=True)
gone = sum(f.cancelled() for f in fs)
print('cancelled', gone, 'of 5 | ran', 5 - gone)
"""

GIL = r"""import os, subprocess, sys, sysconfig
FT = os.environ.get('CH25_FT', 'FTPATH')
ask = ('import sys, sysconfig; print(sys._is_gil_enabled(), '
       'sysconfig.get_config_var("Py_GIL_DISABLED"))')
def run(exe, *flags, **env):
    e = dict(os.environ, **env)
    r = subprocess.run([exe, *flags, '-c', ask], text=True,
                       capture_output=True, env=e)
    return r.stdout.strip()
flag = sysconfig.get_config_var('Py_GIL_DISABLED')
std = (sys._is_gil_enabled(), flag)
print('GIL on?, Py_GIL_DISABLED')
print('standard build      :', *std)
print('free-threaded build :', run(FT))
print('  with PYTHON_GIL=1 :', run(FT, PYTHON_GIL='1'))
print('  with -X gil=1     :', run(FT, '-X', 'gil=1'))
""".replace('FTPATH', FTPATH)

PROC = r"""import multiprocessing as mp, threading, subprocess, sys, time
if __name__ == '__main__':
    d = {'n': 0}
    p = mp.Process(target=d.update, args=({'n': 99},))
    p.start(); p.join()
    print('a child process changed its copy :', d)
    t = threading.Thread(target=d.update, args=({'n': 99},))
    t.start(); t.join()
    print('a thread changed the same object :', d)
    print('default start method             :',
          mp.get_start_method())
    nap = 'import time; time.sleep(1)'
    t0 = time.time()
    k = subprocess.Popen([sys.executable, '-c', nap])
    back = time.time() - t0 < 0.5
    print('Popen came back at once          :', back)
    print('poll() while the child sleeps    :', k.poll())
    print('wait() returns the return code   :', k.wait())
"""

ASYNC = r"""import asyncio, threading, time
async def nap(): await asyncio.sleep(0.3)
async def block(): time.sleep(0.2)
def took(f, n):
    async def together():
        await asyncio.gather(*[f() for _ in range(n)])
    t0 = time.time(); asyncio.run(together())
    return time.time() - t0
print('10 awaits of 0.3 s, under 0.6 s:', took(nap, 10) < 0.6)
print('5 blocking 0.2 s calls, over 1 s  :', took(block, 5) >= 1.0)
def work():
    time.sleep(0.2); return threading.current_thread().name
async def bridge():
    return await asyncio.gather(*map(asyncio.to_thread, [work]*5))
t0 = time.time(); names = asyncio.run(bridge())
print('same 5 on threads, under 0.6 s :', time.time() - t0 < 0.6)
print('worker names start with', {n[:7] for n in names})
"""

PROGRAMS = {
    "startCut_v1_0_0.py": (START, (), True),
    "argsCut_v1_0_0.py": (ARGS, (), True),
    "lifeCut_v1_0_0.py": (LIFE, (), True),
    "joinCut_v1_0_0.py": (JOIN, (), True),
    "daemonCut_v1_0_0.py": (DAEMON, (), True),
    "printedCut_v1_0_0.py": (PRINTED, (), True),
    "fixedCut_v1_0_0.py": (FIXED, (), True),
    "lostCut_v1_0_0.py": (LOST, (), True),
    "lockCut_v1_0_0.py": (LOCK, (), True),
    "deadCut_v1_0_0.py": (DEAD, (), True),
    "semCut_v1_0_0.py": (SEM, (), True),
    "queueCut_v1_0_0.py": (QUEUE, (), True),
    "poolCut_v1_0_0.py": (POOL, (), True),
    "poolerrCut_v1_0_0.py": (POOLERR, (), True),
    "gilCut_v1_0_0.py": (GIL, (), True),
    "procCut_v1_0_0.py": (PROC, (), True),
    "asyncCut_v1_0_0.py": (ASYNC, (), True),
}
KIND = {n: ("standin" if n in ("printedCut_v1_0_0.py", "fixedCut_v1_0_0.py") else "plain") for n in PROGRAMS}
STANDKEY = {n: ("127.0.0.1", "xkcd.com is never contacted") for n in PROGRAMS if KIND[n] == "standin"}
# the pictures a slide shows that a program saved: file name -> the program that makes it (the four photographs of the stories are not here: see images/photos_v1_0_0.json)
IMAGES = {"skipped.png": "fixedCut_v1_0_0.py"}
EQUIV = {}
SUBSET = {}

# ---- charts and tables (re-computed by the deck check) -----------------------------------------------------------------
_REC = "import json, os\nR = json.load(open(os.path.join(HERE, '..', 'ch25-page', 'timing_record_v1_0_0.json')))['runs']\nBUILDS = [('3.14.6', 'standard 3.14.6'), ('3.14.6t', 'free-threaded 3.14.6'), ('3.13.14', '3.13.14'), ('3.12.13', '3.12.13'), ('3.11.15', '3.11.15')]\n"
CHARTS = {
    "cpuRatio": {
        "setup": _REC + "ROWS = [(lab, round(R['cpu_' + k]['result']['threads_4'] / R['cpu_' + k]['result']['serial_4_tasks'], 2)) for k, lab in BUILDS]\n",
        "expr": "ROWS"},
    "waitingRecord": {
        "setup": _REC + "r = R['io_3.14.6']['result']\nROWS = [('one after another', r['serial_8_sleeps']), ('8 threads', r['threads']), ('a pool', r['pool']), ('asyncio', r['asyncio'])]\n",
        "expr": "ROWS"},
}

_PROBE = r'''
import json, sys, sysconfig, threading, concurrent.futures as cf, multiprocessing as mp
def f(): pass
r = {'Python': sys.version.split()[0]}
r['GIL on'] = str(sys._is_gil_enabled()) if hasattr(sys, '_is_gil_enabled') else 'no such call'
r['Py_GIL_DISABLED'] = str(sysconfig.get_config_var('Py_GIL_DISABLED'))
r['thread name'] = threading.Thread(target=f).name
with cf.ThreadPoolExecutor(2) as ex: r['pool map'] = str(list(ex.map(abs, [-1, -2])))
r['InterpreterPool'] = str(hasattr(cf, 'InterpreterPoolExecutor'))
r['start method'] = mp.get_start_method()
print(json.dumps(r))
'''
U = "/root/.local/share/uv/python/"
INTERPS = [("3.11.15", U + "cpython-3.11-linux-x86_64-gnu/bin/python3.11"), ("3.12.13", U + "cpython-3.12-linux-x86_64-gnu/bin/python3.12"),
           ("3.13.14", U + "cpython-3.13-linux-x86_64-gnu/bin/python3.13"), ("3.14.6", "/home/claude/venv314_ch25_latest/bin/python"),
           ("3.14.6 free-threaded", FTPATH)]
_ROWS = ["Python", "GIL on", "Py_GIL_DISABLED", "thread name", "pool map", "InterpreterPool", "start method"]

TABLES = {
    "environments": {
        "setup": "import json, subprocess\nPROBE = %r\nINTERPS = %r\nres = []\nfor v, p in INTERPS:\n"
                 "    r = subprocess.run([p, '-W', 'ignore', '-c', PROBE], capture_output=True, text=True, stdin=subprocess.DEVNULL)\n"
                 "    assert r.returncode == 0, (v, r.stderr[-300:])\n    res.append(json.loads(r.stdout.strip().splitlines()[-1]))\n"
                 "ROWS = %r\n" % (_PROBE, INTERPS, _ROWS),
        "expr": "[['check'] + [v for v, p in INTERPS]] + [[k] + [x[k] for x in res] for k in ROWS]"},
    "raceRecord": {
        "setup": _REC + "def lost(k, i): return format(R['race_%s_run%d' % (k, i)]['result']['lost'], ',')\n",
        "expr": "[['build', 'run 1', 'run 2', 'run 3']] + [[lab] + [lost(k, i) for i in (1, 2, 3)] for k, lab in BUILDS]"},
    "cpuRecord": {
        "setup": _REC + "def s(k, n): return '%.3f' % R['cpu_' + k]['result'][n]\n",
        "expr": "[['build', 'serial', '2 threads', '4 threads']] + [[lab, s(k, 'serial_4_tasks'), s(k, 'threads_2'), s(k, 'threads_4')] for k, lab in BUILDS]"},
    "processRecord": {
        "setup": _REC + "m = R['multiprocessing_3.14.6']['result']; a = R['start_3.14.6']['result']; b = R['start_3.14.6t']['result']\n",
        "expr": "[['recorded run', 'standard 3.14.6', 'free-threaded 3.14.6'], "
                "['4 CPU tasks, serial', '%.3f s' % m['serial_4_tasks'], '-'], "
                "['4 CPU tasks, pool of 2 processes', '%.3f s' % m['pool_2_processes'], '-'], "
                "['one thread started', '%d us' % a['per_thread_us'], '%d us' % b['per_thread_us']], "
                "['one process started', '%.1f ms' % a['per_process_ms'], '%.1f ms' % b['per_process_ms']]]"},
}
