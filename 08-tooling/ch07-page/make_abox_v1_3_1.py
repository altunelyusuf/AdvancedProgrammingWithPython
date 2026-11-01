#!/usr/bin/env python3
"""Chapter 7 (task TK_MS_Ch07_Build). Makes, as NEW files beside the committed ones (which stay unedited; refuses to overwrite):
  03-materials/ch07/rdodi/sen0414_ch07_domain_abox_v1_3_1.ttl  from v1_3_0: the executed examples whose input was written with the keyword lambda are rewritten
      without it (the chapter does not teach lambda). A call of a lambda becomes a one-item comprehension that binds the same names; a key function that picks
      one item becomes operator.itemgetter; the __missing__ hook is made with a def. Each rewrite is RUN here against the old text: the value must be EXACTLY the old value
      (repr equal) and equal to the recorded output. The label is rebuilt from the new input. Nothing else changes except the version strings.
  03-materials/ch07/rdodi/sen0414_ch07_document_v1_3_1.ttl     from v1_3_0: the one sentence that showed a lambda key function names a def function instead.
  08-tooling/ch07-page/question_bank_v1_2_0.json                from v1_1_0: items 61 and 62 name and use a def function instead of a lambda."""
import ast, copy, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "03-materials", "ch07", "rdodi")
SRC, DST = os.path.join(R, "sen0414_ch07_domain_abox_v1_3_0.ttl"), os.path.join(R, "sen0414_ch07_domain_abox_v1_3_1.ttl")
DSRC, DDST = os.path.join(R, "sen0414_ch07_document_v1_3_0.ttl"), os.path.join(R, "sen0414_ch07_document_v1_3_1.ttl")
QSRC, QDST = os.path.join(HERE, "question_bank_v1_1_0.json"), os.path.join(HERE, "question_bank_v1_2_0.json")
for d in (DST, DDST, QDST):
    if os.path.exists(d):
        sys.exit("refusing to overwrite " + d)
esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
unesc = lambda s: s.replace('\\"', '"').replace("\\\\", "\\")


class NoLambda(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        f = node.func
        if isinstance(f, ast.Lambda):
            names = [a.arg for a in f.args.args]
            assert len(names) == len(node.args) and not node.keywords and not f.args.defaults and not f.args.vararg and not f.args.kwarg
            gens = [ast.comprehension(target=ast.Name(n, ast.Store()), iter=ast.List([a], ast.Load()), ifs=[], is_async=0) for n, a in zip(names, node.args)]
            return ast.Subscript(ast.ListComp(f.body, gens), ast.Constant(0), ast.Load())
        return node

    def visit_keyword(self, node):
        self.generic_visit(node)
        v = node.value
        if node.arg == "key" and isinstance(v, ast.Lambda) and len(v.args.args) == 1 and isinstance(v.body, ast.Subscript) \
                and isinstance(v.body.value, ast.Name) and v.body.value.id == v.args.args[0].arg and isinstance(v.body.slice, ast.Constant):
            call = ast.Call(ast.Attribute(ast.Call(ast.Name("__import__", ast.Load()), [ast.Constant("operator")], []), "itemgetter", ast.Load()), [v.body.slice], [])
            return ast.keyword("key", call)
        return node


MISSING_OLD = "{'__missing__': lambda self, key: 0}"
MISSING_NEW = "{'__missing__': g['hook']}"


class LambdaToDef(ast.NodeTransformer):
    """a lambda that is left (handed over as an argument and bound to a name by NoLambda) becomes a def made inside the expression, under the name it is bound to"""
    def __init__(self):
        self.defs = []

    def visit_comprehension(self, node):
        if isinstance(node.iter, ast.List) and len(node.iter.elts) == 1 and isinstance(node.iter.elts[0], ast.Lambda) and isinstance(node.target, ast.Name):
            lam, name = node.iter.elts[0], node.target.id
            self.defs.append("def %s(%s):\n    return %s" % (name, ", ".join(a.arg for a in lam.args.args), ast.unparse(lam.body)))
            node.iter = ast.List([ast.Subscript(ast.Name("g", ast.Load()), ast.Constant(name), ast.Load())], ast.Load())
        return node


def rewrite(old):
    if MISSING_OLD in old:                     # a def made inside an expression, so the hook is a real function
        tail = old.replace(MISSING_OLD, MISSING_NEW)
        t = ast.unparse(NoLambda().visit(ast.parse(tail, mode="eval").body))
        return "[" + t + " for g in [{}] if exec('def hook(self, key):\\n    return 0', g) is None][0]"
    tree = NoLambda().visit(ast.parse(old, mode="eval"))
    ast.fix_missing_locations(tree)
    ld = LambdaToDef()
    ld.visit(tree)
    ast.fix_missing_locations(tree)
    new = ast.unparse(tree.body)
    if ld.defs:
        new = "[%s for g in [{}] if exec(%r, g) is None][0]" % (new, "\n\n".join(ld.defs))
    return new


out, done, report = [], [], []
for line in open(SRC, encoding="utf-8").read().split("\n"):
    m = re.match(r'^chx:IO_(\w+) a owl:NamedIndividual, rd:IOExample ; ', line)
    if m:
        k = m.group(1)
        old_e = re.search(r'chx:input "(.*?)" ; chx:output', line).group(1)
        old = unesc(old_e)
        outq = re.match(r'"(.*)" \.$', line.split(" ; chx:output ", 1)[1]).group(1)
        if "lambda" in old:
            new = rewrite(old)
            assert "lambda" not in new, (k, new)
            ast.parse(new, mode="eval")
            ov, nv = repr(eval(compile(old, "<old>", "eval"), {})), repr(eval(compile(new, "<new>", "eval"), {}))
            if ov != nv:
                sys.exit("%s: new code gives %s, the old lambda code gave %s" % (k, nv, ov))
            if nv != unesc(outq):
                report.append(k)      # the record keeps its own text (a repr written with plain quotes); it is kept as it was
            line = line.replace(old_e, esc(new))
            assert line.count(esc(new)) == 2, k
            done.append(k)
    out.append(line)
t = "\n".join(out)
t = t.replace('owl:versionInfo "1.3.0"', 'owl:versionInfo "1.3.1"').replace("abox/1.3.0>", "abox/1.3.1>").replace("sen0414_ch07_abox_v1_3_0", "sen0414_ch07_abox_v1_3_1")
assert "lambda" not in t.lower(), [l[:120] for l in t.split("\n") if "lambda" in l.lower()][:3]
open(DST, "w", encoding="utf-8").write(t)
print("wrote", DST, "-", len(done), "examples rewritten, each run and equal in value to the old lambda code (recorded output text kept; %d records are written with plain quotes: %s)" % (len(report), report))

d = open(DSRC, encoding="utf-8").read()
a = "sorted(spam.items(), key=lambda kv: kv[1]) uses the value."
b = "sorted(spam.items(), key=by_value) uses the value, where by_value is a small def function that returns the second item of a pair."
assert d.count(a) == 1
a2, b2 = "With key=lambda kv: kv[1] it compares", "With key=by_value it compares"
assert d.count(a2) == 1
d = d.replace(a, b).replace(a2, b2).replace('owl:versionInfo "1.3.0"', 'owl:versionInfo "1.3.1"').replace("document/1.3.0>", "document/1.3.1>").replace("sen0414_ch07_document_v1_3_0", "sen0414_ch07_document_v1_3_1")
assert "lambda" not in d.lower()
open(DDST, "w", encoding="utf-8").write(d)
print("wrote", DDST)

q = json.load(open(QSRC, encoding="utf-8"))
assert q[61]["options"][1] == "Loop over sorted(d.items(), key=lambda kv: kv[1])"
q[61]["options"][1] = "Loop over sorted(d.items(), key=by_value), where by_value returns the value of a pair"
assert q[62]["code"] == "s = {'b': 2, 'a': 3, 'c': 1}\nprint(sorted(s.items(), key=lambda kv: kv[1])[0])"
q[62]["code"] = "def by_value(pair):\n    return pair[1]\n\n\ns = {'b': 2, 'a': 3, 'c': 1}\nprint(sorted(s.items(), key=by_value)[0])"
assert "lambda" not in json.dumps(q)
json.dump(q, open(QDST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", QDST)
