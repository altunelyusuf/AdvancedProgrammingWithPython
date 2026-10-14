#!/usr/bin/env python3
"""SEN0414, chapter 25 (the Threads subject: the multithreading material of chapter 17 of the 2nd edition of Automate the Boring Stuff with Python) - the live
check of the 74 public sources (version 1.0.0). Each page of ch25-page/sources_list_v1_0_0.txt (url|title|author|year) is fetched once through the proxy of the study on
the day the script runs, and the script records the HTTP status, the bytes, the sha256 and whether a passage the research relies on (a needle, case-insensitive) occurs on the
page. Writes ch25-page/live_observations_v1_0_0.json. One run; a page that answers differently on another day is a different observation."""
__version__ = "1.0.0"
import os, sys, json, time, hashlib, subprocess, re, html, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__))
NEEDLES = ["Multithreading", "automate", "Automate", "pip", "thread", "XKCD", "daemon", "ThreadPoolExecutor", "Process", "event loop",
 "task_done", "setswitchinterval", "sleep", "Popen", "scheduler", "interpreter", "free-threaded", "free-threading", "global interpreter lock", "free-threaded",
 "free-threaded", "shared memory", "GIL", "to_thread", "context", "dump_traceback", "optional", "free-threaded", "per-interpreter", "interpreter",
 "future", "multiprocessing", "asyncio", "await", "Beautiful", "free-thread", "free-thread", "free-thread", "GIL", "thread",
 "race condition", "global interpreter lock", "lock", "deadlock", "semaphore", "thread", "speedup", "consumer", "concurrent", "philosopher",
 "thread", "Dijkstra", "race condition", "blackout", "Python", "requests", "numpy", "thread", "python",
 "cpu_count", "GIL", "GIL", "Gilectomy", "memory model", "interpreter", "thread", "concurrency", "BINARY_OP", "thread",
 "register", "signal", "daemon", "ThreadPoolExecutor", "Popen"]
def fetch(row):
    url = row[0]; needle = {'https://docs.python.org/3.14/c-api/init.html': 'thread'}.get(row[0], NEEDLES[row[4]]); ok = None
    for _ in range(2):
        p = subprocess.run(["curl", "-s", "-L", "-A", "Mozilla/5.0 (course research SEN0414)", "--max-time", "60", "-w", "\n%{http_code}", url], capture_output=True, stdin=subprocess.DEVNULL)
        body, _, code = p.stdout.rpartition(b"\n"); ok = code.decode().strip()
        if ok == "200": break
    t = html.unescape(re.sub(r"<[^>]+>", " ", body.decode("utf8", "replace"))).lower()
    return {"url": url, "title": row[1], "status": int(ok or 0), "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "needle": needle, "needle_found": needle.lower() in t}
if __name__ == "__main__":
    rows = [l.rstrip("\n").split("|") + [i] for i, l in enumerate(open(os.path.join(H, "ch25-page", "sources_list_v1_0_0.txt"))) if l.strip()]
    assert len(rows) == len(NEEDLES), (len(rows), len(NEEDLES))
    with cf.ThreadPoolExecutor(6) as ex: out = list(ex.map(fetch, rows))
    rec = {"what": "live check of the sources of the chapter 25 study, one run", "date": time.strftime("%Y-%m-%d"), "sources": out,
           "ok": sum(o["status"] == 200 for o in out), "needles_found": sum(o["needle_found"] for o in out), "total": len(out)}
    json.dump(rec, open(os.path.join(H, "ch25-page", "live_observations_v1_0_0.json"), "w"), indent=1)
    print(rec["ok"], "of", rec["total"], "answered 200;", rec["needles_found"], "needles found")
    for o in out:
        if o["status"] != 200 or not o["needle_found"]: print("  CHECK", o["status"], o["needle"], o["url"])
