"""Draws the chapter 19 narrative diagrams (sen0414_ch19_diagrams_v1_0_0.py, grounding >= 0.84) as native PowerPoint shapes
(the chapter 18 drawer, with one more builder, lifecycle_branch: a state diagram whose second state leads to two final states, each by
several transitions, drawn as straight arrows from one tall box to two tall boxes with each label above its arrow).
Each builder takes a diagram's data exactly as the diagrams module holds it and a box on the slide (inches) and returns a
'shapes' item for the deck plan: a list of primitives (box, line, text) that the renderer draws one for one. Every label of the
diagram is placed as the text of one text frame, unaltered, so that diagram_check_v1_0_0.py can find it on the finished slide.
Text frames are sized with the same wrap rule as deck_fit_check_v1_0_0.py (average advance 0.50 em, line 1.21 em) so that a
frame is never smaller than its text needs. Colours are the course palette of the shared renderer. Orange hexagons are
decisions; dark dots and bars are the start and the end of an activity.
Usage: imported by deck_build_v1_0_0.py."""
__version__ = "1.0.0"
import math

EM, LH = 0.50, 1.21
INK, MUTE, SLATE, ORANGE, CARD, RULE, DARK, WHITE = "2B2622", "6E655C", "2F6D62", "D97A14", "F2ECE1", "DFD6C7", "2B2622", "FFFFFF"


def wrap_lines(text, w_in, fs):
    per = max(1, int(max(0.2, w_in - 0.04) / (EM * fs / 72.0)))
    n = 0
    for para in text.split("\n"):
        words = para.split()
        if not words:
            n += 1
            continue
        cur, k = 0, 1
        for word in words:
            add = len(word) + 1 if cur else len(word)
            if cur + add > per and cur > 0:
                k += 1
                cur = len(word)
            else:
                cur += add
        n += k
    return n


def need_h(text, w_in, fs):
    return wrap_lines(text, w_in, fs) * fs * LH / 72.0


class Canvas:
    def __init__(self):
        self.prims = []
        self.warn = []

    def box(self, shape, x, y, w, h, fill=CARD, line=SLATE, lw=1.25):
        self.prims.append({"k": "box", "shape": shape, "x": round(x, 3), "y": round(y, 3), "w": round(w, 3), "h": round(h, 3),
                           "fill": fill, "line": line, "lw": lw})

    def line(self, x1, y1, x2, y2, color=MUTE, w=1.25, arrow=False, dash=False):
        self.prims.append({"k": "line", "x1": round(x1, 3), "y1": round(y1, 3), "x2": round(x2, 3), "y2": round(y2, 3),
                           "color": color, "w": w, "arrow": arrow, "dash": dash})

    def path(self, pts, color=MUTE, w=1.25, arrow=True, dash=False):
        for i in range(len(pts) - 1):
            self.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color, w, arrow and i == len(pts) - 2, dash)

    def text(self, t, x, y, w, h, fs=9, color=INK, bold=False, italic=False, align="center", valign="middle", min_fs=8, fill=None):
        if fs < min_fs:
            raise SystemExit("REFUSED: diagram text %r below %s pt" % (t, min_fs))
        if need_h(t, w, fs) > h + 0.05:
            raise SystemExit("REFUSED: diagram text %r needs %.2f in but its frame is %.2f in (w %.2f, %s pt)" % (t, need_h(t, w, fs), h, w, fs))
        self.prims.append({"k": "text", "t": t, "x": round(x, 3), "y": round(y, 3), "w": round(w, 3), "h": round(h, 3), "fs": fs,
                           "color": color, "bold": bold, "italic": italic, "align": align, "valign": valign, "fill": fill})

    def label_in(self, t, x, y, w, h, fs, color=INK, bold=False, inset=(0.06, 0.03), min_fs=8):
        """text in a frame inset from a shape; the inset frame is grown in height to what the text needs, centred."""
        fw, fh = w - 2 * inset[0], h - 2 * inset[1]
        nh = need_h(t, fw, fs) + 0.02
        if nh > fh + 0.05:
            raise SystemExit("REFUSED: label %r needs %.2f in, shape gives %.2f in (w %.2f, %s pt)" % (t, nh, fh, fw, fs))
        self.text(t, x + inset[0], y + (h - max(nh, 0.05)) / 2, fw, max(nh, 0.05), fs, color, bold, False, "center", "middle", min_fs)


def _geom(x, y, w, h):
    return {"x": x, "y": y, "w": w, "h": h, "l": x, "r": x + w, "t": y, "b": y + h, "cx": x + w / 2, "cy": y + h / 2}


def _insets(shape):
    return {"round": (0.07, 0.03), "rect": (0.07, 0.03), "hex": (0.17, 0.03), "oval": (0.16, 0.05)}[shape]


# ---------------------------------------------------------------------------------------------------------------------------
# activity diagrams (the Workflow pattern): nodes on a grid, edges routed at right angles (modes h, v, vh, hv and loopR/loopL)
# ---------------------------------------------------------------------------------------------------------------------------
def activity(data, box, grid, cols, rows_n, fs=8.5, nh=0.46, dh=0.56, routes=None, ends=None, starts=None, row_top=None):
    """grid: id -> (col, row); cols: list of (x offset, width) inside the box; routes: (src, dst) -> mode;
    ends: {'type': 'dot'|'bar', 'col':, 'row':, 'row2':}; starts: (col,row) of the start dot. Returns a shapes item."""
    bx, by, bw, bh = box
    cv = Canvas()
    pitch = bh / rows_n
    G = {}
    labels = {n["id"]: n for n in data["nodes"]}
    for nid, (c, r) in grid.items():
        n = labels[nid]
        dec = n.get("kind") == "decision"
        w = cols[c][1]
        h = dh if dec else nh
        x = bx + cols[c][0]
        y = by + r * pitch + (pitch - h) / 2
        G[nid] = _geom(x, y, w, h)
        G[nid]["dec"] = dec
        shape = "hex" if dec else "round"
        cv.box(shape, x, y, w, h, fill=ORANGE if dec else CARD, line=ORANGE if dec else SLATE)
        ins = _insets(shape)
        cv.label_in(n["label"], x, y, w, h, fs, WHITE if dec else INK, bold=dec, inset=ins)
    sc, sr = starts
    d = 0.2
    sx = bx + cols[sc][0] + cols[sc][1] / 2 - d / 2 if sc >= 0 else bx
    G["start"] = _geom(sx, by + sr * pitch + (pitch - d) / 2, d, d)
    cv.box("oval", G["start"]["x"], G["start"]["y"], d, d, fill=DARK, line=DARK)
    et = ends
    if et["type"] == "dot":
        ex = bx + cols[et["col"]][0] + cols[et["col"]][1] / 2 - 0.14
        G["end"] = _geom(ex, by + et["row"] * pitch + (pitch - 0.28) / 2, 0.28, 0.28)
        cv.box("oval", G["end"]["x"], G["end"]["y"], 0.28, 0.28, fill=WHITE, line=DARK, lw=2)
        cv.box("oval", G["end"]["x"] + 0.06, G["end"]["y"] + 0.06, 0.16, 0.16, fill=DARK, line=DARK)
    else:
        top = by + et["row"] * pitch + (pitch - nh) / 2
        bot = by + et["row2"] * pitch + (pitch + nh) / 2
        G["end"] = _geom(bx + et["x"], top, 0.1, bot - top)
        cv.box("rect", G["end"]["x"], top, 0.1, bot - top, fill=DARK, line=DARK)
    routes = routes or {}
    nodes_geo = [g for k, g in G.items() if k not in ("start", "end")]
    for fl in data["flows"]:
        a, b = fl[0], fl[1]
        lab = fl[2] if len(fl) > 2 else None
        ga, gb = G[a], G[b]
        mode = routes.get((a, b), "auto")
        if mode == "auto":
            if b == "end" and et["type"] == "bar":
                mode = "h"
            elif abs(ga["cx"] - gb["cx"]) < 0.02:
                mode = "v"
            elif abs(ga["cy"] - gb["cy"]) < 0.02:
                mode = "h"
            else:
                mode = "vh"
        lx = ly = None
        if mode == "v":
            down = gb["cy"] > ga["cy"]
            y1, y2 = (ga["b"], gb["t"]) if down else (ga["t"], gb["b"])
            cv.path([(ga["cx"], y1), (ga["cx"], y2)])
            lx, ly = ga["cx"] + 0.06, (y1 + y2) / 2 - 0.09
        elif mode == "h":
            right = gb["cx"] > ga["cx"]
            x1, x2 = (ga["r"], gb["l"]) if right else (ga["l"], gb["r"])
            if b == "end" and et["type"] == "bar":
                x2 = gb["l"]
            cv.path([(x1, ga["cy"]), (x2, gb["cy"] if b != "end" else ga["cy"])])
            lx, ly = min(x1, x2) + 0.05, ga["cy"] - 0.2
        elif mode == "vh":  # down (or up) from a, then across into the near side of b
            down = gb["cy"] > ga["cy"]
            y1 = ga["b"] if down else ga["t"]
            right = gb["cx"] > ga["cx"]
            x2 = gb["l"] if right else gb["r"]
            cv.path([(ga["cx"], y1), (ga["cx"], gb["cy"]), (x2, gb["cy"])])
            lx, ly = ga["cx"] + 0.07, y1 + (0.0 if down else -0.2)
        elif mode == "hv":  # across the side of a at its height to the centre of b, then down (or up) into b (chapter 18)
            right = gb["cx"] > ga["cx"]
            x1 = ga["r"] if right else ga["l"]
            down = gb["cy"] > ga["cy"]
            y2 = gb["t"] if down else gb["b"]
            cv.path([(x1, ga["cy"]), (gb["cx"], ga["cy"]), (gb["cx"], y2)])
            lx, ly = (x1 + 0.05, ga["cy"] - 0.2) if right else (gb["cx"] + 0.05, ga["cy"] - 0.2)
        elif mode.startswith("loop"):  # out of the side of a, along a margin, back into the same side of b
            side = mode[4:]  # 'R' or 'L'
            if side == "R":
                xa, xb = ga["r"], gb["r"]
                xm = max(ga["r"], gb["r"]) + 0.22
            else:
                xa, xb = ga["l"], gb["l"]
                xm = min(ga["l"], gb["l"]) - 0.22
            cv.path([(xa, ga["cy"]), (xm, ga["cy"]), (xm, gb["cy"]), (xb, gb["cy"])])
            lx, ly = (xa + 0.04, ga["cy"] + 0.03) if side == "R" else (xm + 0.0, ga["cy"] - 0.2)
        if lab:
            lw = min(1.9, max(0.34, len(lab) * EM * 8 / 72.0 + 0.1))
            cv.text(lab, lx, ly, lw, 0.18, 8, MUTE, False, True, "left", "middle", fill="FAF6EF")
    return {"t": "shapes", "x": bx, "y": by, "w": bw, "h": bh, "shapes": cv.prims}


# ---------------------------------------------------------------------------------------------------------------------------
# sequence diagram (the Interaction pattern)
# ---------------------------------------------------------------------------------------------------------------------------
def sequence(data, box, fs=9, head_w=1.7):
    bx, by, bw, bh = box
    cv = Canvas()
    parts = data["participants"]
    n = len(parts)
    xs = {}
    margin = head_w / 2 + 0.05
    for i, p in enumerate(parts):
        xs[p["id"]] = bx + margin + i * (bw - 2 * margin) / (n - 1)
    hh = 0.42
    for p in parts:
        x = xs[p["id"]]
        cv.box("round", x - head_w / 2, by, head_w, hh, fill=SLATE, line=SLATE)
        cv.label_in(p["label"], x - head_w / 2, by, head_w, hh, 10, WHITE, bold=True, inset=(0.06, 0.03))
        cv.line(x, by + hh, x, by + bh, RULE, 1.5, False, True)
    msgs = data["messages"]
    top = by + hh + 0.25
    pitch = (bh - hh - 0.25) / len(msgs)
    for i, m in enumerate(msgs):
        src, dst, label = m[0], m[1], m[2]
        reply = len(m) > 3 and m[3] == "reply"
        y = top + i * pitch
        if src == dst:  # a step the participant takes by itself: a note on its lifeline, beside the lifeline
            x = xs[src]
            right = x < bx + bw / 2
            nw = min(bw / 2 - 0.4, 3.6)
            nx = x + 0.12 if right else x - 0.12 - nw
            nhh = need_h(label, nw - 0.14, fs) + 0.08
            cv.box("rect", nx, y + 0.05, nw, nhh, fill="FFF4E0", line=ORANGE, lw=1)
            cv.text(label, nx + 0.07, y + 0.05 + 0.04, nw - 0.14, nhh - 0.06, fs, INK, False, False, "left", "middle")
        else:
            x1, x2 = xs[src], xs[dst]
            ya = y + pitch * 0.72
            cv.line(x1, ya, x2, ya, ORANGE if not reply else MUTE, 1.75, True, reply)
            lx = min(x1, x2) + 0.1
            lw = abs(x2 - x1) - 0.2
            cv.text(label, lx, ya - 0.05 - need_h(label, lw, fs) - 0.02, lw, need_h(label, lw, fs) + 0.02, fs, INK, False, reply, "center", "bottom")
    return {"t": "shapes", "x": bx, "y": by, "w": bw, "h": bh, "shapes": cv.prims}


# ---------------------------------------------------------------------------------------------------------------------------
# state diagram (the LifeCycle pattern): two states; the box size, its font and the step between arrows are arguments (chapter 14)
# ---------------------------------------------------------------------------------------------------------------------------
def states(data, box, fs=8.5, sw=1.0, sh=0.62, sfs=11, stepy=0.62):
    bx, by, bw, bh = box
    cv = Canvas()
    sts = {s["id"]: s["label"] for s in data["states"]}
    a, b = [s["id"] for s in data["states"]]
    ya = by + 0.55
    xa, xb = bx + 0.1, bx + bw - 0.1 - sw
    G = {a: _geom(xa, ya, sw, sh), b: _geom(xb, ya, sw, sh)}
    for sid in (a, b):
        g = G[sid]
        cv.box("round", g["x"], g["y"], g["w"], g["h"], fill=SLATE, line=SLATE)
        cv.label_in(sts[sid], g["x"], g["y"], g["w"], g["h"], sfs, WHITE, bold=True)
    ini = G[data["initial"]]
    cv.box("oval", ini["cx"] - 0.1, by + 0.05, 0.2, 0.2, fill=DARK, line=DARK)
    cv.path([(ini["cx"], by + 0.25), (ini["cx"], ini["t"])])
    gap_l, gap_r = G[a]["r"], G[b]["l"]
    tw = gap_r - gap_l - 0.1
    fwd = [t for t in data["transitions"] if t[0] == a and t[1] == b]
    back = [t for t in data["transitions"] if t[0] == b and t[1] == a]
    selfs = [t for t in data["transitions"] if t[0] == t[1]]
    y0 = ya - 0.12
    for i, t in enumerate(fwd):          # to the right, two arrows with their labels above them
        y = y0 + 0.12 + i * stepy
        cv.line(gap_l, y + 0.2, gap_r, y + 0.2, ORANGE, 1.75, True)
        cv.text(t[2], gap_l + 0.05, y + 0.2 - 0.03 - need_h(t[2], tw, fs) - 0.02, tw, need_h(t[2], tw, fs) + 0.02, fs, INK, False, False, "center", "bottom")
    for i, t in enumerate(back):         # back to the left, two arrows below the first pair
        y = y0 + 0.12 + (len(fwd) + i) * stepy
        cv.line(gap_r, y + 0.2, gap_l, y + 0.2, SLATE, 1.75, True)
        cv.text(t[2], gap_l + 0.05, y + 0.2 - 0.03 - need_h(t[2], tw, fs) - 0.02, tw, need_h(t[2], tw, fs) + 0.02, fs, INK, False, False, "center", "bottom")
    ybot = ya + sh
    for t in selfs:                      # a transition from a state to itself: a loop under the state
        g = G[t[0]]
        d = 0.38
        cv.path([(g["cx"] - 0.25, ybot), (g["cx"] - 0.25, ybot + d), (g["cx"] + 0.25, ybot + d), (g["cx"] + 0.25, ybot)], ORANGE if t[0] == a else SLATE, 1.5, True)
        lw = sw + 0.06
        cv.text(t[2], g["cx"] - lw / 2, ybot + d + 0.04, lw, need_h(t[2], lw, fs) + 0.02, fs, INK, False, False, "center", "top")
        ybot += 0.0
    return {"t": "shapes", "x": bx, "y": by, "w": bw, "h": bh, "shapes": cv.prims}


# ---------------------------------------------------------------------------------------------------------------------------
# use-case diagram (the SetOfUses pattern)
# ---------------------------------------------------------------------------------------------------------------------------
def usecases(data, box, fs=8.5):
    bx, by, bw, bh = box
    cv = Canvas()
    act = data["actors"][0]
    aw = 0.7
    sysx = bx + aw + 0.1
    cv.box("rect", sysx, by + 0.28, bw - aw - 0.1, bh - 0.28, fill="FBF8F2", line=MUTE, lw=1)
    cv.text(data["system"], sysx + 0.08, by + 0.02, bw - aw - 0.25, 0.24, 8.5, MUTE, True, False, "left", "middle")
    n = len(data["usecases"])
    pitch = (bh - 0.36) / n
    uw = bw - aw - 0.1 - 0.3
    pos = {}
    for i, u in enumerate(data["usecases"]):
        y = by + 0.36 + i * pitch + 0.03
        h = pitch - 0.06
        x = sysx + 0.15
        cv.box("oval", x, y, uw, h, fill=CARD, line=SLATE)
        cv.label_in(u["label"], x, y, uw, h, fs, INK, inset=(0.28, 0.04))
        pos[u["id"]] = (x, y + h / 2)
    ax = bx + aw / 2
    ay = by + bh / 2 - 0.2
    cv.box("oval", ax - 0.11, ay - 0.5, 0.22, 0.22, fill=WHITE, line=DARK, lw=1.5)
    cv.line(ax, ay - 0.28, ax, ay + 0.1, DARK, 1.5)
    cv.line(ax - 0.2, ay - 0.18, ax + 0.2, ay - 0.18, DARK, 1.5)
    cv.line(ax, ay + 0.1, ax - 0.16, ay + 0.35, DARK, 1.5)
    cv.line(ax, ay + 0.1, ax + 0.16, ay + 0.35, DARK, 1.5)
    cv.text(act["label"], bx, ay + 0.4, aw + 0.1, need_h(act["label"], aw + 0.1, 8.5) + 0.02, 8.5, INK, True, False, "center", "top")
    for a, u in data["links"]:
        ux, uy = pos[u]
        cv.line(ax + 0.2, ay - 0.1, ux, uy, MUTE, 1.0)
    return {"t": "shapes", "x": bx, "y": by, "w": bw, "h": bh, "shapes": cv.prims}


# ---------------------------------------------------------------------------------------------------------------------------
# mind map (the TopicAndParts pattern)
# ---------------------------------------------------------------------------------------------------------------------------
def mindmap(data, box, fs=9, root_w=1.55):
    bx, by, bw, bh = box
    cv = Canvas()
    br = data["branches"]
    per = (len(br) + 1) // 2
    cw = (bw - root_w - 0.8) / 2
    gap = 0.07
    ch = (bh - (per - 1) * gap) / per
    rx = bx + (bw - root_w) / 2
    rh = 1.15
    ry = by + (bh - rh) / 2
    cv.box("round", rx, ry, root_w, rh, fill=ORANGE, line=ORANGE)
    cv.label_in(data["root"], rx, ry, root_w, rh, 11, WHITE, bold=True, inset=(0.08, 0.05))
    for i, b in enumerate(br):
        left = i < per
        r = i if left else i - per
        x = bx if left else bx + bw - cw
        y = by + r * (ch + gap)
        cv.box("round", x, y, cw, ch, fill=CARD, line=SLATE)
        cv.line(x + cw if left else x, y + ch / 2, rx if left else rx + root_w, ry + rh / 2, "C9BFAE", 1.25)
        hh = need_h(b["label"], cw - 0.2, fs + 1) + 0.02
        cv.text(b["label"], x + 0.1, y + 0.05, cw - 0.2, hh, fs + 1, SLATE, True, False, "left", "top")
        body = "\n".join(b["children"])
        bh_ = need_h(body, cw - 0.2, fs - 0.5) + 0.06
        cv.text(body, x + 0.1, y + 0.05 + hh + 0.01, cw - 0.2, bh_, fs - 0.5, INK, False, False, "left", "top")
        if 0.05 + hh + 0.01 + bh_ > ch + 0.03:
            raise SystemExit("REFUSED: mind map branch %r does not fit its card (%.2f > %.2f)" % (b["label"], 0.05 + hh + 0.01 + bh_, ch))
    return {"t": "shapes", "x": bx, "y": by, "w": bw, "h": bh, "shapes": cv.prims}


# ---------------------------------------------------------------------------------------------------------------------------
# state diagram of four states round a square (chapter 15, the life of a token file): s0 top left, s1 top right, s2 bottom right,
# s3 bottom left; the transitions must be s0>s1 (right), s1>s2 (down), s2>s1 (up), s2>s3 (left), s3>s0 (up)
# ---------------------------------------------------------------------------------------------------------------------------
def states4(data, box, fs=8.5, sw=1.7, sh=0.62, sfs=11, margin=1.9):
    bx, by, bw, bh = box
    cv = Canvas()
    ids = [s["id"] for s in data["states"]]
    lab = {s["id"]: s["label"] for s in data["states"]}
    if len(ids) != 4:
        raise SystemExit("REFUSED: states4 draws four states")
    want = {(ids[0], ids[1]), (ids[1], ids[2]), (ids[2], ids[1]), (ids[2], ids[3]), (ids[3], ids[0])}
    got = {(t[0], t[1]) for t in data["transitions"]}
    if want != got:
        raise SystemExit("REFUSED: states4 cannot draw the transitions %r" % sorted(got ^ want))
    ytop, ybot = by + 0.3, by + bh - sh - 0.05
    xl, xr = bx + margin, bx + bw - margin - sw
    G = {ids[0]: _geom(xl, ytop, sw, sh), ids[1]: _geom(xr, ytop, sw, sh), ids[2]: _geom(xr, ybot, sw, sh), ids[3]: _geom(xl, ybot, sw, sh)}
    for sid in ids:
        g = G[sid]
        cv.box("round", g["x"], g["y"], g["w"], g["h"], fill=SLATE, line=SLATE)
        cv.label_in(lab[sid], g["x"], g["y"], g["w"], g["h"], sfs, WHITE, bold=True)
    g0, g1, g2, g3 = (G[i] for i in ids)
    ini = data["initial"]
    gi = G[ini]
    cv.box("oval", gi["l"] - 0.55, gi["cy"] - 0.1, 0.2, 0.2, fill=DARK, line=DARK)
    cv.path([(gi["l"] - 0.35, gi["cy"]), (gi["l"], gi["cy"])])
    T = {(t[0], t[1]): t[2] for t in data["transitions"]}

    def put(t, x, y, w, align):
        h = need_h(t, w, fs) + 0.02
        cv.text(t, x, y, w, h, fs, INK, False, False, align, "middle")
    gw = g1["l"] - g0["r"]
    cv.path([(g0["r"], g0["cy"]), (g1["l"], g1["cy"])], ORANGE, 1.75)
    t = T[(ids[0], ids[1])]
    put(t, g0["r"] + 0.08, g0["cy"] - 0.05 - need_h(t, gw - 0.16, fs) - 0.02, gw - 0.16, "center")
    vx = 0.38                                         # the two vertical arrows on the right sit either side of the centre line
    ym = (g1["b"] + g2["t"]) / 2
    cv.path([(g1["cx"] - vx, g1["b"]), (g2["cx"] - vx, g2["t"])], ORANGE, 1.75)
    t = T[(ids[1], ids[2])]
    put(t, g0["r"] + 0.08, ym - 0.2, g1["cx"] - vx - 0.1 - (g0["r"] + 0.08), "right")
    cv.path([(g2["cx"] + vx, g2["t"]), (g1["cx"] + vx, g1["b"])], SLATE, 1.75)
    t = T[(ids[2], ids[1])]
    put(t, g1["cx"] + vx + 0.1, ym - 0.2, bx + bw - (g1["cx"] + vx + 0.1), "left")
    cv.path([(g2["l"], g2["cy"]), (g3["r"], g3["cy"])], ORANGE, 1.75)
    t = T[(ids[2], ids[3])]
    put(t, g3["r"] + 0.08, g3["cy"] - 0.05 - need_h(t, gw - 0.16, fs) - 0.02, gw - 0.16, "center")
    cv.path([(g3["cx"], g3["t"]), (g0["cx"], g0["b"])], SLATE, 1.75)
    t = T[(ids[3], ids[0])]
    put(t, bx, ym - 0.2, g3["cx"] - 0.1 - bx, "right")
    return {"t": "shapes", "x": bx, "y": by, "w": bw, "h": bh, "shapes": cv.prims}


# ---------------------------------------------------------------------------------------------------------------------------
# state diagram of five states (chapter 18, the life of a rowid): the states are placed by the argument `pos` (id -> (column, row)),
# three columns by two rows; every transition is drawn as a straight or an elbow arrow between the sides the argument `ways` names:
# ways[(from, to)] = 'h' (straight, same row, to the right or left), 'v' (straight, same column, down or up),
#                    'down-left' (out of the bottom of `from` at an offset, down to the row of `to`, left into its right side),
#                    'left-up'  (out of the left side of `from`, left to an offset column, up into the bottom of `to`)
# ---------------------------------------------------------------------------------------------------------------------------
def states5(data, box, pos, fs=8.5, sw=1.55, sh=0.58, sfs=10, offset=0.32, top=0.45, ways=None):
    bx, by, bw, bh = box
    cv = Canvas()
    ids = [s["id"] for s in data["states"]]
    lab = {s["id"]: s["label"] for s in data["states"]}
    if len(ids) != 5 or set(pos) != set(ids):
        raise SystemExit("REFUSED: states5 draws five states and needs a place for each")
    colx = [bx, bx + (bw - sw) / 2, bx + bw - sw]
    rowy = [by + top, by + bh - sh - 0.04]
    G = {i: _geom(colx[pos[i][0]], rowy[pos[i][1]], sw, sh) for i in ids}
    for sid in ids:
        g = G[sid]
        cv.box("round", g["x"], g["y"], g["w"], g["h"], fill=SLATE, line=SLATE)
        cv.label_in(lab[sid], g["x"], g["y"], g["w"], g["h"], sfs, WHITE, bold=True)
    gi = G[data["initial"]]
    cv.box("oval", gi["cx"] - 0.1, by + 0.02, 0.2, 0.2, fill=DARK, line=DARK)
    cv.path([(gi["cx"], by + 0.22), (gi["cx"], gi["t"])])
    T = {(t[0], t[1]): t[2] for t in data["transitions"]}
    if set(T) != set(ways):
        raise SystemExit("REFUSED: states5 ways %r do not match the transitions %r" % (sorted(ways), sorted(T)))

    def put(t, x, y, w, align="center", valign="bottom"):
        h = need_h(t, w, fs) + 0.02
        cv.text(t, x, y - (h if valign == "bottom" else 0), w, h, fs, INK, False, False, align, "middle")
    for (a, b), way in ways.items():
        ga, gb, t = G[a], G[b], T[(a, b)]
        col = ORANGE if way in ("h", "v") else SLATE
        if way == "h":
            right = gb["cx"] > ga["cx"]
            x1, x2 = (ga["r"], gb["l"]) if right else (ga["l"], gb["r"])
            cv.path([(x1, ga["cy"]), (x2, gb["cy"])], col, 1.75)
            put(t, min(x1, x2) + 0.06, ga["cy"] - 0.04, abs(x2 - x1) - 0.12)
        elif way == "v":
            down = gb["cy"] > ga["cy"]
            y1, y2 = (ga["b"], gb["t"]) if down else (ga["t"], gb["b"])
            cv.path([(ga["cx"], y1), (gb["cx"], y2)], col, 1.75)
            wl = 1.75
            put(t, ga["cx"] - wl - 0.1, (y1 + y2) / 2 + need_h(t, wl, fs) / 2, wl, "right", "bottom")
        elif way == "down-left":
            xo = ga["cx"] - offset
            cv.path([(xo, ga["b"]), (xo, gb["cy"]), (gb["r"], gb["cy"])], col, 1.75)
            put(t, gb["r"] + 0.06, gb["cy"] - 0.04, xo - gb["r"] - 0.1)
        elif way == "left-up":
            xo = ga["cx"] - offset * 0 + 0.0
            xt = gb["cx"] + offset
            cv.path([(ga["l"], ga["cy"]), (xt, ga["cy"]), (xt, gb["b"])], col, 1.75)
            put(t, xt + 0.06, ga["cy"] - 0.04, ga["l"] - xt - 0.12)
        else:
            raise SystemExit("REFUSED: states5 has no way %r" % way)
    return {"t": "shapes", "x": bx, "y": by, "w": bw, "h": bh, "shapes": cv.prims}



# ---------------------------------------------------------------------------------------------------------------------------
# state diagram of any number of states in a column (chapter 18, the life of an encrypted PDF): the states are stacked from top to
# bottom in the order of data['states']; a transition to the next state is an arrow between the two boxes with its label to the right;
# a transition from a state to itself is a loop on the right of the box with its label beside it; the final state is followed by an end mark
# ---------------------------------------------------------------------------------------------------------------------------
def lifecycle_col(data, box, fs=8, sw=1.7, sh=0.42, sfs=9, top=0.3, lab_w=2.3):
    bx, by, bw, bh = box
    cv = Canvas()
    ids = [s["id"] for s in data["states"]]
    lab = {s["id"]: s["label"] for s in data["states"]}
    T = {(t[0], t[1]): t[2] for t in data["transitions"]}
    chain = {(ids[i], ids[i + 1]) for i in range(len(ids) - 1)}
    loops = {k for k in T if k[0] == k[1]}
    if set(T) != chain | loops:
        raise SystemExit("REFUSED: lifecycle_col draws a chain of states and loops; transitions %r are neither" % sorted(set(T) ^ (chain | loops)))
    n = len(ids)
    gap = (bh - top - n * sh) / (n - 1)
    x0 = bx + 0.1
    G = {sid: _geom(x0, by + top + i * (sh + gap), sw, sh) for i, sid in enumerate(ids)}
    for sid in ids:
        g = G[sid]
        cv.box("round", g["x"], g["y"], g["w"], g["h"], fill=SLATE, line=SLATE)
        cv.label_in(lab[sid], g["x"], g["y"], g["w"], g["h"], sfs, WHITE, bold=True)
    g0 = G[data["initial"]]
    cv.box("oval", g0["cx"] - 0.09, by + 0.02, 0.18, 0.18, fill=DARK, line=DARK)
    cv.path([(g0["cx"], by + 0.2), (g0["cx"], g0["t"])])
    lx = x0 + sw + 0.3
    for (a, b) in sorted(chain, key=lambda k: ids.index(k[0])):
        ga, gb = G[a], G[b]
        cv.path([(ga["cx"], ga["b"]), (gb["cx"], gb["t"])], ORANGE, 1.75)
        ym = (ga["b"] + gb["t"]) / 2
        t = T[(a, b)]
        h = need_h(t, lab_w, fs) + 0.02
        cv.line(ga["cx"] + 0.02, ym, lx - 0.04, ym, "C9BFAE", 0.75, False, True)
        cv.text(t, lx, ym - h / 2, lab_w, h, fs, INK, False, False, "left", "middle")
    for (a, b) in sorted(loops, key=lambda k: ids.index(k[0])):
        g = G[a]
        cv.path([(g["r"], g["cy"] - 0.09), (g["r"] + 0.26, g["cy"] - 0.09), (g["r"] + 0.26, g["cy"] + 0.09), (g["r"], g["cy"] + 0.09)], SLATE, 1.5, True)
        t = T[(a, b)]
        h = need_h(t, lab_w, fs) + 0.02
        cv.text(t, lx, g["cy"] - h / 2, lab_w, h, fs, INK, False, False, "left", "middle")
    for fid in data.get("final", []):
        g = G[fid]
        cv.path([(g["r"], g["cy"]), (g["r"] + 0.4, g["cy"])], ORANGE, 1.75)
        cv.box("oval", g["r"] + 0.4, g["cy"] - 0.14, 0.28, 0.28, fill=WHITE, line=DARK, lw=2)
        cv.box("oval", g["r"] + 0.46, g["cy"] - 0.08, 0.16, 0.16, fill=DARK, line=DARK)
    return {"t": "shapes", "x": bx, "y": by, "w": bw, "h": bh, "shapes": cv.prims}



# ---------------------------------------------------------------------------------------------------------------------------
# state diagram of any number of states in a column with transitions that skip ahead (chapter 18, a value through JSON): as lifecycle_col,
# plus every transition from a state to a later state that is not the next one, drawn out of the left side of the first state, down a margin
# on the left and into the left side of the second, with its label (wrapped) in the margin on the left of the column
# ---------------------------------------------------------------------------------------------------------------------------
def lifecycle_skip(data, box, fs=8, sw=1.5, sh=0.4, sfs=9, top=0.3, lab_w=1.6, margin=1.35):
    bx, by, bw, bh = box
    cv = Canvas()
    ids = [s["id"] for s in data["states"]]
    lab = {s["id"]: s["label"] for s in data["states"]}
    T = {(t[0], t[1]): t[2] for t in data["transitions"]}
    chain = {(ids[i], ids[i + 1]) for i in range(len(ids) - 1)}
    loops = {k for k in T if k[0] == k[1]}
    skips = {k for k in T if k not in chain and k not in loops and ids.index(k[1]) > ids.index(k[0])}
    if set(T) != chain | loops | skips:
        raise SystemExit("REFUSED: lifecycle_skip draws a chain of states, loops and skips ahead; transitions %r are none of these" % sorted(set(T) ^ (chain | loops | skips)))
    n = len(ids)
    gap = (bh - top - n * sh) / (n - 1)
    x0 = bx + margin + 0.1
    G = {sid: _geom(x0, by + top + i * (sh + gap), sw, sh) for i, sid in enumerate(ids)}
    for sid in ids:
        g = G[sid]
        cv.box("round", g["x"], g["y"], g["w"], g["h"], fill=SLATE, line=SLATE)
        cv.label_in(lab[sid], g["x"], g["y"], g["w"], g["h"], sfs, WHITE, bold=True)
    g0 = G[data["initial"]]
    cv.box("oval", g0["cx"] - 0.09, by + 0.02, 0.18, 0.18, fill=DARK, line=DARK)
    cv.path([(g0["cx"], by + 0.2), (g0["cx"], g0["t"])])
    lx = x0 + sw + 0.3
    for (a, b) in sorted(chain, key=lambda k: ids.index(k[0])):
        ga, gb = G[a], G[b]
        cv.path([(ga["cx"], ga["b"]), (gb["cx"], gb["t"])], ORANGE, 1.75)
        ym = (ga["b"] + gb["t"]) / 2
        t = T[(a, b)]
        h = need_h(t, lab_w, fs) + 0.02
        cv.line(ga["cx"] + 0.02, ym, lx - 0.04, ym, "C9BFAE", 0.75, False, True)
        cv.text(t, lx, ym - h / 2, lab_w, h, fs, INK, False, False, "left", "middle")
    for (a, b) in sorted(loops, key=lambda k: ids.index(k[0])):
        g = G[a]
        cv.path([(g["r"], g["cy"] - 0.09), (g["r"] + 0.26, g["cy"] - 0.09), (g["r"] + 0.26, g["cy"] + 0.09), (g["r"], g["cy"] + 0.09)], SLATE, 1.5, True)
        t = T[(a, b)]
        h = need_h(t, lab_w, fs) + 0.02
        cv.text(t, lx, g["cy"] - h / 2, lab_w, h, fs, INK, False, False, "left", "middle")
    for (a, b) in sorted(skips, key=lambda k: (ids.index(k[0]), ids.index(k[1]))):
        ga, gb = G[a], G[b]
        xm = bx + margin - 0.02
        cv.path([(ga["l"], ga["cy"]), (xm, ga["cy"]), (xm, gb["cy"]), (gb["l"], gb["cy"])], SLATE, 1.5, True)
        t = T[(a, b)]
        w = margin - 0.12
        h = need_h(t, w, fs) + 0.02
        cv.text(t, bx, (ga["cy"] + gb["cy"]) / 2 - h / 2, w, h, fs, INK, False, False, "right", "middle")
    for fid in data.get("final", []):
        g = G[fid]
        cv.path([(g["r"], g["cy"]), (g["r"] + 0.4, g["cy"])], ORANGE, 1.75)
        cv.box("oval", g["r"] + 0.4, g["cy"] - 0.14, 0.28, 0.28, fill=WHITE, line=DARK, lw=2)
        cv.box("oval", g["r"] + 0.46, g["cy"] - 0.08, 0.16, 0.16, fill=DARK, line=DARK)
    return {"t": "shapes", "x": bx, "y": by, "w": bw, "h": bh, "shapes": cv.prims}



# ---------------------------------------------------------------------------------------------------------------------------
# state diagram that branches (chapter 19, a launched process): states [initial, middle, final1, final2]; the transitions are
# initial>middle (one), middle>final1 (several) and middle>final2 (several). The middle state is a tall box on the right of the initial
# state; the two final states are tall boxes stacked on the right of it; every transition is a straight arrow from the middle box to the
# box it leads to, with its label above the arrow, in the order the transitions are given; each final state ends in a bull's-eye mark.
# ---------------------------------------------------------------------------------------------------------------------------
def lifecycle_branch(data, box, fs=8, sfs=9.5, w0=1.25, wm=1.5, wf=1.65):
    bx, by, bw, bh = box
    cv = Canvas()
    ids = [s["id"] for s in data["states"]]
    if len(ids) != 4 or data["final"] != ids[2:]:
        raise SystemExit("REFUSED: lifecycle_branch draws four states whose last two are the final states")
    lab = {s["id"]: s["label"] for s in data["states"]}
    s0, s1, f1, f2 = ids
    T = [(t[0], t[1], t[2]) for t in data["transitions"]]
    first = [t for t in T if (t[0], t[1]) == (s0, s1)]
    to1 = [t for t in T if (t[0], t[1]) == (s1, f1)]
    to2 = [t for t in T if (t[0], t[1]) == (s1, f2)]
    if len(first) != 1 or len(first) + len(to1) + len(to2) != len(T) or not to1 or not to2:
        raise SystemExit("REFUSED: lifecycle_branch needs one transition into the middle state and several out of it to each final state")
    eh = (bh - 0.2) / 2
    xs0, xs1, xf = bx + 0.25, bx + 3.0, bx + 6.7
    G0 = _geom(xs0, by + bh / 2 - 0.25, w0, 0.5)
    G1 = _geom(xs1, by + 0.2, wm, bh - 0.3)
    GF = {f1: _geom(xf, by, wf, eh), f2: _geom(xf, by + eh + 0.2, wf, eh)}
    for sid, g in ((s0, G0), (s1, G1), (f1, GF[f1]), (f2, GF[f2])):
        cv.box("round", g["x"], g["y"], g["w"], g["h"], fill=SLATE, line=SLATE)
        cv.label_in(lab[sid], g["x"], g["y"], g["w"], g["h"], sfs, WHITE, bold=True)
    cv.box("oval", G0["cx"] - 0.09, by + bh / 2 - 0.8, 0.18, 0.18, fill=DARK, line=DARK)
    cv.path([(G0["cx"], by + bh / 2 - 0.62), (G0["cx"], G0["t"])])

    def labelled(label, x1, x2, y, color):
        cv.path([(x1, y), (x2, y)], color, 1.75)
        w = x2 - x1 - 0.1
        h = need_h(label, w, fs) + 0.02
        cv.text(label, x1 + 0.05, y - 0.03 - h, w, h, fs, INK, False, False, "center", "bottom")
    labelled(first[0][2], G0["r"], G1["l"], G0["cy"], ORANGE)
    for items, g in ((to1, GF[f1]), (to2, GF[f2])):
        for k, t in enumerate(items):
            y = g["t"] + 0.42 + k * 0.46
            labelled(t[2], G1["r"], g["l"], y, ORANGE if g is GF[f1] else SLATE)
    for fid in (f1, f2):
        g = GF[fid]
        cv.path([(g["r"], g["cy"]), (g["r"] + 0.2, g["cy"])], ORANGE, 1.75)
        cv.box("oval", g["r"] + 0.2, g["cy"] - 0.14, 0.28, 0.28, fill=WHITE, line=DARK, lw=2)
        cv.box("oval", g["r"] + 0.26, g["cy"] - 0.08, 0.16, 0.16, fill=DARK, line=DARK)
    return {"t": "shapes", "x": bx, "y": by, "w": bw, "h": bh, "shapes": cv.prims}
