"""Chapter 15 deck examples, version 2.0.0: the code examples of the chapter 15 lecture deck (Google Sheets).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language explanation that
stands beside it); the lines of all groups of an example, in order, are the example's code: that text is what the deck shows after the '>>> '
prompt of each line, what the chapter-code manifest lists and what the page runs. A code box holds at most 30 words (the deck standard counts
a code box as a text box), the explanation of a group at most 30 words.
Every example is self-contained (it imports what it uses), runs offline, reads no keyboard and opens no window, and prints an ordinary line first
(never an error message, so that the page can draw its result). Google was never reached: every example that touches a spreadsheet runs the REAL
ezsheets library (release 2026.4.28) and the real google-api-python-client against the stand-in for Google's answers, the module google_standin
(03-materials/ch15/assets/google_standin_v1_0_0.py, installed by the page under the name google_standin), which keeps every cell as text. The
chapter's own sheets (Boringcoin, Bean Count, produceSales3, Sweigart Books) are replaced by small stand-ins typed into the example, with the same
columns, and each slide says so beside the code.
Nothing here carries a result; deck_build_v2_0_0.py runs the code and takes every printed result from the run."""
__version__ = "2.0.0"

EXAMPLES = [
    # ------------------------------------------------------------ part 1: access, sign-in and token files
    dict(id="setup_state", name="Before the sign-in: version, state, scopes", title="Before the sign-in: what EZSheets knows", part=1, visual="setup_state",
         concepts=["Installing and Setting Up EZSheets", "ezsheets", "scope", "ezsheets.init()"],
         groups=[
             (["import ezsheets, google_standin", "google_standin.uninstall()", "print('ezsheets', ezsheets.__version__)", "print('signed in:', ezsheets.IS_INITIALIZED)"],
              "uninstall() takes the stand-in for Google out, so the library is as it is before any sign-in. IS_INITIALIZED stays False until a sign-in has worked."),
             (["print('sheets scope:', ezsheets.SCOPES_SHEETS[0])", "print('drive scope:', ezsheets.SCOPES_DRIVE[0])"],
              "A scope is a permission the program asks for. EZSheets asks for the whole spreadsheets scope and the whole drive scope."),
         ]),
    dict(id="token_file", name="What a token file holds", title="A token file holds a credentials object", part=1, visual="token_file",
         concepts=["token file", "refresh token", "credentials file", "pickle"],
         groups=[
             (["import json, pickle", "from google.oauth2.credentials import Credentials", "creds = Credentials(token='FAKE-access', refresh_token='FAKE-refresh',",
               "    token_uri='https://oauth2.googleapis.com/token',", "    scopes=['https://www.googleapis.com/auth/spreadsheets'])"],
              "A made-up token with the fields of a real one: access token, refresh token, scopes."),
             (["for key, value in json.loads(creds.to_json()).items():", "    print(key, '=', value)", "print(type(pickle.loads(pickle.dumps(creds))).__name__)"],
              "to_json lists the fields. EZSheets saves the object with pickle in token-sheets.pickle."),
         ]),
    dict(id="auth_url", name="The sign-in address the library builds", title="The sign-in address: code, offline access and a challenge", part=1, visual="auth_url",
         concepts=["Logging In with the Credentials File", "google_auth_oauthlib", "OAuth consent screen", "Creating Credentials"],
         groups=[
             (["from google_auth_oauthlib.flow import Flow", "SCOPE = 'https://www.googleapis.com/auth/spreadsheets'",
               "cfg = {'installed': {'client_id': 'FAKE', 'client_secret': 'FAKE',", "    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',",
               "    'token_uri': 'https://oauth2.googleapis.com/token'}}"],
              "The credentials file as a dictionary: an id and a secret, here made up, and Google's two addresses."),
             (["flow = Flow.from_client_config(cfg, [SCOPE],", "    redirect_uri='http://localhost:8080/')", "url, state = flow.authorization_url(access_type='offline')"],
              "No network is used: the flow only builds the address the browser would open."),
             (["q = dict(p.split('=') for p in url.split('?')[1].split('&'))", "for k in ('response_type', 'access_type', 'code_challenge_method'):", "    print(k, '=', q[k])"],
              "Three parts of the address: a code, offline access and a SHA-256 challenge."),
         ]),
    dict(id="pkce", name="The challenge: a hash of a secret", title="The challenge is a hash of a secret the program keeps", part=1, visual="pkce",
         concepts=["refresh token", "google_auth_oauthlib"],
         groups=[
             (["import hashlib, base64", "verifier = b'dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'"],
              "The program makes a random secret, the verifier, and keeps it. This one is the example of RFC 7636, the standard behind the challenge."),
             (["digest = hashlib.sha256(verifier).digest()", "challenge = base64.urlsafe_b64encode(digest).rstrip(b'=')", "print('verifier :', verifier.decode())",
               "print('challenge:', challenge.decode())"],
              "Only the hash, the challenge, goes into the address. Later the program shows the verifier; Google hashes it again and compares."),
         ]),
    dict(id="token_pickle", name="Loading a pickle can run code", title="A token file is a pickle, and a pickle can run code", part=1, visual="token_pickle",
         concepts=["pickle", "token file", "Revoking the Credentials File"],
         groups=[
             (["import pickle", "class Trap:", "    def __reduce__(self):", "        return (print, ('this line ran while loading',))"],
              "A class can tell pickle what to call when it is loaded. Here the call is harmless: it prints a line. In an attack it would be any code."),
             (["data = pickle.dumps(Trap())", "print('file written:', len(data), 'bytes')", "pickle.loads(data)"],
              "Loading the bytes runs the call. EZSheets loads token-sheets.pickle when it is imported, so never use a token file from someone else."),
         ]),
    dict(id="token_expiry", name="Valid, expired and renewable tokens", title="A token has a lifetime; the refresh token renews it", part=1, visual="token_expiry",
         concepts=["refresh token", "token file", "Configuring the OAuth Consent Screen"],
         groups=[
             (["import datetime as dt", "from google.oauth2.credentials import Credentials", "now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)"],
              "The library compares a token's expiry with the clock. Times are in UTC without a time zone, as the library keeps them."),
             (["for name, h in (('fresh', 1), ('stale', -1), ('week old', -168)):", "    c = Credentials('X', 'X', expiry=now + dt.timedelta(hours=h))",
               "    print(name, '| valid:', c.valid, '| expired:', c.expired)"],
              "An expired token is renewed with the refresh token. In an app in Testing status the refresh token itself dies after seven days."),
         ]),
    # ------------------------------------------------------------ part 2: spreadsheet objects
    dict(id="create_list", name="Create a spreadsheet and list spreadsheets", title="Create a spreadsheet, list the spreadsheets of the account", part=2, visual="create_list",
         concepts=["Creating, Uploading, and Listing Spreadsheets", "ezsheets.Spreadsheet()", "ezsheets.listSpreadsheets()", "Spreadsheet object"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "ss = ezsheets.Spreadsheet()", "other = ezsheets.createSpreadsheet('Boringcoin')",
               "print(ss.title, '|', other.title)"],
              "install() plugs the stand-in for Google into ezsheets. Spreadsheet() makes a spreadsheet; createSpreadsheet gives it a title."),
             (["print(ezsheets.listSpreadsheets())", "print(len(g.log), 'requests so far')"],
              "listSpreadsheets returns a dictionary from id to title. The recorder counts the requests."),
         ]),
    dict(id="open_three_ways", name="Open one spreadsheet by id and by address", title="Open a spreadsheet: id, address and getIdFromUrl", part=2, visual="open_three_ways",
         concepts=["ezsheets.Spreadsheet()", "Accessing Spreadsheet Attributes", "http.client", "Spreadsheet object"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "ss = ezsheets.Spreadsheet(g.load('SHEET123', 'Boringcoin', [['A']]))",
               "url = 'https://docs.google.com/spreadsheets/d/SHEET123/edit#gid=0'"],
              "A stand-in for the public Boringcoin sheet is loaded under a made-up id."),
             (["print(ezsheets.Spreadsheet('SHEET123').title)", "print(ezsheets.Spreadsheet(url).title)", "print(ezsheets.getIdFromUrl(url))",
               "print(ezsheets.getIdFromUrl('https://docs.google.com/spreadsheets/d/SHEET123'))"],
              "An id or an address opens the same spreadsheet. getIdFromUrl cuts by position, so an address ending after the id loses a character."),
         ]),
    dict(id="attributes", name="Spreadsheet attributes you can and cannot set", title="Spreadsheet attributes: title, sheetTitles, id and url", part=2, visual="attributes",
         concepts=["Accessing Spreadsheet Attributes", "Spreadsheet object"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "ss = ezsheets.Spreadsheet()", "ss.title = 'Sweigart Books'",
               "print(ss.title, ss.sheetTitles, ss.id, ss.url)"],
              "The title is the only attribute you can change; the new title is sent to Google at once. The others describe the spreadsheet."),
             (["for name in ('id', 'url', 'sheetTitles'):", "    try: setattr(ss, name, 'x')", "    except AttributeError as e: print(name, '->', e)"],
              "The other three are read-only: setting one raises an AttributeError, which the program catches and prints."),
         ]),
    dict(id="upload_download", name="Upload a file and download in six formats", title="Upload a file, download a spreadsheet in six formats", part=2, visual="upload_download",
         concepts=["Downloading and Uploading Spreadsheets", "ezsheets.upload()", "Spreadsheet.downloadAsExcel()", "Converting Spreadsheets to Other Formats"],
         groups=[
             (["import ezsheets, google_standin, os, tempfile", "g = google_standin.install()", "os.chdir(tempfile.mkdtemp())", "open('data.csv', 'w').write('a,b\\n1,2\\n')"],
              "A small file is made in a temporary folder. upload() turns it into a spreadsheet."),
             (["print(ezsheets.upload('data.csv').title)", "ss = ezsheets.Spreadsheet(g.load('X', 'Sweigart Books (DO NOT DELETE)', [['T']]))", "for fmt in ('Excel', 'CSV', 'TSV', 'PDF', 'ODS', 'HTML'):",
               "    print(fmt, '->', getattr(ss, 'downloadAs' + fmt)())"],
              "Each downloadAs method exports the spreadsheet and saves a file. Odd characters in the title become underscores."),
         ]),
    dict(id="delete_trash", name="Delete: to the Trash, or for good", title="Delete moves a spreadsheet to the Trash", part=2, visual="delete_trash",
         concepts=["Deleting Spreadsheets", "Spreadsheet.delete()", "Trash"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "ss = ezsheets.Spreadsheet()", "keep = ezsheets.createSpreadsheet('Keep me')",
               "ss.delete()", "print(g.log[-1][0], g.log[-1][3])", "print(ezsheets.listSpreadsheets())"],
              "delete() only moves the spreadsheet to the Trash: a PATCH sets trashed to True. It is still listed."),
             (["ss.delete(permanent=True)", "print(g.log[-1][0], 'then', list(ezsheets.listSpreadsheets().values()))"],
              "delete(permanent=True) sends a DELETE request. Only now is it gone from the list."),
         ]),
    # ------------------------------------------------------------ part 3: sheet objects
    dict(id="cell_rw", name="Read and write a cell", title="Read and write a cell: A1 notation and column, row", part=3, visual="cell_rw",
         concepts=["Reading and Writing Data", "A1 notation", "1-based index", "Sheet object", "IGNORE_QUOTA"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "rows = [['PRODUCE', 'COST', 'POUNDS'], ['Okra', '2.26', '38.6']]",
               "sheet = ezsheets.Spreadsheet(g.load('P', 'produce', rows)).sheets[0]"],
              "A stand-in for the chapter's produce sheet: three columns and one row of data."),
             (["g.log.clear()", "print(sheet['A1'], sheet[1, 1], sheet['B2'], sheet[2, 2])", "print(len(g.log), 'requests to read four cells')"],
              "A cell is 'B2' or (2, 2): letter or column first, counting from 1. Reading a loaded sheet sends nothing."),
             (["sheet['B2'] = 30", "print(repr(sheet['B2']), '|', g.log[-1][0], g.log[-1][2].split('&')[0])", "sheet.refresh()", "print(repr(sheet['B2']))"],
              "A write is one PUT request. The local copy shows 30 until refresh() reads the text Google holds."),
         ]),
    dict(id="addresses", name="Addresses and column letters", title="Addresses and column letters: convertAddress and friends", part=3, visual="addresses",
         concepts=["ezsheets.convertAddress()", "ezsheets.getColumnLetterOf()", "ezsheets.getColumnNumberOf()", "A1 notation"],
         groups=[
             (["import ezsheets", "print(ezsheets.convertAddress('A2'), ezsheets.convertAddress(1, 2))", "print(ezsheets.convertAddress((2, 5)))"],
              "convertAddress turns a name such as 'A2' into a (column, row) pair, and a pair back into a name."),
             (["L, N = ezsheets.getColumnLetterOf, ezsheets.getColumnNumberOf", "print(L(2), L(27), L(999))", "print(N('B'), N('ZZZ'))"],
              "Column letters count like digits without a zero: 27 is AA, 999 is ALK and ZZZ is column 18278, the last one a sheet can have."),
         ]),
    dict(id="rows_columns", name="Rows and columns: getRow, getColumn, updateRow", title="Rows and columns: get and update whole lines", part=3, visual="rows_columns",
         concepts=["Reading and Writing Data", "Sheet.getRow()", "Sheet.getRows()", "Sheet.getColumn()", "Sheet.updateRow()", "Sheet.updateColumn()"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "rows = [['PRODUCE', 'COST', 'POUNDS'], ['Okra', '2.26', '38.6'],",
               "        ['Garlic', '1.19', '10']]", "sheet = ezsheets.Spreadsheet(g.load('P', 'produce', rows)).sheets[0]"],
              "The stand-in produce sheet: a heading and two rows."),
             (["print(sheet.getRow(2))", "print(sheet.getColumn('A') == sheet.getColumn(1), sheet.getColumn(1)[:3])"],
              "getRow and getColumn return lists of text. A column is a letter or a number."),
             (["sheet.updateRow(3, ['Pumpkin', '11.50', '20'])", "sheet.updateColumn(1, [v.upper() for v in sheet.getColumn(1)])", "print(sheet.getRows())"],
              "Each update replaces a whole line with one request."),
         ]),
    dict(id="batch_writes", name="One request per cell, or one for the column", title="Cell by cell costs a request each; a column costs one", part=3, visual="batch_writes",
         concepts=["Reading and Writing Data", "Sheet.updateRows()", "Working with Google Sheets Quotas", "Sheet.updateColumn()"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "values = [str(n) for n in range(1, 9)]",
               "sheet = ezsheets.Spreadsheet(g.load('S', 'Counts', [['']] * 8)).sheets[0]"],
              "A stand-in sheet of one column and eight empty rows, and eight values."),
             (["g.log.clear()", "for row, value in enumerate(values, 1): sheet[1, row] = value", "print('cell by cell:', len(g.log), 'requests')"],
              "Writing cell by cell sends one PUT request for each value."),
             (["g.log.clear()", "sheet.updateColumn(1, values)", "print('whole column:', len(g.log), 'request')"],
              "updateColumn sends all eight in one request. Google limits requests, not values."),
         ]),
    dict(id="sheet_tabs", name="Create, move and delete sheets", title="Create, move and delete the sheets of a spreadsheet", part=3, visual="sheet_tabs",
         concepts=["Creating, Moving, and Deleting Sheets", "Spreadsheet.createSheet()", "Sheet.delete()", "Spreadsheet.Sheet()"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "ss = ezsheets.Spreadsheet()", "print(ss.Sheet('Spam'))", "ss.createSheet('Eggs')",
               "ss.createSheet('Bacon', 0)", "print(ss.sheetTitles)"],
              "Spreadsheet.Sheet() returns nothing in the current library, so it prints None. createSheet returns the Sheet, and a second argument chooses its place."),
             (["ss.sheets[0].index = 2", "print(ss.sheetTitles)", "ss.sheets[1].delete()", "print(ss.sheetTitles)"],
              "Setting index moves a sheet to a new place; delete() removes one. Sheets are counted from 0, like list items."),
         ]),
    dict(id="copy_clear", name="Copy a sheet and clear a sheet", title="Copy a sheet to another spreadsheet, and clear one", part=3, visual="copy_clear",
         concepts=["Copying Sheets", "Sheet.copyTo()", "Sheet.clear()", "Spreadsheet.refresh()"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "rows = [['PRODUCE', 'COST', 'POUNDS'], ['Okra', '2.26', '38.6']]",
               "source = ezsheets.Spreadsheet(g.load('P', 'produce', rows)).sheets[0]", "target = ezsheets.Spreadsheet()"],
              "A source sheet with data, and a new empty spreadsheet for the copy."),
             (["source.copyTo(target)", "target.refresh()", "print(target.sheetTitles, target.sheets[1].getRows())"],
              "copyTo adds a 'Copy of ...' sheet to the other spreadsheet. refresh() reads it."),
             (["source.clear()", "print(source.getRows(), source.rowCount, source.columnCount)"],
              "clear() empties every cell; the sheet keeps its size."),
         ]),
    dict(id="surprises", name="Surprises of the library", title="Surprises: equal sheets, the in operator, an empty cell", part=3, visual="surprises",
         concepts=["Sheet object", "Accessing Spreadsheet Attributes", "Spreadsheet.Sheet()"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "a = ezsheets.Spreadsheet().sheets[0]", "b = ezsheets.Spreadsheet().sheets[0]",
               "print('equal:', a == b, '| ids', a.sheetId, b.sheetId)"],
              "Two sheets are equal when their sheet ids are equal. The first sheet of every new spreadsheet has the id 0, so unrelated sheets compare equal."),
             (["names = ezsheets.Spreadsheet(g.load('Q', 'Q', [['Alice', '1']])).sheets[0]", "print('Alice in sheet:', 'Alice' in names)", "print('empty cell is', repr(names['C1']))"],
              "The in operator searches the coordinates, not the values, so a name in a cell is not found. An empty cell is an empty string, never None."),
         ]),
    # ------------------------------------------------------------ part 4: forms, formats and quotas
    dict(id="forms_emails", name="Collect e-mail addresses from form answers", title="Google Forms answers are rows: collect the e-mail addresses", part=4, visual="forms_emails",
         concepts=["Google Forms", "Downloading Google Forms Data", "Practice Programs"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "answers = [['Timestamp', 'Name', 'Email address'],",
               "           ['10:00', 'Ada', 'ada@example.org'],", "           ['10:05', 'Alan', 'alan@example.org'],", "           ['10:09', 'Ada', 'ada@example.org']]"],
              "A form saves each answer as a row of a spreadsheet. These three answers stand in for the response sheet of a real form."),
             (["sheet = ezsheets.Spreadsheet(g.load('F', 'Responses', answers)).sheets[0]", "emails = sheet.getColumn(3)[1:]", "print(emails)", "print(sorted(set(emails)))"],
              "Column 3 holds the addresses; the first item is the heading, so it is cut off. A set removes the address that answered twice."),
         ]),
    dict(id="quota_backoff", name="Quota errors: the library waits and retries", title="Quota: the library waits 10 to 45 seconds and retries", part=4, visual="quota_backoff",
         concepts=["Working with Google Sheets Quotas", "quota", "IGNORE_QUOTA", "googleapiclient"],
         groups=[
             (["import ezsheets, google_standin, time, types", "g = google_standin.install()", "pauses = []",
               "ezsheets.time = types.SimpleNamespace(sleep=pauses.append, time=time.time)"],
              "The pauses are recorded instead of slept, so the example needs no waiting. The library's clock is put back at the end."),
             (["g.fail = [(429, 'RESOURCE_EXHAUSTED')] * 20", "try:", "    ezsheets.Spreadsheet()", "except Exception as e:",
               "    print(len(g.log), 'tries,', sum(pauses), 'seconds,', type(e).__name__)", "ezsheets.time = time"],
              "Google answers 429 again and again. The library pauses 10, 15, ... 45 seconds, tries nine times and gives up. Any other error stops it at once."),
         ]),
    # ------------------------------------------------------------ part 5: Project 11 and the practice programs
    dict(id="audit", name="Project 11, step 1: audit the ledger", title="Project 11, step 1: audit the Boringcoin ledger", part=5, visual="audit",
         concepts=["Project 11: Fake Blockchain Cryptocurrency Scam", "fake blockchain", "Sheet.getRows()"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "ledger = [['PRE-MINE', 'Alice', '1000'], ['PRE-MINE', 'Bob', '500'],",
               "          ['Alice', 'Bob', '200'], ['Bob', 'Carol', '150']]", "sheet = ezsheets.Spreadsheet(g.load('B', 'Boringcoin', ledger)).sheets[0]"],
              "A stand-in for the Boringcoin sheet: sender, recipient, amount. PRE-MINE invents money."),
             (["accounts = {}", "for sender, recipient, amount in sheet.getRows():", "    if sender != 'PRE-MINE':", "        accounts[sender] = accounts.get(sender, 0) - int(amount)",
               "    accounts[recipient] = accounts.get(recipient, 0) + int(amount)"],
              "One walk over the rows: the sender loses the amount, the recipient gains it."),
             (["print(accounts)", "print('Total Boringcoins:', sum(accounts.values()))"],
              "An honest ledger adds up to the money PRE-MINE created."),
         ]),
    dict(id="audit_empty", name="The audit stops at an empty row", title="The audit meets an empty row of the grid", part=5, visual="audit_empty",
         concepts=["Project 11: Fake Blockchain Cryptocurrency Scam", "Sheet.getRows()", "Finding Mistakes in a Spreadsheet"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "ledger = [['PRE-MINE', 'Alice', '1000'], ['Alice', 'Bob', '200']]",
               "sheet = ezsheets.Spreadsheet(g.load('B', 'Boringcoin', ledger)).sheets[0]", "sheet.rowCount += 1"],
              "The real sheet is a grid of 1,000 rows, so getRows also returns the empty ones. One added row shows what an empty row looks like."),
             (["print('audit of', len(sheet.getRows()), 'rows')", "try: total = sum(int(row[2]) for row in sheet.getRows())", "except ValueError as e: print('stopped:', e)"],
              "int('') cannot read an empty amount, so the loop of Step 1 stops with a ValueError. A guard for an empty first cell avoids it."),
         ]),
    dict(id="add_transaction", name="Project 11, step 2: add a transaction", title="Project 11, step 2: add one transaction", part=5, visual="add_transaction",
         concepts=["Project 11: Fake Blockchain Cryptocurrency Scam", "sys", "shlex", "Sheet.getRow()"],
         groups=[
             (["import ezsheets, google_standin, sys", "g = google_standin.install()", "sys.argv = ['add.py', 'Al Sweigart', 'Eve', '2000']",
               "sender, recipient, amount = sys.argv[1:]"],
              "The program reads sender, recipient and amount from the command line, here set by hand."),
             (["ledger = [['PRE-MINE', 'Alice', '1000'], ['Alice', 'Bob', '200']]", "sheet = ezsheets.Spreadsheet(g.load('B', 'Boringcoin', ledger)).sheets[0]", "g.log.clear()", "sheet.rowCount += 1"],
              "Adding a row changes the sheet's size, which costs three requests."),
             (["for col, value in enumerate((sender, recipient, amount), 1):", "    sheet[col, sheet.rowCount] = value",
               "print(sheet.getRow(sheet.rowCount), '|', len(g.log), 'requests')"],
              "Each cell is one more request: six in all. A name with a space needs quotes."),
         ]),
    dict(id="lost_update", name="Two programs add a row at the same time", title="Two programs add a row: one transaction is lost", part=5, visual="lost_update",
         concepts=["Project 11: Fake Blockchain Cryptocurrency Scam", "Spreadsheet object", "Sheet.refresh()"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "ledger = [['PRE-MINE', 'Alice', '1000'], ['Alice', 'Bob', '200']]",
               "first = ezsheets.Spreadsheet(g.load('B', 'Boringcoin', ledger)).sheets[0]", "second = ezsheets.Spreadsheet('B').sheets[0]"],
              "Two programs open the same spreadsheet. Each keeps its own copy of the row count."),
             (["for who, sheet in (('first', first), ('second', second)):", "    sheet.rowCount += 1; sheet[1, sheet.rowCount] = who",
               "    print(who, 'writes to row', sheet.rowCount)", "first.refresh()", "print(first.rowCount, first.getRow(3))"],
              "Both count the next row from their own copy, so both write to row 3 and the second silently replaces the first. No error is raised."),
         ]),
    dict(id="bean_count", name="Finding mistakes: check the totals", title="Finding mistakes in a spreadsheet: quantity times price", part=5, visual="bean_count",
         concepts=["Finding Mistakes in a Spreadsheet", "Practice Programs", "Sheet.getRows()"],
         groups=[
             (["import ezsheets, google_standin", "g = google_standin.install()", "beans = [['Qty', 'Price', 'Total'], ['4', '25', '100'],",
               "         ['3', '40', '130'], ['10', '12', '120']]",
               "rows = ezsheets.Spreadsheet(g.load('BEAN', 'Beans', beans)).sheets[0].getRows()"],
              "A stand-in for the Bean Count sheet: quantity, price and a typed total. One total is wrong."),
             (["for n, (qty, price, total) in enumerate(rows[1:], 2):", "    if int(qty) * int(price) != int(total):",
               "        print('row', n, 'says', total, 'is', int(qty) * int(price))"],
              "Check every row against quantity times price. The heading is row 1, so data starts at row 2."),
         ]),
]

BY_ID = {e["id"]: e for e in EXAMPLES}
assert len(BY_ID) == len(EXAMPLES)
assert len({e["name"] for e in EXAMPLES}) == len(EXAMPLES)


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
