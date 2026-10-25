#!/usr/bin/env python3
"""Fetches the six story pictures of the chapter 16 deck 2.0.0 and records, for each file, where it came from, when, its SHA-256 and its licence.
Wikimedia Commons answers HTTP 429 to its files from this machine, so every picture was FOUND through Openverse (api.openverse.org, which indexes Flickr and
Wikimedia Commons under Creative Commons licences); the file is read from the address Openverse gives, with a patient retry for Wikimedia (a 429 lasts minutes; for the Hipp photograph the 429 did not clear in two runs of 8 tries and the 960 px thumbnail of the same file, which Wikimedia serves, is read).
One file is read from its owner's own site because Openverse does not index it: the SQLite banner (sqlite.org/images, public domain by sqlite.org/copyright.html).
(The xkcd comic itself, imgs.xkcd.com, CC BY-NC 2.5, was fetched first and is only 666 x 205 pixels: its speech is unreadable at the size of a story picture, so the photograph of its author is used; the comic stays behind the live link.)
  image_hipp_sqlite.jpg     'D. Richard Hipp, 2009' (Wikimedia Commons via Openverse, CC BY 2.0): D. Richard Hipp, who designed SQLite in 2000
  image_codd.jpg            'Edgar F Codd' (Flickr, yyq123, CC BY-SA 2.0): Edgar F. Codd, author of the 1970 relational-model paper (a small file: it is the only free portrait found)
  image_guido_python.jpg    'Guido van Rossum OSCON 2006' (Wikimedia Commons, Doc Searls, CC BY-SA 2.0) or, when Wikimedia stays at 429, 'Guido van Rossum PyCon 2013' (Flickr, eschipul, CC BY 2.0)
  image_munroe.jpg          'Randall Munroe's Hugo acceptance speech' (Flickr, gruntzooki, CC BY-SA 2.0): Randall Munroe, author of xkcd, at the Hugo Awards, Loncon 3, London, 2014
  image_sqlite_banner.png   the SQLite banner (sqlite.org, public domain): the thing the 3.37.0 release is about; no photograph of a release exists
  image_jim_gray.jpg        'Jim Gray' (Flickr, dullhunk, CC BY 2.0): Jim Gray, whose work on transactions the 1983 paper builds on
Writes 03-materials/ch16/assets/story_images_v2_0_0.json. Usage: python3 story_images_fetch_v2_0_0.py"""
__version__ = "2.0.0"
import datetime, hashlib, io, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "03-materials", "ch16", "assets"))
UA = {"User-Agent": "SEN0414-course/1.0 (altunel.yusuf@gmail.com; course materials, IKU)"}
TODAY = datetime.date.today().isoformat()
MAXSIDE = 1600


def get(url, tries=8, wait=20):
    """GET with a patient retry: Wikimedia answers HTTP 429 when files are asked for in quick succession (waits wait, 2*wait ... seconds)."""
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            print("  429 for", url[:80], "- waiting", wait * (k + 1), "s", flush=True)
            time.sleep(wait * (k + 1))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def openverse(query, creator, title):
    api = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": query, "page_size": 20})
    hits = [r for r in json.loads(get(api, 3, 10))["results"] if r["creator"] == creator and r["title"].startswith(title)]
    assert hits, (query, creator, title)
    return hits[0]


def flickr_taken(page):
    try:
        html = get(page, 2, 10).decode("utf-8", "replace")
    except Exception:
        return ""
    m = re.search(r'"dateTaken":"([^"]*)"', html)
    return m.group(1) if m else ""


def licence_name(h):
    lic = h["license"].lower()
    return "CC0 1.0" if lic == "cc0" else "CC %s %s" % (lic.upper(), h["license_version"])


def store(raw, fname):
    im = Image.open(io.BytesIO(raw))
    fmt = "PNG" if fname.endswith(".png") else "JPEG"
    im = im.convert("RGBA" if fmt == "PNG" else "RGB")
    if max(im.size) > MAXSIDE:
        k = MAXSIDE / float(max(im.size))
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    im.save(os.path.join(ASSETS, fname), fmt)
    return im.size


def fetch(rec, fname, query, creator, title, desc, slide_credit, note, url_override=None):
    hit = openverse(query, creator, title)
    raw = get(url_override or hit["url"])
    size = store(raw, fname)
    taken = flickr_taken(hit["foreign_landing_url"]) if "flickr" in hit["foreign_landing_url"] else ""
    rec[fname] = {
        "found_by": "Openverse search '%s' (id %s)" % (query, hit["id"]), "file_page": hit["foreign_landing_url"], "source_url": url_override or hit["url"], "retrieved": TODAY,
        "sha256_of_source_file": sha(raw), "LicenseShortName": licence_name(hit), "LicenseUrl": hit["license_url"], "Artist": hit["creator"], "Credit": hit["attribution"],
        "ImageDescription": desc, "date_taken_per_flickr_page": taken, "licence_note": note, "SlideCredit": slide_credit,
        "stored_size_px": list(size), "resized_to_at_most_px": MAXSIDE}


def fetch_direct(rec, fname, url, found_by, page, lic, lic_url, artist, desc, slide_credit, note):
    raw = get(url)
    size = store(raw, fname)
    rec[fname] = {"found_by": found_by, "file_page": page, "source_url": url, "retrieved": TODAY, "sha256_of_source_file": sha(raw), "LicenseShortName": lic, "LicenseUrl": lic_url,
                  "Artist": artist, "Credit": artist, "ImageDescription": desc, "date_taken_per_flickr_page": "", "licence_note": note, "SlideCredit": slide_credit,
                  "stored_size_px": list(size), "resized_to_at_most_px": MAXSIDE}


REC_PATH = os.path.join(ASSETS, "story_images_v2_0_0.json")
os.makedirs(ASSETS, exist_ok=True)
# A picture already recorded (a file that exists beside its record) is not fetched again: Wikimedia answers HTTP 429 for long stretches to this machine,
# so the script may be run again until the Wikimedia picture is in; every record keeps the date of its own fetch ('retrieved').
rec = json.load(open(REC_PATH, encoding="utf-8")) if os.path.exists(REC_PATH) else {}


def have(fname):
    return fname in rec and os.path.exists(os.path.join(ASSETS, fname))

if not have("image_codd.jpg"):
  fetch(rec, "image_codd.jpg", "Edgar Codd", "yyq123", "关系型数据库奠基人 Edgar F Codd",
      "Edgar F. Codd, photographed by yyq123", "Edgar F. Codd. Photo: yyq123, CC BY-SA 2.0, Flickr.",
      "A real photograph of the person the story is about. The stored file is small (the only free portrait found), so it looks soft when enlarged.")
if not have("image_jim_gray.jpg"):
  fetch(rec, "image_jim_gray.jpg", "Jim Gray Tandem", "dullhunk", "Jim Gray",
      "Jim Gray, database researcher, photographed by dullhunk", "Jim Gray. Photo: dullhunk, CC BY 2.0, Flickr.",
      "Disclosure: Jim Gray did not write the 1983 paper the story is about (Haerder and Reuter did); the paper builds on his work on transactions. No free picture of Haerder or Reuter was found "
      "(Openverse returned none for either name), so the slide shows Gray and says so.")
if not have("image_guido_python.jpg"):
  fetch(rec, "image_guido_python.jpg", "Guido van Rossum PyCon 2013", "eschipul", "Guido van Rossum PyCon 2013",
      "Guido van Rossum, creator of Python, at PyCon 2013", "Guido van Rossum, who led Python when sqlite3 arrived. Photo: eschipul, CC BY 2.0, Flickr.",
      "Disclosure: taken in 2013, not 2006. Guido van Rossum led the Python project in 2006 but is not named in the 'What's New in Python 2.5' passage the story rests on. "
      "The 2006 OSCON photograph on Wikimedia Commons (Doc Searls, CC BY-SA 2.0) was tried by hand first and Wikimedia answered HTTP 429.")
if not have("image_sqlite_banner.png"):
  fetch_direct(rec, "image_sqlite_banner.png", "https://www.sqlite.org/images/sqlite370_banner.gif", "address in the sqlite.org page header", "https://www.sqlite.org/",
             "Public domain", "https://www.sqlite.org/copyright.html", "SQLite developers",
             "The SQLite banner of the documentation pages", "The SQLite banner. sqlite.org, public domain.",
             "Disclosure: the logo of the product the 3.37.0 release is about; a release is not a thing a photograph shows. The Wikimedia Commons file SQLite370.svg states that this logo is part of the SQLite documentation, released to the public domain.")
if not have("image_munroe.jpg"):
  fetch(rec, "image_munroe.jpg", "Randall Munroe", "gruntzooki", "Randall Munroe's Hugo acceptance speech",
      "Randall Munroe, author of xkcd, accepting a Hugo Award at Loncon 3, London", "Randall Munroe, author of xkcd. Photo: gruntzooki, CC BY-SA 2.0, Flickr.",
      "A real photograph of the person the story is about, taken at the Hugo Awards of Loncon 3 (London, 2014; the title of the Flickr photograph says Loncon 3). The comic itself is only 666 x 205 pixels, too small to read on a slide.")
try:
  if not have("image_hipp_sqlite.jpg"):
    fetch(rec, "image_hipp_sqlite.jpg", "D. Richard Hipp", "D. Richard Hipp", "D. Richard Hipp, 2009年",
          "D. Richard Hipp, creator of SQLite, 2009", "D. Richard Hipp, who designed SQLite in 2000. Photo: D. Richard Hipp, 2009, CC BY 2.0, Wikimedia Commons.",
          "A real photograph of the person the story is about, taken in 2009. The original file answered HTTP 429 (Wikimedia, from this address) every time, so the 960-pixel-wide thumbnail "
          "that Wikimedia itself serves of the same file was fetched instead (the 429 message points to thumbnails); it is the same photograph, scaled by Wikimedia.",
          url_override="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/D._Richard_Hipp%2C_2009%E5%B9%B4.jpg/960px-D._Richard_Hipp%2C_2009%E5%B9%B4.jpg")
except Exception as e:
    print("HIPP PHOTO NOT FETCHED:", repr(e))
with open(os.path.join(ASSETS, "story_images_v2_0_0.json"), "w", encoding="utf-8") as f:
    json.dump(rec, f, indent=1, ensure_ascii=False)
for k, v in rec.items():
    print(k, os.path.getsize(os.path.join(ASSETS, k)), "bytes |", v["LicenseShortName"], "|", v["sha256_of_source_file"][:10], "|", v["stored_size_px"], "|", v.get("date_taken_per_flickr_page", ""))
