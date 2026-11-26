"""Chapter 22 deck examples, version 1.0.0 (SEN0414, Lineage14): the 15 code examples of the chapter 22 lecture deck (Reading Text from Images with OCR), in slide order = page-tab order.
Every example is self-contained and runs offline with the real Tesseract 5.3.4 through pytesseract: the pictures are drawn by the program itself (the book's zip is not used), nothing reads a keyboard or opens a window, no lambda, no prompt.
NAPS2 is not installed on the machine, and its example shows the error that results; the screen of PyAutoGUI needs a display, so the two screen examples draw an emulated screen (marked EMULATED).
`groups` are the code boxes of a slide with the explanation beside each; every box parses on its own."""
__version__ = "1.0.0"

PAGE = ["def page(px, tilt=0):",
        "    font = ImageFont.load_default(size=px)",
        "    im = Image.new('L', (int(font.getlength(TRUTH)) + 60, px * 3), 255)",
        "    ImageDraw.Draw(im).text((30, px), TRUTH, fill=0, font=font)",
        "    return im.rotate(tilt, expand=True, fillcolor=255)"]
SCORE = ["def score(im):", "    read = tess.image_to_string(im).strip()", "    return round(difflib.SequenceMatcher(None, TRUTH, read).ratio(), 2)"]
SETUP = ["import difflib", "import numpy as np", "from PIL import Image, ImageDraw, ImageFont", "import pytesseract as tess",
         "TRUTH = 'The quick brown fox jumps over the lazy dog'"] + PAGE + SCORE
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

EXAMPLES = [
    # ------------------------------------------------------------ part 1: the engine and the first reading
    dict(id="engine", name="The engine and its languages", title="Is the engine installed, and which languages does it know?", part=1, visual="engine",
         concepts=["Installing Tesseract and PyTesseract", "Windows", "macOS", "Linux", "PyTesseract", "pytesseract", "Tesseract", "tess.get_languages()", "'--install', 'ocr-eng'"],
         groups=[
             (["import pytesseract as tess", "print(tess.get_tesseract_version())"],
              "pytesseract is only a bridge: the program Tesseract does the reading."),
             (["langs = tess.get_languages()", "print(len(langs), langs[:5])", "print('eng' in langs, 'xyz' in langs)"],
              "get_languages() lists the language files installed; eng must be there."),
         ]),
    dict(id="read", name="Reading one line of text", title="Reading one line with image_to_string()", part=1, visual="read",
         concepts=["OCR Fundamentals", "tess.image_to_string()", "PIL.Image", "Image.open()", "ocr-example.png", "pytesseract"],
         groups=[
             (["from PIL import Image, ImageDraw, ImageFont", "import pytesseract as tess", "font = ImageFont.load_default(size=40)",
               "im = Image.new('L', (440, 90), 255)", "ImageDraw.Draw(im).text((20, 20), 'Hello OCR 2026', fill=0, font=font)"],
              "A picture made by the program: black text on white, 440 by 90 pixels."),
             (["text = tess.image_to_string(im)", "print(repr(text))", "print(text.strip() == 'Hello OCR 2026')"],
              "The answer is a str; Tesseract ends it with a line break."),
         ]),
    dict(id="lines", name="Lines, breaks and the data behind a line", title="Lines, line breaks and the answer's type", part=1, visual="lines",
         setup=["from PIL import Image, ImageDraw, ImageFont", "font = ImageFont.load_default(size=28)", "im = Image.new('L', (560, 170), 255)", "draw = ImageDraw.Draw(im)",
                "rows = ['It was on a dreary night', 'of November that I beheld', 'the accomplishment of my toils']",
                "for n, line in enumerate(rows):", "    draw.text((20, 10 + n * 50), line, fill=0, font=font)"],
         concepts=["Figure 22-1: the top part of a scanned page from an 1831 print of Frankenstein by Mary Shelley", "frankenstein.png"],
         groups=[
             (["import pytesseract as tess", "# im holds three lines of text, drawn one under the other", "text = tess.image_to_string(im)"],
              "One call reads the whole picture."),
             (["print(type(text).__name__, len(text))", "print(text.splitlines())"],
              "One str for the whole picture; splitlines() gives the lines back."),
         ]),
    dict(id="data", name="Words, boxes and confidence", title="Words with boxes and confidence: image_to_data()", part=1, visual="data",
         setup=["from PIL import Image, ImageDraw, ImageFont", "font = ImageFont.load_default(size=32)", "im = Image.new('L', (560, 80), 255)",
                "ImageDraw.Draw(im).text((20, 20), 'Invoice 2026-114 total 482.50', fill=0, font=font)"],
         concepts=["tess.image_to_string()", "OCR Fundamentals"],
         groups=[
             (["import pytesseract as tess", "# im holds one line: Invoice 2026-114 total 482.50", "d = tess.image_to_data(im, output_type=tess.Output.DICT)"],
              "image_to_data() gives every word with its confidence and its position."),
             (["for w, c, x, y in zip(d['text'], d['conf'], d['left'], d['top']):", "    if w.strip():", "        print(w, c, x, y)"],
              "Empty entries stand for blocks and lines; strip() skips them."),
         ]),
    # ------------------------------------------------------------ part 2: what makes reading fail
    dict(id="size", name="Text that is too small", title="How small can the text be?", part=2, visual="size",
         setup=["import difflib", "from PIL import Image, ImageDraw, ImageFont", "import pytesseract as tess", "TRUTH = 'The quick brown fox jumps over the lazy dog'"],
         concepts=["Preprocessing an Image"],
         groups=[
             (PAGE, "page() draws the sentence at a text height and turns it by a tilt."),
             (SCORE, "score() compares the reading with the truth: 1.0 is perfect."),
             (["for px in (7, 8, 9, 10, 12, 16):", "    print(px, score(page(px)))"],
              "Below 9 pixels the reading is empty."),
         ]),
    dict(id="tilt", name="A page that is crooked", title="How crooked can the page be?", part=2, visual="tilt", setup=SETUP,
         concepts=["Preprocessing an Image"],
         groups=[
             (["# page() and score() are those of the size example", "for deg in (0, 4, 6, 7, 8, 9, 12):", "    print(deg, score(page(24, deg)))"],
              "Up to 8 degrees the reading holds, though it weakens from 6; at 9 it fails."),
         ]),
    dict(id="noise", name="Noise on the picture", title="How much noise can the picture carry?", part=2, visual="noise", setup=SETUP,
         concepts=["Preprocessing an Image"],
         groups=[
             (["def noisy(im, s):", "    rng = np.random.default_rng(1)", "    a = np.array(im, dtype=int) + rng.integers(-s, s + 1, (im.height, im.width))",
               "    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'))"],
              "noisy(im, s) moves each pixel up or down by at most s."),
             (["for s in (0, 50, 90, 100, 105, 110):", "    print(s, score(noisy(page(24), s)))"],
              "The reading holds up to a noise of 100 and is empty from 105."),
         ]),
    # ------------------------------------------------------------ part 3: cleaning, settings and languages
    dict(id="clean", name="Cleaning a picture before reading", title="Cleaning a picture before reading it", part=3, visual="clean", setup=SETUP,
         concepts=["Preprocessing an Image"],
         groups=[
             (["tilted = page(24, 10)", "print('tilted', score(tilted), score(tilted.rotate(-10, expand=True, fillcolor=255)))"],
              "Turn the picture back by the angle it was tilted."),
             (["small = page(8)", "big = small.resize((small.width * 3, small.height * 3), Image.Resampling.LANCZOS)", "print('small', score(small), score(big))"],
              "Enlarge small text to three times its size."),
             (["table = [0] * 128 + [255] * 128", "print('black and white', score(big.point(table)))"],
              "point(table) makes every pixel black or white; here it made the reading worse."),
         ]),
    dict(id="config", name="Telling Tesseract what to expect", title="Page modes and a whitelist of characters", part=3, visual="config",
         setup=["from PIL import Image, ImageDraw, ImageFont", "font = ImageFont.load_default(size=32)", "im = Image.new('L', (520, 90), 255)",
                "ImageDraw.Draw(im).text((20, 20), 'Call 555-0199 now: 2026', fill=0, font=font)"],
         concepts=["tess.image_to_string()"],
         groups=[
             (["import pytesseract as tess", "# im holds the line: Call 555-0199 now: 2026", "print(repr(tess.image_to_string(im).strip()))"],
              "Without settings Tesseract reads everything."),
             (["digits = '--psm 7 -c tessedit_char_whitelist=0123456789-'", "print(repr(tess.image_to_string(im, config=digits).strip()))"],
              "--psm 7 says one line; the whitelist lets only digits and hyphens through."),
         ]),
    dict(id="lang", name="Languages other than English", title="Reading German and French with lang=", part=3, visual="lang",
         setup=["import difflib", "from PIL import Image, ImageDraw, ImageFont", "import pytesseract as tess", "font = ImageFont.truetype('%s', 32)" % DEJAVU,
                "texts = {'deu': 'Straße über Äpfel schön', 'fra': 'Où est le café à côté'}",
                "def line(text):", "    im = Image.new('L', (520, 80), 255)", "    ImageDraw.Draw(im).text((20, 20), text, fill=0, font=font)", "    return im"],
         concepts=["Recognizing Text in Non-English Languages", "frankenstein_jpn.png", "lang='eng+jpn'"],
         groups=[
             (["def ratio(a, b):", "    return round(difflib.SequenceMatcher(None, a, b).ratio(), 2)"], "A similarity of 1.0 means the same text."),
             (["for lang, text in texts.items():", "    as_eng = tess.image_to_string(line(text), lang='eng').strip()", "    as_own = tess.image_to_string(line(text), lang=lang).strip()",
               "    print(lang, ratio(text, as_eng), ratio(text, as_own))"],
              "The same picture read as English and as its own language."),
             (["try:", "    tess.image_to_string(line(texts['deu']), lang='xyz')", "except tess.TesseractError as e:", "    print(type(e).__name__)"],
              "A language that is not installed raises an error."),
         ]),
    # ------------------------------------------------------------ part 4: mistakes, PDF and scanners
    dict(id="mistakes", name="Finding the mistakes of a reading", title="Finding the mistakes of a reading", part=4, visual="mistakes",
         concepts=["Fixing Mistakes Using Large Language Models"],
         groups=[
             (["import difflib", "TRUTH = 'Invoice 2026-114 total 482.50'", "read = 'lnvoice 2O26-114 totaI 482.5O'"],
              "A reading with typical mistakes: l for I, O for 0, I for l."),
             (["for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, TRUTH, read).get_opcodes():", "    if tag != 'equal':", "        print(tag, repr(TRUTH[i1:i2]), 'read as', repr(read[j1:j2]))"],
              "get_opcodes() names each place where the two texts differ."),
             (["ratio = difflib.SequenceMatcher(None, TRUTH, read).ratio()", "print(round(ratio, 2))"],
              "One number for the whole reading; a language model can fix what remains."),
         ]),
    dict(id="pdf", name="A searchable PDF", title="A searchable PDF from a picture", part=4, visual="pdf",
         setup=["from PIL import Image, ImageDraw, ImageFont", "font = ImageFont.load_default(size=28)", "im = Image.new('L', (700, 160), 255)", "draw = ImageDraw.Draw(im)",
                "draw.text((20, 20), 'Invoice 2026-114 total 482.50', font=font, fill=0)", "draw.text((20, 80), 'Paid by bank transfer', font=font, fill=0)"],
         concepts=["output.pdf", "ocrmypdf", "subprocess", "subprocess.run()"],
         groups=[
             (["import subprocess, tempfile", "import pytesseract as tess", "# im holds two lines of text", "pdf = tess.image_to_pdf_or_hocr(im, extension='pdf')", "print(type(pdf).__name__, pdf[:5])"],
              "The answer is bytes of a PDF that has the picture and an invisible text layer."),
             (["path = tempfile.mktemp(suffix='.pdf')", "open(path, 'wb').write(pdf)", "done = subprocess.run(['pdftotext', path, '-'], capture_output=True, text=True)",
               "print([t for t in done.stdout.splitlines() if t.strip()])"],
              "pdftotext, another program, reads the text layer: the PDF is searchable."),
         ]),
    dict(id="naps", name="Running NAPS2 from Python", title="Running the scanner program NAPS2 from Python", part=4, visual="naps",
         concepts=["The NAPS2 Scanner Application", "Installing and Setting Up NAPS2", "Running NAPS2 from Python", "Specifying Input", "NAPS2", "'-n', '0'", "ocr-example.png"],
         groups=[
             (["import subprocess", "command = ['NAPS2.Console', '-n', '0', '-i', 'ocr-example.png', '-o', 'output.pdf']", "print(' '.join(command))"],
              "-n 0 scans nothing new; -i names the input picture, -o the output file."),
             (["try:", "    subprocess.run(command, check=True)", "except FileNotFoundError as e:", "    print(type(e).__name__, e.filename)"],
              "NAPS2 is not installed here: Python says so with FileNotFoundError."),
         ]),
    # ------------------------------------------------------------ part 5: the screen and the practice program
    dict(id="screen", name="Reading the screen", title="Reading text from the screen", part=5, visual="screen",
         setup=["from PIL import Image, ImageDraw, ImageFont", "import pytesseract as tess", "font = ImageFont.load_default(size=28)"],
         concepts=["pyautogui.screenshot()", "pyautogui", "Figure 22-2: an example web page with an embedded document"],
         groups=[
             (["class Screen:", "    def screenshot(self):", "        im = Image.new('RGB', (640, 300), 'white')", "        draw = ImageDraw.Draw(im)",
               "        draw.text((20, 60), 'Embedded document', fill='black', font=font)", "        draw.text((20, 120), 'Page 3 of 12: total 482.50', fill='black', font=font)", "        return im"],
              "EMULATED: a small class stands in for pyautogui, which needs a display."),
             (["shot = Screen().screenshot()", "part = shot.crop((0, 50, 640, 170))", "print(shot.size, part.size)", "print(tess.image_to_string(part).strip().splitlines())"],
              "crop() keeps the region with the text; only that region is read."),
         ]),
    dict(id="scraper", name="Practice program: browser text scraper", title="Practice program: a browser text scraper", part=5, visual="scraper",
         setup=["import os, tempfile", "from PIL import Image, ImageDraw, ImageFont", "import pytesseract as tess", "os.chdir(tempfile.mkdtemp())", "font = ImageFont.load_default(size=28)"],
         concepts=["Practice Program: Browser Text Scraper", "output.txt", "ocrscreen.py"],
         groups=[
             (["def screenshot(n):", "    im = Image.new('RGB', (640, 160), 'white')", "    line = f'Page {n} of 3: total {n * 100}.50'",
               "    ImageDraw.Draw(im).text((20, 50), line, fill='black', font=font)", "    return im"],
              "EMULATED: each call draws the next page of a document on the screen."),
             (["for n in (1, 2, 3):", "    part = screenshot(n).crop((0, 20, 640, 120))", "    text = tess.image_to_string(part).strip()", "    with open('output.txt', 'a') as f:", "        f.write(text + '\\n')"],
              "The loop: screenshot, crop, read, append to output.txt."),
             (["print(open('output.txt').read().splitlines())"], "The file holds one line for every page read."),
         ]),
]

BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def run_text(ex):
    """the hidden setup lines first (they make the files of an example), then the shown code"""
    return "\n".join(ex.get("setup", []) + code_lines(ex)) + "\n"


def code_text(ex):
    return "\n".join(code_lines(ex)) + "\n"
