"""SEN0414 chapter 17 - the story companion to the chapter corpus (version 1.1.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for
PDF and Word documents, written fresh for this chapter from sources opened on 2026-10-12 (the HTTP status each link answered to a
plain GET on that day is in LINK_STATUS, and `python3 sen0414_ch17_stories_v1_0_0.py links` asks again):

* WarnockCamelot1991 - in the spring of 1991 John Warnock outlined a system called Camelot, the beginning of the Portable Document
  Format (Wikipedia, 'John Warnock').
* ZipFormat1989 - the ZIP format, first released on 14 February 1989 by PKWARE, designed by Phil Katz and Gary Conway; a .docx file is
  one (Wikipedia, 'ZIP (file format)').
* OoxmlStandard2006 - Office Open XML, first released as ECMA-376 on 7 December 2006 and published as ISO/IEC 29500 in November 2008
  (Wikipedia, 'Office Open XML').
* PdfBecomesIso2008 - PDF 1.7, released in November 2006 and published as ISO 32000-1 in July 2008 (Library of Congress,
  Sustainability of Digital Formats).
* PypdfFourNames - pyPdf (2005), PyPDF2 (end of 2011), PyPDF2 again under a new maintainer (April 2022) and pypdf (2023), the library the
  chapter uses (the pypdf documentation, 'History of pypdf').
* DocxNameTrap2014 - the package docx on PyPI, whose latest release 0.2.4 is dated 6 February 2014 and which the chapter warns the reader not to
  install; this study installed it under Python 3.14.6 and it failed on import (PyPI page of docx; the study's third-party record).

Photograph: see ch17-page/stories_img_v1_0_0.json for what was fetched and under which licence, or why no photograph is used.
A claim the research first planned and dropped: a famous redaction failure in a court filing, for which no page opened on the day gives a
date and a name that Wikipedia or another source of the study confirms; the general fact (text under a black rectangle stays in the
file) is in the study as an executed leaf and in the Wikipedia article on redaction.
1.1.0 (2026-11-11, owner-approved draft 03-materials/ch17/DRAFT_ch17_v1_0_2.md): ZipFormat1989 is replaced by WordDocBinary2008 (the Word .doc specification, 15 February 2008) and OoxmlStandard2006, already told in
chapter 14, by WordSourceCode2014 (the Word for Windows source code, 25 March 2014); the other four stories are unchanged. The lesson of WordSourceCode2014 is shorter than the draft's, to meet the 14-word limit of run_checks.
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.1.0"

STORIES = [
    {
        "id": "WarnockCamelot1991",
        "title": "A 1991 memo called Camelot started the file format of this chapter",
        "when": "Spring 1991",
        "who": "John Warnock, co-founder of Adobe",
        "where": "Adobe Systems, in a document that outlined a system called Camelot",
        "link": "https://en.wikipedia.org/wiki/John_Warnock",
        "concepts": ["HeaderAndTrailer", "ContentStreamText"],
        "story": ("Wikipedia's article on John Warnock says that in the spring of 1991 he outlined a system called Camelot, inventing the "
                  "Portable Document Format. The goal of Camelot, the article quotes, was to capture documents from any application, send "
                  "electronic versions of them anywhere, and view and print them on any machine. Adobe released the first Acrobat on 15 June 1993. "
                  "A PDF file made today still opens with a header line and ends with an offset and %%EOF, and its text is drawing commands "
                  "that place words on a page; chapter 17 reads and rewrites exactly these files with pypdf."),
        "lesson": "A PDF is a page description made to look the same everywhere",
        "source": ("Wikipedia, 'John Warnock' (spring 1991, Camelot, the quoted goal), read 2026-10-12; Wikipedia, 'Adobe Acrobat' (release "
                   "15 June 1993); this study's leaves HeaderAndTrailer and ContentStreamText."),
    },
    {
        "id": "WordDocBinary2008",
        "title": "In February 2008 Microsoft published the format of the old .doc file",
        "when": "15 February 2008",
        "who": "Microsoft, in a post on Brian Jones's Office blog",
        "where": "Microsoft's Office blog, with the Word, Excel and PowerPoint binary format specifications under the Open Specification Promise",
        "link": "https://learn.microsoft.com/en-us/archive/blogs/brian_jones/binary-documentation-doc-xls-ppt-and-translator-project-site-are-now-live",
        "concepts": ["DocxIsZipOfXml"],
        "story": ("Until that day, the older Word format, the binary .doc file, had no openly published specification; on 15 February 2008 Microsoft released the Word 97-2007 binary format specification, "
                  "together with those for .xls and .ppt, as downloadable PDFs under its Open Specification Promise, a pledge not to sue developers who use the specifications. "
                  "Press reports of the week describe the reason as the billions of documents stored in the old binary formats and the wish to let others build converters to the newer Open XML. "
                  "A .docx file is something else: a ZIP package of XML parts. "
                  "On 2026-11-11 this study opened a file that began with the signature of the old binary container (D0 CF 11 E0 A1 B1 1A E1) with python-docx 1.2.0 on Python 3.13.18, and docx.Document raised PackageNotFoundError."),
        "lesson": "python-docx reads .docx only; a .doc is another, binary format, so convert it first",
        "source": ("Microsoft, Office blog of Brian Jones, 'Binary documentation (.doc, .xls, .ppt) and translator project site are now live' (15 February 2008), read 2026-11-11; "
                   "this study's check of 2026-11-11 (python-docx 1.2.0, Python 3.13.18, a file with the OLE signature D0 CF 11 E0 A1 B1 1A E1)."),
    },
    {
        "id": "WordSourceCode2014",
        "title": "In March 2014 the source code of Word for Windows went to a museum",
        "when": "25 March 2014",
        "who": "Charles Simonyi, Richard Brodie and the Computer History Museum",
        "where": "The Computer History Museum, Mountain View, California, with Microsoft's permission",
        "link": "https://computerhistory.org/blog/microsoft-word-for-windows-1-1a-source-code/",
        "concepts": ["DocumentXmlBody"],
        "story": ("The Register says Word began in 1983 as Multi-Tool Word, built on Bravo, the word processor Charles Simonyi created at Xerox PARC. "
                  "The Computer History Museum adds that Simonyi hired Richard Brodie, whom he had first hired at PARC in 1979, and that Word for DOS, released in 1983, was an also-ran beside WordPerfect. "
                  "The first version for Windows came in late 1989 at a single-user price of $495. "
                  "On 25 March 2014 the museum, with Microsoft's permission, made the source code of Word for Windows 1.1a, as it was on 10 January 1991, available for non-commercial use. "
                  "A .docx file is what such a program saves, and python-docx lets a script write the same kind of file without opening Word."),
        "lesson": "A Word file is the saved work of a program people wrote",
        "source": ("Computer History Museum, 'Microsoft Word for Windows Version 1.1a Source Code' (blog, 25 March 2014) and press release of the same date; The Register, 25 March 2014; read 2026-11-11."),
    },
    {
        "id": "PdfBecomesIso2008",
        "title": "In July 2008 Adobe's PDF 1.7 became an international standard",
        "when": "November 2006 and July 2008",
        "who": "Adobe Systems and the International Organization for Standardization",
        "where": "ISO 32000-1:2008, described by the Library of Congress for digital preservation",
        "link": "https://www.loc.gov/preservation/digital/formats/fdd/fdd000277.shtml",
        "concepts": ["CrossReferenceTable", "HeaderAndTrailer"],
        "story": ("The Library of Congress describes PDF 1.7 in its Sustainability of Digital Formats pages. The page says version 1.7 was released in "
                  "November 2006 with Acrobat and Adobe Reader 8.0, and that it was published as ISO 32000-1 in July 2008. "
                  "The standard defines the pieces this study took apart in a small file: the header, the numbered objects, the cross-reference table and the trailer. "
                  "A reader finds the table by reading the last lines, so pypdf can open a file by jumping to the end first."),
        "lesson": "PDF is a public standard with a table at the end",
        "source": ("Library of Congress, 'PDF, Version 1.7 (ISO 32000-1:2008)' (released November 2006; published as ISO 32000-1 in July 2008), "
                   "read 2026-10-12; ISO 32000-1 text at opensource.adobe.com; this study's leaves HeaderAndTrailer and CrossReferenceTable."),
    },
    {
        "id": "PypdfFourNames",
        "title": "The library of chapter 17 has had four names since 2005",
        "when": "2005 to 2023",
        "who": "Mathieu Fenniak, Phaseit, Martin Thoma and the pypdf contributors",
        "where": "pyPdf, PyPDF2, PyPDF3 and PyPDF4, and pypdf",
        "link": "https://pypdf.readthedocs.io/en/stable/meta/history.html",
        "concepts": ["RemovedNames", "MergePositionalTupleTrap"],
        "story": ("The pypdf documentation tells that Mathieu Fenniak launched pyPdf in 2005, whose last release was 1.13 in 2010. "
                  "At the end of 2011 Phaseit sponsored PyPDF2 as a fork, and Martin Thoma took over its maintenance in April 2022. "
                  "PyPDF2 was then merged back into pypdf, all lowercase and without a number. "
                  "Old tutorials still use PdfFileReader and PdfMerger; in this study pypdf 6.20.1 has neither name, and merge() took the tuple the chapter passes as the title of a bookmark, (0, 2), and inserted the whole file."),
        "lesson": "Check the library's release before copying an old tutorial",
        "source": ("pypdf documentation, 'History of pypdf', pypdf.readthedocs.io/en/stable/meta/history.html, read 2026-10-12; this study's leaves "
                   "RemovedNames and MergePositionalTupleTrap."),
    },
    {
        "id": "DocxNameTrap2014",
        "title": "Installing docx instead of python-docx has not worked since 2014",
        "when": "6 February 2014",
        "who": "The authors of the docx package and Steve Canny, who is credited on its page",
        "where": "The Python Package Index, project docx, release 0.2.4",
        "link": "https://pypi.org/project/docx/",
        "concepts": ["PackageNameTrap"],
        "story": ("The page of the docx project on PyPI shows version 0.2.4 as its latest release, dated 6 February 2014, still offering pip install docx. "
                  "Chapter 17 says to install Python-Docx, not Docx, and to write import docx. "
                  "This study installed docx 0.2.4 in Python 3.14.6 and the import failed with ModuleNotFoundError: No module named exceptions, a module of Python 2. "
                  "The working package, python-docx, was at version 1.2.0 when it was released on 16 June 2025."),
        "lesson": "Install python-docx, import docx, and read the project page first",
        "source": ("PyPI, project docx (latest release 0.2.4, 6 February 2014) and pypi.org/pypi/docx/json and pypi.org/pypi/python-docx/json, read 2026-10-12; "
                   "this study's third-party record (the package docx 0.2.4 in Python 3.14.6) and leaf PackageNameTrap."),
    },
]

LINK_STATUS = {'WarnockCamelot1991': 200, 'WordDocBinary2008': 200, 'WordSourceCode2014': 200, 'PdfBecomesIso2008': 200, 'PypdfFourNames': 200, 'DocxNameTrap2014': 200}


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
    for sid, year in (("WarnockCamelot1991", "1991"), ("WordDocBinary2008", "2008"), ("WordSourceCode2014", "2014"),
                      ("PdfBecomesIso2008", "2008"), ("PypdfFourNames", "2005"), ("DocxNameTrap2014", "2014")):
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
