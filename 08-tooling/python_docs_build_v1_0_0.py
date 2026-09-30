"""Builds python_docs_v1_0_0.json: one-line help for Python's builtins, the methods of str/list/dict/set/tuple and the keywords, read from the interpreter
that runs this script (so the help is the interpreter's own text, not written from memory), plus hand-written one-liners for the keywords.
Usage: python_docs_build_v1_0_0.py [out.json]"""
import builtins, inspect, json, keyword, re, sys
def first(d):
    d = (inspect.getdoc(d) or "").strip()
    d = re.split(r"\n\s*\n", d)[0].replace("\n", " ")
    m = re.match(r"(.+?[.!?])(\s|$)", d)
    return (m.group(1) if m else d)[:160]
def sig(o, n):
    try:
        t = str(inspect.signature(o))
        for a, b in (("(self, /)", "()"), ("(self, /, ", "("), ("(self, ", "("), (", /)", ")"), (", /, ", ", "), ("(/, ", "(")): t = t.replace(a, b)
        return n + t
    except (ValueError, TypeError): return n + "(...)"
doc = {}
for n in sorted(dir(builtins)):
    o = getattr(builtins, n)
    if n.startswith("_") or n in ("eval", "exec", "compile") or not callable(o) or (isinstance(o, type) and issubclass(o, BaseException)): continue  # eval and exec are left out: they are not taught here, and their help text trips the page's own scan for evaluated code
    s = sig(o, n); d = first(o)
    if "->" in d or d.startswith(n + "("): d = ""
    doc[n] = s + (" - " + d if d else "")
meth = {}
for t in (str, list, dict, set, tuple):
    for n in sorted(dir(t)):
        if n.startswith("_"): continue
        o = getattr(t, n); d = first(o)
        if "->" in d or d.startswith(n + "("): d = ""
        meth[t.__name__ + "." + n] = sig(o, n) + (" - " + d if d else "")
doc["range"] = "range(stop) or range(start, stop, step) - the whole numbers from start up to, not including, stop"
KW = {"if":"if condition: - run the block only when the condition is true","elif":"elif condition: - another test, tried only when the earlier ones were false","else":"else: - the block that runs when no earlier test matched (also after a loop or try)",
"for":"for item in things: - repeat the block once for each item","while":"while condition: - repeat the block as long as the condition stays true","break":"break - leave the loop now","continue":"continue - skip to the next round of the loop",
"def":"def name(parameters): - define a function","return":"return value - give a value back and leave the function","class":"class Name: - define a new kind of object","import":"import module - make a module available","from":"from module import name - take one name from a module",
"as":"as - give a new name (import x as y, with f() as g)","try":"try: - run code that might fail; pair with except","except":"except ErrorType: - handle an error raised in the try block","finally":"finally: - always runs, error or not","raise":"raise Error(message) - signal an error",
"with":"with thing as name: - use a resource and close it automatically","lambda":"lambda x: expression - a small unnamed function","in":"in - membership test, or the loop source in for x in y","is":"is - same object (use == for equal value)","not":"not - reverses true and false",
"and":"and - true when both sides are true","or":"or - true when either side is true","pass":"pass - do nothing (a placeholder block)","None":"None - the value that means nothing here","True":"True - the boolean true","False":"False - the boolean false",
"global":"global name - use the module-level variable inside a function","nonlocal":"nonlocal name - use the enclosing function's variable","del":"del target - remove a name, item or slice","assert":"assert condition, message - stop with an error if the condition is false","yield":"yield value - hand back one value at a time (a generator)",
"async":"async def - define a coroutine","await":"await x - wait for a coroutine to finish","match":"match value: - choose a branch by pattern","case":"case pattern: - one branch of a match"}
kw = {k: KW.get(k, k) for k in keyword.kwlist + ["match", "case"]}
out = {"python": sys.version.split()[0], "builtins": doc, "methods": meth, "keywords": kw}
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "python_docs_v1_0_0.json", "w"), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
print(len(doc), len(meth), len(kw))
