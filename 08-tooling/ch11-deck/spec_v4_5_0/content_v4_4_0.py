"""Chapter 11 deck words 4.4.0 (Lineage11, change request 'no everyday analogies'): the five former analogy slides, the summary
sentence and the practice sentence state plainly what each concept is and does. Titles, slide count (41) and concept names stay.
Everything else is content_v3_0_0.py."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spec_v3_0_0"))
import content_v3_0_0 as T0

__version__ = "4.4.0"

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "What it is and does"
CONCEPTS_TAIL = "each explained in plain words"

PARTS = dict(T0.PARTS)
_p4 = list(PARTS[4])
_p4[1] = 'Many files in one smaller file, and back again'
PARTS[4] = tuple(_p4)

ANALOGIES = [
 ('A1', 'Copying and moving files with shutil',
  'A copy leaves the original in place; a move takes the original to the new place and replaces a file of the same name there.',
  [('The shutil Module', 'The standard-library module that copies, moves and deletes whole files and folders.'),
   ('Copying and moving', 'A copy gives two files; a move leaves one, at the new place.'),
   ('shutil.copy', 'Copies one file to a new name or folder and returns the path of the copy.'),
   ('shutil.copytree', 'Copies a folder with every subfolder and file in it.'),
   ('shutil.move', 'Moves or renames a file or folder; a file with the same name at the target is replaced.')]),
 ('A2', 'Deleting files and folders safely',
  'Permanent deletion cannot be undone; a program lists what it would delete first and deletes second.',
  [('Safe deletion', 'Print the names that would be deleted before the program deletes anything.'),
   ('unlink', 'os.unlink removes one file for good; it does not go to the recycle bin.'),
   ('send2trash', 'Moves a file or folder to the recycle bin, where it can still be restored.'),
   ('rmtree', 'shutil.rmtree removes a whole folder with everything inside it, permanently.'),
   ('Dry run', 'A run that prints what would be deleted and deletes nothing.')]),
 ('A3', 'Walking through folder trees',
  'A folder tree is a folder with subfolders, which have subfolders in turn; os.walk visits every folder of it.',
  [('Walking a Directory Tree', 'A loop that visits one folder, then each folder inside it, and so on down the tree.'),
   ('Walking a folder tree', 'At every folder the program receives the folder name, its subfolder names and its file names.'),
   ('walk', 'os.walk gives these three values at every step of the loop.'),
   ('mkdir', 'Creates one folder; parents=True also creates the missing folders above it.'),
   ('listdir and glob', 'Both list one folder: listdir all its names, glob only the names that fit a pattern.')]),
 ('A4', 'Packing files into ZIP archives',
  'A ZIP file holds many files in one smaller file, and every file can be taken out of it unchanged.',
  [('Compressing Files with the zipfile Module', 'zipfile stores files in an archive; with compression the archive is smaller than the files together.'),
   ('Archives', 'One file that contains many files together with their names and folders.'),
   ('zipfile.ZipFile', "Opens an archive; the mode 'w' starts one, 'a' adds to one and 'r' reads one."),
   ('extract', 'extract takes out one file and extractall takes out every file of the archive.')]),
 ('A5', 'Programs that organize files',
  'A practice program combines the tools of this chapter on sample files in a temporary folder, so no real file is at risk.',
  [('Practice Programs', 'Programs that combine walk, copy, move and ZIP on files made in a temporary folder.'),
   ('backupToZip', 'Packs a whole folder into a ZIP file with a number in its name, so an earlier backup is never overwritten.'),
   ('Selective copy', 'Walks a folder tree and copies only the files with one extension to a new folder.'),
   ('Date renaming', 'Finds file names with an American date and renames them with the European order.')]),
]

SUMMARY_ANALOGY = "The summary keeps the five points to remember; each one can be traced to a slide."
PRACTICE_ANALOGY = "The practice questions are short exercises: answer each in a few lines, then run the code to check."

for _k, _v in vars(T0).items():
    if not _k.startswith("__") and _k not in globals():
        globals()[_k] = _v
