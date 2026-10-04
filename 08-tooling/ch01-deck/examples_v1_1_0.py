__version__ = "1.1.0"
# Every code example the renewed chapter 1 lecture deck shows. Nothing here carries an output: the outputs are produced
# by executing each line and each program under the course interpreter at build time (examples_run_v2_0_0.py), so a
# slide can only show what Python actually printed.
#
# EX holds interactive-shell sessions. Each one is run in a namespace of its own, line by line, exactly the way
# ch02-deck/deck_check_v1_0_1.py re-runs them from the finished slides. A line that is a statement records no output
# and must be followed by another line in the same card. No line may print: printing examples belong in PROGRAMS.
#
# 1.1.0 keeps every session of 1.0.1 and adds one session per concept of the chapter corpus
# (sen0414_ch01_corpus_v1_2_0.py) that has a worked example, plus the four whole programs the deck traces. Additive to
# the earlier file's content, so MINOR.
EX = {
 # --- Value: integers, floats, strings ---
 "shell":    ["2 + 2", "2 + 3 * 6", "(2 + 3) * 6"],
 "integer":  ["2 ** 100", "7 + 1", "int('42')"],
 "intmix":   ["6 / 3", "4 * 3.75 - 1"],
 "float":    ["0.1 + 0.2", "round(0.1 + 0.2, 2)", "0.1 + 0.2 == 0.3"],
 "string":   ["'Alice' * 3", "len('Hello, world!')", "'7' + 1"],
 "datatype": ["type(7)", "type(3.5)", "type('Alice')"],
 "expr":     ["3 * (2 + 4)", "2 + 3 * 6"],
 # --- Operation: arithmetic, text, binding ---
 "ops":      ["2 ** 8", "23 / 7", "23 // 7", "23 % 7", "3 * 5", "5 - 2"],
 "operator": ["7 % 3", "2 + 3", "'a' + 'b'", "7 / 2", "7 // 2"],
 "prec":     ["2 + 3 * 6", "(2 + 3) * 6", "-3 ** 2", "(-3) ** 2", "8 / 2 * 3"],
 "intdiv":   ["23 // 7", "23 % 7", "23 / 7", "-7 // 2"],
 "concat":   ["'Alice' + 'Bob'", "'Hello' + 'world'", "'Alice' + 42"],
 "repl":     ["'Alice' * 3", "3 * 'ab'", "'ab' * 0", "'Alice' * 2.5"],
 "var":      ["spam = 42", "spam", "spam = spam + 1", "spam", "Spam"],
 "assign":   ["spam = 42", "spam = spam + 1", "spam", "never_assigned_name"],
 # --- Built-in functions ---
 "call":     ["round(3.14159, 2)", "round(4.7)", "len('hello') + 1", "type(round).__name__", "round"],
 "conv":     ["int('42')", "float('3.5')", "str(29)", "int(4.7)", "int('4.2')"],
 "length":   ["len('hello')", "len('a b')", "len(str(12345))", "len(12345)"],
 # --- Execution environment ---
 "cpython":  ["__import__('sys').implementation.name", "__import__('platform').python_implementation()"],
 "gil":      ["__import__('sys')._is_gil_enabled()", "__import__('sysconfig').get_config_var('Py_GIL_DISABLED')"],
 "version":  ["__import__('sys').version_info[:3]", "__import__('sys').version_info.releaselevel"],
 "thread":   ["__import__('threading').active_count()", "__import__('threading').current_thread().name"],
 # --- Modern practice ---
 "fstr":     ["name = 'Alice'", "f'Hello, {name}!'", "f'{2 ** 8}'", "f'{1 / 3:.2f}'", "'It is {name}'"],
 "package":  ["import random", "type(random).__name__", "random.__name__"],
}

# Whole programs the deck shows. Each entry is (source, [one list of typed lines per run]). The transcript shown on a
# slide is the transcript of the run, and ch03-deck/program_check_v1_0_0.py re-runs each of them against the deck.
PROGRAMS = {
 "firstprogram_v1_1_0.py": (
  "print('Hello, world!')\n"
  "print('What is your name?')\n"
  "my_name = input()\n"
  "print(f'It is good to meet you, {my_name}.')\n"
  "print(f'The length of your name is {len(my_name)}.')\n"
  "my_age = int(input('What is your age? '))\n"
  "print(f'You will be {my_age + 1} in a year.')\n", [["Ayse", "20"]]),
 "bytecode_v1_0_0.py": (
  "import dis\n"
  "dis.dis('a + b * 2')\n", [[]]),
 "thread_v1_0_0.py": (
  "import threading\n"
  "def greet(who):\n"
  "    print('hello from', who)\n"
  "t = threading.Thread(target=greet, args=('the second thread',))\n"
  "t.start()\n"
  "t.join()\n"
  "print('the main thread waited')\n", [[]]),
 "print_v1_0_0.py": (
  "print('Hello,', 'world!')\n"
  "print('Hello,', 'world!', sep='-', end=' <end>\\n')\n"
  "print()\n"
  "print('the line above is empty')\n", [[]]),
 "concat_vs_fstring_v1_0_0.py": (
  "name = 'Alice'\n"
  "age = 20\n"
  "print('Hello, ' + name + '! You are ' + str(age) + '.')\n"
  "print(f'Hello, {name}! You are {age}.')\n", [[]]),
}
