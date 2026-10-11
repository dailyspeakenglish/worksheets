"""Builds the Daily Speak English worksheet site from worksheets.json.
Run: python3 build.py  (writes index.html and <slug>/index.html)"""
import json, html
from datetime import date

BASE = "https://dailyspeakenglish.github.io/worksheets/"
CHANNEL = "https://www.youtube.com/@DailySpeak_English?sub_confirmation=1"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
YT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#FF0000" d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8z"/><path fill="#fff" d="M9.6 15.6V8.4l6.3 3.6z"/></svg>'
e = html.escape


def wave(seed=7, n=90):
    import random
    r = random.Random(seed)
    bars = []
    for i in range(n):
        h = 12 + r.random() * 92 * (0.35 + 0.65 * abs(((i % 30) - 15) / 15))
        bars.append(f'<rect x="{i*12+3}" y="{(120-h)/2:.1f}" width="5" height="{h:.1f}" rx="2.5"/>')
    return f'<svg class="wave" viewBox="0 0 {n*12} 120" preserveAspectRatio="none" aria-hidden="true"><g fill="#8E95C9">{"".join(bars)}</g></svg>'


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
<meta name="theme-color" content="#141936">
<link rel="icon" href="{root}assets/logo.jpg">
{FONTS}
<link rel="stylesheet" href="{root}assets/style.css">
{extra}
</head>
<body>
<div class="night">
{wave()}
<div class="wrap">
<header class="top">
  <a class="brand" href="{root or './'}"><img src="{root}assets/logo.jpg" alt="" width="44" height="44"><span>Daily Speak English<small>Free English worksheets</small></span></a>
  <a class="btn btn-yt" href="{CHANNEL}" target="_blank" rel="noopener">{YT}Subscribe</a>
</header>
"""


FOOT = f"""<footer class="site night"><div class="wrap">
  <span>© {date.today().year} Daily Speak English · Free for personal and classroom use. Please share the page link, not the file.</span>
  <span><a href="https://dailyspeakenglish.github.io/worksheets/">All worksheets</a> · <a href="{CHANNEL}" target="_blank" rel="noopener">YouTube</a></span>
</div></footer>
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
    prev = "".join(f'<img src="{p}" alt="Worksheet page preview" loading="lazy" width="640" height="905">' for p in w["previews"])
    return head(title, desc, url, f"{url}og.jpg", extra, "../") + f"""
<main>
<section class="hero">
  <div>
    <div class="eyebrow"><span class="pill peach">{e(w['level'])}</span><span class="pill sage">FREE PDF WORKSHEET</span><span class="pill line">Answer key included</span></div>
    <h1>{e(w['title'])}</h1>
    <p class="lead">{e(w['summary'])}</p>
    <ul class="facts"><li>📄 {w['pages']} pages</li><li>✏️ {w['exercises']} exercises</li><li>⏱ about {w['minutes']} minutes</li><li>⭐ score out of 100</li></ul>
    <div class="cta">
      <a class="btn btn-main" href="{w['pdf']}" download>⬇ Download the free PDF</a>
      <a class="btn btn-ghost" href="{video}" target="_blank" rel="noopener">▶ Watch the episode</a>
    </div>
    <p class="note">No sign-up, no email. Print it or fill it in on your tablet.</p>
  </div>
  <div class="cover"><span class="sticker">FREE!</span><img src="cover.webp" alt="Cover of the {e(w['title'])} worksheet" width="1200" height="1697" fetchpriority="high"></div>
</section>
</main>
</div>
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
</div>
""" + FOOT


def hub(items):
    url = BASE
    title = "Free English Worksheets (PDF) – Daily Speak English"
    desc = "Free printable B1–B2 English worksheets with answer keys. One fun worksheet for every Daily Speak English podcast episode with Jack and Lucy."
    cards = "".join(f"""<a class="card" href="{w['slug']}/">
  <div class="thumb"><img src="{w['slug']}/cover.webp" alt="" loading="lazy" width="1200" height="1697"></div>
  <div class="body"><div class="eyebrow" style="margin:0"><span class="pill mauve">{e(w['level'])}</span><span class="pill sage">PDF</span></div>
  <h3>{e(w['title'])}</h3><p>{w['pages']} pages · {w['exercises']} exercises · answer key</p><span class="go">Get the worksheet →</span></div>
</a>""" for w in sorted(items, key=lambda x: x["date"], reverse=True))
    return head(title, desc, url, f"{BASE}{items[0]['slug']}/og.jpg") + f"""
<main>
<section class="hub-hero">
  <div>
    <div class="eyebrow"><span class="pill peach">100% FREE</span><span class="pill line">New worksheet with every episode</span></div>
    <h1>Free English worksheets</h1>
    <p class="tagline">Where daily practice turns into fluent English</p>
    <p class="lead" style="margin:0">Listen to Jack and Lucy, then practise with a fun, printable worksheet. Vocabulary, listening, idioms, speaking and writing – with a full answer key.</p>
  </div>
  <div class="faces"><img src="assets/jack.png" alt="Jack"><img src="assets/lucy.png" alt="Lucy"></div>
</section>
</main>
</div>
</div>
<div class="wrap"><section class="grid">{cards}</section></div>
""" + FOOT


if __name__ == "__main__":
    items = json.load(open("worksheets.json", encoding="utf-8"))
    for w in items:
        open(f"{w['slug']}/index.html", "w", encoding="utf-8").write(worksheet_page(w))
    open("index.html", "w", encoding="utf-8").write(hub(items))
    print("built", len(items), "worksheet page(s) + hub")
