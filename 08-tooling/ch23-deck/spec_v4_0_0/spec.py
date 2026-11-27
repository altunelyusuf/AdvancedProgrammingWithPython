"""Chapter 23 deck spec 4.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_10_0.py (Lineage14, SEN0414). It makes the new lecture deck 4.0.0 of chapter 23 (Controlling the Keyboard and Mouse) in the shape of chapters 12 to 21: parts, concept slides in plain words,
sourced story pictures, one code slide for each of 15 examples with two result balloons, a native table of measured limits, practice, summary and resources. The first-version deck stays as it was."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import examples_v1_0_0 as X
import visuals_v4_0_0 as V
import content_v4_0_0 as T0
import notes_v4_0_0 as N0


class _T:
    """the content words with the notes of this version"""
    NOTES = N0.NOTES
    STORY_NOTES = N0.STORY_NOTES
    RESULT_SAYS = N0.RESULT_SAYS

    def __getattr__(self, k):
        return getattr(T0, k)


T = _T()

CH = 23
OUT_DECK = "03-materials/ch23/SEN0414_Ch23_KeyboardAndMouse_3e_v4_0_0.pptx"
OUT_MAN = "03-materials/ch23/page/chapter_code_ch23_v1_0_0.json"
IMAGE_FILES = ["story_images_v1_0_0.json"]
TITLE = "Chapter 23: Controlling the Keyboard and Mouse"
SUBTITLE = "PyAutoGUI on a display; pauses and fail-safes; the mouse; the screen and pictures; the keyboard and the clipboard"
CORE_TITLE = "SEN0414 Chapter 23: Controlling the Keyboard and Mouse (lecture deck 4.0.0)"
WHEELS = {}
MANIFEST_VERSION = "1.0.0"
MANIFEST_ABOUT = ("The code examples of the chapter 23 deck, in the order of the code slides (order = slide order). Every example ran the real PyAutoGUI 0.9.54 on a private virtual X display (Xvfb, with the window manager openbox where needed) "
                  "on which a small Tk window logs every event it receives; nobody saw that display and nothing was sent to a real screen. The lines that start the display and the window are hidden helpers (lab23) and are not part of the code a learner writes. "
                  "Windows and macOS were not run. On the page there is no display, so the printed result of the recorded run is shown.")
LIBRARIES = "PyAutoGUI, PyScreeze, Pillow, pyperclip, and the standard library"
PAGE_REQUIREMENTS = ["the packages pyautogui, pyscreeze, pillow and pyperclip, a graphical display (X) with xdotool, xclip and openbox, and Python 3.14",
                     "on the page (Pyodide) there is no display and no mouse or keyboard to control: every example is shown as recorded, and the chapter-code tab shows the printed result of the recorded run"]
