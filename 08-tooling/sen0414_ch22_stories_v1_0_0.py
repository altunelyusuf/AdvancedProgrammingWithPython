"""SEN0414 chapter 22 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for
recognizing text in images, written fresh for this chapter from Wikipedia pages opened on 2026-10-13 (the HTTP status each
link answered to a plain GET on that day is in LINK_STATUS, and `python3 sen0414_ch22_stories_v1_0_0.py links` asks again):

* Goldberg1915 - Hyman Eli Goldberg was granted a patent in 1915 for a device that read characters and converted them to telegraph code; in the same years Edmund Fournier d'Albe's Optophone turned printed letters into tones.
* Goldberg1931 - Emanuel Goldberg's "Statistical Machine", granted US patent 1,838,389 on 29 December 1931, searched rolls of microfilm with photoelectric cells and pattern recognition.
* Kurzweil1976 - Ray Kurzweil founded Kurzweil Computer Products in 1974 for omni-font OCR; the finished reading machine for blind people was unveiled on 13 January 1976.
* Tesseract1985 - Tesseract was developed at Hewlett-Packard laboratories from 1985, released as open source in 2005 and sponsored by Google from 2006.
* Recaptcha2009 - reCAPTCHA, acquired by Google in September 2009, used the words OCR could not read, paired with a known control word, to digitize books.
* Frankenstein1831 - the novel appeared anonymously in 1818, and the revised edition of 1831 under Mary Shelley's name is the print the chapter scans.

Photograph: see ch22-page/stories_img_v1_0_0.json. The single request to Wikimedia Commons answered HTTP 429, so no photograph is used and nothing is claimed about licences.
Every sentence that says "In this study" was run on 2026-10-13 in /home/claude/venv314_ch22_latest (Python 3.14.6, pytesseract 0.3.13, Pillow 12.3.0) with the Tesseract 5.3.4 of Ubuntu.
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "Goldberg1915",
        "title": "A patent of 1915 read characters and sent them as telegraph code",
        "when": "1915",
        "who": "Hyman Eli Goldberg, who was granted the patent, and Edmund Fournier d'Albe, who developed the Optophone",
        "where": "The patent is US Patent 1165663; the Optophone was a handheld scanner moved across a printed page",
        "link": "https://en.wikipedia.org/wiki/Optical_character_recognition",
        "concepts": ["ImageToString", "ReturnType"],
        "story": ("Wikipedia's article on optical character recognition says its roots lie in telegraphy and in reading devices for the blind. "
                  "In 1915 Hyman Eli Goldberg was granted a patent for a device that read perforated or conductive-ink characters and converted them into standard telegraph code. "
                  "Concurrently Edmund Fournier d'Albe developed the Optophone, a handheld scanner that produced tones corresponding to specific letters when it was moved across a printed page. "
                  "In this study pytesseract returned the string 'Tesseract reads this line of text' with a newline at its end for a line the program drew, a str and not a tone or a code."),
        "lesson": "OCR began as a way to send and hear text",
        "source": ("Wikipedia, 'Optical character recognition' (Hyman Eli Goldberg's patent of 1915, US Patent 1165663; the Optophone of Edmund Fournier d'Albe), read 2026-10-13; "
                   "this study's leaves ImageToString and ReturnType."),
    },
    {
        "id": "Goldberg1931",
        "title": "A machine of 1931 searched microfilm by recognizing patterns",
        "when": "1931",
        "who": "Emanuel Goldberg, a physicist and inventor who headed Zeiss Ikon in Dresden",
        "where": "Germany, where he held US patent 1,838,389 for the \"Statistical Machine\", granted on 29 December 1931",
        "link": "https://en.wikipedia.org/wiki/Emanuel_Goldberg",
        "concepts": ["PillowPdf", "TesseractPdf"],
        "story": ("Wikipedia's article on Emanuel Goldberg says he introduced his \"Statistical Machine\", a document search engine that used photoelectric cells and pattern recognition to search the metadata on rolls of microfilmed documents. "
                  "The patent, US 1,838,389, is dated 29 December 1931, and the article says the technology was used in a variant form in 1938 by Vannevar Bush in his microfilm rapid selector. "
                  "A picture of a page is only searchable once something has read it. "
                  "In this study a PDF that Pillow made from frankenstein.png held 0 characters of text for pdftotext, while the PDF that Tesseract made through pytesseract held 578 characters in 106 word boxes."),
        "lesson": "A scan only becomes searchable after it is read",
        "source": ("Wikipedia, 'Emanuel Goldberg' (the Statistical Machine, US patent 1,838,389 of 29 December 1931, searching microfilm with photoelectric cells and pattern recognition), read 2026-10-13; "
                   "this study's leaves PillowPdf and TesseractPdf and the program pdfRoutes."),
    },
    {
        "id": "Kurzweil1976",
        "title": "A reading machine for blind people was unveiled in January 1976",
        "when": "1976",
        "who": "Ray Kurzweil, who founded Kurzweil Computer Products, Inc. in 1974, with the leaders of the National Federation of the Blind",
        "where": "A widely reported news conference, with a machine that had a CCD-type flatbed scanner and a text-to-speech synthesizer",
        "link": "https://en.wikipedia.org/wiki/Kurzweil_Computer_Products",
        "concepts": ["FontChoice", "SmallText"],
        "story": ("Wikipedia's article on Kurzweil Computer Products says that in 1974 Ray Kurzweil founded the company and led development of the first omni-font optical character recognition system, a program able to recognize text in any normal font, where scanners before could read only a few fonts. "
                  "The article on OCR gives 13 January 1976 as the day the finished reading machine for blind people was unveiled at a news conference. "
                  "He later sold the company to Xerox. "
                  "In this study six typefaces (DejaVu Sans, Serif, Mono and Bold, Nimbus Roman and Z003 italic script) drawn at 24 pixels were read with character error rates from 0.0 to 0.0116, and the same text drawn at 8 pixels with 0.2394."),
        "lesson": "Fonts stopped mattering, size still does",
        "source": ("Wikipedia, 'Kurzweil Computer Products' (founded 1974, the first omni-font OCR system, sold to Xerox) and 'Optical character recognition' (unveiled 13 January 1976), read 2026-10-13; "
                   "this study's leaves FontChoice and SmallText."),
    },
    {
        "id": "Tesseract1985",
        "title": "Tesseract began in the Hewlett-Packard laboratories in 1985",
        "when": "1985",
        "who": "Hewlett-Packard laboratories in Bristol, England and Greeley, Colorado, then the University of Nevada, Las Vegas, and Google",
        "where": "Bristol and Greeley, between 1985 and 1994; open source from 2005; sponsored by Google from 2006",
        "link": "https://en.wikipedia.org/wiki/Tesseract_(software)",
        "concepts": ["EngineVersion", "FastBestLegacy"],
        "story": ("Wikipedia's article on Tesseract says the engine was developed as proprietary software at Hewlett-Packard laboratories between 1985 and 1994 and was released as open source in 2005 by Hewlett-Packard and the University of Nevada, Las Vegas. "
                  "Google sponsored its development from 2006. "
                  "Version 4, released in 2018, added the LSTM-based engine, and version 5 followed in 2021. "
                  "In this study the Tesseract on the PATH reported 5.3.4, and the 4,113,088 bytes of its English data were byte for byte the file of the tessdata_fast repository."),
        "lesson": "The engine you call has a version and a lineage",
        "source": ("Wikipedia, 'Tesseract (software)' (Hewlett-Packard 1985 to 1994, open source 2005, Google 2006, LSTM engine in version 4 of 2018, version 5 of 2021), read 2026-10-13; "
                   "this study's leaves EngineVersion and FastBestLegacy."),
    },
    {
        "id": "Recaptcha2009",
        "title": "Google bought a puzzle that read the words OCR could not",
        "when": "2009",
        "who": "reCAPTCHA, developed at Carnegie Mellon University and acquired by Google",
        "where": "Web sites that showed the puzzle, and the digitization of the archives of The New York Times and of Google Books",
        "link": "https://en.wikipedia.org/wiki/ReCAPTCHA",
        "concepts": ["LowConfidenceWords", "RealWordErrors"],
        "story": ("Wikipedia's article on reCAPTCHA says it was acquired by Google in September 2009 and that it helped to digitize the archives of The New York Times and then Google Books. "
                  "The original service was a mass collaboration platform for digitizing books too illegible for computers. "
                  "Its prompts used pairs of words from scanned pages, one known word as a control for verification and a second to crowdsource the reading of an uncertain word. "
                  "In this study Tesseract's own confidence did a small part of that sorting: of the 106 words of frankenstein.png the wrongly read 'In' had confidence 55 against a mean of 94.5."),
        "lesson": "Uncertain words are the ones to hand to a human",
        "source": ("Wikipedia, 'ReCAPTCHA' (acquired by Google in September 2009; pairs of words with one known control word; the archives of The New York Times), read 2026-10-13; "
                   "this study's leaves LowConfidenceWords and RealWordErrors."),
    },
    {
        "id": "Frankenstein1831",
        "title": "The page the book scans comes from the revised edition of 1831",
        "when": "1831",
        "who": "Mary Shelley, whose name appeared on the revised edition of 1831 of a novel first published anonymously in 1818",
        "where": "London; the 1831 text had stylistic revisions and a new preface, and the chapter scans a page of that print",
        "link": "https://en.wikipedia.org/wiki/Frankenstein",
        "concepts": ["FrankensteinOutput", "ExactResultsVary"],
        "story": ("Wikipedia's article on Frankenstein says the novel was first published anonymously on 1 January 1818 and that in 1831 a revised edition was published under Mary Shelley's name. "
                  "The 1831 version included significant stylistic revisions and a new preface, and chapter 22 of the book scans a page of that print, whose paper is wrinkled and yellowed. "
                  "The book prints 'Iv' for the first word of the chapter. "
                  "In this study Tesseract 5.3.4 returned 'In' for it, 4.1.1 and 5.5.3 with the fast data 'Iv', and the 106 words came back with 2 wrong, a character error rate of 0.0035."),
        "lesson": "Old print gives different mistakes on different engines",
        "source": ("Wikipedia, 'Frankenstein' (first published anonymously in 1818; the revised edition of 1831 under Mary Shelley's name), read 2026-10-13; "
                   "this study's leaves FrankensteinOutput and ExactResultsVary."),
    },
]

LINK_STATUS = {'Goldberg1915': 200, 'Goldberg1931': 200, 'Kurzweil1976': 200, 'Tesseract1985': 200, 'Recaptcha2009': 200, 'Frankenstein1831': 200}


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
    for sid, year in (("Goldberg1915", "1915"), ("Goldberg1931", "1931"), ("Kurzweil1976", "1976"), ("Tesseract1985", "1985"), ("Recaptcha2009", "2009"), ("Frankenstein1831", "1831")):
        if year not in by[sid]["story"] and year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
        if year not in by[sid]["when"]:
            bad.append("%s: year %s not in when" % (sid, year))
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "sen0414-study/1.0 (altunel.yusuf@gmail.com)"})
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
