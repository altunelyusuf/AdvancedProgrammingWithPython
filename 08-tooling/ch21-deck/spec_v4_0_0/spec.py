"""Chapter 21 deck spec 4.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_10_0.py (Lineage14, SEN0414). It makes the new lecture deck 4.0.0 of chapter 21 (Graphs and Images) in the shape of chapters 12 to 20: parts, concept slides in plain words,
sourced story pictures, one code slide for each of 15 examples with two result balloons, a native colour table, practice, summary and resources. The first-version deck (26 slides) stays as it was."""
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

CH = 21
OUT_DECK = "03-materials/ch21/SEN0414_Ch21_GraphsAndImages_3e_v4_0_0.pptx"
OUT_MAN = "03-materials/ch21/page/chapter_code_ch21_v1_0_0.json"
IMAGE_FILES = ["story_images_v1_0_0.json"]
TITLE = "Chapter 21: Making Graphs and Manipulating Images"
SUBTITLE = "Pillow for pixels, colours, boxes, masks and drawing; the clipboard; Matplotlib for line, scatter, bar and pie graphs"
CORE_TITLE = "SEN0414 Chapter 21: Making Graphs and Manipulating Images (lecture deck 4.0.0)"
WHEELS = {}
MANIFEST_VERSION = "1.0.0"
MANIFEST_ABOUT = ("The code examples of the chapter 21 deck, in the order of the code slides (order = slide order). Every example is self-contained and runs offline, reads no keyboard and opens no window. "
                  "Every picture is drawn by the example itself (no file of the book's download is used); the clipboard of pyperclipimg, which needs a display, is replaced by a small class with the same two calls (EMULATED); "
                  "Matplotlib draws with the Agg backend into memory. The slide says so. No example needs an account or a network.")
LIBRARIES = "Pillow, Matplotlib, and the standard library"
PAGE_REQUIREMENTS = ["the packages Pillow (PIL) and Matplotlib, and the standard library modules io, os and tempfile",
                     "on the page (Pyodide) the examples run with the Agg backend and in memory; byte counts of saved pictures belong to the library version that ran them, and the chapter-code tab shows the printed result of the recorded run"]
