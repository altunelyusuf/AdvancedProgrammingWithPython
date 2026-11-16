import sys,re
from playwright.sync_api import sync_playwright
page=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(locale="en-US",viewport={"width":360,"height":740},is_mobile=True,has_touch=True,device_scale_factor=int(sys.argv[2])); m=c.new_page()
    m.goto("file://"+page); m.wait_for_timeout(1500)
    tabs=m.evaluate("[...document.querySelectorAll('[data-pane]')].map(e=>e.dataset.pane)")
    print(len(tabs),tabs)
    for k in tabs:
        try:
            m.evaluate("k=>showTab(k)",k); m.wait_for_timeout(300); print("ok",k)
        except Exception as e:
            print("CRASH at",k,str(e)[:80]); break
    b.close()
