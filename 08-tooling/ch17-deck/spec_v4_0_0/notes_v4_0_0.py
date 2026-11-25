"""Chapter 17 deck notes 4.0.0 (Lineage10, change request 'no everyday analogies'): the notes that compared a concept with an everyday thing
state the concept plainly. The twelve notes of the former analogy slides are written again; every other note is notes_v3_0_0.py with the changed
phrases replaced."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notes_v3_0_0 as N0

__version__ = "4.0.0"

NOTES = dict(N0.NOTES)
STORY_NOTES = dict(N0.STORY_NOTES)
RESULT_SAYS = dict(N0.RESULT_SAYS)
TAKEAWAY = getattr(N0, "TAKEAWAY", {})


def _rep(key, old, new, d=None):
    d = NOTES if d is None else d
    assert d[key].count(old) == 1, (key, old)
    d[key] = d[key].replace(old, new)


_rep("title", "stamps and locks it", "adds watermarks to it and locks it")
_rep("title", "and an everyday picture for every concept", "and a plain explanation of every concept")
_rep("divider2", "A PdfWriter is an empty binder: append and merge copy pages in, rotate turns them, merge_page lays one page on another as a stamp, and encrypt",
     "A PdfWriter is an empty new file: append and merge copy pages in, rotate turns them, merge_page draws one page on another as a watermark, and encrypt")
_rep("rotate_pages", "Slide 16 gave the everyday picture, and slide 21 puts one page on another.", "Slide 20 explained rotation plainly, and slide 21 puts one page on another.")
_rep("watermark", "merge_page lays the stamp page on the base page", "merge_page draws the watermark page on the base page")
_rep("watermark", "A watermark is a stamp behind the words and an overlay is a see-through sheet on top; the call is the same.",
     "A watermark is a faint page behind the words and an overlay is a page on top; the call is the same.")
_rep("docx_styles", "and slide 35 gave the everyday picture.", "and slide 35 explained the objects plainly.")
_rep("docx_picture", "Slide 46 gave the everyday picture; slide 48", "Slide 46 explained the calls plainly; slide 48")
_rep("docxtrap", "and slide 30, where the label on the box says the same.", "and slide 30, where the import name is also not the package name.", STORY_NOTES)
_rep("summary", "pypdf copies, turns, stamps and locks pages", "pypdf copies, turns, watermarks and locks pages")
_rep("watermark", "the stamp came last.", "the watermark came last.", RESULT_SAYS)

NOTES["A1"] = ("A PDF stores how each page is drawn, as drawing commands, so the look is the same on every screen but the words are not kept as sentences that can be moved. "
               "pypdf is the library that reads, copies, rotates, watermarks and locks PDF pages. A PdfReader opens a file for reading and changes nothing. A page object is one page of that file, "
               "pages is the list of page objects counted from zero, and is_encrypted tells you whether the file is locked, so read it before the pages. The io module gives file objects that stay in memory. "
               "Slide 8 shows the same ideas in code.")
NOTES["A2"] = ("extract_text returns the words of a page in the order the file draws them, which is why drawing order and reading order can differ. "
               "The images list holds the pictures of a page and needs the Pillow package. Post-processing, for example by a language model, mends the extracted text: line breaks, hyphens and odd letters. "
               "The two small programs of the book copy the text or the pictures out of a whole file. The open function returns a file object that you close when you are done. "
               "Slide 9 showed the first of these ideas; slide 11 mends the result.")
NOTES["A3"] = ("A new PDF is made by adding chosen pages from other files to an empty PdfWriter and then saving it; only the pages you add are in the new file. append copies pages to the end, "
               "and merge copies them in at a chosen position, with the pages argument named. add_blank_page adds a blank page at the end and insert_blank_page adds one at a given number; "
               "a blank page can separate one part of a document from the next. A rotation turns a page by a multiple of 90 degrees, for example to read a wide table. "
               "Slide 17 shows copying pages in code, and slide 19 shows rotation.")
NOTES["A4"] = ("rotate turns a page by quarter turns, and the new angle adds to the angle the page already has. A watermark is a faint page drawn behind the words and an overlay is a page drawn on top; "
               "merge_page draws one page onto another so that both show, and the later page lies on top. encrypt locks a file with a password, and the default method is RC4. "
               "decrypt tries a password and returns whether it fitted. Slide 21 shows the watermark and slide 22 the lock.")
NOTES["A5"] = ("The user password lets you open a PDF and read it. The owner password lets you open it and also change its permissions. PasswordType is the answer of decrypt: not decrypted, user password or owner password. "
               "Project 12 combines many files in three steps: find the PDF files in a folder, open each one and copy all of its pages except the first, then save the new PDF. "
               "Slide 24 shows both passwords, and slides 27 and 28 run the project.")
NOTES["A6"] = ("A program that handles many files lists a folder or walks a folder tree and then treats every file alike. The os module holds the file-system functions. "
               "os.listdir returns the names in one folder, and os.walk visits every folder below a start folder. Sorting the names with case ignored puts A and a together before the pages are combined, "
               "and combine_pdfs.py is the finished program of Project 12. The same loop could watermark every page, split a book or number the pages. Slide 27 finds the files.")
NOTES["A7"] = ("A .docx file keeps its words, fonts and pictures in separate XML parts of a ZIP file. The Document object is the whole file in the program, a Paragraph is one paragraph of it, "
               "and a Run is a stretch of text inside a paragraph that has one formatting. You install python-docx but you write import docx. Reading a file means going through its paragraphs and then their runs, "
               "and readDocx.py joins the text of all paragraphs into the full text. Slide 32 opens the file.")
NOTES["A8"] = ("A style is a named formatting rule. A paragraph takes a paragraph style, which sets spacing and the size of the letters for the whole paragraph, and a run takes a character style, such as emphasis, for a few words. "
               "The paragraphs property lists the paragraphs of a document in order, and the runs property lists the runs of a paragraph; a run ends where the formatting changes. "
               "The name of a style must fit the kind of object and match exactly. Slide 36 shows both kinds and slide 37 shows what goes wrong.")
NOTES["A9"] = ("Each run attribute has three states: True turns the formatting on, False turns it off, and None means that the style decides. Bold makes the text bold, italic makes it italic, "
               "and underline draws a line under it. A run that never set an attribute reports None, so reading the attribute tells you whether the run decided or the style did. Slide 39 shows all three states, and the same idea returns in part 4 when a new run is written.")
NOTES["A10"] = ("A new document starts empty: you call docx.Document(), add content and save it to a file. add_paragraph adds a paragraph at the end and returns it, and add_run adds more text to a paragraph with its own formatting. "
                "add_heading adds a heading paragraph: level 0 is the title and levels 1 to 9 are headings. A line break starts a new line and is added inside a run with add_break; a page break ends the page and has a call of its own. "
                "Slide 43 writes a small file.")
NOTES["A11"] = ("add_picture places an image file in the document; give a width or a height and the other follows from the shape of the picture. Inches and Cm are units from docx.shared, which also holds Pt and other sizes. "
                "docx.enum.text holds named choices, such as the kind of break: LINE or PAGE. Slide 47 shows the sizes in code, and slide 45 earlier used the named choices.")
NOTES["A12"] = ("The practice programs combine the tools of the chapter. PDF Paranoia encrypts every PDF in a folder tree, tests the encrypted copy and only then removes the original. "
                "Custom Invitations writes one invitation for each guest into a Word file. The Password Breaker tries each word of a list as the password until decrypt succeeds. "
                "A brute-force attack tries every candidate, and a long random password has too many candidates to try. pdfminer.high_level is another library that also extracts the text of PDFs.")
