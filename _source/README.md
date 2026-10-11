# Worksheet sources

Each folder holds the files used to build one worksheet PDF:

- `template.html` – the A4 worksheet (HTML + CSS, 8 pages)
- `ws.json` – word-search grid and word positions
- `hero.jpg`, `jack.png`, `lucy.png`, `qr.png` – images used in the template
- `build_pdf.py` – renders `template.html` to `worksheet.pdf` with Playwright/Chromium

To start a new worksheet, copy the latest folder, change the content and colours, then run `python3 build_pdf.py`.
The finished PDF goes into the public `<slug>/` folder of the site (see the main README).
