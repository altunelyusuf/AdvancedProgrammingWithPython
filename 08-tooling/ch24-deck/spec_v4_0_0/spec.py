"""Chapter 24 deck spec 4.0.0 for the generic builder 08-tooling/chapter_deck_build_v2_11_0.py (Lineage14, SEN0414). It makes the new lecture deck 4.0.0 of chapter 24 (Make Python Talk) in the shape of
chapters 12-23: parts with concept slides in plain words, sourced story pictures, one code slide for each of 16 examples with two result balloons, a native table of measured surprises, practice, summary
and resources. The first-version deck stays as it was."""
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

CH = 24
OUT_DECK = "03-materials/ch24/SEN0414_Ch24_MakePythonTalk_3e_v4_0_0.pptx"
OUT_MAN = "03-materials/ch24/page/chapter_code_ch24_v1_0_0.json"
IMAGE_FILES = ["story_images_v1_0_0.json"]
TITLE = "Chapter 24: Make Python Talk"
SUBTITLE = "pyttsx3 speech; voices, rate, volume and WAV files; Whisper; subtitles; downloading audio with yt-dlp"
CORE_TITLE = "SEN0414 Chapter 24: Make Python Talk (lecture deck 4.0.0)"
WHEELS = {}
MANIFEST_VERSION = "1.0.0"
MANIFEST_ABOUT = ("The code examples of the chapter 24 deck, in the order of the code slides (order = slide order). Every example ran the real pyttsx3, openai-whisper and yt-dlp of the chapter's "
                  "Python 3.14 environment, with eSpeak NG and ffmpeg on the PATH. Nothing was heard: the machine has no sound card, so pyttsx3 wrote WAV files; no microphone, no graphics card, "
                  "no Windows and no macOS were used. The examples that need audio from a public site use a public-domain LibriVox reading that the Internet Archive hosts; it stands in for YouTube, "
                  "and nothing was downloaded from YouTube. The lines that give each example its own folder are hidden helpers (lab24). On the page there is no speech engine, so the printed result of the "
                  "recorded run is shown.")
LIBRARIES = "pyttsx3, openai-whisper, yt-dlp, PyTorch, NumPy, and the standard library"
PAGE_REQUIREMENTS = ["the packages pyttsx3, openai-whisper (with PyTorch) and yt-dlp, the programs ffmpeg and eSpeak NG, network access to archive.org, and Python 3.14",
                     "on the page (Pyodide) there is no speech engine, no model files and no network to a download site: every example is shown as recorded, and the chapter-code tab shows the printed result of the recorded run"]
