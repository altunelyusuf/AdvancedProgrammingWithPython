"""SEN0414 chapter 14 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for
Excel Spreadsheets, written fresh for this chapter from sources opened on 2026-10-12 (the HTTP status each link answered to a
plain GET on that day is in LINK_STATUS, and `python3 sen0414_ch14_stories_v1_0_0.py links` asks again):

* BricklinVisiCalc1979 - Dan Bricklin's own account of the idea of the electronic spreadsheet at Harvard Business School in
  1978, the first Apple II prototype and VisiCalc, which came out on the Apple II in 1979.
* MicrosoftExcel1985 - Excel for the Macintosh, announced on 2 May 1985 and on sale on 30 September 1985, the first Windows
  version in 1987, and the 1900 leap-year bug kept from Lotus 1-2-3 (Wikipedia, whose article cites its sources).
* OoxmlStandard2006 - Office Open XML: TC45 of Ecma set up in December 2005, ECMA 376 approved in December 2006, ISO/IEC 29500
  in early 2008 (Library of Congress format description), the format of every .xlsx file.
* OpenpyxlLibrary2010 - openpyxl, by Eric Gazoni and Charlie Clark, initially based on PHPExcel, first uploaded to PyPI on
  11 August 2010 (openpyxl 1.1.0).
* HerndonSpreadsheet2013 - Herndon, Ash and Pollin's April 2013 working paper, which found a spreadsheet coding error in the
  working file of Reinhart and Rogoff that left five countries out.
* ZiemannGeneNames2016 - Ziemann, Eren and El-Osta's Genome Biology paper of 23 August 2016 on gene symbols that Excel turns into
  dates: errors in 704 of 3,597 papers with supplementary gene lists.

No photograph is used. Wikimedia Commons' search answered on the third try (and HTTP 429 for Thomas Herndon on three tries) and
named File:Dan Bricklin - 2007.jpg, CC BY 2.5, photo by Betsy Devine, but the image server (upload.wikimedia.org) answered
HTTP 429 to about twenty requests for it over about forty minutes, so the file was never fetched and no licence record of a
fetched file exists; the other five stories name people with no picture on the pages read. ch14-page/stories_img_v1_0_0.json says
so, and 03-materials/ch14/assets is not made. A claim the research first planned and dropped: that some program before VisiCalc
was the first spreadsheet; no page that could be opened supported it. Usage: import STORIES; run
the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "BricklinVisiCalc1979",
        "title": "A business student pictured a calculator with rows and columns in 1978",
        "when": "1979",
        "who": "Dan Bricklin and Bob Frankston",
        "where": "Harvard Business School, Cambridge, Massachusetts",
        "link": "http://www.bricklin.com/history/saiidea.htm",
        "concepts": ["CellByName", "ColumnToLetter"],
        "story": ("Dan Bricklin had the idea for an electronic spreadsheet in the spring of 1978, as an MBA student at Harvard "
                   "Business School, and decided that summer to turn it into a product. He prototyped the screen in Basic on the "
                   "school's timesharing system, and that is when the wish to place numbers, formula results and text turned into "
                   "rows and columns with human-friendly names. His work journal dates the first prototype on an Apple II, borrowed from "
                   "Dan Fylstra of Personal Software, to October 8, 1978. With Bob Frankston he made VisiCalc, which Personal Software "
                   "published and which first came out on the Apple II in 1979."),
        "lesson": "The grid of named rows and columns is the idea openpyxl still addresses",
        "source": ("Dan Bricklin, 'The Idea', bricklin.com/history/saiidea.htm (spring and summer 1978, journal entry of October 8, "
                    "1978); Dan Bricklin, 'VisiCalc executable', bricklin.com/history/vcexecutable.htm (the original VisiCalc first "
                    "came out on the Apple II in 1979)."),
    },
    {
        "id": "MicrosoftExcel1985",
        "title": "Excel was announced for the Macintosh in 1985 and kept a bug from Lotus 1-2-3",
        "when": "1985",
        "who": "Microsoft, with Steve Jobs of Apple and Bill Gates",
        "where": "Tavern on the Green, New York City",
        "link": "https://en.wikipedia.org/wiki/Microsoft_Excel",
        "concepts": ["DatesAsDatetime", "FileFormats"],
        "story": ("Microsoft launched its first spreadsheet, Multiplan, in 1982, and began developing a new one, codenamed Odyssey, "
                   "in 1983, when Lotus 1-2-3 had become the dominant program. On May 2, 1985, Steve Jobs of Apple and Bill Gates "
                   "announced Excel for the Macintosh at a press conference at Tavern on the Green in New York City, and it went on "
                   "sale on September 30, 1985. The first Windows version, Excel 2.05, followed on November 19, 1987. Excel still "
                   "treats February 29, 1900 as a day, a bug that began in Lotus 1-2-3 and was kept on purpose for compatibility, "
                   "and that has been carried over into the Office Open XML file format that openpyxl reads."),
        "lesson": "A file format keeps the habits and the bugs of its program",
        "source": ("'Microsoft Excel', Wikipedia, en.wikipedia.org/wiki/Microsoft_Excel, sections Early history (1982 Multiplan, 1983 "
                    "Odyssey, May 2 and September 30, 1985, November 19, 1987) and Fictional leap day in 1900; the article cites its own "
                    "sources and is a secondary source."),
    },
    {
        "id": "OoxmlStandard2006",
        "title": "The .xlsx format became a standard in 2006 and an ISO standard in 2008",
        "when": "2006",
        "who": "Microsoft and Ecma International's technical committee TC45",
        "where": "Ecma International and ISO/IEC JTC 1",
        "link": "https://www.loc.gov/preservation/digital/formats/fdd/fdd000395.shtml",
        "concepts": ["FileFormats", "ChartXml"],
        "story": ("Microsoft submitted documentation of its Office Open XML formats to Ecma International, which set up its "
                   "technical committee TC45 in December 2005 to review them. The document was approved as ECMA 376 in December "
                   "2006 and submitted for standardization through ISO/IEC JTC 1 in early 2007, and approval as ISO/IEC 29500 "
                   "followed in early 2008. A spreadsheet file in the family is an XLSX file, specified through SpreadsheetML inside a "
                   "package based on ZIP, which is what openpyxl opens when chapter 14 calls load_workbook."),
        "lesson": "An .xlsx file is a documented zip of XML that any program may read",
        "source": ("Library of Congress, Sustainability of Digital Formats, 'OOXML Format Family - ISO/IEC 29500 and ECMA 376' "
                    "(fdd000395): TC45 established in December 2005, ECMA 376 approved in December 2006, ISO/IEC 29500 approval in early "
                    "2008, XLSX specified via SpreadsheetML, ZIP-based package. The Ecma and ISO pages could not be opened from this "
                    "machine."),
    },
    {
        "id": "OpenpyxlLibrary2010",
        "title": "openpyxl was born in 2010 from the lack of a Python library for Office Open XML",
        "when": "2010",
        "who": "Eric Gazoni and Charlie Clark",
        "where": "The open-source Python community",
        "link": "https://openpyxl.readthedocs.io/en/stable/",
        "concepts": ["OpenpyxlRelease", "LoadWorkbook"],
        "story": ("The documentation of openpyxl says it was born from the lack of an existing library to read and write the Office "
                   "Open XML format natively from Python, and that it was initially based on PHPExcel. It names Eric Gazoni and "
                   "Charlie Clark as its authors, and the first upload of the package to the Python Package Index, openpyxl 1.1.0, is "
                   "dated August 11, 2010. The project describes itself as maintained by volunteers in their spare time. On "
                   "October 12, 2026 its newest stable release was 3.1.5, uploaded in June 2024, and it is the library on which "
                   "every program of chapter 14 is built."),
        "lesson": "The library behind the chapter is volunteer work, so check which release you ran",
        "source": ("openpyxl documentation, start page (authors, 'born from lack of existing library', PHPExcel, volunteers); PyPI "
                    "JSON record of openpyxl (pypi.org/pypi/openpyxl/json: first upload of 1.1.0 on 2010-08-11, newest 3.1.5 of "
                    "2024-06-28), read on 2026-10-12."),
    },
    {
        "id": "HerndonSpreadsheet2013",
        "title": "A graduate student found a spreadsheet error that left five countries out",
        "when": "2013",
        "who": "Thomas Herndon, Michael Ash and Robert Pollin",
        "where": "Political Economy Research Institute, University of Massachusetts",
        "link": "https://peri.umass.edu/publication/does-high-public-debt-consistently-stifle-economic-growth-a-critique-of-reinhart-and-rogoff/",
        "concepts": ["FormulaString", "RoundingDiffers"],
        "story": ("In April 2013 Herndon, Ash and Pollin published a working paper that replicated Reinhart and Rogoff's "
                   "study of public debt and economic growth. Using the authors' working spreadsheet, they found a coding error that "
                   "entirely excluded five countries, Australia, Austria, Belgium, Canada and Denmark, from the analysis. With "
                   "the selective exclusion of data and an unusual weighting, they found that average real growth for debt above 90 "
                   "percent of GDP was 2.2 percent a year and not the -0.1 percent that Reinhart and Rogoff published. The spreadsheet error, "
                   "together with other errors, accounts for a -0.3 percentage-point error in the published average of the highest debt "
                   "category."),
        "lesson": "A spreadsheet formula is code, so it needs a second reader and a test",
        "source": ("Herndon, Ash and Pollin, 'Does High Public Debt Consistently Stifle Economic Growth? A Critique of Reinhart and "
                    "Rogoff', PERI Working Paper, April 15, 2013 (abstract; section 'Spreadsheet coding error'); the PERI publication "
                    "page, peri.umass.edu, read on 2026-10-12."),
    },
    {
        "id": "ZiemannGeneNames2016",
        "title": "Excel turned gene names into dates in one paper in five",
        "when": "2016",
        "who": "Mark Ziemann, Yotam Eren and Assam El-Osta",
        "where": "Genome Biology, published August 23, 2016",
        "link": "https://genomebiology.biomedcentral.com/articles/10.1186/s13059-016-1044-7",
        "concepts": ["DataTypes", "DatesAsDatetime"],
        "story": ("Excel with its default settings turns gene symbols such as SEPT2 and MARCH1 into the dates 2-Sep and 1-Mar, a "
                   "problem first described in 2004. In 2016 Ziemann, Eren and El-Osta screened 35,175 supplementary Excel files "
                   "from 18 journals published from 2005 to 2015 and found gene lists attached to 3,597 papers. They confirmed gene "
                   "name errors in 987 files from 704 articles, which is 19.6 percent of the published articles with such lists in "
                   "the journals they selected. In openpyxl a symbol written into a cell as a string keeps the data type s, "
                   "and no date is made of it."),
        "lesson": "Check what a spreadsheet application did to your data before you trust it",
        "source": ("Ziemann, Eren and El-Osta, 'Gene name errors are widespread in the scientific literature', Genome Biology 17, "
                    "177 (2016), doi 10.1186/s13059-016-1044-7 (abstract and Results: 35,175 files, 7467 gene lists, 3597 papers, "
                    "987 files, 704 articles, 19.6 %)."),
    },
]

# HTTP status of a plain GET (python urllib, User-Agent 'SEN0414-research/1.0') to each link, 2026-10-12.
LINK_STATUS = {'BricklinVisiCalc1979': 200, 'MicrosoftExcel1985': 200, 'OoxmlStandard2006': 200, 'OpenpyxlLibrary2010': 200, 'HerndonSpreadsheet2013': 200, 'ZiemannGeneNames2016': 200}


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
    for sid, year in (("BricklinVisiCalc1979", "1979"), ("MicrosoftExcel1985", "1985"), ("OoxmlStandard2006", "2006"),
                      ("OpenpyxlLibrary2010", "2010"), ("HerndonSpreadsheet2013", "2013"), ("ZiemannGeneNames2016", "2016")):
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
