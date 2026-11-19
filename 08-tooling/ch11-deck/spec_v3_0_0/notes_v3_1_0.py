"""Chapter 11 deck speaker notes, version 3.1.0 (new file over 3.0.0, which stays as committed): the notes are READER notes (handover of 2026-11-19, practice 3). The slides are handed to
students together with their notes, so each note explains the slide's short wording in fuller sentences, adds detail that the balloons do not carry, and connects the slide to related slides and
chapters. A note gives no direction to a presenter, has no think-of statement, no prompt marker and no lambda. Length 60 to 140 words (at least 30 on title, part and resources slides, ruling 2 of
2026-11-14). The facts are those of notes 3.0.0, of the chapter's examples and of the result visuals; nothing is added that the slide or the run does not show.
RESULT_SAYS: for each code slide, the first of the two result balloons (what the run showed, in plain words); the second is the slide's takeaway.
Slide numbers: 1 title, 2 route, 3 questions, 4 part 1, 5 picture, 6 copy, 7 copytree, 8 copy2, 9 move, 10 part 2, 11 picture, 12 unlink, 13 rmtree, 14 dry run, 15 send2trash, 16 Kare,
17 part 3, 18 picture, 19 listing, 20 walk, 21 sizes, 22 mkdir, 23 Multics, 24 part 4, 25 picture, 26 zipwrite, 27 zipmodes, 28 extract, 29 archives, 30 Katz, 31 zlib, 32 part 5, 33 picture,
34 backup, 35 selective, 36 large, 37 dates, 38 current, 39 summary, 40 practice, 41 resources."""
__version__ = "3.1.0"

NOTES = {
    "title": "This chapter of the book, Organizing Files, moves from single files to whole folders: copying, moving, deleting, listing, walking and packing them into ZIP archives. The deck has nineteen code examples that run on the "
             "chapter page, four true stories about the people behind these tools, and an everyday picture for every concept. Each code slide shows the code in small steps, a balloon that explains each step, and what the run really printed, drawn as a table, "
             "a chart or a small picture. No result is typed in by hand. Slide 2 lays out the route through the five parts.",
    "route": "The table is the map of the chapter. Part 1 (slides 4 to 9) copies and moves, part 2 (10 to 16) deletes and stays safe, part 3 (17 to 23) lists and walks folders, part 4 (24 to 31) packs ZIP archives and part 5 (32 to 37) joins everything in four small programs. "
             "The last row collects the changes since the book, the summary, the practice questions and the links. The nineteen examples of the table are the same ones that the chapter-code tab of the page lists, in the same order, so every slide has a page example to run. "
             "Slide 3 asks the two questions that the chapter answers.",
    "questions": "Two questions run through the whole chapter. The first asks which operations change the disk for good and how a program can show what it is about to do before it does it; the answer is built in part 2 (slides 12 to 14), with the dry run as its centre. "
                 "The second asks how a program visits every file of a folder tree and packs the result into one archive; the answer comes from the walk (slide 20) and the numbered backup (slide 34). "
                 "Keeping these two questions in mind makes the nineteen examples easier to sort: each one either changes files safely or finds them. Part 1, copying and moving, starts on slide 4.",
    "divider1": "Part 1 covers the shutil module's copying and moving tools. The four concepts on the left are shutil.copy for one file, copytree for a whole folder, copy2 for keeping the time stamp, and move for relocating and renaming. "
                "The table on the right lists the slides of this part with their titles. The one rule that separates them is that a copy leaves the original in place and a move does not. "
                "Every one of these functions returns the new path, which is how a program learns where its file ended up. Chapter 10 handled single files with open and Path; this part works on files as objects of the file system. Slide 5 gives the everyday pictures.",
    "A1": "The headline compares a copy to a photocopy and a move to carrying the original to another desk. The table pairs each concept of this part with an everyday picture: shutil.copy is the photocopier, copytree is photocopying a whole ring binder, "
          "copy2 is a photocopy that keeps the date stamp of the original, and move is lifting the page and putting it in another tray. If the other tray already holds a page with the same name, the new page replaces it, "
          "and slides 6 to 9 return to that warning. The pictures are only memory aids: what a function really does is shown by its run. Slide 6 runs shutil.copy.",
    "copy": "Shutil.copy copies the contents of one file to a folder or to a new file name and returns the path of the copy. The first code box creates a temporary folder with a file a.txt and an empty folder box, so no real file of the reader is touched. "
            "The second box shows the two ways of calling it: copying into a folder keeps the file name, and copying to a file name gives the copy a new name. The result table lists the target given, the name of the copy and the returned path, "
            "and the arrows show the two copies leaving a.txt. The original stays where it was. Slide 7 copies a whole folder with copytree.",
    "copytree": "Shutil.copytree copies a folder together with every subfolder and file in it. The first box builds a folder box that holds a subfolder and a file. The second box calls copytree and returns the path of the new folder bak; "
                "calling it a second time is refused, because bak already exists, and the table marks that refusal. The third call adds dirs_exist_ok=True, which merges the copy into the existing folder instead of refusing. "
                "A merge replaces files that have the same name, so the option should be used on purpose. The small trees show the source and the copy holding the same entries. Slide 8 looks at what copying does to time stamps.",
    "copy2": "Copying a file normally gives the copy a new modification time, the moment of copying. Shutil.copy2 also copies the file's metadata, including the modification time, which is why it is the better choice for backups. "
             "The first box sets the file's times to a fixed moment with os.utime, so the run gives the same answer every time. The second box applies both functions and reads the time with a small helper function; the lesson of defining and calling helpers is in chapter 4. "
             "The bar chart shows the original and the copy2 copy with the same bar and the plain copy with a different one, and the table repeats this in numbers. Slide 9 moves files.",
    "move": "Shutil.move relocates a file or folder, and it renames in the same call when the target is a new file name. The second box moves a file into a folder and then moves it again to a new name, and the two rows of arrows show the old path and the path move returned. "
            "The third box shows the dangerous case: moving onto a file name that already exists silently overwrites it, so spam2/f.txt now holds the new text and the source file in spam is gone. Nothing warns the program, so a careful program checks first. "
            "When source and target are on different disks, move copies the file and then deletes the original. Part 2, on deleting, begins on slide 10.",
    "divider2": "Part 2 is about deleting, and about deleting safely. The four concepts are unlink and rmdir for one file or one empty folder, rmtree for a whole folder tree, the dry run that prints what would be deleted, and send2trash that uses the recycle bin. "
                "The headline gives the reason for the whole part: permanent deletion has no undo, so a program prints first and deletes afterwards. "
                "The functions of part 1 could overwrite a file by mistake; the functions of this part can destroy files on purpose, which is why the habit of rehearsing matters more here. The table on the right lists the slides. Slide 11 gives the everyday pictures.",
    "A2": "In the headline, permanent deletion is a paper shredder and the recycle bin is the waste-paper basket beside it. The table pairs os.unlink with the shredder, where nobody can fetch the page back, and shutil.rmtree with demolishing a whole room and everything in it. "
          "The dry run is a dress rehearsal: the actors say their lines and nothing on stage is damaged. The three pictures describe the three habits of this part: delete one thing deliberately, delete a tree only after counting what is inside, "
          "and always rehearse the list before running the real call. The real runs begin on slide 12 with os.unlink and os.rmdir, in a temporary folder.",
    "unlink": "Os.unlink deletes one file for good, and os.rmdir removes one folder, but only when it is empty. The first box creates a.txt, deletes it and prints that it no longer exists. "
              "In the second box, os.rmdir is tried on a folder that is not empty and Python raises an error, which the program catches and prints as a message; after the file inside is removed, the folder can go. "
              "The result table lists the three steps with what the run printed, the refusal is in red, and the small picture shows a.txt turning into gone, with no recycle bin in between. Neither call can be undone. Slide 13 removes a whole tree.",
    "rmtree": "Shutil.rmtree removes a folder and everything inside it in one call, which is why it is the most dangerous function of the chapter. The first box builds spam with one subfolder and one file, so two entries will disappear with it, and the printed list proves it. "
              "The second box calls rmtree, prints that spam no longer exists, and then calls it again on a folder that is gone with ignore_errors=True, which stays quiet; without that argument the second call would raise an error. "
              "The column chart compares what was under spam before and after. Because it cannot be undone, the habit on slide 14 comes first.",
    "dryrun": "A dry run prints what a program would delete, and the delete call is kept as a comment until the list is right. The first box creates three small files, one with the strange extension rxt. The second box uses a pattern with a typo, "
              "and printing the matches shows at once that it would hit the wrong file. The third box loops over the text files and prints would delete for each, while the deleting line stays a comment. "
              "The table puts the two patterns side by side, red for the typo and green for the right list. Only when the printed list is right is the comment mark removed. Slide 15 shows a safer tool, send2trash.",
    "compare_send2trash": "The table sets os.unlink beside send2trash, row by row: where the file goes, whether it can be recovered, where the function comes from, and whether it runs on the chapter page. "
                          "Os.unlink sends the file nowhere and it cannot come back. Send2trash moves it to the recycle bin, where it stays until the bin is emptied. "
                          "Send2trash is a third-party module installed with pip, so it is not part of the standard library and the page cannot run it; it is shown here for comparison only. "
                          "When a program deletes files that a person created, sending them to the bin is the kinder default. The story of the bin's icon follows on slide 16.",
    "kare": "In 1983 Susan Kare drew the trash can icon for the first Macintosh, working with Andy Hertzfeld at Apple Computer in California; the Macintosh shipped in 1984. Pictures made commands friendly for people who had never used a computer, "
            "and the bin taught a whole generation that deleting is a move to a place from which a file can be fetched back. That is exactly what send2trash on slide 15 does, while os.unlink behaves like the shredder. "
            "The picture, the credit and the live read link below the text belong to this story. Of the functions met so far, those that can still be undone are the ones that copy; those that cannot are unlink, rmdir and rmtree. Part 3, folders and trees, begins on slide 17.",
    "divider3": "Part 3 is about folders and trees. The four concepts are listdir and glob for reading one folder, walk for visiting a whole tree, folder sizes for adding up bytes while walking, and mkdir for making folders. "
                "The headline says the order of the part: one folder is listed first, and then a whole tree is walked. A folder tree is like a building where floors hold rooms and rooms hold cupboards, and slide 18 draws that picture. "
                "Walking is the loop from chapter 3 applied to a tree whose size is not known in advance, and a walk can count every folder of a laptop in a second. The table on the right lists the slides of this part.",
    "A3": "The headline compares a folder tree to a building: floors hold rooms and rooms hold cupboards. The table pairs os.walk with a caretaker's round, opening each door and looking in each cupboard before going one level further down. "
          "Mkdir is building a new empty room, and with parents=True it builds the corridor leading to the room as well. Listdir and glob are reading the door plates of one floor, either all of them or only those that match a pattern. "
          "The building also explains why the order of a visit matters: a caretaker may finish a floor before the cupboards, or the other way round, and slide 20 shows both orders. Slide 19 lists one folder in four ways.",
    "listing": "Listing one folder can be done in four ways, and each returns something different. The first box builds a folder spam that holds a subfolder, a PDF and a text file, and the subfolder holds one more text file. "
               "In the second box, os.listdir gives plain names, iterdir gives Path objects that know whether they are folders, glob lists only the entries of one folder that match a pattern, and rglob descends into every subfolder. "
               "The table puts each call next to what it returned, and the small tree shows the same files. So the text file inside eggs is found by rglob and not by glob. The Path methods are those of chapter 10. Slide 20 walks the whole tree.",
    "walk": "Os.walk visits a folder and then each folder below it, and at every step it hands over three values: the folder's path, the list of its subfolders and the list of its files. The second box loops over the walk with the for loop of chapter 3. "
            "Sorting the subfolders fixes the order of the visit, so the printed lines are the same on every run. Each table row is one step, and the small tree shows the route: spam, then eggs, then bacon, then eggs2. "
            "The third box sets topdown=False, so the subfolders are visited before the folder that holds them and the start folder comes last, as the grey line under the tree prints. Slide 21 uses the walk to add up bytes.",
    "sizes": "A walk can add up how much space each folder uses. For every folder the walk hands over, the code adds the sizes of the files directly in it and keeps the sum in a dictionary, then prints the dictionary and the total. "
             "The bar chart shows the bytes of the files directly in each folder, and the table lists the folders with their files and bytes, with the total at the bottom. The run printed 300 bytes for spam, one file, and 200 bytes for eggs, two files of 120 and 80, "
             "so the total of 500 is the sum over every folder, which is why it is not simply the largest folder. The same loop with a size limit finds big files, on slide 36. Slide 22 builds folders with mkdir.",
    "mkdir": "Path.mkdir makes one folder, and it refuses when the folder above it does not exist, so the first box catches the error and prints a message, drawn as the red row of boxes in the result. "
             "The second box passes parents=True, which builds the whole chain of missing folders at once, and exist_ok=True, which accepts a folder that is already there instead of raising an error. "
             "The small green tree shows x and y, and the teal line prints everything below x. With these two options a program can be run twice without failing the second time, which is the safe default for set-up code. "
             "The story of where the folder tree came from is on slide 23.",
    "multics": "In 1965, at the Fall Joint Computer Conference, Peter G. Neumann and R. C. Daley presented a paper on a file system for Multics. Their idea was folders holding folders holding files, so that many users could share one disk and each manage their own part. "
               "Unix kept the same tree, and os.walk descends it folder by folder today, which is why a walk can reach every file on a computer from a single starting point. The portrait, the credit and the live read link belong to this story. "
               "The tree that part 3 walked is therefore a design of the 1960s that is still in every laptop. Part 4, on ZIP archives, begins on slide 24.",
    "divider4": "Part 4 is about ZIP archives: many files in one parcel and back again. The four concepts are ZipFile for opening an archive, compression for making it smaller, extract for taking files out, and make_archive for packing a whole folder in one call. "
                "A ZIP file is like a vacuum-packed suitcase: many things go in, one small parcel comes out, and everything can come out again unchanged. The standard-library zipfile module needs no installation, "
                "so every example of this part runs on the chapter page. The table on the right lists the slides. Slide 25 shows the suitcase picture.",
    "A4": "The headline compares a ZIP file to a vacuum-packed suitcase: many things, one small parcel, and everything comes out again. The table pairs compression with vacuum-packing clothes so that the same clothes fit in a much smaller bag, "
          "and extract with taking one shirt out of the case or emptying the whole case onto the bed. ZipFile is the suitcase itself: it is opened to pack, to add one more item or to look inside. "
          "The picture explains one more detail, that some clothes pack better than others: repeated text shrinks enormously, while a file that is already compressed hardly shrinks at all. Slide 26 writes a file into an archive and measures the saving.",
    "zipwrite": "Zipfile.ZipFile opens an archive, and the mode w starts a new one. The first box writes a file of repeated text into the archive with compress_type=ZIP_DEFLATED; without that argument the file is only stored, not shrunk. "
                "The second box reads the archive back and asks getinfo for each member's original size and stored size. The column chart compares the two sizes and the table lists the file name, both sizes and their ratio: "
                "the stored size is under one percent of the original, because repeated text compresses very well. Real documents shrink much less. Slide 27 shows the other modes of a ZIP file.",
    "zipmodes": "A ZipFile can be opened in four modes, and each one changes what may happen to an existing archive. In the first box, mode w starts the archive x.zip with one member. In the second, mode a adds to an archive that exists, "
                "and writestr stores a piece of text without needing a file on disk. In the third, namelist lists the members, and mode x tries to create an archive that exists and is refused, because x never overwrites. "
                "The table names the four modes w, a, r and x with what each did in the run, and the small chart shows one member after w and two after a. Mode r only reads. Slide 28 unpacks archives.",
    "extract": "An archive can be unpacked completely or one member at a time. The first box writes an archive with two members, one of them inside a subfolder, using writestr. In the second box, extractall unpacks every member into a folder and rebuilds the subfolders, "
               "and the printed list shows them. In the third, extract unpacks a single member, creates the target folder if it is missing, and returns the path of the new file. "
               "The small tree shows z.zip with its two members, and the table says which entries are files and which are folders. Member names in an archive are paths, so a program should only unpack archives it trusts. Slide 29 packs a whole folder in one call.",
    "archives": "The shutil module can pack and unpack a whole folder in one call each. The second box calls make_archive, which packs the folder spam into one ZIP and returns its name; the names inside the ZIP keep the folder name. "
                "The third box calls unpack_archive, the one-call way back, which guesses the format from the file name. The table puts the members inside the ZIP beside what appeared after unpacking, "
                "and the three chips with arrows draw the way: the folder spam, the archive, the folder un. For a quick backup these two calls are enough; for control over every member, the zipfile calls of slides 26 to 28 are needed. The history of the format is on slide 30.",
    "katz": "On 14 February 1989, Phil Katz of PKWARE and Gary Conway released the ZIP format into the public domain. Katz had been sued over his earlier program PKARC, so they designed a new, open format that any program could read or write. "
            "That openness is the reason Python's zipfile module can read archives made by any tool, and every ZipFile call of this chapter works on that same structure. The picture of the PKZIP floppy disk, its credit and the live read link belong to this story. "
            "Slide 31 tells the story of the compression engine that sits inside most ZIP files.",
    "zlib": "On 1 May 1995, Jean-loup Gailly and Mark Adler released zlib 0.9, a free library for the DEFLATE method. It was written by collaborating over the internet and was first needed by the libpng image library. "
            "Programs needed compression that no company owned and no patent blocked, and zlib supplied it. When a write asks for ZIP_DEFLATED, Python's zipfile hands the bytes to zlib, so the saving measured on slide 26 comes from this library. "
            "The portrait, the credit and the live read link belong to this story. Part 5, the programs that use everything so far, begins on slide 32.",
    "divider5": "Part 5 has four programs that use everything so far. The four concepts are backupToZip, selective copy, big files and date renaming. A practice program is like a driving lesson on an empty car park: the real skill with no real risk, "
                "because every program works in its own temporary folder. Each program combines earlier parts: the walk of part 3, the copy and move of part 1 and the ZIP calls of part 4. The date renaming also uses the regular expressions of chapter 9. "
                "The table on the right lists the slides. Slide 33 shows the picture of the driving lesson.",
    "A5": "The headline compares a practice program to a driving lesson on an empty car park: every move is real and no damage is possible. The table pairs backupToZip with a nightly photocopy of the whole filing cabinet, numbered so that no old copy is lost, "
          "and selective copy with a librarian who copies only the blue-covered books from every shelf. The last row is relabelling every folder when an office switches from the American to the European calendar. "
          "Each picture matches the program that follows it. The four programs are chosen because real tasks look like them. Slide 34 builds the numbered backup.",
    "backup": "This is the fifth project of the book, a backup into a numbered ZIP. The second box holds the function: it finds the first free number, walks the folder and writes every file into the new ZIP, then returns the archive's name. "
              "The third box makes a small tree and runs the function twice, which produces spam_1.zip and then spam_2.zip, so the second run never overwrites the first. "
              "In the result column, the small tree shows the folder that is backed up, the two amber chips show the archive names, and the table lists the members of the first archive. The column chart says that both archives hold the same number of files. "
              "The function is the kind of helper that chapter 4 introduced. Slide 35 copies only the PDFs of a tree.",
    "selective": "Selective copy walks a tree and copies only the files of one type. The code boxes in the left column build a source tree with two subfolders and an empty dest folder, with four files of which three are PDFs, one of them with capital letters, "
                 "and then a walk copies each file whose lower-case name ends with pdf. Lower-casing the name first is what lets the file written with capital letters be found. "
                 "The bar chart in the result column counts the PDFs in src, the other files and the copied files, and the table says for each of the four files whether it was copied. The text file stays out, and the source keeps all four files. Slide 36 finds the big files of a tree.",
    "large": "Finding the big files of a tree is a walk with a size test. The first code box walks every folder of the tree, including sub, and keeps the files above one thousand bytes in a dictionary. "
             "The second sorts the names by size, the biggest first, and prints them with their sizes. The bar chart in the result column shows the sizes of the files that were kept, and the table lists all four files with their bytes and a green flag for those above the limit. "
             "Changing the limit changes the list, and the same loop with the sums of slide 21 would report folders instead of files. Slide 37 renames files by swapping day and month.",
    "dates": "This program renames files whose names carry an American date, month-day-year, into the European order, day-month-year. The three code boxes show the three names, of which two carry a date; a pattern that keeps month, day and year as three groups; "
             "and a loop where sub swaps groups one and two and shutil.move renames the file. The pattern is a regular expression, the subject of chapter 9. The table shows the names before and after, green for the renamed ones, "
             "and the two chips spell out 01-02-2020 as month 01, day 02 becoming day 02, month 01. The name without a date, notes.txt, stays as it is. Slide 38 shows what current Python adds.",
    "current": "The table lists five things from the chapter and what current Python offers instead. Path.walk, since Python 3.12, gives the same three values as os.walk, from a Path object. The onexc argument of rmtree, also from 3.12, replaces onerror, which is deprecated. "
               "ZipFile.mkdir, since 3.11, adds an empty folder entry to an archive. Path.copy and Path.move, since 3.14, work without importing shutil, and the recurse_symlinks argument of glob, since 3.13, chooses whether glob follows symbolic links. "
               "The book's examples still run; the table is a guide to what may replace them in newer code. The summary is on slide 39.",
    "summary": "The five numbered sentences are the chapter in short. Copy keeps the original; move relocates and can overwrite. Unlink, rmdir and rmtree cannot be undone, so a program prints first. "
               "Os.walk gives the folder, its subfolders and its files at every step. ZipFile writes, appends and reads archives. A short program can back up, copy by type or rename in bulk. "
               "The column chart on the right shows how many code examples belong to each part, which is also a map of where the chapter spends its time: part 1 and part 5 hold the most. "
               "Each sentence can be traced to a slide with the same words. The practice questions follow on slide 40.",
    "practice": "The four questions are short drills, like finger scales before a performance, and each has its answer on a slide that was already shown. The first asks about copy and move (slides 6 to 9). "
                "The second asks why a program prints before os.unlink may run (slides 12 to 14). The third asks which three values every step of os.walk gives (slide 20). "
                "The fourth asks which ZipFile mode adds a file and which refuses to overwrite one (slide 27). An answer is best given in one sentence and then checked by running the example on the chapter page. The links come last, on slide 41.",
    "resources": "The cards collect the further reading for the chapter: the book chapter first, then the Python documentation for shutil, os.walk, zipfile and pathlib, the what's-new pages for Python 3.12 and 3.14, send2trash on the package index, "
                 "the ZIP format specification, the zlib home page, three history links from the stories and one video. Every link is live and each one belongs to something taught in the deck. "
                 "The chapter-code tab of the page holds all nineteen examples, to run again. This is the end of chapter 11.",
}

STORY_NOTES = {
    "kare": NOTES["kare"],
    "multics": NOTES["multics"],
    "katz": NOTES["katz"],
    "zlib": NOTES["zlib"],
}

RESULT_SAYS = {
    "copy": "The run printed the two new paths and the two copies.",
    "copytree": "The second call was refused; dirs_exist_ok merged it.",
    "copy2": "copy2 kept the time stamp; plain copy did not.",
    "move": "The file moved, was renamed, and the old text was overwritten.",
    "unlink": "The file is gone for good; the non-empty folder was refused.",
    "rmtree": "The whole tree is gone; a missing folder is ignored.",
    "dryrun": "The typo pattern listed the wrong file; the list came first.",
    "listing": "Four calls, four different lists of the same folder.",
    "walk": "One line per folder, with its subfolders and files.",
    "sizes": "spam holds 300 bytes, eggs 200; the total is 500.",
    "mkdir": "The missing parent was refused; parents=True built x/y.",
    "zipwrite": "50000 bytes shrank to under one percent.",
    "zipmodes": "Mode a added a member; mode x refused to overwrite.",
    "extract": "Both members came out, with their subfolder rebuilt.",
    "archives": "snap.zip held the tree; unpacking rebuilt it as un.",
    "backup": "spam_1.zip and spam_2.zip, each holding two files.",
    "selective": "The three PDFs were copied; the text file stayed.",
    "large": "Three files are above 1000 bytes; huge.bin is biggest.",
    "dates": "Two names were swapped to day-month-year; notes.txt stayed.",
}
