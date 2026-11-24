"""Chapter 10 deck words 4.2.0 (Lineage11, change request 'no repeated stories'): the UTF-8 story repeats chapter 8 and the JSON
story repeats chapter 7, so both are replaced in place by two stories about the Windows paths the chapter shows, and the slide count
stays 41. Everything else is content_v3_0_0.py."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spec_v3_0_0"))
import content_v3_0_0 as T0

__version__ = "4.2.0"

PLAN = [('story', 'dosslash') if x == ('story', 'utf8') else ('story', 'driveletter') if x == ('story', 'json') else x for x in T0.PLAN]

STORIES = {k: v for k, v in T0.STORIES.items() if k not in ('utf8', 'json')}
STORIES['dosslash'] = {
    'title': 'Story: why Windows paths use a backslash',
    'img': 'screen_msdos_dir_v1_0_0.png',
    'prose': ['In 1983 Microsoft shipped MS-DOS 2.0, the first version that let a disk hold folders inside folders, and its programmers had to choose a character to separate the names.',
              'The slash was already taken: MS-DOS used it to mark command options, so the backslash became the separator.',
              'Larry Osterman, a Microsoft engineer, explained the choice in a 2005 blog post; historians still debate how much IBM, which wanted the old commands to keep working, pushed for it.',
              'Path() joins names with the separator of the computer it runs on, so one program prints spam\\eggs on Windows and spam/eggs elsewhere.'],
    'link': 'https://learn.microsoft.com/archive/blogs/larryosterman/why-is-the-dos-path-character',
    'linktext': 'Larry Osterman on the DOS path character'}
STORIES['driveletter'] = {
    'title': 'Story: why Windows calls the main drive C:',
    'img': 'screen_msdos5_setup_v1_0_0.png',
    'prose': ['In 1974 Gary Kildall demonstrated CP/M in Pacific Grove, California, one of the first operating systems for personal computers, and it named floppy drives with letters.',
              'MS-DOS began as a CP/M look-alike that Microsoft licensed from Seattle Computer Products, and it kept the lettering.',
              'The first two letters, A and B, went to floppy drives, so a hard disk took the next free one, C, and Windows still starts at C: today.',
              "That history is in every Windows path: PureWindowsPath('C:/Users/Al/spam.txt').drive gives 'C:'."],
    'link': 'https://en.wikipedia.org/wiki/Drive_letter_assignment',
    'linktext': 'Drive letter assignment on Wikipedia'}

for _k, _v in vars(T0).items():
    if not _k.startswith("__") and _k not in globals():
        globals()[_k] = _v
