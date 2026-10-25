#!/usr/bin/env python3
"""Fetches the five story pictures of the chapter 15 deck 2.0.0 and records, for each file, where it came from, when, its SHA-256 and its licence.
Wikimedia Commons answers HTTP 429 to its API from this machine, so every picture was FOUND through Openverse (api.openverse.org, which indexes Flickr and
Wikimedia Commons under Creative Commons licences) and the file is read from the address Openverse gives.
  image_rochelle_google.jpg    Openverse 'Jonathan Rochelle - Google' (Flickr, adactio, CC BY 2.0): the co-founder of 2Web Technologies, whose XL2Web became Google Sheets
  image_cook_oauth.jpg         Openverse 'Blaine Cook (Twitter / OAuth): Building the Social Kaleidoscope' (Flickr, steve-uk, CC BY 2.0): Blaine Cook, who began OAuth
  image_bitcoin_paper.png      Openverse 'Bitcoin white paper' (Wikimedia Commons, CC BY 4.0): the first page of the paper the 31 October 2008 message announced
  image_sheets_screen.jpg      Openverse 'autoCrat for Google Sheets' (Flickr, Wesley Fryer, CC BY 2.0): a screenshot of the Google Sheets add-ons page
  image_forms_screen.jpg       Openverse 'Google Form Link' (Flickr, Wesley Fryer, CC BY 2.0): a screenshot of a web page with the Google Forms icon and a link to a form
(Two Wikimedia Commons screenshots were tried first; Wikimedia answered HTTP 429 to their files for ten minutes, so Flickr pictures of the same kind were used.)
No picture of Al Sweigart or of EZSheets could be found under a free licence (Openverse: no result for his name; the PyPI page is not free), so the sixth story of
08-tooling/sen0414_ch15_stories_v1_0_0.py (EzsheetsRelease2019) has no slide; its dates are in the 'what differs today' table and in the notes.
Writes 03-materials/ch15/assets/story_images_v2_0_0.json. Usage: python3 story_images_fetch_v2_0_0.py"""
__version__ = "2.0.0"
import datetime, hashlib, io, json, os, re, urllib.parse, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "03-materials", "ch15", "assets"))
UA = {"User-Agent": "SEN0414-course/1.0 (altunel.yusuf@gmail.com; course materials, IKU)"}
TODAY = datetime.date.today().isoformat()
MAXSIDE = 1600


def get(url):
    """GET with a patient retry: Wikimedia answers HTTP 429 when files are asked for in quick succession (waits 20, 40, 60 ... seconds, at most 8 tries)."""
    import time, urllib.error
    for k in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == 7:
                raise
            time.sleep(20 * (k + 1))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def openverse(query, creator, title):
    api = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": query, "page_size": 20})
    hits = [r for r in json.loads(get(api))["results"] if r["creator"] == creator and r["title"] == title]
    assert hits, (query, creator, title)
    return hits[0]


def flickr_taken(page):
    html = get(page).decode("utf-8", "replace")
    m = re.search(r'"dateTaken":"([^"]*)"', html)
    return m.group(1) if m else ""


def licence_name(h):
    lic = h["license"].lower()
    return "CC0 1.0" if lic == "cc0" else "CC %s %s" % (lic.upper(), h["license_version"])


def fetch(rec, fname, query, creator, title, desc, slide_credit, note):
    hit = openverse(query, creator, title)
    raw = get(hit["url"])
    im = Image.open(io.BytesIO(raw))
    fmt = "PNG" if fname.endswith(".png") else "JPEG"
    im = im.convert("RGBA" if fmt == "PNG" else "RGB")
    if max(im.size) > MAXSIDE:
        k = MAXSIDE / float(max(im.size))
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    im.save(os.path.join(ASSETS, fname), fmt)
    taken = flickr_taken(hit["foreign_landing_url"]) if "flickr" in hit["foreign_landing_url"] else ""
    rec[fname] = {
        "found_by": "Openverse search '%s' (id %s)" % (query, hit["id"]), "file_page": hit["foreign_landing_url"], "source_url": hit["url"], "retrieved": TODAY,
        "sha256_of_source_file": sha(raw), "LicenseShortName": licence_name(hit), "LicenseUrl": hit["license_url"], "Artist": hit["creator"], "Credit": hit["attribution"],
        "ImageDescription": desc, "date_taken_per_flickr_page": taken, "licence_note": note, "SlideCredit": slide_credit,
        "stored_size_px": list(im.size), "resized_to_at_most_px": MAXSIDE}


rec = {}
os.makedirs(ASSETS, exist_ok=True)
fetch(rec, "image_rochelle_google.jpg", "Jonathan Rochelle", "adactio", "Jonathan Rochelle - Google",
      "Jonathan Rochelle of Google, photographed by Jeremy Keith", "Jonathan Rochelle of Google. Photo: adactio, CC BY 2.0, Flickr.",
      "A real photograph of the person the story is about; the Flickr date is recorded in date_taken_per_flickr_page.")
fetch(rec, "image_cook_oauth.jpg", "Blaine Cook OAuth", "steve-uk", "Blaine Cook (Twitter / OAuth): Building the Social Kaleidoscope",
      "Blaine Cook, speaking about Twitter and OAuth", "Blaine Cook, who began OAuth in 2006. Photo: steve-uk, CC BY 2.0, Flickr.",
      "A real photograph of the person the story is about, taken at a later talk.")
fetch(rec, "image_bitcoin_paper.png", "Bitcoin white paper", "Unknown authorUnknown author", "Bitcoin white paper",
      "The first page of the Bitcoin white paper, bitcoin.pdf", "The first page of bitcoin.pdf, the paper the message announced. Wikimedia Commons, CC BY 4.0.",
      "Disclosure: no photograph of Satoshi Nakamoto exists; the picture is the paper that the 31 October 2008 message announced. The Wikimedia page names the author as unknown; the licence is the one Openverse reports.")
fetch(rec, "image_sheets_screen.jpg", "autoCrat for Google Sheets", "Wesley Fryer", "autoCrat for Google Sheets",
      "A screenshot of the Google Sheets add-ons page showing the add-on autoCrat", "The Google Sheets add-ons page. Screenshot: Wesley Fryer, CC BY 2.0, Flickr.",
      "Disclosure: a screenshot of the product (its logo and an add-on page), not of the Sheets API or of the migration guide the story is about; no free picture of the API itself was found.")
fetch(rec, "image_forms_screen.jpg", "Google Form Link", "Wesley Fryer", "Google Form Link",
      "A screenshot of a school web page with the Google Forms icon beside a link to a form", "A web page that links to a Google Form. Screenshot: Wesley Fryer, CC BY 2.0, Flickr.",
      "Disclosure: a screenshot that shows the Google Forms icon and a link to a form, not a photograph of the 2008 launch.")
with open(os.path.join(ASSETS, "story_images_v2_0_0.json"), "w", encoding="utf-8") as f:
    json.dump(rec, f, indent=1, ensure_ascii=False)
for k, v in rec.items():
    print(k, os.path.getsize(os.path.join(ASSETS, k)), "bytes |", v["LicenseShortName"], "|", v["sha256_of_source_file"][:10], "|", v["stored_size_px"], "|", v.get("date_taken_per_flickr_page", ""))
