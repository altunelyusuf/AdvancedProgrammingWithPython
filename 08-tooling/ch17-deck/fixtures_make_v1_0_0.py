"""Makes the stale fixtures the chapter 17 deck checks must refuse, from the deck itself; each is the finished deck with ONE text
run (or one chart value) on ONE named part changed to something plausible that is not what Python printed or what the deck must say:
  stale_expr     slide 8: the console result 'wellknown' shown as 'well known'
  stale_table    slide 12: the key length 256 of AES-256 shown as 128 (the table is computed with pypdf)
  stale_chart    the native chart of slide 11: the stored rotation 450 shown as 451
  stale_program  slide 13: the transcript line 'ownerpw' -> OWNER_PASSWORD shown as USER_PASSWORD
  stale_code     slide 6: the program line 'reader = pypdf.PdfReader(io.BytesIO(data))' shown with data[1:]
  stale_tcap     slide 15: the transcript line 'Wrong password for tree/a_encrypted.pdf' shown with the capitals .PDF
  stale_diagram  slide 4: the diagram label 'Rotate pages' shown as 'Rotate images'
  stale_label    slide 9: 'sha256 d943896e0bd2...' removed (a LIVE result shown without saying which file hash was checked)
  stale_notexec  slide 8: the card 'NOT EXECUTED here' changed to 'Run here' (a language-model clean-up presented as if run)
  stale_once     slide 16: 'single runs' changed to 'runs' (timings without saying single run)
Each is refused by the check that owns it (deck_check, program_check, diagram_check, honesty_check); the build fails if one is not refused.
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)


def edit(dst, part, old, new):
    zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename == part:
            assert data.count(old.encode()) == 1, (part, old, data.count(old.encode()))
            data = data.replace(old.encode(), new.encode(), 1); n += 1
        zout.writestr(it, data)
    zout.close(); assert n == 1, (old, n)


def slide(n):
    return "ppt/slides/slide%d.xml" % n


f = lambda name: os.path.join(out, "fixture_stale_%s_v1_0_0.pptx" % name)
edit(f("expr"), slide(8), "<a:t>'wellknown'</a:t>", "<a:t>'well known'</a:t>")
edit(f("table"), slide(12), "<a:t>256</a:t>", "<a:t>128</a:t>")
edit(f("chart"), "ppt/charts/chart1.xml", "<c:v>450</c:v>", "<c:v>451</c:v>")
edit(f("program"), slide(13), "<a:t>'ownerpw' -&gt; OWNER_PASSWORD</a:t>", "<a:t>'ownerpw' -&gt; USER_PASSWORD</a:t>")
edit(f("code"), slide(6), "<a:t>reader = pypdf.PdfReader(io.BytesIO(data))</a:t>", "<a:t>reader = pypdf.PdfReader(io.BytesIO(data[1:]))</a:t>")
edit(f("tcap"), slide(15), "<a:t>Wrong password for tree/a_encrypted.pdf</a:t>", "<a:t>Wrong password for tree/a_encrypted.PDF</a:t>")
edit(f("diagram"), slide(4), "<a:t>Rotate pages</a:t>", "<a:t>Rotate images</a:t>")
edit(f("label"), slide(9), "sha256 d943896e0bd2... checked.", "checked.")
edit(f("notexec"), slide(8), "<a:t>NOT EXECUTED here</a:t>", "<a:t>Run here</a:t>")
edit(f("once"), slide(16), "Two single runs started together", "Two runs started together")
print("fixtures written to", out)
