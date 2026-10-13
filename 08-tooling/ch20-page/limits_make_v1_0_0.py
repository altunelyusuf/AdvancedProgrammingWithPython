"""Writes limits_v1_0_0.json, the chapter 20 page's 'Provenance & known limits' entries, from the records Phase A made
(live_observations_v1_0_0.json, interpreter_record_v1_0_0.json, third_party_record_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json
and the 'Not executed' sentence of sen0414_ch20_rdodi_data_v1_0_2.py. Numbers are read from those files. Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
lv, ir, pw, so, tp = J("live_observations_v1_0_0.json"), J("interpreter_record_v1_0_0.json"), J("pywheels_v1_0_0.json"), J("standin_v1_0_0.json"), J("third_party_record_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch20_rdodi_data_v1_0_2.py"), encoding="utf-8").read()
live = {i["what"]: i["saw"] for i in lv["items"]}
find = lambda start: next(v for k, v in live.items() if k.startswith(start))
m = re.search(r"Not executed, and said so where it comes up: (.*?)\.\s+The chapter's 48 interactive statements", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
pg = find("chapter 20 page: status"); mat = find("online materials of the 3rd edition: status")
dns = find("DNS over HTTPS (dns.google/resolve), MX record of every gateway domain")
withmx = sum(1 for k, (st, v) in dns.items() if any(re.match(r"\d+ ", x) for x in v))
assert len(dns) == 18 and withmx == 12, (len(dns), withmx)
tw = find("Twilio REST API without credentials"); nt = find("ntfy.sh health")
rec = so["recorded"]
out = []
out.append("Python and libraries on this page: the examples run in your browser, in Python 3.13.2 with its standard library and Pyodide's ssl package, while the research ran Python 3.14.6 on Linux with ezgmail 2026.4.28, requests 2.34.2 and aiosmtpd 1.4.6 (none of them is on this page). Each concept example and each chapter example was run in the browser and compared with its recorded result.")
out.append("Recorded, not run: %d examples need something a browser's Python cannot give (sockets between programs, a server in a thread, another program, the process time zone) or a library that is not on the page (ezgmail, licence GPLv3+, and Google's client library, a 16.8 MB wheel), or print what Python 3.14 added to imaplib and Python 3.13 does not have; each is shown with its output recorded under Python 3.14.6, labelled 'Recorded, not run on this page', with its reason: %s." % (len(rec), ", ".join(sorted(rec))))
out.append("No real Gmail account, phone, ntfy server or Twilio account was reached, anywhere. Programs of the recording ran against local stand-ins and say so: the real ezgmail and the real Google library against a replacement of Google's HTTP object whose replies were written by the study, a local SMTP server (aiosmtpd) with a self-signed certificate, a local IMAP server (dovecot 2.3.21), a recorder in place of ntfy, a list of messages in place of a mailbox, a sample forecast and a page of HTML written for the course. Their output shows what the libraries send and how the program reacts, not what Gmail, a phone company, ntfy or weather.gov answers.")
out.append("No wheel is embedded on this page and no file of the book's online materials (a zip of %s bytes, none of its files is about this chapter); ezgmail is licensed GPLv3+ and Google's client library is a 16.8 MB wheel, so both are only recorded (03-materials/ch20/assets/ASSETS_PROVENANCE_v1_0_0.md)." % "{:,}".format(mat[1]))
out.append("NOT EXECUTED: " + notexec + ".")
out.append("What the public sites answered on 2026-10-13 is in live_observations_v1_0_0.json: the chapter's page (status %d, %s bytes, equal to the digest in the book's ontology), the notices of AT&T and Verizon, ntfy.sh (health %d, %s; a poll of an unused topic, nothing published), Twilio's API asked once without credentials (status %d) and the DNS answers for the %d gateway domains of Table 20-1, of which %d have mail exchangers (MX records); sms.cricketwireless.net answered only name aliases (CNAME). A missing MX is a symptom, not proof that delivery fails." % (pg[0], "{:,}".format(pg[1]), nt[0], nt[1], tw[0], len(dns), withmx))
out.append("One program was run under %d interpreters (%s); the %d items that differ between them are listed in interpreter_record_v1_0_0.json (for example imaplib's idle() from Python 3.14, the lower case mail from: and rcpt to: that smtplib sends from Python 3.13, the removed keyfile and certfile arguments, and the verify flags of ssl.create_default_context() that Python 3.13 added; its TLS 1.2 minimum is older: 3.11.17 already reports it, the documentation dates it to 3.10, and the Ubuntu 3.12.3 package reports the lowest supported version). The book's Appendix A pins requests 2.32.3; the %d items of the third-party record were run with the newest releases and with that pin." % (len(ir["interpreters"]), ", ".join(ir["interpreters"]), len(ir["differ"]), len(tp["items"])))
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x[:220])
