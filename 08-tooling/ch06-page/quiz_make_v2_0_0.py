#!/usr/bin/env python3
"""SEN0414 chapter 6 - builds quiz_v2_0_0.json, objectives_v2_0_0.json, discussion_v1_0_0.json, test_config_v2_0_0.json and stories_img_v1_0_0.json
(version 2.0.0). Each quiz item that rests on code is checked here by running the code under python3.14; the options, the answer index and the
rationales are written below. Run: python3.14 quiz_make_v2_0_0.py"""
__version__ = "2.0.0"
import json, os, subprocess
here = os.path.dirname(os.path.abspath(__file__))
PY = "/root/.local/bin/python3.14"
Q = []

def q(text, options, answer, level, obj, why, code=None, expect=None):
    if code is not None:
        got = subprocess.run([PY, "-c", code], capture_output=True, text=True).stdout.strip()
        assert got == expect, (text, got, expect)
        assert options[answer] == expect, (text, options[answer], expect)
    Q.append(dict(q=text, options=options, answer=answer, level=level, objective=obj, rationales=["" if i == answer else why[i if i < answer else i - 1] for i in range(len(options))]))

q("For spam = ['a', 'b', 'c', 'd', 'e'], what does spam[-3:-1] give?", ["['d', 'e']", "['c', 'd']", "['b', 'c', 'd']"], 1, "Apply", "CO1",
  ["The slice ends before the last item, and index -1 is 'e', so 'e' is left out.", "-3 is 'c' and the end -1 is 'e', which is left out, so three items cannot be right."],
  "spam = ['a', 'b', 'c', 'd', 'e']\nprint(spam[-3:-1])", "['c', 'd']")
q("After s = [1, 2, 3] and t = s + [4], what are s and t?", ["[1, 2, 3, 4] and [1, 2, 3, 4]", "[1, 2, 3] and [1, 2, 3, 4]", "[1, 2, 3] and [4]"], 1, "Apply", "CO1",
  ["The + operator builds a new list and leaves s alone.", "t is the concatenation of both lists, not only the new one."],
  "s = [1, 2, 3]\nt = s + [4]\nprint(s, 'and', t)", "[1, 2, 3] and [1, 2, 3, 4]")
q("Which call removes the item at index 0 and gives it back?", ["spam.remove(0)", "del spam[0]", "spam.pop(0)"], 2, "Understand", "CO1",
  ["remove takes a value, not an index, and returns None.", "del removes the item but is a statement and gives nothing back."])
q("names = ['bob', 'Alice', 'carol']. What does sorted(names, key=str.lower) give?", ["['Alice', 'bob', 'carol']", "['Alice', 'carol', 'bob']", "['bob', 'carol', 'Alice']"], 0, "Apply", "CO2",
  ["The key lowers the case for the comparison only, so 'bob' comes before 'carol'.", "Without the key, capital letters would come first, but the key is applied here and the order is a, b, c."],
  "names = ['bob', 'Alice', 'carol']\nprint(sorted(names, key=str.lower))", "['Alice', 'bob', 'carol']")
q("For the empty list spam, what does len(spam) > 0 and spam[5] == 'x' give?", ["IndexError", "True", "False"], 2, "Apply", "CO2",
  ["The right operand is never evaluated, because the left one is already False.", "The left operand is False, so the whole expression cannot be True."],
  "spam = []\nprint(len(spam) > 0 and spam[5] == 'x')", "False")
q("What does [i for i, c in enumerate('abc') if c != 'b'] give?", ["[0, 2]", "['a', 'c']", "[1]"], 0, "Apply", "CO3",
  ["The comprehension collects the indexes i, not the characters.", "The only character left out is 'b', which is at index 1, so index 1 is the one missing."],
  "print([i for i, c in enumerate('abc') if c != 'b'])", "[0, 2]")
q("Why does removing items inside 'for x in items' skip some of them?", ["The loop keeps a position that the removals move the items under", "remove only works on every second item", "The loop copies the list before it starts"], 0, "Analyze", "CO3",
  ["remove deletes the first match each time; the skipping comes from the loop's position.", "The loop does not copy the list; that is the remedy, not the cause."])
q("After a, *b, c = [1, 2, 3, 4, 5], what is b?", ["[2, 3, 4]", "[2, 3, 4, 5]", "(2, 3, 4)"], 0, "Apply", "CO3",
  ["The starred name receives the items left over, but c takes the last one.", "The starred name always receives a list, not a tuple."],
  "a, *b, c = [1, 2, 3, 4, 5]\nprint(b)", "[2, 3, 4]")
q("After x = [1], y = x and x += [2], what is y?", ["[1]", "[2]", "[1, 2]"], 2, "Analyze", "CO4",
  ["x += [2] extends the list in place, and y refers to the same list.", "The list still holds its first item."],
  "x = [1]\ny = x\nx += [2]\nprint(y)", "[1, 2]")
q("After a = [[1], [2]], b = copy.copy(a) and b[0].append(9), what is a?", ["[[1], [2]]", "[[1, 9], [2]]", "[[1], [2], 9]"], 1, "Apply", "CO4",
  ["The shallow copy shares the inner lists, so the change reaches a.", "append was applied to an inner list, not to the outer list."],
  "import copy\na = [[1], [2]]\nb = copy.copy(a)\nb[0].append(9)\nprint(a)", "[[1, 9], [2]]")
q("What does random.shuffle(x) return when x is a list?", ["The shuffled list", "A shuffled copy and leaves x unchanged", "None"], 2, "Understand", "CO5",
  ["It changes x in place and returns nothing.", "It does not copy; random.sample would give a new list."])

OBJ = {"_version": "2.0.0",
       "CO1": ["Read, slice, replace, add, remove and combine the items of a list, and predict the IndexError of an index outside it", "Apply"],
       "CO2": ["Search a list with in and index, put it in order with sort and sorted, and guard an item with a short-circuiting test", "Apply"],
       "CO3": ["Loop over a list with for, range(len(...)), enumerate and comprehensions, unpack it with the multiple assignment trick and a starred name, and explain why a list must not change during a loop", "Apply"],
       "CO4": ["Analyze how names, references, function arguments and copies decide whether a change to a list is seen elsewhere, and choose between copy.copy and copy.deepcopy", "Analyze"],
       "CO5": ["Build list-based programs with random.choice and random.shuffle: the Magic 8 Ball, the Matrix screensaver, Comma Code and Coin Flip Streaks", "Apply"],
       "_serves": [],
       "_note": "Chapter 6 is language groundwork. The course's approved outcomes are advanced, and none is specific to lists, so these chapter objectives are not claimed to serve one. They answer the chapter's three competency questions: CO1 and CO2 the first, CO3 and CO4 the second and the third, CO5 the programs."}
DISC = {"_version": "1.0.0", "items": [
    ["Noticeable issues", "What stood out in this chapter, and what surprised you about how a list behaves when two names refer to it?"],
    ["Interesting details", "Which list method or operator would you have designed differently (for example one that returns None), and what would the change cost?"],
    ["Unclarified issues", "Which points need further explanation? Select one critical issue from the chapter and explain it."]]}
TC = {"guide_q": "how do I copy a list so that a change to the copy does not reach the original?", "agent": "agent-Slicing", "root": "what does a slice of a list give back?",
      "_version": "2.0.0", "corpus_kinds": ["book", "chapter", "course", "page", "research"], "course_outcomes": True, "code_layers": True, "bank_complete": True,
      "course_q": "which course learning outcome is about choosing libraries?", "course_lo": "LO-1",
      "note": "2.0.0 for chapter 6, in the shape of chapter 5's test_config_v1_1_0.json: guide_q / agent / root are the questions the page test asks the guide and the Slicing agent (its slice holds executed examples, so a follow-up asking for an example can be answered); corpus_kinds, course_outcomes, code_layers and bank_complete are the switches the sibling line's test reads; course_q/course_lo name the question the course check asks and the outcome it must retrieve."}
IMG = {"_version": "1.0.0", "_note": "Story photographs for the chapter 06 page's Stories tab: every file sits in 03-materials/ch06/assets with its licence in ASSETS_PROVENANCE_v1_0_0.md; the mapping and the credit lines are taken from the chapter deck's own placements (08-tooling/ch06-deck/deck_build_v2_0_0.py).",
       "ZeroStart": [{"file": "photo_edsger_dijkstra.jpg", "credit": "Edsger Dijkstra, 1994 - photo: Andreas F. Borchert, CC BY-SA 4.0"}],
       "Shuffle": [{"file": "photo_ronald_fisher.jpg", "credit": "Ronald Aylmer Fisher, 1952 - photo: Barry Eagel, CC BY-SA 4.0"}],
       "EightBall": [{"file": "photo_magic_8_ball.jpg", "credit": "A Magic 8 Ball showing 'It is certain.' - photo: Zaneology, CC BY 2.0"}],
       "DigitalRain": [{"file": "book_fig_000101.jpg", "credit": "The chapter's screensaver in a console window (Figure 6-5) - Sweigart, Automate the Boring Stuff 3e, CC BY-NC-SA"}]}
for name, obj in (("quiz_v2_0_0.json", {"_version": "2.0.0", "items": Q}), ("objectives_v2_0_0.json", OBJ), ("discussion_v1_0_0.json", DISC), ("test_config_v2_0_0.json", TC), ("stories_img_v1_0_0.json", IMG)):
    json.dump(obj, open(os.path.join(here, name), "w"), indent=1, ensure_ascii=False)
print(len(Q), "quiz items;", sum(1 for x in Q if x["level"] == "Apply"), "Apply;", "answer positions", [x["answer"] for x in Q])
