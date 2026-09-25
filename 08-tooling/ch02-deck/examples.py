# Every expression the SEN0414 chapter 2 deck shows; outputs come from executing them, never from typing.
EX = {
 "bool": ["42 == 42", "type(True)"],
 "cmp": ["42 == 42", "42 != 42", "2 < 3", "2 > 3", "4 <= 4", "5 >= 6"],
 "eq": ["42 == '42'", "'hello' == 'Hello'"],
 "logic": ["True and False", "True or False", "not True"],
 "mix": ["(4 < 5) and (5 < 6)", "2 + 2 == 4 and not 2 + 2 == 5"],
 "truth": ["bool('')", "bool('0')", "bool([])", "bool(0.0)"],
 "short": ["0 or 'default'", "'' or 'default'", "'set' or 'default'"],
 "chain": ["1 < 2 < 3", "3 > 2 > 5"],
 "cond": ["'even' if 10 % 2 == 0 else 'odd'"],
}
