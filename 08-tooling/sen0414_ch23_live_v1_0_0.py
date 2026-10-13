#!/usr/bin/env python3
"""Chapter 23 (Controlling the Keyboard and Mouse): observes, once, what the public sources the chapter names answer today, what the files the book ships hold, what the package index
says about PyAutoGUI and the packages it installs, and which tools of the machine the research programs use, and writes what it saw with the date. A web site changes and the files of the
online materials may be replaced; the record is an observation of the day, not something the build can re-check, and no check reads it.
What it does: fetches the chapter page and compares its SHA-256 with the digest the book's own ontology records; counts what is on the page (listings, figures, practice questions), asks
every external link of the chapter once without following a redirect, and asks for each picture of the chapter; reads Appendix A for the packages the book pins and Appendix B for the
answers to the chapter's thirteen questions; downloads the online materials of the 3rd edition and compares the shipped spiralDraw.py with the chapter's listing; reads the newest releases of
PyAutoGUI, PyScreeze, PyMsgBox, PyTweening, PyGetWindow, MouseInfo, Pyperclip, Pillow, python3-xlib and OpenCV on PyPI and every release of PyAutoGUI and PyScreeze; opens every source of the
research record and checks that the passages the research relies on are on the page (and that one passage that should be gone is gone).
On the machine itself it asks which tools the research programs use (Xvfb, openbox, xdotool, xev, xterm, scrot, xclip, xsel, xprintidle) for their versions.
NOT EXECUTED and said so: Windows and macOS, a real screen, a photograph from Wikimedia Commons (the one request made by hand on 2026-10-13 answered 429 and was not repeated).
Run it with an interpreter that has requests and Beautiful Soup (/home/claude/venv314_web/bin/python).
Usage: sen0414_ch23_live_v1_0_0.py   -> ch23-page/live_observations_v1_0_0.json"""
__version__ = "1.0.0"
import datetime, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time, zipfile
import requests, bs4
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "08-tooling", "ch23-page", "live_observations_v1_0_0.json")
UA = {"User-Agent": "SEN0414-research/1.0 (academic course; altunel.yusuf@gmail.com)"}
BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"}
PYTHON = os.environ.get("CH23_LATEST", "/home/claude/venv314_ch23_latest/bin/python")
obs = []
def see(what, f):
    try: v = f()
    except Exception as e: v = "raised %s: %s" % (type(e).__name__, str(e)[:200])
    obs.append({"what": what, "saw": v})
def get(u, **k):
    k.setdefault("headers", UA)
    for attempt in range(6):       # a site that answers 429 or drops the connection is asked again after a pause; the status of the last answer is the one recorded
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
    s = bs4.BeautifulSoup(r.content.decode("utf-8", "replace"), "html.parser")
    for x in s(["script", "style"]): x.decompose()
    return norm(s.get_text(" "))
# (id, label, url, primary, phrases found on the page)
SOURCES = [
 ('P01', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 23, Controlling the Keyboard and Mouse (Al Sweigart, No Starch Press, 2025)', 'https://automatetheboringstuff.com/3e/chapter23.html', True,
  ['graphical user interface automation', 'FailSafeException', 'pyautogui.moveTo()', 'Win32Window', 'getWindowsWithTitle', 'useImageNotFoundException', 'Reading Text Fields with the Clipboard', 'Writing a Game-Playing Bot', 'Looking Busy', 'CAPTCHAS AND COMPUTER ETHICS', 'In versions of PyAutoGUI before 1.0.0', 'As of version 1.0.0', 'one-tenth-of-a-second pause', 'CTRL-ALT-DEL', 'KEYBOARD_KEYS', 'Accessibility Apps on macOS']),
 ('P02', 'Online materials of the 3rd edition, zip with 91 files, one of them spiralDraw.py of chapter 23 (No Starch Press, 2025)', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', False, []),
 ('P03', 'Automate the Boring Stuff with Python, 3rd edition - table of contents (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/', False, ['Controlling the Keyboard and Mouse']),
 ('P04', 'Automate the Boring Stuff with Python, 3rd edition - book page (No Starch Press, 2025)', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', False, ['Controlling the Keyboard and Mouse']),
 ('P05', 'Appendix A, Installing Third-Party Packages (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixa.html', False, ['pyautogui', 'python3-tk', 'python3-dev', 'xclip', 'automateboringstuff3', 'pillow==10.4.0']),
 ('P06', 'Appendix B, Answers to the Practice Questions (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixb.html', False, ["pyautogui.typewrite('Hello world!')", 'pyautogui.screenshot(', 'pyautogui.PAUSE = 2', 'pyatuogui.getWindowsWithTitle', 'Selenium for controlling a web browser']),
 ('P07', 'PyAutoGUI documentation, home page with the FAQ and the fail-safes (PyAutoGUI documentation, 2026)', 'https://pyautogui.readthedocs.io/en/latest/', False, ['PyAutoGUI works on Windows, macOS, and Linux', 'right now PyAutoGUI only handles the primary monitor', 'one-tenth second delay', 'pyautogui.FAILSAFE = False', 'DARWIN_CATCH_UP_TIME', 'Windows-only, currently', 'PyAutoGUI cannot do this currently']),
 ('P08', 'PyAutoGUI documentation, cheat sheet (PyAutoGUI documentation, 2026)', 'https://pyautogui.readthedocs.io/en/latest/quickstart.html', False, ['PAUSE = 2.5', 'FAILSAFE', 'hotkey', 'Fail-Safes']),
 ('P09', 'PyAutoGUI documentation, mouse control functions (PyAutoGUI documentation, 2026)', 'https://pyautogui.readthedocs.io/en/latest/mouse.html', False, ['tween', 'mouseDown', 'scroll', 'hscroll', 'clicks']),
 ('P10', 'PyAutoGUI documentation, keyboard control functions (PyAutoGUI documentation, 2026)', 'https://pyautogui.readthedocs.io/en/latest/keyboard.html', False, ['KEYBOARD_KEYS', 'hold', 'hotkey', 'interval', 'printscreen', 'volumemute']),
 ('P11', 'PyAutoGUI documentation, screenshot functions (PyAutoGUI documentation, 2026)', 'https://pyautogui.readthedocs.io/en/latest/screenshot.html', False, ['As of version 0.9.41', 'ImageNotFoundException', 'confidence keyword', 'OpenCV', 'grayscale=True', 'scrot', 'tolerance']),
 ('P12', 'PyAutoGUI documentation, message box functions (PyAutoGUI documentation, 2026)', 'https://pyautogui.readthedocs.io/en/latest/msgbox.html', False, ['alert', 'confirm', 'prompt', 'password', "mask = '*'", 'PyMsgBox']),
 ('P13', 'PyAutoGUI documentation, installation (PyAutoGUI documentation, 2026)', 'https://pyautogui.readthedocs.io/en/latest/install.html', False, ['scrot', 'python3-tk', 'python3-dev', 'PyScreeze', 'MouseInfo']),
 ('P14', 'PyAutoGUI documentation, roadmap (PyAutoGUI documentation, 2026)', 'https://pyautogui.readthedocs.io/en/latest/roadmap.html', False, ['strict', 'silently skipping it', 'multiple monitors', 'global hotkey', 'kill switch']),
 ('P15', 'PyAutoGUI README on GitHub (PyAutoGUI documentation, 2026)', 'https://raw.githubusercontent.com/asweigart/pyautogui/master/README.md', False, ['PyAutoGUI', 'pyautogui.write', 'pyautogui.hotkey']),
 ('P16', 'PyAutoGUI on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/pyautogui/json', False, ['0.9.54', 'pyscreeze', 'python3-xlib']),
 ('P17', 'PyScreeze on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/pyscreeze/json', False, ['1.0.1', '0.1.28', '0.1.30', 'pillow']),
 ('P18', 'PyScreeze README on GitHub (PyScreeze documentation, 2026)', 'https://raw.githubusercontent.com/asweigart/pyscreeze/master/README.md', False, ['locateOnScreen', 'gnome-screenshot', 'python3-xlib', 'grayscale', 'tolerance']),
 ('P19', 'PyMsgBox documentation (PyMsgBox documentation, 2026)', 'https://pymsgbox.readthedocs.io/en/latest/', False, ['Timeout', 'Localization', 'Native Message Boxes']),
 ('P20', 'PyMsgBox on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/pymsgbox/json', False, ['2.0.1', '1.0.9', 'tkinter']),
 ('P21', 'PyTweening on the Python Package Index (Python Package Index, 2026)', 'https://pypi.org/pypi/pytweening/json', False, ['1.2.0', 'easing']),
 ('P22', 'PyTweening README on GitHub (PyTweening documentation, 2026)', 'https://raw.githubusercontent.com/asweigart/pytweening/master/README.md', False, ['easeInOutQuad', 'linear', 'getPointOnLine']),
 ('P23', 'PyGetWindow README on GitHub (PyGetWindow documentation, 2026)', 'https://raw.githubusercontent.com/asweigart/PyGetWindow/master/README.md', False, ['Windows', 'getActiveWindow', 'getWindowsWithTitle', 'maximize']),
 ('P24', 'MouseInfo documentation (MouseInfo documentation, 2026)', 'https://mouseinfo.readthedocs.io/en/latest/', False, ['3 Sec. Button Delay', 'Copy XY', 'Log XY', 'F1 through F8', 'XY Origin', 'mouseInfoLog.txt']),
 ('P25', 'Pyperclip documentation (Pyperclip documentation, 2026)', 'https://pyperclip.readthedocs.io/en/latest/', False, ['pyperclip.copy()', 'pyperclip.paste()', 'waitForPaste', 'xclip', 'xsel']),
 ('P26', 'Pyperclip README on GitHub (Pyperclip documentation, 2026)', 'https://raw.githubusercontent.com/asweigart/pyperclip/master/README.md', False, ['pyperclip']),
 ('P27', 'tkinter - Python interface to Tcl/Tk, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/tkinter.html', False, ['Tcl/Tk', 'send_event', 'MouseWheel', 'Tk 9']),
 ('P28', 'time - Time access and conversions, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/time.html', False, ['time.sleep', 'perf_counter', 'monotonic']),
 ('P29', 'logging - Logging facility for Python, Python 3.14 documentation (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/logging.html', False, ['basicConfig', 'FileHandler', 'logging.info']),
 ('P30', 'What is new in Python 3.14 (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/whatsnew/3.14.html', False, ['Python 3.14', 'free-threaded']),
 ('P31', 'The XTEST Extension Protocol (X.Org Foundation, 2026)', 'https://www.x.org/releases/X11R7.7/doc/xextproto/xtest.html', False, ['XTestFakeInput', 'XTestGrabControl', 'XTestCompareCursor']),
 ('P32', 'Xlib - C Language X Interface, the event structures (X.Org Foundation, 2026)', 'https://www.x.org/releases/current/doc/libX11/libX11/libX11.html', False, ['send_event', 'true if this came from a SendEvent request', 'XSendEvent']),
 ('P33', 'SendInput function, Win32 apps (Microsoft Learn, 2026)', 'https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput', False, ['Synthesizes keystrokes, mouse motions, and button clicks', 'This function is subject to UIPI', 'integrity level', 'inserts the events in the INPUT structures serially']),
 ('P34', 'INPUT structure, Win32 apps (Microsoft Learn, 2026)', 'https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input', False, ['INPUT_MOUSE', 'INPUT_KEYBOARD', 'MOUSEINPUT', 'KEYBDINPUT']),
 ('P35', 'mouse_event function, Win32 apps (Microsoft Learn, 2026)', 'https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event', False, ['superseded', 'SendInput', 'MOUSEEVENTF_ABSOLUTE']),
 ('P36', 'Allow accessibility apps to access your Mac (Apple Support, 2026)', 'https://support.apple.com/guide/mac-help/allow-accessibility-apps-to-access-your-mac-mh43185/mac', False, ['Accessibility', 'Privacy', 'Security']),
 ('P37', 'Mac keyboard shortcuts (Apple Support, 2026)', 'https://support.apple.com/en-us/102650', False, ['Shift-Command-Q', 'Log out of your macOS user account', 'Option-Shift-Command-Q', 'Control-Command-Q']),
 ('P38', 'Remote Desktop portal, XDG Desktop Portal documentation (Freedesktop, 2026)', 'https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.RemoteDesktop.html', False, ['NotifyPointerMotion', 'NotifyKeyboardKeycode', 'SelectDevices', 'CreateSession']),
 ('P39', 'The Wayland Protocol, the book (Freedesktop, 2026)', 'https://wayland.freedesktop.org/docs/book/Protocol.html', False, ['wl_seat', 'compositor']),
 ('P40', 'trace, Tcl 9.0 manual (Tcl Developer Exchange, 2026)', 'https://www.tcl-lang.org/man/tcl9.0/TclCmd/trace.html', False, ['trace add variable', 'trace remove variable', 'trace info variable']),
 ('P41', 'Xvfb manual page (X.Org Foundation, 2026)', 'https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml', False, ['virtual framebuffer', '-screen', 'depth']),
 ('P42', 'xterm manual page, the allowSendEvents resource (Dickey, 2026)', 'https://invisible-island.net/xterm/manpage/xterm.html', False, ['allowSendEvents', 'synthetic key and button events', 'should be interpreted or discarded']),
 ('P43', 'sushigoroundbot README on GitHub (Sweigart, 2026)', 'https://raw.githubusercontent.com/asweigart/sushigoroundbot/master/README.md', False, ['Sushi Go Round', 'bot']),
 ('P44', 'Robotic process automation (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Robotic_process_automation', False, ['Robotic process automation', 'screen scraping', 'software robots']),
 ('P45', 'CAPTCHA (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/CAPTCHA', False, ['Completely Automated Public Turing test to tell Computers and Humans Apart', 'spam', 'accessibility']),
 ('P46', 'Graphical user interface testing (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Graphical_user_interface_testing', False, ['GUI testing', 'automation']),
 ('P47', 'ImageGrab module, Pillow reference (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html', False, ['grab', 'xdisplay', 'Wayland', 'macOS']),
 ('P48', 'The Screen Saver Extension Protocol (X.Org Foundation, 2026)', 'https://www.x.org/releases/X11R7.7/doc/scrnsaverproto/saver.html', False, ['ScreenSaverQueryInfo', 'idle', 'ms-since-user-input']),
 ('P49', 'High DPI desktop application development on Windows (Microsoft Learn, 2026)', 'https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows', False, ['DPI', 'per-monitor', 'scaling']),
 ('P50', 'Template Matching, OpenCV tutorial (OpenCV documentation, 2026)', 'https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html', False, ['cv.matchTemplate', 'TM_CCOEFF', 'minMaxLoc']),
 ('P51', 'WebDriver, Selenium documentation (Selenium documentation, 2026)', 'https://www.selenium.dev/documentation/webdriver/', False, ['WebDriver', 'browser']),
 ('P52', 'Installation, Playwright for Python documentation (Playwright documentation, 2026)', 'https://playwright.dev/python/docs/intro', False, ['Playwright', 'pip install', 'browsers']),
 ('P53', 'Keyboard shortcuts in Windows (Microsoft Support, 2026)', 'https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec', False, ['Ctrl+Alt+Del', 'security screen']),
 ('P54', 'uv - Python versions (Astral documentation, 2026)', 'https://docs.astral.sh/uv/concepts/python-versions/', False, ['uv python install', 'uv python list']),
 ('P55', 'Download Python (Python Software Foundation, 2026)', 'https://www.python.org/downloads/', False, ['Python 3.14', 'Download']),
 ('P56', 'xdotool (Sissel, 2026)', 'https://www.semicomplete.com/projects/xdotool/', False, ['xdotool', 'keyboard input', 'mouse']),
]
def sources():
    out = []
    for pid, label, url, prim, phrases in SOURCES:
        try:
            r = get(url, headers=BROWSER if "nostarch.com" in url else UA); ctype = r.headers.get("content-type", "")
            if "zip" in ctype or url.endswith((".zip", ".pdf")): t = ""
            else:
                t = r.content.decode("utf-8", "replace")
                if "html" in ctype:
                    s = bs4.BeautifulSoup(t, "html.parser")
                    for x in s(["script", "style"]): x.decompose()
                    t = s.get_text(" ")
            t = norm(t).replace("’", "'")
            out.append([pid, r.status_code, len(r.content), {p: (norm(p).replace("’", "'").lower() in t.lower()) for p in phrases}])
        except Exception as e: out.append([pid, "unreachable: %s" % type(e).__name__, 0, {}])
    return out
# 0. the chapter and the book's own record of it
ch = get("https://automatetheboringstuff.com/3e/chapter23.html")
DIGEST = "7b31e4333cd9784edea41303bf20b13b6a091198a43450542881eb3715f71fd7"
ONTO = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies/automate_python_3e_ch23_v1_0_0.ttl"
see("chapter 23 page: status, bytes, SHA-256, equal to the chapterDigest of the book ontology (read from its file when present)", lambda: [ch.status_code, len(ch.content), sha(ch.content), sha(ch.content) == DIGEST, (DIGEST in open(ONTO).read()) if os.path.exists(ONTO) else "ontology file not present"])
soup = bs4.BeautifulSoup(ch.content.decode("utf-8"), "html.parser"); text = norm(soup.get_text(" "))
IMGS = [i["src"] for i in soup.find_all("img") if i.get("src") and "cover" not in i["src"]]
def image_dims():
    d = tempfile.mkdtemp(); rows = []
    for k, src in enumerate(IMGS):
        r = get("https://automatetheboringstuff.com/3e/" + src); p = os.path.join(d, "i%d.img" % k); open(p, "wb").write(r.content); rows.append([src, r.status_code, len(r.content)])
    code = "import sys, json; from PIL import Image; print(json.dumps([list(Image.open(p).size) for p in sys.argv[1:]]))"
    sizes = json.loads(subprocess.run([PYTHON, "-c", code] + [os.path.join(d, "i%d.img" % k) for k in range(len(IMGS))], capture_output=True, text=True).stdout)
    shutil.rmtree(d); return [r + [s] for r, s in zip(rows, sizes)]
see("chapter 23 page: number of listings (pre elements), figure captions, tables, and the HTTP status, bytes and pixel size of each picture of the chapter (the pictures are asked for and measured, not kept)", lambda: [len(soup.find_all("pre")), sorted(set(re.findall(r"Figure 23-\d+", text))), sorted(set(re.findall(r"Table 23-\d+", text))), len(soup.find_all("table")), image_dims()])
see("chapter 23 page: the headings of the chapter in order", lambda: [(h.name, norm(h.get_text())) for h in soup.find_all(["h2", "h3", "h4", "h5"])])
STATEMENTS = ("graphical user interface automation", "robotic process automation", "Don't save your programs as pyautogui.py", "macOS doesn't normally let programs control the mouse or keyboard", "one-tenth-of-a-second pause after performing its action",
              "Non-PyAutoGUI instructions won't have this pause", "On Windows and Linux, the logout hotkey is CTRL-ALT-DEL", "The origin , where x and y are both zero, is at the upper-left corner of the screen", "The size of a unit varies for each operating system and application",
              "A full “click” is defined as pushing a mouse button down and then releasing it", "pyautogui.mouseInfo() function is meant to be called from the interactive shell", "In versions of PyAutoGUI before 1.0.0, locateOnScreen() would return None instead of raising an exception",
              "As of version 1.0.0, PyAutoGUI's window features work only on Windows", "The 'shift' string refers to the left SHIFT key", "presses them in order, and releases them in the reverse order", "Use the same screen resolution each time you run the script",
              "Use the logging module from Chapter 5", "PyAutoGUI includes the PyMsgBox module", "Mu Editor", "you can't use PyAutoGUI alone to read the text already inside a text field", "Flash is discontinued as a product", "Completely Automated Public Turing test to tell Computers and Humans Apart")
see("chapter 23 page: statements the research relies on (each is on the page of the book: True)", lambda: {s: (norm(s).replace("’", "'").lower() in text.replace("’", "'").lower()) for s in STATEMENTS})
see("chapter 23 page: words the chapter never uses although the topic needs them (False means absent from the page)", lambda: {s: s.lower() in text.lower() for s in ("Wayland", "XTEST", "SendInput", "Quartz", "hold(", "hscroll", "tripleClick", "multi-monitor", "multiple monitors", "HiDPI", "DPI", "scrot", "tkinter", "xclip", "confidence", "OpenCV", "grayscale", "region", "minSearchTime", "FAILSAFE", "FAILSAFE_POINTS", "DARWIN_CATCH_UP_TIME", "typewrite", "dragRel", "pixelMatchesColor", "tolerance", "silently", "invalid key", "KeyboardInterrupt", "idle", "xdotool", "UIPI", "permission")})
ext = sorted({a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("http") and "automatetheboringstuff.com" not in a["href"]})
def link_status():
    out = []
    for u in ext:
        try:
            r = requests.get(u, timeout=60, headers=BROWSER, allow_redirects=False); out.append([u, r.status_code, r.headers.get("Location", "")[:100]])
        except Exception as e: out.append([u, "unreachable: %s" % type(e).__name__, ""])
    return out
see("chapter 23 page: every external link of the chapter, asked once without following a redirect: URL, HTTP status, Location", link_status)
see("chapter 23 page: every URL that appears in the text of the chapter", lambda: sorted({u.rstrip(".,)") for u in re.findall(r"https?://\s?[\w./?=&#%~:+ -]+", text) if "automatetheboringstuff.com/3e/chapter23" not in u})[:20])
def appendix():
    a = get("https://automatetheboringstuff.com/3e/appendixa.html"); t = visible(a)
    return [a.status_code, "pyautogui" in t.lower(), re.findall(r"In addition, the automateboringstuff3 package always installs[^.]{0,200}\.", t)[:1], re.findall(r"To install Chapter 23 ’s PyAutoGUI package on Linux[^.]{0,200}\.", t)[:1], "pyautogui==" in t, re.findall(r"pillow\s*==\s*[\d.]+", t)[:2]]
see("Appendix A of the book: status, whether PyAutoGUI is named and pinned, the sentences about Linux and about the packages that are always installed at the newest version", appendix)
def appendixb():
    a = get("https://automatetheboringstuff.com/3e/appendixb.html"); t = visible(a)
    i = t.find("Chapter 23 1."); j = t.find("Chapter 24", i)
    return [a.status_code, t[i:j][:1800]]
see("Appendix B of the book: the answers printed for the thirteen questions of chapter 23", appendixb)
def bookpage():
    r = get("https://nostarch.com/automate-boring-stuff-python-3rd-edition", headers=BROWSER); t = visible(r)
    return [r.status_code, len(r.content), {w: len(re.findall(w, t, re.I)) for w in ("Controlling the Keyboard and Mouse", "PyAutoGUI", "GUI automation")}]
see("the book page at nostarch.com: how often words occur on the page", bookpage)
mat = get("https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip", headers=BROWSER)
see("online materials of the 3rd edition: status, bytes, SHA-256 of the zip", lambda: [mat.status_code, len(mat.content), sha(mat.content)])
def materials():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); names = [n for n in z.namelist() if not n.endswith("/") and "__MACOSX" not in n and not n.split("/")[-1].startswith("._")]
    base = {n.split("/")[-1]: n for n in names}; texts = {n.split("/")[-1]: z.read(n).decode("utf-8", "replace") for n in names if n.endswith(".py")}
    hits = lambda pat: sorted(k for k, v in texts.items() if re.search(pat, v))
    return {"files": len(names), "python files": len(texts), "python files that import pyautogui": hits(r"import pyautogui|import .*pyautogui"), "python files that import pyperclip": hits(r"pyperclip"),
            "spiralDraw.py in the zip": "spiralDraw.py" in base, "files the chapter names that the zip does not hold": [n for n in ("pyautogui.py", "submit.png", "screenshot.png", "mouseInfoLog.txt") if n not in base]}
see("online materials: the files, and which of them use PyAutoGUI or Pyperclip", materials)
def shipped_spiral():
    z = zipfile.ZipFile(io.BytesIO(mat.content)); n = [x for x in z.namelist() if x.endswith("/spiralDraw.py") and "__MACOSX" not in x][0]; s = z.read(n).decode()
    listing = [norm(html_text) for html_text in [soup.find_all("pre")[5].get_text()]][0]
    return {"bytes": len(s.encode()), "lines": len(s.splitlines()), "sha256": sha(s.encode()), "calls dragRel (the book's listing calls drag)": "dragRel" in s, "the book's listing calls pyautogui.drag(": "pyautogui.drag(" in listing, "has the pause pyautogui.sleep(5)": "sleep(5)" in s,
            "uses time.sleep(5) and imports time": "time.sleep(5)" in s, "sets LOG_SCREENSHOTS (not in the listing)": "LOG_SCREENSHOTS" in s and "LOG_SCREENSHOTS" not in listing, "variable that shrinks the distance": "shrink" in s, "duration in the file, in the listing": [re.findall(r"duration=([\d.]+)", s)[:1], re.findall(r"duration=([\d.]+)", listing)[:1]]}
see("online materials: spiralDraw.py as shipped against the listing of the chapter", shipped_spiral)
def pypi():
    out = {}
    for n in ("pyautogui", "pyscreeze", "pymsgbox", "pytweening", "pygetwindow", "mouseinfo", "pyperclip", "pillow", "python3-xlib", "opencv-python-headless", "pyrect"):
        j = get("https://pypi.org/pypi/%s/json" % n).json(); i = j["info"]; rel = j["releases"].get(i["version"], [])
        out[n] = {"version": i["version"], "uploaded": rel[0]["upload_time"][:10] if rel else None, "requires_python": i["requires_python"], "requires_dist": sorted((i["requires_dist"] or []))[:12], "yanked": bool(rel and rel[0].get("yanked"))}
    return out
see("PyPI: the newest release, its upload date, Requires-Python and dependencies of PyAutoGUI and the packages it installs, Pillow, python3-xlib and OpenCV", pypi)
def releases(name):
    j = get("https://pypi.org/pypi/%s/json" % name).json(); rel = j["releases"]
    def ver(v): return [int(x) for x in re.findall(r"\d+", v)[:4]]
    vs = sorted(rel, key=ver)
    return {"releases": len(vs), "newest": vs[-1], "has a release 1.0.0": "1.0.0" in rel, "all": {v: rel[v][0]["upload_time"][:10] for v in vs if rel[v]}}
see("PyPI: every release of PyAutoGUI with its upload date (the chapter speaks of version 1.0.0)", lambda: releases("pyautogui"))
see("PyPI: every release of PyScreeze with its upload date", lambda: releases("pyscreeze"))
see("sources of the research record: for each, the HTTP status, the bytes, and whether each passage the research relies on is on the page", sources)
see("Tcl 9.0 manual of the trace command: does the page still document the old form trace variable (False means it does not)", lambda: "trace variable" in visible(get("https://www.tcl-lang.org/man/tcl9.0/TclCmd/trace.html")).lower())
see("PyGetWindow README: what it says about the platforms", lambda: [l for l in get("https://raw.githubusercontent.com/asweigart/PyGetWindow/master/README.md").text.splitlines() if re.search(r"windows|linux|macos|platform", l, re.I)][:6])
see("sushigoroundbot README (raw): its first 400 characters, and the status of the repository page itself through the proxy", lambda: [get("https://raw.githubusercontent.com/asweigart/sushigoroundbot/master/README.md").text[:400], requests.get("https://github.com/asweigart/sushigoroundbot", headers=BROWSER, timeout=60).status_code])
see("the video the chapter links (youtu.be/lfk_T6VKhTE): HTTP status after the redirect, and the sumopaint.com site the chapter names for drawing", lambda: {u: (lambda r: [r.status_code, r.url[:80]])(requests.get(u, headers=BROWSER, timeout=60)) if u.startswith("https://youtu") else None for u in ["https://youtu.be/lfk_T6VKhTE"]} | {"https://www.sumopaint.com/": (lambda: (requests.get("https://www.sumopaint.com/", headers=BROWSER, timeout=60).status_code))() if False else "not asked again; the first request through the proxy raised SSLError"})
# 1. tools of the machine
def run(cmd, env=None, timeout=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env, stdin=subprocess.DEVNULL); return (r.stdout + r.stderr).strip().splitlines()[0:1]
    except Exception as e: return ["raised %s" % type(e).__name__]
def tools():
    out = {}
    for t in ("Xvfb", "openbox", "xdotool", "xev", "xterm", "scrot", "xclip", "xsel", "xprintidle", "xrandr", "xsetroot", "xdpyinfo", "setxkbmap"):
        out[t] = shutil.which(t)
    for p in ("xvfb", "openbox", "xdotool", "x11-utils", "scrot", "xclip", "xsel", "xterm", "xprintidle", "x11-xserver-utils", "x11-xkb-utils", "python3-tk"):
        out["package " + p] = run(["dpkg-query", "-W", "-f", "${Package} ${Version}", p])
    out["openbox --version"] = run(["openbox", "--version"]); out["xdotool version"] = run(["xdotool", "version"]); out["scrot --version"] = run(["scrot", "--version"]); out["xterm -version"] = run(["xterm", "-version"])
    out["python 3.14 Tk (uv)"] = run([PYTHON, "-c", "import tkinter; print(tkinter.Tcl().eval('info patchlevel'))"]); out["python 3.12 Tk (Ubuntu)"] = run(["/home/claude/venv312_ch23_tk86/bin/python", "-c", "import tkinter; print(tkinter.Tcl().eval('info patchlevel'))"])
    return out
see("tools of the machine the research programs use: where they are and which versions", tools)
see("the photograph: one request to Wikimedia Commons (the imageinfo of one file, with a polite User-Agent) was made by hand on 2026-10-13 and answered HTTP 429; it was not repeated and no photograph is used", lambda: {"status": 429, "repeated": False, "photograph used": False})
json.dump({"_version": __version__, "observed": datetime.date.today().isoformat(), "with": "requests %s, beautifulsoup4 %s, Python %s" % (requests.__version__, bs4.__version__, sys.version.split()[0]),
           "_note": "Single requests made on the day named, through the build machine's proxy, to the public pages and files the chapter names; the PyPI JSON of eleven packages; and the tools of the build machine (Xvfb, openbox, xdotool, xev, xterm, scrot, xclip, xsel, xprintidle). Nothing here controls a real screen; Windows and macOS were not executed.",
           "items": obs}, open(OUT, "w"), indent=1, ensure_ascii=False)
print(len(obs), "observations ->", OUT)
