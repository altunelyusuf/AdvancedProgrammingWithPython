#!/usr/bin/env python3
"""Builder of the item set A, version 2.0.0 (task TK4_Items_A2).

Writes   items_a_v2_0_0.json          layer 1 (the paper)    14 records
         items_a_v2_0_0_makeup.json   layer 2 (the make-up)  14 records, no item shared with layer 1
         items_a_v2_0_0_provisional.json   side file: every record is provisional until the Owner's question styles arrive
Why two files: the validator exam_item_check_v1_1_0.py makes the id equal to question plus sub (R23) and the id unique in a list (R02),
so one list holds at most one record per place Q1a to Q5g. A paper and a make-up with no item in both therefore need two lists.
One record is one sub-question (brief r11): a match record has 5 premises and 7 answers, an order record 4 steps, a blank or cloze
record all its gaps; the points belong to the whole record.
Every program that decides an answer is run here and the printed result is compared with the answer; a mismatch stops the build.
Usage: python3 items_a_v2_0_0_make.py            (writes next to this file)
"""
import json, os, re, subprocess, sys, tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
EXAMS = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(EXAMS, "..", ".."))
CP_FILES = {"ch01_04": "critical_points_ch01_04_v1_0_0.json", "ch05": "critical_points_ch05_v1_0_0.json", "ch06_08": "critical_points_ch06_08_v1_0_0.json"}
_cp = {k: json.load(open(os.path.join(EXAMS, v), encoding="utf-8")) for k, v in CP_FILES.items()}


def run(code, stdin=""):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "p.py")
        open(f, "w", encoding="utf-8").write(code)
        p = subprocess.run([sys.executable, "-I", f], cwd=d, capture_output=True, text=True, timeout=10, input=stdin)
    return p.returncode, p.stdout, p.stderr


def expect(code, out=None, err=None, stdin=""):
    rc, so, se = run(code, stdin)
    if err is not None:
        assert rc != 0 and err in se, ("expected error", err, se)
    else:
        assert rc == 0 and " ".join(so.split()) == out, ("expected", out, "got", so, se)


def make(qid, ch, cps, bloom, typ, stem, listing, options, answer, points, reason, asks, tip="none", terms=(), indirect="none",
         width=45, bank_id="none"):
    """cps: list of (cp file key, index); the first one gives critical_point; the sources come from the cited points."""
    source, course_point = [], []
    for key, n in cps:
        p = _cp[key][n]
        course_point.append("%s#%d" % (CP_FILES[key], n))
        s = p["source_file"] + ("#slide %d" % p["place"] if p.get("evidence_kind") in ("slide", "speaker_note") else "")
        if s not in source:
            source.append(s)
    source.append("04-assessment/exams/" + CP_FILES[cps[0][0]])
    return {"id": qid, "chapters": ch, "source": source, "bloom": bloom, "critical_point": _cp[cps[0][0]][cps[0][1]]["point"],
            "course_point": course_point, "seed_item": "none", "type": typ, "stem": stem, "listing": listing,
            "options_or_blanks": options, "answer": answer, "points": points, "reason": reason, "indirect_form": indirect,
            "code_width": width, "bank_id": bank_id, "question": qid[:2], "sub": qid[2], "tip": tip, "terms": list(terms), "asks": asks}


def fill(listing, bank, ans):
    text = "\n".join(listing)
    for i, a in enumerate(ans, 1):
        text = text.replace("[[%d]]" % i, bank[a])
    return text


A, B, C = "ch01_04", "ch05", "ch06_08"
L1, L2 = [], []

# =============================================================== LAYER 1 (the paper)
# ---- Q1
code = ["a = 7", "b = -2", "print(a // b, a % b)"]
expect("\n".join(code), "-4 -1")
L1.append(make("Q1a", [1], [(A, 6), (A, 7)], 3, "predict",
    "Read the program below, then choose exactly what it prints when it runs from the first line to the last.", code,
    ["-3 1", "-4 -1", "-3 -1", "-4 1"], "B", 4,
    "7 // -2 rounds down to -4, and the remainder is 7 - (-2 * -4) = -1; quotient times divisor plus remainder gives 7 back.", "effect",
    tip="Division with // rounds down, not toward zero; check with quotient times divisor plus remainder."))

code = ["count = 0", 'label = count or "none"', 'other = count and "some"', "print(label, other)"]
expect("\n".join(code), "none 0")
L1.append(make("Q1b", [2], [(A, 47), (A, 50)], 3, "predict",
    "Read the program below, then choose exactly what it prints. Think about which operand each operator hands back.", code,
    ["none 0", "none some", "0 some", "none False"], "A", 4,
    "Zero is false, so 'count or none' hands back the second operand 'none'; 'count and some' stops at the false first operand and hands back 0.", "effect",
    tip="Zero counts as false; and, or hand back one of their operands, not only True or False."))

code = ["total = 0", "for n in range(1, 6):", "    if n % 2 == 0:", "        continue", "    total += n", "print(total, n)"]
expect("\n".join(code), "9 5")
L1.append(make("Q1c", [3], [(A, 87), (A, 85)], 3, "predict",
    "Read the program below, then choose exactly what it prints, including the last value the loop variable holds.", code,
    ["6 5", "9 6", "9 5", "15 5"], "C", 4,
    "continue skips the even numbers, so total is 1 + 3 + 5 = 9; after the loop n keeps its last value 5, not 6.", "effect"))

code = ["def add(item, bag=[]):", "    bag.append(item)", "    return bag", "", 'add("a")', 'print(add("b"))']
expect("\n".join(code), "['a', 'b']")
L1.append(make("Q1d", [4], [(A, 130), (A, 131)], 4, "mcq",
    "Read the program, then choose the statement that correctly says what the last line prints and the reason for it.", code,
    ["['b']: each call starts with its own new empty list for bag",
     "['a']: the second call is refused because bag already holds an item",
     "['a', 'b']: the empty list is made once, when def runs, and every call shares it",
     "['a', 'b']: the first call's result is stored by the caller and reused"], "C", 4,
    "A default value is made once, when def runs, so both calls append to the same list; the safe habit is a default of None.", "effect",
    tip="Ask when the default list is created: at the def line, or again at each call?"))

code = ["a = [1, 2, 3]", "b = a", "c = a[:]", "b.append(4)", "print(len(a), len(c))"]
expect("\n".join(code), "4 3")
L1.append(make("Q1e", [6], [(C, 15), (C, 2)], 4, "mcq",
    "After this program runs, which statement correctly says what it prints and why the two lengths differ?", code,
    ["3 3: append works on a private copy, so no list changes",
     "4 4: the copy keeps a link, so c grows along with a",
     "4 3: b is a second name for the list of a, but c was copied",
     "3 4: b got its own list and c shares the list of a"], "C", 4,
    "b = a adds a second name for one list, so append through b changes a; a[:] builds a new list that stays at 3 items.", "effect",
    tip="A name is a tag on a list; assigning one name to another adds a tag, not a list."))

code = ["stock = {'pen': 2, 'ink': 0}", "for item in ['pen', 'cap', 'pen']:", "    stock[item] = stock.get(item, 0) + 1", "print(stock)"]
expect("\n".join(code), "{'pen': 4, 'ink': 0, 'cap': 1}")
L1.append(make("Q1f", [7, 3], [(C, 66), (C, 51)], 4, "mcq",
    "Read the program, then choose the line it prints, thinking about what get() hands back for a name not yet in the table.", code,
    ["{'pen': 3, 'ink': 0, 'cap': 1}", "{'pen': 4, 'ink': 1, 'cap': 1}", "{'pen': 4, 'ink': 0, 'cap': 1}", "{'pen': 2, 'ink': 0, 'cap': 1}"], "C", 5,
    "pen is seen twice (2 + 2 = 4), cap is new so get() gives 0 and it becomes 1, and ink is never visited.", "effect",
    tip="get(key, 0) hands back 0 instead of stopping with an error when the key is missing."))

# ---- Q2
bank = ["total", "<", "0", "+=", "1", "price", "=", ">"]
lst = ["prices = [4, 6, 10, 3]", "total = [[1]]", "for price in prices:", "    if price [[2]] 5:", "        total [[3]] price", 'print("big total:", [[4]])']
ans = [2, 7, 3, 0]
expect(fill(lst, bank, ans), "big total: 16")
L1.append(make("Q2a", [3], [(A, 80), (A, 81)], 3, "blank",
    "Fill the four numbered gaps from the bank so that the program adds up only the prices above five and prints that total.", lst,
    {"gaps": 4, "bank": bank}, ans, 16,
    "The accumulator starts at 0 before the loop, the test is price > 5, += collects at each pass and the final print shows total: 6 + 10 = 16.", "use",
    tip="An accumulator is a variable that starts at a neutral value before the loop and collects at every pass.", bank_id="L1-Q2a"))

bank = ["user", "programmer", "remove", "add", "guard", "message", "speed"]
ans = [1, 2, 4]
L1.append(make("Q2b", [5], [(B, 4), (B, 6)], 2, "cloze",
    "An assert is meant for mistakes of the [[1]]. Because Python can [[2]] every assert when started in optimised mode, an assert must never be the only [[3]] against bad user input.", [],
    {"gaps": 3, "bank": bank}, ans, 9,
    "Errors of the user are raised, errors of the programmer are asserted; python -O removes every assert, so it cannot be the only guard.", "reason",
    tip="An assert line checks a fact about the program itself and stays silent while the fact holds.", bank_id="L1-Q2b"))

# ---- Q3
prem = ["Print every item of a shopping list together with its number, counting from 1",
        "Combine a list of names with a list of scores, one pair at a time",
        "Keep asking until the player types the right password",
        "Find the price of a product quickly from its name",
        "Save the stock table in a text form that other programs can also read"]
tools = ["A while loop that tests each answer", "A recursive function with no base case", "enumerate with a start value of 1",
         "A mapping from each product name to its price", "zip over the two lists", "A global variable shared by all functions",
         "Text in JavaScript Object Notation (JSON) made with json.dumps"]
L1.append(make("Q3a", [3, 7], [(A, 96), (C, 68)], 3, "match",
    "Match each situation to the tool that fits it best. Two of the seven tools fit none of the situations.", [],
    {"premises": prem, "answers": tools}, ["C", "E", "A", "D", "G"], 15,
    "enumerate(items, 1) numbers from 1; zip pairs two lists; while repeats until the test fails; a mapping finds a value by key; json.dumps writes a dictionary as text.", "use",
    tip="enumerate gives each item with a counter; zip walks several lists side by side.", terms=["enumerate"], width=45))

L1.append(make("Q3b", [6, 7], [(C, 49)], 4, "mcq",
    "A programmer wants the pair (2, 3) as a key in a dictionary, but a list [2, 3] is refused. Which reason explains this?", [],
    ["A list is too long to be stored, while a pair always fits",
     "Keys must be numbers, and a list is not a number",
     "A list may change later, so its fingerprint could change and the stored pair would be lost",
     "A list cannot be compared, so no key can ever be found"], "C", 5,
    "A key must be hashable: its fingerprint must never change, so a pair is accepted and a list is refused with a TypeError.", "reason",
    tip="A dictionary stores values under keys and finds each one again from a fingerprint of the key.", terms=["dictionary"]))

# ---- Q4
steps = ["Return the total once the loop has ended", "Set the total to zero before anything is added",
         "Add the current price to the total inside the block", "Start a for loop that visits each price"]
L1.append(make("Q4a", [3, 4], [(A, 80), (A, 129)], 3, "order",
    "Put the four steps of a function that adds up a list of prices in the order in which they must run.", [],
    steps, [4, 1, 3, 2], 16,
    "Order: set to zero (1), start the loop (2), add inside the block (3), return after the loop (4); the answer gives the place of each printed step.", "use",
    tip="Think of a till roll: start at zero, add each price as it comes, show the sum at the end."))

code = ["def read_all(texts):", "    out = []", "    for t in texts:", "        try:", "            out.append(int(t))", "        except ValueError:",
        "            pass", "    return out", "", 'print(read_all(["4", "x", "7"]))']
expect("\n".join(code), "[4, 7]")
changed = "\n".join(code).replace("    for t in texts:\n        try:\n            out.append(int(t))\n        except ValueError:\n            pass",
                                    "    try:\n        for t in texts:\n            out.append(int(t))\n    except ValueError:\n        pass")
expect(changed, "[4]")
L1.append(make("Q4b", [4], [(A, 153), (A, 154)], 4, "mcq",
    "The try sits inside the loop. What changes in the result if the whole loop is moved inside one try instead?", code,
    ["Nothing changes: the result is still [4, 7]",
     "The result is [7]: the loop restarts after the bad text",
     "The result is [4, 7, 'x']: the bad text is kept as text",
     "The result is [4]: the first bad text ends the loop, so 7 is never read"], "D", 4,
    "With the try around the loop, the first failing int() jumps out of the loop to the except, so later texts are skipped.", "effect", indirect="consequence"))

# ---- Q5
code = ["def tidy(names):", "    names.sort()", "", 'team = ["Zoe", "Ali"]', "tidy(team)", "print(team)"]
expect("\n".join(code), "['Ali', 'Zoe']")
L1.append(make("Q5a", [4, 6], [(C, 16), (C, 18)], 4, "mcq",
    "After this program runs, what does the last line print, and what reason explains it?", code,
    ["['Zoe', 'Ali']: the function received a private copy of the list",
     "None: sort returns None and replaces the list",
     "An error: a function may not change a list from outside",
     "['Ali', 'Zoe']: the function received the list itself and sort changed it in place"], "D", 3,
    "A function receives the caller's list itself, and sort() changes a list in place, so the caller sees the sorted list.", "effect", indirect="consequence"))

L1.append(make("Q5b", [6, 8], [(C, 121), (C, 9)], 4, "mcq",
    "A learner writes name.upper() alone on one line and name stays the same, yet team.sort() changes team. What best explains the difference?", [],
    ["A string cannot be changed in place, so upper() builds a new string, while a list can be changed in place",
     "upper() works only inside print, while sort() works anywhere in the program",
     "Strings are copied at every use, while lists are never copied by Python",
     "upper() is a slow method, so Python delays its effect until the program ends"], "A", 3,
    "Strings never change, so upper() returns a new string that must be kept; sort() changes the list itself and returns None.", "reason", indirect="reason"))

# =============================================================== LAYER 2 (the make-up)
code = ['a = "5"', "b = 3", "print(a * b, int(a) * b)"]
expect("\n".join(code), "555 15")
L2.append(make("Q1a", [1], [(A, 23), (A, 15)], 3, "predict",
    "Read the program below, then choose exactly what it prints, watching the difference between the text 5 and the number 5.", code,
    ["15 15", "555 15", "555 555", "8 15"], "B", 4,
    "A text times 3 repeats the text (555); int(a) turns it into the number 5, and 5 * 3 is 15.", "effect",
    tip="Text times a whole number repeats the text; a number times a number multiplies."))

code = ["score = 85", "if score >= 60:", '    grade = "pass"', "elif score >= 80:", '    grade = "merit"', "else:", '    grade = "fail"', "print(grade)"]
expect("\n".join(code), "pass")
L2.append(make("Q1b", [2], [(A, 60), (A, 59)], 3, "predict",
    "Read the program below, then choose what it prints. Consider which test the score meets first.", code,
    ["merit", "pass", "fail", "pass merit"], "B", 4,
    "The ladder stops at the first true test; 85 >= 60 is true, so the narrower test below it is never reached.", "effect",
    tip="In a ladder of tests only the first rung whose test is true runs."))

code = ["found = False", "for n in range(2, 7):", "    if 7 % n == 0:", "        found = True", "        break", "else:", '    print("prime", end=" ")', "print(found)"]
expect("\n".join(code), "prime False")
L2.append(make("Q1c", [3], [(A, 103), (A, 104)], 3, "predict",
    "Read the program below, then choose exactly what it prints. Pay attention to when the else belonging to the loop runs.", code,
    ["prime True", "False", "prime False", "True"], "C", 4,
    "No n from 2 to 6 divides 7, so break never happens; the loop's else then prints prime, and found is still False.", "effect",
    tip="Decide first whether break ever happens, then decide whether the loop's else runs."))

code = ["count = 0", "", "def bump():", "    count = count + 1", "    return count", "", "print(bump())"]
expect("\n".join(code), None, err="UnboundLocalError")
L2.append(make("Q1d", [4], [(A, 145), (A, 139)], 4, "mcq",
    "Read the program, then choose the statement that says what happens when it runs and why.", code,
    ["It prints 1: the function reads the global count and adds one",
     "It prints 0: the function works on a copy of count",
     "It stops with an error: count is local inside bump, so it is read before it has a value",
     "It prints 1 and also changes the global count to 1"], "C", 4,
    "An assignment anywhere in a function makes the name local everywhere in it, so reading count before the assignment fails.", "effect",
    tip="Python decides whether a name is local by looking for an assignment anywhere in the body."))

code = ["nums = [1, 2, 2, 3]", "for n in nums:", "    if n == 2:", "        nums.remove(n)", "print(nums)"]
expect("\n".join(code), "[1, 2, 3]")
L2.append(make("Q1e", [6], [(C, 12)], 4, "mcq",
    "Read the program, then choose the line that says what it prints and why the result looks as it does.", code,
    ["[1, 3]: every 2 is found and removed",
     "[1, 2, 3]: after a removal the next item shifts left and the loop skips it",
     "[1, 2, 2, 3]: remove does nothing while a loop is running",
     "An error: a list may not change while a loop reads it"], "B", 4,
    "Removing the first 2 shifts the second 2 into the position already visited, so it is skipped and stays in the list.", "effect"))

code = ['text = "banana"', 'one = text.strip("ab")', 'two = text.removeprefix("ban")', "print(one, two)"]
expect("\n".join(code), "nan ana")
L2.append(make("Q1f", [8], [(C, 105), (C, 102)], 4, "mcq",
    "Read the program, then choose the pair of results it prints, thinking about what strip does with the letters it is given.", code,
    ["anana ana: strip removes only the first letter given",
     "banana ana: strip with letters does nothing unless the whole word matches",
     "nan nana: removeprefix removes any of the letters it is given",
     "nan ana: strip removes any of the letters from both ends, removeprefix cuts the exact text once"], "D", 5,
    "strip('ab') removes any a or b from both ends, leaving nan; removeprefix('ban') cuts that exact text once, leaving ana.", "effect",
    tip="strip with an argument removes a set of characters, not a word."))

bank = ["None", "is", "not", "[]", "bag", "item", "0", "append"]
lst = ["def collect(item, bag=[[1]]):", "    if bag [[2]] None:", "        bag = [[3]]", "    bag.append(item)", "    return [[4]]", "", 'print(collect("a"), collect("b"))']
ans = [0, 1, 3, 4]
expect(fill(lst, bank, ans), "['a'] ['b']")
L2.append(make("Q2a", [4], [(A, 130), (A, 131)], 3, "blank",
    "Fill the four numbered gaps from the bank so that every call without a list starts with its own fresh list.", lst,
    {"gaps": 4, "bank": bank}, ans, 16,
    "The default is None, tested with is; a fresh [] is made inside the body at each call and returned, so the two calls do not share a list.", "use",
    tip="A safe default is a marker that the body replaces with a fresh list at each call.", bank_id="L2-Q2a"))

bank = ["old", "changed", "deleted", "new", "hidden", "kept", "shared"]
ans = [3, 1, 5]
L2.append(make("Q2b", [8], [(C, 98), (C, 121)], 2, "cloze",
    "A string method such as upper() hands back a [[1]] string, because a string can never be [[2]] in place, so the result must be [[3]] or printed.", [],
    {"gaps": 3, "bank": bank}, ans, 9,
    "Strings never change, so a method returns a new string; the original stays as it was unless the result is kept or printed.", "reason",
    tip="Calling upper() alone leaves the original text as it was.", bank_id="L2-Q2b"))

prem = ["A caller passes a negative age that it could easily correct",
        "A total inside the program must never be negative, whatever the input",
        "Evidence of what ran must survive after the program has finished",
        "You want to pause on line 12 and inspect the variables one step at a time",
        "One bad value in a list must not stop the other values from being processed"]
tools = ["An assert statement placed after the calculation", "A raise statement with a clear message", "Pausing at a breakpoint in an integrated development environment (IDE) and stepping",
         "A global flag that every function sets", "A try and except placed inside the loop around the one risky call", "Log messages written to a file",
         "Deleting the line that fails"]
L2.append(make("Q3a", [4, 5], [(B, 21), (A, 153)], 3, "match",
    "Match each situation to the instrument that fits it best. Two of the seven instruments fit none of the situations.", [],
    {"premises": prem, "answers": tools}, ["B", "A", "F", "C", "E"], 15,
    "raise for what the caller can fix, assert for what must always be true, a log file for evidence, a breakpoint for stepping, try inside the loop to skip one bad value.", "use",
    tip="A breakpoint pauses the running program at a chosen line so that you can look around.", terms=["breakpoint"]))

L2.append(make("Q3b", [5], [(B, 9), (B, 21)], 4, "mcq",
    "A team replaces its print calls with logging at level WARNING. Which reason best explains why this helps them?", [],
    ["Logging calls run faster than print calls, so the whole program finishes sooner",
     "The level acts as a threshold, so quieter messages can be switched on later without editing the calls",
     "Logging stops the program at the first warning, so the bug is easy to see",
     "Logging deletes older messages automatically, so the screen never fills up"], "B", 5,
    "The level is a threshold: messages below it are dropped, and lowering the threshold to DEBUG shows them again with no change to the calls.", "reason",
    tip="Logging writes messages with a severity level instead of printing them directly.", terms=["logging"]))

steps = ["Compare the guess with the secret number and print a hint", "Draw the secret number once, before the loop starts",
         "Leave the loop with break when the guess is right", "Ask the player for a guess at the top of each pass"]
L2.append(make("Q4a", [3], [(A, 114), (A, 83)], 3, "order",
    "Put the four steps of a guessing game in the order in which they must happen for the game to work.", [],
    steps, [3, 1, 4, 2], 16,
    "Draw the secret first (1), then in each pass ask (2), compare (3) and leave with break when right (4); drawing inside the loop would change the secret every pass.", "use",
    tip="Secret first, guesses after: the number to find must stay the same during the game."))

code = ["grid = [[0] * 3] * 2", "grid[0][1] = 5", "print(grid)"]
expect("\n".join(code), "[[0, 5, 0], [0, 5, 0]]")
L2.append(make("Q4b", [6], [(C, 17), (C, 30)], 4, "mcq",
    "This program prints a grid in which both rows changed. What would change if each row were created separately inside a loop?", code,
    ["Only the first row would show the 5, because the rows would no longer be one shared list",
     "Nothing would change because a loop creates the same list again",
     "Both rows would show 5 and the grid would become three rows long",
     "Only the second row would show the 5, because the loop fills rows from the end"], "A", 4,
    "[[0] * 3] * 2 repeats one inner list, so both rows are one list; separate rows are separate lists and only grid[0] changes.", "effect", indirect="consequence"))

code = ['a = input("a? ")', 'b = input("b? ")', 'c = input("c? ")', "print(a + b + c)"]
expect("\n".join(code), "a? b? c? 5342", stdin="5\n3\n42\n")
L2.append(make("Q5a", [1, 5], [(B, 16), (A, 20)], 4, "mcq",
    "Typing 5, 3 and 42 at the three prompts shows 5342 instead of 50. Which reason and fix are correct?", code,
    ["print joins everything it receives, so it should be replaced by another output function",
     "The prompts are too short, so Python keeps digits from earlier answers",
     "input gives text and + joins text, so each answer should be turned into a number with int() first",
     "Numbers above nine cannot be added, so the answers must be typed with leading zeros"], "C", 3,
    "input() always returns text and + on text glues characters, so 5 + 3 + 42 becomes 5342; int() on each answer makes + add.", "reason", indirect="reason"))

L2.append(make("Q5b", [2, 7], [(A, 47), (C, 51)], 5, "mcq",
    "Why does the test 'cat' in pets and pets['cat'] > 1 not crash when the key 'cat' is absent?", [],
    ["Square brackets return None for a missing key, so the comparison is simply false",
     "The in test adds the missing key with a default value before the lookup",
     "Python catches the missing key silently whenever a comparison is used",
     "and stops at the first false operand, so the lookup that would fail never runs"], "D", 3,
    "'cat' in pets is False, and and stops at a false first operand, so pets['cat'] is never evaluated.", "reason", indirect="reason"))

# ---------------------------------------------------------------- write
def dump(path, obj):
    with open(os.path.join(HERE, path), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")

if __name__ == "__main__":
    dump("items_a_v2_0_0.json", L1)
    dump("items_a_v2_0_0_makeup.json", L2)
    dump("items_a_v2_0_0_provisional.json", {
        "set": "A", "version": "2.0.0", "task": "TK4_Items_A2",
        "provisional": True,
        "reason": "The Owner will send question styles that may change the formats; every record below is provisional until then.",
        "records": [{"file": f, "id": it["id"], "provisional": True} for f, L in (("items_a_v2_0_0.json", L1), ("items_a_v2_0_0_makeup.json", L2)) for it in L]})
    print("wrote", len(L1), "and", len(L2), "records; every decisive program run and matched")
