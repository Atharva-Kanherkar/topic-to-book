#!/usr/bin/env python3
"""Pre-publish structural checks for a topic-to-book HTML artifact.

These catch the mistakes that are invisible while writing and obvious to a reader: a contents
page whose numbers drifted, a question whose correct answer is not among its options, a chapter
that never got its practice sheet, a placeholder that survived into the shipped file.

Usage:
    python3 validate_book.py path/to/book.html
    python3 validate_book.py path/to/book.html --max-chars 4200 --min-pages 50

Exit status is 1 if any hard check fails, so it can gate a publish step.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from collections import Counter
from html.parser import HTMLParser

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param",
    "source", "track", "wbr",
    "path", "rect", "line", "circle", "ellipse", "polyline", "polygon", "use", "stop",
    "image", "animate",
}


class Balance(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in VOID:
            return
        self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag: str, attrs) -> None:
        return

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at line {self.getpos()[0]}")
            return
        if self.stack[-1][0] != tag:
            open_tag, open_line = self.stack[-1]
            self.errors.append(
                f"</{tag}> at line {self.getpos()[0]} closes <{open_tag}> opened at line {open_line}"
            )
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    return
            return
        self.stack.pop()


def is_greyscale(hex_colour: str) -> bool:
    r = int(hex_colour[1:3], 16)
    g = int(hex_colour[3:5], 16)
    b = int(hex_colour[5:7], 16)
    return r == g == b


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--max-chars", type=int, default=4500,
                    help="warn when a page's visible text exceeds this (default 4500)")
    ap.add_argument("--min-pages", type=int, default=40,
                    help="warn below this page count (default 40)")
    ap.add_argument("--allow-colour", action="store_true",
                    help="skip the greyscale check")
    args = ap.parse_args()

    path = pathlib.Path(args.path)
    if not path.exists():
        sys.exit(f"no such file: {path}")
    raw = path.read_text(encoding="utf-8")

    # Analyse with comments removed: a shell documents its own page types inside comments, and
    # counting those as real content produces confident nonsense.
    text = re.sub(r"<!--.*?-->", "", raw, flags=re.S)

    hard: list[str] = []
    soft: list[str] = []
    notes: list[str] = []

    # --- tag balance (on the real source, so a comment cannot hide an unclosed tag) ---
    parser = Balance()
    parser.feed(raw)
    hard.extend(parser.errors)
    if parser.stack:
        hard.append("unclosed at EOF: " + ", ".join(f"<{t}> line {ln}" for t, ln in parser.stack))

    # --- pages ---
    page_tags = re.findall(r'<section[^>]*class="page[^"]*"[^>]*>', text)
    ids = [re.search(r'id="([^"]+)"', t).group(1) if 'id="' in t else None for t in page_tags]
    notes.append(f"pages: {len(page_tags)}")
    if len(page_tags) < args.min_pages:
        soft.append(f"{len(page_tags)} pages: below the {args.min_pages} this kind of book "
                    "usually needs. Thin coverage reads as a summary, not a book")
    dupe_ids = [i for i, n in Counter([i for i in ids if i]).items() if n > 1]
    if dupe_ids:
        hard.append("duplicate page id(s): " + ", ".join(dupe_ids) +
                    " — contents links and jumps will land on the wrong page")

    # --- placeholders that must not ship ---
    for needle in ("REPLACE:", "REPLACE-topic-slug", "Chapter title", "Topic name",
                   "TODO", "Lorem ipsum"):
        if needle in text:
            (hard if needle.startswith("REPLACE") else soft).append(
                f"placeholder text still present: {needle!r}")

    # --- no mermaid ---
    # Match usage, not the word: a book may legitimately explain why it avoids Mermaid.
    mermaid = [p for p in (
        r'class\s*=\s*["\'][^"\']*\bmermaid\b',
        r"```\s*mermaid",
        r"\bmermaid\s*\.\s*(initialize|run|render)",
        r"<script[^>]+mermaid",
    ) if re.search(p, text, re.I)]
    if mermaid:
        hard.append(f"Mermaid usage found ({len(mermaid)} pattern(s)): figures must be "
                    "hand-authored SVG")

    # --- figures ---
    svgs = re.findall(r"<svg\b[^>]*>", text)
    labelled = [s for s in svgs if "aria-label=" in s]
    notes.append(f"svg figures: {len(svgs)} ({len(labelled)} with aria-label)")
    if svgs and len(labelled) < len(svgs):
        soft.append(f"{len(svgs) - len(labelled)} svg figure(s) missing aria-label")
    if len(svgs) < max(4, len(page_tags) // 12):
        soft.append(f"only {len(svgs)} figures across {len(page_tags)} pages: a topic book "
                    "carries its argument in diagrams the reader will redraw")
    if svgs and not re.search(r"viewBox", text):
        soft.append("no viewBox on any svg; figures will not scale")

    # --- greyscale ---
    if not args.allow_colour:
        hexes = sorted(set(re.findall(r"#[0-9a-fA-F]{6}\b", text)))
        coloured = [h for h in hexes if not is_greyscale(h)]
        if coloured:
            hard.append("non-greyscale colours: " + ", ".join(coloured))
        else:
            notes.append(f"palette: {len(hexes)} colours, all greyscale")
        loud = re.findall(r"\b(?:rgb|hsl)a?\([^)]*\)", text)
        if loud:
            soft.append(f"{len(loud)} rgb()/hsl() value(s): check they are greyscale too")

    # --- contents page vs actual page order ---
    folio = {pid: i + 1 for i, pid in enumerate(ids) if pid}
    if re.search(r'<div class="toc[^"]*" data-auto="true"\s*>\s*</div>', text):
        hard.append('the contents page still has an empty data-auto slot: run assemble_book.py, '
                    "or write the entries by hand")
    claims = re.findall(r'href="#([\w-]+)"[^>]*>.*?class="pg">\s*(\d+)\s*<', text, re.S)
    if claims:
        bad = [(pid, c, folio.get(pid)) for pid, c in claims if folio.get(pid) != int(c)]
        for pid, claimed, actual in bad:
            hard.append(f"contents says page {claimed} for #{pid} but it is page {actual}")
        if not bad:
            notes.append(f"contents: {len(claims)} entries, all page numbers correct")
        missing = [pid for pid, _ in claims if pid not in folio]
        if missing:
            hard.append("contents links to unknown page id(s): " + ", ".join(missing))
    else:
        soft.append("no contents entries with page numbers found: does the book have a TOC?")

    # --- chapters and their practice sheets ---
    # Every chapter should end in work the reader does. A chapter with no graded question and no
    # open drill is the failure mode this whole format exists to prevent.
    page_blocks = re.findall(r'<section[^>]*class="page.*?</section>', text, re.S)
    chapters: dict[str, dict[str, int]] = {}
    for block in page_blocks:
        m = re.search(r'data-ch="([^"]+)"', block)
        if not m:
            continue
        ch = chapters.setdefault(m.group(1), {"pages": 0, "q": 0, "fr": 0})
        ch["pages"] += 1
        ch["q"] += len(re.findall(r'<li class="q"', block))
        ch["fr"] += len(re.findall(r'<div class="fr"', block))
    notes.append(f"chapters marked with data-ch: {len(chapters)}")
    if not chapters:
        soft.append('no data-ch attributes: the readiness page cannot group anything, and '
                    "practice-sheet coverage cannot be checked")
    unpracticed = [c for c, d in chapters.items() if d["q"] == 0 and d["fr"] == 0]
    if unpracticed:
        soft.append(f"{len(unpracticed)} chapter(s) with no practice at all: " +
                    ", ".join(sorted(unpracticed)[:6]) +
                    ("…" if len(unpracticed) > 6 else ""))
    thin = [c for c, d in chapters.items() if 0 < d["q"] < 3 and d["fr"] == 0]
    if thin:
        soft.append(f"{len(thin)} chapter(s) with fewer than 3 questions and no open drill: " +
                    ", ".join(sorted(thin)[:6]))

    # --- graded questions ---
    questions = re.findall(r'<li class="q"[^>]*data-answer="([^"]*)"[^>]*>(.*?)</li>', text, re.S)
    all_q_tags = re.findall(r'<li class="q"[^>]*>', text)
    notes.append(f"graded questions: {len(questions)}")
    if len(all_q_tags) != len(questions):
        hard.append(f"{len(all_q_tags) - len(questions)} question(s) missing data-answer: "
                    "they can never be graded")

    seen_names: Counter[str] = Counter()
    for i, (answer, body) in enumerate(questions, start=1):
        values = re.findall(r'<input[^>]*value="([^"]*)"', body)
        if not values:
            hard.append(f"question {i} has no radio options")
            continue
        if answer not in values:
            hard.append(f'question {i} expects answer "{answer}" but its options are {values}: '
                        "that question is unpassable")
        names = set(re.findall(r'<input[^>]*name="([^"]*)"', body))
        if len(names) != 1:
            hard.append(f"question {i} uses {len(names)} input names {sorted(names)}; options "
                        "must share one name or they will not behave as one question")
        for n in names:
            seen_names[n] += 1
        if len(values) < 3:
            soft.append(f"question {i} has only {len(values)} options: a guess is close to a "
                        "coin flip")
        if not re.search(r'class="why"', body):
            soft.append(f"question {i} has no explanation; the explanation is the teaching "
                        "moment, the score is only the prompt to read it")

    shared = [n for n, c in seen_names.items() if c > 1]
    if shared:
        hard.append("radio group name(s) reused across questions: " + ", ".join(sorted(shared)[:8]) +
                    " — answering one will unset the other")

    if questions:
        if 'id="answer-key"' not in text:
            soft.append('no <div class="key" id="answer-key"></div>: without it there is no key')
    else:
        soft.append("no graded questions at all")

    # --- open drills ---
    drills = re.findall(r'<div class="fr"[^>]*>(.*?)</div>\s*</div>', text, re.S)
    drill_tags = re.findall(r'<div class="fr"([^>]*)>', text)
    drill_ids = [re.search(r'data-id="([^"]+)"', t).group(1) for t in drill_tags
                 if 'data-id="' in t]
    notes.append(f"open drills: {len(drill_tags)}")
    if len(drill_ids) != len(drill_tags):
        hard.append(f"{len(drill_tags) - len(drill_ids)} open drill(s) without data-id: their "
                    "self-rating cannot be saved")
    dupe_drills = [i for i, n in Counter(drill_ids).items() if n > 1]
    if dupe_drills:
        hard.append("duplicate drill data-id(s): " + ", ".join(dupe_drills))
    if drill_tags:
        without_answer = sum(1 for d in drills if "<details" not in d)
        if without_answer:
            soft.append(f"{without_answer} open drill(s) with no model answer to check against")
        if 'data-rate="solid"' not in text:
            soft.append("open drills have no self-rating buttons: the readiness page will only "
                        "see the graded questions")

    # --- flashcards ---
    cards = re.findall(r'<li class="card"([^>]*)>', text)
    card_ids = [re.search(r'data-id="([^"]+)"', c).group(1) for c in cards if 'data-id="' in c]
    if cards:
        notes.append(f"flashcards: {len(cards)}")
        if len(card_ids) != len(cards):
            hard.append(f"{len(cards) - len(card_ids)} flashcard(s) without data-id")
        dupe_cards = [i for i, n in Counter(card_ids).items() if n > 1]
        if dupe_cards:
            hard.append("duplicate flashcard data-id(s): " + ", ".join(dupe_cards))

    # --- interview apparatus ---
    if not re.search(r'class="ladder"', text):
        soft.append("no follow-up ladder: the book teaches facts but not the shape of the "
                    "conversation they are asked in")
    if not re.search(r'class="dlg"', text):
        soft.append("no annotated mock round: a reader has nowhere to see a whole answer end to "
                    "end")
    if 'id="readiness"' not in text:
        soft.append('no <div class="meter" id="readiness"></div>: nothing reads back the '
                    "reader's progress")

    # --- both grounds and paging mechanics ---
    for needle, why in [
        ('data-book-theme="dark"', "no dark ground defined"),
        ('data-book-theme="light"', "no light ground defined"),
        ("prefers-color-scheme", "no OS-preference default for the theme"),
        ("scroll-snap-type", "horizontal paging needs scroll-snap-type on the container"),
        ("ArrowRight", "arrow-key navigation appears to be missing"),
        ("palette", "no jump palette: turning 100+ pages with arrows alone is unusable"),
    ]:
        if needle not in text:
            soft.append(why)

    # --- overstuffed pages ---
    for i, block in enumerate(page_blocks, start=1):
        body = re.sub(r"<(script|style)\b.*?</\1>", " ", block, flags=re.S)
        visible = re.sub(r"<[^>]+>", " ", body)
        visible = re.sub(r"\s+", " ", visible).strip()
        if len(visible) > args.max_chars:
            soft.append(f"page {i} has ~{len(visible)} chars of text; consider splitting it")

    # --- title and sources ---
    if "<title>" not in raw:
        soft.append("no <title>: the artifact will fall back to a filename")
    if not re.search(r"sources|colophon|references", text, re.I):
        soft.append("no sources page: say where the theory and the interview intelligence came "
                    "from, and when")

    # --- report ---
    print(f"\n=== {path.name} ===")
    for n in notes:
        print(f"  · {n}")
    if soft:
        print("\n  WARNINGS")
        for s in soft:
            print(f"  ~ {s}")
    if hard:
        print("\n  FAILURES")
        for h in hard:
            print(f"  x {h}")
        print(f"\n  {len(hard)} hard failure(s). Fix these before publishing.\n")
        sys.exit(1)
    print("\n  no hard failures: safe to publish\n")


if __name__ == "__main__":
    main()
