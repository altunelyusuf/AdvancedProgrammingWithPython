#!/usr/bin/env python3
"""Builder of the item set B, version 2.0.0 (task TK4_Items_B2).

Writes   items_b_v2_0_0.json          paper list     4 records: Q3c, Q4c, Q5c, Q5d
         items_b_v2_0_0_makeup.json   make-up list   4 records: Q3c, Q4c, Q5c, Q5d
         items_b_v2_0_0_provisional.json   side file, every record provisional
Set B holds only the records still missing from set A (items_a_v2_0_0*.json): 1 unit of Q3 (5 points), 1 unit of Q4 (5 points)
and 2 units of Q5 (2 points each), so that A plus B in each list make 30 units and 25, 25, 25, 25 and 10 points.
Every program that decides an answer is run here and the printed result is compared with the answer; a mismatch stops the build.
Set A's builder is imported for its helpers only; importing it re-runs its own checks and writes nothing.
Usage: python3 items_b_v2_0_0_make.py
"""
import json, os, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from items_a_v2_0_0_make import make, expect, A, B, C   # noqa: E402,F401

L1, L2 = [], []

# =============================================================== paper list
L1.append(make("Q3c", [8, 6], [(C, 88), (C, 87)], 4, "mcq",
    "A program must turn the text 'cat' into 'Cat'. Writing word[0] = 'C' stops with an error. Which reason explains this, and which fix works?", [],
    ["A string cannot be changed in place, so build a new string: 'C' + word[1:]",
     "A string has no first position, so count from one: word[1] = 'C'",
     "A string is too short to be edited, so add spaces to it first",
     "Assignment is allowed only on numbers, so turn the text into a number"], "A", 5,
    "Strings never change, so an edit builds a new string from slices of the old one: 'C' + word[1:] gives 'Cat'.", "reason",
    tip="A slice such as word[1:] is a new string holding the text from position 1 to the end."))

code = ["def count_vowels(text):", "    n = 0", "    for ch in text:", "        if ch in 'aeiou':", "            n += 1", "        return n", "", 'print(count_vowels("banana"))']
expect("\n".join(code).replace("        return n", "    return n"), "3")
expect("\n".join(code), "0")
L1.append(make("Q4c", [4, 3], [(A, 129), (A, 128)], 5, "mcq",
    "The function below counts vowels, but its return line sits inside the loop. What changes in the result for banana, compared with the return placed after the loop?", code,
    ["It still prints 3: return only shows the value, and the loop goes on",
     "It prints 0: return ends the call after the first letter b, so the later vowels are never counted",
     "It prints 6: every letter is counted once more",
     "It stops with an error: a return may not stand inside a loop"], "B", 5,
    "return ends the call at once; inside the loop it runs after the first letter b, which is no vowel, so n is still 0.", "effect", indirect="consequence", width=45))
L1[-1]["listing"] = code

code = ["def add_guest(guests):", "    guests += ['Eda']", "", "def add_other(guests):", "    guests = guests + ['Ali']", "", "team = ['Zoe']", "add_guest(team)", "add_other(team)", "print(team)"]
expect("\n".join(code), "['Zoe', 'Eda']")
L1.append(make("Q5c", [6, 4], [(C, 32), (C, 16)], 5, "mcq",
    "Read the program, then choose what the last line prints and the reason why the two functions act differently.", code,
    ["['Zoe', 'Eda', 'Ali']: both functions change the caller's list",
     "['Zoe']: a function can never change the list of its caller",
     "['Zoe', 'Ali']: the second call replaces the change of the first",
     "['Zoe', 'Eda']: += changes the list itself, while + builds a new list for the local name"], "D", 2,
    "+= changes the caller's list itself, so Eda stays; guests + [...] builds a new list that only the local name guests reaches, so Ali is lost.", "effect",
    tip="A line with += changes the existing list; a line with + and = makes a new list.", indirect="consequence"))

code = ["labels = ['a', 'b']", "groups = dict.fromkeys(labels, [])", "groups['a'].append(1)", "print(groups)"]
expect("\n".join(code), "{'a': [1], 'b': [1]}")
L1.append(make("Q5d", [7, 6], [(C, 80), (C, 82)], 4, "mcq",
    "Read the program, then choose why the list of b also holds the 1 although only groups['a'] was changed.", code,
    ["append always adds the item to every list of a dictionary",
     "dict.fromkeys was given one list, so every key reaches that same list",
     "The keys a and b are equal, so they are one key",
     "A dictionary copies a list into a key only when the key is read"], "B", 2,
    "fromkeys uses the one object it is given as the value of every key, so a change through one key shows under all of them.", "reason",
    tip="A dictionary holds one value per key; one list given as the value is not a list per key.", terms=["dictionary"], indirect="reason"))

# =============================================================== make-up list
L2.append(make("Q3c", [8, 2], [(C, 125)], 4, "mcq",
    "A program tests 'if line.find(\"error\"):' to see whether a log line holds the word error. Which reason shows that this test is unreliable?", [],
    ["find hands back a position: 0 when the word starts the line (false) and -1 when it is missing (true)",
     "find works only on lines that are shorter than ten characters",
     "find changes the line to lower case before it looks for the word",
     "find hands back the word itself, which is never false"], "A", 5,
    "find gives the index of the first match or -1; a match at position 0 is false in an if, while the -1 of a missing word is true.", "reason",
    tip="find tells where a text starts inside another text, counting from zero."))

code = ["def show():", '    print("hello")', "", "show()"]
expect("\n".join(code), "hello")
L2.append(make("Q4c", [4, 1], [(A, 123), (A, 162)], 5, "mcq",
    "A script calls show() on its last line. What changes if the def of show is moved below that call, to the end of the file?", [],
    ["Nothing changes, because Python reads the whole file before it runs the first line",
     "The call stops with a NameError, because the def has not run yet when the call is reached",
     "The function runs twice, once at the call and once at the def",
     "The call prints None, because the function is still empty"], "B", 5,
    "def only stores the function when its line runs; a call placed before the def meets a name that does not exist yet.", "effect",
    tip="A NameError means Python met an unknown name; a def line stores its name only when reached.", terms=["NameError"], indirect="consequence"))
expect("show()\ndef show():\n    print('hello')", None, err="NameError")

code = ["items = [5, 6, 7, 8]", "del items[0]", "del items[1]", "print(items)"]
expect("\n".join(code), "[6, 8]")
expect("items = [5, 6, 7, 8]\ndel items[1]\ndel items[0]\nprint(items)", "[7, 8]")
L2.append(make("Q5c", [6, 4], [(C, 31), (C, 5)], 5, "mcq",
    "Read the program, then choose what it prints and what the opposite order of the two del lines would print.", code,
    ["[6, 8], and [7, 8] in the opposite order: after a deletion the later items move down one place",
     "[6, 8], and [6, 8] in the opposite order: the order of deletions never matters",
     "[7, 8], and [6, 8] in the opposite order: del counts from the back",
     "[6, 7], and [7, 8] in the opposite order: del removes the item at the end"], "A", 2,
    "After del items[0] the list is [6, 7, 8], so index 1 is now 7 and [6, 8] remains; the opposite order removes 6 and then 5, leaving [7, 8].", "effect",
    tip="After a deletion the items behind it move down one place, so the indexes shift.", indirect="consequence"))

code = ["stock = {'pen': 0, 'ink': 3}", "for name in stock:", "    if stock[name] == 0:", "        del stock[name]", "print(stock)"]
expect("\n".join(code), None, err="RuntimeError")
L2.append(make("Q5d", [7, 3], [(C, 81), (C, 12)], 4, "mcq",
    "Read the program, then choose what happens when it runs and the reason for it.", code,
    ["It prints {'ink': 3}: the pair with a zero is deleted and the loop goes on",
     "It prints {'pen': 0, 'ink': 3}: del does nothing inside a loop",
     "It stops with an error: a dictionary may not change its size while a loop reads it",
     "It prints {}: del removes every pair when one pair is deleted"], "C", 2,
    "Deleting a pair while looping over the dictionary raises a RuntimeError; build a new dictionary or loop over a list of the keys instead.", "reason",
    tip="A dictionary stores pairs of key and value, and a loop over it reads those pairs one after another.", terms=["dictionary"], indirect="exception"))


def dump(path, obj):
    with open(os.path.join(HERE, path), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


if __name__ == "__main__":
    dump("items_b_v2_0_0.json", L1)
    dump("items_b_v2_0_0_makeup.json", L2)
    dump("items_b_v2_0_0_provisional.json", {
        "set": "B", "version": "2.0.0", "task": "TK4_Items_B2", "provisional": True,
        "reason": "The Owner will send question styles that may change the formats; every record below is provisional until then.",
        "records": [{"file": f, "id": it["id"], "provisional": True} for f, L in (("items_b_v2_0_0.json", L1), ("items_b_v2_0_0_makeup.json", L2)) for it in L]})
    print("wrote", len(L1), "and", len(L2), "records; every decisive program run and matched")
