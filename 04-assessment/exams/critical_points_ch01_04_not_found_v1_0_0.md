# Critical points of chapters 1 to 4: what could not be found or confirmed (v1.0.0)

For the Owner. Each item is a question that can be answered in one line. Sources read: the newest deck of each chapter (ch01 v4.1.0, ch02 v4.0.0, ch03 v5.1.0, ch04 v3.1.0) with slide text, tables and speaker notes; the newest corpus (ch01 v1.2.0, ch02 v1.0.0, ch03 v1.0.0, ch04 v1.0.0); the newest stories (v1.1.0 of each). Not read: pictures, drawings and chart data inside the decks (only their titles and captions); the research files under 03-materials/chNN/rdodi/.

## All four chapters

1. Nothing in the repository records what you stressed aloud in the lectures; the speaker notes are short. Every point in the JSON file rests on a deck stress (title, closing line, repeated, warning), a speaker note, or a corpus "watch out" paragraph. Which of the 171 points do you want kept, and which dropped?
2. A corpus "watch out" paragraph is a common-mistake warning written for the corpus, not necessarily something you said in class (85 of the 171 points rest on corpus or story text alone; the other 86 rest on slides or speaker notes). Should corpus-only points count as "explained in the course" for the exams?
3. The practice questions on the second-to-last slide of each deck (four per chapter) are not listed as critical points. Are they examinable as written?
4. The "Current Python adds more" table of each deck (slides 36, 39, 40, 43) lists features newer than the book. Are the newer-Python features (versions and PEP numbers) examinable, or only the behaviour?

## Chapter 1

1. No story of chapter 1 (Python's birth, hello world, Leibniz) ties to a common mistake except binary numbers. Are the story facts (names, dates, places) examinable?
2. print with sep and end (slide 23) is explained once and never repeated or warned about. Is it critical?
3. The import statement and the math module (slide 28) are taught once and no corpus warning ties them to a mistake in chapter 1. Is the module idea examinable in chapter 1?
4. bin(), format(n, '08b') and int(text, 2) (slide 35) are shown, but no corpus warning ties them to a mistake. Do you expect students to write these calls from memory?

## Chapter 2

1. Slides 28 and 29 (Opposite Day, capacity calculator) have no closing warning on the slide; the warnings are in the corpus only (the program that can never print Today is Opposite Day; the unit == 'TB' or 'tb' slip). Did you stress these in class?
2. The match statement (slides 34 to 36) is covered at length, but the corpus warns more than the deck does (a name in a case is a capture). Is match examinable at the same depth as if and elif?
3. The conditional expression and the walrus are in the deck (slides 32 and 38) but the deck gives no mistake to avoid. Examinable as recognition only, or as writing?
4. Error kinds (SyntaxError, IndentationError, NameError, TypeError, ZeroDivisionError) are taught in the corpus; the deck mentions only some of them. Which error names must a student know by heart?

## Chapter 3

1. Slides 38 and 39 (Rock, Paper, Scissors) have no stressed point except the three-outcome chain; the corpus warns about the nine written-out combinations. Is the program itself examinable?
2. The dictionary hazards (resizing a dictionary while looping over it, unhashable keys) are named in the corpus but I found no deck slide for them. Are they in the course?
3. The corpus covers the finally clause, KeyboardInterrupt and the exception family; the deck teaches only the Python 3.14 finally warning (slide 40) and Control-C. How far do exceptions go in chapter 3?
4. Slides 11 and 12 (walrus in a loop test, PEP 572 story) repeat chapter 2's walrus. Is the walrus examinable in chapter 3, chapter 2, or both?

## Chapter 4

1. Recursion (RecursionError, base case) is a corpus paragraph, but no slide of the deck teaches it. Is recursion in the course and examinable?
2. Lambda expressions, nested functions, positional-only parameters (slash) and annotations are in the corpus; the deck shows the slash and star only in a table (slide 43) and one star example (slide 15). Which of these are examinable?
3. The call stack and frame objects (slides 19 and 20, inspect and sys._getframe) are shown with code, while the corpus says they are a technical detail. Must students write that code, or only explain the stack?
4. Slides 39 and 40 (Zigzag, Spike) have no stressed point or warning. Are these programs examinable?
5. The deck says the book prints 'referenced before assignment' while Python 3.14 prints a new wording (slide 43). Should an exam item name the message text, or only the error class?
