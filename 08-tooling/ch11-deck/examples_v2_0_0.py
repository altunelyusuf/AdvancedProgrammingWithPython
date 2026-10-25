"""Chapter 11 deck examples, version 2.0.0: the code examples of the chapter 11 lecture deck (Organizing Files).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language
explanation that stands beside it); the lines of all groups of an example, in order, are the example's code: that text is
what the deck shows after the '>>> ' prompt of each line (an indented line after the '... ' prompt), what the chapter-code
manifest lists and what the page runs. Every example is self-contained, works in its own fresh temporary folder (so no real
file is touched and no result carries a path of the machine) and uses only the Python standard library. Every code line is at
most 58 characters, so that the code stands beside its explanation at a readable size.
Nothing here carries a result; deck_build_v2_0_0.py runs the code and takes every printed result from the run."""
__version__ = "2.0.0"

HEAD = ["import os, shutil, tempfile", "from pathlib import Path", "os.chdir(tempfile.mkdtemp())"]
HEADZ = ["import os, shutil, tempfile, zipfile", "from pathlib import Path", "os.chdir(tempfile.mkdtemp())"]
NOTE = "A new temporary folder keeps your real files safe. "

EXAMPLES = [
    # ------------------------------------------------------------------ part 1
    dict(id="copy", name="shutil.copy: one file", title="shutil.copy: one file to a folder or a new name", part=1, visual="copy",
         concepts=["The shutil Module", "shutil.copy", "Copying and moving"],
         groups=[
             (HEAD + ["Path('a.txt').write_text('Hello')", "Path('box').mkdir()"],
              NOTE + "Then one small file and one empty folder to work with."),
             (["print(shutil.copy('a.txt', 'box'))", "print(shutil.copy('a.txt', 'box/b.txt'))", "print(sorted(os.listdir('box')))"],
              "A folder as target keeps the name; a file name as target renames the copy. copy returns the new path."),
         ]),
    dict(id="copytree", name="shutil.copytree: a whole folder", title="shutil.copytree: a folder with everything in it", part=1, visual="copytree",
         concepts=["shutil.copytree", "mkdir"],
         groups=[
             (HEAD + ["Path('box/inner').mkdir(parents=True)", "Path('box/y.txt').write_text('y')"],
              NOTE + "The folder box holds a subfolder and a file."),
             (["print(shutil.copytree('box', 'bak'))", "try:", "    shutil.copytree('box', 'bak')", "except FileExistsError:",
               "    print('second copy refused: the folder exists')",
               "print(shutil.copytree('box', 'bak', dirs_exist_ok=True))"],
              "copytree copies the whole tree to a new name. A second copy is refused; dirs_exist_ok=True merges into the existing folder."),
         ]),
    dict(id="copy2", name="copy2 keeps the time stamp", title="copy and copy2: what happens to the time stamp", part=1, visual="copy2",
         concepts=["shutil.copy"],
         groups=[
             (HEAD + ["Path('a.txt').write_text('Hello')", "Path('box').mkdir()", "os.utime('a.txt', (1000000000, 1000000000))"],
              NOTE + "os.utime sets the file's times to a fixed moment in 2001, so the run is repeatable."),
             (["shutil.copy2('a.txt', 'box/c.txt')", "shutil.copy('a.txt', 'box/d.txt')", "t = lambda n: int(Path(n).stat().st_mtime)",
               "print('copy2 keeps the time:', t('box/c.txt'))", "print('copy gives a new time:', t('box/d.txt') == t('a.txt'))"],
              "copy2 also copies the modification time. Plain copy stamps the copy with the moment of copying."),
         ]),
    dict(id="move", name="shutil.move: move and rename", title="shutil.move: move, rename, overwrite", part=1, visual="move",
         concepts=["shutil.move"],
         groups=[
             (HEAD + ["Path('spam').mkdir(); Path('spam2').mkdir()", "Path('spam/file1.txt').write_text('Hello')"],
              NOTE + "Two folders and one file in the first."),
             (["print(shutil.move('spam/file1.txt', 'spam2'))", "print(shutil.move('spam2/file1.txt', 'spam/new_name.txt'))"],
              "A folder as target moves the file into it. A new file name moves and renames in one step."),
             (["Path('spam2/f.txt').write_text('old')", "Path('spam/f.txt').write_text('new')", "shutil.move('spam/f.txt', 'spam2/f.txt')",
               "print(Path('spam2/f.txt').read_text(), Path('spam/f.txt').exists())"],
              "Moving onto an existing file name silently overwrites it. The source is gone afterwards."),
         ]),
    # ------------------------------------------------------------------ part 2
    dict(id="unlink", name="os.unlink and os.rmdir", title="os.unlink and os.rmdir: one file, one empty folder", part=2, visual="unlink",
         concepts=["unlink"],
         groups=[
             (HEAD + ["Path('a.txt').write_text('x')", "os.unlink('a.txt')", "print('a.txt exists:', Path('a.txt').exists())"],
              NOTE + "os.unlink deletes one file for good. There is no undo and no recycle bin."),
             (["Path('d').mkdir(); Path('d/f.txt').write_text('x')", "try:", "    os.rmdir('d')", "except OSError:",
               "    print('rmdir refused: the folder d is not empty')", "os.unlink('d/f.txt'); os.rmdir('d')", "print('d exists:', Path('d').exists())"],
              "os.rmdir deletes only an empty folder. Empty it first, then remove it."),
         ]),
    dict(id="rmtree", name="shutil.rmtree", title="shutil.rmtree: a folder and everything inside", part=2, visual="rmtree",
         concepts=["Safe deletion"],
         groups=[
             (HEAD + ["Path('spam/eggs').mkdir(parents=True)", "Path('spam/eggs/f.txt').write_text('x')",
                      "print(sorted(str(p) for p in Path('spam').rglob('*')))"],
              NOTE + "A folder with one subfolder and one file: two things that will disappear with it."),
             (["shutil.rmtree('spam')", "print('spam exists:', Path('spam').exists())", "shutil.rmtree('spam', ignore_errors=True)",
               "print('a missing folder is ignored')"],
              "rmtree removes the whole tree at once. ignore_errors=True stays quiet when there is nothing to remove."),
         ]),
    dict(id="dryrun", name="A dry run before deleting", title="Safe deletion: print first, delete later", part=2, visual="dryrun",
         concepts=["Safe deletion", "unlink"],
         groups=[
             (HEAD + ["for n in ('a.txt', 'b.txt', 'c.rxt'):", "    Path(n).write_text(n)"],
              NOTE + "Three small files; one has a strange extension."),
             (["names = sorted(p.name for p in Path('.').glob('*.rxt'))", "print('typo *.rxt would delete:', names)"],
              "A typo in the pattern matches the wrong file. Printing first shows the mistake while nothing is lost."),
             (["for p in sorted(Path('.').glob('*.txt')):", "    print('would delete', p)   # os.unlink(p)"],
              "Run it with the delete line commented out. Only when the printed list is right, remove the comment mark."),
         ]),
    # ------------------------------------------------------------------ part 3
    dict(id="listing", name="Listing one folder", title="Listing one folder: listdir, iterdir, glob", part=3, visual="listing",
         concepts=["Walking a Directory Tree"],
         groups=[
             (HEAD + ["Path('spam/eggs').mkdir(parents=True)", "Path('spam/b.pdf').write_text('x')", "Path('spam/file1.txt').write_text('x')",
                      "Path('spam/eggs/f2.txt').write_text('x')"],
              NOTE + "spam holds a folder, a PDF and a text file; the folder holds one more text file."),
             (["print(sorted(os.listdir('spam')))", "print(sorted((p.name, p.is_dir())", "             for p in Path('spam').iterdir()))",
               "print(sorted(p.name for p in Path('spam').glob('*.txt')))", "print(sorted(p.name for p in Path('spam').rglob('*.txt')))"],
              "listdir gives names; iterdir gives Path objects that know if they are folders. glob stays in one folder; rglob goes down into all subfolders."),
         ]),
    dict(id="walk", name="os.walk visits every folder", title="os.walk: the folder, its subfolders, its files", part=3, visual="walk",
         concepts=["walk", "Walking a folder tree"],
         groups=[
             (HEAD + ["Path('spam/eggs/bacon').mkdir(parents=True)", "Path('spam/eggs2').mkdir()", "Path('spam/file1.txt').write_text('x')",
                      "Path('spam/eggs/file2.txt').write_text('x')"],
              NOTE + "Four folders and two files. The walk starts at spam."),
             (["for folder, subs, files in os.walk('spam'):", "    subs.sort()", "    print(folder, subs, sorted(files))"],
              "Each step gives the folder, its subfolders and its files. Sorting subs fixes the order of the visit."),
             (["last = [f for f, s, fl in os.walk('spam', topdown=False)][-1]", "print('bottom-up ends at:', last)"],
              "With topdown=False the subfolders come first and the start folder comes last."),
         ]),
    dict(id="sizes", name="Folder sizes with os.walk", title="Counting bytes per folder while walking", part=3, visual="sizes",
         concepts=["walk"],
         groups=[
             (HEAD + ["Path('spam/eggs').mkdir(parents=True)", "Path('spam/a.txt').write_text('x' * 300)",
                      "Path('spam/eggs/b.txt').write_text('x' * 120)", "Path('spam/eggs/c.txt').write_text('x' * 80)"],
              NOTE + "Three files of 300, 120 and 80 bytes in two folders."),
             (["sizes = {}", "for folder, subs, files in os.walk('spam'):", "    sizes[folder] = sum(os.path.getsize(Path(folder, f))",
               "                        for f in files)", "print(dict(sorted(sizes.items())))", "print('total:', sum(sizes.values()))"],
              "For every folder the walk hands over, add up the sizes of its files. The dictionary maps each folder to its bytes."),
         ]),
    dict(id="mkdir", name="Path.mkdir with parents", title="Path.mkdir: making folders, also in a chain", part=3, visual="mkdir",
         concepts=["mkdir"],
         groups=[
             (HEAD + ["try:", "    Path('x/y').mkdir()", "except FileNotFoundError:", "    print('refused: the parent x is missing')"],
              NOTE + "mkdir makes one folder. It refuses when the folder above it does not exist yet."),
             (["Path('x/y').mkdir(parents=True)", "Path('x/y').mkdir(parents=True, exist_ok=True)",
               "print(sorted(str(p) for p in Path('x').rglob('*')))"],
              "parents=True builds the whole chain. exist_ok=True accepts a folder that is already there."),
         ]),
    # ------------------------------------------------------------------ part 4
    dict(id="zipwrite", name="Writing a ZIP file", title="zipfile.ZipFile: write a file into an archive", part=4, visual="zipwrite",
         concepts=["zipfile.ZipFile", "Compressing Files with the zipfile Module"],
         groups=[
             (HEADZ + ["Path('file1.txt').write_text('Hello' * 10000)", "with zipfile.ZipFile('example.zip', 'w') as z:",
                       "    z.write('file1.txt', compress_type=zipfile.ZIP_DEFLATED)"],
              NOTE + "Mode 'w' starts a new archive. write adds a file; ZIP_DEFLATED is the compression that really shrinks it."),
             (["with zipfile.ZipFile('example.zip') as z:", "    info = z.getinfo('file1.txt')", "print(info.filename, info.file_size)",
               "small = info.compress_size < info.file_size / 100", "print('squeezed to under 1 percent:', small)"],
              "getinfo reports the original size and the stored size. Repeated text compresses very well."),
         ]),
    dict(id="zipmodes", name="ZIP modes: append and refuse", title="ZIP modes: read, append, exclusive", part=4, visual="zipmodes",
         concepts=["zipfile.ZipFile"],
         groups=[
             (HEADZ + ["Path('a.txt').write_text('A')", "with zipfile.ZipFile('x.zip', 'w') as z:", "    z.write('a.txt')"],
              NOTE + "Mode 'w' starts the archive x.zip with one member."),
             (["with zipfile.ZipFile('x.zip', 'a') as z:", "    z.writestr('two.txt', '2')"],
              "Mode 'a' adds to an archive that exists. writestr stores text without a file on disk."),
             (["with zipfile.ZipFile('x.zip') as z:", "    print(sorted(z.namelist()))", "try:", "    zipfile.ZipFile('x.zip', 'x')",
               "except FileExistsError:", "    print(\"mode 'x' refused: x.zip exists\")"],
              "namelist lists the members. Mode 'x' creates a new archive only; it refuses to overwrite one."),
         ]),
    dict(id="extract", name="Extracting from a ZIP", title="extractall and extract: unpacking an archive", part=4, visual="extract",
         concepts=["extract"],
         groups=[
             (HEADZ + ["with zipfile.ZipFile('z.zip', 'w') as z:", "    z.writestr('a.txt', 'A')", "    z.writestr('sub/b.txt', 'B')"],
              NOTE + "An archive with two members, one of them inside a subfolder."),
             (["with zipfile.ZipFile('z.zip') as z:", "    z.extractall('out')", "print(sorted(str(p) for p in Path('out').rglob('*')))"],
              "extractall unpacks every member into a folder and rebuilds the subfolders of the archive."),
             (["with zipfile.ZipFile('z.zip') as z:", "    print(z.extract('a.txt', 'new/folder'))"],
              "extract unpacks one member. The target folder is created when it is missing, and the new path is returned."),
         ]),
    dict(id="archives", name="make_archive and unpack_archive", title="shutil.make_archive and unpack_archive", part=4, visual="archives",
         concepts=["Archives"],
         groups=[
             (HEADZ + ["Path('spam/sub').mkdir(parents=True)", "Path('spam/a.txt').write_text('x')", "Path('spam/sub/b.txt').write_text('y')"],
              NOTE + "A small tree to pack."),
             (["name = shutil.make_archive('snap', 'zip', '.', 'spam')", "print(Path(name).name)", "with zipfile.ZipFile(name) as z:",
               "    print(sorted(z.namelist()))"],
              "make_archive packs a whole folder into one ZIP in a single call. The names inside keep the folder name."),
             (["shutil.unpack_archive(name, 'un')", "print(sorted(str(p) for p in Path('un').rglob('*')))"],
              "unpack_archive is the one-call way back: it guesses the format from the file name."),
         ]),
    # ------------------------------------------------------------------ part 5
    dict(id="backup", name="Project 5: backupToZip", title="Project 5: back a folder up into a numbered ZIP", part=5, visual="backup", layout="left",
         concepts=["Practice Programs"],
         groups=[
             (["import os, tempfile, zipfile", "from pathlib import Path", "os.chdir(tempfile.mkdtemp())", "def backup_to_zip(folder):", "    n = 1",
               "    while Path(f'{folder}_{n}.zip').exists(): n += 1"],
              "A new temporary folder; the function finds the first unused number."),
             (["# continued", "    with zipfile.ZipFile(f'{folder}_{n}.zip', 'w') as z:", "        for root, subs, files in os.walk(folder):",
               "            for f in files: z.write(Path(root, f))", "    return f'{folder}_{n}.zip'"],
              "Walk the folder and write every file into the new ZIP, then return its name."),
             (["Path('spam/eggs').mkdir(parents=True)", "Path('spam/file1.txt').write_text('Hello')", "Path('spam/eggs/file2.txt').write_text('Hi')",
               "print(backup_to_zip('spam'), backup_to_zip('spam'))", "with zipfile.ZipFile('spam_1.zip') as z:", "    print(sorted(z.namelist()))"],
              "Two runs make spam_1.zip and spam_2.zip, each with both files."),
         ]),
    dict(id="selective", name="Practice 1: copy by extension", title="Practice program: copy every PDF of a tree", part=5, visual="selective", layout="left",
         concepts=["Practice Programs"],
         groups=[
             (HEAD + ["for d in ('src/a', 'src/b', 'dest'):", "    Path(d).mkdir(parents=True)"],
              "A new temporary folder, with a source tree and an empty dest folder."),
             (["files = ('src/one.pdf', 'src/a/two.PDF',", "         'src/b/three.txt', 'src/b/four.pdf')", "for f in files: Path(f).write_text(f)"],
              "Four files: three PDFs, one with capital letters, and one text file."),
             (["for folder, subs, files in os.walk('src'):", "    for f in files:", "        if f.lower().endswith('.pdf'):",
               "            shutil.copy(Path(folder, f), 'dest')"],
              "Walk the tree and copy each PDF; lower() ignores capitals."),
             (["print(sorted(os.listdir('dest')))", "print(sorted(f for _, _, fs in os.walk('src') for f in fs))"],
              "The copies are in dest, and the source keeps all four files."),
         ]),
    dict(id="large", name="Practice 2: the big files", title="Practice program: find the big files", part=5, visual="large", layout="left",
         concepts=["Practice Programs"],
         groups=[
             (HEAD + ["Path('sub').mkdir()", "sizes = {'big.bin': 3000, 'mid.bin': 1200,", "         'tiny.txt': 40, 'sub/huge.bin': 9000}"],
              "A new temporary folder, and four sizes in bytes; one file sits in sub."),
             (["for name, size in sizes.items():", "    Path(name).write_bytes(b'x' * size)"],
              "Write each of the four files with that many bytes."),
             (["found = {}", "for folder, subs, files in os.walk('.'):", "    for f in files:", "        path = Path(folder, f)"],
              "Walk every folder of the tree, including the subfolder sub."),
             (["# continued", "        if os.path.getsize(path) > 1000:", "            found[str(path)] = os.path.getsize(path)",
               "print(dict(sorted(found.items(), key=lambda kv: -kv[1])))"],
              "Keep the files above 1000 bytes, the biggest first."),
         ]),
    dict(id="dates", name="Practice 3: swap day and month", title="Practice program: American dates to European dates", part=5, visual="dates", layout="left",
         concepts=["Practice Programs"],
         groups=[
             (["import os, re, shutil, tempfile", "from pathlib import Path", "os.chdir(tempfile.mkdtemp())",
               "names = ('spam12-31-1900.txt', 'report01-02-2020.txt',", "         'notes.txt')"],
              "A new temporary folder, and three names; two carry a month-day-year date."),
             (["for name in names: Path(name).write_text('')", "pattern = re.compile(r'(\\d\\d)-(\\d\\d)-(\\d\\d\\d\\d)')", "before = sorted(os.listdir('.'))"],
              "The pattern keeps month, day and year as three groups."),
             (["for old in before:", "    if pattern.search(old):", "        new = pattern.sub(r'\\2-\\1-\\3', old)", "        shutil.move(old, new)",
               "print(sorted(os.listdir('.')))"],
              "sub swaps groups 1 and 2, shutil.move renames; notes.txt stays."),
         ]),
]
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
