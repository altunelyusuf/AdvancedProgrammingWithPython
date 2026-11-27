"""Chapter 23 deck content, version 4.0.0 (SEN0414, Lineage14): the words of the deck "Controlling the Keyboard and Mouse". Parts, plan, concept slides in plain words (no everyday comparison), stories,
the native table of quiet surprises that the run itself measured, take-aways, practice and resources.
Slide numbers of the plan: 1 title, 2 route, 3 questions, 4-9 part 1, 10-14 part 2, 15-21 part 3, 22-27 part 4, 28-34 part 5, 35 compare, 36 practice, 37 summary, 38 resources. The notes are in notes_v4_0_0.py."""
__version__ = "4.0.0"
import ast
import re

PARTS = {
    1: ("Part 1: The display, the session and the first input", "A script sends input to a display; without one, or under Wayland, it fails at once", [
        ("version", "PyAutoGUI is still below 1.0.0; the display answers size() and position()"),
        ("session", "No display, or a Wayland session, stops the script"),
        ("synthetic", "The window receives a real click; only the send_event flag differs")]),
    2: ("Part 2: Pauses and fail-safes", "PAUSE slows every acting call; the four corners stop a runaway script", [
        ("PAUSE", "A wait after calls that act, none after calls that only ask"),
        ("corners", "A corner raises FailSafeException; one pixel in does not")]),
    3: ("Part 3: Moving, clicking, dragging, scrolling", "Each mouse call has a printed effect: steps, buttons, a drawing, lines", [
        ("moveTo", "Duration decides how many small steps a move takes"),
        ("click", "Each call sends its own button events"),
        ("drag", "A spiral of relative drags, drawn by the window"),
        ("scroll", "One click moves a different number of lines under Tk 9 and Tk 8.6")]),
    4: ("Part 4: The screen: pictures and finding a button", "A screenshot is a picture; searching it works only on an exact match", [
        ("screenshot", "A Pillow image of the whole display; pixel() reads one point"),
        ("locate", "locateOnScreen() returns a box; locateAll finds twins"),
        ("match", "One pixel off, and nothing is found")]),
    5: ("Part 5: The keyboard and the clipboard", "write() types characters; a wrong key name is skipped without an error", [
        ("write", "A str is typed; a list may hold key names"),
        ("names", "A wrong key name raises nothing and types nothing"),
        ("hotkey", "Keys go down in order and up in reverse; the clipboard carries text")]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("story", "xwindow"), ("code", "pins"), ("code", "session"), ("code", "xtest"),
        ("divider", 2), ("analogy", "A2"), ("story", "deadman"), ("code", "pause"), ("code", "corners"),
        ("divider", 3), ("analogy", "A3"), ("analogy", "A3b"), ("story", "mouse"), ("code", "move"), ("code", "click"), ("code", "drag"), ("code", "scroll"),
        ("divider", 4), ("analogy", "A4"), ("analogy", "A4b"), ("story", "captcha"), ("code", "shot"), ("code", "locate"), ("code", "match"),
        ("divider", 5), ("analogy", "A5"), ("analogy", "A5b"), ("story", "qwerty"), ("code", "type"), ("code", "keys"), ("story", "ctrlaltdel"), ("code", "clip"),
        ("compare", "quiet"), ("practice",), ("summary",), ("resources",)]

ROUTE_RUNS = {1: "version, session, synthetic input", 2: "PAUSE, corners", 3: "move, click, drag, scroll", 4: "screenshot, locate, match", 5: "write, key names, hotkey and clipboard"}
ROUTE_TAIL = ("Summary and links", "what to remember, where next")

QUESTIONS = [
    ("1", "How does a script's click reach a window, and what stops a script that has gone wrong?", "Parts 1 and 2 answer it; the summary repeats it on slide %d.", "summary"),
    ("2", "Which calls fail quietly, with no error and no effect, and how can a script notice?", "The table of quiet surprises is on slide %d; check yourself with the questions on slide %d.", [("compare", "quiet"), ("practice",)]),
]
QUESTIONS_TAKEAWAY = "Every example runs on the chapter page; read its printed result first."

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "What it is and does"
CONCEPTS_TAIL = "each explained in plain words"
ANALOGIES = [
    ("A1", "Installing, the display and the session", "pyautogui sends input to a display; macOS needs permission, Wayland refuses, and without a display nothing starts.", [
        ("Setting Up Accessibility Apps on macOS", "macOS needs the user to allow the program in the accessibility settings."),
        ("Logouts", "A script has no display to control while the user is logged out."),
        ("Setting Up GUI Automation Scripts", "Pin the versions, keep the screen as it was, and keep a way to stop."),
        ("pyautogui", "The third-party module that controls the mouse, the keyboard and the screen."),
        ("PyAutoGUI", "The package name for pip; importlib.metadata reads its version."),
        ("Selenium", "A separate package that controls a browser, not through the mouse."),
        ("logging", "The standard module that records what a script did."),
        ("Staying on Track", "Input goes to the active window, so the right window must be active."),
        ("pyautogui.size()", "Returns the width and height of the screen in pixels."),
        ("Figure 23-1: the coordinates of a computer screen with 1920x1080 resolution", "The origin is the top left corner; x grows to the right and y grows downward."),
        ("Figure 23-4: the scale display settings in Windows and macOS", "A scale above 100 percent changes the numbers; check the scale."),
    ]),
    ("A2", "Pauses and fail-safes protect a running script", "A pause follows each acting call, and a pointer in a corner of the screen raises an exception that stops the script.", [
        ("Pauses and Fail-Safes", "Two safeguards: a pause after each call, and a stop when the pointer reaches a corner."),
        ("pyautogui.PAUSE", "The number of seconds that pyautogui waits after most calls; the default is 0.1."),
        ("pyautogui.FailSafeException", "The exception that is raised when the pointer is in a corner of the screen."),
        ("pyautogui.sleep()", "Waits for a number of seconds; it is the same as time.sleep()."),
        ("pyautogui.countdown()", "Waits and prints the seconds that are left, so a person can get ready."),
        ("Practice Program: Looking Busy", "A program that moves the pointer a little at intervals so that the computer does not count the user as idle."),
    ]),
    ("A3", "The mouse: ideas and calls", "moveTo() and move() set the pointer, click() presses buttons, drag() moves with a button held down, and scroll() turns the wheel.", [
        ("Controlling Mouse Movement", "The group of calls that move the pointer by absolute or relative coordinates."),
        ("Moving the Mouse", "moveTo() goes to a point of the screen; move() goes by a distance from where the pointer is."),
        ("Getting the Current Position", "position() returns the x and y of the pointer."),
        ("Controlling Mouse Interaction", "The group of calls that press buttons, drag and scroll."),
        ("Clicking", "click() sends a press and a release; doubleClick() and tripleClick() send them close together."),
        ("Dragging", "drag() and dragTo() move the pointer while the left button is held down."),
        ("Scrolling", "scroll() turns the wheel; a positive number goes up and a negative number goes down."),
        ("Planning Your Mouse Movements", "Find the coordinates first, for example with MouseInfo, then write the calls."),
        ("pyautogui.moveTo()", "Moves the pointer to x and y; duration spreads the move over time."),
        ("pyautogui.move()", "Moves the pointer by an offset from its present position."),
        ("pyautogui.position()", "Returns the pointer position as a named tuple with x and y."),
    ]),
    ("A3b", "The mouse: calls, figures and options", "The remaining mouse calls, the two figures, the book's spiral program and the arguments duration and button.", [
        ("pyautogui.click()", "Clicks at the pointer or at given coordinates; button and clicks change it."),
        ("pyautogui.dragTo()", "Drags to an absolute point."),
        ("pyautogui.drag()", "Drags by an offset from the present position."),
        ("pyautogui.scroll()", "Turns the wheel by a number of clicks."),
        ("pyautogui.mouseInfo()", "Opens MouseInfo, which shows position and pixel color; it needs Tk."),
        ("MouseInfo", "A small program that shows where the pointer is and what color is under it."),
        ("Figure 23-2: the results from the pyautogui.drag() example, drawn with MS Paint brushes", "The spiral of the example, drawn by a paint program that received the drags."),
        ("Figure 23-3: the MouseInfo application window", "The window with the position, the color and the buttons that copy them."),
        ("spiralDraw.py", "The book's program that draws a square spiral with drag()."),
        ("duration", "The seconds that a move or a drag takes; with 0 the pointer jumps."),
        ("button='left'", "The argument that names the mouse button; 'middle' and 'right' are the others."),
    ]),
    ("A4", "The screen: pictures, pixels and image search", "screenshot() returns a picture, pixel() reads one point, locateOnScreen() searches for a picture, and window objects exist only on Windows.", [
        ("Taking Screenshots", "screenshot() returns the screen as a Pillow image."),
        ("Image Recognition", "locateOnScreen() searches the screen for a small picture and returns where it found it."),
        ("pyautogui.screenshot()", "Returns a picture of the whole screen; a file name saves it."),
        ("pyautogui.pixel()", "Returns the color of one point as red, green and blue."),
        ("pyautogui.pixelMatchesColor()", "Tells whether a point has a color; tolerance allows a small difference."),
        ("pyautogui.locateOnScreen()", "Returns the box of the first match of a picture on the screen."),
        ("pyautogui.locateAllOnScreen()", "Returns every match as a box."),
        ("pyautogui.ImageNotFoundException", "The exception that newer versions raise when no match is found; older ones return None."),
        ("submit.png", "The book's picture of a button that the script searches for."),
    ]),
    ("A4b", "The screen: windows and the book's pictures", "Window objects hold the title, position and size of a window; they work on Windows only.", [
        ("screenshot.png", "The book's name for a saved screenshot."),
        ("Getting Window Information", "Window objects hold the title, the position and the size of a window."),
        ("Obtaining the Active Window", "getActiveWindow() returns the window that has the focus."),
        ("Finding Windows with Other Functions", "getWindowsWithTitle() returns the windows whose title contains a text."),
        ("Manipulating Windows", "A window object can be moved, resized, minimized and closed."),
        ("pyautogui.getActiveWindow()", "Returns the active window; it works on Windows only."),
        ("pyautogui.getWindowsWithTitle()", "Returns the windows with a title; it works on Windows only."),
        ("Figure 23-5: the Mu Editor window before and after using the Window object attributes", "The editor window before and after its position and size were changed by a script."),
    ]),
    ("A5", "The keyboard: typing, keys and hotkeys", "write() types text, press() and keyDown() send keys by name, hotkey() sends a combination, and pyperclip reads the clipboard.", [
        ("Controlling the Keyboard", "The group of calls that type text and press keys."),
        ("Sending Key Press Strings", "write() types the characters of a str, one after the other."),
        ("Specifying Key Names", "press() takes a key name; the names are in pyautogui.KEYBOARD_KEYS."),
        ("Pressing and Releasing the Keyboard", "keyDown() holds a key and keyUp() lets it go."),
        ("Running Hotkey Combinations", "hotkey() holds the first keys down, presses the last, and lets go in reverse order."),
        ("Displaying Message Boxes", "alert(), confirm(), prompt() and password() show a box and return the answer of the user."),
        ("pyautogui.write()", "Types a str, or a list of characters and key names."),
        ("pyautogui.press()", "Presses and releases one key by name."),
        ("pyautogui.keyDown()", "Presses a key and keeps it down."),
        ("pyautogui.hotkey()", "Presses a combination such as ctrl and c."),
        ("pyautogui.alert()", "Shows a message with an OK button."),
        ("pyautogui.confirm()", "Shows a message with buttons and returns the text of the button that was chosen."),
    ]),
    ("A5b", "Message boxes, the clipboard and practice programs", "The message box calls, the helper modules, the key name list and the two practice programs.", [
        ("Figure 23-6: using PyAutoGUI to click the file editor window and enter Hello, world!", "A click on the editor window, then write() types the text."),
        ("pyautogui.prompt()", "Asks for a text and returns it."),
        ("pyautogui.password()", "Asks for a text and hides the characters that are typed."),
        ("pyperclip", "The third-party module that copies to the clipboard and reads from it."),
        ("PyMsgBox", "The package that pyautogui uses for its message boxes."),
        ("pyautogui.KEYBOARD_KEYS", "The list of key names that press() accepts."),
        ("Table 23-1: string values for keyboard keys", "The key names that can be passed to press(), such as 'enter' and 'f1'."),
        ("Practice Program: Reading Text Fields with the Clipboard", "Select all, copy, and read the text with pyperclip."),
        ("Practice Program: Writing a Game-Playing Bot", "A bot that finds a picture on the screen and clicks it again and again."),
    ]),
]

STORIES = {
    "xwindow": dict(
        title="Story: An email of 19 June 1984 introduced the window system X", img="image_xwindow.png",
        prose=["On 19 June 1984 Robert W. Scheifler wrote that he had spent a couple of weeks writing a window system for the VS100 and called it X.",
               "He wrote that its performance appeared to be about twice that of W, from which he had taken a fair amount of code.",
               "The picture shows a desktop of X. PyAutoGUI in this chapter sends its clicks and keys to such a display."],
        linktext="X Window System (Wikipedia)", link="https://en.wikipedia.org/wiki/X_Window_System"),
    "deadman": dict(
        title="Story: A wreck in 1918 spurred train devices that stop without an operator", img="image_sifa.jpg",
        prose=["A dead man's switch stops a machine when its operator can no longer operate it.",
               "The Malbone Street Wreck of 1918 on the Brooklyn Rapid Transit system did not come from a driver's illness, yet it spurred the use of such devices on trains.",
               "The picture shows the pedal of a German train safety system. The corner of the screen is the same idea for a script."],
        linktext="Dead man's switch (Wikipedia)", link="https://en.wikipedia.org/wiki/Dead_man%27s_switch"),
    "mouse": dict(
        title="Story: The mouse was shown in public on 9 December 1968", img="image_mouse.jpg",
        prose=["On 14 November 1963 Douglas Engelbart wrote in his notebook about a pointing device that he called a bug.",
               "Bill English helped him build the first prototype in 1964, and Engelbart showed it in public on 9 December 1968.",
               "The picture shows a prototype of the mouse. moveTo() and click() do in a script what that device did for a hand."],
        linktext="Mouse (Wikipedia)", link="https://en.wikipedia.org/wiki/Mouse_(computing)"),
    "captcha": dict(
        title="Story: The word CAPTCHA was coined in 2003 for a test that bots fail", img="image_captcha.png",
        prose=["Luis von Ahn, Manuel Blum, Nicholas Hopper and John Langford coined the word CAPTCHA in 2003.",
               "It stands for a test that tells computers and humans apart, and its aim is to deter bot attacks and spam.",
               "The picture is such a test. A script that takes a screenshot only gets a picture, as part 4 shows."],
        linktext="CAPTCHA (Wikipedia)", link="https://en.wikipedia.org/wiki/CAPTCHA"),
    "qwerty": dict(
        title="Story: The QWERTY layout was sold on a typewriter from 1874", img="image_qwerty.jpg",
        prose=["Christopher Latham Sholes devised the QWERTY layout in the early 1870s.",
               "E. Remington and Sons bought the manufacturing rights of the Sholes and Glidden typewriter in 1873 and sold it from 1874.",
               "The picture shows that machine. write() types characters, and press() takes names such as 'enter', not positions on a layout."],
        linktext="QWERTY (Wikipedia)", link="https://en.wikipedia.org/wiki/QWERTY"),
    "ctrlaltdel": dict(
        title="Story: Control-Alt-Delete was devised in 1981 to restart a computer without switching it off", img="image_ibm5150.jpg",
        prose=["David Bradley, chief engineer of the IBM PC project, devised a keyboard command in 1981 that restarted the computer without switching it off.",
               "His first choice was too easy to bump, so Mel Hallerman suggested Control, Alt and Delete, which the first keyboard made hard to press with one hand.",
               "The picture shows that keyboard. hotkey() presses such a combination: the keys go down in order and come up in reverse."],
        linktext="Control-Alt-Delete (Wikipedia)", link="https://en.wikipedia.org/wiki/Control-Alt-Delete"),
}


def _measure():
    """measure the quiet surprises with the real PyAutoGUI on a private display (the same helpers as the examples)"""
    import os
    here = os.getcwd()
    import lab23_v1_0_0 as L
    d = L.begin(wm=True)
    import pyautogui
    pyautogui.PAUSE = 0
    w = d.observer(mode="text", geometry="600x300+100+100", focus="text")
    L.time.sleep(0.5)
    pyautogui.click(300, 250)
    L.time.sleep(0.3)
    pyautogui.press("nokey")
    nokey = w.text()
    pyautogui.write("café")
    cafe = w.text()
    w.close()
    d = L.begin(wm=False)
    import pyautogui as p2
    p2.PAUSE = 0
    b = d.observer(mode="button", geometry="400x300+200+150", bg="#00aa00", buttons=[[100, 100]])
    L.time.sleep(0.5)
    bx, by, bw, bh = b.state()["buttons"][0]
    btn = p2.screenshot().crop((bx, by, bx + bw, by + bh))
    btn.save("exact.png")
    btn.putpixel((5, 5), (0, 0, 0))
    btn.save("off.png")
    probe = "import pyautogui as p\ntry: print(type(p.locateOnScreen(%s)).__name__)\nexcept Exception as e: print(type(e).__name__)"
    exact = L.child(probe % "'exact.png'", env=d.env)[1][0]
    off = L.child(probe % "'off.png'", env=d.env)[1][0]
    b.close()
    L.end()
    os.chdir(here)
    return nokey, cafe, exact, off


_NOKEY, _CAFE, _EXACT, _OFF = _measure()
COMPARES = {
    "quiet": dict(
        title="Four quiet surprises, measured by the run", sub="Nothing was raised in the first two rows; check the effect, not the call",
        colw=[2.4, 2.4, 2.6, 2.6], rowh=0.5, fs=11,
        rows=[["Call", "An error?", "What reached the window or screen", "What to do"],
              ["press('nokey')", "none", "typed %r" % _NOKEY, "check the key name in KEYBOARD_KEYS"],
              ["write('café')", "none", "typed %r" % _CAFE, "read the text back and compare"],
              ["locateOnScreen, exact picture", "none", "returned a %s" % _EXACT, "keep the picture exact"],
              ["locateOnScreen, one pixel off", "an exception", "raised %s" % _OFF, "use confidence= with OpenCV"]],
        takeaway="Two calls do nothing and say nothing; the other two answer, so catch the answer."),
}

TAKEAWAY = {
    "pins": "Print the versions; pyautogui is below 1.0.0 and the display answers.",
    "session": "No DISPLAY or a Wayland session stops the script at once.",
    "xtest": "The window receives a real click; only send_event differs.",
    "pause": "PAUSE follows the calls that act, not the calls that ask.",
    "corners": "A corner raises FailSafeException; (1, 1) does not.",
    "move": "More duration, more steps; outside targets are cut to the screen.",
    "click": "Each click call sends its own button events.",
    "drag": "drag() is relative: the spiral shrinks by 20 pixels per side.",
    "scroll": "One click moves more lines under Tk 8.6 than under Tk 9.",
    "shot": "The screenshot is a picture; pixel() needs x and y.",
    "locate": "locateOnScreen() returns a box; click() takes a box.",
    "match": "One pixel off, and an exact search finds nothing.",
    "type": "write() types a str; a list may hold key names.",
    "keys": "A wrong key name, and the letter é, are skipped without an error.",
    "clip": "hotkey() presses down in order and releases in reverse.",
}

SUMMARY_ANALOGY = "Four claims: the display decides, the corners stop, pictures must match, quiet calls need a check."
SUMMARY_POINTS = [
    "pyautogui sends real input to a display; without a display, or under Wayland, it stops at once.",
    "PAUSE follows the calls that act; a pointer in a corner raises FailSafeException.",
    "A screenshot is a picture; locateOnScreen() needs an exact match or OpenCV and confidence.",
    "A wrong key name and some characters are skipped silently; read back what arrived.",
]
SUMMARY_TAKEAWAY = "Two questions of slide 3: how a click arrives, what stops a script, what fails quietly."

PRACTICE_SUB = "Use the slide of the part named in each question"
PRACTICE_ANALOGY = "Each practice question has a short answer; run the code on the chapter page to check it."
PRACTICE = [
    "What does the script need before pyautogui can be imported, and what does a Wayland session do to screenshot()? Use part 1.",
    "Which four points raise FailSafeException, and why does a script that was started before a resize keep its old corners? Use part 2.",
    "How does the number of motion events change with duration, and which call sends a press and a double click? Use part 3.",
    "Why does locateOnScreen() find nothing when one pixel differs, and what do confidence and OpenCV change? Use part 4.",
    "What happens when press() gets a name that does not exist, and in which order does hotkey() release its keys? Use part 5.",
]
PRACTICE_TAKEAWAY = "Run the examples on the chapter page to check each answer."

RESOURCES_SUB = "The chapter, the documentation, and the pages behind the stories"
RESOURCES_TAKEAWAY = "Opened on 2026-11-27; the GitHub page could not be opened from here."
RESOURCES_ROWS = 8
RESOURCES = [
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 23", "https://automatetheboringstuff.com/3e/chapter23.html", "automatetheboringstuff.com"),
    ("PyAutoGUI documentation", "https://pyautogui.readthedocs.io/en/latest/", "pyautogui.readthedocs.io"),
    ("PyAutoGUI on GitHub", "https://github.com/asweigart/pyautogui", "github.com"),
    ("PyAutoGUI on PyPI", "https://pypi.org/pypi/pyautogui/json", "pypi.org"),
    ("PyAutoGUI: mouse functions", "https://pyautogui.readthedocs.io/en/latest/mouse.html", "pyautogui.readthedocs.io"),
    ("PyAutoGUI: keyboard functions", "https://pyautogui.readthedocs.io/en/latest/keyboard.html", "pyautogui.readthedocs.io"),
    ("PyAutoGUI: screenshot functions", "https://pyautogui.readthedocs.io/en/latest/screenshot.html", "pyautogui.readthedocs.io"),
    ("pyperclip on PyPI", "https://pypi.org/pypi/pyperclip/json", "pypi.org"),
    ("X Window System (Wikipedia)", "https://en.wikipedia.org/wiki/X_Window_System", "en.wikipedia.org"),
    ("Dead man's switch (Wikipedia)", "https://en.wikipedia.org/wiki/Dead_man%27s_switch", "en.wikipedia.org"),
    ("Mouse (Wikipedia)", "https://en.wikipedia.org/wiki/Mouse_(computing)", "en.wikipedia.org"),
    ("CAPTCHA (Wikipedia)", "https://en.wikipedia.org/wiki/CAPTCHA", "en.wikipedia.org"),
    ("QWERTY (Wikipedia)", "https://en.wikipedia.org/wiki/QWERTY", "en.wikipedia.org"),
    ("Control-Alt-Delete (Wikipedia)", "https://en.wikipedia.org/wiki/Control-Alt-Delete", "en.wikipedia.org"),
]
