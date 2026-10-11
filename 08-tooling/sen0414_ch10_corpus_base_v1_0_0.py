#!/usr/bin/env python3
"""SEN0414 chapter 10 (Reading and Writing Files, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read, mirroring
the shape of sen0414_ch09_corpus_base_v1_0_0.py (written fresh for this chapter, not copied from another chapter's
base).

Every program below writes its files inside a temporary directory it creates and removes itself, rather than the
real working directory, which has no files for the quiz or Mad Libs programs to find; nothing about the chapter's
own file-handling logic is changed by this, and the chapter's own working-directory concept is exactly what decides
where a plain filename such as 'capitalsquiz1.txt' is read from and written to.

The quiz program (Project 4 of the chapter) keeps the book's own printed quirk exactly as the chapter's research
record found it when run literally: the header is written as '(Form{n})' with no space before the number, the
question is written as 'Capital of <state>:' rather than the chapter's own prose wording 'What is the capital of
<state>?', and the answer key is written with '%d.%s' % (...), joined with no separating newline at all - a real
difference between the chapter's prose and its own listed code, not a bug introduced here. NUM_QUIZZES is reduced
from the chapter's own 35 to 2, only so the transcript shown in the deck and the Lab tab stays short; the per-quiz
logic, including the quirk, is otherwise exactly the chapter's own.

Sources read for this chapter, on 2026-10-01: the book chapter (automatetheboringstuff.com/3e/chapter10.html); the
Python 3.14 documentation (pathlib, os, os.path, shelve, dbm, json, io). Every behaviour quoted is executed
(python3.14 against the programs below).
"""
__version__ = "1.0.0"

# ---------------------------------------------------------------------------------------------------------------------------------
# Practice program 1: Mad Libs, with a text file read, a regex substitution callback, and the result saved back out.
# ---------------------------------------------------------------------------------------------------------------------------------
MAD_LIBS = r"""import os
import re
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as folder:
    os.chdir(folder)
    source = Path('panda.txt')
    source.write_text(
        'The ADJECTIVE panda walked to the NOUN and then VERB. A nearby NOUN was\n'
        'unaffected by these events.', encoding='utf-8')

    text = source.read_text(encoding='utf-8')

    def ask(match):
        word = match.group(1)
        article = 'an' if word[0] in 'AEIOU' else 'a'
        return input(f'Enter {article} {word.lower()}: ')

    result = re.sub(r'\b(ADJECTIVE|NOUN|ADVERB|VERB)\b', ask, text)

    target = Path('panda_filled.txt')
    target.write_text(result, encoding='utf-8')

    print(result)
    print(target.name, target.stat().st_size, target.read_text(encoding='utf-8') == result)
"""
MAD_LIBS_INPUT = "silly\nchandelier\nscreamed\npickup truck\n"

# ---------------------------------------------------------------------------------------------------------------------------------
# Practice program 2: open every .txt file of a folder and print each line that matches a regular expression typed
# by the user, with the filename and line number the chapter's own wording asks for.
# ---------------------------------------------------------------------------------------------------------------------------------
REGEX_SEARCH_FILES = r"""import os
import re
import tempfile
from pathlib import Path


def find_matches(folder, pattern):
    regex = re.compile(pattern)
    matches = []
    for path in sorted(Path(folder).glob('*.txt')):
        with open(path, encoding='utf-8') as text_file:
            for number, line in enumerate(text_file, start=1):
                if regex.search(line):
                    matches.append(f'{path.name}:{number}: {line.rstrip()}')
    return matches


with tempfile.TemporaryDirectory() as folder:
    os.chdir(folder)
    Path('a.txt').write_text('spam and eggs\nbacon alone\nSPAM again\n', encoding='utf-8')
    Path('b.txt').write_text('nothing here\nspam, glorious spam\n', encoding='utf-8')
    Path('notes.csv').write_text('spam,1\n', encoding='utf-8')

    pattern = input('Enter a regular expression to search for: ')
    for line in find_matches(folder, pattern):
        print(line)
"""
REGEX_SEARCH_FILES_INPUT = "spam\n"

# ---------------------------------------------------------------------------------------------------------------------------------
# Project 4: Generating Random Quiz Files, run as the chapter's own listing gives it, its printed quirk kept exactly
# as the research record found (see the module docstring).
# ---------------------------------------------------------------------------------------------------------------------------------
CAPITALS_QUIZ = r"""import os
import random
import tempfile
from pathlib import Path

capitals = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix',
            'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver',
            'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee',
            'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise',
            'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines',
            'Kansas': 'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge',
            'Maine': 'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston',
            'Michigan': 'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson',
            'Missouri': 'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln',
            'Nevada': 'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton',
            'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh',
            'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
            'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence',
            'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee': 'Nashville',
            'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont': 'Montpelier',
            'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston',
            'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

NUM_QUIZZES = 2  # the chapter's own listing makes 35; this demonstration makes 2 (see the module docstring)

random.seed(10)  # fixed only for this repeatable demonstration; the chapter's own program carries no seed

with tempfile.TemporaryDirectory() as folder:
    os.chdir(folder)

    for quiz_num in range(NUM_QUIZZES):
        quiz_file = open(f'capitalsquiz{quiz_num + 1}.txt', 'w', encoding='UTF-8')
        answer_key_file = open(f'capitalsquiz_answers{quiz_num + 1}.txt', 'w', encoding='UTF-8')

        quiz_file.write('Name:\n\nDate:\n\nPeriod:\n\n')
        quiz_file.write((' ' * 20) + f'State Capitals Quiz (Form{quiz_num + 1})')
        quiz_file.write('\n\n')

        states = list(capitals.keys())
        random.shuffle(states)

        for question_num in range(len(states)):
            correct_capital = capitals[states[question_num]]
            wrong_answers = list(capitals.values())
            del wrong_answers[wrong_answers.index(correct_capital)]
            wrong_answers = random.sample(wrong_answers, 3)
            answer_options = wrong_answers + [correct_capital]
            random.shuffle(answer_options)

            quiz_file.write(f'{question_num + 1}. Capital of {states[question_num]}:\n')
            for i in range(4):
                quiz_file.write(f"    {'ABCD'[i]}. {answer_options[i]}\n")
            quiz_file.write('\n')

            answer_key_file.write('%d.%s' % (question_num + 1, 'ABCD'[answer_options.index(correct_capital)]))

        quiz_file.close()
        answer_key_file.close()

    print(Path('capitalsquiz1.txt').read_text(encoding='UTF-8')[:100])
    print('--- answer key 1, first 20 characters (one unbroken line) ---')
    print(Path('capitalsquiz_answers1.txt').read_text(encoding='UTF-8')[:20])
"""

PROGRAMS = {
    "madLibs_v1_0_0.py": (MAD_LIBS, MAD_LIBS_INPUT, None),
    "regexSearchFiles_v1_0_0.py": (REGEX_SEARCH_FILES, REGEX_SEARCH_FILES_INPUT, None),
    "capitalsQuiz_v1_0_0.py": (CAPITALS_QUIZ, None, None),
}
