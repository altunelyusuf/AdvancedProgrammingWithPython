"""Chapter 18 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter was read on automatetheboringstuff.com on 2026-10-12 (an HTTP fetch of https://automatetheboringstuff.com/3e/chapter18.html;
the page returned 200, 83,216 bytes, and its sha256, c998127be7342ac419f9f884a60aea6ef837e3dba1c2deada1e977a6a20a01dc, equals the chapterDigest the
book's own chapter ontology records; the commit the course pins was not opened). The online materials of the 3rd edition (the zip No Starch Press
links from its book page, 7,759,877 bytes, sha256 dac627e807f69ee14913ba621a15dec1f98db739d76939555ba5360d05eba916) were downloaded and the files chapter 18
uses were opened and their sha256 recorded (exampleWithHeader3.csv, example3.xlsx, removeCsvHeader.py, removeCsvHeader.zip with 100 CSV files,
excelSpreadsheets.zip with 26 CSV files, produceSales3.xlsx and censuspopdata.xlsx); neither the zip nor the files are kept in this repository, and the scripts
fetch them and check the hashes. The zip holds no example3.csv, no my_data.xml and no JSON or XML file at all, so the study made those from the chapter's own
listings and says so where it matters. The Python 3.14 documentation of csv, json, xml.etree.ElementTree and the xml package, the RFCs, the W3C
Recommendations, PyPI, the pages of the stories and the other sources were opened on the same day. Every behaviour was executed under Python 3.14.6 (the newest
3.14 release uv offered; python.org lists 3.14.8) installed with uv on Ubuntu 24.04 (Linux) in a dedicated environment with xmltodict 1.0.4, openpyxl 3.1.5,
defusedxml 0.7.1 and lxml 6.1.3, and the chapter's statements were also replayed with the versions Appendix A of the book pins (xmltodict 0.13.0, openpyxl 3.1.5).
Not executed, and said so where it comes up: Microsoft Excel itself (LibreOffice 24.2 stood in for it), a Windows computer (the translation of line ends that
Windows text mode does was reproduced by asking io.TextIOWrapper for it), Python 3.14.7 and 3.14.8 and the final Python 3.15.0 (uv offered only 3.15.0b4), the
language model clean-up of the chapter, and the Practice Program as readers would write it (a converter was written to the printed skeleton and run on the shipped
workbooks). The chapter's 97 interactive statements are replayed by sen0414_ch18_thirdparty_v1_0_0.py into 08-tooling/ch18-page/third_party_record_v1_0_0.json;
what the public sites and the shipped files did on the day is in ch18-page/live_observations_v1_0_0.json; what one program printed under eleven interpreters
(3.11, 3.12, 3.13, the seven 3.14 releases 3.14.0 to 3.14.6 and 3.15.0b4) is in ch18-page/interpreter_record_v1_0_0.json. A claim not in this file was not made."""
__version__ = "1.0.2"
# 1.0.0 and 1.0.1 of the chapter 18 data module are already committed (the earlier build of the chapter); this version rebuilds the chapter at the standard of
# chapters 13 to 17: two cross-referenced paragraphs per section, the shipped files opened, the chapter's statements replayed, and the public sources as they
# answered on 2026-10-12. The data module is 1.0.2 because 1.0.0 and 1.0.1 are already committed.
CH = 18
DATE = "2026-10-12"
PYVER = "3.14.6"
TITLE = "CSV, JSON and XML files for an advanced course: chapter 18 and today's csv, json, xml.etree.ElementTree and Python"
QUESTION = "What does chapter 18 of the 3rd edition teach about reading and writing CSV, JSON and XML files with the csv module, the json module, xml.etree.ElementTree and xmltodict, which of its printed outputs, programs and statements still hold under Python 3.14.6 (with xmltodict 1.0.4 and openpyxl 3.1.5, and with the versions its Appendix A pins), and what must an advanced course correct or add so that it matches the current modules and the standards behind the formats?"
CQS = ("Which rules does each of the three formats impose, which operations read and write them, and which values or structures does each format lose or refuse, given that all three are plain text that a program must still parse and not split?",
       "Which printed outputs, programs, numbers and statements of the chapter differ in current releases of Python and the packages, in the files the book ships or in the pages it points to, and on what source?")
PUBS = [
 ('P01', 'Automate the Boring Stuff with Python, 3rd edition - Chapter 18, CSV, JSON, and XML Files (Al Sweigart, No Starch Press, 2025)', 'https://automatetheboringstuff.com/3e/chapter18.html', True),
 ('P02', 'Online materials of the 3rd edition, zip with exampleWithHeader3.csv, example3.xlsx, removeCsvHeader.zip, excelSpreadsheets.zip and 87 other files (No Starch Press, 2025)', 'https://nostarch.com/download/code/Automate_the_Boring_Stuff_3e_onlinematerials.zip', False),
 ('P03', 'Automate the Boring Stuff with Python, 3rd edition - table of contents (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/', False),
 ('P04', 'Automate the Boring Stuff with Python, 3rd edition - book page (No Starch Press, 2025)', 'https://nostarch.com/automate-boring-stuff-python-3rd-edition', False),
 ('P05', 'Appendix A, Installing Third-Party Modules, with the versions the book pins (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixa.html', False),
 ('P06', 'Appendix B, Answers to the Practice Questions (Al Sweigart, 2025)', 'https://automatetheboringstuff.com/3e/appendixb.html', False),
 ('P07', 'csv - CSV File Reading and Writing (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/csv.html', False),
 ('P08', 'json - JSON encoder and decoder (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/json.html', False),
 ('P09', 'xml.etree.ElementTree - The ElementTree XML API (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/xml.etree.elementtree.html', False),
 ('P10', 'XML Processing Modules, XML security (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/xml.html', False),
 ('P11', 'xml.dom.minidom - Minimal DOM implementation (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/xml.dom.minidom.html', False),
 ('P12', 'xml.sax - Support for SAX2 parsers (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/xml.sax.html', False),
 ('P13', 'xml.parsers.expat - Fast XML parsing using Expat (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/pyexpat.html', False),
 ('P14', 'tomllib - Parse TOML files (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/tomllib.html', False),
 ('P15', 'io - Core tools for working with streams, text encoding and newlines (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/io.html', False),
 ('P16', 'Built-in Functions, open() (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/functions.html', False),
 ('P17', 'What\'s New In Python 3.14 (Python 3.14 documentation)', 'https://docs.python.org/3.14/whatsnew/3.14.html', False),
 ('P18', 'What\'s New In Python 3.13 (Python documentation)', 'https://docs.python.org/3/whatsnew/3.13.html', False),
 ('P19', 'What\'s New In Python 3.12 (Python documentation)', 'https://docs.python.org/3/whatsnew/3.12.html', False),
 ('P20', 'What\'s New In Python 3.11 (Python documentation)', 'https://docs.python.org/3/whatsnew/3.11.html', False),
 ('P21', 'What\'s New In Python 3.9 (Python documentation)', 'https://docs.python.org/3/whatsnew/3.9.html', False),
 ('P22', 'locale - Internationalization services, getencoding (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/locale.html', False),
 ('P23', 'tracemalloc - Trace memory allocations (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/tracemalloc.html', False),
 ('P24', 'codecs - Codec registry and base classes, utf-8-sig (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/codecs.html', False),
 ('P25', 'dbm - Interfaces to Unix databases, and the shelve module (Python 3.14 documentation)', 'https://docs.python.org/3.14/library/dbm.html', False),
 ('P26', 'PEP 686 - Make UTF-8 mode default (Naoki Inada, Python Software Foundation, 2022)', 'https://peps.python.org/pep-0686/', False),
 ('P27', 'PEP 305 - CSV File API (Kevin Altis et al., Python Software Foundation, 2003)', 'https://peps.python.org/pep-0305/', False),
 ('P28', 'RFC 4180 - Common Format and MIME Type for Comma-Separated Values (CSV) Files (Yakov Shafranovich, IETF, 2005)', 'https://www.rfc-editor.org/rfc/rfc4180', False),
 ('P29', 'RFC 8259 - The JavaScript Object Notation (JSON) Data Interchange Format (Tim Bray, IETF, 2017)', 'https://www.rfc-editor.org/rfc/rfc8259', False),
 ('P30', 'RFC 4627 - The application/json Media Type for JavaScript Object Notation (Douglas Crockford, IETF, 2006)', 'https://www.rfc-editor.org/rfc/rfc4627', False),
 ('P31', 'RFC 7159 - The JavaScript Object Notation (JSON) Data Interchange Format (Tim Bray, IETF, 2014)', 'https://www.rfc-editor.org/rfc/rfc7159', False),
 ('P32', 'RFC 3629 - UTF-8, a transformation format of ISO 10646 (Francois Yergeau, IETF, 2003)', 'https://www.rfc-editor.org/rfc/rfc3629', False),
 ('P33', 'ECMA-404 - The JSON data interchange syntax, 2nd edition (Ecma International, 2017)', 'https://ecma-international.org/publications-and-standards/standards/ecma-404/', False),
 ('P34', 'Introducing JSON (json.org)', 'https://www.json.org/json-en.html', False),
 ('P35', 'Extensible Markup Language (XML) 1.0, Fifth Edition (World Wide Web Consortium, 2008)', 'https://www.w3.org/TR/xml/', False),
 ('P36', 'Extensible Markup Language (XML) 1.0, first edition (World Wide Web Consortium, 1998)', 'https://www.w3.org/TR/1998/REC-xml-19980210', False),
 ('P37', 'Namespaces in XML 1.0, Third Edition (World Wide Web Consortium, 2009)', 'https://www.w3.org/TR/xml-names/', False),
 ('P38', 'XML Schema Part 1: Structures, Second Edition, xsi:nil (World Wide Web Consortium, 2004)', 'https://www.w3.org/TR/xmlschema-1/', False),
 ('P39', 'Media type text/csv (Internet Assigned Numbers Authority)', 'https://www.iana.org/assignments/media-types/text/csv', False),
 ('P40', 'PyPI JSON metadata of xmltodict (Python Package Index, 2026)', 'https://pypi.org/pypi/xmltodict/json', False),
 ('P41', 'openpyxl documentation (openpyxl contributors, 2024)', 'https://openpyxl.readthedocs.io/en/stable/', False),
 ('P42', 'PyPI JSON metadata of openpyxl (Python Package Index, 2026)', 'https://pypi.org/pypi/openpyxl/json', False),
 ('P43', 'PyPI JSON metadata of defusedxml (Python Package Index, 2026)', 'https://pypi.org/pypi/defusedxml/json', False),
 ('P44', 'PyPI JSON metadata of lxml (Python Package Index, 2026)', 'https://pypi.org/pypi/lxml/json', False),
 ('P45', 'PyPI JSON metadata of simplejson (Python Package Index, 2026)', 'https://pypi.org/pypi/simplejson/json', False),
 ('P46', 'Comma-separated values (Wikipedia)', 'https://en.wikipedia.org/wiki/Comma-separated_values', False),
 ('P47', 'JSON (Wikipedia)', 'https://en.wikipedia.org/wiki/JSON', False),
 ('P48', 'XML (Wikipedia)', 'https://en.wikipedia.org/wiki/XML', False),
 ('P49', 'Billion laughs attack (Wikipedia)', 'https://en.wikipedia.org/wiki/Billion_laughs_attack', False),
 ('P50', 'Douglas Crockford (Wikipedia)', 'https://en.wikipedia.org/wiki/Douglas_Crockford', False),
 ('P51', 'CSV, Comma Separated Values (RFC 4180) (Library of Congress, Sustainability of Digital Formats)', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000323.shtml', False),
 ('P52', 'JSON (JavaScript Object Notation) (Library of Congress, Sustainability of Digital Formats)', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000381.shtml', False),
 ('P53', 'XML (Extensible Markup Language) (Library of Congress, Sustainability of Digital Formats)', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000075.shtml', False),
 ('P54', 'CWE-776: Improper Restriction of Recursive Entity References in DTDs (XML Entity Expansion) (MITRE)', 'https://cwe.mitre.org/data/definitions/776.html', False),
 ('P55', 'CWE-611: Improper Restriction of XML External Entity Reference (MITRE)', 'https://cwe.mitre.org/data/definitions/611.html', False),
 ('P56', 'XML External Entity (XXE) Processing (OWASP)', 'https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing', False),
 ('P57', 'What\'s New in Python 2.6, the json module (A. M. Kuchling, Python documentation)', 'https://docs.python.org/3/whatsnew/2.6.html', False),
 ('P58', 'What\'s New in Python 2.5, the ElementTree package (A. M. Kuchling, Python documentation)', 'https://docs.python.org/3/whatsnew/2.5.html', False),
 ('P59', 'LibreOffice Help, CSV filter options (The Document Foundation)', 'https://help.libreoffice.org/latest/en-US/text/shared/guide/csv_params.html', False),
 ('P60', 'uv - an extremely fast Python package and project manager (Astral documentation)', 'https://docs.astral.sh/uv/', False),
 ('P61', 'uv - Python versions (Astral documentation)', 'https://docs.astral.sh/uv/concepts/python-versions/', False),
 ('P62', 'Download Python (python.org)', 'https://www.python.org/downloads/', False),
 ('P63', 'Python Release Python 3.14.0 (python.org)', 'https://www.python.org/downloads/release/python-3140/', False),
 ('P64', 'What\'s New In Python 3.15 (Python documentation)', 'https://docs.python.org/3.15/whatsnew/3.15.html', False),
]
CONCEPTS = [('Section', 'The CSV Format'),
 ('Subsection', 'Reading CSV Files'),
 ('Subsection', 'Accessing Data in a for Loop'),
 ('Subsection', 'Writing CSV Files'),
 ('Subsection', 'Using Tabs Instead of Commas'),
 ('Subsection', 'Handling Header Rows'),
 ('Subsection', 'Step 1: Loop Through Each File'),
 ('Subsection', 'Step 2: Read the File'),
 ('Subsection', 'Step 3: Write the New CSV File'),
 ('Subsection', 'Ideas for Similar Programs'),
 ('Section', 'Versatile Plaintext Formats'),
 ('Subsection', 'JSON'),
 ('Subsection', 'Reading JSON Data'),
 ('Subsection', 'Writing JSON Data'),
 ('Subsection', 'XML'),
 ('Subsection', 'Reading XML Files'),
 ('Subsection', 'Writing XML Files'),
 ('Section', 'Summary'),
 ('Section', 'Practice Questions'),
 ('Section', 'Practice Program: Excel-to-CSV Converter'),
 ('Figure', 'Figure 18-1: a CSV file written without newline="" opened in a spreadsheet'),
 ('Program', 'removeCsvHeader.py'),
 ('Program', 'excel-to-CSV converter skeleton'),
 ('Module', 'csv'),
 ('Module', 'json'),
 ('Module', 'xml.etree.ElementTree'),
 ('Module', 'xmltodict'),
 ('Module', 'openpyxl'),
 ('Module', 'shelve'),
 ('File', 'exampleWithHeader3.csv'),
 ('File', 'example3.xlsx'),
 ('File', 'removeCsvHeader.zip'),
 ('File', 'excelSpreadsheets.zip')]

FINDINGS = [('F1',
  'Background',
  'Chapter 18 of the 3rd edition, CSV, JSON, and XML Files, teaches three plain-text data formats: CSV with the csv module (reader, writer, tabs instead of commas, DictReader and DictWriter) and Project 13 that removes the header row from every CSV file of a folder; JSON with json.loads() and json.dumps(); XML with xml.etree.ElementTree (fromstring, parse, the children of an element, iter, Element, SubElement, set, tostring) and the third-party xmltodict; and it ends with 11 practice questions and one practice program, the Excel-to-CSV converter. '
  'The chapter page of 2026-10-12 is 83,216 bytes with 35 listings (20 of them interactive sessions of 97 statements), 1 captioned figure (Figure 18-1) and no table, and its sha256, c998127be7342ac419f9f884a60aea6ef837e3dba1c2deada1e977a6a20a01dc, equals the chapterDigest of the book\'s own chapter ontology [P01] [P03] [P04].',
  ['P01', 'P03', 'P04']),
 ('F2',
  'The online materials',
  'The online materials of the 3rd edition (7,759,877 bytes, 91 files) hold exampleWithHeader3.csv, example3.xlsx, removeCsvHeader.zip (100 CSV files), excelSpreadsheets.zip (26 CSV files) and the Excel files produceSales3.xlsx and censuspopdata.xlsx, but no example3.csv, no my_data.xml, no output.csv and no JSON or XML file at all, although the chapter\'s listings open example3.csv and my_data.xml; a reader has to type them. '
  'The Practice Program tells the reader to unzip excelSpreadsheets.zip and test an Excel-to-CSV converter on it, but that zip holds 26 files that are already CSV (spreadsheet-A.csv to spreadsheet-Z.csv) and no .xlsx file, so a converter that skips non-xlsx files writes nothing from it. '
  'The shipped exampleWithHeader3.csv has CRLF line ends and the year 2025 in its timestamps where the chapter prints 2035, and it has 7 data rows where the first list printed in the chapter has 6 dictionaries [P01] [P02].',
  ['P01', 'P02']),
 ('F3',
  'The replay of the chapter',
  'All 97 interactive statements of the chapter were replayed in the order of the page under Python 3.14.6. As printed, 89 matched. The two xml_string listings fail as typed: their closing quotation mark of the xsi namespace is a curly quotation mark, so ET.fromstring() and xmltodict.parse() raise a not well-formed error and the name root is then undefined; json_string is wrapped over four lines inside its quotes, which is a SyntaxError. '
  'With the curly quotation mark replaced 93 statements matched; the 4 that still differ are the year (2025 in the shipped file against 2035 printed, 2 statements) and the loop that prints None for address and phone, which prints a line of whitespace instead because the statement before it, tree = ET.parse(\'my_data.xml\'), rebinds root to the pretty-printed file, whose address and phone elements hold the whitespace between their tags. With that statement left out 92 of 94 matched. The same result came with the Appendix A pins (xmltodict 0.13.0, openpyxl 3.1.5) [P01] [P02] [P05].',
  ['P01', 'P02', 'P05']),
 ('F4',
  'Appendix B and the chapter text disagree',
  'Appendix B answers question 3, what modes the File objects for reader and writer objects need to be opened in, with read-binary (rb) for Reader objects and write-binary (wb) for Writer objects, but the chapter writes open(\'output.csv\', \'w\', newline=\'\') and open(\'example3.csv\') in text mode, and under Python 3.14.6 csv.reader on a file opened in rb raises Error: iterator should return strings, not bytes, and csv.writer on a file opened in wb raises TypeError: a bytes-like object is required, not str. '
  'Answer 1 begins In Excel, spreadsheets can have values of data types other than strings, which is correct for question 1. The chapter also says XML syntax is similar to HTML, which we covered in Chapter 18, but Chapter 18 is this chapter and HTML is the subject of Chapter 13 (Web Scraping), which the chapter itself names elsewhere [P01] [P06].',
  ['P01', 'P06']),
 ('F5',
  'Line numbers are not record numbers',
  'Project 13 skips the header row with a test of reader.line_num, keeping a row only if line_num is not 1. The Python documentation says line_num is the number of lines read from the source iterator and is not the same as the number of records, because records can span several lines. '
  'With a header cell that holds a line break (a quoted field Name and (first)), the header record ends at line_num 2, the test keeps 3 of 3 records, and the header is still there; next(reader, None) skips the header record whatever its length. On the 100 shipped files, which have one-line headers and no embedded line breaks, the program as written is right: every output equals the input without its first record (19,631 records in, 19,531 out) [P01] [P07].',
  ['P01', 'P07']),
 ('F6',
  'A for loop and memory',
  'The chapter says looping over the reader object, instead of calling list() on it, is the way to save memory with a big file. On a generated file of 300,000 rows (7.5 MB) the peak memory measured with tracemalloc was 69.0 MiB for list(reader) and 0.166 MiB for a for loop, a ratio of 416, and the loop took 0.40 s against 0.90 s; a DictReader loop took 1.22 s. The claim holds, and a reader object has no len() and no index and can be read once: a second list() on it returned 0 rows [P01] [P07] [P23].',
  ['P01', 'P07', 'P23']),
 ('F7',
  'The encoding the chapter never mentions',
  'Every listing of the chapter calls open() without an encoding, and the chapter does not mention encodings. In text mode the encoding is then the locale encoding, which is UTF-8 here and is cp1252 for most Windows users in the United States. A file of UTF-8 text read as cp1252 gives mojibake without an error (Ad,Sehir becomes a mixture of Ã and Å characters) and a file saved as cp1254 and read as UTF-8 raises UnicodeDecodeError. '
  'An Excel file saved as CSV UTF-8 starts with a byte order mark, which csv.reader returns as part of the first field and which DictReader makes part of the first key (\\ufeffName); encoding=\'utf-8-sig\' removes it. Python 3.15 makes UTF-8 mode the default (PEP 686): under 3.15.0b4 sys.flags.utf8_mode was 1 where 3.11 to 3.14.6 gave 0, and python.org lists 3.15.0 as released on 9 October 2026 although uv offered only 3.15.0b4 [P15] [P16] [P24] [P26] [P62] [P64].',
  ['P15', 'P16', 'P24', 'P26', 'P62', 'P64']),
 ('F8',
  'Line ends and the newline argument',
  'The chapter says that on Windows a reader must pass newline=\'\' to open() or the rows of output.csv will be double-spaced (Figure 18-1) and that the reason is beyond the book. The reason: csv.writer ends every record with CRLF, and a text file opened without newline translates every line feed to the platform line end, so on Windows CRLF becomes CRCRLF. '
  'Reproduced by asking io.TextIOWrapper for the translation Windows does: the bytes were a,b CR CR LF, csv.reader returned each record followed by an empty record, and LibreOffice 24.2 opened the file with the layout of Figure 18-1 (rows 1, 3 and 5 filled, 2 and 4 empty). The Python documentation says a file object given to csv.reader or csv.writer should be opened with newline=\'\' and that it should always be safe to specify it, since the csv module does its own universal newline handling. The figure\'s alt text, Screenshot of a Windows computer desktop showing six overlapping calculator programs, does not describe it: the picture is a spreadsheet [P01] [P07] [P15] [P59].',
  ['P01', 'P07', 'P15', 'P59']),
 ('F9',
  'What csv offers that the chapter leaves out',
  'The chapter does not mention the quoting constants (QUOTE_MINIMAL, QUOTE_ALL, QUOTE_NONNUMERIC, QUOTE_NONE and, since Python 3.12, QUOTE_STRINGS and QUOTE_NOTNULL), the limit of 131,072 characters per field (a field of 131,073 raises Error), skipinitialspace, strict mode, escapechar, the Sniffer, the dialects excel, excel-tab and unix, restkey and restval of DictReader, the ValueError of DictWriter for a key not in fieldnames, and the fact that the writer turns None into an empty field and True into True and so cannot return a type. '
  'QUOTE_STRINGS and QUOTE_NOTNULL do not exist in Python 3.11 and exist in 3.12 to 3.15; a read with QUOTE_NOTNULL gives None for an unquoted empty field and an empty string for a quoted one [P07] [P19].',
  ['P07', 'P19']),
 ('F10',
  'JSON values and what the chapter leaves out',
  'The chapter lists the six JSON value types and tells the reader that trailing commas, single quotes and comments are not allowed. All of it holds under Python 3.14.6 (json.loads of ["spam", "eggs",] raises Illegal trailing comma before end of array at column 16), but the message differs by release: Expecting value in 3.11 and 3.12, the trailing-comma message from 3.13. '
  'The chapter does not say that a tuple becomes a list (and does not come back), that integer, float, None and True keys become strings, that a set, datetime, Decimal, bytes or complex raises TypeError, that Python accepts NaN, Infinity and -Infinity, which RFC 8259 does not allow, that 5,000 digits exceed the 4,300-digit limit for converting a string to int, that json.load and json.dump read and write files, that ensure_ascii turns non-ASCII text into escapes, or that the Python documentation still names RFC 7159, which RFC 8259 obsoleted in December 2017, as the specification [P01] [P08] [P29] [P31].',
  ['P01', 'P08', 'P29', 'P31']),
 ('F11',
  'JSON in Python 3.14 and 3.15',
  'Python 3.14 adds notes to the TypeError of a serialization error that name the path to the value (when serializing list item 1, when serializing dict item a) and allows python -m json, now preferred to python -m json.tool; under 3.11 to 3.13 the notes are absent and python -m json exits with an error. Python 3.15 adds the array_hook parameter to load() and loads() and, with csv, deprecates the __version__ attribute of the module: under 3.15.0b4 reading json.__version__ or csv.__version__ raised a DeprecationWarning that says removal is slated for Python 3.20 [P17] [P64].',
  ['P17', 'P64']),
 ('F12',
  'ElementTree reads text as strings and None, and has only a subset of XPath',
  'The chapter says the text of a self-closing element is None (true, root[3].text is None for car) and shows None for address and phone, which holds for the compact string and not for a pretty-printed file; it says XPath can locate elements, but the module has a limited subset and no xpath() method (lxml has one); every text is a str (age is the string 30, programmer is the string true); an element\'s truth value is False for an element without children and, since Python 3.12, testing it emits a DeprecationWarning, so find() results must be tested with is not None. '
  'iter() returns the root first and then every descendant in document order (16 elements for the chapter\'s person, 6 children). ET.tostring() writes a self-closing element with a space before the slash (<car xsi:nil="true" xmlns:xsi="..." />), where the chapter prints it without; with the default encoding it returns bytes and non-ASCII text becomes character references; encoding=\'unicode\' returns a str; ET.indent() (3.9) pretty-prints in place [P01] [P09] [P17] [P19].',
  ['P01', 'P09', 'P17', 'P19']),
 ('F13',
  'Namespaces and xsi:nil',
  'The chapter writes the car element with xsi:nil="true" and a hand-set xmlns:xsi attribute. ElementTree stores a namespaced attribute under its full name, {http://www.w3.org/2001/XMLSchema-instance}nil, drops xmlns:xsi from the attributes, and never turns nil into None: an element with xsi:nil="true" and text keeps its text, as the XML Schema specification says such an element must be empty for the document to be valid, which ElementTree does not check. '
  'xmltodict keeps @xsi:nil and @xmlns:xsi as keys of a dict, so car is a dict and not None; ET.tostring() writes an attribute named xsi:nil with no check that the prefix is declared, and the parser refuses the result with unbound prefix [P01] [P09] [P37] [P38].',
  ['P01', 'P09', 'P37', 'P38']),
 ('F14',
  'XML security, and a chapter that never says it',
  'The chapter parses XML with ET.fromstring() and xmltodict.parse() and never says that XML from an untrusted source can be an attack. A 760-byte billion laughs document that would expand to 3,000,000,000 characters is refused by ElementTree under Python 3.14.6 (Expat 2.8.1) with limit on input amplification factor (from DTD and entities) breached, in 0.12 s; the Python documentation says Expat versions lower than 2.7.2 may be vulnerable, and 3.14.0 to 3.14.5 carry Expat 2.6.3 and 3.11 to 3.13 carry 2.6.1. '
  'An external entity (file:///etc/hostname) was not read (ElementTree reported undefined entity), defusedxml 0.7.1 raised EntitiesForbidden for all three documents, xmltodict 1.0.4 refuses every entity (ValueError: entities are disabled) and xmltodict 0.13.0, the version Appendix A pins, parsed the billion laughs file and the small entity. The billion laughs attack is catalogued as CWE-776 and external entities as CWE-611 [P09] [P10] [P13] [P40] [P43] [P49] [P54] [P55] [P56].',
  ['P09', 'P10', 'P13', 'P40', 'P43', 'P49', 'P54', 'P55', 'P56']),
 ('F15',
  'The Excel-to-CSV practice program',
  'The printed skeleton is not a program: its for loop has no indented body (IndentationError) and it uses wb, sheet and csv_file without defining them. A converter written to it and run on example3.xlsx, produceSales3.xlsx and censuspopdata.xlsx exited 0 and wrote 5 CSV files in 4.3 s; the dates came out as 2035-04-05 13:34:02, not as the 4/5/2035 13:34 the chapter prints for Excel, because openpyxl returns datetime objects and csv.writer writes their str(); LibreOffice 24.2 writing the same file with its CSV filter wrote 04/05/2035 13:34:02. '
  'The skeleton evaluates sheet.max_column inside the row loop, and each evaluation visits every cell of the sheet: on produceSales3.xlsx (23,758 rows, 4 columns) the first 2,000 rows took 5.94 s with the limit inside the loop and 0.006 s with it hoisted, so the nested loop as printed costs time proportional to rows times cells. Sheet2 and Sheet3 of example3.xlsx are empty and gave a file holding one empty quoted field [P01] [P02] [P41] [P42] [P59].',
  ['P01', 'P02', 'P41', 'P42', 'P59']),
 ('F16',
  'Formats compared, and the versions',
  'On the chapter\'s Alice data the compact JSON is 248 characters, indent=2 makes it 326, and the XML without whitespace is 407 (1.64 times the JSON) and 563 as printed. JSON keeps int, bool and null across a round trip; XML through ElementTree or xmltodict and CSV give strings only; CSV needs a flat row and cannot hold the nested address and phones; tomllib (3.11) reads TOML and has no dumps and TOML has no null; shelve is binary and Python-only. '
  'Across 11 interpreters (3.11, 3.12, 3.13, 3.14.0 to 3.14.6, 3.15.0b4) 50 items were compared and 11 differ: the quoting constants (3.11), the empty quotechar message (3.14), the trailing-comma messages (3.13), the exception notes and python -m json (3.14), the iterparse close() method (3.13), the truth-value DeprecationWarning (3.12), the bundled Expat (2.6.1, 2.6.3, 2.8.1), the default encoding mode (3.15) and the __version__ DeprecationWarning (3.15). The newest releases on PyPI on the day were xmltodict 1.0.4 (22 February 2026), openpyxl 3.1.5 (28 June 2024), defusedxml 0.7.1 (8 March 2021, a 0.8.0rc2 exists) and lxml 6.1.3 [P08] [P14] [P25] [P40] [P42] [P43] [P44] [P45].',
  ['P08', 'P14', 'P25', 'P40', 'P42', 'P43', 'P44', 'P45']),
 ('F17',
  'Where the three formats come from',
  'CSV was in use on IBM mainframes in 1972 and was written down in RFC 4180 in October 2005, which says records end in CRLF, the last record may or may not end in a line break and a header line is optional [P28] [P46]. JSON was specified by Douglas Crockford, sent as a first message in April 2001, described by RFC 4627 in 2006, standardized as ECMA-404 in 2013 and as RFC 8259 in 2017 [P29] [P30] [P33] [P47]. '
  'XML 1.0 was published by the W3C on 10 February 1998 and its fifth edition is dated 26 November 2008 [P35] [P36] [P48]. ElementTree entered the standard library with Python 2.5 on 19 September 2006 and json with Python 2.6 on 1 October 2008 [P57] [P58]. The chapter says nothing about any of this, which is why the six stories of the course supply it.',
  ['P28', 'P29', 'P30', 'P33', 'P35', 'P36', 'P46', 'P47', 'P48', 'P57', 'P58']),
 ('F18',
  'The XML statements of the chapter, tested',
  'The chapter says whitespace outside the opening and closing tags is insignificant, but ElementTree reports it: in a pretty-printed file the text of an element that holds only elements is the whitespace between the tags (address had a line break and eight spaces) and the tail of an element is the whitespace after it. It says tag and attribute names can be written in any case, which holds only if the end-tag matches the start-tag: <A></a> raised a mismatched tag error and <Person><NAME>x</NAME></Person> parsed. '
  'It calls a document with several roots not valid and says valid documents must have a single root; the W3C word for a document that obeys the syntax is well-formed, and valid means compliance with a document type declaration, which ElementTree never checks (a person with a banana child parsed, and a DTD checked with lxml refused it). It says attribute values can be in single or double quotes (true) and does not say that a value with no quotes, an attribute with no value, an unescaped & or < and an HTML entity such as &nbsp; are all errors, which they are [P01] [P09] [P35] [P36].',
  ['P01', 'P09', 'P35', 'P36']),
]


def X(code):
    """An executable example as one expression with no double quote and no line break: the code runs in a fresh
    namespace and the value of its variable out is the result."""
    lit = "'" + code.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace('"', "\\x22") + "'"
    return "(lambda g: (exec(%s, g), g['out'])[1])({})" % lit

# The helpers every example starts from: sample data (the chapter's Alice person as a dict and as XML), rd() reads CSV text, wr() writes it, err() returns what a call raised.
_PRE = r'''import io, csv, json, os, re, sys, tempfile, warnings, subprocess, tracemalloc
import xml.etree.ElementTree as ET
A = {'name': 'Alice Doe', 'age': 30, 'car': None, 'programmer': True, 'address': {'street': '100 Larkin St.', 'city': 'San Francisco', 'zip': '94102'}, 'phone': [{'type': 'mobile', 'number': '415-555-7890'}, {'type': 'work', 'number': '415-555-1234'}]}
NS = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
XS = '<person><name>Alice Doe</name><age>30</age><programmer>true</programmer><car xsi:nil="true" ' + NS + '/><address><street>100 Larkin St.</street><city>San Francisco</city><zip>94102</zip></address><phone><phoneEntry><type>mobile</type><number>415-555-7890</number></phoneEntry><phoneEntry><type>work</type><number>415-555-1234</number></phoneEntry></phone></person>'
def rd(t, **k): return list(csv.reader(io.StringIO(t, newline=''), **k))
def wr(rows, **k):
    s = io.StringIO(newline=''); csv.writer(s, **k).writerows(rows); return s.getvalue()
def err(f):
    try: return ('ok', f())
    except Exception as e: return (type(e).__name__, str(e))
'''

# (top, mid, leaf, exemplar, definition, (the example as an expression, its result))
TAX = [
 ('CsvFormat', 'CsvRules', 'FieldsAndRecords', 'spam,eggs\\r\\nbacon,ham',
  "A CSV file is a list of records, one per line, and each record is a list of fields separated by commas; read from the text spam,eggs CRLF bacon,ham CRLF, csv.reader returned [['spam', 'eggs'], ['bacon', 'ham']], 2 records of 2 fields, 2 commas in the text, and every field a str.",
  (X(_PRE + r'''t = 'spam,eggs\r\nbacon,ham\r\n'
out = (rd(t), t.count(','), len(rd(t)), {type(c).__name__ for r in rd(t) for c in r})'''), "([['spam', 'eggs'], ['bacon', 'ham']], 2, 2, {'str'})")),
 ('CsvFormat', 'CsvRules', 'QuotedCommaField', '"Hello, world!",eggs',
  'A field that contains a comma is enclosed in double quotes, and splitting on commas does not know it: the line "Hello, world!",eggs,bacon,ham split into 5 pieces with str.split(\',\') and the first piece began with a quote, while csv.reader returned 4 fields and the first was Hello, world!.',
  (X(_PRE + r'''t = '"Hello, world!",eggs,bacon,ham'
out = (t.split(','), rd(t)[0])'''), '([\'"Hello\', \' world!"\', \'eggs\', \'bacon\', \'ham\'], [\'Hello, world!\', \'eggs\', \'bacon\', \'ham\'])')),
 ('CsvFormat', 'CsvRules', 'DoubledQuoteEscape', '"say ""hi""",x',
  'A double quote inside a quoted field is written twice: the text "say ""hi""",x was read as the field say "hi" followed by x, and writing the row back produced the same text with a CRLF ending.',
  (X(_PRE + r'''out = (rd('"say ""hi""",x'), wr([['say "hi"', 'x']]))'''), '([[\'say "hi"\', \'x\']], \'"say ""hi""",x\\r\\n\')')),
 ('CsvFormat', 'CsvRules', 'EmbeddedLineBreak', '"two\\nlines",x',
  'A quoted field may contain a line break, so a record can span lines: a text of 3 lines was read as 2 records, the first with the field two<LF>lines, and the writer wrote that field in quotes.',
  (X(_PRE + r'''t = '"two\nlines",x\r\nnext,row\r\n'
out = (len(t.splitlines()), rd(t), wr([['two\nlines', 'x']]))'''), '(3, [[\'two\\nlines\', \'x\'], [\'next\', \'row\']], \'"two\\nlines",x\\r\\n\')')),
 ('CsvFormat', 'CsvRules', 'LastRecordNoBreak', 'a,b\\r\\nc,d',
  'RFC 4180 says the last record may or may not have an ending line break, and csv.reader read a,b CRLF c,d with and without the final CRLF as the same two records, while an empty line between records was read as an empty record [].',
  (X(_PRE + r'''out = (rd('a,b\r\nc,d'), rd('a,b\r\nc,d\r\n'), rd('a,b\r\n\r\nc,d'))'''), "([['a', 'b'], ['c', 'd']], [['a', 'b'], ['c', 'd']], [['a', 'b'], [], ['c', 'd']])")),
 ('CsvFormat', 'CsvDialects', 'ExcelDialect', 'csv.excel',
  'A dialect is a set of formatting parameters; the default, csv.excel, has delimiter \',\', quotechar \'"\', doublequote True, skipinitialspace False, lineterminator CRLF and quoting QUOTE_MINIMAL (0), and the registered dialects are excel, excel-tab and unix.',
  (X(_PRE + r'''d = csv.excel
out = (d.delimiter, d.quotechar, d.doublequote, d.skipinitialspace, d.lineterminator, d.quoting, sorted(csv.list_dialects()))'''), '(\',\', \'"\', True, False, \'\\r\\n\', 0, [\'excel\', \'excel-tab\', \'unix\'])')),
 ('CsvFormat', 'CsvDialects', 'TabDelimited', "writer(f, delimiter='\\t')",
  "Passing delimiter='\\t' to csv.writer gave a tab-separated file; read back with the default delimiter the first line stayed one field and 'Hello, world!' broke at its comma, and read with delimiter='\\t' it gave the right fields, while the dialect excel-tab wrote the field with a tab inside in quotes.",
  (X(_PRE + r'''t = wr([['spam', 'eggs'], ['Hello, world!', 'ham']], delimiter='\t')
out = (t, rd(t), rd(t, delimiter='\t'), wr([['a', 'b c', 'd\te']], dialect='excel-tab'))'''), '(\'spam\\teggs\\r\\nHello, world!\\tham\\r\\n\', [[\'spam\\teggs\'], [\'Hello\', \' world!\\tham\']], [[\'spam\', \'eggs\'], [\'Hello, world!\', \'ham\']], \'a\\tb c\\t"d\\te"\\r\\n\')')),
 ('CsvFormat', 'CsvDialects', 'QuotingConstants', 'csv.QUOTE_MINIMAL',
  'The quoting constants are QUOTE_MINIMAL 0, QUOTE_ALL 1, QUOTE_NONNUMERIC 2, QUOTE_NONE 3, QUOTE_STRINGS 4 and QUOTE_NOTNULL 5; the row [\'a\', 1, 2.5, None, \'\', \'b,c\'] was written as a,1,2.5,,,"b,c" with the default, with every field quoted by QUOTE_ALL and with only the non-numbers quoted by QUOTE_NONNUMERIC.',
  (X(_PRE + r'''row = ['a', 1, 2.5, None, '', 'b,c']
out = ({n: getattr(csv, n) for n in sorted(dir(csv)) if n.startswith('QUOTE_')}, [wr([row], quoting=q) for q in (csv.QUOTE_MINIMAL, csv.QUOTE_ALL, csv.QUOTE_NONNUMERIC)])'''), '({\'QUOTE_ALL\': 1, \'QUOTE_MINIMAL\': 0, \'QUOTE_NONE\': 3, \'QUOTE_NONNUMERIC\': 2, \'QUOTE_NOTNULL\': 5, \'QUOTE_STRINGS\': 4}, [\'a,1,2.5,,,"b,c"\\r\\n\', \'"a","1","2.5","","","b,c"\\r\\n\', \'"a",1,2.5,"","","b,c"\\r\\n\'])')),
 ('CsvFormat', 'CsvEncoding', 'DefaultEncodingIsLocale', "open('x.csv')  # no encoding",
  'open() without an encoding uses the locale encoding: in a child interpreter with LC_ALL=C and UTF-8 mode off, open().encoding was ANSI_X3.4-1968 and sys.flags.utf8_mode 0; with -X utf8=1 it was utf-8 while locale.getencoding() still reported ANSI_X3.4-1968.',
  (X(_PRE + r'''env = dict(os.environ, LC_ALL='C', PYTHONCOERCECLOCALE='0'); env.pop('PYTHONUTF8', None)
code = 'import locale, sys, os; print(open(os.devnull).encoding, locale.getencoding(), sys.flags.utf8_mode)'
a = subprocess.run([sys.executable, '-X', 'utf8=0', '-c', code], capture_output=True, text=True, env=env).stdout.split()
b = subprocess.run([sys.executable, '-X', 'utf8=1', '-c', code], capture_output=True, text=True, env=env).stdout.split()
out = (a, b)'''), "(['ANSI_X3.4-1968', 'ANSI_X3.4-1968', '0'], ['utf-8', 'ANSI_X3.4-1968', '1'])")),
 ('CsvFormat', 'CsvEncoding', 'BomUtf8Sig', 'open(f, encoding="utf-8-sig")',
  "A file that Excel saves as CSV UTF-8 starts with the byte order mark EF BB BF; decoded as utf-8 the first field was \\ufeffName and a DictReader key was '\\ufeffName', decoded as utf-8-sig it was Name.",
  (X(_PRE + r'''raw = b'\xef\xbb\xbfName,Age\r\nA,1\r\n'
out = (rd(raw.decode('utf-8'))[0], rd(raw.decode('utf-8-sig'))[0], [k for k in csv.DictReader(io.StringIO(raw.decode('utf-8')))][0].keys().__repr__())'''), '([\'\\ufeffName\', \'Age\'], [\'Name\', \'Age\'], "dict_keys([\'\\\\ufeffName\', \'Age\'])")')),
 ('CsvFormat', 'CsvEncoding', 'Cp1252Mojibake', 'open(f, encoding="cp1252")',
  "Text decoded with the wrong encoding is garbled or refused: the UTF-8 bytes of Ad,Şehir / Çilek,İstanbul read as cp1252 gave Åžehir, Ã‡ilek and Ä°stanbul with no error, and read as cp1254 raised UnicodeDecodeError, a 'charmap' codec error for the byte 0x9e.",
  (X(_PRE + r'''raw = 'Ad,Şehir\r\nÇilek,İstanbul\r\n'.encode('utf-8')
def dec(e):
    try: return rd(raw.decode(e))
    except UnicodeDecodeError as x: return 'UnicodeDecodeError: ' + str(x)[:40]
out = (dec('utf-8'), dec('cp1252'), dec('cp1254'))'''), '([[\'Ad\', \'Şehir\'], [\'Çilek\', \'İstanbul\']], [[\'Ad\', \'Åžehir\'], [\'Ã‡ilek\', \'Ä°stanbul\']], "UnicodeDecodeError: \'charmap\' codec can\'t decode byte 0x9e i")')),
 ('CsvModule', 'ReaderObjects', 'ReaderEveryValueString', 'list(csv.reader(f))',
  "csv.reader returns every field as a str: the line 4/5/2035 13:34,Apples,73 gave ['4/5/2035 13:34', 'Apples', '73'], the types of the three fields were str, str, str and the number 73 had to be converted with int() to give 74.",
  (X(_PRE + r'''r = rd('4/5/2035 13:34,Apples,73\r\n')
out = (r, [type(c).__name__ for c in r[0]], int(r[0][2]) + 1)'''), "([['4/5/2035 13:34', 'Apples', '73']], ['str', 'str', 'str'], 74)")),
 ('CsvModule', 'ReaderObjects', 'ReaderUsedOnce', 'list(reader) twice',
  "A reader object is an iterator over rows, with no len() and no index: list() on a reader of two rows gave 2 rows and a second list() gave 0, hasattr(reader, '__len__') and hasattr(reader, '__getitem__') were both False and the type is named reader.",
  (X(_PRE + r'''reader = csv.reader(io.StringIO('a,b\r\nc,d\r\n', newline=''))
out = (len(list(reader)), len(list(reader)), hasattr(reader, '__len__'), hasattr(reader, '__getitem__'), type(reader).__name__)'''), "(2, 0, False, False, 'reader')")),
 ('CsvModule', 'ReaderObjects', 'LineNumVsRecords', 'reader.line_num',
  "reader.line_num counts the lines read from the source and not the records: for a header cell Name<LF>(first) the records ended at line_num 2, 3 and 4, and the book's test line_num != 1 kept 3 of 3 records, the header record included.",
  (X(_PRE + r'''reader = csv.reader(io.StringIO('"Name\n(first)",Age\r\nAlice,30\r\nBob,25\r\n', newline=''))
seen = [(row, reader.line_num) for row in reader]
r2 = csv.reader(io.StringIO('"Name\n(first)",Age\r\nAlice,30\r\nBob,25\r\n', newline=''))
book = [row for row in r2 if r2.line_num != 1]
out = (seen, len(book), book[0])'''), "([(['Name\\n(first)', 'Age'], 2), (['Alice', '30'], 3), (['Bob', '25'], 4)], 3, ['Name\\n(first)', 'Age'])")),
 ('CsvModule', 'ReaderObjects', 'LoopSavesMemory', 'for row in reader',
  'A for loop over the reader needs far less memory than list(reader): for 60,000 rows the peak traced by tracemalloc was more than 10 times higher for list(); both counted 60,000 rows.',
  (X(_PRE + r'''big = ''.join('%d,Apples,%d\r\n' % (i, i * 2) for i in range(60000))
def peak(f):
    s = io.StringIO(big, newline=''); tracemalloc.start(); n = f(s); p = tracemalloc.get_traced_memory()[1]; tracemalloc.stop(); return n, p
def as_list(s): return len(list(csv.reader(s)))
def as_loop(s):
    n = 0
    for row in csv.reader(s): n += 1
    return n
(n1, pl), (n2, pf) = peak(as_list), peak(as_loop)
out = (n1, n2, pl > 10 * pf)'''), '(60000, 60000, True)')),
 ('CsvModule', 'WriterObjects', 'WriterReturnsLength', 'writer.writerow(row)',
  'writerow() returns the number of characters written, and the three rows of the chapter returned 21, 32 and 16, for a text of 69 characters with 3 CRLF endings.',
  (X(_PRE + r'''s = io.StringIO(newline=''); w = csv.writer(s)
n = [w.writerow(r) for r in (['spam', 'eggs', 'bacon', 'ham'], ['Hello, world!', 'eggs', 'bacon', 'ham'], [1, 2, 3.141592, 4])]
out = (n, len(s.getvalue()), s.getvalue().count('\r\n'))'''), '([21, 32, 16], 69, 3)')),
 ('CsvModule', 'WriterObjects', 'WriterTypes', 'writerow([None, True, 1.0])',
  'The writer converts every value with str(): None became an empty field, True became True, 1.0 stayed 1.0, 10**20 and 1e-07 were written in full as 100000000000000000000 and 1e-07, a list became its repr in quotes, and the reader returned them all as strings; writerow(5) raised Error: iterable expected, not int.',
  (X(_PRE + r'''out = (wr([[None, True, 1.0, 10**20, 1e-07, 'É', ['x', 1]]]), rd(wr([[None, True, 1.0]])), err(lambda: csv.writer(io.StringIO()).writerow(5)))'''), '(\',True,1.0,100000000000000000000,1e-07,É,"[\\\'x\\\', 1]"\\r\\n\', [[\'\', \'True\', \'1.0\']], (\'Error\', \'iterable expected, not int\'))')),
 ('CsvModule', 'WriterObjects', 'WriterDoubleSpacing', "open(f, 'w')  # without newline=''",
  "On Windows a text file opened without newline='' translates LF to CRLF and the writer's CRLF becomes CR CR LF; reproduced with an io.TextIOWrapper asked for newline CRLF, the bytes were a,b CR CR LF against a,b CR LF with newline='', and csv.reader returned a second, empty, record after the row.",
  (X(_PRE + r'''def write_through(newline):
    b = io.BytesIO(); f = io.TextIOWrapper(b, encoding='utf-8', newline=newline); csv.writer(f).writerow(['a', 'b']); f.flush(); return b.getvalue()
win = write_through('\r\n')
out = (write_through(''), win, rd(win.decode()), [len(r) for r in rd(win.decode())])'''), "(b'a,b\\r\\n', b'a,b\\r\\r\\n', [['a', 'b'], []], [2, 0])")),
 ('CsvModule', 'DictReadersWriters', 'DictReaderFirstRowKeys', 'csv.DictReader(f)',
  "DictReader uses the first row as the keys and returns a dict per row, here {'Timestamp': '4/5/2025 13:34', 'Fruit': 'Apples', 'Quantity': '73'}; given fieldnames of its own, the header row became data and the first dict was {'time': 'Timestamp', 'name': 'Fruit', 'amount': 'Quantity'}.",
  (X(_PRE + r'''t = 'Timestamp,Fruit,Quantity\r\n4/5/2025 13:34,Apples,73\r\n'
d = list(csv.DictReader(io.StringIO(t, newline='')))
out = (d, type(d[0]).__name__, list(csv.DictReader(io.StringIO(t, newline=''), ['time', 'name', 'amount']))[0])'''), "([{'Timestamp': '4/5/2025 13:34', 'Fruit': 'Apples', 'Quantity': '73'}], 'dict', {'time': 'Timestamp', 'name': 'Fruit', 'amount': 'Quantity'})")),
 ('CsvModule', 'DictReadersWriters', 'RestkeyRestval', 'DictReader(f, restkey="extra")',
  "A row longer than the header put the extra values in a list under the key None, or under restkey='extra', and a row shorter than the header gave None for the missing keys, or the value of restval='?'.",
  (X(_PRE + r'''longer = list(csv.DictReader(io.StringIO('a,b\r\n1,2,3,4\r\n', newline='')))
longer_k = list(csv.DictReader(io.StringIO('a,b\r\n1,2,3,4\r\n', newline=''), restkey='extra'))
shorter = list(csv.DictReader(io.StringIO('a,b,c\r\n1\r\n', newline='')))
shorter_v = list(csv.DictReader(io.StringIO('a,b,c\r\n1\r\n', newline=''), restval='?'))
out = (longer, longer_k, shorter, shorter_v)'''), "([{'a': '1', 'b': '2', None: ['3', '4']}], [{'a': '1', 'b': '2', 'extra': ['3', '4']}], [{'a': '1', 'b': None, 'c': None}], [{'a': '1', 'b': '?', 'c': '?'}])")),
 ('CsvModule', 'DictReadersWriters', 'DictWriterExtraKey', 'DictWriter(f, fieldnames)',
  "DictWriter.writeheader() returned 10 and writerow() 6; a dict with a key that is not in fieldnames raised ValueError: dict contains fields not in fieldnames: 'Age', and extrasaction='ignore' dropped the key.",
  (X(_PRE + r'''s = io.StringIO(newline=''); w = csv.DictWriter(s, ['Name', 'Pet'])
h = w.writeheader(); n = w.writerow({'Name': 'Bob'})
e = err(lambda: w.writerow({'Name': 'x', 'Age': 3}))
i = io.StringIO(newline=''); w2 = csv.DictWriter(i, ['x'], extrasaction='ignore'); w2.writerow({'x': 1, 'y': 2})
out = (h, n, s.getvalue(), e, i.getvalue())'''), '(10, 6, \'Name,Pet\\r\\nBob,\\r\\n\', (\'ValueError\', "dict contains fields not in fieldnames: \'Age\'"), \'1\\r\\n\')')),
 ('CsvModule', 'CsvLimits', 'FieldSizeLimit', 'csv.field_size_limit()',
  'csv.field_size_limit() is 131072 characters; a field of 131073 characters raised Error: field larger than field limit (131072) and a field of exactly 131072 characters was read.',
  (X(_PRE + r'''lim = csv.field_size_limit()
big = 'a' * (lim + 1)
out = (lim, err(lambda: rd(big)), len(rd('a' * lim)[0][0]))'''), "(131072, ('Error', 'field larger than field limit (131072)'), 131072)")),
 ('CsvModule', 'CsvLimits', 'QuoteStringsNotNull', 'quoting=csv.QUOTE_NOTNULL',
  'QUOTE_NOTNULL and QUOTE_STRINGS (new in Python 3.12) separate None from the empty string: reading "a",,"",3 gave \'\' for the unquoted empty field by default, None with QUOTE_NOTNULL, and with QUOTE_STRINGS None and the unquoted 3 as the float 3.0; writing [\'a\', None, \'\', 3] with QUOTE_STRINGS gave "a",,"",3.',
  (X(_PRE + r'''t = '"a",,"",3\r\n'
out = (rd(t), rd(t, quoting=csv.QUOTE_NOTNULL), rd(t, quoting=csv.QUOTE_STRINGS), wr([['a', None, '', 3]], quoting=csv.QUOTE_STRINGS), wr([['a', None, '', 3]], quoting=csv.QUOTE_NOTNULL))'''), '([[\'a\', \'\', \'\', \'3\']], [[\'a\', None, \'\', \'3\']], [[\'a\', None, \'\', 3.0]], \'"a",,"",3\\r\\n\', \'"a",,"","3"\\r\\n\')')),
 ('JsonFormat', 'JsonSyntax', 'SixValueTypes', 'json.loads(text)',
  "JSON has six value types (string, number, object, array, true and false, null); json.loads of the chapter's Alice text gave a dict with str, int, NoneType, bool, dict and list values, equal to the original Python data, and the compact text is 248 characters.",
  (X(_PRE + r'''d = json.loads(json.dumps(A))
out = ([(k, type(v).__name__) for k, v in d.items()], d == A, json.dumps(A) == json.dumps(json.loads(json.dumps(A))), len(json.dumps(A)))'''), "([('name', 'str'), ('age', 'int'), ('car', 'NoneType'), ('programmer', 'bool'), ('address', 'dict'), ('phone', 'list')], True, True, 248)")),
 ('JsonFormat', 'JsonSyntax', 'TrailingCommaRefused', '["spam", "eggs",]',
  'JSON does not allow a trailing comma, single quotes or comments: json.loads of ["spam", "eggs",] raised JSONDecodeError \'Illegal trailing comma before end of array\' at line 1 column 16 (pos 15), the same for an object, "{\'a\': 1}" gave \'Expecting property name enclosed in double quotes\' and a // comment gave \'Extra data\'.',
  (X(_PRE + r'''def msg(t):
    try: json.loads(t); return 'accepted'
    except json.JSONDecodeError as e: return (e.msg, e.lineno, e.colno, e.pos)
out = (msg('["spam", "eggs"]'), msg('["spam", "eggs",]'), msg('{"a": 1,}'), msg("{'a': 1}"), msg('{"a": 1} // note'))'''), "('accepted', ('Illegal trailing comma before end of array', 1, 16, 15), ('Illegal trailing comma before end of object', 1, 8, 7), ('Expecting property name enclosed in double quotes', 1, 2, 1), ('Extra data', 1, 10, 9))")),
 ('JsonFormat', 'JsonSyntax', 'RawNewlineInString', '"a<LF>b"',
  "A raw line feed inside a JSON string is refused with 'Invalid control character at', and so is a raw tab; the escape \\n is accepted, and json.loads(..., strict=False) accepts the tab.",
  (X(_PRE + r'''def msg(t, **k):
    try: return json.loads(t, **k)
    except json.JSONDecodeError as e: return e.msg
out = (msg('"a\nb"'), msg('"a\\nb"'), msg('"a\tb"'), msg('"a\tb"', strict=False))'''), "('Invalid control character at', 'a\\nb', 'Invalid control character at', 'a\\tb')")),
 ('JsonFormat', 'JsonSyntax', 'NaNAcceptedByPython', 'json.loads("[NaN]")',
  "Python's json accepts what RFC 8259 does not allow: json.loads('[NaN, Infinity, -Infinity]') returned [nan, inf, -inf], dumps wrote [NaN, Infinity] and allow_nan=False raised ValueError: Out of range float values are not JSON compliant.",
  (X(_PRE + r'''out = (json.loads('[NaN, Infinity, -Infinity]'), json.dumps([float('nan'), float('inf')]), err(lambda: json.dumps(float('nan'), allow_nan=False)))'''), "([nan, inf, -inf], '[NaN, Infinity]', ('ValueError', 'Out of range float values are not JSON compliant: nan'))")),
 ('JsonFormat', 'JsonTypes', 'TupleBecomesList', 'json.dumps((1, 2))',
  "JSON has no tuple: json.dumps((1, 2)) is [1, 2] and loads gives a list, so the round trip of {'t': (1, 2)} is not equal to the original, and a set raised TypeError: Object of type set is not JSON serializable.",
  (X(_PRE + r'''out = (json.dumps((1, 2)), json.loads(json.dumps({'t': (1, 2)})), json.loads(json.dumps({'t': (1, 2)})) == {'t': (1, 2)}, err(lambda: json.dumps({1, 2})))'''), "('[1, 2]', {'t': [1, 2]}, False, ('TypeError', 'Object of type set is not JSON serializable'))")),
 ('JsonFormat', 'JsonTypes', 'KeysBecomeStrings', 'json.dumps({1: "a"})',
  'JSON object keys are strings: {1: \'a\', 2.5: \'b\', None: \'c\', True: \'d\'} was written with the keys "1" (True replaced the value of 1), "2.5" and "null", and a tuple key raised TypeError: keys must be str, int, float, bool or None, not tuple.',
  (X(_PRE + r'''s = json.dumps({1: 'a', 2.5: 'b', None: 'c', True: 'd'})
out = (s, list(json.loads(s)), err(lambda: json.dumps({(1, 2): 'x'})))'''), '(\'{"1": "d", "2.5": "b", "null": "c"}\', [\'1\', \'2.5\', \'null\'], (\'TypeError\', \'keys must be str, int, float, bool or None, not tuple\'))')),
 ('JsonFormat', 'JsonTypes', 'UnsupportedTypesRaise', 'json.dumps(datetime)',
  "datetime, Decimal, bytes and complex values raise TypeError: Object of type ... is not JSON serializable, and default=str turned the datetime into '2035-04-05 13:34:00' and the Decimal into '1.5'.",
  (X(_PRE + r'''import datetime, decimal
out = [err(lambda v=v: json.dumps(v))[1] for v in (datetime.datetime(2035, 4, 5, 13, 34), decimal.Decimal('1.5'), b'x', 1j)] + [json.dumps({'when': datetime.datetime(2035, 4, 5, 13, 34), 'x': decimal.Decimal('1.5')}, default=str)]'''), '[\'Object of type datetime is not JSON serializable\', \'Object of type Decimal is not JSON serializable\', \'Object of type bytes is not JSON serializable\', \'Object of type complex is not JSON serializable\', \'{"when": "2035-04-05 13:34:00", "x": "1.5"}\']')),
 ('JsonFormat', 'JsonFiles', 'IndentAndSeparators', 'json.dumps(data, indent=2)',
  "indent=2 pretty-prints the Alice data in 21 lines and 326 characters, and loads reads it back equal; separators=(',', ':') gives 225 characters, indent='\\t' tabs, indent=0 only line breaks, and sort_keys=True starts with address, age, car.",
  (X(_PRE + r'''p = json.dumps(A, indent=2)
out = (len(p.split('\n')), len(p), json.loads(p) == A, len(json.dumps(A, separators=(',', ':'))), json.dumps({'a': [1]}, indent='\t'), json.dumps({'a': [1]}, indent=0), list(json.loads(json.dumps(A, sort_keys=True)))[:3])'''), '(21, 326, True, 225, \'{\\n\\t"a": [\\n\\t\\t1\\n\\t]\\n}\', \'{\\n"a": [\\n1\\n]\\n}\', [\'address\', \'age\', \'car\'])')),
 ('JsonFormat', 'JsonFiles', 'EnsureAscii', 'json.dumps(s, ensure_ascii=False)',
  'By default json.dumps writes non-ASCII text as \\u escapes (M\\u00fcller, \\u0130stanbul, a surrogate pair for U+1F600), ensure_ascii=False writes the characters, and loads turns the surrogate pair back into one character.',
  (X(_PRE + r'''d = {'name': 'Müller', 'city': 'İstanbul'}
out = (json.dumps(d), json.dumps(d, ensure_ascii=False), json.dumps('\U0001f600'), json.loads('"\\ud83d\\ude00"') == '\U0001f600')'''), '(\'{"name": "M\\\\u00fcller", "city": "\\\\u0130stanbul"}\', \'{"name": "Müller", "city": "İstanbul"}\', \'"\\\\ud83d\\\\ude00"\', True)')),
 ('JsonFormat', 'JsonFiles', 'FileRoundTrip', 'json.dump(data, f)',
  "json.dump(data, f) writes a file and returns None and json.load(f) reads it back, from a text file or from one opened in 'rb'; json.loads given a file object raised TypeError: the JSON object must be str, bytes or bytearray, not TextIOWrapper, and json.dump to a file opened 'wb' raised TypeError: a bytes-like object is required, not 'str'.",
  (X(_PRE + r'''d = tempfile.mkdtemp(); p = os.path.join(d, 'person.json')
with open(p, 'w', encoding='utf-8') as f: r = json.dump(A, f, indent=2, ensure_ascii=False)
with open(p, encoding='utf-8') as f: back = json.load(f)
with open(p, 'rb') as f: back2 = json.load(f)
out = (r, back == A, back2 == A, err(lambda: json.loads(open(p))), err(lambda: json.dump(A, open(os.path.join(d, 'x'), 'wb'))))'''), '(None, True, True, (\'TypeError\', \'the JSON object must be str, bytes or bytearray, not TextIOWrapper\'), (\'TypeError\', "a bytes-like object is required, not \'str\'"))')),
 ('JsonFormat', 'JsonFiles', 'BomHandling', 'json.loads(b"\\xef\\xbb\\xbf[1]")',
  'json.loads of bytes that start with a byte order mark returned [1] because the encoding is detected as utf-8-sig, but a str that starts with U+FEFF raised JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig), and UTF-16 bytes were detected too.',
  (X(_PRE + r'''out = (json.loads(b'\xef\xbb\xbf[1]'), json.detect_encoding(b'\xef\xbb\xbf[1]'), err(lambda: json.loads('﻿[1]')), json.loads('["é"]'.encode('utf-16')))'''), "([1], 'utf-8-sig', ('JSONDecodeError', 'Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)'), ['é'])")),
 ('JsonFormat', 'JsonFiles', 'SerializationErrorNotes', 'TypeError.__notes__',
  'Python 3.14 adds notes to the TypeError of a serialization error: for {\'a\': [1, {2, 3}]} the notes were \'when serializing list item 1\' and "when serializing dict item \'a\'", and the error for a tuple key has no notes.',
  (X(_PRE + r'''def notes(v):
    try: json.dumps(v)
    except TypeError as e: return (str(e), getattr(e, '__notes__', None))
out = (notes({'a': [1, {2, 3}]}), notes({'a': 1, (1, 2): 3}))'''), '((\'Object of type set is not JSON serializable\', [\'when serializing list item 1\', "when serializing dict item \'a\'"]), (\'keys must be str, int, float, bool or None, not tuple\', None))')),
 ('XmlFormat', 'XmlSyntax', 'CaseSensitiveTags', '<A></a>',
  'XML tag names are case-sensitive and every tag must be closed in order: <A></a> raised ParseError: mismatched tag at line 1 column 5, <a><b></a> raised the same error, and <Person><NAME>x</NAME></Person> parsed because the cases matched.',
  (X(_PRE + r'''def p(t):
    try: return ET.tostring(ET.fromstring(t), encoding='unicode')
    except ET.ParseError as e: return 'ParseError: ' + str(e)
out = (p('<A></a>'), p('<Person><NAME>x</NAME></Person>'), p('<a><b></a>'), p('<a><b></a></b>'))'''), "('ParseError: mismatched tag: line 1, column 5', '<Person><NAME>x</NAME></Person>', 'ParseError: mismatched tag: line 1, column 8', 'ParseError: mismatched tag: line 1, column 8')")),
 ('XmlFormat', 'XmlSyntax', 'AttributeQuotesRequired', "<a b='1'>",
  'An XML attribute needs a value in quotes, single or double: <a b=\'1\'/> parsed and was written back as <a b="1" />, while <a b=1/> and <a b/> (allowed in HTML) raised ParseError: not well-formed (invalid token), and a repeated attribute raised duplicate attribute.',
  (X(_PRE + r'''def p(t):
    try: return ET.tostring(ET.fromstring(t), encoding='unicode')
    except ET.ParseError as e: return 'ParseError: ' + str(e)
out = (p("<a b='1'/>"), p('<a b=1/>'), p('<a b/>'), p('<a b="1" b="2"/>'))'''), '(\'<a b="1" />\', \'ParseError: not well-formed (invalid token): line 1, column 5\', \'ParseError: not well-formed (invalid token): line 1, column 4\', \'ParseError: duplicate attribute: line 1, column 9\')')),
 ('XmlFormat', 'XmlSyntax', 'SingleRootRequired', '<a/><b/>',
  'An XML document has exactly one root element: <a/><b/> raised ParseError: junk after document element, so did text after the root, a comment before or after the root was allowed, and empty input raised no element found.',
  (X(_PRE + r'''def p(t):
    try: return ET.tostring(ET.fromstring(t), encoding='unicode')
    except ET.ParseError as e: return 'ParseError: ' + str(e)
out = (p('<a/><b/>'), p('<!-- c --><a/>'), p('<a/><!-- c -->'), p(''), p('<a/>junk'))'''), "('ParseError: junk after document element: line 1, column 4', '<a />', '<a />', 'ParseError: no element found: line 1, column 0', 'ParseError: junk after document element: line 1, column 4')")),
 ('XmlFormat', 'XmlSyntax', 'EscapesRequired', '&amp; &lt;',
  'A lone & or < in XML text is an error (not well-formed, invalid token) and must be written &amp; or &lt;, which parse back to & and <; an HTML entity such as &nbsp; is undefined in XML, and a CDATA section holds 1 < 2 & 3 as text.',
  (X(_PRE + r'''def p(t):
    try: return ET.fromstring(t).text
    except ET.ParseError as e: return 'ParseError: ' + str(e)
out = (p('<a>fish & chips</a>'), p('<a>1 < 2</a>'), p('<a>fish &amp; chips &lt; 5</a>'), p('<a>&nbsp;</a>'), p('<a><![CDATA[1 < 2 & 3]]></a>'))'''), "('ParseError: not well-formed (invalid token): line 1, column 9', 'ParseError: not well-formed (invalid token): line 1, column 6', 'fish & chips < 5', 'ParseError: undefined entity: line 1, column 3', '1 < 2 & 3')")),
 ('XmlFormat', 'XmlSyntax', 'WellFormedNotValid', '<person><banana/></person>',
  'ElementTree checks well-formedness and not validity: a person with a banana child and a name child parsed with both children, while lxml with a DTD that allows only a name child answered False for that document and True for a document with a name only; xml.etree.ElementTree has no validate().',
  (X(_PRE + r'''r = ET.fromstring('<person><banana>1</banana><name/></person>')
import lxml.etree as L
dtd = L.DTD(io.StringIO('<!ELEMENT person (name)><!ELEMENT name (#PCDATA)>'))
out = ([c.tag for c in r], dtd.validate(L.fromstring('<person><banana>1</banana><name/></person>')), dtd.validate(L.fromstring('<person><name>x</name></person>')), hasattr(ET, 'validate'))'''), "(['banana', 'name'], False, True, False)")),
 ('XmlFormat', 'XmlNamespaces', 'NamespaceClarkName', '{uri}local',
  'ElementTree names a namespaced element or attribute {uri}local: the b of <x:b x:c="1"/> with x bound to urn:x had the tag {urn:x}b and the attribute {urn:x}c, equal to ET.QName(\'urn:x\', \'b\').text, and was written back with the prefix ns0.',
  (X(_PRE + r'''r = ET.fromstring('<p xmlns:x="urn:x"><x:b x:c="1"/></p>')
out = (r[0].tag, r[0].attrib, ET.tostring(r, encoding='unicode'), ET.QName('urn:x', 'b').text)'''), '(\'{urn:x}b\', {\'{urn:x}c\': \'1\'}, \'<p xmlns:ns0="urn:x"><ns0:b ns0:c="1" /></p>\', \'{urn:x}b\')')),
 ('XmlFormat', 'XmlNamespaces', 'XsiNilNotUnderstood', 'xsi:nil="true"',
  "xsi:nil is an attribute of the XML Schema instance namespace and ElementTree does not interpret it: elements with xsi:nil true, false and true gave the attribute values under the full name {http://www.w3.org/2001/XMLSchema-instance}nil, the text of an element with nil true and content stayed 'not empty', and a document that uses the prefix without declaring it raised ParseError: unbound prefix.",
  (X(_PRE + r'''r = ET.fromstring('<p ' + NS + '><a xsi:nil="true"/><b xsi:nil="false">text</b><c xsi:nil="true">not empty</c></p>')
nil = '{http://www.w3.org/2001/XMLSchema-instance}nil'
out = ([(e.tag, e.attrib.get(nil), e.text) for e in r], ET.tostring(r, encoding='unicode'), err(lambda: ET.fromstring('<a xsi:nil="true"/>')))'''), '([(\'a\', \'true\', None), (\'b\', \'false\', \'text\'), (\'c\', \'true\', \'not empty\')], \'<p xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><a xsi:nil="true" /><b xsi:nil="false">text</b><c xsi:nil="true">not empty</c></p>\', (\'ParseError\', \'unbound prefix: line 1, column 0\'))')),
 ('XmlFormat', 'XmlSecurity', 'BillionLaughsLimit', '<!ENTITY lol9 "&lol8;&lol8;...">',
  "A 760-byte document of 10 levels of entities that would expand to 3,000,000,000 characters was refused by ElementTree with ParseError: limit on input amplification factor (from DTD and entities) breached, while a small entity document parsed to 'hellohello'.",
  (X(_PRE + r'''ents = ''.join('<!ENTITY lol%d "%s">' % (i, ('&lol;' if i == 1 else '&lol%d;' % (i - 1)) * 10) for i in range(1, 10))
doc = '<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol">' + ents + ']><lolz>&lol9;</lolz>'
small = '<?xml version="1.0"?><!DOCTYPE a [<!ENTITY e "hello">]><a>&e;&e;</a>'
out = (len(doc), 3 * 10 ** 9, err(lambda: ET.fromstring(doc)), ET.fromstring(small).text)'''), "(760, 3000000000, ('ParseError', 'limit on input amplification factor (from DTD and entities) breached: line 1, column 747'), 'hellohello')")),
 ('XmlFormat', 'XmlSecurity', 'ExternalEntityNotFetched', '<!ENTITY x SYSTEM "file:///etc/hostname">',
  'ElementTree did not read a local file named by an external entity: a document with <!ENTITY x SYSTEM "file://...secret.txt"> raised ParseError: undefined entity &x;, and the text of the file did not appear in the error.',
  (X(_PRE + r'''p = os.path.join(tempfile.mkdtemp(), 'secret.txt'); open(p, 'w').write('TOPSECRET')
doc = '<?xml version="1.0"?><!DOCTYPE a [<!ENTITY x SYSTEM "file://' + p + '">]><a>&x;</a>'
out = (err(lambda: ET.fromstring(doc)), 'TOPSECRET' in str(err(lambda: ET.fromstring(doc))))'''), "(('ParseError', 'undefined entity &x;: line 1, column 94'), False)")),
 ('XmlFormat', 'XmlSecurity', 'DefusedxmlForbids', 'defusedxml.ElementTree.fromstring',
  'defusedxml.ElementTree.fromstring raised EntitiesForbidden for a document with an entity, parsed an ordinary document, raised DTDForbidden with forbid_dtd=True, and both exceptions are subclasses of ValueError.',
  (X(_PRE + r'''import defusedxml.ElementTree as D
from defusedxml import EntitiesForbidden, DTDForbidden
small = '<?xml version="1.0"?><!DOCTYPE a [<!ENTITY e "hello">]><a>&e;</a>'
r1 = err(lambda: D.fromstring(small)); r2 = err(lambda: D.fromstring('<a>1</a>').text); r3 = err(lambda: D.fromstring(small, forbid_dtd=True))
out = (r1[0], r2, r3[0], issubclass(EntitiesForbidden, ValueError), issubclass(DTDForbidden, ValueError))'''), "('EntitiesForbidden', ('ok', '1'), 'DTDForbidden', True, True)")),
 ('XmlFormat', 'XmlSecurity', 'XmltodictEntitiesDisabled', 'xmltodict.parse(entity document)',
  "xmltodict 1.0.4 refuses every entity: parse of a document with an internal entity raised ValueError: entities are disabled, while a plain document parsed to {'a': '1'}; the version Appendix A pins, 0.13.0, parsed the entity.",
  (X(_PRE + r'''import xmltodict, importlib.metadata as m
small = '<?xml version="1.0"?><!DOCTYPE a [<!ENTITY e "hello">]><a>&e;</a>'
out = (m.version('xmltodict'), err(lambda: xmltodict.parse(small)), xmltodict.parse('<a>1</a>'))'''), "('1.0.4', ('ValueError', 'entities are disabled'), {'a': '1'})")),
 ('XmlLibraries', 'ElementTreeReading', 'RootTagAndChildren', 'root = ET.fromstring(xml_string)',
  "ET.fromstring() returns the root Element: its tag was person, list(root) gave the 6 children name, age, programmer, car, address and phone, root[0].text was 'Alice Doe', root[4][0] was the street element with the text '100 Larkin St.', a slice gave [age, programmer] and root[9] raised IndexError: child index out of range.",
  (X(_PRE + r'''root = ET.fromstring(XS)
out = (root.tag, [c.tag for c in root], len(root), root[0].text, root[4][0].tag, root[4][0].text, type(root).__name__, [c.tag for c in root[1:3]], err(lambda: root[9]))'''), "('person', ['name', 'age', 'programmer', 'car', 'address', 'phone'], 6, 'Alice Doe', 'street', '100 Larkin St.', 'Element', ['age', 'programmer'], ('IndexError', 'child index out of range'))")),
 ('XmlLibraries', 'ElementTreeReading', 'TextNoneOrString', 'elem.text',
  "The text of an element is a str or None: age had the str '30', the self-closing car and the empty pair had None, and an element holding one space had ' ', so '<car/>' and '<car></car>' are the same to the parser.",
  (X(_PRE + r'''root = ET.fromstring(XS)
out = (root[1].text, type(root[1].text).__name__, root[3].text, root[3].text is None, root[4].text, ET.fromstring('<a></a>').text, ET.fromstring('<a> </a>').text)'''), "('30', 'str', None, True, None, None, ' ')")),
 ('XmlLibraries', 'ElementTreeReading', 'ParentTextIsWhitespace', 'ET.parse("my_data.xml")',
  "In a pretty-printed file the text of an element that holds only other elements is the whitespace between the tags: address had '\\n        ', root.text was '\\n    ', name had the tail '\\n    ', and only car, with no content, had None; text.strip() or None gives the None the chapter prints.",
  (X(_PRE + r'''pretty = '<person>\n    <name>Alice Doe</name>\n    <address>\n        <street>100 Larkin St.</street>\n    </address>\n    <car/>\n</person>\n'
root = ET.parse(io.StringIO(pretty)).getroot()
out = ([(c.tag, c.text) for c in root], root.text, root[0].tail, [(c.tag, (c.text or '').strip() or None) for c in root])'''), "([('name', 'Alice Doe'), ('address', '\\n        '), ('car', None)], '\\n    ', '\\n    ', [('name', 'Alice Doe'), ('address', None), ('car', None)])")),
 ('XmlLibraries', 'ElementTreeReading', 'IterDocumentOrder', 'root.iter("number")',
  "iter() walks the element and its descendants in document order, root first: 16 elements for the Alice document against 6 children, the numbers were ['415-555-7890', '415-555-1234'], and the first element returned was the root itself.",
  (X(_PRE + r'''root = ET.fromstring(XS)
out = ([e.tag for e in root.iter()], [e.text for e in root.iter('number')], len(list(root)), len(list(root.iter())), root.iter().__next__() is root)'''), "(['person', 'name', 'age', 'programmer', 'car', 'address', 'street', 'city', 'zip', 'phone', 'phoneEntry', 'type', 'number', 'phoneEntry', 'type', 'number'], ['415-555-7890', '415-555-1234'], 6, 16, True)")),
 ('XmlLibraries', 'ElementTreeReading', 'FindAndXPathSubset', 'root.findall(".//number")',
  "find(), findall() and findtext() take a limited XPath: find('name').text was 'Alice Doe', findall('.//number') gave the two numbers, findtext('address/zip') gave '94102', find('nothing') returned None and .text on it raised AttributeError, and an Element has no xpath() method.",
  (X(_PRE + r'''root = ET.fromstring(XS)
out = (root.find('name').text, [e.text for e in root.findall('.//number')], root.find('nothing'), err(lambda: root.find('nothing').text), root.findtext('address/zip'), hasattr(root, 'xpath'))'''), '(\'Alice Doe\', [\'415-555-7890\', \'415-555-1234\'], None, (\'AttributeError\', "\'NoneType\' object has no attribute \'text\'"), \'94102\', False)')),
 ('XmlLibraries', 'ElementTreeReading', 'ElementTruthDeprecated', 'if elem:',
  'The truth value of an Element is its number of children and testing it raises a DeprecationWarning (since Python 3.12): bool of an empty element was False and of an element with a child True, so a found element must be tested with is not None.',
  (X(_PRE + r'''empty = ET.Element('x'); full = ET.fromstring('<a><b/></a>')
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); v = (bool(empty), bool(full))
out = (v, sorted({x.category.__name__ for x in w}), empty is not None)'''), "((False, True), ['DeprecationWarning'], True)")),
 ('XmlLibraries', 'ElementTreeWriting', 'SubElementAndSet', 'ET.SubElement(root, "name")',
  'Element, SubElement and set build a tree: ET.tostring(root) returned bytes, encoding=\'unicode\' returned the str <person><name>Alice Doe</name><car xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" /></person>, and the namespace attribute was written as a plain attribute.',
  (X(_PRE + r'''root = ET.Element('person'); n = ET.SubElement(root, 'name'); n.text = 'Alice Doe'
car = ET.SubElement(root, 'car'); car.set('xsi:nil', 'true'); car.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
out = (ET.tostring(root), ET.tostring(root, encoding='unicode'), err(lambda: ET.tostring(ET.fromstring('<a>1</a>'), encoding='unicode')))'''), '(b\'<person><name>Alice Doe</name><car xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" /></person>\', \'<person><name>Alice Doe</name><car xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" /></person>\', (\'ok\', \'<a>1</a>\'))')),
 ('XmlLibraries', 'ElementTreeWriting', 'TostringSpaceBeforeSlash', 'ET.tostring(elem)',
  "ET.tostring writes an empty element as <b /> with a space, <b></b> with short_empty_elements=False, writes an XML declaration only with xml_declaration=True, and with the default encoding turns M\\u00fcller into M&#252;ller while encoding='utf-8' keeps the bytes.",
  (X(_PRE + r'''e = ET.fromstring('<a><b/></a>')
out = (ET.tostring(e), ET.tostring(e, short_empty_elements=False), ET.tostring(e, encoding='utf-8'), ET.tostring(e, encoding='utf-8', xml_declaration=True), ET.tostring(ET.fromstring('<u>Müller</u>')), ET.tostring(ET.fromstring('<u>Müller</u>'), encoding='utf-8'))'''), '(b\'<a><b /></a>\', b\'<a><b></b></a>\', b\'<a><b /></a>\', b"<?xml version=\'1.0\' encoding=\'utf-8\'?>\\n<a><b /></a>", b\'<u>M&#252;ller</u>\', b\'<u>M\\xc3\\xbcller</u>\')')),
 ('XmlLibraries', 'ElementTreeWriting', 'IndentPrettyPrint', 'ET.indent(tree)',
  "ET.indent(tree) (Python 3.9) adds whitespace in place: <a><b>x</b><c><d>y</d></c></a> became a text of 5 lines indented by 2 spaces, and the whitespace was stored as the text of a ('\\n  ') and the tail of b.",
  (X(_PRE + r'''root = ET.fromstring('<a><b>x</b><c><d>y</d></c></a>')
ET.indent(root)
out = (ET.tostring(root, encoding='unicode'), root.text, root[0].tail)'''), "('<a>\\n  <b>x</b>\\n  <c>\\n    <d>y</d>\\n  </c>\\n</a>', '\\n  ', '\\n  ')")),
 ('XmlLibraries', 'XmltodictLibrary', 'ParseGivesStrings', 'xmltodict.parse(xml_string)',
  "xmltodict.parse() returns a dict of dicts and every value is a str: age was '30', programmer was 'true', car was {'@xsi:nil': 'true', '@xmlns:xsi': ...} and not None, and address was a dict of three strings.",
  (X(_PRE + r'''import xmltodict
d = xmltodict.parse(XS)
out = (type(d).__name__, d['person']['age'], type(d['person']['age']).__name__, d['person']['programmer'], d['person']['car'], d['person']['address'])'''), "('dict', '30', 'str', 'true', {'@xsi:nil': 'true', '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'}, {'street': '100 Larkin St.', 'city': 'San Francisco', 'zip': '94102'})")),
 ('XmlLibraries', 'XmltodictLibrary', 'OneEntryDictTwoList', "phone': {'phoneEntry': [...]}",
  "xmltodict gives a dict for one child element and a list for two: phoneEntry was a dict with one entry and a list with two, force_list=('e',) made the single one a list, and an element with an attribute and text gave {'@href': 'x', '#text': 'link'}.",
  (X(_PRE + r'''import xmltodict
one = xmltodict.parse('<p><e><t>m</t></e></p>'); two = xmltodict.parse('<p><e><t>m</t></e><e><t>w</t></e></p>')
out = (type(one['p']['e']).__name__, type(two['p']['e']).__name__, xmltodict.parse('<p><e><t>m</t></e></p>', force_list=('e',))['p']['e'], xmltodict.parse('<a href="x">link</a>'), xmltodict.parse('<a href="x"/>'))'''), "('dict', 'list', [{'t': 'm'}], {'a': {'@href': 'x', '#text': 'link'}}, {'a': {'@href': 'x'}})")),
 ('XmlLibraries', 'XmltodictLibrary', 'UnparseRoundTrip', 'xmltodict.unparse(data)',
  'xmltodict.unparse() writes a dict back to XML with an XML declaration: parse(unparse(d)) equalled d for the Alice data, pretty=True indented with tabs, and a dict with two roots raised ValueError: Document must have exactly one root.',
  (X(_PRE + r'''import xmltodict
d = xmltodict.parse(XS)
u = xmltodict.unparse(d)
out = (u[:40], xmltodict.parse(u) == d, xmltodict.unparse({'a': {'@id': '1', 'b': ['x', 'y']}}, pretty=True), err(lambda: xmltodict.unparse({'a': 1, 'b': 2})))'''), '(\'<?xml version="1.0" encoding="utf-8"?>\\n<\', True, \'<?xml version="1.0" encoding="utf-8"?>\\n<a id="1">\\n\\t<b>x</b>\\n\\t<b>y</b>\\n</a>\', (\'ValueError\', \'Document must have exactly one root.\'))')),
 ('XmlLibraries', 'OtherParsers', 'MinidomSameAnswer', 'xml.dom.minidom.parseString',
  'The DOM of xml.dom.minidom gave the same two numbers as ElementTree, with firstChild.data instead of .text, a documentElement named person and node types such as ELEMENT_NODE (1).',
  (X(_PRE + r'''from xml.dom import minidom
dom = minidom.parseString(XS)
a = [n.firstChild.data for n in dom.getElementsByTagName('number')]
b = [e.text for e in ET.fromstring(XS).iter('number')]
out = (a, a == b, dom.documentElement.tagName, dom.firstChild.nodeType, dom.firstChild.nodeType == dom.ELEMENT_NODE)'''), "(['415-555-7890', '415-555-1234'], True, 'person', 1, True)")),
 ('XmlLibraries', 'OtherParsers', 'IterparseClear', 'ET.iterparse(f, events=("end",))',
  'iterparse reads a document as a stream of events: summing 20,000 items gave 199,990,000 with and without clear(), and without clear() the peak memory traced was more than 1.5 times higher (5.7 MB against 2.3 MB in one run).',
  (X(_PRE + r'''doc = '<r>' + ''.join('<i><q>%d</q></i>' % i for i in range(20000)) + '</r>'
def total(clear):
    tracemalloc.start(); s = 0
    for ev, e in ET.iterparse(io.BytesIO(doc.encode()), events=('end',)):
        if e.tag == 'i':
            s += int(e.find('q').text)
            if clear: e.clear()
    p = tracemalloc.get_traced_memory()[1]; tracemalloc.stop(); return s, p
a = total(True); b = total(False)
out = (a[0], a[0] == b[0], b[1] > 1.5 * a[1])'''), '(199990000, True, True)')),
 ('BookAndPractice', 'ChapterAccuracy', 'CurlyQuoteBreaksLiteral', 'xmlns:xsi="..."”/>',
  "The chapter's two xml_string listings end the xsi namespace with a curly quotation mark: the text raised ParseError: unclosed token, the straight-quoted text parsed, and json_string wrapped over two lines inside its quotes raised JSONDecodeError: Invalid control character and parsed once the line break was removed.",
  (X(_PRE + r'''good = '<a xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>'
bad = good.replace('instance"', 'instance”')
wrapped = '{"a": "b' + '\n' + 'c"}'
out = (err(lambda: ET.fromstring(bad)), err(lambda: ET.fromstring(good))[0], err(lambda: json.loads(wrapped)), json.loads(wrapped.replace('\n', '')))'''), "(('ParseError', 'unclosed token: line 1, column 0'), 'ok', ('JSONDecodeError', 'Invalid control character at: line 1 column 9 (char 8)'), {'a': 'bc'})")),
 ('BookAndPractice', 'ChapterAccuracy', 'PrintedNoneVsWhitespace', 'address -- None',
  "The chapter prints None for the text of address and phone, which holds for a compact document and not for a pretty-printed one: for the pretty text the loop gave ('address', '\\n    ') and for the compact text ('address', None).",
  (X(_PRE + r'''pretty = '<person>\n  <car/>\n  <address>\n    <street>x</street>\n  </address>\n</person>'
compact = pretty.replace('\n', '').replace('  ', '')
t = lambda s: [(c.tag, c.text) for c in ET.fromstring(s)]
out = (t(pretty), t(compact))'''), "([('car', None), ('address', '\\n    ')], [('car', None), ('address', None)])")),
 ('BookAndPractice', 'Project13', 'SkipHeaderWithNext', 'next(reader)',
  "next(reader) reads and drops the header record, and next(reader, None) does it safely: for h1,h2 / A,1 / B,2 the first was ['h1', 'h2'] and the rest [['A', '1'], ['B', '2']], and for empty input next(reader, 'empty') gave 'empty' while next(reader) raised StopIteration.",
  (X(_PRE + r'''t = 'h1,h2\r\nA,1\r\nB,2\r\n'
r = csv.reader(io.StringIO(t, newline='')); first = next(r); rest = list(r)
e = csv.reader(io.StringIO('', newline=''))
out = (first, rest, next(e, 'empty'), err(lambda: next(csv.reader(io.StringIO('', newline='')))))'''), "(['h1', 'h2'], [['A', '1'], ['B', '2']], 'empty', ('StopIteration', ''))")),
 ('BookAndPractice', 'Project13', 'EmptyAndHeaderOnly', 'removeCsvHeader.py edge cases',
  'A line_num test that skips line 1 gave nothing for empty input and for a header only, kept a final record without a line break and wrote CRLF endings, but for a header that spans two lines it kept the whole header record in the output, as line_num was already 2 at its end.',
  (X(_PRE + r'''def strip_header(t):
    out = io.StringIO(newline=''); w = csv.writer(out)
    r = csv.reader(io.StringIO(t, newline=''))
    for row in r:
        if r.line_num == 1: continue
        w.writerow(row)
    return out.getvalue()
out = (strip_header(''), strip_header('h\r\n'), strip_header('h\r\n1,2'), strip_header('"a\nb",c\r\n1,2\r\n'), strip_header('h\n1,2\n'))'''), '(\'\', \'\', \'1,2\\r\\n\', \'"a\\nb",c\\r\\n1,2\\r\\n\', \'1,2\\r\\n\')')),
 ('BookAndPractice', 'ExcelToCsv', 'WorkbookCells', 'openpyxl.load_workbook',
  'openpyxl returns datetime objects for date cells and the number format yyyy-mm-dd h:mm:ss here; a two-row workbook read back had max_row 2 and max_column 3, and csv.writer wrote 2035-04-05 13:34:02,Apples,73 with the str() of the datetime.',
  (X(_PRE + r'''import openpyxl, datetime
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Sheet1'
ws.append([datetime.datetime(2035, 4, 5, 13, 34, 2), 'Apples', 73]); ws.append([datetime.datetime(2035, 4, 5, 3, 41, 23), 'Cherries', 85])
b = io.BytesIO(); wb.save(b)
w2 = openpyxl.load_workbook(io.BytesIO(b.getvalue())); s = w2['Sheet1']
s2 = io.StringIO(newline=''); wr_ = csv.writer(s2)
for row in s.iter_rows(values_only=True): wr_.writerow(row)
out = (w2.sheetnames, s.max_row, s.max_column, type(s['A1'].value).__name__, s['A1'].number_format, s2.getvalue())'''), "(['Sheet1'], 2, 3, 'datetime', 'yyyy-mm-dd h:mm:ss', '2035-04-05 13:34:02,Apples,73\\r\\n2035-04-05 03:41:23,Cherries,85\\r\\n')")),
 ('BookAndPractice', 'ExcelToCsv', 'MaxColumnQuadratic', 'range(1, sheet.max_column + 1)',
  'The skeleton evaluates sheet.max_column in the row loop and each evaluation visits every cell: for a sheet of 3,000 rows of 4 columns the loop over 150 rows with max_column inside took more than 20 times as long as the loop with the value hoisted.',
  (X(_PRE + r'''import openpyxl, time
wb = openpyxl.Workbook(); ws = wb.active
for i in range(3000): ws.append([i, 'x', 1.5, None])
def inside(n):
    t = time.perf_counter()
    for r in range(1, n + 1):
        for c in range(1, ws.max_column + 1): pass
    return time.perf_counter() - t
def hoisted(n):
    t = time.perf_counter(); mc = ws.max_column
    for r in range(1, n + 1):
        for c in range(1, mc + 1): pass
    return time.perf_counter() - t
a = inside(150); b = hoisted(150)
out = (ws.max_row, ws.max_column, a > 20 * b)'''), '(3000, 4, True)')),
 ('BookAndPractice', 'FormatChoice', 'SizeComparison', 'len(json.dumps(data))',
  'The Alice data is 248 characters as compact JSON, 326 with indent=2 and 407 as XML without whitespace, 1.64 times the JSON, and the repr of the Python dict is also 248.',
  (X(_PRE + r'''import xmltodict
j = json.dumps(A); jp = json.dumps(A, indent=2)
x = XS
out = (len(j), len(jp), len(x), round(len(x) / len(j), 2), len(repr(A)))'''), '(248, 326, 407, 1.64, 248)')),
 ('BookAndPractice', 'FormatChoice', 'TypesKept', 'round trip through each format',
  "JSON keeps types across a round trip (age int, car NoneType, programmer bool), xmltodict gives str for age and programmer and a dict for car, a CSV round trip gave ['Alice Doe', '30', '', 'True'] all str, and TOML read with tomllib kept int, bool and datetime and has no dumps().",
  (X(_PRE + r'''import xmltodict, tomllib
j = json.loads(json.dumps(A)); x = xmltodict.parse(XS)['person']
c = rd(wr([[A['name'], A['age'], A['car'], A['programmer']]]))[0]
t = tomllib.loads('age = 30\nok = true\nd = 2035-04-05T13:34:00')
out = ({k: type(v).__name__ for k, v in j.items() if k in ('age', 'car', 'programmer')}, {k: type(x[k]).__name__ for k in ('age', 'programmer', 'car')}, c, [type(v).__name__ for v in c], {k: type(v).__name__ for k, v in t.items()}, hasattr(tomllib, 'dumps'))'''), "({'age': 'int', 'car': 'NoneType', 'programmer': 'bool'}, {'age': 'str', 'programmer': 'str', 'car': 'dict'}, ['Alice Doe', '30', '', 'True'], ['str', 'str', 'str', 'str'], {'age': 'int', 'ok': 'bool', 'd': 'datetime'}, False)")),
]

CLAIMS = [
 (X(_PRE + r'''import importlib.metadata as m
out = (m.version('xmltodict'), m.version('openpyxl'), m.version('defusedxml'), m.version('lxml').split('.')[0], sys.version_info[:2] >= (3, 14))'''), "('1.0.4', '3.1.5', '0.7.1', '6', True)"),
 (X(_PRE + r'''import xml.parsers.expat as E
out = (csv.__version__, json.__version__, E.EXPAT_VERSION, csv.field_size_limit(), sys.get_int_max_str_digits())'''), "('1.0', '2.0.9', 'expat_2.8.1', 131072, 4300)"),
 (X(_PRE + r'''out = (round(407 / 248, 2), 3 * 10 ** 9, round(69.0 / 0.166), 2026 - 2006, 2026 - 2008, 97 - 8, 94 - 2)'''), '(1.64, 3000000000, 416, 20, 18, 89, 92)'),
 (X(_PRE + r'''out = (wr([['a', 'b']]), wr([['a', 'b']], dialect='unix'), wr([['a', 'b']], lineterminator='!'), len(wr([['spam', 'eggs', 'bacon', 'ham']])))'''), '(\'a,b\\r\\n\', \'"a","b"\\n\', \'a,b!\', 21)'),
 (X(_PRE + r'''out = (issubclass(json.JSONDecodeError, ValueError), issubclass(csv.Error, Exception), csv.Error.__module__, json.JSONDecodeError.__module__)'''), "(True, True, '_csv', 'json.decoder')"),
 (X(_PRE + r'''out = (hasattr(ET.Element('a'), 'getchildren'), hasattr(ET.Element('a'), 'getiterator'), hasattr(ET, 'XMLTreeBuilder'), hasattr(ET, 'indent'), hasattr(ET, 'canonicalize'), hasattr(ET.XMLPullParser, 'flush'))'''), '(False, False, False, True, True, True)'),
 (X(_PRE + r'''import xml.etree.cElementTree as C
out = (C.Element is ET.Element, C.__name__)'''), "(True, 'xml.etree.cElementTree')"),
 (X(_PRE + r'''import tomllib
out = (sorted(n for n in dir(tomllib) if not n.startswith('_')), hasattr(tomllib, 'dumps'), tomllib.loads('a = 1\nb = [1, 2]\n[t]\nc = "x"'))'''), "(['TOMLDecodeError', 'load', 'loads'], False, {'a': 1, 'b': [1, 2], 't': {'c': 'x'}})"),
 (X(_PRE + r'''out = (json.dumps({'a': [1, 2]}), json.dumps({'a': [1, 2]}, indent=2).count('\n'), json.dumps('é'), json.dumps('é', ensure_ascii=False), json.dumps(None), json.dumps(True))'''), '(\'{"a": [1, 2]}\', 5, \'"\\\\u00e9"\', \'"é"\', \'null\', \'true\')'),
 (X(_PRE + r'''r = subprocess.run([sys.executable, '-m', 'json'], input='{"a":1}', capture_output=True, text=True)
out = (r.returncode, r.stdout.split())'''), '(0, [\'{\', \'"a":\', \'1\', \'}\'])'),
 (X(_PRE + r'''out = (sorted(csv.list_dialects()), csv.excel_tab.delimiter, csv.unix_dialect.quoting, csv.excel.lineterminator)'''), "(['excel', 'excel-tab', 'unix'], '\\t', 1, '\\r\\n')"),
 (X(_PRE + r'''out = (type(next(csv.DictReader(['a,b', '1,2']))).__name__, list(csv.DictReader(['a,b', '1,2']))[0], csv.DictReader(['a,b', '1,2']).fieldnames)'''), "('dict', {'a': '1', 'b': '2'}, ['a', 'b'])"),
 (X(_PRE + r'''import datetime
out = (str(datetime.datetime(2035, 4, 5, 13, 34, 2)), datetime.datetime(2035, 4, 5, 13, 34, 2).isoformat(), wr([[datetime.datetime(2035, 4, 5, 13, 34, 2)]]))'''), "('2035-04-05 13:34:02', '2035-04-05T13:34:02', '2035-04-05 13:34:02\\r\\n')"),
 (X(_PRE + r'''import xml.dom.minidom as M, xml.sax as S, xml.parsers.expat as P
out = (M.parseString('<a><b>1</b></a>').documentElement.tagName, S.make_parser().__class__.__name__, P.ParserCreate().__class__.__name__)'''), "('a', 'ExpatParser', 'xmlparser')"),
 (X(_PRE + r'''out = (ET.fromstring('<a/>').tag, ET.fromstring('<a x="1"/>').attrib, ET.fromstring('<a>t<b/>u</a>').text, ET.fromstring('<a>t<b/>u</a>')[0].tail, ET.tostring(ET.Element('a'), encoding='unicode'))'''), "('a', {'x': '1'}, 't', 'u', '<a />')"),
 (X(_PRE + r'''import xmltodict
out = (xmltodict.parse('<a><b>1</b></a>'), xmltodict.unparse({'a': {'b': '1'}}, full_document=False), xmltodict.parse('<a x="1">t</a>'))'''), "({'a': {'b': '1'}}, '<a><b>1</b></a>', {'a': {'@x': '1', '#text': 't'}})"),
 (X(_PRE + r'''import openpyxl
out = (openpyxl.__version__, openpyxl.Workbook().sheetnames, openpyxl.Workbook().active.title)'''), "('3.1.5', ['Sheet'], 'Sheet')"),
 (X(_PRE + r'''out = (json.loads('{"a": 1, "a": 2}'), json.loads('{"b": 1, "a": 2}', object_pairs_hook=list), json.loads('3'), json.loads('"x"'), json.loads(' [1 , 2] '))'''), "({'a': 2}, [('b', 1), ('a', 2)], 3, 'x', [1, 2])"),
 (X(_PRE + r'''io1 = io.StringIO('a,b\r\n"c\r\nd",e\r\n', newline='')
out = ([r for r in csv.reader(io1)], csv.reader(io.StringIO('x')).line_num, io.TextIOWrapper(io.BytesIO(), newline='\r\n').newlines)'''), "([['a', 'b'], ['c\\r\\nd', 'e']], 0, None)"),
 (X(_PRE + r'''import locale
out = (type(locale.getencoding()).__name__, sys.flags.utf8_mode, sys.flags.warn_default_encoding, os.linesep)'''), "('str', 0, 0, '\\n')"),
 (X(_PRE + r'''out = (ET.tostring(ET.fromstring('<a><b/></a>'), encoding='unicode'), ET.fromstring('<a><b/></a>').find('b').text, ET.fromstring('<a><b></b></a>').find('b').text)'''), "('<a><b /></a>', None, None)"),
 (X(_PRE + r'''out = (len(json.dumps({'k': list(range(100))})), len(json.dumps({'k': list(range(100))}, separators=(',', ':'))))'''), '(397, 297)'),
 (X(_PRE + r'''import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); csv.__version__; json.__version__
out = (len(w), sys.version_info[:2])'''), '(0, (3, 14))'),
]
ERRORS = []

BEH = [
 ["A CSV text is read into lists of strings and the chapter's line with a quoted comma is read two ways",
  r'''import csv, io
t = 'Timestamp,Fruit,Quantity\r\n4/5/2025 13:34,Apples,73\r\n"Hello, world!",eggs,bacon\r\n'
rows = list(csv.reader(io.StringIO(t, newline='')))
print(len(rows), rows[1], [type(c).__name__ for c in rows[1]])
print(rows[2], '|', t.splitlines()[2].split(','))''',
  '3 [\'4/5/2025 13:34\', \'Apples\', \'73\'] [\'str\', \'str\', \'str\']\n[\'Hello, world!\', \'eggs\', \'bacon\'] | [\'"Hello\', \' world!"\', \'eggs\', \'bacon\']'],
 ['writerow returns the number of characters written, None and True are written as text, and the bytes end in CRLF',
  r'''import csv, io
s = io.StringIO(newline='')
w = csv.writer(s)
print(w.writerow(['spam', 'eggs', 'bacon', 'ham']), w.writerow(['Hello, world!', 'eggs']), w.writerow([1, 2, 3.141592, None, True]))
print(repr(s.getvalue()))''',
  '21 22 20\n\'spam,eggs,bacon,ham\\r\\n"Hello, world!",eggs\\r\\n1,2,3.141592,,True\\r\\n\''],
 ["Without newline the writer's CRLF is translated again and a reader sees an empty record after every row",
  r'''import csv, io
for nl in ('', '\r\n'):
    b = io.BytesIO(); f = io.TextIOWrapper(b, encoding='utf-8', newline=nl)
    csv.writer(f).writerows([['a', 'b'], ['c', 'd']]); f.flush()
    back = list(csv.reader(io.StringIO(b.getvalue().decode(), newline='')))
    print(repr(nl), b.getvalue(), len(back), [len(r) for r in back])''',
  "'' b'a,b\\r\\nc,d\\r\\n' 2 [2, 2]\n'\\r\\n' b'a,b\\r\\r\\nc,d\\r\\r\\n' 4 [2, 0, 2, 0]"],
 ['DictReader takes the header row as keys, puts extra values under restkey and fills missing ones with restval',
  r'''import csv, io
print(list(csv.DictReader(io.StringIO('a,b\r\n1,2\r\n3\r\n4,5,6\r\n', newline=''), restkey='extra', restval='?')))
w = csv.DictWriter(io.StringIO(), ['x'])
try: w.writerow({'x': 1, 'y': 2})
except ValueError as e: print('ValueError', e)''',
  "[{'a': '1', 'b': '2'}, {'a': '3', 'b': '?'}, {'a': '4', 'b': '5', 'extra': ['6']}]\nValueError dict contains fields not in fieldnames: 'y'"],
 ['line_num counts lines, so the header test of Project 13 keeps a header that spans two lines',
  r'''import csv, io
t = '"Name\n(first)",Age\r\nAlice,30\r\nBob,25\r\n'
r = csv.reader(io.StringIO(t, newline=''))
print([(row, r.line_num) for row in r])
r = csv.reader(io.StringIO(t, newline='')); print('book test:', [row for row in r if r.line_num != 1])
r = csv.reader(io.StringIO(t, newline='')); next(r, None); print('next:', list(r))''',
  "[(['Name\\n(first)', 'Age'], 2), (['Alice', '30'], 3), (['Bob', '25'], 4)]\nbook test: [['Name\\n(first)', 'Age'], ['Alice', '30'], ['Bob', '25']]\nnext: [['Alice', '30'], ['Bob', '25']]"],
 ["json.dumps and json.loads on the chapter's Alice data: types, indent and the round trip",
  r'''import json
d = json.loads('{"name": "Alice Doe", "age": 30, "car": null, "programmer": true, "phone": [{"type": "mobile"}]}')
print([(k, type(v).__name__) for k, v in d.items()])
print(json.dumps(d))
print(json.dumps(d, indent=2).count('\n') + 1, 'lines;', json.loads(json.dumps(d)) == d)''',
  '[(\'name\', \'str\'), (\'age\', \'int\'), (\'car\', \'NoneType\'), (\'programmer\', \'bool\'), (\'phone\', \'list\')]\n{"name": "Alice Doe", "age": 30, "car": null, "programmer": true, "phone": [{"type": "mobile"}]}\n11 lines; True'],
 ['What json.loads refuses and the message for each',
  r'''import json
for t in ('["spam", "eggs",]', '{"a": 1,}', "{'a': 1}", '{"a": 1} // c', '"a\nb"', '{"a": None}', '[01]', ''):
    try: print(repr(t), '->', json.loads(t))
    except json.JSONDecodeError as e: print(repr(t), '->', e.msg, '| line', e.lineno, 'column', e.colno)''',
  '\'["spam", "eggs",]\' -> Illegal trailing comma before end of array | line 1 column 16\n\'{"a": 1,}\' -> Illegal trailing comma before end of object | line 1 column 8\n"{\'a\': 1}" -> Expecting property name enclosed in double quotes | line 1 column 2\n\'{"a": 1} // c\' -> Extra data | line 1 column 10\n\'"a\\nb"\' -> Invalid control character at | line 1 column 3\n\'{"a": None}\' -> Expecting value | line 1 column 7\n\'[01]\' -> Expecting \',\' delimiter | line 1 column 3\n\'\' -> Expecting value | line 1 column 1'],
 ['JSON turns tuples into lists and keys into strings, and refuses types it does not know',
  r'''import json, datetime
print(json.dumps({1: 'a', None: 'b', 2.5: 'c'}), json.loads(json.dumps({'t': (1, 2)})))
for v in ({1, 2}, datetime.date(2035, 4, 5), b'x'):
    try: json.dumps(v)
    except TypeError as e: print(type(e).__name__, e)
print(json.dumps({'d': datetime.date(2035, 4, 5)}, default=str))''',
  '{"1": "a", "null": "b", "2.5": "c"} {\'t\': [1, 2]}\nTypeError Object of type set is not JSON serializable\nTypeError Object of type date is not JSON serializable\nTypeError Object of type bytes is not JSON serializable\n{"d": "2035-04-05"}'],
 ["ElementTree reads the chapter's person: tag, children, text, iteration and the text of a parent in a pretty file",
  r'''import xml.etree.ElementTree as ET
x = '<person><name>Alice Doe</name><age>30</age><car/><address><street>100 Larkin St.</street></address></person>'
r = ET.fromstring(x)
print(r.tag, [c.tag for c in r], r[0].text, repr(r[1].text), r[2].text, r[3].text)
print([e.tag for e in r.iter()], len(list(r)))
p = ET.fromstring('<person>\n  <car/>\n  <address><street>x</street></address>\n</person>')
print([(c.tag, c.text) for c in p])''',
  "person ['name', 'age', 'car', 'address'] Alice Doe '30' None None\n['person', 'name', 'age', 'car', 'address', 'street'] 4\n[('car', None), ('address', None)]"],
 ['Writing XML: tostring of a built tree, the space before the slash, bytes against str, and xsi:nil as an ordinary attribute',
  r'''import xml.etree.ElementTree as ET
root = ET.Element('person'); ET.SubElement(root, 'name').text = 'Alice Doe'
car = ET.SubElement(root, 'car'); car.set('xsi:nil', 'true'); car.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
print(ET.tostring(root)); print(ET.tostring(root, encoding='unicode'))
print(ET.fromstring(ET.tostring(root))[1].attrib)
ET.indent(root); print(ET.tostring(root, encoding='unicode'))''',
  'b\'<person><name>Alice Doe</name><car xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" /></person>\'\n<person><name>Alice Doe</name><car xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" /></person>\n{\'{http://www.w3.org/2001/XMLSchema-instance}nil\': \'true\'}\n<person>\n  <name>Alice Doe</name>\n  <car xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" />\n</person>'],
 ['A billion laughs document is refused by the parser and a small entity is expanded',
  r'''import xml.etree.ElementTree as ET
ents = ''.join('<!ENTITY lol%d "%s">' % (i, ('&lol;' if i == 1 else '&lol%d;' % (i - 1)) * 10) for i in range(1, 10))
doc = '<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol">' + ents + ']><lolz>&lol9;</lolz>'
print(len(doc), 'bytes, would expand to', 3 * 10 ** 9, 'characters')
try: ET.fromstring(doc)
except ET.ParseError as e: print('ParseError:', str(e).split(':')[0])
print(ET.fromstring('<!DOCTYPE a [<!ENTITY e "hi">]><a>&e;&e;</a>').text)''',
  '760 bytes, would expand to 3000000000 characters\nParseError: limit on input amplification factor (from DTD and entities) breached\nhihi'],
 ['xmltodict gives a dict of strings, a dict for one child and a list for two, and unparse writes it back',
  r'''import xmltodict
d = xmltodict.parse('<p><n>1</n><e><t>a</t></e></p>')
print(d, type(d['p']['n']).__name__, type(d['p']['e']).__name__)
print(type(xmltodict.parse('<p><e/><e/></p>')['p']['e']).__name__)
print(xmltodict.unparse(d, full_document=False))''',
  "{'p': {'n': '1', 'e': {'t': 'a'}}} str dict\nlist\n<p><n>1</n><e><t>a</t></e></p>"],
 ['iterparse sums a document of 5,000 items one element at a time and clear() frees each one',
  r'''import io, xml.etree.ElementTree as ET
doc = '<r>' + ''.join('<i><q>%d</q></i>' % i for i in range(5000)) + '</r>'
s = 0
for ev, e in ET.iterparse(io.BytesIO(doc.encode()), events=('end',)):
    if e.tag == 'i':
        s += int(e.find('q').text); e.clear()
print(s, 'events:', ev)''',
  '12497500 events: end'],
]

BODY = {}
def _b(key, p1, p2):
    BODY[key] = p1 + "\n\n" + p2

# ---- the six subjects ----
_b('CsvFormat',
 "The chapter opens by saying that CSV, JSON and XML are data serialization formats that store data as plaintext files, and that a CSV file is a simplified spreadsheet stored as plaintext whose lines are rows and whose values are separated by commas [S]. RFC 4180 describes the format as records on lines, fields separated by commas, quotes around fields with commas, line breaks or quotes, and CRLF line ends [RFC4180][IANA].",
 "Three ideas carry this subject. The rules of the format cover fields and records, quoted fields, the doubled quote, line breaks inside a field and the last record. Dialects cover the default dialect, tabs and the quoting constants. Encoding covers the locale encoding of open(), the byte order mark and the wrong-encoding garbage. Each was run on small texts under Python 3.14.6 (This study, 2026).")
_b('CsvModule',
 "The first half of the chapter teaches the csv module: pass a file object to csv.reader() or csv.writer(), loop over the reader or call writerow(), pass delimiter and lineterminator to change the format, and use DictReader and DictWriter when the first row is a header [S]. The Python documentation lists the same objects with their parameters and says the module follows PEP 305 [PY][PEP305].",
 "Four ideas carry this subject. Reader objects cover the strings every field is, the single pass, line_num and the memory a loop saves. Writer objects cover the return value, the conversion of values and the double spacing of Figure 18-1. Dict readers and writers cover the header row as keys, restkey, restval and the key that is not in fieldnames. Limits cover the field size and the new quoting modes. Each was run on small texts and on the shipped files (This study, 2026).")
_b('JsonFormat',
 "The chapter says JSON is a text format with the six value types string, number, object, array, Boolean and null, written with double quotes and no trailing commas, and that the json module converts between JSON text and Python data with json.loads() and json.dumps() [S]. RFC 8259 and ECMA-404 define the syntax and the Python documentation describes what the module accepts beyond it [RFC8259][ECMA][PY].",
 "Three ideas carry this subject. Syntax covers the six types and what the parser refuses. Types covers what Python values JSON can and cannot hold. Files covers pretty-printing, the ASCII escapes, json.load and json.dump and the byte order mark, none of which the chapter shows. Each was run under Python 3.14.6 and the differences between releases were recorded (This study, 2026).")
_b('XmlFormat',
 "The chapter says XML stores data in nested elements between opening and closing tags, that a valid document must have a single root element and a document with several roots is not valid, that all text is a string, that whitespace outside the tags is insignificant and that names can be written in any case but are lowercase by convention [S]. The W3C Recommendation calls a document that obeys its syntax rules well-formed and one that also complies with its document type declaration valid, and requires an end-tag to match its start-tag with no case folding [W3C][W3C98].",
 "Three ideas carry this subject. Syntax covers the match of start and end tags, the quotes around attribute values, the single root and the escapes. Namespaces cover the names of the form {uri}local and the xsi:nil attribute that the chapter writes by hand. Security covers entity expansion and external entities, which the chapter never mentions. Each was run in ElementTree, defusedxml and xmltodict (This study, 2026).")
_b('XmlLibraries',
 "The second half of the XML section teaches xml.etree.ElementTree: ET.fromstring() and ET.parse() give an Element whose tag, text and children can be read, Element and SubElement build a tree, set() adds an attribute and ET.tostring() writes it, and the third-party xmltodict turns XML into a Python dictionary [S][PY]. The chapter describes the DOM and SAX approaches in a paragraph and uses ElementTree to read the whole document at once [S].",
 "Four ideas carry this subject. Reading covers the children, the text, iteration, find and the truth value. Writing covers SubElement, the space before the slash, encodings and ET.indent(). xmltodict covers the dict of strings, the list that is not always a list and unparse. The other parsers cover minidom and iterparse. Each was run under Python 3.14.6 with xmltodict 1.0.4 and, for the Appendix A pins, 0.13.0 (This study, 2026).")
_b('BookAndPractice',
 "The chapter ends with Project 13, which removes the header row from every CSV file of a folder in three steps, a summary, eleven practice questions with their answers in Appendix B and a practice program that converts Excel files to CSV with openpyxl [S][APPB]. The online materials ship the files the projects use [S].",
 "Four ideas carry this subject. Chapter accuracy covers the printed listings that do not run as printed. Project 13 covers the header skip and the edge cases of a folder of files. The Excel-to-CSV program covers the skeleton, the dates and the cost of max_column. Format choice covers the sizes and the types of the three formats side by side. Each was run, and the shipped files were fetched and hash-checked (This study, 2026).")

# ---- the mid concepts ----
_b('CsvRules',
 "The chapter describes a CSV file as lines of values separated by commas and warns that splitting a line on commas fails when a value contains a comma, which is why the csv module exists [S]. RFC 4180 gives seven rules: a line break ends each record, the last may lack one, an optional header comes first, fields are separated by commas, quotes enclose special fields, and a quote inside a quoted field is doubled [RFC4180].",
 "Five small texts were read and written to test the rules: plain records, a quoted comma, a doubled quote, a line break inside quotes and a last record without a line break (This study, 2026).")
_b('CsvDialects',
 "The chapter changes the delimiter to a tab with the delimiter keyword and the line ending with lineterminator, and does not use the word dialect [S]. The Python documentation says that, because of the lack of a strict CSV specification, applications produce subtly different data, and that a dialect is a set of formatting parameters such as delimiter, quotechar, doublequote, skipinitialspace, lineterminator and quoting [PY].",
 "The attributes of the default dialect, a tab-separated file, the registered dialects and the quoting constants were read and used to write one row in three ways (This study, 2026).")
_b('CsvEncoding',
 "The chapter's listings open files with open('example3.csv') and open('output.csv', 'w', newline=''), and the chapter does not mention an encoding [S]. The Python documentation says that in text mode, if the encoding is not specified, it is platform-dependent and given by locale.getencoding() [PY][LOCALE].",
 "A file with non-ASCII text was decoded with three encodings, the byte order mark of an Excel file was kept and removed, and the default encoding was read in a child interpreter under the C locale with UTF-8 mode off and on (This study, 2026).")
_b('ReaderObjects',
 "The chapter reads a CSV file by passing the file object that open() returns to csv.reader(), converts the reader to a list with list(), or loops over it in a for loop, which it says saves memory with large files, and notes that a reader can be looped over only once [S]. A reader gives each row as a list of strings [PY].",
 "The shipped exampleWithHeader3.csv and small texts were read to see the types, the single pass, the number of lines against records and the memory of a loop against list() (This study, 2026).")
_b('WriterObjects',
 "The chapter writes a CSV file by opening it with 'w' and newline='', passing it to csv.writer() and calling writerow() with a list, and says writerow() returns the number of characters written [S]. The Python documentation says the writer converts None to an empty string and everything else with str() [PY].",
 "The three rows of the chapter were written to a text buffer and the return values, the bytes and the conversions were read; the translation of line ends that Windows does was reproduced (This study, 2026).")
_b('DictReadersWriters',
 "The chapter says DictReader uses the first row as the keys of each dictionary and that DictWriter writes dictionaries when it is given the field names, and prints a list of the rows as dictionaries [S]. The Python documentation describes restkey, restval, extrasaction and the dict rows that replaced OrderedDict in Python 3.8 [PY].",
 "The shipped exampleWithHeader3.csv was read with DictReader and small texts were used for the rows that are longer or shorter than the header and for a key that is not in fieldnames (This study, 2026).")
_b('CsvLimits',
 "The chapter does not mention a limit of the reader or the modes added in later releases of Python [S]. The Python documentation gives field_size_limit() with a default of 131,072 and says QUOTE_NOTNULL and QUOTE_STRINGS were added in Python 3.12 [PY][WN].",
 "A field one character over the limit was read and the two new modes were used for reading and writing a row with None, an empty string and a number (This study, 2026).")
_b('JsonSyntax',
 "The chapter lists the six value types of JSON and says the format does not allow trailing commas, comments or single quotes, with an invalid list as its example [S]. RFC 8259 states the grammar of the six types and says implementations may accept more than the grammar, and the Python module does [RFC8259][PY].",
 "The chapter's Alice text and a dozen invalid texts were given to json.loads() and the message, line and column of each error were recorded (This study, 2026).")
_b('JsonTypes',
 "The chapter says JSON represents a Python dictionary as an object, a list as an array, None as null and True and False as true and false, and does not list what JSON cannot hold [S]. The Python documentation has a conversion table that maps tuples to arrays and says keys are coerced to strings and that other types need a default function [PY].",
 "Python values were written and read back to see what changes and which raise TypeError (This study, 2026).")
_b('JsonFiles',
 "The chapter shows json.loads() and json.dumps() on strings and says dumps() takes an indent argument for readable output, but not how to read or write a file [S]. The Python documentation describes json.load() and json.dump() for file objects, the ensure_ascii argument, the byte order mark rule of RFC 8259 and, in 3.14, notes on serialization errors [PY][RFC8259].",
 "The Alice data was written to a file and read back, with and without ensure_ascii, from text and binary files and with a byte order mark (This study, 2026).")
_b('XmlSyntax',
 "The chapter says a valid document must have a single root element, that names can be written in any case, that attribute values may be in single or double quotes and that whitespace outside the tags is insignificant [S]. The W3C Recommendation uses well-formed for the syntax rules and valid for compliance with a document type declaration, and says the Name in an end-tag must match the element type in the start-tag [W3C].",
 "About twenty small documents were parsed with ElementTree to see which rules it enforces and with what message, and the words well-formed and valid were tested against a DTD with lxml (This study, 2026).")
_b('XmlNamespaces',
 "The chapter's person has a car element with the attribute xsi:nil=\"true\" and the namespace attribute xmlns:xsi, and says a self-closing tag has None as its text [S]. Namespaces in XML says a name with a prefix belongs to the namespace that the prefix is bound to, and XML Schema says an element labeled xsi:nil true must be empty [NS][XSD].",
 "Documents with prefixed names and with xsi:nil were parsed and written back to see how ElementTree names them and whether it understands nil (This study, 2026).")
_b('XmlSecurity',
 "The chapter parses XML text with ET.fromstring() and xmltodict.parse() and gives no warning about untrusted input [S]. The Python documentation says the built-in XML parsers rely on Expat, that versions lower than 2.7.2 may be vulnerable to billion laughs, quadratic blowup and large tokens, and CWE lists entity expansion and external entities as weaknesses [PY][CWE].",
 "A billion laughs document, a small entity and an external entity were given to ElementTree, defusedxml and both versions of xmltodict (This study, 2026).")
_b('ElementTreeReading',
 "The chapter reads XML with ET.fromstring() or ET.parse() and getroot(), then uses the tag and text attributes, indexes into an element, loops over its children and calls iter() with and without a tag name, and says XPath can locate elements [S]. The Python documentation describes the same Element, the order of iter() and a limited XPath [PY].",
 "The chapter's person was parsed from a string and from a pretty-printed file and each of these operations was run on it (This study, 2026).")
_b('ElementTreeWriting',
 "The chapter builds XML with ET.Element(), ET.SubElement() and set(), sets the text attribute and calls ET.tostring(root, encoding='utf-8').decode('utf-8') to get a string [S]. The Python documentation describes tostring with its encoding, xml_declaration and short_empty_elements parameters and ET.indent() [PY].",
 "The tree of the chapter was built and written with each option, and the bytes and the strings were compared with what the chapter prints (This study, 2026).")
_b('XmltodictLibrary',
 "The chapter installs xmltodict, calls xmltodict.parse(xml_string) and prints a dictionary in which the namespace attribute of car is a key starting with an at sign and the phones are a list [S]. The PyPI page says xmltodict makes working with XML feel like working with JSON, and Appendix A pins version 0.13.0 [PYPI][APPA].",
 "The chapter's statement was replayed with 1.0.4 and 0.13.0, and one child against two, attributes with text and unparse were tried (This study, 2026).")
_b('OtherParsers',
 "The chapter describes the DOM approach, which reads the entire document into memory, and the SAX approach, which reads a stream of elements, names the modules xml.dom, xml.sax and xml.etree.ElementTree, and uses ElementTree for its examples [S]. The Python documentation describes xml.dom.minidom as a minimal DOM implementation, xml.sax as event-driven and ElementTree.iterparse() as incremental parsing [PY][MINIDOM][SAX].",
 "The same two numbers were read with ElementTree, minidom and SAX, and a document of 200,000 items was parsed four ways to measure memory (This study, 2026).")
_b('ChapterAccuracy',
 "A listing of a book is a statement that a reader will type and compare with the output printed beside it; the chapter prints 97 interactive statements, and a reader who types them in the order of the page gets the printed output only if the page, the files and the Python release agree [S]. The online materials were meant to supply the files [S].",
 "All 97 statements were replayed as printed, with the curly quotation mark repaired, with the parse block left out and with the Appendix A pins, and the differences were counted (This study, 2026).")
_b('Project13',
 "Project 13 removes the header row from every CSV file of the working directory in three steps: loop through the files that end in .csv, read each with csv.reader() and skip the first row, and write the other rows to a new file in a folder called headerRemoved [S]. The online materials ship removeCsvHeader.py and a zip of 100 CSV files to run it on [S].",
 "The program was run on the 100 shipped files, and a second set of files with a header of two lines, an empty file, a header only, a final line without a break and a byte order mark was made for its edge cases (This study, 2026).")
_b('ExcelToCsv',
 "The practice program asks for a program that reads every Excel file of the working directory with openpyxl and writes one CSV file per sheet, named for the file and the sheet, and gives a skeleton with nested loops over the rows and columns [S]. The openpyxl documentation describes the library as reading and writing Excel 2010 xlsx files [OPENPYXL].",
 "A converter was written to the skeleton and run on the shipped workbooks, the cost of the skeleton's max_column was measured, and LibreOffice exported the same file for comparison (This study, 2026).")
_b('FormatChoice',
 "The chapter's summary says CSV, JSON and XML are plaintext formats that can be edited in a text editor, that JSON is simpler than XML and more widely adopted than YAML, and that TOML is chiefly used for configuration [S]. It names shelve as storing all Python data types in a binary file that other languages cannot read [S].",
 "The Alice data was written in each format and the sizes were counted, and each format was read back to see which types survived (This study, 2026).")

# ---- CsvFormat leaves ----
_b('FieldsAndRecords',
 "The chapter says each line of a CSV file represents a row of a spreadsheet and commas separate the cells in the row, and prints example3.xlsx as lines of comma-separated values [S]. RFC 4180 says each record is on a separate line and the fields of a record are separated by commas [RFC4180].",
 "A text of two lines was read with csv.reader and gave two records of two fields, all of them strings, and the same text had 2 commas, so the count of commas is not the count of fields (This study, 2026).")
_b('QuotedCommaField',
 "The chapter warns that calling split(',') on each line of text does not work because not every comma separates two cells, and notes that the writer escapes the comma in 'Hello, world!' with double quotes [S]. RFC 4180 says fields containing commas, double quotes or line breaks should be enclosed in double quotes [RFC4180].",
 "The line with 'Hello, world!' in quotes was split both ways: split(',') returned 5 pieces and the first began with a quote, csv.reader returned 4 fields and the first was Hello, world! (This study, 2026).")
_b('DoubledQuoteEscape',
 "The chapter does not say how a double quote inside a value is written [S]. RFC 4180 says a double quote appearing inside a field must be escaped by preceding it with another double quote, and the csv module's doublequote parameter defaults to True [RFC4180][PY].",
 "The text with say, then a doubled quote, hi, then a doubled quote was read as the field say 'hi' in double quotes, and writing that field back gave the same text, ending in CRLF (This study, 2026).")
_b('EmbeddedLineBreak',
 "The chapter does not say that a value can hold a line break [S]. RFC 4180 says fields containing line breaks must be enclosed in double quotes, and the csv documentation says line_num counts lines, not records, because records can span several lines [RFC4180][PY].",
 "A text of 3 lines was read as 2 records and the first held a line feed in its first field; the writer put quotes around that field when it wrote it back. Splitting the text into lines would have given 3 rows (This study, 2026).")
_b('LastRecordNoBreak',
 "The chapter prints its CSV files as lines and says nothing about the end of the file [S]. RFC 4180 says the last record in the file may or may not have an ending line break, and that a header line is optional [RFC4180].",
 "Two texts that differ only by the final CRLF were read as the same two records; the shipped exampleWithHeader3.csv has 8 CRLF endings for 8 lines. An empty line between two records was read as an empty record, which a program must skip (This study, 2026).")
_b('ExcelDialect',
 "The chapter changes the delimiter and the line terminator with keyword arguments and does not name the dialect they modify [S]. The Python documentation says a dialect is a set of formatting parameters, that csv.excel is the default and describes the usual properties of an Excel-generated CSV file, and that excel-tab and unix are also registered [PY].",
 "The attributes of csv.excel were read: a comma, a double quote, doublequote True, skipinitialspace False, CRLF and QUOTE_MINIMAL, and list_dialects() named excel, excel-tab and unix (This study, 2026).")
_b('TabDelimited',
 "The chapter writes a tab-separated file with delimiter='\\t' and lineterminator='\\n\\n', and prints the return values 21, 30 and 16 [S]. The Python documentation registers the dialect excel-tab for tab-delimited files [PY].",
 "The file was read back with the default delimiter, which left a whole line as one field and broke 'Hello, world!' at its comma, and with delimiter='\\t', which gave the right fields; the dialect excel-tab wrote the field that held a tab in quotes. The reader ignores lineterminator (This study, 2026).")
_b('QuotingConstants',
 "The chapter never names a quoting mode [S]. The Python documentation lists QUOTE_MINIMAL, QUOTE_ALL, QUOTE_NONNUMERIC and QUOTE_NONE, and QUOTE_STRINGS and QUOTE_NOTNULL which Python 3.12 added [PY][WN].",
 "One row with a string, an int, a float, None, an empty string and a value with a comma was written under three modes, and the six constants have the values 0 to 5 (This study, 2026).")
_b('DefaultEncodingIsLocale',
 "The chapter's listings call open() without an encoding and never mention one [S]. The Python documentation says that if the encoding is not specified in text mode it is platform-dependent, given by locale.getencoding(), and PEP 686 makes UTF-8 mode the default from Python 3.15 [PY][PEP686].",
 "A child interpreter under the C locale reported the encoding ANSI_X3.4-1968 with UTF-8 mode off and utf-8 with -X utf8=1, and locale.getencoding() was the same in both. The default is a property of the machine, not of the program (This study, 2026).")
_b('BomUtf8Sig',
 "The chapter does not say that a CSV file can start with a byte order mark [S]. The Python documentation describes utf-8-sig as the variant that writes and skips the mark that Microsoft Notepad introduced, and RFC 8259 forbids adding one to JSON that is sent over a network [PY][CODECS][RFC8259].",
 "The bytes of a file saved by Excel as CSV UTF-8 were decoded as utf-8, which left \\ufeff at the start of the first field and of the first DictReader key, and as utf-8-sig, which did not (This study, 2026).")
_b('Cp1252Mojibake',
 "The chapter does not say what happens when the file's encoding and the program's differ [S]. The Python documentation lists cp1252 as Western Europe and cp1254 as Turkish among its standard encodings, and says the default depends on the locale [CODECS][LOCALE].",
 "A UTF-8 file with Turkish text was decoded as cp1252, which gave garbled letters without an error, and as cp1254, which raised UnicodeDecodeError; the reverse, a cp1254 file read as UTF-8, also raised it (This study, 2026).")

# ---- CsvModule leaves ----
_b('ReaderEveryValueString',
 "The chapter lists what CSV files lack, no data types among them, and says that every value is a string, and it prints the rows of example3.csv as lists of strings [S]. The Python documentation says each row read from the file is returned as a list of strings unless QUOTE_NONNUMERIC is set [PY].",
 "The line 4/5/2035 13:34,Apples,73 was read into three strings and 73 had to be converted with int() to add 1; the shipped file's rows read the same, with the year 2025 (This study, 2026).")
_b('ReaderUsedOnce',
 "The chapter says you can loop over the reader object only once and must call open() and csv.reader() again to read the file again [S]. A reader is an iterator over the lines of the file object [PY].",
 "A second list() on a reader returned 0 rows after the first returned 2, and the reader has neither len() nor indexing; the type is named reader. A reader over a filename string is not refused: it iterates over the letters (This study, 2026).")
_b('LineNumVsRecords',
 "The chapter uses reader.line_num to print the row number and to test for row 1 and skip the header, and says line numbers begin at 1 [S]. The Python documentation says line_num is the number of lines read from the source iterator and is not the same as the number of records returned, as records can span multiple lines [PY].",
 "With a header cell that holds a line break the records ended at line numbers 2, 3 and 4, and the test line_num != 1 kept all 3 records, header included. next(reader, None) skips a header of any length (This study, 2026).")
_b('LoopSavesMemory',
 "The chapter says that for large CSV files a for loop over the reader saves loading the entire file into memory at once [S]. The tracemalloc module reports the current and peak size of traced memory blocks [TRACEMALLOC].",
 "On 60,000 generated rows the peak of list(reader) was more than 10 times that of a loop; on a 300,000-row file the figures were 69.0 MiB and 0.166 MiB, a ratio of 416, and the loop was faster too (This study, 2026).")
_b('WriterReturnsLength',
 "The chapter writes output.csv with three calls of writerow() and prints the return values 21, 32 and 16, and says the method returns the number of characters written to the file [S]. The Python documentation says writerow returns the return value of the call to the write method of the file object [PY].",
 "The three rows were written to a text buffer and returned 21, 32 and 16; the buffer held 69 characters and 3 CRLF endings, so each count includes the 2 characters of the line ending (This study, 2026).")
_b('WriterTypes',
 "The chapter writes strings, an int and a float and says the writer escapes the comma of 'Hello, world!' [S]. The Python documentation says all other non-string data is stringified with str() before being written and that None is written as the empty string [PY].",
 "None became an empty field, True became True, a long int and 1e-07 kept their str(), a list was written as its repr in quotes, and reading them back gave only strings; writerow(5) raised Error: iterable expected, not int (This study, 2026).")
_b('WriterDoubleSpacing',
 "The chapter says that on Windows you must pass newline='' to open() or the rows of output.csv will be double-spaced, as shown in Figure 18-1, for technical reasons beyond the scope of the book [S]. The Python documentation says that without newline='' an extra carriage return is added on platforms that use CRLF on write [PY][IO].",
 "An io.TextIOWrapper asked for CRLF, as Windows does, turned the writer's CR LF into CR CR LF, a reader then returned an empty record after each row, and LibreOffice 24.2 drew the figure's layout with rows 1, 3 and 5 filled. The picture's alt text describes calculators (This study, 2026).")
_b('DictReaderFirstRowKeys',
 "The chapter says DictReader treats the values in the first row as keys, that it skips the header for you, that without headers the first row would become the keys, and that a second argument can supply made-up names such as time, name and amount [S]. The documentation adds that rows are dicts since Python 3.8 [PY].",
 "exampleWithHeader3.csv was read as 7 dictionaries with the keys Timestamp, Fruit and Quantity, where the chapter's printed list has 6 and the year 2035; with the made-up names the header row became the first dictionary (This study, 2026).")
_b('RestkeyRestval',
 "The chapter does not mention restkey or restval [S]. The documentation says that if a row has more fields than fieldnames the remaining data goes in a list under restkey, which defaults to None, and that a shorter row is filled with restval, which defaults to None [PY].",
 "A row with two extra values gave a list under the key None, or under 'extra', and a row with a missing value gave None or the restval '?'; a blank line was skipped and a repeated header name kept the last value (This study, 2026).")
_b('DictWriterExtraKey',
 "The chapter writes a header with writeheader(), prints return values 16, 20, 15 and 20, and says a key missing from a dictionary becomes an empty cell and that the order of keys in a dictionary does not matter [S]. The documentation says a key that is not in fieldnames raises ValueError unless extrasaction is 'ignore' [PY].",
 "writeheader() returned 10 for Name and Pet, a dictionary without Pet wrote an empty cell, one with an extra key Age raised ValueError: dict contains fields not in fieldnames, and extrasaction='ignore' dropped the key (This study, 2026).")
_b('FieldSizeLimit',
 "The chapter does not mention a limit on the size of a field [S]. The documentation says field_size_limit() returns the current maximum field size the parser allows and that a field larger than it raises Error [PY].",
 "The default was 131072; a field of 131073 characters raised Error: field larger than field limit (131072) and one of 131072 was read. A program that reads larger fields must raise the limit first (This study, 2026).")
_b('QuoteStringsNotNull',
 "The chapter's reader treats an unquoted empty field and a quoted empty field the same [S]. Python 3.12 added QUOTE_NOTNULL and QUOTE_STRINGS so that a reader and a writer can tell None from an empty string [PY][WN].",
 "The text with a quoted a, an empty field, a quoted empty field and 3 read as empty strings by default, with None for the unquoted empty field under QUOTE_NOTNULL, and under QUOTE_STRINGS the 3 became 3.0; under 3.11 these constants do not exist (This study, 2026).")

# ---- JsonFormat leaves ----
_b('SixValueTypes',
 "The chapter says JSON uses curly brackets for objects and square brackets for arrays, null for None, lowercase true and false, and that json.loads() returns a Python dictionary from a string whose strings use double quotes [S]. RFC 8259 names six value types: object, array, number, string and the three literals false, null and true [RFC8259].",
 "The chapter's Alice text was parsed into a dict with str, int, NoneType, bool, dict and list values that equals the original data, and dumps() gave back the same 248 characters (This study, 2026).")
_b('TrailingCommaRefused',
 "The chapter says JSON does not allow JavaScript comments or multiline strings, that all strings must use double quotes and that [\"spam\", \"eggs\"] is valid and [\"spam\", \"eggs\",] is not [S]. The RFC grammar has no trailing comma, comment or single-quoted string [RFC8259].",
 "json.loads refused the chapter's invalid array with Illegal trailing comma before end of array at line 1 column 16, and a single-quoted key and a trailing comment too; under 3.11 and 3.12 the first message was Expecting value (This study, 2026).")
_b('RawNewlineInString',
 "The chapter says JSON does not allow multiline strings [S]. RFC 8259 says control characters, U+0000 to U+001F, must be escaped inside a string, and the Python documentation describes the strict argument that allows them [RFC8259][PY].",
 "A string with a raw line feed or a raw tab was refused with Invalid control character at; the same string with the escape \\n parsed, and strict=False accepted the tab (This study, 2026).")
_b('NaNAcceptedByPython',
 "The chapter does not mention NaN or Infinity [S]. RFC 8259 says numeric values that cannot be represented in the grammar, such as Infinity and NaN, are not permitted, and the Python documentation says the module by default writes and reads them as JavaScript does [RFC8259][PY].",
 "json.loads accepted NaN, Infinity and -Infinity and returned nan, inf and -inf, dumps wrote them and allow_nan=False refused with ValueError: Out of range float values are not JSON compliant (This study, 2026).")
_b('TupleBecomesList',
 "The chapter says the value passed to json.dumps() can consist only of strings, integers, floats, Booleans, lists, dictionaries and NoneType [S]. The Python documentation's conversion table writes a tuple as an array and reads an array as a list [PY].",
 "A tuple was written as [1, 2] without an error, which the chapter's list suggests it should not be, and read back as a list, so the round trip of a dictionary that held a tuple was not equal to the original; a set raised TypeError (This study, 2026).")
_b('KeysBecomeStrings',
 "The chapter says Python dictionaries and JSON objects both hold key-value pairs [S]. RFC 8259 says the name of an object member is a string, and the Python documentation says that when a dictionary is converted into JSON all its keys are converted to strings [RFC8259][PY].",
 "The keys 1, 2.5 and None were written as 1, 2.5 and null in quotes, and True as the key collided with 1 in the Python dictionary before the writing; a tuple key raised TypeError: keys must be str, int, float, bool or None (This study, 2026).")
_b('UnsupportedTypesRaise',
 "The chapter says JSON cannot represent Python-specific objects such as File objects and CSV reader or writer objects [S]. The Python documentation says an object that is not serializable raises TypeError unless a default function is given [PY].",
 "datetime, Decimal, bytes and complex values each raised TypeError: Object of type ... is not JSON serializable, and default=str turned the datetime and the Decimal into strings (This study, 2026).")
_b('IndentAndSeparators',
 "The chapter writes the Alice data with json.dumps(python_data, indent=2) and says the text is then in separate lines with two spaces of indentation per nesting level, and that the compact form is fine between programs [S]. The documentation describes indent, separators and sort_keys [PY].",
 "indent=2 gave 21 lines and 326 characters and read back equal to the data, the compact separators gave 225 characters, a tab indent worked, and sort_keys=True began with address, age and car (This study, 2026).")
_b('EnsureAscii',
 "The chapter does not say that dumps() escapes non-ASCII characters [S]. The Python documentation says that with ensure_ascii true, the default, the output has all incoming non-ASCII characters escaped [PY].",
 "Müller and İstanbul were written as M\\u00fcller and \\u0130stanbul by default and as the characters with ensure_ascii=False; the emoji U+1F600 was written as a surrogate pair and read back as one character (This study, 2026).")
_b('FileRoundTrip',
 "The chapter says that once you have the JSON text as a string you can write it to a .json file, and it shows no file call [S]. The Python documentation describes json.dump() and json.load() for file objects and says json.loads() takes a string, bytes or bytearray [PY].",
 "json.dump wrote the Alice data to a file with indent=2 and ensure_ascii=False and returned None, json.load read it back from a text file and from one opened in rb, and loads(file) and dump to a file opened wb raised TypeError (This study, 2026).")
_b('BomHandling',
 "The chapter does not mention encodings of JSON text [S]. RFC 8259 says JSON exchanged between systems must be encoded in UTF-8, that implementations must not add a byte order mark and that parsers may ignore one [RFC8259].",
 "json.loads of bytes that start with EF BB BF returned the list, the encoding being detected as utf-8-sig, while a str starting with U+FEFF raised JSONDecodeError: Unexpected UTF-8 BOM; UTF-16 bytes were also detected (This study, 2026).")
_b('SerializationErrorNotes',
 "The chapter does not show a serialization error [S]. Python 3.14 adds exception notes to JSON serialization errors that identify the source of the error, and allows python -m json [WN314].",
 "The error for a set inside a list inside a dictionary carried the notes when serializing list item 1 and when serializing dict item 'a'; under 3.11 to 3.13 the notes were absent, and the error for a tuple key has none (This study, 2026).")

# ---- XmlFormat leaves ----
_b('CaseSensitiveTags',
 "The chapter says tag and attribute names can be written in any case but are lowercase by convention, and that each element has an opening and a closing tag [S]. The W3C Recommendation says the Name in an element's end-tag must match the element type in the start-tag and that no case folding is performed [W3C].",
 "ElementTree refused <A></a> and <a><b></a> with mismatched tag, and parsed <Person><NAME>x</NAME></Person>, so a name may be in any case only if both tags use the same one (This study, 2026).")
_b('AttributeQuotesRequired',
 "The chapter says attributes are key-value pairs written as key=\"value\" inside the opening tag and that values can be in single or double quotes, but double quotes are standard [S]. XML requires a quoted value, unlike HTML, which allows an unquoted one [W3C].",
 "<a b='1'/> parsed and was written back with double quotes; <a b=1/> and <a b/> raised not well-formed (invalid token) and a repeated attribute raised duplicate attribute (This study, 2026).")
_b('SingleRootRequired',
 "The chapter says valid XML documents must have a single root element that contains all the others, and that a document with several roots, such as three person elements one after the other, is not valid [S]. The W3C Recommendation requires a well-formed document to have one element that contains all the others, the root [W3C].",
 "ElementTree raised junk after document element for <a/><b/> and for text after the root, accepted a comment before or after the root, and raised no element found for empty input (This study, 2026).")
_b('EscapesRequired',
 "The chapter does not say how to write an ampersand or a less-than sign in text, and says the comments of XML are identical to HTML's [S]. The W3C Recommendation says the characters < and & must be escaped as &lt; and &amp; and defines only five entities, so an HTML entity like &nbsp; is not defined [W3C].",
 "A lone & or < in text raised not well-formed (invalid token), &amp; and &lt; parsed to & and <, &nbsp; raised undefined entity, and a CDATA section carried 1 < 2 & 3 as plain text (This study, 2026).")
_b('NamespaceClarkName',
 "The chapter writes xmlns:xsi as an ordinary attribute and does not explain namespaces [S]. Namespaces in XML binds a prefix to a namespace name with a xmlns attribute, and ElementTree names a qualified element {namespace}local [NS][PY].",
 "The element x:b with x bound to urn:x had the tag {urn:x}b and the attribute {urn:x}c, equal to the text of an ET.QName, and was written back with the generated prefix ns0 unless register_namespace was called (This study, 2026).")
_b('XsiNilNotUnderstood',
 "The chapter says there is no null value in XML but one can be approximated with xsi:nil=\"true\" and xmlns:xsi, and that a self-closing tag has None as its text [S]. XML Schema says an element labeled xsi:nil true must be empty, and it is a schema processor that acts on the attribute [XSD].",
 "ElementTree kept the attribute under its full name {http://www.w3.org/2001/XMLSchema-instance}nil for the values true and false, left the text of an element with nil true and content intact, and refused a document that used the prefix without declaring it (This study, 2026).")
_b('BillionLaughsLimit',
 "The chapter does not warn about entity expansion [S]. The Python documentation describes the billion laughs attack as multiple levels of nested entities that each refer to another several times, and Wikipedia gives the example of 10 entities, each of 10 of the previous one, expanding to a billion lol [PY][WP][CWE].",
 "The 760-byte document of the example, which would expand to 3,000,000,000 characters, was refused by ElementTree in Python 3.14.6 (Expat 2.8.1) in 0.12 s with a limit on the input amplification factor, and a small entity expanded to hellohello (This study, 2026).")
_b('ExternalEntityNotFetched',
 "The chapter does not warn about external entities [S]. CWE-611 names the weakness of an XML document that references an external entity and OWASP describes the attack that reads local files, and the Python documentation says Expat itself does not by default access local files or create network connections [CWE][OWASP][PY].",
 "A document whose entity named a local file with a unique text raised undefined entity &x; in ElementTree and the text of the file did not appear in the error (This study, 2026).")
_b('DefusedxmlForbids',
 "The chapter does not mention defusedxml [S]. The PyPI page of defusedxml says it defuses XML bombs and other exploits and lists denial-of-service workarounds for Python's XML libraries [PYPI][DEFUSED].",
 "defusedxml 0.7.1 raised EntitiesForbidden for a document with an entity and DTDForbidden with forbid_dtd=True, parsed an ordinary document, and both exceptions are ValueError subclasses; its last upload is 0.7.1 of March 2021 and 0.8.0rc2 exists (This study, 2026).")
_b('XmltodictEntitiesDisabled',
 "The chapter installs xmltodict by Appendix A, which pins version 0.13.0, and calls xmltodict.parse() on text [S][APPA]. The PyPI page lists xmltodict 1.0.4 as the newest release [PYPI].",
 "xmltodict 1.0.4 refused every entity with ValueError: entities are disabled and parsed ordinary text, while 0.13.0 parsed both the small entity and the billion laughs file; the same chapter statements gave the same output in both versions (This study, 2026).")

# ---- XmlLibraries leaves ----
_b('RootTagAndChildren',
 "The chapter parses the xml_string with ET.fromstring(), calls the Element root, and reads root.tag, root.text, list(root), root[0] and root[4][0], and says the children are reachable through an integer index like a list [S]. The Python documentation shows children nested and reached by index, as in root[0][1].text [PY].",
 "The root had the tag person and 6 children, root[0].text was Alice Doe, root[4][0].text was 100 Larkin St., a slice worked, and root[9] raised IndexError: child index out of range (This study, 2026).")
_b('TextNoneOrString',
 "The chapter says any self-closing tag, like <car/>, will use None for its text attribute, and that XML text has no data type so everything between the tags is a string [S]. The documentation says text is the text up to the first child or None and gives <a><b>1<c>2<d/>3</c></b>4</a>, where a has None for both text and tail [PY].",
 "age had the str 30, the self-closing car and an empty pair had None, and an element with one space had that space, so a program cannot tell <car/> from <car></car> (This study, 2026).")
_b('WellFormedNotValid',
 "The chapter calls a document with several roots not valid [S]. The W3C Recommendation defines a well-formed document by its syntax and a valid document as one with a document type declaration that it complies with [W3C].",
 "ElementTree parsed a person with a banana child, and lxml with a DTD that allows only a name child answered False for it and True for a person with a name; xml.etree.ElementTree has no validate() (This study, 2026).")
_b('ParentTextIsWhitespace',
 "The chapter prints None for the text of address and phone in a loop over the root's children, and says whitespace outside the opening and closing tags is insignificant [S]. The documentation says the tail is the text between the element's end tag and the next tag, or None [PY].",
 "In a pretty-printed file address had the text of a line break and eight spaces, the root and each tail held whitespace, and only car had None; text.strip() or None gives the chapter's None, and the chapter's own parse of my_data.xml rebinds root (This study, 2026).")
_b('IterDocumentOrder',
 "The chapter loops over the immediate children with for elem in root, and calls root.iter() to iterate over everything underneath and root.iter('number') to filter by tag [S]. The documentation says iter() walks the element and all its descendants in document order, the element itself first [PY].",
 "iter() returned 16 elements of the Alice document against 6 children, started with the root, and iter('number') gave the two phone numbers in document order (This study, 2026).")
_b('FindAndXPathSubset',
 "The chapter says a language called XPath can locate elements in an XML document and that this is beyond the scope of the chapter [S]. The documentation says the module provides limited support for XPath expressions, a small subset of the abbreviated syntax [PY].",
 "find('name') gave Alice Doe, findall('.//number') the two numbers, findtext('address/zip') 94102, find('nothing') returned None and .text on it raised AttributeError, and an Element has no xpath() method (This study, 2026).")
_b('ElementTruthDeprecated',
 "The chapter tests an element's text against None and does not test an element itself [S]. The documentation says testing the truth value of an Element emits DeprecationWarning since Python 3.12 and will always return True in a future release [PY][WN].",
 "bool() was False for an element without children and True for one with a child, and testing it raised a DeprecationWarning; the test that does not depend on children is is not None (This study, 2026).")
_b('SubElementAndSet',
 "The chapter creates the person Element, adds children with SubElement(), sets the text attribute and sets xsi:nil and xmlns:xsi with set(), and calls ET.tostring(root, encoding='utf-8').decode('utf-8') [S]. It says tostring() returns bytes and that decode() is needed to get a string [S].",
 "tostring(root) returned bytes and encoding='unicode' returned a str, and the namespace was written as an attribute whose name has a colon, with no check that the prefix is declared; the parser refused the document that used it undeclared (This study, 2026).")
_b('TostringSpaceBeforeSlash',
 "The chapter prints the string with the car element ending in a slash and a closing bracket [S]. The documentation says the short_empty_elements parameter chooses between a self-closing tag and an empty pair, and that an encoding of unicode returns a str [PY].",
 "ElementTree wrote <b /> with a space, <b></b> with short_empty_elements=False, an XML declaration only with xml_declaration=True, and with the default encoding turned Müller into M&#252;ller (This study, 2026).")
_b('IndentPrettyPrint',
 "The chapter does not pretty-print XML [S]. The documentation says ET.indent(tree, space, level) appends whitespace to the subtree to indent it visually and was added in Python 3.9 [PY].",
 "A tree of 4 elements was indented in place to 5 lines, and the whitespace was stored in the text of a and the tail of b, so indent() changes the data the tree holds (This study, 2026).")
_b('ParseGivesStrings',
 "The chapter parses the same text with xmltodict.parse() and prints a dictionary, and says everything is a string, that programmer is the string true and that car is an awkward key-value pair instead of None [S]. The PyPI page says xmltodict makes working with XML feel like working with JSON [PYPI].",
 "The printed dictionary matched under 1.0.4 and 0.13.0; age was the str 30, programmer the str true, and car a dict with @xsi:nil and @xmlns:xsi (This study, 2026).")
_b('OneEntryDictTwoList',
 "The chapter prints the phones as a list of dictionaries under phoneEntry and says to double-check the input and output of any XML module [S]. The xmltodict documentation on PyPI describes the force_list option for elements that may occur once or many times [PYPI].",
 "phoneEntry was a dict when there was one entry and a list when there were two, force_list made the single one a list, and an element with an attribute and text gave @href and #text keys (This study, 2026).")
_b('UnparseRoundTrip',
 "The chapter shows xmltodict.parse() only [S]. The xmltodict page says you can also convert in the other direction, using unparse() [PYPI].",
 "unparse() wrote the Alice dictionary with an XML declaration, parse of that text equalled the dictionary, pretty=True used tabs, and a dictionary with two roots raised ValueError: Document must have exactly one root (This study, 2026).")
_b('MinidomSameAnswer',
 "The chapter says the DOM approach reads the whole document into memory and names the xml.dom module [S]. The documentation says xml.dom.minidom is a minimal implementation of the Document Object Model interface [MINIDOM].",
 "minidom returned the same two phone numbers as ElementTree through firstChild.data, its document element was person, and node types were numbers such as ELEMENT_NODE; on a 200,000-item file minidom peaked at 440.6 MiB against 108.3 MiB for ElementTree (This study, 2026).")
_b('IterparseClear',
 "The chapter says the SAX approach reads a stream of elements and is ideal for gigabyte-sized documents, and does not mention iterparse [S]. The documentation says ElementTree builds the tree incrementally but does not free it, and that clear() on an element frees memory while iterparse is used [PY][SAX].",
 "20,000 items summed to 199,990,000 with and without clear(), and without clear() the traced peak was more than 1.5 times higher; on 200,000 items the peaks were 15.7 MiB with clear(), 108.3 MiB without and 0.4 MiB for SAX (This study, 2026).")

# ---- BookAndPractice leaves ----
_b('CurlyQuoteBreaksLiteral',
 "The chapter prints two xml_string listings whose namespace URL ends with a curly closing quotation mark, and prints json_string over several lines inside its quotes [S]. A Python string literal in single or double quotes cannot span lines, and an XML parser needs a straight quotation mark to close an attribute value [PY][W3C].",
 "The text with the curly mark raised ParseError: unclosed token in ElementTree and the straight one parsed; as typed, json_string was a SyntaxError and, with the line break kept inside the JSON text, raised Invalid control character. 8 of the 97 statements differ as printed, 4 once the mark is repaired (This study, 2026).")
_b('PrintedNoneVsWhitespace',
 "The chapter prints None as the text of address and phone in the loop over the root's children and in the loop over iter(), and prints car -- None [S]. That holds for the compact xml_string, and the chapter parses my_data.xml in the statement before it and rebinds root [S].",
 "For a pretty-printed text the loop gave a line break and spaces for address and None only for car, and for the compact text None for both; in the replay of the page's order the two loops differ for that reason, and with the parse statement left out they match (This study, 2026).")
_b('SkipHeaderWithNext',
 "Project 13 skips the first row with an if on line_num and a continue [S]. The Python documentation describes the reader as an iterator, so the built-in next() gives its next row [PY].",
 "next(reader) dropped the header record h1,h2 and left the rest, and next(reader, None) did not fail on empty input where next(reader) raised StopIteration (This study, 2026).")
_b('EmptyAndHeaderOnly',
 "Project 13 reads each file into csv_rows, writes the rows to a file in headerRemoved and opens every name that ends with .csv, and the shipped removeCsvHeader.py does the same [S]. The online materials ship 100 CSV files with one-line headers [S].",
 "On the 100 files every output equalled the input without its first record and the printed lines were in the order os.listdir gave, not sorted as the page shows; for an empty file and a header-only file the output was empty, a final line without a break was kept, and a two-line header was kept whole because line_num was 2 at its end (This study, 2026).")
_b('WorkbookCells',
 "The practice program tells the reader to use openpyxl, load each workbook, loop over the sheet names and write one CSV per sheet named for the file and the sheet [S]. The openpyxl documentation describes the library as reading and writing Excel 2010 xlsx files [OPENPYXL].",
 "A workbook with two rows held datetime objects for the date cells, number format yyyy-mm-dd h:mm:ss, max_row 2 and max_column 3, and csv.writer wrote the dates as 2035-04-05 13:34:02, not as the 4/5/2035 13:34 that Excel shows (This study, 2026).")
_b('MaxColumnQuadratic',
 "The practice program's skeleton loops for row_num in range(1, sheet.max_row + 1) and, inside it, for col_num in range(1, sheet.max_column + 1) [S]. In openpyxl 3.1.5 the docstring of max_column says the maximum column index containing data and the code takes the maximum over every cell of the sheet on each call (This study, 2026).",
 "On a sheet of 3,000 rows of 4 columns the loop over 150 rows with max_column inside took more than 20 times as long as with it hoisted; on produceSales3.xlsx the first 2,000 rows took 5.94 s against 0.006 s (This study, 2026).")
_b('SizeComparison',
 "The chapter says the human-readable plaintext formats do not make the most efficient use of disk space or memory, and that XML is quite verbose compared to JSON [S]. The Alice data of the chapter is written in each format [S].",
 "The compact JSON was 248 characters and indent=2 made it 326; the XML without whitespace was 407, 1.64 times the JSON, and 563 as printed; the repr of the Python dict was 248 (This study, 2026).")
_b('TypesKept',
 "The chapter says XML text has no data type, that CSV has no data types and every value is a string, that JSON keeps null and the Booleans, and that TOML is chiefly for configuration [S]. The tomllib documentation says it parses TOML from a readable binary file and has no function to write [TOMLLIB].",
 "JSON kept int, None and bool through a round trip; xmltodict gave str for age and programmer and a dict for car; CSV gave all strings, with an empty field for None; tomllib kept int, bool and datetime, has no null and has no dumps (This study, 2026).")

PUBS.sort(key=lambda p: p[0])
_CITE = {
 "S": "(Sweigart, 2025)", "APPA": "(Sweigart, 2025, Appendix A)", "APPB": "(Sweigart, 2025, Appendix B)", "PY": "(Python Software Foundation, 2026)",
 "WN": "(Python Software Foundation, 2026, What's New)", "WN314": "(Python Software Foundation, 2025)", "IO": "(Python Software Foundation, 2026, io)", "CODECS": "(Python Software Foundation, 2026, codecs)", "LOCALE": "(Python Software Foundation, 2026, locale)",
 "MINIDOM": "(Python Software Foundation, 2026, minidom)", "SAX": "(Python Software Foundation, 2026, sax)", "TOMLLIB": "(Python Software Foundation, 2026, tomllib)", "TRACEMALLOC": "(Python Software Foundation, 2026, tracemalloc)",
 "PEP305": "(Altis et al., 2003)", "PEP686": "(Inada, 2022)", "RFC4180": "(Shafranovich, 2005)", "IANA": "(Internet Assigned Numbers Authority, n.d.)", "RFC8259": "(Bray, 2017)", "ECMA": "(Ecma International, 2017)",
 "W3C": "(World Wide Web Consortium, 2008)", "W3C98": "(World Wide Web Consortium, 1998)", "NS": "(World Wide Web Consortium, 2009)", "XSD": "(World Wide Web Consortium, 2004)",
 "PYPI": "(Python Package Index, 2026)", "DEFUSED": "(defusedxml contributors, 2021)", "OPENPYXL": "(openpyxl contributors, 2024)", "WP": "(Wikipedia, 2026)", "CWE": "(MITRE, 2026)", "OWASP": "(OWASP, 2026)",
 "P02": "(No Starch Press, 2025)", "T": "(This study, 2026)",
}
for _k in list(BODY):
    _t = BODY[_k]
    for _n, _v in _CITE.items():
        _t = _t.replace("[" + _n + "]", _v)
    BODY[_k] = _t.replace('"', "'")
