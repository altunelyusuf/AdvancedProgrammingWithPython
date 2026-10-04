__version__ = "2.0.0"
# Every code example the renewed chapter 3 lecture deck shows. Nothing here carries an output: the outputs are produced
# by executing each line and each program under the course interpreter at build time (ch01-deck/examples_run_v2_1_0.py),
# so a slide can only show what Python actually printed.
#
# 2.0.0 replaces the small example set of 1.1.0, which served the 30-slide deck v2.0.x. The new deck covers all 52 leaf
# concepts of the chapter corpus (sen0414_ch03_corpus_v1_0_0.py), so the example set is rebuilt around them: one shell
# session or one whole program per concept that has a worked example. The whole programs are taken from the corpus's
# own PG table, so that the deck shows the same source the corpus executes its claims against. Earlier keys are gone,
# hence MAJOR.
#
# EX sessions are run in a namespace of their own, line by line, exactly the way ch02-deck/deck_check_v1_0_1.py re-runs
# them from the finished slides; a statement records no output and must be followed by another line in the same card.
# PROGRAMS entries carrying "mayfail" are meant to stop with an error, which is how the chapter teaches StopIteration,
# an immutable tuple and a dictionary changed while it is being walked through.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sen0414_ch03_corpus_v1_0_0 import PG as CORPUS_PG      # the chapter's own programs, not retyped

EX = {
 # --- group cards ---
 "loopgroup":  ["sum(range(101))", "len(range(101))", "50 * 101"],
 "seqgroup":   ["list(range(5))", "list('abc')", "list({'a': 1, 'b': 2})"],
 "ctrlgroup":  ["break", "continue", "return"],
 "modgroup":   ["len('hello')", "math.sqrt(16)", "__import__('math').sqrt(16)"],
 # --- I. Repetition ---
 "accumulate": ["sum(range(101))", "sum(range(100))", "50 * 101", "len(range(101))"],
 "nesting":    ["4 * 3", "1000 * 1000"],
 # --- II. Sequence: range ---
 "rangestop":  ["list(range(5))", "len(range(5))", "list(range(0))", "range(2.5)"],
 "rangess":    ["list(range(12, 16))", "len(range(12, 16))", "list(range(16, 12))"],
 "rangestep":  ["list(range(0, 10, 2))", "list(range(0, 10, 3))", "len(range(0, 10, 3))", "range(0, 10, 0)"],
 "rangedesc":  ["list(range(5, -1, -1))", "list(range(-10, -100, -30))", "list(range(5, 0))", "list(reversed(range(1, 10, 2)))"],
 "lazyrange":  ["range(10)", "range(10) == list(range(10))", "isinstance(range(3), list)", "sum(range(4))"],
 "halfopen":   ["len(range(0, 24))", "list(range(1, 11))", "'hello'[1:3]", "list(range(0, 5)) + list(range(5, 10)) == list(range(10))"],
 "rangeops":   ["r = range(0, 20, 2)", "10 in r", "11 in r", "r[5]", "r.index(10)", "r[-1]", "r[:5]"],
 # --- II. Sequence: helpers, protocol, collections ---
 "enumerate":  ["list(enumerate(['Spring', 'Summer', 'Fall', 'Winter']))", "list(enumerate(['tic', 'tac', 'toe'], start=1))", "next(enumerate('ab'))"],
 "zipstrict":  ["list(zip('abc', [1, 2]))", "list(zip('ab', [1, 2], strict=True))", "list(zip('ab', [1], strict=True))"],
 "unpack":     ["x, y = (1, 2)", "x", "y", "x, y = (1,)"],
 "iterable":   ["list('abc')", "list({'a': 1, 'b': 2})", "iter(5)"],
 "iterator":   ["it = iter([10, 20])", "next(it)", "next(it)", "next(iter([]), 'done')", "next([1, 2])"],
 "seqkind":    ["'hello'[1]", "[10, 20, 30][0]", "(10, 20, 30)[-1]", "{'a': 1}[0]"],
 "listval":    ["a = [1, 2]", "a.append(3)", "a", "a[0] = 99", "a", "list(range(3)) + [9]"],
 "tupleval":   ["tuple(range(3))", "(0, 'tic')[0]", "len(('hello',))", "type(('hello')).__name__", "len(())"],
 "dictval":    ["{'Ada': 'active', 'Can': 'inactive'}['Can']", "list({'Ada': 'active', 'Can': 'inactive'})", "{'Ada': 'active'}['Eda']"],
 # --- III. Loop control ---
 "breakstmt":  ["break", "continue"],
 "exceptions": ["10 * (1/0)", "int('x')", "issubclass(ValueError, Exception)", "issubclass(SystemExit, Exception)", "issubclass(KeyboardInterrupt, Exception)"],
 "returnstmt": ["return"],
 # --- IV. Modules ---
 "modulefile": ["type(__import__('math')).__name__", "__import__('math').__name__", "__import__('random').__name__"],
 "stdlib":     ["len('hello')", "math.sqrt(16)", "__import__('math').sqrt(16)"],
 "namespace":  ["__import__('math').sqrt(16)", "'sqrt' in dir(__import__('math'))", "__import__('math').nope"],
 "importerr":  ["random.randint(1, 10)", "__import__('no_such_module_x')", "sys.exit()"],
 "starnames":  ["len(__import__('random').__all__)", "'randint' in __import__('random').__all__"],
 "randmod":    ["__import__('random').randint.__doc__.splitlines()[0]", "__import__('random').randrange(1, 2)"],
}

def _p(name, runs, flag=None):
    """a program of the chapter corpus, with the runs the deck shows; the source is the corpus's own"""
    return (CORPUS_PG[name], runs) if flag is None else (CORPUS_PG[name], runs, flag)

PROGRAMS = {
 # --- I. Repetition ---
 "if_once_v1_0_0.py":        _p("if", [[]]),
 "while_fivetimes_v1_0_0.py":_p("while", [[]]),
 "while_skipped_v1_0_0.py":  _p("while_false", [[]]),
 "yourname_v1_0_0.py":       _p("yourname", [["Al", "Albert", "your name"]]),
 "yourname2_v1_0_0.py":      _p("yourname2", [["Al", "your name"]]),
 "fivetimes_for_v1_0_0.py":  _p("five_for", [[]]),
 "fivetimes_while_v1_0_0.py":_p("five_while", [[]]),
 "gauss_v1_0_0.py":          _p("gauss", [[]]),
 "gauss_reset_v1_0_0.py":    _p("gauss_reset", [[]]),
 "nested_break_v1_0_0.py":   _p("nested_break", [[]]),
 "guess16_v1_0_0.py":        _p("guess16", [["10", "15", "17", "16"]]),
 "rps_v1_0_0.py":            _p("rps", [["x", "q"]]),
 # --- II. Sequence ---
 "for_pairs_v1_0_0.py":      _p("for_pairs", [[]]),
 "iter_next_v1_0_0.py":      _p("iter_next", [[]], "mayfail"),
 "tuple_set_v1_0_0.py":      _p("tuple_set", [[]], "mayfail"),
 "dict_ops_v1_0_0.py":       _p("dict_ops", [[]]),
 # --- III. Loop control ---
 "break3_v1_0_0.py":         _p("break3", [[]]),
 "swordfish_v1_0_0.py":      _p("swordfish", [["Ann", "Joe", "swordfish"]]),
 "exitexample_v1_0_0.py":    _p("exitexample", [["hi", "exit"]]),
 "exitcatch_v1_0_0.py":      _p("exitcatch", [[]]),
 "kbint_v1_0_0.py":          _p("kbint", [[]]),
 "return_loop_v1_0_0.py":    _p("return_loop", [[]]),
 "primes_v1_0_0.py":         _p("primes", [[]]),
 "clobber_v1_0_0.py":        _p("clobber", [[]]),
 "break_cond_v1_0_0.py":     _p("break_cond", [[]]),
 "handle_v1_0_0.py":         _p("handle", [[]]),
 "finally_order_v1_0_0.py":  _p("finally_order", [[]]),
 "finally_break_v1_0_0.py":  _p("finally_break", [[]]),
 # --- IV. Modules ---
 "import5_v1_0_0.py":        _p("import5", [[]]),
 "multi_v1_0_0.py":          _p("multi", [[]]),
 "star_pow_v1_0_0.py":       _p("star_pow", [[]]),
 "as_math_v1_0_0.py":        _p("as_math", [[]]),
 "modules_cache_v1_0_0.py":  _p("modules_cache", [[]]),
 "seed_v1_0_0.py":           _p("seed", [[]]),
 "randint_ends_v1_0_0.py":   _p("randint_ends", [[]]),
 # --- V. Modern practice ---
 "walrus_v1_0_0.py":         _p("walrus", [[]]),
 "walrus_old_v1_0_0.py":     _p("walrus_old", [[]]),
 "mutate_dict_v1_0_0.py":    _p("mutate_dict", [[]], "mayfail"),
 "mutate_dict_copy_v1_0_0.py": _p("mutate_dict_copy", [[]]),
 "mutate_list_v1_0_0.py":    _p("mutate_list", [[]]),
 "mutate_list_new_v1_0_0.py":_p("mutate_list_new", [[]]),
}
