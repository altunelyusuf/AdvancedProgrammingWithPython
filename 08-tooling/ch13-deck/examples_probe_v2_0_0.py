#!/usr/bin/env python3
"""Runs every example of examples_v2_0_0.py the way the page runs a chapter-code example (the page's _run function: ast.parse, exec in a fresh namespace with
__name__ '__main__', a final bare expression printed with repr, an exception printed as 'Type: message', the output right-stripped) under the interpreter that runs this
file, and writes {id: output} as JSON. Usage: python3 examples_probe_v2_0_0.py OUT.json"""
__version__ = "2.0.0"
import ast, io, json, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("ex", os.path.join(HERE, "examples_v2_0_0.py")); X = importlib.util.module_from_spec(sp); sp.loader.exec_module(X)


def _run(src):
    o = io.StringIO(); ns = {"__name__": "__main__"}; old = sys.stdout; sys.stdout = o
    try:
        t = ast.parse(src)
        if t.body and isinstance(t.body[-1], ast.Expr):
            last = ast.Expression(t.body.pop().value)
            exec(compile(t, "<code>", "exec"), ns)
            v = eval(compile(last, "<code>", "eval"), ns)
            if v is not None:
                print(repr(v))
        else:
            exec(compile(t, "<code>", "exec"), ns)
    except Exception as e:
        print(type(e).__name__ + ": " + str(e))
    finally:
        sys.stdout = old
    return o.getvalue().rstrip()


if __name__ == "__main__":
    cwd = os.getcwd()
    out = {e["id"]: _run(X.code_text(e)) for e in X.EXAMPLES}
    assert os.getcwd() == cwd, "an example left the current folder"
    json.dump({"python": sys.version.split()[0], "out": out}, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
    print(sys.version.split()[0], len(out), "examples")
