#!/usr/bin/env python3
"""Chapter 19: runs one program, the chapter's time, datetime, zoneinfo, subprocess, sched, threading and signal operations in a row, under every
installed 3.14 patch release (3.14.0 to 3.14.6, `uv python install 3.14.N`) and, for comparison, under 3.15 (a beta, 3.15.0b4, the newest uv offers),
3.13, 3.12 and 3.11, and records what each printed. It answers the question chapters 13 to 18 answered with a difference: does anything the chapter
teaches change between the patch releases of Python 3.14, and between 3.14 and the releases before it? There is no package: time, datetime, zoneinfo,
subprocess, sched, threading, asyncio, signal, shlex and calendar are the standard library of each interpreter, so a difference comes from the
interpreter. The zone is set by TZ in the child process (America/Los_Angeles, the author's, and the machine's own Europe/Istanbul) so that a printed time
can be compared; the operating system is Ubuntu 24.04 and the system time zone database is the tzdata package of the machine (version 2026c).
python runs in isolated mode, each interpreter by `uv run --no-project`.
Usage: sen0414_ch19_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch19-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch19-page", "interpreter_record_v1_0_0.json")
PROG = r'''
import sys, os, io, time, datetime, warnings, signal, threading, sched, calendar, shlex, subprocess, zoneinfo, json, locale
from datetime import datetime as DT, timedelta as TD, date as D, timezone
from zoneinfo import ZoneInfo
res = {}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except Exception as e: v = type(e).__name__ + ': ' + str(e)[:110]
    return [v, sorted({x.category.__name__ for x in seen})]
res['series'] = sys.version.split()[0].rsplit('.', 1)[0] + '.x'
res['platform'] = [sys.platform, os.name]
# the chapter's arithmetic and formats
res['chapter arithmetic'] = [str(DT(2026, 12, 2, 18, 38, 50, 636181) + TD(days=1000)), str(DT(2026, 10, 21, 16, 29) - TD(days=365 * 30)), str(DT(2026, 10, 21, 16, 29) - 2 * TD(days=365 * 30)),
                             str(TD(days=11, hours=10, minutes=9, seconds=8)), TD(days=11, hours=10, minutes=9, seconds=8).total_seconds()]
res['strftime examples'] = [DT(2026, 10, 21, 16, 29).strftime(f) for f in ('%Y/%m/%d %H:%M:%S', '%I:%M %p', "%B of '%y")]
res['strptime examples'] = [str(DT.strptime(s, f)) for s, f in (('October 21, 2026', '%B %d, %Y'), ("November of '63", "%B of '%y"), ("November of '73", "%B of '%y"))]
res['two digit year pivot'] = [DT.strptime(s, '%y').year for s in ('68', '69')]
res['weekday of 2019-01-07'] = [D(2019, 1, 7).weekday(), D(2019, 1, 7).strftime('%A')]
res['ctime of 1773813875 under three zones'] = {z: subprocess.run([sys.executable, '-c', 'import time; print(time.ctime(1773813875))'], capture_output=True, text=True, env=dict(os.environ, TZ=z)).stdout.strip() for z in ('America/Los_Angeles', 'Europe/Istanbul', 'UTC')}
res['fromtimestamp(1000000) under three zones'] = {z: subprocess.run([sys.executable, '-c', 'import datetime; print(repr(datetime.datetime.fromtimestamp(1000000)))'], capture_output=True, text=True, env=dict(os.environ, TZ=z)).stdout.strip() for z in ('America/Los_Angeles', 'Europe/Istanbul', 'UTC')}
# what changed in the releases
res['utcnow and utcfromtimestamp'] = w(lambda: [DT.utcnow().tzinfo, str(DT.utcfromtimestamp(0))])
res['datetime.UTC'] = w(lambda: str(datetime.UTC))
res['strptime month and day only, 29 February'] = w(lambda: str(DT.strptime('02/29', '%m/%d')))
res['strptime month and day only, 21 October'] = w(lambda: str(DT.strptime('10/21', '%m/%d')))
res['date.strptime and time.strptime'] = [hasattr(D, 'strptime'), hasattr(datetime.time, 'strptime')]
res['fromisoformat of 20261021T162907+0300 and 2026-10-21T16:29:07Z'] = w(lambda: [str(DT.fromisoformat('20261021T162907+0300')), str(DT.fromisoformat('2026-10-21T16:29:07Z'))])
res['fromisoformat of 2026-W43-3 (a date)'] = w(lambda: str(D.fromisoformat('2026-W43-3')))
res['strftime %:z'] = w(lambda: DT(2026, 1, 1, tzinfo=timezone(TD(hours=3))).strftime('%:z'))
res['timedelta(months=1)'] = w(lambda: TD(months=1))
res['sleep(-1) and sleep("1")'] = [w(lambda: time.sleep(-1))[0], w(lambda: time.sleep('1'))[0]]
res['int to str limit'] = w(lambda: [sys.get_int_max_str_digits(), len(str(10 ** 5000))])
res['clock info of time, monotonic, perf_counter'] = {n: [time.get_clock_info(n).implementation, time.get_clock_info(n).monotonic, time.get_clock_info(n).adjustable] for n in ('time', 'monotonic', 'perf_counter')}
res['time.sleep survives a signal handler (PEP 475)'] = w(lambda: (lambda hits: (signal.signal(signal.SIGALRM, lambda s, f: hits.append(1)), signal.setitimer(signal.ITIMER_REAL, 0.05), time.sleep(0.2), hits)[-1])([]))
def sleepsecs():
    a = time.monotonic(); time.sleep(0.1); return time.monotonic() - a >= 0.1
res['sleep lasts at least the time asked (monotonic clock)'] = w(sleepsecs)
res['zoneinfo: offsets'] = w(lambda: [str(ZoneInfo('America/Los_Angeles').utcoffset(DT(2026, 3, 17))), str(ZoneInfo('Europe/Istanbul').utcoffset(DT(2016, 1, 1))), str(ZoneInfo('Europe/Istanbul').utcoffset(DT(2017, 1, 1)))])
def fold():
    ny = ZoneInfo('America/New_York'); a = DT(2026, 11, 1, 1, 30, tzinfo=ny); b = a.replace(fold=1)
    return [str(a.utcoffset()), str(b.utcoffset()), a == b, str(DT(2026, 3, 8, 2, 30, tzinfo=ny).astimezone(timezone.utc))]
res['zoneinfo: ambiguous and nonexistent times (PEP 495)'] = w(fold)
res['aware plus one day across daylight saving time'] = w(lambda: (lambda ny: [str((DT(2026, 3, 7, 12, tzinfo=ny) + TD(days=1)).astimezone(timezone.utc) - DT(2026, 3, 7, 12, tzinfo=ny).astimezone(timezone.utc))])(ZoneInfo('America/New_York')))
res['naive and aware compared'] = w(lambda: DT(2026, 1, 1) < DT(2026, 1, 1, tzinfo=timezone.utc))
res['year 2038 and the datetime range'] = w(lambda: [str(DT.fromtimestamp(2 ** 31, timezone.utc)), str(D.max), w(lambda: D.max + TD(days=1))[0]])
res['syntax: an en dash in an expression'] = w(lambda: compile('x = 5 \u2013 3', 'f', 'exec'))
res['syntax: backslash A in a string, compile'] = w(lambda: compile('x = "C:\\\\Users\\Al"', 'f', 'exec') and 'compiled')
res['syntax: backslash A in a string, with -W error'] = [subprocess.run([sys.executable, '-W', 'error', '-c', 'x = "C:\\\\Users\\Al"'], capture_output=True, text=True).stderr.strip().splitlines()[-1][:110]]
# subprocess
res['subprocess: FileNotFoundError text'] = w(lambda: subprocess.run(['/usr/bin/gnome-calculator']))
res['subprocess: the repr of a CompletedProcess'] = repr(subprocess.run(['true'])), repr(subprocess.run(['false']))
res['subprocess: a list with shell=True on POSIX'] = subprocess.run(['echo', 'hi', 'there'], shell=True, capture_output=True, text=True).stdout
res['subprocess: poll then wait'] = (lambda p: [p.poll(), p.wait(), p.poll()])(subprocess.Popen(['sleep', '0.1']))
res['subprocess: kill gives'] = (lambda p: (p.kill(), p.wait())[1])(subprocess.Popen(['sleep', '5']))
res['subprocess: timeout text'] = w(lambda: subprocess.run(['sleep', '2'], timeout=0.1))
res['subprocess: capture_output with stdout'] = w(lambda: subprocess.run(['true'], capture_output=True, stdout=subprocess.PIPE))
res['subprocess: check=True'] = w(lambda: subprocess.run(['false'], check=True))
res['subprocess: process_group argument (3.11)'] = w(lambda: subprocess.run(['true'], process_group=0).returncode)
# in-process scheduling
def sched_order():
    clock = [0.0]; log = []; s = sched.scheduler(lambda: clock[0], lambda d: clock.__setitem__(0, clock[0] + d))
    s.enter(5, 1, log.append, ('five',)); s.enter(2, 1, log.append, ('two',)); s.enter(5, 0, log.append, ('five p0',)); s.run(); return log
res['sched: order by time then priority'] = w(sched_order)
def timer():
    hits = []; t = threading.Timer(0.05, hits.append, args=('fired',)); t.start(); t.join(); return hits
res['threading.Timer fires once'] = w(timer)
def alater():
    import asyncio
    log = []
    async def main():
        l = asyncio.get_running_loop(); l.call_later(0.1, log.append, 'b'); l.call_later(0.05, log.append, 'a'); await asyncio.sleep(0.2)
    asyncio.run(main()); return log
res['asyncio call_later order'] = w(alater)
res['shlex.quote of a name with a semicolon'] = shlex.quote('x; echo INJECTED')
res['calendar facts'] = [calendar.isleap(1900), calendar.isleap(2000), calendar.timegm((2017, 1, 1, 0, 0, 0)) - calendar.timegm((2016, 12, 31, 23, 59, 59))]
res['Friday the 13th in 400 years'] = sum(1 for y in range(2000, 2400) for m in range(1, 13) if D(y, m, 13).weekday() == 4)
res['webbrowser.open without a browser'] = w(lambda: __import__('webbrowser').open('file:///nonexistent'))
res['os.startfile exists'] = hasattr(os, 'startfile')
res['locale encoding'] = [locale.getencoding(), sys.flags.utf8_mode]
print(json.dumps(res, sort_keys=True, default=repr))
'''
INTERPRETERS = ["3.11", "3.12", "3.13", "3.14.0", "3.14.1", "3.14.2", "3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.15"]
def run(py):
    env = dict(os.environ); env.pop("PYTHONPATH", None); env["TZ"] = "Europe/Istanbul"
    r = subprocess.run(["uv", "run", "--no-project", "--python", py, "python", "-I", "-c", PROG], capture_output=True, text=True, env=env, timeout=900)
    if r.returncode != 0: return {"error": (r.stderr.strip().splitlines() or ["?"])[-1]}
    return json.loads(r.stdout.strip().splitlines()[-1])
if __name__ == "__main__":
    results = {}
    for py in INTERPRETERS:
        v = subprocess.run(["uv", "run", "--no-project", "--python", py, "python", "-c", "import sys; print(sys.version.split()[0])"], capture_output=True, text=True).stdout.strip()
        results[v or py] = run(py); print(py, v, "ok" if "error" not in results[v or py] else results[v or py]["error"])
    keys = sorted({k for r in results.values() for k in r if k != "series"})
    differ = {}
    for k in keys:
        vals = {}
        for v, r in results.items(): vals.setdefault(json.dumps(r.get(k), sort_keys=True), []).append(v)
        if len(vals) > 1: differ[k] = [[json.loads(a), b] for a, b in vals.items()]
    json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "_note": "Recorded by sen0414_ch19_interpreters_v1_0_0.py: one program (the chapter's time, datetime, zoneinfo, subprocess, sched, threading and signal operations) under each interpreter, no package in any. The zone of the child process is Europe/Istanbul unless an item names another. 'differ' lists the items whose value is not the same under every interpreter, each value with the interpreters that gave it; the items not listed were identical everywhere.",
               "program": PROG, "interpreters": list(results), "results": results, "items compared": len(keys), "differ": differ}, open(OUT, "w"), indent=1, ensure_ascii=False)
    print("recorded", len(results), "interpreters;", len(keys), "items; items that differ:", sorted(differ))
