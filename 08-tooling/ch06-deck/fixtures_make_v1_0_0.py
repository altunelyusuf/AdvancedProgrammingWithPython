"""Makes the four stale fixtures the chapter 6 deck checks must refuse, from the deck itself: an expression result edited (the shallow-copy identity result (True, False) shown as
(False, False)), a program transcript edited (the Magic 8 Ball answer 'Reply hazy try again' shown as 'Signs point to yes'), a reference-picture value edited (a list item '42' in the copy
picture shown as '43') and a Matrix life-table cell edited (a printed digit 1 shown as 7).
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, re, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
def edit(dst, old, new, slide=None):
    zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        if re.match(r"ppt/slides/slide%s\.xml$" % (slide or r"\d+"), it.filename) and old.encode() in data and n == 0: data = data.replace(old.encode(), new.encode(), 1); n += 1
        zout.writestr(it, data)
    zout.close(); assert n == 1, (old, n)
edit(os.path.join(out, "fixture_stale_expr_v1_0_0.pptx"), "(True, False)", "(False, False)")
edit(os.path.join(out, "fixture_stale_program_v1_0_0.pptx"), "<a:t>Reply hazy try again</a:t>", "<a:t>Signs point to yes</a:t>")
edit(os.path.join(out, "fixture_stale_visual_v1_0_0.pptx"), "<a:t>42</a:t>", "<a:t>43</a:t>")
edit(os.path.join(out, "fixture_stale_matrix_v1_0_0.pptx"), "<a:t>1</a:t>", "<a:t>7</a:t>", slide="28")
print("fixtures written to", out)
