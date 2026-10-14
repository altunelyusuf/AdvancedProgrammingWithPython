#!/usr/bin/env python3
"""SEN0414, chapter 25 (the Threads subject; the multithreading material of chapter 17 of the 2nd edition of Automate the Boring Stuff with Python) -
the timing measurements of the study (version 1.0.0). Every figure is ONE run on 2026-10-14 on Ubuntu 24.04 with 2 vCPUs; before each experiment the script waits
until the one-minute load average is below 1.0 (a quiet machine, up to 90 s) and records the load it saw. Writes ch25-page/timing_record_v1_0_0.json.
Interpreters: Python 3.14.6 (GIL build), Python 3.14.6 free-threaded build, Python 3.13.14, 3.12.13 and 3.11.15, all installed with uv."""
__version__ = "1.0.0"
import os, sys, json, time, subprocess, tempfile, platform
H = os.path.dirname(os.path.abspath(__file__))
UV = "/root/.local/share/uv/python/"
PY = {"3.14.6": "/home/claude/venv314_ch25_latest/bin/python", "3.14.6t": UV + "cpython-3.14.6+freethreaded-linux-x86_64-gnu/bin/python3.14t",
      "3.13.14": UV + "cpython-3.13-linux-x86_64-gnu/bin/python3.13", "3.12.13": UV + "cpython-3.12-linux-x86_64-gnu/bin/python3.12", "3.11.15": UV + "cpython-3.11-linux-x86_64-gnu/bin/python3.11"}
def quiet(limit=1.0, wait=90):
    t0 = time.time()
    while os.getloadavg()[0] > limit and time.time() - t0 < wait: time.sleep(3)
    return round(os.getloadavg()[0], 2)
def run(exe, code, args=(), limit=280):
    # the code goes into a file because multiprocessing cannot start workers from a program given with -c
    fd, path = tempfile.mkstemp(suffix=".py"); os.write(fd, code.encode()); os.close(fd)
    r = subprocess.run([exe, "-W", "ignore", path] + list(args), capture_output=True, text=True, timeout=limit, stdin=subprocess.DEVNULL)
    return r.stdout.strip() if r.returncode == 0 else "ERR " + (r.stderr.strip().splitlines() or [""])[-1]
CPU = """import sys, time, threading
def work(n):
    x = 0
    for i in range(n): x += i * i
N = 6_000_000
work(2_000_000)
t0 = time.perf_counter(); work(N); work(N); work(N); work(N); serial = time.perf_counter() - t0
res = {"serial_4_tasks": serial}
for k in (2, 4):
    ts = [threading.Thread(target=lambda: [work(N) for _ in range(4 // k)]) for _ in range(k)]
    t0 = time.perf_counter(); [t.start() for t in ts]; [t.join() for t in ts]; res["threads_%d" % k] = time.perf_counter() - t0
print({k: round(v, 3) for k, v in res.items()})
"""
IO = """import threading, time
t0 = time.perf_counter(); [time.sleep(0.5) for _ in range(8)]; serial = time.perf_counter() - t0
ts = [threading.Thread(target=time.sleep, args=[0.5]) for _ in range(8)]
t0 = time.perf_counter(); [t.start() for t in ts]; [t.join() for t in ts]; thr = time.perf_counter() - t0
from concurrent.futures import ThreadPoolExecutor
t0 = time.perf_counter()
with ThreadPoolExecutor(8) as ex: list(ex.map(time.sleep, [0.5] * 8))
pool = time.perf_counter() - t0
import asyncio
async def main(): await asyncio.gather(*[asyncio.sleep(0.5) for _ in range(8)])
t0 = time.perf_counter(); asyncio.run(main()); aio = time.perf_counter() - t0
print({"serial_8_sleeps": round(serial, 3), "threads": round(thr, 3), "pool": round(pool, 3), "asyncio": round(aio, 3)})
"""
MP = """import time, multiprocessing as mp
def work(n):
    x = 0
    for i in range(n): x += i * i
    return x
if __name__ == "__main__":
    N = 6_000_000
    work(2_000_000)
    t0 = time.perf_counter(); [work(N) for _ in range(4)]; serial = time.perf_counter() - t0
    t0 = time.perf_counter()
    with mp.Pool(2) as p: p.map(work, [N] * 4)
    pool = time.perf_counter() - t0
    print({"serial_4_tasks": round(serial, 3), "pool_2_processes": round(pool, 3), "start_method": mp.get_start_method()})
"""
START = """import threading, time, multiprocessing as mp
def f(): pass
if __name__ == "__main__":
    t0 = time.perf_counter(); ts = [threading.Thread(target=f) for _ in range(200)]; [t.start() for t in ts]; [t.join() for t in ts]; thr = time.perf_counter() - t0
    t0 = time.perf_counter(); ps = [mp.Process(target=f) for _ in range(20)]; [p.start() for p in ps]; [p.join() for p in ps]; pr = time.perf_counter() - t0
    print({"200_threads_ms": round(thr * 1000, 1), "20_processes_ms": round(pr * 1000, 1), "per_thread_us": round(thr / 200 * 1e6), "per_process_ms": round(pr / 20 * 1000, 1)})
"""
RACE = """import threading, sys
N = 1_000_000
c = 0
def inc():
    global c
    for _ in range(N): c += 1
ts = [threading.Thread(target=inc) for _ in range(4)]
[t.start() for t in ts]; [t.join() for t in ts]
print({"expected": 4 * N, "got": c, "lost": 4 * N - c})
"""
if __name__ == "__main__":
    out = {"what": "timing measurements of the chapter 25 study, single run each", "date": time.strftime("%Y-%m-%d"), "platform": platform.platform(), "cpus": os.cpu_count(), "runs": {}}
    def rec(name, exe, code, **kw):
        ld = quiet(); t0 = time.time(); o = run(PY[exe], code, **kw)
        try: o = eval(o)
        except Exception: pass
        out["runs"][name] = {"interpreter": exe, "load_before": ld, "load_after": round(os.getloadavg()[0], 2), "result": o}; print(name, o, ld, flush=True)
    for k in ("3.14.6", "3.14.6t", "3.13.14", "3.12.13", "3.11.15"): rec("cpu_" + k, k, CPU)
    for k in ("3.14.6", "3.14.6t"): rec("io_" + k, k, IO)
    rec("multiprocessing_3.14.6", "3.14.6", MP)
    for k in ("3.14.6", "3.14.6t"): rec("start_" + k, k, START)
    for i in range(3):
        for k in ("3.14.6", "3.14.6t", "3.13.14", "3.12.13", "3.11.15"): rec("race_%s_run%d" % (k, i + 1), k, RACE)
    json.dump(out, open(os.path.join(H, "ch25-page", "timing_record_v1_0_0.json"), "w"), indent=1)
    print("written")
