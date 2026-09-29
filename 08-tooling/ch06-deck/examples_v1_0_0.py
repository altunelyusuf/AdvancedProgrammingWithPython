__version__ = "1.0.0"
# Every program and every '>>>' session the chapter 6 deck shows. Outputs come from executing them (examples_run_v1_0_0.py), never from typing.
# The chapter's own programs are taken from the research data file (08-tooling/sen0414_ch06_rdodi_data_v1_0_0.py), not retyped: the Magic 8 Ball,
# the Matrix Screensaver and the passing-a-list program are cut out of its behaviour records BEH, which research_check_v1_0_0.py re-executes.
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sen0414_ch06_rdodi_data_v1_0_0 as R
BEH = {t: c for t, c, w in R.BEH}
def _between(title, start, end):
    c = BEH[title]; a = c.index(start) + len(start); return c[a:c.index(end, a)]
EIGHT = _between("Magic 8 Ball of the chapter", "prog = '''", "'''\nanswers")                 # the chapter's program, as recorded
MATRIX = _between("Matrix Screensaver of the chapter: where the counter is decremented", "prog = '''", "'''\ndef run")
PASSING = BEH["passingReference.py of the chapter"]
# the Magic 8 Ball as it is shown: the seed line is the only addition, so that every run of the deck prints the same answer; the answers wrap under the first
_e = EIGHT.replace("import random\n", "import random\nrandom.seed(4)  # the same answer every run\n", 1)
_e = re.sub(r"\n'", "\n    '", _e)
# session lines: expressions and statements run one after the other in one namespace; a statement has no result line, and a session ends with an expression
EX = {
 "hook": ["spam = [0, 1, 2, 3]", "eggs = spam", "eggs[1] = 'Hello!'", "spam"],
 "boxes": ["spam = ['cat', 'bat', 'rat', 'elephant']", "(spam[0], spam[-1], spam[-3], len(spam))", "spam[10000]", "[['cat', 'bat'], [10, 20, 30, 40, 50]][1][4]"],
 "added": ["spam = ['cat', 'dog', 'bat']", "spam = spam.append('moose')", "print(spam)"],
 "copied": ["import copy", "nested = [[1, 2], [3]]", "shallow = copy.copy(nested)", "deep = copy.deepcopy(nested)", "(shallow[0] is nested[0], deep[0] is nested[0])"],
 "replicated": ["lists = [[]] * 3", "lists[0].append(3)", "lists", "lists = [[] for i in range(3)]", "lists[0].append(3)", "lists"],
 "practice1": ["spam = [3, 1, 2]", "(spam.sort(), spam)"],
 "practice2": ["a = [1]; b = a; a += [2]", "b"],
 "practice3": ["lists = [[]] * 3", "len({id(x) for x in lists})"],
 "practice4": ["nums = [1, 2, 3, 4]", "for x in nums: x < 3 and nums.remove(x)", "nums"],
 "zero": ["[0] * 5"],
}
PROGRAMS = {
 "eightball_v1_0_0.py": (_e, [["Will it rain?"]]),
 "mutation_bug_v1_0_0.py": ("items = [1, 2, 3, 4]\nfor x in items:\n    if x < 3:\n        items.remove(x)\nprint(items)\n", [[]]),
 "mutation_fixed_v1_0_0.py": ("items = [1, 2, 3, 4]\nitems = [x for x in items if x >= 3]\nprint(items)\n", [[]]),
 "passing_v1_0_0.py": (PASSING, [[]]),
}
