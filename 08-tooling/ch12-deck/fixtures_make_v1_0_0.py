"""Makes the stale fixtures the chapter 12 deck checks must refuse, from the deck itself: a console result edited
(a boolean shown with its sense flipped) and a program transcript edited (the launcher's mode after chmod u+x shown
without its execute bit). Chapter 12 ships no native chart or table, so there are no chart/table fixtures to make.
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)


def edit(dst, old, new):
    zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        ok = it.filename.endswith(".xml") and it.filename.startswith("ppt/slides/slide")
        if ok and old.encode() in data and n == 0:
            data = data.replace(old.encode(), new.encode(), 1); n += 1
        zout.writestr(it, data)
    zout.close(); assert n == 1, (old, n)


edit(os.path.join(out, "fixture_stale_expr_v1_0_0.pptx"), "<a:t>True</a:t>", "<a:t>False</a:t>")
edit(os.path.join(out, "fixture_stale_program_v1_0_0.pptx"),
     "mode after chmod u+x: -rwxr--r--", "mode after chmod u+x: -rw-r--r--")
print("fixtures written to", out)
