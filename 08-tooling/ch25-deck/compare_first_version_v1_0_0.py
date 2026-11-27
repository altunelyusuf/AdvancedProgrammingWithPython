"""Compares the first-version chapter 25 deck with the new one: on which slides each story or term appears, and how often lambda or '>>>' occurs. Writes the log text to stdout."""
import sys
from pptx import Presentation
OLD, NEW = sys.argv[1], sys.argv[2]
TERMS = ["Munroe", "xkcd", "Therac", "Dijkstra", "semaphore", "blackout", "Athlon", "Thread(", "start()", "join(", "daemon", "Lock", "RLock", "Event", "Semaphore", "Queue", "ThreadPoolExecutor", "as_completed", "Future", "GIL", "free-threaded", "PYTHON_GIL", "multiprocessing", "Popen", "asyncio", "to_thread", "InterpreterPoolExecutor"]
def texts(path):
    out = []
    for s in Presentation(path).slides:
        t = []
        for sh in s.shapes:
            if sh.has_text_frame: t.append(sh.text_frame.text)
            if getattr(sh, "has_table", False) and sh.has_table:
                for r in sh.table.rows:
                    for c in r.cells: t.append(c.text)
        out.append("\n".join(t))
    return out
a, b = texts(OLD), texts(NEW)
print("first-version deck: %d slides; new deck: %d slides" % (len(a), len(b)))
for w in TERMS:
    f = lambda L: [i + 1 for i, x in enumerate(L) if w.lower() in x.lower()]
    print("story/term %-22s first version slides %s | new deck slides %s" % (w, f(a), f(b)))
cnt = lambda L: sum(x.count("lambda") + x.count(">>>") for x in L)
print("lambda or >>> occurrences: first version %d, new deck %d" % (cnt(a), cnt(b)))
print("RESULT CLEAN (0 findings)" if cnt(b) == 0 else "RESULT FINDINGS")
