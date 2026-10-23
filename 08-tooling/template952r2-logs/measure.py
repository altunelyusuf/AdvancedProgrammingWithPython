import sys, json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in sys.argv[1:]:
        for (w,h) in ((1400,900),(360,740)):
            c=b.new_context(viewport={'width':w,'height':h}); pg=c.new_page(); pg.goto('file://'+f); pg.wait_for_timeout(2500)
            r=pg.evaluate("""()=>{const hd=document.querySelector('header.top').getBoundingClientRect().top;
              const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let t='';let n;
              while((n=w.nextNode())){ if(n.parentElement.closest('header,script,style,[hidden]'))continue; if(n.compareDocumentPosition(document.querySelector('header.top'))&Node.DOCUMENT_POSITION_FOLLOWING){t+=n.textContent;} }
              return {header_top:hd, body_text_before_header:t.trim().length}}""")
            print(f.split('/')[-1], w, r)
            c.close()
    b.close()
