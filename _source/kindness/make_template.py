"""Writes template.html for the kindness worksheet (Podcast 62).
CSS design system copied from being-bored (which includes all earlier worksheets).
Word search from ws.json (built by _source/tools/wordsearch.py). Timestamps: video time = NoteGPT time + 5 s."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import wordsearch as W

src = (HERE.parent / "being-bored" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Being Bored Worksheet", "Kindness Worksheet")
ws = json.loads((HERE / "ws.json").read_text())
W.check(ws)

EXTRA = """
/* ---- new in kindness ---- */
.ws td{width:6.9mm;height:6.9mm;font-size:10pt}
.scale{position:relative;height:14mm;margin:1mm 3mm 0}
.scale .end{position:absolute;top:0;font-size:7.4pt;font-weight:700;color:var(--muted)}
.scale .bar{position:absolute;left:0;right:0;top:5mm;height:2.4mm;border-radius:2mm;background:linear-gradient(90deg,#F6C9C2,#F3EFF8 50%,#BFE3CD)}
.scale .tk{position:absolute;top:8.4mm;transform:translateX(-50%);font-size:7pt;color:var(--muted);font-weight:600}
.scale .mk{position:absolute;top:0;transform:translateX(-50%);text-align:center;font-size:7.2pt;font-weight:700;white-space:nowrap}
.scale .mk span{display:block;width:0;height:0;margin:0 auto;border-left:1.6mm solid transparent;border-right:1.6mm solid transparent;border-top:2.2mm solid currentColor}
.claim.un{background:#DCEFF3;color:#1F5F70;border:1.2px solid #9CCAD6}.claim.un .box{border-color:#1F5F70}
.claim.ov{background:#FDE3D3;color:#B9542B;border:1.2px solid #F2B796}.claim.ov .box{border-color:#B9542B}
.phr{display:grid;grid-template-columns:1.05fr .95fr;gap:4mm;align-items:start}
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
 ("JACK", "44-jack-embarrassed-left", f"Excuse me, sorry to {gap(1)} you. Do you know where the meeting room is? I think I'm on the wrong floor."),
 ("LUCY", "09-lucy-talking-right", f"Oh, you must be new. You're actually on the right floor, it's just hidden at the end of that corridor. Here, I'll {gap(2)} you there."),
 ("JACK", "15-jack-shrug-left", f"Are you sure? I don't want to {gap(3)} up your time."),
 ("LUCY", "38-lucy-explaining-right", f"It's no {gap(4)} at all. I was going that way anyway. Is it your first day?"),
 ("JACK", "13-jack-talking-left", "It is. And I've already got lost twice."),
 ("LUCY", "39-lucy-caring-right", f"Don't worry, everyone does in this building. If you need a {gap(5)} with anything this week, just ask. I'm at the desk by the window."),
 ("JACK", "45-jack-agreeing-left", "That's really kind of you. Thank you so much."),
 ("LUCY", "40-lucy-excited-right", f"Don't {gap(6)} it. And if you want, a few of us have lunch together at one. You're {gap(7)} to join us."),
 ("JACK", "41-jack-laughing-left", f"I'd love to. I {gap(8)} you one."),
 ("LUCY", "12-lucy-laughing-right", "Not at all. Someone did the same for me when I started. Here's the meeting room. Have a great first day."),
])

def pair(i, text, a, b, ca, cb):
    return (f'<div class="sit"><div class="t" style="min-height:0"><b>{i}.</b> {text}</div><div class="ch" style="gap:2mm">'
            f'<span class="claim {ca}"><span class="box"></span>{a}</span>'
            f'<span class="claim {cb}"><span class="box"></span>{b}</span></div></div>')
UO = ["☕ The givers thought: “It's only a drink.” But the strangers felt even better.",
      "📝 “I thought the test would be really hard, but it was easy.”",
      "🚆 “I thought the journey would take one hour. It took three!”",
      "🍝 “I bought food for ten people, but only four came.”"]
UOS = "".join(f'      <div class="tm2" style="grid-template-columns:1fr 32mm 31mm"><span>{i}. {t}</span><span class="claim un"><span class="box"></span>⬇️ underestimated</span><span class="claim ov"><span class="box"></span>⬆️ overestimated</span></div>\n' for i, t in enumerate(UO, 1))

BF = ["🎂 A neighbour helped you move house, so you bake them a cake.",
      "☕ A stranger paid for your coffee, so you pay for the next person's.",
      "🧭 An old man helped Jack, so now Jack helps people who look lost.",
      "🥐 The man from the bakery left Lucy two croissants.",
      "💼 Someone helped Lucy on her first day, so she helps new colleagues.",
      "🍽️ A friend lent you money, so you take them out for dinner."]
BFS = "".join(f'      <div class="tm2" style="grid-template-columns:1fr 21mm 25mm"><span>{i}. {t}</span><span class="claim ov"><span class="box"></span>🔙 back</span><span class="claim ok"><span class="box"></span>⏩ forward</span></div>\n' for i, t in enumerate(BF, 1))

clues = [
 ("COMPLIMENT", "“Your garden looks lovely!” is a {}."),
 ("CROISSANT", "A French pastry – Lucy got two: a {}."),
 ("GENEROUS", "Happy to give money, time or help: {}."),
 ("HOSTEL", "The old man walked Jack to his {}."),
 ("FAVOUR", "“Could you do me a {}?”"),
 ("BREAD", "Lucy paid for a stranger's {}."),
 ("GLOVE", "A little girl ran to give Lucy her {}."),
 ("VISIT", "Jack's grandma: the best present is a {}."),
 ("RINK", "Hot chocolate study: an ice-skating {}."),
 ("DOOR", "Easy kindness: hold the {} for someone."),
]
assert sorted(w for w, _ in clues) == sorted(ws["pos"])
def nw(t):  # keep the letter slots and the punctuation after them on one line
    return re.sub(r"\{\}(\S*)", lambda m: '<span style="white-space:nowrap">{}' + m.group(1) + '</span>', t)
CLUES = "".join(f'      <div><span class="n">{i}</span><span>{nw(t).format(W.slots(w))}</span></div>\n'
                for i, (w, t) in enumerate(clues, 1))
WS_KEY = " · ".join(f"{i} {w.lower()}" for i, (w, _) in enumerate(clues, 1))

def tick(v):
    return f'<div class="tk" style="left:{(v + 5) * 10}%">{"+" if v > 0 else ""}{v}</div>'
SCALE = "".join(tick(v) for v in range(-5, 6))

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
      <h1>Why Small Acts of Kindness Make You Happier</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">A hot chocolate experiment, why spending on others can make you happier, easy English for offering help and saying thank you – and two stories: a bread traffic jam and an old man in the rain.</p>
      <div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div class="hero2">
      <div style="position:absolute;z-index:2;top:3.4mm;left:3.4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">"And his bread too, please!" 🥖</div>
      <img class="char" src="img/f/39-lucy-caring-right-lav.jpg" style="position:absolute;bottom:0;left:3mm;width:35mm">
      <img class="char" src="img/f/16-jack-surprised-left-lav.jpg" style="position:absolute;bottom:0;right:2mm;width:35mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · After you listen 💬</div><div class="s">Find the secret message, try one kind act a day – and tell us a kindness story!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: My kindness check <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Be honest! Tick everything that is true for you. 😊</p>
    <div style="display:grid;grid-template-columns:1.42fr .58fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:1.8mm;justify-content:center;padding:2.6mm 3.6mm">
        <div class="conf" style="grid-template-columns:1fr 1fr;justify-content:stretch;font-size:8.7pt">
          <div><span class="box sm"></span>🚪 I hold doors for people</div>
          <div><span class="box sm"></span>🌷 I say nice things out loud</div>
          <div><span class="box sm"></span>📞 I call older relatives</div>
          <div><span class="box sm"></span>🛍️ I help people with bags</div>
          <div><span class="box sm"></span>⭐ I leave kind comments</div>
          <div><span class="box sm"></span>🙈 I find it hard to accept help</div>
        </div>
        <div style="font-size:9pt"><b style="color:var(--night)">My kindness score:</b> <span class="blank s"></span> / 6</div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> On a cold day, people could keep a hot chocolate or give it to a stranger. How many gave it away?</div>
        <div style="display:flex;gap:3.4mm;font-size:8.7pt;white-space:nowrap"><span><span class="circ">a</span> about 1 in 10</span><span><span class="circ">b</span> about half</span><span><span class="circ">c</span> almost 9 in 10</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 1:48</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:1.8mm 2.4mm;font-size:8.1pt;border:1.2px solid #F4D2C2;line-height:1.36"><b style="color:var(--night)">Jack:</b> "Would <i>you</i> give your hot chocolate away?" ☕</div>
        <img class="char" src="img/f/23-jack-hot-chocolate-peach.jpg" style="width:29mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – or write them in your notebook.</p>
    <div class="grid2" style="gap:2.4mm">
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>1.</b> When was the last time a stranger was kind to you?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>2.</b> What small kind thing could you do today?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>3.</b> Is it easy for you to accept help? Why?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>4.</b> Who do you know with a "heart of gold"?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Then check at ⏱ 12:46 and ⏱ 13:51</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> to underestimate</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> to pay it forward</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> generous</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> considerate</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> to go out of your way</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> to make someone's day</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> a compliment</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> to bother someone</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> a favour</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> selfish</td></tr>
      </table>
      <div class="card" style="font-size:9pt;line-height:1.55">
        <b>a)</b> to make someone very happy, so their whole day feels better<br>
        <b>b)</b> something nice you say about someone<br>
        <b>c)</b> to think something is smaller or less important than it really is<br>
        <b>d)</b> to disturb someone who is busy<br>
        <b>e)</b> happy to give money, time or help to others<br>
        <b>f)</b> only thinking about yourself<br>
        <b>g)</b> to be kind to someone new, after someone was kind to you<br>
        <b>h)</b> something kind you do to help someone<br>
        <b>i)</b> thinking about how your actions affect other people<br>
        <b>j)</b> to make a special effort for someone, even if it's not easy
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/19-lucy-glasses-book-w.jpg" style="width:20mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> <b style="color:var(--peach-d)">GEN</b>-er-ous · con-<b style="color:var(--peach-d)">SID</b>-er-ate · <b style="color:var(--peach-d)">COM</b>-pli-ment · un-der-<b style="color:var(--peach-d)">ES</b>-ti-mate · <b style="color:var(--peach-d)">FA</b>-vour. Careful: <b>compliment</b> (nice words) sounds just like <b>complement</b>, but it's spelled with an <b>i</b>! Say it: <i>"You made my day!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>Kindness only matters when it's big and expensive, like a special present.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>Small acts of kindness mean more to other people than we think – and they make us happier too.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>It's better not to help strangers, because it always feels awkward.</div>
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
      <div class="chips predict-chips" style="margin-top:2mm;justify-content:center;gap:1.4mm"><span>hot chocolate</span><span>croissants</span><span>glove</span><span>clock tower</span><span>envelope</span><span>ice rink</span><span>taxi</span><span>little dog</span></div>
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
    <div class="mcq"><div class="qq">1. Someone says "Thank you!" A natural reply is…</div><div class="opt"><span class="c">a</span>"Nothing."</div><div class="opt"><span class="c">b</span>"Don't mention it."</div><div class="opt"><span class="c">c</span>"No, thanks."</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">2. "She's always very kind ______ me."</div><div class="opt"><span class="c">a</span>with</div><div class="opt"><span class="c">b</span>at</div><div class="opt"><span class="c">c</span>to</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">3. "Could you ______ me a favour?"</div><div class="opt"><span class="c">a</span>make</div><div class="opt"><span class="c">b</span>do</div><div class="opt"><span class="c">c</span>give</div><div class="hint">🧠 Make or do?</div></div>
    <div class="mcq"><div class="qq">4. "Thank you for ______ me."</div><div class="opt"><span class="c">a</span>help</div><div class="opt"><span class="c">b</span>to help</div><div class="opt"><span class="c">c</span>helping</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">5. "Do you need a hand?" means…</div><div class="opt"><span class="c">a</span>Do you need some help?</div><div class="opt"><span class="c">b</span>Is your hand hurt?</div><div class="opt"><span class="c">c</span>Do you want to hold hands?</div><div class="hint">🧠 Everyday English</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. What did the man behind Lucy want to buy?</div><div class="opt"><span class="c">a</span>one loaf of bread</div><div class="opt"><span class="c">b</span>two croissants</div><div class="opt"><span class="c">c</span>a birthday cake</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">7. How many of the 84 people gave their hot chocolate away?</div><div class="opt"><span class="c">a</span>fifteen</div><div class="opt"><span class="c">b</span>seventy-five</div><div class="opt"><span class="c">c</span>all eighty-four</div><div class="hint">🎧 ⏱ 1:48</div></div>
    <div class="mcq"><div class="qq">8. In the money experiment, what was in the envelope?</div><div class="opt"><span class="c">a</span>five or twenty dollars</div><div class="opt"><span class="c">b</span>fifty dollars</div><div class="opt"><span class="c">c</span>a gift card</div><div class="hint">🎧 ⏱ 5:38</div></div>
    <div class="mcq"><div class="qq">9. What does Jack's grandmother say is the best present?</div><div class="opt"><span class="c">a</span>flowers</div><div class="opt"><span class="c">b</span>a visit</div><div class="opt"><span class="c">c</span>chocolate</div><div class="hint">🎧 ⏱ 8:54</div></div>
    <div class="mcq"><div class="qq">10. What did the man from the bakery leave for Lucy?</div><div class="opt"><span class="c">a</span>a loaf of bread</div><div class="opt"><span class="c">b</span>the money back</div><div class="opt"><span class="c">c</span>two croissants and a note</div><div class="hint">🎧 ⏱ 20:57</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🧤</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> When Lucy dropped her glove, a little girl ran about fifty metres to give it back – her mum was behind her, out of breath!</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">4</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>The man in the bakery was happy to let Lucy pay for his bread.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>The givers thought their hot chocolate was "nothing special".</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 1:48</td></tr>
      <tr><td class="n">3</td><td>People who received a kind act were less generous with the next person.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 4:37</td></tr>
      <tr><td class="n">4</td><td>In the money experiment, twenty dollars made people much happier than five.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:38</td></tr>
      <tr><td class="n">5</td><td>The Oxford review found that kindness makes people a bit happier.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 7:09</td></tr>
      <tr><td class="n">6</td><td>Kindness to others can replace proper help if you feel low for a long time.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 7:09</td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">5</span>Two studies and a review 🔍 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Which one is each sentence about? Write <b>A</b>, <b>B</b> or <b>C</b>. ⏱ 1:48 · 5:38 · 7:09</p>
      </div>
      <img class="char" src="img/f/46-lucy-magnifying-glass-w.jpg" style="width:16mm;flex:none;margin-top:-4mm">
    </div>
    <div class="studies" style="margin-top:2mm">
      <div style="background:var(--peach-l)"><b class="h" style="color:var(--peach-d)">A · Hot chocolate ☕</b>2022 · Amit Kumar &amp; Nicholas Epley · a park in Chicago</div>
      <div style="background:var(--lav)"><b class="h" style="color:var(--mauve-d)">B · Spending on others 💵</b>2008 · Elizabeth Dunn, Lara Aknin &amp; Michael Norton</div>
      <div style="background:var(--sage)"><b class="h" style="color:var(--sage-d)">C · The big review 📚</b>2018 · a team at the University of Oxford</div>
    </div>
    <table class="tf" style="margin-top:1.6mm">
      <tr><td class="n">1</td><td>People got an envelope with five or twenty dollars inside.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">2</td><td>People could keep a warm drink or give it to a stranger.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">3</td><td>It looked at 27 studies with more than 4,000 people.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">4</td><td>The receivers felt better than the givers expected.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">5</td><td>The effect on happiness was "small to medium".</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">6</td><td>More than 600 Americans answered questions about how they spend their money.</td><td class="ck"><span class="box"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">6</span>Guess vs reality <span class="tag">new! under or over?</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0"><b>A.</b> Listen at ⏱ 1:48 and write the two numbers (1 point each). <b>B.</b> Underestimated or overestimated? Tick one (1 point each).</p>
      </div>
      <img class="char" src="img/f/04-jack-thinking-w.jpg" style="width:15mm;flex:none;margin-top:-4mm">
    </div>
    <div class="card white" style="margin-top:1.8mm;padding:1.4mm 4mm 2mm">
      <div class="scale"><div class="bar"></div>{SCALE}<div class="end" style="left:0">😞 much worse</div><div class="end" style="right:0">much better 😄</div></div>
      <div style="display:flex;justify-content:space-around;font-size:9.1pt;margin-top:.6mm"><span>🤔 The givers guessed: <b>+</b><span class="blank s"></span></span><span>😊 The receivers felt: <b>+</b><span class="blank s"></span></span></div>
      <div class="small" style="text-align:center;margin-top:1mm">Bonus: draw 🤔 and 😊 arrows on the scale!</div>
    </div>
    <div style="margin-top:1.6mm">
{UOS}    </div>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>"Here, I'll walk you there" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">It's Jack's first day at a new job, and he's a bit lost. Listen at ⏱ 11:21 and write <b>one word</b> in each gap (1–8). Then answer A and B. The breakdown at ⏱ 12:46 can help.</p>
    </div>
    <img class="char" src="img/f/32-lucy-coffee-chat-right-w.jpg" style="width:19mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat wide" style="margin-top:2.4mm;gap:.9mm">
{CHAT}
  </div>
  <div class="grid2" style="margin-top:2.6mm;gap:3mm">
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">A.</b> They have lunch together at <span class="blank" style="min-width:20mm"></span>.</div>
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">B.</b> Lucy's last line is paying it <span class="blank" style="min-width:22mm"></span>.</div>
  </div>

  <div class="sec" style="margin-top:4mm">
    <h2><span class="num">8</span>Phrases to steal <span class="tag">expressions</span><span class="tag pts">4 points</span></h2>
    <p class="instr">Match each phrase from the chat (1–4) to its meaning (a–d). ⏱ 12:46</p>
    <div class="grid2" style="gap:4mm;align-items:start">
      <table class="match" style="font-size:9.2pt">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> "I'll walk you there."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> "If you need a hand…"</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> "You're welcome to join us."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> "I owe you one."</td></tr>
      </table>
      <div class="card" style="font-size:8.9pt;line-height:1.62">
        <b>a)</b> We'd be happy if you came.<br>
        <b>b)</b> You helped me – I'll help you one day.<br>
        <b>c)</b> I'll go with you to show you the way.<br>
        <b>d)</b> If you need some help…
      </div>
    </div>
  </div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">9</span>Make or do? <span class="tag">new! collocations</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">Write the right form of <b>make</b> or <b>do</b>. ⏱ 16:00 · 16:43</p>
    </div>
    <img class="char" src="img/f/47-jack-pointing-right-w.jpg" style="width:17mm;flex:none;margin-top:-3mm">
  </div>
  <div class="grid2" style="margin-top:2mm;gap:3mm">
    <table class="coll">
      <tr><td>1. 🙏 Could you <span class="blank s"></span> me a favour?</td></tr>
      <tr><td>2. 💌 Your message really <span class="blank s"></span> my day!</td></tr>
      <tr><td>3. 🌱 Small kind acts can <span class="blank s"></span> a big difference.</td></tr>
    </table>
    <table class="coll">
      <tr><td>4. 🌷 I want to <span class="blank s"></span> something nice for people.</td></tr>
      <tr><td>5. 🌧️ He <span class="blank s"></span> a real effort to help me.</td></tr>
      <tr><td>6. 🚶 A short walk will <span class="blank s"></span> you good.</td></tr>
    </table>
  </div>
  <div class="bub" style="margin-top:2.2mm">
    <img class="char" src="img/f/02-jack-lightbulb-idea-w.jpg" style="width:17mm;flex:none">
    <div class="txt"><b>Jack's tip:</b> <b>Do</b> is for actions and help: <i>do a favour, do good, do your best.</i> <b>Make</b> is for results – something new happens: <i>make a difference, make an effort, make someone's day.</i> Learn them as pairs! 🧩</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">10</span>Your kindness phrasebook <span class="tag">new! offers &amp; replies</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">What do you say? Match each situation (1–6) to a phrase (a–f). ⏱ 18:12</p>
      </div>
      <img class="char" src="img/f/61-jack-shopping-w.jpg" style="width:17mm;flex:none;margin-top:-3mm">
    </div>
    <div class="phr" style="margin-top:2mm">
      <table class="match" style="font-size:9pt">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> 🧳 A woman is carrying a heavy suitcase up the stairs.</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> 🤳 Two tourists are trying to take a selfie.</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> 🛍️ A man with full arms is walking to a door.</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> 😊 Someone says, "Thanks so much!"</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> 🙂 Someone offers to help you, but you're fine.</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> 💺 Someone gives you their seat on the bus.</td></tr>
      </table>
      <div class="card" style="font-size:9pt;line-height:1.75">
        <b>a)</b> "Let me get the door for you."<br>
        <b>b)</b> "No thanks, I can manage – but thank you!"<br>
        <b>c)</b> "Do you need a hand with that?"<br>
        <b>d)</b> "Thank you, that's really kind of you."<br>
        <b>e)</b> "Would you like me to take a photo for you?"<br>
        <b>f)</b> "Any time!"
      </div>
    </div>
    <div class="bub" style="margin-top:2.2mm">
      <img class="char" src="img/f/01-lucy-thumbs-up-w.jpg" style="width:16mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> If someone says <i>"No, thanks"</i>, that's fine! Just smile and say <b>"No problem."</b> You haven't done anything wrong. And remember: accepting kindness well is a gift too. 🎁</div>
    </div>
  </div>
  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">🔁</span>Paid it back or paid it forward? <span class="tag fun">think · no points</span></h2>
        <p class="instr" style="margin-bottom:0"><b>Back</b> = you're kind to the same person who helped you. <b>Forward</b> = you're kind to someone new. ⏱ 4:37 · 20:57</p>
      </div>
      <img class="char" src="img/f/69-duo-thumbs-up-w.jpg" style="width:24mm;flex:none;margin-top:-3mm">
    </div>
    <div style="margin-top:1.6mm">
{BFS}    </div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">11</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 16:43</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "Thank you!" – "Nothing."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "She is very kind with me."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "Can I help to you?"</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "Thank you for your help me."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "You are very kind person."</td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/07-lucy-great-job-w.jpg" style="width:18mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> <b>Polite</b> is about good manners. <b>Kind</b> is about a good heart – so it's usually warmer! And after <b>for</b>, use a noun or <b>-ing</b>: <i>"Thank you for your help." / "Thank you for helping me."</i></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">💛</span>Kind sayings <span class="tag fun">match · no points</span></h2>
        <p class="instr" style="margin-bottom:0">Match each saying (1–4) to its meaning (a–d). ⏱ 7:09 · 16:00</p>
      </div>
      <img class="char" src="img/f/34-lucy-shy-but-brave-w.jpg" style="width:16mm;flex:none;margin-top:-3mm">
    </div>
    <div class="grid2" style="gap:4mm;align-items:start;margin-top:2mm">
      <table class="match" style="font-size:9.1pt">
        <tr><td class="ans"><span class="box sm"></span></td><td><b style="color:var(--night)">1.</b> "She's got a heart of gold."</td></tr>
        <tr><td class="ans"><span class="box sm"></span></td><td><b style="color:var(--night)">2.</b> "A little goes a long way."</td></tr>
        <tr><td class="ans"><span class="box sm"></span></td><td><b style="color:var(--night)">3.</b> "You can't pour from an empty cup."</td></tr>
        <tr><td class="ans"><span class="box sm"></span></td><td><b style="color:var(--night)">4.</b> "He paid it back twice over."</td></tr>
      </table>
      <div class="card" style="font-size:8.9pt;line-height:1.6">
        <b>a)</b> Look after yourself too – then you can help others.<br>
        <b>b)</b> He gave back more than he got.<br>
        <b>c)</b> She's a very kind and good person.<br>
        <b>d)</b> A small amount can have a big effect.
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="card teal" style="padding:2.8mm 4mm">
      <b style="color:var(--night);font-size:9.6pt">💌 Make someone's day – right now!</b> <span class="small">(no points)</span>
      <div style="font-size:9pt;margin-top:1mm">Jack's idea: send a short message to a friend you haven't spoken to for a while. Write it here in English first – then send it!</div>
      <div style="display:grid;grid-template-columns:auto 1fr;gap:0 3mm;align-items:end;font-size:9pt;margin-top:1mm">
        <b style="color:var(--mauve-d)">To:</b><div class="lines"></div>
        <b style="color:var(--mauve-d)">Message:</b><div class="lines"></div>
        <span></span><div class="lines"></div>
      </div>
      <div class="small" style="margin-top:1.4mm">💡 Ideas: <i>"I was thinking about you today. How are you?" · "Your photos always make my day!" · "Thanks for helping me last week – I owe you one!"</i></div>
    </div>
  </div>
  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">🌷</span>Say the nice thing! <span class="tag fun">write · no points</span></h2>
        <p class="instr" style="margin-bottom:0">Jack's tip: don't just <i>think</i> the nice thing – say it! Write a compliment for each person. ⏱ 8:54</p>
      </div>
      <img class="char" src="img/f/55-jack-thumbs-up-w.jpg" style="width:16mm;flex:none;margin-top:-3mm">
    </div>
    <table class="friend" style="margin-top:1.4mm">
      <tr><td class="i" style="color:var(--night);width:44%">🍝 Your friend cooked dinner for you.</td><td>💬 <i>"This is delicious – you're a great cook!"</i></td></tr>
      <tr><td class="i" style="color:var(--night);width:44%">🎤 A colleague gave a great presentation.</td><td>💬 <span class="blank l" style="min-width:88mm"></span></td></tr>
      <tr><td class="i" style="color:var(--night);width:44%">🌻 Your neighbour's garden looks beautiful.</td><td>💬 <span class="blank l" style="min-width:88mm"></span></td></tr>
      <tr><td class="i" style="color:var(--night);width:44%">✂️ Your friend has a new haircut.</td><td>💬 <span class="blank l" style="min-width:88mm"></span></td></tr>
    </table>
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
    <b style="color:var(--night)">🤫 Step 3 – the secret message</b> <span class="small">(no points)</span> Cross out the 10 words. Then write the letters that are left, row by row, from left to right. It's Lucy's last piece of advice in the episode!
    <div class="msgrow" style="margin-top:2.6mm">{W.message_slots(ws['message'])}</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">13</span>The old man in the rain ☔ <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 19:05. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/25-jack-rain-umbrella-w.jpg" style="width:16mm;flex:none;margin-top:-3mm">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">🕰️</span><span>Jack remembered a clock tower with a green roof.</span></div>
      <div class="ev"><span class="box"></span><span class="e">👴</span><span>An old man asked, "Are you lost, son?"</span></div>
      <div class="ev"><span class="box"></span><span class="e">🎒</span><span>At nineteen, Jack travelled alone to a city in the north.</span></div>
      <div class="ev"><span class="box"></span><span class="e">💬</span><span>"One day, you'll do the same for somebody."</span></div>
      <div class="ev"><span class="box"></span><span class="e">📄</span><span>His phone was dead – and he lost the paper with the address.</span></div>
      <div class="ev"><span class="box"></span><span class="e">☔</span><span>They walked together in the rain for about 25 minutes.</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> How does Jack pay it forward today? Write two examples.<div class="lines"></div><div class="lines"></div></div>
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
      <b style="color:var(--night);font-size:9.2pt">A. A stranger was kind to me 💛</b>
      <div class="small" style="margin-top:1mm">What happened? Use <b>go out of their way</b> or <b>make my day</b>. <i>e.g. "A man went out of his way to help me find the station."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. My kindness plan 🌱</b>
      <div class="small" style="margin-top:1mm">What small kind things will you do this week? <i>e.g. "On Friday, I'm going to call my grandmother."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">⏱</span>My kindness week <span class="tag fun">your 7-day mission</span></h2>
        <p class="instr" style="margin-bottom:0">One small act of kindness every day – and use one English phrase if you can!</p>
      </div>
      <img class="char" src="img/f/35-jack-reading-card-w.jpg" style="width:16mm;flex:none">
    </div>
    <table class="log week" style="margin-top:2mm">
      <tr><th>Day</th><th>Small act</th><th>What happened? How did it feel?</th><th>Done?</th></tr>
      <tr><td class="d">1</td><td class="a">🚪 hold a door: "After you."</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">2</td><td class="a">💬 message an old friend</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">3</td><td class="a">🌷 say a nice thing out loud</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">4</td><td class="a">🛍️ "Do you need a hand?"</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">5</td><td class="a">📞 call an older relative</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">6</td><td class="a">⭐ leave a kind comment</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">7</td><td class="a">🎁 accept help: "That's kind!"</td><td></td><td class="c"><span class="box sm"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:var(--sage-d)">🤝 OFFER HELP</b>Do you need a hand?<br>Can I help you with that?<br>Would you like me to…?</div>
        <div><b style="color:var(--peach-d)">🙏 SAY THANKS</b>Thank you so much!<br>That's really kind of you.<br>I owe you one.</div>
        <div><b style="color:var(--mauve-d)">😊 REPLY</b>You're welcome.<br>No problem. / Any time!<br>Don't mention it.</div>
        <div><b style="color:#C0392B">💛 KIND WORDS</b>You made my day!<br>You've got a heart of gold.<br>A little goes a long way.</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain why we underestimate our own kindness.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>offer help in English: "Do you need a hand?"</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>reply to "thank you" in four different ways.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use do a favour, make a difference and make someone's day.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/52-lucy-phone-comment-w.jpg" style="width:19mm;flex:none">
      <div class="txt"><b>Share it with us!</b> Tell us in the comments about a stranger who was kind to you – or something kind you did this week. Did someone <b>go out of their way</b> for you? Did someone <b>make your day</b>? Your comment might make someone else's day too! 💛</div>
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
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: c – 75 out of 84 people gave it away. · Predict: <b>taxi</b> 🚕 isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 c · 2 g · 3 e · 4 i · 5 j · 6 a · 7 b · 8 d · 9 h · 10 f<br>Big idea: b (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 b · 2 c · 3 b · 4 c · 5 a · 6 a · 7 b · 8 a · 9 b · 10 c</p></div>
    <div class="k"><h3>4 · True or false?</h3><p>1 F (he said "I can pay!" and left quickly) · 2 T · 3 F (they were more generous) · 4 F (the amount wasn't important) · 5 T · 6 F (talk to a doctor)</p></div>
    <div class="k"><h3>5 · Two studies and a review · 6 · Guess vs reality</h3><p>5: 1 B · 2 A · 3 C · 4 A · 5 C · 6 B<br>6A: givers guessed +2.7 · receivers felt +3.5<br>6B: 1 underestimated · 2 overestimated · 3 underestimated · 4 overestimated</p></div>
    <div class="k"><h3>7 · "Here, I'll walk you there"</h3><p>1 bother · 2 walk · 3 take · 4 trouble · 5 hand · 6 mention · 7 welcome · 8 owe · A one (o'clock) · B forward</p></div>
    <div class="k"><h3>8 · Phrases to steal · Back or forward?</h3><p>8: 1 c · 2 d · 3 a · 4 b<br><i>Back or forward?</i> 1 back · 2 forward · 3 forward · 4 back · 5 forward · 6 back</p></div>
   </div>
   <div>
    <div class="k"><h3>9 · Make or do? · 10 · Phrasebook</h3><p>9: 1 do · 2 made · 3 make · 4 do · 5 made · 6 do<br>10: 1 c · 2 e · 3 a · 4 f · 5 b · 6 d</p></div>
    <div class="k"><h3>11 · Say it better (2 points each)</h3><p>1 You're welcome. / No problem. / Don't mention it. · 2 She's very kind to me. · 3 Can I help you? / Do you need a hand with that? · 4 Thank you for your help. / Thank you for helping me. · 5 You're a very kind person.<br><i>Kind sayings:</i> 1 c · 2 d · 3 a · 4 b</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Word search (1 point per word)</h3><p>{WS_KEY}<br><b>Secret:</b> Kindness is one of the few things in life that grows when you give it away.</p></div>{W.key_svg(ws, 36)}</div>
    <div class="k"><h3>13 · The old man · 14 · Your turn</h3><p>1 🎒 travelled alone · 2 📄 lost the paper · 3 👴 "Are you lost, son?" · 4 🕰️ clock tower · 5 ☔ walked in the rain · 6 💬 "One day, you'll do the same"<br><i>Think about it:</i> he always stops to help people who look lost – to find train stations, hospitals, even a little dog's owner.<br>14: your own answers – 2 points per good sentence.</p></div>
    <div class="k"><h3>Your score</h3><p>90–100 🏆 <b>A heart of gold!</b> · 70–89 ✨ <b>You made my day</b> · 50–69 🥐 <b>Paying it forward</b> · 0–49 🥖 <b>Bread traffic jam – listen again!</b></p></div>
   </div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy every week. And maybe send this worksheet to a friend who's learning English – that's a small act of kindness too! 💛<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
    <img class="char" src="img/f/29-duo-high-five-night.jpg" style="width:38mm">
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
