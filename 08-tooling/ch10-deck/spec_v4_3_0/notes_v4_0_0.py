"""Chapter 10 deck notes 4.0.0 (new file over notes 3.0.0, which stays as committed; Lineage11, 2026-11-24). Deck 4.0.0 gives each code ONE box, from the single source, with the sample files made by hidden set-up lines;
the notes of the 18 code slides, the result balloons, some takeaways and the title note are written again for that code and for what the run prints. They are reader notes: full sentences that explain the slide's
short wording, no direction to a presenter, no think-of statement, 60 to 140 words. Every number is what the run prints or what the set-up creates."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'spec_v3_0_0'))
import notes_v3_0_0 as N0

__version__ = "4.0.0"

NOTES = dict(N0.NOTES)
STORY_NOTES = dict(N0.STORY_NOTES)
STORY_NOTES["utf8"] = N0.STORY_NOTES["utf8"].replace("Slide 18 showed the two bytes of the accent, and slide 25 shows the encodings side by side.", "Slide 25 shows the two bytes of the accent next to the count of characters.")
NOTES["title"] = ("This chapter of the book, Reading and Writing Files, shows how a program names a file with a path, makes folders, reads and writes text, and keeps Python values between two runs. "
                  "The deck has eighteen code examples that run on the chapter page, true stories about the people behind these tools, and an everyday picture for every concept. "
                  "Each code slide shows one whole program in one box that can be copied in a single step, a balloon that explains it, and what the run really printed, drawn as a table, a chart or a small picture. "
                  "The sample files a program needs are made by lines that the slide does not show. Slide 2 lays out the five parts, and chapter 11 continues with whole folders and archives.")

NOTES.update({
 "pathobjects": ("Path() joins the names it is given with the separator of the computer and returns one path object, so the result prints with slashes on Linux and macOS and with backslashes on Windows. "
                 "The program shows three ways to write the same path: all the names inside Path(), the slash operator between names, and the slash between a Path and another Path; the three lines print the same text. "
                 "The slash works only when a Path stands on its left side, because two plain strings cannot be divided. The last loop joins a folder name with each file name in a list. "
                 "Slide 7 tells the story of the proposal that made paths objects, and slide 10 takes a path apart."),
 "locations": ("Every running program has a current working directory, the folder that its relative paths start from. Path.cwd() returns it and Path.home() returns the home folder of the user; both are absolute paths, "
               "so the first two answers are True. A path written like spam/bacon/eggs has no start of its own, so it is relative and the third answer is False. "
               "The last line shows that a leading dot, which means the current folder, changes nothing: ./spam.txt and spam.txt are the same path. "
               "The names of the real folders differ from computer to computer, which is why the program prints yes-or-no answers and not the folders. Slide 10 takes a path apart."),
 "anatomy": ("A path is made of parts, and each part is an attribute of the path object. The drive is C:, the anchor is the drive with its separator, the parent is everything before the last name, "
             "the name is the last part with its ending, the stem is the name without the ending and the suffix is the ending alone. Parts gives all the names as a tuple, and parents[1] is the folder two levels up. "
             "The program uses PureWindowsPath so that a Windows path can be taken apart on any computer; on Windows the same lines work with Path. "
             "The table on the slide lists the parts as the run found them. Part 2 of the deck, on folders and files, begins with slide 11."),
 "folders": ("Os.makedirs builds a whole chain of folders at once, here delicious, walnut and waffles, and creates the folders in the middle if they are missing. "
             "The Path method mkdir makes only the last folder of a path, here pecan inside walnut, and raises an error if the folder above it does not exist. "
             "The loop at the end walks through everything below delicious with rglob, in sorted order, and prints each path: walnut, then pecan, then waffles. "
             "The table on the slide draws the same tree. Both ways raise an error when the last folder already exists, unless exist_ok=True is given, which chapter 11 uses. Slide 14 finds files by a pattern."),
 "glob": ("Glob finds files by a pattern. In a pattern, an asterisk stands for any number of characters and a question mark for exactly one. "
          "The folder holds project1.txt, project2.txt, project10.txt and notes.csv. The pattern *.txt finds the three text files, and sorted puts them in text order, which is why project10 comes before project2. "
          "The pattern project?.txt finds only project1 and project2, because project10 has two characters after the word project and the question mark allows just one. "
          "The table on the slide shows for each file which pattern takes it. Glob returns paths, so it can feed any loop. Slide 15 asks a path about its size and its time."),
 "fileinfo": ("A path can be asked about the file it points to. Exists says whether anything is there, is_file whether it is a file, and is_dir whether it is a folder; the file spam.txt gives True, True and False. "
              "Stat holds the details: st_size is the size in bytes, 13 for the text Hello, world!, and st_mtime is the time of the last change in seconds since 1970. "
              "The set-up gives the file a fixed time, so asctime with gmtime prints Tue Apr  9 01:45:29 2024 in universal time on every computer; the book prints the local time. "
              "A path that does not exist gives False and no error. Part 3 of the deck, on reading and writing, begins on slide 16."),
 "wholefile": ("The shortest way to use a file is to write or read all of it in one call. Write_text saves a string in a file and returns the number of characters it wrote, here 13 for Hello, world!. "
               "Read_text returns the whole text of the file as a string. The Path object opens and closes the file by itself, so there is nothing to forget. "
               "The table on the slide shows what each call gave back. The method is a good fit for small text files; for a file that is too large to hold at once, or for reading line by line, the open function on the next slides is needed. "
               "Slide 19 tells the story of the character set behind these calls."),
 "openclose": ("Open returns a file object, and a file object must be closed when the work is done. The first call uses mode w, which starts the file empty, and write returns the number of characters it wrote, 14. "
               "The second call uses mode a, which adds to the end, and writes 25 more. The third call opens the file for reading, read returns the whole content and the program prints it, both lines. "
               "The chart shows the two counts, and the file holds 39 bytes in all. Every open names the encoding UTF-8, so the text is read back as it was written. "
               "Forgetting to close can lose data; the with statement on slide 23 does the closing automatically."),
 "readmethods": ("A file object remembers where it has read to, like a cursor in a text. Readlines reads every line from the cursor to the end and returns them as a list, here four lines of the sonnet, each ending with a newline character. "
                 "The program prints how many lines there are and the first line. After that the cursor stands at the end of the file, so the second read returns an empty string, shown as two quotation marks. "
                 "A second read of the same file object therefore finds nothing unless the file is opened again. The table on the slide shows the three results. Slide 23 introduces the with statement."),
 "withstatement": ("The with statement opens a file and closes it when its block ends, even if an error happens inside the block. The program writes a text in the first block and reads it back in the second. "
                   "Inside the second block the variable content takes the text, and after the block the program prints it. The last line prints the closed attribute of the file object, which is True: the file is closed although the program never called close. "
                   "The table shows both values. This is the form that current Python programs use, because the close call cannot be forgotten. Slide 24 compares the write modes."),
 "modes": ("A file can be opened for writing in different modes, and the mode decides what happens to the content that is already there. Mode w starts the file again, so the old content is thrown away. "
           "Mode a keeps the old content and adds the new text at the end. The loop runs four steps: w writes A, a adds B, a adds C, and w writes D. After each step the program reads the file back. "
           "After the last step only D is left, because the second w erased A, B and C. The table lists the file after each step. A third mode, x, creates a new file and refuses if the file exists; it is not part of this program. Slide 25 shows how the bytes of a file become characters."),
 "encoding": ("A file stores bytes, and the encoding says how bytes become characters. The word café has four characters, but in UTF-8 the letter e with an accent takes two bytes, so the file holds five bytes: "
              "the bytes of caf and the two bytes with the values c3 and a9. The chart compares the counts. Reading the file with the same encoding that wrote it gives the word back; reading with another one gives wrong characters or an error. "
              "That is why every open call in this deck names UTF-8. Slide 19 told the story of how the character set was agreed."),
 "shelve": ("The shelve module keeps Python values in a file, so that the next run of a program finds them again. Shelve.open opens a file, here mydata, and the shelf works like a dictionary: the program stores a list under the key cats. "
            "After closing, it opens the shelf again and prints its type, which is DbfilenameShelf, its keys, which are the single word cats, and the list itself. The values survived the closing of the program's file. "
            "The table on the slide lists what was read back. A shelf can hold lists and dictionaries, but not every kind of object. Slide 29 explains what is behind the file, and slide 30 shows a plain-text way of saving values."),
 "json": ("Json writes the same kind of data as plain text that programs in other languages can read, which a shelf file cannot offer. The program makes a dictionary with a list inside it. "
          "Dumps turns it into text with double quotation marks, and the program prints that text. Loads turns the text back into a dictionary, and the comparison with the original is True. "
          "The table shows both steps. A json text can be stored in a file with write_text and sent over a network. Not every Python value fits: a tuple comes back as a list, and keys must be text, which is the price of a format that every language understands. Part 5, the practice programs, begins with slide 31."),
 "madlibs": ("The Mad Libs program reads a story from a file, replaces its capital-letter words with answers, and saves the new story. The story has the words ADJECTIVE, NOUN, VERB and NOUN. "
             "The loop takes the words in order, and replace with a count of one swaps only the first match each time, so the second NOUN receives the fourth answer. The answers come from a list, because the book's version asks the user to type them. "
             "The program prints the finished story and writes it to panda_filled.txt. The text box on the slide shows the saved story. The program reads one file and writes another, which is the pattern of most file programs. Slide 35 searches several files at once."),
 "regexsearch": ("This practice program searches every text file of a folder for lines that match a pattern. Glob lists the files ending in .txt in sorted order, and the file notes.csv is left out because its name does not match. "
                 "For each file the program reads the text, splits it into lines with splitlines, and numbers them with enumerate, starting at one. A compiled pattern tests each line, and a hit prints the file name, the line number and the line. "
                 "The pattern spam finds a.txt line 1 and b.txt line 2; the line with SPAM in capitals is not matched, because patterns are case-sensitive unless told otherwise. The table lists the two hits. Regular expressions are the subject of chapter 9."),
 "quizquestion": ("Project 4 of the book generates quizzes with the capitals of states. Step one makes a single question. The dictionary holds four states and their capitals, and the fixed seed in random.seed makes the shuffle repeat, "
                  "so the same question appears on every run: the capital of Maine. The program shuffles the states, takes the first, remembers the right capital, shuffles the four capitals into options, and prints them with the letters A to D. "
                  "The table marks the right option. The book uses fifty states and removes the right capital from the wrong ones first; with four states all four capitals serve as options. Step two, on slide 37, writes the quiz and its key to files."),
 "quizfiles": ("Step two of Project 4 writes the quiz and its answer key into two files, as the book does. The loop makes one question for each state: the question line and its four options go to the quiz file, "
               "and the number with the right letter goes to the key file. The right letter is found with options.index, which gives the position of the right capital in the shuffled list. "
               "Both files are closed at the end, and the program prints them. The table shows the key, one letter for each question. The book writes thirty-five quizzes of fifty questions; the structure is the same. "
               "Slide 38 looks at what current Python adds to file work."),
})

NOTES["practice"] = ("The four questions are short drills, like finger scales before a concert. Each can be answered in a few lines that you run on the chapter page. "
                     "The first asks why the slash works when a path stands on its left and fails for two strings; slide 6 answers it. The second asks what the file holds after the modes w, a, a, w and what mode x does; slide 24 answers it. "
                     "The third asks why a list changed inside a shelf is lost and how to keep the change: edit the shelve program of slide 28, change the list in place, close the shelf and read it again. "
                     "The fourth asks for the key file to name the right capital as well: edit the program of slide 37. Predict the answer first and then run it.")

RESULT_SAYS = dict(N0.RESULT_SAYS)
RESULT_SAYS.update({
 "pathobjects": "Three ways wrote one path, and the loop joined a folder with each file name.",
 "locations": "Cwd and home are absolute, spam/bacon/eggs is not, and the dot path equals the plain one.",
 "anatomy": "The drive, name, stem and suffix came apart, with the parent and the folder two up.",
 "folders": "The tree has three folders under delicious: walnut, pecan and waffles.",
 "glob": "The star found three text files; the question mark skipped project10.",
 "fileinfo": "True, True, False for the file; 13 bytes, the fixed time, and False for a missing path.",
 "wholefile": "13 characters were written, and read_text gave the same text back.",
 "openclose": "14 and 25 characters were written, and the whole text came back.",
 "readmethods": "Four lines were read, and a second read found only an empty string.",
 "withstatement": "The text was read inside the block, and the file was closed after it.",
 "modes": "w kept only D at the end, and a added B and C in between.",
 "encoding": "The word has 4 characters and 5 bytes; the bytes show the two-byte letter.",
 "shelve": "The shelf gave back its type, its one key and the list of cats.",
 "json": "The dictionary became plain text and came back equal.",
 "madlibs": "The four blanks were filled in order and the story was saved.",
 "regexsearch": "Two hits, in a.txt line 1 and b.txt line 2; the csv file and SPAM were skipped.",
 "quizquestion": "A question about Maine with four lettered options, one of them Augusta.",
 "quizfiles": "Four questions with shuffled options, and a key with one letter for each.",
})

TAKEAWAY = {
 "pathobjects": "Path() and the slash join names into one path object.",
 "openclose": "Open, use, close: always return the file.",
 "readmethods": "Reading moves the cursor to the end of what was read.",
 "modes": "w starts again, a adds at the end.",
 "encoding": "Say the encoding; UTF-8 is the safe choice.",
 "shelve": "shelve.open keeps a dictionary-like store in a file.",
 "json": "json is plain text that other programs read.",
 "madlibs": "Read a file, substitute, write a file.",
 "quizquestion": "Shuffle the options; remember the right one.",
}
