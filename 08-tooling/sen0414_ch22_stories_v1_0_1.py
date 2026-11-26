"""SEN0414 chapter 22 - the story companion to the chapter corpus (version 1.0.1).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Five stories for
reading text from images, following the chapter 22 deck 4.0.0 (Lineage14), whose five stories are these five with sourced pictures:

* Goldberg1931 - Emanuel Goldberg's Statistical Machine, US patent 1,838,389, granted 29 December 1931, searched microfilm with photoelectric cells and pattern recognition; the picture is the memorial stone for him in Dresden.
* Kurzweil1976 - Ray Kurzweil founded Kurzweil Computer Products in 1974 for omni-font OCR; the reading machine for blind people was unveiled on 13 January 1976.
* Tesseract1985 - Tesseract was developed at Hewlett-Packard laboratories from 1985, released as open source in 2005 and sponsored by Google from 2006.
* Recaptcha2009 - reCAPTCHA, started at Carnegie Mellon University in a team around Luis von Ahn, was acquired by Google in September 2009; it used words that OCR could not read, paired with a known word.
* Frankenstein1831 - the novel appeared anonymously in 1818, and the revised edition of 1831 carries Mary Shelley's name; the picture is its frontispiece engraving by Theodor von Holst.

Version 1.0.1 over 1.0.0: the Goldberg1915 story is dropped (the deck 4.0.0 tells one Goldberg story, that of 1931), and the facts of the five are those of version 1.0.0 (Wikipedia pages opened on 2026-10-13).
ch22-page/stories_img_v9_109_0.json holds the picture of each story on the page and its credit; 03-materials/ch22/assets/story_images_v1_0_0.json holds each licence.
Every sentence that says "In this study" was run on 2026-11-26 in /tmp/v21 (Python 3.12.3, Pillow 13.0.0, pytesseract 0.3.13) with the Tesseract 5.3.4 of Ubuntu.
The HTTP status each link answered to a plain GET on 2026-11-26 is in LINK_STATUS (`python3 sen0414_ch22_stories_v1_0_1.py links` asks again).
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.1"

STORIES = [
    {
        "id": "Goldberg1931",
        "title": "A machine of 1931 searched microfilm by recognizing patterns",
        "when": "1931",
        "who": "Emanuel Goldberg, an engineer, who was granted the patent for his Statistical Machine",
        "where": "The patent is US patent 1,838,389; the memorial stone in the picture lies in Dresden",
        "link": "https://en.wikipedia.org/wiki/Emanuel_Goldberg",
        "concepts": ["ImageToString", "ReturnType"],
        "story": ("Wikipedia's article on Emanuel Goldberg says that his Statistical Machine, granted US patent 1,838,389 on 29 December 1931, searched rolls of microfilm with photoelectric cells and pattern recognition. "
                  "The memorial stone laid for him in Dresden gives his birth year, 1881, his flight in 1933 to France and his move in 1937 to Palestine. "
                  "Tesseract also finds the shapes of letters in a picture. "
                  "In this study image_to_string() returned the str 'Hello OCR 2026' with a line break for a line that the program drew."),
        "lesson": "A machine matched the shapes of letters long before Python",
        "source": ("Wikipedia, 'Emanuel Goldberg' (Statistical Machine, US patent 1,838,389, 29 December 1931), read 2026-10-13; the inscription of the Stolperstein in the picture (Wikimedia Commons, photo Dr. Bernd Gross); "
                   "this study's leaves ImageToString and ReturnType."),
    },
    {
        "id": "Kurzweil1976",
        "title": "The first reading machine for blind people was unveiled in 1976",
        "when": "1974 to 1976",
        "who": "Ray Kurzweil, who founded Kurzweil Computer Products",
        "where": "Kurzweil Computer Products, in the United States",
        "link": "https://en.wikipedia.org/wiki/Kurzweil_Computer_Products",
        "concepts": ["SmallText", "Skew"],
        "story": ("Wikipedia's article on Kurzweil Computer Products says that Ray Kurzweil founded it in 1974 to build OCR that reads any typeface, not one fixed font. "
                  "The reading machine for blind people, which scanned a page and spoke it aloud, was unveiled on 13 January 1976. "
                  "A reading is only as good as its picture. "
                  "In this study a sentence drawn 8 pixels high was read as nothing, at 9 pixels the reading matched the truth by 0.95, and a page tilted by 9 degrees was not read."),
        "lesson": "A reading is only as good as its picture",
        "source": ("Wikipedia, 'Kurzweil Computer Products' (founded 1974; reading machine unveiled 13 January 1976), read 2026-10-13; "
                   "this study's leaves SmallText and Skew."),
    },
    {
        "id": "Tesseract1985",
        "title": "Tesseract began at Hewlett-Packard in 1985 and became open source",
        "when": "1985 to 2006",
        "who": "Hewlett-Packard laboratories, which developed it, and Google, which sponsored it from 2006",
        "where": "Hewlett-Packard laboratories",
        "link": "https://en.wikipedia.org/wiki/Tesseract_(software)",
        "concepts": ["TheEngine", "EngineVersion"],
        "story": ("Wikipedia's article on Tesseract says it was developed at Hewlett-Packard laboratories from 1985. "
                  "Hewlett-Packard released it as open source in 2005, and Google sponsored its development from 2006. "
                  "Other tools can therefore offer it as a choice; the picture shows the transcription tool of Wikisource, set to the Tamil script. "
                  "In this study pytesseract answered get_tesseract_version() with 5.3.4 and listed 22 language files."),
        "lesson": "An engine from 1985 is still the one pytesseract calls",
        "source": ("Wikipedia, 'Tesseract (software)' (developed at HP laboratories from 1985; open source in 2005; Google sponsorship from 2006), read 2026-10-13; the screenshot of Wikisource (Wikimedia Commons, Balajijagadesh, CC BY 4.0); "
                   "this study's leaves TheEngine and EngineVersion."),
    },
    {
        "id": "Recaptcha2009",
        "title": "reCAPTCHA used what OCR could not read to digitize books",
        "when": "2009",
        "who": "A team around Luis von Ahn at Carnegie Mellon University, and Google, which acquired reCAPTCHA",
        "where": "Carnegie Mellon University, and then Google",
        "link": "https://en.wikipedia.org/wiki/ReCAPTCHA",
        "concepts": ["RealWordErrors", "CharacterErrorRate"],
        "story": ("Wikipedia's article on reCAPTCHA says Google acquired it in September 2009. "
                  "It showed two words: one the program knew, and one that OCR had failed to read, and a correct answer to the first gave weight to the answer for the second. "
                  "A reading can be checked in the same way against a known text. "
                  "In this study difflib compared a reading with its truth, found four differences and gave a similarity of 0.86."),
        "lesson": "Compare a reading with a known text to find its mistakes",
        "source": ("Wikipedia, 'ReCAPTCHA' (acquired by Google in September 2009; a known word paired with a word that OCR could not read), read 2026-10-13; "
                   "this study's leaves RealWordErrors and CharacterErrorRate."),
    },
    {
        "id": "Frankenstein1831",
        "title": "The 1831 edition of Frankenstein is the page the book scans",
        "when": "1818 and 1831",
        "who": "Mary Shelley, the author, and Theodor von Holst, who made the frontispiece engraving",
        "where": "London, where the revised edition of 1831 was published",
        "link": "https://en.wikipedia.org/wiki/Frankenstein",
        "concepts": ["FrankensteinOutput", "LineBreaks"],
        "story": ("Wikipedia's article on Frankenstein says the novel appeared anonymously in 1818 and that a revised edition of 1831 carries Mary Shelley's name. "
                  "The picture is the frontispiece engraving of that edition by Theodor von Holst. "
                  "The book's Figure 22-1 is a scan of a page of the same print, a hard case for OCR. "
                  "In this study three clean lines of the novel's chapter V were read as one str of 83 characters in which one capital I was read as a vertical bar."),
        "lesson": "Even clean text can come back with a mistake",
        "source": ("Wikipedia, 'Frankenstein' (anonymous first edition 1818; revised edition 1831), read 2026-10-13; Wikimedia Commons, 'Frontispiece to Frankenstein 1831.jpg' (Theodor von Holst, public domain); "
                   "this study's leaves FrankensteinOutput and LineBreaks."),
    },
]

LINK_STATUS = {'Goldberg1931': 200, 'Kurzweil1976': 200, 'Tesseract1985': 200, 'Recaptcha2009': 200, 'Frankenstein1831': 200}


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
    for sid, year in (("Goldberg1931", "1931"), ("Kurzweil1976", "1976"), ("Tesseract1985", "1985"), ("Recaptcha2009", "2009"), ("Frankenstein1831", "1831")):
        if year not in by[sid]["story"] and year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
        if year not in by[sid]["when"] and not (sid == "Kurzweil1976" and "1976" in by[sid]["story"]):
            bad.append("%s: year %s not in when" % (sid, year))
    return bad


def ask_links():
    import requests
    out = {}
    for x in STORIES:
        try:
            r = requests.get(x["link"], timeout=60, headers={"User-Agent": "SEN0414-course-materials/1.0 (course materials; contact via GitHub altunelyusuf)"}, stream=True)
            out[x["id"]] = r.status_code
            r.close()
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
