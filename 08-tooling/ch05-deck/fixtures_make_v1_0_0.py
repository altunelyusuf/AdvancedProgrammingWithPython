"""Makes the four stale fixtures the chapter 5 deck checks must refuse, from the deck itself: an expression result edited (issubclass(AssertionError, Exception)
shown as False), a program transcript edited (the sum 5342 shown as 5324), a debugger value edited (x = 5 at a stop shown as x = 6) and a logging-matrix cell edited
(a shown cell shown as hidden). Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, re, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
def edit(dst, old, new, name_hint=None):
    zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename.startswith("ppt/slides/slide") and it.filename.endswith(".xml") and old.encode() in data and n == 0: data = data.replace(old.encode(), new.encode(), 1); n += 1
        zout.writestr(it, data)
    zout.close(); assert n == 1, (old, n)
edit(os.path.join(out, "fixture_stale_expr_v1_0_0.pptx"), "<a:t>True</a:t>", "<a:t>False</a:t>")
edit(os.path.join(out, "fixture_stale_program_v1_0_0.pptx"), "The sum is 5342", "The sum is 5324")
edit(os.path.join(out, "fixture_stale_debugger_v1_0_0.pptx"), "<a:t>x = 5</a:t>", "<a:t>x = 6</a:t>")
edit(os.path.join(out, "fixture_stale_matrix_v1_0_0.pptx"), "<a:t>shown</a:t>", "<a:t>hidden</a:t>")
print("fixtures written to", out)
