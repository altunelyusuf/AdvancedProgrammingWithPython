import sys,time
from playwright.sync_api import sync_playwright
page=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--enable-logging=stderr","--v=0"])
    c=b.new_context(locale="en-US",viewport={"width":1400,"height":900}); pg=c.new_page()
    pg.on("crash",lambda: print("CRASH desktop page"))
    pg.goto("file://"+page); pg.wait_for_timeout(1500)
    pg.evaluate("showTab('chaptercode')")
    pg.evaluate("ccRunAll()"); 
    t=time.time()
    pg.wait_for_function("()=>{const e=document.querySelector('.ccprog');return e&&/examples ran/.test(e.textContent)}",timeout=300000)
    print("run all done",round(time.time()-t),pg.evaluate("document.querySelector('.ccprog').textContent"))
    m=b.new_context(locale="en-US",viewport={"width":390,"height":844},is_mobile=True,has_touch=True,device_scale_factor=2).new_page()
    m.on("crash",lambda: print("CRASH mobile page"))
    m.goto("file://"+page); m.wait_for_timeout(400)
    tabs=m.evaluate("[...document.querySelectorAll('[data-pane]')].map(e=>e.dataset.pane)")
    for k in tabs:
        try: m.evaluate("k=>showTab(k)",k); m.wait_for_timeout(120)
        except Exception as e: print("CRASH at",k); break
    else: print("mobile loop ok")
    b.close()
