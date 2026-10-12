"""SEN0414 chapter 15 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for
Google Sheets, written fresh for this chapter from sources opened on 2026-10-12 (the HTTP status each link answered to a
plain GET on that day is in LINK_STATUS, and `python3 sen0414_ch15_stories_v1_0_0.py links` asks again):

* GoogleSheetsXL2Web2006 - Google Sheets began as XL2Web, by Jonathan Rochelle and Farzad Khosrowshahi of 2Web Technologies,
  bought by Google in 2006 and opened as a limited test on 6 June 2006 (Wikipedia, whose article cites Google's blog post).
* NakamotoPaper2008 - Satoshi Nakamoto's message to the cryptography mailing list of 31 October 2008 that announced the paper on
  a peer-to-peer electronic cash system, the idea that the chapter's Boringcoin ledger imitates as a joke.
* OAuthBegins2006 - OAuth started around November 2006 with Blaine Cook, Chris Messina, David Recordon and Larry Halff, a
  Google group was made in April 2007, and RFC 6749 followed in October 2012 (oauth.net).
* SheetsApiV3Turndown2021 - Google turned down the Sheets API v3 on 2 August 2021 and sent developers to v4, the version that
  EZSheets and every current client use (Google's migration guide).
* GoogleForms2008 - Google Forms was first introduced in 2008 as part of the Google Docs suite and stores its answers in a
  spreadsheet, which the chapter's first practice program reads (Wikipedia and Google's help page).
* EzsheetsRelease2019 - EZSheets, by Al Sweigart, first uploaded to PyPI on 8 February 2019 and described in the third edition
  of the book, published in April 2025 (672 pages); its newest release is dated 28 April 2026 (PyPI and No Starch Press).

No photograph is used. Wikimedia Commons answered 'too many requests' to the API on the first request of the session for each of
three searches (Chris Messina, Satoshi Nakamoto, Jonathan Rochelle) and again to later ones, so no file was fetched and no licence
record of a fetched file exists; ch15-page/stories_img_v1_0_0.json says so, and 03-materials/ch15/assets is not made. A claim the
research first planned and dropped: that Google Forms was released on a given day in 2008; the pages that could be opened give the
year only. Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "GoogleSheetsXL2Web2006",
        "title": "Google Sheets began as a small company's web spreadsheet that Google bought in 2006",
        "when": "6 June 2006",
        "who": "Jonathan Rochelle and Farzad Khosrowshahi of 2Web Technologies, then Google",
        "where": "Google Labs, on the web",
        "link": "https://en.wikipedia.org/wiki/Google_Sheets",
        "concepts": ["NewSpreadsheet", "DownloadFormats"],
        "story": ("Google Sheets originated from XL2Web, a web-based spreadsheet application made by 2Web Technologies, a company "
                   "founded by Jonathan Rochelle and Farzad Khosrowshahi. Google acquired XL2Web in 2006 and turned it into Google Labs "
                   "Spreadsheets. It was opened as a test for a limited number of users, first come, first served, on June 6, 2006. "
                   "A beta for all Google Account holders replaced the limited test later. Every spreadsheet the chapter's programs create "
                   "or read is a descendant of that 2006 test."),
        "lesson": "A browser spreadsheet is a service you call, not a file",
        "source": ("Wikipedia, 'Google Sheets', History section (XL2Web, 2Web Technologies, acquisition in 2006, launch on June 6, 2006), "
                    "which cites Jonathan Rochelle, 'It's nice to share', Official Google Blog, June 6, 2006."),
    },
    {
        "id": "NakamotoPaper2008",
        "title": "A message to a cryptography mailing list announced the electronic cash that Boringcoin makes fun of",
        "when": "31 October 2008",
        "who": "Satoshi Nakamoto, writing to the readers of a cryptography mailing list",
        "where": "The cryptography mailing list hosted at metzdowd.com",
        "link": "https://www.metzdowd.com/pipermail/cryptography/2008-October/014810.html",
        "concepts": ["AuditProgram", "TransactionProgram"],
        "story": ("On Friday, October 31, 2008, at 14:10 Eastern time, a message from Satoshi Nakamoto reached the cryptography mailing "
                   "list. It said he had been working on a new electronic cash system that was fully peer-to-peer, with no trusted third "
                   "party, and gave the address of the paper, bitcoin.pdf. The message listed the main properties: double-spending is "
                   "prevented with a peer-to-peer network, there is no mint, and new coins are made from Hashcash style proof-of-work. "
                   "The chapter's Boringcoin is a spreadsheet pretending to be such a ledger, and its audit adds up the balances that "
                   "the message says a network must keep honest."),
        "lesson": "A ledger of rows is easy to audit and just as easy to forge",
        "source": ("Satoshi Nakamoto, 'Bitcoin P2P e-cash paper', cryptography mailing list, Fri Oct 31 14:10:00 EDT 2008, "
                    "metzdowd.com/pipermail/cryptography/2008-October/014810.html; the paper itself, bitcoin.org/bitcoin.pdf."),
    },
    {
        "id": "OAuthBegins2006",
        "title": "OAuth began as a way to let Twitter and OpenID share access without sharing passwords",
        "when": "November 2006",
        "who": "Blaine Cook, Chris Messina, David Recordon and Larry Halff",
        "where": "A CitizenSpace OpenID meeting, then an online Google group",
        "link": "https://oauth.net/about/introduction/",
        "concepts": ["LocalServerFlow", "TokenLifetime"],
        "story": ("OAuth started around November 2006, while Blaine Cook was working on the Twitter OpenID implementation. He got in "
                   "touch with Chris Messina, and they met David Recordon, Larry Halff and others at a CitizenSpace OpenID meeting, where "
                   "they concluded that there was no open standard for API access delegation. In April 2007 a Google group was created "
                   "with a small group of implementers to write a proposal, and in July 2007 the team drafted an initial specification. "
                   "The IETF published it as RFC 6749 in October 2012, and its authorization code and refresh token are what the "
                   "chapter's token files hold."),
        "lesson": "The token files exist so that a script never learns your password",
        "source": ("oauth.net, 'Introduction' (A Little Bit of History), adapted from Eran Hammer-Lahav, 'Explaining OAuth', "
                    "September 5, 2007; RFC 6749, The OAuth 2.0 Authorization Framework, October 2012."),
    },
    {
        "id": "SheetsApiV3Turndown2021",
        "title": "Google turned off the old Sheets API in 2021 and every script had to speak the new one",
        "when": "2 August 2021",
        "who": "The Google Sheets API team and the developers who had apps on version 3",
        "where": "Google for Developers, the Sheets API migration guide",
        "link": "https://developers.google.com/workspace/sheets/api/guides/migration",
        "concepts": ["ApiEnablement", "RawRestCalls"],
        "story": ("Google's migration guide opens with a notice that the Google Sheets API v3 was turned down on August 2, 2021, and "
                   "tells developers to migrate to Sheets API v4. It describes v4 as JSON-based, with an easier-to-use interface and a "
                   "substantial amount of functionality that v3 lacked. EZSheets sends its requests to v4 at sheets.googleapis.com, "
                   "so its address, not its code, is the trace of that change. A program written against a service has to follow the "
                   "service when its address and version change."),
        "lesson": "A library is only as stable as the web service behind it",
        "source": ("Google for Developers, 'Migrate from Sheets API v3', developers.google.com/workspace/sheets/api/guides/migration "
                    "(read 2026-10-12)."),
    },
    {
        "id": "GoogleForms2008",
        "title": "Google Forms arrived in 2008 and has saved its answers into a spreadsheet since",
        "when": "2008",
        "who": "Google, as part of the Google Docs suite",
        "where": "The web, in Google Docs",
        "link": "https://en.wikipedia.org/wiki/Google_Forms",
        "concepts": ["FormsResponses"],
        "story": ("Google Forms is a web application for making and editing surveys online with other people at the same time. "
                   "It was first introduced in 2008 as part of the Google Docs suite. The information it collects can be entered "
                   "automatically into a spreadsheet, and Google's help page says the owner picks a new or an existing spreadsheet as the "
                   "destination of the responses. That spreadsheet is what the first practice program of chapter 15 opens with EZSheets "
                   "to collect the email addresses."),
        "lesson": "A form is a front door that writes rows for your script to read",
        "source": ("Wikipedia, 'Google Forms' (first introduced in 2008 as part of the Google Docs suite); Google Docs Editors Help, "
                    "'Choose where to save form responses', support.google.com/docs/answer/2917686."),
    },
    {
        "id": "EzsheetsRelease2019",
        "title": "EZSheets reached PyPI in February 2019 and the book put it in its third edition in 2025",
        "when": "8 February 2019",
        "who": "Al Sweigart",
        "where": "The Python Package Index, and No Starch Press",
        "link": "https://pypi.org/project/ezsheets/",
        "concepts": ["ReleaseState", "DocumentationGap"],
        "story": ("The Python Package Index shows EZSheets, by Al Sweigart, first uploaded as version 0.0.1 on February 8, 2019. "
                   "Its documentation page on Read the Docs carries the copyright years 2018 to 2019 and says it is as of November 2019. "
                   "The third edition of Automate the Boring Stuff with Python, 672 pages, was published by No Starch Press in April "
                   "2025 and teaches the library in chapter 15. The newest release, 2026.4.28, was uploaded on April 28, 2026, and its "
                   "code differs from the release before it only in the version string."),
        "lesson": "Read the version you install, not the book's year",
        "source": ("Python Package Index, ezsheets (pypi.org/project/ezsheets/ and the JSON API pypi.org/pypi/ezsheets/json: first upload "
                    "2019-02-08, 18 releases, newest 2026-04-28); ezsheets.readthedocs.io; nostarch.com, 'Automate the Boring Stuff with "
                    "Python, 3rd Edition', April 2025, 672 pp.; this study's comparison of the 2025.11.11 and 2026.4.28 sources."),
    },
]

LINK_STATUS = {'GoogleSheetsXL2Web2006': 200, 'NakamotoPaper2008': 200, 'OAuthBegins2006': 200, 'SheetsApiV3Turndown2021': 200, 'GoogleForms2008': 200, 'EzsheetsRelease2019': 200}


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
    by = {x["id"]: x for x in STORIES}
    for sid, year in (("GoogleSheetsXL2Web2006", "2006"), ("NakamotoPaper2008", "2008"), ("OAuthBegins2006", "2006"),
                      ("SheetsApiV3Turndown2021", "2021"), ("GoogleForms2008", "2008"), ("EzsheetsRelease2019", "2019")):
        if year not in by[sid]["story"] or year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "SEN0414-research/1.0 (teaching; altunel.yusuf@gmail.com)"})
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
