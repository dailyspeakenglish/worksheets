# Daily Speak English – Free Worksheets

Free printable B1–B2 English worksheets for the [Daily Speak English](https://www.youtube.com/@DailySpeak_English) podcast.

**Live site:** https://dailyspeakenglish.github.io/worksheets/

**Making a new worksheet? Read [`_source/WORKSHEET_GUIDE.md`](_source/WORKSHEET_GUIDE.md) first.**

## How it's organised
- `worksheets.json` – one entry per worksheet (title, level, PDF name, video link…)
- `<slug>/` – the worksheet page, its PDF and preview images
- `build.py` – regenerates `index.html` and every `<slug>/index.html` from `worksheets.json`
- `assets/` – shared styles, channel logo and host avatars
- `_source/` – the HTML templates used to build each worksheet PDF, plus `tools/` (image preparation and site images) and the step-by-step guide
- `_library/characters/` – Jack & Lucy image library for worksheets (see its README)

## Adding a worksheet
1. Create a folder `<slug>/` with the PDF, `cover.jpg`, `og.jpg` and preview images.
2. Add an entry to `worksheets.json`.
3. Run `python3 build.py`, commit and push.
