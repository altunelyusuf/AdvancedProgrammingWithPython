"""Chapter 11 deck notes 4.4.0 (Lineage11, change request 'no everyday analogies'): the notes that compared a concept with an everyday thing
state the concept plainly. Everything else is notes_v4_3_0.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notes_v4_3_0 as N0

__version__ = "4.4.0"

NOTES = dict(N0.NOTES)
STORY_NOTES = dict(N0.STORY_NOTES)
RESULT_SAYS = N0.RESULT_SAYS
TAKEAWAY = N0.TAKEAWAY


def _rep(d, key, old, new):
    assert d[key].count(old) == 1, (key, old)
    d[key] = d[key].replace(old, new)


_rep(NOTES, "title", "and an everyday picture for every concept", "and a plain explanation of every concept")
_rep(NOTES, "divider1", "Slide 5 gives the everyday pictures.", "Slide 5 explains the concepts in plain words.")
_rep(NOTES, "divider2", "Slide 11 gives the everyday pictures.", "Slide 11 explains the concepts in plain words.")
_rep(NOTES, "divider3", "A folder tree is like a building where floors hold rooms and rooms hold cupboards, and slide 18 draws that picture.", "A folder tree is a folder that holds folders, which hold folders in turn, and slide 18 draws that structure.")
_rep(NOTES, "divider4", "A ZIP file is like a vacuum-packed suitcase: many things go in, one small parcel comes out, and everything can come out again unchanged.", "A ZIP file holds many files in one smaller file, and every file can come out again unchanged.")
_rep(NOTES, "divider4", "Slide 25 shows the suitcase picture.", "Slide 25 explains the ZIP concepts in plain words.")
_rep(NOTES, "divider5", "A practice program is like a driving lesson on an empty car park: the real skill with no real risk, because every program works in its own temporary folder.", "A practice program combines the tools of the chapter on sample files, and no real file is at risk, because every program works in its own temporary folder.")
_rep(NOTES, "divider5", "Slide 33 shows the picture of the driving lesson.", "Slide 33 explains the four programs in plain words.")
_rep(NOTES, "practice", "like finger scales before a performance, ", "")
_rep(STORY_NOTES, "kare", "while os.unlink behaves like the shredder", "while os.unlink removes the file for good")
_rep(NOTES, "divider4", "many files in one parcel and back again", "many files in one smaller file and back again")
_rep(NOTES, "divider2", "the habit of rehearsing matters more here", "the habit of printing first matters more here")
_rep(NOTES, "kare", "while os.unlink behaves like the shredder", "while os.unlink removes the file for good")

NOTES["A1"] = ("The headline states the rule of this part: a copy leaves the original in place, and a move takes the original to the new place. "
               "The table explains each concept in plain words: shutil.copy copies one file and returns the path of the copy, copytree copies a whole folder with everything inside it, and move relocates or renames a file or folder. "
               "If the target already holds a file with the same name, the moved file replaces it, and slides 6 to 9 return to that warning. What a function really does is shown by its run. Slide 6 runs shutil.copy.")
NOTES["A2"] = ("The headline gives the reason for the whole part: permanent deletion cannot be undone, while a file in the recycle bin can be restored until the bin is emptied. "
               "The table explains os.unlink, which removes one file for good, send2trash, which moves a file to the recycle bin, and shutil.rmtree, which removes a whole folder with everything inside it. "
               "The dry run prints what would be deleted and deletes nothing. The three habits of this part are to delete one thing deliberately, to delete a tree only after counting what is inside, and to print the list before running the real call. "
               "The real runs begin on slide 12.")
NOTES["A3"] = ("The headline defines the folder tree: a folder holds subfolders, which hold subfolders in turn. The table explains os.walk, which visits one folder and then every folder inside it, and gives at each step the folder name, its subfolder names and its file names. "
               "mkdir creates one new folder, and with parents=True it also creates the missing folders above it. listdir and glob both read one folder: listdir returns every name, and glob only the names that match a pattern. "
               "The order of a visit matters: a walk can handle a folder before its subfolders or after them, and slide 20 shows both orders. Slide 19 lists one folder in four ways.")
NOTES["A4"] = ("The headline defines a ZIP file: many files stored in one smaller file, from which every file comes out again unchanged. "
               "The table explains compression, which makes the archive smaller than the files together, and extract, which takes out one file or, with extractall, every file. "
               "ZipFile is the object that opens an archive: the mode w starts a new one, a adds to one and r reads one. How much a file shrinks depends on its content: repeated text shrinks enormously, while a file that is already compressed hardly shrinks at all. "
               "Slide 26 writes a file into an archive and measures the saving.")
NOTES["A5"] = ("The headline says what a practice program is: it combines the tools of this chapter on sample files in a temporary folder, so no real file is at risk. "
               "The table explains the four programs: backupToZip packs a whole folder into a ZIP file with a number in its name, so an earlier backup is never overwritten; selective copy walks a folder tree and copies only the files with one extension; date renaming finds file names with an American date and renames them with the European order. "
               "The four programs are chosen because real tasks look like them. Slide 34 builds the numbered backup.")
