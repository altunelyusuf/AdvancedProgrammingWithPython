const OG_CON={index:'indexing  x[i]',slice:'slicing  x[a:b]',call:'function call  f(x)',method:'method call  x.m()',attr:'attribute access  x.name',assign:'assignment  x = …',unpack:'unpacking  a, *b = …',itemassign:'item or slice assignment  x[i] = …',augassign:'augmented assignment  x += …',delete:'del statement',loop:'for or while loop',comp:'comprehension',compare:'comparison or membership',boolop:'and / or',binop:'operator + or *',funcdef:'function definition',lambda:'lambda  lambda x: …',classdef:'class definition',ifelse:'if / else',literal:'collection written out',fstring:'formatted string  f"…"',importer:'import statement',tryexc:'try / except',withblock:'with block',raiser:'raise or assert',ret:'return or yield',kwarg:'keyword argument'};
const OG_BEH={inplace:'changes the value itself',new:'builds a new value',copy:'copies a value',share:'shares one value under two names',repeat:'repeats over items',test:'asks a yes-or-no question',decide:'chooses between branches',search:'searches for an item',shortcut:'stops early when the answer is known',measure:'measures its length',order:'puts items in order',random:'chooses at random',bind:'gives a name to a value',define:'defines a function or class',lookup:'looks something up by key or name',text:'works on text',format:'builds formatted text',pattern:'matches a pattern',io:'reads, writes or prints',load:'brings in a module',recover:'handles an error',signal:'signals an error or checks a claim',resource:'opens and closes a resource safely',hand:'hands back a result'};
const OG_PY=String.raw`
import ast, json
S = json.loads(__SNIPS__)
MUT = {'append','insert','remove','pop','sort','reverse','extend','clear','shuffle','update','add','discard','setdefault','popitem'}
TEXTM = {'split','join','strip','lstrip','rstrip','replace','upper','lower','title','startswith','endswith','find','rfind','count','splitlines','center','ljust','rjust','capitalize','swapcase','isalpha','isdigit','isupper','islower','partition','removeprefix','removesuffix','zfill','encode','decode'}
LOOKM = {'get','keys','values','items','setdefault','index'}
IOM = {'read','write','readline','readlines','writelines','dump','load','loads','dumps','open','mkdir','exists','iterdir','glob','rename','unlink','rmtree','copy','move','walk','listdir','makedirs','close','flush','seek'}
PATM = {'match','search','findall','sub','compile','fullmatch','finditer','group','groups','split'}
def parse(src):
    s = src.strip()
    for c in (s, s + ' pass', s + '\n    pass'):
        try: return ast.parse(c), c
        except SyntaxError: continue
    return None, s
out = {}
for cid, src in S.items():
    tree, code = parse(src)
    if tree is None: continue
    con, beh = {}, {}
    def seg(n):
        try: return (ast.get_source_segment(code, n) or type(n).__name__)[:70]
        except Exception: return type(n).__name__
    def C(k, n): con.setdefault(k, seg(n))
    def B(k, n): beh.setdefault(k, seg(n))
    for n in ast.walk(tree):
        if isinstance(n, ast.Subscript):
            if isinstance(n.ctx, ast.Store): C('itemassign', n); B('inplace', n)
            elif isinstance(n.ctx, ast.Del): C('delete', n); B('inplace', n)
            elif isinstance(n.slice, ast.Slice): C('slice', n); B('new', n)
            else: C('index', n); B('lookup', n)
        elif isinstance(n, ast.Call):
            for k in n.keywords: C('kwarg', n)
            f = n.func
            if isinstance(f, ast.Attribute):
                C('method', n); a = f.attr
                if a in MUT: B('inplace', n)
                if a in ('sort', 'reverse'): B('order', n)
                if a == 'index': B('search', n)
                if a in ('copy', 'deepcopy'): B('copy', n)
                if a in TEXTM: B('text', n)
                if a == 'format': B('format', n)
                if a in LOOKM: B('lookup', n)
                if a in IOM: B('io', n)
                if a in PATM and not (isinstance(f.value, ast.Constant) and isinstance(f.value.value, str)): B('pattern', n)
                if isinstance(f.value, ast.Name) and f.value.id == 'random': B('random', n)
                if isinstance(f.value, ast.Name) and f.value.id == 're': B('pattern', n)
            elif isinstance(f, ast.Name):
                C('call', n)
                if f.id == 'len': B('measure', n)
                if f.id == 'sorted': B('order', n); B('new', n)
                if f.id in ('list', 'tuple', 'dict', 'set', 'str', 'int', 'float', 'bytes', 'frozenset'): B('new', n)
                if f.id in ('print', 'input', 'open'): B('io', n)
                if f.id in ('isinstance', 'any', 'all', 'callable', 'hasattr'): B('test', n)
                if f.id in ('min', 'max', 'sum', 'abs', 'round'): B('measure', n)
        elif isinstance(n, ast.Attribute) and not isinstance(n.ctx, ast.Store):
            C('attr', n); B('lookup', n)
        elif isinstance(n, ast.Assign):
            C('assign', n)
            if any(isinstance(t, (ast.Tuple, ast.List)) for t in n.targets): C('unpack', n)
            if any(isinstance(t, ast.Name) for t in n.targets): B('bind', n)
            if isinstance(n.value, ast.Name) and all(isinstance(t, ast.Name) for t in n.targets): B('share', n)
        elif isinstance(n, ast.AnnAssign): C('assign', n); B('bind', n)
        elif isinstance(n, ast.AugAssign): C('augassign', n); B('bind', n)
        elif isinstance(n, ast.Delete): C('delete', n)
        elif isinstance(n, (ast.For, ast.While)): C('loop', n); B('repeat', n)
        elif isinstance(n, (ast.ListComp, ast.GeneratorExp, ast.SetComp, ast.DictComp)): C('comp', n); B('repeat', n); B('new', n)
        elif isinstance(n, ast.Compare):
            C('compare', n); B('test', n)
            if any(isinstance(o, (ast.In, ast.NotIn)) for o in n.ops): B('search', n)
        elif isinstance(n, ast.BoolOp): C('boolop', n); B('test', n); B('shortcut', n)
        elif isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Mult, ast.Mod, ast.Sub, ast.Div, ast.FloorDiv)): C('binop', n); B('new', n)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)): C('funcdef', n); B('define', n)
        elif isinstance(n, ast.Lambda): C('lambda', n); B('define', n)
        elif isinstance(n, ast.ClassDef): C('classdef', n); B('define', n)
        elif isinstance(n, (ast.If, ast.IfExp)): C('ifelse', n); B('decide', n)
        elif isinstance(n, ast.JoinedStr): C('fstring', n); B('format', n)
        elif isinstance(n, (ast.Import, ast.ImportFrom)): C('importer', n); B('load', n)
        elif isinstance(n, ast.Try): C('tryexc', n); B('recover', n)
        elif isinstance(n, (ast.With, ast.AsyncWith)): C('withblock', n); B('resource', n)
        elif isinstance(n, (ast.Raise, ast.Assert)): C('raiser', n); B('signal', n)
        elif isinstance(n, (ast.Return, ast.Yield, ast.YieldFrom)): C('ret', n); B('hand', n)
        elif isinstance(n, (ast.List, ast.Tuple, ast.Dict, ast.Set)) and not isinstance(getattr(n, 'ctx', None), ast.Store): C('literal', n)
        elif isinstance(n, ast.Starred): C('unpack', n)
    out[cid] = {'con': con, 'beh': beh}
print(json.dumps(out))
`;
