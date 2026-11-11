#!/usr/bin/env python3
"""Makes a NEW page version of a SEN0414 chapter page whose only changes are its Stories tab and, when asked, its chapter-code list: the stories (and their embedded pictures) are rebuilt exactly as
sen0414_page_data_v2_27_0.py builds them (the newest sen0414_chNN_stories_v*.py after its own run_checks, the pictures of the newest chNN-page/stories_img_v*.json embedded as data URIs, 640 px wide for one picture, 420 for several,
JPEG quality 82), and put into the page's own data block. Everything else of the page stays byte for byte: the tool first proves that the old page's data block is exactly json.dumps(data, ensure_ascii=True)
with '</' written '<\\/' (the way the page builder writes it), refuses to go on when it is not, and at the end proves that every key of the data other than the changed ones, and all of the page outside the data block except
the version in the meta tag, is unchanged.
Usage: sen0414_page_stories_patch_v1_0_0.py NN OLD_PAGE.html NEW_PAGE.html NEW_VERSION [MANIFEST.json]    (refuses to overwrite NEW_PAGE.html)"""
__version__ = "1.0.0"
import base64, glob, importlib.util, io, json, os, sys
from PIL import Image
if len(sys.argv) < 5: sys.exit(__doc__)
N, OLD, NEW, VER = sys.argv[1:5]; MAN = sys.argv[5] if len(sys.argv) > 5 else None
T = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(T)
if os.path.exists(NEW): sys.exit("refusing to overwrite " + NEW)
TAG = '<script type="application/json" id="data">'
def dump(d): return json.dumps(d, ensure_ascii=True).replace("</", "<\\/")
h = open(OLD, encoding="utf-8").read(); a = h.index(TAG) + len(TAG); b = h.index("</script>", a); blob = h[a:b]; d = json.loads(blob)
if dump(d) != blob: sys.exit("REFUSED: the old page's data block is not json.dumps(data) in the page builder's form")
oldv = d["_version"]
key = lambda x, s, e: [int(v) for v in x.rsplit("_v", 1)[1][:-e].split("_")]
sf = sorted(glob.glob(os.path.join(T, "sen0414_ch%s_stories_v*.py" % N)), key=lambda x: key(x, 0, 3))[-1]
spec = importlib.util.spec_from_file_location("stories_mod", sf); sm = importlib.util.module_from_spec(spec); spec.loader.exec_module(sm)
bad = sm.run_checks()
if bad: sys.exit("story companion fails its own checks: %s" % bad)
imf = sorted(glob.glob(os.path.join(T, "ch%s-page" % N, "stories_img_v*.json")), key=lambda x: key(x, 0, 5))[-1]
imap = {k: v for k, v in json.load(open(imf)).items() if not k.startswith("_")}
ADIR = os.path.join(REPO, "03-materials", "ch%s" % N, "assets")
def embed(fn, maxw):
    im = Image.open(os.path.join(ADIR, fn)); im.load()
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    if fn.lower().endswith(".png"): im.save(buf, "PNG", optimize=True); mime = "image/png"
    else: im.convert("RGB").save(buf, "JPEG", quality=82, optimize=True); mime = "image/jpeg"
    return {"data": "data:%s;base64,%s" % (mime, base64.b64encode(buf.getvalue()).decode()), "w": im.width, "h": im.height}
stories = []
for s in sm.STORIES:
    e = {k: s[k] for k in ("id", "title", "when", "who", "where", "link", "story", "lesson", "source")}
    e["concepts"] = list(s.get("concepts", []))
    pics = imap.get(s["id"], [])
    e["imgs"] = [dict(embed(p["file"], 640 if len(pics) == 1 else 420), credit=p["credit"], file=p["file"]) for p in pics]
    stories.append(e)
nd = dict(d); nd["stories"] = stories; changed = ["stories", "_version"]
if MAN:
    m = json.load(open(MAN, encoding="utf-8")); ex = m["examples"] if isinstance(m, dict) else m
    nd["chaptercode"] = {"file": os.path.relpath(MAN, REPO), "version": m.get("version", ""), "examples": [{k: e[k] for k in ("order", "name", "code", "expected", "slide") if k in e} for e in ex]}
    changed.append("chaptercode")
nd["_version"] = VER
metaold = '<meta name="version" content="%s">' % oldv
if h.count(metaold) != 1: sys.exit("REFUSED: the version meta tag is not found once")
out = h[:a].replace(metaold, '<meta name="version" content="%s">' % VER) + dump(nd) + h[b:]
open(NEW, "w", encoding="utf-8").write(out)
# proof
h2 = open(NEW, encoding="utf-8").read(); a2 = h2.index(TAG) + len(TAG); b2 = h2.index("</script>", a2); d2 = json.loads(h2[a2:b2])
assert h2[:a2].replace('content="%s"' % VER, 'content="%s"' % oldv, 1) == h[:a] and h2[b2:] == h[b:], "the page outside the data block changed beyond the version"
diff = [k for k in set(d) | set(d2) if d.get(k) != d2.get(k)]
assert set(diff) <= set(changed), "unexpected keys changed: %s" % sorted(set(diff) - set(changed))
print("wrote", NEW, "| %s -> %s | data keys changed: %s | stories: %s" % (oldv, VER, sorted(diff), [(s["id"], len(s["imgs"])) for s in stories]))
