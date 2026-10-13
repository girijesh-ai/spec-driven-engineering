#!/usr/bin/env bash
# CSV export that pages through rows. Bug: integer division drops the last
# partial page, so rows go missing only when the count isn't a multiple of
# PAGE_SIZE — the test data (100 rows) never triggers it; production does.
set -euo pipefail
mkdir -p tests
cat > export.py <<'PY'
import csv
import io

PAGE_SIZE = 50


def fetch_page(rows, page):
    start = page * PAGE_SIZE
    return rows[start : start + PAGE_SIZE]


def export_csv(rows):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["id", "amount"])
    for page in range(len(rows) // PAGE_SIZE):
        for row in fetch_page(rows, page):
            writer.writerow(row)
    return buffer.getvalue()
PY
cat > tests/__init__.py <<'PY'
PY
cat > tests/test_export.py <<'PY'
import unittest

from export import export_csv


class ExportTest(unittest.TestCase):
    def test_exports_every_row(self):
        rows = [(i, i * 10) for i in range(100)]
        lines = export_csv(rows).strip().splitlines()
        self.assertEqual(len(lines), 101)  # header + 100 rows


if __name__ == "__main__":
    unittest.main()
PY
printf 'Run tests with: python3 -m unittest discover -s tests -t .\n' > README.md
git init -q && git add -A && git -c user.name=eval -c user.email=eval@example.com commit -q -m init
