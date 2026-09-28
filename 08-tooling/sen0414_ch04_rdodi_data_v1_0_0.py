"""Chapter 4 content for the RDODI build: sources, findings, taxonomy and section bodies.
The book's chapter was read on automatetheboringstuff.com on 2026-09-29. The Python documentation was read from the
CPython source tree at tag v3.14.4 (Doc/), the PEPs from the python/peps repository at commit ce48c4e (2026-09-27);
every behaviour was executed under Python 3.14.4. A claim not in this file was not made."""
__version__ = "1.0.0"
CH = 4
DATE = "2026-09-29"
PYVER = "3.14.4"
TITLE = "Functions for an advanced course: chapter 4 of the 3rd edition and today's Python"
QUESTION = "What does chapter 4 of the 3rd edition teach about defining and calling functions, return values, the call stack, variable scope and exception handling, which of its printed outputs still hold under Python 3.14.4, and what must an advanced course add so that it matches current Python?"
CQS = ("Which constructs define, call and leave a function, and what decides which variable a name refers to?",
       "Which printed outputs and concepts of the chapter differ in current Python, and on what source?")
PUBS = [
 ("P01","Automate the Boring Stuff with Python, 3rd edition - Chapter 4, Functions (Al Sweigart, No Starch Press, 2025)","https://automatetheboringstuff.com/3e/chapter4.html",True),
 ("P02","The Python Tutorial, 4. More Control Flow Tools - defining functions, default argument values, keyword arguments, special parameters (Python 3.14.4 documentation source)","https://docs.python.org/3/tutorial/controlflow.html",False),
 ("P03","The Python Language Reference, 4. Execution model - naming and binding, resolution of names (Python 3.14.4 documentation source)","https://docs.python.org/3/reference/executionmodel.html",False),
 ("P04","Python Frequently Asked Questions, Programming FAQ - Why am I getting an UnboundLocalError (Python 3.14.4 documentation source)","https://docs.python.org/3/faq/programming.html",False),
 ("P05","The Python Language Reference, 7. Simple statements - return, global and nonlocal (Python 3.14.4 documentation source)","https://docs.python.org/3/reference/simple_stmts.html",False),
 ("P06","The Python Standard Library, sys - getrecursionlimit (Python 3.14.4 documentation source)","https://docs.python.org/3/library/sys.html",False),
 ("P07","The Python Standard Library, Built-in Functions - print (Python 3.14.4 documentation source)","https://docs.python.org/3/library/functions.html",False),
 ("P08","The Python Standard Library, Built-in Exceptions - UnboundLocalError, RecursionError, ZeroDivisionError (Python 3.14.4 documentation source)","https://docs.python.org/3/library/exceptions.html",False),
 ("P09","The Python Tutorial, 8. Errors and Exceptions - handling exceptions (Python 3.14.4 documentation source)","https://docs.python.org/3/tutorial/errors.html",False),
 ("P10","What's New In Python 3.14 - PEP 649 and PEP 749 deferred annotations, PEP 758 except without brackets (Python documentation source)","https://docs.python.org/3/whatsnew/3.14.html",False),
 ("P11","PEP 649 - Deferred Evaluation Of Annotations Using Descriptors (Hastings, 2021; Python 3.14)","https://peps.python.org/pep-0649/",False),
 ("P12","PEP 758 - Allow except and except* expressions without parentheses (Galindo Salgado and Cannon, 2024; Python 3.14)","https://peps.python.org/pep-0758/",False),
 ("P13","PEP 570 - Python Positional-Only Parameters (Hastings et al., 2018; Python 3.8)","https://peps.python.org/pep-0570/",False),
 ("P14","PEP 3102 - Keyword-Only Arguments (Talin, 2006; Python 3.0)","https://peps.python.org/pep-3102/",False),
 ("P15","PEP 3104 - Access to Names in Outer Scopes (Yee, 2006; Python 3.0)","https://peps.python.org/pep-3104/",False),
 ("P16","PEP 8 - Style Guide for Python Code (van Rossum, Warsaw and Coghlan, 2001)","https://peps.python.org/pep-0008/",False),
]
CONCEPTS = [("Section",x) for x in ("Creating Functions","Arguments and Parameters","Return Values and return Statements","The None Value","Named Parameters","The Call Stack","Local and Global Scopes","Scope Rules","The global Statement","Scope Identification","Exception Handling","A Short Program: Zigzag","A Short Program: Spike","Summary","Practice Questions")] + \
 [("Concept",x) for x in ("function","function call","deduplication","argument","parameter","return value","call stack","frame object","local scope","global scope","black box","exception","traceback")] + \
 [("Statement",x) for x in ("def","return","global","try","except")] + [("Value","None")] + [("Function",x) for x in ("print()","input()","len()")]
FINDINGS = [
 ("F1","Background","Chapter 4 of the 3rd edition teaches functions: the def statement that defines one and the call that runs it, arguments passed into parameters, return values and the None value, named parameters such as print's sep and end, the call stack that remembers where each call returns to, the local and the global scope and four rules for telling them apart, the global statement, and try and except for recovering from an error, closing with two short animation programs.",["P01"]),
 ("F2","Comparative analysis","One printed output of the chapter has changed: it shows UnboundLocalError: local variable 'eggs' referenced before assignment, while Python 3.14.4 says cannot access local variable 'eggs' where it is not associated with a value, the wording the Programming FAQ now prints; the class, its parent NameError and the cause are unchanged, and the chapter's other printed error messages, NameError and ZeroDivisionError, are the same under 3.14.4.",["P01","P04","P08"]),
 ("F3","Comparative analysis","The chapter's copy-and-paste listing, which it shows to argue for functions, is not equivalent to the function version it stands for: its last line is print(' Good evening!') with a leading space, so running the two programs gives outputs that differ in exactly that line - which is the maintenance hazard of duplicated code the passage warns about.",["P01"]),
 ("F4","Comparative analysis","The reference documentation explains why the chapter's fourth scope rule and its UnboundLocalError follow from one fact: which names are local is decided by scanning the whole function body for name-binding operations, so an assignment anywhere in a function makes the name local everywhere in it; the standard library's symtable module shows the decision - the same name eggs is global in a function with a global statement, local in one that assigns it, and global in one that only reads it.",["P03","P05","P04"]),
 ("F5","Contemporary developments","Beyond the chapter, a function's parameters can be positional-only, with a slash, or keyword-only, with a star, and calling them the wrong way raises a TypeError that names the problem; a default argument value is evaluated once, so a mutable default such as an empty list is shared between calls and the tutorial's remedy is a default of None; and nonlocal lets an inner function rebind a name of the enclosing function, the middle case between local and global that the chapter does not cover.",["P02","P13","P14","P15","P05"]),
 ("F6","Contemporary developments","Python 3.14 changed two things a course on functions meets: annotations on a function are no longer evaluated when it is defined, so a function annotated with names that do not exist yet can be defined and called, and reading its annotations raises NameError until they are evaluated on request; and except may list several exception types without brackets when no as clause is used, which 3.13 and earlier reject.",["P10","P11","P12"]),
 ("F7","Comparative analysis","The chapter's call-stack example reproduces line for line, and the stack itself can be looked at from the program: the standard library's traceback module lists the frames a call is running inside, and the interpreter refuses to grow the stack without end - the recursion limit is 1000 and a function that calls itself forever raises RecursionError, a subclass of RuntimeError, rather than crashing.",["P01","P06","P08"]),
 ("F8","Conclusion","For an advanced course, chapter 4 is best taught as name resolution seen from the function: a call creates a scope, the compiler decides which names in it are local, the call stack holds the scopes that are waiting, and try and except decide where in that stack an error is handled; the book's rules are the four cases of one lookup rule, the printed messages should be regenerated under the Python in use, and parameters, defaults, nonlocal, annotations and the 3.14 except syntax are what the chapter leaves for the course to add.",["P01","P03","P10"]),
]
# (top, mid, leaf, exemplar, definition, io-or-None)
TAX = [
 ("Function","Definition","DefStatement","def hello():","A def statement creates a function and binds its name; the body runs when the function is called, not when it is defined.",None),
 ("Function","Definition","FunctionCall","hello()","A call is the function's name followed by parentheses, with any arguments inside, and execution jumps into the body and comes back.",None),
 ("Function","Definition","Deduplication","one def, three calls","A function groups code that runs more than once, so a fix is made in one place instead of in every pasted copy.",None),
 ("Function","Parameters","ParameterAndArgument","say_hello_to('Alice')","An argument is the value passed in a call, a parameter is the variable that receives it, and the parameter is forgotten when the function returns.",None),
 ("Function","Parameters","NamedParameter","print('a', 'b', sep=',')","A named parameter is identified by its name in the call rather than its position; print's sep and end are two.",("(lambda b: (print('cats', 'dogs', 'mice', sep=',', file=b), b.getvalue())[1])(__import__('io').StringIO())","'cats,dogs,mice\\n'")),
 ("Function","Parameters","PositionalOnlyParameter","def f(a, /, b):","Parameters before a slash can only be passed by position; passing one by name raises a TypeError.",("(lambda a, /, b: a * b)(3, b=4)","12")),
 ("Function","Parameters","KeywordOnlyParameter","def f(a, *, b=2):","Parameters after a star can only be passed by name, so a call cannot get them wrong by position.",("(lambda a, *, b=2: a + b)(1, b=5)","6")),
 ("Function","Parameters","DefaultArgument","def f(a, L=None):","A default value is evaluated once, when the function is defined, so a mutable default is shared between calls; the tutorial's remedy is a default of None.",None),
 ("Result","ReturnValue","ReturnStatement","return 42 / divide_by","A return statement leaves the function with the value of its expression, so a call can be used wherever a value can.",("(lambda d: 42 / d)(2)","21.0")),
 ("Result","ReturnValue","ImplicitNone","def f(): pass","A function without a return statement, or with a bare return, returns None.",("(lambda: None)() is None","True")),
 ("Result","NoneType","NoneValue","spam = print('Hello!')","None is the only value of NoneType and stands for the absence of a value; print returns it, and PEP 8 says to compare with is.",("type(None).__name__","'NoneType'")),
 ("Frames","CallStack","CallStackOrder","a() calls b() calls c()","Python remembers which line called a function so that execution returns there, keeping the waiting calls on a stack of frames.",("len(str(42 / 2))","4")),
 ("Frames","CallStack","StackInspection","traceback.extract_stack()","A program can list the frames it is running inside, and the interpreter stops a runaway chain of calls with a RecursionError.",("__import__('sys').getrecursionlimit()","1000")),
 ("Scope","Namespaces","LocalScope","eggs = 'sss' inside spam()","A variable assigned inside a function exists only in that call's local scope and is destroyed when the call returns.",None),
 ("Scope","Namespaces","GlobalScope","eggs = 'global' outside all functions","There is one global scope, created when the program begins and destroyed when it ends, and code in any function can read its variables.",None),
 ("Scope","Namespaces","SameNameVariables","three variables named eggs","The same name in different scopes gives different variables; the book advises unique names to keep track of them.",None),
 ("Scope","Rules","GlobalStatement","global eggs","A global statement makes a name in the function refer to the global variable, so assigning to it changes the global.",None),
 ("Scope","Rules","ScopeIdentification","four rules for eggs","A name is global if used outside all functions or declared global, local if the function assigns it, and global if the function only reads it.",None),
 ("Scope","Rules","UnboundLocalError","print(eggs) before eggs = 'spam local'","Using a local variable before it is assigned raises UnboundLocalError, whose message in 3.14 reads cannot access local variable where it is not associated with a value.",None),
 ("Scope","Rules","NonlocalStatement","nonlocal n","A nonlocal statement lets an inner function rebind a name of the enclosing function, between the local and the global case.",None),
 ("ErrorHandling","Exceptions","TryExcept","try: ... except ZeroDivisionError:","Code in a try clause that raises an error jumps to the matching except clause, and execution continues after the try statement.",None),
 ("ErrorHandling","Exceptions","ErrorInCall","the try block around spam(0)","An error raised inside a function called from a try clause is caught by that clause, and execution does not return into the try clause.",None),
 ("ErrorHandling","Exceptions","MultipleExceptTypes","except A, B:","Since Python 3.14 an except clause can list several exception types without brackets when it has no as clause.",None),
 ("ModernPractice","Annotations","DeferredAnnotations","def f(x: Undefined):","Since Python 3.14 a function's annotations are not evaluated at definition, so names that do not exist yet can be used and are looked up only on request.",None),
 ("ModernPractice","Style","BlackBoxFunction","use it without reading it","A function can be treated as a black box: its parameters go in, its return value comes out, and its local variables affect nothing else.",None),
]
ERRORS = []
# Checked by sen0414_rdodi_checks: each is executed under the interpreter and compared with the text that states it.
CLAIMS = [
 ("[len('-' * (i * i)) for i in list(range(1, 9)) + list(range(7, 1, -1))]", "[1, 4, 9, 16, 25, 36, 49, 64, 49, 36, 25, 16, 9, 4]"),
 ("[42 / d for d in (2, 12, 1)]", "[21.0, 3.5, 42.0]"),
 ("(3 * 3 + 1, 10 // 2, 5 * 3 + 1, 16 // 2, 8 // 2, 4 // 2, 2 // 2)", "(10, 5, 16, 8, 4, 2, 1)"),
 ("issubclass(UnboundLocalError, NameError), issubclass(RecursionError, RuntimeError), issubclass(ZeroDivisionError, ArithmeticError)", "(True, True, True)"),
 ("' Good evening!' == 'Good evening!'", "False"),
]
S = "(Sweigart, 2025)"; PSF = "(Python Software Foundation, 2026)"; HA = "(Hastings, 2021)"; GC = "(Galindo Salgado and Cannon, 2024)"; HP = "(Hastings et al., 2018)"; TA = "(Talin, 2006)"; YE = "(Yee, 2006)"; VW = "(Van Rossum et al., 2001)"
BODY = {
 "Function": "Chapter 4 is about giving a block of code a name so it can be run from many places, passing values in, getting a value out, and keeping its variables to itself %s." % S,
 "Definition": "Creating Functions introduces the def statement and the call that runs it, and the reason for both: not repeating code %s." % S,
 "DefStatement": "A def statement defines a function named hello() and the indented block after it is the body; that code executes when the function is called, not when it is first defined %s." % S,
 "FunctionCall": "A function call is the function's name followed by parentheses, possibly with arguments between them; execution jumps to the first line of the body and returns to the line after the call when the body ends %s." % S,
 "Deduplication": "A major purpose of functions is to group code that gets executed multiple times, because with pasted copies a fix has to be made in every place; the chapter's own pasted listing ends with print(' Good evening!') with a stray leading space, so its output differs from the function version's last line %s." % S,
 "Parameters": "Arguments and Parameters and Named Parameters describe how values get into a function %s." % S,
 "ParameterAndArgument": "Values passed in a call are arguments and the variables that receive them are parameters, as in def say_hello_to(name) called with say_hello_to('Alice'); the value in a parameter is forgotten when the function returns, so print(name) after the call raises an error %s." % S,
 "NamedParameter": "Python identifies most arguments by position but named parameters by the name placed before them, so print('Hello', end='') prints no newline and print('cats', 'dogs', 'mice', sep=',') prints cats,dogs,mice; print's documentation makes sep, end, file and flush keyword-only %s %s." % (S, PSF),
 "PositionalOnlyParameter": "Parameters listed before a slash in a definition can only be passed by position, so calling such a function with the name raises a TypeError that says some positional-only arguments were passed as keyword arguments %s." % HP,
 "KeywordOnlyParameter": "Parameters listed after a star in a definition can only be passed by keyword, so passing one by position raises a TypeError, which turns a call that could be misread into a call that cannot %s." % TA,
 "DefaultArgument": "A default value is evaluated only once, when the function is defined, so a default such as an empty list accumulates the arguments of successive calls, and the tutorial's remedy is a default of None that the function replaces with a new list %s." % PSF,
 "Result": "Return Values and return Statements and The None Value describe what a call evaluates to %s." % S,
 "ReturnValue": "The value a function call evaluates to is its return value, and because a call is an expression it can be an argument to another call, as in print(get_answer(random.randint(1, 9))) %s." % S,
 "ReturnStatement": "A return statement consists of the return keyword and the value or expression to return; if an expression list is present it is evaluated, else None is substituted, and control leaves the function %s." % PSF,
 "ImplicitNone": "Behind the scenes Python adds return None to the end of any function with no return statement, and a bare return also returns None %s." % S,
 "NoneType": "The None value stands for the absence of a value and is the only value of the NoneType data type %s." % S,
 "NoneValue": "None is the return value of print, so spam = print('Hello!') stores it, and PEP 8 says comparisons to singletons like None should always be done with is or is not, not with equality operators, where the chapter writes None == spam %s %s." % (S, VW),
 "Frames": "The Call Stack explains where execution goes when a function returns %s." % S,
 "CallStack": "Calling a function does not send execution one way to the top of the body: Python remembers the line that made the call, so abcdCallStack.py prints a() starts, b() starts, c() starts, c() returns, b() returns, d() starts, d() returns, a() returns %s." % S,
 "CallStackOrder": "Frame objects are added to and removed from the top of the call stack only, the top frame is the function currently executing, and an empty stack means execution is outside all functions %s." % S,
 "StackInspection": "The interpreter limits the depth of its stack, sys.getrecursionlimit() returns 1000 under Python 3.14.4, and a function that calls itself without end raises RecursionError, a subclass of RuntimeError, instead of overflowing the C stack %s." % PSF,
 "Scope": "Local and Global Scopes, Scope Rules, The global Statement and Scope Identification say which variable a name refers to %s." % S,
 "Namespaces": "Variables live in scopes, containers created when a program starts or a function is called %s." % S,
 "LocalScope": "Variables assigned inside a function exist in that call's local scope, which is created when the function is called and destroyed when it returns, so code outside cannot use them and print(eggs) after spam() raises NameError: name 'eggs' is not defined %s." % S,
 "GlobalScope": "There is only one global scope, created when the program begins and destroyed when it terminates, and code in a local scope can read global variables when it has no local variable of that name %s." % S,
 "SameNameVariables": "A local variable and a global one may share a name, so three variables named eggs give the output bacon local, spam local, bacon local, global, and the chapter advises giving variables unique names %s." % S,
 "Rules": "Four rules tell whether a name is local or global, and one further statement reaches the case between them %s." % S,
 "GlobalStatement": "Putting global eggs at the top of a function makes eggs in that function refer to the global variable, so assigning to it changes the global and no local variable is created %s." % S,
 "ScopeIdentification": "A variable outside all functions is global, one in a function with a global statement is global, one the function assigns is local, and one the function only uses is global; the compiler decides this by scanning the whole function body for name-binding operations, which the symtable module reports as global, local and global for the chapter's spam, bacon and ham %s." % PSF,
 "UnboundLocalError": "Using a local variable before assigning it raises UnboundLocalError, a subclass of NameError; the chapter prints local variable 'eggs' referenced before assignment, while Python 3.14.4 and the Programming FAQ give cannot access local variable 'eggs' where it is not associated with a value %s." % PSF,
 "NonlocalStatement": "The nonlocal statement causes the listed names to refer to names previously bound in the nearest enclosing function scope, which lets an inner function rebind them; the chapter does not cover it %s." % YE,
 "ErrorHandling": "Exception Handling turns an error from a crash into something a program can recover from %s." % S,
 "Exceptions": "An error in a Python program raises an exception, and try and except statements decide what happens next %s." % S,
 "TryExcept": "The try clause runs first; if no exception occurs the except clause is skipped, and if one occurs the rest of the try clause is skipped and, when its type matches, the except clause runs and execution continues after the try statement %s." % PSF,
 "ErrorInCall": "An error inside a function called from a try clause is caught by that clause, and once execution has jumped to the except clause it does not return to the try clause, so the chapter's second version never prints spam(1) %s." % S,
 "MultipleExceptTypes": "Python 3.14 allows except to list several exception types without brackets when there is no as clause, as in except TimeoutError, ConnectionRefusedError:, and rejects the form with as unless the types are in brackets %s." % GC,
 "ModernPractice": "An advanced course pairs the chapter's functions with what current Python adds around them %s." % PSF,
 "Annotations": "Annotations on a function's parameters and result are the newest of those additions %s." % HA,
 "DeferredAnnotations": "Since Python 3.14 annotations are stored and evaluated only when necessary, so def f(x: Undefined) can be defined and called, reading f.__annotations__ raises NameError until the names exist, and a forward-reference format returns the unresolved names %s." % HA,
 "Style": "How a function is meant to be used matters as much as how it is written %s." % S,
 "BlackBoxFunction": "Often all you need to know about a function is its inputs and its return value, so it can be treated as a black box, and because its variables are local its code cannot affect other functions' variables %s." % S,
}
BEH = [
 [
  "UnboundLocalError message in 3.14",
  "def spam():\n    print(eggs)\n    eggs = 'spam local'\neggs = 'global'\ntry:\n    spam()\nexcept UnboundLocalError as e:\n    print(type(e).__name__ + ': ' + str(e), issubclass(UnboundLocalError, NameError))",
  "UnboundLocalError: cannot access local variable 'eggs' where it is not associated with a value True"
 ],
 [
  "global code cannot use a local",
  "def spam():\n    eggs = 'sss'\nspam()\ntry:\n    print(eggs)\nexcept NameError as e:\n    print(e)",
  "name 'eggs' is not defined"
 ],
 [
  "copy vs function",
  "import io, contextlib\ndef out(src):\n    b = io.StringIO()\n    with contextlib.redirect_stdout(b): exec(src, {})\n    return b.getvalue()\nf1 = 'def hello():\\n    print(\"Good morning!\")\\n    print(\"Good afternoon!\")\\n    print(\"Good evening!\")\\nhello()\\nhello()\\nprint(\"ONE MORE TIME!\")\\nhello()\\n'\nf2 = 'print(\"Good morning!\")\\nprint(\"Good afternoon!\")\\nprint(\"Good evening!\")\\nprint(\"Good morning!\")\\nprint(\"Good afternoon!\")\\nprint(\"Good evening!\")\\nprint(\"ONE MORE TIME!\")\\nprint(\"Good morning!\")\\nprint(\"Good afternoon!\")\\nprint(\" Good evening!\")\\n'\na, b = out(f1), out(f2)\nprint(a == b, [(x, y) for x, y in zip(a.splitlines(), b.splitlines()) if x != y])",
  "False [('Good evening!', ' Good evening!')]"
 ],
 [
  "implicit return None",
  "def f():\n    pass\ndef g():\n    return\nprint(f() is None, g() is None, type(f()).__name__)",
  "True True NoneType"
 ],
 [
  "mutable default",
  "def f(a, L=[]):\n    L.append(a)\n    return L\nfor i in (1, 2, 3): print(f(i))\ndef g(a, L=None):\n    if L is None:\n        L = []\n    L.append(a)\n    return L\nprint(g(1), g(2))",
  "[1]\n[1, 2]\n[1, 2, 3]\n[1] [2]"
 ],
 [
  "scope by symtable",
  "import symtable\nsrc = 'def spam():\\n    global eggs\\n    eggs = 1\\ndef bacon():\\n    eggs = 2\\ndef ham():\\n    print(eggs)\\neggs = 3\\n'\nt = symtable.symtable(src, 'x', 'exec')\nprint([('G' if c.lookup('eggs').is_global() else 'L') for c in t.get_children() if c.get_name() in ('spam', 'bacon', 'ham')])",
  "['G', 'L', 'G']"
 ],
 [
  "recursion",
  "import sys\ndef f():\n    return f()\ntry:\n    f()\nexcept RecursionError as e:\n    print(sys.getrecursionlimit(), type(e).__name__, str(e), issubclass(RecursionError, RuntimeError))",
  "1000 RecursionError maximum recursion depth exceeded True"
 ],
 [
  "call order",
  "def a():\n    print('a() starts')\n    b()\n    d()\n    print('a() returns')\ndef b():\n    print('b() starts')\n    c()\n    print('b() returns')\ndef c():\n    print('c() starts')\n    print('c() returns')\ndef d():\n    print('d() starts')\n    print('d() returns')\na()",
  "a() starts\nb() starts\nc() starts\nc() returns\nb() returns\nd() starts\nd() returns\na() returns"
 ],
 [
  "call stack depth",
  "import traceback\ndef a(): return b()\ndef b(): return c()\ndef c(): return [f.name for f in traceback.extract_stack()][-3:]\nprint(a())",
  "['a', 'b', 'c']"
 ],
 [
  "three eggs",
  "def spam():\n    eggs = 'spam local'\n    print(eggs)\ndef bacon():\n    eggs = 'bacon local'\n    print(eggs)\n    spam()\n    print(eggs)\neggs = 'global'\nbacon()\nprint(eggs)",
  "bacon local\nspam local\nbacon local\nglobal"
 ],
 [
  "global stmt",
  "def spam():\n    global eggs\n    eggs = 'spam'\neggs = 'global'\nspam()\nprint(eggs)",
  "spam"
 ],
 [
  "nonlocal",
  "def outer():\n    n = 0\n    def inner():\n        nonlocal n\n        n += 1\n    inner(); inner()\n    return n\nprint(outer())",
  "2"
 ],
 [
  "try in function",
  "def spam(divide_by):\n    try:\n        return 42 / divide_by\n    except ZeroDivisionError:\n        print('Error: Invalid argument.')\nprint(spam(2))\nprint(spam(12))\nprint(spam(0))\nprint(spam(1))",
  "21.0\n3.5\nError: Invalid argument.\nNone\n42.0"
 ],
 [
  "try around calls",
  "def spam(divide_by):\n    return 42 / divide_by\ntry:\n    print(spam(2))\n    print(spam(12))\n    print(spam(0))\n    print(spam(1))\nexcept ZeroDivisionError:\n    print('Error: Invalid argument.')",
  "21.0\n3.5\nError: Invalid argument."
 ],
 [
  "print params",
  "import io\nb = io.StringIO()\nprint('Hello', end='', file=b)\nprint('World', file=b)\nprint('cats', 'dogs', 'mice', sep=',', file=b)\nprint(repr(b.getvalue()))",
  "'HelloWorld\\ncats,dogs,mice\\n'"
 ],
 [
  "pep758",
  "compile('try:\\n    1/0\\nexcept ZeroDivisionError, ValueError:\\n    pass\\n', 'x', 'exec')\nprint('ok')\ntry:\n    compile('try:\\n    pass\\nexcept ZeroDivisionError, ValueError as e:\\n    pass\\n', 'x', 'exec')\nexcept SyntaxError as e:\n    print(e.msg)",
  "ok\nmultiple exception types must be parenthesized when using 'as'"
 ],
 [
  "annotations",
  "import annotationlib\ndef f(x: Undefined) -> Missing:\n    return x\nprint(f(3))\ntry:\n    f.__annotations__\nexcept NameError as e:\n    print('NameError', e)\nprint(sorted(annotationlib.get_annotations(f, format=annotationlib.Format.FORWARDREF)))",
  "3\nNameError name 'Undefined' is not defined\n['return', 'x']"
 ],
 [
  "param kinds",
  "g = lambda a, /, b: a * b\nh = lambda a, *, b=2: a + b\nprint(g(3, b=4), h(1, b=5))\nfor call in (lambda: g(a=3, b=4), lambda: h(1, 5)):\n    try: call()\n    except TypeError as e: print(e)",
  "12 6\n<lambda>() got some positional-only arguments passed as keyword arguments: 'a'\n<lambda>() takes 1 positional argument but 2 were given"
 ],
 [
  "collatz",
  "def collatz(number):\n    if number % 2 == 0:\n        print(number // 2, end=' ')\n        return number // 2\n    print(3 * number + 1, end=' ')\n    return 3 * number + 1\nn = 3\nprint(n, end=' ')\nwhile n != 1:\n    n = collatz(n)\nprint()",
  "3 10 5 16 8 4 2 1"
 ],
 [
  "int puppy",
  "try:\n    int('puppy')\nexcept ValueError as e:\n    print(e)",
  "invalid literal for int() with base 10: 'puppy'"
 ],
 [
  "zigzag",
  "indent = 0\nup = True\nseq = []\nfor step in range(41):\n    seq.append(indent)\n    if up:\n        indent += 1\n        if indent == 20: up = False\n    else:\n        indent -= 1\n        if indent == 0: up = True\nprint(seq[0], seq[20], seq[40], max(seq))",
  "0 20 0 20"
 ]
]
BEH.append(("ZeroDivisionError message is the book's", "def spam(divide_by):\n    return 42 / divide_by\ntry:\n    spam(0)\nexcept ZeroDivisionError as e:\n    print(type(e).__name__ + ': ' + str(e))", "ZeroDivisionError: division by zero"))
