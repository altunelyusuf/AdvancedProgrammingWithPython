"""Chapter 4 deck examples, version 3.1.0: the code examples of the chapter 4 lecture deck (Functions).
One example per code slide, in slide order. The `groups` are the code boxes of the slide (each with the plain-language
explanation that stands beside it); the lines of all groups of an example, in order, are the example's code: that text is
what the deck shows after the '>>> ' prompt of each line, what the chapter-code manifest lists and what the page runs.
Every example is self-contained, uses only the Python standard library, reads no keyboard input and prints nothing that
depends on the Python version (no error message texts, no tracebacks). Nothing here carries a result; deck_build_v3_1_0.py
runs the code and takes every printed result from the run."""
__version__ = "3.1.0"

EXAMPLES = [
    # ---------------------------------------------------------------- part 1: defining and calling
    dict(id="hello", name="def defines, a call runs", title="def defines a function; a call runs it", part=1, visual="hello",
         concepts=["Creating Functions", "function", "function call", "def"],
         groups=[
             (["def hello(name):", "    print('Hello, ' + name)"],
              "def starts the definition. The indented lines are the body. Nothing runs yet: the function is only stored."),
             (["hello('Alice')", "hello('Bob')"],
              "Each call runs the body once, with name set to the argument. Two calls print two greetings."),
         ]),
    dict(id="dedup", name="Deduplication: one function instead of copies", title="Deduplication: a function replaces copied code", part=1, visual="dedup", layout="below",
         concepts=["deduplication", "Creating Functions"],
         groups=[
             (["pasted = ['Good morning!', 'Good afternoon!', ' Good evening!']"],
              "Imagine the same lines copied three times. One copy has a stray space and nobody notices it."),
             (["def greeting(part):", "    return 'Good ' + part + '!'"],
              "One function holds the text once. The part of the day is the only thing that changes."),
             (["made = [greeting(p) for p in ('morning', 'afternoon', 'evening')]", "print(pasted == made, [a == b for a, b in zip(pasted, made)])"],
              "Compare the copies with the function. Only the pasted line with the stray space differs."),
         ]),
    dict(id="params", name="Arguments fill parameters in order", title="Arguments fill the parameters, in order", part=1, visual="params",
         concepts=["Arguments and Parameters", "argument", "parameter"],
         groups=[
             (["def describe(animal, sound):", "    return animal + ' says ' + sound"],
              "animal and sound are parameters: the names in the def line. They stay empty until a call fills them."),
             (["print(describe('cat', 'meow'))", "print(describe('meow', 'cat'))"],
              "The values in the call are arguments. They fill the parameters by position, so swapping them swaps the meaning."),
         ]),
    dict(id="returns", name="return hands a value back", title="return hands a value back to the caller", part=1, visual="returns",
         concepts=["Return Values and return Statements", "return value", "return"],
         groups=[
             (["def double(n):", "    return n * 2"],
              "return ends the call and hands a value back. The call expression then stands for that value."),
             (["x = double(21)", "print(x, type(x).__name__)", "print(double(double(2)))"],
              "The call double(21) is replaced by 42, which is stored in x. Calls can be nested; the inner call runs first."),
         ]),
    dict(id="none", name="None: a function without return", title="None: what a function gives back without return", part=1, visual="none",
         concepts=["The None Value", "None", "len()", "print()"],
         groups=[
             (["def shout(word):", "    print(word.upper())"],
              "This function prints, but it has no return statement. It does its work and hands nothing back."),
             (["result = shout('hi')", "print(result, result is None)", "print(len('hello'), len([1, 2, 3]))"],
              "Python hands back the value None. The built-in len does return a value: the length."),
         ]),
    dict(id="named", name="Named parameters sep and end", title="Named parameters: sep and end of print()", part=1, visual="named",
         concepts=["Named Parameters", "print()"],
         groups=[
             (["print('cats', 'dogs', 'mice')", "print('cats', 'dogs', 'mice', sep=', ')"],
              "print puts a space between values. The named parameter sep chooses another separator."),
             (["print('Hello', end='')", "print(' World')"],
              "The named parameter end replaces the newline that print adds. The two calls make one line."),
         ]),
    dict(id="defaults", name="Default and keyword-only parameters", title="Default values and keyword-only parameters", part=1, visual="defaults",
         concepts=["Named Parameters", "parameter"],
         groups=[
             (["def area(width, height=1, *, unit='m'):", "    return str(width * height) + ' ' + unit"],
              "height has a default, so a call may leave it out. The star makes unit keyword-only: it must be named."),
             (["print(area(3), area(3, 4), area(3, unit='cm'))"],
              "Three calls fill the parameters in three ways. The default and the name decide the result."),
         ]),
    dict(id="mutable", name="A default value is made once", title="A default value is made once: the shared list", part=1, visual="mutable",
         concepts=["parameter", "Named Parameters"],
         groups=[
             (["def add_item(item, bag=[]):", "    bag.append(item)", "    return bag"],
              "The empty list is created once, when def runs. Every call without bag reuses that same list."),
             (["def add_safe(item, bag=None):", "    bag = [] if bag is None else bag", "    bag.append(item)", "    return bag"],
              "The safe habit: default to None and make a fresh list inside the body, once per call."),
             (["print(add_item('a'), add_item('b'))", "print(add_safe('a'), add_safe('b'))"],
              "The first pair shares one list, so both results show both items. The second pair is separate."),
         ]),
    # ---------------------------------------------------------------- part 2: call stack and scope
    dict(id="stack", name="The call stack counted with real frames", title="The call stack: one frame for every active call", part=2, visual="stack",
         concepts=["The Call Stack", "call stack"],
         groups=[
             (["import inspect", "base = len(inspect.stack())", "depth = lambda: len(inspect.stack()) - base - 1"],
              "inspect.stack lists every waiting frame. depth counts them above the top level; the minus 1 leaves out the lambda's own frame."),
             (["def c():", "    return depth()", "def b():", "    return [depth(), c()]", "def a():", "    return [depth(), b()]"],
              "a calls b and b calls c. Each one reports how many calls are waiting: its depth in the stack."),
             (["print(a(), depth())"],
              "a is at depth 1, b at 2, c at 3. Back at the top level the stack is empty again: depth 0."),
         ]),
    dict(id="frame", name="A frame object knows its function and its caller", title="A frame object knows its function and its caller", part=2, visual="frame",
         concepts=["frame object", "call stack"],
         groups=[
             (["import sys", "def inner():", "    me, caller = sys._getframe(), sys._getframe(1)", "    return me.f_code.co_name, caller.f_code.co_name"],
              "sys._getframe gives the frame object of a running call. Its f_code.co_name is the name of the function."),
             (["def outer():", "    return inner()", "print(outer(), inner()[0])"],
              "outer called inner, so the caller frame of inner is the frame of outer."),
         ]),
    dict(id="localgone", name="A local variable disappears after the call", title="A local variable lives only during its call", part=2, visual="localgone",
         concepts=["Local and Global Scopes", "local scope", "global scope"],
         groups=[
             (["def make():", "    eggs = 99", "    return eggs"],
              "eggs is created when make is called and thrown away when the call returns. It is a local variable."),
             (["print(make())", "try:", "    print(eggs)", "except NameError as err:", "    print(type(err).__name__)"],
              "Outside the function the name eggs does not exist, so the lookup raises a NameError."),
         ]),
    dict(id="walls", name="Local scopes are walled off", title="Local scopes are walled off; globals can be read", part=2, visual="walls",
         concepts=["Scope Rules", "local scope", "global scope"],
         groups=[
             (["x = 'global x'", "def f():", "    y = 'local y of f'", "    return x", "def g():", "    return y"],
              "f reads the global x. g tries to read y, but y belongs to the local scope of f, not to g."),
             (["print(f())", "try:", "    g()", "except NameError as err:", "    print('g cannot see y:', type(err).__name__)"],
              "f works because globals are visible everywhere. g fails: one local scope cannot see another."),
         ]),
    dict(id="samename", name="One name, three variables", title="The same name can be three different variables", part=2, visual="samename",
         concepts=["Scope Rules", "local scope", "global scope"],
         groups=[
             (["spam = 'global'", "def one():", "    spam = 'one'", "    return spam", "def two():", "    spam = 'two'", "    return spam"],
              "Each function assigns spam, so each gets its own local spam. The global spam is a third, separate variable."),
             (["print(one(), two(), spam)"],
              "Three lookups of the name spam give three different values. They do not disturb each other."),
         ]),
    dict(id="globalstmt", name="The global statement", title="The global statement reaches the global variable", part=2, visual="globalstmt",
         concepts=["The global Statement", "global"],
         groups=[
             (["eggs = 'global'", "def with_global():", "    global eggs", "    eggs = 'changed by with_global'", "def without_global():", "    eggs = 'local to without_global'"],
              "global eggs says: this name means the global variable. Without it, an assignment makes a new local variable."),
             (["without_global()", "print(eggs)", "with_global()", "print(eggs)"],
              "The first call leaves the global variable untouched. The second call really changes it."),
         ]),
    dict(id="nonlocal", name="nonlocal: between local and global", title="nonlocal: the middle case between local and global", part=2, visual="nonlocal",
         concepts=["Scope Rules", "local scope", "global scope"],
         groups=[
             (["def counter():", "    count = 0", "    def step():", "        nonlocal count", "        count += 1", "        return count", "    return step"],
              "step changes count, a variable of the enclosing function. nonlocal says: not my own, and not global, but the one outside."),
             (["tick = counter()", "print(tick(), tick(), tick())"],
              "The function step keeps its own count alive between calls. Each call adds one to that same variable."),
         ]),
    dict(id="identify", name="Scope identification: read or assign", title="Scope identification: does the body read or assign?", part=2, visual="identify",
         concepts=["Scope Identification", "Scope Rules"],
         groups=[
             (["eggs = 0", "def reads():", "    return eggs", "def assigns():", "    eggs = 1"],
              "reads only looks at eggs. assigns gives eggs a value, which makes it local to assigns."),
             (["def declares():", "    global eggs", "    eggs = 2", "for f in (reads, assigns, declares):", "    c = f.__code__", "    print(f.__name__, c.co_varnames, c.co_names)"],
              "co_varnames lists the local variables; co_names lists the global names a function uses. Python decides by scanning the body."),
         ]),
    dict(id="unbound", name="UnboundLocalError", title="Assign later, crash earlier: UnboundLocalError", part=2, visual="unbound",
         concepts=["Scope Rules", "Scope Identification", "local scope"],
         groups=[
             (["eggs = 'global'", "def broken():", "    print(eggs)", "    eggs = 'local'"],
              "The body assigns eggs, so the whole function treats eggs as local, even in the line before the assignment."),
             (["print('global eggs is still', eggs)", "try:", "    broken()", "except NameError as err:", "    kind = type(err)", "    print(kind.__name__, kind.__mro__[1].__name__)"],
              "The global eggs is untouched, so the first line prints it. Inside broken the read happens before any value exists: Python raises UnboundLocalError, and its parent class is NameError."),
         ]),
    # ---------------------------------------------------------------- part 3: errors
    dict(id="tryexcept", name="try and except", title="try and except recover from an error", part=3, visual="tryexcept",
         concepts=["Exception Handling", "exception", "try", "except"],
         groups=[
             (["def spam(divide_by):", "    try:", "        return 42 / divide_by", "    except ZeroDivisionError:", "        return 'error: cannot divide by zero'"],
              "The try block runs normally. If it raises ZeroDivisionError, the except block runs instead of a crash."),
             (["print(spam(2), spam(12), spam(0), spam(1))"],
              "The call with 0 does not stop the program. It hands back the message, and the next call still runs."),
         ]),
    dict(id="inloop", name="try inside the loop", title="Where the try goes (1): inside the loop", part=3, visual="inloop",
         concepts=["Exception Handling", "try", "except"],
         groups=[
             (["def spam(n):", "    return 42 / n"],
              "This function has no try of its own, so an error inside it travels up to the caller."),
             (["for n in (2, 0, 1):", "    try:", "        print(spam(n))", "    except ZeroDivisionError:", "        print('Error: invalid argument.')"],
              "try is inside the loop: n = 0 fails and is handled, and n = 1 still runs afterwards."),
         ]),
    dict(id="aroundall", name="try around all the calls", title="Where the try goes (2): around all the calls", part=3, visual="aroundall",
         concepts=["Exception Handling", "try", "except"],
         groups=[
             (["def spam(n):", "    return 42 / n"],
              "The same function. This time the try sits outside, around three separate calls."),
             (["try:", "    print(spam(2))", "    print(spam(0))", "    print(spam(1))", "except ZeroDivisionError:", "    print('Error: invalid argument.')"],
              "The failure of the second call jumps straight to except. The third call is never started."),
         ]),
    dict(id="several", name="One except for several errors", title="One except for several kinds of error", part=3, visual="several",
         concepts=["exception", "except"],
         groups=[
             (["def parse(text):", "    try:", "        return int(text)", "    except (ValueError, TypeError) as err:", "        return type(err).__name__"],
              "A tuple of types catches either one. as err names the exception object so the handler can look at it."),
             (["print(parse('12'), parse('x'), parse(None))"],
              "The text 12 converts. The text x raises ValueError and None raises TypeError; both are handled."),
         ]),
    dict(id="traceback", name="A traceback lists the calls to the error", title="A traceback lists the calls that led to the error", part=3, visual="traceback",
         concepts=["traceback", "exception", "call stack"],
         groups=[
             (["import traceback", "def inner():", "    return 1 / 0", "def outer():", "    return inner()"],
              "inner divides by zero. outer called inner, so both calls are on the path to the error."),
             (["try:", "    outer()", "except ZeroDivisionError as err:", "    tb = traceback.extract_tb(err.__traceback__)", "    print([f.name for f in tb][-2:])"],
              "The traceback is the saved stack of calls, oldest first. The slice [-2:] keeps the last two: outer and inner."),
         ]),
    # ---------------------------------------------------------------- part 4: programs
    dict(id="zigzag", name="Short program: Zigzag", title="Short program: Zigzag", part=4, visual="zigzag",
         concepts=["A Short Program: Zigzag"],
         groups=[
             (["def zigzag(steps, width=20):", "    indent, move, path = 0, 1, []", "    for _ in range(steps):", "        path.append(indent)", "        indent += move"],
              "Each step records the indent of the band, then moves it one place in the current direction."),
             (["        if indent in (0, width):", "            move = -move", "    return path"],
              "At the right edge or at zero the direction flips. The function returns the indent of every step."),
             (["path = zigzag(42)", "print(path[:8], max(path), path[-2:])", "print(' ' * path[5] + '*' * 8)"],
              "42 steps make one sweep out and back. The last line draws the band of eight stars as it looks at step 5."),
         ]),
    dict(id="spike", name="Short program: Spike", title="Short program: Spike", part=4, visual="spike", layout="below",
         concepts=["A Short Program: Spike"],
         groups=[
             (["lengths = [i * i for i in range(1, 9)]", "lengths += [i * i for i in range(7, 1, -1)]"],
              "The lines of the spike grow as the squares 1 to 64 and shrink again from 49 down to 4."),
             (["print(lengths, len(lengths))", "print('-' * lengths[3])"],
              "The string '-' repeated n times draws one line. Here is the line for the fourth square."),
         ]),
    dict(id="collatz", name="Practice program: Collatz", title="Practice program: the Collatz sequence", part=4, visual="collatz",
         concepts=["Practice Questions", "function"],
         groups=[
             (["def collatz(n):", "    if n % 2 == 0:", "        return n // 2", "    return 3 * n + 1"],
              "One step of the rule: halve an even number, otherwise triple it and add one."),
             (["n, seq = 6, [6]", "while n != 1:", "    n = collatz(n)", "    seq.append(n)", "print(seq, len(seq) - 1)"],
              "Repeat the step until the number reaches 1. Nobody has proved that every start ends there."),
         ]),
]
BY_ID = {e["id"]: e for e in EXAMPLES}


def code_lines(ex):
    return [l for g, _ in ex["groups"] for l in g]


def code_text(ex):
    return "\n".join(code_lines(ex))
