"""Chapter 21 deck content, version 4.0.0 (SEN0414, Lineage14): the words of the deck "Graphs and Images". Parts, plan, concept slides in plain words (no everyday comparison), stories, the colour table, take-aways, practice and resources.
Slide numbers of the plan: 1 title, 2 route, 3 questions, 4-12 part 1, 13-20 part 2, 21-27 part 3, 28-33 part 4, 34-40 part 5 (practice 38, summary 39, resources 40). The notes are in notes_v4_0_0.py."""
__version__ = "4.0.0"
from PIL import ImageColor

PARTS = {
    1: ("Part 1: Pixels, colours and boxes", "A picture is a grid of numbers that a program can cut and tile", [
        ("colours", "Four numbers from 0 to 255 for each pixel"),
        ("boxes", "A box tuple keeps left and top, stops before right and bottom"),
        ("crop", "A new Image; the original stays as it was"),
        ("paste", "The target changes, and paste() returns None")]),
    2: ("Part 2: Changing pictures", "Masks, resizing, turning, single pixels and saving", [
        ("mask", "The alpha channel decides how much of the top picture shows"),
        ("resize and turn", "A turn keeps the canvas unless expand=True"),
        ("one pixel", "putpixel() and getpixel() change and read one"),
        ("save", "PNG keeps every pixel; JPEG has no alpha channel")]),
    3: ("Part 3: Project 16 and drawing", "A logo on every picture, then shapes and text", [
        ("the project", "Open the logo, loop over the files, resize, paste"),
        ("shapes", "Points, lines, rectangles, ellipses and polygons"),
        ("end points", "A rectangle includes its right and bottom pixels"),
        ("text", "textbbox() measures before text() draws")]),
    4: ("Part 4: The clipboard and graphs", "A picture on the clipboard, then line, scatter, bar and pie graphs", [
        ("clipboard", "copy() and paste() need a display"),
        ("pyplot", "One current figure that each call draws on"),
        ("graphs", "plot, scatter, bar and pie return what they draw"),
        ("saving", "savefig() before show(); 100 dpi by default")]),
    5: ("Part 5: Practice programs", "Tile Maker, seating cards and a search for photo folders", [
        ("tile maker", "Two loops paste one picture across and down"),
        ("seating cards", "One 288 by 360 card for each name"),
        ("photo folders", "A folder is photos when most of its files are"),
        ("questions", "Predict, run, check")]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("analogy", "A2"), ("story", "kirsch"), ("code", "colours"), ("compare", "colours"), ("code", "boxtuple"), ("code", "crop"), ("code", "paste"),
        ("divider", 2), ("analogy", "A3"), ("story", "alpha"), ("code", "mask"), ("code", "transform"), ("story", "png"), ("story", "jpeg"), ("code", "save"),
        ("divider", 3), ("analogy", "A4"), ("analogy", "A5"), ("story", "pil"), ("code", "logo"), ("code", "draw"), ("code", "text"),
        ("divider", 4), ("analogy", "A6"), ("story", "matplotlib"), ("code", "clipboard"), ("code", "line"), ("code", "barpie"),
        ("divider", 5), ("analogy", "A7"), ("code", "tile"), ("code", "seating"), ("practice",),
        ("summary",), ("resources",)]

ROUTE_RUNS = {1: "colours, boxes, crop, paste", 2: "mask, resize and turn, save", 3: "logo project, shapes, text", 4: "clipboard, line and scatter, bar and pie", 5: "tile maker, seating cards"}
ROUTE_TAIL = ("Summary and links", "what to remember, where next")

QUESTIONS = [
    ("1", "How does a program change a picture without damaging the original, and how does it name the pixels it changes?", "The four claims come back on slide %d.", "summary"),
    ("2", "How does a program turn numbers into a graph or a card, and what must it do first so that it runs with no window?", "Check yourself with the questions on slide %d.", "practice"),
]
QUESTIONS_TAKEAWAY = "Every example runs on the chapter page; read its printed result first."

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "What it is and does"
CONCEPTS_TAIL = "each explained in plain words"
# ---- the concept slides: (slide id, title, headline, [(research label, what it is and does)])
ANALOGIES = [
    ("A1", "Pixels, colours and coordinates", "A picture is a grid of pixels; each pixel is four numbers, and each position is a pair of numbers.", [
        ("Computer Image Fundamentals", "A picture is a grid of pixels, and each pixel holds numbers."),
        ("Colors and RGBA Values", "Red, green, blue and alpha, each from 0 to 255; alpha 255 is solid."),
        ("Table 21-1: Standard Color Names and Their RGBA Values", "The book's list of colour names; ImageColor knows many more."),
        ("PIL.ImageColor", "The module that turns a colour name or a hex code into numbers."),
        ("Coordinates and Box Tuples", "The origin is the top left; a box is (left, top, right, bottom)."),
        ("Figure 21-1: the x- and y-coordinates of a 28x27 image", "x counts to the right and y counts downward; the last pixel is 27, 26."),
        ("Figure 21-2: the area represented by the box tuple (3, 1, 9, 6)", "The box holds columns 3 to 8 and rows 1 to 5: 6 by 5 pixels."),
    ]),
    ("A2", "The Image type: cropping and pasting", "An Image object is made, copied, cut and pasted; crop() gives a new one, paste() changes the target.", [
        ("Manipulating Images with Pillow", "Pillow opens, changes and saves pictures through one Image object."),
        ("Working with the Image Data Type", "Image.open(), Image.new(), size, width, height, copy() and save()."),
        ("PIL.Image", "The module of the Image type; the package is installed as Pillow."),
        ("Cropping Images", "crop(box) returns a new Image of the box and leaves the original alone."),
        ("Pasting Images onto Other Images", "paste(image, (left, top)) changes the target and returns None."),
        ("Figure 21-6: nested for loops used with paste() duplicate the cat face", "Two loops over left and top paste the same face again and again."),
    ]),
    ("A3", "Resizing, turning, single pixels and masks", "Each call returns a new Image; the mask of paste() uses alpha to blend instead of replace.", [
        ("Resizing Images", "resize((width, height)) returns a new Image of exactly that size."),
        ("Rotating and Flipping Images", "rotate(degrees) turns it; expand=True keeps the corners; transpose() flips."),
        ("Figure 21-8: the image rotated six degrees normally and with expand=True", "Normally the corners are cut off; with expand=True the canvas grows."),
        ("Changing Individual Pixels", "putpixel(xy, colour) sets one pixel; getpixel(xy) reads one."),
        ("Figure 21-13: the logo with and without the third argument", "The third argument of paste() is the mask; without it the pixels are replaced."),
    ]),
    ("A4", "Project 16: a logo on every picture", "The program opens a logo, loops over a folder, shrinks big pictures and pastes the logo into a corner.", [
        ("Project 16: Add a Logo", "A program that puts the same logo on every picture of a folder."),
        ("Step 1: Open the Logo Image", "Open the logo once, before the loop, and keep its size."),
        ("Step 2: Loop Over All Files", "os.listdir() names the files; skip those that are not pictures."),
        ("Step 3: Resize the Images", "Shrink a picture to 300 at most, with its sides in proportion."),
        ("Step 4: Add the Logo and Save the Changes", "Paste the logo into the corner with its own alpha as the mask, then save."),
        ("Figure 21-12: the left and top coordinates of the logo", "Left is width minus logo width; top is height minus logo height."),
        ("resizeAndAddLogo.py", "The book's name for the finished program."),
        ("catlogo.png", "The logo of the project, a picture with an alpha channel."),
        ("Ideas for Similar Programs", "Add text, add a border, or convert a folder of pictures to one format."),
        ("os", "The standard module that lists the files of a folder."),
    ]),
    ("A5", "Drawing shapes and text on a picture", "An ImageDraw object draws points, lines, shapes and text on the Image it was made from.", [
        ("Drawing on Images", "ImageDraw.Draw(image) gives an object that draws on that image."),
        ("PIL.ImageDraw", "The module with the drawing methods."),
        ("Shapes", "Points, lines, rectangles, ellipses and polygons."),
        ("Points", "point() sets a list of pixels to a colour."),
        ("Lines", "line() joins points; width sets the thickness."),
        ("Rectangles", "rectangle() takes a box; it includes its right and bottom pixels."),
        ("Ellipses", "ellipse() fills the largest oval that fits in its box."),
        ("Polygons", "polygon() joins a list of corners and closes the shape."),
        ("A Drawing Example", "The book draws one of each shape and saves drawing.png."),
        ("Figure 21-14: the resulting drawing.png image", "The result: shapes of several colours on a white picture."),
        ("Text", "text() draws a string; textbbox() measures it first."),
        ("PIL.ImageFont", "The module that loads a font file or the library's own font."),
    ]),
    ("A6", "The clipboard and Matplotlib graphs", "pyperclipimg moves a picture through the clipboard; pyplot draws graphs from lists of numbers.", [
        ("Copying and Pasting Images to the Clipboard", "copy() puts a picture on the clipboard; paste() gets one back."),
        ("pyperclipimg", "The third-party module for pictures on the clipboard; it needs a display."),
        ("Creating Graphs with Matplotlib", "Matplotlib draws graphs from lists of numbers."),
        ("matplotlib.pyplot", "The module with plot(), scatter(), bar(), pie() and savefig()."),
        ("Line Graphs and Scatter Plots", "plot() joins the points; scatter() only marks them."),
        ("Bar Graphs and Pie Charts", "bar() draws one bar for each value; pie() one wedge."),
        ("Additional Components", "A title, axis labels, a legend and a grid."),
        ("Figure 21-20: the example line graph with additional components", "A line graph with a title, labels and a legend."),
    ]),
    ("A7", "The practice programs and their files", "Three programs combine the chapter: a tile sheet, one card for each guest, and a search for folders of photos.", [
        ("Practice Programs", "Three programs: Tile Maker, seating cards and a photo-folder finder."),
        ("Tile Maker", "make_tile(filename, across, down) pastes one picture across and down."),
        ("zophie.png", "The cat picture that the book uses for cropping and tiling."),
        ("Creating Custom Seating Cards", "One 4 by 5 inch card for each guest, with the name drawn on it."),
        ("guests.txt", "A text file with one guest name on each line."),
        ("Identifying Photo Folders on the Hard Drive", "Walk the folders; a folder is photos when most of its pictures are large."),
    ]),
]

# ---- the stories (5N1K, told as natural prose); the picture of each is a record of story_images_v1_0_0.json in the chapter's assets folder
STORIES = {
    "kirsch": dict(
        title="Story: The first scanned photograph was 176 by 176 pixels of a baby", img="image_kirsch.jpg",
        prose=["In 1957 Russell A. Kirsch, an engineer at the National Bureau of Standards, led the group that built a drum scanner for the computer SEAC.",
               "One of the first pictures it scanned showed his three-month-old son, Walden. It was 176 by 176 pixels, 30976 in all, and each pixel was one bit: black or white.",
               "A picture you open in Pillow is still a grid of numbers; Image.new('1', (176, 176)) makes one of the same size."],
        linktext="Russell A. Kirsch (Wikipedia)", link="https://en.wikipedia.org/wiki/Russell_A._Kirsch"),
    "alpha": dict(
        title="Story: The alpha channel came from a graphics lab in the late 1970s", img="image_alpha.jpg",
        prose=["In the late 1970s Alvy Ray Smith and Ed Catmull, at the Computer Graphics Lab of the New York Institute of Technology, introduced the alpha channel.",
               "A paper of 1984 by Thomas Porter and Tom Duff introduced premultiplied alpha.",
               "The fourth number of an RGBA tuple is that alpha: 0 for clear, 255 for solid. A mask in paste() uses it."],
        linktext="Alpha compositing (Wikipedia)", link="https://en.wikipedia.org/wiki/Alpha_compositing"),
    "png": dict(
        title="Story: A patent announcement on 28 December 1994 led to PNG", img="image_png.jpg",
        prose=["On 28 December 1994 it was announced that programs which wrote GIF files would owe royalties to Unisys, which held the patent on the LZW compression.",
               "On 4 January 1995 Thomas Boutell posted a plan for a free alternative on the Usenet group comp.graphics.",
               "The result, PNG, was first released on 1 October 1996. It keeps every pixel and the alpha channel, which the logo project needs."],
        linktext="PNG (Wikipedia)", link="https://en.wikipedia.org/wiki/PNG"),
    "jpeg": dict(
        title="Story: JPEG stands on a transform proposed twenty years earlier", img="image_jpeg.jpg",
        prose=["In 1972 Nasir Ahmed proposed the discrete cosine transform as a way to compress images.",
               "The Joint Photographic Experts Group built its standard on it; the standard of 1992 is ISO/IEC 10918, also called ITU-T T.81.",
               "JPEG throws detail away to make a small file, and it has no alpha channel; Pillow refuses to save an RGBA picture as JPEG."],
        linktext="JPEG (Wikipedia)", link="https://en.wikipedia.org/wiki/JPEG"),
    "pil": dict(
        title="Story: PIL stopped in 2011 and Pillow carried it on", img="image_pil.jpg",
        prose=["Fredrik Lundh wrote the Python Imaging Library, released in 1995 and developed at Secret Labs AB.",
               "Development of the original library stopped in 2011. The Pillow project forked it and added support for Python 3.",
               "Chapter 21 still writes from PIL import Image, because Pillow kept the name of the package; only the name you install differs."],
        linktext="Python Imaging Library (Wikipedia)", link="https://en.wikipedia.org/wiki/Python_Imaging_Library"),
    "matplotlib": dict(
        title="Story: Matplotlib was named for MATLAB, plot and library", img="image_matplotlib.jpg",
        prose=["John D. Hunter wrote Matplotlib and released it in 2003, as a plotting library for Python and its numerical extension NumPy.",
               "Its name joins three words: MATLAB, plot and library. The pyplot module of chapter 21 keeps one current figure that each call draws on.",
               "That is why plt.plot() needs no figure object: it adds a line to the current axes."],
        linktext="Matplotlib (Wikipedia)", link="https://en.wikipedia.org/wiki/Matplotlib"),
}

# ---- the native comparison table (Table 21-1): the answers of ImageColor itself, taken at the build
_NAMES = ["red", "lime", "blue", "yellow", "CornflowerBlue", "tan", "orange"]
COMPARES = {
    "colours": dict(
        title="Table 21-1: colour names and the numbers behind them", sub="What ImageColor.getcolor(name, 'RGBA') answers for seven names",
        colw=[2.2, 2.2, 1.6, 3.0], rowh=0.42, fs=11,
        rows=[["Name", "Red, green, blue, alpha", "Hex code", "Mostly"]] + [
            [n, str(ImageColor.getcolor(n, "RGBA")), "#%02x%02x%02x" % ImageColor.getcolor(n, "RGB"),
             {"red": "red", "lime": "green", "blue": "blue", "yellow": "red and green", "CornflowerBlue": "blue", "tan": "red", "orange": "red and green"}[n]] for n in _NAMES],
        takeaway="Every name is four numbers; 255 for alpha means solid."),
}

# ---- one take-away line for every code slide
TAKEAWAY = {
    "colours": "A colour name is four numbers from 0 to 255.",
    "boxtuple": "A box is (left, top, right, bottom); right and bottom are not inside.",
    "crop": "crop() returns a new Image; the original is untouched.",
    "paste": "paste() changes the target and returns None: copy first.",
    "mask": "The third argument of paste() is the mask: alpha blends, no mask replaces.",
    "transform": "A turn keeps the canvas unless expand=True; the corners come out black.",
    "save": "PNG keeps every pixel; JPEG is smaller and has no alpha.",
    "logo": "One loop, two decisions, and a paste with the logo as its own mask.",
    "draw": "A rectangle includes its end points: 41 by 31, not 40 by 30.",
    "text": "Measure with textbbox() before you draw with text().",
    "clipboard": "A clipboard holds one picture at a time; the real one needs a display.",
    "line": "Every pyplot call draws on the current axes; save before you show.",
    "barpie": "bar() returns the bars, pie() the wedges; figure() starts a new graph.",
    "tile": "Two loops and one multiplication place every tile.",
    "seating": "Centre a name with the width that textbbox() measures.",
}

SUMMARY_ANALOGY = "Four claims: a grid of numbers, a new Image each time, a mask for alpha, a current figure."
SUMMARY_POINTS = [
    "A picture is a grid of pixels, and a box tuple names a region of it.",
    "crop(), resize() and rotate() return new pictures; paste() changes its target.",
    "A mask lets alpha blend a paste; JPEG has no alpha and PNG keeps it.",
    "pyplot draws on one current figure; savefig() comes before show().",
]
SUMMARY_TAKEAWAY = "Two questions of slide 3: change pictures without damage, and draw with no window."

PRACTICE_SUB = "Use the slide of the part named in each question"
PRACTICE_ANALOGY = "Each practice question has a short answer; run the code on the chapter page to check it."
PRACTICE = [
    "What size is the part of a picture cut out with the box (3, 1, 9, 6)? Use the box tuple slide.",
    "Why must you copy() a picture before you paste() onto it, and what does paste() return?",
    "What does the third argument of paste() do, and which value of it does the logo project use?",
    "Why does saving an RGBA picture as JPEG fail, and how would you avoid the failure?",
    "What must a program do before it calls plt.savefig() or plt.show(), and why does savefig() come first?",
]
PRACTICE_TAKEAWAY = "Run the examples on the chapter page to check each answer."

RESOURCES_SUB = "The chapter, the documentation, and the pages behind the stories"
RESOURCES_TAKEAWAY = "Every link was opened on 2026-11-26 and answered."
RESOURCES_ROWS = 8
RESOURCES = [
    ("Russell A. Kirsch (Wikipedia)", "https://en.wikipedia.org/wiki/Russell_A._Kirsch", "en.wikipedia.org"),
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 21", "https://automatetheboringstuff.com/3e/chapter21.html", "automatetheboringstuff.com"),
    ("Pillow documentation: the Image module", "https://pillow.readthedocs.io/en/stable/reference/Image.html", "pillow.readthedocs.io"),
    ("Pillow documentation: the ImageDraw module", "https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html", "pillow.readthedocs.io"),
    ("Pillow documentation: the ImageFont module", "https://pillow.readthedocs.io/en/stable/reference/ImageFont.html", "pillow.readthedocs.io"),
    ("Pillow documentation: the ImageColor module", "https://pillow.readthedocs.io/en/stable/reference/ImageColor.html", "pillow.readthedocs.io"),
    ("Matplotlib: pyplot tutorial", "https://matplotlib.org/stable/tutorials/pyplot.html", "matplotlib.org"),
    ("Matplotlib: the pyplot API", "https://matplotlib.org/stable/api/pyplot_summary.html", "matplotlib.org"),
    ("Alpha compositing (Wikipedia)", "https://en.wikipedia.org/wiki/Alpha_compositing", "en.wikipedia.org"),
    ("PNG (Wikipedia)", "https://en.wikipedia.org/wiki/PNG", "en.wikipedia.org"),
    ("JPEG (Wikipedia)", "https://en.wikipedia.org/wiki/JPEG", "en.wikipedia.org"),
    ("Python Imaging Library (Wikipedia)", "https://en.wikipedia.org/wiki/Python_Imaging_Library", "en.wikipedia.org"),
    ("Matplotlib (Wikipedia)", "https://en.wikipedia.org/wiki/Matplotlib", "en.wikipedia.org"),
    ("Pillow on PyPI", "https://pypi.org/pypi/pillow/json", "pypi.org"),
    ("Matplotlib on PyPI", "https://pypi.org/pypi/matplotlib/json", "pypi.org"),
]
