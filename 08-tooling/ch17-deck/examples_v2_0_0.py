"""Chapter 17 deck examples, version 2.0.0: the code examples of the chapter 17 lecture deck (PDF and Word Documents).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language explanation that
stands beside it); the lines of all groups of an example, in order, are the example's code: that text is what the deck shows after the '>>> '
prompt of each line, what the chapter-code manifest lists and what the page runs. A code box holds at most 30 words (the deck standard counts
a code box as a text box, the '>>> ' prompt of each line included), the explanation of a group at most 30 words.
Every example is self-contained (it imports what it uses), uses pypdf, python-docx and Pillow (the packages the chapter page offers) and the standard library,
runs offline, reads no keyboard and opens no window, keeps its documents in memory (io.BytesIO) or in a fresh temporary folder, and prints an ordinary line first
(never an error message, so that the page can draw its result). What an example prints is the same under pypdf 5.9.0 and 6.20.1: pages are told apart by their width,
a layout string is split into words, and an error is caught and replaced by a plain sentence.
The book's own files (Recursion_Chapter1.pdf, demo.docx, watermark.pdf, zophie.png, dictionary.txt) are not used: each example builds a small stand-in with the same
kind of content, and says so.
Nothing here carries a result; deck_build_v2_0_0.py runs the code and takes every printed result from the run."""
__version__ = "2.0.0"

# a two-page PDF of 859 bytes, zlib-compressed and base64-coded so that it fits on a slide (made by the builder's own writer; page 1 draws the word 'world'
# first and then 'Hello'; page 2 draws a text line and then a black rectangle over it)
BLOB = [
    'eNq1kF9PgzAUxd/5FPdliT5oW6DAzMLD/sVEjcvAp2UP3SjIgtS0nW5+etsNRx',
    'BfLUlJT8+95/46WEznN+TWdwhgEJudMxqh9PjO0YRpVokCLVjBFbjmdhnHDq8z',
    'a3J/mU8m9FBmauVbJwR2X6OJ2Nca3LbQ+1U4F7VGyX6j7cEqBI2Z4if5nlcfXJ',
    'db1pb7f+SaTXKbYiPRE89KNhaHFTZHD2OI8BotuRJ7ueXK1NnW9kfAOzPFsRmz',
    '1qaFAtrFpG3cI68L/QqhZVFacvbmjFOwbUgEaQ6EYvAxpBlcfQpZZdeQ7mCWQs',
    'fkXjyGrRKNx6Y1LZvc4J8xwy5m2MekfUy/S5CwisnjHRAXmwUvyfQHGZ8+WZg3',
    'MaOB69oJQXLI+6QHyXPHTO/gy4KAUo9CDq02hPNN3WrU72mEkL4W9n1uRHuaj/',
    'saJUGracnKikv7Rkn5xSFCSyE0kOYllWZSn2ACb+gMBrPnufMNU9nkUQ==',
]


def _blob_group(first):
    """the code lines that hold the blob: `first` is the line before them"""
    return list(first) + ["blob = ('%s'" % BLOB[0]] + ["        '%s'" % b for b in BLOB[1:-1]] + ["        '%s')" % BLOB[-1]]


EXAMPLES = [
    # ------------------------------------------------------------ part 1: what a PDF holds
    dict(id="pdf_anatomy", name="Inside a small PDF", title="Inside a small PDF: header, objects, table, trailer", part=1, visual="pdf_anatomy",
         concepts=["PDF Documents", "PDF", "io", "open"],
         groups=[
             (_blob_group(["import base64, zlib"]),
              "A two-page PDF squeezed into text so that it fits a slide; the book's sample files are not needed."),
             (["data = zlib.decompress(base64.b64decode(blob))", "print(data[:8], data.rstrip().endswith(b'%%EOF'))", "text = data.decode()",
               "start = text.split('startxref')[1].split()[0]", "print(text.count(' obj'), 'objects; table at byte', start)"],
              "The file starts with a version line, ends with an EOF marker, and startxref names the byte where the table begins."),
         ]),
    dict(id="reader_pages", name="PdfReader, pages and page size", title="PdfReader: pages, their size and whether the file is locked", part=1, visual="reader_pages",
         concepts=["PdfReader", "PdfWriter", "Page object", "pages", "is_encrypted", "io", "pypdf"],
         groups=[
             (["import io, pypdf", "writer = pypdf.PdfWriter()", "for width in (100, 200, 300): writer.add_blank_page(width, 100)"],
              "A PdfWriter starts empty. Three blank pages of different widths stand in for a real document."),
             (["buf = io.BytesIO()", "writer.write(buf)", "reader = pypdf.PdfReader(buf)", "print(len(reader.pages), 'pages; locked:', reader.is_encrypted)"],
              "write() saves into memory; PdfReader reads it back. pages is a list, and is_encrypted says whether a password is needed."),
             (["widths = [float(p.mediabox.width) for p in reader.pages]", "print('width of each page in points:', widths)"],
              "Page numbers count from 0 in code. The media box is the page's size in points; 72 points make an inch."),
         ]),
    dict(id="extract_text", name="Extracting text: stream order and the black box", title="Extracting text: what comes out, and what a black box hides", part=1, visual="extract_text",
         concepts=["Extracting Text", "extract_text", "PdfReader", "Page object", "pages", "pypdf"],
         groups=[
             (_blob_group(["import base64, io, zlib, pypdf"]),
              "The same sample. Page 1 draws world, then Hello; page 2 draws a salary line, then a black box over it."),
             (["pdf = zlib.decompress(base64.b64decode(blob))", "reader = pypdf.PdfReader(io.BytesIO(pdf))", "print('stream order:', repr(reader.pages[0].extract_text()))",
               "layout = reader.pages[0].extract_text(extraction_mode='layout')", "print('layout mode:', layout.split())",
               "print('under the black box:', reader.pages[1].extract_text())"],
              "Stream order is the order of drawing: worldHello. Layout mode sorts by position. The black box only covers the text."),
         ]),
    dict(id="post_process", name="Post-processing extracted text", title="Post-processing: mend the text before anyone reads it", part=1, visual="post_process",
         concepts=["Post-Processing with AI", "Extracting Text", "extract_text"],
         groups=[
             (["import re", "raw = 'The ﬁrst chap-\\nter was long.\\nIt had two\\nlines.'", "print(repr(raw))"],
              "Extracted text often has a ligature, a hyphen at a line end and breaks inside sentences. This line imitates that."),
             (["text = raw.replace('ﬁ', 'fi')", "text = re.sub(r'-\\n', '', text)", "text = re.sub(r'(?<!\\.)\\n', ' ', text)", "print(repr(text))"],
              "Three repairs: swap the ligature, join the hyphenated word, and turn a break into a space unless a sentence ended."),
             (["prompt = 'Fix the line breaks of this text:\\n' + raw", "n = len(prompt.split())", "print(len(raw.split()), 'words in; a prompt of', n, 'words')"],
              "The chapter hands such repairs to a language model. These lines only build the request; no model is called."),
         ]),
    dict(id="scan_images", name="Extracting images, and a page with no text", title="Extracting images: a scanned page is a picture without text", part=1, visual="scan_images",
         concepts=["Extracting Images", "images", "Page object", "extractpdfimages.py", "open", "os"],
         groups=[
             (["import io, os, tempfile, pypdf", "from PIL import Image", "buf = io.BytesIO()", "Image.new('RGB', (60, 40), 'red').save(buf, 'PDF')"],
              "Pillow saves a small red picture as a one-page PDF. A scan is such a page: a picture and no text."),
             (["page = pypdf.PdfReader(buf).pages[0]", "print('text found:', repr(page.extract_text()))", "print('images found:', len(page.images))"],
              "There is no text, so extract_text() returns an empty string. The picture is there: page.images lists it."),
             (["os.chdir(tempfile.mkdtemp())", "for i, image in enumerate(page.images, 1):", "    open('page1_%d.bin' % i, 'wb').write(image.data)",
               "size = Image.open(io.BytesIO(page.images[0].data)).size", "print(os.listdir('.'), size)"],
              "The chapter's loop writes each image's bytes to a file. The bytes open as a picture of 60 by 40 pixels."),
         ]),
    # ------------------------------------------------------------ part 2: new PDFs from pages
    dict(id="append_pages", name="Copying pages: a tuple is a range", title="Copying pages into a new file: a tuple is a range, a list is exact", part=2, visual="append_pages",
         concepts=["Creating PDFs from Other Pages", "PdfWriter", "append", "pages", "io"],
         groups=[
             (["import io, pypdf", "src = pypdf.PdfWriter()", "for n in range(1, 7): src.add_blank_page(100 * n, 100)", "buf = io.BytesIO()", "src.write(buf)"],
              "A six-page source. Page n is n hundred points wide, so a width tells which page it was."),
             (["def pick(pages):", "    w = pypdf.PdfWriter()", "    w.append(io.BytesIO(buf.getvalue()), pages)", "    return [int(p.mediabox.width) // 100 for p in w.pages]"],
              "pick() copies chosen pages into a new writer and reports which source pages arrived."),
             (["for pages in ((0, 5), (0, 5, 2), [0, 5]):", "    print(pages, '->', pick(pages))"],
              "A tuple is a range like range(): start, stop, step. A list names the pages exactly."),
         ]),
    dict(id="merge_insert", name="merge() and blank pages", title="merge() puts pages inside; blank pages fill gaps", part=2, visual="merge_insert",
         concepts=["Inserting Blank Pages", "merge", "add_blank_page", "insert_blank_page", "PdfWriter", "pages"],
         groups=[
             (["import io, pypdf", "w = pypdf.PdfWriter()", "for n in (1, 2, 3): w.add_blank_page(100 * n, 100)"],
              "Three pages 100, 200 and 300 points wide. add_blank_page() adds a page at the end."),
             (["other = pypdf.PdfWriter()", "for n in (7, 8): other.add_blank_page(100 * n, 100)", "buf = io.BytesIO()", "other.write(buf)"],
              "A second file of two pages, 700 and 800 points wide, kept in memory."),
             (["def sizes(): return [int(p.mediabox.width) for p in w.pages]", "w.merge(1, buf, pages=(0, 2))", "print('after merge at 1:', sizes())",
               "w.insert_blank_page(index=2)", "print('after insert_blank_page:', sizes())"],
              "merge() inserts pages at position 1; write pages=, or a tuple is read as a bookmark title. A blank page copies its neighbour's size."),
         ]),
    dict(id="rotate_pages", name="Rotating pages", title="Rotating pages: angles add up and must be multiples of 90", part=2, visual="rotate_pages",
         concepts=["Rotating Pages", "rotate", "Page object", "PdfWriter"],
         groups=[
             (["import pypdf", "page = pypdf.PdfWriter().add_blank_page(100, 100)", "print('start:', page.rotation)"],
              "A fresh page has rotation 0. add_blank_page() returns the new Page object."),
             (["seen = [page.rotate(angle).rotation for angle in (90, 270, -90, 180)]", "print('rotation after each turn:', seen)"],
              "rotate() turns the page clockwise and adds the angle to the total already there. The total is not wrapped at 360."),
             (["try:", "    page.rotate(45)", "except ValueError:", "    print('45 degrees refused: use multiples of 90')"],
              "Only quarter turns are allowed. Any other angle raises a ValueError, caught here."),
         ]),
    dict(id="watermark", name="Watermarks and overlays", title="Watermarks and overlays: merge_page lays one page on another", part=2, visual="watermark",
         concepts=["Adding Watermarks and Overlays", "Watermark", "Overlay", "merge_page", "images", "Page object"],
         groups=[
             (["import io, pypdf", "from PIL import Image", "def page_with(size, color):", "    buf = io.BytesIO()", "    Image.new('RGB', size, color).save(buf, 'PDF')",
               "    return pypdf.PdfReader(buf).pages[0]"],
              "A helper that makes a one-page PDF holding a picture of one size and colour."),
             (["base = page_with((60, 40), 'blue')", "top = page_with((30, 20), 'red')", "before = len(base.images)", "base.merge_page(top)"],
              "A big blue page stands for the document, a small red one for the stamp. merge_page() copies the stamp onto the base page."),
             (["print('images:', before, '->', len(base.images))", "print('drawn first to last:', [im.image.size for im in base.images])"],
              "The page now draws two pictures. The later one lies on top: by default the stamp goes over the page."),
         ]),
    dict(id="encrypt_decrypt", name="Encrypt and decrypt", title="Encrypt, then decrypt: a locked file refuses its pages", part=2, visual="encrypt_decrypt",
         concepts=["Encrypting and Decrypting PDFs", "encrypt", "decrypt", "is_encrypted", "PasswordType", "User password"],
         groups=[
             (["import io, pypdf", "writer = pypdf.PdfWriter()", "writer.add_blank_page(100, 100)", "writer.encrypt('userpw', algorithm='AES-256')",
               "buf = io.BytesIO()", "writer.write(buf)"],
              "encrypt() locks the file with a password. AES-256 is the strong algorithm; the default form is weaker."),
             (["reader = pypdf.PdfReader(buf)", "print('locked:', reader.is_encrypted)", "try: reader.pages[0]", "except Exception as e: print('refused:', type(e).__name__)"],
              "A reader opens a locked file but refuses its pages. The refusal is an error, caught here to go on."),
             (["for guess in ('wrong', 'userpw'):", "    print(repr(guess), '->', reader.decrypt(guess).name)", "print(len(reader.pages), 'page after decrypt')"],
              "decrypt() answers with a PasswordType. One password serves as user and owner password, so a match says OWNER_PASSWORD."),
         ]),
    dict(id="user_owner", name="User and owner passwords", title="Two passwords: the user opens, the owner may do more", part=2, visual="user_owner",
         concepts=["User password", "Owner password", "PasswordType", "encrypt", "decrypt"],
         groups=[
             (["import io, pypdf", "writer = pypdf.PdfWriter()", "writer.add_blank_page(100, 100)",
               "writer.encrypt(user_password='open-me', owner_password='boss',", "               algorithm='AES-256')"],
              "One file, two passwords. The user password is for reading; the owner password is for whoever controls the file."),
             (["buf = io.BytesIO()", "writer.write(buf)", "for pw in ('open-me', 'boss', 'guess'):", "    reader = pypdf.PdfReader(io.BytesIO(buf.getvalue()))",
               "    print(pw, '->', reader.decrypt(pw).name)"],
              "decrypt() tells which password matched: USER_PASSWORD, OWNER_PASSWORD or NOT_DECRYPTED. Each try uses a fresh reader."),
         ]),
    dict(id="encrypt_schemes", name="Which lock was used", title="Which lock was used: RC4 by default, AES when asked", part=2, visual="encrypt_schemes",
         concepts=["encrypt", "Encrypting and Decrypting PDFs", "is_encrypted"],
         groups=[
             (["import io, pypdf", "def lock(**options):", "    w = pypdf.PdfWriter()", "    w.add_blank_page(100, 100)", "    w.encrypt('pw', **options)",
               "    b = io.BytesIO()", "    w.write(b)", "    return pypdf.PdfReader(b).trailer['/Encrypt']"],
              "A helper that locks a one-page file with the options given and returns the record of the lock that the file keeps."),
             (["for algo in (None, 'AES-128', 'AES-256'):", "    e = lock(algorithm=algo)", "    v, r, bits = e['/V'], e['/R'], e['/Length']", "    print('%s: V=%d R=%d bits=%d' % (algo, v, r, bits))"],
              "None asks for the default, the old RC4. V and R name the scheme; AES needs the cryptography package."),
         ]),
    dict(id="project12_find", name="Project 12, step 1: find the PDF files", title="Project 12, step 1: find all PDF files and sort them", part=2, visual="project12_find",
         concepts=["Project 12: Combine Select Pages from Many PDFs", "Step 1: Find All PDF Files", "os.listdir", "sort", "os", "Ideas for Similar Programs"],
         groups=[
             (["import os, tempfile", "os.chdir(tempfile.mkdtemp())", "for name in ('b.pdf', 'A.pdf', 'c.PDF', 'notes.txt'):", "    open(name, 'w').close()"],
              "A folder with three PDF names and a text file, all empty: step 1 only needs names. One PDF has a capital extension."),
             (["pdf_filenames = []", "for filename in os.listdir('.'):", "    if filename.lower().endswith('.pdf'):", "        pdf_filenames.append(filename)",
               "pdf_filenames.sort(key=str.lower)", "print(pdf_filenames)"],
              "listdir() names everything in the folder. lower() lets the test see c.PDF too, and the sort ignores case."),
         ]),
    dict(id="project12_combine", name="Project 12, steps 2 and 3: combine and save", title="Project 12, steps 2 and 3: open each PDF, copy, save", part=2, visual="project12_combine",
         concepts=["Project 12: Combine Select Pages from Many PDFs", "Step 2: Open Each PDF", "Step 3: Save the Results", "combine_pdfs.py", "append", "PdfWriter"],
         groups=[
             (["import os, tempfile, pypdf", "os.chdir(tempfile.mkdtemp())", "w = pypdf.PdfWriter()", "w.add_blank_page(100, 100)", "for name in ('b.pdf', 'A.pdf', 'c.PDF'):",
               "    w.add_blank_page(100, 100)", "    w.write(name)"],
              "Three PDFs of 2, 3 and 4 pages stand in for the folder's files: one writer is saved after each added page."),
             (["pdf_filenames = ['A.pdf', 'b.pdf', 'c.PDF']", "writer = pypdf.PdfWriter()", "for name in pdf_filenames:",
               "    writer.append(name, (1, len(pypdf.PdfReader(name).pages)))"],
              "Step 2: open each file in the sorted order and copy the range (1, number of pages): the first page of each file is skipped."),
             (["writer.write('combined.pdf')", "sizes = [len(pypdf.PdfReader(n).pages) for n in pdf_filenames]", "print(sizes, 'pages ->', len(pypdf.PdfReader('combined.pdf').pages))"],
              "Step 3: save the result, then read back the sizes of the three files and of the new file."),
         ]),
    # ------------------------------------------------------------ part 3: reading Word documents
    dict(id="docx_zip", name="A .docx file is a ZIP of XML", title="A .docx file is a ZIP archive of XML parts", part=3, visual="docx_zip",
         concepts=["Word Documents", "Word document (.docx)", "docx", "Document object", "io"],
         groups=[
             (["import io, zipfile, docx", "doc = docx.Document()", "doc.add_paragraph('Hello, world!')", "buf = io.BytesIO()", "doc.save(buf)"],
              "A new document with one paragraph, saved into memory. python-docx is installed as python-docx and imported as docx."),
             (["print(buf.getvalue()[:2], 'starts every ZIP file')", "z = zipfile.ZipFile(buf)", "names = z.namelist()", "part = 'word/document.xml'",
               "print(len(names), 'parts;', part, 'in names:', part in names)"],
              "The first two bytes are PK, the mark of a ZIP file. The zipfile module lists the parts inside."),
             (["body = z.read(part).decode().split('<w:body>')[1]", "print(body[:46])"],
              "The text lives in word/document.xml, in XML tags: a paragraph, a run, the text."),
         ]),
    dict(id="docx_read", name="Paragraphs and runs", title="Reading a Word file: paragraphs hold runs", part=3, visual="docx_read",
         concepts=["Reading Word Documents", "Document object", "Paragraph object", "Run object", "paragraphs", "runs", "bold"],
         groups=[
             (["import docx", "doc = docx.Document()", "p = doc.add_paragraph('A plain ')", "p.add_run('bold').bold = True", "p.add_run(' word.')"],
              "A stand-in for demo.docx: one paragraph of three runs. A run is a stretch of text with one look."),
             (["table = doc.add_table(rows=1, cols=1)", "table.cell(0, 0).text = 'in a table'"],
              "A table with one cell. Its text is part of the document, but not of any paragraph in it."),
             (["print([x.text for x in doc.paragraphs])", "print([(r.text, r.bold) for r in p.runs])", "print('table text is kept apart:', doc.tables[0].cell(0, 0).text)"],
              "doc.paragraphs lists Paragraph objects, and each has runs. Table text is not in that list; it sits in doc.tables."),
         ]),
    dict(id="docx_fulltext", name="Getting the full text of a .docx file", title="Getting the full text from a .docx file", part=3, visual="docx_fulltext",
         concepts=["Getting the Full Text from a .docx File", "readDocx.py", "Document object", "paragraphs", "open", "io"],
         groups=[
             (["import io, docx", "doc = docx.Document()", "for line in ('Title line', 'First paragraph.', 'Second paragraph.'):", "    doc.add_paragraph(line)",
               "buf = io.BytesIO()", "doc.save(buf)"],
              "A three-paragraph document saved in memory. The buffer stands in for a file name."),
             (["def get_text(source):", "    doc = docx.Document(source)", "    return '\\n'.join(p.text for p in doc.paragraphs)",
               "text = get_text(io.BytesIO(buf.getvalue()))", "print(text)", "print(len(text.split('\\n')), 'lines,', len(text.split()), 'words')"],
              "The idea of readDocx.py: open the file, join each paragraph's text with a line break. Document() takes a name or a file object."),
         ]),
    dict(id="docx_styles", name="Styles: paragraph kind and run kind", title="Styles: a paragraph style and a run style", part=3, visual="docx_styles",
         concepts=["Styling Paragraph and Run Objects", "Paragraph style", "Character style", "style", "Paragraph object", "Run object"],
         groups=[
             (["import docx", "doc = docx.Document()", "p = doc.add_paragraph('Quoted words')", "p.style = 'Quote'", "print('paragraph style:', p.style.name)"],
              "A paragraph style shapes the whole paragraph. Quote is a paragraph style of the default template."),
             (["run = p.add_run(' and a run')", "run.style = 'Quote Char'", "print('run style:', run.style.name)", "print(len(doc.styles), 'styles in a new document')"],
              "A character style shapes a run. Quote Char matches Quote. The template holds 164 styles of four kinds."),
         ]),
    dict(id="docx_style_errors", name="Styles: the kind and the exact name", title="Styles: the right kind and the exact name", part=3, visual="docx_style_errors",
         concepts=["Paragraph style", "Character style", "style", "Paragraph object"],
         groups=[
             (["import docx", "doc = docx.Document()", "p = doc.add_paragraph('Quoted words')", "try: p.style = 'Quote Char'",
               "except ValueError: print('a paragraph refuses a character style')"],
              "The kind must fit the object: a character style on a paragraph raises a ValueError, caught here."),
             (["try: doc.add_paragraph('x', 'List Number ')", "except KeyError: print('style not found: names match exactly')",
               "doc.add_paragraph('x', 'List Number')", "print('List Number found:', doc.paragraphs[-1].style.name)"],
              "The name must match letter for letter. One trailing space, as the book's printed list shows, and the style is not found."),
         ]),
    dict(id="run_attributes", name="Run attributes: three states", title="Run attributes: bold, italic and underline have three states", part=3, visual="run_attributes",
         concepts=["Applying Run Attributes", "bold", "italic", "underline", "Run object", "style"],
         groups=[
             (["import docx", "doc = docx.Document()", "run = doc.add_paragraph().add_run('text')", "for value in (True, False, None):",
               "    run.bold = value", "    print('bold =', value, '-> reads back', run.bold)"],
              "True turns bold on, False turns it off, None means the style decides. The run reads back what was set."),
             (["run.italic, run.underline = True, True", "print('italic:', run.italic, '| underline:', run.underline)"],
              "Italic and underline work like bold. These three are real attributes of a run."),
             (["run.strike = True", "print('run.strike ->', run.font.strike)", "run.font.strike = True", "print('run.font.strike ->', run.font.strike)"],
              "Strike is not an attribute of a run: setting it does nothing and raises no error. It lives in run.font."),
         ]),
    # ------------------------------------------------------------ part 4: writing Word documents
    dict(id="docx_write", name="Writing paragraphs and runs", title="Writing a Word file: add_paragraph and add_run", part=4, visual="docx_write",
         concepts=["Writing Word Documents", "add_paragraph", "add_run", "Document object", "Paragraph object", "Run object"],
         groups=[
             (["import io, docx", "doc = docx.Document()", "p = doc.add_paragraph('Hello world!')", "r = p.add_run(' A second run.')", "r.italic = True",
               "print(type(p).__name__, type(r).__name__)"],
              "add_paragraph() returns the new Paragraph; add_run() returns the new Run. Keep them to change them."),
             (["buf = io.BytesIO()", "doc.save(buf)", "again = docx.Document(buf)", "texts = [r.text for r in again.paragraphs[0].runs]", "print(len(again.paragraphs), 'paragraph; runs:', texts)"],
              "save() writes the file; opening it again shows one paragraph whose two runs kept their text."),
         ]),
    dict(id="docx_headings", name="Adding headings", title="Adding headings: levels 0 to 9", part=4, visual="docx_headings",
         concepts=["Adding Headings", "add_heading", "Paragraph style", "Document object"],
         groups=[
             (["import docx", "doc = docx.Document()", "for level in (0, 1, 9):", "    h = doc.add_heading('Heading %d' % level, level)",
               "    print('level', level, '->', h.style.name)"],
              "add_heading() takes a level. Level 0 is the Title style; levels 1 to 9 are Heading 1 to Heading 9."),
             (["try: doc.add_heading('Too deep', 10)", "except ValueError: print('level 10 refused: levels are 0 to 9')"],
              "Outside 0 to 9 the call raises a ValueError. The chapter says 0 to 4 in one place and 1 to 9 in another."),
         ]),
    dict(id="docx_breaks", name="Line and page breaks", title="Adding line breaks and page breaks", part=4, visual="docx_breaks",
         concepts=["Adding Line and Page Breaks", "add_break", "Page break", "Run object", "docx.enum.text"],
         groups=[
             (["import docx", "from docx.enum.text import WD_BREAK", "doc = docx.Document()", "p = doc.add_paragraph('First line')",
               "p.add_run().add_break(WD_BREAK.LINE)", "p.add_run('second line, same paragraph')"],
              "A break is an item inside a run. WD_BREAK.LINE starts a new line without starting a new paragraph."),
             (["doc.add_page_break()", "doc.add_paragraph('Second page')", "xml = doc.element.xml", "pages = xml.count('w:type=\"page\"')",
               "print(pages, 'page break;', xml.count('<w:br'), 'breaks in all')"],
              "add_page_break() adds a paragraph that holds a page break. Counting tags in the XML shows one page break among two breaks."),
         ]),
    dict(id="docx_picture", name="Adding pictures", title="Adding pictures: width and height in inches or centimetres", part=4, visual="docx_picture",
         concepts=["Adding Pictures", "add_picture", "Inches", "Cm", "docx.shared", "io"],
         groups=[
             (["import io, docx", "from PIL import Image", "from docx.shared import Cm, Inches", "png = io.BytesIO()",
               "Image.new('RGB', (60, 80), 'red').save(png, 'PNG')", "doc = docx.Document()"],
              "Pillow makes a stand-in for zophie.png: 60 by 80 pixels, kept in memory."),
             (["sizes = {'as is': {}, '1 inch wide': {'width': Inches(1)},", "         '2 cm high': {'height': Cm(2)}}"],
              "Three ways to place it: as it is, one inch wide, or two centimetres high."),
             (["for label, kw in sizes.items():", "    shape = doc.add_picture(io.BytesIO(png.getvalue()), **kw)",
               "    print(label, '->', int(shape.width), 'x', int(shape.height), 'EMU')"],
              "Give a width or a height and the other follows. Sizes are stored in EMU: 914400 to the inch."),
         ]),
    # ------------------------------------------------------------ part 5: practice programs
    dict(id="pdf_paranoia_walk", name="Practice program: PDF Paranoia, walk the tree", title="Practice program 1, part 1: walk a folder tree for PDFs", part=5, visual="pdf_paranoia_walk",
         concepts=["PDF Paranoia", "Practice Programs", "os.walk", "os"],
         groups=[
             (["import os, tempfile", "os.chdir(tempfile.mkdtemp())", "os.makedirs('tree/sub')", "for path in ('tree/a.pdf', 'tree/sub/B.PDF', 'tree/c.txt'):",
               "    open(path, 'w').close()"],
              "A folder tree of two PDF names and a text file stands in for the reader's files. One extension is in capitals."),
             (["found = []", "for folder, dirs, names in os.walk('tree'):", "    for name in names:", "        if name.lower().endswith('.pdf'):",
               "            found.append(os.path.join(folder, name))", "print(sorted(found))"],
              "os.walk visits every folder of the tree. Each name ending in .pdf, in any case, becomes a full path."),
         ]),
    dict(id="pdf_paranoia", name="Practice program: PDF Paranoia, lock and check", title="Practice program 1, part 2: lock a copy, check it, remove the original", part=5, visual="pdf_paranoia",
         concepts=["PDF Paranoia", "Practice Programs", "encrypt", "decrypt", "PasswordType", "os"],
         groups=[
             (["import os, tempfile, pypdf", "os.chdir(tempfile.mkdtemp())", "w = pypdf.PdfWriter()", "w.add_blank_page(100, 100)", "w.write('a.pdf')"],
              "One small PDF stands in for a file the program found."),
             (["w = pypdf.PdfWriter(clone_from='a.pdf')", "w.encrypt('swordfish', algorithm='AES-256')", "w.write('a_encrypted.pdf')",
               "r = pypdf.PdfReader('a_encrypted.pdf')", "ok = r.is_encrypted and r.decrypt('swordfish').name != 'NOT_DECRYPTED'",
               "if ok: os.remove('a.pdf')", "print(ok, os.listdir('.'))"],
              "Copy, lock, save under a new name, test the copy with the password, and only then remove the original."),
         ]),
    dict(id="custom_invitations", name="Practice program: Custom Invitations", title="Practice program 2: Custom Invitations", part=5, visual="custom_invitations",
         concepts=["Custom Invitations", "Practice Programs", "Paragraph style", "Page break", "add_paragraph", "docx.shared", "docx.enum.text"],
         groups=[
             (["import docx", "doc = docx.Document()", "guests = ['Prof. Plum', 'Miss Scarlet', 'Col. Mustard']"],
              "Three guests. The book's invitations use styles from a template file; the built-in Title style stands in for them."),
             (["for i, guest in enumerate(guests):", "    doc.add_paragraph('You are invited,')", "    doc.add_paragraph(guest, 'Title')",
               "    if i < len(guests) - 1:", "        doc.add_page_break()"],
              "One card per guest: a line, then the name in the big style. A page break follows every card but the last."),
             (["names = [p.text for p in doc.paragraphs if p.style.name == 'Title']", "xml = doc.element.xml", "print(len(names), 'guests;', xml.count('w:type=\"page\"'), 'page breaks')", "print(names)"],
              "Three cards need two page breaks. Filtering by style name finds the names again."),
         ]),
    dict(id="password_breaker", name="Practice program: PDF Password Breaker", title="Practice program 3: PDF Password Breaker", part=5, visual="password_breaker",
         concepts=["PDF Password Breaker", "Practice Programs", "Brute-force attack", "decrypt", "PasswordType", "open"],
         groups=[
             (["import io, pypdf", "words = ['apple', 'banana', 'cherry', 'dragonfruit']", "w = pypdf.PdfWriter()", "w.add_blank_page(100, 100)",
               "w.encrypt('CHERRY', algorithm='AES-256')", "buf = io.BytesIO()", "w.write(buf)"],
              "A locked file whose password is a dictionary word in capitals. Four words stand in for the book's dictionary.txt."),
             (["reader = pypdf.PdfReader(buf)", "tries = [g for x in words for g in (x, x.upper())]", "for attempts, guess in enumerate(tries, 1):",
               "    if reader.decrypt(guess).name != 'NOT_DECRYPTED': break"],
              "Try every word in lower case, then in capitals, until decrypt() stops answering NOT_DECRYPTED."),
             (["print('found', guess, 'after', attempts, 'of at most', len(tries))"],
              "Attempts grow with the dictionary and the cases tried. A long random password is in no dictionary."),
         ]),
]

BY_ID = {e["id"]: e for e in EXAMPLES}
assert len(BY_ID) == len(EXAMPLES)
assert len({e["name"] for e in EXAMPLES}) == len(EXAMPLES)


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
