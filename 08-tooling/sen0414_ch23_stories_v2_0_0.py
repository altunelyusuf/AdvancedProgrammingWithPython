"""SEN0414 chapter 23 - the story companion to the chapter corpus (version 2.0.0, over 1.0.0).

Six real, dated, sourced stories, one live link each, checked by this file's own run_checks(). Version 2.0.0 carries the story text of the lecture deck
4.0.0 of chapter 23 (SEN0414_Ch23_KeyboardAndMouse_3e_v4_0_0.pptx), so the page and the deck tell the same story; the who, where, lesson and concept
links of version 1.0.0 are kept. LINK_STATUS is the HTTP status that each link answered to a plain GET on 2026-11-27 with the identifying agent
"SEN0414-course-materials/1.0 (course materials; contact via GitHub altunelyusuf)"; `python3 sen0414_ch23_stories_v2_0_0.py links` asks again.
Pictures: see ch23-page/stories_img_v9_110_0.json and 03-materials/ch23/assets/story_images_v1_0_0.json (files, licences, credits).
Usage: import STORIES; run the file for the self-check, or with the argument links to ask every link again.
"""
__version__ = "2.0.0"

STORIES = [{'id': 'XWindow1984',
  'title': 'An email of 19 June 1984 introduced the window system X',
  'when': '1984',
  'who': 'Robert W. Scheifler of the MIT Laboratory for Computer Science, writing to the Project Athena community',
  'where': 'MIT; the message was sent to window@athena on Tuesday 19 June 1984',
  'link': 'https://en.wikipedia.org/wiki/X_Window_System',
  'concepts': ['XTestEvents', 'SyntheticVersusReal'],
  'story': 'On 19 June 1984 Robert W. Scheifler wrote that he had spent a couple of weeks writing a window system for the VS100 and called it X. He '
           'wrote that its performance appeared to be about twice that of W, from which he had taken a fair amount of code. The picture shows a '
           'desktop of X. PyAutoGUI in this chapter sends its clicks and keys to such a display.',
  'lesson': 'The X protocol still carries the clicks of scripts',
  'source': "Wikipedia, 'X Window System' (the email of 19 June 1984 of Robert W. Scheifler), read 2026-11-27; this study's leaves XTestEvents and "
            'SyntheticVersusReal.'},
 {'id': 'DeadMan1918',
  'title': 'A wreck in 1918 spurred train devices that stop without an operator',
  'when': '1918',
  'who': 'The Brooklyn Rapid Transit system, whose train was wrecked at Malbone Street, and the operators of the New York City Subway',
  'where': 'Brooklyn, New York City, on the Malbone Street line',
  'link': 'https://en.wikipedia.org/wiki/Dead_man%27s_switch',
  'concepts': ['FailsafeCorners', 'FailsafeFires'],
  'story': "A dead man's switch stops a machine when its operator can no longer operate it. The Malbone Street Wreck of 1918 on the Brooklyn Rapid "
           "Transit system did not come from a driver's illness, yet it spurred the use of such devices on trains. The picture shows the pedal of a "
           'German train safety system. The corner of the screen is the same idea for a script.',
  'lesson': "The corner of the screen is a dead man's switch",
  'source': "Wikipedia, 'Dead man's switch' (the definition, the use as a fail-safe, the Malbone Street Wreck of 1918), read 2026-11-27; this "
            "study's leaves FailsafeCorners and FailsafeFires."},
 {'id': 'Mouse1968',
  'title': 'The mouse was shown in public on 9 December 1968',
  'when': '1968',
  'who': 'Douglas Engelbart of the Stanford Research Institute, with Bill English, who helped build the first prototype in 1964',
  'where': "SRI's Augmentation Research Center; the public demonstration was The Mother of All Demos",
  'link': 'https://en.wikipedia.org/wiki/Mouse_(computing)',
  'concepts': ['PositionTuple', 'ClickSequence'],
  'story': 'On 14 November 1963 Douglas Engelbart wrote in his notebook about a pointing device that he called a bug. Bill English helped him build '
           'the first prototype in 1964, and Engelbart showed it in public on 9 December 1968. The picture shows a prototype of the mouse. moveTo() '
           'and click() do in a script what that device did for a hand.',
  'lesson': 'A script now does what the first mouse did',
  'source': "Wikipedia, 'Mouse (computing)' (Engelbart's notebook of 14 November 1963, the prototype of 1964, the demonstration of 9 December 1968), "
            "read 2026-11-27; this study's leaves PositionTuple and ClickSequence."},
 {'id': 'Captcha2003',
  'title': 'The word CAPTCHA was coined in 2003 for a test that bots fail',
  'when': '2003',
  'who': 'Luis von Ahn, Manuel Blum, Nicholas J. Hopper and John Langford',
  'where': 'The term appeared in computing in 2003; the form with distorted letters was invented in 1997 by two groups working in parallel',
  'link': 'https://en.wikipedia.org/wiki/CAPTCHA',
  'concepts': ['CaptchaEthics', 'ScreenshotImage'],
  'story': 'Luis von Ahn, Manuel Blum, Nicholas Hopper and John Langford coined the word CAPTCHA in 2003. It stands for a test that tells computers '
           'and humans apart, and its aim is to deter bot attacks and spam. The picture is such a test. A script that takes a screenshot only gets a '
           'picture, as part 4 shows.',
  'lesson': 'A test made to stop scripts should not be scripted',
  'source': "Wikipedia, 'CAPTCHA' (the term coined in 2003 by von Ahn, Blum, Hopper and Langford; the 1997 form), read 2026-11-27; this study's "
            'leaves CaptchaEthics (the ethics part is not run) and ScreenshotImage.'},
 {'id': 'Qwerty1874',
  'title': 'The QWERTY layout was sold on a typewriter from 1874',
  'when': '1874',
  'who': 'Christopher Latham Sholes, a newspaper editor and printer in Kenosha, Wisconsin, with Carlos Glidden, and E. Remington and Sons',
  'where': 'Kenosha, Wisconsin, and the factory of E. Remington and Sons, which bought the manufacturing rights in 1873',
  'link': 'https://en.wikipedia.org/wiki/QWERTY',
  'concepts': ['KeyboardLayout', 'KeyTable'],
  'story': 'Christopher Latham Sholes devised the QWERTY layout in the early 1870s. E. Remington and Sons bought the manufacturing rights of the '
           'Sholes and Glidden typewriter in 1873 and sold it from 1874. The picture shows that machine. write() types characters, and press() takes '
           "names such as 'enter', not positions on a layout.",
  'lesson': 'A script types characters, not the keys of a layout',
  'source': "Wikipedia, 'QWERTY' (Sholes, the sale to Remington in 1873, the typewriter sold from 1874, the Remington No. 2 of 1878), read "
            "2026-11-27; this study's leaves KeyboardLayout and KeyTable."},
 {'id': 'CtrlAltDel1981',
  'title': 'Control-Alt-Delete was devised in 1981 to restart a computer without switching it off',
  'when': '1981',
  'who': 'David Bradley, chief engineer of the IBM PC project, and Mel Hallerman, its chief programmer',
  'where': 'IBM at Boca Raton, Florida; the command was invented in 1981 for people who wrote programs',
  'link': 'https://en.wikipedia.org/wiki/Control-Alt-Delete',
  'concepts': ['ClipboardRoundTrip', 'HotkeyOrder'],
  'story': 'David Bradley, chief engineer of the IBM PC project, devised a keyboard command in 1981 that restarted the computer without switching it '
           'off. His first choice was too easy to bump, so Mel Hallerman suggested Control, Alt and Delete, which the first keyboard made hard to '
           'press with one hand. The picture shows that keyboard. hotkey() presses such a combination: the keys go down in order and come up in '
           'reverse.',
  'lesson': 'Keys held together are one command',
  'source': "Wikipedia, 'Control-Alt-Delete' (Bradley and Hallerman, the choice of the combination, 1981 in Boca Raton), read 2026-11-27; this "
            "study's leaves ClipboardRoundTrip and HotkeyOrder."}]

LINK_STATUS = {'Mouse1968': 200, 'XWindow1984': 200, 'Qwerty1874': 200, 'Captcha2003': 200, 'DeadMan1918': 200, 'CtrlAltDel1981': 200}


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
        if LINK_STATUS.get(x["id"]) != 200:
            bad.append("%s: link status %r, not 200" % (x["id"], LINK_STATUS.get(x["id"])))
    by = {x["id"]: x for x in STORIES}
    for sid, year in (("Mouse1968", "1968"), ("XWindow1984", "1984"), ("Qwerty1874", "1874"), ("Captcha2003", "2003"), ("DeadMan1918", "1918"), ("CtrlAltDel1981", "1981")):
        if year not in by[sid]["story"] and year not in by[sid]["when"]:
            bad.append("%s: date missing from story" % sid)
        if year not in by[sid]["when"]:
            bad.append("%s: year %s not in when" % (sid, year))
    return bad


def ask_links():
    import urllib.request, urllib.error
    out = {}
    for x in STORIES:
        req = urllib.request.Request(x["link"], headers={"User-Agent": "SEN0414-course-materials/1.0 (course materials; contact via GitHub altunelyusuf)"})
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
