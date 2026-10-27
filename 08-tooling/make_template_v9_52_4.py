#!/usr/bin/env python3
"""Makes course_page_template_v9_52_4.html from course_page_template_v9_52_3.html (which stays): the Python worker also restores, after EVERY run, the interpreter state the
leak probe v1_2_0 reads: tracemalloc tracing (stopped when the program left it on), warnings.filters (the list and its content), the recursion limit, the default socket timeout,
tempfile.tempdir and the umask. Nothing else changed. Refuses to overwrite. Usage: make_template_v9_52_4.py"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); src = os.path.join(H, "course_page_template_v9_52_3.html"); dst = os.path.join(H, "course_page_template_v9_52_4.html")
if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
t = open(src, encoding="utf-8").read()
def rep(old, new):
    global t
    assert t.count(old) == 1, old[:60]; t = t.replace(old, new)
rep("<!-- course_page_template version 9.52.3 (SEN0414):",
    "<!-- course_page_template version 9.52.4 (SEN0414): REPAIR over 9.52.3 - the Python worker restored sys.path, the added modules, the working folder and os.environ after a run, but not the tracing of tracemalloc: a blank exercise's probe that failed after tracemalloc.start() left tracing on, and the next real run of the same page measured a larger peak and the right answer was refused (chapter 18, example IterparseClear, found on one seed of six). The worker's _run now also stops tracemalloc when a program left it tracing, and restores warnings.filters (the list and its content), the recursion limit, the default socket timeout, tempfile.tempdir and the umask after EVERY run; nothing else changed from 9.52.3. Version 9.52.3 follows. course_page_template version 9.52.3 (SEN0414):")
rep("import sys, io, ast, os, sysconfig\\\\ndef _run_inner", "import sys, io, ast, os, sysconfig, warnings, socket, tempfile\\\\ntry:\\\\n    import tracemalloc\\\\nexcept Exception:\\\\n    tracemalloc = None\\\\ndef _run_inner")
rep("def _restore(p, m, c, e):", "def _state_x():\\\\n    u = os.umask(0o22); os.umask(u)\\\\n    return (bool(tracemalloc is not None and tracemalloc.is_tracing()), warnings.filters, list(warnings.filters), sys.getrecursionlimit(), socket.getdefaulttimeout(), tempfile.tempdir, u)\\\\ndef _restore(p, m, c, e, x):")
rep("        import importlib; importlib.invalidate_caches()\\\\n    except Exception: pass\\\\n",
    "        import importlib; importlib.invalidate_caches()\\\\n    except Exception: pass\\\\n"
    "    try:\\\\n        if tracemalloc is not None and tracemalloc.is_tracing() and not x[0]: tracemalloc.stop()\\\\n    except Exception: pass\\\\n"
    "    try:\\\\n        x[1][:] = x[2]; warnings.filters = x[1]; warnings._filters_mutated()\\\\n    except Exception: pass\\\\n"
    "    try:\\\\n        sys.setrecursionlimit(x[3])\\\\n    except Exception: pass\\\\n"
    "    try:\\\\n        socket.setdefaulttimeout(x[4])\\\\n    except Exception: pass\\\\n"
    "    try:\\\\n        tempfile.tempdir = x[5]\\\\n    except Exception: pass\\\\n"
    "    try:\\\\n        os.umask(x[6])\\\\n    except Exception: pass\\\\n")
rep("_e = dict(os.environ)\\\\n    try:\\\\n        return _run_inner(src, inp)\\\\n    finally:\\\\n        _restore(_p, _m, _c, _e)",
    "_e = dict(os.environ); _x = _state_x()\\\\n    try:\\\\n        return _run_inner(src, inp)\\\\n    finally:\\\\n        _restore(_p, _m, _c, _e, _x)")
open(dst, "w", encoding="utf-8").write(t); print("wrote", dst)
