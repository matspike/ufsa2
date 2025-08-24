from __future__ import annotations

import re
from html import unescape
from pathlib import Path


def _extract_with_regex(html_text: str) -> list[list[str]]:
    """Very small HTML table extractor using regex as a fallback.

    Not a general-purpose HTML parser, but sufficient for simple tables in tests.
    """
    rows: list[list[str]] = []
    # Find the first <table>...</table>
    m = re.search(r"<table\b[^>]*>(.*?)</table>", html_text, re.I | re.S)
    if not m:
        return rows
    table_html = m.group(1)
    # Find each row
    for tr in re.finditer(r"<tr\b[^>]*>(.*?)</tr>", table_html, re.I | re.S):
        tr_html = tr.group(1)
        cells = []
        for cell in re.finditer(
            r"<(?:th|td)\b[^>]*>(.*?)</(?:th|td)>", tr_html, re.I | re.S
        ):
            raw = cell.group(1)
            # Strip any nested tags naively
            text = re.sub(r"<[^>]+>", "", raw)
            text = unescape(text).strip()
            if text:
                cells.append(text)
        if cells:
            rows.append(cells)
    return rows


def extract_table_rows(html_path: Path) -> list[list[str]]:
    html_text = html_path.read_text(encoding="utf-8")
    try:
        from bs4 import BeautifulSoup  # type: ignore[import]
    except Exception:  # pragma: no cover
        return _extract_with_regex(html_text)
    soup = BeautifulSoup(html_text, "html.parser")
    rows: list[list[str]] = []
    table = soup.find("table")
    if not table:
        return rows
    for tr in table.find_all("tr"):
        cols = [c.get_text(strip=True) for c in tr.find_all(["th", "td"])]
        if cols:
            rows.append(cols)
    return rows
