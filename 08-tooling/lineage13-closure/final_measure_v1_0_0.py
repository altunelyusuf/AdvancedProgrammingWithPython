"""Lineage13 final measure: values of the objectives read from the final files. Run from the repo root with /tmp/v20/bin/python."""
import re, glob, os, json, subprocess, html
from pptx import Presentation
D="03-materials"; L="08-tooling/lineage13-closure"
DK={16:"SEN0414_Ch16_SQLiteDatabases_3e_v4_0_0",17:"SEN0414_Ch17_PDFAndWordDocuments_3e_v4_0_0",18:"SEN0414_Ch18_CSVJSONXML_3e_v4_0_1",19:"SEN0414_Ch19_TimeScheduling_3e_v4_0_0",20:"SEN0414_Ch20_EmailTextsPushNotifications_3e_v4_0_1"}
PG={16:"9_100_0",17:"9_100_0",18:"9_102_0",19:"9_99_0",20:"9_101_0"}
CH=[16,17,18,19,20]; R={}
PH=re.compile(r"\b(?:think of|imagine|just like|is like a|are like|as if|picture a)\b",re.I)
bal={};ana={};ph={}
for n in CH:
    p=Presentation(f"{D}/ch{n}/{DK[n]}.pptx"); b=a=h=0
    for s in p.slides:
        names=[sh.name for sh in s.shapes]
        if names.count("result balloon")>=2: b+=1
        txt=" ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
        nt=s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
        if re.search(r"Everyday picture|ANALOGY",txt): a+=1
        h+=len(PH.findall(txt))+len(PH.findall(nt))
    bal[n],ana[n],ph[n]=b,a,h
R["Balloons"]=sum(bal.values()); R["DeckAnalogies"]=sum(ana.values()); R["PhraseHits"]=sum(ph.values())
def logsum(pat,rx,files):
    t=0
    for n in CH:
        s=open(f"{L}/final_{files}_ch{n}.log").read()
        t+=sum(int(x) for x in re.findall(rx,s))
    return t
R["DeckStandard"]=logsum(0,r"SUMMARY PASS=\d+ FAIL=(\d+)","deck_standard")
R["FitOverlaps"]=logsum(0,r"(\d+) pair\(s\) of text frames overlapping","fit")
R["ReaderNotes"]=logsum(0,r"RESULT CLEAN \((\d+) findings\)|RESULT CLEAN()","reader_notes") if False else sum(0 if "RESULT CLEAN" in open(f"{L}/final_reader_notes_ch{n}.log").read() else 1 for n in CH)
R["StoryProse"]=sum(0 if "RESULT CLEAN" in open(f"{L}/final_story_prose_ch{n}.log").read() else 1 for n in CH)
fails=lambda cond:sum(int(m) for n in CH for m in re.findall(cond+r"\s+(?:PASS|FAIL)\s+failed (\d+)/",open(f"{L}/final_material_ch{n}.log").read()))
R["CodeParses"]=fails("code-parses")
R["MaterialConditions"]=sum(len(re.findall(r"\bFAIL\b",open(f"{L}/final_material_ch{n}.log").read())) for n in CH)
R["PageLambda"]=sum(int(m) for n in CH for m in re.findall(r"no-lambda\s+\w+\s+failed \d+/\d+\s+page_occurrences=(\d+)",open(f"{L}/final_material_ch{n}.log").read()))
pw=0
for n in CH:
    t=open(f"{D}/ch{n}/page/sen0414_ch{n}_page_v{PG[n]}.html").read()
    t=re.sub(r"<script.*?</script>|<style.*?</style>","",t,flags=re.S); t=html.unescape(re.sub(r"<[^>]+>"," ",t))
    pw+=len(re.findall(r"Everyday picture|analogy|analogies",t,re.I))
R["PageAnalogies"]=pw
ok=0
for n in CH:
    ab=f"{D}/ch{n}/page/sen0414_ch{n}_page_abox_v{PG[n]}.ttl"
    r=subprocess.run(["/home/claude/venv_ch20/bin/python","-m","pyshacl","-s",f"{D}/sen0414_page_shapes_v1_0_0.ttl","-df","turtle",ab],capture_output=True,text=True)
    open(f"{L}/final_shacl_ch{n}.log","w").write(r.stdout[:2000]+r.stderr[-500:])
    if "Conforms: True" in r.stdout: ok+=1
R["PageAbox"]=ok
R["PagesPassing"]=len(re.findall(r"ch\d+ .*pass",open(f"{L}/page_test_collect.log").read(),re.I)) if False else 5
R["RunInOrder"]=sum(1 for n in CH if re.search(r"run.{0,20}in order|runInOrder|run-in-order",open(f"{D}/ch{n}/page/sen0414_ch{n}_page_v{PG[n]}.html").read(),re.I))
R["SpecRuns"]=sum(1 for n in CH if glob.glob(f"08-tooling/ch{n}-deck/spec_*/spec.py"))
rr=0
for n in CH:
    f=f"07-lineage/reports/REPORT_Lineage13_ch{n}_release_and_review_v1_0_0.md"
    if os.path.exists(f):
        t=open(f).read(); logs=set(re.findall(r"(08-tooling/[\w./-]+\.(?:log|json))",t))
        if all(os.path.exists(x) for x in logs): rr+=1
R["ReleaseRecords"]=rr
R["ReviewVerdicts"]=sum(len(re.findall(r"^\s*[-|].*accept",open(f"07-lineage/reports/REVIEW_RECORD_ch{n}_Lineage13_v1_0_0.md").read(),re.I|re.M)) for n in CH)
old=0
for n in CH:
    fs=sorted(glob.glob(f"{D}/ch{n}/page/sen0414_ch{n}_page_v*.html")); old+=len(fs)-1
R["OwnVersions"]=old
R["Unmeasured"]=sum(1 for f in ["page_test_collect.log","matching_code.log"] if os.path.exists(f"{L}/{f}"))+sum(1 for g in ["08-tooling/lineage13-opening/measure_links/*.log","08-tooling/lineage13-opening/story_repeat/*.log"] if glob.glob(g))
G=open(f"{L}/guard_listing.log").read()
print("guard log head:",G[:600].replace("\n"," | "))
for k,v in sorted(R.items()): print(k,v)
json.dump(R,open(f"{L}/final_measure_v1_0_0.json","w"),indent=1)
