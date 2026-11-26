"""Lineage14 mission-stage measure of chapters 21 to 25 as they stand (run from repo root with /tmp/v20/bin/python)."""
import re,glob,subprocess,os
from pptx import Presentation
PH=re.compile(r"\b(?:think of|imagine|just like|is like a|are like|as if|picture a)\b",re.I)
out=[]
for n in range(21,26):
    d=f"08-tooling/ch{n}-deck/sen0414_ch{n}_deck_v1_0_0.pptx"; p=Presentation(d)
    sl=len(p.slides); bal=ana=ph=pr=lam=code=0; nonotes=0
    for s in p.slides:
        names=[x.name for x in s.shapes]
        txt=" ".join(x.text_frame.text for x in s.shapes if x.has_text_frame)
        nt=s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
        if not nt.strip(): nonotes+=1
        if names.count("result balloon")>=2: bal+=1
        if re.search(r"Everyday picture|ANALOGY|analogy",txt,re.I): ana+=1
        ph+=len(PH.findall(txt))+len(PH.findall(nt)); pr+=txt.count(">>>"); lam+=len(re.findall(r"\blambda\b",txt))
    pages=sorted(glob.glob(f"03-materials/ch{n}/page/sen0414_ch{n}_page_v*.html"),key=lambda f:tuple(map(int,re.findall(r"v(\d+)_(\d+)_(\d+)",f)[0])))
    pg=open(pages[-1]).read()
    pt=re.sub(r"<script.*?</script>|<style.*?</style>","",pg,flags=re.S)
    pa=len(re.findall(r"Everyday picture|analog",pt,re.I))
    ro=bool(re.search(r"run.{0,20}in order|runInOrder|run-in-order",pg,re.I))
    abox=glob.glob(f"03-materials/ch{n}/page/*abox*")
    man=glob.glob(f"03-materials/ch{n}/page/chapter_code*")
    r={}
    for k,sc in [("fit","deck_fit_check_v1_0_0.py"),("overlap","sen0414_deck_overlap_check_v1_0_0.py"),("reader","sen0414_reader_notes_check_v1_0_0.py"),("story","sen0414_story_prose_check_v1_0_0.py")]:
        o=subprocess.run(["python3","08-tooling/"+sc,d],capture_output=True,text=True).stdout
        r[k]=o.strip().splitlines()[-1][:60] if o.strip() else "no output"
        if k=="fit":
            m=re.search(r"(\d+) frame\(s\) overflowing.*?(\d+) pair\(s\) of text frames overlapping.*?(\d+) slide\(s\) with text but no speaker",o); r[k]=m.groups() if m else o[:80]
    out.append(f"ch{n}: deck {d.split('/')[-1]} slides {sl}; result-balloon slides {bal}; analogy slides {ana}; phrase hits {ph}; '>>>' {pr}; lambda words {lam}; slides without notes {nonotes}; fit(overflow,overlap,nonotes) {r['fit']}; overlap {r['overlap']}; reader-notes {r['reader']}; story-prose {r['story']}; newest page {os.path.basename(pages[-1])}, analogy words {pa}, run-in-order item {ro}, page A-box files {len(abox)}, chapter-code manifests {len(man)}")
print("\n".join(out))
