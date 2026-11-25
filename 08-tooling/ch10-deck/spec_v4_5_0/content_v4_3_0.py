"""Chapter 10 deck words 4.3.0 (Lineage11, change request 'no everyday analogies'): the seven former analogy slides, the summary
sentence and the practice sentence state plainly what each concept is and does. Titles, slide count (41) and concept names stay.
Everything else is content_v4_2_0.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_v4_2_0 as T0

__version__ = "4.3.0"

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "What it is and does"
CONCEPTS_TAIL = "each explained in plain words"

PARTS = dict(T0.PARTS)
_p1 = list(PARTS[1])
_p1[1] = 'Names, locations and the parts of a path'
_p1[2] = [(a, 'A path from the root of the drive, or a path from the working directory.') if a == 'Absolute or relative' else (a, b) for a, b in _p1[2]]
PARTS[1] = tuple(_p1)
_p3 = list(PARTS[3])
_p3[2] = [(a, 'Open a file object, use it, close it.') if a == 'open and close' else (a, b) for a, b in _p3[2]]
PARTS[3] = tuple(_p3)

ANALOGIES = [
 ('A1', 'Filepaths and how to join them',
  'A filepath says where a file is: the folders to open, in order, and the file name at the end.',
  [('Files and Filepaths', 'A file holds data under a name; its filepath tells which folders lead to it.'),
   ('Filepath', 'The folder names from the start of a drive down to the file, then the file name.'),
   ('Standardizing Path Separators', 'Windows uses a backslash and Linux and macOS a slash; Path writes the local one.'),
   ('Joining Paths', "The slash operator joins names into one path: Path('spam') / 'eggs'."),
   ('Absolute path', 'Starts at the root of the drive and names the same file everywhere.'),
   ('Relative path', 'Starts at the working directory, so it means another file when that changes.'),
   ('Specifying Absolute vs. Relative Paths', 'A leading root, or a drive letter on Windows, makes a path absolute.'),
   ('Handling Absolute and Relative Paths', 'absolute() makes a path absolute; relative_to() cuts it back.')]),
 ('A2', 'The working directory and Path objects',
  'The working directory is the folder a program starts from; every relative path is read from there.',
  [('Accessing the Current Working Directory', 'os.getcwd() returns the folder the program works in right now.'),
   ('Current working directory', 'The folder that every relative path starts from.'),
   ('os.chdir()', 'Changes the working directory, so every relative path afterwards means a different place.'),
   ('Accessing the Home Directory', "Path.home() returns the folder that holds the user's own files."),
   ('Path()', 'Builds a path object from text without touching the disk.'),
   ('Path.cwd()', 'A path object for the current working directory.'),
   ('Path.home()', 'A path object for the home directory.'),
   ('is_absolute', 'Returns True when the path starts at the root and False when it is relative.'),
   ('Getting the Parts of a Filepath', 'The attributes name, stem, suffix, parent and drive return the pieces of a path.')]),
 ('A3', 'Folders, file facts and glob patterns',
  'A folder holds files and other folders; a glob pattern with * and ? selects every name that fits it.',
  [('Creating New Folders', 'makedirs and mkdir add folders to the disk before files are written into them.'),
   ('os.makedirs()', 'Creates a folder and every missing folder above it in one call.'),
   ('mkdir', 'Path.mkdir creates one folder; parents=True adds the missing ones above it.'),
   ('Checking Path Validity', 'Ask whether a path exists before using it, so the program can create it or stop.'),
   ('exists', 'Returns True when the path names an existing file or folder, otherwise False.'),
   ('Finding File Sizes and Timestamps', "A file's size in bytes and its times of change are read without opening it."),
   ('stat', 'Returns the size and times of one file, such as st_size and st_mtime.'),
   ('Finding Files Using Glob Patterns', 'A pattern with * and ? lists every file whose name fits it.'),
   ('glob', 'Path.glob yields the paths in one folder that match a pattern.')]),
 ('A4', 'Opening, reading and closing files',
  'Reading or writing a file takes three steps, always in this order: open it, read or write, close it.',
  [('The File Reading and Writing Process', 'Open the file, read or write through the file object, close the file.'),
   ('Plaintext file', 'A file of characters and line breaks that a text editor shows as they are.'),
   ('Binary file', 'A file of bytes, such as a picture or a sound; an editor shows nonsense.'),
   ('Opening Files', 'open() takes a path and a mode and returns a file object.'),
   ('open()', "The built-in function that starts the process; the mode 'r' reads and 'w' writes."),
   ('File object', 'The value open() returns; it remembers how far the program has read.'),
   ('Reading the Contents of Files', 'Methods such as read() and readlines() return the text of the file.'),
   ('read', 'Returns the rest of the file, from the current position, as one string.'),
   ('close', 'Ends the use of the file and releases it for other programs.')]),
 ('A5', 'Writing files and the with block',
  'A with block opens a file and closes it again when the block ends, even if an error stops the program inside it.',
  [('Writing to Files', "'w' starts the file empty, 'a' adds to its end, 'x' refuses an existing file."),
   ('write', 'Adds one string to the file; a newline character has to be written explicitly.'),
   ('write_text', 'A Path method that writes a whole string to a file in one call.'),
   ('read_text', 'A Path method that returns the whole content of a file in one call.'),
   ('readlines', 'Returns the lines of a file as a list of strings, each ending with a newline.'),
   ('Using with Statements', 'with open(...) as f: closes f automatically at the end of the block.'),
   ('Context manager', 'An object that sets up when a with block starts and cleans up when the block ends.')]),
 ('A6', 'Saving variables with shelve and json',
  'A shelf and a json file both keep Python values between two runs; a shelf is a file used like a dictionary.',
  [('Saving Variables with the shelve Module', 'shelve keeps values in a file, so that the next run of the program finds them.'),
   ('Shelf', 'The object shelve.open() returns; it is used like a dictionary whose entries are saved in a file.'),
   ('shelve.open()', 'Opens the shelf file and creates it when it does not exist; close it when done.'),
   ('json', 'A plain-text format that programs in many languages can read, which suits data shared between programs.')]),
 ('A7', 'Chapter programs and practice work',
  'The programs of this chapter read files, change the text and write a new file; the practice work repeats those steps.',
  [('Project 4: Generate Random Quiz Files', 'Shuffles the questions and writes a different quiz file for each student.'),
   ('Practice Programs', 'Short programs that repeat the path, reading and writing steps until they are familiar.'),
   ('Practice Questions', 'Four questions that each have their answer on an earlier slide and can be checked by running code.'),
   ('Summary', 'Five sentences that restate the chapter; each can be traced to a slide.'),
   ('Mad Libs', 'Reads a text file, replaces its placeholder words and writes the finished text to a new file.'),
   ('Regex Search', 'Opens every text file in a folder and prints the lines that match a regular expression.')]),
]

SUMMARY_ANALOGY = "The summary keeps the five points to remember; each one can be traced to a slide."
PRACTICE_ANALOGY = "The practice questions are short exercises: answer each in a few lines, then run the code to check."

for _k, _v in vars(T0).items():
    if not _k.startswith("__") and _k not in globals():
        globals()[_k] = _v
