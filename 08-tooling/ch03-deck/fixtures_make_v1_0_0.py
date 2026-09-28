"""Makes the two stale fixtures the deck checks must refuse, from the deck itself: one with an expression result edited
(range(5) shown as five values starting at 1), one with a program transcript edited (Total: 12 shown as Total: 13).
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, shutil, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
def edit(dst, old, new):
    zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename.startswith("ppt/slides/slide") and it.filename.endswith(".xml") and old.encode() in data: data = data.replace(old.encode(), new.encode()); n += 1
        zout.writestr(it, data)
    zout.close(); assert n == 1, (old, n)
edit(os.path.join(out, "fixture_stale_expr_v1_0_0.pptx"), "[0, 1, 2, 3, 4]", "[1, 2, 3, 4, 5]")
edit(os.path.join(out, "fixture_stale_program_v1_0_0.pptx"), "Total: 12", "Total: 13")
print("fixtures written to", out)
