"""Chapter 14 deck speaker notes, version 3.0.0: READER notes (handover of 2026-11-19, practice 3). The slides are handed to students together with their notes, so each note explains the slide's short wording in
fuller sentences, adds detail that the slide does not carry, and connects the slide to related slides and chapters. A note gives no direction to a presenter, has no think-of statement, no prompt marker, no
lambda and no everyday picture. The facts are those of the chapter's examples, of their runs and of the chapter research of deck 2.0.0 (findings F3 to F14). RESULT_SAYS: for each code slide, the first result balloon (what the run showed).
Slide numbers: 1 title, 2 route, 3 questions, 4 part 1, 5 A1, 6 xlsx_zip, 7 ooxml story, 8 sheets, 9 openpyxl story, 10 A2, 11 cell_read, 12 bricklin story, 13 col_letters, 14 slices, 15 A3, 16 dates, 17 ziemann story,
18 touching, 19 read_only, 20 part 2, 21 A4, 22 census_read, 23 census_tally, 24 census_file, 25 produce_update, 26 part 3, 27 A5, 28 write_workbook, 29 formula_string, 30 excel story, 31 round_halves,
32 herndon story, 33 insert_rows, 34 part 4, 35 A6, 36 A7, 37 mult_table, 38 fonts, 39 dimensions, 40 merge, 41 freeze, 42 part 5, 43 A8, 44 chart_build, 45 reference_order, 46 chart_parts, 47 tools,
48 current, 49 summary, 50 practice, 51 resources."""
__version__ = "3.0.0"

NOTES = {
    "title": "This chapter of the book, Excel Spreadsheets, explains how a Python program reads and writes Excel workbooks with the library openpyxl: the file, its sheets and cells, two projects on real data, formulas, "
             "looks and layout, and charts. The deck has twenty-four code examples that run on the chapter page, six true stories about spreadsheets and their tools, and tables where a comparison helps. "
             "Slide 2 lays out the five parts. Chapter 13 comes before it with web scraping, and chapter 15 follows with Google Sheets.",
    "route": "The table is the map of the chapter. Each row is one of the five parts, with the slides it covers, the number of code examples and what you will run in it. The last row covers the tools table, the "
             "changes against the book, the summary, the practice questions and the links. The same twenty-four examples are listed in the Slide code tab of the chapter page, in this order, so a slide and its "
             "tab can be opened side by side. Part 1 starts on slide 4, and each later part begins with a divider slide that names its four ideas.",
    "questions": "Two questions run through the chapter, and the deck answers them near the end. The first asks which object of openpyxl stands for which part of a workbook, and what the library keeps of what a "
                 "spreadsheet program stored; the answer is the table on slide 47. The second asks where the book's printed outputs, programs and files differ from current Python and the current library; slide 48 "
                 "lists those changes from the chapter research. Keeping both questions in mind makes each later slide easier to place.",
    "divider1": "Part 1 is about reading a workbook. An .xlsx file is a zip of XML parts, a workbook holds sheets, a sheet holds cells, and the columns carry letters that count like a number without a zero. "
                "The four cards are the ideas of the part. Slides 5 to 19 cover them: the zip, the sheets, cells by name and by number, column letters, slices, data types, the fact that looking at a cell creates it, "
                "and read-only mode. Part 2 later puts this reading to work on a larger sheet.",
    "divider2": "Part 2 is about two projects on real data. Project 9 reads a census sheet row by row and tallies tracts and population by county; Project 10 corrects the prices of a produce sheet and keeps its formulas. "
                "The four cards are the ideas of the part. The files of the book are replaced by small stand-ins with the same columns, so every example runs on the chapter page. Slides 21 to 25 cover them, and "
                "part 1 earlier explains the cells and rows that the projects read.",
    "divider3": "Part 3 is about writing and formulas. A workbook is written with save, which replaces the whole file. A formula is only text that starts with an equal sign; a spreadsheet program calculates it and "
                "stores the result, which data_only reads back. The fourth card, insert_rows, moves values but not the references in formulas. The four cards are the ideas of the part. Slides 27 to 33 cover them.",
    "divider4": "Part 4 is about looks and layout. A font is a style object that cannot be changed and keeps only what it is given. Row height is measured in points, column width in characters, a merged range keeps one "
                "real cell, and freeze panes pins rows and columns to the window. The four cards are the ideas of the part. Slides 35 to 41 cover them, and part 3 earlier explains why none of these settings "
                "changes a value.",
    "divider5": "Part 5 is about charts. openpyxl writes a description of the chart into the file, and a spreadsheet program draws it. Reference names the cells of the data, Series wraps them with a title, BarChart is the "
                "chart itself and add_chart places it on the sheet. The four cards are the ideas of the part. Slides 43 to 46 cover them, and part 4 earlier shows the other settings that the library stores "
                "without drawing.",
    "A1": "A workbook is the whole .xlsx file seen as one object, and openpyxl reads and writes it without Excel. The rows give a plain meaning to each idea of the file: the reading of an existing file with "
          "load_workbook, the zip of XML parts inside it, the library, the new workbook that starts with one blank sheet, the writing of a document, and save, which replaces a file of the same name. Slide 6 "
          "opens a new workbook and lists the parts of its zip, and slide 28 writes one.",
    "A2": "A sheet is a grid of rows and columns, and every cell has a name such as B2 and also a row number and a column number. The rows explain the sheet, the active sheet that was open when the file was saved, "
          "create_sheet, the cell and the cell call, the utils module, and the two converters between column numbers and letters. Slide 8 shows the sheets in code, slide 11 the cells, and slide 13 the two converters.",
    "A3": "A big sheet is read one row at a time, so that the whole sheet need not be held in memory. Iter_rows hands out the rows, and read-only mode reads a file in that way and cannot write. The third row, "
          "insert_rows, belongs to writing: values move down, but formulas that refer to them do not change. Slide 19 shows read-only mode in code and slide 33 shows insert_rows.",
    "A4": "A project reads a sheet, works on its values and writes a result. The rows give plain meanings to Project 9 and the census tract it counts, to setdefault, pprint and pformat that build and save the tally, "
          "to Project 10 that corrects prices, to the sys module that holds the command line, and to the practice programs of the chapter. Slides 22 to 25 show the two projects in code.",
    "A5": "A formula is text that starts with an equal sign, and a spreadsheet program, not openpyxl, calculates it. The rows explain the formulas of the chapter, the string with data type f, the cached result that "
          "a spreadsheet program stores with the formula, and the option data_only that returns the cached results instead of the formulas. Slide 29 shows the difference in code, and slide 33 shows how a "
          "formula keeps its old references.",
    "A6": "Looks are objects and settings that openpyxl stores; they do not change the numbers. The rows explain setting a font through a Font object that keeps only the options it is given and cannot be changed "
          "afterwards, the styles module, and the adjusting of rows and columns, with height in points and width in characters. Slide 37 gives a practice program, slide 38 shows the fonts and slide 39 shows the "
          "dimensions.",
    "A7": "Merging joins cells into one, and freezing keeps the first rows and columns in view while the sheet scrolls. A merged range keeps one real cell, the top-left one, and the others are read-only; unmerge "
          "splits the block again and leaves the value in the top-left cell. Freeze panes keeps the rows above and the columns left of a chosen cell in view. Slide 40 shows the merge and slide 41 shows freezing.",
    "A8": "openpyxl writes a description of the chart, and Excel or LibreOffice draws it. The rows explain the chart as the object saved in the file, the chart module, Reference that names the cells by their "
          "corners with the column first, Series that wraps them with a title, BarChart that draws the series as bars, and add_chart that places the chart at a chosen cell. Slide 44 builds the chart, slide 45 "
          "shows the order of Reference, and slide 46 looks inside the file.",
    "xlsx_zip": "An .xlsx file is an ordinary zip archive, and openpyxl writes and reads its parts. A new workbook holds nine parts: the content types, the relationships, the document properties, the workbook, one "
                "sheet, the styles and a theme. The workbook is saved into memory here, so the example needs no file on disk. The list of names is the proof that the file is a zip. The story on slide 7 tells "
                "how this format became a standard.",
    "sheets": "A new workbook has one sheet named Sheet. Create_sheet adds one at the end, or at the index you give, so Sheet3 comes second and Sheet2 last. Load_workbook opens the saved bytes again, and sheetnames "
              "lists the sheets in tab order. The active sheet is the one that was open when the file was saved. Slide 28 uses the same calls to write and remove sheets.",
    "cell_read": "Append writes a row below the last used row, so three rows of two values fill A1 to B3. A cell is found by its name, A1, or by row and column number with cell. Max_row and max_column give the size of "
                 "the used area, and a Cell object prints with its sheet and coordinate. The names and numbers of columns are converted on slide 13, and the cell is created by looking at it on slide 18.",
    "col_letters": "Column letters are a number system without a zero: after Z comes AA, so column 27 is AA and column 900 is AHP. The last column of a sheet is XFD, number 16,384. Column 0 does not exist, and a number "
                   "outside the range raises a ValueError. These two converters are in the utils module, and slide 11 shows the cells that they name.",
    "slices": "A slice such as A1:C2 gives a tuple of rows, and each row is a tuple of cells; here two rows of three cells. The name B alone gives a whole column. The properties rows and columns are generators, so a "
              "loop can read them once but they cannot be indexed. Slide 19 shows iter_rows, the generator that reads a big sheet row by row.",
    "dates": "Every cell has a data type: n for a number, s for a string, d for a date and f for a formula. A datetime stays a date, a string stays a string, and a number stays a number. A gene symbol like SEPT2 "
             "written as a string is never turned into a date by openpyxl, which is the point of the story on slide 17. Slide 29 shows the type f.",
    "touching": "Looking at a cell creates it. A sheet with one value in A1 has one used row; one look at row 40 made the cell, and max_row became 40 and the dimensions A1:A40. A loop up to max_row then reaches empty "
                "rows, which is how Project 9 can fail. Read the dimensions before you loop. Slide 22 shows the loop of Project 9, and slide 19 shows a way to read without creating cells.",
    "read_only": "Read-only mode reads a file row by row and uses little memory; the sheet is a ReadOnlyWorksheet and cannot be written. Iter_rows with values_only gives plain tuples of values, here rows 2 to 4. On the "
                 "real census file of the chapter, the cell loop peaked at 114 MB and read-only iteration at 11 MB, a finding of the chapter research. Slide 15 gives the plain meaning of read-only mode, and part 2 reads a larger sheet.",
    "census_read": "Project 9 begins with a sheet of census tracts. Row 1 holds the headers, so the loop starts at row 2. Columns B, C and D hold the state, the county and the population. The real file has 72,865 rows; "
                   "the stand-in has three. The loop reads each row by its cell names, which slide 11 explained. The tally of these values follows on slide 23.",
    "census_tally": "Project 9, the tally. Setdefault creates a missing key once and leaves an existing key alone, first for the state and then for the county. Each row then adds one tract and its population to the "
                    "county. Anchorage ends with two tracts and 7,155 people, and Autauga with two tracts and 4,082. Slide 24 saves this dictionary as Python text.",
    "census_file": "Pformat turns the dictionary into text that is valid Python. The book writes that text to a file, census2010.py, and imports it; here exec reads the same text back into a dictionary so that the "
                   "example needs no file. The population of Anchorage is read from it again, 7,155. Pformat sorts the keys, so pop comes before tracts. Project 10 follows on slide 25.",
    "produce_update": "Project 10 corrects wrong prices in a produce sheet. The prices of garlic and celery are replaced by the values of a dictionary, and the formula in column D of each row is not touched. The book "
                      "saves the result under a new name so that the original file is kept. A formula is text that starts with an equal sign; slide 29 shows what openpyxl does and does not do with it.",
    "write_workbook": "A new workbook, a renamed sheet, a filled cell, a sheet created at index 0, a sheet created at index 2 and removed again: the sheet names end as First Sheet and Spam Bacon Eggs Sheet. Save writes the whole "
                      "workbook and replaces an old file without asking. Loading the bytes again proves what was written. Slide 8 explained create_sheet and load_workbook.",
    "formula_string": "A formula is a string that starts with an equal sign, and its data type is f. Python only stores the text; it does not calculate. Data_only=True asks for the result that a spreadsheet program "
                      "stored, and a file that openpyxl wrote has none, so the answer is None. A spreadsheet program must open and save the file first. Slide 25 corrected prices without touching such formulas.",
    "round_halves": "A spreadsheet's ROUND takes a half away from zero, while Python rounds the binary number that it holds. 0.125 is exact in binary and goes to the even digit, 0.12, and the other three sit just off the "
                    "half, so Python gives 1.0, 2.67 and 65.2 where the decimal rule gives 1.01, 2.68 and 65.21. On the real produce file the two differed in 629 of 23,757 rows. Decimal with ROUND_HALF_UP gives "
                    "the spreadsheet's answer. Slide 29 showed another difference between a spreadsheet and Python.",
    "insert_rows": "The practice program reads a row number and a count from sys.argv; a list stands in for the command line here. Two blank rows were inserted at row 3, the values moved down, and the sum moved to "
                   "B8. But it still says B1:B5: insert_rows does not rewrite references inside formulas, nor merged ranges or row heights. The repair is the practice program of slide 50.",
    "mult_table": "The practice program in a small size: N is 4. The first row and the first column hold the headings 1 to N in bold, and every other cell holds the product of its row heading and its column heading. One "
                  "Font object is made for each heading cell. The corner A1 was never written, so it prints as None. Slide 38 explains what a Font keeps.",
    "fonts": "A style object keeps only the options it was given. A1 has a size of 24 and no name; B3 has a name and bold but no size; C5 was never styled and shows the default, Calibri 11. A style object cannot be "
             "changed in place: assigning bold to it raises an AttributeError, and the way to change one option is to assign a new Font. Slide 37 shares one Font among many cells.",
    "dimensions": "Row height is measured in points and column width in characters. The example sets row 5 to 70 and column B to 20, and hides column D, which stays in the file. Reading a dimension creates it too, so "
                  "only the rows and columns that were set are listed: B and D, and row 5. Slide 18 showed the same creation for cells.",
    "merge": "After merge_cells on F1:I3 only the top-left cell F1 is a real Cell; the other eleven are MergedCell objects, and a merged cell is read-only, so writing to G2 raises an AttributeError. Unmerge gives "
             "ordinary empty cells back, and the text stays in the top-left cell, so after unmerge the sheet holds no merged range and G2 is a plain Cell again. Insert_rows on slide 33 does not move merged ranges, "
             "and slide 36 gives the plain meanings of merge and freeze.",
    "freeze": "The cell you name is the first one that scrolls. A2 freezes row 1, which the pane records as ySplit 1; B1 freezes column A, recorded as xSplit 1; and C2 freezes both. The view is "
              "saved in the sheet's pane. Nothing here changes a value: freezing is a setting of the view. Slides 39 and 40 showed other settings of this part that are stored in the sheet.",
    "chart_build": "Ten squares in column A are the data. Reference names the cells by their corners, Series wraps them with a title, BarChart is the chart itself, and add_chart places it on the sheet at C2. The printed "
                   "reference is 'Sheet'!$A$1:$A$10 and the sheet holds one chart. The application draws the chart when it opens the file. Slide 45 shows the order of the numbers of Reference.",
    "reference_order": "The order is min_col, min_row, max_col, max_row: column first. Reference(ws, 2, 1, 2, 10) names column B from row 1 to row 10, and Reference(ws, 1, 2, 10, 2) names row 2 from column A to column J. The "
                       "chapter's text says row first, and its own example hides the mistake because the block is square. Slide 48 lists this among the changes.",
    "chart_parts": "A chart is stored as XML inside the zip: a drawing part, its relationships and a chart part of their own. openpyxl writes the XML that describes the chart, and the application that opens the file "
                   "draws it. This is the same zip as on slide 6, with three more parts: a chart part, a drawing part and the relationships of the drawing. The example saves the workbook into memory and lists only the names that hold chart or drawing, so the chart is shown to be part of the file and not of the library. Slide 44 builds a chart, and slide 45 explains the numbers that name its cells.",
    "compare_tools": "The table sums up what openpyxl keeps and what it does not do. It stores values and formulas as text, the settings of looks and the orders for charts. It does not calculate a formula, keep a result "
                     "unless an application stored one, fix references after insert_rows, or draw a chart or a font. Looking at a cell creates it, and a file from outside is not safe against XML bombs until "
                     "defusedxml is installed. The last column names the slide of each answer: slides 18, 29, 33, 46 and 48.",
    "current": "The book's scripts and outputs differ from today's in places. The table lists each change with its version or date and what it means for the chapter; the last column names the slide whose example "
               "it touches. The online scripts use removed names, Reference takes the column first, a saved workbook loses formula results, and ROUND and round differ on exact halves. The library itself is stable "
               "and quiet; install defusedxml before you open a file you did not make. Slide 3 asked this question.",
    "summary": "Five ideas are worth keeping. An .xlsx file is a zip, a workbook holds sheets, and a sheet holds cells. Cells have names, numbers and data types, and looking at one can create it. A formula is text "
               "that a spreadsheet program calculates. Fonts, sizes, merges and frozen panes are objects and settings. A chart is a drawing order that an application draws. The chart counts the code examples of "
               "each part; see the route on slide 2.",
    "practice": "Four short drills close the chapter. The first converts column letters and numbers, the second asks where a formula goes when rows are inserted, the third asks what a Reference names, and the "
                "fourth is a practice program that repairs the Blank Row Inserter. Each answer fits in a few lines that can be run on the chapter page. The code of slides 13, 33 and 45 holds what the drills need.",
    "resources": "Start with the chapter of the book and the documentation of openpyxl, then the Python documents of the modules used. The stories link to first-hand sources: Dan Bricklin's own account of the idea, the "
                 "Library of Congress description of the format, and the gene-name paper. Chapter 13 and chapter 15 of the same book come before and after this one. Choose one link and read it before "
                 "the next class.",
}

STORY_NOTES = {
    "bricklin": "Dan Bricklin had the idea in spring 1978 at Harvard Business School, and his journal dates the first Apple II prototype to 8 October 1978. The grid of named rows and columns that he wanted is the "
                "grid that openpyxl still addresses, with cell names such as A1. The photograph shows him at a conference in 2010, long after the idea. Slide 11 shows the names of cells in code.",
    "excel": "Excel for the Macintosh was announced on 2 May 1985 and went on sale on 30 September of that year. It kept a Lotus 1-2-3 bug on purpose, the day 29 February 1900, and the file format still carries "
             "it. A file format keeps the habits and the bugs of the program that made it. The photograph shows a Macintosh with Excel 1.0. Slide 31 shows another place where a spreadsheet differs from Python.",
    "ooxml": "An .xlsx file is a documented zip of XML. Ecma approved it in December 2006 and ISO in early 2008. The photograph is a rally in Oslo about the ISO vote, not the format itself. Because any program may read "
             "the format, openpyxl can read and write it without Excel. Slide 6 shows the zip in code, and slide 9 tells the story of the library that does it. The same family of formats covers other "
             "Office files, which the Library of Congress page below describes.",
    "openpyxl": "openpyxl began in 2010 because Python had no library for the format, and its first upload to PyPI was on 11 August 2010. Its volunteers still maintain it; the newest release is 3.1.5 of June 2024. "
                "The picture is the logo of its documentation, shown enlarged, and not a picture of its authors. Say which release you ran, as slide 48 does.",
    "herndon": "In April 2013 three economists found a coding error in a published spreadsheet: five countries had been left out. The picture is the title page of the paper that they tested, not a photograph of the "
               "three. A formula is code, so it needs a second reader and a test. Slide 29 shows what a formula is for openpyxl, and slide 31 shows another place where a spreadsheet and Python give different answers.",
    "ziemann": "Excel turns gene symbols such as SEPT2 into dates by default. In 2016 three researchers counted errors in 704 of 3,597 papers with gene lists, which is 19.6 percent. The picture is Figure 1 of their "
               "paper. Check what a spreadsheet application did to your data before you trust it. Slide 16 shows that openpyxl keeps a string as a string.",
}

RESULT_SAYS = {
    "xlsx_zip": "A new workbook is a zip of nine parts.",
    "sheets": "The sheets are Sheet, Sheet3 and Sheet2; Sheet is active.",
    "cell_read": "A1 is Apples and row 2, column 2 is 85.",
    "col_letters": "Column 27 is AA, column 900 is AHP and the last is XFD.",
    "slices": "A slice gave two rows of three cells.",
    "dates": "A date, a string and a number keep their own types.",
    "touching": "One look at row 40 made the sheet 40 rows tall.",
    "read_only": "The sheet is read-only; rows 2 to 4 came out as tuples.",
    "census_read": "Each row gives state, county and population.",
    "census_tally": "Anchorage has two tracts and 7,155 people.",
    "census_file": "The tally became Python text, and exec read it back.",
    "produce_update": "The prices of garlic and celery were replaced.",
    "write_workbook": "The sheets are First Sheet and Spam Bacon Eggs Sheet.",
    "formula_string": "The formula has type f; its cached result is None.",
    "round_halves": "Python and the decimal rule differ at the halves.",
    "insert_rows": "Two blank rows came in, and the sum still says B1:B5.",
    "mult_table": "The grid holds the products; the corner is None.",
    "fonts": "A1 has a size and no name; C5 shows the default.",
    "dimensions": "Row 5 is 70 points high and column B is 20 wide.",
    "merge": "F1:I3 is merged and G2 is a MergedCell.",
    "freeze": "A2 splits one row, B1 one column, C2 both.",
    "chart_build": "The reference names A1 to A10 and one chart is on the sheet.",
    "reference_order": "Column first: B1 to B10, and A2 to J2.",
    "chart_parts": "The zip holds a chart part and a drawing part.",
}
