"""Re-runs the statements chapter 9's data module makes about Humre 1.0.0, which the shared checks cannot run (Humre is not installed).
Usage: humre_check_v1_0_0.py <path to Humre-1.0.0/src>  (unpack the source archive of Humre 1.0.0 from the Python Package Index;
sha256 of Humre-1.0.0.tar.gz: 469ae0831969e01726049dc463cdba23a571c8d9fa0ecee49ac2d36f5a3290fa). Exits 1 on any mismatch."""
import re, sys
sys.path.insert(0, sys.argv[1])
import humre
from humre import *
bad = []
def chk(name, got, want):
    if got != want: bad.append((name, got, want))
rows = [(group('A'), '(A)'), (optional('A'), 'A?'), (either('A', 'B', 'C'), 'A|B|C'), (exactly(3, 'A'), 'A{3}'), (between(3, 5, 'A'), 'A{3,5}'),
 (at_least(3, 'A'), 'A{3,}'), (at_most(3, 'A'), 'A{,3}'), (chars('A-Z'), '[A-Z]'), (nonchars('A-Z'), '[^A-Z]'), (zero_or_more('A'), 'A*'),
 (zero_or_more_lazy('A'), 'A*?'), (one_or_more('A'), 'A+'), (one_or_more_lazy('A'), 'A+?'), (starts_with('A'), '^A'), (ends_with('A'), 'A$'),
 (starts_and_ends_with('A'), '^A$'), (named_group('name', 'A'), '(?P<name>A)'), (optional_group('A'), '(A)?'), (group_either('A', 'B', 'C'), '(A|B|C)'),
 (exactly_group(3, 'A'), '(A){3}'), (between_group(3, 5, 'A'), '(A){3,5}'), (at_least_group(3, 'A'), '(A){3,}'), (at_most_group(3, 'A'), '(A){,3}'),
 (zero_or_more_group('A'), '(A)*'), (zero_or_more_lazy_group('A'), '(A)*?'), (one_or_more_group('A'), '(A)+'), (one_or_more_lazy_group('A'), '(A)+?')]
chk('rows', len(rows), 27)
for k, (got, want) in enumerate(rows): chk('row %d' % k, got, want)
chk('multi-argument group', group(DIGIT, PERIOD, DIGIT), r'(\d\.\d)')
chk('phone', exactly(3, DIGIT) + '-' + exactly(3, DIGIT) + '-' + exactly(4, DIGIT), r'\d{3}-\d{3}-\d{4}')
pr = group(optional_group(either(exactly(3, DIGIT), OPEN_PAREN + exactly(3, DIGIT) + CLOSE_PAREN)), optional(group_either(WHITESPACE, '-', PERIOD)),
    group(exactly(3, DIGIT)), group_either(WHITESPACE, '-', PERIOD), group(exactly(4, DIGIT)),
    optional_group(zero_or_more(WHITESPACE), group_either('ext', 'x', r'ext\.'), zero_or_more(WHITESPACE), group(between(2, 5, DIGIT))))
chk('long phone regex', pr, r'((\d{3}|\(\d{3}\))?(\s|-|\.)?(\d{3})(\s|-|\.)(\d{4})(\s*(ext|x|ext\.)\s*(\d{2,5}))?)')
chk('finds', re.compile(pr).search('My number is 415-555-1212.').group(), '415-555-1212')
chk('PERIOD', (re.search(DIGIT + PERIOD + DIGIT, '4.5') is not None, re.search(DIGIT + PERIOD + DIGIT, '4A5'), re.search(r'\d.\d', '4A5') is not None), (True, None, True))
for n in ('DOLLAR_SIGN', 'HASHTAG', 'ANY_SINGLE', 'ANYTHING_LAZY', 'ANYTHING_GREEDY', 'SOMETHING_LAZY', 'SOMETHING_GREEDY'): chk('missing ' + n, hasattr(humre, n), False)
chk('names', (humre.DOLLAR, humre.HASH_TAG, humre.ANYCHAR, humre.ANYTHING, humre.EVERYTHING, humre.SOMETHING), (r'\$', r'\#', '.', '.*?', '.*', '.+?'))
chk('parse', humre.parse(r'\d{3}-\d{3}-\d{4}'), None)
print("%d mismatches" % len(bad))
for b in bad: print(" ", b)
sys.exit(1 if bad else 0)
