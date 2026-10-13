"""Chapter 21 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter was read on automatetheboringstuff.com on 2026-10-13 (an HTTP fetch of https://automatetheboringstuff.com/3e/chapter21.html; the page
returned 200, 119,144 bytes, and its sha256, cb9e204bc3d3455abe51f81c96b6360f01491635805b5bea65e93643cb186a28, equals the chapterDigest the book's own chapter
ontology records; the commit the course pins was not opened). The online materials of the 3rd edition (the zip No Starch Press links from its book page, 7,759,877
bytes, sha256 dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916, 91 files) were downloaded at run time and hash-checked file by file for the four
files of this chapter (zophie.png, catlogo.png, guests.txt, resizeAndAddLogo.py); neither the zip nor any file of it is kept in this repository. 60 sources (the
chapter, its appendices, the 2nd edition's chapter 19, the Pillow and Matplotlib documentation and release notes, PyPI, the PNG, JPEG and CSS specifications, the
Python 3.14 documentation, the pages of the stories, uv and python.org) were each fetched on the same day and answered HTTP 200; the passages the research relies on
were looked for on each page (live observations). Every behaviour was executed under Python 3.14.6 (the newest 3.14 release uv offered) installed with uv on
Ubuntu 24.04 (Linux; the zone of the shell Europe/Istanbul) in dedicated environments: Pillow 12.3.0 with Matplotlib 3.11.2, NumPy 2.5.4 and pyperclipimg 0.2.0
(the newest); Pillow 10.4.0 with Matplotlib 3.9.2, the pins of Appendix A (Matplotlib 3.9.2 is the release the book writes as matplotlib==3.92, which does not exist),
built from source on 3.14.6 because neither has a CPython 3.14 wheel; the same two as wheels on Python 3.13.14; and an empty environment. Windows and macOS were never used.
The window and the clipboard programs ran on a virtual X display (Xvfb) with the real xclip, xdg-open, ImageMagick display and Tk 9.0 of the uv
Python; nobody saw the screen, a screenshot of it was taken and compared by pixels.
Not executed, and said so where it comes up: Windows and macOS (the Windows fill of rotated corners, the path C:\\folder_with_image_file, Paint and Photoshop); the
text of the PDFs of the JPEG standard and of JFIF (reached, not searched); the commit the course pins; Python 3.14.7 and later and the final 3.15.0 (uv offered
3.15.0b4); the Matplotlib window on a real screen (a virtual display was used); and a photograph (the single request to Wikimedia Commons answered 429).
The chapter's 138 interactive statements are replayed by sen0414_ch21_thirdparty_v1_0_0.py into 08-tooling/ch21-page/third_party_record_v1_0_0.json; what the public
sites and the shipped files did on the day, and what the virtual display did, is in ch21-page/live_observations_v1_0_0.json; what one program printed under eleven
interpreters (3.11, 3.12, 3.13, the seven 3.14 releases 3.14.0 to 3.14.6 and 3.15.0b4), and what small programs printed under 14 Pillow releases and 14 Matplotlib
runs, is in ch21-page/interpreter_record_v1_0_0.json. A claim not in this file was not made."""
__version__ = "1.0.2"
# 1.0.0 and 1.0.1 of the chapter 21 data module are already committed (the earlier builds of the chapter); this version rebuilds the chapter at the standard of
# chapters 13 to 20: two cross-referenced paragraphs per section, the chapter replayed as printed, the real Pillow and Matplotlib run in four environments,
# and the public sources as they answered on 2026-10-13. The data module is 1.0.2 because 1.0.0 and 1.0.1 are already committed.
CH = 21
DATE = "2026-10-13"
PYVER = "3.14.6"
TITLE = "Making graphs and manipulating images for an advanced course: chapter 21 and today's Pillow, ImageDraw, pyperclipimg and Matplotlib"
QUESTION = 'What does chapter 21 of the 3rd edition teach about images with Pillow (colours, boxes, crop, paste, resize, rotate, transpose, pixels, a logo project, drawing, text and the clipboard) and about graphs with Matplotlib (line, scatter, bar, pie, labels, saving and showing), which of its printed outputs, listings and statements still hold under Python 3.14.6 with Pillow 12.3.0 and Matplotlib 3.11.2 and with the Pillow 10.4.0 and Matplotlib 3.9.2 that its Appendix A pins, and what must an advanced course correct or add so that it matches the Pillow releases, the Matplotlib backends and the files the book ships?'
CQS = ('Which parts of a program that edits pictures, draws on them and plots graphs can be shown to work, and which can only be shown to fail, on a machine that has no screen, no clipboard owner and no Windows or macOS?',
       'Which printed outputs, programs, numbers and statements of the chapter differ in current releases of Python, Pillow and Matplotlib, with the versions its appendix pins, with the operating system of the reader, or in the files and pages it points to, and on what source?')
PUBS = [
 ('P01', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 21, Making Graphs and Manipulating Images (Al Sweigart, No Starch Press, 2025)', 'https://automatetheboringstuff.com/3e/chapter21.html', True),
 ('P02', 'Online materials of the 3rd edition, zip with 91 files, four of them the files of chapter 21 (No Starch Press, 2025)', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', False),
 ('P03', 'Automate the Boring Stuff with Python, 3rd edition - table of contents (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/', False),
 ('P04', 'Automate the Boring Stuff with Python, 3rd edition - book page (No Starch Press, 2025)', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', False),
 ('P05', 'Appendix A, Installing Third-Party Modules, with the versions the book pins (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixa.html', False),
 ('P06', 'Appendix B, Answers to the Practice Questions (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixb.html', False),
 ('P07', 'Automate the Boring Stuff with Python, 2nd edition - Chapter 19, Manipulating Images (Al Sweigart, No Starch Press, 2019)', 'https://automatetheboringstuff.com/2e/chapter19/', False),
 ('P08', 'Image module, Pillow reference (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/reference/Image.html', False),
 ('P09', 'ImageColor module, Pillow reference (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/reference/ImageColor.html', False),
 ('P10', 'ImageDraw module, Pillow reference (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html', False),
 ('P11', 'ImageFont module, Pillow reference (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/reference/ImageFont.html', False),
 ('P12', 'Tutorial, Pillow handbook (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/handbook/tutorial.html', False),
 ('P13', 'Image file formats, Pillow handbook (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html', False),
 ('P14', 'Concepts, Pillow handbook (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/handbook/concepts.html', False),
 ('P15', 'ImageGrab module, Pillow reference (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html', False),
 ('P16', 'ImageShow module, Pillow reference (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/reference/ImageShow.html', False),
 ('P17', 'Pillow 9.1.0 release notes (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/releasenotes/9.1.0.html', False),
 ('P18', 'Pillow 9.4.0 release notes (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/releasenotes/9.4.0.html', False),
 ('P19', 'Pillow 10.0.0 release notes (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/releasenotes/10.0.0.html', False),
 ('P20', 'Pillow 10.1.0 release notes (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/releasenotes/10.1.0.html', False),
 ('P21', 'Pillow 11.0.0 release notes (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/releasenotes/11.0.0.html', False),
 ('P22', 'Pillow 12.0.0 release notes (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/releasenotes/12.0.0.html', False),
 ('P23', 'Deprecations and removals, Pillow documentation (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/deprecations.html', False),
 ('P24', 'Python support, Pillow installation (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/installation/python-support.html', False),
 ('P25', 'About Pillow, the history of the PIL fork (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/about.html', False),
 ('P26', 'Release notes index, Pillow documentation (Pillow Developers, 2026)', 'https://pillow.readthedocs.io/en/stable/releasenotes/index.html', False),
 ('P27', 'matplotlib.pyplot.plot (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html', False),
 ('P28', 'matplotlib.pyplot.scatter (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html', False),
 ('P29', 'matplotlib.pyplot.bar (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html', False),
 ('P30', 'matplotlib.pyplot.pie (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pie.html', False),
 ('P31', 'matplotlib.pyplot.show (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.show.html', False),
 ('P32', 'matplotlib.pyplot.savefig (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html', False),
 ('P33', 'Matplotlib Application Interfaces (APIs), user guide (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/users/explain/figure/api_interfaces.html', False),
 ('P34', 'Backends, user guide (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/users/explain/figure/backends.html', False),
 ('P35', 'Interactive figures and asynchronous programming, user guide (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/users/explain/figure/interactive.html', False),
 ('P36', 'API changes in Matplotlib 3.11.0 (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/api/prev_api_changes/api_changes_3.11.0.html', False),
 ('P37', 'Dependencies, Matplotlib installation (Matplotlib Development Team, 2026)', 'https://matplotlib.org/stable/install/dependencies.html', False),
 ('P38', 'pyperclipimg README (Al Sweigart, 2024)', 'https://raw.githubusercontent.com/asweigart/pyperclipimg/main/README.md', False),
 ('P39', 'PyPI JSON metadata of pillow (Python Package Index, 2026)', 'https://pypi.org/pypi/pillow/json', False),
 ('P40', 'PyPI JSON metadata of matplotlib (Python Package Index, 2026)', 'https://pypi.org/pypi/matplotlib/json', False),
 ('P41', 'PyPI JSON metadata of pyperclipimg (Python Package Index, 2026)', 'https://pypi.org/pypi/pyperclipimg/json', False),
 ('P42', 'Portable Network Graphics (PNG) Specification, Third Edition (World Wide Web Consortium, 2026)', 'https://www.w3.org/TR/png-3/', False),
 ('P43', 'RFC 2083 - PNG (Portable Network Graphics) Specification Version 1.0 (Thomas Boutell, IETF, 1997)', 'https://www.rfc-editor.org/rfc/rfc2083', False),
 ('P44', 'ITU-T T.81, Digital compression and coding of continuous-tone still images, the JPEG standard (International Telecommunication Union, 1992)', 'https://www.w3.org/Graphics/JPEG/itu-t81.pdf', False),
 ('P45', 'JPEG File Interchange Format, version 1.02 (Eric Hamilton, 1992)', 'https://www.w3.org/Graphics/JPEG/jfif3.pdf', False),
 ('P46', 'CSS Color Module Level 4 (World Wide Web Consortium, 2026)', 'https://www.w3.org/TR/css-color-4/', False),
 ('P47', 'os - Miscellaneous operating system interfaces (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/os.html', False),
 ('P48', 'struct - Interpret bytes as packed binary data (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/struct.html', False),
 ('P49', 'What is new in Python 3.14 (Python Software Foundation, 2026)', 'https://docs.python.org/3.14/whatsnew/3.14.html', False),
 ('P50', 'tkinter - Python interface to Tcl/Tk (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/tkinter.html', False),
 ('P51', 'Tcl/Tk 9.0 (Tcl Developer Exchange, 2026)', 'https://www.tcl-lang.org/software/tcltk/9.0.html', False),
 ('P52', 'Russell A. Kirsch (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Russell_A._Kirsch', False),
 ('P53', 'Alpha compositing (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Alpha_compositing', False),
 ('P54', 'PNG (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/PNG', False),
 ('P55', 'JPEG (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/JPEG', False),
 ('P56', 'Matplotlib (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Matplotlib', False),
 ('P57', 'Python Imaging Library (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Python_Imaging_Library', False),
 ('P58', 'Web colors (Wikipedia, 2026)', 'https://en.wikipedia.org/wiki/Web_colors', False),
 ('P59', 'uv - Python versions (Astral documentation)', 'https://docs.astral.sh/uv/concepts/python-versions/', False),
 ('P60', 'Download Python (python.org)', 'https://www.python.org/downloads/', False),
]
CONCEPTS = [
 ('Section', 'Computer Image Fundamentals'),
 ('Section', 'Colors and RGBA Values'),
 ('Section', 'Coordinates and Box Tuples'),
 ('Section', 'Manipulating Images with Pillow'),
 ('Section', 'Working with the Image Data Type'),
 ('Section', 'Cropping Images'),
 ('Section', 'Pasting Images onto Other Images'),
 ('Section', 'Resizing Images'),
 ('Section', 'Rotating and Flipping Images'),
 ('Section', 'Changing Individual Pixels'),
 ('Section', 'Project 16: Add a Logo'),
 ('Section', 'Step 1: Open the Logo Image'),
 ('Section', 'Step 2: Loop Over All Files'),
 ('Section', 'Step 3: Resize the Images'),
 ('Section', 'Step 4: Add the Logo and Save the Changes'),
 ('Section', 'Ideas for Similar Programs'),
 ('Section', 'Drawing on Images'),
 ('Section', 'Shapes'),
 ('Section', 'Points'),
 ('Section', 'Lines'),
 ('Section', 'Rectangles'),
 ('Section', 'Ellipses'),
 ('Section', 'Polygons'),
 ('Section', 'A Drawing Example'),
 ('Section', 'Text'),
 ('Section', 'Copying and Pasting Images to the Clipboard'),
 ('Section', 'Creating Graphs with Matplotlib'),
 ('Section', 'Line Graphs and Scatter Plots'),
 ('Section', 'Bar Graphs and Pie Charts'),
 ('Section', 'Additional Components'),
 ('Section', 'Summary'),
 ('Section', 'Practice Questions'),
 ('Section', 'Practice Programs'),
 ('Section', 'Tile Maker'),
 ('Section', 'Identifying Photo Folders on the Hard Drive'),
 ('Section', 'Creating Custom Seating Cards'),
 ('Figure', 'Figure 21-1: the x- and y-coordinates of a 28x27 image'),
 ('Figure', 'Figure 21-2: the area represented by the box tuple (3, 1, 9, 6)'),
 ('Figure', 'Figure 21-6: nested for loops used with paste() duplicate the cat face'),
 ('Figure', 'Figure 21-8: the image rotated six degrees normally and with expand=True'),
 ('Figure', 'Figure 21-12: the left and top coordinates of the logo'),
 ('Figure', 'Figure 21-13: the logo with and without the third argument'),
 ('Figure', 'Figure 21-14: the resulting drawing.png image'),
 ('Figure', 'Figure 21-20: the example line graph with additional components'),
 ('Table', 'Table 21-1: Standard Color Names and Their RGBA Values'),
 ('Module', 'PIL.Image'),
 ('Module', 'PIL.ImageColor'),
 ('Module', 'PIL.ImageDraw'),
 ('Module', 'PIL.ImageFont'),
 ('Module', 'pyperclipimg'),
 ('Module', 'matplotlib.pyplot'),
 ('Module', 'os'),
 ('File', 'zophie.png'),
 ('File', 'catlogo.png'),
 ('File', 'guests.txt'),
 ('File', 'resizeAndAddLogo.py'),
]
FINDINGS = [
 ('F1', 'Background',
  "Chapter 21 of the 3rd edition, Making Graphs and Manipulating Images, teaches Pillow and Matplotlib: colours as RGBA tuples and box tuples, the Image methods crop, copy, paste, resize, rotate and transpose with getpixel and putpixel, Project 16 Add a Logo, drawing with ImageDraw and text with ImageFont, the clipboard through pyperclipimg, and line, scatter, bar and pie graphs; it ends with 12 practice questions and 3 practice programs, Tile Maker, the photo folder finder and the seating cards [P01]. The page was fetched on 2026-10-13 and returned 200 with 119,144 bytes, holds 31 listings, 20 figures and 1 table, and its sha256 equals the chapterDigest the book's own chapter ontology records [P01] [P03] [P04].",
  ['P01', 'P03', 'P04']),
 ('F2', 'The online materials',
  'The online materials of the 3rd edition (7,759,877 bytes, 91 files, 72 of them Python) hold zophie.png (816 by 1088, mode RGB), catlogo.png (100 by 95, mode LA), guests.txt with 5 names and resizeAndAddLogo.py, and none of zophie_xmas_tree.png, me_and_zophie.png, zophie_the_cat.jpg or a file with flower in its name among 184 entries of the zip, although the chapter says a public domain flower image is also available [P01] [P02]. The book page of the publisher has 1 occurrence of Making Graphs and 0 of Pillow, Matplotlib, zophie or catlogo [P04].',
  ['P01', 'P02', 'P04']),
 ('F3', 'The chapter replayed',
  "The 138 statements of the chapter's 25 interactive listings (31 listings in all) were replayed as printed in four environments. With Python 3.14.6, Pillow 12.3.0 and Matplotlib 3.11.2, 131 of 138 matched the book headless and 135 on a virtual X display; with Pillow 10.4.0 and Matplotlib 3.9.2, the book's pins, built from source on 3.14.6, 125 matched headless and 108 on the display; with the same pins as wheels on Python 3.13.14, 129 and 108; with an empty Python, 15 [P01] [P05]. The 3 that still differ with the newest packages and a display are os.chdir to a Windows path (FileNotFoundError), the font arial.ttf (OSError) and the printed tuple of plt.pie, which is a PieContainer [P01] [P11] [P30].",
  ['P01', 'P05', 'P11', 'P30']),
 ('F4', 'Project 16 as printed and as shipped',
  'The four listings of Project 16 joined as printed stop with SyntaxError: invalid character U+2013 at line 38, because the listing writes width - logo_width with an en dash; with a minus sign, and as the shipped resizeAndAddLogo.py (SHA-256 starting 4291c7cedd9d), the program exits with 0 and turns zophie.png into 225 by 300 pixels, where 300 / 1088 * 816 is the float 225.00000000000003 [P01] [P02]. The test needs both sides above 300, so a 1200 by 250 strip and a 250 by 900 column keep their size while a 1200 by 400 panorama becomes 300 by 100 and a 500 by 700 picture 214 by 300, and C.PNG and e.JPG are skipped because the extension test is case sensitive [P01] [P47].',
  ['P01', 'P02', 'P47']),
 ('F5', 'Table 21-1 and the colour names',
  "Table 21-1 gives Green as (0, 255, 0, 255), but of its 8 rows only Green differs from Pillow 12.3.0, which returns (0, 128, 0, 255) for green and (0, 255, 0, 255) for lime, the two CSS values; ImageColor.colormap holds 148 names, from aliceblue to yellowgreen, where the Pillow page says some 140 and the chapter more than 100, and 'transparent' raises ValueError [P01] [P09] [P46].",
  ['P01', 'P09', 'P46']),
 ('F6', 'Pixel density',
  "The chapter says Pillow's PNG files are 72 pixels per inch by default, but a PNG saved with no dpi has no pHYs chunk and no density to read back, and with dpi=(72, 72) the chunk holds 2835 pixels per metre, which Pillow reads as 72.009 dpi; a JPEG saved with defaults has jfif_density (1, 1) and jfif_unit 0, no unit, and Matplotlib's PNG carries 100 dpi [P01] [P13] [P42]. The sums of the seating-card text are right, 4 by 5 inches at 72 pixels per inch is 288 by 360 pixels, and the ImageFont page says the size of truetype() is in pixels, not points [P01] [P11].",
  ['P01', 'P11', 'P13', 'P42']),
 ('F7', 'The fill of a rotation',
  "The chapter says rotation gaps are black on Windows and transparent on macOS and Linux, but on Linux rotate(6) of the RGB zophie.png left (0, 0, 0) at the corner, an RGBA copy left (0, 0, 0, 0), and fillcolor='red' left (255, 0, 0): the fill follows the mode of the image, and the Pillow page of rotate() names a fill colour and no operating system; rotate(6, expand=True) of 816 by 1088 gives 926 by 1168 [P01] [P08].",
  ['P01', 'P08']),
 ('F8', 'plt.show and the figure',
  'With the Agg backend, which Matplotlib chooses when there is no display, plt.show() returns None at once and the figure stays, so the axes held 2 lines and 0 collections, then 2 and 2, then 4 bars and then 8 patches at the four calls of savefig(); with a real Tk window plt.show() blocks, the figure list is then empty, a second show returns at once, and a savefig() after it writes a blank image of 1 colour, as the Matplotlib page says [P01] [P31] [P34]. Appendix B answer 12, that plt.show() cannot be called twice because it resets the graph data, is true for a window and not for Agg [P06].',
  ['P01', 'P06', 'P31', 'P34']),
 ('F9', 'What pie and the colour cycle return',
  "plt.pie() returned a tuple of 3 in Matplotlib 3.7.5 to 3.10.8 and returns a PieContainer in 3.11.0 and 3.11.2, which unpacks into 3 parts with autopct and 2 without it and whose len() raises TypeError; the Matplotlib page marks the change as in 3.11, and the first line colour #1f77b4 is stored as a text up to 3.10.8 and as a tuple of floats from 3.11.0 [P30] [P36] [P40]. The book's printed tuple matches its pinned Matplotlib and not the newest [P01].",
  ['P01', 'P30', 'P36', 'P40']),
 ('F10', 'Pillow releases',
  'Across 14 Pillow releases from 9.5.0 to 12.3.0, ImageDraw.textsize and ImageFont.getsize existed only in 9.5.0 and were removed in 10.0.0; the default font became a FreeType font, Aileron Regular, in 10.1.0 and load_default(size=) was accepted from then on; Image.filename was an absolute path in 10.3.0, 10.4.0 and 11.0.0 and the plain name in the others; and Image.getdata() gives a DeprecationWarning from 12.1.0, saying it will be removed in Pillow 14 (2027-10-15) [P19] [P20] [P23] [P39].',
  ['P19', 'P20', 'P23', 'P39']),
 ('F11', 'The pins of Appendix A',
  'Appendix A pins pillow==10.4.0 and matplotlib==3.92, and PyPI has no Matplotlib 3.92 among 85 plain-numbered releases, so uv answers that no version exists; the first CPython 3.14 wheel is Pillow 11.3.0 and Matplotlib 3.10.5, so the pins need a source build on Python 3.14 [P05] [P39] [P40]. Matplotlib 3.9.2 built from source on 3.14.6 but savefig() and legend() raised RecursionError, and its TkAgg backend failed with ImportError (Failed to load Tcl_SetVar) against Tk 9.0 in both Python 3.14.6 and Python 3.13.14, while Matplotlib 3.11.2 opened its windows [P37] [P50] [P51].',
  ['P05', 'P37', 'P39', 'P40', 'P50', 'P51']),
 ('F12', 'Eleven interpreters',
  'One program of 35 items (Pillow colours, crop, paste, resize, rotate, flip, pixels, drawing, fonts and Matplotlib figures, pie and bar) printed the same under 11 interpreters, Python 3.11.17, 3.12.3, 3.13.14, 3.14.0 to 3.14.6 and 3.15.0b4, each with Pillow 12.3.0 and Matplotlib 3.11.2; every difference found came from the releases of the packages, not of Python [P39] [P40] [P60].',
  ['P39', 'P40', 'P60']),
 ('F13', 'Appendix B',
  'Appendix B answers question 6 with im.crop((0, 50, 50, 50)), whose size is (50, 0), where (0, 50, 50, 100) gives the 50 by 50 lower-left quarter; it calls the box left, top, width and height in answer 3 where the chapter says right and bottom; and it states in answer 12 that plt.show() resets the graph data [P01] [P06].',
  ['P01', 'P06']),
 ('F14', 'The clipboard and the viewer',
  'With xclip on a virtual X display pyperclipimg 0.2.0 copied a 40 by 30 RGB image and pasted it back as a PNG with equal pixels, and the clipboard offered image/png; with no DISPLAY copy() returned None and paste() raised ChildProcessError, with text on the clipboard paste() raised UnidentifiedImageError, and with no xclip the import raised NotImplementedError [P38] [P41] [P15]. Image.show() started xdg-open and the display program, and a screenshot of the screen matched 5 of 6 probe pixels of zophie.png [P16].',
  ['P15', 'P16', 'P38', 'P41']),
 ('F15', 'The second edition',
  "The 2nd edition's chapter 19, Manipulating Images, mentions Pillow 30 times, textsize 3 times and ImageFont 13 times, and neither matplotlib nor pyperclipimg; the 3rd edition's chapter 21 adds Matplotlib, the clipboard and 3 practice programs, and uses neither textsize nor getsize [P01] [P07].",
  ['P01', 'P07']),
 ('F16', 'Not executed',
  'Nothing ran on Windows or macOS, so the Windows fill and the paths of listing 4 are read, not run; the PDFs of the JPEG standard and of JFIF were reached but their text was not searched; the repository commit the course pins was not opened; and the photograph of the stories was not fetched because the single request to Wikimedia Commons answered 429 [P44] [P45] [P01].',
  ['P01', 'P44', 'P45']),
]

def X(code):
    """An executable example as one expression with no double quote and no line break: the code runs in a fresh
    namespace and the value of its variable out is the result."""
    lit = "'" + code.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace('"', "\\x22") + "'"
    return "(lambda g: (exec(%s, g), g['out'])[1])({})" % lit

# The helpers every example starts from: the modules, err() (what a call raised), wd() (make and enter a temporary folder), grad() (a 60 by 40 gradient made here),
# shp() (writes the four shipped files of the online materials into a temporary folder, fetched at run time and hash-checked, or reuses the zip kept in the
# temporary directory under its SHA-256) and child() (runs a small program in a child interpreter, with or without a display).
_PRE = r'''import io, os, re, sys, math, json, time, shutil, zipfile, hashlib, tempfile, warnings, subprocess, struct, importlib.metadata as md
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageChops, ImageShow
warnings.simplefilter('ignore')
def err(f):
    try: return ('ok', f())
    except BaseException as e: return (type(e).__name__, str(e))
def wd():
    d = tempfile.mkdtemp(); os.chdir(d); return d
def grad():
    im = Image.new('RGB', (60, 40))
    for x in range(60):
        for y in range(40): im.putpixel((x, y), (x * 4 % 256, y * 6 % 256, (x + y) * 3 % 256))
    return im
def sha(im): return hashlib.sha256(im.tobytes()).hexdigest()[:12]
ZIPSHA = 'dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916'
def zipbytes():
    p = os.path.join(tempfile.gettempdir(), 'ch21_materials_%s.zip' % ZIPSHA[:8])
    if not os.path.exists(p):
        import urllib.request
        rq = urllib.request.Request('https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0'})
        open(p + '.part', 'wb').write(urllib.request.urlopen(rq, timeout=180).read()); os.replace(p + '.part', p)
    b = open(p, 'rb').read(); assert hashlib.sha256(b).hexdigest() == ZIPSHA, 'the online materials differ from the recorded zip'
    return b
FILESHA = {'zophie.png': '5c5bf02fd0c95cee5d490a6daf3f1c4ccbbcab9fdc59bd8bba9564cad1462ba1', 'catlogo.png': '107740e7ca46ce7642b6940ff1232689bc3d34eb14c026813a61cfae45385db0',
           'guests.txt': 'e6136e39f829ae7380be4969b780c72bd8022a1a97efc399f0f2002ce1fd5164', 'resizeAndAddLogo.py': '4291c7cedd9dcf37b792ee7c20485902ad746b2743f66873ccc953bf4681634a'}
def shp():
    d = wd(); z = zipfile.ZipFile(io.BytesIO(zipbytes())); names = [n for n in z.namelist() if '__MACOSX' not in n]
    for f, h in FILESHA.items():
        data = z.read([n for n in names if n.endswith('/' + f)][0]); assert hashlib.sha256(data).hexdigest() == h, f; open(f, 'wb').write(data)
    return d
def child(code, drop=(), extra=None):
    e = dict(os.environ); e.update(extra or {})
    for k in drop: e.pop(k, None)
    fo = tempfile.TemporaryFile('w+'); fe = tempfile.TemporaryFile('w+')
    r = subprocess.run([sys.executable, '-W', 'ignore', '-c', code], stdin=subprocess.DEVNULL, stdout=fo, stderr=fe, text=True, env=e, timeout=120); fo.seek(0); fe.seek(0)
    return fo.read().strip()
'''
TAX = [
 # ---------------- ImageFundamentals / ColorRepresentation
 ('ImageFundamentals', 'ColorRepresentation', 'RgbaTuple', "ImageColor.getcolor('red', 'RGBA')",
  'An RGBA value is a tuple of four integers from 0 to 255, red, green, blue and alpha; Pillow returns (255, 0, 0, 255) for red and (255, 0, 0) in mode RGB, a new RGBA image is filled with the invisible (0, 0, 0, 0), and a pixel with alpha 0 keeps its colour numbers but cannot be seen.',
  (X(_PRE + r'''out = (ImageColor.getcolor('red', 'RGBA'), ImageColor.getcolor('red', 'RGB'), Image.new('RGBA', (1, 1)).getpixel((0, 0)), Image.new('RGBA', (1, 1), (10, 20, 30, 0)).getpixel((0, 0)), Image.new('RGB', (1, 1), (10, 20, 30)).getpixel((0, 0)))'''), '((255, 0, 0, 255), (255, 0, 0), (0, 0, 0, 0), (10, 20, 30, 0), (10, 20, 30))')),
 ('ImageFundamentals', 'ColorRepresentation', 'ColorNames', "ImageColor.getcolor('green', 'RGBA')",
  "ImageColor.getcolor() turns a colour name that is not case sensitive into a tuple through the dictionary ImageColor.colormap, which holds 148 names from aliceblue to yellowgreen; 'green' is (0, 128, 0, 255) and 'lime' is (0, 255, 0, 255), and the name 'transparent' is not in the dictionary and raises ValueError.",
  (X(_PRE + r'''out = (ImageColor.getcolor('green', 'RGBA'), ImageColor.getcolor('lime', 'RGBA'), len(ImageColor.colormap), ImageColor.getcolor('RED', 'RGBA') == ImageColor.getcolor('red', 'RGBA'), ImageColor.getcolor('CornflowerBlue', 'RGBA'), err(lambda: ImageColor.getcolor('transparent', 'RGBA'))[0], list(ImageColor.colormap)[0], list(ImageColor.colormap)[-1])'''), "((0, 128, 0, 255), (0, 255, 0, 255), 148, True, (100, 149, 237, 255), 'ValueError', 'aliceblue', 'yellowgreen')")),
 ('ImageFundamentals', 'ColorRepresentation', 'ImageModes', "Image.open('catlogo.png').mode",
  'The mode of an image names its channels: zophie.png of the online materials is RGB with no alpha channel and catlogo.png is LA, a grey channel with alpha, whose first pixel is (255, 0); a mode with an alpha channel cannot be written as JPEG, which raises OSError with the text cannot write mode RGBA as JPEG.',
  (X(_PRE + r'''shp(); z = Image.open('zophie.png'); c = Image.open('catlogo.png')
out = (z.mode, c.mode, c.size, c.getpixel((0, 0)), err(lambda: c.convert('RGBA').save('x.jpg'))[1], err(lambda: c.save('x.jpg'))[0])'''), "('RGB', 'LA', (100, 95), (255, 0), 'cannot write mode RGBA as JPEG', 'OSError')")),
 # ---------------- ImageFundamentals / CoordinateSystem
 ('ImageFundamentals', 'CoordinateSystem', 'PixelOrigin', 'g.getpixel((59, 0))',
  'A pixel is addressed by (x, y) with the origin (0, 0) at the top left, x growing to the right and y growing downward; the last pixel of a 60 by 40 image is (59, 39), (60, 0) raises IndexError with the text image index out of range, and a negative x such as -1 counts from the right edge and returns the pixel of x 59.',
  (X(_PRE + r'''g = grad()
out = (g.getpixel((0, 0)), g.getpixel((59, 0)), g.getpixel((-1, 0)) == g.getpixel((59, 0)), err(lambda: g.getpixel((60, 0))), err(lambda: g.getpixel((0, 40)))[0])'''), "((0, 0, 0), (236, 0, 177), True, ('IndexError', 'image index out of range'), 'IndexError')")),
 ('ImageFundamentals', 'CoordinateSystem', 'BoxTuple', "Image.new('RGB', (28, 27)).crop((3, 1, 9, 6)).size",
  'A box tuple has four integers in the order left, top, right, bottom, where right and bottom are one pixel beyond the region; the box (3, 1, 9, 6) of Figure 21-2 covers 6 columns and 5 rows, which is 30 pixels, and the width is right minus left, not the third number.',
  (X(_PRE + r'''box = (3, 1, 9, 6)
out = (Image.new('RGB', (28, 27)).crop(box).size, (box[2] - box[0]) * (box[3] - box[1]), (box[2] - box[0], box[3] - box[1]))'''), '((6, 5), 30, (6, 5))')),
 ('ImageFundamentals', 'CoordinateSystem', 'HalfOpenBox', 'g.crop((50, 30, 70, 50)).size',
  'A box includes its left and top edge and excludes its right and bottom edge, so crop((10, 5, 40, 35)) of a 60 by 40 image is 30 by 30; a box past the edge still gives the full size 20 by 20 with black pixels outside, a box with right less than left raises ValueError, and a box with right equal to left gives width 0.',
  (X(_PRE + r'''g = grad(); past = g.crop((50, 30, 70, 50))
out = (g.crop((10, 5, 40, 35)).size, past.size, past.getpixel((19, 19)), err(lambda: g.crop((40, 5, 10, 35))), g.crop((10, 5, 10, 35)).size)'''), '((30, 30), (20, 20), (0, 0, 0), (\'ValueError\', "Coordinate \'right\' is less than \'left\'"), (0, 30))')),
 # ---------------- ImageFundamentals / ImageObject
 ('ImageFundamentals', 'ImageObject', 'OpenAndSize', "Image.open('zophie.png').size",
  "Image.open() returns an Image object whose size is the tuple (816, 1088) for zophie.png, whose width and height attributes hold the two numbers, whose format is 'PNG' and format_description 'Portable network graphics', and whose mode is 'RGB'; the file is opened lazily and the pixels are read when they are first needed.",
  (X(_PRE + r'''shp(); im = Image.open('zophie.png'); w, h = im.size
out = (im.size, (w, h), im.format, im.format_description, im.mode, im.width, im.height)'''), "((816, 1088), (816, 1088), 'PNG', 'Portable network graphics', 'RGB', 816, 1088)")),
 ('ImageFundamentals', 'ImageObject', 'ImageFilename', "Image.open('zophie.png').filename",
  "The filename attribute holds the text the program passed to Image.open(); in Pillow 12.3.0 it is 'zophie.png' and os.path.isabs() of it is False, but Pillow 10.3.0, 10.4.0 and 11.0.0 return the absolute path, which is the answer the book's pinned Pillow 10.4.0 gives and the book's printed 'zophie.png' does not.",
  (X(_PRE + r'''shp(); im = Image.open('zophie.png')
out = (im.filename, md.version('pillow'), os.path.isabs(im.filename))'''), "('zophie.png', '12.3.0', False)")),
 ('ImageFundamentals', 'ImageObject', 'NewImage', "Image.new('RGBA', (20, 20))",
  "Image.new(mode, size, color) makes a blank image: with no colour an RGBA image is the invisible (0, 0, 0, 0) and an RGB image is black (0, 0, 0), and the colour may be a name such as 'purple', which gives (128, 0, 128, 255) for the 100 by 200 image of the chapter, or a tuple from ImageColor.getcolor().",
  (X(_PRE + r'''a = Image.new('RGBA', (20, 20)); b = Image.new('RGB', (1, 1)); p = Image.new('RGBA', (100, 200), 'purple')
out = (a.getpixel((0, 0)), b.getpixel((0, 0)), p.getpixel((0, 0)), p.size, Image.new('RGBA', (1, 1), ImageColor.getcolor('purple', 'RGBA')).getpixel((0, 0)))'''), '((0, 0, 0, 0), (0, 0, 0), (128, 0, 128, 255), (100, 200), (128, 0, 128, 255))')),
 ('ImageFundamentals', 'ImageObject', 'SaveFormats', "im.save('zophie.jpg')",
  'save() chooses the file format from the extension: zophie.png of 1,287,443 bytes saved as zophie.jpg is 125,433 bytes, and reading it back changes the largest channel value by 37, so JPEG is lossy; an extension Pillow does not know, such as .unknownext, raises ValueError with the text unknown file extension.',
  (X(_PRE + r'''shp(); im = Image.open('zophie.png'); im.save('zophie.jpg'); j = Image.open('zophie.jpg')
out = (os.path.getsize('zophie.jpg'), os.path.getsize('zophie.png'), j.format, [hi for lo, hi in ImageChops.difference(im, j).getextrema()], err(lambda: im.save('x.unknownext'))[1])'''), "(125433, 1287443, 'JPEG', [33, 36, 37], 'unknown file extension: .unknownext')")),
 # ---------------- ImageEditing / CropAndPaste
 ('ImageEditing', 'CropAndPaste', 'CropBox', 'im.crop((335, 345, 565, 560))',
  'crop() takes one box tuple, not four arguments, and returns a new Image without changing the original: the face box (335, 345, 565, 560) of zophie.png gives 230 by 215 pixels, the mode stays RGB, and the original is still 816 by 1088.',
  (X(_PRE + r'''shp(); im = Image.open('zophie.png'); face = im.crop((335, 345, 565, 560))
out = (face.size, im.size, face.mode, face is im)'''), "((230, 215), (816, 1088), 'RGB', False)")),
 ('ImageEditing', 'CropAndPaste', 'PasteInPlace', 'c.paste(face, (0, 0))',
  "paste(im, (left, top)) changes the image it is called on and returns None, so a program copies the picture first with copy(); after pasting the face into the copy the corner of the copy equals the face's corner while the original's corner is unchanged, and copy() and paste() have nothing to do with the clipboard.",
  (X(_PRE + r'''shp(); im = Image.open('zophie.png'); face = im.crop((335, 345, 565, 560)); before = im.getpixel((0, 0)); c = im.copy(); r = c.paste(face, (0, 0))
out = (r, c.getpixel((0, 0)) == face.getpixel((0, 0)), im.getpixel((0, 0)) == before, c.getpixel((0, 0)) == before, c is im)'''), '(None, True, True, False, False)')),
 ('ImageEditing', 'CropAndPaste', 'PasteMask', 'm.paste(logo, (0, 0), logo)',
  'The third argument of paste() is a mask: with the logo as its own mask the transparent corner leaves the red background (200, 0, 0, 255) alone, and without a mask the same corner is copied as (255, 255, 255, 0), so the invisible pixels of an RGBA copy overwrite what is below them.',
  (X(_PRE + r'''shp(); logo = Image.open('catlogo.png'); base = Image.new('RGBA', (100, 95), (200, 0, 0, 255)); m = base.copy(); m.paste(logo, (0, 0), logo); n = base.copy(); n.paste(logo.convert('RGBA'), (0, 0))
out = (m.getpixel((0, 0)), n.getpixel((0, 0)), logo.getpixel((0, 0)), m.getpixel((50, 47)) == n.getpixel((50, 47)))'''), '((200, 0, 0, 255), (255, 255, 255, 0), (255, 0), True)')),
 ('ImageEditing', 'CropAndPaste', 'TileLoop', 'for left in range(0, im.width, face.width)',
  "Two nested range() loops with the tile's width and height as the steps paste the tile at every grid position: the face of 230 by 215 pixels on the 816 by 1088 picture gives 4 columns and 6 rows, so 24 pastes from (0, 0) to (690, 1075), and the last column and row run past the edge and are cut off.",
  (X(_PRE + r'''shp(); im = Image.open('zophie.png'); face = im.crop((335, 345, 565, 560)); c = im.copy(); pos = []
for left in range(0, im.width, face.width):
    for top in range(0, im.height, face.height):
        c.paste(face, (left, top)); pos.append((left, top))
out = (len(pos), pos[:3], pos[-2:], len(range(0, 816, 230)), len(range(0, 1088, 215)))'''), '(24, [(0, 0), (0, 215), (0, 430)], [(690, 860), (690, 1075)], 4, 6)')),
 # ---------------- ImageEditing / ResizeAndRotate
 ('ImageEditing', 'ResizeAndRotate', 'ResizeInteger', 'im.resize((int(w / 2), int(h / 2)))',
  "resize() takes a tuple of two integers and returns a new image: half of 816 by 1088 is 408 by 544, the call with the height raised by 300 gives 816 by 1388, and a float such as 408.0 raises TypeError with the text 'float' object cannot be interpreted as an integer, which is why the chapter wraps the division in int().",
  (X(_PRE + r'''shp(); im = Image.open('zophie.png'); w, h = im.size
out = (im.resize((int(w / 2), int(h / 2))).size, im.resize((w, h + 300)).size, err(lambda: im.resize((w / 2, h / 2)))[1], im.size)'''), '((408, 544), (816, 1388), "\'float\' object cannot be interpreted as an integer", (816, 1088))')),
 ('ImageEditing', 'ResizeAndRotate', 'ResizeFilter', 'g.resize((30, 20))',
  'When no resample filter is given resize() uses bicubic for an RGB image, so its bytes equal those of Image.Resampling.BICUBIC and differ from NEAREST and from LANCZOS; the book never names a filter, and the argument resample= is the way to choose one.',
  (X(_PRE + r'''g = grad(); d = g.resize((30, 20)).tobytes()
out = (d == g.resize((30, 20), Image.Resampling.BICUBIC).tobytes(), d == g.resize((30, 20), Image.Resampling.NEAREST).tobytes(), d == g.resize((30, 20), Image.Resampling.LANCZOS).tobytes(), g.resize((30, 20)).size)'''), '(True, False, False, (30, 20))')),
 ('ImageEditing', 'ResizeAndRotate', 'RotateFill', 'g.rotate(6).getpixel((0, 0))',
  "rotate() turns an image counterclockwise and keeps its size, and the corners that no pixel reaches are filled with black (0, 0, 0) in mode RGB and with the invisible (0, 0, 0, 0) in mode RGBA; the keyword fillcolor, for example 'red', replaces the fill, so the colour depends on the image's mode.",
  (X(_PRE + r'''g = grad()
out = (g.rotate(6).getpixel((0, 0)), g.convert('RGBA').rotate(6).getpixel((0, 0)), g.rotate(6, fillcolor='red').getpixel((0, 0)), g.rotate(6).size, g.rotate(90).size)'''), '((0, 0, 0), (0, 0, 0, 0), (255, 0, 0), (60, 40), (60, 40))')),
 ('ImageEditing', 'ResizeAndRotate', 'RotateExpand', 'im.rotate(6, expand=True).size',
  'With expand=True rotate() makes the image big enough for the turned picture: 6 degrees turns 816 by 1088 into 926 by 1168, 90 degrees swaps it to 1088 by 816, and 180 degrees keeps 816 by 1088, while without expand the size always stays 816 by 1088 and the corners are cut off.',
  (X(_PRE + r'''shp(); im = Image.open('zophie.png')
out = (im.rotate(90).size, im.rotate(180).size, im.rotate(90, expand=True).size, im.rotate(180, expand=True).size, im.rotate(6, expand=True).size, im.rotate(6).size)'''), '((816, 1088), (816, 1088), (1088, 816), (816, 1088), (926, 1168), (816, 1088))')),
 # ---------------- ImageEditing / FlipAndPixels
 ('ImageEditing', 'FlipAndPixels', 'TransposeFlip', 'g.transpose(Image.FLIP_LEFT_RIGHT)',
  "transpose() returns a mirrored or quarter-turned image: Image.FLIP_LEFT_RIGHT makes the pixel at x 0 the pixel that was at x 59, FLIP_TOP_BOTTOM works on rows, and ROTATE_90 gives 40 by 60 from 60 by 40; in Pillow 12.3.0 Image.FLIP_LEFT_RIGHT is the integer 0 equal to Image.Transpose.FLIP_LEFT_RIGHT, which the chapter's older constant still reaches.",
  (X(_PRE + r'''g = grad()
out = (g.transpose(Image.FLIP_LEFT_RIGHT).getpixel((0, 0)) == g.getpixel((59, 0)), Image.FLIP_LEFT_RIGHT == Image.Transpose.FLIP_LEFT_RIGHT, type(Image.FLIP_LEFT_RIGHT).__name__, type(Image.Transpose.FLIP_LEFT_RIGHT).__name__, int(Image.Transpose.FLIP_LEFT_RIGHT), int(Image.Transpose.FLIP_TOP_BOTTOM), g.transpose(Image.Transpose.ROTATE_90).size, g.transpose(Image.Transpose.FLIP_TOP_BOTTOM).getpixel((0, 0)) == g.getpixel((0, 39)))'''), "(True, True, 'int', 'Transpose', 0, 1, (40, 60), True)")),
 ('ImageEditing', 'FlipAndPixels', 'PixelAccess', 'im.putpixel((0, 0), (210, 210, 210))',
  "getpixel() and putpixel() read and set one pixel: putting the RGB tuple (210, 210, 210) into an RGBA image stores (210, 210, 210, 255), the colour (169, 169, 169, 255) of 'darkgray' needs ImageColor.getcolor() because putpixel() with the name 'red' raises TypeError, and putpixel() returns None.",
  (X(_PRE + r'''im = Image.new('RGBA', (100, 100)); im.putpixel((0, 0), (210, 210, 210)); im.putpixel((0, 50), ImageColor.getcolor('darkgray', 'RGBA'))
out = (im.getpixel((0, 0)), im.getpixel((0, 50)), err(lambda: im.putpixel((1, 0), 'red')), im.putpixel((2, 0), (1, 2, 3, 4)))'''), "((210, 210, 210, 255), (169, 169, 169, 255), ('TypeError', 'color must be int or tuple'), None)")),
 # ---------------- LogoProject / LogoSetup
 ('LogoProject', 'LogoSetup', 'LogoConstants', 'SQUARE_FIT_SIZE = 300',
  "The shipped resizeAndAddLogo.py names its two settings at the top, SQUARE_FIT_SIZE = 300 and LOGO_FILENAME = 'catlogo.png', so that one edit changes the size or the logo, and it opens the 100 by 95 logo once with Image.open() before the loop; the file has 25 lines of code.",
  (X(_PRE + r'''shp(); s = open('resizeAndAddLogo.py').read()
out = ('SQUARE_FIT_SIZE = 300' in s, "LOGO_FILENAME = 'catlogo.png'" in s, len([l for l in s.splitlines() if l.strip() and not l.strip().startswith('#')]), Image.open('catlogo.png').size)'''), '(True, True, 25, (100, 95))')),
 ('LogoProject', 'LogoSetup', 'LogoFileLoop', "filename.endswith('.png') or filename.endswith('.jpg')",
  "The program loops over os.listdir('.') and skips every name that does not end in the lower case .png or .jpg and the logo itself, so a.png and b.jpg are processed while C.PNG, e.JPG, d.jpeg and n.txt are skipped; the order of os.listdir() is arbitrary.",
  (X(_PRE + r'''names = ['a.png', 'b.jpg', 'C.PNG', 'd.jpeg', 'catlogo.png', 'n.txt', 'e.JPG']
skip = lambda f: not (f.endswith('.png') or f.endswith('.jpg')) or f == 'catlogo.png'
out = ([f for f in names if not skip(f)], [f for f in names if skip(f)])'''), "(['a.png', 'b.jpg'], ['C.PNG', 'd.jpeg', 'catlogo.png', 'n.txt', 'e.JPG'])")),
 # ---------------- LogoProject / LogoResizeLogic
 ('LogoProject', 'LogoResizeLogic', 'BothSidesTest', 'if width > SQUARE_FIT_SIZE and height > SQUARE_FIT_SIZE:',
  'The program resizes an image only when both its width and its height exceed 300: a 1200 by 400 panorama becomes 300 by 100 and a 500 by 700 picture becomes 214 by 300, but a 1200 by 250 strip and a 250 by 900 column keep their size, so the 300 pixel limit is not kept for them.',
  (X(_PRE + r'''d = shp(); sizes = {'panorama.png': (1200, 400), 'strip.png': (1200, 250), 'tall.jpg': (500, 700), 'narrow.png': (250, 900)}
for n, s in sizes.items(): Image.new('RGB', s, 'gray').save(n)
r = subprocess.run([sys.executable, 'resizeAndAddLogo.py'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
out = (r.returncode, {n: Image.open('withLogo/' + n).size for n in sorted(sizes)})'''), "(0, {'narrow.png': (250, 900), 'panorama.png': (300, 100), 'strip.png': (1200, 250), 'tall.jpg': (214, 300)})")),
 ('LogoProject', 'LogoResizeLogic', 'ProportionMath', 'int((SQUARE_FIT_SIZE / height) * width)',
  'The new width is the 300 pixel limit divided by the height times the width and cut to an integer by int(): 300 / 1088 * 816 is the float 225.00000000000003 and gives 225, 300 / 700 * 500 gives 214 with int() and with round(), and int() always cuts toward zero.',
  (X(_PRE + r'''out = (300 / 1088 * 816, int(300 / 1088 * 816), int(300 / 700 * 500), round(300 / 700 * 500), int(300 / 500 * 700), 300 / 500 * 700)'''), '(225.00000000000003, 225, 214, 214, 420, 420.0)')),
 # ---------------- LogoProject / LogoPlacement
 ('LogoProject', 'LogoPlacement', 'CornerPosition', '(width - logo_width, height - logo_height)',
  "The logo's top-left corner goes to the image width minus the logo width and the image height minus the logo height, so a 100 by 95 logo on the 225 by 300 picture is pasted at (125, 205) and on a 300 by 100 picture at (200, 5), which puts its bottom-right corner on the image's corner.",
  (X(_PRE + r'''shp(); lw, lh = Image.open('catlogo.png').size
out = ((lw, lh), (225 - lw, 300 - lh), (300 - lw, 100 - lh))'''), '((100, 95), (125, 205), (200, 5))')),
 ('LogoProject', 'LogoPlacement', 'MaskedPaste', 'im.paste(logo_im, (width - logo_width, height - logo_height), logo_im)',
  "The logo is passed as its own third argument so that its transparent pixels are not pasted: the pixel at the logo's corner then equals the picture's own pixel, while the call without the mask puts (255, 255, 255) there, and a pixel in the middle of the cat is (0, 0, 0).",
  (X(_PRE + r'''shp(); logo = Image.open('catlogo.png'); base = Image.open('zophie.png').resize((225, 300)); pos = (225 - logo.width, 300 - logo.height)
a = base.copy(); a.paste(logo, pos, logo); b = base.copy(); b.paste(logo, pos)
out = (a.getpixel(pos) == base.getpixel(pos), b.getpixel(pos), a.getpixel((pos[0] + 50, pos[1] + 47)), a.mode)'''), "(True, (255, 255, 255), (0, 0, 0), 'RGB')")),
 ('LogoProject', 'LogoPlacement', 'OutputFolder', "os.makedirs('withLogo', exist_ok=True)",
  'The program writes the changed pictures to a folder withLogo under their old names and leaves the originals alone: two runs in a row both exit with code 0 because exist_ok=True stops makedirs from raising, and the file zophie.png has the same bytes after the runs.',
  (X(_PRE + r'''d = shp(); h = hashlib.sha256(open('zophie.png', 'rb').read()).hexdigest()
r1 = subprocess.run([sys.executable, 'resizeAndAddLogo.py'], capture_output=True, text=True, stdin=subprocess.DEVNULL); r2 = subprocess.run([sys.executable, 'resizeAndAddLogo.py'], capture_output=True, text=True, stdin=subprocess.DEVNULL)
out = (r1.returncode, r2.returncode, sorted(os.listdir('withLogo')), hashlib.sha256(open('zophie.png', 'rb').read()).hexdigest() == h, sorted(r1.stdout.splitlines()))'''), "(0, 0, ['zophie.png'], True, ['Adding logo to zophie.png...', 'Resizing zophie.png...'])")),
 ('LogoProject', 'LogoPlacement', 'ShippedScript', 'resizeAndAddLogo.py',
  'The file resizeAndAddLogo.py of the online materials has the SHA-256 4291c7cedd9d... and uses an ASCII minus sign in width - logo_width, whereas the listing of the web page has an en dash (U+2013) there, which Python reads as an invalid character and rejects with SyntaxError when the printed code is typed or pasted.',
  (X(_PRE + r'''shp(); s = open('resizeAndAddLogo.py', encoding='utf-8').read()
out = (hashlib.sha256(open('resizeAndAddLogo.py', 'rb').read()).hexdigest()[:12], '–' in s, err(lambda: compile(s.replace('width - logo_width', 'width – logo_width'), 'x', 'exec'))[0], s.splitlines()[0])'''), "('4291c7cedd9d', False, 'SyntaxError', '# https://autbor.com/resizeAndAddLogo.py - Resizes all images in')")),
 # ---------------- DrawingAndClipboard / ImageDrawShapes
 ('DrawingAndClipboard', 'ImageDrawShapes', 'DrawObject', 'ImageDraw.Draw(im)',
  'ImageDraw.Draw(im) returns an ImageDraw object that draws on the very image it was given, not on a copy: its drawing methods such as line() return None, and after drawing a red line along the top of a 10 by 10 image the pixel (5, 0) is (255, 0, 0).',
  (X(_PRE + r'''im = Image.new('RGB', (10, 10)); d = ImageDraw.Draw(im)
out = (type(d).__name__, d.line([(0, 0), (9, 0)], fill='red'), im.getpixel((5, 0)), im.getpixel((0, 5)), d.im is not None)'''), "('ImageDraw', None, (255, 0, 0), (0, 0, 0), True)")),
 ('DrawingAndClipboard', 'ImageDrawShapes', 'PointsAndLines', "draw.line([(0, 5), (9, 5)], fill='red', width=3)",
  'point() paints single pixels and takes either pairs or a flat list of numbers with the same result, 2 red pixels for two points, and line() paints one pixel wide unless width is given: a horizontal line from x 0 to 9 is 10 pixels and with width=3 it is 30 pixels.',
  (X(_PRE + r'''def red(im): return sum(1 for p in im.getdata() if p == (255, 0, 0))
def mk(f):
    im = Image.new('RGB', (12, 12)); f(ImageDraw.Draw(im)); return im
a = mk(lambda d: d.point([(1, 1), (3, 3)], fill='red')); b = mk(lambda d: d.point([1, 1, 3, 3], fill='red'))
out = (a.tobytes() == b.tobytes(), red(a), red(mk(lambda d: d.line([(0, 5), (9, 5)], fill='red'))), red(mk(lambda d: d.line([(0, 5), (9, 5)], fill='red', width=3))))'''), '(True, 2, 10, 30)')),
 ('DrawingAndClipboard', 'ImageDrawShapes', 'RectangleEllipse', "draw.rectangle((20, 30, 60, 60), fill='red')",
  'ImageDraw rectangle and ellipse boxes include their last pixel, unlike crop(): the rectangle (20, 30, 60, 60) paints 41 by 31, which is 1271 pixels; a box with the corners reversed raises ValueError with the text x1 must be greater than or equal to x0, and a rectangle with neither fill nor outline is drawn as a white outline.',
  (X(_PRE + r'''def count(f, c=(255, 0, 0)):
    im = Image.new('RGB', (100, 100)); f(ImageDraw.Draw(im)); return sum(1 for p in im.getdata() if p == c)
e = Image.new('RGB', (50, 50), 'blue'); ImageDraw.Draw(e).rectangle((5, 5, 20, 20))
out = (count(lambda d: d.rectangle((20, 30, 60, 60), fill='red')), 41 * 31, count(lambda d: d.rectangle((20, 30, 60, 60), fill='red')) == len(range(20, 61)) * len(range(30, 61)), err(lambda: ImageDraw.Draw(Image.new('RGB', (50, 50))).rectangle((60, 60, 20, 30)))[1], e.getpixel((5, 5)), e.getpixel((10, 10)))'''), "(1271, 1271, True, 'x1 must be greater than or equal to x0', (255, 255, 255), (0, 0, 255))")),
 ('DrawingAndClipboard', 'ImageDrawShapes', 'PolygonDrawing', "draw.polygon([(0, 0), (10, 0), (0, 10)], fill='red')",
  'polygon() joins the points in order and closes the shape from the last point to the first by itself: the triangle (0, 0), (10, 0), (0, 10) fills 66 pixels of an 11 by 11 image, including the closing edge at (0, 5) and the corner (5, 5), and leaves (10, 10) black.',
  (X(_PRE + r'''im = Image.new('RGB', (11, 11)); ImageDraw.Draw(im).polygon([(0, 0), (10, 0), (0, 10)], fill='red')
out = (sum(1 for p in im.getdata() if p == (255, 0, 0)), im.getpixel((0, 5)), im.getpixel((5, 5)), im.getpixel((10, 10)))'''), '(66, (255, 0, 0), (255, 0, 0), (0, 0, 0))')),
 ('DrawingAndClipboard', 'ImageDrawShapes', 'DrawingExample', "draw.line([(i, 0), (200, i - 100)], fill='green')",
  "The chapter's 200 by 200 drawing example makes a black border, a blue rectangle, a red ellipse, a brown polygon and ten green lines; the green lines start at y 0 and overwrite the border there, so the pixel (100, 0) is (0, 128, 0, 255), 654 pixels are green, and 1271 are blue.",
  (X(_PRE + r'''im = Image.new('RGBA', (200, 200), 'white'); draw = ImageDraw.Draw(im)
draw.line([(0, 0), (199, 0), (199, 199), (0, 199), (0, 0)], fill='black'); draw.rectangle((20, 30, 60, 60), fill='blue'); draw.ellipse((120, 30, 160, 60), fill='red')
draw.polygon(((57, 87), (79, 62), (94, 85), (120, 90), (103, 113)), fill='brown')
for i in range(100, 200, 10): draw.line([(i, 0), (200, i - 100)], fill='green')
P = list(im.getdata())
out = (im.getpixel((100, 0)), im.getpixel((50, 45)), im.getpixel((0, 0)), im.getpixel((0, 199)), sum(1 for p in P if p == (0, 128, 0, 255)), sum(1 for p in P if p == (0, 0, 255, 255)))'''), '((0, 128, 0, 255), (0, 0, 255, 255), (0, 0, 0, 255), (0, 0, 0, 255), 654, 1271)')),
 # ---------------- DrawingAndClipboard / TextDrawing
 ('DrawingAndClipboard', 'TextDrawing', 'DefaultFont', 'ImageFont.load_default(size=20)',
  'ImageFont.load_default() returns a FreeTypeFont of size 10 named Aileron Regular in Pillow 12.3.0, and load_default(size=20) a size 20; before Pillow 10.1.0 it returned a small bitmap font that has no size argument, so draw.text() without a font argument gave different sizes in different releases.',
  (X(_PRE + r'''f = ImageFont.load_default(); g = ImageFont.load_default(size=20)
out = (type(f).__name__, f.size, type(g).__name__, g.size, f.getname())'''), "('FreeTypeFont', 10, 'FreeTypeFont', 20, ('Aileron', 'Regular'))")),
 ('DrawingAndClipboard', 'TextDrawing', 'TrueTypeFont', "ImageFont.truetype('DejaVuSans.ttf', 32)",
  "ImageFont.truetype(file, size) loads a TrueType font by file name from the system folders: 'arial.ttf' of the chapter raises OSError with the text cannot open resource on this Linux machine, while 'DejaVuSans.ttf' gives a FreeTypeFont named DejaVu Sans of size 32.",
  (X(_PRE + r'''f = ImageFont.truetype('DejaVuSans.ttf', 32)
out = (err(lambda: ImageFont.truetype('arial.ttf', 32)), f.getname(), f.size, type(f).__name__)'''), "(('OSError', 'cannot open resource'), ('DejaVu Sans', 'Book'), 32, 'FreeTypeFont')")),
 ('DrawingAndClipboard', 'TextDrawing', 'TextMeasuring', "draw.textbbox((100, 150), 'Howdy', font=f)",
  "textbbox() returns the box (100, 156, 209, 187) of 'Howdy' in 32 pixel DejaVu Sans at (100, 150) and textlength() the width 109.06, so the right edge 209 lies beyond the 200 pixel image and the word is cut off; draw.textsize() and font.getsize() no longer exist.",
  (X(_PRE + r'''im = Image.new('RGBA', (200, 200), 'white'); d = ImageDraw.Draw(im); f = ImageFont.truetype('DejaVuSans.ttf', 32); box = d.textbbox((100, 150), 'Howdy', font=f)
out = (box, round(d.textlength('Howdy', font=f), 2), box[2] > im.width, hasattr(d, 'textsize'), hasattr(f, 'getsize'), f.getbbox('Howdy'))'''), '((100, 156, 209, 187), 109.06, True, False, False, (0, 6, 109, 37))')),
 # ---------------- DrawingAndClipboard / ClipboardAndViewer
 ('DrawingAndClipboard', 'ClipboardAndViewer', 'ShowViewer', 'im.show()',
  'Image.show() writes the picture to a temporary file and starts a viewer program, and returns None; on this Linux machine Pillow lists XDGViewer and DisplayViewer first, so on a machine with no viewer on the PATH, as in the headless replay of this study, the call returned None, showed nothing and raised no error.',
  (X(_PRE + r'''out = ([type(v).__name__ for v in ImageShow._viewers][:2], callable(ImageShow.show), Image.Image.show.__name__)'''), "(['XDGViewer', 'DisplayViewer'], True, 'show')")),
 ('DrawingAndClipboard', 'ClipboardAndViewer', 'ClipboardCopyPaste', 'pyperclipimg.copy(im)',
  "pyperclipimg 0.2.0 puts a Pillow image on the operating system's clipboard with copy() and returns the clipboard's image as an Image with paste(); on Linux it needs the program xclip, which is installed here, and with a display the round trip gave back a 40 by 30 RGB PNG with equal pixels.",
  (X(_PRE + r'''import pyperclipimg
out = (md.version('pyperclipimg'), callable(pyperclipimg.copy), callable(pyperclipimg.paste), shutil.which('xclip') is not None)'''), "('0.2.0', True, True, True)")),
 ('DrawingAndClipboard', 'ClipboardAndViewer', 'ClipboardFailures', 'pyperclipimg.paste()',
  'With no DISPLAY, pyperclipimg.copy() returns None without a message and paste() raises ChildProcessError from xclip; with text on the clipboard paste() raises UnidentifiedImageError, and importing the module with no xclip or wl-copy on the PATH raises NotImplementedError.',
  (X(_PRE + r'''code = "import pyperclipimg\nfrom PIL import Image\nprint(repr(pyperclipimg.copy(Image.new('RGB', (4, 4)))))\ntry: pyperclipimg.paste()\nexcept Exception as x: print(type(x).__name__)"
out = child(code, drop=('DISPLAY', 'WAYLAND_DISPLAY')).splitlines()'''), "['None', 'ChildProcessError']")),
 # ---------------- MatplotlibGraphs / FigureModel
 ('MatplotlibGraphs', 'FigureModel', 'PyplotState', 'plt.plot([1, 2, 3], [1, 2, 3])',
  'pyplot keeps one current figure and axes, and every plot call draws on them: two plot() calls give 2 lines, plt.show() with the Agg backend returns None and leaves the figure, and a following plt.scatter() adds 1 collection to the same axes, so state piles up from one example to the next.',
  (X(_PRE + r'''plt.close('all'); plt.plot([1, 2, 3], [1, 2, 3]); plt.plot([1, 2, 3], [3, 2, 1]); a = len(plt.gca().lines); r = plt.show(); b = plt.get_fignums(); plt.scatter([1, 2, 3], [1, 2, 3])
out = (a, r, b, len(plt.gca().lines), len(plt.gca().collections), plt.close('all'))'''), '(2, None, [1], 2, 1, None)')),
 ('MatplotlibGraphs', 'FigureModel', 'FigureDefaults', 'plt.figure().get_size_inches()',
  'A new figure is 6.4 by 4.8 inches at 100 dots per inch, which is 640 by 480 pixels, and its first line colour is #1f77b4 stored as a text in Matplotlib 3.10 and earlier and as an RGB tuple of floats from 3.11.0 on, so code that compared the colour with a text broke in 3.11.',
  (X(_PRE + r'''plt.close('all'); fig = plt.figure(); c0 = matplotlib.rcParams['axes.prop_cycle'].by_key()['color'][0]
out = ([float(v) for v in fig.get_size_inches()], fig.dpi, matplotlib.colors.to_hex(c0), type(c0).__name__, md.version('matplotlib'), plt.close('all'))'''), "([6.4, 4.8], 100.0, '#1f77b4', 'tuple', '3.11.2', None)")),
 ('MatplotlibGraphs', 'FigureModel', 'BackendChoice', 'matplotlib.get_backend()',
  "Matplotlib draws through a backend: a program with no DISPLAY gets agg, which makes images and no windows, and a program with a display gets tkagg, which opens windows; the reply of get_backend() is 'agg' with no display in this study and the Tk window is the one that blocks plt.show().",
  (X(_PRE + r'''out = (child('import matplotlib\nimport matplotlib.pyplot as plt\nprint(matplotlib.get_backend())', drop=('DISPLAY', 'MPLBACKEND')), matplotlib.is_interactive(), matplotlib.get_backend())'''), "('agg', False, 'Agg')")),
 # ---------------- MatplotlibGraphs / LineAndScatter
 ('MatplotlibGraphs', 'LineAndScatter', 'LinePlot', 'plt.plot(x_values, y_values1)',
  'plt.plot(x, y) draws a line and returns a list with one Line2D, so the shell prints a list with one <matplotlib.lines.Line2D> entry; the first two lines get the colours #1f77b4 and #ff7f0e, which Matplotlib 3.11 stores as tuples.',
  (X(_PRE + r'''plt.close('all'); r = plt.plot([0, 1, 2, 3, 4, 5], [10, 13, 15, 18, 16, 20]); r2 = plt.plot([0, 1, 2, 3, 4, 5], [9, 11, 18, 16, 17, 19])
out = (type(r).__name__, len(r), type(r[0]).__name__, [int(v) for v in r[0].get_ydata()], matplotlib.colors.to_hex(r[0].get_color()), matplotlib.colors.to_hex(r2[0].get_color()), plt.close('all'))'''), "('list', 1, 'Line2D', [10, 13, 15, 18, 16, 20], '#1f77b4', '#ff7f0e', None)")),
 ('MatplotlibGraphs', 'LineAndScatter', 'ScatterPlot', 'plt.scatter([0, 1, 2], [3, 1, 2])',
  'plt.scatter(x, y) draws points and returns a PathCollection, which is one entry of ax.collections and not of ax.lines: after one scatter() the axes hold 1 collection and 0 lines, and the offsets are an array of shape (3, 2).',
  (X(_PRE + r'''plt.close('all'); s = plt.scatter([0, 1, 2], [3, 1, 2])
out = (type(s).__name__, len(plt.gca().collections), len(plt.gca().lines), s.get_offsets().shape, plt.close('all'))'''), "('PathCollection', 1, 0, (3, 2), None)")),
 # ---------------- MatplotlibGraphs / BarAndPie
 ('MatplotlibGraphs', 'BarAndPie', 'BarChart', 'plt.bar(categories, values)',
  'plt.bar(categories, values) draws one rectangle for each category in the order given and returns a BarContainer; the heights 100, 200, 300 and 400 come back as numpy int64 and the tick labels are the four category names, so the chart is not sorted.',
  (X(_PRE + r'''plt.close('all'); b = plt.bar(['Cats', 'Dogs', 'Mice', 'Moose'], [100, 200, 300, 400])
out = (type(b).__name__, [int(h.get_height()) for h in b], {type(h.get_height()).__name__ for h in b}, [t.get_text() for t in plt.gca().get_xticklabels()], plt.close('all'))'''), "('BarContainer', [100, 200, 300, 400], {'int64'}, ['Cats', 'Dogs', 'Mice', 'Moose'], None)")),
 ('MatplotlibGraphs', 'BarAndPie', 'PieChart', "plt.pie(slices, labels=labels, autopct='%.1f%%')",
  "plt.pie() draws one wedge for each number and returns a PieContainer in Matplotlib 3.11.2 and a tuple in 3.10 and earlier; the container still unpacks into 3 parts with autopct and 2 without it, len() of it raises TypeError, the percent texts are '10.0%' to '40.0%' and the first wedge runs from 0 to 36 degrees.",
  (X(_PRE + r'''plt.close('all'); r = plt.pie([100, 200, 300, 400], labels=['Cats', 'Dogs', 'Mice', 'Moose'], autopct='%.1f%%'); n = len(tuple(plt.pie([1, 2, 3])))
out = (type(r).__name__, len(tuple(r)), n, [t.get_text() for t in r[2]], (r[0][0].theta1, float(r[0][0].theta2)), err(lambda: len(r))[0], plt.close('all'))'''), "('PieContainer', 3, 2, ['10.0%', '20.0%', '30.0%', '40.0%'], (0.0, 36.0), 'TypeError', None)")),
 # ---------------- MatplotlibGraphs / DecorationsAndOutput
 ('MatplotlibGraphs', 'DecorationsAndOutput', 'PlotDecorations', "plt.plot(x, y, marker='o', color='b', label='Line 1')",
  "The keywords marker, color and label decorate a line, plt.legend() returns a Legend, and plt.xlabel(), plt.ylabel() and plt.title() return Text objects whose text right after the call is Text(0.5, 0, 'X-axis Label'), Text(0, 0.5, 'Y-axis Label') and Text(0.5, 1.0, 'Graph Title').",
  (X(_PRE + r'''plt.close('all'); l1 = plt.plot([0, 1, 2], [1, 3, 2], marker='o', color='b', label='Line 1'); lg = plt.legend(); x = plt.xlabel('X-axis Label'); y = plt.ylabel('Y-axis Label'); t = plt.title('Graph Title')
out = (l1[0].get_marker(), l1[0].get_label(), type(lg).__name__, repr(x), repr(y), repr(t), plt.close('all'))'''), '(\'o\', \'Line 1\', \'Legend\', "Text(0.5, 0, \'X-axis Label\')", "Text(0, 0.5, \'Y-axis Label\')", "Text(0.5, 1.0, \'Graph Title\')", None)')),
 ('MatplotlibGraphs', 'DecorationsAndOutput', 'SaveFigure', "plt.savefig('linegraph.png')",
  'plt.savefig() writes the current figure: the default PNG is 640 by 480 pixels in mode RGBA with a density of 100 dots per inch, and dpi=200 gives 1280 by 960; the call belongs before plt.show(), as the chapter says, and takes the figure as it is at that moment.',
  (X(_PRE + r'''plt.close('all'); plt.plot([1, 2, 3]); b = io.BytesIO(); plt.savefig(b, format='png'); im = Image.open(io.BytesIO(b.getvalue())); c = io.BytesIO(); plt.savefig(c, format='png', dpi=200)
out = (im.size, im.mode, round(im.info['dpi'][0], 1), Image.open(io.BytesIO(c.getvalue())).size, plt.close('all'))'''), "((640, 480), 'RGBA', 100.0, (1280, 960), None)")),
 ('MatplotlibGraphs', 'DecorationsAndOutput', 'ShowLifecycle', 'plt.show()',
  'With the Agg backend plt.show() returns None at once and keeps the figure, so a savefig() after it still holds the line; with a Tk window plt.show() blocks until the window is closed and then the figure list is empty, a second plt.show() returns at once, and a savefig() after it writes a blank image.',
  (X(_PRE + r'''plt.close('all'); plt.plot([1, 2, 3]); a = io.BytesIO(); plt.savefig(a, format='png'); r = plt.show(); b = io.BytesIO(); plt.savefig(b, format='png')
ca = len(set(Image.open(io.BytesIO(a.getvalue())).convert('RGB').getdata())); cb = len(set(Image.open(io.BytesIO(b.getvalue())).convert('RGB').getdata()))
out = (r, plt.get_fignums(), ca == cb, matplotlib.get_backend(), plt.close('all'))'''), "(None, [1], True, 'Agg', None)")),
 # ---------------- BookAndPractice / InstallAndVersions
 ('BookAndPractice', 'InstallAndVersions', 'AppendixPins', 'matplotlib==3.92',
  'Appendix A pins pillow==10.4.0 and matplotlib==3.92, and no Matplotlib release 3.92 exists: pip reads 3.92 as 3.92.0, which is greater than 3.11.2, so the pin asks for a version that is not there, and the release the author meant is 3.9.2.',
  (X(_PRE + r'''from packaging.version import Version
out = (Version('3.92') == Version('3.92.0'), Version('3.92') > Version('3.11.2'), Version('3.9.2') < Version('3.11.2'), str(Version('3.9.2')))'''), "(True, True, True, '3.9.2')")),
 ('BookAndPractice', 'InstallAndVersions', 'PythonWheelSupport', 'uv pip install pillow==10.4.0',
  "A wheel is a prebuilt package for one Python version: the first Pillow release with a CPython 3.14 wheel is 11.3.0 and the first Matplotlib release is 3.10.5, so the book's pins Pillow 10.4.0 and Matplotlib 3.9.2 have wheels for Python 3.13 and not for 3.14, and pip must build them from source.",
  None),
 ('BookAndPractice', 'InstallAndVersions', 'PinnedBuildOnSource', 'Matplotlib 3.9.2 built on Python 3.14.6',
  "Matplotlib 3.9.2 built from source on Python 3.14.6 with the system FreeType and Qhull installs, but its savefig() and legend() raise RecursionError while copying a MarkerStyle, so the pinned release cannot draw a figure under 3.14.6 and the book's pins work only up to Python 3.13.",
  None),
 ('BookAndPractice', 'InstallAndVersions', 'TkVersionNine', 'tkinter.TkVersion',
  'Python 3.14.6 from uv has tkinter built against Tk 9.0, and the Matplotlib 3.9.2 TkAgg backend fails with ImportError (Failed to load Tcl_SetVar) against Tk 9.0 in both uv Pythons, 3.14.6 and 3.13.14, so the window of plt.show() opens with Matplotlib 3.11.2 and not with the pinned 3.9.2.',
  (X(_PRE + r'''import tkinter
out = (tkinter.TkVersion, tkinter.TclVersion, sys.version_info[:2] >= (3, 14))'''), '(9.0, 9.0, True)')),
 # ---------------- BookAndPractice / BookCorrections
 ('BookAndPractice', 'BookCorrections', 'GreenTableError', "ImageColor.getcolor('Green', 'RGBA')",
  "Table 21-1 gives Green as (0, 255, 0, 255), but checking all 8 rows of the table against ImageColor.getcolor() finds one that differs: 'Green' is (0, 128, 0, 255) and the table's value belongs to 'Lime', the HTML name of full green.",
  (X(_PRE + r'''T = [('White', (255, 255, 255, 255)), ('Red', (255, 0, 0, 255)), ('Green', (0, 255, 0, 255)), ('Blue', (0, 0, 255, 255)), ('Gray', (128, 128, 128, 255)), ('Yellow', (255, 255, 0, 255)), ('Black', (0, 0, 0, 255)), ('Purple', (128, 0, 128, 255))]
out = ([n for n, v in T if ImageColor.getcolor(n, 'RGBA') != v], len(T), ImageColor.getcolor('Green', 'RGBA'), ImageColor.getcolor('Lime', 'RGBA'))'''), "(['Green'], 8, (0, 128, 0, 255), (0, 255, 0, 255))")),
 ('BookAndPractice', 'BookCorrections', 'DpiClaim', "im.save('b.png', dpi=(72, 72))",
  "The chapter says Pillow's PNG files are 72 pixels per inch by default, but a PNG saved with no dpi has no pHYs chunk at all and no density to read back; with dpi=(72, 72) the chunk holds 2835 pixels per metre, which reads back as 72.009 dots per inch, so the 288 by 360 card needs the argument.",
  (X(_PRE + r'''d = wd(); im = Image.new('RGB', (8, 8)); im.save('a.png'); im.save('b.png', dpi=(72, 72))
def ppm(n):
    b = open(n, 'rb').read(); i = b.find(b'pHYs'); return struct.unpack('>IIB', b[i + 4:i + 13]) if i >= 0 else None
out = (b'pHYs' in open('a.png', 'rb').read(), Image.open('a.png').info.get('dpi'), ppm('b.png'), round(Image.open('b.png').info['dpi'][0], 3), round(72 / 0.0254), 288 / 72, 360 / 72)'''), '(False, None, (2835, 2835, 1), 72.009, 2835, 4.0, 5.0)')),
 ('BookAndPractice', 'BookCorrections', 'RotateFillClaim', 'z.rotate(6).getpixel((0, 0))',
  "The chapter says gaps are black on Windows and transparent on macOS and Linux, but zophie.png is mode RGB, which has no alpha, and the gap is (0, 0, 0) on this Linux machine; only an RGBA copy gives the invisible (0, 0, 0, 0), so the rule is the image's mode and not the system.",
  (X(_PRE + r'''shp(); z = Image.open('zophie.png')
out = (z.mode, z.rotate(6).getpixel((0, 0)), z.convert('RGBA').rotate(6).getpixel((0, 0)), sys.platform, z.rotate(6).getpixel((0, 0))[:3] == (0, 0, 0))'''), "('RGB', (0, 0, 0), (0, 0, 0, 0), 'linux', True)")),
 ('BookAndPractice', 'BookCorrections', 'AppendixBErrors', 'im.crop((0, 50, 50, 50))',
  'Appendix B answers question 6 with im.crop((0, 50, 50, 50)), which has the size (50, 0) because bottom equals top, while (0, 50, 50, 100) gives the 50 by 50 lower-left quarter; question 3 calls the box left, top, width and height although the chapter says right and bottom, and question 12 says plt.show() resets the data, true only for a window.',
  (X(_PRE + r'''im = Image.new('RGB', (100, 100))
out = (im.crop((0, 50, 50, 50)).size, im.crop((0, 50, 50, 100)).size, im.crop((0, 50, 50, 100)).size == (50, 50), 50 * 50)'''), '((50, 0), (50, 50), True, 2500)')),
 ('BookAndPractice', 'BookCorrections', 'MissingFiles', 'zipfile.ZipFile(...).namelist()',
  "The online materials hold zophie.png, catlogo.png, guests.txt and resizeAndAddLogo.py and none of zophie_xmas_tree.png, me_and_zophie.png, zophie_the_cat.jpg or any flower file, so the chapter's Project 16 output of three files and its public domain flower cannot be reproduced from the zip alone.",
  (X(_PRE + r'''z = zipfile.ZipFile(io.BytesIO(zipbytes())); base = {n.rsplit('/', 1)[-1] for n in z.namelist() if '__MACOSX' not in n}
want = ['zophie.png', 'catlogo.png', 'guests.txt', 'resizeAndAddLogo.py', 'zophie_xmas_tree.png', 'me_and_zophie.png', 'zophie_the_cat.jpg', 'flower.png']
out = ([n for n in want if n in base], [n for n in want if n not in base], len(z.namelist()), [n for n in base if 'flower' in n.lower()])'''), "(['zophie.png', 'catlogo.png', 'guests.txt', 'resizeAndAddLogo.py'], ['zophie_xmas_tree.png', 'me_and_zophie.png', 'zophie_the_cat.jpg', 'flower.png'], 184, [])")),
 # ---------------- BookAndPractice / DeprecatedApis
 ('BookAndPractice', 'DeprecatedApis', 'TextsizeGone', "hasattr(ImageDraw.ImageDraw, 'textsize')",
  "ImageDraw.textsize() and ImageFont.getsize() were removed in Pillow 10.0.0 and are False in 12.3.0, and textbbox(), textlength() and getbbox() take their place; the 2nd edition's chapter 19 mentions textsize 3 times, and this chapter avoids it.",
  (X(_PRE + r'''out = (hasattr(ImageDraw.ImageDraw, 'textsize'), hasattr(ImageFont.FreeTypeFont, 'getsize'), hasattr(ImageDraw.ImageDraw, 'textbbox'), hasattr(ImageDraw.ImageDraw, 'textlength'), hasattr(ImageFont.FreeTypeFont, 'getbbox'))'''), '(False, False, True, True, True)')),
 ('BookAndPractice', 'DeprecatedApis', 'GetdataDeprecation', 'Image.getdata()',
  "Image.getdata() gives a DeprecationWarning from Pillow 12.1.0 that says it will be removed in Pillow 14 (2027-10-15), with get_flattened_data() as the replacement, so the pixel-counting loops over getdata() in this study's programs are the first thing to change.",
  (X(_PRE + r'''with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); v = list(Image.new('RGB', (2, 1), 'red').getdata())
out = (v, [str(x.message)[:62] for x in w], hasattr(Image.Image, 'get_flattened_data'), md.version('pillow'))'''), "([(255, 0, 0), (255, 0, 0)], ['Image.Image.getdata is deprecated and will be removed in Pillo'], True, '12.3.0')")),
 # ---------------- BookAndPractice / PracticePrograms
 ('BookAndPractice', 'PracticePrograms', 'TileMaker', "make_tile('zophie_the_cat.jpg', 6, 10)",
  'The Tile Maker practice program makes a larger image from one tile: for a 20 by 50 pixel file make_tile(filename, 6, 10) returns a 120 by 500 image from 6 times 10, which is 60 pastes, as the book says.',
  (X(_PRE + r'''d = wd(); Image.new('RGB', (20, 50), 'tan').save('zophie_the_cat.jpg')
def make_tile(filename, across, down):
    tile = Image.open(filename); w, h = tile.size; out = Image.new('RGB', (w * across, h * down)); n = 0
    for x in range(across):
        for y in range(down): out.paste(tile, (x * w, y * h)); n += 1
    return out, n
t, n = make_tile('zophie_the_cat.jpg', 6, 10)
out = (t.size, n, t.getpixel((119, 499)), t.getpixel((0, 0)))'''), '((120, 500), 60, (209, 180, 140), (209, 180, 140))')),
 ('BookAndPractice', 'PracticePrograms', 'PhotoFolderFinder', "os.walk('.')",
  'The photo folder finder walks the folders with os.walk() and prints those where more than half of the files are .png or .jpg pictures wider and taller than 500 pixels; on a test tree it found ./a with 2 of 3 and ./b/c with 3 of 4 and not ./b with 0 of 2.',
  (X(_PRE + r'''d = wd()
def mk(p, s): os.makedirs(os.path.dirname(p), exist_ok=True); Image.new('RGB', s, 'gray').save(p)
mk('a/p1.png', (800, 600)); mk('a/p2.jpg', (900, 700)); open('a/n.txt', 'w').write('x'); mk('b/s.png', (300, 300)); mk('b/w.png', (2000, 400)); mk('b/c/q1.png', (600, 600)); mk('b/c/q2.jpg', (700, 800)); mk('b/c/q3.jpg', (650, 900)); open('b/c/r.txt', 'w').write('x')
def photo(p):
    if os.path.splitext(p)[1] not in ('.png', '.jpg'): return False
    with Image.open(p) as im: return im.width > 500 and im.height > 500
found = []
for folder, subs, files in os.walk('.'):
    if files and sum(photo(os.path.join(folder, f)) for f in files) > len(files) / 2: found.append(folder)
out = sorted(found)'''), "['./a', './b/c']")),
 ('BookAndPractice', 'PracticePrograms', 'SeatingCards', "Image.new('RGBA', (288, 360), 'white')",
  'The seating card program makes one 288 by 360 pixel card for each of the 5 names of guests.txt, which is 4 by 5 inches at 72 pixels per inch, draws a black rectangle at the edges, and the widest name, 176 pixels in 28 pixel DejaVu Sans, fits in the width.',
  (X(_PRE + r'''shp(); guests = open('guests.txt').read().splitlines(); f = ImageFont.truetype('DejaVuSans.ttf', 28); card = Image.new('RGBA', (288, 360), 'white'); d = ImageDraw.Draw(card); d.rectangle((0, 0, 287, 359), outline='black')
w = [d.textbbox((0, 0), g, font=f)[2] - d.textbbox((0, 0), g, font=f)[0] for g in guests]
out = (len(guests), card.size, (4 * 72, 5 * 72), max(w), max(w) <= 288, card.getpixel((0, 0)), guests[0])'''), "(5, (288, 360), (288, 360), 176, True, (0, 0, 0, 255), 'Prof. Plum')")),
]
CLAIMS = [
 (X(_PRE + r'''out = (md.version('pillow'), md.version('matplotlib'), md.version('pyperclipimg'), sys.version_info[:3] == (3, 14, 6))'''), "('12.3.0', '3.11.2', '0.2.0', True)"),
 (X(_PRE + r'''out = (288 / 72, 360 / 72, 4 * 72, 5 * 72, round(72 / 0.0254), 41 * 31, 6 * 5)'''), '(4.0, 5.0, 288, 360, 2835, 1271, 30)'),
 (X(_PRE + r'''out = (len(range(0, 816, 230)), len(range(0, 1088, 215)), len(range(0, 816, 230)) * len(range(0, 1088, 215)), 6 * 10, 20 * 6, 50 * 10)'''), '(4, 6, 24, 60, 120, 500)'),
 (X(_PRE + r'''import datetime as dt
out = ((dt.date(2027, 10, 15) - dt.date(2026, 10, 13)).days, dt.date(2027, 10, 15).strftime('%A'), dt.date(2026, 10, 13).strftime('%A'))'''), "(367, 'Friday', 'Tuesday')"),
 (X(_PRE + r'''out = (round(125433 / 1287443, 4), round(1287443 / 125433, 1), 816 * 1088, 816 * 1088 * 3)'''), '(0.0974, 10.3, 887808, 2663424)'),
 (X(_PRE + r'''from packaging.version import Version
out = (Version('3.9.2') < Version('3.10.8') < Version('3.11.0') < Version('3.92'), Version('10.4.0') < Version('11.3.0'), Version('3.10.5') > Version('3.9.2'))'''), '(True, True, True)'),
]
ERRORS = []
BEH = [
 ['crop with right less than left raises ValueError and with right equal to left gives width 0',
  "from PIL import Image\nim = Image.new('RGB', (60, 40))\ntry:\n    im.crop((40, 5, 10, 35))\nexcept ValueError as e:\n    print(type(e).__name__, e)\nprint(im.crop((10, 5, 10, 35)).size)",
  "ValueError Coordinate 'right' is less than 'left'\n(0, 30)"],
 ['paste changes the image it is called on and returns None, and copy keeps the original',
  "from PIL import Image\na = Image.new('RGB', (4, 4), 'red'); b = a.copy(); r = b.paste((0, 0, 255), (0, 0, 2, 2))\nprint(r, a.getpixel((0, 0)), b.getpixel((0, 0)), b.getpixel((3, 3)))",
  'None (255, 0, 0) (0, 0, 255) (255, 0, 0)'],
 ['putpixel refuses a colour name and getcolor turns it into a tuple',
  "from PIL import Image, ImageColor\nim = Image.new('RGB', (2, 2))\ntry:\n    im.putpixel((0, 0), 'red')\nexcept TypeError as e:\n    print(type(e).__name__)\nim.putpixel((0, 0), ImageColor.getcolor('red', 'RGB')); print(im.getpixel((0, 0)))",
  'TypeError\n(255, 0, 0)'],
 ['the corner of a rotation is black in RGB and invisible in RGBA',
  "from PIL import Image\nim = Image.new('RGB', (30, 20), 'white')\nprint(im.rotate(6).getpixel((0, 0)), im.convert('RGBA').rotate(6).getpixel((0, 0)))",
  '(0, 0, 0) (0, 0, 0, 0)'],
 ['an ImageDraw rectangle includes its last row and column',
  "from PIL import Image, ImageDraw\nim = Image.new('RGB', (30, 30)); ImageDraw.Draw(im).rectangle((2, 3, 6, 7), fill='red')\nprint(sum(1 for p in im.getdata() if p == (255, 0, 0)), 5 * 5)",
  '25 25'],
 ['a JPEG cannot hold an alpha channel',
  "from PIL import Image\nimport io\ntry:\n    Image.new('RGBA', (2, 2)).save(io.BytesIO(), 'JPEG')\nexcept OSError as e:\n    print(e)",
  'cannot write mode RGBA as JPEG'],
 ['with the Agg backend plt.show returns None at once and the figure stays',
  "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nplt.plot([1, 2, 3])\nprint(plt.show(), plt.get_fignums())",
  'None [1]'],
 ['the pie chart of Matplotlib 3.11 is a PieContainer that unpacks but has no length',
  "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nr = plt.pie([1, 2, 3], autopct='%.0f%%')\nw, t, a = r\nprint(type(r).__name__, len(w), len(a))\ntry:\n    len(r)\nexcept TypeError as e:\n    print('TypeError')",
  'PieContainer 3 3\nTypeError'],
 ['textsize and getsize no longer exist and textbbox measures text',
  "from PIL import Image, ImageDraw, ImageFont\nf = ImageFont.truetype('DejaVuSans.ttf', 32); d = ImageDraw.Draw(Image.new('RGB', (200, 200)))\nprint(hasattr(d, 'textsize'), hasattr(f, 'getsize'), d.textbbox((100, 150), 'Howdy', font=f))",
  'False False (100, 156, 209, 187)'],
 ['a negative pixel coordinate counts from the far edge and one past the edge raises IndexError',
  "from PIL import Image\nim = Image.new('RGB', (6, 4)); im.putpixel((5, 0), (9, 9, 9))\nprint(im.getpixel((-1, 0)))\ntry:\n    im.getpixel((6, 0))\nexcept IndexError as e:\n    print(e)",
  '(9, 9, 9)\nimage index out of range'],
]
BODY = {}
def _b(key, p1, p2):
    BODY[key] = p1 + "\n\n" + p2

# ---- ImageFundamentals ----
_b('ImageFundamentals',
 'The first part of the chapter, Computer Image Fundamentals, teaches the two ideas every Pillow call rests on: a colour is an RGBA value of four integers from 0 to 255, and a pixel is addressed by an x and y coordinate from the top-left origin, with box tuples naming rectangles [S]. It then loads zophie.png as an Image object with size, format and save [S].',
 "Three ideas carry this subject: colour representation covers the tuple, the names and the modes; the coordinate system covers the origin, the box tuple and its half-open edges; the image object covers opening, the filename, new images and saving. All of it was run with Pillow 12.3.0 on Python 3.14.6 and against the Pillow 10.4.0 the book pins, on the files of the publisher's zip, which the programs fetched and hash-checked [T].")
_b('ColorRepresentation',
 'The chapter explains an RGBA value as red, green, blue and alpha from 0 to 255, gives Table 21-1 of eight colour names, and says Pillow uses the same standard names as HTML and holds more than 100 of them in ImageColor.colormap [S]. The Pillow ImageColor page says the module converts CSS3-style colour specifiers and provides some 140 standard names, case insensitive, and the CSS Color module lists lime and green as separate colours [PILLOW][CSS].',
 'Three leaves cover it: the tuple, the names and the modes. Run against Pillow 12.3.0, the dictionary held 148 names, one value of Table 21-1 was wrong, and the two files of the chapter turned out to have different modes, RGB and LA, which matters as soon as a picture is saved or pasted [T].')
_b('RgbaTuple',
 'The chapter says Pillow writes red as (255, 0, 0, 255), that alpha 0 means invisible and that the other three numbers then do not matter [S]. The Pillow concepts page says an image has one or more bands, a PNG for example R, G, B and A, and that the mode is a string that defines the type and depth of a pixel [PILLOW].',
 'Pillow 12.3.0 returned (255, 0, 0, 255) for red in RGBA and (255, 0, 0) in RGB; a new RGBA image started as (0, 0, 0, 0), and a pixel set to (10, 20, 30, 0) kept the numbers 10, 20 and 30 although it cannot be seen [T]. A program that tests for transparency must test the fourth number, not the colour.')
_b('ColorNames',
 "The chapter calls getcolor() with 'red', 'RED', 'chocolate' and 'CornflowerBlue' and lists the dictionary from 'aliceblue' to 'yellowgreen' [S]. The Pillow page says its names come from the X Window system and most web browsers, and the CSS Color module lists lime as the colour with full green [PILLOW][CSS].",
 "ImageColor.colormap held 148 names, the first aliceblue and the last yellowgreen; 'RED' gave the same tuple as 'red', 'CornflowerBlue' gave (100, 149, 237, 255), and 'transparent' raised ValueError because it is not a name of the dictionary. 'green' was (0, 128, 0, 255) and 'lime' (0, 255, 0, 255), which is where the chapter's table goes wrong [T].")
_b('ImageModes',
 "The chapter creates every image in mode 'RGBA' and says there are other modes the book does not go into [S]. The Pillow concepts page describes the mode as the string that defines the type and depth of a pixel [PILLOW].",
 "zophie.png of the online materials was mode RGB, 816 by 1088 pixels, and catlogo.png was mode LA, 100 by 95 pixels, whose first pixel is (255, 0): white with alpha 0. Saving the LA logo converted to RGBA as a JPEG raised OSError with the text cannot write mode RGBA as JPEG, and saving the LA image itself raised OSError too [T]. Neither file of the chapter is RGBA, so the chapter's mode 'RGBA' describes only the images it creates.")
_b('CoordinateSystem',
 "The chapter teaches the pixel origin at the top-left corner with y growing downward, which it calls the opposite of school mathematics, and the box tuple of left, top, right and bottom with Figure 21-1 and Figure 21-2 [S]. Pillow's tutorial uses the same box for crop() and paste() [PILLOW].",
 'Three leaves cover it: where the origin is and what a pixel read outside the image does, what a box tuple holds, and why its right and bottom edges are left out. The sizes and the errors of this subject were produced by calling the methods, not by reading the text [T].')
_b('PixelOrigin',
 'The chapter says (0, 0) is the top-left pixel, that x grows to the right, that y grows downward and that this bears repeating because it differs from mathematics [S]. The Pillow reference gives getpixel() the coordinate as (x, y) [PILLOW].',
 'On a 60 by 40 gradient the pixel (59, 0) was (236, 0, 177); getpixel((-1, 0)) returned the same colour, because a negative x counts from the right edge, while getpixel((60, 0)) and getpixel((0, 40)) raised IndexError with the text image index out of range [T]. The chapter does not mention that negative coordinates are accepted, which can hide an off-by-one error.')
_b('BoxTuple',
 'The chapter defines the box as left, top, right and bottom, says right and bottom are one pixel beyond the edge, and shows (3, 1, 9, 6) in Figure 21-2 [S]. Appendix B answer 3 says the four integers are left, top, width and height, which contradicts it [S].',
 "The box (3, 1, 9, 6) cropped from a 28 by 27 image gave the size (6, 5), a width of 9 minus 3 and a height of 6 minus 1, which is 30 pixels, so the chapter's definition is right and the answer of Appendix B is wrong [T]. A program that passes width and height as the third and fourth numbers crops a different region without any error.")
_b('HalfOpenBox',
 'The chapter notes that a box includes the left column and top row but not the right column and bottom row [S]. The Pillow reference calls the crop box a 4-tuple of the left, upper, right and lower pixel coordinate [PILLOW].',
 "crop((10, 5, 40, 35)) of the 60 by 40 gradient gave 30 by 30; crop((50, 30, 70, 50)) gave 20 by 20 whose last pixel was black (0, 0, 0); a box with right 10 less than left 40 raised ValueError with the text Coordinate 'right' is less than 'left', and a box with right equal to left gave the size (0, 30) without an error [T]. So a wrong box fails loudly only in one of the two ways.")
_b('ImageObject',
 'The chapter loads zophie.png with Image.open(), reads size, filename, format and format_description, saves a JPEG, and makes blank images with Image.new() [S]. The Pillow tutorial describes the same attributes [PILLOW].',
 'Four leaves cover it: opening and size, the filename attribute, new images and saving by extension. Two of the printed values depend on the Pillow release, the filename and the default fill, and the pinned Pillow 10.4.0 prints a path where the book prints a name [T].')
_b('OpenAndSize',
 "The chapter prints cat_im.size as (816, 1088), format as 'PNG' and format_description as 'Portable network graphics', and unpacks size into width and height [S]. The Pillow reference says the image data is not read from the file until you try to process it or call load() [PILLOW].",
 "Pillow 12.3.0 gave the size (816, 1088), the format 'PNG', the description 'Portable network graphics' and the mode 'RGB', and the attributes width and height gave 816 and 1088; every line of that listing matched what the book prints in the replay [T]. The mode RGB is a fact the chapter does not print.")
_b('ImageFilename',
 "The chapter prints cat_im.filename as 'zophie.png' and describes it as the original file's name [S]. The Pillow reference describes Image.open() as taking a filename string, a path object or a file object [PILLOW].",
 "Pillow 12.3.0 printed 'zophie.png', but across 14 releases run on Python 3.11 the attribute was absolute in 10.3.0, 10.4.0 and 11.0.0 and relative in 9.5.0, 10.0.0, 10.1.0, 10.2.0, 11.1.0, 11.2.1, 11.3.0, 12.0.0, 12.1.0, 12.2.0 and 12.3.0 [T]. The Pillow 10.4.0 that Appendix A pins therefore printed an absolute path in the replay, one of the lines of the chapter's printed listings that differed there [S][T].")
_b('NewImage',
 'The chapter makes a 100 by 200 purple image, calls Image.new() again with no colour for a 20 by 20 image and says the default is the invisible black (0, 0, 0, 0) [S]. The Pillow reference says the colour default of Image.new() is black and that colour strings are accepted for RGB images [PILLOW].',
 "The purple image had the pixel (128, 0, 128, 255), the colourless RGBA image (0, 0, 0, 0) and a colourless RGB image (0, 0, 0), which is opaque black; the colour from ImageColor.getcolor('purple', 'RGBA') gave the same pixel as the name [T]. The chapter's remark about invisible black holds for RGBA only.")
_b('SaveFormats',
 'The chapter saves zophie.png as zophie.jpg and says Pillow sees the extension .jpg and uses the JPEG format, and that the two files are not identical [S]. The Pillow reference says save() takes the format from the file name extension when none is given, the format page gives the JPEG option quality a default of 75, and the PNG specification defines the pHYs chunk for pixel density [PILLOW][PNG3].',
 "The JPEG was 125,433 bytes against the 1,287,443 bytes of the PNG, and the largest difference in a channel after reading it back was 37, so the chapter's not identical means lossy; saving as .unknownext raised ValueError with the text unknown file extension [T]. The chapter does not say that the JPEG quality, 75 by default, trades size for loss.")
# ---- ImageEditing ----
_b('ImageEditing',
 'The second part of the chapter, Manipulating Images with Pillow, edits an opened picture with a handful of methods: crop(), copy(), paste(), resize(), rotate() and transpose(), and getpixel() and putpixel() for single pixels [S]. The summary lists the same six methods and save() [S].',
 'Three ideas carry this subject: cropping and pasting cover the box, the in-place paste, the mask and the tile loop; resizing and rotating cover the integer size, the filter and the fill and expanded size; flipping and pixel access cover transpose and the two pixel calls. Every size and colour below was measured on the shipped zophie.png and on a 60 by 40 gradient made by the program [T].')
_b('CropAndPaste',
 'The chapter crops the face out of zophie.png, copies the picture, pastes the face twice, and tiles it with two nested loops, noting that crop() returns a new image and paste() changes its own [S]. The Pillow reference describes both calls [PILLOW].',
 'Four leaves cover it: the crop box, the in-place paste of a copy, the transparency mask and the tile loop. In Pillow 12.3.0 the crop gave 230 by 215, paste returned None, a missing mask copied a transparent pixel as (255, 255, 255, 0) and the loop made 24 pastes [T].')
_b('CropBox',
 'The chapter says crop() takes a box tuple, returns a new Image and leaves the original untouched, and crops the face with (335, 345, 565, 560) [S]. Appendix B answer 6 gives im.crop((0, 50, 50, 50)) for a quarter of a picture [S].',
 'The face was 230 by 215 pixels in mode RGB, the original stayed 816 by 1088, and the returned object was a different one [T]. The box of Appendix B answer 6 has the same top and bottom, so its height is 0; the quarter it names needs (0, 50, 50, 100).')
_b('PasteInPlace',
 'The chapter says copy() returns a new Image so the original can be kept, that paste() modifies its Image in place and does not return one, and that copy() and paste() do not use the clipboard [S]. The Pillow reference gives the paste box as a 2-tuple for the upper left corner and says a pasted image of another mode is converted to the mode of the target [PILLOW].',
 "paste() returned None; after pasting the 230 by 215 face at (0, 0) into a copy the copy's corner pixel equalled the face's and differed from the original's, which was untouched, and the copy was a different object from the original [T]. A program that writes im = im.paste(...) loses its image, because the name then holds None.")
_b('PasteMask',
 'The chapter says an image with transparency must be passed as the optional third argument, otherwise its transparent pixels appear as white pixels, and it shows both results in Figure 21-13 [S]. The Pillow reference says a mask of mode 1, L, LA, RGBA or RGBa updates only the regions it indicates, that the alpha band is used as the mask if present, and that where the mask is 0 the current value is kept [PILLOW].',
 "On a red RGBA background the corner of catlogo.png pasted with itself as the mask stayed (200, 0, 0, 255), and pasted without a mask became (255, 255, 255, 0); a pixel in the middle of the cat was the same in both [T]. The white of the book's figure exists because the stored colour under alpha 0 in this logo is 255, the L value of its first pixel (255, 0), so a logo saved with a black fill would give black.")
_b('TileLoop',
 'The chapter tiles the 230 by 215 face over the 816 by 1088 picture with a loop over left in range(0, width, face width) and an inner loop over top, and prints the positions from (0, 0) to (690, 1075) [S]. Nothing in the chapter says what happens at the right and bottom edge, where the last tiles do not fit.',
 'The loop made 4 columns and 6 rows, 24 pastes, the first three at (0, 0), (0, 215) and (0, 430) and the last two at (690, 860) and (690, 1075), the same positions the chapter prints; the last column and the last row run past the edge and are cut off without an error [T]. Counting the pastes first, 4 times 6, is the check the practice program asks for with 6 times 10.')
_b('ResizeAndRotate',
 'The chapter resizes the cat to half its width and height and to a taller shape, and rotates it by 90, 180, 270 and 6 degrees, with and without expand [S]. The Pillow reference documents resize() with a resample argument and rotate() with expand and fillcolor [PILLOW].',
 'Four leaves cover it: the integer size, the filter nobody names, the fill of the corners and the expanded size. Pillow 12.3.0 refused a float size, used bicubic by default, filled an RGB corner with black and made 6 degrees of rotation 926 by 1168 [T].')
_b('ResizeInteger',
 'The chapter says resize() accepts only integers in its tuple, which is why both divisions are wrapped in int(), and that it returns a new Image [S]. The Pillow reference gives size as the requested size in pixels, (width, height) [PILLOW].',
 "int(width / 2) and int(height / 2) gave 408 by 544 from 816 by 1088; the taller shape gave 816 by 1388; and a size of w / 2, h / 2, the floats 408.0 and 544.0, raised TypeError with the text 'float' object cannot be interpreted as an integer, while the original stayed 816 by 1088 [T]. Integer division with // would do the same without the int() call.")
_b('ResizeFilter',
 'The chapter does not name a resampling filter and calls resize() with a size only [S]. The Pillow reference says the default filter is Resampling.BICUBIC, except for modes 1 and P, which always use NEAREST, and lists NEAREST, BOX, BILINEAR, HAMMING, BICUBIC and LANCZOS [PILLOW].',
 'On the 60 by 40 gradient resized to 30 by 20 the bytes of the default call equalled those of Image.Resampling.BICUBIC and differed from NEAREST and from LANCZOS [T]. The choice of a filter changes the pixels of every scaled picture of Project 16, and the chapter leaves it at the default.')
_b('RotateFill',
 'The chapter says rotated images keep their size, that on Windows a black background fills the gaps and that on macOS and Linux transparent pixels fill them instead [S]. The Pillow reference describes fillcolor of rotate() as an optional colour for the area outside the rotated image and names no operating system [PILLOW].',
 "On the RGB gradient the corner after rotate(6) was (0, 0, 0), on an RGBA copy it was (0, 0, 0, 0) and with fillcolor='red' it was (255, 0, 0); the size stayed 60 by 40 in both rotations [T]. The result follows the image's mode, not the operating system,.")
_b('RotateExpand',
 'The chapter says expand=True enlarges the image to fit the whole rotated picture and that with 90, 180 or 270 degrees the result has no black or transparent background [S]. The Pillow reference describes expand as making the output image large enough to hold the entire rotated image [PILLOW].',
 'Without expand rotate(90), rotate(180) and rotate(6) all gave 816 by 1088; with expand=True rotate(90) gave 1088 by 816, rotate(180) gave 816 by 1088 and rotate(6) gave 926 by 1168 [T]. The tiling loop of the same picture would need 926 by 1168 to be recomputed, which is why a program should read the size again after an expanded rotation.')
_b('FlipAndPixels',
 'The chapter mirrors the picture with transpose() and the constants Image.FLIP_LEFT_RIGHT and Image.FLIP_TOP_BOTTOM, and reads and sets single pixels with getpixel() and putpixel(), colouring half a 100 by 100 image grey [S]. The Pillow release notes of 9.1.0 moved the constants to Image.Transpose and those of 9.4.0 restored the old names [PILLOW].',
 "Two leaves cover it: flipping and the pixel calls. In Pillow 12.3.0 the old constant was the integer 0, equal to Image.Transpose.FLIP_LEFT_RIGHT, so the chapter's code runs, and putpixel() with an RGB tuple on an RGBA image stored alpha 255 [T].")
_b('TransposeFlip',
 'The chapter flips horizontally with Image.FLIP_LEFT_RIGHT and vertically with Image.FLIP_TOP_BOTTOM and says transpose() returns a new Image [S]. Pillow 9.1.0 deprecated the module constants in favour of Image.Transpose and 9.4.0 reversed that, so both spellings work [PILLOW].',
 "On the gradient the pixel at x 0 after the flip equalled the original pixel at x 59 and the top row equalled the bottom row; Image.FLIP_LEFT_RIGHT was an int equal to the member of Image.Transpose, whose values were 0 for left-right and 1 for top-bottom; ROTATE_90 turned 60 by 40 into 40 by 60 [T]. The chapter's two calls ran unchanged in every environment of the replay that had Pillow.")
_b('PixelAccess',
 "The chapter says getpixel() and putpixel() take an x and y tuple, that putpixel() accepts an RGBA or an RGB tuple, and that a colour name such as 'darkgray' has to go through ImageColor.getcolor() [S]. The Pillow reference says of putpixel() that it is relatively slow and points to paste() or the ImageDraw module for larger changes [PILLOW].",
 "putpixel((0, 0), (210, 210, 210)) on an RGBA image stored (210, 210, 210, 255) and the pixel from 'darkgray' was (169, 169, 169, 255), the two values the chapter prints; putpixel() with the name 'red' raised TypeError with the text color must be int or tuple, and the call returned None [T]. Loops over 100 by 50 pixels are fine here and slow for large pictures.")
# ---- LogoProject ----
_b('LogoProject',
 "Project 16, Add a Logo, is the chapter's one complete program: it resizes every .png and .jpg file of the working directory to fit a 300 by 300 square, pastes catlogo.png into the bottom-right corner and saves the result in a folder named withLogo, in four steps that open the logo, loop over the files, resize and paste [S].",
 "Three ideas carry this subject: setup covers the constants and the file loop; the resize logic covers the both-sides test and the proportion; placement covers the corner, the mask, the output folder and the shipped file. The program was run as the page prints it, which fails, and as the publisher's file ships it, which runs, and its edge cases were measured with pictures made by the program [T].")
_b('LogoSetup',
 "Step 1 and Step 2 put two constants at the top, open the logo once and loop over os.listdir('.') with an if statement that skips names without .png or .jpg and the logo itself, using continue [S]. The Python documentation says os.listdir() returns the names in arbitrary order [PY].",
 'Two leaves cover it: the constants and the file loop. The shipped file has 25 lines of code, names 300 and catlogo.png once each, and keeps the case-sensitive extension test that skips C.PNG and e.JPG [T].')
_b('LogoConstants',
 "The chapter says setting SQUARE_FIT_SIZE and LOGO_FILENAME at the start makes the program easy to change, and that without them a reader would have to search the code for every 300 and 'catlogo.png' [S]. It adds that command line arguments could set them [S].",
 "The shipped resizeAndAddLogo.py contained SQUARE_FIT_SIZE = 300 and LOGO_FILENAME = 'catlogo.png', had 25 lines that are not blank or comments, and the logo it opens is 100 by 95 pixels [T]. The constant 300 appears again in the program's arithmetic only through the name, so one edit really does change the limit.")
_b('LogoFileLoop',
 "The chapter loops over os.listdir('.'), skips names that do not end with .png or .jpg and the logo's name, and says the loop uses continue to go to the next file [S]. The Python os documentation says listdir returns the names in arbitrary order [PY].",
 'Applied to seven names, the test kept a.png and b.jpg and skipped C.PNG, d.jpeg, catlogo.png, n.txt and e.JPG [T]. The chapter says the program handles all .png and .jpg files, but a photograph named IMG_0001.JPG, which cameras write, is skipped without a message; str.lower() before the test would keep it.')
_b('LogoResizeLogic',
 'Step 3 resizes only if the width and the height are both larger than 300, and then scales the longer side to 300 and the other side by the same proportion, converting the float result with int() because resize() needs integers [S].',
 'Two leaves cover it: the test on both sides and the proportion. Pictures made for the study showed that the test leaves some large pictures at their size and that the arithmetic gives the 225 by 300 the chapter prints for zophie.png [T].')
_b('BothSidesTest',
 "The chapter's list of what the program does says to check whether the image is wider and taller than 300 pixels, and the code tests width > SQUARE_FIT_SIZE and height > SQUARE_FIT_SIZE with and [S]. The chapter's own summary calls the aim fitting every picture into 300 by 300 [S].",
 'Run through the shipped file, a 1200 by 400 panorama became 300 by 100 and a 500 by 700 picture became 214 by 300, but a 1200 by 250 strip stayed 1200 by 250 and a 250 by 900 column stayed 250 by 900 [T]. The test needs or to fit every picture into the square; with and the logo is also pasted at the unchanged size.')
_b('ProportionMath',
 'The chapter multiplies the ratio SQUARE_FIT_SIZE / width by the height for a wide picture and the ratio SQUARE_FIT_SIZE / height by the width otherwise, and says int() must convert the float [S].',
 'For zophie.png 300 / 1088 * 816 was the float 225.00000000000003 and int() gave 225, the 225 by 300 of the chapter; for 500 by 700 the value 214.28 gave 214 with int() and with round(), and 300 / 500 * 700 was exactly 420.0 [T]. A product that lands just below a whole number would lose a pixel, which is why round() is the safer call.')
_b('LogoPlacement',
 'Step 4 pastes the logo at the image width minus the logo width and the image height minus the logo height, passes the logo as the third argument, prints a message, and saves under the original filename in withLogo [S]. Figure 21-12 draws the arithmetic and Figure 21-13 shows the result with and without the mask [S].',
 "Four leaves cover it: the corner position, the masked paste, the output folder and the shipped file. The arithmetic gave (125, 205) for the 225 by 300 picture, the mask kept the picture's own pixel under the logo's transparent corner, two runs both exited with 0, and the page's listing, unlike the file, fails with SyntaxError [T].")
_b('CornerPosition',
 'The chapter says the left coordinate is the image width minus the logo width and the top coordinate is the image height minus the logo height, as Figure 21-12 shows [S]. The Pillow reference takes the 2-tuple of paste() as the upper left corner of the pasted image [PILLOW].',
 'With the 100 by 95 logo the 225 by 300 picture gave (125, 205) and the 300 by 100 panorama gave (200, 5) [T]. For a 50 by 50 picture smaller than the logo the position (-50, -45) is accepted and paste() raised no error, and the logo is cut off at the top and left, which the chapter does not mention.')
_b('MaskedPaste',
 'The chapter says paste() does not paste the transparency pixels unless logo_im is passed as the third argument, and Figure 21-13 shows the transparent pixels as solid white without it [S]. The Pillow reference says the alpha band of the mask decides what is copied, 255 as it is and 0 left alone [PILLOW].',
 "After the masked paste the pixel at the logo's corner equalled the picture's own pixel there, and a pixel in the middle of the cat was (0, 0, 0); without the mask the corner became (255, 255, 255), and the picture stayed RGB [T]. The white of the figure comes from the logo's stored grey value 255 under alpha 0.")
_b('OutputFolder',
 'The chapter says os.makedirs() creates withLogo instead of overwriting the originals and that exist_ok=True keeps it from raising if the folder exists, and the program saves each file under its old name [S]. The Python documentation says that with exist_ok False, the default, FileExistsError is raised if the target directory exists [PY].',
 "Two runs in a row in the same folder both exited with 0 and wrote only zophie.png into withLogo, and the original zophie.png had the same bytes afterwards; the first run printed Adding logo to zophie.png... and Resizing zophie.png... [T]. A plain file called withLogo made os.makedirs('withLogo', exist_ok=True) raise FileExistsError.")
_b('ShippedScript',
 "The chapter prints the program in four listings and says the file can be had from the online materials; its fourth listing writes (width – logo_width, height – logo_height) with an en dash [S]. The file in the publisher's zip is the same program with an ASCII minus and a header comment [S].",
 "Joined as printed, the four listings stopped with SyntaxError: invalid character U+2013 at line 38; with the dash written as a minus, and as the shipped file, the program exited with 0 and made a 225 by 300 picture, and the shipped file's SHA-256 started 4291c7cedd9d [T]. Every line of the shipped file was found among the listings once the callout numbers were removed.")
# ---- DrawingAndClipboard ----
_b('DrawingAndClipboard',
 'The third part of the chapter draws on images with the ImageDraw module, which has methods for points, lines, rectangles, ellipses and polygons and for text, and then copies and pastes images with pyperclipimg, an operating-system clipboard tool [S]. Its drawing example makes the 200 by 200 picture of Figure 21-14 [S].',
 'Three ideas carry this subject: the shape methods cover the draw object, points, lines, rectangles, polygons and the drawing example; text covers the fonts and their size; the clipboard and viewer cover show() and pyperclipimg. The drawings were checked by counting pixels and by looking at the saved PNGs; the window and clipboard programs ran on a virtual X display (Xvfb) with the real xclip and viewer [T].')
_b('ImageDrawShapes',
 'The chapter lists point(), line(), rectangle(), ellipse() and polygon() with their fill, outline and width arguments, says the optional fill and outline default to white, and draws a 200 by 200 example [S]. The Pillow ImageDraw page documents the same methods and the width argument [PILLOW].',
 'Five leaves cover it: the draw object, points and lines, rectangles and ellipses, polygons and the drawing example. The numbers were counted from the pixels: 1271 pixels for the rectangle (20, 30, 60, 60), 66 for a small triangle and 654 for the green lines of the example [T].')
_b('DrawObject',
 'The chapter passes the Image object to ImageDraw.Draw() and stores the ImageDraw object in draw so the following examples can use it [S]. The Pillow ImageDraw page says the module provides simple 2D graphics for Image objects [PILLOW].',
 'Draw() returned an ImageDraw object, its line() returned None, and the pixel (5, 0) of the image itself became (255, 0, 0), so the drawing happens on the image that was passed in and not on a copy [T]. A program that needs the original untouched must call copy() before Draw().')
_b('PointsAndLines',
 'The chapter says point() draws individual pixels from a list of tuples or of bare coordinates and notes that point here means a pixel, not the unit of font size; line() draws one or more lines and takes a width that defaults to 1 [S]. The Pillow page documents both [PILLOW].',
 'Two points given as [(1, 1), (3, 3)] and as [1, 1, 3, 3] made identical images with 2 red pixels; a horizontal line from (0, 5) to (9, 5) painted 10 pixels and with width=3 it painted 30 [T]. The end points of a line are painted, as they are for the rectangle.')
_b('RectangleEllipse',
 'The chapter says the box of rectangle() and ellipse() is a left, top, right, bottom tuple, that equal width and height make a circle, and that fill and outline default to white [S]. Unlike crop(), where it says the right column is not included, it gives no rule for ImageDraw [S].',
 'The rectangle (20, 30, 60, 60) painted 1271 pixels, 41 columns by 31 rows, so the right and bottom edges are included; the corners reversed raised ValueError with the text x1 must be greater than or equal to x0; and a rectangle with neither fill nor outline drew a white outline, (255, 255, 255) at (5, 5) on a blue image [T]. Two boxes in the same chapter therefore count the edge differently.')
_b('PolygonDrawing',
 'The chapter says polygon() takes tuples or integers for the connecting points, that the last pair of coordinates is joined to the first, and that fill and outline are optional [S]. The Pillow page documents polygon() with the same arguments [PILLOW].',
 'The triangle (0, 0), (10, 0), (0, 10) filled 66 pixels of an 11 by 11 image, including the closing edge, (0, 5) and the inner pixel (5, 5) were red, and the far corner (10, 10) stayed black [T]. The closing edge is drawn although no point was listed twice.')
_b('DrawingExample',
 'The chapter draws a black border, a blue rectangle, a red ellipse, a brown five-point polygon and, in a loop from 100 to 190 in steps of 10, green lines from (i, 0) to (200, i - 100), and shows the result as Figure 21-14 [S]. The picture is 200 by 200 [S].',
 'The pixel (100, 0), which the border had painted black, was (0, 128, 0, 255) after the loop because the lines start at y 0; the pixel (50, 45) inside the rectangle was (0, 0, 255, 255), the corners (0, 0) and (0, 199) stayed black, 654 pixels were green and 1271 were blue [T]. The saved PNG, looked at as an image, shows the green curve in the top right corner, as Figure 21-14 does.')
_b('TextDrawing',
 "The chapter draws text with draw.text(), takes a font from ImageFont.truetype() with the file name and a size it calls points, and says Pillow's PNGs are 72 pixels per inch so a point is one pixel [S]. The Pillow ImageFont page says the size is in pixels [PILLOW].",
 "Three leaves cover it: the default font, the TrueType font and the measuring of text. Under Pillow 12.3.0 the default font is a sized FreeType font, 'arial.ttf' does not exist on this Linux machine, and the word Howdy of the chapter's example does not fit [T].")
_b('DefaultFont',
 'The chapter writes Hello with no font argument and says the typeface and size are not customised [S]. The Pillow release notes of 10.1.0 say a version of Aileron Regular that can be drawn at chosen sizes is now loaded, and the reference says load_default() takes a size [PILLOW].',
 'load_default() returned a FreeTypeFont of size 10 named Aileron Regular, and load_default(size=20) one of size 20; across the 14 Pillow releases run the class was ImageFont in 9.5.0 and 10.0.0 and FreeTypeFont from 10.1.0, and size= raised TypeError before 10.1.0 [T]. Hello drawn with no font argument therefore differs between Pillow 10.0.0 and 10.1.0, and the pinned 10.4.0 draws the sized FreeType font.')
_b('TrueTypeFont',
 "The chapter calls ImageFont.truetype('arial.ttf', 32) and says Pillow searches C:\\Windows\\Fonts, /Library/Fonts, /System/Library/Fonts and /usr/share/fonts/truetype and raises an error for a font it cannot find [S]. The Pillow page lists Windows, macOS and Linux folders, among them /usr/share/fonts, and says the size is the requested size in pixels [PILLOW].",
 "On this Linux machine 'arial.ttf' raised OSError with the text cannot open resource, so the chapter's listing 24 did not run, while 'DejaVuSans.ttf' loaded by name as a FreeTypeFont named DejaVu Sans of size 32 [T]. The book's points equal the documentation's pixels only if one point is one pixel, the chapter's 72 pixels per inch; a default PNG carries no density, so the size is a height in pixels.")
_b('TextMeasuring',
 'The chapter does not measure text; it draws Howdy at (100, 150) on a 200 pixel image and shows Figure 21-15 [S]. The Pillow ImageDraw page documents textbbox() and textlength(), and the release notes of 10.0.0 say textsize() and getsize() were removed in favour of them [PILLOW].',
 "textbbox((100, 150), 'Howdy', font=f) returned (100, 156, 209, 187), so the word is 109 pixels wide and 31 high and its right edge 209 lies beyond the 200 pixel image; textlength gave 109.06, and neither draw.textsize nor font.getsize existed [T]. The 2nd edition's chapter 19 mentions textsize 3 times [S2E].")
_b('ClipboardAndViewer',
 "The chapter's show() opens the picture in a window for debugging, and the section on the clipboard says pyperclipimg.copy() puts a Pillow Image on the operating system's clipboard and paste() returns the clipboard's image [S]. The pyperclipimg README names xclip or wl-copy as the programs it needs on Linux [PPI].",
 'Three leaves cover it: the viewer that show() starts, the round trip through the clipboard and the ways the clipboard fails. The programs ran on a virtual X display with xclip and the display program of ImageMagick, and a screenshot of that screen found the picture [T].')
_b('ShowViewer',
 'The chapter says show() opens the image in a window and is useful when debugging [S]. The Pillow ImageShow page lists XDGViewer, which runs the freedesktop.org xdg-open command, and DisplayViewer, the ImageMagick display command, among the Unix viewers registered if their command is found, and says the temporary files created from images are not removed [PILLOW].',
 'On the virtual display Image.show() returned None and started xdg-open and the display program, and a screenshot of the screen matched 5 of 6 probe pixels of zophie.png at one position; Pillow listed XDGViewer and DisplayViewer first, and with no viewer on the PATH the headless replay showed nothing and raised no error [T]. A program therefore cannot learn from show() whether anything was shown.')
_b('ClipboardCopyPaste',
 'The chapter copies zophie.png with pyperclipimg.copy(im), pastes it with pyperclipimg.paste() and shows it, and says the module lets users put image data into and out of Python programs [S]. The README of pyperclipimg says it needs xclip or wl-copy on Linux and PyPI lists version 0.2.0 [PPI][PYPI].',
 'With xclip on a display, copy() returned None and paste() returned a PngImageFile in format PNG and mode RGB, 40 by 30 pixels, with every pixel equal to the original; the clipboard offered the image as image/png [T]. The same round trip does not work on a server with no display.')
_b('ClipboardFailures',
 'The chapter shows only the working case and tells the reader to copy a new image from a graphics program before paste() [S]. The README says the module needs xclip or wl-copy on Linux [PPI].',
 "With no DISPLAY copy() returned None and no message, and paste() raised ChildProcessError with xclip's text Can't open display; with text on the clipboard paste() raised UnidentifiedImageError; and importing the module with no xclip or wl-copy on the PATH raised NotImplementedError that tells the reader to install one of them [T]. In the headless replay the chapter's lines of listing 25 therefore did not match.")
# ---- MatplotlibGraphs ----
_b('MatplotlibGraphs',
 'The last part of the chapter makes graphs with Matplotlib: a line graph and a scatter plot of the same two series, a bar graph and a pie chart, and then markers, colours, labels and a legend, saving with plt.savefig() and previewing with plt.show() [S]. The Matplotlib interface guide calls pyplot an implicit interface that keeps track of the last Figure and Axes created [MPL].',
 "Four ideas carry this subject: the figure model covers the current figure, its defaults and the backend; line and scatter cover the two plot calls; bar and pie cover the other two charts; decorations and output cover labels, saving and the show lifecycle. Everything ran under Matplotlib 3.11.2 and, for the book's pin, 3.9.2, with the Agg backend and with a real Tk window on a virtual display [T].")
_b('FigureModel',
 'The chapter calls plt a short name for matplotlib.pyplot, says a figure is the window that holds one or more plots and that Matplotlib picks colours and size by itself [S]. The Matplotlib guide to its interfaces says pyplot keeps a list of figures and that gcf and gca return the current figure and axes [MPL].',
 'Three leaves cover it: how state piles up in the current figure, the defaults of a figure, and the backend choice. A figure was 640 by 480 pixels, a second plot call added a second line to the same axes, and the backend was agg with no display and tkagg with one [T].')
_b('PyplotState',
 'The chapter calls plt.plot() twice to put two lines on one graph, saves with savefig() and calls plt.show() [S]. The Matplotlib interface guide calls pyplot an implicit interface that keeps track of the last Figure and Axes created and adds artists to the object it thinks the user wants [MPL].',
 'With Agg two plot() calls made 2 lines, plt.show() returned None at once and figure 1 stayed open, and a following plt.scatter() added 1 collection to the same axes [T]. In the headless replay each later example drew on the figure of the earlier ones: at the four calls of savefig() the axes held 2 lines and 0 collections, 2 lines and 2 collections, 2 lines and 2 collections with 4 bars, and the same with 8 patches for the pie, whereas with a window each plt.show() emptied them and the pie figure held only its 4 wedges.')
_b('FigureDefaults',
 'The chapter says Matplotlib selects colours for the lines and an appropriate size for the graph automatically, and does not give the size [S]. The Matplotlib savefig reference documents the dpi argument [MPL].',
 "A new figure was 6.4 by 4.8 inches at 100 dpi, which is 640 by 480 pixels, and the first line colour was #1f77b4 in every release; but the colour cycle held texts such as '#1f77b4' in 3.7.5 to 3.10.8 and tuples of floats in 3.11.0 and 3.11.2 [T]. The chapter prints neither, so only the size of the saved PNGs can be compared with the figures of the book.")
_b('BackendChoice',
 'The chapter says plt.show() opens a window with the graph and that the window is interactive, and says nothing about a program that has no window [S]. The Matplotlib backends guide separates interactive backends such as TkAgg from non-interactive ones such as Agg [MPL].',
 "With no DISPLAY Matplotlib 3.11.2 chose agg and with a display it chose tkagg, and matplotlib.is_interactive() was False [T]. The first choice is why the chapter's listings run to the end in a container without opening a window.")
_b('LineAndScatter',
 'The chapter says a line graph is ideal for showing changes in one measure over time and makes it with plt.plot() twice, then makes the scatter plot of the same data with plt.scatter(), noting that the code is identical except for the function name [S]. The Matplotlib pages document both functions [MPL].',
 'Two leaves cover it: the line plot and the scatter plot. plot() returned a list holding one Line2D, scatter() a PathCollection stored beside the lines and not among them, and the two series got the colours #1f77b4 and #ff7f0e [T].')
_b('LinePlot',
 'The chapter plots x_values against y_values1 and y_values2 and shows the shell returning a list for each call, and the first values of the two lists belong together [S]. The Matplotlib reference says plot() returns a list of Line2D objects [MPL].',
 'plot() returned a list of 1 Line2D whose y data were 10, 13, 15, 18, 16 and 20, and the colours of the two lines were #1f77b4 and #ff7f0e [T]. In Matplotlib 3.11 the colour is kept as a tuple of floats and not as a text.')
_b('ScatterPlot',
 'The chapter says the scatter plot uses points instead of connected lines and that the data are the same as in the line graph [S]. The Matplotlib reference says scatter() returns a PathCollection [MPL].',
 'scatter([0, 1, 2], [3, 1, 2]) returned a PathCollection; the axes then held 1 collection and 0 lines, and the offsets were an array of shape (3, 2) [T]. A program that counts ax.lines to know what is drawn finds nothing for a scatter plot.')
_b('BarAndPie',
 'The chapter says a bar graph compares the same data in different categories, that unlike a line graph the order of categories is not important, and that a pie chart has labels and slices and an autopct format string [S]. The Matplotlib pages for bar() and pie() document both [MPL].',
 'Two leaves cover it: the bar chart and the pie chart. bar() returned a BarContainer in the order given, and pie() returned a tuple in Matplotlib 3.10 and earlier and a PieContainer in 3.11, which the 3.11 API changes name [T].')
_b('BarChart',
 'The chapter calls plt.bar(categories, values) with the four categories Cats, Dogs, Mice and Moose and the values 100 to 400 and says the order of categories is not important [S]. The Matplotlib reference says bar() returns a BarContainer and accepts categorical x values [MPL].',
 'bar() returned a BarContainer, the heights were 100, 200, 300 and 400 as numpy int64 values and the tick labels were the four names in the given order, so the chart is not sorted [T]. The values come back as numpy integers, not Python ints, which matters when they are printed or compared with JSON.')
_b('PieChart',
 "The chapter calls plt.pie(slices, labels=labels, autopct='%.1f%%') and shows a printed tuple, and says that without autopct the chart will not list the percentage text [S]. The Matplotlib reference says that since 3.11 pie() returns a PieContainer and that the wedges and texts were returned in a tuple before [MPL].",
 "Matplotlib 3.11.2 returned a PieContainer that unpacked into 3 parts with autopct and 2 without it, whose len() raised TypeError; the percent texts were '10.0%', '20.0%', '30.0%' and '40.0%' and the first wedge ran from 0 to 36 degrees; releases 3.7.5 to 3.10.8 returned a tuple of 3 [T]. The book's printed tuple therefore matches the pinned Matplotlib and not the newest.")
_b('DecorationsAndOutput',
 "The chapter adds marker, color and label keywords, calls plt.legend(), plt.xlabel(), plt.ylabel(), plt.title() and plt.grid(True), and says to call plt.savefig() before plt.show() [S]. The Matplotlib savefig reference gives dpi the default 'figure', the dpi of the figure, and documents format [MPL].",
 'Three leaves cover it: the decorations and what they return, the saved file, and the life of a figure through plt.show(). The saved PNG was 640 by 480 pixels, plt.show() on Agg left the figure, and a real Tk window changed that [T].')
_b('PlotDecorations',
 "The chapter's example gives the lines marker='o' with color='b' and marker='s' with color='r', labels them, adds a legend and the three labels, and prints Text(0.5, 0, 'X-axis Label'), Text(0, 0.5, 'Y-axis Label') and Text(0.5, 1.0, 'Graph Title') [S]. The Matplotlib reference for plot() lists the marker and color codes [MPL].",
 "Right after the call plt.xlabel returned Text(0.5, 0, 'X-axis Label'), plt.ylabel Text(0, 0.5, 'Y-axis Label') and plt.title Text(0.5, 1.0, 'Graph Title'), and plt.legend() returned a Legend; the first two texts changed their coordinates once the figure had been drawn in a headless run, which is where two lines of listing 30 did not match [T].")
_b('SaveFigure',
 "The chapter saves with plt.savefig('linegraph.png') and says the call must come before plt.show() [S]. The Matplotlib reference says dpi defaults to the figure's dpi value and format names the file format [MPL].",
 'The default PNG was 640 by 480 pixels in mode RGBA with a density of 100 dpi, and dpi=200 gave 1280 by 960 [T]. A PNG that Matplotlib writes does carry a pixel density, while the PNG that Pillow writes by default carries none.')
_b('ShowLifecycle',
 'The chapter says plt.show() blocks until the window is closed, that closing it resets the graph data so a second plt.show() does nothing or shows an empty window, and that plt.savefig() must come first [S]. Appendix B answer 12 says you cannot call plt.show() twice in a row because it resets the graph data [S]. The Matplotlib show reference says that at the end of a blocking show() the figure is closed and unregistered from pyplot and that calling savefig() afterwards would save a new and thus empty figure [MPL].',
 "With Agg plt.show() returned None at once, the figure stayed and a savefig() after it still held the line; with a real Tk window it blocked until the window closed, the figure list was then empty, a second show returned at once, and a savefig() after the window saved a blank image of 1 colour, while showing a new empty figure blocked again [T]. The chapter's rule holds for a window and the answer of Appendix B holds for it only.")
# ---- BookAndPractice ----
_b('BookAndPractice',
 'The rest of the chapter is the pins and files around the text: Appendix A names the packages to install, the summary and the 12 practice questions check what was learned, and three practice programs, Tile Maker, the photo folder finder and the seating cards, use the files of the online materials [S]. Appendix B gives the answers [S].',
 "Four ideas carry this subject: install and versions cover the pins and the Python they run on; book corrections cover the statements and files that do not hold; deprecated interfaces cover what the newest Pillow removed or warns about; the practice programs were written from the chapter's text and run. The sources that the chapter itself points to were fetched on the day, and the zip of the publisher was fetched and hash-checked at run time [T]. The chapter page returned 200 with 119,144 bytes, holds 31 listings, 20 figures and 1 table, and its sha256 equals the chapterDigest of the book's own chapter ontology; nothing ran on Windows or macOS, the PDFs of the JPEG standard and of JFIF were reached but not searched, the commit the course pins was not opened, and the photograph of the stories was not fetched because the single request to Wikimedia Commons answered 429 [T].")
_b('InstallAndVersions',
 'The chapter tells the reader to install Pillow, Matplotlib and pyperclipimg by Appendix A, which pins pillow==10.4.0 and matplotlib==3.92 and lists pyperclipimg with no number [S]. PyPI lists the releases and the Python each one supports [PYPI].',
 "Four leaves cover it: the pins, the first wheels for Python 3.14, the pinned Matplotlib built from source and the Tk 9.0 clash. On Python 3.14.6 the pinned Pillow built and ran, the pinned Matplotlib built but could not draw, and its window backend could not load [T]. The 138 statements of the chapter's 25 interactive listings, replayed as printed, matched 131 headless and 135 on a virtual X display with the newest packages, 125 and 108 with the pins built on 3.14.6, 129 and 108 with the pins as wheels on Python 3.13.14, and 15 with an empty Python.")
_b('AppendixPins',
 'Appendix A lists pillow==10.4.0, matplotlib==3.92 and requests==2.32.3 and does not number pyperclipimg [S]. PyPI shows the releases of Matplotlib as plain numbers such as 3.9.2, 3.10.0 and 3.11.2 [PYPI].',
 'PyPI had no release 3.92 of Matplotlib among its 85 plain-numbered releases; the number reads as 3.92.0, which is greater than 3.11.2 and than 3.9.2, and the resolver of uv answered that there is no version of matplotlib==3.92 and the requirements are unsatisfiable [T]. The pyperclipimg version PyPI lists is 0.2.0, which is the one that ran.')
_b('PythonWheelSupport',
 'The Pillow page on Python support lists the Python versions each release supports, and its release notes of 12.0.0 say Pillow 11.3.0 had wheels for the 3.14 beta and Pillow 12.0.0 officially supports Python 3.14 [PILLOW]. PyPI lists the files of each release, and a wheel is built for one interpreter series; for a release without one the installer builds from source, as it did here [PYPI][T].',
 'PyPI listed no CPython 3.14 wheel for Pillow before 11.3.0 and none for Matplotlib before 3.10.5, so the pinned Pillow 10.4.0 and Matplotlib 3.9.2, which have 3.13 wheels, need a compiler and the libjpeg, FreeType and Qhull headers under 3.14 [T]. The Python itself was installed with uv, and one program of 35 items printed the same under 11 interpreters, Python 3.11.17, 3.12.3, 3.13.14, 3.14.0 to 3.14.6 and 3.15.0b4, each with Pillow 12.3.0 and Matplotlib 3.11.2, so every difference found came from the releases of the packages and not of Python.')
_b('PinnedBuildOnSource',
 "The book pins Matplotlib as 3.92, meaning 3.9.2, and the Pillow page of Python support says Pillow 12 supports Python 3.14 [PILLOW]. Matplotlib's dependency page lists Tk (>= 8.5, != 8.6.0 or 8.6.1) for the Tk-based backends, a rule with no upper limit [MPL].",
 'Matplotlib 3.9.2 built from source on Python 3.14.6, but savefig(), legend() and similar calls raised RecursionError while copying a MarkerStyle, while Pillow 10.4.0 built and behaved as the book prints; the same Matplotlib 3.9.2 on Python 3.13.14 matched the book except for 2 lines [T]. The pinned pair is therefore a Python 3.13 pair.')
_b('TkVersionNine',
 "The chapter's windows are Tk windows, which tkinter provides; the Python documentation of tkinter writes the Tcl/Tk version in the notation '9.0.3' and says Tk 9.0 added window attributes [PY], and the Tcl project publishes Tcl and Tk 9.0 [TCL].",
 "The uv Pythons 3.14.6 and 3.13.14 reported TkVersion 9.0, and Matplotlib 3.9.2 failed to start a TkAgg window with ImportError: Failed to load Tcl_SetVar in both, while Matplotlib 3.11.2 opened its windows; the replay's display mode matched 135 of 138 statements with the newest packages and only 108 with the pinned ones [T]. The 3 that did not match were the Windows path, the font and the pie.")
_b('BookCorrections',
 'Several statements of the chapter and its appendices do not hold when they are run: a table value, the pixel density of a PNG, the fill of a rotated corner, three answers of Appendix B and the files said to be in the online resources [S].',
 'Five leaves cover them: the green of Table 21-1, the 72 pixels per inch, the rotation fill, the answers of Appendix B and the missing files. Each was found by running the statement, not by comparing texts, and each has a number or a name in its leaf [T].')
_b('GreenTableError',
 'Table 21-1 lists eight names and says they are standard HTML colour names, among them Green as (0, 255, 0, 255) and Gray as (128, 128, 128, 255) [S]. The CSS Color module lists green as #008000, which is 0 128 0, and lime as #00ff00, which is 0 255 0 [CSS].',
 "Of the 8 rows only one differed: ImageColor.getcolor('Green', 'RGBA') was (0, 128, 0, 255) and 'Lime' was (0, 255, 0, 255), so the printed value belongs to lime [T]. The value Pillow returns is the CSS one.")
_b('DpiClaim',
 'The chapter says Pillow creates PNG images that are 72 pixels per inch by default and that a 4 by 5 inch card would require 288 by 360 pixels [S]. The Pillow format page documents the dpi option of the PNG writer and the PNG specification defines the pHYs chunk [PILLOW][PNG3].',
 'A PNG saved with no dpi had no pHYs chunk and no dpi to read back; with dpi=(72, 72) the chunk held 2835 pixels per metre and Pillow read it back as 72.009, and the sums 288 / 72 and 360 / 72 gave 4 and 5 inches [T]. A JPEG saved with defaults had a jfif_density of (1, 1) with unit 0, which is no unit.')
_b('RotateFillClaim',
 "The chapter says that on Windows a black background fills the gaps of a rotation and that on macOS and Linux transparent pixels fill them instead [S]. Pillow's reference for rotate() names a fill colour for the area outside and no operating system [PILLOW].",
 "zophie.png is RGB, and on this Linux machine rotate(6) left (0, 0, 0) at its corner, black, while only an RGBA copy gave (0, 0, 0, 0) [T]. A picture with no alpha band cannot hold a transparent pixel on any system, so the chapter's Linux statement is true only for images that already have alpha.")
_b('AppendixBErrors',
 'Appendix B answers question 3 with left, top, width and height, question 6 with im.crop((0, 50, 50, 50)) for the lower-left quarter of a 100 by 100 image, and question 12 with the statement that plt.show() resets the graph data so it cannot be called twice [S]. The chapter itself defines the box as left, top, right and bottom [S].',
 "The box of answer 6 gave the size (50, 0), an empty picture, and (0, 50, 50, 100) gave the 50 by 50 quarter; the box definition of answer 3 contradicts the chapter's; and answer 12 holds for a Tk window and not for Agg [T].")
_b('MissingFiles',
 "The chapter points to the book's online resources for zophie.png, catlogo.png and guests.txt, shows output for zophie_xmas_tree.png and me_and_zophie.png, uses zophie_the_cat.jpg in a practice program and says a public domain flower image is also available [S]. The book page links the zip [NSP].",
 "The zip of 7,759,877 bytes with 91 files, 72 of them Python, held 4 of the chapter's files, zophie.png, catlogo.png, guests.txt and resizeAndAddLogo.py, and none of zophie_xmas_tree.png, me_and_zophie.png, zophie_the_cat.jpg or a file with flower in its name, among 184 entries [T]. The study therefore made its own pictures where the book's are missing and says so.")
_b('DeprecatedApis',
 "The chapter uses neither textsize() nor getsize(), which the 2nd edition's chapter 19 used [S][S2E]. The Pillow deprecation page lists what is removed and what is deprecated and when [PILLOW].",
 'Two leaves cover it: textsize and getsize, which are gone, and getdata, which warns. Across the 14 Pillow releases run, textsize and getsize existed only in 9.5.0, and the warning for getdata appeared in 12.1.0, 12.2.0 and 12.3.0 [T].')
_b('TextsizeGone',
 "The 2nd edition's chapter 19 mentions Pillow 30 times, ImageFont 13 times and textsize 3 times, and neither matplotlib nor pyperclipimg, and the Pillow release notes of 10.0.0 say ImageDraw.textsize() and ImageFont.getsize() were removed in favour of textbbox(), textlength() and getbbox() [S2E][PILLOW]. The 3rd edition's chapter does not use them [S].",
 "In 12.3.0 hasattr gave False for ImageDraw.textsize and for FreeTypeFont.getsize and True for textbbox, textlength and getbbox; the 14 releases split at 9.5.0, which had both, and 10.0.0, which had neither [T]. Code copied from the 2nd edition fails with AttributeError on any Pillow of the book's pin.")
_b('GetdataDeprecation',
 "The chapter does not use getdata(), and the Pillow deprecation page says getdata() has been deprecated since 12.1.0 and that get_flattened_data() can be used instead [PILLOW]. This study's own programs used getdata() to count pixels [T].",
 "In Pillow 12.3.0 list(im.getdata()) gave a DeprecationWarning, Image.Image.getdata is deprecated and will be removed in Pillow 14 (2027-10-15), and get_flattened_data existed; 12.0.0 gave no warning and 12.1.0 did [T]. The study's counting loops must change before that date.")
_b('PracticePrograms',
 "The chapter's three practice programs are Tile Maker, which makes a larger image from one tile with make_tile(), the photo folder finder, which walks the hard drive for folders that are mostly large pictures, and the seating cards for the guests of guests.txt [S]. The chapter says guests.txt and a flower image are among the book's online resources [S].",
 "Three leaves cover them: the tile maker, the finder and the cards. The publisher's book page had 1 occurrence of Making Graphs and 0 of Pillow, Matplotlib, zophie or catlogo, and the chapter gives the three tasks only as text and a skeleton, so the programs were written from that text and run, on pictures made by the program and on the shipped guests.txt, which the program fetched and hash-checked [T].")
_b('TileMaker',
 'The chapter asks for make_tile() with a string filename and two integers for the number of tiles across and down, and says a 20 by 50 pixel zophie_the_cat.jpg tiled 6 by 10 should give a 120 by 500 image with 60 tiles [S]. Its bonus asks for random flips or rotations [S].',
 "make_tile('zophie_the_cat.jpg', 6, 10) on a 20 by 50 file returned a 120 by 500 image and counted 60 pastes, as the book says; the file zophie_the_cat.jpg is not in the zip, so a 20 by 50 file was made [T]. Flipping keeps the 20 by 50 size and a 90 degree turn gives 50 by 20, so the bonus needs square tiles or a larger cell.")
_b('PhotoFolderFinder',
 "The chapter defines a photo folder as one where more than half of the files are photos, a photo as a .png or .jpg file whose width and height are both larger than 500 pixels, and gives a skeleton around os.walk('C:\\\\') [S]. The Python os documentation describes os.walk [PY].",
 'On a test tree the program found ./a, with 2 photos of 3 files, and ./b/c, with 3 of 4, and not ./b, with 0 of 2, because 300 by 300 and 2000 by 400 are not both larger than 500 [T]. The skeleton as printed raised NameError because it never imports os.')
_b('SeatingCards',
 "The chapter asks for one image for each guest of guests.txt with the name and some flowery decoration and a black rectangle at the edges, and says Pillow's PNGs are 72 pixels per inch so a 4 by 5 inch card is 288 by 360 pixels [S]. It points to a public domain flower image in the online resources [S].",
 'guests.txt held 5 names, Prof. Plum, Miss Scarlet, Col. Mustard, Al Sweigart and Robocop; 28 pixel DejaVu Sans made the widest name, 176 pixels, which fits in 288; the card was 288 by 360 and its border pixel black [T]. The cards need dpi=(72, 72) to carry the inch size, and no flower file is in the zip, so a pink circle stood in for it.')

PUBS.sort(key=lambda p: p[0])
_CITE = {
 "S": "(Sweigart, 2025)", "S2E": "(Sweigart, 2019)", "PPI": "(Sweigart, 2024)", "NSP": "(No Starch Press, 2025)",
 "PILLOW": "(Pillow Developers, 2026)", "MPL": "(Matplotlib Development Team, 2026)", "PYPI": "(Python Package Index, 2026)",
 "PY": "(Python Software Foundation, 2026)", "CSS": "(World Wide Web Consortium, 2026)", "PNG3": "(World Wide Web Consortium, 2026)",
 "TCL": "(Tcl Developer Exchange, 2026)", "ASTRAL": "(Astral, 2026)", "T": "(This study, 2026)",
}
for _k in list(BODY):
    _t = BODY[_k]
    for _n, _v in _CITE.items():
        _t = _t.replace("[" + _n + "]", _v)
    BODY[_k] = _t.replace('"', "'")
