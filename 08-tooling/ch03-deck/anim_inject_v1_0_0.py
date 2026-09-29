"""Adds what pptxgenjs cannot write: click-by-click build animations and slide transitions.
A shape whose name ends in '|bN' appears (Fade entrance) on the N-th click of its slide; shapes sharing N appear together.
Dark slides (the hook, title and closing slides) fade in. Everything else in the file is left byte-for-byte as built.
Usage: anim_inject_v1_0_0.py <in.pptx> <out.pptx>   Prints the number of animated slides and click effects."""
__version__ = "1.0.0"
import re, sys, zipfile

def timing(shapes_by_click, has_text):
    nid = [2]
    def nx(): nid[0] += 1; return nid[0]
    clicks = []
    for k in sorted(shapes_by_click):
        pars = []
        for i, spid in enumerate(shapes_by_click[k]):
            grp = ' grpId="0"' if spid in has_text else ''
            pars.append(
                '<p:par><p:cTn id="%d" presetID="10" presetClass="entr" presetSubtype="0" fill="hold"%s nodeType="%s"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                '<p:set><p:cBhvr><p:cTn id="%d" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="%s"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
                '<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="%d" dur="400"/><p:tgtEl><p:spTgt spid="%s"/></p:tgtEl></p:cBhvr></p:animEffect>'
                '</p:childTnLst></p:cTn></p:par>' % (nx(), grp, "clickEffect" if i == 0 else "withEffect", nx(), spid, nx(), spid))
        outer = nx(); inner = nx()
        clicks.append('<p:par><p:cTn id="%d" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="%d" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>%s</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>' % (outer, inner, "".join(pars)))
    bld = "".join('<p:bldP spid="%s" grpId="0" animBg="1"/>' % sp for sp in sorted(has_text, key=int))
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>%s</p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>%s</p:timing>'
            % ("".join(clicks), ("<p:bldLst>%s</p:bldLst>" % bld) if bld else ""))

def main(src, dst):
    zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED); slides = clicks_total = 0
    for it in zin.infolist():
        data = zin.read(it.filename)
        if re.match(r"ppt/slides/slide\d+\.xml$", it.filename):
            x = data.decode("utf-8"); by = {}; has_text = set()
            for m in re.finditer(r'<p:sp><p:nvSpPr><p:cNvPr id="(\d+)" name="([^"]*)"[^>]*>(.*?)</p:sp>', x, flags=re.S):
                spid, name, body = m.group(1), m.group(2), m.group(3)
                mm = re.search(r"\|b(\d+)$", name)
                if mm:
                    by.setdefault(int(mm.group(1)), []).append(spid)
                    if "<p:txBody>" in body: has_text.add(spid)
            dark = 'name="Slide' in x and re.search(r'<p:bg><p:bgPr><a:solidFill><a:srgbClr val="1E2A3A"', x) is not None
            add = ""
            if dark: add += '<p:transition spd="med"><p:fade/></p:transition>'
            if by:
                add += timing(by, has_text); slides += 1; clicks_total += len(by)
            if add:
                assert "</p:clrMapOvr>" in x
                x = x.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + add, 1)
            data = x.encode("utf-8")
        zout.writestr(it, data)
    zout.close(); print("animated %d slides, %d click steps" % (slides, clicks_total))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
