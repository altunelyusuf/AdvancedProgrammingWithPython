"""Chapter 25 deck examples, version 1.0.0 (SEN0414, Lineage14): the 17 code examples of the deck "Threads", in slide order, in five parts. Every example is run by the generic builder
08-tooling/chapter_deck_build_v2_11_0.py with the interpreter of the chapter (Python 3.14.6, requests and beautifulsoup4); its printed text is what the result slides show.
The hidden setup lines (lab25) give an example its own folder; the comic site is replaced by a local stand-in (127.0.0.1) and xkcd.com is never contacted.
A program that waits prints only what does not depend on how long it took: a list, a name, an error message, a count or a boolean. The timings that the research measured once are in the
record of the chapter and are marked Recorded where a slide shows them."""
__version__ = "1.0.0"

LAB = ["from lab25_v1_0_0 import *", "begin()"]
LOOP = ["import threading", "threads = []", "for i in range(0, 140, 10):", "    start, end = max(i, 1), i + 9",
        "    t = threading.Thread(target=downloadXkcd, args=(start, end))", "    threads.append(t)"]

EXAMPLES = [
    # ------------------------------------------------------------ part 1: starting, waiting and ending threads
    dict(id="start", name="Starting a thread", title="start() runs the target on a second thread", part=1, visual="start", layout="left",
         setup=LAB, concepts=["Multithreading", "threading.Thread()", "threadObj.start()", "threadObj.join()", "time.sleep()", "target=takeANap", "threadDemo.py", "threading.current_thread()"],
         groups=[
             (["import threading, time", "print('Start of program.')", "def takeANap():", "    time.sleep(0.5)", "    print('Wake up!')",
               "threadObj = threading.Thread(target=takeANap)", "threadObj.start()", "print('End of program.')", "threadObj.join()"],
              "The line of the new thread comes last, although start() was called before the last line of the main thread."),
             (["box = []", "def f():", "    me = threading.current_thread()", "    box.append((me.name, threading.active_count()))",
               "t = threading.Thread(target=f)", "t.start(); t.join()", "print(box[0], threading.current_thread().name)"],
              "A thread has a name, and the main thread is called MainThread."),
         ]),
    dict(id="args", name="The arguments of the target", title="args is a list, kwargs is a dictionary", part=1, visual="args", layout="left",
         setup=LAB, concepts=["Passing Arguments to the Thread's Target Function", "args=['Cats', 'Dogs', 'Frogs']", "kwargs={'sep': ' & '}"],
         groups=[
             (["import threading", "def go(sep):", "    t = threading.Thread(target=print, kwargs={'sep': sep},",
               "                         args=['Cats', 'Dogs', 'Frogs'])", "    t.start(); t.join()", "go(' & ')", "go('& ')"],
              "The list becomes the positional arguments and the dictionary the keyword arguments of print()."),
             (["t = threading.Thread(target=print('Now', 'not later'))", "t.start(); t.join()", "print('thread alive:', t.is_alive())"],
              "print() ran at once, in the main thread; the target of the thread is None."),
         ]),
    dict(id="life", name="The life of a Thread object", title="A thread starts once, and its error stays in it", part=1, visual="life", layout="left",
         setup=LAB, concepts=["Concurrency Issues"],
         groups=[
             (["import threading", "def f(): pass", "a = threading.Thread(target=f)", "a.start(); a.join()", "try:", "    a.start()", "except RuntimeError as e:",
               "    print('RuntimeError:', e)"],
              "A thread can be started once; a second start() raises RuntimeError."),
             (["def boom():", "    raise ValueError('boom')", "def hook(args):", "    print('hook:', repr(args.exc_value))",
               "threading.excepthook = hook", "t = threading.Thread(target=boom); t.start(); t.join()", "print('main continues')"],
              "An error in a thread does not stop the main thread; threading.excepthook receives it."),
         ]),
    dict(id="join", name="join(): waiting for a thread", title="join() waits; a thread not started cannot be joined", part=1, visual="join", layout="left",
         setup=LAB, concepts=[],
         groups=[
             (["import threading, time", "t = threading.Thread(target=time.sleep, args=[0.6]); t.start()", "r = t.join(0.1)",
               "print('join(0.1) returned', r, '| alive:', t.is_alive())", "t.join()", "print('join() waited | alive:', t.is_alive())"],
              "join(0.1) only waits up to 0.1 s; join() waits until the thread has ended."),
             (["u = threading.Thread(target=print)", "try:", "    u.join()", "except RuntimeError as e:", "    print('RuntimeError:', e)"],
              "A thread that was never started cannot be joined."),
         ]),
    dict(id="daemon", name="Daemon threads", title="A daemon thread does not keep the program alive", part=1, visual="daemon", layout="left",
         setup=LAB, concepts=["daemon=True"],
         groups=[
             (["import threading, time", "tmpl = '''import threading, time", "def f():", "    time.sleep(0.5); print('late')",
               "threading.Thread(target=f, daemon=%s).start()", "print('end')'''", "for flag in (True, False):", "    out = py(tmpl % flag)",
               "    print('daemon=%s prints' % flag, out.split())"],
              "Two child programs: the daemon thread is cut off at the end; the other thread is waited for."),
             (["t = threading.Thread(target=time.sleep, args=[0.2]); t.start()", "try:", "    t.daemon = True", "except RuntimeError as e:",
               "    print('RuntimeError:', e)"],
              "The flag can be set only before start()."),
         ]),
    # ------------------------------------------------------------ part 2: the downloader
    dict(id="printed", name="The downloader as printed", title="The listing never starts the threads", part=2, visual="printed", layout="left",
         setup=LAB + ["serve()"], concepts=["Project: Multithreaded XKCD Downloader", "Step 1: Modify the Program to Use a Function", "downloadXkcd()", "threadedDownloadXkcd.py"],
         groups=[
             (LOOP, "Step 2 of the book: one thread for each range of ten comics, put in a list."),
             (["try:", "    for t in threads:", "        t.join()", "except RuntimeError as e:", "    print('RuntimeError:', e)",
               "print('comic pages requested:', len(requested()))"],
              "Without start() no request is made, and join() raises."),
         ]),
    dict(id="fixed", name="The downloader with start()", title="With start() it skips every tenth comic", part=2, visual="fixed", layout="left",
         setup=LAB + ["serve()"], concepts=["Step 2: Create and Start Threads", "Step 3: Wait for All Threads to End"],
         groups=[
             (LOOP + ["    t.start()", "for t in threads:", "    t.join()"], "Step 3 of the book: join() every thread, so that the program ends when all are done."),
             (["pages = requested()", "missing = [n for n in range(1, 140) if n not in pages]", "print('requested', len(pages), '| never requested', len(missing))",
               "print(missing[:3], '...', missing[-1])", "skipped_png(pages)"],
              "The ranges end one short: 9, 19, 29 and every tenth number after them are never asked for."),
         ]),
    # ------------------------------------------------------------ part 3: threads that share data
    dict(id="lost", name="Lost updates", title="Two threads read 0 and both write 1", part=3, visual="lost", layout="left",
         setup=LAB, concepts=["Concurrency Issues"],
         groups=[
             (["import threading, time", "def trial(use_lock):", "    box = [0]; lk = threading.Lock()", "    def f():",
               "        if use_lock: lk.acquire()", "        v = box[0]; time.sleep(0.05); box[0] = v + 1", "        if use_lock: lk.release()",
               "    ts = [threading.Thread(target=f) for _ in range(2)]", "    for t in ts: t.start()", "    for t in ts: t.join()", "    return box[0]"],
              "Each thread reads the value, waits, and writes back the value plus one."),
             (["print('no lock  :', [trial(False) for _ in range(3)])", "print('with lock:', [trial(True) for _ in range(3)])"],
              "Without the lock both threads read 0 and the counter ends at 1; with it, at 2."),
         ]),
    dict(id="lock", name="Locks", title="A lock makes the read and the write one step", part=3, visual="lock", layout="left",
         setup=LAB, concepts=["threading.Lock", "threading.RLock"],
         groups=[
             (["import threading", "box = [0]; lk = threading.Lock()", "def f():", "    for _ in range(100000):", "        with lk:",
               "            box[0] += 1", "ts = [threading.Thread(target=f) for _ in range(4)]", "for t in ts: t.start()", "for t in ts: t.join()",
               "print('4 threads x 100000 with a lock:', box[0])"],
              "Four threads add 100000 times each; the with statement takes and releases the lock."),
             (["rk = threading.RLock(); lk.acquire(); rk.acquire()", "print('Lock again, 0.2 s :', lk.acquire(timeout=0.2))",
               "print('RLock again       :', rk.acquire(timeout=0.2))"],
              "A Lock cannot be taken twice by its owner; an RLock can."),
         ]),
    dict(id="dead", name="Deadlock", title="Two locks in opposite orders wait for ever", part=3, visual="dead", layout="left",
         setup=LAB, concepts=[],
         groups=[
             (["import threading, time", "a, b = threading.Lock(), threading.Lock()", "def f(x, y):", "    with x:", "        time.sleep(0.1)", "        with y:",
               "            pass", "t1 = threading.Thread(target=f, args=(a, b), daemon=True)", "t2 = threading.Thread(target=f, args=(b, a), daemon=True)",
               "t1.start(); t2.start(); t1.join(0.5); t2.join(0.5)", "print('alive after 0.5 s:', t1.is_alive(), t2.is_alive())"],
              "Each thread holds one lock and waits for the other; both are still alive."),
         ]),
    dict(id="sem", name="Semaphores", title="A Semaphore of 2 lets two of six threads in", part=3, visual="sem", layout="left",
         setup=LAB, concepts=["threading.Semaphore"],
         groups=[
             (["import threading, time", "def trial(limit):", "    inside, top, lk = [0], [0], threading.Lock()", "    sem = threading.BoundedSemaphore(limit)",
               "    def f():", "        with sem:", "            with lk:", "                inside[0] += 1", "                top[0] = max(top[0], inside[0])",
               "            time.sleep(0.1)", "            with lk:", "                inside[0] -= 1",
               "    ts = [threading.Thread(target=f) for _ in range(6)]", "    for t in ts: t.start()", "    for t in ts: t.join()", "    return top[0]"],
              "The most threads inside at once is counted."),
             (["print('most inside, Semaphore(2):', trial(2))", "print('most inside, Semaphore(6):', trial(6))"],
              "The semaphore keeps the number inside at its limit."),
         ]),
    dict(id="queue", name="Queues and events", title="A queue hands items over; an Event says go", part=3, visual="queue", layout="left",
         setup=LAB, concepts=["queue.Queue", "threading.Event", "queue"],
         groups=[
             (["import threading, queue", "q, got = queue.Queue(), []", "def consumer():", "    for x in iter(q.get, None):", "        got.append(x)",
               "t = threading.Thread(target=consumer); t.start()", "for i in range(5): q.put(i)", "q.put(None); t.join()", "print('consumer received', got)"],
              "The consumer takes items until it gets None."),
             (["import time", "ev, seen = threading.Event(), []", "def wait():", "    ev.wait(); seen.append('woke')", "w = threading.Thread(target=wait)",
               "w.start(); time.sleep(0.2)", "print('before set():', seen); ev.set(); w.join()", "print('after set()  :', seen)"],
              "A thread waits on an Event until it is set."),
         ]),
    dict(id="pool", name="A pool of threads", title="map() keeps the order of the inputs", part=4, visual="pool", layout="left",
         setup=LAB, concepts=["concurrent.futures", "concurrent.futures.ThreadPoolExecutor()", "executor.submit()", "executor.map()", "max_workers"],
         groups=[
             (["import os, time, threading", "from concurrent.futures import ThreadPoolExecutor, as_completed", "def f(n):", "    time.sleep(0.1 * (3 - n))",
               "    return n", "with ThreadPoolExecutor(3) as ex:", "    print('map         :', list(ex.map(f, [0, 1, 2])))",
               "    fs = [ex.submit(f, n) for n in [0, 1, 2]]", "    done = [fu.result() for fu in as_completed(fs)]", "    print('as_completed:', done)"],
              "map() keeps input order; as_completed() finish order."),
             (["def name(i):", "    time.sleep(0.05)", "    return threading.current_thread().name", "with ThreadPoolExecutor(2, thread_name_prefix='dl') as ex:",
               "    print('names:', sorted(set(ex.map(name, range(4)))))", "with ThreadPoolExecutor() as ex:", "    used = set(ex.map(name, range(40)))",
               "print('used by default:', len(used), '| CPUs:', os.cpu_count())"],
              "A pool reuses threads; the default is CPUs plus 4."),
         ]),
    dict(id="future", name="Futures: results, errors, cancelling", title="A Future carries its error to result()", part=4, visual="future", layout="left",
         setup=LAB, concepts=["future.result()"],
         groups=[
             (["import time, concurrent.futures as cf", "def bad():", "    raise ValueError('boom')", "with cf.ThreadPoolExecutor(1) as ex:", "    fu = ex.submit(bad); time.sleep(0.1)",
               "    print('exception():', repr(fu.exception()))", "    try:", "        fu.result()", "    except ValueError as e:", "        print('result() raises:', e)"],
              "The error of the thread is kept in the Future and raised by result()."),
             (["ex = cf.ThreadPoolExecutor(1)", "fs = [ex.submit(time.sleep, 0.2) for _ in range(5)]", "time.sleep(0.05)", "ex.shutdown(wait=True, cancel_futures=True)",
               "gone = sum(f.cancelled() for f in fs)", "print('cancelled', gone, 'of 5 | ran', 5 - gone)"],
              "shutdown(cancel_futures=True) cancels the tasks that have not started."),
         ]),
    dict(id="gil", name="The GIL, on and off", title="The standard build has the lock; the other can drop it", part=5, visual="gil", layout="left",
         setup=LAB, concepts=["The global interpreter lock", "The free-threaded build", "sys._is_gil_enabled()", "PYTHON_GIL=1"],
         groups=[
             (["import sys, sysconfig", "ask = 'import sys; print(sys._is_gil_enabled())'", "flag = sysconfig.get_config_var('Py_GIL_DISABLED')",
               "print('GIL on?  Py_GIL_DISABLED')", "print('standard      :', sys._is_gil_enabled(), flag)", "print('free-threaded :', py(ask, exe=FT))",
               "print('PYTHON_GIL=1  :', py(ask, exe=FT, PYTHON_GIL='1'))"],
              "Two builds of Python 3.14.6 are asked whether their lock is on; PYTHON_GIL=1 switches it back on."),
         ]),
    dict(id="proc", name="Processes", title="A process has its own copy of the variables", part=5, visual="proc", layout="left",
         setup=LAB, concepts=["multiprocessing", "subprocess", "subprocess.Popen()", "ProcessPoolExecutor", "Keeping Time, Scheduling Tasks, and Launching Programs", "Launching Other Programs from Python"],
         groups=[
             (["import subprocess, sys", "child = \'\'\'import multiprocessing as mp, threading", "if __name__ == '__main__':", "    d = {'n': 0}",
               "    p = mp.Process(target=d.update, args=({'n': 99},))", "    p.start(); p.join()", "    print('child process:', d)",
               "    t = threading.Thread(target=d.update, args=({'n': 99},))", "    t.start(); t.join()", "    print('thread:', d)",
               "    print('start method:', mp.get_start_method())\'\'\'", "print(py(child))"],
              "A child process changes its own copy of the dictionary; a thread changes the same one."),
             (["nap = 'import time; time.sleep(1)'", "k = subprocess.Popen([sys.executable, '-c', nap])", "print('poll() while the child sleeps:', k.poll())",
               "print('wait() returns the return code:', k.wait())"],
              "Popen() starts a program and comes back at once; poll() asks, wait() waits."),
         ]),
    dict(id="async", name="asyncio, and choosing a tool", title="asyncio overlaps waiting on one thread", part=5, visual="async", layout="left",
         setup=LAB, concepts=["asyncio", "asyncio.gather()", "asyncio.to_thread()", "InterpreterPoolExecutor", "concurrent.interpreters"],
         groups=[
             (["import asyncio, time", "async def pause(how):", "    if how == 'await':", "        await asyncio.sleep(0.2)", "    else:",
               "        time.sleep(0.2)", "async def together(how):", "    await asyncio.gather(*[pause(how) for _ in range(5)])",
               "for how in ('await', 'block'):", "    t0 = time.time(); asyncio.run(together(how))", "    print(how, 'under 0.6 s:', time.time() - t0 < 0.6)"],
              "await overlaps the waits; a blocking call stalls all."),
             (["def work():", "    time.sleep(0.2)", "async def bridge():", "    jobs = [asyncio.to_thread(work) for _ in range(5)]",
               "    await asyncio.gather(*jobs)", "t0 = time.time(); asyncio.run(bridge())", "print('to_thread under 0.6 s:', time.time() - t0 < 0.6)"],
              "to_thread() runs a blocking call on a thread."),
         ]),
]

BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def run_text(ex):
    """the hidden setup lines first (they give the example its own folder), then the shown code"""
    return "\n".join(ex.get("setup", []) + code_lines(ex)) + "\n"


def code_text(ex):
    return "\n".join(code_lines(ex)) + "\n"
