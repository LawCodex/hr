#!/usr/bin/env python3
"""Convert Narodne novine HTML (cached by hr_fetch.py) into LawCodex Markdown.

Pipeline
  1. Read the yearly NN indexes (CSV) and the cached HTML of every selected document.
  2. Classify each document by its title: base act, amendment ("... o izmjenama i dopunama
     Zakona o X"), correction ("Ispravak ..."), repeal ("Zakon o prestanku važenja ..."),
     official consolidated text ("... (pročišćeni tekst)").
  3. Group by act title.  For every title only the most recent base act is a candidate for
     "in force"; earlier acts with the same title are considered superseded.
  4. Detect repeals: titles "Zakon o prestanku važenja X", and repeal clauses in the text of
     later acts ("Danom stupanja na snagu ovoga Zakona prestaje važiti Zakon o X
     (»Narodne novine«, br. 12/01, ...)").  The first NN reference identifies the act.
  5. Time-limited acts whose title names a past year ("... za 2019. godinu") are treated as
     expired.
  6. Write one Markdown file per remaining act: main text = latest official consolidated
     text (pročišćeni tekst) when NN published one after the act, otherwise the original
     act; followed by the full text of every later amendment/correction published in NN.
"""
import csv
import datetime as dt
import html as htmlmod
import json
import os
import re
import shutil
import sys
import difflib
import unicodedata
from collections import defaultdict

from bs4 import BeautifulSoup, NavigableString, Tag

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
RAW = os.path.abspath(os.environ.get("HR_RAW", os.path.join(REPO, "..", "_raw", "hr")))
IDX = os.path.join(RAW, "index")
HTMLDIR = os.path.join(RAW, "html")
BASE = "https://narodne-novine.nn.hr"
TODAY = dt.date.today()
RECENT_YEAR = 2010  # acts enacted/amended since then and not repealed => presumed in force
RETRIEVED = os.environ.get("HR_RETRIEVED", TODAY.isoformat())

# --------------------------------------------------------------------------- index


def read_index():
    rows = []
    for fn in sorted(os.listdir(IDX)):
        if not fn.endswith(".csv"):
            continue
        with open(os.path.join(IDX, fn), encoding="utf-8-sig", newline="") as f:
            rd = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            next(rd, None)
            for r in rd:
                if len(r) < 8 or "/eli/sluzbeni/" not in r[7]:
                    continue
                parts = r[7].strip().rstrip("/").split("/")
                year, issue, num = int(parts[-3]), int(parts[-2]), parts[-1]
                rows.append({
                    "year": year, "issue": issue, "num": num,
                    "title": progl_title(norm_title(r[2])), "vrsta": r[3].strip(), "status": r[5].strip(),
                    "donositelj": r[6].strip(), "url": r[7].strip(),
                    "path": os.path.join(HTMLDIR, str(year), f"{year}_{issue:03d}_{num}.html"),
                })
    return rows


PROGL_RE = re.compile(r"^(?:odluk[au]|ukaz)\s+o\s+proglašenju\s+(?P<rest>(?:\S+\s+){0,2}?(?:zakona|zakonika)\b.*)$", re.I)


def nominative(gen):
    """'Zakona o radu' -> 'Zakon o radu'; 'Kaznenog zakona' -> 'Kazneni zakon'."""
    words = gen.split(" ")
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if lw in ("zakona", "zakonika"):
            out.append(w[:-1])
            res = out + words[i + 1:]
            res[0] = res[0][0].upper() + res[0][1:]
            return " ".join(res)
        if lw.endswith(("og", "eg")):
            out.append(w[:-2] + "i")
        else:
            out.append(w)
    return gen


def progl_title(t):
    m = PROGL_RE.match(t)
    if m:
        return nominative(m.group("rest"))
    return t


def norm_title(t):
    t = t.replace(" ", " ").replace("​", "")
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+\d+$", "", t)  # stray footnote numbers at end
    t = re.sub(r"^Uredbu\s", "Uredba ", t)
    t = re.sub(r"^NN\s*\d+[A-Za-z]?/\d+\s*[-–]\s*", "", t)  # 'NN 91A/93 - Zakon ...'
    return t


def key(t):
    t = t.lower()
    t = re.sub(r"[»«„“”\"'`]", "", t)
    t = t.replace("–", "-").replace("—", "-")
    t = re.sub(r"\s*-\s*", "-", t)
    t = re.sub(r"[\s,]+", " ", t).strip(" .")
    return t


def strip_pt(t):
    return re.sub(r"\s*[-–]?\s*\(?\s*(?:pro|pre)[čc]i[šs][ćc]eni\s+tekst\s*\)?\s*\.?$", "", t, flags=re.I).strip()


# --------------------------------------------------------------------------- classification

AMEND_RE = re.compile(
    r"^(?:ustavni\s+)?(zakon|uredba|uredbu)\s+o\s+"
    r"(?:(?:izmjen\w*|dopun\w*|izmjeni|dopuni)(?:\s*(?:i|,)\s*(?:izmjen\w*|dopun\w*))*)\s+"
    r"(?P<target>.+)$", re.I)
REPEAL_RE = re.compile(r"^(zakon|uredba)\s+o\s+(?:prestanku\s+(?:važenja|važnosti)|stavljanju\s+izvan\s+snage)\s+(?P<target>.+)$", re.I)
CORR_RE = re.compile(r"^ispravak\s+(?P<target>.+)$", re.I)
PROMJENA_USTAVA_RE = re.compile(r"^promjen[ae]\s+ustava\s+republike\s+hrvatske", re.I)


def classify(row):
    t = row["title"]
    tl = t.lower()
    if row["vrsta"] == "pročišćeni tekst" or re.search(r"(pro|pre)[čc]i[šs][ćc]eni\s+tekst", tl):
        st = strip_pt(t)
        if not re.match(r"^(?:\S+\s+){0,2}?(zakon|zakonik|uredba|ustav)\b", st.lower()):
            return "other", None
        return "pt", st
    if PROMJENA_USTAVA_RE.match(t):
        return "amend", "Ustava Republike Hrvatske"
    m = CORR_RE.match(t)
    if m:
        return "corr", m.group("target")
    m = REPEAL_RE.match(t)
    if m:
        return "repeal", m.group("target")
    m = AMEND_RE.match(t)
    if m:
        return "amend", m.group("target")
    if "referendum" in tl and "ustava republike hrvatske" in tl:
        return "amend", "Ustava Republike Hrvatske"
    if tl.startswith("vjerodostojno tumačenje") or tl.startswith("odluka") or tl.startswith("rješenje"):
        return "other", None
    return "base", t


SOFT = ("c", "č", "ć", "đ", "j", "š", "ž")
HEADS = {"zakon": "zakona", "zakonik": "zakonika", "zakona": "zakona",
         "uredba": "uredbe", "ustav": "ustava", "zakonom": "zakona"}


def genitive(title):
    """Genitive of an act title: 'Kazneni zakon' -> 'Kaznenog zakona', 'Zakon o radu' ->
    'Zakona o radu', 'Uredba o X' -> 'Uredbe o X'."""
    words = title.split(" ")
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if lw in HEADS:
            g = HEADS[lw]
            out.append(g if w[0].islower() else g.capitalize())
            return " ".join(out + words[i + 1:])
        # adjective before the head noun
        if lw.endswith("i") and len(lw) > 2:
            stem = w[:-1]
            out.append(stem + ("eg" if stem.lower().endswith(SOFT) or stem.lower().endswith(("lj", "nj")) else "og"))
        elif lw.endswith("a") and len(lw) > 2:  # feminine adjective (uredba)
            out.append(w[:-1] + "e")
        else:
            out.append(w)
        if i > 3:
            break
    return title


def target_key(target):
    t = key(target)
    # drop trailing NN citation "(»Narodne novine«, br. ...)"
    t = re.sub(r"\s*\(narodne novine.*$", "", t)
    t = re.sub(r"\s*\(nn.*$", "", t)
    return t.strip()


# --------------------------------------------------------------------------- HTML parsing

BLOCK = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "table", "ul", "ol", "pre", "blockquote", "dl"}
CONTAINER = {"div", "center", "section", "article", "font", "span", "form", "body", "tbody"}

PUB_DATE_RE = re.compile(r"Datum tiskanog izdanja:</span>\s*(\d{1,2})\.(\d{1,2})\.(\d{4})")


def load(path):
    with open(path, "rb") as f:
        raw = f.read()
    return raw.decode("utf-8", errors="replace")


def pub_date(src):
    m = PUB_DATE_RE.search(src)
    if m:
        d, mo, y = map(int, m.groups())
        try:
            return dt.date(y, mo, d)
        except ValueError:
            return None
    return None


def content_root(soup):
    root = soup.select_one("div.sl-content div.doc") or soup.select_one("div.sl-content")
    return root


def pdf_links(soup):
    out = []
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if h.lower().endswith(".pdf") or "/pdf" in h.lower():
            out.append(h if h.startswith("http") else BASE + ("" if h.startswith("/") else "/") + h)
    return out


def inline_one(c):
    if isinstance(c, NavigableString):
        if c.__class__.__name__ in ("Comment", "Declaration", "ProcessingInstruction", "Doctype"):
            return ""
        return str(c).replace("\r", "").replace("\n", " ")
    if not isinstance(c, Tag):
        return ""
    n = c.name
    if n == "br":
        return "\n"
    if n in ("sup", "sub"):
        inner = inline_text(c).strip()
        return f"<{n}>{inner}</{n}>" if inner else ""
    if n == "img":
        src = c.get("src", "")
        if src:
            if not src.startswith("http"):
                src = BASE + ("" if src.startswith("/") else "/") + src
            return f"![]({src})"
        return ""
    if n in ("script", "style", "meta", "title", "head"):
        return ""
    return inline_text(c)


def inline_text(node):
    """Render inline content of node into text (br -> newline, sup/sub kept as HTML)."""
    return "".join(inline_one(c) for c in node.children)


def clean_text(s):
    s = s.replace(" ", " ").replace("\r", "").replace("​", "").replace("﻿", "")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in s.split("\n")]
    # join soft-wrapped source lines; keep explicit <br> breaks (we cannot distinguish
    # them after rendering, so collapse runs of empty lines and keep single newlines)
    out = []
    for ln in lines:
        if ln:
            out.append(ln)
    return out


def is_italic(tag):
    txt = tag.get_text(" ", strip=True)
    if not txt:
        return False
    it = "".join(x.get_text(" ", strip=True) for x in tag.find_all(["i", "em"]))
    return len(it) >= 0.9 * len(txt)


def is_bold(tag):
    txt = tag.get_text(" ", strip=True)
    if not txt:
        return False
    b = "".join(x.get_text(" ", strip=True) for x in tag.find_all(["b", "strong"]))
    return len(b) >= 0.9 * len(txt)


def blocks_of(root):
    """Yield blocks: dict(kind=p|h|table|list, text=..., cls=..., centered=bool, tag=Tag)."""
    out = []
    buf = []

    def flush(centered):
        txt = "".join(buf)
        buf.clear()
        lines = clean_text(txt)
        if lines:
            out.append({"kind": "p", "lines": lines, "cls": "", "centered": centered, "tagname": "text",
                        "italic": False, "bold": False})

    def walk(node, centered=False):
        for c in node.children:
            if isinstance(c, NavigableString):
                if c.__class__.__name__ in ("Comment", "Declaration", "ProcessingInstruction", "Doctype"):
                    continue
                buf.append(str(c).replace("\r", "").replace("\n", " "))
                continue
            if not isinstance(c, Tag):
                continue
            n = c.name
            if n in ("script", "style", "meta", "link", "hr", "input", "select", "button", "title", "head"):
                continue
            if n == "br":
                buf.append("\n")
                continue
            if n in BLOCK:
                flush(centered)
                cen = centered or (c.get("align", "").lower() == "center") or "sred" in " ".join(c.get("class", []))
                if n == "table":
                    out.append({"kind": "table", "tag": c})
                elif n in ("ul", "ol"):
                    items = []
                    for li in c.find_all("li", recursive=False):
                        lines = clean_text(inline_text(li))
                        if lines:
                            items.append(" ".join(lines))
                    if items:
                        out.append({"kind": "list", "items": items, "ordered": n == "ol"})
                else:
                    lines = clean_text(inline_text(c))
                    if lines:
                        out.append({"kind": "p", "lines": lines, "cls": " ".join(c.get("class", [])),
                                    "centered": cen, "tagname": n, "italic": is_italic(c), "bold": is_bold(c)})
                continue
            if n in ("b", "strong", "i", "em", "u", "a", "sup", "sub", "small", "big", "img", "font", "span") and not c.find(list(BLOCK) + ["div", "center"]):
                buf.append(inline_one(c))
                continue
            # container
            flush(centered)
            cen = centered or n == "center" or c.get("align", "").lower() == "center"
            walk(c, cen)
            flush(cen)
        return

    walk(root)
    flush(False)
    return out


# --------------------------------------------------------------------------- tables


def cell_text(td):
    lines = clean_text(inline_text(td))
    return "<br>".join(lines)


def table_md(tbl):
    rows = tbl.find_all("tr")
    if not rows:
        return ""
    complex_ = any(td.get("rowspan", "1") not in ("1", "") or td.get("colspan", "1") not in ("1", "")
                   for td in tbl.find_all(["td", "th"]))
    nested = tbl.find("table") is not None
    if complex_ or nested:
        return table_html(tbl)
    grid = []
    for tr in rows:
        cells = [cell_text(td).replace("|", "\\|") for td in tr.find_all(["td", "th"], recursive=False)]
        if cells:
            grid.append(cells)
    if not grid:
        return ""
    w = max(len(r) for r in grid)
    if w == 1:
        return "\n\n".join(r[0] for r in grid if r[0])
    grid = [r + [""] * (w - len(r)) for r in grid]
    lines = ["| " + " | ".join(grid[0]) + " |", "|" + "---|" * w]
    for r in grid[1:]:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def table_html(tbl):
    def rec(node):
        if isinstance(node, NavigableString):
            return htmlmod.escape(str(node).replace(" ", " "), quote=False)
        if not isinstance(node, Tag):
            return ""
        n = node.name
        inner = "".join(rec(c) for c in node.children)
        if n in ("table", "tr", "td", "th", "thead", "tbody", "tfoot"):
            attrs = ""
            for a in ("rowspan", "colspan"):
                if node.get(a) and node.get(a) != "1":
                    attrs += f' {a}="{node.get(a)}"'
            if n == "td" or n == "th":
                inner = re.sub(r"\s+", " ", inner).strip()
            return f"<{n}{attrs}>{inner}</{n}>"
        if n == "br":
            return "<br>"
        if n in ("sup", "sub", "b", "i"):
            return f"<{n}>{inner}</{n}>"
        if n == "p":
            return inner.strip() + "<br>"
        if n == "img":
            src = node.get("src", "")
            if src and not src.startswith("http"):
                src = BASE + ("" if src.startswith("/") else "/") + src
            return f'<img src="{src}">'
        return inner
    s = rec(tbl)
    s = re.sub(r"(<br>)+</t([dh])>", r"</t\2>", s)
    s = re.sub(r"\n\s*", "\n", s)
    s = s.replace("<tr>", "\n<tr>").replace("</table>", "\n</table>")
    return s.strip()


# --------------------------------------------------------------------------- markdown

ART_RE = re.compile(r"^(?:Članak|Član|ČLANAK|ČLAN|Clanak|Čl\.)\s*\d+\s*\.?\s*(?:[a-zA-Z]{1,2}\s*\.?)?\s*(?:\(\s*\d+\s*\))?$")
KNJIGA_RE = re.compile(r"^(KNJIGA|Knjiga)\b|^\S+\s+KNJIGA\b")
DIO_RE = re.compile(r"^(?:(?:PRVI|DRUGI|TREĆI|ČETVRTI|PETI|ŠESTI|SEDMI|OSMI|DEVETI|DESETI|JEDANAESTI|DVANAESTI|TRINAESTI|ČETRNAESTI|PETNAESTI|ŠESNAESTI|SEDAMNAESTI|OSAMNAESTI|DEVETNAESTI|DVADESETI|[A-ZČĆŠŽĐ]+I)\s+DIO|DIO\s+[A-ZČĆŠŽĐ0-9IVXLC]+\b)", re.I)
GLAVA_RE = re.compile(r"^(GLAVA|Glava)\s+\S+|^[IVXLC]+\.?\s*(GLAVA|Glava)")
ROMAN_RE = re.compile(r"^[IVXLC]+\.\s*\S|^[IVXLC]+\.?$")
ODJ_RE = re.compile(r"^(\d+\.\s*\S|Odjeljak|ODJELJAK|\d+\.$)")
PODODJ_RE = re.compile(r"^(\d+\.\d+\.|Pododjeljak|PODODJELJAK|[a-zA-Z]\)\s)")
FOOT_RE = re.compile(r"^(Klasa|KLASA|Urbroj|URBROJ|Ur\.\s*broj|Ur\.broj|Broj:|BROJ:)\b")
TITLE_RE = re.compile(r"^(USTAVNI\s+ZAKON|ZAKON|ZAKONIK|UREDB[AU]|USTAV\b|PROMJEN[AU]\s+USTAVA|(?:[A-ZČĆŠŽĐ]+I\s+){1,2}ZAKON)")
LABEL_RE = re.compile(r"^(?:(?:\S+\s+)?DIO(?:\s+\S+)?|(?:\S+\s+)?GLAVA(?:\s+\S+)?(?:\s*\([IVXLC]+\.?\))?|KNJIGA(?:\s+\S+)?|[IVXLC]+\.?|\d+\.|ODJELJAK\s+\S+)$")
RANKS = ["knjiga", "dio", "glava", "roman", "odj", "pododj", "head"]


def upper_ratio(s):
    letters = [ch for ch in s if ch.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for ch in letters if ch.isupper()) / len(letters)


def esc_md(s):
    if s.startswith("#"):
        s = "\\" + s
    if re.match(r"^[*+](\s|$)", s):
        s = "\\" + s
    if re.match(r"^>", s):
        s = "\\" + s
    return s


def para(lines):
    return "  \n".join(esc_md(x) for x in lines)


def to_markdown(blocks, base_level=2):
    """Convert blocks to markdown body. base_level = level of the top division heading."""
    n = len(blocks)
    texts = [" ".join(b["lines"]) if b["kind"] == "p" else "" for b in blocks]
    first_art = next((i for i, b in enumerate(blocks) if b["kind"] == "p" and ART_RE.match(texts[i])), None)
    # body start: last title-like block before first article
    body_start = None
    lim = first_art if first_art is not None else min(n, 40)
    for i in range(lim):
        t = texts[i]
        b = blocks[i]
        if b["kind"] != "p" or not t or "PROGLAŠ" in t.upper() or not TITLE_RE.match(t.upper()):
            continue
        if upper_ratio(b["lines"][0]) > 0.8 or (len(t) < 300 and (
                b["centered"] or b["bold"] or b["tagname"] in ("h1", "h2", "h3", "h4") or len(t.split()) <= 2)):
            body_start = i
    has_title = body_start is not None
    if body_start is None:
        body_start = 0
    # classify headings
    kinds = [None] * n
    footer = False
    for i in range(n):
        b = blocks[i]
        if b["kind"] != "p":
            continue
        t = texts[i]
        if i < body_start:
            continue
        if FOOT_RE.match(t) and i > (first_art or 0):
            footer = True
            continue
        if ART_RE.match(t):
            kinds[i] = "art"
            footer = False if footer and False else footer
            continue
        if footer:
            if t.upper().startswith("PRILOG") and upper_ratio(t) > 0.6 and len(t) < 200:
                footer = False
                kinds[i] = "head"
            continue
        cls = b["cls"]
        if has_title and first_art is not None and i < first_art and (i == body_start or (i == body_start + 1 and re.match(r"^(o|za|u|od|na|kojom|kojim)\s", t, re.I))):
            kinds[i] = "title"
            continue
        if len(t) > 300:
            continue
        caption = ("kurz" in cls) or (b["italic"] and not b["centered"] and upper_ratio(t) < 0.5) or (
            b["italic"] and upper_ratio(t) < 0.5)
        headingish = ("sred" in cls or "fett" in cls or b["tagname"] in ("h1", "h2", "h3", "h4", "h5", "h6")
                      or (b["centered"] and upper_ratio(t) > 0.6) or (b["bold"] and upper_ratio(t) > 0.6))
        if caption and not ("sred" in cls or "fett" in cls):
            kinds[i] = "caption"
            continue
        if b["centered"] and not headingish and len(t) < 200 and not t.endswith((".", ":", ";", ",")):
            kinds[i] = "caption"
            continue
        if not headingish:
            continue
        if KNJIGA_RE.match(t):
            kinds[i] = "knjiga"
        elif DIO_RE.match(t):
            kinds[i] = "dio"
        elif GLAVA_RE.match(t):
            kinds[i] = "glava"
        elif ROMAN_RE.match(t):
            kinds[i] = "roman"
        elif PODODJ_RE.match(t):
            kinds[i] = "pododj"
        elif ODJ_RE.match(t):
            kinds[i] = "odj"
        elif "sred" in cls:
            kinds[i] = "glava"
        elif "fett" in cls:
            kinds[i] = "odj"
        else:
            kinds[i] = "head"
    # merge a bare division label ("GLAVA PRVA (I.)", "DRUGI DIO", "III.") with the
    # unnumbered heading line that follows it ("TEMELJNE ODREDBE")
    for i in range(n - 1):
        if kinds[i] in ("knjiga", "dio", "glava", "roman", "odj") and LABEL_RE.match(texts[i].upper()):
            j = i + 1
            if blocks[j]["kind"] == "p" and kinds[j] in ("head", "caption") and len(texts[j]) < 250:
                blocks[i] = dict(blocks[i], lines=blocks[i]["lines"] + blocks[j]["lines"])
                kinds[j] = "skip"
    present = [r for r in RANKS if r in kinds]
    level = {}
    for j, r in enumerate(present):
        level[r] = min(6, base_level + j)
    art_level = min(6, base_level + len(present))
    out = []
    for i, b in enumerate(blocks):
        k = kinds[i]
        if b["kind"] == "table":
            md = table_md(b["tag"])
            if md:
                out.append(md)
            continue
        if b["kind"] == "list":
            for j, it in enumerate(b["items"], 1):
                out.append((f"{j}. " if b["ordered"] else "- ") + it)
            continue
        t = " ".join(b["lines"])
        if k == "skip":
            continue
        if k == "art":
            out.append("#" * art_level + " " + t if art_level <= 6 else f"**{t}**")
        elif k in level:
            out.append("#" * level[k] + " " + " — ".join(b["lines"]).replace("*", "\\*"))
        elif k == "title":
            out.append("**" + " ".join(b["lines"]).replace("*", "\\*") + "**")
        elif k == "caption":
            out.append("*" + " ".join(b["lines"]).replace("*", "\\*") + "*")
        else:
            out.append(para(b["lines"]))
    return "\n\n".join(out)


def convert_doc(path, base_level=2):
    if os.path.exists(path + ".linked.html"):
        path = path + ".linked.html"
    src = load(path)
    soup = BeautifulSoup(src, "lxml")
    root = content_root(soup)
    info = {"date": pub_date(src), "pdf": [], "empty": False}
    if root is None:
        info["empty"] = True
        return "", info
    for bad in root.select("#article-details, .detailsTable, .metaTable, script, style, p.broj-d"):
        bad.decompose()
    blocks = blocks_of(root)
    md = to_markdown(blocks, base_level)
    if len(re.sub(r"\s", "", md)) < 80:
        info["empty"] = True
        info["pdf"] = pdf_links(root) or pdf_links(soup)
    return md, info


def plain_text(path):
    if os.path.exists(path + ".linked.html"):
        path = path + ".linked.html"
    src = load(path)
    soup = BeautifulSoup(src, "lxml")
    root = content_root(soup)
    if root is None:
        return ""
    return re.sub(r"\s+", " ", root.get_text(" "))


# --------------------------------------------------------------------------- slugs / ids

TRANS = str.maketrans({"č": "c", "ć": "c", "đ": "dj", "š": "s", "ž": "z",
                       "Č": "c", "Ć": "c", "Đ": "dj", "Š": "s", "Ž": "z"})


def slug(s, maxlen=80):
    s = s.translate(TRANS)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    if len(s) > maxlen:
        s = s[:maxlen].rsplit("-", 1)[0]
    return s


def nn_ref(r):
    return f"NN {r['issue']}/{r['year']}"


def ident(r):
    return f"NN {r['issue']}/{r['year']} ({r['num']})"


NNCIT_RE = re.compile(r"[»«\"„“]?\s*Narodne\s+novine\s*[»«\"„“”]?\s*,?\s*(?:br\.|broj|brojevi)?\s*:?\s*([0-9][0-9/.,\s,i\-–]*)", re.I)


def parse_nn_list(s):
    """'93/14, 127/17 i 98/19' -> [(93,2014),(127,2017),(98,2019)]"""
    out = []
    for m in re.finditer(r"(\d{1,3})\s*/\s*(\d{2,4})", s):
        n, y = int(m.group(1)), int(m.group(2))
        if y < 100:
            y += 1900 if y >= 50 else 2000
        out.append((n, y))
    return out


REPEAL_CLAUSE_RE = re.compile(
    r"(prestaj[eu]\s+(?:važiti|važenje|vrijediti|se\s+primjenjivati)|prestanku\s+važenja|stavlja(?:ju)?\s+se\s+izvan\s+snage|izvan\s+snage\s+stavlja)",
    re.I)
# nominative act name immediately followed by an NN citation
NAMED_CIT_RE = re.compile(
    r"((?:Ustavni\s+)?(?:Zakon|Uredba|[A-ZČĆŠŽĐ][a-zčćšžđ]+i\s+zakon(?:ik)?|Zakonik)\s+[^()]{0,400}?)\s*\(\s*[»«\"„“]?\s*Narodne\s+novine\s*[»«\"„“”]?\s*,?\s*(?:br\.|broj|brojevi)?\s*:?\s*([^)]{1,300})\)")


HEAD_START_RE = re.compile(r"(?:Ustavni\s+)?(?:Zakon|Uredba|Zakonik|(?:[A-ZČĆŠŽĐ][a-zčćšžđ]+i\s+)+zakon(?:ik)?)\s")


def detect_repeals(text):
    """Return list of (issue, year, name) for whole acts declared repealed in text."""
    res = []
    for sent in re.split(r"(?<=[.;])\s+(?=[A-ZČĆŠŽĐ(])|Članak\s+\d+\.", text):
        if not REPEAL_CLAUSE_RE.search(sent):
            continue
        for m in NAMED_CIT_RE.finditer(sent):
            name = m.group(1)
            # skip partial repeals: '... odredbe ... Zakona', 'članak 5. Zakona o ...'
            pre = sent[max(0, m.start() - 60):m.start()].lower()
            if re.search(r"(odredb\w*|član\w*|stav\w*|točk\w*|dio|dijel\w*|glav\w*|prilog\w*)\s*[\d\s.,a-z-]*$", pre):
                continue
            nn = parse_nn_list(m.group(2))
            if nn:
                res.append((nn[0][0], nn[0][1], name.strip()))
    return res


EXPIRED_RE = re.compile(r"(?:za|u)\s+(\d{4})\.?\s*(?:i\s+\d{4}\.?\s*)?(?:godin\w+|\.)|(\d{4})\.\s*[-–]\s*(\d{4})\.", re.I)


def expired_year(title):
    tl = title.lower()
    m = re.search(r"\b(?:za|u)\s+(?:razdoblje\s+(?:od\s+)?)?(\d{4})\.?\s*(?:(?:i|do|[-–])\s*(\d{4})\.?\s*)?godin", tl)
    if m:
        y = int(m.group(2) or m.group(1))
        return y
    m = re.search(r"\b(\d{4})\.\s*[-–]\s*(\d{4})\.", tl)
    if m:
        return int(m.group(2))
    return None


# --------------------------------------------------------------------------- main build


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def build():
    rows = [r for r in read_index() if os.path.exists(r["path"])]
    print("documents with cached HTML:", len(rows), file=sys.stderr)
    seen = set()
    docs = []
    for r in rows:
        k = (r["year"], r["issue"], r["num"])
        if k in seen:
            continue
        seen.add(k)
        r["kind"], r["target"] = classify(r)
        r["order"] = (r["year"], r["issue"], int(re.sub(r"\D", "", r["num"]) or 0))
        docs.append(r)
    docs.sort(key=lambda r: r["order"])

    # category of a document
    def cat(r):
        tl = r["title"].lower()
        if tl.startswith("ustav republike hrvatske") or "ustava republike hrvatske" in (r["target"] or "").lower() and r["kind"] != "base":
            return "ustav"
        if r["vrsta"].startswith("uredba") or tl.startswith("uredb"):
            return "uredbe"
        return "zakoni"

    bases = defaultdict(list)    # key(title) -> [rows]
    for r in docs:
        r["cat"] = cat(r)
        if r["kind"] == "base":
            bases[key(r["title"])].append(r)
    # official consolidated texts of acts that are not themselves in the online gazette
    # (e.g. pre-1990 acts) become stand-alone base documents
    for r in docs:
        if r["kind"] == "pt":
            tk = key(r["target"])
            if tk not in bases:
                r["kind"] = "base"
                r["is_pt"] = True
                r["title"] = r["target"]
                bases[tk].append(r)
    # genitive lookup
    gen = {}
    for k, lst in bases.items():
        t = lst[-1]["title"]
        gen[key(genitive(t))] = k
        gen[k] = k
    gen.setdefault(key("Ustava Republike Hrvatske"), key("Ustav Republike Hrvatske"))

    def resolve(target, kind):
        if target is None:
            return None
        tk = target_key(target)
        if kind == "pt":
            return tk if tk in bases else gen.get(tk)
        for _ in range(3):
            if tk in gen:
                return gen[tk]
            m2 = re.match(r"^(?:ustavnog\s+)?(?:zakona|uredbe)\s+o\s+(?:(?:izmjen\w*|dopun\w*)(?:\s*(?:i|,)\s*(?:izmjen\w*|dopun\w*))*)\s+(.+)$", tk)
            if not m2:
                break
            tk = m2.group(1)
        # strip trailing qualifiers like ' (»Narodne novine«...' already done; try prefix match
        for cut in (r"\s+i\s+.*$", r",.*$"):
            t2 = re.sub(cut, "", tk)
            if t2 in gen:
                return gen[t2]
        return None

    # attach amendments / corrections / PTs / repeals to the latest base before them
    unmatched = []
    for r in docs:
        if r["kind"] in ("amend", "corr", "pt", "repeal"):
            bk = resolve(r["target"], r["kind"])
            if bk is None:
                if r["kind"] != "corr" or r["target"] and re.match(r"(zakon|uredb|ustav)", r["target"], re.I):
                    unmatched.append(r)
                continue
            cands = [b for b in bases[bk] if b["order"] <= r["order"]]
            if not cands:
                cands = bases[bk][:1]
                if r["kind"] != "pt":
                    unmatched.append(r)
                    continue
            b = cands[-1]
            b.setdefault("changes", []).append(r)
    # supersession by same title
    status = {}
    for k, lst in bases.items():
        for b in lst[:-1]:
            status[id(b)] = ("superseded", lst[-1])
    # repeals by title
    for k, lst in bases.items():
        for b in lst:
            for c in b.get("changes", []):
                if c["kind"] == "repeal":
                    status[id(b)] = ("repealed", c)
    # repeals in text
    by_nn = defaultdict(list)
    for k, lst in bases.items():
        for b in lst:
            by_nn[(b["issue"], b["year"])].append(b)
    nrep = 0
    for r in docs:
        if r["kind"] not in ("base", "amend") or r["cat"] == "ustav":
            continue
        txt = plain_text(r["path"])
        if "prestaj" not in txt and "izvan snage" not in txt and "prestanku važenja" not in txt:
            continue
        for issue, year, name in detect_repeals(txt):
            for b in by_nn.get((issue, year), []):
                if b is r or b["order"] >= r["order"]:
                    continue
                # the cited name must match the base title
                starts = [mm.start() for mm in HEAD_START_RE.finditer(name)]
                nk = key(name[starts[-1]:] if starts else name)
                bk = key(b["title"])
                if nk == bk or difflib.SequenceMatcher(None, nk, bk).ratio() >= 0.96:
                    if id(b) not in status:
                        status[id(b)] = ("repealed", r)
                        nrep += 1
    print("repealed via text clauses:", nrep, file=sys.stderr)

    # write
    for d in ("ustav", "zakoni", "uredbe"):
        p = os.path.join(REPO, d)
        if os.path.isdir(p):
            shutil.rmtree(p)
    stats = defaultdict(int)
    excluded = []
    written = []
    for k, lst in bases.items():
        for b in lst:
            st = status.get(id(b))
            ey = expired_year(b["title"])
            if b["cat"] == "ustav":
                if b is not lst[-1]:
                    continue
            elif st is not None:
                excluded.append((b, st[0], st[1]))
                continue
            elif ey is not None and ey < TODAY.year:
                excluded.append((b, "expired", None))
                continue
            elif b["vrsta"] in ("uredba sa zakonskom snagom",) or (b["year"] <= 1991 and b["title"].lower().startswith("uredba") and "zakonsk" in b["vrsta"]):
                pass
            info = write_act(b)
            if info:
                written.append(info)
                stats[b["cat"]] += 1
    with open(os.path.join(RAW, "build_report.json"), "w") as f:
        json.dump({
            "written": stats,
            "excluded": [{"nn": ident(b), "title": b["title"], "cat": b["cat"], "why": why,
                          "by": (ident(o) + " " + o["title"]) if o else None} for b, why, o in excluded],
            "unmatched": [{"nn": ident(r), "title": r["title"], "kind": r["kind"]} for r in unmatched],
            "files": written,
        }, f, ensure_ascii=False, indent=1)
    print(dict(stats), "excluded", len(excluded), "unmatched", len(unmatched), file=sys.stderr)


def doc_type(b):
    tl = b["title"].lower()
    if b["cat"] == "ustav":
        return "constitution"
    if tl.startswith("ustavni zakon"):
        return "constitutional_act"
    if tl.endswith("zakonik") or " zakonik " in tl or tl.startswith("kazneni zakon") or tl.startswith("pomorski zakonik"):
        return "code"
    if b["cat"] == "uredbe":
        return "decree"
    return "act"


def write_act(b):
    changes = sorted(b.get("changes", []), key=lambda r: r["order"])
    pts = [c for c in changes if c["kind"] == "pt"]
    main = b
    consolidated = bool(b.get("is_pt"))
    if pts:
        main = pts[-1]
        consolidated = True
    later = [c for c in changes if c["kind"] in ("amend", "corr") and c["order"] > main["order"]]
    earlier = [c for c in changes if c["kind"] in ("amend", "corr") and c["order"] <= main["order"]]
    body, info = convert_doc(main["path"], 2)
    bdate = None
    try:
        bdate = convert_doc(b["path"], 2)[1]["date"] if main is not b else info["date"]
    except Exception:
        pass
    last = later[-1] if later else (main if consolidated else (earlier[-1] if earlier else b))
    ldate = None
    title = b["title"]
    if b["cat"] == "ustav":
        rel = os.path.join("ustav", "ustav-republike-hrvatske.md")
    else:
        rel = os.path.join(b["cat"], str(b["year"]),
                           f"{b['year']}-{b['issue']:03d}-{slug(b['num'], 10)}-{slug(title, 70)}.md")
    sections = []
    for c in later:
        cbody, cinfo = convert_doc(c["path"], 3)
        ldate = cinfo["date"] or ldate
        if cinfo["empty"]:
            pdfl = cinfo["pdf"][0] if cinfo["pdf"] else c["url"]
            cbody = f"*Tekst nije dostupan u HTML obliku na stranicama Narodnih novina; vidi {pdfl}*"
        sections.append(f"## {c['title']} ({nn_ref(c)})\n\n*Izvor: {c['url']}*\n\n{cbody}")
    if info["empty"]:
        pdfl = info["pdf"][0] if info["pdf"] else main["url"]
        body = f"*Tekst nije dostupan u HTML obliku na stranicama Narodnih novina; vidi {pdfl}*"
    activity = max([b["year"]] + [c["year"] for c in changes if c["kind"] in ("amend", "corr", "pt")])
    if b["cat"] == "ustav":
        status, basis = "in_force", "Constitution of the Republic of Croatia"
    elif activity >= RECENT_YEAR:
        status = "in_force"
        basis = (f"derived: enacted or amended in {activity} and no later repeal, replacement or expiry "
                 "detected in Narodne novine (not an official in-force list)")
    else:
        status = "unknown"
        basis = (f"no repeal detected in Narodne novine, but no amendment since {activity}; "
                 "may be obsolete or implicitly repealed")
    scanned = bool(re.search(r"!\[\]\(", body)) and len(re.sub(r"!\[\]\([^)]*\)|\s", "", body)) < 400
    nnlist = ", ".join(f"{r['issue']}/{str(r['year'])[2:]}" for r in [b] + [c for c in changes if c["kind"] in ("amend", "corr", "pt")])
    fm = ["---",
          f"title: {yaml_str(title)}",
          f"identifier: {yaml_str(ident(b))}",
          f"eli: {yaml_str(b['url'])}",
          f"type: {doc_type(b)}",
          "jurisdiction: hr",
          "language: hr",
          f"date: {bdate.isoformat() if bdate else str(b['year'])}",
          ]
    lastd = ldate if later else info["date"] if consolidated else None
    if not later and not consolidated and earlier:
        lastd = None
    if lastd:
        fm.append(f"last_amended: {lastd.isoformat()}")
    fm += [
        f"status: {status}",
        f"status_basis: {yaml_str(basis)}",
        f"text_version: {'official_consolidated' if consolidated else 'original_with_amendments' if later else 'original'}",
    ]
    if consolidated:
        fm.append(f"consolidated_text: {yaml_str(ident(main) + ' ' + main['url'])}")
    fm.append(f"narodne_novine: {yaml_str(nnlist)}")
    fm.append("amendments:")
    if not [c for c in changes if c["kind"] in ("amend", "corr")]:
        fm[-1] = "amendments: []"
    for c in changes:
        if c["kind"] in ("amend", "corr"):
            fm.append(f"  - {yaml_str(ident(c) + ' ' + c['title'])}")
    fm += [f"source: {yaml_str(main['url'])}", f"retrieved: {RETRIEVED}", "---", "", ""]
    head = [f"# {title}", ""]
    note = [f"> Izvor: Narodne novine, {nn_ref(b)} ({b['url']})."]
    if consolidated:
        note.append(f"> Tekst u nastavku je službeni pročišćeni tekst objavljen u {nn_ref(main)} ({main['url']}).")
    if earlier and not consolidated:
        pass
    if later:
        note.append("> Izmjene, dopune i ispravci objavljeni nakon "
                    + ("pročišćenog teksta" if consolidated else "izvornog teksta")
                    + " nisu ugrađeni u tekst; njihov cjeloviti tekst naveden je na kraju dokumenta: "
                    + ", ".join(nn_ref(c) for c in later) + ".")
    if scanned:
        note.append("> Tekst je u Narodnim novinama objavljen samo kao skenirana slika; slike su povezane s izvornika.")
    note.append("> Ovo nije službeni pročišćeni tekst osim ako je gore navedeno; status je utvrđen automatski.")
    out = "\n".join(fm) + "\n".join(head) + "\n" + "\n>\n".join(note) + "\n\n" + body.strip() + "\n"
    if sections:
        out += "\n---\n\n# Izmjene, dopune i ispravci nakon " + ("pročišćenog teksta" if consolidated else "izvornog teksta") + "\n\n" + "\n\n".join(sections).strip() + "\n"
    out = re.sub(r"\n{3,}", "\n\n", out)
    p = os.path.join(REPO, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    return {"path": rel, "title": title, "nn": ident(b), "cat": b["cat"], "consolidated": consolidated,
            "amendments_appended": len(later), "empty": info["empty"], "scanned": scanned,
            "status": status}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--one":
        md, info = convert_doc(sys.argv[2])
        print(md)
        print(info, file=sys.stderr)
    else:
        build()
