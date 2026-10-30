#!/usr/bin/env python3
"""Makes course_page_template_v9_53_1.html from course_page_template_v9_53_0.html (which stays). Task TK_U8_Page_Build. REPAIR: the resize strip's hint text was .75rem (12.75 px at the
page's root size), under the 14 px text rule that the small-phone check (360 and 390 px) enforces on the map and the ERD views; it is now at least 14 px. Nothing else changed. Refuses to overwrite."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); src = os.path.join(H, "course_page_template_v9_53_0.html"); dst = os.path.join(H, "course_page_template_v9_53_1.html")
if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
t = open(src, encoding="utf-8").read()
def rep(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:70]); t = t.replace(old, new)
rep("<!-- course_page_template version 9.53.0 (SEN0414):", "<!-- course_page_template version 9.53.1 (SEN0414): REPAIR over 9.53.0 - the hint text of the resize strip is at least 14 px (it was 12.75 px and the small-phone check refused it); nothing else changed. Version 9.53.0 follows. course_page_template version 9.53.0 (SEN0414):")
rep(".dprz .note{font-size:.75rem;color:var(--muted,inherit)}", ".dprz .note{font-size:max(14px,.85rem);color:var(--muted,inherit)}")
open(dst, "w", encoding="utf-8").write(t); print("wrote", dst)
