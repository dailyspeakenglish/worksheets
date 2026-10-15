"""Writes template.html for the why-we-laugh worksheet (Podcast 58).
CSS design system copied from time-flies (which includes build-a-habit's); word search from ws.json."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import wordsearch as W

src = (HERE.parent / "time-flies" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Time Flies Worksheet", "Why We Laugh Worksheet")
ws = json.loads((HERE / "ws.json").read_text())
W.check(ws)

EXTRA = """
/* ---- new in why-we-laugh ---- */
.meter{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-radius:4mm;overflow:hidden;border:1.3px solid var(--lav2)}
.meter .z{padding:2.4mm 2.6mm;text-align:center;min-height:30mm;display:flex;flex-direction:column;gap:1.6mm;align-items:center}
.meter .z .h{font-weight:800;font-size:10pt}
.meter .z .s{font-size:7.6pt;line-height:1.3}
.meter .z .slots{display:flex;gap:2mm}
.meter .z1{background:#EAF3EC;color:var(--sage-d)}
.meter .z2{background:#FDEDE5;color:var(--peach-d)}
.meter .z3{background:#F6DCDC;color:#A33B3B}
.meterbar{height:3mm;border-radius:2mm;background:linear-gradient(90deg,#B9D3C4,#F2AE94,#E07B7B);margin:1.4mm 0 .6mm}
.nums2{display:grid;grid-template-columns:1fr auto;gap:1.2mm 3mm;font-size:9.2pt;align-items:center}
.nums2 .bx{display:inline-block;width:8mm;height:6.4mm;border:1.4px solid var(--night);border-radius:1.4mm;background:var(--lav)}
.mix{display:grid;grid-template-columns:1fr 1fr;gap:2mm 3mm;font-size:9.2pt}
.mix div{background:#fff;border:1.2px solid var(--line);border-radius:2.6mm;padding:1.8mm 3mm;line-height:1.5}
.mix .w{display:inline-flex;gap:1.6mm;margin-left:1mm}
.mix .w span{border:1.2px solid var(--night);border-radius:10mm;padding:0 2.4mm;font-weight:600;font-size:8.6pt}
.tone{display:inline-flex;align-items:center;gap:1.2mm;padding:.5mm 2.2mm .5mm 1mm;border-radius:10mm;font-size:7.6pt;font-weight:700;white-space:nowrap}
.tone.sin{background:#DDF1E3;color:#1E7B45;border:1.2px solid #8FCBA3}
.tone.sar{background:#EDE3FA;color:#5B3A99;border:1.2px solid #B9A3E0}
.tone .box{width:4.2mm;height:4.2mm;border-radius:1mm;border-width:1.2px}
.tone.sin .box{border-color:#1E7B45}.tone.sar .box{border-color:#5B3A99}
.sar .sit .t{min-height:0}
.log th{background:var(--night);color:#F8E3C4;font-size:8.2pt;font-weight:600;padding:1.8mm 2mm;text-align:left}
.log th:first-child{border-radius:3mm 0 0 0}.log th:last-child{border-radius:0 3mm 0 0;text-align:center}
.log td{border:1px solid #E6DFEE;height:7mm;font-size:8.4pt;padding:0 2mm;vertical-align:middle}
.log td.d{font-weight:700;color:var(--night);background:var(--lav);width:12mm;text-align:center}
.log td.c{text-align:center;width:34mm;font-size:8pt;color:var(--muted)}
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
 ("LUCY", "09-lucy-talking-right", f"You look very {gap(1)} today. What happened?"),
 ("JACK", "43-jack-explaining-left", "Oh, I have to tell you. Yesterday, in our big meeting, my boss was giving a really serious presentation about money."),
 ("LUCY", "37-lucy-thinking-right", "Okay…"),
 ("JACK", "13-jack-talking-left", f"And halfway through, his phone started ringing really loudly. And his ringtone was a {gap(2)}. Just a duck, quacking."),
 ("LUCY", "36-lucy-surprised-right", f"No {gap(3)}! What did everyone do?"),
 ("JACK", "44-jack-embarrassed-left", f"At first, total silence. Everyone was trying to keep a straight {gap(4)}. And then the new intern started {gap(5)}, and that was it. The whole room burst out laughing."),
 ("LUCY", "11-lucy-asking-right", "Even your boss?"),
 ("JACK", "41-jack-laughing-left", f"He was in {gap(6)}. He couldn't finish his sentence for about two minutes. Honestly, I haven't laughed like that for ages."),
 ("LUCY", "12-lucy-laughing-right", f"That's hilarious. I'm {gap(7)} up just imagining it."),
 ("JACK", "16-jack-surprised-left", f"You had to be {gap(8)}, really. But it was the best meeting we've ever had."),
])

clues = [
 ("CONTAGIOUS", "Laughter is {}: it spreads from person to person."),
 ("HILARIOUS", "Extremely funny: “That video was {}!”"),
 ("STITCHES", "Jack's boss was in {} – he couldn't stop laughing."),
 ("CHUCKLE", "Older people often {} – a quiet, warm laugh."),
 ("SARCASM", "“Lovely weather!” when it's pouring with rain is {}."),
 ("GIGGLE", "Children often {} at the back of the classroom."),
 ("SITCOM", "A funny TV series about the same people at home or at work: a {}."),
 ("PIGEON", "A {} flew into Lucy's classroom and walked across her papers."),
 ("POISON", "In France, Lucy asked the waiter for {} instead of fish!"),
 ("RINGTONE", "In the meeting, the boss's phone {} played really loudly."),
 ("DUCK", "Quack, quack! The ringtone was a {}."),
]
assert sorted(w for w, _ in clues) == sorted(ws["pos"])
CLUES = "".join(f'      <div><span class="n">{i}</span><span>{t.format(W.slots(w))}</span></div>\n'
                for i, (w, t) in enumerate(clues, 1))

SAR = [
 ("🌧️", "It's pouring with rain. Your friend says:", "“Lovely weather today!”"),
 ("🚗", "Your friend has just passed her driving test. You say:", "“Well done! I'm so proud of you!”"),
 ("🥪", "Your colleague drops his whole lunch on the floor. He says:", "“Well, that went well.”"),
 ("📰", "Your colleague is relaxing with a coffee and a newspaper. Someone says:", "“Wow, you look really busy!”"),
 ("☀️", "The sun is shining and it's warm. Your neighbour says:", "“Lovely weather today!”"),
 ("🍝", "Your friend cooks you a delicious dinner. You say:", "“This is amazing – thank you!”"),
]
SAR_KEY = "1 sarcastic · 2 sincere · 3 sarcastic · 4 sarcastic · 5 sincere · 6 sincere"
SARC = "".join(f'<div class="sit"><div class="t"><b>{i}.</b> {e} {s}<br><b style="color:var(--night)">{q}</b></div><div class="ch" style="gap:2mm"><span class="tone sin"><span class="box"></span>😊 SINCERE</span><span class="tone sar"><span class="box"></span>😏 SARCASTIC</span></div></div>'
               for i, (e, s, q) in enumerate(SAR, 1))

body = f"""
<!-- ================= PAGE 1 ================= -->
<section class="page">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:1mm">
    <div class="brand"><img src="img/logo.jpg">DAILY SPEAK ENGLISH · PODCAST WORKSHEET</div>
    <div><span class="pill">B1–B2</span> <span class="pill p">⏱ 50 min</span></div>
  </div>
  <div style="display:grid;grid-template-columns:1.12fr .88fr;gap:4mm;margin-top:5mm;align-items:center">
    <div>
      <div class="small" style="font-weight:700;color:var(--mauve);letter-spacing:.7pt">LISTEN · LEARN · SPEAK</div>
      <h1>Why We Laugh (It's Not Because of Jokes)</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">What really makes us laugh, what laughing does to your body, how to spot sarcasm – lots of funny English – and the story of a very confident pigeon.</p>
      <div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div style="background:var(--lav);border-radius:6mm;height:60mm;position:relative;overflow:hidden;border:1px solid var(--lav2)">
      <div style="position:absolute;z-index:2;top:3.4mm;left:4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">Ha ha! 😂</div>
      <img class="char" src="img/f/66-duo-podcast-lav.jpg" style="position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:66mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · After you listen 💬</div><div class="s">Spot the sarcasm, solve the word search and share your funniest English moment!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: My laugh check <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Think about yesterday. Where did you laugh the most? Tick all that are true.</p>
    <div style="display:grid;grid-template-columns:1.3fr .7fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:2mm;justify-content:center">
        <div class="conf" style="grid-template-columns:1fr 1fr;justify-content:stretch">
          <div><span class="box sm"></span>👫 with friends</div>
          <div><span class="box sm"></span>🏠 with my family</div>
          <div><span class="box sm"></span>📱 watching videos alone</div>
          <div><span class="box sm"></span>💼 at work or school</div>
          <div><span class="box sm"></span>💬 reading messages</div>
          <div><span class="box sm"></span>🙈 at my own mistake</div>
        </div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> A scientist listened to people laughing in cafés and shops. How many laughs came after something like a <b>joke</b>?</div>
        <div style="display:flex;gap:4mm;font-size:8.9pt;flex-wrap:wrap"><span><span class="circ">a</span> about 70%</span><span><span class="circ">b</span> about 40%</span><span><span class="circ">c</span> only 10–20%</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 0:05</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:2mm 2.8mm;font-size:8.5pt;border:1.2px solid #F4D2C2;line-height:1.4"><b style="color:var(--night)">Jack:</b> "With my brother, we laugh at almost nothing. A stranger would think we were mad!" 😆</div>
        <img class="char" src="img/f/41-jack-laughing-left-peach.jpg" style="width:30mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – or write them in your notebook.</p>
    <div class="grid2" style="gap:3mm">
      <div class="card teal"><b>1.</b> Who makes you laugh the most? Why?</div>
      <div class="card teal"><b>2.</b> What was the last thing that made you really laugh?</div>
      <div class="card teal"><b>3.</b> Do you understand jokes in English? What's hard about them?</div>
      <div class="card teal"><b>4.</b> Have you ever made a funny mistake in another language?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Check in the Word Tour at ⏱ 14:16</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> contagious</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> to giggle</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> to chuckle</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> to be in stitches</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> to keep a straight face</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> hilarious</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> to burst out laughing</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> to pull someone's leg</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> to get (a joke)</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> a sitcom</td></tr>
      </table>
      <div class="card" style="font-size:9.1pt;line-height:1.62">
        <b>a)</b> to understand a joke<br>
        <b>b)</b> spreading easily from one person to another<br>
        <b>c)</b> to laugh quietly, usually to yourself<br>
        <b>d)</b> extremely funny<br>
        <b>e)</b> to suddenly start laughing loudly<br>
        <b>f)</b> to joke by telling someone something that isn't true<br>
        <b>g)</b> to laugh in a light, high, often silly way<br>
        <b>h)</b> a funny TV series about the same characters in everyday situations<br>
        <b>i)</b> to laugh so much that it almost hurts<br>
        <b>j)</b> to not laugh or smile, even when something is funny
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/38-lucy-explaining-right-w.jpg" style="width:24mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> hi-<b style="color:var(--peach-d)">LAIR</b>-ee-us · con-<b style="color:var(--peach-d)">TA</b>-gious · <b style="color:var(--peach-d)">SAR</b>-casm · <b style="color:var(--peach-d)">SIT</b>-com · <b style="color:var(--peach-d)">CHUCK</b>-le. And the "gh" in <b>laugh</b> sounds like <b>f</b>: /lɑːf/. Say it out loud: <i>"That was absolutely hilarious!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>Most laughter comes after jokes, so you need to learn clever jokes in English.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>Most laughter isn't about jokes – it's a friendly signal we share with other people.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>Laughing is bad for your body, so it's better to keep a straight face.</div>
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
      <div class="chips predict-chips" style="margin-top:2mm;justify-content:center;gap:1.4mm"><span>shopping centres</span><span>cuff</span><span>sitcom</span><span>waiter</span><span>banana</span><span>intern</span><span>sock</span><span>pigeon</span></div>
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
    <div class="mcq"><div class="qq">1. "Hilarious" means…</div><div class="opt"><span class="c">a</span>a little bit funny</div><div class="opt"><span class="c">b</span>extremely funny</div><div class="opt"><span class="c">c</span>not funny at all</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">2. You didn't understand a joke. The most natural reply is…</div><div class="opt"><span class="c">a</span>"Sorry, I didn't get it."</div><div class="opt"><span class="c">b</span>"Sorry, I didn't take it."</div><div class="opt"><span class="c">c</span>"Sorry, I don't joke."</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">3. "The party was really ______ – we danced all night!"</div><div class="opt"><span class="c">a</span>funny</div><div class="opt"><span class="c">b</span>fun</div><div class="opt"><span class="c">c</span>funnily</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">4. Something "contagious"…</div><div class="opt"><span class="c">a</span>spreads from person to person</div><div class="opt"><span class="c">b</span>is very loud</div><div class="opt"><span class="c">c</span>happens very rarely</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">5. "Please don't laugh ______ me!"</div><div class="opt"><span class="c">a</span>to</div><div class="opt"><span class="c">b</span>on</div><div class="opt"><span class="c">c</span>at</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. Which sentence made people laugh in Provine's research?</div><div class="opt"><span class="c">a</span>"See you later."</div><div class="opt"><span class="c">b</span>"Here's a funny joke."</div><div class="opt"><span class="c">c</span>"Please laugh now."</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">7. In a conversation, who laughs more?</div><div class="opt"><span class="c">a</span>the person who is listening</div><div class="opt"><span class="c">b</span>the person who is speaking</div><div class="opt"><span class="c">c</span>they both laugh the same</div><div class="hint">🎧 ⏱ 2:17</div></div>
    <div class="mcq"><div class="qq">8. Lucy wanted fish in a French restaurant. What did she ask for?</div><div class="opt"><span class="c">a</span>chicken</div><div class="opt"><span class="c">b</span>the bill</div><div class="opt"><span class="c">c</span>poison</div><div class="hint">🎧 ⏱ 6:57</div></div>
    <div class="mcq"><div class="qq">9. What was the ringtone on the boss's phone?</div><div class="opt"><span class="c">a</span>a dog barking</div><div class="opt"><span class="c">b</span>a duck quacking</div><div class="opt"><span class="c">c</span>a bell ringing</div><div class="hint">🎧 ⏱ 11:59</div></div>
    <div class="mcq"><div class="qq">10. Diego said the pigeon had a question about…</div><div class="opt"><span class="c">a</span>the past simple</div><div class="opt"><span class="c">b</span>the weather</div><div class="opt"><span class="c">c</span>the present perfect</div><div class="hint">🎧 ⏱ 18:47</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🧩</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> We usually laugh at the <b>end</b> of a phrase – like a full stop or a comma. Laughter fits into language!</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">4</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>Provine and his students listened to people laughing in shopping centres and cafés.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>We usually laugh in the middle of a sentence.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:17</td></tr>
      <tr><td class="n">3</td><td>When you hear someone laughing, it's hard not to laugh too.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 4:25</td></tr>
      <tr><td class="n">4</td><td>Deep laughing is hard physical work for your body.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:32</td></tr>
      <tr><td class="n">5</td><td>In Robin Dunbar's study, people watched the comedy videos alone.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:32</td></tr>
      <tr><td class="n">6</td><td>After Lucy's mistake, the French waiter was unfriendly all evening.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 6:57</td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">5</span>Laughter by numbers 🔍 <span class="tag">listening</span><span class="tag pts">5 points</span></h2>
        <p class="instr" style="margin-bottom:0">Match each number (a–e) to the right fact. Write the letter in the box. ⏱ 0:05 · 2:17 · 4:25 · 5:32</p>
      </div>
      <img class="char" src="img/f/46-lucy-magnifying-glass-w.jpg" style="width:20mm;flex:none">
    </div>
    <div class="chips" style="margin:2mm 0 2mm 10.8mm"><span>a) 10–20%</span><span>b) about 50%</span><span>c) 30 times</span><span>d) 15 minutes</span><span>e) 10%</span></div>
    <div class="card white nums2" style="padding:2.4mm 4mm">
      <span><b>1.</b> how much more the <b>speaker</b> laughs than the listener</span><span class="bx"></span>
      <span><b>2.</b> how much your pain threshold went up after laughing</span><span class="bx"></span>
      <span><b>3.</b> how many laughs came after something like a joke</span><span class="bx"></span>
      <span><b>4.</b> how long people watched comedy together in Dunbar's study</span><span class="bx"></span>
      <span><b>5.</b> how much more people laughed with others than alone</span><span class="bx"></span>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">6</span>Funny mix-ups 🐟 <span class="tag">new! pronunciation</span><span class="tag pts">4 points</span></h2>
        <p class="instr" style="margin-bottom:0">Lucy asked for <b>poison</b> instead of <b>poisson</b> (fish)! Circle the word each speaker <b>meant</b>. Then say both words out loud – can you hear the difference?</p>
      </div>
      <img class="char" src="img/f/71-lucy-embarrassed-w.jpg" style="width:20mm;flex:none">
    </div>
    <div class="mix" style="margin-top:2.2mm">
      <div><b>1.</b> "Can I have the ______ soup, please?" <span class="w"><span>kitchen</span><span>chicken</span></span></div>
      <div><b>2.</b> "I'm so ______ – I haven't eaten all day!" <span class="w"><span>hungry</span><span>angry</span></span></div>
      <div><b>3.</b> "For ______, I'd like chocolate cake." <span class="w"><span>desert</span><span>dessert</span></span></div>
      <div><b>4.</b> "Can I borrow a ______? I need to write this down." <span class="w"><span>pan</span><span>pen</span></span></div>
    </div>
  </div>
  <div class="sec">
    <div class="card peach" style="display:flex;gap:3mm;align-items:center;font-size:9pt">
      <span style="font-size:17pt">🧪</span>
      <div><b style="color:var(--night)">Laughter glue:</b> real, deep laughing is hard work for your body. It seems to release <b>endorphins</b> – natural chemicals in your brain that help you feel good and reduce pain. And they may help people feel <b>closer</b> to each other!</div>
    </div>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>"You had to be there!" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Two friends talk about something that happened at work. Listen at ⏱ 11:59 and write <b>one word</b> in each gap (1–8). Then answer A and B. The breakdown at ⏱ 13:18 can help.</p>
    </div>
    <img class="char" src="img/f/63-jack-at-work-w.jpg" style="width:22mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat" style="margin-top:2.6mm;gap:1.3mm">
{CHAT}
  </div>
  <div class="grid2" style="margin-top:2.8mm;gap:3mm">
    <div class="card" style="padding:2.4mm 4mm"><b style="color:var(--night)">A.</b> What do we say when a story is <b>funnier in real life</b> than when you tell it?<div class="lines"></div></div>
    <div class="card" style="padding:2.4mm 4mm"><b style="color:var(--night)">B.</b> Find the phrase that means <b>"suddenly started laughing loudly"</b>:<div class="lines"></div></div>
  </div>
  <div class="small" style="margin-top:2mm;text-align:center">🎭 <b>Say it out loud!</b> Play both parts – then tell the story again with a funny moment from <b>your</b> life.</div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">8</span>The laugh-o-meter 📈 <span class="tag">new! word scale</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">How big is each laugh? Put the six expressions (a–f) in the right part of the meter. ⏱ 14:16</p>
    </div>
    <img class="char" src="img/f/40-lucy-excited-right-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chips" style="margin:2.4mm 0 0;justify-content:center"><span>a) to chuckle</span><span>b) to be in stitches</span><span>c) to burst out laughing</span><span>d) to giggle</span><span>e) to nearly die laughing</span><span>f) to crack up</span></div>
  <div class="meterbar"></div>
  <div class="meter">
    <div class="z z1"><span class="h">🤭 QUIET</span><span class="s">a small, soft laugh – maybe one you're trying to hide</span><span class="slots"><span class="box"></span><span class="box"></span></span></div>
    <div class="z z2"><span class="h">😆 SUDDEN &amp; LOUD</span><span class="s">you start laughing a lot, all at once</span><span class="slots"><span class="box"></span><span class="box"></span></span></div>
    <div class="z z3"><span class="h">🤣 CAN'T STOP!</span><span class="s">you laugh so much that it hurts</span><span class="slots"><span class="box"></span><span class="box"></span></span></div>
  </div>
  <div class="bub" style="margin-top:2.6mm">
    <img class="char" src="img/f/07-lucy-great-job-w.jpg" style="width:18mm;flex:none">
    <div class="txt"><b>Lucy's tip:</b> <b>Giggle</b> is often a silly or nervous laugh – children giggle. <b>Chuckle</b> is warm and quiet – you chuckle when you read a funny message. Using the right word makes your stories come alive!</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">9</span>Sincere or sarcastic? 😏 <span class="tag">new! listening for meaning</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Read the situation. Does the person <b>mean it</b> (sincere), or mean the <b>opposite</b> (sarcastic)? Tick one. ⏱ 10:31</p>
      </div>
      <img class="char" src="img/f/72-jack-confused-w.jpg" style="width:20mm;flex:none">
    </div>
    <div class="grid2 sar" style="margin-top:2.2mm;gap:2.2mm">{SARC}</div>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/25-jack-rain-umbrella-w.jpg" style="width:17mm;flex:none">
      <div class="txt" style="font-size:8.5pt"><b>How to spot sarcasm:</b> the words don't match the situation · the voice is slower, flatter or a bit exaggerated · there's often a tiny smile or a pause. Not sure? Just smile and say, <i>"You're joking, right?"</i> And be careful with sarcasm in <b>messages</b> – nobody can hear your voice!</div>
    </div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">10</span>fun · funny · laugh at · laugh with <span class="tag">common mistakes</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">Complete each sentence with <b>fun</b>, <b>funny</b>, <b>at</b> or <b>with</b>.</p>
    </div>
    <img class="char" src="img/f/62-lucy-birthday-cake-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <div class="grid2" style="gap:2.4mm;margin-top:2.2mm">
    <div class="card sage" style="font-size:8.6pt"><b style="color:var(--sage-d);font-size:9.6pt">fun 🎉</b> = enjoyable, a good time<br><i>"The party was really fun." · "We had lots of fun."</i></div>
    <div class="card peach" style="font-size:8.6pt"><b style="color:var(--peach-d);font-size:9.6pt">funny 😂</b> = it makes you laugh (or: strange)<br><i>"He's so funny!" · "This milk smells funny."</i></div>
  </div>
  <div class="card white" style="margin-top:2.4mm;font-size:9.3pt;line-height:2.05">
    1. The party was really <span class="blank"></span> – we danced all night.<br>
    2. My brother is so <span class="blank"></span> – he always makes me laugh.<br>
    3. This soup tastes a bit <span class="blank"></span>. Is it OK?<br>
    4. We had lots of <span class="blank"></span> at the beach yesterday.<br>
    5. It isn't kind to laugh <span class="blank s"></span> people when they make mistakes.<br>
    6. Don't worry – we're laughing <span class="blank s"></span> you, not at you!
  </div>

  <div class="sec">
    <h2><span class="num">11</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 16:48</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "Are you making joke?"</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "I died from laughing."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "I didn't understand the joke."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "It was very very funny."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "Are you serious? I don't believe!" <span class="small">(your friend tells you something hard to believe)</span></td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/69-duo-thumbs-up-w.jpg" style="width:26mm;flex:none">
      <div class="txt"><b>Remember:</b> if you laugh <b>at</b> someone, you make fun of them – that can hurt. If you laugh <b>with</b> someone, you laugh together and everyone enjoys it. Small word, big difference! 💜</div>
    </div>
  </div>
  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/52-lucy-phone-comment-w.jpg" style="width:19mm;flex:none">
      <div class="txt"><b>Share it with us!</b> Tell us in the comments about your <b>funniest moment while learning English</b> – a funny mistake, like Lucy's French poison. We'll read them all (and probably laugh – <b>with</b> you!). 💜</div>
    </div>
  </div>
  {foot(7)}
</section>

<!-- ================= PAGE 8 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">12</span>Clue word search + secret message <span class="tag">puzzle</span><span class="tag pts">11 points</span></h2>
      <p class="instr" style="margin-bottom:0"><b>Step 1:</b> Complete each clue – the first letter and the number of letters are given (1 point each). <b>Step 2:</b> Find the 11 words in the grid. They go → ↓ ↘ or ↗ and never cross each other.</p>
    </div>
    <img class="char" src="img/f/50-lucy-puzzle-piece-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <div style="display:grid;grid-template-columns:1fr auto;gap:3.4mm;margin-top:2.2mm;align-items:center">
    <div class="card white clues" style="padding:2.4mm 3.2mm">
{CLUES}    </div>
    <div>{W.grid_html(ws)}</div>
  </div>
  <div class="card sage" style="margin-top:2.6mm;padding:2.6mm 4mm">
    <b style="color:var(--night)">🤫 Step 3 – the secret message</b> <span class="small">(no points)</span> Cross out the 11 words. Then write the letters that are left, row by row, from left to right. It's Jack's advice from the end of the episode!
    <div class="msgrow" style="margin-top:2.6mm">{W.message_slots(ws['message'])}</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">13</span>The pigeon story 🐦 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 18:47. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/19-lucy-glasses-book-w.jpg" style="width:18mm;flex:none">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">🐦</span><span>A pigeon flew in and walked across Lucy's papers.</span></div>
      <div class="ev"><span class="box"></span><span class="e">💌</span><span>On the last day, Diego gave Lucy a card with a pigeon wearing glasses.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🤫</span><span>Lucy had a quiet evening class, and Diego was very shy.</span></div>
      <div class="ev"><span class="box"></span><span class="e">😂</span><span>The whole class exploded with laughter.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🪟</span><span>One warm evening, Lucy opened the window.</span></div>
      <div class="ev"><span class="box"></span><span class="e">💬</span><span>Diego said, "I think he has a question about the present perfect."</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> How was the class different after that night? Why?<div class="lines"></div></div>
  </div>
  {foot(8)}
</section>

<!-- ================= PAGE 9 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
    <div>
      <h2><span class="num">14</span>Your turn <span class="tag">writing</span><span class="tag pts">8 points</span></h2>
      <p class="instr" style="margin-bottom:0">2 points for each good sentence.</p>
    </div>
    <img class="char" src="img/f/05-lucy-writing-w.jpg" style="width:18mm;flex:none">
  </div>
  <div class="grid2" style="margin-top:2.2mm;gap:3mm;align-items:stretch">
    <div class="card" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">A. My funniest English moment 😂</b>
      <div class="small" style="margin-top:1mm">Write two sentences. Use <b>burst out laughing</b>, <b>in stitches</b> or <b>couldn't keep a straight face</b>. <i>e.g. "I asked for a 'pan' instead of a 'pen', and the whole class burst out laughing."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. One situation, two replies 😊 😏</b>
      <div class="small" style="margin-top:1mm">Your friend arrives <b>one hour late</b>. Write one <b>sincere</b> reply and one friendly <b>sarcastic</b> reply. <i>e.g. "Oh, you're right on time!"</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">📓</span>My laugh log <span class="tag fun">your 7-day mission</span></h2>
    <p class="instr">Jack's challenge: notice when you laugh – and why. Was it a <b>joke</b> 🃏 or just a <b>moment</b> ✨?</p>
    <table class="log">
      <tr><th>Day</th><th>What made me laugh?</th><th>Who was I with?</th><th>Joke 🃏 or moment ✨?</th></tr>
      <tr><td class="d">1</td><td></td><td></td><td class="c">🃏 · ✨</td></tr>
      <tr><td class="d">2</td><td></td><td></td><td class="c">🃏 · ✨</td></tr>
      <tr><td class="d">3</td><td></td><td></td><td class="c">🃏 · ✨</td></tr>
      <tr><td class="d">4</td><td></td><td></td><td class="c">🃏 · ✨</td></tr>
      <tr><td class="d">5</td><td></td><td></td><td class="c">🃏 · ✨</td></tr>
      <tr><td class="d">6</td><td></td><td></td><td class="c">🃏 · ✨</td></tr>
      <tr><td class="d">7</td><td></td><td></td><td class="c">🃏 · ✨</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:var(--teal-d)">🙉 DIDN'T GET IT</b>Sorry, I didn't get that.<br>Can you explain?<br>You're joking, right?</div>
        <div><b style="color:var(--peach-d)">😂 REACT</b>That's hilarious!<br>I'm cracking up!<br>We were in stitches.</div>
        <div><b style="color:#5B3A99">😏 IRONY</b>"Lovely weather!" <span style="color:var(--muted)">(in the rain)</span><br>"Well, that went well."</div>
        <div><b style="color:var(--sage-d)">💜 BE KIND</b>I was only joking!<br>Laugh <span style="font-weight:700">with</span> people, not <span style="font-weight:700">at</span> them.</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain why most laughter isn't about jokes.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>describe different laughs: giggle, chuckle, in stitches…</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>tell when someone is being sarcastic.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>say politely when I didn't get a joke.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
    </table>
  </div>

  {foot(9)}
</section>

<!-- ================= PAGE 10 (KEY) ================= -->
<section class="page key">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:2mm">
    <h2><span class="num">✓</span>Answer key</h2>
    <span class="small">Count your points and write your score on page 1!</span>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:2mm;margin-top:2.6mm">
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: c – only about 10–20% of laughs came after anything like a joke. · Predict: <b>banana</b> 🍌 isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 b · 2 g · 3 c · 4 i · 5 j · 6 d · 7 e · 8 f · 9 a · 10 h<br>Big idea: b (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 b · 2 a · 3 b · 4 a · 5 c · 6 a · 7 b · 8 c · 9 b · 10 c</p></div>
    <div class="k"><h3>4 · True or false?</h3><p>1 T · 2 F (at the end of a phrase, like punctuation) · 3 T · 4 T · 5 F (with other people) · 6 F (he was the friendliest waiter ever)</p></div>
    <div class="k"><h3>5 · Laughter by numbers</h3><p>1 b · 2 e · 3 a · 4 d · 5 c</p></div>
    <div class="k"><h3>6 · Funny mix-ups</h3><p>1 chicken · 2 hungry · 3 dessert · 4 pen</p></div>
    <div class="k"><h3>7 · "You had to be there!"</h3><p>1 cheerful · 2 duck · 3 way · 4 face · 5 giggling · 6 stitches · 7 cracking · 8 there · A "You had to be there." · B "burst out laughing"</p></div>
    <div class="k"><h3>8 · The laugh-o-meter</h3><p>🤭 QUIET: a, d · 😆 SUDDEN &amp; LOUD: c, f · 🤣 CAN'T STOP: b, e</p></div>
    <div class="k"><h3>9 · Sincere or sarcastic?</h3><p>{SAR_KEY}</p></div>
    <div class="k"><h3>10 · fun · funny · at · with</h3><p>1 fun · 2 funny · 3 funny · 4 fun · 5 at · 6 with</p></div>
    <div class="k"><h3>11 · Say it better (2 points each)</h3><p>1 Are you joking? / You're kidding! · 2 I nearly died laughing. / I was in stitches. · 3 I didn't get it. · 4 It was absolutely hilarious. / I couldn't stop laughing. · 5 You're kidding! / Are you pulling my leg?</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Word search (1 point per word)</h3><p>1 contagious · 2 hilarious · 3 stitches · 4 chuckle · 5 sarcasm · 6 giggle · 7 sitcom · 8 pigeon · 9 poison · 10 ringtone · 11 duck<br><b>Secret:</b> You don't need to be a comedian. You just need to be there.</p></div>{W.key_svg(ws, 38)}</div>
    <div class="k"><h3>13 · The pigeon story · 14 · Your turn</h3><p>1 🤫 quiet class · 2 🪟 window · 3 🐦 pigeon · 4 💬 present perfect · 5 😂 laughter · 6 💌 the card<br><i>Think about it:</i> laughing together made them a group – they stayed to chat and had coffee together.<br>14: your own answers – 2 points per good sentence.</p></div>
    <div class="k"><h3>Your score</h3><p>90–100 🏆 <b>Comedy star!</b> · 70–89 🤣 <b>In stitches</b> · 50–69 😆 <b>Cracking up</b> · 0–49 🤭 <b>Giggling – listen again!</b></p></div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy every week. Come and laugh with us!<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
    <img class="char" src="img/f/29-duo-high-five-night.jpg" style="width:37mm">
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
