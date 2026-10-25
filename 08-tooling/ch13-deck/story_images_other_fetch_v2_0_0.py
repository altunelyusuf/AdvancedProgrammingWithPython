#!/usr/bin/env python3
"""Fetches the story pictures of the chapter 13 deck 2.0.0 that come from the projects' own sites (Wikimedia answered HTTP 429 to this machine for hours,
and the earlier research found no Commons photograph of these subjects): the illustration on Leonard Richardson's Beautiful Soup page, the Selenium logo
of selenium.dev and the Playwright logo of playwright.dev. Records for each file its source address, the retrieval date, the SHA-256 and the licence
statement that was read (and what could not be read), into 03-materials/ch13/assets/story_images_other_v2_0_0.json.
Usage: python3 story_images_other_fetch_v2_0_0.py"""
__version__ = "2.0.0"
import hashlib, json, os, subprocess, tempfile, time
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "03-materials", "ch13", "assets")
UA = "SEN0414-course/1.0 (altunel.yusuf@gmail.com; course materials, IKU)"


def get(url, path):
    r = subprocess.run(["curl", "-sS", "-L", "-m", "60", "-A", UA, "-o", path, "-w", "%{http_code}", url], capture_output=True, text=True)
    assert r.stdout.strip() == "200", (url, r.stdout, r.stderr)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    rec, tmp = {}, tempfile.mkdtemp()
    today = time.strftime("%Y-%m-%d", time.gmtime())
    # 1. Richardson: the illustration of his Beautiful Soup page
    src = "https://www.crummy.com/software/BeautifulSoup/10.1.jpg"
    raw = os.path.join(tmp, "r.jpg"); get(src, raw)
    Image.open(raw).convert("RGB").save(os.path.join(OUT, "image_richardson_tortoise.jpg"), "JPEG", quality=92)
    rec["image_richardson_tortoise.jpg"] = {"found_by": "the picture on the author's own page", "file_page": "https://www.crummy.com/software/BeautifulSoup/", "source_url": src, "retrieved": today,
        "sha256_of_source_file": sha(raw), "LicenseShortName": "Public domain (artwork of 1865)", "LicenseUrl": "", "Artist": "John Tenniel",
        "Credit": "As shown on Leonard Richardson's page, crummy.com", "ImageDescription": "Tenniel's drawing of Alice with the Mock Turtle and the Gryphon, shown on the Beautiful Soup page under the line 'We called him Tortoise because he taught us'",
        "licence_note": "The drawing is by John Tenniel (1820-1914) for Alice's Adventures in Wonderland (1865) and is in the public domain by its age. The file is the copy served by crummy.com; that site carries a general 'All rights reserved' line and no statement about this file, so the scan itself has no recorded licence."}
    # 2. Selenium logo
    src = "https://www.selenium.dev/images/selenium_logo_square_green.png"
    raw = os.path.join(tmp, "s.png"); get(src, raw)
    im = Image.open(raw).convert("RGBA"); im.thumbnail((640, 640)); im.save(os.path.join(OUT, "image_selenium_logo.png"), "PNG")
    lic = os.path.join(tmp, "sl.txt"); get("https://raw.githubusercontent.com/SeleniumHQ/seleniumhq.github.io/trunk/LICENSE", lic)
    rec["image_selenium_logo.png"] = {"found_by": "the project's own site", "file_page": "https://www.selenium.dev/", "source_url": src, "retrieved": today, "sha256_of_source_file": sha(raw),
        "LicenseShortName": "Apache-2.0 (repository of the site); logo is a trademark of its owners", "LicenseUrl": "https://www.apache.org/licenses/LICENSE-2.0", "Artist": "The Selenium project",
        "Credit": "selenium.dev", "ImageDescription": "The Selenium logo", "licence_note": "LICENSE of SeleniumHQ/seleniumhq.github.io read on %s (Apache License 2.0, sha256 %s). The file itself carries no separate licence line; it is used to identify the project the story is about." % (today, sha(lic))}
    # 3. Playwright logo (an SVG, drawn to a picture by LibreOffice)
    src = "https://playwright.dev/img/playwright-logo.svg"
    raw = os.path.join(tmp, "pw.svg"); get(src, raw)
    subprocess.run(["soffice", "--headless", "--convert-to", "png", "--outdir", tmp, raw], capture_output=True, timeout=180)
    im = Image.open(os.path.join(tmp, "pw.png")).convert("RGBA"); im.save(os.path.join(OUT, "image_playwright_logo.png"), "PNG")
    lic = os.path.join(tmp, "pl.txt"); get("https://raw.githubusercontent.com/microsoft/playwright/main/LICENSE", lic)
    rec["image_playwright_logo.png"] = {"found_by": "the project's own site", "file_page": "https://playwright.dev/", "source_url": src, "retrieved": today, "sha256_of_source_file": sha(raw),
        "LicenseShortName": "Apache-2.0 (repository of the project); logo is a trademark of its owners", "LicenseUrl": "https://www.apache.org/licenses/LICENSE-2.0", "Artist": "Microsoft and the Playwright contributors",
        "Credit": "playwright.dev", "ImageDescription": "The Playwright logo", "licence_note": "LICENSE of microsoft/playwright read on %s (Apache License 2.0, sha256 %s). The SVG itself carries no separate licence line; it is used to identify the project the story is about." % (today, sha(lic))}
    json.dump(rec, open(os.path.join(OUT, "story_images_other_v2_0_0.json"), "w"), indent=1, ensure_ascii=False)
    for k, v in rec.items():
        print(k, os.path.getsize(os.path.join(OUT, k)), "bytes", v["LicenseShortName"])


if __name__ == "__main__":
    main()
