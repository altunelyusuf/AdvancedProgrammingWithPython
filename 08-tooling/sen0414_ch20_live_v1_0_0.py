#!/usr/bin/env python3
"""Chapter 20 (Sending Email, Texts, and Push Notifications): observes, once, what the public sources the chapter names answer today, what the real
services that can be asked without an account answer, and what real mail software on the machine does, and writes what it saw with the date. A web site changes
and the files of the online materials may be replaced; the record is an observation of the day, not something the build can re-check, and no check reads it.
What it does: fetches the chapter page and compares its SHA-256 with the digest the book's own ontology records; counts what is on the page (listings, figures,
tables, practice questions) and asks every external link of the chapter once without following a redirect; reads Appendix A for the versions the book pins and
Appendix B for the answers to the chapter's five questions; downloads the online materials of the 3rd edition and looks for any file of the chapter; reads the second
edition's chapter 18 for what the chapter replaced; reads the newest releases of ezgmail, requests, aiosmtpd, imapclient, oauth2client and twilio on PyPI; opens every
source of the research record and checks that the passages the research relies on are on the page; asks ntfy.sh for its health (GET) and for one poll of a random,
unused topic (GET, which publishes nothing); asks Twilio's REST API for its account list without credentials (the answer is the refusal); asks a DNS-over-HTTPS resolver
for the MX records of every gateway domain of Table 20-1 and the SPF and DMARC records of gmail.com; asks api.weather.gov for a forecast (the Umbrella Reminder).
On the machine itself it starts a real IMAP server (dovecot 2.3.21, a local stand-in for imap.gmail.com) and a real SMTP server (aiosmtpd, a local stand-in for
smtp.gmail.com), and drives them with smtplib, imaplib (including IDLE, new in Python 3.14) and imapclient, and runs the Email-Based Computer Control program end to end.
NOT EXECUTED and said so: anything that needs a Google account (ezgmail's authorisation, the Gmail API itself, imap.gmail.com and smtp.gmail.com with a login), a phone
number, a carrier gateway delivering a text, a Twilio account, a push to ntfy.sh (nothing is posted to the public service), the ntfy server and apps, Windows, macOS.
Run it with an interpreter that has requests and Beautiful Soup (/home/claude/venv314_web/bin/python); the local part uses CH20_LATEST (/home/claude/venv314_ch20_latest/bin/python).
Usage: sen0414_ch20_live_v1_0_0.py   -> ch20-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, secrets, shutil, subprocess, sys, tempfile, time, zipfile
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch20-page", "live_observations_v1_0_0.json")
UA = {"User-Agent": "SEN0414-research/1.0 (teaching; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
PYTHON = os.environ.get("CH20_LATEST", "/home/claude/venv314_ch20_latest/bin/python")
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:200])
    obs.append({"what": what, "saw": v})
def get(u, **k):
    k.setdefault("headers", BROWSER)
    for attempt in range(6):       # a site that answers 429 (too many requests) or drops the connection is asked again after a pause; the status of the last answer is the one recorded
        try:
            r = requests.get(u, timeout=90, **k)
            if r.status_code != 429: return r
        except requests.ConnectionError:
            if attempt == 5: raise
        time.sleep(20)
    return r
def sha(b): return hashlib.sha256(b).hexdigest()
def norm(t): return re.sub(r"\s+", " ", t)
def visible(r):
    s = bs4.BeautifulSoup(r.text, "html.parser")
    for x in s(["script", "style"]): x.decompose()
    return norm(s.get_text(" "))
SOURCES = [
    ('P01', 'https://automatetheboringstuff.com/3e/chapter20.html', ['EZGmail', 'ntfy', 'Table 20-1', 'Umbrella Reminder', 'Auto Unsubscriber', 'Email-Based Computer Control', '250 messages per day', '4,096 bytes']),
    ('P02', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', []),
    ('P03', 'https://automatetheboringstuff.com/3e/', ['Sending Email, Texts, and Push Notifications']),
    ('P04', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', ['Sending Email, Texts, and Push Notifications']),
    ('P05', 'https://automatetheboringstuff.com/3e/appendixa.html', ['requests==2.32.3', 'ezgmail']),
    ('P06', 'https://automatetheboringstuff.com/3e/appendixb.html', ['has:attachment', 'ntfy', 'credentials.json']),
    ('P07', 'https://automatetheboringstuff.com/2e/chapter18/', ['smtplib', 'imapclient', 'pyzmail', 'Twilio']),
    ('P08', 'https://raw.githubusercontent.com/asweigart/ezgmail/master/README.md', ['credentials.json', 'token.json']),
    ('P09', 'https://pypi.org/pypi/ezgmail/json', ['ezgmail']),
    ('P10', 'https://pypi.org/pypi/requests/json', ['requests']),
    ('P11', 'https://pypi.org/pypi/aiosmtpd/json', ['aiosmtpd']),
    ('P12', 'https://pypi.org/pypi/imapclient/json', ['imapclient']),
    ('P13', 'https://pypi.org/pypi/oauth2client/json', ['oauth2client']),
    ('P14', 'https://aiosmtpd.aio-libs.org/en/latest/', ['aiosmtpd', 'STARTTLS']),
    ('P15', 'https://docs.ntfy.sh/publish/', ['250', '4,096', 'Priority', 'Tags', 'Title']),
    ('P16', 'https://docs.ntfy.sh/subscribe/api/', ['poll=1', 'since', 'keepalive', 'poll_request', 'message_delete', 'message_clear']),
    ('P17', 'https://docs.ntfy.sh/config/', ['message-size-limit', 'visitor-request-limit']),
    ('P18', 'https://docs.ntfy.sh/faq/', ['topic']),
    ('P19', 'https://ntfy.sh/v1/health', ['healthy']),
    ('P20', 'https://docs.python.org/3.14/library/smtplib.html', ['STARTTLS', 'send_message', 'sendmail', 'SMTPUTF8', 'SMTP_SSL']),
    ('P21', 'https://docs.python.org/3.14/library/imaplib.html', ['IMAP4_SSL', 'idle', 'Internaldate2tuple', 'authenticate']),
    ('P22', 'https://docs.python.org/3.14/library/email.message.html', ['EmailMessage', 'iter_attachments', 'add_attachment', 'get_body']),
    ('P23', 'https://docs.python.org/3.14/library/email.policy.html', ['max_line_length', 'SMTPUTF8', 'compat32']),
    ('P24', 'https://docs.python.org/3.14/library/email.mime.html', ['MIMEText', 'MIMEMultipart']),
    ('P25', 'https://docs.python.org/3.14/library/email.utils.html', ['parseaddr', 'getaddresses', 'strict', 'make_msgid', 'formatdate']),
    ('P26', 'https://docs.python.org/3.14/library/email.header.html', ['decode_header', 'make_header']),
    ('P27', 'https://docs.python.org/3.14/library/ssl.html', ['create_default_context', 'check_hostname', 'PROTOCOL_TLS_CLIENT']),
    ('P28', 'https://docs.python.org/3.14/library/mimetypes.html', ['guess_type']),
    ('P29', 'https://docs.python.org/3.14/whatsnew/3.14.html', ['imaplib', 'IDLE']),
    ('P30', 'https://docs.python.org/3.13/whatsnew/3.13.html', ['imghdr', 'sndhdr']),
    ('P31', 'https://docs.python.org/3.12/whatsnew/3.12.html', ['smtpd', 'aiosmtpd']),
    ('P32', 'https://docs.python.org/3.15/whatsnew/3.15.html', ['email']),
    ('P33', 'https://peps.python.org/pep-0594/', ['smtpd', 'imghdr', 'sndhdr', 'aiosmtpd']),
    ('P34', 'https://www.rfc-editor.org/rfc/rfc5321', ['RCPT TO', '8BITMIME']),
    ('P35', 'https://www.rfc-editor.org/rfc/rfc5322', ['998 characters', '78 characters', 'Bcc', 'Message-ID']),
    ('P36', 'https://www.rfc-editor.org/rfc/rfc2045', ['quoted-printable', 'base64', '7bit']),
    ('P37', 'https://www.rfc-editor.org/rfc/rfc2047', ['encoded-word']),
    ('P38', 'https://www.rfc-editor.org/rfc/rfc3501', ['SELECT', 'FETCH', 'STARTTLS', 'LOGINDISABLED']),
    ('P39', 'https://www.rfc-editor.org/rfc/rfc3207', ['STARTTLS']),
    ('P40', 'https://www.rfc-editor.org/rfc/rfc8314', ['Implicit TLS', '465']),
    ('P41', 'https://www.rfc-editor.org/rfc/rfc4954', ['AUTH']),
    ('P42', 'https://www.rfc-editor.org/rfc/rfc2369', ['List-Unsubscribe', 'mailto']),
    ('P43', 'https://www.rfc-editor.org/rfc/rfc8058', ['One-Click', 'List-Unsubscribe-Post']),
    ('P44', 'https://www.rfc-editor.org/rfc/rfc7208', ['Sender Policy Framework']),
    ('P45', 'https://www.rfc-editor.org/rfc/rfc7489', ['DMARC']),
    ('P46', 'https://www.rfc-editor.org/rfc/rfc2177', ['IDLE']),
    ('P47', 'https://www.rfc-editor.org/rfc/rfc821', ['SIMPLE MAIL TRANSFER PROTOCOL']),
    ('P48', 'https://developers.google.com/identity/protocols/oauth2', ['7 days', 'Testing']),
    ('P49', 'https://developers.google.com/workspace/gmail/api/guides/sending', ['base64url', 'The Subject headers match', 'In-Reply-To', 'References', 'raw']),
    ('P50', 'https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/send', ['raw', 'mail.google.com']),
    ('P51', 'https://developers.google.com/workspace/gmail/api/auth/scopes', ['https://mail.google.com/', 'gmail.send', 'gmail.readonly']),
    ('P52', 'https://developers.google.com/workspace/gmail/api/reference/quota', ['quota units', 'messages.send', 'threads.list']),
    ('P53', 'https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.threads/list', ['maxResults', '500']),
    ('P54', 'https://support.google.com/mail/answer/7190', ['has:attachment', 'label:', 'from:']),
    ('P55', 'https://support.google.com/mail/answer/6590', ['.exe']),
    ('P56', 'https://support.google.com/mail/answer/6584', ['25 MB']),
    ('P57', 'https://support.google.com/a/answer/81126', ['5,000', 'SPF', 'DKIM', 'DMARC']),
    ('P58', 'https://www.att.com/support/article/wireless/KM1061254/', ['June 17', '2025']),
    ('P59', 'https://www.verizon.com/support/vtext-vzwpix-shutdown/', ['vtext', 'vzwpix', '2027']),
    ('P60', 'https://www.twilio.com/docs/glossary/what-is-gsm-7-character-encoding', ['GSM-7', '160', 'UCS-2']),
    ('P61', 'https://www.twilio.com/docs/messaging/api/message-resource', ['Message resource']),
    ('P62', 'https://www.twilio.com/docs/messaging/compliance/a2p-10dlc', ['10DLC']),
    ('P63', 'https://www.weather.gov/documentation/services-web-api', ['api.weather.gov', 'User-Agent']),
    ('P64', 'https://en.wikipedia.org/wiki/Ray_Tomlinson', ['1971']),
    ('P65', 'https://en.wikipedia.org/wiki/Email_spam', ['Thuerk', '1978']),
    ('P66', 'https://en.wikipedia.org/wiki/SMS', ['Papworth', 'Merry Christmas', '1992', '160']),
    ('P67', 'https://en.wikipedia.org/wiki/Gmail', ['April 1, 2004', 'Paul Buchheit']),
    ('P68', 'https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol', ['Postel', 'RFC 821']),
    ('P69', 'https://developers.google.com/workspace/gmail/imap/imap-smtp', ['imap.gmail.com', 'smtp.gmail.com', 'OAuth']),
    ('P70', 'https://developers.google.com/workspace/gmail/imap/xoauth2-protocol', ['XOAUTH2', 'auth=Bearer']),
    ('P71', 'https://docs.astral.sh/uv/concepts/python-versions/', ['uv python install']),
    ('P72', 'https://www.python.org/downloads/', ['Python 3.14']),
]
def sources():
    out = []
    for pid, url, phrases in SOURCES:
        try:
            r = get(url, headers=BROWSER if "nostarch.com" in url else UA); ctype = r.headers.get("content-type", "")
            if "zip" in ctype or url.endswith(".zip"): t = ""
            else:
                t = r.content.decode("utf-8", "replace")
                if "html" in ctype:
                    s = bs4.BeautifulSoup(t, "html.parser")
                    for x in s(["script", "style"]): x.decompose()
                    t = s.get_text(" ")
            t = norm(t).replace("’", "'")
            out.append([pid, r.status_code, len(r.content), {p: (norm(p).replace("’", "'").lower() in t.lower()) for p in phrases}])
        except Exception as e: out.append([pid, "unreachable: %s" % type(e).__name__, 0, {}])
    return out

# 0. the chapter and the book's own record of it
ch = get("https://automatetheboringstuff.com/3e/chapter20.html", headers=UA)
DIGEST = "584483b8c1b41f45076a8a64d97c6afd680904246fc605b21d0f405724a09967"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch20_v1_0_0.ttl"
see("chapter 20 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not present"])
soup = bs4.BeautifulSoup(ch.text, "html.parser"); text = norm(soup.get_text(" "))
see("chapter 20 page: number of listings (pre elements), figure captions, tables, images and the HTTP status of each image file", lambda: [len(soup.find_all("pre")), sorted(set(re.findall(r"Figure 20-\d+", text))), sorted(set(re.findall(r"Table 20-\d+", text))), len(soup.find_all("table")), [(i["src"], get("https://automatetheboringstuff.com/3e/" + i["src"] if not i["src"].startswith("http") else i["src"], headers=UA).status_code) for i in soup.find_all("img") if i.get("src") and "cover" not in i["src"]]])
see("chapter 20 page: alt text of the pictures", lambda: [i.get("alt") for i in soup.find_all("img") if i.get("src") and "cover" not in i["src"]])
see("chapter 20 page: the headings of the chapter in order", lambda: [(h.name, norm(h.get_text())) for h in soup.find_all(["h2", "h3", "h4", "h5"])])
STATEMENTS = ("EZGmail", "Table 20-1", "160 characters", "250 messages per day", "4,096 bytes", "/json?poll=1", "since=10m", "'poll_request'", "2026 -12-20 21:28:32", "Treat this topic name as a password",
              "AlSweigartZPgxBQ42", "Umbrella Reminder", "Auto Unsubscriber", "Email-Based Computer Control", "Twilio", "it is fairly trivial for hackers to fake a")
see("chapter 20 page: statements the research relies on (each is on the page of the book: True)", lambda: {s: (norm(s) in text) for s in STATEMENTS})
see("chapter 20 page: words the chapter never uses although the topic needs them (False means absent from the page)", lambda: {s: s.lower() in text.lower() for s in ("smtplib", "imaplib", "STARTTLS", "OAuth", "scope", "refresh", "app password", "HTML", "UTF-8", "unsubscribe", "SPF", "DKIM", "DMARC", "attachment", "Reply-To", "Message-ID", "TLS", "SSL", "encoding", "latin", "timeout", "raise_for_status", "status_code", "token.json", "credentials.json")})
ext = sorted({a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http") and "automatetheboringstuff.com" not in a["href"]})
def link_status():
    out = []
    for u in ext:
        try:
            r = requests.get(u, timeout=60, headers=BROWSER, allow_redirects=False); out.append([u, r.status_code, r.headers.get("Location", "")[:100]])
        except Exception as e: out.append([u, "unreachable: %s" % type(e).__name__, ""])
    return out
see("chapter 20 page: every external link of the chapter, asked once without following a redirect: URL, HTTP status, Location", link_status)
see("chapter 20 page: every URL that appears in the text of the chapter", lambda: sorted({u.rstrip(".,)") for u in re.findall(r"https?://[\w./?=&#%~:+-]+", text) if "automatetheboringstuff.com/3e/chapter20" not in u}))
def appendix():
    a = get("https://automatetheboringstuff.com/3e/appendixa.html", headers=UA); t = visible(a)
    return [a.status_code, re.findall(r"(?:ezgmail|requests|pyperclip|beautifulsoup4|ntfy)\s*[=~<>]+\s*[\w.]+", t), "requests==2.32.3" in t, "ezgmail" in t, re.findall(r"ezgmail[^.]{0,80}", t)[:3]]
see("Appendix A of the book: status, the pins of the packages chapter 20 names, whether requests is pinned to 2.32.3, whether ezgmail is listed and with what text", appendix)
def appendixb():
    a = get("https://automatetheboringstuff.com/3e/appendixb.html", headers=UA); t = visible(a)
    i = t.find("Chapter 20 1."); j = t.find("Chapter 21", i)
    return [a.status_code, t[i:j][:1500]]
see("Appendix B of the book: the answers printed for the five questions of chapter 20", appendixb)
def bookpage():
    r = get("https://nostarch.com/automate-boring-stuff-python-3rd-edition"); t = visible(r)
    links = [a["href"] for a in bs4.BeautifulSoup(r.text, "html.parser").find_all("a", href=True) if re.search(r"zip|download|code|github", a["href"], re.I)]
    return [r.status_code, len(r.content), {w: len(re.findall(w, t, re.I)) for w in ("Sending Email", "example implementation", "Email-Based", "ezgmail", "ntfy")}, links[:8]]
see("the book page at nostarch.com that chapter 20 points to for 'an example implementation': how often words occur on the page, and the download links on it", bookpage)
mat = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip")
see("online materials of the 3rd edition: status, bytes, SHA-256 of the zip", lambda: [mat.status_code, len(mat.content), sha(mat.content)])
def materials():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); names = [n for n in z.namelist() if not n.endswith("/") and "__MACOSX" not in n and not n.split("/")[-1].startswith("._")]
    texts = {n.split("/")[-1]: z.read(n).decode("utf-8", "replace") for n in names if n.endswith(".py")}
    hits = lambda pat: sorted(k for k, v in texts.items() if re.search(pat, v))
    return {"files": len(names), "python files": len(texts), "files named for the chapter's programs": [n for n in names if re.search(r"umbrella|unsubscrib|emailcontrol|ezgmail|ntfy|gmail", n, re.I)],
            "python files that mention ezgmail": hits(r"ezgmail"), "python files that mention ntfy": hits(r"ntfy"), "python files that import smtplib or imaplib": hits(r"import\s+(smtplib|imaplib)"), "python files that mention twilio": hits(r"(?i)twilio"),
            "python files that mention weather.gov": hits(r"weather\.gov"), "phoneAndEmail.py (the file of chapter 8) and what it holds": [bool(texts.get("phoneAndEmail.py")), (texts.get("phoneAndEmail.py", "")[:200])]}
see("online materials: the files (without the macOS resource forks), and whether any file in them is about the programs or modules of chapter 20", materials)
def second_edition():
    r = get("https://automatetheboringstuff.com/2e/chapter18/", headers=UA); t = visible(r)
    return [r.status_code, {w: len(re.findall(w, t)) for w in ("smtplib", "imapclient", "pyzmail", "Twilio", "SMTP", "IMAP", "app password", "STARTTLS", "SMTP_SSL", "ezgmail")}, re.findall(r"\bsmtp[\w.]*gmail\.com", t)[:2]]
see("the second edition's chapter 18 (Sending Email and Text Messages), which this chapter replaced: how often each name occurs on the page", second_edition)
def pypi():
    out = {}
    for n in ("ezgmail", "requests", "aiosmtpd", "imapclient", "oauth2client", "twilio", "google-api-python-client"):
        j = get("https://pypi.org/pypi/%s/json" % n, headers=UA).json(); i = j["info"]; rel = j["releases"].get(i["version"], [])
        out[n] = {"version": i["version"], "uploaded": rel[0]["upload_time"][:10] if rel else None, "requires_python": i["requires_python"], "requires_dist": sorted((i["requires_dist"] or []))[:12], "development status": [c for c in i["classifiers"] if "Development Status" in c], "yanked": bool(rel and rel[0].get("yanked"))}
    return out
see("PyPI: the newest release, its upload date, Requires-Python, dependencies and development status of ezgmail, requests, aiosmtpd, imapclient, oauth2client, twilio and google-api-python-client", pypi)
see("sources of the research record: for each, the HTTP status, the bytes, and whether each passage the research relies on is on the page", sources)

# 1. services that can be asked without an account
see("ntfy.sh health: GET https://ntfy.sh/v1/health (status, body)", lambda: (lambda r: [r.status_code, r.text.strip(), r.headers.get("content-type")])(get("https://ntfy.sh/v1/health", headers=UA)))
TOPIC = "sen0414poll" + secrets.token_hex(8)
see("ntfy.sh poll of a random, unused topic (GET only, nothing is published): status, the body, and the headers a client may rely on", lambda: (lambda r: [r.status_code, r.text, r.headers.get("content-type"), {k: v for k, v in r.headers.items() if k.lower().startswith(("access-control", "x-", "cache"))}])(get("https://ntfy.sh/%s/json?poll=1" % TOPIC, headers=UA)))
see("ntfy.sh poll of a random topic with since=10m and since=all, as the chapter describes: statuses and bodies", lambda: [(lambda r: [r.status_code, r.text])(get("https://ntfy.sh/%s/json?poll=1&since=%s" % (TOPIC, s), headers=UA)) for s in ("10m", "all", "1737866912")])
see("Twilio REST API without credentials: GET https://api.twilio.com/2010-04-01/Accounts.json (status, body, the WWW-Authenticate header)", lambda: (lambda r: [r.status_code, r.text[:300], r.headers.get("WWW-Authenticate")])(get("https://api.twilio.com/2010-04-01/Accounts.json", headers=UA)))
def doh(name, typ):
    r = get("https://dns.google/resolve", params={"name": name, "type": typ}, headers={"accept": "application/dns-json", **UA}); j = r.json()
    return [j.get("Status"), [a["data"] for a in j.get("Answer", [])][:5]]
GATEWAYS = ["txt.att.net", "mms.att.net", "sms.myboostmobile.com", "sms.cricketwireless.net", "mms.cricketwireless.net", "msg.fi.google.com", "mymetropcs.com", "text.republicwireless.com", "messaging.sprintpcs.com", "pm.sprint.com", "tmomail.net",
            "email.uscc.net", "mms.uscc.net", "vtext.com", "vzwpix.com", "vmobl.com", "vmpix.com", "mypixmessages.com"]
see("DNS over HTTPS (dns.google/resolve), MX record of every gateway domain of Table 20-1: DNS status (0 = NOERROR, 3 = NXDOMAIN) and the mail exchangers", lambda: {d: doh(d, "MX") for d in GATEWAYS})
see("DNS over HTTPS: MX of gmail.com, the SPF record (TXT of gmail.com) and the DMARC record (TXT of _dmarc.gmail.com)", lambda: {"MX gmail.com": doh("gmail.com", "MX"), "TXT gmail.com": [x for x in doh("gmail.com", "TXT")[1] if "spf" in x], "TXT _dmarc.gmail.com": doh("_dmarc.gmail.com", "TXT"), "MX ntfy.sh": doh("ntfy.sh", "MX")})
def weather():
    p = get("https://api.weather.gov/points/41.8781,-87.6298", headers={**UA, "Accept": "application/geo+json"}); j = p.json(); fu = j["properties"]["forecast"]
    f = get(fu, headers={**UA, "Accept": "application/geo+json"}); per = f.json()["properties"]["periods"]
    return {"points status": p.status_code, "forecast url": fu, "forecast status": f.status_code, "period keys": sorted(per[0]), "first period": {k: per[0][k] for k in ("name", "shortForecast", "probabilityOfPrecipitation")}, "periods": len(per),
            "short forecasts": [x["shortForecast"] for x in per[:6]], "precipitation values": [x["probabilityOfPrecipitation"]["value"] for x in per[:6]]}
see("api.weather.gov (the Umbrella Reminder practice program): the point lookup for Chicago, the forecast, the keys of a period and the precipitation chance", weather)

# 2. real mail software on the machine (local stand-ins)
LOCAL_SRC = r"""# runs under the LATEST interpreter (python 3.14.6 with ezgmail, aiosmtpd, imapclient, cryptography); prints a JSON list of [what, saw]
import sys, json, os, io, ssl, time, socket, threading, smtplib, imaplib, subprocess, hmac, email, datetime, tempfile, shutil, ipaddress, importlib.metadata as md
from email import policy
from email.message import EmailMessage
sys.path.insert(0, os.environ['DV_DIR'])
import dovecot_stand_in as dv
obs = []
def see(what, f):
    try: v = f()
    except BaseException as e: v = 'raised %s: %s' % (type(e).__name__, str(e)[:200])
    obs.append([what, v])
proc, root, p1, p2, cp, rc, derr = dv.start()
ctx = ssl.create_default_context(cafile=cp)
see('dovecot (the real IMAP server, a local stand-in for imap.gmail.com): version and whether doveconf accepts the configuration; it listens on 127.0.0.1 only, a self-signed certificate, one user', lambda: [subprocess.run(['dovecot', '--version'], capture_output=True, text=True).stdout.strip(), rc, derr])
def imap_conn():
    m = imaplib.IMAP4('127.0.0.1', p1); m.starttls(ssl_context=ctx); m.login('user', 'secret'); return m
see('imaplib over STARTTLS to dovecot: capability before STARTTLS, STARTTLS answer, LOGIN, SELECT of an empty INBOX, LIST', lambda: (lambda m: [m.capability()[1][0].decode(), m.starttls(ssl_context=ctx)[0], m.login('user', 'secret')[1][0].decode(), m.select()[1][0].decode(), m.list()[1]])(imaplib.IMAP4('127.0.0.1', p1)))
see('imaplib to dovecot with a wrong password: the exception and its text', lambda: (lambda m: (m.starttls(ssl_context=ctx), (lambda: m.login('user', 'wrong'))))(imaplib.IMAP4('127.0.0.1', p1))[1]())
def smtp_to_imap():
    import asyncio
    from aiosmtpd.controller import Controller
    from aiosmtpd.smtp import AuthResult, LoginPassword
    got = []
    class H:
        async def handle_DATA(self, server, session, envelope):
            m = imap_conn(); r = m.append('INBOX', None, None, envelope.original_content); m.logout()
            got.append([envelope.mail_from, list(envelope.rcpt_tos), r[0], bool(session.authenticated)]); return '250 delivered to the local IMAP INBOX'
    def authn(server, session, envelope, mechanism, data):
        ok = isinstance(data, LoginPassword) and data.login == b'user' and data.password == b'secret'; return AuthResult(success=ok, handled=ok)
    from cryptography import x509
    sc = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER); sc.load_cert_chain(root + '/c.pem', root + '/k.pem')
    c = Controller(H(), hostname='127.0.0.1', port=dv.free_port(), tls_context=sc, authenticator=authn, auth_required=True, auth_require_tls=True)
    c.start(); return c, got
c, got = smtp_to_imap()
def send(subj, body, frm='me@example.com'):
    m = EmailMessage(); m['From'] = frm; m['To'] = 'user@localhost'; m['Subject'] = subj; m['Date'] = email.utils.formatdate(1797000528, usegmt=True); m.set_content(body)
    s = smtplib.SMTP('127.0.0.1', c.port, timeout=10); s.ehlo(); s.starttls(context=ctx); s.ehlo(); s.login('user', 'secret'); r = s.send_message(m); s.quit(); return r
see('smtplib (STARTTLS, LOGIN) to a local aiosmtpd, which hands the message to dovecot by IMAP APPEND: send_message result and what the SMTP handler recorded', lambda: (lambda r: [r, list(got)])(send('RoboCop', 'Do you want to watch RoboCop this weekend?')))
def read_back():
    m = imap_conn(); m.select()
    a = m.search(None, 'UNSEEN'); peek = m.fetch('1', '(FLAGS BODY.PEEK[HEADER.FIELDS (SUBJECT)])'); flags1 = m.fetch('1', '(FLAGS)')[1]
    full = m.fetch('1', '(RFC822)'); flags2 = m.fetch('1', '(FLAGS)')[1]
    msg = email.message_from_bytes(full[1][0][1], policy=policy.default)
    u = m.uid('SEARCH', None, 'ALL'); st = m.store('1', '+FLAGS', '\\Deleted'); ex = m.expunge(); left = m.search(None, 'ALL'); m.logout()
    return {'UNSEEN before': a[1], 'peek keeps unseen': [x.decode() if isinstance(x, bytes) else x for x in flags1], 'flags after RFC822 fetch': [x.decode() if isinstance(x, bytes) else x for x in flags2], 'subject': msg['subject'], 'body': msg.get_content().strip(),
            'uid search': u[1], 'store': [x.decode() for x in st[1]], 'expunge': ex[1], 'ALL after expunge': left[1]}
see('imaplib: SEARCH UNSEEN, FETCH with BODY.PEEK (flags stay), FETCH RFC822 (sets \\Seen), parse with the email package, STORE \\Deleted, EXPUNGE (the delete step of the Email-Based Computer Control program)', read_back)
def idle_test():
    m = imap_conn(); m.select(); ev = []
    t = threading.Timer(1.0, lambda: send('while idle', 'x')); t.start()
    with m.idle(duration=6) as idler:
        for typ, data in idler:
            ev.append([typ, data]); 
            if typ == 'EXISTS': break
    m.logout(); t.join(); return {'imaplib.IMAP4.idle exists': hasattr(imaplib.IMAP4, 'idle'), 'events': ev}
see('imaplib.IMAP4.idle() (new in Python 3.14, RFC 2177) against dovecot while a message arrives one second later', idle_test)
def imapclient_test():
    import imapclient
    ic = imapclient.IMAPClient('127.0.0.1', port=p1, ssl=False); ic.starttls(ssl_context=ctx); ic.login('user', 'secret'); ic.select_folder('INBOX')
    ids = ic.search(['UNSEEN']); f = ic.fetch(ids, ['ENVELOPE', 'FLAGS']); env = f[ids[0]][b'ENVELOPE']
    r = {'imapclient': md.version('imapclient'), 'search UNSEEN': ids, 'envelope subject': env.subject.decode(), 'from': str(env.from_[0]), 'flags': [x.decode() for x in f[ids[0]][b'FLAGS']], 'capabilities has IDLE': ic.has_capability('IDLE')}
    ic.delete_messages(ids); ic.expunge(); r['after'] = ic.search(['ALL']); ic.logout(); return r
see('imapclient 4.1.0 (the library the second edition used) against dovecot: search, fetch of the envelope, delete and expunge', imapclient_test)
def control_loop():
    SECRET = 'correct horse'; ALLOW = {'noop': [sys.executable, '-c', 'pass'], 'say': [sys.executable, '-c', 'print(1)']}; done = []
    send('noop', 'correct horse:noop', frm='me@example.com'); send('guess', 'wrong:noop', frm='x@example.net'); send('rm', 'correct horse:rm', frm='me@example.com')
    m = imap_conn(); m.select(); typ, ids = m.search(None, 'UNSEEN')
    for i in ids[0].split():
        msg = email.message_from_bytes(m.fetch(i, '(RFC822)')[1][0][1], policy=policy.default); body = msg.get_content().strip(); pw, _, cmd = body.partition(':')
        if not hmac.compare_digest(pw.encode(), SECRET.encode()): done.append([msg['from'], 'bad password'])
        elif cmd not in ALLOW: done.append([msg['from'], 'refused ' + cmd])
        else: done.append([msg['from'], cmd, subprocess.Popen(ALLOW[cmd]).wait()])
        m.store(i, '+FLAGS', '\\Deleted')
    m.expunge(); left = m.search(None, 'ALL')[1]; m.logout(); return {'handled': done, 'left in INBOX': left}
see('the Email-Based Computer Control program end to end on local stand-ins: three messages arrive by SMTP, the loop reads them by IMAP, checks the password with hmac.compare_digest, runs only an allowed command with Popen and wait, deletes what it read', control_loop)
c.stop()
def tcp():
    out = []
    for h, p in (('imap.gmail.com', 993), ('smtp.gmail.com', 587), ('smtp.gmail.com', 465)):
        try:
            so = socket.create_connection((h, p), timeout=10); so.settimeout(10)
            banner = so.recv(100).decode('ascii', 'replace').strip() if p == 587 else 'connected'; so.close(); out.append([h, p, banner])
        except OSError as e: out.append([h, p, 'raised %s: %s' % (type(e).__name__, str(e)[:120])])
    return out
see('TCP connection (no login, nothing sent) to the real Gmail servers named in Google documentation, 10 second timeout: imap.gmail.com:993, smtp.gmail.com:587 (banner read), smtp.gmail.com:465', tcp)
proc.terminate()
try: proc.wait(10)
except Exception: proc.kill()
print(json.dumps(obs, default=lambda o: o.decode('utf-8', 'replace') if isinstance(o, bytes) else repr(o)))
"""
DOVECOT_SRC = r"""import os, shutil, subprocess, tempfile, time, socket, datetime, ipaddress
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p
def start(root=None):
    root = root or tempfile.mkdtemp(prefix='dv'); os.chmod(root, 0o755); os.makedirs(root + '/run', exist_ok=True); os.makedirs(root + '/mail', exist_ok=True)
    key = ec.generate_private_key(ec.SECP256R1()); nm = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'localhost')]); t0 = datetime.datetime(2026, 1, 1)
    crt = (x509.CertificateBuilder().subject_name(nm).issuer_name(nm).public_key(key.public_key()).serial_number(1).not_valid_before(t0).not_valid_after(t0 + datetime.timedelta(days=3650))
           .add_extension(x509.SubjectAlternativeName([x509.DNSName('localhost'), x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]), critical=False).sign(key, hashes.SHA256()))
    open(root + '/c.pem', 'wb').write(crt.public_bytes(serialization.Encoding.PEM)); open(root + '/k.pem', 'wb').write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    shutil.chown(root + '/mail', 'dovecot', 'dovecot')
    open(root + '/users', 'w').write('user:{PLAIN}secret\n')
    p1, p2 = free_port(), free_port()
    open(root + '/dovecot.conf', 'w').write(f'''protocols = imap
listen = 127.0.0.1
base_dir = {root}/run
log_path = {root}/dovecot.log
mail_location = maildir:{root}/mail/%u
mail_uid = dovecot
mail_gid = dovecot
first_valid_uid = 100
disable_plaintext_auth = yes
auth_mechanisms = plain login
ssl = required
ssl_cert = <{root}/c.pem
ssl_key = <{root}/k.pem
passdb {{
  driver = passwd-file
  args = scheme=PLAIN username_format=%u {root}/users
}}
userdb {{
  driver = static
  args = uid=dovecot gid=dovecot home={root}/mail/%u
}}
service imap-login {{
  inet_listener imap {{
    port = {p1}
  }}
  inet_listener imaps {{
    port = {p2}
  }}
}}
namespace inbox {{
  inbox = yes
}}
''')
    chk = subprocess.run(['doveconf', '-c', root + '/dovecot.conf', '-n'], capture_output=True, text=True)
    proc = subprocess.Popen(['dovecot', '-F', '-c', root + '/dovecot.conf'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for _ in range(50):
        try: socket.create_connection(('127.0.0.1', p1), timeout=0.5).close(); break
        except OSError: time.sleep(0.2)
    return proc, root, p1, p2, root + '/c.pem', chk.returncode, chk.stderr[:200]
"""
def local():
    d = tempfile.mkdtemp(); open(os.path.join(d, "dovecot_stand_in.py"), "w").write(DOVECOT_SRC); open(os.path.join(d, "live_local.py"), "w").write(LOCAL_SRC)
    r = subprocess.run([PYTHON, os.path.join(d, "live_local.py")], capture_output=True, text=True, env={**os.environ, "DV_DIR": d}, timeout=300)
    if r.returncode: return [["local stand-ins failed", r.stderr[-800:]]]
    return [{"what": w, "saw": s} for w, s in json.loads(r.stdout.strip().splitlines()[-1])]
try: obs.extend(local())
except Exception as e: obs.append({"what": "local stand-ins", "saw": "raised %s: %s" % (type(e).__name__, str(e)[:200])})

json.dump({"_version": __version__, "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s" % (requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names; two GET requests to ntfy.sh (health and a poll of a random unused topic, which publishes nothing); one GET to Twilio's API without credentials; DNS over HTTPS queries; and experiments with real mail software on the build machine (dovecot as IMAP server and aiosmtpd as SMTP server, both labelled local stand-ins for Gmail's servers, bound to 127.0.0.1 with self-signed certificates). Nothing was sent to any person, phone or push service, no account was used, and a connection attempt to Gmail's servers (no login) is recorded as the machine answered it. Not executed: anything needing a Google account, a phone number, a carrier, a Twilio account, a push to ntfy.sh, Windows or macOS.",
           "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print(len(obs), "observations ->", OUT)
