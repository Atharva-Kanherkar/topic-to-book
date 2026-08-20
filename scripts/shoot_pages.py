#!/usr/bin/env python3
"""Screenshot specific pages of a book, in either ground, using headless Chrome.

A paginated book cannot be captured by pointing a screenshotter at the file: every page lives at
the same URL and the position is JavaScript state. This script solves that by writing a temporary
copy of the book with a small bootstrap appended. The bootstrap sets the theme, jumps to the
page, and optionally opens the quiz or the jump palette, then captures that copy.

Useful for a README, a pull request description, or checking a page you cannot see in your host's
preview pane.

Usage:
    python3 shoot_pages.py book.html --out docs/screenshots
    python3 shoot_pages.py book.html --out shots --pages 1,4,12 --theme dark
    python3 shoot_pages.py book.html --out shots --pages 30 --graded    # quiz pre-graded
    python3 shoot_pages.py book.html --out shots --pages 3 --palette    # jump palette open

Requires Google Chrome, Chromium, or Edge. Note that Chrome's sandbox usually refuses to read
files under /tmp or /private/tmp, so keep the book somewhere under your home directory.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]

# Injected BEFORE the book's own script so the book paints its theme toggle in the right state.
# Setting the attribute afterwards would leave the icon showing the opposite ground.
PRELUDE = """
<script>
document.documentElement.setAttribute('data-book-theme', "__THEME__");
try { localStorage.setItem('topic-book-theme', "__THEME__"); } catch (e) {}
</script>
"""

# Runs after the book's own script, so the paging engine already exists. Sets state directly
# rather than dispatching clicks, because headless captures fire before smooth scrolling settles.
BOOTSTRAP = """
<script>
(function () {
  var PAGE = __PAGE__, GRADED = __GRADED__, PALETTE = __PALETTE__;
  var book = document.getElementById('book');
  if (book) {
    book.style.scrollBehavior = 'auto';
    book.scrollLeft = PAGE * book.clientWidth;
    book.dispatchEvent(new Event('scroll'));
  }
  if (GRADED) {
    document.querySelectorAll('form.quiz').forEach(function (f, fi) {
      // answer most questions correctly and one wrongly, so the shot shows both states
      f.querySelectorAll('li.q').forEach(function (q, i) {
        var want = q.getAttribute('data-answer');
        var inputs = q.querySelectorAll('input[type=radio]');
        var pick = null;
        inputs.forEach(function (inp) {
          if (i === 1 ? inp.value !== want : inp.value === want) { if (!pick) pick = inp; }
        });
        if (pick) pick.checked = true;
      });
      var btn = f.querySelector('[data-action="check"]');
      if (btn) btn.click();
    });
  }
  if (GRADED) {
    // press one rating per open drill so a practice-sheet shot shows the component in use
    document.querySelectorAll('.fr .rbtn[data-rate="solid"]').forEach(function (b, i) {
      if (i % 2 === 0) b.click();
    });
    document.querySelectorAll('.fr .rbtn[data-rate="shaky"]').forEach(function (b, i) {
      if (i % 2 === 1) b.click();
    });
  }
  if (PALETTE) {
    var c = document.getElementById('count');
    if (c) c.click();
  }
})();
</script>
"""


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if c.startswith("/"):
            if pathlib.Path(c).exists():
                return c
        else:
            found = shutil.which(c)
            if found:
                return found
    sys.exit("No Chrome/Chromium/Edge found. Install one, or capture the screenshots by hand.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("book", help="path to the book HTML")
    ap.add_argument("--out", required=True, help="output directory for PNGs")
    ap.add_argument("--pages", default="1",
                    help="1-based page numbers, comma separated (default 1)")
    ap.add_argument("--theme", default="dark", choices=["dark", "light"])
    ap.add_argument("--size", default="1440x900", help="viewport, WxH (default 1440x900)")
    ap.add_argument("--graded", action="store_true",
                    help="pre-answer and grade the quizzes before capturing")
    ap.add_argument("--palette", action="store_true", help="open the jump palette")
    ap.add_argument("--prefix", default="", help="filename prefix")
    args = ap.parse_args()

    book = pathlib.Path(args.book).expanduser().resolve()
    if not book.exists():
        sys.exit(f"no such file: {book}")
    out = pathlib.Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    try:
        width, height = (int(x) for x in args.size.lower().split("x"))
    except ValueError:
        sys.exit("--size must look like 1440x900")

    try:
        pages = [int(p.strip()) for p in args.pages.split(",") if p.strip()]
    except ValueError:
        sys.exit("--pages must be comma-separated integers, 1-based")

    chrome = find_chrome()
    html = book.read_text(encoding="utf-8")

    # The temp copy must sit beside the original so any relative references still resolve,
    # and because Chrome's sandbox tends to refuse files under /tmp.
    written = []
    for page in pages:
        pre = PRELUDE.replace("__THEME__", args.theme)
        boot = (
            BOOTSTRAP.replace("__PAGE__", str(max(0, page - 1)))
            .replace("__GRADED__", "true" if args.graded else "false")
            .replace("__PALETTE__", "true" if args.palette else "false")
        )
        tmp = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".html", prefix="_shot_", dir=book.parent,
                delete=False, encoding="utf-8",
            ) as fh:
                fh.write(pre + html + boot)
                tmp = pathlib.Path(fh.name)

            name = f"{args.prefix}{'' if not args.prefix else '-'}page-{page:02d}-{args.theme}"
            if args.graded:
                name += "-graded"
            if args.palette:
                name += "-palette"
            target = out / f"{name}.png"

            proc = subprocess.run(
                [
                    chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={target}",
                    f"--window-size={width},{height}",
                    "--virtual-time-budget=4000",
                    "--force-device-scale-factor=2",
                    f"file://{tmp}",
                ],
                capture_output=True, text=True, timeout=120,
            )
            if not target.exists():
                sys.exit(f"Chrome produced no image for page {page}:\n"
                         f"{(proc.stderr or '').strip()[:400]}")
            written.append(target)
            print(f"  page {page:>3} {args.theme:<5} -> {target.relative_to(out.parent)}"
                  f"  ({target.stat().st_size // 1024} KB)")
        finally:
            if tmp and tmp.exists():
                tmp.unlink()

    print(f"\n{len(written)} screenshot(s) in {out}")
    print("Look at them before shipping: a label can drift outside its box in a figure, and only "
          "a human eye catches that.")


if __name__ == "__main__":
    main()
