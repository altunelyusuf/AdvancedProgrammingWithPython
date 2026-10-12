#!/usr/bin/env python3
"""SEN0414 chapter 17 (PDF and Word Documents, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, in the shape of
sen0414_ch16_corpus_base_v1_0_0.py. Each program is a complete script that exits 0 and prints what it printed on 2026-10-12 under
Python 3.14.6 (uv) with pypdf 6.20.1, python-docx 1.2.0, pdfminer.six 20260107, Pillow 12.3.0 and cryptography 50.0.2 (the environment
/home/claude/venv314_ch17_latest; the packages are not part of the standard library, so the file is run with that interpreter).
Ten programs build their own small PDF and Word files in a temporary folder and need no network. Two read the files the book ships: they
fetch the online-materials zip from nostarch.com on their first run (the zip and the files are not kept in this repository), check the
sha256 of each file they use, and work on copies in a temporary folder; they are marked LIVE below. The chapter's code is kept as
printed apart from the changes a comment or the next sentence names: Project 12 names its list pdf_filenames in the program and pdf_files in
its loop, so the programs use pdf_filenames; merge() is called with pages=(0, 5) because a tuple in the third place is read as a
bookmark title; and the extraction and image loops open files in the binary modes the library needs.

Shipped-file programs (LIVE): SHIPPEDCHAPTERPDF (the sample chapter: 18 pages, the images, the text of its first page) and
SHIPPEDDEMODOCX (demo.docx: its paragraphs, runs and the restyling of the chapter). Synthetic: PDFSTRUCTURE, PAGESELECTION,
ROTATEBLANKWATERMARK, ENCRYPTDECRYPT, TEXTANDIMAGES, DOCXREADSTYLES, DOCXWRITING, and the three practice programs PDFPARANOIA,
CUSTOMINVITATIONS and PASSWORDBREAKER (the last one on a four-word dictionary; the study's full run is in ch17-page/live_observations).

Sources read for this chapter, on 2026-10-12: the book chapter (automatetheboringstuff.com/3e/chapter17.html, sha256 00cb1643...4b789 as the
book's ontology records), the pypdf, python-docx and pdfminer.six documentation, the Python 3.14 documentation and the other sources the
research record lists.
"""
HEAD = '''import io, os, re, sys, tempfile, zipfile, struct, zlib
os.chdir(tempfile.mkdtemp())
import pypdf
def make_pdf(*pages):
    """a small valid PDF 1.4 of text pages (Helvetica, 612 x 792); a page that starts with BT is used as a content stream"""
    o = ['<</Type/Catalog/Pages 2 0 R>>', None, '<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>']; kids = []
    for s in pages:
        n = len(o) + 1; kids.append(n); c = s if s.startswith('BT') else 'BT /F1 18 Tf 72 720 Td (%s) Tj ET' % s
        o.append('<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Resources<</Font<</F1 3 0 R>>>>/Contents %d 0 R>>' % (n + 1))
        o.append('<</Length %d>>\\nstream\\n%s\\nendstream' % (len(c), c))
    o[1] = '<</Type/Pages/Kids[%s]/Count %d>>' % (' '.join('%d 0 R' % k for k in kids), len(kids))
    b = b'%PDF-1.4\\n'; offs = []
    for i, s in enumerate(o, 1): offs.append(len(b)); b += ('%d 0 obj\\n%s\\nendobj\\n' % (i, s)).encode()
    x = len(b); b += ('xref\\n0 %d\\n0000000000 65535 f \\n' % (len(o) + 1)).encode() + ''.join('%010d 00000 n \\n' % i for i in offs).encode()
    return b + ('trailer\\n<</Size %d/Root 1 0 R>>\\nstartxref\\n%d\\n%%%%EOF\\n' % (len(o) + 1, x)).encode()
def save(name, data):
    with open(name, 'wb') as f: f.write(data)
'''
REAL = '''import hashlib, urllib.request
SHA = {'Recursion_Chapter1.pdf': 'd943896e0bd2241d5d8d819b43c197225c5e87c23a4b852c4819e74261bbad29', 'demo.docx': 'b43b21137d7d69b16e9e1ec7ebb75e0e2f053d8947cd2ddcf79d60a0dfe5f121'}
def real_file(name):
    cache = os.environ.get('CH17_CACHE') or tempfile.gettempdir(); p = os.path.join(cache, 'ch17_' + SHA[name][:8] + '_' + name)
    if not os.path.exists(p):
        rq = urllib.request.Request('https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0'})
        z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(rq, timeout=120).read()))
        open(p + '.part', 'wb').write(z.read('Automate_the_Boring_Stuff_3e_onlinematerials/' + name)); os.replace(p + '.part', p)
    assert hashlib.sha256(open(p, 'rb').read()).hexdigest() == SHA[name], 'the shipped file is not the one the study read'
    import shutil; shutil.copy(p, name); return name
'''

PDFSTRUCTURE = HEAD + '''# What a PDF file is made of: header, numbered objects, a cross-reference table at the end, text as drawing commands.
data = make_pdf('Page one', 'Page two')
print(data[:8], data.rstrip().endswith(b'%%EOF'))
start = int(re.search(rb'startxref\\n(\\d+)', data).group(1))
print('startxref points at', data[start:start + 4])
rows = re.findall(rb'(\\d{10}) (\\d{5}) ([nf]) \\n', data[start:])
print(len(rows), 'table entries; object 0 is', 'free' if rows[0][2] == b'f' else 'in use')
print([data[int(o):int(o) + 7] for o, g, t in rows[1:4]])
reader = pypdf.PdfReader(io.BytesIO(data))
print('content stream:', reader.pages[0].get_contents().get_data())
# Text drawn in the order of the stream, not of the page; and a black box over text hides nothing from a program.
c = 'BT /F1 12 Tf 200 700 Td (world) Tj ET BT /F1 12 Tf 72 700 Td (Hello) Tj ET'
page = pypdf.PdfReader(io.BytesIO(make_pdf(c))).pages[0]
print(repr(page.extract_text()), repr(page.extract_text(extraction_mode='layout').strip()))
secret = pypdf.PdfReader(io.BytesIO(make_pdf('BT /F1 18 Tf 72 720 Td (Salary: 120000 USD) Tj ET 0 0 0 rg 60 710 300 30 re f'))).pages[0]
print('text under the black box:', secret.extract_text())
w = pypdf.PdfWriter(); w.append(io.BytesIO(data)); out = io.BytesIO(); w.write(out)
print('after pypdf wrote it:', dict(pypdf.PdfReader(out).metadata))
'''
PAGESELECTION = HEAD + '''# Copying pages into a new file: a tuple is a range, a list is exact, merge() inserts at a position.
six = make_pdf(*['Page %d' % i for i in range(1, 7)])
def texts(writer):
    buf = io.BytesIO(); writer.write(buf); return [p.extract_text() for p in pypdf.PdfReader(buf).pages]
for label, pages in (('(0, 5)', (0, 5)), ('(0, 5, 2)', (0, 5, 2)), ('[0, 5]', [0, 5])):
    w = pypdf.PdfWriter(); w.append(io.BytesIO(six), pages)
    print('append', label, '->', texts(w))
w = pypdf.PdfWriter(); w.append(io.BytesIO(make_pdf('A1', 'A2', 'A3')))
w.merge(1, io.BytesIO(six), pages=(0, 2))
print('merge(1, file, pages=(0, 2)) ->', texts(w))
w = pypdf.PdfWriter(); w.append(io.BytesIO(make_pdf('A1', 'A2', 'A3')))
w.merge(1, io.BytesIO(six), (0, 2))   # the chapter's way of writing it
print('merge(1, file, (0, 2)) ->', len(w.pages), 'pages; bookmark titles', [o['/Title'] for o in w.outline])
for pages in ((0, 99), [0, 99]):
    try:
        pypdf.PdfWriter().append(io.BytesIO(six), pages)
    except IndexError as e:
        print(pages, 'raises IndexError:', e)
'''
ROTATEBLANKWATERMARK = HEAD + '''# Rotating, inserting blank pages and laying one page over another.
w = pypdf.PdfWriter(); w.append(io.BytesIO(make_pdf('x')))
page = w.pages[0]
seen = []
for angle in (90, 270, -90, 180):
    page.rotate(angle); seen.append(page.rotation)
print('rotation after 90, 270, -90, 180:', seen)
try:
    page.rotate(45)
except ValueError as e:
    print('ValueError:', e)
w = pypdf.PdfWriter()
for size in ((300, 400), (100, 100), (200, 200)): w.add_blank_page(width=size[0], height=size[1])
w.add_blank_page(); w.insert_blank_page(index=1)
print('sizes:', [(float(p.mediabox.width), float(p.mediabox.height)) for p in w.pages])
print('insert_blank_page(2) makes a page', float(w.insert_blank_page(2).mediabox.width), 'points wide; index=2 makes one', float(w.insert_blank_page(index=2).mediabox.width))
for over in (False, True):
    base = pypdf.PdfReader(io.BytesIO(make_pdf('BASE'))).pages[0]; mark = pypdf.PdfReader(io.BytesIO(make_pdf('MARK'))).pages[0]
    print('merge_page(over=%s) draws' % over, re.findall(rb'\\((\\w+)\\) Tj', (base.merge_page(mark, over=over), base.get_contents().get_data())[1]))
'''
ENCRYPTDECRYPT = HEAD + '''# Encrypting with RC4 (the default) and AES-256, and what a reader does before and after decrypt().
def encrypted(**kw):
    w = pypdf.PdfWriter(); w.append(io.BytesIO(make_pdf('Secret page'))); w.encrypt('swordfish', **kw)
    b = io.BytesIO(); w.write(b); return b.getvalue()
for label, kw in (('default', {}), ('AES-128', {'algorithm': 'AES-128'}), ('AES-256', {'algorithm': 'AES-256'})):
    e = pypdf.PdfReader(io.BytesIO(encrypted(**kw))).trailer['/Encrypt']
    print('%-8s V %s R %s Length %s' % (label, e['/V'], e['/R'], e['/Length']))
data = encrypted(algorithm='AES-256')
reader = pypdf.PdfReader(io.BytesIO(data))
print('is_encrypted', reader.is_encrypted)
try:
    reader.pages[0]
except Exception as e:
    print(type(e).__name__, '-', e)
for pw in ('an incorrect password', '', 'Swordfish', 'swordfish'):
    print(repr(pw), '->', pypdf.PdfReader(io.BytesIO(data)).decrypt(pw).name)
print(reader.decrypt('swordfish').name, repr(reader.pages[0].extract_text()))
w = pypdf.PdfWriter(); w.append(io.BytesIO(make_pdf('Two passwords'))); w.encrypt('userpw', owner_password='ownerpw')
b = io.BytesIO(); w.write(b)
print([(p, pypdf.PdfReader(io.BytesIO(b.getvalue())).decrypt(p).name) for p in ('userpw', 'ownerpw', 'swordfish')])
w = pypdf.PdfWriter(); w.append(io.BytesIO(make_pdf('Open'))); w.encrypt('', owner_password='owner')
b = io.BytesIO(); w.write(b); r = pypdf.PdfReader(b)
print('empty user password:', r.is_encrypted, repr(r.pages[0].extract_text()))
'''
TEXTANDIMAGES = HEAD + '''# Text extraction in three ways, an image, a scanned page, and damaged files.
from pdfminer.high_level import extract_text
from PIL import Image
six = make_pdf(*['Page %d' % i for i in range(1, 7)])
reader = pypdf.PdfReader(io.BytesIO(six))
text = ''
for page in reader.pages: text += page.extract_text()
print('pypdf, pages added one after another:', repr(text))
print('pdfminer.six:', repr(extract_text(io.BytesIO(six))[:24]), 'form feeds', extract_text(io.BytesIO(six)).count('\\x0c'))
c = 'BT /F1 12 Tf 72 700 Td (Name) Tj 200 0 Td (Price) Tj ET BT /F1 12 Tf 72 686 Td (Tea) Tj 200 0 Td (3) Tj ET'
page = pypdf.PdfReader(io.BytesIO(make_pdf(c))).pages[0]
print(repr(page.extract_text())); print(page.extract_text(extraction_mode='layout').strip())
t = pypdf.PdfReader(io.BytesIO(make_pdf('BT /F1 12 Tf 72 700 Td (follow-) Tj ET BT /F1 12 Tf 72 686 Td (ing the execution) Tj ET'))).pages[0].extract_text()
print(repr(t), '->', repr(re.sub(r'-\\n', '', t)))
buf = io.BytesIO(); Image.new('RGB', (40, 40), 'white').save(buf, 'PDF')
scan = pypdf.PdfReader(io.BytesIO(buf.getvalue())).pages[0]
print('a scanned page: text', repr(scan.extract_text()), 'images', [(i.name, i.data[:2]) for i in scan.images])
cut = six[:six.index(b'xref')]
for label, f in (('pypdf, cut before xref', lambda: pypdf.PdfReader(io.BytesIO(cut))), ('pdfminer, cut before xref', lambda: extract_text(io.BytesIO(cut))), ('pypdf, empty file', lambda: pypdf.PdfReader(io.BytesIO(b'')))):
    try:
        f()
    except Exception as e:
        print(label, '->', type(e).__name__)
'''
DOCXREADSTYLES = HEAD + '''# Reading a Word document: paragraphs, runs, what paragraphs leave out, and the styles of the template.
import docx
from collections import Counter
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import parse_xml
doc = docx.Document()
p = doc.add_paragraph('A plain paragraph with some ')
p.add_run('bold').bold = True
p.add_run(' text and some ')
p.add_run('italic').italic = True
doc.add_paragraph('')
t = doc.add_table(rows=1, cols=1); t.cell(0, 0).text = 'in a table'
doc.sections[0].header.paragraphs[0].text = 'IN THE HEADER'
q = doc.add_paragraph('before '); q._p.append(parse_xml('<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:r><w:t>linked</w:t></w:r></w:hyperlink>'))
doc.save('read.docx')
doc = docx.Document('read.docx')
print([x.text for x in doc.paragraphs])
print([(r.text, r.bold, r.italic) for r in doc.paragraphs[0].runs])
print('table text:', doc.tables[0].cell(0, 0).text, '| header text:', doc.sections[0].header.paragraphs[0].text)
print('hyperlink paragraph: text', repr(doc.paragraphs[-1].text), 'runs', [r.text for r in doc.paragraphs[-1].runs])
styles = docx.Document().styles
print(sorted(Counter(s.type.name for s in styles).items()), len(list(styles)))
for obj, name in ((doc.paragraphs[0], 'Quote Char'), (doc.paragraphs[0].runs[0], 'Quote'), (doc.paragraphs[0], 'Quote'), (doc.paragraphs[0].runs[0], 'Quote Char')):
    try:
        obj.style = name; print(name, 'accepted')
    except ValueError as e:
        print(name, '->', e)
for n in ('List Number ', 'List Number'):
    try:
        doc.add_paragraph('x', n); print(repr(n), 'ok')
    except KeyError as e:
        print(repr(n), 'KeyError', e)
s = doc.styles.add_style('Invitation Name', WD_STYLE_TYPE.PARAGRAPH); s.base_style = doc.styles['Normal']; s.font.bold = True
print(s.name, s.type.name, doc.add_paragraph('Prof. Plum', 'Invitation Name').style.name)
'''
DOCXWRITING = HEAD + '''# Writing a Word document: paragraphs, headings, run formatting, breaks and pictures.
import docx
from docx.shared import Inches, Cm
from docx.enum.text import WD_BREAK, WD_UNDERLINE
def png(w, h):
    raw = b''.join(b'\\x00' + b'\\xff\\x00\\x00' * w for _ in range(h))
    ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d))
    return b'\\x89PNG\\r\\n\\x1a\\n' + ch(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw)) + ch(b'IEND', b'')
doc = docx.Document()
for level in (0, 1, 4, 9, 10):
    try:
        print(level, doc.add_heading('Header %d' % level, level).style.name)
    except ValueError as e:
        print(level, 'ValueError:', e)
p = doc.add_paragraph('Hello world!'); r = p.add_run(' This text is being added to the second paragraph.')
print(type(p).__name__, type(r).__name__, len(p.runs))
r.bold = True; print('bold', r.bold, re.findall(r'<w:b[ /][^>]*>', r._r.xml)); r.bold = False; print('bold', r.bold, re.findall(r'<w:b[ /][^>]*>', r._r.xml)); r.bold = None; print('bold', r.bold)
r.underline = WD_UNDERLINE.DOUBLE; print(re.findall(r'<w:u [^>]*>', r._r.xml))
r.strike = True; print('run.strike = True:', r.font.strike); r.font.strike = True; print('run.font.strike = True:', r.font.strike)
p.add_run().add_break(WD_BREAK.PAGE); doc.add_paragraph('This is on the second page!')
print(re.findall(r'<w:br[^>]*>', doc.element.xml))
data = png(60, 80)
for kw in ({}, {'width': Inches(1)}, {'width': Inches(1), 'height': Cm(4)}):
    shape = doc.add_picture(io.BytesIO(data), **kw); print(kw and {k: int(v) for k, v in kw.items()}, '->', int(shape.width), int(shape.height))
doc.save('written.docx'); z = zipfile.ZipFile('written.docx')
print(len(doc.paragraphs), 'paragraphs;', len(doc.inline_shapes), 'pictures; media parts', [n for n in z.namelist() if n.startswith('word/media')])
print(z.namelist()[:4], len(z.namelist()), 'parts; first bytes', open('written.docx', 'rb').read(4))
'''
PDFPARANOIA = HEAD + '''# Practice program 1, PDF Paranoia: encrypt every PDF in a folder tree, check the copy, delete the original; then decrypt.
import pypdf
root = 'tree'
for rel in ('a.pdf', 'sub/b.pdf', 'sub/deeper/C.PDF', 'notes.txt'):
    os.makedirs(os.path.dirname(os.path.join(root, rel)) or root, exist_ok=True)
    save(os.path.join(root, rel), make_pdf(rel.upper()) if rel.lower().endswith('.pdf') else b'plain text')
def encrypt_tree(folder, password):
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in sorted(filenames):
            if not filename.lower().endswith('.pdf') or '_encrypted' in filename: continue
            path = os.path.join(dirpath, filename)
            reader = pypdf.PdfReader(path)
            if reader.is_encrypted: print('Skipping (already encrypted):', path); continue
            writer = pypdf.PdfWriter(); writer.append(reader); writer.encrypt(password, algorithm='AES-256')
            new = os.path.join(dirpath, filename[:-4] + '_encrypted' + filename[-4:])
            with open(new, 'wb') as f: writer.write(f)
            check = pypdf.PdfReader(new)
            if check.decrypt(password).name != 'NOT_DECRYPTED' and len(check.pages) == len(reader.pages):
                os.remove(path); print('Encrypted and removed the original:', path)
def decrypt_tree(folder, password):
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in sorted(filenames):
            if not filename.lower().endswith('_encrypted.pdf'): continue
            path = os.path.join(dirpath, filename); reader = pypdf.PdfReader(path)
            if reader.decrypt(password).name == 'NOT_DECRYPTED': print('Wrong password for', path, '- continuing'); continue
            writer = pypdf.PdfWriter(); writer.append(reader)
            with open(path.replace('_encrypted', '_decrypted'), 'wb') as f: writer.write(f)
            print('Decrypted copy:', path.replace('_encrypted', '_decrypted'))
encrypt_tree(root, 'swordfish')
print(sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs))
decrypt_tree(root, 'wrong'); decrypt_tree(root, 'swordfish')
print(sorted(os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs))
print({os.path.basename(os.path.join(d, f)): pypdf.PdfReader(os.path.join(d, f)).pages[0].extract_text() for d, _, fs in os.walk(root) for f in fs if f.lower().endswith('_decrypted.pdf')})
'''
CUSTOMINVITATIONS = HEAD + '''# Practice program 2, Custom Invitations: one invitation per page, with styles made in the program.
import docx
from docx.shared import Pt
from docx.enum.style import WD_STYLE_TYPE
guests = ['Prof. Plum', 'Miss Scarlet', 'Col. Mustard', 'Al Sweigart', 'Robocop']
doc = docx.Document()
for name, size, bold in (('Invite Lead', 20, False), ('Invite Name', 32, True), ('Invite Detail', 14, False)):
    s = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH); s.base_style = doc.styles['Normal']; s.font.size = Pt(size); s.font.bold = bold
for i, guest in enumerate(guests):
    doc.add_paragraph('It would be a pleasure to have the company of', 'Invite Lead')
    doc.add_paragraph(guest, 'Invite Name')
    doc.add_paragraph('at 11010 Memory Lane on the Evening of', 'Invite Lead')
    doc.add_paragraph('April 1st', 'Invite Detail')
    doc.add_paragraph("at 7 o'clock", 'Invite Detail')
    if i < len(guests) - 1: doc.add_page_break()
doc.save('invitations.docx')
d = docx.Document('invitations.docx')
print(len(d.paragraphs), 'paragraphs;', d.element.xml.count('w:type="page"'), 'page breaks for', len(guests), 'guests')
print([p.text for p in d.paragraphs if p.style.name == 'Invite Name'])
print(sorted({p.style.name for p in d.paragraphs if p.style.name.startswith('Invite')}))
'''
PASSWORDBREAKER = HEAD + '''# Practice program 3, PDF Password Breaker, on a small dictionary: both cases of every word, until decrypt() succeeds.
import pypdf, time
words = ['apple', 'banana', 'cherry', 'dragonfruit']
w = pypdf.PdfWriter(); w.append(io.BytesIO(make_pdf('Locked'))); w.encrypt('CHERRY', algorithm='AES-256')
b = io.BytesIO(); w.write(b); data = b.getvalue()
reader = pypdf.PdfReader(io.BytesIO(data))
attempts = 0; found = None
for word in words:
    for guess in (word, word.upper()):
        attempts += 1
        if reader.decrypt(guess).name != 'NOT_DECRYPTED': found = guess; break
    if found: break
print('found', found, 'after', attempts, 'attempts;', 'a dictionary of n words costs up to', 2 * len(words), 'attempts')
print(repr(reader.pages[0].extract_text()))
start = time.perf_counter(); pypdf.PdfReader(io.BytesIO(data)).decrypt('nope'); print('one failed AES-256 attempt takes under one second:', time.perf_counter() - start < 1)
'''
SHIPPEDCHAPTERPDF = HEAD + REAL + '''# The sample chapter the book ships: pages, images, the text of the first page, and the chapter's own loops on it.
name = real_file('Recursion_Chapter1.pdf')
reader = pypdf.PdfReader(name)
print(len(reader.pages), 'pages; encrypted', reader.is_encrypted, '; page size', [float(x) for x in reader.pages[0].mediabox])
print(repr(reader.pages[0].extract_text()[:60]))
text = ''
for page in reader.pages: text += page.extract_text()
print(len(text) > 30000, 'characters of text; the pages are joined with no separator:', repr(reader.pages[0].extract_text()[-12:] + reader.pages[1].extract_text()[:12]))
print('images per page:', [len(p.images) for p in reader.pages])
n = 0
for number, page in enumerate(reader.pages, 1):
    for image in page.images:
        n += 1
        with open('%d_page%d_%s' % (n, number, image.name), 'wb') as f: f.write(image.data)
print(n, 'image files written')
writer = pypdf.PdfWriter(); writer.append(name, (0, 5))
with open('first_five_pages.pdf', 'wb') as f: writer.write(f)
print(len(pypdf.PdfReader('first_five_pages.pdf').pages), 'pages in first_five_pages.pdf')
'''
SHIPPEDDEMODOCX = HEAD + REAL + '''# The Word file the book ships: its paragraphs, its runs, and the restyling of the chapter.
import docx
name = real_file('demo.docx')
doc = docx.Document(name)
print([(p.style.name, p.text) for p in doc.paragraphs])
print([(r.text, r.bold, r.italic) for r in doc.paragraphs[1].runs])
print('table count', len(doc.tables), '; author of the file', repr(doc.core_properties.author), '; last modified by', repr(doc.core_properties.last_modified_by))
doc.paragraphs[0].style = 'Normal'
doc.paragraphs[1].runs[0].style = 'Quote Char'
doc.paragraphs[1].runs[1].underline = True
doc.paragraphs[1].runs[3].underline = True
doc.save('restyled.docx')
d = docx.Document('restyled.docx')
print(d.paragraphs[0].style.name, [(r.text, r.style.name, r.underline) for r in d.paragraphs[1].runs])
print(zipfile.ZipFile('restyled.docx').namelist()[:5])
'''
PROGRAMS = {
    'pdfStructure_v1_0_0.py': (PDFSTRUCTURE, (), False),
    'pageSelection_v1_0_0.py': (PAGESELECTION, (), False),
    'rotateBlankWatermark_v1_0_0.py': (ROTATEBLANKWATERMARK, (), False),
    'encryptDecrypt_v1_0_0.py': (ENCRYPTDECRYPT, (), False),
    'textAndImages_v1_0_0.py': (TEXTANDIMAGES, (), False),
    'docxReadStyles_v1_0_0.py': (DOCXREADSTYLES, (), False),
    'docxWriting_v1_0_0.py': (DOCXWRITING, (), False),
    'practicePdfParanoia_v1_0_0.py': (PDFPARANOIA, (), False),
    'practiceCustomInvitations_v1_0_0.py': (CUSTOMINVITATIONS, (), False),
    'practicePasswordBreaker_v1_0_0.py': (PASSWORDBREAKER, (), False),
    'shippedChapterPdf_v1_0_0.py': (SHIPPEDCHAPTERPDF, (), True),
    'shippedDemoDocx_v1_0_0.py': (SHIPPEDDEMODOCX, (), True),
}
FIXTURE_BASED = []

if __name__ == "__main__":
    # Usage: /home/claude/venv314_ch17_latest/bin/python sen0414_ch17_corpus_base_v1_0_0.py   (exits 1 if a program does not exit 0)
    import os, subprocess, sys
    bad = 0
    for name, (code, needs, live) in PROGRAMS.items():
        r = subprocess.run([sys.executable, "-W", "ignore", "-c", code], capture_output=True, text=True, timeout=300)
        bad += r.returncode != 0
        print("=== %s (exit %d)%s" % (name, r.returncode, " LIVE" if live else "")); print(r.stdout.rstrip()[:1600]); print(r.stderr[-300:].rstrip())
    print("%d programs, %d did not exit 0" % (len(PROGRAMS), bad)); sys.exit(1 if bad else 0)
