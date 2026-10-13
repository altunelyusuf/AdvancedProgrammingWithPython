"""SEN0414 chapter 21 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for
making graphs and manipulating images, written fresh for this chapter from Wikipedia pages opened on 2026-10-13 (the HTTP status each
link answered to a plain GET on that day is in LINK_STATUS, and `python3 sen0414_ch21_stories_v1_0_0.py links` asks again):

* Kirsch1957 - Russell A. Kirsch's group at the National Bureau of Standards scanned a picture of his three-month-old son Walden in 1957: 176 x 176 = 30,976 pixels, one bit each.
* Alpha1970s - the alpha channel was introduced by Alvy Ray Smith and Ed Catmull in the late 1970s; Porter and Duff's 1984 paper introduced premultiplied alpha.
* Png1996 - the announcement on 28 December 1994 that GIF implementations would owe royalties to Unisys for LZW led to PNG, first released 1 October 1996.
* Jpeg1992 - the Joint Photographic Experts Group created the standard in 1992 on the discrete cosine transform that Nasir Ahmed first proposed in 1972.
* Matplotlib2003 - Matplotlib, by John D. Hunter, released in 2003, named for MATLAB, plot and library.
* Pil1995 - Fredrik Lundh's Python Imaging Library of 1995, discontinued in 2011, and the Pillow fork that replaced it.

Photograph: see ch21-page/stories_img_v1_0_0.json. The single request to Wikimedia Commons answered HTTP 429, so no photograph is used and nothing is claimed about licences.
Every sentence that says "In this study" was run on 2026-10-13 in /home/claude/venv314_ch21_latest (Python 3.14.6, Pillow 12.3.0, Matplotlib 3.11.2).
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "Kirsch1957",
        "title": "The first scanned photograph was 176 by 176 pixels of a baby",
        "when": "1957",
        "who": "Russell A. Kirsch, an engineer whose group at the National Bureau of Standards developed a drum scanner",
        "where": "The National Bureau of Standards (now NIST), where Kirsch had joined the team that ran the computer SEAC in 1951",
        "link": "https://en.wikipedia.org/wiki/Russell_A._Kirsch",
        "concepts": ["ImageModes", "NewImage"],
        "story": ("Wikipedia's article on Russell A. Kirsch says that in 1957 his group developed a drum scanner, and that one of the first photographs scanned was a picture of his three-month-old son, Walden. "
                  "It was captured as just 30,976 pixels, a 176 x 176 array, in an area of 5 cm x 5 cm. "
                  "The bit depth was one bit per pixel, black or white with no shades of gray. "
                  "In this study Image.new('1', (176, 176)) made a picture of mode 1 with 30,976 pixels, each holding 0 or 1."),
        "lesson": "Every picture you open began as a grid of numbers",
        "source": ("Wikipedia, 'Russell A. Kirsch' (the 1957 scan of his three-month-old son Walden; 30,976 pixels, a 176 x 176 array, one bit per pixel), read 2026-10-13; "
                   "this study's leaves ImageModes and NewImage."),
    },
    {
        "id": "Alpha1970s",
        "title": "The alpha channel came from a computer graphics lab in the late 1970s",
        "when": "The late 1970s, with a paper in 1984",
        "who": "Alvy Ray Smith and Ed Catmull, and later Thomas Porter and Tom Duff",
        "where": "The New York Institute of Technology Computer Graphics Lab",
        "link": "https://en.wikipedia.org/wiki/Alpha_compositing",
        "concepts": ["PasteMask", "RgbaTuple"],
        "story": ("Wikipedia's article on alpha compositing says the concept of an alpha channel was introduced by Alvy Ray Smith and Ed Catmull in the late 1970s at the New York Institute of Technology Computer Graphics Lab. "
                  "It adds that a 1984 paper by Thomas Porter and Tom Duff introduced premultiplied alpha. "
                  "The fourth number of an RGBA tuple in chapter 21 is that alpha, from 0 for clear to 255 for solid. "
                  "In this study a blue square with alpha 128 pasted with itself as the mask over a red one gave the pixel (127, 0, 128)."),
        "lesson": "Alpha is how much of the top picture you see",
        "source": ("Wikipedia, 'Alpha compositing' (alpha channel introduced by Smith and Catmull in the late 1970s; Porter and Duff in 1984), read 2026-10-13; "
                   "this study's leaves PasteMask and RgbaTuple."),
    },
    {
        "id": "Png1996",
        "title": "A patent announcement on 28 December 1994 led to PNG",
        "when": "28 December 1994 to 1 October 1996",
        "who": "Unisys, which held the LZW patent, and Thomas Boutell, who posted a plan for a free alternative on Usenet",
        "where": "The Usenet newsgroup comp.graphics, and then the PNG Development Group",
        "link": "https://en.wikipedia.org/wiki/PNG",
        "concepts": ["SaveFormats", "PasteMask"],
        "story": ("Wikipedia's article on PNG says the motivation for creating the format was the announcement on 28 December 1994 that implementations of GIF would have to pay royalties to Unisys for their patent of the LZW compression algorithm. "
                  "Thomas Boutell posted a thread on comp.graphics on 4 January 1995 in which he devised a plan for a free alternative. "
                  "The article gives the initial release of PNG as 1 October 1996. "
                  "In this study img.save(buffer, 'PNG') and a reopen gave back the format PNG, and the format keeps the alpha channel that chapter 21 uses for its logo."),
        "lesson": "A format can be born from a licence dispute",
        "source": ("Wikipedia, 'PNG' (announcement on 28 December 1994; Boutell's posting on 4 January 1995; initial release 1 October 1996), read 2026-10-13; "
                   "this study's leaves SaveFormats and PasteMask."),
    },
    {
        "id": "Jpeg1992",
        "title": "JPEG stands on a transform proposed twenty years earlier",
        "when": "1972 and 1992",
        "who": "Nasir Ahmed, who first proposed the discrete cosine transform for image compression, and the Joint Photographic Experts Group",
        "where": "The standard ISO/IEC 10918 and ITU-T T.81",
        "link": "https://en.wikipedia.org/wiki/JPEG",
        "concepts": ["SaveFormats", "ImageFilename"],
        "story": ("Wikipedia's article on JPEG says the Joint Photographic Experts Group created the standard in 1992 and that its lossy compression is based on the discrete cosine transform. "
                  "That transform was first proposed by Nasir Ahmed as an image compression technique in 1972. "
                  "The article gives the initial release as 18 September 1992. "
                  "In this study img.save(buffer, 'JPEG') and a reopen gave back the format JPEG, the format chapter 21 uses for the photographs of its logo project."),
        "lesson": "JPEG throws detail away to make a small file",
        "source": ("Wikipedia, 'JPEG' (standard created in 1992; discrete cosine transform first proposed by Nasir Ahmed in 1972; initial release 18 September 1992), read 2026-10-13; "
                   "this study's leaves SaveFormats and ImageFilename."),
    },
    {
        "id": "Matplotlib2003",
        "title": "Matplotlib was named for MATLAB, plot and library",
        "when": "2003",
        "who": "John D. Hunter, the original author of Matplotlib",
        "where": "The Python language, with the numerical library NumPy",
        "link": "https://en.wikipedia.org/wiki/Matplotlib",
        "concepts": ["LinePlot", "PyplotState"],
        "story": ("Wikipedia's article on Matplotlib gives John D. Hunter as the original author and 2003 as the release. "
                  "It explains the name as a portmanteau of MATLAB, plot and library, and calls it a plotting library for Python and its numerical extension NumPy. "
                  "The pyplot module of chapter 21 keeps one current figure that each call draws on. "
                  "In this study plt.plot([1, 2, 3]) under Matplotlib 3.11.2 returned a list holding the line it drew."),
        "lesson": "pyplot remembers the current figure so you do not have to",
        "source": ("Wikipedia, 'Matplotlib' (original author John D. Hunter; release 2003; a portmanteau of MATLAB, plot, and library), read 2026-10-13; "
                   "this study's leaves LinePlot and PyplotState."),
    },
    {
        "id": "Pil1995",
        "title": "PIL stopped in 2011 and Pillow carried it on",
        "when": "1995 to 2011",
        "who": "Fredrik Lundh, the original author of the Python Imaging Library, and the developers of the Pillow fork",
        "where": "Secret Labs AB, the library's developer, and then the Pillow project",
        "link": "https://en.wikipedia.org/wiki/Python_Imaging_Library",
        "concepts": ["TextsizeGone", "OpenAndSize"],
        "story": ("Wikipedia's article on the Python Imaging Library gives Fredrik Lundh as the original author and 1995 as the release. "
                  "It says development of the original project, known as PIL, was discontinued in 2011, and that a successor project named Pillow forked the repository and added Python 3.x support. "
                  "Chapter 21 still imports from PIL, because Pillow kept the package name. "
                  "In this study Pillow 12.3.0 imported as PIL and its ImageDraw class had no textsize method any more."),
        "lesson": "Install Pillow, import PIL, and read the release notes",
        "source": ("Wikipedia, 'Python Imaging Library' (Fredrik Lundh; release 1995; development discontinued in 2011; Pillow forked the repository), read 2026-10-13; "
                   "this study's leaves TextsizeGone and OpenAndSize."),
    },
]

LINK_STATUS = {'Kirsch1957': 200, 'Alpha1970s': 200, 'Png1996': 200, 'Jpeg1992': 200, 'Matplotlib2003': 200, 'Pil1995': 200}


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
    for sid, year in (("Kirsch1957", "1957"), ("Alpha1970s", "1970s"), ("Png1996", "1996"), ("Jpeg1992", "1992"), ("Matplotlib2003", "2003"), ("Pil1995", "1995")):
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
