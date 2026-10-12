"""Makes the stale fixtures the chapter 13 deck checks must refuse, from the deck itself; each is the finished deck with ONE text
run on ONE named slide changed to something that was true once or is plausible but is not what Python printed:
  stale_expr     slide 5: the console result of can_fetch for pypi.org's search page, False (3.14.6), shown as True (3.14.0-3.14.4)
  stale_program  slide 15: the transcript line '8 links found; 5 opened' shown as '8 links found; 6 opened'
  stale_code     slide 20: the program line password_elem.submit() shown as password_elem.click()
  stale_tcap     slide 11: the live transcript line 401 shown as 403
  stale_diagram  slide 9: the diagram label ... 'wb' shown as ... 'rb'
Each is refused by the check that owns it (deck_check, program_check, diagram_check); the build fails if one is not refused.
Usage: fixtures_make_v1_0_0.py <deck.pptx> <out-dir>"""
__version__ = "1.0.0"
import os, sys, zipfile
deck, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)


def edit(dst, slide, old, new):
    zin = zipfile.ZipFile(deck); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); n = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename == "ppt/slides/slide%d.xml" % slide:
            assert data.count(old.encode()) == 1, (slide, old, data.count(old.encode()))
            data = data.replace(old.encode(), new.encode(), 1); n += 1
        zout.writestr(it, data)
    zout.close(); assert n == 1, (old, n)


edit(os.path.join(out, "fixture_stale_expr_v1_0_0.pptx"), 5, "<a:t>False</a:t>", "<a:t>True</a:t>")
edit(os.path.join(out, "fixture_stale_program_v1_0_0.pptx"), 15, "<a:t>8 links found; 5 opened</a:t>", "<a:t>8 links found; 6 opened</a:t>")
edit(os.path.join(out, "fixture_stale_code_v1_0_0.pptx"), 20, "<a:t>password_elem.submit()</a:t>", "<a:t>password_elem.click()</a:t>")
edit(os.path.join(out, "fixture_stale_tcap_v1_0_0.pptx"), 11, "<a:t>401 application/json; charset=utf-8</a:t>", "<a:t>403 application/json; charset=utf-8</a:t>")
edit(os.path.join(out, "fixture_stale_diagram_v1_0_0.pptx"), 9, "write binary mode with 'wb'", "write binary mode with 'rb'")
print("fixtures written to", out)
