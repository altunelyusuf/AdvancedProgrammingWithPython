"""Chapter 13 deck: the two story pictures that could not come from Wikimedia (HTTP 429 on the shared address), and the record for the
Reitz photo that was already in the repository. Writes 03-materials/ch13/assets/story_images_v2_0_0.json.
  image_gray_wanderer.jpg : Openverse result 'The First Web Server' (Flickr, asvensson, CC BY 2.0)
  image_koster_robots.jpg : a picture made here of the live text of https://pypi.org/robots.txt
Run: python3 story_images_make_v2_0_0.py"""
import hashlib, json, os, ssl, urllib.parse, urllib.request, datetime
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "03-materials", "ch13", "assets"))
UA = {"User-Agent": "SEN0414-course/1.0 (altunel.yusuf@gmail.com)"}
TODAY = datetime.date.today().isoformat()


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
        return r.read()


def sha(b):
    return hashlib.sha256(b).hexdigest()


rec = {}
# ---- Gray: Openverse
api = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": "The First Web Server", "page_size": 6})
hit = [r for r in json.loads(get(api))["results"] if r["creator"] == "asvensson" and r["title"] == "The First Web Server"][0]
raw = get(hit["url"])
open(os.path.join(ASSETS, "image_gray_wanderer.jpg"), "wb").write(raw)
rec["image_gray_wanderer.jpg"] = {
    "found_by": "Openverse search 'The First Web Server' (id %s)" % hit["id"],
    "file_page": hit["foreign_landing_url"], "source_url": hit["url"], "retrieved": TODAY, "sha256_of_source_file": sha(raw),
    "LicenseShortName": "CC BY 2.0", "LicenseUrl": hit["license_url"], "Artist": hit["creator"],
    "Credit": hit["attribution"],
    "ImageDescription": "The NeXT computer used as the first Web server at CERN, Flickr photo 'The First Web Server'",
    "licence_note": "Disclosure: this is NOT a picture of Matthew Gray or of the Wanderer; no free picture of either could be fetched because Wikimedia answered HTTP 429 for hours. It shows the first Web server, the kind of machine the Wanderer counted. The caption on the slide says so."}

# ---- Koster: picture of a real robots.txt
text = get("https://pypi.org/robots.txt").decode("utf-8")
lines = text.rstrip("\n").split("\n")
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 26)
bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 22)
W, lh, top = 1000, 36, 70
H = top + lh * len(lines) + 30
img = Image.new("RGB", (W, H), (30, 34, 40))
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 48], fill=(52, 58, 66))
for i, c in enumerate(((237, 106, 94), (245, 191, 79), (97, 197, 84))):
    d.ellipse([16 + i * 30, 16, 32 + i * 30, 32], fill=c)
d.text((130, 12), "https://pypi.org/robots.txt", font=bold, fill=(220, 224, 230))
for n, ln in enumerate(lines):
    col = (140, 200, 255) if ln.lower().startswith("user-agent") else ((255, 170, 110) if ln.lower().startswith("disallow") else (190, 230, 160))
    d.text((24, top + n * lh), ln, font=font, fill=col)
out = os.path.join(ASSETS, "image_koster_robots.jpg")
img.save(out, quality=90)
rec["image_koster_robots.jpg"] = {
    "found_by": "made for this deck: a rendering of the live text of the PyPI robots.txt, fetched %s" % TODAY,
    "file_page": "https://pypi.org/robots.txt", "source_url": "https://pypi.org/robots.txt", "retrieved": TODAY,
    "sha256_of_source_file": sha(text.encode("utf-8")),
    "LicenseShortName": "Made for this course (rendering); the text is a plain list of directives published by PyPI, no licence stated",
    "LicenseUrl": "", "Artist": "SEN0414 course (rendering); text by the PyPI maintainers",
    "Credit": "rendering of pypi.org/robots.txt",
    "ImageDescription": "A robots.txt file as served by pypi.org: User-agent and Disallow lines",
    "licence_note": "Disclosure: no photograph or scan of the 1994 standard could be used. robotstxt.org carries '(c) 2007 All rights reserved' and Wikimedia answered HTTP 429. The picture is a drawing of a real, current robots.txt, made by this script from the text as served; PyPI states no licence for the file."}

# ---- Reitz: the photo already in the repository (record from ASSETS_PROVENANCE_v1_0_0.md)
rp = os.path.join(ASSETS, "photo_kenneth_reitz.jpg")
rec["photo_kenneth_reitz.jpg"] = {
    "found_by": "Wikimedia Commons, fetched 2026-10-12 (see ASSETS_PROVENANCE_v1_0_0.md)",
    "file_page": "https://commons.wikimedia.org/wiki/File:Rupy_Talk_Kenneth_Reitz_(18947687).jpeg",
    "source_url": "https://commons.wikimedia.org/wiki/File:Rupy_Talk_Kenneth_Reitz_(18947687).jpeg", "retrieved": "2026-10-12",
    "sha256_of_source_file": sha(open(rp, "rb").read()),
    "LicenseShortName": "CC BY 3.0", "LicenseUrl": "https://creativecommons.org/licenses/by/3.0",
    "Artist": "Nils Pascal Illenseer", "Credit": "photo: Nils Pascal Illenseer",
    "ImageDescription": "Kenneth Reitz giving a talk at Rupy, 17 November 2012",
    "licence_note": "960-pixel rendition of the 2048-pixel original; the identification rests on the Commons file title."}

rec["image_gray_wanderer.jpg"]["SlideCredit"] = "The first Web server (CERN), not Gray's machine. Photo: asvensson, CC BY 2.0, Flickr."
rec["image_koster_robots.jpg"]["SlideCredit"] = "A real robots.txt (pypi.org), drawn for this deck. Not the 1994 file."
json.dump(rec, open(os.path.join(ASSETS, "story_images_v2_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("ok", {k: (v["LicenseShortName"][:30], v["sha256_of_source_file"][:10]) for k, v in rec.items()})
