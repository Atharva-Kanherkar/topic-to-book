#!/usr/bin/env python3
"""Splice chapter fragments into the book shell and write the contents page for them.

A 200-page book cannot be written in one pass: you write it a chapter at a time, and then the
page numbers on the contents page are wrong the moment you insert anything. This script removes
both problems. Write each chapter as its own fragment file holding one or more
<section class="page"> blocks, and let the assembler concatenate them in filename order and
generate the contents entries with page numbers counted from the assembled result.

FRAGMENT CONVENTIONS

    <section class="page" data-part="Part II · The mechanisms">   starts a contents group
    <section class="page" data-toc="Routing policies" data-toc-n="03">   a contents entry
    <section class="page" data-ch="Three · Routing policies">     groups work on the readiness page

    data-toc-n is the label in the left column: a chapter number, a letter for an appendix, or
    omit it for an unnumbered entry such as a practice sheet.

The contents page itself is a fragment containing an empty auto slot:

    <div class="toc" data-auto="true"></div>

Usage:
    python3 assemble_book.py chapters/ -o book.html
    python3 assemble_book.py chapters/ -o book.html --title "LLM Routers" --book-id llm-routers
    python3 assemble_book.py 00-front.html 01-ch1.html -o book.html --shell my-shell.html
"""

from __future__ import annotations

import argparse
import html
import pathlib
import re
import sys

BEGIN = "<!-- BEGIN:PAGES -->"
END = "<!-- END:PAGES -->"

SECTION_OPEN = re.compile(r"<section\b", re.I)
SECTION_CLOSE = re.compile(r"</section\s*>", re.I)
PAGE_OPEN = re.compile(r'<section[^>]*class="[^"]*\bpage\b[^"]*"[^>]*>', re.I)


def mask_comments(markup: str) -> str:
    """Blank out comment bodies so a <section> mentioned inside one cannot skew the scan."""
    return re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), markup, flags=re.S)


def split_pages(markup: str) -> list[str]:
    """Return each top-level <section class="page"> block, nesting-aware."""
    scan = mask_comments(markup)
    events = [(m.start(), m.end(), "open") for m in re.finditer(r"<section\b", scan)]
    events += [(m.start(), m.end(), "close") for m in re.finditer(r"</section\s*>", scan)]
    events.sort()

    blocks: list[str] = []
    depth = 0
    start = None
    is_page = False
    for s, e, kind in events:
        if kind == "open":
            if depth == 0:
                start = s
                is_page = bool(PAGE_OPEN.match(scan, s))
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                raise SystemExit(f"stray </section> at offset {s}")
            if depth == 0 and start is not None:
                if is_page:
                    blocks.append(markup[start:e])
                start = None
    if depth:
        raise SystemExit("unclosed <section> in fragment")
    return blocks


def attr(tag: str, name: str) -> str | None:
    m = re.search(rf'{name}="([^"]*)"', tag)
    return m.group(1) if m else None


def slug(text: str) -> str:
    plain = re.sub(r"&[a-z]+;|&#\d+;", " ", text)
    plain = re.sub(r"<[^>]+>", " ", plain)
    out = re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")
    return out[:40] or "page"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+",
                    help="a directory of fragments, or the fragment files in order")
    ap.add_argument("-o", "--out", required=True, help="output HTML path")
    ap.add_argument("--shell", default=None,
                    help="path to book-shell.html (default: ../assets/book-shell.html)")
    ap.add_argument("--title", default=None, help="replace the <title>")
    ap.add_argument("--book-id", default=None,
                    help="data-book-id on .book; namespaces saved progress per book")
    args = ap.parse_args()

    here = pathlib.Path(__file__).resolve().parent
    shell_path = pathlib.Path(args.shell) if args.shell else here.parent / "assets" / "book-shell.html"
    if not shell_path.exists():
        sys.exit(f"no shell at {shell_path}")
    shell = shell_path.read_text(encoding="utf-8")
    if BEGIN not in shell or END not in shell:
        sys.exit(f"shell is missing the {BEGIN} / {END} markers")

    # gather fragments
    files: list[pathlib.Path] = []
    for s in args.sources:
        p = pathlib.Path(s)
        if p.is_dir():
            files.extend(sorted(x for x in p.iterdir()
                                if x.suffix.lower() in (".html", ".htm") and not x.name.startswith("_")))
        elif p.exists():
            files.append(p)
        else:
            sys.exit(f"no such fragment: {p}")
    if not files:
        sys.exit("no fragment files found")

    pages: list[tuple[str, pathlib.Path]] = []
    for f in files:
        found = split_pages(f.read_text(encoding="utf-8"))
        if not found:
            print(f"  ! {f.name} contains no <section class=\"page\">, skipped")
            continue
        pages.extend((blk, f) for blk in found)
    if not pages:
        sys.exit('no <section class="page"> blocks found in the supplied fragments')

    # give every contents-bound page an id, then number the pages
    entries: list[dict] = []
    rebuilt: list[str] = []
    seen_ids: set[str] = set()
    for i, (blk, src) in enumerate(pages, start=1):
        open_tag = PAGE_OPEN.search(blk).group(0)
        toc = attr(open_tag, "data-toc")
        part = attr(open_tag, "data-part")
        pid = attr(open_tag, "id")
        if (toc or part) and not pid:
            base = slug(toc or part or "")
            pid = f"p-{base}"
            n = 2
            while pid in seen_ids:
                pid = f"p-{base}-{n}"
                n += 1
            blk = blk.replace(open_tag, open_tag[:-1] + f' id="{pid}">', 1)
        if pid:
            if pid in seen_ids:
                sys.exit(f"duplicate page id {pid!r} (fragment {src.name}); ids must be unique")
            seen_ids.add(pid)
        if part:
            entries.append({"kind": "part", "label": part})
        if toc:
            entries.append({"kind": "entry", "label": toc, "n": attr(open_tag, "data-toc-n") or "",
                            "id": pid, "page": i})
        rebuilt.append(blk)

    # build the contents markup
    toc_lines: list[str] = []
    for e in entries:
        if e["kind"] == "part":
            toc_lines.append(f'        <p class="grp">{e["label"]}</p>')
        else:
            num = e["n"] or "&nbsp;&nbsp;"
            toc_lines.append(
                f'        <a href="#{e["id"]}"><span class="n">{num}</span>'
                f'<span>{e["label"]}</span><span class="dots"></span>'
                f'<span class="pg">{e["page"]:02d}</span></a>'
            )
    toc_html = "\n".join(toc_lines)

    body = "\n\n".join(rebuilt)

    filled = 0

    def fill(m: re.Match) -> str:
        nonlocal filled
        filled += 1
        return m.group(1) + "\n" + toc_html + "\n      " + m.group(3)

    body = re.sub(r'(<div class="toc[^"]*" data-auto="true"\s*>)(.*?)(</div>)', fill, body, flags=re.S)
    if entries and not filled:
        print('  ! no <div class="toc" data-auto="true"></div> found: the contents page was not '
              "written. Add the slot to your contents fragment.")

    out_html = shell[: shell.index(BEGIN) + len(BEGIN)] + "\n\n" + body + "\n\n" + shell[shell.index(END):]

    if args.title:
        out_html = re.sub(r"<title>.*?</title>", f"<title>{html.escape(args.title)}</title>",
                          out_html, count=1, flags=re.S)
    if args.book_id:
        book_id = html.escape(args.book_id, quote=True)
        out_html = re.sub(r'(<div class="book" id="book" data-book-id=")[^"]*(")',
                          lambda m: m.group(1) + book_id + m.group(2), out_html, count=1)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(out_html, encoding="utf-8")

    questions = len(re.findall(r'<li class="q"', body))
    drills = len(re.findall(r'<div class="fr"', body))
    cards = len(re.findall(r'<li class="card"', body))
    figures = len(re.findall(r"<svg\b", body))
    print(f"  {out}")
    print(f"  {len(files)} fragment(s) -> {len(rebuilt)} pages · {len(entries)} contents entries")
    print(f"  {figures} figures · {questions} graded questions · {drills} open drills · {cards} cards")
    print(f"  {out.stat().st_size // 1024} KB")
    print("\n  Next: python3 validate_book.py " + str(out))


if __name__ == "__main__":
    main()
