#!/usr/bin/env python3
"""Multi-tab xlsx builder for the GTD Board.

Reads JSON from stdin: [{"name": str, "rows": [[cell, ...], ...]}, ...]
Writes a .xlsx to the path in argv[1] and prints its base64 length.

Built on openpyxl rather than hand-rolled OOXML: an earlier hand-rolled
minimal writer (coordinate-free rows/cells, no <dimension>/<cols>) produced
files that Python's zipfile read back correctly but that Google Drive's
xlsx->Sheets converter would sometimes silently convert into a BLANK sheet
for one tab (observed on "Today") while every other tab came through fine -
confirmed by downloading the converted Sheet back out and inspecting its
worksheet XML directly, not just by eyeballing read_file_content's summary.
The failure was deterministic for a given payload but the exact trigger in
the minimal OOXML was never isolated. Producing fully spec-conformant OOXML
via openpyxl avoids it. Keep using this module rather than reintroducing a
minimal writer.
"""
import base64
import json
import sys

import openpyxl


def build(tabs, path):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for tab in tabs:
        ws = wb.create_sheet(tab["name"])
        for row in tab["rows"]:
            ws.append(row)
    wb.save(path)


if __name__ == "__main__":
    tabs = json.load(sys.stdin)
    out = sys.argv[1]
    build(tabs, out)
    b64 = base64.b64encode(open(out, "rb").read()).decode()
    open(out + ".b64", "w").write(b64)
    print(f"tabs={len(tabs)} xlsx_bytes={len(b64)*3//4} b64_chars={len(b64)}")
