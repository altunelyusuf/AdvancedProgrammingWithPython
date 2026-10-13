"""Chapter 20 deck examples: every console session, whole program (or excerpt), chart and table the lecture deck shows. Nothing here
carries a result; examples_run_v1_0_0.py runs it all under the interpreter given (the uv Python 3.14.6 of the chapter 20 research
environment /home/claude/venv314_ch20_latest: ezgmail 2026.4.28, requests 2.34.2, aiosmtpd 1.4.6, cryptography, google-api-python-client 2.201.0,
oauth2client 4.1.3; email, smtplib, imaplib, ssl, json, hmac, subprocess, html.parser and zoneinfo are the standard library) and records the
results. A console group is one session: its rows run in order in one namespace (the deck check re-runs them per slide, one namespace per slide).
Every console row uses the standard library only, touches neither the network nor the file system, and reads no clock, so each can be typed into a
Python in a browser and prints the same text on any day.

NOTHING HERE REACHES A REAL SERVICE. No Gmail account, Gmail server, phone number, carrier, Twilio account or ntfy server was used, and nothing was sent to
a person. Programs come from sen0414_ch20_corpus_base_v1_0_0.py, all twelve, run and recorded under their own names (the corpus lines are often wider than a
slide can show without wrapping, so the slides show deck-written copies, 'Cut' programs, of the same stand-ins and the same behaviours; every Cut is
run, recorded and re-run like the originals). KIND says what a program's output depends on, so that honesty_check can require the matching words on the
slide that shows it:
  standin   the output comes from a LOCAL STAND-IN on 127.0.0.1 or in memory: SMTP (aiosmtpd with a self-signed certificate), Gmail (the real ezgmail
            library on a replacement of the Google client's HTTP layer, with replies written by this study), ntfy (a recorder that is not ntfy), the
            mailbox (a list in memory), the browser (webbrowser.open replaced by a recorder) or sample data (forecast periods made up in the shape of api.weather.gov);
  none      the output depends on no stand-in (pure functions of the standard library, or of a library that makes a file).
STANDKEY holds, for each stand-in program, the words that the slide showing it must say."""
__version__ = "1.0.0"
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("base20", os.path.join(HERE, "..", "sen0414_ch20_corpus_base_v1_0_0.py"))
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)
_HEAD, _MSG, _SMTP, _GM, _NTFY = B.HEAD, B.MSG, B.SMTP, B.GM, B.NTFY

CONSOLES = {
    "title": ["import platform, importlib.metadata as m", "platform.python_version()", "m.version('ezgmail')", "m.version('requests')"],
    "address": ["from email.utils import parseaddr, formataddr", "parseaddr('Al Sweigart <al@inventwithpython.com>')",
                "'al@inventwithpython.com'.partition('@')", "formataddr(('Jon Doe', 'jon@example.org'))",
                "parseaddr('real@example.com, evil@example.net')", "parseaddr('real@example.com, evil@example.net', strict=False)"],
    "imap": ["import imaplib, smtplib", "smtplib.SMTP_PORT, smtplib.SMTP_SSL_PORT", "imaplib.IMAP4_PORT, imaplib.IMAP4_SSL_PORT",
             "hasattr(imaplib.IMAP4, 'idle')", "imaplib.Commands['IDLE']", "imaplib.ParseFlags(b'1 (FLAGS (\\\\Seen))')",
             "from datetime import datetime as dt, timezone as tz", "d = dt(2026, 12, 9, 13, 28, 48, tzinfo=tz.utc)", "imaplib.Time2Internaldate(d)"],
    "shell": ["import subprocess as sp", "sp.run('echo a; echo PWNED', shell=True, capture_output=True).stdout",
              "sp.run(['echo', 'a; echo PWNED'], capture_output=True).stdout"],
    "jsonlines": ["import json", "t = '{\"id\": \"a\"}\\n{\"id\": \"b\"}\\n'", "json.loads(t)", "[json.loads(x)['id'] for x in t.splitlines()]",
                  "json.loads('')"],
}

# ---- programs written for the deck ---------------------------------------------------------------------------------------------
# helper block for the Gmail stand-in programs: a message in the shape of the API's answer, written by this study
_GH = r'''BODY = {'mimeType': 'text/plain', 'filename': '', 'headers': [], 'body': {'size': 1, 'data': b64('x')}}
def part(name, aid='A1'): return {'mimeType': 'text/plain', 'filename': name, 'headers': [], 'body': {'attachmentId': aid, 'size': 4}}
def one(subj='RoboCop', ms=1797000528000, parts=None):
    return api_msg('M1', 'T1', 'Al <al@example.com>', 'Jon <jon@example.org>', subj, 'Do you want to watch RoboCop?\r\n', ms, parts)
'''

SETUP = _HEAD + _GM + r'''# ezgmail with no credentials.json: what init() says, and what a token.json holds. Made-up values; nothing leaves the machine.
d = wd()
try:
    ezgmail.init()
except ezgmail.EZGmailException as e:
    print('init():', str(e).split(' You can')[0].replace(d, '.'))
print('LOGGED_IN', ezgmail.LOGGED_IN, ezgmail.SCOPES)
print(inspect.getsource(ezgmail).splitlines()[-1])
from oauth2client import client, file
c = client.OAuth2Credentials('tok','id','sec','ref',None,'u','ua')
file.Storage('token.json').put(c)
t = json.load(open('token.json'))
print(len(t), 'keys, mode', oct(os.stat('token.json').st_mode)[-3:])
print('in the file:', t['refresh_token'], t['client_secret'])
'''

SEND = _HEAD + _GM + _GH + r'''# ezgmail.send() on a STAND-IN for Google's server: the real library, replies written by this study; nothing leaves the machine.
d = wd()
for n in ('a.jpg', 'b.mp3', 'setup.exe'): open(n, 'wb').write(b'0' * 9)
h = gm({}, {}, {}, {})
ezgmail.send('r@example.com', 'Subject line', 'Body of the email')
m = raw_of(h, 0)
print('POST', h.log[0][1], '| body keys', list(json.loads(h.log[0][2])))
print('headers:', [k for k in m.keys() if k in ('to', 'from', 'subject')])
ezgmail.send('r@example.com', 'S', 'B', ['a.jpg', 'b.mp3', 'setup.exe'])
print('attachments:', [a.get_filename() for a in raw_of(h, 1).iter_attachments()])
ezgmail.send('r@example.com', 'S', 'B', cc='f@example.com', bcc='o@example.com')
m = raw_of(h, 2)
print('cc:', m['cc'], '| Bcc header in the message:', m['bcc'])
'''

READ = _HEAD + _GM + _GH + r'''# The read side of ezgmail on a STAND-IN for Google's server: a thread, the zone of a timestamp, a message with no Subject header.
th = ezgmail.GmailThread({'id': 'T1', 'snippet': 'Do you want to watch?',
                          'historyId': '9'})
h = gm({'id': 'T1', 'messages': [one(), one('Re: RoboCop')]})
text = str(th)
print('requests made by str(thread):', len(h.log))
print(text)
for z in ('UTC', 'America/Chicago', 'Europe/Istanbul'):
    os.environ['TZ'] = z; time.tzset()
    print(z.ljust(16), ezgmail.GmailMessage(one()).timestamp)
nm = one()
hs = nm['payload']['headers']
nm['payload']['headers'] = [x for x in hs if x['name'] != 'Subject']
print('no Subject header:', err(lambda: ezgmail.GmailMessage(nm).subject)[0])
'''

REPLY = _HEAD + _GM + _GH + r'''# reply(), the queries of unread(), recent() and search(), and removeQuotedParts(), on a STAND-IN for Google's server.
src = ezgmail.GmailMessage(one()); h = gm({}, {}, {}, {})
src.reply('Yes, Saturday works.')
body = json.loads(h.log[0][2]); m = raw_of(h, 0)
print(list(body), body['threadId'], m['subject'], m['in-reply-to'])
print('replyAll:', src.replyAll('x'), len(h.log))
ezgmail.unread(); ezgmail.recent()
ezgmail.search('has:attachment')
for r in h.log[1:]:
    print(r[1].split('?')[1].replace('&alt=json', ''))
q1 = 'Ok.\n\nOn Sun, Jan 1, 2018 at 12:00 PM Al <a@b.c> wrote:'
q2 = 'Ok.\n\nOn Sun, 1 Jan 2018 at 12:00, Al <a@b.c> wrote:'
rq = ezgmail.removeQuotedParts
print(repr(rq(q1)), 'day-month form uncut:', rq(q2) == q2)
'''

DOWNLOAD = _HEAD + _GM + _GH + r'''# Downloading attachments on a STAND-IN for Google's server: a name with a path, and a file that already exists.
d = wd(); os.mkdir('inbox')
ps = [BODY, part('../evil.txt', 'A9')]
m = ezgmail.GmailMessage(one(parts=ps))
gm({'data': b64(b'PWNED'), 'size': 5})
print(m.downloadAllAttachments(downloadFolder='inbox'))
print(os.listdir('inbox'), sorted(os.listdir('.')))
open('tulips.jpg', 'wb').write(b'MINE')
ps = [BODY, part('tulips.jpg')]
m = ezgmail.GmailMessage(one(parts=ps))
gm({'data': b64(b'AAAA'), 'size': 4})
m.downloadAttachment('tulips.jpg')
print('tulips.jpg is now', open('tulips.jpg', 'rb').read())
print('no.jpg:', err(lambda: m.downloadAttachment('no.jpg'))[0])
'''

BUILD = _HEAD + _MSG + r'''# The standard library builds a message (EZGmail does this for you): EmailMessage, the MIME tree and the bytes that are sent.
m = mk()
raw = m.as_bytes()
smtp = m.as_bytes(policy=policy.SMTP)
print('CRLF:', raw.count(b'\r\n'), '| with policy.SMTP:', smtp.count(b'\r\n'))
print(len(m.keys()), 'headers;', m['Content-Type'], m['Content-Transfer-Encoding'])
m.add_alternative('<p>Watch <b>RoboCop</b>?</p>', subtype='html')
m.add_attachment(b'\0\1\2', maintype='application', subtype='octet-stream',
                 filename='poster.bin')
for p in m.walk():
    print(p.get_content_type())
print([a.get_filename() for a in m.iter_attachments()])
print(m.get_body(preferencelist=('html', 'plain')).get_content_type())
'''

HEADERS = _HEAD + r'''# Encoded headers, addresses and a line break in a header, with the standard library only.
from email.header import decode_header, make_header
m = EmailMessage(); m['Subject'] = 'Yedekleme bitti şğı'
print(line := m.as_bytes().decode().splitlines()[0])
print(str(make_header(decode_header(line.split(': ', 1)[1]))))
s = '"Doe, Jon" <jon@example.org>, Al Sweigart <al@example.com>'
print(eu.getaddresses([s]))
print(eu.getaddresses([s.replace('"Doe, Jon"', 'Doe, Jon')]))
two = 'real@example.com, evil@example.net'
print(eu.parseaddr(two), eu.parseaddr(two, strict=False))
bad = 'hi\r\nBcc: evil@example.net'
try: EmailMessage()['Subject'] = bad
except ValueError: print('EmailMessage: ValueError at once')
t = MIMEText('x'); t['Subject'] = bad
try: t.as_string()
except Exception as ex: print('MIMEText, when written:', type(ex).__name__)
'''

STARTTLS = _HEAD + _MSG + _SMTP + r'''# smtplib against a LOCAL STAND-IN (aiosmtpd, a self-signed certificate, 127.0.0.1), not Gmail: STARTTLS, certificate checks, AUTH after TLS.
c, box, port, cp = serve()
import atexit; atexit.register(c.stop)
ctx = ssl.create_default_context(cafile=cp)
def conn():
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo(); return s
def ehlo(s):
    return [x for x in s.ehlo()[1].decode().splitlines() if x[:2] in ('ST', 'AU')]
s = conn(); print('before:', ehlo(s))
s.starttls(context=ctx); print('after:', ehlo(s))
s.send_message(mk()); print('TLS seen:', box[0]['tls']); s.quit()
s = conn()
try: s.starttls(context=ssl.create_default_context())
except ssl.SSLCertVerificationError as e: print(e.verify_message)
s = conn(); print('no context:', s.starttls()[0])
s = conn(); s.starttls(context=ctx); s.ehlo()
print('login after:', s.login('user', 'secret')[0])
s.quit()
'''

REFUSALS = _HEAD + _MSG + _SMTP + r'''# What smtplib does when the LOCAL STAND-IN (aiosmtpd on 127.0.0.1) refuses a recipient or the password, and when nothing listens.
c, box, port, cp = serve()
import atexit; atexit.register(c.stop)
ctx = ssl.create_default_context(cafile=cp)
def conn():
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo(); return s
s = conn()
r = s.send_message(mk(to='ok@example.org, x@refused.example'))
print(r)
print('stored for', box[0]['to'])
try: s.send_message(mk(to='x@refused.example'))
except smtplib.SMTPRecipientsRefused:
    print('raised; stored:', len(box))
s.quit()
s = conn(); s.starttls(context=ctx); s.ehlo()
try: s.login('user', 'wrong')
except smtplib.SMTPAuthenticationError as e:
    print('password:', e.smtp_code)
s.close()
try: smtplib.SMTP('127.0.0.1', 1, timeout=3)
except OSError as e: print('closed port:', type(e).__name__)
'''

ENVELOPE = _HEAD + _MSG + _SMTP + r'''# The envelope is not the header, on a LOCAL STAND-IN (aiosmtpd on 127.0.0.1): Bcc is in RCPT TO and not in the text; From can be anything.
c, box, port, cp = serve()
import atexit; atexit.register(c.stop)
def parse(i):
    return email.message_from_bytes(box[i]['data'], policy=policy.default)
s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
s.send_message(mk(extra={'Cc': 'cc@x.org', 'Bcc': 'bcc@x.org'}))
h = parse(0)
print(box[0]['from'], box[0]['to'])
print('header Bcc:', h['Bcc'], '| Cc:', h['Cc'])
print('bcc@x.org in text:', b'bcc@x.org' in box[0]['data'])
s.sendmail('bounces@mallory.example', ['jon@example.org'],
           mk(frm='CEO <ceo@bank.example>').as_bytes())
h = parse(1)
print(box[1]['from'], '|', h['From'], '| login:', box[1]['auth'])
s.quit()
'''

_TABLE = r'''T = {'AT&T': ('txt.att.net', 'mms.att.net'), 'Boost Mobile': ('sms.myboostmobile.com', None), 'Cricket': ('sms.cricketwireless.net', 'mms.cricketwireless.net'), 'Google Fi': ('msg.fi.google.com', None),
     'Metro PCS': ('mymetropcs.com', None), 'Republic Wireless': ('text.republicwireless.com', None), 'Sprint': ('messaging.sprintpcs.com', 'pm.sprint.com'), 'T-Mobile': ('tmomail.net', None),
     'U.S. Cellular': ('email.uscc.net', 'mms.uscc.net'), 'Verizon': ('vtext.com', 'vzwpix.com'), 'Virgin Mobile': ('vmobl.com', 'vmpix.com'), 'Xfinity Mobile': ('vtext.com', 'mypixmessages.com')}
def addr(number, carrier, mms=False):
    sms, m = T[carrier]; return '%s@%s' % (number, (m or sms) if mms else sms)
'''
GATEWAY = _HEAD + _TABLE + r'''# Table 20-1 as a dict (typed from the chapter) and the dates of the two notices. Pure arithmetic; no message is sent.
print(len(T), 'providers; SMS', addr('2125551234', 'Verizon'))
print('MMS', addr('2125551234', 'Verizon', True))
print('Boost MMS:', addr('5555550100', 'Boost Mobile', True))
print('vtext.com:', [c for c, v in T.items() if v[0] == 'vtext.com'])
print('distinct SMS domains:', len(set(v[0] for v in T.values())))
today = D(2026, 10, 13)
print('AT&T off', (today - D(2025, 6, 17)).days, 'days before', today)
print('Verizon ends in', (D(2027, 3, 31) - today).days, 'days from', today)
'''

_GSM = r'''BASIC = '@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !"#¤%&\'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà'
EXT = '^{}\\[~]|€'
def segments(t):
    n = 0
    for ch in t:
        if ch in BASIC: n += 1
        elif ch in EXT: n += 2
        else: n = None; break
    if n is not None: return ('GSM-7', n, 1 if n <= 160 else -(-n // 153))
    u = len(t.encode('utf-16-le')) // 2; return ('UCS-2', u, 1 if u <= 70 else -(-u // 67))
'''
SEGMENTS = _HEAD + _GSM + r'''# How many characters a text holds. A GSM-7 table written for this study; no message is sent and no carrier is asked.
print('140 * 8 // 7 =', 140 * 8 // 7, '| 140 // 2 =', 140 // 2)
for t in ('Hello, world!', 'a' * 160, 'a' * 161, '{x}', 'Yedekleme tamamlandi',
          'Yedekleme tamamlandı', 'ş' * 70, 'ş' * 71):
    print(t[:20].ljust(21), str(len(t)).rjust(3), segments(t))
'''

NTFYPUB = _HEAD + _NTFY + r'''# Publishing with requests to a LOCAL RECORDER on 127.0.0.1 (it logs what requests sends; it is not ntfy and says nothing about ntfy.sh).
srv, log, base = recorder(200, '{}')
r = requests.post(base + '/AlSweigartZPgxBQ42', 'Hello, world!')
q = log[0]; h = q['headers']
print(r.status_code, q['method'], q['path'], q['body'])
print('length', h['Content-Length'], 'type', h.get('Content-Type'))
hd = {'Title': 'Important: Read this!',
      'Tags': 'warning,neutral_face', 'Priority': '5'}
requests.post(base + '/t', 'The rent is too high!', headers=hd)
for k in hd:
    print(k.ljust(9), log[1]['headers'][k])
srv.shutdown()
'''

NTFYHDR = _HEAD + _NTFY + r'''# Bytes and errors with requests against a LOCAL RECORDER on 127.0.0.1 (not ntfy): a header that is not latin-1, a body with a dotless i, a 429.
srv, log, base = recorder(200, '{}')
for hd in ({'Priority': 5}, {'Title': 'Yedekleme tamamlandı'}):
    try: requests.post(base + '/t', 'x', headers=hd)
    except Exception as e: print(hd, '->', type(e).__name__)
t = 'Yedekleme tamamlandı'
requests.post(base + '/t', t); b = log[-1]
print('wire:', b['body'], '| bytes', b['headers']['Content-Length'], '| chars', len(t))
srv, log, base = recorder(429, '{"code":42908,"http":429,"error":"limit reached"}')
r = requests.post(base + '/t', 'Hello, world!')
print('refused post: ok', r.ok, '| nothing raised')
try: r.raise_for_status()
except requests.HTTPError as e: print('raise_for_status ->', type(e).__name__)
'''

_TXT = r'''TXT = ('{"id":"1jnHKeFNqwnS","time":1797823340,"expires":1797866540,"event":"message","topic":"AlSweigartZPgxBQ42","message":"Hello, world!"}\n'
       '{"id":"wZ22cjyKXw1F","time":1797823712,"expires":1797866912,"event":"message","topic":"AlSweigartZPgxBQ42","title":"Important: Read this!","message":"The rent is too high!","priority":5,"tags":["warning","neutral_face"]}\n')
'''
NTFYPOLL = _HEAD + _NTFY + _TXT + r'''# Reading a poll answer. The server is a LOCAL RECORDER on 127.0.0.1 that answers the text the book prints (not ntfy).
srv, log, base = recorder(200, TXT)
resp = requests.get(base + '/AlSweigartZPgxBQ42/json?poll=1')
try: json.loads(resp.text)
except json.JSONDecodeError as e: print('whole text:', e.msg)
n = [json.loads(x) for x in resp.text.splitlines()]
print(len(n), [x['message'] for x in n])
print(sorted(set(n[1]) - set(n[0])))
for z in ('America/Chicago', 'UTC'):
    print(z.ljust(16), DT.fromtimestamp(n[1]['time'], ZoneInfo(z)))
srv.shutdown()
'''

SECRECY = _HEAD + r'''# The topic name is the only secret, and the limits in bytes. Arithmetic only; nothing is published.
book = 'AlSweigartZPgxBQ42'; rnd = book[len('AlSweigart'):]
bits = round(len(rnd) * math.log2(62), 1)
print(rnd, len(rnd), 'chars of 62 ->', bits, 'bits')
t = secrets.token_urlsafe(16)
print('token_urlsafe(16):', len(t), 'characters, 128 bits')
print('the topic is in the URL path: https://ntfy.sh/' + book)
ok, tr = 'a' * 4096, 'ı' * 2049
print(len(ok.encode()), 'bytes for 4096 characters')
print(len(tr), 'dotless i:', len(tr.encode()), 'bytes, over the limit')
print('250 messages of 4096 bytes =', 250 * 4096, 'bytes a day')
'''

UNSUB = _HEAD + r'''# Auto Unsubscriber: links whose text says unsubscribe, and the List-Unsubscribe header. webbrowser.open is replaced by a recorder.
import webbrowser
from html.parser import HTMLParser
HTML = ('<p><a href="https://example.com/u?id=1">Unsubscribe</a> | <a href="https://example.com/p">Preferences</a> | '
        '<a href="https://example.com/x"><img alt="unsubscribe"></a> <a href="https://example.com/u2">click here to opt out</a></p>')
class P(HTMLParser):
    def __init__(s): super().__init__(); s.cur = None; s.found = []; s.txt = ''
    def handle_starttag(s, tag, attrs):
        if tag == 'a': s.cur = dict(attrs).get('href'); s.txt = ''
    def handle_data(s, d):
        if s.cur: s.txt += d
    def handle_endtag(s, tag):
        if tag == 'a':
            if s.cur and 'unsubscribe' in s.txt.lower(): s.found.append(s.cur)
            s.cur = None
p = P(); p.feed(HTML)
print('links whose text says unsubscribe:', p.found)
m = EmailMessage()
a = '<mailto:unsub@example.com?subject=unsubscribe>'
m['List-Unsubscribe'] = a + ', <https://example.com/u?id=1>'
lu = [x.strip('<>') for x in m['List-Unsubscribe'].split(', ')]
print(f'List-Unsubscribe gives {len(lu)} addresses:', *lu, sep='\n  ')
opened = []
webbrowser.open = lambda u: opened.append(u) or True
for u in p.found: webbrowser.open(u)
print('the recorder was asked to open', opened)
'''

UMBRELLA = _HEAD + r'''# Umbrella Reminder: searching the text for 'rain' against comparing the chance of precipitation. SAMPLE periods in the shape of api.weather.gov, no network.
P = [{'shortForecast': 'Chance Showers And Thunderstorms', 'detailedForecast': 'A chance of showers and thunderstorms. Sunny.',
      'probabilityOfPrecipitation': {'unitCode': 'wmoUnit:percent', 'value': 60}},
     {'shortForecast': 'Mostly Cloudy', 'detailedForecast': 'Mostly cloudy, with a low around 50.',
      'probabilityOfPrecipitation': {'unitCode': 'wmoUnit:percent', 'value': None}}]
words = lambda p: (p['shortForecast'] + p['detailedForecast']).lower()
chance = lambda p: p['probabilityOfPrecipitation']['value']
print('text has rain:', ['rain' in words(p) for p in P])
print('limit 40:', [(chance(p) or 0) >= 40 for p in P])
print('chances:', [chance(p) for p in P])
'''

CONTROL = _HEAD + r'''# Email-Based Computer Control. The MAILBOX IS A LIST IN MEMORY (the IMAP version ran against dovecot, recorded). Only an allow-list is run.
inbox = [('me@a.org', 'correct horse:noop'), ('x@b.net', 'guess:noop'),
         ('me@a.org', 'correct horse:rm')]
SECRET = 'correct horse'
ALLOW = {'noop': [sys.executable, '-c', 'pass']}
def handle(frm, body):
    pw, _, cmd = body.partition(':')
    if not hmac.compare_digest(pw.encode(), SECRET.encode()):
        return (frm, 'bad password')
    if cmd not in ALLOW:
        return (frm, 'refused ' + cmd)
    return (frm, cmd, subprocess.Popen(ALLOW[cmd]).wait())
for m in inbox: print(handle(*m))
'''

PROGRAMS = dict(B.PROGRAMS)
_CUTS = (("setupCut", SETUP), ("sendCut", SEND), ("readCut", READ), ("replyCut", REPLY), ("downloadCut", DOWNLOAD), ("buildCut", BUILD),
         ("headersCut", HEADERS), ("starttlsCut", STARTTLS), ("refusalsCut", REFUSALS), ("envelopeCut", ENVELOPE), ("gatewayCut", GATEWAY),
         ("segmentsCut", SEGMENTS), ("ntfyPubCut", NTFYPUB), ("ntfyHdrCut", NTFYHDR), ("ntfyPollCut", NTFYPOLL), ("secrecyCut", SECRECY),
         ("unsubCut", UNSUB), ("umbrellaCut", UMBRELLA), ("controlCut", CONTROL))
for _n, _c in _CUTS:
    PROGRAMS[_n + "_v1_0_0.py"] = (_c, (), False)
SUBSET = {}
EQUIV = {}
KIND = {n: "none" for n in PROGRAMS}
STANDKEY = {}
_GMAIL = ("Stand-in for Gmail",)
_SMTPK = ("Stand-in for an SMTP server",)
_NTFYK = ("Stand-in for ntfy",)
for _n in ("sendCut", "readCut", "replyCut", "downloadCut", "ezgmailSendWithStandIn", "ezgmailReadWithStandIn"):
    KIND[_n + "_v1_0_0.py"] = "standin"; STANDKEY[_n + "_v1_0_0.py"] = _GMAIL
for _n in ("starttlsCut", "refusalsCut", "envelopeCut", "smtpLocalStarttls", "smtpErrorsLocal", "envelopeVersusHeaders"):
    KIND[_n + "_v1_0_0.py"] = "standin"; STANDKEY[_n + "_v1_0_0.py"] = _SMTPK
for _n in ("ntfyPubCut", "ntfyHdrCut", "ntfyPollCut", "ntfyPublishRecorder", "ntfyPollParse"):
    KIND[_n + "_v1_0_0.py"] = "standin"; STANDKEY[_n + "_v1_0_0.py"] = _NTFYK
for _n in ("controlCut", "emailControlLoop"):
    KIND[_n + "_v1_0_0.py"] = "standin"; STANDKEY[_n + "_v1_0_0.py"] = ("Stand-in mailbox",)
for _n in ("unsubCut", "unsubscribeFinder"):
    KIND[_n + "_v1_0_0.py"] = "standin"; STANDKEY[_n + "_v1_0_0.py"] = ("Stand-in for the browser",)
KIND["umbrellaCut_v1_0_0.py"] = "standin"; STANDKEY["umbrellaCut_v1_0_0.py"] = ("Sample forecast data",)
# ---- charts and tables: each a setup and one expression --------------------------------------------------------------------------
CHARTS = {"topicBits": {"setup": "import math, secrets\n",
                        "expr": "[['book: 8 of 62', round(8 * math.log2(62), 1)], ['urlsafe(16)', 16 * 8], ['urlsafe(32)', 32 * 8]]"}}
# the interpreters of the research that are installed on the build machine (Ubuntu packages for 3.11 to 3.13, uv for 3.14.6 and 3.15.0b4)
INTERPS = [("3.11.17", "/usr/bin/python3.11"), ("3.12.3", "/usr/bin/python3.12"), ("3.13.16", "/usr/bin/python3.13"),
           ("3.14.6", "/root/.local/bin/python3.14"), ("3.15.0b4", "/root/.local/bin/python3.15")]
_PROBE = r'''
import ssl, smtplib, imaplib, importlib, inspect, warnings, socketserver, threading, time, json, datetime, email.utils as eu
from email.message import EmailMessage
warnings.simplefilter('ignore')
r = {}
r['idle'] = 'yes' if hasattr(imaplib.IMAP4, 'idle') else 'no'
r['keyfile'] = 'yes' if 'keyfile' in inspect.signature(smtplib.SMTP.starttls).parameters else 'no'
def imp(n):
    try: importlib.import_module(n); return 'yes'
    except ModuleNotFoundError: return 'gone'
r['smtpd'] = imp('smtpd'); r['telnetlib'] = imp('telnetlib')
f = ssl.create_default_context().verify_flags
r['strict'] = 'yes' if (f & ssl.VERIFY_X509_STRICT and f & ssl.VERIFY_X509_PARTIAL_CHAIN) else 'no'
r['minv'] = ssl.create_default_context().minimum_version.name.replace('TLSv1_2', 'TLS 1.2').replace('MINIMUM_SUPPORTED', 'lowest')
r['pstrict'] = 'yes' if 'strict' in inspect.signature(eu.parseaddr).parameters else 'no'
try: eu.localtime(datetime.datetime(2026, 1, 1), isdst=0); r['isdst'] = 'yes'
except TypeError: r['isdst'] = 'TypeError'
log = []
class H(socketserver.StreamRequestHandler):
    def handle(self):
        w = lambda s: (self.wfile.write(s.encode() + b'\r\n'), self.wfile.flush()); w('220 x'); cm = []
        while True:
            l = self.rfile.readline()
            if not l: break
            c = l.decode().strip(); cm.append(c); u = c.upper()
            if u == 'DATA':
                w('354 go')
                while self.rfile.readline() not in (b'.\r\n', b''): pass
                w('250 q')
            elif u == 'QUIT': w('221 b'); break
            else: w('250 ok')
        log.append(cm)
srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); srv.daemon_threads = True; threading.Thread(target=srv.serve_forever, daemon=True).start()
m = EmailMessage(); m['From'] = 'al@example.com'; m['To'] = 'jon@example.org'; m['Subject'] = 's'; m.set_content('b')
with smtplib.SMTP('127.0.0.1', srv.server_address[1]) as s: s.send_message(m)
for _ in range(200):
    if log: break
    time.sleep(0.02)
r['wire'] = [x for x in log[0] if x.lower().startswith('mail')][0].split(':')[0]
print(json.dumps(r))
'''
_ROWS = [("IMAP4.idle() exists", "idle"), ("starttls(keyfile=...) accepted", "keyfile"), ("import smtpd", "smtpd"), ("import telnetlib", "telnetlib"),
         ("default context: STRICT + PARTIAL_CHAIN", "strict"), ("default context: lowest TLS version", "minv"), ("parseaddr(strict=...) accepted", "pstrict"), ("localtime(isdst=0)", "isdst"), ("smtplib writes", "wire")]
TABLES = {"interpreters": {
    "setup": "import json, subprocess\nPROBE = %r\nINTERPS = %r\nres = []\nfor v, p in INTERPS:\n    r = subprocess.run([p, '-c', PROBE], capture_output=True, text=True)\n    assert r.returncode == 0, (v, r.stderr[-300:])\n    res.append(json.loads(r.stdout))\nROWS = %r\n" % (_PROBE, INTERPS, _ROWS),
    "expr": "[['check'] + [v for v, p in INTERPS]] + [[label] + [x[key] for x in res] for label, key in ROWS]"}}
# ---- runs under other environments of the research (recorded, then used in a card) ---------------------------------------------------
BARE_CODE = ("for name in ('ezgmail', 'requests', 'aiosmtpd'):\n"
             "    try:\n"
             "        __import__(name); print(name, 'imported')\n"
             "    except ImportError as e:\n"
             "        print(type(e).__name__, '-', e)\n"
             "import smtplib, email.message, imaplib\n"
             "print('smtplib, email and imaplib imported')\n")
PINS_CODE = ("import importlib.metadata as m, requests\n"
             "print('requests', m.version('requests'), '| ezgmail', m.version('ezgmail'))\n"
             "r = requests.Request('POST', 'http://127.0.0.1:1/t', data='Yedekleme tamamlandı').prepare()\n"
             "print('body', r.body, '| Content-Length', r.headers['Content-Length'], '| Content-Type', r.headers.get('Content-Type'))\n"
             "try:\n"
             "    requests.Request('POST', 'http://127.0.0.1:1/t', data='x', headers={'Priority': 5}).prepare()\n"
             "except Exception as e:\n"
             "    print('Priority 5 ->', type(e).__name__)\n")
