"""Makes the two stale fixtures the deck checks must refuse: an expression result edited (type(None).__name__ shown as NoneTypo) and a program transcript edited (the 3.14 UnboundLocalError message replaced by the old wording).
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
edit(os.path.join(out, "fixture_stale_expr_v1_0_0.pptx"), "'NoneType'", "'NoneTypo'")
edit(os.path.join(out, "fixture_stale_program_v1_0_0.pptx"), "cannot access local variable", "referenced before assignment")
print("fixtures written to", out)
