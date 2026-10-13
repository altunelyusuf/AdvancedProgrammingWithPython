"""Chapter 20 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter was read on automatetheboringstuff.com on 2026-10-13 (an HTTP fetch of https://automatetheboringstuff.com/3e/chapter20.html;
the page returned 200, 53,147 bytes, and its sha256, 584483b8c1b41f45076a8a64d97c6afd680904246fc605b21d0f405724a09967, equals the chapterDigest the
book's own chapter ontology records; the commit the course pins was not opened). The online materials of the 3rd edition (the zip No Starch Press
links from its book page, 7,759,877 bytes, sha256 dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916, 91 files) were downloaded and searched:
no file is about chapter 20 (none names ezgmail, ntfy, smtplib, imaplib, twilio or weather.gov), and neither the zip nor any file is kept in this repository.
The book page that the chapter names for an example implementation of the last practice program holds none, so the study built the practice programs
from the chapter's own text and says so where it matters. 72 sources (the chapter, its appendices, the 2nd edition's chapter 18, the EZGmail README, PyPI,
the Python 3.14 documentation of smtplib, imaplib, email and ssl, the RFCs, the Gmail API and help pages, the ntfy documentation, the notices of AT&T and Verizon,
the Twilio and National Weather Service pages, the pages of the stories, uv and python.org) were each fetched on the same day and answered HTTP 200; the passages the
research relies on were looked for on each page (live observations). Every behaviour was executed under Python 3.14.6 (the newest 3.14 release uv offered)
installed with uv on Ubuntu 24.04 (Linux; the zone of the shell Europe/Istanbul) in dedicated environments: ezgmail 2026.4.28 with requests 2.34.2,
google-api-python-client 2.201.0, oauth2client 4.1.3, aiosmtpd 1.4.6, imapclient 4.1.0 and cryptography; the Requests 2.32.3 that Appendix A pins; and an
empty environment. The real servers named in the chapter were never used. The stand-ins are labelled where they appear: the Gmail API is a replacement of httplib2 that
returns replies written by this study, so the real ezgmail and the real Google client library run against it; the SMTP server is aiosmtpd with a self-signed
certificate on 127.0.0.1; the IMAP server is dovecot 2.3.21 on 127.0.0.1; and ntfy is a recorder on 127.0.0.1 that is not ntfy.
Not executed, and said so where it comes up: any Gmail account, Google Cloud project, OAuth consent screen, browser authorisation or token refresh (so the 7-day
expiry of a Testing refresh token, the acceptance of .exe and .zip attachments by Gmail and the behaviour of a real inbox are read, not run); a connection to
Gmail's servers (imap.gmail.com and smtp.gmail.com timed out from this machine); any text message (no phone number, carrier, gateway delivery or Twilio account;
Twilio's API was only asked once without credentials and answered 401); any publication to ntfy.sh, the ntfy app and the real ntfy server (github.com answered
403 and archive.heckel.io was denied, so no ntfy binary; ntfy.sh was only asked for its health and for the messages of an unused topic); Windows and macOS (the
Popen of qBittorrent and a torrent download); the 153 and 67 character segments of long texts, which come from arithmetic and were not found on a page opened by
this study; Python 3.14.7 and later and the final 3.15.0 (uv offered 3.15.0b4); the commit the course pins; and a photograph (the single request to Wikimedia
Commons answered 429).
The chapter's 48 interactive statements are replayed by sen0414_ch20_thirdparty_v1_0_0.py into 08-tooling/ch20-page/third_party_record_v1_0_0.json;
what the public sites and the shipped files did on the day, and what the local stand-in servers did, is in ch20-page/live_observations_v1_0_0.json; what one program
printed under eleven interpreters (3.11, 3.12, 3.13, the seven 3.14 releases 3.14.0 to 3.14.6 and 3.15.0b4) is in ch20-page/interpreter_record_v1_0_0.json.
A claim not in this file was not made."""
__version__ = "1.0.1"
# 1.0.0 of the chapter 20 data module is already committed (the earlier build of the chapter); this version rebuilds the chapter at the standard of
# chapters 13 to 19: two cross-referenced paragraphs per section, the chapter replayed as printed, the real ezgmail, smtplib, imaplib and requests
# run against labelled local stand-ins, and the public sources as they answered on 2026-10-13. The data module is 1.0.1 because 1.0.0 is already committed.
CH = 20
DATE = "2026-10-13"
PYVER = "3.14.6"

TITLE = "Sending email, texts and push notifications for an advanced course: chapter 20 and today's EZGmail, Gmail API, smtplib, imaplib, SMS gateways and ntfy"
QUESTION = 'What does chapter 20 of the 3rd edition teach about sending and reading email with EZGmail and the Gmail API, texting through SMS email gateways and sending push notifications through ntfy, which of its printed outputs, listings and statements still hold under Python 3.14.6 (with ezgmail 2026.4.28 and requests 2.34.2, and with the Requests version its Appendix A pins), and what must an advanced course correct or add so that it matches the Gmail API, the email, smtplib and imaplib modules of the standard library, the state of the SMS gateways and the real behaviour of ntfy?'
CQS = ('Which parts of a program that sends or reads email, sends a text or pushes a notification can be shown to work, and which can only be shown to fail, on a machine that has no Gmail account, no phone number and no push service?',
       'Which printed outputs, programs, numbers and statements of the chapter differ in current releases of Python and of the packages it uses, in the zone of the reader, in the services it names or in the files and pages it points to, and on what source?')
PUBS = [
 ('P01', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 20, Sending Email, Texts, and Push Notifications (Al Sweigart, No Starch Press, 2025)', 'https://automatetheboringstuff.com/3e/chapter20.html', True),
 ('P02', 'Online materials of the 3rd edition, zip with 91 files and none for chapter 20 (No Starch Press, 2025)', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', False),
 ('P03', 'Automate the Boring Stuff with Python, 3rd edition - table of contents (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/', False),
 ('P04', 'Automate the Boring Stuff with Python, 3rd edition - book page (No Starch Press, 2025)', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', False),
 ('P05', 'Appendix A, Installing Third-Party Modules, with the versions the book pins (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixa.html', False),
 ('P06', 'Appendix B, Answers to the Practice Questions (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixb.html', False),
 ('P07', 'Automate the Boring Stuff with Python, 2nd edition - Chapter 18, Sending Email and Text Messages (Al Sweigart, No Starch Press, 2019)', 'https://automatetheboringstuff.com/2e/chapter18/', False),
 ('P08', 'EZGmail README (Al Sweigart, 2024)', 'https://raw.githubusercontent.com/asweigart/ezgmail/master/README.md', False),
 ('P09', 'PyPI JSON metadata of ezgmail (Python Package Index, 2026)', 'https://pypi.org/pypi/ezgmail/json', False),
 ('P10', 'PyPI JSON metadata of requests (Python Package Index, 2026)', 'https://pypi.org/pypi/requests/json', False),
 ('P11', 'PyPI JSON metadata of aiosmtpd (Python Package Index, 2026)', 'https://pypi.org/pypi/aiosmtpd/json', False),
 ('P12', 'PyPI JSON metadata of imapclient (Python Package Index, 2026)', 'https://pypi.org/pypi/imapclient/json', False),
 ('P13', 'PyPI JSON metadata of oauth2client (Python Package Index, 2026)', 'https://pypi.org/pypi/oauth2client/json', False),
 ('P14', 'aiosmtpd documentation (The aiosmtpd Developers, 2026)', 'https://aiosmtpd.aio-libs.org/en/latest/', False),
 ('P15', 'Publishing, ntfy documentation (Philipp Heckel, 2026)', 'https://docs.ntfy.sh/publish/', False),
 ('P16', 'Subscribe through the API, ntfy documentation (Philipp Heckel, 2026)', 'https://docs.ntfy.sh/subscribe/api/', False),
 ('P17', 'Configuring the ntfy server (Philipp Heckel, 2026)', 'https://docs.ntfy.sh/config/', False),
 ('P18', 'Frequently asked questions, ntfy documentation (Philipp Heckel, 2026)', 'https://docs.ntfy.sh/faq/', False),
 ('P19', 'ntfy.sh health endpoint (Philipp Heckel, 2026)', 'https://ntfy.sh/v1/health', False),
 ('P20', 'smtplib - SMTP protocol client (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/smtplib.html', False),
 ('P21', 'imaplib - IMAP4 protocol client (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/imaplib.html', False),
 ('P22', 'email.message - Representing an email message (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/email.message.html', False),
 ('P23', 'email.policy - Policy objects (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/email.policy.html', False),
 ('P24', 'email.mime - Creating email and MIME objects from scratch (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/email.mime.html', False),
 ('P25', 'email.utils - Miscellaneous utilities (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/email.utils.html', False),
 ('P26', 'email.header - Internationalized headers (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/email.header.html', False),
 ('P27', 'ssl - TLS/SSL wrapper for socket objects (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/ssl.html', False),
 ('P28', 'mimetypes - Map filenames to MIME types (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/mimetypes.html', False),
 ('P29', "What's New In Python 3.14 (Python 3.14 documentation)", 'https://docs.python.org/3.14/whatsnew/3.14.html', False),
 ('P30', "What's New In Python 3.13 (Python documentation)", 'https://docs.python.org/3.13/whatsnew/3.13.html', False),
 ('P31', "What's New In Python 3.12 (Python documentation)", 'https://docs.python.org/3.12/whatsnew/3.12.html', False),
 ('P32', "What's New In Python 3.15 (Python documentation)", 'https://docs.python.org/3.15/whatsnew/3.15.html', False),
 ('P33', 'PEP 594 - Removing dead batteries from the standard library (Christian Heimes and Brett Cannon, Python Software Foundation, 2019)', 'https://peps.python.org/pep-0594/', False),
 ('P34', 'RFC 5321 - Simple Mail Transfer Protocol (John Klensin, IETF, 2008)', 'https://www.rfc-editor.org/rfc/rfc5321', False),
 ('P35', 'RFC 5322 - Internet Message Format (Pete Resnick, IETF, 2008)', 'https://www.rfc-editor.org/rfc/rfc5322', False),
 ('P36', 'RFC 2045 - Multipurpose Internet Mail Extensions, Part One (Ned Freed and Nathaniel Borenstein, IETF, 1996)', 'https://www.rfc-editor.org/rfc/rfc2045', False),
 ('P37', 'RFC 2047 - MIME, Part Three: Message Header Extensions for Non-ASCII Text (Keith Moore, IETF, 1996)', 'https://www.rfc-editor.org/rfc/rfc2047', False),
 ('P38', 'RFC 3501 - Internet Message Access Protocol, version 4rev1 (Mark Crispin, IETF, 2003)', 'https://www.rfc-editor.org/rfc/rfc3501', False),
 ('P39', 'RFC 3207 - SMTP Service Extension for Secure SMTP over TLS (Paul Hoffman, IETF, 2002)', 'https://www.rfc-editor.org/rfc/rfc3207', False),
 ('P40', 'RFC 8314 - Cleartext Considered Obsolete: Use of TLS for Email Submission and Access (Keith Moore and Chris Newman, IETF, 2018)', 'https://www.rfc-editor.org/rfc/rfc8314', False),
 ('P41', 'RFC 4954 - SMTP Service Extension for Authentication (Robert Siemborski and Alexey Melnikov, IETF, 2007)', 'https://www.rfc-editor.org/rfc/rfc4954', False),
 ('P42', 'RFC 2369 - The Use of URLs as Meta-Syntax for Core Mail List Commands (Grant Neufeld and Josh Baer, IETF, 1998)', 'https://www.rfc-editor.org/rfc/rfc2369', False),
 ('P43', 'RFC 8058 - Signaling One-Click Functionality for List Email Headers (Sean Leonard, IETF, 2017)', 'https://www.rfc-editor.org/rfc/rfc8058', False),
 ('P44', 'RFC 7208 - Sender Policy Framework (Scott Kitterman, IETF, 2014)', 'https://www.rfc-editor.org/rfc/rfc7208', False),
 ('P45', 'RFC 7489 - Domain-based Message Authentication, Reporting, and Conformance (Murray Kucherawy and Elizabeth Zwicky, IETF, 2015)', 'https://www.rfc-editor.org/rfc/rfc7489', False),
 ('P46', 'RFC 2177 - IMAP4 IDLE command (Barry Leiba, IETF, 1997)', 'https://www.rfc-editor.org/rfc/rfc2177', False),
 ('P47', 'RFC 821 - Simple Mail Transfer Protocol (Jonathan Postel, IETF, 1982)', 'https://www.rfc-editor.org/rfc/rfc821', False),
 ('P48', 'Using OAuth 2.0 to Access Google APIs (Google, 2026)', 'https://developers.google.com/identity/protocols/oauth2', False),
 ('P49', 'Sending email, Gmail API guide (Google, 2026)', 'https://developers.google.com/workspace/gmail/api/guides/sending', False),
 ('P50', 'users.messages.send, Gmail API reference (Google, 2026)', 'https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/send', False),
 ('P51', 'Choose Gmail API scopes (Google, 2026)', 'https://developers.google.com/workspace/gmail/api/auth/scopes', False),
 ('P52', 'Usage limits, Gmail API (Google, 2026)', 'https://developers.google.com/workspace/gmail/api/reference/quota', False),
 ('P53', 'users.threads.list, Gmail API reference (Google, 2026)', 'https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.threads/list', False),
 ('P54', 'Search operators you can use with Gmail (Google, 2026)', 'https://support.google.com/mail/answer/7190', False),
 ('P55', 'Messages that have attachments, file types Gmail blocks (Google, 2026)', 'https://support.google.com/mail/answer/6590', False),
 ('P56', 'Send attachments with your Gmail message, 25 MB limit (Google, 2026)', 'https://support.google.com/mail/answer/6584', False),
 ('P57', 'Email sender guidelines (Google, 2026)', 'https://support.google.com/a/answer/81126', False),
 ('P58', 'AT&T email to text and text to email ending (AT&T, 2025)', 'https://www.att.com/support/article/wireless/KM1061254/', False),
 ('P59', 'Verizon vtext.com and vzwpix.com shutdown notice (Verizon, 2026)', 'https://www.verizon.com/support/vtext-vzwpix-shutdown/', False),
 ('P60', 'What is GSM-7 character encoding (Twilio, 2026)', 'https://www.twilio.com/docs/glossary/what-is-gsm-7-character-encoding', False),
 ('P61', 'Message resource, Twilio Programmable Messaging API (Twilio, 2026)', 'https://www.twilio.com/docs/messaging/api/message-resource', False),
 ('P62', 'A2P 10DLC registration, Twilio documentation (Twilio, 2026)', 'https://www.twilio.com/docs/messaging/compliance/a2p-10dlc', False),
 ('P63', 'National Weather Service API documentation (National Weather Service, 2026)', 'https://www.weather.gov/documentation/services-web-api', False),
 ('P64', 'Ray Tomlinson (Wikipedia)', 'https://en.wikipedia.org/wiki/Ray_Tomlinson', False),
 ('P65', 'Email spam (Wikipedia)', 'https://en.wikipedia.org/wiki/Email_spam', False),
 ('P66', 'SMS (Wikipedia)', 'https://en.wikipedia.org/wiki/SMS', False),
 ('P67', 'Gmail (Wikipedia)', 'https://en.wikipedia.org/wiki/Gmail', False),
 ('P68', 'Simple Mail Transfer Protocol (Wikipedia)', 'https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol', False),
 ('P69', 'IMAP, POP and SMTP for Gmail (Google, 2026)', 'https://developers.google.com/workspace/gmail/imap/imap-smtp', False),
 ('P70', 'OAuth 2.0 Mechanism, XOAUTH2 for Gmail IMAP and SMTP (Google, 2026)', 'https://developers.google.com/workspace/gmail/imap/xoauth2-protocol', False),
 ('P71', 'uv - Python versions (Astral documentation)', 'https://docs.astral.sh/uv/concepts/python-versions/', False),
 ('P72', 'Download Python (python.org)', 'https://www.python.org/downloads/', False),
]
CONCEPTS = [
 ('Section', 'The Gmail API'),
 ('Section', 'Enabling the API'),
 ('Section', 'Sending Mail'),
 ('Section', 'Reading Mail'),
 ('Section', 'Searching for Mail'),
 ('Section', 'Downloading Attachments'),
 ('Section', 'SMS Email Gateways'),
 ('Section', 'Push Notifications'),
 ('Section', 'Sending Notifications'),
 ('Section', 'Transmitting Metadata'),
 ('Section', 'Receiving Notifications'),
 ('Section', 'Summary'),
 ('Section', 'Practice Questions'),
 ('Section', 'Practice Programs'),
 ('Section', 'Umbrella Reminder'),
 ('Section', 'Auto Unsubscriber'),
 ('Section', 'Email-Based Computer Control'),
 ('Figure', 'Figure 20-1: searching for RoboCop email at the Gmail website'),
 ('Table', 'Table 20-1: SMS email gateways for cell phone providers'),
 ('Module', 'ezgmail'),
 ('Module', 'requests'),
 ('Module', 'json'),
 ('Module', 'subprocess'),
 ('Module', 'smtplib'),
 ('Module', 'imaplib'),
 ('Module', 'webbrowser'),
 ('Module', 'Beautiful Soup'),
 ('Module', 'datetime'),
 ('Module', 'logging'),
 ('Program', 'qBittorrent'),
 ('Program', 'ntfy app'),
 ('File', 'credentials.json'),
 ('File', 'token.json'),
 ('File', 'shakespeare_complete_works.torrent'),
]
FINDINGS = [
 ('F1', 'Background',
  "Chapter 20 of the 3rd edition, Sending Email, Texts, and Push Notifications, teaches three ways for a program to reach a person: the Gmail API through the EZGmail module (setup with a credentials file and a token file, send() with attachments, cc and bcc, GmailThread and GmailMessage objects from unread(), recent() and search(), and the download of attachments), texts through the SMS email gateways of Table 20-1 with Twilio named as the reliable alternative, and push notifications through ntfy with the Requests library (a POST to a topic, the headers Title, Tags and Priority, and a poll with /json?poll=1 and since); it ends with five practice questions and three practice programs, Umbrella Reminder, Auto Unsubscriber and Email-Based Computer Control [P01]. The page was fetched on 2026-10-13 and returned 200 with 53,147 bytes, and its sha256 equals the chapterDigest of the book's own chapter ontology [P01] [P03] [P04].",
  ['P01', 'P03', 'P04']),
 ('F2', 'The online materials',
  "The online materials of the 3rd edition (7,759,877 bytes, 91 files, 72 of them Python) hold no file for chapter 20: no program names ezgmail, ntfy, smtplib, imaplib, Twilio or weather.gov, and phoneAndEmail.py in them belongs to chapter 8 [P02]. The chapter's last sentence sends a reader who is stuck on the Email-Based Computer Control program to the book page of No Starch Press for an example implementation, but that page has 0 occurrences of an example implementation, of Email-Based, of ezgmail or of ntfy [P01] [P04]. The 2nd edition's chapter 18 mentions smtplib 21 times, imapclient 20, pyzmail 14 and Twilio 31, which the 3rd edition's chapter 20 replaces with the Gmail API, the gateway table and ntfy, and it names smtplib and imaplib only to say that EZGmail is better [P01] [P07].",
  ['P01', 'P02', 'P04', 'P07']),
 ('F3', 'The chapter replayed',
  "The 48 statements of the chapter's 15 listings were replayed as printed in three environments. With ezgmail 2026.4.28 and no credentials, which is where a reader stands before the Google Cloud steps, 19 of 48 matched the book, and 19 matched with the Requests 2.32.3 that Appendix A pins; in an environment with neither package 3 matched; ezgmail.init() and every call after it raised EZGmailException (Can't find credentials file at DIR/credentials.json.) and ezgmail.LOGGED_IN stayed False [P01] [P05] [P08]. On a stand-in for the server of Google, whose replies were written by this study, 42 of 46 matched in the zone America/Los_Angeles and 38 of 46 in Europe/Istanbul, where the dates printed Dec 10 instead of Dec 09 and the timestamp read 2026-12-10 00:28:48 [P01]. The four that do not match in either zone are the send() of listing 4 and the Popen of listing 15, whose quoted strings the web page breaks across lines (SyntaxError: unterminated string literal), the printed text of str(unread_threads[0]), and the Popen of a Windows path with its line break repaired (FileNotFoundError on Linux) [P01].",
  ['P01', 'P05', 'P08']),
 ('F4', 'The printed thread text',
  "The chapter prints str(unread_threads[0]) as a GmailThread with len=2 and a snippet that has no opening quote, but ezgmail 2026.4.28 prints <GmailThread numMessages=2 snippet='Do you want to watch RoboCop this weekend?'>, and building that text costs a request to the API, because the thread fetches its messages the first time messages is read [P01] [P08] [P09]. The printed summary line ends in Dec 09 and the printed timestamp is datetime.datetime(2026, 12, 9, 13, 28, 48), but the package builds timestamp as a naive datetime from internalDate, so the same message reads 08:48:48 in America/Chicago, 14:48:48 in UTC and 17:48:48 in Europe/Istanbul; the chapter never says that the reading depends on the zone of the computer [P01]. The example fromtimestamp(1797823712) printed as 2026-12-20 21:28:32 is right only in a zone at UTC-6; in UTC it is 2026-12-21 03:28:32, a Monday [P01].",
  ['P01', 'P08', 'P09']),
 ('F5', 'Credentials, token and expiry',
  "The page of the chapter never uses the file name credentials.json (it says a credentials file and a token file and names token.json), although Appendix B does, and it never uses the word refresh [P01] [P06]. import ezgmail already calls init(_raiseException=False), so a failure of login is hidden until the first call; a token.json written by oauth2client is plain JSON of 16 keys with the file mode 0o600 and holds the client secret and the refresh token, so the chapter's advice to treat it like a password is right [P08] [P09]. Google's OAuth page says that a project whose consent screen is external and in the publishing status Testing is issued a refresh token that expires in 7 days, which the chapter does not say and which this study read but could not run, because it needs a Google account and a week [P48].",
  ['P01', 'P06', 'P08', 'P09', 'P48']),
 ('F6', 'The library under EZGmail',
  "ezgmail 2026.4.28 (uploaded 2026-04-28) requires google-api-python-client and oauth2client; oauth2client 4.1.3 was uploaded on 2018-09-07 and is classified Development Status 7 - Inactive, while google-api-python-client was at 2.201.0, uploaded 2026-09-30, so the login of the chapter's library stands on an authorisation package that has not changed in eight years [P09] [P13]. The package declares no Requires-Python in its metadata, and under Python 3.14.6 it was imported and ran through the stand-in [P09].",
  ['P09', 'P13']),
 ('F7', 'Defects of EZGmail found by execution',
  "On the stand-in, reply() posted a message with the threadId of the original but with the subject unchanged (RoboCop, no Re:) and without In-Reply-To or References, which Google's sending guide names, together with a matching Subject, as what makes a message join a thread, and replyAll() made no API call and returned None [P49]. downloadAllAttachments wrote an attachment named ../evil.txt one level above the download folder, and downloadAttachment overwrote an existing file as the chapter says [P01]. A message with no Subject header raised AttributeError on .subject and on str(); summary() cut the last character of a sender written without a space (noreply@example.com became noreply@example.co); removeQuotedParts cut only the English form On Sun, Jan 1, 2018 at 12:00 PM ... wrote: and left the replies of the forms On Sun, 1 Jan 2018 at 12:00, a Turkish line, and the English line with U+202F before PM; and a subject with a line break raised HeaderParseError before any request was made [P08] [P09].",
  ['P01', 'P08', 'P09', 'P49']),
 ('F8', 'Non-ASCII text and bytes',
  "ezgmail sent a Turkish body as charset utf-8 in base64 and a Turkish subject as an encoded word, and both came back unchanged [P36] [P37]. Requests sent a str body as UTF-8 (21 bytes for the 20 characters of Yedekleme tamamlandı) with no Content-Type, so the receiver has to assume the charset, and refused a header value with a dotless i with UnicodeEncodeError because it encodes header values as latin-1, and a header given as the integer 5 with InvalidHeader, so a Title with a Turkish word fails while the book's English Title and its Priority string work [P01] [P10]. The limit of ntfy is 4,096 bytes, not characters: 4096 ASCII characters fit and 2049 dotless i characters are 4098 bytes, and the documentation says a longer message is treated as an attachment, which the chapter does not say [P15].",
  ['P01', 'P10', 'P15', 'P36', 'P37']),
 ('F9', 'The gateways have gone or are going',
  "Table 20-1 of the chapter begins with the gateways txt.att.net and mms.att.net, and AT&T's support article says that on June 17, 2025 its email-to-text and text-to-email service was shut down, 483 days before 2026-10-13 and a Tuesday [P01] [P58]. Verizon's notice says it has begun to shut down email-to-text for Vtext.com and VZWPix.com, expects to complete it by 03/31/2027, a Wednesday 169 days after 2026-10-13, and that some senders may lose access earlier, so the gateway of the chapter's own example, 2125551234@vtext.com, is on a schedule to end [P59]. A DNS-over-HTTPS query for the MX records of the 18 domains of the table found no MX for txt.att.net, mms.att.net and sms.cricketwireless.net, NXDOMAIN for messaging.sprintpcs.com and pm.sprint.com and SERVFAIL for sms.myboostmobile.com, and mail exchangers for the other 12; a missing MX is a symptom, not proof [P01]. Twilio's REST API answered a request with no credentials with HTTP 401 (code 20003), and nothing else about Twilio could be observed without an account [P61].",
  ['P01', 'P58', 'P59', 'P61']),
 ('F10', 'How long a text can be',
  "The chapter says an SMS gateway limits a message to 160 characters; Twilio's page explains the arithmetic, 140 bytes of 8 bits at 7 bits a character, and that a character such as { needs an escape and counts as two [P01] [P60]. Counted with a GSM-7 table written for the study, 160 characters of the basic set fit one message and 161 need 2, {x} costs 5, and one character outside the table, the dotless i of Yedekleme tamamlandı, turns the text into UCS-2 at 16 bits a character, so 70 characters fit and 71 need 2 [P60]. The segment sizes for longer texts, 153 and 67 characters, follow from a 6-byte header and were not found on a page opened by this study; they are unconfirmed [P60].",
  ['P01', 'P60']),
 ('F11', 'ntfy as the chapter uses it',
  "The chapter's four event values, message, open, keepalive and poll_request, are two fewer than the six in the documentation, which adds message_delete and message_clear; the example answer has expires 43200 seconds, 12 hours, after time [P01] [P16]. The poll answer is not valid JSON as a whole (json.loads raised Extra data) but one object per line, and a blank line raised JSONDecodeError again, so a program that splits lines should skip empty ones [P01]. The random part of the book's topic, ZPgxBQ42, is 8 characters of 62, 47.6 bits, and the other half is the author's name; ntfy's FAQ says that without access control the topic name is the password, and the topic is part of the URL path, so it appears in logs [P18]. post() returns a Response whose ok was False on a 429 that a recorder returned, with nothing raised, so a program that notifies about a long job fails silently when a limit is reached; only raise_for_status() raised [P01] [P10]. GET /v1/health answered 200 with healthy true on the day and a poll of an unused topic answered 200 with an empty body; nothing was published to ntfy.sh [P19].",
  ['P01', 'P10', 'P16', 'P18', 'P19']),
 ('F12', 'The from address and what the chapter leaves out',
  "The chapter says it is fairly trivial for hackers to fake a from address and asks for a password in the mail [P01]. On a local server the envelope sender bounces@mallory.example and the header From: CEO <ceo@bank.example> were independent, with no login and no TLS, and a Bcc recipient was in the envelope but not in the text, as the documentation of send_message says [P20] [P34] [P35]. The page of the chapter never uses the words STARTTLS, TLS, SSL, SPF, DKIM, DMARC, Reply-To, Message-ID, encoding or timeout [P01]. The SPF record of gmail.com on the day was v=spf1 redirect=_spf.google.com, its DMARC record v=DMARC1; p=none; sp=quarantine; rua=mailto:mailauth-reports@google.com, and Google's sender guidelines require authentication from senders of more than 5,000 messages a day [P44] [P45] [P57].",
  ['P01', 'P20', 'P34', 'P35', 'P44', 'P45', 'P57']),
 ('F13', 'What changed in Python and in the standard library',
  'One program that exercises email, smtplib, imaplib, ssl and email.utils against a small SMTP server written with sockets was run under 11 interpreters (3.11.17, 3.12.3, 3.13.16, 3.14.0 to 3.14.6 and 3.15.0b4) and compared 48 items; 19 differ between releases [P29] [P30] [P31] [P32]. imaplib.IMAP4.idle() exists from 3.14 only; smtplib sends its commands in lower case from 3.13 (mail from:, rcpt to:) where 3.12 sent mail FROM:; the keyfile and certfile arguments of starttls and of the SSL classes are gone from 3.12; ssl.create_default_context() adds VERIFY_X509_STRICT and VERIFY_X509_PARTIAL_CHAIN and a minimum of TLS 1.2 from 3.13; smtpd, asyncore and asynchat are gone from 3.12 and cgi, imghdr, sndhdr, nntplib and telnetlib from 3.13; and email.utils.localtime(isdst=) is gone from 3.14 [P20] [P21] [P33]. parseaddr returned empty strings for two addresses in one string in every interpreter of the study, and the 3.14 documentation says its strict argument came in 3.13 [P25].',
  ['P20', 'P21', 'P25', 'P29', 'P30', 'P31', 'P32', 'P33']),
 ('F14', 'The practice programs',
  "A search of the forecast text for the word rain found it in neither of 2 sample periods and so missed the period with a chance of precipitation of 60, which a comparison of the probabilityOfPrecipitation number with a limit flagged; api.weather.gov returned 14 periods for a point in Chicago with such a number in each [P01] [P63]. A parser for links whose text says unsubscribe found 1 of 3 candidates, because an image link and the text opt out are missed, while the List-Unsubscribe header (RFC 2369) with List-Unsubscribe-Post (RFC 8058) gives a mailto: and an https: address without parsing HTML [P42] [P43]. The control loop ran only the commands of an allow-list, so rm was refused, and a subject run through a shell (status; echo PWNED) printed an injected line until it was passed as a list argument; hmac.compare_digest raised TypeError for a non-ASCII str, and the book's Popen of qBittorrent raised FileNotFoundError on Linux [P01]. Mail was received with SMTP and read with IMAP, deleted and expunged against dovecot 2.3.21, a local stand-in for Gmail [P38].",
  ['P01', 'P38', 'P42', 'P43', 'P63']),
 ('F15', 'Not done in this study',
  'No Gmail account, Google Cloud project, phone number, carrier, Twilio account or ntfy subscriber was used: nothing was sent to a person, a phone or a push service, and a connection to imap.gmail.com and smtp.gmail.com timed out from this machine, so no Gmail server was reached [P69] [P70]. The Gmail replies were written by this study, the SMTP server was aiosmtpd, the IMAP server was dovecot 2.3.21 and the ntfy side was a recorder on 127.0.0.1, all labelled stand-ins; the real ntfy server could not be downloaded here, github.com answering 403. The 7-day expiry of a Testing refresh token, the acceptance of .exe and .zip attachments, the delivery of a text through a gateway, the 153 and 67 character segments and the behaviour of a real Gmail inbox are therefore not verified [P48] [P55]. No photograph is used, because the single request to Wikimedia Commons answered 429.',
  ['P48', 'P55', 'P69', 'P70']),
]

def X(code):
    """An executable example as one expression with no double quote and no line break: the code runs in a fresh
    namespace and the value of its variable out is the result."""
    lit = "'" + code.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace('"', "\\x22") + "'"
    return "(lambda g: (exec(%s, g), g['out'])[1])({})" % lit

# The helpers every example starts from (the modules, err() returns what a call raised, wd() makes and enters a temporary folder) and the stand-ins:
# _GM replaces the HTTP object of the Google client library with one that records each request and returns replies written by this study (the Gmail API stand-in),
# _SMTP starts aiosmtpd with a self-signed certificate on 127.0.0.1, _NTFY starts a recorder on 127.0.0.1 that is not ntfy, _MSG builds a fixed EmailMessage,
# _TABLE is Table 20-1 as data, _GSM counts GSM-7 and UCS-2 segments and _BOOKTEXT is the answer the chapter prints for the poll of the ntfy topic.
_PRE = r'''import io, os, re, sys, math, shlex, subprocess, json, time, base64, shutil, socket, ssl, smtplib, tempfile, threading, datetime, hashlib, hmac, mimetypes, secrets, warnings, email, inspect, contextlib, importlib.metadata as md
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
_GM = r'''import ezgmail, httplib2
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
_MSG = r'''def mk(**kw):
    m = EmailMessage(); m['From'] = kw.get('frm', 'Al Sweigart <al@example.com>'); m['To'] = kw.get('to', 'Jon Doe <jon@example.org>'); m['Subject'] = kw.get('subj', 'RoboCop')
    m['Date'] = eu.formatdate(1797000528, usegmt=True); m['Message-ID'] = '<fixed-1@example.com>'
    for k, v in kw.get('extra', {}).items(): m[k] = v
    m.set_content(kw.get('body', 'Do you want to watch RoboCop this weekend?')); return m
'''
_SMTP = r'''import ipaddress, logging
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
_NTFY = r'''import http.server, requests
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
_TABLE = r'''T = {'AT&T': ('txt.att.net', 'mms.att.net'), 'Boost Mobile': ('sms.myboostmobile.com', None), 'Cricket': ('sms.cricketwireless.net', 'mms.cricketwireless.net'), 'Google Fi': ('msg.fi.google.com', None),
     'Metro PCS': ('mymetropcs.com', None), 'Republic Wireless': ('text.republicwireless.com', None), 'Sprint': ('messaging.sprintpcs.com', 'pm.sprint.com'), 'T-Mobile': ('tmomail.net', None),
     'U.S. Cellular': ('email.uscc.net', 'mms.uscc.net'), 'Verizon': ('vtext.com', 'vzwpix.com'), 'Virgin Mobile': ('vmobl.com', 'vmpix.com'), 'Xfinity Mobile': ('vtext.com', 'mypixmessages.com')}
def addr(number, carrier, mms=False):
    sms, m = T[carrier]; return '%s@%s' % (number, (m or sms) if mms else sms)
'''
_GSM = r'''BASIC = '@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !"#¤%&\'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà'
EXT = '^{}\\[~]|€'
def septets(t):
    n = 0
    for ch in t:
        if ch in BASIC: n += 1
        elif ch in EXT: n += 2
        else: return None
    return n
def segments(t):
    s = septets(t)
    if s is not None: return ('GSM-7', s, 1 if s <= 160 else -(-s // 153))
    u = len(t.encode('utf-16-le')) // 2; return ('UCS-2', u, 1 if u <= 70 else -(-u // 67))
'''
_BOOKTEXT = r'''TXT = ('{"id":"1jnHKeFNqwnS","time":1797823340,"expires":1797866540,"event":"message","topic":"AlSweigartZPgxBQ42","message":"Hello, world!"}\n'
       '{"id":"wZ22cjyKXw1F","time":1797823712,"expires":1797866912,"event":"message","topic":"AlSweigartZPgxBQ42","title":"Important: Read this!","message":"The rent is too high!","priority":5,"tags":["warning","neutral_face"]}\n')
'''

# (top, mid, leaf, exemplar, definition, (the example as an expression, its result) or None when it needs an account, a phone or a service)
TAX = [
 # ---------------- GmailApi
 ('GmailApi', 'GmailSetup', 'CredentialsAndToken', 'ezgmail.init()',
  'ezgmail 2026.4.28 reads credentials.json and token.json from the working directory and asks for the one scope https://mail.google.com/; with no credentials.json, ezgmail.init() raises EZGmailException (Can\'t find credentials file at DIR/credentials.json.) and ezgmail.LOGGED_IN and ezgmail.EMAIL_ADDRESS stay False, so the chapter\'s "If no error appears" test fails on a machine where the Google Cloud steps of chapter 15 were not done.',
  (X(_PRE + r'''import ezgmail
d = wd()
e = err(lambda: ezgmail.init())
out = (e[0], e[1].split(' You can')[0].replace(d, 'DIR'), ezgmail.LOGGED_IN, ezgmail.EMAIL_ADDRESS, ezgmail.SCOPES, ezgmail.__version__)'''), '(\'EZGmailException\', "Can\'t find credentials file at DIR/credentials.json.", False, False, \'https://mail.google.com/\', \'2026.4.28\')')),
 ('GmailApi', 'GmailSetup', 'ImportRunsInit', 'import ezgmail',
  'The last line of the ezgmail package is the call init(_raiseException=False), so import ezgmail already tries to log in and hides the failure; init takes userId, tokenFile (default token.json), credentialsFile (default credentials.json) and _raiseException (default True), and its source calls run_flow, the browser authorisation of oauth2client.',
  (X(_PRE + r'''import ezgmail
src = inspect.getsource(ezgmail).rstrip().splitlines()
sig = inspect.signature(ezgmail.init)
out = (src[-1], list(sig.parameters), sig.parameters['tokenFile'].default, sig.parameters['credentialsFile'].default, sig.parameters['_raiseException'].default, 'run_flow' in inspect.getsource(ezgmail.init))'''), "('init(_raiseException=False)', ['userId', 'tokenFile', 'credentialsFile', '_raiseException'], 'token.json', 'credentials.json', True, True)")),
 ('GmailApi', 'GmailSetup', 'TokenFileContents', 'token.json',
  "A token.json written by oauth2client holds 16 keys as plain JSON, among them client_id, client_secret, access_token and refresh_token, with the file mode 0o600 (owner only), and reading it back gives the same refresh token; the chapter's advice to treat token.json like a password is right, because the file carries everything needed to act as the user.",
  (X(_PRE + r'''from oauth2client import client, file
d = wd()
c = client.OAuth2Credentials('dummy-access-token', 'dummy-client-id', 'dummy-client-secret', 'dummy-refresh-token', None, 'https://oauth2.googleapis.com/token', 'ezgmail-test', scopes=['https://mail.google.com/'])
st = file.Storage('token.json'); st.put(c)
j = json.load(open('token.json'))
out = (sorted(j), j['client_secret'], j['refresh_token'], j['scopes'], oct(os.stat('token.json').st_mode & 0o777), file.Storage('token.json').get().refresh_token)'''), "(['_class', '_module', 'access_token', 'client_id', 'client_secret', 'id_token', 'id_token_jwt', 'invalid', 'refresh_token', 'revoke_uri', 'scopes', 'token_expiry', 'token_info_uri', 'token_response', 'token_uri', 'user_agent'], 'dummy-client-secret', 'dummy-refresh-token', ['https://mail.google.com/'], '0o600', 'dummy-refresh-token')")),
 ('GmailApi', 'GmailSetup', 'TestingModeExpiry', 'publishing status Testing',
  "Google's OAuth page says a Google Cloud project whose consent screen is of the external user type and in the publishing status Testing is issued a refresh token that expires in 7 days, unless the scopes are only name, address and profile, so a script that worked last week can ask for the browser authorisation again; the chapter does not say this. Not executed: it needs a Google account and a week.",
  None),
 ('GmailApi', 'GmailSetup', 'DeprecatedOauthLibrary', "md.version('oauth2client')",
  "ezgmail 2026.4.28 requires google-api-python-client and oauth2client; oauth2client 4.1.3 was uploaded on 2018-09-07 and is classified Development Status 7 - Inactive on PyPI, while google-api-python-client is at 2.201.0, so the chapter's library stands on an authorisation package that has not changed in eight years.",
  (X(_PRE + r'''out = (md.version('oauth2client'), md.requires('ezgmail'), md.version('google-api-python-client'), md.version('ezgmail'), [x for x in md.requires('ezgmail') if 'oauthlib' in x])'''), "('4.1.3', ['google-api-python-client', 'oauth2client'], '2.201.0', '2026.4.28', [])")),
 ('GmailApi', 'GmailSending', 'SendCall', "ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email')",
  'ezgmail.send makes one POST to users/me/messages/send whose JSON body has the single key raw, the message as base64url; the message is a legacy MIMEText with the headers Content-Type, MIME-Version, Content-Transfer-Encoding, to, from and subject, type text/plain and encoding 7bit for an ASCII body.',
  (X(_PRE + _GM + r'''h = gm({})
ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email')
m = raw_of(h)
out = (h.log[0][0], h.log[0][1], list(m.keys()), m.get_content_type(), m['Content-Transfer-Encoding'], m.get_content(), list(json.loads(h.log[0][2])))'''), "('POST', 'users/me/messages/send?alt=json', ['Content-Type', 'MIME-Version', 'Content-Transfer-Encoding', 'to', 'from', 'subject'], 'text/plain', '7bit', 'Body of the email', ['raw'])")),
 ('GmailApi', 'GmailSending', 'AttachmentParts', "ezgmail.send(to, subject, body, ['attachment1.jpg', 'attachment2.mp3'])",
  "With a list of file names ezgmail.send builds a multipart/mixed message with the text first and one base64 part per file, typed by its extension (image/jpeg, audio/mpeg, application/x-msdos-program for setup.exe, application/zip for notes.zip); it does not refuse an .exe or a .zip, and a name that does not exist raises EZGmailException. Google's help page lists .exe among the types Gmail does not let you attach and says a .zip is refused only for what is inside it, which is more exact than the chapter's sentence about .exe or .zip attachments.",
  (X(_PRE + _GM + r'''d = wd()
open('attachment1.jpg', 'wb').write(b'\xff\xd8\xff\xe0' + b'0' * 20); open('attachment2.mp3', 'wb').write(b'ID3' + b'0' * 20); open('setup.exe', 'wb').write(b'MZ' + b'0' * 8); open('notes.zip', 'wb').write(b'PK' + b'0' * 8)
h = gm({})
ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email', ['attachment1.jpg', 'attachment2.mp3', 'setup.exe', 'notes.zip'])
m = raw_of(h)
out = (m.get_content_type(), [(p.get_content_type(), p.get_filename(), p['Content-Transfer-Encoding']) for p in m.iter_parts()], err(lambda: ezgmail.send('a@example.com', 's', 'b', ['missing.pdf']))[0])'''), "('multipart/mixed', [('text/plain', None, '7bit'), ('image/jpeg', 'attachment1.jpg', 'base64'), ('audio/mpeg', 'attachment2.mp3', 'base64'), ('application/x-msdos-program', 'setup.exe', 'base64'), ('application/zip', 'notes.zip', 'base64')], 'EZGmailException')")),
 ('GmailApi', 'GmailSending', 'CcAndBccHeaders', "ezgmail.send(..., cc='friend@example.com', bcc='a@example.com,b@example.com')",
  "The cc and bcc arguments become the Cc and Bcc headers of the message that is sent: a comma-joined bcc string is parsed into 2 addresses, and the Bcc header is part of the raw message that ezgmail posts to the Gmail API, where Google's guide says the recipients of Bcc are taken from the headers.",
  (X(_PRE + _GM + r'''h = gm({})
ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email', cc='friend@example.com', bcc='otherfriend@example.com,someoneelse@example.com')
m = raw_of(h)
out = (m['to'], m['cc'], m['bcc'], [a.addr_spec for a in m['bcc'].addresses], len(json.loads(h.log[0][2])['raw']) > 0)'''), "('recipient@example.com', 'friend@example.com', 'otherfriend@example.com, someoneelse@example.com', ['otherfriend@example.com', 'someoneelse@example.com'], True)")),
 ('GmailApi', 'GmailSending', 'NonAsciiText', "ezgmail.send('a@example.com', 'Rapor: şğı', 'Yedekleme tamamlandı')",
  'Non-ASCII text survives ezgmail.send: the body becomes charset utf-8 in base64 (Yedekleme tamamlandı: ğüşiöç İI came back unchanged), the subject becomes an encoded word (=?utf-8?b?...?=), and a mimeSubtype that is not plain or html raises EZGmailValueError.',
  (X(_PRE + _GM + r'''h = gm({}, {})
ezgmail.send('a@example.com', 'Yedekleme bitti', 'Yedekleme tamamlandı: ğüşiöç İI')
ezgmail.send('a@example.com', 'Rapor: şğı', 'plain ascii body')
r1 = base64.urlsafe_b64decode(json.loads(h.log[0][2])['raw']).decode('ascii').splitlines(); r2 = base64.urlsafe_b64decode(json.loads(h.log[1][2])['raw']).decode('ascii').splitlines()
m1 = raw_of(h, 0); m2 = raw_of(h, 1)
out = ([x for x in r1 if x.lower().startswith('content-')], m1.get_content().strip(), [x for x in r2 if x.startswith('subject')], m2['subject'], err(lambda: ezgmail.send('a@example.com', 's', 'b', mimeSubtype='rich'))[0])'''), '([\'Content-Type: text/plain; charset="utf-8"\', \'Content-Transfer-Encoding: base64\'], \'Yedekleme tamamlandı: ğüşiöç İI\', [\'subject: =?utf-8?b?UmFwb3I6IMWfxJ/EsQ==?=\'], \'Rapor: şğı\', \'EZGmailValueError\')')),
 ('GmailApi', 'GmailSending', 'ReplyThreading', 'GmailMessage.reply(body)',
  "GmailMessage.reply posts a message with the original sender as the recipient and the threadId of the original, but with the subject unchanged (RoboCop, no Re:) and without In-Reply-To or References headers, which Google's sending guide names as what makes a message join a thread together with a matching subject; GmailMessage.replyAll made no API call at all and returned None.",
  (X(_PRE + _GM + r'''h = gm({}, {})
m0 = ezgmail.GmailMessage(api_msg('M1', 'T1', 'Al Sweigart <al@inventwithpython.com>', 'Jon Doe <example@gmail.com>', 'RoboCop', 'Do you want to watch RoboCop this weekend?', 1797000000000))
m0.reply('Yes, Saturday works.')
body = json.loads(h.log[0][2]); m = raw_of(h)
out = (h.log[0][1], sorted(body), body['threadId'], m['to'], m['subject'], [k for k in m.keys() if k.lower() in ('in-reply-to', 'references')], ezgmail.GmailMessage.replyAll(m0, 'x'), len(h.log))'''), "('users/me/messages/send?alt=json', ['raw', 'threadId'], 'T1', 'Al Sweigart <al@inventwithpython.com>', 'RoboCop', [], None, 1)")),
 ('GmailApi', 'GmailReading', 'ThreadVersusMessage', 'str(unread_threads[0])',
  "A GmailThread holds an id, a snippet and a historyId and fetches its GmailMessage objects with one more GET (users/me/threads/T1) the first time messages is read; its repr is <GmailThread numMessages=2 snippet='Do you want to watch RoboCop this weekend?'> and building that text itself costs an API call, which is not the text the chapter prints (<GmailThread len=2 snippet= Do you ...'>).",
  (X(_PRE + _GM + r'''t = {'id': 'T1', 'snippet': 'Do you want to watch RoboCop this weekend?', 'historyId': '9'}
full = {'id': 'T1', 'messages': [api_msg('M1', 'T1', 'Al Sweigart <al@inventwithpython.com>', 'Jon Doe <example@gmail.com>', 'RoboCop', 'Do you want to watch RoboCop this weekend?\r\n', 1797000000000), api_msg('M2', 'T1', 'Jon Doe <example@gmail.com>', 'Al Sweigart <al@inventwithpython.com>', 'Re: RoboCop', 'Yes.\r\n', 1797000100000)]}
h = gm(full); th = ezgmail.GmailThread(t)
n0 = len(h.log); s = str(th); n1 = len(h.log); _ = th.messages; n2 = len(h.log)
book = "<GmailThread len=2 snippet= Do you want to watch RoboCop this weekend?'>"
out = (n0, n1, h.log[0][:2], s, s == book, n2, len(th.messages), type(th.messages[0]).__name__, th.text, th.senders())'''), '(0, 1, (\'GET\', \'users/me/threads/T1?alt=json\'), "<GmailThread numMessages=2 snippet=\'Do you want to watch RoboCop this weekend?\'>", False, 1, 2, \'GmailMessage\', [\'Do you want to watch RoboCop this weekend?\\r\\n\', \'Yes.\\r\\n\'], [\'Al Sweigart <al@inventwithpython.com>\', \'Jon Doe <example@gmail.com>\'])')),
 ('GmailApi', 'GmailReading', 'UnreadRecentSearch', 'ezgmail.unread(maxResults=50)',
  "unread, recent and search all call threads.list with a query and maxResults: unread asks q=label:UNREAD, recent asks q=label:INBOX, search passes the text as q (has:attachment, from:... subject:...), and the default maxResults of all three is 25, where Google's API default is 100 and its maximum is 500.",
  (X(_PRE + _GM + r'''h = gm({}, {}, {}, {}, {})
a = ezgmail.unread(); b = ezgmail.unread(maxResults=50); c = ezgmail.recent(); d = ezgmail.search('has:attachment'); e = ezgmail.search('from:al@inventwithpython.com subject:hello', maxResults=3)
out = ([x[1] for x in h.log], a, ezgmail.unread.__defaults__, ezgmail.recent.__defaults__, ezgmail.search.__defaults__)'''), "(['users/me/threads?q=label%3AUNREAD&maxResults=25&alt=json', 'users/me/threads?q=label%3AUNREAD&maxResults=50&alt=json', 'users/me/threads?q=label%3AINBOX&maxResults=25&alt=json', 'users/me/threads?q=has%3Aattachment&maxResults=25&alt=json', 'users/me/threads?q=from%3Aal%40inventwithpython.com+subject%3Ahello&maxResults=3&alt=json'], [], (25, 'me'), (25, 'me'), (25, 'me'))")),
 ('GmailApi', 'GmailReading', 'MessageFields', 'unread_threads[0].messages[0].timestamp',
  "A GmailMessage gets subject, sender, recipient, body, snippet and timestamp from the API's message; timestamp is a naive datetime made from internalDate with fromtimestamp, so the same message reads 08:48:48 in America/Chicago, 14:48:48 in UTC and 17:48:48 in Europe/Istanbul, and a message with no Subject header raises AttributeError on .subject and on str().",
  (X(_PRE + _GM + r'''m = ezgmail.GmailMessage(api_msg('M1', 'T1', 'Al Sweigart <al@inventwithpython.com>', 'Jon Doe <example@gmail.com>', 'RoboCop', 'Do you want to watch RoboCop this weekend?\r\n', 1797000528000))
res = []
for z in ('UTC', 'America/Chicago', 'Europe/Istanbul'):
    os.environ['TZ'] = z; time.tzset(); res.append((z, str(ezgmail.GmailMessage(api_msg('M1', 'T1', 'a', 'b', 'c', 'd', 1797000528000)).timestamp)))
bare = api_msg('M2', 'T2', 'x@example.com', 'y@example.com', 'S', 'text', 1)
bare['payload']['headers'] = [h for h in bare['payload']['headers'] if h['name'] != 'Subject']
nm = ezgmail.GmailMessage(bare)
out = (m.subject, m.sender, m.recipient, repr(m.body), m.snippet, res, err(lambda: nm.subject)[0], err(lambda: str(nm))[0], err(lambda: nm.subject)[1])'''), '(\'RoboCop\', \'Al Sweigart <al@inventwithpython.com>\', \'Jon Doe <example@gmail.com>\', "\'Do you want to watch RoboCop this weekend?\\\\r\\\\n\'", \'Do you want to watch RoboCop this weekend?\\r\\n\', [(\'UTC\', \'2026-12-11 14:48:48\'), (\'America/Chicago\', \'2026-12-11 08:48:48\'), (\'Europe/Istanbul\', \'2026-12-11 17:48:48\')], \'AttributeError\', \'AttributeError\', "\'GmailMessage\' object has no attribute \'subject\'")')),
 ('GmailApi', 'GmailReading', 'QuotedTextCut', 'ezgmail.removeQuotedParts(text)',
  'removeQuotedParts cuts a reply at the English line On Sun, Jan 1, 2018 at 12:00 PM Name <address> wrote: and keeps the text before it (0 quote marks left), and it cut the same line with a short sender, Al <a@b.c>; it did not cut a reply written On Sun, 1 Jan 2018 at 12:00, a Turkish 1 Oca 2018 Paz 12:00 tarihinde ... yazdi: line, or the English line in which the space before PM is the narrow no-break space U+202F (the regular expression wants a plain space); each uncut reply kept its 2 > characters. This study did not observe which mail programs write the narrow space.',
  (X(_PRE + _GM + r'''q1 = 'Sounds good.\n\nOn Sun, Jan 1, 2018 at 12:00 PM Al Sweigart <al@inventwithpython.com> wrote:\n> Do you want to watch?'
q2 = 'Sounds good.\n\nOn Sun, 1 Jan 2018 at 12:00, Al Sweigart <al@inventwithpython.com> wrote:\n> Do you want to watch?'
q3 = 'Tamam.\n\n1 Oca 2018 Paz 12:00 tarihinde Al Sweigart <al@inventwithpython.com> yazdi:\n> Film izleyelim mi?'
q4 = q1.replace('12:00 PM', '12:00 PM')
q5 = 'Sounds good.\n\nOn Sun, Jan 1, 2018 at 12:00 PM Al <a@b.c> wrote:\n> hi'
out = ([ezgmail.removeQuotedParts(q).count('>') for q in (q1, q2, q3, q4, q5)], repr(ezgmail.removeQuotedParts(q1)), q4 != q1, len(q1) - len(q4))'''), '([0, 2, 2, 2, 0], "\'Sounds good.\\\\n\\\\n\'", True, 0)')),
 ('GmailApi', 'GmailReading', 'SummaryLine', 'ezgmail.summary(threads)',
  'summary prints the first names of the senders, the snippet and the month and day of each thread, as in Al, Jon - Do you want to watch RoboCop this weekend? - Dec 11, and it cuts the last character off a sender written without a space: noreply@example.com is printed as noreply@example.co.',
  (X(_PRE + _GM + r'''h = gm({'id': 'T1', 'messages': [api_msg('M1', 'T1', 'Al Sweigart <al@inventwithpython.com>', 'Jon <j@example.com>', 'RoboCop', 'Do you want to watch RoboCop this weekend?', 1797000000000), api_msg('M2', 'T1', 'Jon Doe <j@example.com>', 'Al <a@example.com>', 'Re: RoboCop', 'Yes', 1797000100000)]},
        {'id': 'T2', 'messages': [api_msg('M3', 'T2', 'noreply@example.com', 'j@example.com', 'News', 'Thanks for stopping me from buying Bitcoin.', 1797000200000)]})
ths = [ezgmail.GmailThread({'id': 'T1', 'snippet': 'Do you want to watch RoboCop this weekend?', 'historyId': '1'}), ezgmail.GmailThread({'id': 'T2', 'snippet': 'Thanks for stopping me from buying Bitcoin.', 'historyId': '1'})]
buf = io.StringIO()
with contextlib.redirect_stdout(buf): ezgmail.summary(ths)
raw = ezgmail.summary(ths, printInfo=False)
out = (buf.getvalue().splitlines(), [(x[0], x[1][:12]) for x in raw], 'noreply@example.com'[: 'noreply@example.com'.find(' ')])'''), "(['Al, Jon - Do you want to watch RoboCop this weekend? - Dec 11', 'noreply@example.co - Thanks for stopping me from buying Bitcoin. - Dec 11'], [(['Al Sweigart <al@inventwithpython.com>', 'Jon Doe <j@example.com>'], 'Do you want '), (['noreply@example.com'], 'Thanks for s')], 'noreply@example.co')")),
 ('GmailApi', 'GmailAttachments', 'AttachmentNames', 'threads[0].messages[0].attachments',
  'attachments is a list of file names, with duplicates (tulips.jpg, canal.jpg, canal.jpg), and the body of a multipart message is the text part only; downloadAttachment with a name that is not in the list raises AttributeError, not a message that names the file.',
  (X(_PRE + _GM + r'''parts = [{'mimeType': 'text/plain', 'filename': '', 'headers': [{'name': 'Content-Type', 'value': 'text/plain; charset="UTF-8"'}], 'body': {'size': 5, 'data': b64('Photos')}},
         {'mimeType': 'image/jpeg', 'filename': 'tulips.jpg', 'headers': [], 'body': {'attachmentId': 'A1', 'size': 11}}, {'mimeType': 'image/jpeg', 'filename': 'canal.jpg', 'headers': [], 'body': {'attachmentId': 'A2', 'size': 12}},
         {'mimeType': 'image/jpeg', 'filename': 'canal.jpg', 'headers': [], 'body': {'attachmentId': 'A3', 'size': 13}}]
m = ezgmail.GmailMessage(api_msg('M1', 'T1', 'a@example.com', 'b@example.com', 'vacation photos', 'Photos', 1797000000000, parts))
out = (m.attachments, m._attachmentsInfo[0], repr(m.body), type(m.attachments).__name__, err(lambda: m.downloadAttachment('nothere.jpg'))[0], err(lambda: m.downloadAllAttachments('x', overwrite=False))[0])'''), '([\'tulips.jpg\', \'canal.jpg\', \'canal.jpg\'], {\'filename\': \'tulips.jpg\', \'id\': \'A1\', \'size\': 11}, "\'Photos\'", \'list\', \'AttributeError\', \'EZGmailException\')')),
 ('GmailApi', 'GmailAttachments', 'DownloadOverwrite', "message.downloadAllAttachments(downloadFolder='vacation2026')",
  'downloadAttachment overwrote an existing tulips.jpg (MINE became AAAA), as the chapter says, and downloadAllAttachments fetched every attachment again, including tulips.jpg a second time, with the folder created for it and canal.jpg saved with the bytes of its own attachment id.',
  (X(_PRE + _GM + r'''d = wd()
parts = [{'mimeType': 'text/plain', 'filename': '', 'headers': [], 'body': {'size': 1, 'data': b64('x')}}, {'mimeType': 'image/jpeg', 'filename': 'tulips.jpg', 'headers': [], 'body': {'attachmentId': 'A1', 'size': 4}}, {'mimeType': 'image/jpeg', 'filename': 'canal.jpg', 'headers': [], 'body': {'attachmentId': 'A2', 'size': 4}}]
m = ezgmail.GmailMessage(api_msg('M1', 'T1', 'a@example.com', 'b@example.com', 's', 'x', 1797000000000, parts))
open('tulips.jpg', 'wb').write(b'MINE')
h = gm({'data': b64(b'AAAA'), 'size': 4}, {'data': b64(b'BBBB'), 'size': 4}, {'data': b64(b'CCCC'), 'size': 4})
r0 = m.downloadAttachment('tulips.jpg'); first = open('tulips.jpg', 'rb').read()
r1 = m.downloadAllAttachments(downloadFolder='vacation2026')
out = (r0, first, r1, sorted(os.listdir('vacation2026')), [x[1].split('?')[0] for x in h.log], open('vacation2026/canal.jpg', 'rb').read())'''), "(None, b'AAAA', ['tulips.jpg', 'canal.jpg'], ['canal.jpg', 'tulips.jpg'], ['users/me/messages/M1/attachments/A1', 'users/me/messages/M1/attachments/A1', 'users/me/messages/M1/attachments/A2'], b'CCCC')")),
 ('GmailApi', 'GmailAttachments', 'FilenameTraversal', "downloadAllAttachments(downloadFolder='inbox')",
  "An attachment named ../evil.txt was written one level above the download folder: inbox stayed empty, evil.txt appeared beside it, and downloadAllAttachments returned ['../evil.txt'], so a program that downloads attachments from strangers must reduce each name to its last part (os.path.basename gives evil.txt).",
  (X(_PRE + _GM + r'''d = wd(); os.mkdir('inbox')
parts = [{'mimeType': 'text/plain', 'filename': '', 'headers': [], 'body': {'size': 1, 'data': b64('x')}}, {'mimeType': 'text/plain', 'filename': '../evil.txt', 'headers': [], 'body': {'attachmentId': 'A9', 'size': 4}}]
m = ezgmail.GmailMessage(api_msg('M1', 'T1', 'a@example.com', 'b@example.com', 's', 'x', 1797000000000, parts))
h = gm({'data': b64(b'PWNED'), 'size': 5})
done = m.downloadAllAttachments(downloadFolder='inbox')
out = (done, os.listdir('inbox'), sorted(os.listdir('.')), open('evil.txt').read(), os.path.basename('../evil.txt'), os.path.realpath('inbox/../evil.txt') == os.path.realpath('evil.txt'))'''), "(['../evil.txt'], [], ['evil.txt', 'inbox'], 'PWNED', 'evil.txt', True)")),
 # ---------------- StandardLibraryMail
 ('StandardLibraryMail', 'MessageObjects', 'EmailMessageBuild', 'EmailMessage()',
  'EmailMessage with set_content builds a text/plain message whose headers are written in the order they were set (From, To, Subject, Date, Message-ID, then Content-Type, Content-Transfer-Encoding 7bit and MIME-Version); as_bytes() ends lines with LF (0 CRLF) and as_bytes(policy=policy.SMTP) with CRLF (10), and a message read back keeps display name Jon Doe and address jon@example.org apart.',
  (X(_PRE + _MSG + r'''m = mk()
raw = m.as_bytes(); smtp = m.as_bytes(policy=policy.SMTP); back = email.message_from_bytes(raw, policy=policy.default)
out = (type(m).__name__, type(m.policy).__name__, raw.decode().splitlines(), raw.count(b'\r\n'), smtp.count(b'\r\n'), back['to'].addresses[0].display_name, back['to'].addresses[0].addr_spec, back.get_content())'''), '(\'EmailMessage\', \'EmailPolicy\', [\'From: Al Sweigart <al@example.com>\', \'To: Jon Doe <jon@example.org>\', \'Subject: RoboCop\', \'Date: Fri, 11 Dec 2026 14:48:48 +0000\', \'Message-ID: <fixed-1@example.com>\', \'Content-Type: text/plain; charset="utf-8"\', \'Content-Transfer-Encoding: 7bit\', \'MIME-Version: 1.0\', \'\', \'Do you want to watch RoboCop this weekend?\'], 0, 10, \'Jon Doe\', \'jon@example.org\', \'Do you want to watch RoboCop this weekend?\\n\')')),
 ('StandardLibraryMail', 'MessageObjects', 'MimeTree', 'msg.add_alternative(html, subtype="html")',
  'add_alternative and add_attachment turn the message into multipart/mixed holding multipart/alternative (text/plain and text/html) and application/octet-stream; get_body with preference html and plain returns the html part, and iter_attachments finds poster.bin.',
  (X(_PRE + _MSG + r'''m = mk(); m.add_alternative('<p>Do you want to watch <b>RoboCop</b>?</p>', subtype='html'); m.add_attachment(b'\x00\x01\x02', maintype='application', subtype='octet-stream', filename='poster.bin')
tree = []
def walk(p, d=0):
    tree.append(('  ' * d) + p.get_content_type())
    for c in p.iter_parts(): walk(c, d + 1)
walk(m)
out = (tree, m.get_body(preferencelist=('plain',)).get_content().strip(), m.get_body(preferencelist=('html', 'plain')).get_content_type(), [a.get_filename() for a in m.iter_attachments()], m.get_boundary() is not None, m.is_multipart())'''), "(['multipart/mixed', '  multipart/alternative', '    text/plain', '    text/html', '  application/octet-stream'], 'Do you want to watch RoboCop this weekend?', 'text/html', ['poster.bin'], False, True)")),
 ('StandardLibraryMail', 'MessageObjects', 'HeaderEncoding', 'msg["Subject"] = "Yedekleme bitti ✓ şğı"',
  'A Subject with non-ASCII characters is written as an encoded word (=?utf-8?b?4pyTIMWfxJ/EsQ==?=), a display name with a comma and a dotless i as =?utf-8?q?Y=C4=B1lmaz=2C_Ay=C5=9Fe?=, and decode_header with make_header gives the text back; with a policy that has utf8=True the same header is written as raw UTF-8.',
  (X(_PRE + _MSG + r'''from email.header import decode_header, make_header
m = mk(subj='Yedekleme bitti ✓ şğı', to='"Yılmaz, Ayşe" <ayse@example.org>')
a = m.as_bytes().decode('ascii').splitlines(); u = m.as_bytes(policy=policy.default.clone(utf8=True)).decode('utf-8').splitlines()
subj = [x for x in a if x.startswith('Subject')][0]
out = (subj, [x for x in a if x.startswith('To')], [x for x in u if x.startswith('Subject')], str(make_header(decode_header(subj.split(': ', 1)[1]))), decode_header(subj.split(': ', 1)[1])[0][1], m['subject'], [x for x in a if x.startswith('Content-Type')])'''), '(\'Subject: Yedekleme bitti =?utf-8?b?4pyTIMWfxJ/EsQ==?=\', [\'To: =?utf-8?q?Y=C4=B1lmaz=2C_Ay=C5=9Fe?= <ayse@example.org>\'], [\'Subject: Yedekleme bitti ✓ şğı\'], \'Yedekleme bitti ✓ şğı\', None, \'Yedekleme bitti ✓ şğı\', [\'Content-Type: text/plain; charset="utf-8"\'])')),
 ('StandardLibraryMail', 'MessageObjects', 'AddressParsing', 'email.utils.parseaddr(text)',
  'parseaddr splits Al Sweigart <al@inventwithpython.com> into a name and an address; given two addresses in one string it returns (\'\', \'\') under Python 3.14 and the other releases of this study, and (\'\', \'real@example.com\') only with strict=False, and getaddresses keeps a quoted name with a comma ("Doe, Jon") whole but splits it in two without the quotes.',
  (X(_PRE + r'''s = '"Doe, Jon" <jon@example.org>, Al Sweigart <al@inventwithpython.com>, plain@example.com'
bad = 'real@example.com, evil@example.net'
out = (eu.parseaddr('Al Sweigart <al@inventwithpython.com>'), eu.getaddresses([s]), eu.getaddresses([s.replace('"Doe, Jon"', 'Doe, Jon')]), eu.parseaddr(bad), eu.parseaddr(bad, strict=False), eu.formataddr(('Yılmaz, Ayşe', 'ayse@example.org')), eu.formataddr(('Jon Doe', 'jon@example.org')), getattr(eu, 'supports_strict_parsing', None))'''), "(('Al Sweigart', 'al@inventwithpython.com'), [('Doe, Jon', 'jon@example.org'), ('Al Sweigart', 'al@inventwithpython.com'), ('', 'plain@example.com')], [('', 'Doe'), ('Jon', 'jon@example.org'), ('Al Sweigart', 'al@inventwithpython.com'), ('', 'plain@example.com')], ('', ''), ('', 'real@example.com'), '=?utf-8?b?WcSxbG1heiwgQXnFn2U=?= <ayse@example.org>', 'Jon Doe <jon@example.org>', True)")),
 ('StandardLibraryMail', 'SmtpClient', 'StarttlsSession', 'smtp.starttls(context=ctx)',
  'On a local aiosmtpd stand-in the server advertised STARTTLS before and AUTH LOGIN PLAIN only after it, STARTTLS was answered 220, send_message returned {} and the server saw the session as TLS with the envelope sender al@example.com and recipient jon@example.org; smtp.gmail.com is the real server Google names for the same steps.',
  (X(_PRE + _MSG + _SMTP + r'''c, box, port, cp = serve()
try:
    s = smtplib.SMTP('127.0.0.1', port, timeout=10)
    e1 = s.ehlo()[1].decode().splitlines()[1:]
    r = s.starttls(context=ssl.create_default_context(cafile=cp))
    e2 = s.ehlo()[1].decode().splitlines()[1:]
    resp = s.send_message(mk()); s.quit()
    out = (e1, r[0], e2, resp, box[0]['tls'], box[0]['from'], box[0]['to'], box[0]['data'].decode().splitlines()[:3])
finally: c.stop()'''), "(['SIZE 33554432', '8BITMIME', 'SMTPUTF8', 'STARTTLS', 'HELP'], 220, ['SIZE 33554432', '8BITMIME', 'SMTPUTF8', 'AUTH LOGIN PLAIN', 'HELP'], {}, True, 'al@example.com', ['jon@example.org'], ['From: Al Sweigart <al@example.com>', 'To: Jon Doe <jon@example.org>', 'Subject: RoboCop'])")),
 ('StandardLibraryMail', 'SmtpClient', 'CertificateVerification', 'ssl.create_default_context(cafile=cert)',
  "starttls() with the default context of the server's self-signed certificate raised SSLCertVerificationError (self-signed certificate), starttls() with no context succeeded (220) on a context with verify_mode CERT_NONE and so encrypted without authenticating the server, and a context from create_default_context(cafile=...) had check_hostname True and verify_mode CERT_REQUIRED and connected to localhost.",
  (X(_PRE + _SMTP + r'''c, box, port, cp = serve()
try:
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    e1 = err(lambda: s.starttls(context=ssl.create_default_context()))
    s2 = smtplib.SMTP('127.0.0.1', port, timeout=10); s2.ehlo(); r2 = s2.starttls()
    s3 = smtplib.SMTP('127.0.0.1', port, timeout=10); s3.ehlo()
    e3 = err(lambda: s3.starttls(context=ssl.create_default_context(cafile=cp)))
    ctx = ssl.create_default_context(cafile=cp); s4 = smtplib.SMTP('localhost', port, timeout=10); s4.ehlo(); r4 = s4.starttls(context=ctx)
    out = (e1[0], e1[1].split(' (_ssl')[0], r2[0], s2.sock.context.verify_mode.name if hasattr(s2.sock, 'context') else None, e3[0], r4[0], ctx.check_hostname, ctx.verify_mode.name)
finally: c.stop()'''), "('SSLCertVerificationError', '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate', 220, 'CERT_NONE', 'ok', 220, True, 'CERT_REQUIRED')")),
 ('StandardLibraryMail', 'SmtpClient', 'LoginAfterTls', 'smtp.login(user, password)',
  "login before STARTTLS raised SMTPNotSupportedError (SMTP AUTH extension not supported by server) because the server offered AUTH only after TLS; after STARTTLS login returned (235, b'2.7.0 Authentication successful') and a wrong password raised SMTPAuthenticationError with code 535.",
  (X(_PRE + _SMTP + r'''c, box, port, cp = serve(auth_required=False)
try:
    def conn(tls):
        s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
        if tls: s.starttls(context=ssl.create_default_context(cafile=cp)); s.ehlo()
        return s
    s = conn(False); before = [x for x in s.ehlo()[1].decode().splitlines() if x.startswith('AUTH')]; a = err(lambda: s.login('user', 'secret')); s.close()
    s = conn(True); after = [x for x in s.ehlo()[1].decode().splitlines() if x.startswith('AUTH')]; ok = s.login('user', 'secret'); s.quit()
    s = conn(True); b = err(lambda: s.login('user', 'wrong')); s.close()
    out = (before, a, after, ok, b)
finally: c.stop()'''), '([], (\'SMTPNotSupportedError\', \'SMTP AUTH extension not supported by server.\'), [\'AUTH LOGIN PLAIN\'], (235, b\'2.7.0 Authentication successful\'), (\'SMTPAuthenticationError\', "(535, b\'5.7.8 Authentication credentials invalid\')"))')),
 ('StandardLibraryMail', 'SmtpClient', 'EnvelopeRecipients', 'smtp.send_message(msg)',
  'send_message sent RCPT TO for the To, the Bcc and the Cc addresses (jon@example.org, secret@example.com, friend@example.com), left the Bcc header out of the transmitted message (it was None at the server) and kept the secret address nowhere in the text; the message object itself still had its Bcc header after sending.',
  (X(_PRE + _MSG + _SMTP + r'''c, box, port, cp = serve()
try:
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    m = mk(extra={'Cc': 'friend@example.com', 'Bcc': 'secret@example.com'})
    resp = s.send_message(m); s.quit()
    hdr = email.message_from_bytes(box[0]['data'], policy=policy.default)
    out = (resp, box[0]['to'], box[0]['from'], hdr['Bcc'], hdr['Cc'], 'secret@example.com' in box[0]['data'].decode(), m['Bcc'])
finally: c.stop()'''), "({}, ['jon@example.org', 'secret@example.com', 'friend@example.com'], 'al@example.com', None, 'friend@example.com', False, 'secret@example.com')")),
 ('StandardLibraryMail', 'SmtpClient', 'RefusedRecipients', 'smtplib.SMTPRecipientsRefused',
  'When the server refused one of two recipients (550) send_message returned a dict naming the refused address and the message was stored for the other; only when every recipient was refused did it raise SMTPRecipientsRefused, and nothing was stored.',
  (X(_PRE + _MSG + _SMTP + r'''c, box, port, cp = serve()
try:
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    m = mk(to='ok@example.org, gone@refused.example'); one = s.send_message(m)
    m2 = mk(to='gone@refused.example'); e = err(lambda: s.send_message(m2))
    s.quit()
    out = (one, len(box), e[0], str(e[1])[:70], [x['to'] for x in box])
finally: c.stop()'''), '({\'gone@refused.example\': (550, b\'5.1.1 no such mailbox\')}, 1, \'SMTPRecipientsRefused\', "{\'gone@refused.example\': (550, b\'5.1.1 no such mailbox\')}", [[\'ok@example.org\']])')),
 ('StandardLibraryMail', 'ImapClient', 'ImapSession', 'imaplib.IMAP4(host).starttls(ssl_context=ctx)',
  'Against dovecot 2.3.21 on 127.0.0.1, a local stand-in for imap.gmail.com, imaplib did STARTTLS, LOGIN, SELECT, SEARCH UNSEEN, FETCH, STORE +FLAGS \\Deleted and EXPUNGE: a fetch with BODY.PEEK left the message unseen, a fetch of RFC822 set \\Seen, the expunge left the INBOX empty, and a wrong password raised imaplib.IMAP4.error ([AUTHENTICATIONFAILED]); imapclient 4.1.0 did the same search, fetch and delete. Recorded in the live observations; not run against Gmail.',
  None),
 ('StandardLibraryMail', 'ImapClient', 'ImapParsing', 'imaplib.ParseFlags(data)',
  'ParseFlags returns the flags of a FETCH answer as bytes (b\'\\Seen\', b\'\\Flagged\'), Internaldate2tuple turns "17-Jul-1996 02:44:25 -0700" into a time tuple, Time2Internaldate writes an aware datetime as "09-Dec-2026 13:28:48 +0000", the ports are 143 and 993, and the Commands table has 43 entries.',
  (X(_PRE + r'''import imaplib
d = b'1 (FLAGS (\\Seen \\Flagged) INTERNALDATE "17-Jul-1996 02:44:25 -0700" RFC822.SIZE 4286)'
t = imaplib.Internaldate2tuple(d)
out = (imaplib.ParseFlags(d), t[:6], imaplib.Time2Internaldate(datetime.datetime(2026, 12, 9, 13, 28, 48, tzinfo=datetime.timezone.utc)), imaplib.Int2AP(1234567), imaplib.IMAP4_PORT, imaplib.IMAP4_SSL_PORT, sorted(imaplib.Commands)[:3], len(imaplib.Commands), 'IDLE' in imaplib.Commands)'''), '((b\'\\\\Seen\', b\'\\\\Flagged\'), (1996, 7, 17, 12, 44, 25), \'"09-Dec-2026 13:28:48 +0000"\', b\'BCNGIH\', 143, 993, [\'APPEND\', \'AUTHENTICATE\', \'CAPABILITY\'], 43, True)')),
 ('StandardLibraryMail', 'ImapClient', 'ImapIdle', 'imaplib.IMAP4.idle()',
  'Python 3.14 added IMAP4.idle() for the IDLE command of RFC 2177; under 3.14.6 imaplib.IMAP4 has idle and IDLE is in imaplib.Commands for the states AUTH and SELECTED, and the interpreter record shows 3.11, 3.12 and 3.13 without it.',
  (X(_PRE + r'''import imaplib
out = (hasattr(imaplib.IMAP4, 'idle'), 'IDLE' in imaplib.Commands, imaplib.Commands.get('IDLE'), [n for n in ('idle', 'starttls', 'login', 'authenticate', 'uid', 'search', 'fetch', 'store', 'expunge') if hasattr(imaplib.IMAP4, n)], sys.version_info[:2] >= (3, 14))'''), "(True, True, ('AUTH', 'SELECTED'), ['idle', 'starttls', 'login', 'authenticate', 'uid', 'search', 'fetch', 'store', 'expunge'], True)")),
 ('StandardLibraryMail', 'GmailByProtocol', 'GmailEndpoints', 'imap.gmail.com:993',
  'Google documents imap.gmail.com on 993 with SSL and smtp.gmail.com on 465 with SSL or 587 with STARTTLS, and says the Gmail IMAP, POP and SMTP servers support OAuth 2.0 through the SASL XOAUTH2 mechanism; a TCP connection from this machine to all three ports timed out after 10 seconds, so no Gmail server was reached and no login was tried. Recorded in the live observations.',
  None),
 ('StandardLibraryMail', 'GmailByProtocol', 'XoauthString', 'base64("user=... \\x01auth=Bearer ... \\x01\\x01")',
  'The SASL XOAUTH2 initial response is the string user=NAME, Control-A, auth=Bearer TOKEN, Control-A, Control-A in base64: for someuser@example.com and ya29.vF9dfd39 it is 72 characters of base64 that decode to those 3 control-A separated fields; the construction follows the format Google documents and was not sent to Google.',
  (X(_PRE + r'''s = 'user=someuser@example.com\x01auth=Bearer ya29.vF9dfd39\x01\x01'
b = base64.b64encode(s.encode()).decode()
out = (b, base64.b64decode(b).split(b'\x01'), len(b), 'user=' + 'someuser@example.com' == s.split('\x01')[0])'''), "('dXNlcj1zb21ldXNlckBleGFtcGxlLmNvbQFhdXRoPUJlYXJlciB5YTI5LnZGOWRmZDM5AQE=', [b'user=someuser@example.com', b'auth=Bearer ya29.vF9dfd39', b'', b''], 72, True)")),
 # ---------------- SmsGateways
 ('SmsGateways', 'GatewayAddressing', 'GatewayAddress', 'number@txt.att.net',
  "Table 20-1 lists 12 providers; an address is the number, an @ and the provider's SMS or MMS domain (5555550100@txt.att.net, 5555550100@mms.att.net), 5 of the 12 say Same as SMS for MMS, and nothing in the table says how the number is written for a provider that wants a country code or no dashes.",
  (X(_PRE + _TABLE + r'''out = (len(T), addr('5555550100', 'AT&T'), addr('5555550100', 'AT&T', mms=True), addr('5555550100', 'Boost Mobile', mms=True), sum(1 for v in T.values() if v[1] is None), addr('5555550100', 'Google Fi'), sorted(T)[:3])'''), "(12, '5555550100@txt.att.net', '5555550100@mms.att.net', '5555550100@sms.myboostmobile.com', 5, '5555550100@msg.fi.google.com', ['AT&T', 'Boost Mobile', 'Cricket'])")),
 ('SmsGateways', 'GatewayAddressing', 'SharedGateway', 'number@vtext.com',
  'Verizon and Xfinity Mobile share the SMS domain vtext.com, so of the 12 rows only 11 SMS domains are distinct and the address 5555550100@vtext.com does not say which carrier is meant; their MMS domains differ (vzwpix.com and mypixmessages.com).',
  (X(_PRE + _TABLE + r'''from collections import Counter
cnt = Counter(v[0] for v in T.values()); dup = [k for k, n in cnt.items() if n > 1]
out = (len(set(v[0] for v in T.values())), dup, [c for c, v in T.items() if v[0] == 'vtext.com'], addr('5555550100', 'Verizon') == addr('5555550100', 'Xfinity Mobile'), addr('5555550100', 'Verizon', True) == addr('5555550100', 'Xfinity Mobile', True))'''), "(11, ['vtext.com'], ['Verizon', 'Xfinity Mobile'], True, False)")),
 ('SmsGateways', 'GatewayRetreat', 'AttNotice', 'txt.att.net',
  "AT&T's support article KM1061254 says that on June 17, 2025 its email-to-text and text-to-email service was shut down, which is 483 days before 2026-10-13 and a Tuesday; Table 20-1 still lists txt.att.net and mms.att.net first, and the chapter's own warning that a gateway that works today may not work tomorrow came true for them.",
  (X(_PRE + _TABLE + r'''shut = D(2025, 6, 17); on = D(2026, 10, 13)
out = (T['AT&T'], (on - shut).days, shut.strftime('%A'), D(2026, 12, 20) > shut, 'txt.att.net' in [v[0] for v in T.values()])'''), "(('txt.att.net', 'mms.att.net'), 483, 'Tuesday', True, True)")),
 ('SmsGateways', 'GatewayRetreat', 'VerizonNotice', 'vtext.com',
  "Verizon's notice says it has begun to shut down email-to-text for vtext.com and vzwpix.com, expects it to be complete by 03/31/2027 (a Wednesday, 169 days after 2026-10-13) and says some senders may lose access earlier, so the gateway the chapter uses in its example (2125551234@vtext.com) is on a schedule to end.",
  (X(_PRE + _TABLE + r'''end = D(2027, 3, 31); on = D(2026, 10, 13)
out = (T['Verizon'], (end - on).days, end.strftime('%A'), (end - D(2025, 6, 17)).days)'''), "(('vtext.com', 'vzwpix.com'), 169, 'Wednesday', 652)")),
 ('SmsGateways', 'GatewayRetreat', 'DomainStatus', 'dig MX txt.att.net',
  'A DNS-over-HTTPS query on 2026-10-13 for the MX records of the 18 gateway domains of Table 20-1 found no MX for txt.att.net and mms.att.net (answered NOERROR with no records) and none for sms.cricketwireless.net (NOERROR, with names that carry no MX priority), NXDOMAIN for messaging.sprintpcs.com and pm.sprint.com and SERVFAIL for sms.myboostmobile.com, and mail exchangers for the other 12; a missing MX is a symptom, not proof that delivery fails. Recorded in the live observations.',
  None),
 ('SmsGateways', 'GatewayRetreat', 'TwilioInstead', 'GET https://api.twilio.com/2010-04-01/Accounts.json',
  'The chapter names Twilio as the reliable way to send texts and describes it as a service that may need a subscription, fees and an application; Twilio\'s REST API answered a request with no credentials with HTTP 401 and {"code":20003,"message":"Authentication Error - No credentials provided"}, which is all this study could observe without an account. Recorded in the live observations; no message was sent.',
  None),
 ('SmsGateways', 'SmsLimits', 'Gsm7Length', '(140 bytes * 8 bits) / 7 bits',
  'A text message carries 140 bytes, which hold 160 characters of 7 bits (GSM-7): 160 characters of the basic set fit one message and 161 need 2, a character of the extension table ({ } [ ] \\ ^ ~ | €) counts twice so {x} costs 5, and Yedekleme tamamlandi without the dotless i is 20 GSM-7 characters; a longer text is split into segments of 153 characters, a figure that comes from the 6-byte concatenation header (134 bytes of 8 bits as 7-bit characters) and not from a page opened by this study.',
  (X(_PRE + _GSM + r'''t160 = 'a' * 160
out = (140 * 8 // 7, septets('Hello, world!'), segments(t160), segments(t160 + 'a'), segments('a' * 306), segments('a' * 307), septets('{x}'), septets('€5'), segments('Yedekleme tamamlandi'), segments('Umbrella: bring one \u2602'))'''), "(160, 13, ('GSM-7', 160, 1), ('GSM-7', 161, 2), ('GSM-7', 306, 2), ('GSM-7', 307, 3), 5, 3, ('GSM-7', 20, 1), ('UCS-2', 21, 1))")),
 ('SmsGateways', 'SmsLimits', 'Ucs2Length', 'len(text.encode("utf-16-le")) // 2',
  'A character outside the GSM-7 sets, such as the dotless i of Yedekleme tamamlandı, makes the whole text UCS-2 at 16 bits a character: 70 characters fit one message (140 bytes / 2 bytes), 71 need 2, and an emoji is 2 code units, so 35 emoji fit and 36 do not; a long UCS-2 text is split into segments of 67 characters by the same concatenation arithmetic (134 bytes / 2), not confirmed from a page opened by this study.',
  (X(_PRE + _GSM + r'''t = 'Yedekleme tamamlandı'
out = (segments(t), 'ı' in BASIC, len(t), segments('ş' * 70), segments('ş' * 71), segments('ş' * 134), segments('ş' * 135), len('\U0001F600'), len('\U0001F600'.encode('utf-16-le')) // 2, segments('\U0001F600' * 35), segments('\U0001F600' * 36))'''), "(('UCS-2', 20, 1), False, 20, ('UCS-2', 70, 1), ('UCS-2', 71, 2), ('UCS-2', 134, 2), ('UCS-2', 135, 3), 1, 2, ('UCS-2', 70, 1), ('UCS-2', 72, 2))")),
 # ---------------- NtfyPush
 ('NtfyPush', 'NtfyPublishing', 'PostBody', "requests.post('https://ntfy.sh/topic', 'Hello, world!')",
  "On a local recorder that stands in for the service, requests.post(url, 'Hello, world!') sent a POST to the path /AlSweigartZPgxBQ42 with the 13 bytes as the body, Content-Length 13, no Content-Type and a python-requests User-Agent, and returned a Response with status 200; the recorder is not ntfy.",
  (X(_PRE + _NTFY + r'''srv, log, base = recorder(200, '{}')
r = requests.post(base + '/AlSweigartZPgxBQ42', 'Hello, world!')
q = log[0]
out = (r.status_code, r.ok, q['method'], q['path'], q['body'], q['headers'].get('Content-Length'), q['headers'].get('Content-Type'), q['headers']['User-Agent'].startswith('python-requests/'), q['headers']['Host'].startswith('127.0.0.1:'))
srv.shutdown()'''), "(200, True, 'POST', '/AlSweigartZPgxBQ42', b'Hello, world!', '13', None, True, True)")),
 ('NtfyPush', 'NtfyPublishing', 'MetadataHeaders', "headers={'Title': ..., 'Tags': ..., 'Priority': '5'}",
  'The three headers arrived unchanged (Title Important: Read this!, Tags warning,neutral_face, Priority 5), a Priority given as the integer 5 raised InvalidHeader because header values must be str or bytes, and a Title with a dotless i raised UnicodeEncodeError because requests encodes header values as latin-1.',
  (X(_PRE + _NTFY + r'''srv, log, base = recorder(200, '{}')
requests.post(base + '/t', 'The rent is too high!', headers={'Title': 'Important: Read this!', 'Tags': 'warning,neutral_face', 'Priority': '5'})
h = log[0]['headers']
e1 = err(lambda: requests.post(base + '/t', 'x', headers={'Priority': 5}))
e2 = err(lambda: requests.post(base + '/t', 'x', headers={'Title': 'Yedekleme tamamlandı'}))
out = ({k: h[k] for k in ('Title', 'Tags', 'Priority')}, e1[0], e1[1][:60], e2[0], e2[1][:50], len(log))
srv.shutdown()'''), '({\'Title\': \'Important: Read this!\', \'Tags\': \'warning,neutral_face\', \'Priority\': \'5\'}, \'InvalidHeader\', "Header part (5) from (\'Priority\', 5) must be of type str or ", \'UnicodeEncodeError\', "\'latin-1\' codec can\'t encode character \'\\\\u0131\' in", 1)')),
 ('NtfyPush', 'NtfyPublishing', 'BodyEncoding', "requests.post(url, 'Yedekleme tamamlandı')",
  "With urllib3 2.8.0 a str body is sent as UTF-8 (b'Yedekleme tamamland\\xc4\\xb1'), 21 bytes for 20 characters, with no Content-Type header, so a receiver has to assume the charset; encoding by hand to latin-1 with replace gave b'Yedekleme tamamland?', and an explicit Content-Type text/plain; charset=utf-8 was passed through.",
  (X(_PRE + _NTFY + r'''srv, log, base = recorder(200, '{}')
t = 'Yedekleme tamamlandı'
requests.post(base + '/t', t); requests.post(base + '/t', 'café'); requests.post(base + '/t', t.encode('latin-1', 'replace')); requests.post(base + '/t', t, headers={'Content-Type': 'text/plain; charset=utf-8'})
out = (log[0]['body'], log[0]['headers']['Content-Length'], len(t), len(t.encode()), log[0]['body'].decode('utf-8'), log[1]['body'], log[2]['body'], log[0]['headers'].get('Content-Type'), log[3]['headers']['Content-Type'], md.version('urllib3'))
srv.shutdown()'''), "(b'Yedekleme tamamland\\xc4\\xb1', '21', 20, 21, 'Yedekleme tamamlandı', b'caf\\xc3\\xa9', b'Yedekleme tamamland?', None, 'text/plain; charset=utf-8', '2.8.0')")),
 ('NtfyPush', 'NtfyPublishing', 'ResponseObject', 'requests.post(...).ok',
  'The chapter ignores the Response: when the recorder answered 429 with a JSON body written by this study (not a reply of ntfy) post returned a Response with ok False, nothing was raised, and only raise_for_status() raised HTTPError (429 Client Error: Too Many Requests), so a program that notifies you about a long job fails silently when the limit is reached.',
  (X(_PRE + _NTFY + r'''srv, log, base = recorder(429, '{"code":42908,"http":429,"error":"limit reached"}')
r = requests.post(base + '/t', 'Hello, world!')
e = err(lambda: r.raise_for_status())
r2 = None
out = (r.status_code, r.ok, bool(r), r.text, r.json()['http'], e[0], e[1][:48], len(log))
srv.shutdown()'''), '(429, False, False, \'{"code":42908,"http":429,"error":"limit reached"}\', 429, \'HTTPError\', \'429 Client Error: Too Many Requests for url: htt\', 1)')),
 ('NtfyPush', 'NtfySubscribing', 'PollUrl', "requests.get('https://ntfy.sh/topic/json?poll=1&since=10m')",
  "The poll is a GET of /topic/json with poll=1 and optionally since=10m, since=2h30m or since=1737866912, and requests builds the same query from params={'poll': 1, 'since': '2h30m'}; all four requests reached the recorder as GET.",
  (X(_PRE + _NTFY + r'''srv, log, base = recorder(200, '')
requests.get(base + '/AlSweigartZPgxBQ42/json?poll=1'); requests.get(base + '/AlSweigartZPgxBQ42/json?poll=1&since=10m')
requests.get(base + '/AlSweigartZPgxBQ42/json', params={'poll': 1, 'since': '2h30m'}); requests.get(base + '/AlSweigartZPgxBQ42/json', params={'poll': 1, 'since': 1737866912})
out = ([x['path'] for x in log], [x['method'] for x in log], requests.Request('GET', 'https://ntfy.sh/t/json', params={'poll': 1}).prepare().url)
srv.shutdown()'''), "(['/AlSweigartZPgxBQ42/json?poll=1', '/AlSweigartZPgxBQ42/json?poll=1&since=10m', '/AlSweigartZPgxBQ42/json?poll=1&since=2h30m', '/AlSweigartZPgxBQ42/json?poll=1&since=1737866912'], ['GET', 'GET', 'GET', 'GET'], 'https://ntfy.sh/t/json?poll=1')")),
 ('NtfyPush', 'NtfySubscribing', 'JsonLines', 'resp.text.splitlines()',
  'The poll answer is one JSON object per line: json.loads of the whole text raised JSONDecodeError (Extra data: line 2 column 1), splitlines then loads gave the 2 messages Hello, world! and The rent is too high!, and a blank line, which a stream can contain, raised JSONDecodeError again.',
  (X(_PRE + _BOOKTEXT + r'''e = err(lambda: json.loads(TXT))
n = [json.loads(x) for x in TXT.splitlines()]
ka = TXT + '\n{"id":"k1","time":1797823800,"expires":0,"event":"keepalive","topic":"AlSweigartZPgxBQ42"}\n'
e2 = err(lambda: [json.loads(x) for x in (TXT + '\n').splitlines()])
out = (e[0], e[1], len(n), n[0]['message'], n[1]['message'], e2[0], len([json.loads(x) for x in ka.splitlines() if x.strip()]), TXT.count('\n'))'''), "('JSONDecodeError', 'Extra data: line 2 column 1 (char 134)', 2, 'Hello, world!', 'The rent is too high!', 'JSONDecodeError', 3, 2)")),
 ('NtfyPush', 'NtfySubscribing', 'EventFields', "notifications[1]['expires']",
  "The first message has the keys id, time, expires, event, topic and message and the second adds title, priority 5 and tags; expires minus time is 43200 seconds, 12 hours; the documentation lists the event types open, keepalive, message, message_delete, message_clear and poll_request, 2 more than the chapter's four; and time 1797823712 is 2026-12-21T03:28:32 in UTC.",
  (X(_PRE + _BOOKTEXT + r'''n = [json.loads(x) for x in TXT.splitlines()]
book = {'message', 'open', 'keepalive', 'poll_request'}; docs = {'open', 'keepalive', 'message', 'message_delete', 'message_clear', 'poll_request'}
t = n[1]['time']
out = (sorted(n[0]), sorted(n[1]), n[1]['expires'] - n[1]['time'], (n[1]['expires'] - n[1]['time']) / 3600, DT.fromtimestamp(t, UTC).isoformat(), sorted(docs - book), n[1]['priority'], n[1]['tags'], [x['event'] for x in n])'''), "(['event', 'expires', 'id', 'message', 'time', 'topic'], ['event', 'expires', 'id', 'message', 'priority', 'tags', 'time', 'title', 'topic'], 43200, 12.0, '2026-12-21T03:28:32+00:00', ['message_clear', 'message_delete'], 5, ['warning', 'neutral_face'], ['message', 'message'])")),
 ('NtfyPush', 'NtfyServiceLimits', 'TopicSecrecy', 'secrets.token_urlsafe(16)',
  "The random part of the chapter's topic, ZPgxBQ42, is 8 characters of 62, 47.6 bits, and its first half is the author's name; secrets.token_urlsafe(16) gives 22 characters of 128 bits; the topic is part of the URL path, so it appears in logs, and ntfy's FAQ says that without access control the topic name is the password.",
  (X(_PRE + r'''import math
book = 'AlSweigartZPgxBQ42'; rnd = book[len('AlSweigart'):]
t = secrets.token_urlsafe(16)
out = (len(rnd), round(len(rnd) * math.log2(62), 1), round(math.log2(62 ** len(rnd) * 1), 1), 62 ** 8, round(16 * 8, 0), len(t), set(t) <= set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'), round(math.log2(62 ** 8) / 8, 2), 'https://ntfy.sh/' + book)'''), "(8, 47.6, 47.6, 218340105584896, 128, 22, True, 5.95, 'https://ntfy.sh/AlSweigartZPgxBQ42')")),
 ('NtfyPush', 'NtfyServiceLimits', 'DailyAndSize', "len(text.encode('utf-8'))",
  'The limit of 4,096 bytes is bytes, not characters: 4096 ASCII characters are 4096 bytes and 4097 are over, while 2049 dotless i characters are 4098 bytes; 250 messages of 4096 bytes are 1,024,000 bytes a day, one message every 345.6 seconds on average; the ntfy documentation says a message over the limit is turned into an attachment, which the chapter does not.',
  (X(_PRE + r'''ok = 'a' * 4096; no = 'a' * 4097; tr = 'ı' * 2048; tr2 = 'ı' * 2049
out = (len(ok.encode()), len(no.encode()), len(tr), len(tr.encode()), len(tr2.encode()), len(tr2.encode()) > 4096, 250 * 4096, 250 * 4096 // 1024, 24 * 60 // 250, 86400 / 250)'''), '(4096, 4097, 2048, 4096, 4098, True, 1024000, 1000, 5, 345.6)')),
 ('NtfyPush', 'NtfyServiceLimits', 'ServiceHealth', 'GET https://ntfy.sh/v1/health',
  'GET https://ntfy.sh/v1/health answered 200 with {"healthy":true}, and a GET poll of a random, unused topic answered 200 with an empty body and the content type application/x-ndjson; nothing was published to ntfy.sh by this study. Recorded in the live observations.',
  None),
 # ---------------- EmailTrust
 ('EmailTrust', 'EnvelopeAndHeaders', 'EnvelopeVersusHeader', 'smtp.sendmail(from_addr, to_addrs, msg)',
  "The envelope and the header are separate: the local server received MAIL FROM bounces@mallory.example and RCPT TO jon@example.org and hidden@example.org while the message said From: CEO <ceo@bank.example> and To: Jon Doe <jon@example.org>, with no login and no TLS, so the hidden address is nowhere in the text and the From is whatever the sender wrote; the chapter's remark that a from address is trivial to fake is right.",
  (X(_PRE + _MSG + _SMTP + r'''c, box, port, cp = serve()
try:
    s = smtplib.SMTP('127.0.0.1', port, timeout=10); s.ehlo()
    m = mk(frm='CEO <ceo@bank.example>', to='Jon Doe <jon@example.org>')
    s.sendmail('bounces@mallory.example', ['jon@example.org', 'hidden@example.org'], m.as_bytes()); s.quit()
    hdr = email.message_from_bytes(box[0]['data'], policy=policy.default)
    out = (box[0]['from'], box[0]['to'], hdr['From'], hdr['To'], 'hidden@example.org' in box[0]['data'].decode(), box[0]['auth'], box[0]['tls'])
finally: c.stop()'''), "('bounces@mallory.example', ['jon@example.org', 'hidden@example.org'], 'CEO <ceo@bank.example>', 'Jon Doe <jon@example.org>', False, False, False)")),
 ('EmailTrust', 'EnvelopeAndHeaders', 'HeaderLineLimits', 'policy.default.max_line_length',
  'The default policy folds headers at 78 characters (policy.SMTP also has 78 and CRLF as linesep): a 300-character Subject of words became 5 lines of at most 78, and a 1200-character Subject without spaces was written as encoded words (Subject: =?utf-8?q?x...) over 19 lines of at most 78, and read back as the original.',
  (X(_PRE + _MSG + r'''m = mk(subj='word ' * 60); raw = m.as_bytes().split(b'\r\n') if False else m.as_bytes().splitlines()
longone = mk(subj='x' * 1200)
r2 = longone.as_bytes().splitlines()
fold = [l for l in raw if l.startswith(b'Subject') or l.startswith(b' ')]
out = (max(len(l) for l in raw), len(fold), max(len(l) for l in fold), max(len(l) for l in r2), policy.default.max_line_length, policy.SMTP.max_line_length, policy.SMTP.linesep, [l for l in r2 if l.startswith(b'Subject')][0][:20], len([l for l in r2 if l.startswith(b'Subject') or l.startswith(b' ')]), email.message_from_bytes(longone.as_bytes(), policy=policy.default)['subject'] == 'x' * 1200)'''), "(78, 5, 78, 78, 78, 78, '\\r\\n', b'Subject: =?utf-8?q?x', 19, True)")),
 ('EmailTrust', 'EnvelopeAndHeaders', 'MessageIdAndDate', 'email.utils.make_msgid()',
  "make_msgid(idstring='job1', domain='example.com') gives <...job1@example.com> and two calls differ; formatdate(1797000528, usegmt=True) is Fri, 11 Dec 2026 14:48:48 GMT, without usegmt it ends -0000, and format_datetime of an aware UTC moment ends +0000 and parses back to the same instant.",
  (X(_PRE + r'''mid = eu.make_msgid(idstring='job1', domain='example.com')
out = (bool(re.fullmatch(r'<\d{14}\.\d+\.[0-9]+job1@example\.com>', mid)) or bool(re.fullmatch(r'<[0-9.]+job1@example\.com>', mid)), mid.startswith('<') and mid.endswith('@example.com>'), eu.formatdate(1797000528, usegmt=True), eu.formatdate(1797000528, localtime=False), eu.format_datetime(DT(2026, 12, 9, 13, 28, 48, tzinfo=UTC)), eu.parsedate_to_datetime('Wed, 09 Dec 2026 07:28:48 -0600').astimezone(UTC).isoformat(), eu.make_msgid() != eu.make_msgid())'''), "(True, True, 'Fri, 11 Dec 2026 14:48:48 GMT', 'Fri, 11 Dec 2026 14:48:48 -0000', 'Wed, 09 Dec 2026 13:28:48 +0000', '2026-12-09T13:28:48+00:00', True)")),
 ('EmailTrust', 'SenderAuthentication', 'DmarcRecordParse', 'dig TXT _dmarc.gmail.com',
  "A DMARC record is tag=value pairs separated by semicolons: the record observed for _dmarc.gmail.com on 2026-10-13 was v=DMARC1; p=none; sp=quarantine; rua=mailto:mailauth-reports@google.com, a policy of none for the domain and quarantine for subdomains, and a stricter sample has p=reject, pct=100, adkim=s and aspf=r; Google's sender guidelines require DMARC from senders of more than 5,000 messages a day.",
  (X(_PRE + r'''def tags(txt): return dict(p.strip().split('=', 1) for p in txt.split(';') if '=' in p)
seen = 'v=DMARC1; p=none; sp=quarantine; rua=mailto:mailauth-reports@google.com'
strict = 'v=DMARC1; p=reject; sp=reject; rua=mailto:reports@example.com; adkim=s; aspf=r; pct=100'
a = tags(seen); b = tags(strict)
out = (a['v'], a['p'], a['sp'], a['rua'], sorted(a), a.get('pct', '100'), b['p'], b['pct'], b['adkim'], b['aspf'], tags('v=DMARC1;p=quarantine;')['p'])'''), "('DMARC1', 'none', 'quarantine', 'mailto:mailauth-reports@google.com', ['p', 'rua', 'sp', 'v'], '100', 'reject', '100', 's', 'r', 'quarantine')")),
 ('EmailTrust', 'SenderAuthentication', 'SpfRecordParse', 'dig TXT gmail.com',
  'An SPF record is a version, mechanisms and a modifier: the TXT record observed for gmail.com on 2026-10-13 was v=spf1 redirect=_spf.google.com, which sends the check to another name, and a sample with 2 include mechanisms, an ip4 range and ~all (softfail) has 2 mechanisms that cost a DNS lookup.',
  (X(_PRE + r'''seen = 'v=spf1 redirect=_spf.google.com'
mine = 'v=spf1 include:_spf.google.com include:mailgun.org ip4:203.0.113.0/24 ~all'
def parse(r):
    parts = r.split(); return parts[0], [p for p in parts[1:] if '=' in p.split(':')[0]], [p for p in parts[1:] if p.split(':')[0].lstrip('+-~?') in ('include', 'a', 'mx', 'ptr', 'exists', 'ip4', 'ip6')], parts[-1]
q = {'+': 'pass', '-': 'fail', '~': 'softfail', '?': 'neutral'}
v, mods, mech, last = parse(mine)
out = (parse(seen), v, mods, mech, last, q[last[0]], sum(1 for m in mech if m.split(':')[0] in ('include', 'a', 'mx', 'ptr', 'exists')))'''), "(('v=spf1', ['redirect=_spf.google.com'], [], 'redirect=_spf.google.com'), 'v=spf1', [], ['include:_spf.google.com', 'include:mailgun.org', 'ip4:203.0.113.0/24'], '~all', 'softfail', 2)")),
 ('EmailTrust', 'HeaderInjection', 'NewlineInHeader', 'msg["Subject"] = "hi\\r\\nBcc: evil@example.net"',
  'EmailMessage refuses a header value with a line break (ValueError: Header values may not contain linefeed or carriage return characters), the legacy MIMEText that ezgmail uses raised HeaderParseError (header value appears to contain an embedded header) when the text was written, and ezgmail.send with a subject that contained a linefeed raised the same error before any API call was made.',
  (X(_PRE + _GM + r'''def modern():
    m = EmailMessage(); m['Subject'] = 'hello\r\nBcc: evil@example.net'
def legacy():
    m = MIMEText('body'); m['To'] = 'a@example.com'; m['Subject'] = 'hello\r\nBcc: evil@example.net'; return m.as_string()
e1 = err(modern); e2 = err(legacy)
h = gm({})
e3 = err(lambda: ezgmail.send('a@example.com', 'hello\nBcc: evil@example.net', 'body'))
out = (e1[0], e1[1][:60], e2[0] if e2[0] != 'ok' else [x for x in e2[1].splitlines() if x.lower().startswith(('subject', 'bcc', ' '))], e3[0], e3[1][:60], len(h.log))'''), '(\'ValueError\', \'Header values may not contain linefeed or carriage return ch\', \'HeaderParseError\', \'HeaderParseError\', "header value appears to contain an embedded header: \'hello\\\\n", 0)')),
 ('EmailTrust', 'HeaderInjection', 'CommandInjectionRefused', "subprocess.run('echo ' + subject, shell=True)",
  "A subject of status; echo PWNED run through a shell printed 2 lines, status and PWNED; the same text as an argument of a list printed it whole; an allow-list lookup answered 0 for status and 'refused' for the text status; echo PWNED and for rm -rf /, and shlex.quote made the shell version safe.",
  (X(_PRE + r'''subj = 'status; echo PWNED'
a = subprocess.run('echo ' + subj, shell=True, capture_output=True, text=True).stdout.splitlines()
b = subprocess.run(['echo', subj], capture_output=True, text=True).stdout.splitlines()
ALLOWED = {'status': ['uptime'], 'time': ['date', '+%Y']}
def handle(s): return subprocess.run(ALLOWED[s.strip()], capture_output=True, text=True).returncode if s.strip() in ALLOWED else 'refused'
out = (a, b, handle('status'), handle('status; echo PWNED'), handle('rm -rf /'), shlex.quote(subj), subprocess.run('echo ' + shlex.quote(subj), shell=True, capture_output=True, text=True).stdout.splitlines())'''), '([\'status\', \'PWNED\'], [\'status; echo PWNED\'], 0, \'refused\', \'refused\', "\'status; echo PWNED\'", [\'status; echo PWNED\'])')),
 # ---------------- BookAndPractice
 ('BookAndPractice', 'ListingsAsPrinted', 'ListingsReplay', 'ezgmail.send(...) with no credentials',
  "Run as printed with no credentials, ezgmail.init(), send, unread, search and recent all raised EZGmailException with the same text (Can't find credentials file at DIR/credentials.json.), LOGGED_IN and EMAIL_ADDRESS stayed False; the full replay of the 15 listings in 3 environments is in the third-party record.",
  (X(_PRE + _GM + r'''d = wd()
import ezgmail
def a(): ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email')
def b(): ezgmail.unread()
def c(): ezgmail.search('has:attachment')
def e(): ezgmail.recent()
def f(): ezgmail.summary([])
ezgmail.SERVICE_GMAIL = None
res = [err(x) for x in (a, b, c, e, f)]
out = ([r[0] for r in res], res[0][1].split(' You can')[0].replace(d, 'DIR'), ezgmail.LOGGED_IN, ezgmail.EMAIL_ADDRESS, [r[1].split(' You can')[0].replace(d, 'DIR') == res[0][1].split(' You can')[0].replace(d, 'DIR') for r in res])'''), '([\'EZGmailException\', \'EZGmailException\', \'EZGmailException\', \'EZGmailException\', \'EZGmailException\'], "Can\'t find credentials file at DIR/credentials.json.", False, False, [True, True, True, True, True])')),
 ('BookAndPractice', 'ListingsAsPrinted', 'ExampleDates', 'datetime.datetime.fromtimestamp(1797823712)',
  'str(datetime.datetime.fromtimestamp(1797823712)) is 2026-12-20 21:28:32 only in a zone at UTC-6 such as America/Chicago (offset -6.0 hours); in UTC it is 2026-12-21 03:28:32, in Europe/Istanbul 2026-12-21 06:28:32, and that moment is a Monday 69 days after 2026-10-13.',
  (X(_PRE + r'''ts = 1797823712
os.environ['TZ'] = 'America/Chicago'; time.tzset(); chi = str(DT.fromtimestamp(ts))
os.environ['TZ'] = 'UTC'; time.tzset(); utc = str(DT.fromtimestamp(ts))
os.environ['TZ'] = 'Europe/Istanbul'; time.tzset(); ist = str(DT.fromtimestamp(ts))
out = (chi, utc, ist, str(DT.fromtimestamp(ts, ZoneInfo('America/Chicago'))), DT.fromtimestamp(ts, ZoneInfo('America/Chicago')).utcoffset().total_seconds() / 3600, DT.fromtimestamp(ts, UTC).strftime('%A'), (DT.fromtimestamp(ts, UTC).date() - D(2026, 10, 13)).days)'''), "('2026-12-20 21:28:32', '2026-12-21 03:28:32', '2026-12-21 06:28:32', '2026-12-20 21:28:32-06:00', -6.0, 'Monday', 69)")),
 ('BookAndPractice', 'ListingsAsPrinted', 'AppendixAnswers', "ezgmail.search('has:attachment')",
  'Appendix B answers Question 3 with the text has:attachment passed to search(), which asked the API for users/me/threads?q=has:attachment&maxResults=25 and returned GmailThread objects, and Question 5 with the Requests library, which is true and means no ntfy-specific package is needed; Question 1 says the two files tell EZGmail which account to use, which describes token.json more than credentials.json.',
  (X(_PRE + _GM + r'''h = gm({'threads': [{'id': 'T1', 'snippet': 's', 'historyId': '1'}]})
r = ezgmail.search('has:attachment')
q = h.log[0][1]
out = (q, [type(x).__name__ for x in r], ezgmail.search.__defaults__, 'has:attachment' in q.replace('%3A', ':'))'''), "('users/me/threads?q=has%3Aattachment&maxResults=25&alt=json', ['GmailThread'], (25, 'me'), True)")),
 ('BookAndPractice', 'PracticePrograms', 'UmbrellaReminder', 'probabilityOfPrecipitation',
  "Searching the text of a forecast for the word rain found it in neither of 2 sample periods, so it missed the period with a precipitation chance of 60 (Chance Showers And Thunderstorms) that a comparison with a limit of 40 flagged; api.weather.gov answered the point lookup for Chicago and its forecast with periods that carry shortForecast and probabilityOfPrecipitation (a number from 0 to 100 in each of the 14 periods), a number to compare, where the chapter's scraping of weather.gov gives text.",
  (X(_PRE + r'''PERIODS = [{'name': 'Today', 'shortForecast': 'Chance Showers And Thunderstorms', 'detailedForecast': 'A chance of showers and thunderstorms. Sunny.', 'probabilityOfPrecipitation': {'unitCode': 'wmoUnit:percent', 'value': 60}},
           {'name': 'Tonight', 'shortForecast': 'Mostly Cloudy', 'detailedForecast': 'Mostly cloudy, with a low around 50.', 'probabilityOfPrecipitation': {'unitCode': 'wmoUnit:percent', 'value': None}}]
def naive(p): return 'rain' in (p['shortForecast'] + p['detailedForecast']).lower()
def better(p, limit=40): return (p['probabilityOfPrecipitation']['value'] or 0) >= limit
out = ([naive(p) for p in PERIODS], [better(p) for p in PERIODS], [p['probabilityOfPrecipitation']['value'] for p in PERIODS], PERIODS[0]['probabilityOfPrecipitation']['value'] or 0)'''), '([False, False], [True, False], [60, None], 60)')),
 ('BookAndPractice', 'PracticePrograms', 'AutoUnsubscriber', 'List-Unsubscribe',
  'Scanning HTML with html.parser for links whose text says unsubscribe found 1 of 3 candidates (the image link and the link that says opt out were missed), the word occurs 2 times in the HTML, and the List-Unsubscribe header (RFC 2369) with List-Unsubscribe-Post (RFC 8058) gave a mailto: and an https: address without parsing any HTML; opening a link with a browser confirms the address is read.',
  (X(_PRE + r'''from html.parser import HTMLParser
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
m = EmailMessage(); m['List-Unsubscribe'] = '<mailto:unsub@example.com?subject=unsubscribe>, <https://example.com/u?id=1>'; m['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click'
lu = [x.strip('<>') for x in m['List-Unsubscribe'].split(', ')]
out = (p.found, lu, m['List-Unsubscribe-Post'], len(re.findall(r'unsubscribe', HTML, re.I)), [u for u in lu if u.startswith('https://')])'''), "(['https://example.com/u?id=1'], ['mailto:unsub@example.com?subject=unsubscribe', 'https://example.com/u?id=1'], 'List-Unsubscribe=One-Click', 2, ['https://example.com/u?id=1'])")),
 ('BookAndPractice', 'PracticePrograms', 'EmailControlLoop', 'hmac.compare_digest(pw, SECRET)',
  "The Email-Based Computer Control loop checked a password with hmac.compare_digest, ran only commands of an allow-list with Popen and wait (noop exit 0, sleep exit 0), answered bad password for a wrong one and refused rm; the book's Popen of qBittorrent raised FileNotFoundError on Linux, and compare_digest of a non-ASCII str raised TypeError.",
  (X(_PRE + r'''SECRET = 'correct horse'; ALLOW = {'sleep': [sys.executable, '-c', 'import time; time.sleep(0.2)'], 'noop': [sys.executable, '-c', 'pass']}
def check(msgs):
    done = []
    for frm, body in msgs:
        pw, _, cmd = body.partition(':')
        if not hmac.compare_digest(pw.encode(), SECRET.encode()): done.append((frm, 'bad password')); continue
        if cmd not in ALLOW: done.append((frm, 'refused ' + cmd)); continue
        p = subprocess.Popen(ALLOW[cmd]); done.append((frm, cmd, p.wait()))
    return done
r = check([('me@example.com', 'correct horse:noop'), ('x@example.net', 'guess:noop'), ('me@example.com', 'correct horse:rm'), ('me@example.com', 'correct horse:sleep')])
fnf = err(lambda: subprocess.Popen(['C:\\Program Files (x86)\\qBittorrent\\qbittorrent.exe', 'shakespeare_complete_works.torrent']))
out = (r, fnf[0], hmac.compare_digest(b'a', b'a'), err(lambda: hmac.compare_digest('é', 'é'))[0])'''), "([('me@example.com', 'noop', 0), ('x@example.net', 'bad password'), ('me@example.com', 'refused rm'), ('me@example.com', 'sleep', 0)], 'FileNotFoundError', True, 'TypeError')")),
 ('BookAndPractice', 'EditionChange', 'SecondEditionContent', 'smtplib in the 2nd edition',
  "The 2nd edition's chapter 18, Sending Email and Text Messages, mentions smtplib 21 times, imapclient 20, pyzmail 14 and Twilio 31, while chapter 20 of the 3rd edition names smtplib and imaplib only to say EZGmail is better, and replaces them with the Gmail API, the gateway table and ntfy; observed on 2026-10-13. Recorded in the live observations.",
  None),
 ('BookAndPractice', 'EditionChange', 'MissingExampleImplementation', 'an example implementation',
  'Chapter 20 says that a reader who gets stuck on the Email-Based Computer Control program can download an example implementation from the book page of No Starch Press; the page holds none (0 occurrences of an example implementation, of Email-Based, of ezgmail or of ntfy), the online materials hold 91 files and none for this chapter, and phoneAndEmail.py in them belongs to chapter 8. Recorded in the live observations.',
  None),
]

CLAIMS = [
 (X(_PRE + r'''out = (md.version('ezgmail'), md.version('requests'), md.version('oauth2client'), md.version('google-api-python-client'), md.version('aiosmtpd'), md.version('imapclient'), sys.version_info[:2] >= (3, 14))'''), "('2026.4.28', '2.34.2', '4.1.3', '2.201.0', '1.4.6', '4.1.0', True)"),
 (X(_PRE + r'''out = (140 * 8 // 7, 140 // 2, 250 * 4096, round(86400 / 250, 1), 4096 // 2, len('ı'.encode()), len(('ı' * 2049).encode()), (140 - 6) * 8 // 7, (140 - 6) // 2)'''), '(160, 70, 1024000, 345.6, 2048, 2, 4098, 153, 67)'),
 (X(_PRE + r'''out = ((D(2026, 10, 13) - D(2025, 6, 17)).days, D(2025, 6, 17).strftime('%A'), (D(2027, 3, 31) - D(2026, 10, 13)).days, D(2027, 3, 31).strftime('%A'), (D(2027, 3, 31) - D(2026, 10, 13)).days // 7)'''), "(483, 'Tuesday', 169, 'Wednesday', 24)"),
 (X(_PRE + r'''ts = 1797823712
out = (DT.fromtimestamp(ts, UTC).isoformat(), DT.fromtimestamp(ts, ZoneInfo('America/Chicago')).isoformat(), DT.fromtimestamp(ts, ZoneInfo('Europe/Istanbul')).isoformat(), DT.fromtimestamp(ts, UTC).strftime('%A'), ts - 1797823340, 1797866912 - ts)'''), "('2026-12-21T03:28:32+00:00', '2026-12-20T21:28:32-06:00', '2026-12-21T06:28:32+03:00', 'Monday', 372, 43200)"),
 (X(_PRE + r'''out = (round(8 * math.log2(62), 1), 62 ** 8, 16 * 8, len(secrets.token_urlsafe(16)), len('AlSweigartZPgxBQ42'))'''), '(47.6, 218340105584896, 128, 22, 18)'),
 (X(_PRE + r'''out = (2 * 3600 + 30 * 60, 10 * 60, DT.fromtimestamp(1737866912, UTC).isoformat())'''), "(9000, 600, '2025-01-26T04:48:32+00:00')"),
 (X(_PRE + r'''s = 'user=someuser@example.com\x01auth=Bearer ya29.vF9dfd39\x01\x01'
out = (base64.b64encode(s.encode()).decode(), len(base64.b64encode(s.encode())), s.count('\x01'))'''), "('dXNlcj1zb21ldXNlckBleGFtcGxlLmNvbQFhdXRoPUJlYXJlciB5YTI5LnZGOWRmZDM5AQE=', 72, 3)"),
 (X(_PRE + r'''import imaplib
out = (smtplib.SMTP_PORT, smtplib.SMTP_SSL_PORT, imaplib.IMAP4_PORT, imaplib.IMAP4_SSL_PORT, len(imaplib.Commands), imaplib.Commands['IDLE'])'''), "(25, 465, 143, 993, 43, ('AUTH', 'SELECTED'))"),
 (X(_PRE + r'''t = '{"a":1}\n{"a":2}\n'
out = (err(lambda: json.loads(t))[0], [json.loads(x)['a'] for x in t.splitlines()], err(lambda: [json.loads(x) for x in (t + '\n').splitlines()])[0])'''), "('JSONDecodeError', [1, 2], 'JSONDecodeError')"),
 (X(_PRE + r'''import requests
p = requests.Request('GET', 'https://ntfy.sh/AlSweigartZPgxBQ42/json', params={'poll': 1, 'since': '10m'}).prepare()
out = (p.method, p.url)'''), "('GET', 'https://ntfy.sh/AlSweigartZPgxBQ42/json?poll=1&since=10m')"),
 (X(_PRE + r'''out = (eu.formatdate(1797823712, usegmt=True), eu.formatdate(1797823712), eu.format_datetime(DT.fromtimestamp(1797823712, UTC)), eu.parsedate_to_datetime('Mon, 21 Dec 2026 03:28:32 +0000') == DT.fromtimestamp(1797823712, UTC))'''), "('Mon, 21 Dec 2026 03:28:32 GMT', 'Mon, 21 Dec 2026 03:28:32 -0000', 'Mon, 21 Dec 2026 03:28:32 +0000', True)"),
 (X(_PRE + r'''out = (shlex.quote('status; echo PWNED'), shlex.split("a 'b c' d"), shlex.join(['echo', 'x y']))'''), '("\'status; echo PWNED\'", [\'a\', \'b c\', \'d\'], "echo \'x y\'")'),
 (X(_PRE + r'''raw = base64.urlsafe_b64encode(b'To: a@example.com\r\n\r\nhi?>').decode()
out = (raw, '+' in raw, '/' in raw, base64.urlsafe_b64decode(raw))'''), "('VG86IGFAZXhhbXBsZS5jb20NCg0KaGk_Pg==', False, False, b'To: a@example.com\\r\\n\\r\\nhi?>')"),
 (X(_PRE + r'''out = (len('\U0001F600'), len('\U0001F600'.encode('utf-16-le')) // 2, len('ş'.encode('utf-16-le')) // 2, 35 * 2, 36 * 2)'''), '(1, 2, 1, 70, 72)'),
 (X(_PRE + r'''out = ('ı'.upper(), 'İ'.lower() == 'i̇', len('İ'.lower()), 'ı'.isalpha(), 'tamamlandı'.encode('latin-1', 'replace'))'''), "('I', True, 2, True, b'tamamland?')"),
]
ERRORS = []

BEH = [
 ['EmailMessage refuses a line break in a header and the legacy MIMEText refuses it too',
  r'''from email.message import EmailMessage
from email.mime.text import MIMEText
try:
    m = EmailMessage(); m['Subject'] = 'hi\r\nBcc: evil@example.net'
except ValueError as e:
    print(type(e).__name__)
try:
    t = MIMEText('x'); t['Subject'] = 'hi\r\nBcc: evil@example.net'; t.as_string()
except Exception as e:
    print(type(e).__name__)''',
  'ValueError\nHeaderParseError'],
 ['parseaddr gives empty strings for two addresses in one string unless strict is False',
  r'''import email.utils as eu
s = 'real@example.com, evil@example.net'
print(eu.parseaddr(s), eu.parseaddr(s, strict=False))''',
  "('', '') ('', 'real@example.com')"],
 ['a Turkish subject is written as an encoded word and decodes back',
  r'''from email.message import EmailMessage
from email.header import decode_header, make_header
m = EmailMessage(); m['Subject'] = 'Yedekleme bitti şğı'
line = [l for l in m.as_bytes().decode().splitlines() if l.startswith('Subject')][0]
print(line)
print(str(make_header(decode_header(line.split(': ', 1)[1]))))''',
  'Subject: Yedekleme bitti =?utf-8?b?xZ/En8Sx?=\nYedekleme bitti şğı'],
 ['send_message sends the Bcc recipient in the envelope and not in the text (a local server on sockets)',
  r'''import smtplib, socketserver, threading, email
from email.message import EmailMessage
log = []
class H(socketserver.StreamRequestHandler):
    def handle(self):
        w = lambda s: (self.wfile.write(s.encode() + b'\r\n'), self.wfile.flush()); w('220 x'); cmds = []; data = b''
        while True:
            l = self.rfile.readline()
            if not l: break
            c = l.decode().strip(); cmds.append(c); u = c.upper()
            if u.startswith('EHLO'): w('250 x')
            elif u.startswith(('MAIL', 'RCPT')): w('250 ok')
            elif u == 'DATA':
                w('354 go')
                while True:
                    d = self.rfile.readline()
                    if d == b'.\r\n' or not d: break
                    data += d
                w('250 queued')
            elif u == 'QUIT': w('221 bye'); break
            else: w('250 ok')
        log.append((cmds, data))
srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); srv.daemon_threads = True; threading.Thread(target=srv.serve_forever, daemon=True).start()
m = EmailMessage(); m['From'] = 'al@example.com'; m['To'] = 'jon@example.org'; m['Bcc'] = 'secret@example.com'; m['Subject'] = 's'; m.set_content('b')
with smtplib.SMTP('127.0.0.1', srv.server_address[1]) as s: s.send_message(m)
import time
for _ in range(100):
    if log: break
    time.sleep(0.02)
cmds, data = log[0]
print([c.split('<')[1].rstrip('>') for c in cmds if c.upper().startswith('RCPT')], b'secret' in data, email.message_from_bytes(data)['Bcc'])''',
  "['jon@example.org', 'secret@example.com'] False None"],
 ['a str body gets the Content-Length of its UTF-8 bytes and no Content-Type, and an integer header value is refused',
  r'''import requests
r = requests.Request('POST', 'http://127.0.0.1:1/t', data='Yedekleme tamamlandı').prepare()
print(r.body, r.headers.get('Content-Length'), r.headers.get('Content-Type'))
try:
    requests.Request('POST', 'http://127.0.0.1:1/t', data='x', headers={'Priority': 5}).prepare()
except Exception as e:
    print(type(e).__name__)''',
  'Yedekleme tamamlandı 21 None\nInvalidHeader'],
 ['requests.post to a refused port raises ConnectionError and a 429 does not raise until raise_for_status',
  r'''import http.server, threading, requests
class Hd(http.server.BaseHTTPRequestHandler):
    def do_POST(s):
        s.rfile.read(int(s.headers.get('Content-Length') or 0)); s.send_response(429); s.send_header('Content-Length', '0'); s.end_headers()
    def log_message(s, *a): pass
srv = http.server.HTTPServer(('127.0.0.1', 0), Hd); threading.Thread(target=srv.serve_forever, daemon=True).start()
r = requests.post('http://127.0.0.1:%d/t' % srv.server_address[1], 'x')
print(r.status_code, r.ok)
try: r.raise_for_status()
except requests.HTTPError as e: print(type(e).__name__)
srv.shutdown()
try: requests.post('http://127.0.0.1:1/t', 'x', timeout=3)
except requests.ConnectionError as e: print(type(e).__name__)''',
  '429 False\nHTTPError\nConnectionError'],
 ['a topic of 8 random characters of 62 carries 47.6 bits and token_urlsafe(16) 128',
  r'''import math, secrets
print(round(8 * math.log2(62), 1), len(secrets.token_urlsafe(16)), 16 * 8)''',
  '47.6 22 128'],
 ['ezgmail.init with no credentials.json raises EZGmailException and leaves LOGGED_IN False',
  r'''import os, tempfile
os.chdir(tempfile.mkdtemp())
import ezgmail
print(ezgmail.LOGGED_IN, ezgmail.EMAIL_ADDRESS)
try: ezgmail.init()
except ezgmail.EZGmailException as e: print(type(e).__name__, str(e).split(' You can')[0].replace(os.getcwd(), 'DIR'))''',
  "False False\nEZGmailException Can't find credentials file at DIR/credentials.json."],
 ['ezgmail.removeQuotedParts cuts the English form and leaves the day-month form',
  r'''import ezgmail
a = 'ok\n\nOn Sun, Jan 1, 2018 at 12:00 PM Al <a@b.c> wrote:\n> hi'
b = 'ok\n\nOn Sun, 1 Jan 2018 at 12:00, Al <a@b.c> wrote:\n> hi'
print(repr(ezgmail.removeQuotedParts(a)), len(ezgmail.removeQuotedParts(b)) == len(b))''',
  "'ok\\n\\n' True"],
 ['a list argument stays one argument for the program while shell=True makes a second command',
  r'''import subprocess
s = 'status; echo PWNED'
print(subprocess.run('echo ' + s, shell=True, capture_output=True, text=True).stdout.splitlines())
print(subprocess.run(['echo', s], capture_output=True, text=True).stdout.splitlines())''',
  "['status', 'PWNED']\n['status; echo PWNED']"],
 ['hmac.compare_digest refuses a non-ASCII str and accepts bytes',
  r'''import hmac
print(hmac.compare_digest(b'abc', b'abc'), hmac.compare_digest('abc', 'abc'))
try: hmac.compare_digest('é', 'é')
except TypeError as e: print(type(e).__name__)''',
  'True True\nTypeError'],
 ['importing smtpd, asyncore, cgi and imghdr fails in 3.14',
  r'''import importlib
for n in ('smtpd', 'asyncore', 'cgi', 'imghdr'):
    try: importlib.import_module(n); print(n, 'imported')
    except ModuleNotFoundError: print(n, 'gone')''',
  'smtpd gone\nasyncore gone\ncgi gone\nimghdr gone'],
 ['imaplib in 3.14 has idle and the IDLE command, and the parse helpers work',
  r'''import imaplib, datetime
print(hasattr(imaplib.IMAP4, 'idle'), imaplib.Commands['IDLE'])
print(imaplib.ParseFlags(b'1 (FLAGS (\\Seen \\Flagged))'))
print(imaplib.Time2Internaldate(datetime.datetime(2026, 12, 9, 13, 28, 48, tzinfo=datetime.timezone.utc)))''',
  'True (\'AUTH\', \'SELECTED\')\n(b\'\\\\Seen\', b\'\\\\Flagged\')\n"09-Dec-2026 13:28:48 +0000"'],
 ['the default context checks the certificate and the unverified context of the standard library does not',
  r'''import ssl
c = ssl.create_default_context(); n = ssl._create_stdlib_context()
print(c.check_hostname, c.verify_mode.name, n.check_hostname, n.verify_mode.name)''',
  'True CERT_REQUIRED False CERT_NONE'],
 ['an SMS of 160 GSM-7 characters is one segment and 70 UCS-2 characters is one',
  r'''print(140 * 8 // 7, 140 // 2, len('ş' * 70), len(('ş' * 70).encode('utf-16-le')))''',
  '160 70 70 140'],
 ['a json.loads of a ntfy style answer fails whole and works per line',
  r'''import json
t = '{"id":"a","message":"x"}\n{"id":"b","message":"y"}\n'
try: json.loads(t)
except json.JSONDecodeError as e: print(e.msg)
print([json.loads(l)['message'] for l in t.splitlines()])''',
  "Extra data\n['x', 'y']"],
]

BODY = {}
def _b(key, p1, p2):
    BODY[key] = p1 + "\n\n" + p2

# ---- the six subjects ----
_b('GmailApi',
 "The longest section of the chapter teaches the Gmail API through the EZGmail module: the credentials file and token file, send() with attachments, cc and bcc, the GmailThread and GmailMessage objects that unread(), recent() and search() return, and the download of attachments [S]. EZGmail is the author's wrapper over the official Gmail API, and the chapter prefers it to smtplib and imaplib because of the security and anti-spam measures of Gmail [S][EZ].",
 "Four ideas carry this subject: setup covers the credentials, the token, its expiry and the library underneath; sending covers the one request that carries a base64url message, attachments, copies, non-ASCII text and replies; reading covers threads against messages, searches, fields, quoted text and the summary line; attachments covers names, overwriting and a path inside a name. Everything was run with ezgmail 2026.4.28, either with no credentials, which fails, or on a stand-in for the server of Google that returned replies written by this study; no Gmail account was used [T].")
_b('StandardLibraryMail',
 "The chapter names smtplib and imaplib only to say that EZGmail is the better way to reach Gmail [S]. The Python 3.14 documentation describes the modules the chapter leaves out: email builds and parses messages, smtplib is an SMTP client with STARTTLS and login, and imaplib is an IMAP4 client, new in 3.14 with the IDLE command [PY][RFC5321][RFC3501].",
 "Four ideas carry this subject: message objects cover building, MIME structure, header encoding and address parsing; the SMTP client covers STARTTLS, certificate checks, login, the envelope and refused recipients; the IMAP client covers a session, parsing and IDLE; Gmail by protocol covers the endpoints and the XOAUTH2 string. The SMTP side ran against aiosmtpd on 127.0.0.1 and the IMAP side against dovecot 2.3.21 on 127.0.0.1, both local stand-ins for Gmail, and a connection to the real Gmail servers timed out. Under 11 interpreters 19 of 48 items differed, among them smtpd, asyncore and asynchat (gone from 3.12) and cgi, imghdr, sndhdr, nntplib and telnetlib (gone from 3.13) [T].")
_b('SmsGateways',
 "The chapter's second section sends a text message as an email to the SMS gateway of a phone company, lists 12 providers in Table 20-1, and warns that a gateway that works today may not work tomorrow; for reliability it names Twilio [S]. Two providers have since published the end of their gateways [ATT][VZ].",
 "Three ideas carry this subject: addressing covers how the table builds an address and the domain two providers share; the retreat covers the notice of ATT, the notice of Verizon, the DNS records of the 18 domains and what Twilio answered; the limits cover how many characters fit in one message in the GSM-7 and UCS-2 encodings. No text was sent to any phone and no message was sent through Twilio [T].")
_b('NtfyPush',
 "The chapter's third section sends and receives push notifications through the free service ntfy with the Requests library: a POST to a topic URL, the headers Title, Tags and Priority, and a GET of the topic with /json?poll=1 and since [S]. The ntfy documentation describes the same interface, its limits and its event types [NTFY].",
 "Three ideas carry this subject: publishing covers the body, the metadata headers, the encoding of the text and the response object; subscribing covers the poll URL, the lines of JSON and the fields of an event; the service limits cover topic secrecy, the daily and size limits and the health of the service. The publishing side ran against a recorder on 127.0.0.1 that is not ntfy, because nothing was published to ntfy.sh; the service itself was only asked for its health and for the messages of an unused topic [T].")
_b('EmailTrust',
 "The chapter says in its last practice program that it is fairly trivial for hackers to fake a from address, and that the program should require a password [S]. The standards separate the envelope of SMTP from the header of the message, and SPF and DMARC are the records through which a receiver judges the sender [RFC5321][RFC5322][RFC7208][RFC7489].",
 "Three ideas carry this subject: envelope and headers cover the sender and recipients that SMTP carries against those the message shows, the 78-character fold and the message identifier and date; sender authentication covers the DMARC and SPF records of gmail.com as they answered on the day; header injection covers a line break in a header and a command in a subject. The envelope experiments ran against aiosmtpd on 127.0.0.1 and the two records were read by DNS over HTTPS [T].")
_b('BookAndPractice',
 "This subject holds what the chapter itself shows and asks: 15 listings with printed outputs, five practice questions with the answers of Appendix B, and three practice programs, Umbrella Reminder, Auto Unsubscriber and Email-Based Computer Control [S][APPB]. The chapter replaces chapter 18 of the 2nd edition, which taught smtplib, imapclient, pyzmail and Twilio [S2E].",
 "Three ideas carry this subject: the listings as printed cover the replay of all 15 listings, the dates in the examples and the appendix answers; the practice programs cover a forecast, the unsubscribe links and the control loop, each built on local stand-ins; the edition change covers what the 2nd edition taught and the example implementation that the chapter promises. The online materials hold no file for the chapter [T].")

# ---- the twenty mids ----
_b('GmailSetup',
 "The chapter says to enable the Gmail API in the Google Cloud console as for EZSheets in chapter 15, to add the scope https://mail.google.com, and to end with a credentials file and a token file; running import ezgmail and ezgmail.init() without an error shows that it works, and token.json is to be treated like a password [S]. Google documents the flow and the scope that EZGmail asks for [GOOG].",
 "ezgmail 2026.4.28 looks for credentials.json and token.json in the working directory, asks for one scope, and calls init on import without raising; its token file is plain JSON of mode 0o600, and its authorisation library has had no release since 2018. What happens to a refresh token of a project in the Testing state was read on a Google page and not run, because it needs an account [T].")
_b('GmailSending',
 "The chapter sends mail with ezgmail.send(recipient, subject, body), an optional list of attachment names, and the keyword arguments cc and bcc, and notes that Gmail may refuse repeated text and .exe or .zip attachments [S]. The Gmail API takes the whole message as one base64url string in the raw field and joins a reply to a thread by threadId, References and In-Reply-To headers and a matching subject [GOOG].",
 "The message that ezgmail builds was caught on the stand-in before it left: one POST to users/me/messages/send, a legacy MIMEText or multipart/mixed, copies as headers, UTF-8 text in base64 and an encoded-word subject, and a reply that keeps the thread id but not the subject prefix or the reference headers [T].")
_b('GmailReading',
 "The chapter reads mail with unread(), recent() and search(), which return GmailThread objects of up to 25 threads; each thread holds GmailMessage objects with subject, body, timestamp, sender and recipient, and summary() prints a line for each thread [S]. Google's thread listing takes a query q and maxResults, with a default of 100 and a maximum of 500 [GOOG].",
 "Fed with replies written by this study, ezgmail asked for label:UNREAD, label:INBOX and the search text, fetched the messages of a thread by a second request, built a naive timestamp in the zone of the reader, cut the quoted part of a reply only in one English form and shortened a sender written without a space [T].")
_b('GmailAttachments',
 "The chapter says a GmailMessage has an attachments list of file names, that downloadAttachment() and downloadAllAttachments() save to the working directory or to a downloadFolder, and that an existing file with the same name is overwritten [S]. A mail from a stranger controls the file name it carries [GOOG].",
 "On the stand-in the list repeated a name, an unknown name raised AttributeError, an existing file was overwritten as the chapter says, and a name with ../ in it was written outside the folder [T].")
_b('MessageObjects',
 "The email package builds a message as an EmailMessage with set_content(), add_alternative() and add_attachment(), writes headers in the order they were set, encodes non-ASCII header text as encoded words, and parses addresses with email.utils [PY][RFC5322][RFC2045][RFC2047]. The chapter uses none of this directly, because EZGmail builds the message [S].",
 "A message was built, its MIME tree printed, a Turkish subject and a display name with a comma encoded and decoded, and addresses parsed; in every release of this study parseaddr returned empty strings for two addresses in one string [T].")
_b('SmtpClient',
 "smtplib.SMTP connects to a server, ehlo() learns its extensions, starttls() upgrades the connection with RFC 3207, login() authenticates with RFC 4954 and send_message() sends the message to the recipients in To, Cc and Bcc [PY][RFC3207][RFC4954]. RFC 8314 prefers TLS from the start of a submission connection, which is port 465 [RFC8314].",
 "Against aiosmtpd on 127.0.0.1 the steps were run in order: STARTTLS first and AUTH after it, a self-signed certificate refused until trusted, login refused before TLS, Bcc recipients in the envelope but not in the text, and one refused recipient reported without stopping the others [T].")
_b('ImapClient',
 "imaplib.IMAP4 is the client of RFC 3501 with SELECT, SEARCH, FETCH, STORE and EXPUNGE; Python 3.14 added IDLE from RFC 2177, and the ports are 143 and 993 [PY][RFC3501][RFC2177]. The 2nd edition used the imapclient package for the same work [S2E].",
 "Against dovecot 2.3.21 on 127.0.0.1 imaplib logged in after STARTTLS, searched, fetched with and without setting the seen flag, deleted and expunged; imapclient 4.1.0 did the same, and IDLE reported a message that arrived a second later [T].")
_b('GmailByProtocol',
 "Google documents imap.gmail.com on port 993 and smtp.gmail.com on 465 or 587, and says that these servers accept OAuth 2.0 through the SASL XOAUTH2 mechanism [GOOG]. The chapter says only that Gmail does not let a program use the standard protocols as easily as EZGmail does [S].",
 "A connection to the three ports timed out after 10 seconds from this machine, so no login was tried; the XOAUTH2 string was built by hand from the format Google documents and never sent [T].")
_b('GatewayAddressing',
 "An SMS gateway address is the phone number, an @ and the domain of the phone company, as in 2125551234@vtext.com, and Table 20-1 gives an SMS domain and an MMS domain for 12 providers [S]. The subject and body of the email become the body of the text message [S].",
 "The table was typed in as data and the addresses built from it: 12 rows, 11 distinct SMS domains because two providers share one, and 5 rows whose MMS domain is the same as the SMS domain [T].")
_b('GatewayRetreat',
 "The chapter lists five disadvantages of the gateways and says that one that works today may not work tomorrow [S]. ATT's support article says its gateway ended in 2025, Verizon's notice says its gateway is being shut down, and Twilio is the paid service the chapter names instead [ATT][VZ][TWILIO].",
 "The dates of the two notices were counted from 13 October 2026, the MX records of the 18 domains of the table were asked by DNS over HTTPS, and Twilio's REST API was asked once without credentials; no text was sent [T].")
_b('SmsLimits',
 "The chapter says that SMS gateways limit a message to 160 characters and MMS has no limit [S]. The limit comes from the encoding: 140 bytes hold 160 characters of 7 bits in GSM-7, and 70 characters of 16 bits when a character outside the set forces UCS-2 [TWILIO].",
 "Counting functions written for the study gave 1 segment for 160 plain characters, 2 for 161, a double count for the extension characters, and 1 for 70 Turkish characters against 2 for 71 [T].")
_b('NtfyPublishing',
 "The chapter publishes with requests.post(url, 'Hello, world!') and adds the headers Title, Tags and Priority as a dictionary; it says the free limits are 250 messages a day and 4,096 bytes a message [S]. The ntfy documentation says the body is the message and the headers carry the metadata [NTFY].",
 "Against a recorder on 127.0.0.1 the request carried the 13 bytes of the body and no content type, the three headers arrived unchanged, an integer priority and a dotless i in a header were refused by Requests, a str body went out as UTF-8, and a 429 answer raised nothing [T].")
_b('NtfySubscribing',
 "The chapter reads a topic with requests.get(url + '/json?poll=1'), optionally with since=10m, since=2h30m, a timestamp or a message id, and parses the answer line by line with json.loads [S]. The ntfy documentation lists six event types and the fields of a message [NTFY].",
 "The poll URL was built with params, the book's answer was parsed as lines, and the fields were counted from the printed answer; the real service answered only a poll of an unused topic [T].")
_b('NtfyServiceLimits',
 "The chapter says that the topic name is a password, that the free limits are 250 messages a day and 4,096 bytes, and that flooding may get an IP address blocked [S]. The ntfy FAQ says that without access control the name of a topic is the only protection [NTFY].",
 "The entropy of the book's topic, the size in bytes of a limit-sized text, and the arithmetic of 250 messages were computed; the health endpoint of ntfy.sh answered healthy and a poll of an unused topic answered with an empty body [T].")
_b('EnvelopeAndHeaders',
 "SMTP carries an envelope, MAIL FROM and RCPT TO, and a message with headers From, To and Date; RFC 5321 defines the envelope and RFC 5322 the message, whose lines are capped at 998 characters with 78 recommended [RFC5321][RFC5322]. The chapter's remark that a from address is easy to fake rests on this split [S].",
 "A local server received an envelope sender and recipient that differed from the header; the default policy folded a long subject at 78 characters; and Message-ID and Date were generated with fixed arguments [T].")
_b('SenderAuthentication',
 "SPF publishes in DNS which hosts may send for a domain, and DMARC publishes what a receiver should do with a message that fails both SPF and DKIM alignment; both are TXT records [RFC7208][RFC7489]. Google's sender guidelines require them from senders of more than 5,000 messages a day to Gmail [GOOG].",
 "The records of gmail.com were read by DNS over HTTPS on 2026-10-13 and parsed by functions written for the study; the chapter does not mention SPF, DKIM or DMARC [T].")
_b('HeaderInjection',
 "A header value that contains a line break lets its writer add headers of his own; the email package and ezgmail refuse it, and a subject that reaches a shell can add commands the same way [PY][RFC5322]. The chapter's last program runs programs on the strength of an email, which is the risky case [S].",
 "EmailMessage refused the line break, the legacy MIMEText refused it when the text was written, and a subject run through a shell printed the injected command until it was passed as a list argument or checked against an allow-list [T].")
_b('ListingsAsPrinted',
 "The chapter prints 15 listings with their outputs and a date in 2026 in several of them [S]. A reader who types the listings meets the Google Cloud steps first, because ezgmail cannot send or read without a credentials file [S].",
 "The 48 statements were replayed in 3 environments and in two zones; the record of the replay is in the third-party record file [T].")
_b('PracticePrograms',
 "The chapter asks for three programs: an Umbrella Reminder that checks weather.gov and texts the reader, an Auto Unsubscriber that finds unsubscribe links in all mail and opens them with webbrowser, and an Email-Based Computer Control that checks mail or ntfy every 15 minutes, requires a password, runs the instruction and deletes the mail [S]. The National Weather Service documents the API that the first one can use [NWS].",
 "Each was built in small, on stand-ins: a forecast structure, an HTML parser against the List-Unsubscribe header, and a loop of SMTP, IMAP and Popen [T].")
_b('EditionChange',
 "Chapter 20 of the 3rd edition replaces chapter 18 of the 2nd edition, Sending Email and Text Messages, which taught smtplib, imapclient, pyzmail and Twilio [S][S2E]. The chapter ends by pointing to the book's page for an example implementation [S].",
 "The 2nd edition page was fetched and its names counted, and the book page and the online materials were searched for the promised example [T].")


# ---- GmailApi leaves ----
_b('CredentialsAndToken',
 "The chapter ends the setup with a credentials file and a token file and tests it with import ezgmail and ezgmail.init(): if no error appears, EZGmail has been correctly installed [S]. The README of EZGmail says the same two files must be in the folder of the program [EZ].",
 "With no credentials.json in the working directory ezgmail.init() raised EZGmailException (Can't find credentials file at DIR/credentials.json.) and ezgmail.LOGGED_IN and ezgmail.EMAIL_ADDRESS stayed False; the scope was https://mail.google.com/ and the version 2026.4.28. The chapter's test therefore fails on any machine where the Google Cloud steps were not done [T].")
_b('ImportRunsInit',
 "The chapter shows import ezgmail and ezgmail.init() as two lines, as if the import did nothing [S]. The source of the package ends with a call of init that hides its exception [EZ].",
 "The last line of the installed package is init(_raiseException=False), so importing it already tries to log in; init takes userId, tokenFile (default token.json), credentialsFile (default credentials.json) and _raiseException (default True), and its source calls run_flow, the browser authorisation of oauth2client [T].")
_b('TokenFileContents',
 "The chapter says token.json is to be treated like a password, because anyone who has it can use the Gmail account but cannot change its password, and that a token is revoked in the Google Cloud console [S]. Google's page on OAuth 2.0 describes the refresh token that such a file holds [GOOG].",
 "A token.json written by oauth2client with dummy values held 16 keys as plain JSON, among them client_id, client_secret, access_token and refresh_token; the file mode was 0o600 and reading it back gave the same refresh token. The chapter's advice is right [T].")
_b('TestingModeExpiry',
 "The chapter says nothing about the publishing status of the Google Cloud project [S]. Google's OAuth page says that a project whose consent screen is of the external type and in the status Testing is issued a refresh token that expires in 7 days [GOOG].",
 "This was read on the page and not run, because it needs a Google account and a week; a reader who follows the chapter with a new project may find the browser authorisation asked for again after a week. Not executed [T].")
_b('DeprecatedOauthLibrary',
 "The chapter does not name the library under the login of EZGmail [S]. The package metadata of ezgmail lists google-api-python-client and oauth2client as requirements [PYPI].",
 "ezgmail 2026.4.28 required both; oauth2client 4.1.3 was uploaded on 2018-09-07 and is classified Development Status 7 - Inactive, while google-api-python-client was at 2.201.0, uploaded 2026-09-30 [T].")
_b('SendCall',
 "The chapter sends mail with one call, ezgmail.send('recipient@example.com', 'Subject line', 'Body of the email') [S]. The Gmail API accepts the message as one base64url string in the raw field of a POST to users/me/messages/send [GOOG].",
 "On the stand-in the call made one POST to users/me/messages/send?alt=json whose JSON body had the single key raw; the message had the headers Content-Type, MIME-Version, Content-Transfer-Encoding, to, from and subject, was text/plain and 7bit for an ASCII body [T].")
_b('AttachmentParts',
 "The chapter attaches files by an extra list argument, and says Gmail might refuse .exe or .zip attachments [S]. Google's help page lists .exe among the file types Gmail blocks and gives 25 MB as the size limit of an attachment [GOOG].",
 "The message was multipart/mixed with the text first and one base64 part per file, typed by extension: image/jpeg, audio/mpeg, application/x-msdos-program for setup.exe and application/zip for notes.zip; ezgmail did not refuse the .exe or the .zip, and a missing file raised EZGmailException. Whether Google accepted them was not tried [T].")
_b('CcAndBccHeaders',
 "The chapter sends carbon copies with cc and blind copies with bcc, the latter as a comma-joined string [S]. Google's sending guide takes the recipients from the To, Cc and Bcc headers of the message [GOOG].",
 "The To, Cc and Bcc headers were written in the raw message, and the comma-joined bcc string was parsed into 2 addresses [T].")
_b('NonAsciiText',
 "The chapter's examples are English and ASCII [S]. The MIME standards encode non-ASCII text with a charset and a transfer encoding, and non-ASCII header text as encoded words [RFC2045][RFC2047].",
 "The body of a Turkish text became charset utf-8 in base64 and came back unchanged, the subject became an encoded word (=?utf-8?b?...?=), and a mimeSubtype that is not plain or html raised EZGmailValueError [T].")
_b('ReplyThreading',
 "The chapter does not use GmailMessage.reply [S]. Google's sending guide says a message joins a thread when its threadId is given, its References and In-Reply-To headers follow RFC 2822 and its Subject headers match [GOOG].",
 "reply() posted a message to the sender with the threadId of the original, but with the subject unchanged (RoboCop, no Re:) and without In-Reply-To or References; replyAll() made no API call at all and returned None [T].")
_b('ThreadVersusMessage',
 "The chapter says a GmailThread holds a messages list of GmailMessage objects, that Gmail shows conversations, and prints the text of the first thread as a GmailThread with len=2 and a snippet [S][APPB]. Question 2 of Appendix B answers that a message is a single email and a thread a conversation of several [APPB].",
 "A thread held an id, a snippet and a historyId, and fetched its messages with one more GET (users/me/threads/T1) the first time messages was read; its text was <GmailThread numMessages=2 snippet='Do you want to watch RoboCop this weekend?'>, not the printed one, and building that text itself cost an API call [T].")
_b('UnreadRecentSearch',
 "The chapter says unread() and recent() return the 25 most recent threads, that maxResults changes the limit, and that search() takes the operators of the Gmail search box [S][GOOG]. Google's list call has a default of 100 and a maximum of 500 for maxResults [GOOG].",
 "unread asked for q=label:UNREAD, recent for q=label:INBOX and search for the text it was given, each with maxResults 25 by default and 50 when asked; the default of all three in the package was 25 [T].")
_b('MessageFields',
 "The chapter lists subject, body, timestamp, sender and recipient as the attributes of a message and prints a timestamp of datetime.datetime(2026, 12, 9, 13, 28, 48) [S]. The package takes the time from the internalDate field of the API reply [EZ].",
 "timestamp was a naive datetime made from internalDate with fromtimestamp, so the same message read 08:48:48 in America/Chicago, 14:48:48 in UTC and 17:48:48 in Europe/Istanbul; a message with no Subject header raised AttributeError on .subject and on str() [T].")
_b('QuotedTextCut',
 "The chapter does not mention removeQuotedParts [S]. The README of EZGmail says the body may carry the quoted earlier mails of a reply [EZ].",
 "The function cut a reply at the English line On Sun, Jan 1, 2018 at 12:00 PM Name <address> wrote:, and did not cut the forms On Sun, 1 Jan 2018 at 12:00, a Turkish line, or the English line with the narrow no-break space U+202F before PM; this study did not observe which mail programs write that space [T].")
_b('SummaryLine',
 "The chapter prints summary() as Al, Jon - Do you want to watch RoboCop this weekend? - Dec 09 [S]. The function builds the line from the first names of the senders, the snippet and the month and day [EZ].",
 "The line was Al, Jon - Do you want to watch RoboCop this weekend? - Dec 11 for the dates of the test, and a sender written without a space lost its last character: noreply@example.com was printed as noreply@example.co [T].")
_b('AttachmentNames',
 "The chapter says attachments is a list of file names and that any of them can be passed to downloadAttachment [S]. The names are returned as found in the message, one for each attached file [EZ].",
 "The list was ['tulips.jpg', 'canal.jpg', 'canal.jpg'], the body of the multipart message was the text part only, and downloadAttachment with a name not in the list raised AttributeError [T].")
_b('DownloadOverwrite',
 "The chapter says that a file of the same name is overwritten by the download and shows downloadAllAttachments(downloadFolder='vacation2026') [S].",
 "An existing tulips.jpg went from MINE to AAAA, as the chapter says; downloadAllAttachments created the folder, fetched every attachment again and saved canal.jpg with the bytes of its own attachment id [T].")
_b('FilenameTraversal',
 "The chapter does not say that an attachment name comes from the sender [S]. A message from a stranger controls the file name it carries [S].",
 "An attachment named ../evil.txt was written one level above the download folder: inbox stayed empty, evil.txt appeared beside it, and downloadAllAttachments returned ['../evil.txt']; os.path.basename gives evil.txt, which a careful program uses [T].")

# ---- StandardLibraryMail leaves ----
_b('EmailMessageBuild',
 "EmailMessage is the class of the email package that builds a message: headers are set like dictionary items and set_content() writes the body, with a default policy that serialises with LF line ends [PY][RFC5322]. The chapter never builds a message, because EZGmail does [S].",
 "The headers came out in the order they were set (From, To, Subject, Date, Message-ID, then Content-Type, Content-Transfer-Encoding 7bit and MIME-Version); as_bytes() had 0 CRLF and as_bytes(policy=policy.SMTP) had 10, and a message read back kept the display name Jon Doe apart from jon@example.org [T].")
_b('MimeTree',
 "A message with text, HTML and a file is a tree of MIME parts: multipart/mixed holding multipart/alternative and the attachment [RFC2045][PY]. The chapter's attachments are always files, never an HTML alternative [S].",
 "add_alternative and add_attachment gave multipart/mixed, multipart/alternative, text/plain, text/html and application/octet-stream; get_body with the preference html returned the html part, and iter_attachments found poster.bin [T].")
_b('HeaderEncoding',
 "RFC 2047 encodes non-ASCII header text as encoded words, and the email package does it automatically, or writes raw UTF-8 under a policy with utf8=True [RFC2047][PY]. The chapter sends English subjects only [S].",
 "A Subject with a check mark and Turkish letters became =?utf-8?b?4pyTIMWfxJ/EsQ==?=, a display name with a comma and a dotless i became =?utf-8?q?Y=C4=B1lmaz=2C_Ay=C5=9Fe?=, and decode_header with make_header gave the text back; with utf8=True the header was raw UTF-8 [T].")
_b('AddressParsing',
 "email.utils.parseaddr and getaddresses split a header value into display names and addresses; the 3.14 documentation says that strict, added in 3.13, makes parseaddr return ('', '') for malformed input, which is now the default [PY]. The chapter writes addresses as plain strings [S].",
 "parseaddr split Al Sweigart <al@inventwithpython.com> into a name and an address; given two addresses in one string it returned ('', '') in all 11 interpreters of the study (the builds 3.11.17 and 3.12.3 behaved like 3.13 and later) and ('', 'real@example.com') with strict=False, and getaddresses kept a quoted name with a comma whole but split it in two without the quotes [T].")
_b('StarttlsSession',
 "A client connects on port 587, calls ehlo(), upgrades with starttls() (RFC 3207) and only then logs in; Google names smtp.gmail.com for these steps [PY][RFC3207][GOOG]. The chapter does not use smtplib [S].",
 "On aiosmtpd the server advertised STARTTLS before and AUTH LOGIN PLAIN only after it, STARTTLS was answered 220, send_message returned {} and the server saw the session as TLS with envelope sender al@example.com and recipient jon@example.org; the 3.13 builds sent their commands in lower case (mail from:) where 3.12.3 sent mail FROM:, and the keyfile and certfile arguments of starttls are gone from 3.12 [T].")
_b('CertificateVerification',
 "The ssl documentation recommends create_default_context() for a client because it turns on certificate and host name checking [PY]. A server with a self-signed certificate is therefore refused by a default context.",
 "starttls() with the default context raised SSLCertVerificationError (self-signed certificate); starttls() with no context succeeded (220) on a context with verify_mode CERT_NONE and so encrypted without authenticating the server; a context from create_default_context(cafile=...) had check_hostname True and verify_mode CERT_REQUIRED and connected to localhost; from 3.13 the default context also sets VERIFY_X509_STRICT and VERIFY_X509_PARTIAL_CHAIN and a minimum of TLS 1.2, which the 3.12.3 build did not [T].")
_b('LoginAfterTls',
 "RFC 4954 defines the AUTH command, and a server may offer it only on an encrypted connection; smtplib.login() raises SMTPNotSupportedError if AUTH is not offered [RFC4954][PY].",
 "login before STARTTLS raised SMTPNotSupportedError (SMTP AUTH extension not supported by server) because the server offered AUTH only after TLS; after STARTTLS login returned (235, 'Authentication successful') and a wrong password raised SMTPAuthenticationError with code 535 [T].")
_b('EnvelopeRecipients',
 "smtplib.send_message() takes the recipients from the To, Cc and Bcc headers and, as its documentation says, does not transmit any Bcc header [PY][RFC5321]. The chapter's bcc argument relies on the same idea [S].",
 "RCPT TO was sent for jon@example.org, secret@example.com and friend@example.com; the Bcc header was None at the server and the secret address was nowhere in the text, and the message object still had its Bcc header after sending [T].")
_b('RefusedRecipients',
 "send_message() returns a dictionary of the recipients the server refused and raises SMTPRecipientsRefused only when all were refused [PY][RFC5321]. The chapter has no word on refused recipients [S].",
 "When the server refused one of two recipients with 550 the dictionary named the refused address and the message was stored for the other; when every recipient was refused it raised SMTPRecipientsRefused and nothing was stored [T].")
_b('ImapSession',
 "imaplib.IMAP4 connects, upgrades with starttls(), logs in, selects a mailbox, searches, fetches, marks messages deleted and expunges, as RFC 3501 describes [PY][RFC3501]. The chapter leaves this to EZGmail [S].",
 "Against dovecot 2.3.21 on 127.0.0.1 a fetch with BODY.PEEK left the message unseen, a fetch of RFC822 set \\Seen, expunge left the INBOX empty, and a wrong password raised imaplib.IMAP4.error with the answer AUTHENTICATIONFAILED; imapclient 4.1.0 did the same search, fetch and delete. Not run against Gmail [T].")
_b('ImapParsing',
 "imaplib provides ParseFlags, Internaldate2tuple, Time2Internaldate and Int2AP for the strings of the protocol [PY][RFC3501].",
 "ParseFlags returned (b'\\Seen', b'\\Flagged'), Internaldate2tuple turned 17-Jul-1996 02:44:25 -0700 into a time tuple, Time2Internaldate wrote an aware datetime as 09-Dec-2026 13:28:48 +0000, the ports were 143 and 993, and the Commands table had 43 entries [T].")
_b('ImapIdle',
 "IDLE (RFC 2177) lets the server tell the client about new mail, and Python 3.14 added IMAP4.idle() for it [RFC2177][PY]. The chapter's control program polls every 15 minutes instead [S].",
 "Under 3.14.6 imaplib.IMAP4 had idle and IDLE was in Commands for the states AUTH and SELECTED, and the interpreter record shows 3.11, 3.12 and 3.13 without it; against dovecot idle() reported an EXISTS event for a message that arrived a second later [T].")
_b('GmailEndpoints',
 "Google documents imap.gmail.com on 993 with SSL, and smtp.gmail.com on 465 with SSL or 587 with STARTTLS [GOOG]. The chapter names no host [S].",
 "A TCP connection from this machine to the three ports timed out after 10 seconds, so no Gmail server was reached and no login was tried. Not executed against Gmail [T].")
_b('XoauthString',
 "The SASL XOAUTH2 initial response is user=NAME, Control-A, auth=Bearer TOKEN, two Control-A, in base64, as Google documents [GOOG]. The chapter does not touch this level [S].",
 "For someuser@example.com and ya29.vF9dfd39 the string was 72 characters of base64 that decoded to the three Control-A separated fields; it was built by hand and never sent to Google [T].")


# ---- SmsGateways leaves ----
_b('GatewayAddress',
 "Table 20-1 lists 12 providers with an SMS gateway and an MMS gateway, written number@domain, and the text says the number and the domain of the phone company make up the recipient address [S]. Five rows say Same as SMS for the MMS gateway [S].",
 "The table was typed in as data: 12 rows, 5555550100@txt.att.net for SMS and 5555550100@mms.att.net for MMS of ATT, 5 rows with the same address for MMS; nothing in the table says how a number is written for a provider that wants a country code or no dashes [T].")
_b('SharedGateway',
 "Verizon and Xfinity Mobile have the same SMS gateway, number@vtext.com, in Table 20-1, and different MMS gateways, vzwpix.com and mypixmessages.com [S].",
 "Of the 12 rows only 11 SMS domains were distinct, and the address 5555550100@vtext.com did not say which carrier was meant [T].")
_b('AttNotice',
 "Table 20-1 begins with ATT and its txt.att.net and mms.att.net gateways, and the chapter warns that a gateway that works today may not work tomorrow [S]. ATT's support article says that on June 17, 2025 its email-to-text and text-to-email service was shut down [ATT].",
 "That date is 483 days before 2026-10-13 and a Tuesday; the table still lists the two domains, so the warning of the chapter came true for the first row [T].")
_b('VerizonNotice',
 "The chapter's own example sends a text to 2125551234@vtext.com [S]. Verizon's notice says it has begun to shut down email-to-text for Vtext.com and VZWPix.com, expects to complete it by 03/31/2027, and says some senders may lose access earlier [VZ].",
 "31 March 2027 is a Wednesday and 169 days after 2026-10-13, so the gateway of the chapter's example is on a schedule to end [T].")
_b('DomainStatus',
 "The chapter says a gateway is an email server of the phone company, which means its domain should have mail exchanger records in DNS [S][RFC5321].",
 "A DNS-over-HTTPS query on 2026-10-13 for the MX records of the 18 gateway domains of Table 20-1 found none for txt.att.net and mms.att.net (NOERROR with no records) and none for sms.cricketwireless.net (NOERROR, with names that carry no MX priority), NXDOMAIN for messaging.sprintpcs.com and pm.sprint.com and SERVFAIL for sms.myboostmobile.com, and mail exchangers for the other 12; a missing MX is a symptom, not proof that delivery fails. Recorded in the live observations [T].")
_b('TwilioInstead',
 "The chapter names the API of a telecom service provider such as Twilio as the more reliable way to send texts, and says such services often require a subscription or fees and an application [S]. Twilio's compliance documentation describes the registration that senders of application-to-person texts to US numbers go through [TWILIO].",
 "Twilio's REST API answered a request with no credentials with HTTP 401, code 20003 and the message Authentication Error - No credentials provided, which is all this study could observe without an account. No message was sent. Not executed [T].")
_b('Gsm7Length',
 "The chapter says an SMS gateway limits a message to 160 characters [S]. Twilio's page explains that an SMS carries 140 bytes, which hold 160 characters of 7 bits in GSM-7, and that a character such as { or ] needs an escape and counts as two [TWILIO].",
 "Counting with a GSM-7 table written for the study, 160 characters of the basic set fit one message and 161 needed 2, {x} cost 5, and Yedekleme tamamlandi without the dotless i was 20 characters; a longer text is split into segments of 153 characters, a figure that comes from the arithmetic of a 6-byte header and was not found on a page opened by this study [T].")
_b('Ucs2Length',
 "Twilio's page says devices change to UCS-2, which uses 16 bits per character, when a text needs a character outside the GSM-7 tables [TWILIO]. The chapter does not mention encodings [S].",
 "The dotless i of Yedekleme tamamlandı made the whole text UCS-2: 70 characters fit one message and 71 needed 2, an emoji was 2 code units so 35 emoji fit and 36 did not; segments of 67 characters follow by the same arithmetic and were not confirmed from a page opened by this study [T].")

# ---- NtfyPush leaves ----
_b('PostBody',
 "The chapter publishes with requests.post('https://ntfy.sh/AlSweigartZPgxBQ42', 'Hello, world!') and says it is a POST, unlike the GET of chapter 13 [S]. The ntfy documentation says the body of the request is the message [NTFY].",
 "On a recorder on 127.0.0.1 that stands in for the service, the request was a POST to /AlSweigartZPgxBQ42 with the 13 bytes as body, Content-Length 13, no Content-Type and a python-requests User-Agent, and returned a Response with status 200; the recorder is not ntfy [T].")
_b('MetadataHeaders',
 "The chapter sends Title, Tags and Priority as HTTP headers in a dictionary, with a priority from 1 to 5 whose default is 3 [S].",
 "The three headers arrived unchanged (Title Important: Read this!, Tags warning,neutral_face, Priority 5); a Priority given as the integer 5 raised InvalidHeader because header values must be str or bytes, and a Title with a dotless i raised UnicodeEncodeError because Requests encodes header values as latin-1 [T].")
_b('BodyEncoding',
 "The chapter posts English text only [S]. HTTP says nothing of the charset of a body without a Content-Type, and ntfy's documentation speaks of messages that consist of non UTF-8 characters being turned into attachments [NTFY].",
 "With urllib3 2.8.0 a str body was sent as UTF-8, 21 bytes for the 20 characters of Yedekleme tamamlandı, with no Content-Type, so a receiver has to assume the charset; encoding by hand to latin-1 with replace gave a question mark, and an explicit Content-Type text/plain; charset=utf-8 was passed through [T].")
_b('ResponseObject',
 "The chapter does not use the Response that post returns, and says that a reserved topic gives a Response with status 403 [S]. Requests raises for a bad status only when raise_for_status() is called.",
 "When the recorder answered 429 with a body written by this study, post returned a Response with ok False and raised nothing, and only raise_for_status() raised HTTPError (429 Client Error: Too Many Requests), so a program that notifies about a long job fails silently when a limit is reached [T].")
_b('PollUrl',
 "The chapter polls with a GET of https://ntfy.sh/AlSweigartZPgxBQ42/json?poll=1 and a since parameter that takes 10m, 2h30m, a Unix timestamp or a message id [S][NTFY].",
 "requests built the same query from params={'poll': 1, 'since': '2h30m'}, and all four URLs reached the recorder as GET [T].")
_b('JsonLines',
 "The chapter says the answer is not valid JSON, because it holds a JSON object on each line, so it uses splitlines() and json.loads() on each line [S]. The ntfy documentation names a way to subscribe as a JSON stream, with the fields of a message in a table [NTFY].",
 "json.loads of the whole text raised JSONDecodeError (Extra data: line 2 column 1); splitlines then loads gave the 2 messages Hello, world! and The rent is too high!, and a blank line, which a stream can contain, raised JSONDecodeError again [T].")
_b('EventFields',
 "The chapter lists the keys id, time, expires, event, topic, title, message, priority and tags, and four event values: message, open, keepalive and poll_request [S]. The ntfy documentation lists six: open, keepalive, message, message_delete, message_clear and poll_request [NTFY].",
 "The first message of the book's answer has the keys id, time, expires, event, topic and message and the second adds title, priority 5 and tags; expires minus time is 43200 seconds, 12 hours; and time 1797823712 is 2026-12-21T03:28:32 in UTC [T].")
_b('TopicSecrecy',
 "The chapter says to treat the topic name as a password and uses AlSweigartZPgxBQ42 in its examples [S]. ntfy's FAQ says that without access control the topic name is the password and that a randomly generated name is as good as a good password [NTFY].",
 "The random part of the book's topic, ZPgxBQ42, is 8 characters of 62, 47.6 bits, and the other half is the author's name; secrets.token_urlsafe(16) gives 22 characters of 128 bits; the topic is part of the URL path, so it appears in logs [T].")
_b('DailyAndSize',
 "The chapter says free users are limited to 250 messages a day and messages to 4,096 bytes [S]. The ntfy documentation says a longer message is treated as an attachment [NTFY].",
 "The limit is bytes, not characters: 4096 ASCII characters are 4096 bytes and 4097 are over, while 2049 dotless i characters are 4098 bytes; 250 messages of 4096 bytes are 1,024,000 bytes a day, one message every 345.6 seconds on average [T].")
_b('ServiceHealth',
 "The ntfy server has a health endpoint at /v1/health, and the chapter's link https://ntfy.sh answers the web app [NTFY][S].",
 "GET https://ntfy.sh/v1/health answered 200 with healthy true, and a GET poll of a random, unused topic answered 200 with an empty body and the content type application/x-ndjson; nothing was published to ntfy.sh by this study. Recorded in the live observations [T].")

# ---- EmailTrust leaves ----
_b('EnvelopeVersusHeader',
 "SMTP separates the envelope from the message: MAIL FROM and RCPT TO name the sender and recipients, while the From and To headers are text that the sender writes [RFC5321][RFC5322]. The chapter says it is fairly trivial for hackers to fake a from address [S].",
 "A local server received MAIL FROM bounces@mallory.example and RCPT TO jon@example.org and hidden@example.org while the message said From: CEO <ceo@bank.example> and To: Jon Doe <jon@example.org>, with no login and no TLS; the hidden address was nowhere in the text, and the From was whatever the sender wrote [T].")
_b('HeaderLineLimits',
 "RFC 5322 caps a line at 998 characters and recommends 78, and long header values are folded [RFC5322]. The policy objects of the email package carry a max_line_length [PY].",
 "The default policy folded at 78 (policy.SMTP also had 78 and CRLF as line end): a 300-character Subject of words became 5 lines of at most 78, and a 1200-character Subject without spaces was written as encoded words over 19 lines of at most 78 and read back as the original [T].")
_b('MessageIdAndDate',
 "Every message should carry a Message-ID and a Date header [RFC5322]. The email.utils module provides make_msgid(), formatdate() and format_datetime() for them [PY].",
 "make_msgid(idstring='job1', domain='example.com') gave <...job1@example.com> and two calls differed; formatdate(1797000528, usegmt=True) was Fri, 11 Dec 2026 14:48:48 GMT, without usegmt it ended -0000, and format_datetime of an aware UTC moment ended +0000 and parsed back to the same instant [T].")
_b('DmarcRecordParse',
 "A DMARC record is a TXT record at _dmarc.domain of tag=value pairs separated by semicolons, with the tags v, p, sp, rua, pct, adkim and aspf [RFC7489]. Google's sender guidelines require DMARC from senders of more than 5,000 messages a day [GOOG]. The chapter does not mention it [S].",
 "The record observed for _dmarc.gmail.com on 2026-10-13 was v=DMARC1; p=none; sp=quarantine; rua=mailto:mailauth-reports@google.com, a policy of none for the domain and quarantine for subdomains; a stricter sample had p=reject, pct=100, adkim=s and aspf=r [T].")
_b('SpfRecordParse',
 "An SPF record is a TXT record that begins v=spf1 followed by mechanisms and modifiers, such as include, ip4, redirect and the qualifier at the end, and a check is limited to 10 mechanisms and modifiers that cause DNS lookups [RFC7208]. The chapter does not mention it [S].",
 "The TXT record observed for gmail.com on 2026-10-13 was v=spf1 redirect=_spf.google.com, which sends the check to another name; a sample with 2 include mechanisms, an ip4 range and ~all (softfail) had 2 mechanisms that cost a DNS lookup [T].")
_b('NewlineInHeader',
 "A line break in a header value lets its writer start another header, Bcc for instance; the email package refuses it [PY][RFC5322]. The chapter takes the subject from the caller [S].",
 "EmailMessage raised ValueError (Header values may not contain linefeed or carriage return characters); the legacy MIMEText that ezgmail uses raised HeaderParseError (header value appears to contain an embedded header) when the text was written, and ezgmail.send with a subject that contained a linefeed raised the same error before any API call was made [T].")
_b('CommandInjectionRefused',
 "The last practice program runs the instruction found in an email with subprocess.Popen, and requires a password in the mail [S]. Text from a stranger's email that reaches a shell is the case that follows from this.",
 "A subject of status; echo PWNED run through a shell printed 2 lines, status and PWNED; the same text as an argument of a list printed it whole; an allow-list lookup answered 0 for status and refused for the text status; echo PWNED and for rm -rf /, and shlex.quote made the shell version safe [T].")

# ---- BookAndPractice leaves ----
_b('ListingsReplay',
 "The chapter's listings are typed into the interactive shell in order, from import ezgmail to the Popen of qBittorrent [S].",
 "Run as printed with no credentials, init(), send, unread, search and recent all raised EZGmailException with the same text (Can't find credentials file at DIR/credentials.json.) and LOGGED_IN and EMAIL_ADDRESS stayed False; of the 48 statements 19 matched the book with ezgmail 2026.4.28 and 19 with the Requests version of Appendix A, and 3 in an environment with neither package; on the stand-in 42 of 46 matched, and in the zone Europe/Istanbul 38 [T].")
_b('ExampleDates',
 "The chapter prints datetime.datetime.fromtimestamp(1797823712) as 2026-12-20 21:28:32 and a message timestamp of 2026-12-09 13:28:48 [S].",
 "str(datetime.datetime.fromtimestamp(1797823712)) is 2026-12-20 21:28:32 only in a zone at UTC-6 such as America/Chicago; in UTC it is 2026-12-21 03:28:32, in Europe/Istanbul 2026-12-21 06:28:32, and that moment is a Monday 69 days after 2026-10-13 [T].")
_b('AppendixAnswers',
 "Appendix B answers Question 1 with the credentials.json and token.json files telling EZGmail which Google account to use, Question 3 with the text has:attachment passed to search(), and Question 5 with the Requests library [APPB].",
 "search('has:attachment') asked the API for users/me/threads?q=has:attachment&maxResults=25 and returned GmailThread objects; the Requests answer is true and means no ntfy package is needed; Question 1 describes token.json more than credentials.json, which holds the client of the project [T].")
_b('UmbrellaReminder',
 "The first practice program asks for a program that checks whether rain is in the forecast for the day and texts a reminder, using weather.gov as in chapter 13 [S]. The National Weather Service documents an API whose forecast periods carry a short forecast and a probability of precipitation [NWS].",
 "Searching the text of a forecast for the word rain found it in neither of 2 sample periods, so it missed the period with a precipitation chance of 60 that a comparison with a limit of 40 flagged; api.weather.gov answered the point lookup for Chicago and its forecast with 14 periods that each carry a chance of precipitation as a number [T].")
_b('AutoUnsubscriber',
 "The second practice program scans all mail for links whose text says unsubscribe, with Beautiful Soup, and opens them with webbrowser.open() [S]. RFC 2369 defines the List-Unsubscribe header and RFC 8058 the one-click form [RFC2369][RFC8058].",
 "A parser that looks for the word in the text of links found 1 of 3 candidates in a sample (the image link and the link that says opt out were missed); the word occurred 2 times in the HTML, and the List-Unsubscribe header with List-Unsubscribe-Post gave a mailto: and an https: address without parsing any HTML [T].")
_b('EmailControlLoop',
 "The third practice program checks mail or ntfy every 15 minutes, requires a password in the message, launches a program with subprocess.Popen, waits for it, and deletes the mail it handled [S].",
 "The loop on local stand-ins checked the password with hmac.compare_digest, ran only commands of an allow-list with Popen and wait (noop exit 0, sleep exit 0), answered bad password for a wrong one and refused rm; the book's Popen of qBittorrent raised FileNotFoundError on Linux, and compare_digest of a non-ASCII str raised TypeError [T].")
_b('SecondEditionContent',
 "Chapter 18 of the 2nd edition, Sending Email and Text Messages, taught smtplib, imapclient, pyzmail and Twilio [S2E]. The 3rd edition's chapter 20 says EZGmail is better than smtplib and imaplib for Gmail [S].",
 "Counting names on the pages as served on 2026-10-13, the 2nd edition's chapter mentions smtplib 21 times, imapclient 20, pyzmail 14 and Twilio 31, while chapter 20 of the 3rd edition names smtplib and imaplib only to say EZGmail is better. Recorded in the live observations [T].")
_b('MissingExampleImplementation',
 "Chapter 20 says that a reader who is stuck on the Email-Based Computer Control program can download an example implementation from the book page of No Starch Press [S][P04].",
 "The page holds none (0 occurrences of an example implementation, of Email-Based, of ezgmail or of ntfy), the online materials hold 91 files and none for this chapter, and phoneAndEmail.py in them belongs to chapter 8. Recorded in the live observations [T].")


PUBS.sort(key=lambda p: p[0])
_CITE = {
 "S": "(Sweigart, 2025)", "APPB": "(Sweigart, 2025)", "S2E": "(Sweigart, 2019)", "EZ": "(Sweigart, 2024)",
 "PY": "(Python Software Foundation, 2026)", "PYPI": "(Python Package Index, 2026)", "NTFY": "(Heckel, 2026)", "GOOG": "(Google, 2026)",
 "ATT": "(ATT, 2025)", "VZ": "(Verizon, 2026)", "TWILIO": "(Twilio, 2026)", "NWS": "(National Weather Service, 2026)",
 "RFC5321": "(Klensin, 2008)", "RFC5322": "(Resnick, 2008)", "RFC2045": "(Freed and Borenstein, 1996)", "RFC2047": "(Moore, 1996)",
 "RFC3501": "(Crispin, 2003)", "RFC3207": "(Hoffman, 2002)", "RFC8314": "(Moore and Newman, 2018)", "RFC4954": "(Siemborski and Melnikov, 2007)",
 "RFC2369": "(Neufeld and Baer, 1998)", "RFC8058": "(Leonard, 2017)", "RFC7208": "(Kitterman, 2014)", "RFC7489": "(Kucherawy and Zwicky, 2015)",
 "RFC2177": "(Leiba, 1997)", "P04": "(No Starch Press, 2025)", "T": "(This study, 2026)",
}
for _k in list(BODY):
    _t = BODY[_k]
    for _n, _v in _CITE.items():
        _t = _t.replace("[" + _n + "]", _v)
    BODY[_k] = _t.replace('"', "'")
