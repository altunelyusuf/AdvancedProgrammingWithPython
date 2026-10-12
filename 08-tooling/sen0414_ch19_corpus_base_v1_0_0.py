#!/usr/bin/env python3
"""SEN0414 chapter 19 (Keeping Time, Scheduling Tasks, and Launching Programs, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, in the shape of
sen0414_ch18_corpus_base_v1_0_0.py. Each program is a complete script that exits 0 and prints what it printed on 2026-10-13 under
Python 3.14.6 (uv) with schedule 1.2.2 (the environment /home/claude/venv314_ch19_latest; the rest is the standard library). The programs
that would otherwise depend on the clock, the zone or the machine fix them: moments are made from numbers, zones are named, the clock of
the stopwatch and the countdown is a fake that the program advances, and child programs are Python itself, so all twelve give the same text
on every run and need no network, so none is marked LIVE (the record that reads the book's page and the files it ships, and runs the chapter's
statements, is sen0414_ch19_thirdparty_v1_0_0.py). Nothing here starts a Windows or macOS program; where the chapter does, the program uses a
command that exists on Linux and says so in a comment.

Programs: EPOCHTIME, CLOCKS, DTARITH, FORMATS, ZONES, SUBPROC, SHELLSAFE, EXITSIG, SCHEDULERS, CRONNEXT, STOPWATCH (Project 14 and Project 15 on a
fake clock) and FRIDAY13 (the practice program, forward and backward from a fixed day).
"""
HEAD = r'''import io, os, re, sys, time, datetime, subprocess, tempfile, calendar, signal, threading, shlex, sched, math
from datetime import datetime as DT, timedelta as TD, date as D, UTC
from zoneinfo import ZoneInfo
os.chdir(tempfile.mkdtemp())
'''
EPOCHTIME = HEAD + r'''# The epoch timestamp: the zero point, the POSIX expression, leap seconds that have no number, the float, and the wrap of 32 bits.
import struct
print('epoch:', time.gmtime(0)[:6], calendar.timegm((1970, 1, 1, 0, 0, 0)), DT(1970, 1, 1, tzinfo=UTC).timestamp())
t = calendar.timegm((2026, 3, 18, 6, 4, 35))
print('timegm of 2026-03-18 06:04:35 UTC:', t, '| from the float of the chapter:', DT.fromtimestamp(1773813875.3518236, UTC).isoformat())
print('one second across the leap second of 2016:', calendar.timegm((2017, 1, 1, 0, 0, 0)) - calendar.timegm((2016, 12, 31, 23, 59, 59)))
try: DT(2016, 12, 31, 23, 59, 60)
except ValueError as e: print('datetime refuses a 60th second:', e)
print('spacing of floats near the timestamp:', math.ulp(1773813875.35), '| time_ns is an int:', type(time.time_ns()).__name__)
wrapped = struct.unpack('<i', struct.pack('<I', 2**31))[0]
print('2**31 - 1 ->', DT.fromtimestamp(2**31 - 1, UTC).isoformat(), '| 2**31 in 32 bits ->', wrapped, DT.fromtimestamp(wrapped, UTC).isoformat())
for z in ('America/Los_Angeles', 'UTC', 'Europe/Istanbul'):
    print('fromtimestamp(1000000) in', z, DT.fromtimestamp(1000000, ZoneInfo(z)).isoformat())
'''
CLOCKS = HEAD + r'''# Which clock answers which question: get_clock_info, a wall clock that is set back, sleep timed on a monotonic clock, and drift.
for n in ('time', 'monotonic', 'perf_counter', 'process_time'):
    i = time.get_clock_info(n); print(n, 'monotonic', i.monotonic, 'adjustable', i.adjustable, i.implementation)
wall = iter([1000.0, 990.0]); mono = iter([50.0, 60.0])
w0, m0, w1, m1 = next(wall), next(mono), next(wall), next(mono)
print('a wall clock set back by 10 s: difference', w1 - w0, '| monotonic difference', m1 - m0)
t = time.monotonic(); r = time.sleep(0.2); e = time.monotonic() - t
print('sleep(0.2) returned', r, 'and lasted at least 0.2 s:', e >= 0.2)
for call in (lambda: time.sleep(-1), lambda: time.sleep('1')):
    try: call()
    except Exception as ex: print(type(ex).__name__, ex)
hits = []
signal.signal(signal.SIGALRM, lambda s, f: hits.append('handler ran')); signal.setitimer(signal.ITIMER_REAL, 0.05)
t = time.monotonic(); time.sleep(0.3); print('a handler that returns does not cut the sleep short:', hits, time.monotonic() - t >= 0.3)
def drifting(n, work):
    t = 0.0
    for _ in range(n - 1): t += work + 1.0
    return t
def anchored(n, work):
    t = 0.0
    for i in range(n - 1): t += max(work, 1.0)
    return t
print('start of round 3600 with 0.02 s of work, fixed sleep:', round(drifting(3600, 0.02), 2), '| anchored to the tick:', round(anchored(3600, 0.02), 2))
print('round:', round(2.4), round(2.5), round(3.5), round(2.675, 2), type(round(2.5)).__name__, type(round(2.5, 2)).__name__)
'''
DTARITH = HEAD + r'''# Durations and the chapter's examples: timedelta fields, no months, 1000 days, and the thirty years that are 7 days off.
d = TD(days=11, hours=10, minutes=9, seconds=8)
print(d.days, d.seconds, d.microseconds, d.total_seconds(), '|', d, '|', repr(TD(seconds=-1)))
for kw in ({'months': 1}, {'years': 1}):
    try: TD(**kw)
    except TypeError as e: print('TypeError:', e)
print('31 Jan + 30 days:', (DT(2026, 1, 31) + TD(days=30)).date(), '| + 31 days:', (DT(2026, 1, 31) + TD(days=31)).date())
now = DT(2026, 12, 2, 18, 38, 50, 636181)
print('now + 1000 days:', now + TD(days=1000), (now + TD(days=1000)).strftime('%A'))
o = DT(2026, 10, 21, 16, 29); thirty = TD(days=365 * 30)
print('minus about thirty years:', o - thirty, '| the real date:', o.replace(year=1996), '| days off:', (o - thirty - o.replace(year=1996)).days)
print('minus sixty years:', o - 2 * thirty, '| days off from 1966-10-21:', (o.replace(year=1966) - (o - 2 * thirty)).days)
print('leap days in the thirty years:', (o - DT(1996, 10, 21, 16, 29)).days - 365 * 30)
try: datetime.delta(days=1)
except AttributeError as e: print('AttributeError:', e)
print(D(2019, 1, 7).strftime('%A'), D(2019, 1, 7).weekday(), D(2019, 1, 7).isoweekday())
h, n = DT(2026, 10, 31), DT(2027, 1, 1)
print(h == DT(2026, 10, 31), h > n, n > h, n - h)
'''
FORMATS = HEAD + r'''# Table 19-1 on a fixed moment, strftime, strptime, the %y rule, the year-less date and ISO 8601.
import warnings
dt = DT(2026, 11, 3, 16, 29, 7)
print({d: dt.strftime(d) for d in '%Y %y %m %B %b %d %j %w %A %a %H %I %M %S %p %%'.split()})
print(DT(2026, 10, 21, 16, 29).strftime('%Y/%m/%d %H:%M:%S'), '|', DT(2026, 10, 21, 16, 29).strftime('%I:%M %p'))
print(DT.strptime('October 21, 2026', '%B %d, %Y'), DT.strptime("November of '63", "%B of '%y"), DT.strptime("November of '73", "%B of '%y"))
for s, f in (('2026-10-21', '%Y/%m/%d'), ('Oct 21, 2026', '%B %d, %Y')):
    try: DT.strptime(s, f)
    except ValueError as e: print('ValueError:', e)
print('%y:', [(s, DT.strptime(s, '%y').year) for s in ('00', '26', '68', '69', '99')])
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    try: DT.strptime('02/29', '%m/%d')
    except ValueError as e: print('year-less 29 February:', e, [x.category.__name__ for x in w])
    print('year-less 21 October:', DT.strptime('10/21', '%m/%d'), '| with a year:', DT.strptime('02/29;1984', '%m/%d;%Y').date())
print('3.14 methods:', D.strptime('2026-10-21', '%Y-%m-%d'), datetime.time.strptime('16:29', '%H:%M'))
x = DT(2026, 10, 21, 16, 29, 7, 123456, tzinfo=UTC)
print(x.isoformat(), x.isoformat(timespec='seconds'), DT.fromisoformat('2026-10-21T16:29:07Z'), D.fromisoformat('2026-W43-3'))
'''
ZONES = HEAD + r'''# Naive and aware values, zones, the day of 23 hours, the hour that does not exist and the hour that happens twice.
import importlib.metadata as md
n, a = DT(2026, 10, 21, 16, 29), DT(2026, 10, 21, 16, 29, tzinfo=UTC)
print('naive == aware:', n == a)
for call in (lambda: n < a, lambda: n - a):
    try: call()
    except TypeError as e: print('TypeError:', e)
print('16:29 UTC == 19:29 Istanbul:', a == DT(2026, 10, 21, 19, 29, tzinfo=ZoneInfo('Europe/Istanbul')))
la = ZoneInfo('America/Los_Angeles'); d = DT.fromtimestamp(1773813875.3518236, la)
print('the chapter\'s moment in Los Angeles:', d.isoformat(timespec='seconds'), d.tzname(), '(not Pacific Standard Time)')
print('Istanbul offsets 1970 / 2015 / 2026:', ZoneInfo('Europe/Istanbul').utcoffset(DT(1970, 1, 12)), ZoneInfo('Europe/Istanbul').utcoffset(DT(2015, 7, 1)), ZoneInfo('Europe/Istanbul').utcoffset(DT(2026, 7, 1)), '| tzdata', md.version('tzdata'))
ny = ZoneInfo('America/New_York'); x = DT(2026, 3, 7, 12, tzinfo=ny); y = x + TD(days=1)
print('a day added across 8 March 2026:', x.isoformat(), '->', y.isoformat(), '| UTC difference', y.astimezone(UTC) - x.astimezone(UTC), '| wall difference', y - x)
g = DT(2026, 3, 8, 2, 30, tzinfo=ny); print('02:30 in the gap:', g.astimezone(UTC).astimezone(ny).isoformat())
f0 = DT(2026, 11, 1, 1, 30, tzinfo=ny); f1 = f0.replace(fold=1)
print('01:30 twice:', f0.astimezone(UTC).isoformat(), f1.astimezone(UTC).isoformat(), 'equal:', f0 == f1)
print('range:', D.min, D.max, '| 5 October 1582 is a', D(1582, 10, 5).strftime('%A'))
for call in (lambda: DT.max + TD(microseconds=1), lambda: D.min - TD(days=1)):
    try: call()
    except OverflowError as e: print('OverflowError:', e)
'''
SUBPROC = HEAD + r'''# run() waits and returns a CompletedProcess, Popen does not wait, poll() and wait(), check and timeout. The children are Python itself and sleep.
t = time.monotonic(); r = subprocess.run(['sleep', '0.3']); print(r, '| waited:', time.monotonic() - t >= 0.3)
r = subprocess.run([sys.executable, '-c', 'print("hi")'], capture_output=True, text=True)
print(repr(r).replace(sys.executable, 'PY'), r.returncode, repr(r.stdout))
t = time.monotonic(); p = subprocess.Popen(['sleep', '0.4']); print('Popen returned at once:', time.monotonic() - t < 0.2, '| poll:', p.poll())
print('wait:', p.wait(), '| poll after:', p.poll(), '| pid is a number:', p.pid > 0)
for call in (lambda: subprocess.run(['false'], check=True), lambda: subprocess.run(['sleep', '5'], timeout=0.2),
             lambda: subprocess.run(['no-such-program-xyz']), lambda: subprocess.Popen(['sleep', '2']).wait(timeout=0.1)):
    try: call()
    except Exception as e: print(type(e).__name__, e)
c = 'import sys; print(sys.argv[1:])'
print(subprocess.run([sys.executable, '-c', c, 'my file.txt', 'a b', '*.txt'], capture_output=True, text=True).stdout.strip())
b = subprocess.run([sys.executable, '-c', 'import sys; print("out"); print("err", file=sys.stderr)'], capture_output=True)
print(b.stdout, b.stderr, '| text=True gives str')
print('ping -n 4 on Linux exits', subprocess.run(['ping', '-n', '4', 'localhost'], capture_output=True, text=True).returncode, '| ping -c 2 exits', subprocess.run(['ping', '-c', '2', '-W', '2', '127.0.0.1'], capture_output=True, text=True).returncode)
'''
SHELLSAFE = HEAD + r'''# shell=True with a list, a command built from a file name, shlex.quote. start is a Windows command; on POSIX it is not found.
r = subprocess.run(['echo', 'hi', 'there'], shell=True, capture_output=True, text=True); print('list with shell=True prints', repr(r.stdout))
r = subprocess.run('echo hi there', shell=True, capture_output=True, text=True); print('string with shell=True prints', repr(r.stdout))
r = subprocess.run(['start', 'hello.txt'], shell=True, capture_output=True, text=True); print('start hello.txt:', r.returncode, r.stderr.strip().split(': ', 1)[1])
name = 'x; echo INJECTED'
print(repr(subprocess.run(f'echo opening {name}', shell=True, capture_output=True, text=True).stdout))
print(repr(subprocess.run(f'echo opening {shlex.quote(name)}', shell=True, capture_output=True, text=True).stdout))
print(repr(subprocess.run(['echo', 'opening', name], capture_output=True, text=True).stdout))
print(shlex.split("notepad 'my file.txt' x"), shlex.quote('a b'), shlex.join(['a', 'b c']))
import shutil
print('open ->', shutil.which('open'), '| xdg-open ->', shutil.which('xdg-open'), '| startfile:', hasattr(os, 'startfile'))
import webbrowser
print('webbrowser.open without a browser:', webbrowser.open('file:///nonexistent'))
'''
EXITSIG = HEAD + r'''# Exit codes, a negative code for a signal, terminate against kill, and SIGKILL that cannot be handled.
c = lambda code: subprocess.run([sys.executable, '-c', code], stderr=subprocess.DEVNULL).returncode
print([c('pass'), c('import sys; sys.exit(3)'), c('raise ValueError'), c('import sys; sys.exit("msg")'), c('import os; os._exit(256+7)'),
       c('import os,signal; os.kill(os.getpid(), signal.SIGKILL)'), c('import os,signal; os.kill(os.getpid(), signal.SIGTERM)')])
code = "import signal,time,sys\nsignal.signal(signal.SIGTERM, lambda s,f: (print('asked to stop, saving work', flush=True), sys.exit(0)))\nprint('ready', flush=True)\ntime.sleep(30)"
for how in ('terminate', 'kill'):
    p = subprocess.Popen([sys.executable, '-c', code], stdout=subprocess.PIPE, text=True); p.stdout.readline(); getattr(p, how)()
    print(how, '->', repr(p.communicate()[0].strip()), p.returncode)
try: signal.signal(signal.SIGKILL, lambda *a: None)
except OSError as e: print('SIGKILL cannot be handled:', type(e).__name__, e.errno)
'''
SCHEDULERS = HEAD + r'''# The schedulers that live inside a process: sched with a fake clock, threading.Timer, asyncio call_later and the schedule package.
clock = [0.0]; log = []
s = sched.scheduler(lambda: clock[0], lambda d: clock.__setitem__(0, clock[0] + d))
s.enter(5, 1, log.append, ('five',)); s.enter(2, 1, log.append, ('two',)); s.enter(5, 0, log.append, ('five, priority 0',)); s.enter(0, 9, log.append, ('now',))
print('queued', len(s.queue)); s.run(); print(log, clock[0], s.empty())
hits = []
t = threading.Timer(0.1, hits.append, args=('fired',)); t.start(); print('right after start:', hits); t.join(); print('after join:', hits)
t2 = threading.Timer(5, hits.append, args=('never',)); t2.start(); t2.cancel(); t2.join(1); print('cancelled:', hits, t2.is_alive())
import asyncio
order = []
async def main():
    loop = asyncio.get_running_loop(); loop.call_later(0.2, order.append, 'later 0.2'); loop.call_later(0.1, order.append, 'later 0.1'); loop.call_soon(order.append, 'soon')
    await asyncio.sleep(0.3)
asyncio.run(main()); print(order)
try:
    import schedule
    sc = schedule.Scheduler(); j = sc.every().day.at('10:30').do(print, 'job'); sc.every(10).minutes.do(print, 'tick')
    print('schedule', __import__('importlib.metadata', fromlist=['version']).version('schedule'), 'first run', j.next_run.strftime('%H:%M:%S'), 'jobs', len(sc.jobs))
except ImportError:
    print('the schedule package is not installed in this environment')
'''
CRONNEXT = HEAD + r'''# A crontab line has five time fields; with both day fields restricted a day matches if either does. Next runs found by a small matcher
# (the study's own function, written to the rule of the Debian manual page), and a plist and a systemd calendar expression.
def parse(f, lo, hi):
    vals = set()
    for part in f.split(','):
        step = 1
        if '/' in part: part, s = part.split('/'); step = int(s)
        if part == '*': a, b = lo, hi
        elif '-' in part: a, b = map(int, part.split('-'))
        else: a = b = int(part)
        if '/' in f and '-' not in part and part != '*': b = hi
        vals.update(range(a, b + 1, step))
    return vals
def nxt(expr, start):
    m, h, dom, mon, dow = expr.split()
    M, H, DOM, MON, DOW = parse(m, 0, 59), parse(h, 0, 23), parse(dom, 1, 31), parse(mon, 1, 12), parse(dow.replace('7', '0'), 0, 6)
    t = start.replace(second=0, microsecond=0) + TD(minutes=1)
    while True:
        cd = (t.weekday() + 1) % 7
        day = (t.day in DOM) if dow == '*' else (cd in DOW) if dom == '*' else (t.day in DOM or cd in DOW)
        if t.minute in M and t.hour in H and t.month in MON and day: return t
        t += TD(minutes=1)
s = DT(2026, 10, 13, 9, 30)
for e in ('30 9 * * 1-5', '*/15 * * * *', '0 0 13 * 5', '0 4 * * *', '0 0 29 2 *'): print('%-14s next after %s: %s %s' % (e, s, nxt(e, s), nxt(e, s).strftime('%a')))
import plistlib
d = {'Label': 'org.example.backup', 'ProgramArguments': ['/usr/bin/python3', '/Users/al/backup.py'], 'StartCalendarInterval': {'Hour': 4, 'Minute': 0}}
b = plistlib.dumps(d); print('plist', len(b), 'bytes, reads back equal:', plistlib.loads(b) == d)
import shutil
if shutil.which('systemd-analyze'):
    for ex in ('Mon..Fri 09:00', 'daily', 'weekly'):
        r = subprocess.run(['systemd-analyze', 'calendar', ex], capture_output=True, text=True, env=dict(os.environ, TZ='UTC')); print(r.stdout.splitlines()[1].strip())
else:
    print('systemd-analyze is not on this machine')
'''
STOPWATCH = HEAD + r'''# Project 14 (the Super Stopwatch) and Project 15 (the Simple Countdown) on a clock that the program advances, so the laps are known.
import builtins
now = [1000.0]
class FakeTime:
    def time(self): return now[0]
    def sleep(self, s): now[0] += s
ftime = FakeTime()
presses = iter([3.56, 5.07, 9.05, 1.43])
def fake_input(prompt=''):
    try: now[0] += next(presses)
    except StopIteration: raise KeyboardInterrupt
    return ''
# the chapter's program with its en dashes written as minus signs and its f prefix on the print, time replaced by the fake
print('Press ENTER to begin. Afterward, press ENTER to "click" the stopwatch. Press Ctrl-C to quit.')
start_time = ftime.time(); last_time = start_time; lap_number = 1
try:
    while True:
        fake_input()
        lap_time = round(ftime.time() - last_time, 2)
        total_time = round(ftime.time() - start_time, 2)
        print(f'Lap #{lap_number}: {total_time}({lap_time})')
        lap_number += 1
        last_time = ftime.time()
except KeyboardInterrupt:
    print('\nDone.')
print('as shipped, without the f prefix:', 'Lap #{lap_number}: {total_time}({lap_time})')
# Practice program: the columns.
rows = [(1, 3.56, 3.56), (2, 8.63, 5.07), (3, 17.68, 9.05), (4, 19.11, 1.43)]
for n, t, l in rows: print('Lap #' + str(n).rjust(2) + ': ' + str(t).rjust(6) + ' (' + str(l).rjust(6) + ')')
# Project 15: the countdown from 5 with the fake sleep; the chapter counts from 60.
time_left = 5
while time_left > 0:
    print(time_left, end=' '); ftime.sleep(1); time_left = time_left - 1
print('\nthe fake clock advanced', round(now[0] - 1000.0 - sum([3.56, 5.07, 9.05, 1.43]), 2), 'seconds in the countdown; the alarm is played by opening alarm.wav, which needs a desktop')
'''
FRIDAY13 = HEAD + r'''# The practice program: the next ten Friday the 13ths from a fixed day, the walk backward to the end of the date range, and the 400-year cycle.
from collections import Counter
d = D(2026, 10, 13); found = []
while len(found) < 10:
    if d.day == 13 and d.weekday() == 4: found.append(d)
    d += TD(days=1)
print([x.isoformat() for x in found])
d = D(2026, 10, 13); n = 0; first = last = None
try:
    while True:
        if d.day == 13 and d.weekday() == 4:
            n += 1; last = d
            if first is None: first = d
        d -= TD(days=1)
except OverflowError as e: print('backward:', n, 'dates, latest', first, 'earliest', last, '| stopped at', d, '|', e)
by = Counter(D(y, m, 13).weekday() for y in range(2000, 2400) for m in range(1, 13))
print('13ths by weekday in 400 years, Monday first:', [by[i] for i in range(7)], '| cycle days', 400 * 365 + 97, 'mod 7 =', (400 * 365 + 97) % 7)
print('Friday the 13th in the years 1 to 9999: every year has at least one:', all(any(D(y, m, 13).weekday() == 4 for m in range(1, 13)) for y in range(1, 10000)))
'''
PROGRAMS = {
    'epochTimestamp_v1_0_0.py': (EPOCHTIME, (), False),
    'clocksAndSleep_v1_0_0.py': (CLOCKS, (), False),
    'durationsAndDates_v1_0_0.py': (DTARITH, (), False),
    'formatAndParse_v1_0_0.py': (FORMATS, (), False),
    'zonesAndDaylightSaving_v1_0_0.py': (ZONES, (), False),
    'subprocessRunAndPopen_v1_0_0.py': (SUBPROC, (), False),
    'shellSafety_v1_0_0.py': (SHELLSAFE, (), False),
    'exitCodesAndSignals_v1_0_0.py': (EXITSIG, (), False),
    'inProcessSchedulers_v1_0_0.py': (SCHEDULERS, (), False),
    'cronFieldsAndTimers_v1_0_0.py': (CRONNEXT, (), False),
    'stopwatchAndCountdown_v1_0_0.py': (STOPWATCH, (), False),
    'practiceFridayThirteenth_v1_0_0.py': (FRIDAY13, (), False),
}
FIXTURE_BASED = []

if __name__ == "__main__":
    # Usage: /home/claude/venv314_ch19_latest/bin/python sen0414_ch19_corpus_base_v1_0_0.py   (exits 1 if a program does not exit 0)
    import os, subprocess, sys
    bad = 0
    for name, (code, needs, live) in PROGRAMS.items():
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=300)
        bad += r.returncode != 0
        print("=== %s (exit %d)%s" % (name, r.returncode, " LIVE" if live else "")); print(r.stdout.rstrip()[:2400]); print(r.stderr[-400:].rstrip())
    print("%d programs, %d did not exit 0" % (len(PROGRAMS), bad)); sys.exit(1 if bad else 0)
