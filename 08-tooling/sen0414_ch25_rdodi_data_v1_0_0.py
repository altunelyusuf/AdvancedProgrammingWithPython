"""Chapter 25 content for the RDODI build: sources, findings, taxonomy and section bodies.
Chapter 25 is the numeric slot of the Threads subject: the multithreading material of chapter 17 of the 2nd edition of Automate the Boring Stuff with Python (Keeping Time, Scheduling Tasks, and Launching Programs),
which the 3rd edition dropped (its chapter 19 of the same title has no occurrence of the word thread). The number 25 is not a chapter number of either edition.
The 2nd-edition chapter was read on automatetheboringstuff.com on 2026-10-14 (an HTTP fetch of https://automatetheboringstuff.com/2e/chapter17/; the page answered 200 with 103,558 bytes, sha256 b6b804ee11473663eeba0a399c8ddc815e6225a8e3f3ae645003cbf667302f9e); its text is paraphrased, never copied.
74 sources (the chapter and book pages of both editions, the Python 3.14 documentation of threading, concurrent.futures, multiprocessing, asyncio, queue, sys, subprocess and the free-threading guide, the PEPs on the GIL,
subinterpreters and futures, the free-threading community guide, Wikipedia articles on threads, races, locks and deadlocks, two LWN articles, the NumPy thread-safety page, the sources of threading.py and thread.py) were each fetched on the same day through the proxy of the study and
answered HTTP 200; the passage each was used for was looked for on the page (ch25-page/live_observations_v1_0_0.json). Every behaviour was executed on Ubuntu 24.04 (Linux, 2 vCPUs, 8,029 MiB, no GPU) with Python 3.14.6 (the newest 3.14 release uv offered) in a venv with requests 2.34.2 and
beautifulsoup4 4.15.0, with the free-threaded Python 3.14.6 and with Python 3.13.14, 3.12.13 and 3.11.15, all installed with uv. The chapter's downloader was run against a stand-in HTTP server on 127.0.0.1 (xkcd.com was never contacted).
The timings are in ch25-page/timing_record_v1_0_0.json (made by sen0414_ch25_live_timing_v1_0_0.py): every figure is ONE run on 2026-10-14, taken after the script waited for a one-minute load average below 1.0, and each run states the load it saw (the largest was 0.75).
Not executed, and said so where it comes up: the free-threaded build of Python 3.13; a C extension that re-enables the GIL (the documentation was read, no extension was built); Windows and macOS thread behaviour; more than 2 CPUs; the real xkcd.com site; and runs under load.
A claim not in this file was not made."""
__version__ = "1.0.0"
import os, re
CH = 25
DATE = "2026-10-14"
PYVER = "3.14.6"
TITLE = "Threads for an advanced course: chapter 25 as the Threads subject of the 2nd edition's multithreading material and today's Python 3.14.6 threading, executors, GIL and free-threaded build"
QUESTION = "What does the multithreading material of chapter 17 of the 2nd edition (the Thread object, start, the args and kwargs of the target, join, concurrency issues, the multithreaded XKCD downloader and the launching of programs) teach, which of its listings and statements still hold under Python 3.14.6, what do daemon threads, locks, queues, events, semaphores, concurrent.futures executors, the global interpreter lock and the free-threaded build add to it, how do threads compare with processes and asyncio, and what must an advanced course correct or add, given that the 3rd edition dropped the material?"
CQS = ('Which parts of the 2nd edition\'s multithreading chapter can be shown to work, fail or differ from its prose on a 2-CPU machine with Python 3.14.6, and which statements about the GIL, the free-threaded build and other platforms can only be read from documentation?',
       'How large are the differences in speed and in lost updates between the GIL build and the free-threaded build, between threads, processes and asyncio, and between Python 3.11 and 3.14, and on what recorded run and source?')

PUBS = [
 ('P01', 'Automate the Boring Stuff with Python, 2nd edition - Chapter 17, Keeping Time, Scheduling Tasks, and Launching Programs (Sweigart, 2019)', 'https://automatetheboringstuff.com/2e/chapter17/', True),
 ('P02', 'Automate the Boring Stuff with Python, 3rd edition - table of contents (Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/', False),
 ('P03', 'Automate the Boring Stuff with Python, 2nd edition - book page (No Starch Press, 2019)', 'https://nostarch.com/automatestuff2', False),
 ('P04', 'Appendix A of the 2nd edition, Installing Third-Party Modules (Sweigart, 2019)', 'https://automatetheboringstuff.com/2e/appendixa/', False),
 ('P05', 'Appendix C of the 2nd edition, Answers to the Practice Questions (Sweigart, 2019)', 'https://automatetheboringstuff.com/2e/appendixc/', False),
 ('P06', 'Automate the Boring Stuff with Python, 2nd edition - Chapter 12, Web Scraping (Sweigart, 2019)', 'https://automatetheboringstuff.com/2e/chapter12/', False),
 ('P07', 'threading - Thread-based parallelism, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/threading.html', False),
 ('P08', 'concurrent.futures - Launching parallel tasks, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/concurrent.futures.html', False),
 ('P09', 'multiprocessing - Process-based parallelism, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/multiprocessing.html', False),
 ('P10', 'asyncio - Asynchronous I/O, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/asyncio.html', False),
 ('P11', 'queue - A synchronized queue class, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/queue.html', False),
 ('P12', 'sys - System-specific parameters and functions, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/sys.html', False),
 ('P13', 'time - Time access and conversions, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/time.html', False),
 ('P14', 'subprocess - Subprocess management, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/subprocess.html', False),
 ('P15', 'sched - Event scheduler, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/sched.html', False),
 ('P16', 'concurrent.interpreters - Multiple interpreters in the same process, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/concurrent.interpreters.html', False),
 ('P17', 'Python support for free threading, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/howto/free-threading-python.html', False),
 ('P18', 'C API Extension Support for Free Threading, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/howto/free-threading-extensions.html', False),
 ('P19', 'Glossary (global interpreter lock, free threading, thread-safe), Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/glossary.html', False),
 ('P20', "What's New In Python 3.14 (Python Software Foundation, 2026)", 'https://docs.python.org/3.14/whatsnew/3.14.html', False),
 ('P21', "What's New In Python 3.13 (Python Software Foundation, 2026)", 'https://docs.python.org/3.14/whatsnew/3.13.html', False),
 ('P22', 'multiprocessing.shared_memory, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/multiprocessing.shared_memory.html', False),
 ('P23', 'Initialization, Finalization, and Threads (the GIL in the C API), Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/c-api/init.html', False),
 ('P24', 'Coroutines and Tasks (asyncio.to_thread), Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/asyncio-task.html', False),
 ('P25', 'contextvars - Context Variables, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/contextvars.html', False),
 ('P26', 'faulthandler - Dump the Python traceback, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/faulthandler.html', False),
 ('P27', 'PEP 703 - Making the Global Interpreter Lock Optional in CPython (Python Enhancement Proposals, 2023)', 'https://peps.python.org/pep-0703/', False),
 ('P28', 'PEP 779 - Criteria for supported status for free-threaded Python (Python Enhancement Proposals, 2025)', 'https://peps.python.org/pep-0779/', False),
 ('P29', 'PEP 684 - A Per-Interpreter GIL (Python Enhancement Proposals, 2022)', 'https://peps.python.org/pep-0684/', False),
 ('P30', 'PEP 734 - Multiple Interpreters in the Stdlib (Python Enhancement Proposals, 2023)', 'https://peps.python.org/pep-0734/', False),
 ('P31', 'PEP 3148 - futures - execute computations asynchronously (Python Enhancement Proposals, 2009)', 'https://peps.python.org/pep-3148/', False),
 ('P32', 'PEP 371 - Addition of the multiprocessing package (Python Enhancement Proposals, 2008)', 'https://peps.python.org/pep-0371/', False),
 ('P33', 'PEP 3156 - Asynchronous IO Support Rebooted: the asyncio Module (Python Enhancement Proposals, 2012)', 'https://peps.python.org/pep-3156/', False),
 ('P34', 'PEP 492 - Coroutines with async and await syntax (Python Enhancement Proposals, 2015)', 'https://peps.python.org/pep-0492/', False),
 ('P35', 'PEP 20 - The Zen of Python (Python Enhancement Proposals, 2004)', 'https://peps.python.org/pep-0020/', False),
 ('P36', 'Python Free-Threading Guide (Free Threading community, 2026)', 'https://py-free-threading.github.io/', False),
 ('P37', 'Porting Python Packages to Support Free-Threading (Free Threading community, 2026)', 'https://py-free-threading.github.io/porting/', False),
 ('P38', 'Compatibility status tracking of free-threaded Python (Free Threading community, 2026)', 'https://py-free-threading.github.io/tracking/', False),
 ('P39', 'Global Interpreter Lock, Python wiki (Python wiki, 2026)', 'https://wiki.python.org/moin/GlobalInterpreterLock', False),
 ('P40', 'Thread (computing) (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Thread_(computing)', False),
 ('P41', 'Race condition (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Race_condition', False),
 ('P42', 'Global interpreter lock (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Global_interpreter_lock', False),
 ('P43', 'Lock (computer science) (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Lock_(computer_science)', False),
 ('P44', 'Deadlock (computer science) (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Deadlock_(computer_science)', False),
 ('P45', 'Semaphore (programming) (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Semaphore_(programming)', False),
 ('P46', 'Thread safety (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Thread_safety', False),
 ('P47', "Amdahl's law (Wikipedia, 2026)", 'https://en.wikipedia.org/wiki/Amdahl%27s_law', False),
 ('P48', 'Producer-consumer problem (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem', False),
 ('P49', 'Concurrency (computer science) (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Concurrency_(computer_science)', False),
 ('P50', 'Dining philosophers problem (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Dining_philosophers_problem', False),
 ('P51', 'Multithreading (computer architecture) (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Multithreading_(computer_architecture)', False),
 ('P52', 'Edsger W. Dijkstra (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Edsger_W._Dijkstra', False),
 ('P53', 'Therac-25 (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Therac-25', False),
 ('P54', 'Northeast blackout of 2003 (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Northeast_blackout_of_2003', False),
 ('P55', 'Python (programming language) (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Python_(programming_language)', False),
 ('P56', 'requests on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/project/requests/', False),
 ('P57', 'numpy on the Python Package Index, release metadata (Python Package Index, 2026)', 'https://pypi.org/pypi/numpy/json', False),
 ('P58', 'Thread Safety, NumPy documentation (NumPy developers, 2026)', 'https://numpy.org/doc/stable/reference/thread_safety.html', False),
 ('P59', 'Python versions, uv documentation (Astral, 2026)', 'https://docs.astral.sh/uv/concepts/python-versions/', False),
 ('P60', 'os.cpu_count, Python documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3/library/os.html#os.cpu_count', False),
 ('P61', 'PEP 703 discussion on discuss.python.org (Python Discourse, 2023)', 'https://discuss.python.org/t/pep-703-making-the-global-interpreter-lock-optional-3-12-updated/26503', False),
 ('P62', "A viable solution for Python concurrency (LWN article on Sam Gross's nogil work) (LWN, 2021)", 'https://lwn.net/Articles/872869/', False),
 ('P63', "Gilectomy (LWN article on Larry Hastings' experiment to remove the GIL) (LWN, 2016)", 'https://lwn.net/Articles/689548/', False),
 ('P64', 'PEP 583 - A Concurrency Memory Model for Python (Python Enhancement Proposals, 2008)', 'https://peps.python.org/pep-0583/', False),
 ('P65', 'PEP 554 - Multiple Interpreters in the Stdlib (superseded) (Python Enhancement Proposals, 2017)', 'https://peps.python.org/pep-0554/', False),
 ('P66', 'Fearless Concurrency, The Rust Programming Language (Klabnik and Nichols, 2026)', 'https://doc.rust-lang.org/book/ch16-00-concurrency.html', False),
 ('P67', 'Concurrency is not parallelism (Rob Pike) (Go blog, 2013)', 'https://go.dev/blog/waza-talk', False),
 ('P68', 'dis - Disassembler for Python bytecode, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/dis.html', False),
 ('P69', 'Library and Extension FAQ (what kinds of global value mutation are thread-safe), Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/faq/library.html', False),
 ('P70', 'atexit, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/atexit.html', False),
 ('P71', 'signal - Set handlers for asynchronous events, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/signal.html', False),
 ('P72', 'threading.py source of CPython on GitHub (Python Software Foundation, 2026)', 'https://raw.githubusercontent.com/python/cpython/main/Lib/threading.py', False),
 ('P73', 'concurrent/futures/thread.py source of CPython on GitHub (Python Software Foundation, 2026)', 'https://raw.githubusercontent.com/python/cpython/main/Lib/concurrent/futures/thread.py', False),
 ('P74', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 19, Keeping Time, Scheduling Tasks, and Launching Programs (Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/chapter19.html', False),
]
PUBS.sort(key=lambda p: p[0])

CONCEPTS = [
 ('Section', 'Keeping Time, Scheduling Tasks, and Launching Programs'),
 ('Section', 'Multithreading'),
 ('Section', "Passing Arguments to the Thread's Target Function"),
 ('Section', 'Concurrency Issues'),
 ('Section', 'Project: Multithreaded XKCD Downloader'),
 ('Section', 'Step 1: Modify the Program to Use a Function'),
 ('Section', 'Step 2: Create and Start Threads'),
 ('Section', 'Step 3: Wait for All Threads to End'),
 ('Section', 'Launching Other Programs from Python'),
 ('Section', 'Practice Questions'),
 ('Section', 'Summary'),
 ('Function', 'threading.Thread()'),
 ('Function', 'threadObj.start()'),
 ('Function', 'threadObj.join()'),
 ('Function', 'time.sleep()'),
 ('Function', 'subprocess.Popen()'),
 ('Function', 'downloadXkcd()'),
 ('Function', 'threading.current_thread()'),
 ('Function', 'concurrent.futures.ThreadPoolExecutor()'),
 ('Function', 'executor.submit()'),
 ('Function', 'executor.map()'),
 ('Function', 'future.result()'),
 ('Function', 'sys._is_gil_enabled()'),
 ('Function', 'asyncio.gather()'),
 ('Function', 'asyncio.to_thread()'),
 ('Module', 'threading'),
 ('Module', 'concurrent.futures'),
 ('Module', 'multiprocessing'),
 ('Module', 'asyncio'),
 ('Module', 'queue'),
 ('Module', 'subprocess'),
 ('Module', 'concurrent.interpreters'),
 ('Option', 'target=takeANap'),
 ('Option', "args=['Cats', 'Dogs', 'Frogs']"),
 ('Option', "kwargs={'sep': ' & '}"),
 ('Option', 'daemon=True'),
 ('Option', 'PYTHON_GIL=1'),
 ('Option', 'max_workers'),
 ('File', 'threadDemo.py'),
 ('File', 'threadedDownloadXkcd.py'),
 ('Tool', 'threading.Lock'),
 ('Tool', 'threading.RLock'),
 ('Tool', 'threading.Event'),
 ('Tool', 'threading.Semaphore'),
 ('Tool', 'queue.Queue'),
 ('Tool', 'The global interpreter lock'),
 ('Tool', 'The free-threaded build'),
 ('Tool', 'InterpreterPoolExecutor'),
 ('Tool', 'ProcessPoolExecutor'),
]

FINDINGS = [
 ('F1', 'Background', 'Chapter 25 of this course is the Threads subject: the multithreading material of chapter 17 of the 2nd edition of Automate the Boring Stuff with Python, Keeping Time, Scheduling Tasks, and Launching Programs, which teaches the threading module (a Thread object with a target, start(), the args and kwargs of the target, join(), concurrency issues, and the multithreaded XKCD downloader project) and then launching programs with subprocess.Popen, and ends with practice questions 7 and 8 on threads [P01] [P03]. The page was fetched on 2026-10-14, answered 200 with 103,558 bytes, and its multithreading section holds 9 code paragraphs; the number 25 is the numeric slot of this package and not a chapter number of either edition [P01].', ['P01', 'P03']),
 ('F2', 'Dropped from the 3rd edition', "Chapter 19 of the 3rd edition, which has the same title as chapter 17 of the 2nd, answered 200 with 0 occurrences of the word thread and still teaches the subprocess module, so the multithreading material is not in the 3rd edition; the 3rd edition's table of contents lists the chapter under that title [P74] [P02].", ['P74', 'P02']),
 ('F3', 'The chapter replayed', "The chapter's listings that are executable offline ran on Python 3.14.6: threadDemo.py printed Start of program., End of program. and Wake up! in that order; the call with args=['Cats', 'Dogs', 'Frogs'] and kwargs={'sep': ' & '} printed Cats & Dogs & Frogs; the incorrect form target=print(...) printed at once in the main thread and gave the thread no target [P01] [P07].", ['P01', 'P07']),
 ('F4', 'A one-character difference in the prose', "The chapter's explanation writes the keyword dictionary as {'sep': '& '} while its listing writes {'sep': ' & '}; run as the prose writes it, the output is Cats& Dogs& Frogs [P01].", ['P01']),
 ('F5', 'The printed downloader does not start its threads', "Run exactly as the chapter's Step 2 listing prints it, threadedDownloadXkcd.py against a local stand-in server (127.0.0.1, not xkcd.com) made 0 requests and ended with return code 1 and RuntimeError: cannot join thread before it is started, because the loop appends the Thread objects and nothing calls start(); the prose says the loop calls start() [P01] [P07] [P72].", ['P01', 'P07', 'P72']),
 ('F6', 'The downloader skips every tenth comic', 'With one line added to start each thread, the downloader requested 125 of the 139 comic numbers its loop covers and saved 125 files; the 14 comics 9, 19, 29 and so on up to 139 were never requested, because each thread runs range(start, end) with end equal to the last number of its block [P01] [P06].', ['P01', 'P06']),
 ('F7', 'Threads speed up waiting', 'Against a stand-in server that waits 0.05 s per request, the 14-thread downloader finished at least 5 times faster than one thread doing the same 250 requests; eight sleeps of 0.5 s took 4.001 s one after another and 0.502 s on 8 threads, 0.502 s in a pool and 0.501 s with asyncio on the GIL build, and 0.503 s on 8 threads on the free-threaded build, all single runs on a machine whose load average was below 1.0 [P07] [P08] [P10] [P56].', ['P07', 'P08', 'P10', 'P56']),
 ('F8', 'The advice of the chapter', 'The chapter tells the reader to avoid concurrency issues by never letting threads read or write the same variables and by using only local variables in the target function, and calls multithreading beyond its scope; four threads that each summed their own list returned the four expected totals, a threading.local value set in a thread was absent in the main thread, and the chapter names no lock, queue or executor [P01] [P07] [P11] [P46].', ['P01', 'P07', 'P11', 'P46']),
 ('F9', 'Lost updates', 'Two threads that each read a shared counter, waited 0.05 s and wrote back the value plus one left it at 1 instead of 2 in all 3 runs, and at 2 with a lock; counter += 1 compiled to 5 bytecode steps on Python 3.14.6, among them LOAD_GLOBAL, BINARY_OP and STORE_GLOBAL, so it is not one step [P41] [P68] [P69] [P07].', ['P41', 'P68', 'P69', 'P07']),
 ('F10', 'The race on the GIL and without it', 'Four threads that each ran counter += 1 one million times lost no update in any of 3 runs on Python 3.14.6 with the GIL or on 3.13.14, 3.12.13 and 3.11.15, and lost between 2,500,522 and 2,913,206 of 4,000,000 updates in each of 3 runs on the free-threaded 3.14.6 build; no loss in a run proves nothing, and the free-threaded numbers are single runs [P27] [P17] [P42] [P39].', ['P27', 'P17', 'P42', 'P39']),
 ('F11', 'Locks, events, semaphores and queues', 'A lock around the update gave the exact 400,000; a plain Lock asked twice by the same thread timed out while an RLock did not; two threads taking two locks in opposite orders were both still alive after 1.0 s (a deadlock); a BoundedSemaphore of 2 held the number of threads inside a block at 2 instead of 6; an Event released a waiting thread; and a queue.Queue handed 5 items in order from a producer to a consumer [P07] [P11] [P43] [P44] [P45] [P50] [P48].', ['P07', 'P11', 'P43', 'P44', 'P45', 'P50', 'P48']),
 ('F12', 'join, timeouts and daemon threads', 'join() waited for the thread and returned None; join(0.1) returned after about 0.1 s with the thread still alive; join() on a thread never started raised RuntimeError; a daemon thread that would print after 1 s printed nothing because the program ended, the same thread as a non-daemon thread printed; the daemon flag could not be set after start() and a thread inherited it from its creator; an exception in a thread went to standard error and the main thread ended with return code 0 [P07] [P12] [P70] [P13].', ['P07', 'P12', 'P70', 'P13']),
 ('F13', 'Executors', 'ThreadPoolExecutor.map returned results in the order of the inputs (0, 1, 2) for tasks that finished in the opposite order, as_completed yielded them in completion order (2, 1, 0), an exception stayed in the Future until result(), result(timeout=0.1) raised TimeoutError, the default max_workers was 6 on 2 CPUs, shutdown(cancel_futures=True) cancelled 4 of 5 queued tasks, and leaving the with block waited for the slowest task [P08] [P31] [P73].', ['P08', 'P31', 'P73']),
 ('F14', 'The global interpreter lock and the free-threaded build', 'On the standard Python 3.14.6 build sys._is_gil_enabled() was True and Py_GIL_DISABLED was 0; the free-threaded 3.14.6 installed with uv reported False and 1, PYTHON_GIL=1 and -X gil=1 turned the lock on, and four CPU-bound tasks took 0.89 s serially and 1.003 s on 4 threads on the GIL build, but 1.292 s serially and 0.522 s on 4 threads on the free-threaded build on 2 CPUs; the free-threaded serial run was slower than the GIL one, and every figure is one run [P27] [P28] [P17] [P19] [P21] [P20] [P59] [P12].', ['P27', 'P28', 'P17', 'P19', 'P21', 'P20', 'P59', 'P12']),
 ('F15', 'Extensions and the ecosystem', 'The Python documentation says some third-party packages with an extension module may not be ready for a free-threaded build and will re-enable the GIL; this study built no such extension, so the behaviour was NOT EXECUTED, and the pages on porting, compatibility and thread safety were read, not run [P17] [P18] [P36] [P37] [P38] [P58] [P57] [P23].', ['P17', 'P18', 'P36', 'P37', 'P38', 'P58', 'P57', 'P23']),
 ('F16', 'Other interpreters', 'On Python 3.11.15, 3.12.13 and 3.13.14 the 4-thread run of the CPU-bound loop took at least 0.8 of the serial time, the same picture as 3.14.6 with the GIL; Python 3.14.6 has concurrent.futures.InterpreterPoolExecutor and concurrent.interpreters, whose worker ran in the same process; the first free-threaded build, that of Python 3.13, was NOT EXECUTED [P21] [P20] [P16] [P29] [P30] [P65] [P64].', ['P21', 'P20', 'P16', 'P29', 'P30', 'P65', 'P64']),
 ('F17', 'Processes', "A child process that set a module variable left the parent's copy unchanged while a thread changed it; subprocess.Popen returned in under 0.5 s for a program that slept 1 s; the default start method of multiprocessing was forkserver on Python 3.14.6, which the documentation says replaced fork in 3.14; in the recorded run, four CPU-bound tasks took 0.963 s serially and 0.667 s on a pool of 2 processes, and starting a thread cost 112 microseconds against 5.4 milliseconds for a process [P09] [P14] [P32] [P22] [P20].", ['P09', 'P14', 'P32', 'P22', 'P20']),
 ('F18', 'asyncio', 'Ten coroutines that awaited asyncio.sleep(0.3) finished together in under 0.6 s on one thread; five coroutines that called the blocking time.sleep(0.2) took at least 1.0 s; and asyncio.to_thread ran five blocking 0.2 s calls in worker threads in under 0.6 s [P10] [P24] [P33] [P34] [P25].', ['P10', 'P24', 'P33', 'P34', 'P25']),
 ('F19', 'The choice of tool', "For waiting, threads, a pool and asyncio were equal on the timer; for CPU-bound work the GIL build needed processes (or interpreters) and the free-threaded build could use threads, at the cost of a slower single thread; Amdahl's law bounds the gain on any number of CPUs, and the Rust and Go documents show how other languages frame the same choice [P47] [P49] [P51] [P40] [P66] [P67] [P35].", ['P47', 'P49', 'P51', 'P40', 'P66', 'P67', 'P35']),
 ('F20', 'Scheduling by sleeping', 'The chapter motivates threads with a loop that calls time.sleep(1) until a start date; the standard library also has the sched module for events at a time, and signal for asynchronous events in the main thread [P01] [P13] [P15] [P71] [P26].', ['P01', 'P13', 'P15', 'P71', 'P26']),
 ('F21', 'Stories behind the vocabulary', "The article on the Therac-25 says concurrent programming errors, also known as race conditions, sometimes gave patients radiation doses up to 250 times higher than normal; the article on the blackout of 2003 says a race condition in an energy management system stalled the control room alarms for over an hour; and Dijkstra's name belongs to the semaphore and the dining philosophers [P53] [P54] [P52] [P45] [P50].", ['P53', 'P54', 'P52', 'P45', 'P50']),
 ('F22', 'The history of the lock', "Larry Hastings' Gilectomy experiment, Sam Gross's nogil work and PEP 703 with its discussion are the line from the lock to the optional lock; the study read the two LWN articles and the discussion page and used them for names and dates, not for measurements [P62] [P63] [P61] [P27] [P55].", ['P62', 'P63', 'P61', 'P27', 'P55']),
 ('F23', 'Thread names and limits', "On Python 3.14.6 the first thread of a process was named Thread-1 (f) with the function name in brackets, a pool with thread_name_prefix='dl' named its workers dl_0 and dl_1, a thread had 2 thread objects alive while it ran, and 2,000 threads waiting on one Event all lived at the same time in this container; the limit of another machine was not searched for [P07] [P08] [P60].", ['P07', 'P08', 'P60']),
 ('F24', 'The sources', "All 74 sources answered HTTP 200 on 2026-10-14 through the proxy of the study and the passage each was used for was found on the page; the Python documentation was read for version 3.14, whose pages announce unreleased changes of 3.14.8, and the sources of CPython's threading.py and concurrent/futures/thread.py were read from the main branch [P72] [P73] [P35] [P04] [P05]; Appendix A of the 2nd edition was read for the installs and Appendix C for the answers to the chapter's questions.", ['P72', 'P73', 'P35', 'P04', 'P05']),
 ('F25', 'What did not run', 'Not executed: the free-threaded build of Python 3.13, a C extension that re-enables the lock, Windows and macOS thread behaviour, more than 2 CPUs, the real xkcd.com site (a stand-in server on 127.0.0.1 was used), a load above 1.0, and the Appendix C answers beyond their text; the machine had 2 CPUs and the timings wait for a load average below 1.0 [P01] [P05] [P17] [P59].', ['P01', 'P05', 'P17', 'P59']),
]

def X(code):
    """An executable example as one expression with no double quote and no line break: the code runs in a fresh
    namespace and the value of its variable out is the result."""
    lit = "'" + code.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace('"', "\\x22") + "'"
    return "(lambda g: (exec(%s, g), g['out'])[1])({})" % lit

# The helpers every example starts: J reads the records of the study in 08-tooling/ch25-page; py and pyf run code under a named interpreter (LATEST, FT, P313, P312 and P311 are the interpreters of this machine); serve and bookrun are the stand-in server and the chapter's downloader.
_PRE = 'import io, os, sys, re, json, time, tempfile, warnings, subprocess, importlib.metadata as md\nwarnings.simplefilter(\'ignore\')\nLATEST = os.environ.get(\'CH25_LATEST\', \'/home/claude/venv314_ch25_latest/bin/python\')\nFT = os.environ.get(\'CH25_FT\', \'/root/.local/share/uv/python/cpython-3.14.6+freethreaded-linux-x86_64-gnu/bin/python3.14t\')\nP313 = os.environ.get(\'CH25_P313\', \'/root/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin/python3.13\')\nP312 = os.environ.get(\'CH25_P312\', \'/root/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12\')\nP311 = os.environ.get(\'CH25_P311\', \'/root/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11\')\nR = \'/home/claude/AdvancedProgrammingWithPython/08-tooling/ch25-page/\'\ndef J(n): return json.load(open(R + n + \'_v1_0_0.json\'))\ndef py(code, exe=None, limit=120, env=None):\n    # runs code in a new interpreter: (return code, stdout, last stderr line)\n    try: r = subprocess.run([exe or LATEST, \'-W\', \'ignore\', \'-c\', code], capture_output=True, text=True, timeout=limit, stdin=subprocess.DEVNULL, env=env)\n    except subprocess.TimeoutExpired: return (None, \'NO RETURN\', \'\')\n    return (r.returncode, r.stdout.strip(), (r.stderr.strip().splitlines() or [\'\'])[-1][:160])\ndef pyf(code, exe=None, limit=120):\n    # like py(), but the code is run from a file, which multiprocessing needs\n    fd, p = tempfile.mkstemp(suffix=\'.py\'); os.write(fd, code.encode()); os.close(fd)\n    try: r = subprocess.run([exe or LATEST, \'-W\', \'ignore\', p], capture_output=True, text=True, timeout=limit, stdin=subprocess.DEVNULL)\n    except subprocess.TimeoutExpired: return (None, \'NO RETURN\', \'\')\n    return (r.returncode, r.stdout.strip(), (r.stderr.strip().splitlines() or [\'\'])[-1][:160])\ndef lines(code, exe=None, limit=120): return py(code, exe, limit)[1].splitlines()\ndef quiet(limit=1.0, wait=60):\n    # waits until the one-minute load average is below limit (a quiet machine) and returns the load seen\n    t0 = time.time()\n    while os.getloadavg()[0] > limit and time.time() - t0 < wait: time.sleep(2)\n    return round(os.getloadavg()[0], 1)\ndef cpu(n): return \'x = 0\\nfor i in range(%d): x += i * i\\n\' % n\n\nimport threading, http.server\ndef serve(delay=0.0, n=999):\n    # a local stand-in for xkcd.com (127.0.0.1, not the real site): page /N has one comic image, /img/N.png is 100 bytes; every request waits delay seconds; hits records the paths served\n    hits = []\n    class H(http.server.BaseHTTPRequestHandler):\n        def log_message(self, *a): pass\n        def do_GET(self):\n            hits.append(self.path); time.sleep(delay)\n            if self.path.startswith(\'/img/\'): body, ct = b\'x\' * 100, \'image/png\'\n            else: body, ct = (\'<html><body><div id="comic"><img src="http://127.0.0.1:%d/img/%s.png"></div></body></html>\' % (self.server.server_port, self.path.strip(\'/\'))).encode(), \'text/html\'\n            self.send_response(200); self.send_header(\'Content-Type\', ct); self.send_header(\'Content-Length\', str(len(body))); self.end_headers(); self.wfile.write(body)\n    h = http.server.ThreadingHTTPServer((\'127.0.0.1\', 0), H); h.daemon_threads = True\n    threading.Thread(target=h.serve_forever, daemon=True).start()\n    return h, h.server_port, hits\nBOOK = """import requests, os, bs4, threading, sys\nBASE = sys.argv[1]\nos.makedirs(\'xkcd\', exist_ok=True)\ndef downloadXkcd(startComic, endComic):\n    for urlNumber in range(startComic, endComic):\n        res = requests.get(BASE + \'/%s\' % (urlNumber))\n        res.raise_for_status()\n        soup = bs4.BeautifulSoup(res.text, \'html.parser\')\n        comicElem = soup.select(\'#comic img\')\n        if comicElem == []:\n            print(\'Could not find comic image.\')\n        else:\n            comicUrl = comicElem[0].get(\'src\')\n            res = requests.get(comicUrl)\n            res.raise_for_status()\n            imageFile = open(os.path.join(\'xkcd\', os.path.basename(comicUrl)), \'wb\')\n            for chunk in res.iter_content(100000):\n                imageFile.write(chunk)\n            imageFile.close()\ndownloadThreads = []\nfor i in range(0, 140, 10):\n    start = i\n    end = i + 9\n    if start == 0:\n        start = 1\n    downloadThread = threading.Thread(target=downloadXkcd, args=(start, end))\n    downloadThreads.append(downloadThread)\n    START\nfor downloadThread in downloadThreads:\n    downloadThread.join()\nprint(\'Done.\')\n"""\ndef bookrun(variant, delay=0.0):\n    # runs the book\'s downloader against the local stand-in; variant \'printed\' has no start() call, \'fixed\' calls start(); returns (seconds, comic pages requested, image requests, files saved, stdout, last stderr line, return code)\n    h, port, hits = serve(delay); d = tempfile.mkdtemp(); code = BOOK.replace(\'    START\', \'    downloadThread.start()\' if variant == \'fixed\' else \'    pass\')\n    t0 = time.time(); r = subprocess.run([LATEST, \'-c\', code, \'http://127.0.0.1:%d\' % port], capture_output=True, text=True, cwd=d, timeout=250); el = time.time() - t0\n    h.shutdown(); pages = sorted(int(p.strip(\'/\')) for p in hits if not p.startswith(\'/img/\')); imgs = [p for p in hits if p.startswith(\'/img/\')]\n    return el, pages, len(imgs), len(os.listdir(d + \'/xkcd\')) if os.path.isdir(d + \'/xkcd\') else 0, r.stdout.strip(), (r.stderr.strip().splitlines() or [\'\'])[-1], r.returncode\n'

TAX = [
 ('ThreadBasics', 'StartingThreads', 'StartAThread', 'threading.Thread(target=takeANap).start()',
  "The chapter's threadDemo.py, with the nap shortened to 0.3 s, printed ['Start of program.', 'End of program.', 'Wake up!'] in that order: the new thread's text came last although start() was called before the main thread's last line.",
  (X(_PRE + 'code = "import threading, time\\nprint(\'Start of program.\')\\ndef takeANap():\\n    time.sleep(0.3)\\n    print(\'Wake up!\')\\nthreadObj = threading.Thread(target=takeANap)\\nthreadObj.start()\\nprint(\'End of program.\')"\nout = (lines(code),)'), "(['Start of program.', 'End of program.', 'Wake up!'],)")),
 ('ThreadBasics', 'StartingThreads', 'ProgramWaitsForThreads', 'A Python program will not terminate until all its threads have terminated',
  'The process of the threadDemo.py shape ended with return code 0; it lasted at least the 0.5 s nap of the second thread (that test was True) although the main thread had printed its last line within 0.2 s (that test was True), so the program lives as long as its slowest non-daemon thread.',
  (X(_PRE + 'code = "import threading, time\\nt0 = time.time()\\nthreading.Thread(target=time.sleep, args=[0.5]).start()\\nprint(\'main done %.1f\' % (time.time() - t0))"\nt0 = time.time(); r = py(code); el = time.time() - t0\nout = (r[0], el >= 0.5, float(r[1].split()[2]) < 0.2)'), '(0, True, True)')),
 ('ThreadBasics', 'StartingThreads', 'MainThreadIsAThread', 'threading.current_thread()',
  "The main program ran in a thread named MainThread whose is_main_thread test was True; a new thread was named Thread-1 (f) and it saw 2 thread objects alive while it ran, so the chapter's single finger is the main thread and every start() adds one.",
  (X(_PRE + 'box = []\ndef f(): box.append((threading.current_thread().name, threading.active_count()))\nt = threading.Thread(target=f); t.start(); t.join()\nout = (threading.current_thread().name, threading.current_thread() is threading.main_thread(), box[0][0], box[0][1])'), "('MainThread', True, 'Thread-1 (f)', 2)")),
 ('ThreadBasics', 'ArgumentsOfThreads', 'ArgsAndKwargs', "threading.Thread(target=print, args=['Cats', 'Dogs', 'Frogs'], kwargs={'sep': ' & '})",
  "The chapter's call with args=['Cats', 'Dogs', 'Frogs'] and kwargs={'sep': ' & '} printed Cats & Dogs & Frogs, so the list becomes the positional arguments and the dictionary the keyword arguments of the target.",
  (X(_PRE + 'code = "import threading\\nt = threading.Thread(target=print, args=[\'Cats\', \'Dogs\', \'Frogs\'], kwargs={\'sep\': \' & \'})\\nt.start()\\nt.join()"\nout = (py(code)[1],)'), "('Cats & Dogs & Frogs',)")),
 ('ThreadBasics', 'ArgumentsOfThreads', 'SepTypoInProse', "kwargs={'sep': '& '}",
  "The chapter's explanation writes the dictionary as {'sep': '& '} without the space before the ampersand, while its listing has ' & '; run as the prose writes it, the output is Cats& Dogs& Frogs, so the prose differs from the listing in one character.",
  (X(_PRE + 'code = "import threading\\nt = threading.Thread(target=print, args=[\'Cats\', \'Dogs\', \'Frogs\'], kwargs={\'sep\': \'& \'})\\nt.start()\\nt.join()"\nout = (py(code)[1],)'), "('Cats& Dogs& Frogs',)")),
 ('ThreadBasics', 'ArgumentsOfThreads', 'WrongCallRunsNow', "threading.Thread(target=print('Cats', 'Dogs', 'Frogs', sep=' & '))",
  'The incorrect form from the chapter printed Cats & Dogs & Frogs at once in the main thread and handed the thread None as its target, and the thread was alive afterwards: False, since it had nothing to run.',
  (X(_PRE + "box = []\nimport contextlib\nbuf = io.StringIO()\nwith contextlib.redirect_stdout(buf):\n    t = threading.Thread(target=print('Cats', 'Dogs', 'Frogs', sep=' & '))\n    t.start(); t.join()\nout = (buf.getvalue().strip(), 'None', t.is_alive())"), "('Cats & Dogs & Frogs', 'None', False)")),
 ('ThreadBasics', 'ThreadObjectsInfo', 'ThreadNames', 'threading.Thread(target=f).name',
  "On Python 3.14.6 the first thread created in a process is named Thread-1 (f), the second Thread-2 (f), and a thread given name='copier' keeps it; the number counts every thread made so far and the function name was added to the default name in Python 3.10.",
  (X(_PRE + "names = []\ndef f(): pass\na = threading.Thread(target=f); b = threading.Thread(target=f); c = threading.Thread(target=f, name='copier')\nout = (a.name, b.name, c.name)"), "('Thread-1 (f)', 'Thread-2 (f)', 'copier')")),
 ('ThreadBasics', 'ThreadObjectsInfo', 'StartOnce', 'threadObj.start(); threadObj.start()',
  "Calling start() a second time on the same Thread object raised RuntimeError: threads can only be started once, so a thread object is single use and the chapter's loop makes a new Thread for each range.",
  (X(_PRE + "t = threading.Thread(target=lambda: None); t.start(); t.join()\ntry: t.start(); out = ('nothing', '')\nexcept Exception as e: out = (type(e).__name__, str(e))"), "('RuntimeError', 'threads can only be started once')")),
 ('ThreadBasics', 'ThreadObjectsInfo', 'ExceptionInThread', 'threading.excepthook',
  'An exception raised in a thread printed ValueError: boom on standard error and the main thread went on and ended with return code 0; the main thread never saw the exception, which is why a thread needs its own try and except.',
  (X(_PRE + 'code = "import threading\\ndef f(): raise ValueError(\'boom\')\\nt = threading.Thread(target=f); t.start(); t.join()\\nprint(\'main continues\')"\nr = py(code)\nout = (r[2].split(\':\')[0] + \': boom\' if \'boom\' in r[2] else r[2], r[0]) if r[1] == \'main continues\' else (\'lost\', r[0])'), "('ValueError: boom', 0)")),
 ('JoinAndDaemon', 'JoiningThreads', 'JoinWaits', 'threadObj.join()',
  'join() on a thread that slept 0.4 s returned after at least 0.4 s (True), the thread was no longer alive afterwards (True), and a second join() on a finished thread returned within 0.05 s (True), as the chapter says.',
  (X(_PRE + 't = threading.Thread(target=time.sleep, args=[0.4]); t.start()\nt0 = time.time(); t.join(); el = time.time() - t0\nt1 = time.time(); t.join(); el2 = time.time() - t1\nout = (el >= 0.39, t.is_alive() is False, el2 < 0.05)'), '(True, True, True)')),
 ('JoinAndDaemon', 'JoiningThreads', 'JoinTimeout', 'threadObj.join(timeout=0.1)',
  'join(0.1) on a thread that slept 0.6 s returned after about 0.1 s (True) with is_alive() still True, and returned nothing (None), so the caller must test is_alive() to know whether the thread finished.',
  (X(_PRE + 't = threading.Thread(target=time.sleep, args=[0.6]); t.start()\nt0 = time.time(); r = t.join(0.1); el = time.time() - t0\nout = (0.09 <= el < 0.3, t.is_alive(), r)\nt.join()'), '(True, True, None)')),
 ('JoinAndDaemon', 'JoiningThreads', 'JoinBeforeStart', 'threadObj.join()  # never started',
  'join() on a thread that was never started raised RuntimeError: cannot join thread before it is started.',
  (X(_PRE + "t = threading.Thread(target=lambda: None)\ntry: t.join(); out = ('nothing', '')\nexcept Exception as e: out = (type(e).__name__, str(e))"), "('RuntimeError', 'cannot join thread before it is started')")),
 ('JoinAndDaemon', 'DaemonThreads', 'DaemonDiesWithProgram', 'threading.Thread(daemon=True)',
  "A daemon thread that would print after 1 s did not print because the program ended first, with output ['end'] and a run of under 0.8 s (True), while the same thread as a non-daemon thread printed ['end', 'late'].",
  (X(_PRE + 'tmpl = "import threading, time\\ndef f():\\n    time.sleep(1)\\n    print(\'late\')\\nthreading.Thread(target=f, daemon=%s).start()\\nprint(\'end\')"\nt0 = time.time(); a = py(tmpl % True); el = time.time() - t0\nb = py(tmpl % False)\nout = (a[1].splitlines(), el < 0.8, b[1].splitlines())'), "(['end'], True, ['end', 'late'])")),
 ('JoinAndDaemon', 'DaemonThreads', 'DaemonAfterStart', 't.daemon = True after start()',
  'Setting daemon on a thread that had already started raised RuntimeError: cannot set daemon status of active thread; the flag can only be set before start().',
  (X(_PRE + "t = threading.Thread(target=time.sleep, args=[0.2]); t.start()\ntry: t.daemon = True; out = ('nothing', '')\nexcept Exception as e: out = (type(e).__name__, str(e))\nt.join()"), "('RuntimeError', 'cannot set daemon status of active thread')")),
 ('JoinAndDaemon', 'DaemonThreads', 'DaemonInherited', 'threading.Thread(daemon=None)',
  'A thread created without the daemon argument inherits it from its creator: a thread made inside a daemon thread had daemon True, one made in the main thread had False.',
  (X(_PRE + 'box = []\ndef inner(): box.append(threading.current_thread().daemon)\ndef outer():\n    t = threading.Thread(target=inner); t.start(); t.join()\na = threading.Thread(target=outer, daemon=True); a.start(); a.join()\nb = threading.Thread(target=lambda: None)\nout = (box[0], b.daemon)'), '(True, False)')),
 ('JoinAndDaemon', 'TheXkcdDownloader', 'PrintedListingJoinFails', 'downloadThread.join()  # no start() in Step 2',
  "The chapter's threadedDownloadXkcd.py, run exactly as the two listings print it against a local stand-in server (127.0.0.1, not xkcd.com), requested 0 pages and 0 images and saved 0 files, because the loop only appends the Thread objects and nothing calls start(); it ended with return code 1 and the message RuntimeError: cannot join thread before it is started.",
  (X(_PRE + "r = bookrun('printed')\nout = (len(r[1]), r[2], r[3], r[6], r[5])"), "(0, 0, 0, 1, 'RuntimeError: cannot join thread before it is started')")),
 ('JoinAndDaemon', 'TheXkcdDownloader', 'FixedListingSkipsComics', 'range(startComic, endComic)',
  'With one line added to start each thread, the downloader requested 125 comic pages for the 139 numbers the loop covers and saved 125 files; 14 comics, among them [9, 19, 29, 39, 49], were never requested, because each thread downloads range(start, end) and end is the last number of its block, so every 10th comic is skipped.',
  (X(_PRE + "f = bookrun('fixed')\nmiss = [n for n in range(1, 140) if n not in f[1]]\nout = (len(f[1]), f[3], miss[:5], len(miss))"), '(125, 125, [9, 19, 29, 39, 49], 14)')),
 ('JoinAndDaemon', 'TheXkcdDownloader', 'ThreadsSpeedUpWaiting', '14 threads against 1 thread',
  'Against a stand-in server that waits 0.05 s per request, the 14-thread downloader finished at least 5 times faster than one thread doing the same 250 requests: True; the seconds of this single run, taken after waiting for a quiet machine, are in the timing record.',
  (X(_PRE + 'quiet()\nh, port, hits = serve(0.05); d = tempfile.mkdtemp(); t0 = time.time()\ncode = "import requests, sys\\nfor n in range(1, 126):\\n    requests.get(sys.argv[1] + \'/%d\' % n)\\n    requests.get(sys.argv[1] + \'/img/%d.png\' % n)"\nsubprocess.run([LATEST, \'-c\', code, \'http://127.0.0.1:%d\' % port], cwd=d, timeout=250); h.shutdown(); s = time.time() - t0\nf = bookrun(\'fixed\', 0.05)\nout = (s / f[0] >= 5, len(hits))'), '(True, 250)')),
 ('SharedDataAndLocks', 'LostUpdates', 'IncrementIsSeveralSteps', 'counter += 1',
  "The statement counter += 1 in a function compiled to 5 bytecode steps on Python 3.14.6, among them ['LOAD_GLOBAL', 'BINARY_OP', 'STORE_GLOBAL'], so a thread can be stopped between the read and the write of the variable; it is not one indivisible step.",
  (X(_PRE + "import dis\nc = 0\ndef inc():\n    global c\n    c += 1\nnames = [i.opname for i in dis.get_instructions(inc) if i.opname not in ('RESUME', 'RETURN_CONST', 'RETURN_VALUE', 'CACHE')]\nout = (len(names), [n for n in names if n.startswith(('LOAD_GLOBAL', 'BINARY_OP', 'STORE_GLOBAL'))])"), "(5, ['LOAD_GLOBAL', 'BINARY_OP', 'STORE_GLOBAL'])")),
 ('SharedDataAndLocks', 'LostUpdates', 'ForcedLostUpdate', 'read, wait, write',
  'Two threads that each read a shared counter, waited 0.05 s and wrote back the value plus one left the counter at 1 instead of 2, in all 3 runs, because both read 0 before either wrote; with a lock around the read and write it ended at 2.',
  (X(_PRE + 'def trial(use_lock):\n    box = [0]; lk = threading.Lock()\n    def f():\n        if use_lock: lk.acquire()\n        v = box[0]; time.sleep(0.05); box[0] = v + 1\n        if use_lock: lk.release()\n    ts = [threading.Thread(target=f) for _ in range(2)]\n    [t.start() for t in ts]; [t.join() for t in ts]; return box[0]\nr = {trial(False) for _ in range(3)}\nout = (sorted(r)[0] if len(r) == 1 else sorted(r), 3, trial(True))'), '(1, 3, 2)')),
 ('SharedDataAndLocks', 'LostUpdates', 'SwitchInterval', 'sys.getswitchinterval()',
  'On Python 3.14.6 the thread switch interval was 0.005 s, setswitchinterval(0.0001) changed it to 0.0001 s, and the value is a request that only matters to threads that hold the global interpreter lock.',
  (X(_PRE + 'a = sys.getswitchinterval(); sys.setswitchinterval(0.0001); b = round(sys.getswitchinterval(), 6); sys.setswitchinterval(a)\nout = (a, b)'), '(0.005, 0.0001)')),
 ('SharedDataAndLocks', 'LostUpdates', 'RaceInTheRecord', '4 threads x 1,000,000 times counter += 1',
  'In the timing record, 4 threads that each ran counter += 1 one million times lost updates in 0 of 3 runs on Python 3.14.6 with the GIL, 3 of 3 on the free-threaded build, and 0 of 3, 0 of 3 and 0 of 3 on 3.13, 3.12 and 3.11; the lost counts are in the record and are single runs, so the absence of a lost update in one run proves nothing.',
  (X(_PRE + "rec = J('timing_record')['runs']\ndef n(k): return sum(1 for i in (1, 2, 3) if rec['race_%s_run%d' % (k, i)]['result']['lost'] > 0)\nout = (n('3.14.6'), n('3.14.6t'), n('3.13.14'), n('3.12.13'), n('3.11.15'))"), '(0, 3, 0, 0, 0)')),
 ('SharedDataAndLocks', 'LocksAndEvents', 'LockFixesCounter', 'with lock: counter += 1',
  'Four threads that each added 1 to a shared counter 100,000 times inside a with-lock block ended at 400000, the exact total (True); the lock makes the read and the write one step for the threads that use it.',
  (X(_PRE + 'box = [0]; lk = threading.Lock()\ndef f():\n    for _ in range(100000):\n        with lk: box[0] += 1\nts = [threading.Thread(target=f) for _ in range(4)]\n[t.start() for t in ts]; [t.join() for t in ts]\nout = (box[0], box[0] == 400000)'), '(400000, True)')),
 ('SharedDataAndLocks', 'LocksAndEvents', 'LockReleasedOnError', 'with lock:  # an exception inside',
  'After an exception inside a with-lock block the lock was still locked: False (the with statement had released it), whereas acquire() without release() left it locked: True, which is the reason to prefer the with statement.',
  (X(_PRE + 'lk = threading.Lock()\ntry:\n    with lk: raise ValueError\nexcept ValueError: pass\na = lk.locked()\nlk2 = threading.Lock(); lk2.acquire()\nout = (a, lk2.locked())'), '(False, True)')),
 ('SharedDataAndLocks', 'LocksAndEvents', 'LockNotReentrant', 'lock.acquire(timeout=0.2)',
  'A thread that already held a plain Lock and asked for it again with a 0.2 s timeout got False, while the same request on an RLock got True; without a timeout the first would wait forever.',
  (X(_PRE + 'lk = threading.Lock(); rk = threading.RLock()\nlk.acquire(); rk.acquire()\nout = (lk.acquire(timeout=0.2), rk.acquire(timeout=0.2))'), '(False, True)')),
 ('SharedDataAndLocks', 'LocksAndEvents', 'DeadlockWithTwoLocks', 'two locks taken in opposite orders',
  'Two threads that took two locks in opposite orders with a pause between them were both still alive after a join(1.0) (True and True); the program was stuck, and the process had to end through daemon threads, which is the deadlock that the Wikipedia article describes.',
  (X(_PRE + 'a = threading.Lock(); b = threading.Lock()\ndef f(x, y):\n    with x:\n        time.sleep(0.1)\n        with y: pass\nt1 = threading.Thread(target=f, args=(a, b), daemon=True); t2 = threading.Thread(target=f, args=(b, a), daemon=True)\nt1.start(); t2.start(); t1.join(1.0); t2.join(1.0)\nout = (t1.is_alive(), t2.is_alive())'), '(True, True)')),
 ('SharedDataAndLocks', 'LocksAndEvents', 'EventSignals', 'threading.Event().wait()',
  "A thread waiting on an Event stayed blocked for the 0.3 s before set() was called (True) and went on right after it (True); Event is the tool for 'wait until another thread says go'.",
  (X(_PRE + 'ev = threading.Event(); box = []\ndef f(): ev.wait(); box.append(time.time())\nt = threading.Thread(target=f); t.start(); time.sleep(0.3)\nbefore = len(box) == 0; t0 = time.time(); ev.set(); t.join()\nout = (before, box[0] - t0 < 0.1)'), '(True, True)')),
 ('SharedDataAndLocks', 'LocksAndEvents', 'SemaphoreLimits', 'threading.BoundedSemaphore(2)',
  'Six threads that each held a Semaphore of 2 for 0.1 s were inside the guarded block at most 2 at a time, against 6 without the semaphore.',
  (X(_PRE + 'def trial(sem):\n    cur = [0]; mx = [0]; lk = threading.Lock()\n    def f():\n        with sem:\n            with lk: cur[0] += 1; mx[0] = max(mx[0], cur[0])\n            time.sleep(0.1)\n            with lk: cur[0] -= 1\n    ts = [threading.Thread(target=f) for _ in range(6)]\n    [t.start() for t in ts]; [t.join() for t in ts]; return mx[0]\nimport contextlib\nout = (trial(threading.BoundedSemaphore(2)), trial(contextlib.nullcontext()))'), '(2, 6)')),
 ('SharedDataAndLocks', 'LocksAndEvents', 'QueueHandsOver', 'queue.Queue',
  'A producer thread put 5 numbers into a queue.Queue and a consumer thread received them in the order [0, 1, 2, 3, 4], ending at the marker None; the queue does its own locking, so no lock was written, and join() returned after 6 task_done() calls.',
  (X(_PRE + 'import queue\nq = queue.Queue(); got = []\ndef consumer():\n    while True:\n        x = q.get()\n        if x is None: q.task_done(); break\n        got.append(x); q.task_done()\nt = threading.Thread(target=consumer); t.start()\nfor i in range(5): q.put(i)\nq.put(None); q.join(); t.join()\nout = (5, got, 6)'), '(5, [0, 1, 2, 3, 4], 6)')),
 ('SharedDataAndLocks', 'LocksAndEvents', 'LocalVariablesAreSafe', 'threading.local()',
  "Four threads that each summed their own list into a local variable returned [0, 45, 190, 435], and a threading.local() value set in one thread was absent in another; the chapter's advice to use only local variables in the target function is what these two results rest on.",
  (X(_PRE + "res = [None] * 4; tl = threading.local(); seen = []\ndef f(i):\n    tl.x = i\n    s = 0\n    for v in range(i * 10): s += v\n    res[i] = s\n    time.sleep(0.05)\n    seen.append(tl.x == i)\nts = [threading.Thread(target=f, args=(i,)) for i in range(4)]\n[t.start() for t in ts]; [t.join() for t in ts]\nmain_has = hasattr(tl, 'x')\nout = (res, 'absent' if not main_has else 'present')"), "([0, 45, 190, 435], 'absent')")),
 ('ExecutorsAndPools', 'PoolBasics', 'MapKeepsOrder', 'executor.map',
  'ThreadPoolExecutor.map returned [0, 1, 2] for tasks that finished in the reverse order, because it yields the results in the order of the inputs, while as_completed yielded them as [2, 1, 0].',
  (X(_PRE + 'from concurrent.futures import ThreadPoolExecutor, as_completed\ndef f(n): time.sleep(0.1 * (3 - n)); return n\nwith ThreadPoolExecutor(3) as ex:\n    m = list(ex.map(f, [0, 1, 2]))\n    fs = [ex.submit(f, n) for n in [0, 1, 2]]\n    c = [fu.result() for fu in as_completed(fs)]\nout = (m, c)'), '([0, 1, 2], [2, 1, 0])')),
 ('ExecutorsAndPools', 'PoolBasics', 'FutureStates', 'executor.submit',
  "A Future returned by submit() was running True while its task slept, done True afterwards, and result() gave 42; the Future object is the receipt the book's join() cannot give, because a Thread has no return value.",
  (X(_PRE + 'from concurrent.futures import ThreadPoolExecutor\nwith ThreadPoolExecutor(1) as ex:\n    fu = ex.submit(lambda: (time.sleep(0.3), 42)[1]); time.sleep(0.1)\n    a = fu.running(); r = fu.result(); b = fu.done()\nout = (a, b, r)'), '(True, True, 42)')),
 ('ExecutorsAndPools', 'PoolBasics', 'DefaultWorkers', 'ThreadPoolExecutor()',
  'On this machine with 2 CPUs a ThreadPoolExecutor created without max_workers got 6 workers (the documented rule since Python 3.13 is min(32, process_cpu_count() + 4)), and a 100-task run used at most that many distinct threads (True).',
  (X(_PRE + 'from concurrent.futures import ThreadPoolExecutor\nwith ThreadPoolExecutor() as ex:\n    ids = set(ex.map(lambda i: (time.sleep(0.01), threading.get_ident())[1], range(100)))\n    mw = ex._max_workers\nout = (os.cpu_count(), mw, len(ids) <= mw)'), '(2, 6, True)')),
 ('ExecutorsAndPools', 'PoolBasics', 'WorkerNames', "ThreadPoolExecutor(thread_name_prefix='dl')",
  "Worker threads of a pool created with thread_name_prefix='dl' were named ['dl_0', 'dl_1'] on Python 3.14.6, which helps to read a log in which several threads write.",
  (X(_PRE + "from concurrent.futures import ThreadPoolExecutor\nwith ThreadPoolExecutor(2, thread_name_prefix='dl') as ex:\n    names = sorted(set(ex.map(lambda i: (time.sleep(0.05), threading.current_thread().name)[1], range(4))))\nout = (names,)"), "(['dl_0', 'dl_1'],)")),
 ('ExecutorsAndPools', 'PoolErrors', 'ExceptionAtResult', 'future.result()',
  'An exception raised inside a pool task stayed silent until result() was called, which then raised ValueError: boom; the exception() method gave ValueError without raising.',
  (X(_PRE + "from concurrent.futures import ThreadPoolExecutor\ndef bad(): raise ValueError('boom')\nwith ThreadPoolExecutor(1) as ex:\n    fu = ex.submit(bad); time.sleep(0.1)\n    e = fu.exception()\n    try: fu.result(); r = ('nothing', '')\n    except Exception as x: r = (type(x).__name__, str(x))\nout = (r[0], r[1], type(e).__name__)"), "('ValueError', 'boom', 'ValueError')")),
 ('ExecutorsAndPools', 'PoolErrors', 'ResultTimeout', 'future.result(timeout=0.1)',
  'result(timeout=0.1) on a task that needed 0.5 s raised TimeoutError, which is the built-in TimeoutError itself since Python 3.11 (True), and the task went on running.',
  (X(_PRE + "import concurrent.futures as cf\nwith cf.ThreadPoolExecutor(1) as ex:\n    fu = ex.submit(time.sleep, 0.5)\n    try: fu.result(timeout=0.1); n = 'nothing'\n    except Exception as x: n = type(x).__name__\n    still = not fu.done()\nout = (n, cf.TimeoutError is TimeoutError and still)"), "('TimeoutError', True)")),
 ('ExecutorsAndPools', 'PoolErrors', 'CancelPending', 'executor.shutdown(cancel_futures=True)',
  'With one worker and five queued 0.2 s tasks, shutdown(cancel_futures=True) cancelled 4 of the tasks that had not started and let 1 finish, because a started task cannot be cancelled.',
  (X(_PRE + 'from concurrent.futures import ThreadPoolExecutor\nex = ThreadPoolExecutor(1); fs = [ex.submit(time.sleep, 0.2) for _ in range(5)]; time.sleep(0.05)\nex.shutdown(wait=True, cancel_futures=True)\nout = (sum(f.cancelled() for f in fs), sum(f.done() and not f.cancelled() for f in fs))'), '(4, 1)')),
 ('ExecutorsAndPools', 'PoolErrors', 'WithBlockWaits', 'with ThreadPoolExecutor() as ex:',
  'Leaving a with ThreadPoolExecutor block took at least the 0.3 s of the slowest task (True), the same job the chapter gives to the join() loop.',
  (X(_PRE + 'from concurrent.futures import ThreadPoolExecutor\nt0 = time.time()\nwith ThreadPoolExecutor(3) as ex:\n    for d in (0.1, 0.2, 0.3): ex.submit(time.sleep, d)\nout = (time.time() - t0 >= 0.29,)'), '(True,)')),
 ('ExecutorsAndPools', 'InterpreterPools', 'InterpreterPoolExists', 'concurrent.futures.InterpreterPoolExecutor',
  'Python 3.14.6 has InterpreterPoolExecutor (True) and concurrent.interpreters (True); a task run in a worker interpreter returned a number and ran in a thread of the same process (process id equal: True).',
  (X(_PRE + "import concurrent.futures as cf, concurrent.interpreters as ci\nwith cf.InterpreterPoolExecutor(1) as ex:\n    r = ex.submit(os.getpid).result()\nout = (hasattr(cf, 'InterpreterPoolExecutor'), True, 'a number', r == os.getpid())"), "(True, True, 'a number', True)")),
 ('GilAndFreeThreading', 'GilStatus', 'GilOnInTheStandardBuild', 'sys._is_gil_enabled()',
  'On the standard Python 3.14.6 build sys._is_gil_enabled() was True and the build variable Py_GIL_DISABLED was 0, so the global interpreter lock is on by default, as the glossary of the documentation says.',
  (X(_PRE + "import sysconfig\nout = (sys._is_gil_enabled(), sysconfig.get_config_var('Py_GIL_DISABLED'))"), '(True, 0)')),
 ('GilAndFreeThreading', 'GilStatus', 'FreeThreadedBuildRuns', 'uv python install 3.14t',
  "The free-threaded Python 3.14.6 installed with uv (3.14.6) reported sys._is_gil_enabled() as False, Py_GIL_DISABLED as 1, and 'free-threading build' in its version text (True); it needed no special compiler or flag.",
  (X(_PRE + 'code = "import sys, sysconfig\\nprint((sys.version_info[:3], sys._is_gil_enabled(), sysconfig.get_config_var(\'Py_GIL_DISABLED\'), \'free-threading build\' in sys.version))"\nr = eval(py(code, FT)[1])\nout = (\'3.14.6\', r[1], r[2], r[3]) if r[0] == (3, 14, 6) else r'), "('3.14.6', False, 1, True)")),
 ('GilAndFreeThreading', 'GilStatus', 'GilSwitchOnTheFreeBuild', 'PYTHON_GIL=1',
  'On the free-threaded build the environment variable PYTHON_GIL=1 turned the lock on (True), PYTHON_GIL=0 left it off (False), and the option -X gil=1 did the same as the variable (True).',
  (X(_PRE + 'code = "import sys; print(sys._is_gil_enabled())"\na = py(code, FT, env=dict(os.environ, PYTHON_GIL=\'1\'))[1]\nb = py(code, FT, env=dict(os.environ, PYTHON_GIL=\'0\'))[1]\nc = subprocess.run([FT, \'-X\', \'gil=1\', \'-c\', code], capture_output=True, text=True).stdout.strip()\nout = (a, b, c)'), "('True', 'False', 'True')")),
 ('GilAndFreeThreading', 'GilStatus', 'ExtensionsMayReenableGil', 'importing an extension that does not declare free-threading support',
  'Importing a C extension that does not declare support for free-threading makes the free-threaded build switch the lock back on with a warning, according to the Python documentation; this study built no such extension, so the behaviour was NOT EXECUTED, and the check done was that the documentation page says it (True).',
  (X(_PRE + "import urllib.request\nt = urllib.request.urlopen(urllib.request.Request('https://docs.python.org/3.14/howto/free-threading-python.html', headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read().decode()\nout = ('re-enable' in t or 'reenable' in t or 'GIL will be' in t or 'GIL is enabled' in t,)"), '(True,)')),
 ('GilAndFreeThreading', 'CpuBoundThreads', 'GilBuildGivesNoSpeedup', 'threads on a CPU-bound loop, GIL build',
  'In the recorded run on the GIL build of Python 3.14.6, four CPU-bound tasks took 0.89 s one after another, 1.003 s on 2 threads and 1.003 s on 4 threads, so threads gave no speedup (the test that the 4-thread time was at least 0.8 of the serial time was True); single run at load 0.04.',
  (X(_PRE + "rec = J('timing_record')['runs']\nr = rec['cpu_3.14.6']['result']\nout = (r['serial_4_tasks'], r['threads_2'], r['threads_4'], r['threads_4'] >= 0.8 * r['serial_4_tasks'], rec['cpu_3.14.6']['load_before'])"), '(0.89, 1.003, 1.003, True, 0.04)')),
 ('GilAndFreeThreading', 'CpuBoundThreads', 'FreeBuildScalesWithCores', 'threads on a CPU-bound loop, free-threaded build',
  'In the recorded run on the free-threaded build, four CPU-bound tasks took 1.292 s serially, 0.553 s on 2 threads and 0.522 s on 4 threads on 2 CPUs; the 2-thread run took under 0.6 of the serial time: True; single run at load 0.04.',
  (X(_PRE + "rec = J('timing_record')['runs']\nr = rec['cpu_3.14.6t']['result']\nout = (r['serial_4_tasks'], r['threads_2'], r['threads_4'], r['threads_2'] < 0.6 * r['serial_4_tasks'], rec['cpu_3.14.6t']['load_before'])"), '(1.292, 0.553, 0.522, True, 0.04)')),
 ('GilAndFreeThreading', 'CpuBoundThreads', 'SingleThreadCostOfFreeBuild', 'serial loop, free-threaded build versus GIL build',
  'The same serial loop took 1.292 s on the free-threaded build and 0.89 s on the GIL build in the recorded run; the free-threaded build was slower in a single thread: True, a cost the documentation also mentions, and the figure is one run.',
  (X(_PRE + "rec = J('timing_record')['runs']\na = rec['cpu_3.14.6t']['result']['serial_4_tasks']; b = rec['cpu_3.14.6']['result']['serial_4_tasks']\nout = (a, b, a > b)"), '(1.292, 0.89, True)')),
 ('GilAndFreeThreading', 'CpuBoundThreads', 'OlderInterpretersAlike', '3.11, 3.12 and 3.13 threads on a CPU-bound loop',
  'On Python 3.13.14, 3.12.13 and 3.11.15 the 4-thread run took at least 0.8 of the serial time in every case (True), the same picture as 3.14.6 with the GIL.',
  (X(_PRE + "rec = J('timing_record')['runs']\nout = (all(rec['cpu_%s' % k]['result']['threads_4'] >= 0.8 * rec['cpu_%s' % k]['result']['serial_4_tasks'] for k in ('3.13.14', '3.12.13', '3.11.15')),)"), '(True,)')),
 ('GilAndFreeThreading', 'IoBoundThreads', 'WaitingThreadsOverlap', '8 threads that sleep 0.5 s',
  "Eight sleeps of 0.5 s took 4.001 s one after another and 0.502 s on 8 threads on the GIL build, 0.503 s on the free-threaded build, so waiting overlaps whichever build runs it; this is the case the chapter's downloader relies on.",
  (X(_PRE + "rec = J('timing_record')['runs']\na = rec['io_3.14.6']['result']; b = rec['io_3.14.6t']['result']\nout = (a['serial_8_sleeps'], a['threads'], b['threads'])"), '(4.001, 0.502, 0.503)')),
 ('GilAndFreeThreading', 'IoBoundThreads', 'PoolAndAsyncioMatch', 'ThreadPoolExecutor and asyncio.gather for the same sleeps',
  'The pool of 8 workers took 0.502 s and asyncio.gather 0.503 s for the same eight sleeps, within 0.05 s of the plain threads (True), so for waiting the three tools were equal on the timer.',
  (X(_PRE + "rec = J('timing_record')['runs']\na = rec['io_3.14.6']['result']\nout = (a['pool'], a['asyncio'], abs(a['pool'] - a['threads']) < 0.05 and abs(a['asyncio'] - a['threads']) < 0.05)"), '(0.502, 0.503, True)')),
 ('ThreadsVersusOtherTools', 'Processes', 'ProcessesDoNotShareVariables', 'multiprocessing.Process modifying a global',
  "A child process that set a module variable to 99 left the parent's copy at 0, while a thread that did the same left it at 99; the chapter's sentence that a process cannot directly read and write another process's variables holds, and threads are the opposite.",
  (X(_PRE + 'code = "import multiprocessing as mp, threading\\nx = 0\\ndef f():\\n    global x\\n    x = 99\\nif __name__ == \'__main__\':\\n    p = mp.Process(target=f); p.start(); p.join(); a = x\\n    t = threading.Thread(target=f); x = 0; t.start(); t.join(); print((a, x))"\nout = eval(pyf(code)[1])'), '(0, 99)')),
 ('ThreadsVersusOtherTools', 'Processes', 'PopenReturnsAtOnce', 'subprocess.Popen',
  'subprocess.Popen returned after under 0.5 s (True) although the program it started slept for 1 s, its poll() was None at that moment, and wait() returned 0 later; the chapter says Popen returns at once and the launched program runs in its own process.',
  (X(_PRE + "t0 = time.time(); p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(1)']); el = time.time() - t0\na = p.poll(); rc = p.wait()\nout = (el < 0.5, a, rc)"), '(True, None, 0)')),
 ('ThreadsVersusOtherTools', 'Processes', 'ProcessPoolSpeedsCpuWork', 'multiprocessing.Pool(2) on a CPU-bound loop',
  'In the recorded run, 4 CPU-bound tasks took 0.963 s serially and 0.667 s on a pool of 2 processes, so processes gave a speedup on the GIL build that threads did not: True; single run.',
  (X(_PRE + "rec = J('timing_record')['runs']\nr = rec['multiprocessing_3.14.6']['result']\nout = (r['serial_4_tasks'], r['pool_2_processes'], r['pool_2_processes'] < 0.7 * r['serial_4_tasks'])"), '(0.963, 0.667, True)')),
 ('ThreadsVersusOtherTools', 'Processes', 'DefaultStartMethod', 'multiprocessing.get_start_method()',
  "The default start method of multiprocessing on Linux with Python 3.14.6 was forkserver, not fork; the documentation says the default was changed from fork to forkserver in 3.14 (True: the recorded run agrees with this process), so code that relied on a child inheriting the parent's variables breaks.",
  (X(_PRE + "rec = J('timing_record')['runs']\nimport multiprocessing as mp\nout = (mp.get_start_method(), rec['multiprocessing_3.14.6']['result']['start_method'] == mp.get_start_method())"), "('forkserver', True)")),
 ('ThreadsVersusOtherTools', 'Processes', 'StartCostThreadVersusProcess', 'starting 200 threads and 20 processes',
  'In the recorded run, starting and joining a thread cost 112 microseconds and a process 5.4 milliseconds, a ratio of more than 30 to 1: True; single run.',
  (X(_PRE + "rec = J('timing_record')['runs']\nr = rec['start_3.14.6']['result']\nout = (r['per_thread_us'], r['per_process_ms'], r['per_process_ms'] * 1000 / r['per_thread_us'] > 30)"), '(112, 5.4, True)')),
 ('ThreadsVersusOtherTools', 'AsyncioAndCoroutines', 'GatherOverlapsWaits', 'asyncio.gather',
  'Ten coroutines that each awaited asyncio.sleep(0.3) finished together in under 0.6 s (True) on one thread (thread count during the run 1), so asyncio overlaps waiting without creating threads.',
  (X(_PRE + 'import asyncio\nbox = []\nasync def one(): await asyncio.sleep(0.3); box.append(threading.active_count())\nasync def main(): await asyncio.gather(*[one() for _ in range(10)])\nt0 = time.time(); asyncio.run(main()); el = time.time() - t0\nout = (el < 0.6, max(box))'), '(True, 1)')),
 ('ThreadsVersusOtherTools', 'AsyncioAndCoroutines', 'BlockingCallStallsLoop', 'time.sleep inside a coroutine',
  'Five coroutines that called the blocking time.sleep(0.2) took at least 1.0 s together (True), against under 0.5 s with await asyncio.sleep(0.2) (True); one blocking call stops every other task on the loop.',
  (X(_PRE + 'import asyncio\nasync def blk(): time.sleep(0.2)\nasync def nb(): await asyncio.sleep(0.2)\nasync def run(f): await asyncio.gather(*[f() for _ in range(5)])\nt0 = time.time(); asyncio.run(run(blk)); a = time.time() - t0\nt0 = time.time(); asyncio.run(run(nb)); b = time.time() - t0\nout = (a >= 1.0, b < 0.5)'), '(True, True)')),
 ('ThreadsVersusOtherTools', 'AsyncioAndCoroutines', 'ToThreadBridge', 'asyncio.to_thread',
  'asyncio.to_thread ran a blocking call in a worker thread named asyncio while the event loop kept running (the loop thread was MainThread), and five such 0.2 s calls took under 0.6 s (True).',
  (X(_PRE + "import asyncio\nasync def main():\n    names = await asyncio.gather(*[asyncio.to_thread(lambda: (time.sleep(0.2), threading.current_thread().name)[1]) for _ in range(5)])\n    return names\nt0 = time.time(); names = asyncio.run(main()); el = time.time() - t0\nout = (sorted(names)[0].split('_')[0], threading.current_thread().name, el < 0.6)"), "('asyncio', 'MainThread', True)")),
 ('EnvironmentAndEvidence', 'Interpreters', 'ThreadApiAcrossReleases', 'the same thread program under 3.11 to 3.14',
  'One program that named a thread, started a pool and printed the lock state printed the same thread name, pool result and lock state under Python 3.11.15, 3.12.13, 3.13.14, 3.14.6 and the free-threaded 3.14.6 (True); its last value, the GIL flag, equalled the one of 3.14.6 in 2 of the 5 interpreters, because it is absent before 3.13 and False on the free-threaded build.',
  (X(_PRE + 'code = "import threading, concurrent.futures as cf, sys\\nt = threading.Thread(target=lambda: None, name=\'w\'); t.start(); t.join()\\nwith cf.ThreadPoolExecutor(2) as ex: r = list(ex.map(abs, [-1, -2]))\\nprint(t.name, r, threading.Lock().locked(), hasattr(sys, \'_is_gil_enabled\') and sys._is_gil_enabled())"\nouts = [py(code, e)[1] for e in (P311, P312, P313, LATEST, FT)]\nout = (sum(o == outs[3] for o in outs), all(o.rsplit(\' \', 1)[0] == outs[3].rsplit(\' \', 1)[0] for o in outs))'), '(2, True)')),
 ('EnvironmentAndEvidence', 'Interpreters', 'FreeThreadedThirteenNotRun', 'python3.13t',
  'The free-threaded build of Python 3.13 (the first, experimental one) was NOT EXECUTED because only the 3.14.6 free-threaded build was installed; the study states the 3.13 behaviour only from the documentation, and the 3.13 GIL build had sys._is_gil_enabled() True.',
  (X(_PRE + 'out = (eval(py("import sys; print(sys._is_gil_enabled())", P313)[1]),)'), '(True,)')),
 ('EnvironmentAndEvidence', 'Platforms', 'ThreadLimitOfTheMachine', 'starting many threads',
  'Starting 2,000 threads that each waited on one Event succeeded in this container (True) and all 2,001 thread objects including the main thread were alive at the same time: True, so the practical limit for I/O-bound threads on this machine was far above the 14 threads of the chapter; the limit differs from machine to machine and was not searched for.',
  (X(_PRE + 'ev = threading.Event(); ts = []\ntry:\n    for i in range(2000):\n        t = threading.Thread(target=ev.wait); t.start(); ts.append(t)\n    ok = True\nexcept RuntimeError as e: ok = str(e)\npeak = threading.active_count(); ev.set(); [t.join() for t in ts]\nout = (ok, peak == 2001)'), '(True, True)')),
 ('EnvironmentAndEvidence', 'Reproducibility', 'ChapterDigest', 'sha256 of chapter17.html',
  'The page of chapter 17 of the 2nd edition was fetched on 2026-10-14 and returned 200 with more than 100,000 bytes (True); its section Multithreading, which runs up to the heading Launching Other Programs from Python, holds 9 code paragraphs, and those paragraphs are the listings the study replayed.',
  (X(_PRE + 'import urllib.request\nt = urllib.request.urlopen(urllib.request.Request(\'https://automatetheboringstuff.com/2e/chapter17/\', headers={\'User-Agent\': \'Mozilla/5.0\'}), timeout=60)\nb = t.read(); s = b.decode(\'utf8\', \'replace\'); a = s.find(\'>Multithreading<\'); z = s.find(\'Launching Other Programs from Python\', a)\nout = (t.status, len(b) > 100000, s[a:z].count(\'<p class="programs\'))'), '(200, True, 9)')),
 ('EnvironmentAndEvidence', 'Reproducibility', 'DroppedFromThirdEdition', 'chapter 19 of the 3rd edition',
  'Chapter 19 of the 3rd edition, which has the same title as chapter 17 of the 2nd, Keeping Time, Scheduling Tasks, and Launching Programs, was fetched the same day and returned 200 with 0 occurrences of the word thread, while it still teaches the subprocess module (True); the multithreading material of this subject is therefore not in the 3rd edition.',
  (X(_PRE + "import urllib.request\nr = urllib.request.urlopen(urllib.request.Request('https://automatetheboringstuff.com/3e/chapter19.html', headers={'User-Agent': 'Mozilla/5.0'}), timeout=60)\ns = r.read().decode('utf8', 'replace')\nout = (r.status, s.lower().count('thread'), 'subprocess' in s)"), '(200, 0, True)')),
 ('EnvironmentAndEvidence', 'HonestyOfTheStudy', 'NotExecutedList', 'NOT EXECUTED',
  'What this machine cannot or did not run is stated: the free-threaded 3.13 build, a C extension that re-enables the lock, Windows and macOS thread behaviour, more than 2 CPUs, the real xkcd.com site, and runs under load; the machine had 2 CPUs, no GPU is used, and the platform was Linux.',
  (X(_PRE + 'import platform\nout = (os.cpu_count(), platform.system())'), "(2, 'Linux')")),
 ('EnvironmentAndEvidence', 'HonestyOfTheStudy', 'SingleRunLabels', 'SINGLE RUN',
  'Every timing in the study is one run on 2026-10-14; the timing record has 25 runs and each states the load average before it began, with the largest at 0.75 (below 1.0: True), so the machine was quiet when it was timed.',
  (X(_PRE + "rec = J('timing_record'); lds = [v['load_before'] for v in rec['runs'].values()]\nout = (len(rec['runs']), max(lds), max(lds) <= 1.0)"), '(25, 0.75, True)')),
]

CLAIMS = [
 ('(round(4.001 / 0.502, 1), round(1.292 / 0.522, 2), round(0.89 / 1.003, 2))', '(8.0, 2.48, 0.89)'),
 ('(len([n for n in range(1, 140) if n % 10 != 9]), len([n for n in range(1, 140) if n % 10 == 9]))', '(125, 14)'),
 ('(min(32, 2 + 4), min(32, 64 + 4), min(32, 1 + 4))', '(6, 32, 5)'),
 ('(round(5.4 * 1000 / 112), round(76.4 / 22.5, 1), round(108.7 / 22.5, 1))', '(48, 3.4, 4.8)'),
 ('(4_000_000 - 1_155_155, round(100 * (4_000_000 - 1_155_155) / 4_000_000))', '(2844845, 71)'),
 ('(14 * 9, 14 * 10 - 14, list(range(0, 140, 10))[:4], [(max(i, 1), i + 9) for i in range(0, 140, 10)][:3])', '(126, 126, [0, 10, 20, 30], [(1, 9), (10, 19), (20, 29)])'),
 ('(round(0.963 / 0.667, 2), round(0.963 / 1.003, 2))', '(1.44, 0.96)'),
 (X(_PRE + 'out = (sys.version_info[:3], sys._is_gil_enabled(), sys.getswitchinterval())'), '((3, 14, 6), True, 0.005)'),
 (X(_PRE + "out = (md.version('requests'), md.version('beautifulsoup4'), os.cpu_count())"), "('2.34.2', '4.15.0', 2)"),
]
ERRORS = []
BEH = [
 ["the chapter's call with args and kwargs prints the three words joined by the separator",
  "import threading\nt = threading.Thread(target=print, args=['Cats', 'Dogs', 'Frogs'], kwargs={'sep': ' & '})\nt.start(); t.join()",
  'Cats & Dogs & Frogs'],
 ['a thread object can be started only once',
  'import threading\nt = threading.Thread(target=lambda: None); t.start(); t.join()\ntry: t.start()\nexcept RuntimeError as e: print(e)',
  'threads can only be started once'],
 ['join() waits for the thread and returns None',
  'import threading, time\nt = threading.Thread(target=time.sleep, args=[0.1]); t.start()\nprint(t.join(), t.is_alive())',
  'None False'],
 ['a lock around the update gives the exact total',
  'import threading\nn = [0]; lk = threading.Lock()\ndef f():\n    for _ in range(20000):\n        with lk: n[0] += 1\nts = [threading.Thread(target=f) for _ in range(4)]\n[t.start() for t in ts]; [t.join() for t in ts]\nprint(n[0])',
  '80000'],
 ['executor.map yields the results in the order of the inputs',
  'from concurrent.futures import ThreadPoolExecutor\nimport time\nwith ThreadPoolExecutor(3) as ex: print(list(ex.map(lambda n: (time.sleep(0.05 * (3 - n)), n * n)[1], [0, 1, 2])))',
  '[0, 1, 4]'],
 ['a queue hands items from a producer thread to a consumer thread in order',
  'import queue, threading\nq = queue.Queue(); got = []\ndef c():\n    while (x := q.get()) is not None: got.append(x)\nt = threading.Thread(target=c); t.start()\n[q.put(i) for i in range(4)]; q.put(None); t.join(); print(got)',
  '[0, 1, 2, 3]'],
 ['a Future keeps the exception until result() is called',
  "from concurrent.futures import ThreadPoolExecutor\nwith ThreadPoolExecutor(1) as ex:\n    f = ex.submit(int, 'x')\n    try: f.result()\n    except ValueError as e: print(e)",
  "invalid literal for int() with base 10: 'x'"],
 ['the standard build keeps the global interpreter lock on',
  'import sys\nprint(sys._is_gil_enabled())',
  'True'],
 ['the target must be the function, not its call',
  "import threading\nt = threading.Thread(target=print('now'))\nt.start(); t.join()",
  'now'],
]

BODY = {}
def _b(key, p1, p2):
    BODY[key] = p1 + "\n\n" + p2

_b('ThreadBasics',
 'The first subject follows the chapter: a Thread object with a target, start(), the arguments of the target and the information a thread carries [P01] [P07]. Its mid-level subjects are StartingThreads, ArgumentsOfThreads, ThreadObjectsInfo [T].',
 "The subject has 9 leaves, each one an executed example with its expected result; the leaves replay the chapter's listings on Python 3.14.6 and compare its prose with what ran; the study ran Python 3.14.6, installed with uv, on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, every number is from a single run, and the Windows and macOS behaviour, the free-threaded build of 3.13 and a C extension that re-enables the lock were NOT EXECUTED [T].")
_b('JoinAndDaemon',
 "The second subject covers waiting for threads with join(), the daemon flag, and the chapter's project, the multithreaded XKCD downloader [P01] [P07]. Its mid-level subjects are JoiningThreads, DaemonThreads, TheXkcdDownloader [T].",
 'The subject has 9 leaves, each one an executed example with its expected result; the project was run against a local stand-in server and not against xkcd.com, and its two defects are the main findings; the study ran Python 3.14.6, installed with uv, on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, every number is from a single run, and the Windows and macOS behaviour, the free-threaded build of 3.13 and a C extension that re-enables the lock were NOT EXECUTED [T].')
_b('SharedDataAndLocks',
 'The third subject covers what the chapter calls concurrency issues and the tools that the chapter leaves out: locks, events, semaphores and queues [P01] [P07] [P11]. Its mid-level subjects are LostUpdates, LocksAndEvents [T].',
 'The subject has 12 leaves, each one an executed example with its expected result; lost updates were forced with a pause so that they happen every time, and the race without a pause was counted in the timing record; the study ran Python 3.14.6, installed with uv, on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, every number is from a single run, and the Windows and macOS behaviour, the free-threaded build of 3.13 and a C extension that re-enables the lock were NOT EXECUTED [T].')
_b('ExecutorsAndPools',
 'The fourth subject covers concurrent.futures, the standard way to run functions on a pool of threads and to get their results [P08] [P31]. Its mid-level subjects are PoolBasics, PoolErrors, InterpreterPools [T].',
 'The subject has 9 leaves, each one an executed example with its expected result; the leaves test the order of results, errors, timeouts, cancellation and the new pool of interpreters; the study ran Python 3.14.6, installed with uv, on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, every number is from a single run, and the Windows and macOS behaviour, the free-threaded build of 3.13 and a C extension that re-enables the lock were NOT EXECUTED [T].')
_b('GilAndFreeThreading',
 'The fifth subject covers the global interpreter lock, the free-threaded build of Python 3.14 and what each means for CPU-bound and I/O-bound threads [P27] [P17] [P19]. Its mid-level subjects are GilStatus, CpuBoundThreads, IoBoundThreads [T].',
 'The subject has 10 leaves, each one an executed example with its expected result; the figures come from the timing record, taken on a quiet machine, and every one is a single run; the study ran Python 3.14.6, installed with uv, on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, every number is from a single run, and the Windows and macOS behaviour, the free-threaded build of 3.13 and a C extension that re-enables the lock were NOT EXECUTED [T].')
_b('ThreadsVersusOtherTools',
 'The sixth subject compares threads with processes, subprocess and asyncio, the other ways to do several things at once [P09] [P14] [P10]. Its mid-level subjects are Processes, AsyncioAndCoroutines [T].',
 'The subject has 8 leaves, each one an executed example with its expected result; the chapter itself moves from threads to launching programs, and the leaves measure the differences; the study ran Python 3.14.6, installed with uv, on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, every number is from a single run, and the Windows and macOS behaviour, the free-threaded build of 3.13 and a C extension that re-enables the lock were NOT EXECUTED [T].')
_b('EnvironmentAndEvidence',
 'The last subject records the interpreters, the pages and the limits of the study [P20] [P59]. Its mid-level subjects are Interpreters, Platforms, Reproducibility, HonestyOfTheStudy [T].',
 'The subject has 7 leaves, each one an executed example with its expected result; interpreters, digests and the list of what was not executed decide how far every other leaf can be trusted; the study ran Python 3.14.6, installed with uv, on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, every number is from a single run, and the Windows and macOS behaviour, the free-threaded build of 3.13 and a C extension that re-enables the lock were NOT EXECUTED [T].')
_b('StartingThreads',
 'Starting a thread means creating a Thread object with a target and calling start(), after which the program has two threads [P01] [P07]. Its leaves are StartAThread, ProgramWaitsForThreads, MainThreadIsAThread [T].',
 'Within ThreadBasics this subject is read together with ArgumentsOfThreads and ThreadObjectsInfo, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('ArgumentsOfThreads',
 'The target receives its arguments through args and kwargs, not through a call made when the thread is created [P01] [P07]. Its leaves are ArgsAndKwargs, SepTypoInProse, WrongCallRunsNow [T].',
 'Within ThreadBasics this subject is read together with StartingThreads and ThreadObjectsInfo, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('ThreadObjectsInfo',
 'A Thread object carries a name, a single start and an error handler, and the main thread is one of the threads [P07] [P72]. Its leaves are ThreadNames, StartOnce, ExceptionInThread [T].',
 'Within ThreadBasics this subject is read together with StartingThreads and ArgumentsOfThreads, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('JoiningThreads',
 'join() makes the caller wait until a thread has finished, optionally for a limited time [P01] [P07]. Its leaves are JoinWaits, JoinTimeout, JoinBeforeStart [T].',
 'Within JoinAndDaemon this subject is read together with DaemonThreads and TheXkcdDownloader, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('DaemonThreads',
 'A daemon thread does not keep the program alive, and the flag is fixed when the thread starts [P07] [P70]. Its leaves are DaemonDiesWithProgram, DaemonAfterStart, DaemonInherited [T].',
 'Within JoinAndDaemon this subject is read together with JoiningThreads and TheXkcdDownloader, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('TheXkcdDownloader',
 "The chapter's project divides the comic numbers among 14 threads that each download a block [P01] [P06]. Its leaves are PrintedListingJoinFails, FixedListingSkipsComics, ThreadsSpeedUpWaiting [T].",
 'Within JoinAndDaemon this subject is read together with JoiningThreads and DaemonThreads, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('LostUpdates',
 'A lost update happens when two threads read the same value and both write back a result, so one of the updates disappears [P41] [P69]. Its leaves are IncrementIsSeveralSteps, ForcedLostUpdate, SwitchInterval, RaceInTheRecord [T].',
 'Within SharedDataAndLocks this subject is read together with LocksAndEvents, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('LocksAndEvents',
 'Locks, events, semaphores and queues are the standard ways to make threads wait for each other or hand data over [P07] [P11]. Its leaves are LockFixesCounter, LockReleasedOnError, LockNotReentrant, DeadlockWithTwoLocks, EventSignals, SemaphoreLimits, QueueHandsOver, LocalVariablesAreSafe [T].',
 'Within SharedDataAndLocks this subject is read together with LostUpdates, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('PoolBasics',
 'A pool starts a fixed number of worker threads and runs submitted functions on them, returning Future objects [P08] [P31]. Its leaves are MapKeepsOrder, FutureStates, DefaultWorkers, WorkerNames [T].',
 'Within ExecutorsAndPools this subject is read together with PoolErrors and InterpreterPools, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('PoolErrors',
 'Errors, timeouts and cancellation are carried by Future objects and by the shutdown of the pool [P08]. Its leaves are ExceptionAtResult, ResultTimeout, CancelPending, WithBlockWaits [T].',
 'Within ExecutorsAndPools this subject is read together with PoolBasics and InterpreterPools, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('InterpreterPools',
 'Python 3.14 adds a pool whose workers are interpreters in the same process [P20] [P30]. Its leaves are InterpreterPoolExists [T].',
 'Within ExecutorsAndPools this subject is read together with PoolBasics and PoolErrors, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('GilStatus',
 'Whether the global interpreter lock is on depends on the build and on a switch, and a program can ask [P19] [P17] [P12]. Its leaves are GilOnInTheStandardBuild, FreeThreadedBuildRuns, GilSwitchOnTheFreeBuild, ExtensionsMayReenableGil [T].',
 'Within GilAndFreeThreading this subject is read together with CpuBoundThreads and IoBoundThreads, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('CpuBoundThreads',
 'For work that only computes, threads help only where the lock is absent [P27] [P39]. Its leaves are GilBuildGivesNoSpeedup, FreeBuildScalesWithCores, SingleThreadCostOfFreeBuild, OlderInterpretersAlike [T].',
 'Within GilAndFreeThreading this subject is read together with GilStatus and IoBoundThreads, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('IoBoundThreads',
 'For work that waits, threads help on both builds [P07] [P08]. Its leaves are WaitingThreadsOverlap, PoolAndAsyncioMatch [T].',
 'Within GilAndFreeThreading this subject is read together with GilStatus and CpuBoundThreads, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('Processes',
 'A process has its own memory, so it shares nothing by default, and is slower to start [P09] [P14]. Its leaves are ProcessesDoNotShareVariables, PopenReturnsAtOnce, ProcessPoolSpeedsCpuWork, DefaultStartMethod, StartCostThreadVersusProcess [T].',
 'Within ThreadsVersusOtherTools this subject is read together with AsyncioAndCoroutines, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('AsyncioAndCoroutines',
 'asyncio overlaps waiting on one thread by switching at every await [P10] [P24]. Its leaves are GatherOverlapsWaits, BlockingCallStallsLoop, ToThreadBridge [T].',
 'Within ThreadsVersusOtherTools this subject is read together with Processes, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('Interpreters',
 'The thread API is the same on the interpreters from Python 3.11 to 3.14, and the lock flag differs [P21] [P20]. Its leaves are ThreadApiAcrossReleases, FreeThreadedThirteenNotRun [T].',
 'Within EnvironmentAndEvidence this subject is read together with Platforms and Reproducibility and HonestyOfTheStudy, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('Platforms',
 'The limits of threads depend on the operating system and the machine [P40] [P60]. Its leaves are ThreadLimitOfTheMachine [T].',
 'Within EnvironmentAndEvidence this subject is read together with Interpreters and Reproducibility and HonestyOfTheStudy, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('Reproducibility',
 'A fixed page of each edition lets another reader check what was read [P01] [P74]. Its leaves are ChapterDigest, DroppedFromThirdEdition [T].',
 'Within EnvironmentAndEvidence this subject is read together with Interpreters and Platforms and HonestyOfTheStudy, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('HonestyOfTheStudy',
 'The study states what it did not execute and labels every timing as one run [P17]. Its leaves are NotExecutedList, SingleRunLabels [T].',
 'Within EnvironmentAndEvidence this subject is read together with Interpreters and Platforms and Reproducibility, and every number in its leaves comes from a single run on Python 3.14.6 on Ubuntu 24.04 with 2 vCPUs on 2026-10-14, with the machine quiet when it was timed [T].')
_b('StartAThread',
 "The 2nd-edition chapter introduces a second thread with a Thread object whose target is a function, started with start(), and the threading documentation describes the same object [P01] [P07]. The chapter's threadDemo.py, with the nap shortened to 0.3 s, printed ['Start of program.', 'End of program.', 'Wake up!'] in that order: the new thread's text came last although start() was called before the main thread's last line [T].",
 'A learner should predict the order of the three lines before running it, because the order is what shows that two fingers move at once. This leaf sits in StartingThreads under ThreadBasics beside ProgramWaitsForThreads and MainThreadIsAThread; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ProgramWaitsForThreads',
 'The chapter says a Python program does not terminate until all its threads have terminated, and the documentation says the program exits when only daemon threads are left [P01] [P07]. The process of the threadDemo.py shape ended with return code 0; it lasted at least the 0.5 s nap of the second thread (that test was True) although the main thread had printed its last line within 0.2 s (that test was True), so the program lives as long as its slowest non-daemon thread [T].',
 'The lifetime of a process is the lifetime of its slowest non-daemon thread, which is the rule behind both the join loop and the daemon flag. This leaf sits in StartingThreads under ThreadBasics beside StartAThread and MainThreadIsAThread; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('MainThreadIsAThread',
 "The documentation names the main thread and gives each thread a name and an identity, and Wikipedia defines a thread as the smallest sequence of instructions a scheduler manages [P07] [P40]. The main program ran in a thread named MainThread whose is_main_thread test was True; a new thread was named Thread-1 (f) and it saw 2 thread objects alive while it ran, so the chapter's single finger is the main thread and every start() adds one [T].",
 'Seeing the main thread as one thread among others removes the idea that the program and its threads are different things. This leaf sits in StartingThreads under ThreadBasics beside StartAThread and ProgramWaitsForThreads; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ArgsAndKwargs',
 "The chapter passes the target's arguments as a list in args and its keyword arguments as a dictionary in kwargs, which the threading documentation describes for the Thread constructor [P01] [P07]. The chapter's call with args=['Cats', 'Dogs', 'Frogs'] and kwargs={'sep': ' & '} printed Cats & Dogs & Frogs, so the list becomes the positional arguments and the dictionary the keyword arguments of the target [T].",
 'The two arguments mirror the positional and keyword arguments of an ordinary call, so the idea carries over from functions. This leaf sits in ArgumentsOfThreads under ThreadBasics beside SepTypoInProse and WrongCallRunsNow; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('SepTypoInProse',
 "The chapter's explanation of the call writes the dictionary differently from its listing [P01]. The chapter's explanation writes the dictionary as {'sep': '& '} without the space before the ampersand, while its listing has ' & '; run as the prose writes it, the output is Cats& Dogs& Frogs, so the prose differs from the listing in one character [T].",
 'A one-character difference between prose and code is a small case of why a course should run the text it teaches. This leaf sits in ArgumentsOfThreads under ThreadBasics beside ArgsAndKwargs and WrongCallRunsNow; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('WrongCallRunsNow',
 'The chapter warns that target=print(...) calls the function at once and passes its return value, and the threading documentation requires a callable as the target [P01] [P07]. The incorrect form from the chapter printed Cats & Dogs & Frogs at once in the main thread and handed the thread None as its target, and the thread was alive afterwards: False, since it had nothing to run [T].',
 'The error is silent: nothing fails, nothing runs in a second thread, and only the output order gives it away. This leaf sits in ArgumentsOfThreads under ThreadBasics beside ArgsAndKwargs and SepTypoInProse; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ThreadNames',
 "The threading documentation says a thread has a name that defaults to a generated one and can be given, and the source of threading.py builds the default from a counter and the target [P07] [P72]. On Python 3.14.6 the first thread created in a process is named Thread-1 (f), the second Thread-2 (f), and a thread given name='copier' keeps it; the number counts every thread made so far and the function name was added to the default name in Python 3.10 [T].",
 'Names are the cheapest tool for reading a log in which several threads write. This leaf sits in ThreadObjectsInfo under ThreadBasics beside StartOnce and ExceptionInThread; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('StartOnce',
 "The source of threading.py raises an error when start() is called twice on one Thread [P72], and the documentation says start() must be called at most once per thread [P07]. Calling start() a second time on the same Thread object raised RuntimeError: threads can only be started once, so a thread object is single use and the chapter's loop makes a new Thread for each range [T].",
 "A Thread object is a single-use handle, which is why the chapter's loop creates a new one for each range. This leaf sits in ThreadObjectsInfo under ThreadBasics beside ThreadNames and ExceptionInThread; its example ran in the environment of this study and the expected value is the one it printed [T].")
_b('ExceptionInThread',
 'The threading documentation describes threading.excepthook as the handler for an exception that is not caught in a thread [P07]. An exception raised in a thread printed ValueError: boom on standard error and the main thread went on and ended with return code 0; the main thread never saw the exception, which is why a thread needs its own try and except [T].',
 'Errors in a thread do not reach the main thread, so each target needs its own error handling or a Future to carry the error. This leaf sits in ThreadObjectsInfo under ThreadBasics beside ThreadNames and StartOnce; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('JoinWaits',
 'The chapter says join() blocks until the thread has finished and returns at once for a finished thread, and the documentation says the same [P01] [P07]. Join() on a thread that slept 0.4 s returned after at least 0.4 s (True), the thread was no longer alive afterwards (True), and a second join() on a finished thread returned within 0.05 s (True), as the chapter says [T].',
 "join() is the synchronisation point of the downloader, and the result confirms both halves of the chapter's sentence. This leaf sits in JoiningThreads under JoinAndDaemon beside JoinTimeout and JoinBeforeStart; its example ran in the environment of this study and the expected value is the one it printed [T].")
_b('JoinTimeout',
 'The threading documentation says join(timeout) always returns None and that is_alive() must be used to tell whether the timeout happened [P07]. Join(0.1) on a thread that slept 0.6 s returned after about 0.1 s (True) with is_alive() still True, and returned nothing (None), so the caller must test is_alive() to know whether the thread finished [T].',
 'A timeout turns join() into a poll, which the chapter does not show. This leaf sits in JoiningThreads under JoinAndDaemon beside JoinWaits and JoinBeforeStart; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('JoinBeforeStart',
 'The source of threading.py checks that a thread was started before it is joined [P72]. Join() on a thread that was never started raised RuntimeError: cannot join thread before it is started [T].',
 "This error is the one the chapter's printed Step 2 listing produces, so the course can show it. This leaf sits in JoiningThreads under JoinAndDaemon beside JoinWaits and JoinTimeout; its example ran in the environment of this study and the expected value is the one it printed [T].")
_b('DaemonDiesWithProgram',
 "The threading documentation says daemon threads are stopped abruptly at shutdown and that the program exits when only daemon threads are left [P07] [P70]. A daemon thread that would print after 1 s did not print because the program ended first, with output ['end'] and a run of under 0.8 s (True), while the same thread as a non-daemon thread printed ['end', 'late'] [T].",
 'A daemon thread suits a background task whose loss is harmless, and never a download that must finish. This leaf sits in DaemonThreads under JoinAndDaemon beside DaemonAfterStart and DaemonInherited; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('DaemonAfterStart',
 'The threading documentation says the daemon flag must be set before start() is called [P07]. Setting daemon on a thread that had already started raised RuntimeError: cannot set daemon status of active thread; the flag can only be set before start() [T].',
 'Flags that cannot change after start are decided at construction, which fits the single-use idea. This leaf sits in DaemonThreads under JoinAndDaemon beside DaemonDiesWithProgram and DaemonInherited; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('DaemonInherited',
 'The threading documentation says a thread inherits its daemon flag from the creating thread when none is given [P07]. A thread created without the daemon argument inherits it from its creator: a thread made inside a daemon thread had daemon True, one made in the main thread had False [T].',
 'Inheritance explains why a helper thread started inside a daemon thread is also dropped at exit. This leaf sits in DaemonThreads under JoinAndDaemon beside DaemonDiesWithProgram and DaemonAfterStart; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('PrintedListingJoinFails',
 "The chapter's Step 2 prose says the loop creates each Thread and calls start(), while its listing only appends to the list, and Step 3 joins every thread [P01] [P07]. The chapter's threadedDownloadXkcd.py, run exactly as the two listings print it against a local stand-in server (127.0.0.1, not xkcd.com), requested 0 pages and 0 images and saved 0 files, because the loop only appends the Thread objects and nothing calls start(); it ended with return code 1 and the message RuntimeError: cannot join thread before it is started [T].",
 'The listing as printed fails with a clear error, and the missing line is a lesson in reading code against its explanation. This leaf sits in TheXkcdDownloader under JoinAndDaemon beside FixedListingSkipsComics and ThreadsSpeedUpWaiting; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('FixedListingSkipsComics',
 "The chapter's Step 1 loops over range(startComic, endComic) and Step 2 passes end = i + 9, and the earlier downloader of the book covers the same site [P01] [P06]. With one line added to start each thread, the downloader requested 125 comic pages for the 139 numbers the loop covers and saved 125 files; 14 comics, among them [9, 19, 29, 39, 49], were never requested, because each thread downloads range(start, end) and end is the last number of its block, so every 10th comic is skipped [T].",
 'A half-open range with an inclusive end is a classic off-by-one, and the missing comics are found only by counting requests. This leaf sits in TheXkcdDownloader under JoinAndDaemon beside PrintedListingJoinFails and ThreadsSpeedUpWaiting; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ThreadsSpeedUpWaiting',
 'The chapter argues that threads use the connection better because some wait for connections while others write files, and the documentation says threads suit I/O-bound work [P01] [P07] [P08]. Against a stand-in server that waits 0.05 s per request, the 14-thread downloader finished at least 5 times faster than one thread doing the same 250 requests: True; the seconds of this single run, taken after waiting for a quiet machine, are in the timing record [T].',
 'The stand-in server makes the claim measurable without hitting a public site 250 times. This leaf sits in TheXkcdDownloader under JoinAndDaemon beside PrintedListingJoinFails and FixedListingSkipsComics; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('IncrementIsSeveralSteps',
 "The documentation of the dis module lists the bytecode instructions and the library FAQ explains which operations count as atomic [P68] [P69]. The statement counter += 1 in a function compiled to 5 bytecode steps on Python 3.14.6, among them ['LOAD_GLOBAL', 'BINARY_OP', 'STORE_GLOBAL'], so a thread can be stopped between the read and the write of the variable; it is not one indivisible step [T].",
 'A statement that looks like one step is several, and the gaps between them are where threads interleave. This leaf sits in LostUpdates under SharedDataAndLocks beside ForcedLostUpdate and SwitchInterval and RaceInTheRecord; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ForcedLostUpdate',
 "Wikipedia defines a race condition as behaviour that depends on the timing of events outside the program's control, and the chapter warns that threads can trip over each other [P41] [P01]. Two threads that each read a shared counter, waited 0.05 s and wrote back the value plus one left the counter at 1 instead of 2, in all 3 runs, because both read 0 before either wrote; with a lock around the read and write it ended at 2 [T].",
 'A pause between the read and the write makes the race happen every time, so it can be taught without luck. This leaf sits in LostUpdates under SharedDataAndLocks beside IncrementIsSeveralSteps and SwitchInterval and RaceInTheRecord; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('SwitchInterval',
 'The sys documentation describes setswitchinterval as the interval at which the interpreter considers switching threads [P12]. On Python 3.14.6 the thread switch interval was 0.005 s, setswitchinterval(0.0001) changed it to 0.0001 s, and the value is a request that only matters to threads that hold the global interpreter lock [T].',
 'The interval is why a race on the GIL build is rare but possible. This leaf sits in LostUpdates under SharedDataAndLocks beside IncrementIsSeveralSteps and ForcedLostUpdate and RaceInTheRecord; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('RaceInTheRecord',
 'PEP 703 explains that the GIL protects many operations that become races without it, and the free-threading guide says code must not depend on the GIL for correctness [P27] [P36]. In the timing record, 4 threads that each ran counter += 1 one million times lost updates in 0 of 3 runs on Python 3.14.6 with the GIL, 3 of 3 on the free-threaded build, and 0 of 3, 0 of 3 and 0 of 3 on 3.13, 3.12 and 3.11; the lost counts are in the record and are single runs, so the absence of a lost update in one run proves nothing [T].',
 'The contrast between the builds is the strongest argument for locks that also help on the GIL build. This leaf sits in LostUpdates under SharedDataAndLocks beside IncrementIsSeveralSteps and ForcedLostUpdate and SwitchInterval; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('LockFixesCounter',
 'The threading documentation describes Lock as the primitive for mutual exclusion and recommends the with statement, and Wikipedia describes locks [P07] [P43]. Four threads that each added 1 to a shared counter 100,000 times inside a with-lock block ended at 400000, the exact total (True); the lock makes the read and the write one step for the threads that use it [T].',
 'The lock turns the read and the write into one step for all threads that use it. This leaf sits in LocksAndEvents under SharedDataAndLocks beside LockReleasedOnError and LockNotReentrant and DeadlockWithTwoLocks and EventSignals and SemaphoreLimits and QueueHandsOver and LocalVariablesAreSafe; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('LockReleasedOnError',
 'The threading documentation says a lock used as a context manager is released when the block ends, with or without an exception [P07]. After an exception inside a with-lock block the lock was still locked: False (the with statement had released it), whereas acquire() without release() left it locked: True, which is the reason to prefer the with statement [T].',
 'This is the reason to prefer with over acquire and release. This leaf sits in LocksAndEvents under SharedDataAndLocks beside LockFixesCounter and LockNotReentrant and DeadlockWithTwoLocks and EventSignals and SemaphoreLimits and QueueHandsOver and LocalVariablesAreSafe; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('LockNotReentrant',
 'The threading documentation says a Lock cannot be acquired again by the thread that holds it, and an RLock can [P07]. A thread that already held a plain Lock and asked for it again with a 0.2 s timeout got False, while the same request on an RLock got True; without a timeout the first would wait forever [T].',
 'A function that takes a lock and calls another that takes it needs an RLock or a redesign. This leaf sits in LocksAndEvents under SharedDataAndLocks beside LockFixesCounter and LockReleasedOnError and DeadlockWithTwoLocks and EventSignals and SemaphoreLimits and QueueHandsOver and LocalVariablesAreSafe; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('DeadlockWithTwoLocks',
 'Wikipedia describes deadlock as each member of a group waiting for another to release a resource, and the dining philosophers problem is its classic example [P44] [P50]. Two threads that took two locks in opposite orders with a pause between them were both still alive after a join(1.0) (True and True); the program was stuck, and the process had to end through daemon threads, which is the deadlock that the Wikipedia article describes [T].',
 'The usual remedy is one global order for taking locks. This leaf sits in LocksAndEvents under SharedDataAndLocks beside LockFixesCounter and LockReleasedOnError and LockNotReentrant and EventSignals and SemaphoreLimits and QueueHandsOver and LocalVariablesAreSafe; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('EventSignals',
 "The threading documentation describes Event as a flag threads can wait for [P07]. A thread waiting on an Event stayed blocked for the 0.3 s before set() was called (True) and went on right after it (True); Event is the tool for 'wait until another thread says go' [T].",
 'An event is the simplest way for one thread to tell another that it may go on. This leaf sits in LocksAndEvents under SharedDataAndLocks beside LockFixesCounter and LockReleasedOnError and LockNotReentrant and DeadlockWithTwoLocks and SemaphoreLimits and QueueHandsOver and LocalVariablesAreSafe; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('SemaphoreLimits',
 'Wikipedia describes the semaphore, which Dijkstra introduced, and the threading documentation gives Semaphore and BoundedSemaphore [P45] [P52] [P07]. Six threads that each held a Semaphore of 2 for 0.1 s were inside the guarded block at most 2 at a time, against 6 without the semaphore [T].',
 'A semaphore limits how many threads work at once, for example how many connections a downloader opens. This leaf sits in LocksAndEvents under SharedDataAndLocks beside LockFixesCounter and LockReleasedOnError and LockNotReentrant and DeadlockWithTwoLocks and EventSignals and QueueHandsOver and LocalVariablesAreSafe; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('QueueHandsOver',
 'The queue documentation describes Queue as a thread-safe queue with task_done and join, and Wikipedia describes the producer-consumer problem [P11] [P48]. A producer thread put 5 numbers into a queue.Queue and a consumer thread received them in the order [0, 1, 2, 3, 4], ending at the marker None; the queue does its own locking, so no lock was written, and join() returned after 6 task_done() calls [T].',
 'The queue removes the shared variable the chapter warns about, because items are handed over, not shared. This leaf sits in LocksAndEvents under SharedDataAndLocks beside LockFixesCounter and LockReleasedOnError and LockNotReentrant and DeadlockWithTwoLocks and EventSignals and SemaphoreLimits and LocalVariablesAreSafe; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('LocalVariablesAreSafe',
 "The chapter's advice is to use only local variables in the target function, and the documentation describes thread-local data [P01] [P07] [P46]. Four threads that each summed their own list into a local variable returned [0, 45, 190, 435], and a threading.local() value set in one thread was absent in another; the chapter's advice to use only local variables in the target function is what these two results rest on [T].",
 'Local variables belong to one call of a function, so they cannot be shared between threads by accident. This leaf sits in LocksAndEvents under SharedDataAndLocks beside LockFixesCounter and LockReleasedOnError and LockNotReentrant and DeadlockWithTwoLocks and EventSignals and SemaphoreLimits and QueueHandsOver; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('MapKeepsOrder',
 'The concurrent.futures documentation says map returns results in the order of the inputs and as_completed yields futures as they finish, and PEP 3148 introduced the module [P08] [P31]. ThreadPoolExecutor.map returned [0, 1, 2] for tasks that finished in the reverse order, because it yields the results in the order of the inputs, while as_completed yielded them as [2, 1, 0] [T].',
 'The choice between the two decides whether the caller sees input order or completion order. This leaf sits in PoolBasics under ExecutorsAndPools beside FutureStates and DefaultWorkers and WorkerNames; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('FutureStates',
 "The documentation describes the Future object with running, done and result, and PEP 3148 explains why it was added [P08] [P31]. A Future returned by submit() was running True while its task slept, done True afterwards, and result() gave 42; the Future object is the receipt the book's join() cannot give, because a Thread has no return value [T].",
 "A Future is a receipt for a result that will exist later, which the chapter's Thread objects cannot give. This leaf sits in PoolBasics under ExecutorsAndPools beside MapKeepsOrder and DefaultWorkers and WorkerNames; its example ran in the environment of this study and the expected value is the one it printed [T].")
_b('DefaultWorkers',
 'The documentation gives the default number of workers as min(32, process_cpu_count() + 4) since Python 3.13 and explains the reason, and the source of thread.py implements it [P08] [P73] [P60]. On this machine with 2 CPUs a ThreadPoolExecutor created without max_workers got 6 workers (the documented rule since Python 3.13 is min(32, process_cpu_count() + 4)), and a 100-task run used at most that many distinct threads (True) [T].',
 'The default depends on the machine, so a course should print it before it reasons about speed. This leaf sits in PoolBasics under ExecutorsAndPools beside MapKeepsOrder and FutureStates and WorkerNames; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('WorkerNames',
 "The documentation lists thread_name_prefix as an argument of ThreadPoolExecutor [P08]. Worker threads of a pool created with thread_name_prefix='dl' were named ['dl_0', 'dl_1'] on Python 3.14.6, which helps to read a log in which several threads write [T].",
 'A prefix is the cheapest way to tell pools apart in a log. This leaf sits in PoolBasics under ExecutorsAndPools beside MapKeepsOrder and FutureStates and DefaultWorkers; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ExceptionAtResult',
 'The documentation says an exception raised by the call is raised again by result() and available from exception() [P08]. An exception raised inside a pool task stayed silent until result() was called, which then raised ValueError: boom; the exception() method gave ValueError without raising [T].',
 'The executor moves the error to the place where the result is used, which is easier to handle than a lost message. This leaf sits in PoolErrors under ExecutorsAndPools beside ResultTimeout and CancelPending and WithBlockWaits; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ResultTimeout',
 'The documentation says result(timeout) raises TimeoutError, and the Python 3.11 change made concurrent.futures.TimeoutError an alias of the built-in one [P08]. Result(timeout=0.1) on a task that needed 0.5 s raised TimeoutError, which is the built-in TimeoutError itself since Python 3.11 (True), and the task went on running [T].',
 'A timeout on the wait does not stop the task. This leaf sits in PoolErrors under ExecutorsAndPools beside ExceptionAtResult and CancelPending and WithBlockWaits; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('CancelPending',
 'The documentation says shutdown(cancel_futures=True) cancels all pending futures [P08]. With one worker and five queued 0.2 s tasks, shutdown(cancel_futures=True) cancelled 4 of the tasks that had not started and let 1 finish, because a started task cannot be cancelled [T].',
 'A running task cannot be cancelled, only waited for. This leaf sits in PoolErrors under ExecutorsAndPools beside ExceptionAtResult and ResultTimeout and WithBlockWaits; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('WithBlockWaits',
 'The documentation says leaving the with block calls shutdown(wait=True) [P08]. Leaving a with ThreadPoolExecutor block took at least the 0.3 s of the slowest task (True), the same job the chapter gives to the join() loop [T].',
 "The with statement does the work of the chapter's loop of join() calls. This leaf sits in PoolErrors under ExecutorsAndPools beside ExceptionAtResult and ResultTimeout and CancelPending; its example ran in the environment of this study and the expected value is the one it printed [T].")
_b('InterpreterPoolExists',
 'The Python 3.14 notes announce InterpreterPoolExecutor and the interpreters module, built on PEP 734 and PEP 684 [P20] [P16] [P30] [P29]. Python 3.14.6 has InterpreterPoolExecutor (True) and concurrent.interpreters (True); a task run in a worker interpreter returned a number and ran in a thread of the same process (process id equal: True) [T].',
 'Interpreters in one process, each with its own lock, are a third road between threads and processes. This leaf sits in InterpreterPools under ExecutorsAndPools beside no other leaf; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('GilOnInTheStandardBuild',
 'The glossary defines the global interpreter lock and the sys documentation describes sys._is_gil_enabled() [P19] [P12]. On the standard Python 3.14.6 build sys._is_gil_enabled() was True and the build variable Py_GIL_DISABLED was 0, so the global interpreter lock is on by default, as the glossary of the documentation says [T].',
 'The flag lets a program ask which build it runs on. This leaf sits in GilStatus under GilAndFreeThreading beside FreeThreadedBuildRuns and GilSwitchOnTheFreeBuild and ExtensionsMayReenableGil; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('FreeThreadedBuildRuns',
 "PEP 779 sets the criteria for the supported status of the free-threaded build, and the free-threading guide says how to install it, for example with uv [P28] [P17] [P59]. The free-threaded Python 3.14.6 installed with uv (3.14.6) reported sys._is_gil_enabled() as False, Py_GIL_DISABLED as 1, and 'free-threading build' in its version text (True); it needed no special compiler or flag [T].",
 'The build is an ordinary download, so a class can try it. This leaf sits in GilStatus under GilAndFreeThreading beside GilOnInTheStandardBuild and GilSwitchOnTheFreeBuild and ExtensionsMayReenableGil; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('GilSwitchOnTheFreeBuild',
 'The free-threading guide describes the PYTHON_GIL variable and the -X gil option [P17]. On the free-threaded build the environment variable PYTHON_GIL=1 turned the lock on (True), PYTHON_GIL=0 left it off (False), and the option -X gil=1 did the same as the variable (True) [T].',
 'A switch to turn the lock on again helps to find out whether a bug comes from the free-threaded build. This leaf sits in GilStatus under GilAndFreeThreading beside GilOnInTheStandardBuild and FreeThreadedBuildRuns and ExtensionsMayReenableGil; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ExtensionsMayReenableGil',
 'The free-threading guide says that some packages with an extension module may not be ready for a free-threaded build and will re-enable the GIL, and the extension guide explains how a module declares support [P17] [P18]. Importing a C extension that does not declare support for free-threading makes the free-threaded build switch the lock back on with a warning, according to the Python documentation; this study built no such extension, so the behaviour was NOT EXECUTED, and the check done was that the documentation page says it (True) [T].',
 'This behaviour was not run here, and a course should say what was read and what was run. This leaf sits in GilStatus under GilAndFreeThreading beside GilOnInTheStandardBuild and FreeThreadedBuildRuns and GilSwitchOnTheFreeBuild; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('GilBuildGivesNoSpeedup',
 'The Python wiki and Wikipedia describe the global interpreter lock as allowing one thread at a time to run Python bytecode [P39] [P42]. In the recorded run on the GIL build of Python 3.14.6, four CPU-bound tasks took 0.89 s one after another, 1.003 s on 2 threads and 1.003 s on 4 threads, so threads gave no speedup (the test that the 4-thread time was at least 0.8 of the serial time was True); single run at load 0.04 [T].',
 'CPU-bound threads on the GIL build do not run faster, which is the fact most beginners are surprised by. This leaf sits in CpuBoundThreads under GilAndFreeThreading beside FreeBuildScalesWithCores and SingleThreadCostOfFreeBuild and OlderInterpretersAlike; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('FreeBuildScalesWithCores',
 'PEP 703 states the goal that threads run Python code in parallel on several cores [P27]. In the recorded run on the free-threaded build, four CPU-bound tasks took 1.292 s serially, 0.553 s on 2 threads and 0.522 s on 4 threads on 2 CPUs; the 2-thread run took under 0.6 of the serial time: True; single run at load 0.04 [T].',
 "The result is for two cores and one run, and the speed-up is bounded by the number of cores as Amdahl's law says [[wamdahl]]. This leaf sits in CpuBoundThreads under GilAndFreeThreading beside GilBuildGivesNoSpeedup and SingleThreadCostOfFreeBuild and OlderInterpretersAlike; its example ran in the environment of this study and the expected value is the one it printed [T].")
_b('SingleThreadCostOfFreeBuild',
 'The free-threading guide and PEP 703 state that the free-threaded build can be slower in a single thread [P17] [P27]. The same serial loop took 1.292 s on the free-threaded build and 0.89 s on the GIL build in the recorded run; the free-threaded build was slower in a single thread: True, a cost the documentation also mentions, and the figure is one run [T].',
 'A single measurement cannot give the size of the cost, and the course should say so. This leaf sits in CpuBoundThreads under GilAndFreeThreading beside GilBuildGivesNoSpeedup and FreeBuildScalesWithCores and OlderInterpretersAlike; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('OlderInterpretersAlike',
 'The documentation of the older releases lists no change in how threads run CPU-bound code, and the Python 3.13 notes describe the first free-threaded build as experimental [P21]. On Python 3.13.14, 3.12.13 and 3.11.15 the 4-thread run took at least 0.8 of the serial time in every case (True), the same picture as 3.14.6 with the GIL [T].',
 'Earlier releases behave like the GIL build of 3.14. This leaf sits in CpuBoundThreads under GilAndFreeThreading beside GilBuildGivesNoSpeedup and FreeBuildScalesWithCores and SingleThreadCostOfFreeBuild; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('WaitingThreadsOverlap',
 "The chapter's downloader relies on threads waiting at the same time, and the documentation says the GIL is released while a thread waits for input or output [P01] [P07] [P19]. Eight sleeps of 0.5 s took 4.001 s one after another and 0.502 s on 8 threads on the GIL build, 0.503 s on the free-threaded build, so waiting overlaps whichever build runs it; this is the case the chapter's downloader relies on [T].",
 'Waiting overlaps on both builds, which is why threads suit downloads. This leaf sits in IoBoundThreads under GilAndFreeThreading beside PoolAndAsyncioMatch; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('PoolAndAsyncioMatch',
 'The documentation of concurrent.futures and asyncio presents both as ways to overlap waiting [P08] [P10]. The pool of 8 workers took 0.502 s and asyncio.gather 0.503 s for the same eight sleeps, within 0.05 s of the plain threads (True), so for waiting the three tools were equal on the timer [T].',
 'On a timer the three tools are equal, so the choice rests on code structure and not on speed. This leaf sits in IoBoundThreads under GilAndFreeThreading beside WaitingThreadsOverlap; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ProcessesDoNotShareVariables',
 "The chapter says a process cannot directly read and write another process's variables, and the multiprocessing documentation describes the ways to share data [P01] [P09] [P22]. A child process that set a module variable to 99 left the parent's copy at 0, while a thread that did the same left it at 99; the chapter's sentence that a process cannot directly read and write another process's variables holds, and threads are the opposite [T].",
 'A thread shares memory and a process copies it, which is the reason for the different tools. This leaf sits in Processes under ThreadsVersusOtherTools beside PopenReturnsAtOnce and ProcessPoolSpeedsCpuWork and DefaultStartMethod and StartCostThreadVersusProcess; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('PopenReturnsAtOnce',
 'The chapter says Popen() returns immediately and the launched program runs in its own process, and the subprocess documentation says the same [P01] [P14]. Subprocess.Popen returned after under 0.5 s (True) although the program it started slept for 1 s, its poll() was None at that moment, and wait() returned 0 later; the chapter says Popen returns at once and the launched program runs in its own process [T].',
 'Launching a program is the opposite of joining a thread: the caller goes on. This leaf sits in Processes under ThreadsVersusOtherTools beside ProcessesDoNotShareVariables and ProcessPoolSpeedsCpuWork and DefaultStartMethod and StartCostThreadVersusProcess; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ProcessPoolSpeedsCpuWork',
 'The multiprocessing documentation says it sidesteps the global interpreter lock by using subprocesses, and PEP 371 added the package [P09] [P32]. In the recorded run, 4 CPU-bound tasks took 0.963 s serially and 0.667 s on a pool of 2 processes, so processes gave a speedup on the GIL build that threads did not: True; single run [T].',
 'Processes give a speedup for CPU-bound work on the GIL build, at the cost of copying data. This leaf sits in Processes under ThreadsVersusOtherTools beside ProcessesDoNotShareVariables and PopenReturnsAtOnce and DefaultStartMethod and StartCostThreadVersusProcess; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('DefaultStartMethod',
 "The multiprocessing documentation says the default start method on POSIX changed from fork to forkserver in 3.14, and the 3.14 notes repeat it for ProcessPoolExecutor [P09] [P20]. The default start method of multiprocessing on Linux with Python 3.14.6 was forkserver, not fork; the documentation says the default was changed from fork to forkserver in 3.14 (True: the recorded run agrees with this process), so code that relied on a child inheriting the parent's variables breaks [T].",
 'A program that relied on fork to inherit state must now pass it explicitly. This leaf sits in Processes under ThreadsVersusOtherTools beside ProcessesDoNotShareVariables and PopenReturnsAtOnce and ProcessPoolSpeedsCpuWork and StartCostThreadVersusProcess; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('StartCostThreadVersusProcess',
 'The multiprocessing documentation notes that starting a process is slower than starting a thread, and Wikipedia describes the cost of processes against threads [P09] [P40] [P51]. In the recorded run, starting and joining a thread cost 112 microseconds and a process 5.4 milliseconds, a ratio of more than 30 to 1: True; single run [T].',
 'A thread is cheap to start, a process is not, and both costs are small beside a network request. This leaf sits in Processes under ThreadsVersusOtherTools beside ProcessesDoNotShareVariables and PopenReturnsAtOnce and ProcessPoolSpeedsCpuWork and DefaultStartMethod; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('GatherOverlapsWaits',
 'The asyncio documentation describes gather and the event loop, and PEP 3156 and PEP 492 introduced them [P10] [P24] [P33] [P34]. Ten coroutines that each awaited asyncio.sleep(0.3) finished together in under 0.6 s (True) on one thread (thread count during the run 1), so asyncio overlaps waiting without creating threads [T].',
 'Coroutines overlap waiting on one thread, with no lock needed between awaits. This leaf sits in AsyncioAndCoroutines under ThreadsVersusOtherTools beside BlockingCallStallsLoop and ToThreadBridge; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('BlockingCallStallsLoop',
 'The asyncio documentation warns that a blocking call stops the event loop [P10] [P24]. Five coroutines that called the blocking time.sleep(0.2) took at least 1.0 s together (True), against under 0.5 s with await asyncio.sleep(0.2) (True); one blocking call stops every other task on the loop [T].',
 'A coroutine must not call time.sleep or other blocking functions. This leaf sits in AsyncioAndCoroutines under ThreadsVersusOtherTools beside GatherOverlapsWaits and ToThreadBridge; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ToThreadBridge',
 'The asyncio documentation describes asyncio.to_thread as the way to run a blocking function in a thread without blocking the loop, and contextvars carries the context [P24] [P25]. Asyncio.to_thread ran a blocking call in a worker thread named asyncio while the event loop kept running (the loop thread was MainThread), and five such 0.2 s calls took under 0.6 s (True) [T].',
 'The bridge lets old blocking code live inside new asynchronous code. This leaf sits in AsyncioAndCoroutines under ThreadsVersusOtherTools beside GatherOverlapsWaits and BlockingCallStallsLoop; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ThreadApiAcrossReleases',
 'The Python 3.13 and 3.14 notes list what changed in threading, concurrent.futures and the GIL flag [P21] [P20]. One program that named a thread, started a pool and printed the lock state printed the same thread name, pool result and lock state under Python 3.11.15, 3.12.13, 3.13.14, 3.14.6 and the free-threaded 3.14.6 (True); its last value, the GIL flag, equalled the one of 3.14.6 in 2 of the 5 interpreters, because it is absent before 3.13 and False on the free-threaded build [T].',
 "The API a learner writes against has not changed between 3.11 and 3.14, which keeps the chapter's core stable. This leaf sits in Interpreters under EnvironmentAndEvidence beside FreeThreadedThirteenNotRun; its example ran in the environment of this study and the expected value is the one it printed [T].")
_b('FreeThreadedThirteenNotRun',
 'The Python 3.13 notes describe the free-threaded build of 3.13 as experimental [P21]. The free-threaded build of Python 3.13 (the first, experimental one) was NOT EXECUTED because only the 3.14.6 free-threaded build was installed; the study states the 3.13 behaviour only from the documentation, and the 3.13 GIL build had sys._is_gil_enabled() True [T].',
 'The build was not installed, so the study makes no claim about it beyond the documentation. This leaf sits in Interpreters under EnvironmentAndEvidence beside ThreadApiAcrossReleases; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('ThreadLimitOfTheMachine',
 'The Wikipedia article on threads describes the cost of a thread and the operating system sets the limit, and os.cpu_count() reports the processors [P40] [P60]. Starting 2,000 threads that each waited on one Event succeeded in this container (True) and all 2,001 thread objects including the main thread were alive at the same time: True, so the practical limit for I/O-bound threads on this machine was far above the 14 threads of the chapter; the limit differs from machine to machine and was not searched for [T].',
 "A thousand idle threads are possible, which is far more than the chapter's 14, and the limit is a fact of the machine. This leaf sits in Platforms under EnvironmentAndEvidence beside no other leaf; its example ran in the environment of this study and the expected value is the one it printed [T].")
_b('ChapterDigest',
 "The 2nd-edition chapter page is the text the study read, and the book's page places it in the book [P01] [P03]. The page of chapter 17 of the 2nd edition was fetched on 2026-10-14 and returned 200 with more than 100,000 bytes (True); its section Multithreading, which runs up to the heading Launching Other Programs from Python, holds 9 code paragraphs, and those paragraphs are the listings the study replayed [T].",
 'A fixed page, size and count of code paragraphs let another reader check the same text. This leaf sits in Reproducibility under EnvironmentAndEvidence beside DroppedFromThirdEdition; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('DroppedFromThirdEdition',
 'The 3rd-edition chapter with the same title and its table of contents were read [P74] [P02]. Chapter 19 of the 3rd edition, which has the same title as chapter 17 of the 2nd, Keeping Time, Scheduling Tasks, and Launching Programs, was fetched the same day and returned 200 with 0 occurrences of the word thread, while it still teaches the subprocess module (True); the multithreading material of this subject is therefore not in the 3rd edition [T].',
 'The material that this package teaches is absent from the current edition, which is the reason for the package. This leaf sits in Reproducibility under EnvironmentAndEvidence beside ChapterDigest; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('NotExecutedList',
 'The study names what it could not run so that a reader does not take a reading of documentation for a result [P17] [P05]. What this machine cannot or did not run is stated: the free-threaded 3.13 build, a C extension that re-enables the lock, Windows and macOS thread behaviour, more than 2 CPUs, the real xkcd.com site, and runs under load; the machine had 2 CPUs, no GPU is used, and the platform was Linux [T].',
 'The list follows from the facts of the machine and not from choice. This leaf sits in HonestyOfTheStudy under EnvironmentAndEvidence beside SingleRunLabels; its example ran in the environment of this study and the expected value is the one it printed [T].')
_b('SingleRunLabels',
 'The timing record states the load average before every run and the study waited for a quiet machine [P07]. Every timing in the study is one run on 2026-10-14; the timing record has 25 runs and each states the load average before it began, with the largest at 0.75 (below 1.0: True), so the machine was quiet when it was timed [T].',
 'A single run is a sample, and the course should not present it as a distribution. This leaf sits in HonestyOfTheStudy under EnvironmentAndEvidence beside NotExecutedList; its example ran in the environment of this study and the expected value is the one it printed [T].')

_CITE = {"T": "(This study, 2026)"}
for _p in PUBS:
    _m = re.search(r"\((?:[^()]*), \d{4}\)$", _p[1])
    _CITE[_p[0]] = _m.group(0)
for _k in list(BODY):
    _t = BODY[_k]
    for _n, _v in _CITE.items():
        _t = _t.replace("[" + _n + "]", _v)
    BODY[_k] = _t.replace('"', "'")
