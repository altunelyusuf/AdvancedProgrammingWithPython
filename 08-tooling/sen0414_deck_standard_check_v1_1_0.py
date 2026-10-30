#!/usr/bin/env python3
"""sen0414_deck_standard_check v1.1.0 (python-pptx 1.0.2) - the deck standard of the SEN0414 lecture decks, D1 to D12 and M1, measured; code boxes recognised by their MONOSPACE FONT and
story slides recognised WITHOUT label words. A NEW tool beside sen0414_deck_standard_check_v1_0_0.py (which stays as committed, unchanged, and keeps printing what it prints); it edits nothing.
Written on the Owner's ruling of 2026-10-30 (about 03:40 Istanbul): no '>>>' prompts in code and no WHO/WHAT/... labels on slides, so the v1.0.0 detectors (a '>>> ' paragraph; WHO/WHAT labels) see nothing.
Usage:   sen0414_deck_standard_check_v1_1_0.py NN [deck.pptx [manifest.json]]     NN = chapter number (06, 07, 08 ...). Without deck.pptx the newest .pptx of 03-materials/chNN is read.
         sen0414_deck_standard_check_v1_1_0.py --selftest        builds the fixture decks (sen0414_deck_standard_check_fixtures_v1_1_0.py), prints expected and actual for every element of every
                                                                  fixture, exits 0 only when all are as expected.
Environment: SEN0414_ROOT (default the parent of this file's folder).
Result words, as printed: PASS, FAIL, NOT_MEASURED (the input of the measure is missing), CANNOT_RUN (the tool failed). Exit code 0 only when D1..D12 and M1 all PASS; 1 when any FAIL; 2 when any
NOT_MEASURED/CANNOT_RUN and none FAIL. A skip is not a pass. NOT_MEASURED and CANNOT_RUN are never a pass.

WHAT CHANGED AGAINST v1.0.0 (each stated; everything else is v1.0.0's code and definition)
  (a) code box  : a text shape (also inside a group) with at least one non-blank run, ALL of whose non-blank runs are set in a monospace font: a font name that, in lower case, contains 'courier'
                  (Courier New), 'consolas' or 'mono'. A shape whose whole text is '>>>' and whose top lies in the top 12 percent of the slide height is the deck's BRAND MARK and is not a code box.
                  A run without an explicit font name (inherited) does not count as monospace. Code slide = a slide holding at least one code box. Code line = a paragraph of a code box.
                  A prompt is no longer needed or looked for: the code box is the whole text of the shape.
  (b) D2        : applied to the boxes that are NOT code boxes (the rule 'no text box over 30 words' is a rule for prose). Code boxes are measured by D12 and D3.
  D12           : unchanged measure on the new code boxes: every paragraph's estimated width (characters x 0.6 x the largest run size, default 18 pt; Courier New advance = 0.6 em) fits the room
                  (box width minus left and right inset; for wrap='none' the distance from the box's left edge to the slide's right edge). Lines over the room are listed with the slide number.
  D3            : share of code slides that have BOTH (i) an explanation for EVERY code box and (ii) an executed result shown as a visual (target 100 percent).
                  (i) explanation = a non-code text box of at least 8 words that stands BESIDE the code box: either it overlaps the code box's horizontal span and its vertical gap to the code box is
                      at most 0.6 inch (above or below), or it overlaps the code box's vertical span and its horizontal gap is at most 0.6 inch (left or right). The 'run under' stamp does not count.
                  (ii) result visual, recognised from the decks' own construction (the chapter 8 and chapter 7 decks show 'What the run printed' as a native table or chart placed under or beside the code):
                      on the same slide a native table, a native chart, a picture shape of at least 3 percent of the slide area, or a drawn diagram (v1.0.0: at least one connector or arrow/chevron shape and at least three auto shapes that
                      carry text), whose top is not above the top of the code box it belongs to (it is placed with the code, not in the slide's header). A caption or a plain text line alone is not a visual.
                      What the check cannot see: whether the table or picture really is THE output of THIS code; it sees only that a visual result stands with the code.
  (c) M1        : compares the manifest (newest 03-materials/chNN/page/chapter_code_chNN_v*.json whose 'deck' field names this deck, or the file given as third argument) with the code boxes in slide
                  order, text and order. Per code slide in slide order the deck code = the paragraphs of all its code boxes (shape order), each with trailing whitespace removed, joined by newline,
                  trailing blank lines removed. The manifest code = the 'code' of the example at the same position, same normalisation. PASS when the number of examples equals the number of
                  code slides and every pair is equal (and the 'slide' field equals the slide number); FAIL otherwise, the first differences are printed. No code box on the deck: NOT_MEASURED when the
                  manifest is absent or lists no example; FAIL when the manifest lists examples (the deck lacks them). Manifest absent while code boxes exist: NOT_MEASURED.
  (d) story slide and D5 (rule fixed BEFORE the first run on the delivered decks)
        The decks mark a story slide by its construction, not by label words: it carries ONE real picture (a picture shape, the person or the object of the story), a credit line right after the picture,
        a live link, and the story told in 2-3 text boxes. Chapter 8 titles it 'Story: ...'; chapter 7 titles it with the story's own headline. So:
        STORY SLIDE = a slide (not the first, not the last, not a resources slide with 5 or more external links) that EITHER has a title (the first text box that is not the brand mark) beginning with
                      'Story' (any case) followed by ':' OR holds a picture shape of at least 8 percent of the slide area together with at least one external http(s) hyperlink.
        D5, for each story slide, needs ALL of:
          picture : a picture shape of at least 8 percent of the slide area;
          link    : at least one external http(s) hyperlink on the slide (a hyperlink on a shape or on a run is a relationship of the slide part, as in v1.0.0);
          facts   : the six facts of the story, told as sentences, found by mechanical patterns in the STORY TEXT. Story text = the text of the slide's text boxes of at least 5 words, leaving out the
                    title, the brand mark, the slide number, the credit line (the text box that follows the picture in shape order) and the link box (the box carrying the hyperlink).
                    who   : a name of two to four capitalised words, initials allowed ('Eric V. Smith', 'Ken Thompson', 'Bell Labs');
                    what  : an event verb: a word ending in -ed, or one of: wrote, made, gave, ran, took, began, became, built, said, was, were, had, saw, found, held, led, sent, told, won, chose, drew,
                            grew, knew, left, met, taught, thought, shipped, died, sketched;
                    when  : a year 1500 to 2099 (four digits);
                    where : one of in, at, from, near, on, to, of followed by (an optional a/an/the, an optional one lowercase word and) a capitalised word that is not a month or a weekday ('in Palo Alto', 'at Xerox PARC');
                    why   : a reason word: because, so that, since, therefore, that is why, which is why, why, in order to, need, needs, needed, reason;
                    how   : a means word: by, with, using, through, via, inside, how, means, 'in one/two/three ...'.
          WHAT THE CHECK CANNOT SEE: it cannot tell a person from an organisation or a title with capitals ('Python Enhancement Proposal' passes as a name), cannot tell a true date from any year, cannot
          tell a place from any capitalised word after a preposition, cannot see a reason that is told without a reason word (a contrast, a consequence), and cannot see that the facts belong together or
          are true. It sees that each of the six kinds of fact has a mechanical trace; the teaching reviewer reads the rest. A story slide that is neither titled 'Story' nor holds picture + link (for
          example a story with no picture and no title word) is not recognised and is not measured. No story slide at all: D5 NOT_MEASURED.
  (e) brand mark: a shape whose whole text is '>>>' in the top 12 percent of the slide height (v1.0.0: any text box '>>>'). Used for the divider test of D10 and the title test.
  (f) D4, D11   : as v1.0.0 (research concept list; the 'ANALOGY' / 'EVERYDAY' marker or the phrases 'is like a', 'think of', 'just as', 'imagine'). The deck-specific marker word 'ANALOGY' is a label of the
                  analogy, not one of the six story labels the Owner forbade.
D1, D6 to D10: as v1.0.0 (definitions below, unchanged).
DEFINITIONS KEPT FROM v1.0.0 (unchanged)
  text box     : every shape with a text frame (text boxes AND auto shapes carrying text, also inside groups); table cells are not boxes. Words = len(text.split()) of the whole frame.
  slide number : a text box whose text is 'k / N' (k = the slide's position, N = number of slides), or a slide-number field. D1: every slide numbered.
  analogy      : a text box that starts with 'ANALOGY' or 'EVERYDAY', or contains 'is like a/an/the', 'are like', 'think of', 'just as', 'imagine' (case-insensitive).
  key concept  : every primary-source concept of the chapter research (03-materials/chNN/rdodi/sen0414_chNN_research_vX_Y_Z.ttl, newest; class sen0414:PrimarySourceConcept, label rdfs:label),
                 de-duplicated by normalised label (lower case, parenthesis text removed, non-alphanumerics to one space, a trailing 's' of each word dropped).
  D4 measure   : share of key concepts occurring on a slide that holds an analogy text box (target 100 percent).   D11 measure: share of key concepts shown on a slide (target not below 90 percent).
  native chart : a graphic frame with a native PowerPoint chart. Chart picture = a picture whose alt text or name contains chart/graph/plot/histogram. D6: number of chart pictures (target 0).
  D7 measure   : the largest speaker-note word count of any slide (target at most 60).
  resources    : a slide whose title contains resources, where to go, further reading/watching or read more AND at least 5 external hyperlinks (D8).
  background   : the slide background colour (p:bg solid fill); if none, the fill of the first shape covering at least 95 percent of the slide. Dark = relative luminance below 0.5. D9: all slides on one side.
  divider      : a slide without the brand mark that is neither the first nor the last slide and has a title (the first text box). D10: a divider passes when it names at least one concept (a remaining
                 text box of at most 4 words after title, subtitle, picture caption and slide number), has a line of meaning for every concept (a remaining text box of at least 5 words, or a
                 'Name | meaning' box), and holds a visual (picture, native chart or native table).
Facts printed for every deck: slides, code slides, code boxes, native charts, analogy text boxes, longest non-code text box in words.
"""
__version__ = "1.1.0"
import glob, os, re, sys

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SEN0414_ROOT") or os.path.dirname(TOOL)
EMU_IN = 914400
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", os.path.basename(p))[-1]]


def newest(pat):
    f = sorted(glob.glob(pat), key=vkey)
    return f[-1] if f else None


try:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    import pptx
except Exception as e:  # pragma: no cover
    print("CANNOT_RUN python-pptx not importable: %s" % e); sys.exit(2)

NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main", "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
MONO = ("courier", "consolas", "mono")
PICMIN_STORY, PICMIN_RESULT = 0.08, 0.03


def walk(shapes):
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            for x in walk(sh.shapes):
                yield x
        else:
            yield sh


def words(t):
    return len(t.split())


def norm(t):
    t = re.sub(r"\([^)]*\)", " ", t.lower())
    t = re.sub(r"[^a-z0-9]+", " ", t).split()
    return " ".join(w[:-1] if len(w) > 3 and w.endswith("s") else w for w in t)


def lum(hexrgb):
    r, g, b = [int(hexrgb[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def all_mono(sh):
    """(a) every non-blank run of the shape is in an explicitly named monospace font; at least one such run."""
    runs = [r for p in sh.text_frame.paragraphs for r in p.runs if r.text.strip()]
    return bool(runs) and all((r.font.name or "").lower() != "" and any(m in r.font.name.lower() for m in MONO) for r in runs)


def has_link(sh):
    try:
        if sh.click_action.hyperlink.address:
            return True
    except Exception:
        pass
    if sh.has_text_frame:
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if r.hyperlink.address:
                    return True
    return False


class Box:
    def __init__(self, sh, H):
        self.sh = sh
        self.text = sh.text_frame.text
        self.l, self.t, self.w, self.h = sh.left or 0, sh.top or 0, sh.width or 0, sh.height or 0
        self.words = words(self.text)
        self.paras = [p.text for p in sh.text_frame.paragraphs]
        self.mark = self.text.strip() == ">>>" and self.t < 0.12 * H
        self.code = (not self.mark) and all_mono(sh)


class Slide:
    def __init__(self, idx, s, W, H, n):
        self.i, self.s, self.W, self.H, self.n = idx, s, W, H, n
        self.shapes = list(walk(s.shapes))
        self.boxes = [Box(x, H) for x in self.shapes if x.has_text_frame and x.text_frame.text.strip() != ""]
        self.tables = [x for x in self.shapes if getattr(x, "has_table", False) and x.has_table]
        self.charts = [x for x in self.shapes if getattr(x, "has_chart", False) and x.has_chart]
        self.pics = [x for x in self.shapes if x.shape_type == MSO_SHAPE_TYPE.PICTURE]
        self.notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
        self.links = [r.target_ref for r in s.part.rels.values() if r.is_external and r.target_ref.lower().startswith("http")]
        self.text = " ".join(b.text for b in self.boxes) + " " + " ".join(c.text_frame.text for t in self.tables for r in t.table.rows for c in r.cells)
        self.codeboxes = [b for b in self.boxes if b.code]
        self.prose = [b for b in self.boxes if not b.code]

    def numbered(self):
        if any(re.fullmatch(r"\s*%d\s*/\s*%d\s*" % (self.i, self.n), b.text) for b in self.boxes):
            return True
        return bool(self.s._element.xpath('.//a:fld[@type="slidenum"]'))

    def title(self):
        for b in self.boxes:
            if not b.mark:
                return b.text
        return ""

    def title_box(self):
        for b in self.boxes:
            if not b.mark:
                return b
        return None

    def has_mark(self):
        return any(b.mark for b in self.boxes)

    def bgcolor(self):
        x = self.s._element.xpath("./p:cSld/p:bg//a:srgbClr/@val")
        if x:
            return x[0].upper()
        for sh in self.shapes:
            if sh.width and sh.height and sh.width * sh.height >= 0.95 * self.W * self.H:
                y = sh._element.xpath("./p:spPr/a:solidFill/a:srgbClr/@val")
                if y:
                    return y[0].upper()
        return None

    def bigpics(self, share):
        return [p for p in self.pics if p.width * p.height >= share * self.W * self.H]


ANALOGY = re.compile(r"^\s*(ANALOGY|EVERYDAY)\b|\b(is|are) like (a|an|the)\b|\bthink of\b|\bjust as\b|\bimagine\b", re.I)


def research_concepts(ch):
    f = newest(os.path.join(ROOT, "03-materials", "ch%s" % ch, "rdodi", "sen0414_ch%s_research_v*.ttl" % ch))
    if not f:
        return None, []
    txt = open(f, encoding="utf-8").read()
    labs = re.findall(r"a sen0414:PrimarySourceConcept\s*;\s*rdfs:label\s+\"((?:[^\"\\]|\\.)*)\"", txt)
    seen, out = set(), []
    for l in labs:
        k = norm(l)
        if k and k not in seen:
            seen.add(k); out.append((l, k))
    return f, out


def is_arrow(sh):
    try:
        return sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and re.search(r"ARROW|CHEVRON", str(sh.auto_shape_type), re.I) is not None
    except Exception:
        return False


def beside(c, n):
    """note box n stands beside code box c: above/below (horizontal overlap, vertical gap <= 0.6 in) or left/right (vertical overlap, horizontal gap <= 0.6 in)."""
    hov = min(c.l + c.w, n.l + n.w) - max(c.l, n.l) > 0
    vov = min(c.t + c.h, n.t + n.h) - max(c.t, n.t) > 0
    vgap = max(n.t - (c.t + c.h), c.t - (n.t + n.h))
    hgap = max(n.l - (c.l + c.w), c.l - (n.l + n.w))
    return (hov and vgap <= 0.6 * EMU_IN) or (vov and hgap <= 0.6 * EMU_IN)


def explained(sl):
    notes = [b for b in sl.prose if b.words >= 8 and not b.text.startswith("run under") and not b.mark]
    return all(any(beside(c, n) for n in notes) for c in sl.codeboxes)


def visual_result(sl):
    top = min(c.t for c in sl.codeboxes) - int(0.05 * EMU_IN)
    if any(x.top is not None and x.top >= top for x in sl.tables + sl.charts):
        return True
    if any(p.top >= top for p in sl.bigpics(PICMIN_RESULT)):
        return True
    codeids = {c.sh.shape_id for c in sl.codeboxes}
    conn = len(sl.s._element.xpath(".//p:cxnSp")) + sum(1 for x in sl.shapes if is_arrow(x))
    texted = sum(1 for x in sl.shapes if x.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and x.has_text_frame and x.text_frame.text.strip()
                 and x.shape_id not in codeids and x.top >= top and not x.text_frame.text.strip() == ">>>")
    return conn >= 1 and texted >= 3


def wrapped_lines(sl):
    bad, total = [], 0
    for b in sl.codeboxes:
        bp = b.sh.text_frame._txBody.find("{%s}bodyPr" % NS["a"])
        wrap = bp.get("wrap", "square")
        li, ri = int(bp.get("lIns", 91440)), int(bp.get("rIns", 91440))
        room = (b.w - li - ri) if wrap != "none" else (sl.W - b.l - li)
        for p in b.sh.text_frame.paragraphs:
            szs = [r.font.size.pt for r in p.runs if r.font.size] or [18.0]
            sz = max(szs)
            w = len(p.text) * 0.6 * sz * 12700
            total += 1
            if w > room:
                bad.append((sl.i, len(p.text), round(w / room, 2)))
    return bad, total


def deck_code_by_slide(S):
    out = []
    for s in S:
        if s.codeboxes:
            lines = [p.rstrip() for b in s.codeboxes for p in b.paras]
            out.append((s.i, "\n".join(lines).rstrip()))
    return out


def manifest_check(ch, S, mpath, deck=""):
    import json
    if not mpath:  # the newest manifest whose 'deck' field names THIS deck
        for c in sorted(glob.glob(os.path.join(ROOT, "03-materials", "ch%s" % ch, "page", "chapter_code_ch%s_v*.json" % ch)), key=vkey, reverse=True):
            try:
                if os.path.basename(json.load(open(c, encoding="utf-8")).get("deck", "")) == os.path.basename(deck):
                    mpath = c; break
            except Exception:
                pass
    dk = deck_code_by_slide(S)
    if not mpath or not os.path.exists(mpath):
        return "NOT_MEASURED", "no chapter-code manifest names this deck (%s) in 03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (os.path.basename(deck), ch, ch)
    ex = json.load(open(mpath, encoding="utf-8"))["examples"]
    rel = os.path.relpath(mpath, ROOT)
    if not dk:
        if not ex:
            return "NOT_MEASURED", "no code box on the deck and no example in the manifest %s" % rel
        return "FAIL", "no code box on the deck, but the manifest %s lists %d examples" % (rel, len(ex))
    nc = lambda t: "\n".join(l.rstrip() for l in t.replace("\r\n", "\n").split("\n")).rstrip()
    diffs, equal = [], 0
    if len(ex) != len(dk):
        diffs.append("%d manifest examples, %d deck code slides" % (len(ex), len(dk)))
    for k, ((si, dc), e) in enumerate(zip(dk, ex), 1):
        ok = True
        if e.get("slide") != si:
            diffs.append("example %d: manifest slide %s, deck slide %d" % (k, e.get("slide"), si)); ok = False
        if nc(e["code"]) != dc:
            diffs.append("example %d (slide %d): code text differs" % (k, si)); ok = False
        equal += ok
    return ("PASS" if not diffs else "FAIL"), "%d of %d deck code slides equal their manifest example in text and order%s; manifest %s" % (
        equal, len(dk), ("; differences: %s" % diffs[:6]) if diffs else "", rel)


# ---- story slides and the six facts (patterns fixed before the first run, see the docstring)
MONTHS = "January February March April May June July August September October November December Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
F_WHO = re.compile(r"\b[A-Z][a-zà-ÿ]+(?:\s+(?:[A-Z]\.|[A-Z][a-zà-ÿ]+)){1,3}")
F_WHAT = re.compile(r"\b\w{2,}ed\b|\b(wrote|made|gave|ran|took|began|became|built|said|was|were|had|saw|found|held|led|sent|told|won|chose|drew|grew|knew|left|met|taught|thought|shipped|died|sketched)\b")
F_WHEN = re.compile(r"\b(1[5-9]\d\d|20\d\d)\b")
F_WHERE = re.compile(r"\b(?:in|at|from|near|on|to|of)\s+(?:(?:a|an|the)\s+)?(?:[a-z]+\s+)?([A-Z][\w.]*)")
F_WHY = re.compile(r"\b(because|so that|since|therefore|that is why|which is why|why|in order to|need|needs|needed|reason)\b", re.I)
F_HOW = re.compile(r"\b(by|with|using|through|via|inside|how|means|in (?:one|two|three|four|five|a few) \w+)\b", re.I)


def is_story(s):
    if s.i == 1 or s.i == s.n or len(s.links) >= 5:
        return False
    if re.match(r"\s*story\s*:", s.title(), re.I):
        return True
    return bool(s.bigpics(PICMIN_STORY)) and bool(s.links)


def story_text(s):
    skip = set()
    tb = s.title_box()
    if tb:
        skip.add(tb.sh.shape_id)
    for k, x in enumerate(s.shapes[:-1]):
        if x.shape_type == MSO_SHAPE_TYPE.PICTURE and s.shapes[k + 1].has_text_frame:
            skip.add(s.shapes[k + 1].shape_id)
    keep = [b for b in s.boxes if b.sh.shape_id not in skip and not b.mark and not has_link(b.sh)
            and not re.fullmatch(r"\s*\d+\s*/\s*\d+\s*", b.text) and b.words >= 5]
    return " ".join(b.text for b in keep)


def six_facts(t):
    f = {"who": bool(F_WHO.search(t)), "what": bool(F_WHAT.search(t)), "when": bool(F_WHEN.search(t)),
         "where": any(m.group(1) not in MONTHS for m in F_WHERE.finditer(t)), "why": bool(F_WHY.search(t)), "how": bool(F_HOW.search(t))}
    return f


def measure(ch, deck, mpath=None):
    prs = Presentation(deck)
    W, H = prs.slide_width, prs.slide_height
    n = len(prs.slides)
    S = [Slide(i, s, W, H, n) for i, s in enumerate(prs.slides, 1)]
    res = []  # (id, name, status, measured)
    add = lambda i, name, status, meas: res.append((i, name, status, meas))
    code_slides = [s for s in S if s.codeboxes]
    n_charts = sum(len(s.charts) for s in S)
    analog = [(s.i, b) for s in S for b in s.boxes if ANALOGY.search(b.text)]
    longest = max([(b.words, s.i) for s in S for b in s.prose] or [(0, 0)])
    facts = "slides=%d code_slides=%d code_boxes=%d native_charts=%d analogies=%d longest_noncode_box_words=%d (slide %d)" % (
        n, len(code_slides), sum(len(s.codeboxes) for s in S), n_charts, len(analog), longest[0], longest[1])

    miss = [s.i for s in S if not s.numbered()]
    add("D1", "every slide is numbered", "PASS" if not miss else "FAIL", "%d of %d slides numbered; unnumbered: %s" % (n - len(miss), n, miss or "none"))
    over = [(s.i, b.words) for s in S for b in s.prose if b.words > 30]
    add("D2", "no text box over 30 words (code boxes are measured by D12 and D3)", "PASS" if not over else "FAIL",
        "longest non-code box %d words (slide %d); %d boxes over 30: %s" % (longest[0], longest[1], len(over), over[:12]))
    good = [s.i for s in code_slides if explained(s) and visual_result(s)]
    noexp = [s.i for s in code_slides if not explained(s)]
    novis = [s.i for s in code_slides if not visual_result(s)]
    if not code_slides:
        add("D3", "code slides: explanation beside the code + executed result as a visual", "NOT_MEASURED", "no code box on the deck")
    else:
        add("D3", "code slides: explanation beside the code + executed result as a visual", "PASS" if len(good) == len(code_slides) else "FAIL",
            "%d of %d code slides complete (%.0f%%); without explanation: %s; without visual result: %s" % (len(good), len(code_slides), 100.0 * len(good) / len(code_slides), noexp, novis))
    rf, concepts = research_concepts(ch)
    if not concepts:
        add("D4", "every key concept has an everyday analogy", "NOT_MEASURED", "no research concept list found for chapter %s" % ch)
        add("D11", "coverage of the research concepts", "NOT_MEASURED", "no research concept list found for chapter %s" % ch)
    else:
        an_slide_text = norm(" ".join(next(s.text for s in S if s.i == i) for i in sorted({i for i, _ in analog})))
        have = [l for l, k in concepts if k in an_slide_text]
        add("D4", "every key concept has an everyday analogy", "PASS" if len(have) == len(concepts) else "FAIL",
            "%d of %d key concepts have an analogy slide or box (%.1f%%); research %s" % (len(have), len(concepts), 100.0 * len(have) / len(concepts), os.path.relpath(rf, ROOT)))
        alltext = norm(" ".join(s.text for s in S))
        shown = [l for l, k in concepts if k in alltext]
        pct = 100.0 * len(shown) / len(concepts)
        missing = [l for l, k in concepts if k not in alltext]
        add("D11", "coverage of the research concepts", "PASS" if pct >= 90.0 else "FAIL",
            "%d of %d research concepts appear on a slide = %.1f%% (target not below 90); not shown (%d): %s" % (len(shown), len(concepts), pct, len(missing), "; ".join(missing[:40]) + (" ..." if len(missing) > 40 else "")))
    stories = [s for s in S if is_story(s)]
    if not stories:
        add("D5", "every story has a real picture, a live link and the six facts told as sentences", "NOT_MEASURED", "no story slide recognised (title 'Story:' or picture + live link)")
    else:
        det, okc = [], 0
        for s in stories:
            pic = bool(s.bigpics(PICMIN_STORY))
            fx = six_facts(story_text(s))
            lack = [k for k, v in fx.items() if not v]
            ok = pic and bool(s.links) and not lack
            okc += ok
            det.append("slide %d: picture=%s live_links=%d facts_missing=%s" % (s.i, "yes" if pic else "no", len(s.links), "/".join(lack) or "none"))
        add("D5", "every story has a real picture, a live link and the six facts told as sentences", "PASS" if okc == len(stories) else "FAIL",
            "%d of %d story slides complete; %s" % (okc, len(stories), "; ".join(det)))
    cpics = []
    for s in S:
        for p in s.pics:
            d = (p._element.xpath("./p:nvPicPr/p:cNvPr/@descr") or [""])[0] + " " + p.name
            if re.search(r"chart|graph|plot|histogram", d, re.I):
                cpics.append(s.i)
    add("D6", "every chart is a native chart object", "PASS" if not cpics else "FAIL", "%d native charts, %d chart pictures %s" % (n_charts, len(cpics), cpics or ""))
    nw = [(s.i, words(s.notes)) for s in S]
    overn = [x for x in nw if x[1] > 60]
    add("D7", "speaker notes at most 60 words per slide", "PASS" if not overn else "FAIL", "longest note %d words (slide %d); %d slides over 60: %s" % (max(w for _, w in nw), max(nw, key=lambda x: x[1])[0], len(overn), overn))
    res_s = [s for s in S if re.search(r"resources|where to go|further (reading|watching)|read more", s.title(), re.I) and len(s.links) >= 5]
    add("D8", "a resources slide with links", "PASS" if res_s else "FAIL", "resources slide(s): %s with %s external links" % ([s.i for s in res_s] or "none", [len(s.links) for s in res_s] or 0))
    cols = [(s.i, s.bgcolor()) for s in S]
    if any(c is None for _, c in cols):
        add("D9", "one background scheme", "NOT_MEASURED", "no background colour readable on slides %s" % [i for i, c in cols if c is None])
    else:
        dk = ["D" if lum(c) < 0.5 else "L" for _, c in cols]
        sw = sum(1 for a, b in zip(dk, dk[1:]) if a != b)
        add("D9", "one background scheme", "PASS" if len(set(dk)) == 1 else "FAIL", "%d dark, %d light slides, %d switches; colours %s" % (dk.count("D"), dk.count("L"), sw, sorted({c for _, c in cols})))
    divs = [s for s in S if not s.has_mark() and 1 < s.i < n and s.title()]
    if not divs:
        add("D10", "every divider names its concepts with a meaning line and a visual", "NOT_MEASURED", "no divider found")
    else:
        det, okc = [], 0
        for s in divs:
            rest = [b for b in s.boxes if not re.fullmatch(r"\s*\d+\s*/\s*\d+\s*", b.text)]
            rest = rest[2:]
            caps = set()
            for k, x in enumerate(s.shapes[:-1]):
                if x.shape_type == MSO_SHAPE_TYPE.PICTURE and s.shapes[k + 1].has_text_frame:
                    caps.add(s.shapes[k + 1].shape_id)
            rest = [b for b in rest if b.sh.shape_id not in caps]
            pills = [b for b in rest if b.words <= 4]
            meaning = [b for b in rest if b.words >= 5 or ("|" in b.text and words(b.text.split("|", 1)[1]) >= 5)]
            vis = bool(s.pics or s.charts or s.tables)
            ok = len(pills) >= 1 and len(meaning) >= len(pills) and vis
            okc += ok
            det.append("slide %d: concepts=%d meaning_lines=%d visual=%s" % (s.i, len(pills), len(meaning), "yes" if vis else "no"))
        add("D10", "every divider names its concepts with a meaning line and a visual", "PASS" if okc == len(divs) else "FAIL", "%d of %d dividers complete; %s" % (okc, len(divs), "; ".join(det)))
    badl, tot = [], 0
    for s in code_slides:
        b, t = wrapped_lines(s); badl += b; tot += t
    if not code_slides:
        add("D12", "no code line wraps", "NOT_MEASURED", "no code box on the deck")
    else:
        add("D12", "no code line wraps", "PASS" if not badl else "FAIL", "%d of %d code lines exceed their room (slide, characters, width/room): %s" % (len(badl), tot, badl[:10]))
    st, meas = manifest_check(ch, S, mpath, deck)
    add("M1", "chapter-code manifest equals the deck's code boxes (text, order)", st, meas)
    return facts, res


def verdict(res):
    fails = [i for i, _, st, _ in res if st == "FAIL"]
    nm = [i for i, _, st, _ in res if st in ("NOT_MEASURED", "CANNOT_RUN")]
    return fails, nm


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) < 2:
        print("usage: sen0414_deck_standard_check_v1_1_0.py NN [deck.pptx [manifest.json]] | --selftest"); return 2
    ch = argv[1].zfill(2)
    deck = argv[2] if len(argv) > 2 else newest(os.path.join(ROOT, "03-materials", "ch%s" % ch, "*.pptx"))
    if not deck or not os.path.exists(deck):
        print("CANNOT_RUN no deck for chapter %s" % ch); return 2
    facts, res = measure(ch, deck, argv[3] if len(argv) > 3 else None)
    print("sen0414_deck_standard_check v%s | python-pptx %s | chapter %s | deck %s" % (__version__, pptx.__version__, ch, os.path.relpath(deck, ROOT)))
    print("FACTS " + facts)
    for i, name, st, meas in res:
        print("%s %s %s | %s" % (i, st, name, meas))
    fails, nm = verdict(res)
    print("SUMMARY PASS=%d FAIL=%d NOT_MEASURED=%d | failing: %s%s" % (sum(1 for r in res if r[2] == "PASS"), len(fails), len(nm), ",".join(fails) or "none",
                                                                     (" | not measured: " + ",".join(nm)) if nm else ""))
    if fails:
        print("RESULT FAILING (exit 1): deck standard not met")
        return 1
    if nm:
        print("RESULT NOT_MEASURED (exit 2)")
        return 2
    print("RESULT PASS (exit 0)")
    return 0


def selftest():
    """Builds every fixture (sen0414_deck_standard_check_fixtures_v1_1_0.py) into a temporary folder, runs measure() on it and prints expected and actual for each element."""
    global ROOT
    import importlib.util, shutil, tempfile
    spec = importlib.util.spec_from_file_location("fx110", os.path.join(TOOL, "sen0414_deck_standard_check_fixtures_v1_1_0.py"))
    fx = importlib.util.module_from_spec(spec); spec.loader.exec_module(fx)
    tmp = tempfile.mkdtemp(prefix="deckstd110_")
    old_root, bad, total = ROOT, 0, 0
    try:
        for name, (root, deck, expected) in fx.build_all(tmp).items():
            ROOT = root
            _, res = measure(fx.CH, deck)
            got = {i: st for i, _, st, _ in res}
            line = []
            for el in fx.ELEMENTS:
                total += 1
                ok = got.get(el) == expected[el]
                bad += (not ok)
                line.append("%s expected %s actual %s %s" % (el, expected[el], got.get(el), "ok" if ok else "MISMATCH"))
            print("FIXTURE %s" % name)
            for l in line:
                print("   " + l)
    finally:
        ROOT = old_root
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST %d element checks over the fixtures, %d mismatches" % (total, bad))
    print("SELFTEST " + ("OK (exit 0)" if bad == 0 else "FAILED (exit 1)"))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except SystemExit:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        print("CANNOT_RUN %s" % e); sys.exit(2)
