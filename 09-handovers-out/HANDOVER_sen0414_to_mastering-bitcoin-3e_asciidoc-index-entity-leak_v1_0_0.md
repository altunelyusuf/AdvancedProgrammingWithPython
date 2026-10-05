# Handover to the Mastering Bitcoin 3rd-edition ontology package: an AsciiDoc character entity leaks into labels, IRIs and carried text

**From:** the SEN0414 course repository (`altunelyusuf/AdvancedProgrammingWithPython`), its chapter-page lineage
session, 2026-10-05, while applying an adversarial audit of the SEN0401 chapter 1 interactive page to the five
SEN0414 chapter pages. The audit's finding F-C7 named two labels in one file; this handover is the result of
checking how far the same leak reaches.

**To:** the session that owns `Ontologies/mastering-bitcoin-3e` (package version 0.9.0, `VERSION.txt`).

**Not an edit.** Under OE boundary B1 and the monorepo's own session-ownership rule, that package is not this
session's to change. Nothing in it has been modified. Every figure below was produced this session, by reading
the files on disk and by fetching the authors' own source at the commit the package pins.

**Where this is filed, and why it is not in your inbox.** `mastering-bitcoin-3e` has no `07-handover-inbox/`,
so there was nowhere in it to deposit this without creating a directory inside a package this session does not
own. The monorepo's `GOVERNANCE.md` prescribes a pull request for a cross-package finding; this session is
forbidden git operations, so it cannot open one. This file therefore sits in the sending repository, which OE's
L-115 names as the fallback when the addressee has no inbox. **It has been filed, not delivered** — in the words
of this framework's own G80, a proposal the addressee never receives is waiting on the sender. Please either
copy it into `mastering-bitcoin-3e/07-handover-inbox/pending/` (creating the inbox the other four packages of
the monorepo already have) or hand it to that session directly.

---

## 1. What is wrong

The authors of *Mastering Bitcoin*, 3rd edition, write an apostrophe, an em dash, an en dash and a right
double quote inside their AsciiDoc as XML character entities — `&#x27;`, `&#x2014;`, `&#x2013;`, `&#x201d;` —
because AsciiDoc would otherwise substitute them. An AsciiDoc processor decodes these before anything is
rendered. This package's harvest does not decode them, so the entity text travels into the register and is
presented to a reader, and to a SPARQL query, as if it were part of the book's own wording.

Confirmed at the pinned commit `275c4eb8eab8800c6adc39f8def8e8f8fa356a57`, fetched this session.
`ch01_intro.adoc` line 130 carries the index marker

```
Satoshi Nakamoto's invention ((("Byzantine Generals&#x27; Problem")))((("distributed computing problem")))is
```

while line 132, the prose two lines below it, reads `"Byzantine Generals' Problem."` with an ordinary
apostrophe. The entity belongs to the index term, by the authors' deliberate choice; it is not part of the
term's own text.

## 2. How far it reaches — nine files, 19 occurrences, in two entity forms

Counted by `grep -o '&#x[0-9a-fA-F]+;'` over every file of the package, and then by reading every remaining
`&` in `01-ontologies/` to separate the leak from legitimate ampersands.

| File | occurrences | sha256 (first 16) |
|---|---|---|
| `01-ontologies/mastering_bitcoin_3e_ch01_v1_1_0.ttl` | 2 | `d17a3f30b3c3f333` |
| `01-ontologies/mastering_bitcoin_3e_ch08_v1_1_0.ttl` | 1 | `05a0daca98402c5f` |
| `01-ontologies/mastering_bitcoin_3e_ch12_v1_1_0.ttl` | 2 | `f27b40c0ca1fd761` |
| `01-ontologies/mastering_bitcoin_3e_ch14_v1_1_0.ttl` | 1 | `ce1d654044cd5857` |
| `01-ontologies/mastering_bitcoin_3e_appA_v1_1_0.ttl` | 2 | `9e47ca4855417e30` |
| `01-ontologies/mastering_bitcoin_3e_supplements_v1_0_0.ttl` | 4 | `36eadeba2925b202` |
| `00-source-inventory/source_inventory_v1_2_0.json` | 4 | `d53637f79d4892fc` |
| `02-shacl-safeguards/fixtures/fixture_passage_wrong_line_v1_0_0.ttl` | 2 | `151141b809138bdf` |
| `01-ontologies/mastering_bitcoin_3e_ch09_v1_1_0.ttl` | 1, and it is a **named** entity | `f8987f9563ea9afd` |

The leak is not only in the numeric form. `mbb:Passage_ch09_carve_outs_CPFP` carries
`mbb:text "… being actively developed as of this writing&mdash;ephemeral anchors."` — the same defect written
`&mdash;` rather than `&#x2014;`. Any fix that maps a fixed list of numeric entities would leave this one
standing, which is the argument for decoding with `html.unescape` rather than with a hand-written table.

The other 16 chapter, appendix, preface, figure, repository and vocabulary files are clean. Four ampersands in
`01-ontologies/` are legitimate and must survive any fix: the `&` separators of a BIP 21 payment URI in
chapter 2's listing 1, the shell `&&` in chapter 3's listing 10, and the C++ reference
`const Consensus::Params&` in chapter 12's listing 3. A decoding step over `clean()` leaves all four
untouched, since none of them forms an entity; a blanket rule refusing every `&` would not.

**It is not only labels.** The audit found the leak in two `rdfs:label` values. It is in four places:

1. **Concept and passage labels** — the index-term case the audit named:
   - `rdfs:label "Byzantine Generals&#x27; Problem"` and `rdfs:label "Where Introduction first indexes Byzantine Generals&#x27; Problem"` (chapter 1)
   - `rdfs:label "Moore&#x27;s Law"` and `rdfs:label "Where Mining and Consensus first indexes Moore&#x27;s Law"` (chapter 12)
   - `rdfs:label "Gambler&#x27;s Ruin problem"` and `rdfs:label "Where The Bitcoin Whitepaper by Satoshi Nakamoto first indexes Gambler&#x27;s Ruin problem"` (appendix A)
2. **A section label** — `rdfs:label "State Channels&#x2014;Basic Concepts and Terminology"` on `mbb:Sec_ch14_010`, which is the title of a real section of chapter 14 and should read `State Channels—Basic Concepts and Terminology`.
3. **Carried passage text, under attribution** — `mbb:text "ALL|ANYONECANPAY :: This construction can be used to make a \"crowdfunding&#x201d;-style transaction."` on `mbb:Passage_ch08_crowdfunding`. This one matters more than the labels: the triple carries `dcterms:creator`, `dcterms:license <…by-sa/4.0/>` and the pinned commit, so the package is attributing to the authors a sentence they did not write in that form. The same applies to `mbb:glossaryDefinition` and `mbb:text` on the offchain-transactions glossary entry, where two `&#x2014;` stand where two em dashes belong.
4. **IRI local names** — because `mbb3_build_part_v1_1_0.py` builds the local name from the term by
   `slug = lambda s: re.sub(r"_+", "_", re.sub(r"[^A-Za-z0-9]+", "_", s)).strip("_")`, the entity is slugged
   into the identifier itself. Six IRIs currently carry it:

   ```
   mbb:Concept_Byzantine_Generals_x27_Problem      mbb:Passage_ch01_Byzantine_Generals_x27_Problem
   mbb:Concept_Moore_x27_s_Law                     mbb:Passage_ch12_Moore_x27_s_Law
   mbb:Concept_Gambler_x27_s_Ruin_problem          mbb:Passage_appA_Gambler_x27_s_Ruin_problem
   ```

## 3. The cause, located in the code

Two files, read this session:

- `03-tooling/mbb3_extract_inventory_v1_2_0.py` builds the inventory. Its index-term scan is
  `idx = re.findall(r'\(\(\(\s*"([^"]+)"', t)`, and its section and part titles are built by stripping
  `\(\(\(.*?\)\)\)` markers and role markup. Neither path decodes character entities, so
  `index_primary_terms` and `sections[].title` already hold the entity text — which is why
  `00-source-inventory/source_inventory_v1_2_0.json` carries four occurrences before any ontology is written.
- `03-tooling/mbb3_build_part_v1_1_0.py` writes the concepts, passages and sections from that inventory and
  from the source. Its `clean()` function removes footnotes, cross-references, URL macros, role markup and
  inline formatting; it does not decode entities either, which is how the chapter 8 passage text and the
  glossary definition acquired theirs.

The leak is therefore a single missing step in harvesting, in two places, not six separate data defects.

## 4. Recommended fix

1. **Decode once, in `clean()`**, in a new version of `mbb3_build_part_*.py`:
   `html.unescape` applied to the cleaned string. A hand-written map of the numeric entities the book uses
   (`&#x27;`, `&#x2013;`, `&#x2014;`, `&#x201d;`) would be smaller and more auditable, but it would miss the
   `&mdash;` of chapter 9, so the general decoder is the safer choice here. **Either way it keeps the fidelity
   gate honest**, because
   `mbb3_passage_fidelity_v1_0_2.py` imports `clean` out of the builder by
   `exec(b[b.index("IDX = re.compile"):b.index("PART = ")], ns)` — both sides of the comparison then decode,
   and the gate neither breaks nor has to be relaxed. Decoding in the builder alone, outside `clean()`, would
   make every affected passage fail fidelity.
2. **Decode in the extractor too**, in a new version of `mbb3_extract_inventory_*.py`, for
   `index_primary_terms` and for the section and part titles — otherwise the inventory stays wrong and the
   coverage gate keeps measuring against entity text.
3. **Expect a MAJOR bump on the affected ontology files.** Decoding changes the slug, so
   `mbb:Concept_Byzantine_Generals_x27_Problem` becomes `mbb:Concept_Byzantine_Generals_Problem`,
   `mbb:Concept_Moore_x27_s_Law` becomes `mbb:Concept_Moore_s_Law`, and so on. Six IRIs are renamed, which is a
   removal under BP-D7, not a backwards-compatible addition. The three chapter files, the appendix file and the
   supplements file need new versions; the inventory and the negative fixture need regenerating with them.
4. **Check the consumers before renaming.** The SEN0401 course repository embeds
   `mastering_bitcoin_3e_ch01_v1_1_0.ttl` in its chapter 1 interactive page and pins its sha256 in
   `corpus_manifest_v*.json`; any query there that names one of the six IRIs will stop matching. This session
   did not read that repository, so the count of such references is unknown to it and is named here as work for
   whoever applies the fix rather than guessed at.
5. **Add a gate that would have caught it.** A short check over the written register — no `rdfs:label`,
   `mbb:text`, `mbb:glossaryDefinition` or IRI local name may match `&(#x[0-9a-fA-F]+|[a-zA-Z]+);`, with the
   `CodeListing` passages exempt so chapter 2's payment URI, chapter 3's `&&` and chapter 12's `Params&`
   still pass — belongs beside the attribution and coverage gates. The present gates cannot see this: the attribution
   gate checks that a passage carries its text, file, line, commit, work, authors and licence, and the coverage
   gate counts rows against the inventory, so an entity inside an otherwise complete and correctly attributed
   passage passes both.

## 5. Checked and found clean, so it need not be re-checked

- **`automate-python-book-3e`** (the SEN0414 textbook ontology, package 0.20.0): **0 occurrences** of
  `&#x` in any of its ontology files. Its source is HTML-derived rather than AsciiDoc-index-derived, so the
  path that produces this defect does not exist there.
- **`automate-python-book`** (the first-edition package, 0.67.0): **0 occurrences**.
- The remaining 17 files of `mastering-bitcoin-3e`'s `01-ontologies/`, listed in section 2 as clean.

## 6. What this session could not verify

- Whether any artifact outside the monorepo already depends on the six affected IRIs. The SEN0401 repository
  was out of this session's scope by instruction and was not read.
- Whether `html.unescape` over the whole cleaned string is safe for every carried passage of the book, as
  against the narrow four-entity map. Twelve occurrences were counted in the six files this leak touches;
  the other twelve chapters' sources were not scanned.
- Whether the package's release gate and manifest tooling would need changes beyond regeneration. They were
  read for the two tools named in section 3 only.

*Filed by the SEN0414 chapter-page lineage session. No file of `mastering-bitcoin-3e`, and no handover log of
any package, was changed by this session.*
