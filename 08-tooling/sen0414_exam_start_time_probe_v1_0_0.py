import sys,time
from playwright.sync_api import sync_playwright
page=sys.argv[1]; n=int(sys.argv[2]); out=[]
with sync_playwright() as p:
    br=p.chromium.launch()
    for i in range(n):
        c=br.new_context(viewport={"width":1366,"height":768}); pg=c.new_page(); pg.goto("file://"+page); pg.wait_for_timeout(800)
        pg.evaluate("showTab('exam')"); pg.wait_for_timeout(500)
        pg.fill("#xesno","20210001"); pg.fill("#xesname","Test"); pg.fill("#xessur","Student"); pg.select_option("#xekind","F"); pg.uncheck("#xetimeron"); pg.fill("#xecode","F-31337")
        t0=time.time(); pg.click("#xestart")
        try:
            pg.wait_for_selector("#xefinish",timeout=180000); out.append(round(time.time()-t0,1))
        except Exception as e: out.append("TIMEOUT")
        c.close()
print(page.split('/')[-1],out)
