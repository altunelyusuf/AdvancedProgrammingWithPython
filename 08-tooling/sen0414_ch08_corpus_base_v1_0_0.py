#!/usr/bin/env python3
"""SEN0414 chapter 8 (Manipulating Strings, 3rd edition) - the shared base of the corpus, version 1.0.0.

Holds what every text module of the chapter shares: the facet names, the containers RAW / CHECKS / RAISES, the chapter's
whole programs as text (the single source the corpus checks, the deck, the page's Code Lab and the question bank all
read), and the citation tokens. Nothing in this file is taught text; the paragraphs are in
sen0414_ch08_corpus_text_a/b/c_v1_0_0.py. Written fresh for this chapter (not copied from another chapter's base).

Sources read for this chapter, on 2026-10-11: the book chapter (automatetheboringstuff.com/3e/chapter8.html); the Python
3.14 documentation (Text Sequence Type str; string methods; String Formatting; f-strings and the Formatted String
Literals grammar; the codecs and io documentation on encodings; the Unicode HOWTO). Every behaviour quoted is executed
(python3.14 sen0414_ch08_corpus_v1_0_0.py python3.14).
"""
__version__ = "1.0.0"

W, Y, E, H, K, C = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out", "What changed"
CITE = {"[SW]": "(Sweigart, 2025)", "[PSF]": "(Python Software Foundation, 2026)", "[PEP498]": "(Smith, 2015)",
        "[PEP701]": "(Jelle Zijlstra and Pablo Galindo, 2023)", "[PEP750]": "(Jelle Zijlstra et al., 2024)",
        "[UNIC]": "(Unicode Consortium, 2026)"}

RAW = []      # the nodes with citation tokens such as [SW] and [PSF]; the main corpus module resolves them
CHECKS = []   # (expression, repr of its value) pairs, all executed
RAISES = []   # (expression, exception class name) pairs, all executed


def PROG(code, expected, stream="stdout", inp=None):
    """a whole program run as a separate process (python -c); the expected text is the stream named"""
    return ("__import__('subprocess').run([__import__('sys').executable, '-c', %r], capture_output=True, text=True, input=%r).%s" % (code, inp, stream), repr(expected))


# ---------------------------------------------------------------------------------------------------------------------------------
# The chapter's whole programs. Each is the book's program with comments added (the logic is unchanged); the sample inputs
# and the outputs are produced by running them, never typed.
# ---------------------------------------------------------------------------------------------------------------------------------
BULLET_POINT_ADDER = """import pyperclip

text = pyperclip.paste()          # get the text off the clipboard
lines = text.split('\\n')          # break it into a list of lines

for i in range(len(lines)):       # add a bullet to every line
    lines[i] = '* ' + lines[i]

text = '\\n'.join(lines)           # join the lines back into one string
pyperclip.copy(text)              # put the result back on the clipboard
"""

ALTERNATING_CASE = """def alternate_case(text):
    result = ''
    for i, character in enumerate(text):     # i counts 0, 1, 2, ... as the loop walks the string
        if i % 2 == 0:
            result = result + character.lower()
        else:
            result = result + character.upper()
    return result

print(alternate_case('Hello, world!'))
"""
ALTERNATING_CASE_OUT = "hElLo, WoRlD!\n"

INPUT_VALIDATION = """def ask_age():
    while True:
        print('Enter your age:')
        age = input()
        if age.isdecimal():
            return age
        print('Please enter a whole number for your age.')

def ask_password():
    while True:
        print('Select a new password (letters and numbers only):')
        password = input()
        if password.isalnum():
            return password
        print('Passwords can only have letters and numbers.')
"""

PIG_LATIN = """def is_vowel(letter):
    return letter.lower() in list('aeiouy')

text = input('Enter the text to translate into Pig Latin: ')
words = text.split()
new_words = []

for word in words:
    prefix_letters = ''                 # punctuation kept at the front, e.g. a quote mark
    while len(word) > 0 and not word[0].isalpha():
        prefix_letters = prefix_letters + word[0]
        word = word[1:]
    suffix_letters = ''                  # punctuation kept at the end, e.g. a full stop
    while len(word) > 0 and not word[-1].isalpha():
        suffix_letters = suffix_letters + word[-1]
        word = word[:-1]
    if word == '':
        new_words.append(prefix_letters + suffix_letters)
        continue

    was_upper = word.isupper()
    was_title = word[0].isupper()
    word = word.lower()

    if is_vowel(word[0]):
        new_word = word + 'yay'          # starts with a vowel: just add yay
    else:
        prefix_consonants = ''
        while len(word) > 0 and not is_vowel(word[0]):
            prefix_consonants = prefix_consonants + word[0]
            word = word[1:]
        new_word = word + prefix_consonants + 'ay'   # move the consonants to the end, add ay

    if was_upper:
        new_word = new_word.upper()
    elif was_title:
        new_word = new_word[0].upper() + new_word[1:]

    new_words.append(prefix_letters + new_word + suffix_letters)

print(' '.join(new_words))
"""
PIG_LATIN_INPUT = "My name is Al Sweigart. I am 4,000 years old.\n"
PIG_LATIN_OUT = "Enter the text to translate into Pig Latin: Ymay amenay isyay Alyay Eigartsway. IYAY amyay 4,000 yearsyay oldyay.\n"

TABLE_PRINTER = """def print_table(table_data):
    col_widths = [0] * len(table_data)         # the widest string of each column, so far 0
    for i in range(len(table_data)):
        for j in range(len(table_data[i])):
            col_widths[i] = max(col_widths[i], len(table_data[i][j]))

    for row_index in range(len(table_data[0])):
        row = ''
        for col_index in range(len(table_data)):
            item = table_data[col_index][row_index].rjust(col_widths[col_index])
            row = row + item + ' '
        print(row)

table_data = [['apples', 'oranges', 'cherries', 'banana'],
              ['Alice', 'Bob', 'Carol', 'David'],
              ['dogs', 'cats', 'moose', 'goose']]
print_table(table_data)
"""
TABLE_PRINTER_OUT = ("  apples Alice  dogs \n oranges   Bob  cats \ncherries Carol moose \n  banana David goose \n")

PROGRAMS = {
    "bulletPointAdder_v1_0_0.py": (BULLET_POINT_ADDER, None, None),
    "alternateCase_v1_0_0.py": (ALTERNATING_CASE, None, ALTERNATING_CASE_OUT),
    "pigLatin_v1_0_0.py": (PIG_LATIN, PIG_LATIN_INPUT, PIG_LATIN_OUT),
    "tablePrinter_v1_0_0.py": (TABLE_PRINTER, None, TABLE_PRINTER_OUT),
}
