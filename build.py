#!/usr/bin/env python3
"""
World2Vision static-site builder.

Wraps each chapter body fragment (chapters/_bodies/<stem>.html) in the shared
shell — sidebar table of contents, mobile drawer, reading-progress rail,
prev/next nav — and writes the final pages. The landing page is built from
chapters/_bodies/index.html.

No dependencies. Run:  python3 build.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
BODIES = ROOT / "chapters" / "_bodies"
OUT_CHAP = ROOT / "chapters"

# ---- the book map --------------------------------------------------------
# (id, filename-stem, part-heading-or-None, short-title, sidebar-label)
CHAPTERS = [
    ("preface", "00-preface", "Front matter", "Preface", "Preface — how to read this"),
    ("problem", "01-the-problem", "I · The problem & the shape",
        "Seeing Small Things in a Big Sky", "Seeing small things in a big sky"),
    ("system", "02-the-system", None,
        "The Shape of the System", "The shape of the system"),
    ("worlds", "03-synthetic-worlds", "II · Manufacturing truth",
        "Building Worlds", "Building worlds: synthetic data"),
    ("labels", "04-labels-from-geometry", None,
        "Truth From Geometry", "Truth from geometry: labeling"),
    ("datasets", "05-datasets", None,
        "Datasets That Don't Lie", "Datasets that don't lie"),
    ("detectors", "06-detectors", "III · Learning to see",
        "The Detectors", "The detectors"),
    ("sim2real", "07-sim-to-real", None,
        "The Sim-to-Real Gap", "The sim-to-real gap"),
    ("tiling", "08-tiny-objects", None,
        "Tiny Objects & Tiling", "Tiny objects and tiling"),
    ("evaluation", "09-evaluation", "IV · Judgment & the loop",
        "Measuring What Matters", "Measuring what matters"),
    ("deployment", "10-deployment", None,
        "Off the Desktop", "Off the desktop: edge & export"),
    ("loop", "11-closing-the-loop", None,
        "Closing the Loop", "Closing the loop"),
]

SHELL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — World2Vision</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{cssroot}assets/style.css">
</head>
<body>
<div class="progress" id="progress"></div>
<div class="topbar">
  <button class="topbar__burger" id="burger" aria-label="Open navigation">☰ Contents</button>
  <span class="topbar__title">{shorttitle}</span>
</div>
<div class="scrim" id="scrim"></div>
<div class="layout">
{sidebar}
  <main class="content">
    <div class="reading prose">
{body}
{chapnav}
      <footer class="page-foot">
        World2Vision · an open field guide to airborne-object perception ·
        <a href="{cssroot}index.html">home</a>
      </footer>
    </div>
  </main>
</div>
<script src="{cssroot}assets/site.js"></script>
</body>
</html>'''


def sidebar(active_id, link_prefix, brand_href):
    items, last_part, counter = [], "__none__", 0
    for cid, stem, part, _short, side in CHAPTERS:
        if part and part != last_part:
            items.append(f'    <li class="toc__part">{part}</li>')
            last_part = part
        if cid == "preface":
            num = '<span class="n">·</span>'
        else:
            counter += 1
            num = f'<span class="n">{counter}</span>'
        cls = "active" if cid == active_id else ""
        items.append(
            f'    <li><a class="{cls}" href="{link_prefix}{stem}.html">{num}'
            f'<span>{side}</span></a></li>'
        )
    toc = "\n".join(items)
    return f'''  <aside class="sidebar" id="sidebar">
    <a class="sidebar__brand" href="{brand_href}">
      <span class="kicker">World<span aria-hidden="true">2</span>Vision</span>
      <h1>Seeing the Sky</h1>
    </a>
    <p class="sidebar__tagline">Building perception systems that find small, fast objects in the air.</p>
    <ol class="toc">
{toc}
    </ol>
  </aside>'''


def chapnav(idx):
    prev_html = next_html = ""
    if idx > 0:
        _, stem, _, short, _ = CHAPTERS[idx - 1]
        prev_html = (f'<a class="prev" href="{stem}.html"><span class="dir">‹ Previous</span>'
                     f'<span class="ttl">{short}</span></a>')
    if idx < len(CHAPTERS) - 1:
        _, stem, _, short, _ = CHAPTERS[idx + 1]
        next_html = (f'<a class="next" href="{stem}.html"><span class="dir">Next ›</span>'
                     f'<span class="ttl">{short}</span></a>')
    if not (prev_html or next_html):
        return ""
    return f'      <nav class="chapnav">{prev_html}{next_html}</nav>'


def describe(body):
    m = re.search(r'class="lede">(.*?)</p>', body, re.S)
    if not m:
        return "Building perception systems for airborne objects."
    text = re.sub(r"<[^>]+>", "", m.group(1))
    text = re.sub(r"\s+", " ", text).strip()
    return (text[:180].rsplit(" ", 1)[0] + "…").replace('"', "'")


def main():
    built = []
    for idx, (cid, stem, part, short, side) in enumerate(CHAPTERS):
        body_path = BODIES / f"{stem}.html"
        if not body_path.exists():
            print(f"  ! missing body: {body_path.name} (skipped)")
            continue
        body = body_path.read_text()
        page = SHELL.format(
            title=short, shorttitle=short, desc=describe(body), cssroot="../",
            sidebar=sidebar(cid, link_prefix="", brand_href="../index.html"),
            body=body, chapnav=chapnav(idx),
        )
        (OUT_CHAP / f"{stem}.html").write_text(page)
        built.append(stem)

    idx_body_path = BODIES / "index.html"
    if idx_body_path.exists():
        idx_body = idx_body_path.read_text()
        landing = SHELL.format(
            title="A field guide to airborne-object perception",
            shorttitle="World2Vision", desc=describe(idx_body), cssroot="",
            sidebar=sidebar("__home__", link_prefix="chapters/", brand_href="index.html"),
            body=idx_body, chapnav="",
        )
        (ROOT / "index.html").write_text(landing)
        built.append("index")

    print(f"built {len(built)} pages: {', '.join(built)}")


if __name__ == "__main__":
    main()
