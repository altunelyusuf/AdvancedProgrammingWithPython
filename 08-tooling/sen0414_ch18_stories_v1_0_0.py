"""SEN0414 chapter 18 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for
CSV, JSON and XML files, written fresh for this chapter from sources opened on 2026-10-12 (the HTTP status each link answered to a
plain GET on that day is in LINK_STATUS, and `python3 sen0414_ch18_stories_v1_0_0.py links` asks again):

* CsvFortran1972 - the IBM Fortran (level H extended) compiler under OS/360 read comma-separated values in 1972; the abbreviation CSV was in
  use by 1983 (Wikipedia, 'Comma-separated values').
* Rfc4180In2005 - RFC 4180, October 2005, by Yakov Shafranovich, the written definition of CSV: CRLF line ends, an optional header, and a last
  record that may or may not end in a line break (RFC Editor).
* JsonMessage2001 - Douglas Crockford sent the first JSON message in April 2001 with Chip Morningstar at State Software (Wikipedia, 'JSON').
* Xml10In1998 - the W3C published XML 1.0 as a Recommendation on 10 February 1998, after work that began in mid-1996 under Jon Bosak (W3C;
  Wikipedia, 'XML').
* PythonLibraries2006 - ElementTree came into the standard library with Python 2.5 on 19 September 2006 and json, from simplejson by Bob Ippolito,
  with Python 2.6 on 1 October 2008 (the 'What's New' pages of Python).
* BillionLaughs2002 - the billion laughs attack, reported as early as 2002 and widely addressed from 2008, a 760-byte document that asks for a
  billion copies of lol (Wikipedia, 'Billion laughs attack').

Photograph: see ch18-page/stories_img_v1_0_0.json for what was fetched and under which licence, or why no photograph is used.
A claim the research first planned and dropped: the exact day on which Crockford registered json.org, for which no page opened on the day gives
a date that another source of the study confirms.
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "CsvFortran1972",
        "title": "Commas separated values on IBM mainframes in 1972, long before personal computers",
        "when": "1972, and by 1983 under the name CSV",
        "who": "The IBM Fortran (level H extended) compiler and the people who wrote spreadsheets for it",
        "where": "IBM OS/360, list-directed input and output with commas between the values",
        "link": "https://en.wikipedia.org/wiki/Comma-separated_values",
        "concepts": ["FieldsAndRecords", "QuotedCommaField"],
        "story": ("Wikipedia's article on comma-separated values says the format predates personal computers by more than a decade: the IBM Fortran (level H extended) compiler "
                  "under OS/360 supported list-directed free-form input and output, with commas between values, in 1972. List-directed input was defined in FORTRAN 77, approved in 1978, "
                  "and it used commas or spaces as delimiters, so an unquoted string could not contain either. The term comma-separated value and the abbreviation CSV were in use by 1983. "
                  "The quoting rule that lets a field hold a comma is the answer to that old limit: in this study the line with 'Hello, world!' in quotes split into five pieces with split(','), "
                  "and into four fields with csv.reader."),
        "lesson": "Never split a CSV line on commas yourself; let csv.reader read it",
        "source": ("Wikipedia, 'Comma-separated values' (History: IBM Fortran 1972, FORTRAN 77 in 1978, the term in use by 1983), read 2026-10-12; "
                   "this study's leaves FieldsAndRecords and QuotedCommaField."),
    },
    {
        "id": "Rfc4180In2005",
        "title": "In October 2005 an informational RFC wrote down what CSV had been for thirty years",
        "when": "October 2005",
        "who": "Yakov Shafranovich, in the IETF's RFC series, with the text/csv media type registered at IANA",
        "where": "RFC 4180, Common Format and MIME Type for Comma-Separated Values (CSV) Files",
        "link": "https://www.rfc-editor.org/rfc/rfc4180",
        "concepts": ["LastRecordNoBreak", "EmbeddedLineBreak"],
        "story": ("RFC 4180, dated October 2005 and written by Yakov Shafranovich, is an Informational memo that documents the common format and registers the MIME type text/csv. "
                  "It says each record is on a separate line delimited by a line break (CRLF), that the last record may or may not have an ending line break, "
                  "and that a header line is optional. Fields with line breaks, double quotes or commas must be enclosed in double quotes, and a quote inside is written twice. "
                  "Python's csv module follows these habits: in this study a record with a line break inside quotes read as one record on two lines, and a final record with no line break read the same as one with it."),
        "lesson": "RFC 4180 describes common practice; real files still differ",
        "source": ("RFC 4180, rfc-editor.org (October 2005, Y. Shafranovich, Informational; rules 1 to 7), read 2026-10-12; IANA registration of text/csv; "
                   "this study's leaves LastRecordNoBreak and EmbeddedLineBreak."),
    },
    {
        "id": "JsonMessage2001",
        "title": "The first JSON message was sent in April 2001",
        "when": "April 2001",
        "who": "Douglas Crockford and Chip Morningstar, at State Software",
        "where": "State Software, a company cofounded in March 2001 to build stateful web applications in the browser",
        "link": "https://en.wikipedia.org/wiki/JSON",
        "concepts": ["SixValueTypes", "TrailingCommaRefused"],
        "story": ("Wikipedia's article on JSON says Douglas Crockford originally specified the format in the early 2000s and sent the first JSON message in April 2001 with Chip Morningstar. "
                  "The acronym came from State Software, a company he cofounded with others in March 2001. "
                  "RFC 4627 was its informational specification from 2006, ECMA-404 standardized it in 2013, and RFC 8259, published in 2017, is the current Internet standard. "
                  "The format is small enough to fit on one page, and a parser is strict about it: in this study json.loads refused the chapter's own example, a list with a comma before the closing bracket, in Python 3.14.6."),
        "lesson": "JSON is tiny and strict; one extra comma is an error",
        "source": ("Wikipedia, 'JSON' (first message April 2001, State Software March 2001, RFC 4627 in 2006, ECMA-404 in 2013, RFC 8259 in 2017), read 2026-10-12; "
                   "RFC 8259; this study's leaves SixValueTypes and TrailingCommaRefused."),
    },
    {
        "id": "Xml10In1998",
        "title": "XML 1.0 became a W3C Recommendation on 10 February 1998",
        "when": "10 February 1998, after work that began in mid-1996",
        "who": "The W3C XML working group, started by Jon Bosak of Sun Microsystems",
        "where": "The World Wide Web Consortium, as a simplified descendant of SGML for use on the web",
        "link": "https://en.wikipedia.org/wiki/XML",
        "concepts": ["SingleRootRequired", "CaseSensitiveTags"],
        "story": ("Wikipedia's article on XML gives 10 February 1998 as the date XML 1.0 was first published as a W3C Recommendation. "
                  "Work began in mid-1996 when the Sun Microsystems engineer Jon Bosak developed a charter and recruited collaborators who knew both SGML and the Web. "
                  "The first edition of the specification, still on the W3C site, carries the date 10-February-1998; the fifth edition is dated 26 November 2008. "
                  "The rules were made strict on purpose, which this study saw in ElementTree: the closing tag a for the opening tag A was a mismatched tag, and two roots were junk after the document element."),
        "lesson": "XML is strict by design: one root, matching case, closed tags",
        "source": ("Wikipedia, 'XML' (work began mid-1996, Jon Bosak; first published 10 February 1998), read 2026-10-12; W3C, XML 1.0 first edition "
                   "(REC-xml-19980210) and fifth edition (26 November 2008); this study's leaves SingleRootRequired and CaseSensitiveTags."),
    },
    {
        "id": "PythonLibraries2006",
        "title": "ElementTree joined Python in 2006 and json in 2008",
        "when": "19 September 2006 and 1 October 2008",
        "who": "Fredrik Lundh, whose ElementTree library was added, and Bob Ippolito, who wrote simplejson, which became json",
        "where": "The standard library of Python 2.5 (xml.etree) and Python 2.6 (json)",
        "link": "https://docs.python.org/3/whatsnew/2.5.html",
        "concepts": ["RootTagAndChildren", "IterDocumentOrder"],
        "story": ("The 'What's New in Python 2.5' page says the release came out on 19 September 2006 and added a subset of Fredrik Lundh's ElementTree library as xml.etree, version 1.2.6 of the library, with the cElementTree accelerator. "
                  "The 'What's New in Python 2.6' page, for the release of 1 October 2008, says json, originally called simplejson, was written by Bob Ippolito. "
                  "The two modules of chapter 18 have therefore been in the standard library for 20 and 18 years. "
                  "In Python 3.14.6 this study still imported xml.etree.cElementTree, though its documentation calls the alias deprecated, and found that getchildren() and getiterator() of the old tutorials are gone."),
        "lesson": "Old tutorials use old names; check the release you run",
        "source": ("Python documentation, 'What's New in Python 2.5' (released 19 September 2006; the ElementTree package), and 'What's New in Python 2.6' "
                   "(released 1 October 2008; the json module), read 2026-10-12; this study's third-party record (removed names) and leaves RootTagAndChildren and IterDocumentOrder."),
    },
    {
        "id": "BillionLaughs2002",
        "title": "A 760-byte XML file that asks for a billion laughs",
        "when": "First reported as early as 2002, widely addressed from 2008",
        "who": "Parser authors and security reporters, and the people who named it the billion laughs attack or XML bomb",
        "where": "Any XML parser that expands entities declared in the document's own DTD",
        "link": "https://en.wikipedia.org/wiki/Billion_laughs_attack",
        "concepts": ["BillionLaughsLimit", "XmltodictEntitiesDisabled"],
        "story": ("Wikipedia's article on the billion laughs attack says it targets XML parsers and is also called an XML bomb or an exponential entity expansion attack. "
                  "The example defines 10 entities, each made of 10 of the one before, so one use of the largest expands to a billion copies of lol, almost 3 gigabytes. "
                  "The problem was first reported as early as 2002 and began to be widely addressed in 2008; the article's references include the entry CVE-2003-1564. "
                  "In this study a 760-byte file of that kind was refused by ElementTree in Python 3.14.6 with a limit on input amplification, and xmltodict 1.0.4 refused every entity, while xmltodict 0.13.0, the version Appendix A pins, parsed it."),
        "lesson": "Never parse untrusted XML with a parser you have not checked",
        "source": ("Wikipedia, 'Billion laughs attack' (the example, almost 3 gigabytes, reported as early as 2002, widely addressed in 2008, CVE-2003-1564 among the references), read 2026-10-12; "
                   "Python 3.14 documentation, XML security; this study's leaves BillionLaughsLimit and XmltodictEntitiesDisabled."),
    },
]

LINK_STATUS = {'CsvFortran1972': 200, 'Rfc4180In2005': 200, 'JsonMessage2001': 200, 'Xml10In1998': 200, 'PythonLibraries2006': 200, 'BillionLaughs2002': 200}


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
    for sid, year in (("CsvFortran1972", "1972"), ("Rfc4180In2005", "2005"), ("JsonMessage2001", "2001"), ("Xml10In1998", "1998"), ("PythonLibraries2006", "2006"), ("BillionLaughs2002", "2002")):
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
