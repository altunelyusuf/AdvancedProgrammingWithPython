"""Chapter 11 deck speaker notes, version 3.0.0: one note for every slide of deck 3.0.0, 60 to 140 words (at least 30 on the title, part and resources slides). Each note says what to
point at, what to say about it, and what the next slide brings (ruling 2 of 2026-11-14). The facts are those of notes_v2 of the chapter 11 deck, of the chapter's examples and of
the result visuals; nothing is added that the slide does not show."""
__version__ = "3.0.0"

NOTES = {
    "title": "Welcome to chapter 11, Organizing Files. Point at the cards on the slide: nineteen code examples that run on the chapter page, four true stories, and an everyday picture for every concept. "
             "This chapter moves from one file to whole folders: we copy, move, delete, walk and archive them. Every code slide shows the code, a plain explanation, and what the run printed, drawn as a table, a chart or a small picture. "
             "Say that no result is typed in by hand; each one comes from a real run. The next slide shows today's route through the five parts.",
    "route": "Point at the table: five parts, and for each part the range of slides and the number of code examples. Part one copies and moves, part two deletes and stays safe, part three lists and walks folders, "
             "part four packs ZIP archives, and part five joins everything in four small programs. The last row lists the changes since the book, the summary, the practice questions and the links. "
             "Tell the class that the chapter-code tab of the page holds the same nineteen examples in this same order, so they can run each one. The next slide asks two questions to carry through the chapter.",
    "questions": "Point at the two numbered cards. The first question is which operations change the disk for good, and how a program can show what it will do before it does it. The second is how a program visits every file of a folder tree "
                 "and packs the result into one archive. Each card says on which slides the answer comes: the shredder and the dry run for the first, the walk and the backup project for the second. "
                 "Ask the class to guess the answers now and to check them when the slides come. The next slide opens part one, copying and moving.",
    "divider1": "Part one is about copying and moving files with the shutil module. Point at the four words on the left, shutil.copy, copytree, move and the time stamp, and at the table on the right that lists the slides of this part. "
                "Say the key difference in one line: a copy keeps the original, a move does not. Ask the class to watch what each function returns, because the returned path is how a program knows where the new file went. "
                "The next slide gives an everyday picture for these four ideas.",
    "A1": "Point at the headline: a copy is a photocopy, a move is carrying the original to another desk. Read two rows of the table, the photocopier for shutil.copy and the ring binder for copytree, and tell the class that every row pairs "
          "a chapter concept with something from daily life. Move is lifting the page and putting it in another tray; if the tray already holds the same page, it is replaced, and that warning comes back in the examples. "
          "Ask which function the class expects to return the new path. The next slide runs shutil.copy.",
    "copy": "Point at the first code box: a new temporary folder, one small file a.txt and one empty folder box, so no real file is touched. In the second box, copying into a folder keeps the name, copying to a file name renames the copy, "
            "and copy returns the new path. Then point at the table in the result: it shows the target we gave, the name of the copy and the returned path, and the arrows draw the two copies leaving a.txt. "
            "The green line shows what the folder box now holds. The next slide copies a whole folder with copytree.",
    "copytree": "Point at the first code box: a folder box that holds a subfolder and a file. The second box calls copytree, then calls it again. Point at the two small trees in the result: box on the left, bak on the right, "
                "with an arrow between them, and the green line says that both hold the same entries. In the table, the second call is marked as refused because the folder bak already exists. "
                "The third call adds dirs_exist_ok equals True, and that merges into the existing folder. Ask what a merge would overwrite. The next slide compares copy and copy2.",
    "copy2": "Point at the first box: os.utime sets the file's times to a fixed moment in 2001, so the run is repeatable. In the second box, copy2 and copy are both applied, and a small function t reads the modification time. "
             "Point at the bar chart: the original and the copy2 copy have the same bar, and the plain copy has a taller one because it is stamped with the moment of copying. The table beside it says the same in numbers, "
             "with green for the same time and red for a different one. Say that copy2 is the one to use for backups. The next slide moves files.",
    "move": "Point at the second code box: moving a file into a folder, then moving it again to a new name, which relocates and renames in one step. In the result, the two rows of boxes with arrows show the old path and the path "
            "that move returned. Now point at the third code box and the table on the right: moving onto a file name that already exists silently overwrites it, so spam2 f.txt now holds the new text, "
            "and the source in spam is gone. Stress that nothing warned us. The next slide opens part two, deleting safely.",
    "divider2": "Part two is about deleting, and about staying safe. Point at the four words on the left: unlink, rmtree, the dry run and send2trash, and at the list of slides on the right. The headline says that permanent deletion has no undo, "
                "so we print before we delete. Ask the class to remember a time when they deleted the wrong file, and say that the habit shown in this part prevents that. "
                "The next slide gives the everyday picture for deleting: the paper shredder and the waste-paper basket.",
    "A2": "Point at the headline: permanent deletion is a paper shredder, and the recycle bin is the waste-paper basket beside it. Read the rows for unlink, the shredder where nobody can fetch the page back, "
          "and for rmtree, demolishing a whole room with everything in it. The dry run is a dress rehearsal: the actors say their lines and nothing on stage is damaged. "
          "Tell the class that the habit of this part is to rehearse first. The next slide runs os.unlink and os.rmdir for real, in a temporary folder.",
    "unlink": "Point at the first code box: we create a.txt, delete it with os.unlink and print that it no longer exists. In the second box, os.rmdir is tried on a folder that is not empty, the error is caught, "
              "and the message is printed; then the file is removed first and the folder after it. In the result, the table lists the three steps with what the run printed, the refusal is in red, "
              "and the small picture shows a.txt turning into gone with no recycle bin. Say that unlink cannot be undone. The next slide removes a whole tree.",
    "rmtree": "Point at the first code box: a folder spam with one subfolder and one file, so two things will disappear with it, and the printed list proves it. The second box calls rmtree and prints that spam no longer exists, "
              "then calls it again on the missing folder with ignore_errors True, which stays quiet. In the result, the small tree on the left is crossed by the red rmtree box, and the column chart compares "
              "the number of things under spam before and after. Ask the class why this call is more dangerous than unlink. The next slide shows the habit that makes it safe.",
    "dryrun": "Point at the three code boxes. First, three small files, one with the strange extension rxt. Second, a pattern with a typo that matches the wrong file, and the list is printed instead of deleting. Third, "
              "the loop prints would delete for each text file, and the delete line is only a comment. In the result, the table puts the two patterns side by side with the verdict, red for the typo and green for the right list, "
              "and the chips show which files would be touched. Only when the list is right do we remove the comment mark. The next slide shows a safer deleting tool, send2trash.",
    "compare_send2trash": "Point at the table that sets os.unlink beside send2trash. Read the rows in order: where the file goes, whether you can get it back, where the function comes from, and whether it runs on the chapter page. "
                          "Unlink sends the file nowhere and it cannot come back; send2trash puts it in the recycle bin until the bin is emptied. Say that send2trash is a third-party module that you install with pip, "
                          "so it is not part of the standard library and the page does not run it. When in doubt, send the file to the bin. The next slide tells where the bin icon came from.",
    "divider3": "Part three is about folders and trees. Point at the four words on the left: listdir and glob, walk, folder sizes and mkdir, and at the list of slides on the right. The headline says that we list one folder first, "
                "and then walk a whole tree. A folder tree is a building where floors hold rooms and rooms hold cupboards, and the next slide draws that picture. "
                "Ask the class how many folders their own laptop has, and say that a walk can count them in a second.",
    "A3": "Point at the headline: a folder tree is a building, floors hold rooms, and rooms hold cupboards. Read the caretaker's round for walking a tree, opening each door and looking in each cupboard before going one level down. "
          "Then read the row for mkdir: building a new empty room, where parents True builds the corridor leading to it as well. Listdir and glob are reading the door plates of one floor, "
          "all of them or only the ones that match a pattern. The next slide lists one folder in four different ways.",
    "listing": "Point at the first code box: a folder spam that holds a subfolder, a PDF and a text file, and the subfolder holds one more text file. The second box lists it four ways. In the result, the table puts each call "
               "next to what it returns: listdir gives names, iterdir gives Path objects that know whether they are folders, glob stays in one folder, rglob goes down into every subfolder. "
               "The small tree on the right shows the same files. Ask which call finds the text file inside eggs, and why. The next slide walks the whole tree.",
    "walk": "Point at the second code box: a for loop over os.walk gives three values at every step, the folder, its subfolders and its files. Sorting the subfolders fixes the order of the visit. "
            "In the result, each row of the table is one step, and the small tree shows where the walk goes: spam first, then eggs, then bacon, then eggs2. Now point at the third box: "
            "with topdown False the subfolders come first and the start folder comes last, and the grey line under the tree prints that last folder. The next slide uses the walk to add up bytes.",
    "sizes": "Point at the code box: for every folder that the walk hands over, we add up the sizes of its files and keep them in a dictionary, then print the dictionary and the total. In the result, "
             "the bar chart shows the bytes of the files directly in each folder, and the table lists the folders with their files and their bytes, with the total at the bottom. "
             "The three files have 300, 120 and 80 bytes, so the total is 500. Ask which folder is the largest and why the total is not just the biggest folder. The next slide builds folders with mkdir.",
    "mkdir": "Point at the first code box: mkdir makes one folder, and it refuses when the folder above it does not exist, so the error is caught and printed. In the result, the first row of boxes shows the refused call "
             "with a red message. The second box uses parents True, which builds the whole chain, and exist ok True, which accepts a folder that is already there. The small green tree shows x and y, "
             "and the teal line prints everything below x. Say that these two options make a program safe to run twice. The next slide tells the story of the folder tree.",
    "divider4": "Part four is about ZIP archives, many files in one parcel and back again. Point at the four words on the left: ZipFile, compression, extract and make archive, and at the list of slides on the right. "
                "A ZIP file is a vacuum-packed suitcase: many things go in, one small parcel comes out, and everything can come out again. "
                "Ask the class when they last sent a ZIP file, and tell them that this part builds one from code. The next slide shows the suitcase picture.",
    "A4": "Point at the headline: a ZIP file is a vacuum-packed suitcase, many things, one small parcel, and they come out again. Read the row for compression, vacuum-packing clothes so that the same clothes fit in a much smaller bag, "
          "and the row for extract, taking one shirt out or emptying the whole case onto the bed. ZipFile is the suitcase itself: open it to pack, to add one more item or to look inside. "
          "The next slide writes a file into an archive and measures how much it shrinks.",
    "zipwrite": "Point at the first code box: a file of repeated text, then a ZipFile opened with mode w, and write with compress type ZIP_DEFLATED, which is the compression that really shrinks it. The second box reads the archive back "
                "and asks getinfo for the original size and the stored size. In the result, the column chart compares the two sizes, and the table lists the file name, the two sizes and their ratio. "
                "The stored size is under one percent of the original, because repeated text compresses very well. The next slide shows the other modes of a ZIP file.",
    "zipmodes": "Point at the three code boxes. First, mode w starts the archive x.zip with one member. Second, mode a adds to an archive that exists, and writestr stores text without a file on disk. "
                "Third, namelist lists the members, and mode x tries to create an archive that exists and is refused. In the result, the table names the four modes, w, a, r and x, with what each did in the run, "
                "and the small chart shows one member after w and two after a. Say that x never overwrites. The next slide unpacks archives.",
    "extract": "Point at the first code box: an archive with two members, one of them inside a subfolder, written with writestr. In the second box, extractall unpacks every member into a folder and rebuilds the subfolders, "
               "and the printed list shows them. In the third, extract unpacks one member, creates the target folder when it is missing, and returns the new path. In the result, the small tree shows z.zip "
               "with its two members, and the table says which entries are files and which are folders. The next slide packs a whole folder in one call.",
    "archives": "Point at the second code box: make archive packs the whole folder spam into one ZIP in a single call, and the names inside keep the folder name. The third box calls unpack archive, "
                "the one-call way back, and it guesses the format from the file name. In the result, the table puts the members inside the ZIP beside what appeared after unpacking, and the three chips with arrows draw the way: "
                "the folder spam, the archive, the folder un. Say that for a quick backup these two calls are enough. The next slide tells how the ZIP format became free.",
    "divider5": "Part five has four programs that use everything so far. Point at the four words on the left: backupToZip, selective copy, big files and date renaming, and at the list of slides on the right. "
                "A practice program is a driving lesson on an empty car park: the real skill, no real risk. Ask the class to predict the output of each program before the slide shows it, "
                "then run it on the page. The next slide shows the picture of the driving lesson.",
    "A5": "Point at the headline: a practice program is a driving lesson on an empty car park, every move is real and no damage is possible. Read the row for backupToZip, a nightly photocopy of the whole filing cabinet, "
          "numbered so that no old copy is lost, and the row for selective copy, a librarian who copies only the blue-covered books from every shelf. "
          "The last row relabels every folder when the office switches from the American to the European calendar. The next slide builds the numbered backup.",
    "backup": "This is project five of the book. Point at the second code box: the function finds the first free number, walks the folder, and writes every file into the new ZIP, then returns its name. "
              "The third box makes a small tree and runs the function twice. In the result column, the small tree shows the folder to back up, the two amber chips show spam_1.zip and spam_2.zip, "
              "and the table lists the members of the first archive. The column chart says that both archives hold the same number of files. The next slide copies only the PDFs of a tree.",
    "selective": "Point at the code boxes in the left column: a source tree with two subfolders and an empty dest folder, four files of which three are PDFs, one with capital letters, "
                 "and a walk that copies each file whose lower case name ends with pdf. In the result column, the bar chart counts the PDFs in src, the other files and the copied files, "
                 "and the table says for each of the four files whether it was copied. The text file stays out, and the source keeps all four files. "
                 "Ask why lower is needed. The next slide finds the big files of a tree.",
    "large": "Point at the code boxes in the left column. The first walks every folder of the tree, including sub, and keeps the files above one thousand bytes. The second sorts the names by size, "
             "the biggest first, and prints them with their sizes. In the result column, the bar chart shows the sizes of the files that were kept, and the table lists all four files with their bytes "
             "and a green flag for those above one thousand. Ask what would change if the limit were five hundred. The next slide renames files by swapping day and month.",
    "dates": "Point at the three code boxes in the left column: three names, two of which carry a month day year date; a pattern that keeps month, day and year as three groups; "
             "and a loop where sub swaps groups one and two and shutil.move renames the file. In the result column, the table shows the names before and after, green for the renamed ones, "
             "and the two chips spell out 01-02-2020 as month 01, day 02 becoming day 02, month 01. notes.txt stays as it is. The next slide shows what current Python adds to this chapter.",
    "current": "Point at the table: it lists five things from the chapter and what current Python offers instead. Path walk since 3.12 gives the same three values as os.walk, from a Path. "
               "The onexc argument of rmtree, also 3.12, replaces onerror, which is deprecated. ZipFile mkdir since 3.11 adds an empty folder entry. Path copy and Path move since 3.14 work without importing shutil, "
               "and recurse symlinks in glob since 3.13 chooses whether glob follows symbolic links. Say: run what the book printed, then check what changed. The next slide is the summary.",
    "summary": "Point at the five numbered sentences and read them aloud: copy keeps the original, move relocates and can overwrite; unlink, rmdir and rmtree cannot be undone, so print first; "
               "os.walk gives folder, subfolders and files at every step; ZipFile writes, appends and reads archives; and a short program can back up, copy by type or rename in bulk. "
               "The column chart on the right shows how many code examples belong to each part. Ask the class which of the five they would explain to a friend. The next slide has the practice questions.",
    "practice": "Point at the four numbered questions. They are finger scales: short drills before the performance. Each one has an answer on a slide already shown. The first asks about copy and move, "
                "the second why we print before os.unlink may run, the third which three values every step of os.walk gives, and the fourth which ZipFile mode adds a file and which refuses to overwrite one. "
                "Tell the class to predict first, then run each answer on the chapter page, and to explain it in one sentence. The last slide has the links.",
    "resources": "Point at the cards: the book chapter first, then the Python documentation for shutil, os.walk, zipfile and pathlib, the what's new pages for Python 3.12 and 3.14, "
                 "send2trash on the package index, the ZIP specification, the zlib home page, three history links from the stories, and one video. Every link is live. "
                 "Ask each student to pick one link and read it before the next class. Remind the class that the chapter-code tab of the page holds all nineteen examples to run again. This is the end of chapter 11.",
}

STORY_NOTES = {
    "kare": "Point at the picture of Susan Kare and read the first card: in 1983 she drew the trash can icon for the first Macintosh, working with Andy Hertzfeld at Apple Computer in California. "
            "The Macintosh shipped in 1984, and pictures made commands friendly for people who had never used a computer. Then link it to the chapter: send2trash moves a file into that same bin instead of deleting it, "
            "so the move can still be undone. Ask which functions of this chapter can still be undone, and which cannot. Point at the read link at the bottom. The next slide opens part three, folders and trees.",
    "multics": "Point at the portrait of Peter G. Neumann and read the first card: in 1965, at the Fall Joint Computer Conference, he and R. C. Daley presented a paper on a file system for Multics. "
               "Their idea was folders holding folders holding files, so that many users could share one disk and each manage their own part. Unix kept the same tree, and os.walk descends it folder by folder today. "
               "Ask the students to draw the tree of their own laptop on paper. Point at the read link at the bottom. The next slide opens part four, ZIP archives.",
    "katz": "Point at the picture of the PKZIP floppy disk and read the first card: on 14 February 1989 Phil Katz of PKWARE and Gary Conway released the ZIP format into the public domain. "
            "Katz had been sued over PKARC, so they designed a new, open format that any program could read or write. That openness is why zipfile can read archives from any tool, "
            "and every ZipFile call of this chapter uses that same structure. Ask why a free format helps a programmer. Point at the read link at the bottom. The next slide tells the story of the engine inside the compression.",
    "zlib": "Point at the portrait of Mark Adler and read the first card: on 1 May 1995 Jean-loup Gailly and Mark Adler released zlib 0.9, a free library for the DEFLATE method, "
            "written over the internet and first built for the libpng image library. Programs needed compression that no company owned and no patent blocked. "
            "Python's zipfile hands the bytes to zlib whenever a write asks for ZIP_DEFLATED. Ask what would break if compression were owned by one company. Point at the read link at the bottom. The next slide opens part five, the programs.",
}
