__version__ = "1.0.0"
# Every expression and program the chapter 5 deck shows. Outputs come from executing them (examples_run_v1_0_0.py), never from typing.
# A program is (code, [input-lists, one per run]). Programs whose result goes to standard error (a traceback) are recorded by
# visuals_make_v1_0_0.py instead, in a subprocess, and drawn from the specification.
L = "import logging, sys\nlogging.basicConfig(level=%s, stream=sys.stdout, format='%%(levelname)s - %%(message)s')\n"
EX = {
 "levels": ["[(n, getattr(__import__('logging'), n)) for n in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')]",
            "__import__('logging').getLogger().getEffectiveLevel()"],
 "assertion": ["issubclass(AssertionError, Exception)", "__debug__"],
 "hook": ["__import__('sys').breakpointhook.__name__", "hasattr(__import__('sys'), 'remote_exec')",
          "[c for c in ('do_step', 'do_next', 'do_return', 'do_continue', 'do_break', 'do_where') if hasattr(__import__('pdb').Pdb, c)]", "hasattr(__import__('pdb').Pdb, 'do_quit')"],
}
PROGRAMS = {
 "boxprint_v1_0_0.py": ("def box_print(symbol, width, height):\n    if len(symbol) != 1:\n        raise Exception('Symbol must be a single character string.')\n    if width <= 2:\n        raise Exception('Width must be greater than 2.')\n    if height <= 2:\n        raise Exception('Height must be greater than 2.')\n    print(symbol * width)\n    for i in range(height - 2):\n        print(symbol + (' ' * (width - 2)) + symbol)\n    print(symbol * width)\n\nfor sym, w, h in (('*', 4, 4), ('x', 1, 3), ('ZZ', 3, 3)):\n    try:\n        box_print(sym, w, h)\n    except Exception as err:\n        print('An exception happened: ' + str(err))\n", [[]]),
 "unwinding_v1_0_0.py": ("def read_age(text):\n    return int(text)\n\ndef load(record):\n    return read_age(record['age'])\n\ndef process(records):\n    return [load(r) for r in records]\n\ntry:\n    process([{'age': '41'}, {'age': 'abc'}])\nexcept ValueError as e:\n    print('caught:', e)\n", [[]]),
 "notes_v1_0_0.py": ("try:\n    try:\n        int('x')\n    except ValueError as e:\n        e.add_note('while reading the age field')\n        raise\nexcept ValueError as e:\n    print(e.__notes__)\n", [[]]),
 "assertdemo_v1_0_0.py": ("ages = [26, 57, 92, 54, 22, 15, 17, 80, 47, 73]\nages.reverse()\ntry:\n    assert ages[0] <= ages[-1]\n    print('the list is sorted')\nexcept AssertionError as e:\n    print(type(e).__name__, repr(str(e)))\n", [[]]),
 "assertmsg_v1_0_0.py": ("x = -1\ntry:\n    assert x > 0, f'x must be positive, got {x}'\nexcept AssertionError as e:\n    print(e)\n", [[]]),
 "optimised_v1_0_0.py": ("src = \"assert False, 'boom'\\nprint('reached')\"\ntry:\n    exec(compile(src, 'x', 'exec'))\nexcept AssertionError as e:\n    print('normal run:', e)\nexec(compile(src, 'x', 'exec', optimize=1))\n", [[]]),
 "filelog_v1_0_0.py": ("import logging, os, tempfile\npath = os.path.join(tempfile.mkdtemp(), 'myProgramLog.txt')\nlogging.basicConfig(filename=path, level=logging.DEBUG, format='%(levelname)s - %(message)s')\nlogging.debug('to the file')\nlogging.critical('also to the file')\nprint(open(path).read(), end='')\n", [[]]),
 "levelsdemo_v1_0_0.py": (L % "logging.INFO" + "logging.debug('debug message')\nlogging.info('info message')\nlogging.warning('warning message')\nlogging.error('error message')\nlogging.critical('critical message')\n", [[]]),
 "force_v1_0_0.py": (L % "logging.INFO" + "logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(levelname)s - %(message)s')\nlogging.debug('second call ignored')\nlogging.info('first call rules')\nlogging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(levelname)s - %(message)s', force=True)\nlogging.debug('force=True replaces it')\n", [[]]),
 "disable_v1_0_0.py": (L % "logging.INFO" + "logging.critical('before disable')\nlogging.disable(logging.CRITICAL)\nlogging.critical('after disable')\nlogging.error('after disable')\nlogging.disable(logging.NOTSET)\nlogging.error('after re-enabling')\n", [[]]),
 "lazy_v1_0_0.py": ("import logging\nclass Loud:\n    calls = 0\n    def __str__(self):\n        Loud.calls += 1\n        return 'loud'\nlog = logging.getLogger('demo')\nlog.setLevel(logging.INFO)\nlog.addHandler(logging.NullHandler())\nlog.debug('value is %s', Loud())\nprint('lazy:', Loud.calls)\nlog.debug(f'value is {Loud()}')\nprint('f-string:', Loud.calls)\n", [[]]),
 "factorial_bug_v1_0_0.py": (L % "logging.DEBUG" + "def factorial(n):\n    logging.debug('Start of factorial(%s)', n)\n    total = 1\n    for i in range(n + 1):\n        total *= i\n        logging.debug('i is %s, total is %s', i, total)\n    logging.debug('End of factorial(%s)', n)\n    return total\n\nprint(factorial(3))\n", [[]]),
 "factorial_fixed_v1_0_0.py": (L % "logging.DEBUG" + "def factorial(n):\n    logging.debug('Start of factorial(%s)', n)\n    total = 1\n    for i in range(1, n + 1):\n        total *= i\n        logging.debug('i is %s, total is %s', i, total)\n    logging.debug('End of factorial(%s)', n)\n    return total\n\nprint(factorial(3))\n", [[]]),
 "adding_bug_v1_0_0.py": ("print('Enter the first number to add:')\nfirst = input()\nprint('Enter the second number to add:')\nsecond = input()\nprint('Enter the third number to add:')\nthird = input()\nprint('The sum is ' + first + second + third)\n", [["5", "3", "42"]]),
 "adding_fixed_v1_0_0.py": ("print('Enter the first number to add:')\nfirst = int(input())\nprint('Enter the second number to add:')\nsecond = int(input())\nprint('Enter the third number to add:')\nthird = int(input())\nprint('The sum is', first + second + third)\n", [["5", "3", "42"]]),
 "cointoss_bug_v1_0_0.py": ("import random\nrandom.seed(7)\nguess = input('Guess the coin toss! Enter heads or tails: ')\ntoss = random.randint(0, 1)  # 0 is tails, 1 is heads\nif toss == guess:\n    print('You got it!')\nelse:\n    print('Nope! Guess again!')\nprint(type(toss).__name__, type(guess).__name__)\n", [["heads"], ["tails"]]),
 "debugdemo_v1_0_0.py": ("def add(a, b):\n    total = a + b\n    return total\n\ndef main():\n    x = add(2, 3)\n    y = add(x, 10)\n    print(y)\n\nmain()\n", [[]]),
}
