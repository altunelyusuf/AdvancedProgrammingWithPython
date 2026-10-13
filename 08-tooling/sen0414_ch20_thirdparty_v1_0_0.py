#!/usr/bin/env python3
"""Chapter 20 (Sending Email, Texts, and Push Notifications): runs the chapter's own listings, whole and as printed, under the given interpreter, and writes or
checks their recorded output.
What is fetched at run time and kept in a cache directory (CH20_CACHE, default the system temp directory): the chapter page
(https://automatetheboringstuff.com/3e/chapter20.html; its sha256 is compared with the chapterDigest of the book's own chapter ontology, 584483b8...9967).
Nothing is stored in the repository.
Three environments, all Python 3.14.6 installed with uv, are named by environment variables:
  LATEST  the newest releases on 2026-10-13: ezgmail 2026.4.28 (with google-api-python-client 2.201.0 and oauth2client 4.1.3) and requests 2.34.2
  PINS    the version Appendix A of the book pins for the package of this chapter it pins: requests 2.32.3 (ezgmail is listed without a version, so it is the newest)
  BARE    no package at all, to see what a reader gets who has installed nothing
The environments are named by CH20_LATEST, CH20_PINS and CH20_BARE (paths of their python), defaults /home/claude/venv314_ch20_latest/bin/python,
/home/claude/venv314_ch20_pins/bin/python and /home/claude/venv314_ch20_bare/bin/python.
What the replay does, and what it cannot do. Every statement of the 15 listings is run in the order of the book, as printed (a line break the typesetting put inside
a string stays), and the output is compared with the book's printed output with all white space removed. Three kinds of stand-in are used, and each is named in the record:
  (a) ezgmail with no credentials: what a reader gets on a machine where the Google Cloud steps were not done;
  (b) the ezgmail library itself on top of a stand-in for Google's server: the Gmail API client is built from the library's own discovery document and its HTTP layer is
      replaced by a function that returns API-shaped replies WRITTEN BY THIS STUDY (a mailbox of the book's examples); no Google account, no network;
  (c) requests with the one address https://ntfy.sh redirected to a recorder on 127.0.0.1 that logs what it receives and answers with a status and a text; for the poll it
      answers the text the book prints. That is not ntfy and says nothing about what ntfy.sh does; ntfy.sh was only asked, by GET, in sen0414_ch20_live_v1_0_0.py.
Nothing is sent to anyone. Not executed: a real Google account, the real Gmail API, a phone, ntfy.sh with a POST, qBittorrent, Windows.
Time zone: the machine runs in Europe/Istanbul (UTC+03:00); the replay of listings 5 to 10 is run in America/Los_Angeles, the zone the author's Gmail dates are read in.
Usage: sen0414_ch20_thirdparty_v1_0_0.py write|check [python]   (python defaults to the LATEST environment)
Record: 08-tooling/ch20-page/third_party_record_v1_0_0.json"""
__version__ = "1.0.0"
import json, os, re, subprocess, sys, tempfile, hashlib, html, urllib.request
MODE = sys.argv[1] if len(sys.argv) > 1 else "check"
LATEST = os.environ.get("CH20_LATEST", "/home/claude/venv314_ch20_latest/bin/python")
PINS = os.environ.get("CH20_PINS", "/home/claude/venv314_ch20_pins/bin/python")
BARE = os.environ.get("CH20_BARE", "/home/claude/venv314_ch20_bare/bin/python")
PY = sys.argv[2] if len(sys.argv) > 2 else LATEST
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(REPO, "08-tooling", "ch20-page", "third_party_record_v1_0_0.json")
CACHE = os.environ.get("CH20_CACHE") or tempfile.gettempdir()
DIGEST = "584483b8c1b41f45076a8a64d97c6afd680904246fc605b21d0f405724a09967"
def chapter():
    p = os.path.join(CACHE, "ch20_chapter.html")
    if not os.path.exists(p):
        open(p + ".part", "wb").write(urllib.request.urlopen(urllib.request.Request("https://automatetheboringstuff.com/3e/chapter20.html", headers={"User-Agent": "SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)"}), timeout=120).read()); os.replace(p + ".part", p)
    b = open(p, "rb").read(); assert hashlib.sha256(b).hexdigest() == DIGEST, "the chapter page differs from the one the study recorded"
    return b.decode("utf-8")
def pres():
    return [html.unescape(re.sub(r"<[^>]+>", "", p)) for p in re.findall(r"<pre[^>]*>(.*?)</pre>", chapter(), re.S)]

# The statements of each listing as the book prints them: (source as printed, source with the typesetter's line break removed or None, output as printed)
BOOK_POLL = ('{"id":"1jnHKeFNqwnS","time":1797823340,"expires":1797866540,"event":"message","topic":"AlSweigartZPgxBQ42","message":"Hello, world!"}\n'
             '{"id":"wZ22cjyKXw1F","time":1797823712,"expires":1797866912,"event":"message","topic":"AlSweigartZPgxBQ42","title":"Important: Read this!","message":"The rent is too high!","priority":5,"tags":["warning","neutral_face"]}\n')
LISTINGS = [
 (1, "ezgmail.init()", [("import ezgmail", None, ""), ("ezgmail.init()", None, "")]),
 (2, "ezgmail.send() with three arguments", [("import ezgmail", None, ""), ("ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email')", None, "")]),
 (3, "ezgmail.send() with a list of attachments (the book breaks the line after a comma)", [("ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email',\n['attachment1.jpg', 'attachment2.mp3'])", None, "")]),
 (4, "ezgmail.send() with cc and bcc (the book breaks the line inside a string)", [("import ezgmail", None, ""), ("ezgmail.send('recipient@example.com', 'Subject line', 'Body of the \nemail', cc='friend@example.com', bcc='otherfriend@example.com,\nsomeoneelse@example.com')", "ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email', cc='friend@example.com', bcc='otherfriend@example.com,someoneelse@example.com')", "")]),
 (5, "ezgmail.EMAIL_ADDRESS", [("import ezgmail", None, ""), ("ezgmail.EMAIL_ADDRESS", None, "'example@gmail.com'")]),
 (6, "unread() and summary()", [("import ezgmail", None, ""), ("unread_threads = ezgmail.unread()  # List of GmailThread objects", None, ""), ("ezgmail.summary(unread_threads)", None, "Al, Jon - Do you want to watch RoboCop this weekend? - Dec 09\nJon - Thanks for stopping me from buying Bitcoin. - Dec 09")]),
 (7, "threads and messages", [("len(unread_threads)", None, "2"), ("str(unread_threads[0])", None, "\"<GmailThread len=2 snippet= Do you want to watch RoboCop this weekend?'>\""), ("len(unread_threads[0].messages)", None, "2"),
    ("str(unread_threads[0].messages[0])", None, "\"<GmailMessage from='Al Sweigart <al@inventwithpython.com>' to='Jon Doe\n<example@gmail.com>' timestamp=datetime.datetime(2026, 12, 9, 13, 28, 48)\nsubject='RoboCop' snippet='Do you want to watch RoboCop this weekend?'>\""),
    ("unread_threads[0].messages[0].subject", None, "'RoboCop'"), ("unread_threads[0].messages[0].body", None, "'Do you want to watch RoboCop this weekend?\\r\\n'"), ("unread_threads[0].messages[0].timestamp", None, "datetime.datetime(2026, 12, 9, 13, 28, 48)"),
    ("unread_threads[0].messages[0].sender", None, "'Al Sweigart <al@inventwithpython.com>'"), ("unread_threads[0].messages[0].recipient", None, "'Jon Doe <example@gmail.com>'")]),
 (8, "recent()", [("recent_threads = ezgmail.recent()", None, ""), ("len(recent_threads)", None, "25"), ("recent_threads = ezgmail.recent(maxResults=100)", None, ""), ("len(recent_threads)", None, "46")]),
 (9, "search()", [("result_threads = ezgmail.search('RoboCop')", None, ""), ("len(result_threads)", None, "1"), ("ezgmail.summary(result_threads)", None, "Al, Jon - Do you want to watch RoboCop this weekend? - Dec 09")]),
 (10, "attachments", [("import ezgmail", None, ""), ("threads = ezgmail.search('vacation photos')", None, ""), ("threads[0].messages[0].attachments", None, "['tulips.jpg', 'canal.jpg', 'bicycles.jpg']"), ("threads[0].messages[0].downloadAttachment('tulips.jpg')", None, ""),
    ("threads[0].messages[0].downloadAllAttachments(downloadFolder='vacation2026')", None, "['tulips.jpg', 'canal.jpg', 'bicycles.jpg']")]),
 (11, "requests.post() of a plain text", [("import requests", None, ""), ("requests.post('https://ntfy.sh/AlSweigartZPgxBQ42', 'Hello, world!')", None, "<Response [200]>")]),
 (12, "requests.post() with headers (the book breaks the line inside the call)", [("import requests", None, ""), ("requests.post('https://ntfy.sh/AlSweigartZPgxBQ42', 'The rent is too high!', \nheaders={'Title':'Important: Read this!', 'Tags': 'warning,neutral_face', 'Priority':'5'})", None, "<Response [200]>")]),
 (13, "requests.get() of the poll URL", [("import requests", None, ""), ("resp = requests.get('https://ntfy.sh/AlSweigartZPgxBQ42/json?poll=1')", None, ""), ("resp.text", None, repr(BOOK_POLL))]),
 (14, "parsing the JSON lines", [("import json", None, ""), ("notifications = []", None, ""), ("for json_text in resp.text.splitlines():\n    notifications.append(json.loads(json_text))\n", None, ""), ("notifications[0]['message']", None, "'Hello, world!'"), ("notifications[1]['message']", None, "'The rent is too high!'")]),
 (15, "subprocess.Popen() of qBittorrent (the book breaks the line inside a string and does not import subprocess; chapter 19 does)", [("subprocess.Popen(['C:\\\\Program Files (x86)\\\\qBittorrent\\\\\nqbittorrent.exe', 'shakespeare_complete_works.torrent'])", "subprocess.Popen(['C:\\\\Program Files (x86)\\\\qBittorrent\\\\qbittorrent.exe', 'shakespeare_complete_works.torrent'])", ""),
    ("import subprocess", None, ""), ("subprocess.Popen(['C:\\\\Program Files (x86)\\\\qBittorrent\\\\qbittorrent.exe', 'shakespeare_complete_works.torrent'])", None, "")]),
]
SESSIONS = {"plain": [("S1", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), ("S2", [11, 12, 13, 14]), ("S3", [15])], "standin": [("S1", [2, 3, 4, 5, 6, 7, 8, 9, 10]), ("S2", [11, 12, 13, 14]), ("S3", [15])]}

HARNESS = r'''import sys, os, io, json, re, base64, tempfile, threading, http.server, datetime, time, contextlib, traceback, importlib.metadata as md
LISTINGS = json.loads(os.environ['LISTINGS_JSON']); MODE = os.environ['REPLAY_MODE']; GROUP = os.environ['REPLAY_GROUP']
BOOK_POLL = os.environ['BOOK_POLL']
os.chdir(tempfile.mkdtemp())
for f in ('attachment1.jpg', 'attachment2.mp3'): open(f, 'wb').write(b'x')
def norm(t): return re.sub(r'\s+', '', t)
# (c) the recorder that stands for https://ntfy.sh
log = []
class Hd(http.server.BaseHTTPRequestHandler):
    def _do(s):
        n = int(s.headers.get('Content-Length') or 0); body = s.rfile.read(n) if n else b''
        log.append((s.command, s.path, s.headers.get('Title'), s.headers.get('Tags'), s.headers.get('Priority'), body.decode('utf-8', 'replace')))
        t = BOOK_POLL.encode() if s.command == 'GET' else b'{}'
        s.send_response(200); s.send_header('Content-Length', str(len(t))); s.end_headers(); s.wfile.write(t)
    do_GET = do_POST = _do
    def log_message(s, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Hd); threading.Thread(target=srv.serve_forever, daemon=True).start()
try:
    import requests.adapters
    _send = requests.adapters.HTTPAdapter.send
    def send(self, request, **k):
        request.url = request.url.replace('https://ntfy.sh', 'http://127.0.0.1:%d' % srv.server_address[1]); return _send(self, request, **k)
    requests.adapters.HTTPAdapter.send = send
except ImportError: pass
# (b) ezgmail on a stand-in for Google's server
def b64(t): return base64.urlsafe_b64encode(t if isinstance(t, bytes) else t.encode()).decode()
def standin():
    import httplib2, ezgmail
    from googleapiclient.discovery import build
    from zoneinfo import ZoneInfo
    ms = int(datetime.datetime(2026, 12, 9, 13, 28, 48, tzinfo=ZoneInfo('America/Los_Angeles')).timestamp()) * 1000
    def msg(i, tid, frm, to, subj, text, parts=None):
        h = [{'name': 'From', 'value': frm}, {'name': 'To', 'value': to}, {'name': 'Subject', 'value': subj}, {'name': 'Content-Type', 'value': 'text/plain; charset=\"UTF-8\"'}]
        pl = {'headers': h, 'mimeType': 'text/plain', 'body': {'size': len(text), 'data': b64(text)}} if parts is None else {'headers': h, 'mimeType': 'multipart/mixed', 'body': {'size': 0}, 'parts': parts}
        return {'id': i, 'threadId': tid, 'snippet': text.strip()[:60], 'historyId': '1', 'internalDate': str(ms), 'payload': pl}
    AL, JON = 'Al Sweigart <al@inventwithpython.com>', 'Jon Doe <example@gmail.com>'
    t1 = {'id': 'T1', 'messages': [msg('M1', 'T1', AL, JON, 'RoboCop', 'Do you want to watch RoboCop this weekend?\r\n'), msg('M2', 'T1', JON, AL, 'Re: RoboCop', 'Yes.\r\n')]}
    t2 = {'id': 'T2', 'messages': [msg('M3', 'T2', JON, AL, 'Bitcoin', 'Thanks for stopping me from buying Bitcoin.\r\n')]}
    th = lambda t: {'id': t['id'], 'snippet': t['messages'][0]['snippet'], 'historyId': '1'}
    att = [{'mimeType': 'text/plain', 'filename': '', 'headers': [], 'body': {'size': 6, 'data': b64('Photos')}}] + [{'mimeType': 'image/jpeg', 'filename': n, 'headers': [], 'body': {'attachmentId': 'A' + str(k), 'size': 4}} for k, n in enumerate(('tulips.jpg', 'canal.jpg', 'bicycles.jpg'))]
    t3 = {'id': 'T3', 'messages': [msg('M4', 'T3', AL, JON, 'vacation photos', 'Photos', att)]}
    n25 = {'threads': [{'id': 'X%d' % i, 'snippet': 's', 'historyId': '1'} for i in range(25)]}; n46 = {'threads': [{'id': 'X%d' % i, 'snippet': 's', 'historyId': '1'} for i in range(46)]}
    replies = [{}, {}, {}, {'threads': [th(t1), th(t2)]}, t1, t2, n25, n46, {'threads': [th(t1)]}, t1, {'threads': [th(t3)]}, t3, {'data': b64(b'AAAA'), 'size': 4}, {'data': b64(b'AAAA'), 'size': 4}, {'data': b64(b'BBBB'), 'size': 4}, {'data': b64(b'CCCC'), 'size': 4}]
    class Rec(httplib2.Http):
        def __init__(s): super().__init__(); s.log = []
        def request(s, uri, method='GET', body=None, headers=None, **k):
            s.log.append((method, uri.split('/gmail/v1/')[-1].split('?')[0]))
            r = replies.pop(0) if replies else {}
            return httplib2.Response({'status': '200', 'content-type': 'application/json'}), json.dumps(r).encode()
    h = Rec(); ezgmail.SERVICE_GMAIL = build('gmail', 'v1', http=h); ezgmail.EMAIL_ADDRESS = 'example@gmail.com'; return h
http_log = None
if MODE == 'standin' and GROUP == 'S1':
    try: http_log = standin()
    except ImportError: pass
ns = {}
res = []
CWD = os.getcwd()
def clean(t): return t.replace(CWD, 'DIR')
for n, title, stmts in LISTINGS:
    out = []
    for printed, repaired, expected in stmts:
        row = {'source': printed}
        for label, src in (('as printed', printed), ('repaired', repaired)):
            if src is None: continue
            buf = io.StringIO(); shown = []
            old = sys.displayhook
            sys.displayhook = lambda v: (shown.append(repr(v)) if v is not None else None)
            try:
                with contextlib.redirect_stdout(buf):
                    code = compile(src.rstrip('\n') + '\n', '<listing %d>' % n, 'single')
                    exec(code, ns)
                got = (buf.getvalue() + ''.join(s + '\n' for s in shown)).strip(); row[label] = {'printed': clean(got)[:400], 'raised': None, 'matches the book': norm(got) == norm(expected)}
            except BaseException as e:
                row[label] = {'printed': (buf.getvalue() + ''.join(s + '\n' for s in shown)).strip()[:200], 'raised': clean('%s: %s' % (type(e).__name__, str(e).splitlines()[0][:150] if str(e) else '')), 'matches the book': False}
            finally: sys.displayhook = old
            if label == 'as printed' and row[label]['raised'] is None: break
        row['book prints'] = expected[:300]; out.append(row)
    res.append({'listing': n, 'what': title, 'statements': out})
extra = {'requests seen by the recorder': [(a, b, c, d, e, f[:60]) for a, b, c, d, e, f in log]}
if http_log is not None: extra['API calls made through the stand-in'] = http_log.log
print(json.dumps({'results': res, **extra}, default=repr))
'''
ENVINFO = r'''import sys, os, time, platform, importlib.metadata as md
out = {'python': sys.version.split()[0], 'zone of the process': time.tzname, 'platform': platform.platform()}
for n in ('ezgmail', 'requests', 'urllib3', 'google-api-python-client', 'oauth2client', 'httplib2', 'google-auth', 'aiosmtpd', 'imapclient'):
    try: out[n] = md.version(n)
    except md.PackageNotFoundError: out[n] = None
print(__import__('json').dumps(out))'''
def sh(py, code=None, env=None, args=None):
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run([py, "-c", code] if code else [py] + (args or []), capture_output=True, text=True, env=e, timeout=300)
    return r.stdout.strip(), r.stderr.strip(), r.returncode
def replay(py, mode, tz):
    out = {}
    L = {n: (n, t, s) for n, t, s in LISTINGS}
    for g, nums in SESSIONS[mode]:
        so, se, rc = sh(py, HARNESS, {"LISTINGS_JSON": json.dumps([L[n] for n in nums]), "REPLAY_MODE": mode, "REPLAY_GROUP": g, "BOOK_POLL": BOOK_POLL, "TZ": tz, "PYTHONDONTWRITEBYTECODE": "1"})
        if rc: out[g] = {"harness failed": se[-400:]}
        else: out[g] = json.loads(so.splitlines()[-1])
    return out
def summarise(rep):
    rows = []
    for g, r in rep.items():
        if "results" not in r: rows.append([g, r]); continue
        for l in r["results"]:
            for s in l["statements"]:
                for k in ("as printed", "repaired"):
                    if k in s: rows.append([l["listing"], s["source"][:90], k, s[k]["matches the book"], s[k]["raised"]])
    return rows
def record():
    items = []
    chapter()
    items.append({"what": "The environments: interpreter, packages and their versions in the three environments of the study, the zone of the process", "output": {n: json.loads(sh(p, ENVINFO)[0]) for n, p in (("LATEST", LATEST), ("PINS", PINS), ("BARE", BARE))}})
    items.append({"what": "The chapter's listings, 15 in all, whose statements number %d, found on the page (a count, not a replay)" % sum(len(s) for _, _, s in LISTINGS), "output": [len(pres()), sum(len(s) for _, _, s in LISTINGS)]})
    for name, p in (("LATEST", LATEST), ("PINS", PINS), ("BARE", BARE)):
        items.append({"what": "Replay as printed with NO credentials and the recorder in place of https://ntfy.sh, environment %s (a reader who followed Appendix A and the chapter and has not done the Google Cloud steps)" % name, "output": replay(p, "plain", "America/Los_Angeles")})
    for name, p in (("LATEST", LATEST), ("PINS", PINS)):
        items.append({"what": "Replay as printed with ezgmail on the stand-in for Google's server (replies written by this study) and the recorder in place of https://ntfy.sh, environment %s, process zone America/Los_Angeles" % name, "output": replay(p, "standin", "America/Los_Angeles")})
    items.append({"what": "The same replay on the stand-in in the zone of the machine, Europe/Istanbul, to show that the dates of listings 6, 7 and 9 and the timestamp of listing 7 depend on the zone of the reader, environment LATEST", "output": replay(LATEST, "standin", "Europe/Istanbul")})
    return items
def digest(it):
    t = json.dumps(it, sort_keys=True)
    return t
if MODE == "write":
    items = record()
    json.dump({"_version": __version__, "_note": "Recorded by sen0414_ch20_thirdparty_v1_0_0.py write; every output was printed by the program beside it under the interpreter named in the item, on a machine in the zone Europe/Istanbul. The chapter page is fetched at run time and not kept in the repository. The ezgmail listings ran either with no credentials or on a stand-in for Google's server whose replies were written by this study; the ntfy listings ran against a recorder on 127.0.0.1 that is not ntfy. Nothing was sent to anyone.", "python": "3.14.6 ezgmail 2026.4.28 requests 2.34.2 (LATEST), requests 2.32.3 (PINS)", "items": items}, open(REC, "w"), indent=1, ensure_ascii=False)
    n = sum(len(summarise(i["output"])) for i in items if isinstance(i["output"], dict) and "S1" in i["output"])
    print("recorded", len(items), "items,", n, "statement runs ->", REC)
else:
    old = json.load(open(REC))["items"]; new = record(); bad = [i for i, (a, b) in enumerate(zip(old, new)) if digest(a["output"]) != digest(b["output"])]
    print("items checked:", len(new), "differences:", bad); sys.exit(1 if bad else 0)
