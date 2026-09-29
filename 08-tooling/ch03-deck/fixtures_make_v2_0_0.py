"""Makes the three stale fixtures the version 2 deck checks must refuse, from the deck itself: an expression result edited
(range(10) shown as range(1, 10)), a program transcript edited (the total 12 shown as 13), and a visual value edited (a trace cell of the
guessing program, Guess: 15 / too high shown as too low). Usage: fixtures_make_v2_0_0.py <deck.pptx> <out-dir>"""
__version__ = "2.0.0"
import os, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
def edit(dst, old, new):
    zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename.startswith("ppt/slides/slide") and it.filename.endswith(".xml") and old.encode() in data: data = data.replace(old.encode(), new.encode()); n += 1
        zout.writestr(it, data)
    zout.close(); assert n == 1, (old, n)
edit(os.path.join(out, "fixture_stale_expr_v2_0_0.pptx"), "range(0, 10)</a:t>", "range(1, 10)</a:t>")
edit(os.path.join(out, "fixture_stale_program_v2_0_0.pptx"), "Total: 12", "Total: 13")
edit(os.path.join(out, "fixture_stale_visual_v2_0_0.pptx"), "Guess: 15 / too high", "Guess: 15 / too low")
print("fixtures written to", out)
