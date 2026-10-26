"""Chapter 18 deck content, version 2.0.0: the words of the deck (analogies, stories, notes, take-aways, resources, tables).
Every concept label of the chapter research (sen0414_ch18_research_v1_0_2.ttl, 33 labels) has its everyday analogy here, under the research's own label, so the deck
check can find it; stories follow 5N1K with a dated, sourced account and a live link. Facts of the stories are those of 08-tooling/sen0414_ch18_stories_v1_0_0.py
(sources opened on 2026-10-12) read again on 2026-10-26: the Wikipedia pages Comma-separated values, JSON, XML and Billion laughs attack, RFC 4180 on rfc-editor.org
and the Python documentation pages What's New in Python 2.5 and 2.6; facts of the tables are the findings F2 to F18 of the chapter research (03-materials/ch18/rdodi,
data module sen0414_ch18_rdodi_data_v1_0_2.py), named where they are used. Those findings were measured under Python 3.14.6; the examples of this deck ran under
Python 3.13 with xmltodict 0.13.0 and 1.0.4 and print the same lines."""
__version__ = "2.0.0"

# ---- everyday analogies, grouped on the analogy slides: (slide id, title, headline analogy, [(research label, everyday picture)])
ANALOGIES = [
    ("A1", "Everyday pictures: the CSV format", "A CSV file is like a paper register: one line for each entry, and commas as the column lines.", [
        ("The CSV Format", "A paper register: every line is one entry, and commas mark where one column ends."),
        ("csv", "The clerk who knows the register's rules, such as quoted names with commas inside them."),
        ("Reading CSV Files", "Reading the register line by line and cutting each line into its columns."),
        ("Accessing Data in a for Loop", "Turning the pages one at a time instead of photocopying the whole book."),
        ("Writing CSV Files", "Copying entries into a new register, one line for each entry."),
    ]),
    ("A2", "Everyday pictures: tabs, headers and line ends", "A header row is like the heading strip of a register: it names the columns and holds no entry.", [
        ("Using Tabs Instead of Commas", "Ruling the register with tab stops instead of commas; the entries stay the same."),
        ("Handling Header Rows", "Tearing the heading strip off before you count the entries."),
        ("exampleWithHeader3.csv", "A sample register that comes with a heading strip, for practice."),
        ("Figure 18-1: a CSV file written without newline='' opened in a spreadsheet", "A typist who presses the return key twice at the end of each line: a blank line after every entry."),
    ]),
    ("A3", "Everyday pictures: Project 13", "Project 13 is like a clerk who tears the heading strip off every register in a drawer.", [
        ("removeCsvHeader.py", "The clerk's routine: open each register, skip the strip, copy the rest."),
        ("Step 1: Loop Through Each File", "Going through the drawer and taking out only the registers."),
        ("Step 2: Read the File", "Opening one register and passing over its heading strip."),
        ("Step 3: Write the New CSV File", "Copying the remaining lines into a clean register in another drawer."),
        ("removeCsvHeader.zip", "A parcel with a hundred practice registers."),
        ("Ideas for Similar Programs", "The same clerk on other jobs: add up a column, merge registers, pick out some lines."),
    ]),
    ("A4", "Everyday pictures: JSON", "JSON is like a labelled form: every blank has a name, and the value is written next to it.", [
        ("Versatile Plaintext Formats", "Three ways to write one address: a register line, a labelled form, a tree of tags."),
        ("JSON", "A labelled form: name, age, phones, with lists for the blanks that repeat."),
        ("Reading JSON Data", "Reading a filled-in form and copying its values into your own notebook."),
        ("Writing JSON Data", "Filling in a form from your notebook."),
        ("json", "The form-office clerk who reads and fills in forms for you, and refuses a badly written one."),
    ]),
    ("A5", "Everyday pictures: XML", "XML is like a family tree written in labelled boxes: every box has a name and may hold smaller boxes.", [
        ("XML", "Labelled boxes inside boxes, each opened and closed by the same name."),
        ("Reading XML Files", "Opening the outer box and looking inside, box by box."),
        ("Writing XML Files", "Packing boxes into boxes and writing a label on each lid."),
        ("xml.etree.ElementTree", "The standard toolkit for opening and packing the boxes."),
        ("xmltodict", "An unpacking trick: lay the boxes out as a notebook page of names and values."),
    ]),
    ("A6", "Everyday pictures: the practice program", "A converter is like a copy clerk who writes each sheet of a ledger on a card of its own.", [
        ("Practice Program: Excel-to-CSV Converter", "Copying each sheet of a ledger onto its own register."),
        ("excel-to-CSV converter skeleton", "A to-do list for the copy clerk: the steps are named, the work is not done."),
        ("openpyxl", "The key to the ledger cabinet: it opens workbooks without Excel."),
        ("example3.xlsx", "A sample ledger with three sheets, two of them empty."),
        ("excelSpreadsheets.zip", "A parcel of practice sheets, already copied as registers."),
        ("shelve", "A sealed shelf of whole Python objects: only Python can read it."),
    ]),
]

# ---- the stories (5N1K); the picture of each is a record of story_images_v2_0_0.json
STORIES = {
    "ibm": dict(
        title="Story: Commas between values on IBM mainframes, 1972", img="image_ibm.jpg",
        who="IBM, whose Fortran (level H extended) compiler read values separated by commas.",
        what="List-directed input and output with commas between the values: the root of today's CSV files.",
        when="In 1972; the name CSV was in use by 1983.",
        where="On IBM OS/360 mainframes; by 1983 the Osborne Executive's SuperCalc manual documented CSV quoting.",
        why="Free-form input saved counting columns, but an unquoted string could hold no comma and no space.",
        how="Quotes are the later answer: csv.reader keeps a comma inside quotes in one field, as the first example showed.",
        linktext="Comma-separated values (Wikipedia)", link="https://en.wikipedia.org/wiki/Comma-separated_values"),
    "rfc": dict(
        title="Story: RFC 4180 wrote CSV down in October 2005", img="image_ietf.jpg",
        who="Yakov Shafranovich of SolidMatrix Technologies, in the series of RFC memos.",
        what="RFC 4180 documents the common CSV format and registers the media type text/csv.",
        when="October 2005, after more than thirty years of CSV files.",
        where="In the RFC series for the Internet community; the type is registered with IANA.",
        why="No formal specification existed, so programs read CSV in many ways; the memo is Informational, not a standard.",
        how="Records end in CRLF, a header is optional, and fields with commas, quotes or line breaks sit in double quotes.",
        linktext="RFC 4180 (RFC Editor)", link="https://www.rfc-editor.org/rfc/rfc4180"),
    "json": dict(
        title="Story: The first JSON message was sent in April 2001", img="image_crockford.jpg",
        who="Douglas Crockford and Chip Morningstar.",
        what="They sent the first JSON message; Crockford specified and popularized the format.",
        when="In April 2001; RFC 8259 (2017) is the current Internet standard.",
        where="At State Software, a company cofounded by Crockford and others in March 2001.",
        why="The cofounders wanted a system that used standard browser capabilities for stateful web applications.",
        how="JSON borrows a small part of JavaScript's notation, and json.loads() refuses even a comma before a closing bracket.",
        linktext="JSON (Wikipedia)", link="https://en.wikipedia.org/wiki/JSON"),
    "xml": dict(
        title="Story: XML 1.0 became a W3C Recommendation in 1998", img="image_bosak.jpg",
        who="Jon Bosak of Sun Microsystems, with the W3C working group that wrote XML.",
        what="XML 1.0, a simplified descendant of SGML for the web, became a W3C Recommendation.",
        when="On 10 February 1998, after work that began in mid-1996.",
        where="At the World Wide Web Consortium, W3C.",
        why="Bosak recruited collaborators who knew both SGML and the web, to make a strict and simple markup language.",
        how="The rules are strict on purpose: one root, matching tags and case. ElementTree raises ParseError when they break.",
        linktext="XML (Wikipedia)", link="https://en.wikipedia.org/wiki/XML"),
    "pylib": dict(
        title="Story: ElementTree joined Python in 2006 and json in 2008", img="image_guido.jpg",
        who="Fredrik Lundh, who wrote ElementTree, and Bob Ippolito, who wrote simplejson, which became json.",
        what="Their libraries entered Python's standard library as xml.etree and json.",
        when="ElementTree with Python 2.5 on 19 September 2006; json with Python 2.6 on 1 October 2008.",
        where="In the standard library of Python; the What's New pages of the Python documentation say so.",
        why="Modules of the standard library need no installation, so any Python can read JSON and XML.",
        how="Write import json or import xml.etree.ElementTree as ET. The getchildren() of old tutorials is gone today.",
        linktext="What's New in Python 2.5 (docs.python.org)", link="https://docs.python.org/3/whatsnew/2.5.html"),
    "laughs": dict(
        title="Story: A small XML file that asks for a billion laughs", img="image_servers.jpg",
        who="Parser authors and security reporters, who named it the billion laughs attack or XML bomb.",
        what="A document under 1 KB whose entities expand to a billion copies of lol, almost 3 gigabytes.",
        when="First reported as early as 2002; widely addressed from 2008.",
        where="In any XML parser that expands the entities declared in the document's own DTD.",
        why="A parser that expands entities faithfully can be asked for far more memory than the file is big.",
        how="Ten entities, each made of ten of the one before. defusedxml refuses entities, as the last XML example showed.",
        linktext="Billion laughs attack (Wikipedia)", link="https://en.wikipedia.org/wiki/Billion_laughs_attack"),
}
STORY_NOTES = {
    "ibm": "CSV is older than the personal computer: IBM's Fortran compiler read comma-separated values in 1972. The photograph shows an IBM System/360 console and tape drives in a museum, the machine family of OS/360, not the compiler itself.",
    "rfc": "RFC 4180 is dated October 2005 and is informational. The photograph shows an IETF meeting room, the body behind the RFC series; it does not show the author. Python's csv module follows these habits.",
    "json": "Crockford and Morningstar sent the first JSON message in April 2001. The photograph is a portrait of Douglas Crockford. JSON is tiny and strict: a trailing comma is an error.",
    "xml": "XML 1.0 became a W3C Recommendation on 10 February 1998. The photograph is a portrait of Jon Bosak, who started the work in mid-1996. The strict rules are why ElementTree raises ParseError.",
    "pylib": "ElementTree came with Python 2.5 in 2006 and json with Python 2.6 in 2008. The photograph shows Guido van Rossum, the creator of Python, at OSCON 2006. It does not show Lundh or Ippolito.",
    "laughs": "A tiny XML file can ask for a billion copies of lol. The photograph shows server racks in a data centre, the kind of machine such a file can exhaust. It does not show an attack. Use defusedxml for untrusted XML.",
}

# ---- speaker notes, at most 60 words each
NOTES = {
    "title": "Welcome. Chapter 18 reads and writes CSV, JSON and XML files. Every example builds its own data in memory or in a temporary folder, and the same examples stand in the chapter-code tab of the page, in this order.",
    "route": "Six parts. Reading CSV files, writing CSV files, Project 13, then JSON, XML, and the practice program that turns Excel sheets into CSV files. The table gives the slides of each part.",
    "questions": "Two questions to carry through. How do you read and write a table, a record and a tree with the standard library, and what does each format lose? And which statements of the book differ today? The last slides answer both.",
    "divider1": "Part one. A CSV file is records on lines, each a list of fields. csv.reader splits the fields, a for loop reads one row at a time, line_num counts lines, and next() skips a header row.",
    "divider2": "Part two. csv.writer writes lists, DictWriter writes dictionaries. Tabs are a delimiter. newline empty stops Windows doubling line ends, and Excel's UTF-8 files start with a byte order mark.",
    "divider3": "Part three. Project 13 removes the header row of every CSV file in a folder: loop, read, write. The same plan fits other small programs.",
    "divider4": "Part four. JSON has six kinds of value. loads reads text into Python values, dumps writes them out, and a round trip changes tuples into lists. The syntax is strict.",
    "divider5": "Part five. ElementTree reads and writes XML trees; text is always a string or None. xmltodict turns XML into a dictionary. XML from someone else needs defusedxml.",
    "divider6": "Part six. The practice program: open a workbook with openpyxl and write one CSV file for each sheet. The book's skeleton is a to-do list; the examples finish it.",
    "A1": "A CSV file is a register: a line for each entry, commas between columns. The csv module is the clerk who knows the rules. Reading cuts lines into columns; writing copies entries into a new register.",
    "A2": "Tabs instead of commas change only the separator. A header row names the columns and is not data. Without newline empty, Windows presses return twice: a blank line after each entry.",
    "A3": "Project 13 in three steps. Loop through the files of a folder, read each and skip its header, write the rest to a new file. Similar programs follow the same plan.",
    "A4": "One address, three formats: a register line, a labelled form, a tree of tags. JSON is the labelled form. loads reads a form, dumps fills one in, and the json module refuses badly written forms.",
    "A5": "XML is boxes inside boxes with matching labels. ElementTree opens and packs them. xmltodict lays the boxes out as one notebook page of names and values.",
    "A6": "The converter copies each sheet of a ledger onto its own register. openpyxl opens the workbook without Excel. shelve is a sealed shelf of Python objects, not a text format.",
    "csv_split": "A CSV line is not simply split on commas: a quoted field may hold one. csv.reader respects the quotes. A file is a list of records, and a record is a list of fields.",
    "reader_list": "The reader reads a file and list() keeps its rows. data[row][column] picks a value, and every value is a string. A temporary file stands in for the book's example file.",
    "for_loop": "A for loop reads one row at a time. line_num counts lines of the file, so a record with a line break in it makes the numbers jump. A reader can be used once.",
    "next_header": "next() takes the header off the reader. The line_num test of the book fails when the header has a line break inside quotes, because its record ends on line two.",
    "writer_basics": "The writer wraps a file; writerow returns the characters written and quotes a field that holds a comma. Numbers and None become text. Every record ends with CRLF.",
    "tabs": "delimiter sets the character between fields and lineterminator what ends a record. writerows writes many rows. Read with the same delimiter and the rows come back as they were.",
    "newline_blank": "Windows turns every line feed into CRLF. The writer already ends records with CRLF, so the file gets CR CR LF and a reader sees empty records. A TextIOWrapper stands in for Windows here.",
    "quoting": "Six quoting constants, one row. The default, QUOTE_MINIMAL, quotes only the field with the comma. QUOTE_NONE needs an escape character. QUOTE_STRINGS and QUOTE_NOTNULL are newer.",
    "encoding_bom": "Excel's CSV UTF-8 starts with three bytes, a byte order mark. Decoded as plain utf-8 the mark sticks to the first key. Use utf-8-sig, and always pass an encoding to open().",
    "dict_rw": "DictReader takes the keys from the first row; a short row gets None. DictWriter writes the header and fills a missing key with an empty field.",
    "p13_loop": "Step one of Project 13: loop over the sorted file names and skip what does not end in .csv. The test is case-sensitive, so C.CSV is skipped.",
    "p13_read": "Step two: read each file and skip the first row. next(reader, None) does not fail on an empty file. A file with only a header gives an empty list.",
    "p13_write": "Step three: write the remaining rows to a file of the same name in a new folder. Count the lines before and after: each file is one line shorter.",
    "col_total": "A similar program: add up a column per group. The values are strings, so int() converts them. The dictionary keeps a total for each region.",
    "formats_compare": "The same two people in CSV, JSON and XML. CSV is smallest because it names the columns once. JSON and XML repeat names in every record but keep the structure.",
    "json_loads": "loads reads JSON text and gives a dictionary. null is None, true is True, numbers keep their kind. Every value of the dictionary has one of the six types.",
    "json_dumps": "dumps writes Python values as JSON. A tuple becomes a list and a number key becomes text, so the round trip does not return the original. indent makes the text readable.",
    "json_strict": "json.loads is strict: a trailing comma, single quotes, None and an empty text are refused, each with a message and a column. NaN is accepted although JSON has none.",
    "json_files": "dump and load use a file. ensure_ascii False keeps letters as they are. Bytes with a byte order mark load; a string that starts with the mark is refused.",
    "et_read": "fromstring gives the root element. Looping over an element gives its children. find and findall look up children, get reads an attribute, and text is always a string or None.",
    "et_traps": "ElementTree keeps whitespace between tags as text and tail. Broken XML raises ParseError: closing tags must match, there is one root, and capitals count.",
    "et_write": "Element makes a root, SubElement adds children, tostring writes text. A less-than sign is escaped as lt. indent adds line breaks. write saves a file; xml_declaration adds the first line.",
    "et_nil": "xsi:nil is an attribute in a namespace. ElementTree shows it under its full name in braces and does not interpret it. A namespaced element is written with the address in braces.",
    "xmltodict_rt": "xmltodict turns XML into a dictionary of strings. An attribute gets an @, the text of an element with attributes sits under #text. One child is a dict, two are a list.",
    "xml_security": "Entities can multiply. The standard parser expands them; defusedxml refuses them. Never parse XML from someone else without checking the parser. The billion laughs story is the big cousin.",
    "xl_make": "openpyxl builds a workbook without Excel. append adds a row, create_sheet adds a sheet. Save into memory, load it again, and the numbers are still numbers.",
    "xl_convert": "The converter loops over the sheets and writes one CSV file for each. iter_rows with values_only gives plain values. List the files and read them back to check.",
    "tools": "The calls of the chapter in one table, each with its code slide. Reads change nothing; writes make new text or files.",
    "current": "What differs from the book today, from the chapter research. Run the book's lines first, then compare with these rows. Each row names the slide that shows it.",
    "summary": "Five sentences. CSV is lines of fields. JSON has six value types and a strict syntax. XML is a tree and all its text is strings. Untrusted XML needs defusedxml. One CSV file per sheet.",
    "practice": "Predict first, then run what you can on the chapter page. Each question points to a slide.",
    "resources": "Links to read and watch next: the chapter, the documentation of the three modules, the RFC and the pages behind the stories.",
}

# ---- one take-away line for every code slide
TAKEAWAY = {
    "csv_split": "Never split a CSV line on commas yourself.",
    "reader_list": "list(reader) keeps the rows; every value is a string.",
    "for_loop": "A loop holds one row; line_num counts lines, not records.",
    "next_header": "next(reader) skips the header whatever its length.",
    "writer_basics": "writerow() quotes what needs it and returns the length.",
    "tabs": "delimiter and lineterminator change the layout, not the data.",
    "newline_blank": "Open CSV files with newline='' and Windows cannot double the line ends.",
    "quoting": "QUOTE_MINIMAL quotes only what must be quoted.",
    "encoding_bom": "Name the encoding; utf-8-sig removes Excel's mark.",
    "dict_rw": "A header row becomes the keys.",
    "p13_loop": "Sort the names and test the extension.",
    "p13_read": "next(reader, None) is safe on an empty file.",
    "p13_write": "Copy the rest of each file into the new folder.",
    "col_total": "int() before adding: CSV values are text.",
    "formats_compare": "CSV names columns once; JSON and XML name every value.",
    "json_loads": "null is None, true is True; the numbers keep their kind.",
    "json_dumps": "A round trip turns tuples into lists and number keys into text.",
    "json_strict": "One extra comma is an error.",
    "json_files": "dump and load use a file; the encoding is yours to name.",
    "et_read": "Text is always a string or None; convert numbers yourself.",
    "et_traps": "Whitespace is kept; broken XML raises ParseError.",
    "et_write": "Escape and indent are done for you; the declaration is a choice.",
    "et_nil": "ElementTree does not interpret xsi:nil.",
    "xmltodict_rt": "One child is a dict, two are a list: expect both.",
    "xml_security": "Never parse untrusted XML with a parser you have not checked.",
    "xl_make": "A workbook holds sheets; a sheet holds rows.",
    "xl_convert": "One CSV file for each sheet.",
}

# ---- the table 'which call does what' (header row, then rows: call, what it does, what to know, example id)
TOOLS = [
    ["Call", "What it does", "What to know", "Example"],
    ["csv.reader(f)", "reads rows as lists", "open with newline=''; every value is a str", "reader_list"],
    ["next(reader, None)", "skips the header row", "safe on an empty file", "p13_read"],
    ["csv.writer(f).writerow(row)", "writes one record", "returns the length; CRLF ends", "writer_basics"],
    ["csv.DictReader, DictWriter", "rows as dictionaries", "first row gives the keys", "dict_rw"],
    ["json.loads, json.dumps", "text to value and back", "tuples become lists", "json_dumps"],
    ["ET.fromstring(text)", "XML text to a tree", "text is str or None; ParseError", "et_read"],
    ["ET.tostring, ET.indent", "a tree to XML text", "escapes < and &; space before />", "et_write"],
    ["xmltodict.parse, unparse", "XML to a dictionary", "one child a dict, two a list", "xmltodict_rt"],
    ["defusedxml.ElementTree", "the safe XML parser", "refuses entities", "xml_security"],
]

# ---- what differs from the book today (header row, then: the book, today, example id)
CURRENT = [
    ["What the book says", "Today", "Example"],
    ["Appendix B: open reader files in rb and writer files in wb", "Text mode with newline=''; rb raises an Error and wb a TypeError", "writer_basics"],
    ["Project 13 skips the header with a line_num test", "A header with a line break stays; next(reader, None) always works", "next_header"],
    ["Without newline='' the rows are double-spaced; the reason is beyond the book", "The writer's CRLF becomes CR CR LF; a reader finds empty records", "newline_blank"],
    ["The encoding of a CSV file is never named", "Excel's CSV UTF-8 starts with a byte order mark; use utf-8-sig", "encoding_bom"],
    ["JSON: loads() and dumps() give back what you put in", "Tuples become lists and number keys become text", "json_dumps"],
    ["XML whitespace between tags is insignificant", "ElementTree keeps it as text and tail", "et_traps"],
    ["xsi:nil marks a missing value", "ElementTree keeps it as an attribute; the text stays None", "et_nil"],
    ["XML parsing needs no warning", "Entities can explode: defusedxml refuses them, xmltodict 1.0.4 too", "xml_security"],
    ["The Excel-to-CSV skeleton is a program to complete", "Its loop has no body; dates print as 2035-04-05 13:34:02", "xl_convert"],
]

SUMMARY_POINTS = [
    "A CSV file is lines of fields; let csv.reader split them, and open with newline=''.",
    "JSON has six kinds of value and a strict syntax; a round trip changes tuples.",
    "XML is a tree; ElementTree gives strings and None, and keeps whitespace.",
    "Untrusted XML needs a safe parser such as defusedxml.",
    "A converter writes one CSV file for each sheet of a workbook.",
]

PRACTICE = [
    "A line holds a name, an age and a city with a comma inside quotes. What do split(',') and csv.reader() return? Use the first slide.",
    "Why does the line_num test fail for a header whose first cell holds a line break? Use the header slide.",
    "What does json.loads() give for null, true and a list? What does json.dumps() do to a tuple?",
    "What are the text and the tail of an element, and why is the text of an empty element None?",
    "Write the steps of a converter that saves each sheet of a workbook as its own CSV file.",
]

RESOURCES = [
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 18", "https://automatetheboringstuff.com/3e/chapter18/", "automatetheboringstuff.com"),
    ("Python documentation: csv", "https://docs.python.org/3/library/csv.html", "docs.python.org"),
    ("Python documentation: json", "https://docs.python.org/3/library/json.html", "docs.python.org"),
    ("Python documentation: xml.etree.ElementTree", "https://docs.python.org/3/library/xml.etree.elementtree.html", "docs.python.org"),
    ("Python documentation: XML security", "https://docs.python.org/3/library/xml.html", "docs.python.org"),
    ("xmltodict on PyPI", "https://pypi.org/project/xmltodict/", "pypi.org"),
    ("defusedxml on PyPI", "https://pypi.org/project/defusedxml/", "pypi.org"),
    ("openpyxl documentation", "https://openpyxl.readthedocs.io/en/stable/", "openpyxl.readthedocs.io"),
    ("RFC 4180: the CSV format", "https://www.rfc-editor.org/rfc/rfc4180", "rfc-editor.org"),
    ("JSON: the official site", "https://www.json.org/", "json.org"),
    ("Extensible Markup Language (XML) 1.0, fifth edition", "https://www.w3.org/TR/xml/", "w3.org"),
    ("Wikipedia: Comma-separated values", "https://en.wikipedia.org/wiki/Comma-separated_values", "en.wikipedia.org"),
    ("Wikipedia: Billion laughs attack", "https://en.wikipedia.org/wiki/Billion_laughs_attack", "en.wikipedia.org"),
    ("What's New in Python 2.6: the json module", "https://docs.python.org/3/whatsnew/2.6.html", "docs.python.org"),
]
