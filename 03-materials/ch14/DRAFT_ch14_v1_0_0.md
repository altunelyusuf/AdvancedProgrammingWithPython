# Chapter 14 draft — Excel Spreadsheets (3rd edition)

## Status

State check (ex:TK5_StateCheck_Ch14, Lineage5) found no gap against the current standard: all six story slides match their sourced companion-script text exactly, the resources slide's 15 links are live and correct, and all 24 code examples — no network dependency in this chapter — were re-run and matched the recorded output exactly. This is a direct write-up of already-correct content, not a correction pass — same situation as chapters 11-12. One open item outside the chapter's own content: a legacy YA-suffixed deck duplicating this subject, already decided this turn (see Open items).

## 1. The story

Six real, dated, sourced beats, told in the order the deck teaches them:

1. **1979 (idea, spring 1978) — Dan Bricklin and Bob Frankston, VisiCalc.** Bricklin had the idea for an electronic spreadsheet in spring 1978 as a Harvard MBA student, deciding that summer to make it a product; he prototyped the screen in Basic on the school's timesharing system — the moment numbers, formula results and text became rows and columns with human-friendly names. His work journal dates the first prototype, on a borrowed Apple II, to 8 October 1978. With Frankston he built VisiCalc, published by Personal Software, first out on the Apple II in 1979. (bricklin.com/history/saiidea.htm)
2. **1985 — Microsoft, with Steve Jobs and Bill Gates, Excel for Macintosh.** Microsoft's Multiplan (1982) gave way to a new spreadsheet, codenamed Odyssey (1983), as Lotus 1-2-3 dominated. On 2 May 1985, Jobs and Gates announced Excel for the Macintosh at Tavern on the Green, NYC; it went on sale 30 September 1985, with the first Windows version (2.05) following 19 November 1987. Excel still treats 29 February 1900 as a real day — a bug inherited on purpose from Lotus 1-2-3 for compatibility, carried into the Office Open XML format openpyxl reads today. (Wikipedia: Microsoft Excel)
3. **2006 — Microsoft and Ecma International's TC45, the .xlsx standard.** Microsoft submitted Office Open XML documentation to Ecma International, which formed TC45 in December 2005 to review it; approved as ECMA 376 in December 2006, submitted through ISO/IEC JTC 1 in early 2007, approved as ISO/IEC 29500 in early 2008. An .xlsx file is SpreadsheetML inside a ZIP-based package — exactly what `load_workbook` opens. (loc.gov, digital format description)
4. **2010 — Eric Gazoni and Charlie Clark, openpyxl.** openpyxl's own documentation: born from the lack of a native Python library to read/write Office Open XML, initially based on PHPExcel; first PyPI upload (1.1.0) dated 11 August 2010. Described as maintained by volunteers in their spare time. As of 12 October 2026 the newest stable release was 3.1.5 (uploaded June 2024) — the library every program in this chapter runs on. (openpyxl.readthedocs.io)
5. **2013 — Thomas Herndon, Michael Ash, Robert Pollin, the Reinhart–Rogoff spreadsheet error.** In April 2013 they replicated Reinhart and Rogoff's debt-and-growth study; using the authors' own working spreadsheet, found a coding error that entirely excluded five countries — Australia, Austria, Belgium, Canada, Denmark — from the analysis. With that exclusion and an unusual weighting corrected, average real growth above 90% debt-to-GDP was 2.2%/year, not the published −0.1%; the spreadsheet error contributed a −0.3 percentage-point error in the published high-debt average. (peri.umass.edu)
6. **2016 — Mark Ziemann, Yotam Eren, Assam El-Osta, gene names turned into dates.** Excel's default settings turn gene symbols like SEPT2 and MARCH1 into dates (2-Sep, 1-Mar) — first described in 2004. In 2016 the team screened 35,175 supplementary Excel files from 18 journals (2005–2015), found gene lists in 3,597 papers, and confirmed gene-name errors in 987 files from 704 articles — 19.6% of articles with such lists in the selected journals. In openpyxl a symbol written as a string keeps data type `s`; no date is made of it. (genomebiology.biomedcentral.com)

## 2. Explanations

- An .xlsx file is a ZIP of XML parts; `load_workbook`/`Workbook` open and create them; sheets are created, listed (`sheetnames`) and selected via the active sheet or by name.
- A cell is addressed by name (`"B2"`) or by row/column number; `get_column_letter`/`column_index_from_string` convert between the two; slices give a tuple of rows/columns of cells (generators under the hood).
- Every cell has a data type — number, text or date — and *looking at* a cell can create it; read-only mode (`iter_rows`) reads values row by row without materializing the whole sheet.
- Capstone projects: reading the census sheet row by row and tallying tracts/population with `setdefault` (Project 9), saving the tally as a Python file via `pprint.pformat`, correcting prices in a produce sheet (Project 10).
- Writing: creating/removing sheets, saving; a formula is text — openpyxl never calculates it, so a saved workbook has no formula result until opened in an application.
- `ROUND` (spreadsheet) and `round` (Python) differ on exact halves — real-data consequence: 629 of 23,757 rows of the produce file.
- `insert_rows` moves values but not formula references — a correctness trap, not a convenience.
- Fonts (`Font()` keeps only the attributes it's given), row height/column width, hidden columns, merge/unmerge, `freeze_panes`.
- Charts: `Reference` takes the column before the row (opposite of the chapter's prose order), `Series`, `BarChart`, `add_chart`; a chart is stored as XML inside the zip.

## 3. Slide/page-tab outline (slide order; 24/24 code examples re-run and matched exactly)

| Slide | Content | Code example |
|---|---|---|
| 1–3 | Title, today's route, two questions this chapter answers | — |
| 4–5 | Part 1: Reading a workbook — everyday pictures | — |
| 6 | An .xlsx file is a zip of XML parts | An .xlsx file is a zip of XML parts |
| 7 | **Story: .xlsx became a standard, 2006** | — |
| 8 | Sheets: create_sheet, sheetnames, active sheet | Sheets of a workbook: names, order, active |
| 9 | **Story: openpyxl was born, 2010** | — |
| 10 | Everyday pictures: sheets and cells | — |
| 11 | A cell by name, by row/column, its coordinate | Cells by name and by number |
| 12 | **Story: a student pictured the spreadsheet, 1978** | — |
| 13 | get_column_letter and column_index_from_string | Column letters and numbers |
| 14 | A slice of cells, one column, and generators | Slices, rows and columns of cells |
| 15 | Everyday pictures: reading many cells | — |
| 16 | Every cell has a data type | Data types of cells: numbers, text, dates |
| 17 | **Story: Excel turned gene names into dates, 2016** | — |
| 18 | Looking at a cell changes the workbook | Looking at a cell creates it |
| 19 | Read-only mode: iter_rows | Read-only mode and iter_rows |
| 20–21 | Part 2: Two projects on real data — everyday pictures | — |
| 22 | Project 9: read the census sheet row by row | Project 9: read the rows of the census sheet |
| 23 | Project 9: tally tracts/population, setdefault | Project 9: tally tracts and population by county |
| 24 | pprint.pformat: save the tally as a Python file | pprint.pformat writes the result as Python |
| 25 | Project 10: correct prices in a produce sheet | Project 10: correct the prices |
| 26–27 | Part 3: Writing and formulas — everyday pictures | — |
| 28 | Writing a workbook: sheets, remove, save | Writing a workbook: sheets and save |
| 29 | A formula is text; openpyxl never calculates it | A formula is text; the result is cached |
| 30 | **Story: Excel on the Macintosh, 2 May 1985** | — |
| 31 | Exact halves: spreadsheet ROUND vs Python round | ROUND in a spreadsheet and round in Python |
| 32 | **Story: a spreadsheet error excluded five countries, 2013** | — |
| 33 | insert_rows moves values but not references | Blank Row Inserter and insert_rows |
| 34–36 | Part 4: Looks and layout — everyday pictures | — |
| 37 | Practice program: a multiplication table | Practice Program: a multiplication table |
| 38 | Setting the font style of cells | Fonts: Font() keeps only what it is given |
| 39 | Adjusting rows and columns | Row height, column width and hidden columns |
| 40 | Merge and unmerge cells | Merged cells keep one real cell |
| 41 | freeze_panes | Freeze panes |
| 42–43 | Part 5: Charts — everyday pictures | — |
| 44 | Charts: Reference, Series, BarChart, add_chart | A bar chart: Reference, Series, BarChart |
| 45 | Reference: columns before rows | Reference takes the column first |
| 46 | What a saved chart looks like inside the file | A chart is stored as XML in the zip |
| 47 | What openpyxl keeps, and what it does not do | — |
| 48 | What differs from the book today (research table: get_sheet_by_name warns/get_highest_row gone in 3.1.5; Reference takes column first; saved workbook has no formula result; ROUND vs round on exact halves, 629/23,757 produce rows; Font() keeps only given attributes; looking at a cell creates it) | — |
| 49–50 | Summary, practice questions | — |
| 51 | Resources | — |

## 4. Resources slide (15 links, all live)

Book: Automate the Boring Stuff 3e, ch14 (automatetheboringstuff.com/3e/chapter14.html) · openpyxl docs: start page, tutorial, styles, charts, optimised/read-only modes · Python docs: pprint, decimal, zipfile · Library of Congress: OOXML format family · Dan Bricklin: The Idea (VisiCalc history) · Gene name errors are widespread (Genome Biology) · openpyxl and defusedxml on PyPI.

## 5. Open items

1. **Legacy duplicate (decided this turn):** `03-materials/slides/Chapter12WorkingWithExcelSpreadheets_YA_v1_0_0.pptx` (old-edition numbering) duplicated this chapter's subject. Owner approved retiring it; file removed, recoverable from git history.
2. **No structural retrofit gap** — TK_Ret_Ch14_* was already Done in the closed slides lineage; not reopened here.
