"""Chapter 8 deck content, version 2.1.0: the words of the deck. A NEW file; the analogies and the resources of version 2.0.0 are read
from deck_content_v2_0_0.py (unchanged), everything else is written anew for the Owner's review remarks of 2026-10-30: every concept
is taught on the slides (idea, reason, everyday picture, drawn mechanism, code, executed result), stories are told as connected
sentences without label words, speaker notes carry what to say, one example and one question (40 to 60 words)."""
__version__ = "2.1.0"
import importlib.util
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("deck_content_v2_0_0", os.path.join(_here, "deck_content_v2_0_0.py"))
_old = importlib.util.module_from_spec(_sp)
sys.modules["deck_content_v2_0_0"] = _old
_sp.loader.exec_module(_old)
ANALOGIES = _old.ANALOGIES
RESOURCES = _old.RESOURCES
TAKEAWAY = _old.TAKEAWAY

# ---- stories: connected sentences, three boxes of at most 30 words each, a picture and a live link
STORIES = {
    "utf8": dict(title="Story: UTF-8 on a diner placemat", img="photo_ken_thompson_2019.jpg", credit="Ken Thompson, 2019. Photo: A.C.Diller, CC BY-SA 4.0, Wikimedia Commons.",
                 p1="In September 1992, Ken Thompson and Rob Pike of Bell Labs were building Plan 9. In a New Jersey diner, in one evening, they sketched a new encoding.",
                 p2="Programs needed one encoding for every language that did not break old ASCII text. Their answer gives a character one to four bytes and leaves plain ASCII unchanged.",
                 p3="You can watch it work: 'café'.encode('utf-8') turns four characters into five bytes, and the next code slide runs exactly that.",
                 link="https://doc.cat-v.org/bell_labs/utf-8_history", linktext="Read Rob Pike's own account (doc.cat-v.org)"),
    "unicode": dict(title="Story: nine companies agree on one table", img="logo_unicode.png", credit="Unicode logo. Wikimedia Commons, CC BY-SA 4.0.",
                    p1="On 19 February 1991, a press release from Mountain View, California, announced Unicode Inc., backed by Apple, GO, IBM, Metaphor, Microsoft, NeXT, Novell, the Research Libraries Group and Sun.",
                    p2="They agreed to keep one table that gives every character its number, so that any program can agree on what a number means.",
                    p3="That is why ord('A') is 65 and chr(8364) is the euro sign: Python reads the same table.",
                    link="https://www.unicode.org/history/first-pr.htm", linktext="Read the 1991 press release (unicode.org)"),
    "pep498": dict(title="Story: one proposal gave Python the f-string", img="logo_python.png", credit="Python logo. Source: python.org, Python Software Foundation, used under its trademark policy.",
                   p1="Eric V. Smith wrote PEP 498, Literal String Interpolation, and created the proposal on 1 August 2015. It lives in the Python Enhancement Proposal index at peps.python.org.",
                   p2="Older styles keep the text and its values apart. One literal with expressions inside braces keeps them together, and Python 3.6 shipped it.",
                   p3="f'My name is {name}' has worked the same way in every Python release since 3.6.",
                   link="https://peps.python.org/pep-0498/", linktext="Read PEP 498 (peps.python.org)"),
    "tesler": dict(title="Story: copy and paste is fifty years old", img="photo_larry_tesler_2007.jpg", credit="Larry Tesler, 2007. Photo: Yahoo! Blog, CC BY 2.0, Wikimedia Commons.",
                   p1="From 1973, Larry Tesler, working with Tim Mott at Xerox PARC in Palo Alto, shaped cut, copy and paste on the Gypsy word processor. He died on 16 February 2020.",
                   p2="Editing needs one simple idea: select something, hold it somewhere, insert it elsewhere.",
                   p3="pyperclip.copy() and pyperclip.paste() are that idea in two function calls.",
                   link="https://en.wikipedia.org/wiki/Larry_Tesler", linktext="Read about Larry Tesler (Wikipedia)"),
}
STORY_NOTES = {
    "utf8": "Rob Pike wrote that UTF-8 was sketched on a diner placemat in New Jersey in September 1992. Plain ASCII text stays valid. Show the café example that follows. Ask the class: why must a new encoding keep old ASCII files readable?",
    "unicode": "On 19 February 1991 nine companies announced Unicode Inc. Every ord and chr call reads from the table this group keeps. Name one company from the list. Ask the class: which character that is not on your keyboard would you want in a table?",
    "pep498": "PEP 498 was created on 1 August 2015 and reached Python 3.6. Open the proposal page and show the date. Tell the class the f-string keeps text and values together. Ask: what went wrong in older code when the text and the values drifted apart?",
    "tesler": "Larry Tesler brought cut, copy and paste to computing at Xerox PARC in 1973. The clipboard program of this chapter makes the same three moves in code. Ask the class: which of the three moves, select, hold or insert, does pyperclip.paste do?",
}

# ---- teach slides: one per code example. idea, reason and picture are single short boxes; flow = the drawn mechanism, three or four steps
TEACH = {
    "quotes": dict(title="Quotes: how text is written in code", idea="A string literal is text written between quotes. Python reads it and creates a string object that holds those characters.",
                   reason="Code needs a clear border between text and instructions. Two quote styles exist so that one kind can sit inside the other.",
                   picture="A string literal is a sign written exactly as it will hang on the shop door.",
                   flow=[("You type", "\"Alice's cat\" or 'Bob\\'s cat'"), ("Python reads", "the quotes only mark the border"), ("Python stores", "Alice's cat, 11 characters"), ("print shows", "the text without the quotes")]),
    "escapes": dict(title="Escape sequences: characters you cannot type", idea="An escape sequence is a backslash plus one letter or symbol. Python turns the pair into a single character such as a tab or a new line.",
                    reason="Some characters, like a line break, cannot sit inside a one-line literal. The backslash is a signal that the next symbol has a special meaning.",
                    picture="An escape sequence is a stage direction in a script: it says tab here, and nobody speaks it.",
                    flow=[("You type", "two symbols: \\ and t"), ("Python sees", "the backslash starts a code"), ("Python stores", "one tab character"), ("len counts", "1, not 2")]),
    "raw_multiline": dict(title="Raw strings and triple quotes", idea="A raw string, written with an r before the quote, keeps every backslash as typed. Triple quotes let a literal run over many lines.",
                          reason="File paths and patterns are full of backslashes. Long text with quotes inside is painful to escape one by one.",
                          picture="A raw string is a photocopy: every mark, every backslash, is copied as it stands.",
                          flow=[("Plain literal", "backslash plus n becomes one line break"), ("Raw literal", "backslash plus n stays two characters"), ("Triple quotes", "both quote kinds and line breaks allowed"), ("Result", "len shows 2 for raw, 1 for plain")]),
    "index": dict(title="Indexes: a number for every character", idea="An index is the position of one character in a string. Counting starts at 0, and negative numbers count back from the end.",
                  reason="A program must say which character it wants. A number is the shortest and safest way to point at one.",
                  picture="An index is the number on a coat-check ticket: it leads you to exactly one coat.",
                  flow=[("The string", "Hello, world! has 13 characters"), ("From the left", "index 0 is H, index 4 is o"), ("From the right", "index -1 is the last character"), ("The limit", "the last index is len minus 1")]),
    "slice": dict(title="Slices: cutting out a piece", idea="A slice takes a run of characters, written start, colon, stop. The character at stop is not included, and a step can skip or reverse.",
                  reason="Programs often need a part of a text, such as a prefix or an ending. A slice cuts it without a loop.",
                  picture="A slice is a piece of cake cut between two marks; the second mark is not included.",
                  flow=[("Choose marks", "start 0, stop 5"), ("Python cuts", "characters 0 up to 4"), ("A new string", "Hello"), ("Step -1", "walks backwards and reverses")]),
    "in_immutable": dict(title="The in operator and strings that never change", idea="The in operator answers True or False: does one text sit inside another? A string itself can never be changed in place.",
                         reason="Searching is the most common question about text. Fixed strings are safe to share, so edits always make a new string.",
                         picture="The in operator is Ctrl+F on a page: it only answers yes or no.",
                         flow=[("Ask", "'Hello' in 'Hello, World'"), ("Python scans", "case sensitive, left to right"), ("Answer", "True or False, never a position"), ("To edit", "build a new string from slices")]),
    "fstring": dict(title="F-strings: text with holes", idea="An f-string is a literal that starts with f. Each pair of braces holds an expression that Python runs and pastes into the text.",
                    reason="Joining text and values with plus is clumsy and error prone. An f-string keeps the sentence and its values together.",
                    picture="An f-string is a form letter whose blanks fill themselves from your address book.",
                    flow=[("Write", "f'I am {age} years old'"), ("Python evaluates", "age is 4000"), ("Python pastes", "the value into the hole"), ("Result", "I am 4000 years old")]),
    "fspec": dict(title="Format specifications after the colon", idea="Inside a brace, the text after a colon says how to show the value: decimals, width, alignment, separators. An equals sign shows the name too.",
                  reason="Numbers must line up in reports and be readable. The specifier shapes them without extra functions.",
                  picture="A format specifier is the style menu of a spreadsheet cell: the number stays, the look changes.",
                  flow=[("Value", "3.14159"), ("Specifier", ".2f after the colon"), ("Python formats", "rounds to two decimals"), ("Shown", "3.14")]),
    "older": dict(title="Older styles: percent, format() and plus", idea="Before f-strings Python used the percent operator, the format method and plain joining. They still fill slots with values.",
                  reason="You will meet them in existing code, so you must read them. New code should prefer the f-string.",
                  picture="The older styles are mail-merge with slots: the values wait in a queue, or in numbered mailboxes.",
                  flow=[("Percent s", "slots filled in order"), ("format()", "slots filled by position"), ("Plus", "joins pieces, numbers need str"), ("All four", "print the same sentence")]),
    "case": dict(title="Changing the case", idea="The methods upper and lower return a copy of the string in capitals or small letters. The original string stays exactly as it was.",
                 reason="Users type text in any case. Changing the case lets a program compare text fairly.",
                 picture="upper and lower are a photocopier with a stamp: the original sheet stays as it was.",
                 flow=[("Original s", "Hello, world!"), ("s.upper()", "makes a new copy in capitals"), ("s.lower()", "makes a new copy in small letters"), ("s itself", "is unchanged")]),
    "chars": dict(title="Testing what a string is made of", idea="Methods such as isalpha, isalnum, isdecimal and isspace answer True or False for the whole string, not for one character.",
                  reason="Programs must check input before they trust it, for example that a PIN holds only digits.",
                  picture="These tests are a bouncer with a checklist: letters only? digits only? blanks only?",
                  flow=[("Take a string", "abc123"), ("Test every character", "is each one a letter? a digit?"), ("All must agree", "one failure makes it False"), ("Answer", "isalpha False, isalnum True")]),
    "casetests": dict(title="Testing upper, lower and title case", idea="isupper, islower and istitle ask how the letters are cased. Each needs at least one letter, and digits have no case.",
                      reason="Knowing the case tells a program whether text is shouted, whispered or written like a title.",
                      picture="isupper asks: is every letter shouting? istitle asks: does every word start like a book title?",
                      flow=[("Look at letters", "ignore digits and blanks"), ("isupper", "all letters capitals"), ("islower", "all letters small"), ("istitle", "each word starts with a capital")]),
    "affixes": dict(title="Start, end and affixes", idea="startswith and endswith test one edge of a string. removeprefix and removesuffix cut off exactly that text from the edge.",
                    reason="File names and messages are often recognised by their beginning or ending, such as .txt.",
                    picture="startswith is glancing at the greeting on a letter; endswith is checking the stamp on a parcel.",
                    flow=[("Name", "report.txt"), ("endswith('.txt')", "True"), ("removesuffix('.txt')", "cuts those four characters"), ("New string", "report")]),
    "joinsplit": dict(title="Joining and splitting", idea="split cuts a string into a list of pieces at a marker. join does the reverse and glues a list into one string.",
                      reason="Text arrives as one long string, but programs work on words and lines. Splitting and joining convert between the two.",
                      picture="split is a pair of scissors; join is a thread that ties the pieces together again.",
                      flow=[("One string", "My name is Simon"), ("split()", "cuts at every blank"), ("A list", "four words"), ("' '.join(list)", "ties them back into one string")]),
    "justify": dict(title="Justifying and centring text", idea="rjust, ljust and center pad a string with spaces, or with a fill character, until it reaches the width you give.",
                    reason="Columns of text only line up when every cell has the same width.",
                    picture="rjust, ljust and center move a book to the right, the left or the middle of a shelf.",
                    flow=[("Word", "Hello, 5 characters"), ("Width", "10 wanted"), ("rjust", "adds 5 spaces on the left"), ("Result", "10 characters wide")]),
    "strip": dict(title="Removing whitespace", idea="strip removes blanks, tabs and line breaks from both ends of a string. lstrip cuts the left end only, rstrip the right end only.",
                  reason="Text read from files and forms often carries stray blanks that break comparisons.",
                  picture="strip is trimming the white border off a photo print.",
                  flow=[("Padded text", "four blanks each side"), ("strip()", "cuts both borders"), ("lstrip / rstrip", "cut one border"), ("Lengths", "20, 12, 16, 16")]),
    "search": dict(title="Finding, counting and replacing", idea="find gives the index of the first match, or -1. count tallies the matches. replace returns a copy with the matches changed.",
                   reason="Searching inside text is the first step of almost every text task.",
                   picture="find is the finger that follows a line of text until it lands on the word.",
                   flow=[("Search text", "spam eggs spam"), ("find", "index of the first match"), ("count", "how many matches"), ("replace", "a new string, the old one stays")]),
    "codepoints": dict(title="Code points: ord() and chr()", idea="Every character has a number, its Unicode code point. ord turns a character into its number and chr turns a number back.",
                       reason="Computers store numbers, not letters. One shared table lets every program agree which number means which character.",
                       picture="A code point is a locker number: ord reads it from the name, chr opens the locker.",
                       flow=[("Character", "A"), ("ord('A')", "65"), ("Add one", "66"), ("chr(66)", "B")]),
    "encoding": dict(title="Characters are not bytes", idea="An encoding is the rule that turns code points into bytes for storage and travel. UTF-8 uses one to four bytes for each character.",
                     reason="Files and networks carry bytes, not characters. Both sides must use the same rule or the text breaks.",
                     picture="Encoding is a shipping box: text is packed into bytes to travel and unpacked to be read.",
                     flow=[("Text", "café, 4 characters"), ("encode('utf-8')", "packs each character"), ("Bytes", "5 bytes, the é takes two"), ("ASCII", "cannot hold é, so it becomes ?")]),
    "book_rjust": dict(title="Checking the book against the run", idea="A printed result in a book can be wrong for the Python you use. The only proof is to run the line and measure.",
                       reason="Programmers trust measured results, not memory. Checking a source also teaches you to report differences.",
                       picture="Re-running the book's lines is a second weighing on the shop scale.",
                       flow=[("The book prints", "14 and 9 spaces"), ("You run it", "Python 3 gives 15 and 8"), ("Compare", "the numbers differ by one"), ("Report", "say what you measured")]),
    "alternate": dict(title="Program: alternating case", idea="This program changes the case of each letter by its position. A function holds the rule, and enumerate supplies each position.",
                      reason="It shows how a loop, an index and a method work together on text.",
                      picture="It is a piano keyboard pattern: black key, white key, black key, white key.",
                      flow=[("Position i", "0, 1, 2, 3 and so on"), ("Even i", "letter goes lower"), ("Odd i", "letter goes upper"), ("join", "glues the letters back together")]),
    "piglatin": dict(title="Program: Pig Latin", idea="Pig Latin moves the opening consonants of a word to the end and adds ay. A word that starts with a vowel just gets yay.",
                     reason="It combines a search, slices and a join in one small program that you can predict by hand.",
                     picture="Pig Latin is a children's secret code: move the opening sounds to the back and add ay.",
                     flow=[("Word", "name"), ("cut", "finds the first vowel at index 1"), ("Slices", "ame plus n"), ("Add ay", "amenay")]),
    "tableprinter": dict(title="Practice program: table printer", idea="The table printer pads every cell to the width of its column. A column is as wide as its longest string.",
                         reason="Aligned columns are readable. The program shows how rjust, zip and a loop build a report.",
                         picture="A typesetter measures every column first, so all rows line up.",
                         flow=[("Columns", "three lists of strings"), ("Measure", "longest string per column"), ("zip(*table)", "turns columns into rows"), ("rjust", "pads each cell to its width")]),
    "clipboard": dict(title="Clipboard programs: paste, change, copy", idea="A clipboard program reads the text on the clipboard, changes it and puts it back. Here a list of one item stands in for the clipboard.",
                      reason="The same three steps automate many editing chores, such as adding a star to every line.",
                      picture="A clipboard is one shelf next to your desk: a new copy replaces whatever was there.",
                      flow=[("paste()", "read the text from the shelf"), ("split", "cut it into lines"), ("Change", "put a star in front of each"), ("copy()", "join and put it back")]),
}

# ---- speaker notes: 40 to 60 words, short sentences: what to tell, one example, one question (dividers and title 25 to 60)
NOTES = {
    "title": "Welcome. This chapter treats text as data you can cut, test, format and count. Every concept has an idea, an everyday picture, a drawn mechanism, the code and what the run printed. The same examples run on the chapter page.",
    "route": "Five parts, each a run of slides you can jump to. Every code example sits in the chapter-code tab of the page in this same order. Example: part three has seven examples about methods. Ask the class: which part do you expect to be hardest, and why?",
    "questions": "Two questions guide the chapter. Which operations make a new string and which only test it? Which printed results differ in current Python? Example: upper makes a new string, isalpha only answers. Ask the class to guess the answer to the first question now.",
    "divider1": "Part one. A literal is how you write text in code. An index and a slice read pieces of it. The in operator asks whether one text sits in another. Watch how the backslash changes meaning.",
    "divider2": "Part two. Formatting puts values into text. The f-string is the modern way; the older styles still appear in existing code. The text after a colon shapes the value.",
    "divider3": "Part three. Methods either make a new string, test the string, or cut it. None changes the original. Keep that rule in mind and the long method list becomes short.",
    "divider4": "Part four. Characters are numbers; bytes are how those numbers are stored. ord and chr switch between character and number. The encoding decides the byte count.",
    "divider5": "Part five. Three small programs and the clipboard idea. Each one uses only what parts one to four taught. Predict the output before you run it.",
    "A1": "Read each row aloud and let the class add a picture of their own. The point is that a string behaves like a fixed object: you read it and copy it, but never edit it in place. Example: the necklace. Question: what would a new necklace cost?",
    "A2": "A cinema row has numbered seats. The index names one seat; a slice names a block, and the stop seat is not included. The in operator is a yes or no search. Example: seat 4 of Hello is o. Question: which seat is last?",
    "A3": "Formatting is mail-merge. You write the pattern once and the blanks fill themselves from variables. The older styles fill blanks in order or by number. Example: a form letter with the name field. Question: what happens if a blank has no value?",
    "A4": "Case methods are a photocopier: the original page stays as it was, and you get a copy. The is-tests are a checklist that returns True or False for the whole string. Example: upper on hello. Question: does the original change?",
    "A5": "Split cuts, join ties. Start and end tests look at one edge only. Example: split a sentence into words, then join them with dashes. Ask the class which is-test fits a PIN, a book title and an empty line.",
    "A6": "Padding puts spaces around a word so columns line up. Strip removes the spaces again, from one end or from both. Example: a price list with right-aligned numbers. Ask the class where they have seen padded columns, for example on a receipt.",
    "A7": "Every character is a locker with a number. The encoding is the box used to ship that number. UTF-8 uses one to four boxes. Example: the letter A is locker 65. Ask the class how many boxes the euro sign needs.",
    "A8": "The clipboard is a one-slot shelf. Copy replaces what is there; paste only reads. A clipboard program reads the shelf, changes the text and puts it back. Example: adding a star to each line. Question: what would a second copy do?",
    "current": "Python moves on, and these features are newer than the book. Example: the debug specifier prints a name and its value, and template strings need Python 3.14. Ask the class which of these features they would use first, and which version of Python they have installed.",
    "summary": "Five sentences to keep. No string operation changes a string in place. The chart sorts the methods of this chapter by what they give back. Example: strip gives a new string, isalpha gives True or False. Ask: which method here would you use for a PIN check?",
    "practice": "Four drills. Predict first, then run on the chapter page. Example: reversing a split with a step of minus one. Ask each student to explain one answer in a single sentence to the neighbour, and then compare the explanations.",
    "resources": "Start with the book chapter, then the Python documentation. The stories link to first-hand sources and a video explains Unicode. Example: Rob Pike's own account of UTF-8. Ask the class to choose one link and read it before the next class.",
}
# code slides: (teach slide note, code slide note) per example
EX_NOTES = {
    "quotes": ("A literal is text between quotes in code. The two quote styles exist so one kind can hold the other. Example: Alice's cat in double quotes. Ask the class: how many characters does Bob's cat hold when typed with a backslash?",
               "Run the code and compare the two lengths. The backslash is typed but never stored. The prefix b makes bytes and the prefix r keeps text. Ask the class to predict each length before the run, then check the table."),
    "escapes": ("An escape sequence is two typed symbols that become one stored character. Example: backslash and t become one tab. Ask the class: how many characters does the typed pair backslash and n count in a plain string, and what in a raw one?",
                "Each escape in the table is one character long. Splitting on the new line cuts the text into two lines. Ask the class which escape they would need to print a path with a backslash, then run it."),
    "raw_multiline": ("A raw string keeps every backslash; triple quotes keep line breaks and both quote kinds. Example: a Windows path. Ask the class: why would a file path in a plain string go wrong with the folder name new?",
                      "Compare r and the plain literal in the picture: two characters against one. Then read the triple-quoted note, which needs no escapes. Ask the class to change the path to a folder starting with n and predict the length."),
    "index": ("An index is a position, counted from zero on the left and from minus one on the right. Example: Hello has H at index 0 and o at index 4. Ask the class: what index reaches the last letter without knowing the length?",
              "Point at the highlighted cells in the picture: index 0, 4 and minus 1. The last index is the length minus one. Ask the class to predict greeting at index 13 and then run it to see the error."),
    "slice": ("A slice cuts a run of characters; the stop index is not included. Example: zero to five of Hello, world gives Hello. Ask the class: what does leaving out both numbers give, and what does a step of minus one do?",
              "The picture marks the two slices in colour. Leaving a side empty runs to the edge, and a step of minus one reverses the text. Ask the class to write the slice that returns the word world."),
    "in_immutable": ("The in operator answers True or False. A string never changes in place, so every edit builds a new string. Example: Zophie a cat becomes Zophie the cat. Ask the class: why does the empty string count as inside every string?",
                     "Read the answer table row by row. The in test is case sensitive. The first line shows an edit made by slicing, not by changing the original. Ask the class which row surprised them most."),
    "fstring": ("An f-string runs the expression in each brace and pastes the answer. Example: the age plus ten inside the sentence. Ask the class: how would you print a literal brace inside an f-string, and why did we double it?",
                "Follow the arrows in the picture from each hole to its value. Even a sum works inside braces. Doubled braces print one brace. Ask the class to change the age and predict the new sentence before running."),
    "fspec": ("The text after the colon shapes the value: two decimals, a width, centred, a comma for thousands, hexadecimal. Example: 3.14159 with .2f shows 3.14. Ask the class: which specifier would you choose to print a price in a receipt?",
              "The table lists each specifier, its meaning and what it showed. The equals sign prints the name and the value, which is the quickest debugging aid. Ask the class to format their own phone number with a width of 12."),
    "older": ("The percent operator and the format method came before f-strings and you will meet them in old code. Example: the percent s slot fills in order. Ask the class: which of the four styles is easiest to read, and why?",
              "The table shows that all four styles give the same sentence. Notice that format uses numbered slots, so the order can change. Ask the class to rewrite one of the old lines as an f-string."),
    "case": ("upper and lower return a copy and leave the original alone. Example: Hello, world in capitals. Ask the class: if the original does not change, what must you write to keep the new version?",
             "The table shows each call and that s was unchanged after all of them. casefold goes further than lower. Ask the class to explain why comparing after lower ignores the case of both texts."),
    "chars": ("The is-tests answer for the whole string, so one failing character makes the answer False. Example: abc123 is alphanumeric but not alphabetic. Ask the class: which of these tests would you use to validate a PIN?",
              "Read the grid: green means True. Notice the lone blank passes only isspace. The empty string would fail every test. Ask the class to add a sixth sample and predict its row."),
    "casetests": ("isupper and islower need at least one letter, and digits have no case. Example: 123 is neither upper nor lower. Ask the class: why is Hello World a title but HELLO is not?",
                  "The grid shows which sample passes which test. Look at the digit row: all False. Ask the class to predict the row for the text Hello world with a small w and then run it."),
    "affixes": ("startswith and endswith test an edge; removeprefix and removesuffix cut exactly that text. Example: report.txt without .txt is report. Ask the class: how is removesuffix different from strip with the same letters?",
                "The picture shows the cut text in red and the kept text in teal. A tuple lets endswith accept several endings. Ask the class to cut the prefix test_ from three file names and print them."),
    "joinsplit": ("split cuts a string into a list; join glues a list into a string. Example: a sentence into four words. Ask the class: what does split do when you call it with no argument, and why is that useful?",
                  "The chart counts the pieces each call returned. Notice split on the letter m cuts inside words. partition cuts once and keeps the separator. Ask the class to join the words with a dash and predict the result."),
    "justify": ("rjust, ljust and center pad to a width, with an optional fill character. Example: Hello padded to ten characters. Ask the class: what happens when the width is smaller than the word, and why?",
                "Each row of the picture shows the letters in teal and the padding in grey. The bar after each line makes trailing spaces visible. Ask the class to centre their own name in thirty characters with a star as filler."),
    "strip": ("strip removes blanks at both ends; with an argument it removes any of those characters, not a word. Example: SpamSpamBacon with strip of ampS leaves Bacon. Ask the class: why does strip not remove the m in the middle?",
              "The chart shows the length before and after each call: twenty, twelve, sixteen and sixteen. The table says which border each call cuts. Ask the class to predict what strip of a single letter does to the word."),
    "search": ("find returns the index of the first match or minus one; count tallies matches; replace returns a copy. Example: spam appears twice in the sample. Ask the class: why does a start argument of one skip the first match?",
               "The picture highlights both matches and marks where find lands. replace with a limit of one changes only the first. Ask the class what find returns for a missing word, then run it to confirm."),
    "codepoints": ("Every character has a number called its code point. ord goes from character to number; chr goes back. Example: ord of A is 65. Ask the class: why is the code of a small a larger than a capital A by 32?",
                   "The chart plots the code point of each letter of Hello. The table shows ord and chr as a pair. Ask the class to compute the code of the letter Z by hand and then check it with ord."),
    "encoding": ("An encoding turns code points into bytes. In UTF-8 a character takes one to four bytes. Example: café is four characters but five bytes. Ask the class: why can ASCII not hold the letter é?",
                 "The chart counts the bytes of each character. The picture splits café into its bytes, with the two-byte é in amber. Ask the class which of the three sample characters costs the most bytes."),
    "book_rjust": ("A book can print a result that differs from the Python you run. The proof is to measure. Example: the padding added by rjust. Ask the class: when your run disagrees with a book, whom do you trust, and what do you do next?",
                   "The chart sets the book's figures next to the figures Python gave. The difference is one space in each case. Ask the class to explain how the code counts the padding instead of reading it by eye."),
    "alternate": ("This program changes the case by position. A function holds the rule; enumerate supplies each position. Example: the first letter has position zero, so it goes lower. Ask the class: which positions become capitals?",
                  "The picture shows each input letter, an arrow, and the output letter, with colour for upper and lower. Ask the class to change the rule so that odd positions go lower and predict the new output."),
    "piglatin": ("Pig Latin moves the opening consonants to the end and adds ay. A word that starts with a vowel just gets yay. Example: name becomes amenay. Ask the class: what does the function cut return for the word apple?",
                 "The table splits each word into its opening consonants and the rest, then shows the result. Ask the class to change the program so a word that starts with a vowel gets way instead of yay."),
    "tableprinter": ("A table is a list of columns. Each column is as wide as its longest string, and rjust pads each cell to that width. Example: the column of fruits is eight characters wide. Ask the class: why do we measure first?",
                     "The table shows the printed result and the chart shows the three column widths. Notice zip turns columns into rows. Ask the class to add a fourth column and predict what changes."),
    "clipboard": ("A clipboard program has three steps: paste, change, copy. Here a one-item list stands in for the clipboard so the program runs everywhere. Example: a star in front of each line. Ask the class: which step does pyperclip.copy replace?",
                  "The picture follows the text through five steps, from paste to copy. The printed result shows the starred lines. Ask the class to change the star into a dash and predict the new output."),
}


# ---- notes shorter than 40 words get one closing instruction, so that each note says what to tell, an example, a question and what to do with the picture
_PAD_T = [" Point at the drawing and read its four steps aloud, from left to right.", " Draw the four steps on the board, then compare them with the slide.", " Let one student retell the four steps in their own words."]
_PAD_C = [" Run the example on the chapter page and compare it with the picture.", " Change one value in the code, predict the new result, then run it.", " Ask a student to read the result picture aloud before you run it."]


def _pad(s, pads, k):
    return s if len(s.split()) >= 40 else s + pads[k % 3]


EX_NOTES = {k: (_pad(a, _PAD_T, i), _pad(b, _PAD_C, i)) for i, (k, (a, b)) in enumerate(EX_NOTES.items())}
NOTES = {k: (_pad(v, [" Ask a volunteer to answer before you click on."] * 3, 0) if not (k.startswith("div") or k == "title") else v) for k, v in NOTES.items()}
