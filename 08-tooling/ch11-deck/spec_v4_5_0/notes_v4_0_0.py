"""Chapter 11 deck notes 4.0.0 (new file over notes 3.1.0, which stays as committed; Lineage11, 2026-11-24). Deck 4.0.0 gives each code ONE box, with the sample files made by hidden set-up lines,
so the notes of the 19 code slides, the two result balloons and the title note are written again for that code and for what the run now prints. They are reader notes: full sentences that explain
the slide's short wording, no direction to a presenter, no think-of statement, 60 to 140 words. Every number below is what the run prints or what the set-up creates."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'spec_v3_0_0'))
import notes_v3_1_0 as N0

__version__ = "4.0.0"

NOTES = dict(N0.NOTES)
STORY_NOTES = N0.STORY_NOTES
NOTES["title"] = ("This chapter of the book, Organizing Files, moves from single files to whole folders: copying, moving, deleting, listing, walking and packing them into ZIP archives. "
                  "The deck has nineteen code examples that run on the chapter page, four true stories about the people behind these tools, and an everyday picture for every concept. "
                  "Each code slide shows one whole program in one box that can be copied in a single step, a balloon that explains it, and what the run really printed, drawn as a table, a chart or a small picture. "
                  "The sample files each program needs are made by lines that the slide does not show. Slide 2 lays out the route through the five parts.")

NOTES.update({
 "copy": ("Shutil.copy copies the contents of one file and returns the path of the copy. The program calls it twice. The first call gives a folder as the target, here the current folder, so the copy keeps the name file1.txt. "
          "The second call gives a file name as the target, so the copy is called file2.txt and sits inside spam. Each call prints the path it returns, and those two paths are the two lines of the result. "
          "The folder list under them shows that spam still holds the original file1.txt next to the new file2.txt, because a copy never removes the original. Slide 7 copies a whole folder with copytree."),
 "copytree": ("Shutil.copytree copies a folder together with every subfolder and file in it, and returns the path of the new folder. The program copies spam to spam_backup and prints that path. "
              "The result compares the two folders: both hold the same names, so the copy is complete. The target name must be new, because copytree refuses a folder that already exists; the option dirs_exist_ok=True "
              "merges into an existing folder instead, and it replaces files with the same name, so it should be used on purpose. The folder list shows what spam_backup contains. Slide 8 looks at what copying does to time stamps."),
 "copy2": ("Copying a file normally gives the copy a new modification time, the moment of copying. Shutil.copy2 also copies the file's metadata, including the modification time, which is why it is the better choice for backups. "
           "The program copies file1.txt to kept.txt with copy2, reads the modification time of both files with stat, and prints whether they are equal; the answer is True. "
           "The table shows the same fact in numbers, one identical time stamp for the original and for the copy. With plain copy the two times would differ. Slide 9 moves files."),
 "move": ("Shutil.move relocates a file or folder, and it renames in the same call when the target is a new file name. The program moves file1.txt into the folder spam2, which keeps its name, "
          "and then moves it again to spam2/new_name.txt, which renames it. Each call prints the path it returns, and those are the two lines of the result. The folder list shows that spam is now empty and spam2 holds only new_name.txt. "
          "Moving onto a name that already exists silently overwrites it, so a careful program checks first. When source and target are on different disks, move copies the file and then deletes the original. Part 2, on deleting, begins on slide 10."),
 "unlink": ("Os.unlink deletes one file for good, and os.rmdir removes one folder, but only when it is empty. The program deletes spam/file1.txt, removes the empty folder spam/eggs, and prints what is left in spam. "
            "The result is an empty list, so both are gone and nothing is left. The small note under the folder list says why this matters: there is no recycle bin in between, and neither call can be undone. "
            "If rmdir is pointed at a folder that still holds something, Python raises an error instead of deleting it. Slide 13 removes a whole tree."),
 "rmtree": ("Shutil.rmtree removes a folder and everything inside it in one call, which is why it is the most dangerous function of the chapter. The program starts with spam, which holds a subfolder eggs and one file inside it, "
            "so three paths exist. It calls rmtree on spam and prints whether spam still exists; the answer is False. The table lists the three paths before the call and after it: all three were there, and all three are gone. "
            "Because it cannot be undone, the habit on slide 14 comes first: print what would go before anything is deleted."),
 "dryrun": ("A dry run prints what a program would delete, and the delete call stays a comment until the list is right. The folder holds a.txt, b.txt and c.rxt. The loop uses the pattern *.rxt, "
            "which has a typo, because the wanted extension is txt. Printing the matches shows at once that only c.rxt would be deleted, and the line with os.unlink is still marked with a hash, so nothing was touched. "
            "The table shows for each file whether it matches the pattern. Only when the printed list is right is the comment mark removed. Slide 15 shows a safer tool, send2trash."),
 "listing": ("Listing one folder can be done in different ways, and each returns something different. Os.listdir gives plain names as text. The iterdir method of a Path gives Path objects, which know their own location "
             "and whether they are folders. The program prints both for the folder spam, wrapped in sorted so that the order is the same on every computer. Both lists hold eggs and file1.txt, and only the second shows the type, "
             "PosixPath on Linux and WindowsPath on Windows, as the book shows. The text file inside eggs is not listed, because neither call descends into subfolders; the walk on slide 20 does. The Path methods are those of chapter 10."),
 "walk": ("Os.walk visits a folder and then each folder below it, and at every step it hands over three values: the folder's path, the list of its subfolders and the list of its files. "
          "The program loops over the walk with the for loop of chapter 3 and prints one line for each subfolder and each file. Sorting the subfolders fixes the order of the visit, so the lines are the same on every run. "
          "The result shows three steps, spam, spam/eggs and spam/eggs/bacon, with four files in all; the table and the chips draw the same tree. Slide 21 uses the walk to add up bytes."),
 "sizes": ("A walk can add up how much space the files of a tree use. For every folder the walk hands over, the program takes each file name, joins it to the folder path with os.path.join, "
           "asks os.path.getsize for its size in bytes, and adds it to a running total. The tree has four files of five bytes each, so the printed total is 20. "
           "The bar chart shows the same bytes split by folder, which is useful when the question is where the space went. The same loop with a size limit finds big files, on slide 36. Slide 22 builds folders with mkdir."),
 "mkdir": ("Path.mkdir makes one folder, and it refuses when the folder above it does not exist. The program passes parents=True, which builds the whole chain of missing folders, spam, eggs and bacon, in one call. "
           "The second call asks for the same chain again with exist_ok=True, which accepts a folder that is already there instead of raising an error. The program ends by printing whether the last folder is a directory, and the answer is True. "
           "The small tree shows the three folders. With these two options a program can run twice without failing the second time, which is the safe default for set-up code. The story of where the folder tree came from is on slide 23."),
 "zipwrite": ("Zipfile.ZipFile opens an archive, and the mode w starts a new one. The program first writes a file of repeated text, fifty thousand characters, then adds it to a new archive with compress_type=ZIP_DEFLATED "
              "and the highest compression level; without that argument the file is only stored, not shrunk. It then reads the archive back and asks getinfo for the original size and the stored size, which print as 50000 and 97. "
              "The column chart compares the two sizes, and the chip says the archive is about five hundred times smaller. Repeated text compresses extremely well; real documents shrink much less. Slide 27 shows another mode of a ZIP file."),
 "zipmodes": ("A ZipFile can be opened in four modes, and each one changes what may happen to an existing archive: w starts a new archive, a adds to an existing one, r only reads, and x creates a new one and refuses to overwrite. "
              "The program opens example.zip, which already holds file1.txt, in mode a and writes file2.txt into it. It then prints the member names with namelist, and the list now holds both files. "
              "The table shows the two members with their sizes in bytes. Nothing already in the archive was lost. Slide 28 unpacks archives."),
 "extract": ("An archive can be unpacked completely or one member at a time. The program opens example.zip, which holds file1.txt. Extractall unpacks every member into the folder out, creating the folder if needed. "
             "Extract takes out one named member into a folder of your choice, here new/folder, and returns the path of the new file, which the program prints. The folder list shows both places: out and new. "
             "Member names in an archive are paths, so a program should only unpack archives it trusts. Slide 29 packs a whole folder in one call."),
 "archives": ("The shutil module can pack and unpack a whole folder in one call each. Make_archive packs the folder spam into spam_backup.zip, and the names inside keep the structure of the folder. "
              "Unpack_archive is the one-call way back and guesses the format from the file name; here it unpacks into the new folder spam_copy. The program prints the content of spam_copy, which is eggs and file1.txt, "
              "the same top level as spam. The table lists the members of the ZIP, and the chip counts the entries that appeared after unpacking. For a quick backup these two calls are enough; for control over every member the zipfile calls of slides 26 to 28 are needed. The history of the format is on slide 30."),
 "backup": ("This is the fifth project of the book, a backup into a numbered ZIP. The function finds the first number for which a name such as spam_1.zip is still free, so an old backup is never overwritten. "
            "It then walks the folder, prints a line for every folder and file it adds, writes each file into the new archive and closes it. The last line of the program calls the function for spam. "
            "The result shows the printed lines and the member of spam_1.zip; the amber chip says that the next run makes spam_2.zip. The function is the kind of helper that chapter 4 introduced. Slide 35 copies only the PDFs of a tree."),
 "selective": ("Selective copy walks a tree and copies only the files of one type. The source tree src holds one.pdf, a subfolder a with two.pdf, and three.txt, and the folder dest is empty. "
               "The loop walks src, tests whether each name ends with .pdf, and copies the match into dest. The program prints the content of dest, which is the two PDFs, and the text file stays out. "
               "The chip counts the files of src and the files copied, and the folder list shows the source, which keeps everything. The test is case-sensitive, so a name ending in .PDF would not be found. Slide 36 finds the big files of a tree."),
 "large": ("Finding the big files of a tree is a walk with a size test. The program walks spam and, for every file, asks os.path.getsize for the size in bytes. Only files larger than 1000 bytes are printed, with their size. "
           "The tree holds big.bin with 3000 bytes, tiny.txt with 40 bytes and huge.bin with 9000 bytes inside sub, so two lines are printed. The bar chart shows all three sizes against the limit of one thousand. "
           "Changing the limit changes the list, and the same loop with the sums of slide 21 would report folders instead of files. Slide 37 renames files by swapping day and month."),
 "dates": ("This program renames files whose names carry an American date, month-day-year, into the European order, day-month-year. The folder holds spam12-31-1900.txt, report01-02-2020.txt and notes.txt. "
           "The pattern keeps month, day and year as three groups, and the loop uses sub to swap groups one and two and shutil.move to rename the file. The pattern is a regular expression, the subject of chapter 9. "
           "The printed list shows spam31-12-1900.txt and report02-01-2020.txt, so the day and the month changed places, while notes.txt, which has no date, stays as it is. Slide 38 shows what current Python adds."),
})

RESULT_SAYS = dict(N0.RESULT_SAYS)
RESULT_SAYS.update({
 "copy": "The run printed the two new paths and the two copies.",
 "copytree": "spam_backup holds the same names as spam.",
 "copy2": "The two time stamps are equal, so the answer is True.",
 "move": "The file moved into spam2, then took a new name.",
 "unlink": "The file and the empty folder are gone; spam is empty.",
 "rmtree": "The whole tree is gone, so exists is False.",
 "dryrun": "Only c.rxt would be deleted; the delete line is a comment.",
 "listing": "Two calls, two lists: names, and Path objects.",
 "sizes": "Four files of five bytes: the total is 20.",
 "mkdir": "The chain was built; the second call raised no error.",
 "zipmodes": "Mode a added file2.txt to the archive.",
 "extract": "extractall made out; extract put one file in new/folder.",
 "archives": "The ZIP held the tree; unpacking rebuilt it in spam_copy.",
 "backup": "One run made spam_1.zip with its files inside.",
 "selective": "Only the two PDFs were copied to dest.",
 "large": "Two files are above 1000 bytes; huge.bin is the biggest.",
})

TAKEAWAY = {
 "copytree": "copytree makes a new folder with the same contents.",
 "copy2": "copy2 keeps the time stamp of the original.",
 "move": "move relocates and renames in one call.",
 "listing": "listdir gives names; iterdir gives Path objects.",
 "zipmodes": "Mode a adds to an archive that already exists.",
}
