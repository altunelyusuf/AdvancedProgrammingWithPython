"""Makes the stale fixtures the chapter 18 deck checks must refuse, from the deck itself; each is the finished deck with ONE text
run (or one chart value) on ONE named part changed to something plausible that is not what Python printed or what the deck must say:
  stale_expr       slide 8: the console result 'Error: field...' of the bytes reader changed to a different message (Appendix B slide)
  stale_table      slide 12: the table cell for QUOTE_ALL changed to the output of QUOTE_MINIMAL
  stale_chart      the native chart of slide 22: the 407 characters of compact XML shown as 408
  stale_program    slide 17: the transcript line {"t": [1, 2], ... changed so the tuple stays a tuple in the loads line
  stale_code       slide 10: the program line 'back = io.StringIO(data.decode(), newline='')' shown with newline='\\n'
  stale_tcap       slide 18: the transcript line 'long integer: Exceeds the limit (4300 digits)' shown with 4400
  stale_diagram    slide 6: the diagram label 'Loop over the reader in a for loop' shown as 'Loop over the writer in a for loop'
  stale_notexec    slide 10: the card 'NOT EXECUTED here' changed to 'Run here' (Excel presented as if run)
  stale_once       slide 7: the card 'Single run, research' changed to 'Run, research' (a measurement without saying single run)
  stale_emulated   slide 10: the card 'EMULATED, not a Windows computer' changed to 'On a Windows computer' (an emulation presented as Windows)
  stale_honest_not slide 12: a card heading changed to 'NOT EXECUTED' on a slide the plan does not list
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

edit(f("expr"), slide(8), "Error: iterator should return strings, not bytes (the file should be opened in text mode)",
     "Error: iterator should return strings, not bytes (open the file in text mode)")
edit(f("table"), slide(12), """'"a b","c,d","7","",""\\r\\n'""", """'"a b","c,d",7,"",""\\r\\n'""".replace('7,"",""', '7,,'))
edit(f("chart"), "ppt/charts/chart1.xml", "<c:v>407</c:v>", "<c:v>408</c:v>")
edit(f("program"), slide(17), '{"t": [1, 2], "1": "a", "null": "c"}', '{"t": [1, 2], "1": "a", "null": "d"}')
edit(f("code"), slide(10), "back = io.StringIO(data.decode(), newline=", "back = io.StringIO(data.decode(), newlines=")
edit(f("tcap"), slide(18), "long integer: Exceeds the limit (4300 digits)", "long integer: Exceeds the limit (4400 digits)")
edit(f("diagram"), slide(6), "Loop over the reader in a for loop", "Loop over the writer in a for loop")
edit(f("notexec"), slide(10), "NOT EXECUTED here", "Run here")
edit(f("once"), slide(7), "Single run, research", "Run, research")
edit(f("emulated"), slide(10), "EMULATED, not a Windows computer", "On a Windows computer")
edit(f("honest_not"), slide(12), "The row written", "NOT EXECUTED")
print("made 11 stale fixtures in", out)
