"""Chapter 17 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter was read on automatetheboringstuff.com on 2026-10-12 (an HTTP fetch of https://automatetheboringstuff.com/3e/chapter17.html;
the page returned 200, 100,057 bytes, and its sha256, 00cb1643dca3afd3b75bfd9ce7ad594f3dd80f8606de1cffe40b8583846b4789, equals the chapterDigest the
book's own chapter ontology records; the commit the course pins was not opened). The online materials of the 3rd edition (the zip No Starch Press
links from its book page, 7,759,877 bytes) were downloaded and the files chapter 17 uses were opened and their sha256 recorded (Recursion_Chapter1.pdf,
18 pages; watermark.pdf; demo.docx; zophie.png; guests.txt; dictionary.txt; and the book's scripts extractpdftext.py, extractpdfimages.py,
combine_pdfs.py and readDocx.py); neither the zip nor the files are kept in this repository, and the scripts fetch them and check the hashes. The pypdf,
python-docx and pdfminer.six documentation, the Python 3.14 documentation, PyPI, the standards pages, the pages of the stories and the other
sources were opened on the same day. Every behaviour was executed under Python 3.14.6 (installed with uv) on Ubuntu 24.04 (Linux) in a
dedicated environment with pypdf 6.20.1, python-docx 1.2.0, pdfminer.six 20260107, Pillow 12.3.0 and cryptography 50.0.2, and the chapter's statements were
also replayed with the versions Appendix A of the book pins (pypdf 5.0.1, python-docx 1.1.2). Not executed, and said so where it comes up: Microsoft Word
itself and any PDF viewer (LibreOffice 24.2 and the poppler and qpdf tools stood in for them), the language model clean-up of extracted text, the Mu editor,
the book's figures as drawn, and the Practice Programs as readers would write them (the programs were written and run on files made for the purpose).
The chapter's 91 interactive statements are replayed by sen0414_ch17_thirdparty_v1_0_0.py into 08-tooling/ch17-page/third_party_record_v1_0_0.json;
what the public sites and the shipped files did on the day, with the worst case of the PDF Password Breaker run to the end, is in
ch17-page/live_observations_v1_0_0.json; what one program printed under ten interpreters (3.11, 3.12, 3.13 and the seven 3.14 releases) is in
ch17-page/interpreter_record_v1_0_0.json. A claim not in this file was not made."""
__version__ = "1.0.1"
# 1.0.0 (25 sources, 2026-10-01, pypdf 6.19.0, small stand-in files for the book's own) stays in the repository; this version rebuilds the chapter with
# two cross-referenced paragraphs per section, the shipped files opened, the chapter's statements replayed, and the public sources as they answered on
# 2026-10-12. The data module is 1.0.1 because 1.0.0 is already committed.
CH = 17
DATE = "2026-10-12"
PYVER = "3.14.6"
TITLE = "PDF and Word documents for an advanced course: chapter 17 and today's pypdf, python-docx and Python"
QUESTION = "What does chapter 17 of the 3rd edition teach about reading and writing PDF and Word documents with PyPDF and Python-Docx, which of its printed outputs, programs and statements still hold under Python 3.14.6 with pypdf 6.20.1 and python-docx 1.2.0 (and with the versions its Appendix A pins), and what must an advanced course correct or add so that it matches the current packages?"
CQS = ("Which operations read a document, which build a new one from parts of others, and which cannot be done at all, given that PDF and Word files are made for people to read and not for programs to parse?",
       "Which printed outputs, programs, numbers and statements of the chapter differ in current releases of the packages, in the files the book ships or in the pages it points to, and on what source?")
PUBS = [
 ('P01', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 17, PDF and Word Documents (Al Sweigart, No Starch Press, 2025)', 'https://automatetheboringstuff.com/3e/chapter17.html', True),
 ('P02', 'Online materials of the 3rd edition, zip with Recursion_Chapter1.pdf, watermark.pdf, demo.docx, zophie.png, guests.txt and dictionary.txt (No Starch Press, 2025)', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', False),
 ('P03', 'Automate the Boring Stuff with Python, 3rd edition - table of contents (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/', False),
 ('P04', 'Automate the Boring Stuff with Python, 3rd edition - book page (No Starch Press, 2025)', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', False),
 ('P05', 'Appendix A, Installing Third-Party Modules, with the versions the book pins (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixa.html', False),
 ('P06', 'pypdf documentation, home page (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/', False),
 ('P07', 'pypdf documentation, Extract Text from a PDF (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/user/extract-text.html', False),
 ('P08', 'pypdf documentation, Post-Processing of Text Extraction (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/latest/user/post-processing-in-text-extraction.html', False),
 ('P09', 'pypdf documentation, Extract Images (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/user/extract-images.html', False),
 ('P10', 'pypdf documentation, Merging PDF files (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/user/merging-pdfs.html', False),
 ('P11', 'pypdf documentation, Encryption and Decryption of PDFs (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/user/encryption-decryption.html', False),
 ('P12', 'pypdf documentation, Adding a Stamp or Watermark to a PDF (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/user/add-watermark.html', False),
 ('P13', 'pypdf documentation, Installation, with the optional dependencies (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/user/installation.html', False),
 ('P14', 'pypdf documentation, the PdfWriter class (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/modules/PdfWriter.html', False),
 ('P15', 'pypdf documentation, the PageObject class (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/modules/PageObject.html', False),
 ('P16', 'pypdf documentation, Changelog (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/meta/CHANGELOG.html', False),
 ('P17', 'pypdf documentation, History of pypdf (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/meta/history.html', False),
 ('P18', 'pypdf documentation, Security (pypdf contributors, 2026)', 'https://pypdf.readthedocs.io/en/stable/user/security.html', False),
 ('P19', 'python-docx documentation, Quickstart (Steve Canny, 2013)', 'https://python-docx.readthedocs.io/en/latest/user/quickstart.html', False),
 ('P20', 'python-docx documentation, Working with Text (Steve Canny, 2013)', 'https://python-docx.readthedocs.io/en/latest/user/text.html', False),
 ('P21', 'python-docx documentation, Understanding Styles (Steve Canny, 2013)', 'https://python-docx.readthedocs.io/en/latest/user/styles-understanding.html', False),
 ('P22', 'python-docx documentation, Working with Styles (Steve Canny, 2013)', 'https://python-docx.readthedocs.io/en/latest/user/styles-using.html', False),
 ('P23', 'python-docx documentation, API: Document objects (Steve Canny, 2013)', 'https://python-docx.readthedocs.io/en/latest/api/document.html', False),
 ('P24', 'python-docx documentation, API: Text and Run objects (Steve Canny, 2013)', 'https://python-docx.readthedocs.io/en/latest/api/text.html', False),
 ('P25', 'python-docx documentation, Installation (Steve Canny, 2013)', 'https://python-docx.readthedocs.io/en/latest/user/install.html', False),
 ('P26', 'python-docx documentation, home page (Steve Canny, 2013)', 'https://python-docx.readthedocs.io/en/latest/', False),
 ('P27', 'pdfminer.six documentation (pdfminer.six contributors, 2026)', 'https://pdfminersix.readthedocs.io/en/latest/', False),
 ('P28', 'PyPI JSON metadata of pypdf (Python Package Index, 2026)', 'https://pypi.org/pypi/pypdf/json', False),
 ('P29', 'PyPI JSON metadata of docx, the package the chapter says not to install (Python Package Index, 2026)', 'https://pypi.org/pypi/docx/json', False),
 ('P30', 'PyPI JSON metadata of python-docx (Python Package Index, 2026)', 'https://pypi.org/pypi/python-docx/json', False),
 ('P31', 'PyPI JSON metadata of pdfminer.six (Python Package Index, 2026)', 'https://pypi.org/pypi/pdfminer.six/json', False),
 ('P32', 'PyPI JSON metadata of pdfplumber (Python Package Index, 2026)', 'https://pypi.org/pypi/pdfplumber/json', False),
 ('P33', 'PyPI JSON metadata of reportlab (Python Package Index, 2026)', 'https://pypi.org/pypi/reportlab/json', False),
 ('P34', 'zipfile - Work with ZIP archives (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/zipfile.html', False),
 ('P35', 'os - Miscellaneous operating system interfaces, os.walk and os.listdir (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/os.html', False),
 ('P36', 'Sorting Techniques, key functions (Python 3.14 documentation)', 'https://docs.python.org/3.14/howto/sorting.html', False),
 ('P37', 'io - Core tools for working with streams, BytesIO (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/io.html', False),
 ('P38', 'PDF, Version 1.7 (ISO 32000-1:2008) (Library of Congress, Sustainability of Digital Formats, 2019)', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000277.shtml', False),
 ('P39', 'Office Open XML (OOXML) Format Family (Library of Congress, Sustainability of Digital Formats)', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000397.shtml', False),
 ('P40', 'Document management - Portable document format - Part 1: PDF 1.7, ISO 32000-1:2008 (Adobe Systems Incorporated, 2008)', 'https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/PDF32000_2008.pdf', False),
 ('P41', 'qpdf documentation, Command-Line Options (qpdf contributors, 2026)', 'https://qpdf.readthedocs.io/en/stable/cli.html', False),
 ('P42', 'LibreOffice home page (The Document Foundation)', 'https://www.libreoffice.org', False),
 ('P43', 'CWE-214: Invocation of Process Using Visible Sensitive Information (MITRE)', 'https://cwe.mitre.org/data/definitions/214.html', False),
 ('P44', 'Redaction (Wikipedia)', 'https://en.wikipedia.org/wiki/Redaction', False),
 ('P45', 'John Warnock (Wikipedia)', 'https://en.wikipedia.org/wiki/John_Warnock', False),
 ('P46', 'ZIP (file format) (Wikipedia)', 'https://en.wikipedia.org/wiki/Zip_(file_format)', False),
 ('P47', 'Office Open XML (Wikipedia)', 'https://en.wikipedia.org/wiki/Office_Open_XML', False),
 ('P48', 'Adobe Acrobat (Wikipedia)', 'https://en.wikipedia.org/wiki/Adobe_Acrobat', False),
 ('P49', 'Open XML SDK (Microsoft Learn)', 'https://learn.microsoft.com/en-us/office/open-xml/open-xml-sdk', False),
 ('P50', 'uv - an extremely fast Python package and project manager (Astral documentation)', 'https://docs.astral.sh/uv/', False),
 ('P51', 'Download Python (python.org)', 'https://www.python.org/downloads/', False),
 ('P52', 'LibreOffice Writer (The Document Foundation)', 'https://www.libreoffice.org/discover/writer/', False),
]

CONCEPTS = [('Section', 'PDF Documents'),
 ('Section', 'Word Documents'),
 ('Section', 'Summary'),
 ('Section', 'Practice Questions'),
 ('Section', 'Practice Programs'),
 ('Subsection', 'Extracting Text'),
 ('Subsection', 'Post-Processing with AI'),
 ('Subsection', 'Extracting Images'),
 ('Subsection', 'Creating PDFs from Other Pages'),
 ('Subsection', 'Rotating Pages'),
 ('Subsection', 'Inserting Blank Pages'),
 ('Subsection', 'Adding Watermarks and Overlays'),
 ('Subsection', 'Encrypting and Decrypting PDFs'),
 ('Subsection', 'Project 12: Combine Select Pages from Many PDFs'),
 ('Subsection', 'Step 1: Find All PDF Files'),
 ('Subsection', 'Step 2: Open Each PDF'),
 ('Subsection', 'Step 3: Save the Results'),
 ('Subsection', 'Ideas for Similar Programs'),
 ('Subsection', 'Reading Word Documents'),
 ('Subsection', 'Getting the Full Text from a .docx File'),
 ('Subsection', 'Styling Paragraph and Run Objects'),
 ('Subsection', 'Applying Run Attributes'),
 ('Subsection', 'Writing Word Documents'),
 ('Subsection', 'Adding Headings'),
 ('Subsection', 'Adding Line and Page Breaks'),
 ('Subsection', 'Adding Pictures'),
 ('Subsection', 'PDF Paranoia'),
 ('Subsection', 'Custom Invitations'),
 ('Subsection', 'PDF Password Breaker'),
 ('Class', 'PdfReader'),
 ('Class', 'PdfWriter'),
 ('Class', 'Page object'),
 ('Class', 'Document object'),
 ('Class', 'Paragraph object'),
 ('Class', 'Run object'),
 ('Class', 'PasswordType'),
 ('Method', 'extract_text'),
 ('Method', 'append'),
 ('Method', 'merge'),
 ('Method', 'rotate'),
 ('Method', 'add_blank_page'),
 ('Method', 'insert_blank_page'),
 ('Method', 'merge_page'),
 ('Method', 'encrypt'),
 ('Method', 'decrypt'),
 ('Method', 'add_paragraph'),
 ('Method', 'add_run'),
 ('Method', 'add_heading'),
 ('Method', 'add_break'),
 ('Method', 'add_picture'),
 ('Attribute', 'pages'),
 ('Attribute', 'images'),
 ('Attribute', 'is_encrypted'),
 ('Attribute', 'paragraphs'),
 ('Attribute', 'runs'),
 ('Attribute', 'bold'),
 ('Attribute', 'italic'),
 ('Attribute', 'underline'),
 ('Attribute', 'style'),
 ('Concept', 'PDF'),
 ('Concept', 'Word document (.docx)'),
 ('Concept', 'Paragraph style'),
 ('Concept', 'Character style'),
 ('Concept', 'Watermark'),
 ('Concept', 'Overlay'),
 ('Concept', 'User password'),
 ('Concept', 'Owner password'),
 ('Concept', 'Brute-force attack'),
 ('Concept', 'Page break'),
 ('Module', 'pypdf'),
 ('Module', 'docx'),
 ('Module', 'pdfminer.high_level'),
 ('Module', 'docx.shared'),
 ('Module', 'docx.enum.text'),
 ('Module', 'os'),
 ('Function', 'os.walk'),
 ('Function', 'os.listdir'),
 ('Method', 'sort'),
 ('Function', 'Inches'),
 ('Function', 'Cm'),
 ('Function', 'open'),
 ('Program', 'extractpdftext.py'),
 ('Program', 'extractpdfimages.py'),
 ('Program', 'combine_pdfs.py'),
 ('Program', 'readDocx.py')]

FINDINGS = [('F1',
  'Background',
  'Chapter 17 of the 3rd edition, PDF and Word Documents, teaches PDF with the PyPDF package (extract text, post-process it with a language model, extract '
  'images, copy pages into a new file, rotate pages, insert blank pages, merge a watermark or overlay, encrypt and decrypt), Project 12 that combines select '
  'pages from many PDFs, and Word with the Python-Docx package (read paragraphs and runs, get the full text, style paragraphs and runs, apply run attributes, '
  'write paragraphs, headings, line and page breaks and pictures), and it ends with 12 practice questions and three practice programs, PDF Paranoia, Custom '
  'Invitations and PDF Password Breaker. The chapter page of 2026-10-12 is 100,057 bytes with 32 listings (19 of them interactive sessions of 91 statements), '
  "10 captioned figures and 1 table, and its sha256, 00cb1643dca3afd3b75bfd9ce7ad594f3dd80f8606de1cffe40b8583846b4789, equals the chapterDigest of the book's "
  'own chapter ontology [P01] [P03] [P04].',
  ['P01', 'P03', 'P04']),
 ('F2',
  'Comparative analysis',
  "The chapter's interactive sessions were replayed statement by statement, in order, on the files the book ships under Python 3.14.6 with pypdf 6.20.1 and "
  'python-docx 1.2.0: of 91 statements 89 printed what the page prints and 2 differ, both in the same place, the third run of the demo paragraph, which the '
  "page prints as ' and some ' and which is ' text and some ' in the shipped demo.docx. Under the versions Appendix A pins, pypdf 5.0.1 and python-docx 1.1.2, "
  "88 match and 3 differ: the same two and writer.merge(2, 'Recursion_Chapter1.pdf', (0, 5)), which raises AttributeError: 'tuple' object has no attribute "
  "'startswith'. The agreement is smaller than it looks: a statement that prints nothing cannot differ from the page, so the next finding concerns one that "
  'matches and still goes wrong [P01] [P02] [P05] [P06] [P19].',
  ['P01', 'P02', 'P05', 'P06', 'P19']),
 ('F3',
  'Comparative analysis',
  "The chapter's merge() example, writer.merge(2, 'Recursion_Chapter1.pdf', (0, 5)), prints nothing and so matches the page under pypdf 6.20.1, but it does "
  'not do what the chapter says: the tuple lands in the third parameter, outline_item, so the library made a bookmark titled (0, 5) and inserted the whole '
  '18-page file, and a writer of 5 pages ended with 23, identically on ten interpreters (3.11 to 3.14.6). With pages=(0, 5) the same call inserted 5 pages. '
  'append() accepts the tuple in its second place because the signature types its outline_item parameter as a title or a page range, and the signature of '
  'merge() types it as a title only. pypdf 5.0.1 raises AttributeError for the same line [P01] [P10] [P14] [P16].',
  ['P01', 'P10', 'P14', 'P16']),
 ('F4',
  'Comparative analysis',
  "Project 12 as printed does not run: the loop appends to pdf_files, a name never defined, and Python 3.14.6 answers NameError: name 'pdf_files' is not "
  "defined, suggesting pdf_filenames. The shipped combine_pdfs.py is not the finished program either: it stops at NameError: name 'PdfWriter' is not defined, "
  'because it writes PdfWriter without the pypdf prefix, and it also names pdf_files in its loop. With the name corrected the program combined three small '
  'files into combined.pdf of 5 pages (every page but the first of each), and a second run read combined.pdf as one of its own inputs and wrote 9 pages, which '
  "the program does not guard against. The test filename.endswith('.pdf') also misses a file named with capital letters [P01] [P02] [P35].",
  ['P01', 'P02', 'P35']),
 ('F5',
  'Comparative analysis',
  "The book's two shipped scripts for text and images are the listings of the chapter, with Windows line endings: extractpdftext.py and extractpdfimages.py "
  'equal the printed text. Run on the shipped Recursion_Chapter1.pdf the text script wrote 32,981 characters in 688 lines and 5,363 words, with 11 warnings on '
  'the error stream that name fontTools, and the page texts are joined with no separator (page 1 ends with the words Al Sweigart and page 2 begins with 2 and '
  'Chapter 1, which run together as Al Sweigart2). The image script wrote 11 files of 2,099,648 bytes under the newest releases and 2,074,308 under the pinned '
  'ones, 7 images from page 1; the sample output the chapter prints says page 7 was skipped with not enough image data, and neither environment skipped it: '
  'both wrote 10_page7_Im0.tif. The zip does not hold encrypted.pdf, helloworld.docx or restyled.docx, which the chapter names as files the reader makes [P01] '
  '[P02] [P07] [P09].',
  ['P01', 'P02', 'P07', 'P09']),
 ('F6',
  'Comparative analysis',
  'Several statements about Word documents differ from the current package. The chapter prints a list of default style names (34 of them); a new document has '
  "164 styles of four kinds (27 character, 1 list, 36 paragraph, 100 table), 'List Number ' with the trailing space the page prints raises KeyError, and "
  'MacroText is the id of a style named macro, which works only through a deprecated lookup by id that warns. A paragraph accepts only paragraph styles and a '
  "run only character styles: assigning 'Quote Char' to a paragraph or 'Quote' to a run raises ValueError. The paragraph list of a document does not include "
  'text in tables or headers, and text inside a hyperlink is in paragraph.text but in no run. The text script shipped as readDocx.py joins paragraphs with a '
  'blank line, so the output differs from the six lines the page prints [P01] [P02] [P20] [P21] [P22] [P24].',
  ['P01', 'P02', 'P20', 'P21', 'P22', 'P24']),
 ('F7',
  'Comparative analysis',
  'Table 17-1 lists twelve text attributes as attributes of a Run, and only three are: bold, italic and underline; strike, double_strike, all_caps, '
  'small_caps, shadow, outline, rtl, imprint and emboss exist on run.font. Assigning run.strike = True raises nothing and changes nothing (font.strike stayed '
  "None, no element in the XML), so the chapter's table sends a reader to a silent failure. The tri-state values are as the chapter says: None writes nothing, "
  'True writes <w:b/>, False writes <w:b w:val=0/>. The heading levels are given as 0 to 4 in one sentence and 1 to 9 in the next, and add_heading accepts 0 '
  'to 9 and raises ValueError outside it, which is also the answer to practice question 12 [P01] [P23] [P24].',
  ['P01', 'P23', 'P24']),
 ('F8',
  'Comparative analysis',
  'Two optional dependencies and a default that the chapter does not mention matter in practice. page.images needs the Pillow package and raises ImportError '
  'without it. AES needs the cryptography package: without it AES-128 fails later, at write(), and AES-256 fails at encrypt(), both with DependencyError. '
  "encrypt() without an algorithm wrote RC4 with a 128-bit key (V 2, R 3), and algorithm='AES-256' wrote V 5, R 6 with qpdf reporting AESv3; the chapter shows "
  "only the AES-256 form. The chapter's text names neither Pillow nor cryptography, and the versions the book pins are given only in Appendix A, pypdf 5.0.1 "
  'and python-docx 1.1.2 [P01] [P05] [P09] [P11] [P13] [P41].',
  ['P01', 'P05', 'P09', 'P11', 'P13', 'P41']),
 ('F9',
  'Comparative analysis',
  "Text extraction is weaker than the chapter's tone suggests and the gap is documented: a PDF stores drawing commands, so the text comes out in stream order "
  '(worldHello for a page that shows Hello world), a black rectangle drawn over text leaves the text in the file, and a scanned page returned the empty string '
  "with one image. pypdf documents post-processing as outside its scope. On the sample chapter pdfminer.six returned 33,200 characters against pypdf's 32,981, "
  'put a form feed after every page and spaced out the chapter heading (W H A T), and of eleven damaged files none was read by pdfminer.six and refused by '
  "pypdf, so the fallback the chapter's listing offers was not needed in any of them [P07] [P08] [P27] [P40] [P44].",
  ['P07', 'P08', 'P27', 'P40', 'P44']),
 ('F10',
  'Comparative analysis',
  'The first practice program, PDF Paranoia, takes its password from the command line, where any program that lists processes can read it (CWE-214), and '
  'deletes each original after a test decryption; written as the chapter asks, it encrypted the PDFs of a small folder tree with AES-256, removed the '
  'originals, skipped an already encrypted file, and decrypted with a wrong password without stopping. A filter on the lower-case extension .pdf misses C.PDF. '
  'The second practice program, Custom Invitations, needs styles that exist in the template; the study made them in code with styles.add_style, and a page '
  'break after every guest left no blank last page in LibreOffice 24.2, which counted 5 pages for 5 guests [P01] [P22] [P43] [P52].',
  ['P01', 'P22', 'P43', 'P52']),
 ('F11',
  'Comparative analysis',
  "The worst case of the PDF Password Breaker, run to the end on a file written by pypdf 6.20.1 with the book's dictionary.txt (349,900 words, both cases of "
  'each, so 699,800 attempts) and a password that is not in the list, found nothing and took 241.7 seconds for RC4, the default of encrypt(), and 1467.5 '
  'seconds for AES-256, the two runs started together on a machine with two cores. The page speaks of 88,000 attempts; the shipped file gives 699,800 (8.0 '
  "times the 44,000 words on the page), and a stronger algorithm costs about six times as much per guess, so the chapter's remark that a long random password "
  'defeats the program is shown by the timing, not only stated. Python 3.14.6.',
  ['P01', 'P11', 'P13']),
 ('F12',
  'Contemporary developments',
  "The packages have moved on since the chapter's examples. The pypdf documentation tells that pyPdf (2005, Mathieu Fenniak) was forked as PyPDF2 at the end "
  'of 2011, that Martin Thoma took over PyPDF2 in April 2022 and that it was merged back into pypdf; PdfMerger, which older tutorials use, was removed in '
  'pypdf 5.0.0 (in 5.0.1 the name exists and raises DeprecationError, in 6.20.1 it is gone), and PdfFileReader and PdfFileWriter are not names of pypdf 6.20.1 '
  'either. Appendix A pins pypdf 5.0.1 and python-docx 1.1.2 while PyPI offers pypdf 6.20.1 and python-docx 1.2.0; an attempt to install Pillow 10.4.0 for the '
  'pinned environment found no wheel for Python 3.14 and the build failed for lack of libjpeg headers, so that environment used the newest Pillow. The package '
  'docx, which the chapter warns against, is at 0.2.4 from 6 February 2014 and its import fails under Python 3.14.6 with ModuleNotFoundError: No module named '
  "'exceptions' [P05] [P16] [P17] [P28] [P29] [P30].",
  ['P05', 'P16', 'P17', 'P28', 'P29', 'P30']),
 ('F13',
  'Comparative analysis',
  'One program that exercises both packages was run under ten interpreters installed with uv: 3.11.17, 3.12.3, 3.13.16 and the seven releases 3.14.0 to '
  '3.14.6, with the same pypdf, python-docx and pdfminer.six. Eleven results were equal in all ten: the page count (18), the images per page, the hash of the '
  'text from pypdf and from pdfminer.six, every pypdf operation (append (0, 5) gave 5 pages, (0, 5, 2) gave 3, [0, 5] gave 2, merge with pages=(0, 2) gave 4, '
  'rotation 90, encrypted file V 5 R 6), the python-docx operations, the silent ignoring of run.strike, the warning for the style id and the 23 pages of the '
  "chapter's merge line. The only difference was the build of the cryptography wheel on 3.13 (50.0.1 against 50.0.2). The chapter's PDF and Word behaviour "
  'does not depend on the 3.x release [P06] [P19] [P27] [P50].',
  ['P06', 'P19', 'P27', 'P50']),
 ('F14',
  'Comparative analysis',
  "A PDF or Word file made by the chapter's listings opens elsewhere: LibreOffice 24.2 converted the seven Word files the study wrote (hello world, multiple "
  'paragraphs, headings, two pages, a picture, the restyled file and demo.docx) to PDF, counted 2 pages for the file with the page break and 1 for the others, '
  'and showed the text; qpdf --check accepted the PDF written by hand and by pypdf, and pdftotext without the password refused the encrypted file and read it '
  'with it. Microsoft Word itself, a PDF viewer and the language model clean-up of the section Post-Processing with AI were NOT EXECUTED, and the statement '
  'that the style names in the Styles pane of Word match the list the chapter prints is therefore checked only against the template of python-docx [P01] [P41] '
  '[P42] [P52].',
  ['P01', 'P41', 'P42', 'P52']),
 ('F15',
  'Conclusion',
  'For an advanced course, chapter 17 is best taught as a limit on what can be automated: a PDF is a page description made for display and a .docx is a zip of '
  'XML parts, so a program can copy, reorder, rotate, stamp, encrypt, read the paragraphs and runs of and write a new document, and cannot recover structure '
  'that was never stored. The sections to correct are few and exact: pass pages= to merge(), rename pdf_files in Project 12 and guard against reading its own '
  'output, take heading levels as 0 to 9, set run attributes through run.font, use the style names the template has (no trailing space, no MacroText), name '
  'Pillow and cryptography, and keep the password of PDF Paranoia out of the command line. The sections to add are the file formats themselves, redaction that '
  'does not remove text, scanned pages, and the size of a brute-force attack. The 91 statements, the 12 corpus programs and the 70 examples of this study are '
  'the evidence [P01] [P06] [P19] [P40] [P43] [P44].',
  ['P01', 'P06', 'P19', 'P40', 'P43', 'P44'])]


def X(code):
    """An executable example as one expression with no double quote and no line break: the code runs in a fresh
    namespace and the value of its variable out is the result."""
    lit = "'" + code.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace('"', "\\x22") + "'"
    return "(lambda g: (exec(%s, g), g['out'])[1])({})" % lit

# The helpers every example starts from: a small valid PDF of text pages written byte by byte (mk), a reader over bytes (rd),
# a six-page file (six), the texts of a written file (txts) and a PNG made without a library (png).
_PRE = "import io, os, re, sys, zipfile, zlib, struct, tempfile, warnings\nimport pypdf\ndef mk(*t):\n    o = ['<</Type/Catalog/Pages 2 0 R>>', None, '<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>']; k = []\n    for s in t:\n        n = len(o) + 1; k.append(n); c = s if s.startswith('BT') else 'BT /F1 18 Tf 72 720 Td (%s) Tj ET' % s\n        o.append('<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Resources<</Font<</F1 3 0 R>>>>/Contents %d 0 R>>' % (n + 1)); o.append('<</Length %d>>\\nstream\\n%s\\nendstream' % (len(c), c))\n    o[1] = '<</Type/Pages/Kids[%s]/Count %d>>' % (' '.join('%d 0 R' % i for i in k), len(k))\n    b = b'%PDF-1.4\\n'; f = []\n    for i, s in enumerate(o, 1): f.append(len(b)); b += ('%d 0 obj\\n%s\\nendobj\\n' % (i, s)).encode()\n    x = len(b); b += ('xref\\n0 %d\\n0000000000 65535 f \\n' % (len(o) + 1)).encode() + ''.join('%010d 00000 n \\n' % i for i in f).encode()\n    return b + ('trailer\\n<</Size %d/Root 1 0 R>>\\nstartxref\\n%d\\n%%%%EOF\\n' % (len(o) + 1, x)).encode()\ndef rd(b, pw=None):\n    r = pypdf.PdfReader(io.BytesIO(b))\n    if pw is not None: r.decrypt(pw)\n    return r\ndef six():\n    return mk(*['Page %d' % i for i in range(1, 7)])\ndef txts(w):\n    b = io.BytesIO(); w.write(b); return [p.extract_text() for p in pypdf.PdfReader(b).pages]\ndef png(w, h):\n    raw = b''.join(b'\\x00' + b'\\xff\\x00\\x00' * w for _ in range(h))\n    ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d))\n    return b'\\x89PNG\\r\\n\\x1a\\n' + ch(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw)) + ch(b'IEND', b'')\n"

def XC(body):
    """like X, for an example that must run with the cryptography package made unavailable: it runs in a child interpreter"""
    child = "import sys\nsys.modules['cryptography'] = None\n" + _PRE + body
    return X("import subprocess, sys\nsrc = %r\nr = subprocess.run([sys.executable, '-c', src + '\\nprint(repr(out))'], capture_output=True, text=True)\nout = eval(r.stdout) if r.returncode == 0 else r.stderr.strip().splitlines()[-1]" % child)


# (top, mid, leaf, exemplar, definition, (the example as an expression, its result))
TAX = [
 ('PdfFormat', 'FileStructure', 'HeaderAndTrailer', '%PDF-1.4 ... startxref 621 %%EOF',
  'A PDF file starts with a header line, here %PDF-1.4, and ends with the word startxref, a byte offset and %%EOF; in a two-page file written for the study the offset pointed at the bytes xref and the last line was %%EOF, so a reader finds the table by reading from the end.',
  (X(_PRE + "b = mk('Page one', 'Page two')\nsx = int(re.search(rb'startxref\\n(\\d+)', b).group(1))\nout = (b[:8], b.rstrip().endswith(b'%%EOF'), b[sx:sx + 4], len(b) > sx)"), "(b'%PDF-1.4', True, b'xref', True)")),
 ('PdfFormat', 'FileStructure', 'CrossReferenceTable', 'xref 0 8 / 0000000015 00000 n',
  'The cross-reference table lists the byte offset of every numbered object: the table of the two-page file had 8 entries, the first (object 0) free, and the offsets of the first three used entries pointed at the text 1 0 obj, 2 0 obj and 3 0 obj.',
  (X(_PRE + "b = mk('Page one', 'Page two')\nsx = int(re.search(rb'startxref\\n(\\d+)', b).group(1))\nrows = re.findall(rb'(\\d{10}) (\\d{5}) ([nf]) \\n', b[sx:])\noffs = [int(o) for o, g, t in rows if t == b'n']\nout = (len(rows), [b[o:o + 7] for o in offs[:3]], rows[0][2])"), "(8, [b'1 0 obj', b'2 0 obj', b'3 0 obj'], b'f')")),
 ('PdfFormat', 'FileStructure', 'ContentStreamText', 'BT /F1 18 Tf 72 720 Td (Page one) Tj ET',
  'The visible words of a page are drawing commands in a content stream, BT /F1 18 Tf 72 720 Td (Page one) Tj ET, and get_contents().get_data() on the page returned those same bytes; text in a PDF is placed on the page and is not stored as paragraphs.',
  (X(_PRE + "b = mk('Page one')\nout = (re.findall(rb'BT .*? ET', b), rd(b).pages[0].get_contents().get_data())"), "([b'BT /F1 18 Tf 72 720 Td (Page one) Tj ET'], b'BT /F1 18 Tf 72 720 Td (Page one) Tj ET')")),
 ('PdfFormat', 'FileStructure', 'ProducerMetadata', 'writer.write(f)  # /Producer /pypdf',
  "A hand-made file had no metadata (None); after pypdf copied it into a PdfWriter and wrote it, the document information held {'/Producer': 'pypdf'}, so a file saved by the library names the library as its producer.",
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x')))\nb = io.BytesIO(); w.write(b)\nout = (dict(pypdf.PdfReader(b).metadata), rd(mk('x')).metadata)"), "({'/Producer': 'pypdf'}, None)")),
 ('PdfFormat', 'TextAndLayout', 'TextOrderIsStreamOrder', '(world) Tj ... (Hello) Tj',
  "Text comes out in the order of the drawing commands in the stream, not in the order of the page: with (world) drawn first at x 200 and (Hello) drawn second at x 72, extract_text() returned worldHello, while extraction_mode='layout' returned Hello and world on one line with a gap between them.",
  (X(_PRE + "c = 'BT /F1 12 Tf 200 700 Td (world) Tj ET BT /F1 12 Tf 72 700 Td (Hello) Tj ET'\nt = rd(mk(c)).pages[0].extract_text()\nout = (t, rd(mk(c)).pages[0].extract_text(extraction_mode='layout').strip())"), "('worldHello', 'Hello                       world')")),
 ('PdfFormat', 'TextAndLayout', 'ScannedPageNoText', "Image.save(..., 'PDF')",
  'A page that is only a picture has no text to extract: a file made from a 40 by 40 pixel image had 1 page, extract_text() returned the empty string and the page held one image named image.jpg, which is what a scanned document looks like to the library.',
  (X(_PRE + "from PIL import Image\nbuf = io.BytesIO(); Image.new('RGB', (40, 40), 'white').save(buf, 'PDF')\nr = rd(buf.getvalue())\nout = (len(r.pages), r.pages[0].extract_text(), [i.name for i in r.pages[0].images])"), "(1, '', ['image.jpg'])")),
 ('PdfFormat', 'TextAndLayout', 'RedactionByOverlay', '0 0 0 rg 60 700 200 30 re f',
  "A black rectangle drawn over text hides it from the eye and not from a program: with '0 0 0 rg 60 710 300 30 re f' drawn after the line, extract_text() still returned Salary: 120000 USD and the stream still held the drawing command.",
  (X(_PRE + "c = 'BT /F1 18 Tf 72 720 Td (Salary: 120000 USD) Tj ET 0 0 0 rg 60 710 300 30 re f'\nr = rd(mk(c))\nout = (r.pages[0].extract_text(), b' re f' in r.pages[0].get_contents().get_data())"), "('Salary: 120000 USD', True)")),
 ('PdfFormat', 'TextAndLayout', 'NoParagraphsInPdf', '(Hello) Tj (world) Tj',
  "A PDF has no paragraphs: two separate drawing commands one row apart extracted as Hello and world with a newline between them, while the same words drawn by one command extracted as Hello world, so the line breaks of extracted text come from positions and not from the author's structure.",
  (X(_PRE + "c = 'BT /F1 12 Tf 72 700 Td (Hello) Tj ET BT /F1 12 Tf 72 686 Td (world) Tj ET'\nout = (rd(mk(c)).pages[0].extract_text(), rd(mk('Hello world')).pages[0].extract_text())"), "('Hello\\nworld', 'Hello world')")),
 ('PdfTextAndImages', 'ReadingPages', 'PdfReaderPages', 'len(reader.pages)',
  "reader.pages behaves like a list of page objects: for a six-page file len() was 6, the type is the library's own _VirtualList, the index -1 reached the last page ('Page 6') and the slice [1:3] gave the second and third pages.",
  (X(_PRE + 'r = rd(six())\nout = (len(r.pages), type(r.pages).__name__, r.pages[-1].extract_text(), [p.extract_text() for p in r.pages[1:3]])'), "(6, '_VirtualList', 'Page 6', ['Page 2', 'Page 3'])")),
 ('PdfTextAndImages', 'ReadingPages', 'PageIndexIsZeroBased', 'reader.pages[4]',
  "The first page is pages[0], so pages[4] is the fifth page ('Page 5'), and an index past the end raises IndexError with the message Sequence index out of range.",
  (X(_PRE + 'r = rd(six())\ntry:\n    r.pages[6]\n    e = None\nexcept IndexError as x:\n    e = str(x)\nout = (r.pages[4].extract_text(), e)'), "('Page 5', 'Sequence index out of range')")),
 ('PdfTextAndImages', 'ReadingPages', 'JoinedPagesNoSeparator', 'text += page.extract_text()',
  "Adding each page's text to one string with += joins the pages with nothing between them, giving Page 1Page 2Page 3Page 4Page 5Page 6, and the last word of a page runs into the first of the next; joining with a newline keeps them apart.",
  (X(_PRE + "r = rd(six()); text = ''\nfor p in r.pages: text += p.extract_text()\nout = (text, '\\n'.join(p.extract_text() for p in r.pages[:2]))"), "('Page 1Page 2Page 3Page 4Page 5Page 6', 'Page 1\\nPage 2')")),
 ('PdfTextAndImages', 'ExtractionQuality', 'LayoutMode', "page.extract_text(extraction_mode='layout')",
  "The default extraction joins the words of a row with single spaces (Name Price and Tea 3), and extraction_mode='layout' keeps the horizontal gap between columns with runs of spaces, so a table-like page can be read column by column.",
  (X(_PRE + "c = 'BT /F1 12 Tf 72 700 Td (Name) Tj 200 0 Td (Price) Tj ET BT /F1 12 Tf 72 686 Td (Tea) Tj 200 0 Td (3) Tj ET'\np = rd(mk(c)).pages[0]\nout = (p.extract_text(), p.extract_text(extraction_mode='layout').strip().split('\\n'))"), "('Name Price\\nTea 3', ['Name                                                  Price', 'Tea                                                      3'])")),
 ('PdfTextAndImages', 'ExtractionQuality', 'PdfminerAlternative', 'pdfminer.high_level.extract_text(PDF_FILENAME)',
  "pdfminer.six reads the same six-page file through extract_text(), which ends every page with a form feed character (6 in all, after blank lines), where pypdf returned the pages' texts without any separator.",
  (X(_PRE + "from pdfminer.high_level import extract_text\nb = six()\nout = (extract_text(io.BytesIO(b))[:22], extract_text(io.BytesIO(b)).count('\\x0c'), ''.join(p.extract_text() for p in rd(b).pages)[:14])"), "('Page 1\\n\\n\\x0cPage 2\\n\\n\\x0cPage', 6, 'Page 1Page 2Pa')")),
 ('PdfTextAndImages', 'ExtractionQuality', 'DamagedInput', 'PdfReader(truncated)',
  "Damaged files fail in the library's own way: a file cut off before its xref table raised PdfStreamError in pypdf and PDFSyntaxError in pdfminer.six, and an empty file raised EmptyFileError in pypdf, so a program that falls back from one library to the other must catch more than one exception class.",
  (X(_PRE + "from pdfminer.high_level import extract_text\nb = six(); cut = b[:b.index(b'xref')]\nres = []\nfor f in (lambda: pypdf.PdfReader(io.BytesIO(cut)), lambda: extract_text(io.BytesIO(cut)), lambda: pypdf.PdfReader(io.BytesIO(b''))):\n    try:\n        f(); res.append('ok')\n    except Exception as e:\n        res.append(type(e).__name__)\nout = res"), "['PdfStreamError', 'PDFSyntaxError', 'EmptyFileError']")),
 ('PdfTextAndImages', 'ExtractionQuality', 'TextPostProcessing', 'follow-\\ning the execution',
  "Extracted text keeps the hyphens and row breaks of the printed page: follow- at the end of one row and ing the execution on the next came out with a newline between them, and re.sub of a hyphen followed by a newline joined them to following the execution; cleaning the text is the program's job.",
  (X(_PRE + "c = 'BT /F1 12 Tf 72 700 Td (follow-) Tj ET BT /F1 12 Tf 72 686 Td (ing the execution) Tj ET'\nt = rd(mk(c)).pages[0].extract_text()\nout = (t, re.sub(r'-\\n', '', t))"), "('follow-\\ning the execution', 'following the execution')")),
 ('PdfTextAndImages', 'ImageExtraction', 'ImagesNeedPillow', 'page.images',
  "page.images needs the Pillow package: with Pillow made unavailable, reading the images raised ImportError, 'pillow is required to do image extraction', and the chapter does not name Pillow at all.",
  (X(_PRE + "from PIL import Image\nbuf = io.BytesIO(); Image.new('RGB', (30, 30), 'red').save(buf, 'PDF'); b = buf.getvalue()\nsys.modules['PIL'] = None\ntry:\n    rd(b).pages[0].images[0]\n    out = 'no error'\nexcept ImportError as e:\n    out = (type(e).__name__, str(e)[:48])"), "('ImportError', 'pillow is required to do image extraction. It ca')")),
 ('PdfTextAndImages', 'ImageExtraction', 'ImageNameAndData', 'image.name, image.data',
  'Each image object has a name and the bytes of the image file: the picture on the scanned page was named image.jpg, its data began with the JPEG marker FF D8, and .image gave a Pillow JpegImageFile of 30 by 30 pixels.',
  (X(_PRE + "from PIL import Image\nbuf = io.BytesIO(); Image.new('RGB', (30, 30), 'red').save(buf, 'PDF')\nim = rd(buf.getvalue()).pages[0].images[0]\nout = (im.name, im.data[:2], len(im.data) > 100, type(im.image).__name__, im.image.size)"), "('image.jpg', b'\\xff\\xd8', True, 'JpegImageFile', (30, 30))")),
 ('PdfTextAndImages', 'ImageExtraction', 'ImageNamesRepeat', "f'{counter}_page{n}_{image.name}'",
  "Image names are only unique within a page: two pages carrying the same picture both listed image.jpg, which is why the chapter's listing puts a counter and the page number in front of the name it writes.",
  (X(_PRE + "from PIL import Image\nbuf = io.BytesIO(); Image.new('RGB', (30, 30), 'red').save(buf, 'PDF'); b = buf.getvalue()\nw = pypdf.PdfWriter(); w.append(io.BytesIO(b)); w.append(io.BytesIO(b))\no = io.BytesIO(); w.write(o)\nout = [[i.name for i in p.images] for p in pypdf.PdfReader(o).pages]"), "[['image.jpg'], ['image.jpg']]")),
 ('PdfWriting', 'PageSelection', 'PdfWriterStartsEmpty', 'writer = pypdf.PdfWriter()',
  'A PdfWriter starts with no pages (0) and only receives pages from other files: after append() of a six-page file it held 6.',
  (X(_PRE + 'w = pypdf.PdfWriter()\nn0 = len(w.pages)\nw.append(io.BytesIO(six()))\nout = (n0, len(w.pages))'), '(0, 6)')),
 ('PdfWriting', 'PageSelection', 'AppendRangeTuple', 'writer.append(file, (0, 5))',
  "A tuple of two numbers selects pages the way range() does: append(file, (0, 5)) copied Page 1 to Page 5 and not the sixth, which is why the chapter's first-five-pages example works.",
  (X(_PRE + 'w = pypdf.PdfWriter(); w.append(io.BytesIO(six()), (0, 5))\nout = txts(w)'), "['Page 1', 'Page 2', 'Page 3', 'Page 4', 'Page 5']")),
 ('PdfWriting', 'PageSelection', 'AppendStepTuple', 'writer.append(file, (0, 5, 2))',
  'A tuple of three numbers adds a step: (0, 5, 2) copied Page 1, Page 3 and Page 5.',
  (X(_PRE + 'w = pypdf.PdfWriter(); w.append(io.BytesIO(six()), (0, 5, 2))\nout = txts(w)'), "['Page 1', 'Page 3', 'Page 5']")),
 ('PdfWriting', 'PageSelection', 'AppendListOfPages', 'writer.append(file, [0, 5])',
  'A list names pages exactly: [0, 5] copied Page 1 and Page 6, two pages, where the tuple (0, 5) copies five.',
  (X(_PRE + 'w = pypdf.PdfWriter(); w.append(io.BytesIO(six()), [0, 5])\nout = txts(w)'), "['Page 1', 'Page 6']")),
 ('PdfWriting', 'PageSelection', 'AppendOutOfRange', 'writer.append(file, (0, 99))',
  'A page number past the end of the file raises IndexError, Sequence index out of range, for the tuple (0, 99) and for the list [0, 99] alike.',
  (X(_PRE + 'res = []\nfor pg in ((0, 99), [0, 99]):\n    w = pypdf.PdfWriter()\n    try:\n        w.append(io.BytesIO(six()), pg); res.append(len(w.pages))\n    except Exception as e:\n        res.append((type(e).__name__, str(e)))\nout = res'), "[('IndexError', 'Sequence index out of range'), ('IndexError', 'Sequence index out of range')]")),
 ('PdfWriting', 'InsertAndMerge', 'MergeInsertsAtPosition', 'writer.merge(1, file, pages=(0, 2))',
  'merge() takes the position first and puts the copied pages there: merging pages (0, 2) of the six-page file at position 1 of a three-page writer gave A1, Page 1, Page 2, A2, A3.',
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('A1', 'A2', 'A3')))\nw.merge(1, io.BytesIO(six()), pages=(0, 2))\nout = txts(w)"), "['A1', 'Page 1', 'Page 2', 'A2', 'A3']")),
 ('PdfWriting', 'InsertAndMerge', 'MergePositionalTupleTrap', 'writer.merge(2, file, (0, 5))',
  'Written as the chapter writes it, merge(1, file, (0, 2)), the tuple lands in the parameter outline_item and not in pages: pypdf 6.20.1 made a bookmark titled (0, 2) and inserted the whole six-page file, so the writer ended with 9 pages and not 5; the parameters are self, position, fileobj, outline_item and pages, and pypdf 5.0.1 raises AttributeError instead.',
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('A1', 'A2', 'A3')))\nw.merge(1, io.BytesIO(six()), (0, 2))\nimport inspect\nout = (len(w.pages), [o['/Title'] for o in w.outline], list(inspect.signature(pypdf.PdfWriter.merge).parameters)[:5])"), "(9, ['(0, 2)'], ['self', 'position', 'fileobj', 'outline_item', 'pages'])")),
 ('PdfWriting', 'InsertAndMerge', 'BlankPageSize', 'writer.add_blank_page()',
  "A new blank page takes its size from a page already in the writer: add_blank_page() after a 200 by 200 page made another 200 by 200 page, and insert_blank_page(index=1) between a 300 by 400 page and a 100 by 100 page took 100 by 100, the size of the page that follows it, and not the 300 by 400 of the page before it that the chapter's words suggest.",
  (X(_PRE + 'w = pypdf.PdfWriter()\nw.add_blank_page(width=300, height=400)\nw.add_blank_page(width=100, height=100)\nw.add_blank_page(width=200, height=200)\nw.add_blank_page()\nw.insert_blank_page(index=1)\nout = [(float(p.mediabox.width), float(p.mediabox.height)) for p in w.pages]'), '[(300.0, 400.0), (100.0, 100.0), (100.0, 100.0), (200.0, 200.0), (200.0, 200.0)]')),
 ('PdfWriting', 'InsertAndMerge', 'InsertBlankPageArguments', 'writer.insert_blank_page(2)',
  'insert_blank_page takes width, height and index in that order, so a single positional number is the width: insert_blank_page(2) made a page 2 points wide, while index=2 made a page of the normal 612 points, and the writer grew from 6 to 8 pages.',
  (X(_PRE + 'import inspect\nw = pypdf.PdfWriter(); w.append(io.BytesIO(six()))\np = w.insert_blank_page(2)\nq = w.insert_blank_page(index=2)\nout = (list(inspect.signature(pypdf.PdfWriter.insert_blank_page).parameters), float(p.mediabox.width), float(q.mediabox.width), len(w.pages))'), "(['self', 'width', 'height', 'index'], 2.0, 612.0, 8)")),
 ('PdfWriting', 'PageEditing', 'RotateMultiplesOf90', 'page.rotate(90)',
  'rotate() takes a multiple of 90, changes the page in place, returns the page and stores the angle (90); rotate(45) raised ValueError, Rotation angle must be a multiple of 90.',
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x')))\np = w.pages[0]; r = p.rotate(90)\ntry:\n    p.rotate(45); e = None\nexcept ValueError as x:\n    e = str(x)\nout = (type(r).__name__, p.rotation, e)"), "('PageObject', 90, 'Rotation angle must be a multiple of 90')")),
 ('PdfWriting', 'PageEditing', 'RotationAccumulates', 'page.rotate(90); page.rotate(270)',
  'Rotations add up and the sum is not reduced to a turn: rotate(90), rotate(270), rotate(-90) and rotate(180) left the rotations 90, 360, 270 and 450, and a negative angle is stored as given.',
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x')))\np = w.pages[0]; seen = []\nfor a in (90, 270, -90, 180):\n    p.rotate(a); seen.append(p.rotation)\nout = seen"), '[90, 360, 270, 450]')),
 ('PdfWriting', 'PageEditing', 'WatermarkUnderlay', 'page.merge_page(watermark, over=False)',
  "merge_page(watermark, over=False) puts the watermark's drawing commands before the page's own, MARK then BASE, so it lies under the text, and the default over=True puts them after, BASE then MARK.",
  (X(_PRE + "def order(over):\n    base = pypdf.PdfReader(io.BytesIO(mk('BASE'))).pages[0]; wm = pypdf.PdfReader(io.BytesIO(mk('MARK'))).pages[0]\n    base.merge_page(wm, over=over)\n    return re.findall(rb'\\((\\w+)\\) Tj', base.get_contents().get_data())\nout = (order(False), order(True))"), "([b'MARK', b'BASE'], [b'BASE', b'MARK'])")),
 ('PdfWriting', 'PageEditing', 'MergePageInPlace', 'base.merge_page(watermark)',
  "merge_page() changes the page it is called on and returns None; the merged page's text came out as BASEMARK.",
  (X(_PRE + "base = pypdf.PdfReader(io.BytesIO(mk('BASE'))).pages[0]; wm = pypdf.PdfReader(io.BytesIO(mk('MARK'))).pages[0]\nr = base.merge_page(wm)\nout = (r, base.extract_text())"), "(None, 'BASEMARK')")),
 ('PdfWriting', 'Protection', 'EncryptRc4Default', "writer.encrypt('swordfish')",
  "encrypt('swordfish') without an algorithm wrote RC4 with a 128-bit key: encryption version V 2, revision R 3, Length 128 and no crypt filter dictionary.",
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x'))); w.encrypt('swordfish')\nb = io.BytesIO(); w.write(b); e = pypdf.PdfReader(b).trailer['/Encrypt']\nout = (e['/V'], e['/R'], e['/Length'], e.get('/CF'))"), '(2, 3, 128, None)')),
 ('PdfWriting', 'Protection', 'EncryptAes256', "writer.encrypt('swordfish', algorithm='AES-256')",
  "encrypt('swordfish', algorithm='AES-256') wrote V 5, R 6, Length 256 and the crypt filter method /AESV3, which is what the chapter recommends and the only form it shows.",
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x'))); w.encrypt('swordfish', algorithm='AES-256')\nb = io.BytesIO(); w.write(b); e = pypdf.PdfReader(b).trailer['/Encrypt']\nout = (e['/V'], e['/R'], e['/Length'], str(e['/CF']['/StdCF']['/CFM']))"), "(5, 6, 256, '/AESV3')")),
 ('PdfWriting', 'Protection', 'DecryptReturnValues', "reader.decrypt('swordfish')",
  'decrypt() returns a PasswordType whose name says which password matched: USER_PASSWORD for userpw, OWNER_PASSWORD for ownerpw and NOT_DECRYPTED for a wrong, empty or differently capitalised password; it raises nothing for a wrong one.',
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x'))); w.encrypt('userpw', owner_password='ownerpw', algorithm='AES-256')\nb = io.BytesIO(); w.write(b); b = b.getvalue()\nout = [(p, pypdf.PdfReader(io.BytesIO(b)).decrypt(p).name) for p in ('userpw', 'ownerpw', 'swordfish', '', 'USERPW')]"), "[('userpw', 'USER_PASSWORD'), ('ownerpw', 'OWNER_PASSWORD'), ('swordfish', 'NOT_DECRYPTED'), ('', 'NOT_DECRYPTED'), ('USERPW', 'NOT_DECRYPTED')]")),
 ('PdfWriting', 'Protection', 'ReaderRefusesBeforeDecrypt', 'reader.pages[0] before decrypt()',
  "For an encrypted file is_encrypted is True and pages[0] raises FileNotDecryptedError, File has not been decrypted; after decrypt('pw') returned OWNER_PASSWORD (encrypt('pw') sets one password for both roles) the page text was Secret.",
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('Secret'))); w.encrypt('pw')\nb = io.BytesIO(); w.write(b)\nr = pypdf.PdfReader(b)\ntry:\n    r.pages[0]; e = None\nexcept Exception as x:\n    e = (type(x).__name__, str(x))\nout = (r.is_encrypted, e, r.decrypt('pw').name, r.pages[0].extract_text())"), "(True, ('FileNotDecryptedError', 'File has not been decrypted'), 'OWNER_PASSWORD', 'Secret')")),
 ('PdfWriting', 'Protection', 'EmptyUserPassword', "writer.encrypt(user_password='', owner_password='x')",
  'A file encrypted with an empty user password and another owner password opens without a decrypt() call: is_encrypted was True, pages[0] gave Open, and the owner password still returned OWNER_PASSWORD.',
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('Open'))); w.encrypt('', owner_password='owner')\nb = io.BytesIO(); w.write(b)\nr = pypdf.PdfReader(b)\nout = (r.is_encrypted, r.pages[0].extract_text(), r.decrypt('owner').name)"), "(True, 'Open', 'OWNER_PASSWORD')")),
 ('PdfWriting', 'ApiHistory', 'RemovedNames', 'pypdf.PdfFileReader',
  'PdfFileReader, PdfFileWriter and PdfMerger are not attributes of pypdf 6.20.1 (False) while PdfReader and PdfWriter are (True), so tutorials written for older versions raise AttributeError.',
  (X(_PRE + "res = {}\nfor n in ('PdfFileReader', 'PdfFileWriter', 'PdfMerger', 'PdfReader', 'PdfWriter'):\n    res[n] = hasattr(pypdf, n)\nout = res"), "{'PdfFileReader': False, 'PdfFileWriter': False, 'PdfMerger': False, 'PdfReader': True, 'PdfWriter': True}")),
 ('PdfWriting', 'ApiHistory', 'WriteNeedsBinaryFile', "open('out.pdf', 'wb')",
  "write() wants a file opened for binary writing: opened with 'w' it raised TypeError, write() argument must be str, not bytes, and with 'wb' it wrote.",
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x')))\nd = tempfile.mkdtemp(); res = []\nfor mode in ('w', 'wb'):\n    try:\n        with open(os.path.join(d, 'o.pdf'), mode) as f:\n            w.write(f)\n        res.append((mode, 'written'))\n    except TypeError as e:\n        res.append((mode, str(e)))\nout = res"), "[('w', 'write() argument must be str, not bytes'), ('wb', 'written')]")),
 ('WordDocuments', 'DocxPackage', 'DocxIsZipOfXml', "zipfile.ZipFile('helloworld.docx')",
  'A .docx file is a ZIP archive: the first bytes were PK and 03 04, a new document held 17 parts including word/document.xml, and three files ending in .rels tie the parts together.',
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); d.add_paragraph('Hello, world!')\nb = io.BytesIO(); d.save(b)\nz = zipfile.ZipFile(b)\nout = (b.getvalue()[:4], len(z.namelist()), 'word/document.xml' in z.namelist(), [n for n in z.namelist() if n.endswith('.rels')])"), "(b'PK\\x03\\x04', 17, True, ['_rels/.rels', 'word/_rels/document.xml.rels', 'customXml/_rels/item1.xml.rels'])")),
 ('WordDocuments', 'DocxPackage', 'DocumentXmlBody', '<w:p><w:r><w:t>Hello, world!</w:t></w:r></w:p>',
  'The body of word/document.xml for one paragraph was <w:p><w:r><w:t>Hello, world!</w:t></w:r></w:p>: a paragraph (w:p) holds runs (w:r), and a run holds text (w:t).',
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); d.add_paragraph('Hello, world!')\nb = io.BytesIO(); d.save(b)\nx = zipfile.ZipFile(b).read('word/document.xml').decode()\nout = re.findall(r'<w:body>(.*?)<w:sectPr', x, re.S)[0]"), "'<w:p><w:r><w:t>Hello, world!</w:t></w:r></w:p>'")),
 ('WordDocuments', 'DocxPackage', 'DefaultTemplate', 'docx.Document()',
  "docx.Document() starts from the package's own template and not from an empty file: its author was python-docx, it was created in 2013, it had 0 paragraphs, 1 section and more than 100 styles.",
  (X(_PRE + 'import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document()\ncp = d.core_properties\nout = (cp.author, cp.created.year, len(d.paragraphs), len(d.sections), len(list(d.styles)) > 100)'), "('python-docx', 2013, 0, 1, True)")),
 ('WordDocuments', 'ReadingText', 'ParagraphsOfBody', 'doc.paragraphs',
  'doc.paragraphs is a list of Paragraph objects in body order: the texts were one, two and an empty string (an empty paragraph counts), and joining them with newlines ends with a newline because the last paragraph is empty.',
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); d.add_paragraph('one'); d.add_paragraph('two'); d.add_paragraph('')\nout = (type(d.paragraphs).__name__, [p.text for p in d.paragraphs], '\\n'.join(p.text for p in d.paragraphs))"), "('list', ['one', 'two', ''], 'one\\ntwo\\n')")),
 ('WordDocuments', 'ReadingText', 'RunsSplitAtFormatting', 'doc.paragraphs[1].runs',
  "A paragraph is split into runs wherever the formatting changes: the four runs were 'A plain paragraph with some ', 'bold', ' text and some ' and 'italic', with bold values None, True, None, None and italic values None, None, None, True; the chapter prints the third run as ' and some ' without the word text.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); p = d.add_paragraph('A plain paragraph with some ')\np.add_run('bold').bold = True\np.add_run(' text and some ')\np.add_run('italic').italic = True\nout = ([r.text for r in p.runs], [r.bold for r in p.runs], [r.italic for r in p.runs], p.text)"), "(['A plain paragraph with some ', 'bold', ' text and some ', 'italic'], [None, True, None, None], [None, None, None, True], 'A plain paragraph with some bold text and some italic')")),
 ('WordDocuments', 'ReadingText', 'TablesAndHeadersApart', 'doc.paragraphs',
  "doc.paragraphs holds only the body's own paragraphs: with a table and a header present it returned ['body'], and the table text 'in a table' and the header text 'IN THE HEADER' had to be read from the table cell and from the section header.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); d.add_paragraph('body')\nt = d.add_table(rows=1, cols=1); t.cell(0, 0).text = 'in a table'\nd.sections[0].header.paragraphs[0].text = 'IN THE HEADER'\nout = ([p.text for p in d.paragraphs], t.cell(0, 0).text, d.sections[0].header.paragraphs[0].text)"), "(['body'], 'in a table', 'IN THE HEADER')")),
 ('WordDocuments', 'ReadingText', 'HyperlinkTextAndRuns', 'paragraph.runs',
  "For a paragraph that contains a hyperlink, text includes the linked words (before linked) in python-docx 1.2.0 but runs lists only 'before ': the linked text is not in any Run, so a program that joins run texts loses it.",
  (X(_PRE + 'import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); q = d.add_paragraph(\'before \')\nq._p.append(parse_xml(\'<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:r><w:t>linked</w:t></w:r></w:hyperlink>\'))\nout = (q.text, [r.text for r in q.runs])'), "('before linked', ['before '])")),
 ('WordDocuments', 'StyleSystem', 'StyleKindsOfTemplate', 'doc.styles',
  "The template's 164 styles are of four kinds: 27 character, 1 list, 36 paragraph and 100 table styles, and Heading 1 and Normal are among them.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document()\nfrom collections import Counter\nout = (sorted(Counter(s.type.name for s in d.styles).items()), 'Heading 1' in [s.name for s in d.styles], 'Normal' in [s.name for s in d.styles])"), "([('CHARACTER', 27), ('LIST', 1), ('PARAGRAPH', 36), ('TABLE', 100)], True, True)")),
 ('WordDocuments', 'StyleSystem', 'StyleKindMismatch', "paragraph.style = 'Quote Char'",
  "A paragraph accepts only paragraph styles and a run only character styles: paragraph.style = 'Quote Char' and run.style = 'Quote' raised ValueError (assigned style is type CHARACTER, need PARAGRAPH, and the reverse), while Quote on the paragraph and Quote Char on the run were accepted.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); p = d.add_paragraph('x'); r = p.add_run('y'); res = []\nfor obj, name in ((p, 'Quote Char'), (r, 'Quote'), (p, 'Quote'), (r, 'Quote Char')):\n    try:\n        obj.style = name; res.append((name, 'accepted'))\n    except ValueError as e:\n        res.append((name, str(e)[:42]))\nout = res"), "[('Quote Char', 'assigned style is type CHARACTER (2), need'), ('Quote', 'assigned style is type PARAGRAPH (1), need'), ('Quote', 'accepted'), ('Quote Char', 'accepted')]")),
 ('WordDocuments', 'StyleSystem', 'UnknownStyleKeyError', "doc.add_paragraph('x', 'List Number ')",
  "A style name must match exactly: 'List Number ' with the trailing space the chapter prints raised KeyError, no style with name 'List Number ', 'List Number' worked, and 'NoSuchStyle' raised the same KeyError.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); res = []\nfor n in ('List Number ', 'List Number', 'NoSuchStyle'):\n    try:\n        d.add_paragraph('x', n); res.append((n, 'ok'))\n    except KeyError as e:\n        res.append((n, str(e)))\nout = res"), '[(\'List Number \', \'"no style with name \\\'List Number \\\'"\'), (\'List Number\', \'ok\'), (\'NoSuchStyle\', \'"no style with name \\\'NoSuchStyle\\\'"\')]')),
 ('WordDocuments', 'StyleSystem', 'StyleIdLookupDeprecated', "doc.add_paragraph('x', 'MacroText')",
  "The chapter lists MacroText among the default style names; in the template the style is named macro and has the id MacroText, add_paragraph('x', 'MacroText') worked but warned that style lookup by style_id is deprecated, and the name Macro Text is not among the styles.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nimport warnings\nd = docx.Document()\nwith warnings.catch_warnings(record=True) as w:\n    warnings.simplefilter('always')\n    p = d.add_paragraph('x', 'MacroText')\nout = (p.style.name, p.style.style_id, [str(i.message)[:48] for i in w], 'Macro Text' in [s.name for s in d.styles])"), "('macro', 'MacroText', ['style lookup by style_id is deprecated. Use styl'], False)")),
 ('WordDocuments', 'StyleSystem', 'CustomParagraphStyle', "doc.styles.add_style('Invitation Name', WD_STYLE_TYPE.PARAGRAPH)",
  "styles.add_style('Invitation Name', WD_STYLE_TYPE.PARAGRAPH) makes a paragraph style whose base is Normal and whose font can be set (24 points, bold), and add_paragraph('Prof. Plum', 'Invitation Name') used it.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document()\ns = d.styles.add_style('Invitation Name', WD_STYLE_TYPE.PARAGRAPH)\ns.base_style = d.styles['Normal']; s.font.size = docx.shared.Pt(24); s.font.bold = True\np = d.add_paragraph('Prof. Plum', 'Invitation Name')\nout = (s.name, s.type.name, p.style.name, s.font.size.pt, s.font.bold, s.base_style.name)"), "('Invitation Name', 'PARAGRAPH', 'Invitation Name', 24.0, True, 'Normal')")),
 ('WordWriting', 'BuildingContent', 'AddParagraphReturnsParagraph', "doc.add_paragraph('Hello, world!')",
  "add_paragraph('Hello, world!') returns the new Paragraph, whose text is the string and whose style is Normal, and it became the only entry of doc.paragraphs.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); p = d.add_paragraph('Hello, world!')\nout = (type(p).__name__, p.text, len(d.paragraphs), p.style.name)"), "('Paragraph', 'Hello, world!', 1, 'Normal')")),
 ('WordWriting', 'BuildingContent', 'AddRunAppends', "paragraph.add_run(' This text is being added')",
  "add_run() adds a Run at the end of the paragraph and returns it: after adding the second text the paragraph's text was the two strings joined and it had 2 runs.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); p = d.add_paragraph('Hello world!')\nr = p.add_run(' This text is being added to the second paragraph.')\nout = (type(r).__name__, p.text, len(p.runs))"), "('Run', 'Hello world! This text is being added to the second paragraph.', 2)")),
 ('WordWriting', 'BuildingContent', 'AddHeadingLevels', "doc.add_heading('Header 4', 4)",
  "add_heading(text, level) accepts 0 to 9: 0 gives the style Title, 1 Heading 1, 4 Heading 4 and 9 Heading 9, while -1 and 10 raised ValueError and the string '1' raised TypeError; the chapter says 0 to 4 in one sentence and 1 to 9 in the next.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); res = []\nfor lv in (0, 1, 4, 9, -1, 10, '1'):\n    try:\n        res.append((lv, d.add_heading('h', lv).style.name))\n    except (ValueError, TypeError) as e:\n        res.append((lv, type(e).__name__))\nout = res"), "[(0, 'Title'), (1, 'Heading 1'), (4, 'Heading 4'), (9, 'Heading 9'), (-1, 'ValueError'), (10, 'ValueError'), ('1', 'TypeError')]")),
 ('WordWriting', 'RunFormatting', 'TriStateBold', 'run.bold = True / False / None',
  'Run.bold has three values: None until set (the file says nothing), True writes <w:b/>, False writes <w:b w:val=0/>, and setting None removes the element again.',
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); r = d.add_paragraph().add_run('t'); res = [r.bold]\nfor v in (True, False, None):\n    r.bold = v; res.append((v, r.bold, re.findall(r'<w:b[ /][^>]*>', r._r.xml)))\nout = res"), '[None, (True, True, [\'<w:b/>\']), (False, False, [\'<w:b w:val="0"/>\']), (None, None, [])]')),
 ('WordWriting', 'RunFormatting', 'UnderlineValues', 'run.underline = WD_UNDERLINE.DOUBLE',
  'underline takes True (single), a WD_UNDERLINE member such as DOUBLE, or False (none), and writes <w:u w:val=single/>, <w:u w:val=double/> and <w:u w:val=none/>.',
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); r = d.add_paragraph().add_run('t'); res = []\nfor v in (True, WD_UNDERLINE.DOUBLE, False):\n    r.underline = v; res.append((r.underline, re.findall(r'<w:u [^>]*>', r._r.xml)))\nout = res"), '[(True, [\'<w:u w:val="single"/>\']), (<WD_UNDERLINE.DOUBLE: 3>, [\'<w:u w:val="double"/>\']), (False, [\'<w:u w:val="none"/>\'])]')),
 ('WordWriting', 'RunFormatting', 'RunVersusFontAttributes', 'run.strike / run.font.strike',
  "Of the twelve attributes of the chapter's Table 17-1 only bold, italic and underline are attributes of a Run; all twelve, including strike, double_strike, all_caps, small_caps, shadow, outline, rtl, imprint and emboss, are attributes of run.font.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); r = d.add_paragraph().add_run('t')\nnames = ('bold', 'italic', 'underline', 'strike', 'double_strike', 'all_caps', 'small_caps', 'shadow', 'outline', 'rtl', 'imprint', 'emboss')\nout = ([n for n in names if n in dir(type(r))], [n for n in names if n in dir(type(r.font))])"), "(['bold', 'italic', 'underline'], ['bold', 'italic', 'underline', 'strike', 'double_strike', 'all_caps', 'small_caps', 'shadow', 'outline', 'rtl', 'imprint', 'emboss'])")),
 ('WordWriting', 'RunFormatting', 'UnknownRunAttributeIgnored', 'run.strike = True',
  'run.strike = True raised nothing and changed nothing (font.strike stayed None and the XML had no w:strike element), because Python lets any object take a new attribute; run.font.strike = True set it and wrote the element.',
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); r = d.add_paragraph().add_run('t')\nr.strike = True\na = (r.font.strike, '<w:strike' in r._r.xml)\nr.font.strike = True\nout = (a, (r.font.strike, '<w:strike' in r._r.xml))"), '((None, False), (True, True))')),
 ('WordWriting', 'BreaksAndPictures', 'PageBreakRun', 'doc.add_page_break() / run.add_break(WD_BREAK.PAGE)',
  'A page break is a run holding <w:br w:type=page/>: run.add_break(WD_BREAK.PAGE) and add_page_break() each wrote one (2 in the document), add_page_break() adds a paragraph of its own (3 paragraphs in all), and WD_BREAK is reachable as docx.enum.text.WD_BREAK.',
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); p = d.add_paragraph('First page'); p.add_run().add_break(WD_BREAK.PAGE); d.add_paragraph('Second page')\nd.add_page_break()\nout = (re.findall(r'<w:br[^>]*>', d.element.xml), len(d.paragraphs), WD_BREAK.PAGE.name, docx.enum.text.WD_BREAK is WD_BREAK)"), '([\'<w:br w:type="page"/>\', \'<w:br w:type="page"/>\'], 3, \'PAGE\', True)')),
 ('WordWriting', 'BreaksAndPictures', 'NewlineBecomesBreak', "run.text = 'a\\tb\\nc'",
  "In the text of a run a tab becomes <w:tab/> and a newline becomes <w:br/>, and reading the run's text gives the tab and the newline back.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); p = d.add_paragraph(); r = p.add_run('a\\tb\\nc')\nout = (re.findall(r'<w:(?:tab|br)/>', r._r.xml), r.text)"), "(['<w:tab/>', '<w:br/>'], 'a\\tb\\nc')")),
 ('WordWriting', 'BreaksAndPictures', 'PictureSizeFromWidth', "doc.add_picture('zophie.png', width=Inches(1))",
  'add_picture() with no size uses the size of the image (a 60 by 80 pixel PNG with no resolution recorded came out as 762000 by 1016000 EMU, 72 pixels to the inch), a width alone keeps the aspect ratio (914400 by 1219200) and a width with a height gives both exactly (914400 by 1440000), so the ratio is lost.',
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); b = io.BytesIO(png(60, 80)); res = []\nfor kw in ({}, {'width': Inches(1)}, {'width': Inches(1), 'height': Cm(4)}):\n    b.seek(0); s = d.add_picture(b, **kw); res.append((s.width, s.height))\nout = res"), '[(762000, 1016000), (914400, 1219200), (914400, 1440000)]')),
 ('WordWriting', 'BreaksAndPictures', 'EmuUnits', 'Inches(1), Cm(1)',
  'Lengths are integers in English Metric Units: Inches(1) is 914400, Cm(1) is 360000, Pt(1) is 12700, and Inches(1).inches is 1.0.',
  (X(_PRE + 'import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nout = (int(Inches(1)), int(Cm(1)), int(docx.shared.Pt(1)), Inches(1).inches, round(Cm(2.54).inches, 6))'), '(914400, 360000, 12700, 1.0, 1.0)')),
 ('WordWriting', 'BreaksAndPictures', 'PictureStoredOnce', 'doc.add_picture(...) three times',
  'Each add_picture() adds a paragraph and an inline shape, but identical bytes are stored once: three pictures gave 3 paragraphs, 3 inline shapes and one media part, word/media/image1.png, equal to the original bytes.',
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nd = docx.Document(); data = png(10, 10)\nfor i in range(3): d.add_picture(io.BytesIO(data))\nb = io.BytesIO(); d.save(b); z = zipfile.ZipFile(b)\nout = (len(d.paragraphs), len(d.inline_shapes), [n for n in z.namelist() if n.startswith('word/media')], z.read('word/media/image1.png') == data)"), "(3, 3, ['word/media/image1.png'], True)")),
 ('ToolsAndPractice', 'PackagesAndSetup', 'PackageNameTrap', 'pip install python-docx',
  'The import name docx belongs to the package python-docx (1.2.0 installed); a distribution called docx is not installed (None), and pypdf is 6.20.1 while PyPDF2 (None) is the name of an older project.',
  (X(_PRE + "import importlib.metadata as m, docx\nres = {}\nfor n in ('python-docx', 'docx', 'pypdf', 'PyPDF2'):\n    try: res[n] = m.version(n)\n    except m.PackageNotFoundError: res[n] = None\nout = (res, docx.__name__, docx.__file__.endswith('__init__.py'))"), "({'python-docx': '1.2.0', 'docx': None, 'pypdf': '6.20.1', 'PyPDF2': None}, 'docx', True)")),
 ('ToolsAndPractice', 'PackagesAndSetup', 'OptionalDependencyAes', "writer.encrypt('pw', algorithm='AES-256')",
  'Without the cryptography package RC4, the default, is written, AES-128 fails later, at write(), and AES-256 fails at encrypt(), both with DependencyError, cryptography>=3.1 is required for AES algorithm.',
  (XC("res = []\nfor kw in ({}, {'algorithm': 'AES-128'}, {'algorithm': 'AES-256'}):\n    w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x'))); step = 'encrypt'\n    try:\n        w.encrypt('pw', **kw); step = 'write'; w.write(io.BytesIO()); res.append('written')\n    except Exception as e:\n        res.append((step, type(e).__name__, str(e)))\nout = res"), "['written', ('write', 'DependencyError', 'cryptography>=3.1 is required for AES algorithm'), ('encrypt', 'DependencyError', 'cryptography>=3.1 is required for AES algorithm')]")),
 ('ToolsAndPractice', 'PracticePrograms', 'CombineAllPdfs', 'combine_pdfs.py (Project 12)',
  "Project 12 with the loop's list named consistently: three files sorted without regard to case (A_cover, b_report, c_one) and every file's pages from the second on appended gave A2, B2, B3, and the one-page file added nothing.",
  (X(_PRE + "d = tempfile.mkdtemp()\nfor n, t in (('b_report.pdf', ('B1', 'B2', 'B3')), ('A_cover.pdf', ('A1', 'A2')), ('c_one.pdf', ('C1',))):\n    open(os.path.join(d, n), 'wb').write(mk(*t))\nnames = sorted((f for f in os.listdir(d) if f.lower().endswith('.pdf')), key=str.lower)\nw = pypdf.PdfWriter()\nfor n in names:\n    r = pypdf.PdfReader(os.path.join(d, n))\n    w.append(r, pages=(1, len(r.pages)))\nout = (names, txts(w))"), "(['A_cover.pdf', 'b_report.pdf', 'c_one.pdf'], ['A2', 'B2', 'B3'])")),
 ('ToolsAndPractice', 'PracticePrograms', 'CaseInsensitiveSort', 'pdf_filenames.sort(key=str.lower)',
  "Sorting puts capital letters first, Mango.pdf, Zebra.pdf, apple.pdf, and key=str.lower, the argument of the chapter's pdf_filenames.sort(), gives apple.pdf, Mango.pdf, Zebra.pdf.",
  (X(_PRE + "n = ['Zebra.pdf', 'apple.pdf', 'Mango.pdf']\nout = (sorted(n), sorted(n, key=str.lower))"), "(['Mango.pdf', 'Zebra.pdf', 'apple.pdf'], ['apple.pdf', 'Mango.pdf', 'Zebra.pdf'])")),
 ('ToolsAndPractice', 'PracticePrograms', 'WalkFindsAllPdfs', "for filename in os.listdir('.'): if filename.endswith('.pdf')",
  "os.walk visits every subfolder, and a test with f.lower().endswith('.pdf') found C.PDF as well as the other two files (3), while f.endswith('.pdf'), the form Project 12 uses with os.listdir, missed it (2).",
  (X(_PRE + "d = tempfile.mkdtemp(); os.makedirs(os.path.join(d, 'sub', 'deeper'))\nfor rel in ('a.pdf', 'notes.txt', 'sub/b.pdf', 'sub/deeper/C.PDF'): open(os.path.join(d, rel), 'wb').write(b'x')\nfound = sorted(os.path.relpath(os.path.join(r, f), d) for r, ds, fs in os.walk(d) for f in fs if f.lower().endswith('.pdf'))\nexact = sorted(os.path.relpath(os.path.join(r, f), d) for r, ds, fs in os.walk(d) for f in fs if f.endswith('.pdf'))\nout = (found, exact)"), "(['a.pdf', 'sub/b.pdf', 'sub/deeper/C.PDF'], ['a.pdf', 'sub/b.pdf'])")),
 ('ToolsAndPractice', 'PracticePrograms', 'InvitationPageBreaks', 'doc.add_page_break() after each guest',
  'Adding a page break after every guest wrote 3 breaks for 3 guests and 6 paragraphs, while adding one only between guests wrote 2 breaks and 5 paragraphs.',
  (X(_PRE + 'import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nnames = [\'Prof. Plum\', \'Miss Scarlet\', \'Col. Mustard\']\nd = docx.Document(); e = docx.Document()\nfor i, n in enumerate(names):\n    d.add_paragraph(n); d.add_page_break()\n    e.add_paragraph(n)\n    if i < len(names) - 1: e.add_page_break()\nf = lambda x: x.element.xml.count(\'w:type="page"\')\nout = (f(d), f(e), len(d.paragraphs), len(e.paragraphs))'), '(3, 2, 6, 5)')),
 ('ToolsAndPractice', 'PracticePrograms', 'DictionaryAttackBothCases', 'for word in words: decrypt(word); decrypt(word.upper())',
  'Trying each word and then its upper-case form against a file encrypted with BANANA found BANANA after 4 attempts out of 6 possible, so a dictionary of n words costs up to 2n attempts.',
  (X(_PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('Locked'))); w.encrypt('BANANA')\nb = io.BytesIO(); w.write(b); data = b.getvalue()\nwords = ['apple', 'banana', 'cherry']; tries = 0; found = None\nfor word in words:\n    for guess in (word, word.upper()):\n        tries += 1\n        if pypdf.PdfReader(io.BytesIO(data)).decrypt(guess).name != 'NOT_DECRYPTED':\n            found = guess; break\n    if found: break\nout = (found, tries, 2 * len(words))"), "('BANANA', 4, 6)")),
 ('ToolsAndPractice', 'PracticeQuestions', 'PracticeAnswersChecked', 'the 12 practice questions',
  "The code answers of the 12 practice questions were checked: pages[4] is the fifth page ('Page 5'), docx.Document() returns a Document with 0 paragraphs, add_paragraph returns a Paragraph with the given text, only bold, underline and italic are attributes of a Run, and doc.paragraphs is a list.",
  (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nfrom docx.oxml import parse_xml\nr = pypdf.PdfReader(io.BytesIO(six()))\nd = docx.Document(); p = d.add_paragraph('Hello, there!')\nout = (r.pages[4].extract_text(), type(d).__name__, type(p).__name__, len(docx.Document().paragraphs), p.text, [x for x in ('bold', 'underline', 'italic', 'strike', 'outline') if x in dir(docx.text.run.Run)], isinstance(d.paragraphs, list))"), "('Page 5', 'Document', 'Paragraph', 0, 'Hello, there!', ['bold', 'underline', 'italic'], True)")),
]

CLAIMS = [
 (X(_PRE + "import importlib.metadata as m, sys\nout = (m.version('pypdf').split('.')[0], m.version('python-docx').split('.')[0], m.version('pdfminer.six'), sys.version_info[:2] >= (3, 14))"), "('6', '1', '20260107', True)"),
 (X(_PRE + "out = (rd(mk('a')).pdf_header, rd(mk('a')).is_encrypted, rd(mk('a')).pages[0].rotation, [float(x) for x in rd(mk('a')).pages[0].mediabox])"), "('%PDF-1.4', False, 0, [0.0, 0.0, 612.0, 792.0])"),
 (X(_PRE + "r = rd(mk('a'))\nout = (hasattr(r, 'getPage'), hasattr(r, 'numPages'), hasattr(r.pages[0], 'extractText'), hasattr(r.pages[0], 'rotateClockwise'), hasattr(pypdf.PdfWriter, 'addBlankPage'))"), '(False, False, False, False, False)'),
 (X(_PRE + 'out = [(m.name, m.value) for m in pypdf.PasswordType]'), "[('NOT_DECRYPTED', 0), ('USER_PASSWORD', 1), ('OWNER_PASSWORD', 2)]"),
 (X(_PRE + "import inspect\nout = inspect.signature(pypdf.PdfWriter.encrypt).parameters['algorithm'].default"), 'None'),
 (X(_PRE + 'out = (pypdf.PdfWriter().add_blank_page(100, 50).mediabox.width, pypdf.PdfWriter().add_blank_page(100, 50).mediabox.height)'), '(100.0, 50.0)'),
 (X(_PRE + "import docx\nd = docx.Document(); b = io.BytesIO(); d.save(b)\nout = (zipfile.is_zipfile(io.BytesIO(mk('a'))), zipfile.is_zipfile(b), b.getvalue()[:2])"), "(False, True, b'PK')"),
 (X(_PRE + 'import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nd = docx.Document(); s = d.sections[0]\nout = (d.add_paragraph().style.name, s.page_width, s.page_height, Inches(8.5), Inches(11), Pt(12))'), "('Normal', 7772400, 10058400, 7772400, 10058400, 152400)"),
 (X(_PRE + 'import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nout = ([m.name for m in WD_BREAK][:6], sorted(m.name for m in WD_STYLE_TYPE), WD_UNDERLINE.DOUBLE.value, WD_UNDERLINE.NONE.value)'), "(['COLUMN', 'LINE', 'LINE_CLEAR_LEFT', 'LINE_CLEAR_RIGHT', 'LINE_CLEAR_ALL', 'PAGE'], ['CHARACTER', 'LIST', 'PARAGRAPH', 'TABLE'], 3, 0)"),
 (X(_PRE + 'import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nd = docx.Document()\nout = (repr(d.core_properties.title), d.core_properties.revision, d.core_properties.last_modified_by)'), '("\'\'", 1, \'\')'),
 (X(_PRE + 'out = (44000 * 2, 349900 * 2, round(349900 / 44000, 1), 2 * 4)'), '(88000, 699800, 8.0, 8)'),
 (X(_PRE + "import PIL, cryptography, lxml\nout = (int(PIL.__version__.split('.')[0]) >= 10, int(cryptography.__version__.split('.')[0]) >= 3)"), '(True, True)'),
 (X(_PRE + 'import pdfminer.high_level as h, pdfminer\nout = (callable(h.extract_text), pdfminer.__version__)'), "(True, '20260107')"),
 (X(_PRE + "out = sorted(n for n in dir(pypdf) if n.startswith('Pdf') and n[3:4].isupper())[:8]"), "['PdfReader', 'PdfWriter']"),
 (X(_PRE + 'w = pypdf.PdfWriter(); w.add_blank_page(10, 10)\nb = io.BytesIO(); r = w.write(b)\nout = (type(r).__name__, len(r), b.getvalue()[:5])'), "('tuple', 2, b'%PDF-')"),
 (X(_PRE + "out = (re.findall(rb'/Type ?/Catalog', mk('a')), mk('a').count(b'endobj'), len(mk('a', 'b', 'c')) > len(mk('a')))"), "([b'/Type/Catalog'], 5, True)"),
 (X(_PRE + "def enc(**kw):\n    w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x'))); w.encrypt('a', **kw); b = io.BytesIO(); w.write(b); return b.getvalue()\nout = (enc() == enc(), enc(algorithm='AES-256') == enc(algorithm='AES-256'))"), '(True, False)'),
 (X(_PRE + "r = rd(six())\nout = (r.pages[0].extract_text() == 'Page 1', [p.extract_text() for p in r.pages][-1], r.get_num_pages() if hasattr(r, 'get_num_pages') else None)"), "(True, 'Page 6', 6)"),
 (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nd = docx.Document(); p = d.add_paragraph('a'); p.add_run('b'); p.add_run('c')\nout = (p.text, len(p.runs), p.runs[0].text, p.runs[1].text, p.paragraph_format.alignment, p.runs[0].font.size, p.runs[0].font.name)"), "('abc', 3, 'a', 'b', None, None, None)"),
 (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nd = docx.Document(); d.add_heading('T', 0); d.add_heading('H1', 1); d.add_paragraph('x', 'List Bullet'); d.add_paragraph('y', 'List Number'); d.add_paragraph('q', 'Intense Quote')\nout = [(p.style.name, p.text) for p in d.paragraphs]"), "[('Title', 'T'), ('Heading 1', 'H1'), ('List Bullet', 'x'), ('List Number', 'y'), ('Intense Quote', 'q')]"),
 (X(_PRE + "import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.enum.style import WD_STYLE_TYPE\nd = docx.Document(); d.add_paragraph('a')\nb = io.BytesIO(); d.save(b); e = docx.Document(io.BytesIO(b.getvalue()))\nout = ([p.text for p in e.paragraphs], len(e.paragraphs), e.core_properties.author)"), "(['a'], 1, 'python-docx')"),
 (X(_PRE + "import os, tempfile\nd = tempfile.mkdtemp(); open(os.path.join(d, 'x.pdf'), 'wb').write(mk('a'))\nout = (os.listdir(d), os.path.getsize(os.path.join(d, 'x.pdf')) > 200)"), "(['x.pdf'], True)"),
]
ERRORS = []

BEH = [
 ['A hand-built PDF is read back: the page count, the text of each page, the version line and the missing metadata',
  _PRE + "r = rd(mk('Page one', 'Page two'))\nprint(len(r.pages), [p.extract_text() for p in r.pages])\nprint(r.pdf_header, r.metadata, r.is_encrypted)",
  "2 ['Page one', 'Page two']\n%PDF-1.4 None False"],
 ['append() takes a tuple as a range, a step tuple, and a list as exact pages',
  _PRE + 'for pages in ((0, 5), (0, 5, 2), [0, 5]):\n    w = pypdf.PdfWriter(); w.append(io.BytesIO(six()), pages); print(pages, txts(w))',
  "(0, 5) ['Page 1', 'Page 2', 'Page 3', 'Page 4', 'Page 5']\n(0, 5, 2) ['Page 1', 'Page 3', 'Page 5']\n[0, 5] ['Page 1', 'Page 6']"],
 ['merge() with the tuple in the third place inserts the whole file under a bookmark, with pages= it inserts the pages',
  _PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('A1', 'A2', 'A3'))); w.merge(1, io.BytesIO(six()), (0, 2))\nprint(len(w.pages), [o['/Title'] for o in w.outline])\nw = pypdf.PdfWriter(); w.append(io.BytesIO(mk('A1', 'A2', 'A3'))); w.merge(1, io.BytesIO(six()), pages=(0, 2))\nprint(len(w.pages), txts(w))",
  "9 ['(0, 2)']\n5 ['A1', 'Page 1', 'Page 2', 'A2', 'A3']"],
 ['Rotation angles add up and a multiple of 90 is required',
  _PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x'))); p = w.pages[0]\nfor a in (90, 270, -90, 180): p.rotate(a); print(a, p.rotation)\ntry: p.rotate(45)\nexcept ValueError as e: print(e)",
  '90 90\n270 360\n-90 270\n180 450\nRotation angle must be a multiple of 90'],
 ['The default encryption is RC4 and AES-256 is a choice, with the numbers the file records',
  _PRE + "for kw in ({}, {'algorithm': 'AES-256'}):\n    w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('x'))); w.encrypt('swordfish', **kw)\n    b = io.BytesIO(); w.write(b); e = pypdf.PdfReader(b).trailer['/Encrypt']; print(kw, e['/V'], e['/R'], e['/Length'])",
  "{} 2 3 128\n{'algorithm': 'AES-256'} 5 6 256"],
 ['decrypt() names the password that matched and never raises for a wrong one',
  _PRE + "w = pypdf.PdfWriter(); w.append(io.BytesIO(mk('Secret'))); w.encrypt('swordfish', algorithm='AES-256')\nb = io.BytesIO(); w.write(b); data = b.getvalue()\nr = pypdf.PdfReader(io.BytesIO(data))\ntry: r.pages[0]\nexcept Exception as e: print(type(e).__name__)\nfor pw in ('an incorrect password', 'swordfish'): print(pw, pypdf.PdfReader(io.BytesIO(data)).decrypt(pw).name)",
  'FileNotDecryptedError\nan incorrect password NOT_DECRYPTED\nswordfish OWNER_PASSWORD'],
 ['Text under a black rectangle is still extracted',
  _PRE + "c = 'BT /F1 18 Tf 72 720 Td (Salary: 120000 USD) Tj ET 0 0 0 rg 60 710 300 30 re f'\nprint(rd(mk(c)).pages[0].extract_text())",
  'Salary: 120000 USD'],
 ['A paragraph is made of runs and bold has three values',
  _PRE + "import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.oxml import parse_xml\nd = docx.Document(); p = d.add_paragraph('A plain paragraph with some ')\np.add_run('bold').bold = True; p.add_run(' text and some '); p.add_run('italic').italic = True\nprint([(r.text, r.bold, r.italic) for r in p.runs]); print(p.text)",
  "[('A plain paragraph with some ', None, None), ('bold', True, None), (' text and some ', None, None), ('italic', None, True)]\nA plain paragraph with some bold text and some italic"],
 ['add_heading accepts 0 to 9 and refuses the rest',
  _PRE + "import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.oxml import parse_xml\nd = docx.Document()\nfor lv in (0, 1, 9, 10):\n    try: print(lv, d.add_heading('h', lv).style.name)\n    except ValueError as e: print(lv, e)",
  '0 Title\n1 Heading 1\n9 Heading 9\n10 level must be in range 0-9, got 10'],
 ["The text of a hyperlink is in the paragraph's text and not in its runs",
  _PRE + 'import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.oxml import parse_xml\nd = docx.Document(); q = d.add_paragraph(\'before \')\nq._p.append(parse_xml(\'<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:r><w:t>linked</w:t></w:r></w:hyperlink>\'))\nprint(repr(q.text), [r.text for r in q.runs])',
  "'before linked' ['before ']"],
 ["A style name with the trailing space of the chapter's list is refused",
  _PRE + "import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.oxml import parse_xml\nd = docx.Document()\nfor n in ('List Number ', 'List Number'):\n    try: d.add_paragraph('x', n); print(repr(n), 'ok')\n    except KeyError as e: print(repr(n), 'KeyError', e)",
  '\'List Number \' KeyError "no style with name \'List Number \'"\n\'List Number\' ok'],
 ['A .docx file is a ZIP archive and its first bytes are PK',
  _PRE + "import docx\nfrom docx.shared import Inches, Cm, Pt\nfrom docx.enum.text import WD_BREAK, WD_UNDERLINE\nfrom docx.oxml import parse_xml\nd = docx.Document(); d.add_paragraph('Hello, world!'); b = io.BytesIO(); d.save(b)\nz = zipfile.ZipFile(b); print(b.getvalue()[:2], 'word/document.xml' in z.namelist(), len(z.namelist()))",
  "b'PK' True 17"],
]

BODY = {}
def _b(key, p1, p2):
    BODY[key] = p1 + "\n\n" + p2

# ---- the six subjects ----
_b('PdfFormat',
 "The chapter opens by saying that PDF and Word are binary files that also hold font, colour and layout information, so a program cannot simply pass their filenames to open(), and that a PDF is great for laying out text for people to print and read and is not easy to parse into plaintext [S]. The PDF standard describes the file as a header, numbered objects, a cross-reference table and a trailer, and the text of a page as drawing commands [ISO][LOC].",
 "Two ideas carry this subject. File structure covers the header and trailer, the cross-reference table, the content stream and the producer metadata. Text and layout covers why text comes out in stream order, why a scanned page has none, why a black box does not redact and why a PDF has no paragraphs. A small PDF written by hand for each example makes every number below reproducible (This study, 2026).")
_b('PdfTextAndImages',
 "The first task of the PDF section is to read a PDF with PyPDF: open a PdfReader, loop over its pages, call extract_text() on each and add the strings together, then write the text to a file, with pdfminer.six as a fallback when PyPDF cannot open a file, and extract the images of each page and write them to files [S][PD]. The chapter says PyPDF might make mistakes when extracting text and may fail to open some PDFs, and that cleaning the extracted text is boring and cannot easily be automated [S].",
 "Three ideas carry this subject. Reading pages covers the pages list, the zero-based index and the way page texts are joined. Extraction quality covers the layout mode, the pdfminer.six alternative, damaged input and the clean-up of hyphens and rows. Image extraction covers the Pillow dependency, the name and data of an image and the names that repeat. Each was run on small files and the chapter's loops on the shipped sample chapter (This study, 2026).")
_b('PdfWriting',
 "The second task is to create a new PDF from pages of existing ones: a PdfWriter starts empty, copies pages from files with append() and merge(), rotates them, adds blank pages, merges a watermark or overlay and encrypts the result, and PdfReader decrypts a protected file [S][PD]. Project 12 puts the copying to work by combining the pages after the first of every PDF in a folder into one file [S].",
 "Five ideas carry this subject. Page selection covers the tuple, the step and the list of pages. Insert and merge covers merge() at a position, the positional tuple trap and the size of a blank page. Page editing covers rotation, the watermark and the overlay. Protection covers the two algorithms, the return values of decrypt() and the empty user password. API history covers the names that older tutorials use. Each was run on pypdf 6.20.1 (This study, 2026).")
_b('WordDocuments',
 "The Word section starts with the Python-Docx package, installed as python-docx and imported as docx, and with the three data types it uses: a Document object for the whole file, Paragraph objects for the paragraphs and Run objects for the stretches of text inside a paragraph [S][DX]. Reading a document means looping over doc.paragraphs and, for a style, setting the style attribute to the name of a paragraph style or a character style [S].",
 "Three ideas carry this subject. The package covers a .docx file as a ZIP archive of XML parts, the body in word/document.xml and the template a new document starts from. Reading text covers paragraphs, runs, and what the paragraphs list leaves out. The style system covers the kinds of style, the names that work and the styles a program can make. Each was run on python-docx 1.2.0 (This study, 2026).")
_b('WordWriting',
 "Writing a Word document means calling add_paragraph() and add_run(), add_heading() with a level, add_break() with a break type on a run, and add_picture() with a width and a height, then save(); the chapter shows each in the shell and ends the section with the attributes of a run in Table 17-1 [S][DX]. The document is saved to a .docx file that Word or LibreOffice Writer opens [S].",
 "Three ideas carry this subject. Building content covers what add_paragraph(), add_run() and add_heading() return and the heading levels. Run formatting covers the three-valued bold and underline, the attributes that live on run.font and the attribute that is silently ignored. Breaks and pictures covers the page break run, the newline, the size of a picture and the way identical pictures are stored. Each was run on python-docx 1.2.0 (This study, 2026).")
_b('ToolsAndPractice',
 "The chapter ends with a summary, twelve practice questions and three practice programs: PDF Paranoia encrypts and decrypts the PDFs of a folder tree, Custom Invitations makes one invitation per page from a list of guests, and PDF Password Breaker tries every word of a dictionary as the password of an encrypted PDF [S]. Installing the two packages is left to Appendix A, which pins their versions [S][APPA].",
 "Three ideas carry this subject. Packages and setup covers the names of the distributions and the optional dependencies. The practice programs cover Project 12, the sort, the walk through a folder tree, the page breaks of the invitations and the dictionary attack. The practice questions cover the code answers that can be checked. The programs were written for this study and run on files made for the purpose and on the shipped files (This study, 2026).")

# ---- the mid concepts ----
_b('FileStructure',
 "A PDF file starts with a header line that names the version, is followed by numbered objects, and ends with a cross-reference table, a trailer and the line %%EOF; the pages, the fonts and the drawing commands of each page are such objects [ISO][LOC]. The chapter does not describe the file, only the PyPDF objects that stand for it [S].",
 "A two-page file was written byte by byte and read back to show the four parts: the header and trailer, the table of offsets, the content stream of a page and the producer entry a library leaves. The same file passed qpdf --check and was read by pypdf and pdftotext (This study, 2026).")
_b('TextAndLayout',
 "The chapter warns that PDFs are great for laying out text for people and are not easy to parse into plaintext, and lists the choices that extraction cannot make by itself: where paragraphs end and begin, whether page numbers, headers and footers are included, how tables are converted and how much whitespace is kept [S]. The PDF standard places text with drawing commands at coordinates, in the order the stream gives them [ISO].",
 "Small pages with known drawing commands show what follows: the text comes out in stream order, a page that is only a picture has no text, a black rectangle drawn over text does not remove it, and separate drawing commands extract as separate lines (This study, 2026).")
_b('ReadingPages',
 "The chapter opens a file in binary read mode, builds a PdfReader from it, takes len(reader.pages) and loops over reader.pages, calling extract_text() on each page and adding the string to a variable; page 1 of the PDF is pages[0] [S][PD]. The pages attribute is a list-like collection of Page objects [PD].",
 "The six-page file used here shows the type of pages, the index of the fifth page, the error past the end and the way the strings of the pages are joined by +=, which is how the chapter's listing builds the text of a whole file (This study, 2026).")
_b('ExtractionQuality',
 "The chapter says PyPDF can make mistakes, offers the pdfminer.six function extract_text() as a fallback for a file PyPDF cannot understand, and suggests a language model prompt to clean up hyphens, headers and paragraph breaks [S][MN]. The pypdf documentation lists extraction modes and says post-processing is outside the library [PD].",
 "The same page was extracted in the default and in the layout mode, the same six-page file went through pdfminer.six, damaged files went through both libraries, and a hyphenated row was repaired by a regular expression. The language model clean-up was NOT EXECUTED (This study, 2026).")
_b('ImageExtraction',
 "The chapter extracts images with the images attribute of a Page object, whose items have a name and the bytes in data, and writes each image to a file opened in binary write mode, putting a counter and the page number in front of the name [S][PD]. The chapter's text does not say that the attribute needs another package [S].",
 "Images were made with Pillow and wrapped in a PDF, so that their name and bytes are known; the access was repeated with Pillow made unavailable, and two pages carrying the same picture showed the names repeat. The shipped sample chapter gave 11 image files (This study, 2026).")
_b('PageSelection',
 "A new PdfWriter has no pages; the chapter calls writer.append() with a filename and a tuple of two integers, which tells the writer to copy pages starting at page index 0 up to but not including index 5, and says a third integer is a step; a list names pages exactly [S][PD]. The write() method saves the writer to a file opened in binary write mode [S].",
 "The same six-page file was appended with a range, a step and a list, and with a number past the end, so that the pages that arrived could be read off by their text (This study, 2026).")
_b('InsertAndMerge',
 "The append() method adds copied pages at the end; to insert them before the end the chapter calls merge(), which has an additional integer argument that gives the position, and add_blank_page() and insert_blank_page() add a page whose size, the chapter says, is the same as that of the preceding page [S][PD]. The chapter prints merge(2, 'Recursion_Chapter1.pdf', (0, 5)) [S].",
 "A three-page writer received pages from the six-page file at position 1, once with the keyword pages and once with the tuple in the place the chapter writes it, and blank pages were added to pages of different sizes (This study, 2026).")
_b('PageEditing',
 "Page objects are edited in place: rotate() turns a page by a multiple of 90 degrees, clockwise when positive, and merge_page() lays the content of one page on another, a watermark under the text or an overlay over it [S][PD]. The chapter rotates every page of the sample chapter in a loop and applies a watermark PDF to pages of it [S].",
 "One page was rotated by several angles, and a one-word page was merged under and over another, so that the order of the drawing commands shows which is below (This study, 2026).")
_b('Protection',
 "PdfWriter.encrypt() accepts a password string and a string that selects the algorithm, and the chapter always uses 'AES-256'; a PdfReader reports is_encrypted and its decrypt() method returns a PasswordType object whose name is NOT_DECRYPTED, USER_PASSWORD or OWNER_PASSWORD [S][PD]. A PDF can have a user password to view it and an owner password to set permissions [S].",
 "Files were written with the default algorithm and with AES-256, opened with the right, wrong and differently capitalised passwords, and written with an empty user password. qpdf and pdftotext confirmed the algorithm and the refusal (This study, 2026).")
_b('ApiHistory',
 "The chapter uses PdfReader and PdfWriter and calls pages, append(), merge(), rotate(), add_blank_page(), insert_blank_page(), merge_page(), encrypt() and decrypt() [S]. The pypdf history says the project began as pyPdf in 2005, was forked as PyPDF2 and merged back into pypdf, and the changelog records the removal of PdfMerger in 5.0.0 [PD].",
 "The old names that tutorials use were looked up in pypdf 6.20.1 and in 5.0.1, and write() was given a file opened in text mode and in binary mode (This study, 2026).")
_b('DocxPackage',
 "A Word document has the .docx extension; Python-Docx opens it with docx.Document(filename) and saves with save() [S][DX]. The format is Office Open XML, a ZIP archive of XML parts, which the chapter does not show [WP][LOC2].",
 "A new document was saved and opened with zipfile to list its parts and read word/document.xml, and the template that docx.Document() starts from was inspected (This study, 2026).")
_b('ReadingText',
 "Reading a Word document means opening it with docx.Document(), taking doc.paragraphs, a list of Paragraph objects, and for each paragraph its text and its list of Run objects; a new paragraph begins whenever the user presses ENTER, and a run is a stretch of text with one style [S][DX]. The chapter's get_text() function joins the texts of the paragraphs [S].",
 "A document was built with known runs and read back; a table, a header and a hyperlink were added to show what doc.paragraphs and paragraph.runs leave out (This study, 2026).")
_b('StyleSystem',
 "The chapter says Word documents contain three types of styles: paragraph styles apply to Paragraph objects, character styles to Run objects and linked styles to both; to style a paragraph or a run, set its style attribute to the name of the style, and for the linked style of a run add ' Char' to the name [S]. It prints a list of default style names and says custom styles are made in the Word application [S].",
 "The styles of the template were counted by kind, wrong kinds and wrong names were assigned, the style id the chapter prints was looked up, and a paragraph style was made in code with add_style() (This study, 2026).")
_b('BuildingContent',
 "The chapter creates a document with docx.Document(), adds a paragraph with add_paragraph('Hello, world!'), adds a run to it with add_run(), and adds headings with add_heading(text, level) [S][DX]. Both add_paragraph() and add_run() accept an optional second argument that is a string of the style to use [S].",
 "The objects returned by the three methods were inspected, and add_heading() was called with levels from -1 to 10 and with a string (This study, 2026).")
_b('RunFormatting',
 "Table 17-1 of the chapter lists twelve attributes of a Run object, bold, italic, underline, strike, double_strike, all_caps, small_caps, shadow, outline, rtl, imprint and emboss, and says each can be set to True, False or None, where None makes the run use the style's setting [S]. The python-docx documentation puts the tri-state properties on the font of a run [DX].",
 "Each attribute name was looked up on a Run and on run.font, the XML each value writes was read, and the assignment of an attribute the Run does not have was run (This study, 2026).")
_b('BreaksAndPictures',
 "To add a line break rather than a new paragraph the chapter calls add_break() on the Run object after which the break appears, and for a page break passes docx.enum.text.WD_BREAK.PAGE; add_picture() takes a filename and optional width and height, which can be given with docx.shared.Inches() and docx.shared.Cm() [S][DX].",
 "Breaks were added and their XML read, a newline and a tab were put in a run, pictures were added with no size, with a width and with both, and three identical pictures were saved and counted in the package (This study, 2026).")
_b('PackagesAndSetup',
 "The chapter tells the reader to install PyPDF and Python-Docx by following Appendix A, to install Python-Docx and not Docx, which belongs to a different package, and to import docx and not python-docx [S]. Appendix A pins pypdf 5.0.1 and python-docx 1.1.2 [APPA].",
 "The names of the installed distributions were read, and the encryption and image examples were run with the optional packages made unavailable. The pinned versions were also installed and the chapter's statements replayed with them (This study, 2026).")
_b('PracticePrograms',
 "Project 12 finds all PDF files in the working directory, sorts them alphabetically, copies every page after the first of each to an output PDF and saves it; the three practice programs encrypt and decrypt a folder tree of PDFs, make one invitation per page for each guest, and try the words of a dictionary as a password [S].",
 "Each program was written and run on files made for the purpose: the combining with a case-insensitive sort, the walk with a lower-case extension test, the invitations with page breaks, and the dictionary attack on a four-word list. Their results are the leaves below (This study, 2026).")
_b('PracticeQuestions',
 "The chapter ends with twelve practice questions that ask for the modes in which the file of a PdfWriter is opened, how to get the Page object for page 5, what to do before getting pages from a PdfReader whose PDF is encrypted with the password swordfish, how to rotate a page counterclockwise, which method returns a Document for demo.docx, the difference between a Paragraph and a Run, how to get the list of paragraphs, which type of object has bold, underline, italic, strike and outline variables, what the values True, False and None of bold mean, how to create a new Document, how to add a paragraph and which integers are heading levels [S].",
 "The code answers were run and the conceptual ones were matched to the chapter's text (This study, 2026). Two answers need a caveat in the course: question 4, because rotate(-90) is stored as -90 and not as 270, and question 8, because in python-docx 1.2.0 only bold, italic and underline are variables of a Run and strike and outline belong to run.font.")

# ---- the leaves: PdfFormat ----
_b('HeaderAndTrailer',
 "A PDF file begins with a header line such as %PDF-1.4 and ends with the keyword startxref, the byte offset of the cross-reference table and the marker %%EOF; the standard says a reader finds the table by reading from the end of the file [ISO][LOC]. The chapter never opens a PDF as bytes, since PyPDF does it [S].",
 "A two-page file written for the study began with %PDF-1.4, ended with %%EOF, and its startxref offset pointed at the bytes xref. The file passed qpdf --check and pypdf read two pages from it (This study, 2026).")
_b('CrossReferenceTable',
 "The cross-reference table lists, for each numbered object of the file, the byte offset at which the object starts and whether it is in use; entry 0 is the head of the list of free objects [ISO]. A reader that has the table can jump to any page without reading the whole file [LOC].",
 "The table of the two-page file had 8 entries, the first free, and the offsets of entries 1 to 3 pointed at the text 1 0 obj, 2 0 obj and 3 0 obj. That is why a file cut off before its table cannot be opened, as the damaged-input leaf shows (This study, 2026).")
_b('ContentStreamText',
 "The chapter extracts the text of a page with extract_text(), and the PDF standard says the text of a page is a content stream of drawing commands: BT begins a text object, Tf selects a font and size, Td moves to a position, Tj shows a string and ET ends it [S][ISO].",
 "For the page of the study the stream was BT /F1 18 Tf 72 720 Td (Page one) Tj ET, and get_contents().get_data() returned those bytes exactly. The words are placed at coordinates and nothing in the stream says that they form a sentence or a paragraph (This study, 2026).")
_b('ProducerMetadata',
 "A PDF may carry document information such as the producer and creation date; the chapter does not read metadata, and the pypdf documentation says the reader's metadata attribute gives it [S][PD]. A file that a library writes records the library as its producer.",
 "The file written by hand had no metadata (None). After pypdf appended its page to a PdfWriter and wrote the result, the metadata held only the producer, pypdf. The shipped sample chapter says Adobe PDF Library 16.0.5, and the first_five_pages.pdf the chapter writes says pypdf (This study, 2026).")
_b('TextOrderIsStreamOrder',
 "The chapter's list of subjective decisions starts with where paragraphs end and begin and does not mention the order of the text [S]. The standard lets a page draw its strings in any order, because each Td or Tm command says where the next string goes [ISO].",
 "A page drew (world) at x 200 first and (Hello) at x 72 second. extract_text() returned worldHello, the stream order, and the layout mode returned Hello and world on one line, ordered by position. A program that needs reading order must ask for the layout mode (This study, 2026).")
_b('ScannedPageNoText',
 "The chapter says PyPDF may make mistakes when extracting text and may even fail to open some PDFs, and does not say what a scanned document gives [S]. A scan is an image on a page with no text commands, so there is nothing to extract; recognising the letters of a picture is a different task from the one extract_text() does.",
 "A page made from a 40 by 40 pixel image had one page, an empty string from extract_text() and one image, image.jpg. The shipped sample chapter is not a scan: it gave 32,981 characters (This study, 2026).")
_b('RedactionByOverlay',
 "The chapter shows how to lay one page over another with merge_page(), and a black rectangle drawn over text is the same kind of overlay [S]. Wikipedia says that where text is redacted in a PDF by overlaying graphical elements, usually black rectangles, the original text remains in the file and can be uncovered by deleting the overlay [WP].",
 "A page drew Salary: 120000 USD and then filled a black rectangle over it with the command re f. extract_text() still returned the salary and the stream still held the rectangle command; pdftotext also read the text. A redaction must remove the text from the stream, not cover it (This study, 2026).")
_b('NoParagraphsInPdf',
 "The chapter asks where paragraphs in the PDF should end and begin, and answers that these are subjective decisions of the extraction [S]. A PDF stores each string where it is drawn, so a paragraph exists only as a group of lines that a human sees [ISO].",
 "Two drawing commands one row apart extracted as Hello and world on two lines, while the same words in one command extracted as Hello world. The line breaks of extracted text are decisions of the library from positions, which is why the chapter suggests a language model to clean the text (This study, 2026).")

# ---- PdfTextAndImages ----
_b('PdfReaderPages',
 "After import pypdf the chapter opens the file in binary read mode and passes it to PdfReader; the pages attribute holds the Page objects, len(reader.pages) gives their number and the loop for page in reader.pages visits them in order [S][PD].",
 "For a six-page file len(reader.pages) was 6 and the type was the library's own _VirtualList. The index -1 reached the last page and the slice [1:3] gave pages two and three, so pages behaves like a list. The shipped sample chapter has 18 pages (This study, 2026).")
_b('PageIndexIsZeroBased',
 "Practice question 2 asks how to get the Page object for page 5, and the chapter counts page indexes from 0 when it says the tuple (0, 5) copies pages from page index 0 up to but not including page index 5 [S].",
 "In the six-page file pages[4] was Page 5 and pages[6] raised IndexError with the message Sequence index out of range. The same holds for a PdfWriter, and the sample chapter has no page index 18 (This study, 2026).")
_b('JoinedPagesNoSeparator',
 "The chapter's extraction listing sets text to an empty string and, for each page, adds the text of the page with +=, then writes the result to a file [S]. extract_text() returns the text of one page without a trailing newline or a page marker [PD].",
 "Six pages gave Page 1Page 2Page 3Page 4Page 5Page 6. On the shipped chapter the end of page 1, Al Sweigart, and the start of page 2, 2 and Chapter 1, ran together as Al Sweigart2. A program that wants page boundaries must join the texts with a separator of its own (This study, 2026).")
_b('LayoutMode',
 "The chapter calls extract_text() with no argument. The pypdf documentation shows extraction_mode='layout', which extracts text in a fixed-width format that closely adheres to the rendered layout of the source PDF [PD].",
 "A page with Name and Price on one row and Tea and 3 on the next gave Name Price and Tea 3 by default, and in the layout mode the gap between the columns was kept as runs of spaces, so the numbers stand under their headings. The chapter does not mention the mode (This study, 2026).")
_b('PdfminerAlternative',
 "When PyPDF cannot understand an unconventional file the chapter turns to pdfminer.high_level, whose extract_text() function takes the filename and returns the whole text as one string, written to a file [S][MN].",
 "On the six-page file pdfminer.six returned Page 1 followed by blank lines and a form feed after every page, 6 in all. On the shipped chapter it returned 33,200 characters against 32,981 for pypdf and spaced the chapter heading out as W H A T I S (This study, 2026).")
_b('DamagedInput',
 "The chapter says PyPDF may fail to open some PDFs and that the author has not met one it could not open [S]. The fallback it offers is pdfminer.six [S][MN].",
 "A six-page file cut off before its cross-reference table raised PdfStreamError in pypdf and PDFSyntaxError in pdfminer.six; an empty file raised EmptyFileError in pypdf. Of eleven damaged files the study made, none was refused by pypdf and read by pdfminer.six, and both libraries refused four of them (This study, 2026).")
_b('TextPostProcessing',
 "The chapter prints the extracted text of a page with a newline at the end of every printed row and the word following split by a hyphen across two rows, and suggests a language model prompt that puts paragraphs on a single line and removes the hyphens and the headers [S]. The pypdf documentation says post-processing is outside the scope of pypdf, calls it a natural language processing task and shows ligature replacement and dehyphenation as examples [PD].",
 "A page with follow- on one row and ing the execution on the next extracted as follow-, a newline, ing the execution, and re.sub of a hyphen and a newline gave following the execution. That repair is deterministic where the language model is not, and the model call itself was NOT EXECUTED (This study, 2026).")
_b('ImagesNeedPillow',
 "The chapter's image listing loops over page.images and writes image.data to a file, and its text does not say that the attribute needs a second package [S]. The pypdf installation page says that for image extraction you need Pillow, installed with the image extra [PD].",
 "With Pillow made unavailable, reading the first image raised ImportError, pillow is required to do image extraction. In an environment with pypdf alone the same page gave 7 images in len(page.images) and the same error as soon as one was read (This study, 2026).")
_b('ImageNameAndData',
 "Each item of page.images is an image object whose name attribute is a filename and whose data attribute holds the bytes of the file; the chapter writes the data to a file named from the counter, the page number and the name [S][PD].",
 "The picture on the scanned page was named image.jpg, its data began with FF D8, the marker of a JPEG file, and the image attribute gave a Pillow JpegImageFile of 30 by 30 pixels. On the shipped chapter page 1 gave Im0.jpg and Im1.png among 7 images, and page 7 a TIFF (This study, 2026).")
_b('ImageNamesRepeat',
 "The chapter writes each image to a file named with a running number, the page number and the image's name, for example 0_page1_Im0.jpg, and does not say why the number is needed [S].",
 "Two pages that carried the same picture both listed image.jpg, so a name alone would have overwritten the first file with the second. The running number is what keeps the 11 files of the shipped chapter apart (This study, 2026).")

# ---- PdfWriting ----
_b('PdfWriterStartsEmpty',
 "The chapter creates a new PDF with pypdf.PdfWriter(): the object starts with no pages and receives pages copied from other files with append() and merge(), never text typed in; write() saves it to a file opened in binary write mode [S][PD].",
 "A new PdfWriter held 0 pages, and after append() of the six-page file it held 6. To create text from nothing one needs another package, such as reportlab, which the chapter does not cover (This study, 2026).")
_b('AppendRangeTuple',
 "The chapter calls writer.append('Recursion_Chapter1.pdf', (0, 5)) and explains that the tuple tells the PdfWriter to copy pages starting at page index 0, up to but not including page index 5 [S][PD].",
 "The six-page file copied with (0, 5) gave Page 1 to Page 5, five pages. The shipped sample chapter gave a five-page first_five_pages.pdf of 966,777 bytes against 2,350,773 for the original (This study, 2026).")
_b('AppendStepTuple',
 "The chapter says that a tuple of three integers adds a step to the range, as in range(), so that (0, 5, 2) copies every second page [S].",
 "The six-page file copied with (0, 5, 2) gave Page 1, Page 3 and Page 5. The same call on the shipped chapter gave 3 pages under all ten interpreters (This study, 2026).")
_b('AppendListOfPages',
 "The chapter says that a list of integers selects exactly the pages it names, where a tuple selects a range, and the difference is the one between range(0, 5) and [0, 5] [S][PD].",
 "The six-page file copied with [0, 5] gave Page 1 and Page 6, two pages. The tuple and the list are the two ways to ask for pages, and mixing them up is a quiet error because both run (This study, 2026).")
_b('AppendOutOfRange',
 "The chapter's examples keep inside the pages of the file, and the sample chapter has 18 pages [S].",
 "A page number past the end of the file, (0, 99) or [0, 99], raised IndexError with the message Sequence index out of range. The error comes from the page list of the source file, so no page is copied by mistake (This study, 2026).")
_b('MergeInsertsAtPosition',
 "The merge() method has an additional integer argument that specifies the position at which the pages are inserted, so the pages that were at and after that position move later [S][PD]. The pypdf documentation gives the keyword pages for the page selection [PD].",
 "A three-page writer received pages (0, 2) of the six-page file at position 1 and held A1, Page 1, Page 2, A2, A3. The call used the keyword pages, which is the form the signature of merge() takes (This study, 2026).")
_b('MergePositionalTupleTrap',
 "The chapter prints writer.merge(2, 'Recursion_Chapter1.pdf', (0, 5)) with the tuple as the third positional argument and shows no output [S]. The signature of merge() in pypdf 6.20.1 is position, fileobj, outline_item, pages [PD].",
 "The tuple went to outline_item: the writer got a bookmark titled (0, 2) and the whole six-page file, 9 pages in all instead of 5; in the shipped chapter case 23 pages instead of 10. pypdf 5.0.1 raised AttributeError, tuple has no attribute startswith. The call must be written with pages= (This study, 2026).")
_b('BlankPageSize',
 "The chapter says that the size of a new blank page will be the same as that of the preceding page, and creates one with add_blank_page() at the end and one with insert_blank_page(index=2) [S][PD].",
 "At the end add_blank_page() took the size of the last page. For the inserted page the size came from the page that follows it: between a 300 by 400 page and a 100 by 100 page the new page was 100 by 100. A blank page in an empty writer raised PageSizeNotDefinedError (This study, 2026).")
_b('InsertBlankPageArguments',
 "The chapter writes insert_blank_page(index=2) with the keyword, and the signature of the method is width, height, index in that order [S][PD].",
 "A call insert_blank_page(2) made a page 2 points wide, because the first positional argument is the width, and index=2 made a page of the normal 612 points; the writer grew from 6 to 8 pages. The keyword is therefore not a style choice (This study, 2026).")
_b('RotateMultiplesOf90',
 "The chapter rotates pages with the rotate() method of Page objects: 90, 180 or 270 turn the page clockwise and -90, -180 or -270 counterclockwise [S][PD].",
 "rotate(90) changed the page in place, returned the page object and left the rotation at 90; rotate(45) raised ValueError, Rotation angle must be a multiple of 90. The rotation is stored in the /Rotate entry and the content stream is not changed (This study, 2026).")
_b('RotationAccumulates',
 "Practice question 4 asks how to rotate a page counterclockwise, and the answer in the chapter's own text is a negative angle [S].",
 "Calls add up and the total is not reduced to a turn: 90, 270, -90 and 180 gave 90, 360, 270 and 450. A program that compares rotations must reduce the value modulo 360 itself (This study, 2026).")
_b('WatermarkUnderlay',
 "The chapter merges a one-page watermark PDF into each page with merge_page() and the keyword over=False, so the watermark goes under the text, and notes that the default puts it over [S][PD]. Figure 17-3 shows the result [S].",
 "A page drawn with BASE and a page with MARK merged with over=False drew MARK before BASE, so the mark is below, and with the default over=True drew BASE and then MARK. On the shipped watermark.pdf the text of page 1 gained blank lines in front of its first line (This study, 2026).")
_b('MergePageInPlace',
 "The chapter calls page.merge_page(watermark_page, over=False) and then adds the page to the writer, without using a return value [S].",
 "merge_page() returned None and changed the page it was called on; the text of the merged page was BASEMARK. A program that wants to keep the original page must copy it first (This study, 2026).")
_b('EncryptRc4Default',
 "The chapter says the encrypt() method accepts a password and a string that selects the algorithm and that it will always use AES-256; the call without an algorithm is not shown [S]. The pypdf documentation names the algorithms that encrypt() offers [PD].",
 "encrypt('swordfish') without an algorithm wrote RC4 with a 128-bit key: encryption version V 2, revision R 3. qpdf reported R = 3 and no named method. The pypdf installation page says encryption using RC4 is supported by the regular installation and AES needs the crypto extra; the default of the library is the form the chapter never shows (This study, 2026).")
_b('EncryptAes256',
 "The chapter calls writer.encrypt('swordfish', algorithm='AES-256') and says the argument implements a recommended modern encryption algorithm [S][PD].",
 "The file written with AES-256 carried V 5, R 6 and the crypt filter method AESV3, which qpdf reported as AESv3. Two files written from the same writer differed in bytes because of random salts (This study, 2026).")
_b('DecryptReturnValues',
 "The chapter enters is_encrypted, then decrypt('an incorrect password').name, then decrypt('swordfish').name, and explains that decrypt() returns a PasswordType object whose name is NOT_DECRYPTED, USER_PASSWORD or OWNER_PASSWORD [S][PD].",
 "With a user password and an owner password the right user password gave USER_PASSWORD, the owner password OWNER_PASSWORD, and a wrong one, an empty one and a differently capitalised one gave NOT_DECRYPTED. None raised an error (This study, 2026).")
_b('ReaderRefusesBeforeDecrypt',
 "Practice question 3 asks what to do before obtaining Page objects from an encrypted PdfReader, and the answer is to call decrypt() with the password [S].",
 "For an encrypted file is_encrypted was True and pages[0] raised FileNotDecryptedError, File has not been decrypted. The file the study encrypted with one password returned OWNER_PASSWORD, and after that pages[0] gave Secret. The error also arises when append() is given the path of an encrypted file (This study, 2026).")
_b('EmptyUserPassword',
 "The chapter explains that a PDF can have a user password that allows viewing and an owner password that sets permissions for printing, commenting and extracting text [S]. A reader opens such a file without being given a password.",
 "A file encrypted with an empty user password and the owner password owner was encrypted (is_encrypted True) and still gave its text with no decrypt() call; decrypt('owner') returned OWNER_PASSWORD. The file therefore protects the permissions and not the reading (This study, 2026).")
_b('RemovedNames',
 "The chapter uses PdfReader and PdfWriter, and many tutorials use PdfFileReader, PdfFileWriter and PdfMerger, and the pypdf changelog records the removal of PdfMerger in 5.0.0 [S][PD].",
 "In pypdf 6.20.1 hasattr gave False for PdfFileReader, PdfFileWriter and PdfMerger and True for PdfReader and PdfWriter; in 5.0.1 the name PdfMerger existed and raised a DeprecationError when called. The camelCase methods getPage, numPages and addBlankPage are gone as well (This study, 2026).")
_b('WriteNeedsBinaryFile',
 "Practice question 1 asks in what modes the file of a PdfWriter is opened to save the PDF, and the chapter's listings open files with 'wb' [S].",
 "write() with a file opened in text mode raised TypeError, write() argument must be str, not bytes, and in mode 'wb' it wrote. The same holds for image data, which is bytes (This study, 2026).")

# ---- WordDocuments ----
_b('DocxIsZipOfXml',
 "The chapter says .docx files have many structural elements which Python-Docx represents with three data types, and does not say what a .docx file is on disk [S]. Office Open XML packages a document as a ZIP archive of XML parts, and a ZIP file usually starts with the bytes PK, the initials of its inventor Phil Katz [LOC2][WP].",
 "A new document saved by python-docx began with PK and 03 04, held 17 parts including word/document.xml and three relationship files ending in .rels, and could be opened with the zipfile module. The shipped demo.docx has 16 parts (This study, 2026).")
_b('DocumentXmlBody',
 "The paragraphs, runs and text that the chapter names are elements of word/document.xml: w:p for a paragraph, w:r for a run and w:t for the text of a run [LOC2][DX].",
 "For add_paragraph('Hello, world!') the body held <w:p><w:r><w:t>Hello, world!</w:t></w:r></w:p>. The structure of the XML is the structure of the three data types: a Document holds paragraphs, a paragraph holds runs (This study, 2026).")
_b('DefaultTemplate',
 "The chapter creates a new document with docx.Document() and says the result has no paragraphs (practice question 10) [S]. The python-docx documentation says a new document is created from a default template that the package ships [DX].",
 "The new document had 0 paragraphs, 1 section and more than 100 styles, its core properties named the author python-docx and the year 2013, and the template is the origin of the 164 styles of the next leaves. A file made this way carries those properties unless the program changes them (This study, 2026).")
_b('ParagraphsOfBody',
 "The chapter's get_text() function and its shell session read doc.paragraphs, a list of Paragraph objects, and join the text attribute of each; practice question 7 asks how to obtain that list [S][DX].",
 "The attribute gave a list, in body order, of one, two and an empty string; an empty paragraph counts and so the joined text ends with a newline. The shipped demo.docx has 7 paragraphs and the last one is empty, which the chapter's six printed lines do not show (This study, 2026).")
_b('RunsSplitAtFormatting',
 "The chapter says each Paragraph object contains a list of one or more Run objects and that the single-sentence paragraph of Figure 17-4 has four runs; it prints the run texts as 'A plain paragraph with some ', 'bold', ' and some ' and 'italic' [S].",
 "A paragraph built with the same four parts gave the texts 'A plain paragraph with some ', 'bold', ' text and some ' and 'italic', bold None, True, None, None and italic None, None, None, True. The third text in the shipped demo.docx has the word text, which the chapter's printed ' and some ' lacks (This study, 2026).")
_b('TablesAndHeadersApart',
 "The chapter says a Document object contains a list of Paragraph objects for the paragraphs in the document, and its get_text() function reads only those [S]. The python-docx documentation puts tables in doc.tables and headers in the sections [DX].",
 "With a table and a header present doc.paragraphs held only the body paragraph. The table text came from the cell and the header text from the header of the first section, so a function that claims the full text of a document must read all three places (This study, 2026).")
_b('HyperlinkTextAndRuns',
 "The chapter says a paragraph is a list of runs and that its text attribute is the joined text of them [S]. A hyperlink in Word is an element of its own that contains runs, and the python-docx documentation describes paragraph.runs as the runs directly in the paragraph [DX].",
 "A paragraph made of before and a hyperlink containing linked had the text before linked in python-docx 1.2.0, while its runs listed only before. Code that rebuilds a paragraph from its runs loses the link text (This study, 2026).")
_b('StyleKindsOfTemplate',
 "The chapter says Word documents contain three types of styles, paragraph, character and linked, and prints 34 default style names [S]. The python-docx documentation distinguishes paragraph, character, table and numbering (list) styles [DX].",
 "The template of a new document has 164 styles: 27 character, 1 list, 36 paragraph and 100 table styles. No kind is called linked; a linked style is a paragraph style with a character style that goes with it, the Quote and Quote Char of the chapter (This study, 2026).")
_b('StyleKindMismatch',
 "The chapter says to set the style attribute of a Paragraph or Run to the name of the style, and that for a linked style a run uses the name with Char added, paragraphObj.style = 'Quote' and runObj.style = 'Quote Char' [S].",
 "'Quote Char' on a paragraph and 'Quote' on a run raised ValueError, assigned style is type CHARACTER (2), need type PARAGRAPH (1), and the reverse; the two correct forms were accepted. The error message names the two types (This study, 2026).")
_b('UnknownStyleKeyError',
 "The chapter prints the default style names in a table of strings, among them 'List Number ' with a space before the closing quote, and tells the reader to use those strings [S].",
 "add_paragraph('x', 'List Number ') raised KeyError, no style with name 'List Number ', while 'List Number' was accepted; an unknown name raised the same error. The trailing space of the page is an artefact of the table layout (This study, 2026).")
_b('StyleIdLookupDeprecated',
 "The default names the chapter prints include 'MacroText', which in the template is not a name [S]. The python-docx documentation says styles are looked up by name and that a style also has an id (style_id) in the XML [DX].",
 "The template names the style macro and gives it the id MacroText. add_paragraph('x', 'MacroText') worked and warned, style lookup by style_id is deprecated, and the name Macro Text is not among the styles. All ten interpreters gave the same warning (This study, 2026).")
_b('CustomParagraphStyle',
 "The chapter says that to create custom styles one uses the Word application to define them and then reads them from the style attribute of a Paragraph or Run object; the Custom Invitations program asks the reader to add styles to a blank Word file first [S].",
 "styles.add_style('Invitation Name', WD_STYLE_TYPE.PARAGRAPH) made a paragraph style with base Normal, 24 points and bold, and add_paragraph used it by name. The practice program needs no hand-made template file (This study, 2026).")

# ---- WordWriting ----
_b('AddParagraphReturnsParagraph',
 "To write a document the chapter calls docx.Document() and then doc.add_paragraph('Hello, world!'), and saves it with doc.save('helloworld.docx'); Figure 17-7 shows the file [S][DX].",
 "The call returned a Paragraph with the text Hello, world! and the style Normal, and doc.paragraphs then held it as the only entry. LibreOffice 24.2 converted the saved file to one PDF page showing the text (This study, 2026).")
_b('AddRunAppends',
 "The chapter adds a second paragraph and then a run to it, calling add_run() with the text to append, and notes that both add_paragraph() and add_run() accept an optional second argument for the style [S][DX]. Figure 17-8 shows the result [S].",
 "add_run() returned a Run and the paragraph's text was the two strings joined, Hello world! This text is being added to the second paragraph., with 2 runs. A run keeps its own formatting while the paragraph holds its text (This study, 2026).")
_b('AddHeadingLevels',
 "The chapter calls add_heading('Header 0', 0) through level 4 and says the arguments are the heading text and an integer ranging from 0 to 4, where 0 is the Title style and the integers 1 to 9 are headings of decreasing size [S][DX]. Practice question 12 asks which integers are the levels [S].",
 "add_heading accepted 0 to 9: 0 gave Title, 1 gave Heading 1, 4 gave Heading 4 and 9 gave Heading 9. -1 and 10 raised ValueError, level must be in range 0-9, and the string '1' raised TypeError. The range 0 to 4 in the chapter's sentence is what its example uses, not what the method accepts (This study, 2026).")
_b('TriStateBold',
 "The chapter says each text attribute can be set to True, always enabled, False, always disabled, or None, which defaults to whatever the style of the run says [S][DX].",
 "A new run's bold was None and wrote nothing. True wrote <w:b/>, False wrote <w:b w:val=0/> and None removed the element again, so the three values are three states of the XML (This study, 2026).")
_b('UnderlineValues',
 "The underline attribute is the one of the three Run attributes that takes more than True and False: the python-docx documentation says it accepts a member of the WD_UNDERLINE enumeration for the kinds of underline [DX].",
 "True wrote single, WD_UNDERLINE.DOUBLE wrote double and False wrote none in the w:u element. After assigning DOUBLE the attribute read back as the enumeration member and not as True (This study, 2026).")
_b('RunVersusFontAttributes',
 "Table 17-1 lists twelve attributes under the heading of text attributes that can be set on Run objects: bold, italic, underline, strike, double_strike, all_caps, small_caps, shadow, outline, rtl, imprint and emboss [S]. Practice question 8 asks what type of object has bold, underline, italic, strike and outline variables [S].",
 "Looking the names up in python-docx 1.2.0, only bold, italic and underline are attributes of Run, and all twelve are attributes of run.font. The documentation of the Font class lists them [DX]. The table is correct for the font of a run and wrong for the run (This study, 2026).")
_b('UnknownRunAttributeIgnored',
 "The chapter's sentences about Table 17-1 tell the reader to set the attributes on Run objects, for instance runObj.strike = True [S].",
 "run.strike = True raised no error, and font.strike stayed None with no element in the XML; run.font.strike = True set it and wrote w:strike. A Python object accepts a new attribute without complaint, so the mistake shows only in the output document. All ten interpreters gave the same result (This study, 2026).")
_b('PageBreakRun',
 "To add a page break the chapter calls add_break() on the Run object after which the break should appear, passing docx.enum.text.WD_BREAK.PAGE, and describes a second page that begins with This is on the second page! [S][DX].",
 "The break is a run holding <w:br w:type=page/>. Both run.add_break(WD_BREAK.PAGE) and add_page_break() wrote one, and add_page_break() added a paragraph of its own. LibreOffice 24.2 counted 2 pages for the file of the chapter and showed both texts (This study, 2026).")
_b('NewlineBecomesBreak',
 "The chapter says that to add a line break rather than a new paragraph one calls add_break() on a run [S]. The python-docx documentation says that a newline or a tab in the text assigned to a run is turned into a break or a tab element [DX].",
 "A run with the text a, a tab, b, a newline and c held <w:tab/> and <w:br/> in its XML and gave the same characters back from its text attribute. A newline in the text of a run is therefore a line break, not a new paragraph (This study, 2026).")
_b('PictureSizeFromWidth',
 "The chapter calls doc.add_picture('zophie.png', width=docx.shared.Inches(1), height=docx.shared.Cm(4)) and says it is easier to give the width and height in inches and centimetres than in the units of the file [S][DX].",
 "With neither a size nor resolution recorded the picture took the size of its pixels at 72 per inch; with a width alone the height followed the aspect ratio; with both the picture was stretched to the sizes, so the ratio changed. The shipped zophie.png, 816 by 1088 pixels, gave 0.635 in ratio with Inches(1) and Cm(4) against 0.75 for the image (This study, 2026).")
_b('EmuUnits',
 "docx.shared.Inches() and docx.shared.Cm() return lengths, and the python-docx documentation says lengths are integers in English Metric Units, 914,400 to the inch [DX].",
 "Inches(1) was 914400, Cm(1) was 360000 and Pt(1) was 12700, and Inches(1).inches was 1.0. A width given as a bare integer is read as EMU, so add_picture(width=1) makes a picture about a millionth of an inch wide (This study, 2026).")
_b('PictureStoredOnce',
 "Each add_picture() call adds a paragraph with a picture, and the chapter's own session adds one picture (Figure 17-9 shows headings and Figure 17-10 shows the invitation file) [S].",
 "Three calls with identical bytes gave 3 paragraphs and 3 inline shapes but one media part, word/media/image1.png, equal to the bytes given. The shipped zophie.png of 1,287,443 bytes was stored once in a file with three pictures (This study, 2026).")

# ---- ToolsAndPractice ----
_b('PackageNameTrap',
 "The chapter says to install Python-Docx, not Docx, which belongs to a different package that the book does not cover, and to run import docx, not import python-docx [S]. PyPI shows the project docx at version 0.2.4, released on 6 February 2014 [PYPI].",
 "The environment held python-docx 1.2.0 and pypdf 6.20.1 and no distribution named docx or PyPDF2. Installing docx 0.2.4 under Python 3.14.6 made import docx fail with ModuleNotFoundError: No module named exceptions (This study, 2026).")
_b('OptionalDependencyAes',
 "The chapter says to follow Appendix A to install PyPDF [S][APPA]. The pypdf installation page says encryption with RC4 is supported by the regular installation, and AES needs the crypto extra, which installs the cryptography package [PD].",
 "Without cryptography the default RC4 file was written, AES-128 failed at write() and AES-256 failed at encrypt(), both with DependencyError, cryptography>=3.1 is required for AES algorithm. The chapter's own call, AES-256, is the one that fails first (This study, 2026).")
_b('CombineAllPdfs',
 "Project 12 finds the PDF files of the working directory with os.listdir('.'), sorts them with pdf_filenames.sort(key=str.lower), creates a PdfWriter and, for each file, copies all pages after the first, then saves the output [S].",
 "With the name pdf_filenames used in the loop, the three small files gave combined.pdf with A2, B2 and B3, and the one-page file added nothing, as the page range (1, number of pages) is empty for it. A second run would read combined.pdf as input (This study, 2026).")
_b('CaseInsensitiveSort',
 "Step 1 of Project 12 calls the sort() list method on pdf_filenames with the argument key=str.lower, so that the filenames are alphabetized without regard to case [S][PY].",
 "Sorting Mango.pdf, Zebra.pdf and apple.pdf gave Mango, Zebra, apple without the key and apple, Mango, Zebra with it. The key function only decides the order, and the names keep their case (This study, 2026).")
_b('WalkFindsAllPdfs',
 "PDF Paranoia asks for os.walk() to go through every PDF in a folder and its subfolders, and Project 12 tests filename.endswith('.pdf') [S][PY].",
 "In a tree with a.pdf, notes.txt, sub/b.pdf and sub/deeper/C.PDF the test with lower() found 3 files and the test the chapter uses found 2. A file with a capital extension is skipped without a message (This study, 2026).")
_b('InvitationPageBreaks',
 "Custom Invitations asks for one invitation per page for each guest, with styles added to a blank Word file [S].",
 "A break after every guest wrote as many breaks as guests and left one empty page at the end in Word terms; a break only between guests wrote one fewer. LibreOffice 24.2 counted 5 pages for 5 guests in both forms (This study, 2026).")
_b('DictionaryAttackBothCases',
 "PDF Password Breaker reads a dictionary of words, passes each to decrypt(), and the chapter says to try both the uppercase and lowercase form of each word; it says the dictionary has over 44,000 words and the program makes about 88,000 attempts [S].",
 "On a four-word list and a file encrypted with BANANA the loop found BANANA after 4 of the 6 possible attempts. The shipped dictionary.txt has 349,900 words, 8.0 times 44,000, so both cases make 699,800 attempts, and the book's password swordfish is not in the dictionary (This study, 2026).")
_b('PracticeAnswersChecked',
 "The twelve questions ask for definitions, and some ask for code that can be run: the index of page 5, the call that returns a Document, the list of paragraphs, the variables of a Run and the heading levels [S].",
 "Executed answers: pages[4] gave Page 5, docx.Document('demo.docx') returned a Document, doc.paragraphs was a list, a new Document had 0 paragraphs, add_paragraph('Hello, there!') returned a Paragraph with that text, and only bold, underline and italic were attributes of a Run. The 'wb' mode of question 1 was confirmed by the TypeError of text mode (This study, 2026).")

PUBS.sort(key=lambda p: p[0])
_CITE = {
 "S": "(Sweigart, 2025)", "APPA": "(Sweigart, 2025, Appendix A)", "PD": "(pypdf contributors, 2026)", "DX": "(Canny, 2013)", "MN": "(pdfminer.six contributors, 2026)",
 "PY": "(Python Software Foundation, 2026)", "ISO": "(Adobe Systems, 2008)", "LOC": "(Library of Congress, 2019)", "LOC2": "(Library of Congress, n.d.)",
 "WP": "(Wikipedia, 2026)", "QP": "(qpdf contributors, 2026)", "CWE": "(MITRE, 2026)", "PYPI": "(Python Package Index, 2026)", "T": "(This study, 2026)",
}
for _k in list(BODY):
    _t = BODY[_k]
    for _n, _v in _CITE.items():
        _t = _t.replace("[" + _n + "]", _v)
    BODY[_k] = _t.replace('"', "'")
