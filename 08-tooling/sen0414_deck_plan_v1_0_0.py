#!/usr/bin/env python3
"""Builds the lecture plan a chapter deck is rendered from, by reading the chapter's own sources and nothing else:
the chapter corpus (every concept, its taxonomy place, its one-sentence definition, its example label and its
four to six paragraphs), the chapter page's objectives and question bank, the chapter's RDODI research record
(the sources and the author-year strings the corpus cites them by) and the textbook ontology for the 3rd edition
(the book's own section headings for the chapter). Nothing is composed here that is not in one of those files:
this tool selects, orders and labels; it does not write teaching text.

The plan is data, so the deck renderer contains no chapter text of its own and the same renderer serves every chapter.
Usage: sen0414_deck_plan_v1_0_0.py <chapter-number, e.g. 04> <out.json>
"""
__version__ = "1.0.0"
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BOOK = "/home/claude/Ontologies/automate-python-book-3e/01-ontologies"

W, Y, E, H, K = 0, 1, 2, 3, 4          # the corpus writes every leaf's paragraphs in this order


def newest(folder, pattern):
    """the highest-versioned file matching the pattern, by SemVer order of the v<major>_<minor>_<patch> token"""
    best, bestkey = None, None
    for name in os.listdir(folder):
        m = re.fullmatch(pattern, name)
        if not m:
            continue
        key = tuple(int(p) for p in m.group(1).split("_"))
        if bestkey is None or key > bestkey:
            best, bestkey = os.path.join(folder, name), key
    if best is None:
        raise SystemExit("no file matching %s in %s" % (pattern, folder))
    return best


def load_corpus(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("corpus", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def research_sources(path):
    """the publications of the research record, in file order: (label, url, role). The label carries the author and
    year by which the corpus cites the source, so the deck quotes the record rather than restating it."""
    text = open(path, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'a res:Publication ;\s*rdfs:label "([^"]+)"@en ;\s*dcterms:source "([^"]+)"', text):
        label, url = m.group(1), m.group(2)
        role = "primary" if ('sourceRole "primary"' in text[m.end():m.end() + 400]) else "secondary"
        out.append([label, url, role])
    return out


def book_sections(chapter):
    """the chapter's own section headings, as the textbook ontology for the 3rd edition records them"""
    path = os.path.join(BOOK, "automate_python_3e_ch%s_v1_0_0.ttl" % chapter)
    text = open(path, encoding="utf-8").read()
    title = re.search(r'd:Ch%s a apb:Chapter ;\s*rdfs:label "([^"]+)"@en' % chapter, text).group(1)
    url = re.search(r'apb3:chapterUrl "([^"]+)"', text).group(1)
    secs = [m.group(1) for m in re.finditer(r'a apb:Section ;\s*rdfs:label "([^"]+)"@en', text)]
    return title, url, secs


def sentences(text):
    """split a paragraph into sentences, keeping abbreviations such as 3.14 and e.g. together"""
    parts = re.split(r'(?<=[.!?]) +(?=[A-Z(])', text)
    return [p.strip() for p in parts if p.strip()]


def shorten(text, limit):
    """the leading whole sentences of a paragraph that fit inside the character limit (at least one)"""
    out = ""
    for s in sentences(text):
        if out and len(out) + 1 + len(s) > limit:
            break
        out = (out + " " + s).strip()
    return out


def main():
    chapter, out_path = sys.argv[1], sys.argv[2]
    deck_dir = os.path.join(HERE, "ch%s-deck" % chapter)
    page_dir = os.path.join(HERE, "ch%s-page" % chapter)
    rdodi = os.path.join(REPO, "03-materials", "ch%s" % chapter, "rdodi")

    corpus_file = newest(HERE, r"sen0414_ch%s_corpus_v(\d+_\d+_\d+)\.py" % chapter)
    qbank_file = newest(page_dir, r"question_bank_v(\d+_\d+_\d+)\.json")
    research_file = newest(rdodi, r"sen0414_ch%s_research_v(\d+_\d+_\d+)\.ttl" % chapter)
    page_data_file = newest(page_dir, r"page_data_v(\d+_\d+_\d+)\.json")
    objectives_file = newest(page_dir, r"objectives_v(\d+_\d+_\d+)\.json")

    C = load_corpus(corpus_file)
    qbank = json.load(open(qbank_file, encoding="utf-8"))
    objectives = json.load(open(objectives_file, encoding="utf-8"))
    page = json.load(open(page_data_file, encoding="utf-8"))
    sources = research_sources(research_file)
    book_title, book_url, book_secs = book_sections(chapter)

    by_id = {n[0]: n for n in C.NODES}
    label = lambda n: n[1] or re.sub(r"(?<!^)(?=[A-Z])", " ", n[0])
    kids = lambda pid: [n for n in C.NODES if n[3] == pid]

    concepts, order = {}, []
    for n in C.NODES:
        nid, lvl, paras = n[0], n[2], n[5]
        rec = {"id": nid, "label": label(n), "level": lvl, "parent": n[3],
               "paras": [t for f, t in paras], "facets": [f for f, t in paras]}
        if lvl == 3:
            rec["example"] = n[4][0]
            rec["definition"] = n[4][1]
            rec["io"] = list(n[4][2]) if n[4][2] else None
        concepts[nid] = rec
        order.append(nid)

    tops = [n[0] for n in C.NODES if n[2] == 1]
    tree = []
    for t in tops:
        subs = []
        for s in kids(t):
            subs.append({"id": s[0], "leaves": [l[0] for l in kids(s[0])]})
        tree.append({"id": t, "subs": subs})

    # questions: the chapter's own bank, one per concept, spread over the branches in taxonomy order
    want = {q["concept"]: q for q in reversed(qbank)}          # the first item of each concept wins
    picked, seen_branch = [], {}
    for nid in order:
        if nid in want:
            branch = nid
            while concepts[branch]["parent"]:
                branch = concepts[branch]["parent"]
            seen_branch.setdefault(branch, 0)
            if seen_branch[branch] < 3:
                seen_branch[branch] += 1
                q = want[nid]
                picked.append({"concept": nid, "label": concepts[nid]["label"], "level": q["level"],
                               "q": q["q"], "answer": q["options"][q["answer"]], "why": q["why"],
                               "options": q["options"]})
    plan = {
        "_version": __version__,
        "chapter": int(chapter),
        "chapter_pad": chapter,
        "corpus_file": os.path.basename(corpus_file),
        "question_bank_file": os.path.basename(qbank_file),
        "research_file": os.path.basename(research_file),
        "objectives_file": os.path.basename(objectives_file),
        "page_data_file": os.path.basename(page_data_file),
        "book_title": book_title,
        "book_url": book_url,
        "book_sections": book_secs,
        "doc_title": C.DOC_TITLE,
        "doc_about": C.DOC_ABOUT,
        "interpreters": C.INTERPRETERS,
        "provenance": C.PROVENANCE,
        "competency_questions": C.CQS,
        "objectives": [[k, v[0], v[1]] for k, v in objectives.items() if re.fullmatch(r"CO\d+", k)],
        "objectives_note": objectives.get("_note", ""),
        "objectives_serves": objectives.get("_serves", []),
        "page_title": page.get("title", ""),
        "python": page.get("python", ""),
        "tree": tree,
        "concepts": concepts,
        "order": order,
        "sources": sources,
        "questions": picked,
    }
    json.dump(plan, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("written %s: %d concepts (%d leaves), %d questions, %d sources, %d book sections"
          % (os.path.basename(out_path), len(concepts),
             sum(1 for c in concepts.values() if c["level"] == 3), len(picked), len(sources), len(book_secs)))


if __name__ == "__main__":
    main()
