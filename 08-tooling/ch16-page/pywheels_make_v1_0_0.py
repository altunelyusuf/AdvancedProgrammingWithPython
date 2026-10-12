#!/usr/bin/env python3
"""Writes pywheels_v1_0_0.json for chapter 16: no wheels (the browser's Python has sqlite3), and a boot snippet that puts the book's shipped
database, sweigartcats.db, where the chapter's programs look for it (the temporary folder, under the name the research scripts use),
so that the five examples that open it run in the browser unchanged. The file is taken from the online materials of the 3rd edition
(No Starch Press), as the research scripts take it, and its SHA-256 is checked here and again inside the snippet.
Usage: pywheels_make_v1_0_0.py [path-to-the-downloaded-zip]   (without a path the zip is fetched from nostarch.com)"""
import io, sys, json, zipfile, hashlib, urllib.request, os
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip"
MEMBER = "Automate_the_Boring_Stuff_3e_onlinematerials/sweigartcats.db"
SHA = "41f0d0b5bc2ebf3835d5b8c59567626bd526038f9733eb57b6759cd05aafcdf9"
if len(sys.argv) > 1: raw = open(sys.argv[1], "rb").read()
else:
    rq = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0"})
    raw = urllib.request.urlopen(rq, timeout=120).read()
db = zipfile.ZipFile(io.BytesIO(raw)).read(MEMBER)
assert hashlib.sha256(db).hexdigest() == SHA, "sweigartcats.db is not the file the research recorded"
boot = ("import os, tempfile, hashlib, binascii\n"
        "_DB = binascii.unhexlify('%s')\n"
        "assert hashlib.sha256(_DB).hexdigest() == '%s'\n"
        "_P = os.path.join(tempfile.gettempdir(), 'ch16_sweigartcats_41f0d0b5.db')\n"
        "def _put():\n"
        "    if not (os.path.exists(_P) and os.path.getsize(_P) == len(_DB) and hashlib.sha256(open(_P, 'rb').read()).hexdigest() == '%s'):\n"
        "        open(_P, 'wb').write(_DB)\n"
        "_put()\n"
        "_cwd0 = os.getcwd()\n"
        "def _before_run():\n"
        "    os.chdir(_cwd0); _put()\n") % (db.hex(), SHA, SHA)
json.dump({"_version": "1.0.0", "wheels": [], "pyodide_packages": [], "boot_python": boot,
           "_note": "No wheel: sqlite3 is part of the browser's Python. The boot snippet writes the 24,576-byte sweigartcats.db of the book's online materials (SHA-256 %s) to the temporary folder under the name the research scripts use, and puts it back before each program if a program removed or changed it." % SHA},
          open(os.path.join(HERE, "pywheels_v1_0_0.json"), "w"), indent=1)
print("written", len(boot), "characters of boot snippet")
