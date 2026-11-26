"""Chapter 15 deck content, version 3.0.0: the words of the deck for the generic builder (parts, plan, route, questions, plain meanings, stories, take-aways, tables, summary, practice, resources).
The chapter's content is that of deck 2.0.0 (deck_content_v2_0_0.py and the plan and parts of the chapter's own builder deck_build_v2_0_0.py); what the rulings force is changed: the everyday pictures
become plain meanings (no analogy anywhere; the box label is IN SHORT), the five stories are the same stories with the same facts and links, told as prose in paragraphs of at most 30 words, the
table of tools is a comparison slide, and the notes are notes_v3_0_0.py. Google was never reached: the notes say so where a result is shown."""
__version__ = "3.0.0"

BOX_LABEL = "IN SHORT"
TABLE_HEAD = "In short"
CONCEPTS_TAIL = "each with a plain meaning"

PARTS = {
    1: ("Part 1: Access, sign-in and token files", "Sign in first; the pieces that need no account run here", [
        ("Credentials file", "Names your program to Google."),
        ("Token file", "Saves the sign-in, as a pickle."),
        ("Scope", "A permission the program asks for."),
        ("Refresh token", "Renews a token without a new sign-in."),
    ]),
    2: ("Part 2: Spreadsheet objects", "Each call here is one request to Google", [
        ("Spreadsheet", "One spreadsheet, found by its id."),
        ("Attributes", "Only the title can be rewritten."),
        ("downloadAs", "Asks Google to export the spreadsheet as a file."),
        ("Trash", "Where delete() sends a spreadsheet first."),
    ]),
    3: ("Part 3: Sheet objects", "Read from a local copy, write with requests", [
        ("A1 notation", "The letter first, then the row number."),
        ("getRow, getColumn", "Read a whole line as a list of text."),
        ("updateColumn", "Writes a whole column with one request."),
        ("copyTo", "Copies a sheet into another spreadsheet."),
    ]),
    4: ("Part 4: Forms and quotas", "Forms save answers as rows; Google limits requests", [
        ("Google Forms", "Its answers arrive as rows of a sheet."),
        ("Quota", "How many requests Google allows each minute."),
        ("IGNORE_QUOTA", "Switches off the library's own throttle only."),
        ("Backoff", "Wait longer after each refusal, then try again."),
    ]),
    5: ("Part 5: Project 11, a fake blockchain", "A sheet that pretends to be a ledger: audit it, extend it", [
        ("Project 11", "A shared sheet of who paid whom."),
        ("Audit", "Add up what each account holds."),
        ("Lost update", "Two writers use the same row number."),
        ("Bean Count", "Check each total against a rule."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("analogy", "A2"), ("code", "setup_state"), ("code", "token_file"), ("story", "oauth"), ("code", "auth_url"), ("analogy", "A3"),
        ("code", "pkce"), ("code", "token_pickle"), ("code", "token_expiry"),
        ("divider", 2), ("analogy", "A4"), ("code", "create_list"), ("code", "open_three_ways"), ("code", "attributes"), ("story", "sheets2006"), ("analogy", "A5"),
        ("code", "upload_download"), ("code", "delete_trash"),
        ("divider", 3), ("analogy", "A6"), ("code", "cell_rw"), ("code", "addresses"), ("analogy", "A7"), ("code", "rows_columns"), ("code", "batch_writes"), ("story", "apiv3"),
        ("analogy", "A8"), ("code", "sheet_tabs"), ("code", "copy_clear"), ("code", "surprises"),
        ("divider", 4), ("analogy", "A9"), ("code", "forms_emails"), ("story", "forms2008"), ("code", "quota_backoff"),
        ("divider", 5), ("analogy", "A10"), ("code", "audit"), ("code", "audit_empty"), ("code", "add_transaction"), ("code", "lost_update"), ("story", "nakamoto"), ("code", "bean_count"),
        ("compare", "tools"),
        ("current",), ("summary",), ("practice",), ("resources",)]

ROUTE_RUNS = {1: "the version, token file, sign-in address, challenge, pickle, expiry", 2: "create, open, attributes, upload and download, delete",
              3: "cells, addresses, rows and columns, batching, sheets, copy, surprises", 4: "form answers and the quota", 5: "audit, empty row, add, lost update, totals"}

ROUTE_TAIL = ("Tools, changes, summary, practice, resources", "what each call sends, and what differs today")

QUESTIONS = [("1", "Which object of EZSheets stands for which part of a Google account, and which request does each call send?",
              "Answer on slide %d: the objects and their requests.", [("compare", "tools")]),
             ("2", "Which printed outputs, programs and files of the book differ today?",
              "Answer on slide %d: the changes, from the chapter research.", [("current",)])]

QUESTIONS_TAKEAWAY = "Each call is one or more requests; the stand-in answers them here."

ANALOGIES = [
    ("A1", "In short: setting up the account", "Setting up means a cloud project, two enabled APIs, a consent screen and a credentials file, in this order.", [
        ("Installing and Setting Up EZSheets", "Installs the ezsheets package with pip; the Google client libraries come with it."),
        ("Creating a New Google Cloud Project", "Makes a project in the Google Cloud console that owns the credentials and the enabled APIs."),
        ("Google Cloud project", "The container in Google Cloud to which the credentials and the enabled APIs belong."),
        ("Enabling the Sheets and Drive APIs", "Turns on the two services in the project; EZSheets calls both."),
        ("Configuring the OAuth Consent Screen", "Names the program and the permissions it asks for, as the user will see them."),
        ("OAuth consent screen", "The page Google shows when a user is asked to allow the program."),
        ("Creating Credentials", "Makes the client id and secret of a desktop app, to download as a JSON file."),
        ("credentials file", "The JSON file with the client id and secret; it names the program but holds no user token."),
    ]),
    ("A2", "In short: signing in and tokens", "A token is a saved permission with an expiry; the refresh token asks for a new one without another sign-in.", [
        ("Logging In with the Credentials File", "The first call opens a browser page where the user clicks Allow; the result is saved as token files."),
        ("ezsheets.init()", "Signs in with the credentials file and saves the token files that later runs reuse."),
        ("token file", "A file that stores the access token, the refresh token and the scopes; EZSheets saves it as a pickle."),
        ("refresh token", "A long-lived token that asks Google for a new access token without a new sign-in."),
        ("scope", "One permission the program asks for, written as an address; EZSheets asks for spreadsheets and drive."),
        ("Revoking the Credentials File", "Cancels the credentials in the console; token files made from them stop working."),
        ("pickle", "A standard module that saves a Python object as bytes; loading the bytes can run code."),
        ("webbrowser", "A standard module that opens a page in the user's browser; the sign-in uses it."),
    ]),
    ("A3", "In short: the libraries underneath", "EZSheets is a thin layer; Google's client libraries build and send every request.", [
        ("ezsheets", "The library of this chapter; it offers short calls such as getRow."),
        ("googleapiclient", "Google's client library; it builds each request to the Sheets and Drive APIs."),
        ("google_auth_oauthlib", "Google's library for the sign-in flow that makes the token."),
        ("http.client", "A standard module for HTTP connections."),
        ("shlex", "A standard module that splits a command line and keeps a quoted name in one piece."),
        ("sys", "A standard module; sys.argv holds the words typed after the program's name."),
    ]),
    ("A4", "In short: spreadsheet objects", "A Spreadsheet object stands for one spreadsheet of the account; creating, opening and changing it are requests to Google.", [
        ("Spreadsheet Objects", "The objects that stand for the spreadsheets of the account."),
        ("Spreadsheet object", "Holds the title, the sheets, the id and the address of one spreadsheet."),
        ("ezsheets.Spreadsheet()", "Creates a new spreadsheet, or opens one by id or address."),
        ("Creating, Uploading, and Listing Spreadsheets", "Makes a new spreadsheet, turns a file into one, and lists the spreadsheets of the account."),
        ("ezsheets.upload()", "Uploads a file and returns the spreadsheet that Google makes from it."),
        ("ezsheets.listSpreadsheets()", "Returns a dictionary from the id of each spreadsheet to its title."),
        ("Accessing Spreadsheet Attributes", "Reads the title, the sheet titles, the id and the address; only the title can be changed."),
        ("Spreadsheet.refresh()", "Reads the spreadsheet from Google again, to see what changed."),
    ]),
    ("A5", "In short: downloading and deleting", "Downloading asks Google to export a file; delete() moves a spreadsheet to the Trash first.", [
        ("Downloading and Uploading Spreadsheets", "Saves a spreadsheet as a file, or makes a spreadsheet from a file."),
        ("Spreadsheet.downloadAsExcel()", "Saves the spreadsheet as an .xlsx file."),
        ("Converting Spreadsheets to Other Formats", "The same download as CSV, TSV, PDF, ODS or HTML."),
        ("Deleting Spreadsheets", "Removes a spreadsheet from the account, to the Trash or for good."),
        ("Spreadsheet.delete()", "Moves the spreadsheet to the Trash; delete(permanent=True) removes it for good."),
        ("Trash", "Google's holding place for deleted files; the library still lists a spreadsheet that is there."),
    ]),
    ("A6", "In short: sheets, cells and addresses", "A sheet is a grid; a cell has a name such as B2, and rows and columns count from 1.", [
        ("Sheet Objects", "The objects that stand for the tabs of a spreadsheet."),
        ("Sheet object", "One tab, with its rows, columns and cells."),
        ("Reading and Writing Data", "Reads a cell from the local copy and writes it with one request."),
        ("A1 notation", "A cell name with the column letter first, then the row number, as in B2."),
        ("1-based index", "Counting that starts at 1, where a Python list starts at 0."),
        ("ezsheets.convertAddress()", "Turns a name such as B2 into a column and a row, and back."),
        ("ezsheets.getColumnLetterOf()", "Turns a column number into its letters; 27 is AA."),
        ("ezsheets.getColumnNumberOf()", "Turns column letters into the number; ZZZ is 18278."),
    ]),
    ("A7", "In short: rows and columns", "A row or a column is read as a list of text and changed with one request.", [
        ("Sheet.getRow()", "Returns one row as a list of text."),
        ("Sheet.getRows()", "Returns all rows as a list of lists."),
        ("Sheet.getColumn()", "Returns one column as a list of text."),
        ("Sheet.updateRow()", "Replaces one row with one request."),
        ("Sheet.updateRows()", "Replaces several rows with one request."),
        ("Sheet.updateColumn()", "Replaces one column with one request."),
    ]),
    ("A8", "In short: more sheets in a spreadsheet", "A spreadsheet holds several sheets; each can be created, moved, copied, cleared or deleted.", [
        ("Creating, Moving, and Deleting Sheets", "Adds a sheet, changes its place with index, or removes it."),
        ("Spreadsheet.Sheet()", "Looks like a way to add a sheet, but returns nothing in the current library."),
        ("Spreadsheet.createSheet()", "Adds a sheet and returns it; a second argument chooses its place."),
        ("Sheet.delete()", "Removes one sheet; the last sheet of a spreadsheet cannot be removed."),
        ("Copying Sheets", "Puts a copy of a sheet into another spreadsheet."),
        ("Sheet.copyTo()", "Makes the copy; its name is Copy of, then the old name."),
        ("Sheet.clear()", "Empties every cell; the sheet keeps its size."),
    ]),
    ("A9", "In short: forms and quotas", "A form saves its answers as rows; Google limits how many requests a project may send each minute.", [
        ("Google Forms", "Makes a survey whose answers are saved as rows of a spreadsheet."),
        ("Downloading Google Forms Data", "Reads those rows with EZSheets, like any other sheet."),
        ("Working with Google Sheets Quotas", "Keeps the program within the number of requests that Google allows."),
        ("quota", "The number of requests that Google allows in a period of time."),
        ("IGNORE_QUOTA", "A setting that switches off the library's own throttle; it does not change Google's limit."),
        ("Practice Programs", "Short programs that apply the chapter: here collecting e-mail addresses and the Bean Count check."),
    ]),
    ("A10", "In short: the project", "Project 11 is a ledger on a sheet; auditing means adding up what each row moves.", [
        ("Project 11: Fake Blockchain Cryptocurrency Scam", "Builds a ledger called Boringcoin on a shared sheet, audits it and adds a transaction."),
        ("fake blockchain", "A sheet of transactions that is easy to audit and just as easy to forge."),
        ("Finding Mistakes in a Spreadsheet", "Checks each row against a rule, such as quantity times price."),
    ]),
]

STORIES = {
    "oauth": dict(title="Story: OAuth began in 2006 to end password sharing", img="image_cook_oauth.jpg",
                  prose=["Blaine Cook, Chris Messina, David Recordon and Larry Halff began OAuth in November 2006, at a CitizenSpace OpenID meeting and later in an online Google group.",
                         "Twitter and OpenID needed a way to share access without sharing passwords, and no open standard existed.",
                         "They wrote a proposal, drafted a specification in July 2007, and the IETF published it as RFC 6749 in October 2012.",
                         "OAuth lets a program act for you without learning your password; your token files are its result."],
                  link="https://oauth.net/about/introduction/", linktext="Introduction to OAuth (oauth.net)"),
    "sheets2006": dict(title="Story: Google Sheets began as a small web spreadsheet", img="image_rochelle_google.jpg",
                       prose=["Jonathan Rochelle and Farzad Khosrowshahi of 2Web Technologies, then Google, are named with XL2Web, a spreadsheet in a web browser.",
                              "Google bought it in 2006, and a limited test began on 6 June 2006, first come first served, at Google Labs.",
                              "A spreadsheet in a browser can be shared with no file to send around; Rochelle's post is titled It's nice to share.",
                              "A beta for all Google Account holders replaced the test; the product became Google Sheets."],
                       link="https://en.wikipedia.org/wiki/Google_Sheets", linktext="Google Sheets (Wikipedia)"),
    "apiv3": dict(title="Story: Google turned off the old Sheets API in 2021", img="image_sheets_screen.jpg",
                  prose=["On 2 August 2021 the Google Sheets API team turned down version 3 of the API, and every developer with an app on it had to move.",
                         "Version 4 is JSON-based, has a simpler interface and much functionality that version 3 lacked; it lives at sheets.googleapis.com.",
                         "EZSheets and every current client speak version 4; Google published a migration guide and a turn-down date.",
                         "A program must follow the service when its address and version change. The picture is a screenshot of the Sheets add-ons page, not of the API."],
                  link="https://developers.google.com/workspace/sheets/api/guides/migration", linktext="Migrate from the Sheets API v3 (Google for Developers)"),
    "forms2008": dict(title="Story: Google Forms arrived in 2008", img="image_forms_screen.jpg",
                      prose=["Google introduced Google Forms in 2008 as part of the Google Docs suite; the pages that could be opened give the year only, not the day.",
                             "It is a web application for making surveys, and the answers can fill a spreadsheet automatically.",
                             "The owner picks a new or an existing spreadsheet as the place for the responses; EZSheets then opens it like any other.",
                             "So the answers arrive as rows that a program can read, which is the first practice program of the chapter."],
                      link="https://en.wikipedia.org/wiki/Google_Forms", linktext="Google Forms (Wikipedia)"),
    "nakamoto": dict(title="Story: a 2008 message announced the cash Boringcoin copies", img="image_bitcoin_paper.png",
                     prose=["On Friday 31 October 2008, at 14:10 Eastern time, Satoshi Nakamoto, the name of an unknown author, wrote to a cryptography mailing list hosted at metzdowd.com.",
                            "The message announced a peer-to-peer electronic cash system and the paper bitcoin.pdf, with no trusted third party.",
                            "It lists the properties: a peer-to-peer network prevents double spending, there is no mint, and new coins come from proof of work.",
                            "The chapter's Boringcoin ledger is a joke copy of the idea. The picture is the first page of the paper."],
                     link="https://www.metzdowd.com/pipermail/cryptography/2008-October/014810.html", linktext="The message of 31 October 2008 (metzdowd.com)"),
}

TAKEAWAY = {
    "setup_state": "Before the sign-in, no request can leave.", "token_file": "A token file holds two secrets and the scopes.", "auth_url": "The sign-in address asks for a code, offline.",
    "pkce": "The challenge is a hash of a secret kept at home.", "token_pickle": "A token file from someone else is a program.", "token_expiry": "A token has a lifetime; the refresh token renews it.",
    "create_list": "Every call is a request to Google.", "open_three_ways": "An id or an address opens the same spreadsheet.", "attributes": "Only the title can be set.",
    "upload_download": "A download name is made safe, not kept.", "delete_trash": "delete() moves to the Trash.", "cell_rw": "A write is one request; a read is none.",
    "addresses": "Letters count like digits without a zero.", "rows_columns": "A row or a column is a list of text.", "batch_writes": "Batch: one request for many values.",
    "sheet_tabs": "createSheet returns the Sheet; Sheet() does not.", "copy_clear": "copyTo copies; clear() keeps the size.", "surprises": "Equal ids make equal sheets.",
    "forms_emails": "A form's answers are rows.", "quota_backoff": "The library waits 220 seconds, then gives up.", "audit": "An honest ledger adds up.",
    "audit_empty": "getRows also returns the empty rows.", "add_transaction": "One transaction costs six requests.", "lost_update": "Two writers can lose a row.",
    "bean_count": "Check a total with a rule.",
}

COMPARES = {
    "tools": dict(title="Which EZSheets object sends which request", sub="From the chapter research; each row has its slide",
                  rows=[["EZSheets object", "Stands for", "Request it sends", "Slide"],
                        ["Spreadsheet()", "one spreadsheet of the account", "POST to create; GET to open", "17"],
                        ["Sheet, sheet['B2']", "one tab, and one cell of it", "GET values; PUT one cell", "26"],
                        ["getRow, getColumn", "a line of text values", "none after the first load", "29"],
                        ["updateColumn", "a whole column", "one PUT for all values", "30"],
                        ["rowCount += 1", "the size of the grid", "GET, GET, POST: three", "45"],
                        ["delete()", "the Trash", "PATCH trashed: true", "23"],
                        ["downloadAsExcel", "a file on your disk", "GET export", "22"],
                        ["token-sheets.pickle", "your sign-in", "none: a local pickle", "8"]],
                  colw=[2.3, 2.7, 2.9, 0.9], rowh=0.42, fs=12, takeaway="Each call is a request; a loaded sheet is read without one."),
}

CURRENT_SUB = "What differs from the book, from the chapter research"

CURRENT = [["What differs from the book", "Today", "Example"],
           ["ss.Sheet('Spam') returns the new Sheet", "Sheet() returns None; use createSheet", "sheet_tabs"],
           ["sheet['B2'] = 30 prints '30'", "prints the number 30 until refresh()", "cell_rw"],
           ["Downloads are named Sweigart_Books.xlsx", "named Sweigart_Books_(DO_NOT_DELETE).xlsx", "upload_download"],
           ["250 new spreadsheets a day", "no such figure; 300 reads and 300 writes a minute per project", "quota_backoff"],
           ["The setup is done once", "in Testing status the sign-in expires every seven days", "token_expiry"],
           ["Token files are JSON files", "they are pickles, and a pickle can run code", "token_pickle"],
           ["The consent screen wizard", "now the pages Branding, Audience, Data Access", "auth_url"],
           ["Up to 10 million cells", "Google's help says 20 million cells or 100 MB", ""],
           ["Step 2 adds one row", "it sends six requests, and two writers can collide", "lost_update"],
           ["The book opens sheets by short links (autbor.com)", "some requests were answered 403; open by id", "open_three_ways"]]

CURRENT_TAKEAWAY = "Run what the book printed; then check what changed."

SUMMARY_ANALOGY = "A summary keeps only the five ideas you need to take away from the lecture."

SUMMARY_POINTS = ["A program must be let in: a cloud project, a credentials file, token files.",
                  "A token file is a pickle: never load one you did not make.",
                  "A Spreadsheet object stands for one spreadsheet, a Sheet object for one tab; each call is a request.",
                  "Batch your writes: Google limits requests, not values.",
                  "A ledger of rows is easy to audit and just as easy to forge."]

SUMMARY_TAKEAWAY = "Let the program in, batch the writes, and check the ledger."

PRACTICE_SUB = "Predict first, then run what you can on the chapter page"

PRACTICE_ANALOGY = "Practice questions are short drills: predict the answer first, then run the code."

PRACTICE = ["Which column letters name column 703, and which number has the name ZZ? Use the code of the addresses slide.",
            "A program writes 100 cells one at a time. How many requests are sent, and how many with updateColumn?",
            "Two programs open the same ledger and each adds a row. What do you see in the sheet, and why?",
            "Practice program: write a Bean Count check that also prints the correct total next to each wrong one."]

PRACTICE_TAKEAWAY = "Each answer fits in a few lines you can run."

RESOURCES_SUB = "Reading and watching, chosen for this chapter; every link is live"

RESOURCES_TAKEAWAY = "Pick one link and read it before the next class."

RESOURCES = [
    ("Book: Automate the Boring Stuff, 3rd edition, chapter 15", "https://automatetheboringstuff.com/3e/chapter15.html", "automatetheboringstuff.com"),
    ("EZSheets documentation (Read the Docs)", "https://ezsheets.readthedocs.io/en/latest/", "ezsheets.readthedocs.io"),
    ("EZSheets on the Python Package Index", "https://pypi.org/project/ezsheets/", "pypi.org"),
    ("Google Sheets API: usage limits", "https://developers.google.com/workspace/sheets/api/limits", "developers.google.com"),
    ("Google Sheets API: reading and writing values", "https://developers.google.com/workspace/sheets/api/guides/values", "developers.google.com"),
    ("Google Sheets API: choose scopes", "https://developers.google.com/workspace/sheets/api/scopes", "developers.google.com"),
    ("Google Sheets API: migrate from v3", "https://developers.google.com/workspace/sheets/api/guides/migration", "developers.google.com"),
    ("Google Identity: OAuth 2.0 for desktop apps", "https://developers.google.com/identity/protocols/oauth2/native-app", "developers.google.com"),
    ("RFC 7636: Proof Key for Code Exchange", "https://www.rfc-editor.org/rfc/rfc7636.txt", "rfc-editor.org"),
    ("Python documentation: pickle", "https://docs.python.org/3/library/pickle.html", "docs.python.org"),
    ("OWASP: Deserialization Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html", "cheatsheetseries.owasp.org"),
    ("gspread documentation: the other library", "https://docs.gspread.org/en/latest/", "docs.gspread.org"),
    ("Introduction to OAuth (oauth.net)", "https://oauth.net/about/introduction/", "oauth.net"),
    ("Bitcoin: A Peer-to-Peer Electronic Cash System", "https://bitcoin.org/bitcoin.pdf", "bitcoin.org"),
]
