# Chapter 20 Draft — Sending Email, Texts and Push Notifications (v1.0.1)

**Status note:** checked against live files on 2026-11-12: deck `sen0414_ch20_deck_v1_0_1.pptx (26 slides, in 08-tooling/ch20-deck)`, page `sen0414_ch20_page_v9_35_0.html`, no chapter-code manifest, stories script v1_0_0 (6 stories, self-check clean, no link shared with chapters 1 to 18; the story-repeat check `sen0414_story_repeat_check_v1_0_0.py` is clean). The deck standard check v1.0.0 fails D1 D2 D3 D4 D5 D7 D11; D10 and M1 not measured. This chapter never received the retrofit that chapters 9 to 18 received, so this draft is the plan of a new deck, page and manifest, built after your approval. Nothing has been built.

## 1. The story (6 beats, one per concept, sourced)

1. **1971, on the ARPANET — Ray Tomlinson, a programmer at Bolt, Beranek and Newman (BBN).** Wikipedia's article on Ray Tomlinson says he invented the first email program on the ARPANET in 1971, the first system able to send mail between users on different hosts. Before that, mail could be sent only to others who used the same computer. He was asked to adapt SNDMSG, which let users leave messages for others on the same time-sharing computer, so that it could run on TENEX, and he built in code from his file-transfer program CPYNET. To separate the user name from the name of the machine he used the @ sign, because it was not used in user names or in TENEX programming. In this study email.utils.parseaddr split 'Al Sweigart <al@inventwithpython.com>' into the name and the address at that sign. *Lesson: Every address your program builds still has Tomlinson's @ in it.* (https://en.wikipedia.org/wiki/Ray_Tomlinson)

2. **1978 — Gary Thuerk, who sent a message advertising a product presentation of the Digital Equipment Corporation (DEC).** Wikipedia's article on email spam says that at the beginning of the Internet, in the ARPANET, sending commercial email was prohibited. Gary Thuerk sent the first known spam email in 1978, advertising a DEC product presentation, to 600 addresses by the article's count (other sources give 293, 393 or about 400, so the slide will say several hundred), and he was reprimanded and told not to do it again. The article adds that the ARPANET had 2600 users at the time and that, because of software limitations, only slightly more than half of the intended recipients received the message. That history is why Gmail, as chapter 20 says, has security and anti-spam measures that might not send repeated emails with the exact same text. *Lesson: Volume is judged by the receiver, so send little and say who you are.* (https://en.wikipedia.org/wiki/Email_spam)

3. **August 1982 — Jonathan B. Postel of the Information Sciences Institute, University of Southern California.** The RFC Editor's page for RFC 821, Simple Mail Transfer Protocol, by Jonathan B. Postel, is dated August 1982 and names the Information Sciences Institute of the University of Southern California in Marina del Rey. The same page now says that the RFC is obsolete and points to RFC 2821, which RFC 5321 of October 2008 by J. Klensin in turn obsoleted. Python's smtplib still opens a conversation with EHLO, the extended greeting that RFC 821's HELO grew into, and sends MAIL FROM and RCPT TO commands. In this study a local aiosmtpd server received exactly those commands, and the message header's From was not the MAIL FROM of the envelope. *Lesson: Mail is an old protocol; trust nothing in it that is not checked.* (https://www.rfc-editor.org/rfc/rfc821)

4. **3 December 1992 — Neil Papworth, a test engineer for Sema Group, and his colleague Richard Jarvis of Vodafone.** Wikipedia's article on SMS says the first SMS message was sent on 3 December 1992 over the Vodafone GSM network in the United Kingdom, when Neil Papworth of Sema Group sent 'Merry Christmas' from a personal computer to Richard Jarvis's Orbitel 901 phone. The service allows messages of up to 160 characters, and the article says the length was limited to 128 bytes, later improved to 160 seven-bit characters, so that messages fit into the existing signalling formats. In this study 140 bytes of 8 bits hold 160 characters of 7 bits, a text of 161 ASCII characters needed 2 messages, and 'Yedekleme tamamlandı' with its dotless i needed the 16-bit coding that holds only 70 characters in one message. *Lesson: Count the characters in the coding the phone uses, not in Python.* (https://en.wikipedia.org/wiki/SMS)

5. **1986 — Mark Crispin, who designed IMAP at Stanford University.** Wikipedia's article on IMAP says Mark Crispin designed it in 1986 as a remote mailbox protocol, in contrast to the widely used POP, which simply retrieves the contents of a mailbox. With IMAP the mail stays on the server until the client deletes it, so several clients can manage the same mailbox, and the original was a Xerox Lisp machine client with a TOPS-20 server (imap.org says it was developed at Stanford). Crispin's IMAP2 followed as RFC 1064 in 1988 and RFC 1176 in 1990. Chapter 20 reads mail with imaplib, which speaks this protocol, and then says that Gmail's API is the better way in; the story explains why the chapter's search and read examples act on mail that stays on the server. *Lesson: IMAP leaves mail on the server, so many programs can share one mailbox.* (https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol)

6. **17 June 2025 — AT&T Wireless, which told its customers they could no longer send or receive texts using email.** AT&T's own support page says that on 17 June 2025 its email-to-text and text-to-email service was shut down, and gives no reason. Commentators say the likely reasons are that the service was outdated and open to spam and abuse, and that it was free and brought support tickets and compliance risk without revenue; these are their judgements, not AT&T's. The alternatives named by third parties are a paid texting service registered with the carriers (10DLC), or leaving texts for push notifications over a plain web request, which is what the ntfy examples of this chapter do. Table 20-1 of chapter 20 still lists AT&T first, with the gateways txt.att.net and mms.att.net, and the chapter itself warns that the fact that a gateway delivers a text today does not mean it will work tomorrow. In this study a DNS query for the mail exchangers of txt.att.net and mms.att.net came back without any, while 12 of the other 16 gateway domains of the table had them (sprint's two answered NXDOMAIN and boost's SERVFAIL). Verizon's page says its shutdown of vtext.com and vzwpix.com is expected to be complete by 31 March 2027. *Lesson: A gateway the carrier owns can be switched off without asking you.* (https://www.att.com/support/article/wireless/KM1061254/)

Pictures: each story slide gets a real picture from Wikimedia Commons or another free source whose licence is read at build; where no free picture of the person or object exists, the slide says so and shows a document picture, never an invented one. Each story is told as who, what, when, where, why and how, with its live link and a lesson of at most 14 words.

## 2. Slide / page-tab outline (19 code examples; the example number is the page-tab order)

| Slide | Title | Code example |
|---|---|---|
| 1 | >>> |  |
| 2 | Today's route |  |
| 3 | Two questions this chapter answers |  |
| 4 | Part 1: The Gmail API |  |
| 5 | Everyday pictures: the Gmail API |  |
| 6 | Story: IMAP, designed in 1986, leaves your mail on the server, so a program can read it |  |
| 7 | Setting up the Gmail API: credentials and the first sign-in | 1 |
| 8 | Sending mail with EZGmail | 2 |
| 9 | Reading and searching mail | 3 |
| 10 | Replying to a message | 4 |
| 11 | Downloading attachments | 5 |
| 12 | Part 2: Mail as a protocol (smtplib) |  |
| 13 | Everyday pictures: SMTP |  |
| 14 | Story: Ray Tomlinson put an @ between the user and the machine |  |
| 15 | Story: RFC 821 is the SMTP that smtplib still speaks, and it is obsolete |  |
| 16 | Building a message with email.message.EmailMessage | 6 |
| 17 | Headers and the envelope: what a mail says and what a mail does | 7 |
| 18 | smtplib and STARTTLS | 8 |
| 19 | SMTP refusals and errors | 9 |
| 20 | Envelope against headers | 10 |
| 21 | Story: The first spam went to 600 addresses on the ARPANET |  |
| 22 | Part 3: Texts by email |  |
| 23 | Everyday pictures: SMS gateways |  |
| 24 | Story: The first text message said Merry Christmas |  |
| 25 | SMS email gateways: sending a text by email | 11 |
| 26 | Segments: how many texts is this message? | 12 |
| 27 | Story: AT&T switched off email-to-text on 17 June 2025 |  |
| 28 | Native table of the carrier gateways (Table 20-1) and what became of them |  |
| 29 | Part 4: Push notifications |  |
| 30 | Everyday pictures: ntfy |  |
| 31 | ntfy: publish a notification | 13 |
| 32 | ntfy: headers, priority and tags | 14 |
| 33 | ntfy: polling and parsing messages | 15 |
| 34 | Topic secrecy and limits | 16 |
| 35 | Part 5: Practice programs |  |
| 36 | Practice: auto unsubscriber | 17 |
| 37 | Practice: umbrella reminder | 18 |
| 38 | Practice: email-based computer control | 19 |
| 39 | Practice questions |  |
| 40 | Summary |  |
| 41 | Resources |  |

Total 41 slides. Each code example sits on its own slide with a short explanation beside the code and the executed result drawn as a visual (a native chart or table where the result is numbers; no picture of a chart); the example list is exactly the page tabs, in this order. Every slide is numbered, text boxes stay at or below 30 words and speaker notes at or below 60 words. Examples are run under the chapter's pinned Python and packages and nothing needing an account is run against a real service: the Gmail steps use the stand-in the research set already has, and the ntfy steps a local recorder.

### Everyday pictures (analogies), one slide at the start of each part

- **Part 1 — the Gmail API:** a post-office box needs a key you were given once (credentials.json), a visitor pass that expires (token.json) and a clerk who only fetches what the pass allows (scopes).
- **Part 2 — SMTP:** the envelope is the address the postman reads, the letter's own header is what the reader sees; a registered-mail counter refuses what is wrongly addressed.
- **Part 3 — SMS gateways:** a carrier's mail-to-text address is a side door into the phone network; the owner of the door can lock it.
- **Part 4 — ntfy:** a noticeboard in a corridor: anyone who knows the board's name can pin a note and anyone who knows it can read it, so the name is the secret.

The analogy slides cover the key concepts of the chapter's research set (34); concepts not named above are carried by an analogy box on the slide that teaches them, and the deck standard check D4 and D11 count them.

## 3. Resources slide (15 links; the Gmail page was replaced by two IMAP pages)

1. https://en.wikipedia.org/wiki/Ray_Tomlinson  (answered 200 on 2026-11-12)
2. https://www.att.com/support/article/wireless/KM1061254/  (answered 200 on 2026-11-12)
3. https://automatetheboringstuff.com/3e/chapter20.html  (answered 200 on 2026-11-12)
4. https://docs.python.org/3.14/library/email.message.html  (answered 200 on 2026-11-12)
5. https://docs.python.org/3.14/library/smtplib.html  (answered 200 on 2026-11-12)
6. https://developers.google.com/workspace/gmail/api/guides/sending  (answered 200 on 2026-11-12)
7. https://docs.ntfy.sh/publish/  (answered 200 on 2026-11-12)
8. https://docs.ntfy.sh/subscribe/api/  (answered 200 on 2026-11-12)
9. https://en.wikipedia.org/wiki/Email_spam  (answered 200 on 2026-11-12)
10. https://en.wikipedia.org/wiki/SMS  (answered 200 on 2026-11-12)
11. https://pypi.org/pypi/ezgmail/json  (answered 200 on 2026-11-12)
12. https://pypi.org/pypi/requests/json  (answered 200 on 2026-11-12)
13. https://www.rfc-editor.org/rfc/rfc821  (answered 200 on 2026-11-12)
14. https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol  (answered 200 on 2026-11-12)
15. https://imap.org/history/  (answered 200 on 2026-11-12)

## 4. Open items

- **What the build changes:** deck from 26 slides to about 41, one example per slide, analogies, story pictures, short notes; a chapter-code manifest of 19 examples; page rebuilt on the current template with the stories and chapter-code tab. The research-artifact folder `rdodi/` is not touched.
- **Resources:** unchanged from the current deck. Your standing wish for a resources slide with community, corpus, seminal works, tutorials and videos is only partly met by these links (no video, no community link). Say if you want videos and a community link added; each would be found and checked live before it goes in.
- **Known limits:** the page test on this machine stops at 70 features when the browser tab crashes (the accepted pages do the same); the build will report what ran and what did not.
