#!/usr/bin/env python3
"""Fetches the six story pictures of the chapter 18 deck 2.0.0 and writes their licence records.
Every picture is found through Openverse (api.openverse.org), which indexes Wikimedia Commons and Flickr under Creative Commons licences; the search query, the exact title, the creator
and, where several pictures share a title, the Openverse id are asserted, so that a different picture cannot be taken by mistake. The file is fetched from the source URL with a patient retry
(Wikimedia answers HTTP 429 now and then); when Wikimedia keeps refusing, the 960 px thumbnail that Wikimedia itself serves of the same file is read and the record says so. Stores
03-materials/ch18/assets/image_*.jpg (at most 1600 px on the long side) and writes 03-materials/ch18/assets/story_images_v2_0_0.json with, for each file, the file page, the source URL
actually read, the SHA-256 of the bytes read, the licence, the creator, a description that names only what the picture really shows, and the credit line the slide prints.
The bytes read are cached in the folder named by the environment variable STORY_CACHE (default: none) so that a second run reads no web page again; the cache is the caller's scratch folder.
Usage: [STORY_CACHE=/some/scratch/folder] python3 story_images_fetch_v2_0_0.py"""
__version__ = "2.0.0"
import datetime, hashlib, io, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "03-materials", "ch18", "assets"))
CACHE = os.environ.get("STORY_CACHE")
UA = {"User-Agent": "SEN0414-course/1.0 (altunel.yusuf@gmail.com; course materials, IKU)"}

# file name, search query, exact title, creator (start), licence, version, Openverse id or None, description (what the picture shows), slide credit, note
TARGETS = [
    ("image_ibm.jpg", "IBM System/360 mainframe", "IBM System/360 Mainframe", "Erik Pitti", "by", "2.0", "4a22345e-5f06-4cf1-86f9-bb5577496d21",
     "An IBM System/360 console with rows of switches and a sign reading IBM System/360, and tape drives with blue and red reels beside it, in a museum hall (title of the Flickr photograph: IBM System/360 Mainframe)",
     "An IBM System/360 console and tape drives: the machine family, not the compiler. Photo: Erik Pitti, CC BY 2.0, Flickr.",
     "Disclosure: the story is about the Fortran compiler of IBM OS/360 in 1972; the picture shows a System/360 machine, the family that OS/360 ran on, not the compiler. No free picture of the compiler was found."),
    ("image_ietf.jpg", "IETF meeting", "IETF Meeting", "Christopher Blizzard", "by-sa", "2.0", "d3d91d4d-e30f-4984-9d5c-647cb23d0c25",
     "People in a meeting hall: two men seated at a table with laptops, a man in an orange shirt standing with a hand at his ear, and more people standing in the background (title of the Flickr photograph: IETF Meeting)",
     "A meeting hall titled 'IETF Meeting' by its photographer: not the author of the RFC. Photo: Christopher Blizzard, CC BY-SA 2.0, Flickr.",
     "Disclosure: the story is about RFC 4180 and its author Yakov Shafranovich; the picture shows a meeting of the body behind the RFC series (by its title), not the author. No free picture of him was found."),
    ("image_crockford.jpg", "Douglas Crockford", "Douglas Crockford", "Franco Folini", "by-sa", "2.0", None,
     "@CROCKFORD@",
     "Douglas Crockford, as titled on Wikimedia Commons. Photo: Franco Folini, CC BY-SA 2.0.",
     "A real portrait of the person the story is about."),
    ("image_bosak.jpg", "Jon Bosak", "Jon Bosak", "Tim Bray", "by-sa", "3.0", None,
     "@BOSAK@",
     "Jon Bosak, as titled on Wikimedia Commons. Photo: Tim Bray, CC BY-SA 3.0.",
     "A real portrait of the person the story is about."),
    ("image_guido.jpg", "Guido van Rossum", "Guido van Rossum OSCON 2006", "Doc Searls", "by-sa", "2.0", None,
     "@GUIDO@",
     "Guido van Rossum, Python's creator, at OSCON 2006: not Lundh or Ippolito. Photo: Doc Searls, CC BY-SA 2.0.",
     "Disclosure: the story is about Fredrik Lundh (ElementTree) and Bob Ippolito (json); the picture shows Guido van Rossum, the creator of Python, in the year of Python 2.5. No free picture of Lundh or Ippolito was found."),
    ("image_servers.jpg", "data center server racks", "Virginia Tech - data center", "cbowns", "by-sa", "2.0", "81351986-cac1-4ca4-bdaf-2e22ff7ca3e2",
     "A long aisle between tall black server racks in a data centre, lit from above (title of the Flickr photograph: Virginia Tech - data center)",
     "Server racks in a data centre: not an attack. Photo: cbowns, CC BY-SA 2.0, Flickr.",
     "Disclosure: the story is about an XML file that exhausts a parser's memory; the picture shows the kind of machine memory belongs to, not an attack."),
]
DESC = {}  # filled from story_images_desc_v2_0_0.json when it exists next to this file (descriptions written after the pictures were looked at)
_dp = os.path.join(HERE, "story_images_desc_v2_0_0.json")
if os.path.exists(_dp):
    DESC = json.load(open(_dp, encoding="utf-8"))


def get(url, tries=5, wait=20):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 424, 503) or k == tries - 1:
                raise
            print("  HTTP %d - waiting %d s" % (e.code, wait * (k + 1)), flush=True)
            time.sleep(wait * (k + 1))


def find(query, title, creator, lic, ver, oid):
    d = json.loads(get("https://api.openverse.org/v1/images/?q=%s&page_size=20" % urllib.parse.quote(query), 4, 15))
    for r in d["results"]:
        if r["title"] == title and r["creator"].startswith(creator) and r["license"] == lic and r["license_version"] == ver and (oid is None or r["id"] == oid):
            return r
    raise SystemExit("REFUSED: no Openverse record with title %r, creator %r and licence %s %s for the query %r" % (title, creator, lic, ver, query))


def main():
    rec = {}
    for fn, query, title, creator, lic, ver, oid, desc, credit, lnote in TARGETS:
        if desc.startswith("@"):
            if desc not in DESC:
                print("WARN: no description yet for %s (story_images_desc_v2_0_0.json): look at the picture and write it before the record is final" % fn)
                desc = "(description pending)"
            else:
                desc = DESC[desc]
        cp = os.path.join(CACHE, fn + ".src.json") if CACHE else None
        if cp and os.path.exists(cp):
            c = json.load(open(cp))
            hit, url, note = c["hit"], c["url"], c["note"]
            raw = open(cp[:-5] + ".bin", "rb").read()
        else:
            hit = find(query, title, creator, lic, ver, oid)
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
                raw = get(url, 8, 30)
                note = " The source file answered HTTP %d, so the 960 px thumbnail that Wikimedia serves of the same file was read." % e.code
            if cp:
                os.makedirs(CACHE, exist_ok=True)
                json.dump({"hit": hit, "url": url, "note": note}, open(cp, "w"))
                open(cp[:-5] + ".bin", "wb").write(raw)
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
