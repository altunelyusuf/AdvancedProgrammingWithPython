#!/usr/bin/env python3
"""Fetches the five story pictures of the chapter 17 deck 2.0.0 and writes their licence records.
Every picture is found through Openverse (api.openverse.org), which indexes Wikimedia Commons and Flickr under Creative Commons licences; the search query, the exact title and the
creator are asserted, so that a different picture cannot be taken by mistake. The file is fetched from the source URL with a patient retry (Wikimedia answers HTTP 429 now and then); when Wikimedia
keeps refusing, the 960 px thumbnail that Wikimedia itself serves of the same file is read and the record says so. Stores 03-materials/ch17/assets/image_*.jpg (at most 1600 px on the long side) and writes
03-materials/ch17/assets/story_images_v2_0_0.json with, for each file, the file page, the source URL actually read, the SHA-256 of the bytes read, the licence, the creator, a description
that names only what the picture really shows, and the credit line the slide prints.
Usage: python3 story_images_fetch_v2_0_0.py"""
__version__ = "2.0.0"
import datetime, hashlib, io, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "03-materials", "ch17", "assets"))
UA = {"User-Agent": "SEN0414-course/1.0 (altunel.yusuf@gmail.com; course materials, IKU)"}

# file name, search query, exact title, creator (start), licence, version, description (what the picture shows), slide credit, note
TARGETS = [
    ("image_warnock.jpg", "John Warnock 2008", "File:John Warnock 2008.jpg", "Marvalous", "by-sa", "3.0",
     "John Warnock, co-founder of Adobe Systems: a black-and-white portrait photograph, shirt and tie, smiling (the file name of Wikimedia Commons gives the year 2008)",
     "John Warnock. Photo: Marvalous, CC BY-SA 3.0, Wikimedia Commons.",
     "A real portrait of the person the story is about."),
    ("image_adobe_hq.jpg", "Adobe Systems headquarters San Jose", "Adobe HQ - 2", "Coolcaesar", "by-sa", "3.0",
     "The headquarters towers of Adobe Systems in San Jose, California (title of the Wikimedia Commons file: Adobe HQ - 2)",
     "Adobe's headquarters towers, San Jose. Photo: Coolcaesar, CC BY-SA 3.0, Wikimedia Commons.",
     "Disclosure: the story is about the standardization of PDF by Adobe and ISO; no free picture of the ISO committee was found, so the slide shows the company that began the format and says so."),
    ("image_pkzip.jpg", "PKZIP floppy found in sock drawer", "PKZIP floppy found in sock drawer", "blakespot", "by", "2.0",
     "A blue 3.5-inch floppy disk labelled PKZIP DOS, PKZIP, PKUNZIP and PKSFX with a copyright line of PKWARE (1989-91), lying among socks in a drawer",
     "A PKZIP floppy disk, label of PKWARE. Photo: blakespot, CC BY 2.0, Flickr.",
     "A real photograph of the product of the company the story is about; it is not a picture of Phil Katz (no free picture of him was found)."),
    ("image_ooxml.jpg", "Microsoft Office 2007 Display", "Microsoft Office 2007 Display", "@netweb", "by-sa", "2.0",
     "Boxes of Microsoft Office 2007 (several editions) on yellow shop shelves, with boxes of Windows Vista beside them",
     "Boxes of Microsoft Office 2007 on a shop shelf. Photo: Stephen Edgar (@netweb), CC BY-SA 2.0, Flickr.",
     "Disclosure: Office 2007 is where the .docx format became Word's default (Wikipedia, Office Open XML); no free picture of the standards committees was found."),
    ("image_pypi.jpg", "Key Solutions Releases on PYPI", "Key Solutions Releases on PYPI", "Vurter", "by-sa", "2.0",
     "A screenshot of the home page of the Python Package Index in a Firefox window, with the text 'There are currently 3121 packages here' and a list of the last 30 updates dated 2007-12-06",
     "The Python Package Index home page, 6 December 2007 (screenshot). Photo: Vurter, CC BY-SA 2.0, Flickr.",
     "A real screenshot of the place the story is about, from 2007, years before the docx release of 2014 the story names."),
]


def get(url, tries=5, wait=20):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            print("  429 - waiting", wait * (k + 1), "s", flush=True)
            time.sleep(wait * (k + 1))


def find(query, title, creator, lic, ver):
    d = json.loads(get("https://api.openverse.org/v1/images/?q=%s&page_size=20" % urllib.parse.quote(query), 4, 15))
    for r in d["results"]:
        if r["title"] == title and r["creator"].startswith(creator) and r["license"] == lic and r["license_version"] == ver:
            return r
    raise SystemExit("REFUSED: no Openverse record with title %r, creator %r and licence %s %s for the query %r" % (title, creator, lic, ver, query))


def main():
    rec = {}
    for fn, query, title, creator, lic, ver, desc, credit, lnote in TARGETS:
        hit = find(query, title, creator, lic, ver)
        url = hit["url"]
        note = ""
        try:
            raw = get(url, 3, 20)
        except urllib.error.HTTPError as e:
            if "upload.wikimedia.org/wikipedia/commons/" not in url:
                raise
            # Wikimedia asks for its thumbnail sizes: the 960 px thumbnail of the same file (a different URL, served from the same file)
            path = url.split("/wikipedia/commons/")[1]
            name = path.rsplit("/", 1)[1]
            url = "https://upload.wikimedia.org/wikipedia/commons/thumb/%s/960px-%s" % (path, name)
            print("  the source answered %d - reading the 960 px thumbnail that Wikimedia serves of the same file" % e.code, flush=True)
            raw = get(url, 6, 30)
            note = " The source file answered HTTP %d, so the 960 px thumbnail that Wikimedia serves of the same file was read." % e.code
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        orig = im.size
        if max(im.size) > 1600:
            k = 1600 / float(max(im.size))
            im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        im.save(os.path.join(ASSETS, fn), "JPEG", quality=90)
        rec[fn] = {"found_by": "Openverse search '%s' (id %s)" % (query, hit["id"]), "file_page": hit["foreign_landing_url"], "source_url": url,
                   "retrieved": datetime.date.today().isoformat(), "sha256_of_source_file": hashlib.sha256(raw).hexdigest(),
                   "LicenseShortName": ("CC %s %s" % (lic.upper(), ver)), "LicenseUrl": hit["license_url"], "Artist": hit["creator"], "Credit": hit["attribution"],
                   "ImageDescription": desc, "licence_note": lnote + " Original size %dx%d px." % orig + note, "SlideCredit": credit,
                   "stored_size_px": list(im.size), "resized_to_at_most_px": 1600}
        print(fn, im.size, "from", url, "| licence", rec[fn]["LicenseShortName"], flush=True)
        time.sleep(3)
    with open(os.path.join(ASSETS, "story_images_v2_0_0.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
    print("wrote story_images_v2_0_0.json:", len(rec), "pictures")


if __name__ == "__main__":
    main()
