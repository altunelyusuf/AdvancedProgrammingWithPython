"""Chapter 10 deck notes 4.4.0 (Lineage11, change request 'no everyday analogies'): the notes that compared a concept with an everyday thing
state the concept plainly. Everything else is notes_v4_3_0.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notes_v4_3_0 as N0

__version__ = "4.4.0"

NOTES = dict(N0.NOTES)
STORY_NOTES = N0.STORY_NOTES
RESULT_SAYS = N0.RESULT_SAYS
TAKEAWAY = N0.TAKEAWAY


def _rep(key, old, new):
    assert NOTES[key].count(old) == 1, (key, old)
    NOTES[key] = NOTES[key].replace(old, new)


_rep("title", "and an everyday picture for every concept", "and a plain explanation of every concept")
_rep("divider1", "A path is the address of a file, and pathlib turns that address into an object", "A path names the place of a file, and pathlib turns that name into an object")
_rep("readmethods", "A file object remembers where it has read to, like a cursor in a text.", "A file object remembers the position it has read to.")
_rep("summary", "The analogy is a packing list: only what you really need goes into the bag.", "Each sentence keeps only the point that must be remembered, and each can be traced to a slide.")
_rep("practice", "The four questions are short drills, like finger scales before a concert.", "The four questions are short exercises.")

NOTES["A1"] = ("The headline says what a filepath is: the list of folders to open, in order, with the file name at the end. The rows explain each idea in plain words. "
               "An absolute path starts at the root of the drive and names the same file wherever the program runs, while a relative path starts at the working directory and means something else when that directory changes. "
               "The slash operator joins names, and Path writes the separator of the computer that runs the program: a backslash on Windows and a slash on Linux and macOS. "
               "Slide 6 shows the same ideas in code, and slide 9 returns to absolute and relative paths.")
NOTES["A2"] = ("The headline defines the working directory: the folder from which every relative path is read. os.getcwd() and Path.cwd() return it, and os.chdir() changes it, after which the same relative path names a different place. "
               "Path.home() returns the home directory of the user who runs the program. Path() only builds a path object from text and does not look at the disk, so a path can name a file that does not exist. "
               "is_absolute tells whether a path starts at the root, and name, stem, suffix, parent and drive return its parts. Slide 9 runs these calls, and slide 10 takes a path apart.")
NOTES["A3"] = ("The headline explains the two ideas of this part. A folder holds files and other folders, and a glob pattern selects names with the wildcards * and ?. "
               "os.makedirs creates every missing folder on the way, while mkdir creates one folder and needs parents=True to create the missing ones above it. "
               "exists answers True or False without raising an error. stat returns the size in bytes and the times of change of a file, and glob lists the paths that match a pattern. "
               "Slides 13 to 15 turn each row into code.")
NOTES["A4"] = ("The headline gives the three steps of working with a file: open it, read or write, and close it, always in this order. "
               "A plaintext file holds characters and line breaks that an editor shows as they are, while a binary file holds bytes, such as a picture or a spreadsheet, that need the program made for them. "
               "open() takes a path and a mode and returns a file object, which remembers how far the program has read. read returns everything from that position to the end, and close ends the use of the file. "
               "Slides 18 to 21 run these steps.")
NOTES["A5"] = ("The headline explains the with block: it opens a file and closes it again when the block ends, even if an error stops the program inside the block. "
               "The rows give the writing modes: w starts with an empty file, a adds to the end and x refuses a file that already exists. "
               "write adds one string, write_text writes a whole string in one call, read_text returns the whole content and readlines returns a list of lines. "
               "A context manager is an object that sets up when the block starts and cleans up when it ends. Slides 23 and 24 show the with block and the modes.")
NOTES["A6"] = ("The headline defines the shelf: a file that is used like a dictionary and keeps its entries between two runs of a program. "
               "shelve.open() opens the shelf file and creates it when it does not exist, and the Shelf object is used with keys and values. "
               "json is a plain-text format that programs in many languages can read, which is the reason to choose it when another program has to read your data. "
               "Slide 28 runs the shelf, and slide 30 runs json.")
NOTES["A7"] = ("The headline says what the programs of this chapter have in common: they read files, change the text and write a new file. "
               "Project 4 writes a different quiz file for each student, Mad Libs replaces the placeholder words of a story from a text file, and Regex Search prints the matching lines of every text file in a folder. "
               "The practice programs repeat the same steps until they are familiar, and the practice questions on slide 40 are short exercises that each have their answer on an earlier slide.")
