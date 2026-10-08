"""Makes the stale fixtures that the chapter 6 deck checks must refuse, so each gate has its own proof that it can fail. Every
fixture is the finished deck with ONE edit and nothing else touched:
  fixture_stale_expr_v2_0_0.pptx      a console result edited ([0, 3, 6, 9] shown as [0, 3, 6, 8])      -> deck_check_v1_0_1.py
  fixture_stale_program_v2_0_0.pptx   a program transcript edited (81.48 % shown as 81.84 %)              -> program_check_v2_0_1.py
  fixture_stale_code_v2_0_0.pptx      a program line edited (comment line changed by one letter)     -> program_check_v2_0_1.py
  fixture_cue_notes_v2_0_0.pptx       a speaker note given a presenter cue ("SAY: " in front of it)      -> deck_notes_check_v1_0_0.py
Chapter 5's fixtures_make_v1_0_0.py, adapted: same mechanism, this chapter's printed values.
Usage: fixtures_make_v2_0_0.py <deck.pptx> <out-dir>"""
__version__ = "2.0.0"
import os, re, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)


def edit(dst, member_re, old, new):
    zin = zipfile.ZipFile(deck)
    zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        if re.match(member_re, it.filename) and old.encode() in data and n == 0:
            data = data.replace(old.encode(), new.encode(), 1)
            n += 1
        zout.writestr(it, data)
    zout.close()
    assert n == 1, (old, n)


S = r"ppt/slides/slide\d+\.xml$"
edit(os.path.join(out, "fixture_stale_expr_v2_0_0.pptx"), S, "<a:t>[0, 3, 6, 9]</a:t>", "<a:t>[0, 3, 6, 8]</a:t>")
edit(os.path.join(out, "fixture_stale_program_v2_0_0.pptx"), S, "81.48 %", "81.84 %")
edit(os.path.join(out, "fixture_stale_code_v2_0_0.pptx"), S, "same on every run", "same on every ruin")
edit(os.path.join(out, "fixture_cue_notes_v2_0_0.pptx"), r"ppt/notesSlides/notesSlide4\.xml$", "<a:t>", "<a:t>SAY: ")
print("fixtures written to", out)
