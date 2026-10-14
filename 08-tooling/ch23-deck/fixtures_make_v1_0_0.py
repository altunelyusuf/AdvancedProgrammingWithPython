"""Makes the stale fixtures the chapter 23 deck checks must refuse, from the deck itself; each is the finished deck with ONE text run, ONE chart value or
ONE picture on ONE named part changed to something plausible that is not what Python printed, what the program saves, or what the deck must say:
  stale_expr          slide 4: the console result "(3, 14)" of sys.version_info[:2] changed to "(3, 13)"
  stale_table         slide 23: the cell '41 of 80' of the configurations table changed to '42 of 80'
  stale_chart         the native chart of slide 9: the 21 motion events of a move of one second changed to 22
  stale_program       slide 9: the transcript line 'duration=0.5): 11 motion events' changed to 12
  stale_code          slide 6: the program line "print('click :', btns(o))" shown as "print('clock :', btns(o))"
  stale_diagram       slide 4: the diagram label 'Move the mouse with moveTo()' shown as 'Move the mouse with moveRel()'
  stale_notexec       slide 5: the line 'NOT EXECUTED here' changed to 'Run here' (Windows and macOS presented as if they had been run)
  stale_standin       slide 22: 'Virtual display:' changed to 'Real display:' (output of the virtual display presented as a real screen's)
  stale_standin_local slide 22: 'a local stand-in for a screen' changed to 'a screen' (the virtual display no longer called a local stand-in)
  stale_recorded      slide 4: 'Recorded 13 Oct 2026' changed to 'Run 13 Oct 2026' (a recorded result presented as run now)
  stale_honest_not    slide 10: the line 'Lines 1 to N (imports,' changed to 'NOT EXECUTED (imports,' on a slide the plan does not list
  stale_title         slide 1: 'never used' changed to 'used' (the title no longer says that Windows, macOS and a real screen were never used)
  stale_image_pixel   slide 11: the picture spiral.png replaced by a PNG of the same size and mode with ONE pixel changed (a stale picture)
  stale_image_swap    slide 11: the picture spiral.png replaced by screen.png of slide 14 (the wrong picture in the right place)
  stale_image_caption slide 11: the caption 'image spiral.png made by dragCut' changed to 'made by shotCut' (a picture named for a program that did not save it)
  stale_image_loose   slide 11: the caption 'image spiral.png made by' changed to 'picture spiral.png made by' (a picture that no caption names)
There is no stale_tcap: this deck has no panel that shows a transcript without its program, so that refusal has nothing to test.
One more file is NOT stale and must be ACCEPTED (a control that shows the pixel comparison works):
  ok_image_reencoded  slide 11: spiral.png re-encoded by Pillow with optimize=True: other bytes, the same pixels - 'pixel-identical'
Each stale one is refused by the check that owns it (deck_check, program_check, diagram_check, honesty_check); the build fails if one is not refused,
or if the control is not accepted.
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
edit(f("stale_expr"), slide(4), "<a:t>(3, 14)</a:t>", "<a:t>(3, 13)</a:t>")
edit(f("stale_table"), slide(23), "<a:t>41 of 80</a:t>", "<a:t>42 of 80</a:t>")
edit(f("stale_chart"), "ppt/charts/chart1.xml", "<c:v>21</c:v>", "<c:v>22</c:v>")
edit(f("stale_program"), slide(9), "duration=0.5): 11 motion events", "duration=0.5): 12 motion events")
edit(f("stale_code"), slide(6), "<a:t>'click :'</a:t>", "<a:t>'clock :'</a:t>")
edit(f("stale_diagram"), slide(4), "Move the mouse with moveTo()", "Move the mouse with moveRel()")
edit(f("stale_notexec"), slide(5), "NOT EXECUTED here", "Run here")
edit(f("stale_standin"), slide(22), "Virtual display:", "Real display:")
edit(f("stale_standin_local"), slide(22), "a local stand-in for a screen", "a screen")
edit(f("stale_recorded"), slide(4), "Recorded 13 Oct 2026", "Run 13 Oct 2026")
_hid = re.search(r"Lines 1 to \d+ \(imports,", zipfile.ZipFile(deck).read(slide(10)).decode()).group(0)
edit(f("stale_honest_not"), slide(10), _hid, "NOT EXECUTED (imports,")
edit(f("stale_title"), slide(1), "never used", "used")
# pictures
b = io.BytesIO(); changed_pixel(png(media(11))).save(b, "PNG")
edit(f("stale_image_pixel"), media(11), None, b.getvalue())
edit(f("stale_image_swap"), media(11), None, zipfile.ZipFile(deck).read(media(14)))
edit(f("stale_image_caption"), slide(11), "image spiral.png made by dragCut_v1_0_0.py", "image spiral.png made by shotCut_v1_0_0.py")
edit(f("stale_image_loose"), slide(11), "image spiral.png made by", "picture spiral.png made by")
orig = zipfile.ZipFile(deck).read(media(11)); b = io.BytesIO(); png(media(11)).save(b, "PNG", optimize=True)
assert b.getvalue() != orig, "the re-encoded picture must have other bytes than the original"
edit(f("ok_image_reencoded"), media(11), None, b.getvalue())
print("made 16 stale fixtures and 1 control in", out)
