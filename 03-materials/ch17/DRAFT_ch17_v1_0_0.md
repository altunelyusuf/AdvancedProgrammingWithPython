# Chapter 17 Draft — PDF and Word Documents (v1.0.0)

**Status note:** checked against live files: deck `SEN0414_Ch17_PDFAndWordDocuments_3e_v2_0_0.pptx` (58 slides), page `sen0414_ch17_page_v9_96_0.html`, manifest `chapter_code_ch17_v1_0_0.json` (28 examples), stories script (6 stories). The page checks pass (Page/Ch17 PASS, 402 features). The chapter went through a real repair cycle in October (page v9_95_0 to v9_96_0), now resolved. For your approval before any render step.

## 1. The story (6 beats, one per concept, sourced)

1. **Spring 1991 — John Warnock, co-founder of Adobe.** Wikipedia's article on John Warnock says that in the spring of 1991 he outlined a system called Camelot, inventing the Portable Document Format. The goal of Camelot, the article quotes, was to capture documents from any application, send electronic versions of them anywhere, and view and print them on any machine. Adobe released the first Acrobat on 15 June 1993. A PDF file made today still opens with a header line and ends with an offset and %%EOF, and its text is drawing commands that place words on a page; chapter 17 reads and rewrites exactly these files with pypdf. *Lesson: A PDF is a page description made to look the same everywhere.* (https://en.wikipedia.org/wiki/John_Warnock)

2. **14 February 1989 — Phil Katz of PKWARE and Gary Conway of Infinity Design Concepts.** Wikipedia's article on the ZIP file format gives 14 February 1989 as the initial release and says the format was designed by Phil Katz of PKWARE and Gary Conway of Infinity Design Concepts, after Systems Enhancement Associates sued PKWARE over its archiving products. The first two bytes of a ZIP file are usually PK, the initials of Phil Katz. Office Open XML is one of the formats listed as extended from ZIP. In this study a new python-docx document began with the bytes PK and held 17 parts, among them word/document.xml, which is why a .docx file can be opened with the zipfile module. *Lesson: A .docx file is a ZIP archive of XML parts.* (https://en.wikipedia.org/wiki/Zip_(file_format))

3. **7 December 2006 and November 2008 — Microsoft, Ecma International and ISO/IEC Joint Technical Committee 1.** Wikipedia's article on Office Open XML gives 7 December 2006 as the initial release, as the first edition of ECMA-376. After a first failed vote, an amended version won approval as an ISO/IEC standard in a fast-track process that ended in April 2008. The four-part standard, ISO/IEC 29500:2008, was published in November 2008. The .docx files that python-docx writes follow this format. In this study the template a new document starts from still carried the author python-docx and the year 2013. *Lesson: The .docx format is a published standard, not a secret.* (https://en.wikipedia.org/wiki/Office_Open_XML)

4. **November 2006 and July 2008 — Adobe Systems and the International Organization for Standardization.** The Library of Congress describes PDF 1.7 in its Sustainability of Digital Formats pages. The page says version 1.7 was released in November 2006 with Acrobat and Adobe Reader 8.0, and that it was published as ISO 32000-1 in July 2008. The standard defines the pieces this study took apart in a small file: the header, the numbered objects, the cross-reference table and the trailer. A reader finds the table by reading the last lines, so pypdf can open a file by jumping to the end first. *Lesson: PDF is a public standard with a table at the end.* (https://www.loc.gov/preservation/digital/formats/fdd/fdd000277.shtml)

5. **2005 to 2023 — Mathieu Fenniak, Phaseit, Martin Thoma and the pypdf contributors.** The pypdf documentation tells that Mathieu Fenniak launched pyPdf in 2005, whose last release was 1.13 in 2010. At the end of 2011 Phaseit sponsored PyPDF2 as a fork, and Martin Thoma took over its maintenance in April 2022. PyPDF2 was then merged back into pypdf, all lowercase and without a number. Old tutorials still use PdfFileReader and PdfMerger; in this study pypdf 6.20.1 has neither name, and merge() took the tuple the chapter passes as the title of a bookmark, (0, 2), and inserted the whole file. *Lesson: Check the library's release before copying an old tutorial.* (https://pypdf.readthedocs.io/en/stable/meta/history.html)

6. **6 February 2014 — The authors of the docx package and Steve Canny, who is credited on its page.** The page of the docx project on PyPI shows version 0.2.4 as its latest release, dated 6 February 2014, still offering pip install docx. Chapter 17 says to install Python-Docx, not Docx, and to write import docx. This study installed docx 0.2.4 in Python 3.14.6 and the import failed with ModuleNotFoundError: No module named exceptions, a module of Python 2. The working package, python-docx, was at version 1.2.0 when it was released on 16 June 2025. *Lesson: Install python-docx, import docx, and read the project page first.* (https://pypi.org/project/docx/)


## 2. Slide / page-tab outline (58 slides, 28 code examples; the example number is the page-tab order)

| Slide | Title | Code example |
|---|---|---|
| 1 | >>> |  |
| 2 | Today's route |  |
| 3 | Two questions this chapter answers |  |
| 4 | Part 1: What a PDF holds |  |
| 5 | Everyday pictures: a PDF and its reader |  |
| 6 | Story: A 1991 memo called Camelot started the PDF |  |
| 7 | Inside a small PDF: header, objects, table, trailer | 1: Inside a small PDF |
| 8 | PdfReader: pages, their size and whether the file is locked | 2: PdfReader, pages and page size |
| 9 | Extracting text: what comes out, and what a black box hides | 3: Extracting text: stream order and the black box |
| 10 | Everyday pictures: text and images |  |
| 11 | Post-processing: mend the text before anyone reads it | 4: Post-processing extracted text |
| 12 | Extracting images: a scanned page is a picture without text | 5: Extracting images, and a page with no text |
| 13 | Story: In July 2008 PDF became an international standard |  |
| 14 | Part 2: New PDFs from pages |  |
| 15 | Everyday pictures: building a new PDF |  |
| 16 | Copying pages into a new file: a tuple is a range, a list is exact | 6: Copying pages: a tuple is a range |
| 17 | merge() puts pages inside; blank pages fill gaps | 7: merge() and blank pages |
| 18 | Rotating pages: angles add up and must be multiples of 90 | 8: Rotating pages |
| 19 | Everyday pictures: stamps and padlocks |  |
| 20 | Watermarks and overlays: merge_page lays one page on another | 9: Watermarks and overlays |
| 21 | Encrypt, then decrypt: a locked file refuses its pages | 10: Encrypt and decrypt |
| 22 | Everyday pictures: two keys, and Project 12 |  |
| 23 | Two passwords: the user opens, the owner may do more | 11: User and owner passwords |
| 24 | Which lock was used: RC4 by default, AES when asked | 12: Which lock was used |
| 25 | Everyday pictures: folders and the program |  |
| 26 | Project 12, step 1: find all PDF files and sort them | 13: Project 12, step 1: find the PDF files |
| 27 | Project 12, steps 2 and 3: open each PDF, copy, save | 14: Project 12, steps 2 and 3: combine and save |
| 28 | Part 3: Reading Word documents |  |
| 29 | Everyday pictures: a Word file |  |
| 30 | Story: The ZIP format of 1989 is the box every .docx comes in |  |
| 31 | A .docx file is a ZIP archive of XML parts | 15: A .docx file is a ZIP of XML |
| 32 | Reading a Word file: paragraphs hold runs | 16: Paragraphs and runs |
| 33 | Getting the full text from a .docx file | 17: Getting the full text of a .docx file |
| 34 | Everyday pictures: paragraphs, runs and styles |  |
| 35 | Styles: a paragraph style and a run style | 18: Styles: paragraph kind and run kind |
| 36 | Styles: the right kind and the exact name | 19: Styles: the kind and the exact name |
| 37 | Everyday pictures: bold, italic and underline |  |
| 38 | Run attributes: bold, italic and underline have three states | 20: Run attributes: three states |
| 39 | Story: Word's .docx format became a standard in 2006 and 2008 |  |
| 40 | Part 4: Writing Word documents |  |
| 41 | Everyday pictures: writing a Word file |  |
| 42 | Writing a Word file: add_paragraph and add_run | 21: Writing paragraphs and runs |
| 43 | Adding headings: levels 0 to 9 | 22: Adding headings |
| 44 | Adding line breaks and page breaks | 23: Line and page breaks |
| 45 | Everyday pictures: pictures and sizes |  |
| 46 | Adding pictures: width and height in inches or centimetres | 24: Adding pictures |
| 47 | Story: pip install docx has not worked since 2014 |  |
| 48 | Part 5: Practice programs |  |
| 49 | Everyday pictures: the practice programs |  |
| 50 | Practice program 1, part 1: walk a folder tree for PDFs | 25: Practice program: PDF Paranoia, walk the tree |
| 51 | Practice program 1, part 2: lock a copy, check it, remove the original | 26: Practice program: PDF Paranoia, lock and check |
| 52 | Practice program 2: Custom Invitations | 27: Practice program: Custom Invitations |
| 53 | Practice program 3: PDF Password Breaker | 28: Practice program: PDF Password Breaker |
| 54 | Which call does what, and what it needs |  |
| 55 | What differs from the book today |  |
| 56 | Summary |  |
| 57 | Practice Questions |  |
| 58 | Resources: where to go next |  |

## 3. Resources slide (14 links, targets read from the deck's own hyperlinks)

1. https://automatetheboringstuff.com/3e/chapter17.html
2. https://pypdf.readthedocs.io/en/stable/
3. https://pypdf.readthedocs.io/en/stable/user/extract-text.html
4. https://pypdf.readthedocs.io/en/stable/user/merging-pdfs.html
5. https://pypdf.readthedocs.io/en/stable/user/encryption-decryption.html
6. https://pypdf.readthedocs.io/en/stable/user/add-watermark.html
7. https://pypdf.readthedocs.io/en/stable/meta/history.html
8. https://python-docx.readthedocs.io/en/latest/
9. https://python-docx.readthedocs.io/en/latest/user/styles-using.html
10. https://python-docx.readthedocs.io/en/latest/user/quickstart.html
11. https://www.loc.gov/preservation/digital/formats/fdd/fdd000277.shtml
12. https://www.loc.gov/preservation/digital/formats/fdd/fdd000397.shtml
13. https://docs.python.org/3/library/zipfile.html
14. https://en.wikipedia.org/wiki/John_Warnock

## 4. Open items
- **Gap found (deck only):** the deck has five story slides (6, 13, 30, 39, 47) but the stories script and the page carry six. The pypdf history story (story 5 above: pyPdf 2005, PyPDF2 fork, merged back into pypdf) has no story slide in the deck; it appears only as a resources link. If you approve, the render step adds that story slide (a new deck version, numbering and code-example slide numbers in the manifest shift by one after the new slide; the page is unchanged).
- No legacy duplicate deck to retire.
- `rdodi/` research-artifact folder left untouched (out of scope).
