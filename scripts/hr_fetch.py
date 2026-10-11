#!/usr/bin/env python3
"""Fetch Croatian legislation from Narodne novine (https://narodne-novine.nn.hr).

Step 1: download the yearly document index (CSV, "Kazalo") for every year 1990..now.
Step 2: download the HTML of every selected document of the official part (službeni dio):
        zakoni, ustav / ustavni zakoni, pročišćeni tekstovi, uredbe (and, with --pravilnici,
        pravilnici).

Everything is cached under _raw/hr/ so re-runs only fetch what is missing.
Politeness: descriptive User-Agent, <= 4 concurrent connections, global rate limit well
below the 3 requests/second that Narodne novine asks of automated clients, retries with
exponential backoff. robots.txt has no Crawl-delay and does not disallow /eli/sluzbeni/.
"""
import argparse
import csv
import datetime as dt
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

BASE = "https://narodne-novine.nn.hr"
UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
RAW = os.environ.get("HR_RAW", os.path.join(os.path.dirname(__file__), "..", "..", "_raw", "hr"))
RAW = os.path.abspath(RAW)
IDX = os.path.join(RAW, "index")
HTML = os.path.join(RAW, "html")

TYPES_CORE = {"zakon", "ustav", "pročišćeni tekst", "uredba",
              "uredba na temelju zakonske ovlasti", "uredba sa zakonskom snagom"}
TYPES_PRAV = {"pravilnik"}

_lock = threading.Lock()
_last = [0.0]
MIN_INTERVAL = 0.4  # seconds between request starts (global) => <= 2.5 req/s

session = requests.Session()
session.headers["User-Agent"] = UA


def throttle():
    with _lock:
        now = time.monotonic()
        wait = _last[0] + MIN_INTERVAL - now
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.monotonic()


def get(url, tries=6):
    delay = 5
    for i in range(tries):
        throttle()
        try:
            r = session.get(url, timeout=120)
            if r.status_code == 200:
                return r
            if r.status_code == 404:
                return r
            print(f"HTTP {r.status_code} {url}", file=sys.stderr)
        except requests.RequestException as e:
            print(f"ERR {e} {url}", file=sys.stderr)
        time.sleep(delay)
        delay *= 2
    return None


def fetch_index(refresh_current=True):
    os.makedirs(IDX, exist_ok=True)
    this_year = dt.date.today().year
    for y in range(1990, this_year + 1):
        p = os.path.join(IDX, f"k{y}.csv")
        if os.path.exists(p) and os.path.getsize(p) > 200 and not (refresh_current and y == this_year):
            continue
        r = get(f"{BASE}/get_index_file.aspx?year={y}&type=csv")
        if r is not None and r.status_code == 200:
            with open(p, "wb") as f:
                f.write(r.content)
            print("index", y, len(r.content))


def read_index():
    rows = []
    for fn in sorted(os.listdir(IDX)):
        if not fn.endswith(".csv"):
            continue
        with open(os.path.join(IDX, fn), encoding="utf-8-sig", newline="") as f:
            rd = csv.reader(f, delimiter="\t")
            header = next(rd, None)
            for r in rd:
                if len(r) < 8:
                    continue
                rows.append({
                    "izdanje": r[0].strip(), "broj": r[1].strip(), "naziv": " ".join(r[2].split()),
                    "vrsta": r[3].strip(), "podvrsta": r[4].strip(), "status": r[5].strip(),
                    "donositelj": r[6].strip(), "url": r[7].strip(),
                })
    return rows


def wanted(row, with_prav):
    v = row["vrsta"]
    t = row["naziv"].lower()
    if v in TYPES_CORE:
        return True
    if with_prav and v in TYPES_PRAV:
        return True
    # constitutional amendments are sometimes typed odluka/ostalo
    if t.startswith("promjena ustava republike hrvatske") or t.startswith("ustav republike hrvatske"):
        return True
    if t.startswith("ustavni zakon"):
        return True
    return False


def html_path(row):
    # url: https://narodne-novine.nn.hr/eli/sluzbeni/<year>/<issue>/<num>
    parts = row["url"].rstrip("/").split("/")
    year, issue, num = parts[-3], parts[-2], parts[-1]
    return os.path.join(HTML, year, f"{year}_{int(issue):03d}_{num}.html")


def fetch_doc(row):
    p = html_path(row)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return "cached"
    r = get(row["url"])
    if r is None:
        return "fail"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if r.status_code == 404:
        open(p + ".404", "w").close()
        return "404"
    tmp = p + ".part"
    with open(tmp, "wb") as f:
        f.write(r.content)
    os.replace(tmp, p)
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pravilnici", action="store_true", help="also fetch pravilnici")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-index", action="store_true")
    a = ap.parse_args()
    if not a.no_index:
        fetch_index()
    rows = [r for r in read_index() if wanted(r, a.pravilnici) and "/eli/sluzbeni/" in r["url"]]
    todo = [r for r in rows if not os.path.exists(html_path(r)) and not os.path.exists(html_path(r) + ".404")]
    print(f"selected {len(rows)} documents, {len(todo)} to fetch", flush=True)
    stats = {}
    with ThreadPoolExecutor(max_workers=min(4, a.workers)) as ex:
        futs = {ex.submit(fetch_doc, r): r for r in todo}
        for i, f in enumerate(as_completed(futs), 1):
            s = f.result()
            stats[s] = stats.get(s, 0) + 1
            if i % 100 == 0:
                print(i, stats, flush=True)
    print("done", stats, flush=True)


if __name__ == "__main__":
    main()
