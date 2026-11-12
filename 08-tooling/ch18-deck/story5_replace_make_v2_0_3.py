#!/usr/bin/env python3
"""Makes the chapter 18 build files of deck 2.0.3 as NEW files from those of 2.0.2 (nothing committed is edited), for the owner decision of 2026-11-12
to replace story 5 (draft 03-materials/ch18/DRAFT_ch18_v1_0_2.md): the picture image_etheader.png (the history comment at the top of Fredrik Lundh's ElementTree.py, drawn as text),
story_images_v2_0_3.json, deck_content_v2_0_3.py, deck_build_v2_0_3.py, build_v2_0_3.sh, links_check_v2_0_3.py and sen0414_ch18_stories_v1_2_0.py. Refuses to overwrite. Usage: story5_replace_make_v2_0_3.py"""
import json, os, re, sys, hashlib
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H); R = os.path.dirname(T); A = os.path.join(R, "03-materials/ch18/assets")
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s):
    if os.path.exists(p): sys.exit("refusing to overwrite " + p)
    open(p, "w", encoding="utf-8").write(s)
# picture: real header lines of ElementTree.py (code.activestate.com recipe 576403, history 5), drawn as text
lines = ["# history:", "# 2001-10-20 fl   created", "#   (from various sources)", "# 2004-08-23 fl   take advantage", "#   of post-2.1 expat features",
         "# 2005-02-01 fl   added iterparse", "#   implementation", "#", "# Copyright (c) 1999-2005 by", "# Fredrik Lundh."]   # lines of the header, wrapped to fit the picture
png = os.path.join(A, "image_etheader.png")
if os.path.exists(png): sys.exit("refusing to overwrite " + png)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 44)
W = 900; im = Image.new("RGB", (W, 60 + 68 * len(lines)), (250, 248, 240)); d = ImageDraw.Draw(im)
for i, l in enumerate(lines): d.text((30, 30 + 68 * i), l, font=font, fill=(60, 70, 80))
im.save(png)
rec = json.load(open(os.path.join(A, "story_images_v2_0_2.json"), encoding="utf-8"))
rec["image_etheader.png"] = {
    "found_by": "Text of the history comment of ElementTree.py as shown on code.activestate.com/recipes/576403-arbitrary-order-attribute-writing-with-elementtree/history/5/",
    "file_page": "https://code.activestate.com/recipes/576403-arbitrary-order-attribute-writing-with-elementtree/history/5/",
    "retrieved": "2026-11-12", "sha256_of_source_file": hashlib.sha256(open(png, "rb").read()).hexdigest(),
    "LicenseShortName": "text of a source-code header by Fredrik Lundh, drawn as a picture by this study", "Artist": "Fredrik Lundh (the text)",
    "licence_note": "No free portrait of Fredrik Lundh the Python developer was found on Wikimedia Commons (the file of a Fredrik Lundh from Sweden is another person), so the picture is the module's own history header: the 2001, 2004 and 2005 lines and the copyright line, the history lines and the copyright line of a permissively licensed source file, wrapped to fit the picture. Drawn by this study, not a photograph.",
    "SlideCredit": "The history comment at the top of Fredrik Lundh's ElementTree.py, drawn from the text shown on code.activestate.com. Not a photograph of Lundh."}
wr(os.path.join(A, "story_images_v2_0_3.json"), json.dumps(rec, indent=1, ensure_ascii=False))
# deck content
c = rd(os.path.join(H, "deck_content_v2_0_2.py"))
c = c.replace("story_images_v2_0_2.json", "story_images_v2_0_3.json")
a = c.index('    "pylib": dict('); b = c.index('    "laughs": dict(')
c = c[:a] + '''    "pylib": dict(
        title="Story: ElementTree was one person's library until 2005", img="image_etheader.png",
        who="Fredrik Lundh, who wrote ElementTree, and the Python developers who took it in.",
        what="ElementTree, a small XML toolkit, was created in 2001 and given to Python.",
        when="Created on 20 October 2001; added to the Python project on 12 December 2005.",
        where="On Lundh's website effbot.org, then in the Python source tree and on the Python-Dev mailing list.",
        why="Lundh kept the copyright, gave the library to Python and later handed its upkeep to the Python developers.",
        how="Write import xml.etree.ElementTree as ET. A module has a person behind it; the getchildren() of old tutorials is gone.",
        linktext="Improving ElementTree for 3.3 (Eli Bendersky)", link="https://eli.thegreenplace.net/2012/03/02/python-development-improving-elementtree-for-3-3/"),
''' + c[b:]
c = re.sub(r'    "pylib": "ElementTree came with Python 2.5[^\n]*\n', '    "pylib": "ElementTree was created by Fredrik Lundh on 20 October 2001 and added to the Python project on 12 December 2005. The picture is the history comment at the top of his ElementTree.py, drawn as text; it is not a photograph, because no free portrait of Lundh was found.",\n', c)
c = c.replace("# ---- the stories (5N1K)", "# 2.0.3 (over 2.0.2; owner decision 2026-11-12, draft 03-materials/ch18/DRAFT_ch18_v1_0_2.md): story 'pylib' (ElementTree 2006 and json 2008, same source page as chapter 16's SQLite story) becomes the ElementTree origin story.\n# ---- the stories (5N1K)", 1)
c = c.replace("deck_content_v2_0_2", "deck_content_v2_0_3")
wr(os.path.join(H, "deck_content_v2_0_3.py"), c)
for src, dst in (("deck_build_v2_0_2.py", "deck_build_v2_0_3.py"), ("build_v2_0_2.sh", "build_v2_0_3.sh"), ("links_check_v2_0_2.py", "links_check_v2_0_3.py")):
    s = rd(os.path.join(H, src)).replace("v2_0_2", "v2_0_3").replace("2.0.2", "2.0.3").replace("chapter_code_ch18_v1_0_2", "chapter_code_ch18_v1_0_3")
    wr(os.path.join(H, dst), s)
# stories script
s = rd(os.path.join(T, "sen0414_ch18_stories_v1_1_0.py"))
a = s.index('    {\n        "id": "PythonLibraries2006"'); b = s.index('    {\n        "id": "BillionLaughs2002"')
new = '''    {
        "id": "ElementTreeOrigin2001",
        "title": "ElementTree was one person's library until 2005",
        "when": "20 October 2001, and 12 December 2005",
        "who": "Fredrik Lundh, who wrote ElementTree, and the Python developers who took it into the standard library",
        "where": "Lundh's website effbot.org, the Python source tree and the Python-Dev mailing list",
        "link": "https://eli.thegreenplace.net/2012/03/02/python-development-improving-elementtree-for-3-3/",
        "concepts": ["RootTagAndChildren", "IterDocumentOrder"],
        "story": ("The history comment at the top of Lundh's ElementTree.py, as kept in an ActiveState recipe, says the module was created on 20 October 2001 'from various sources' and gives its copyright as 1999-2005 by Fredrik Lundh. "
                  "The commit mails of the Python project show him adding the library to the project's external directory on 12 December 2005, and the next day he took part in the Python-Dev thread on putting it into the standard library. "
                  "Eli Bendersky's account of the later work on Python 3.3 says the package was donated to CPython by its maintainer, who kept the copyright, and that Lundh later agreed to hand further maintenance to the Python developers. "
                  "In Python 3.14.6 this study still imported xml.etree.cElementTree, though its documentation calls the alias deprecated, and found that getchildren() and getiterator() of the old tutorials are gone."),
        "lesson": "A standard-library module has a person behind it; check the release you run",
        "source": ("The history comment of ElementTree.py (code.activestate.com recipe 576403, history 5); Python-checkins mails of 12 and 14 December 2005 (python.org pipermail); the Python-Dev thread 'ElementTree in stdlib' of 13 December 2005; "
                   "Eli Bendersky, 'Python development: improving ElementTree for 3.3', 2 March 2012, read 2026-11-12; this study's third-party record (removed names) and leaves RootTagAndChildren and IterDocumentOrder."),
    },
'''
s = s[:a] + new + s[b:]
s = s.replace("PythonLibraries2006", "ElementTreeOrigin2001").replace('("ElementTreeOrigin2001", "2006")', '("ElementTreeOrigin2001", "2005")')
s = s.replace("LINK_STATUS = {", "LINK_STATUS = {", 1)
wr(os.path.join(T, "sen0414_ch18_stories_v1_2_0.py"), s)
print("ok")
