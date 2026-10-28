import sys
from playwright.sync_api import sync_playwright
page=sys.argv[1]; which=[int(x) for x in sys.argv[2:]] or list(range(1,29))
with sync_playwright() as p:
    import os; br=p.chromium.launch(**({"proxy":{"server":os.environ["HTTPS_PROXY"]}} if os.environ.get("HTTPS_PROXY") else {})); pg=br.new_context(locale="en-US").new_page(); pg.set_viewport_size({"width":1400,"height":845}); pg.on("console", lambda m: print("CONSOLE", m.text[:200]) if m.type in ("error","warning") else None); pg.goto("file://"+page); pg.wait_for_timeout(1000)
    pg.evaluate("showTab('chaptercode')"); pg.wait_for_timeout(500)
    items=pg.query_selector_all('[data-cc-item]'); print(len(items))
    for n in which:
        items=pg.query_selector_all('[data-cc-item]')
        items[n-1].click(); pg.wait_for_timeout(300)
        pg.click('[data-cc-run]')
        pg.wait_for_function("()=>{const r=document.querySelector('[data-cc-result]');return r&&r.innerText.trim().length>0&&!/running/i.test(r.innerText)}",timeout=120000)
        pg.wait_for_timeout(500)
        print("=== example",n); t=pg.inner_text("[data-cc-result]"); print(("ERR " if "error" in t.lower() or "Traceback" in t else "ok ")+t.replace("\n"," | ")[:1500])
    br.close()
