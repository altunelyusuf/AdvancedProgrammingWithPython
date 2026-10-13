"""Chapter 22 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter was read on automatetheboringstuff.com on 2026-10-13 (an HTTP fetch of https://automatetheboringstuff.com/3e/chapter22.html; the page
returned 200, 40,521 bytes, and its sha256 equals the chapterDigest the book's own chapter ontology records; the commit the course pins was not opened).
The online materials of the 3rd edition (the zip No Starch Press links from its book page, 7,759,877 bytes, sha256
dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916, 91 files, 72 of them Python) were downloaded at run time and hash-checked file by file for
the images and the script of this chapter (ocr-example.png, frankenstein.png, frankenstein_jpn.png, preprocess_ocr.py); neither the zip nor any file of it is kept
in this repository. 53 sources (the chapter, its appendices, the Tesseract, pytesseract, NAPS2 and OCRmyPDF documentation, PyPI, the Python 3.14 documentation,
the Pillow documentation, the ISO 639 pages, the pages of the stories and uv) were each fetched on the same day and answered HTTP 200; the passages the research
relies on were looked for on each page (live observations). Every behaviour was executed under Python 3.14.6 (the newest 3.14 release uv offered) installed with uv
on Ubuntu 24.04 (Linux; the zone of the shell Europe/Istanbul) in dedicated environments: pytesseract 0.3.13 with Pillow 12.3.0, NumPy 2.5.4, opencv-python-headless
5.0.0.93 and PyAutoGUI 0.9.54 (the newest); the pins of Appendix A (pytesseract 0.3.10, Pillow 10.4.0) on 3.14.6 and on 3.13.14; an empty environment; and ocrmypdf
17.13.0 in a venv of its own. The real Tesseract ran in three builds, the apt 5.3.4 and two built from source, 5.5.3 and 4.1.1, with the tessdata_fast, tessdata_best
and legacy tessdata files, and NAPS2 8.5.1 (the .deb) with its own Tesseract 5.5.0; PDFs were read with poppler 24.02.0. The screen scraper ran on a virtual X display
(Xvfb) as a stand-in; nobody saw a real screen. The images were looked at with the file viewer, and what was seen is stated in the sections OpenImage and JapaneseImage. Accuracy numbers are
MEASURED single runs with the Tesseract version named; they are character error rates computed with an edit distance written for the study.
Not executed, and said so where it comes up: Windows and macOS (the installers, Homebrew, the PATH of Windows); the Flatpak of NAPS2; a flatbed scanner; the large
language model step; a real screen with a real browser; the UB Mannheim installer page (it answered 403 through the proxy); the commit the course pins; the final
Python 3.15 (uv offered 3.15.0b4); pytesseract 0.3.4, 0.3.7 and 0.3.8 (no wheels; 0.3.12 does not exist); the text of the PDF embedded in Figure 22-2; and a photograph
(the single request to Wikimedia Commons answered 429).
The chapter's 22 interactive statements of listings 1, 2, 4, 5 and 6 are replayed by sen0414_ch22_thirdparty_v1_0_0.py into 08-tooling/ch22-page/third_party_record_v1_0_0.json;
what the public sites and the shipped files did on the day is in ch22-page/live_observations_v1_0_0.json; what one program printed under eleven interpreters (3.11, 3.12,
3.13, the seven 3.14 releases 3.14.0 to 3.14.6 and 3.15.0b4) and what small programs printed under 14 Pillow releases and three pytesseract releases is in
ch22-page/interpreter_record_v1_0_0.json. A claim not in this file was not made."""
__version__ = "1.0.2"
# 1.0.0 and 1.0.1 of the chapter 22 data module are already committed (the earlier builds of the chapter); this version rebuilds the chapter at the standard of
# chapters 13 to 21: two cross-referenced paragraphs per section, the chapter replayed as printed, the real Tesseract, pytesseract, NAPS2 and OCRmyPDF run in
# several environments, and the public sources as they answered on 2026-10-13. The data module is 1.0.2 because 1.0.0 and 1.0.1 are already committed.
CH = 22
DATE = "2026-10-13"
PYVER = "3.14.6"
TITLE = "Recognizing text in images for an advanced course: chapter 22 and today's Tesseract, pytesseract, NAPS2 and OCRmyPDF"
QUESTION = "What does chapter 22 of the 3rd edition teach about reading text from images with the Tesseract engine and pytesseract (installing, the four lines that read an image, accuracy and preprocessing, other languages, a language model that fixes mistakes) and about making searchable PDFs with NAPS2, which of its printed outputs, listings and statements still hold under Python 3.14.6 with pytesseract 0.3.13 and Pillow 12.3.0, with the pytesseract 0.3.10 and Pillow 10.4.0 that its Appendix A pins, and with the Tesseract builds a reader may have, and what must an advanced course correct or add so that it matches the engines, the data files and the files the book ships?"
CQS = ('Which parts of a program that reads text from pictures can be shown to work, and which can only be shown to fail, on a machine that has no scanner, no real screen and no Windows or macOS, and how large is the spread between engine versions and data files?',
       'Which printed outputs, programs, numbers and statements of the chapter differ in current releases of Python, pytesseract, Pillow and Tesseract, with the versions its appendix pins, with the data files installed, or in the files and pages it points to, and on what source?')
PUBS = [
 ('P01', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 22, Recognizing Text in Images (Al Sweigart, No Starch Press, 2025)', 'https://automatetheboringstuff.com/3e/chapter22.html', True),
 ('P02', 'Online materials of the 3rd edition, zip with 91 files, four of them the files of chapter 22 (No Starch Press, 2025)', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', False),
 ('P03', 'Automate the Boring Stuff with Python, 3rd edition - table of contents (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/', False),
 ('P04', 'Automate the Boring Stuff with Python, 3rd edition - book page (No Starch Press, 2025)', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', False),
 ('P05', 'Appendix A, Installing Third-Party Modules, with the versions the book pins (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixa.html', False),
 ('P06', 'Appendix B, Answers to the Practice Questions (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixb.html', False),
 ('P07', 'Tesseract User Manual, documentation home (Tesseract OCR contributors, 2026)', 'https://tesseract-ocr.github.io/tessdoc/', False),
 ('P08', 'Improving the quality of the Tesseract output (Tesseract OCR contributors, 2026)', 'https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html', False),
 ('P09', 'Tesseract command line usage (Tesseract OCR contributors, 2026)', 'https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html', False),
 ('P10', 'Tesseract data files (Tesseract OCR contributors, 2026)', 'https://tesseract-ocr.github.io/tessdoc/Data-Files.html', False),
 ('P11', 'Tesseract data files in different versions (Tesseract OCR contributors, 2026)', 'https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html', False),
 ('P12', 'Installing Tesseract (Tesseract OCR contributors, 2026)', 'https://tesseract-ocr.github.io/tessdoc/Installation.html', False),
 ('P13', 'Tesseract FAQ (Tesseract OCR contributors, 2026)', 'https://tesseract-ocr.github.io/tessdoc/FAQ.html', False),
 ('P14', 'tesseract(1) manual page, tesseract.1.asc (Tesseract OCR contributors, 2026)', 'https://raw.githubusercontent.com/tesseract-ocr/tesseract/main/doc/tesseract.1.asc', False),
 ('P15', 'Tesseract OCR README (Tesseract OCR contributors, 2026)', 'https://raw.githubusercontent.com/tesseract-ocr/tesseract/main/README.md', False),
 ('P16', 'tessdata_fast README (Tesseract OCR contributors, 2026)', 'https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/README.md', False),
 ('P17', 'tessdata_best README (Tesseract OCR contributors, 2026)', 'https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/main/README.md', False),
 ('P18', 'An Overview of the Tesseract OCR Engine (Ray Smith, Google, 2007)', 'https://research.google/pubs/an-overview-of-the-tesseract-ocr-engine/', False),
 ('P19', 'PyPI JSON metadata of pytesseract (Python Package Index, 2026)', 'https://pypi.org/pypi/pytesseract/json', False),
 ('P20', 'pytesseract README (Pytesseract contributors, 2026)', 'https://raw.githubusercontent.com/madmaze/pytesseract/master/README.rst', False),
 ('P21', 'pytesseract.py, the source of the wrapper (Pytesseract contributors, 2026)', 'https://raw.githubusercontent.com/madmaze/pytesseract/master/pytesseract/pytesseract.py', False),
 ('P22', 'NAPS2 command line documentation (NAPS Developers, 2026)', 'https://www.naps2.com/doc/command-line', False),
 ('P23', 'NAPS2 download page (NAPS Developers, 2026)', 'https://www.naps2.com/download', False),
 ('P24', 'OCRmyPDF documentation (OCRmyPDF contributors, 2026)', 'https://ocrmypdf.readthedocs.io/en/latest/', False),
 ('P25', 'PyPI JSON metadata of ocrmypdf (Python Package Index, 2026)', 'https://pypi.org/pypi/ocrmypdf/json', False),
 ('P26', 'PyPI JSON metadata of opencv-python-headless (Python Package Index, 2026)', 'https://pypi.org/pypi/opencv-python-headless/json', False),
 ('P27', 'subprocess - Subprocess management (Python 3.14 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/subprocess.html', False),
 ('P28', 'What is new in Python 3.14 (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/whatsnew/3.14.html', False),
 ('P29', 'Levenshtein distance (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Levenshtein_distance', False),
 ('P30', 'Word error rate (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Word_error_rate', False),
 ('P31', 'ISO 639-3 code tables (SIL International, 2026)', 'https://iso639-3.sil.org/code_tables/639/data', False),
 ('P32', 'ISO 639-2 language code list (Library of Congress, 2026)', 'https://www.loc.gov/standards/iso639-2/php/code_list.php', False),
 ('P33', 'PyAutoGUI documentation, screenshot functions (Al Sweigart, 2026)', 'https://pyautogui.readthedocs.io/en/latest/screenshot.html', False),
 ('P34', 'PyPI JSON metadata of pyautogui (Python Package Index, 2026)', 'https://pypi.org/pypi/pyautogui/json', False),
 ('P35', 'Optical character recognition (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Optical_character_recognition', False),
 ('P36', 'Tesseract (software) (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Tesseract_(software)', False),
 ('P37', 'Emanuel Goldberg (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Emanuel_Goldberg', False),
 ('P38', 'Kurzweil Computer Products (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Kurzweil_Computer_Products', False),
 ('P39', 'ReCAPTCHA (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/ReCAPTCHA', False),
 ('P40', 'Frankenstein (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Frankenstein', False),
 ('P41', 'Image Preprocessing for Tesseract OCR, the placeholder post the chapter links to (Al Sweigart, 2026)', 'https://autbor.com/preprocessingocr', False),
 ('P42', 'Frankenstein, the page with an embedded document of Figure 22-2 (Al Sweigart, 2026)', 'https://autbor.com/embeddedfrankenstein/', False),
 ('P43', "Otsu's method (Wikipedia, 2026)", 'https://en.wikipedia.org/wiki/Otsu%27s_method', False),
 ('P44', 'PyPI JSON metadata of pillow (Python Package Index, 2026)', 'https://pypi.org/pypi/pillow/json', False),
 ('P45', 'Image module, Pillow reference (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/reference/Image.html', False),
 ('P46', 'Image file formats, Pillow handbook (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html', False),
 ('P47', 'Pillow 12.0.0 release notes (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/releasenotes/12.0.0.html', False),
 ('P48', 'Python support, Pillow installation (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/installation/python-support.html', False),
 ('P49', 'uv - Python versions (Astral documentation, 2026)', 'https://docs.astral.sh/uv/concepts/python-versions/', False),
 ('P50', 'Download Python (Python Software Foundation, 2026)', 'https://www.python.org/downloads/', False),
 ('P51', 'ImageOps module, Pillow reference (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/reference/ImageOps.html', False),
 ('P52', 'difflib - Helpers for computing deltas (Python 3.14 documentation, Python Software Foundation, 2026)', 'https://docs.python.org/3.14/library/difflib.html', False),
 ('P53', 'Hewlett-Packard (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Hewlett-Packard', False),
]
CONCEPTS = [
 ('Section', 'Installing Tesseract and PyTesseract'),
 ('Section', 'Windows'),
 ('Section', 'macOS'),
 ('Section', 'Linux'),
 ('Section', 'PyTesseract'),
 ('Section', 'OCR Fundamentals'),
 ('Section', 'Preprocessing an Image'),
 ('Section', 'Fixing Mistakes Using Large Language Models'),
 ('Section', 'Recognizing Text in Non-English Languages'),
 ('Section', 'The NAPS2 Scanner Application'),
 ('Section', 'Installing and Setting Up NAPS2'),
 ('Section', 'Running NAPS2 from Python'),
 ('Section', 'Specifying Input'),
 ('Section', 'Summary'),
 ('Section', 'Practice Questions'),
 ('Section', 'Practice Program: Browser Text Scraper'),
 ('Figure', 'Figure 22-1: the top part of a scanned page from an 1831 print of Frankenstein by Mary Shelley'),
 ('Figure', 'Figure 22-2: an example web page with an embedded document'),
 ('Function', 'tess.image_to_string()'),
 ('Function', 'tess.get_languages()'),
 ('Function', 'subprocess.run()'),
 ('Function', 'pyautogui.screenshot()'),
 ('Function', 'Image.open()'),
 ('Module', 'pytesseract'),
 ('Module', 'PIL.Image'),
 ('Module', 'subprocess'),
 ('Module', 'pyautogui'),
 ('Module', 'ocrmypdf'),
 ('Option', "lang='eng+jpn'"),
 ('Option', "'--install', 'ocr-eng'"),
 ('Option', "'-n', '0'"),
 ('File', 'ocr-example.png'),
 ('File', 'frankenstein.png'),
 ('File', 'frankenstein_jpn.png'),
 ('File', 'output.pdf'),
 ('File', 'output.txt'),
 ('File', 'ocrscreen.py'),
 ('Tool', 'Tesseract'),
 ('Tool', 'NAPS2'),
]

FINDINGS = [
 ('F1', 'Background',
  "Chapter 22 of the 3rd edition, Recognizing Text in Images, teaches PyTesseract and the Tesseract OCR engine (four lines to read an image, preprocessing advice, a large language model to fix mistakes, other languages) and the NAPS2 application run from Python for PDFs with embedded text, and ends with 7 practice questions and 1 practice program, the Browser Text Scraper [P01]. The page was fetched on 2026-10-13 and returned 200 with 40,521 bytes, holds 8 listings and 2 figures, and its sha256 equals the chapterDigest the book's own chapter ontology records [P01] [P03] [P04].",
  ['P01', 'P03', 'P04']),
 ('F2', 'The online materials',
  'The online materials of the 3rd edition (7,759,877 bytes, 91 files, 72 of them Python) hold ocr-example.png (939 by 1198, mode RGBA), frankenstein.png (1130 by 672, mode P), frankenstein_jpn.png (1211 by 606, mode RGB) and preprocess_ocr.py (190 lines), and none of ocrscreen.py, output.pdf, cat.png, dog.png, moose.png, spam.pdf, eggs.pdf or output.txt, which the chapter creates or assumes; the publisher\'s book page has 1 occurrence of Recognizing Text and 0 of Tesseract, OCR or NAPS2 [P01] [P02] [P04].',
  ['P01', 'P02', 'P04']),
 ('F3', 'The chapter replayed',
  "Of the 22 statements of the chapter's listings 1, 2, 4, 5 and 6 replayed as printed, 18 matched the book with the apt Tesseract 5.3.4, 20 with 5.5.3 and the fast data, 20 with 4.1.1, 18 with 5.5.3 and the best data, 19 with all the apt languages and 21 with all languages under 5.5.3; with the book's pins, 18 matched on Python 3.13.14, 8 on Python 3.14.6 and 0 in an empty Python; the statements that differ are get_languages(), the first word Iv, the Japanese heading and the English gibberish [P01] [P05].",
  ['P01', 'P05']),
 ('F4', 'The pin that cannot import',
  "Appendix A pins pytesseract==0.3.10, whose source imports pkgutil.find_loader, removed in Python 3.14, so on Python 3.14.6 the import raises ImportError (cannot import name 'find_loader' from 'pkgutil'), on 3.13.14 it only warns, and 0.3.13 has no find_loader; PyPI has 28 releases of pytesseract, none numbered 0.3.11 or 0.3.12, and three older ones (0.3.4, 0.3.7 and 0.3.8) install only from source [P05] [P19] [P28].",
  ['P05', 'P19', 'P28']),
 ('F5', 'The same page, different engines',
  "The first word of frankenstein.png came back as Iv with 4.1.1 and 5.5.3 and the fast data, In with the apt 5.3.4, Ir with the best data of all three and It with the legacy data under 4.1.1 and 5.5.3, where the book prints Iv; the character error rate against the page was 0.0035 with the fast data and 0.0017 with the best and the legacy data (MEASURED single runs with the Tesseract versions named); the picture shows an I followed by a small capital T [P01] [P10] [P16] [P17].",
  ['P01', 'P10', 'P16', 'P17']),
 ('F6', 'The three kinds of English data',
  "eng.traineddata is 4,113,088 bytes in tessdata_fast, 15,400,601 in tessdata_best and 23,466,654 in tessdata, each equal to the file its GitHub repository serves on 2026-10-13, and the apt package's file is the fast one; all of tessdata_fast is 706,776,225 bytes (126 languages and 37 script models), where the chapter says all languages add about 600MB [P01] [P10] [P16] [P17].",
  ['P01', 'P10', 'P16', 'P17']),
 ('F7', 'Language codes',
  "The chapter calls the language strings ISO 639-3 codes while the Tesseract manual page says ISO 639-2; 13 of the 126 names of tessdata_fast are not three letters, osd is no language, lang='ger' (the bibliographic 639-2 code of German) raises TesseractError while lang='deu' reads, lang='Japanese' raises the same error, and a missing pack inside 'eng+xyz' raises nothing and reads at 0.0116 [P01] [P14] [P31] [P32].",
  ['P01', 'P14', 'P31', 'P32']),
 ('F8', 'The Japanese page',
  "On frankenstein_jpn.png (1211 by 606, 13 lines) the picture shows 第 5 章 and 憂鬱; the apt Tesseract with lang='jpn' printed 第 5 剖 and 愛鬱 where the book prints 第 5 剖 and 芝鬱, the fast data under 5.5.3 equalled the book and the best data gave 901 characters against 538; lang='eng' gave 0 Japanese characters and gibberish, and 'eng+jpn' read a mixed line correctly [P01].",
  ['P01']),
 ('F9', 'What hurts',
  "On drawn pages with known text the apt Tesseract read 8-pixel letters at 0.2278 and 12-pixel letters at 0.0193, a page turned by 2 degrees at 0.0154 and by 5 degrees at 0.5753, noise of deviation 60 at 0.1313 and of 90 at 1.0 (MEASURED single runs with the Tesseract version 5.3.4); white text on black read at 0.0116 because tessedit_do_invert is 1 (deprecated, to go in release 6) and at 1.0965 with it off, so the chapter's advice of dark text on light describes what the engine did not need [P01] [P08].",
  ['P01', 'P08']),
 ('F10', 'What helps',
  "Enlarging a 9-pixel page 2 times lowered the error rate from 0.0579 to 0.0154, deskewing a page turned by 6 degrees (estimated -6.0) from 0.5985 to 0.0116, Otsu thresholding raised 0.0154 to 0.0347 on a noisy page, a tight crop returned the empty string and the same crop with a 10-pixel white border returned the line, and telling the engine 300 dpi for a 9-pixel page raised 0.0579 to 0.7452 (MEASURED single runs with the Tesseract version 5.3.4) [P01] [P08] [P43].",
  ['P01', 'P08', 'P43']),
 ('F11', 'Segmentation',
  "--psm 3, 4, 6 and 11 read a page of 6 lines at 0.0116 and --psm 7 and 13 at 0.9923 and 0.9961; two columns read column by column with the default mode and merged line by line with --psm 6, and columns 2 and 4 pixels apart merged at 0.5819 and 0.5791; tesseract --help-psm lists 14 modes, and the chapter uses none of the words psm, dpi, whitelist or timeout (MEASURED single runs with the Tesseract version 5.3.4) [P01] [P14].",
  ['P01', 'P14']),
 ('F12', 'Errors a spell checker cannot see',
  "The 2 wrong words of the 106 on Figure 22-1 (IT as In, motion as Motion) are real English words and a spell check against the 104,334 words of /usr/share/dict/words flagged nothing; the mean confidence was 94.5, the wrong In had 55 and Motion 92; the language model step was NOT EXECUTED, and its sample prompt has 419 characters [P01].",
  ['P01']),
 ('F13', 'Hyphens at the line ends',
  "ocr-example.png gave 51 lines with 7 words hyphenated at a line end (dig-ital, pro-grams, compre-hend, pro-grams, straight-forward, pro-gramming and graph-ics); removing every hyphen at a line end turned the real compound well-known into wellknown in a sample, so a word list is needed [P01].",
  ['P01']),
 ('F14', 'NAPS2',
  "NAPS2 8.5.1 (the .deb package) ran the book's call with naps2_path = ['naps2', 'console'] (return code 0, 1 page, text error rate 0.0035) with its own Tesseract 5.5.0; a second call without -f returned 0 and printed File already exists. Use --force to overwrite.; the Windows path and flatpak raised FileNotFoundError; -i spam.pdf[0:2], spam.pdf[-2:] and spam.pdf[1:6:2] gave the pages 0 and 1, 5 and 6, and 1, 3 and 5 (MEASURED single run with the Tesseract version 5.5.0) [P01] [P22] [P23].",
  ['P01', 'P22', 'P23']),
 ('F15', 'Searchable PDFs',
  "A PDF that Pillow made from frankenstein.png held 0 characters of text, the PDF of image_to_pdf_or_hocr read at 0.0138 with 106 word boxes, and ocrmypdf 17.13.0 exited 2 for a PNG without a resolution, 0 with --image-dpi 150 (0.0035), 6 for a PDF that already has text and 0 with --skip-text (MEASURED single runs with the Tesseract version 5.3.4) [P24] [P25].",
  ['P24', 'P25']),
 ('F16', 'The screen scraper',
  "On a virtual X display the template's own constants (400, 200, 1000, 800) cropped 600 by 600 pixels and appended 361 characters (0.3824 against the page), the whole window gave 581 characters at 0.0035 and a second run made 1162 in all; without DISPLAY the import raised KeyError: 'DISPLAY'; nobody saw the screen (MEASURED single runs with the Tesseract version 5.3.4) [P01] [P33].",
  ['P01', 'P33']),
 ('F17', 'The shipped script and the linked post',
  "preprocess_ocr.py (190 lines) calls FileNotFileError, grayscale_image and open_image, which it never defines, defines a function named open, and ends with NameError: name 'open_image' is not defined when run; the post at autbor.com/preprocessingocr answered 301 and then 200 and says it is a placeholder [P01] [P02] [P41].",
  ['P01', 'P02', 'P41']),
 ('F18', 'Interpreters and releases',
  "One program of 19 items printed the same under 11 interpreters (Python 3.11.17 to 3.15.0b4); 9 items printed the same under 14 Pillow releases (9.5.0 to 12.3.0); between pytesseract 0.3.9, 0.3.10 and 0.3.13 only the confidence type changed, a str in 0.3.9 and an int from 0.3.10 [P19] [P44] [P50].",
  ['P19', 'P44', 'P50']),
 ('F19', 'Not executed',
  'Nothing ran on Windows or macOS, with Homebrew, with the Flatpak of NAPS2, with a flatbed scanner, with a large language model or on a real screen with a real browser; Python 3.15 was only a beta (3.15.0b4); the repository commit the course pins was not opened; and the photograph of the stories was not fetched because the single request to Wikimedia Commons answered 429 [P01] [P23] [P50].',
  ['P01', 'P23', 'P50']),
]

def X(code):
    """An executable example as one expression with no double quote and no line break: the code runs in a fresh
    namespace and the value of its variable out is the result."""
    lit = "'" + code.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace('"', "\\x22") + "'"
    return "(lambda g: (exec(%s, g), g['out'])[1])({})" % lit

# The helpers every example starts: err, wd, lev, norm, cer, wrap, render, ocr, zipbytes, shp, with_engine and reset_engine; EXE and DATA hold the Tesseract
# builds and the data folders of this machine, and the chapter's online materials are fetched at run time and hash-checked.
_PRE = r'''import io, os, re, sys, math, json, time, shutil, hashlib, tempfile, warnings, subprocess, zipfile, difflib, importlib.metadata as md
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import pytesseract as tess
warnings.simplefilter('ignore')
FONTS = {'sans': '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'serif': '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 'mono': '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 'bold': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'roman': '/usr/share/fonts/opentype/urw-base35/NimbusRoman-Regular.otf', 'script': '/usr/share/fonts/opentype/urw-base35/Z003-MediumItalic.otf', 'jp': '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'}
TEXT = 'It was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet.'
TRUTH = ('THE MODERN PROMETHEUS. 43 CHAPTER V. IT was on a dreary night of November, that I beheld the accomplishment of my toils. With an anxiety that almost amounted to agony, I collected the instruments of life around me, that I might infuse a spark of being into the lifeless thing that lay at my feet. It was already one in the morning ; the rain pattered dismally against the panes, and my candle was nearly burnt out, when, by the glimmer of the half-extinguished light, I saw the dull yellow eye of the creature open ; it breathed hard, and a convulsive motion agitated its limbs.')
ZIPSHA = 'dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916'
FILESHA = {'ocr-example.png': 'c875a04c8a51401f59848ea93bd754fb6095f9f1a0041e4878dd05eeb44b13b8', 'frankenstein.png': 'c2125e5ef6840d4f23dfba68021c52710290a4c8d3cafdbabf1f619c70b33851', 'frankenstein_jpn.png': '3f812b8e5e396db6685f1cfe9e35639b9eaabd727cdb861e2663c6c768ca40fd', 'preprocess_ocr.py': 'e204109350e49c621159c3c8d656da3af564e368a9d0d84b95f222cfa583f377', 'dictionary.txt': 'dc4042ec00f36acbb1c2c514c86db9d48348a1cfa8ec1bf105c08910bc094d3f'}
def err(f):
    try: return ('ok', f())
    except BaseException as e: return (type(e).__name__, str(e).splitlines()[0][:90] if str(e) else '')
def wd():
    d = tempfile.mkdtemp(); os.chdir(d); return d
def lev(a, b):
    if a == b: return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1): cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
def norm(t): return re.sub(r'\s+', ' ', t).strip()
def cer(ref, hyp):
    r = norm(ref); return round(lev(r, norm(hyp)) / len(r), 4)
def wrap(text, font, width):
    d = ImageDraw.Draw(Image.new('L', (10, 10))); lines = []; cur = ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines
def render(text=TEXT, font='sans', px=24, fg=0, bg=255, width=900, pad=20, noise=0, rot=0, seed=1):
    f = ImageFont.truetype(FONTS.get(font, font), px); lines = wrap(text, f, width - 2 * pad); lh = int(px * 1.4)
    im = Image.new('L', (width, lh * len(lines) + 2 * pad), bg); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines): d.text((pad, pad + i * lh), l, font=f, fill=fg)
    if rot: im = im.rotate(rot, expand=True, fillcolor=bg, resample=Image.Resampling.BICUBIC)
    if noise:
        a = np.asarray(im).astype(float) + np.random.default_rng(seed).normal(0, noise, (im.height, im.width)); im = Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
    return im, ' '.join(lines)
def ocr(im, **k): return tess.image_to_string(im, **k)
def zipbytes():
    p = os.path.join(tempfile.gettempdir(), 'ch22_materials_%s.zip' % ZIPSHA[:8])
    if not os.path.exists(p):
        import urllib.request
        rq = urllib.request.Request('https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0'})
        open(p + '.part', 'wb').write(urllib.request.urlopen(rq, timeout=180).read()); os.replace(p + '.part', p)
    b = open(p, 'rb').read(); assert hashlib.sha256(b).hexdigest() == ZIPSHA, 'the online materials differ from the recorded zip'
    return b
def shp(extra=False):
    d = wd(); z = zipfile.ZipFile(io.BytesIO(zipbytes())); names = [n for n in z.namelist() if '__MACOSX' not in n]
    for f, h in FILESHA.items():
        if f == 'dictionary.txt' and not extra: continue
        data = z.read([n for n in names if n.endswith('/' + f)][0]); assert hashlib.sha256(data).hexdigest() == h, f; open(f, 'wb').write(data)
    return d
EXE = {'4.1.1': '/home/claude/tesseract-4.1.1/bin/tesseract', '5.3.4': '/usr/bin/tesseract', '5.5.3': '/home/claude/tesseract-5.5.3/bin/tesseract'}
DATA = {'fast': '/home/claude/tessdata_fast', 'best': '/home/claude/tessdata_best', 'legacy': '/home/claude/tessdata_legacy', 'all': '/home/claude/tessdata_fast_all'}
def with_engine(v, data='fast'):
    tess.pytesseract.tesseract_cmd = EXE[v]; os.environ['TESSDATA_PREFIX'] = DATA[data]
def reset_engine():
    tess.pytesseract.tesseract_cmd = 'tesseract'; os.environ.pop('TESSDATA_PREFIX', None)
'''
TAX = [
 ('InstallingTheTools', 'TheEngine', 'EngineVersion', 'tess.get_tesseract_version()',
  'The command tesseract --version prints a first line such as tesseract 5.3.4 followed by the libraries it was built with (leptonica among them) and ends with return code 0, and pytesseract.get_tesseract_version() returns the same 5.3.4.',
  (X(_PRE + r'''
r = subprocess.run(['tesseract', '--version'], capture_output=True, text=True, stdin=subprocess.DEVNULL); first = (r.stdout + r.stderr).splitlines()[0]
out = (first, str(tess.get_tesseract_version()), r.returncode, 'leptonica' in (r.stdout + r.stderr))'''), "('tesseract 5.3.4', '5.3.4', 0, True)")),
 ('InstallingTheTools', 'TheEngine', 'LanguageFolder', 'tesseract --list-langs',
  'The command tesseract --list-langs prints a first line that names the data folder and the count 7 and then the codes deu, eng, fra, jpn, osd, rus and tur, one on each line.',
  (X(_PRE + r'''
r = subprocess.run(['tesseract', '--list-langs'], capture_output=True, text=True, stdin=subprocess.DEVNULL); ls = r.stdout.splitlines()
out = (ls[0], sorted(ls[1:]), len(ls) - 1)'''), '(\'List of available languages in "/usr/share/tesseract-ocr/5/tessdata/" (7):\', [\'deu\', \'eng\', \'fra\', \'jpn\', \'osd\', \'rus\', \'tur\'], 7)')),
 ('InstallingTheTools', 'TheEngine', 'PathLookup', 'tess.pytesseract.tesseract_cmd',
  "pytesseract runs the program named in tesseract_cmd, which is 'tesseract' by default and found on the PATH (/usr/bin/tesseract here), and a path that does not exist makes the first call raise TesseractNotFoundError; C:\\Program Files\\Tesseract-OCR\\tesseract.exe is an absolute Windows path but does not exist on this Linux machine.",
  (X(_PRE + r'''
import ntpath
old = tess.pytesseract.tesseract_cmd; where = shutil.which('tesseract'); tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
e = err(lambda: tess.image_to_string(Image.new('L', (40, 20), 255))); tess.pytesseract.tesseract_cmd = old
out = (old, where, e[0], ntpath.isabs(r'C:\Program Files\Tesseract-OCR\tesseract.exe'), sys.platform)'''), "('tesseract', '/usr/bin/tesseract', 'TesseractNotFoundError', True, 'linux')")),
 ('InstallingTheTools', 'TheWrapper', 'PyTesseractRelease', "md.version('pytesseract')",
  'The newest pytesseract is 0.3.13; it requires Pillow 8.0.0 or newer and packaging 21.3 or newer and Python 3.8 or newer, and the book pins 0.3.10.',
  (X(_PRE + r'''
req = md.requires('pytesseract')
out = (md.version('pytesseract'), sorted(req), md.metadata('pytesseract')['Requires-Python'], hasattr(tess, 'image_to_string'), tess.__version__ if hasattr(tess, '__version__') else None)'''), "('0.3.13', ['Pillow>=8.0.0', 'packaging>=21.3'], '>=3.8', True, '0.3.13')")),
 ('InstallingTheTools', 'TheWrapper', 'FindLoaderBreak', "hasattr(pkgutil, 'find_loader')",
  "pkgutil.find_loader was removed in Python 3.14, so hasattr(pkgutil, 'find_loader') is False on 3.14; pytesseract 0.3.13 no longer contains the name, while 0.3.10 used it and stops at the import.",
  (X(_PRE + r'''
import pkgutil, inspect, pytesseract.pytesseract as pp
src = inspect.getsource(pp)
import importlib.util
out = (hasattr(pkgutil, 'find_loader'), 'find_loader' in src, importlib.util.find_spec('numpy') is not None, sys.version_info[:2])'''), '(False, False, True, (3, 14))')),
 ('InstallingTheTools', 'TheWrapper', 'PillowCoupling', "tess.image_to_string(Image.open('line.png'))",
  "image_to_string accepts a file name, an open Pillow image or a NumPy array and returns the same text for all three, here 'Tesseract reads this line of text' with a final newline, for a 700 by 84 image in mode L with Pillow 12.3.0.",
  (X(_PRE + r'''
d = wd(); im, truth = render('Tesseract reads this line of text', px=32, width=700); im.save('line.png')
a = tess.image_to_string('line.png'); b = tess.image_to_string(Image.open('line.png')); c = tess.image_to_string(np.asarray(Image.open('line.png')))
out = (a == b, a == c, repr(a), md.version('pillow'), im.size, im.mode)'''), '(True, True, "\'Tesseract reads this line of text\\\\n\'", \'12.3.0\', (700, 84), \'L\')')),
 ('InstallingTheTools', 'InstallerPlatforms', 'WindowsInstaller', 'ntpath.basename(path)',
  "On Windows the installer puts tesseract.exe into C:\\Program Files\\Tesseract-OCR, the folder to add to the PATH or to give to pytesseract as tesseract_cmd; on this Linux machine that path does not exist and shutil.which('tesseract.exe') is None.",
  (X(_PRE + r'''
import ntpath
p = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
out = (ntpath.basename(p), ntpath.dirname(p), ntpath.splitdrive(p)[0], os.path.exists(p), shutil.which('tesseract.exe'))'''), "('tesseract.exe', 'C:\\\\Program Files\\\\Tesseract-OCR', 'C:', False, None)")),
 ('InstallingTheTools', 'InstallerPlatforms', 'MacHomebrew', "shutil.which('brew')",
  'On macOS Homebrew installs the engine with brew install tesseract, usually into /opt/homebrew/bin; here brew is not found, /opt/homebrew does not exist and pointing tesseract_cmd there raises TesseractNotFoundError.',
  (X(_PRE + r'''
old = tess.pytesseract.tesseract_cmd; tess.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
e = err(lambda: tess.get_tesseract_version()); tess.pytesseract.tesseract_cmd = old
out = (shutil.which('brew'), os.path.exists('/opt/homebrew'), e[0], sys.platform)'''), "(None, False, 'TesseractNotFoundError', 'linux')")),
 ('InstallingTheTools', 'InstallerPlatforms', 'LinuxApt', 'dpkg-query tesseract-ocr',
  'On Ubuntu apt installs the packages tesseract-ocr 5.3.4-1build5 and tesseract-ocr-eng 1:4.1.0-2, and 7 language codes (deu, eng, fra, jpn, osd, rus, tur) were installed on this machine.',
  (X(_PRE + r'''
r = subprocess.run(['dpkg-query', '-W', '-f', '${Package} ${Version}\n', 'tesseract-ocr', 'tesseract-ocr-eng'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
inst = subprocess.run(['dpkg-query', '-W', '-f', '${Package}\n', 'tesseract-ocr-*'], capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout.split()
out = (r.stdout.splitlines(), sorted(n[-3:] for n in inst if len(n) == 17), shutil.which('tesseract'))'''), "(['tesseract-ocr 5.3.4-1build5', 'tesseract-ocr-eng 1:4.1.0-2'], ['deu', 'eng', 'fra', 'jpn', 'osd', 'rus', 'tur'], '/usr/bin/tesseract')")),
 ('ReadingAnImage', 'TheFourLines', 'OpenImage', "Image.open('ocr-example.png')",
  'The three images of the online materials open as ocr-example.png 939 by 1198 in mode RGBA, frankenstein.png 1130 by 672 in mode P and frankenstein_jpn.png 1211 by 606 in mode RGB, all PNG.',
  (X(_PRE + r'''
shp(); a = Image.open('ocr-example.png'); f = Image.open('frankenstein.png'); j = Image.open('frankenstein_jpn.png')
out = ((a.size, a.mode, a.format), (f.size, f.mode, f.format), (j.size, j.mode, j.format))'''), "(((939, 1198), 'RGBA', 'PNG'), ((1130, 672), 'P', 'PNG'), ((1211, 606), 'RGB', 'PNG'))")),
 ('ReadingAnImage', 'TheFourLines', 'ImageToString', 'tess.image_to_string(im)',
  "image_to_string(im) returns a str; for the line 'Tesseract reads this line of text' drawn at 32 pixels it returned the line plus a newline with a character error rate of 0.0 (MEASURED single runs with the Tesseract version 5.3.4).",
  (X(_PRE + r'''
d = wd(); im, truth = render('Tesseract reads this line of text', px=32, width=700); t = tess.image_to_string(im)
out = (repr(t), truth, cer(truth, t), type(t).__name__)'''), '("\'Tesseract reads this line of text\\\\n\'", \'Tesseract reads this line of text\', 0.0, \'str\')')),
 ('ReadingAnImage', 'TheFourLines', 'ReturnType', 'tess.Output.BYTES',
  'The default return is a str ending in a newline, output_type=Output.BYTES returns bytes with the same ending, and output_type=Output.DICT returns a dictionary whose only key is text.',
  (X(_PRE + r'''
im, truth = render('Tesseract reads this line of text', px=32, width=700); t = tess.image_to_string(im); b = tess.image_to_string(im, output_type=tess.Output.BYTES); dct = tess.image_to_string(im, output_type=tess.Output.DICT)
out = (repr(t[-3:]), type(b).__name__, b[-3:], list(dct), t.strip() == truth)'''), '("\'xt\\\\n\'", \'bytes\', b\'xt\\n\', [\'text\'], True)')),
 ('ReadingAnImage', 'WhatComesBack', 'FrankensteinOutput', "tess.image_to_string(Image.open('frankenstein.png'))",
  'On frankenstein.png the apt Tesseract returned 581 characters (578 once the white space is normalised), the first line was THE MODERN PROMETHEUS. 43 and the character error rate against the page was 0.0035 (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
shp(); t = tess.image_to_string(Image.open('frankenstein.png'))
out = (len(t), len(norm(t)), cer(TRUTH, t), t.split('\n')[0], norm(t)[:70])'''), "(581, 578, 0.0035, 'THE MODERN PROMETHEUS. 43', 'THE MODERN PROMETHEUS. 43 CHAPTER V. In was on a dreary night of Novem')")),
 ('ReadingAnImage', 'WhatComesBack', 'LineBreaks', "t.split('\\n')",
  'The string keeps the line breaks of the picture: splitting the text of frankenstein.png at newlines gave 15 pieces, 2 blank lines between paragraphs and a final newline, and joining the words with single spaces gives the normalised text.',
  (X(_PRE + r'''
shp(); t = tess.image_to_string(Image.open('frankenstein.png')); ls = t.split('\n')
out = (len(ls), t.count('\n\n'), [len(l) for l in ls[:6]], norm(t) == ' '.join(t.split()), repr(t[-2:]))'''), '(15, 2, [25, 0, 10, 0, 55, 55], True, "\'.\\\\n\'")')),
 ('ReadingAnImage', 'WhatComesBack', 'ExactResultsVary', 'cer(truth, tess.image_to_string(im))',
  'On the same noisy 12 pixel page the character error rate was 0.0154 with 4.1.1, 0.0193 with 5.3.4, 0.0154 with 5.5.3 and the fast data, 0.0077 with the best data and 0.0154 with all languages, 3 distinct values in 5 runs (MEASURED single runs with the Tesseract version 5.3.4)s named.',
  (X(_PRE + r'''
im, truth = render(px=12, width=700, noise=10); res = {}
for v, k in (('4.1.1', 'fast'), ('5.3.4', 'fast'), ('5.5.3', 'fast'), ('5.5.3', 'best'), ('5.5.3', 'all')):
    with_engine(v, k) if v != '5.3.4' else reset_engine(); res[v + '/' + k] = cer(truth, tess.image_to_string(im))
reset_engine()
out = (res, len(set(res.values())))'''), "({'4.1.1/fast': 0.0154, '5.3.4/fast': 0.0193, '5.5.3/fast': 0.0154, '5.5.3/best': 0.0077, '5.5.3/all': 0.0154}, 3)")),
 ('ReadingAnImage', 'WhatComesBack', 'LineEndHyphens', "re.findall(r'(\\w+)-\\n(\\w+)', t)",
  'On ocr-example.png the text had 51 lines, 10 blank, and 7 words broken at a line end by a hyphen: dig-ital, pro-grams, compre-hend, pro-grams, straight-forward, pro-gramming and graph-ics.',
  (X(_PRE + r'''
shp(); t = tess.image_to_string(Image.open('ocr-example.png')); pairs = re.findall(r'(\w+)-\n(\w+)', t)
out = (len(pairs), pairs, len(t.splitlines()), t.count('\n\n'))'''), "(7, [('dig', 'ital'), ('pro', 'grams'), ('compre', 'hend'), ('pro', 'grams'), ('straight', 'forward'), ('pro', 'gramming'), ('graph', 'ics')], 51, 10)")),
 ('ReadingAnImage', 'OtherOutputs', 'ImageToData', 'tess.image_to_data(im, output_type=tess.Output.DICT)',
  'image_to_data returns 12 columns (level, page_num, block_num, par_num, line_num, word_num, left, top, width, height, conf, text); for a one line image it had 10 rows on levels 1 to 5 and the six words Tesseract, reads, this, line, of and text.',
  (X(_PRE + r'''
im, truth = render('Tesseract reads this line of text', px=32, width=700); dd = tess.image_to_data(im, output_type=tess.Output.DICT)
out = (list(dd), len(dd['text']), sorted(set(dd['level'])), [t for t in dd['text'] if t.strip()], dd['left'][-1] > 0)'''), "(['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text'], 10, [1, 2, 3, 4, 5], ['Tesseract', 'reads', 'this', 'line', 'of', 'text'], True)")),
 ('ReadingAnImage', 'OtherOutputs', 'ConfidenceScale', "dd['conf']",
  'The conf column is -1 on the rows above word level and from 0 to 100 on word rows; the six words of the test line had 96, 96, 96, 95, 96 and 96.',
  (X(_PRE + r'''
im, truth = render('Tesseract reads this line of text', px=32, width=700); dd = tess.image_to_data(im, output_type=tess.Output.DICT)
w = [(t, round(float(c), 1)) for t, c in zip(dd['text'], dd['conf']) if t.strip()]
out = (sorted({float(c) for t, c, l in zip(dd['text'], dd['conf'], dd['level']) if l < 5}), w, all(0 <= c <= 100 for t, c in w))'''), "([-1.0], [('Tesseract', 96.0), ('reads', 96.0), ('this', 96.0), ('line', 95.0), ('of', 96.0), ('text', 96.0)], True)")),
 ('ReadingAnImage', 'OtherOutputs', 'SearchableOutputs', "tess.image_to_pdf_or_hocr(im, extension='pdf')",
  'image_to_pdf_or_hocr returns bytes that start with %PDF- for a searchable PDF, hOCR markup with ocr_page and ocrx_word classes, and image_to_alto_xml returns XML that begins <?xml and holds 6 String elements for the six words.',
  (X(_PRE + r'''
im, truth = render('Tesseract reads this line of text', px=32, width=700)
pdf = tess.image_to_pdf_or_hocr(im, extension='pdf'); hocr = tess.image_to_pdf_or_hocr(im, extension='hocr'); alto = tess.image_to_alto_xml(im)
out = (pdf[:5], b'ocr_page' in hocr, b'ocrx_word' in hocr, alto[:5], alto.count(b'<String '), pdf.count(b'/Type /Page') >= 1)'''), "(b'%PDF-', True, True, b'<?xml', 6, True)")),
 ('ReadingAnImage', 'OtherOutputs', 'OsdOrientation', 'tess.image_to_osd(im, output_type=tess.Output.DICT)',
  'image_to_osd reported orientation 0 and rotate 0 for an upright page and orientation 270, rotate 90 and script Latin for the same page turned by 90 degrees; the turned page is 220 by 900 pixels.',
  (X(_PRE + r'''
im, truth = render(px=26, width=900); r = im.rotate(90, expand=True, fillcolor=255)
o = tess.image_to_osd(r, output_type=tess.Output.DICT); o0 = tess.image_to_osd(im, output_type=tess.Output.DICT)
out = ((o0['orientation'], o0['rotate']), (o['orientation'], o['rotate']), o['script'], r.size)'''), "((0, 0), (270, 90), 'Latin', (220, 900))")),
 ('AccuracyAndPreprocessing', 'MeasuringAccuracy', 'EditDistance', "lev('kitten', 'sitting')",
  'The edit distance counts the insertions, deletions and substitutions that turn one string into another: kitten to sitting is 3, an empty string to abc is 3, equal strings 0, It to Iv 1 and In to IT 1.',
  (X(_PRE + r'''
out = (lev('kitten', 'sitting'), lev('', 'abc'), lev('same', 'same'), lev('It', 'Iv'), lev('In', 'IT'))'''), '(3, 3, 0, 1, 1)')),
 ('AccuracyAndPreprocessing', 'MeasuringAccuracy', 'CharacterErrorRate', "cer('abcd', 'abxd')",
  'The character error rate is the edit distance divided by the length of the reference after white space is normalised: abcd against abxd is 0.25, an empty reading is 1.0 and a longer reading is 1.0 for abcd against abcdefgh.',
  (X(_PRE + r'''
out = (cer('abcd', 'abxd'), cer('a  b\nc', 'a b c'), cer('abcd', ''), cer('abcd', 'abcdefgh'), lev(norm('a  b\nc'), 'a b c'))'''), '(0.25, 0.0, 1.0, 1.0, 0)')),
 ('AccuracyAndPreprocessing', 'MeasuringAccuracy', 'WordErrorRate', 'wer(TRUTH, t)',
  'The word error rate is the edit distance of the word lists divided by the number of reference words: the cat sat against the cat sit is 0.3333, and the 106 words of frankenstein.png had 0.0189 against a character error rate of 0.0035 (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
def wer(r, h):
    r = r.split(); h = h.split(); return round(lev(r, h) / len(r), 4)
shp(); t = tess.image_to_string(Image.open('frankenstein.png'))
out = (wer('the cat sat', 'the cat sit'), wer('the cat sat', 'the cat'), len(TRUTH.split()), wer(TRUTH, t), cer(TRUTH, t))'''), '(0.3333, 0.3333, 106, 0.0189, 0.0035)')),
 ('AccuracyAndPreprocessing', 'WhatHurts', 'SmallText', 'render(px=8)',
  'The character error rate for the same text drawn at 8, 10, 12, 16 and 24 pixels was 0.2278, 0.0309, 0.0193, 0.0116 and 0.0116 (MEASURED single runs with the Tesseract version 5.3.4), so small type is the first thing that hurts.',
  (X(_PRE + r'''
res = {}
for px in (8, 10, 12, 16, 24):
    im, truth = render(px=px, width=700); res[px] = cer(truth, tess.image_to_string(im))
out = res'''), '{8: 0.2278, 10: 0.0309, 12: 0.0193, 16: 0.0116, 24: 0.0116}')),
 ('AccuracyAndPreprocessing', 'WhatHurts', 'FontChoice', "render(font='script')",
  'At 24 pixels the character error rate was 0.0116 for the sans font, 0.0 for the serif, 0.0 for the mono, 0.0116 for the bold, 0.0 for Roman and 0.0 for the script font (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
res = {}
for f in ('sans', 'serif', 'mono', 'bold', 'roman', 'script'):
    im, truth = render(font=f, px=24, width=900); res[f] = cer(truth, tess.image_to_string(im))
out = res'''), "{'sans': 0.0116, 'serif': 0.0, 'mono': 0.0, 'bold': 0.0116, 'roman': 0.0, 'script': 0.0}")),
 ('AccuracyAndPreprocessing', 'WhatHurts', 'Skew', 'render(rot=5)',
  'The character error rate for a page turned by 0, 2, 5, 10 and 20 degrees was 0.0116, 0.0154, 0.5753, 1.0 and 1.0 (MEASURED single runs with the Tesseract version 5.3.4), so a few degrees are tolerated and 5 degrees already break the reading.',
  (X(_PRE + r'''
res = {}
for rot in (0, 2, 5, 10, 20):
    im, truth = render(px=22, width=700, rot=rot); res[rot] = cer(truth, tess.image_to_string(im))
out = res'''), '{0: 0.0116, 2: 0.0154, 5: 0.5753, 10: 1.0, 20: 1.0}')),
 ('AccuracyAndPreprocessing', 'WhatHurts', 'NoiseLevel', 'render(noise=60)',
  'The character error rate with Gaussian noise of standard deviation 0, 30, 60 and 90 was 0.0116, 0.0116, 0.1313 and 1.0 (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
res = {}
for nz in (0, 30, 60, 90):
    im, truth = render(px=22, width=700, noise=nz); res[nz] = cer(truth, tess.image_to_string(im))
out = res'''), '{0: 0.0116, 30: 0.0116, 60: 0.1313, 90: 1.0}')),
 ('AccuracyAndPreprocessing', 'WhatHurts', 'LowContrast', 'render(fg=110, bg=140)',
  'With noise of 12 the character error rate was 0.0116 for black on white, 0.0656 for grey levels 100 on 160, and 1.0 for 110 on 140, 120 on 135 and 125 on 130 (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
res = {}
for fg, bg in ((0, 255), (100, 160), (110, 140), (120, 135), (125, 130)):
    im, truth = render(px=22, width=700, fg=fg, bg=bg, noise=12); res[(fg, bg)] = cer(truth, tess.image_to_string(im))
out = res'''), '{(0, 255): 0.0116, (100, 160): 0.0656, (110, 140): 1.0, (120, 135): 1.0, (125, 130): 1.0}')),
 ('AccuracyAndPreprocessing', 'WhatHurts', 'WhiteOnBlack', 'tessedit_do_invert=0',
  'White text on black read with a character error rate of 0.0116 by default, 1.0965 with -c tessedit_do_invert=0, and 0.0116 again when the picture is inverted first (MEASURED single runs with the Tesseract version 5.3.4), so the engine inverts by itself unless told not to.',
  (X(_PRE + r'''
im, truth = render(px=22, width=700, fg=255, bg=0)
out = (cer(truth, tess.image_to_string(im)), cer(truth, tess.image_to_string(im, config='-c tessedit_do_invert=0')), cer(truth, tess.image_to_string(ImageOps.invert(im), config='-c tessedit_do_invert=0')))'''), '(0.0116, 1.0965, 0.0116)')),
 ('AccuracyAndPreprocessing', 'WhatHelps', 'GrayscaleConversion', "c.convert('L')",
  "A colour page with first pixel (167, 205, 128) becomes grey level 185 with convert('L'); here colour and grey both read with a character error rate of 0.0116 (MEASURED single runs with the Tesseract version 5.3.4).",
  (X(_PRE + r'''
im, truth = render(px=22, width=700); c = Image.merge('RGB', (im.point(lambda v: 40 + v // 2), im.point(lambda v: 120 + v // 3), im.point(lambda v: 255 - v // 2)))
out = (c.mode, cer(truth, tess.image_to_string(c)), cer(truth, tess.image_to_string(c.convert('L'))), c.getpixel((0, 0)), c.convert('L').getpixel((0, 0)))'''), "('RGB', 0.0116, 0.0116, (167, 205, 128), 185)")),
 ('AccuracyAndPreprocessing', 'WhatHelps', 'Binarization', 'cv2.threshold(a, 0, 255, THRESH_BINARY + THRESH_OTSU)',
  "Otsu's method chose the threshold 136.0 for a noisy page and left only the values 0 and 255, and the character error rate was 0.0154 before and 0.0347 after (MEASURED single runs with the Tesseract version 5.3.4), so binarising did not help here.",
  (X(_PRE + r'''
import cv2
im, truth = render(px=22, width=700, noise=45); a = np.asarray(im); t, b = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
out = (cer(truth, tess.image_to_string(im)), cer(truth, tess.image_to_string(Image.fromarray(b))), float(t), sorted(set(b.flatten().tolist())))'''), '(0.0154, 0.0347, 136.0, [0, 255])')),
 ('AccuracyAndPreprocessing', 'WhatHelps', 'Upscaling', 'im.resize((w * k, h * k), Image.Resampling.LANCZOS)',
  'Nine pixel text of 600 by 76 pixels read with a character error rate of 0.0579 at the original size and 0.0154 when enlarged 2, 3 or 4 times (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
res = {}
im, truth = render(px=9, width=600)
for k in (1, 2, 3, 4):
    res[k] = cer(truth, tess.image_to_string(im.resize((im.width * k, im.height * k), Image.Resampling.LANCZOS) if k > 1 else im))
out = (res, im.size)'''), '({1: 0.0579, 2: 0.0154, 3: 0.0154, 4: 0.0154}, (600, 76))')),
 ('AccuracyAndPreprocessing', 'WhatHelps', 'WhiteBorder', 'ImageOps.expand(tight, border=10, fill=255)',
  'A line cropped tight (383 by 24 pixels) returned an empty string and the same line with a 10 pixel white border (403 by 44) returned Tesseract reads this line.',
  (X(_PRE + r'''
im, truth = render('Tesseract reads this line', px=32, width=900, pad=0); tight = im.crop(ImageOps.invert(im).getbbox()); bd = ImageOps.expand(tight, border=10, fill=255)
out = (tight.size, repr(tess.image_to_string(tight)), bd.size, repr(tess.image_to_string(bd)))'''), '((383, 24), "\'\'", (403, 44), "\'Tesseract reads this line\\\\n\'")')),
 ('AccuracyAndPreprocessing', 'WhatHelps', 'Deskew', 'cv2.minAreaRect(pts)',
  'For a page turned by 6 degrees minAreaRect estimated the angle -6.0 and turning back reduced the character error rate from 0.5985 to 0.0116 (MEASURED single runs with the Tesseract version 5.3.4), the image growing from 718 by 264 to 742 by 338.',
  (X(_PRE + r'''
import cv2
im, truth = render(px=22, width=700, rot=6); a = np.asarray(im); pts = np.column_stack(np.where(a < 128)).astype(np.float32)[:, ::-1]
ang = cv2.minAreaRect(pts)[-1]; ang = ang - 90 if ang > 45 else ang
fixed = im.rotate(ang, expand=True, fillcolor=255, resample=Image.Resampling.BICUBIC)
out = (round(float(ang), 2), cer(truth, tess.image_to_string(im)), cer(truth, tess.image_to_string(fixed)), im.size, fixed.size)'''), '(-6.0, 0.5985, 0.0116, (718, 264), (742, 338))')),
 ('AccuracyAndPreprocessing', 'Segmentation', 'PsmModes', "config='--psm 6'",
  'On a six line paragraph the page segmentation modes 3, 4, 6 and 11 returned 6 lines with a character error rate of 0.0116 while 7 and 13 returned 1 line with 0.9923 and 0.9961 (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
im, truth = render(px=24, width=600); res = {}
for p in (3, 4, 6, 7, 11, 13):
    t = tess.image_to_string(im, config='--psm %d' % p); res[p] = (len([l for l in t.splitlines() if l.strip()]), cer(truth, t))
out = (res, len(wrap(TEXT, ImageFont.truetype(FONTS['sans'], 24), 560)))'''), '({3: (6, 0.0116), 4: (6, 0.0116), 6: (6, 0.0116), 7: (1, 0.9923), 11: (6, 0.0116), 13: (1, 0.9961)}, 6)')),
 ('AccuracyAndPreprocessing', 'Segmentation', 'ColumnLayout', "config='--psm 6'",
  'A page of two columns read by default came out column by column, psm 6 mixed the rows of the two columns, and cropping each column and reading it alone gave a character error rate of 0.0 for both.',
  (X(_PRE + r'''
f = ImageFont.truetype(FONTS['sans'], 22); a, ta = render('alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon', px=22, width=330); b, tb = render('one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen', px=22, width=330)
pg = Image.new('L', (700, max(a.height, b.height)), 255); pg.paste(a, (0, 0)); pg.paste(b, (360, 0))
t3 = tess.image_to_string(pg); t6 = tess.image_to_string(pg, config='--psm 6'); left = tess.image_to_string(pg.crop((0, 0, 350, pg.height))); right = tess.image_to_string(pg.crop((350, 0, 700, pg.height)))
out = (norm(t3)[:60], norm(t6)[:60], cer(ta, left), cer(tb, right))'''), "('alpha beta gamma delta epsilon zeta eta theta iota kappa lam', 'alpha beta gamma delta one two three four five six epsilon z', 0.0, 0.0)")),
 ('AccuracyAndPreprocessing', 'Segmentation', 'SingleLine', "config='--psm 7'",
  'A one line image Order 4417-B shipped read the same by default and with --psm 7, and --psm 8 added a stray opening quotation mark.',
  (X(_PRE + r'''
im, truth = render('Order 4417-B shipped', px=30, width=420, pad=15)
out = (repr(tess.image_to_string(im)), repr(tess.image_to_string(im, config='--psm 7')), repr(tess.image_to_string(im, config='--psm 8')), truth)'''), '("\'Order 4417-B shipped\\\\n\'", "\'Order 4417-B shipped\\\\n\'", "\'‘Order 4417-B shipped\\\\n\'", \'Order 4417-B shipped\')')),
 ('AccuracyAndPreprocessing', 'ConfigStrings', 'WhitelistDigits', '-c tessedit_char_whitelist=0123456789-',
  'With the whitelist 0123456789- the line Order 4417-B shipped on 2026-10-13 was read as 4417-02026-10-13: letters are forced into the allowed characters and the B became a 0.',
  (X(_PRE + r'''
im, truth = render('Order 4417-B shipped on 2026-10-13', px=34, width=900)
a = norm(tess.image_to_string(im, config='--psm 7')); b = norm(tess.image_to_string(im, config='--psm 7 -c tessedit_char_whitelist=0123456789-'))
out = (a, b, truth)'''), "('Order 4417-B shipped on 2026-10-13', '4417-02026-10-13', 'Order 4417-B shipped on 2026-10-13')")),
 ('AccuracyAndPreprocessing', 'ConfigStrings', 'UserDefinedDpi', '-c user_defined_dpi=300',
  "A generated image carries no dpi (im.info.get('dpi') is None); for 9 pixel text the error rate was 0.0579 by default and with user_defined_dpi=70 and 0.7452 with 300 (MEASURED single runs with the Tesseract version 5.3.4).",
  (X(_PRE + r'''
im, truth = render(px=9, width=600); res = {}
for cfg in ('', '-c user_defined_dpi=70', '-c user_defined_dpi=300'): res[cfg or 'default'] = cer(truth, tess.image_to_string(im, config=cfg))
out = (res, im.info.get('dpi'))'''), "({'default': 0.0579, '-c user_defined_dpi=70': 0.0579, '-c user_defined_dpi=300': 0.7452}, None)")),
 ('AccuracyAndPreprocessing', 'ConfigStrings', 'TimeoutArgument', 'tess.image_to_string(im, timeout=0.001)',
  'timeout=0.001 raised RuntimeError with the text Tesseract process timeout, timeout=60 read the page with a character error rate of 0.0116 and timeout=0 means no limit (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
im, truth = render(px=22, width=700)
a = err(lambda: tess.image_to_string(im, timeout=0.001)); b = err(lambda: tess.image_to_string(im, timeout=60)); c = err(lambda: tess.image_to_string(im, timeout=0))
out = (a, cer(truth, b[1]), c[0])'''), "(('RuntimeError', 'Tesseract process timeout'), 0.0116, 'ok')")),
 ('LanguagesAndData', 'LanguagePacks', 'GetLanguages', "tess.get_languages(config='')",
  'get_languages returns a sorted list of 7 codes (deu, eng, fra, jpn, osd, rus, tur) on this machine, and osd is in it although it is not a language.',
  (X(_PRE + r'''
g = tess.get_languages(config='')
out = (g, len(g), type(g).__name__, 'osd' in g, g == sorted(g))'''), "(['deu', 'eng', 'fra', 'jpn', 'osd', 'rus', 'tur'], 7, 'list', True, True)")),
 ('LanguagesAndData', 'LanguagePacks', 'DataFolder', "config='--tessdata-dir folder'",
  "The language list is made of the .traineddata files in the folder: a folder with eng gave ['eng'], adding deu (1,525,436 bytes beside the 4,113,088 of eng) gave ['deu', 'eng'].",
  (X(_PRE + r'''
t0 = tempfile.mkdtemp(); src = '/usr/share/tesseract-ocr/5/tessdata/'; shutil.copy(src + 'eng.traineddata', t0); a = tess.get_languages(config='--tessdata-dir ' + t0); shutil.copy(src + 'deu.traineddata', t0); b = tess.get_languages(config='--tessdata-dir ' + t0)
out = (a, b, os.path.getsize(t0 + '/deu.traineddata'), os.path.getsize(t0 + '/eng.traineddata'))'''), "(['eng'], ['deu', 'eng'], 1525436, 4113088)")),
 ('LanguagesAndData', 'LanguagePacks', 'AllLanguagesSize', 'sum(os.path.getsize(f))',
  "The fast repository holds 126 languages (afr to yor) with 361,832,630 bytes and 37 scripts with 344,943,595 bytes, 706,776,225 bytes together, about 707 MB against the book's about 600MB.",
  (X(_PRE + r'''
ALL = DATA['all']; top = [f for f in os.listdir(ALL) if f.endswith('.traineddata')]; sc = os.listdir(ALL + '/script')
a = sum(os.path.getsize(ALL + '/' + f) for f in top); b = sum(os.path.getsize(ALL + '/script/' + f) for f in sc)
g = tess.get_languages(config='--tessdata-dir ' + ALL)
out = (len(g), g[:3], g[-3:], a, b, a + b, round((a + b) / 1e6), len(sc))'''), "(126, ['afr', 'amh', 'ara'], ['vie', 'yid', 'yor'], 361832630, 344943595, 706776225, 707, 37)")),
 ('LanguagesAndData', 'ChoosingLanguage', 'IsoCodes', "lang='deu'",
  "The code is the file name before .traineddata: lang='deu' read Die Größe der Straße und die Übung, and lang='ger' raised TesseractError because ger.traineddata does not exist.",
  (X(_PRE + r'''
im, truth = render('Die Größe der Straße und die Übung', px=32, width=900)
r = {l: err(lambda l=l: norm(tess.image_to_string(im, lang=l))) for l in ('deu', 'ger')}
out = (r['deu'], r['ger'][0], 'Error opening data file' in r['ger'][1], 'ger.traineddata' in r['ger'][1])'''), "(('ok', 'Die Größe der Straße und die Übung'), 'TesseractError', True, True)")),
 ('LanguagesAndData', 'ChoosingLanguage', 'JapaneseImage', "lang='jpn'",
  "On frankenstein_jpn.png lang='jpn' returned 13 lines beginning 第 5 剖 私が自分の労, which did not equal the book's two lines (error rates 0.0426 and 0.0233 against them).",
  (X(_PRE + r'''
shp(); BOOK = ['第 5 剖 私が自分の労苦の成果を目の当たりにしたのは、11 月の芝鬱な夜でした。 ほとんど苦', '痛に等しい不安を抱えながら、 私は足元に横たわる生命のないものに存在の輝きを吹き込むこ']
j = [l for l in tess.image_to_string(Image.open('frankenstein_jpn.png'), lang='jpn').split('\n') if l.strip()]
out = (len(j), j[:2] == BOOK, j[0][:12], cer(BOOK[0], j[0]), cer(BOOK[1], j[1]))'''), "(13, False, '第 5 剖 私が自分の労', 0.0426, 0.0233)")),
 ('LanguagesAndData', 'ChoosingLanguage', 'WrongLanguage', "lang='eng'",
  "On the top 200 pixels of the Japanese page lang='eng' returned HSE ALBADOGEOMRE AON with 0 Japanese characters while lang='jpn' returned 166 beginning 第 5 章 私が自分の労.",
  (X(_PRE + r'''
shp(); im = Image.open('frankenstein_jpn.png').crop((0, 0, 1211, 200)); e = tess.image_to_string(im, lang='eng'); j = tess.image_to_string(im, lang='jpn')
out = (sum(ord(c) > 0x2E80 for c in e), sum(ord(c) > 0x2E80 for c in j), repr(e[:20]), j[:12])'''), '(0, 166, "\'HSE ALBADOGEOMRE AON\'", \'第 5 章 私が自分の労\')')),
 ('LanguagesAndData', 'ChoosingLanguage', 'CombinedLanguages', "lang='eng+jpn'",
  "For a line of English with two Japanese characters, lang='eng' read the cat as 4 and the dog as %, and lang='jpn', 'eng+jpn' and 'jpn+eng' all read The cat is 猫 and the dog is 犬 today.",
  (X(_PRE + r'''
MIX = 'The cat is 猫 and the dog is 犬 today'; f = ImageFont.truetype(FONTS['jp'], 40); mi = Image.new('L', (1000, 90), 255); ImageDraw.Draw(mi).text((20, 20), MIX, font=f, fill=0)
out = {lg: norm(tess.image_to_string(mi, lang=lg, config='--psm 7')) for lg in ('eng', 'jpn', 'eng+jpn', 'jpn+eng')}'''), "{'eng': 'The cat is 4 and the dog is % today', 'jpn': 'The cat is 猫 and the dog is 犬 today', 'eng+jpn': 'The cat is 猫 and the dog is 犬 today', 'jpn+eng': 'The cat is 猫 and the dog is 犬 today'}")),
 ('LanguagesAndData', 'ChoosingLanguage', 'MissingLanguage', "lang='xyz'",
  'A code with no file raises TesseractError whose message holds Error opening data file and xyz.traineddata, and the command line ends with return code 1.',
  (X(_PRE + r'''
im = Image.new('L', (200, 60), 255)
e = err(lambda: tess.image_to_string(im, lang='xyz'))
r = subprocess.run(['tesseract', 'stdin', 'stdout', '-l', 'xyz'], input=b'', capture_output=True)
out = (e[0], 'Error opening data file' in e[1], 'xyz.traineddata' in e[1], r.returncode, r.stderr.decode().startswith('Error opening data file'))'''), "('TesseractError', True, True, 1, True)")),
 ('LanguagesAndData', 'ChoosingLanguage', 'AccentedLetters', "lang='fra'",
  "With the matching pack French, German, Turkish and Russian lines read with a character error rate of 0.0, and with lang='eng' the rates were 0.1212, 0.1176, 0.1562 and 0.9 (MEASURED single runs with the Tesseract version 5.3.4).",
  (X(_PRE + r'''
LINES = {'fra': 'Où êtes-vous allé après la fête ?', 'deu': 'Die Größe der Straße und die Übung', 'tur': 'Çocuğun şeker istediğini söyledi', 'rus': 'Съешь же ещё этих мягких булок'}
res = {}
for lg, tx in LINES.items():
    im, truth = render(tx, px=34, width=1000); res[lg] = (cer(tx, tess.image_to_string(im, lang=lg)), cer(tx, tess.image_to_string(im, lang='eng')))
out = res'''), "{'fra': (0.0, 0.1212), 'deu': (0.0, 0.1176), 'tur': (0.0, 0.1562), 'rus': (0.0, 0.9)}")),
 ('LanguagesAndData', 'ModelKinds', 'FastBestLegacy', "os.path.getsize('eng.traineddata')",
  'eng.traineddata is 4,113,088 bytes in the fast set (identical to the apt file, sha-256 7d4322bd2a77), 15,400,601 in the best set (8280aed0782f) and 23,466,654 in the legacy set (daa0c97d651c).',
  (X(_PRE + r'''
import hashlib
out = {k: (os.path.getsize(DATA[k] + '/eng.traineddata'), hashlib.sha256(open(DATA[k] + '/eng.traineddata', 'rb').read()).hexdigest()[:12]) for k in ('fast', 'best', 'legacy')}
out['apt'] = (os.path.getsize('/usr/share/tesseract-ocr/5/tessdata/eng.traineddata'), hashlib.sha256(open('/usr/share/tesseract-ocr/5/tessdata/eng.traineddata', 'rb').read()).hexdigest()[:12])'''), "{'fast': (4113088, '7d4322bd2a77'), 'best': (15400601, '8280aed0782f'), 'legacy': (23466654, 'daa0c97d651c'), 'apt': (4113088, '7d4322bd2a77')}")),
 ('LanguagesAndData', 'ModelKinds', 'OemModes', "config='--oem 0'",
  'With the legacy data --oem 0 read the line with an error rate of 0.0 and oems 1 and 3 with 0.0116, and with the fast data --oem 0 failed because the legacy engine needs a data file that holds it (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
im, truth = render(px=22, width=700); res = {}
for v, k in (('4.1.1', 'fast'), ('4.1.1', 'legacy'), ('5.5.3', 'fast'), ('5.5.3', 'legacy')):
    with_engine(v, k); res[v + '/' + k] = {o: err(lambda o=o: cer(truth, tess.image_to_string(im, config='--oem %d' % o)))[1:] for o in (0, 1, 3)}
reset_engine(); out = res'''), '{\'4.1.1/fast\': {0: (\'(1, "read_params_file: Can\\\'t open txt Error: Tesseract (legacy) engine requested, but comp\',), 1: (0.0116,), 3: (0.0116,)}, \'4.1.1/legacy\': {0: (0.0,), 1: (0.0116,), 3: (0.0116,)}, \'5.5.3/fast\': {0: (\'(1, "read_params_file: Can\\\'t open txt Error: Tesseract (legacy) engine requested, but comp\',), 1: (0.0116,), 3: (0.0116,)}, \'5.5.3/legacy\': {0: (0.0,), 1: (0.0116,), 3: (0.0116,)}}')),
 ('SearchablePdfs', 'Naps2', 'NapsPackage', 'naps2 console --help',
  'NAPS2 8.5.1 installed from the .deb as /usr/bin/naps2, and naps2 console --help returned 0 and listed --ocrlang, --install, --noprofile, -n, -f, -i and -o.',
  (X(_PRE + r'''
v = subprocess.run(['dpkg-query', '-W', '-f', '${Package} ${Version}', 'naps2'], capture_output=True, text=True).stdout
r = subprocess.run(['naps2', 'console', '--help'], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120); t = r.stdout + r.stderr
out = (v, shutil.which('naps2'), r.returncode, [k for k in ('--ocrlang', '--install', '--noprofile', '-n', '-f', '-i', '-o') if k in t])'''), "('naps2 8.5.1', '/usr/bin/naps2', 0, ['--ocrlang', '--install', '--noprofile', '-n', '-f', '-i', '-o'])")),
 ('SearchablePdfs', 'Naps2', 'NapsCommand', 'naps2 console -i frankenstein.png -o output.pdf',
  'The command naps2 console -i frankenstein.png -o output.pdf --install ocr-eng --ocrlang eng -n 0 -f -v returned 0 and a 1 page PDF whose text read with a character error rate of 0.0035 (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
shp(); args = ['-i', 'frankenstein.png', '-o', 'output.pdf', '--install', 'ocr-eng', '--ocrlang', 'eng', '-n', '0', '-f', '-v']
proc = subprocess.run(['naps2', 'console'] + args, capture_output=True, stdin=subprocess.DEVNULL, timeout=300)
pdf = subprocess.run(['pdftotext', 'output.pdf', '-'], capture_output=True, text=True).stdout; info = subprocess.run(['pdfinfo', 'output.pdf'], capture_output=True, text=True).stdout
out = (proc.returncode, type(proc.stdout).__name__, re.search(r'Pages:\s+(\d+)', info).group(1), cer(TRUTH, pdf), norm(pdf)[:40])'''), "(0, 'bytes', '1', 0.0035, 'THE MODERN PROMETHEUS,. 43 CHAPTER V. In')")),
 ('SearchablePdfs', 'Naps2', 'NapsOverwrite', 'naps2 console ... -f',
  'Run a second time without -f, NAPS2 printed File already exists. Use --force to overwrite. and still returned 0; with -f it returned 0 and wrote the file.',
  (X(_PRE + r'''
shp(); a = ['naps2', 'console', '-i', 'frankenstein.png', '-o', 'output.pdf', '--ocrlang', 'eng', '-n', '0']
r1 = subprocess.run(a + ['-f'], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300); r2 = subprocess.run(a, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300); r3 = subprocess.run(a + ['-f'], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300)
out = (r1.returncode, r2.returncode, r2.stdout.strip().split(' Path')[0], r3.returncode)'''), "(0, 0, 'File already exists. Use --force to overwrite.', 0)")),
 ('SearchablePdfs', 'Naps2', 'NapsInputLanguage', '-i spam.pdf[0:2]',
  'The page specifier of a PDF selects pages: [0] page 0, [0:2] pages 0 and 1, [-2:] pages 5 and 6 and [1:6:2] pages 1, 3 and 5 of a 7 page file, counted from 0.',
  (X(_PRE + r'''
d = wd(); F = ImageFont.truetype(FONTS['sans'], 90)
def label(t):
    im = Image.new('L', (700, 300), 255); ImageDraw.Draw(im).text((40, 90), t, font=F, fill=0); return im
ims = [label('spam%d' % i) for i in range(7)]; ims[0].save('spam.pdf', save_all=True, append_images=ims[1:])
res = {}
for spec in ('spam.pdf[0]', 'spam.pdf[0:2]', 'spam.pdf[-2:]', 'spam.pdf[1:6:2]'):
    r = subprocess.run(['naps2', 'console', '-i', spec, '-o', 'o.pdf', '--ocrlang', 'eng', '-n', '0', '-f'], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=300)
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', 'o.pdf'], capture_output=True, text=True).stdout).group(1))
    res[spec] = (r.returncode, [re.findall(r'\d', subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), 'o.pdf', '-'], capture_output=True, text=True).stdout)[0] for i in range(1, n + 1)])
out = (res, list(range(7))[0:2], list(range(7))[-2:], list(range(7))[1:6:2])'''), "({'spam.pdf[0]': (0, ['0']), 'spam.pdf[0:2]': (0, ['0', '1']), 'spam.pdf[-2:]': (0, ['5', '6']), 'spam.pdf[1:6:2]': (0, ['1', '3', '5'])}, [0, 1], [5, 6], [1, 3, 5])")),
 ('SearchablePdfs', 'OtherPdfRoutes', 'PillowPdf', "im.save('image_only.pdf', resolution=150)",
  'Pillow wrote a 1 page PDF of 542.4 x 322.56 pts from the 1130 by 672 image saved at 150 dpi, with no text in it (0 characters through pdftotext).',
  (X(_PRE + r'''
shp(); im = Image.open('frankenstein.png').convert('RGB'); im.save('image_only.pdf', resolution=150)
t = subprocess.run(['pdftotext', 'image_only.pdf', '-'], capture_output=True, text=True).stdout; info = subprocess.run(['pdfinfo', 'image_only.pdf'], capture_output=True, text=True).stdout
out = (len(norm(t)), re.search(r'Pages:\s+(\d+)', info).group(1), re.search(r'Page size:\s+(.*)', info).group(1), os.path.getsize('image_only.pdf') > 10000)'''), "(0, '1', '542.4 x 322.56 pts', True)")),
 ('SearchablePdfs', 'OtherPdfRoutes', 'TesseractPdf', "tess.image_to_pdf_or_hocr(im, extension='pdf')",
  "pytesseract's PDF bytes start with %PDF- and pdftotext read them with a character error rate of 0.0138 and 106 words in the bounding boxes, as many as the 106 of the page (MEASURED single runs with the Tesseract version 5.3.4).",
  (X(_PRE + r'''
shp(); im = Image.open('frankenstein.png').convert('RGB'); b = tess.image_to_pdf_or_hocr(im, extension='pdf'); open('t.pdf', 'wb').write(b)
t = subprocess.run(['pdftotext', 't.pdf', '-'], capture_output=True, text=True).stdout; bb = subprocess.run(['pdftotext', '-bbox', 't.pdf', '-'], capture_output=True, text=True).stdout
out = (type(b).__name__, b[:5], cer(TRUTH, t), bb.count('<word'), len(TRUTH.split()))'''), "('bytes', b'%PDF-', 0.0138, 106, 106)")),
 ('SearchablePdfs', 'OtherPdfRoutes', 'OcrmypdfRoute', 'ocrmypdf --image-dpi 150 in.png out.pdf',
  'ocrmypdf 17.13.0 exits with 2 and writes nothing for an image without a dpi, with --image-dpi 150 it exits 0 and the text reads with an error rate of 0.0035, and a file that already has text exits 6 unless --skip-text is given (MEASURED single runs with the Tesseract version 5.3.4).',
  (X(_PRE + r'''
shp(); OMP = '/home/claude/venv314_ch22_ocrmypdf/bin/ocrmypdf'
def om(*a):
    fo = tempfile.TemporaryFile('w+'); fe = tempfile.TemporaryFile('w+'); r = subprocess.run([OMP] + list(a), stdout=fo, stderr=fe, stdin=subprocess.DEVNULL, timeout=300); fe.seek(0); e = fe.read().strip().splitlines(); return r.returncode, (e[-1][:60] if e else '')
a = om('frankenstein.png', 'a.pdf'); b = om('--image-dpi', '150', 'frankenstein.png', 'b.pdf')
t = subprocess.run(['pdftotext', 'b.pdf', '-'], capture_output=True, text=True).stdout
c = om('b.pdf', 'c.pdf'); e = om('--skip-text', 'b.pdf', 'e.pdf')
out = (a[0], os.path.exists('a.pdf'), b[0], cer(TRUTH, t), c[0], e[0], subprocess.run([OMP, '--version'], capture_output=True, text=True).stdout.strip())'''), "(2, False, 0, 0.0035, 6, 0, '17.13.0')")),
 ('SearchablePdfs', 'SubprocessAndInput', 'SubprocessRun', 'subprocess.run(args, capture_output=True)',
  "subprocess.run returns an object with returncode (3), stdout (b'hi\\n') and stderr (b'err\\n') as bytes, text=True gives a str, and check=True raises CalledProcessError for a non-zero exit.",
  (X(_PRE + r'''
r = subprocess.run([sys.executable, '-c', 'print("hi"); import sys; print("err", file=sys.stderr); sys.exit(3)'], capture_output=True, stdin=subprocess.DEVNULL); s = subprocess.run([sys.executable, '-c', 'print("hi")'], capture_output=True, text=True)
try: subprocess.run([sys.executable, '-c', 'raise SystemExit(2)'], check=True)
except subprocess.CalledProcessError as e: c = (type(e).__name__, e.returncode, e.cmd[1:])
out = (r.returncode, r.stdout, r.stderr, s.stdout, c)'''), "(3, b'hi\\n', b'err\\n', 'hi\\n', ('CalledProcessError', 2, ['-c', 'raise SystemExit(2)']))")),
 ('SearchablePdfs', 'SubprocessAndInput', 'ProgramNotFound', "subprocess.run(['flatpak', ...])",
  'Naming a program that is not installed (the Windows console of NAPS2, the flatpak command) raises FileNotFoundError, and on this machine flatpak is not found while /usr/bin/naps2 is.',
  (X(_PRE + r'''
a = err(lambda: subprocess.run([r'C:\Program Files\NAPS2\NAPS2.Console.exe', '-v'], capture_output=True)); b = err(lambda: subprocess.run(['flatpak', 'run', 'com.naps2.Naps2', 'console'], capture_output=True))
out = (a[0], b[0], shutil.which('flatpak'), shutil.which('naps2'))'''), "('FileNotFoundError', 'FileNotFoundError', None, '/usr/bin/naps2')")),
 ('BookAndPractice', 'LlmCorrection', 'RealWordErrors', 'difflib.SequenceMatcher(None, a, b).get_opcodes()',
  'Of the 106 words of frankenstein.png the engine got 2 wrong, IT read as In and Motion read as motion, and both are real words that a spell checker would let pass.',
  (X(_PRE + r'''
shp(); t = tess.image_to_string(Image.open('frankenstein.png')); a = norm(TRUTH).split(); b = norm(t).split()
ops = [(tag, a[i1:i2], b[j1:j2]) for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if tag != 'equal']
out = (ops, len(a), len(b))'''), "([('replace', ['IT'], ['In']), ('replace', ['motion'], ['Motion'])], 106, 106)")),
 ('BookAndPractice', 'LlmCorrection', 'LowConfidenceWords', 'tess.image_to_data(im, output_type=tess.Output.DICT)',
  'The 106 words had a mean confidence of 94.5; the wrong In had 55, the lowest, and the wrong motion had 92, so confidence finds one of the two.',
  (X(_PRE + r'''
shp(); dd = tess.image_to_data(Image.open('frankenstein.png'), output_type=tess.Output.DICT)
w = [(t, int(float(c))) for t, c in zip(dd['text'], dd['conf']) if t.strip()]; a = norm(TRUTH).split(); b = [t for t, c in w]
bad = [i for i, (x, y) in enumerate(zip(a, b)) if x != y] if len(a) == len(b) else None
out = (len(w), [(w[i], a[i]) for i in bad], round(sum(c for t, c in w) / len(w), 1), sorted(c for t, c in w)[:6])'''), "(106, [(('In', 55), 'IT'), (('Motion', 92), 'motion')], 94.5, [55, 81, 81, 85, 90, 90])")),
 ('BookAndPractice', 'ScreenScraper', 'ScreenshotCrop', 'screen.crop((40, 30, 740, 130))',
  'A crop box of (40, 30, 740, 130) cut a 700 by 100 pixel region from a 1280 by 1024 screenshot, and reading it returned Page text on the screen.',
  (X(_PRE + r'''
LEFT, TOP, RIGHT, BOTTOM = 40, 30, 740, 130; screen = Image.new('RGB', (1280, 1024), 'white'); f = ImageFont.truetype(FONTS['sans'], 32); ImageDraw.Draw(screen).text((60, 50), 'Page text on the screen', font=f, fill='black')
img = screen.crop((LEFT, TOP, RIGHT, BOTTOM)); t = tess.image_to_string(img)
out = (screen.size, img.size, norm(t), img.mode)'''), "((1280, 1024), (700, 100), 'Page text on the screen', 'RGB')")),
 ('BookAndPractice', 'ScreenScraper', 'AppendOutput', "open('output.txt', 'a')",
  "Opening a file in mode 'a' three times and writing abc each time left 12 characters, in mode 'w' only 4.",
  (X(_PRE + r'''
d = wd(); text = 'abc\n'
for i in range(3):
    with open('output.txt', 'a', encoding='utf-8') as f: f.write(text)
for i in range(3):
    with open('write.txt', 'w', encoding='utf-8') as f: f.write(text)
out = (open('output.txt').read(), len(open('output.txt').read()), len(open('write.txt').read()))'''), "('abc\\nabc\\nabc\\n', 12, 4)")),
 ('BookAndPractice', 'ScreenScraper', 'NoDisplay', 'import pyautogui',
  "Without a DISPLAY the import of pyautogui ended with return code 1 and KeyError: 'DISPLAY'.",
  (X(_PRE + r'''
def child(code, drop=()):
    e = dict(os.environ)
    for k in drop: e.pop(k, None)
    fo = tempfile.TemporaryFile('w+'); fe = tempfile.TemporaryFile('w+'); r = subprocess.run([sys.executable, '-W', 'ignore', '-c', code], stdin=subprocess.DEVNULL, stdout=fo, stderr=fe, text=True, env=e, timeout=120); fe.seek(0)
    l = fe.read().strip().splitlines(); return r.returncode, (l[-1][:80] if l else '')
out = child('import pyautogui', drop=('DISPLAY', 'WAYLAND_DISPLAY'))'''), '(1, "KeyError: \'DISPLAY\'")')),
 ('BookAndPractice', 'BookCorrections', 'InversionAdvice', 'tesseract --print-parameters',
  'tessedit_do_invert defaults to 1 and is marked deprecated, invert_threshold is 0.7, tessedit_char_whitelist is empty and user_defined_dpi is 0.',
  (X(_PRE + r'''
r = subprocess.run(['tesseract', '--print-parameters'], capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout
rows = {l.split('\t')[0]: l.split('\t')[1:] for l in r.splitlines() if '\t' in l}
out = (rows['tessedit_do_invert'][0], 'deprecated' in rows['tessedit_do_invert'][1], rows['invert_threshold'][0], rows['tessedit_char_whitelist'], rows['user_defined_dpi'][0])'''), "('1', True, '0.7', ['', 'Whitelist of chars to recognize'], '0')")),
 ('BookAndPractice', 'BookCorrections', 'ShippedScriptNames', 'ast.walk(tree)',
  'preprocess_ocr.py has 190 lines and calls FileNotFileError, grayscale_image and open_image, which it never defines, and defines a function named open.',
  (X(_PRE + r'''
import ast, builtins
shp(); src = open('preprocess_ocr.py', encoding='utf-8').read(); tree = ast.parse(src)
defined = {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))} | {a.asname or a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names}
assigned = {t.id for n in ast.walk(tree) if isinstance(n, (ast.Assign, ast.AugAssign, ast.For, ast.With)) for t in ast.walk(n) if isinstance(t, ast.Name) and isinstance(t.ctx, ast.Store)} | {a.arg for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) for a in n.args.args}
called = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
und = sorted(c for c in called if c not in defined | assigned and not hasattr(builtins, c))
out = (len(src.splitlines()), und, sorted(n.name for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'open'))'''), "(190, ['FileNotFileError', 'grayscale_image', 'open_image'], ['open'])")),
 ('BookAndPractice', 'BookCorrections', 'AppendixAPins', "Requirement('pytesseract==0.3.10')",
  'Appendix A pins pytesseract==0.3.10 and pillow==10.4.0, and neither is satisfied by the installed 0.3.13 and 12.3.0.',
  (X(_PRE + r'''
from packaging.requirements import Requirement
pins = [Requirement('pytesseract==0.3.10'), Requirement('pillow==10.4.0')]
out = [(p.name, str(p.specifier), p.specifier.contains(md.version(p.name)), md.version(p.name)) for p in pins]'''), "[('pytesseract', '==0.3.10', False, '0.3.13'), ('pillow', '==10.4.0', False, '12.3.0')]")),
 ('BookAndPractice', 'BookCorrections', 'PlaceholderLink', "urlsplit('https://autbor.com/preprocessingocr')",
  'The link autbor.com/preprocessingocr has the host autbor.com and the path /preprocessingocr, and is the placeholder the page itself says it is.',
  (X(_PRE + r'''
import urllib.parse
a = urllib.parse.urlsplit('https://autbor.com/preprocessingocr'); b = urllib.parse.urlsplit('https://autbor.com/preprocessingocr/')
out = (a.netloc, a.path, b.path, a.path + '/' == b.path, a.scheme)'''), "('autbor.com', '/preprocessingocr', '/preprocessingocr/', True, 'https')")),
 ('BookAndPractice', 'BookCorrections', 'TopicsTheChapterOmits', 'tesseract --help-psm',
  'tesseract --help-psm lists 14 page segmentation modes (0 to 13) and --help-oem lists 4 engine modes (0 to 3), most of which the chapter never names.',
  (X(_PRE + r'''
h = subprocess.run(['tesseract', '--help-psm'], capture_output=True, text=True, stdin=subprocess.DEVNULL); o = subprocess.run(['tesseract', '--help-oem'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
t = h.stdout + h.stderr; p = [l.split()[0] for l in t.splitlines() if re.match(r'\s*\d+\s', l)]; oo = [l.split()[0] for l in (o.stdout + o.stderr).splitlines() if re.match(r'\s*\d+\s', l)]
out = (p, oo)'''), "(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'], ['0', '1', '2', '3'])")),
 ('BookAndPractice', 'Interpreters', 'PythonTargets', 'SpecifierSet(Requires-Python).contains(v)',
  'On Python 3.14.6 both pytesseract (Requires-Python >=3.8) and Pillow 12.3.0 accept the interpreter, and Pillow 12.3.0 does not accept Python 3.9.0.',
  (X(_PRE + r'''
from packaging.specifiers import SpecifierSet
v = '%d.%d.%d' % sys.version_info[:3]
out = (v, SpecifierSet(md.metadata('pytesseract')['Requires-Python']).contains(v), SpecifierSet(md.metadata('pillow')['Requires-Python']).contains(v), SpecifierSet(md.metadata('pillow')['Requires-Python']).contains('3.9.0'))'''), "('3.14.6', True, True, False)")),
 ('BookAndPractice', 'Interpreters', 'PillowReleases', "hasattr(Image, 'ANTIALIAS')",
  'Image.ANTIALIAS does not exist in Pillow 12.3.0 while Image.Resampling.LANCZOS and Image.LANCZOS do, and ImageDraw.textsize is gone.',
  (X(_PRE + r'''
out = (hasattr(Image, 'ANTIALIAS'), hasattr(Image.Resampling, 'LANCZOS'), hasattr(Image, 'LANCZOS'), md.version('pillow'), hasattr(ImageDraw.ImageDraw, 'textsize'), hasattr(Image.Image, 'get_flattened_data'))'''), "(False, True, True, '12.3.0', False, True)")),
 ('BookAndPractice', 'Interpreters', 'PytesseractReleases', 'inspect.signature(tess.image_to_string)',
  'pytesseract 0.3.13 has get_languages(config), image_to_string(image, lang, config, nice, output_type, timeout), the 8 functions image_to_string to get_tesseract_version and the Output kinds BYTES, DATAFRAME, DICT and STRING.',
  (X(_PRE + r'''
import inspect
p = tess.pytesseract
out = (list(inspect.signature(tess.get_languages).parameters), [m for m in ('image_to_string', 'image_to_data', 'image_to_boxes', 'image_to_osd', 'image_to_alto_xml', 'image_to_pdf_or_hocr', 'run_and_get_multiple_output', 'get_tesseract_version') if hasattr(tess, m)], sorted(x for x in dir(tess.Output) if not x.startswith('_')), list(inspect.signature(tess.image_to_string).parameters))'''), "(['config'], ['image_to_string', 'image_to_data', 'image_to_boxes', 'image_to_osd', 'image_to_alto_xml', 'image_to_pdf_or_hocr', 'run_and_get_multiple_output', 'get_tesseract_version'], ['BYTES', 'DATAFRAME', 'DICT', 'STRING'], ['image', 'lang', 'config', 'nice', 'output_type', 'timeout'])")),
]

CLAIMS = [
 (X(_PRE + r'''
out = (md.version('pytesseract'), md.version('pillow'), md.version('numpy'), md.version('opencv-python-headless'), sys.version_info[:3] == (3, 14, 6), str(tess.get_tesseract_version()))'''), "('0.3.13', '12.3.0', '2.5.4', '5.0.0.93', True, '5.3.4')"),
 ('(361832630 + 344943595, round((361832630 + 344943595) / 1e6), round(706776225 / 600e6, 2), 126 + 37)', '(706776225, 707, 1.18, 163)'),
 ('(round(15400601 / 4113088, 1), round(23466654 / 4113088, 1))', '(3.7, 5.7)'),
 ('(round(1130 / 150 * 72, 2), round(672 / 150 * 72, 2), 1130 * 672, 1211 * 606, 939 * 1198)', '(542.4, 322.56, 759360, 733866, 1124922)'),
 (X(_PRE + r'''
out = (lev('kitten', 'sitting'), cer('abcd', 'abxd'), round(2 / 578, 4), round(2 / 106, 4))'''), '(3, 0.25, 0.0035, 0.0189)'),
 (X(_PRE + r'''
z = zipfile.ZipFile(io.BytesIO(zipbytes())); names = [n for n in z.namelist() if '__MACOSX' not in n and not n.endswith('/')]
out = (len(zipbytes()), len(names), sum(n.endswith('.py') for n in names))'''), '(7759877, 91, 72)'),
]
ERRORS = []
BEH = [
 ['image_to_string returns a str that ends with a newline',
  "from PIL import Image, ImageDraw, ImageFont\nimport pytesseract as t\nim = Image.new('L', (700, 60), 255); ImageDraw.Draw(im).text((10, 10), 'Tesseract reads this line of text', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 32), fill=0)\ns = t.image_to_string(im); print(type(s).__name__, repr(s))",
  "str 'Tesseract reads this line of text\\n'"],
 ['a language with no file raises TesseractError',
  "from PIL import Image, ImageDraw, ImageFont\nimport pytesseract as t\nim = Image.new('L', (700, 60), 255); ImageDraw.Draw(im).text((10, 10), 'Tesseract reads this line of text', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 32), fill=0)\ntry:\n    t.image_to_string(im, lang='xyz')\nexcept t.TesseractError as e:\n    print(type(e).__name__, 'xyz.traineddata' in str(e))",
  'TesseractError True'],
 ['a program that does not exist raises TesseractNotFoundError',
  "from PIL import Image, ImageDraw, ImageFont\nimport pytesseract as t\nim = Image.new('L', (700, 60), 255); ImageDraw.Draw(im).text((10, 10), 'Tesseract reads this line of text', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 32), fill=0)\nt.pytesseract.tesseract_cmd = '/nowhere/tesseract'\ntry:\n    t.image_to_string(im)\nexcept t.TesseractNotFoundError as e:\n    print(type(e).__name__)",
  'TesseractNotFoundError'],
 ['a timeout that is too short raises RuntimeError',
  "from PIL import Image, ImageDraw, ImageFont\nimport pytesseract as t\nim = Image.new('L', (700, 60), 255); ImageDraw.Draw(im).text((10, 10), 'Tesseract reads this line of text', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 32), fill=0)\ntry:\n    t.image_to_string(im, timeout=0.001)\nexcept RuntimeError as e:\n    print(e)",
  'Tesseract process timeout'],
 ['the confidence is -1 above the word level',
  "from PIL import Image, ImageDraw, ImageFont\nimport pytesseract as t\nim = Image.new('L', (700, 60), 255); ImageDraw.Draw(im).text((10, 10), 'Tesseract reads this line of text', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 32), fill=0)\nd = t.image_to_data(im, output_type=t.Output.DICT)\nprint(sorted({c for c, l in zip(d['conf'], d['level']) if l < 5}), min(c for c, l in zip(d['conf'], d['level']) if l == 5) > 0)",
  '[-1] True'],
 ['a file opened in mode a keeps what is there and mode w starts again',
  "import tempfile, os\nos.chdir(tempfile.mkdtemp())\nfor m in 'aw':\n    for i in range(3):\n        with open(m + '.txt', m) as f: f.write('abc\\n')\nprint(len(open('a.txt').read()), len(open('w.txt').read()))",
  '12 4'],
 ['subprocess.run raises FileNotFoundError for a program that is not installed',
  "import subprocess\ntry:\n    subprocess.run(['no-such-program-xyz'])\nexcept FileNotFoundError as e:\n    print(type(e).__name__)",
  'FileNotFoundError'],
 ['the list of languages is sorted and holds osd',
  "import pytesseract as t\ng = t.get_languages(config='')\nprint(g == sorted(g), 'osd' in g, 'eng' in g)",
  'True True True'],
 ['a file name, a Pillow image and a NumPy array give the same text',
  "from PIL import Image, ImageDraw, ImageFont\nimport pytesseract as t\nim = Image.new('L', (700, 60), 255); ImageDraw.Draw(im).text((10, 10), 'Tesseract reads this line of text', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 32), fill=0)\nimport numpy as np, tempfile, os\nos.chdir(tempfile.mkdtemp()); im.save('l.png')\na = t.image_to_string('l.png'); print(a == t.image_to_string(Image.open('l.png')) == t.image_to_string(np.asarray(im)))",
  'True'],
 ['the PDF output of image_to_pdf_or_hocr is bytes that start with %PDF-',
  "from PIL import Image, ImageDraw, ImageFont\nimport pytesseract as t\nim = Image.new('L', (700, 60), 255); ImageDraw.Draw(im).text((10, 10), 'Tesseract reads this line of text', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 32), fill=0)\nb = t.image_to_pdf_or_hocr(im, extension='pdf'); print(type(b).__name__, b[:5])",
  "bytes b'%PDF-'"],
 ['pkgutil.find_loader does not exist in Python 3.14',
  "import pkgutil, sys\nprint(sys.version_info[:2], hasattr(pkgutil, 'find_loader'))",
  '(3, 14) False'],
]

BODY = {}
def _b(key, p1, p2):
    BODY[key] = p1 + "\n\n" + p2

# ---- InstallingTheTools ----
_b('InstallingTheTools',
 "The first part of the chapter, Installing Tesseract and PyTesseract, tells the reader to install the free Tesseract OCR engine on Windows, macOS or Linux, optionally with language packs, and then the PyTesseract package, which also installs Pillow [S]. The Tesseract documentation describes the engine as a command line program that is installed with apt on Linux, with brew on macOS and with an installer from UB Mannheim on Windows [TESS].",
 "Three ideas carry this subject: the engine (its version, its data folder and how pytesseract finds the program), the wrapper (the pytesseract release, the Python versions and the coupling with Pillow) and the installers of the three platforms. This study ran on Ubuntu 24.04 with the apt Tesseract 5.3.4 and its English data, pytesseract 0.3.13, Pillow 12.3.0 and Python 3.14.6 installed with uv; the Windows installer, the macOS installer and Homebrew were NOT EXECUTED [T].")
_b('TheEngine',
 "The chapter says PyTesseract works with the Tesseract OCR engine, a separate program that must be installed first, and that on Windows its folder must be on the PATH so that PyTesseract can reach tesseract.exe [S]. The Tesseract command line documentation lists the options --version and --list-langs of that program [TESS].",
 "Three leaves cover it: the version line, the data folder with the list of installed languages, and the way pytesseract looks the program up. The version of the engine matters because the same page gave different mistakes under Tesseract 4.1.1, 5.3.4 and 5.5.3 in this study [T].")
_b('EngineVersion',
 "The chapter never prints the version of Tesseract it used; it says only that the exact results may vary as the language packs are updated [S]. Wikipedia's article says version 4, released in 2018, added the LSTM-based engine, and version 5 was released in 2021 [WIKI].",
 "tesseract --version printed tesseract 5.3.4 on its first line, followed by the leptonica and image library versions, with exit status 0, and pytesseract.get_tesseract_version() returned 5.3.4 as a Version object [T]. Tesseract 5.5.3 and 4.1.1, built from source on the same machine, were used only where a program says so.")
_b('LanguageFolder',
 "The chapter lists the installed language packs through tess.get_languages() and says the packs are files with a .traineddata extension, such as jpn.traineddata [S]. The Tesseract command line documentation says --list-langs lists the languages whose data files are installed, and --tessdata-dir names another folder [TESS].",
 "On this machine tesseract --list-langs printed the folder /usr/share/tesseract-ocr/5/tessdata/ with the count (7) and then deu, eng, fra, jpn, osd, rus and tur [T]. osd is not a language but the orientation and script data that image_to_osd needs.")
_b('PathLookup',
 "The chapter says that on Windows the installation folder must be added to the PATH variable so PyTesseract can access tesseract.exe, and that Chapter 12 covered the PATH [S]. The pytesseract README says that when the executable is not on the PATH, the variable pytesseract.pytesseract.tesseract_cmd names it [PYT].",
 "The default value of tesseract_cmd was the bare name 'tesseract', which shutil.which found at /usr/bin/tesseract; setting it to r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe', a well-formed Windows path (ntpath.isabs gave True), raised TesseractNotFoundError on this Linux machine [T]. The same error is what a reader sees on any system when the PATH entry is missing.")
_b('TheWrapper',
 "The chapter introduces PyTesseract as the Python package that works with the Tesseract engine and says it installs Pillow with it; Appendix A pins pytesseract==0.3.10 and pillow==10.4.0 [S]. The PyPI page of pytesseract lists 0.3.13, uploaded on 2024-08-16, as the newest release [PYPI].",
 "Three leaves cover it: the release and what it requires, the line of pytesseract 0.3.10 that fails under Python 3.14, and the three ways of handing over an image. In this study pytesseract 0.3.13 ran under all eleven interpreters from Python 3.11.17 to 3.15.0b4, and the pinned 0.3.10 failed on 3.14.6 with ImportError [T].")
_b('PyTesseractRelease',
 "The chapter says to install the latest version of PyTesseract by following Appendix A, which pins pytesseract==0.3.10 [S]. PyPI lists 28 releases of pytesseract, from 0.1 (2014-02-06) to 0.3.13 (2024-08-16), with no 0.3.11 and no 0.3.12 among them [PYPI].",
 "pytesseract 0.3.13 was installed; its metadata required Pillow>=8.0.0 and packaging>=21.3 and Python>=3.8, so the chapter's remark that PyTesseract also installs the Pillow image library holds [T]. Three of the releases before 0.3.9 (0.3.4, 0.3.7 and 0.3.8) could not be installed as wheels by uv, and are marked NOT EXECUTED in the interpreter record [T].")
_b('FindLoaderBreak',
 "Appendix A pins pytesseract==0.3.10 [S]. The page of what is new in Python 3.14 lists the removal of pkgutil.find_loader, with importlib.util.find_spec as its replacement [PY].",
 "The source of pytesseract 0.3.10 imports find_loader from pkgutil and calls it for numpy and pandas, so on Python 3.14.6 the import stopped with ImportError: cannot import name 'find_loader' from 'pkgutil'; on Python 3.13.14 it worked with a DeprecationWarning, and 0.3.13 contains no find_loader [T]. Of the 22 statements of the chapter's listings 1, 2, 4, 5 and 6, 18 matched the book with the pins on Python 3.13.14 and 8 with the pins on Python 3.14.6, where the first statement raised the ImportError and the rest raised NameError [T].")
_b('PillowCoupling',
 "The chapter opens the image with Image.open() and passes the Image object to tess.image_to_string(); Appendix B answer 2 says PyTesseract works with the Pillow image library [S]. The pytesseract README shows image_to_string called with an opened image and with a file name [PYT].",
 "A drawn line (700 by 84 pixels, mode L) gave the same text 'Tesseract reads this line of text' with a newline for the path string, the Pillow Image and the NumPy array, with Pillow 12.3.0 [T]. An object that is none of these raised TypeError: Unsupported image object, and pytesseract replaces an alpha channel by white before it writes the file for the engine [T][PYT].")
_b('InstallerPlatforms',
 "The chapter gives one installer per platform: the UB Mannheim installer and the PATH on Windows, Homebrew on macOS (brew install tesseract and brew install tesseract-lang) and apt on Linux (sudo apt install tesseract-ocr, or tesseract-ocr-all) [S]. The Tesseract installation page lists apt, brew and the UB Mannheim installers [TESS].",
 "Only the Linux route could be run here. Three leaves cover the platforms: the Windows folder and the PATH, Homebrew, and apt; for the first two the study ran only what does not depend on the platform (path handling, the error a missing program gives) and marks the installers NOT EXECUTED [T].")
_b('WindowsInstaller',
 "The chapter says to download the installer from the UB Mannheim page, to tick the boxes for additional script and language data, and to add C:\\Program Files\\Tesseract-OCR to the PATH [S]. The page github.com/UB-Mannheim/tesseract/wiki answered HTTP 403 to the study's single request, so the installer page itself was not read [T].",
 "ntpath, the module that handles Windows paths on any system, split r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' into the drive C:, the folder C:\\Program Files\\Tesseract-OCR and the name tesseract.exe, and no such file exists here [T]. The installer, its checkboxes and the PATH dialog were NOT EXECUTED.")
_b('MacHomebrew',
 "The chapter says to install Homebrew from docs.brew.sh, then run brew install tesseract and, for the other languages, brew install tesseract-lang [S]. The Tesseract installation page lists brew among the ways to install the engine [TESS].",
 "This machine has no brew (shutil.which gave None) and no /opt/homebrew folder, and pointing tesseract_cmd at /opt/homebrew/bin/tesseract raised TesseractNotFoundError [T]. Homebrew and the macOS installation were NOT EXECUTED.")
_b('LinuxApt',
 "The chapter says sudo apt install tesseract-ocr installs the engine, sudo apt install tesseract-ocr-all every language, and a three-character code such as fra, deu or jpn in place of all one language [S]. The Tesseract installation page lists the apt packages [TESS].",
 "dpkg reported tesseract-ocr 5.3.4-1build5 and tesseract-ocr-eng 1:4.1.0-2 on this Ubuntu 24.04 machine, with the packs deu, eng, fra, jpn, osd, rus and tur installed and tesseract at /usr/bin/tesseract [T]. The English data of the package 4.1.0 are byte for byte the tessdata_fast file, so the apt package pairs the 5.3.4 engine with the fast data.")

# ---- ReadingAnImage ----
_b('ReadingAnImage',
 "The second part, OCR Fundamentals, shows the whole job in four lines: import pytesseract as tess and Pillow's Image, open ocr-example.png, and pass the Image to tess.image_to_string(), which returns the text [S]. It then scans a page of Frankenstein printed in 1831 (Figure 22-1) and finds that the result has mistakes [S].",
 "Three ideas carry this subject: the four lines and what the call returns, what comes back for a real page (its lines, its mistakes and how they vary with the engine and the data), and the other outputs of the wrapper (a table with confidences, PDF, hOCR, ALTO and the orientation). The pictures were those of the online materials, fetched and hash-checked, and pages the programs drew with known text; the study also looked at each picture with an image viewer [T].")
_b('TheFourLines',
 "The chapter's four lines import the two modules, open the image, call tess.image_to_string(img) and print the text, which is the first part of the introduction of The Big Book of Small Python Projects and ends with --snip-- [S]. The pytesseract README documents image_to_string and its keyword arguments [PYT].",
 "Three leaves cover it: opening the files, the call on a line of known text, and the return types. All three were run with pytesseract 0.3.13 and the apt Tesseract 5.3.4 [T].")
_b('OpenImage',
 "The chapter says to download ocr-example.png from the book's online resources and open it with Image.open() [S]. The online materials, a zip of 7,759,877 bytes with 91 files, hold ocr-example.png, frankenstein.png, frankenstein_jpn.png and preprocess_ocr.py, and the study fetched the zip and checked the SHA-256 of each [NSP].",
 "ocr-example.png is 939 by 1198 pixels in mode RGBA, frankenstein.png is 1130 by 672 in the palette mode P and frankenstein_jpn.png is 1211 by 606 in RGB, all three PNG [T]. Looking at them, ocr-example.png is a page of a book with a serif body, bold sans headings and a monospace code font; frankenstein.png is a yellowed page with a dark left edge, whose first word is I and a small capital T; frankenstein_jpn.png is 13 lines of black Japanese text on white [T].")
_b('ImageToString',
 "The chapter calls tess.image_to_string(img) and says Python makes the sophisticated algorithms accessible with four lines of code [S]. Appendix B answer 3 says the function accepts an Image object and returns a string [S].",
 "A 700 by 84 picture of the line 'Tesseract reads this line of text', drawn in DejaVu Sans at 32 pixels, came back as that line followed by a newline, a str, with a character error rate of 0.0 [T]. The trailing newline is part of the result, so a comparison strips it.")
_b('ReturnType',
 "Appendix B says image_to_string returns a string [S]. The pytesseract README documents an output_type argument with the values Output.BYTES, Output.DICT and Output.STRING [PYT].",
 "The default result was a str ending in a newline (its last characters xt and a newline); Output.BYTES gave the bytes b'xt\\n'; Output.DICT gave a dict with the single key text; and the stripped text equalled the drawn line [T].")
_b('WhatComesBack',
 "The chapter shows the result for frankenstein.png and says Tesseract misreads two characters ('Iv' for IT and 'Motion' for motion), adding that the exact results may vary as the language packs are updated [S]. It lists the issues to expect: end-of-line hyphens, no font information, odd white space, wrong characters and mixed columns [S].",
 "Four leaves cover it: the result for Figure 22-1, the line breaks it keeps, how the result differs between engines and data, and the hyphens. The page was read by the apt Tesseract 5.3.4 and then by 4.1.1 and 5.5.3 built from source [T].")
_b('FrankensteinOutput',
 "The chapter prints 14 lines beginning THE MODERN PROMETHEUS. 43 and CHAPTER V., and says Tesseract misreads two characters on the page [S]. The page of Figure 22-1 is from an 1831 print, which Wikipedia describes as the revised edition published under Mary Shelley's name [WIKI].",
 "The apt Tesseract returned 581 characters, 578 once white space is normalised, beginning 'THE MODERN PROMETHEUS. 43 CHAPTER V. In was on a dreary night of Novem'; the character error rate against the text read from the picture was 0.0035 (MEASURED single runs with the Tesseract version 5.3.4) [T]. The book prints Iv where this machine printed In, so the first mismatch with the book is already in the first word; the picture shows an I followed by a small capital T.")
_b('LineBreaks',
 "The chapter prints the result with a blank line after the heading and after CHAPTER V., and says the whitespace in the string may not match the text [S]. It also says the string does not conserve font or size information [S].",
 "Split at its newlines the result had 15 pieces, the last one empty, so 14 lines; it had empty lines after the heading and after the chapter line (the first lengths 25, 0, 10 and 0, then 55 and 55), no blank line inside the paragraph, 2 occurrences of two newlines in a row, and it ended with a full stop and a newline [T]. Each line of the page became a line of the string, so a program that wants running text has to join them itself.")
_b('ExactResultsVary',
 "The chapter ends the listing with the remark that the exact results may vary as the language packs are updated [S]. The Tesseract data files page says tessdata_fast holds integer models and tessdata_best the float models, and that the repositories differ in speed and accuracy [TESS].",
 "On frankenstein.png the first word came back as Iv with 4.1.1 and with 5.5.3 and the fast data, In with the apt 5.3.4, Ir with the best data of all three, and It with the legacy data under 4.1.1 and 5.5.3 [T]. On a noisy page drawn at 12 pixels the character error rate was 0.0154 with 4.1.1, 0.0193 with 5.3.4, 0.0154 with 5.5.3 and the fast data and 0.0077 with 5.5.3 and the best data, 3 distinct values in 5 runs (MEASURED single runs with the Tesseract versions named). Replaying the chapter's 22 statements matched the book on 18 with the apt Tesseract, 20 with 5.5.3 and the fast data, 20 with 4.1.1, 18 with 5.5.3 and the best data, 19 with all apt languages and 21 with all languages under 5.5.3 [T].")
_b('LineEndHyphens',
 "The chapter lists the first issue to expect: the string maintains any end-of-line hyphenation, for example in dig- and ital or pro- and grams [S]. It says always to consider OCR text imperfect and in need of correction [S].",
 "On ocr-example.png the apt Tesseract returned 51 lines, 10 of them blank lines between paragraphs, and 7 words broken at a line end by a hyphen: dig-ital, pro-grams, compre-hend, pro-grams, straight-forward, pro-gramming and graph-ics [T]. Joining the halves gave digital, programs, comprehend, straightforward, programming and graphics, but a sample sentence with two real compounds broken at a line end (well-known and self-contained) lost their hyphens when every hyphen was removed, so the join needs a word list [T].")
_b('OtherOutputs',
 "The chapter uses only image_to_string; the pytesseract README lists image_to_data, image_to_boxes, image_to_osd, image_to_alto_xml and image_to_pdf_or_hocr as well [PYT]. The chapter mentions text embedded in a PDF only through NAPS2 [S].",
 "Four leaves cover them: the data table with the word boxes, the confidence column, the PDF, hOCR and ALTO outputs, and the orientation report. On the drawn line each ran without a file left on disk, because pytesseract writes its own temporary files and deletes them [T].")
_b('ImageToData',
 "The chapter does not mention image_to_data. The pytesseract README documents it, with output_type=Output.DICT returning a dict of lists [PYT]. Its table has the columns level, page_num, block_num, par_num, line_num, word_num, left, top, width, height, conf and text [T].",
 "On the drawn line image_to_data returned those 12 columns and 10 rows: the levels 1 to 5 (1 page, 2 block, 3 paragraph, 4 line, 5 word), the 6 words Tesseract, reads, this, line, of and text at level 5, and positive left coordinates [T]. On frankenstein.png the same call as text gave 131 lines of 12 tab-separated columns.")
_b('ConfidenceScale',
 "The chapter does not say how sure Tesseract is about a word, although it warns that OCR text always needs correction [S]. The pytesseract README returns the conf column in the dict of image_to_data [PYT].",
 "Rows for the page, block, paragraph and line carried the confidence -1.0, and the 6 words of the drawn line carried 96.0, 96.0, 96.0, 95.0, 96.0 and 96.0, all between 0 and 100 [T]. On frankenstein.png the 106 words had a mean confidence of 94.5, and the wrongly read In had 55 (MEASURED single run with the Tesseract version 5.3.4) [T].")
_b('SearchableOutputs',
 "The chapter makes a searchable PDF only through NAPS2, and says a common use of OCR is a PDF of scanned images with searchable text [S]. The pytesseract README lists image_to_pdf_or_hocr and image_to_alto_xml [PYT].",
 "image_to_pdf_or_hocr(extension='pdf') returned bytes beginning %PDF-, extension 'hocr' returned HTML with ocr_page and ocrx_word elements, and image_to_alto_xml returned XML beginning <?xml with 6 String elements for the 6 words of the drawn line [T]. On frankenstein.png the hOCR had 107 ocrx_word elements for 106 words [T].")
_b('OsdOrientation',
 "The chapter says to rotate the image so that the lines of text are upright [S]. The pytesseract README lists image_to_osd, which reports orientation and script [PYT].",
 "For the upright drawn page image_to_osd gave orientation 0 and rotate 0; for the same page turned by 90 degrees (220 by 900 pixels) it gave orientation 270 and rotate 90 with the script Latin [T]. On a blank image it raised TesseractError (Too few characters), and image_to_string with --psm 0 raised FileNotFoundError because no text file is written in that mode [T].")

# ---- AccuracyAndPreprocessing ----
_b('AccuracyAndPreprocessing',
 "The part Preprocessing an Image warns that OCR text is always imperfect and lists nine preprocessing steps: separate columns, typewritten text, conventional fonts, upright lines, dark text on a light background, no dark borders, a small white border, enough contrast and no noise pixels; it points to a blog post on OpenCV [S]. The Tesseract documentation page on quality has sections on rescaling, binarisation, noise removal, dilation and erosion, rotation and deskewing, and borders [TESS].",
 "Five ideas carry this subject: measuring accuracy (edit distance, character and word error rates), what hurts (small letters, typefaces, tilt, noise, low contrast, white on black), what helps (grey, thresholds, enlarging, a border, deskewing), how the page is segmented (psm) and the configuration strings. Every error rate below is for a page the program drew with known text and read with the apt Tesseract 5.3.4: MEASURED single runs with the Tesseract version 5.3.4 [T].")
_b('MeasuringAccuracy',
 "The chapter has no measure of accuracy; it says OCR output is imperfect and should be corrected and that mistakes in numbers are harder to spot than misspelled words [S]. The character error rate is the Levenshtein edit distance divided by the length of the reference, and the word error rate is the same quotient over words [WIKI].",
 "Three leaves define the measures used in every later number: the edit distance, the character error rate after white space is normalised, and the word error rate. They are a few lines of the study's own code, not a library, and they were checked on frankenstein.png, whose text was read from the picture [T].")
_b('EditDistance',
 "Wikipedia's article on the Levenshtein distance defines it as the minimum number of single-character edits (insertions, deletions or substitutions) that change one word into the other and uses kitten and sitting as its example [WIKI]. The Python documentation of difflib offers SequenceMatcher for aligning two sequences [PY].",
 "The study's lev() gave 3 for kitten and sitting, 3 for the empty string and abc, 0 for equal strings, and 1 for It against Iv and for In against IT, the two kinds of mistake in the chapter's listing [T]. The distance between In and IT is 1 because only the second letter differs.")
_b('CharacterErrorRate',
 "A rate needs a reference. The study divides the edit distance by the number of characters of the reference after every run of white space has become one space, so that line breaks do not count as errors [T]. The Wikipedia article on word error rate gives the same quotient for words [WIKI].",
 "abcd read as abxd gave 0.25; 'a  b' and 'c' on two lines against 'a b c' gave 0.0; an empty reading of abcd gave 1.0, and so did abcd read as abcdefgh, because the quotient reaches 1.0 when the output is twice as long and can pass it (white text on black without inversion gave 1.0965) [T]. A rate of 1.0 therefore means nothing useful was read, not that every character was wrong.")
_b('WordErrorRate',
 "The word error rate counts words; the Wikipedia article gives it as the substitutions, deletions and insertions over the number of words in the reference [WIKI]. The chapter counts mistakes only by eye, naming Iv and Motion [S].",
 "'The cat sat' read as 'the cat sit' and as 'the cat' gave 1 of 3 words each, 0.3333; frankenstein.png has 106 words, 2 of them wrong, so its word error rate was 0.0189 against a character error rate of 0.0035, because one wrong letter spoils a whole word (MEASURED single run with the Tesseract version 5.3.4) [T].")
_b('WhatHurts',
 "The chapter says Tesseract is designed for typewritten dark text on light backgrounds where the text is level, that photographs and handwriting are out of reach, and that cursive and stylized fonts, tilt, noise and white text on black should be avoided [S]. The Tesseract quality page lists scale, skew, noise and borders among the causes of poor results [TESS].",
 "Six leaves cover it: letter size, typeface, tilt, noise, low contrast and white text on black. Each drew a text of 259 characters (the opening of the Frankenstein paragraph) with Pillow and read it with the apt Tesseract 5.3.4: MEASURED single runs with the Tesseract version 5.3.4 [T]. Looking at the drawn pages, the tilted, the noisy and the 8-pixel pages are all readable by eye, so the engine's limits are not a human's [T].")
_b('SmallText',
 "The Tesseract quality page says the engine works best on images of at least 300 dpi, so it may help to resize them [TESS]. The chapter does not mention size or resolution [S].",
 "On a 700-pixel page of DejaVu Sans the error rate was 0.2278 at 8 pixels, 0.0309 at 10, 0.0193 at 12 and 0.0116 at 16 and at 24 pixels; on a 900-pixel page 6 pixels gave 1.0 (nothing read) and 8 pixels 0.2394 (MEASURED single runs with the Tesseract version 5.3.4) [T]. The letters of a screenshot are small, so the screen scraper of the practice program needs one more rule: enlarge before reading.")
_b('FontChoice',
 "The chapter says to use conventional fonts, not cursive or stylized fonts [S]. Kurzweil's company, founded in 1974, built the first omni-font OCR system, which Wikipedia describes as able to recognize text in any normal font [WIKI].",
 "Six typefaces drawn at 24 pixels on a 900-pixel page read with error rates of 0.0116 (DejaVu Sans), 0.0 (DejaVu Serif), 0.0 (DejaVu Sans Mono), 0.0116 (DejaVu Sans Bold), 0.0 (Nimbus Roman) and 0.0 (Z003 italic script) (MEASURED single runs with the Tesseract version 5.3.4) [T]. So the advice to avoid stylized fonts did not matter for clean typeset faces of this size; it concerns handwriting and decoration, which were not measured.")
_b('Skew',
 "The chapter says to rotate the image so that the lines of text are perfectly upright and not skewed at a slight angle [S]. The Tesseract quality page has a section on rotation and deskewing [TESS].",
 "A page turned by 2 degrees read at 0.0154, but 5 degrees gave 0.5753 and 10 and 20 degrees gave 1.0, against 0.0116 upright; on the 900-pixel page of the corpus program 3 degrees already gave 0.6409 (MEASURED single runs with the Tesseract version 5.3.4) [T]. So 'a slight angle' in the chapter means about two degrees; the picture of a page turned by 5 degrees is easily readable by eye.")
_b('NoiseLevel',
 "The chapter says to remove small bits of noise pixels before scanning [S]. The Tesseract quality page has a section on noise removal and says some noise cannot be removed by the binarisation step [TESS].",
 "Gaussian noise with a standard deviation of 30 grey levels left the error rate at 0.0116, 60 gave 0.1313 and 90 gave 1.0; on the 900-pixel page of the corpus program 50 gave 0.0154 and 60 gave 1.0 (MEASURED single runs with the Tesseract version 5.3.4) [T]. The picture with a deviation of 60 looks speckled but readable to a person.")
_b('LowContrast',
 "The chapter says to adjust the brightness and contrast of the image so that the text stands out from the background [S]. The Tesseract quality page has a section on binarisation, the step that turns grey into black and white [TESS].",
 "In the corpus program grey 170 on 190 read as well as black on white (0.0116), but with light noise (a standard deviation of 12 grey levels) grey 100 on 160 read at 0.0656 while 110 on 140, 120 on 135 and 125 on 130 gave 1.0, against 0.0116 for black on white (MEASURED single runs with the Tesseract version 5.3.4) [T]. Contrast and noise together decide, not either alone.")
_b('WhiteOnBlack',
 "The chapter says to use dark text on a light background, not white text on a black background [S]. The Tesseract quality page says that for version 4.x one should use dark text on a light background [TESS].",
 "White text on black read at 0.0116 with the default settings, the same as black on white, because Tesseract tries an inverted line image (the parameter tessedit_do_invert is 1); with -c tessedit_do_invert=0 the error rate was 1.0965, and inverting the picture oneself and keeping the switch off gave 0.0116 again (MEASURED single runs with the Tesseract version 5.3.4) [T]. The chapter's advice describes what the engine does not need in 4.x and later.")
_b('WhatHelps',
 "The chapter says some of the preprocessing steps can be performed automatically with Python using the OpenCV library, and points to the blog post Preprocessing Images for OCR with Python and OpenCV at autbor.com/preprocessingocr [S]. PyPI lists opencv-python-headless 5.0.0.93 as the newest release, uploaded on 2026-07-02 [PYPI].",
 "Five leaves cover it: grey conversion, Otsu thresholding, enlarging, a white border and deskewing, done with Pillow, NumPy and OpenCV 5.0.0 on pages drawn by the program (MEASURED single runs with the Tesseract version 5.3.4) [T]. Not every step helped: thresholding made one page worse.")
_b('GrayscaleConversion',
 "The chapter's contrast step can be done with Pillow's ImageOps, whose reference lists autocontrast, invert, grayscale and expand [PILLOW]. The chapter itself does not mention grey conversion [S].",
 "convert('L') turned the colour pixel (167, 205, 128) into the grey 185 and left the error rate of a clean colour page at 0.0116, as before the conversion, so the engine did not need it; on the book's frankenstein.png the corpus program measured 0.0035 as shipped and 0.0017 after the grey conversion, and the first word changed from In to Iv [T]. A palette image such as that file (mode P) becomes a different picture to the engine when converted.")
_b('Binarization',
 "Wikipedia says Otsu's method, published by Nobuyuki Otsu in 1979, chooses a threshold automatically from the grey histogram [WIKI]. The Tesseract quality page says version 5.0.0 added the Leptonica-based Adaptive Otsu and Sauvola binarisation methods [TESS].",
 "Otsu's threshold on a page with noise of 45 was 136.0 and left only the values 0 and 255, but the error rate rose from 0.0154 to 0.0347 (MEASURED single runs with the Tesseract version 5.3.4) [T]. In the corpus program the median filter of 3 pixels followed by Otsu gave 0.0116 on a page with noise of 60, where the unfiltered page gave 1.0, so the order of the steps matters.")
_b('Upscaling',
 "The Tesseract quality page says the engine works best on images of at least 300 dpi, so it may be beneficial to resize them [TESS]. Pillow's Image.resize takes a size and a resampling filter [PILLOW].",
 "A page drawn at 9 pixels (600 by 76) read at 0.0579; enlarged 2, 3 or 4 times with Lanczos resampling it read at 0.0154 each time (MEASURED single runs with the Tesseract version 5.3.4) [T]. In the corpus program an 8-pixel page went from 0.2394 to 0.0386 at a factor of 2.")
_b('WhiteBorder',
 "The chapter says to add a small white border if the text runs up against the edge of the image [S]. The Tesseract quality page has a section called missing borders, which says text without any border may give problems [TESS].",
 "Text cropped tight to its ink (383 by 24 pixels) returned the empty string, and the same crop with a 10-pixel white border (403 by 44) returned 'Tesseract reads this line' with a newline [T]. In the corpus program a page drawn with a margin of 0 pixels still read at 0.0116, because its lines were not cut off, so the border rule matters for tight crops, such as those of the screen scraper.")
_b('Deskew',
 "The chapter says to rotate the image so the lines are upright, and that OpenCV can do some of the steps automatically [S]. The Tesseract quality page has a section on rotation and deskewing [TESS].",
 "OpenCV's minAreaRect of the dark pixels estimated the skew of a page turned by 6 degrees as -6.0 degrees; rotating back with Pillow lowered the error rate from 0.5985 to 0.0116 and enlarged the picture from 718 by 264 to 742 by 338 pixels (MEASURED single runs with the Tesseract version 5.3.4) [T]. In the corpus program the estimate was right for 3, 5 and 10 degrees and wrong for 30 (it found -20), where the result stayed at 1.0.")
_b('Segmentation',
 "The chapter says not to scan multicolumn images and to put each column into a separate image, because with tables or columns the string may mix the text and give it out of order [S]. The Tesseract manual page lists the page segmentation modes behind --psm [TESS].",
 "Three leaves cover it: the modes on a multi-line page, two columns, and a single line. The chapter never uses --psm; tesseract --help-psm listed 14 modes here, numbered 0 to 13 [T].")
_b('PsmModes',
 "The chapter never names a page segmentation mode; the Tesseract manual page lists them, from 0 (orientation and script detection only) to 13 (raw line), and says some are not implemented [TESS].",
 "--psm 3, 4, 6 and 11 read a page of 6 lines at 0.0116 with 6 non-empty lines each, --psm 7 (a single line) gave 1 line and an error rate of 0.9923 and --psm 13 gave 1 line at 0.9961 (MEASURED single runs with the Tesseract version 5.3.4) [T]. tesseract --help-psm printed the modes 0 to 13, with 2 marked not implemented.")
_b('ColumnLayout',
 "The chapter's rule is not to scan multicolumn images; its Summary says Tesseract works with typewritten dark text on light backgrounds where the text is level [S].",
 "Two columns of 330 pixels placed 360 pixels apart on a 700-pixel page read with the default mode column by column (alpha beta gamma delta epsilon zeta eta theta iota kappa lam), while --psm 6 joined them line by line (alpha beta gamma delta one two three four five six epsilon); each column cut out and read alone had an error rate of 0.0 [T]. In the corpus program columns 2 or 4 pixels apart merged (0.5819 and 0.5791) and 6 pixels or more did not (MEASURED single runs with the Tesseract version 5.3.4).")
_b('SingleLine',
 "The Tesseract manual page lists --psm 7 as the mode that treats the image as a single text line and --psm 8 as a single word [TESS].",
 "The line 'Order 4417-B shipped' read the same with the default mode and with --psm 7, while --psm 8 added a stray quotation mark in front [T]. In the corpus program a single digit read as 7 with --psm 7, 8, 10 and 13 and as the empty string with the default mode.")
_b('ConfigStrings',
 "The chapter passes only the image and lang to image_to_string. The pytesseract README documents a config string that is handed to the tesseract command line, and a timeout argument [PYT].",
 "Three leaves cover it: the character whitelist, the declared resolution and the time limit. For config='--psm 6' pytesseract ran tesseract with the temporary file, an output name, -l eng, --psm 6 and txt [T].")
_b('WhitelistDigits',
 "The Tesseract quality page names the parameter tessedit_char_whitelist as the way to limit the characters that are recognized [TESS]. The chapter says to pay special attention to mistakes in numbers [S].",
 "With -c tessedit_char_whitelist=0123456789- the line 'Order 4417-B shipped on 2026-10-13' became '4417-02026-10-13': the letters vanished and the B was read as a 0 [T]. In the corpus program a digits-only image '0123456789 0O8B 5S 1l 2Z 6G' read without the whitelist as '0123456789 008B 5S 1l 2Z 6G' and with it as '0123456789008855112266'. A whitelist removes look-alike letters by forcing digits, so it can also turn a wrong letter into a wrong digit.")
_b('UserDefinedDpi',
 "The Tesseract quality page says the engine works best at 300 dpi [TESS]. The chapter does not mention resolution [S].",
 "A page drawn at 9 pixels read at 0.0579 by default and with -c user_defined_dpi=70 but at 0.7452 with 300, and the PNG made by Pillow carried no dpi at all (None) (MEASURED single runs with the Tesseract version 5.3.4) [T]. Telling the engine a higher resolution than the letters have made it worse, not better.")
_b('TimeoutArgument',
 "The pytesseract README documents a timeout argument that stops Tesseract after the given number of seconds [PYT]. The chapter does not use it [S].",
 "timeout=0.001 raised RuntimeError with the text Tesseract process timeout, timeout=60 returned the text with an error rate of 0.0116, and timeout=0 returned normally [T]. A batch of hundreds of images can use it so that one broken page does not stop the run.")

# ---- LanguagesAndData ----
_b('LanguagesAndData',
 "The part Recognizing Text in Non-English Languages says Tesseract assumes English by default, lists the packs with tess.get_languages(), explains that the strings are mostly three-character ISO 639-3 language codes, passes lang='jpn' to read frankenstein_jpn.png, shows the gibberish of the wrong language and joins languages with a plus sign [S]. The installation section adds that installing all languages takes about 600MB [S].",
 "Three ideas carry this subject: the packs (the list, the folder and the size), the choice of language (the codes, the Japanese page, the wrong language, combinations, a missing pack and accented letters) and the kinds of data (fast, best and legacy) with the engine modes. The apt package carries the tessdata_fast English file; tessdata_best and tessdata were cloned from their GitHub repositories and each file was compared with the one the repository serves today [T].")
_b('LanguagePacks',
 "The chapter prints the result of tess.get_languages() as a list beginning afr, amh, ara, asm, aze and ending ton, tur, uig, ukr, urd, uzb, uzb_cyrl, vie, yid, yor, and says a pack is a file with the extension .traineddata [S]. The Tesseract data files page describes the repositories that hold those files [TESS].",
 "Three leaves cover it: the call and its list, the folder it is read from, and the size of all the packs. On this machine the list was the 7 packs of the apt installation, not the long list of the book [T].")
_b('GetLanguages',
 "Appendix B answer 5 says tess.get_languages() returns a list of language pack strings [S]. The pytesseract README documents get_languages(config='') [PYT].",
 "tess.get_languages(config='') returned the sorted list ['deu', 'eng', 'fra', 'jpn', 'osd', 'rus', 'tur'], 7 strings of which osd is not a language [T]. The listing of the chapter therefore does not match here, and with the tessdata_fast_all folder of all languages in use the apt Tesseract's replay of that listing matched the book [T].")
_b('DataFolder',
 "The chapter says to install the packs and to see which are installed with get_languages() [S]. The Tesseract command line documentation documents --tessdata-dir for naming the folder that holds the data files [TESS].",
 "A folder holding only eng.traineddata (4,113,088 bytes) gave ['eng'], and after deu.traineddata (1,525,436 bytes) was copied into it the next call gave ['deu', 'eng'], so the list is read from the folder at every call [T]. A program can therefore carry its own data folder instead of relying on the installation.")
_b('AllLanguagesSize',
 "The chapter says installing all languages adds about 600MB to the install size, and prints a list that begins afr, amh, ara and ends vie, yid, yor [S]. The Tesseract data files page says the tessdata_fast repository holds integer models for the languages and scripts [TESS].",
 "The tessdata_fast repository held 126 language files of 361,832,630 bytes and a script folder of 37 models of 344,943,595 bytes, 706,776,225 bytes in all, 707 MB, where the chapter says about 600MB; its list began afr, amh, ara and ended vie, yid, yor, as the book prints [T]. The 600MB is therefore low for the fast models of the repository.")
_b('ChoosingLanguage',
 "The chapter passes lang='jpn' for the Japanese page, shows lang='eng' giving gibberish on it, and joins codes with a plus sign, as in lang='eng+jpn' [S]. Appendix B answers 1 and 6 repeat the default and the combination [S].",
 "Six leaves cover it: the codes themselves, the Japanese image, the wrong language, combinations, a missing pack and accented letters. French, German, Turkish and Russian lines were drawn here with fonts that have their letters [T].")
_b('IsoCodes',
 "The chapter says the strings are mostly three-character ISO 639-3 codes with a few exceptions such as aze_cyrl, and the installation section says to use a three-character ISO 639 code such as fra, deu or jpn [S]. The Tesseract manual page says the language is given as an ISO 639-2 code [TESS]; ISO 639-3 is the SIL table and ISO 639-2 the Library of Congress list [ISO3][ISO2].",
 "In the corpus program 13 of the 126 names of tessdata_fast were not three letters (aze_cyrl, chi_sim, chi_sim_vert, chi_tra, chi_tra_vert, deu_latf, ita_old, jpn_vert, kat_old, kor_vert, spa_old, srp_latn and uzb_cyrl), and the apt list holds osd, which is no language [T]. lang='deu' read 'Die Größe der Straße und die Übung' correctly, while lang='ger', the ISO 639-2 bibliographic code of German, raised TesseractError (Error opening data file ger.traineddata); so the codes are Tesseract's own names, which for the languages shown agree with both tables.")
_b('JapaneseImage',
 "The chapter prints the first two and the last two lines of the Japanese text read from frankenstein_jpn.png with lang='jpn', beginning 第 5 剖 and containing 芝鬱 [S]. The Tesseract data files page lists jpn among the packs and the different data sets [TESS].",
 "The picture itself shows 第 5 章 and 憂鬱 on 13 lines; the apt Tesseract returned 13 lines beginning 第 5 剖 私が自分の労, which did not equal the book's two printed lines (error rates of 0.0426 and 0.0233 against the book's first two lines) and read 愛鬱 where the book prints 芝鬱 [T]. With the fast Japanese data under Tesseract 5.5.3 the replay equalled the book, while the best data gave 第 5 章 with spaces between the words and 901 characters instead of 538 (MEASURED single runs with the Tesseract versions named) [T].")
_b('WrongLanguage',
 "The chapter says that with the wrong language image_to_string returns Tesseract's best guess of what English characters the Japanese characters looked like, which is gibberish, and prints BS FABADOABOMEE as the start [S].",
 "On the top 200 pixels of frankenstein_jpn.png lang='eng' returned HSE ALBADOGEOMRE AON with 0 Japanese characters, while lang='jpn' returned 166 Japanese characters and began 第 5 章 私が自分の労; on the whole image the apt Tesseract wrote BS FAMSBADOABOMERE where the book prints BS FABADOABOMEE [T]. The gibberish varies with the engine and the data, the lesson does not.")
_b('CombinedLanguages',
 "The chapter says to combine language codes with a + character, as in lang='eng+jpn', and Appendix B answer 6 says to pass lang='eng+jpn' [S]. It says NAPS2's --ocrlang is passed directly to Tesseract, so 'eng+jpn+rus' works there too [S].",
 "On the line 'The cat is 猫 and the dog is 犬 today' lang='eng' returned 'The cat is 4 and the dog is % today', while 'jpn', 'eng+jpn' and 'jpn+eng' all returned the whole line correctly [T]. In the corpus program a generated Japanese line read at 0.0303 with jpn and with both combinations and at 1.0 with eng (MEASURED single runs with the Tesseract version 5.3.4).")
_b('MissingLanguage',
 "The chapter does not say what happens when a pack is not installed; it says only that the packs are installed with the instructions of its installation section [S].",
 "lang='xyz' raised TesseractError whose text says Error opening data file for xyz.traineddata, and the tesseract program exited with status 1 and printed the same text on its error stream [T]. In the corpus program 'eng+xyz' raised nothing and read the page at 0.0116, and lang='Japanese', the name written the book's way, raised the same error as xyz, so a name is not a code.")
_b('AccentedLetters',
 "The chapter's installation section names fra for French, deu for German and jpn for Japanese [S]. The Tesseract data files page lists these and the other languages with their files [TESS].",
 "French, German, Turkish and Russian lines read with their own pack gave error rates of 0.0, and with lang='eng' 0.1212, 0.1176, 0.1562 and 0.9 (MEASURED single runs with the Tesseract version 5.3.4) [T]. The English pack puts the nearest letter it knows in place of an accented one, and has nothing for Cyrillic.")
_b('ModelKinds',
 "The chapter does not distinguish kinds of language data. The Tesseract data files page distinguishes tessdata_fast, tessdata_best and the tessdata repository with the legacy and the LSTM engines, and says --oem chooses the engine [TESS].",
 "Two leaves cover it: the three English files and the engine modes. The apt package carries the fast kind; best and legacy were cloned from GitHub for the comparison of this study [T].")
_b('FastBestLegacy',
 "The Tesseract data files page says tessdata_fast holds integer models, tessdata_best the float models and tessdata both the legacy and the LSTM models [TESS]. The README of tessdata_fast calls it the fast integer version of the trained data and the README of tessdata_best the best trained models for LSTM [TESS].",
 "eng.traineddata was 4,113,088 bytes in tessdata_fast (SHA-256 starting 7d4322bd2a77), 15,400,601 in tessdata_best (8280aed0782f) and 23,466,654 in tessdata (daa0c97d651c), and the apt package's file was the fast one byte for byte; each file equalled the file the main branch of its GitHub repository served on 2026-10-13 [T]. The three kinds give 0.0035, 0.0017 and 0.0017 on frankenstein.png under Tesseract 5.5.3 (MEASURED single runs with the Tesseract version 5.5.3).")
_b('OemModes',
 "The Tesseract command line documentation documents --oem, with 0 for the legacy engine, 1 for the LSTM engine and 3 for the default [TESS]. The chapter does not use it [S].",
 "--oem 0 with the fast data failed with exit status 1 under Tesseract 4.1.1 and 5.5.3 (the legacy engine was requested but its components were not present), and with the legacy data it read the page at 0.0, while --oem 1 and 3 read it at 0.0116 with either data (MEASURED single runs with the Tesseract versions named) [T]. On frankenstein.png --oem 0 gave 0.0138.")

# ---- SearchablePdfs ----
_b('SearchablePdfs',
 "The part The NAPS2 Scanner Application says a common use of OCR is a PDF of scanned images with searchable text, recommends the free NAPS2 application, and runs it from Python with subprocess.run() and a list of command line arguments, among them -i, -o, --install, --ocrlang, -n 0 and -f [S]. It adds a mini language for the input and points to ocrmypdf [S].",
 "Three ideas carry this subject: NAPS2 itself (the package, the book's call, the overwrite flag and the input language), other ways of making a searchable PDF (Pillow alone, the Tesseract PDF output and ocrmypdf) and the subprocess side (the result of run() and a program that is not there). NAPS2 8.5.1 ran as the .deb package, with its own Tesseract; ocrmypdf 17.13.0 ran in its own environment [T].")
_b('Naps2',
 "The chapter describes NAPS2, Not Another PDF Scanner 2, as an open source application for flatbed scanners that can run Tesseract and add text to PDF documents without a scanner, and says it runs on Windows, macOS and Linux [S]. The NAPS2 command line documentation describes the console mode [NAPS].",
 "Four leaves cover it: the package, the book's call, the overwrite flag and the -i mini language. All ran with naps2 console; the Flatpak, Windows and macOS paths of the chapter were NOT EXECUTED [T].")
_b('NapsPackage',
 "The chapter says to download the installer from naps2.com/download, and on Linux to install the Flatpak with flatpak install and run it with flatpak run com.naps2.Naps2 [S]. The NAPS2 download page lists a Flatpak and the other installers [NAPS].",
 "This study installed the .deb package of NAPS2 8.5.1, which put naps2 at /usr/bin/naps2; naps2 console --help exited 0 and listed --ocrlang, --install, --noprofile, -n, -f, -i and -o [T]. The Flatpak route of the chapter was NOT EXECUTED because flatpak is not installed here.")
_b('NapsCommand',
 "The chapter runs NAPS2 with subprocess.run(naps2_path + ['-i', 'frankenstein.png', '-o', 'output.pdf', '--install', 'ocr-eng', '--ocrlang', 'eng', '-n', '0', '-f', '-v'], capture_output=True), and says the call creates output.pdf with one page whose text can be highlighted and copied [S]. The NAPS2 command line documentation lists --ocrlang and --install [NAPS].",
 "With naps2_path = ['naps2', 'console'] the call returned 0 and its stdout was bytes; output.pdf had 1 page and pdftotext read its text with an error rate of 0.0035, beginning THE MODERN PROMETHEUS,. 43 CHAPTER V. In (MEASURED single run with the Tesseract version 5.5.0 that NAPS2 carries) [T]. strace showed NAPS2 running its own /usr/lib/naps2/_linux/tesseract, version 5.5.0, on the data of the folder tesseract4/fast, and not the apt 5.3.4 of pytesseract [T].")
_b('NapsOverwrite',
 "The chapter says -f forces NAPS2 to overwrite output.pdf if a file with that name already exists [S]. The NAPS2 command line documentation documents the console options [NAPS].",
 "Without -f and with output.pdf present NAPS2 exited with status 0 and printed File already exists. Use --force to overwrite.; with -f it exited 0 again [T]. The status 0 does not say that nothing was written, so a program has to read the message or the file.")
_b('NapsInputLanguage',
 "The chapter describes a semicolon-delimited mini language with Python index and slice notation: spam.pdf[0];spam.pdf[5];eggs.pdf and spam.pdf[0:2];eggs.pdf[-1] [S].",
 "On a 7-page PDF drawn here, spam.pdf[0] gave page 0, spam.pdf[0:2] pages 0 and 1, spam.pdf[-2:] pages 5 and 6 and spam.pdf[1:6:2] pages 1, 3 and 5, exactly the slices Python gives for list(range(7)) [T]. In the corpus program cat.png;dog.png;moose.png gave 3 pages in that order and spam.pdf[0];spam.pdf[5];eggs.pdf gave 5 pages.")
_b('OtherPdfRoutes',
 "The chapter ends the NAPS2 section by recommending the ocrmypdf package for creating PDFs with embedded text [S]. The OCRmyPDF documentation says it adds an OCR text layer to scanned PDF files so that they become searchable [OMP].",
 "Three leaves cover it: a PDF made by Pillow alone, the PDF Tesseract makes through pytesseract and ocrmypdf. All three read frankenstein.png, with pdftotext and pdfinfo from poppler 24.02.0 to see what the files hold [T].")
_b('PillowPdf',
 "Pillow can save an image as a PDF; its file formats page documents the PDF writer and the dpi option [PILLOW]. The chapter notes that NAPS2 adds the text, which a plain PDF of a picture does not have [S].",
 "A PDF that Pillow made from frankenstein.png at a resolution of 150 had 1 page of 542.4 x 322.56 pts and no text: pdftotext found 0 characters [T]. Rendered again with pdftoppm at 150 dpi it gave a 1130 by 672 picture that Tesseract read at 0.0017 (MEASURED single run with the Tesseract version 5.3.4).")
_b('TesseractPdf',
 "The pytesseract README lists image_to_pdf_or_hocr, which returns a PDF whose invisible text layer holds the recognized words [PYT]. NAPS2 does the same through hOCR [NAPS].",
 "image_to_pdf_or_hocr(extension='pdf') returned bytes starting %PDF-, whose text pdftotext read with an error rate of 0.0138 and 106 word boxes for the 106 words (MEASURED single run with the Tesseract version 5.3.4) [T]. The producer of the file was Tesseract 5.3.4.")
_b('OcrmypdfRoute',
 "The OCRmyPDF documentation describes the tool as adding a text layer to scanned PDFs [OMP]. PyPI lists ocrmypdf 17.13.0, uploaded on 2026-09-28, which requires Python 3.11 or newer [PYPI].",
 "ocrmypdf 17.13.0 on frankenstein.png exited with status 2 and wrote nothing, because the PNG has no resolution; with --image-dpi 150 it exited 0 and the text layer had an error rate of 0.0035; a PDF that already has text exited 6 (PriorOcrFoundError) and --skip-text exited 0 (MEASURED single run with the Tesseract version 5.3.4) [T]. The output was a PDF/A-2b file produced with pikepdf 10.17.0.")
_b('SubprocessAndInput',
 "The chapter says Python scripts can use the subprocess module to run NAPS2 with command line arguments, so that no application window appears, and that Chapter 19 covered subprocess [S]. The Python documentation describes subprocess.run(), capture_output and the returncode attribute [PY].",
 "Two leaves cover it: what subprocess.run() returns, and the errors of a program path that does not exist. Both ran with the Python 3.14.6 subprocess module [T].")
_b('SubprocessRun',
 "The chapter calls subprocess.run() with capture_output=True and notes that capture_output=False shows the status text [S]. The Python documentation says run() returns a CompletedProcess whose returncode, stdout and stderr are bytes unless text is set, and that check=True raises CalledProcessError [PY].",
 "A child that printed hi, wrote err to its error stream and exited with 3 gave returncode 3, stdout b'hi\\n' and stderr b'err\\n'; with text=True stdout was the str 'hi\\n'; and with check=True an exit status of 2 raised CalledProcessError [T]. The book's call never reads proc.returncode, so a failure is silent.")
_b('ProgramNotFound',
 "The chapter gives three paths for NAPS2: r'C:\\Program Files\\NAPS2\\NAPS2.Console.exe' on Windows, '/Applications/NAPS2.app/Contents/MacOS/NAPS2' with 'console' on macOS, and flatpak run com.naps2.Naps2 console on Linux [S].",
 "The Windows path and the Flatpak call both raised FileNotFoundError here, since there is no C: drive and no flatpak (shutil.which gave None), while naps2 was found at /usr/bin/naps2 [T]. So the replay of the chapter's listing 7 as printed raised FileNotFoundError, and with the Linux path of this machine it ran.")

# ---- BookAndPractice ----
_b('BookAndPractice',
 "The last part of the chapter adds the large language model step that fixes mistakes the engine makes, the Summary, seven practice questions and the practice program Browser Text Scraper, ocrscreen.py [S]. Appendix B answers the seven questions: English is the default language, PyTesseract works with Pillow, image_to_string() takes an Image and returns a string, a photograph of a street sign will not do, tess.get_languages() lists the packs, lang='eng+jpn' joins two languages and NAPS2 makes PDFs with embedded OCR text [S].",
 "Four ideas carry this subject: the correction step, the screen scraper, the places where the book and the machines differ, and the interpreters. The language model step was NOT EXECUTED: there was no key for an online service and no local model on this machine [T]. Every answer of Appendix B was consistent with what the study measured; the differences are in the listings, the helper script and the pins [T].")
_b('LlmCorrection',
 "The chapter says a spell checker will not find OCR errors, because it flags the accurately recognized characters of words misspelled in the original and misses errors that give correctly spelled words, and proposes a large language model with a sample prompt [S]. It says to verify the model's output because it may miss mistakes or add new ones [S].",
 "Two leaves cover it: the two kinds of error on Figure 22-1 and the confidences. The model step itself was NOT EXECUTED; what could be measured is the input of that step, the text the engine returns, and the sample prompt of the book, which is 419 characters long [T].")
_b('RealWordErrors',
 "The chapter names 'Iv' for 'IT' and 'Motion' for 'motion' as the incorrectly scanned characters, and explains that a spell checker would miss errors that give correctly spelled words [S]. The Python documentation of difflib describes SequenceMatcher and its opcodes, which align two sequences [PY].",
 "difflib aligned the 106 words of the page with the 106 words of the result and found 2 replacements: IT as In and motion as Motion, both real English words [T]. A spell check against the 104,334 words of /usr/share/dict/words found no unknown token in the result, and iv, in, it and motion are all in that list, so the check flagged nothing, as the chapter says.")
_b('LowConfidenceWords',
 "The chapter says that identifying character mistakes requires understanding context [S]. The reCAPTCHA of 2009 handed the words that OCR could not read to people, one of a pair being a known control word [WIKI].",
 "image_to_data gave each of the 106 words of frankenstein.png a confidence: the mean was 94.5, the lowest six were 55, 81, 81, 85, 90 and 90, and the two wrong words were In (55) and Motion (92) [T]. In the corpus program only In was below 80, so a threshold of 80 would have sent one of the two errors to a human and no correct word, and a threshold of 90 would also have sent 43 (85), open (81) and a semicolon (81), which are correct (MEASURED single run with the Tesseract version 5.3.4).")
_b('ScreenScraper',
 "The practice program asks for ocrscreen.py: a screenshot taken with pyautogui, cropped to the text portion and passed to PyTesseract, with the text appended to output.txt; the template has LEFT = 400, TOP = 200, RIGHT = 1000 and BOTTOM = 800 [S]. The PyAutoGUI documentation says screenshot() needs Pillow and, on Linux, scrot or gnome-screenshot [PYA].",
 "Three leaves cover it: the crop box, the appending and what happens without a display. The corpus program ran ocrscreen.py on a virtual X display (Xvfb, 1280 by 1024) with the real ImageMagick display showing frankenstein.png; nobody saw the screen, so a real browser and a real PDF page were NOT EXECUTED [T].")
_b('ScreenshotCrop',
 "The template of the chapter takes pyautogui.screenshot() and crops it with img.crop((LEFT, TOP, RIGHT, BOTTOM)), the box of Pillow [S]. Chapter 21's box tuple is left, top, right and bottom [S].",
 "A 1280 by 1024 screen cropped to (40, 30, 740, 130) gave a 700 by 100 RGB picture that read 'Page text on the screen' [T]. In the corpus program the template's own constants (400, 200, 1000, 800) cut a 600 by 600 piece of the window and appended 361 characters with an error rate of 0.3824 against the whole page, while the constants (0, 0, 1130, 672) appended 581 characters at 0.0035, equal to the text of the file itself (MEASURED single runs with the Tesseract version 5.3.4).")
_b('AppendOutput',
 "The chapter asks the program to append the recognized text to the end of output.txt, calling open() in append mode [S]. The template leaves that as a TODO [S].",
 "Opening output.txt with mode 'a' three times added three copies of abc and a newline, 12 characters, while mode 'w' three times left 4 [T]. In the corpus program the second run of ocrscreen.py appended 581 characters to the 581 of the first, 1162 in all, 29 lines, as the book intends for scrolled pages.")
_b('NoDisplay',
 "The chapter says PyAutoGUI is covered in Chapter 23 and takes screenshots [S]. The PyAutoGUI documentation lists the Linux requirements for screenshots [PYA].",
 "Importing pyautogui in a process with neither DISPLAY nor WAYLAND_DISPLAY exited with status 1 and KeyError: 'DISPLAY' [T]. In the corpus program, with a display but no XDG_SESSION_TYPE=x11, pyautogui.screenshot() raised an Exception asking for gnome-screenshot, and with no ~/.Xauthority file the import raised XauthError, so the template needs a logged-in graphical session.")
_b('BookCorrections',
 "The book and the machines differ in several places a reader will meet: the white-on-black advice, the shipped helper script, the pins of Appendix A, the linked blog post and the topics the chapter leaves out [S]. The study found each by running or reading, not by assumption [T].",
 "Five leaves cover them. The pages the chapter points to answered HTTP 200 except github.com/UB-Mannheim/tesseract/wiki, which answered 403 to the study's request, and autbor.com/preprocessingocr, which answered 301 and then 200 [T]. The chapter's Figure 22-2 page autbor.com/embeddedfrankenstein/ answered 200 and holds an iframe of frankenstein.html [T].")
_b('InversionAdvice',
 "The chapter says to use dark text on a light background, not white text on a black background [S]. The Tesseract quality page says for version 4.x to use dark text on light background [TESS].",
 "tesseract --print-parameters listed tessedit_do_invert with the value 1 and a note that it is deprecated, to be removed in release 6, with invert_threshold (0.7) as the replacement; tessedit_char_whitelist was empty and user_defined_dpi was 0 [T]. So the advice describes a feature that is on by default, and the parameter that does it is on its way out.")
_b('ShippedScriptNames',
 "The online materials contain preprocess_ocr.py, a script that imports pytesseract and cv2; the chapter does not name it but the topic is its Preprocessing section [S]. The Python documentation says a name that is never bound raises NameError [PY].",
 "preprocess_ocr.py has 190 lines and calls 3 names it never defines, FileNotFileError, grayscale_image and open_image, and it defines a function named open that hides the built-in; run as a program with OpenCV installed it ended with NameError: name 'open_image' is not defined [T]. The post it was written for, autbor.com/preprocessingocr, says it is a placeholder.")
_b('AppendixAPins',
 "Appendix A pins pytesseract==0.3.10 and pillow==10.4.0, and says the pytesseract package is left out of the automateboringstuff3 package because it is fairly large [S]. PyPI lists pytesseract 0.3.13 and Pillow 12.3.0 as the newest releases [PYPI].",
 "Neither pin is satisfied by the installed 0.3.13 and 12.3.0: Requirement('pytesseract==0.3.10').specifier.contains('0.3.13') gave False, and so did the Pillow pin [T]. The pinned pytesseract could not be imported on Python 3.14.6 and the replay with the pins matched the book on only 8 of 22 statements there [T].")
_b('PlaceholderLink',
 "The chapter links to the blog post Preprocessing Images for OCR with Python and OpenCV at https://autbor.com/preprocessingocr, with no trailing slash [S]. The page the link leads to is titled Image Preprocessing for Tesseract OCR [PPA].",
 "The server answered 301 to the link and sent the browser to the same path with a trailing slash, /preprocessingocr/, which answered 200 with a page of 5,211 visible characters whose note says it is a placeholder blog post that will be updated in the future [T]. The only offline part of this is the path arithmetic: the two URLs differ by exactly a trailing slash.")
_b('TopicsTheChapterOmits',
 "The chapter does not use the words psm, page segmentation, image_to_data, tessdata, dpi, threshold, deskew, whitelist, hocr or timeout, although it does use the words confidence and OpenCV [S].",
 "tesseract --help-psm listed the 14 modes 0 to 13 and --help-oem listed the 4 engine modes 0 to 3 here, none of which the chapter names [T]. Every measured result of this study that changed an accuracy number (size, tilt, noise, segmentation, resolution and the data kind) rests on a topic the chapter leaves out.")
_b('Interpreters',
 "The chapter's code uses only calls that exist in every release of pytesseract and Pillow of the last years, and Appendix A pins pytesseract 0.3.10 and Pillow 10.4.0 [S]. Pillow 12.3.0 requires Python 3.10 or newer, and its documentation lists the Python versions each release supports [PILLOW].",
 "Three leaves cover it: the Python versions the packages accept, the Pillow calls that changed, and the pytesseract calls. One program of 19 items printed the same under 11 interpreters, Python 3.11.17, 3.12.3, 3.13.14, the seven releases 3.14.0 to 3.14.6 and 3.15.0b4, each with pytesseract 0.3.13 and Pillow 12.3.0, and 9 items printed the same under 14 Pillow releases from 9.5.0 to 12.3.0 [T].")
_b('PythonTargets',
 "The Python 3.14 documentation lists what was removed, among it pkgutil.find_loader [PY]. Pillow's Python support page lists the Python versions of each release [PILLOW].",
 "On Python 3.14.6 the Requires-Python of pytesseract (>=3.8) and of Pillow 12.3.0 (>=3.10) were both satisfied, and Python 3.9.0 would not satisfy Pillow's [T]. The newest Python on which the pinned pytesseract 0.3.10 imported was 3.13.14, with a DeprecationWarning.")
_b('PillowReleases',
 "The chapter does not resize or rotate images; the Pillow documentation of 12.0.0 lists Python 3.14 support among its changes [PILLOW]. Preprocessing recipes written for older Pillow can be tested against the newest release with a few hasattr calls [T].",
 "In Pillow 12.3.0 Image.ANTIALIAS was gone (hasattr gave False), Image.Resampling.LANCZOS and Image.LANCZOS existed, ImageDraw.textsize was gone and Image.get_flattened_data existed [T]. The 9 items of the pytesseract calls printed the same under all 14 Pillow releases from 9.5.0 to 12.3.0 on Python 3.11.17, so the wrapper does not depend on the Pillow release.")
_b('PytesseractReleases',
 "The PyPI page lists the releases of pytesseract; 0.3.13 of 2024-08-16 is the newest and the book pins 0.3.10 [PYPI]. The pytesseract README documents the functions of the wrapper [PYT].",
 "In 0.3.13 get_languages took config, image_to_string took image, lang, config, nice, output_type and timeout, the functions image_to_data, image_to_boxes, image_to_osd, image_to_alto_xml, image_to_pdf_or_hocr, run_and_get_multiple_output and get_tesseract_version existed, and Output had BYTES, DATAFRAME, DICT and STRING [T]. Across the releases 0.3.9, 0.3.10 and 0.3.13 only the confidence type changed, a str in 0.3.9 and an int from 0.3.10, and 0.3.4, 0.3.7 and 0.3.8 could not be installed as wheels (NOT EXECUTED).")

PUBS.sort(key=lambda p: p[0])
_CITE = {
 "S": "(Sweigart, 2025)", "PPA": "(Sweigart, 2026)", "PYA": "(Sweigart, 2026)", "NSP": "(No Starch Press, 2025)",
 "TESS": "(Tesseract OCR contributors, 2026)", "PYT": "(Pytesseract contributors, 2026)", "PYPI": "(Python Package Index, 2026)",
 "NAPS": "(NAPS Developers, 2026)", "OMP": "(OCRmyPDF contributors, 2026)", "PY": "(Python Software Foundation, 2026)",
 "WIKI": "(Wikipedia, 2026)", "ISO3": "(SIL International, 2026)", "ISO2": "(Library of Congress, 2026)", "PILLOW": "(Pillow Developers, 2026)",
 "T": "(This study, 2026)",
}
for _k in list(BODY):
    _t = BODY[_k]
    for _n, _v in _CITE.items():
        _t = _t.replace("[" + _n + "]", _v)
    BODY[_k] = _t.replace('"', "'")

# ---- gap closers: facts a finding states are also taught in the section ----
def _add(k, s):
    BODY[k] = BODY[k] + s
_add('OpenImage', " The zip holds 72 Python files and none of ocrscreen.py, output.pdf, cat.png, dog.png, moose.png, spam.pdf, eggs.pdf or output.txt, which the chapter creates or assumes, so the reader makes those; the publisher's book page for the chapter has 1 occurrence of Recognizing Text and 0 of Tesseract, OCR or NAPS2, because the page is a table of contents (This study, 2026).")
_add('ShippedScriptNames', " The listing of preprocess_ocr.py counted 190 lines in the online materials (This study, 2026).")
_add('BookAndPractice', " The chapter page was fetched on 2026-10-13 and returned 200 with 40,521 bytes; it holds 8 listings, 2 figures, 7 practice questions and 1 practice program, and its SHA-256 equals the chapterDigest of the book's own chapter ontology (This study, 2026). The one request for a photograph to Wikimedia Commons answered 429, so no photograph is used, and Python 3.15 was only the beta 3.15.0b4 (This study, 2026).")
_add('FindLoaderBreak', " With the pins in an empty Python, 0 of the 22 statements matched, because pytesseract was not installed there (This study, 2026).")
_add('ExactResultsVary', " Of those statements, the ones that differ are get_languages(), the first word Iv, the Japanese heading and the English gibberish (This study, 2026).")
_add('JapaneseImage', " The image frankenstein_jpn.png is 1211 by 606 pixels (This study, 2026).")

