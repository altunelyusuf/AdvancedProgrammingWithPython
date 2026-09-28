__version__ = "1.0.0"
# Every expression and every whole program the SEN0414 chapter 3 deck shows. Outputs come from executing them
# (examples_run_v1_0_0.py), never from typing. Programs are this course's own, not the book's.
EX = {
 "range": ["list(range(5))", "list(range(12, 16))", "list(range(0, 10, 2))", "list(range(5, -1, -1))"],
 "lazy": ["range(10)", "sum(range(4))"],
 "same": ["list(range(10)) == list(range(0, 10)) == list(range(0, 10, 1))"],
 "enum": ["list(enumerate(['tic', 'tac', 'toe']))", "list(enumerate(['tic', 'tac', 'toe'], start=1))"],
 "zip": ["list(zip('ab', [1, 2]))", "list(zip('abc', [1, 2]))", "list(zip('abc', [1, 2], strict=True))"],
}
# name: (code, [inputs of each run])
PROGRAMS = {
 "waiting_v1_0_0.py": ("answer = ''\nwhile answer != 'yes':\n    answer = input('Ready? ')\nprint('Starting')\n", [["no", "maybe", "yes"]]),
 "summing_v1_0_0.py": ("total = 0\nwhile True:\n    entry = input('Number (blank to stop): ')\n    if entry == '':\n        break\n    if not entry.isdigit():\n        continue\n    total += int(entry)\nprint('Total:', total)\n", [["5", "x", "7", ""]]),
 "searching_v1_0_0.py": ("words = ['cat', 'dog', 'bird']\ntarget = input('Find: ')\nfor word in words:\n    if word == target:\n        print('found', word)\n        break\nelse:\n    print('not found')\n", [["dog"], ["fish"]]),
 "loopvar_v1_0_0.py": ("for i in range(3):\n    pass\nprint(i)\nfor j in []:\n    pass\nprint('j' in dir())\n", [[]]),
 "quitting_v1_0_0.py": ("import sys\nwhile True:\n    command = input('Command: ')\n    if command == 'exit':\n        sys.exit()\n    print('you typed', command)\n", [["hi", "exit"]]),
 "guessing_v1_0_0.py": ("import random\nrandom.seed(7)\nsecret = random.randint(1, 20)\nfor attempt in range(1, 4):\n    guess = int(input('Guess: '))\n    if guess < secret:\n        print('too low')\n    elif guess > secret:\n        print('too high')\n    else:\n        print(f'got it in {attempt}')\n        break\nelse:\n    print(f'out of guesses; it was {secret}')\n", [["10", "15", "11"], ["1", "2", "3"]]),
 "chunks_v1_0_0.py": ("import io\nfile = io.StringIO('abcdefgh')\nwhile chunk := file.read(3):\n    print(chunk)\n", [[]]),
 "copying_v1_0_0.py": ("users = {'Ada': 'active', 'Can': 'inactive', 'Eda': 'inactive'}\nfor name, status in users.copy().items():\n    if status == 'inactive':\n        del users[name]\nprint(users)\n", [[]]),
}
