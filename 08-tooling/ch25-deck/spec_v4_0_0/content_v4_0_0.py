"""Chapter 25 deck content, version 4.0.0 (SEN0414, Lineage14): the words of the deck "Threads". Parts, plan, concept slides in plain words (no everyday comparison), stories, the native
tables and chart of the recorded timings and of the five interpreters, take-aways, practice and resources.
Slide numbers of the plan: 1 title, 2 route, 3 questions, 4-11 part 1, 12-16 part 2, 17-25 part 3, 26-30 part 4, 31-37 part 5, 38-39 compare, 40 practice, 41 summary, 42 resources.
The notes are in notes_v4_0_0.py."""
__version__ = "4.0.0"
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = {
    1: ("Part 1: Starting, waiting and ending threads", "start() runs the target, join() waits, a daemon thread is cut off at the end", [
        ("start", "start() runs the target on a second thread; its line comes last"),
        ("args", "args is a list and kwargs a dictionary; a call in place of the target runs at once"),
        ("join", "join() waits, a thread starts once, and its error stays in it")]),
    2: ("Part 2: The multithreaded downloader", "One thread for each range of ten comics, against a local stand-in site", [
        ("printed", "The printed listing never calls start(): no request, and join() raises"),
        ("fixed", "With start() the program asks for 125 of 139 numbers")]),
    3: ("Part 3: Threads that share data", "A lock, an event, a semaphore and a queue keep shared values and waiting threads in order", [
        ("lost", "Two threads read 0 and both write 1 without a lock"),
        ("lock", "A lock, a with statement and an RLock"),
        ("sem", "A semaphore limits how many threads are inside; a queue hands items over")]),
    4: ("Part 4: Pools of threads", "A pool starts and reuses threads and returns results in Future objects", [
        ("pool", "map() keeps the order of the inputs; a pool reuses its threads"),
        ("future", "A Future carries its error to result(); unstarted tasks can be cancelled")]),
    5: ("Part 5: The GIL, processes and asyncio", "The lock of the interpreter, programs of their own, and tasks on one thread", [
        ("gil", "Two builds of Python 3.14.6 and the switch PYTHON_GIL=1"),
        ("proc", "A process has its own copy of the variables; Popen starts a program"),
        ("async", "asyncio overlaps waiting; to_thread() hands blocking calls to threads")]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("analogy", "A1b"), ("code", "start"), ("code", "args"), ("code", "life"), ("code", "join"), ("code", "daemon"),
        ("divider", 2), ("analogy", "A2"), ("story", "munroe"), ("code", "printed"), ("code", "fixed"),
        ("divider", 3), ("analogy", "A3"), ("story", "therac"), ("code", "lost"), ("code", "lock"), ("code", "dead"), ("story", "dijkstra"), ("code", "sem"), ("code", "queue"),
        ("divider", 4), ("analogy", "A4"), ("story", "blackout"), ("code", "pool"), ("code", "future"),
        ("divider", 5), ("analogy", "A5"), ("analogy", "A5b"), ("story", "athlon"), ("code", "gil"), ("code", "proc"), ("code", "async"),
        ("compare", "record"), ("compare", "envs"), ("practice",), ("summary",), ("resources",)]

ROUTE_RUNS = {1: "threads, arguments, errors, join, daemons", 2: "the downloader as printed and with start()", 3: "lost updates, locks, deadlock, semaphores, queues, events",
              4: "pools, map, futures, cancelling", 5: "the GIL, processes, asyncio"}
ROUTE_TAIL = ("Summary and links", "what to remember, where next")

QUESTIONS = [
    ("1", "What does a program need to start, wait for and end threads, and where does the book's downloader go wrong?", "Parts 1 and 2 answer it; the summary repeats it on slide %d.", "summary"),
    ("2", "When do threads lose updates or wait for ever, and which tool fits which work: threads, a pool, processes or asyncio?", "Parts 3 to 5 answer it; the table on slide %d and the questions on slide %d close it.", [("compare", "record"), ("practice",)]),
]
QUESTIONS_TAKEAWAY = "Every example runs on the chapter page; read its printed result first."

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "What it is and does"
CONCEPTS_TAIL = "each explained in plain words"
ANALOGIES = [
    ("A1", "Threads: the module and the first calls", "A Thread object runs a function; start() begins it, join() waits for it, and the module also gives the running thread.", [
        ("Keeping Time, Scheduling Tasks, and Launching Programs", "The heading of the book's chapter: waiting, running work beside the main program, and starting other programs."),
        ("Multithreading", "Running several threads in one process, so that a program can do other work while one thread waits."),
        ("threading", "The standard module for threads, locks, events and semaphores."),
        ("threading.Thread()", "Makes a thread object; target is the function it will run."),
        ("target=takeANap", "The function that the new thread runs; it is given without brackets."),
        ("threadObj.start()", "Starts the thread; the target runs beside the main thread. It can be called once."),
        ("threadObj.join()", "Waits until the thread has ended; join(0.1) waits at most 0.1 s."),
        ("time.sleep()", "Waits for a number of seconds; the thread that calls it does nothing meanwhile."),
        ("threading.current_thread()", "Returns the thread that runs this line; its name is MainThread for the main thread."),
        ("threadDemo.py", "The book's first program: a function that sleeps and prints, run on a thread."),
    ]),
    ("A1b", "Arguments, daemons and errors", "The target gets arguments from args and kwargs; a daemon thread is cut off when the program ends.", [
        ("Passing Arguments to the Thread's Target Function", "The target is called with the arguments that args and kwargs give."),
        ("args=['Cats', 'Dogs', 'Frogs']", "A list of the positional arguments of the target."),
        ("kwargs={'sep': ' & '}", "A dictionary of the keyword arguments of the target."),
        ("daemon=True", "Marks a thread that does not keep the program alive; it is set before start()."),
    ]),
    ("A2", "The multithreaded XKCD downloader project", "The book's project downloads comics with threads: a function, threads that start, and a join for every thread.", [
        ("Project: Multithreaded XKCD Downloader", "A program that downloads many comic pages and their images, with one thread for each range."),
        ("Step 1: Modify the Program to Use a Function", "The download loop becomes a function with a start and an end number."),
        ("downloadXkcd()", "The function that gets the pages from a start to an end and saves their images."),
        ("Step 2: Create and Start Threads", "One thread is made for each range and started."),
        ("Step 3: Wait for All Threads to End", "join() is called for every thread, so the program ends after all are done."),
        ("threadedDownloadXkcd.py", "The book's file name of the finished project."),
    ]),
    ("A3", "Shared data and waiting: locks, events, semaphores, queues", "Threads share variables; a lock makes a read and a write one step, and a queue hands items from one thread to another.", [
        ("Concurrency Issues", "Two threads that change the same value can leave it wrong, because their steps interleave."),
        ("threading.Lock", "A lock that one thread holds at a time; with lock: takes and releases it."),
        ("threading.RLock", "A lock that the thread which holds it can take again."),
        ("threading.Event", "A flag that threads wait on until another thread sets it."),
        ("threading.Semaphore", "A counter that lets a fixed number of threads in at once."),
        ("queue", "The standard module for queues that threads share."),
        ("queue.Queue", "A first-in first-out queue; put() adds an item and get() waits for one."),
    ]),
    ("A4", "Pools of threads: concurrent.futures", "An executor starts and reuses threads and returns each result in a Future.", [
        ("concurrent.futures", "The standard module with thread pools and process pools."),
        ("concurrent.futures.ThreadPoolExecutor()", "A pool of threads that run the submitted calls and are reused."),
        ("executor.submit()", "Starts one call and returns a Future at once."),
        ("executor.map()", "Calls a function for every input and returns the results in the order of the inputs."),
        ("future.result()", "Waits for the call and returns its value, or raises the error of the call."),
        ("max_workers", "The number of threads of the pool; the default is the number of CPUs plus 4, at most 32."),
    ]),
    ("A5", "The global interpreter lock and the free-threaded build", "A lock lets one thread at a time run Python code in the standard build; the free-threaded build can drop it.", [
        ("The global interpreter lock", "The lock inside CPython that lets one thread at a time run Python code."),
        ("The free-threaded build", "A build of Python 3.13 and later in which threads can run Python code at the same time."),
        ("sys._is_gil_enabled()", "Tells whether the lock is on in this interpreter."),
        ("PYTHON_GIL=1", "An environment variable that switches the lock on in the free-threaded build."),
        ("InterpreterPoolExecutor", "A pool whose workers are sub-interpreters, new in Python 3.14."),
        ("concurrent.interpreters", "The module for sub-interpreters, new in Python 3.14."),
    ]),
    ("A5b", "Processes, asyncio and the end of the chapter", "A process has its own memory; asyncio runs tasks on one thread; the summary and the questions close the chapter.", [
        ("multiprocessing", "The module that runs a function in another process, with its own copy of the variables."),
        ("ProcessPoolExecutor", "A pool whose workers are processes."),
        ("subprocess", "The module that starts other programs."),
        ("subprocess.Popen()", "Starts a program and returns at once; poll() asks and wait() waits."),
        ("Launching Other Programs from Python", "The last section of the book's chapter."),
        ("asyncio", "The module for tasks that overlap their waiting on one thread."),
        ("asyncio.gather()", "Runs several awaitable calls together and collects their results."),
        ("asyncio.to_thread()", "Runs a blocking call on a thread, so that the event loop stays free."),
        ("Summary", "The chapter in a few sentences."),
        ("Practice Questions", "Questions to check the chapter."),
    ]),
]

STORIES = {
    "munroe": dict(
        title="Story: Randall Munroe began xkcd in September 2005", img="image_munroe.jpg",
        prose=["Randall Munroe, born on 17 October 1984, is an American cartoonist, author and engineer.",
               "xkcd began in September 2005, when he scanned his doodles and put them on his personal website; in January 2006 the comic moved to a site of its own.",
               "The picture shows him in Berlin in 2016. The downloader of this part works like the book's project, but a local stand-in answers and xkcd.com is never contacted."],
        linktext="xkcd (Wikipedia)", link="https://en.wikipedia.org/wiki/Xkcd"),
    "therac": dict(
        title="Story: The Therac-25 overdosed patients in 1985 to 1987", img="therac.png",
        prose=["The Therac-25 was a computer-controlled radiation therapy machine that Atomic Energy of Canada Limited produced in 1982.",
               "It was involved in at least six overdoses of radiation between 1985 and 1987, and Wikipedia names concurrent programming errors, also known as race conditions, among the causes.",
               "The picture is a newspaper photograph of the machine. The lost updates of this part are a small race of the same kind."],
        linktext="Therac-25 (Wikipedia)", link="https://en.wikipedia.org/wiki/Therac-25"),
    "dijkstra": dict(
        title="Story: Dijkstra invented the semaphore for the THE system", img="dijkstra.jpg",
        prose=["Edsger W. Dijkstra, a Dutch computer scientist, invented the semaphore in 1962 or 1963.",
               "He and his team were then developing an operating system for the Electrologica X8, which became known as the THE multiprogramming system.",
               "The picture shows him. The Semaphore of the example is the same counter: it lets two of six threads into a block."],
        linktext="Semaphore (Wikipedia)", link="https://en.wikipedia.org/wiki/Semaphore_(programming)"),
    "blackout": dict(
        title="Story: A race condition stalled the alarms in 2003", img="blackout.png",
        prose=["The blackout of 14 August 2003 affected 55 million people in the northeastern United States and Ontario.",
               "A software bug known as a race condition in General Electric Energy's XA/21 energy management system stalled the alarm system of FirstEnergy's control room for over an hour.",
               "The picture is a map of the area. A race that needs a rare timing hides in tests; part 5 shows one that appeared only on the free-threaded build."],
        linktext="Northeast blackout of 2003 (Wikipedia)", link="https://en.wikipedia.org/wiki/Northeast_blackout_of_2003"),
    "athlon": dict(
        title="Story: Dual-core desktop processors came in May 2005", img="image_athlon.jpg",
        prose=["The Athlon 64 X2 was the first native dual-core desktop processor that AMD designed.",
               "Its first models were released in May 2005, the same month as the Pentium D, the first dual-core processor of Intel.",
               "The picture shows an X2 with its heat spreader removed. Only a Python build without the lock can use both cores for Python code."],
        linktext="Athlon 64 X2 (Wikipedia)", link="https://en.wikipedia.org/wiki/Athlon_64_X2"),
}

# ---- the recorded timings (measured once on 2026-10-14; the deck never times them again) and the five interpreters (probed live) -------------------------------
_R = json.load(open(os.path.join(HERE, "..", "..", "ch25-page", "timing_record_v1_0_0.json")))["runs"]
_BUILDS = [("3.14.6", "standard 3.14.6"), ("3.14.6t", "free-threaded 3.14.6"), ("3.13.14", "3.13.14"), ("3.12.13", "3.12.13"), ("3.11.15", "3.11.15")]
_RATIO = [round(_R["cpu_" + k]["result"]["threads_4"] / _R["cpu_" + k]["result"]["serial_4_tasks"], 2) for k, _ in _BUILDS]
_LOST = [[lab] + [format(_R["race_%s_run%d" % (k, i)]["result"]["lost"], ",") for i in (1, 2, 3)] for k, lab in _BUILDS]
_PROBE = r'''
import json, sys, sysconfig, threading, concurrent.futures as cf, multiprocessing as mp
def f(): pass
r = {'Python': sys.version.split()[0]}
r['GIL on'] = str(sys._is_gil_enabled()) if hasattr(sys, '_is_gil_enabled') else 'no such call'
r['Py_GIL_DISABLED'] = str(sysconfig.get_config_var('Py_GIL_DISABLED'))
r['thread name'] = threading.Thread(target=f).name
with cf.ThreadPoolExecutor(2) as ex: r['pool map'] = str(list(ex.map(abs, [-1, -2])))
r['InterpreterPool'] = str(hasattr(cf, 'InterpreterPoolExecutor'))
r['start method'] = mp.get_start_method()
print(json.dumps(r))
'''
_U = "/root/.local/share/uv/python/"
_INTERPS = [("3.11.15", _U + "cpython-3.11-linux-x86_64-gnu/bin/python3.11"), ("3.12.13", _U + "cpython-3.12-linux-x86_64-gnu/bin/python3.12"),
            ("3.13.14", _U + "cpython-3.13-linux-x86_64-gnu/bin/python3.13"), ("3.14.6", "/home/claude/venv314_ch25_latest/bin/python"),
            ("3.14.6 free-threaded", _U + "cpython-3.14.6+freethreaded-linux-x86_64-gnu/bin/python3.14t")]


def _probe():
    res = []
    for v, p in _INTERPS:
        r = subprocess.run([p, "-W", "ignore", "-c", _PROBE], capture_output=True, text=True, stdin=subprocess.DEVNULL)
        assert r.returncode == 0, (v, r.stderr[-300:])
        res.append(json.loads(r.stdout.strip().splitlines()[-1]))
    return res


_PR = _probe()
_KEYS = ["Python", "GIL on", "Py_GIL_DISABLED", "thread name", "pool map", "InterpreterPool", "start method"]
COMPARES = {
    "record": dict(
        title="Recorded: the race and the speed on five builds", sub="Measured once on 2026-10-14 on 2 CPUs; below 1 means faster than one after another",
        colw=[1.3, 0.76, 0.76, 0.78], rowh=0.45, fs=9,
        chart=dict(label="Recorded: 4 threads divided by 4 tasks one after another", cats=[lab for _, lab in _BUILDS], series="time ratio", values=_RATIO, vmax=1.2, major=0.2),
        rows=[["Updates lost of 4,000,000", "run 1", "run 2", "run 3"]] + _LOST,
        takeaway="Only the free-threaded build lost updates and was clearly faster on 4 threads."),
    "envs": dict(
        title="Five interpreters, one probe", sub="The same program, run live under each; the cells are what it printed",
        colw=[1.7, 1.4, 1.5, 1.6, 1.4], rowh=0.42, fs=10,
        rows=[["Printed by the probe", "3.11.15", "3.12.13", "3.13.14", "3.14.6", "3.14.6 free-threaded"][:1] + [v for v, _ in _INTERPS[:4]] + ["3.14.6 free-threaded"]] +
             [[k] + [x[k] for x in _PR[:5]] for k in _KEYS[1:]],
        takeaway="The lock call exists from 3.13; the pool of interpreters only from 3.14."),
}
COMPARES["envs"]["colw"] = [1.5, 1.4, 1.4, 1.4, 1.5, 1.8]

TAKEAWAY = {
    "start": "start() runs the target beside the main thread; join() waits for it.",
    "args": "args is a list, kwargs a dictionary; a call in place of the target runs at once.",
    "life": "A thread starts once; its error stays in it and the main thread goes on.",
    "join": "join(0.1) only waits; join() waits for the end; a thread not started raises.",
    "daemon": "A daemon thread is cut off at the end; the flag is fixed at start().",
    "printed": "Without start() no request is made, and join() raises.",
    "fixed": "With start() the ranges skip every tenth number.",
    "lost": "Without a lock both threads write 1; with it the result is 2.",
    "lock": "A with statement releases the lock; an RLock can be taken twice.",
    "dead": "Two locks in opposite orders leave both threads waiting.",
    "sem": "A Semaphore of 2 keeps at most 2 threads inside.",
    "queue": "A queue hands items in order; an Event wakes a waiting thread.",
    "pool": "map() keeps the order; a pool reuses its threads.",
    "future": "The error of a thread comes out of result().",
    "gil": "The standard build has the lock; the free-threaded build can drop it.",
    "proc": "A process changes only its own copy of the variables.",
    "async": "await overlaps waiting; a blocking call stalls the loop.",
}

SUMMARY_ANALOGY = "Four claims: start and join, lock shared data, use a pool, know which tool fits."
SUMMARY_POINTS = [
    "A thread runs only after start(), and join() waits for it; the printed downloader never calls start().",
    "A shared counter needs a lock; a semaphore, an event and a queue order the threads that wait.",
    "A pool starts and reuses threads, and a Future carries the result or the error back.",
    "Threads overlap waiting; only the free-threaded build sped up CPU work.",
]
SUMMARY_TAKEAWAY = "Two questions of slide 3: how threads start, wait and end; which tool fits which work."

PRACTICE_SUB = "Use the slide of the part named in each question"
PRACTICE_ANALOGY = "Each practice question has a short answer; run the code on the chapter page to check it."
PRACTICE = [
    "What happens at join() when start() was never called, and in which order do the lines of the first example appear? Use parts 1 and 2.",
    "What does the lost-update example print without and with a lock, and what does an RLock allow that a Lock does not? Use part 3.",
    "Which result order do map() and as_completed() give, and what does result() do with an error? Use part 4.",
    "Which build lost updates in the record, and why is a blocking call a problem in asyncio? Use part 5 and slide 38.",
    "Which tool fits waiting for answers from a site, and which fits work on the CPU? Use slides 38 and 39.",
]
PRACTICE_TAKEAWAY = "Run the examples on the chapter page to check each answer."

RESOURCES_SUB = "The chapter, the documentation, and the pages behind the stories"
RESOURCES_TAKEAWAY = "13 of 13 pages opened on 2026-11-27; see the notes."
RESOURCES_ROWS = 8
RESOURCES = [
    ("Book: Automate the Boring Stuff, 2nd edition, chapter 17", "https://automatetheboringstuff.com/2e/chapter17/", "automatetheboringstuff.com"),
    ("Book: Automate the Boring Stuff, 3rd edition", "https://automatetheboringstuff.com/3e/", "automatetheboringstuff.com"),
    ("threading in the Python documentation", "https://docs.python.org/3.14/library/threading.html", "docs.python.org"),
    ("concurrent.futures in the Python documentation", "https://docs.python.org/3.14/library/concurrent.futures.html", "docs.python.org"),
    ("asyncio in the Python documentation", "https://docs.python.org/3.14/library/asyncio.html", "docs.python.org"),
    ("Python support for free threading", "https://docs.python.org/3.14/howto/free-threading-python.html", "docs.python.org"),
    ("Python Free-Threading Guide", "https://py-free-threading.github.io/", "py-free-threading.github.io"),
    ("PEP 703: making the GIL optional", "https://peps.python.org/pep-0703/", "peps.python.org"),
    ("xkcd (Wikipedia)", "https://en.wikipedia.org/wiki/Xkcd", "en.wikipedia.org"),
    ("Therac-25 (Wikipedia)", "https://en.wikipedia.org/wiki/Therac-25", "en.wikipedia.org"),
    ("Semaphore (Wikipedia)", "https://en.wikipedia.org/wiki/Semaphore_(programming)", "en.wikipedia.org"),
    ("Northeast blackout of 2003 (Wikipedia)", "https://en.wikipedia.org/wiki/Northeast_blackout_of_2003", "en.wikipedia.org"),
    ("Athlon 64 X2 (Wikipedia)", "https://en.wikipedia.org/wiki/Athlon_64_X2", "en.wikipedia.org"),
]
