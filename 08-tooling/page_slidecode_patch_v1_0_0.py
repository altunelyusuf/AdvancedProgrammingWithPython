"""Generic page patch (owner ruling 2026-11-27, urgency case chapter 11): derived from the reviewed
chapter 11 change v9_26_0 -> v9_32_0 (Slide source code tab under Lab, large editor, walk-through,
slide numbers, open corrections, 'Open result and answers', exam review rebuild). Each changed unit
must match exactly once in the target, otherwise the file is refused."""
import re,sys,difflib
B='/home/claude/advancedprogrammingwithpython/03-materials/ch11/page/sen0414_ch11_page_v9_%d_0.html'
A=open(B%26,encoding='utf8').read().split('><');Z=open(B%32,encoding='utf8').read().split('><')
OPS=[]
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,A,Z,autojunk=False).get_opcodes():
    if op=='equal':continue
    old='><'.join(A[i1:i2]);new='><'.join(Z[j1:j2])
    if len(old)>200000 or len(new)>200000: continue   # data / question-bank scripts: not part of the code patch
    if i1==i2: old='><'.join(A[i1-1:i1+1]);new='><'.join(Z[j1-1:j2+1])
    OPS.append((i1,old,new))
WALK=[n for i,o,n in OPS if i==1654][0]
SCRIPT='<'+WALK[:WALK.rfind('</script>')+9]
def patch(h):
    miss=[]
    g="...(CC.length?[['chaptercode','💻 Chapter code']]:[]),"
    lab="lab:[['play','▶ Playground'],"
    if h.count(g)==1 and h.count(lab)==1:
        h=h.replace(g,'').replace(lab,lab+"...(CC.length?[['chaptercode','💻 Slide source code']]:[]),")
    else: miss.append(('groups',h.count(g),h.count(lab)))
    if h.count('</body>')==1 and 'data-cc-walk]' not in h:
        h=h.replace('</body>',SCRIPT+'</body>')
    else: miss.append(('walk',))
    for i1,old,new in OPS:
        if i1 in (147,1654): continue
        if h.count(old)!=1: miss.append((i1,h.count(old)));continue
        h=h.replace(old,new)
    return h,miss
