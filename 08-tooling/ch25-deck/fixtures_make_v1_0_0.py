"""Makes the stale fixtures the chapter 25 deck checks must refuse, from the deck itself; each is the finished deck with ONE text run, ONE chart value or
ONE picture on ONE named part changed to something plausible that is not what Python printed, what the program saves, or what the deck must say:
  stale_expr          slide 1: the console result "'3.14.6'" of platform.python_version() changed to "'3.14.5'"
  stale_table         slide 19: the cell '2,500,522' of the race table (updates lost, free-threaded run 2) changed to '2,500,523'
  stale_chart         the native chart of slide 20: the ratio 1.13 of the standard build changed to 1.14
  stale_program       slide 12: the transcript line 'two threads, with lock: [2, 2, 2]' changed to '[2, 2, 1]'
  stale_code          slide 5: the program line 'threadObj.start()' shown as 'threadObj.run()' (token-level, in its own <a:t>)
  stale_diagram       slide 4: the diagram label 'Hand items over with a queue' shown as 'Hand items over with a pipe'
  stale_notexec       slide 11: the line 'NOT EXECUTED here' changed to 'Run here' (the real xkcd.com presented as if it had been run)
  stale_standin       slide 10: 'xkcd.com is never contacted' changed to 'xkcd.com is contacted' (the stand-in presented as the real site)
  stale_standin_local slide 10: 'a local stand-in' changed to 'a copy' (the stand-in server no longer called a local stand-in)
  stale_recorded      slide 9: 'Recorded 14 Oct 2026' changed to 'Run 14 Oct 2026' (a recorded result presented as run now)
  stale_honest_not    slide 10: the line 'Lines 1 to N (imports,' changed to 'NOT EXECUTED (imports,' on a slide the plan does not list
  stale_title         slide 1: 'never used' changed to 'used' (the title no longer says that Windows, macOS and the real xkcd.com were never used)
  stale_image_pixel   slide 11: the picture skipped.png replaced by a PNG of the same size and mode with ONE pixel changed (a stale picture)
  stale_image_swap    slide 11: the picture skipped.png replaced by therac.png of slide 12 (the wrong picture in the right place)
  stale_image_caption slide 11: the caption 'image skipped.png made by fixedCut' changed to 'made by lostCut' (a picture named for a program that did not save it)
  stale_image_loose   slide 11: the caption 'image skipped.png made by' changed to 'picture skipped.png made by' (a picture that no caption names)
  stale_photo_pixel   slide 12: the photograph therac.png replaced by a PNG with ONE pixel changed (a stale photograph)
  stale_photo_swap    slide 12: the photograph therac.png replaced by blackout.png of slide 19 (the wrong photograph in the right place)
  stale_photo_caption slide 12: the credit 'Therac 25, Unknown author' changed to 'Therac 25, Jane Doe' (a photograph credited to someone else)
  stale_photo_loose   slide 12: the caption 'photo therac.png:' changed to 'picture therac.png:' (a photograph that no caption names)
There is no stale_tcap: this deck has no panel that shows a transcript without its program, so that refusal has nothing to test.
Two more files are NOT stale and must be ACCEPTED (controls that show the pixel comparison works):
  ok_image_reencoded  slide 11: skipped.png re-encoded by Pillow with optimize=True: other bytes, the same pixels - 'pixel-identical'
  ok_photo_reencoded  slide 12: therac.png re-encoded by Pillow with compress_level=1: other bytes, the same pixels - 'pixel-identical'
Each stale one is refused by the check that owns it (deck_check, program_check, diagram_check, honesty_check); the build fails if one is not refused,
or if a control is not accepted.
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>   (needs Pillow)"""
__version__ = "1.0.0"
import io, os, re, sys, zipfile
from PIL import Image
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)


def edit(dst, part, old, new):
    """old and new are text (replaced once, which must be the only occurrence) or bytes (the whole part is replaced by new)"""
    zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename == part:
            if isinstance(new, bytes):
                data = new
            else:
                assert data.count(old.encode()) == 1, (part, old, data.count(old.encode()))
                data = data.replace(old.encode(), new.encode(), 1)
            n += 1
        zout.writestr(it, data)
    zout.close(); assert n == 1, (old, n)


def slide(n):
    return "ppt/slides/slide%d.xml" % n


def media(n, k=1):
    """the picture file of a slide: its k-th media part, as the slide's relationships name it"""
    return "ppt/media/image-%d-%d.png" % (n, k)


def png(part):
    return Image.open(io.BytesIO(zipfile.ZipFile(deck).read(part)))


def changed_pixel(im):
    """the picture with the pixel (100, 100) made different, whatever the mode"""
    im = im.copy(); v = im.getpixel((100, 100))
    im.putpixel((100, 100), (v + 1) % 256 if isinstance(v, int) else ((v[0] + 1) % 256,) + tuple(v[1:]))
    return im


f = lambda name: os.path.join(out, "fixture_%s_v1_0_0.pptx" % name)
edit(f("stale_expr"), slide(1), "<a:t>'3.14.6'</a:t>", "<a:t>'3.14.5'</a:t>")
edit(f("stale_table"), slide(19), "<a:t>2,500,522</a:t>", "<a:t>2,500,523</a:t>")
edit(f("stale_chart"), "ppt/charts/chart1.xml", "<c:v>1.13</c:v>", "<c:v>1.14</c:v>")
edit(f("stale_program"), slide(12), "<a:t>two threads, with lock: [2, 2, 2]</a:t>", "<a:t>two threads, with lock: [2, 2, 1]</a:t>")
edit(f("stale_code"), slide(5), "<a:t>threadObj.start()</a:t>", "<a:t>threadObj.run()</a:t>")
edit(f("stale_diagram"), slide(4), "Hand items over with a queue", "Hand items over with a pipe")
edit(f("stale_notexec"), slide(11), "NOT EXECUTED here", "Run here")
edit(f("stale_standin"), slide(10), "xkcd.com is never contacted", "xkcd.com is contacted")
edit(f("stale_standin_local"), slide(10), "a local stand-in", "a copy")
edit(f("stale_recorded"), slide(9), "Recorded 14 Oct 2026", "Run 14 Oct 2026")
_hid = re.search(r"Lines 1 to \d+ \(imports,", zipfile.ZipFile(deck).read(slide(10)).decode()).group(0)
edit(f("stale_honest_not"), slide(10), _hid, "NOT EXECUTED (imports,")
edit(f("stale_title"), slide(1), "never used", "used")
# pictures a program saves
b = io.BytesIO(); changed_pixel(png(media(11))).save(b, "PNG")
edit(f("stale_image_pixel"), media(11), None, b.getvalue())
edit(f("stale_image_swap"), media(11), None, zipfile.ZipFile(deck).read(media(12)))
edit(f("stale_image_caption"), slide(11), "image skipped.png made by fixedCut_v1_0_0.py", "image skipped.png made by lostCut_v1_0_0.py")
edit(f("stale_image_loose"), slide(11), "image skipped.png made by", "picture skipped.png made by")
orig = zipfile.ZipFile(deck).read(media(11)); b = io.BytesIO(); png(media(11)).save(b, "PNG", optimize=True)
assert b.getvalue() != orig, "the re-encoded picture must have other bytes than the original"
edit(f("ok_image_reencoded"), media(11), None, b.getvalue())
# photographs
b = io.BytesIO(); changed_pixel(png(media(12))).save(b, "PNG")
edit(f("stale_photo_pixel"), media(12), None, b.getvalue())
edit(f("stale_photo_swap"), media(12), None, zipfile.ZipFile(deck).read(media(19)))
edit(f("stale_photo_caption"), slide(12), "Therac 25, Unknown author", "Therac 25, Jane Doe")
edit(f("stale_photo_loose"), slide(12), "photo therac.png:", "picture therac.png:")
orig = zipfile.ZipFile(deck).read(media(12)); b = io.BytesIO(); png(media(12)).save(b, "PNG", compress_level=1)
assert b.getvalue() != orig, "the re-encoded photograph must have other bytes than the original"
edit(f("ok_photo_reencoded"), media(12), None, b.getvalue())
print("made 20 stale fixtures and 2 controls in", out)
