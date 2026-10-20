"""Writes template.html for the reading-books worksheet (Podcast 64).
CSS design system copied from remember-more (which includes all earlier worksheets).
Word search from ws.json (built by _source/tools/wordsearch.py). Timestamps: video time = NoteGPT time + 5 s."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import wordsearch as W

src = (HERE.parent / "remember-more" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Remember More Worksheet", "Reading Books Worksheet")
ws = json.loads((HERE / "ws.json").read_text())
W.check(ws)

EXTRA = """
/* ---- new in reading-books ---- */
.ws td{width:7.2mm;height:7.2mm;font-size:10.4pt}
.dots{display:flex;flex-wrap:wrap;gap:1mm;margin:1.4mm 0}
.dots i{display:inline-block;width:2.6mm;height:2.6mm;border-radius:50%;background:#D9D2E6}
.dots i.u{background:#E8875F}
.cov{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.cov>div{border-radius:3mm;padding:2mm 3mm;font-size:8.6pt;line-height:1.4}
.story-text{font-family:Georgia,'Times New Roman',serif;font-size:10.4pt;line-height:1.75;color:#2B2440;background:#FFFDF8;border:1px solid #EFE2D0;border-radius:3mm;padding:3mm 5mm}
.meter{display:flex;gap:2mm;font-size:8.4pt;margin-top:1.6mm}
.meter span{flex:1;border-radius:2.4mm;padding:1.2mm 2mm;text-align:center;font-weight:700}
.checks{display:grid;grid-template-columns:1fr 1fr;gap:1.4mm 5mm;font-size:8.9pt}
.checks div{display:flex;gap:1.8mm;align-items:center}
"""

def foot(n): return "{{FOOT%d}}" % n

def chat(rows):
    out = []
    for who, img, text in rows:
        side = "l" if who == "LUCY" else "j"
        out.append(f'    <div class="msg {side}"><div class="ava"><img src="img/f/{img}-lav.jpg"></div>'
                   f'<div class="b"><span class="who">{who}</span>{text}</div></div>')
    return "\n".join(out)

def gap(n): return f'<span class="gap">{n}</span>'

CHAT = chat([
 ("JACK", "13-jack-talking-left", f"Hi, sorry, could you help me? I'm looking for something to read on {gap(1)}, but I'm not sure what to choose."),
 ("LUCY", "11-lucy-asking-right", "Of course. What kind of books do you usually enjoy?"),
 ("JACK", "15-jack-shrug-left", f"To be honest, I haven't read a book in {gap(2)}. I used to love adventure stories, though."),
 ("LUCY", "38-lucy-explaining-right", f"Then you might like this one. It's about two brothers who get lost in the {gap(3)}. It's a real page-{gap(4)}. I read it in two days."),
 ("JACK", "16-jack-surprised-left", f"That sounds great. Is it hard to get {gap(5)}? I sometimes give up after the first chapter."),
 ("LUCY", "09-lucy-talking-right", f"Not at all. It grabs you from the very first page. Here, have a {gap(6)} through."),
 ("JACK", "43-jack-explaining-left", "Oh, the first line is really good. Okay, I'm interested. Does it have a happy ending?"),
 ("LUCY", "12-lucy-laughing-right", f"I'm not going to tell you that. No {gap(7)}."),
 ("JACK", "45-jack-agreeing-left", f"Fair enough. I'll take it. And if I can't put it {gap(8)}, I'll come back for another one."),
 ("LUCY", "40-lucy-excited-right", "Deal. And if you don't like it, bring it back and tell me why. I want to know."),
])

def pair(i, text, a, b, ca, cb):
    return (f'<div class="sit"><div class="t" style="min-height:0"><b>{i}.</b> {text}</div><div class="ch" style="gap:2mm">'
            f'<span class="claim {ca}"><span class="box"></span>{a}</span>'
            f'<span class="claim {cb}"><span class="box"></span>{b}</span></div></div>')
BL = [
 ("“Can I ______ your book, please?” 📕", "📥 borrow", "📤 lend"),
 ("“Could you ______ me your book?” 📗", "📥 borrow", "📤 lend"),
 ("“I ______ this novel from the library.” 🏛️", "📥 borrowed", "📤 lent"),
 ("“I've been reading it ______ Monday.” 📅", "⏳ for", "📍 since"),
 ("“She's been a bookworm ______ she was six.” 🐛", "⏳ for", "📍 since"),
 ("“I've had this graded reader ______ two weeks.” 📘", "⏳ for", "📍 since"),
]
BLS = "".join(pair(i, t, a, b, "ed", "ing") for i, (t, a, b) in enumerate(BL, 1))

PS = ["📚 Studying a textbook for an exam", "🏖️ Reading a novel on holiday", "⏰ Reading an important article in a hurry",
      "💬 A quick message from a friend", "🔬 Learning new facts from a science text", "😂 A funny short story before bed"]
PSS = "".join(f'      <div class="tm2" style="grid-template-columns:1fr 23mm 31mm;padding:.6mm 0"><span>{i}. {t}</span><span class="claim ed"><span class="box"></span>📄 paper</span><span class="claim ing"><span class="box"></span>📱 screen is fine</span></div>\n' for i, t in enumerate(PS, 1))

clues = [
 ("BOOKWORM", "A person who loves reading: a {}."),
 ("BOOKMARK", "Grandad hid a leather {} in the book."),
 ("LIBRARY", "You can borrow books from a {}."),
 ("CHAPTER", "Jack often gave up after the first {}."),
 ("SPOILER", "“Don't tell me the end!” No {}s!"),
 ("SAILORS", "Grandad's stories: travellers and {}."),
 ("DESERT", "Two brothers get lost in the {}."),
 ("SHELF", "The book sat on a {} for ten years."),
 ("NOVEL", "A long story in a book: a {}."),
 ("BUS", "Lucy missed her stop on the {}."),
]
assert sorted(w for w, _ in clues) == sorted(ws["pos"])
def nw(t):
    return re.sub(r"\{\}(\S*)", lambda m: '<span style="white-space:nowrap">{}' + m.group(1) + '</span>', t)
CLUES = "".join(f'      <div><span class="n">{i}</span><span>{nw(t).format(W.slots(w))}</span></div>\n'
                for i, (w, t) in enumerate(clues, 1))
WS_KEY = " · ".join(f"{i} {w.lower()}" for i, (w, _) in enumerate(clues, 1))

DOTS50 = '<div class="dots">' + '<i></i>' * 24 + '<i class="u"></i>' + '<i></i>' * 25 + '</div>'
DOTS20 = '<div class="dots">' + '<i></i>' * 9 + '<i class="u"></i>' + '<i></i>' * 10 + '</div>'

MINI = ("Lucy opened her book as the bus left the city centre. It was a detective story, and she was close to the end. "
        "“Just one more page,” she thought. The bus stopped and started, again and again. People got on and off, but Lucy "
        "didn't notice anything. She was completely absorbed in the story. When she finally looked up, the bus was silent and "
        "empty. The driver was standing next to her. “End of the line, madam,” he said, smiling. Lucy laughed. She was on the "
        "other side of the city, but it didn't matter. She knew who did it!")
assert len(re.findall(r"[A-Za-z']+", MINI.replace("’", "'"))) == 100

body = f"""
<!-- ================= PAGE 1 ================= -->
<section class="page">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:1mm">
    <div class="brand"><img src="img/logo.jpg">DAILY SPEAK ENGLISH · PODCAST WORKSHEET</div>
    <div><span class="pill">B1–B2</span> <span class="pill p">⏱ 50 min</span></div>
  </div>
  <div style="display:grid;grid-template-columns:1.12fr .88fr;gap:4mm;margin-top:4mm;align-items:center">
    <div>
      <div class="small" style="font-weight:700;color:var(--mauve);letter-spacing:.7pt">LISTEN · LEARN · SPEAK</div>
      <h1>Why Reading Books Is So Good for You</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">A twelve-year study about book readers, paper or screen, the 98% rule for choosing the right book in English, book idioms – and the secret inside Jack's grandfather's book.</p>
      <div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div class="hero2">
      <div style="position:absolute;z-index:2;top:3.4mm;left:3.4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">"End of the line, madam!" 🚌</div>
      <img class="char" src="img/f/19-lucy-glasses-book-lav.jpg" style="position:absolute;bottom:0;left:3mm;width:35mm">
      <img class="char" src="img/f/16-jack-surprised-left-lav.jpg" style="position:absolute;bottom:0;right:2mm;width:35mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · After you listen 📖</div><div class="s">Try the one-page test, find the secret message – and read one page every day!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: My reading check <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Be honest! Tick everything that is true for you. 😊</p>
    <div style="display:grid;grid-template-columns:1.42fr .58fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:1.8mm;justify-content:center;padding:2.6mm 3.6mm">
        <div class="conf" style="grid-template-columns:1fr 1fr;justify-content:stretch;font-size:8.7pt">
          <div><span class="box sm"></span>📖 I finished a book this year</div>
          <div><span class="box sm"></span>🛏️ I read before bed</div>
          <div><span class="box sm"></span>📱 I read more on screens</div>
          <div><span class="box sm"></span>🚌 I read on buses or trains</div>
          <div><span class="box sm"></span>📗 I've read a book in English</div>
          <div><span class="box sm"></span>😴 I often give up after a page</div>
        </div>
        <div style="font-size:9pt"><b style="color:var(--night)">My reading score:</b> <span class="blank s"></span> / 6</div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> In a twelve-year study, how much longer did book readers live, on average?</div>
        <div style="display:flex;gap:3.4mm;font-size:8.7pt;white-space:nowrap"><span><span class="circ">a</span> about two months</span><span><span class="circ">b</span> almost two years</span><span><span class="circ">c</span> about ten years</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 2:51</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:1.8mm 2.4mm;font-size:8.1pt;border:1.2px solid #F4D2C2;line-height:1.36"><b style="color:var(--night)">Jack:</b> "Grandad's old book sat on my shelf for ten years…" 📕</div>
        <img class="char" src="img/f/35-jack-reading-card-peach.jpg" style="width:28mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – or write them in your notebook.</p>
    <div class="grid2" style="gap:2.4mm">
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>1.</b> What was the last book you finished?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>2.</b> Which book did you love as a child?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>3.</b> Do you prefer paper books or screens? Why?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>4.</b> Have you ever missed your stop because of a book?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Then check at ⏱ 13:43 and ⏱ 14:52</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> a bookworm</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> to skim</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> a page-turner</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> to get lost in a book</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> absorbed</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> a graded reader</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> a spoiler</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> to flick through</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> to get into (a book)</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> an association</td></tr>
      </table>
      <div class="card" style="font-size:9pt;line-height:1.55">
        <b>a)</b> a book so exciting that you keep turning the pages<br>
        <b>b)</b> to start enjoying a book<br>
        <b>c)</b> a person who loves reading and reads a lot<br>
        <b>d)</b> a link between two things – but not proof<br>
        <b>e)</b> a book written for language learners at a particular level<br>
        <b>f)</b> to read very quickly to get the general idea<br>
        <b>g)</b> to turn the pages quickly without reading carefully<br>
        <b>h)</b> to be so interested in a book that you forget the world around you<br>
        <b>i)</b> information that tells you what happens in a story too early<br>
        <b>j)</b> giving something all your attention
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/03-lucy-did-you-know-w.jpg" style="width:20mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> <b style="color:var(--peach-d)">BOOK</b>-worm · ab-<b style="color:var(--peach-d)">SORBED</b> (/əbˈzɔːbd/) · <b style="color:var(--peach-d)">LI</b>-bra-ry (three syllables – not "libery"!) · <b style="color:var(--peach-d)">CHAP</b>-ter · <b style="color:var(--peach-d)">NOV</b>-el. Say it: <i>"It's a real page-turner – I couldn't put it down!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>Reading books is a healthy, pleasant habit – and in English, an easy book you enjoy, a little every day, works best.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>You should only read difficult novels, with a dictionary next to you.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>Reading on paper and reading on screens are always exactly the same.</div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <div class="ava" style="width:22mm;height:22mm"><img src="img/f/53-jack-listen-carefully-lav.jpg" style="height:140%"></div>
      <div class="txt"><b>Jack's tip:</b> First listen = the <b>big picture</b>. Don't stop the video and don't worry about every word. Second listen = the <b>details</b>. That's when you answer the 🎧 questions.</div>
    </div>
  </div>

  <div class="sec">
    <div class="card sage">
      <b style="color:var(--night)">🔮 Predict before you listen!</b> <span class="small">(no points)</span> Seven of these words are in the episode. One is <b>not</b>. Circle the one you think you <b>won't</b> hear – then check while you listen.
      <div class="chips predict-chips" style="margin-top:2mm;justify-content:center;gap:1.4mm"><span>car park</span><span>detective story</span><span>desert</span><span>bookmark</span><span>sailors</span><span>glasses</span><span>dinosaur</span><span>book club</span></div>
    </div>
  </div>
  {foot(2)}
</section>

<!-- ================= PAGE 3 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">3</span>Know it or hear it? <span class="tag">quiz + listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Circle a, b or c. Questions 🧠 1–5: you can probably answer them <b>before</b> you listen. Questions 🎧 6–10: listen to find the answer.</p>
    </div>
    <img class="char" src="img/f/31-duo-quiz-w.jpg" style="width:36mm;flex:none;margin-top:-2mm">
  </div>
  <div class="small" style="margin:2.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--sage-d)">🧠 YOU MIGHT ALREADY KNOW</div>
  <div class="mc">
    <div class="mcq"><div class="qq">1. "I ______ this book from the library."</div><div class="opt"><span class="c">a</span>lent</div><div class="opt"><span class="c">b</span>borrowed</div><div class="opt"><span class="c">c</span>gave</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">2. "I've been reading this book ______ two weeks."</div><div class="opt"><span class="c">a</span>since</div><div class="opt"><span class="c">b</span>from</div><div class="opt"><span class="c">c</span>for</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">3. "Have you read the new book ______ Jane Smith?"</div><div class="opt"><span class="c">a</span>of</div><div class="opt"><span class="c">b</span>by</div><div class="opt"><span class="c">c</span>from</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">4. "It's a real page-turner." The book is…</div><div class="opt"><span class="c">a</span>very exciting</div><div class="opt"><span class="c">b</span>long and boring</div><div class="opt"><span class="c">c</span>full of pictures</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">5. "No spoilers!" means…</div><div class="opt"><span class="c">a</span>Don't damage the book!</div><div class="opt"><span class="c">b</span>Don't read it too fast!</div><div class="opt"><span class="c">c</span>Don't tell me what happens!</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. How far past her stop did Lucy go?</div><div class="opt"><span class="c">a</span>about ten minutes</div><div class="opt"><span class="c">b</span>about forty minutes</div><div class="opt"><span class="c">c</span>about two hours</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">7. How old was Jack when his grandfather gave him the book?</div><div class="opt"><span class="c">a</span>fifteen</div><div class="opt"><span class="c">b</span>twelve</div><div class="opt"><span class="c">c</span>twenty-two</div><div class="hint">🎧 ⏱ 1:13</div></div>
    <div class="mcq"><div class="qq">8. People who read more than 3.5 hours a week were ___ less likely to die.</div><div class="opt"><span class="c">a</span>3%</div><div class="opt"><span class="c">b</span>17%</div><div class="opt"><span class="c">c</span>23%</div><div class="hint">🎧 ⏱ 2:51</div></div>
    <div class="mcq"><div class="qq">9. Paper was clearly better than screens for…</div><div class="opt"><span class="c">a</span>stories and novels</div><div class="opt"><span class="c">b</span>texts you read to learn</div><div class="opt"><span class="c">c</span>short messages</div><div class="hint">🎧 ⏱ 5:25</div></div>
    <div class="mcq"><div class="qq">10. What did Jack find in the middle of Grandad's book?</div><div class="opt"><span class="c">a</span>an old photo</div><div class="opt"><span class="c">b</span>a leather bookmark</div><div class="opt"><span class="c">c</span>some money</div><div class="hint">🎧 ⏱ 20:30</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">👓</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> Lucy's dad avoided reading for years – then he found out he just needed reading glasses!</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">4</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>Lucy finished her detective story while she waited for the next bus.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>Jack opened his grandfather's book on his fifteenth birthday.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 1:13</td></tr>
      <tr><td class="n">3</td><td>Everyone in the Yale study was over the age of fifty.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:51</td></tr>
      <tr><td class="n">4</td><td>Reading newspapers showed the same strong link as reading books.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:51</td></tr>
      <tr><td class="n">5</td><td>The study proves that reading books makes you live longer.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:51</td></tr>
      <tr><td class="n">6</td><td>Over the years, the advantage of paper seemed to grow.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:25</td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">5</span>Three reading studies 🔍 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Which study is each sentence about? Write <b>A</b>, <b>B</b> or <b>C</b>. ⏱ 2:51 · 5:25 · 7:38</p>
      </div>
      <img class="char" src="img/f/20-jack-glasses-laptop-w.jpg" style="width:16mm;flex:none;margin-top:-4mm">
    </div>
    <div class="studies" style="margin-top:2mm">
      <div style="background:var(--peach-l)"><b class="h" style="color:var(--peach-d)">A · Books and a long life 📚</b>2016 · Bavishi, Slade &amp; Levy, Yale University</div>
      <div style="background:var(--lav)"><b class="h" style="color:var(--mauve-d)">B · Paper or screen? 📱</b>2018 · a team led by Pablo Delgado, Spain</div>
      <div style="background:var(--sage)"><b class="h" style="color:var(--sage-d)">C · The 98% rule 🔢</b>Marcella Hu &amp; Paul Nation, New Zealand</div>
    </div>
    <table class="tf" style="margin-top:1.6mm">
      <tr><td class="n">1</td><td>It combined 54 studies with more than 170,000 people.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">2</td><td>More than 3,500 people over fifty were followed for twelve years.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">3</td><td>Learners read the same story with different amounts of unknown words.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">4</td><td>Book readers lived almost two years longer than non-readers.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">5</td><td>One unknown word in every fifty is comfortable for reading on your own.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">6</td><td>The difference was bigger when people read under time pressure.</td><td class="ck"><span class="box"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">6</span>The 98% rule in numbers <span class="tag">new! do the maths</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 7:38 and ⏱ 19:35 – then do a little maths! Write one number in each gap.</p>
      </div>
      <img class="char" src="img/f/04-jack-thinking-w.jpg" style="width:15mm;flex:none;margin-top:-4mm">
    </div>
    <div class="cov" style="margin-top:1.8mm">
      <div style="background:#DDF1E3"><b style="color:#1E7B45">😊 98% – just right!</b> One unknown word 🟠 in every <span class="blank s"></span> words. <span class="small">(1)</span>{DOTS50}That's about one new word every <span class="blank s"></span> lines. <span class="small">(2)</span></div>
      <div style="background:#FBE1DE"><b style="color:#C0392B">😓 95% – hard work!</b> One unknown word 🟠 in every <span class="blank s"></span> words. <span class="small">(3)</span>{DOTS20}You stop, check the dictionary – and lose the story.</div>
    </div>
    <table class="coll" style="margin-top:1.4mm">
      <tr><td>4. 🔢 A text has 100 words. At 98%, how many words don't you know? <span class="blank s"></span></td></tr>
      <tr><td>5. 🔢 The same 100 words at 95%: how many unknown words? <span class="blank s"></span></td></tr>
      <tr><td>6. 📄 One-page test: more than <span class="blank s"></span> or six unknown words on one page = probably too hard for now.</td></tr>
    </table>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>"It's a real page-turner!" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Jack is in a bookshop, looking for a book to read on holiday. Listen at ⏱ 12:19 and write <b>one word</b> in each gap (1–8). Then answer A and B. The breakdown at ⏱ 13:43 can help.</p>
    </div>
    <img class="char" src="img/f/61-jack-shopping-w.jpg" style="width:17mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat wide" style="margin-top:2mm;gap:.4mm">
{CHAT}
  </div>
  <div class="grid2" style="margin-top:2.6mm;gap:3mm">
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">A.</b> Lucy read the book in <span class="blank" style="min-width:24mm"></span>.</div>
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">B.</b> The book is about two <span class="blank" style="min-width:24mm"></span>.</div>
  </div>

  <div class="sec" style="margin-top:4mm">
    <h2><span class="num">8</span>Phrases to steal <span class="tag">expressions</span><span class="tag pts">4 points</span></h2>
    <p class="instr">Match each phrase from the chat (1–4) to its meaning (a–d). ⏱ 13:43</p>
    <div class="grid2" style="gap:4mm;align-items:start">
      <table class="match" style="font-size:9.2pt">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> "I haven't read a book in ages."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> "It grabs you from the very first page."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> "Fair enough."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> "I can't put it down."</td></tr>
      </table>
      <div class="card" style="font-size:8.9pt;line-height:1.62">
        <b>a)</b> Okay, that's reasonable – I accept that.<br>
        <b>b)</b> I love it so much that I can't stop reading.<br>
        <b>c)</b> It's been a very long time since I read a book.<br>
        <b>d)</b> The story catches your attention immediately.
      </div>
    </div>
  </div>
  <div class="sec">
    <div class="card sage" style="padding:2.4mm 4mm">
      <b style="color:var(--night);font-size:9.6pt">🛍️ Your turn: be the bookseller!</b> <span class="small">(no points) Recommend a book you love to a friend – out loud, in English!</span>
      <div class="chips" style="margin-top:1.4mm;gap:1.4mm"><span>You might like this one.</span><span>It's about…</span><span>It's a real page-turner.</span><span>No spoilers!</span></div>
    </div>
  </div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">9</span>Book idioms <span class="tag">idioms</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">Complete each sentence with a word from the box. ⏱ 14:52 · 16:52</p>
    </div>
    <img class="char" src="img/f/46-lucy-magnifying-glass-w.jpg" style="width:16mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chips" style="margin:1.6mm 0 2mm 10.8mm"><span>book</span><span>bookworm</span><span>cover</span><span>lines</span><span>lost</span><span>open</span></div>
  <table class="coll" style="margin-left:2mm">
    <tr><td>1. 😐 He looks very serious, but he's really funny. Don't judge a book by its <span class="blank s"></span>.</td></tr>
    <tr><td>2. 😢 If I'm upset, everyone can see it. I'm an <span class="blank s"></span> book.</td></tr>
    <tr><td>3. 🤔 She said she was fine, but if you read between the <span class="blank s"></span>, she was worried.</td></tr>
    <tr><td>4. 📋 My manager follows the rules exactly. She does everything by the <span class="blank s"></span>.</td></tr>
    <tr><td>5. 🐛 My sister always has a book in her bag. She's a real <span class="blank s"></span>.</td></tr>
    <tr><td>6. 🍝 I got completely <span class="blank s"></span> in the story and forgot to make dinner!</td></tr>
  </table>
  <div class="bub" style="margin-top:2.2mm">
    <img class="char" src="img/f/02-jack-lightbulb-idea-w.jpg" style="width:17mm;flex:none">
    <div class="txt"><b>Jack's tip:</b> A <b>worm</b> is a long, thin creature that lives in the ground – so a <b>bookworm</b> is like a little creature that lives inside books! 🐛📚 And <i>"Don't judge a book by its cover"</i> is about people too – just like my grandad's very ordinary-looking book.</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">10</span>Borrow or lend? For or since? <span class="tag">new! word pairs</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Tick the right word. ⏱ 17:49</p>
      </div>
      <img class="char" src="img/f/48-lucy-holding-blank-card-w.jpg" style="width:15mm;flex:none;margin-top:-4mm">
    </div>
    <div class="edrule">
      <div style="background:#DCEFF3"><b style="color:#1F5F70">📥 borrow = take</b> (from someone) · <b style="color:#1F5F70">⏳ for</b> + a period: <i>for two weeks</i></div>
      <div style="background:#FDE3D3"><b style="color:#B9542B">📤 lend = give</b> (to someone): <i>Lend me…</i> ✓ <i>Borrow me…</i> ✗ · <b style="color:#B9542B">📍 since</b> + a start: <i>since Monday</i></div>
    </div>
    <div class="grid2" style="gap:2.2mm">{BLS}</div>
  </div>
  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">📄</span>Paper or screen? It depends! <span class="tag fun">think · no points</span></h2>
        <p class="instr" style="margin-bottom:0">Paper helps most with texts you read <b>to learn</b>, or <b>in a hurry</b>. ⏱ 5:25</p>
      </div>
      <img class="char" src="img/f/59-jack-phone-w.jpg" style="width:14mm;flex:none;margin-top:-3mm">
    </div>
    <div style="margin-top:1.6mm">
{PSS}    </div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">11</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 17:49</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "I am reading this book since two weeks."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "I like the history of this book."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "This book is very interesting for me."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "Did you read the book of Jane Smith?"</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "I read it in English and I understood nothing."</td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/07-lucy-great-job-w.jpg" style="width:18mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> <b>History</b> is about real events in the past. For a book or a film, say <b>story</b>: <i>"I love the story of this book."</i> And to <b>follow</b> a story means to understand what's happening.</div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">📄</span>Try the one-page test! <span class="tag fun">read · no points</span></h2>
        <p class="instr" style="margin-bottom:0">This mini-page has exactly <b>100 words</b>. Read it once and <u>underline</u> every word you don't know. Each unknown word = 1%.</p>
      </div>
      <img class="char" src="img/f/34-lucy-shy-but-brave-w.jpg" style="width:15mm;flex:none;margin-top:-3mm">
    </div>
    <div class="story-text" style="margin-top:2mm">{MINI}</div>
    <div style="font-size:9pt;margin-top:1.8mm"><b style="color:var(--night)">Words I didn't know:</b> <span class="blank s"></span> → I know about <span class="blank s"></span> % of the words.</div>
    <div class="meter"><span style="background:#DDF1E3;color:#1E7B45">0–2 unknown: just right! 😊 Keep reading.</span><span style="background:#FDF1D9;color:#9A6A14">3–5: a bit hard 😐 – try a graded reader.</span><span style="background:#FBE1DE;color:#C0392B">6+: too hard for now 😓 – choose an easier book.</span></div>
  </div>

  <div class="sec">
    <div class="card teal" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.6pt">✅ Choosing your next book in English</b> <span class="small">(no points) Tick the ones you'll try!</span>
      <div class="checks" style="margin-top:1.6mm">
        <div><span class="box sm"></span>📄 Do the one-page test first.</div>
        <div><span class="box sm"></span>📘 Try a graded reader at your level.</div>
        <div><span class="box sm"></span>🔁 Read a book you know in your own language.</div>
        <div><span class="box sm"></span>💛 Choose something you <b>want</b> to read.</div>
        <div><span class="box sm"></span>✏️ Underline new words – look up repeats only.</div>
        <div><span class="box sm"></span>👫 Read with a friend – a tiny book club!</div>
      </div>
    </div>
  </div>
  <div class="sec">
    <div class="card white" style="padding:2.6mm 4mm;border:1.6px dashed var(--mauve)">
      <b style="color:var(--night);font-size:9.6pt">⭐ My mini book review</b> <span class="small">(no points) – about a book you've read, in any language!</span>
      <div style="display:grid;grid-template-columns:auto 1fr auto 1fr;gap:1.2mm 3mm;align-items:end;font-size:9pt;margin-top:1.4mm">
        <b style="color:var(--mauve-d)">Title:</b><div class="lines"></div><b style="color:var(--mauve-d)">by</b><div class="lines"></div>
      </div>
      <div style="display:grid;grid-template-columns:auto 1fr;gap:1.2mm 3mm;align-items:end;font-size:9pt">
        <b style="color:var(--mauve-d)">It's about…</b><div class="lines"></div>
        <b style="color:var(--mauve-d)">I'd recommend it to…</b><div class="lines"></div>
      </div>
      <div style="font-size:9pt;margin-top:1.6mm"><b style="color:var(--mauve-d)">My stars:</b> ☆ ☆ ☆ ☆ ☆ &nbsp;·&nbsp; <b style="color:var(--mauve-d)">One word:</b> page-turner · hard to get into · funny · sad · exciting · slow</div>
    </div>
  </div>
  {foot(7)}
</section>

<!-- ================= PAGE 8 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">12</span>Clue word search + secret message <span class="tag">puzzle</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0"><b>Step 1:</b> Complete each clue – the first letter and the number of letters are given (1 point each). <b>Step 2:</b> Find the 10 words in the grid. They go → ↓ ↘ or ↗ and never cross each other.</p>
    </div>
    <img class="char" src="img/f/50-lucy-puzzle-piece-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <div style="display:grid;grid-template-columns:1fr auto;gap:3mm;margin-top:2.2mm;align-items:center">
    <div class="card white clues" style="padding:2.4mm 3mm">
{CLUES}    </div>
    <div>{W.grid_html(ws)}</div>
  </div>
  <div class="card sage" style="margin-top:2.6mm;padding:2.6mm 4mm">
    <b style="color:var(--night)">🤫 Step 3 – the secret message</b> <span class="small">(no points)</span> Cross out the 10 words. Then write the letters that are left, row by row, from left to right. It's the note Jack found in his grandfather's book!
    <div class="msgrow" style="margin-top:2.6mm">{W.message_slots(ws['message'])}</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">13</span>Grandad's book 📕 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 20:30. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/33-jack-blue-scarf-good-morning-w.jpg" style="width:16mm;flex:none;margin-top:-3mm">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">📝</span><span>On the first page, there was a note in Grandad's handwriting.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🎁</span><span>At fifteen, Jack got an old book of short stories from his grandfather.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🌙</span><span>He read the whole book that night – and now he reads a page every day.</span></div>
      <div class="ev"><span class="box"></span><span class="e">📦</span><span>Years later, Jack was packing his books to move house.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🔖</span><span>In the middle, there was a leather bookmark with his name on it.</span></div>
      <div class="ev"><span class="box"></span><span class="e">📚</span><span>He said, "Thanks, Grandad," and put it on a shelf.</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> Grandad said there was "something special" in the book. What do you think it really was?<div class="lines"></div></div>
  </div>
  {foot(8)}
</section>

<!-- ================= PAGE 9 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">14</span>Your turn <span class="tag">writing</span><span class="tag pts">8 points</span></h2>
      <p class="instr" style="margin-bottom:0">2 points for each good sentence.</p>
    </div>
    <img class="char" src="img/f/05-lucy-writing-w.jpg" style="width:17mm;flex:none;margin-top:-3mm">
  </div>
  <div class="grid2" style="margin-top:2.2mm;gap:3mm;align-items:stretch">
    <div class="card" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">A. A book I love 📚</b>
      <div class="small" style="margin-top:1mm">Use <b>page-turner</b>, <b>get lost in</b> or <b>hard to get into</b>. <i>e.g. "I got completely lost in the story – it's a real page-turner."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. My reading plan 🗓️</b>
      <div class="small" style="margin-top:1mm">What will you read in English? When and where? <i>e.g. "I'm going to read ten pages on the bus every morning."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">⏱</span>My one-page-a-day week <span class="tag fun">your 7-day mission</span></h2>
        <p class="instr" style="margin-bottom:0">Read at least one page of a book in English every day. Want more? Ten minutes!</p>
      </div>
      <img class="char" src="img/f/60-lucy-bedtime-w.jpg" style="width:17mm;flex:none">
    </div>
    <table class="log week" style="margin-top:2mm">
      <tr><th>Day</th><th>Pages I read</th><th>One new word I underlined</th><th>Done?</th></tr>
      <tr><td class="d">1</td><td class="a"></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">2</td><td class="a"></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">3</td><td class="a"></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">4</td><td class="a"></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">5</td><td class="a"></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">6</td><td class="a"></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">7</td><td class="a"></td><td></td><td class="c"><span class="box sm"></span></td></tr>
    </table>
    <div class="small" style="margin-top:1.4mm">📖 My book: <span class="blank" style="min-width:70mm"></span> &nbsp; by <span class="blank" style="min-width:45mm"></span></div>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:var(--peach-d)">📚 TALK ABOUT BOOKS</b>It's a real page-turner.<br>I couldn't put it down.<br>It's hard to get into.</div>
        <div><b style="color:var(--mauve-d)">🛍️ IN A BOOKSHOP</b>Could you help me?<br>Have a flick through.<br>No spoilers, please!</div>
        <div><b style="color:var(--sage-d)">📥 BORROW / FOR</b>Can I borrow your book?<br>Could you lend me…?<br>I've been reading it for…</div>
        <div><b style="color:#C0392B">🔢 READ SMART</b>the 98% rule<br>the one-page test<br>one page a day</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain what the twelve-year study found – and why it's a link, not proof.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use the one-page test to choose a book at my level.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use borrow / lend and for / since correctly.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>talk about a book: page-turner, get lost in, hard to get into.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/52-lucy-phone-comment-w.jpg" style="width:19mm;flex:none">
      <div class="txt"><b>Share it with us!</b> Tell us in the comments about a book you love – in English! Is it a <b>page-turner</b>? Did you <b>get lost in it</b>? And have you ever missed your stop because of a book? 🚌📖</div>
    </div>
  </div>
  {foot(9)}
</section>

<!-- ================= PAGE 10 (KEY) ================= -->
<section class="page key">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:2mm">
    <h2><span class="num">✓</span>Answer key</h2>
    <span class="small">Count your points and write your score on page 1!</span>
  </div>
  <div class="keycols">
   <div>
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: b – almost two years longer. · Predict: <b>dinosaur</b> 🦕 isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 c · 2 f · 3 a · 4 h · 5 j · 6 e · 7 i · 8 g · 9 b · 10 d<br>Big idea: a (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 b · 2 c · 3 b · 4 a · 5 c · 6 b · 7 a · 8 c · 9 b · 10 b</p></div>
    <div class="k"><h3>4 · True or false?</h3><p>1 T · 2 F (he didn't open it for years) · 3 T · 4 F (it was books that made the difference) · 5 F (it shows a link, not proof) · 6 T</p></div>
    <div class="k"><h3>5 · Three studies · 6 · The 98% rule</h3><p>5: 1 B · 2 A · 3 C · 4 A · 5 C · 6 B<br>6: 1 fifty · 2 four or five · 3 twenty · 4 two · 5 five · 6 five</p></div>
    <div class="k"><h3>7 · "It's a real page-turner!"</h3><p>1 holiday · 2 ages · 3 desert · 4 turner · 5 into · 6 flick · 7 spoilers · 8 down · A two days · B brothers</p></div>
    <div class="k"><h3>8 · Phrases to steal</h3><p>1 c · 2 d · 3 a · 4 b</p></div>
   </div>
   <div>
    <div class="k"><h3>9 · Book idioms · 10 · Borrow or lend?</h3><p>9: 1 cover · 2 open · 3 lines · 4 book · 5 bookworm · 6 lost<br>10: 1 borrow · 2 lend · 3 borrowed · 4 since · 5 since · 6 for</p></div>
    <div class="k"><h3>11 · Say it better (2 points each)</h3><p>1 I've been reading this book for two weeks. · 2 I like the story of this book. · 3 I find this book really interesting. / This book is really interesting. · 4 Have you read Jane Smith's book? / …the book by Jane Smith? · 5 I read it in English, but I didn't understand much. / I couldn't follow it.</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Word search (1 point per word)</h3><p>{WS_KEY}<br><b>Secret:</b> Read one page a day, and you will never be alone.</p></div>{W.key_svg(ws, 34)}</div>
    <div class="k"><h3>13 · Grandad's book · 14 · Your turn</h3><p>1 🎁 the old book · 2 📚 on a shelf · 3 📦 moving house · 4 📝 the note · 5 🔖 the bookmark · 6 🌙 read it all that night<br><i>Think about it, e.g.:</i> the reading habit he wanted to give Jack.<br><i>Paper or screen?</i> paper: 1, 3, 5 · screen is fine: 2, 4, 6<br>14: your own answers – 2 points per good sentence.</p></div>
    <div class="k"><h3>Your score</h3><p>90–100 🏆 <b>A real bookworm!</b> · 70–89 📖 <b>A page-turner</b> · 50–69 🔖 <b>One page a day</b> · 0–49 🚌 <b>End of the line – listen again!</b></p></div>
   </div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy every week. And remember what Jack's grandad said: one page a day, and you'll never be alone. 📖💜<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
    <img class="char" src="img/f/67-duo-chatting-night.jpg" style="width:40mm">
  </div>
  {foot(10)}
</section>

</body>
</html>
"""
html = head + EXTRA + "</style>\n</head>\n<body>\n" + body
(HERE / "template.html").write_text(html)
pts = [int(x) for x in re.findall(r'tag pts">(\d+) points', html)]
print("points", sum(pts), pts)
