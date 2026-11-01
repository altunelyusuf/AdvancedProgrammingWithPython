"""Chapter 2 deck content, version 4.1.0: the words of the deck. A NEW file; the analogies, the take-aways and the resources of version 4.0.0
are read from deck_content_v4_0_0.py (unchanged). Everything else is written anew for the Owner's review remarks of 2026-10-30 and the
Friday standard: every concept is taught on the slides (idea, reason, everyday picture, drawn mechanism, code, executed result), stories are told
as connected sentences without label words, speaker notes carry what to say, one example and one question (40 to 60 words)."""
__version__ = "4.1.0"
import importlib.util
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("deck_content_v4_0_0", os.path.join(_here, "deck_content_v4_0_0.py"))
_old = importlib.util.module_from_spec(_sp)
sys.modules["deck_content_v4_0_0"] = _old
_sp.loader.exec_module(_old)
ANALOGIES = _old.ANALOGIES
RESOURCES = _old.RESOURCES
TAKEAWAY = _old.TAKEAWAY

# ---- stories: connected sentences, three boxes of at most 30 words each, a picture and a live link
STORIES = {
    "boole": dict(title="Story: the man inside the bool type", img="photo_george_boole.jpg",
                  credit="George Boole. Portrait: public domain, via Wikimedia Commons (George Boole color.jpg).",
                  p1="George Boole, born in Lincoln, England, became the first professor of mathematics at Queen's College, Cork, and published The Mathematical Analysis of Logic in 1847.",
                  p2="Because he wanted exact rules for reasoning, he showed in 1854 that logic follows algebra, with statements as values and AND, OR and NOT as operations.",
                  p3="Python names its type bool after him, and every and, or and not of this chapter is one of his operations at work.",
                  link="https://en.wikipedia.org/wiki/George_Boole", linktext="Read about George Boole (Wikipedia)"),
    "indent": dict(title="Story: the whitespace that is the syntax", img="photo_guido_van_rossum_2006.jpg",
                   credit="Guido van Rossum at OSCON, 2006. Photo: Doc Searls, CC BY-SA 2.0, Wikimedia Commons.",
                   p1="Guido van Rossum started Python in December 1989 at Centrum Wiskunde & Informatica (CWI), the Dutch research institute in Amsterdam, and released it in February 1991.",
                   p2="He took the idea from ABC, a teaching language built at CWI. The layout of the code is its block structure, with no braces, only the indentation after a colon.",
                   p3="Because what the reader sees is what the interpreter sees, a program cannot look right and group wrong. Every block of this chapter shows it.",
                   link="https://docs.python.org/3/faq/design.html#why-does-python-use-indentation-for-grouping-of-statements", linktext="Read the Python design FAQ on indentation"),
    "match": dict(title="Story: a thirty-year-old wish, granted in 3.10", img="logo_python.png",
                  credit="Python logo. Source: python.org, Python Software Foundation, used under its trademark policy.",
                  p1="Brandt Bucher and Guido van Rossum wrote the specification and Daniel F Moisset the tutorial. The PEPs were created on 12 September 2020 and accepted on 8 February 2021.",
                  p2="Since Python had no switch statement, chains of elif and dictionaries were the usual answer for years. Structural pattern matching shipped in Python 3.10 on 4 October 2021.",
                  p3="The Steering Council accepted it through the PEP process on peps.python.org. The match status of this chapter, with case 401 | 403 | 404, is that statement running.",
                  link="https://peps.python.org/pep-0636/", linktext="Read PEP 636, the tutorial (peps.python.org)"),
    "walrus": dict(title="Story: the walrus that changed who leads Python", img="photo_walrus_novaya_zemlya.jpg",
                   credit="A walrus, Russian Arctic National Park, 2015. Photo: Nixette, CC BY-SA 4.0, Wikimedia Commons.",
                   p1="Chris Angelico, Tim Peters and Guido van Rossum wrote PEP 572, created on 28 February 2018. The operator := shipped in Python 3.8 in October 2019.",
                   p2="It assigns a value to a name and gives the value back inside a larger expression, so that a value can be tested and kept in one step.",
                   p3="The debate on the python-dev mailing list was so long that on 12 July 2018 Guido van Rossum announced that he would step down as BDFL.",
                   link="https://peps.python.org/pep-0572/", linktext="Read PEP 572 (peps.python.org)"),
}
STORY_NOTES = {
    "boole": "George Boole published his algebra of logic in 1847 and 1854, and Python's bool type carries his name. Show the portrait and open the link. Ask the class: where in your own code do you use and, or and not without thinking of him?",
    "indent": "Guido van Rossum took the indentation idea from ABC at CWI in Amsterdam, and the design FAQ still defends it. Show the photo and open the link. Ask the class: what could go wrong if the layout and the logic were allowed to disagree?",
    "match": "The match statement arrived in Python 3.10 in October 2021, after PEPs 634 to 636. It is more than a switch, because patterns also bind names. Open the tutorial link. Ask the class: which cases of the next slide could be elif lines?",
    "walrus": "PEP 572 gave Python the walrus operator in version 3.8, and the debate led Guido van Rossum to step down as BDFL in July 2018. Show the walrus photo. Ask the class: when should a name that is tested also be kept?",
}

# ---- teach slides: one per code example. idea, reason and picture are single short boxes; flow = the drawn mechanism, four steps
TEACH = {
    "booleans": dict(title="Boolean values: only two answers", idea="A Boolean value is True or False. It answers a yes or no question, and its type is called bool.",
                     reason="A program decides by asking questions. Two possible answers keep every decision simple and exact.",
                     picture="A Boolean value is a light switch: it is on or off, never half.",
                     flow=[("Ask", "a yes or no question"), ("Python answers", "True or False"), ("Numbers inside", "True is 1 and False is 0"), ("bool() converts", "0 gives False, others True")]),
    "comparison": dict(title="Comparison operators: six questions", idea="A comparison operator compares two values and returns True or False. There are six: ==, !=, <, >, <= and >=.",
                       reason="Every decision starts with a question about data, such as is the age at least 18. The six operators ask it.",
                       picture="A comparison is a pair of kitchen scales: put two things on it and read which side is heavier.",
                       flow=[("Take two values", "x is 7 and y is 9"), ("Pick an operator", "for example x < y"), ("Python compares", "7 is below 9"), ("Python answers", "True")]),
    "equality": dict(title="Equality: what counts as the same", idea="== asks whether two values are equal. A number never equals a string, and strings are compared letter by letter.",
                     reason="Programs compare input, numbers and text all the time. Knowing what counts as equal prevents silent bugs.",
                     picture="Equality is two keys side by side: the teeth must match exactly, or the door stays shut.",
                     flow=[("Compare types", "42 equals 42.0, not '42'"), ("Compare letters", "'hello' differs from 'Hello'"), ("Compare decimals", "0.1 + 0.2 is a little off"), ("Compare order", "character codes: Z before a")]),
    "chained": dict(title="Chained comparisons: between two limits", idea="A chain such as 10 < age < 20 joins two comparisons. Python reads it as 10 < age and age < 20.",
                    reason="Checking that a value lies between two limits is very common. The chain writes it the way mathematics does.",
                    picture="A chain is a height bar with a lower and an upper mark: you must pass between both.",
                    flow=[("Write", "10 < age < 20"), ("Python splits", "10 < age and age < 20"), ("Python tests", "each link, left to right"), ("Result", "True only if every link holds")]),
    "truthtable": dict(title="and, or: the truth table", idea="and gives True only when both sides are true. or gives True when at least one side is true.",
                       reason="Real conditions have several parts. and and or join the parts into one answer, and a table shows every case.",
                       picture="and is two locks on one door; or is two doors into one room.",
                       flow=[("Pick a pair", "a and b: four pairs exist"), ("and", "True in one row only"), ("or", "True in three rows"), ("Count", "the chart shows the true results")]),
    "notprec": dict(title="not, and the order of the operators", idea="not flips a Boolean value. When operators are mixed, Python applies comparisons first, then not, then and, then or.",
                    reason="Without a fixed order the same line could mean two things. Parentheses make the order visible to readers.",
                    picture="not is a mirror: it shows the opposite of what stands in front of it.",
                    flow=[("Comparisons", "== < > are done first"), ("not", "flips the result"), ("and", "binds tighter than or"), ("Parentheses", "override the order")]),
    "mixing": dict(title="Mixing Boolean and comparison operators", idea="Comparisons give Boolean values, and Boolean operators join those values into one answer.",
                   reason="Real rules, such as who may enter, combine several facts: an age limit and a membership.",
                   picture="A club door: first read the age on the card, then look for the membership stamp.",
                   flow=[("Read the facts", "age is 25, member is True"), ("Compare", "age >= 18 gives True"), ("Join", "True and True gives True"), ("Answer", "the door opens")]),
    "shortcircuit": dict(title="Short-circuit: stop early, return an operand", idea="or stops at the first true operand and and stops at the first false one. The result is that operand, not always True or False.",
                         reason="Stopping early saves work and avoids errors, for example a division by zero that is never reached.",
                         picture="Asking two guards: if the first says no, you do not walk to the second.",
                         flow=[("Look at the left", "1 or ...: the left is true"), ("Stop early", "the right side is skipped"), ("Return an operand", "the value looked at last"), ("No error", "1 / 0 is never run")]),
    "truthiness": dict(title="Truthiness: which values count as false", idea="Every value counts as true or false in a condition. Zero, empty containers, the empty string and None are false; all else is true.",
                       reason="A short test such as if items: reads naturally and needs no comparison with True.",
                       picture="An empty box counts as nothing; a box with anything inside counts as something.",
                       flow=[("Take a value", "0, '', [], None or 'a'"), ("Ask bool()", "is it empty or zero?"), ("Empty or zero", "counts as False"), ("Anything else", "counts as True")]),
    "block": dict(title="Blocks: lines that belong together", idea="A block is a run of lines indented under a statement that ends with a colon. The lines run together or not at all.",
                  reason="A decision must say which lines depend on it. The indentation shows it to the reader and to Python.",
                  picture="A block is a room in a house: everything inside the walls belongs together.",
                  flow=[("The header", "if age > 65: ends in a colon"), ("Condition true?", "age is 70, so yes"), ("The block runs", "both indented lines"), ("Then", "the next unindented line runs")]),
    "indent": dict(title="Indentation decides the block", idea="Indentation is the syntax of Python. Lines with the same indent belong together, and a less indented line ends the block.",
                   reason="What the reader sees is what Python sees, so a program cannot look right and group wrong.",
                   picture="Indentation is a bullet list: the deeper dash belongs to the item above it.",
                   flow=[("The header", "if x > 3: with x equal to 1"), ("Condition false", "x > 3 is False"), ("Block skipped", "both indented lines"), ("Outside the block", "the last line always runs")]),
    "password": dict(title="if and else: two roads", idea="if runs its block when the condition is true, and else runs when it is false. An if can sit inside another block.",
                     reason="Decisions often depend on earlier decisions, such as the name first and then the password.",
                     picture="A door that opens only when its sensor sees you, and a side door for when it does not.",
                     flow=[("Check the name", "username == 'Mary'"), ("Inside: the password", "password == 'swordfish'"), ("True", "Access granted."), ("False", "the else prints Wrong password.")]),
    "elif": dict(title="elif: a ladder with one exit", idea="elif is another condition, tested only if every condition above it was false. The first true rung runs and the rest are skipped.",
                 reason="Many decisions have more than two outcomes. A ladder of rungs handles them in one statement.",
                 picture="A ladder: you climb down from the top and stop at the first rung that holds.",
                 flow=[("Rung 1", "is the name Alice? No"), ("Rung 2", "is age below 12? No"), ("Rung 3", "is age above 2000? Yes, run it"), ("The rest", "skipped")]),
    "elifOrder": dict(title="elif: the order of the rungs", idea="The rungs are tested from the top, so a broad test placed too early hides a narrow test below it.",
                      reason="The order of the rungs is part of the logic. A wrong order leaves a rung that can never run.",
                      picture="A coarse sieve above a fine sieve: nothing ever reaches the fine one.",
                      flow=[("age < 12", "catches the children"), ("age > 100", "also catches every age above 2000"), ("age > 2000", "never reached"), ("else", "catches what is left")]),
    "oppositeday": dict(title="Opposite Day: follow one variable", idea="The program sets a flag, may flip an answer with not, and prints a message. Follow one variable through the lines that ran.",
                        reason="Tracing one variable line by line is the way to understand and to debug any program.",
                        picture="A child who says the opposite of everything: says yes, means no.",
                        flow=[("Set the flag", "opposite_day is True"), ("First if", "say_it becomes True"), ("Flip", "not turns it into False"), ("Last if", "prints the answer")]),
    "capacity": dict(title="The Dishonest Capacity Calculator", idea="An elif ladder chooses a ratio by unit, and an else keeps the result defined for a unit nobody planned.",
                     reason="Disk makers count in powers of ten, but computers count in powers of two. The program converts one into the other.",
                     picture="A bakery's dozen of eleven rolls: the label and the box do not count the same way.",
                     flow=[("Read the unit", "'TB' for terabyte"), ("Pick the ratio", "10**12 divided by 2**40"), ("Multiply", "advertised times the ratio"), ("Print", "the real capacity, rounded")]),
    "condexpr": dict(title="The conditional expression", idea="A conditional expression, a value if a condition else another value, picks one of two values in a single line.",
                     reason="Short choices stay short. Only the chosen side is evaluated, so the other side may hold a risky expression.",
                     picture="A coin toss with a rule: heads you take the first prize, tails the second.",
                     flow=[("Test", "n % 2 == 0"), ("True", "the value before if"), ("False", "the value after else"), ("Only one side runs", "1 / 0 is skipped")]),
    "match": dict(title="match: a switch that matches patterns", idea="match compares a value with each case from the top and runs the first case that fits. The underscore case fits anything.",
                  reason="Python had no switch statement. A match reads better than a long elif chain for many fixed values.",
                  picture="The sorting machine of a post office: each parcel slides to the first slot its shape fits.",
                  flow=[("The value", "status is 403"), ("case 200", "does not fit"), ("case 401 | 403 | 404", "fits, so it runs"), ("case _", "never reached")]),
    "matchseq": dict(title="match: sequences and captures", idea="A pattern can take a list apart. A name inside the pattern captures the item at that position.",
                     reason="Commands and messages often arrive as lists. A pattern checks the shape and unpacks the parts at once.",
                     picture="A parcel scanner reads the shape of the box and opens it in one move.",
                     flow=[("The value", "['go', 'north']"), ("The shape", "two items, the first is 'go'"), ("The capture", "direction becomes 'north'"), ("The block runs", "going north")]),
    "matchguard": dict(title="match: guards", idea="A guard adds an if to a case. The case runs only if the pattern fits and the guard is true.",
                       reason="Some tests cannot be written as a pattern alone, such as two items being equal.",
                       picture="A guard at one slot: the shape fits, but the ticket must also be right.",
                       flow=[("The value", "(3, 3)"), ("The pattern", "(x, y) fits: x and y are 3"), ("The guard", "x == y is True"), ("The block runs", "diagonal at 3")]),
    "walrus": dict(title="The walrus: test and keep", idea="The walrus := assigns a value to a name and gives the value back inside a larger expression.",
                   reason="A value can be tested and kept in one step, without computing it twice or adding a line.",
                   picture="A cashier who rings up the price and reads out the total in the same breath.",
                   flow=[("Compute", "len(name)"), ("Keep", "size stores the length"), ("Test", "is size above 3?"), ("Use", "size is printed in the block")]),
}

# ---- speaker notes: 40 to 60 words (dividers and title 25 to 60): what to tell, one example, one question
NOTES = {
    "title": "Welcome. This chapter teaches how a program decides. Every concept has an idea, an everyday picture, a drawn mechanism, the code and what the run printed. The same examples run on the chapter page, in the same order.",
    "route": "Five parts, each a run of slides you can jump to. Every code example sits in the chapter-code tab of the page in this same order. Example: part three has five examples about blocks and branches. Ask the class: which part do you expect to be hardest, and why?",
    "questions": "Two questions guide the chapter. How does a program choose what to do, and what makes a condition true? What does current Python add to the book? Example: the match statement. Ask the class to guess the answer to the first question now.",
    "divider1": "Part one. A Boolean value is the answer to a yes or no question, and comparison operators ask the questions. Predict each result before the run. Example: is seven below nine? Ask the class which comparison surprises them.",
    "divider2": "Part two. The operators and, or and not combine answers. Python stops early and returns an operand, and truthiness lets any value act as true or false. Example: an empty list. Ask the class which values count as false.",
    "divider3": "Part three. A block is a run of indented lines. The statement if runs it on a true condition, and else and elif add the other roads. Watch the order of the rungs. Ask the class what happens when two rungs are true.",
    "divider4": "Part four. Two short programs from the book use everything so far. Follow the variables line by line, then predict the printed text. Example: Opposite Day flips an answer. Ask the class to say what a trace is.",
    "divider5": "Part five. Python moved on after the book. The conditional expression, match and the walrus are in current code every day. Example: match replaces a long elif chain. Ask the class which one they would use first.",
    "A1": "A switch is on or off, like a Boolean value, and scales compare two things. Read each row aloud and let the class add a picture of their own. Example: the height bar at a fairground. Ask: which picture fits greater than or equal to?",
    "A2": "The word and is two locks on one door, or is two doors into one room, and not is a mirror. Example: a club door that checks age and membership. Ask the class which picture is closest to an empty list counting as false.",
    "A3": "A signpost at a fork sends you one way, a block is a room, and an elif ladder is climbed from the top. Example: a hiking trail with three forks. Ask the class what happens if two rungs are both true.",
    "A4": "Both programs of the book are small recipes. Opposite Day flips an answer, and the capacity calculator chooses a ratio by unit. A trace is a notebook with one line per step. Ask the class: why does a baker's dozen differ from a dozen?",
    "A5": "The conditional expression picks one of two values, match sorts by shape, a guard adds a condition and the walrus assigns inside an expression. Example: the post office sorting machine. Ask the class which of the four they would explain to a friend first.",
    "current": "Python moves on, and these features are newer than the book. And and or return operands, match came in 3.10 and the walrus in 3.8. Example: Python 3.14 warns about leaving a finally block. Ask the class which version of Python they have installed.",
    "summary": "Five sentences to keep. The chart shows how many code examples each part of the chapter has. Example: part five has the most, because Python grew after the book. Ask the class to say the five sentences back in their own words.",
    "practice": "Four drills. Predict first, then run them on the chapter page. Example: add parentheses to a line so that the order is obvious. Ask each student to explain one answer in a single sentence to the neighbour, then compare the explanations.",
    "resources": "Start with the book chapter, then the Python documentation. The stories link to first-hand sources and the PEPs. Example: PEP 636 is the tutorial for match. Ask the class to choose one link and read it before the next class.",
}
# code slides: (teach slide note, code slide note) per example
EX_NOTES = {
    "booleans": ("A Boolean value is the answer to a yes or no question, and Python has exactly two of them. Example: a light switch is on or off. Ask the class: why is it handy that True also counts as the number one?",
                 "Read the three results on the slide. True plus True is two, because the values are numbers in disguise. The bool function turns zero into False and everything else into True. Ask the class to predict bool of minus three and a half."),
    "comparison": ("Six operators ask six questions, and each one answers True or False. Example: is seven below nine? Ask the class: what is the difference between the single equals sign and the double equals sign?",
                   "The table shows the six questions about x and y with their answers. Notice that the not-equal operator is the exact opposite of the equal operator. Ask the class to change y to seven and predict the new row of answers."),
    "equality": ("Equality needs the same kind of value. A number never equals a string, and a capital letter is a different character. Example: 42 and the text 42. Ask the class: why would anyone compare text typed by a user in lower case?",
                 "Read the table row by row and mark the surprise. The decimal sum is a little off, because computers store fractions in binary. Capital Z sorts before small a because of character codes. Ask the class to predict the comparison of two tiny differences."),
    "chained": ("A chain checks that a value lies between two limits. Python expands it into comparisons joined by and. Example: is fifteen between ten and twenty? Ask the class: how would you write the same test in a language without chains?",
                "Look at the number line on the slide and find the marker for age. The second chain fails at its last link, so the whole chain is False. Ask the class to change age to twenty and predict both answers before the run."),
    "truthtable": ("The word and needs both sides true, while or needs only one. Example: a door with two locks against a room with two doors. Ask the class: in how many of the four rows is and true, and in how many is or true?",
                   "The table lists all four pairs and the answers of and and or. The chart counts the true results: one for and, three for or. Ask the class to say, in one sentence, when the word or gives False."),
    "notprec": ("The word not flips a value, and it binds weaker than the comparison operators. Example: not four equals five is not of the comparison. Ask the class: why do parentheses help a reader even when Python does not need them?",
                "Check the order in the table: comparisons, then not, then and, then or. The parentheses in the last line change the answer. Ask the class to add parentheses to the second line so that Python reads it the way a person would."),
    "mixing": ("A comparison gives a Boolean value, and the Boolean operators join those values. Example: age at least eighteen and a membership. Ask the class: which rule would you write for a cinema ticket with a student discount?",
               "Read each row from the left: the comparisons first, then the join, then the result. A member aged twenty-five passes the first test and fails the second. Ask the class to change age to twelve and predict all three answers."),
    "shortcircuit": ("The words and and or stop as soon as the answer is known, and they return the operand they stopped at. Example: asking two guards. Ask the class: why is a division by zero safe on the right side of or?",
                     "Follow the arrows in the picture to the operand that was returned. The division by zero never runs. Empty text and None count as false. Ask the class to predict what the expression zero and one divided by zero gives, then run it."),
    "truthiness": ("Every value counts as true or false when a condition tests it. Example: an empty shopping bag counts as nothing. Ask the class: why is writing if greeting better than comparing the greeting with True?",
                   "The table shows each value and what bool gives for it. Zero, empty text, an empty list and None are false. A list holding zero is true, because it is not empty. Ask the class which row surprised them most."),
    "block": ("A block is the group of lines that belong to one statement, and a colon opens it. Example: the two lines under the senior discount. Ask the class: what would the program print if the age were fifty?",
              "Look at the boxes on the slide: the teal ones ran. The two indented lines ran together, and the last line ran in any case. Ask the class to change the age to fifty and say which boxes turn grey."),
    "indent": ("In Python the indentation is the syntax, so the layout and the logic can never disagree. Example: a bullet list with a deeper dash. Ask the class: what would happen if the last line were indented as well?",
               "The table says which lines ran. The condition is false, so both indented lines were skipped, and only the last line was printed. Ask the class to indent the last line by four spaces, predict the output and then run it."),
    "password": ("An if can sit inside the block of another if, and an else belongs to the if at its own indent. Example: first the name, then the password. Ask the class: which message appears for the name Bob?",
                 "Follow the teal path through the boxes for this username and password. The inner else is skipped because the password is right. Ask the class to change the password and predict which box lights up instead."),
    "elif": ("An elif is tested only when everything above it was false, so exactly one block runs. Example: a ladder climbed from the top. Ask the class: what is printed for Carol if her age is fifty instead of three thousand?",
             "The table shows which rungs were tested and which one ran. The first true condition wins and the rest are skipped. Age three thousand stops at the third rung. Ask the class to predict the answer for age eighty."),
    "elifOrder": ("A broad test placed too early shadows a narrow test below it. Example: every age above two thousand is also above one hundred. Ask the class: how would you reorder the rungs so that the vampire message can appear?",
                  "Read the results for the four ages. Three thousand is stopped at the grannie rung, so the vampire rung never runs. The chart counts the rungs tested for each age. Ask the class to swap the two rungs and run it again."),
    "oppositeday": ("Follow one variable through the lines that ran. On an Opposite Day the flag starts as True, and the answer is then flipped with not. Example: a child who says the opposite. Ask the class: what is printed if the flag is False?",
                    "The table is a trace: one row for each line that ran and the value of the variable afterwards. The else lines were skipped. Ask the class to set the flag to False and predict which lines will run."),
    "capacity": ("A maker counts a terabyte as ten to the twelve bytes, but a computer counts two to the forty. The ladder picks the ratio by unit. Example: a ten terabyte disk. Ask the class: why does the else keep the program from crashing?",
                 "The table runs the same code for three units, and the chart sets the advertised size beside the real one. The else gives a ratio of one for an unknown unit. Ask the class to predict the real capacity of a ten gigabyte card."),
    "condexpr": ("The conditional expression picks one of two values in a single line. Example: the word even or the word odd for a number. Ask the class: when is the four-line if and else easier to read than the one-line version?",
                 "The arrows show which side of the expression was chosen for seven and for ten. In the last line the division by zero is never evaluated. Ask the class to write the same choice with an if and an else and compare the two versions."),
    "match": ("The match statement tries the cases from the top and runs the first one that fits. Example: a status code of 403 fits the third case. Ask the class: why must the underscore case stand last?",
              "The table shows which case caught each status. A pipe joins alternatives into one case. The status 418 falls through to the underscore. Ask the class to add a case for 500 that prints server error, and say where it must stand."),
    "matchseq": ("A pattern can take a list apart and capture a name from it. Example: go north gives the name direction the value north. Ask the class: which of the three commands falls through to the underscore case, and why?",
                 "The table shows each command and the case that caught it, and the chart counts the items in each list. A list with one item fits the quit case. Ask the class to add a case for a list that starts with take."),
    "matchguard": ("A guard adds a condition to a case: the pattern must fit and the guard must be true. Example: a point whose two numbers are equal lies on the diagonal. Ask the class: why must the guarded case stand before the plain case?",
                   "The table shows both points and the case that caught each. The point three and three passes the guard, while three and four falls to the plain case. Ask the class to remove the guard and predict what the first case would catch."),
    "walrus": ("The walrus operator assigns a value to a name and gives the value back, so one condition can test and keep it. Example: the length of a name. Ask the class: why would you not compute the length twice?",
               "The table shows each name, its length and whether the test passed. The name size stays available after the loop and holds the last length. Ask the class to change the limit from three to five and predict which names are printed."),
}


# ---- notes shorter than 40 words get one closing instruction, so that each note says what to tell, an example, a question and what to do with the picture
_PAD_T = [" Point at the drawing and read its four steps aloud, from left to right.", " Draw the four steps on the board, then compare them with the slide.", " Let one student retell the four steps in their own words."]
_PAD_C = [" Run the example on the chapter page and compare it with the picture.", " Change one value in the code, predict the new result, then run it.", " Ask a student to read the result picture aloud before you run it."]


def _pad(s, pads, k):
    return s if len(s.split()) >= 40 else s + pads[k % 3]


EX_NOTES = {k: (_pad(a, _PAD_T, i), _pad(b, _PAD_C, i)) for i, (k, (a, b)) in enumerate(EX_NOTES.items())}
