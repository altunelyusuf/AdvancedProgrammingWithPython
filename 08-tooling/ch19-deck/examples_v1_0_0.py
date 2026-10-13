"""Chapter 19 deck examples: every console session, whole program (or excerpt), chart and table the lecture deck shows. Nothing here
carries a result; examples_run_v1_0_0.py runs it all under the interpreter given (the uv Python 3.14.6 of the chapter 19 research
environment /home/claude/venv314_ch19_latest, with schedule 1.2.2, tzdata 2026.5, pyperclip 1.11.0 and playsound3 3.3.2 installed; time,
datetime, zoneinfo, subprocess, signal, threading, sched, asyncio, calendar, shlex and plistlib are the standard library) and records the
results. A console group is one session: its rows run in order in one namespace (the deck check re-runs them per slide, one namespace per
slide).

NOTHING HERE DEPENDS ON THE CLOCK. A console row never reads the current time: every moment is built from numbers (datetime(2026, 10, 21,
16, 29), a timestamp of 1773813875.35), every zone is named (ZoneInfo('America/New_York')), and the only clock a program reads is a monotonic
one whose result is compared with a bound (the sleep lasted at least what was asked) or a fake one that the program advances (the stopwatch
and the countdown). Each child program is Python itself or `sleep`. So the deck check can run every row and every program again on any day, in
any zone of the machine, and compare the text. The tzdata in use is the one of the machine (system tz database 2026c, tzdata package 2026.5).
What the research recorded on a day (the cron runs, the public pages) is not re-run: it appears on a slide as 'recorded on 13 October 2026'.

Programs come from sen0414_ch19_corpus_base_v1_0_0.py, all twelve, run and recorded under their own names. A corpus line is often wider than a
slide can show without wrapping, so the slides show deck-written copies (the corpus program cut into pieces that fit a slide, with comments);
the first four lines of every program are the corpus HEAD (imports and a temporary folder) and are not shown, nor is the comment line.
KIND says what a program's output depends on, so that honesty_check can require the matching words on the slide that shows it. No program of
this chapter is 'live' (none reads the network); the programs in which a Python object stands in for a machine, a clock or a person are
'emulated' and the slide that shows one must say EMULATED."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base19", os.path.join(HERE, "..", "sen0414_ch19_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)
_HEAD = B.HEAD

CONSOLES = {
    "title": ["import platform, importlib.metadata as m", "platform.python_version()", "m.version('tzdata')", "m.version('schedule')"],
    "epoch": ["import time, calendar", "time.gmtime(0)[:6]", "calendar.timegm((1970, 1, 1, 0, 0, 0))",
              "calendar.timegm((2038, 1, 19, 3, 14, 7)) == 2**31 - 1", "round(2**32 / 60 / (86400 * 365.25), 2)"],
    "repairs": ["compile('d = 5 \u2013 3', 'listing', 'eval')", "eval(compile('5 - 3', 'listing', 'eval'))",
                "import math, sys", "sys.get_int_max_str_digits()", "len(str(math.factorial(1000)))",
                "str(math.factorial(100000))[:5]", "int(math.lgamma(100001) / math.log(10)) + 1"],
    "dtbasics": ["import datetime", "halloween = datetime.datetime(2026, 10, 31)", "later = datetime.datetime(2027, 1, 1)",
                 "halloween < later", "later - halloween", "halloween.weekday()", "datetime.datetime(2026, 10, 21, 16, 29).isoformat()",
                 "datetime.datetime(2026, 2, 30)", "datetime.date(2019, 1, 7).weekday()"],
}

# ---- programs written for the deck ---------------------------------------------------------------------------------------------
EPOCH = _HEAD + r'''# The epoch timestamp: a count of seconds, and what it cannot hold.
t = calendar.timegm((2026, 3, 18, 6, 4, 35))
print('2026-03-18 06:04:35 UTC is', t)
print('timestamp 0 is', DT.fromtimestamp(0, UTC).isoformat())
a = calendar.timegm((2016, 12, 31, 23, 59, 59))
b = calendar.timegm((2017, 1, 1, 0, 0, 0))
print('across the 2016 leap second, seconds apart:', b - a)
try: DT(2016, 12, 31, 23, 59, 60)
except ValueError as e: print('datetime refuses:', e)
print('float spacing near the timestamp:', math.ulp(t + 0.35))
print('2**31 - 1 ->', DT.fromtimestamp(2**31 - 1, UTC).isoformat())
print('wrapped:', DT.fromtimestamp(-2**31, UTC).isoformat())
'''

CLOCKS = _HEAD + r'''# Which clock answers which question. EMULATED: two numbers stand in for a clock that is set back.
for n in ('time', 'monotonic', 'perf_counter', 'process_time'):
    i = time.get_clock_info(n)
    print(n.ljust(13), i.monotonic, i.adjustable, i.implementation)
wall, mono = iter([1000.0, 990.0]), iter([50.0, 60.0])
w0, m0, w1, m1 = next(wall), next(mono), next(wall), next(mono)
print('set back by 10 sec: wall', w1 - w0, '| monotonic', m1 - m0)
t = time.monotonic(); time.sleep(0.2)
print('sleep(0.2) lasted at least 0.2:', time.monotonic() - t >= 0.2)
'''

SLEEP = _HEAD + r'''# sleep returns None; a handler that returns does not cut it short; a loop that sleeps after its work drifts.
t = time.monotonic(); r = time.sleep(0.2)
ok = time.monotonic() - t >= 0.2
print('sleep returns', r, '| lasted at least 0.2:', ok)
hits = []
signal.signal(signal.SIGALRM, lambda s, f: hits.append('ran'))
signal.setitimer(signal.ITIMER_REAL, 0.05)
t = time.monotonic(); time.sleep(0.3)
ok = time.monotonic() - t >= 0.3
print('handler', hits, '| not cut short:', ok)
def start_of_round(n, work, fixed):
    t = 0.0
    for _ in range(n - 1):
        t += work + 1.0 if fixed else max(work, 1.0)
    return round(t, 2)
print('sleeping after work:', start_of_round(3600, 0.02, True))
print('anchored to the tick:', start_of_round(3600, 0.02, False))
'''

STOPWATCH = _HEAD + r'''# Project 14 on a clock the program moves. EMULATED: the user's key presses are numbers added to a fake clock.
now = [1000.0]
clock = lambda: now[0]
start_time = last_time = clock()
lap_number = 1
for gap in (3.56, 5.07, 9.05, 1.43):
    now[0] += gap                  # the user presses ENTER
    lap_time = round(clock() - last_time, 2)
    total_time = round(clock() - start_time, 2)
    print(f'Lap #{lap_number}: {total_time}({lap_time})')
    lap_number += 1
    last_time = clock()
print('as shipped:', 'Lap #{lap_number}: {total_time}({lap_time})')
'''

DURATIONS = _HEAD + r'''# timedelta has days, seconds and microseconds; no months; thirty years of 365 days are 7 days short.
d = TD(days=11, hours=10, minutes=9, seconds=8)
print(d.days, d.seconds, d.total_seconds(), '|', d)
try: TD(months=1)
except TypeError as e: print('TypeError:', e)
print('31 Jan + 30 days:', (DT(2026, 1, 31) + TD(days=30)).date())
o = DT(2026, 10, 21, 16, 29)
thirty = TD(days=365 * 30)
real = o.replace(year=1996)
print('book: 30 years back =', (o - thirty).date(), '| real:', real.date())
print('days off:', (o - thirty - real).days, '| leap days:', (o - real).days - 365 * 30)
print('book: 60 years back =', (o - 2 * thirty).date(), '| real: 1966-10-21')
try: datetime.delta(days=1)
except AttributeError as e: print('AttributeError:', e)
'''

STRFTIME = _HEAD + r'''# strftime turns a moment into text; isoformat and fromisoformat are the standard way to store one.
dt = DT(2026, 11, 3, 16, 29, 7)
print(dt.strftime('%Y/%m/%d %H:%M:%S'))
print(dt.strftime('%I:%M %p'), '|', dt.strftime('%A, %B %d'))
print(dt.strftime('%j %w'), '| percent:', dt.strftime('%d%%'))
print(dt.isoformat(), '|', dt.isoformat(timespec='minutes'))
x = DT(2026, 10, 21, 16, 29, 7, 123456, tzinfo=UTC)
print(x.isoformat())
print(DT.fromisoformat('2026-10-21T16:29:07Z'))
print(D.fromisoformat('2026-W43-3'))
'''

STRPTIME = _HEAD + r'''# strptime turns text into a moment; the format must match the text exactly.
print(DT.strptime('October 21, 2026', '%B %d, %Y'))
print(DT.strptime("November of '63", "%B of '%y").date())
print(DT.strptime("November of '73", "%B of '%y").date())
for s, f in (('2026-10-21', '%Y/%m/%d'), ('Oct 21, 2026', '%B %d, %Y')):
    try: DT.strptime(s, f)
    except ValueError as e: print('ValueError:', e)
print(DT.strptime('10/21', '%m/%d').date(), '<- a date with no year')
print(D.strptime('2026-10-21', '%Y-%m-%d'), '<- new in Python 3.14')
'''

ZONES = _HEAD + r'''# Naive and aware values, and the zone of the chapter's example.
n = DT(2026, 10, 21, 16, 29)
a = DT(2026, 10, 21, 16, 29, tzinfo=UTC)
print('naive == aware:', n == a)
try: n - a
except TypeError as e: print('TypeError:', e)
ist = ZoneInfo('Europe/Istanbul')
print('16:29 UTC == 19:29 Istanbul:', a == DT(2026, 10, 21, 19, 29, tzinfo=ist))
d = DT.fromtimestamp(1773813875.3518236, ZoneInfo('America/Los_Angeles'))
print('the chapter:', d.isoformat(timespec='seconds'), d.tzname())
for z in ('America/Los_Angeles', 'UTC', 'Europe/Istanbul'):
    print(z.ljust(20), DT.fromtimestamp(1000000, ZoneInfo(z)).isoformat())
print('Istanbul:', ist.utcoffset(DT(1970, 1, 1)), ist.utcoffset(DT(2026, 7, 1)))
'''

DST = _HEAD + r'''# A day added across the change, an hour that does not exist, an hour that happens twice, and utcnow.
import warnings
ny = ZoneInfo('America/New_York')
x = DT(2026, 3, 7, 12, tzinfo=ny)
y = x + TD(days=1)
print(x.isoformat(' ', 'minutes'), '->', y.isoformat(' ', 'minutes'))
print('UTC difference:', y.astimezone(UTC) - x.astimezone(UTC))
print('wall difference:', y - x)
g = DT(2026, 3, 8, 2, 30, tzinfo=ny)
print('02:30 in the gap ->', g.astimezone(UTC).astimezone(ny).isoformat())
f0 = DT(2026, 11, 1, 1, 30, tzinfo=ny)
f1 = f0.replace(fold=1)
utc = lambda v: v.astimezone(UTC).isoformat()[11:16]
print('01:30 twice, in UTC:', utc(f0), utc(f1), '| equal:', f0 == f1)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); u = DT.utcnow()
print('naive:', u.tzinfo is None, [x.category.__name__ for x in w])
print('now(UTC) is aware:', DT.now(UTC).tzinfo)
'''

RUN = _HEAD + r'''# run() waits and returns a CompletedProcess; Popen returns at once; text=True gives str.
r = subprocess.run(['sleep', '0.3'])
print(r)
c = 'import sys; print("out"); print("err", file=sys.stderr)'
cmd = [sys.executable, '-c', c]
r = subprocess.run(cmd, capture_output=True)
print(r.returncode, r.stdout, r.stderr)
r = subprocess.run(cmd, capture_output=True, text=True)
print(type(r.stdout).__name__, repr(r.stdout))
p = subprocess.Popen(['sleep', '0.4'])
print('Popen returned; poll() ->', p.poll())
print('wait() ->', p.wait(), '| poll() ->', p.poll())
'''

POPEN = _HEAD + r'''# check=True, a timeout, a missing program, and arguments that pass through no shell.
for call in (lambda: subprocess.run(['nosuch']),
             lambda: subprocess.run(['false'], check=True),
             lambda: subprocess.run(['sleep', '5'], timeout=0.2)):
    try: call()
    except Exception as e: print(type(e).__name__, e)
c = 'import sys; print(sys.argv[1:])'
a = ['my file.txt', 'a b', '*.txt']
cmd = [sys.executable, '-c', c, *a]
print(subprocess.run(cmd, capture_output=True, text=True).stdout.strip())
'''

EXITS = _HEAD + r'''# Exit codes, and a negative code for a signal.
run = lambda s: subprocess.run([sys.executable, '-c', s], stderr=subprocess.DEVNULL).returncode
K = 'import os, signal; os.kill(os.getpid(), signal.SIG%s)'
codes = [run('pass'), run('import sys; sys.exit(3)'), run('raise ValueError')]
print(*codes, run(K % 'KILL'), run(K % 'TERM'))
'''

SHELL = _HEAD + r'''# shell=True with a list, a command built from a file name, and shlex.quote. start is a Windows command.
import shutil, webbrowser
sh = lambda a, **k: subprocess.run(a, capture_output=True, text=True, **k)
print('list + shell=True:', repr(sh(['echo', 'hi', 'there'], shell=True).stdout))
print('string + shell=True:', repr(sh('echo hi there', shell=True).stdout))
r = sh(['start', 'hello.txt'], shell=True)
print('start hello.txt:', r.returncode, '|', r.stderr.strip())
name = 'x; echo INJECTED'
print(repr(sh(f'echo opening {name}', shell=True).stdout))
print(repr(sh(f'echo opening {shlex.quote(name)}', shell=True).stdout))
print(repr(sh(['echo', 'opening', name]).stdout))
print('open:', shutil.which('open'), '| xdg-open:', shutil.which('xdg-open'))
print('webbrowser.open with no browser:', webbrowser.open('file:///nonexistent'))
'''

SCHED = _HEAD + r'''# Schedulers inside a process. EMULATED: sched runs on a clock the program moves. Then Timer and call_later.
import asyncio
now, log = [0.0], []
def advance(d): now[0] += d
s = sched.scheduler(lambda: now[0], advance)
jobs = [(5, 1, 'five'), (2, 1, 'two'), (5, 0, 'five-0'), (0, 9, 'now')]
for d, p, w in jobs: s.enter(d, p, log.append, (w,))
s.run(); print(log, now[0])
hits = []
t = threading.Timer(0.1, hits.append, args=('fired',))
t.start(); print('after start():', hits)
t.join(); print('after join():', hits)
async def main():
    loop = asyncio.get_running_loop(); out = []
    for d in (0.2, 0.1, 0): loop.call_later(d, out.append, d)
    await asyncio.sleep(0.3); return out
print('call_later order:', asyncio.run(main()))
'''

CRON = _HEAD + r'''# A crontab line has five time fields; with both day fields restricted a day matches if EITHER does.
def field(f, lo, hi):
    ok = set()
    for p in f.split(','):
        r, _, st = p.partition('/')
        a, b = (lo, hi) if r == '*' else (r.split('-') * 2)[:2]
        ok |= set(range(int(a), int(b) + 1, int(st or 1)))
    return ok
def nxt(expr, t):
    m, h, dom, mon, dow = expr.split()
    M, H, MON = field(m, 0, 59), field(h, 0, 23), field(mon, 1, 12)
    DOM, DOW = field(dom, 1, 31), field(dow.replace('7', '0'), 0, 6)
    t = t.replace(second=0) + TD(minutes=1)
    while True:
        cd = (t.weekday() + 1) % 7
        if dow == '*': day = t.day in DOM
        elif dom == '*': day = cd in DOW
        else: day = t.day in DOM or cd in DOW
        if t.minute in M and t.hour in H and t.month in MON and day:
            return t
        t += TD(minutes=1)
s = DT(2026, 10, 13, 9, 30)
for e in ('30 9 * * 1-5', '*/15 * * * *', '0 0 13 * 5', '0 0 29 2 *'):
    print(e.ljust(13), nxt(e, s).strftime('%Y-%m-%d %H:%M %a'))
'''

COUNTDOWN = _HEAD + r'''# Project 15 without the wait. EMULATED: a number stands in for the clock that time.sleep(1) would move.
now = [0.0]
time_left = 5
while time_left > 0:
    print(time_left, end=' ')
    now[0] += 1                      # the program would call time.sleep(1)
    time_left = time_left - 1
print('\ncounted', now[0], 'seconds; the alarm needs a sound card')
'''

PRETTY = _HEAD + r'''# Practice program: the stopwatch laps in columns with rjust().
rows = [(1, 3.56, 3.56), (2, 8.63, 5.07), (3, 17.68, 9.05), (4, 19.11, 1.43)]
r = lambda v, k: str(v).rjust(k)
for n, total, lap in rows:
    print('Lap #' + r(n, 2) + ': ' + r(total, 6) + ' (' + r(lap, 6) + ')')
'''

FRIDAY = _HEAD + r'''# Practice program: the next ten Friday the 13ths from a fixed day, then backward to the edge of the date range.
import collections
d = D(2026, 10, 13)
found = []
while len(found) < 10:
    if d.day == 13 and d.weekday() == 4: found.append(d.isoformat())
    d += TD(days=1)
print(found[0], '...', found[-1])
d, n, last = D(2026, 10, 13), 0, None
try:
    while True:
        if d.day == 13 and d.weekday() == 4: n, last = n + 1, d
        d -= TD(days=1)
except OverflowError as e:
    print('backward:', n, 'dates, earliest', last)
    print('stopped at', d, '-', e)
days = (D(y, m, 13) for y in range(2000, 2400) for m in range(1, 13))
by = collections.Counter(x.weekday() for x in days)
print('Mon..Sun in 400 years:', [by[i] for i in range(7)])
'''

PROGRAMS = dict(B.PROGRAMS)
for _n, _c in (("epochCut", EPOCH), ("clocksCut", CLOCKS), ("sleepCut", SLEEP), ("stopwatchCut", STOPWATCH), ("durationsCut", DURATIONS),
               ("strftimeCut", STRFTIME), ("strptimeCut", STRPTIME), ("zonesCut", ZONES), ("dstCut", DST), ("runCut", RUN),
               ("popenCut", POPEN), ("exitsCut", EXITS), ("shellCut", SHELL), ("schedCut", SCHED), ("cronCut", CRON),
               ("countdownCut", COUNTDOWN), ("prettyCut", PRETTY), ("fridayCut", FRIDAY)):
    PROGRAMS[_n + "_v1_0_0.py"] = (_c, (), False)

SUBSET = {}
EQUIV = {}
KIND = {n: "none" for n in PROGRAMS}
for _n in ("clocksCut", "stopwatchCut", "countdownCut", "schedCut"):
    KIND[_n + "_v1_0_0.py"] = "emulated"
KIND["stopwatchAndCountdown_v1_0_0.py"] = "emulated"
KIND["inProcessSchedulers_v1_0_0.py"] = "emulated"
LIVEKEY = {}
EMUKEY = {n: ("EMULATED",) for n, k in KIND.items() if k == "emulated"}

# ---- charts and tables: each a setup and one expression --------------------------------------------------------------------------
_THIRTEENTHS = ("import datetime as dt, collections\n"
                "def counts():\n"
                "    by = collections.Counter(dt.date(y, m, 13).weekday() for y in range(2000, 2400) for m in range(1, 13))\n"
                "    return [[n, by[i]] for i, n in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])]\n")
CHARTS = {"thirteenths": {"setup": _THIRTEENTHS, "expr": "counts()"}}
_DIR = ("import datetime as dt\n"
        "M = dt.datetime(2026, 11, 3, 16, 29, 7)\n")
_YY = ("import datetime as dt\n"
       "def yy(s):\n"
       "    return dt.datetime.strptime(s, '%y').year\n")
TABLES = {
    "directives": {"setup": _DIR,
                   "expr": "[['directive', 'meaning', '3 Nov 2026 16:29:07']] + [[d, m, M.strftime(d)] for d, m in (('%Y', 'year, four digits'), ('%y', 'year, two digits'), ('%m', 'month number'), ('%B', 'month name'), ('%d', 'day of the month'), ('%j', 'day of the year'), ('%w', 'weekday, Sunday is 0'), ('%A', 'weekday name'), ('%H', 'hour, 24-hour clock'), ('%I', 'hour, 12-hour clock'), ('%p', 'AM or PM'))]"},
    "twoDigitYear": {"setup": _YY,
                     "expr": "[['text', '%y gives']] + [[repr(s), str(yy(s))] for s in ('00', '26', '68', '69', '99')]"}}

# ---- runs under other environments of the research (recorded, then used in a card) ---------------------------------------------------
BARE_CODE = ("for name in ('schedule', 'tzdata', 'zoneinfo'):\n"
             "    try:\n"
             "        __import__(name); print(name, 'imported')\n"
             "    except ImportError as e:\n"
             "        print(type(e).__name__, '-', e)\n"
             "import zoneinfo, datetime\n"
             "print(datetime.datetime(2026, 3, 8, 12, tzinfo=zoneinfo.ZoneInfo('America/New_York')).isoformat())\n")
PINS_CODE = ("import importlib.metadata as m\n"
             "print('playsound3', m.version('playsound3'), '| pyperclip', m.version('pyperclip'))\n"
             "try:\n"
             "    import schedule\n"
             "except ImportError as e:\n"
             "    print(type(e).__name__, '-', e)\n")
