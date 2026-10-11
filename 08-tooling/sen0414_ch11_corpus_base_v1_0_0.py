#!/usr/bin/env python3
"""SEN0414 chapter 11 (Organizing Files, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, mirroring
the shape of sen0414_ch10_corpus_base_v1_0_0.py (written fresh for this chapter, not copied from another chapter's
base).

Every program below writes its files inside a temporary directory it creates and removes itself, rather than the
real working directory, which has no files of its own for any of these programs to find; nothing about the
chapter's own file-handling logic is changed by this.

BACKUP_PROJECT is Project 5 of the chapter, backupToZip, kept exactly as the chapter's own research record found
it when run literally: the archive is opened with no compression type at all, so it is never actually compressed,
and write() is handed the absolute path folder_name / filename the walk itself hands back, so each member's own
name inside the archive carries the whole path rather than a short, relative one - a real property of the
chapter's own listed code, not a bug introduced here. The demonstration below runs the function from a working
directory that sits next to the folder being backed up, not inside it, so the one placement mistake self
inclusion documents separately does not also appear in this transcript.

SELECTIVE_COPY and DATE_RENAMING are, respectively, the first and fourth of the chapter's own four practice
programs; LARGE_FILES and RENUMBER_FILES, the second and third, are documented instead through their own
input-output examples in the domain ABox, to keep this module's own transcripts short enough for the deck.

Sources read for this chapter, on 2026-10-01: the book chapter (automatetheboringstuff.com/3e/chapter11.html); the
Python 3.14 documentation (shutil, os, os.path, pathlib, zipfile, re). Every behaviour quoted is executed
(python3.14 against the programs below).
"""
__version__ = "1.0.0"

# ---------------------------------------------------------------------------------------------------------------------------------
# Project 5: backupToZip, the chapter's own program that backs a folder up into a numbered ZIP file.
# ---------------------------------------------------------------------------------------------------------------------------------
BACKUP_PROJECT = r"""import os
import tempfile
import zipfile
from pathlib import Path


def backup_to_zip(folder):
    folder = Path(folder)
    number = 1
    while True:
        zip_filename = Path(folder.parts[-1] + '_' + str(number) + '.zip')
        if not zip_filename.exists():
            break
        number = number + 1

    print('Creating %s...' % zip_filename)
    backup_zip = zipfile.ZipFile(zip_filename, 'w')

    for folder_name, subfolders, filenames in os.walk(folder):
        print('Adding files in %s...' % folder_name)
        folder_name = Path(folder_name)
        for filename in filenames:
            print('Adding file %s...' % filename)
            backup_zip.write(folder_name / filename)

    backup_zip.close()
    print('Done.')
    return zip_filename


with tempfile.TemporaryDirectory() as base:
    os.chdir(base)
    Path('spam').mkdir()
    (Path('spam') / 'file1.txt').write_text('Hello, world!')
    (Path('spam') / 'eggs').mkdir()
    (Path('spam') / 'eggs' / 'file2.txt').write_text('Hi there.')

    made = backup_to_zip('spam')

    archive = zipfile.ZipFile(made)
    members = sorted(archive.namelist())
    print('members:', members)
    print('one member is stored, not compressed:', archive.getinfo(members[0]).compress_type == zipfile.ZIP_STORED)

    second = backup_to_zip('spam')
    print('second run named:', second)
"""

# ---------------------------------------------------------------------------------------------------------------------------------
# Practice program 1: walk a tree and copy every file of one chosen extension into a new folder.
# ---------------------------------------------------------------------------------------------------------------------------------
SELECTIVE_COPY = r"""import os
import shutil
import tempfile
from pathlib import Path


def copy_by_extension(source, destination, extension):
    destination.mkdir(exist_ok=True)
    copied = []
    for folder_name, subfolders, filenames in os.walk(source):
        for filename in filenames:
            if filename.lower().endswith(extension.lower()):
                shutil.copy(Path(folder_name) / filename, destination)
                copied.append(filename)
    return sorted(copied)


with tempfile.TemporaryDirectory() as base:
    os.chdir(base)
    for d in ('src/a', 'src/b'):
        Path(d).mkdir(parents=True)
    for f, text in (('src/one.pdf', 'one'), ('src/a/two.PDF', 'two'),
                    ('src/b/three.txt', 'three'), ('src/b/four.pdf', 'four')):
        Path(f).write_text(text)

    result = copy_by_extension(Path('src'), Path('dest'), '.pdf')
    print('copied:', result)
    print('left behind:', sorted(p.name for p in Path('src').rglob('*') if p.is_file()) )
"""

# ---------------------------------------------------------------------------------------------------------------------------------
# Practice program 4: swap the month and the day inside file names carrying an American MM-DD-YYYY date.
# ---------------------------------------------------------------------------------------------------------------------------------
DATE_RENAMING = r"""import os
import re
import shutil
import tempfile
from pathlib import Path

date_pattern = re.compile(r'(\d\d)-(\d\d)-(\d\d\d\d)')


def swap_month_and_day(folder):
    renamed = []
    for folder_name, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            if not date_pattern.search(filename):
                continue
            new_filename = date_pattern.sub(r'\2-\1-\3', filename)
            old_path = Path(folder_name) / filename
            new_path = Path(folder_name) / new_filename
            shutil.move(old_path, new_path)
            renamed.append((filename, new_filename))
    return renamed


with tempfile.TemporaryDirectory() as base:
    os.chdir(base)
    for name in ('spam12-31-1900.txt', 'report01-02-2020.txt', 'notes.txt'):
        Path(name).write_text('')

    changes = swap_month_and_day(Path(base))
    print('renamed:', sorted(changes))
    print('final folder:', sorted(p.name for p in Path(base).iterdir()))
"""

PROGRAMS = {
    "backupProject_v1_0_0.py": (BACKUP_PROJECT, None, None),
    "selectiveCopy_v1_0_0.py": (SELECTIVE_COPY, None, None),
    "dateRenaming_v1_0_0.py": (DATE_RENAMING, None, None),
}
