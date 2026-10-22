"""Builds the worksheet PDF from template.html.
Run from this folder: python3 build_pdf.py   (needs playwright + chromium)"""
import asyncio, pathlib, re
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "worksheet.pdf"
html = (HERE / "template.html").read_text()
pages = len(re.findall(r'<section class="page', html))

def foot(n):
    mid = ('Free for personal and classroom use. Please share the page link, not the file.' if n == pages else
           '<a href="https://www.youtube.com/@DailySpeak_English">youtube.com/@DailySpeak_English</a> · Free worksheets: <a href="https://dailyspeakenglish.github.io/worksheets/">dailyspeakenglish.github.io/worksheets</a>')
    return (f'<div class="footer"><span class="brand"><img src="img/logo.jpg">Daily Speak English</span>'
            f'<span>{mid}</span><span>{n} / {pages}</span></div>')

DN = '<svg class="arr" viewBox="0 0 16 16"><path d="M3 3L12.5 12.5M12.5 5.5V12.5H5.5" stroke="#2F5E50" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
UP = '<svg class="arr" viewBox="0 0 16 16"><path d="M3 13L12.5 3.5M5.5 3.5H12.5V10.5" stroke="#6E5D8C" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
html = html.replace("↘", DN).replace("↗", UP)
for n in range(1, pages + 1):
    html = html.replace("{{FOOT%d}}" % n, foot(n))
(HERE / "index.html").write_text(html)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto((HERE / "index.html").as_uri()); await pg.wait_for_timeout(900)
        await pg.pdf(path=str(OUT), format="A4", print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}, prefer_css_page_size=True)
        await b.close()

asyncio.run(main())

# lossless size squeeze (object streams + max flate) – keeps the PDF comfortably under 2 MB
import shutil, subprocess
if shutil.which("qpdf"):
    tmp = OUT.with_suffix(".tmp.pdf")
    subprocess.run(["qpdf", "--object-streams=generate", "--recompress-flate", "--compression-level=9", str(OUT), str(tmp)], check=True)
    tmp.replace(OUT)
print("wrote", OUT, pages, "pages")
