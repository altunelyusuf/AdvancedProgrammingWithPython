"""Prints, for each example of examples_v2_0_0.py, the layout that deck_build_v2_0_0.plan_code chose (layout, code font, heights of every code box and its
explanation, room left for the result). Usage: python3 plan_debug_v2_0_0.py [EXAMPLE_ID ...]   Builder helper, not a check of the standard."""
__version__ = "2.0.0"
import importlib.util, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sp = importlib.util.spec_from_file_location("b", os.path.join(HERE, "deck_build_v2_0_0.py"))
B = importlib.util.module_from_spec(sp)
sys.modules["b"] = B
sp.loader.exec_module(B)
want = sys.argv[1:]
for ex in B.X.EXAMPLES:
    if want and ex["id"] not in want:
        continue
    v = B.V.VISUALS[ex["visual"]]
    lay, fs, nfs, bw, ew, rows, heights, ry, avail = B.plan_code(ex, v)
    print(ex["id"], lay, fs, "box_w %.2f expl_w %.2f" % (bw, ew), "avail %.2f need %.2f" % (avail, v.need))
    for (c, n), h in zip(rows, heights):
        print("   code_h %.2f note_h %.2f -> %.2f" % (c, n, h))
