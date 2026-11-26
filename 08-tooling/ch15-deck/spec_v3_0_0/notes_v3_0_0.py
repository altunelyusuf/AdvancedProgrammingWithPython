"""Chapter 15 deck speaker notes, version 3.0.0: notes for the reader of the distributed slides. Each note explains the slide's short wording in fuller sentences, adds detail that the slide does not carry, and connects the slide to related slides and chapters. A note gives no direction to a presenter, has no think-of statement, no prompt marker, no
lambda and no everyday picture. The facts are those of the chapter's examples, of their runs against the stand-in for Google (Google was never reached) and of the chapter research of deck 2.0.0 (findings F2 to F14). RESULT_SAYS: for each code slide, the first result balloon (what the run showed).
Slide numbers: 1 title, 2 route, 3 questions, 4 part 1, 5 A1, 6 A2, 7 setup_state, 8 token_file, 9 oauth story, 10 auth_url, 11 A3, 12 pkce, 13 token_pickle, 14 token_expiry, 15 part 2, 16 A4, 17 create_list, 18 open_three_ways,
19 attributes, 20 sheets2006 story, 21 A5, 22 upload_download, 23 delete_trash, 24 part 3, 25 A6, 26 cell_rw, 27 addresses, 28 A7, 29 rows_columns, 30 batch_writes, 31 apiv3 story, 32 A8, 33 sheet_tabs, 34 copy_clear, 35 surprises,
36 part 4, 37 A9, 38 forms_emails, 39 forms2008 story, 40 quota_backoff, 41 part 5, 42 A10, 43 audit, 44 audit_empty, 45 add_transaction, 46 lost_update, 47 nakamoto story, 48 bean_count, 49 tools, 50 current, 51 summary, 52 practice, 53 resources."""
__version__ = "3.0.0"

NOTES = {
    "title": "This chapter of the book, Google Sheets, explains how a Python program reads and writes Google spreadsheets with the library EZSheets: signing in, spreadsheet objects, sheet objects, forms and quotas, and a project. "
             "Google was never reached while this deck was made: every result comes from the real library talking to a stand-in for Google's answers, and each result slide says so. The deck has twenty-five code examples that run on the chapter page, five true stories, "
             "and tables where a comparison helps. Slide 2 lays out the five parts. Chapter 14 comes before it with Excel spreadsheets.",
    "route": "The table is the map of the chapter. Each row is one of the five parts, with the slides it covers, the number of code examples and what you will run in it. The last row covers the table of objects and requests, the changes against the book, the summary, "
             "the practice questions and the links. The same twenty-five examples are listed in the chapter-code tab of the page, in this order, so a slide and its tab can be opened side by side. Part 1 starts on slide 4, and each later part begins with a divider slide that names its four ideas.",
    "questions": "Two questions run through the chapter, and the deck answers them near the end. The first asks which object of EZSheets stands for which part of a Google account and which request each call sends; the answer is the table on slide 49. "
                 "The second asks where the book's printed outputs, programs and files differ from today; slide 50 lists those changes from the chapter research. Keeping both questions in mind makes each later slide easier to place.",
    "divider1": "Part 1 is about access. Before any request leaves the program it must be let in: a cloud project, a credentials file, a sign-in and token files. The four cards are the ideas of the part: the credentials file, the token file, the scope and the refresh token. "
                "Slides 5 to 14 cover them, using the pieces that run without an account: the address of the sign-in, the challenge, the token as a pickle and its expiry. Part 2 later uses the signed-in library.",
    "divider2": "Part 2 is about spreadsheet objects. A Spreadsheet object stands for one spreadsheet of the account, and each call that creates, opens, changes or deletes one is a request to Google. The four cards are the ideas of the part: the Spreadsheet itself, its attributes, "
                "the export with downloadAs and the Trash. Slides 16 to 23 cover them. Part 1 earlier explains the sign-in that every one of these calls depends on.",
    "divider3": "Part 3 is about sheet objects. A Sheet object stands for one tab of a spreadsheet: its cells, rows and columns. A sheet is read from a local copy and written with requests, so the number of requests is the number to watch. "
                "The four cards are the ideas of the part: A1 notation, getRow and getColumn, updateColumn and copyTo. Slides 25 to 35 cover them. Part 4 next shows why the number of requests matters.",
    "divider4": "Part 4 is about forms and quotas. A Google Form saves its answers as rows of a spreadsheet, which EZSheets reads like any other sheet. Google limits how many requests a project may send each minute, and the library waits and retries when a request is refused. "
                "The four cards are the ideas of the part. Slides 37 to 40 cover them, and part 3 earlier showed how to send fewer requests.",
    "divider5": "Part 5 is Project 11, a spreadsheet that pretends to be a blockchain. The program audits the Boringcoin ledger, adds a transaction, meets a lost update when two programs write at once, and checks the totals of the practice sheet. "
                "The four cards are the ideas of the part. Slides 42 to 48 cover them. Chapter 14 earlier showed the same kind of project on Excel files, and part 3 explains the calls that the project uses.",
    "A1": "Setting up has a fixed order: a project in the Google Cloud console, the Sheets and Drive APIs turned on in it, a consent screen that names the program and its permissions, and then a credentials file with a client id and secret. "
          "The rows give a plain meaning to each idea, from installing EZSheets with pip to the credentials file that names the program but holds no user token. Slide 6 continues with the sign-in that uses the credentials file, and slide 7 shows the library before any sign-in.",
    "A2": "A token is a saved permission with an expiry, and the refresh token asks for a new one without another sign-in. The rows explain the first login with the credentials file, ezsheets.init(), the token file, the refresh token, the scope, "
          "the revoking of the credentials file, the pickle format in which the token is saved, and the module that opens the browser page. Slide 8 shows what a token holds, slide 13 a pickle, and slide 14 the lifetime of a token.",
    "A3": "EZSheets is a thin layer. The short calls such as getRow belong to EZSheets, while Google's client library builds each request and Google's authentication library runs the sign-in. The last rows name three standard modules that the chapter's projects use: "
          "http.client for HTTP connections, shlex for splitting a command line, and sys for the words typed after the program's name. Slide 10 shows the sign-in address that the authentication library builds, and slide 45 uses sys.",
    "A4": "A Spreadsheet object stands for one spreadsheet of the account. The rows explain the objects, the call that creates or opens one, the three jobs of creating, uploading and listing, the two functions upload and listSpreadsheets, "
          "the attributes of which only the title can be changed, and refresh, which reads the spreadsheet again. Slide 17 creates and lists, slide 18 opens by id and by address, and slide 19 shows the attributes.",
    "A5": "Downloading asks Google to export a spreadsheet as a file, and delete moves a spreadsheet to the Trash first. The rows explain downloading and uploading, the Excel export, the five other formats, deleting, the delete call "
          "with its permanent option, and the Trash, where a deleted spreadsheet stays and is still listed. Slide 22 shows six downloads and slide 23 shows the two kinds of delete.",
    "A6": "A sheet is a grid in which every cell has a name such as B2, with the column letter first, and a pair of numbers that start at 1. The rows explain the Sheet object, reading and writing a cell, A1 notation, "
          "counting from 1, and the three helper functions that convert between names, numbers and letters. Slide 26 reads and writes cells, and slide 27 runs the helpers. Chapter 14 uses the same names for Excel cells.",
    "A7": "A row or a column is read as a list of text and changed with one request. The rows explain the six calls: getRow, getRows and getColumn read, and updateRow, updateRows and updateColumn replace a whole line. "
          "Every value is text. Slide 29 runs the calls on a produce sheet, and slide 30 counts the requests: one request for a column against one for each cell.",
    "A8": "A spreadsheet holds several sheets, and each can be created, moved, copied, cleared or deleted. The rows explain the creating, moving and deleting of sheets, the Sheet call that returns nothing in the current library, createSheet, which returns the new sheet, "
          "the delete of a sheet, the copying to another spreadsheet and the clear call that keeps the size. Slide 33 shows the sheets, slide 34 the copy and clear, and slide 35 three surprises of the library.",
    "A9": "A Google Form saves its answers as rows of a spreadsheet, and Google limits how many requests a project may send each minute. The rows explain Google Forms, the reading of its data with EZSheets, working with quotas, the quota itself, "
          "the setting IGNORE_QUOTA that switches off only the library's own throttle, and the practice programs of the chapter. Slide 38 collects e-mail addresses and slide 40 shows the library waiting.",
    "A10": "Project 11 builds a ledger called Boringcoin on a shared sheet. Auditing means adding up what each row moves, and a sheet of transactions is easy to audit and just as easy to forge. The rows explain the project, the fake blockchain "
           "and the checking of a sheet against a rule. Slide 43 audits the ledger, slide 45 adds a transaction, and slide 47 tells the story of the real electronic cash that the project copies as a joke.",
    "setup_state": "Before any sign-in the library already knows its release, 2026.4.28, and its two scopes: the whole spreadsheets scope and the whole drive scope. The flag IS_INITIALIZED stays False until a sign-in has worked. "
                   "The call uninstall takes the stand-in for Google out, so the result shows the library as it is before any account is used. The scope is the permission from slide 6, and slide 8 looks at the file that stores a token.",
    "token_file": "A token file holds a credentials object. The example makes one with made-up values and prints its fields: the access token, the refresh token, the address where tokens are renewed, the scopes, the universe domain and the account. "
                  "EZSheets saves such an object with pickle in a file named token-sheets.pickle, and slide 13 shows what that format allows. The access token is short-lived and the refresh token renews it, as slide 14 shows.",
    "auth_url": "No network is used. The flow builds the address that the browser would open for the sign-in, and the example reads three parts of it: the response type code, access type offline, and the challenge method S256. "
                "The credentials file is shown as a dictionary with made-up values. The return address is localhost on port 8080. Slide 12 explains the hashed challenge, and slide 9 tells how OAuth began.",
    "pkce": "The program makes a random secret, the verifier, and keeps it. Only the SHA-256 hash of the verifier, the challenge, goes into the sign-in address, and later the program shows the verifier so that Google can hash it again and compare. "
            "The example uses the verifier printed in RFC 7636, the standard behind the challenge, which is on the resources slide. Slide 10 shows where the challenge appears in the address.",
    "token_pickle": "A pickle can run code when it is loaded. The class in the example tells pickle to call print, so loading its 67 bytes prints a line; in an attack the call could be any code. "
                    "EZSheets loads token-sheets.pickle when it is imported, so a token file from someone else is a program, not data. The same danger is described on the OWASP page on the resources slide, and slide 8 shows the token that such a file holds.",
    "token_expiry": "The library compares a token's expiry with the clock, in UTC without a time zone. A fresh token is valid; a stale one and one a week old are expired, and an expired token is renewed with the refresh token. "
                    "In an app in Testing status the refresh token itself dies after seven days, which slide 50 lists among the changes. Slide 8 shows the fields of a token.",
    "create_list": "The stand-in plays Google. Spreadsheet() creates an untitled spreadsheet, createSpreadsheet gives one a title, and listSpreadsheets returns a dictionary from each id to its title. "
                   "The recorder of the stand-in counted fourteen requests so far, among them the requests that make a spreadsheet and the listing; a real quota counts the same requests. Slide 30 compares request counts for writes, and slide 49 lists the request each call sends.",
    "open_three_ways": "A spreadsheet can be opened by its id or by its address, and both give the same title. getIdFromUrl cuts the id by position, so an address that ends right after the id loses its last character: SHEET12 instead of SHEET123. "
                       "The public sheets of the book are replaced by a stand-in loaded under a made-up id. Slide 50 notes that the book's short links were answered with 403, so opening by id is safer.",
    "attributes": "A Spreadsheet has four attributes: the title, the sheet titles, the id and the address. Only the title can be set, and the new title is sent to Google at once. "
                  "The other three are properties without a setter, so setting one raises an AttributeError, which the program catches and prints. Slide 17 creates the spreadsheet that these attributes describe.",
    "upload_download": "Upload turns a file into a spreadsheet, here a small CSV file made in a temporary folder. Each downloadAs method exports the spreadsheet and saves a file with the title as its name, in which spaces become underscores. "
                       "The HTML export is saved as a zip. The book prints a plainer name, which slide 50 lists among the differences. Slide 23 shows what delete does to such a spreadsheet.",
    "delete_trash": "delete() only moves the spreadsheet to the Trash: the request is a PATCH that sets trashed to True, and the spreadsheet is still listed. delete(permanent=True) sends a DELETE request, and only then does the list lose it. "
                    "Check your own Trash before you trust a list. Slide 49 names the request of each call, and slide 17 shows the listing that this slide changes.",
    "cell_rw": "A cell is read by name or by column and row, both counting from 1. Reading from a loaded sheet sent no request, and a write is one PUT whose input is typed as if by a person. "
               "The local copy shows the number 30 after the write until refresh() reads the text that Google holds. The book prints the text 30, which slide 50 lists. Slide 27 shows the conversion of names, and slide 30 counts requests.",
    "addresses": "These are plain functions that need no account. convertAddress turns a name into a column and row pair and back, so A2 is (1, 2) and the pair (2, 5) is B5. getColumnLetterOf and getColumnNumberOf convert between letters and numbers: "
                 "27 is AA, 999 is ALK and ZZZ is column 18278. Letters count like digits without a zero. Slide 26 uses the names, and chapter 14 has the same converters for Excel.",
    "rows_columns": "Rows and columns are lists of text, and every value is a string. getRow and getColumn read a line, and getColumn accepts a letter or a number. updateRow and updateColumn replace a whole line with one request. "
                    "The example upper-cases the first column and replaces row 3. Slide 30 counts the requests of these updates, and slide 33 moves on to the sheets themselves.",
    "batch_writes": "Writing eight values cell by cell sent eight requests, and updateColumn sent all eight in one. Google limits requests, not values, so batching is the cure for a slow program and for a refused one. "
                    "The limit is described on the usage-limits page of the resources slide, and slide 40 shows what the library does when a request is refused.",
    "sheet_tabs": "Spreadsheet.Sheet() returns None in the current library, although the sheet Spam does appear in the sheet titles afterwards. createSheet returns the Sheet, and a second argument chooses its place. "
                  "Setting index moves a sheet and delete() removes one; sheets are counted from 0. The book's listings print Sheet objects, which slide 50 lists as a difference. Slide 34 copies a sheet.",
    "copy_clear": "copyTo adds a sheet named Copy of, then the old name, to another spreadsheet, and refresh() reads it. clear() empties every cell but keeps the size: the sheet still has two rows and three columns. "
                  "A new spreadsheet starts with one sheet, so the copy is its second. Slide 33 shows creating and deleting sheets, and slide 35 shows three surprises of the library.",
    "surprises": "Three surprises of the library. Two sheets are equal when their sheet ids are equal, and the first sheet of every new spreadsheet has the id 0, so sheets of unrelated spreadsheets compare equal. "
                 "The in operator searches the coordinates, not the values, so a name in a cell is not found. An empty cell is an empty string, never None. Slide 29 shows the lists of text that rows and columns return.",
    "forms_emails": "A form saves each answer as a row of a spreadsheet; the three answers here stand in for the response sheet of a real form. Column 3 holds the addresses, the first item is the heading and is cut off, "
                    "and a set removes the address that answered twice. Slide 39 tells how Google Forms began, and slide 29 shows getColumn, which this program uses.",
    "quota_backoff": "Google answers 429 when a project sends too many requests, and the library waits and retries. In the example the pauses are recorded instead of slept: nine tries, 220 seconds in all, then an HttpError is raised. "
                     "IGNORE_QUOTA does not change this retry. The page on usage limits, on the resources slide, gives Google's own figures, and slide 30 shows how to send fewer requests.",
    "audit": "Step 1 of Project 11. PRE-MINE invents money and every other row moves it: the sender loses the amount and the recipient gains it. If the ledger is honest, the balances add up to what was created, here 1,500 Boringcoins. "
             "The real sheet has far more rows; this one has four. Slide 44 shows what happens on the real grid, and slide 47 tells the story that the project copies.",
    "audit_empty": "The real sheet is a grid of 1,000 rows, so getRows also returns the empty rows. One added row shows it: the audit sees three rows, and int of an empty string raises a ValueError, so the loop of step 1 stops. "
                   "A guard for an empty first cell avoids it. Slide 43 shows the audit that this guard completes, and slide 29 shows getRows.",
    "add_transaction": "Step 2 of Project 11. The program reads sender, recipient and amount from the command line, here set by hand. Adding a row changes the size of the sheet, which costs three requests, and each of the three cells costs one more: six requests for one transaction. "
                       "A name with a space needs quotes on the command line, or sys.argv has four items. Slide 46 shows what two such programs do together.",
    "lost_update": "Two programs each count the next row from their own copy of the sheet, so both write to row 3, and the second silently replaces the first. No error is raised, and after a refresh row 3 holds the second program's text. "
                   "A guard or a lock is needed, and the sheet itself offers none. Slide 45 shows the single program that this slide runs twice, and slide 48 checks totals.",
    "bean_count": "The practice program checks each total against quantity times price. The heading is row 1, so the data starts at row 2, and the row numbers that the program prints count the heading. "
                  "One total is wrong in this stand-in: row 3 says 130, and 3 times 40 is 120. The same idea, a check against a rule, ends the audit on slide 43. Slide 52 asks for a version that prints the correct total.",
    "compare_tools": "The table sums up which EZSheets object stands for which part of the account and which request it sends. A Spreadsheet is one spreadsheet, a Sheet one tab, getRow and getColumn read a loaded sheet without a request, "
                     "updateColumn writes a column with one request, a change of size costs three requests, delete moves to the Trash, downloadAsExcel exports a file, and the token file is a local pickle. The last column names the slide that shows each row in code. It answers the first question of slide 3.",
    "current": "The book's scripts and outputs differ from today's in places. The table lists each change, what it is now, and the slide with its example. Sheet() returns None, a write shows the number until a refresh, downloads get a longer name, "
               "the quota figures differ, a Testing app signs in again every seven days, token files are pickles, the consent screen has new pages, and Step 2 sends six requests. It answers the second question of slide 3.",
    "summary": "Five ideas are worth keeping. A program must be let in with a cloud project, a credentials file and token files. A token file is a pickle, so never load one you did not make. "
               "A Spreadsheet object stands for one spreadsheet and a Sheet object for one tab, and each call is a request. Batch your writes, because Google limits requests, not values. "
               "A ledger of rows is easy to audit and just as easy to forge. The chart counts the code examples in each part of this deck. Slide 3 holds the two questions that these ideas answer, and slide 50 lists what differs from the book.",
    "practice": "Four drills and a program. The first uses the addresses of slide 27 for column 703 and the name ZZ. The second counts requests, as slide 30 does. The third is the lost update of slide 46. "
                "The program extends the Bean Count check of slide 48 to print the correct total. Try each on the chapter page, and write the answer in one sentence before you run it.",
    "resources": "Start with the book chapter and the EZSheets documentation, then Google's pages on limits, values and scopes, and the standards behind the sign-in: OAuth, and RFC 7636 for the challenge. "
                 "The Python and OWASP pages explain the danger of pickle, gspread is the other library for Google Sheets, and the last link is the paper that Project 11 copies as a joke. Choose one link and read it before the next class. Slide 49 and slide 50 name the objects and the changes that most of these pages describe in full.",
}

STORY_NOTES = {
    "oauth": "OAuth began in November 2006 at a CitizenSpace OpenID meeting, where Blaine Cook, Chris Messina and others found that no open standard existed for sharing access without sharing a password. A specification was drafted in July 2007 and the IETF published RFC 6749 in October 2012. "
             "The photograph shows Blaine Cook. Your token files, slides 8 and 13, are the result, and slide 10 shows the address of a sign-in that uses it.",
    "sheets2006": "Google Sheets began as XL2Web, made by 2Web Technologies; Google bought it in 2006 and opened a limited test on 6 June 2006. The photograph shows Jonathan Rochelle. A spreadsheet in a browser is a service that a program calls, not a file, "
                  "which is why every call on slides 17 to 23 is a request. Chapter 14 tells how the file-based spreadsheet began.",
    "apiv3": "Google turned down Sheets API version 3 on 2 August 2021, and EZSheets speaks version 4. The picture is a screenshot of the Google Sheets add-ons page, not of the API itself. A library is only as stable as the service behind it, "
             "which is why slide 50 lists what changed since the book was written. Slide 30 shows the requests that version 4 receives.",
    "forms2008": "Google Forms was introduced in 2008; the pages we could open give the year, not the day. The picture is a web page with the Forms icon and a link to a form. A form is a front door that writes rows for your script, "
                 "and slide 38 reads those rows. Slide 37 gives the plain meaning of Google Forms.",
    "nakamoto": "On 31 October 2008 Satoshi Nakamoto announced the paper bitcoin.pdf to a cryptography mailing list. No photograph of the author exists, so the picture is the first page of the paper. "
                "A ledger of rows is easy to audit and easy to forge, which is what slides 43 to 46 show on a sheet. The paper is on the resources slide.",
}

RESULT_SAYS = {
    "setup_state": "The release is 2026.4.28 and no sign-in has happened.",
    "token_file": "A token holds an access token, a refresh token and scopes.",
    "auth_url": "The address asks for a code, offline access and an S256 challenge.",
    "pkce": "The challenge is the hash of the verifier.",
    "token_pickle": "Loading the pickle ran a print call.",
    "token_expiry": "A fresh token is valid; the other two are expired.",
    "create_list": "Two spreadsheets are listed after fourteen requests.",
    "open_three_ways": "An id and an address open the same spreadsheet.",
    "attributes": "The title was set; id, url and sheetTitles refused.",
    "upload_download": "Six downloads got a safe file name.",
    "delete_trash": "After delete() the spreadsheet is still listed.",
    "cell_rw": "Reading four cells sent no request; one write sent one.",
    "addresses": "27 is AA, 999 is ALK and ZZZ is 18278.",
    "rows_columns": "A row and a column are lists of text.",
    "batch_writes": "Eight requests cell by cell, one for the column.",
    "sheet_tabs": "Sheet() printed None; createSheet added sheets.",
    "copy_clear": "The copy holds the data; clear() kept the size.",
    "surprises": "Two unrelated sheets compare equal.",
    "forms_emails": "Three answers give two different addresses.",
    "quota_backoff": "Nine tries and 220 seconds, then an HttpError.",
    "audit": "The balances add up to 1,500 Boringcoins.",
    "audit_empty": "The audit stopped at an empty row with a ValueError.",
    "add_transaction": "One transaction cost six requests.",
    "lost_update": "Both programs wrote to row 3.",
    "bean_count": "Row 3 says 130 and the product is 120.",
}
