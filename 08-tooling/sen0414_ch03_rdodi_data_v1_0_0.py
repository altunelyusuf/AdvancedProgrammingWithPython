"""Chapter 3 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter was read on automatetheboringstuff.com on 2026-09-28. The Python documentation was read from the
CPython source tree at tag v3.14.4 (Doc/), the PEPs from the python/peps repository at commit ce48c4e (2026-09-27);
every behaviour was executed under Python 3.14.4. A claim not in this file was not made."""
__version__ = "1.0.0"
CH = 3
DATE = "2026-09-28"
PYVER = "3.14.4"
TITLE = "Loops for an advanced course: chapter 3 of the 3rd edition and today's Python"
QUESTION = "What does chapter 3 of the 3rd edition teach about repetition, ranges, importing modules and ending a program, and what must an advanced course add so that it matches current Python?"
CQS = ("Which constructs repeat a block, and what decides when each one stops?",
       "Which concepts reach beyond the 3rd edition into current Python, and on what source?")
PUBS = [
 ("P01","Automate the Boring Stuff with Python, 3rd edition - Chapter 3, Loops (Al Sweigart, No Starch Press, 2025)","https://automatetheboringstuff.com/3e/chapter3.html",True),
 ("P02","The Python Tutorial, 4. More Control Flow Tools - for, range(), break and continue, else clauses on loops (Python 3.14.4 documentation source)","https://docs.python.org/3/tutorial/controlflow.html",False),
 ("P03","The Python Language Reference, 8. Compound statements - the while and for statements (Python 3.14.4 documentation source)","https://docs.python.org/3/reference/compound_stmts.html",False),
 ("P04","The Python Standard Library, Built-in Functions - range, enumerate and zip (Python 3.14.4 documentation source)","https://docs.python.org/3/library/functions.html",False),
 ("P05","The Python Standard Library, sys - sys.exit (Python 3.14.4 documentation source)","https://docs.python.org/3/library/sys.html",False),
 ("P06","The Python Standard Library, Built-in Exceptions - KeyboardInterrupt (Python 3.14.4 documentation source)","https://docs.python.org/3/library/exceptions.html",False),
 ("P07","The Python Tutorial, 5. Data Structures - Looping Techniques (Python 3.14.4 documentation source)","https://docs.python.org/3/tutorial/datastructures.html",False),
 ("P08","PEP 572 - Assignment Expressions (Angelico, Peters and van Rossum, 2018; Python 3.8)","https://peps.python.org/pep-0572/",False),
 ("P09","PEP 618 - Add Optional Length-Checking To zip (Bucher, 2020; Python 3.10)","https://peps.python.org/pep-0618/",False),
 ("P10","PEP 765 - Disallow return/break/continue that exit a finally block (Katriel and Coghlan, 2024; Python 3.14)","https://peps.python.org/pep-0765/",False),
 ("P11","What's New In Python 3.14 - PEP 765: Control flow in finally blocks (Python documentation source)","https://docs.python.org/3/whatsnew/3.14.html",False),
 ("P12","PEP 8 - Style Guide for Python Code (van Rossum, Warsaw and Coghlan, 2001)","https://peps.python.org/pep-0008/",False),
]
CONCEPTS = [("Section",x) for x in ("while Loop Statements","for Loops and the range() Function","Importing Modules","Ending a Program Early with sys.exit()","A Short Program: Guess the Number","A Short Program: Rock, Paper, Scissors","Summary","Practice Questions")] + \
 [("Concept",x) for x in ("Loop","Sequence to iterate","Early exit")] + \
 [("Statement",x) for x in ("while","for","break","continue")] + [("Function","range()")]
FINDINGS = [
 ("F1","Background","Chapter 3 of the 3rd edition teaches repetition with the while statement, which repeats a block as long as its condition is true, and the for statement with the range() function, which repeats it a counted number of times; break leaves a loop early and continue jumps back to its start. It then shows how to import modules, how sys.exit() ends a program, and two short programs, Guess the Number and Rock, Paper, Scissors.",["P01"]),
 ("F2","Contemporary developments","Python 3.8 added assignment expressions, so a loop can test and name a value in one line - while chunk := file.read(8192): is the PEP's own example of a loop that cannot be trivially rewritten with the two-argument form of iter(). Python 3.10 added an optional strict argument to zip that raises ValueError when the iterables differ in length. Python 3.14 makes the compiler emit a SyntaxWarning when a return, break or continue leaves a finally block.",["P08","P09","P10","P11"]),
 ("F3","Comparative analysis","The reference documentation makes precise what the chapter leaves informal: a for statement evaluates its iterable once and iterates over an iterator made from it; range() returns an immutable arithmetic sequence that generates its values on demand rather than a list; a loop's else clause runs when the loop finishes without a break; the loop variable is overwritten on each pass and is not deleted when the loop ends; and code that modifies a collection while iterating over it is tricky, so the tutorial advises looping over a copy. enumerate() replaces range(len(a)) when both index and item are needed. sys.exit() raises SystemExit, so finally clauses still run. PEP 8 advises against wildcard imports, which agrees with the chapter, and advises imports on separate lines, which the chapter's import random, sys, os, math does not follow. The chapter's practice question on stopping a program stuck in an infinite loop is answered by the KeyboardInterrupt entry: Control-C.",["P03","P02","P04","P05","P06","P07","P12"]),
 ("F4","Conclusion","For an advanced course, chapter 3 is best taught as the iteration protocol seen from the loop: a for loop consumes an iterable, range() is one lazy sequence among many, enumerate() and zip() are the idioms that replace index arithmetic, the loop else and the assignment expression are the two features that shorten common loops, and the chapter's while-True-with-break pattern is the one to compare them against.",["P02","P04","P08"]),
]
# (top, mid, leaf, exemplar, definition, io-or-None)
TAX = [
 ("Repetition","ConditionLoop","WhileStatement","while name != 'your name':","A while statement repeats its block as long as its condition is true, and tests the condition again after every pass.",None),
 ("Repetition","ConditionLoop","InfiniteLoop","while True:","A loop whose condition never becomes false runs until something inside it leaves: break, return, sys.exit() or an exception.",None),
 ("Repetition","CountedLoop","ForStatement","for i in range(5):","A for statement takes each item of an iterable in turn, assigns it to its variable and runs the block once for each.",None),
 ("Sequence","RangeSequence","RangeStop","range(5)","range(n) yields the integers from 0 up to but not including n.",("list(range(5))","[0, 1, 2, 3, 4]")),
 ("Sequence","RangeSequence","RangeStartStop","range(12, 16)","range(start, stop) begins at start and ends before stop.",("list(range(12, 16))","[12, 13, 14, 15]")),
 ("Sequence","RangeSequence","RangeStep","range(0, 10, 2)","A third argument is the step between values.",("list(range(0, 10, 2))","[0, 2, 4, 6, 8]")),
 ("Sequence","RangeSequence","RangeDescending","range(5, -1, -1)","A negative step counts down, and the stop value is still excluded.",("list(range(5, -1, -1))","[5, 4, 3, 2, 1, 0]")),
 ("Sequence","RangeSequence","LazyRange","range(10)","A range is an object that produces its values when iterated, not a list holding them.",("range(10)","range(0, 10)")),
 ("Sequence","IterationHelper","EnumerateFunction","enumerate(['tic', 'tac', 'toe'])","enumerate pairs each item with a running count, replacing range(len(a)) when both are needed.",("list(enumerate(['tic', 'tac', 'toe']))","[(0, 'tic'), (1, 'tac'), (2, 'toe')]")),
 ("Sequence","IterationHelper","ZipStrict","zip(a, b, strict=True)","zip walks several iterables together; strict=True raises ValueError when their lengths differ instead of stopping at the shortest.",("list(zip('ab', [1, 2], strict=True))","[('a', 1), ('b', 2)]")),
 ("LoopControl","EarlyExit","BreakStatement","break","break ends the innermost enclosing loop at once and skips the loop's else clause.",None),
 ("LoopControl","EarlyExit","ExitFunction","sys.exit()","sys.exit() raises SystemExit, which ends the program unless something intercepts it; finally clauses still run.",None),
 ("LoopControl","Skipping","ContinueStatement","continue","continue skips the rest of the block and goes back to test the condition, or to take the next item.",None),
 ("LoopControl","LoopCompletion","LoopElseClause","for ... else:","An else clause on a loop runs when the loop finishes without executing break.",None),
 ("LoopControl","LoopCompletion","LoopVariableScope","the variable after the loop","The loop variable is overwritten on each pass and is not deleted when the loop ends; after a loop over an empty sequence it was never assigned.",None),
 ("Module","ImportForm","ImportStatement","import random","import makes a module's names available under the module's name, as random.randint(1, 10).",None),
 ("Module","ImportForm","MultipleImport","import random, sys, os, math","One import statement can name several modules separated by commas.",None),
 ("Module","ImportForm","StarImport","from random import *","from module import * brings every public name into the program without the module prefix.",None),
 ("ModernPractice","ExpressionStyle","AssignmentExpressionLoop","while chunk := file.read(8192):","An assignment expression names a value inside a condition, so a loop can read and test in one line.",None),
 ("ModernPractice","ExpressionStyle","ImportStyle","import os on one line, import sys on the next","PEP 8 advises one import per line and against wildcard imports.",None),
 ("ModernPractice","Hazard","MutationWhileIterating","for user in users: del users[user]","Changing a collection while iterating over it is tricky to get right; loop over a copy or build a new collection.",None),
 ("ModernPractice","Hazard","FinallyExit","break inside a finally block","Python 3.14 emits a SyntaxWarning when return, break or continue leaves a finally block.",None),
]
ERRORS = []
# Checked by sen0414_ch03_claims_check: each is executed under the interpreter and compared with the text that states it.
CLAIMS = [
 ("list(range(10)) == list(range(0, 10)) == list(range(0, 10, 1))", "True"),
 ("list(range(0))", "[]"),
 ("sum(range(4))", "6"),
]
S = "(Sweigart, 2025)"; PSF = "(Python Software Foundation, 2026)"; AN = "(Angelico et al., 2018)"; BU = "(Bucher, 2020)"; KC = "(Katriel and Coghlan, 2024)"; VW = "(Van Rossum et al., 2001)"
BODY = {
 "Repetition": "Chapter 3 is about running a block again: some loops repeat while a condition holds, others once for each item of a sequence %s." % S,
 "ConditionLoop": "A condition loop repeats as long as an expression is true, so how many times it runs depends on the program's data rather than on a count %s." % S,
 "WhileStatement": "A while statement repeats its block as long as its condition is true; unlike an if statement, execution jumps back to the start of the block, and the yourName.py program keeps asking until the user types the phrase %s." % S,
 "InfiniteLoop": "If the condition never becomes false the program keeps going forever, a common programming bug; written deliberately as while True:, the loop is left by break, return, sys.exit() or an exception %s %s." % (S, PSF),
 "CountedLoop": "A counted loop runs its block once for each item of a sequence, so its length is known before it starts %s." % S,
 "ForStatement": "A for statement evaluates its iterable once, makes an iterator from it, assigns each item to the target in turn and runs the block, so for i in range(5): runs five times %s %s." % (S, PSF),
 "Sequence": "Loops need something to iterate over, and range() is the chapter's way of making a sequence of integers %s." % S,
 "RangeSequence": "The range function makes an arithmetic progression of integers and takes one, two or three arguments %s." % S,
 "RangeStop": "With one argument range starts at 0 and stops before the argument, so list(range(5)) is [0, 1, 2, 3, 4] and the end point is never part of the sequence %s %s." % (S, PSF),
 "RangeStartStop": "With two arguments range begins at the first and stops before the second, so list(range(12, 16)) is [12, 13, 14, 15]; range(10), range(0, 10) and range(0, 10, 1) all give the same values %s %s." % (S, PSF),
 "RangeStep": "A third argument sets the step, so list(range(0, 10, 2)) is [0, 2, 4, 6, 8] %s." % S,
 "RangeDescending": "A negative step counts down, and the stop value is still excluded, so list(range(5, -1, -1)) is [5, 4, 3, 2, 1, 0] %s." % S,
 "LazyRange": "Printing a range shows range(0, 10), not the numbers: it behaves like a list in many ways but is an object that returns successive items when iterated, which saves space %s." % PSF,
 "IterationHelper": "Two built-in functions replace most index arithmetic in loops: one adds a count, the other walks several sequences together %s." % PSF,
 "EnumerateFunction": "When a loop needs both the position and the item, enumerate gives them as pairs, so list(enumerate(['tic', 'tac', 'toe'])) is [(0, 'tic'), (1, 'tac'), (2, 'toe')]; the tutorial prefers it to combining range and len %s." % PSF,
 "ZipStrict": "zip walks several iterables together and by default stops at the shortest; since Python 3.10 zip(..., strict=True) raises ValueError when the lengths differ, which turns a silent truncation into an error %s." % BU,
 "LoopControl": "Three statements and one function change how a loop runs or ends: break, continue, the loop's else clause and sys.exit() %s." % S,
 "EarlyExit": "Some programs must leave a loop, or the whole program, before the loop's own test would %s." % S,
 "BreakStatement": "The break statement ends the innermost enclosing for or while loop at once, and skips the loop's else clause; yourName2.py uses it to leave a while True: loop %s %s." % (S, PSF),
 "ExitFunction": "sys.exit() raises SystemExit, so it ends the program only when nothing intercepts the exception and only from the main thread; finally clauses still run, and an argument of None or 0 means success while a string is printed to standard error with exit status 1 %s." % PSF,
 "Skipping": "Skipping a pass is different from leaving the loop: the loop continues %s." % S,
 "ContinueStatement": "The continue statement skips the rest of the block and goes back to test the condition of a while loop, or to take the next item of a for loop; swordfish.py uses it to keep asking for a name %s %s." % (S, PSF),
 "LoopCompletion": "How a loop finishes can be told apart from how it was left, and what the loop variable holds afterwards is defined %s." % PSF,
 "LoopElseClause": "The else clause of a for or while loop runs when the loop finishes without executing break, and is skipped by a break, a return or a raised exception; it is the tidy way to say 'searched everything and found nothing' %s." % PSF,
 "LoopVariableScope": "The for statement overwrites its target on every pass, so assigning to it inside the block does not change the loop, and the name is not deleted when the loop ends; after a loop over an empty sequence it was never assigned %s." % PSF,
 "Module": "A program reaches the standard library's functions by importing the module that holds them %s." % S,
 "ImportForm": "The chapter shows three forms of the import statement, and PEP 8 has a view on each %s %s." % (S, VW),
 "ImportStatement": "The import statement makes a module's names available under the module's name, so after import random a program calls random.randint(1, 10), which returns an integer N with 1 <= N <= 10 %s %s." % (S, PSF),
 "MultipleImport": "The chapter lets one statement import several modules, as in import random, sys, os, math %s; PEP 8 says imports should usually be on separate lines %s." % (S, VW),
 "StarImport": "from random import * removes the module prefix, but the chapter itself concludes that using the full name makes for more readable code %s, and PEP 8 says wildcard imports should be avoided because they make it unclear which names are present %s." % (S, VW),
 "ModernPractice": "An advanced course pairs the chapter's loops with what current Python offers for the same jobs, and with the hazards the reference documentation names %s." % PSF,
 "ExpressionStyle": "Two recent language and style features shorten and tidy the loops and imports the chapter teaches %s." % AN,
 "AssignmentExpressionLoop": "Since Python 3.8 an assignment expression names a value inside a condition, so while chunk := file.read(8192): process(chunk) reads and tests in one line - the PEP's own example of a loop that cannot be trivially rewritten with a two-argument iter() %s." % AN,
 "ImportStyle": "PEP 8 advises one import per line and says wildcard imports should be avoided, with the single defensible exception of republishing an internal interface as part of a public API %s." % VW,
 "Hazard": "Two hazards the documentation names are worth teaching beside the chapter's programs %s." % PSF,
 "MutationWhileIterating": "Code that modifies a collection while iterating over that same collection can be tricky to get right; the tutorial's remedy is to loop over a copy, such as users.copy().items(), or to build a new collection %s." % PSF,
 "FinallyExit": "Python 3.14 makes the compiler emit a SyntaxWarning when a return, break or continue statement has the effect of leaving a finally block, as PEP 765 specifies %s." % KC,
}
