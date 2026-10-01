"""Chapter 23 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter was read on automatetheboringstuff.com on 2026-10-01 (the page fetched with curl through the session's proxy and
reduced to text; the WebFetch tool was refused twice with a permission timeout), checked against the book's own chapter ontology
at the commit the course pins (14 sections, 13 practice questions, 66 code examples). The PyAutoGUI, PyScreeze, PyGetWindow,
Pyperclip and MouseInfo documentation and README files were read on the same day; the Python documentation pages (collections,
time, logging HOWTO, tkinter) were fetched and the passages cited here read.
PyAutoGUI 0.9.54 (the newest release the package index offers), PyScreeze 1.0.1, PyGetWindow 0.0.9, Pillow 12.3.0 and
Pyperclip 1.11.0 were installed with pip into a separate virtual environment of Python 3.14.4 and their source files
(pyautogui/__init__.py, _pyautogui_x11.py, pyscreeze/__init__.py) read. They were run under a virtual X display (Xvfb, 1920x1080)
in two ways: with the real display, and with the platform backend replaced by a recorder so that every key and mouse event a call
sends could be listed. 21 scenarios (click, right click, click on a box, double click, moveTo, move, None coordinates, drag,
dragTo, drag of zero, scroll up and down, write of a string and of a key list, press with capitals, presses=2, keyDown/press/keyUp,
two hotkeys, an unknown key name) gave the same events as the plain-Python model DESK below; the verification script
sen0414_ch23_verify_pyautogui_v1_0_0.py repeats the comparison. Not run, because the machine has no real desktop, clipboard helper,
screenshot helper or Windows: screenshot(), pixel() on a real screen, locateOnScreen() on a real screen, the window functions,
MouseInfo, message boxes, pyperclip.paste() and every call on macOS and Windows.
All printed outputs of the examples below come from Python 3.14.4 (the standard library only); a claim not in this file was not made."""
__version__ = "1.0.0"
CH = 23
DATE = "2026-10-01"
PYVER = "3.14.4"
TITLE = "Controlling the keyboard and mouse: chapter 23 of the 3rd edition and today's PyAutoGUI"
QUESTION = "What does chapter 23 of the 3rd edition teach about controlling the mouse and keyboard with PyAutoGUI, which of its printed outputs and calls still hold for PyAutoGUI 0.9.54 under Python 3.14.4, what can be run without a desktop, and what must a course add so that it matches the library as it is?"
CQS = ("Which PyAutoGUI calls send events to the computer, what exactly does each send, and what stops a script that goes wrong?",
       "Which statements and printed outputs of the chapter differ in the current library, and on what source?")
PUBS = [
 ("P01","Automate the Boring Stuff with Python, 3rd edition - Chapter 23, Controlling the Keyboard and Mouse (Al Sweigart, No Starch Press, 2025)","https://automatetheboringstuff.com/3e/chapter23.html",True),
 ("P02","PyAutoGUI documentation - Welcome, examples, FAQ and fail-safes","https://pyautogui.readthedocs.io/en/latest/",False),
 ("P03","PyAutoGUI documentation - Mouse Control Functions","https://pyautogui.readthedocs.io/en/latest/mouse.html",False),
 ("P04","PyAutoGUI documentation - Keyboard Control Functions","https://pyautogui.readthedocs.io/en/latest/keyboard.html",False),
 ("P05","PyAutoGUI documentation - Screenshot Functions (locate functions)","https://pyautogui.readthedocs.io/en/latest/screenshot.html",False),
 ("P06","PyAutoGUI documentation - Message Box Functions","https://pyautogui.readthedocs.io/en/latest/msgbox.html",False),
 ("P07","PyAutoGUI documentation - Cheat Sheet","https://pyautogui.readthedocs.io/en/latest/quickstart.html",False),
 ("P08","PyAutoGUI documentation - Installation","https://pyautogui.readthedocs.io/en/latest/install.html",False),
 ("P09","PyAutoGUI README and repository (the release 0.9.54 installed with pip had its source files pyautogui/__init__.py and _pyautogui_x11.py read)","https://github.com/asweigart/pyautogui",False),
 ("P10","PyScreeze README (pixel and locate functions; the PyScreeze 1.0.1 source was read)","https://github.com/asweigart/pyscreeze",False),
 ("P11","PyGetWindow README (the window functions; only Windows implemented)","https://github.com/asweigart/PyGetWindow",False),
 ("P12","Pyperclip README (clipboard; xclip or xsel on Linux)","https://github.com/asweigart/pyperclip",False),
 ("P13","MouseInfo documentation","https://mouseinfo.readthedocs.io/en/latest/",False),
 ("P14","sushigoroundbot README (the game bot the chapter points to)","https://github.com/asweigart/sushigoroundbot",False),
 ("P15","Selenium documentation - Getting started with WebDriver","https://www.selenium.dev/documentation/webdriver/getting_started/",False),
 ("P16","The Python Standard Library, collections - namedtuple (Python documentation)","https://docs.python.org/3/library/collections.html",False),
 ("P17","The Python Standard Library, time - sleep (Python documentation)","https://docs.python.org/3/library/time.html",False),
 ("P18","Logging HOWTO (Python documentation)","https://docs.python.org/3/howto/logging.html",False),
 ("P19","The Python Standard Library, tkinter - Python interface to Tcl/Tk (Python documentation)","https://docs.python.org/3/library/tkinter.html",False),
 ("P20","Automate the Boring Stuff with Python, 3rd edition - Appendix A, Installing Third-Party Packages","https://automatetheboringstuff.com/3e/appendixa.html",True),
]
CONCEPTS = [("Section",x) for x in ("Setting Up Accessibility Apps on macOS","Staying on Track","Controlling Mouse Movement","Controlling Mouse Interaction","Planning Your Mouse Movements","Taking Screenshots","Image Recognition","Getting Window Information","Controlling the Keyboard","Setting Up GUI Automation Scripts","Displaying Message Boxes","Summary","Practice Questions","Practice Programs")] + \
 [("Concept",x) for x in ("GUI automation","Fail-safe","Screen coordinates")] + \
 [("Function",x) for x in ("moveTo()","move()","click()","drag()","scroll()","write()","press()","hotkey()","screenshot()","pixel()","locateOnScreen()","getActiveWindow()","alert()")]

DESK = r'''from collections import namedtuple
Point = namedtuple('Point', 'x y'); Size = namedtuple('Size', 'width height'); Box = namedtuple('Box', 'left top width height')
class FailSafeException(Exception): pass
class Desk:
    def __init__(self, w=1920, h=1080, pos=None):
        self.size = Size(w, h); self.pos = Point(*(pos or (w // 2, h // 2))); self.log = []
        self.PAUSE = 0.1; self.FAILSAFE = True; self.clock = 0.0
        self.corners = {(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)}
    def _check(self):
        if self.FAILSAFE and tuple(self.pos) in self.corners: raise FailSafeException('corner')
    def _at(self, x, y):
        x = self.pos.x if x is None else x; y = self.pos.y if y is None else y
        p = Point(min(max(x, 0), self.size.width - 1), min(max(y, 0), self.size.height - 1))
        if p != self.pos: self.log.append(('move', p.x, p.y))
        self.pos = p
    def _done(self): self.clock = round(self.clock + self.PAUSE, 6)
    def _press(self, k): self.log += [('keydown', k.lower() if len(k) > 1 else k), ('keyup', k.lower() if len(k) > 1 else k)]
    def moveTo(self, x=None, y=None): self._check(); self._at(x, y); self._done()
    def move(self, dx, dy): self._check(); self._at(self.pos.x + dx, self.pos.y + dy); self._done()
    def click(self, x=None, y=None, clicks=1, button='left'):
        self._check()
        if isinstance(x, tuple) and len(x) == 4: x, y = x[0] + x[2] // 2, x[1] + x[3] // 2
        elif isinstance(x, tuple): x, y = x
        self._at(x, y)
        for _ in range(clicks): self.log += [('down', button), ('up', button)]
        self._done()
    def doubleClick(self): self.click(clicks=2)
    def scroll(self, n):
        self._check(); self.log += [('wheel', 1 if n > 0 else -1)] * abs(n); self._done()
    def drag(self, dx, dy, button='left'):
        self._check()
        if (dx, dy) != (0, 0):
            self.log.append(('down', button)); self._at(self.pos.x + dx, self.pos.y + dy); self.log.append(('up', button))
        self._done()
    def dragTo(self, x, y, button='left'):
        self._check(); self.log.append(('down', button)); self._at(x, y); self.log.append(('up', button)); self._done()
    def keyDown(self, k): self._check(); self.log.append(('keydown', k.lower() if len(k) > 1 else k)); self._done()
    def keyUp(self, k): self._check(); self.log.append(('keyup', k.lower() if len(k) > 1 else k)); self._done()
    def press(self, keys, presses=1):
        self._check()
        for _ in range(presses):
            for k in ([keys] if isinstance(keys, str) else keys): self._press(k)
        self._done()
    def write(self, message):
        self._check()
        for c in message: self._press(c)
        self._done()
    def hotkey(self, *keys):
        self._check()
        for k in keys: self.log.append(('keydown', k.lower() if len(k) > 1 else k))
        for k in reversed(keys): self.log.append(('keyup', k.lower() if len(k) > 1 else k))
        self._done()
'''

FINDINGS = [
 ("F1","Background","Chapter 23 of the 3rd edition, Controlling the Keyboard and Mouse, introduces GUI automation with the PyAutoGUI library: a warning not to name a program pyautogui.py; the accessibility setting macOS needs; the fail-safe, the pause and the logout as ways to stay in control; screen coordinates, size(), moveTo(), move() and position(); click(), mouseDown(), mouseUp(), doubleClick(), drag(), dragTo() and scroll() with the square-spiral program spiralDraw.py; the MouseInfo tool; screenshot(), pixel(), pixelMatchesColor(), locateOnScreen(), locateAllOnScreen() and ImageNotFoundException; window objects and their attributes and methods; a box about captchas and ethics; write(), key names, press(), keyDown(), keyUp() and hotkey(); tips for setting up scripts, sleep() and countdown(); the message boxes of PyMsgBox; and it closes with 13 practice questions and 3 practice programs, Looking Busy, Reading Text Fields with the Clipboard and Writing a Game-Playing Bot.",["P01"]),
 ("F2","Comparative analysis","The chapter names PyAutoGUI version 1.0.0 three times, twice for the window features working only on Windows and once for locateOnScreen() raising ImageNotFoundException instead of returning None, but the newest release the package index offers is 0.9.54, and the source of 0.9.54 already has the names the chapter uses, write() as another name of typewrite(), drag() of dragRel() and move() of moveRel(), with comments that say they are the names PyAutoGUI 1.0 is meant to use; the documentation dates ImageNotFoundException to version 0.9.41, so the version number 1.0.0 in the chapter names a release that does not exist and the behaviour it describes is that of 0.9.54.",["P01","P05","P09"]),
 ("F3","Comparative analysis","One printed command of the chapter fails in the current library: pyautogui.pixel((50, 200)), which the chapter prints twice, raises TypeError because PyScreeze 1.0.1 takes the two coordinates as separate arguments, pixel(x, y), and its source notes that the second edition of the book documented the tuple form; the chapter's pixelMatchesColor(50, 200, (130, 135, 144)) is called correctly and its True, and its False for a different colour, hold, and the function has a tolerance argument, default 0, that the chapter does not mention, so that (255, 255, 254) against (255, 255, 255) is False at tolerance 0 and True at tolerance 1.",["P01","P09","P10"]),
 ("F4","Comparative analysis","The chapter's account of the fail-safe and the pause holds with two additions: the fail-safe points of 0.9.54 are the four corners of the screen, as the chapter says, although the documentation's cheat sheet names only the upper-left, and they are computed once when PyAutoGUI is imported, so they do not follow a change of resolution; and the exception is raised by the next PyAutoGUI call after the pointer has reached a corner, not by the move that reached it, since the check runs before each call and a move that ends on a fail-safe point is itself exempt from the check. The pause is 0.1 second by default, added after every public call, and two clicks with PAUSE at 0.5 took 1.0 second.",["P01","P02","P07","P09"]),
 ("F5","Comparative analysis","What the chapter says about platforms matches the library but leaves out what a course needs: the window functions getActiveWindow(), getAllWindows(), getWindowsAt() and getWindowsWithTitle() exist only on Windows, and on Linux the names are absent and raise AttributeError (PyGetWindow implements only Windows); a screenshot on Linux needs a helper program that the chapter does not name, so screenshot() raised an Exception on the machine used here, and the Linux installation of the chapter's appendix lists python3-tk and python3-dev but no screenshot helper, while the PyAutoGUI and PyScreeze documents name scrot and gnome-screenshot; pyperclip needs xclip or xsel on Linux, and without them paste and copy raise PyperclipException.",["P01","P08","P09","P10","P11","P12","P20"]),
 ("F6","Contemporary developments","Current PyAutoGUI has more than the chapter presents: click() takes clicks, interval and button, with tripleClick(); press() takes presses and a list of keys and hold() is a context manager that holds keys for the length of a with block; moveTo() takes None for a coordinate to keep the present one; hscroll() scrolls sideways; onScreen() tests coordinates; center() and locateCenterOnScreen() give the middle of a Box; the optional confidence argument of the locate functions needs OpenCV; isValidKey() tests a key name; KEYBOARD_KEYS has 194 names including f1 to f24, where the chapter's table lists f1 to f12; and the tween functions shape a timed movement.",["P01","P03","P04","P05","P07","P09"]),
 ("F7","Contemporary developments","Some behaviour of the library surprises a reader of the chapter: PyAutoGUI does not keep a coordinate on the screen, since the lines that would clamp it are commented out in the source, so on the virtual X display used here it was the display that held the pointer at x = 0 after move(-300, 0) from x = 200, and the chapter's statement that there are no negative coordinates is a property of the screen and not a check of the library; a name that is not a key is silently ignored by press(), keyDown() and write(), which is why isValidKey() exists; a drag of (0, 0) does nothing; the chapter's spiralDraw.py makes 32 drag calls of which 2 are zero drags, and because distance has become negative by the last call its final drag moves down 20 pixels instead of up; and the nudge of the Looking Busy program from the pointer's corner position can reach a corner and trigger the fail-safe.",["P01","P03","P04","P09"]),
 ("F8","Conclusion","For an advanced course, chapter 23 is best taught as a small event language: every call is a list of events (a move, a button down and up, a key down and up, a wheel step) preceded by a fail-safe check and followed by a pause, and its reliability comes from what the script checks (a pixel, an image, a window, a log) before it lets the next events go; most of it can be run and compared without a desktop by recording the events, as done here for 21 scenarios, while screenshots, real windows, the clipboard and message boxes need a desktop and are read, not run, in this study; the chapter's printed outputs hold for PyAutoGUI 0.9.54 except the tuple form of pixel, and the version numbers, the platform notes and the library's additions listed above are what the course adds.",["P01","P02","P03","P04","P05","P09","P10","P11"]),
]

# (top, mid, leaf, exemplar, definition, io-or-None)
TAX = [
 ("ScreenCoordinates","Geometry","CoordinateOrigin","x, y = 0, 0","The origin (0, 0) is the upper-left pixel of the screen, x grows to the right and y grows downward, so on a screen 1920 pixels wide and 1080 high the lower-right pixel is (1919, 1079).",("(lambda w, h: ((0, 0), (w - 1, h - 1)))(1920, 1080)",'((0, 0), (1919, 1079))')),
 ("ScreenCoordinates","Geometry","ScreenSize","pyautogui.size()","size() returns a named tuple Size with the width and the height of the screen in pixels, readable by index or by attribute and unpackable into two names.",("(lambda S: (S(1920, 1080)[0], S(1920, 1080).height, tuple(S(1920, 1080))))(__import__('collections').namedtuple('Size', 'width height'))",'(1920, 1080, (1920, 1080))')),
 ("ScreenCoordinates","Geometry","PointAndBox","box = pyautogui.locateOnScreen('submit.png')","position() gives a named tuple Point of x and y, and the locate functions give a named tuple Box of left, top, width and height; the middle of a Box is its left plus half its width and its top plus half its height.",("(lambda B: (B(643, 745, 70, 29).left, (643 + 70 // 2, 745 + 29 // 2)))(__import__('collections').namedtuple('Box', 'left top width height'))",'(643, (678, 759))')),
 ("ScreenCoordinates","Movement","MoveTo","pyautogui.moveTo(100, 100, duration=0.25)","moveTo moves the pointer to absolute coordinates, at once or over the given number of seconds, and None for one coordinate keeps the present value of that coordinate.",("(lambda pos, x, y: (pos[0] if x is None else x, pos[1] if y is None else y))((100, 200), None, 500)",'(100, 500)')),
 ("ScreenCoordinates","Movement","MoveRelative","pyautogui.move(100, 0, duration=0.25)","move moves the pointer by an offset from where it is, to the right for a positive first number and downward for a positive second, so a negative number moves it left or up.",("(lambda pos, dx, dy: (pos[0] + dx, pos[1] + dy))((200, 100), -100, 0)",'(100, 100)')),
 ("ScreenCoordinates","Movement","ClampToScreen","pyautogui.onScreen(1920, 1080)","A point is on the screen when 0 <= x < width and 0 <= y < height, which onScreen tests; PyAutoGUI 0.9.54 does not clamp a target to the screen itself, so the display decides where a pointer sent off the screen stops.",("[(x, 0 <= x < 1920) for x in (-1, 0, 1919, 1920)]",'[(-1, False), (0, True), (1919, True), (1920, False)]')),
 ("MouseActions","Clicking","ClickFunction","pyautogui.click(10, 5)","click moves the pointer to the given coordinates if any and then sends a button press and a release for each click; doubleClick, rightClick and middleClick are the same call with other arguments, and mouseDown and mouseUp send the two halves alone.",("[(e, 'left') for _ in range(2) for e in ('down', 'up')]","[('down', 'left'), ('up', 'left'), ('down', 'left'), ('up', 'left')]")),
 ("MouseActions","Clicking","ButtonChoice","pyautogui.click(200, 250, button='right')","The button argument names the button: 'left', 'middle' or 'right' (also 'primary', 'secondary' and the numbers 1 to 7 on Linux), and any other value raises PyAutoGUIException.",("{'left': 1, 'middle': 2, 'right': 3}['right']",'3')),
 ("MouseActions","Clicking","ScrollWheel","pyautogui.scroll(200)","scroll sends wheel steps at the pointer, upward for a positive number and downward for a negative one; the size of a step depends on the system, and on the Linux backend every unit is one wheel click.",("[('up' if n > 0 else 'down', abs(n)) for n in (3, -2)]","[('up', 3), ('down', 2)]")),
 ("MouseActions","Dragging","DragFunctions","pyautogui.drag(30, 0, duration=0.2)","drag and dragTo hold the left button (or the one named by button) down while the pointer moves by an offset or to a place, and release it there; a drag of (0, 0) sends nothing.",("(lambda pos, dx, dy: [('down', 'left'), ('move', pos[0] + dx, pos[1] + dy), ('up', 'left')])((100, 100), 30, 0)","[('down', 'left'), ('move', 130, 100), ('up', 'left')]")),
 ("MouseActions","Dragging","SpiralDrawProgram","while distance > 0: pyautogui.drag(distance, 0, duration=0.2)","The chapter's spiralDraw.py drags right, down, left and up with a distance that shrinks by 20 after every second drag; starting from 300 it makes 32 drag calls, two of them with a zero distance, and the last one moves down because distance has turned negative.",("len([c for d in range(300, 0, -40) for c in ((d, 0), (0, d - 20), (-(d - 20), 0), (0, -(d - 40)))])",'32')),
 ("KeyboardActions","TypingText","WriteFunction","pyautogui.write('Hello, world!')","write presses and releases one key for every character of a string, adds the shift key by itself for capitals and symbols such as ! and lets an optional interval pass between the characters.",("('H'.isupper(), '!' in '~!@#$%^&*()_+', 'h'.isupper())",'(True, True, False)')),
 ("KeyboardActions","TypingText","KeyListTyping","pyautogui.write(['a', 'b', 'left', 'left', 'X', 'Y'])","Given a list, write presses each named key in turn, so arrow keys move the text cursor and the list above types XYab.",("(lambda keys: __import__('functools').reduce(lambda st, k: (st[0][:st[1]] + k + st[0][st[1]:], st[1] + 1) if len(k) == 1 else (st[0], max(0, st[1] - 1)) if k == 'left' else st, keys, ('', 0))[0])(['a', 'b', 'left', 'left', 'X', 'Y'])","'XYab'")),
 ("KeyboardActions","KeyNames","KeyNameTable","pyautogui.KEYBOARD_KEYS","A key that is not a single character has a short lowercase name such as 'enter', 'esc', 'left' or 'f1', listed in KEYBOARD_KEYS; names of more than one character are lowercased by the library, and 'shift', 'ctrl', 'alt' and 'win' mean the left-hand key.",("[k.lower() if len(k) > 1 else k for k in ('ENTER', 'A', 'Shift')]","['enter', 'A', 'shift']")),
 ("KeyboardActions","KeyNames","SilentInvalidKey","pyautogui.press('notakey')","A name that is not a valid key does not raise an error in press, keyDown or write; the call is ignored, so a script can test a name first with isValidKey.",("[k in {'enter', 'esc', 'left'} for k in ('left', 'leftt')]",'[True, False]')),
 ("KeyboardActions","KeyPresses","PressAndRelease","pyautogui.keyDown('shift'); pyautogui.press('4'); pyautogui.keyUp('shift')","keyDown sends a key press and keyUp a release; press sends both, as often as presses says, and hold holds keys for the length of a with block.",("[(e, 'left') for _ in range(2) for e in ('keydown', 'keyup')]","[('keydown', 'left'), ('keyup', 'left'), ('keydown', 'left'), ('keyup', 'left')]")),
 ("KeyboardActions","KeyPresses","HotkeyFunction","pyautogui.hotkey('ctrl', 'alt', 'shift', 's')","hotkey presses its keys in the order given and releases them in the reverse order, so that a combination such as CTRL-C is one call instead of four.",("(lambda ks: [('keydown', k) for k in ks] + [('keyup', k) for k in reversed(ks)])(('ctrl', 'c'))","[('keydown', 'ctrl'), ('keydown', 'c'), ('keyup', 'c'), ('keyup', 'ctrl')]")),
 ("KeepingControl","SafetyNets","FailSafe","pyautogui.FailSafeException","While pyautogui.FAILSAFE is True, a pointer in one of the four corners of the screen makes the next PyAutoGUI call raise FailSafeException before it does anything, so a runaway script can be stopped by sliding the mouse into a corner.",("(lambda w, h: sorted({(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)}))(1920, 1080)",'[(0, 0), (0, 1079), (1919, 0), (1919, 1079)]')),
 ("KeepingControl","SafetyNets","PauseSetting","pyautogui.PAUSE = 2","PAUSE is the number of seconds, 0.1 by default, that every PyAutoGUI call waits after it has finished; statements that are not PyAutoGUI calls are not slowed.",("round(10 * 0.1, 6)",'1.0')),
 ("KeepingControl","ScriptDiscipline","GuardedClick","if not pyautogui.pixelMatchesColor(x, y, expected): raise SystemExit","A script that checks what is on the screen before each event, and stops at the first check that fails, does no harm when a window has moved or a pop-up covers a button.",("next((i for i, ok in enumerate([True, True, False, True]) if not ok), None)",'2')),
 ("KeepingControl","ScriptDiscipline","ScriptLogging","logging.info('typed row %d', i)","A script that logs each finished step to a file can be stopped halfway and restarted at the first step that the log does not show as done.",("(lambda lines: 1 + max(int(l.split()[-1]) for l in lines if l.startswith('INFO')))(['INFO typed row 0', 'INFO typed row 1', 'ERROR stopped before row 2'])",'2')),
 ("KeepingControl","ScriptDiscipline","CountdownAndSleep","pyautogui.countdown(3)","sleep is time.sleep without the import; countdown prints the numbers from the given one down to 1, each followed by a space and a one-second wait, and then ends the line.",("''.join(str(i) + ' ' for i in range(3, 0, -1)) + '\\n'","'3 2 1 \\n'")),
 ("KeepingControl","ScriptDiscipline","AutomationEthics","captcha","A captcha is a test that only a human should pass, there to stop scripts from signing up for accounts, flooding sites or guessing passwords; the chapter holds the programmer responsible for what a program does.",None),
 ("SeeingTheScreen","Capture","ScreenshotFunction","im = pyautogui.screenshot()","screenshot returns a Pillow Image of the screen and can save it to a file; it needs Pillow, and on Linux a helper program for capturing the screen.",None),
 ("SeeingTheScreen","Capture","PixelMatch","pyautogui.pixelMatchesColor(50, 200, (130, 135, 144))","pixel(x, y) returns the RGB colour of one screen pixel, and pixelMatchesColor(x, y, rgb) is True when each of the three channels differs from the given colour by no more than tolerance, which is 0 by default, so the match is exact.",("(lambda pix, exp, tol: all(abs(a - b) <= tol for a, b in zip(pix, exp)))((255, 255, 254), (255, 255, 255), 0)",'False')),
 ("SeeingTheScreen","Recognition","LocateOnScreen","pyautogui.locateOnScreen('submit.png')","locateOnScreen searches the screen from the upper-left corner, to the right and then down, for a picture that matches pixel for pixel and returns the Box of the first match or raises ImageNotFoundException; locateAllOnScreen yields every match.",("(lambda g, t: [(x, y) for y in range(len(g) - len(t) + 1) for x in range(len(g[0]) - len(t[0]) + 1) if all(g[y + j][x:x + len(t[0])] == t[j] for j in range(len(t)))])(['..##..', '..##..', '......'], ['##', '##'])",'[(2, 0)]')),
 ("SeeingTheScreen","Recognition","MouseInfoTool","pyautogui.mouseInfo()","mouseInfo opens a small window that shows the pointer's coordinates and the colour under it and can copy or log them, to help a script's author find the numbers to use.",None),
 ("WindowsAndDialogs","WindowObjects","ActiveWindow","pyautogui.getActiveWindow()","getActiveWindow returns the window that receives the keyboard, as a Window object; with PyAutoGUI 0.9.54 this and the other window functions exist only on Windows.",None),
 ("WindowsAndDialogs","WindowObjects","WindowGeometry","active_win.topleft","A Window has left, top, width and height that can be read and set, and derived attributes such as right, bottom, topleft, center, size, area and box, so a button at a fixed offset inside a window can be clicked wherever the window is.",("(lambda l, t, w, h: (l + w, t + h, (l + w // 2, t + h // 2)))(500, 300, 2070, 1208)",'(2570, 1508, (1535, 904))')),
 ("WindowsAndDialogs","WindowObjects","WindowSearch","pyautogui.getWindowsWithTitle('Notepad')","getWindowsWithTitle returns a list of the windows whose title contains the text, an empty list when there are none; getAllWindows, getWindowsAt and getAllTitles return all windows, those at a point and the titles.",("[t for t in ('Untitled - Notepad', 'Mu 1.0.1 - test1.py', 'Notepad++') if 'Notepad' in t]","['Untitled - Notepad', 'Notepad++']")),
 ("WindowsAndDialogs","WindowObjects","WindowState","active_win.maximize()","A Window reports isMaximized, isMinimized and isActive and is changed by maximize, minimize, restore, activate and close; close may skip a dialog that asks to save work.",None),
 ("WindowsAndDialogs","MessageBoxes","MessageBoxFunctions","pyautogui.confirm('Continue?')","alert, confirm, prompt and password show a message box, from PyMsgBox, because a script's own text window may be hidden by the windows it works on; confirm returns the text of the button clicked, and prompt and password return the text typed or None after Cancel.",None),
 ("PracticeWork","Questions","PracticeQuestions","pyautogui.getWindowsWithTitle('Notepad')","The chapter's 13 practice questions ask for the fail-safe, size(), position(), moveTo() against move(), drag(), write(), key names, screenshot('screenshot.png'), PAUSE, PyAutoGUI against Selenium, what makes PyAutoGUI error prone, the size of every Notepad window and activating Firefox.",("(lambda W: [w.size for w in W if 'Notepad' in w.title])([type('W', (), {'title': 'Untitled - Notepad', 'size': (800, 600)})(), type('W', (), {'title': 'Mu', 'size': (2070, 1208)})()])",'[(800, 600)]')),
 ("PracticeWork","Programs","LookingBusy","pyautogui.move(-1, 0); pyautogui.sleep(10)","Looking Busy nudges the pointer one pixel left, waits ten seconds, nudges it one pixel right and repeats, so that a chat program sees mouse movement.",("sum(-1 if i % 2 == 0 else 1 for i in range(6))",'0')),
 ("PracticeWork","Programs","ClipboardReading","pyautogui.hotkey('ctrl', 'a'); pyautogui.hotkey('ctrl', 'c'); text = pyperclip.paste()","To read a text field, the program activates its window, clicks into it, selects all and copies with two hotkeys and reads the clipboard with pyperclip.paste(); PyAutoGUI alone cannot read text from another program.",None),
 ("PracticeWork","Programs","GameBot","asweigart/sushigoroundbot","Writing a Game-Playing Bot points to a bot for the Flash game Sushi Go Round that watches the game window for pictures of orders and clicks ingredient buttons.",None),
]
ERRORS = []
CLAIMS = [
 ("(1920 - 1, 1080 - 1)", "(1919, 1079)"),
 ("len(list(range(300, 0, -20)))", "15"),
 ("round(10 * 0.1, 6)", "1.0"),
 ("sorted({'enter', 'return', '\\n'})", "['\\n', 'enter', 'return']"),
]
S = "(Sweigart, 2025)"; PA = "(PyAutoGUI documentation, 2026)"; SRC = "(PyAutoGUI 0.9.54 source, read and run for this study)"; PSF = "(Python Software Foundation, 2026)"
GW = "(PyGetWindow README, 2026)"; PC = "(Pyperclip README, 2026)"; SG = "(sushigoroundbot README, 2026)"; MI = "(MouseInfo documentation, 2026)"; SEL = "(Selenium documentation, 2026)"; EX = "(executed for this study)"
BODY = {
 "ScreenCoordinates": "Where things are on the screen, and how the pointer is sent there, are the base of Chapter 23 " + S + ".",
 "Geometry": "The screen is a grid of pixels, and the chapter gives it a size and gives places on it points and boxes " + S + ".",
 "CoordinateOrigin": "The origin (0, 0) is the upper-left corner, x increases to the right and y increases downward, so on a 1920 by 1080 screen the lower-right pixel is (1919, 1079), and the chapter states that all coordinates are positive integers " + S + "; the documentation's onScreen(0, -1) is False, onScreen(1919, 1079) is True and onScreen(1920, 1080) is False, as run here, and an on-screen test written for this study gave [True, False, True, False] for (0, 0), (0, -1), (1919, 1079) and (1920, 1080) " + PA + " " + SRC + ".",
 "ScreenSize": "size() returns the named tuple Size(width=1920, height=1080) on the chapter's screen, which can be indexed, read by attribute, unpacked into two names and turned into a tuple " + S + "; a named tuple gives each position a name and is still a tuple " + PSF + "; PyAutoGUI handles only the primary monitor " + PA + ".",
 "PointAndBox": "position() returns a Point such as Point(x=1536, y=637), read by index or by x and y " + S + "; a Box is left, top, width and height, as in Box(left=643, top=745, width=70, height=29), whose middle is Point(x=678, y=759), the place at which click((643, 745, 70, 29)) moved the pointer in the recorded PyAutoGUI events " + S + " " + SRC + ".",
 "Movement": "moveTo() sets the pointer's place and move() changes it by an offset " + S + ".",
 "MoveTo": "moveTo(100, 100, duration=0.25) moves the pointer there over a quarter of a second and, without a duration, at once " + S + "; None keeps a coordinate, so from (100, 200) moveTo(None, 500) ended at (100, 500) and moveTo(600, None) at (600, 200) in the recorded events, and a duration of no more than MINIMUM_DURATION, 0.1 second, means an instant move " + PA + " " + SRC + ".",
 "MoveRelative": "move(100, 0, duration=0.25) moves the pointer 100 pixels to the right and the chapter's square uses move(100, 0), move(0, 100), move(-100, 0) and move(0, -100) " + S + "; in the recorded events moveTo(100, 100), move(100, 0) and move(0, 100) sent moves to (100, 100), (200, 100) and (200, 200), and the model sent the same events " + SRC + ".",
 "ClampToScreen": "A point is on the screen when 0 <= x < width and 0 <= y < height, which onScreen() tests " + PA + "; the lines of the source that would keep a target inside the screen are commented out, so PyAutoGUI does not clamp, and on the virtual X display used here the pointer stopped at x = 0 after move(-300, 0) from x = 200 and at x = 0 after moveTo(-5, 400), which is why the model clamps; the chapter's statement that there are no negative coordinates describes the screen, not a check in the library " + S + " " + SRC + ".",
 "MouseActions": "Clicking, scrolling and dragging send mouse-button and wheel events to the computer " + S + ".",
 "Clicking": "A click is a button press followed by a release at a place, and the wheel is a separate kind of step " + S + ".",
 "ClickFunction": "click(10, 5) moves the pointer to (10, 5) and clicks the left button once, a full click being a button down and then a button up, and mouseDown() and mouseUp() send the two halves " + S + "; the recorded events of click(10, 5) were a move to (10, 5), a press of the left button and its release, doubleClick() sent two press-and-release pairs, click(10, 5, clicks=3) sent three, and the model sent the same events as the recorded ones for the first two; on the Linux backend click() is built from the same press and release, as the chapter says " + SRC + "; the documentation adds tripleClick() and the clicks and interval arguments " + PA + ".",
 "ButtonChoice": "button='left', 'middle' or 'right' chooses the button, as in click(100, 150, button='left') and click(200, 250, button='right') " + S + "; the right button was recorded as a press and release of the right button at (100, 150), and an unknown value raised PyAutoGUIException with the message button argument must be one of ('left', 'middle', 'right', 'primary', 'secondary', 1, 2, 3, 4, 5, 6, 7) on Linux, where 1, 2 and 3 are left, middle and right " + SRC + ".",
 "ScrollWheel": "scroll(200) scrolls up and a negative number scrolls down, by units whose size the operating system and the program decide " + S + "; on the Linux backend the recorded events of scroll(3) were three wheel-up steps and of scroll(-2) two wheel-down steps, because the source repeats one wheel click for every unit, so scroll(200) sends 200 of them; hscroll() scrolls sideways on macOS and Linux " + SRC + " " + PA + ".",
 "Dragging": "Dragging is moving the pointer while a button is held, and the chapter draws a spiral with it " + S + ".",
 "DragFunctions": "drag() moves by an offset and dragTo() to a place while the left button is held, and macOS needs a duration to drag correctly " + S + "; the recorded events of drag(30, 0) from (100, 100) were a press of the left button, a move to (130, 100) and a release, dragTo(200, 150) sent a move to (200, 150) between the same two events, drag(0, 0) sent no events at all, and button='right' held the right button, the model giving the same events for the first three; the documentation says the button keyword is 'left', 'middle' or 'right' " + SRC + " " + PA + ".",
 "SpiralDrawProgram": "spiralDraw.py starts with distance = 300 and change = 20 and in each pass of its while loop drags right, reduces distance, drags down, drags left, reduces distance and drags up " + S + "; run against the model from (500, 500) it made 32 drag calls, (0, 0) appeared twice, distance ended at -20 and the last call was (0, 20), a drag downward, because distance was already negative; the points it visited lay inside the rectangle from (500, 500) to (800, 780) and the pointer ended at (660, 660), and the same loop against PyAutoGUI 0.9.54 with recorded events made 32 calls, 30 button presses and also ended at (660, 660) " + SRC + " " + EX + ".",
 "KeyboardActions": "Typing, key names and key presses send keyboard events to the active window " + S + ".",
 "TypingText": "write() types text, either as a string of characters or as a list of key names " + S + ".",
 "WriteFunction": "write('Hello, world!') types the string into the active window, with an optional pause after each character, and for characters such as A or ! it holds the shift key by itself " + S + "; the recorded events of write('Hi!') were a press and release of H, i and ! with no separate shift event, because the Linux backend adds the shift key inside the press of a shift character, which isShiftCharacter() decides: it gave [False, True, True, False, True] for a, A, !, 4 and ~; the documentation says write() with a string can press only single-character keys " + SRC + " " + PA + ".",
 "KeyListTyping": "write(['a', 'b', 'left', 'left', 'X', 'Y']) presses the keys in turn and, because the left arrow moves the text cursor, types XYab " + S + "; the recorded events were a press and release of a, b, left, left, X and Y, so the library sends the arrow key and does not edit text itself, and a text-cursor model fed those keys gave XYab and, fed the characters of Hello, world! one by one, gave Hello, world!; the keyboard page of the documentation says write() presses only single-character keys, while the source accepts a list of key names and the events above show it " + SRC + " " + PA + " " + EX + ".",
 "KeyNames": "Keys that are not single characters are named by short strings " + S + ".",
 "KeyNameTable": "Table 23-1 gives names such as 'enter' (or 'return'), 'esc', 'tab', 'shiftleft', 'left', 'f1', 'volumemute', 'pause', 'capslock', 'printscreen', 'winleft' and 'command', and says 'shift', 'ctrl', 'alt' and 'win' mean the left-hand key " + S + "; every name of that table is in pyautogui.KEYBOARD_KEYS of 0.9.54, which has 194 names including f1 to f24 where the table says F1 to F12, 'shift' and 'shiftleft' have the same keycode, 50, on the X display used here, and a name longer than one character is lowercased, so press('ENTER') was recorded as enter; on that Linux backend isValidKey() is False for 'command', 'option' and 'volumemute' and True for 'enter', 'return', 'esc', 'f13', 'printscreen' and 'win' " + SRC + ".",
 "SilentInvalidKey": "press('notakey') raised no error: the recorded call passed the name to the backend, which dropped it, and the source says that an invalid key is currently a no-op that does not raise, so isValidKey('notakey') is False while isValidKey('enter') and isValidKey('ctrl') are True; in the text-cursor model an unknown key was ignored and a, b, notakey, c gave abc; the chapter does not mention this " + S + " " + SRC + " " + EX + ".",
 "KeyPresses": "A key press is a down and an up event, and a hotkey is several of them in a fixed order " + S + ".",
 "PressAndRelease": "keyDown('shift'), press('4') and keyUp('shift') in a row type a dollar sign, and press() calls keyDown() and keyUp() for one key " + S + "; the recorded events of that line were keydown shift, keydown 4, keyup 4, keyup shift, the same as in the model, press('left', presses=2) gave two press-and-release pairs, and hold('shift') around press(['left', 'left']) gave keydown shift, two pairs of left and keyup shift, which the chapter does not present; that a dollar sign appears on a screen was not run here " + SRC + " " + PA + ".",
 "HotkeyFunction": "hotkey('ctrl', 'c') presses ctrl, presses c, releases c and releases ctrl, and hotkey('ctrl', 'alt', 'shift', 's') takes the place of eight calls; the copy shortcut is the command key on macOS " + S + "; the recorded events of the four-key call were keydown ctrl, alt, shift, s and then keyup s, shift, alt, ctrl, as in the model, and the documentation gives the same order " + SRC + " " + PA + ".",
 "KeepingControl": "A GUI script can run faster than its author can react, so the chapter adds ways to stop it and to keep it honest " + S + ".",
 "SafetyNets": "The fail-safe and the pause are the library's two built-in ways of staying in control " + S + ".",
 "FailSafe": "Sliding the mouse into a corner makes PyAutoGUI raise pyautogui.FailSafeException, and every PyAutoGUI call pauses a tenth of a second to leave time for that " + S + "; in 0.9.54 FAILSAFE is True by default and the fail-safe points are the four corners, (0, 0), (0, 1079), (1919, 0) and (1919, 1079) on the 1920 by 1080 display, computed once when PyAutoGUI is imported, although the documentation's cheat sheet names only the upper-left; moveTo(0, 0) raised nothing, the pointer stood at (0, 0), and the next call raised FailSafeException before it did anything, a click at a corner sent no events, press('a') raised at each of the four corners and not at (1, 0) or (960, 540), FAILSAFE = False let the script carry on, and FailSafeException is a PyAutoGUIException " + PA + " " + SRC + ".",
 "PauseSetting": "Every PyAutoGUI call pauses PAUSE seconds afterwards, 0.1 by default, and PAUSE = 2 gives the two-second pause that practice question 9 asks for; statements that are not PyAutoGUI calls have no pause " + S + "; in the model ten calls at the default pause added up to 1.0 second and two clicks at PAUSE 0.5 to 1.0 second, which two clicks under PyAutoGUI 0.9.54 took in real time, and a call that does several things such as write() or hotkey() pauses once at its end, so write('abc') and hotkey('ctrl', 'a') at PAUSE 2 added up to 4.0 seconds in the model " + SRC + " " + EX + ".",
 "ScriptDiscipline": "A GUI script is finicky, so the chapter asks it to check, wait, log and stop " + S + ".",
 "GuardedClick": "The chapter's tips are to keep the resolution and the window state the same, to pause for content to load, to use locateOnScreen() and stop if it fails, to check the window with getWindowsWithTitle() and activate() it, to log, to add checks and to supervise the first run, and it suggests testing a pixel before click() " + S + "; in a model a click guarded by a pixel test sent a move to (50, 200) and a left click while the pixel was (130, 135, 144), and after a pop-up changed the pixel it raised SystemExit with the text stop: the screen is not what the script expects at (50, 200) and sent no events " + EX + ".",
 "ScriptLogging": "The chapter says to keep a logfile with the logging module, so that a script stopped halfway can be changed to pick up where it left off " + S + "; with the standard library logging module a run that stopped before row 2 left the lines INFO typed row 0, INFO typed row 1 and ERROR stopped before row 2, the resume point read from those lines was row 2, and the second run logged rows 2 and 3 " + PSF + " " + EX + ".",
 "CountdownAndSleep": "sleep(3) pauses the program for 3 seconds exactly as time.sleep() does, and countdown(10) prints 10 9 8 7 6 5 4 3 2 1, so print('Starting in ', end=''); countdown(3) shows Starting in 3 2 1 " + S + "; in the PyAutoGUI source countdown() prints each number followed by a space, waits a second and ends the line at the end, and the same loop with the sleeps replaced printed Starting in 3 2 1 with a space after each number and a line break after the last, and slept [1, 1, 1] " + PSF + " " + SRC + " " + EX + ".",
 "AutomationEthics": "The box on captchas says they are tests that people pass easily and software almost never does, that the chapter's techniques could otherwise sign up for accounts, flood users with messages or guess passwords, and that responsibility for a program falls on its programmer " + S + "; the PyAutoGUI FAQ adds that it does no OCR and cannot tell whether a key is held down " + PA + ".",
 "SeeingTheScreen": "A script that looks at the screen before it acts can notice that it has gone wrong " + S + ".",
 "Capture": "A screenshot is an image of the screen, and a pixel is one colour in it " + S + ".",
 "ScreenshotFunction": "im = pyautogui.screenshot() returns a Pillow Image of the screen, and Chapter 21 and Pillow are needed first " + S + "; screenshot('my_screenshot.png') also saves the file and region=(left, top, width, height) takes a part " + PA + "; on the Linux machine used here, with Pillow 12.3.0, the call raised an Exception that says Pillow 9.2.0 or greater and gnome-screenshot are needed, so no screenshot was taken and no output of screenshot() or pixel() on a real screen was reproduced; the documentation names scrot for Linux " + SRC + ".",
 "PixelMatch": "pixel(0, 0) returns an RGB tuple such as (176, 176, 175), pixelMatchesColor(50, 200, (130, 135, 144)) is True and with (255, 135, 144) False, and the match must be exact, (255, 255, 254) against (255, 255, 255) being False " + S + "; with the screen replaced by an in-memory Pillow image, PyScreeze 1.0.1 gave True, False, False and, with tolerance=1, True for those four cases, pixel((50, 200)) raised TypeError: pixel() missing 1 required positional argument: 'y', so the tuple form the chapter prints twice does not run and the coordinates must be separate, and the pixel test written for the model gave False for the same near miss " + SRC + " " + EX + ".",
 "Recognition": "Image recognition finds a picture on the screen instead of using fixed coordinates " + S + ".",
 "LocateOnScreen": "locateOnScreen('submit.png') returns Box(left=643, top=745, width=70, height=29) for the first place the picture is found, raises ImageNotFoundException when it is not found or is a pixel off, list(locateAllOnScreen('submit.png')) lists every Box and click('submit.png') clicks the middle " + S + "; in 0.9.54 the locate functions also work on two in-memory Pillow images without a screen: pyautogui.locate() found a 3 by 2 block in a 12 by 6 image as Box(left=4, top=2, width=3, height=2), locateAll() found it and a second block as Box(left=8, top=3, width=3, height=2), a picture that was not there raised pyautogui.ImageNotFoundException, which a handler written with that name caught, and after useImageNotFoundException(False) the same search returned None; a grid search written for this study gave the same two boxes; the documentation says the search starts at the upper-left corner and goes right and then down, that the exception has been raised since version 0.9.41, that the confidence argument needs OpenCV and that a search of a 1920 by 1080 screen takes about 1 or 2 seconds " + PA + " " + SRC + " " + EX + ".",
 "MouseInfoTool": "pyautogui.mouseInfo() opens the MouseInfo window, which shows the pointer's coordinates and the colour under it as an RGB tuple and a hex value, has Copy and Log buttons with a 3 second delay that the F1 to F8 keys avoid, and can save its log " + S + "; the MouseInfo documentation describes the same program and the origin at the top left " + MI + "; 0.9.54 has a mouseInfo attribute, but the window needs a desktop and was not opened here " + SRC + ".",
 "WindowsAndDialogs": "Windows can be found, measured and moved, and message boxes talk to the user when the terminal is hidden " + S + ".",
 "WindowObjects": "A Window object describes one application window " + S + ".",
 "ActiveWindow": "getActiveWindow() returns the window that accepts keyboard input, a Win32Window on Windows, and the chapter notes that the window features work only on Windows " + S + "; in 0.9.54 they are imported from PyGetWindow only when the platform is win32, so on Linux getActiveWindow, getAllTitles and getWindowsWithTitle raised AttributeError: module 'pyautogui' has no attribute with that name, and the PyGetWindow README says only Windows is implemented " + GW + " " + SRC + ".",
 "WindowGeometry": "For a window at left 500, top 300 with width 2070 and height 1208 the chapter prints right 2570, bottom 1508, size Size(width=2070, height=1208) and topleft Point(x=500, y=300), and click(left + 10, top + 20) hits a button fixed 10 pixels right of and 20 below the corner " + S + "; arithmetic on those four numbers in a model of the attributes gave right 2570, bottom 1508, centre (1535, 904) and area 2500560, a click at (510, 320), and right 1500 after the width was set to 1000; PyGetWindow itself was not run " + EX + ".",
 "WindowSearch": "getWindowsWithTitle('Notepad') returns a list of the windows with that text in their title and an empty list if there are none, getAllWindows() returns all windows, getWindowsAt(x, y) those at a point and getAllTitles() their titles " + S + "; a search written as 'Notepad' in title over three windows returned the two windows whose titles hold it and [] for 'Firefox'; how PyGetWindow matches on Windows was not run, its README shows getWindowsWithTitle('Untitled') finding Untitled - Notepad " + GW + " " + EX + ".",
 "WindowState": "isMaximized, isMinimized and isActive are True or False, maximize(), minimize(), activate() and restore() change the state, restore() undoes a minimize or maximize and close() may bypass a dialog that asks to save " + S + "; the PyGetWindow README also lists resize, resizeTo, move and moveTo " + GW + "; none of it was run, since it needs Windows.",
 "MessageBoxes": "Message boxes give a script a place to talk to the user that the windows it works on cannot hide " + S + ".",
 "MessageBoxFunctions": "alert(text) shows an OK button, confirm(text) returns 'OK' or 'Cancel', prompt(text) returns the typed text and password(text) does the same with asterisks " + S + "; the documentation adds that confirm returns the text of the button clicked and can carry other buttons, and that prompt and password return None after Cancel " + PA + "; in 0.9.54 the functions are built on tkinter (alert is a function named _alertTkinter here) and tkinter is the standard Python interface to Tk; they open a window and were not run " + PSF + " " + SRC + ".",
 "PracticeWork": "The chapter ends with 13 practice questions and three practice programs " + S + ".",
 "Questions": "The practice questions revisit the fail-safe, movement, dragging, typing, screenshots, pauses and windows " + S + ".",
 "PracticeQuestions": "The answers read from the chapter's text: 1, slide the mouse into a screen corner so that FailSafeException is raised; 2, size(); 3, position(); 4, moveTo() goes to absolute coordinates and move() by an offset; 5, drag() and dragTo(); 6, write('Hello, world!'); 7, a key name such as 'left' in press() or in a list given to write(); 8, screenshot('screenshot.png'); 9, pyautogui.PAUSE = 2; 10, Selenium for a web browser, since PyAutoGUI clicks blindly at coordinates while Selenium drives the browser through WebDriver; 11, it cannot see what it is clicking, so a moved window or a pop-up sends it wrong; 12, getWindowsWithTitle('Notepad') and the size of each window returned; 13, getWindowsWithTitle('Firefox')[0].activate() " + S + " " + SEL + "; a list comprehension over two stand-in windows gave [(800, 600)] for the one titled Untitled - Notepad " + EX + ".",
 "Programs": "The practice programs keep a chat status active, read a text field and play a game " + S + ".",
 "LookingBusy": "The program nudges the pointer one pixel left every 10 seconds and one pixel right 10 seconds later " + S + "; in the model six nudges from (400, 300) at 10-second steps gave x of 399, 400, 399, 400, 399 and 400; started at (1, 0) the first nudge reached the corner (0, 0) and the second call raised the fail-safe; started at x = 0 the left nudge moved nothing, so after four nudges the pointer stood at (1, 300) after three move events, one pixel from where it began " + EX + ".",
 "ClipboardReading": "The program gets the window with getWindowsWithTitle('Notepad'), activates it, clicks into the text field, sends hotkey('ctrl', 'a') and hotkey('ctrl', 'c') and reads pyperclip.paste(), because PyAutoGUI alone cannot read text from another program " + S + "; in a model the two hotkeys copied the field's text to the clipboard and typing a and c without ctrl copied nothing; Pyperclip needs xclip or xsel on Linux and here copy() raised PyperclipException: Pyperclip could not find a copy/paste mechanism for your system, so paste() was not run " + PC + " " + SRC + " " + EX + ".",
 "GameBot": "The last practice program points to a bot for the Flash game Sushi Go Round and says Flash is discontinued " + S + "; the repository README says the bot is written with PyAutoGUI, that the game must stay fully visible and unmoved, and that moving the mouse to the top-left corner interrupts it; it was not run " + SG + ".",
}
BEH = [
 ['the coordinate types of the chapter as named tuples, and the on-screen test', r"""from collections import namedtuple
Size = namedtuple('Size', 'width height'); Point = namedtuple('Point', 'x y')
Box = namedtuple('Box', 'left top width height')
screen = Size(1920, 1080)
print(screen, screen[0], screen.width, tuple(screen))
p = Point(1536, 637)
print(p, p[0], p.x)
width, height = screen
print('bottom-right pixel:', (width - 1, height - 1))
def on_screen(x, y):
    return 0 <= x < screen.width and 0 <= y < screen.height
print([on_screen(*xy) for xy in [(0, 0), (0, -1), (1919, 1079), (1920, 1080)]])
box = Box(643, 745, 70, 29)
print(box, box.left, box[0])
print('centre:', Point(box.left + box.width // 2, box.top + box.height // 2))""", 'Size(width=1920, height=1080) 1920 1920 (1920, 1080)\nPoint(x=1536, y=637) 1536 1536\nbottom-right pixel: (1919, 1079)\n[True, False, True, False]\nBox(left=643, top=745, width=70, height=29) 643 643\ncentre: Point(x=678, y=759)'],
 ['moveTo, move and None, as events (the model matches the recorded PyAutoGUI events)', DESK + r"""d = Desk(pos=(311, 622))
d.moveTo(100, 100); d.move(100, 0); d.move(0, 100)
print(d.pos, d.log)
d.move(-300, 0)
print(d.pos)
d.moveTo(None, 500); print(d.pos)
d.moveTo(600, None); print(d.pos)""", "Point(x=200, y=200) [('move', 100, 100), ('move', 200, 100), ('move', 200, 200)]\nPoint(x=0, y=200)\nPoint(x=0, y=500)\nPoint(x=600, y=500)"],
 ['clicks, buttons and the wheel as the events they send', DESK + r"""d = Desk(pos=(960, 540))
d.click(10, 5); print(d.log)
d.log.clear(); d.click(100, 150, button='right'); print(d.log, tuple(d.pos))
d.log.clear(); d.click((643, 745, 70, 29)); print(d.log)
d.log.clear(); d.doubleClick(); print(len(d.log), d.log[:2])
d.log.clear(); d.scroll(3); d.scroll(-2); print(d.log)""", "[('move', 10, 5), ('down', 'left'), ('up', 'left')]\n[('move', 100, 150), ('down', 'right'), ('up', 'right')] (100, 150)\n[('move', 678, 759), ('down', 'left'), ('up', 'left')]\n4 [('down', 'left'), ('up', 'left')]\n[('wheel', 1), ('wheel', 1), ('wheel', 1), ('wheel', -1), ('wheel', -1)]"],
 ['drag, dragTo and a drag of zero', DESK + r"""d = Desk(pos=(100, 100))
d.drag(30, 0); print(d.log, tuple(d.pos))
d.log.clear(); d.dragTo(200, 150); print(d.log, tuple(d.pos))
d.log.clear(); d.drag(0, 0); print(d.log, tuple(d.pos))
d.log.clear(); d.drag(10, 0, button='right'); print(d.log)""", "[('down', 'left'), ('move', 130, 100), ('up', 'left')] (130, 100)\n[('down', 'left'), ('move', 200, 150), ('up', 'left')] (200, 150)\n[] (200, 150)\n[('down', 'right'), ('move', 210, 150), ('up', 'right')]"],
 ['spiralDraw.py of the chapter: the drag calls it makes', DESK + r"""d = Desk(pos=(500, 500)); calls = []; seen = [tuple(d.pos)]
def drag(dx, dy):
    calls.append((dx, dy)); d.drag(dx, dy); seen.append(tuple(d.pos))
distance = 300
change = 20
while distance > 0:
    drag(distance, 0)
    distance = distance - change
    drag(0, distance)
    drag(-distance, 0)
    distance = distance - change
    drag(0, -distance)
print(len(calls), calls[:4], calls[-4:])
print('distance at the end:', distance, 'zero drags:', calls.count((0, 0)))
print('button-down events:', sum(1 for e in d.log if e[0] == 'down'), 'final pointer:', tuple(d.pos))
xs = [q[0] for q in seen]; ys = [q[1] for q in seen]
print('rectangle walked:', (min(xs), min(ys), max(xs), max(ys)))""", '32 [(300, 0), (0, 280), (-280, 0), (0, -260)] [(20, 0), (0, 0), (0, 0), (0, 20)]\ndistance at the end: -20 zero drags: 2\nbutton-down events: 30 final pointer: (660, 660)\nrectangle walked: (500, 500, 800, 780)'],
 ['write with a string and with a key list, and what a text cursor does with them', DESK + r"""d = Desk()
d.write('Hi!'); print(d.log)
d.log.clear(); d.write(['a', 'b', 'left', 'left', 'X', 'Y'])
keys = [e[1] for e in d.log if e[0] == 'keydown']
print(keys)
def editor(keys):
    text, cursor = '', 0
    for k in keys:
        if len(k) == 1: text, cursor = text[:cursor] + k + text[cursor:], cursor + 1
        elif k == 'left': cursor = max(0, cursor - 1)
        elif k == 'right': cursor = min(len(text), cursor + 1)
        elif k == 'backspace' and cursor: text, cursor = text[:cursor - 1] + text[cursor:], cursor - 1
    return text
print(editor(keys), editor(list('Hello, world!')))
print(editor(['a', 'b', 'notakey', 'c']))""", "[('keydown', 'H'), ('keyup', 'H'), ('keydown', 'i'), ('keyup', 'i'), ('keydown', '!'), ('keyup', '!')]\n['a', 'b', 'left', 'left', 'X', 'Y']\nXYab Hello, world!\nabc"],
 ['press, keyDown, keyUp and hotkey as events, and the shift rule', DESK + r"""d = Desk()
d.press('ENTER'); d.press('left', presses=2); print(d.log)
d.log.clear(); d.keyDown('shift'); d.press('4'); d.keyUp('shift'); print(d.log)
d.log.clear(); d.hotkey('ctrl', 'c'); print(d.log)
d.log.clear(); d.hotkey('ctrl', 'alt', 'shift', 's')
downs = [e[1] for e in d.log if e[0] == 'keydown']; ups = [e[1] for e in d.log if e[0] == 'keyup']
print(downs, ups, ups == downs[::-1])
def needs_shift(ch): return ch.isupper() or ch in set('~!@#$%^&*()_+{}|:<>?')
print([needs_shift(c) for c in 'aA!4~'])""", "[('keydown', 'enter'), ('keyup', 'enter'), ('keydown', 'left'), ('keyup', 'left'), ('keydown', 'left'), ('keyup', 'left')]\n[('keydown', 'shift'), ('keydown', '4'), ('keyup', '4'), ('keyup', 'shift')]\n[('keydown', 'ctrl'), ('keydown', 'c'), ('keyup', 'c'), ('keyup', 'ctrl')]\n['ctrl', 'alt', 'shift', 's'] ['s', 'shift', 'alt', 'ctrl'] True\n[False, True, True, False, True]"],
 ['the fail-safe raises on the next call, not on the move into the corner', DESK + r"""d = Desk(pos=(500, 500))
d.moveTo(0, 0)
print('at the corner:', tuple(d.pos), 'and nothing has been raised')
try:
    d.moveTo(500, 500)
except FailSafeException:
    print('the next call raised; the pointer is still at', tuple(d.pos))
print(sorted(d.corners))
for xy in [(0, 0), (1919, 0), (0, 1079), (1919, 1079), (1, 0), (960, 540)]:
    t = Desk(pos=xy)
    try:
        t.press('a'); r = 'ok'
    except FailSafeException:
        r = 'raises'
    print(xy, r)
d.FAILSAFE = False; d.moveTo(500, 500); print(tuple(d.pos), len(d.log))""", 'at the corner: (0, 0) and nothing has been raised\nthe next call raised; the pointer is still at (0, 0)\n[(0, 0), (0, 1079), (1919, 0), (1919, 1079)]\n(0, 0) raises\n(1919, 0) raises\n(0, 1079) raises\n(1919, 1079) raises\n(1, 0) ok\n(960, 540) ok\n(500, 500) 2'],
 ['PAUSE is added after every call', DESK + r"""d = Desk(); d.PAUSE = 0.5
d.click(); d.click(); print(d.clock)
d = Desk()
for i in range(10): d.move(1, 0)
print(d.PAUSE, round(d.clock, 2))
d = Desk(); d.PAUSE = 2
d.write('abc'); d.hotkey('ctrl', 'a'); print(d.clock, len(d.log))""", '1.0\n0.1 1.0\n4.0 10'],
 ['a click that first checks a pixel of the screen and stops when it is wrong', DESK + r"""class Screen:
    def __init__(self, default): self.default, self.pixels = default, {}
    def pixel(self, x, y): return self.pixels.get((x, y), self.default)
    def matches(self, x, y, expected, tolerance=0):
        return all(abs(a - b) <= tolerance for a, b in zip(self.pixel(x, y), expected))
screen = Screen((255, 255, 254)); screen.pixels[(50, 200)] = (130, 135, 144)
print(screen.matches(50, 200, (130, 135, 144)), screen.matches(50, 200, (255, 135, 144)))
print(screen.matches(1, 1, (255, 255, 255)), screen.matches(1, 1, (255, 255, 255), tolerance=1))
d = Desk()
def guarded_click(x, y, expected):
    if not screen.matches(x, y, expected):
        raise SystemExit('stop: the screen is not what the script expects at (%d, %d)' % (x, y))
    d.click(x, y)
guarded_click(50, 200, (130, 135, 144)); print(d.log)
screen.pixels[(50, 200)] = (200, 0, 0)
d.log.clear()
try:
    guarded_click(50, 200, (130, 135, 144))
except SystemExit as e:
    print(e, d.log)""", "True False\nFalse True\n[('move', 50, 200), ('down', 'left'), ('up', 'left')]\nstop: the screen is not what the script expects at (50, 200) []"],
 ['a log that lets a stopped script start again at the first unfinished step', r"""import io, logging
buf = io.StringIO()
logging.basicConfig(stream=buf, level=logging.INFO, format='%(levelname)s %(message)s', force=True)
rows = ['ann', 'bob', 'cem', 'dia']
def run(first, fail_at=None):
    for i in range(first, len(rows)):
        if i == fail_at:
            logging.error('stopped before row %d', i); return
        logging.info('typed row %d', i)
run(0, fail_at=2)
lines = buf.getvalue().splitlines(); print(lines)
done = [int(l.split()[-1]) for l in lines if l.startswith('INFO')]
resume = max(done) + 1; print('resume at row', resume)
run(resume); print(buf.getvalue().splitlines()[-2:])""", "['INFO typed row 0', 'INFO typed row 1', 'ERROR stopped before row 2']\nresume at row 2\n['INFO typed row 2', 'INFO typed row 3']"],
 ['countdown prints the numbers with the sleeps replaced', r"""import io, time, contextlib
slept = []
time.sleep = slept.append
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(str(i), end=' ', flush=True)
        time.sleep(1)
    print()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print('Starting in ', end=''); countdown(3)
print(repr(buf.getvalue()), slept)""", "'Starting in 3 2 1 \\n' [1, 1, 1]"],
 ['finding a picture in a screen grid, all matches, no match, and the click in its middle', DESK + r"""class ImageNotFoundException(Exception): pass
def locate_all(screen, needle):
    h, w = len(needle), len(needle[0])
    for y in range(len(screen) - h + 1):
        for x in range(len(screen[0]) - w + 1):
            if all(screen[y + j][x:x + w] == needle[j] for j in range(h)):
                yield Box(x, y, w, h)
def locate(screen, needle):
    for box in locate_all(screen, needle):
        return box
    raise ImageNotFoundException('the picture is not on the screen')
screen = ['............', '............', '....###.....', '....###.###.', '........###.', '............']
needle = ['###', '###']
print(locate(screen, needle))
print(list(locate_all(screen, needle)))
try:
    locate(screen, ['###', '##.'])
except ImageNotFoundException as e:
    print('ImageNotFoundException:', e)
box = locate(screen, needle); d = Desk(); d.click(box)
print(tuple(d.pos), (box.left + box.width // 2, box.top + box.height // 2))""", 'Box(left=4, top=2, width=3, height=2)\n[Box(left=4, top=2, width=3, height=2), Box(left=8, top=3, width=3, height=2)]\nImageNotFoundException: the picture is not on the screen\n(5, 3) (5, 3)'],
 ['window attributes as arithmetic, a click inside a window and a title search', DESK + r"""class Window:
    def __init__(self, title, left, top, width, height):
        self.title, self.left, self.top, self.width, self.height = title, left, top, width, height
    right = property(lambda s: s.left + s.width); bottom = property(lambda s: s.top + s.height)
    topleft = property(lambda s: Point(s.left, s.top)); size = property(lambda s: Size(s.width, s.height))
    center = property(lambda s: Point(s.left + s.width // 2, s.top + s.height // 2))
    area = property(lambda s: s.width * s.height)
w = Window('Mu 1.0.1 - test1.py', 500, 300, 2070, 1208)
print(w.size, (w.left, w.top, w.right, w.bottom), w.topleft, w.center, w.area)
d = Desk(); d.click(w.left + 10, w.top + 20); print(tuple(d.pos))
w.width = 1000; print(w.right, w.size)
windows = [w, Window('Untitled - Notepad', 10, 10, 800, 600), Window('Notepad++', 0, 0, 300, 200)]
def with_title(text): return [x for x in windows if text in x.title]
print([x.title for x in with_title('Notepad')], with_title('Firefox'))
print([x.size for x in with_title('Notepad')])""", "Size(width=2070, height=1208) (500, 300, 2570, 1508) Point(x=500, y=300) Point(x=1535, y=904) 2500560\n(510, 320)\n1500 Size(width=1000, height=1208)\n['Untitled - Notepad', 'Notepad++'] []\n[Size(width=800, height=600), Size(width=300, height=200)]"],
 ['Looking Busy: the nudges, a corner start and a start at the left edge', DESK + r"""d = Desk(pos=(400, 300)); elapsed = 0; path = []
for i in range(6):
    d.move(-1 if i % 2 == 0 else 1, 0)
    elapsed += 10
    path.append((elapsed, d.pos.x))
print(path, d.pos.x == 400)
d = Desk(pos=(1, 0))
for i in range(6):
    try:
        d.move(-1 if i % 2 == 0 else 1, 0)
    except FailSafeException:
        print('the fail-safe stopped the nudging at step', i, 'with the pointer at', tuple(d.pos)); break
d = Desk(pos=(0, 300))
for i in range(4): d.move(-1 if i % 2 == 0 else 1, 0)
print(tuple(d.pos), len(d.log))""", '[(10, 399), (20, 400), (30, 399), (40, 400), (50, 399), (60, 400)] True\nthe fail-safe stopped the nudging at step 1 with the pointer at (0, 0)\n(1, 300) 3'],
 ['reading a text field with two hotkeys, and typing c and a without ctrl', DESK + r"""class TextApp:
    def __init__(self, text): self.text, self.selected, self.clipboard = text, False, ''
    def feed(self, log):
        held = []
        for kind, key in log:
            if kind == 'keydown':
                if key == 'ctrl': held.append(key)
                elif held and key == 'a': self.selected = True
                elif held and key == 'c' and self.selected: self.clipboard = self.text
            elif kind == 'keyup' and key in held: held.remove(key)
d = Desk(); app = TextApp('Text that is already in the field')
d.hotkey('ctrl', 'a'); d.hotkey('ctrl', 'c'); app.feed(d.log)
print(repr(app.clipboard))
d2 = Desk(); app2 = TextApp('not copied'); d2.write('ac'); app2.feed(d2.log); print(repr(app2.clipboard))""", "'Text that is already in the field'\n''"],
]
