#!/usr/bin/env python3
"""Detect text-label overlaps in the Sankey SVG.

Usage:
    python tests/check_sankey_overlaps.py [URL]

Exits 0 when no overlaps are found, 1 when overlaps are detected.

Approach
--------
1. Fetch the dashboard HTML.
2. Extract the Sankey <svg> element (identified by aria-label).
3. Parse every <text> element and estimate its axis-aligned bounding box:
       x1 = anchor_x  (text-anchor: start|end|middle → adjust x)
       y1 = y - h/2   (dominant-baseline: middle)
       x2 = x1 + estimated_width
       y2 = y1 + h
   char_width ≈ font_size × 0.58  (conservative monospace-ish estimate)
4. Report any pairs whose bounding boxes intersect.
"""

import re
import sys
import urllib.request
import urllib.error

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
CHAR_WIDTH_RATIO = 0.58   # px per pt of font-size per character
LINE_HEIGHT_RATIO = 1.25  # bounding-box height = font_size × this
PADDING = 2               # extra px to shrink boxes slightly (reduce false positives)


def fetch(url: str) -> str:
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return r.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"SKIP: could not reach {url}: {e}")
        sys.exit(0)


def extract_sankey_svg(html: str) -> str:
    m = re.search(r'(<svg[^>]*aria-label="Cash flow sankey".*?</svg>)', html, re.DOTALL)
    if not m:
        print("SKIP: Sankey SVG not found in page (no data yet?)")
        sys.exit(0)
    return m.group(1)


def parse_texts(svg: str) -> list[dict]:
    """Return list of approximate bounding boxes for every <text> in the SVG."""
    results = []
    pattern = re.compile(
        r'<text([^>]*)>(.*?)</text>', re.DOTALL | re.IGNORECASE
    )
    attr_re = {
        'x':         re.compile(r'\bx="([^"]+)"'),
        'y':         re.compile(r'\by="([^"]+)"'),
        'fs':        re.compile(r'font-size="([^"]+)"'),
        'anchor':    re.compile(r'text-anchor="([^"]+)"'),
        'baseline':  re.compile(r'dominant-baseline="([^"]+)"'),
    }

    for m in pattern.finditer(svg):
        attrs_str, raw_text = m.group(1), m.group(2)
        text = re.sub(r'<[^>]+>', '', raw_text).strip()
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&nbsp;', ' ', text)
        if not text:
            continue

        def ga(key):
            r = attr_re[key].search(attrs_str)
            return r.group(1) if r else None

        try:
            x  = float(ga('x') or 0)
            y  = float(ga('y') or 0)
            fs = float(ga('fs') or 11)
        except ValueError:
            continue

        anchor   = ga('anchor') or 'start'
        baseline = ga('baseline') or 'auto'

        w = len(text) * fs * CHAR_WIDTH_RATIO
        h = fs * LINE_HEIGHT_RATIO

        # Horizontal origin
        if anchor == 'end':
            x1 = x - w
        elif anchor == 'middle':
            x1 = x - w / 2
        else:
            x1 = x

        # Vertical origin
        if baseline == 'middle':
            y1 = y - h / 2
        else:
            y1 = y - h   # approximate for 'auto' (ascender above y)

        results.append({
            'text': text,
            'x1': x1 + PADDING, 'y1': y1 + PADDING,
            'x2': x1 + w - PADDING, 'y2': y1 + h - PADDING,
        })

    return results


def overlaps(a: dict, b: dict) -> bool:
    return (a['x1'] < b['x2'] and a['x2'] > b['x1'] and
            a['y1'] < b['y2'] and a['y2'] > b['y1'])


def main():
    html = fetch(URL)
    svg  = extract_sankey_svg(html)
    boxes = parse_texts(svg)

    hits: list[tuple[str, str]] = []
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if overlaps(a, b):
                hits.append((a['text'], b['text']))

    if hits:
        print(f"FAIL  Sankey text overlaps detected ({len(hits)} pair(s)):")
        for t1, t2 in hits:
            print(f"  ✗  \"{t1}\"  ⟷  \"{t2}\"")
        sys.exit(1)
    else:
        print(f"PASS  No Sankey text overlaps ({len(boxes)} labels checked)")


if __name__ == "__main__":
    main()
