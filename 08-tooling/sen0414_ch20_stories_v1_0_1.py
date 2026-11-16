"""SEN0414 chapter 20 - the story companion to the chapter corpus (version 1.0.1).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for
sending email, texts and push notifications, written fresh for this chapter from pages opened on 2026-10-13 (the IMAP story on 2026-11-12) (the HTTP status each
link answered to a plain GET on that day is in LINK_STATUS, and `python3 sen0414_ch20_stories_v1_0_0.py links` asks again):

* Tomlinson1971 - Ray Tomlinson at Bolt, Beranek and Newman adapted SNDMSG for TENEX in 1971 and used the @ sign to separate the user name from the
  name of the machine (Wikipedia, 'Ray Tomlinson').
* Thuerk1978 - Gary Thuerk sent the first known spam e-mail in 1978, advertising a DEC product presentation, to 600 addresses on the ARPANET
  (Wikipedia, 'Email spam').
* Postel1982 - Jonathan B. Postel's RFC 821, 'Simple Mail Transfer Protocol', dated August 1982 at the Information Sciences Institute; the page of the
  RFC Editor says it is obsolete and points to RFC 2821 (rfc-editor.org).
* Papworth1992 - on 3 December 1992 the test engineer Neil Papworth of Sema Group sent 'Merry Christmas' to Richard Jarvis of Vodafone on an Orbitel 901
  handset, the first SMS; the service allows up to 160 characters (Wikipedia, 'SMS').
* Imap1986 - Mark Crispin designed IMAP in 1986 at Stanford University as a protocol for a remote mailbox; IMAP2 followed as RFC 1064 (1988) and RFC 1176 (1990) (Wikipedia, 'Internet Message Access Protocol'). Version 1.0.1 replaces the story of Gmail's launch (Gmail2004) with this one, the story of the chapter 20 deck 2.0.0.
* Att2025 - AT&T's own support page says that on 17 June 2025 its email-to-text and text-to-email service was shut down (att.com).

Photograph: see ch20-page/stories_img_v9_98_0.json for the pictures of the page and the credit of each; 03-materials/ch20/assets/story_images_v1_0_0.json holds each licence.
A claim the research first planned and dropped: the text of the first message Tomlinson sent; the Wikipedia article says its content was not preserved and
that it was likely a random string such as QWERTYUIOP, which is often misquoted.
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.1"

STORIES = [
    {
        "id": "Tomlinson1971",
        "title": "Ray Tomlinson put an @ between the user and the machine",
        "when": "1971, on the ARPANET",
        "who": "Ray Tomlinson, a programmer at Bolt, Beranek and Newman (BBN)",
        "where": "BBN, on the ARPANET, adapting the program SNDMSG for the TENEX operating system",
        "link": "https://en.wikipedia.org/wiki/Ray_Tomlinson",
        "concepts": ["EmailMessageBuild", "AddressParsing"],
        "story": ("Wikipedia's article on Ray Tomlinson says he invented the first email program on the ARPANET in 1971, the first system able to send mail between users on different hosts. "
                  "Before that, mail could be sent only to others who used the same computer. "
                  "He was asked to adapt SNDMSG, which let users leave messages for others on the same time-sharing computer, so that it could run on TENEX, and he built in code from his file-transfer program CPYNET. "
                  "To separate the user name from the name of the machine he used the @ sign, because it was not used in user names or in TENEX programming. "
                  "In this study email.utils.parseaddr split 'Al Sweigart <al@inventwithpython.com>' into the name and the address at that sign."),
        "lesson": "Every address your program builds still has Tomlinson's @ in it",
        "source": ("Wikipedia, 'Ray Tomlinson' (the first email program on the ARPANET in 1971; SNDMSG adapted for TENEX; the @ sign chosen because it was not used in user names), read 2026-10-13; "
                   "this study's leaves EmailMessageBuild and AddressParsing."),
    },
    {
        "id": "Thuerk1978",
        "title": "The first spam went to 600 addresses on the ARPANET",
        "when": "1978",
        "who": "Gary Thuerk, who sent a message advertising a product presentation of the Digital Equipment Corporation (DEC)",
        "where": "The ARPANET, where sending commercial email was prohibited",
        "link": "https://en.wikipedia.org/wiki/Email_spam",
        "concepts": ["AutoUnsubscriber", "DmarcRecordParse"],
        "story": ("Wikipedia's article on email spam says that at the beginning of the Internet, in the ARPANET, sending commercial email was prohibited. "
                  "Gary Thuerk sent the first known spam email in 1978, advertising a DEC product presentation, to 600 addresses, and he was reprimanded and told not to do it again. "
                  "The article adds that the ARPANET had 2600 users at the time and that, because of software limitations, only slightly more than half of the intended recipients received the message. "
                  "That history is why Gmail, as chapter 20 says, has security and anti-spam measures that might not send repeated emails with the exact same text."),
        "lesson": "Volume is judged by the receiver, so send little and say who you are",
        "source": ("Wikipedia, 'Email spam' (Gary Thuerk, 1978, 600 addresses, a DEC product presentation, 2600 users on the ARPANET); chapter 20 of the 3rd edition (Gmail might not send repeated emails with the exact same text), read 2026-10-13; "
                   "this study's leaves AutoUnsubscriber and DmarcRecordParse."),
    },
    {
        "id": "Postel1982",
        "title": "RFC 821 is the SMTP that smtplib still speaks, and it is obsolete",
        "when": "August 1982",
        "who": "Jonathan B. Postel of the Information Sciences Institute, University of Southern California",
        "where": "Marina del Rey, California, in the RFC series; the RFC Editor's page today",
        "link": "https://www.rfc-editor.org/rfc/rfc821",
        "concepts": ["StarttlsSession", "EnvelopeVersusHeader"],
        "story": ("The RFC Editor's page for RFC 821, Simple Mail Transfer Protocol, by Jonathan B. Postel, is dated August 1982 and names the Information Sciences Institute of the University of Southern California in Marina del Rey. "
                  "The same page now says that the RFC is obsolete and points to RFC 2821, which RFC 5321 of October 2008 by J. Klensin in turn obsoleted. "
                  "Python's smtplib still opens a conversation with EHLO, the extended greeting that RFC 821's HELO grew into, and sends MAIL FROM and RCPT TO commands. "
                  "In this study a local aiosmtpd server received exactly those commands, and the message header's From was not the MAIL FROM of the envelope."),
        "lesson": "Mail is an old protocol; trust nothing in it that is not checked",
        "source": ("RFC Editor, RFC 821 (Postel, August 1982; this RFC is now obsolete, see RFC 2821) and RFC 5321 (Klensin, October 2008, obsoletes 2821), read 2026-10-13; "
                   "this study's leaves StarttlsSession and EnvelopeVersusHeader."),
    },
    {
        "id": "Papworth1992",
        "title": "The first text message said Merry Christmas",
        "when": "3 December 1992",
        "who": "Neil Papworth, a test engineer for Sema Group, and his colleague Richard Jarvis of Vodafone",
        "where": "The Vodafone GSM network in the United Kingdom, from a personal computer to an Orbitel 901 handset",
        "link": "https://en.wikipedia.org/wiki/SMS",
        "concepts": ["Gsm7Length", "Ucs2Length"],
        "story": ("Wikipedia's article on SMS says the first SMS message was sent on 3 December 1992 over the Vodafone GSM network in the United Kingdom, when Neil Papworth of Sema Group sent 'Merry Christmas' from a personal computer to Richard Jarvis's Orbitel 901 phone. "
                  "The service allows messages of up to 160 characters, and the article says the length was limited to 128 bytes, later improved to 160 seven-bit characters, so that messages fit into the existing signalling formats. "
                  "In this study 140 bytes of 8 bits hold 160 characters of 7 bits, a text of 161 ASCII characters needed 2 messages, and 'Yedekleme tamamlandı' with its dotless i needed the 16-bit coding that holds only 70 characters in one message."),
        "lesson": "Count the characters in the coding the phone uses, not in Python",
        "source": ("Wikipedia, 'SMS' (the first SMS on 3 December 1992, Neil Papworth, Richard Jarvis, Orbitel 901; 160 seven-bit characters), read 2026-10-13; "
                   "this study's leaves Gsm7Length and Ucs2Length."),
    },
    {
        "id": "Imap1986",
        "title": "IMAP, designed in 1986, leaves your mail on the server",
        "when": "1986, with IMAP2 in 1988 and 1990",
        "who": "Mark Crispin, who designed the protocol at Stanford University",
        "where": "Stanford University; the protocol is the one Python's imaplib speaks",
        "link": "https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol",
        "concepts": ["ImapParsing", "ImapIdle"],
        "story": ("Wikipedia's article on the Internet Message Access Protocol says Mark Crispin designed IMAP in 1986 at Stanford University as a protocol for a remote mailbox, while the widely used POP simply fetched the contents of a mailbox. "
                  "With IMAP the mail stays on the server until a client deletes it, so several programs can share one mailbox. "
                  "The article names RFC 1064 of 1988 as the specification of IMAP2 and RFC 1176 of 1990 as its update. "
                  "Chapter 20 of the 3rd edition reads mail with imaplib and then says that the Gmail API is the better way in. "
                  "In this study the imaplib of Python 3.14.6 had an idle() method and the IDLE command that Python 3.13 does not have."),
        "lesson": "A mailbox on a server can be shared by every program that logs in",
        "source": ("Wikipedia, 'Internet Message Access Protocol' (Mark Crispin, 1986, Stanford University; RFC 1064 of 1988 and RFC 1176 of 1990), read 2026-11-12; chapter 20 of the 3rd edition; "
                   "this study's leaves ImapParsing and ImapIdle."),
    },
    {
        "id": "Att2025",
        "title": "AT&T switched off email-to-text on 17 June 2025",
        "when": "17 June 2025",
        "who": "AT&T Wireless, which told its customers they could no longer send or receive texts using email",
        "where": "AT&T's support page, article KM1061254; the gateways txt.att.net and mms.att.net of Table 20-1",
        "link": "https://www.att.com/support/article/wireless/KM1061254/",
        "concepts": ["AttNotice", "GatewayAddress"],
        "story": ("AT&T's own support page says that effective 17 June 2025 you can no longer send or receive texts using email, and that on that day its email-to-text and text-to-email service was shut down. "
                  "Table 20-1 of chapter 20 still lists AT&T first, with the gateways txt.att.net and mms.att.net, and the chapter itself warns that the fact that a gateway delivers a text today does not mean it will work tomorrow. "
                  "In this study a DNS query for the mail exchangers of txt.att.net and mms.att.net came back without any, while 12 of the other 16 gateway domains of the table had them (sprint's two answered NXDOMAIN and boost's SERVFAIL). "
                  "Verizon's page says its shutdown of vtext.com and vzwpix.com is expected to be complete by 31 March 2027."),
        "lesson": "A gateway the carrier owns can be switched off without asking you",
        "source": ("AT&T support article KM1061254 (shut down on June 17, 2025); Verizon, 'Shutdown of email to Vtext and VZWPix' (03/31/2027); chapter 20 of the 3rd edition (Table 20-1 and the list of disadvantages), read 2026-10-13; "
                   "this study's live observation of MX records and its leaves AttNotice and GatewayAddress."),
    },
]

# the order of the chapter 20 deck 2.0.0
_by = {x["id"]: x for x in STORIES}
STORIES = [_by[i] for i in ("Imap1986", "Tomlinson1971", "Postel1982", "Thuerk1978", "Papworth1992", "Att2025")]

LINK_STATUS = {'Tomlinson1971': 200, 'Thuerk1978': 200, 'Postel1982': 200, 'Papworth1992': 200, 'Imap1986': 200, 'Att2025': 200}


def run_checks():
    bad = []
    ids = [x["id"] for x in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for x in STORIES:
        for f in ("who", "where", "link", "when", "title", "lesson", "source", "story"):
            if not str(x.get(f, "")).strip():
                bad.append("%s: missing %s (5N1K)" % (x["id"], f))
        if not x.get("link", "").startswith("http"):
            bad.append("%s: link is not a URL" % x["id"])
        if len(x["lesson"].split()) > 14:
            bad.append("%s: lesson over 14 words" % x["id"])
        if not (2 <= x["story"].count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % x["id"])
        if LINK_STATUS and LINK_STATUS.get(x["id"]) != 200:
            bad.append("%s: link status %r, not 200" % (x["id"], LINK_STATUS.get(x["id"])))
        if not LINK_STATUS:
            bad.append("LINK_STATUS is empty")
    by = {x["id"]: x for x in STORIES}
    for sid, year in (("Tomlinson1971", "1971"), ("Thuerk1978", "1978"), ("Postel1982", "1982"), ("Papworth1992", "1992"), ("Imap1986", "1986"), ("Att2025", "2025")):
        if year not in by[sid]["story"] and year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
        if year not in by[sid]["when"]:
            bad.append("%s: year %s not in when" % (sid, year))
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "SEN0414-research/1.0 (teaching)"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out[x["id"]] = r.status
        except urllib.error.HTTPError as e:
            out[x["id"]] = e.code
        except Exception as e:
            out[x["id"]] = type(e).__name__
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "links":
        print(ask_links())
    else:
        b = run_checks()
        print(len(STORIES), "stories; self-check failures:", len(b))
        for x in b:
            print("  ", x)
