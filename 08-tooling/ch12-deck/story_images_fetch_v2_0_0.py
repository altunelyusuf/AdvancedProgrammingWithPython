#!/usr/bin/env python3
"""Fetches the story pictures of the chapter 12 deck 2.0.0 from Wikipedia/Wikimedia Commons, slowly (the egress IP is shared and rate limited),
and records for each picture its file page, author and licence as the Commons API prints them, into 03-materials/ch12/assets/story_images_v2_0_0.json.
Usage: python3 story_images_fetch_v2_0_0.py  (skips pictures already present)"""
__version__ = "2.0.0"
import json, os, re, subprocess, sys, time, urllib.parse
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "03-materials", "ch12", "assets")
UA = "SEN0414-course/1.0 (altunel.yusuf@gmail.com; course materials, IKU)"
# local file name -> (Wikipedia article, expected Commons file title or None = the article's lead image)
TARGETS = {
    "photo_dennis_ritchie_2011.jpg": ("Dennis_Ritchie", None),
    "photo_doug_mcilroy.jpg": ("Douglas_McIlroy", None),
    "image_midnight_commander.png": ("Midnight_Commander", None),
    "image_pip_logo.png": ("Pip_(package_manager)", None),
}


def get(url, binary=False, tries=8):
    for k in range(tries):
        r = subprocess.run(["curl", "-sS", "-m", "60", "-A", UA, "-w", "\n%{http_code}", url], capture_output=True)
        body, _, code = r.stdout.rpartition(b"\n")
        if code.strip() == b"200":
            return body if binary else body.decode("utf-8")
        time.sleep(30 + 30 * k)
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    rec_path = os.path.join(OUT, "story_images_v2_0_0.json")
    rec = json.load(open(rec_path)) if os.path.exists(rec_path) else {}
    for fn, (art, _) in TARGETS.items():
        if fn in rec and os.path.exists(os.path.join(OUT, fn)):
            continue
        time.sleep(15)
        s = get("https://en.wikipedia.org/api/rest_v1/page/summary/" + art)
        if not s:
            print("no summary", art); continue
        d = json.loads(s)
        oi = d.get("originalimage")
        if not oi:
            print("no lead image", art); continue
        src = oi["source"].split("?")[0]
        title = "File:" + urllib.parse.unquote(src.rsplit("/", 1)[1])
        time.sleep(15)
        info = get("https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extmetadata|url&format=json&titles=" + urllib.parse.quote(title))
        meta = {}
        if info:
            pages = json.loads(info)["query"]["pages"]
            em = list(pages.values())[0].get("imageinfo", [{}])[0].get("extmetadata", {})
            meta = {k: re.sub(r"<[^>]+>", "", em.get(k, {}).get("value", "")) for k in ("LicenseShortName", "LicenseUrl", "Artist", "Credit", "ImageDescription", "DateTimeOriginal")}
        thumb = src.replace("/commons/", "/commons/thumb/") + "/640px-" + src.rsplit("/", 1)[1] + (".png" if src.lower().endswith(".svg") else "") if (oi["width"] > 640 or src.lower().endswith(".svg")) else src
        time.sleep(15)
        data = get(src, binary=True) if (oi["width"] <= 1600 and not src.lower().endswith(".svg")) else None
        data = data or get(thumb, binary=True)
        if not data:
            print("no picture", art); continue
        open(os.path.join(OUT, fn), "wb").write(data)
        rec[fn] = {"article": "https://en.wikipedia.org/wiki/" + art, "file_page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                   "source_url": src, "bytes": len(data), "retrieved": time.strftime("%Y-%m-%d", time.gmtime()), **meta}
        json.dump(rec, open(rec_path, "w"), indent=1, ensure_ascii=False)
        print("ok", fn, meta.get("LicenseShortName"))
    json.dump(rec, open(rec_path, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
