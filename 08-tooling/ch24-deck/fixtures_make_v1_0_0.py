"""Makes the stale fixtures the chapter 24 deck checks must refuse, from the deck itself; each is the finished deck with ONE text run, ONE chart value or
ONE picture on ONE named part changed to something plausible that is not what Python printed, what the program saves, or what the deck must say:
  stale_expr          slide 4: the console result "'/usr/bin/espeak-ng'" of shutil.which('espeak-ng') changed to "'/usr/bin/espeak'"
  stale_table         slide 23: the cell '34 of 46' of the configurations table changed to '36 of 46'
  stale_chart         the native chart of slide 9: the 3.62 seconds of rate 150 changed to 3.63
  stale_program       slide 9: the transcript line '150 -> 3.62 s' changed to '150 -> 3.63 s'
  stale_code          slide 6: the program text 'pinned' shown as 'pinnec' (the label of the pinned interpreter in the loop)
  stale_diagram       slide 4: the diagram label 'Save speech as a WAV file' shown as 'Save speech as an MP3 file'
  stale_notexec       slide 5: the line 'NOT EXECUTED here' changed to 'Run here' (SAPI5, macOS and the cloud presented as if they had been run)
  stale_standin       slide 7: 'No sound card:' changed to 'A sound card:' (output written to WAV files presented as if it had been played)
  stale_standin_local slide 7: 'a local stand-in for a loudspeaker' changed to 'a loudspeaker' (the WAV file no longer called a local stand-in)
  stale_standin_remote slide 19: 'stands in for YouTube' changed to 'is YouTube' (archive.org presented as YouTube) - a seventeenth fixture, for the kind this chapter adds
  stale_recorded      slide 4: 'Recorded 14 Oct 2026' changed to 'Run 14 Oct 2026' (a recorded result presented as run now)
  stale_honest_not    slide 10: the line 'Lines 1 to N (imports,' changed to 'NOT EXECUTED (imports,' on a slide the plan does not list
  stale_title         slide 1: 'never used' changed to 'used' (the title no longer says that Windows, macOS, a microphone, a GPU and YouTube were never used)
  stale_image_pixel   slide 10: the picture hello.png replaced by a PNG of the same size and mode with ONE pixel changed (a stale picture)
  stale_image_swap    slide 10: the picture hello.png replaced by audio16k.png of slide 14 (the wrong picture in the right place)
  stale_image_caption slide 10: the caption 'image hello.png made by wavCut' changed to 'made by ffmpegCut' (a picture named for a program that did not save it)
  stale_image_loose   slide 10: the caption 'image hello.png made by' changed to 'picture hello.png made by' (a picture that no caption names)
There is no stale_tcap: no panel of this deck's slides is a transcript that stands for a program whose code is on another slide, except where the transcript panel sits beside its code panel,
and that pairing is covered by stale_program.
One more file is NOT stale and must be ACCEPTED (a control that shows the pixel comparison works):
  ok_image_reencoded  slide 10: hello.png re-encoded by Pillow with optimize=True: other bytes, the same pixels - 'pixel-identical'
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
    """the picture with the pixel (100, 30) made different, whatever the mode"""
    im = im.copy(); v = im.getpixel((100, 30))
    im.putpixel((100, 30), (v + 1) % 256 if isinstance(v, int) else ((v[0] + 1) % 256,) + tuple(v[1:]))
    return im


f = lambda name: os.path.join(out, "fixture_%s_v1_0_0.pptx" % name)
edit(f("stale_expr"), slide(4), "<a:t>'/usr/bin/espeak-ng'</a:t>", "<a:t>'/usr/bin/espeak'</a:t>")
edit(f("stale_table"), slide(23), "<a:t>34 of 46</a:t>", "<a:t>36 of 46</a:t>")
edit(f("stale_chart"), "ppt/charts/chart1.xml", "<c:v>3.62</c:v>", "<c:v>3.63</c:v>")
edit(f("stale_program"), slide(9), "150 -&gt; 3.62 s", "150 -&gt; 3.63 s")
edit(f("stale_code"), slide(6), "<a:t>'pinned'</a:t>", "<a:t>'pinnec'</a:t>")
edit(f("stale_diagram"), slide(4), "Save speech as a WAV file", "Save speech as an MP3 file")
edit(f("stale_notexec"), slide(5), "NOT EXECUTED here", "Run here")
edit(f("stale_standin"), slide(7), "No sound card:", "A sound card:")
edit(f("stale_standin_local"), slide(7), "a local stand-in for a loudspeaker", "a loudspeaker")
edit(f("stale_standin_remote"), slide(19), "stands in for YouTube", "is YouTube")
edit(f("stale_recorded"), slide(4), "Recorded 14 Oct 2026", "Run 14 Oct 2026")
_hid = re.search(r"Lines 1 to \d+ \(imports,", zipfile.ZipFile(deck).read(slide(10)).decode()).group(0)
edit(f("stale_honest_not"), slide(10), _hid, "NOT EXECUTED (imports,")
edit(f("stale_title"), slide(1), "never used", "used")
# pictures
b = io.BytesIO(); changed_pixel(png(media(10))).save(b, "PNG")
edit(f("stale_image_pixel"), media(10), None, b.getvalue())
edit(f("stale_image_swap"), media(10), None, zipfile.ZipFile(deck).read(media(14)))
edit(f("stale_image_caption"), slide(10), "image hello.png made by wavCut_v1_0_0.py", "image hello.png made by ffmpegCut_v1_0_0.py")
edit(f("stale_image_loose"), slide(10), "image hello.png made by", "picture hello.png made by")
orig = zipfile.ZipFile(deck).read(media(10)); b = io.BytesIO(); png(media(10)).save(b, "PNG", optimize=True)
assert b.getvalue() != orig, "the re-encoded picture must have other bytes than the original"
edit(f("ok_image_reencoded"), media(10), None, b.getvalue())
print("made 17 stale fixtures and 1 control in", out)
