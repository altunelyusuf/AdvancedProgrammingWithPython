"""Chapter 11 deck notes 4.3.0 (Lineage11): the listing note names the Windows type, because Windows is the default platform of the examples.
Everything else is notes_v4_0_0.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notes_v4_0_0 as N0

__version__ = "4.3.0"

NOTES = dict(N0.NOTES)
STORY_NOTES = N0.STORY_NOTES
RESULT_SAYS = N0.RESULT_SAYS
TAKEAWAY = N0.TAKEAWAY
NOTES["listing"] = N0.NOTES["listing"].replace("PosixPath on Linux and WindowsPath on Windows, as the book shows", "WindowsPath, as the book shows, because Windows is the default platform of these examples; Linux and macOS show PosixPath")
