#!/usr/bin/env python3
"""Builder of the item set A, version 2.1.0 (task TK4_Items_A3, brief BRIEF_TK4_Items_A3.md of the exam change of 2026-11-01).

Writes   items_a_v2_1_0.json               the paper list     14 records
         items_a_v2_1_0_makeup.json        the make-up list   14 records, no item shared with the paper list or with set B
         items_a_v2_1_0_provisional.json   side file: every record is provisional until the Owner's question styles arrive
Why a new version: v2_0_0 gave one chapter list per record without following the unit plan of the design v1_2_0, so the merged lists
failed rule E03 (units per chapter) and E09 (cross-chapter minimum). Here every record follows the plan unit by unit:
  - blank, cloze, match, order: `chapters` holds exactly one chapter per unit, in unit order (gap 1, 2, ..., premise 1..5, step 1..4);
  - one-unit choice records: the first chapter is the one the engine counts; only Q1f, Q3b, Q4b, Q5a and Q5b list two chapters
    (the five cross-chapter units of set A; set B brings Q3c, Q4c, Q5c and Q5d, together the nine of the design);
  - indirect forms only on Q4b, Q5a and Q5b (set B has Q4c, Q5c and Q5d: together the six of the design).
Good wording of v2_0_0 is reused where it fits the plan (Q1a to Q1f of the paper, Q1a to Q1e of the make-up, Q3b of the paper, Q5b of the
make-up); the other records are rewritten. v2_0_0 files are not touched. Every program that decides an answer is run here and the
printed result is compared with the answer; a mismatch stops the build.
Usage: python3 items_a_v2_1_0_make.py            (writes next to this file)
"""
import importlib.util, json, os, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("items_a_v2_0_0_make", os.path.join(HERE, "items_a_v2_0_0_make.py"))
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)                      # only reads the builder of v2_0_0 for its helpers and records; nothing is written
make, expect, fill = base.make, base.expect, base.fill
A, B, C = base.A, base.B, base.C
old1 = {r["id"]: r for r in base.L1}
old2 = {r["id"]: r for r in base.L2}


def reuse(rec, chapters, **change):
    """A record of v2_0_0 with new chapters (and optional changed fields); the rest of its wording stays."""
    r = json.loads(json.dumps(rec))
    r["chapters"] = chapters
    r.update(change)
    return r


L1, L2 = [], []

# =============================================================== LAYER 1 (the paper)
# ---- Q1: the plan of the design is already met by v2_0_0 (chapters 1, 2, 3, 4, 6 and 7 first with 3 as second chapter of Q1f)
for k in ("Q1a", "Q1b", "Q1c", "Q1d", "Q1e", "Q1f"):
    L1.append(reuse(old1[k], old1[k]["chapters"]))

# ---- Q2a: blank, four gaps, chapters 1 2 3 4 (gap 1 turns text into a number, gap 2 is the test, gap 3 loops, gap 4 hands back a result)
bank = ["int", "str", "<=", ">", "continue", "break", "total", "value"]
lst = ["def big_total(texts):", "    total = 0", "    for t in texts:", "        value = [[1]](t)", "        if value [[2]] 5:",
       "            [[3]]", "        total += value", "    return [[4]]", "", 'print(big_total(["4", "6", "10", "3"]))']
ans = [0, 2, 4, 6]
expect(fill(lst, bank, ans), "16")
L1.append(make("Q2a", [1, 2, 3, 4], [(A, 85), (A, 20), (A, 60), (A, 170)], 3, "blank",
    "Fill the four numbered gaps from the bank so that the function adds up only the texts whose number is above five.", lst,
    {"gaps": 4, "bank": bank}, ans, 16,
    "Gap 1: text from outside must become a number (ch 1); gap 2: the test skips the small ones (ch 2); gap 3: continue goes to the next pass without leaving the loop (ch 3); gap 4: only the returned total leaves the function (ch 4). 6 + 10 = 16.", "use",
    tip="Text typed by a user must become a number before it can be compared or added.", bank_id="L1-Q2a"))

# ---- Q2b: cloze, three gaps, chapters 5 6 8
bank = ["threshold", "changes", "copies", "changed", "printed", "counter", "hidden"]
ans = [0, 1, 3]
L1.append(make("Q2b", [5, 6, 8], [(B, 9), (C, 5), (C, 120)], 2, "cloze",
    "A log level is a [[1]] below which messages are dropped. The list method sort() [[2]] the list itself, but upper() builds a new string because strings are never [[3]].", [],
    {"gaps": 3, "bank": bank}, ans, 9,
    "Gap 1: the log level is a threshold (ch 5); gap 2: sort() changes the list itself (ch 6); gap 3: a string is never changed in place (ch 8).", "reason",
    bank_id="L1-Q2b"))

# ---- Q3a: match, five premises from chapters 1 to 5
prem = ["Turn the answer typed at a prompt into a number so that it can be added",
        "Run a block only when two conditions are both true",
        "Visit every key and value of a stock table, one pair at a time",
        "Give an optional argument a safe starting value that calls do not share",
        "Stop the program at once with a clear message when a caller passes an impossible age"]
tools = ["A global variable that every function changes", "int() applied to the answer", "A raise statement with a clear message",
         "A for loop over items()", "Deleting the line that fails", "Two tests joined with and", "A default of None that the body replaces with a fresh list"]
L1.append(make("Q3a", [1, 2, 3, 4, 5], [(A, 20), (A, 45), (A, 95), (A, 130), (B, 0)], 3, "match",
    "Match each situation to the tool that fits it best. Two of the seven tools fit none of the situations.", [],
    {"premises": prem, "answers": tools}, ["B", "F", "D", "G", "C"], 15,
    "int() makes the typed text a number (ch 1); and joins two tests (ch 2); a for loop over items() gives key and value (ch 3); a None default replaced in the body avoids a shared list (ch 4); raise refuses a call the function cannot serve (ch 5).", "use",
    width=90))

# ---- Q3b: mcq on a reason, chapter 7 first (stands for Q3f)
L1.append(reuse(old1["Q3b"], [7, 6]))

# ---- Q4a: order, four steps from chapters 3 5 6 7 (printed order = unit order)
steps = ["Loop over the pairs of day and reading", "Log the finished table at level DEBUG so the run leaves evidence",
         "Append each reading to the list stored under its day", "Create an empty dictionary that will map each day to a list of readings"]
L1.append(make("Q4a", [3, 5, 6, 7], [(A, 95), (B, 14), (C, 5), (C, 60)], 3, "order",
    "Put the four steps of a program that groups daily readings into one table in the order in which they must run.", [],
    steps, [2, 4, 3, 1], 16,
    "The dictionary comes first (1, ch 7), then the loop starts (2, ch 3), the append sits inside the loop (3, ch 6) and the log line comes after the loop (4, ch 5); the answer gives the place of each printed step.", "use",
    tip="A dictionary stores values under keys and finds each one again by its key.", terms=["dictionary"]))

# ---- Q4b: mcq on a consequence, chapter 8 first (stands for Q4e), indirect
code = ['name = "ada lovelace"', "for part in name.split():", "    part.capitalize()", "print(name)"]
expect("\n".join(code), "ada lovelace")
changed = 'name = "ada lovelace"\nwords = []\nfor part in name.split():\n    words.append(part.capitalize())\nprint(" ".join(words))'
expect(changed, "Ada Lovelace")
L1.append(make("Q4b", [8, 6], [(C, 105), (C, 115)], 4, "mcq",
    "The program prints ada lovelace unchanged. What changes if the loop appends each part.capitalize() to a list, and the joined list is printed?", code,
    ["It prints Ada Lovelace: each call hands back a new string, and now the results are kept",
     "It prints ada lovelace: capitalize cannot work on the pieces made by split",
     "It prints Ada Lovelace: capitalize changed name in place before, and joining only shows it",
     "It prints Ada lovelace: capitalize changes only the first letter of the whole text"], "A", 4,
    "A string method never changes the string it is called on; it hands back a new one, so the result must be kept, here in a list, before join builds one text.", "effect", indirect="consequence",
    tip="A string method hands back a new string and leaves the old one as it was."))

# ---- Q5a: mcq, chapter 1 first, indirect
code = ["total = 0.1 + 0.2", "print(total == 0.3, round(total, 1) == 0.3)"]
expect("\n".join(code), "False True")
L1.append(make("Q5a", [1, 2], [(A, 0), (A, 25)], 4, "mcq",
    "Read the program, then choose what it prints and what that shows about comparing calculated decimal numbers.", code,
    ["True True: both tests hold because 0.1 + 0.2 is exactly 0.3",
     "False False: round cannot change a value that is already stored",
     "False True: the sum is stored slightly off, so only the rounded value equals 0.3",
     "True False: round changes the value so that the first test no longer holds"], "C", 3,
    "0.1 + 0.2 is stored as a close approximation, so == against 0.3 is False; round(total, 1) gives 0.3, so that test is True.", "effect", indirect="consequence",
    tip="Many decimal fractions are stored as close approximations, not exactly."))

# ---- Q5b: mcq on a reason, chapter 2 first, indirect
code = ["for data in ([], [0]):", "    if data:", '        print("run", data)']
expect("\n".join(code), "run [0]")
L1.append(make("Q5b", [2, 6], [(A, 50), (C, 0)], 4, "mcq",
    "Only one of the two lists makes the program print. Which reason explains this?", code,
    ["An empty list counts as false, while a list holding anything, even a 0, counts as true",
     "The number 0 counts as false, so the list [0] is skipped and the empty list is the one printed",
     "The test compares the length with zero, and both lists have the same length",
     "Lists always count as true, so the loop prints twice and the output is cut"], "A", 3,
    "An empty container counts as false; a list that holds anything, even the number 0, counts as true, so only [0] runs the block.", "reason", indirect="reason"))

# =============================================================== LAYER 2 (the make-up)
for k in ("Q1a", "Q1b", "Q1c", "Q1d", "Q1e"):
    L2.append(reuse(old2[k], old2[k]["chapters"]))

# ---- Q1f: chapter 7 first (the strip record of v2_0_0 is chapter 8 and moves to Q4b)
code = ['slots = dict.fromkeys(["a", "b"], [])', 'slots["a"].append(1)', "print(slots)"]
expect("\n".join(code), "{'a': [1], 'b': [1]}")
L2.append(make("Q1f", [7, 6], [(C, 80), (C, 15)], 4, "mcq",
    "Read the program, then choose the line it prints, thinking about how many lists fromkeys really makes for the two keys.", code,
    ["{'a': [1], 'b': []}: only the list under a receives the item",
     "{'a': [1], 'b': [1]}: both keys hold the very same list, so the item shows twice",
     "{'a': [], 'b': []}: append works on a copy of the list",
     "An error: fromkeys cannot take a list as a value"], "B", 5,
    "dict.fromkeys hands every key the one list it was given, so appending through key a shows under key b as well.", "effect"))

# ---- Q2a: blank, chapters 1 2 3 4
bank = ["%", "//", "==", "=", "break", "continue", "found", "n"]
lst = ["def has_even(numbers):", "    found = False", "    for n in numbers:", "        if n [[1]] 2 [[2]] 0:", "            found = True",
       "            [[3]]", "    return [[4]]", "", "print(has_even([3, 7, 8, 5]))"]
ans = [0, 2, 4, 6]
expect(fill(lst, bank, ans), "True")
L2.append(make("Q2a", [1, 2, 3, 4], [(A, 6), (A, 40), (A, 85), (A, 170)], 3, "blank",
    "Fill the four numbered gaps from the bank so that the function stops looking at the first even number and reports True.", lst,
    {"gaps": 4, "bank": bank}, ans, 16,
    "Gap 1: % gives the remainder of the division by 2 (ch 1); gap 2: == compares the remainder with 0 (ch 2); gap 3: break leaves the loop at the first even number (ch 3); gap 4: found is the result that leaves the function (ch 4).", "use",
    tip="An even number leaves remainder zero when divided by two.", bank_id="L2-Q2a"))

# ---- Q2b: cloze, chapters 5 6 8
bank = ["programmer", "user", "name", "copy", "new", "old", "guard"]
ans = [0, 2, 4]
L2.append(make("Q2b", [5, 6, 8], [(B, 4), (C, 15), (C, 120)], 2, "cloze",
    "An assert checks the mistakes of the [[1]], and optimised mode can remove it. After b = a, b is a second [[2]] of one list, but upper() gives a [[3]] string.", [],
    {"gaps": 3, "bank": bank}, ans, 9,
    "Gap 1: asserts are for the programmer's mistakes and can be removed (ch 5); gap 2: assigning a list adds a name, not a list (ch 6); gap 3: a string method gives a new string (ch 8).", "reason",
    bank_id="L2-Q2b"))

# ---- Q3a: match, chapters 1 to 5
prem = ["Split 20 sweets into boxes of 6 and learn how many full boxes there are",
        "A narrow case must be tested before the broad case that would also fit it",
        "Keep asking until the player types the right password",
        "Share a value between two functions without a global variable",
        "Stop on a chosen line and look at the variables one step at a time"]
tools = ["A while loop that tests each answer", "A recursive function with no base case", "The // operator that rounds the division down",
         "An if, elif, else ladder with the narrow test first", "Passing it as an argument and sending results back with return",
         "Stopping at a chosen line and stepping from there", "A global variable shared by all functions"]
L2.append(make("Q3a", [1, 2, 3, 4, 5], [(A, 6), (A, 60), (A, 96), (A, 170), (B, 19)], 3, "match",
    "Choose for each situation the answer that suits it best. Two of the seven answers suit none of the situations.", [],
    {"premises": prem, "answers": tools}, ["C", "D", "A", "E", "F"], 15,
    "// rounds down and counts full boxes (ch 1); the narrow test goes first in a ladder (ch 2); while repeats until the test fails (ch 3); information moves through parameters and return (ch 4); stepping from a chosen line shows the variables (ch 5).", "use",
    width=90))

# ---- Q3b: mcq on a reason, chapter 7 first
L2.append(make("Q3b", [7, 1], [(C, 50), (A, 10)], 4, "mcq",
    "A program stores table[1] = 'a', then table[1.0] = 'b', then table[True] = 'c'. Why does the table end with one key holding c?", [],
    ["The numbers 1, 1.0 and True are equal and look alike to the table, so they are one key and the last value replaces the earlier ones",
     "A key of another type is refused silently, so the first value stays and the others are dropped",
     "Floats and truth values are turned into text first, so all three keys become the same text",
     "A key may be used only once per line of the program, so a new line replaces the old key"], "A", 5,
    "1, 1.0 and True are equal and hash alike, so they are one key, and each assignment replaces the value of the one before.", "reason"))

# ---- Q4a: order, chapters 3 5 6 7 (printed order = unit order)
steps = ["Loop over the names in the order",
         "Inside the loop, raise an error with a clear message when a name is not a key of the stock",
         "Once every name has passed, append the word ready to the order list",
         "Build the stock dictionary with each item name as the key"]
L2.append(make("Q4a", [3, 5, 6, 7], [(A, 95), (B, 0), (C, 5), (C, 60)], 3, "order",
    "Put the four steps of a program that checks an order against the stock in the order in which they must run.", [],
    steps, [2, 3, 4, 1], 16,
    "The stock table is built first (1, ch 7), the loop starts (2, ch 3), the check raises inside the loop (3, ch 5) and ready is appended once all names passed (4, ch 6); the answer gives the place of each printed step.", "use",
    tip="A dictionary stores values under keys and finds each one again by its key.", terms=["dictionary"]))

# ---- Q4b: chapter 8 first, indirect (the strip record of v2_0_0, now asking what a change does)
code = ['for word in ["banana", "bob", "cab"]:', '    print(word.strip("ab"), end=" ")']
expect("\n".join(code), "nan o c")
expect('for word in ["banana", "bob", "cab"]:\n    print(word.removeprefix("ba"), end=" ")', "nana bob cab")
L2.append(make("Q4b", [8, 3], [(C, 105), (C, 102)], 4, "mcq",
    "This loop prints nan o c. What would change if strip(\"ab\") were replaced by removeprefix(\"ba\")?", code,
    ["It would print nana bob cab: removeprefix cuts the exact text ba once, and only from the front",
     "It would still print nan o c: both methods remove the same letters",
     "It would print nana ob cab: removeprefix removes any of the letters from the front only",
     "It would stop with an error: removeprefix cannot be used inside a loop"], "A", 4,
    "strip with letters removes any of them from both ends; removeprefix cuts one exact text from the front, and only if the word starts with it.", "effect", indirect="consequence"))

# ---- Q5a: chapter 1 first, indirect, effect
code = ['a = input("a? ")', 'b = input("b? ")', 'c = input("c? ")', "print(a + b + c)"]
expect("\n".join(code), "a? b? c? 5342", stdin="5\n3\n42\n")
fixed = 'a = int(input("a? "))\nb = int(input("b? "))\nc = int(input("c? "))\nprint(a + b + c)'
expect(fixed, "a? b? c? 50", stdin="5\n3\n42\n")
L2.append(make("Q5a", [1, 5], [(B, 16), (A, 20)], 4, "mcq",
    "Typing 5, 3 and 42 at the prompts shows 5342. What would the program print if each of the three input calls were wrapped in int()?", code,
    ["50: each answer would become a number, so + would add them",
     "5342: the digits would still be glued because int() changes nothing",
     "An error: int() cannot be used on the answer of input",
     "5 3 42: print would show the three answers separated by spaces"], "A", 3,
    "input() always returns text and + on text glues characters; int() on each answer makes + add, so 5 + 3 + 42 is 50.", "effect", indirect="consequence"))

# ---- Q5b: chapter 2 first, indirect, reason
L2.append(reuse(old2["Q5b"], [2, 7], bloom=4))

# ---------------------------------------------------------------- write
def dump(path, obj):
    with open(os.path.join(HERE, path), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")

if __name__ == "__main__":
    dump("items_a_v2_1_0.json", L1)
    dump("items_a_v2_1_0_makeup.json", L2)
    dump("items_a_v2_1_0_provisional.json", {
        "set": "A", "version": "2.1.0", "task": "TK4_Items_A3",
        "provisional": True,
        "reason": "The Owner will send question styles that may change the formats; every record below is provisional until then.",
        "records": [{"file": f, "id": it["id"], "provisional": True} for f, L in (("items_a_v2_1_0.json", L1), ("items_a_v2_1_0_makeup.json", L2)) for it in L]})
    print("wrote", len(L1), "and", len(L2), "records; every decisive program run and matched")
