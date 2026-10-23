import sys, json
from playwright.sync_api import sync_playwright
page_path, = sys.argv[1:2]
with sync_playwright() as p:
    b = p.chromium.launch()
    for w,h in ((1366,768),(390,800)):
        c = b.new_context(viewport={'width':w,'height':h}); pg = c.new_page(); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('file://'+page_path); pg.wait_for_timeout(2500)
        r = pg.evaluate("""()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
          std:(document.querySelector('meta[name=page-standard]')||{}).content, charset_first: document.head.firstElementChild.outerHTML,
          cc:document.querySelectorAll('[data-pane=chaptercode]').length, panels:document.querySelectorAll('[data-panel]').length,
          tabs:document.querySelectorAll('[role=tab]').length, tree:document.querySelectorAll('[role=treeitem]').length,
          pg:document.querySelectorAll('[data-pg-item]').length})""")
        print(w, json.dumps(r), 'pageerrors', errs[:3])
        if w==1366 and r['cc']:
            pg.evaluate("document.querySelector('[data-tab=chaptercode]').click()"); pg.wait_for_timeout(600)
            print(' items', pg.evaluate("[...document.querySelectorAll('[data-cc-item]')].map(e=>[e.dataset.ccOrder,e.dataset.ccName])"))
            pg.evaluate("document.querySelectorAll('[data-cc-item]')[1].click()"); pg.wait_for_timeout(400)
            pg.evaluate("document.querySelector('[data-cc-run]').click()")
            pg.wait_for_function("document.querySelector('[data-cc-result]') && document.querySelector('[data-cc-result]').innerText.trim().length>0 && !/Running/.test(document.querySelector('[data-cc-result]').innerText)", timeout=120000)
            print(' result:', pg.evaluate("document.querySelector('[data-cc-result]').innerText")[:200].replace('\n',' | '))
        c.close()
    b.close()
