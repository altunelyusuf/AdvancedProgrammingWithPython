#!/usr/bin/env python3
"""SEN0414 chapter 20 (Sending Email, Texts, and Push Notifications, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, in the shape of
sen0414_ch19_corpus_base_v1_0_0.py. Each program is a complete script that exits 0 and prints what it printed on 2026-10-13 under
Python 3.14.6 (uv) in the environment /home/claude/venv314_ch20_latest (ezgmail 2026.4.28, requests 2.34.2, aiosmtpd 1.4.6, cryptography,
google-api-python-client 2.201.0, oauth2client 4.1.3); the rest is the standard library. Nothing is sent to any person, phone, push service or mail
provider, and no account is used. Where a program needs a server it uses a LOCAL STAND-IN, and the standing label of each is in its first comment line:
  SMTP    aiosmtpd on 127.0.0.1 with a self-signed certificate (a stand-in for smtp.gmail.com; the chapter itself does not use SMTP);
  Gmail   the real ezgmail library on a stand-in for Google's server: the Gmail API client is built from the library's own discovery document and its HTTP
          layer returns API-shaped replies written by this study;
  ntfy    a recorder on 127.0.0.1 that logs what requests sends (it is not ntfy and says nothing about what ntfy.sh does).
Programs that need no stand-in: EMAILBUILD, SMS, SECRECY, UNSUB (webbrowser.open is replaced by a recorder), CONTROL (the mailbox is a list in memory).
Programs that use a stand-in: SMTPLOCAL, SMTPERRORS, ENVELOPE (SMTP); EZGMAIL1, EZGMAIL2 (Gmail); NTFY1, NTFY2 (ntfy). Moments are made from numbers and the
zone is named, so all twelve give the same text on every run. The record that reads the book's page, asks the public services and drives real IMAP software is
sen0414_ch20_live_v1_0_0.py; the record that replays the chapter's listings is sen0414_ch20_thirdparty_v1_0_0.py.
"""
HEAD = r'''import io, os, re, sys, math, shlex, subprocess, json, time, base64, shutil, socket, ssl, smtplib, tempfile, threading, datetime, hashlib, hmac, mimetypes, secrets, warnings, email, inspect, contextlib, importlib.metadata as md
from datetime import datetime as DT, timedelta as TD, date as D, timezone, UTC
from zoneinfo import ZoneInfo
from email import policy, utils as eu
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def err(f):
    try: return ('ok', f())
    except BaseException as e: return (type(e).__name__, str(e))
def wd():
    d = tempfile.mkdtemp(); os.chdir(d); return d
'''
MSG = r'''def mk(**kw):
    m = EmailMessage(); m['From'] = kw.get('frm', 'Al Sweigart <al@example.com>'); m['To'] = kw.get('to', 'Jon Doe <jon@example.org>'); m['Subject'] = kw.get('subj', 'RoboCop')
    m['Date'] = eu.formatdate(1797000528, usegmt=True); m['Message-ID'] = '<fixed-1@example.com>'
    for k, v in kw.get('extra', {}).items(): m[k] = v
    m.set_content(kw.get('body', 'Do you want to watch RoboCop this weekend?')); return m
'''
SMTP = r'''import ipaddress, logging
logging.getLogger('mail.log').setLevel(logging.CRITICAL)
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult, LoginPassword
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
def serve(**kw):
    d = tempfile.mkdtemp(); key = ec.generate_private_key(ec.SECP256R1()); nm = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'localhost')]); t0 = datetime.datetime(2026, 1, 1)
    crt = (x509.CertificateBuilder().subject_name(nm).issuer_name(nm).public_key(key.public_key()).serial_number(1).not_valid_before(t0).not_valid_after(t0 + datetime.timedelta(days=3650))
           .add_extension(x509.SubjectAlternativeName([x509.DNSName('localhost'), x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]), critical=False).sign(key, hashes.SHA256()))
    cp, kp = d + '/c.pem', d + '/k.pem'
    open(cp, 'wb').write(crt.public_bytes(serialization.Encoding.PEM)); open(kp, 'wb').write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    sc = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER); sc.load_cert_chain(cp, kp); box = []
    class H:
        async def handle_RCPT(s, server, session, envelope, address, rcpt_options):
            if address.endswith('@refused.example'): return '550 5.1.1 no such mailbox'
            envelope.rcpt_tos.append(address); return '250 OK'
        async def handle_DATA(s, server, session, envelope):
            box.append({'from': envelope.mail_from, 'to': list(envelope.rcpt_tos), 'data': envelope.original_content, 'tls': session.ssl is not None, 'auth': bool(session.authenticated), 'opts': list(envelope.mail_options)}); return '250 OK queued'
    def authn(server, session, envelope, mechanism, data):
        ok = isinstance(data, LoginPassword) and data.login == b'user' and data.password == b'secret'
        return AuthResult(success=ok, handled=ok)
    so = socket.socket(); so.bind(('127.0.0.1', 0)); port = so.getsockname()[1]; so.close()
    c = Controller(H(), hostname='127.0.0.1', port=port, tls_context=sc, authenticator=authn, auth_required=kw.get('auth_required', False), auth_require_tls=kw.get('auth_require_tls', True), require_starttls=kw.get('require_starttls', False), enable_SMTPUTF8=True)
    c.start(); return c, box, port, cp
'''
GM = r'''import ezgmail, httplib2
from googleapiclient.discovery import build
class Rec(httplib2.Http):
    def __init__(s, replies=()): super().__init__(); s.log = []; s.replies = list(replies)
    def request(s, uri, method='GET', body=None, headers=None, **k):
        s.log.append((method, uri.split('/gmail/v1/')[-1], body)); r = s.replies.pop(0) if s.replies else {}
        return httplib2.Response({'status': '200', 'content-type': 'application/json'}), json.dumps(r).encode()
def gm(*replies):
    h = Rec(replies); ezgmail.SERVICE_GMAIL = build('gmail', 'v1', http=h); ezgmail.EMAIL_ADDRESS = 'me@example.com'; return h
def b64(t): return base64.urlsafe_b64encode(t if isinstance(t, bytes) else t.encode()).decode()
def api_msg(i, tid, frm, to, subj, text, ms, parts=None):
    h = [{'name': 'From', 'value': frm}, {'name': 'To', 'value': to}, {'name': 'Subject', 'value': subj}, {'name': 'Content-Type', 'value': 'text/plain; charset="UTF-8"'}]
    if parts is None: pl = {'headers': h, 'mimeType': 'text/plain', 'body': {'size': len(text), 'data': b64(text)}}
    else: pl = {'headers': h, 'mimeType': 'multipart/mixed', 'body': {'size': 0}, 'parts': parts}
    return {'id': i, 'threadId': tid, 'snippet': text[:60], 'historyId': '1', 'internalDate': str(ms), 'payload': pl}
def raw_of(h, n=0): return email.message_from_bytes(base64.urlsafe_b64decode(json.loads(h.log[n][2])['raw']), policy=policy.default)
'''
NTFY = r'''import http.server, requests
def recorder(status=200, text=''):
    log = []
    class Hd(http.server.BaseHTTPRequestHandler):
        def _do(s):
            n = int(s.headers.get('Content-Length') or 0); body = s.rfile.read(n) if n else b''
            log.append({'method': s.command, 'path': s.path, 'headers': dict(s.headers.items()), 'body': body})
            s.send_response(status); s.send_header('Content-Length', str(len(text.encode()))); s.end_headers(); s.wfile.write(text.encode())
        do_GET = do_POST = do_PUT = _do
        def log_message(s, *a): pass
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Hd); threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, log, 'http://127.0.0.1:%d' % srv.server_address[1]
'''
EMAILBUILD = HEAD + MSG + r'''# The standard library's way to build a message (the chapter uses EZGmail instead): EmailMessage, the MIME tree, encoded headers, address parsing.
m = mk()
raw = m.as_bytes()
print('class:', type(m).__name__, '| policy:', type(m.policy).__name__, '| CRLF in as_bytes():', raw.count(b'\r\n'), '| in as_bytes(policy=SMTP):', m.as_bytes(policy=policy.SMTP).count(b'\r\n'))
print('\n'.join(raw.decode().splitlines()))
m.add_alternative('<p>Do you want to watch <b>RoboCop</b>?</p>', subtype='html'); m.add_attachment(b'\x00\x01\x02', maintype='application', subtype='octet-stream', filename='poster.bin')
print('MIME tree:', [p.get_content_type() for p in m.walk()], '| attachments:', [a.get_filename() for a in m.iter_attachments()], '| preferred body:', m.get_body(preferencelist=('html', 'plain')).get_content_type())
from email.header import decode_header, make_header
t = mk(subj='Yedekleme bitti \u2713 \u015f\u011f\u0131', to='"Y\u0131lmaz, Ay\u015fe" <ayse@example.org>').as_bytes().decode('ascii').splitlines()
print([x for x in t if x.startswith(('Subject', 'To'))])
print('decoded subject:', str(make_header(decode_header([x for x in t if x.startswith('Subject')][0].split(': ', 1)[1]))))
s = '"Doe, Jon" <jon@example.org>, Al Sweigart <al@inventwithpython.com>, plain@example.com'
print('getaddresses:', eu.getaddresses([s]), '| without the quotes:', eu.getaddresses([s.replace('"Doe, Jon"', 'Doe, Jon')]))
print('parseaddr of two addresses:', eu.parseaddr('real@example.com, evil@example.net'), '| strict=False:', eu.parseaddr('real@example.com, evil@example.net', strict=False))
print('formataddr:', eu.formataddr(('Jon Doe', 'jon@example.org')), '|', eu.formataddr(('Y\u0131lmaz, Ay\u015fe', 'ayse@example.org')))
try:
    e = EmailMessage(); e['Subject'] = 'hello\r\nBcc: evil@example.net'
except ValueError as ex: print('EmailMessage refuses a line break in a header:', ex)
try: MIMEText('body')['Subject']; l = MIMEText('body'); l['Subject'] = 'hello\r\nBcc: evil@example.net'; l.as_string()
except Exception as ex: print('MIMEText (what EZGmail uses) refuses it only when written:', type(ex).__name__)
mid = eu.make_msgid(idstring='job1', domain='example.com'); print('Message-ID shape:', mid.startswith('<') and mid.endswith('job1@example.com>'), '| Date:', eu.formatdate(1797000528, usegmt=True))
'''
SMTPLOCAL = HEAD + MSG + SMTP + r'''# smtplib against a LOCAL STAND-IN (aiosmtpd with a self-signed certificate on 127.0.0.1), not against Gmail: STARTTLS, certificate checks, AUTH only after TLS.
c, box, port, cp = serve()
try:
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); print('EHLO before STARTTLS:', s.ehlo()[1].decode().splitlines()[1:])
    print('STARTTLS:', s.starttls(context=ssl.create_default_context(cafile=cp))[0], '| EHLO after:', s.ehlo()[1].decode().splitlines()[1:])
    print('send_message:', s.send_message(mk()), '| the server saw TLS:', box[0]['tls'], '| envelope:', box[0]['from'], box[0]['to']); s.quit()
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    try: s.starttls(context=ssl.create_default_context())
    except ssl.SSLCertVerificationError as e: print('default context, self-signed certificate:', type(e).__name__, '|', e.verify_message)
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo(); r = s.starttls()
    print('starttls() with NO context:', r[0], '(no certificate check: the connection is encrypted but not authenticated)'); s.close()
    ctx = ssl.create_default_context(cafile=cp); print('create_default_context():', ctx.check_hostname, ctx.verify_mode.name)
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    try: s.login('user', 'secret')
    except smtplib.SMTPNotSupportedError as e: print('login before STARTTLS:', e)
    s.starttls(context=ctx); s.ehlo(); print('AUTH advertised after TLS:', [x for x in s.ehlo()[1].decode().splitlines() if x.startswith('AUTH')], '| login:', s.login('user', 'secret')); s.quit()
finally: c.stop()
'''
SMTPERRORS = HEAD + MSG + SMTP + r'''# What smtplib raises when the server refuses, on a LOCAL STAND-IN (aiosmtpd on 127.0.0.1): one recipient refused, all refused, wrong password, closed port.
c, box, port, cp = serve()
try:
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    print('one of two refused -> returns a dict, the message WAS sent to the other:', s.send_message(mk(to='ok@example.org, gone@refused.example')), [x['to'] for x in box])
    try: s.send_message(mk(to='gone@refused.example'))
    except smtplib.SMTPRecipientsRefused as e: print('all refused ->', type(e).__name__, e.recipients, '| messages stored:', len(box))
    s.quit()
    ctx = ssl.create_default_context(cafile=cp); s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo(); s.starttls(context=ctx); s.ehlo()
    try: s.login('user', 'wrong')
    except smtplib.SMTPAuthenticationError as e: print('wrong password ->', type(e).__name__, e.smtp_code, e.smtp_error)
    s.close()
finally: c.stop()
try: smtplib.SMTP('127.0.0.1', 1, timeout=3)
except OSError as e: print('closed port ->', type(e).__name__)
'''
ENVELOPE = HEAD + MSG + SMTP + r'''# The envelope is not the header: Bcc recipients are in RCPT TO and not in the message, and the From of the header can be anything. LOCAL STAND-IN (aiosmtpd).
c, box, port, cp = serve()
try:
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    m = mk(extra={'Cc': 'friend@example.com', 'Bcc': 'secret@example.com'}); s.send_message(m)
    h = email.message_from_bytes(box[0]['data'], policy=policy.default)
    print('send_message: envelope', box[0]['from'], box[0]['to'], '| header Bcc:', h['Bcc'], '| header Cc:', h['Cc'], '| secret address anywhere in the message:', 'secret@example.com' in box[0]['data'].decode())
    s.sendmail('bounces@mallory.example', ['jon@example.org', 'hidden@example.org'], mk(frm='CEO <ceo@bank.example>').as_bytes()); s.quit()
    h = email.message_from_bytes(box[1]['data'], policy=policy.default)
    print('sendmail: envelope from', box[1]['from'], '| header From:', h['From'], '| rcpt:', box[1]['to'], '| the server asked for no login:', box[1]['auth'])
finally: c.stop()
print('the book: "it is fairly trivial for hackers to fake a from address"; here the server accepted a From that matches neither the envelope nor a login.')
'''
EZGMAIL1 = HEAD + GM + r'''# The real ezgmail library on a STAND-IN for Google's server (the HTTP layer returns replies written by this study); nothing leaves the machine.
d = wd(); open('attachment1.jpg', 'wb').write(b'\xff\xd8\xff\xe0' + b'0' * 20); open('attachment2.mp3', 'wb').write(b'ID3' + b'0' * 20); open('setup.exe', 'wb').write(b'MZ' + b'0' * 8)
e = err(lambda: ezgmail.init()); print('init() with no credentials:', e[0], '|', e[1].split(' You can')[0].replace(d, 'DIR'), '| LOGGED_IN:', ezgmail.LOGGED_IN, '| SCOPES:', ezgmail.SCOPES, '| version:', ezgmail.__version__)
print('last line of the module:', inspect.getsource(ezgmail).rstrip().splitlines()[-1])
h = gm({}, {}, {}, {}, {})
ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email'); m = raw_of(h, 0)
print('send ->', h.log[0][0], h.log[0][1], '| body keys:', list(json.loads(h.log[0][2])), '| headers:', list(m.keys()), '|', m.get_content_type(), m['Content-Transfer-Encoding'])
ezgmail.send('recipient@example.com', 'Subject line', 'Body', ['attachment1.jpg', 'attachment2.mp3', 'setup.exe']); m = raw_of(h, 1)
print('attachments:', [(p.get_content_type(), p.get_filename()) for p in m.iter_parts()], '| the library did not refuse the .exe (the Gmail help page says Gmail blocks it; not run against Gmail)')
ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email', cc='friend@example.com', bcc='otherfriend@example.com,someoneelse@example.com'); m = raw_of(h, 2)
print('cc:', m['cc'], '| bcc header written into the message:', m['bcc'])
ezgmail.send('a@example.com', 'Rapor: \u015f\u011f\u0131', 'Yedekleme tamamland\u0131'); m = raw_of(h, 3)
print('non-ASCII: subject', m['subject'], '| body', m.get_content().strip(), '| charset', m.get_content_charset())
try: ezgmail.send('a@example.com', 'hello\nBcc: evil@example.net', 'body')
except Exception as ex: print('a line break in the subject:', type(ex).__name__)
src = ezgmail.GmailMessage(api_msg('M1', 'T1', 'Al Sweigart <al@inventwithpython.com>', 'Jon Doe <example@gmail.com>', 'RoboCop', 'Do you want to watch RoboCop this weekend?', 1797000000000))
src.reply('Yes, Saturday works.'); body = json.loads(h.log[4][2]); m = raw_of(h, 4)
print('reply -> body keys', sorted(body), '| threadId', body['threadId'], '| To', m['to'], '| Subject', m['subject'], '| In-Reply-To/References:', [k for k in m.keys() if k.lower() in ('in-reply-to', 'references')], '| replyAll() returns', ezgmail.GmailMessage.replyAll(src, 'x'))
'''
EZGMAIL2 = HEAD + GM + r'''# ezgmail's read side on a STAND-IN for Google's server: threads, messages, the repr, summary(), the quoted-text cut, attachment download and a hostile file name.
t = {'id': 'T1', 'snippet': 'Do you want to watch RoboCop this weekend?', 'historyId': '9'}
full = {'id': 'T1', 'messages': [api_msg('M1', 'T1', 'Al Sweigart <al@inventwithpython.com>', 'Jon Doe <example@gmail.com>', 'RoboCop', 'Do you want to watch RoboCop this weekend?\r\n', 1797000000000), api_msg('M2', 'T1', 'Jon Doe <example@gmail.com>', 'Al Sweigart <al@inventwithpython.com>', 'Re: RoboCop', 'Yes.\r\n', 1797000100000)]}
h = gm(full); th = ezgmail.GmailThread(t); n0 = len(h.log); s = str(th); n1 = len(h.log)
print('API calls before / after str(thread):', n0, n1, '| the repr:', s, '| the book prints: <GmailThread len=2 snippet= Do you want to watch RoboCop this weekend?\'>')
print('messages:', len(th.messages), [type(x).__name__ for x in th.messages], th.text, th.senders())
h = gm({}, {}, {}, {}, {}); ezgmail.unread(); ezgmail.unread(maxResults=50); ezgmail.recent(); ezgmail.search('has:attachment'); ezgmail.search('from:al@inventwithpython.com subject:hello', maxResults=3)
print('queries sent:', [x[1] for x in h.log])
m = ezgmail.GmailMessage(api_msg('M1', 'T1', 'Al Sweigart <al@inventwithpython.com>', 'Jon Doe <example@gmail.com>', 'RoboCop', 'Do you want to watch RoboCop this weekend?\r\n', 1797000528000))
res = []
for z in ('UTC', 'America/Chicago', 'Europe/Istanbul'):
    os.environ['TZ'] = z; time.tzset(); res.append((z, str(ezgmail.GmailMessage(api_msg('M1', 'T1', 'a', 'b', 'c', 'd', 1797000528000)).timestamp)))
print('subject', m.subject, '| sender', m.sender, '| body', repr(m.body), '| timestamp by zone:', res)
bare = api_msg('M2', 'T2', 'x@example.com', 'y@example.com', 'S', 'text', 1); bare['payload']['headers'] = [x for x in bare['payload']['headers'] if x['name'] != 'Subject']
nm = ezgmail.GmailMessage(bare); print('a message with no Subject header:', err(lambda: nm.subject)[0], '|', err(lambda: str(nm))[0])
q1 = 'Sounds good.\n\nOn Sun, Jan 1, 2018 at 12:00 PM Al Sweigart <al@inventwithpython.com> wrote:\n> Do you want to watch?'
q3 = 'Tamam.\n\n1 Oca 2018 Paz 12:00 tarihinde Al Sweigart <al@inventwithpython.com> yazd\u0131:\n> Film izleyelim mi?'
print('removeQuotedParts: English pattern ->', repr(ezgmail.removeQuotedParts(q1)), '| Turkish pattern ->', ezgmail.removeQuotedParts(q3) == q3)
ths = [ezgmail.GmailThread({'id': 'T1', 'snippet': 'x', 'historyId': '1'}), ezgmail.GmailThread({'id': 'T2', 'snippet': 'y', 'historyId': '1'})]
gm({'id': 'T1', 'messages': full['messages']}, {'id': 'T2', 'messages': [api_msg('M3', 'T2', 'noreply@example.com', 'j@example.com', 'News', 'Thanks for stopping me from buying Bitcoin.', 1797000200000)]})
os.environ['TZ'] = 'UTC'; time.tzset(); ezgmail.summary(ths)
d = wd(); os.mkdir('inbox')
parts = [{'mimeType': 'text/plain', 'filename': '', 'headers': [], 'body': {'size': 1, 'data': b64('x')}}, {'mimeType': 'text/plain', 'filename': '../evil.txt', 'headers': [], 'body': {'attachmentId': 'A9', 'size': 4}}]
m = ezgmail.GmailMessage(api_msg('M1', 'T1', 'a@example.com', 'b@example.com', 's', 'x', 1797000000000, parts)); gm({'data': b64(b'PWNED'), 'size': 5})
print('downloadAllAttachments(downloadFolder="inbox") with a file named ../evil.txt ->', m.downloadAllAttachments(downloadFolder='inbox'), '| inside inbox:', os.listdir('inbox'), '| beside it:', sorted(os.listdir('.')))
parts = [{'mimeType': 'text/plain', 'filename': '', 'headers': [], 'body': {'size': 1, 'data': b64('x')}}, {'mimeType': 'image/jpeg', 'filename': 'tulips.jpg', 'headers': [], 'body': {'attachmentId': 'A1', 'size': 4}}]
m = ezgmail.GmailMessage(api_msg('M1', 'T1', 'a@example.com', 'b@example.com', 's', 'x', 1797000000000, parts)); open('tulips.jpg', 'wb').write(b'MINE'); gm({'data': b64(b'AAAA'), 'size': 4})
m.downloadAttachment('tulips.jpg'); print('an existing tulips.jpg after downloadAttachment:', open('tulips.jpg', 'rb').read(), '(overwritten, as the book says)')
print('downloadAttachment of a name that is not there:', err(lambda: m.downloadAttachment('nothere.jpg'))[0])
'''
SMS = HEAD + r'''# SMS email gateways (Table 20-1) and the length of a text. Pure arithmetic; no message is sent.
T = {'AT&T': ('txt.att.net', 'mms.att.net'), 'Boost Mobile': ('sms.myboostmobile.com', None), 'Cricket': ('sms.cricketwireless.net', 'mms.cricketwireless.net'), 'Google Fi': ('msg.fi.google.com', None),
     'Metro PCS': ('mymetropcs.com', None), 'Republic Wireless': ('text.republicwireless.com', None), 'Sprint': ('messaging.sprintpcs.com', 'pm.sprint.com'), 'T-Mobile': ('tmomail.net', None),
     'U.S. Cellular': ('email.uscc.net', 'mms.uscc.net'), 'Verizon': ('vtext.com', 'vzwpix.com'), 'Virgin Mobile': ('vmobl.com', 'vmpix.com'), 'Xfinity Mobile': ('vtext.com', 'mypixmessages.com')}
def addr(number, carrier, mms=False):
    sms, m = T[carrier]; return '%s@%s' % (number, (m or sms) if mms else sms)
print(len(T), 'providers;', 'SMS', addr('2125551234', 'Verizon'), '| MMS', addr('2125551234', 'Verizon', True), '| Boost MMS ("Same as SMS"):', addr('5555550100', 'Boost Mobile', True))
print('the same SMS domain for two carriers:', [c for c, v in T.items() if v[0] == 'vtext.com'], '| distinct SMS domains:', len(set(v[0] for v in T.values())))
print('AT&T notice: shutdown 2025-06-17 is', (datetime.date(2026, 10, 13) - datetime.date(2025, 6, 17)).days, 'days before 2026-10-13 | Verizon notice: 2027-03-31 is', (datetime.date(2027, 3, 31) - datetime.date(2026, 10, 13)).days, 'days after')
BASIC = '@\u00a3$\u00a5\u00e8\u00e9\u00f9\u00ec\u00f2\u00c7\n\u00d8\u00f8\r\u00c5\u00e5\u0394_\u03a6\u0393\u039b\u03a9\u03a0\u03a8\u03a3\u0398\u039e\x1b\u00c6\u00e6\u00df\u00c9 !"#\u00a4%&\'()*+,-./0123456789:;<=>?\u00a1ABCDEFGHIJKLMNOPQRSTUVWXYZ\u00c4\u00d6\u00d1\u00dc\u00a7\u00bfabcdefghijklmnopqrstuvwxyz\u00e4\u00f6\u00f1\u00fc\u00e0'
EXT = '^{}\\[~]|\u20ac'
def segments(t):
    n = 0
    for ch in t:
        if ch in BASIC: n += 1
        elif ch in EXT: n += 2
        else: n = None; break
    if n is not None: return ('GSM-7', n, 1 if n <= 160 else -(-n // 153))
    u = len(t.encode('utf-16-le')) // 2; return ('UCS-2', u, 1 if u <= 70 else -(-u // 67))
print('140 bytes * 8 / 7 =', 140 * 8 // 7, 'characters')
for t in ('Hello, world!', 'a' * 160, 'a' * 161, 'a' * 306, 'a' * 307, '{x}', 'Yedekleme tamamlandi', 'Yedekleme tamamland\u0131', '\u015f' * 70, '\u015f' * 71, '\U0001F600' * 35, '\U0001F600' * 36):
    print(repr(t[:24]) + ('...' if len(t) > 24 else ''), len(t), 'characters ->', segments(t))
'''
NTFY1 = HEAD + NTFY + r'''# Publishing to ntfy with requests, against a LOCAL RECORDER on 127.0.0.1 (it logs what requests sends; it is not ntfy and says nothing about what ntfy.sh does).
srv, log, base = recorder(200, '{}')
r = requests.post(base + '/AlSweigartZPgxBQ42', 'Hello, world!'); q = log[0]
print('post:', r.status_code, q['method'], q['path'], q['body'], '| Content-Length', q['headers'].get('Content-Length'), '| Content-Type', q['headers'].get('Content-Type'), '| User-Agent starts python-requests/', q['headers']['User-Agent'].startswith('python-requests/'))
requests.post(base + '/t', 'The rent is too high!', headers={'Title': 'Important: Read this!', 'Tags': 'warning,neutral_face', 'Priority': '5'}); h = log[1]['headers']
print('headers on the wire:', {k: h[k] for k in ('Title', 'Tags', 'Priority')})
for hd in ({'Priority': 5}, {'Title': 'Yedekleme tamamland\u0131'}):
    try: requests.post(base + '/t', 'x', headers=hd)
    except Exception as e: print('headers', hd, '->', type(e).__name__, str(e)[:70])
t = 'Yedekleme tamamland\u0131'
requests.post(base + '/t', t); requests.post(base + '/t', 'caf\u00e9'); requests.post(base + '/t', t.encode('latin-1', 'replace'))
print('a str body is sent as UTF-8 by urllib3', md.version('urllib3'), ':', log[-3]['body'], '| Content-Length', log[-3]['headers']['Content-Length'], 'for', len(t), 'characters; no Content-Type:', log[-3]['headers'].get('Content-Type'), '| latin-1 encoding by hand:', log[-1]['body'])
srv.shutdown(); srv, log, base = recorder(429, '{"code":42908,"http":429,"error":"limit reached"}')
r = requests.post(base + '/t', 'Hello, world!'); print('a refused post (429): the call returned', r, '| ok', r.ok, '| text', r.text, '| nothing raised; raise_for_status ->', end=' ')
try: r.raise_for_status()
except requests.HTTPError as e: print(type(e).__name__)
srv.shutdown()
'''
NTFY2 = HEAD + NTFY + r'''# Receiving from ntfy: the poll URL, the JSON lines, the event types and the timestamps. The server is a LOCAL RECORDER that answers the text the book prints.
TXT = ('{"id":"1jnHKeFNqwnS","time":1797823340,"expires":1797866540,"event":"message","topic":"AlSweigartZPgxBQ42","message":"Hello, world!"}\n'
       '{"id":"wZ22cjyKXw1F","time":1797823712,"expires":1797866912,"event":"message","topic":"AlSweigartZPgxBQ42","title":"Important: Read this!","message":"The rent is too high!","priority":5,"tags":["warning","neutral_face"]}\n')
srv, log, base = recorder(200, TXT)
resp = requests.get(base + '/AlSweigartZPgxBQ42/json?poll=1'); requests.get(base + '/AlSweigartZPgxBQ42/json?poll=1&since=10m'); requests.get(base + '/AlSweigartZPgxBQ42/json', params={'poll': 1, 'since': '2h30m'}); requests.get(base + '/AlSweigartZPgxBQ42/json', params={'poll': 1, 'since': 1737866912})
print('paths asked:', [x['path'] for x in log], '| methods:', {x['method'] for x in log})
try: json.loads(resp.text)
except json.JSONDecodeError as e: print('json.loads of the whole text:', type(e).__name__, e)
n = [json.loads(x) for x in resp.text.splitlines()]
print('splitlines then loads:', len(n), n[0]['message'], '|', n[1]['message'], '| keys of the second:', sorted(n[1]))
book = {'message', 'open', 'keepalive', 'poll_request'}; docs = {'open', 'keepalive', 'message', 'message_delete', 'message_clear', 'poll_request'}
print('event types the documentation lists that the book does not:', sorted(docs - book), '| expires - time =', n[1]['expires'] - n[1]['time'], 'seconds =', (n[1]['expires'] - n[1]['time']) / 3600, 'hours')
ts = 1797823712
for z in ('America/Chicago', 'America/Los_Angeles', 'UTC', 'Europe/Istanbul'): print(z, str(DT.fromtimestamp(ts, ZoneInfo(z))))
print('the book prints 2026-12-20 21:28:32 for str(datetime.fromtimestamp(1797823712)), which is a clock at UTC-6 (Central Standard Time)')
print('a blank line (a keepalive in a stream, or a trailing newline)', end=' -> ')
try: [json.loads(x) for x in (TXT + '\n').splitlines()]
except json.JSONDecodeError as e: print(type(e).__name__)
srv.shutdown()
'''
SECRECY = HEAD + r'''# The topic name is the only secret: how many bits the book's example has, a random one, and what the 250-a-day and 4,096-byte limits mean in bytes. Arithmetic only.
book = 'AlSweigartZPgxBQ42'; rnd = book[len('AlSweigart'):]
print('the book\'s topic:', book, '| random part:', rnd, len(rnd), 'characters of 62 ->', round(len(rnd) * math.log2(62), 1), 'bits; the name part is guessable')
t = secrets.token_urlsafe(16); print('secrets.token_urlsafe(16):', len(t), 'characters, 128 bits, alphabet', set(t) <= set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'))
print('62**8 =', 62 ** 8, '| the topic is part of the URL path:', 'https://ntfy.sh/' + book, '(it lands in logs, proxies and browser history)')
ok = 'a' * 4096; no = 'a' * 4097; tr = '\u0131' * 2049
print('4096 ASCII characters =', len(ok.encode()), 'bytes | 4097 =', len(no.encode()), '| 2049 Turkish dotless i =', len(tr), 'characters but', len(tr.encode()), 'bytes (over the limit)')
print('250 messages of 4096 bytes =', 250 * 4096, 'bytes a day;', 'one message every', 86400 / 250, 'seconds on average')
print('the book: "Anyone in the world can send messages to a topic ... there is no way to determine who posted a message"; the sender line has to be inside the text')
'''
UNSUB = HEAD + r'''# The Auto Unsubscriber practice program: find unsubscribe links in HTML with html.parser (the book suggests Beautiful Soup) and read the List-Unsubscribe header (RFC 2369, RFC 8058).
from html.parser import HTMLParser
HTML = '<p>Hi <a href="https://example.com/u?id=1">Unsubscribe</a> | <a href="https://example.com/p">Preferences</a> | <a href="https://example.com/x"><img alt="unsubscribe"></a> <a href="https://example.com/u2">click here to opt out</a></p>'
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
print('links whose text says unsubscribe:', p.found, '| the word occurs', len(re.findall('unsubscribe', HTML, re.I)), 'times in the HTML (an alt text and a link that says "opt out" are not found by the book\'s method)')
m = EmailMessage(); m['List-Unsubscribe'] = '<mailto:unsub@example.com?subject=unsubscribe>, <https://example.com/u?id=1>'; m['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click'
lu = [x.strip('<>') for x in m['List-Unsubscribe'].split(', ')]; print('List-Unsubscribe:', lu, '| One-Click:', m['List-Unsubscribe-Post'])
opened = []
class FakeBrowser:
    def open(self, url): opened.append(url); return True
import webbrowser; webbrowser.open = FakeBrowser().open
for u in p.found: webbrowser.open(u)
print('webbrowser.open was replaced by a recorder; it would have opened', opened, '- opening a link from an unknown sender with a browser confirms to the sender that the address is read')
'''
CONTROL = HEAD + r'''# The Email-Based Computer Control practice program: the password check, an allow-list, Popen and wait, deleting what was read. The mailbox is a list in memory
# (the IMAP version ran against a real IMAP server in sen0414_ch20_live_v1_0_0.py).
SECRET = 'correct horse'; ALLOW = {'sleep': [sys.executable, '-c', 'import time; time.sleep(0.2)'], 'noop': [sys.executable, '-c', 'pass']}
inbox = [('me@example.com', 'correct horse:noop'), ('x@example.net', 'guess:noop'), ('me@example.com', 'correct horse:rm'), ('me@example.com', 'correct horse:sleep')]
done = []
while inbox:
    frm, body = inbox.pop(0); pw, _, cmd = body.partition(':')
    if not hmac.compare_digest(pw.encode(), SECRET.encode()): done.append((frm, 'bad password')); continue
    if cmd not in ALLOW: done.append((frm, 'refused ' + cmd)); continue
    p = subprocess.Popen(ALLOW[cmd]); done.append((frm, cmd, p.wait()))
print(done, '| left in the inbox:', inbox)
try: subprocess.Popen(['C:\\Program Files (x86)\\qBittorrent\\qbittorrent.exe', 'shakespeare_complete_works.torrent'])
except FileNotFoundError as e: print("the book's Popen on Linux:", type(e).__name__)
subj = 'status; echo PWNED'
print('shell=True with text from an e-mail:', subprocess.run('echo ' + subj, shell=True, capture_output=True, text=True).stdout.splitlines(), '| as a list:', subprocess.run(['echo', subj], capture_output=True, text=True).stdout.splitlines(), '| shlex.quote:', shlex.quote(subj))
try: hmac.compare_digest('\u00e9', '\u00e9')
except TypeError as e: print('compare_digest of non-ASCII str:', type(e).__name__)
print('the book: "require that the emails contain a password" - an e-mail password travels in clear text through every server unless the hops use TLS (see smtpLocalStarttls)')
'''
PROGRAMS = {
    'emailMessageBuild_v1_0_0.py': (EMAILBUILD, (), False),
    'smtpLocalStarttls_v1_0_0.py': (SMTPLOCAL, ('aiosmtpd', 'cryptography'), False),
    'smtpErrorsLocal_v1_0_0.py': (SMTPERRORS, ('aiosmtpd', 'cryptography'), False),
    'envelopeVersusHeaders_v1_0_0.py': (ENVELOPE, ('aiosmtpd', 'cryptography'), False),
    'ezgmailSendWithStandIn_v1_0_0.py': (EZGMAIL1, ('ezgmail',), False),
    'ezgmailReadWithStandIn_v1_0_0.py': (EZGMAIL2, ('ezgmail',), False),
    'smsGatewaysAndSegments_v1_0_0.py': (SMS, (), False),
    'ntfyPublishRecorder_v1_0_0.py': (NTFY1, ('requests',), False),
    'ntfyPollParse_v1_0_0.py': (NTFY2, ('requests',), False),
    'topicSecrecyAndLimits_v1_0_0.py': (SECRECY, (), False),
    'unsubscribeFinder_v1_0_0.py': (UNSUB, (), False),
    'emailControlLoop_v1_0_0.py': (CONTROL, (), False),
}
STAND_IN = {'smtpLocalStarttls_v1_0_0.py': 'SMTP', 'smtpErrorsLocal_v1_0_0.py': 'SMTP', 'envelopeVersusHeaders_v1_0_0.py': 'SMTP', 'ezgmailSendWithStandIn_v1_0_0.py': 'Gmail',
            'ezgmailReadWithStandIn_v1_0_0.py': 'Gmail', 'ntfyPublishRecorder_v1_0_0.py': 'ntfy', 'ntfyPollParse_v1_0_0.py': 'ntfy', 'emailControlLoop_v1_0_0.py': 'mailbox (an in-memory list)'}
FIXTURE_BASED = []

if __name__ == "__main__":
    # Usage: /home/claude/venv314_ch20_latest/bin/python sen0414_ch20_corpus_base_v1_0_0.py   (exits 1 if a program does not exit 0)
    import os, subprocess, sys
    bad = 0
    for name, (code, needs, live) in PROGRAMS.items():
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=300)
        bad += r.returncode != 0
        print("=== %s (exit %d)%s%s" % (name, r.returncode, " LIVE" if live else "", " [local stand-in: %s]" % STAND_IN[name] if name in STAND_IN else "")); print(r.stdout.rstrip()[:3000]); print(r.stderr[-400:].rstrip())
    print("%d programs, %d did not exit 0" % (len(PROGRAMS), bad)); sys.exit(1 if bad else 0)
