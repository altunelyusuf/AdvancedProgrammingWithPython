#!/usr/bin/env python3
"""Patches course_page_template_v9_37_0.html into course_page_template_v9_38_0.html.

One subject: the exam identity comes from the configuration, not from the template. The template carried the
instructor's public key, the release prefix and the bonus points as constants (XEX_PUB, XEX_PREFIX, XEX_BONUS). The key
pair was re-provisioned after the environment move (the original private key did not survive; the new public half is in
course_page_config_v1_4_0.json), so a page built from this template verified release codes against a key nobody holds:
measured on the 9.27.0 chapter 1 trial page, the full test's unlock with a code made by the current key never showed
the report. The sibling course's line made this repair in its own 9.24.0; it is the same change here: the constants read
data.course.exam {public_key, release_prefix, bonus_points, course, title} with the old values as fallbacks, and the
result-file, audit-log and PDF strings take the course from there too.
"""
__version__ = "9.38.0"
SRC, DST = "course_page_template_v9_37_0.html", "course_page_template_v9_38_0.html"
s = open(SRC, encoding="utf-8").read(); n0 = len(s)
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)
a = s.index("const XEX_PUB={"); e = s.index("const XEX_CH=")
old = s[a:e]
assert old.rstrip().endswith("XEX_BONUS=10;") and "sen0414-exam-release" in old
pub_old = old[old.index("{"):old.index("}") + 1]
s = s[:a] + ("const XEX_CFG=D.course.exam||{},XEX_PUB=XEX_CFG.public_key||" + pub_old + ", XEX_PREFIX=XEX_CFG.release_prefix||'sen0414-exam-release', XEX_BONUS=XEX_CFG.bonus_points==null?10:XEX_CFG.bonus_points,\n"
             " XEX_COURSE=XEX_CFG.course||'SEN0414', XEX_SLUG=XEX_COURSE.toLowerCase(), XEX_TITLE=XEX_CFG.title||'SEN0414 Advanced Programming with Python';\n") + s[e:]
rep("format:'sen0414-exam-result',format_version:1,course:'SEN0414'", "format:XEX_SLUG+'-exam-result',format_version:1,course:XEX_COURSE", 1)
rep("format:'sen0414-audit-log',format_version:1,course:'SEN0414'", "format:XEX_SLUG+'-audit-log',format_version:1,course:XEX_COURSE", 1)
rep("'sen0414-ch'+XEX_CH+'-'+rec.code", "XEX_SLUG+'-ch'+XEX_CH+'-'+rec.code", 1)
rep("return 'sen0414-ch'+XEX_CH+'-audit-'", "return XEX_SLUG+'-ch'+XEX_CH+'-audit-'", 1)
rep("put('SEN0414 Advanced Programming with Python',22,false,'#6E655C',2)", "put(XEX_TITLE,22,false,'#6E655C',2)", 1)
rep("<!-- course_page_template version 9.37.0:", "<!-- course_page_template version 9.38.0: the exam identity (public key, release prefix, bonus, course, title) is read from data.course.exam instead of constants baked into the template, so the re-provisioned instructor key verifies release codes. Earlier: --><!-- course_page_template version 9.37.0:", 1)
open(DST, "w", encoding="utf-8").write(s); print("written %s (%d -> %d bytes)" % (DST, n0, len(s)))
