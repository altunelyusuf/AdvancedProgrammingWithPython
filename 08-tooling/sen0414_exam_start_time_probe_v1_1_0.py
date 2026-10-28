"""sen0414_exam_start_time_probe v1_1_0 (a NEW file over v1_0_0, which stays): python3 PROBE PAGE.html N CODE
Clicks #xestart with the given exam code (kind F for F-codes, M for M-codes, timer off) N times in fresh browser contexts and prints the seconds until #xefinish is visible
(TIMEOUT after 200 s), plus the number of programs the page stopped for the time limit (console messages naming a stopped program)."""
import sys, time
from playwright.sync_api import sync_playwright
page = sys.argv[1]; n = int(sys.argv[2]); code = sys.argv[3]; out = []
with sync_playwright() as p:
    br = p.chromium.launch()
    for i in range(n):
        c = br.new_context(viewport={"width": 1366, "height": 768}); pg = c.new_page(); msgs = []
        pg.on("console", lambda m: msgs.append(m.text[:120]))
        pg.goto("file://" + page); pg.wait_for_timeout(800)
        pg.evaluate("showTab('exam')"); pg.wait_for_timeout(500)
        pg.fill("#xesno", "20210001"); pg.fill("#xesname", "Test"); pg.fill("#xessur", "Student"); pg.select_option("#xekind", code[0]); pg.uncheck("#xetimeron"); pg.fill("#xecode", code)
        t0 = time.time(); pg.click("#xestart")
        try:
            pg.wait_for_selector("#xefinish", timeout=200000); out.append(round(time.time() - t0, 1))
        except Exception:
            out.append("TIMEOUT")
        out.append(len([m for m in msgs if "stopped" in m or "still running" in m]))
        c.close()
print(page.split("/")[-1], code, out)
