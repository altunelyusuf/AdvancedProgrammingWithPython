#!/usr/bin/env python3
"""Fetches the story pictures of the chapter 19 deck 2.0.0 and writes 03-materials/ch19/assets/story_images_v1_0_0.json (one record for each picture).
Five pictures are read from Wikimedia Commons by their exact file titles (the file page, licence, creator and credit are read from the Commons API and the title and licence are
asserted, so that a different file cannot be taken by mistake); the thumbnail that Wikimedia serves is read, because full-size downloads answer HTTP 429. The sixth, for the year 2038 story,
no free picture was found, so it is DRAWN here from the printed result of the chapter's first example (own work, no photograph, and the record says so).
No photograph of a person is used. Usage: python3 story_images_fetch_v1_0_0.py"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "03-materials", "ch19", "assets"))
UA = {"User-Agent": "SEN0414-course/1.0 (course materials, IKU; github.com/altunelyusuf/AdvancedProgrammingWithPython)"}
TARGETS = [
    ("image_pdp11.jpg", "File:DEC PDP-11 20 computer at the Computer History Museum.jpg", "CC BY 2.0",
     "A DEC PDP-11/20 minicomputer with its front panel of switches and lights, in the Computer History Museum (Commons file description)",
     "A DEC PDP-11/20 in the Computer History Museum: the machine family Unix first ran on. Photo: Don DeBold, CC BY 2.0, Wikimedia Commons.",
     "Disclosure: the story is about the manuals of Unix; the picture shows a PDP-11/20, a machine of the family Unix ran on, not a page of the manual."),
    ("image_oct1582.jpg", "File:Koledar 1582 oktober.png", "CC BY-SA 4.0",
     "A calendar page of October 1582 in which the days after the 4th jump to the 15th (Commons file description: Koledar 1582 oktober)",
     "The calendar of October 1582: 4 October is followed by 15 October. Image: Andrej Jakobčič, CC BY-SA 4.0, Wikimedia Commons.",
     "A real picture of the thing the story is about; the labels are Slovenian (koledar means calendar)."),
    ("image_clock.jpg", "File:Atomic Clock041.jpg", "Public domain",
     "Cesium, the heart of the National Bureau of Standards' atomic clock, in a capsule (Commons file description)",
     "Cesium, the heart of an atomic clock, in its capsule. Photo: National Institute of Standards and Technology, public domain, Wikimedia Commons.",
     "Disclosure: the story is about leap seconds; the picture shows the cesium of an atomic clock, which keeps the second, not a leap second."),
    ("image_tzmap.jpg", "File:Standard time zones of the world (2012).svg", "CC BY-SA 3.0",
     "A world map coloured in the standard time zones, 2012 (Commons file description: Timezones in the world, 2012)",
     "Time zones of the world, 2012. Map: Poulpy, CC BY-SA 3.0, Wikimedia Commons.",
     "Disclosure: the story is about the tz database; the map shows the zones that the database describes the rules of, not the database."),
    ("image_vax.jpg", "File:LCM - DEC VAX 11-780-5 - 01.jpg", "CC BY-SA 3.0",
     "A DEC VAX 11/780-5 computer cabinet at the Living Computer Museum, Seattle (Commons file description)",
     "A DEC VAX 11/780 at the Living Computer Museum, Seattle. Photo: Joe Mabel, CC BY-SA 3.0, Wikimedia Commons.",
     "Disclosure: the story is about the time-shared VAX at Purdue; the picture shows a VAX 11/780 in a museum, not the Purdue machine."),
]


def get(url, tries=7, wait=20):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read()
        except Exception as e:
            code = getattr(e, "code", None)
            if k == tries - 1 or (code is not None and code != 429):
                raise
            print("  retry after", wait * (k + 1), "s:", e, flush=True)
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


def drawn_2038():
    """The year-2038 picture, drawn from the first example's printed result (own work)."""
    from datetime import datetime, UTC
    last = datetime.fromtimestamp(2 ** 31 - 1, UTC).strftime("%Y-%m-%d %H:%M:%S")
    wrap = datetime.fromtimestamp(-2 ** 31, UTC).strftime("%Y-%m-%d %H:%M:%S")
    W, H = 960, 1050
    im = Image.new("RGB", (W, H), (251, 248, 242))
    d = ImageDraw.Draw(im)
    def font(sz, bold=False):
        for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""), "/usr/share/fonts/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")):
            if os.path.exists(p):
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()
    ink, teal, red, grey = (31, 41, 51), (14, 124, 134), (180, 60, 50), (91, 103, 115)
    d.text((W // 2, 60), "A signed 32-bit counter", font=font(44, True), fill=ink, anchor="mm")
    d.text((W // 2, 115), "seconds since 1 January 1970 UTC", font=font(30), fill=grey, anchor="mm")
    d.rounded_rectangle((60, 190, W - 60, 420), 24, fill=(215, 238, 240), outline=teal, width=4)
    d.text((W // 2, 245), "last value that fits", font=font(30), fill=grey, anchor="mm")
    d.text((W // 2, 300), "2**31 - 1 = 2147483647", font=font(40, True), fill=ink, anchor="mm")
    d.text((W // 2, 370), last + " UTC", font=font(36), fill=teal, anchor="mm")
    d.polygon([(W // 2 - 40, 450), (W // 2 + 40, 450), (W // 2, 520)], fill=red)
    d.text((W // 2, 570), "one more second", font=font(32, True), fill=red, anchor="mm")
    d.rounded_rectangle((60, 620, W - 60, 850), 24, fill=(251, 232, 228), outline=red, width=4)
    d.text((W // 2, 675), "the counter wraps to", font=font(30), fill=grey, anchor="mm")
    d.text((W // 2, 730), "-2**31 = -2147483648", font=font(40, True), fill=ink, anchor="mm")
    d.text((W // 2, 800), wrap + " UTC", font=font(36), fill=red, anchor="mm")
    d.text((W // 2, 940), "Drawn for this deck from the result of the first", font=font(26), fill=grey, anchor="mm")
    d.text((W // 2, 980), "code example. Not a photograph.", font=font(26), fill=grey, anchor="mm")
    return im


def main():
    jf = os.path.join(ASSETS, "story_images_v1_0_0.json")
    rec = json.load(open(jf, encoding="utf-8")) if os.path.exists(jf) else {}
    failed = []
    for fn, title, lic, desc, credit, lnote in TARGETS:
        if fn in rec and os.path.exists(os.path.join(ASSETS, fn)):
            print(fn, "already fetched; kept", flush=True)
            continue
        try:
            t, ii = info(title)
            m = ii["extmetadata"]
            if t != title or m["LicenseShortName"]["value"] != lic:
                raise SystemExit("REFUSED: %r has title %r licence %r, expected %r %r" % (fn, t, m["LicenseShortName"]["value"], title, lic))
            url = ii["url"].split("?")[0]
            time.sleep(4)
            path = url.split("/wikipedia/commons/")[1]
            name = path.rsplit("/", 1)[1]
            svg = url.endswith(".svg")
            turl = "https://upload.wikimedia.org/wikipedia/commons/thumb/%s/960px-%s%s" % (path, name, ".png" if svg else "")
            raw = get(turl, 6, 30)
        except urllib.error.HTTPError as e:
            print(fn, "NOT fetched:", e, flush=True)
            failed.append(fn)
            continue
        im = Image.open(io.BytesIO(raw))
        if svg or im.mode in ("RGBA", "LA", "P"):
            png = im.convert("RGBA")
            im = Image.new("RGB", png.size, "white")
            im.paste(png, mask=png.split()[3])
        else:
            im = im.convert("RGB")
        note = " Read as the 960 px thumbnail that Wikimedia serves of the same file%s (full-size downloads answer HTTP 429)." % (" (a PNG rendering of the SVG, flattened on white)" if svg else "")
        orig = (ii["width"], ii["height"])
        im.save(os.path.join(ASSETS, fn), "JPEG", quality=90)
        rec[fn] = {"found_by": "Wikimedia Commons, exact file title %r" % title, "file_page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                   "source_url": turl, "retrieved": datetime.date.today().isoformat(), "sha256_of_source_file": hashlib.sha256(raw).hexdigest(),
                   "LicenseShortName": lic, "LicenseUrl": plain(m.get("LicenseUrl", {}).get("value")) or "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                   "Artist": plain(m.get("Artist", {}).get("value")), "Credit": plain(m.get("Credit", {}).get("value")),
                   "ImageDescription": desc, "licence_note": lnote + " Original size %dx%d px." % orig + note, "SlideCredit": credit,
                   "stored_size_px": list(im.size), "resized_to_at_most_px": 1600}
        json.dump(rec, open(jf, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(fn, im.size, "|", lic, "|", rec[fn]["Artist"][:40], flush=True)
        time.sleep(6)
    im = drawn_2038()
    im.save(os.path.join(ASSETS, "image_y2038.jpg"), "JPEG", quality=92)
    rec["image_y2038.jpg"] = {"found_by": "no free picture found; drawn by the build script", "file_page": None, "source_url": None, "retrieved": datetime.date.today().isoformat(),
                              "sha256_of_source_file": None, "LicenseShortName": "own work (drawn for this deck)", "LicenseUrl": None, "Artist": "Yusuf Altunel's course build (this script)", "Credit": "",
                              "ImageDescription": "A drawn diagram of a signed 32-bit counter: the last second that fits, 2038-01-19 03:14:07 UTC, and the value it wraps to, 1901-12-13 20:45:52 UTC (the values are those printed by the chapter's first example)",
                              "licence_note": "Disclosure: no free photograph or diagram of the problem was found with a licence read, so the picture is drawn from the example's own numbers; it is not a photograph.",
                              "SlideCredit": "Drawn for this deck from the result of the first example; not a photograph.", "stored_size_px": list(im.size), "resized_to_at_most_px": 1600}
    json.dump(rec, open(jf, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote story_images_v1_0_0.json:", len(rec), "records;", "NOT fetched: %s" % failed if failed else "all fetched")


if __name__ == "__main__":
    main()
