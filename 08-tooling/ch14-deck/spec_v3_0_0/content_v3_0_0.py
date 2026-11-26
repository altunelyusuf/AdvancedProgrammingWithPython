"""Chapter 14 deck content, version 3.0.0: the words of the deck for the generic builder (parts, plan, route, questions, plain meanings, stories, take-aways, tables, summary, practice, resources).
The chapter's content is that of deck 2.0.0 (deck_content_v2_0_0.py and the plan and parts of the chapter's own builder deck_build_v2_0_0.py); what the rulings force is changed: the everyday pictures
become plain meanings (no analogy anywhere; the box label is IN SHORT), the six stories are the same stories with the same facts and links, told as prose in paragraphs of at most 30 words, the
table of tools is a comparison slide of its own kind, and the notes are notes_v3_0_0.py."""
__version__ = "3.0.0"

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "In short"
CONCEPTS_TAIL = "each with a plain meaning"

PARTS = {
    1: ("Part 1: Reading a workbook", "An .xlsx file is a zip; a workbook holds sheets, and a sheet holds cells", [
        ("xlsx file", "A zip of XML parts that openpyxl opens."),
        ("Workbook", "The whole file, holding a list of sheets."),
        ("Cell", "One box with a name, a value and a type."),
        ("Column letter", "A number written in letters, without a zero."),
    ]),
    2: ("Part 2: Two projects on real data", "Read and tally a census sheet, then correct the prices of a produce sheet", [
        ("Project 9", "Tally tracts and population by county."),
        ("setdefault", "Creates a missing key once, never twice."),
        ("pformat", "Writes the result as Python text."),
        ("Project 10", "Corrects prices and keeps the formulas."),
    ]),
    3: ("Part 3: Writing and formulas", "A formula is only text; an application calculates it and caches the result", [
        ("save()", "Writes the whole workbook and replaces the old file."),
        ("Formula", "Text that starts with an equal sign."),
        ("data_only", "Reads the result an application stored."),
        ("insert_rows", "Moves values but not the references."),
    ]),
    4: ("Part 4: Looks and layout", "Fonts, sizes, merges and frozen panes are objects and settings", [
        ("Font()", "A style object that cannot be changed."),
        ("Row height", "Measured in points, like type."),
        ("Merged cell", "Only the top-left cell stays real."),
        ("Freeze panes", "Pins rows and columns to the window."),
    ]),
    5: ("Part 5: Charts", "openpyxl writes the order; an application draws the chart", [
        ("Reference", "Names the cells of the data."),
        ("Series", "Wraps the cells with a title."),
        ("BarChart", "The chart itself, with its bars."),
        ("add_chart", "Places the chart on the sheet."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("code", "xlsx_zip"), ("story", "ooxml"), ("code", "sheets"), ("story", "openpyxl"), ("analogy", "A2"), ("code", "cell_read"),
        ("story", "bricklin"), ("code", "col_letters"), ("code", "slices"), ("analogy", "A3"), ("code", "dates"), ("story", "ziemann"), ("code", "touching"), ("code", "read_only"),
        ("divider", 2), ("analogy", "A4"), ("code", "census_read"), ("code", "census_tally"), ("code", "census_file"), ("code", "produce_update"),
        ("divider", 3), ("analogy", "A5"), ("code", "write_workbook"), ("code", "formula_string"), ("story", "excel"), ("code", "round_halves"), ("story", "herndon"),
        ("code", "insert_rows"),
        ("divider", 4), ("analogy", "A6"), ("analogy", "A7"), ("code", "mult_table"), ("code", "fonts"), ("code", "dimensions"), ("code", "merge"), ("code", "freeze"),
        ("divider", 5), ("analogy", "A8"), ("code", "chart_build"), ("code", "reference_order"), ("code", "chart_parts"),
        ("compare", "tools"),
        ("current",), ("summary",), ("practice",), ("resources",)]

ROUTE_RUNS = {1: "the zip, sheets, cells, letters, slices, dates", 2: "the census tally and the price correction", 3: "save, formulas, rounding, insert_rows",
              4: "fonts, sizes, merge, freeze panes", 5: "Reference, Series, BarChart"}

ROUTE_TAIL = ("Tools, changes, summary, practice, resources", "what openpyxl keeps, and what differs today")

QUESTIONS = [("1", "Which object of openpyxl stands for which part of a workbook, and what does it keep of what the spreadsheet program stored?",
              "Answer on slide %d: what openpyxl keeps, and what it does not do.", [("compare", "tools")]),
             ("2", "Which printed outputs, programs and files of the book differ in current Python and the current library?",
              "Answer on slide %d: the changes, from the chapter research.", [("current",)])]

QUESTIONS_TAKEAWAY = "openpyxl keeps what was stored; the application calculates and draws."

ANALOGIES = [
    ("A1", "In short: the file and the workbook", "A workbook is the whole .xlsx file as one object; openpyxl reads and writes it, and Excel need not be installed.", [
        ("Reading Excel Files", "Opens an existing .xlsx file with load_workbook and reads its sheets, cells and values."),
        ("xlsx file", "A ZIP archive of XML parts that holds the sheets, the strings and the styles."),
        ("openpyxl", "A third-party Python library that reads and writes .xlsx files."),
        ("workbook", "The whole file as one object; it holds a list of sheets."),
        ("Workbook()", "Makes a new workbook in memory; it starts with one blank sheet."),
        ("openpyxl.load_workbook()", "Opens a saved .xlsx file and returns its workbook."),
        ("Writing Excel Documents", "Builds a workbook in the program, then saves it as an .xlsx file."),
        ("save()", "Writes the whole workbook to a file; a file of the same name is replaced."),
    ]),
    ("A2", "In short: sheets and cells", "A sheet is a grid of rows and columns, and every cell is found by its name or by its row and column number.", [
        ("worksheet", "One sheet of a workbook: a named grid of rows and columns."),
        ("active sheet", "The sheet that was open when the file was last saved; wb.active returns it."),
        ("create_sheet()", "Adds a new sheet at the end, or at the index you give."),
        ("cell", "One box of a sheet, found by its name such as B2; it holds a value or a formula."),
        ("cell()", "Returns a cell by row number and column number, such as ws.cell(row=2, column=2)."),
        ("openpyxl.utils", "A module of small helpers, such as the two column converters."),
        ("get_column_letter()", "Turns a column number into its letters; 27 becomes AA."),
        ("column_index_from_string()", "Turns column letters into the number; AA becomes 27."),
    ]),
    ("A3", "In short: reading many cells", "A big sheet is read one row at a time, so that the whole sheet need not be held in memory.", [
        ("iter_rows()", "Hands out the rows of a sheet one at a time, as tuples of cells or of values."),
        ("read-only mode", "Reads a big file row by row without holding every cell in memory; such a sheet cannot be written."),
        ("insert_rows()", "Inserts empty rows into a sheet; values move down, but formulas that point at them do not change."),
    ]),
    ("A4", "In short: the two projects", "A project reads a sheet, works on its values and writes a result.", [
        ("Project 9: Reading Data from a Spreadsheet", "Reads the census sheet row by row and tallies the tracts and the population of each county."),
        ("census tract", "A small area for which the census counts people; each row of the sheet is one tract."),
        ("setdefault()", "A dictionary method that creates a missing key with a default value and leaves an existing key alone."),
        ("pprint", "A standard module that lays out data structures as readable text."),
        ("pprint.pformat()", "Returns that text as a string instead of printing it; the text is valid Python."),
        ("Project 10: Updating a Spreadsheet", "Reads a produce sheet, corrects wrong prices in it and keeps its formulas."),
        ("sys", "A standard module; sys.argv holds the words typed after the program's name."),
        ("Practice Programs", "Short programs that apply the ideas of the chapter: here a multiplication table and the Blank Row Inserter."),
    ]),
    ("A5", "In short: formulas and their results", "A formula is text that starts with an equal sign; a spreadsheet program calculates it, not openpyxl.", [
        ("Formulas", "Calculations written in cells; openpyxl stores them and does not calculate them."),
        ("formula", "A string that starts with an equal sign, such as =SUM(A1:A2); its data type is f."),
        ("cached result", "The value that a spreadsheet program stored with the formula when it last saved the file."),
        ("data_only", "An option of load_workbook that returns the cached results instead of the formulas."),
    ]),
    ("A6", "In short: fonts, rows and columns", "Looks are objects and settings that openpyxl stores; they do not change the numbers.", [
        ("Setting the Font Style of Cells", "Gives cells a font name, a size, bold or italic through a Font object."),
        ("Font()", "A style object that keeps only the options it is given; it cannot be changed afterwards."),
        ("openpyxl.styles", "The module that holds Font and the other style objects."),
        ("Adjusting Rows and Columns", "Sets the height of rows and the width of columns, and can hide columns."),
        ("row height", "Measured in points."),
        ("column width", "Measured in characters."),
    ]),
    ("A7", "In short: merge and freeze", "Merging joins cells into one; freezing keeps the first rows and columns in view while the sheet scrolls.", [
        ("merge_cells()", "Joins a block of cells into one."),
        ("merged cell", "Only the top-left cell of the block stays a real cell; the others are read-only."),
        ("unmerge_cells()", "Splits the block again; the value stays in the top-left cell."),
        ("freeze panes", "Keeps the rows above and the columns left of a chosen cell in view while the rest scrolls."),
    ]),
    ("A8", "In short: charts and their parts", "openpyxl writes a description of the chart; Excel or LibreOffice draws it.", [
        ("Charts", "A chart is added to a sheet from the data in its cells."),
        ("chart", "The chart object; it is saved as XML in the file."),
        ("openpyxl.chart", "The module that holds the chart types, Reference and Series."),
        ("Reference()", "Names a block of cells by its corners, column first."),
        ("Series()", "Wraps a Reference with a title as one series of data."),
        ("BarChart()", "A chart that draws its series as bars."),
        ("add_chart()", "Places a chart on a sheet, with its corner at a chosen cell."),
    ]),
]

STORIES = {
    "bricklin": dict(title="Story: a student pictured the spreadsheet in 1978", img="image_bricklin_talk.jpg",
                     prose=["Dan Bricklin, a student at Harvard Business School in Cambridge, Massachusetts, had the idea of an electronic spreadsheet in spring 1978.",
                            "He wanted numbers, formula results and text on a screen in rows and columns with human-friendly names, and built the screen in Basic on the school's timesharing system.",
                            "His journal dates the first prototype on an Apple II, borrowed from Dan Fylstra, to 8 October 1978.",
                            "With Bob Frankston he built VisiCalc, the first product, which came out for the Apple II in 1979."],
                     link="http://www.bricklin.com/history/saiidea.htm", linktext="The Idea, by Dan Bricklin (bricklin.com)"),
    "excel": dict(title="Story: Excel came to the Macintosh on 2 May 1985", img="image_excel_mac_1985.jpg",
                  prose=["On 2 May 1985 Steve Jobs of Apple and Bill Gates of Microsoft announced Excel for the Macintosh at a press conference at Tavern on the Green, New York City.",
                         "Lotus 1-2-3 had become the leading program, so Microsoft began a new spreadsheet in 1983, code-named Odyssey, after its Multiplan of 1982.",
                         "Excel went on sale on 30 September 1985; Excel 2.05, the first for Windows, followed on 19 November 1987.",
                         "Excel kept a Lotus bug on purpose: 29 February 1900 counts as a day. The Office Open XML format still carries it."],
                  link="https://en.wikipedia.org/wiki/Microsoft_Excel", linktext="Microsoft Excel (Wikipedia)"),
    "ooxml": dict(title="Story: the .xlsx format became a standard in 2006", img="image_ooxml_rally.jpg",
                  prose=["Microsoft submitted its Office formats to Ecma International, to make them a documented standard that any program may read.",
                         "Ecma set up the committee TC45 in December 2005 and approved ECMA 376 in December 2006; ISO/IEC 29500 followed in early 2008.",
                         "An .xlsx file is SpreadsheetML in a ZIP-based package, a zip of XML files; openpyxl opens it as any zip program can.",
                         "The photograph shows a rally in Oslo on 9 April 2008 about the ISO vote, not the format itself."],
                  link="https://www.loc.gov/preservation/digital/formats/fdd/fdd000395.shtml", linktext="OOXML Format Family (Library of Congress)"),
    "openpyxl": dict(title="Story: openpyxl was born in 2010", img="image_openpyxl_logo.png",
                     prose=["Eric Gazoni and Charlie Clark are named with openpyxl, a Python library that reads and writes Office Open XML files; volunteers maintain it in their spare time.",
                            "It began because no library could read and write the format natively from Python; the project was first based on PHPExcel.",
                            "The first upload to PyPI, openpyxl 1.1.0, is dated 11 August 2010; the newest release, 3.1.5, is of 28 June 2024.",
                            "It is written in Python, so Excel is not needed, and every program of chapter 14 is built on it. The picture is its logo."],
                     link="https://openpyxl.readthedocs.io/en/stable/", linktext="openpyxl documentation"),
    "herndon": dict(title="Story: a spreadsheet error left five countries out, 2013", img="image_rr_paper.jpg",
                    prose=["On 15 April 2013 Thomas Herndon, Michael Ash and Robert Pollin published a working paper at the Political Economy Research Institute of UMass.",
                           "They replicated Reinhart and Rogoff's study of public debt and growth, from the authors' own working spreadsheet.",
                           "A coding error had left out five countries: Australia, Austria, Belgium, Canada and Denmark.",
                           "With that and a weighting corrected, growth above 90 percent debt was 2.2 percent a year, not the published -0.1."],
                    link="https://peri.umass.edu/publication/does-high-public-debt-consistently-stifle-economic-growth-a-critique-of-reinhart-and-rogoff/",
                    linktext="Herndon, Ash and Pollin: a critique (PERI)"),
    "ziemann": dict(title="Story: Excel turned gene names into dates, 2016", img="image_gene_names_fig1.png",
                    prose=["By default Excel turns gene symbols such as SEPT2 and MARCH1 into the dates 2-Sep and 1-Mar; the problem was first described in 2004.",
                           "Mark Ziemann, Yotam Eren and Assam El-Osta screened 35,175 Excel files of 2005 to 2015 from 18 journals; Genome Biology published it on 23 August 2016.",
                           "They found gene lists in 3,597 papers and gene-name errors in 987 files from 704 papers: 19.6 percent.",
                           "In openpyxl a string stays a string, with data type s; no date is made of it."],
                    link="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-016-1044-7", linktext="Gene name errors are widespread (Genome Biology)"),
}

TAKEAWAY = {
    "xlsx_zip": "An .xlsx file is a zip of XML parts.", "sheets": "A workbook is a list of sheets; one is active.", "cell_read": "A cell has a name and a row and column number.",
    "col_letters": "Letters count like digits without a zero.", "slices": "A slice gives rows; a rows property is a generator.", "dates": "Numbers, text and dates keep their own data types.",
    "touching": "Looking at a cell can create it.", "read_only": "Read-only mode saves memory.", "census_read": "Row 1 is the header; the loop starts at row 2.", "census_tally": "Count with a dictionary and setdefault.",
    "census_file": "pformat writes a dictionary as Python.", "produce_update": "Change the cell, keep the formula.", "write_workbook": "Save writes the whole workbook.",
    "formula_string": "openpyxl stores a formula; it never calculates it.", "round_halves": "Binary rounding and decimal rounding differ at halves.",
    "insert_rows": "insert_rows does not fix formulas.", "mult_table": "One Font object can style many cells.", "fonts": "A style keeps only what it is given.",
    "dimensions": "Heights are in points, widths in characters.", "merge": "A merged range keeps one real cell.", "freeze": "The named cell is the first that scrolls.",
    "chart_build": "Reference, Series, BarChart, add_chart.", "reference_order": "Reference: column first, then row.", "chart_parts": "A chart is XML; an application draws it.",
}

COMPARES = {
    "tools": dict(title="What openpyxl keeps, and what it does not do", sub="From the chapter research; each answer has its slide",
                  rows=[["Question", "Answer of openpyxl", "Slide"],
                        ["Does it calculate a formula?", "No: it stores the text; a spreadsheet program calculates", "29"],
                        ["Does it keep the result of a formula?", "Only if you read with data_only=True; a saved file loses it", "29"],
                        ["Does looking at a cell change the file?", "Yes: the cell, and the sheet's size, are created", "18"],
                        ["Does insert_rows fix the formulas?", "No: values and styles move, references do not", "33"],
                        ["Does it draw a chart or a font?", "No: it writes XML; an application draws it", "46"],
                        ["Is a file from outside safe to open?", "Not against XML bombs; install defusedxml first", "48"]],
                  colw=[3.2, 4.8, 0.9], rowh=0.5, fs=12, takeaway="openpyxl keeps what was stored; it calculates and draws nothing."),
}

CURRENT_SUB = "What differs from the book, from the chapter research"

CURRENT = [["What changed", "What it means for the chapter", "Example"],
           ["get_sheet_by_name warns; get_highest_row is gone (openpyxl 3.1.5)", "The online scripts stop: use wb[name] and max_row", ""],
           ["Reference takes the column first (openpyxl 3.1.5)", "The chapter says row first; its example is square", "reference_order"],
           ["A saved workbook has no formula results (openpyxl 3.1.5)", "Project 10 saves None for D2; open and save in an application", "formula_string"],
           ["ROUND and round differ on exact halves (12 Oct 2026)", "629 of 23,757 rows of the real produce file", "round_halves"],
           ["Font() keeps only what it is given (openpyxl 3.1.5)", "Calibri 11 holds only for cells never styled", "fonts"],
           ["Looking at a cell creates it (openpyxl 3.1.5)", "Project 9's loop can reach empty rows", "touching"],
           ["The newest release is quiet but current (3.1.5, 28 Jun 2024)", "Runs the same on Python 3.12 to 3.14", ""],
           ["No guard against XML bombs (openpyxl documentation)", "Install defusedxml before you open a foreign file", ""]]

CURRENT_TAKEAWAY = "Run what the book printed; then check what changed."

SUMMARY_ANALOGY = "A summary keeps only the five ideas you need to take away from the lecture."

SUMMARY_POINTS = ["An .xlsx file is a zip; a workbook holds sheets, a sheet holds cells.",
                  "Cells have names, numbers and data types; looking can create them.",
                  "A formula is text: a spreadsheet program calculates it.",
                  "Fonts, sizes, merges and frozen panes are objects and settings.",
                  "A chart is a drawing order that an application draws."]

SUMMARY_TAKEAWAY = "openpyxl keeps what was stored; the application calculates and draws."

PRACTICE_SUB = "Predict first, then run what you can on the chapter page"

PRACTICE_ANALOGY = "Practice questions are short drills: predict the answer first, then run the code."

PRACTICE = ["Which letters name column 703, and which number has the name ZZ? Use the code of the column-letters slide.",
            "A sheet holds =SUM(B1:B5) in B6. Two rows are inserted at row 3. Where is the formula, and what does it add?",
            "What does Reference(ws, 3, 2, 3, 9) name? Write the range, then run it.",
            "Practice program: write a Blank Row Inserter that also fixes the SUM of the last row."]

PRACTICE_TAKEAWAY = "Each answer fits in a few lines you can run."

RESOURCES_SUB = "Reading and watching, chosen for this chapter; every link is live"

RESOURCES_TAKEAWAY = "Pick one link and read it before the next class."

RESOURCES = [
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 14", "https://automatetheboringstuff.com/3e/chapter14.html", "automatetheboringstuff.com"),
    ("openpyxl documentation: start page", "https://openpyxl.readthedocs.io/en/stable/", "openpyxl.readthedocs.io"),
    ("openpyxl tutorial: workbooks, data_only, copy", "https://openpyxl.readthedocs.io/en/stable/tutorial.html", "openpyxl.readthedocs.io"),
    ("openpyxl: working with styles", "https://openpyxl.readthedocs.io/en/stable/styles.html", "openpyxl.readthedocs.io"),
    ("openpyxl: charts, introduction", "https://openpyxl.readthedocs.io/en/stable/charts/introduction.html", "openpyxl.readthedocs.io"),
    ("openpyxl: optimised modes (read-only)", "https://openpyxl.readthedocs.io/en/stable/optimized.html", "openpyxl.readthedocs.io"),
    ("openpyxl on the Python Package Index", "https://pypi.org/project/openpyxl/", "pypi.org"),
    ("Python documentation: pprint", "https://docs.python.org/3/library/pprint.html", "docs.python.org"),
    ("Python documentation: decimal", "https://docs.python.org/3/library/decimal.html", "docs.python.org"),
    ("Python documentation: zipfile", "https://docs.python.org/3/library/zipfile.html", "docs.python.org"),
    ("Library of Congress: OOXML format family", "https://www.loc.gov/preservation/digital/formats/fdd/fdd000395.shtml", "loc.gov"),
    ("Dan Bricklin: The Idea (VisiCalc history)", "http://www.bricklin.com/history/saiidea.htm", "bricklin.com"),
    ("Gene name errors are widespread (Genome Biology)", "https://genomebiology.biomedcentral.com/articles/10.1186/s13059-016-1044-7", "genomebiology.biomedcentral.com"),
    ("defusedxml on the Python Package Index", "https://pypi.org/project/defusedxml/", "pypi.org"),
]
