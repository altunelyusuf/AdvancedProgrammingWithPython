#!/usr/bin/env python3
"""Template 9.57.0 = 9.56.0 + REPAIR (found by building chapter 2 on 9.56.0 on 2026-11-27: 'Cannot access XMETAIDS before initialization').
In 9.56.0 the constant XMETANODES reads XMETAIDS, which is declared later in the script, so every page built from 9.56.0 stops at load.
The declaration of XMETAIDS and XMETATEXT moves before XMETANODES. Nothing else changes.
usage: template_patch_v9_57_0.py IN(9.56.0) OUT(9.57.0)"""
import sys, re
__version__ = "9.57.0"
s = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"const XMETAIDS=new Set\(\[[^\]]*\]\),XMETATEXT=/[^\n]*?/i;", s)
assert m and s.count("const XMETAIDS=") == 1, "declaration not found once"
decl = m.group(0)
s = s[:m.start()] + s[m.end():]
a = "const XMETANODES=new Set(D.nodes.filter(n=>XMETAIDS.has(n.id)"
assert s.count(a) == 1
s = s.replace(a, decl + "\n" + a)
assert s.index("const XMETAIDS=") < s.index("XMETAIDS.has(n.id)")
b = "<!-- course_page_template version 9.56.0"
assert s.count(b) == 1
s = s.replace(b, "<!-- course_page_template version 9.57.0 (new file over 9.56.0; REPAIR: XMETAIDS is declared before XMETANODES reads it, so the page loads). Earlier line: course_page_template version 9.56.0")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
