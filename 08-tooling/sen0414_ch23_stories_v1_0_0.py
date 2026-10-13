"""SEN0414 chapter 23 - the story companion to the chapter corpus (version 1.0.0).

The owner's 5N1K rule: real, dated, sourced stories with one live link, enforced by this file's self-check. Six stories for
controlling the keyboard and mouse, written fresh for this chapter from Wikipedia pages opened on 2026-10-13 (the HTTP status each
link answered to a plain GET on that day is in LINK_STATUS, and `python3 sen0414_ch23_stories_v1_0_0.py links` asks again):

* Mouse1968 - Douglas Engelbart wrote of a "bug" on 14 November 1963, Bill English helped build the first prototype in 1964, and the mouse was shown in public on 9 December 1968 at The Mother of All Demos.
* XWindow1984 - Robert W. Scheifler announced "window system X" to the Project Athena community at MIT on 19 June 1984.
* Qwerty1874 - Sholes and Glidden's typewriter, sold by E. Remington and Sons from 1874, carries the layout that is still the de facto standard.
* Captcha2003 - the term CAPTCHA was coined in 2003 by Luis von Ahn, Manuel Blum, Nicholas J. Hopper and John Langford.
* DeadMan1918 - the Malbone Street Wreck of 1918 spurred the universal deployment of devices to halt trains when the operator is disabled.
* CutCopyPaste1974 - Larry Tesler and colleagues at Xerox PARC implemented editors with cut, copy and paste from 1974; Apple popularized them in 1983 and 1984.

Photograph: see ch23-page/stories_img_v1_0_0.json. The single request to Wikimedia Commons answered HTTP 429, so no photograph is used and nothing is claimed about licences.
Every sentence that says "In this study" was run on 2026-10-13 under Python 3.14 (uv) in /home/claude/venv314_ch23_latest (PyAutoGUI 0.9.54) on a virtual display (Xvfb), not a real screen.
Usage: import STORIES; run the file for self-checks, or with the argument links to ask every link again.
"""
__version__ = "1.0.0"

STORIES = [
    {
        "id": "Mouse1968",
        "title": "The mouse was shown in public on 9 December 1968",
        "when": "1968",
        "who": "Douglas Engelbart of the Stanford Research Institute, with Bill English, who helped build the first prototype in 1964",
        "where": "SRI's Augmentation Research Center; the public demonstration was The Mother of All Demos",
        "link": "https://en.wikipedia.org/wiki/Mouse_(computing)",
        "concepts": ["PositionTuple", "ClickSequence"],
        "story": ("Wikipedia's article on the computer mouse says that on 14 November 1963 Douglas Engelbart first recorded in his notebook a pointing device he called a \"bug\", and that Bill English helped him build the first prototype in 1964. "
                  "On 9 December 1968 Engelbart publicly demonstrated the mouse at what came to be known as The Mother of All Demos. "
                  "In this study a script that called pyautogui.click(10, 5) on a virtual display made the window under the pointer receive a ButtonPress and a ButtonRelease of button 1 at (10, 5), and position() returned a Point with the integer fields x and y."),
        "lesson": "A script now does what the first mouse did",
        "source": ("Wikipedia, 'Mouse (computing)' (Engelbart's notebook of 14 November 1963, the prototype of 1964, the demonstration of 9 December 1968), read 2026-10-13; "
                   "this study's leaves PositionTuple and ClickSequence."),
    },
    {
        "id": "XWindow1984",
        "title": "An email of 19 June 1984 introduced the window system X",
        "when": "1984",
        "who": "Robert W. Scheifler of the MIT Laboratory for Computer Science, writing to the Project Athena community",
        "where": "MIT; the message was sent to window@athena on Tuesday 19 June 1984",
        "link": "https://en.wikipedia.org/wiki/X_Window_System",
        "concepts": ["XTestEvents", "SyntheticVersusReal"],
        "story": ("Wikipedia's article on the X Window System reproduces the email in which Robert W. Scheifler wrote on 19 June 1984 that he had spent a couple of weeks writing a window system for the VS100, taken a fair amount of code from W, given it an asynchronous interface and called it X. "
                  "He wrote that its performance appeared to be about twice that of W. "
                  "In this study PyAutoGUI sent its keys to a window of that system through the XTEST extension and the window saw send_event as False, while a key sent with a SendEvent request arrived with send_event as True."),
        "lesson": "The X protocol still carries the clicks of scripts",
        "source": ("Wikipedia, 'X Window System' (the email of 19 June 1984 of Robert W. Scheifler), read 2026-10-13; "
                   "this study's leaves XTestEvents and SyntheticVersusReal."),
    },
    {
        "id": "Qwerty1874",
        "title": "The QWERTY layout was sold on a typewriter from 1874",
        "when": "1874",
        "who": "Christopher Latham Sholes, a newspaper editor and printer in Kenosha, Wisconsin, with Carlos Glidden, and E. Remington and Sons",
        "where": "Kenosha, Wisconsin, and the factory of E. Remington and Sons, which bought the manufacturing rights in 1873",
        "link": "https://en.wikipedia.org/wiki/QWERTY",
        "concepts": ["KeyboardLayout", "KeyTable"],
        "story": ("Wikipedia's article on QWERTY says the layout was devised in the early 1870s by Christopher Latham Sholes, that the manufacturing rights of the Sholes and Glidden Type-Writer were sold to E. Remington and Sons in 1873, and that the QWERTY design is based on the layout of the Sholes and Glidden typewriter sold by Remington from 1874. "
                  "It became popular with the Remington No. 2 of 1878 and is still a de facto standard on computers. "
                  "In this study write('zqay;') produced the same five characters under the us, de, tr and fr layouts of setxkbmap, and the table of key names held 194 entries."),
        "lesson": "A script types characters, not the keys of a layout",
        "source": ("Wikipedia, 'QWERTY' (Sholes, the sale to Remington in 1873, the typewriter sold from 1874, the Remington No. 2 of 1878), read 2026-10-13; "
                   "this study's leaves KeyboardLayout and KeyTable."),
    },
    {
        "id": "Captcha2003",
        "title": "The word CAPTCHA was coined in 2003 for a test that bots fail",
        "when": "2003",
        "who": "Luis von Ahn, Manuel Blum, Nicholas J. Hopper and John Langford",
        "where": "The term appeared in computing in 2003; the form with distorted letters was invented in 1997 by two groups working in parallel",
        "link": "https://en.wikipedia.org/wiki/CAPTCHA",
        "concepts": ["CaptchaEthics", "ScreenshotImage"],
        "story": ("Wikipedia's article on CAPTCHA says it is a challenge-response Turing test used in computing to determine whether the user is human in order to deter bot attacks and spam. "
                  "The term was coined in 2003 by Luis von Ahn, Manuel Blum, Nicholas J. Hopper and John Langford, as a contrived acronym for Completely Automated Public Turing test to tell Computers and Humans Apart. "
                  "In this study PyAutoGUI had no function with captcha or solve in its name, and screenshot() returned a 1920 by 1080 RGB image of a virtual display, so what a script reads from a screen is a picture."),
        "lesson": "A test made to stop scripts should not be scripted",
        "source": ("Wikipedia, 'CAPTCHA' (the term coined in 2003 by von Ahn, Blum, Hopper and Langford; the 1997 form), read 2026-10-13; "
                   "this study's leaves CaptchaEthics (the ethics part is not run) and ScreenshotImage."),
    },
    {
        "id": "DeadMan1918",
        "title": "A wreck in 1918 spurred train devices that stop without an operator",
        "when": "1918",
        "who": "The Brooklyn Rapid Transit system, whose train was wrecked at Malbone Street, and the operators of the New York City Subway",
        "where": "Brooklyn, New York City, on the Malbone Street line",
        "link": "https://en.wikipedia.org/wiki/Dead_man%27s_switch",
        "concepts": ["FailsafeCorners", "FailsafeFires"],
        "story": ("Wikipedia's article on the dead man's switch says it is designed to be activated or deactivated if the human operator becomes incapacitated, and that it is a form of fail-safe that stops a machine with no operator. "
                  "It says the Malbone Street Wreck on the Brooklyn Rapid Transit system in 1918, though not caused by driver incapacitation, did spur the need for universal deployment of such devices to halt trains in the event of the operator's disability. "
                  "In this study PyAutoGUI raised FailSafeException for a pointer in each of the four corners of a 1920 by 1080 screen and not at (1, 1), the one-pixel inset that is no corner."),
        "lesson": "The corner of the screen is a dead man's switch",
        "source": ("Wikipedia, 'Dead man's switch' (the definition, the use as a fail-safe, the Malbone Street Wreck of 1918), read 2026-10-13; "
                   "this study's leaves FailsafeCorners and FailsafeFires."),
    },
    {
        "id": "CutCopyPaste1974",
        "title": "Cut, copy and paste were implemented at Xerox PARC from 1974",
        "when": "1974",
        "who": "Lawrence G. Tesler and colleagues at Xerox PARC, and Apple Computer, which popularized the commands",
        "where": "Xerox PARC from 1974; the Apple Lisa of 1983 and the Macintosh of 1984",
        "link": "https://en.wikipedia.org/wiki/Cut,_copy,_and_paste",
        "concepts": ["ClipboardRoundTrip", "HotkeyOrder"],
        "story": ("Wikipedia's article on cut, copy and paste says Larry Tesler proposed the names cut and copy for the first step and paste for the second, and that beginning in 1974 he and colleagues at Xerox PARC implemented several text editors that used the commands. "
                  "Apple Computer popularized the paradigm with its Lisa in 1983 and Macintosh in 1984, mapping the functions to key combinations. "
                  "In this study a script pressed ctrl and a, then ctrl and c, in a window and pyperclip.paste() returned the two lines 'Hello, world!' and 'second line' through xclip."),
        "lesson": "Two key presses still move text between programs",
        "source": ("Wikipedia, 'Cut, copy, and paste' (Tesler and Xerox PARC from 1974; Apple Lisa 1983 and Macintosh 1984), read 2026-10-13; "
                   "this study's leaves ClipboardRoundTrip and HotkeyOrder."),
    },
]

LINK_STATUS = {'Mouse1968': 200, 'XWindow1984': 200, 'Qwerty1874': 200, 'Captcha2003': 200, 'DeadMan1918': 200, 'CutCopyPaste1974': 200}


def run_checks():
    bad = []
    ids = [x["id"] for x in STORIES]
    if len(ids) != len(set(ids)):
        bad.append("duplicate story ids")
    for x in STORIES:
        for f in ("who", "where", "link", "when", "title", "lesson", "source", "story"):
            if not str(x.get(f, "")).strip():
                bad.append("%s: missing %s (5N1K)" % (x["id"], f))
        if not x.get("link", "").startswith("http"):
            bad.append("%s: link is not a URL" % x["id"])
        if len(x["lesson"].split()) > 14:
            bad.append("%s: lesson over 14 words" % x["id"])
        if not (2 <= x["story"].count(". ") + 1 <= 7):
            bad.append("%s: story not 2-7 sentences" % x["id"])
        if LINK_STATUS and LINK_STATUS.get(x["id"]) != 200:
            bad.append("%s: link status %r, not 200" % (x["id"], LINK_STATUS.get(x["id"])))
        if not LINK_STATUS:
            bad.append("LINK_STATUS is empty")
    by = {x["id"]: x for x in STORIES}
    for sid, year in (("Mouse1968", "1968"), ("XWindow1984", "1984"), ("Qwerty1874", "1874"), ("Captcha2003", "2003"), ("DeadMan1918", "1918"), ("CutCopyPaste1974", "1974")):
        if year not in by[sid]["story"] and year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
        if year not in by[sid]["when"]:
            bad.append("%s: year %s not in when" % (sid, year))
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "sen0414-study/1.0 (altunel.yusuf@gmail.com)"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out[x["id"]] = r.status
        except urllib.error.HTTPError as e:
            out[x["id"]] = e.code
        except Exception as e:
            out[x["id"]] = type(e).__name__
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "links":
        print(ask_links())
    else:
        b = run_checks()
        print(len(STORIES), "stories; self-check failures:", len(b))
        for x in b:
            print("  ", x)
