"""Makes the stale fixtures the chapter 21 deck checks must refuse, from the deck itself; each is the finished deck with ONE text run, ONE chart value or
ONE picture on ONE named part changed to something plausible that is not what Python printed, what the program saves, or what the deck must say:
  stale_expr          slide 7: the console result "(6, 5)" of crop((3, 1, 9, 6)).size changed to "(5, 6)"
  stale_table         slide 21: the cell 'PieContainer' of the environments table changed to 'tuple'
  stale_chart         the native chart of slide 12: the 28.9 kilobytes of the JPEG at quality 10 changed to 29.9
  stale_program       slide 9: the transcript line '24 pastes, the last at (690, 1075)' changed to (690, 1076)
  stale_code          slide 8: the program text "'past the edge:'" shown as "'past edge:'"
  stale_tcap          slide 18: the transcript line of a second program, 60 tiles, shown as 61 tiles
  stale_diagram       slide 4: the diagram label 'Crop a rectangle with a box tuple' shown as 'Cut a rectangle with a box tuple'
  stale_notexec       slide 11: the card 'NOT EXECUTED here' changed to 'Run here' (a Windows/macOS statement presented as if it had been run)
  stale_standin       slide 19: 'Virtual display:' changed to 'Real display:' (output of the virtual display presented as a real screen's)
  stale_standin_local slide 19: 'a local stand-in for a screen' changed to 'a screen' (the virtual display no longer called a local stand-in)
  stale_recorded      slide 20: 'Recorded 13 Oct 2026' changed to 'Run 13 Oct 2026' (a recorded result presented as run now)
  stale_honest_not    slide 8: the line 'Lines 1 to 41 (imports,' changed to 'NOT EXECUTED (imports,' on a slide the plan does not list
  stale_title         slide 1: 'never used' changed to 'used' (the title no longer says that Windows, macOS and a real screen were never used)
  stale_image_pixel   slide 15: the picture drawing.png replaced by a PNG of the same size and mode with ONE pixel changed (a stale picture)
  stale_image_swap    slide 20: the picture line.png replaced by scatter.png (the wrong graph in the right place)
  stale_image_caption slide 15: the caption 'image drawing.png made by drawingPngCut' changed to 'made by plotsFourCut' (a picture named for a program that did not save it)
  stale_image_loose   slide 6: the caption 'image swatches.png made by' changed to 'picture swatches.png made by' (a picture that no caption names)
One more file is NOT stale and must be ACCEPTED (a control that shows the pixel comparison works):
  ok_image_reencoded  slide 15: drawing.png re-encoded by Pillow with optimize=True: other bytes, the same pixels - 'pixel-identical'
Each stale one is refused by the check that owns it (deck_check, program_check, diagram_check, honesty_check); the build fails if one is not refused,
or if the control is not accepted.
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>   (needs Pillow)"""
__version__ = "1.0.0"
import io, os, sys, zipfile
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


f = lambda name: os.path.join(out, "fixture_%s_v1_0_0.pptx" % name)
edit(f("stale_expr"), slide(7), "<a:t>(6, 5)</a:t>", "<a:t>(5, 6)</a:t>")
edit(f("stale_table"), slide(21), "<a:t>PieContainer</a:t>", "<a:t>tuple</a:t>")
edit(f("stale_chart"), "ppt/charts/chart1.xml", "<c:v>28.9</c:v>", "<c:v>29.9</c:v>")
edit(f("stale_program"), slide(9), "24 pastes, the last at (690, 1075)", "24 pastes, the last at (690, 1076)")
edit(f("stale_code"), slide(8), "<a:t>'past the edge:'</a:t>", "<a:t>'past edge:'</a:t>")
edit(f("stale_tcap"), slide(18), "((120, 500), 60)", "((120, 500), 61)")
edit(f("stale_diagram"), slide(4), "Crop a rectangle with a box tuple", "Cut a rectangle with a box tuple")
edit(f("stale_notexec"), slide(11), "NOT EXECUTED here", "Run here")
edit(f("stale_standin"), slide(19), "Virtual display:", "Real display:")
edit(f("stale_standin_local"), slide(19), "a local stand-in for a screen", "a screen")
edit(f("stale_recorded"), slide(20), "Recorded 13 Oct 2026", "Run 13 Oct 2026")
edit(f("stale_honest_not"), slide(8), "Lines 1 to 41 (imports,", "NOT EXECUTED (imports,")
edit(f("stale_title"), slide(1), "never used", "used")
# pictures
im = png(media(15)).copy(); im.putpixel((100, 100), (1, 2, 3, 255)); b = io.BytesIO(); im.save(b, "PNG")
edit(f("stale_image_pixel"), media(15), None, b.getvalue())
edit(f("stale_image_swap"), media(20, 1), None, zipfile.ZipFile(deck).read(media(20, 2)))
edit(f("stale_image_caption"), slide(15), "image drawing.png made by drawingPngCut_v1_0_0.py", "image drawing.png made by plotsFourCut_v1_0_0.py")
edit(f("stale_image_loose"), slide(6), "image swatches.png made by", "picture swatches.png made by")
orig = zipfile.ZipFile(deck).read(media(15)); b = io.BytesIO(); png(media(15)).save(b, "PNG", optimize=True)
assert b.getvalue() != orig, "the re-encoded picture must have other bytes than the original"
edit(f("ok_image_reencoded"), media(15), None, b.getvalue())
print("made 16 stale fixtures and 1 control in", out)
