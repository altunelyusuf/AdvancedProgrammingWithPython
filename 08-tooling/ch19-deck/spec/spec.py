"""Chapter 19 deck spec for the generic builder 08-tooling/chapter_deck_build_v2_1_0.py (deck 2.0.0 of chapter 19, built from the owner-approved draft DRAFT_ch19_v1_0_1... v1.0.0)."""
import hashlib
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import examples_v2_0_0 as X
import visuals_v2_0_0 as V
import content_v2_0_0 as T

CH = 19
OUT_DECK = "03-materials/ch19/SEN0414_Ch19_TimeScheduling_3e_v2_0_0.pptx"
OUT_MAN = "03-materials/ch19/page/chapter_code_ch19_v1_0_0.json"
IMAGE_FILES = ["story_images_v1_0_0.json"]
TITLE = "Chapter 19: Time, Scheduling and Launching Programs"
SUBTITLE = "Keeping time, scheduling tasks and launching programs: the time and datetime modules, subprocess, cron"
CORE_TITLE = "SEN0414 Chapter 19: Keeping Time, Scheduling Tasks and Launching Programs"
_ASSETS = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "03-materials", "ch19", "assets"))
WHEELS = {w: hashlib.sha256(open(os.path.join(_ASSETS, w), "rb").read()).hexdigest() for w in sorted(os.listdir(_ASSETS)) if w.endswith(".whl")}
MANIFEST_VERSION = "1.0.0"
MANIFEST_ABOUT = ("The code examples of the chapter 19 deck, in the order of the code slides (order = slide order). Every example is self-contained, uses the Python standard library "
                  "(time, calendar, datetime, zoneinfo, subprocess, shlex, sched) and runs offline, reads no keyboard and opens no window. Waiting is replaced by a stand-in "
                  "clock (a list holding a number) where a real wait would be slow or machine-dependent; the slide says so. The child programs of the subprocess examples are Python "
                  "itself (sys.executable) or the commands sleep, false and echo. The schedule package, playsound3 and pyperclip of the book are not used by the examples: the "
                  "scheduling slide uses the standard library, and the countdown stands in for the alarm. The page's time zone data is the tzdata wheel of the assets.")
LIBRARIES = "standard library only (zoneinfo reads tzdata 2026.5 or the system copy)"
PAGE_REQUIREMENTS = ["the standard library modules time, calendar, datetime, zoneinfo, subprocess, shlex, and sched, and the built-ins print, len, range, round, repr, type, str, int, float, sorted, list, tuple, isinstance",
                     "the tzdata wheel (03-materials/ch19/assets/tzdata-2026.5-py2.py3-none-any.whl) that the page embeds, for zoneinfo",
                     "the subprocess examples start sys.executable and the commands sleep, false and echo; in the browser's Python (Pyodide) there is no subprocess, so the page runs the four subprocess examples as recorded stand-ins and the chapter-code tab says which (the page's standin_v1_0_0.json and limits_v1_0_0.json)"]
