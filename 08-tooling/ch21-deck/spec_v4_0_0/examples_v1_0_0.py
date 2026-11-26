"""Chapter 21 deck examples, version 1.0.0 (SEN0414, Lineage14): the 15 code examples of the chapter 21 lecture deck (Graphs and Images), in slide order = page-tab order.
Every example is self-contained and runs offline: pictures are drawn by the program itself (no file of the book's zip is needed), nothing reads a keyboard or opens a window, no lambda, no prompt.
`groups` are the code boxes of a slide with the explanation beside each; every box parses on its own. The deck builder runs the code and takes every printed result from the run."""
__version__ = "1.0.0"

EXAMPLES = [
    # ------------------------------------------------------------ part 1: pixels, colours and boxes
    dict(id="colours", name="Colours and RGBA values", title="Colours, names and RGBA values (Table 21-1)", part=1, visual="colours",
         concepts=["Computer Image Fundamentals", "Colors and RGBA Values", "Table 21-1: Standard Color Names and Their RGBA Values", "PIL.ImageColor"],
         groups=[
             (["from PIL import Image, ImageColor", "names = ['red', 'lime', 'blue', 'CornflowerBlue', '#CCDDEE']"],
              "ImageColor turns a name or a hex code into numbers."),
             (["for n in names:", "    print(n, ImageColor.getcolor(n, 'RGBA'))"],
              "Four integers from 0 to 255: red, green, blue and alpha."),
             (["print(Image.new('1', (176, 176)).size, 176 * 176, 'pixels')"],
              "A picture is a grid of numbers: 176 by 176 pixels is 30976 values."),
         ]),
    dict(id="boxtuple", name="Coordinates and box tuples", title="Coordinates and box tuples", part=1, visual="boxtuple",
         concepts=["Coordinates and Box Tuples", "Figure 21-1: the x- and y-coordinates of a 28x27 image", "Figure 21-2: the area represented by the box tuple (3, 1, 9, 6)", "Working with the Image Data Type"],
         groups=[
             (["from PIL import Image", "im = Image.new('RGB', (28, 27), 'white')", "print(im.size, im.width, im.height)"],
              "The origin (0, 0) is the top left; x grows to the right, y downward."),
             (["left, top, right, bottom = 3, 1, 9, 6", "print(right - left, 'wide,', bottom - top, 'high')"],
              "A box tuple keeps left and top, and stops short of right and bottom."),
             (["part = im.crop((left, top, right, bottom))", "print(part.size, im.size)"],
              "The box (3, 1, 9, 6) holds 6 by 5 pixels; the picture is unchanged."),
         ]),
    dict(id="crop", name="Cropping a picture", title="Cropping a picture with crop()", part=1, visual="crop",
         concepts=["Manipulating Images with Pillow", "Cropping Images"],
         groups=[
             (["from PIL import Image, ImageDraw", "cat = Image.new('RGB', (200, 140), 'tan')", "ImageDraw.Draw(cat).ellipse((60, 30, 140, 110), fill='black')"],
              "A picture made by the program: a dark face on a tan field."),
             (["face = cat.crop((60, 30, 141, 111))", "print(cat.size, face.size)", "print(cat.getpixel((100, 70)), face.getpixel((40, 40)))"],
              "crop() returns a new Image; the original keeps its size."),
         ]),
    dict(id="paste", name="Pasting and tiling", title="Pasting and tiling with paste()", part=1, visual="paste",
         concepts=["Pasting Images onto Other Images", "Figure 21-6: nested for loops used with paste() duplicate the cat face"],
         groups=[
             (["from PIL import Image", "face = Image.new('RGB', (40, 40), 'orange')", "sheet = Image.new('RGB', (200, 120), 'white')"],
              "A small face and a larger blank sheet."),
             (["count = 0", "for left in range(0, sheet.width, face.width):", "    for top in range(0, sheet.height, face.height):",
               "        sheet.paste(face, (left, top))", "        count += 1"],
              "paste() changes the sheet it is called on; two loops tile it."),
             (["print(count, 'pastes')", "print(sheet.getpixel((199, 119)), sheet.paste(face, (0, 0)))"],
              "5 columns and 3 rows make 15 pastes; paste() itself returns None."),
         ]),
    # ------------------------------------------------------------ part 2: changing pictures
    dict(id="mask", name="Pasting with a mask and the alpha channel", title="Masks and the alpha channel", part=2, visual="mask",
         concepts=["Colors and RGBA Values", "Figure 21-13: the logo with and without the third argument"],
         groups=[
             (["from PIL import Image", "base = Image.new('RGBA', (4, 4), 'red')", "top = Image.new('RGBA', (2, 2), (0, 0, 255, 128))"],
              "A red base, and a blue square that is half see-through (alpha 128)."),
             (["plain, masked = base.copy(), base.copy()", "plain.paste(top, (1, 1))", "masked.paste(top, (1, 1), top)"],
              "The third argument of paste() is the mask: here the square's own alpha."),
             (["print(plain.getpixel((1, 1)))", "print(masked.getpixel((1, 1)))"],
              "Without the mask the pixel is replaced; with it, red and blue blend."),
         ]),
    dict(id="transform", layout="left", name="Resize, rotate, flip and set a pixel", title="Resize, rotate, flip and set a pixel", part=2, visual="transform",
         concepts=["Resizing Images", "Rotating and Flipping Images", "Changing Individual Pixels", "Figure 21-8: the image rotated six degrees normally and with expand=True"],
         groups=[
             (["from PIL import Image", "im = Image.new('RGB', (120, 80), 'white')", "big = im.rotate(90, expand=True)", "print(im.resize((60, 40)).size, im.rotate(90).size, big.size)"],
              "resize() takes the new size; rotate() keeps the canvas unless expand=True."),
             (["print(im.rotate(6).size, im.rotate(6, expand=True).size)", "print(im.transpose(Image.Transpose.FLIP_LEFT_RIGHT).size)"],
              "A turn of 6 degrees: the canvas grows to fit only with expand=True."),
             (["im.putpixel((0, 0), (255, 0, 0))", "print(im.getpixel((0, 0)), im.getpixel((1, 0)))", "print(im.rotate(6).getpixel((0, 0)))"],
              "One pixel changed; the corner left empty by a turn is black."),
         ]),
    dict(id="save", layout="left", name="Saving: PNG, JPEG and pixel density", title="Saving: PNG, JPEG and file size", part=2, visual="save",
         concepts=["Working with the Image Data Type", "PIL.Image"],
         groups=[
             (["import io", "from PIL import Image, ImageDraw", "im = Image.new('RGB', (200, 200), 'white')", "ImageDraw.Draw(im).ellipse((20, 20, 180, 180), fill='green')"],
              "Flat colour, saved into memory and not into a file."),
             (["for kind in ('PNG', 'JPEG'):", "    buf = io.BytesIO()", "    im.save(buf, kind)", "    print(kind, len(buf.getvalue()))"],
              "The same picture in two formats: the byte counts differ."),
             (["try:", "    im.convert('RGBA').save(io.BytesIO(), 'JPEG')", "except OSError as e:", "    print(e)"],
              "JPEG has no alpha: convert an RGBA picture first."),
         ]),
    # ------------------------------------------------------------ part 3: Project 16 and drawing
    dict(id="logo", layout="left", name="Project 16: add a logo", setup=["import os, tempfile", "from PIL import Image", "os.chdir(tempfile.mkdtemp())", "for w in [300, 80, 500]:", "    Image.new('RGB', (w, w // 2), 'skyblue').save(f'{w}.png')"], title="Project 16: a logo on every picture", part=3, visual="logo",
         concepts=["Project 16: Add a Logo", "Step 1: Open the Logo Image", "Step 2: Loop Over All Files", "Step 3: Resize the Images", "Step 4: Add the Logo and Save the Changes",
                   "Figure 21-12: the left and top coordinates of the logo", "resizeAndAddLogo.py", "Ideas for Similar Programs", "os", "catlogo.png"],
         groups=[
             (["import os", "from PIL import Image", "logo = Image.new('RGBA', (40, 30), (255, 0, 0, 200))"],
              "Step 1: the logo; three pictures wait in the folder."),
             (["def stamp(name):", "    im = Image.open(name)", "    if im.width < 4 * logo.width:", "        return None", "    r = min(1, 300 / max(im.size))",
               "    im = im.resize((round(im.width * r), round(im.height * r)))", "    x, y = im.width - logo.width, im.height - logo.height", "    im.paste(logo, (x, y), logo)", "    return im.size"],
              "Steps 2-4: skip small ones, shrink, paste the logo."),
             (["for name in sorted(os.listdir('.')):", "    print(name, stamp(name))"],
              "The loop over the folder: each result is the new size."),
         ]),
    dict(id="draw", name="Drawing shapes on a picture", title="Drawing shapes on a picture", part=3, visual="draw",
         concepts=["Drawing on Images", "Shapes", "Points", "Lines", "Rectangles", "Ellipses", "Polygons", "A Drawing Example", "Figure 21-14: the resulting drawing.png image", "PIL.ImageDraw"],
         groups=[
             (["from PIL import Image, ImageDraw", "im = Image.new('RGBA', (200, 200), 'white')", "draw = ImageDraw.Draw(im)"],
              "An ImageDraw object draws on the picture it was made from."),
             (["draw.point([(5, 5), (6, 6)], fill='red')", "draw.line([(0, 0), (199, 199)], fill='black', width=3)", "draw.rectangle((20, 30, 60, 60), fill='blue')"],
              "A point, a line and a rectangle; the rectangle includes its end points."),
             (["draw.ellipse((100, 50, 180, 130), outline='green')", "draw.polygon([(30, 150), (90, 190), (20, 190)], fill='purple')",
               "colours = {c: n for n, c in im.getcolors()}", "print(colours[(0, 0, 255, 255)], 'blue pixels')"],
              "41 by 31 is 1271 blue pixels, not 40 by 30."),
         ]),
    dict(id="text", name="Drawing text", title="Drawing text and choosing fonts", part=3, visual="text",
         concepts=["Text", "PIL.ImageFont"],
         groups=[
             (["from PIL import Image, ImageDraw, ImageFont", "font = ImageFont.load_default(size=24)", "im = Image.new('RGB', (200, 60), 'white')", "draw = ImageDraw.Draw(im)"],
              "A font of the library itself; arial.ttf is not on every system."),
             (["box = draw.textbbox((10, 10), 'Howdy!', font=font)", "print(box)", "print(box[2] - box[0], 'wide,', box[3] - box[1], 'high')"],
              "textbbox() measures the text before it is drawn: left, top, right, bottom."),
             (["draw.text((10, 10), 'Howdy!', fill='black', font=font)", "print(len(im.getcolors()) > 1)"],
              "text() draws it; more than one colour is now in the picture."),
         ]),
    # ------------------------------------------------------------ part 4: the clipboard and graphs
    dict(id="clipboard", name="Copying and pasting images to the clipboard", title="The clipboard holds a picture", part=4, visual="clipboard",
         concepts=["Copying and Pasting Images to the Clipboard", "pyperclipimg"],
         groups=[
             (["from PIL import Image", "class Clipboard:", "    held = None", "    def copy(self, im):", "        self.held = im.copy()", "    def paste(self):", "        return self.held"],
              "EMULATED: a small class stands in for pyperclipimg, which needs a display."),
             (["clip = Clipboard()", "clip.copy(Image.new('RGB', (30, 20), 'orange'))", "got = clip.paste()", "print(got.size, got.getpixel((0, 0)))"],
              "copy() keeps a picture; paste() hands it back, as the real module does."),
         ]),
    dict(id="line", layout="left", name="Line graphs and scatter plots", title="Line graphs and scatter plots with pyplot", part=4, visual="line",
         concepts=["Creating Graphs with Matplotlib", "Line Graphs and Scatter Plots", "matplotlib.pyplot", "Additional Components", "Figure 21-20: the example line graph with additional components"],
         groups=[
             (["import io", "import matplotlib", "matplotlib.use('Agg')", "import matplotlib.pyplot as plt"],
              "The Agg backend draws into memory, with no window."),
             (["lines = plt.plot([1, 2, 3, 4], [1, 4, 9, 16], label='squares')", "dots = plt.scatter([1, 2, 3, 4], [2, 3, 5, 8])",
               "plt.title('Growth'); plt.xlabel('step')", "plt.ylabel('size'); plt.legend()"],
              "plot() and scatter() draw on the current axes; labels and a legend are calls too."),
             (["buf = io.BytesIO()", "plt.savefig(buf, dpi=100, format='png')", "title, size = plt.gca().get_title(), len(buf.getvalue())", "print(len(lines), type(dots).__name__, title, size > 1000)"],
              "Save before you show; savefig() writes the figure at 100 dpi."),
         ]),
    dict(id="barpie", name="Bar graphs and pie charts", title="Bar graphs and pie charts", part=4, visual="barpie",
         concepts=["Bar Graphs and Pie Charts"],
         groups=[
             (["import matplotlib", "matplotlib.use('Agg')", "import matplotlib.pyplot as plt", "names, votes = ['A', 'B', 'C'], [5, 3, 2]"],
              "Three names and their votes."),
             (["bars = plt.bar(names, votes)", "print([round(b.get_height()) for b in bars])", "plt.figure()"],
              "bar() returns one bar for each value; figure() starts a fresh graph."),
             (["wedges, labels = plt.pie(votes, labels=names)", "print(len(wedges), round(wedges[0].theta2 - wedges[0].theta1))"],
              "pie() returns the wedges; the share of A is 5 in 10, which is 180 degrees."),
         ]),
    # ------------------------------------------------------------ part 5: practice programs
    dict(id="tile", name="Tile Maker", title="Practice program: Tile Maker", part=5, visual="tile",
         concepts=["Practice Programs", "Tile Maker", "zophie.png"],
         groups=[
             (["from PIL import Image, ImageDraw", "def make_tile(face, across, down):", "    w, h = face.size", "    sheet = Image.new('RGB', (w * across, h * down))",
               "    for x in range(across):", "        for y in range(down):", "            sheet.paste(face, (x * w, y * h))", "    return sheet"],
              "A function: a blank sheet as large as the tiles need, and two loops that paste the face at every position."),
             (["face = Image.new('RGB', (50, 40), 'tan')", "ImageDraw.Draw(face).ellipse((10, 5, 40, 35), fill='black')", "sheet = make_tile(face, 4, 3)",
               "print(sheet.size, sheet.getpixel((25, 20)), sheet.getpixel((75, 60)))"],
              "4 across and 3 down make 200 by 120; the middle of each tile agrees."),
         ]),
    dict(id="seating", layout="left", name="Creating custom seating cards", title="Practice program: seating cards, and finding photo folders", part=5, visual="seating",
         concepts=["Creating Custom Seating Cards", "guests.txt", "Identifying Photo Folders on the Hard Drive"],
         groups=[
             (["from PIL import Image, ImageDraw, ImageFont", "guests = ['Ada Lovelace', 'Alan Turing', 'Grace Hopper']", "font = ImageFont.load_default(size=28)"],
              "The names come from guests.txt; here they are typed."),
             (["cards = []", "for name in guests:", "    card = Image.new('RGB', (288, 360), 'white')", "    draw = ImageDraw.Draw(card)", "    box = draw.textbbox((0, 0), name, font=font)", "    x = (288 - (box[2] - box[0])) // 2",
               "    draw.text((x, 160), name, fill='black', font=font)", "    cards.append(card)"],
              "One card of 288 by 360 for each name, name centred."),
             (["card, white = cards[0], (255, 255, 255)", "print(len(cards), card.size)", "print(card.getpixel((0, 0)), card.getpixel((144, 175)) != white)"],
              "A white corner; the middle holds ink."),
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
