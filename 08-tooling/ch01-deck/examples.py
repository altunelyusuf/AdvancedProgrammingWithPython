# Every code example the deck shows. Outputs are NOT typed: they are produced by executing each one
# under the current Python release at build time, so a slide can only show what Python actually prints.
EX = {
 "shell": ["2 + 2", "2 + 3 * 6", "(2 + 3) * 6"],
 "ops": ["2 ** 8", "23 / 7", "23 // 7", "23 % 7", "3 * 5", "5 - 2"],
 "big": ["2 ** 100"],
 "float": ["0.1 + 0.2", "round(0.1 + 0.2, 2)"],
 "str": ["'Alice' + 'Bob'", "'Alice' * 3", "'Alice' + 42"],
 "conv": ["int('42')", "str(29)", "float('3.14')", "int('4.2')", "len('hello')"],
 "var": ["spam = 42; spam", "spam = 42; spam = spam + 1; spam"],
 "fstr": ["name = 'Alice'; f'Hello, {name}! 2 ** 8 is {2 ** 8}.'"],
}
