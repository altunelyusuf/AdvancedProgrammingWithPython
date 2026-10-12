#!/usr/bin/env python3
"""Chapter 19 (Keeping Time, Scheduling Tasks, and Launching Programs): runs the chapter's own listings and interactive statements, whole, and the
files the book ships for the chapter, under the given interpreter, and writes or checks their recorded output.
What is fetched at run time and kept in a cache directory (CH19_CACHE, default the system temp directory): the chapter page
(https://automatetheboringstuff.com/3e/chapter19.html, its sha256 is compared with the chapterDigest of the book's own chapter ontology), the zip of
the 3rd edition's online materials (No Starch Press, sha256 dac627e8...a916) that holds the three files the chapter has (calcProd.py, stopwatch.py,
simplecountdown.py), and alarm.wav, which the chapter points to as https://autbor.com/alarm.wav. None of those files is stored in the repository; every
file is checked against the sha256 recorded here before it is used.
Three environments, all Python 3.14.6 installed with uv, are named by environment variables:
  LATEST  the newest releases on 2026-10-13: pyperclip 1.11.0, playsound3 3.3.2, tzdata 2026.5, schedule 1.2.2 (time, datetime, zoneinfo, subprocess, sched,
          threading, asyncio, signal, webbrowser, plistlib and shlex are the standard library)
  PINS    the version Appendix A of the book pins for the one package of this chapter it pins: playsound3 2.4.0 (pyperclip is listed without a version)
  BARE    no package at all, to see what a reader gets who has installed nothing
The environments are named by CH19_LATEST, CH19_PINS and CH19_BARE (paths of their python), defaults /home/claude/venv314_ch19_latest/bin/python,
/home/claude/venv314_ch19_pins/bin/python and /home/claude/venv314_ch19_bare/bin/python.
Time zones: the machine runs in Europe/Istanbul (UTC+03:00); the author's printed outputs are in America/Los_Angeles. Every replay that depends on the
zone is run under both (TZ is set in the child process), so a difference caused by the zone is told from one caused by the clock or by Python.
Not executed here: Windows (calc.exe, notepad.exe, mspaint.exe, the start command, Task Scheduler), macOS (open of an .app, launchd), a desktop (xdg-open
needs one to open anything), a sound device (alarm.wav is not heard), a clipboard program (pyperclip finds none). What follows the word MEASURED on a line is a
clock reading or a timing of the day; it is recorded and is not compared by the check.
Usage: sen0414_ch19_thirdparty_v1_0_0.py write|check [python]   (python defaults to the LATEST environment)
Record: 08-tooling/ch19-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import json, os, re, subprocess, sys, tempfile
MODE = sys.argv[1] if len(sys.argv) > 1 else "check"
LATEST = os.environ.get("CH19_LATEST", "/home/claude/venv314_ch19_latest/bin/python")
PINS = os.environ.get("CH19_PINS", "/home/claude/venv314_ch19_pins/bin/python")
BARE = os.environ.get("CH19_BARE", "/home/claude/venv314_ch19_bare/bin/python")
PY = sys.argv[2] if len(sys.argv) > 2 else LATEST
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch19-page", "third_party_record_v1_0_0.json")
GET = r'''import os, io, zipfile, hashlib, shutil, tempfile, urllib.request, html, re, json, subprocess, sys, contextlib, warnings, time, datetime
UA = 'SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)'
BROWSER = 'Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0'
CACHE = os.environ.get('CH19_CACHE') or tempfile.gettempdir()
ZIPSHA = 'dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916'
SHA = {'calcProd.py': '829148ea78d9e93b55c068b3584532567e1d355301a0380df8d9e0be814783fc', 'stopwatch.py': 'c3405030450860ee6371080d91edc35f7a1d8c7bab94f7c59d7dcb6fd7b37ab9',
       'simplecountdown.py': '3fc7a82af22a918d912ba46fa171d02061217db4f0c439d81cdf22b3e0eb4fde'}
PREFIX = 'Automate_the_Boring_Stuff_3e_onlinematerials/'
LATEST = os.environ.get('CH19_LATEST', '/home/claude/venv314_ch19_latest/bin/python')
PINS = os.environ.get('CH19_PINS', '/home/claude/venv314_ch19_pins/bin/python')
BARE = os.environ.get('CH19_BARE', '/home/claude/venv314_ch19_bare/bin/python')
def fetch(url, ua=UA):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': ua}), timeout=120).read()
def cached(name, url, ua=UA):
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        open(p + '.part', 'wb').write(fetch(url, ua)); os.replace(p + '.part', p)
    return open(p, 'rb').read()
def chapter(): return cached('ch19_chapter.html', 'https://automatetheboringstuff.com/3e/chapter19.html')
def materials():
    p = os.path.join(CACHE, 'ch19_materials.zip')
    if not os.path.exists(p):
        open(p + '.part', 'wb').write(fetch('https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', BROWSER)); os.replace(p + '.part', p)
    assert hashlib.sha256(open(p, 'rb').read()).hexdigest() == ZIPSHA, 'the online materials differ from the recorded zip'
    return p
def shipped(name):
    b = zipfile.ZipFile(materials()).read(PREFIX + name)
    assert hashlib.sha256(b).hexdigest() == SHA[name], name + ' differs from the recorded file'
    return b
def alarm():
    return cached('ch19_alarm.wav', 'https://autbor.com/alarm.wav')
def work(*names):
    d = tempfile.mkdtemp()
    for n in names: open(os.path.join(d, n), 'wb').write(shipped(n))
    os.chdir(d); return d
def pres():
    h = chapter().decode('utf-8')
    return [html.unescape(re.sub(r'<[^>]+>', '', x)) for x in re.findall(r'<pre\b[^>]*>.*?</pre>', h, re.S)]
def sh(cmd, **k):
    return subprocess.run(cmd, capture_output=True, text=True, **k)
def unmark(text):
    """the book's numbered markers stand in the margin: at the start of a line they are dropped, after indentation they count as two columns"""
    out = []
    for ln in text.split('\n'):
        m = re.match(r'^(\s*)[❶-❿] ', ln)
        out.append((ln[m.end():] if not m.group(1) else m.group(1) + '  ' + ln[m.end():]) if m else ln)
    return '\n'.join(out)
def listing_stopwatch():
    """the stopwatch as the two steps print it, put together: step 1 up to its TODO, then the body of step 2 after --snip--"""
    P = pres(); s1, s2 = unmark(P[5]), unmark(P[6])
    return s1.split('# TODO: Start tracking the lap times.')[0].rstrip() + '\n\n' + s2.split('--snip--', 1)[1].strip('\n') + '\n'
def listing_countdown():
    """simplecountdown.py as the two steps print it: step 1 up to its TODO, then the body of step 2 after --snip--"""
    P = pres(); s1, s2 = unmark(P[25]), unmark(P[26])
    return s1.split('# TODO: At the end of the countdown, play a sound file.')[0].rstrip() + '\n\n' + s2.split('--snip--', 1)[1].strip('\n') + '\n'
EN = '–'
import pty, select, signal
def session(args, steps, env=None, lead=0.6, tail=0.6):
    """runs a program in a pseudo-terminal, as a person at a terminal would: steps are (seconds to wait, bytes to type); \x03 is Ctrl-C"""
    pid, fd = pty.fork()
    if pid == 0:
        signal.signal(signal.SIGINT, signal.SIG_DFL)      # a shell that starts a job in the background leaves SIGINT ignored, and then Ctrl-C does nothing
        if env: os.environ.update(env)
        os.execv(args[0], args)
    out = b''
    def drain(t):
        nonlocal out
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.05)
            if r:
                try: d = os.read(fd, 4096)
                except OSError: return
                if not d: return
                out += d
    drain(lead)
    for delay, data in steps:
        drain(delay); os.write(fd, data)
    drain(tail)
    st = None; end = time.time() + 10
    while time.time() < end:
        try: done, st = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError: st = None; break
        if done: break
        drain(0.2)
    else:
        os.kill(pid, 9); _, st = os.waitpid(pid, 0)
    return out.decode(errors='replace').replace('\r\n', '\n'), (os.waitstatus_to_exitcode(st) if st is not None else None)
'''
REPLAY = r'''PRES = pres()
MARK = re.compile('[❶-❿][ \t]?')
CLOCK = re.compile(r'time\.time\(\)|time\.ctime\(\)|datetime\.now\(\)')
def parse(block, join=''):
    block = MARK.sub('', block)
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
        if ln.startswith('...') and cur is not None and cur['open']:
            cur['src'] += '\n' + ln[4:]
            if ln.strip() == '...': cur['open'] = False
            continue
        if cur is not None and cur['open']:
            cur['src'] += join + ln
            if complete(cur['src']): cur['open'] = False
            continue
        if ln.startswith('...') and cur is not None: continue
        if cur is not None: cur['out'].append(ln)
    return items
def norm(t):
    t = re.sub(r'\s+', '', t)
    t = re.sub(r'0x[0-9A-Fa-f]+', '0xADDR', t)
    return t
def match(expected, got):
    e = norm('\n'.join(expected)); g = norm(got)
    return 'match' if e == g else 'differs'
def kind(src, got):
    """why a statement does not give the printed text: it reads the clock, it needs Windows or macOS, or it has the en dash"""
    if EN in src: return 'en dash'
    if CLOCK.search(src) or re.search(r'\bctime\(', src) or src.strip() in ('now', 'now + thousand_days'): return 'clock'
    if re.search(r'calc\.exe|gnome-calculator|mspaint|notepad|Calculator\.app|calc_proc|paint_proc|proc\.stdout|\[.start.', src): return 'platform'
    return 'other'
def replay(repair=False):
    d = tempfile.mkdtemp(); os.chdir(d); ns = {'__name__': '__main__'}; rows = []
    for bi, blk in enumerate(PRES):
        if '>>> ' not in MARK.sub('', blk)[:12]: continue
        for it in parse(blk):
            if not it['src'].strip(): continue      # the empty prompt that ends a block is not a statement
            src = it['src'].replace(EN, '-') if repair else it['src']; buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf), warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    exec(compile(src + '\n', '<chapter>', 'single'), ns)
                got = buf.getvalue()
            except BaseException as e:
                t = type(e); q = t.__qualname__ if t.__module__ == 'builtins' else t.__module__ + '.' + t.__qualname__
                got = buf.getvalue() + 'Traceback (most recent call last):\n--snip--\n%s: %s' % (q, e)
            rows.append((bi, src, '\n'.join(it['out']), got.rstrip('\n'), match(it['out'], got)))
    return rows
'''
REPLAY_RUN = r'''import sys
rows = replay(repair=(sys.argv[1] == 'repair'))
print(json.dumps(rows))
'''
PROGS = []
PROGS += [
 ("The environments: interpreter, packages and their versions in the three environments of the study, the zone and the clock of the machine, and the two time zone databases", GET + r'''for name, py in (('LATEST', LATEST), ('PINS', PINS), ('BARE', BARE)):
    r = sh([py, '-I', '-c', "import sys, importlib.metadata as m\nd = {x.metadata['Name']: x.version for x in m.distributions()}\nprint(sys.version.split()[0], dict(sorted(d.items())))"])
    print(name, r.stdout.strip() or r.stderr.strip()[-200:])
import zoneinfo, platform, time
print('MEASURED clock', time.time(), time.ctime(), time.tzname, time.timezone)
print('os', platform.platform(), '| TZ environment variable', os.environ.get('TZ'), '| /etc/localtime ->', os.path.realpath('/etc/localtime'))
print('system tz database: first line of /usr/share/zoneinfo/tzdata.zi =', open('/usr/share/zoneinfo/tzdata.zi').readline().strip(), '| zoneinfo.TZPATH', zoneinfo.TZPATH)
print('PyPI tzdata (LATEST):', sh([LATEST, '-I', '-c', 'import tzdata, importlib.metadata as m; print(m.version("tzdata"), tzdata.IANA_VERSION)']).stdout.strip())
print('zoneinfo with PYTHONTZPATH=/nonexistent and no site-packages (-S):', sh([LATEST, '-S', '-c', "import zoneinfo\ntry: zoneinfo.ZoneInfo('Europe/Istanbul'); print('found')\nexcept Exception as e: print(type(e).__name__, e)"], env=dict(os.environ, PYTHONTZPATH='/nonexistent')).stdout.strip())
print('the same with the site-packages of LATEST (tzdata present):', sh([LATEST, '-c', "import zoneinfo\nz = zoneinfo.ZoneInfo('Europe/Istanbul'); print('found', z.utcoffset(__import__('datetime').datetime(2026, 1, 1)))"], env=dict(os.environ, PYTHONTZPATH='/nonexistent')).stdout.strip())
'''),
 ("The listings of the chapter: which of the 29 compile as printed under Python 3.14, and what the compiler says of the others", GET + r'''P = pres(); MK = re.compile('[❶-❿][ \t]?')
print('listings (pre elements):', len(P), '| interactive (start with >>>):', sum(1 for b in P if '>>> ' in MK.sub('', b)[:12]))
bad = []
for i, b in enumerate(P):
    t = MK.sub('', b)
    if '>>> ' in t[:12]:
        for ln in t.split('\n'):
            if ln.startswith('>>> ') and EN in ln: bad.append((i, 'statement', ln[4:60]))
        continue
    if t.lstrip().startswith(('Lap', 'It took')): continue
    try: compile(unmark(b).replace('--snip--', 'pass'), '<listing %d>' % i, 'exec')
    except SyntaxError as e: bad.append((i, type(e).__name__, str(e)[:70]))
for x in bad: print('block %d: %s: %s' % x)
print('characters outside ASCII in the listings, apart from the numbered markers:', sorted({(c, hex(ord(c))) for b in P for c in MK.sub('', b) if ord(c) > 127}))
print('listings with an en dash U+2013 where a minus sign belongs:', [i for i, b in enumerate(P) if EN in b], '| en dashes in all listings:', sum(b.count(EN) for b in P))
'''),
 ("The chapter's interactive statements replayed in the order of the page, as printed, in the author's zone (America/Los_Angeles), under the interpreter of the study", GET + REPLAY + r'''r = subprocess.run([sys.executable, '-c', GETSRC + '\n' + REPLAYSRC + '\n' + REPLAY_RUN, 'asprinted'], capture_output=True, text=True, env=dict(os.environ, TZ='America/Los_Angeles'))
rows = json.loads(r.stdout.strip().splitlines()[-1])
from collections import Counter
print('statements', len(rows), dict(sorted(Counter(x[4] for x in rows).items())), '| by reason, among the ones that differ:', dict(sorted(Counter(kind(x[1], x[3]) for x in rows if x[4] != 'match').items())))
one = lambda s: re.sub(r'\s+', ' ', s)[:90]
for bi, src, exp, got, v in rows:
    k = kind(src, got)
    if v != 'match' and k != 'platform': print('%sblock %d %s (%s) | %s | printed: %s | got: %s' % ('MEASURED ' if k == 'clock' else '', bi, v, k, one(src), one(exp), one(got)))
print('statements that need Windows or macOS and so fail or differ here:', [(bi, one(src)) for bi, src, exp, got, v in rows if v != 'match' and kind(src, got) == 'platform'])
'''),
 ("The same replay with the en dash replaced by the minus sign, in the author's zone and in the zone of the machine", GET + REPLAY + r'''from collections import Counter
res = {}
for z in ('America/Los_Angeles', 'Europe/Istanbul'):
    r = subprocess.run([sys.executable, '-c', GETSRC + '\n' + REPLAYSRC + '\n' + REPLAY_RUN, 'repair'], capture_output=True, text=True, env=dict(os.environ, TZ=z))
    res[z] = json.loads(r.stdout.strip().splitlines()[-1])
    print(z, 'statements', len(res[z]), dict(sorted(Counter(x[4] for x in res[z]).items())), '| differing without a clock reading in the statement:', sum(1 for x in res[z] if x[4] != 'match' and not CLOCK.search(x[1])))
la, ist = res['America/Los_Angeles'], res['Europe/Istanbul']
one = lambda s: re.sub(r'\s+', ' ', s)[:90]
print('by reason among the ones that differ, Los Angeles:', dict(sorted(Counter(kind(x[1], x[3]) for x in la if x[4] != 'match').items())), '| Istanbul:', dict(sorted(Counter(kind(x[1], x[3]) for x in ist if x[4] != 'match').items())))
for (bi, src, exp, g1, v1), (_, _, _, g2, v2) in zip(la, ist):
    k = kind(src, g1)
    if (v1 != 'match' or v2 != 'match') and k != 'platform':
        print('%sblock %d (%s) | %s | printed: %s | Los Angeles: %s %s | Istanbul: %s %s' % ('MEASURED ' if k == 'clock' else '', bi, k, one(src), one(exp), v1, one(g1) if v1 != 'match' else '', v2, one(g2) if v2 != 'match' else ''))
print('statements whose result depends on the zone and on nothing else (match in one zone, differ in the other):', [one(src) for (bi, src, exp, g1, v1), (_, _, _, g2, v2) in zip(la, ist) if v1 != v2 and kind(src, g1) != 'clock'])
'''),
 ("The three files the online materials ship for the chapter, byte for byte: calcProd.py, stopwatch.py and simplecountdown.py, as the interpreter reads them", GET + r'''for n in ('calcProd.py', 'stopwatch.py', 'simplecountdown.py'):
    b = shipped(n); t = b.decode('utf-8')
    print('%-20s %5d bytes sha256 %s | line ends CRLF %d LF-only %d | en dash %d' % (n, len(b), hashlib.sha256(b).hexdigest()[:16], t.count('\r\n'), t.count('\n') - t.count('\r\n'), t.count(EN)))
    try: compile(t, n, 'exec'); print('   compiles')
    except SyntaxError as e: print('   %s: %s' % (type(e).__name__, e))
d = work('calcProd.py', 'stopwatch.py', 'simplecountdown.py')
t = shipped('stopwatch.py').decode(); print('stopwatch.py print line:', [l.strip() for l in t.splitlines() if 'print(' in l and 'Lap' in l], '| f-string prefix present:', "print(f'" in t)
c = shipped('calcProd.py').decode(); print('calcProd.py range and prints:', [l.strip() for l in c.splitlines() if 'range(' in l or 'print(' in l])
s = shipped('simplecountdown.py').decode(); print('simplecountdown.py variable and calls:', [l.strip() for l in s.splitlines() if 'time_left' in l or 'subprocess' in l][:4])
chp = pres()
print('calcProd listing of the chapter loops to', re.search(r'range\(1, (\d+)\)', chp[2]).group(1), '| the shipped file loops to', re.search(r'range\(1, (\d+)\)', c).group(1), '| the chapter prints only the time; the shipped file also prints the number of digits')
fixed = c.replace(EN, '-').replace('\r\n', '\n')
r = sh([sys.executable, '-c', fixed]); print('calcProd.py after replacing the en dash: exit', r.returncode, '|', (r.stderr.strip().splitlines() or [''])[-1][:130])
r = sh([sys.executable, '-c', 'import sys; sys.set_int_max_str_digits(0)\n' + fixed]); print('and with sys.set_int_max_str_digits(0): exit', r.returncode, '|', [l if not l.startswith('It took') else 'MEASURED ' + l for l in r.stdout.strip().splitlines()])
'''),
 ("The profiling listing, calcProd.py of the chapter: as printed, with the minus sign, printing the product, and against math.factorial and time.perf_counter", GET + r'''code = unmark(pres()[2])
open('calcProd_asprinted.py', 'w').write(code)
r = sh([sys.executable, 'calcProd_asprinted.py']); print('as printed: exit', r.returncode, '|', r.stderr.strip().splitlines()[-1])
fixed = code.replace(EN, '-'); open('calcProd.py', 'w').write(fixed)
r = sh([sys.executable, 'calcProd.py']); print('with the minus sign: exit', r.returncode, '| MEASURED', r.stdout.strip(), '| the chapter prints 2.844162940979004 seconds')
r = sh([sys.executable, '-c', fixed + '\nprint(result)']); print('printing the product: exit', r.returncode, '|', r.stderr.strip().splitlines()[-1][:120])
import math
t = time.perf_counter(); a = math.factorial(100000); t1 = time.perf_counter() - t
t = time.perf_counter(); p = 1
for i in range(1, 100001): p = p * i
t2 = time.perf_counter() - t
t = time.perf_counter(); q = math.prod(range(1, 100001)); t3 = time.perf_counter() - t
print('the three products are equal:', a == p == q, '| bits', p.bit_length(), '| MEASURED loop %.3f s, math.prod %.3f s, math.factorial %.4f s' % (t2, t3, t1))
t0 = time.time(); t1 = time.perf_counter(); time.sleep(0.2); print('MEASURED time.time() difference %.6f, perf_counter difference %.6f' % (time.time() - t0, time.perf_counter() - t1))
'''),
 ("Project 14, the Super Stopwatch, put together from its two steps and run in a pseudo-terminal with scripted key presses: as printed, with the minus sign, with the shipped file, and without a terminal", GET + r'''prog = listing_stopwatch(); open('stopwatch_asprinted.py', 'w').write(prog)
r = sh([sys.executable, 'stopwatch_asprinted.py']); print('as printed: exit', r.returncode, '|', r.stderr.strip().splitlines()[-1])
fixed = prog.replace(EN, '-'); open('stopwatch.py', 'w').write(fixed)
steps = [(0.1, b'\n'), (0.7, b'\n'), (1.2, b'\n'), (0.3, b'\x03')]
out, code = session([sys.executable, 'stopwatch.py'], steps)
print('with the minus sign, three ENTER presses and Ctrl-C, typed at a terminal: exit', code); print('MEASURED output', repr(out))
print('the lines of the output without the numbers:', [re.sub(r'[\d.]+', 'N', l) for l in out.splitlines()])
r = sh([sys.executable, 'stopwatch.py'], input=''); print('without a terminal (standard input empty): exit', r.returncode, '|', r.stderr.strip().splitlines()[-1])
r = sh([sys.executable, 'stopwatch.py'], input='\n\n'); print('MEASURED two lines on standard input, no terminal: exit', r.returncode, '| output', repr(r.stdout), '|', r.stderr.strip().splitlines()[-1] if r.stderr else '')
d = work('stopwatch.py'); sw = open('stopwatch.py', encoding='utf-8').read().replace(EN, '-'); open('stopwatch_shipped_fixed.py', 'w').write(sw)
out, code = session([sys.executable, 'stopwatch_shipped_fixed.py'], [(0.1, b'\n'), (0.5, b'\n'), (0.3, b'\x03')])
print('MEASURED the shipped file with the minus sign: exit', code, 'output', repr(out))
print('the book prints the practice output as "Lap #1: 3.56 (3.56)" with a space before the bracket; the listing prints "{total_time}({lap_time})" with none')
'''),
 ("The pause-until-a-date loop of the chapter, run with a date two seconds away, and the time left until Halloween 2039", GET + r'''import datetime, time
src = unmark(pres()[13])
print('the loop as printed compiles:', bool(compile(src, 'l', 'exec')))
target = datetime.datetime.now() + datetime.timedelta(seconds=2)
code = src.replace('datetime.datetime(2039, 10, 31, 0, 0, 0)', 'datetime.datetime.now() + datetime.timedelta(seconds=2)') + '\nprint("loop ended")\n'
t = time.monotonic(); c0 = time.process_time(); r = sh([sys.executable, '-c', code]); e = time.monotonic() - t
print('with the date two seconds ahead: exit', r.returncode, '|', r.stdout.strip(), '| MEASURED wall time %.2f s' % e)
left = datetime.datetime(2039, 10, 31) - datetime.datetime.now()
print('MEASURED time left until 2039-10-31 00:00 on the clock of the machine:', left, '| seconds:', int(left.total_seconds()), '| years about', round(left.days / 365.2425, 2))
print('the loop would call sleep(1) about MEASURED', int(left.total_seconds()), 'times; it checks the wall clock, which can be set, and the local time, which changes at daylight saving time')
'''),
 ("Project 15, the Simple Countdown, put together from its two steps and run whole for 60 seconds, then the shipped file, the file at autbor.com, alarm.wav and the launch of it", GET + r'''prog = listing_countdown(); open('simplecountdown.py', 'w').write(prog)
print('the program as the chapter prints it:'); print(prog)
t = time.monotonic(); r = sh([sys.executable, 'simplecountdown.py']); e = time.monotonic() - t
lines = r.stdout.split()
print('run whole: exit', r.returncode, '| numbers printed', len(lines), 'from', lines[0], 'to', lines[-1], '| subprocess output', repr(r.stderr))
print('MEASURED wall time of the run: %.3f s for 60 sleeps of one second' % e)
print('shipped simplecountdown.py differs from the chapter listing only in:', [(a.strip(), b.strip()) for a, b in zip(shipped('simplecountdown.py').decode().splitlines(), prog.splitlines()) if a.strip() != b.strip()][:4])
online = fetch('https://autbor.com/simplecountdown.py').decode(); print('https://autbor.com/simplecountdown.py: lines that differ from the shipped file:', [l for l in online.splitlines() if l not in shipped('simplecountdown.py').decode().splitlines()])
a = alarm(); import wave
open('alarm.wav', 'wb').write(a); w = wave.open('alarm.wav')
print('alarm.wav: %d bytes, sha256 %s, %d channels, %d bits, %d Hz, %.2f s' % (len(a), hashlib.sha256(a).hexdigest()[:16], w.getnchannels(), w.getsampwidth() * 8, w.getframerate(), w.getnframes() / w.getframerate()))
r = sh(['open', 'alarm.wav'], timeout=60); print("subprocess.run(['open', 'alarm.wav']) on this Linux: exit", r.returncode, '|', r.stderr.strip().splitlines()[-1])
r = sh(['xdg-open', 'alarm.wav'], timeout=60); print("xdg-open alarm.wav: exit", r.returncode, '|', r.stderr.strip().splitlines()[-1])
r = subprocess.run(['start', 'alarm.wav'], shell=True, capture_output=True, text=True); print("subprocess.run(['start', 'alarm.wav'], shell=True) on Linux: exit", r.returncode, '|', r.stderr.strip())
'''),
 ("Practice Program 1, the Prettified Stopwatch: rjust and ljust, and pyperclip in the three environments", GET + r'''rows = [(1, 3.56, 3.56), (2, 8.63, 5.07), (3, 17.68, 9.05), (4, 19.11, 1.43)]
text = '\n'.join('Lap #' + str(n).rjust(2) + ': ' + str(t).rjust(6) + ' (' + str(l).rjust(6) + ')' for n, t, l in rows)
print(text)
printed = pres()[28].rstrip('\n'); print('equal to the output the chapter prints:', text == printed)
print('ljust and rjust:', repr('x'.ljust(3)), repr('x'.rjust(3)), '| a float prints its repr:', str(2.0), str(round(2.004, 2)), '| round(8.63 - 3.56, 2) =', round(8.63 - 3.56, 2), '| 19.11 - 17.68 =', 19.11 - 17.68)
for name, py in (('LATEST', LATEST), ('PINS', PINS), ('BARE', BARE)):
    r = sh([py, '-I', '-c', "import pyperclip\ntry:\n    pyperclip.copy('Lap # 1')\n    print('copied', pyperclip.paste())\nexcept Exception as e: print(type(e).__name__, str(e).splitlines()[0][:100])"])
    print(name, 'pyperclip:', r.stdout.strip() or r.stderr.strip().splitlines()[-1])
print('xclip, xsel, wl-copy on this machine:', [shutil.which(x) for x in ('xclip', 'xsel', 'wl-copy')], '| DISPLAY', os.environ.get('DISPLAY'))
'''),
 ("playsound3, which the chapter names for sound files (Chapter 12), in the pinned and the newest version, on a machine without a sound device", GET + r'''open('alarm.wav', 'wb').write(alarm())
for name, py in (('PINS', PINS), ('LATEST', LATEST), ('BARE', BARE)):
    code = "import time, importlib.metadata as m\nimport playsound3\nprint(m.version('playsound3'), sorted(n for n in dir(playsound3) if not n.startswith('_')))\nt = time.time(); r = playsound3.playsound('alarm.wav')\nprint('returned', type(r).__name__, 'MEASURED %.2f s' % (time.time() - t))"
    r = sh([py, '-I', '-c', code]); lines = [l for l in r.stdout.strip().splitlines()]
    print(name, 'exit', r.returncode, '|', ' | '.join(lines) if lines else r.stderr.strip().splitlines()[-1])
    print('   stderr lines that name ALSA:', sum(1 for l in r.stderr.splitlines() if l.startswith('ALSA')))
'''),
 ("Practice Program 2, the Friday the 13th finder, in the two programs the chapter asks for, from a fixed day", GET + r'''import datetime
one = datetime.timedelta(days=1)
def forward(start, n=10):
    day, found = start, []
    while len(found) < n:
        if day.day == 13 and day.weekday() == 4: found.append(day)
        day += one
    return found
def backward(start):
    day, found = start, []
    try:
        while True:
            if day.day == 13 and day.weekday() == 4: found.append(day)
            day -= one
    except OverflowError as e: return found, str(e), day
start = datetime.datetime(2026, 10, 13)
print('forward from', start.date(), [d.strftime('%B %Y') for d in forward(start)])
f, msg, last = backward(start)
print('backward from', start.date(), ': found', len(f), '| the first three', [d.date().isoformat() for d in f[:3]], '| the last', f[-1].date().isoformat(), '| then OverflowError:', msg, '| the day reached', last.date())
print('the chapter says to stop when it reaches the year 1; the loop above reaches datetime.min and subtracting one more day raises', msg)
print('MEASURED a program that starts from datetime.now() today:', [d.strftime('%B %Y') for d in forward(datetime.datetime.now())][:3])
'''),
 ("Appendix B's answers to the chapter's seven questions, executed", GET + r'''import datetime, time
print('1. the epoch:', time.gmtime(0)[:6], 'in UTC')
print('2. time.time() returns a', type(time.time()).__name__)
print('3. time.asctime() == time.ctime():', time.asctime() == time.ctime(), '| time.asctime(time.gmtime(1773813875)) =', time.asctime(time.gmtime(1773813875)))
t = time.monotonic(); time.sleep(5); print('4. time.sleep(5): MEASURED %.3f s' % (time.monotonic() - t))
print('5. round(2.4), round(2.5), round(3.5), round(2.675, 2):', round(2.4), round(2.5), round(3.5), round(2.675, 2), '| type of round(2.5):', type(round(2.5)).__name__, '| type of round(2.5, 1):', type(round(2.5, 1)).__name__)
print('6. datetime vs timedelta:', datetime.datetime(2026, 1, 1) - datetime.datetime(2025, 1, 1), '(a timedelta)')
d = datetime.datetime(2019, 1, 7); print('7. datetime.datetime(2019, 1, 7).weekday():', d.weekday(), '| strftime %A:', d.strftime('%A'), '| isoweekday:', d.isoweekday())
print('Question 3 asks for a function that returns "Mon Jun 15 14:00:38 2026":', repr(time.strftime('%a %b %d %H:%M:%S %Y', time.struct_time((2026, 6, 15, 14, 0, 38, 0, 166, 0)))), '- June 15, 2026 is a', datetime.date(2026, 6, 15).strftime('%A'))
'''),
]
def run(code):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1"); env.pop("PYTHONPATH", None)
    code = code.replace("GETSRC", repr(GET_SOURCE)).replace("REPLAYSRC", repr(REPLAY_SOURCE)).replace("REPLAY_RUN", repr(REPLAY_RUN)) if "GETSRC" in code else code
    r = subprocess.run([PY, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env, timeout=1800, cwd=tempfile.mkdtemp())
    o = (r.stdout if r.returncode == 0 else r.stdout + "FAILED: " + (r.stderr.strip().splitlines() or ["?"])[-1]).rstrip("\n")
    return re.sub(r"0x[0-9a-f]{6,}", "0x...", o)   # the address of an object differs from run to run
GET_SOURCE = GET; REPLAY_SOURCE = REPLAY
if __name__ == "__main__":
    out = [{"what": w, "code": c, "output": run(c)} for w, c in PROGS]
    strip = lambda s: "\n".join(l.split("MEASURED")[0] + ("MEASURED" if "MEASURED" in l else "") for l in s.split("\n"))   # what follows the word MEASURED on a line is not compared
    if MODE == "write":
        ver = subprocess.run([PY, "-c", "import sys, importlib.metadata as m; print(sys.version.split()[0], 'pyperclip', m.version('pyperclip'), 'tzdata', m.version('tzdata'), 'playsound3', m.version('playsound3'), 'schedule', m.version('schedule'))"], capture_output=True, text=True).stdout.strip()
        json.dump({"_version": "1.0.0", "_note": "Recorded by sen0414_ch19_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter named in the field python, on a machine in the zone Europe/Istanbul. The chapter page, the online materials and alarm.wav are fetched at run time and not kept in the repository. A line that starts with MEASURED is a clock reading or a timing of the day.", "python": ver, "items": out}, open(REC, "w"), indent=1, ensure_ascii=False)
        print("recorded", len(out), "programs to", REC)
        for o in out:
            if "FAILED" in o["output"]: print("  FAILED:", o["what"], "|", o["output"][-200:])
    else:
        old = json.load(open(REC))["items"]; bad = [a["what"] for a, b in zip(old, out) if strip(a["output"]) != strip(b["output"]) or a["code"] != b["code"]]
        print("%d programs; %d differ" % (len(out), len(bad)))
        for b in bad: print("  DIFFERS", b)
        sys.exit(1 if bad else 0)
