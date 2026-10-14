"""Writes limits_v1_0_0.json, the Threads page's 'Provenance & known limits' entries, from the records the research made
(live_observations_v1_0_0.json, timing_record_v1_0_0.json), pywheels_v1_0_0.json, standin_v1_0_0.json
and the 'Not executed' sentence of sen0414_ch25_rdodi_data_v1_0_0.py. Numbers are read from those files. Usage: limits_make_v1_0_0.py"""
__version__ = "1.0.0"
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(H, n)))
lv, tr, pw, so = J("live_observations_v1_0_0.json"), J("timing_record_v1_0_0.json"), J("pywheels_v1_0_0.json"), J("standin_v1_0_0.json")
src = open(os.path.join(H, "..", "sen0414_ch25_rdodi_data_v1_0_0.py"), encoding="utf-8").read()
m = re.search(r"Not executed, and said so where it comes up: (.*?under load)\.", src, re.S)
notexec = re.sub(r"\s+", " ", m.group(1)).strip()
ch = next(s for s in lv["sources"] if s["url"] == "https://automatetheboringstuff.com/2e/chapter17/")
rec = so["recorded"]; pics = so["pictures"]; runs = tr["runs"]
running = [n["id"] for n in J("page_data_v9_35_0.json")["nodes"] if "io" in n and n["id"] not in rec]  # the examples that run in the browser
load = max(r["load_before"] for r in runs.values())
out = []
out.append("Python and libraries on this page: the page's own playground runs in your browser, in Python 3.13.2, while the research ran Python 3.14.6 on Linux (2 CPUs) with requests 2.34.2 and beautifulsoup4 4.15.0, and timed the standard 3.14.6 build against the free-threaded 3.14.6 build and Python 3.13.14, 3.12.13 and 3.11.15.")
out.append("What a browser's Python does with threads: it has a threading module and a concurrent.futures module, but it cannot start a thread. Thread.start(), threading.Timer.start() and ThreadPoolExecutor.submit (and so map) raise RuntimeError: can't start new thread; Lock, Event and queue.Queue exist and work inside the one thread (a Lock's second acquire with a timeout returned False, an Event's wait with a timeout returned False until set()); subprocess raises OSError: emscripten does not support processes, a multiprocessing Process raises OSError: Function not implemented and ProcessPoolExecutor raises NotImplementedError; asyncio's run_until_complete raised RuntimeError in the page's runner. time.sleep blocks the one thread. This was checked in the browser when the page was built, with Pyodide 0.28.2 (Python 3.13.2, platform 'emscripten', sys._is_gil_enabled() True), and is a finding about this build of the browser's Python, not a statement about every browser or every Python in WebAssembly.")
out.append("Recorded, not run: %d of the %d examples of the chapter; the other %d run in your browser (%s) and equal what the research recorded. Each recorded example needs something a browser's Python cannot give (a second thread, a child interpreter, sockets, a file of the repository) or prints something else there, and is shown with its output recorded under Python 3.14.6, labelled 'Recorded, not run on this page', with its reason: %s." % (len(rec), len(rec) + len(running), len(running), ", ".join(running), ", ".join(sorted(rec))))
out.append("Stand-in: a local HTTP server on 127.0.0.1 stood in for xkcd.com; the real site was never contacted and no comic was fetched or shown. Its answers are 100 bytes of text, so the speed-up of threads against it is the speed-up of overlapping a fixed wait.")
out.append("Picture: %d recorded picture drawn by the deck's program (under %s) is shown beside its example, labelled 'Recorded picture, not made on this page'; it is SHA-256 checked when the page is made." % (len(pics), ", ".join(sorted(pics))))
out.append("No wheel is embedded on this page and no file of the book's online materials (their licence has not been checked, an open question for the owner, 03-materials/ch25/assets/ASSETS_PROVENANCE_v1_0_0.md). This page has no book ontology: the 3rd edition has no chapter 25 and does not teach multithreading, so the material is the 2nd edition's chapter 17.")
out.append("NOT EXECUTED: " + notexec + ".")
out.append("What the public sites answered on 2026-10-14 is in live_observations_v1_0_0.json: %d of %d sources answered 200 and held the text the research relied on; the 2nd edition's chapter 17 page answered %d with %s bytes, and the 3rd edition's chapter 19, with the same title, has no occurrence of the word thread." % (lv["ok"], lv["total"], ch["status"], "{:,}".format(ch["bytes"])))
out.append("Every timing is one run on 2026-10-14 on 2 CPUs (%d runs in timing_record_v1_0_0.json, the largest one-minute load average before a run %.2f); a different machine, more cores or a loaded machine gives other numbers, and the free-threaded 3.14.6 speed-up was measured on 2 CPUs only." % (len(runs), load))
json.dump({"_version": __version__, "limits": out}, open(os.path.join(H, "limits_v1_0_0.json"), "w"), indent=1, ensure_ascii=False)
for x in out: print("-", x[:200])
