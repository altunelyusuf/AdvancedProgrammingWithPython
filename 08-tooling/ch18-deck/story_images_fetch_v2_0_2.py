#!/usr/bin/env python3
"""Fetches the NEW story picture of the chapter 18 deck 2.0.2 and writes story_images_v2_0_2.json (the records of v2_0_0 unchanged, plus the new one).
New story (owner-approved draft of 2026-11-11, 03-materials/ch18/DRAFT_ch18_v1_0_1.md): Jesse James Garrett names Ajax, 18 February 2005; it replaces the JSON-origin story already told in chapters 7 and 10.
Each picture is read from Wikimedia Commons by its exact file title; the file page, licence, creator and credit are read from the Commons API (imageinfo, extmetadata) and the title and licence are asserted,
so that a different file cannot be taken by mistake. Patient retry on HTTP 429. The thumbnail Wikimedia serves is read (full-size downloads answer HTTP 429); an SVG is read as its PNG rendering, flattened on white.
Usage: python3 story_images_fetch_v2_1_0.py"""
__version__ = "2.0.2"
import datetime, hashlib, io, json, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "03-materials", "ch18", "assets"))
UA = {"User-Agent": "SEN0414-course/1.0 (course materials, IKU; github.com/altunelyusuf/AdvancedProgrammingWithPython)"}
# file name, exact Commons title, licence asserted, description (what the picture shows), slide credit, note
TARGETS = [
    ("image_garrett.jpg", "File:Jesse-James-Garrett Web2.0-Kongress 2007.jpg", "CC BY 2.5",
     "A portrait photograph of Jesse James Garrett, who named Ajax, taken at the Web 2.0 Kongress in Mainz, Germany, on 25 April 2007 (Commons file description)",
     "Jesse James Garrett, 25 April 2007. Photo: Tim 'Avatar' Bartel, CC BY 2.5, Wikimedia Commons.",
     "A real portrait of the person the story is about, taken two years after the essay of 18 February 2005."),
]


def get(url, tries=6, wait=20):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            print("  429 - waiting", wait * (k + 1), "s", flush=True)
            time.sleep(wait * (k + 1))


def info(title):
    u = "https://commons.wikimedia.org/w/api.php?action=query&titles=%s&prop=imageinfo&iiprop=extmetadata|url|size&format=json" % urllib.parse.quote(title)
    d = json.loads(get(u))
    p = list(d["query"]["pages"].values())[0]
    if "imageinfo" not in p:
        raise SystemExit("REFUSED: no Commons file titled %r" % title)
    return p["title"], p["imageinfo"][0]


def plain(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h or "")).strip()


def main():
    old = json.load(open(os.path.join(ASSETS, "story_images_v2_0_0.json"), encoding="utf-8"))
    rec = dict(old)
    for fn, title, lic, desc, credit, lnote in TARGETS:
        t, ii = info(title)
        m = ii["extmetadata"]
        if t != title or m["LicenseShortName"]["value"] != lic:
            raise SystemExit("REFUSED: %r has title %r licence %r, expected %r %r" % (fn, t, m["LicenseShortName"]["value"], title, lic))
        url = ii["url"].split("?")[0]
        time.sleep(4)
        # Wikimedia refuses full-size downloads from this machine (HTTP 429 asking for thumbnail sizes); the thumbnail it serves of the same file is read, and the record says so
        path = url.split("/wikipedia/commons/")[1]; name = path.rsplit("/", 1)[1]
        if url.endswith(".svg"):
            turl = "https://upload.wikimedia.org/wikipedia/commons/thumb/%s/500px-%s.png" % (path, name)
        else:
            turl = "https://upload.wikimedia.org/wikipedia/commons/thumb/%s/960px-%s" % (path, name)
        raw = get(turl, 6, 30)
        im = Image.open(io.BytesIO(raw)).convert("RGB") if not url.endswith(".svg") else None
        if im is None:
            png = Image.open(io.BytesIO(raw)).convert("RGBA"); im = Image.new("RGB", png.size, "white"); im.paste(png, mask=png.split()[3])
        note = " Read as the %s that Wikimedia serves of the same file (full-size downloads answered HTTP 429)." % ("500 px PNG rendering of the SVG, flattened on white" if url.endswith(".svg") else "960 px thumbnail")
        url = turl
        orig = (ii["width"], ii["height"])
        if max(im.size) > 1600:
            k = 1600 / float(max(im.size)); im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        im.save(os.path.join(ASSETS, fn), "JPEG", quality=90)
        rec[fn] = {"found_by": "Wikimedia Commons, exact file title %r" % title, "file_page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                   "source_url": url, "retrieved": datetime.date.today().isoformat(), "sha256_of_source_file": hashlib.sha256(raw).hexdigest(),
                   "LicenseShortName": lic, "LicenseUrl": plain(m.get("LicenseUrl", {}).get("value")) or "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                   "Artist": plain(m.get("Artist", {}).get("value")), "Credit": plain(m.get("Credit", {}).get("value")),
                   "ImageDescription": desc, "licence_note": lnote + " Original size %dx%d px." % orig + note, "SlideCredit": credit,
                   "stored_size_px": list(im.size), "resized_to_at_most_px": 1600}
        print(fn, im.size, "|", lic, "|", rec[fn]["Artist"][:40], flush=True)
        time.sleep(4)
    json.dump(rec, open(os.path.join(ASSETS, "story_images_v2_0_2.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote story_images_v2_0_2.json:", len(rec), "records")


if __name__ == "__main__":
    main()
