#!/usr/bin/env python3
"""Minimal multi-tab xlsx builder for the GTD Board.

Reads JSON from stdin: [{"name": str, "rows": [[cell, ...], ...]}, ...]
Writes a compact .xlsx (inline strings, no theme/styles bloat) to the path in
argv[1] and prints its base64 length. Purpose: keep the create_file payload
small enough to transcribe reliably.
"""
import base64
import json
import sys
import zipfile
from xml.sax.saxutils import escape


def sheet_xml(rows):
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
           '<sheetData>']
    for r_i, row in enumerate(rows, 1):
        out.append(f'<row r="{r_i}">')
        for c_i, val in enumerate(row):
            if val is None or val == "":
                continue
            col = ""
            n = c_i
            while True:
                col = chr(65 + n % 26) + col
                n = n // 26 - 1
                if n < 0:
                    break
            out.append(f'<c r="{col}{r_i}" t="inlineStr"><is><t>'
                       f'{escape(str(val))}</t></is></c>')
        out.append('</row>')
    out.append('</sheetData></worksheet>')
    return "".join(out)


def build(tabs, path):
    n = len(tabs)
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>']
    for i in range(1, n + 1):
        ct.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
                  'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    ct.append('</Types>')

    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                 '</Relationships>')

    wb = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>']
    wb_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for i, tab in enumerate(tabs, 1):
        wb.append(f'<sheet name="{escape(tab["name"])}" sheetId="{i}" r:id="rId{i}"/>')
        wb_rels.append(f'<Relationship Id="rId{i}" '
                       'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                       f'Target="worksheets/sheet{i}.xml"/>')
    wb.append('</sheets></workbook>')
    wb_rels.append('</Relationships>')

    # Google's xlsx->Sheets converter requires a styles part; declare it.
    ct.insert(-1, '<Override PartName="/xl/styles.xml" '
                  'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="2"><fill><patternFill patternType="none"/></fill>'
              '<fill><patternFill patternType="gray125"/></fill></fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
              '</styleSheet>')
    wb_rels.insert(-1, f'<Relationship Id="rId{n+1}" '
                       'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
                       'Target="styles.xml"/>')

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("[Content_Types].xml", "".join(ct))
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", "".join(wb))
        z.writestr("xl/_rels/workbook.xml.rels", "".join(wb_rels))
        z.writestr("xl/styles.xml", styles)
        for i, tab in enumerate(tabs, 1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(tab["rows"]))


if __name__ == "__main__":
    tabs = json.load(sys.stdin)
    out = sys.argv[1]
    build(tabs, out)
    b64 = base64.b64encode(open(out, "rb").read()).decode()
    open(out + ".b64", "w").write(b64)
    print(f"tabs={len(tabs)} xlsx_bytes={len(b64)*3//4} b64_chars={len(b64)}")
