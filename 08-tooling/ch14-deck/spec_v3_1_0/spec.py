"""Chapter 14 deck spec 3.1.0 for the generic builder 08-tooling/chapter_deck_build_v2_10_0.py. Deck 3.1.0 of chapter 14 replaces deck 2.0.0 (built by the chapter's own builder deck_build_v2_0_0.py) to meet the
rulings of 2026-11-14 and 2026-11-24: one thing per slide, notes for the reader, plain meanings instead of everyday pictures, code without prompts or lambda, stories as prose. The chapter's content, stories and examples are those of deck 2.0.0."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import examples_v3_1_0 as X
import visuals_v3_1_0 as V
import content_v3_1_0 as T0
import notes_v3_1_0 as N0


class _T:
    """the content words with the notes of this version"""
    NOTES = N0.NOTES
    STORY_NOTES = N0.STORY_NOTES
    RESULT_SAYS = N0.RESULT_SAYS

    def __getattr__(self, k):
        return getattr(T0, k)


T = _T()

CH = 14
OUT_DECK = "03-materials/ch14/SEN0414_Ch14_ExcelSpreadsheets_3e_v3_1_0.pptx"
OUT_MAN = "03-materials/ch14/page/chapter_code_ch14_v1_2_0.json"
IMAGE_FILES = ["story_images_v2_0_0.json"]
TITLE = "Chapter 14: Excel Spreadsheets"
SUBTITLE = "Chapter 14 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course"
CORE_TITLE = "SEN0414 Chapter 14: Excel Spreadsheets (lecture deck 3.1.0)"
WHEELS = {"openpyxl-3.1.5-py2.py3-none-any.whl": "5282c12b107bffeef825f4617dc029afaf41d0ea60823bbb665ef3079dc79de2",
          "et_xmlfile-2.0.0-py3-none-any.whl": "7a91720bc756843502c3b7504c77b8fe44217c85c537d85037f0f536151b2caa"}
MANIFEST_VERSION = "1.2.0"
MANIFEST_ABOUT = ("The code examples of the chapter 14 deck, in the order of the code slides (order = slide order). The page's Slide code tab lists them by name in this order; "
                  "every example is self-contained and runs with openpyxl 3.1.5 and the Python standard library, builds its workbooks in memory, reads no keyboard, opens no network connection and no window "
                  "(the chapter's own files are replaced by small stand-ins with the same sheets, columns and formulas, named beside the code).")
LIBRARIES = "openpyxl 3.1.5 and the Python standard library"
PAGE_REQUIREMENTS = ["openpyxl 3.1.5 and its dependency et_xmlfile 2.0.0 (loaded from the wheels of the chapter's assets folder; Pyodide installs them without a network)",
                     "The Python standard library modules io, zipfile, datetime, pprint, decimal and sys (imported by the examples that use them); no disk file, no keyboard input, no network, no window"]
