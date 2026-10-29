# Critical points of chapters 6 to 8: what could not be found or confirmed (v1.0.0)

For the Owner. Each item is a question that can be answered in one line. Chapter 5 (Debugging) was not read. Sources read: the newest deck of each chapter with slide text, tables and speaker notes (ch06 v3.0.0, ch07 v2.0.0, ch08 v2.0.0); the newest stories of each chapter (v1.0.0); for chapters 6 and 7 the corpus text modules `sen0414_chNN_text_a..d` / `sen0414_ch07_corpus_text_a..c` (the corpus files assemble them). Not read: pictures, drawings and chart data inside the decks (only their titles and captions); the research files under 03-materials/chNN/rdodi/ except the chapter 8 document named below.

## All three chapters

1. Nothing in the repository records what you stressed aloud in the lectures, and the speaker notes are short (two to four sentences per slide; none explains a point at length). Every point in the JSON file rests on a deck stress (title, closing line, repeated, warning), a speaker note, or a corpus or story passage. Which of the 129 points do you want kept, and which dropped?
2. A corpus "watch out" paragraph is a common-mistake warning written for the corpus, not necessarily something you said in class (36 of the 129 points rest on corpus or story text alone). Should corpus-only points count as "explained in the course" for the exams?
3. The practice questions on the closing slides (ch06 slide 47, ch07 slide 44, ch08 slide 47) are listed as one point each. Are they examinable as written, or only as the topic they test?
4. The stories of the decks (names, dates, places) are listed only where a story file states a lesson that the deck also teaches in code. Are story facts such as dates and names themselves examinable?

## Chapter 6 (Lists)

1. Competency question 3 of slide 3 asks which printed results of the book differ in current Python. I found no slide in the deck that names such a difference. Did you teach any, and which?
2. The Magic 8 Ball program keeps four answers on slide 22 but nine answers in the story file (`sen0414_ch06_stories_v1_0_0.py`); the toy has twenty. Which number is the one to examine, if any?
3. The corpus warns about things the deck never shows: a mutable default argument (`def f(items=[])`), the one-item tuple `('hello',)`, the argument order of insert, and the upper bound of randint. Did you explain these in class?
4. Slide 44 prints a streak estimate of 81.48 per cent that depends on the fixed seed. Is the number itself to be remembered, or only that streaks are common?
5. Slides 41 and 42 (Matrix digital rain, list of counters) and slides 21 and 22 (Magic 8 Ball) are programs and stories without a closing warning. Are the programs examinable as code to read or write?
6. The corpus has a concept for the `reverse()` method, but the deck shows only `reverse=True` (slide 18) and the slice `[::-1]` (slide 9). Is `reverse()` in the course?

## Chapter 7 (Dictionaries)

1. The corpus warns that adding or removing pairs while looping over a dictionary raises an error, and that `dict.fromkeys(labels, [])` shares one list. I found no deck slide for either. Are they in the course?
2. The corpus says an empty `{}` is a dictionary and the empty set is `set()`; no slide shows it. Did you say it in class?
3. Slide 43 lists six things newer than the book (insertion order, merge operators, live views, the hashing rule, TypedDict, match). Are the Python versions and PEP numbers (3.7, 3.9, 3.8, 3.10, PEP 584, 589, 634) examinable, or only the behaviour?
4. Slides 41 and 42 (TypedDict, MappingProxyType, match with a dictionary) are teaching beyond the book. Are they in the exam scope at the same depth as slides 5 to 16?
5. The character count of slide 21 (73 characters, 23 different) and the totals of slides 33 and 34 (49 and 47) are results of the run. Must students know these numbers?
6. The picnic, chessboard validator and inventory slides (31 to 34) have closing lines but no common-mistake warning in the deck. Is a student expected to write these programs from memory?

## Chapter 8 (Strings)

1. The corpus files of chapter 8 are missing from the repository: `08-tooling/sen0414_ch08_corpus_v1_0_0.py` and `sen0414_ch08_corpus_text_a/b/c_v1_0_0.py` do not exist (only `sen0414_ch08_corpus_base_v1_0_0.py`, which holds no taught text). I used the built chapter document `03-materials/ch08/rdodi/sen0414_ch08_document_v1_1_1.ttl` as the corpus text of chapter 8 (6 points, marked `corpus`). Is that source accepted, or can you supply the corpus files?
2. The `%` operator trap (a single tuple on the right), `casefold` against `lower`, and decoding with the wrong encoding are in the corpus text only; slide 18 shows `%` but not its trap. Did you explain them in class?
3. Slide 37 says Python prints 15 and 8 spaces where the book printed 14 and 9 (the numbers are in the speaker note). Must students know the numbers, or only to run the book's lines and trust the run?
4. Slide 45 lists features newer than the book (f-string debug specifier 3.8, removeprefix 3.9, PEP 701 in 3.12, template strings PEP 750 in 3.14, UTF-8 mode PEP 686 in 3.15). Are version numbers and PEP numbers examinable, or only the behaviour?
5. Slide 44 uses a list as a stand-in for the clipboard because pyperclip is not installed everywhere. Is pyperclip examinable at all?
6. The Pig Latin program on slide 41 is a shortened lambda version of the book's program (vowels `aeiouy`, `yay` for vowel-start words), while the corpus base holds the longer book version. Which of the two is the one to examine?
