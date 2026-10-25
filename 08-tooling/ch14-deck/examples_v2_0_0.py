"""Chapter 14 deck examples, version 2.0.0: the code examples of the chapter 14 lecture deck (Excel Spreadsheets).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language explanation that
stands beside it); the lines of all groups of an example, in order, are the example's code: that text is what the deck shows after the '>>> '
prompt of each line, what the chapter-code manifest lists and what the page runs. A code box holds at most 30 words (the deck standard counts
a code box as a text box), the explanation of a group at most 30 words.
Every example is self-contained (it imports what it uses), uses only openpyxl 3.1.5 and the Python standard library, builds its workbooks in memory
(io.BytesIO) instead of on disk, reads no keyboard, opens no network connection and no window, and prints an ordinary line first (never an error
message, so that the page can draw its result). The chapter's own files (example3.xlsx, censuspopdata.xlsx, produceSales3.xlsx) are replaced by
small stand-ins built in the example, with the same sheets, columns and formulas, and each slide says so beside the code.
Nothing here carries a result; deck_build_v2_0_0.py runs the code and takes every printed result from the run."""
__version__ = "2.0.0"

EXAMPLES = [
    # ------------------------------------------------------------ part 1: reading a workbook
    dict(id="xlsx_zip", name="An .xlsx file is a zip of XML parts", title="An .xlsx file is a zip of XML parts", part=1, visual="xlsx_zip",
         concepts=["xlsx file", "workbook", "Workbook()", "save()", "openpyxl"],
         groups=[
             (["import io, zipfile, openpyxl", "wb = openpyxl.Workbook()", "buf = io.BytesIO()", "wb.save(buf)"],
              "Workbook() makes a new workbook in memory. save() writes the .xlsx bytes; here into memory, so that this example needs no disk file."),
             (["names = sorted(zipfile.ZipFile(buf).namelist())", "print(len(names), 'parts in the zip')", "for name in names: print(name)"],
              "An .xlsx file is an ordinary zip archive. The names inside show what openpyxl keeps: the workbook, a sheet, the strings and the styles."),
         ]),
    dict(id="sheets", name="Sheets of a workbook: names, order, active", title="Sheets: create_sheet, sheetnames and the active sheet", part=1, visual="sheets",
         concepts=["worksheet", "create_sheet()", "active sheet", "openpyxl.load_workbook()"],
         groups=[
             (["import io, openpyxl", "wb = openpyxl.Workbook()", "wb.create_sheet('Sheet2')", "wb.create_sheet('Sheet3', 1)", "buf = io.BytesIO(); wb.save(buf)"],
              "A new workbook has one sheet named Sheet. create_sheet adds one at the end, or at the index you give. The stand-in for example3.xlsx goes into memory."),
             (["wb = openpyxl.load_workbook(buf)", "print(wb.sheetnames)", "print(wb.active.title, wb['Sheet3'].title)"],
              "load_workbook opens the saved bytes again. sheetnames lists the sheets in tab order, and the active sheet is the one that was open when the file was saved."),
         ]),
    dict(id="cell_read", name="Cells by name and by number", title="A cell by name, by row and column, and its coordinate", part=1, visual="cell_read",
         concepts=["cell", "cell()", "worksheet"],
         groups=[
             (["import openpyxl", "ws = openpyxl.Workbook().active", "for row in [('Apples', 73), ('Cherries', 85), ('Pears', 14)]:", "    ws.append(row)"],
              "append writes one row below the last used row. These three rows stand in for the chapter's fruit sheet."),
             (["print(ws['A1'].value, ws.cell(row=2, column=2).value)", "print(ws['B3'].coordinate, ws.max_row, ws.max_column)", "print(ws['A1'])"],
              "A cell is found by its name, A1, or by row and column number with cell(). max_row and max_column give the size of the used area."),
         ]),
    dict(id="col_letters", name="Column letters and numbers", title="get_column_letter and column_index_from_string", part=1, visual="col_letters",
         concepts=["get_column_letter()", "column_index_from_string()"],
         groups=[
             (["from openpyxl.utils import get_column_letter, column_index_from_string", "print([get_column_letter(n) for n in (1, 2, 27, 900)])",
               "print(column_index_from_string('AA'), column_index_from_string('XFD'))"],
              "Column 27 is AA, because the letters count like digits without a zero. Column 900 is AHP, and the last column of a sheet is XFD."),
             (["try:", "    get_column_letter(0)", "except ValueError as e:", "    print('ValueError:', e)"],
              "There is no column 0, and no column beyond 18278. The wrong number stops the program with a ValueError."),
         ]),
    dict(id="slices", name="Slices, rows and columns of cells", title="A slice of cells, one column, and the generators", part=1, visual="slices",
         concepts=["cell", "iter_rows()"],
         groups=[
             (["import openpyxl", "ws = openpyxl.Workbook().active", "for r in [(1, 'Apples', 73), (2, 'Cherries', 85), (3, 'Pears', 14)]:", "    ws.append(r)"],
              "A small sheet of three rows and three columns."),
             (["block = ws['A1':'C2']", "print(len(block), 'rows of', len(block[0]), 'cells')", "for row in block: print([c.value for c in row])"],
              "A slice such as A1:C2 gives a tuple of rows, and each row is a tuple of cells."),
             (["print([c.value for c in ws['B']])", "print(type(ws.rows).__name__, type(ws.columns).__name__)"],
              "ws['B'] is the whole column B. rows and columns are generators, so they can be looped over but not indexed."),
         ]),
    dict(id="dates", name="Data types of cells: numbers, text, dates", title="Every cell has a data type: number, text or date", part=1, visual="dates",
         concepts=["cell", "workbook"],
         groups=[
             (["import datetime, openpyxl", "ws = openpyxl.Workbook().active", "ws['A1'] = datetime.datetime(2035, 4, 5, 13, 34, 2)", "ws['B1'] = 'SEPT2'",
               "ws['C1'] = 73"],
              "Python values go into cells as they are: a datetime, a string that only looks like a gene name or a date, and a number."),
             (["print(ws['A1'].value)", "for c in ws[1]:", "    print(c.coordinate, c.data_type, type(c.value).__name__)"],
              "data_type is n for a number, s for a string and d for a date. A string stays a string: openpyxl never turns SEPT2 into a date."),
         ]),
    dict(id="touching", name="Looking at a cell creates it", title="Looking at a cell changes the workbook", part=1, visual="touching",
         concepts=["cell()", "worksheet"],
         groups=[
             (["import openpyxl", "ws = openpyxl.Workbook().active", "ws['A1'] = 'tall'", "print(ws.max_row, ws.dimensions)"],
              "A sheet with one value in A1 has one used row."),
             (["ws.cell(row=40, column=1)", "print(ws.max_row, ws.dimensions)", "print(ws['A40'].value is None)"],
              "Only looking at row 40 created the cell and raised max_row to 40. A loop up to max_row now reaches empty rows, which is how Project 9 can fail."),
         ]),
    dict(id="read_only", name="Read-only mode and iter_rows", title="Read-only mode: values row by row, with iter_rows", part=1, visual="read_only",
         concepts=["read-only mode", "iter_rows()"],
         groups=[
             (["import io, openpyxl", "ws = openpyxl.Workbook().active", "for i in range(1, 6): ws.append([i, i * 10])", "buf = io.BytesIO(); ws.parent.save(buf)"],
              "A stand-in file with five rows and two columns."),
             (["fast = openpyxl.load_workbook(buf, read_only=True)", "sheet = fast.active", "print(type(sheet).__name__, sheet.max_row)",
               "rows = list(sheet.iter_rows(min_row=2, max_row=4, values_only=True))", "print(rows)"],
              "read_only=True reads a big file row by row without holding every cell in memory. iter_rows with values_only gives plain tuples of values."),
         ]),
    # ------------------------------------------------------------ part 2: the two projects
    dict(id="census_read", name="Project 9: read the rows of the census sheet", title="Project 9: read the census sheet row by row", part=2, visual="census_read",
         concepts=["Project 9: Reading Data from a Spreadsheet", "census tract"],
         groups=[
             (["import openpyxl", "sheet = openpyxl.Workbook().active", "sheet.append(['CensusTract', 'State', 'County', 'POP2010'])"],
              "A stand-in for censuspopdata.xlsx: a header row, then one row for each census tract."),
             (["tracts = [('02020000100', 'AK', 'Anchorage', 4115),", "          ('02020000200', 'AK', 'Anchorage', 3040),", "          ('01001020100', 'AL', 'Autauga', 1912)]",
               "for tract in tracts: sheet.append(tract)"],
              "Three tracts in two states and two counties. The real file has 72,865 rows."),
             (["for row in range(2, sheet.max_row + 1):", "    print(row, [sheet[c + str(row)].value for c in 'BCD'])"],
              "Row 1 holds the headers, so the loop starts at row 2. Columns B, C and D hold the state, the county and the population."),
         ]),
    dict(id="census_tally", name="Project 9: tally tracts and population by county", title="Project 9: tally tracts and population with setdefault", part=2, visual="census_tally",
         concepts=["Project 9: Reading Data from a Spreadsheet", "setdefault()"],
         groups=[
             (["rows = [('AK', 'Anchorage', 4115), ('AK', 'Anchorage', 3040),", "        ('AL', 'Autauga', 1912), ('AL', 'Autauga', 2170)]"],
              "The values the last loop read from the sheet, typed in so that this example stands alone."),
             (["county_data = {}", "for state, county, pop in rows:", "    county_data.setdefault(state, {})"],
              "Start with an empty dictionary. setdefault creates the state's entry once and leaves an existing one alone."),
             (["    county_data[state].setdefault(county, {'tracts': 0, 'pop': 0})", "    county_data[state][county]['tracts'] += 1",
               "    county_data[state][county]['pop'] += pop", "print(county_data)"],
              "The same for the county, then add one tract and its population to it."),
         ]),
    dict(id="census_file", name="pprint.pformat writes the result as Python", title="pprint.pformat: save the tally as a Python file", part=2, visual="census_file",
         concepts=["pprint.pformat()", "Project 9: Reading Data from a Spreadsheet"],
         groups=[
             (["import pprint", "county_data = {'AK': {'Anchorage': {'tracts': 2, 'pop': 7155}},", "               'AL': {'Autauga': {'tracts': 2, 'pop': 4082}}}"],
              "The result of the tally of Project 9, typed in so that this example stands alone."),
             (["text = 'allData = ' + pprint.pformat(county_data)", "print(text)", "ns = {}", "exec(text, ns)", "print(ns['allData']['AK']['Anchorage']['pop'])"],
              "pformat turns the dictionary into text that is valid Python. The book writes it to census2010.py and imports it; here exec reads the text back."),
         ]),
    dict(id="produce_update", name="Project 10: correct the prices", title="Project 10: correct prices in a sheet of produce", part=2, visual="produce_update",
         concepts=["Project 10: Updating a Spreadsheet", "formula"],
         groups=[
             (["import openpyxl", "ws = openpyxl.Workbook().active", "ws.append(['PRODUCE', 'COST PER POUND', 'POUNDS SOLD', 'TOTAL'])",
               "ws.append(['Garlic', 1.19, 10.0, '=ROUND(B2*C2,2)'])", "ws.append(['Celery', 3.07, 4.5, '=ROUND(B3*C3,2)'])"],
              "A stand-in for produceSales3.xlsx. Garlic and celery carry wrong prices. The total of each row is a formula: text that starts with an equal sign."),
             (["updates = {'Garlic': 3.07, 'Celery': 1.19}", "for row in range(2, ws.max_row + 1):", "    name = ws.cell(row=row, column=1).value"],
              "The correct prices are a dictionary. The loop reads the name in column A of every row below the header."),
             (["    if name in updates:", "        ws.cell(row=row, column=2).value = updates[name]", "print([ws.cell(row=r, column=2).value for r in range(2, 4)])"],
              "When the name is in the dictionary, replace the price in column B. The formulas in column D are not touched."),
         ]),
    # ------------------------------------------------------------ part 3: writing documents and formulas
    dict(id="write_workbook", name="Writing a workbook: sheets and save", title="Writing a workbook: title, new sheets, remove, save", part=3, visual="write_workbook",
         concepts=["Writing Excel Documents", "Workbook()", "create_sheet()", "save()"],
         groups=[
             (["import io, openpyxl", "wb = openpyxl.Workbook()", "wb.active.title = 'Spam Bacon Eggs Sheet'", "wb['Spam Bacon Eggs Sheet']['A1'] = 'Hello, world!'"],
              "A new workbook, its sheet renamed, and A1 filled. Nothing is on disk yet."),
             (["wb.create_sheet(index=0, title='First Sheet')", "wb.create_sheet(index=2, title='Middle Sheet')", "wb.remove(wb['Middle Sheet'])", "print(wb.sheetnames)"],
              "create_sheet puts a sheet at a position; remove takes one away."),
             (["buf = io.BytesIO(); wb.save(buf)", "copy = openpyxl.load_workbook(buf)", "print(copy.sheetnames, copy['Spam Bacon Eggs Sheet']['A1'].value)"],
              "save writes the whole workbook, and replaces an old file without asking. Loading it again proves what was written."),
         ]),
    dict(id="formula_string", name="A formula is text; the result is cached", title="A formula is text, and openpyxl never calculates it", part=3, visual="formula_string",
         concepts=["Formulas", "formula", "cached result", "data_only"],
         groups=[
             (["import io, openpyxl", "ws = openpyxl.Workbook().active", "ws['A1'], ws['A2'] = 200, 300", "ws['A3'] = '=SUM(A1:A2)'", "print(ws['A3'].value, ws['A3'].data_type)"],
              "A formula is a string that starts with an equal sign. Its data type is f. Python only stores the text."),
             (["buf = io.BytesIO(); ws.parent.save(buf)", "kept = openpyxl.load_workbook(buf)['Sheet']", "cached = openpyxl.load_workbook(buf, data_only=True)['Sheet']",
               "print(kept['A3'].value, '|', cached['A3'].value)"],
              "data_only=True asks for the result that a spreadsheet program stored. This file was never opened in one, so there is no result: None."),
         ]),
    dict(id="round_halves", name="ROUND in a spreadsheet and round in Python", title="Exact halves: a spreadsheet's ROUND and Python's round", part=3, visual="round_halves",
         concepts=["formula", "cached result"],
         groups=[
             (["from decimal import Decimal, ROUND_HALF_UP", "for text in ('0.125', '1.005', '2.675', '65.205'):", "    x = float(text)",
               "    up = Decimal(text).quantize(Decimal('0.01'), ROUND_HALF_UP)", "    print(text, round(x, 2), up)"],
              "A spreadsheet's ROUND takes a half away from zero. Python rounds the binary float: 0.125 is exact and goes to the even digit, the others sit just off the half."),
         ]),
    dict(id="insert_rows", name="Blank Row Inserter and insert_rows", title="insert_rows moves values but not references", part=3, visual="insert_rows",
         concepts=["insert_rows()", "sys"],
         groups=[
             (["import sys, openpyxl", "sys.argv = ['blankRowInserter.py', '3', '2']", "ws = openpyxl.Workbook().active", "for i in range(1, 6): ws.append(['row %d' % i, i])",
               "ws['B6'] = '=SUM(B1:B5)'"],
              "The practice program reads a row number and a count from sys.argv. A list stands in for the command line here."),
             (["start, count = int(sys.argv[1]), int(sys.argv[2])", "ws.insert_rows(start, count)", "print([ws.cell(row=r, column=1).value for r in range(1, 8)])",
               "print(ws['B8'].value)"],
              "Two blank rows now sit at row 3, and the sum moved down to B8. But it still says B1:B5: insert_rows does not rewrite references inside formulas."),
         ]),
    # ------------------------------------------------------------ part 4: looks and layout
    dict(id="mult_table", name="Practice Program: a multiplication table", title="A multiplication table with bold headings", part=4, visual="mult_table",
         concepts=["Practice Programs", "Font()"],
         groups=[
             (["import openpyxl", "from openpyxl.styles import Font", "N = 4", "ws = openpyxl.Workbook().active"],
              "The practice program takes N from the command line; here N is 4. Font comes from openpyxl.styles."),
             (["for i in range(1, N + 1):", "    ws.cell(row=1, column=i + 1, value=i).font = Font(bold=True)", "    ws.cell(row=i + 1, column=1, value=i).font = Font(bold=True)"],
              "The first row and the first column hold the headings 1 to N, in bold."),
             (["    for j in range(1, N + 1):", "        ws.cell(row=i + 1, column=j + 1, value=i * j)", "for row in ws.iter_rows(values_only=True): print(row)"],
              "Every other cell holds the product of its row heading and its column heading. The last line prints the grid; the empty corner A1 is None."),
         ]),
    dict(id="fonts", name="Fonts: Font() keeps only what it is given", title="Setting the font style of cells", part=4, visual="fonts",
         concepts=["Setting the Font Style of Cells", "Font()", "openpyxl.styles"],
         groups=[
             (["import openpyxl", "from openpyxl.styles import Font", "ws = openpyxl.Workbook().active", "ws['A1'].font = Font(size=24, italic=True)",
               "ws['B3'].font = Font(name='Times New Roman', bold=True)"],
              "Font comes from openpyxl.styles and keeps only the options you give. A1 gets a size and italic; B3 gets a name and bold."),
             (["for c in (ws['A1'], ws['B3'], ws['C5']):", "    print(c.coordinate, c.font.name, c.font.sz, c.font.b)"],
              "A1 has no name and B3 has no size. Calibri 11 is the default only for cells that were never styled, such as C5."),
             (["try: ws['A1'].font.bold = True", "except AttributeError as e: print('AttributeError:', e)"],
              "A style object cannot be changed. To change one option, assign a new Font."),
         ]),
    dict(id="dimensions", name="Row height, column width and hidden columns", title="Adjusting rows and columns", part=4, visual="dimensions",
         concepts=["Adjusting Rows and Columns", "row height", "column width"],
         groups=[
             (["import openpyxl", "ws = openpyxl.Workbook().active", "ws['A5'], ws['B5'] = 'Tall row', 'Wide column'", "ws.row_dimensions[5].height = 70",
               "ws.column_dimensions['B'].width = 20", "ws.column_dimensions['D'].hidden = True"],
              "Row height is in points and column width in characters. A column can be hidden without being deleted."),
             (["print(ws.row_dimensions[5].height, ws.column_dimensions['B'].width)", "print(ws.column_dimensions['D'].hidden)",
               "print(sorted(ws.column_dimensions), sorted(ws.row_dimensions))"],
              "Reading a dimension creates it too. Here only the rows and columns that were set are listed."),
         ]),
    dict(id="merge", name="Merged cells keep one real cell", title="Merge and unmerge cells", part=4, visual="merge",
         concepts=["merged cell"],
         groups=[
             (["import openpyxl", "ws = openpyxl.Workbook().active", "ws.merge_cells('F1:I3')", "ws['F1'] = 'Twelve cells merged together.'",
               "print(*ws.merged_cells.ranges, type(ws['G2']).__name__)"],
              "merge_cells joins a block into one. Only the top-left cell is a real Cell; the other eleven are MergedCell objects."),
             (["try:", "    ws['G2'] = 'x'", "except AttributeError as e:", "    print('AttributeError:', e)", "ws.unmerge_cells('F1:I3')",
               "print(len(ws.merged_cells.ranges), type(ws['G2']).__name__)"],
              "A merged cell is read-only. After unmerge_cells the text stays in the top-left cell and the others are ordinary empty cells again."),
         ]),
    dict(id="freeze", name="Freeze panes", title="freeze_panes: the cell above and left of it stays in view", part=4, visual="freeze",
         concepts=["freeze panes"],
         groups=[
             (["import openpyxl", "for setting in ('A2', 'B1', 'C2'):", "    ws = openpyxl.Workbook().active", "    ws.freeze_panes = setting",
               "    pane = ws.sheet_view.pane", "    print(setting, pane.xSplit, pane.ySplit)"],
              "The cell you name is the first one that scrolls. A2 freezes row 1, B1 freezes column A, and C2 freezes both."),
         ]),
    # ------------------------------------------------------------ part 5: charts
    dict(id="chart_build", name="A bar chart: Reference, Series, BarChart", title="Charts: Reference, Series, BarChart and add_chart", part=5, visual="chart_build",
         concepts=["Charts", "Reference()", "Series()", "BarChart()", "add_chart()", "openpyxl.chart"],
         groups=[
             (["import openpyxl", "from openpyxl.chart import BarChart, Reference, Series", "ws = openpyxl.Workbook().active", "for i in range(1, 11): ws['A%d' % i] = i * i"],
              "Ten squares in column A are the data of the chart."),
             (["ref = Reference(ws, 1, 1, 1, 10)", "series = Series(ref, title='First series')", "chart = BarChart()", "chart.title = 'My Chart'"],
              "Reference names the cells by their corners. Series wraps them with a title. BarChart is the chart itself."),
             (["chart.append(series)", "ws.add_chart(chart, 'C2')", "print(ref, len(ws._charts))"],
              "append puts the series into the chart; add_chart places the chart on the sheet, its corner at C2."),
         ]),
    dict(id="reference_order", name="Reference takes the column first", title="Reference: columns come before rows", part=5, visual="reference_order",
         concepts=["Reference()", "Series()"],
         groups=[
             (["import openpyxl", "from openpyxl.chart import Reference", "ws = openpyxl.Workbook().active"],
              "Reference needs a worksheet and four numbers, which name the corner cells of a block."),
             (["column_b = Reference(ws, 2, 1, 2, 10)", "row_2 = Reference(ws, 1, 2, 10, 2)", "print(column_b)", "print(row_2)"],
              "The order is min_col, min_row, max_col, max_row: column first. The chapter's text says row first, but its example hides the mistake because the block is square."),
         ]),
    dict(id="chart_parts", name="A chart is stored as XML in the zip", title="What a saved chart looks like inside the file", part=5, visual="chart_parts",
         concepts=["chart", "xlsx file"],
         groups=[
             (["import io, zipfile, openpyxl", "from openpyxl.chart import BarChart, Reference", "ws = openpyxl.Workbook().active"],
              "A new sheet, and the two pieces of openpyxl that a chart needs."),
             (["for v in (1, 4, 9): ws.append([v])", "chart = BarChart(); chart.add_data(Reference(ws, 1, 1, 1, 3))", "ws.add_chart(chart, 'C2')"],
              "A small chart of three values is added to the sheet."),
             (["buf = io.BytesIO(); ws.parent.save(buf)", "names = sorted(zipfile.ZipFile(buf).namelist())", "print([n for n in names if 'chart' in n or 'drawing' in n])"],
              "The saved file has a drawing part and a chart part of its own. openpyxl writes the XML that describes the chart; the application draws it."),
         ]),
]
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
