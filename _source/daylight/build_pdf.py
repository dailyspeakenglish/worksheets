"""Builds the worksheet PDF from template.html (+ ws.json word search).
Run from this folder: python3 build_pdf.py   (needs playwright + chromium)"""
import json, asyncio, pathlib
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "worksheet.pdf"

d = json.load(open(HERE / "ws.json")); g = d["grid"]; pos = d["pos"]
on = set(tuple(c) for cells in pos.values() for c in cells)
ws = '<table class="ws">' + ''.join('<tr>' + ''.join(f'<td>{ch}</td>' for ch in row) + '</tr>' for row in g) + '</table>'
wk = '<table class="wsk" style="border-collapse:separate;border-spacing:.6mm">' + ''.join(
    '<tr>' + ''.join(f'<td class="{"on" if (r, c) in on else ""}">{ch}</td>' for c, ch in enumerate(row)) + '</tr>'
    for r, row in enumerate(g)) + '</table>'
html = (HERE / "template.html").read_text().replace('{{WORDSEARCH}}', ws).replace('{{WORDSEARCH_KEY}}', wk)
(HERE / "index.html").write_text(html)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto((HERE / "index.html").as_uri()); await pg.wait_for_timeout(800)
        await pg.pdf(path=str(OUT), format="A4", print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}, prefer_css_page_size=True)
        await b.close()

asyncio.run(main())
print("wrote", OUT)
