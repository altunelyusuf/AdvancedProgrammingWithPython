#!/usr/bin/env python3
"""Fetches the story pictures of the chapter 20 deck 2.0.0 and writes 03-materials/ch20/assets/story_images_v1_0_0.json (one record for each picture).
Five pictures are read from Wikimedia Commons by their exact file titles (the file page, licence, creator and credit are read from the Commons API and the title and licence are
asserted, so that a different file cannot be taken by mistake); the thumbnail that Wikimedia serves is read, because full-size downloads answer HTTP 429. The sixth, for the AT&T story,
no free picture was found, so it is DRAWN here from the DNS answers that the chapter research recorded (own work, no photograph, and the record says so).
No photograph of a person is used. Usage: python3 story_images_fetch_v1_0_0.py"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "03-materials", "ch20", "assets"))
UA = {"User-Agent": "SEN0414-course/1.0 (course materials, IKU; github.com/altunelyusuf/AdvancedProgrammingWithPython)"}
TARGETS = [
    ("image_imap.jpg", "File:Xerox Alto I, 1973, Computer History Museum.jpg", "CC BY-SA 4.0",
     "A Xerox Alto I of 1973 in the Computer History Museum (Commons file description)",
     "A Xerox Alto I (1973) in the Computer History Museum: a Xerox workstation of the period. Photo: The wub, CC BY-SA 4.0, Wikimedia Commons.",
     "Disclosure: the story says IMAP's first client ran on a Xerox Lisp machine; the picture shows a Xerox Alto, an earlier Xerox workstation, not the Lisp machine."),
    ("image_arpanet.jpg", "File:ARPA Network, Logical Map, September 1973.jpg", "Public domain",
     "ARPA Network, Logical Map, September 1973, with satellite links to Hawaii and London (Commons file description)",
     "The ARPA Network, logical map, September 1973. Bolt Beranek and Newman Inc., public domain, Wikimedia Commons.",
     "A real picture of the network of the story, two years after the first network mail; the map is of 1973, the mail of 1971."),
    ("image_smtp.jpg", "File:SMTP-transfer-model.svg", "CC BY-SA 3.0",
     "SMTP transfer model; blue arrows can be implemented by SMTP variations (Commons file description)",
     "The SMTP transfer model. Diagram: Ale2006-from-en, CC BY-SA 3.0, Wikimedia Commons.",
     "Disclosure: the story is about RFC 821; the picture is a diagram of the transfer model that SMTP describes, not a page of the RFC."),
    ("image_dec.jpg", "File:LCM - DECSYSTEM-20 KL-10 - 01.jpg", "CC BY-SA 3.0",
     "A DEC DECsystem-20 KL-10 computer at the Living Computer Museum, Seattle (Commons file description)",
     "A DEC DECsystem-20 KL-10 at the Living Computer Museum, Seattle. Photo: Joe Mabel, CC BY-SA 3.0, Wikimedia Commons.",
     "Disclosure: the story is about an advertisement of the Digital Equipment Corporation; the picture shows a DEC computer of the ARPANET era, not the machine that sent the mail."),
    ("image_sms.jpg", "File:SMS-Message-On-Phone.png", "CC BY-SA 4.0",
     "SMS messages on a mobile phone (Commons file description)",
     "Text messages on a mobile phone. Image: gmcgcc, CC BY-SA 4.0, Wikimedia Commons.",
     "Disclosure: the story is about the first text of 1992; the picture shows a modern phone screen with text messages."),
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


def drawn_att():
    """The AT&T picture, drawn from the DNS answers that the chapter research recorded (own work)."""
    W, H = 960, 1050
    im = Image.new("RGB", (W, H), (251, 248, 242))
    d = ImageDraw.Draw(im)
    def font(sz, bold=False):
        for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""), "/usr/share/fonts/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")):
            if os.path.exists(p):
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()
    ink, teal, red, amber, grey = (31, 41, 51), (14, 124, 134), (180, 60, 50), (176, 120, 20), (91, 103, 115)
    d.text((W // 2, 60), "Mail servers of 18 gateway domains", font=font(40, True), fill=ink, anchor="mm")
    d.text((W // 2, 112), "DNS answers recorded by the chapter research", font=font(28), fill=grey, anchor="mm")
    rows = [("12", "have mail servers", teal, 12, "vtext.com, tmomail.net, ..."),
            ("3", "answer: none", red, 3, "txt.att.net, mms.att.net, sms.cricketwireless.net"),
            ("2", "no such name", red, 2, "messaging.sprintpcs.com, pm.sprint.com"),
            ("1", "lookup failed", amber, 1, "sms.myboostmobile.com")]
    y = 190
    for num, label, col, n, ex in rows:
        d.text((60, y + 40), num, font=font(54, True), fill=col, anchor="lm")
        d.rounded_rectangle((150, y + 10, 150 + n * 62, y + 70), 14, fill=col)
        d.text((150, y + 100), label + ": " + ex, font=font(23), fill=ink, anchor="lm")
        y += 170
    d.text((W // 2, 900), "AT&T: email-to-text ended 17 June 2025", font=font(32, True), fill=ink, anchor="mm")
    d.text((W // 2, 960), "A missing mail server is a symptom, not proof.", font=font(26), fill=grey, anchor="mm")
    d.text((W // 2, 1005), "Drawn for this deck. Not a photograph.", font=font(24), fill=grey, anchor="mm")
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
    im = drawn_att()
    im.save(os.path.join(ASSETS, "image_att.jpg"), "JPEG", quality=92)
    rec["image_att.jpg"] = {"found_by": "no free picture found; drawn by the build script", "file_page": None, "source_url": None, "retrieved": datetime.date.today().isoformat(),
                            "sha256_of_source_file": None, "LicenseShortName": "own work (drawn for this deck)", "LicenseUrl": None, "Artist": "Yusuf Altunel's course build (this script)", "Credit": "",
                            "ImageDescription": "A drawn diagram of the DNS answers for the mail servers of the 18 gateway domains of Table 20-1: 12 have mail servers, 3 answer none, 2 no such name, 1 a failed lookup (the counts are those recorded by the chapter research).",
                            "licence_note": "Disclosure: no free photograph or diagram of the AT&T shutdown was found with a licence read, so the picture is drawn from the research's own numbers; it is not a photograph.",
                            "SlideCredit": "Drawn for this deck from the DNS answers of the chapter research; not a photograph.", "stored_size_px": list(im.size), "resized_to_at_most_px": 1600}
    json.dump(rec, open(jf, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote story_images_v1_0_0.json:", len(rec), "records;", "NOT fetched: %s" % failed if failed else "all fetched")


if __name__ == "__main__":
    main()
