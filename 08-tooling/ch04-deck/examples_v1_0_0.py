__version__ = "1.0.0"
# Every expression and every whole program the SEN0414 chapter 4 deck shows. Outputs come from executing them
# (examples_run_v1_0_0.py), never from typing. Programs are this course's own, not the book's.
EX = {
 "types": ["type(None).__name__", "(lambda: None)() is None"],
 "limits": ["__import__('sys').getrecursionlimit()", "issubclass(RecursionError, RuntimeError)"],
 "errors": ["issubclass(UnboundLocalError, NameError)", "issubclass(ZeroDivisionError, ArithmeticError)"],
}
# name: (code, [inputs of each run])
PROGRAMS = {
 "hello_v1_0_0.py": ("def hello():\n    print('Good morning!')\n    print('Good evening!')\nhello()\nprint('ONE MORE TIME!')\nhello()\n", [[]]),
 "pasted_v1_0_0.py": ("pasted = ['Good morning!', 'Good afternoon!', 'Good evening!'] * 2 + ['ONE MORE TIME!', 'Good morning!', 'Good afternoon!', ' Good evening!']\ncalled = ['Good morning!', 'Good afternoon!', 'Good evening!'] * 2 + ['ONE MORE TIME!', 'Good morning!', 'Good afternoon!', 'Good evening!']\nfor one, other in zip(pasted, called):\n    if one != other:\n        print(repr(one), 'is not', repr(other))\n", [[]]),
 "params_v1_0_0.py": ("def say_hello_to(name):\n    print('Good morning, ' + name)\nsay_hello_to('Alice')\nsay_hello_to('Bob')\ntry:\n    print(name)\nexcept NameError as error:\n    print(error)\n", [[]]),
 "named_v1_0_0.py": ("print('Hello', end='')\nprint('World')\nprint('cats', 'dogs', 'mice', sep=',')\n", [[]]),
 "kinds_v1_0_0.py": ("def scale(value, /, factor=2):\n    return value * factor\ndef area(width, *, height):\n    return width * height\nprint(scale(3), scale(3, factor=4), area(2, height=5))\nfor call in (lambda: scale(value=3), lambda: area(2, 5)):\n    try:\n        call()\n    except TypeError as error:\n        print(error)\n", [[]]),
 "returns_v1_0_0.py": ("def area(width, height):\n    return width * height\ndef shout(text):\n    print(text.upper())\nprint(area(3, 4) + area(1, 2))\nresult = shout('hi')\nprint(result is None)\n", [[]]),
 "defaults_v1_0_0.py": ("def collect(item, box=[]):\n    box.append(item)\n    return box\nprint(collect(1))\nprint(collect(2))\ndef collect_safely(item, box=None):\n    if box is None:\n        box = []\n    box.append(item)\n    return box\nprint(collect_safely(1))\nprint(collect_safely(2))\n", [[]]),
 "stack_v1_0_0.py": ("import traceback\ndef outer():\n    print('outer starts')\n    middle()\n    print('outer returns')\ndef middle():\n    print('middle starts')\n    inner()\n    print('middle returns')\ndef inner():\n    print('inner: frames are', [frame.name for frame in traceback.extract_stack()][-3:])\nouter()\n", [[]]),
 "recursion_v1_0_0.py": ("import sys\ndef forever():\n    return forever()\ntry:\n    forever()\nexcept RecursionError as error:\n    print(sys.getrecursionlimit(), error)\n", [[]]),
 "scopes_v1_0_0.py": ("def inner():\n    name = 'inner local'\n    print(name)\ndef outer():\n    name = 'outer local'\n    print(name)\n    inner()\n    print(name)\nname = 'global'\nouter()\nprint(name)\n", [[]]),
 "globalstmt_v1_0_0.py": ("def change():\n    global mood\n    mood = 'changed'\ndef shadow():\n    mood = 'local only'\nmood = 'original'\nshadow()\nprint(mood)\nchange()\nprint(mood)\n", [[]]),
 "symtable_v1_0_0.py": ("import symtable\nsource = 'def a():\\n    global x\\n    x = 1\\ndef b():\\n    x = 2\\ndef c():\\n    print(x)\\nx = 3\\n'\ntable = symtable.symtable(source, 'demo', 'exec')\nfor function in table.get_children():\n    if function.get_name() in ('a', 'b', 'c'):\n        symbol = function.lookup('x')\n        print(function.get_name(), 'global' if symbol.is_global() else 'local')\n", [[]]),
 "unbound_v1_0_0.py": ("def show():\n    print(count)\n    count = 1\ncount = 0\ntry:\n    show()\nexcept UnboundLocalError as error:\n    print(type(error).__name__ + ':', error)\n", [[]]),
 "nonlocal_v1_0_0.py": ("def counter():\n    total = 0\n    def add():\n        nonlocal total\n        total += 1\n    add()\n    add()\n    return total\nprint(counter())\n", [[]]),
 "inside_v1_0_0.py": ("def divide(by):\n    try:\n        return 42 / by\n    except ZeroDivisionError:\n        print('Error: Invalid argument.')\nprint(divide(2))\nprint(divide(0))\nprint(divide(1))\n", [[]]),
 "outside_v1_0_0.py": ("def divide(by):\n    return 42 / by\ntry:\n    print(divide(2))\n    print(divide(0))\n    print(divide(1))\nexcept ZeroDivisionError:\n    print('Error: Invalid argument.')\n", [[]]),
 "except758_v1_0_0.py": ("try:\n    int('puppy')\nexcept ValueError, TypeError:\n    print('caught either one')\n", [[]]),
 "annotations_v1_0_0.py": ("import annotationlib\ndef parse(text: Document) -> Result:\n    return text\nprint(parse('ok'))\ntry:\n    parse.__annotations__\nexcept NameError as error:\n    print('NameError:', error)\nprint(sorted(annotationlib.get_annotations(parse, format=annotationlib.Format.FORWARDREF)))\n", [[]]),
 "collatz_v1_0_0.py": ("def collatz(number):\n    if number % 2 == 0:\n        result = number // 2\n    else:\n        result = 3 * number + 1\n    print(result, end=' ')\n    return result\nnumber = int(input('Enter number: '))\nprint(number, end=' ')\nwhile number != 1:\n    number = collatz(number)\nprint()\n", [["3"]]),
 "validated_v1_0_0.py": ("def collatz(number):\n    result = number // 2 if number % 2 == 0 else 3 * number + 1\n    print(result, end=' ')\n    return result\nwhile True:\n    try:\n        number = int(input('Enter number: '))\n        break\n    except ValueError:\n        print('Please enter a whole number.')\nprint(number, end=' ')\nwhile number != 1:\n    number = collatz(number)\nprint()\n", [["puppy", "6"]]),
}
