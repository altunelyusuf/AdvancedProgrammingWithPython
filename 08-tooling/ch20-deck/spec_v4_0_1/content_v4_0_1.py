"""Chapter 20 deck content, version 4.0.1 (SEN0414, Lineage13): the words of the deck; over 4.0.0 only the picture of the AT&T story changes (a sourced photograph replaces the drawing). Derived from content 2.0.0 with one change, made to meet the ruling of 2026-11-24: the five concept slides state what each concept is and does in plain words, with no everyday comparison. Parts, plan, stories, take-aways, tables, practice and resources are unchanged. The notes are in notes_v4_0_0.py."""
__version__ = "4.0.1"

PARTS = {
    1: ("Part 1: The Gmail API", "Two files, one sign-in, then send, read, reply and download", [
        ("setup", "credentials.json and token.json come first"),
        ("send / read", "One call sends; search returns threads"),
        ("reply", "Answers go to the sender, in the same thread"),
        ("download", "A received file name is never safe")]),
    2: ("Part 2: Mail as a protocol (smtplib)", "What really travels between your program and a mail server", [
        ("message", "Headers, a body, parts and attachments"),
        ("STARTTLS", "Starts in plain text, then encrypts"),
        ("refusals", "A server can refuse some or all recipients"),
        ("envelope", "Who gets it is not who the header names")]),
    3: ("Part 3: Texts by email", "A carrier's mail domain turns a message into a text", [
        ("gateway", "Number at the carrier's domain"),
        ("segments", "160 characters, or 70 outside the alphabet"),
        ("switched off", "The carrier can close the door"),
        ("Table 20-1", "The book's list, and what became of it")]),
    4: ("Part 4: Push notifications (ntfy)", "One web request to a topic, and every subscriber sees it", [
        ("publish", "The topic is the path, the message the body"),
        ("headers", "Title, priority and tags; Latin-1 only"),
        ("poll", "One JSON object per line"),
        ("secrecy", "The topic name is the password")]),
    5: ("Part 5: Practice programs", "Three small programs that combine the parts", [
        ("unsubscriber", "Find the safe link in a mail"),
        ("umbrella", "Decide by the chance of rain"),
        ("mail control", "A password and a list of allowed commands"),
        ("questions", "Predict, run, check")]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("story", "imap"), ("code", "setup"), ("code", "send"), ("code", "read"), ("code", "reply"), ("code", "download"),
        ("divider", 2), ("analogy", "A2"), ("story", "tomlinson"), ("story", "rfc821"), ("code", "build"), ("code", "headers"), ("code", "starttls"), ("code", "refusals"), ("code", "envelope"), ("story", "spam"),
        ("divider", 3), ("analogy", "A3"), ("story", "sms"), ("code", "gateway"), ("code", "segments"), ("story", "att"), ("compare", "gateways"),
        ("divider", 4), ("analogy", "A4"), ("code", "ntfyPub"), ("code", "ntfyHdr"), ("code", "ntfyPoll"), ("code", "secrecy"),
        ("divider", 5), ("analogy", "A5"), ("code", "unsub"), ("code", "umbrella"), ("code", "control"), ("practice",),
        ("summary",), ("resources",)]

ROUTE_RUNS = {1: "sign-in, send, read, reply, download", 2: "build, headers, STARTTLS, refusals, envelope", 3: "gateways, segments, what became of them",
              4: "publish, headers, poll, secrecy", 5: "unsubscriber, umbrella, mail control"}
ROUTE_TAIL = ("Summary and links", "what to remember, where next")

QUESTIONS = [
    ("1", "How does a program send a message to a person without lying about who it is from, or sending it to the wrong people?", "The five points come back on slide %d.", "summary"),
    ("2", "How does it do so without putting a secret in the wrong place: a password, a topic name, or a command a stranger can choose?", "Check yourself with the questions on slide %d.", "practice"),
]
QUESTIONS_TAKEAWAY = "Every example runs on the chapter page; read its printed result first."

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "What it is and does"
CONCEPTS_TAIL = "each explained in plain words"
# ---- the concept slides, grouped: (slide id, title, headline, [(research label, what it is and does)])
ANALOGIES = [
    ("A1", "The Gmail API and the ezgmail module", "A program needs two files before it can use Gmail: credentials.json, given once, and token.json, saved after the first sign-in.", [
        ("The Gmail API", "Google's web interface for sending, reading and searching one account's mail."),
        ("Enabling the API", "A one-time step that switches the API on and gives credentials.json."),
        ("ezgmail", "A module that wraps the API in short calls: init(), send(), search()."),
        ("credentials.json", "Issued once by Google; it names your program and stays private."),
        ("token.json", "Written after the first sign-in, so later runs need none."),
        ("Sending Mail", "send(recipient, subject, body) sends one message."),
        ("Reading Mail", "Search returns threads; a message has sender, subject and body."),
        ("Searching for Mail", "The search text reaches Gmail unchanged, so every operator works."),
        ("Figure 20-1: searching for RoboCop email at the Gmail website", "The same search typed at the website; the program gets the same threads."),
        ("Downloading Attachments", "The sender chooses each file's name, so check it before using it as a path."),
    ]),
    ("A2", "Mail as a protocol: smtplib and its neighbours", "A mail has headers that the reader sees and an envelope that the server delivers by; smtplib sends both.", [
        ("smtplib", "The standard-library module that talks to a mail server: it greets, names the sender and the recipients, and hands over the message."),
        ("imaplib", "The standard-library module that reads a mailbox directly from the server and leaves the mail there."),
        ("logging", "The standard-library module that records what a program did; here it can keep the conversation with the server."),
        ("datetime", "The standard-library module that writes the Date header and reads dates back."),
    ]),
    ("A3", "Texts by email gateway", "A carrier's gateway turns a mail sent to the phone number at its domain into a text; the carrier can switch it off.", [
        ("SMS Email Gateways", "An address made of a phone number and the carrier's mail domain; mail sent to it arrives as a text message."),
        ("Table 20-1: SMS email gateways for cell phone providers", "The book's list of the gateway domains of the carriers, as they stood when it was written."),
    ]),
    ("A4", "Push notifications with ntfy", "A notification is one web request to a topic; every phone subscribed to the topic shows it.", [
        ("Push Notifications", "A short message pushed to a phone by a service, with no mail account involved."),
        ("Sending Notifications", "One POST request to the address of the topic; the body of the request is the message."),
        ("Transmitting Metadata", "The title, the priority and the tags travel as request headers, and the headers must be Latin-1."),
        ("Receiving Notifications", "A GET request to the topic returns what it holds, one JSON object for each line."),
        ("ntfy app", "The phone application that subscribes to a topic and shows each message as it arrives."),
        ("requests", "The third-party module that sends the web requests: post() to publish, get() to read."),
        ("json", "The standard-library module that turns one line of the answer into a dictionary."),
    ]),
    ("A5", "The practice programs and their parts", "Three small programs combine the parts: they find a link, decide by a number, and obey a mail safely.", [
        ("Practice Programs", "Three programs: an unsubscriber, an umbrella reminder, a mail-controlled program."),
        ("Umbrella Reminder", "Reads a forecast and decides by the chance of rain."),
        ("Auto Unsubscriber", "Finds the unsubscribe link of a mail, for senders you know."),
        ("Email-Based Computer Control", "Checks a password and a list, and runs only an allowed command."),
        ("Beautiful Soup", "Reads an HTML page and finds its links; the standard library does it here."),
        ("webbrowser", "Its open() shows a web address in the default browser."),
        ("subprocess", "Starts another program, here the torrent client."),
        ("qBittorrent", "A free torrent client that a program starts to begin a download."),
        ("shakespeare_complete_works.torrent", "The torrent file that starts the download of the complete works."),
    ]),
]

# ---- the stories (5N1K, told as natural prose); the picture of each is a record of story_images_v1_0_0.json in the chapter's assets folder
STORIES = {
    "imap": dict(
        title="Story: IMAP, designed in 1986, leaves your mail on the server", img="image_imap.jpg",
        prose=["In 1986 Mark Crispin, at Stanford University, designed IMAP as a protocol for a remote mailbox. The widely used POP simply fetched the contents of a mailbox.",
               "With IMAP the mail stays on the server until a client deletes it, so several programs can share one mailbox.",
               "His IMAP2 followed as RFC 1064 in 1988 and RFC 1176 in 1990. The book reads mail with imaplib, then says Gmail's API is the better way in."],
        linktext="Internet Message Access Protocol (Wikipedia)", link="https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol"),
    "tomlinson": dict(
        title="Story: Ray Tomlinson put an @ between the user and the machine", img="image_arpanet.jpg",
        prose=["In 1971 Ray Tomlinson, a programmer at Bolt, Beranek and Newman, built the first email program that could send mail between users on different hosts of the ARPANET.",
               "He adapted SNDMSG, which left messages for users of the same time-sharing computer, to run on TENEX, with code from his file-transfer program CPYNET.",
               "He chose the @ to separate the user from the machine because TENEX did not use it. Every address your program builds still has it."],
        linktext="Ray Tomlinson (Wikipedia)", link="https://en.wikipedia.org/wiki/Ray_Tomlinson"),
    "rfc821": dict(
        title="Story: RFC 821 is the SMTP that smtplib still speaks, and it is obsolete", img="image_smtp.jpg",
        prose=["In August 1982 Jonathan B. Postel, of the Information Sciences Institute of the University of Southern California in Marina del Rey, published RFC 821, the Simple Mail Transfer Protocol.",
               "Its page now says it is obsolete: RFC 2821 replaced it, and RFC 5321 of October 2008, by J. Klensin, replaced that one.",
               "Yet smtplib still opens with EHLO, the grown-up HELO, then sends MAIL FROM and RCPT TO, as the earlier slides showed."],
        linktext="RFC 821 at the RFC Editor", link="https://www.rfc-editor.org/rfc/rfc821"),
    "spam": dict(
        title="Story: The first spam went to several hundred addresses on the ARPANET", img="image_dec.jpg",
        prose=["On the early ARPANET, sending commercial email was prohibited. In 1978 Gary Thuerk sent the first known spam, which advertised a product presentation of the Digital Equipment Corporation.",
               "Sources count between 293 and 600 recipients, so we say several hundred. He was reprimanded and told not to do it again.",
               "The ARPANET had 2600 users, and because of software limits only slightly more than half of the intended recipients received it."],
        linktext="Email spam (Wikipedia)", link="https://en.wikipedia.org/wiki/Email_spam"),
    "sms": dict(
        title="Story: The first text message said Merry Christmas", img="image_sms.jpg",
        prose=["On 3 December 1992 Neil Papworth, a test engineer of Sema Group, sent 'Merry Christmas' from a personal computer over the Vodafone GSM network in the United Kingdom.",
               "It reached Richard Jarvis's Orbitel 901 phone. The length was limited so that a message fit the existing signalling formats: 160 characters of seven bits.",
               "In this study 140 bytes held 160 such characters, and a text with a dotless i needed the 16-bit coding, which holds only 70."],
        linktext="SMS (Wikipedia)", link="https://en.wikipedia.org/wiki/SMS"),
    "att": dict(
        title="Story: AT&T switched off email-to-text on 17 June 2025", img="image_att_commons.jpg",
        prose=["AT&T told its customers that on 17 June 2025 its email-to-text and text-to-email service was shut down. Its support page gives no reason.",
               "Commentators say it was outdated, open to spam and abuse, and free; those are their judgements, not AT&T's.",
               "A DNS query in this study found no mail servers for txt.att.net or mms.att.net, though 12 of the other 16 gateway domains of the table had them."],
        linktext="AT&T support: email-to-text ended", link="https://www.att.com/support/article/wireless/KM1061254/"),
}

# ---- the native comparison table (Table 20-1 and what became of it)
COMPARES = {
    "gateways": dict(
        title="Table 20-1 and what became of its gateway domains", sub="DNS answers for the 18 gateway domains of the book's table, and the carriers' own notices",
        colw=[3.1, 2.4, 3.5], rowh=0.55, fs=10.5,
        rows=[["Gateway domain", "Answer for its mail servers", "What the carrier says"],
              ["txt.att.net, mms.att.net", "none", "ended 17 June 2025 (AT&T support page)"],
              ["sms.cricketwireless.net", "none", "-"],
              ["messaging.sprintpcs.com, pm.sprint.com", "NXDOMAIN: no such name", "-"],
              ["sms.myboostmobile.com", "SERVFAIL: the lookup failed", "-"],
              ["vtext.com, vzwpix.com (and 10 more)", "mail servers found", "Verizon: shutdown expected complete by 31 March 2027"]],
        takeaway="A missing mail server is a symptom, not proof; the carrier's notice is the evidence."),
}

# ---- one take-away line for every code slide
TAKEAWAY = {
    "setup": "No credentials.json, no sign-in; token.json is made for you.",
    "send": "One call sends; the message is a base64 text underneath.",
    "read": "search() gives threads; each message has sender, subject, body.",
    "reply": "reply() goes to the sender, in the same thread.",
    "download": "A file name you receive is data: never trust it as a path.",
    "build": "EmailMessage writes the headers and the parts for you.",
    "headers": "A line break in a header value is refused: that is injection.",
    "starttls": "Plain text first, then 220, then everything encrypted.",
    "refusals": "Check the dictionary: some recipients can fail alone.",
    "envelope": "The server delivers by the envelope, not by the headers.",
    "gateway": "A gateway is a number at a carrier's domain; it can be closed.",
    "segments": "160 characters in 7 bits, 70 outside the alphabet.",
    "ntfyPub": "One POST to a topic is a notification.",
    "ntfyHdr": "Title, tags and priority are headers; headers are Latin-1.",
    "ntfyPoll": "One JSON object per line: parse each, keep the messages.",
    "secrecy": "The topic name is the password: make it random.",
    "unsub": "Take the address from a link or from List-Unsubscribe.",
    "umbrella": "Decide by the chance, and treat None as zero.",
    "control": "A password and a list of allowed commands, never a shell.",
}

SUMMARY_ANALOGY = "Five points: two files, headers and envelope, the phone's coding, a topic as password, an allowed list."
SUMMARY_POINTS = [
    "The Gmail API needs two files; a received file name is only data.",
    "A mail is headers and a body; the envelope decides who gets it.",
    "A text is counted in the phone's coding; its gateway can be closed.",
    "A notification topic is a password: give it real randomness.",
    "A program that obeys mail needs a password and an allowed list.",
]
SUMMARY_TAKEAWAY = "Two questions of slide 3: send to the right people, and keep secrets in the right place."

PRACTICE_SUB = "Use the slide of the part named in each question"
PRACTICE_ANALOGY = "Each practice question has a short answer; run the code on the chapter page to check it."
PRACTICE = [
    "Which two files does ezgmail need, and what does init() do when one is missing? Use the setup slide.",
    "What is the difference between the envelope and the headers of a mail, and how does a blind copy use it?",
    "How many texts does a 161-character message need, and what changes when it holds a dotless i?",
    "Why is an ntfy topic name a password, and how would you make a strong one?",
    "What two checks keep a program that obeys mail safe? Use the last slide of part 5.",
]
PRACTICE_TAKEAWAY = "Run the examples on the chapter page to check each answer."

RESOURCES_SUB = "The chapter, the documentation, and the pages behind the stories"
RESOURCES_TAKEAWAY = "Every link was opened on 2026-11-12 and answered."
RESOURCES_ROWS = 8
RESOURCES = [
    ("Ray Tomlinson (Wikipedia)", "https://en.wikipedia.org/wiki/Ray_Tomlinson", "en.wikipedia.org"),
    ("AT&T support: email-to-text ended", "https://www.att.com/support/article/wireless/KM1061254/", "www.att.com"),
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 20", "https://automatetheboringstuff.com/3e/chapter20.html", "automatetheboringstuff.com"),
    ("Python documentation: email.message", "https://docs.python.org/3.14/library/email.message.html", "docs.python.org"),
    ("Python documentation: smtplib", "https://docs.python.org/3.14/library/smtplib.html", "docs.python.org"),
    ("Gmail API guide: sending email", "https://developers.google.com/workspace/gmail/api/guides/sending", "developers.google.com"),
    ("ntfy documentation: publishing", "https://docs.ntfy.sh/publish/", "docs.ntfy.sh"),
    ("ntfy documentation: subscribe API", "https://docs.ntfy.sh/subscribe/api/", "docs.ntfy.sh"),
    ("Email spam (Wikipedia)", "https://en.wikipedia.org/wiki/Email_spam", "en.wikipedia.org"),
    ("SMS (Wikipedia)", "https://en.wikipedia.org/wiki/SMS", "en.wikipedia.org"),
    ("ezgmail on PyPI", "https://pypi.org/pypi/ezgmail/json", "pypi.org"),
    ("requests on PyPI", "https://pypi.org/pypi/requests/json", "pypi.org"),
    ("RFC 821: Simple Mail Transfer Protocol", "https://www.rfc-editor.org/rfc/rfc821", "www.rfc-editor.org"),
    ("Internet Message Access Protocol (Wikipedia)", "https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol", "en.wikipedia.org"),
    ("IMAP history (imap.org)", "https://imap.org/history/", "imap.org"),
]


