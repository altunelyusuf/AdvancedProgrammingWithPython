#!/usr/bin/env python3
"""Chapter 24 (Text-to-Speech and Speech Recognition Engines): runs the chapter's own listings, whole and as printed, under the given interpreters and package sets with the REAL eSpeak NG 1.51
as the engine of pyttsx3 and the real Whisper models on the CPU (no sound card, no GPU, no microphone: NOT heard; the speech goes to the engine and nothing plays), and writes or checks
their recorded output.
What is fetched at run time and kept in a cache directory (CH24_CACHE, default the system temp directory): the chapter page (https://automatetheboringstuff.com/3e/chapter24.html; its
sha256 is compared with the chapterDigest of the book's own chapter ontology, 239d91a7...462b0b). Nothing of it is stored in the repository.
The listings are not typed in here: every listing is parsed from the page itself (the prompt lines, the continuation lines and the printed output that follows them; the numbered call-out
marks of the typesetting are dropped) and every statement is run in the order of the book, in one session, as printed. The page has 17 listings: 1 program (hello_tts.py, run with the
keyboard answer supplied), 11 interactive sessions, 3 printed subtitle files (SRT, VTT and TSV: compared with what Whisper's writers produce for the two segments the book prints), 1 line
of print() and 1 line of speak(), and the lyrics of the song (text). Substitutions, each recorded: listings 11 and 12 download a video from YouTube and are NOT EXECUTED against YouTube
(the study asks YouTube for metadata only); listing 12 is run again with the address of a public-domain LibriVox reading hosted by the Internet Archive instead (listing 13 then finds its
file); listing 14 is run as printed (metadata, no download).
Rows of the record (Python 3.14.6 unless named, installed with uv):
  LATEST    pyttsx3 2.99, openai-whisper 20250625, yt-dlp 2026.8.19, torch 2.14.1+cpu, NumPy 2.5.4: /home/claude/venv314_ch24_latest
  PINS      Python 3.12.3, pyttsx3 2.98, openai-whisper 20231117, NumPy 1.26.4, torch 2.14.1+cpu, yt-dlp 2026.8.19: the versions Appendix A pins (installed with pip --no-build-isolation
            because `pip install openai-whisper==20231117` fails today, see the live record): /home/claude/venv312_ch24_pins
  BARE      no package at all: /home/claude/venv314_ch24_bare
  NOFFMPEG  the LATEST environment with a PATH that holds no ffmpeg and no ffprobe
Not executed: Windows (SAPI5), macOS (NSSpeechSynthesizer), a sound card, a microphone, a GPU, the author's voices, a download from YouTube.
Usage: sen0414_ch24_thirdparty_v1_0_0.py write|check
Record: 08-tooling/ch24-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import hashlib, html, json, os, re, subprocess, sys, tempfile, time, urllib.request
MODE = sys.argv[1] if len(sys.argv) > 1 else "check"
HOME = "/home/claude"
ROWS = [("LATEST", os.environ.get("CH24_LATEST", HOME + "/venv314_ch24_latest/bin/python")), ("PINS", os.environ.get("CH24_PINS", HOME + "/venv312_ch24_pins/bin/python")),
        ("BARE", os.environ.get("CH24_BARE", HOME + "/venv314_ch24_bare/bin/python")), ("NOFFMPEG", os.environ.get("CH24_LATEST", HOME + "/venv314_ch24_latest/bin/python"))]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch24-page", "third_party_record_v1_0_0.json")
CACHE = os.environ.get("CH24_CACHE") or tempfile.gettempdir()
DIGEST = "239d91a73d232342d42b8c6c514a603eb3562681904a53b29f83214ac5462b0b"
UA = {"User-Agent": "SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)"}
def chapter():
    p = os.path.join(CACHE, "ch24_chapter.html")
    if not os.path.exists(p):
        open(p + ".part", "wb").write(urllib.request.urlopen(urllib.request.Request("https://automatetheboringstuff.com/3e/chapter24.html", headers=UA), timeout=120).read()); os.replace(p + ".part", p)
    b = open(p, "rb").read(); assert hashlib.sha256(b).hexdigest() == DIGEST, "the chapter page differs from the one the study recorded"
    return b.decode("utf-8")
def pres(): return [html.unescape(re.sub(r"<[^>]+>", "", p)) for p in re.findall(r"<pre[^>]*>(.*?)</pre>", chapter(), re.S)]
def depth(s): return sum(s.count(c) for c in "([{") - sum(s.count(c) for c in ")]}")
def clean(t): return re.sub(r" ?[❶-❿]", "", re.sub(r"(?<=\s)[❶-❿] ", "  ", t))   # a call-out mark that stands inside the indentation of a code line takes the width of two spaces
def parse_repl(text):
    """statements of an interactive listing: [(source, expected output)]. A line without a prompt that follows a statement whose brackets are still open belongs to the statement."""
    out = []; cur = None
    for raw in clean(text).split("\n"):
        l = raw.rstrip()
        if cur is not None and not cur["out"] and depth("\n".join(cur["src"])) > 0 and not l.startswith(">>>"):
            cur["src"].append(l[4:] if l.startswith("... ") else l.lstrip("."))
        elif l.startswith(">>> ") or l == ">>>": cur = {"src": [l[4:]], "out": []}; out.append(cur)
        elif l.startswith("...") and cur is not None and not cur["out"]: cur["src"].append(l[4:] if l.startswith("... ") else l[3:])
        elif cur is not None: cur["out"].append(l)
    return [("\n".join(c["src"]).rstrip("\n"), "\n".join(c["out"]).strip("\n")) for c in out]
def listings():
    """[(number, title, kind, [(source, expected output)])] for the 17 listings of the page"""
    P = pres(); res = []
    for n, p in enumerate(P, 1):
        first = [l for l in clean(p).split("\n") if l.strip()][0]
        if first.startswith(">>>"): res.append((n, "listing %d" % n, "repl", parse_repl(p)))
        elif n in (7, 8, 9): res.append((n, "listing %d" % n, "subtitle", [(clean(p).strip("\n"), "")]))
        elif n == 17: res.append((n, "listing %d" % n, "lyrics", [(clean(p).strip("\n"), "")]))
        elif n in (15, 16): res.append((n, "listing %d" % n, "statements", [(clean(p).strip("\n"), "")]))
        else: res.append((n, "listing %d" % n, "program", [(clean(p).strip("\n"), "")]))
    return res
HARNESS = r"""import os, sys, io, re, json, time, tempfile, warnings, contextlib, subprocess, builtins
warnings.simplefilter('ignore')
spec = json.load(open(os.environ['SPEC_FILE']))
def norm(t): return re.sub(r'\s+', '', t)
def lines(t): return [l.strip() for l in t.split('\n') if l.strip()]
def matches(got, exp): return norm(got) == norm(exp)
def addr(t): return re.sub(r'0x[0-9A-Fa-f]+', '0xADDR', t)
def differences(got, exp):
    gl, el = lines(got), lines(exp); out = []
    for a, b in zip(gl, el):
        if norm(a) != norm(b): out.append({'got': a, 'book': b})
    if len(gl) != len(el): out.append({'lines printed': len(gl), 'lines in the book': len(el)})
    return out[:6]
NS = {}; results = []; probes = {}
def settle(limit=120, quiet=0.6):
    # the book is typed by a person at the speed of a person: wait until the files of the working folder have stopped growing, because runAndWait() of pyttsx3 can return while a WAV is still being written
    t0 = time.time(); last = None; since = time.time()
    while time.time() - t0 < limit:
        cur = sorted((f, os.path.getsize(f)) for f in os.listdir('.') if os.path.isfile(f))
        if cur != last: last = cur; since = time.time()
        elif time.time() - since >= quiet: return
        time.sleep(0.05)
os.chdir(tempfile.mkdtemp())
ARCHIVE = 'https://archive.org/details/gettysburg_shurtagal_librivox'; NS['ARCHIVE'] = ARCHIVE
def run_stmt(src, n, mode):
    buf = io.StringIO(); shown = []; old = sys.displayhook; sys.displayhook = lambda v: (shown.append(repr(v)) if v is not None else None)
    t0 = time.time()
    try:
        with contextlib.redirect_stdout(buf), warnings.catch_warnings(record=True) as wr:
            warnings.simplefilter('always')
            exec(compile(src.rstrip('\n') + '\n', '<listing %d>' % n, mode), NS)
        got = (buf.getvalue() + ''.join(s + '\n' for s in shown)).strip()
        return {'printed': got[:700], 'raised': None, 'seconds': round(time.time() - t0, 1), 'warnings': sorted({'%s: %s' % (x.category.__name__, str(x.message)[:80]) for x in wr if x.category.__name__ != 'ResourceWarning'})}, got
    except BaseException as e:
        return {'printed': buf.getvalue().strip()[:300], 'raised': '%s: %s' % (type(e).__name__, str(e).splitlines()[0][:150] if str(e) else ''), 'seconds': round(time.time() - t0, 1), 'warnings': []}, ''
    finally: sys.displayhook = old
_run_stmt = run_stmt
def run_stmt(src, n, mode):
    out = _run_stmt(src, n, mode); settle(); return out
def not_executed(why): return {'printed': '', 'raised': None, 'not executed': why, 'seconds': 0, 'warnings': []}
BOOKRES = {'text': ' Dinosaurs are a diverse group of reptiles of the clade dinosauria. They first appeared during the triassic period. Between 245 and 233.23 million years ago.', 'language': 'en',
           'segments': [{'id': 0, 'start': 0.0, 'end': 5.64, 'text': ' Dinosaurs are a diverse group of reptiles of the clade dinosauria. They first'}, {'id': 1, 'start': 5.64, 'end': 14.96, 'text': ' appeared during the triassic period. Between 245 and 233.23 million years ago.'}]}
for n, title, kind, stmts in spec['listings']:
    rows = []
    for src, exp in stmts:
        row = {'source': src}
        if kind == 'program':
            builtins.input = lambda prompt='': (sys.stdout.write(prompt + 'fine\n'), 'fine')[1]
            r, got = run_stmt(src, n, 'exec'); row['as printed'] = r; row['book prints'] = ''
        elif kind == 'statements':
            r, got = run_stmt(src, n, 'exec'); row['as printed'] = r; row['book prints'] = ''
        elif kind == 'lyrics':
            row['as printed'] = {'printed': '', 'raised': None, 'not executed': 'the lyrics are text, not code; the study compares them with the song its program writes', 'seconds': 0, 'warnings': []}; row['book prints'] = src[:200]
        elif kind == 'subtitle':
            fmt = {7: 'srt', 8: 'vtt', 9: 'tsv'}[n]
            code = "import whisper\nfrom whisper.utils import get_writer\nget_writer(%r, '.')(%r, 'audio')\nout = open('audio.%s', encoding='utf-8').read()" % (fmt, BOOKRES, fmt)
            r, got = run_stmt(code, n, 'exec'); out = NS.get('out', '') if r['raised'] is None else ''
            book = src.replace('--snip--', '').strip()
            r['printed'] = out[:400]; r['matches the book'] = (norm(out) == norm(book)); r['byte-for-byte equal to the book after trimming blank ends'] = (out.strip() == book.strip())
            if r['raised'] is None and not r['matches the book']: r['differences from the book'] = differences(out, book)
            if fmt == 'tsv' and r['raised'] is None: r['tabs in the written file'] = out.count('\t'); r['spaces-only separators in the book listing'] = ('\t' not in src)
            row['as printed'] = r; row['book prints'] = src[:300]; rows.append(row); continue
        else:
            if n in (11,) and 'download' in src:
                row['as printed'] = not_executed('listing 11 downloads the video from YouTube; the study does not download from YouTube'); row['book prints'] = exp[:300]; rows.append(row); continue
            if n == 12 and 'ydl.download' in src:
                row['as printed'] = not_executed('listing 12 downloads and converts the video of YouTube; the study does not download from YouTube (see the substituted statement below)'); row['book prints'] = exp[:300]; rows.append(row)
                sub = src.replace("ydl.download([video_url])", "ydl.download([ARCHIVE])")
                r, got = run_stmt(sub, n, 'single'); r['substituted'] = 'the address of a public-domain LibriVox reading on the Internet Archive instead of the YouTube address'
                rows.append({'source': sub, 'as printed': r, 'book prints': ''}); continue
            r, got = run_stmt(src, n, 'single')
            if exp and r['raised'] is None:
                r['matches the book'] = matches(got, exp)
                if not r['matches the book']:
                    r['differences from the book'] = differences(got, exp); r['matches the book except object addresses'] = matches(addr(got), addr(exp))
            elif not exp and r['raised'] is None: r['matches the book'] = True if not got else False
            else: r['matches the book'] = False
            row['as printed'] = r; row['book prints'] = exp[:300]; rows.append(row); continue
        r = row['as printed']; r['matches the book'] = r['raised'] is None
        rows.append(row)
    results.append({'listing': n, 'what': title, 'statements': rows})
def peek(f):
    try: return f()
    except BaseException as e: return type(e).__name__
probes['files in the working folder after the listings'] = sorted(os.listdir('.'))
probes['hello.wav'] = peek(lambda: (lambda w: [w.getnchannels(), w.getsampwidth(), w.getframerate(), round(w.getnframes() / w.getframerate(), 2)])(__import__('wave').open('hello.wav')))
probes['audio.srt exists'] = os.path.exists('audio.srt')
probes['downloaded_content.m4a exists'] = os.path.exists('downloaded_content.m4a')
json.dump({'results': results, 'probes after the listings': probes}, open(os.environ['RESULT_FILE'], 'w'), default=repr, ensure_ascii=False)
"""
def sh(py, code, env=None, timeout=300):
    r = subprocess.run([py, "-W", "ignore::ResourceWarning", "-c", code], capture_output=True, text=True, env=env or os.environ, timeout=timeout, stdin=subprocess.DEVNULL)
    return r.stdout.strip(), r.stderr.strip(), r.returncode
ENVINFO = r"""import sys, importlib.metadata as md, json, shutil
out = {'python': sys.version.split()[0]}
for n in ('pyttsx3', 'openai-whisper', 'yt-dlp', 'torch', 'numpy', 'numba', 'tiktoken'):
    try: out[n] = md.version(n)
    except md.PackageNotFoundError: out[n] = None
out['ffmpeg on the PATH'] = shutil.which('ffmpeg'); out['espeak-ng on the PATH'] = shutil.which('espeak-ng'); out['aplay on the PATH'] = shutil.which('aplay')
print(json.dumps(out))"""
def nopath_env():
    bindir = tempfile.mkdtemp()
    for n in os.listdir("/usr/bin"):
        if n not in ("ffmpeg", "ffprobe"):
            try: os.symlink("/usr/bin/" + n, os.path.join(bindir, n))
            except OSError: pass
    return bindir
def run_row(name, py, specs):
    """output in files, not pipes: a child that outlives its parent keeps the pipes open"""
    env = dict(os.environ); env.pop("DISPLAY", None); env["CH24_CACHE"] = CACHE
    if name == "NOFFMPEG": env["PATH"] = os.path.dirname(py) + ":" + nopath_env()
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(specs, f); f.close(); env["SPEC_FILE"] = f.name
    res = tempfile.NamedTemporaryFile(suffix=".json", delete=False); res.close(); env["RESULT_FILE"] = res.name
    err = tempfile.NamedTemporaryFile(suffix=".err", delete=False)
    p = subprocess.Popen([py, "-W", "ignore", "-c", HARNESS], stdout=subprocess.DEVNULL, stderr=err, env=env, stdin=subprocess.DEVNULL)
    try: rc = p.wait(timeout=2400)
    except subprocess.TimeoutExpired: p.kill(); rc = -9
    if rc or not os.path.getsize(res.name): return {"harness failed": open(err.name).read().strip()[-500:]}
    return json.load(open(res.name))
def record():
    L = listings(); n_statements = sum(len(s) for _, _, _, s in L); items = []
    spec = {"listings": [list(x) for x in L]}
    items.append({"what": "The rows of the study: interpreter and packages of each row", "output": {n: json.loads(sh(p, ENVINFO, env=(dict(os.environ, PATH=os.path.dirname(p) + ":" + nopath_env()) if n == "NOFFMPEG" else None))[0]) for n, p in ROWS}})
    t = chapter()
    items.append({"what": "The chapter page: %d listings found and replayed statement by statement (%d statements); figures and the table counted" % (len(L), n_statements),
                  "output": {"listings": len(L), "kinds": {k: sum(1 for x in L if x[2] == k) for k in ("repl", "program", "statements", "subtitle", "lyrics")}, "statements": n_statements, "figures": sorted(set(re.findall(r"Figure 24-\d", t))), "tables": sorted(set(re.findall(r"Table 24-\d", t))), "sha256": hashlib.sha256(t.encode()).hexdigest()}})
    for name, py in ROWS:
        items.append({"what": "Replay as printed, row %s (all 17 listings in one session; no sound card, no GPU; the speech is not heard)" % name, "output": run_row(name, py, spec)})
    return items
def tally(items):
    out = {}
    for i in items:
        o = i["output"]
        if isinstance(o, dict) and "results" in o:
            c = {"statements": 0, "matched the book": 0, "ran without an exception": 0, "raised": 0, "not executed": 0}
            for l in o["results"]:
                for s in l["statements"]:
                    r = s["as printed"]; c["statements"] += 1
                    if r.get("not executed"): c["not executed"] += 1; continue
                    c["raised"] += bool(r.get("raised")); c["ran without an exception"] += not r.get("raised"); c["matched the book"] += bool(r.get("matches the book"))
            out[i["what"].split(",")[1].split(" (")[0].strip()] = c
    return out
def digest(it):
    t = json.dumps(it, sort_keys=True, ensure_ascii=False)
    for a, b in ((r"0x[0-9a-f]{6,}", "0xADDR"), (r'"seconds": [0-9.]+', '"seconds": T'), (r"/tmp/\w+", "/tmp/X")): t = re.sub(a, b, t)
    return t
if __name__ == "__main__":
    if MODE == "write":
        items = record()
        json.dump({"_version": __version__, "_note": "Recorded by sen0414_ch24_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter and package set named in the item, with the real eSpeak NG 1.51 and the real Whisper models on the CPU of a machine with no sound card (the speech was NOT heard) in the zone Europe/Istanbul. The chapter page was fetched and its sha256 equals the chapterDigest of the book's own chapter ontology. Seconds are what the statement took on that run. Listings 11 and 12 download from YouTube and were NOT EXECUTED against YouTube; listing 12 was run with a public-domain reading on the Internet Archive instead.",
                   "python": "3.14.6 (LATEST, BARE, NOFFMPEG) and 3.12.3 (PINS)", "tally": tally(items), "items": items}, open(REC, "w"), indent=1, ensure_ascii=False)
        print("recorded", len(items), "items ->", REC); print(json.dumps(tally(items), indent=1))
    else:
        old = json.load(open(REC))["items"]; new = record(); bad = [i for i, (a, b) in enumerate(zip(old, new)) if digest(a["output"]) != digest(b["output"])]
        print("items checked:", len(new), "differences:", bad); sys.exit(1 if bad else 0)
