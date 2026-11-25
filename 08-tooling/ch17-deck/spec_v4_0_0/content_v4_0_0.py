"""Chapter 17 deck words 4.0.0 (Lineage10, change request 'no everyday analogies'): the twelve former analogy slides, the summary sentence and the
practice sentence state plainly what each concept is and does. Slide count (59), the slide titles' length rule, the concept names and everything else
stay as in content_v3_0_0.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_v3_0_0 as T0

__version__ = "4.0.0"

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "What it is and does"
CONCEPTS_TAIL = "each explained in plain words"

PARTS = T0.PARTS
PLAN = T0.PLAN
ROUTE_RUNS = T0.ROUTE_RUNS
ROUTE_TAIL = T0.ROUTE_TAIL
QUESTIONS = T0.QUESTIONS
QUESTIONS_TAKEAWAY = T0.QUESTIONS_TAKEAWAY
STORIES = T0.STORIES
TAKEAWAY = T0.TAKEAWAY
TOOLS = T0.TOOLS
TOOLS_TAKEAWAY = T0.TOOLS_TAKEAWAY
CURRENT = T0.CURRENT
CURRENT_SUB = T0.CURRENT_SUB
CURRENT_TAKEAWAY = T0.CURRENT_TAKEAWAY
RESOURCES = T0.RESOURCES
RESOURCES_SUB = T0.RESOURCES_SUB
RESOURCES_TAKEAWAY = T0.RESOURCES_TAKEAWAY
SUMMARY_POINTS = T0.SUMMARY_POINTS
SUMMARY_TAKEAWAY = T0.SUMMARY_TAKEAWAY
PRACTICE = T0.PRACTICE
PRACTICE_SUB = T0.PRACTICE_SUB
PRACTICE_TAKEAWAY = T0.PRACTICE_TAKEAWAY

SUMMARY_ANALOGY = "The summary keeps the five points to remember; each one can be traced to a slide."
PRACTICE_ANALOGY = "Each practice question has a short answer; run the code on the chapter page to check it."

ANALOGIES = [
 ('A1', 'PDF files and how pypdf reads them',
  'A PDF stores how each page is drawn, so its words are not kept as sentences you can move.',
  [('PDF Documents', 'A PDF stores each page as drawing commands, so the look is the same on every screen.'),
   ('PDF', 'A file format for pages: numbered objects, drawing commands and a table at the end.'),
   ('pypdf', 'A library that reads, copies, rotates, watermarks and locks PDF pages.'),
   ('PdfReader', 'Opens a PDF for reading; it changes nothing in the file.'),
   ('Page object', 'One page of the file; it can be rotated, merged with another or copied to a writer.'),
   ('pages', 'The list of page objects, counted from zero.'),
   ('is_encrypted', 'True when the file is locked; check it before you read the pages.'),
   ('io', 'Gives file objects that live in memory, such as BytesIO, and never touch the disk.')]),
 ('A2', 'Extracting text and pictures from PDFs',
  'extract_text() returns the words of a page in the order they were drawn, which may differ from reading order.',
  [('Extracting Text', 'Read the words of a page, in the order the file draws them.'),
   ('extract_text', 'One call on a page; it returns the text as one string.'),
   ('Post-Processing with AI', 'A model can mend extracted text: line breaks, hyphens and odd letters.'),
   ('Extracting Images', 'Take the pictures out of a page as image objects.'),
   ('images', 'The list of pictures found on one page; it needs the Pillow package.'),
   ('extractpdftext.py', 'Program: a PDF goes in, its text comes out as a text file.'),
   ('extractpdfimages.py', 'Program: saves the pictures of every page into a folder.'),
   ('open', 'Opens a file and returns a file object; close it when you are done.')]),
 ('A3', 'Building a new PDF from pages',
  'A PdfWriter starts empty; you add chosen pages from other files and then save it.',
  [('Creating PDFs from Other Pages', 'Copy chosen pages from existing files into a new PDF.'),
   ('PdfWriter', 'An empty new PDF; only the pages you add are in the new file.'),
   ('append', 'Copies pages to the end of the new file.'),
   ('merge', 'Copies pages in at a chosen position; name the pages= argument.'),
   ('Inserting Blank Pages', 'A blank page can separate one part of a document from the next.'),
   ('add_blank_page', 'Adds a blank page at the end of the new file.'),
   ('insert_blank_page', 'Adds a blank page at a given page number.'),
   ('Rotating Pages', 'Turn a page by multiples of 90 degrees, for example to read a wide table.')]),
 ('A4', 'Rotation, watermarks and passwords',
  'rotate() turns a page, merge_page() draws one page on another, and encrypt() locks the file.',
  [('rotate', 'Turns a page by quarter turns; the new angle adds to the angle it already has.'),
   ('Adding Watermarks and Overlays', 'Draw one page on another, so that both show.'),
   ('Watermark', 'A faint page drawn behind the words, such as DRAFT.'),
   ('Overlay', 'A page drawn on top of another page.'),
   ('merge_page', 'Draws a second page onto the page; the later page lies on top.'),
   ('Encrypting and Decrypting PDFs', 'Lock a file with a password, and unlock it with the same password.'),
   ('encrypt', 'Locks the new file with a password; the default method is RC4.'),
   ('decrypt', 'Tries a password and returns whether it fitted.')]),
 ('A5', 'User password, owner password, Project 12',
  'The user password opens the file to read; the owner password also controls its permissions.',
  [('PasswordType', 'The answer of decrypt: not decrypted, user password, or owner password.'),
   ('User password', 'Lets you open the file and read it.'),
   ('Owner password', 'Lets you open the file and also change its permissions.'),
   ('Project 12: Combine Select Pages from Many PDFs', 'One new PDF made from all pages but the first of every report.'),
   ('Step 1: Find All PDF Files', 'List the folder and keep only the names that end in .pdf.'),
   ('Step 2: Open Each PDF', 'Open each file in turn and copy all of its pages except the first.'),
   ('Step 3: Save the Results', 'Write the new PDF to a file such as combined.pdf.')]),
 ('A6', 'Working through many files',
  'A program that handles many files lists a folder or walks a folder tree, then treats every file alike.',
  [('os', 'The module with file-system functions: list folders, walk trees, join paths.'),
   ('os.listdir', 'Returns the names in one folder.'),
   ('os.walk', 'Visits every folder below a start folder, one after another.'),
   ('sort', 'Puts the file names in order; ignore case, so that A and a sort together.'),
   ('combine_pdfs.py', 'The finished program of Project 12.'),
   ('Ideas for Similar Programs', 'The same loop can watermark every page, split a book or number the pages.')]),
 ('A7', 'Word files and python-docx objects',
  'A .docx file holds paragraphs, and each paragraph holds runs of text that share one formatting.',
  [('Word Documents', 'A .docx file keeps words, fonts and pictures in separate XML parts of a ZIP file.'),
   ('docx', 'The import name: you install python-docx but you write import docx.'),
   ('Document object', 'The whole Word file in the program.'),
   ('Paragraph object', 'One paragraph of the document.'),
   ('Run object', 'A stretch of text inside a paragraph that has one formatting.'),
   ('Reading Word Documents', 'Open the file and go through its paragraphs, then through their runs.'),
   ('Getting the Full Text from a .docx File', 'Join the text of all paragraphs with line breaks.'),
   ('readDocx.py', 'Program: returns the full text of a .docx file.')]),
 ('A8', 'Paragraphs, runs and named styles',
  'A style is a named formatting rule; a paragraph takes a paragraph style and a run a character style.',
  [('paragraphs', 'The list of paragraphs of a document, in order.'),
   ('runs', 'The list of runs of a paragraph, in order; a run ends where the formatting changes.'),
   ('Styling Paragraph and Run Objects', 'Set a style on a whole paragraph, or on only a few words.'),
   ('Paragraph style', 'A rule for a whole paragraph: spacing, size of the letters, indent.'),
   ('Character style', 'A rule for a few words, such as emphasis.'),
   ('style', 'The name of the style; it must fit the kind of object and match exactly.')]),
 ('A9', 'Bold, italic and underline in runs',
  'Each run attribute has three states: True, False, or None, which means that the style decides.',
  [('Applying Run Attributes', 'Set the attributes of a run to turn a formatting on or off.'),
   ('bold', 'True makes the text bold, False removes it, None follows the style.'),
   ('italic', 'True makes the text italic, False removes it, None follows the style.'),
   ('underline', 'True draws a line under the text, False removes it, None follows the style.')]),
 ('A10', 'Writing a new Word file',
  'A new document starts empty; you add paragraphs, runs and headings, then save it.',
  [('Writing Word Documents', 'Start with docx.Document(), add content, then save to a file.'),
   ('add_paragraph', 'Adds a new paragraph at the end and returns it.'),
   ('add_run', 'Adds more text to a paragraph with its own formatting; it returns the run.'),
   ('Adding Headings', 'A heading is a paragraph that takes a heading style.'),
   ('add_heading', 'Level 0 is the title; levels 1 to 9 are headings.'),
   ('Adding Line and Page Breaks', 'A line break starts a new line; a page break starts a new page.'),
   ('add_break', 'Adds a line break inside a run; a page break has a call of its own.'),
   ('Page break', 'Ends the page; the next text starts on a new page.')]),
 ('A11', 'Pictures and their sizes',
  'add_picture() places a picture; give a width or a height and the other follows.',
  [('Adding Pictures', 'Add an image file to the document; it is placed in its own paragraph.'),
   ('add_picture', 'Takes the file and, if you give them, a width and a height.'),
   ('Inches', 'A unit from docx.shared: Inches(1) is one inch.'),
   ('Cm', 'A unit from docx.shared: Cm(2) is two centimetres.'),
   ('docx.shared', 'The module of sizes and units, such as Inches, Cm and Pt.'),
   ('docx.enum.text', 'The module of named choices, such as the kind of break: LINE or PAGE.')]),
 ('A12', 'Practice programs and brute force',
  'The practice programs combine the tools of the chapter; a brute-force attack tries every candidate password.',
  [('Practice Programs', 'Three small programs that combine the tools of this chapter.'),
   ('PDF Paranoia', 'Encrypt every PDF in a folder tree, test the copy, then remove the original.'),
   ('Custom Invitations', 'Write one invitation for each guest into a Word file.'),
   ('PDF Password Breaker', 'Tries each word of a list as the password until decrypt() succeeds.'),
   ('Brute-force attack', 'Tries every candidate; a long random password has too many to try.'),
   ('pdfminer.high_level', 'Another library that also extracts the text of PDFs.')])]
