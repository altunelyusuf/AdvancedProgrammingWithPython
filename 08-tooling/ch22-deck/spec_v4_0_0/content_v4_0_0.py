"""Chapter 22 deck content, version 4.0.0 (SEN0414, Lineage14): the words of the deck "Reading Text from Images with OCR". Parts, plan, concept slides in plain words (no everyday comparison), stories,
the native table of limits that the run itself measured, take-aways, practice and resources.
Slide numbers of the plan: 1 title, 2 route, 3 questions, 4-11 part 1, 12-18 part 2, 19-24 part 3, 25-30 part 4, 31-36 part 5 (practice 36), 37 summary, 38 resources. The notes are in notes_v4_0_0.py."""
__version__ = "4.0.0"
import difflib

TRUTH = "The quick brown fox jumps over the lazy dog"

PARTS = {
    1: ("Part 1: The engine and the first reading", "Tesseract does the reading; pytesseract carries the picture to it and the text back", [
        ("engine", "pytesseract is a bridge to the program Tesseract"),
        ("one line", "image_to_string() returns a str that ends with a line break"),
        ("lines", "One str for the whole picture; splitlines() splits it"),
        ("data", "image_to_data() gives every word a box and a confidence")]),
    2: ("Part 2: What makes reading fail", "Size, tilt and noise each have a limit that the run measures", [
        ("size", "Text below 9 pixels high is not read"),
        ("tilt", "The reading weakens from 6 degrees and fails at 9"),
        ("noise", "Noise up to 100 is read; from 105 nothing is"),
        ("limits", "Three limits, measured in one table")]),
    3: ("Part 3: Cleaning, settings and languages", "Repair the picture, tell Tesseract what to expect, name the language", [
        ("cleaning", "Turn back, enlarge; black and white can hurt"),
        ("settings", "--psm and a whitelist narrow what is read"),
        ("languages", "lang= selects the language file; a missing one raises an error"),
        ("accents", "The English file turns an accented letter into another letter")]),
    4: ("Part 4: Mistakes, PDF and scanners", "Find the mistakes, write a searchable PDF, call the scanner program NAPS2", [
        ("mistakes", "get_opcodes() names each difference"),
        ("PDF", "A picture with an invisible text layer"),
        ("subprocess", "run() starts another program"),
        ("NAPS2", "A missing program raises FileNotFoundError")]),
    5: ("Part 5: The screen and the practice program", "Read a region of the screen, then repeat it in a loop", [
        ("screenshot", "A picture of the screen; crop() keeps a region"),
        ("region", "Read only the part that holds the text"),
        ("loop", "Screenshot, crop, read, append"),
        ("questions", "Predict, run, check")]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("story", "goldberg"), ("code", "engine"), ("analogy", "A2"), ("code", "read"), ("code", "lines"), ("code", "data"),
        ("divider", 2), ("analogy", "A3"), ("story", "kurzweil"), ("code", "size"), ("code", "tilt"), ("code", "noise"), ("compare", "limits"),
        ("divider", 3), ("analogy", "A4"), ("story", "tesseract"), ("code", "clean"), ("code", "config"), ("code", "lang"),
        ("divider", 4), ("analogy", "A5"), ("story", "recaptcha"), ("code", "mistakes"), ("code", "pdf"), ("code", "naps"),
        ("divider", 5), ("analogy", "A6"), ("story", "frankenstein"), ("code", "screen"), ("code", "scraper"), ("practice",),
        ("summary",), ("resources",)]

ROUTE_RUNS = {1: "engine, read, lines, data", 2: "size, tilt, noise, limits", 3: "clean, config, lang", 4: "mistakes, PDF, NAPS2", 5: "screen, scraper"}
ROUTE_TAIL = ("Summary and links", "what to remember, where next")

QUESTIONS = [
    ("1", "Which three properties of a picture decide whether Tesseract can read it, and how far can each go?", "The measured limits come back on slide %d.", "summary"),
    ("2", "How does a program read a region of the screen, keep the text, and tell when the reading went wrong?", "Check yourself with the questions on slide %d.", "practice"),
]
QUESTIONS_TAKEAWAY = "Every example runs on the chapter page; read its printed result first."

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "What it is and does"
CONCEPTS_TAIL = "each explained in plain words"
ANALOGIES = [
    ("A1", "Installing Tesseract and pytesseract", "Tesseract is a program; pytesseract is the Python module that calls it, and both must be installed.", [
        ("Installing Tesseract and PyTesseract", "Install the program first, then the Python module with pip."),
        ("Windows", "Download an installer of Tesseract and add its folder to the PATH."),
        ("macOS", "Install Tesseract with a package manager such as Homebrew."),
        ("Linux", "Install the tesseract-ocr package with the system's package manager."),
        ("PyTesseract", "The third-party package that sends a picture to Tesseract and returns the text."),
        ("pytesseract", "The module name that a program imports."),
        ("Tesseract", "The open-source OCR program that does the reading."),
        ("tess.get_languages()", "Returns the list of language files that are installed."),
        ("'--install', 'ocr-eng'", "The book's arguments that install the English language data for NAPS2."),
    ]),
    ("A2", "OCR fundamentals and the first reading", "OCR turns the picture of a text into a str; image_to_string() takes a picture and returns it.", [
        ("OCR Fundamentals", "Optical character recognition turns a picture of text into text."),
        ("tess.image_to_string()", "Takes a picture and returns everything it read as one str."),
        ("PIL.Image", "The Pillow module whose Image object pytesseract accepts."),
        ("Image.open()", "Opens a picture file as an Image object."),
        ("ocr-example.png", "The book's four-line example picture."),
        ("frankenstein.png", "The book's scan of a printed page."),
        ("Figure 22-1: the top part of a scanned page from an 1831 print of Frankenstein by Mary Shelley", "A scan with a page header and a paragraph."),
    ]),
    ("A3", "Preparing a picture for reading", "Size, tilt and noise decide how well Tesseract reads; each has a repair that the examples test.", [
        ("Preprocessing an Image", "Changes made to a picture before it is read: turn, enlarge, remove noise, reduce to black and white."),
    ]),
    ("A4", "Languages other than English", "lang= names the language file; the default is English, which has no letters such as ü or ß.", [
        ("Recognizing Text in Non-English Languages", "Install the language file, then pass its code as lang=."),
        ("lang='eng+jpn'", "Two language files at once, joined by a plus sign."),
        ("frankenstein_jpn.png", "The book's page with Japanese text."),
    ]),
    ("A5", "Mistakes, searchable PDFs and NAPS2", "A reading has mistakes that can be found, a PDF can carry the text, and NAPS2 is another program that subprocess starts.", [
        ("Fixing Mistakes Using Large Language Models", "A language model can correct the remaining mistakes of a reading; the program checks the result."),
        ("NAPS2", "The program's short name; its console version is called NAPS2.Console."),
        ("The NAPS2 Scanner Application", "A free scanner program with a command line."),
        ("Installing and Setting Up NAPS2", "Install it, then add the language file for the language of the page."),
        ("Running NAPS2 from Python", "subprocess.run() starts the program with its arguments."),
        ("Specifying Input", "-i names the picture to read; -o names the output file."),
        ("subprocess", "The standard module that starts other programs."),
        ("subprocess.run()", "Starts a program and waits for it; check=True raises an error if it fails."),
        ("'-n', '0'", "The NAPS2 argument that scans no new page."),
        ("output.pdf", "The searchable PDF that the program writes."),
        ("ocrmypdf", "A command-line program that adds an invisible text layer to a PDF."),
    ]),
    ("A6", "The screen and the practice program", "pyautogui takes a picture of the screen; a loop crops, reads and appends the text to a file.", [
        ("pyautogui", "The third-party module that controls the mouse, the keyboard and the screen."),
        ("pyautogui.screenshot()", "Returns a picture of the screen as an Image."),
        ("Figure 22-2: an example web page with an embedded document", "A page whose text is a picture and cannot be copied."),
        ("Practice Program: Browser Text Scraper", "Reads the text of each page of an embedded document from screenshots."),
        ("output.txt", "The text file that the scraper appends to."),
        ("ocrscreen.py", "The book's name for the finished program."),
    ]),
]

STORIES = {
    "goldberg": dict(
        title="Story: A machine of 1931 searched microfilm by recognizing patterns", img="image_goldberg.jpg",
        prose=["In 1931 the engineer Emanuel Goldberg was granted US patent 1,838,389 for his Statistical Machine, which searched rolls of microfilm with photoelectric cells and pattern recognition.",
               "The picture shows the memorial stone laid for him in Dresden: born 1881, fled in 1933 to France, and in 1937 to Palestine.",
               "Tesseract also looks for the shapes of letters in a picture; image_to_string() returns what it found as a str."],
        linktext="Emanuel Goldberg (Wikipedia)", link="https://en.wikipedia.org/wiki/Emanuel_Goldberg"),
    "kurzweil": dict(
        title="Story: The first reading machine for blind people was unveiled in 1976", img="image_kurzweil.jpg",
        prose=["Ray Kurzweil founded Kurzweil Computer Products in 1974 to build OCR that reads any typeface, not one fixed font.",
               "The reading machine for blind people, which scanned a page and spoke it aloud, was unveiled on 13 January 1976.",
               "A reading is only as good as its picture: part 2 measures how small, how crooked and how noisy a picture may be."],
        linktext="Kurzweil Computer Products (Wikipedia)", link="https://en.wikipedia.org/wiki/Kurzweil_Computer_Products"),
    "tesseract": dict(
        title="Story: Tesseract began at Hewlett-Packard in 1985 and became open source", img="image_tesseract.jpg",
        prose=["Tesseract was developed at Hewlett-Packard laboratories from 1985.",
               "Hewlett-Packard released it as open source in 2005, and Google sponsored its development from 2006.",
               "The picture shows Wikisource, where Tesseract OCR is one choice of transcription tool, here set to the Tamil script."],
        linktext="Tesseract (Wikipedia)", link="https://en.wikipedia.org/wiki/Tesseract_(software)"),
    "recaptcha": dict(
        title="Story: reCAPTCHA used what OCR could not read to digitize books", img="image_recaptcha.jpg",
        prose=["reCAPTCHA began at Carnegie Mellon University in a team around Luis von Ahn, and Google acquired it in September 2009.",
               "It showed two words: one the program knew, and one that OCR had failed to read. A correct first answer gave weight to the second.",
               "Part 4 looks at the mistakes of a reading in the same spirit: compare it with a known text, and see where it differs."],
        linktext="reCAPTCHA (Wikipedia)", link="https://en.wikipedia.org/wiki/ReCAPTCHA"),
    "frankenstein": dict(
        title="Story: The 1831 edition of Frankenstein is the page the book scans", img="image_frankenstein.jpg",
        prose=["Mary Shelley's Frankenstein appeared anonymously in 1818; a revised edition of 1831 carries her name.",
               "The picture is the frontispiece engraving of that edition by Theodor von Holst. The book's Figure 22-1 is a scan of a page of the same print.",
               "A scan of an old print is the hard case for OCR; the screenshot of part 5 is the easy case, because the text is sharp."],
        linktext="Frankenstein (Wikipedia)", link="https://en.wikipedia.org/wiki/Frankenstein"),
}


def _limits():
    """measure the three limits with the real Tesseract (the same helpers as the examples); the table is made of what was measured"""
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    import pytesseract as tess

    def page(px, tilt=0):
        font = ImageFont.load_default(size=px)
        im = Image.new("L", (int(font.getlength(TRUTH)) + 60, px * 3), 255)
        ImageDraw.Draw(im).text((30, px), TRUTH, fill=0, font=font)
        return im.rotate(tilt, expand=True, fillcolor=255) if tilt else im

    def score(im):
        return difflib.SequenceMatcher(None, TRUTH, tess.image_to_string(im).strip()).ratio()

    def noisy(im, s):
        a = np.array(im, dtype=int) + np.random.default_rng(1).integers(-s, s + 1, (im.height, im.width))
        return Image.fromarray(np.clip(a, 0, 255).astype("uint8"))
    size = min(px for px in range(6, 17) if score(page(px)) >= 0.9)
    tilt = max(d for d in range(0, 9) if score(page(24, d)) >= 0.9)
    noise = max(s for s in range(0, 141, 5) if score(noisy(page(24), s)) >= 0.9)
    small = page(8)
    big = small.resize((small.width * 3, small.height * 3), Image.Resampling.LANCZOS)
    crooked = page(24, 10)
    fixed = crooked.rotate(-10, expand=True, fillcolor=255)
    return size, tilt, noise, score(big), score(fixed)


_SIZE, _TILT, _NOISE, _BIG, _FIXED = _limits()
COMPARES = {
    "limits": dict(
        title="Three limits of a reading, measured by the run", sub="Reading counts as good when the similarity to the truth is at least 0.9",
        colw=[2.6, 2.2, 3.2, 2.0], rowh=0.5, fs=11,
        rows=[["Property of the picture", "Good down to or up to", "Repair tested in the examples", "Result of the repair"],
              ["Height of the text", "%d pixels" % _SIZE, "enlarge three times (LANCZOS)", "%.2f at 8 pixels" % _BIG],
              ["Tilt of the page", "%d degrees" % _TILT, "turn back by the tilt", "%.2f at 10 degrees" % _FIXED],
              ["Noise added to each pixel", "%d of 255" % _NOISE, "none found in these examples", "-"]],
        takeaway="Three limits; two repairs worked, and black and white made one reading worse."),
}

TAKEAWAY = {
    "engine": "pytesseract calls the program Tesseract: install both.",
    "read": "image_to_string() returns a str; strip() removes the line break.",
    "lines": "The whole picture comes back as one str; splitlines() gives the lines.",
    "data": "image_to_data() gives each word, its confidence and its position.",
    "size": "Text below 9 pixels high is not read.",
    "tilt": "A page tilted by 9 degrees or more is not read.",
    "noise": "Noise above 100 empties the reading.",
    "clean": "Repair the cause: turn back, enlarge; test every step.",
    "config": "--psm 7 and a whitelist narrow what is read.",
    "lang": "Name the language: lang='deu' reads ü and ß.",
    "mistakes": "Compare with the truth: get_opcodes() lists each mistake.",
    "pdf": "image_to_pdf_or_hocr() makes a PDF that can be searched.",
    "naps": "A program that is not installed raises FileNotFoundError.",
    "screen": "Crop the screenshot to the text before reading it.",
    "scraper": "Screenshot, crop, read, append: one loop.",
}

SUMMARY_ANALOGY = "Four claims: install two parts, mind the picture, name the language, check the reading."
SUMMARY_POINTS = [
    "pytesseract is a bridge to the program Tesseract; image_to_string() returns a str.",
    "Size, tilt and noise each have a limit; turn back and enlarge before reading.",
    "lang= names the language, and --psm and a whitelist narrow the reading.",
    "Compare a reading with a known text; crop a screenshot to its text first.",
]
SUMMARY_TAKEAWAY = "Two questions of slide 3: the limits of a picture, and reading a region of the screen."

PRACTICE_SUB = "Use the slide of the part named in each question"
PRACTICE_ANALOGY = "Each practice question has a short answer; run the code on the chapter page to check it."
PRACTICE = [
    "What two things must be installed before image_to_string() works, and what does get_languages() list?",
    "Which text height did the run find to be the smallest that reads well, and what did it return below that?",
    "What does the whitelist digits and hyphen do to the line with a telephone number? Use the settings slide.",
    "Why does lang='deu' read ü and the English file does not, and what error does a missing language raise?",
    "What are the four steps of the browser text scraper's loop, and where does each result go?",
]
PRACTICE_TAKEAWAY = "Run the examples on the chapter page to check each answer."

RESOURCES_SUB = "The chapter, the documentation, and the pages behind the stories"
RESOURCES_TAKEAWAY = "Every link was opened on 2026-11-26."
RESOURCES_ROWS = 8
RESOURCES = [
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 22", "https://automatetheboringstuff.com/3e/chapter22.html", "automatetheboringstuff.com"),
    ("Tesseract on GitHub", "https://github.com/tesseract-ocr/tesseract", "github.com"),
    ("Tesseract documentation", "https://tesseract-ocr.github.io/tessdoc/", "tesseract-ocr.github.io"),
    ("pytesseract on GitHub", "https://github.com/madmaze/pytesseract", "github.com"),
    ("pytesseract on PyPI", "https://pypi.org/pypi/pytesseract/json", "pypi.org"),
    ("NAPS2 (Not Another PDF Scanner)", "https://www.naps2.com/", "www.naps2.com"),
    ("OCRmyPDF documentation", "https://ocrmypdf.readthedocs.io/en/latest/", "ocrmypdf.readthedocs.io"),
    ("PyAutoGUI: screenshot functions", "https://pyautogui.readthedocs.io/en/latest/screenshot.html", "pyautogui.readthedocs.io"),
    ("Python: difflib", "https://docs.python.org/3/library/difflib.html", "docs.python.org"),
    ("Python: subprocess", "https://docs.python.org/3/library/subprocess.html", "docs.python.org"),
    ("Emanuel Goldberg (Wikipedia)", "https://en.wikipedia.org/wiki/Emanuel_Goldberg", "en.wikipedia.org"),
    ("Kurzweil Computer Products (Wikipedia)", "https://en.wikipedia.org/wiki/Kurzweil_Computer_Products", "en.wikipedia.org"),
    ("Tesseract (Wikipedia)", "https://en.wikipedia.org/wiki/Tesseract_(software)", "en.wikipedia.org"),
    ("reCAPTCHA (Wikipedia)", "https://en.wikipedia.org/wiki/ReCAPTCHA", "en.wikipedia.org"),
    ("Frankenstein (Wikipedia)", "https://en.wikipedia.org/wiki/Frankenstein", "en.wikipedia.org"),
]
