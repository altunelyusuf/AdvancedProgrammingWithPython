#!/usr/bin/env python3
"""Template 9.58.0 = 9.57.0 + corrections open only where the owner ruled it: the finished mock exam and its review (xFeed gets a third argument, true there).
The practice drill keeps its corrections folded under the mark until opened, as the page test of 9.42.0 states. Owner ruling of 2026-11-27: the mock exam shows its answers after finishing.
usage: template_patch_v9_58_0.py IN(9.57.0) OUT(9.58.0)"""
import sys
__version__ = "9.58.0"
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90]); s = s.replace(a, b)
rep("function xFeed(it,r){", "function xFeed(it,r,op){")
rep("xFeed=function(it,r){", "xFeed=function(it,r,op){")
rep("(r.fix?'<details class=\"xfixd\" open><summary>'", "(r.fix?'<details class=\"xfixd\"'+(op?' open':'')+'><summary>'")
rep("res.push(r);fs.querySelector('.xfeed').innerHTML=xFeed(it,r);", "res.push(r);fs.querySelector('.xfeed').innerHTML=xFeed(it,r,true);", 2)
rep("const r=rec.res[i];fs.querySelector('.xfeed').innerHTML=xFeed(it,r);", "const r=rec.res[i];fs.querySelector('.xfeed').innerHTML=xFeed(it,r,true);")
rep("<!-- course_page_template version 9.57.0", "<!-- course_page_template version 9.58.0 (new file over 9.57.0; corrections open in the finished exam and its review only, folded in the practice drill). Earlier line: course_page_template version 9.57.0")
open(sys.argv[2], "w", encoding="utf-8").write(s); print("wrote", sys.argv[2], len(s))
