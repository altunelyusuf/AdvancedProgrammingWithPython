#!/usr/bin/env python3
"""SEN0414 chapter 9 (Text Pattern Matching with Regular Expressions, 3rd edition) - the shared base of the
corpus, version 1.0.0.

Holds the chapter's whole programs as text, the single source the deck and the page's Lab tab both read. Written
fresh for this chapter (not copied from another chapter's base), mirroring the shape of
sen0414_ch08_corpus_base_v1_0_0.py.

Project 3's own clipboard calls are replaced by a plain text variable standing in for the clipboard's contents,
exactly as chapter 8's bulletPointAdder.py was run against a stand-in in this same build environment, which has no
desktop clipboard at all; nothing about the regular-expression logic itself is changed by this substitution.

Sources read for this chapter, on 2026-10-01: the book chapter (automatetheboringstuff.com/3e/chapter9.html); the
Python 3.14 documentation (re - Regular expression operations; the regex HOWTO). Every behaviour quoted is executed
(python3.14 against the programs below).
"""
__version__ = "1.0.0"

# ---------------------------------------------------------------------------------------------------------------------------------
# Project 3: Extract Contact Information from Large Documents, with its own printed quirk (joining group 6, the whole
# extension clause, rather than group 8, the extension digits alone) kept exactly as the chapter prints it.
# ---------------------------------------------------------------------------------------------------------------------------------
CONTACT_EXTRACTOR = r"""import re

phoneRegex = re.compile(r'''(
    (\d{3}|\(\d{3}\))?            # area code
    (\s|-|\.)?                    # separator
    (\d{3})                       # first 3 digits
    (\s|-|\.)                     # separator
    (\d{4})                       # last 4 digits
    (\s*(ext|x|ext\.)\s*(\d{2,5}))?  # extension
    )''', re.VERBOSE)

emailRegex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+      # username
    @                      # @ symbol
    [a-zA-Z0-9.-]+         # domain name
    (\.[a-zA-Z]{2,4})      # dot-something
    )''', re.VERBOSE)

text = ('Call 800-555-7240 or (415) 555-9900 or 415.555.9950 ext. 123 or 555-1234 x99 today. '
        'Email info@nostarch.com, media@nostarch.com, academic@nostarch.com, or info@nostarch.com again.')

matches = []
for groups in phoneRegex.findall(text):
    phoneNum = '-'.join([groups[1], groups[3], groups[5]])
    if groups[6] != '':
        phoneNum += ' x' + groups[6]
    matches.append(phoneNum)
for groups in emailRegex.findall(text):
    matches.append(groups[0])

if len(matches) > 0:
    print('Copied to clipboard:')
    print('\n'.join(matches))
else:
    print('No phone numbers or email addresses found.')
"""

# ---------------------------------------------------------------------------------------------------------------------------------
# Practice program 1: the strong-password check, several small patterns checked together with all().
# ---------------------------------------------------------------------------------------------------------------------------------
STRONG_PASSWORD = r"""import re

def is_strong_password(password):
    rules = (r'.{8}', r'[a-z]', r'[A-Z]', r'\d')
    return all(re.search(rule, password) for rule in rules)

while True:
    print('Enter a new password:')
    password = input()
    if is_strong_password(password):
        print('That password is strong. Accepted.')
        break
    print('Passwords must be at least 8 characters and have a lowercase letter, '
          'an uppercase letter, and a digit.')
"""
STRONG_PASSWORD_INPUT = "password1\nPASSWORD1\nPassword\nSh0rt\nPassw0rdOK\n"

# ---------------------------------------------------------------------------------------------------------------------------------
# Practice program 2: a regex version of strip(), checked against str.strip() itself.
# ---------------------------------------------------------------------------------------------------------------------------------
REGEX_STRIP = r"""import re

def regex_strip(text, chars=None):
    if chars is None:
        pattern = r'^\s+|\s+$'
    else:
        char_class = '[' + re.escape(chars) + ']'
        pattern = '^' + char_class + '+|' + char_class + '+$'
    return re.sub(pattern, '', text)

print(repr(regex_strip('  hi there \n')))
print(repr(regex_strip('xyhixy', 'xy')))
print(repr(regex_strip('[[a]]', '[]')))
"""

PROGRAMS = {
    "contactExtractor_v1_0_0.py": (CONTACT_EXTRACTOR, None, None),
    "strongPasswordDetector_v1_0_0.py": (STRONG_PASSWORD, STRONG_PASSWORD_INPUT, None),
    "regexStrip_v1_0_0.py": (REGEX_STRIP, None, None),
}
