# Daily Speak English – Worksheet Guide

Everything needed to make, check and publish the free PDF worksheet for a new episode.
Read this whole file before starting. The best current example is `_source/talk-to-strangers/`
(the one before it, `_source/daylight/`, uses the old orange palette – don't copy its colours).

---

## 1. Who it's for and what "good" means

- Channel: **Daily Speak English** (youtube.com/@DailySpeak_English) – a B1–B2 English-learning podcast with two illustrated hosts, **Jack** and **Lucy**. Many viewers are in Brazil.
- YouTube auto-translates the videos into 21 languages, so **never add country-specific sections** (no "Turkish speakers / Brazilian speakers watch out" boxes). Keep everything international.
- No alcohol anywhere (no wine, beer etc.), nothing that promotes things with no benefit to the body.
- The worksheet must be **fun, educational and channel-branded**, printable **and** usable on a tablet, and **doable alone** (never require a partner; "with a friend – or out loud to yourself" is fine).
- Score is always **exactly 100 points**. About **8–10 A4 pages**, ~45–50 minutes.
- Every new worksheet should be at least as good as `talk-to-strangers` – and try 1–2 new ideas from research.

## 2. Inputs from the user

1. The episode script (`.txt`, JACK:/LUCY: lines).
2. The NoteGPT audio length and chapter list.

**Video timestamps** (for the ⏱ hints): the video plays the audio at 0.95 speed after a 5-second intro, so
`video time = NoteGPT time ÷ 0.95 + 5 s`, rounded **down** to the second. Example: NoteGPT 12:44 → 13:29.
Use the start of the matching chapter for each ⏱ hint.

## 3. Research (every worksheet)

- **Fact-check the script**: every study, year, number and name. Use primary or reliable sources and note anything wrong.
- **Look for 1–2 fresh worksheet ideas** for this topic from reliable teaching sources (British Council / TeachingEnglish, Cambridge English, BBC Learning English, Oxford, academic ESL sources). Use different sources each time.
- Report in Turkish what you checked and what you applied, with links.

## 4. Structure and pedagogy

Follow pre-listening → while-listening → post-listening:

- **Page 1:** cover (title, one-line summary, Name/Date/My score ___ / 100), hero image of Jack & Lucy, "How to use" (3 steps), a fun warm-up (0 points), "Let's talk" (4 questions).
- **Before listening:** key words matching (10), a prediction task (e.g. "one of these words is NOT in the episode").
- **First listen = gist:** one "big idea" question (2 points).
- **Second listen = details:** "Know it or hear it?" – questions 🧠 1–5 can be answered without listening (common sense, grammar, Ex. 1), 🎧 6–10 need listening, each with a ⏱ time. True/False with ⏱ times.
- **Language work:** a chat-style dialogue from the script with gaps (Lucy on the left, Jack on the right, with library avatars), phrase sorting, pronunciation (e.g. intonation), "Say it better" (natural vs. textbook sentences, 2 points each), idioms in context.
- **Thinking / culture:** short judgement tasks (e.g. "Good moment to say hi? 👍/✋", "Safe or tricky topic?").
- **Story / reading:** order the events of the episode's story, plus a "Think about it" question (0 points).
- **Production:** a short guided writing task (2 points per line).
- **After:** a 7-day real-life challenge table, a cut-out pocket phrase card, a "Can you do it now?" self-check, a "Share it with us" comment prompt.
- **Last page:** full answer key + QR (subscribe) + "More free worksheets: dailyspeakenglish.github.io/worksheets".

Rules that came from the user's feedback:
- Some quiz questions must be answerable **without** listening (🧠), others need listening (🎧).
- Use **varied** images of Jack and Lucy – avoid using the same image twice on one page.
- Tips come from the characters in speech bubbles ("Jack's tip", "Lucy's tip", "Did you know?").
- Keep instructions short and simple (B1).
- Two-choice judgement tasks (good/bad, safe/tricky…) must use **opposite colours and shapes**: green ✓ chip vs red ✗ chip (`.pick.good` / `.pick.bad` in `build-a-habit`). Never two similar emoji (🌱/🌵 looked the same in print).
- **Word search:** always build it with `python3 _source/tools/wordsearch.py _source/<slug>/ws_spec.json`. The tool guarantees: words never cross, each word appears exactly once (all 8 directions), only → ↓ ↘ ↗, max 4 diagonals, and the leftover letters spell the secret message. Use clues with letter slots (`wordsearch.slots`) instead of a word list, and the capsule answer key (`wordsearch.key_svg`) – never a key that only shades cells.

## 5. Design system

Copy `_source/talk-to-strangers/template.html` – its CSS is the design system. Channel palette (from the logo/banner):

| Token | Hex | Use |
|---|---|---|
| `--night` | #1B2147 | headings, dark panels |
| `--mauve` | #6E5D8C | section numbers, accents |
| `--lav` / `--lav2` | #F1EDF8 / #DED5EE | cards, avatar circles |
| `--peach` / `--peach-l` / `--peach-d` | #F2AE94 / #FDEDE5 / #A9532F | points tags, Lucy bubbles, hints |
| `--sage` / `--sage-d` | #D7E7DD / #2F5E50 | "fun" tags, correct/safe |
| `--teal-l` | #E3F0F3 | "Let's talk" cards |

- Fonts: Poppins (installed) + Noto Color Emoji. A4, 12 mm top / 14 mm sides, footer added by `build_pdf.py` (`{{FOOTn}}` placeholders, page count is automatic).
- Useful components: `.mcq` (multiple choice), `.tf` (true/false table), `.chat` + `.msg.l` / `.msg.j` (chat dialogue), `.map` (3-column sorting), `.sit` (situation cards), `.story` (ordering), `.chal` (7-day table), `.pocket` (cut-out card), `.cando` (self-check), `.bub` (character tip bubble), `.key .k` (answer key cards).
- Arrows ↘ ↗ are turned into SVG by `build_pdf.py` (the emoji font would otherwise draw blue boxes).

## 6. Jack & Lucy images

- Library: `_library/characters/` (catalog in its README and `characters.json`; 35 images, flat style, white background). Lucy `*-right` images face right, Jack `*-left` images face left – use them for dialogues.
- In the template, reference an image as `img/f/<library name>-<bg>.jpg`, where `<bg>` is the colour behind it: `w` (white page/card), `lav`, `peach`, `night`, `sage`, `teal`. Avatars in `.ava` circles use `lav`.
- Then run `python3 _source/tools/prepare_images.py _source/<slug>` – it cuts each image out, keeps teeth/eyes (`cutout-keeps.json`), resizes and flattens it onto the right colour as a small JPEG. **Always check faces at 110 dpi** after building – if teeth or eyes look coloured, add a `--keep x,y` entry to `cutout-keeps.json` (coordinates in the 2048 px original) and rebuild.
- Don't give the user new image prompts unless they ask for them.

## 7. Build and check

```
cp -r _source/talk-to-strangers _source/<slug>      # start from the latest worksheet
# edit _source/<slug>/template.html
python3 _source/tools/prepare_images.py _source/<slug>   # builds missing images, deletes unused ones
cd _source/<slug> && python3 build_pdf.py            # writes worksheet.pdf
pdftoppm -r 75 -png worksheet.pdf /tmp/p             # look at EVERY page
```

Check every page image for: text running into the footer, awkward wraps, empty half pages, broken emoji, images with coloured eyes/teeth. Fix and rebuild until clean. Target PDF size ≤ 2 MB.

**QA checklist before publishing**
- Every answer in the key matches its question; letters/numbers are spread (not all "b").
- Points on the tags add up to exactly 100.
- ⏱ times are converted video times.
- Facts match the sources; no typos (run a repeated-word/space check).

## 8. Publish (only when the user wants it live – never for a test run)

```
mkdir <slug> && cp _source/<slug>/worksheet.pdf <slug>/daily-speak-english-<slug>-worksheet.pdf
python3 _source/tools/site_images.py <slug> <3 preview page numbers>
# add an entry to worksheets.json (copy the talk-to-strangers entry: slug, title, topic, summary,
#   level, pages, exercises, minutes, pdf, video, date, inside[], previews[])
python3 build.py
git add -A && git commit && git push origin HEAD:main
```

- GitHub: attach the repo `dailyspeakenglish/worksheets` with push access (do **not** attach `dailyspeakenglish.github.io`).
- GitHub Pages deploys in ~1 minute. The shell can't reach github.io – verify with WebFetch, adding `?v=<n>` to dodge its 15-minute cache:
  `https://dailyspeakenglish.github.io/worksheets/<slug>/?v=1` and the PDF link.
- Live link format: `https://dailyspeakenglish.github.io/worksheets/<slug>/` (keep the trailing slash).

## 9. What to send the user (in Turkish)

1. The PDF file.
2. The live link, plus ready-to-paste lines:
   - Description: `📄 FREE PDF WORKSHEET (answer key included) 👇` + link
   - Pinned comment: `📄 Free PDF worksheet for this episode (answer key + …): ` + link
3. A short list of what's new in this worksheet and what the research changed.

## 10. Known pitfalls

- `img{height:auto}` is required, or images with width/height attributes get stretched.
- Footer spans need `white-space:nowrap`.
- T/F circles need `white-space:nowrap` and ~17 mm width.
- Long chat dialogues overflow page bottoms – keep bubbles compact (`.msg .b` padding ~1.6 mm).
- Transparent PNGs get embedded once per use and make the PDF huge – always use the flattened JPEGs.
