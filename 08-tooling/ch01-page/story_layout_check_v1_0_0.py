import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h in ((1366,768),(390,844)):
        pg=b.new_page(viewport={"width":w,"height":h}); pg.goto("file://"+f); pg.wait_for_timeout(2500)
        pg.get_by_role("tab",name="Learn").first.click(); pg.wait_for_timeout(800)
        pg.get_by_role("tab",name="Stories").first.click(); pg.wait_for_timeout(1500)
        n=pg.eval_on_selector_all("article.story","e=>e.length")
        for i in range(n):
            r=pg.evaluate("""i=>{const a=document.querySelectorAll('article.story')[i];a.scrollIntoView({block:'start'});return null}""",i); pg.wait_for_timeout(500)
            r=pg.evaluate("""i=>{const a=document.querySelectorAll('article.story')[i];const t=a.getBoundingClientRect().top;const im=a.querySelector('figure img').getBoundingClientRect();const ps=[...a.querySelectorAll(':scope > p')];const nar=ps.find(p=>!p.classList.contains('takeaway')&&!p.classList.contains('ssrc')&&!p.classList.contains('lact'));const pr=nar.getBoundingClientRect();return {absTop:Math.round(t),narAbs:Math.round(pr.top),imgBottomAbs:Math.round(im.bottom),id:a.id,imgH:Math.round(im.height),imgBottomRel:Math.round(im.bottom-t),narTopRel:Math.round(pr.top-t),vh:innerHeight}}""",i)
            r["ok"]= r["imgH"]<r["vh"] and r["narTopRel"]<r["vh"]
            print(w,h,r)
        pg.close()
    b.close()
