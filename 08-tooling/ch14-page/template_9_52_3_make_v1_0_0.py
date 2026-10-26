#!/usr/bin/env python3
"""Writes 08-tooling/course_page_template_v9_52_3.html from course_page_template_v9_52_2.html (which is not touched): the Python worker's _run restores, after EVERY run,
sys.path, the modules the program added that do not come from the interpreter's library folders, the working folder and os.environ. Usage: template_9_52_3_make_v1_0_0.py"""
import os
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(os.path.dirname(H), "")
src = open(T + "course_page_template_v9_52_2.html", encoding="utf-8").read()
OLD_HEAD = 'import sys, io, ast\\\\ndef _run(src, inp):\\\\n'
NEW_HEAD = 'import sys, io, ast, os, sysconfig\\\\ndef _run_inner(src, inp):\\\\n'
OLD_TAIL = "    return _o.getvalue().rstrip()\\\\n\");"
assert src.count(OLD_HEAD) == 1 and src.count(OLD_TAIL) == 1, (src.count(OLD_HEAD), src.count(OLD_TAIL))
EXTRA = r'''
_CWD0 = os.getcwd()
_LIBS = tuple(sorted({os.path.join(p, '') for p in [sysconfig.get_path(k) for k in ('stdlib', 'platstdlib', 'purelib', 'platlib')] + [q for q in sys.path if q and q != _CWD0 and q != '.']}))
def _inlib(w):
    return str(w).startswith(_LIBS)
def _restore(p, m, c, e):
    try:
        sys.path[:] = p
    except Exception: pass
    try:
        for k in [k for k in list(sys.modules) if k not in m]:
            mod = sys.modules.get(k); f = getattr(mod, '__file__', None)
            where = [f] if f else [str(x) for x in (getattr(mod, '__path__', None) or [])]
            if where and not all(_inlib(w) for w in where): sys.modules.pop(k, None)
    except Exception: pass
    try:
        os.chdir(c)
    except Exception: pass
    try:
        os.environ.clear(); os.environ.update(e)
    except Exception: pass
    try:
        import importlib; importlib.invalidate_caches()
    except Exception: pass
def _run(src, inp):
    _p = list(sys.path); _m = set(sys.modules); _c = os.getcwd(); _e = dict(os.environ)
    try:
        return _run_inner(src, inp)
    finally:
        _restore(_p, _m, _c, _e)
'''
assert '"' not in EXTRA and '`' not in EXTRA and '\\' not in EXTRA and '${' not in EXTRA
enc = EXTRA.replace('\n', '\\\\n')
out = src.replace(OLD_HEAD, NEW_HEAD).replace(OLD_TAIL, "    return _o.getvalue().rstrip()" + enc + '");')
NOTE = ("<!-- course_page_template version 9.52.3 (SEN0414): REPAIR over 9.52.2 - the Python worker kept the state a program left behind: a blank exercise's probe that failed after sys.path.insert left the temporary folder in sys.path and the module in sys.modules, so the next real run of the program met the leftover module and the right answer was refused (chapter 14, 'Import result'). The worker's _run now restores, after EVERY run, sys.path, the modules the program added that do not come from the interpreter's library folders (the standard library and site-packages, wheels included), the working folder and os.environ, and refreshes the import caches; nothing else changed from 9.52.2. Version 9.52.2 follows. ")
a = "<!-- course_page_template version 9.52.2 (SEN0414): REPAIR over 9.52.1"
assert out.count(a) == 1
out = out.replace(a, NOTE + a[len("<!-- "):], 1)
open(T + "course_page_template_v9_52_3.html", "w", encoding="utf-8").write(out)
print("written course_page_template_v9_52_3.html", len(out), "bytes (9.52.2:", len(src), ")")
