"""Builds the chapter 4 visual specifications by EXECUTING code under the interpreter it is run with. A specification
is data, not a drawing: the deck draws it as native shapes, so no number, message or class name on a diagram was typed.
Five specifications: the call stack as a real line-event record of pushes and pops; the exception hierarchy as the real
method resolution order of the chapter's exception classes; the four scope-identification rules decided by a real
symbol-table run; the parameter kinds as a table of real calls with the real TypeError text of the ones that fail;
and name resolution as the real value a name takes when the same lookup is run with the name bound in each scope.
Usage: visuals_make_v1_0_0.py <out.json>   (run under the Python the course teaches)"""
__version__ = "1.0.0"
import contextlib, io, json, platform, sys, symtable

STACK_SRC = """def outer():
    print('outer starts')
    middle()
    print('outer returns')

def middle():
    print('middle starts')
    inner()
    print('middle returns')

def inner():
    print('inner runs')

outer()
"""


def call_stack():
    """a real record of every call and return of the program, with the stack of function names at each moment"""
    lines = STACK_SRC.rstrip("\n").split("\n")
    steps, buf = [], io.StringIO()

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<prog>":
            return None
        if event in ("call", "return"):
            stack, f = [], frame
            while f is not None and f.f_code.co_filename == "<prog>":
                stack.append("the program" if f.f_code.co_name == "<module>" else f.f_code.co_name + "()")
                f = f.f_back
            stack.reverse()
            if event == "return":
                stack = stack[:-1]
            steps.append({"event": "call" if event == "call" else "return",
                          "func": "the program" if frame.f_code.co_name == "<module>" else frame.f_code.co_name + "()",
                          "line": frame.f_lineno, "stack": stack, "out": buf.getvalue().rstrip("\n").replace("\n", " / ")})
        return tracer

    try:
        sys.settrace(tracer)
        with contextlib.redirect_stdout(buf):
            exec(compile(STACK_SRC, "<prog>", "exec"), {"__name__": "__main__"})
    finally:
        sys.settrace(None)
    steps = [s for s in steps if s["func"] != "the program"]
    return {"kind": "callstack", "code": lines, "steps": steps, "printed": buf.getvalue().rstrip("\n"),
            "caption": "Every call pushes a frame and every return pops one; the stack is what Python uses to find its way back."}


def hierarchy():
    """the real ancestry of the exception classes the chapter raises, read from each class's method resolution order"""
    classes = [ZeroDivisionError, ValueError, NameError, UnboundLocalError, KeyboardInterrupt, SystemExit, RecursionError, TypeError]
    rows = [{"name": c.__name__, "chain": [k.__name__ for k in c.__mro__ if k is not object],
             "under_exception": issubclass(c, Exception)} for c in classes]
    return {"kind": "hierarchy", "root": "BaseException", "rows": rows,
            "caption": "Read each row from the left: the class, then every class it is a kind of. "
                       "Only the two on the right of the line are outside Exception, which is why except Exception does not catch them."}


SYM_SRC = ("def reads_global():\n    print(eggs)\n"
           "def makes_local():\n    eggs = 'local'\n    print(eggs)\n"
           "def declares_global():\n    global eggs\n    eggs = 'changed'\n"
           "def uses_before_assigning():\n    print(eggs)\n    eggs = 'local'\n"
           "eggs = 'global'\n")


def scope_rules():
    """the four rules of the chapter, each decided for a real function by the compiler's own symbol table"""
    table = symtable.symtable(SYM_SRC, "scopes.py", "exec")
    rows = []
    explain = {"reads_global": "uses eggs, never assigns it, and declares nothing",
               "makes_local": "assigns eggs inside the function",
               "declares_global": "declares global eggs and then assigns it",
               "uses_before_assigning": "assigns eggs somewhere in the function, but reads it first"}
    for fn in table.get_children():
        name = fn.get_name()
        if name not in explain:
            continue
        sym = fn.lookup("eggs")
        rows.append({"function": name + "()", "condition": explain[name],
                     "verdict": "global" if sym.is_global() else "local",
                     "declared_global": sym.is_declared_global(), "assigned": sym.is_assigned()})
    return {"kind": "scoperules", "code": SYM_SRC.rstrip("\n").split("\n"), "rows": rows,
            "caption": "The verdict in each row is the compiler's own, read back from the symbol table of this program; "
                       "nothing here is a reading of the rules by hand."}


KINDS = [
    ("scale(3)", "def scale(value, /, factor=2)"),
    ("scale(3, 4)", "def scale(value, /, factor=2)"),
    ("scale(value=3)", "def scale(value, /, factor=2)"),
    ("area(2, height=5)", "def area(width, *, height)"),
    ("area(2, 5)", "def area(width, *, height)"),
]
KIND_SRC = "def scale(value, /, factor=2):\n    return value * factor\n\ndef area(width, *, height):\n    return width * height\n"


def parameter_kinds():
    """each call really made: the value it gives back, or the exact text of the TypeError Python raises"""
    g = {}
    exec(compile(KIND_SRC, "<kinds>", "exec"), g)
    rows = []
    for call, signature in KINDS:
        try:
            rows.append({"call": call, "signature": signature, "ok": True, "result": repr(eval(call, g))})
        except TypeError as e:
            rows.append({"call": call, "signature": signature, "ok": False, "result": "TypeError: %s" % e})
    return {"kind": "paramkinds", "code": KIND_SRC.rstrip("\n").split("\n"), "rows": rows,
            "caption": "A slash closes the parameters before it to names; a star opens the parameters after it to names only. "
                       "Each line below is a real call and its real answer."}


LEGB = [
    ("the function's own body", "def look():\n    where = 'local'\n    return where\nprint(look())\n"),
    ("the function around it", "def outside():\n    where = 'enclosing'\n    def look():\n        return where\n    return look()\nprint(outside())\n"),
    ("the file, outside every function", "where = 'global'\ndef look():\n    return where\nprint(look())\n"),
    ("the built-in names Python always has", "def look():\n    return len.__name__\nprint(look())\n"),
]


def name_resolution():
    """the same lookup run four times, with the name bound one step further out each time: the value really found"""
    rows = []
    for place, src in LEGB:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(compile(src, "<legb>", "exec"), {"__name__": "__main__"})
        rows.append({"place": place, "code": src.rstrip("\n").split("\n"), "found": buf.getvalue().strip()})
    return {"kind": "resolution", "rows": rows,
            "caption": "Python looks for a name in the function first, then in any function around it, then in the file, "
                       "and last among the built-in names. The first place that has the name wins."}


V = {"CallStackOrder": call_stack(), "ExceptionHierarchy": hierarchy(), "ScopeIdentification": scope_rules(),
     "PositionalOnlyParameter": parameter_kinds(), "NameResolution": name_resolution()}
V["_meta"] = {"version": __version__, "python": platform.python_version(),
              "note": "Executed specifications for the chapter 4 lecture deck; every value was produced by running the code above."}
json.dump(V, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
print("written", sys.argv[1], "under Python", platform.python_version(), "-", len(V) - 1, "visuals,",
      sum(len(v.get("rows", v.get("steps", []))) for k, v in V.items() if k != "_meta"), "executed rows")
