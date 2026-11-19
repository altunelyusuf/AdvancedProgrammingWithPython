"""Chapter 10 deck speaker notes, version 3.0.0: the notes are READER notes (handover of 2026-11-19, practice 3). The slides are handed to students together with their notes, so each note explains the slide's
short wording in fuller sentences, adds detail that the balloons do not carry, and connects the slide to related slides and chapters. A note gives no direction to a presenter, has no think-of statement, no
prompt marker and no lambda. Length 60 to 140 words (at least 30 on title, part and resources slides, ruling 2 of 2026-11-14). The facts are those of the chapter's examples, of the result visuals and of the
notes of deck 2.0.0; nothing is added that the slide or the run does not show.
RESULT_SAYS: for each code slide, the first of the two result balloons (what the run showed, in plain words); the second is the slide's takeaway.
Slide numbers: 1 title, 2 route, 3 questions, 4 part 1, 5 picture, 6 pathobjects, 7 pathlib story, 8 picture, 9 locations, 10 anatomy, 11 part 2, 12 picture, 13 folders, 14 glob, 15 fileinfo, 16 part 3,
17 picture, 18 wholefile, 19 UTF-8 story, 20 openclose, 21 readmethods, 22 picture, 23 withstatement, 24 modes, 25 encoding, 26 part 4, 27 picture, 28 shelve, 29 dbm story, 30 json, 31 JSON story,
32 part 5, 33 picture, 34 madlibs, 35 regexsearch, 36 quizquestion, 37 quizfiles, 38 current, 39 summary, 40 practice, 41 resources."""
__version__ = "3.0.0"

NOTES = {
    "title": "This chapter of the book, Reading and Writing Files, shows how a program names a file with a path, makes folders, reads and writes text, and keeps Python values between two runs. The deck has eighteen code examples "
             "that run on the chapter page, four true stories about the people behind these tools, and an everyday picture for every concept. Each code slide shows the code in small steps, a balloon that explains each step, and what the run "
             "really printed, drawn as a table, a chart or a small picture. Slide 2 lays out the five parts, and chapter 11 continues with whole folders and archives.",
    "route": "The table is the map of the chapter. Each row is one of the five parts, with the slides it covers, the number of code examples in it and the tools you will run. The last row covers the newer features of Python, the summary, "
             "the practice questions and the links. The same eighteen examples are listed in the Slide code tab of the chapter page, in this order, so a slide and its tab can be opened side by side. The parts build on each other: paths first, "
             "then folders, text, saved values and programs. Part 1 starts on slide 4.",
    "questions": "Two questions run through the chapter, and the deck comes back to them at the end. The first asks which tools only compute a path, which ask the file system a question and which change a file or a folder; the summary on "
                 "slide 39 sorts them. The second asks where the book's printed output and programs differ from current Python; slide 37, the quiz files of Project 4, and slide 38, the newer features, answer it. Every tool of the chapter is one of "
                 "the three kinds: compute, ask or change. Holding that sort in mind makes each later slide easier to place.",
    "divider1": "Part 1 is about filepaths. A path is the address of a file, and pathlib turns that address into an object that you can join with a slash, ask where it starts and take apart. The four cards on the slide are the ideas of the part: the "
                "path object, the working directory, absolute and relative paths, and the parts of a path. Slides 5 to 10 cover them in code and in pictures, and the same ideas return in part 2, where paths are used to build folders and find files.",
    "A1": "The headline compares a filepath to a street address: it says in which building, on which floor and in which room to look. The cards give one picture for each idea. An absolute path is a full postal address that works from anywhere, "
          "while a relative path is a direction such as two doors down from here. Joining paths is gluing address pieces together, and the separator is the local way of writing an address. Slide 6 shows the same ideas in code, "
          "and slide 9 returns to absolute and relative paths.",
    "pathobjects": "Path() joins the names it is given with the separator of the computer and returns one path object, so the result prints with slashes on Linux and macOS. The slash operator joins in the same way. "
                   "A Windows path object writes the same names with backslashes, which shows that the separator belongs to the computer and not to the names. Two plain strings cannot use the slash, because neither one is a path object, "
                   "and Python raises a TypeError. Slide 7 tells the story of the proposal that made paths objects, and slide 10 takes a path apart.",
    "pathlib": "On 30 July 2012 Antoine Pitrou, a Python core developer, wrote PEP 428, which proposed that a filesystem path should be an object with its own methods and not a plain string. The proposal went through the Python Enhancement "
               "Proposals process and shipped in Python 3.4 in March 2014. Before that, separate functions of the os.path module worked on strings and were clumsy and hard to read. Path('spam', 'bacon', 'eggs') and the slash operator "
               "of this chapter come from that proposal, and slide 6 uses both. The link on the slide leads to the proposal itself.",
    "A2": "The headline compares the working directory to the room you are standing in: every short direction starts from there. Path.cwd() is a card that already carries the address of that room, Path.home() carries the address of your "
          "front door, and os.chdir() is walking into another room, after which next door means something else. The card, as Path() shows, is not the house: a path object only holds an address. Slide 9 runs these calls, "
          "and slide 10 reads an address label piece by piece.",
    "locations": "The working directory is the folder that every short path starts from, and os.chdir makes the new scratch folder that directory. Path.cwd() and Path.home() both start at the root of the disk, so is_absolute answers True for "
                 "them, while a path that names only its own parts, such as spam/bacon/eggs, is relative and answers False. A relative path is read from the working directory: the dot means this folder, and resolve adds the full address in front. "
                 "Part 2 depends on this, because mkdir and glob also start from the working directory. Slide 8 gave the pictures.",
    "anatomy": "A pure path works only on the text of a path and never touches the disk, so a Windows path can be taken apart on any computer. The drive is the letter, the name is the last part, the stem is the name without its ending "
               "and the suffix is the ending. The parts attribute lists every piece, parents climbs up one folder at a time, and with_suffix gives a new path with another ending without changing anything on disk. "
               "These pieces are the parts of the address labels on slide 8. Part 2 starts on slide 11 and uses paths to create real folders.",
    "divider2": "Part 2 builds folders, finds files and asks the file system questions. makedirs and mkdir create folders, glob finds files by a pattern, and exists and stat tell you whether a path is there and how big and how old it is. "
                "Only makedirs and mkdir change the disk, by adding folders; glob, exists and stat only ask. The four cards on the slide give the ideas, and slides 12 to 15 show them in pictures and in code. Part 3 then opens "
                "files and starts to read and write the text inside them.",
    "A3": "The headline compares a folder to a box inside a box, and a glob pattern to a search card that says every box whose label looks like this. makedirs builds every missing shelf on the way, mkdir adds one new box to a shelf that is "
          "already there, and exists is the yes or no question of whether a label is on any shelf. Stat reads the weight and the date stamp of a parcel, and glob is the librarian who walks the shelves with your card. "
          "Slides 13 to 15 turn each picture into code.",
    "folders": "os.makedirs builds every missing folder on the way, so one call creates delicious, walnut and waffles together. Path.mkdir makes exactly one folder and refuses when a parent is missing; exist_ok=True allows that the "
               "folder already exists. rglob walks the whole tree below a folder, and the star pattern takes every name, so the printed list is the tree that the calls built. The work happens in a fresh scratch folder, "
               "so none of your own files is touched. Chapter 11 returns to folder trees with os.walk.",
    "glob": "A question mark stands for exactly one character and a star for any number of them, so project?.txt fits project1 and project2 but not project10, which has two characters after the word. glob returns paths and not names, "
            "which is why the code takes the name of each path, and sorted fixes the order of the printout. The third pattern, a star alone, takes every file of the folder, including notes.csv. "
            "Slide 35 uses glob again to search a whole folder for a pattern.",
    "fileinfo": "exists answers a plain yes or no, and a missing path is not an error: before the file is written it says False. After writing, the path exists and is a file, and the dot is a folder. stat reports the size in bytes, thirteen "
                "for Hello, world!, and the last-modified time. The code sets a fixed time with utime, so the printout never changes between runs. Python 3.12 deprecates st_ctime on Windows, and slide 38 lists this "
                "and other changes. These tools only ask the file system and change nothing.",
    "divider3": "Part 3 is about reading and writing text. A file is opened, read or written, and closed again, and the with statement does the closing for you. The modes w, a and x decide what happens to text that is already in the file, and "
                "the encoding decides how letters become bytes. Slides 17 to 25 take these ideas in order, from whole-file calls to the cursor, with, modes and encoding. Part 4 then saves whole Python values instead of text.",
    "A4": "The headline compares working with a file to a library loan: you open the book, you read or write, and you must give it back. The cards separate a plain text file, a note you can read with your own eyes, from a binary file, "
          "a sealed parcel for the right machine. open() is the librarian's desk, the file object is the borrowed book with a bookmark, read takes the whole book from the bookmark on, and close returns it. "
          "Slides 18 to 21 run these steps.",
    "wholefile": "Path.write_text and Path.read_text handle a whole file in one call. write_text returns the number of characters it wrote, thirteen for Hello, world!, and not the number of bytes. The accent of café takes two bytes in UTF-8, so "
                 "four characters need five bytes in the file, and stat shows that size. A binary file holds bytes and not text, so write_bytes and read_bytes give the three values 0, 1 and 255 back exactly. "
                 "Slide 19 tells where UTF-8 comes from, and slide 25 compares encodings.",
    "utf8": "In September 1992 Ken Thompson and Rob Pike of Bell Labs designed UTF-8 in a diner in New Jersey and then finished it at Bell Labs in Murray Hill. The first working code ran on 4 September, and the proposal went to X/Open on 8 "
            "September. The rival encoding FSS/UTF could not recover a byte stream that was picked up in the middle of a character, and UTF-8 can. The encoding='utf-8' you pass to open() names this format, which writes every character as "
            "one to four bytes. Slide 18 showed the two bytes of the accent, and slide 25 shows the encodings side by side.",
    "openclose": "open() returns a file object. The mode w means write and starts a new empty file, and each write returns the number of characters it wrote: fourteen for the first line and twenty-five for the second. close finishes the job "
                 "and frees the file. Mode r, reading, is the default; read returns the whole text, and the closed attribute says whether the file is shut. Forgetting close is a common mistake, and slide 23 shows the with "
                 "statement, which closes for you. Slide 21 reads the same kind of file line by line.",
    "readmethods": "A file object has a cursor, like a bookmark, and tell shows where it stands. readline takes one line and moves the cursor to 6, readlines takes the rest and moves it to 20, and read at the end gives an empty string. "
                   "seek(0) rewinds the cursor to the start, so read(5) takes the five letters of roses. The strip in the picture colours the characters that each call took. This is the loan of slide 17 seen from the "
                   "inside, and slide 23 shows the safe way to close the book.",
    "A5": "The headline compares a with block to a borrowing slip that returns the book by itself, even if you drop everything and run. The cards give the writing modes as a notebook: w brings a clean page, a continues, and x refuses to "
          "touch a used one. write adds one more line, write_text is dictating a whole letter, read_text asks for it back, and readlines tears the letter into strips. A context manager is a hotel porter who opens the door and "
          "shuts it again. Slides 23 and 24 show the with block and the modes.",
    "withstatement": "Inside the with block the file is open, and write returns 3 for abc. When the block ends, the with statement closes the file for you, so closed is True afterwards. The second example raises an error inside the block on "
                     "purpose, and the file is still closed, which is why with is the safe way: a close call that is skipped by an error leaves the file open. The same statement works with any context manager, "
                     "and the porter picture on slide 22 shows the idea. Slide 24 uses with for the modes.",
    "modes": "The mode decides what happens to old text. Mode w empties the file first, so after A, B and C the file holds three lines, and the second w leaves only D. Mode a adds to the end. The printout shows the whole file after "
             "every step, and the chart shows its size. Mode x creates a new file and refuses when the file exists, so the second block ends with a FileExistsError that the code catches. Choose x when an old file must never be overwritten. "
             "The notebook picture is on slide 22.",
    "encoding": "Say the encoding every time you open a text file. The same encoding that wrote café reads it back correctly. The wrong one either garbles the accent into replacement marks or stops with an error: ascii cannot read the byte "
                "0xc3. The same four letters take four bytes in latin-1, five in UTF-8 and eight in UTF-16. Python 3.10 adds an EncodingWarning that finds open() calls without an encoding, and slide 38 lists the newer defaults. "
                "The story of UTF-8 is on slide 19.",
    "divider4": "Part 4 keeps Python values between two runs of a program. A shelf is a dictionary that is kept in a file, with one value under each key, and json is a plain text format that other programs can read as well. The cards also carry a "
                "warning: a list changed in place is not saved, and a shelf that came from a stranger must never be opened. Slides 27 to 31 show both ways and the stories behind them. Part 5 puts everything to work in programs.",
    "A6": "The headline compares a shelf to a pigeonhole cupboard: every value sits in a slot with a label, and the cupboard stays when you go home. shelve.open() unlocks the cupboard and builds a new one when there is none, and the "
          "Shelf is the cupboard itself, a dictionary that lives in a file. json is a letter in plain language that any reader in any country can understand, which is the reason to choose it when another program has to read your data. "
          "Slide 28 runs the shelf, and slide 30 runs json.",
    "shelve": "A Shelf is a dictionary that stores every value pickled, and shelve.open('mydata') puts it in a file; here a plain dict plays the file, because a browser has no dbm backend. Keys and values come back as you stored them, and "
              "underneath the dict holds bytes. The trap is on the last box: a list changed in place is not saved, so the length stays 3, and assigning the list back to its key keeps the change and gives 4. "
              "Never open a shelf from a stranger, because opening it can run code. Slide 29 tells where the idea comes from.",
    "dbm": "In 1979 Ken Thompson, a programmer at AT&T Bell Laboratories in Murray Hill, New Jersey, wrote the first dbm, a small store that keeps a value under a text key. AT&T released it as part of Unix. A program needed to save "
           "a value and get it back by one key, with no server to run. That one-key, one-value shape is still what a Python dbm file offers today. shelve.open() gives the same shape, and Python's dbm package picks the backend file "
           "that holds your values, as slide 28 shows.",
    "json": "json.dumps turns a Python value into JSON text, and json.loads reads the text back. The first printout shows what changes on the way: JSON keys are always text, so the key 5 becomes the text 5, and a tuple becomes a "
            "list. That is why the value that comes back is not equal in every detail to the value that went in. Prefer json to a shelf when another program must read the data, because it is plain text. "
            "Slide 31 tells how JSON was written up, and slide 28 showed the shelf.",
    "divider5": "Part 5 has two practice programs and Project 4 of the book, the quiz maker. Mad Libs fills the blanks of a story file with re.sub, Regex Search finds a pattern in every text file of a folder, and Project 4 writes quiz files and answer "
                "keys at random. Each program uses only what parts 1 to 4 taught: paths, glob, reading, writing and a little randomness. Slides 33 to 37 follow, and slide 38 lists what current Python adds.",
    "A7": "The headline compares a project to a small workshop job: you read the files, you change them, and you write a new one. Project 4 is a teacher who shuffles the question cards and prints a new test for every student. "
          "Mad Libs is a party game with blanks in a story, and Regex Search is a detective with a magnifying glass going through every file in the folder. Practice programs are exercises at the piano, and the practice questions "
          "on slide 40 are the finger scales before the concert.",
    "madlibs": "The story file holds capital-letter blanks: ADJECTIVE, NOUN and VERB. The function fill hands out the next answer of an iterator, and re.sub calls it once for every blank it finds, so the blanks are filled in the order they "
               "appear. The answers come from a list instead of from typing, which makes the run repeat. The finished story is saved to a second file and printed. The same read, change and write steps return in Project 4 on "
               "slides 36 and 37.",
    "regexsearch": "The helper put writes a text file in a fresh scratch folder, and three small files give the search something to find: two text files and one csv file. glob picks the txt files only, so notes.csv is skipped. Each line is tested "
                   "with the pattern spam, and a hit prints the file, the line number and the line. SPAM in capital letters is not a hit, because the pattern is case sensitive. Slide 14 showed glob alone, "
                   "and chapter 11 continues with walks over whole trees.",
    "quizquestion": "Project 4 of the book makes random quiz files, and this slide builds one question. Five states stand in for the fifty of the book, and the seed makes the random choices repeat. The code picks a state, takes three wrong "
                    "capitals, adds the right one and shuffles the four options. Then it prints the question and the lettered options. The right capital is known from the dictionary, "
                    "and slide 37 uses it to write the answer key.",
    "quizfiles": "Step two writes the quiz and its answer key to two files. One loop makes one question per state: a question line holds the options and a key line holds the right letter. With four states, sample lists all four "
                 "capitals in a random order, so each question shows every capital once. Both files are written and read back. The book prints a different layout and uses fifty states, and the research notes list the "
                 "differences. Slide 36 showed the choice of three wrong capitals and the right one.",
    "current": "The table lists seven things from the chapter that current Python changes, and the last column says on which slide the chapter's own example is. Python 3.12 adds Path.walk and a case_sensitive option for glob, and it "
               "deprecates st_ctime on Windows. Python 3.14 makes exists, is_file and is_dir return False instead of raising any OSError. Python 3.13 makes dbm.sqlite3 the first shelve backend, Python 3.10 adds EncodingWarning, "
               "and Python 3.15 makes UTF-8 mode the default. The examples are on slides 13, 14, 15, 25 and 28. Running what the book printed and then checking what changed is the safest habit.",
    "summary": "The five numbered sentences are the chapter in one line each, and they answer the first question of slide 3: Path() and the slash compute, exists, glob and stat ask, and makedirs, writing and shelve change. The chart counts the "
               "code examples in each part: three in part 1, three in part 2, six in part 3, two in part 4 and four in part 5, eighteen in all. The analogy is a packing list: only what you really need goes into the bag. "
               "Chapter 11 builds on all of it.",
    "practice": "The four questions are short drills, like finger scales before a concert. Each can be answered in a few lines that you run on the chapter page: the slash with a string and a path, the file after the modes w, a, a, w and "
                "the mode x, the shelf that loses a list changed in place, and the quiz program with a key that names the right capital. Predict the answer first and then run it. The answers are on slides 6, 24, 28 "
                "and 37.",
    "resources": "The cards collect the further reading for this chapter, and every link is live. They begin with the book chapter and the Python documentation of pathlib, open, io, shelve, dbm, json and tempfile, continue "
                 "with the proposals behind pathlib, UTF-8 mode and the encoding warning, and end with first-hand sources for the stories and a video on file objects. Choose one link and read it before the next class. "
                 "The stories on slides 7, 19, 29 and 31 link to their own sources.",
}
STORY_NOTES = {
    "pathlib": NOTES["pathlib"],
    "utf8": NOTES["utf8"],
    "dbm": NOTES["dbm"],
    "json": "In 2001 Douglas Crockford and Chip Morningstar wrote up JSON, a minimal text format for data in which every key sits in quotes. They worked at State Software, a consulting firm in California, and Crockford opened json.org "
            "on 12 November 2002. A browser and a server needed to exchange data without reloading the page, and plain text was enough. json.dumps() and json.loads() read and write that format for any program or language, "
            "as slide 30 shows. The link on the slide leads to the description of the format.",
}

RESULT_SAYS = {
    "pathobjects": "The path printed with slashes, the Windows version with backslashes, and two strings raised the error.",
    "locations": "Cwd and home are absolute, spam/bacon/eggs is not, and the dot path equals the plain one.",
    "anatomy": "The drive, name, stem and suffix came apart, and with_suffix gave spam.csv.",
    "folders": "The tree has three folders: walnut, pecan and waffles under delicious.",
    "glob": "The question mark skipped project10; the star found every text file, then every file.",
    "fileinfo": "False before the file, True after; 13 bytes, and the fixed time of 9 April 2024.",
    "wholefile": "13 characters were written; café took 5 bytes, and the binary file gave back 0, 1 and 255.",
    "openclose": "14 and 25 characters were written; the text came back, and the file reports closed.",
    "readmethods": "The cursor stood at 6, then 20 and 20; after seek(0), read(5) gave roses.",
    "withstatement": "Open inside the block, closed after it, and closed even after the error.",
    "modes": "w kept D, a added B and C, and x refused because the file exists.",
    "encoding": "The right encoding read café; ascii failed; the byte counts were 5, 8 and 4.",
    "shelve": "The shelf kept the list as bytes; the in-place change stayed at 3, the assigned one gave 4.",
    "json": "The JSON text has the key 5 as text, and the tuple came back as a list.",
    "madlibs": "The three blanks were filled in order: silly, chandelier, screamed.",
    "regexsearch": "Two hits, in a.txt line 1 and b.txt line 2; the csv file and SPAM were skipped.",
    "quizquestion": "A question about California with four lettered options, one of them Sacramento.",
    "quizfiles": "Four quiz lines with shuffled options and a key of four letters: A, A, D, B.",
}
