"""Writes template.html for the put-things-off worksheet (Podcast 66).
CSS design system copied from make-friends (which includes all earlier worksheets).
Word search from ws.json (built by _source/tools/wordsearch.py). Timestamps: video time = NoteGPT time + 5 s."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import wordsearch as W

src = (HERE.parent / "make-friends" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Make Friends Worksheet", "Put Things Off Worksheet")
ws = json.loads((HERE / "ws.json").read_text())
W.check(ws)

EXTRA = """
/* ---- new in put-things-off ---- */
.ws td{width:7.2mm;height:7.2mm;font-size:10.4pt}
.circle{display:grid;grid-template-columns:repeat(5,1fr);gap:4.2mm;align-items:stretch;position:relative}
.circle>div{border-radius:3mm;padding:2mm 1.6mm;font-size:8.3pt;line-height:1.4;text-align:center;position:relative}
.circle>div b.e{display:block;font-size:14pt;line-height:1.2}
.circle>div:not(:last-child)::after{content:"➜";position:absolute;right:-3.7mm;top:42%;font-size:9pt;color:var(--mauve);z-index:2}
.loop{margin-top:1.2mm;border:1.6px dashed var(--mauve);border-top:none;border-radius:0 0 4mm 4mm;height:4mm;position:relative}
.loop span{position:absolute;left:50%;transform:translateX(-50%);bottom:-2.6mm;background:#fff;padding:0 2mm;font-size:8pt;font-weight:700;color:var(--mauve)}
.ifthen td{padding:2.1mm 1mm;font-size:9pt;vertical-align:middle}
.tiny td{padding:1.1mm 1mm}
.feel{display:grid;grid-template-columns:repeat(4,1fr);gap:1.8mm}
.feel div{border-radius:3mm;padding:1.6mm 2.2mm;font-size:8.2pt;line-height:1.35}
.feel div b{display:block;font-size:8.8pt;color:var(--night)}
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
 ("LUCY", "37-lucy-thinking-right", f"Ugh. I really need to start {gap(1)} for my exam."),
 ("JACK", "15-jack-shrug-left", "You said that yesterday. And the day before. When is it again?"),
 ("LUCY", "38-lucy-explaining-right", f"Next Thursday. I keep {gap(2)} it off. Every time I open my notes, I just feel {gap(3)}. There's so much to learn."),
 ("JACK", "43-jack-explaining-left", "Okay, so don't try to learn it all tonight. What's the first topic?"),
 ("LUCY", "11-lucy-asking-right", f"The first {gap(4)}, I suppose. But it's really long."),
 ("JACK", "13-jack-talking-left", f"Then just do ten minutes. Set a {gap(5)}. If you want to stop after ten minutes, you can stop."),
 ("LUCY", "09-lucy-talking-right", f"Only ten minutes? I can probably {gap(6)} that."),
 ("JACK", "44-jack-embarrassed-left", "And give me your phone. You can have it back when the timer goes off."),
 ("LUCY", "36-lucy-surprised-right", f"Fine. Let's just get it {gap(7)} with."),
 ("JACK", "45-jack-agreeing-left", f"That's the {gap(8)}. You've got this."),
 ("LUCY", "12-lucy-laughing-right", "Okay. Thanks. Honestly, I think the worrying is worse than the actual studying."),
 ("JACK", "41-jack-laughing-left", "It usually is."),
])

PUT = [("Please don't put ______ again! (it)", "off it", "it off", "it off"),
       ("Stop putting ______ – start now! (them)", "them off", "off them", "them off"),
       ("I keep ______ my homework.", "to put off", "putting off", "putting off"),
       ("I finally got round to ______ my bike.", "fixing", "fix", "fixing"),
       ("I haven't got round ______ it yet.", "to", "for", "to"),
       ("Why do you always leave it ______ the last minute?", "in", "until", "until")]
PUTS = "".join(f'      <div class="tm2" style="grid-template-columns:1fr 28mm 28mm"><span>{i}. {t}</span><span class="claim ed"><span class="box"></span>{a}</span><span class="claim ing"><span class="box"></span>{b}</span></div>\n' for i, (t, a, b, _) in enumerate(PUT, 1))
PUT_KEY = " · ".join(f"{i} {k}" for i, (_, _a, _b, k) in enumerate(PUT, 1))

clues = [
 ("PASSPORT", "Lucy avoided her {} form for three weeks."),
 ("MOMENTUM", "Once you start, you keep going: {}."),
 ("DEADLINE", "The day you must finish by: a {}."),
 ("CURTAINS", "Lucy washed the kitchen {}."),
 ("BISCUITS", "Grandma bought Lucy's favourite {}."),
 ("STRANGER", "To our brain, future you is like a {}."),
 ("BULLET", "Do the hard thing: bite the {}."),
 ("SPICES", "Lucy put her {} in A–Z order."),
 ("TIMER", "Just two minutes – set a {}!"),
 ("PHONE", "The easy escape: your {}."),
]
assert sorted(w for w, _ in clues) == sorted(ws["pos"])
def nw(t):
    return re.sub(r"\{\}(\S*)", lambda m: '<span style="white-space:nowrap">{}' + m.group(1) + '</span>', t)
CLUES = "".join(f'      <div><span class="n">{i}</span><span>{nw(t).format(W.slots(w))}</span></div>\n'
                for i, (w, t) in enumerate(clues, 1))
WS_KEY = " · ".join(f"{i} {w.lower()}" for i, (w, _) in enumerate(clues, 1))

IFS = [("🚌 If I'm on the bus to work,", "c"), ("🍽️ If it's seven o'clock and I've finished dinner,", "e"),
       ("📱 If I want to check my phone while I'm working,", "a"), ("😵 If I feel overwhelmed by a big task,", "f"),
       ("📅 If I miss a day,", "b"), ("☕ If I'm making my morning coffee,", "d")]
THENS = ["then I'll put it in another room.", "then I'll forgive myself and start again tomorrow.",
         "then I'll listen to an English podcast.", "then I'll learn five new words.",
         "then I'll do fifteen minutes of English.", "then I'll write down the first three steps."]
IF_ROWS = "".join(f'        <tr><td class="ans" style="width:8mm"><span class="box sm"></span></td><td><b style="color:var(--night)">{i}.</b> {t}</td></tr>\n' for i, (t, _) in enumerate(IFS, 1))
THEN_ROWS = "".join(f'<b>{chr(97+i)})</b> {t}<br>' for i, t in enumerate(THENS))
IF_KEY = " · ".join(f"{i} {k}" for i, (_, k) in enumerate(IFS, 1))

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
      <h1>Why We Put Things Off (And How to Stop)</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">Why procrastination is about feelings, not laziness, why your brain treats "future you" like a stranger, the two-minute trick, natural English for plans, delays and deadlines – and Lucy's passport form.</p>
      <div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div class="hero2">
      <div style="position:absolute;z-index:2;top:3.4mm;left:3.4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">"I'll do it after a cup of tea…" ☕</div>
      <img class="char" src="img/f/32-lucy-coffee-chat-right-lav.jpg" style="position:absolute;bottom:0;left:2mm;width:36mm">
      <img class="char" src="img/f/72-jack-confused-lav.jpg" style="position:absolute;bottom:0;right:1mm;width:37mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · Don't put it off! ⏱️</div><div class="s">Jack's tip: open this worksheet today – even if you only do the first exercise!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: My procrastination check <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Be honest! Tick everything that is true for you. 😅</p>
    <div style="display:grid;grid-template-columns:1.42fr .58fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:1.8mm;justify-content:center;padding:2.6mm 3.6mm">
        <div class="conf" style="grid-template-columns:1fr 1fr;justify-content:stretch;font-size:8.7pt">
          <div><span class="box sm"></span>🧹 I clean when I should work</div>
          <div><span class="box sm"></span>📧 I leave emails for days</div>
          <div><span class="box sm"></span>🗓️ I say "I'll start tomorrow"</div>
          <div><span class="box sm"></span>📱 My phone is my easy escape</div>
          <div><span class="box sm"></span>⏰ I do things at the last minute</div>
          <div><span class="box sm"></span>✅ I usually start straight away</div>
        </div>
        <div style="font-size:9pt"><b style="color:var(--night)">My procrastination score:</b> <span class="blank s"></span> / 6</div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> Lucy avoided her passport form for three weeks. When she finally did it, how long did it take?</div>
        <div style="display:flex;gap:3.4mm;font-size:8.7pt;white-space:nowrap"><span><span class="circ">a</span> eleven minutes</span><span><span class="circ">b</span> two hours</span><span><span class="circ">c</span> a whole weekend</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 22:00</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:1.8mm 2.4mm;font-size:8.1pt;border:1.2px solid #F4D2C2;line-height:1.36"><b style="color:var(--night)">Jack:</b> "My bike's been broken for two months. Future Jack will fix it!" 🚲</div>
        <img class="char" src="img/f/51-jack-stopwatch-peach.jpg" style="width:27mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – or write them in your notebook.</p>
    <div class="grid2" style="gap:2.4mm">
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>1.</b> What's one thing you've been putting off?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>2.</b> What do you do instead – your "spice jars"?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>3.</b> Do you work better with a deadline? Why?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>4.</b> What would "future you" say to you today?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Then check at ⏱ 14:33 and ⏱ 15:52</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> to procrastinate</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> to put something off</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> to get round to</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> a deadline</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> at the last minute</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> momentum</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> chronic</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> overwhelmed</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> to revise (for an exam)</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> to forgive yourself</td></tr>
      </table>
      <div class="card" style="font-size:9pt;line-height:1.55">
        <b>a)</b> to delay something to a later time<br>
        <b>b)</b> the force that keeps something moving once it has started<br>
        <b>c)</b> to delay doing something you should do, usually because you don't want to<br>
        <b>d)</b> to study again to prepare for an exam (British English)<br>
        <b>e)</b> the time or day by which you have to finish something<br>
        <b>f)</b> to stop being angry with yourself for a mistake<br>
        <b>g)</b> to finally do something, after a long time of not doing it<br>
        <b>h)</b> happening again and again, for a long time<br>
        <b>i)</b> at the latest possible time<br>
        <b>j)</b> feeling that something is too big or difficult to deal with
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/03-lucy-did-you-know-w.jpg" style="width:20mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> pro-<b style="color:var(--peach-d)">CRAS</b>-ti-nate · pro-cras-ti-<b style="color:var(--peach-d)">NA</b>-tion · mo-<b style="color:var(--peach-d)">MEN</b>-tum · <b style="color:var(--peach-d)">DEAD</b>-line · <span style="white-space:nowrap">o-ver-<b style="color:var(--peach-d)">WHELMED</b>.</span> Say it: <i>"I keep putting it off – let's just get it over with!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>People put things off because they are lazy, so they need a better calendar.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>The best way to stop procrastinating is to be very hard on yourself.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>We put things off to escape a bad feeling – tiny first steps and being kind to yourself (and "future you") help.</div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <div class="ava" style="width:22mm;height:22mm"><img src="img/f/06-jack-listening-lav.jpg" style="height:140%"></div>
      <div class="txt"><b>Jack's tip:</b> First listen = the <b>big picture</b>. Don't stop the video and don't worry about every word. Second listen = the <b>details</b>. That's when you answer the 🎧 questions.</div>
    </div>
  </div>

  <div class="sec">
    <div class="card sage">
      <b style="color:var(--night)">🔮 Predict before you listen!</b> <span class="small">(no points)</span> Seven of these words are in the episode. One is <b>not</b>. Circle the one you think you <b>won't</b> hear – then check while you listen.
      <div class="chips predict-chips" style="margin-top:2mm;justify-content:center;gap:1.4mm"><span>kettle</span><span>spice jars</span><span>curtains</span><span>fridge</span><span>biscuits</span><span>bike</span><span>umbrella</span><span>dentist</span></div>
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
    <div class="mcq"><div class="qq">1. "I keep ______ it off."</div><div class="opt"><span class="c">a</span>put</div><div class="opt"><span class="c">b</span>to put</div><div class="opt"><span class="c">c</span>putting</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">2. "I finished my essay ______ the last minute."</div><div class="opt"><span class="c">a</span>at</div><div class="opt"><span class="c">b</span>in</div><div class="opt"><span class="c">c</span>on</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">3. Which sentence is correct?</div><div class="opt"><span class="c">a</span>I put off it.</div><div class="opt"><span class="c">b</span>I put it off.</div><div class="opt"><span class="c">c</span>I it put off.</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">4. "I finally bit the bullet." I…</div><div class="opt"><span class="c">a</span>ate something very hard</div><div class="opt"><span class="c">b</span>did something difficult I'd been avoiding</div><div class="opt"><span class="c">c</span>got very angry</div><div class="hint">🧠 Imagine it!</div></div>
    <div class="mcq"><div class="qq">5. "I'll do it ______." (= at a later time)</div><div class="opt"><span class="c">a</span>after</div><div class="opt"><span class="c">b</span>last</div><div class="opt"><span class="c">c</span>later</div><div class="hint">🧠 Everyday English</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. How long did Lucy avoid the passport form?</div><div class="opt"><span class="c">a</span>three days</div><div class="opt"><span class="c">b</span>three weeks</div><div class="opt"><span class="c">c</span>three months</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">7. What did Lucy put in alphabetical order?</div><div class="opt"><span class="c">a</span>her books</div><div class="opt"><span class="c">b</span>her socks</div><div class="opt"><span class="c">c</span>her spice jars</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">8. About how many adults are chronic procrastinators?</div><div class="opt"><span class="c">a</span>15–20%</div><div class="opt"><span class="c">b</span>1–2%</div><div class="opt"><span class="c">c</span>50–60%</div><div class="hint">🎧 ⏱ 2:57</div></div>
    <div class="mcq"><div class="qq">9. In the brain scanner, thinking about "you in ten years" looked a lot like thinking about…</div><div class="opt"><span class="c">a</span>your best friend</div><div class="opt"><span class="c">b</span>a stranger</div><div class="opt"><span class="c">c</span>your parents</div><div class="hint">🎧 ⏱ 5:54</div></div>
    <div class="mcq"><div class="qq">10. What has Jack been putting off for two months?</div><div class="opt"><span class="c">a</span>calling his mum</div><div class="opt"><span class="c">b</span>cleaning the fridge</div><div class="opt"><span class="c">c</span>fixing the wheel on his bike</div><div class="hint">🎧 ⏱ 9:37</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🧂</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> Lucy's spice jars went from <i>allspice</i> to <i>turmeric</i> – and they're still in alphabetical order!</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">4</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>Lucy had promised to visit her grandmother in the spring.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>Tim Pychyl says procrastination is mainly a time management problem.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 3:40</td></tr>
      <tr><td class="n">3</td><td>Avoiding a task makes us feel better for a long time.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 3:40</td></tr>
      <tr><td class="n">4</td><td>People who saw an older version of their face saved more money.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:54</td></tr>
      <tr><td class="n">5</td><td>Students who forgave themselves procrastinated more before the second exam.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 7:49</td></tr>
      <tr><td class="n">6</td><td>The self-forgiveness study was a survey, so it shows a link, not definite proof.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 7:49</td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">5</span>Three procrastination studies 🔍 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Which study is each sentence about? Write <b>A</b>, <b>B</b> or <b>C</b>. ⏱ 2:57 · 5:54 · 7:49</p>
      </div>
      <img class="char" src="img/f/20-jack-glasses-laptop-w.jpg" style="width:16mm;flex:none;margin-top:-4mm">
    </div>
    <div class="studies" style="margin-top:2mm">
      <div style="background:var(--peach-l)"><b class="h" style="color:var(--peach-d)">A · How common? 📊</b>2007 · Piers Steel, University of Calgary</div>
      <div style="background:var(--lav)"><b class="h" style="color:var(--mauve-d)">B · Future you 🧓</b>2009 · Hal Hershfield and colleagues, Stanford</div>
      <div style="background:var(--sage)"><b class="h" style="color:var(--sage-d)">C · Forgive yourself 💜</b>2010 · Wohl, Pychyl &amp; Bennett, Carleton University</div>
    </div>
    <table class="tf" style="margin-top:1.6mm">
      <tr><td class="n">1</td><td>People lay in a brain scanner and thought about different people.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">2</td><td>It looked at hundreds of studies on procrastination.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">3</td><td>First-year students had two big exams during the term.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">4</td><td>About one in five adults put things off again and again.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">5</td><td>"You in ten years" looked more like a famous actor you've never met.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">6</td><td>Being kind to yourself after a mistake made it easier to start again.</td><td class="ck"><span class="box"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">6</span>The procrastination circle <span class="tag">new! complete the diagram</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Write one word in each gap: <b>avoid · better · emotion · guilty · time · worse</b>. ⏱ 3:40</p>
      </div>
      <img class="char" src="img/f/75-lucy-a-bit-sad-w.jpg" style="width:14mm;flex:none;margin-top:-4mm">
    </div>
    <div class="circle" style="margin-top:2mm">
      <div style="background:#EEE9F6"><b class="e">😟</b>A task makes you feel bad: bored, worried or unsure.</div>
      <div style="background:#DCEFF3"><b class="e">🏃</b>So you <span class="blank s" style="min-width:12mm"></span> it. <span class="small">(1)</span></div>
      <div style="background:#DDF1E3"><b class="e">😌</b>You feel <span class="blank s" style="min-width:12mm"></span> – but only for a few minutes. <span class="small">(2)</span></div>
      <div style="background:#FDF1D9"><b class="e">⏳</b>Now there's less time, and you feel <span class="blank s" style="min-width:12mm"></span>. <span class="small">(3)</span></div>
      <div style="background:#FBE1DE"><b class="e">😩</b>The task feels even <span class="blank s" style="min-width:12mm"></span>! <span class="small">(4)</span></div>
    </div>
    <div class="loop"><span>↺ … and the circle starts again</span></div>
    <div class="card white" style="margin-top:3.6mm;padding:2mm 4mm;font-size:9.1pt">💬 Pychyl: "Procrastination is an <span class="blank s"></span> regulation problem, not a <span class="blank s"></span> management problem." <span class="small">(5, 6)</span></div>
  </div>
  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/73-lucy-calm-w.jpg" style="width:16mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> If procrastination is about <b>feelings</b>, the solution isn't a better calendar. It's learning to deal with that uncomfortable feeling for a few minutes – and then just starting. 💜</div>
    </div>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>"Let's just get it over with!" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">A sister has an important exam next week – and she hasn't started studying. Listen at ⏱ 13:30 and write <b>one word</b> in each gap (1–8). Then answer A and B. The breakdown at ⏱ 14:33 can help.</p>
    </div>
    <img class="char" src="img/f/19-lucy-glasses-book-w.jpg" style="width:17mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat wide" style="margin-top:2mm;gap:.5mm">
{CHAT}
  </div>
  <div class="grid2" style="margin-top:2.4mm;gap:3mm">
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">A.</b> The exam is next <span class="blank" style="min-width:26mm"></span>.</div>
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">B.</b> Jack takes her <span class="blank" style="min-width:24mm"></span> away.</div>
  </div>

  <div class="sec" style="margin-top:3.4mm">
    <h2><span class="num">8</span>Phrases to steal <span class="tag">expressions</span><span class="tag pts">4 points</span></h2>
    <p class="instr">Match each phrase from the chat (1–4) to its meaning (a–d). ⏱ 14:33</p>
    <div class="grid2" style="gap:4mm;align-items:start">
      <table class="match" style="font-size:9.2pt">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> "I keep putting it off."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> "I can probably manage that."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> "Let's just get it over with."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> "That's the spirit!"</td></tr>
      </table>
      <div class="card" style="font-size:8.9pt;line-height:1.62">
        <b>a)</b> Let's do it quickly, so it's finished.<br>
        <b>b)</b> Great – I like your positive attitude!<br>
        <b>c)</b> I delay it again and again.<br>
        <b>d)</b> I can succeed in doing that.
      </div>
    </div>
  </div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">9</span>Idioms for getting started <span class="tag">idioms</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">Complete each sentence with a word from the box. ⏱ 15:52</p>
    </div>
    <img class="char" src="img/f/47-jack-pointing-right-w.jpg" style="width:17mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chips" style="margin:1.6mm 0 2mm 10.8mm"><span>ball</span><span>bullet</span><span>can</span><span>minute</span><span>present</span><span>round</span></div>
  <table class="coll" style="margin-left:2mm">
    <tr><td>1. 📞 "Should I call him tomorrow?" "There's no time like the <span class="blank s"></span>!"</td></tr>
    <tr><td>2. 🧾 I finally bit the <span class="blank s"></span> and started my tax form.</td></tr>
    <tr><td>3. ⚽ Let's get the <span class="blank s"></span> rolling with a quick meeting on Monday.</td></tr>
    <tr><td>4. 🥫 Stop kicking the <span class="blank s"></span> down the road – deal with it now!</td></tr>
    <tr><td>5. 🧳 He always packs his suitcase at the last <span class="blank s"></span>.</td></tr>
    <tr><td>6. 🚲 I haven't got <span class="blank s"></span> to fixing my bike yet.</td></tr>
  </table>
  <div class="bub" style="margin-top:2.2mm">
    <img class="char" src="img/f/02-jack-lightbulb-idea-w.jpg" style="width:17mm;flex:none">
    <div class="txt"><b>Jack's tip:</b> <b>Kick the can down the road</b> 🥫 = instead of putting the can in the bin, you just kick it a little further. The problem doesn't go away – it waits for <b>future you</b>! And in American English, people say <i>get <b>around</b> to</i>.</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">10</span>If–then plans <span class="tag">new! plan it</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Match each <b>if</b> (1–6) to a <b>then</b> (a–f). With an if–then plan, the decision is already made! ⏱ 10:21</p>
      </div>
      <img class="char" src="img/f/63-jack-at-work-w.jpg" style="width:15mm;flex:none;margin-top:-4mm">
    </div>
    <div class="phr" style="margin-top:2mm;grid-template-columns:1fr 1fr">
      <table class="match ifthen">
{IF_ROWS}      </table>
      <div class="card" style="font-size:8.9pt;line-height:2.2">{THEN_ROWS}</div>
    </div>
    <div class="bub" style="margin-top:2.2mm">
      <img class="char" src="img/f/01-lucy-thumbs-up-w.jpg" style="width:16mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> Psychologists call these <b>implementation intentions</b>. Connect your English to something you <b>already</b> do every day – the bus, your coffee, dinner – and you don't have to decide again. Write your own: <i>If <span class="blank" style="min-width:30mm"></span>, then I'll <span class="blank" style="min-width:34mm"></span>.</i></div>
    </div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">11</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 19:25</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "I am procrastinating my homework."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "I did it in the last minute."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "I will do it after."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "I'm so lazy. I never finish anything."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "Tomorrow I will begin, I promise."</td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/07-lucy-great-job-w.jpg" style="width:18mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> <b>Procrastinate</b> usually has no object: <i>"I'm procrastinating."</i> To say <i>what</i> you're delaying, use <b>put off</b>: <i>"I'm putting off my homework."</i> And <b>first thing</b> = early, before anything else: <i>"I'll start first thing tomorrow."</i></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">✅</span>Put it off – or put off it? <span class="tag fun">tick · no points</span></h2>
        <p class="instr" style="margin-bottom:0">Tick the right one. Remember: with <b>it</b> or <b>them</b>, the small word goes at the <b>end</b> – and after <b>keep</b> and <b>get round to</b>, use <b>-ing</b>. ⏱ 15:52</p>
      </div>
      <img class="char" src="img/f/48-lucy-holding-blank-card-w.jpg" style="width:14mm;flex:none;margin-top:-3mm">
    </div>
    <div style="margin-top:1.6mm">
{PUTS}    </div>
  </div>

  <div class="sec">
    <div class="card teal" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.6pt">💭 Name the feeling!</b> <span class="small">(no points) Lucy's first tip. When you avoid something, ask: "What am I feeling right now?" – then try the fix. ⏱ 10:21</span>
      <div class="feel" style="margin-top:1.8mm">
        <div style="background:#fff"><b>🥱 bored</b>Make it a game: set a timer for two minutes.</div>
        <div style="background:#fff"><b>😰 scared of doing it badly</b>"The first try can be messy. I'll improve it later."</div>
        <div style="background:#fff"><b>🤷 don't know where to start</b>Write down the first three steps.</div>
        <div style="background:#fff"><b>😵 overwhelmed</b>Do only the smallest part – one page, one question.</div>
      </div>
      <div style="font-size:9pt;margin-top:2mm">Something I'm avoiding: <span class="blank" style="min-width:42mm"></span> · I feel: <span class="blank" style="min-width:30mm"></span> · My fix: <span class="blank" style="min-width:34mm"></span></div>
    </div>
  </div>
  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">🐜</span>Make the first step tiny! <span class="tag fun">write · no points</span></h2>
        <p class="instr" style="margin-bottom:0">Starting is like pushing a heavy car – the first push is the hardest. Turn each big task into a tiny first step. ⏱ 10:21</p>
      </div>
      <img class="char" src="img/f/55-jack-thumbs-up-w.jpg" style="width:14mm;flex:none;margin-top:-3mm">
    </div>
    <table class="friend tiny" style="margin-top:1mm">
      <tr><td class="i" style="color:var(--night);width:40%">😩 Study English for two hours</td><td>🐜 <i>Open my book and read one page.</i></td></tr>
      <tr><td class="i" style="color:var(--night)">😩 Clean the whole flat</td><td>🐜 <span class="blank l" style="min-width:76mm"></span></td></tr>
      <tr><td class="i" style="color:var(--night)">😩 Fix my bike (Jack!)</td><td>🐜 <span class="blank l" style="min-width:76mm"></span></td></tr>
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
    <b style="color:var(--night)">🤫 Step 3 – the secret message</b> <span class="small">(no points)</span> Cross out the 10 words. Then write the letters that are left, row by row, from left to right. It's what Lucy thinks now, whenever she wants to put something off!
    <div class="msgrow" style="margin-top:2.6mm">{W.message_slots(ws['message'])}</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">13</span>Lucy's passport story 🛂 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 0:05 and ⏱ 22:00. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/28-lucy-travel-w.jpg" style="width:16mm;flex:none;margin-top:-3mm">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">📞</span><span>Her grandmother called: "I've bought your favourite biscuits!"</span></div>
      <div class="ev"><span class="box"></span><span class="e">💻</span><span>Lucy opened the form and thought, "I'll do this after a cup of tea."</span></div>
      <div class="ev"><span class="box"></span><span class="e">✈️</span><span>The form took eleven minutes – the passport came ten days before her flight.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🧂</span><span>She put all her spice jars in alphabetical order.</span></div>
      <div class="ev"><span class="box"></span><span class="e">⏱️</span><span>She set a two-minute timer and answered the first question.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🧽</span><span>She washed the curtains and cleaned behind the fridge.</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> Why did the two-minute timer work? Use the word <b>momentum</b>.<div class="lines"></div><div class="lines"></div></div>
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
      <b style="color:var(--night);font-size:9.2pt">A. What I've been putting off 🙈</b>
      <div class="small" style="margin-top:1mm">What is it, and how does it make you feel? <i>e.g. "I've been putting off a phone call to my bank, because I'm worried it'll take ages."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. Dear future me 💌</b>
      <div class="small" style="margin-top:1mm">Write a short note to "future you", like Jack. <i>e.g. "Dear Friday Maria, I've already done the hard part for you. You're welcome!"</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">⏱</span>My two-minute week <span class="tag fun">your 7-day mission</span></h2>
        <p class="instr" style="margin-bottom:0">Every day, choose one small thing you've been putting off. Set a timer for two minutes and start. You're allowed to stop – but you probably won't!</p>
      </div>
      <img class="char" src="img/f/59-jack-phone-w.jpg" style="width:15mm;flex:none">
    </div>
    <table class="log week" style="margin-top:2mm">
      <tr><th>Day</th><th>The thing I put off</th><th>Did I keep going after two minutes?</th><th>Done?</th></tr>
      <tr><td class="d">1</td><td class="a">📧 a message I've avoided</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">2</td><td class="a">📝 a form or a task</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">3</td><td class="a">📞 a phone call</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">4</td><td class="a">📚 two minutes of English</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">5</td><td class="a">🔧 a small repair</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">6</td><td class="a">🗂️ the hardest task first</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">7</td><td class="a">💌 a note to future me</td><td></td><td class="c"><span class="box sm"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:var(--peach-d)">🙈 DELAYING</b>I keep putting it off.<br>I haven't got round to it.<br>I'll do it later.</div>
        <div><b style="color:var(--sage-d)">🚀 STARTING</b>Let's get the ball rolling.<br>I finally bit the bullet.<br>Let's get it over with.</div>
        <div><b style="color:var(--mauve-d)">💜 BEING KIND</b>That happened – I'll start again.<br>That's the spirit!<br>You've got this.</div>
        <div><b style="color:#C0392B">⏱️ TRICKS</b>just two minutes<br>phone in another room<br>if–then plans</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain why procrastination is about feelings, not laziness.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use put off, get round to and at the last minute correctly.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>make an if–then plan for my English practice.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use idioms like "bite the bullet" and "get the ball rolling".</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/52-lucy-phone-comment-w.jpg" style="width:19mm;flex:none">
      <div class="txt"><b>Share it with us!</b> Tell us in the comments what you've been putting off – and whether you <b>got round to it</b>. Did you <b>bite the bullet</b>? Did you <b>get the ball rolling</b>? And have you ever organised something silly to avoid something important? 🧂😅</div>
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
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: a – only eleven minutes! · Predict: <b>umbrella</b> ☂️ isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 c · 2 a · 3 g · 4 e · 5 i · 6 b · 7 h · 8 j · 9 d · 10 f<br>Big idea: c (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 c · 2 a · 3 b · 4 b · 5 c · 6 b · 7 c · 8 a · 9 b · 10 c</p></div>
    <div class="k"><h3>4 · True or false?</h3><p>1 T · 2 F (it's an emotion regulation problem) · 3 F (only for a few minutes) · 4 T · 5 F (they procrastinated less) · 6 T</p></div>
    <div class="k"><h3>5 · Three studies · 6 · The circle</h3><p>5: 1 B · 2 A · 3 C · 4 A · 5 B · 6 C<br>6: 1 avoid · 2 better · 3 guilty · 4 worse · 5 emotion · 6 time</p></div>
    <div class="k"><h3>7 · "Let's just get it over with!"</h3><p>1 revising · 2 putting · 3 overwhelmed · 4 chapter · 5 timer · 6 manage · 7 over · 8 spirit · A Thursday · B phone</p></div>
    <div class="k"><h3>8 · Phrases to steal</h3><p>1 c · 2 d · 3 a · 4 b</p></div>
   </div>
   <div>
    <div class="k"><h3>9 · Idioms · 10 · If–then plans</h3><p>9: 1 present · 2 bullet · 3 ball · 4 can · 5 minute · 6 round<br>10: {IF_KEY}</p></div>
    <div class="k"><h3>11 · Say it better (2 points each)</h3><p>1 I'm putting off my homework. / I'm procrastinating. · 2 I did it at the last minute. · 3 I'll do it later. / I'll do it in a bit. · 4 I've been putting this off. Let me do a small part now. · 5 I'll start first thing tomorrow.<br><i>Put it off?</i> {PUT_KEY}</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Word search (1 point per word)</h3><p>{WS_KEY}<br><b>Secret:</b> This might only take eleven minutes.</p></div>{W.key_svg(ws, 34)}</div>
    <div class="k"><h3>13 · The passport story · 14 · Your turn</h3><p>1 💻 "after a cup of tea" · 2 🧂 spice jars · 3 🧽 curtains and fridge · 4 📞 Grandma called · 5 ⏱️ two-minute timer · 6 ✈️ eleven minutes<br><i>Think about it, e.g.:</i> once she started, she got some momentum and just kept going.<br>14: your own answers – 2 points per good sentence.</p></div>
    <div class="k"><h3>Your score</h3><p>90–100 🏆 <b>No time like the present!</b> · 70–89 🚀 <b>Great momentum</b> · 50–69 ⏱️ <b>Two more minutes</b> · 0–49 🧂 <b>Still sorting the spices – try again!</b></p></div>
   </div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy. You didn't put this off – you did it! And remember: future you is not a stranger. Be kind to them. 💜<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
    <img class="char" src="img/f/66-duo-podcast-night.jpg" style="width:40mm">
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
