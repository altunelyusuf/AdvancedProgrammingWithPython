#!/usr/bin/env python3
"""Repair of the chapter 16 story pictures (deck 2.0.1). The picture of the Bobby Tables story (image_munroe.jpg, 2.0.0) shows the speech NOTE read for Randall Munroe,
not the person, and was captioned as a photograph of him. This NEW tool finds a real, freely licensed PORTRAIT of Randall Munroe through Openverse
(id 0829cb21-01d0-4081-9671-953adcc9a5ce, 'Randall Munroe 2016' by re:publica from Germany, Wikimedia Commons, CC BY 2.0), fetches it, stores it as image_munroe_portrait.jpg
and writes 03-materials/ch16/assets/story_images_v2_0_1.json: every record of story_images_v2_0_0.json unchanged, except that the record 'image_munroe.jpg' is replaced by
'image_munroe_portrait.jpg'. The old file image_munroe.jpg and story_images_v2_0_0.json stay as committed. Wikimedia answers HTTP 429 now and then: patient retry, then the
960 px thumbnail that Wikimedia itself serves of the same file (as for the Hipp photograph in 2.0.0).
Usage: python3 story_images_fetch_v2_0_1.py"""
__version__ = "2.0.1"
import datetime, hashlib, io, json, os, sys, time, urllib.error, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "03-materials", "ch16", "assets"))
UA = {"User-Agent": "SEN0414-course/1.0 (altunel.yusuf@gmail.com; course materials, IKU)"}
OID = "0829cb21-01d0-4081-9671-953adcc9a5ce"


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


hit = json.loads(get("https://api.openverse.org/v1/images/%s/" % OID, 3, 10))
assert hit["creator"] == "re:publica from Germany" and hit["title"] == "Randall Munroe 2016" and hit["license"] == "by" and hit["license_version"] == "2.0", hit
url = hit["url"]
try:
    raw = get(url)
except urllib.error.HTTPError as e:
    print("original answered", e.code, "- reading the 960 px thumbnail Wikimedia serves of the same file")
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Randall_Munroe_2016.jpg/960px-Randall_Munroe_2016.jpg"
    raw = get(url)
im = Image.open(io.BytesIO(raw)).convert("RGB")
orig = im.size
if max(im.size) > 1600:
    k = 1600 / float(max(im.size))
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
im.save(os.path.join(ASSETS, "image_munroe_portrait.jpg"), "JPEG", quality=90)
rec = json.load(open(os.path.join(ASSETS, "story_images_v2_0_0.json"), encoding="utf-8"))
del rec["image_munroe.jpg"]
rec["image_munroe_portrait.jpg"] = {
    "found_by": "Openverse search 'Randall Munroe' (id %s)" % OID, "file_page": hit["foreign_landing_url"], "source_url": url,
    "retrieved": datetime.date.today().isoformat(), "sha256_of_source_file": hashlib.sha256(raw).hexdigest(),
    "LicenseShortName": "CC BY 2.0", "LicenseUrl": hit["license_url"], "Artist": hit["creator"], "Credit": hit["attribution"],
    "ImageDescription": "Randall Munroe, author of xkcd, portrait, 2016",
    "date_taken_per_flickr_page": "", "licence_note": "A real portrait photograph of the person the story is about (Wikimedia Commons, 'Randall Munroe 2016', from the re:publica conference photographs). "
    "It replaces the 2.0.0 picture, which showed the note of his 2014 Hugo speech and not the person (found by the controller, 2026-10-26). Original size %dx%d px." % orig,
    "SlideCredit": "Randall Munroe, author of xkcd, 2016. Photo: re:publica, CC BY 2.0, Wikimedia Commons.",
    "stored_size_px": list(im.size), "resized_to_at_most_px": 1600}
json.dump(rec, open(os.path.join(ASSETS, "story_images_v2_0_1.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("image_munroe_portrait.jpg", im.size, "from", url, "| sha256", rec["image_munroe_portrait.jpg"]["sha256_of_source_file"][:12])
