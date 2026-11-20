"""Chapter 17 deck speaker notes, version 3.0.0: the notes are READER notes (handover of 2026-11-19, practice 3). The slides are handed to students together with their notes, so each note explains the slide's
short wording in fuller sentences, adds detail that the balloons do not carry, and connects the slide to related slides and chapters. A note gives no direction to a presenter, has no think-of statement, no
prompt marker and no lambda. Length 60 to 140 words (at least 30 on title, part and resources slides, ruling 2 of 2026-11-14). The facts are those of the chapter's examples, of the result visuals and of the
notes of deck 2.1.0; nothing is added that the slide or the run does not show.
RESULT_SAYS: for each code slide, the first of the two result balloons (what the run showed, in plain words); the second is the slide's takeaway.
Slide numbers: 1 title, 2 route, 3 questions, 4 part 1, 5 picture, 6 Warnock story, 7 pdf_anatomy, 8 reader_pages, 9 extract_text, 10 picture, 11 post_process, 12 scan_images, 13 ISO story, 14 pypdf story,
15 part 2, 16 picture, 17 append_pages, 18 merge_insert, 19 rotate_pages, 20 picture, 21 watermark, 22 encrypt_decrypt, 23 picture, 24 user_owner, 25 encrypt_schemes, 26 picture, 27 project12_find,
28 project12_combine, 29 part 3, 30 picture, 31 .doc story, 32 docx_zip, 33 docx_read, 34 docx_fulltext, 35 picture, 36 docx_styles, 37 docx_style_errors, 38 picture, 39 run_attributes, 40 Word source story,
41 part 4, 42 picture, 43 docx_write, 44 docx_headings, 45 docx_breaks, 46 picture, 47 docx_picture, 48 docx trap story, 49 part 5, 50 picture, 51 pdf_paranoia_walk, 52 pdf_paranoia, 53 custom_invitations,
54 password_breaker, 55 tools, 56 current, 57 summary, 58 practice, 59 resources."""
__version__ = "3.0.0"

NOTES = {
    "title": "This chapter of the book, PDF and Word Documents, shows how a program reads a PDF with pypdf, builds a new PDF from chosen pages, stamps and locks it, and how it reads and writes Word files with python-docx. "
             "The deck has twenty-eight code examples that run on the chapter page, six true stories about the formats and the libraries, and an everyday picture for every concept. Each code slide shows small steps, a balloon "
             "for each step, and what the run really printed. Slide 2 lays out the five parts; chapter 10 and chapter 11 come before it with files and folders.",
    "route": "The table is the map of the chapter. Each row is one of the five parts, with the slides it covers, the number of code examples in it and what you will run. The last row covers the table of calls, the changes "
             "against the book, the summary, the practice questions and the links. The same twenty-eight examples are listed in the Slide code tab of the chapter page, in this order, so a slide and its tab can be opened side by "
             "side. Parts 1 and 2 are about PDF files, parts 3 and 4 about Word files, and part 5 joins both in three practice programs. Part 1 starts on slide 4.",
    "questions": "Two questions run through the chapter, and the deck answers them at the end. The first asks what a program can do with a PDF or a Word file and what it cannot recover from them; slide 55 lists the calls and "
                 "what each one needs. The second asks where the book's printed output, programs and statements differ from current pypdf and python-docx; slide 56 lists the changes that the chapter research found. Keeping both "
                 "questions in mind makes each later slide easier to place, because every example either shows a call that works or a limit that the call has.",
    "divider1": "Part 1 is about what a PDF holds. A PDF is a page description: drawing commands, numbered objects and a table at the end. The four cards on the slide are the ideas of the part: PdfReader opens a file and lists its pages, "
                "extract_text returns words in drawing order, images lists the pictures of a page, and post-processing mends the text. Slides 5 to 14 cover them, and part 2 later builds new files from the same pages.",
    "divider2": "Part 2 builds new PDF files. A PdfWriter is an empty binder: append and merge copy pages in, rotate turns them, merge_page lays one page on another as a stamp, and encrypt locks the file so that a password is needed. "
                "The four cards are the ideas of the part, and Project 12 at the end combines many files into one. Slides 16 to 28 cover them, and part 1 earlier explains what a page is made of.",
    "divider3": "Part 3 reads Word documents. A .docx file is a ZIP archive of XML parts. A document holds paragraphs, a paragraph holds runs, and a style is a named rule that must fit the object it is given. The four cards are the "
                "ideas of the part: the ZIP and XML, paragraph and run, style, and the three states of a run attribute. Slides 30 to 40 cover them, and part 4 later writes the same kind of file.",
    "divider4": "Part 4 writes Word documents. A new document starts empty; add_paragraph adds a card and returns it, add_heading adds a title or a heading from level 0 to 9, a line break sits inside a run while a page break is a "
                "call of its own, and add_picture pins a picture by width or height. Slides 42 to 48 cover the four cards, and part 3 earlier shows how the same objects look when a file is read.",
    "divider5": "Part 5 gathers three practice programs: PDF Paranoia, which locks every PDF of a folder tree, Custom Invitations, which makes one card per guest in a Word file, and the Password Breaker, which tries a word list against "
                "a locked file. Each runs on small stand-in files, and each shows a limit of its method. Slides 50 to 54 cover them, and the tools of part 2 and part 4 return here in new combinations.",
    "A1": "The headline compares a PDF to a printed photograph of a page: the look is kept on every screen, but the words are no longer sentences that can be moved. The cards give one picture to each idea. pypdf is scissors, glue "
          "and a paper clip. A PdfReader looks at the sheets and writes nothing. A page object is one sheet taken out of the binder, pages are the numbered sheets counted from zero, and is_encrypted is a lock sign to read first. "
          "Slide 8 shows the same ideas in code.",
    "A2": "Extracting text is like tracing a poster letter by letter in the order the printer drew the ink, which is why drawing order and reading order can differ. The cards give one picture to each idea: extract_text is the "
          "reading aloud, images is a shoebox of the pictures on a page, and post-processing is a proofreader who tidies a rough dictation. The two small programs of the book copy text and images out of a whole file. "
          "Slide 9 showed the first of these ideas; slide 11 mends the result.",
    "A3": "Building a new PDF from old pages is like making a new binder from other binders: you choose sheets and clip them in. A PdfWriter is the empty binder, append clips sheets onto the end, and merge slips them in at a "
          "chosen place. Blank pages separate one chapter from the next, and a rotation turns a sheet by a quarter turn so that a wide table can be read. Slide 17 shows copying pages in code, and slide 19 shows rotation.",
    "A4": "A watermark is like a rubber stamp and a password is like a padlock on the binder. Rotation adds to the turn a page already has. A watermark is a faint stamp behind the words, an overlay is a see-through sheet laid on "
          "top, and merge_page lays one sheet on another so that both show. Encrypt snaps the padlock shut and chooses its key, and decrypt tries a key and reports whether it fits. Slide 21 shows the stamp and slide 22 the lock.",
    "A5": "There are two keys: the guest key opens the door, and the owner key also changes the locks. The user password lets you in to read, the owner password lets you in and also sets the house rules, and PasswordType is the "
          "padlock's answer: no fit, the guest key or the owner key. Project 12 is a similar job on many files: find the reports, take each one out in turn and leave its cover sheet behind, then bind the pile. Slide 24 shows both keys.",
    "A6": "A program that handles many files is like a mail sorter: it walks the shelves and treats every item alike. The os module is the directory board of the building, os.listdir is a glance at one shelf, and os.walk is a walk "
          "through the whole building. Sorting puts the folders in alphabetical order before they are bound, and combine_pdfs.py is the finished routine of Project 12. Slide 27 finds the files; the same sorter could stamp pages, "
          "split a book or number the sheets.",
    "A7": "A Word file is like a recipe box: it holds cards, each card holds short stretches of words, and each stretch has its own pen. The Document object is the whole box, a Paragraph is one card and a Run is a stretch of words "
          "written with one pen. You install python-docx but you write import docx, as the label on the box says. Reading is flipping through the cards, and readDocx.py copies the words of every card for you. Slide 32 opens the box.",
    "A8": "A style is like a house rule for a card: headings are big and bold, quotes lean. The paragraphs are the cards of the box in order, and the runs are the places inside a card where the pen changes. A paragraph style is a "
          "rule for the whole card, a character style is a rule for a few words, and the name of the style must match exactly, like a key cut for one lock. Slide 36 shows both kinds and slide 37 shows what goes wrong.",
    "A9": "A run attribute is like a light switch with three positions: on, off, or follow the house rule. Bold is a thick pen, italic is a pen that leans, and underline is a ruler line drawn under the words. In code the three "
          "positions are True, False and None, and None means that the style decides. Slide 39 shows all three states, and the same idea returns in part 4 when a new run is written.",
    "A10": "Writing a Word file is like filling a new recipe box: add a card, add words to it, then save the box. add_paragraph puts a new card into the box, add_run writes a few more words on the same card with another pen, and "
           "add_heading is the heading pen: level 0 is the title and levels 1 to 9 are headings. A line break starts a new line and a page break is the tear line between two sheets. Slide 43 writes a small file.",
    "A11": "A picture in a Word file is like a photo pinned to a card: you choose the width and the height follows. add_picture is the pin and the photo it holds. Inches and Cm are the rulers, and docx.shared is the drawer where "
           "the package keeps its rulers and pen sizes. docx.enum.text is the drawer of named choices, such as the kind of break. Slide 47 shows the sizes in code, and slide 45 earlier used the same drawer of named choices.",
    "A12": "The practice programs are small recital pieces after the finger exercises. PDF Paranoia locks every report in a vault, checks that the lock works and only then shreds the paper copy. Custom Invitations is a card printer: "
           "one personal card for each guest. The Password Breaker is a locksmith with a list of likely keys. A brute-force attack tries every key on the ring, and a long random key makes the ring far too big. "
           "pdfminer.high_level is a second library that also reads PDF text.",
    "pdf_anatomy": "The sample PDF travels inside the code as compressed text, so the book's own files are not needed. Unpacked, it is a file that begins with a version line, holds numbered objects and ends with a table whose position "
                   "the last lines name. The run found the version line and the end marker, counted the objects and named the byte where the table begins. A reader follows that table to find the pages. "
                   "Slide 8 opens the same kind of file with PdfReader, and slide 13 tells how the format became a standard.",
    "reader_pages": "A PdfWriter starts empty, and here three blank pages of different widths stand in for a real document. Writing them into memory and reading them back gives a PdfReader. Its pages are a list counted from zero, and the "
                    "media box gives each page's size in points, which is how the three pages are told apart. is_encrypted says whether a password is needed before the pages can be read. "
                    "Slide 7 showed what such a file holds inside; slide 9 reads the words of its pages.",
    "extract_text": "A PDF stores drawing commands, not sentences. Page one draws the word world before Hello, so the stream order gives worldHello, while layout mode sorts the words by their position and gives Hello world. Page two "
                    "draws a black box over a line of text, yet extract_text still returns the line: the text is in the file, only covered. A black rectangle is therefore not a safe way to hide text. "
                    "Slide 11 mends rough text; slide 12 meets a page with no text at all.",
    "post_process": "Extracted text often needs mending before anyone reads it: a ligature such as the single letter fi, a hyphen at the end of a line, and line breaks inside sentences. Three small regular expressions do that work here. "
                    "The chapter hands the same job to a language model; this example only builds the request and counts its words, so nothing is sent anywhere. Compare slide 9, where the rough text came from, "
                    "and chapter 10, which covers writing the result to a file.",
    "scan_images": "A scanned page is a picture with no text, so extract_text gives an empty string and the images list holds the picture. The loop writes each image's bytes to a file, as the chapter's image script does for every "
                   "page of a file. The images list needs the Pillow package; without it, the call fails with an ImportError. A scan therefore needs a different tool, optical character recognition, before its words can be used. "
                   "Slide 9 showed text that is really in the file.",
    "append_pages": "Page widths tell which page was copied, because each page is a different width. A tuple is a range with a start, a stop and a step, while a list names pages exactly. So (0, 5) copies the first five pages and "
                    "[0, 5] copies page one and page six. A third value in the tuple is the step: (0, 5, 2) takes pages one, three and five. Slide 18 shows merge, which puts pages inside a file, and slide 28 "
                    "uses append on whole files.",
    "merge_insert": "merge puts another file's pages inside this one at an index, here at position 1. Write pages= by name: the third position of merge is a bookmark title, so a tuple given there is wrong. The book's call inserts "
                    "five pages; with a tuple in that place, current pypdf takes it as a title and all pages go in. insert_blank_page adds a clean sheet and copies the size of the page before it. "
                    "Compare slide 17, where append put pages at the end.",
    "rotate_pages": "rotate adds the angle to the total already there, and the total is not wrapped at 360, so turns of 90, 270, minus 90 and 180 end at 450. Only multiples of 90 are accepted; anything else raises a ValueError, which "
                    "the example catches and replaces by a plain sentence. A wide table can be read after a quarter turn. The rotation is stored with the page and does not change the drawing commands. "
                    "Slide 16 gave the everyday picture, and slide 21 puts one page on another.",
    "watermark": "merge_page lays the stamp page on the base page, and the page then draws both pictures, the later one on top. The run shows the image count of the base page rising from one to two, and the order in which the "
                 "pictures are drawn, from first to last. A watermark is a stamp behind the words and an overlay is a see-through sheet on top; the call is the same. Without Pillow the images list would not work. "
                 "Slide 22 locks the result.",
    "encrypt_decrypt": "encrypt locks the file. A reader still opens it but refuses its pages, with a FileNotDecryptedError, until decrypt matches the password. decrypt answers with a PasswordType: a wrong word gives NOT_DECRYPTED, and "
                       "the right one gives a code for the key that fitted. When only one password is given it serves as both the user and the owner password, so the answer here is OWNER_PASSWORD. "
                       "Slide 24 separates the two keys.",
    "user_owner": "Two passwords give two answers. The user password opens the file to read; the owner password also controls what the file allows. decrypt reports which one fitted: USER_PASSWORD, OWNER_PASSWORD, or NOT_DECRYPTED "
                  "when neither did. The run tries three words in turn, and each answer names the key that fitted. The distinction matters when a file may be read but not changed. Compare slide 22, where one password served as both, "
                  "and slide 25, which shows how the file records its lock.",
    "encrypt_schemes": "A locked file records how it was locked. The default algorithm in pypdf is the old RC4, recorded as version 2, revision 3 and a 128-bit key. AES-128 records version 4, revision 4, and AES-256 records version 5, "
                       "revision 6 with a 256-bit key. The book shows AES-256 only; asking for it needs the cryptography package. The trailer entry that the run reads is part of the structure that slide 7 opened. "
                       "Slide 28 uses the lock in Project 12.",
    "project12_find": "Project 12, step one: find the PDF files of a folder and sort them. lower() lets the test see c.PDF too, and sorting with str.lower ignores case, so A.pdf comes first. The files here are empty, because only their "
                      "names matter at this step. The result is a list called pdf_filenames, the name that the next slide uses. os.listdir, shown on slide 26, looks at one shelf only; "
                      "walking a whole tree needs os.walk, which slide 51 uses.",
    "project12_combine": "Project 12, steps two and three: open each PDF, copy every page but the first, and save the result. The three small files here have three, two and four pages, so the combined file has six. The chapter's loop uses "
                         "a list name that does not exist; the list is pdf_filenames, as slide 27 builds it. A second run would also read combined.pdf, because it is in the same folder, so a real program saves the result elsewhere. "
                         "Compare slide 17, which copies pages by range.",
    "docx_zip": "A .docx file begins with the two bytes PK because it is a ZIP archive. This one holds seventeen parts, and the text lives in word/document.xml, inside paragraph, run and text tags. python-docx hides this structure, "
                "but knowing it explains why a .doc file, which starts with other bytes, is refused. Chapter 11 shows how to open a ZIP archive with the zipfile module. Slide 31 tells how the older .doc format was "
                "published, and slide 33 reads paragraphs and runs.",
    "docx_read": "A document holds paragraphs and a paragraph holds runs. The example makes a paragraph with three runs, of which only the middle one is bold: the others read back None, which means that the style decides. "
                 "A table's text is not in the paragraphs list; it is in the tables list, and the same holds for headers. Reading both lists is therefore needed for the full text of a file. "
                 "Slide 34 joins the paragraphs into one text.",
    "docx_fulltext": "The readDocx idea is short: open the file and join each paragraph's text with a line break. Document accepts a file name or a file object, so the example builds three paragraphs in memory and reads them back. "
                     "The run printed the three lines and counted three lines and six words. The same function works on a real file by giving its name. Slide 33 explains why tables stay out of this text; "
                     "chapter 10 covers writing such text to a plain file.",
    "docx_styles": "A paragraph takes a paragraph style and a run takes a character style. Quote is the first kind and Quote Char is the second, and the example gives one of each to the same words. A new document holds 164 styles, "
                   "while the chapter prints a list of 34. Styles are the way to change the look of a whole document in one place. Slide 37 shows what happens when the kind or the name is wrong, "
                   "and slide 35 gave the everyday picture.",
    "docx_style_errors": "The kind of style must fit the object: a character style given to a paragraph raises a ValueError. The name must also match exactly: a trailing space raises a KeyError, as the book's printed list of names would. "
                         "The run shows both errors caught and replaced by plain sentences, and then the correct name working. Compare slide 36, where the right kinds were used. "
                         "Print the names of the styles in your own document before you rely on one.",
    "run_attributes": "Bold, italic and underline are real attributes of a run, with three states: True, False and None. The run reads each value back. Strike is not an attribute of a run: setting run.strike does nothing visible and "
                      "reads back None, while run.font.strike really sets it. The book's table lists more attributes than the library accepts. Compare slide 33, where None meant that the style decides. "
                      "Slide 40 turns from attributes to the history of Word itself.",
    "docx_write": "add_paragraph returns the new Paragraph and add_run returns the new Run, so the names p and r hold what you want to change next. After saving to memory and opening the file again, the one paragraph holds two runs "
                  "with their text intact. Saving writes the whole document at once, so a program builds the content first and saves last. Slide 44 adds headings to the same kind of document, "
                  "and slide 33 reads one back.",
    "docx_headings": "add_heading takes levels 0 to 9: level 0 is the Title style and levels 1 to 9 are Heading 1 to Heading 9. Level 10 raises a ValueError, which the example catches. The book's text says 0 to 4 in one place and 1 to 9 in "
                     "another; the library accepts 0 to 9. The levels are the outline of a document, so a program can build a table of contents from them. Slide 45 adds breaks.",
    "docx_breaks": "A line break is an item inside a run, added by add_break with a named choice; a page break is added by add_page_break on the document. Counting the tags in the XML shows what was written: one page break and two breaks "
                   "in all. The named choice WD_BREAK comes from docx.enum.text, the drawer of named choices that slide 46 describes. Compare slide 44, where headings gave the document its outline, "
                   "and slide 53, where page breaks separate invitations.",
    "docx_picture": "A picture's size is stored in EMU, English Metric Units, 914400 to the inch. Given no size, the picture keeps its own shape. Given a width or a height, the other follows from the picture's shape, so one inch wide "
                    "gives 1219200 units high for this 60 by 80 picture. Inches and Cm come from docx.shared. Pillow makes the stand-in picture here, in memory. Slide 46 gave the everyday picture; slide 48 ends the part "
                    "with a warning about the package name.",
    "pdf_paranoia_walk": "PDF Paranoia, part one: os.walk visits every folder of a tree, and each name that ends in .pdf, in any case, becomes a full path. The tree holds empty files, because only the names matter. The two PDFs, one of them "
                         "B.PDF in a subfolder, were found, and the text file was skipped. Compare slide 27, where os.listdir looked at one folder only. Slide 52 locks the files that this walk finds.",
    "pdf_paranoia": "PDF Paranoia, part two: copy the PDF, lock the copy with AES-256, test it with the password, and only then remove the original. The test is the point: a program that deletes before it checks can destroy the only copy. "
                    "Real use never passes the password on the command line, where other programs can read it. The needs of AES are those of slide 25. Slide 51 found the files that this step would lock.",
    "custom_invitations": "Custom Invitations: one card per guest, the name in a big built-in style, and a page break after every card but the last. Three guests need two page breaks, and the run lists the three names it found in the "
                          "Title style. The book's version reads the guests from a text file; here a list stands in. Compare slide 45, where a single page break was added, and slide 43, which wrote a paragraph.",
    "password_breaker": "The Password Breaker tries every word in two cases until decrypt stops answering NOT_DECRYPTED. Four words give at most eight attempts, and the run found CHERRY at the sixth. The book's dictionary has far more words, "
                        "so the attempts grow with the size of the list, while a long random password is in no dictionary. With the shipped dictionary of 699,800 attempts, the research measured about 241 seconds for RC4 and 1467 seconds for AES-256. "
                        "Slide 24 explains the answers that decrypt gives.",
    "tools": "The calls of the chapter in one table, each with the slide of its code. Reads change nothing; writes make a new file; locks need the cryptography package for AES. A PdfReader only looks; a PdfWriter builds; "
             "a Document opens or starts a Word file, and its paragraphs, runs and tables are kept apart. The last column leads to the example, so a call can be found again after the lecture. "
             "Compare slide 56, which lists where the book differs from today's libraries.",
    "current": "What differs from the book today, from the chapter research of 12 October 2026. Run the book's lines first; then compare with these rows. The merge call takes a title where the book gives a range, the Project 12 loop "
               "names a list that does not exist, and the table of run attributes lists more than the library accepts. Older tutorials use PdfFileReader and PdfMerger, which are gone. "
               "Each row names the slide that shows it, so slide 55 and this slide can be read together.",
    "summary": "Five sentences close the chapter. A PDF is a page description: drawing commands, objects and a table. pypdf copies, turns, stamps and locks pages, but it cannot recover structure that was lost. A .docx file is a "
               "ZIP of XML, where documents hold paragraphs and paragraphs hold runs. A style must fit its object and match by exact name. A password is only as strong as it is long and random. "
               "The chart counts the examples of each part; compare slide 2.",
    "practice": "Five questions to predict first and then check by running the code on the chapter page. Each one points back to a slide: the order of extracted text, a tuple against a list, the three states of a bold run, "
                "why a black rectangle hides nothing, and how many attempts a word list needs. Writing the prediction before the run is what makes the result useful. Slides 9, 17 and 39 hold the answers "
                "to the first three, and slide 54 the last.",
    "resources": "Links to read and watch next: the chapter of the book, the documentation of pypdf and python-docx, the PDF and Office standards at the Library of Congress, the zipfile documentation and the page behind the first "
                 "story. Each link is live and was opened while this deck was made. The documentation pages of the two packages go deeper than the chapter does, so read them also when a call behaves differently from the book. "
                 "Slide 55 lists the calls that these pages describe.",
}

STORY_NOTES = {
    "warnock": "John Warnock outlined the system called Camelot in the spring of 1991, in a design document at Adobe. The photograph shows him in 2008. A PDF is a page description made to look the same everywhere, and "
               "the first Acrobat was released on 15 June 1993. Chapter 17 reads and rewrites exactly such files. Slide 7 opens a small one and shows its numbered objects and its table; slide 13 tells how the format "
               "later became an international standard. The link on the slide leads to a biography of Warnock.",
    "iso": "PDF 1.7 was released in November 2006 and became the standard ISO 32000-1 in July 2008, after Adobe announced in January 2007 that it sought standardization. The photograph shows the Adobe headquarters towers in "
           "San Jose. The standard describes the pieces that slide 7 opened: header, objects, table and trailer, so that other programs such as pypdf can read and write PDF from the same rules. "
           "The link leads to the description of the format at the Library of Congress.",
    "pypdf": "The library of this chapter began as pyPdf in 2005 by Mathieu Fenniak, became PyPDF2 at the end of 2011, and took the name pypdf in 2023. The picture is the Python logo of that time, not a picture of the authors. "
             "Old tutorials say PyPDF2 or use PdfFileReader, which no longer exists; slide 56 lists such changes. A library that nobody maintains stops working with new Python, and a fork and new "
             "maintainers kept this one alive. The link leads to the history in the pypdf documentation.",
    "doc2008": "On 15 February 2008 Microsoft published the binary format of the older Word .doc file, in a post on Brian Jones's Office blog. The photograph shows Office 2007 boxes, the release whose default format was already "
               ".docx; it is not a picture of the announcement. A .doc file starts with the bytes D0 CF 11 E0, not with PK, so python-docx refuses it, as slide 32 explains for the newer format. "
               "The link leads to the Microsoft post.",
    "wordsrc": "In 1983 Word began as Multi-Tool Word, built on Bravo, the word processor that Charles Simonyi made at Xerox PARC. On 25 March 2014 the Computer History Museum published the source code of Word for Windows 1.1a. "
               "The photograph shows Simonyi in 2006. A .docx file is what such a program saves, and python-docx lets a script save the same kind of file without Word, as slide 43 shows. "
               "The link leads to the museum's page about the source code.",
    "docxtrap": "Two packages share the import name docx, but only python-docx is maintained. The package called docx on PyPI has its last release, 0.2.4, dated 6 February 2014, and it fails under current Python. Install python-docx "
                "and write import docx. The picture is a screenshot of the Python Package Index home page from December 2007. Compare slide 14, where a library changed its name, and slide 30, where the label on the box says "
                "the same. The link leads to the old package.",
}

RESULT_SAYS = {
    "pdf_anatomy": "A version line, an EOF marker, seven objects, and a table at byte 639.",
    "reader_pages": "Three pages, not locked; the widths 100, 200 and 300 tell them apart.",
    "extract_text": "Stream order gave worldHello; layout gave Hello world; the covered text remained.",
    "post_process": "Ligature, hyphen and line breaks mended; a prompt of 17 words built.",
    "scan_images": "No text, one image found, and its bytes written to a file.",
    "append_pages": "(0, 5) gave pages 1 to 5, (0, 5, 2) gave 1, 3, 5; [0, 5] gave 1 and 6.",
    "merge_insert": "Pages 700 and 800 stand after page one; the blank copied width 800.",
    "rotate_pages": "The turns added up to 90, 360, 270 and 450; 45 was refused.",
    "watermark": "The base page went from one image to two; the stamp came last.",
    "encrypt_decrypt": "Locked, pages refused; a wrong word failed and the right one opened it.",
    "user_owner": "open-me gave USER, boss gave OWNER, guess gave NOT_DECRYPTED.",
    "encrypt_schemes": "RC4 gave V 2, R 3; AES-128 gave 4 and 4; AES-256 gave 5 and 6.",
    "project12_find": "A.pdf, b.pdf and c.PDF in order; notes.txt left out.",
    "project12_combine": "Files of 3, 2 and 4 pages gave 6 pages: first pages left out.",
    "docx_zip": "PK at the start, 17 parts, and the text in word/document.xml.",
    "docx_read": "One paragraph of three runs, only the middle one bold.",
    "docx_fulltext": "Three lines joined with line breaks: 3 lines and 6 words.",
    "docx_styles": "Paragraph took Quote, run took Quote Char; 164 styles in all.",
    "docx_style_errors": "A wrong kind and a trailing space raised errors; the exact name worked.",
    "run_attributes": "True, False and None read back; run.strike stayed None.",
    "docx_write": "A Paragraph and a Run came back; two runs survived the save.",
    "docx_headings": "Level 0 gave Title, 9 gave Heading 9, and level 10 was refused.",
    "docx_breaks": "One page break and two breaks in all were counted.",
    "docx_picture": "762000 by 1016000 as is; 1 inch wide gave 1219200 high.",
    "pdf_paranoia_walk": "Found tree/a.pdf and tree/sub/B.PDF; skipped the text file.",
    "pdf_paranoia": "The locked copy opened, so the original could go.",
    "custom_invitations": "Three guests, two page breaks, three names in Title style.",
    "password_breaker": "CHERRY found at the sixth of at most eight attempts.",
}
