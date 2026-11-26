"""Chapter 22 deck spec 4.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_10_0.py (Lineage14, SEN0414). It makes the new lecture deck 4.0.0 of chapter 22 (Reading Text from Images with OCR) in the shape of chapters 12 to 21: parts, concept slides in plain words,
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

CH = 22
OUT_DECK = "03-materials/ch22/SEN0414_Ch22_ReadingTextFromImages_3e_v4_0_0.pptx"
OUT_MAN = "03-materials/ch22/page/chapter_code_ch22_v2_0_0.json"
IMAGE_FILES = ["story_images_v1_0_0.json"]
TITLE = "Chapter 22: Reading Text from Images with OCR"
SUBTITLE = "Tesseract and pytesseract; the limits of a picture; settings and languages; searchable PDFs; NAPS2; reading the screen"
CORE_TITLE = "SEN0414 Chapter 22: Reading Text from Images with OCR (lecture deck 4.0.0)"
WHEELS = {}
MANIFEST_VERSION = "1.0.0"
MANIFEST_ABOUT = ("The code examples of the chapter 22 deck, in the order of the code slides (order = slide order). Every example is self-contained and runs offline, reads no keyboard and opens no window. "
                  "Every picture is drawn by the example itself (no file of the book's download is used); the screen of pyautogui, which needs a display, is replaced by a small class with the same call (EMULATED); "
                  "the program NAPS2 is not installed and its example shows the error. The examples need the program Tesseract with its English, German and French data. No example needs an account or a network.")
LIBRARIES = "Pillow, NumPy, pytesseract, and the standard library"
PAGE_REQUIREMENTS = ["the packages Pillow (PIL), NumPy and pytesseract, and the standard library modules difflib, subprocess, os and tempfile",
                     "on the page (Pyodide) there is no Tesseract program, no NAPS2 and no display: the examples that need them are shown as recorded, and the chapter-code tab shows the printed result of the recorded run"]
