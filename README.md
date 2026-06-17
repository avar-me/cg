# Cyril Graham — *The Avâr Language* (1881)

A static website presenting Cyril Graham's *The Avâr Language*, originally published in the *Journal of the Royal Asiatic Society of Great Britain and Ireland*, New Series, Vol. 18, No. 3 (1881), pp. 215–342 (Art. XI).

The site contains:

- **Vocabulary** — Graham's English → Avâr dictionary (~930 entries, with Arabic script).
- **Alphabet** — the consonant and vowel tables Graham gives in the original.
- **Grammar** — all chapters: numerals, substantive, plural, declension and tables, adjective, pronouns, verbs, prepositions, conjunctions, interjections, conclusion. Tables include the modern Cyrillic equivalents of Graham's Latin transliterations where available.
- **About** — Graham's own Introduction and a biographical note about the author.

Live site: <https://cg.avar.me/>

## Layout

```
.
├── data/                source data (JSON), edit this and rebuild
│   ├── about/
│   ├── alphabet/
│   ├── grammar/
│   └── vocabulary/
├── build_html/          build scripts + page templates
│   ├── build_html.sh
│   ├── build_from_data.py
│   ├── build_grammar.py
│   ├── build_vocabulary.py
│   ├── embed_vocabulary.py
│   ├── config_helper.py
│   └── templates/
├── docs/                generated site, served by GitHub Pages
├── build.sh             one-shot builder
└── README.md
```

## Building

```bash
./build.sh
```

That regenerates `docs/` from `data/` and `build_html/templates/`. The build is purely client-side static HTML/CSS/JS — no server, no JS framework.

Requirements: Python 3.6+.

## Editing content

All editable text lives in `data/`. Edit any JSON file, then run `./build.sh`.

- **Vocabulary** entries: `data/vocabulary/<LETTER>.json`. Each entry has `english`, `english_full`, `type`, `avar` (Graham's Latin transliteration), `arabic`, `page`, optional `note`.
- **About / Introduction**: `data/about/introduction.json`. Sections appear in document order.
- **Alphabet**: `data/alphabet/correspondence.json` (Arabic ↔ Latin table) and `data/alphabet/content.json` (prose around the tables).
- **Grammar**: `data/grammar/<section>.json`. Each file may use either:
  - a single `content` field with plain text (`\n\n` separates paragraphs), or
  - a `sections` array with per-section `id` / `title` / `content` and/or `body` (raw HTML, for tables).
  - Optional top-level `intro` / `intro_html` and `outro` / `outro_html` for content rendered before/after the sections.

For grammar tables we use raw HTML in `body` fields with these CSS classes:
`grammar-table` (+`compact`), `latin`, `cyr`, `gloss`, `case-label`, `example`, `editor-note`.

## Deployment (GitHub Pages)

The repository is configured so GitHub Pages serves the `docs/` directory of the `main` branch. After running `./build.sh`, commit and push — Pages will publish within a minute.

## Source

The text and tables are adapted from:

- Graham, Cyril. *The Avâr Language*. Journal of the Royal Asiatic Society, 1881.
- Атаев Б.М. (ed., transl.). *Сирил Грэхем. Аварский язык с англо-аварским словарем.* Махачкала: ИЯЛИ ДНЦ РАН; АЛЕФ, 2014. Used as a reference for modern Cyrillic equivalents and editorial commentary.

## Contact

- Web: <https://cg.avar.me/>
- Email: <admin@avar.me>
