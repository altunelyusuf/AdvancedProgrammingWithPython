"""Makes the stale fixtures the chapter 20 deck checks must refuse, from the deck itself; each is the finished deck with ONE text
run (or one chart value) on ONE named part changed to something plausible that is not what Python printed or what the deck must say:
  stale_expr          slide 9: the console result "('', 'real@example.com')" changed to "('', 'evil@example.net')"
  stale_table         slide 15: the cell 'lowest' of the interpreters table changed to 'TLS 1.2'
  stale_chart         the native chart of slide 21: the 47.6 bits changed to 47.7
  stale_program       slide 7: the transcript line 'America/Chicago  2026-12-11 08:48:48' changed to 08:48:49
  stale_code          slide 12: the program text "'TLS seen:'" shown as "'TLS saw:'"
  stale_tcap          slide 13: the transcript line 'raised; stored: 1' of a second program shown as 'raised; stored: 2'
  stale_diagram       slide 5: the diagram label 'Call ezgmail.init()' shown as 'Call ezgmail.login()'
  stale_notexec       slide 6: the card 'NOT EXECUTED here' changed to 'Run here' (a Gmail result presented as if it had been run)
  stale_standin_gmail slide 7: 'Stand-in for Gmail:' changed to 'Real Gmail:' (output of the stand-in presented as Gmail's)
  stale_standin_local slide 12: 'a local stand-in; Gmail' changed to 'a server; Gmail' (the SMTP server no longer called a local stand-in)
  stale_recorded      slide 16: 'Recorded 13 Oct 2026' changed to 'Run 13 Oct 2026' (a recorded result presented as run now)
  stale_honest_not    slide 12: the line 'Lines 1 to 52 (imports,' changed to 'NOT EXECUTED (imports,' on a slide the plan does not list
  stale_title         slide 1: 'never reached' changed to 'reached' (the title no longer says that Gmail, a phone and ntfy were never reached)
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

edit(f("expr"), slide(9), "<a:t>('', 'real@example.com')</a:t>", "<a:t>('', 'evil@example.net')</a:t>")
edit(f("table"), slide(15), "<a:t>lowest</a:t>", "<a:t>TLS 1.2</a:t>")
edit(f("chart"), "ppt/charts/chart1.xml", "<c:v>47.6</c:v>", "<c:v>47.7</c:v>")
edit(f("program"), slide(7), "America/Chicago  2026-12-11 08:48:48", "America/Chicago  2026-12-11 08:48:49")
edit(f("code"), slide(12), "<a:t>'TLS seen:'</a:t>", "<a:t>'TLS saw:'</a:t>")
edit(f("tcap"), slide(13), "<a:t>raised; stored: 1</a:t>", "<a:t>raised; stored: 2</a:t>")
edit(f("diagram"), slide(5), "Call ezgmail.init()", "Call ezgmail.login()")
edit(f("notexec"), slide(6), "NOT EXECUTED here", "Run here")
edit(f("standin_gmail"), slide(7), "Stand-in for Gmail:", "Real Gmail:")
edit(f("standin_local"), slide(12), "a local stand-in; Gmail", "a server; Gmail")
edit(f("recorded"), slide(16), "Recorded 13 Oct 2026", "Run 13 Oct 2026")
edit(f("honest_not"), slide(12), "Lines 1 to 52 (imports,", "NOT EXECUTED (imports,")
edit(f("title"), slide(1), "never reached", "reached")
print("made 13 stale fixtures in", out)
