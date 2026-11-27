"""Exam content rule (owner, 2026-11-24/27): questions test course content and code, never book metadata
(practice-section scaffolding, edition changes, errata). Strips generation fields of meta nodes and
drops meta question-bank items; every removed item is listed."""
import re,json,sys
META={'PracticeWork','PracticeQuestions','PracticePrograms','PracticeProgram','PracticeProgramsAndAnswers','BookAndPractice','WorkingVocabulary','EditionChange','SecondEditionContent','BookCorrections','Questions'}
EXTRA={('ch04','Programs')}
TXT=re.compile(r'practice|chapter|reader|subject cover|questions answered|vocabulary|textbook|\bbook\b|edition|errata',re.I)
def clean(h,ch):
    rep=[]
    m=re.search(r'(id="data">)(.*?)(</script>)',h,re.S);D=json.loads(m.group(2))
    for n in D['nodes']:
        if n['id'] in META:
            for k in ('example','definition','io'):
                if k in n: del n[k];rep.append('node %s.%s'%(n['id'],k))
    h=h[:m.start(2)]+json.dumps(D,ensure_ascii=True).replace('</','<\\/')+h[m.end(2):]
    m=re.search(r'(id="qbank">)(.*?)(</script>)',h,re.S);Q=json.loads(m.group(2));keep=[]
    for x in Q:
        t=x.get('q','')+' '+' '.join(map(str,x.get('options') or []))+' '+x.get('why','')
        if (x.get('concept') in META and TXT.search(t)) or (ch,x.get('concept')) in EXTRA: rep.append('q %s: %s'%(x['concept'],x['q'][:70]));continue
        keep.append(x)
    h=h[:m.start(2)]+json.dumps(keep,ensure_ascii=True).replace('</','<\\/')+h[m.end(2):]
    return h,rep
if __name__=='__main__':
    for f in open('/tmp/newpages.txt').read().split():
        ch=re.search(r'/(ch\d\d)/',f).group(1)
        h,rep=clean(open(f,encoding='utf8').read(),ch)
        open(f,'w',encoding='utf8').write(h);print(ch,len(rep),rep[:6])

def exclude(h,ch):
    """exam/quiz/drill generation skips the meta nodes (practice scaffolding, edition changes, errata)"""
    if 'const XMETANODES=' in h: return h,'already'
    m=re.search(r'(id="data">)(.*?)(</script>)',h,re.S);D=json.loads(m.group(2))
    ids=sorted({n['id'] for n in D['nodes'] if n['id'] in META or (n['label'] in ('Programs','Questions') and n.get('parent') in META)})
    a="qUnder=id=>{const r=[];const w=i=>qKids(i).forEach(k=>{r.push(k.id);w(k.id)});w(id);return r};"
    assert h.count(a)==1
    h=h.replace(a,a+"\nconst XMETANODES=new Set("+json.dumps(ids)+");")
    p1="cids:xsh([top.id].concat(qUnder(top.id)),R)";assert h.count(p1)==1
    h=h.replace(p1,"cids:xsh([top.id].concat(qUnder(top.id)).filter(i=>!XMETANODES.has(i)),R)")
    p2="if(!scope||scope==='all')return D.nodes.map(n=>n.id);return [scope].concat(qUnder(scope))";assert h.count(p2)==1
    h=h.replace(p2,"if(!scope||scope==='all')return D.nodes.map(n=>n.id).filter(i=>!XMETANODES.has(i));return [scope].concat(qUnder(scope)).filter(i=>!XMETANODES.has(i))")
    p3="const ids=scope&&scope!=='all'?[scope].concat(qUnder(scope)):D.nodes.map(n=>n.id);return xsh(ids,R)";assert h.count(p3)==1
    h=h.replace(p3,"const ids=(scope&&scope!=='all'?[scope].concat(qUnder(scope)):D.nodes.map(n=>n.id)).filter(i=>!XMETANODES.has(i));return xsh(ids,R)")
    return h,ids
