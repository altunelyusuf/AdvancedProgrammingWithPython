"""Chapter 25 deck spec 4.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_11_0.py (Lineage14, SEN0414). It makes the new lecture deck 4.0.0 of chapter 25 (Threads) in the shape of
chapters 12-24: parts with concept slides in plain words, sourced story pictures, one code slide for each of 17 examples with two result balloons, native tables and a chart of the recorded
timings, practice, summary and resources. The first-version deck stays as it was."""
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

CH = 25
OUT_DECK = "03-materials/ch25/SEN0414_Ch25_Threads_3e_v4_0_0.pptx"
OUT_MAN = "03-materials/ch25/page/chapter_code_ch25_v1_0_0.json"
IMAGE_FILES = ["story_images_v1_0_0.json"]
TITLE = "Chapter 25: Threads"
SUBTITLE = "Threads, locks, pools, the GIL, processes and asyncio; the multithreading that the 3rd edition dropped"
CORE_TITLE = "SEN0414 Chapter 25: Threads (lecture deck 4.0.0)"
WHEELS = {}
MANIFEST_VERSION = "1.0.0"
MANIFEST_ABOUT = ("The code examples of the chapter 25 deck, in the order of the code slides (order = slide order). Every example ran under the Python 3.14.6 of the chapter's environment with requests "
                  "and beautifulsoup4; the free-threaded build of Python 3.14.6 is started as a child program where a slide asks it. Programs that wait print only what does not depend on how long they took. "
                  "The downloader asks a stand-in of the comic site that runs on 127.0.0.1; xkcd.com is never contacted. The lines that give each example its own folder are hidden helpers (lab25). "
                  "On the page there is no thread, no second process and no network socket, so the printed result of the recorded run is shown.")
LIBRARIES = "requests, beautifulsoup4, and the standard library"
PAGE_REQUIREMENTS = ["Python 3.14.6 with requests and beautifulsoup4, a free-threaded build of Python 3.14.6 for the slide on the lock, and a machine that allows local sockets and child processes",
                     "on the page (Pyodide) there are no threads, no child processes and no sockets: every example is shown as recorded, and the chapter-code tab shows the printed result of the recorded run"]
