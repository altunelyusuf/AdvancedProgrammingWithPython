"""Makes the four stale fixtures the chapter 7 deck checks must refuse, from the deck itself: a console result edited
({1: 'bool'} shown as {1: 'int'}), a program transcript edited (23 different characters shown as 24), a chart value edited
(the 13 spaces shown as 12) and a table cell edited (the white queen wQ on d1 shown as bQ).
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)


def edit(dst, old, new):
    zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        ok = it.filename.endswith(".xml") and (it.filename.startswith("ppt/slides/slide") or it.filename.startswith("ppt/charts/chart"))
        if ok and old.encode() in data and n == 0:
            data = data.replace(old.encode(), new.encode(), 1); n += 1
        zout.writestr(it, data)
    zout.close(); assert n == 1, (old, n)


edit(os.path.join(out, "fixture_stale_expr_v1_0_0.pptx"), "<a:t>{1: 'bool'}</a:t>", "<a:t>{1: 'int'}</a:t>")
edit(os.path.join(out, "fixture_stale_program_v1_0_0.pptx"), "23 different characters", "24 different characters")
edit(os.path.join(out, "fixture_stale_chart_v1_0_0.pptx"), "<c:v>13</c:v>", "<c:v>12</c:v>")
edit(os.path.join(out, "fixture_stale_table_v1_0_0.pptx"), "<a:t>wQ</a:t>", "<a:t>bQ</a:t>")
print("fixtures written to", out)
