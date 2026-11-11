# Chapter 18 Draft — CSV, JSON and XML (v1.0.1)

**Status note:** checked against live files: deck `SEN0414_Ch18_CSVJSONXML_3e_v2_0_1.pptx` (53 slides; v2_0_0 is superseded and not delivered), page `sen0414_ch18_page_v9_96_0.html`, manifest `chapter_code_ch18_v1_0_1.json` (27 examples), stories script (6 stories; each has a story slide in the deck: 6, 13, 28, 36, 42, 44). The page checks pass (Page/Ch18 PASS, 400 features). Repair cycle in October (page v9_95_0 to v9_96_0, deck v2_0_0 to v2_0_1) resolved. For your approval before any render step.

## 1. The story (6 beats, one per concept, sourced)

1. **1972, and by 1983 under the name CSV — The IBM Fortran (level H extended) compiler and the people who wrote spreadsheets for it.** Wikipedia's article on comma-separated values says the format predates personal computers by more than a decade: the IBM Fortran (level H extended) compiler under OS/360 supported list-directed free-form input and output, with commas between values, in 1972. List-directed input was defined in FORTRAN 77, approved in 1978, and it used commas or spaces as delimiters, so an unquoted string could not contain either. The term comma-separated value and the abbreviation CSV were in use by 1983. The quoting rule that lets a field hold a comma is the answer to that old limit: in this study the line with 'Hello, world!' in quotes split into five pieces with split(','), and into four fields with csv.reader. *Lesson: Never split a CSV line on commas yourself; let csv.reader read it.* (https://en.wikipedia.org/wiki/Comma-separated_values)

2. **October 2005 — Yakov Shafranovich, in the IETF's RFC series, with the text/csv media type registered at IANA.** RFC 4180, dated October 2005 and written by Yakov Shafranovich, is an Informational memo that documents the common format and registers the MIME type text/csv. It says each record is on a separate line delimited by a line break (CRLF), that the last record may or may not have an ending line break, and that a header line is optional. Fields with line breaks, double quotes or commas must be enclosed in double quotes, and a quote inside is written twice. Python's csv module follows these habits: in this study a record with a line break inside quotes read as one record on two lines, and a final record with no line break read the same as one with it. *Lesson: RFC 4180 describes common practice; real files still differ.* (https://www.rfc-editor.org/rfc/rfc4180)

3. **18 February 2005 — Jesse James Garrett, co-founder of Adaptive Path.** Heise says that Gmail, launched in 2004, and other web applications drew more and more questions from Garrett's clients about how to build such things, and that he saw the many technologies and abbreviations needed one accessible name. On 18 February 2005 he published the essay 'Ajax: A New Approach to Web Applications' on Adaptive Path's blog, naming Google Suggest and Google Maps as examples. The name stands for Asynchronous JavaScript + XML. In a question-and-answer added on 13 March 2005 Adaptive Path said it had not invented Ajax and that Ajax is not something you can download. The chapter's two plain-text formats sit in that name and beside it: XML is the X of Ajax, and the JSON and XML tools of this chapter read the kind of text a browser and a server pass to each other. *Lesson: The same plain-text formats that a script reads from a file are what web pages exchange with servers.* (https://heise.de/-10285844)

4. **10 February 1998, after work that began in mid-1996 — The W3C XML working group, started by Jon Bosak of Sun Microsystems.** Wikipedia's article on XML gives 10 February 1998 as the date XML 1.0 was first published as a W3C Recommendation. Work began in mid-1996 when the Sun Microsystems engineer Jon Bosak developed a charter and recruited collaborators who knew both SGML and the Web. The first edition of the specification, still on the W3C site, carries the date 10-February-1998; the fifth edition is dated 26 November 2008. The rules were made strict on purpose, which this study saw in ElementTree: the closing tag a for the opening tag A was a mismatched tag, and two roots were junk after the document element. *Lesson: XML is strict by design: one root, matching case, closed tags.* (https://en.wikipedia.org/wiki/XML)

5. **19 September 2006 and 1 October 2008 — Fredrik Lundh, whose ElementTree library was added, and Bob Ippolito, who wrote simplejson, which became json.** The 'What's New in Python 2.5' page says the release came out on 19 September 2006 and added a subset of Fredrik Lundh's ElementTree library as xml.etree, version 1.2.6 of the library, with the cElementTree accelerator. The 'What's New in Python 2.6' page, for the release of 1 October 2008, says json, originally called simplejson, was written by Bob Ippolito. The two modules of chapter 18 have therefore been in the standard library for 20 and 18 years. In Python 3.14.6 this study still imported xml.etree.cElementTree, though its documentation calls the alias deprecated, and found that getchildren() and getiterator() of the old tutorials are gone. *Lesson: Old tutorials use old names; check the release you run.* (https://docs.python.org/3/whatsnew/2.5.html)

6. **First reported as early as 2002, widely addressed from 2008 — Parser authors and security reporters, and the people who named it the billion laughs attack or XML bomb.** Wikipedia's article on the billion laughs attack says it targets XML parsers and is also called an XML bomb or an exponential entity expansion attack. The example defines 10 entities, each made of 10 of the one before, so one use of the largest expands to a billion copies of lol, almost 3 gigabytes. The problem was first reported as early as 2002 and began to be widely addressed in 2008; the article's references include the entry CVE-2003-1564. In this study a 760-byte file of that kind was refused by ElementTree in Python 3.14.6 with a limit on input amplification, and xmltodict 1.0.4 refused every entity, while xmltodict 0.13.0, the version Appendix A pins, parsed it. *Lesson: Never parse untrusted XML with a parser you have not checked.* (https://en.wikipedia.org/wiki/Billion_laughs_attack)


## 2. Slide / page-tab outline (53 slides, 27 code examples; the example number is the page-tab order)

| Slide | Title | Code example |
|---|---|---|
| 1 | >>> |  |
| 2 | Today's route |  |
| 3 | Two questions this chapter answers |  |
| 4 | Part 1: Reading CSV files |  |
| 5 | Everyday pictures: the CSV format |  |
| 6 | Story: Commas between values on IBM mainframes, 1972 |  |
| 7 | The CSV format: why split(',') is not enough | 1: Why not split on commas |
| 8 | Reading CSV files: reader(), list() and one value | 2: reader and list() |
| 9 | Accessing data in a for loop: one row at a time | 3: Reading in a for loop |
| 10 | Handling header rows: next() and line_num | 4: Handling header rows |
| 11 | Part 2: Writing CSV files |  |
| 12 | Everyday pictures: tabs, headers and line ends |  |
| 13 | Story: RFC 4180 wrote CSV down in October 2005 |  |
| 14 | Writing CSV files: writer() and writerow() | 5: writer and writerow() |
| 15 | Using tabs instead of commas: delimiter and lineterminator | 6: Tabs instead of commas |
| 16 | newline='' and the double-spaced file (Figure 18-1) | 7: newline='' and the double-spaced file |
| 17 | Quoting: six constants, one row | 8: Quoting and the quoting constants |
| 18 | The encoding the chapter never names: utf-8 and the BOM | 9: Encoding and the byte order mark |
| 19 | DictReader and DictWriter: rows as dictionaries | 10: DictReader and DictWriter |
| 20 | Part 3: Project 13, remove the header row |  |
| 21 | Everyday pictures: Project 13 |  |
| 22 | Project 13, step 1: loop through each file | 11: Project 13, step 1: loop through the files |
| 23 | Project 13, step 2: read the file, skip the first row | 12: Project 13, step 2: read the file |
| 24 | Project 13, step 3: write the new CSV file | 13: Project 13, step 3: write the new file |
| 25 | Ideas for similar programs: total a column | 14: Ideas for similar programs: totals |
| 26 | Part 4: JSON |  |
| 27 | Everyday pictures: JSON |  |
| 28 | Story: Ajax got its name on 18 February 2005 |  |
| 29 | Versatile plaintext formats: one record in CSV, JSON and XML | 15: Three plaintext formats |
| 30 | Reading JSON data: loads() and the six value types | 16: Reading JSON with loads() |
| 31 | Writing JSON data: dumps(), keys and a round trip | 17: Writing JSON with dumps() |
| 32 | JSON is strict: what json.loads() refuses | 18: What JSON refuses |
| 33 | JSON and files: dump(), load() and the byte order mark | 19: JSON and files |
| 34 | Part 5: XML |  |
| 35 | Everyday pictures: XML |  |
| 36 | Story: XML 1.0 became a W3C Recommendation in 1998 |  |
| 37 | Reading XML files: root, children, text and attributes | 20: Reading XML with ElementTree |
| 38 | ElementTree: whitespace stays, and broken XML raises ParseError | 21: Whitespace and errors in ElementTree |
| 39 | Writing XML files: Element, SubElement, tostring and indent | 22: Writing XML with ElementTree |
| 40 | Namespaces and xsi:nil: names are not what they seem | 23: Namespaces and xsi:nil |
| 41 | xmltodict: XML as a dictionary of strings | 24: xmltodict: XML as a dictionary |
| 42 | Story: ElementTree joined Python in 2006 and json in 2008 |  |
| 43 | XML from someone else: entities and defusedxml | 25: XML from someone else |
| 44 | Story: A small XML file that asks for a billion laughs |  |
| 45 | Part 6: Practice program, Excel to CSV |  |
| 46 | Everyday pictures: the practice program |  |
| 47 | Practice program: a workbook to convert | 26: Excel-to-CSV converter: the workbook |
| 48 | Practice program: write one CSV file for each sheet | 27: Excel-to-CSV converter: one CSV per sheet |
| 49 | Which call does what, and what it needs |  |
| 50 | What differs from the book today |  |
| 51 | Summary |  |
| 52 | Practice Questions |  |
| 53 | Resources: where to go next |  |

## 3. Resources slide (14 links, targets read from the deck's own hyperlinks)

1. https://automatetheboringstuff.com/3e/chapter18.html
2. https://docs.python.org/3/library/csv.html
3. https://docs.python.org/3/library/json.html
4. https://docs.python.org/3/library/xml.etree.elementtree.html
5. https://docs.python.org/3/library/xml.html
6. https://pypi.org/project/xmltodict/
7. https://pypi.org/project/defusedxml/
8. https://openpyxl.readthedocs.io/en/stable/
9. https://www.rfc-editor.org/rfc/rfc4180
10. https://www.json.org/
11. https://www.w3.org/TR/xml/
12. https://en.wikipedia.org/wiki/Comma-separated_values
13. https://en.wikipedia.org/wiki/Billion_laughs_attack
14. https://docs.python.org/3/whatsnew/2.6.html

## 4. Open items
- **Story 3 replaced (v1.0.1), owner rule of 2026-11-11:** the JSON-origin story (Crockford and Morningstar, April 2001) was already told in chapters 7 and 10, so it is replaced by the 2005 Ajax story. Render consequences: slide 28 and the matching page story are rewritten; the story needs a real picture from a free source (the Adaptive Path essay's own figure of the two web-application models is the candidate; its reuse terms are to be confirmed at render, otherwise a Wikimedia Commons picture). The 'one extra comma is an error' demonstration stays where it already is, on slide 32. The story has no code check of its own; it is history. The primary source, Garrett's essay on Adaptive Path, is read through a copy hosted at https://designftw.csail.mit.edu/lectures/apis/ajax_adaptive_path.pdf; the resources slide gets the story's link at render.
- No gap found against the story principle or the resources standard.
- Deck version note: `_v2_0_0.pptx` is superseded; `_v2_0_1.pptx` is the controlled file. Flagged so it is not mistaken for a second live version.
- No legacy duplicate deck to retire.
- `rdodi/` research-artifact folder left untouched (out of scope).
