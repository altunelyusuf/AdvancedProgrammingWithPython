"""Chapter 9 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter 9 (Text Pattern Matching with Regular Expressions) was read in full on automatetheboringstuff.com on 2026-10-01
(the page HTML was fetched with curl through the session proxy and converted to text, because the WebFetch tool was not answered),
and checked against the book's own chapter ontology at commit 89f68596 (15 sections, 19 practice questions; the text also has 2 practice programs).
The Python documentation (re, the Regular expression HOWTO, Lexical analysis, What's new in 3.13 and 3.14) was read on docs.python.org
on 2026-10-01; the site then served the 3.14 series as 3.14.8, so a documentation statement was kept only when a run under Python 3.14.4
confirmed it. Humre 1.0.0 (the newest release on PyPI that day) was read from its PyPI JSON record and its source archive
(sha256 469ae0831969e01726049dc463cdba23a571c8d9fa0ecee49ac2d36f5a3290fa), and was executed from that unpacked archive under Python 3.14.4; the
PyPI project page itself answered with a bot challenge and was not read. Every other behaviour was executed under Python 3.14.4 by the checks.
Humre is not part of the Python standard library and is not installed in this environment or in the browser, so the statements about it are
not re-run by the checks and are not run on the page. The book's clipboard program (pyperclip) and its web-page test were NOT executed.
A claim not in this file was not made."""
__version__ = "1.0.0"
CH = 9
DATE = "2026-10-01"
PYVER = "3.14.4"
TITLE = "Regular expressions for an advanced course: chapter 9 of the 3rd edition and today's Python"
QUESTION = ('What does chapter 9 of the 3rd edition teach about text pattern matching with regular expressions and the Humre module, which of its printed outputs and programs still hold under Python 3.14.4, '
 'and what must an advanced course add so that it matches current Python?')
CQS = ('Which part of a pattern decides what is matched, which part decides how many times, and which operation of the re module (search, findall, sub) uses the result in which way?',
 'Which printed outputs, programs and statements of the chapter differ in current Python or in the current Humre release, and on what source?')
PUBS = [('P01',
  'Automate the Boring Stuff with Python, 3rd edition - Chapter 9, Text Pattern Matching with Regular Expressions (Al Sweigart, No Starch Press, 2025)',
  'https://automatetheboringstuff.com/3e/chapter9.html',
  True),
 ('P02', 'The Python Standard Library, re - Regular expression operations (Python documentation, 3.14 series)', 'https://docs.python.org/3/library/re.html', False),
 ('P03', 'Regular expression HOWTO - match versus search, greedy versus non-greedy, use string methods (Python documentation, 3.14 series)', 'https://docs.python.org/3/howto/regex.html', False),
 ('P04',
  'The Python Language Reference, 2. Lexical analysis - raw string literals and invalid escape sequences (Python documentation, 3.14 series)',
  'https://docs.python.org/3/reference/lexical_analysis.html',
  False),
 ('P05', "What's new in Python 3.14 - the re module: the z escape and the B escape on empty input (Python documentation)", 'https://docs.python.org/3/whatsnew/3.14.html', False),
 ('P06', "What's new in Python 3.13 - re.error renamed PatternError (Python documentation)", 'https://docs.python.org/3/whatsnew/3.13.html', False),
 ('P07', 'Humre 1.0.0 - a human-readable regular expression module for Python (Al Sweigart, Python Package Index, source archive and JSON record)', 'https://pypi.org/project/Humre/', False)]
CONCEPTS = [('Section', 'Finding Text Patterns Without Regular Expressions'),
 ('Section', 'Finding Text Patterns with Regular Expressions'),
 ('Section', 'The Syntax of Regular Expressions'),
 ('Section', 'Qualifier Syntax: What Characters to Match'),
 ('Section', 'Quantifier Syntax: How Many Qualifiers to Match'),
 ('Section', 'Greedy and Non-greedy Matching'),
 ('Section', 'Matching at the Start and End of a String'),
 ('Section', 'Case-Insensitive Matching'),
 ('Section', 'Substituting Strings'),
 ('Section', 'Managing Complex Regexes with Verbose Mode'),
 ('Section', 'Combining re.IGNORECASE, re.DOTALL, and re.VERBOSE'),
 ('Section', 'Humre: A Module for Human-Readable Regexes'),
 ('Section', 'Summary'),
 ('Section', 'Practice Questions'),
 ('Section', 'Practice Programs'),
 ('Project', 'Project 3: Extract Contact Information from Large Documents'),
 ('Concept', 'Regular expression'),
 ('Concept', 'Match object'),
 ('Concept', 'Groups'),
 ('Concept', 'Finding every match'),
 ('Concept', 'Substitution'),
 ('Method', 're.compile'),
 ('Method', 'search'),
 ('Method', 'findall'),
 ('Method', 'group'),
 ('Method', 'groups'),
 ('Method', 'sub'),
 ('Function', 'is_phone_number()'),
 ('Function', 'isdecimal()')]
FINDINGS = [('F1',
  'Background',
  'Chapter 9 of the 3rd edition, Text Pattern Matching with Regular Expressions, builds a phone-number check by hand with is_phone_number() and a 12-character window, then teaches the re module: '
  're.compile() gives a Pattern object, search() a Match object, group() and groups() the matched text, with parentheses for groups, backslash escapes, the pipe for alternatives, findall() for every '
  'match (strings without groups, tuples with groups, no overlap), character classes and their negation, the shorthand classes \\d \\w \\s and their capitals, the dot, the quantifiers ? * + {n} '
  '{n,m}, greedy and non-greedy matching, .* and .*?, re.DOTALL, the anchors ^ $ and the boundaries \\b \\B, re.IGNORECASE, sub() with back references such as \\1, verbose mode, and the combination '
  'of flags with the pipe; Project 3 extracts phone numbers and e-mail addresses through the clipboard with pyperclip; the Humre module writes the same patterns in plain English; the chapter closes '
  'with 19 practice questions and 2 practice programs, a strong-password check and a regex version of strip().',
  ['P01']),
 ('F2',
  'Comparative analysis',
  'Most printed outputs of the chapter reproduce under Python 3.14.4: the is_phone_number() program and the window search, the group, groups, findall and non-overlap examples, the vowel and '
  'consonant lists, the twelve days of Christmas list, the dot examples, the optional, curly-bracket, greedy and lazy examples, DOTALL, the anchors and boundaries, the case-insensitive examples and '
  'both sub() examples; three statements do not reproduce as printed: the error type of an unbalanced parenthesis is named PatternError in 3.14.4 (re.error is an alias kept since 3.13) while the '
  'message text is the one the chapter prints; the star and plus examples use the patterns Eggs(and spam)* and Eggs(and spam)+ without a space before and, so Eggs and spam matches only Eggs, span '
  '(0, 4), with the star and nothing with the plus, where the chapter prints the spans (0, 13), (0, 22) and (0, 31) that the patterns Eggs( and spam)* and Eggs( and spam)+ give; and Project 3 joins '
  'groups 1, 3, 5 and 6 of the phone pattern, but group 6 is the whole extension text, so a number with an extension prints as 415-555-9950 x ext. 123, a number in parentheses keeps them as '
  '(415)-555-9900 and a number without an area code starts with a hyphen, while the extension digits are group 8.',
  ['P01', 'P02']),
 ('F3',
  'Comparative analysis',
  'The chapter describes the shorthand classes for digits, letters and spaces more narrowly than the documentation: \\d is any Unicode decimal digit, not only 0 to 9, \\w is any Unicode alphanumeric '
  'character or the underscore, \\s is any character that str.isspace() accepts, including carriage return, form feed, vertical tab and the non-breaking space, and all four restrict to ASCII under '
  're.ASCII; a word boundary \\b lies between a word character and a non-word character, so digits and underscores belong to words; and with re.IGNORECASE the unicode classes [a-z] and [A-Z] also '
  'match four non-ASCII letters.',
  ['P01', 'P02']),
 ('F4',
  'Comparative analysis',
  'The chapter says that the dollar sign requires the string to end with the pattern; the documentation says it matches at the end of the string or just before the newline at the end, so ^\\d+$ '
  "matches '123\\n' while fullmatch does not, that \\Z matches only at the very end, and that \\z, added in Python 3.14, is its synonym; the same release changed \\B so that it now matches the empty "
  "string, where re.findall(r'\\B', '') was [] before and is [''] in 3.14.4.",
  ['P01', 'P02', 'P05']),
 ('F5',
  'Comparative analysis',
  'The chapter describes sub() as taking the replacement and then the string of the regular expression; the documentation gives Pattern.sub(repl, string, count=0), so the second argument is the text '
  'to search, the replacement may be a function as well as a string, and since Python 3.13 passing count or flags positionally to re.sub() or maxsplit positionally to re.split() is deprecated and '
  "raises a DeprecationWarning; the chapter's raw-string advice is backed by the language reference, where an unrecognised escape such as '\\d' in an ordinary string already draws a SyntaxWarning "
  'and will become a SyntaxError.',
  ['P01', 'P02', 'P04']),
 ('F6',
  'Contemporary developments',
  'Current Python gives the re module more than the chapter presents: match() and fullmatch() beside search(), finditer() with start, end and span, split(), subn(), escape(), named groups, '
  'non-capturing groups, back references inside a pattern, lookahead and lookbehind assertions, possessive quantifiers and atomic groups since 3.11, inline flags such as (?i) that must come first, '
  're.NOFLAG, the flags MULTILINE and ASCII, and the practice the HOWTO recommends of preferring search() to match() with a leading .* and string methods to regular expressions for fixed text.',
  ['P02', 'P03']),
 ('F7',
  'Contemporary developments',
  "Humre 1.0.0, the newest release on the Python Package Index on 2026-10-01, reproduces all 27 rows of the chapter's Tables 9-2 and 9-3, its multi-argument group(DIGIT, PERIOD, DIGIT) example and "
  'the phone-number regex string printed at the end of the chapter, but differs from the chapter elsewhere: the constants DOLLAR_SIGN, HASHTAG, ANY_SINGLE, ANYTHING_LAZY, ANYTHING_GREEDY, '
  'SOMETHING_LAZY and SOMETHING_GREEDY do not exist and the release names DOLLAR, HASH_TAG, ANYCHAR, ANYTHING (which is the lazy .*?), EVERYTHING (the greedy .*) and SOMETHING (the lazy .+?), and '
  'humre.parse() is not implemented: its body is a TODO and it returns None, where the chapter prints the generated source code; Humre is not in the standard library and is not installed for the '
  'page.',
  ['P01', 'P07']),
 ('F8',
  'Conclusion',
  'For an advanced course, chapter 9 is best taught by separating what a pattern matches (character classes, shorthand classes, the dot, anchors), how many times (the quantifiers and their lazy '
  'forms), what is kept (groups and their numbers) and what is done with the result (search, findall, finditer, sub, split): its printed outputs hold under 3.14.4 except the Eggs examples, the '
  'extension index of Project 3 and the name of the error, and the course should add fullmatch, named groups, the Unicode meaning of the shorthand classes, the newline behaviour of the dollar sign, '
  'sub() with a function, the flags and the check of a pattern on real data, while treating Humre as a third-party convenience whose current release differs from the chapter.',
  ['P01', 'P02', 'P03', 'P07'])]
# (top, mid, leaf, exemplar, definition, io-or-None)
TAX = [('FindingPatterns',
  'ManualChecking',
  'ManualPhoneCheck',
  "is_phone_number('415-555-4242')",
  'A pattern can be checked by hand with code that tests the length of a string and then each character in turn, which accepts one exact format and needs a loop over 12-character windows to find a '
  'number inside longer text.',
  ("[m[i:i+12] for m in ['Call me at 415-555-1011 tomorrow. 415-555-9999 is my office.'] for i in range(len(m)) if (lambda t: len(t) == 12 and t[:3].isdecimal() and t[3] == '-' and "
   "t[4:7].isdecimal() and t[7] == '-' and t[8:].isdecimal())(m[i:i+12])]",
   "['415-555-1011', '415-555-9999']")),
 ('FindingPatterns',
  'PatternObjects',
  'RawStrings',
  "r'\\d{3}-\\d{3}-\\d{4}'",
  "A raw string literal, written with the r prefix, keeps every backslash as a character, which is what a regular expression wants; in an ordinary string '\\d' draws a SyntaxWarning and '\\b' is a "
  'backspace character.',
  ("(r'\\d{3}' == '\\\\d{3}', len(r'\\d'), len('\\n'))", '(True, 2, 1)')),
 ('FindingPatterns',
  'PatternObjects',
  'CompileAndSearch',
  're.compile(pattern).search(text)',
  're.compile turns a pattern string into a Pattern object that can be reused, and its search method scans the text and returns a Match object for the first place the pattern fits, or None when it '
  'fits nowhere.',
  ("(lambda re: re.compile(r'\\d{3}-\\d{3}-\\d{4}').search('My number is 415-555-4242.').group())(__import__('re'))", "'415-555-4242'")),
 ('FindingPatterns',
  'PatternObjects',
  'MatchObjectAccess',
  'mo.group(), mo.span()',
  'A Match object holds the matched text, returned by group(), and its position, given by start(), end() and span(); search returns None on failure, so a result must be tested before group is called '
  'on it.',
  ("(lambda re: (lambda m: (m.group(), m.span(), m.start(), m.end(), re.compile(r'\\d{3}').search('no digits')))(re.search(r'\\d{3}-\\d{3}-\\d{4}', 'My number is 415-555-4242.')))(__import__('re'))",
   "('415-555-4242', (13, 25), 13, 25, None)")),
 ('FindingPatterns',
  'PatternObjects',
  'MatchVersusSearch',
  're.match, re.search, re.fullmatch',
  'match finds the pattern only at the start of the text, search finds it anywhere, and fullmatch requires it to cover the whole text; each returns None when the pattern does not fit.',
  ("(lambda re: (re.match('c', 'abcdef'), re.search('c', 'abcdef').span(), re.fullmatch('p.*n', 'python').span(), re.fullmatch('r.*n', 'python')))(__import__('re'))", '(None, (2, 3), (0, 6), None)')),
 ('FindingPatterns',
  'PatternObjects',
  'PatternError',
  're.error',
  'A pattern that is not valid, such as one with an unclosed parenthesis, raises re.PatternError when it is compiled; the name re.error is kept as an alias of that class, and the exception carries '
  'the message, the pattern and the position.',
  ("(lambda re: (re.error is re.PatternError, re.PatternError.__mro__[1].__name__))(__import__('re'))", "(True, 'Exception')")),
 ('PatternSyntax',
  'Grouping',
  'GroupingParentheses',
  '(\\d\\d\\d)-(\\d\\d\\d-\\d\\d\\d\\d)',
  'Parentheses group part of a pattern and number the groups from 1 by their opening parenthesis; group(0) or group() is the whole match, group(1) the first group and groups() a tuple of all groups.',
  ("(lambda re: (lambda m: (m.group(1), m.group(2), m.group(0), m.groups()))(re.search(r'(\\d\\d\\d)-(\\d\\d\\d-\\d\\d\\d\\d)', 'My number is 415-555-4242.')))(__import__('re'))",
   "('415', '555-4242', '415-555-4242', ('415', '555-4242'))")),
 ('PatternSyntax',
  'Grouping',
  'EscapedMetacharacters',
  '\\(\\d\\d\\d\\)',
  'A backslash in front of a special character such as a parenthesis, dot, question mark, star, plus or pipe makes the pattern match that character itself instead of its special meaning.',
  ("(lambda re: re.search(r'(\\(\\d\\d\\d\\)) (\\d\\d\\d-\\d\\d\\d\\d)', 'My phone number is (415) 555-4242.').groups())(__import__('re'))", "('(415)', '555-4242')")),
 ('PatternSyntax',
  'Grouping',
  'Alternation',
  'Cat(erpillar|astrophe|ch|egory)',
  'The pipe offers alternatives; inside parentheses it lets a shared prefix be written once, and the alternatives are tried from left to right, so the first one that fits wins even if a later one '
  'would be longer.',
  ("(lambda re: (re.search(r'Cat(erpillar|astrophe|ch|egory)', 'Catch me if you can.').group(1), re.search('a|ab', 'ab').group(), re.search('ab|a', 'ab').group()))(__import__('re'))",
   "('ch', 'a', 'ab')")),
 ('PatternSyntax',
  'Grouping',
  'NamedGroups',
  '(?P<first>\\w+) (?P<last>\\w+)',
  "A group written (?P<name>...) can be read by its name with group('name'), m['name'] or groupdict() as well as by its number.",
  ("(lambda re: re.match(r'(?P<first>\\w+) (?P<last>\\w+)', 'Malcolm Reynolds').groupdict())(__import__('re'))", "{'first': 'Malcolm', 'last': 'Reynolds'}")),
 ('PatternSyntax',
  'Grouping',
  'BackReferenceInPattern',
  '(\\w+) \\1',
  'Inside a pattern, \\1 to \\99 match the same text that an earlier numbered group matched, which finds repeated words; it repeats the text, not the pattern.',
  ("(lambda re: (re.search(r'\\b(\\w+) \\1\\b', 'this is is a typo').group(), re.search(r'(.+) \\1', 'thethe')))(__import__('re'))", "('is is', None)")),
 ('PatternSyntax',
  'CharacterSets',
  'CharacterClass',
  '[aeiouAEIOU]',
  'Square brackets define a class that matches one character from the set, with ranges such as a-z; ordinary symbols lose their meaning inside it, a range like [A-Za-z] covers only unaccented ASCII '
  'letters, and ^ after the opening bracket negates the class.',
  ("(lambda re: (re.findall(r'[aeiouAEIOU]', 'RoboCop eats BABY FOOD.'), re.search(r'First Name: ([A-Za-z]+)', 'First Name: Sin\\u00e9ad').group(1), re.search(r'First Name: (\\w+)', 'First Name: "
   "Sin\\u00e9ad').group(1)))(__import__('re'))",
   "(['o', 'o', 'o', 'e', 'a', 'A', 'O', 'O'], 'Sin', 'Sinéad')")),
 ('PatternSyntax',
  'CharacterSets',
  'NegativeClass',
  '[^aeiouAEIOU]',
  'A caret just after the opening bracket makes a class that matches any single character not in the set, including spaces, punctuation, digits and newlines.',
  ("(lambda re: ''.join(re.findall(r'[^aeiouAEIOU]', 'RoboCop eats BABY FOOD.')))(__import__('re'))", "'RbCp ts BBY FD.'")),
 ('PatternSyntax',
  'CharacterSets',
  'ShorthandClasses',
  '\\d+\\s\\w+',
  '\\d, \\w and \\s stand for digit, word and whitespace characters and \\D, \\W and \\S for their opposites; they are shorthands for classes, so a quantifier after one repeats that one-character '
  'choice.',
  ("(lambda re: re.findall(r'\\d+\\s\\w+', '12 drummers, 11 pipers, 10 lords'))(__import__('re'))", "['12 drummers', '11 pipers', '10 lords']")),
 ('PatternSyntax',
  'CharacterSets',
  'UnicodeShorthand',
  're.ASCII',
  'For a text pattern \\d matches any Unicode decimal digit and \\w any Unicode letter, digit or underscore, so both reach beyond 0-9 and A-Za-z; the re.ASCII flag narrows \\d, \\w, \\s and \\b to '
  'ASCII.',
  ("(lambda re: (len(re.findall(r'\\d', '1\\u0663\\u096a')), len(re.findall(r'\\d', '1\\u0663\\u096a', re.ASCII)), bool(re.match(r'\\w', '\\u00e9')), bool(re.match(r'\\w', '\\u00e9', "
   "re.ASCII))))(__import__('re'))",
   '(3, 1, True, False)')),
 ('PatternSyntax',
  'CharacterSets',
  'DotCharacter',
  '.at',
  'The dot matches any one character except a newline, so .at fits cat, hat and the lat of flat; a literal period must be escaped.',
  ("(lambda re: re.findall(r'.at', 'The cat in the hat sat on the flat mat.'))(__import__('re'))", "['cat', 'hat', 'sat', 'lat', 'mat']")),
 ('PatternSyntax',
  'Repetition',
  'OptionalQuantifier',
  '42!?',
  'A question mark after the preceding item makes it optional, matching it zero or one time; it applies only to the item directly before it, so 42!? and 42?! are different patterns.',
  ("(lambda re: (re.search(r'42!?', '42').group(), re.search(r'42?!', '4!').group(), re.search(r'42?!', '42')))(__import__('re'))", "('42', '4!', None)")),
 ('PatternSyntax',
  'Repetition',
  'StarQuantifier',
  'Eggs( and spam)*',
  'A star after an item matches it zero or more times, so the repeated part may be absent.',
  ("(lambda re: [re.search(r'Eggs( and spam)*', s).group() for s in ('Eggs', 'Eggs and spam', 'Eggs and spam and spam')])(__import__('re'))", "['Eggs', 'Eggs and spam', 'Eggs and spam and spam']")),
 ('PatternSyntax',
  'Repetition',
  'PlusQuantifier',
  'Eggs( and spam)+',
  'A plus after an item matches it one or more times, so the repeated part must appear at least once.',
  ("(lambda re: [re.search(r'Eggs( and spam)+', s) is not None for s in ('Eggs', 'Eggs and spam')])(__import__('re'))", '[False, True]')),
 ('PatternSyntax',
  'Repetition',
  'BraceQuantifier',
  '(Ha){3,5}',
  'Curly brackets state how many times the preceding item repeats: {n} exactly, {n,m} from n to m inclusive, {n,} at least n and {,m} at most m.',
  ("(lambda re: ([re.fullmatch(r'(Ha){3,5}', 'Ha' * n) is not None for n in range(2, 7)], re.fullmatch(r'(Ha){,5}', '') is not None, re.fullmatch(r'(Ha){3}', 'HaHa')))(__import__('re'))",
   '([False, True, True, True, False], True, None)')),
 ('PatternSyntax',
  'Repetition',
  'GreedyAndLazy',
  '(Ha){3,5}?',
  'A quantifier is greedy and takes as many repetitions as it can; a question mark after it makes it lazy, so it takes as few as will still let the whole pattern match.',
  ("(lambda re: (re.search(r'(Ha){3,5}', 'HaHaHaHaHa').group(), re.search(r'(Ha){3,5}?', 'HaHaHaHaHa').group()))(__import__('re'))", "('HaHaHaHaHa', 'HaHaHa')")),
 ('PatternSyntax',
  'Repetition',
  'DotStar',
  '<.*?>',
  'The dot followed by a star matches any run of characters on one line; greedy .* runs to the last possible end and lazy .*? stops at the first.',
  ("(lambda re: (re.search(r'<.*?>', '<To serve man> for dinner.>').group(), re.search(r'<.*>', '<To serve man> for dinner.>').group()))(__import__('re'))",
   "('<To serve man>', '<To serve man> for dinner.>')")),
 ('PatternSyntax',
  'Anchors',
  'StartEndAnchors',
  '^\\d+$',
  'A caret at the start of a pattern requires the match to begin at the beginning of the text and a dollar sign at the end requires it to end there, so both together ask the whole string to fit.',
  ("(lambda re: (re.search(r'^\\d+$', '1234567890').span(), re.search(r'^\\d+$', '12345xyz67890'), re.search(r'^Hello', 'Say Hello.')))(__import__('re'))", '((0, 10), None, None)')),
 ('PatternSyntax',
  'Anchors',
  'WordBoundary',
  '\\bcat.*?\\b',
  '\\b matches the empty position between a word character and a non-word character, or the edge of the text, and \\B matches where there is no such boundary.',
  ("(lambda re: (re.findall(r'\\bcat.*?\\b', 'The cat found a catapult catalog in the catacombs.'), re.findall(r'\\Bcat\\B', 'certificate'), re.findall(r'\\Bcat\\B', "
   "'catastrophe')))(__import__('re'))",
   "(['cat', 'catapult', 'catalog', 'catacombs'], ['cat'], [])")),
 ('PatternSyntax',
  'Anchors',
  'DollarBeforeNewline',
  '\\Z',
  "A dollar sign matches at the end of the text and also just before a newline that ends the text, so ^\\d+$ fits '123\\n'; \\Z matches only at the very end, and with re.MULTILINE ^ and $ also fit "
  'at every line.',
  ("(lambda re: (re.search(r'^\\d+$', '123\\n') is not None, re.fullmatch(r'\\d+', '123\\n'), re.search(r'^\\d+\\Z', '123\\n'), re.findall(r'^\\w+', 'one\\ntwo'), re.findall(r'^\\w+', 'one\\ntwo', "
   "re.M)))(__import__('re'))",
   "(True, None, None, ['one'], ['one', 'two'])")),
 ('PatternSyntax',
  'Anchors',
  'LookAround',
  '\\d+(?= dollars)',
  'A lookahead such as (?=...) or a lookbehind such as (?<=...) checks the text next to a position without using it up, so the check is not part of the match.',
  ("(lambda re: (re.findall(r'\\d+(?= dollars)', '5 dollars and 7 euros'), re.findall(r'(?<=\\$)\\d+', 'cost $30 or 40')))(__import__('re'))", "(['5'], ['30'])")),
 ('PatternOperations',
  'Finding',
  'FindallMethod',
  'pattern.findall(text)',
  'findall returns every non-overlapping match in order: a list of strings when the pattern has no group or one group (the text of that group), and a list of tuples of the group texts when it has '
  'two or more.',
  ("(lambda re: (re.findall(r'\\d{3}-\\d{3}-\\d{4}', 'Cell: 415-555-9999 Work: 212-555-0000'), re.findall(r'(\\d{3})-(\\d{3})-(\\d{4})', 'Cell: 415-555-9999 Work: 212-555-0000'), "
   "re.findall(r'(\\w+)=(\\d+)', 'set width=20 and height=10'), re.findall(r'(\\d)\\d', '1234')))(__import__('re'))",
   "(['415-555-9999', '212-555-0000'], [('415', '555', '9999'), ('212', '555', '0000')], [('width', '20'), ('height', '10')], ['1', '3'])")),
 ('PatternOperations',
  'Finding',
  'FindallNoOverlap',
  "re.compile(r'\\d{3}').findall('1234')",
  "findall continues after the end of each match, so text already matched is not matched again and r'\\d{3}' finds one three-digit run in '1234' and in '12345'.",
  ("(lambda re: [re.findall(r'\\d{3}', s) for s in ('1234', '12345', '123456')])(__import__('re'))", "[['123'], ['123'], ['123', '456']]")),
 ('PatternOperations',
  'Finding',
  'FinditerMethod',
  're.finditer(pattern, text)',
  'finditer yields a Match object for each non-overlapping match, which gives positions through start(), end() and span() as well as the text.',
  ("(lambda re: [(m.start(), m.end(), m.group()) for m in re.finditer(r'\\w+ly\\b', 'He was carefully disguised but captured quickly by police.')])(__import__('re'))",
   "[(7, 16, 'carefully'), (40, 47, 'quickly')]")),
 ('PatternOperations',
  'Replacing',
  'SubMethod',
  "pattern.sub('CENSORED', text)",
  'sub returns a new string in which every match is replaced; its first argument is the replacement and its second is the text to search, and the original text is not changed.',
  ("(lambda re: re.compile(r'Agent \\w+').sub('CENSORED', 'Agent Alice contacted Agent Bob.'))(__import__('re'))", "'CENSORED contacted CENSORED.'")),
 ('PatternOperations',
  'Replacing',
  'SubBackReference',
  "r'\\1****'",
  'In a replacement string \\1, \\2 and so on insert the text of a group of the match, and \\g<name> or \\g<0> insert a named group or the whole match.',
  ("(lambda re: (re.compile(r'Agent (\\w)\\w*').sub(r'\\1****', 'Agent Alice contacted Agent Bob.'), re.sub(r'(?P<w>\\w+)@', r'<\\g<w>>@', 'ann@x bob@y')))(__import__('re'))",
   "('A**** contacted B****.', '<ann>@x <bob>@y')")),
 ('PatternOperations',
  'Replacing',
  'SubWithFunction',
  're.sub(pattern, function, text)',
  'When the replacement is a function it is called with each Match object and returns the replacement text, which lets the new text be computed; count limits the number of replacements and subn also '
  'returns how many were made.',
  ("(lambda re: (re.sub(r'\\d+', lambda m: str(int(m.group()) * 2), '3 cats 12 dogs'), re.subn('a', 'A', 'banana', count=2)))(__import__('re'))", "('6 cats 24 dogs', ('bAnAna', 2))")),
 ('PatternOperations',
  'Replacing',
  'EscapeFunction',
  're.escape(text)',
  're.escape puts a backslash before every character of a string that could have a special meaning in a pattern, so text typed by a user can be matched literally.',
  ("(lambda re: (re.escape('a.b*c'), re.search(re.escape('a.b'), 'axb'), re.search('a.b', 'axb').group()))(__import__('re'))", "('a\\\\.b\\\\*c', None, 'axb')")),
 ('PatternOperations',
  'Flags',
  'IgnoreCaseFlag',
  're.compile(p, re.I)',
  'The flag re.IGNORECASE, short re.I, makes letters match in either case; (?i) at the start of a pattern does the same.',
  ("(lambda re: ([re.search('robocop', s, re.I).group() for s in ('RoboCop is part man', 'ROBOCOP protects', 'seen robocop?')], re.search('(?i)robocop', 'ROBOCOP').group()))(__import__('re'))",
   "(['RoboCop', 'ROBOCOP', 'robocop'], 'ROBOCOP')")),
 ('PatternOperations',
  'Flags',
  'DotAllFlag',
  "re.compile('.*', re.DOTALL)",
  'The flag re.DOTALL makes the dot match a newline as well, so .* can run across lines.',
  ("(lambda re: (re.search('.*', 'a\\nb').group(), re.search('.*', 'a\\nb', re.DOTALL).group()))(__import__('re'))", "('a', 'a\\nb')")),
 ('PatternOperations',
  'Flags',
  'VerboseMode',
  're.compile(p, re.VERBOSE)',
  'The flag re.VERBOSE makes the compiler ignore whitespace and comments that start with # inside the pattern, so a long pattern can be written over several lines with notes; a needed space must '
  'then be escaped or put in a class.',
  ("(lambda re: (re.search('\\\\d{3}  # area code\\n-\\\\d{4}  # number', '415-5551', re.X).group(), bool(re.search(r'a b', 'ab', re.X))))(__import__('re'))", "('415-5551', True)")),
 ('PatternOperations',
  'Flags',
  'CombiningFlags',
  're.I | re.S | re.X',
  'Flags are numbers that can be combined with the bitwise or operator written as a pipe, because compile takes one flags argument; re.I | re.S | re.X is a single combined value.',
  ("(lambda re: (int(re.I | re.S | re.X), re.search('A.b', 'a\\nB', re.I | re.S).group()))(__import__('re'))", "(82, 'a\\nB')")),
 ('PatternPrograms',
  'ContactExtractor',
  'PhoneRegex',
  '(\\d{3}|\\(\\d{3}\\))?(\\s|-|\\.)?(\\d{3})(\\s|-|\\.)(\\d{4})',
  "The project's phone pattern has an optional area code with or without parentheses, an optional separator, three digits, a separator, four digits and an optional extension, and it accepts several "
  'formats of the same number.',
  ("(lambda re: [g[0] for g in re.compile(r'((\\d{3}|\\(\\d{3}\\))?(\\s|-|\\.)?(\\d{3})(\\s|-|\\.)(\\d{4})(\\s*(ext|x|ext\\.)\\s*(\\d{2,5}))?)').findall('800-555-7240 or (415) 555-9900 or "
   "415.555.9950 ext. 123')])(__import__('re'))",
   "['800-555-7240', '(415) 555-9900', '415.555.9950 ext. 123']")),
 ('PatternPrograms',
  'ContactExtractor',
  'EmailRegex',
  '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\\.[a-zA-Z]{2,4})',
  "The project's e-mail pattern is a user name, an at sign, a domain name and a dot followed by two to four letters; it matches typical addresses, not every valid one, and cuts a longer ending such "
  'as .museum short.',
  ("(lambda re: ([g[0] for g in re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\\.[a-zA-Z]{2,4}))').findall('info@nostarch.com, media@nostarch.com')], "
   "re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}', 'me@example.museum')))(__import__('re'))",
   "(['info@nostarch.com', 'media@nostarch.com'], ['me@example.muse'])")),
 ('PatternPrograms',
  'ContactExtractor',
  'ExtensionGroupIndex',
  'groups[6]',
  "findall returns the groups in the order of their opening parentheses, so in the project's pattern index 6 is the whole extension part with its spaces and keyword and its digits are at index 8; "
  'counting groups before joining them avoids a wrong index.',
  ("(lambda re: re.compile(r'((\\d{3}|\\(\\d{3}\\))?(\\s|-|\\.)?(\\d{3})(\\s|-|\\.)(\\d{4})(\\s*(ext|x|ext\\.)\\s*(\\d{2,5}))?)').findall('415.555.9950 ext. 123')[0][5:])(__import__('re'))",
   "('9950', ' ext. 123', 'ext.', '123')")),
 ('PatternPrograms',
  'ContactExtractor',
  'ClipboardRoundTrip',
  'pyperclip.paste() and pyperclip.copy()',
  'The project reads the text to search from the clipboard with pyperclip.paste() and writes the joined matches back with pyperclip.copy(); this needs the third-party pyperclip module and a '
  'clipboard, so it was not executed here.',
  None),
 ('PatternPrograms',
  'HumreModule',
  'HumreFunctions',
  'exactly(3, DIGIT)',
  'Humre is a third-party module whose constants and functions, such as DIGIT, exactly, optional_group and either, return ordinary pattern strings that are passed to re.compile; it is not part of '
  'the standard library and was executed here only from its downloaded source archive.',
  None),
 ('PatternPrograms',
  'HumreModule',
  'HumreCompatibility',
  'humre.parse(pattern)',
  'The current Humre release differs from the chapter: several constants of the chapter have other names or do not exist, and humre.parse() is not implemented and returns None; the release was '
  'executed from its source archive, not run on the page.',
  None),
 ('PatternPrograms',
  'PracticeWork',
  'PracticeQuestions',
  "num_re.sub('X', text)",
  "The chapter closes with 19 practice questions about the functions, symbols, flags and methods of the chapter; question 18 asks what sub('X', ...) returns for r'\\d+' applied to a text with "
  'numbers and a written-out number.',
  ("(lambda re: (re.compile(r'\\d+').sub('X', '12 drummers, 11 pipers, five rings, 3 hens'), re.compile(r'\\d+').groups, "
   "re.compile(r'(\\d\\d\\d)-(\\d\\d\\d-\\d\\d\\d\\d)').search('415-555-4242').group(0)))(__import__('re'))",
   "('X drummers, X pipers, five rings, X hens', 0, '415-555-4242')")),
 ('PatternPrograms',
  'PracticeWork',
  'StrongPassword',
  "re.search(r'[A-Z]', password)",
  'A strong-password check is easier as several small patterns, one per rule (length, lowercase, uppercase, digit), all of which must match, than as one pattern.',
  ("(lambda re: [all(re.search(p, s) for p in (r'.{8}', r'[a-z]', r'[A-Z]', r'\\d')) for s in ('Passw0rdOK', 'password1', 'Sh0rt')])(__import__('re'))", '[True, False, False]')),
 ('PatternPrograms',
  'PracticeWork',
  'RegexStrip',
  "re.sub(r'^\\s+|\\s+$', '', text)",
  'A regex version of strip removes matches anchored at the start or the end of the text, using whitespace by default or a class built from the given characters, which must be escaped.',
  ("(lambda re: (lambda s: (re.sub(r'^\\s+|\\s+$', '', s), re.sub('^[xy]+|[xy]+$', '', 'xyhixy'), s.strip()))('  hi there \\n'))(__import__('re'))", "('hi there', 'hi', 'hi there')")),
 ('PatternPrograms',
  'PracticeWork',
  'StringMethodsInstead',
  "text.replace('word', 'deed')",
  'For fixed text, string methods such as replace, translate, startswith and the in operator are simpler and faster than a regular expression, and the HOWTO advises using them before reaching for '
  'the re module.',
  ("('swordfish'.replace('word', 'deed'), 'a\\nb'.translate({10: 32}), 'spam' in 'eggs and spam')", "('sdeedfish', 'a b', True)"))]
ERRORS = []
CLAIMS = [("(lambda re: (re.findall(r'\\B', ''), re.findall(r'\\b', '')))(__import__('re'))", "([''], [])"),
 ("(lambda re: re.findall(r'\\bcat\\b', 'cat_1 cat 1cat'))(__import__('re'))", "['cat']"),
 ("(lambda re: (len(re.findall('[a-z]', '\\u0130\\u0131\\u017f\\u212a', re.I)), len(re.findall('[a-z]', '\\u0130\\u0131\\u017f\\u212a', re.I | re.A))))(__import__('re'))", '(4, 0)'),
 ("(lambda re: [bool(re.match(r'\\s', c)) for c in (' ', '\\t', '\\n', '\\r', '\\f', '\\v', '\\u00a0')])(__import__('re'))", '[True, True, True, True, True, True, True]'),
 ("(lambda re: [hasattr(re, n) for n in ('match', 'fullmatch', 'finditer', 'split', 'subn', 'escape', 'NOFLAG', 'PatternError')])(__import__('re'))",
  '[True, True, True, True, True, True, True, True]'),
 ("(lambda re: (re.compile(r'(a)(b)').groups, dict(re.compile(r'(?P<x>a)').groupindex)))(__import__('re'))", "(2, {'x': 1})"),
 ("(lambda re: (re.compile(r'\\d').sub('#', 'a1b2'), re.compile(r'\\d').sub(lambda m: '<' + m.group() + '>', 'a1b2')))(__import__('re'))", "('a#b#', 'a<1>b<2>')"),
 ("(lambda re: (re.split(r'\\W+', 'Words, words, words.'), re.split(r'(\\W+)', 'Words, words, words.', maxsplit=1)))(__import__('re'))",
  "(['Words', 'words', 'words', ''], ['Words', ', ', 'words, words.'])"),
 ("(lambda re: re.search(r'(Ha){,5}', 'HaHa').group())(__import__('re'))", "'HaHa'"),
 ("(lambda re: (re.search(r'\\d$', '42\\n') is not None, re.search(r'\\d\\Z', '42\\n')))(__import__('re'))", '(True, None)'),
 ("(lambda re: (re.search(r'(?i)robocop', 'RoboCop').group(), re.search(r'(?s:.)', '\\n').group() == '\\n'))(__import__('re'))", "('RoboCop', True)")]
S = "(Sweigart, 2025)"; PSF = "(Python Software Foundation, 2026)"; HUM = "(Sweigart, 2022)"
BODY = {'FindingPatterns': 'The chapter starts from a hand-written check of a phone number and moves to the re module and its Pattern and Match objects (Sweigart, 2025).',
 'ManualChecking': 'The chapter first tests a string by hand, position by position, before it introduces regular expressions (Sweigart, 2025).',
 'ManualPhoneCheck': 'is_phone_number() returns False unless the text has 12 characters, digits in positions 0 to 2, 4 to 6 and 8 to 11 and hyphens in positions 3 and 7, so it is True for '
                     "'415-555-4242' and False for 'Moshi moshi'; looped over every 12-character window of 'Call me at 415-555-1011 tomorrow. 415-555-9999 is my office.' it finds 415-555-1011 and "
                     "415-555-9999 and prints Done, and it is False for '415.555.4242' and '(415) 555-4242', the formats the chapter says it cannot find (Sweigart, 2025).",
 'PatternObjects': 'The re module turns a pattern string into a Pattern object and a search into a Match object (Sweigart, 2025) (Python Software Foundation, 2026).',
 'RawStrings': "The chapter writes patterns as raw strings, r'\\d' having two characters, a backslash and a d, and being equal to '\\\\d' (Sweigart, 2025); the language reference adds that an "
               "unrecognised escape such as '\\d' in an ordinary string draws a SyntaxWarning, and executing it showed that '\\b' in an ordinary string is a backspace character, so re.search('\\b', "
               "'a') finds nothing while re.search(r'\\b', 'a') finds a word boundary (Python Software Foundation, 2026).",
 'CompileAndSearch': 'The four steps are to import re, pass the pattern string to re.compile() for a Pattern object, pass the text to its search() method for a Match object and call group() for the '
                     "text; re.compile(r'\\d{3}-\\d{3}-\\d{4}').search('My number is 415-555-4242.').group() is '415-555-4242', the object is a Pattern, and searching text with no number returns "
                     "None so that calling group() on it raises AttributeError: 'NoneType' object has no attribute 'group' (Sweigart, 2025); compiled patterns of recent calls are cached by the "
                     'module, so a few patterns need no explicit compile, although compiling once is better for a pattern used many times (Python Software Foundation, 2026).',
 'MatchObjectAccess': "For the match of '415-555-4242' in 'My number is 415-555-4242.' group() is the text, span() is (13, 25), start() is 13 and end() is 25, and printing the Match object gives "
                      "<re.Match object; span=(13, 25), match='415-555-4242'>; a pattern that fits nowhere gives None, and a Match object is always true, so if mo: is a safe test (Sweigart, 2025) "
                      '(Python Software Foundation, 2026).',
 'MatchVersusSearch': "re.match('c', 'abcdef') is None because match looks only at the start, re.search('c', 'abcdef') has span (2, 3), re.fullmatch('p.*n', 'python') has span (0, 6) and "
                      "re.fullmatch('r.*n', 'python') is None; the chapter presents only search, and the HOWTO advises search over match with a leading .*, which defeats the compiler's search for "
                      'the first character (Python Software Foundation, 2026).',
 'PatternError': "re.compile(r'(\\(Parentheses\\)') raises PatternError: missing ), unterminated subpattern at position 0 under Python 3.14.4, with msg 'missing ), unterminated subpattern', pos 0 "
                 'and the pattern attached, where the chapter prints re.error with the same message; re.error is re.PatternError is True, because the class was renamed in Python 3.13 and the old '
                 'name kept as an alias (Sweigart, 2025) (Python Software Foundation, 2026).',
 'PatternSyntax': 'A pattern is made of what to match, how many times, where, and which parts to keep (Sweigart, 2025) (Python Software Foundation, 2026).',
 'Grouping': 'Parentheses, backslashes and the pipe structure a pattern and decide which parts can be read afterwards (Sweigart, 2025).',
 'GroupingParentheses': "With (\\d\\d\\d)-(\\d\\d\\d-\\d\\d\\d\\d) on 'My number is 415-555-4242.' group(1) is '415', group(2) is '555-4242', group(0) and group() are '415-555-4242' and groups() is "
                        "('415', '555-4242'), which multiple assignment can split into area_code and main_number (Sweigart, 2025); a group that did not take part in the match gives None, so "
                        "re.match(r'(\\d+)\\.?(\\d+)?', '24').groups() is ('24', None) and groups('0') is ('24', '0'), and a non-capturing group (?:...) groups without numbering, so "
                        "findall(r'(?:\\d{3}-)?\\d{4}', '555-1234 and 9876') gives ['555-1234', '9876'] where the capturing form gives ['555-', ''] (Python Software Foundation, 2026).",
 'EscapedMetacharacters': "To match (415) the chapter escapes the parentheses, (\\(\\d\\d\\d\\)) (\\d\\d\\d-\\d\\d\\d\\d) on 'My phone number is (415) 555-4242.' giving group(1) '(415)' and group(2) "
                          "'555-4242'; the characters with a special meaning are listed as $ ( ) * + - . ? [ \\ ] ^ { | } and an unescaped lone parenthesis is what raises the error 'missing ), "
                          "unterminated subpattern' (Sweigart, 2025); inside square brackets most of them lose their meaning, so [()] matches either parenthesis and [|] matches a pipe (Python "
                          'Software Foundation, 2026).',
 'Alternation': "Cat(erpillar|astrophe|ch|egory) on 'Catch me if you can.' gives group() 'Catch' and group(1) 'ch', r'Cat|Dog' finds Dog in 'I like my Dog', and an actual pipe is written \\| "
                "(Sweigart, 2025); alternatives are tried from left to right and the first that fits is kept, so re.search('a|ab', 'ab').group() is 'a' while re.search('ab|a', 'ab').group() is 'ab' "
                '(Python Software Foundation, 2026).',
 'NamedGroups': "re.match(r'(?P<first_name>\\w+) (?P<last_name>\\w+)', 'Malcolm Reynolds') gives group('first_name') 'Malcolm', m['last_name'] 'Reynolds' and groupdict() {'first_name': 'Malcolm', "
                "'last_name': 'Reynolds'}, and lastgroup is 'last_name'; the chapter as read does not present named groups, though Humre has a named_group function (Sweigart, 2025) (Python Software "
                'Foundation, 2026).',
 'BackReferenceInPattern': "r'\\b(\\w+) \\1\\b' finds the repeated word in 'this is is a typo', returning 'is is', and r'(.+) \\1' matches 'the the' but not 'thethe'; the chapter uses \\1 only in "
                           'the replacement of sub() and lists repeated words as a typo to look for, without this form (Sweigart, 2025) (Python Software Foundation, 2026).',
 'CharacterSets': 'What a single position of the text may be is written as a class, a shorthand or the dot (Sweigart, 2025).',
 'CharacterClass': "[aeiouAEIOU] finds 'o', 'o', 'o', 'e', 'a', 'A', 'O', 'O' in 'RoboCop eats BABY FOOD.', and [()] matches either parenthesis without escapes (Sweigart, 2025); [A-Za-z]+ stops at "
                   "the accented letter, so 'First Name: ([A-Za-z]+)' on 'First Name: Sinéad' gives 'Sin' while (\\w+) gives 'Sinéad', and 'Last Name: (\\w+)' on O’Connor, written with the "
                   "typographic apostrophe, and on O'Connor with the plain one gives 'O' in both, as the chapter warns; the range [A-z] is not the letters, since it also includes [, _ and the other "
                   'characters between Z and a, and with re.IGNORECASE the classes [a-z] and [A-Z] also match four non-ASCII letters (Sweigart, 2025) (Python Software Foundation, 2026).',
 'NegativeClass': "[^aeiouAEIOU] on 'RoboCop eats BABY FOOD.' finds the 15 characters R, b, C, p, a space, t, s, a space, B, B, Y, a space, F, D and the period, so joined they read 'RbCp ts BBY FD.' "
                  '(Sweigart, 2025).',
 'ShorthandClasses': "\\d+\\s\\w+ finds '12 drummers', '11 pipers', '10 lords' and so on in the twelve days of Christmas text, twelve matches in all, where the chapter lists \\d as 0 to 9, \\w as "
                     'letters, digits and the underscore and \\s as space, tab and newline (Sweigart, 2025); in a str pattern \\s matches every character str.isspace() accepts, which includes '
                     'carriage return, form feed, vertical tab and the non-breaking space, all seven of which were tested (Python Software Foundation, 2026).',
 'UnicodeShorthand': "In '1' followed by an Arabic-Indic three and a Devanagari four, \\d finds 3 digits and re.ASCII leaves 1, [0-9] finds 1, and \\w matches the letter é (U+00E9) but not under "
                     're.ASCII or in a bytes pattern; \\s matches the non-breaking space U+00A0 unless re.ASCII is given, and a bytes pattern cannot be used on a str, raising TypeError: cannot use a '
                     'bytes pattern on a string-like object; the chapter states only the 0 to 9 and A-Z meanings (Sweigart, 2025) (Python Software Foundation, 2026).',
 'DotCharacter': ".at finds 'cat', 'hat', 'sat', 'lat' and 'mat' in 'The cat in the hat sat on the flat mat.', the dot matching one character so that flat gives lat, and a period is written \\. "
                 '(Sweigart, 2025).',
 'Repetition': 'A quantifier after a qualifier says how many times it is matched, and a question mark after a quantifier makes it lazy (Sweigart, 2025).',
 'OptionalQuantifier': "42!? matches '42!' with span (0, 3) and '42' with span (0, 2), whereas 42?! means a 4, an optional 2 and a ! so that it matches '42!' and '4!' but not '42'; "
                       "(\\d{3}-)?\\d{3}-\\d{4} finds '415-555-4242' and '555-4242' (Sweigart, 2025).",
 'StarQuantifier': "As printed in the chapter, the pattern 'Eggs(and spam)*' has no space before and, so on 'Eggs', 'Eggs and spam' and 'Eggs and spam and spam' it matches only 'Eggs', span (0, 4) "
                   "each time, and not the spans (0, 13) and (0, 22) the chapter prints; with the space, 'Eggs( and spam)*' gives 'Eggs', 'Eggs and spam' and 'Eggs and spam and spam' and also spans "
                   '(0, 13), (0, 22) and, for three repeats, (0, 31) (Sweigart, 2025).',
 'PlusQuantifier': "As printed, 'Eggs(and spam)+' finds nothing in 'Eggs', 'Eggs and spam' or 'Eggs and spam and spam' because of the missing space, while 'Eggs( and spam)+' gives None for 'Eggs' "
                   "and matches 'Eggs and spam' with span (0, 13) and the two-repeat text with span (0, 22), as the chapter's prose says (Sweigart, 2025).",
 'BraceQuantifier': "(Ha){3} matches 'HaHaHa' and gives None for 'HaHa'; for 0 to 6 repeats of Ha, (Ha){3,5} accepts only 3, 4 and 5, (Ha){3,} accepts 3 or more and (Ha){,5} accepts 0 to 5, so the "
                    'lower bound may be left out as the chapter says, and the upper number is inclusive, unlike a slice (Sweigart, 2025) (Python Software Foundation, 2026).',
 'GreedyAndLazy': "On 'HaHaHaHaHa' the greedy (Ha){3,5} matches 'HaHaHaHaHa' and the lazy (Ha){3,5}? matches 'HaHaHa' (Sweigart, 2025); the documentation adds possessive forms such as a*+, which "
                  "never give characters back, so 'a*a' matches 'aaaa' but 'a*+a' does not (Python Software Foundation, 2026).",
 'DotStar': "'First Name: (.*) Last Name: (.*)' on 'First Name: Al Last Name: Sweigart' gives 'Al' and 'Sweigart'; on '<To serve man> for dinner.>' the lazy <.*?> matches '<To serve man>' and the "
            "greedy <.*> matches the whole string, and on '<html><head><title>Title</title>' the greedy match has span (0, 32) and the lazy one (0, 6) (Sweigart, 2025) (Python Software Foundation, "
            '2026).',
 'Anchors': 'A pattern can be tied to the start or end of the text, to word edges, to line edges or to its surroundings (Sweigart, 2025) (Python Software Foundation, 2026).',
 'StartEndAnchors': '^Hello matches \'Hello, world!\' with span (0, 5) and not \'He said "Hello."\'; \\d$ matches the 2 of \'Your number is 42\' at span (16, 17) and nothing in \'Your number is '
                    "forty two.'; ^\\d+$ matches '1234567890' with span (0, 10) and not '12345xyz67890' (Sweigart, 2025).",
 'WordBoundary': "\\bcat.*?\\b finds 'cat', 'catapult', 'catalog' and 'catacombs' in 'The cat found a catapult catalog in the catacombs.', and \\Bcat\\B finds 'cat' in 'certificate' and nothing in "
                 "'catastrophe' (Sweigart, 2025); the chapter calls a word a run of letters, but the documentation defines it as a run of word characters, so digits and underscores belong to words "
                 "and r'\\bcat\\b' finds only the last cat in 'cat_1 cat 1cat' (Python Software Foundation, 2026).",
 'DollarBeforeNewline': "re.search(r'^\\d+$', '123\\n') matches, because $ also fits just before a final newline, while fullmatch(r'\\d+', '123\\n') and the patterns ending in \\Z and, in Python "
                        "3.14, \\z do not; with re.MULTILINE ^\\w+ finds 'one' and 'two' in 'one\\ntwo' and without it only 'one', and re.findall('$', 'foo\\n') gives two empty matches; the chapter "
                        'says only that $ means the string must end with the pattern (Sweigart, 2025) (Python Software Foundation, 2026).',
 'LookAround': "\\d+(?= dollars) finds '5' in '5 dollars and 7 euros', (?<=\\$)\\d+ finds '30' in 'cost $30 or 40', Isaac (?!Asimov) matches 'Isaac ' in 'Isaac Newton' but nothing in 'Isaac Asimov', "
               'and a lookbehind must have a fixed width, since (?<=a*)b raises PatternError: look-behind requires fixed-width pattern; the chapter as read does not present these forms (Python '
               'Software Foundation, 2026).',
 'PatternOperations': 'The re module finds matches, replaces them and is tuned by flags (Sweigart, 2025) (Python Software Foundation, 2026).',
 'Finding': 'search gives the first match and findall, finditer and split work on all of them (Sweigart, 2025) (Python Software Foundation, 2026).',
 'FindallMethod': "On 'Cell: 415-555-9999 Work: 212-555-0000' findall(r'\\d{3}-\\d{3}-\\d{4}') returns ['415-555-9999', '212-555-0000'] and, with three groups, [('415', '555', '9999'), ('212', "
                  "'555', '0000')] (Sweigart, 2025); two groups give tuples, findall(r'(\\w+)=(\\d+)', 'set width=20 and height=10') being [('width', '20'), ('height', '10')], but exactly one group "
                  "gives a list of strings, findall(r'(\\d)\\d', '1234') being ['1', '3'], and a non-capturing group does not count (Python Software Foundation, 2026).",
 'FindallNoOverlap': "r'\\d{3}' gives ['123'] for '1234', ['123'] for '12345' and ['123', '456'] for '123456', because the search resumes after each match (Sweigart, 2025).",
 'FinditerMethod': "For 'He was carefully disguised but captured quickly by police.' finditer(r'\\w+ly\\b') gives the matches 'carefully' at span (7, 16) and 'quickly' at span (40, 47), printed as "
                   "07-16 and 40-47, where findall gives only the two words; the chapter as read does not present finditer, and split(r'\\W+', 'Words, words, words.') gives ['Words', 'words', "
                   "'words', ''] (Python Software Foundation, 2026).",
 'Replacing': 'sub replaces matches with fixed text, with group text or with computed text (Sweigart, 2025) (Python Software Foundation, 2026).',
 'SubMethod': "Agent \\w+ applied to 'Agent Alice contacted Agent Bob.' with the replacement 'CENSORED' gives 'CENSORED contacted CENSORED.'; the chapter calls the second argument the string of the "
              'regular expression, but it is the text to search, in Pattern.sub(repl, string, count=0) (Sweigart, 2025) (Python Software Foundation, 2026).',
 'SubBackReference': "The pattern Agent (\\w)\\w* with the replacement r'\\1****' turns 'Agent Alice contacted Agent Bob.' into 'A**** contacted B****.' (Sweigart, 2025); a named group is inserted "
                     "with \\g<name>, so re.sub(r'(?P<w>\\w+)@', r'<\\g<w>>@', 'ann@x bob@y') gives '<ann>@x <bob>@y', and \\g<1> avoids the ambiguity of \\20 (Python Software Foundation, 2026).",
 'SubWithFunction': "re.sub(r'\\d+', f, '3 cats 12 dogs') with a function that doubles the number gives '6 cats 24 dogs', re.sub('a', 'A', 'banana', count=2) gives 'bAnAna', re.subn('a', 'A', "
                    "'banana') gives ('bAnAnA', 3), and sub('x*', '-', 'abxd') gives '-a-b--d-'; since Python 3.13 passing count or flags by position to re.sub and maxsplit to re.split draws a "
                    "DeprecationWarning, though re.sub('a', 'b', 'aaa', 1) still returns 'baa'; the chapter as read does not present these (Python Software Foundation, 2026).",
 'EscapeFunction': "re.escape('a.b*c') is 'a\\\\.b\\\\*c' as printed by repr, re.search(re.escape('a.b'), 'axb') is None while re.search('a.b', 'axb') finds 'axb', and "
                   "re.escape('https://www.python.org') prints https://www\\.python\\.org; the chapter escapes special characters by hand and does not present the function (Sweigart, 2025) (Python "
                   'Software Foundation, 2026).',
 'Flags': 'Flags change how a pattern is read, and the chapter names three (Sweigart, 2025) (Python Software Foundation, 2026).',
 'IgnoreCaseFlag': "re.compile(r'robocop', re.I) finds 'RoboCop', 'ROBOCOP' and 'robocop' in the three sentences of the chapter, while re.compile('RoboCop') does not find 'robocop'; re.I is short "
                   'for re.IGNORECASE, and the pattern (?i)robocop has the same effect, the inline flag having to stand at the start of the pattern (Sweigart, 2025) (Python Software Foundation, '
                   '2026).',
 'DotAllFlag': "On 'Serve the public trust.\\nProtect the innocent.\\nUphold the law.' the pattern .* matches only 'Serve the public trust.' and with re.DOTALL it matches all three lines; the inline "
               'form (?s:.) matches any character whatever the flags (Sweigart, 2025) (Python Software Foundation, 2026).',
 'VerboseMode': "With re.VERBOSE the chapter's phone pattern written over several lines with # comments finds '415-555-4242 x99' in 'Call 415-555-4242 x99 now' and has 6 groups; spaces are ignored, "
                "so re.search('a b', 'ab', re.X) matches 'ab', and a real space is written a\\ b or [ ] (Sweigart, 2025) (Python Software Foundation, 2026).",
 'CombiningFlags': "re.IGNORECASE | re.DOTALL | re.VERBOSE is one value, int(...) being 82 and its repr re.IGNORECASE|re.DOTALL|re.VERBOSE, and re.compile('foo', re.IGNORECASE | re.DOTALL) finds "
                   "'FOO' in 'xFOOx'; the chapter calls the syntax old-fashioned and leaves the bitwise operators out of scope (Sweigart, 2025).",
 'PatternPrograms': 'Project 3, Humre and the practice work put the syntax to use (Sweigart, 2025) (Sweigart, 2022).',
 'ContactExtractor': 'Project 3 builds a phone pattern and an e-mail pattern, collects the matches of both in one list and prints them (Sweigart, 2025).',
 'PhoneRegex': "The verbose pattern of the project, with the extra parentheses around the first three digits, the last four digits and the extension digits, finds '800-555-7240', '(415) 555-9900' "
               "and '415.555.9950 ext. 123' as whole matches in a text with three formats; it has 9 groups (Sweigart, 2025).",
 'EmailRegex': 'The e-mail pattern finds info@nostarch.com and media@nostarch.com in a list of addresses and has 2 groups, the whole address and the dot-something; its ending of two to four letters '
               "cuts me@example.museum to 'me@example.muse' (Sweigart, 2025).",
 'ExtensionGroupIndex': 'Run on a text with four numbers, the program as printed gives 800-555-7240, then (415)-555-9900, then 415-555-9950 x ext. 123, then -555-1234 x x99, followed by '
                        "info@nostarch.com, media@nostarch.com, academic@nostarch.com and info@nostarch.com again; the tuple for '415.555.9950 ext. 123' is ('415.555.9950 ext. 123', '415', '.', "
                        "'555', '.', '9950', ' ext. 123', 'ext.', '123'), so index 6 is ' ext. 123'; reading the digits from index 8, removing the parentheses and leaving out an empty area code "
                        'gives 800-555-7240, 415-555-9900, 415-555-9950 x123 and 555-1234 x99 (Sweigart, 2025).',
 'ClipboardRoundTrip': 'The project copies the page text to the clipboard by hand, reads it with pyperclip.paste(), joins the matches with a newline and writes them back with pyperclip.copy(), '
                       'printing Copied to clipboard: or No phone numbers or email addresses found.; this was not executed here, because it needs the third-party pyperclip module, a clipboard and '
                       'the No Starch Press contact page, and the program logic was run on a text in place of the clipboard instead (Sweigart, 2025).',
 'HumreModule': 'Humre builds pattern strings from plain-English names and the chapter presents it as a readable alternative to verbose mode (Sweigart, 2025) (Sweigart, 2022).',
 'HumreFunctions': "exactly(3, DIGIT) + '-' + exactly(3, DIGIT) + '-' + exactly(4, DIGIT) is the string \\d{3}-\\d{3}-\\d{4}, which re.compile() accepts, and DIGIT + PERIOD + DIGIT is \\d\\.\\d, "
                   "which finds '4.5' but not '4A5' where \\d.\\d finds both; all 27 rows of the chapter's two tables gave the strings the tables print in Humre 1.0.0, group(DIGIT, PERIOD, DIGIT) "
                   "gave (\\d\\.\\d), and the chapter's long Humre phone program produced exactly the regex string the chapter prints and found 415-555-1212 in 'My number is 415-555-1212.'; this was "
                   'executed from the unpacked source archive of Humre 1.0.0 under Python 3.14.4, and is not run on the page (Sweigart, 2025) (Sweigart, 2022).',
 'HumreCompatibility': 'In Humre 1.0.0 the constants DOLLAR_SIGN, HASHTAG, ANY_SINGLE, ANYTHING_LAZY, ANYTHING_GREEDY, SOMETHING_LAZY and SOMETHING_GREEDY that the chapter lists do not exist; the '
                       "release has DOLLAR, HASH_TAG, ANYCHAR ('.'), ANYTHING ('.*?'), EVERYTHING ('.*') and SOMETHING ('.+?'), and humre.parse(r'\\d{3}-\\d{3}-\\d{4}') returns None instead of the "
                       'source code the chapter prints, because the function body is a TODO; these were executed from the source archive, not on the page (Sweigart, 2025) (Sweigart, 2022).',
 'PracticeWork': 'The practice questions and programs check the syntax and the methods (Sweigart, 2025).',
 'PracticeQuestions': "The chapter has 19 practice questions; for question 18, re.compile(r'\\d+').sub('X', '12 drummers, 11 pipers, five rings, 3 hens') returns 'X drummers, X pipers, five rings, X "
                      "hens', the pattern r'\\d+' has no groups, and for question 5 the group 0 of r'(\\d\\d\\d)-(\\d\\d\\d-\\d\\d\\d\\d)' on '415-555-4242' is the whole text (Sweigart, 2025).",
 'StrongPassword': "Checking the rules one pattern each (.{8}, [a-z], [A-Z], \\d) with all() gives True for 'Passw0rdOK' and False for 'password1', 'PASSWORD1', 'Password' and 'Sh0rt', and the "
                   "chapter's hint to use several patterns is followed (Sweigart, 2025).",
 'RegexStrip': "A version of strip() with sub() removes ^\\s+ and \\s+$ when no characters are given, giving 'hi there' for '  hi there \\n', and with a given set builds a class from "
               "re.escape(chars), giving 'hi' for ('xyhixy', 'xy') and 'a' for ('[[a]]', '[]'); all three agreed with the str.strip() method (Sweigart, 2025).",
 'StringMethodsInstead': "'swordfish'.replace('word', 'deed') is 'sdeedfish', the same as re.sub('word', 'deed', 'swordfish'), while r'\\bword\\b' leaves swordfish alone, which replace cannot do; "
                         "'a\\nb'.translate({10: 32}) gives 'a b', and the in operator and startswith() answer simple questions; the HOWTO advises string methods for fixed text and the chapter as "
                         'read does not (Sweigart, 2025) (Python Software Foundation, 2026).'}
BEH = [['the book program is_phone_number and the 12-character window search',
  'def is_phone_number(text):\n'
  '    if len(text) != 12:\n'
  '        return False\n'
  '    for i in range(0, 3):\n'
  '        if not text[i].isdecimal():\n'
  '            return False\n'
  "    if text[3] != '-':\n"
  '        return False\n'
  '    for i in range(4, 7):\n'
  '        if not text[i].isdecimal():\n'
  '            return False\n'
  "    if text[7] != '-':\n"
  '        return False\n'
  '    for i in range(8, 12):\n'
  '        if not text[i].isdecimal():\n'
  '            return False\n'
  '    return True\n'
  "print('Is 415-555-4242 a phone number?', is_phone_number('415-555-4242'))\n"
  "print('Is Moshi moshi a phone number?', is_phone_number('Moshi moshi'))\n"
  "message = 'Call me at 415-555-1011 tomorrow. 415-555-9999 is my office.'\n"
  'for i in range(len(message)):\n'
  '    segment = message[i:i+12]\n'
  '    if is_phone_number(segment):\n'
  "        print('Phone number found: ' + segment)\n"
  "print('Done')\n"
  "print(message[0:12], '|', message[1:13])\n"
  "print(is_phone_number('415.555.4242'), is_phone_number('(415) 555-4242'))",
  'Is 415-555-4242 a phone number? True\nIs Moshi moshi a phone number? False\nPhone number found: 415-555-1011\nPhone number found: 415-555-9999\nDone\nCall me at 4 | all me at 41\nFalse False'],
 ['compile, search, group, groups and the group numbers',
  'import re\n'
  "pattern = re.compile(r'\\d{3}-\\d{3}-\\d{4}')\n"
  "print(type(pattern).__name__, pattern.search('My number is 415-555-4242.').group())\n"
  "phone_re = re.compile(r'(\\d\\d\\d)-(\\d\\d\\d-\\d\\d\\d\\d)')\n"
  "mo = phone_re.search('My number is 415-555-4242.')\n"
  'print(mo.group(1), mo.group(2), mo.group(0), mo.group())\n'
  'print(mo.groups())\n'
  'area_code, main_number = mo.groups()\n'
  'print(area_code, main_number)\n'
  'print(mo)\n'
  "print(pattern.search('no number here'))\n"
  'try:\n'
  "    pattern.search('no number here').group()\n"
  'except AttributeError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))",
  'Pattern 415-555-4242\n'
  '415 555-4242 415-555-4242 415-555-4242\n'
  "('415', '555-4242')\n"
  '415 555-4242\n'
  "<re.Match object; span=(13, 25), match='415-555-4242'>\n"
  'None\n'
  "AttributeError: 'NoneType' object has no attribute 'group'"],
 ['an unbalanced parenthesis raises PatternError, which is also called re.error',
  'import re\n'
  'try:\n'
  "    re.compile(r'(\\(Parentheses\\)')\n"
  'except re.error as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  '    print(e.msg, e.pos, e.pattern)\n'
  'print(re.error is re.PatternError, issubclass(re.PatternError, Exception))',
  'PatternError: missing ), unterminated subpattern at position 0\nmissing ), unterminated subpattern 0 (\\(Parentheses\\)\nTrue True'],
 ['escaped parentheses and the pipe, including the leftmost alternative that wins',
  'import re\n'
  "mo = re.compile(r'(\\(\\d\\d\\d\\)) (\\d\\d\\d-\\d\\d\\d\\d)').search('My phone number is (415) 555-4242.')\n"
  'print(mo.group(1), mo.group(2))\n'
  "match = re.compile(r'Cat(erpillar|astrophe|ch|egory)').search('Catch me if you can.')\n"
  'print(match.group(), match.group(1))\n'
  "print(re.search(r'Cat|Dog', 'I like my Dog').group())\n"
  "print(re.search('a|ab', 'ab').group(), re.search('ab|a', 'ab').group())\n"
  "print(re.search(r'a\\|b', 'a|b').group(), re.search('[|]', 'a|b').group())",
  '(415) 555-4242\nCatch ch\nDog\na ab\na|b |'],
 ['findall returns strings without groups and tuples with groups, and never overlaps',
  'import re\n'
  "text = 'Cell: 415-555-9999 Work: 212-555-0000'\n"
  "print(re.compile(r'\\d{3}-\\d{3}-\\d{4}').findall(text))\n"
  "print(re.compile(r'(\\d{3})-(\\d{3})-(\\d{4})').findall(text))\n"
  "p = re.compile(r'\\d{3}')\n"
  "print(p.findall('1234'), p.findall('12345'), p.findall('123456'))\n"
  "print(re.findall(r'(\\w+)=(\\d+)', 'set width=20 and height=10'))\n"
  "print(re.findall(r'(\\d)\\d', '1234'), re.findall(r'(?:\\d)\\d', '1234'))",
  "['415-555-9999', '212-555-0000']\n[('415', '555', '9999'), ('212', '555', '0000')]\n['123'] ['123'] ['123', '456']\n[('width', '20'), ('height', '10')]\n['1', '3'] ['12', '34']"],
 ['character classes, shorthand classes and the dot of the chapter',
  'import re\n'
  "print(re.compile(r'[aeiouAEIOU]').findall('RoboCop eats BABY FOOD.'))\n"
  "print(re.compile(r'[^aeiouAEIOU]').findall('RoboCop eats BABY FOOD.'))\n"
  "print(re.compile(r'[()]').findall('f(x)'))\n"
  "s = '12 drummers, 11 pipers, 10 lords, 9 ladies, 8 maids, 7 swans, 6 geese, 5 rings, 4 birds, 3 hens, 2 doves, 1 partridge'\n"
  "print(re.compile(r'\\d+\\s\\w+').findall(s))\n"
  "print(re.compile(r'.at').findall('The cat in the hat sat on the flat mat.'))",
  "['o', 'o', 'o', 'e', 'a', 'A', 'O', 'O']\n"
  "['R', 'b', 'C', 'p', ' ', 't', 's', ' ', 'B', 'B', 'Y', ' ', 'F', 'D', '.']\n"
  "['(', ')']\n"
  "['12 drummers', '11 pipers', '10 lords', '9 ladies', '8 maids', '7 swans', '6 geese', '5 rings', '4 birds', '3 hens', '2 doves', '1 partridge']\n"
  "['cat', 'hat', 'sat', 'lat', 'mat']"],
 ['what a class really matches: accented letters, apostrophes and the underscore',
  'import re\n'
  "name = 'First Name: Sin\\u00e9ad'\n"
  "print(re.search(r'First Name: ([A-Za-z]+)', name).group(1))\n"
  "print(re.search(r'First Name: (\\w+)', name).group(1))\n"
  "print(re.search(r'Last Name: (\\w+)', 'Last Name: O\\u2019Connor').group(1))\n"
  'print(re.search(r\'Last Name: (\\w+)\', "Last Name: O\'Connor").group(1))\n'
  "print(re.findall(r'\\w', 'a_1-'), re.findall(r'[A-z]', '[_a'), re.findall(r'[A-Za-z]', '[_a'))",
  "Sin\nSinéad\nO\nO\n['a', '_', '1'] ['[', '_', 'a'] ['a']"],
 ['the optional mark: 42!? is not 42?!',
  'import re\n'
  "p = re.compile(r'42!?')\n"
  "print(p.search('42!'))\n"
  "print(p.search('42'))\n"
  "p = re.compile(r'42?!')\n"
  "print(p.search('42!'))\n"
  "print(p.search('4!'))\n"
  "print(p.search('42') == None)\n"
  "p = re.compile(r'(\\d{3}-)?\\d{3}-\\d{4}')\n"
  "print(p.search('My number is 415-555-4242').group(), p.search('My number is 555-4242').group())",
  "<re.Match object; span=(0, 3), match='42!'>\n"
  "<re.Match object; span=(0, 2), match='42'>\n"
  "<re.Match object; span=(0, 3), match='42!'>\n"
  "<re.Match object; span=(0, 2), match='4!'>\n"
  'True\n'
  '415-555-4242 555-4242'],
 ['star and plus: the pattern as printed in the book has no space before and, the corrected one has',
  'import re\n'
  "book_star = re.compile('Eggs(and spam)*')\n"
  "book_plus = re.compile('Eggs(and spam)+')\n"
  "for s in ('Eggs', 'Eggs and spam', 'Eggs and spam and spam'):\n"
  '    print(repr(s), book_star.search(s), book_plus.search(s))\n'
  "star = re.compile('Eggs( and spam)*')\n"
  "plus = re.compile('Eggs( and spam)+')\n"
  "for s in ('Eggs', 'Eggs and spam', 'Eggs and spam and spam', 'Eggs and spam and spam and spam'):\n"
  '    print(repr(s), star.search(s), plus.search(s))',
  "'Eggs' <re.Match object; span=(0, 4), match='Eggs'> None\n"
  "'Eggs and spam' <re.Match object; span=(0, 4), match='Eggs'> None\n"
  "'Eggs and spam and spam' <re.Match object; span=(0, 4), match='Eggs'> None\n"
  "'Eggs' <re.Match object; span=(0, 4), match='Eggs'> None\n"
  "'Eggs and spam' <re.Match object; span=(0, 13), match='Eggs and spam'> <re.Match object; span=(0, 13), match='Eggs and spam'>\n"
  "'Eggs and spam and spam' <re.Match object; span=(0, 22), match='Eggs and spam and spam'> <re.Match object; span=(0, 22), match='Eggs and spam and spam'>\n"
  "'Eggs and spam and spam and spam' <re.Match object; span=(0, 31), match='Eggs and spam and spam and spam'> <re.Match object; span=(0, 31), match='Eggs and spam and spam and spam'>"],
 ['curly brackets: exact, range, open ends, and the unbounded lower bound {,5}',
  'import re\n'
  "ha = re.compile(r'(Ha){3}')\n"
  "print(ha.search('HaHaHa').group(), ha.search('HaHa'))\n"
  "for pat in (r'(Ha){3}', r'(Ha){3,5}', r'(Ha){3,}', r'(Ha){,5}'):\n"
  "    print(pat, [re.fullmatch(pat, 'Ha' * n) is not None for n in range(0, 7)])\n"
  "print(re.fullmatch(r'(Ha){3,5}', 'HaHaHa' ) is not None, re.fullmatch(r'(HaHaHa)|(HaHaHaHa)|(HaHaHaHaHa)', 'HaHaHaHa') is not None)",
  'HaHaHa None\n'
  '(Ha){3} [False, False, False, True, False, False, False]\n'
  '(Ha){3,5} [False, False, False, True, True, True, False]\n'
  '(Ha){3,} [False, False, False, True, True, True, True]\n'
  '(Ha){,5} [True, True, True, True, True, True, False]\n'
  'True True'],
 ['greedy and lazy matching, and dot-star',
  'import re\n'
  "print(re.compile(r'(Ha){3,5}').search('HaHaHaHaHa').group())\n"
  "print(re.compile(r'(Ha){3,5}?').search('HaHaHaHaHa').group())\n"
  "n = re.compile(r'First Name: (.*) Last Name: (.*)').search('First Name: Al Last Name: Sweigart')\n"
  'print(n.group(1), n.group(2))\n'
  "print(re.compile(r'<.*?>').search('<To serve man> for dinner.>').group())\n"
  "print(re.compile(r'<.*>').search('<To serve man> for dinner.>').group())\n"
  "print(re.match('<.*>', '<html><head><title>Title</title>').span(), re.match('<.*?>', '<html><head><title>Title</title>').span())",
  'HaHaHaHaHa\nHaHaHa\nAl Sweigart\n<To serve man>\n<To serve man> for dinner.>\n(0, 32) (0, 6)'],
 ['the dot stops at a newline unless DOTALL is given',
  'import re\n'
  "t = 'Serve the public trust.\\nProtect the innocent.\\nUphold the law.'\n"
  "print(repr(re.compile('.*').search(t).group()))\n"
  "print(repr(re.compile('.*', re.DOTALL).search(t).group()))\n"
  "print(repr(re.search('(?s:.+)', t).group()) == repr(t))",
  "'Serve the public trust.'\n'Serve the public trust.\\nProtect the innocent.\\nUphold the law.'\nTrue"],
 ['start, end and boundary anchors of the chapter',
  'import re\n'
  "print(re.compile(r'^Hello').search('Hello, world!'))\n"
  'print(re.compile(r\'^Hello\').search(\'He said "Hello."\') == None)\n'
  "print(re.compile(r'\\d$').search('Your number is 42'))\n"
  "print(re.compile(r'\\d$').search('Your number is forty two.') == None)\n"
  "print(re.compile(r'^\\d+$').search('1234567890'))\n"
  "print(re.compile(r'^\\d+$').search('12345xyz67890') == None)\n"
  "print(re.compile(r'\\bcat.*?\\b').findall('The cat found a catapult catalog in the catacombs.'))\n"
  "print(re.compile(r'\\Bcat\\B').findall('certificate'), re.compile(r'\\Bcat\\B').findall('catastrophe'))\n"
  "print(re.findall(r'\\bat\\b', 'at. (at) as at ay attempt atlas'))",
  "<re.Match object; span=(0, 5), match='Hello'>\n"
  'True\n'
  "<re.Match object; span=(16, 17), match='2'>\n"
  'True\n'
  "<re.Match object; span=(0, 10), match='1234567890'>\n"
  'True\n'
  "['cat', 'catapult', 'catalog', 'catacombs']\n"
  "['cat'] []\n"
  "['at', 'at', 'at']"],
 ['a dollar sign also matches before a final newline; the end-of-text escapes do not',
  'import re\n'
  "print(re.search(r'^\\d+$', '123\\n'))\n"
  "print(re.fullmatch(r'\\d+', '123\\n'))\n"
  "print(re.search(r'^\\d+\\Z', '123\\n'), re.search(r'^\\d+\\z', '123\\n'))\n"
  "print(re.search(r'^\\d+\\z', '123'), re.search(r'^\\d+\\Z', '123'))\n"
  "print(re.findall(r'^\\w+$', 'one\\ntwo\\n'), re.findall(r'^\\w+$', 'one\\ntwo\\n', re.M))\n"
  "print(re.findall('$', 'foo\\n'))\n"
  "print(re.match('X', 'A\\nB\\nX', re.M), re.search('^X', 'A\\nB\\nX', re.M))",
  "<re.Match object; span=(0, 3), match='123'>\n"
  'None\n'
  'None None\n'
  "<re.Match object; span=(0, 3), match='123'> <re.Match object; span=(0, 3), match='123'>\n"
  "[] ['one', 'two']\n"
  "['', '']\n"
  "None <re.Match object; span=(4, 5), match='X'>"],
 ['case-insensitive matching, substitution and back references of the chapter',
  'import re\n'
  "p = re.compile(r'robocop', re.I)\n"
  "for s in ('RoboCop is part man, part machine, all cop.', 'ROBOCOP protects the innocent.', 'Have you seen robocop?'):\n"
  '    print(p.search(s).group())\n'
  "print(re.compile('RoboCop').search('robocop'))\n"
  "print(re.compile(r'Agent \\w+').sub('CENSORED', 'Agent Alice contacted Agent Bob.'))\n"
  "print(re.compile(r'Agent (\\w)\\w*').sub(r'\\1****', 'Agent Alice contacted Agent Bob.'))\n"
  "print(re.compile(r'\\d+').sub('X', '12 drummers, 11 pipers, five rings, 3 hens'))\n"
  "print(re.sub('(?i)agent', 'spy', 'Agent agent AGENT'))",
  'RoboCop\nROBOCOP\nrobocop\nNone\nCENSORED contacted CENSORED.\nA**** contacted B****.\nX drummers, X pipers, five rings, X hens\nspy spy spy'],
 ['verbose mode ignores spaces and comments; flags are combined with the pipe',
  'import re\n'
  "pattern = re.compile(r'''(\n"
  '    (\\d{3}|\\(\\d{3}\\))?  # Area code\n'
  '    (\\s|-|\\.)?  # Separator\n'
  '    \\d{3}  # First three digits\n'
  '    (\\s|-|\\.)  # Separator\n'
  '    \\d{4}  # Last four digits\n'
  '    (\\s*(ext|x|ext\\.)\\s*\\d{2,5})?  # Extension\n'
  "    )''', re.VERBOSE)\n"
  "print(pattern.search('Call 415-555-4242 x99 now').group())\n"
  'print(pattern.groups)\n'
  'print(int(re.IGNORECASE | re.DOTALL | re.VERBOSE), re.IGNORECASE | re.DOTALL | re.VERBOSE)\n'
  "print(re.compile('foo', re.IGNORECASE | re.DOTALL).search('xFOOx').group())\n"
  "print(re.search('a b', 'ab', re.X), re.search(r'a\\ b', 'a b', re.X).group(), re.search('[ ]', 'a b', re.X).group() == ' ')",
  "415-555-4242 x99\n6\n82 re.IGNORECASE|re.DOTALL|re.VERBOSE\nFOO\n<re.Match object; span=(0, 2), match='ab'> a b True"],
 ['the contact extractor as printed in the book, run on text in place of the clipboard',
  'import re\n'
  "phone_re = re.compile(r'''(\n"
  '    (\\d{3}|\\(\\d{3}\\))?  # Area code\n'
  '    (\\s|-|\\.)?  # Separator\n'
  '    (\\d{3})  # First three digits\n'
  '    (\\s|-|\\.)  # Separator\n'
  '    (\\d{4})  # Last four digits\n'
  '    (\\s*(ext|x|ext\\.)\\s*(\\d{2,5}))?  # Extension\n'
  "    )''', re.VERBOSE)\n"
  "email_re = re.compile(r'''(\n"
  '    [a-zA-Z0-9._%+-]+  # Username\n'
  '    @  # @ symbol\n'
  '    [a-zA-Z0-9.-]+  # Domain name\n'
  '    (\\.[a-zA-Z]{2,4})  # Dot-something\n'
  "    )''', re.VERBOSE)\n"
  "text = 'Call 800-555-7240 or (415) 555-9900 or 415.555.9950 ext. 123, also 555-1234 x99.\\nWrite to info@nostarch.com, media@nostarch.com or academic@nostarch.com; again info@nostarch.com'\n"
  'matches = []\n'
  'for groups in phone_re.findall(text):\n'
  "    phone_num = '-'.join([groups[1], groups[3], groups[5]])\n"
  "    if groups[6] != '':\n"
  "        phone_num += ' x' + groups[6]\n"
  '    matches.append(phone_num)\n'
  'for groups in email_re.findall(text):\n'
  '    matches.append(groups[0])\n'
  "print('\\n'.join(matches))\n"
  'print(phone_re.groups, email_re.groups)',
  '800-555-7240\n(415)-555-9900\n415-555-9950 x ext. 123\n-555-1234 x x99\ninfo@nostarch.com\nmedia@nostarch.com\nacademic@nostarch.com\ninfo@nostarch.com\n9 2'],
 ['the same extractor with the extension read from its digits group and the parentheses removed',
  'import re\n'
  "phone_re = re.compile(r'((\\d{3}|\\(\\d{3}\\))?(\\s|-|\\.)?(\\d{3})(\\s|-|\\.)(\\d{4})(\\s*(ext|x|ext\\.)\\s*(\\d{2,5}))?)')\n"
  "text = 'Call 800-555-7240 or (415) 555-9900 or 415.555.9950 ext. 123, also 555-1234 x99.'\n"
  'matches = []\n'
  'for groups in phone_re.findall(text):\n'
  "    area = groups[1].strip('()')\n"
  "    phone_num = '-'.join(part for part in (area, groups[3], groups[5]) if part)\n"
  "    if groups[8] != '':\n"
  "        phone_num += ' x' + groups[8]\n"
  '    matches.append(phone_num)\n'
  "print('\\n'.join(matches))\n"
  "print(phone_re.findall('415.555.9950 ext. 123')[0])",
  "800-555-7240\n415-555-9900\n415-555-9950 x123\n555-1234 x99\n('415.555.9950 ext. 123', '415', '.', '555', '.', '9950', ' ext. 123', 'ext.', '123')"],
 ['match, search and fullmatch; pos and endpos',
  'import re\n'
  "print(re.match('c', 'abcdef'), re.search('c', 'abcdef'), re.fullmatch('p.*n', 'python'), re.fullmatch('r.*n', 'python'))\n"
  "print(re.match('super', 'superstition').span(), re.match('super', 'insuperable'), re.search('super', 'insuperable').span())\n"
  "pattern = re.compile('o[gh]')\n"
  "print(pattern.fullmatch('dog'), pattern.fullmatch('ogre'), pattern.fullmatch('doggie', 1, 3))\n"
  "print(re.compile('d').search('dog', 1), re.compile('o').match('dog', 1))",
  "None <re.Match object; span=(2, 3), match='c'> <re.Match object; span=(0, 6), match='python'> None\n"
  '(0, 5) None (2, 7)\n'
  "None None <re.Match object; span=(1, 3), match='og'>\n"
  "None <re.Match object; span=(1, 2), match='o'>"],
 ['split, finditer and the positions of the matches',
  'import re\n'
  "print(re.split(r'\\W+', 'Words, words, words.'))\n"
  "print(re.split(r'(\\W+)', 'Words, words, words.'))\n"
  "print(re.split(r'\\W+', 'Words, words, words.', maxsplit=1))\n"
  "for m in re.finditer(r'\\w+ly\\b', 'He was carefully disguised but captured quickly by police.'):\n"
  "    print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))\n"
  "print(re.findall(r'\\w+ly\\b', 'He was carefully disguised but captured quickly by police.'))",
  "['Words', 'words', 'words', '']\n['Words', ', ', 'words', ', ', 'words', '.', '']\n['Words', 'words, words.']\n07-16: carefully\n40-47: quickly\n['carefully', 'quickly']"],
 ['sub with a function, a count, subn, and escape for literal text',
  'import re\n'
  "print(re.sub(r'\\d+', lambda m: str(int(m.group()) * 2), '3 cats 12 dogs'))\n"
  "print(re.sub('a', 'A', 'banana', count=2), re.subn('a', 'A', 'banana'))\n"
  "print(re.sub('x*', '-', 'abxd'))\n"
  "print(re.escape('https://www.python.org'))\n"
  "print(re.search(re.escape('1+1'), '1+1=2').group(), re.search('1+1', '1+1=2'))\n"
  "print(re.sub(r'(\\w)(\\w*)', r'\\g<2>\\g<1>', 'spam eggs'))",
  "6 cats 24 dogs\nbAnAna ('bAnAnA', 3)\n-a-b--d-\nhttps://www\\.python\\.org\n1+1 None\npams ggse"],
 ['named groups, non-capturing groups and back references inside a pattern',
  'import re\n'
  "m = re.match(r'(?P<first_name>\\w+) (?P<last_name>\\w+)', 'Malcolm Reynolds')\n"
  "print(m.group('first_name'), m['last_name'], m.groupdict(), m.lastgroup)\n"
  "print(re.findall(r'(?:\\d{3}-)?\\d{4}', '555-1234 and 9876'), re.findall(r'(\\d{3}-)?\\d{4}', '555-1234 and 9876'))\n"
  "print(re.search(r'\\b(\\w+) \\1\\b', 'this is is a typo').group(), re.search(r'(.+) \\1', 'the the').group())\n"
  "print(re.match(r'(\\d+)\\.?(\\d+)?', '24').groups(), re.match(r'(\\d+)\\.?(\\d+)?', '24').groups('0'))",
  "Malcolm Reynolds {'first_name': 'Malcolm', 'last_name': 'Reynolds'} last_name\n['555-1234', '9876'] ['555-', '']\nis is the the\n('24', None) ('24', '0')"],
 ['lookahead, lookbehind and possessive quantifiers',
  'import re\n'
  "print(re.findall(r'\\d+(?= dollars)', '5 dollars and 7 euros'))\n"
  "print(re.findall(r'(?<=\\$)\\d+', 'cost $30 or 40'))\n"
  "print(re.search('Isaac (?!Asimov)', 'Isaac Newton').group(), re.search('Isaac (?!Asimov)', 'Isaac Asimov'))\n"
  "print(re.match('a*a', 'aaaa').group(), re.match('a*+a', 'aaaa'))\n"
  'try:\n'
  "    re.compile('(?<=a*)b')\n"
  'except re.error as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))",
  "['5']\n['30']\nIsaac  None\naaaa None\nPatternError: look-behind requires fixed-width pattern"],
 ['Unicode digits and letters against the ASCII flag; the bytes pattern',
  'import re\n'
  "s = '1\\u0663\\u096a'\n"
  "print(len(re.findall(r'\\d', s)), len(re.findall(r'\\d', s, re.ASCII)), len(re.findall(r'[0-9]', s)))\n"
  "print(bool(re.match(r'\\w', '\\u00e9')), bool(re.match(r'\\w', '\\u00e9', re.ASCII)), bool(re.match(rb'\\w', '\\u00e9'.encode())))\n"
  "print(bool(re.match(r'\\s', '\\u00a0')), bool(re.match(r'\\s', '\\u00a0', re.ASCII)))\n"
  'try:\n'
  "    re.search(rb'a', 'abc')\n"
  'except TypeError as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))",
  '3 1 1\nTrue False False\nTrue False\nTypeError: cannot use a bytes pattern on a string-like object'],
 ['the two practice programs with checks, one regex per rule',
  'import re\n'
  'def is_strong(password):\n'
  "    return all(re.search(rule, password) for rule in (r'.{8}', r'[a-z]', r'[A-Z]', r'\\d'))\n"
  "for pw in ('Passw0rdOK', 'password1', 'PASSWORD1', 'Password', 'Sh0rt'):\n"
  '    print(pw, is_strong(pw))\n'
  'def regex_strip(text, chars=None):\n'
  '    if chars is None:\n'
  "        return re.sub(r'^\\s+|\\s+$', '', text)\n"
  "    cls = '[' + re.escape(chars) + ']'\n"
  "    return re.sub('^' + cls + '+|' + cls + '+$', '', text)\n"
  "print(repr(regex_strip('  hi there \\n')), repr(regex_strip('xyhixy', 'xy')), repr(regex_strip('[[a]]', '[]')))\n"
  "print(regex_strip('  hi there \\n') == '  hi there \\n'.strip(), regex_strip('xyhixy', 'xy') == 'xyhixy'.strip('xy'), regex_strip('[[a]]', '[]') == '[[a]]'.strip('[]'))",
  "Passw0rdOK True\npassword1 False\nPASSWORD1 False\nPassword False\nSh0rt False\n'hi there' 'hi' 'a'\nTrue True True"],
 ['string methods are enough for fixed text',
  'import re\n'
  "print('swordfish'.replace('word', 'deed'), re.sub('word', 'deed', 'swordfish'))\n"
  "print(re.sub(r'\\bword\\b', 'deed', 'a word in swordfish'))\n"
  "print(repr('a\\nb'.translate({10: 32})), 'spam' in 'eggs and spam', 'eggs and spam'.startswith('eggs'))",
  "sdeedfish sdeedfish\na deed in swordfish\n'a b' True True"],
 ['inline flags must come first, and positional count and flags are deprecated',
  'import re, warnings\n'
  'try:\n'
  "    re.compile('a(?i)b')\n"
  'except re.error as e:\n'
  "    print(type(e).__name__ + ': ' + str(e))\n"
  'with warnings.catch_warnings(record=True) as w:\n'
  "    warnings.simplefilter('always')\n"
  "    re.sub('a', 'b', 'aaa', 1)\n"
  "    re.split(',', 'a,b,c', 1)\n"
  "    re.sub('a', 'b', 'aaa', count=1)\n"
  'print([x.category.__name__ for x in w])\n'
  "print(re.sub('a', 'b', 'aaa', 1))",
  "PatternError: global flags not at the start of the expression at position 1\n['DeprecationWarning', 'DeprecationWarning']\nbaa"],
 ['raw strings against ordinary strings in patterns',
  'import re, warnings\n'
  "print(len(r'\\d'), len('\\\\d'), r'\\d' == '\\\\d')\n"
  'with warnings.catch_warnings(record=True) as w:\n'
  "    warnings.simplefilter('always')\n"
  '    compile(r"\'\\\\d\'", \'x\', \'eval\')\n'
  '    compile(r"\'\\d\'", \'x\', \'eval\')\n'
  'print([x.category.__name__ for x in w])\n'
  "print(bool(re.search('\\\\d', 'a1')), bool(re.search(r'\\d', 'a1')), bool(re.search('\\b', 'a')), bool(re.search(r'\\b', 'a')))",
  "2 2 True\n['SyntaxWarning']\nTrue True False True"]]
