"""SEN0414 chapter 11 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Four
stories for Organizing Files, written fresh for this chapter:

* PhilKatzZip1989 - Phil Katz, with Gary Conway, published the .ZIP format in the public domain on 14 February
  1989, after a lawsuit over PKWARE's own earlier ARC-compatible archiver; the module this chapter teaches,
  zipfile, reads and writes exactly the format that press release described.
* GaillyAdlerZlib1995 - Jean-Loup Gailly and Mark Adler released zlib 0.9 on 1 May 1995, a free implementation
  of the DEFLATE algorithm first built for the libpng image library; zipfile.ZIP_DEFLATED, the compression
  method this chapter's own write() calls choose, is zlib running underneath.
* KareTrashIcon1983 - Susan Kare, hired by Apple in 1983, drew the trash can icon for the original Macintosh on
  a 32-by-32 pixel grid with Andy Hertzfeld's own icon editor; the recycle bin this chapter's send2trash module
  moves a file into is the same icon, forty years on.
* DaleyNeumannMultics1965 - R. C. Daley and P. G. Neumann presented Multics's own tree-structured file system
  at the 1965 Fall Joint Computer Conference; Ken Thompson and Dennis Ritchie, who had worked on Multics,
  carried the same tree into Unix, the ancestor of the folder tree os.walk now walks.

Usage: import STORIES; run the file for self-checks. The photographs are named in ch11-page/stories_img_v2_0_0.json (1.0.1).
"""
__version__ = "1.0.1"
# 1.0.1 (new file over 1.0.0, made for the chapter 11 page v9.95.0; 1.0.0 stays as committed): two wording repairs, nothing else changed. (a) The Multics story no
#   longer ends on "fifty-six years before this chapter's own program renamed a single file inside it": that span had no date behind it (1965 plus 56 is 2021, the
#   year of no event of the story); it now ends on the one date it states, 1965. (b) The zlib story's "where" no longer says "the Free Software Foundation's own GNU
#   project, by email" (gzip was a GNU project, zlib 0.9 was not shown to be); it says what the deck's story slide says: over the internet, first built for libpng.
#   The photographs are named in ch11-page/stories_img_v2_0_0.json.

STORIES = [
    {
        "id": "PhilKatzZip1989",
        "title": "The ZIP format was given away free on 14 February 1989",
        "when": "1989-02-14",
        "who": "Phil Katz, with Gary Conway of Infinity Design Concepts",
        "where": "PKWARE, Glendale, Wisconsin",
        "link": "https://en.wikipedia.org/wiki/ZIP_(file_format)",
        "concepts": ["CreateZip"],
        "story": ("Phil Katz had already been sued by Systems Enhancement Associates, which claimed his own "
                   "PKARC archiver copied its ARC format too closely; rather than fight over one more compatible "
                   "format, Katz and Gary Conway of Infinity Design Concepts designed a new one of their own and, "
                   "on 14 February 1989, PKWARE and Infinity Design Concepts issued a joint press release placing "
                   "the .ZIP format in the public domain, free for any program to read or write. Katz's friend "
                   "Robert Mahoney suggested the name itself, 'zip', meaning to move at high speed, to promise a "
                   "program faster than ARC; the first specification, APPNOTE.TXT, shipped that same year inside "
                   "Katz's own PKZIP 0.9. Every zipfile.ZipFile this chapter opens, in mode 'w', 'a' or 'r', reads "
                   "and writes exactly the public-domain structure that one press release described."),
        "lesson": "zipfile reads the format PKWARE gave away free on 14 Feb 1989",
        "source": ("'ZIP (file format)', Wikipedia, en.wikipedia.org/wiki/ZIP_(file_format) (Phil Katz and Gary "
                    "Conway, PKWARE and Infinity Design Concepts, public-domain press release 14 February 1989; "
                    "APPNOTE.TXT first published in PKZIP 0.9, 1989). Photo: Wikimedia Commons."),
    },
    {
        "id": "GaillyAdlerZlib1995",
        "title": "The compression under ZIP_DEFLATED shipped free on 1 May 1995",
        "when": "1995-05-01",
        "who": "Jean-Loup Gailly and Mark Adler",
        "where": "over the internet; first built for the libpng image library",
        "link": "https://en.wikipedia.org/wiki/Zlib",
        "concepts": ["CompressionMethod"],
        "story": ("Jean-Loup Gailly, who had already written the compression half of gzip, and Mark Adler, who "
                   "wrote the matching decompression half, joined their work into a single free library they "
                   "called zlib, built first for Thomas Boutell's own libpng image library rather than for any "
                   "archiver at all. Gailly handled compressing and Adler handled decompressing, and together "
                   "they released zlib 0.9 on 1 May 1995, a clean-room implementation of the DEFLATE algorithm "
                   "that owed nothing to Phil Katz's own patented code, free of charge and free to embed in any "
                   "program at all. Python's own zipfile module links against exactly this library whenever a "
                   "write names compress_type=zipfile.ZIP_DEFLATED, the method this chapter's own backup project "
                   "never actually asks for."),
        "lesson": "ZIP_DEFLATED runs zlib, free since Gailly and Adler's 1995 release",
        "source": ("'Zlib', Wikipedia, en.wikipedia.org/wiki/Zlib (Jean-Loup Gailly and Mark Adler, version 0.9 "
                    "released 1 May 1995, written first for the libpng library). Photo: Wikimedia Commons."),
    },
    {
        "id": "KareTrashIcon1983",
        "title": "The recycle bin's own icon is a 1983 Macintosh drawing",
        "when": "1983",
        "who": "Susan Kare, with Andy Hertzfeld's icon editor",
        "where": "Apple Computer",
        "link": "https://www.smithsonianmag.com/innovation/how-susan-kare-designed-user-friendly-icons-for-first-macintosh-180973286/",
        "concepts": ["RecycleBin"],
        "story": ("Susan Kare joined Apple in 1983 with no formal training in computer graphics at all, and was "
                   "asked to draw the small pictures the first Macintosh would need for its own commands; working "
                   "on a 32-by-32 pixel grid that lead software architect Andy Hertzfeld had proposed, she first "
                   "blocked the squares out by hand on graph paper before redrawing each one electronically in an "
                   "icon editor Hertzfeld built on the Macintosh prototype itself. Among the icons Kare drew that "
                   "year was the trash can, the picture that shipped on the Macintosh's own desktop in 1984 and "
                   "has stood for a reversible delete on a graphical desktop ever since. The third-party "
                   "send2trash module this chapter names moves a file to exactly that bin instead of deleting it "
                   "outright, the one operation of this whole chapter that can still be undone by a user's own "
                   "hand."),
        "lesson": "send2trash's bin is Kare's own 1983 Macintosh trash icon",
        "source": ("Jackie Mansky, 'How Susan Kare Designed User-Friendly Icons for the First Macintosh', "
                    "Smithsonian Magazine, smithsonianmag.com (Kare joined Apple 1983; Macintosh released 1984; "
                    "Andy Hertzfeld's 32x32 grid and icon editor). Photo: Wikimedia Commons."),
    },
    {
        "id": "DaleyNeumannMultics1965",
        "title": "The folder tree os.walk visits is a 1965 Multics design",
        "when": "1965",
        "who": "R.C. Daley and P.G. Neumann",
        "where": "the Fall Joint Computer Conference",
        "link": "https://multicians.org/history.html",
        "concepts": ["WalkTree"],
        "story": ("R.C. Daley of MIT's Project MAC, with P.G. Neumann of Bell Labs, presented 'A General "
                   "Purpose File System for Secondary Storage' at the 1965 Fall Joint Computer Conference, laying "
                   "out Multics's own tree-structured file system, folders holding folders holding files, built "
                   "for a system meant to be shared by many users and administered in pieces at once. Ken "
                   "Thompson and Dennis Ritchie, together with Doug McIlroy and J.F. Ossanna, had all worked on "
                   "Multics at Bell Labs before the project's own slow progress pushed Bell Labs out of it, and "
                   "the small operating system the four built next, Unix, kept the identical tree of folders "
                   "inside folders at its very core. Every folder os.walk visits today, descending from one "
                   "folder into its own subfolders in turn, walks the same shape Daley and Neumann described in "
                   "1965."),
        "lesson": "os.walk descends the folder tree Daley and Neumann designed in 1965",
        "source": ("'Multics History', multicians.org/history.html (R.C. Daley and P.G. Neumann, 'A General "
                    "Purpose File System for Secondary Storage', Fall Joint Computer Conference, 1965; Ken "
                    "Thompson, Dennis Ritchie and colleagues carried the tree into Unix after working on "
                    "Multics). Photo: Wikimedia Commons."),
    },
]


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
    by = {x["id"]: x for x in STORIES}
    if "1989" not in by["PhilKatzZip1989"]["story"] or "1989" not in by["PhilKatzZip1989"]["when"]:
        bad.append("PhilKatzZip1989: date missing from story")
    if "1995" not in by["GaillyAdlerZlib1995"]["story"] or "1995" not in by["GaillyAdlerZlib1995"]["when"]:
        bad.append("GaillyAdlerZlib1995: date missing from story")
    if "1983" not in by["KareTrashIcon1983"]["story"] or "1983" not in by["KareTrashIcon1983"]["when"]:
        bad.append("KareTrashIcon1983: date missing from story")
    if "1965" not in by["DaleyNeumannMultics1965"]["story"] or "1965" not in by["DaleyNeumannMultics1965"]["when"]:
        bad.append("DaleyNeumannMultics1965: date missing from story")
    return bad


if __name__ == "__main__":
    b = run_checks()
    print(len(STORIES), "stories; self-check failures:", len(b))
    for x in b:
        print("  ", x)
