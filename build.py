"""Builds the Daily Speak English worksheet site from worksheets.json.
Run: python3 build.py  (writes index.html and <slug>/index.html)"""
import json, html
from datetime import date

BASE = "https://dailyspeakenglish.github.io/worksheets/"
CHANNEL = "https://www.youtube.com/@DailySpeak_English?sub_confirmation=1"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='32' fill='%23F28C28'/%3E%3Crect x='24' y='12' width='16' height='26' rx='8' fill='%23fff'/%3E%3Cpath d='M18 30a14 14 0 0 0 28 0' stroke='%23fff' stroke-width='4' fill='none' stroke-linecap='round'/%3E%3Cpath d='M32 44v8M24 52h16' stroke='%23fff' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E"
YT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#FF0000" d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8z"/><path fill="#fff" d="M9.6 15.6V8.4l6.3 3.6z"/></svg>'
e = html.escape


def head(title, desc, url, image, extra="", root=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Daily Speak English">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F28C28">
<link rel="icon" href="{FAVICON}">
{FONTS}
<link rel="stylesheet" href="{root}assets/style.css">
{extra}
</head>
<body>
<div class="stripe"></div>
<div class="wrap">
<header class="top">
  <a class="brand" href="{root or './'}"><span class="mic">🎙</span><span>Daily Speak English<small>Free English worksheets</small></span></a>
  <a class="btn btn-yt" href="{CHANNEL}" target="_blank" rel="noopener">{YT}Subscribe</a>
</header>
"""


FOOT = f"""<footer>
  <span>© {date.today().year} Daily Speak English · Free for personal and classroom use. Please share the page link, not the file.</span>
  <span><a href="https://dailyspeakenglish.github.io/worksheets/">All worksheets</a> · <a href="{CHANNEL}" target="_blank" rel="noopener">YouTube</a></span>
</footer>
</div>
</body>
</html>
"""


def worksheet_page(w):
    url = f"{BASE}{w['slug']}/"
    title = f"{w['title']} – Free English Worksheet (PDF, {w['level']})"
    desc = f"Free printable {w['level']} English worksheet with answer key: {w['topic'].lower()}. {w['exercises']} fun exercises based on the Daily Speak English podcast."
    video = w["video"] or CHANNEL
    ld = {
        "@context": "https://schema.org", "@type": "LearningResource",
        "name": f"{w['title']} – English worksheet", "description": desc, "url": url,
        "inLanguage": "en", "learningResourceType": "Worksheet", "educationalLevel": f"CEFR {w['level']}",
        "isAccessibleForFree": True, "timeRequired": f"PT{w['minutes']}M", "datePublished": w["date"],
        "image": f"{url}cover.jpg", "encoding": {"@type": "MediaObject", "contentUrl": f"{url}{w['pdf']}", "encodingFormat": "application/pdf"},
        "publisher": {"@type": "Organization", "name": "Daily Speak English", "url": "https://www.youtube.com/@DailySpeak_English"},
    }
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    checks = "".join(f"<li>{e(x)}</li>" for x in w["inside"])
    prev = "".join(f'<img src="{p}" alt="Worksheet page preview" loading="lazy" width="760" height="1075">' for p in w["previews"])
    return head(title, desc, url, f"{url}og.jpg", extra, "../") + f"""
<main>
<section class="hero">
  <div>
    <div class="eyebrow"><span class="pill navy">{e(w['level'])}</span><span class="pill sun">FREE PDF WORKSHEET</span><span class="pill white">Answer key included</span></div>
    <h1>{e(w['title'])}</h1>
    <p class="lead">{e(w['summary'])}</p>
    <ul class="facts"><li>📄 {w['pages']} pages</li><li>✏️ {w['exercises']} exercises</li><li>⏱ about {w['minutes']} minutes</li><li>⭐ score out of 100</li></ul>
    <div class="cta">
      <a class="btn btn-main" href="{w['pdf']}" download>⬇ Download the free PDF</a>
      <a class="btn btn-ghost" href="{video}" target="_blank" rel="noopener">▶ Watch the episode</a>
    </div>
    <p class="note">No sign-up, no email. Print it or fill it in on your tablet.</p>
  </div>
  <div class="cover"><span class="sticker">FREE!</span><img src="cover.jpg" alt="Cover of the {e(w['title'])} worksheet" width="760" height="1075"></div>
</section>
</main>
</div>
<section class="band">
  <div class="wrap inside">
    <div>
      <h2>What's inside</h2>
      <ul class="checks">{checks}</ul>
    </div>
    <div class="previews">{prev}</div>
  </div>
</section>
<div class="wrap">
<section class="how">
  <h2>How to use it</h2>
  <div class="steps">
    <div class="step"><div class="n">1</div><b>Before you listen</b><span>Do the warm-up, learn the key words and make your predictions.</span></div>
    <div class="step"><div class="n">2</div><b>While you listen</b><span>Answer the questions. The ⏱ times show you where to find each part of the episode.</span></div>
    <div class="step"><div class="n">3</div><b>After you listen</b><span>Practise the phrases, check the answer key and share your writing in the comments!</span></div>
  </div>
  <div class="bubble"><img src="../assets/lucy.png" alt="Lucy"><p><b>Lucy:</b> Don't worry if you don't catch every word. Listen for the key words – numbers, names and places help a lot. See you in the comments! 💛</p></div>
</section>
""" + FOOT


def hub(items):
    url = BASE
    title = "Free English Worksheets (PDF) – Daily Speak English"
    desc = "Free printable B1–B2 English worksheets with answer keys. One fun worksheet for every Daily Speak English podcast episode with Jack and Lucy."
    cards = "".join(f"""<a class="card" href="{w['slug']}/">
  <div class="thumb"><img src="{w['slug']}/cover.jpg" alt="" loading="lazy" width="760" height="1075"></div>
  <div class="body"><div class="eyebrow" style="margin:0"><span class="pill navy">{e(w['level'])}</span><span class="pill sun">PDF</span></div>
  <h3>{e(w['title'])}</h3><p>{w['pages']} pages · {w['exercises']} exercises · answer key</p><span class="go">Get the worksheet →</span></div>
</a>""" for w in sorted(items, key=lambda x: x["date"], reverse=True))
    return head(title, desc, url, f"{BASE}{items[0]['slug']}/og.jpg") + f"""
<main>
<section class="hub-hero">
  <div>
    <div class="eyebrow"><span class="pill sun">100% FREE</span><span class="pill white">New worksheet with every episode</span></div>
    <h1>Free English worksheets</h1>
    <p class="lead" style="margin:0">Listen to Jack and Lucy, then practise with a fun, printable worksheet. Vocabulary, listening, idioms, speaking and writing – with a full answer key.</p>
  </div>
  <div class="faces"><img src="assets/jack.png" alt="Jack"><img src="assets/lucy.png" alt="Lucy"></div>
</section>
<section class="grid">{cards}</section>
</main>
""" + FOOT


if __name__ == "__main__":
    items = json.load(open("worksheets.json", encoding="utf-8"))
    for w in items:
        open(f"{w['slug']}/index.html", "w", encoding="utf-8").write(worksheet_page(w))
    open("index.html", "w", encoding="utf-8").write(hub(items))
    print("built", len(items), "worksheet page(s) + hub")
