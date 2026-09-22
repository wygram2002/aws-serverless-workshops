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

Uses a minimal xl/theme/theme1.xml instead of openpyxl's ~10KB default Excel
theme (full color/font/effect scheme boilerplate, irrelevant to a data-only
workbook with no custom styling). That default theme alone is roughly a
third of the whole file's base64 size - large enough that transmitting the
full base64 payload as a single upload-tool-call argument became unreliable
(silent truncation and, separately, silent single-character substitution
were both observed on ~28k-character payloads, with no error surfaced by
any tool - only caught by downloading the uploaded file back and comparing
bytes). The minimal theme keeps every OOXML part the converter needs
(clrScheme/fontScheme/fmtScheme with their required child counts) while
cutting the payload enough to upload reliably in one call.
"""
import base64
import json
import sys

import openpyxl

_MINIMAL_THEME_XML = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Minimal">
<a:themeElements>
<a:clrScheme name="Minimal">
<a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>
<a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>
<a:dk2><a:srgbClr val="000000"/></a:dk2>
<a:lt2><a:srgbClr val="FFFFFF"/></a:lt2>
<a:accent1><a:srgbClr val="4472C4"/></a:accent1>
<a:accent2><a:srgbClr val="ED7D31"/></a:accent2>
<a:accent3><a:srgbClr val="A5A5A5"/></a:accent3>
<a:accent4><a:srgbClr val="FFC000"/></a:accent4>
<a:accent5><a:srgbClr val="5B9BD5"/></a:accent5>
<a:accent6><a:srgbClr val="70AD47"/></a:accent6>
<a:hlink><a:srgbClr val="0563C1"/></a:hlink>
<a:folHlink><a:srgbClr val="954F72"/></a:folHlink>
</a:clrScheme>
<a:fontScheme name="Minimal">
<a:majorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
<a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
</a:fontScheme>
<a:fmtScheme name="Minimal">
<a:fillStyleLst>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
</a:fillStyleLst>
<a:lnStyleLst>
<a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
<a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
<a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
</a:lnStyleLst>
<a:effectStyleLst>
<a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle>
</a:effectStyleLst>
<a:bgFillStyleLst>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
</a:bgFillStyleLst>
</a:fmtScheme>
</a:themeElements>
</a:theme>
"""


def build(tabs, path):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    wb.loaded_theme = _MINIMAL_THEME_XML
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
