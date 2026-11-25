"""Chapter 10 deck notes 4.2.0 (Lineage11): the notes of the two replaced stories. Everything else is notes_v4_0_0.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notes_v4_0_0 as N0

__version__ = "4.2.0"

NOTES = dict(N0.NOTES)
RESULT_SAYS = N0.RESULT_SAYS
TAKEAWAY = N0.TAKEAWAY
STORY_NOTES = {k: v for k, v in N0.STORY_NOTES.items() if k not in ('utf8', 'json')}
STORY_NOTES["dosslash"] = ("In 1983 Microsoft released MS-DOS 2.0, the first version of DOS that could keep folders inside folders, and its programmers had to pick a character to separate the folder names in a path. "
                           "They could not use the slash, because MS-DOS already used it in front of command options. The backslash was chosen instead, and every Windows path since then is written that way. "
                           "Larry Osterman, an engineer at Microsoft, described the reason in a blog post in 2005, and writers on computer history still disagree about how much IBM's wish to keep the old commands working had to do with it. "
                           "Slide 6 shows Path() joining names, and it hides the difference: Path() joins the names with the separator of the computer that runs the program. The link opens Osterman's post.")
STORY_NOTES["driveletter"] = ("Gary Kildall demonstrated CP/M in 1974 in Pacific Grove, California, and it named each floppy drive with a letter. "
                              "MS-DOS began as a CP/M look-alike that Microsoft licensed from Seattle Computer Products, so the letters came along. "
                              "The letters A and B went to the floppy drives, which is why a hard disk received the next free letter, C. Windows is no longer built on MS-DOS, but its paths still start with a drive letter, such as C:\\Users. "
                              "Slide 10 takes a Windows path apart and shows the drive as one part of it, and the drive attribute of a Windows path returns it. The link opens a short article on how drive letters began.")
