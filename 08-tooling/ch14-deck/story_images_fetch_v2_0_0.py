#!/usr/bin/env python3
"""Fetches the six story pictures of the chapter 14 deck 2.0.0 and records, for each file, where it came from, when, its SHA-256 and its licence.
Wikimedia answered HTTP 429 to this machine, so the pictures come from Openverse (api.openverse.org, which indexes Flickr and other sources under Creative
Commons licences), from the open-access article itself (Genome Biology, CC BY 4.0) and from the project's own documentation (the openpyxl logo).
  image_bricklin_talk.jpg      Openverse 'Business of Software - Dan Bricklin' (Flickr, betsyweber, CC BY 2.0)
  image_excel_mac_1985.jpg     Openverse 'Apple Computer with Excel 1.0 for Macintosh Screenshot 1985' (Flickr, Microsoft Sweden, CC BY 2.0)
  image_ooxml_rally.jpg        Openverse 'OOXML Rally' (Flickr, AndyArmstrong, CC BY-SA 2.0); taken 2008-04-09 in Oslo, per the Flickr page
  image_openpyxl_logo.png      the logo of the openpyxl documentation (openpyxl.readthedocs.io/en/stable/_static/logo.png), 179 x 35 pixels, enlarged
  image_rr_paper.jpg           Openverse 'nber-reinhart-rogoff' (Flickr, okfn, CC BY 2.0): the title page of the paper that Herndon, Ash and Pollin tested
  image_gene_names_fig1.png    Fig. 1 of Ziemann, Eren and El-Osta 2016, Genome Biology 17:177 (CC BY 4.0), as served by media.springernature.com
Writes 03-materials/ch14/assets/story_images_v2_0_0.json. Usage: python3 story_images_fetch_v2_0_0.py"""
__version__ = "2.0.0"
import datetime, hashlib, io, json, os, re, urllib.parse, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "03-materials", "ch14", "assets"))
UA = {"User-Agent": "SEN0414-course/1.0 (altunel.yusuf@gmail.com; course materials, IKU)"}
TODAY = datetime.date.today().isoformat()


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
        return r.read()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def openverse(query, creator, title):
    api = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": query, "page_size": 12})
    hits = [r for r in json.loads(get(api))["results"] if r["creator"] == creator and r["title"] == title]
    assert hits, (query, creator, title)
    return hits[0]


def flickr_taken(page):
    html = get(page).decode("utf-8", "replace")
    m = re.search(r'"dateTaken":"([^"]*)"', html)
    return m.group(1) if m else ""


def from_openverse(rec, fname, query, creator, title, desc, slide_credit, note):
    hit = openverse(query, creator, title)
    raw = get(hit["url"])
    open(os.path.join(ASSETS, fname), "wb").write(raw)
    taken = flickr_taken(hit["foreign_landing_url"]) if "flickr" in hit["foreign_landing_url"] else ""
    rec[fname] = {
        "found_by": "Openverse search '%s' (id %s)" % (query, hit["id"]), "file_page": hit["foreign_landing_url"], "source_url": hit["url"], "retrieved": TODAY,
        "sha256_of_source_file": sha(raw), "LicenseShortName": "%s %s" % (hit["license"].upper().replace("BY-SA", "CC BY-SA").replace("BY", "CC BY") if not hit["license"].startswith("by-") else "CC " + hit["license"].upper(), hit["license_version"]),
        "LicenseUrl": hit["license_url"], "Artist": hit["creator"], "Credit": hit["attribution"], "ImageDescription": desc, "date_taken_per_flickr_page": taken,
        "licence_note": note, "SlideCredit": slide_credit}


rec = {}
from_openverse(rec, "image_bricklin_talk.jpg", "Dan Bricklin", "betsyweber", "Business of Software - Dan Bricklin",
               "Dan Bricklin speaking at the Business of Software conference; the slide behind him is dated October 6, 2010",
               "Dan Bricklin at the Business of Software conference, 2010. Photo: Betsy Weber, CC BY 2.0, Flickr.",
               "A real photograph of the person the story is about, taken 32 years after the idea of 1978 that the story tells.")
from_openverse(rec, "image_excel_mac_1985.jpg", "Excel 1.0 Macintosh", "Microsoft Sweden", "Apple Computer with Excel 1.0 for Macintosh Screenshot 1985",
               "An Apple Macintosh showing a screenshot of Excel 1.0, 1985",
               "A Macintosh showing Excel 1.0, 1985. Photo: Microsoft Sweden, CC BY 2.0, Flickr.",
               "A real photograph of the machine and program the story is about (Excel for the Macintosh, 1985).")
from_openverse(rec, "image_ooxml_rally.jpg", "OOXML Rally", "AndyArmstrong", "OOXML Rally",
               "A protester holding a sign 'Defend ISO's integrity: no more standards in through the back door' at the OOXML rally in Oslo",
               "A rally about the OOXML vote in ISO, Oslo, 9 April 2008. Photo: Andy Armstrong, CC BY-SA 2.0, Flickr.",
               "Disclosure: the photograph shows a protest in Oslo about the way Office Open XML was approved as an ISO standard (Flickr tags: ooxml, oslo, protest; date taken 2008-04-09 per the Flickr page). "
               "It shows neither the file format nor the Ecma committee; no free photograph of those could be fetched (Wikimedia answered HTTP 429, and the Open Packaging Convention diagram could not be fetched through Openverse either: HTTP 424).")
# openpyxl logo
src = "https://openpyxl.readthedocs.io/en/stable/_static/logo.png"
raw = get(src)
im = Image.open(io.BytesIO(raw)).convert("RGBA")
big = im.resize((im.width * 4, im.height * 4), Image.LANCZOS)
big.save(os.path.join(ASSETS, "image_openpyxl_logo.png"))
rec["image_openpyxl_logo.png"] = {
    "found_by": "the openpyxl documentation, start page (img class=logo)", "file_page": "https://openpyxl.readthedocs.io/en/stable/", "source_url": src, "retrieved": TODAY,
    "sha256_of_source_file": sha(raw), "LicenseShortName": "MIT (the project's licence); no separate licence line for the logo file", "LicenseUrl": "https://opensource.org/license/mit",
    "Artist": "The openpyxl project", "Credit": "openpyxl documentation", "ImageDescription": "The OpenPyXL logo of the project's documentation",
    "licence_note": "Disclosure: the logo file is 179 x 35 pixels and is shown enlarged four times, so it looks soft. The documentation page says 'Copyright 2010 - 2024, See AUTHORS' and the project is MIT-licensed; the logo has no licence line of its own. No photograph of the authors (Eric Gazoni, Charlie Clark) could be found under a free licence.",
    "SlideCredit": "The logo of the openpyxl documentation, enlarged. Not a picture of the authors."}
from_openverse(rec, "image_rr_paper.jpg", "Reinhart Rogoff", "okfn", "nber-reinhart-rogoff",
               "The title page of NBER Working Paper 15639, Growth in a Time of Debt, by Carmen M. Reinhart and Kenneth S. Rogoff, January 2010",
               "Title page of Reinhart and Rogoff's working paper, 2010. Image: Open Knowledge Foundation, CC BY 2.0, Flickr.",
               "Disclosure: this is the title page of the paper that Herndon, Ash and Pollin tested, not a photograph of the three authors of the 2013 critique; no free photograph of them could be fetched.")
# the figure of the article
src = "https://media.springernature.com/lw1200/springer-static/image/art%3A10.1186%2Fs13059-016-1044-7/MediaObjects/13059_2016_1044_Fig1_HTML.gif"
raw = get(src)
Image.open(io.BytesIO(raw)).convert("RGB").save(os.path.join(ASSETS, "image_gene_names_fig1.png"))
rec["image_gene_names_fig1.png"] = {
    "found_by": "the open-access article itself, Genome Biology 17:177 (2016), doi 10.1186/s13059-016-1044-7", "file_page": "https://genomebiology.biomedcentral.com/articles/10.1186/s13059-016-1044-7",
    "source_url": src, "retrieved": TODAY, "sha256_of_source_file": sha(raw), "LicenseShortName": "CC BY 4.0", "LicenseUrl": "https://creativecommons.org/licenses/by/4.0/",
    "Artist": "Mark Ziemann, Yotam Eren and Assam El-Osta", "Credit": "Ziemann M, Eren Y, El-Osta A. Genome Biology 2016;17:177, Fig. 1", "ImageDescription": "Fig. 1 of the article: percentage of papers with gene lists affected, by journal, and files with gene name errors per year, 2005 to 2015",
    "licence_note": "The article page carries the Creative Commons Attribution 4.0 licence (creativecommons.org/licenses/by/4.0/ found in the page text on %s). The GIF was converted to PNG without other change." % TODAY,
    "SlideCredit": "Fig. 1 of the paper: share of papers with gene-name errors by journal, and files per year. Ziemann et al. 2016, CC BY 4.0."}
json.dump(rec, open(os.path.join(ASSETS, "story_images_v2_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for k, v in rec.items():
    print(k, os.path.getsize(os.path.join(ASSETS, k)), "bytes |", v["LicenseShortName"], "|", v["sha256_of_source_file"][:10], "|", v.get("date_taken_per_flickr_page", ""))
