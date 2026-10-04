"""Reads a finished deck with python-pptx and refuses it when something would not be readable on the screen.

Four questions are asked of every slide, because a deck that passes the code checks can still be unusable:
  1. does any shape hang off the 10 x 5.625 inch page;
  2. does any text box need more height than it has, estimated from the real font size, the real box width and the
     real text, using the average character width of the three fonts the house style uses (Courier New is a monospaced
     font, so 0.60 em exactly; Calibri and Cambria are measured averages for running text);
  3. does any table reach past the bottom of the page;
  4. does every slide carry speaker notes.
It also prints the slide count and, with --verbose, the longest text box of each slide, so that the author can compare
what was intended with what was built.

Usage: layout_check_v1_0_0.py <deck.pptx> [expected-slide-count] [--verbose]
Exits 1 on any overflow, any off-page shape or any slide without notes.
"""
__version__ = "1.0.0"
import sys
from pptx import Presentation
from pptx.util import Emu

EMU_IN = 914400.0
PT_IN = 72.0
# average advance width as a fraction of the font size, for the three faces the house style uses
WIDTH = {"Courier New": 0.600, "Calibri": 0.479, "Cambria": 0.502, None: 0.500}
LINE = 1.22          # line height as a multiple of the font size, single spacing
TOL = 1.04           # a box may be filled to 104 per cent before it is called an overflow

def frame_need(shape):
    """estimated height in points that this shape's text needs, and the longest paragraph it holds"""
    tf = shape.text_frame
    inset = (tf.margin_left or 0) + (tf.margin_right or 0)
    w_pt = max(1.0, (shape.width - inset) / EMU_IN * PT_IN)
    need, longest = 0.0, ""
    for p in tf.paragraphs:
        txt = "".join(r.text for r in p.runs)
        size = next((r.font.size.pt for r in p.runs if r.font.size), None) or (p.font.size.pt if p.font.size else 18.0)
        face = next((r.font.name for r in p.runs if r.font.name), None)
        cpl = max(1, int(w_pt / (WIDTH.get(face, WIDTH[None]) * size)))
        lines = max(1, -(-len(txt) // cpl))
        need += lines * size * LINE + (p.space_after.pt if p.space_after else 0)
        if len(txt) > len(longest): longest = txt
    return need, longest

def check(path, expected=None, verbose=False):
    pres = Presentation(path)
    W, H = pres.slide_width / EMU_IN, pres.slide_height / EMU_IN
    bad = []
    for i, s in enumerate(pres.slides, 1):
        if not (s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip()):
            bad.append((i, "no speaker notes", ""))
        widest = ("", 0.0, 0.0)
        for sh in s.shapes:
            l, t = sh.left / EMU_IN, sh.top / EMU_IN
            r, b = l + sh.width / EMU_IN, t + sh.height / EMU_IN
            if l < -0.01 or t < -0.01 or r > W + 0.01 or b > H + 0.01:
                bad.append((i, "off page", "%s at %.2f,%.2f to %.2f,%.2f" % (sh.shape_type, l, t, r, b)))
            if sh.has_table:
                th = sum(row.height for row in sh.table.rows) / EMU_IN
                if t + th > H + 0.01: bad.append((i, "table past the page", "%.2f in tall from %.2f" % (th, t)))
                continue
            if not sh.has_text_frame or not sh.text_frame.text.strip(): continue
            need, longest = frame_need(sh)
            have = sh.height / EMU_IN * PT_IN
            if need > have * TOL:
                bad.append((i, "text overflows its box", "needs %.0f pt in %.0f pt: %r" % (need, have, longest[:70])))
            if need / have > widest[2]: widest = (longest, need, need / have)
        if verbose: print("  slide %2d  fullest box %3.0f%%  %r" % (i, widest[2] * 100, widest[0][:60]))
    n = len(pres.slides)
    print("%d slides, %.1f x %.1f in; %d layout problem(s)" % (n, W, H, len(bad)))
    if expected is not None and n != int(expected):
        bad.append((0, "slide count", "expected %s, built %d" % (expected, n)))
    for b in bad: print("  REFUSED slide %d: %s - %s" % b)
    return 1 if bad else 0

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if x != "--verbose"]
    sys.exit(check(a[0], a[1] if len(a) > 1 else None, "--verbose" in sys.argv))
