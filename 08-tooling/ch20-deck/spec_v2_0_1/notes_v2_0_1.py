"""Chapter 20 presenter notes, version 2.0.1 (over 2.0.0, which stays unchanged): ruling 2 of 2026-11-14 also asks that a code slide's notes say what to point at and what the result shows,
and that every note leads into the next slide. Each 2.0.0 note is kept word for word; a code slide gets one opening sentence (what to point at in the printed result) and every slide
except the last gets one closing sentence that names what comes next. Every note stays within 60 to 140 words (30 or more on title, part and resources slides)."""
__version__ = "2.0.1"
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spec"))
from notes_v2_0_0 import NOTES as N0, STORY_NOTES as S0

POINT = {
 "setup": "Point at the two printed lines: the message that the credentials file is missing, and the scope followed by False, which says nobody is signed in.",
 "send": "Point at the printed line with the recipient, the sender and the subject, and at the body under it: the result is the mail we typed.",
 "read": "Point at the printed sender and subject, then at the empty list, then at the query printed last, which reached the service as typed.",
 "reply": "Point at the printed thread number T1, which is the one of the original mail, and at the reply text on the last line.",
 "download": "Point at the first printed list: the saved name starts with two dots and a slash, so the file left the folder we chose.",
 "build": "Point at the five content types in the first printed list, and at poster.bin, the name of the attachment that the second result prints.",
 "headers": "Point at the printed subject with its encoded word, and at the refused line printed last: a line break in a header is an error.",
 "starttls": "Point at the three printed lines: the answer 250 to the greeting, the code 220 for go ahead, and SSLSocket, which shows the connection is now wrapped in TLS.",
 "refusals": "Point at the two printed dictionaries: the refused address with its code 550, first returned by sendmail and then carried by the exception.",
 "envelope": "Point at the printed recipient lists, where the header names Jon and the server delivered to Jon and the boss, and at the last line, which says the boss is not in the text.",
 "gateway": "Point at the three printed lines: the gateway address, the carriers that share a domain, and the days since AT&T closed its gateway.",
 "segments": "Point at the printed groups: the coding, the character count and the parts, and at the last line, where UCS-2 appears.",
 "ntfyPub": "Point at the printed request line with the topic in the path, and at the body with its length of 13.",
 "ntfyHdr": "Point at the printed dictionary of three headers as the recorder received them, and at the error line printed last.",
 "ntfyPoll": "Point at the printed list of kinds, an open and two messages, and at the two clock times printed after it.",
 "secrecy": "Point at the printed bits: 107.2 at most for the long name, 47.6 for the guessable one and 144 for the random one, then the bytes on the last line.",
 "unsub": "Point at the two printed lists: the link found in the text, and the two addresses of the List-Unsubscribe header.",
 "umbrella": "Point at the two printed decisions: Tonight has a chance of 60 and takes an umbrella, and Friday has 0 and does not.",
 "control": "Point at the three printed outcomes: wrong password, not allowed, and ran hello.",
}
LEAD = {
 "title": "Next comes the route through the five parts.",
 "route": "Next come the two questions that run through the chapter.",
 "questions": "Part one starts on the next slide, with the Gmail API.",
 "divider1": "The next slide gives an everyday picture for the part.",
 "divider2": "The next slide gives the everyday picture for the protocol.",
 "divider3": "The next slide gives the everyday picture for texts by email.",
 "divider4": "The next slide gives the everyday picture of a noticeboard.",
 "divider5": "The next slide gives the pictures for the three programs.",
 "A1": "Next comes a true story about mail that stays on the server.",
 "A2": "Next come two stories about where the @ and the protocol came from.",
 "A3": "Next comes the story of the first text message.",
 "A4": "Next comes the first code slide of the part, which publishes a notification.",
 "A5": "Next comes the first practice program.",
 "setup": "Next comes the first real call, which sends a message.",
 "send": "Next we read and search the mailbox.",
 "read": "Next we reply to one of those messages.",
 "reply": "Next come attachments, and why their names cannot be trusted.",
 "download": "Part two begins on the next slide, with mail as a protocol.",
 "build": "Next come the headers of this message.",
 "headers": "Next we see how the connection to the server is encrypted.",
 "starttls": "Next we see what happens when the server refuses a recipient.",
 "refusals": "Next we see how the envelope differs from the headers.",
 "envelope": "Next comes a story about the first spam.",
 "gateway": "Next we count how many texts a message really needs.",
 "segments": "Next comes the story of how a gateway was closed.",
 "compare_gateways": "Part four starts on the next slide, with push notifications.",
 "ntfyPub": "Next we add a title, a priority and tags to the same notification.",
 "ntfyHdr": "Next we read what the topic holds.",
 "ntfyPoll": "Next we see why a topic name is a password.",
 "secrecy": "Part five begins on the next slide, with the practice programs.",
 "unsub": "Next comes a program that reads a forecast.",
 "umbrella": "Next comes the most dangerous program, the one that obeys mail.",
 "control": "After it come the practice questions.",
 "practice": "The summary follows on the next slide.",
 "summary": "The last slide lists where to go next.",
}
SLEAD = {
 "imap": "Next comes the first code slide, which sets up the Gmail API.",
 "tomlinson": "Next comes the story of the protocol itself.",
 "rfc821": "Next we build a message with the email package.",
 "spam": "Part three begins on the next slide, with texts by email.",
 "sms": "Next we build a gateway address.",
 "att": "Next we see what became of the book's gateway table.",
}
NOTES = {k: " ".join(x for x in (POINT.get(k, ""), v, LEAD.get(k, "")) if x) for k, v in N0.items()}
STORY_NOTES = {k: v + " " + SLEAD[k] for k, v in S0.items()}
if __name__ == "__main__":
    for k, v in list(NOTES.items()) + list(STORY_NOTES.items()):
        w = len(v.split()); lo = 30 if k in ("title", "route", "questions", "resources") or k.startswith("divider") else 60
        assert lo <= w <= 140, (k, w)
    print("notes ok", min(len(v.split()) for v in NOTES.values()), max(len(v.split()) for v in NOTES.values()))
