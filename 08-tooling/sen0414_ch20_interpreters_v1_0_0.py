#!/usr/bin/env python3
"""Chapter 20: runs one program, the standard-library side of e-mail (email, smtplib, imaplib, ssl and email.utils) against a small SMTP server written with
sockets inside the program, under every installed 3.14 patch release (3.14.0 to 3.14.6, `uv python install 3.14.N`) and, for comparison, under 3.15 (a beta,
3.15.0b4, the newest uv offers), 3.13, 3.12 and 3.11, and records what each printed. It answers the question chapters 13 to 19 answered with a difference:
does anything the chapter's neighbours (smtplib, imaplib, email) do change between the patch releases of Python 3.14, and between 3.14 and the releases before it?
There is no package: email, smtplib, imaplib, ssl, socket and threading are the standard library of each interpreter, so a difference comes from the interpreter.
The chapter itself uses none of these modules (it uses EZGmail and requests); the standard-library modules are what the chapter says EZGmail replaces.
The SMTP server in the program is a local stand-in: it speaks just enough of RFC 5321 (EHLO, MAIL, RCPT, DATA, QUIT, and a refusal of one address) on 127.0.0.1 and logs
what it receives; it is not a mail server. Nothing leaves the machine. The operating system is Ubuntu 24.04. Python runs in isolated mode, each interpreter by
`uv run --no-project`.
Usage: sen0414_ch20_interpreters_v1_0_0.py   (needs uv on PATH)   -> ch20-page/interpreter_record_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "08-tooling", "ch20-page", "interpreter_record_v1_0_0.json")
PROG = r'''
import sys, os, io, ssl, json, socket, socketserver, threading, warnings, inspect, smtplib, imaplib, email, importlib, datetime
from email import policy, utils as eu
from email.message import EmailMessage
from email.mime.text import MIMEText
res = {}
def w(f):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter('always')
        try: v = f()
        except BaseException as e: v = type(e).__name__ + ': ' + str(e)[:110]
    return [v, sorted({x.category.__name__ for x in seen})]
res['series'] = sys.version.split()[0].rsplit('.', 1)[0] + '.x'
res['platform'] = [sys.platform, os.name]
# removed modules
for m in ('smtpd', 'asyncore', 'asynchat', 'imghdr', 'sndhdr', 'cgi', 'telnetlib', 'nntplib'):
    res['import ' + m] = w(lambda m=m: (importlib.import_module(m), 'imported')[1])
# signatures
res['smtplib.SMTP.starttls parameters'] = list(inspect.signature(smtplib.SMTP.starttls).parameters)
res['smtplib.SMTP_SSL parameters'] = list(inspect.signature(smtplib.SMTP_SSL.__init__).parameters)
res['imaplib.IMAP4_SSL parameters'] = list(inspect.signature(imaplib.IMAP4_SSL.__init__).parameters)
res['imaplib.IMAP4.starttls parameters'] = list(inspect.signature(imaplib.IMAP4.starttls).parameters)
res['imaplib.IMAP4 has idle and IDLE in Commands'] = [hasattr(imaplib.IMAP4, 'idle'), 'IDLE' in imaplib.Commands]
res['smtplib.SMTP_SSL(keyfile=) draws'] = w(lambda: smtplib.SMTP_SSL(keyfile='k.pem'))
res['imaplib.IMAP4_SSL(keyfile=) draws'] = w(lambda: imaplib.IMAP4_SSL('127.0.0.1', 1, keyfile='k.pem'))
res['ports'] = [smtplib.SMTP_PORT, smtplib.SMTP_SSL_PORT, imaplib.IMAP4_PORT, imaplib.IMAP4_SSL_PORT]
# ssl defaults
def sslinfo():
    c = ssl.create_default_context(); return [c.check_hostname, c.verify_mode.name, c.minimum_version.name, sorted(f.name for f in ssl.VerifyFlags if f in c.verify_flags and f.value)]
res['ssl.create_default_context(): check_hostname, verify_mode, minimum_version, verify_flags'] = w(sslinfo)
res['ssl.PROTOCOL_TLS_CLIENT context verify_mode'] = w(lambda: ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT).verify_mode.name)
# address parsing (a security fix of 3.12.6 / 3.13)
bad = 'real@example.com, evil@example.net'
res['email.utils.parseaddr of two addresses'] = w(lambda: eu.parseaddr(bad))
res['email.utils.parseaddr(strict=False)'] = w(lambda: eu.parseaddr(bad, strict=False))
res['email.utils.getaddresses of two addresses'] = w(lambda: eu.getaddresses([bad]))
res['email.utils.supports_strict_parsing'] = getattr(eu, 'supports_strict_parsing', None)
res['email.utils.parseaddr of a quoted name with a comma'] = w(lambda: eu.parseaddr('"Doe, Jon" <jon@example.org>'))
res['email.utils.localtime(isdst=0)'] = w(lambda: str(eu.localtime(datetime.datetime(2026, 1, 1), isdst=0)))
# header injection (a fix of 3.12.5 / 3.13)
def modern():
    m = EmailMessage(); m['Subject'] = 'hello\r\nBcc: evil@example.net'; return 'accepted'
def legacy():
    m = MIMEText('body'); m['To'] = 'a@example.com'; m['Subject'] = 'hello\r\nBcc: evil@example.net'; return [l for l in m.as_string().splitlines() if l.lower().startswith(('subject', 'bcc', ' '))]
def legacy_bytes():
    m = MIMEText('body'); m['Subject'] = 'hello\nBcc: evil@example.net'; return m.as_bytes().decode().splitlines()[:6]
res['EmailMessage header with a line break'] = w(modern)
res['MIMEText (the legacy compat32 policy, which EZGmail uses) header with a line break, as_string'] = w(legacy)
res['MIMEText header with a bare linefeed, as_bytes'] = w(legacy_bytes)
def policy_default_set():
    m = EmailMessage(policy=policy.default); m['To'] = 'a@example.com'; m['Subject'] = 'x'; m['X-Evil'] = 'a\nBcc: b@example.net'; return 'accepted'
res['EmailMessage X- header with a bare linefeed'] = w(policy_default_set)
# non-ascii text and addresses
def body():
    m = EmailMessage(); m['Subject'] = 'Yedekleme bitti'; m.set_content('tamamlandı'); return [m['Content-Transfer-Encoding'], m.get_content_charset(), m.as_bytes().decode().splitlines()[-1]]
res['EmailMessage with Turkish text: transfer encoding, charset, last line'] = w(body)
def mimetext():
    m = MIMEText('tamamlandı'); return [m['Content-Type'], m['Content-Transfer-Encoding']]
res['MIMEText with Turkish text'] = w(mimetext)
def nonascii_addr():
    m = EmailMessage(); m['To'] = 'ayşe@example.org'; m['From'] = 'a@example.com'; m.set_content('x'); return m.as_bytes(policy=policy.SMTP).decode().splitlines()[:2]
res['EmailMessage with a non-ASCII address, policy.SMTP, as_bytes'] = w(nonascii_addr)
def nonascii_addr_utf8():
    m = EmailMessage(); m['To'] = 'ayşe@example.org'; m['From'] = 'a@example.com'; m.set_content('x'); return m.as_bytes(policy=policy.SMTPUTF8).decode('utf-8').splitlines()[:2]
res['EmailMessage with a non-ASCII address, policy.SMTPUTF8, as_bytes'] = w(nonascii_addr_utf8)
def long_header():
    m = EmailMessage(); m['Subject'] = 'x' * 1200; return max(len(l) for l in m.as_bytes().splitlines())
res['longest line of a header with 1200 characters and no space'] = w(long_header)
def make_id():
    mid = eu.make_msgid(idstring='job1', domain='example.com'); return [mid.startswith('<'), mid.endswith('job1@example.com>')]
res['email.utils.make_msgid shape'] = w(make_id)
res['email.utils.formatdate(1797000528, usegmt=True)'] = w(lambda: eu.formatdate(1797000528, usegmt=True))
res['imaplib.Time2Internaldate of an aware datetime'] = w(lambda: imaplib.Time2Internaldate(datetime.datetime(2026, 12, 9, 13, 28, 48, tzinfo=datetime.timezone.utc)))
res['imaplib.Internaldate2tuple'] = w(lambda: imaplib.Internaldate2tuple(b'1 (INTERNALDATE "17-Jul-1996 02:44:25 -0700")')[:6])
res['imaplib.ParseFlags'] = w(lambda: imaplib.ParseFlags(b'1 (FLAGS (\\Seen \\Flagged))'))
# a small SMTP server on sockets: what smtplib sends, as the server sees it
log = []
class H(socketserver.StreamRequestHandler):
    def handle(self):
        w_ = lambda s: (self.wfile.write(s.encode() + b'\r\n'), self.wfile.flush())
        w_('220 local stand-in'); rec = {'cmds': [], 'data': b''}
        while True:
            line = self.rfile.readline()
            if not line: break
            c = line.decode('utf-8', 'replace').strip(); rec['cmds'].append(c); u = c.upper()
            if u.startswith('EHLO'): self.wfile.write(b'250-local stand-in\r\n250-8BITMIME\r\n250 SMTPUTF8\r\n'); self.wfile.flush()
            elif u.startswith('MAIL'): w_('250 OK')
            elif u.startswith('RCPT'): w_('550 no mailbox' if 'refused' in c else '250 OK')
            elif u == 'DATA':
                w_('354 go'); d = b''
                while True:
                    l = self.rfile.readline(); 
                    if l == b'.\r\n' or not l: break
                    d += l
                rec['data'] = d; w_('250 queued')
            elif u == 'QUIT': w_('221 bye'); break
            else: w_('250 OK')
        log.append(rec)
srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); srv.daemon_threads = True; port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
def send(msg, **kw):
    n = len(log); s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    try: r = s.send_message(msg, **kw)
    finally:
        try: s.quit()
        except Exception: pass
    import time
    for _ in range(50):
        if len(log) > n: break
        time.sleep(0.02)
    return r, log[-1] if len(log) > n else None
def bcc():
    m = EmailMessage(); m['From'] = 'al@example.com'; m['To'] = 'jon@example.org'; m['Cc'] = 'friend@example.com'; m['Bcc'] = 'secret@example.com'; m['Subject'] = 's'; m.set_content('b')
    r, rec = send(m); hdr = email.message_from_bytes(rec['data']); return [r, [c for c in rec['cmds'] if c.upper().startswith(('MAIL', 'RCPT'))], hdr['Bcc'], hdr['Cc']]
res['smtplib.send_message: envelope and the Bcc header the server sees'] = w(bcc)
def refused():
    m = EmailMessage(); m['From'] = 'al@example.com'; m['To'] = 'ok@example.org, gone@refused.example'; m['Subject'] = 's'; m.set_content('b'); r, rec = send(m); return [r]
res['smtplib.send_message with one refused recipient'] = w(refused)
def allrefused():
    m = EmailMessage(); m['From'] = 'al@example.com'; m['To'] = 'gone@refused.example'; m['Subject'] = 's'; m.set_content('b'); return send(m)[0]
res['smtplib.send_message with all recipients refused'] = w(allrefused)
def utf8_send():
    m = EmailMessage(); m['From'] = 'al@example.com'; m['To'] = 'ayşe@example.org'; m['Subject'] = 's'; m.set_content('b'); r, rec = send(m); return [r, [c for c in rec['cmds'] if c.upper().startswith(('MAIL', 'RCPT'))]]
res['smtplib.send_message to a non-ASCII address (SMTPUTF8 offered by the server)'] = w(utf8_send)
def nostarttls():
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    try: s.starttls(context=ssl.create_default_context())
    finally: s.close()
res['starttls() on a server that does not offer STARTTLS'] = w(nostarttls)
def noauth():
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    try: s.login('user', 'secret')
    finally: s.close()
res['login() on a server that does not offer AUTH'] = w(noauth)
def badport():
    return smtplib.SMTP('127.0.0.1', 1, timeout=3)
res['connecting to a closed port'] = w(badport)
def mixed_msg():
    m = EmailMessage(); m['From'] = 'a@example.com'; m['To'] = 'b@example.org'; m.set_content('plain'); m.add_alternative('<b>html</b>', subtype='html'); m.add_attachment(b'1234', maintype='application', subtype='octet-stream', filename='x.bin')
    return [p.get_content_type() for p in m.walk()]
res['EmailMessage walk of text + html + attachment'] = w(mixed_msg)
def mime_guess():
    import mimetypes
    return [mimetypes.guess_type(n)[0] for n in ('a.jpg', 'a.mp3', 'a.exe', 'a.zip', 'a.pdf', 'a.docx', 'a.unknownext')]
res['mimetypes.guess_type of seven names'] = w(mime_guess)
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
    json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "_note": "Recorded by sen0414_ch20_interpreters_v1_0_0.py: one program (the standard-library side of e-mail: email, smtplib, imaplib, ssl, email.utils, mimetypes, against a small SMTP server written with sockets inside the program, a local stand-in on 127.0.0.1) under each installed interpreter, in the zone Europe/Istanbul. Python 3.15.0b4 is a beta. The chapter itself uses none of these modules.",
               "program": PROG, "interpreters": list(results), "results": results, "items compared": len(keys), "differ": differ}, open(OUT, "w"), indent=1, ensure_ascii=False)
    print("recorded", len(results), "interpreters;", len(keys), "items; items that differ:", sorted(differ))
