"""Chapter 11 deck content, version 3.0.0: the words of the deck for the generic builder (analogies, parts, plan, stories, tables, take-aways, resources). The analogies, take-aways and
links are those of deck_content_v2_0_0.py; the stories are the same four stories with the same facts, told as prose in paragraphs of at most 30 words (ruling 1 and the story ruling of 2026-11-14),
and the plan, parts and tables of the old builder moved here. The notes are notes_v3_0_0.py."""
__version__ = "3.0.0"

PARTS = {
    1: ("Part 1: Copying and moving", "The shutil module relocates files and whole folders", [
        ("shutil.copy", "Copies one file; the original stays where it is."),
        ("shutil.copytree", "Copies a folder with everything inside it."),
        ("shutil.move", "Relocates or renames; it can overwrite a file."),
        ("Time stamp", "copy2 also keeps the modification time of the file."),
    ]),
    2: ("Part 2: Deleting, and staying safe", "Permanent deletion has no undo, so print before you delete", [
        ("unlink", "Deletes one file for good, with no recycle bin."),
        ("rmtree", "Removes a whole folder tree in one call."),
        ("Dry run", "Print what would go before anything is deleted."),
        ("send2trash", "A third-party module that uses the recycle bin."),
    ]),
    3: ("Part 3: Folders and trees", "List one folder, then walk a whole tree", [
        ("listdir and glob", "Names of one folder, filtered by a pattern."),
        ("walk", "Gives folder, subfolders and files at every step."),
        ("Folder sizes", "Add up bytes per folder while walking."),
        ("mkdir", "Builds a folder, or a whole chain of folders."),
    ]),
    4: ("Part 4: ZIP archives", "Many files in one parcel, and back again", [
        ("ZipFile", "Opens an archive to write, add or read."),
        ("Compression", "ZIP_DEFLATED shrinks repeated text a great deal."),
        ("extract", "Unpacks one member or all of them."),
        ("make_archive", "Packs a whole folder in a single call."),
    ]),
    5: ("Part 5: Programs that organize files", "Four programs that use everything so far", [
        ("backupToZip", "Backs a folder up into a numbered ZIP."),
        ("Selective copy", "Copies only the files of one extension."),
        ("Big files", "Finds the files above a size limit."),
        ("Date renaming", "Swaps day and month inside file names."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("code", "copy"), ("code", "copytree"), ("code", "copy2"), ("code", "move"),
        ("divider", 2), ("analogy", "A2"), ("code", "unlink"), ("code", "rmtree"), ("code", "dryrun"), ("compare", "send2trash"), ("story", "kare"),
        ("divider", 3), ("analogy", "A3"), ("code", "listing"), ("code", "walk"), ("code", "sizes"), ("code", "mkdir"), ("story", "multics"),
        ("divider", 4), ("analogy", "A4"), ("code", "zipwrite"), ("code", "zipmodes"), ("code", "extract"), ("code", "archives"), ("story", "katz"), ("story", "zlib"),
        ("divider", 5), ("analogy", "A5"), ("code", "backup"), ("code", "selective"), ("code", "large"), ("code", "dates"),
        ("current",), ("summary",), ("practice",), ("resources",)]

ROUTE_RUNS = {1: "copy, copytree, copy2, move", 2: "unlink, rmdir, rmtree, a dry run", 3: "listdir, glob, walk, folder sizes, mkdir",
              4: "write, append, extract, make_archive", 5: "backup, selective copy, big files, date renaming"}
ROUTE_TAIL = ("Changes, summary, practice, links", "what current Python adds")
QUESTIONS = [("1", "Which operations change the disk for good, and how can a program show what it will do first?",
              "Answer on slides %d and %d: unlink and rmtree, then the dry run.", [("code", "unlink"), ("code", "dryrun")]),
             ("2", "How does a program visit every file of a folder tree and pack the result into one archive?",
              "Answer on slides %d and %d: os.walk, then the backup project.", [("code", "walk"), ("code", "backup")])]
QUESTIONS_TAKEAWAY = "Know what a call destroys before you run it."

ANALOGIES = [('A1',
  'Everyday pictures: copying and moving',
  'A copy is a photocopy; a move is carrying the original to another desk.',
  [('The shutil Module', 'A removals firm: it carries, copies and packs whole files and folders for you.'),
   ('Copying and moving', 'Photocopying a page, or lifting the page and putting it in another tray.'),
   ('shutil.copy', 'A photocopier: the original stays, and you choose the name of the copy.'),
   ('shutil.copytree', 'Photocopying a whole ring binder, every divider and page inside.'),
   ('shutil.move', 'Moving a page to another tray; if the new tray holds the same page, it is replaced.')]),
 ('A2',
  'Everyday pictures: deleting safely',
  'Permanent deletion is a paper shredder; the recycle bin is the waste-paper basket beside it.',
  [('Safe deletion', 'Reading the shredding list aloud before anything goes into the machine.'),
   ('unlink', 'A shredder: the page is gone, and nobody can fetch it back.'),
   ('send2trash', 'The waste-paper basket: the page can still be pulled out until the bin is emptied.'),
   ('rmtree', 'Demolishing a whole room with everything in it, not just emptying one shelf.'),
   ('Dry run', 'A dress rehearsal: the actors say their lines, and nothing on stage is damaged.')]),
 ('A3',
  'Everyday pictures: folder trees',
  'A folder tree is a building: floors hold rooms, and rooms hold cupboards.',
  [('Walking a Directory Tree', "A caretaker's round through every floor of the building."),
   ('Walking a folder tree', 'Opening each door, looking in each cupboard, then going one level down.'),
   ('walk', "The caretaker's checklist: for each room, its inner rooms and its cupboards' contents."),
   ('mkdir', 'Building a new empty room; parents=True builds the corridor leading to it as well.'),
   ('listdir and glob', "Reading the names on one floor's door plates, or only the plates that match a pattern.")]),
 ('A4',
  'Everyday pictures: ZIP archives',
  'A ZIP file is a vacuum-packed suitcase: many things, one small parcel, and they come out again.',
  [('Compressing Files with the zipfile Module', 'Vacuum-packing clothes: the same clothes, a much smaller bag.'),
   ('Archives', 'A single suitcase for a whole wardrobe.'),
   ('zipfile.ZipFile', 'The suitcase itself: open it to pack, to add one more item or to look inside.'),
   ('extract', 'Taking one shirt out, or emptying the whole case onto the bed.')]),
 ('A5',
  'Everyday pictures: programs that organize files',
  'A practice program is a driving lesson on an empty car park: the real skill, no real risk.',
  [('Practice Programs', 'Driving lessons on an empty car park: every move is real, no damage is possible.'),
   ('backupToZip', 'A nightly photocopy of the whole filing cabinet, numbered so no old copy is lost.'),
   ('Selective copy', 'A librarian who copies only the blue-covered books from every shelf.'),
   ('Date renaming', 'Relabelling every folder when the office switches from the American to the European calendar.')])]

STORIES = {
    "kare": dict(title="Story: the recycle bin is a 1983 drawing", img="photo_kare.jpg",
                 prose=["In 1983 Susan Kare, a graphic designer hired by Apple, drew the trash can icon, working with software architect Andy Hertzfeld.",
                        "It was one of the small pictures of the first Macintosh, which Apple Computer in California shipped in 1984.",
                        "Pictures made commands friendly for people who had never used a computer, and a bin promised that a deleted page could still be pulled out.",
                        "send2trash moves a file into that same bin instead of deleting it, so the move can still be undone."],
                 link="https://www.smithsonianmag.com/innovation/how-susan-kare-designed-user-friendly-icons-for-first-macintosh-180973286/", linktext="Susan Kare's icons, Smithsonian Magazine"),
    "multics": dict(title="Story: the folder tree is a 1965 Multics design", img="photo_neumann.jpg",
                    prose=["In 1965, at the Fall Joint Computer Conference, R. C. Daley of MIT's Project MAC and Peter G. Neumann of Bell Labs presented a paper.",
                           "Its title was 'A General Purpose File System for Secondary Storage': folders holding folders holding files, for Multics, the shared system of MIT, Bell Labs and General Electric.",
                           "Many users had to share one disk and manage their own parts of it, and a tree gave each of them a place.",
                           "Unix kept the same tree, and os.walk descends it folder by folder today."],
                    link="https://multicians.org/history.html", linktext="Multics history, multicians.org"),
    "katz": dict(title="Story: the ZIP format was given away on 14 February 1989", img="photo_katz.jpg",
                 prose=["On 14 February 1989 Phil Katz, a programmer at PKWARE in Glendale, Wisconsin, and Gary Conway of Infinity Design Concepts put the ZIP format in the public domain.",
                        "They announced it in a joint press release. Katz had been sued over PKARC, his ARC-compatible archiver, so the two designed a new, open format.",
                        "Any program could read or write it for free, which is why zipfile can open archives made by any tool.",
                        "Every zipfile.ZipFile call of this chapter reads and writes that same public-domain structure."],
                 link="https://en.wikipedia.org/wiki/ZIP_(file_format)", linktext="ZIP (file format), Wikipedia"),
    "zlib": dict(title="Story: the engine under ZIP_DEFLATED shipped on 1 May 1995", img="photo_adler.jpg",
                 prose=["On 1 May 1995 Jean-loup Gailly wrote the compression half and Mark Adler the decompression half of zlib 0.9, a free library for the DEFLATE method.",
                        "They wrote it over the internet, first for the libpng image library, and anyone could embed it in a program.",
                        "Programs needed compression that no company owned and no patent blocked.",
                        "zipfile hands the bytes to zlib whenever a write asks for compress_type=zipfile.ZIP_DEFLATED."],
                 link="https://en.wikipedia.org/wiki/Zlib", linktext="Zlib, Wikipedia"),
}

COMPARES = {"send2trash": dict(
    title="send2trash: the recycle bin", sub="A third-party helper; not in the standard library and not run on the chapter page",
    rows=[["", "os.unlink", "send2trash.send2trash"],
          ["Where the file goes", "nowhere, it is gone", "the recycle bin of the system"],
          ["Can you get it back?", "no", "yes, until the bin is emptied"],
          ["Where does it come from?", "the standard library", "pip install send2trash"],
          ["Run on the chapter page?", "yes", "no, it needs an installed module"]],
    colw=[2.6, 2.7, 3.7], rowh=0.5, fs=13, takeaway="When in doubt, send to the bin instead of deleting.")}

TAKEAWAY = {'archives': 'make_archive and unpack_archive: one call each way.',
 'backup': 'Walk, write, count: a numbered backup.',
 'copy': 'copy keeps the original and returns the new path.',
 'copy2': 'copy2 keeps the time stamp; copy does not.',
 'copytree': 'copytree needs a new name, or dirs_exist_ok=True.',
 'dates': 'A pattern plus move renames many files at once.',
 'dryrun': 'Print the list first; delete only when it is right.',
 'extract': 'extractall unpacks all; extract takes one.',
 'large': 'Walk, measure, keep what is above the limit.',
 'listing': 'listdir for names, glob for patterns, rglob for the whole tree.',
 'mkdir': 'parents=True builds the chain; exist_ok=True accepts it.',
 'move': 'move relocates and renames; it can overwrite.',
 'rmtree': 'rmtree removes the whole tree at once.',
 'selective': 'Walk, test the extension, copy.',
 'sizes': 'A walk can add up bytes per folder.',
 'unlink': 'unlink and rmdir cannot be undone.',
 'walk': 'os.walk gives folder, subfolders and files at every step.',
 'zipmodes': 'w starts, a adds, x refuses to overwrite.',
 'zipwrite': 'ZIP_DEFLATED really shrinks repeated text.'}

CURRENT_SUB = "Features newer than the book, from the Python documentation"
CURRENT = [["What the chapter uses", "Today", "Example"],
           ["os.walk visits a tree and gives three values", "Python 3.12 adds Path.walk(), the same three values from a Path object", "walk"],
           ["shutil.rmtree takes onerror to handle failures", "Python 3.12 adds onexc, which replaces onerror; onerror is deprecated", "rmtree"],
           ["A ZipFile is written with write and writestr", "Python 3.11 adds ZipFile.mkdir(), an empty folder entry in an archive", "zipmodes"],
           ["shutil.copy and shutil.move copy and move files", "Python 3.14 adds Path.copy() and Path.move(), with no shutil import", "copy"],
           ["glob matches the names of one folder or of a tree", "Python 3.13 adds recurse_symlinks to choose whether glob follows symbolic links", "listing"]]
CURRENT_TAKEAWAY = "Run what the book printed; then check what changed."
SUMMARY_ANALOGY = "A summary is a packing list: only what you really need goes into the bag."
SUMMARY_POINTS = ["copy keeps the original; move relocates and can overwrite.",
                  "unlink, rmdir and rmtree cannot be undone; print first.",
                  "os.walk gives folder, subfolders and files at every step.",
                  "ZipFile writes, appends and reads archives; extract unpacks them.",
                  "A short program can back up, copy by type or rename in bulk."]
SUMMARY_TAKEAWAY = "Know what a call destroys before you run it."
PRACTICE_SUB = "Predict first, then run it on the chapter page"
PRACTICE_ANALOGY = "Practice questions are finger scales for a pianist: short drills before the performance."
PRACTICE = ["What is the difference between shutil.copy and shutil.move for the original file?",
            "Why print the file names with a dry run before os.unlink is allowed to run?",
            "Which three values does every step of os.walk give you?",
            "Which ZipFile mode adds a file to an archive, and which refuses to overwrite one?"]
PRACTICE_TAKEAWAY = "Each answer fits in one line you can run."
RESOURCES_SUB = "Reading and watching, chosen for this chapter; every link is live"
RESOURCES_TAKEAWAY = "Pick one link and read it before the next class."
RESOURCES = [('Book: Automate the Boring Stuff, 3rd edition, chapter 11', 'https://automatetheboringstuff.com/3e/chapter11.html', 'automatetheboringstuff.com'),
 ('Python documentation: shutil, high-level file operations', 'https://docs.python.org/3/library/shutil.html', 'docs.python.org'),
 ('Python documentation: os.walk', 'https://docs.python.org/3/library/os.html#os.walk', 'docs.python.org'),
 ('Python documentation: zipfile', 'https://docs.python.org/3/library/zipfile.html', 'docs.python.org'),
 ('Python documentation: pathlib', 'https://docs.python.org/3/library/pathlib.html', 'docs.python.org'),
 ("What's new in Python 3.14", 'https://docs.python.org/3/whatsnew/3.14.html', 'docs.python.org'),
 ("What's new in Python 3.12", 'https://docs.python.org/3/whatsnew/3.12.html', 'docs.python.org'),
 ('send2trash on the Python Package Index', 'https://pypi.org/project/Send2Trash/', 'pypi.org'),
 ('ZIP file format specification (APPNOTE.TXT)', 'https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT', 'pkware.cachefly.net'),
 ('zlib home page', 'https://www.zlib.net/', 'zlib.net'),
 ('ZIP (file format) on Wikipedia', 'https://en.wikipedia.org/wiki/ZIP_(file_format)', 'wikipedia.org'),
 ('Multics history', 'https://multicians.org/history.html', 'multicians.org'),
 ("Susan Kare's Macintosh icons (Smithsonian)",
  'https://www.smithsonianmag.com/innovation/how-susan-kare-designed-user-friendly-icons-for-first-macintosh-180973286/',
  'smithsonianmag.com'),
 ('Video: working with ZIP files in Python (Corey Schafer)', 'https://www.youtube.com/watch?v=z0gguhEmWiY', 'youtube.com')]
