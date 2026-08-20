#!/usr/bin/env python3

import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSEMBLER = ROOT / "scripts" / "assemble_book.py"
VALIDATOR = ROOT / "scripts" / "validate_book.py"


class ScriptRegressionTests(unittest.TestCase):
    def run_script(self, script: pathlib.Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(script), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_assembler_rejects_sources_without_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            fragment = root / "empty.html"
            fragment.write_text("<p>not a page</p>", encoding="utf-8")
            result = self.run_script(ASSEMBLER, str(fragment), "-o", str(root / "book.html"))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn('no <section class="page"> blocks found', result.stderr)

    def test_validator_rejects_chromatic_functional_colour(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book = pathlib.Path(tmp) / "book.html"
            book.write_text(
                '<title>x</title><style>:root{color:rgb(255,0,0)}</style>',
                encoding="utf-8",
            )
            result = self.run_script(VALIDATOR, str(book), "--min-pages", "0")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("non-greyscale functional colours", result.stdout)

    def test_validator_does_not_count_page_prefix_class(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book = pathlib.Path(tmp) / "book.html"
            book.write_text(
                '<title>x</title><section class="pageant" id="fake"></section>',
                encoding="utf-8",
            )
            result = self.run_script(VALIDATOR, str(book), "--min-pages", "0")

        self.assertEqual(result.returncode, 0)
        self.assertIn("pages: 0", result.stdout)

    def test_assembler_escapes_book_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            fragment = root / "page.html"
            output = root / "book.html"
            fragment.write_text('<section class="page"></section>', encoding="utf-8")
            result = self.run_script(
                ASSEMBLER,
                str(fragment),
                "-o",
                str(output),
                "--book-id",
                'one" onmouseover="bad',
            )

            rendered = output.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0)
        self.assertIn('data-book-id="one&quot; onmouseover=&quot;bad"', rendered)
        self.assertNotIn('data-book-id="one" onmouseover="bad"', rendered)


if __name__ == "__main__":
    unittest.main()
