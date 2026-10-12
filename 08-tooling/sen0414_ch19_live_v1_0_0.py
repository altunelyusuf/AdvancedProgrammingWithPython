#!/usr/bin/env python3
"""Chapter 19 (Keeping Time, Scheduling Tasks, and Launching Programs): observes, once, what the public sources the chapter names answer today and
what the machine's own operating system tools do, and writes what it saw with the date. A web site changes and the files of the online materials may be
replaced; the record is an observation of the day, not something the build can re-check, and no check reads it.
What it does: fetches the chapter page and compares its SHA-256 with the digest the book's own ontology records; counts what is on the page (listings,
figures with the HTTP status of each image, tables, practice questions) and asks every external link of the chapter once without following a redirect;
downloads the online materials of the 3rd edition and checks the three files of chapter 19 (calcProd.py, stopwatch.py, simplecountdown.py) against the SHA-256
the research recorded; asks autbor.com for simplecountdown.py and alarm.wav and follows the redirect of strftime.org; reads Appendix A for the versions the
book pins and Appendix B for the answers to the chapter's seven questions; checks that the book page the chapter's Summary points to for scheduling holds no
instructions for it; reads the newest releases and upload dates of pyperclip, playsound3, tzdata and schedule on PyPI; opens the pages that give the stories
their dates; asks python.org which release is the newest and uv which 3.14 and 3.15 releases it can install; and opens every source of the research record and
checks that the passages the research relies on are on the page. On the machine itself it runs the operating system's own scheduler for real: it starts cron,
installs a crontab whose entry runs a Python program every minute and reads what that program saw (the time of the job against the clock of the machine, the
environment variables, the working directory, whether it had a terminal); it installs a crontab with a TZ line, and one with CRON_TZ lines for two zones and
reads which entries fired at the target moment; it asks systemd-analyze to normalise an OnCalendar expression; it asks the system which program `open` is;
it pings with the Windows and the Linux flag; and it builds a launchd property list with plistlib. NOT EXECUTED: Windows Task Scheduler (schtasks), launchd
itself, a systemd timer (the container has no systemd as process 1), Windows and macOS themselves, a desktop session. Nothing is posted anywhere and every URL is
asked once; the cron experiments wait for the minute to turn and take about seven minutes in all.
Run it with an interpreter that has requests and Beautiful Soup (/home/claude/venv314_web/bin/python), as root on a machine where cron is installed.
Usage: sen0414_ch19_live_v1_0_0.py   -> ch19-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time, zipfile
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch19-page", "live_observations_v1_0_0.json")
UA = {"User-Agent": "SEN0414-research/1.0 (teaching; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
PYTHON = os.environ.get("CH19_LATEST", "/home/claude/venv314_ch19_latest/bin/python")
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:200])
    obs.append({"what": what, "saw": v})
def get(u, **k):
    k.setdefault("headers", BROWSER)
    for attempt in range(6):       # a site that answers 429 (too many requests) or drops the connection is asked again after a pause; the status of the last answer is the one recorded
        try:
            r = requests.get(u, timeout=90, **k)
            if r.status_code != 429: return r
        except requests.ConnectionError:
            if attempt == 5: raise
        time.sleep(20)
    return r
def sha(b): return hashlib.sha256(b).hexdigest()
def norm(t): return re.sub(r"\s+", " ", t)
def visible(r):
    s = bs4.BeautifulSoup(r.text, "html.parser")
    for x in s(["script", "style"]): x.decompose()
    return norm(s.get_text(" "))
WORK = tempfile.mkdtemp()
SOURCES = [
    ('P01', 'https://automatetheboringstuff.com/3e/chapter19.html', ['Returning the Epoch Timestamp', 'Super Stopwatch', 'Simple Countdown', 'Friday the 13th Finder', 'Running Task Scheduler, launchd, and cron', 'Table 19-1']),
    ('P02', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', []),
    ('P03', 'https://automatetheboringstuff.com/3e/', ['Keeping Time, Scheduling Tasks, and Launching Programs']),
    ('P04', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', ['Keeping Time, Scheduling Tasks, and Launching Programs']),
    ('P05', 'https://automatetheboringstuff.com/3e/appendixa.html', ['playsound3==2.4.0', 'pyperclip', 'xclip']),
    ('P06', 'https://automatetheboringstuff.com/3e/appendixb.html', ['time.asctime()', 'closest integer', 'weekday()']),
    ('P07', 'https://autbor.com/simplecountdown.py', ['timeLeft', 'alarm.wav']),
    ('P08', 'https://strftime.org', ['strftime']),
    ('P09', 'https://inventwithpython.com/beyond/chapter13.html', ['Big O', 'cProfile']),
    ('P10', 'https://docs.python.org/3.14/library/time.html', ['epoch', 'clock_nanosleep', 'monotonic', 'perf_counter', 'leap seconds', '1969']),
    ('P11', 'https://docs.python.org/3.14/library/datetime.html', ['utcnow', 'fold', 'idealized naive date', 'always include a year', 'Deprecated since version 3.13', 'fromisoformat']),
    ('P12', 'https://docs.python.org/3.14/library/zoneinfo.html', ['tzdata', 'PYTHONTZPATH', 'ZoneInfoNotFoundError', 'TZPATH']),
    ('P13', 'https://docs.python.org/3.14/library/subprocess.html', ['capture_output', 'shell=True', 'CompletedProcess', 'kill()', 'poll()', 'Security Considerations']),
    ('P14', 'https://docs.python.org/3.14/library/threading.html', ['Timer', 'cancel']),
    ('P15', 'https://docs.python.org/3.14/library/sched.html', ['scheduler', 'enterabs', 'priority']),
    ('P16', 'https://docs.python.org/3.14/library/asyncio-eventloop.html', ['call_later', 'call_at']),
    ('P17', 'https://docs.python.org/3.14/library/signal.html', ['setitimer', 'SIGALRM', 'SIGKILL']),
    ('P18', 'https://docs.python.org/3.14/library/webbrowser.html', ['open_new_tab', 'BROWSER']),
    ('P19', 'https://docs.python.org/3.14/library/os.html', ['startfile']),
    ('P20', 'https://docs.python.org/3.14/library/shlex.html', ['quote', 'split']),
    ('P21', 'https://docs.python.org/3.14/library/calendar.html', ['timegm', 'isleap', 'proleptic']),
    ('P22', 'https://docs.python.org/3.14/library/stdtypes.html', ['Integer string conversion length limitation', '4300']),
    ('P23', 'https://docs.python.org/3.14/library/plistlib.html', ['plist']),
    ('P24', 'https://docs.python.org/3.14/library/timeit.html', ['timeit', 'perf_counter']),
    ('P25', 'https://docs.python.org/3.14/library/functions.html', ['round(']),
    ('P26', 'https://docs.python.org/3.14/whatsnew/3.14.html', ['Add the strptime() method to the datetime.date and datetime.time classes']),
    ('P27', 'https://docs.python.org/3.12/whatsnew/3.12.html', ['utcnow', 'utcfromtimestamp', 'DeprecationWarning']),
    ('P28', 'https://docs.python.org/3.11/whatsnew/3.11.html', ['clock_nanosleep', 'fromisoformat', 'datetime.UTC']),
    ('P29', 'https://docs.python.org/3.15/whatsnew/3.15.html', ['strptime() now raises ValueError when the format string contains %d']),
    ('P30', 'https://peps.python.org/pep-0418/', ['monotonic', 'perf_counter']),
    ('P31', 'https://peps.python.org/pep-0475/', ['EINTR', 'sleep']),
    ('P32', 'https://peps.python.org/pep-0495/', ['fold', 'ambiguous']),
    ('P33', 'https://peps.python.org/pep-0615/', ['zoneinfo', 'tzdata']),
    ('P34', 'https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html', ['Seconds Since the Epoch', 'tm_yday', '31536000']),
    ('P35', 'https://pubs.opengroup.org/onlinepubs/9799919799/utilities/crontab.html', ['crontab', 'minute']),
    ('P36', 'https://www.rfc-editor.org/rfc/rfc3339', ['date-time', 'leap second']),
    ('P37', 'https://www.rfc-editor.org/rfc/rfc9557', ['time zone', 'Suffix']),
    ('P38', 'https://www.rfc-editor.org/rfc/rfc6557', ['Procedures for Maintaining the Time Zone Database']),
    ('P39', 'https://www.iana.org/time-zones', ['Time Zone Database']),
    ('P40', 'https://manpages.debian.org/bookworm/cron/crontab.5.en.html', ['LOGNAME', 'SHELL is set to /bin/sh', 'MAILTO', 'the command will be run when either field matches the current time', 'CRON_TZ']),
    ('P41', 'https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create', ['schtasks', '/create']),
    ('P42', 'https://keith.github.io/xcode-man-pages/launchd.plist.5.html', ['StartCalendarInterval', 'launchd']),
    ('P43', 'https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html', ['OnCalendar', 'Persistent']),
    ('P44', 'https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html', ['calendar']),
    ('P45', 'https://www.freedesktop.org/wiki/Software/xdg-utils/', ['xdg-open']),
    ('P46', 'https://manpages.ubuntu.com/manpages/noble/man1/xdg-open.1.html', ['xdg-open']),
    ('P47', 'https://pyperclip.readthedocs.io/en/latest/', ['xclip', 'clipboard']),
    ('P48', 'https://pypi.org/pypi/pyperclip/json', ['pyperclip']),
    ('P49', 'https://pypi.org/pypi/playsound3/json', ['playsound3']),
    ('P50', 'https://pypi.org/pypi/tzdata/json', ['tzdata']),
    ('P51', 'https://pypi.org/pypi/schedule/json', ['schedule']),
    ('P52', 'https://en.wikipedia.org/wiki/Unix_time', ['The current epoch of 1 January 1970 00:00:00 UTC was selected arbitrarily', 'measured in sixtieths of a second', '2.26 years']),
    ('P53', 'https://en.wikipedia.org/wiki/Year_2038_problem', ['03:14:07 UTC on 19 January 2038', 'signed 32-bit integer']),
    ('P54', 'https://en.wikipedia.org/wiki/Cron', ['Robert Brown', 'Franta', 'Purdue', 'CRON_TZ']),
    ('P55', 'https://en.wikipedia.org/wiki/Leap_second', ['27 leap seconds have been added', '31 December 2016', '2035']),
    ('P56', 'https://www.bipm.org/en/cgpm-2022/resolution-4', ['UT1-UTC', '2035']),
    ('P57', 'https://en.wikipedia.org/wiki/Tz_database', ['Astrolabe, Inc. v. Olson', '6 October 2011', '14 October 2011', '22 February 2012']),
    ('P58', 'https://en.wikipedia.org/wiki/Gregorian_calendar', ['Inter gravissimas dated 24 February 1582', 'Thursday 4 October 1582 was followed by Friday 15 October 1582']),
    ('P59', 'https://en.wikipedia.org/wiki/Launchd', ['Dave Zarzycki', 'Tiger']),
    ('P60', 'https://en.wikipedia.org/wiki/Triskaidekaphobia', ['Friday the 13th']),
    ('P61', 'https://en.wikipedia.org/wiki/Coordinated_Universal_Time', ['UTC']),
    ('P62', 'https://en.wikipedia.org/wiki/ISO_8601', ['ISO 8601']),
    ('P63', 'https://docs.astral.sh/uv/concepts/python-versions/', ['uv python install']),
    ('P64', 'https://www.python.org/downloads/', ['Python 3.14']),
]
def sources():
    out = []
    for pid, url, phrases in SOURCES:
        try:
            r = get(url, headers=BROWSER if "nostarch.com" in url else UA); ctype = r.headers.get("content-type", "")
            if "zip" in ctype or url.endswith(".zip"): t = ""
            else:
                if "html" in ctype or "text/plain" in ctype:
                    try: t = r.content.decode("utf-8")
                    except UnicodeDecodeError: t = r.text
                else: t = r.text
                if "html" in ctype:
                    s = bs4.BeautifulSoup(t, "html.parser")
                    for x in s(["script", "style"]): x.decompose()
                    t = s.get_text(" ")
            t = norm(t).replace("’", "'")
            out.append([pid, r.status_code, len(r.content), {p: (norm(p).replace("’", "'").lower() in t.lower()) for p in phrases}])
        except Exception as e: out.append([pid, "unreachable: %s" % type(e).__name__, 0, {}])
    return out

# 0. the chapter and the book's own record of it
ch = get("https://automatetheboringstuff.com/3e/chapter19.html", headers=UA)
DIGEST = "067b9119b1a4c68cf65acedab9e68df264d609e72345fdbb112bcfd6db475db7"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch19_v1_0_0.ttl"
see("chapter 19 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not present"])
soup = bs4.BeautifulSoup(ch.text, "html.parser"); text = norm(soup.get_text(" "))
see("chapter 19 page: number of listings (pre elements), figure captions, tables, images and the HTTP status of each image file", lambda: [len(soup.find_all("pre")), sorted(set(re.findall(r"Figure 19-\d+", text))), sorted(set(re.findall(r"Table 19-\d+", text))), len(soup.find_all("table")), [(i["src"], get("https://automatetheboringstuff.com/3e/" + i["src"].lstrip("/") if not i["src"].startswith("/") else "https://automatetheboringstuff.com" + i["src"]).status_code) for i in soup.find_all("img") if i.get("src") and "cover" not in i["src"]]])
see("chapter 19 page: alt text of the pictures (an empty alt on the opener and a description of the calculators on Figure 19-1)", lambda: [i.get("alt") for i in soup.find_all("img") if i.get("src") and "cover" not in i["src"]])
see("chapter 19 page: the headings of the chapter in order", lambda: [(h.name, norm(h.get_text())) for h in soup.find_all(["h2", "h3", "h4", "h5"])])
STATEMENTS = ("the epoch timestamp", "Pacific Standard Time", "1970 to 2069", "datetime.delta()", "Chapter 13 of my other book", "the instructions at https://nostarch.com/automate-boring-stuff-python-3rd-edition",
              "On macOS and Linux, this is the open command", "the pyperclip module introduced in Chapter 8", "Chapter 12 covers the playsound3 module", "returns a string description of the current time",
              "Halloween 2039", "stop when it reaches the year 1", "a variable amount of time depending on the particular month or year")
see("chapter 19 page: statements the research relies on (each is on the page of the book: True)", lambda: {s: (norm(s) in text) for s in STATEMENTS})
see("chapter 19 page: words the chapter never uses although the topic needs them (False means absent from the page)", lambda: {s: s.lower() in text.lower() for s in ("zoneinfo", "tzinfo", "UTC", "utcnow", "monotonic", "perf_counter", "timeit", "isoformat", "check=True", "timeout", "shlex", "sched", "Timer", "asyncio", "daylight", "leap second", "fold", "2038", "crontab", "schtasks", "systemd", "xdg-open", "startfile", "shell=True", "SIGKILL", "terminate")})
ext = sorted({a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http") and "automatetheboringstuff.com" not in a["href"]})
def link_status():
    out = []
    for u in ext:
        try:
            r = requests.get(u, timeout=60, headers=BROWSER, allow_redirects=False); out.append([u, r.status_code, r.headers.get("Location", "")[:100]])
        except Exception as e: out.append([u, "unreachable: %s" % type(e).__name__, ""])
    return out
see("chapter 19 page: every external link of the chapter, asked once without following a redirect: URL, HTTP status, Location", link_status)
see("chapter 19 page: every URL that appears in the text of the chapter", lambda: sorted({u.rstrip(".,)") for u in re.findall(r"https?://[\w./?=&#%~:+-]+", text) if "automatetheboringstuff.com/3e/chapter19" not in u}))
def appendix():
    a = get("https://automatetheboringstuff.com/3e/appendixa.html", headers=UA); t = visible(a)
    return [a.status_code, re.findall(r"(?:playsound3|pyperclip|requests|tzdata|pytz)\s*[=~<>]+\s*[\w.]+", t), "playsound3==2.4.0" in t, "pyperclip" in t, "sudo apt install xclip" in t]
see("Appendix A of the book: status, the pins of the packages chapter 19 names, whether the pin the study replayed is on the page, whether pyperclip is listed without a pin, the xclip advice", appendix)
def appendixb():
    a = get("https://automatetheboringstuff.com/3e/appendixb.html", headers=UA); t = visible(a)
    i = t.find("Chapter 19 1."); j = t.find("Chapter 20", i)
    return [a.status_code, t[i:j][:1500]]
see("Appendix B of the book: the answers printed for the seven questions of chapter 19", appendixb)
def bookpage():
    r = get("https://nostarch.com/automate-boring-stuff-python-3rd-edition"); t = visible(r)
    sched = [a["href"] for a in bs4.BeautifulSoup(r.text, "html.parser").find_all("a", href=True) if re.search(r"sched|cron|launchd", a["href"], re.I)]
    return [r.status_code, len(r.content), {w: len(re.findall(w, t, re.I)) for w in ("cron", "launchd", "Task Scheduler", "schedul", "Scheduling Tasks")}, sched]
see("the book page at nostarch.com that the Summary of chapter 19 points to for 'the instructions' on the operating system's scheduler: how often each word occurs on the page, and links with sched, cron or launchd in them", bookpage)
def toc():
    r = get("https://automatetheboringstuff.com/3e/", headers=UA); t = visible(r)
    return [r.status_code, {w: len(re.findall(w, t, re.I)) for w in ("cron", "launchd", "Task Scheduler", "Scheduling Tasks")}, re.findall(r"Appendix [A-Z] - [\w ,']+", t)]
see("the table of contents of the book online: words about scheduling and the appendices it lists", toc)

# 1. the online materials and the files at autbor.com
mat = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip")
see("online materials of the 3rd edition: status, bytes, SHA-256 of the zip", lambda: [mat.status_code, len(mat.content), sha(mat.content)])
RECORDED = {'calcProd.py': '829148ea78d9e93b55c068b3584532567e1d355301a0380df8d9e0be814783fc', 'stopwatch.py': 'c3405030450860ee6371080d91edc35f7a1d8c7bab94f7c59d7dcb6fd7b37ab9', 'simplecountdown.py': '3fc7a82af22a918d912ba46fa171d02061217db4f0c439d81cdf22b3e0eb4fde'}
def materials():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); names = [n for n in z.namelist() if not n.endswith("/") and "__MACOSX" not in n and not n.split("/")[-1].startswith("._")]
    got = {n.split("/")[-1]: sha(z.read(n)) for n in names if n.split("/")[-1] in RECORDED}
    base = [n.split("/")[-1] for n in names]
    texts = {n.split("/")[-1]: z.read(n).decode("utf-8", "replace") for n in names if n.endswith(".py")}
    return {"files": len(names), "each recorded file is there with the recorded SHA-256": {k: got.get(k) == v for k, v in RECORDED.items()},
            "files chapter 19 names or needs that the zip does not hold": {n: (n in base) for n in ("alarm.wav", "hello.txt", "prettifiedStopwatch.py", "fridayThirteenth.py", "crontab", "scheduler.md")},
            "python files that mention cron, launchd, schtasks or a scheduler": sorted(k for k, v in texts.items() if re.search(r"cron|launchd|schtasks|scheduler", v, re.I)),
            "python files that import datetime, time or subprocess": sorted(k for k, v in texts.items() if re.search(r"^\s*(import|from)\s+(datetime|time|subprocess)", v, re.M))}
see("online materials: the files (without the macOS resource forks), whether the three files of chapter 19 match the SHA-256 recorded by the study, what the zip does not hold and whether any file in it is about scheduling", materials)
def shipped_text():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); P = "Automate_the_Boring_Stuff_3e_onlinematerials/"; out = {}
    for n in RECORDED:
        t = z.read(P + n).decode("utf-8"); out[n] = {"bytes": len(t.encode()), "crlf lines": t.count("\r\n"), "en dashes": t.count("–"), "compiles": None}
        try: compile(t, n, "exec"); out[n]["compiles"] = True
        except SyntaxError as e: out[n]["compiles"] = "%s: %s" % (type(e).__name__, e.msg)
    out["stopwatch.py has the f prefix on its print"] = "print(f'" in z.read(P + "stopwatch.py").decode()
    return out
see("online materials: the three files of chapter 19 as the compiler reads them (line ends, en dashes, whether they compile)", shipped_text)
def autbor():
    out = {}
    for u in ("https://autbor.com/simplecountdown.py", "https://autbor.com/alarm.wav"):
        r = requests.get(u, headers=UA, timeout=60, allow_redirects=False); out[u] = [r.status_code, r.headers.get("Location", ""), len(r.content)]
    w = requests.get("https://autbor.com/alarm.wav", headers=UA, timeout=60); out["alarm.wav after the redirect"] = [w.status_code, w.url, len(w.content), sha(w.content)[:16], w.headers.get("content-type")]
    s = requests.get("https://autbor.com/simplecountdown.py", headers=UA, timeout=60).text; shipped = zipfile.ZipFile(io.BytesIO(mat.content)).read("Automate_the_Boring_Stuff_3e_onlinematerials/simplecountdown.py").decode()
    out["simplecountdown.py at autbor.com equals the shipped file"] = s.replace("\r\n", "\n") == shipped.replace("\r\n", "\n")
    out["lines of the autbor.com file that are not in the shipped file"] = [l for l in s.replace("\r\n", "\n").split("\n") if l not in shipped.replace("\r\n", "\n").split("\n")]
    return out
see("autbor.com: the status and Location of simplecountdown.py and alarm.wav, the sound file after the redirect, and how the script served there differs from the shipped file", autbor)
def strftime_org():
    r = requests.get("https://strftime.org", headers=UA, timeout=60, allow_redirects=False); f = requests.get("https://strftime.org", headers=UA, timeout=60)
    return [r.status_code, r.headers.get("Location"), f.status_code, f.url, bs4.BeautifulSoup(f.text, "html.parser").title.get_text().strip()]
see("strftime.org, which the chapter names for the strftime directives: status and Location of the first answer, and where a browser ends", strftime_org)

# 2. the packages on PyPI
def pypi():
    out = {}
    for n in ("pyperclip", "playsound3", "tzdata", "schedule"):
        j = requests.get("https://pypi.org/pypi/%s/json" % n, headers=UA, timeout=60).json(); v = j["info"]["version"]
        out[n] = [v, (j["releases"][v][0]["upload_time"] if j["releases"].get(v) else None), j["info"].get("requires_python"), len(j["releases"])]
    return out
see("PyPI: newest release of each package the study uses: version, upload time, Requires-Python, number of releases", pypi)
def pinned():
    out = {}
    for n, v in (("playsound3", "2.4.0"), ("pyperclip", "1.9.0")):
        j = requests.get("https://pypi.org/pypi/%s/%s/json" % (n, v), headers=UA, timeout=60).json()
        out["%s %s" % (n, v)] = [j["urls"][0]["upload_time"] if j["urls"] else None, j["info"].get("requires_python")]
    return out
see("PyPI: the upload time and Requires-Python of playsound3 2.4.0, the version the book pins, and of pyperclip 1.9.0", pinned)
def tzdata_map():
    j = requests.get("https://pypi.org/pypi/tzdata/json", headers=UA, timeout=60).json(); v = j["info"]["version"]
    return [v, j["info"]["summary"], sorted(j["releases"], key=lambda s: [int(x) for x in s.split(".") if x.isdigit()])[-5:]]
see("PyPI: tzdata, the newest release and its five newest version numbers (the version is the year and the release of that year, 2026.5 holds the IANA release 2026e)", tzdata_map)

# 3. the dates that the stories rest on
def wp(u, needles, w=140):
    t = visible(get(u, headers=UA)); r = {}
    for n in needles:
        i = t.find(n); r[n] = t[max(0, i - w): i + len(n) + w] if i >= 0 else None
    return r
see("Wikipedia, Unix time: the epoch chosen arbitrarily and the two early epochs, 1971 and 1972, with the manual sentences", lambda: wp("https://en.wikipedia.org/wiki/Unix_time", ["The current epoch of 1 January 1970 00:00:00 UTC was selected arbitrarily", "measured in sixtieths of a second", "2.26 years"], 220))
see("Wikipedia, Year 2038 problem: the first sentence and the overflow time", lambda: wp("https://en.wikipedia.org/wiki/Year_2038_problem", ["03:14:07 UTC on 19 January 2038", "03:14:08 UTC on 19 January 2038"], 200))
see("Wikipedia, Cron: the Version 7 algorithm, Purdue and Robert Brown", lambda: wp("https://en.wikipedia.org/wiki/Cron", ["Sleep for one minute", "In an experiment at Purdue University in the late 1970s", "A Purdue graduate student, Robert Brown", "CRON_TZ"], 260))
see("Wikipedia, Leap second: 1972, 27 leap seconds, the most recent on 31 December 2016", lambda: wp("https://en.wikipedia.org/wiki/Leap_second", ["The leap second was introduced in 1972", "27 leap seconds have been added"], 260))
see("BIPM, Resolution 4 of the 27th CGPM (2022): the sentence on the maximum value of UT1-UTC", lambda: wp("https://www.bipm.org/en/cgpm-2022/resolution-4", ["Resolution 4 of the 27th CGPM (2022)", "decides that the maximum value for the difference (UT1-UTC) will be increased in, or before, 2035"], 200))
see("Wikipedia, tz database: the lawsuit and ICANN", lambda: wp("https://en.wikipedia.org/wiki/Tz_database", ["On 30 September 2011, a lawsuit, Astrolabe, Inc. v. Olson et al., was filed", "ICANN took responsibility for the maintenance of the database on 14 October 2011", "resolved on 22 February 2012", "Arthur David Olson"], 260))
see("Wikipedia, Gregorian calendar: the bull and the ten days", lambda: wp("https://en.wikipedia.org/wiki/Gregorian_calendar", ["papal bull Inter gravissimas dated 24 February 1582", "Thursday 4 October 1582 was followed by Friday 15 October 1582"], 260))
see("Python documentation of datetime: the sentences on the Gregorian calendar, UTC and the leap day", lambda: wp("https://docs.python.org/3.14/library/datetime.html", ["assuming the current Gregorian calendar always was, and always will be, in effect", "always include a year in the format", "Deprecated since version 3.13, will be removed in version 3.15"], 200))
see("Python 3.15 'What's New': the sentence on strptime and a day without a year", lambda: wp("https://docs.python.org/3.15/whatsnew/3.15.html", ["strptime() now raises ValueError when the format string contains %d"], 200))
see("Python 3.14 'What's New': the sentence on date.strptime and time.strptime", lambda: wp("https://docs.python.org/3.14/whatsnew/3.14.html", ["Add the strptime() method to the datetime.date and datetime.time classes"], 200))
see("Python documentation of time: the %y rule and the epoch, leap seconds and the system clock", lambda: wp("https://docs.python.org/3.14/library/time.html", ["1969", "leap seconds", "clock_nanosleep"], 260))
see("POSIX, 4.19 Seconds Since the Epoch: the expression", lambda: wp("https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html", ["tm_sec + tm_min*60 + tm_hour*3600", "If the year is <1970 or the value is negative, the relationship is undefined"], 220))
see("Debian crontab(5): the environment variables cron sets up", lambda: wp("https://manpages.debian.org/bookworm/cron/crontab.5.en.html", ["Several environment variables are set up automatically by the cron(8) daemon"], 400))

# 4. Python and the tools
py = get("https://docs.python.org/3.14/library/time.html", headers=UA)
see("Python documentation of time: the release the page describes", lambda: re.search(r"(3\.\d+\.\d+) documentation", visible(py), re.I).group(1))
pyd = get("https://www.python.org/downloads/", headers=UA)
see("python.org downloads page: the newest release it offers and the list of releases with their dates", lambda: [re.findall(r"Download Python (3\.\d+\.\d+)", visible(pyd))[:2], re.findall(r"Python (3\.1[345]\.\d+) ([A-Z][a-z]+\.? \d+, \d{4})", visible(pyd))[:8]])
def uvlist():
    r = subprocess.run(["uv", "python", "list", "--all-versions"], capture_output=True, text=True)
    return sorted({m for m in re.findall(r"cpython-(3\.1[45]\.\d+[a-z0-9]*)-linux-x86_64-gnu", r.stdout)}, key=lambda s: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s)])
see("uv (python list --all-versions): the 3.14 and 3.15 releases of CPython for this machine that uv knew on the day", uvlist)

# 5. the machine and its own scheduler
def run(cmd, **k):
    r = subprocess.run(cmd, capture_output=True, text=True, **k); return [r.returncode, r.stdout.strip()[:600], r.stderr.strip()[:400]]
see("the machine: operating system, kernel, the zone of the shell (TZ), the zone of the system (/etc/localtime), the clock and the version of the system tz database", lambda: [run(["uname", "-sr"])[1], os.environ.get("TZ"), os.path.realpath("/etc/localtime"), time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime()), open("/usr/share/zoneinfo/tzdata.zi").readline().strip(), run(["dpkg-query", "-W", "-f", "${Package} ${Version}", "tzdata"])[1], run(["dpkg-query", "-W", "-f", "${Package} ${Version}", "cron"])[1]])
see("which program is `open`: the path, what it resolves to, the package whose post-install script registers the alternative, and what it does for a missing file", lambda: [shutil.which("open"), os.path.realpath(shutil.which("open") or ""), run(["sh", "-c", "grep -l 'update-alternatives.*open' /var/lib/dpkg/info/*.postinst"])[1], run(["dpkg", "-S", "/usr/bin/xdg-open"])[1], run(["open", "/nonexistent-file"])[:3]])
see("the Windows commands on this machine: schtasks, launchctl, start and calc.exe are looked for on PATH (None means absent)", lambda: {n: shutil.which(n) for n in ("schtasks", "launchctl", "start", "calc.exe", "gnome-calculator", "notepad", "xclip", "xsel", "wl-copy", "xdg-open", "open", "systemd-analyze", "crontab", "cron", "anacron", "at")})
see("ping with the Windows flag (-n 4) and the Linux flag (-c 2), and the book's host: exit code and the summary line", lambda: [run(["ping", "-n", "4", "localhost"], timeout=60), run(["ping", "-c", "2", "-W", "3", "127.0.0.1"], timeout=60)[:2], [l for l in run(["ping", "-c", "2", "-W", "3", "nostarch.com"], timeout=60)[1].splitlines() if "packets" in l or "PING" in l]])
see("systemd: process 1, systemctl list-timers, and systemd-analyze calendar on the OnCalendar expression 'Mon..Fri 09:00'", lambda: [open("/proc/1/comm").read().strip(), run(["systemctl", "list-timers"])[:3], run(["systemd-analyze", "calendar", "Mon..Fri 09:00", "--iterations=3"], env=dict(os.environ, TZ="Europe/Istanbul"))[1], run(["systemd-analyze", "calendar", "*-*-* 04:00:00", "--iterations=2"], env=dict(os.environ, TZ="UTC"))[1]])
def plist():
    import plistlib
    d = {"Label": "org.example.backup", "ProgramArguments": ["/usr/bin/python3", "/Users/al/backup.py"], "StartCalendarInterval": {"Hour": 4, "Minute": 0}, "RunAtLoad": False}
    b = plistlib.dumps(d); back = plistlib.loads(b)
    return [b.decode().splitlines()[:3], back == d, len(b), shutil.which("plutil"), shutil.which("launchctl")]
see("launchd: a property list for a job at 04:00 every day written with plistlib (the head of the XML, whether it reads back equal, its size), and whether plutil or launchctl is on this machine", plist)

# 5a. cron, for real
JOB = r'''import os, sys, time, datetime, json
rec = {"label": sys.argv[1], "epoch": time.time(), "local": datetime.datetime.now().isoformat(timespec="seconds"), "utc": datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds"),
       "PATH": os.environ.get("PATH"), "TZ": os.environ.get("TZ"), "CRON_TZ": os.environ.get("CRON_TZ"), "HOME": os.environ.get("HOME"), "SHELL": os.environ.get("SHELL"), "LOGNAME": os.environ.get("LOGNAME"),
       "cwd": os.getcwd(), "has_terminal": sys.stdin.isatty(), "environment variables": len(os.environ), "parent": open("/proc/%d/comm" % os.getppid()).read().strip(), "tzname": list(time.tzname)}
with open(sys.argv[2], "a") as f: f.write(json.dumps(rec) + "\n")
'''
def cron_zone():
    """the TZ in the environment of the running cron daemon (None when it has none)"""
    pids = subprocess.run(["pgrep", "-x", "cron"], capture_output=True, text=True).stdout.split()
    if not pids: return "not running"
    for kv in open("/proc/%s/environ" % pids[0], "rb").read().split(b"\0"):
        if kv.startswith(b"TZ="): return kv[3:].decode()
    return None
def cron_start(tz=None):
    """(re)starts the cron daemon with TZ=tz in its environment (no TZ when None); the zone of the daemon, not of the job, decides when entries run"""
    if cron_zone() != "not running" and cron_zone() == tz: return subprocess.run(["pgrep", "-x", "cron"], capture_output=True, text=True).stdout.split()
    subprocess.run(["pkill", "-x", "cron"]); time.sleep(1)
    env = {k: v for k, v in os.environ.items() if k != "TZ"}
    if tz: env["TZ"] = tz
    subprocess.run(["/usr/sbin/cron"], env=env); time.sleep(2)
    return subprocess.run(["pgrep", "-x", "cron"], capture_output=True, text=True).stdout.split()
def cron_alive():
    return cron_start(None)
def cron_experiment(tab_lines, outfile, wait, want):
    """installs a crontab, waits until `want` job records are in outfile or `wait` seconds are over, removes the crontab, returns the records"""
    if cron_zone() == "not running": cron_start(None)
    open(outfile, "w").close(); t = tempfile.mktemp(); open(t, "w").write("\n".join(tab_lines) + "\n")
    inst = subprocess.run(["crontab", t], capture_output=True, text=True); end = time.time() + wait; recs = []
    while time.time() < end:
        recs = [json.loads(l) for l in open(outfile).read().splitlines() if l]
        if len(recs) >= want: break
        time.sleep(2)
    subprocess.run(["crontab", "-r"], capture_output=True)
    return inst.returncode, recs
job = os.path.join(WORK, "job.py"); open(job, "w").write(JOB)
def cron_basic():
    out = os.path.join(WORK, "cron1.jsonl"); started = time.time()
    rc, recs = cron_experiment(["* * * * * %s %s every_minute %s" % (PYTHON, job, out)], out, 130, 1)
    r = recs[0] if recs else None
    return {"cron daemon pids": cron_alive(), "crontab install exit code": rc, "seconds from install to first record": round(r["epoch"] - started, 1) if r else None,
            "second of the minute when the job started (cron starts jobs at the turn of the minute)": round(r["epoch"] % 60, 1) if r else None, "record": r,
            "the clock of the shell at the same moment (TZ in this shell)": time.strftime("%H:%M:%S %Z", time.localtime(r["epoch"])) if r else None,
            "the job saw local time equal to UTC (the system zone) and not the shell's zone": (r["local"][:16] == r["utc"][:16]) if r else None}
see("cron, for real: a crontab with the entry '* * * * *' runs a Python program once at the turn of the minute; what the program saw (its clock, environment variables, working directory, terminal, parent)", cron_basic)
def cron_tz_line():
    out = os.path.join(WORK, "cron2.jsonl")
    rc, recs = cron_experiment(["TZ=Asia/Kolkata", "* * * * * %s %s with_TZ_line %s" % (PYTHON, job, out)], out, 130, 1)
    return {"install exit code": rc, "record": recs[0] if recs else None}
see("cron, for real: a crontab with the line TZ=Asia/Kolkata above the entry (the line sets an environment variable of the job)", cron_tz_line)
def cron_cron_tz():
    out = os.path.join(WORK, "cron3.jsonl")
    now = datetime.datetime.now(datetime.UTC).replace(second=0, microsecond=0) + datetime.timedelta(minutes=3)
    kol = now + datetime.timedelta(hours=5, minutes=30)
    tab = ["CRON_TZ=Asia/Kolkata", "%d %d * * * %s %s kolkata_entry %s" % (kol.minute, kol.hour, PYTHON, job, out), "CRON_TZ=UTC", "%d %d * * * %s %s utc_entry %s" % (now.minute, now.hour, PYTHON, job, out)]
    rc, recs = cron_experiment(tab, out, 235, 2)
    return {"target moment UTC": now.isoformat(), "the same moment on the clock of Kolkata (UTC+05:30)": kol.strftime("%H:%M"), "install exit code": rc, "crontab": tab[0::1][:4],
            "entries that fired within 235 s": [[r["label"], r["utc"], r["CRON_TZ"], r["TZ"]] for r in recs], "labels that fired": sorted(r["label"] for r in recs), "the entry written on the UTC clock fired and the entry written on the Kolkata clock did not (CRON_TZ not used for the schedule)": sorted(r["label"] for r in recs) == ["utc_entry"], "daemon TZ": cron_zone()}
see("cron, for real: two entries for the same moment, one written on the clock of Kolkata under CRON_TZ=Asia/Kolkata and one on UTC under CRON_TZ=UTC; which of them fired", cron_cron_tz)
def cron_daemon_zone():
    out = os.path.join(WORK, "cron4.jsonl")
    cron_start("Europe/Istanbul")
    try:
        now = datetime.datetime.now(datetime.UTC).replace(second=0, microsecond=0) + datetime.timedelta(minutes=3)
        ist = now + datetime.timedelta(hours=3)
        tab = ["%d %d * * * %s %s utc_clock_entry %s" % (now.minute, now.hour, PYTHON, job, out), "%d %d * * * %s %s istanbul_clock_entry %s" % (ist.minute, ist.hour, PYTHON, job, out)]
        rc, recs = cron_experiment(tab, out, 235, 2)
        z = cron_zone()
    finally:
        cron_start(None)
    return {"zone in the environment of the daemon": z, "target moment UTC": now.isoformat(), "the same moment on the clock of Istanbul (UTC+03:00)": ist.strftime("%H:%M"), "install exit code": rc,
            "labels that fired": sorted(r["label"] for r in recs), "the entry written on the daemon's clock fired and the entry written on the UTC clock did not": sorted(r["label"] for r in recs) == ["istanbul_clock_entry"],
            "zone the job itself saw (TZ in its environment, local time minus UTC)": [[r["TZ"], r["local"][11:16], r["utc"][11:16]] for r in recs]}
see("cron, for real: with the daemon started in a shell whose TZ is Europe/Istanbul, two entries for the same moment, one on the UTC clock and one on the Istanbul clock; which of them fired (the zone of the daemon decides, the job does not inherit it)", cron_daemon_zone)
def cron_bad():
    t = tempfile.mktemp(); open(t, "w").write("61 * * * * /bin/true\n")
    r = subprocess.run(["crontab", t], capture_output=True, text=True); subprocess.run(["crontab", "-r"], capture_output=True)
    return [r.returncode, r.stderr.strip()[:200]]
see("cron, for real: a crontab with a minute of 61 is refused by the crontab command (exit code and message)", cron_bad)
see("cron: left over after the experiments (the crontab of the user is removed; None means no crontab)", lambda: run(["crontab", "-l"])[:3])

see("every source of the research record opened: id, HTTP status, bytes, and whether each passage the research relies on is on the page", sources)
json.dump({"_version": "1.0.0", "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s" % (requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names, and the experiments of the operating system's own tools on the build machine (an Ubuntu 24.04 container in the zone Europe/Istanbul whose system zone is UTC). Windows, macOS, Task Scheduler and launchd were not used. A record of one observation; web sites change and nothing re-checks it.",
           "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print("observed", len(obs), "things on", datetime.date.today())
