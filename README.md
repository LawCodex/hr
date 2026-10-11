# Croatia — legislation as Markdown (LawCodex)

Legislation of the **Republic of Croatia** (Republika Hrvatska) as plain Markdown, generated
from the official gazette **Narodne novine** (NN), https://narodne-novine.nn.hr — published by
Narodne novine d.d. on behalf of the Republic. Language: Croatian (`hr`), the only official
language.

Part of [LawCodex](https://github.com/LawCodex): one repository per jurisdiction.

## What is covered

| Directory | Content | Files |
|---|---|---|
| `ustav/` | Ustav Republike Hrvatske (Constitution) — official consolidated text NN 85/2010 + the 2013 referendum amendment (NN 5/2014) | 1 |
| `zakoni/<year>/` | Zakoni (Acts of the Croatian Parliament), incl. ustavni zakoni (constitutional acts) and codes (Kazneni zakon, Pomorski zakonik …) | 977 |
| `uredbe/<year>/` | Uredbe (Government decrees), incl. uredbe na temelju zakonske ovlasti / sa zakonskom snagom | 1,108 |

`<year>` is the year of the original publication in Narodne novine. File names are
`<year>-<NN issue>-<NN document no.>-<slug of title>.md`, e.g.
`zakoni/2014/2014-093-1872-zakon-o-radu.md` = *Zakon o radu*, NN 93/2014, document 1872.

Status breakdown (front matter `status`): zakoni — 669 `in_force`, 308 `unknown`; uredbe — 457 `in_force`, 651 `unknown`; Ustav `in_force`.

### How "in force" was determined (important)

Narodne novine does **not** publish an official list of acts in force, nor machine-readable
amendment/repeal relations (its ELI metadata has no `changes`/`repeals` links). The set of acts
here is therefore **derived automatically** from the whole official part of the gazette
1990–2026:

1. Every act (zakon / uredba) published in NN since 1990 is classified by its title as an
   original act, an amendment (*Zakon o izmjenama i dopunama Zakona o …*), a correction
   (*Ispravak …*), a repeal act (*Zakon o prestanku važenja …*) or an official consolidated
   text (*… (pročišćeni tekst)*). Amendments are linked to their act through the genitive form
   of the title.
2. An act is **dropped** when (a) a later act with the same title was published (replacement),
   (b) a *Zakon/Uredba o prestanku važenja* names it, (c) the text of a later act contains a
   repeal clause naming it with its NN citation (*„Danom stupanja na snagu ovoga Zakona prestaje
   važiti Zakon o … (»Narodne novine«, br. 12/01, …)“*), or (d) its title is limited to a past
   year (*… za 2019. godinu*, budget-execution acts, etc.).
3. The remaining acts are kept. `status: in_force` is given to those enacted, amended or
   consolidated in 2010 or later; older acts with no later activity get `status: unknown`
   (many of them are obsolete or implicitly repealed, but no explicit repeal was found).
   The reasoning is recorded in each file's `status_basis`.

Excluded by these rules: 2,300 acts (zakoni: 443 replaced by a later act with the same title, 294 repealed, 62 expired; uredbe: 880 replaced, 471 repealed, 150 expired). This is a best-effort heuristic: some repealed acts may
remain (e.g. repealed by a differently worded clause or by a Constitutional Court decision) and,
rarely, an act may have been dropped wrongly. Always verify against the official gazette.

### Text versions — consolidated vs. original + amendments

Narodne novine only occasionally publishes official consolidated texts (*pročišćeni tekst*,
established by the parliamentary Legislation Committee). For each act:

- if NN published a *pročišćeni tekst* after the act, the **latest official consolidated text**
  is the main text (`text_version: official_consolidated`);
- otherwise the main text is the **original act as published** (`text_version: original` or
  `original_with_amendments`);
- the **full text of every amendment and correction published after that main text** is
  appended at the end of the file, under *Izmjene, dopune i ispravci …*, in chronological order.
  The amendments are **not** merged into the article text.

The front matter lists all NN references (`narodne_novine`, `amendments`) in the usual Croatian
citation form. Counts: zakoni — 34 official consolidated texts, 469 files with appended later amendments, 491 original text only (never amended in NN since publication); uredbe — 222 with appended amendments, 886 original only; the Constitution uses the official consolidated text NN 85/2010 + NN 5/2014.

No unofficial consolidations are used. The obvious free source of unofficial consolidated texts,
**zakon.hr** (Val savjetovanje d.o.o.), was checked: its robots.txt allows crawling but its
terms of use (*Opći uvjeti korištenja*, §17–18) explicitly prohibit robots, scrapers, systematic
extraction and re-publication of the database and claim the sui-generis database right, so it was
**not** used.

## What is NOT covered

- **Pravilnici** (ministerial rulebooks, ~12,000 documents incl. amendments), **odluke**,
  **naredbe**, **naputci**, collective agreements and other secondary acts — skipped for volume
  (the NN server answers in ~4–6 s per request; the zakoni + uredbe crawl of ~9,250 documents took ~2.5 h at the
  allowed rate).
- **International treaties** (*Međunarodni ugovori* part of NN, incl. *Zakon o potvrđivanju …*
  ratification acts) and **Constitutional Court decisions** (except the 2013 constitutional
  amendment), official notices (*oglasni dio*).
- **Acts published before 1990** (SR Hrvatska / SFRJ legislation taken over as Croatian law):
  NN online starts in 1990. Amendments published after 1990 to such older acts cannot be
  attached to a base text (647 amendment/repeal documents could not be matched to an
  act in the corpus, mostly for that reason or because the act was renamed by amendment).
- A few acts are published in NN only as PDF (e.g. the 2024 salary-grade decrees); their text
  was machine-extracted from the official PDF with `pdftotext` (tables not preserved, marked in
  the file). One 1990 act has no text online at all and only links to the source.
- Annex graphics/forms are linked to the images hosted by Narodne novine, not copied.

## Format

Each file has YAML front matter (`title`, `identifier` = NN issue/year and document number,
`eli`, `type` = constitution | constitutional_act | code | act | decree, `date` = date of the NN
issue of the original act, `last_amended` = date of the NN issue of the latest
amendment/consolidation, `status`, `status_basis`, `text_version`, `narodne_novine`,
`amendments`, `source`, `retrieved`), then the text: promulgation decision as published,
then the act with its parts/chapters (*dio*, *glava*, roman/arabic sections) as headings and
each article (*Članak*) as the deepest heading. Article captions are in italics. Tables are
Markdown tables, or HTML when they have merged cells.

## Sources

- Narodne novine, službeni dio (official part): https://narodne-novine.nn.hr — HTML of each act
  via its ELI URI `https://narodne-novine.nn.hr/eli/sluzbeni/<year>/<issue>/<number>`.
- Yearly document index (*Kazalo*, CSV): `https://narodne-novine.nn.hr/get_index_file.aspx?year=<year>&type=csv`
  (see https://narodne-novine.nn.hr/data_access_hr.aspx).

Retrieved: 2026-10-12 (Narodne novine up to issue 115/2026).

## Licence / copyright

Under Article 18(3) of the Croatian Copyright and Related Rights Act (*Zakon o autorskom pravu
i srodnim pravima*, NN 111/2021, included in this repository) official texts in the field of
legislation, administration and the judiciary — laws, decrees, decisions etc. — cease to be
protected by copyright once they are published for the official information of the public. The
general copyright notice on the Narodne novine website covers the site's own content, not the
legislation itself. The Markdown conversion and the scripts in this repository are released
into the public domain (CC0).

This is not an official publication. Only the texts published in Narodne novine are authentic.

## Regenerate

```sh
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/hr_fetch.py     # index + HTML cache in ../_raw/hr (HR_RAW to override)
.venv/bin/python scripts/hr_convert.py   # rewrites ustav/, zakoni/, uredbe/
```

`hr_fetch.py` keeps ≤ 4 connections and ≤ 2.5 requests/s (Narodne novine asks automated
clients for at most 3 requests/s; robots.txt has no Crawl-delay) and only downloads documents
not yet cached.
