"""Writes template.html for the being-bored worksheet (Podcast 61).
CSS design system copied from talk-to-yourself (which includes messy-room, why-we-laugh, time-flies, build-a-habit).
Crossword from cw.json (built by _source/tools/crossword.py). Timestamps: video time = NoteGPT time + 5 s."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import crossword as X

src = (HERE.parent / "talk-to-yourself" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Talk to Yourself Worksheet", "Being Bored Worksheet")
cw = json.loads((HERE / "cw.json").read_text())
X.check(cw)
spec = json.loads((HERE / "cw_spec.json").read_text())
CLUES = {w.upper(): c for w, c in spec["words"]}
ACROSS, DOWN = X.clues_html(cw, CLUES)

EXTRA = """
/* ---- new in being-bored ---- */
.claim.ed{background:#DCEFF3;color:#1F5F70;border:1.2px solid #9CCAD6}.claim.ed .box{border-color:#1F5F70}
.claim.ing{background:#FDE3D3;color:#B9542B;border:1.2px solid #F2B796}.claim.ing .box{border-color:#B9542B}
.claim.ok{background:#DDF1E3;color:#1E7B45;border:1.2px solid #8FCBA3}.claim.ok .box{border-color:#1E7B45}
.claim.no{background:#FBE1DE;color:#C0392B;border:1.2px solid #EDA59D}.claim.no .box{border-color:#C0392B}
.edrule{display:grid;grid-template-columns:1fr 1fr;gap:2.4mm;margin:1.6mm 0 2mm}
.edrule div{border-radius:3mm;padding:1.6mm 3mm;font-size:8.6pt;line-height:1.4}
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
 ("JACK", "13-jack-talking-left", f"Well, that's the {gap(1)} gone. The whole street is dark."),
 ("LUCY", "36-lucy-surprised-right", f"You're joking. And my phone's almost dead. What are we {gap(2)} to do now?"),
 ("JACK", "15-jack-shrug-left", "I don't know. We could just sit here and talk, like people did in the old days."),
 ("LUCY", "38-lucy-explaining-right", f"I'm already bored {gap(3)}, and it's only been five minutes."),
 ("JACK", "43-jack-explaining-left", f"Come on, it's not that {gap(4)}. Let's play a game. I'll think of a word, and you guess it. You can ask me twenty {gap(5)}."),
 ("LUCY", "11-lucy-asking-right", f"Fine. Is it something you can {gap(6)}?"),
 ("JACK", "14-jack-listening-left", "No."),
 ("LUCY", "37-lucy-thinking-right", "Is it bigger than a car?"),
 ("JACK", "16-jack-surprised-left", "Much bigger."),
 ("LUCY", "12-lucy-laughing-right", "Is it a train stuck in a field?"),
 ("JACK", "41-jack-laughing-left", "Very funny. No."),
 ("LUCY", "40-lucy-excited-right", "Okay, I'm actually starting to enjoy this. I can't believe I'm saying that."),
 ("JACK", "45-jack-agreeing-left", f"See? Being bored isn't the {gap(7)} of the world."),
 ("LUCY", "09-lucy-talking-right", f"Let's not get {gap(8)} away. But I'll admit, this is better than scrolling."),
])

def pair(i, text, a, b, ca, cb):
    return (f'<div class="sit"><div class="t" style="min-height:0"><b>{i}.</b> {text}</div><div class="ch" style="gap:2mm">'
            f'<span class="claim {ca}"><span class="box"></span>{a}</span>'
            f'<span class="claim {cb}"><span class="box"></span>{b}</span></div></div>')

ED = [
 ("The film was so ______ that I fell asleep. 😴", "bored", "boring"),
 ("I'm ______ – let's go for a walk! 🚶", "bored", "boring"),
 ("Lucy was very ______ in Jack's cow story. 🐄", "interested", "interesting"),
 ("Jack's train story was really ______. 🚆", "interested", "interesting"),
 ("I was ______ that so many men pressed it. ⚡", "surprised", "surprising"),
 ("Copying phone numbers is very ______. 📖", "tired", "tiring"),
]
EDS = "".join(pair(i, t, "😩 " + a, "📺 " + b, "ed", "ing") for i, (t, a, b) in enumerate(ED, 1))

GOOD = [
 "🚌 Leaving your phone in your pocket at the bus stop.",
 "🍫 Opening the fridge every twenty minutes, just to look.",
 "🚶 Going for a short walk without headphones.",
 "📱 Scrolling for an hour every time you're bored.",
 "📓 Keeping a little notebook for your ideas.",
 "⏱️ Waiting two minutes before you pick up your phone.",
]
FLY = ["🎉 at a party", "🏦 in a long queue", "🎬 watching a great film", "🦷 at the dentist's",
       "🏖️ on holiday", "⏰ Friday's last work hour"]
FLIES = "".join(f'      <div class="tm2"><span>{i}. {t}</span><span class="claim ed"><span class="box"></span>✈️ flies</span><span class="claim ing"><span class="box"></span>🐌 drags</span></div>\n' for i, t in enumerate(FLY, 1))
GOODS = "".join(pair(i, t, "✓ HELPS", "✗ DOESN'T HELP", "ok", "no") for i, t in enumerate(GOOD, 1))

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
      <h1>Why Being Bored Is Good for You</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">The experiment where people chose an electric shock, why a boring job can make you more creative, colourful English for boring moments – and Jack, a stuck train and a very patient cow.</p>
      <div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div class="hero2">
      <div style="position:absolute;z-index:2;top:3.4mm;left:3.4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">2 hours 40 minutes… with a cow?! 🐄</div>
      <img class="char" src="img/f/36-lucy-surprised-right-lav.jpg" style="position:absolute;bottom:0;left:3mm;width:35mm">
      <img class="char" src="img/f/26-jack-sleepy-morning-lav.jpg" style="position:absolute;bottom:0;right:2mm;width:37mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · After you listen 💬</div><div class="s">Solve the crossword, try five bored minutes a day – and tell us your most boring moment!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: My boredom check <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Be honest! Tick everything that is true for you. 😄</p>
    <div style="display:grid;grid-template-columns:1.42fr .58fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:1.8mm;justify-content:center;padding:2.6mm 3.6mm">
        <div class="conf" style="grid-template-columns:1fr 1fr;justify-content:stretch;font-size:8.7pt">
          <div><span class="box sm"></span>📱 I check my phone in queues</div>
          <div><span class="box sm"></span>☕ …and while the kettle boils</div>
          <div><span class="box sm"></span>🍫 I eat snacks when I'm bored</div>
          <div><span class="box sm"></span>🛏️ I check my phone in bed</div>
          <div><span class="box sm"></span>🚶 I walk without headphones</div>
          <div><span class="box sm"></span>💡 I get ideas in the shower</div>
        </div>
        <div style="font-size:9pt"><b style="color:var(--night)">My boredom score:</b> <span class="blank s"></span> / 6</div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> People sat alone for 15 minutes. They could press a button for a small electric shock. How many men pressed it?</div>
        <div style="display:flex;gap:3.4mm;font-size:8.7pt;white-space:nowrap"><span><span class="circ">a</span> nobody</span><span><span class="circ">b</span> about two out of three</span><span><span class="circ">c</span> every single one</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 2:41</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:1.8mm 2.4mm;font-size:8.1pt;border:1.2px solid #F4D2C2;line-height:1.36"><b style="color:var(--night)">Jack:</b> "I read the safety sign about eleven times!" 🚆</div>
        <img class="char" src="img/f/72-jack-confused-peach.jpg" style="width:30mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – or write them in your notebook.</p>
    <div class="grid2" style="gap:2.4mm">
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>1.</b> When do you usually feel bored?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>2.</b> What's the first thing you do when you're bored?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>3.</b> Where do your best ideas usually come to you?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>4.</b> What's the most boring thing you've ever had to do?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Then check at ⏱ 13:23 and ⏱ 14:22</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> to daydream</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> to let your mind wander</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> an urge</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> to resist the urge</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> restless</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> a distraction</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> to kill time</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> scrolling</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> a power cut</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> a participant</td></tr>
      </table>
      <div class="card" style="font-size:9pt;line-height:1.55">
        <b>a)</b> a strong, sudden feeling that you want to do something<br>
        <b>b)</b> something that takes your attention away from what you're doing<br>
        <b>c)</b> to think about pleasant or random things while you're awake<br>
        <b>d)</b> moving through things on your phone with your finger, often without thinking<br>
        <b>e)</b> a person who takes part in a study<br>
        <b>f)</b> to not do something, although you really want to<br>
        <b>g)</b> when the electricity suddenly stops<br>
        <b>h)</b> when your thoughts move from one thing to another, with no plan<br>
        <b>i)</b> to do something unimportant while you're waiting<br>
        <b>j)</b> unable to relax or stay still
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/03-lucy-did-you-know-w.jpg" style="width:20mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> <b style="color:var(--peach-d)">DAY</b>-dream · <b style="color:var(--peach-d)">REST</b>-less · dis-<b style="color:var(--peach-d)">TRAC</b>-tion · par-<b style="color:var(--peach-d)">TI</b>-ci-pant · <span style="white-space:nowrap">urge (/ɜːdʒ/).</span> Fun fact: <b>bored</b> sounds exactly like <b>board</b> (/bɔːd/)! Say it: <i>"I'm bored, not boring!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>Boredom can be useful: when your mind wanders, it makes new connections – so give yourself a few quiet minutes without your phone.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>Boredom is always bad for you, so you should keep busy every minute of the day.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>The best way to stop feeling bored is to use your phone more often.</div>
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
      <div class="chips predict-chips" style="margin-top:2mm;justify-content:center;gap:1.4mm"><span>cow</span><span>kettle</span><span>plastic cups</span><span>dentist</span><span>bakery</span><span>robot</span><span>bicycle</span><span>umbrella</span></div>
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
    <div class="mcq"><div class="qq">1. "The film was really slow. I was ______."</div><div class="opt"><span class="c">a</span>bored</div><div class="opt"><span class="c">b</span>boring</div><div class="opt"><span class="c">c</span>bore</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">2. "To kill time" means…</div><div class="opt"><span class="c">a</span>to work really fast</div><div class="opt"><span class="c">b</span>to waste money</div><div class="opt"><span class="c">c</span>to do something while you wait</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">3. "I ______ nothing all weekend."</div><div class="opt"><span class="c">a</span>made</div><div class="opt"><span class="c">b</span>did</div><div class="opt"><span class="c">c</span>passed</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">4. "It was like watching paint dry." It was…</div><div class="opt"><span class="c">a</span>very exciting</div><div class="opt"><span class="c">b</span>very messy</div><div class="opt"><span class="c">c</span>very boring</div><div class="hint">🧠 Imagine it!</div></div>
    <div class="mcq"><div class="qq">5. "Restless" means…</div><div class="opt"><span class="c">a</span>unable to relax or stay still</div><div class="opt"><span class="c">b</span>very sleepy</div><div class="opt"><span class="c">c</span>without a day off</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. How much battery did Jack's phone have on the train?</div><div class="opt"><span class="c">a</span>thirty percent</div><div class="opt"><span class="c">b</span>three percent</div><div class="opt"><span class="c">c</span>thirteen percent</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">7. When people did the thinking task at home, how many cheated?</div><div class="opt"><span class="c">a</span>about a third</div><div class="opt"><span class="c">b</span>almost nobody</div><div class="opt"><span class="c">c</span>everyone</div><div class="hint">🎧 ⏱ 2:41</div></div>
    <div class="mcq"><div class="qq">8. For the boring job, people had to ______ numbers from an old phone book.</div><div class="opt"><span class="c">a</span>call</div><div class="opt"><span class="c">b</span>copy</div><div class="opt"><span class="c">c</span>sell</div><div class="hint">🎧 ⏱ 5:25</div></div>
    <div class="mcq"><div class="qq">9. On her boring walk, where did Lucy solve a work problem?</div><div class="opt"><span class="c">a</span>at the bus stop</div><div class="opt"><span class="c">b</span>in the shower</div><div class="opt"><span class="c">c</span>near the bakery</div><div class="hint">🎧 ⏱ 8:40</div></div>
    <div class="mcq"><div class="qq">10. What did Jack's nephew play with for three hours?</div><div class="opt"><span class="c">a</span>an expensive robot</div><div class="opt"><span class="c">b</span>the box</div><div class="opt"><span class="c">c</span>a notebook</div><div class="hint">🎧 ⏱ 8:40</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🍽️</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> Lucy's secret thinking time? Washing the dishes! Jack's best ideas come in the shower. 🚿</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">4</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>Jack's train journey normally takes about one hour.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>The cow looked away first.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">3</td><td>In Wilson's studies, most people enjoyed sitting alone with their thoughts.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:41</td></tr>
      <tr><td class="n">4</td><td>One man pressed the shock button 190 times.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:41</td></tr>
      <tr><td class="n">5</td><td>The people who only <i>read</i> the phone numbers were the most creative.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:25</td></tr>
      <tr><td class="n">6</td><td>The study proves that being bored will turn you into a genius.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:25</td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">5</span>Two studies and a train 🔍 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Who or what is each sentence about? Write <b>A</b>, <b>B</b> or <b>C</b>. ⏱ 0:05 · 2:41 · 5:25</p>
      </div>
      <img class="char" src="img/f/20-jack-glasses-laptop-w.jpg" style="width:16mm;flex:none;margin-top:-4mm">
    </div>
    <div class="studies" style="margin-top:2mm">
      <div style="background:var(--peach-l)"><b class="h" style="color:var(--peach-d)">A · "Just think" ⚡</b>2014 · Timothy Wilson, University of Virginia</div>
      <div style="background:var(--lav)"><b class="h" style="color:var(--mauve-d)">B · Bored and creative? 🥤</b>Sandi Mann &amp; Rebekah Cadman, Univ. of Central Lancashire</div>
      <div style="background:var(--sage)"><b class="h" style="color:var(--sage-d)">C · Jack's train 🐄</b>a field, a cow and a dead phone</div>
    </div>
    <table class="tf" style="margin-top:1.6mm">
      <tr><td class="n">1</td><td>People copied numbers from an old telephone book.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">2</td><td>People sat alone in a plain, empty room for six to fifteen minutes.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">3</td><td>He read the safety sign on the window about eleven times.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">4</td><td>Some people gave themselves a small electric shock.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">5</td><td>After about an hour, his mind went quiet – and he had an idea.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">6</td><td>People thought of different uses for two plastic cups.</td><td class="ck"><span class="box"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">6</span>Bored or boring? <span class="tag">new! -ed or -ing</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Tick the right word. ⏱ 17:39</p>
      </div>
      <img class="char" src="img/f/71-lucy-embarrassed-w.jpg" style="width:15mm;flex:none;margin-top:-4mm">
    </div>
    <div class="edrule">
      <div style="background:#DCEFF3"><b style="color:#1F5F70">😩 -ED = how you feel.</b> <i>I'm bored. I'm interested.</i></div>
      <div style="background:#FDE3D3"><b style="color:#B9542B">📺 -ING = what makes you feel it.</b> <i>The film is boring.</i></div>
    </div>
    <div class="grid2" style="gap:2.2mm">{EDS}</div>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>"That's the power gone!" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Two flatmates on a Sunday evening – and the electricity has just gone off. Listen at ⏱ 12:22 and write <b>one word</b> in each gap (1–8). Then answer A and B. The breakdown at ⏱ 13:23 can help.</p>
    </div>
    <img class="char" src="img/f/60-lucy-bedtime-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat wide" style="margin-top:2.4mm;gap:.9mm">
{CHAT}
  </div>
  <div class="grid2" style="margin-top:2.6mm;gap:3mm">
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">A.</b> Or say: "There's a power <span class="blank" style="min-width:18mm"></span>."</div>
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">B.</b> The game is better than <span class="blank" style="min-width:28mm"></span>.</div>
  </div>
  <div class="small" style="margin-top:2.4mm;text-align:center">🎭 <b>Say it out loud!</b> Play both parts – then play "twenty questions" in English with a friend, or in your head!</div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">8</span>Phrases to steal <span class="tag">expressions</span><span class="tag pts">4 points</span></h2>
    <p class="instr">Match each phrase from the chat (1–4) to its meaning (a–d). ⏱ 13:23</p>
    <div class="grid2" style="gap:4mm;align-items:start">
      <table class="match" style="font-size:9.2pt">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> "What are we supposed to do now?"</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> "It's not that bad."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> "It isn't the end of the world."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> "Let's not get carried away."</td></tr>
      </table>
      <div class="card" style="font-size:8.9pt;line-height:1.62">
        <b>a)</b> It's not a serious problem.<br>
        <b>b)</b> Let's not get too excited.<br>
        <b>c)</b> What should we do in this new situation?<br>
        <b>d)</b> You're exaggerating a little.
      </div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">9</span>So boring! <span class="tag">idioms</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">English has colourful ways to say something is boring! Complete each sentence with a word from the box. ⏱ 14:22</p>
      </div>
      <img class="char" src="img/f/15-jack-shrug-left-w.jpg" style="width:18mm;flex:none;margin-top:-3mm">
    </div>
    <div class="chips" style="margin:1.6mm 0 2mm 10.8mm"><span>dragged</span><span>flew</span><span>paint</span><span>stiff</span><span>tears</span><span>thumbs</span></div>
    <table class="coll" style="margin-left:2mm">
      <tr><td>1. 😭 The lecture was so long that it bored me to <span class="blank s"></span>.</td></tr>
      <tr><td>2. 🎨 Honestly, that football match was like watching <span class="blank s"></span> dry.</td></tr>
      <tr><td>3. 👍 I sat in the waiting room twiddling my <span class="blank s"></span> for an hour.</td></tr>
      <tr><td>4. 🐌 The last hour of work really <span class="blank s"></span>.</td></tr>
      <tr><td>5. ✈️ We were having so much fun – time just <span class="blank s"></span>!</td></tr>
      <tr><td>6. 🥶 Two hours with nothing to do? I was bored <span class="blank s"></span>!</td></tr>
    </table>
    <div class="bub" style="margin-top:2.2mm">
      <img class="char" src="img/f/02-jack-lightbulb-idea-w.jpg" style="width:17mm;flex:none">
      <div class="txt"><b>Jack's tip:</b> <b>"Stiff"</b> means hard and difficult to move – so <i>bored stiff</i> is like your body is frozen by boredom! 🥶 And <b>time drags</b> 🐌 is the opposite of <b>time flies</b> ✈️.</div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">10</span>What do you do with time? <span class="tag">new! collocations</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Complete with <b>spent</b>, <b>kill</b>, <b>waste</b>, <b>save</b>, <b>make</b> or <b>take</b>. ⏱ 14:22 · 17:39</p>
      </div>
      <img class="char" src="img/f/51-jack-stopwatch-w.jpg" style="width:16mm;flex:none">
    </div>
    <div class="grid2" style="margin-top:2mm;gap:3mm;grid-template-columns:1.05fr .95fr">
      <table class="coll">
        <tr><td>1. 🚆 I <span class="blank s"></span> two hours on the train.</td></tr>
        <tr><td>2. 🎬 We had an hour to <span class="blank s"></span> before the film.</td></tr>
        <tr><td>3. 📱 Don't <span class="blank s"></span> your evening scrolling!</td></tr>
      </table>
      <table class="coll">
        <tr><td>4. 🛒 Shopping online can <span class="blank s"></span> you time.</td></tr>
        <tr><td>5. 🫖 I always <span class="blank s"></span> time for my tea.</td></tr>
        <tr><td>6. 🙂 No hurry – <span class="blank s"></span> your time!</td></tr>
      </table>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">⏳</span>Time flies or time drags? <span class="tag fun">your opinion · no points</span></h2>
    <p class="instr">How does time feel for <b>you</b> in each situation? Tick one – then say it: <i>"At a party, time flies!"</i></p>
    <div class="grid2" style="gap:0 6mm">
{FLIES}    </div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">11</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 17:39</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "I am boring." <span class="small">(you want to say how you feel)</span></td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "Time is not passing."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "I make nothing all weekend."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "I'm bored to wait."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "My phone is distracting me always."</td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/07-lucy-great-job-w.jpg" style="width:18mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> Words like <b>always</b>, <b>often</b> and <b>never</b> usually go <b>before</b> the main verb: <i>"My phone always distracts me."</i> And after <b>of</b>, use <b>-ing</b>: <i>"I'm tired of waiting."</i></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">🌱</span>Bored in a good way? <span class="tag fun">think · no points</span></h2>
        <p class="instr" style="margin-bottom:0">Does each habit help you use boredom well – or not? ⏱ 5:25 · 8:40 · 19:33</p>
      </div>
      <img class="char" src="img/f/73-lucy-calm-w.jpg" style="width:18mm;flex:none">
    </div>
    <div class="grid2" style="margin-top:2mm;gap:2.2mm">{GOODS}</div>
  </div>

  <div class="sec">
    <div class="card teal" style="display:grid;grid-template-columns:auto 1fr;gap:3.4mm;align-items:center;padding:2.8mm 4mm">
      <img class="char" src="img/f/55-jack-thumbs-up-w.jpg" style="width:20mm;border-radius:3mm">
      <div style="font-size:9pt;line-height:1.45"><b style="color:var(--night);font-size:9.6pt">⏱ Jack's two-minute rule</b><br>Feel the urge to grab your phone? Wait <b>two minutes</b>. Count your breaths, look out of the window – or describe what you see in English: <i>"There's a woman with a red umbrella. The bus is late again."</i> If the urge is still there, fine – now it's a <b>choice</b>, not an automatic movement.<div style="margin-top:1.6mm"><b style="color:var(--night)">Try it now!</b> Describe one thing you can see: <span class="blank" style="min-width:70mm"></span></div></div>
    </div>
  </div>
  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/62-lucy-birthday-cake-w.jpg" style="width:19mm;flex:none">
      <div class="txt"><b>Did you know? 🧸</b> Sandi Mann looked at children on long flights. Children with a <b>whole bag of toys</b> picked up each thing and moved on quickly. Children with <b>one toy at a time</b> stayed busy for much longer – and a plain notebook and a pen kept them happy for ages! Just like Jack's nephew and the box. 📦 ⏱ 8:40</div>
    </div>
  </div>
  {foot(7)}
</section>

<!-- ================= PAGE 8 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">12</span>Boredom crossword 🧩 <span class="tag">puzzle</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Read the clues and write the words in the grid (1 point each). The number in brackets is the number of letters. Letters that cross help you!</p>
    </div>
    <img class="char" src="img/f/50-lucy-puzzle-piece-w.jpg" style="width:19mm;flex:none;margin-top:-3mm">
  </div>
  <div style="margin-top:2.6mm">{X.grid_html(cw, 7.2)}</div>
  <div class="grid2 cclues" style="margin-top:2.6mm;gap:4mm">
    <div class="card white" style="padding:2.4mm 3.4mm"><h4>➡️ Across</h4>{ACROSS}</div>
    <div class="card white" style="padding:2.4mm 3.4mm"><h4>⬇️ Down</h4>{DOWN}</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">13</span>The train, the cow and the idea 🐄 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 0:05 and ⏱ 20:33. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/23-jack-hot-chocolate-w.jpg" style="width:17mm;flex:none">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">🤫</span><span>After about an hour, his mind went quiet.</span></div>
      <div class="ev"><span class="box"></span><span class="e">💡</span><span>Now he's calmer, with more ideas – even for the podcast!</span></div>
      <div class="ev"><span class="box"></span><span class="e">🔋</span><span>His phone was on three percent – soon it was dead.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🫖</span><span>He decided: the first twenty minutes of the day belong to him.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🐄</span><span>He sat staring at a cow, and the cow stared back.</span></div>
      <div class="ev"><span class="box"></span><span class="e">📱</span><span>He realised he always looked at his phone first thing in the morning.</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> Jack calls it "planned boredom". What would <b>your</b> first twenty minutes look like?<div class="lines"></div></div>
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
      <b style="color:var(--night);font-size:9.2pt">A. My most boring moment 🥱</b>
      <div class="small" style="margin-top:1mm">Use one idiom from Exercise 9. <i>e.g. "Waiting six hours at the airport was like watching paint dry."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. Bored in a good way 🌱</b>
      <div class="small" style="margin-top:1mm">Where will you be bored this week – and what will you do instead of your phone? <i>e.g. "At the bus stop, I'll look around."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">⏱</span>My five bored minutes <span class="tag fun">your 7-day mission</span></h2>
        <p class="instr" style="margin-bottom:0">Once a day, be bored for five minutes. No phone, no screen – just let your mind wander.</p>
      </div>
      <img class="char" src="img/f/58-lucy-autumn-walk-w.jpg" style="width:16mm;flex:none">
    </div>
    <table class="log week" style="margin-top:2mm">
      <tr><th>Day</th><th>Where</th><th>What I noticed – or my idea!</th><th>Done?</th></tr>
      <tr><td class="d">1</td><td class="a">🚌 waiting for the bus</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">2</td><td class="a">☕ while the kettle boils</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">3</td><td class="a">🚶 a walk, no headphones</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">4</td><td class="a">🪟 tea by the window</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">5</td><td class="a">🛒 standing in a queue</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">6</td><td class="a">🗣️ describe it in English</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">7</td><td class="a">📓 write one bored idea</td><td></td><td class="c"><span class="box sm"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:var(--peach-d)">🥱 SO BORING!</b>like watching paint dry<br>I'm bored stiff.<br>It bored me to tears.</div>
        <div><b style="color:var(--mauve-d)">⏳ TIME</b>Time dragged.<br>Time flew!<br>We had an hour to kill.</div>
        <div><b style="color:var(--sage-d)">🌱 GOOD BOREDOM</b>Let your mind wander.<br>Resist the urge.<br>the two-minute rule</div>
        <div><b style="color:#C0392B">⚠️ -ED or -ING?</b>I'm bored. ✓<br>It's boring. ✓<br>I'm boring. 😅</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain why boredom can sometimes help creativity.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>say "I'm bored" (not "I'm boring") – and explain why.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use idioms like "bored stiff" and "like watching paint dry".</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use spend, kill, waste and save with "time".</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/52-lucy-phone-comment-w.jpg" style="width:19mm;flex:none">
      <div class="txt"><b>Share it with us!</b> What's the most boring situation you've ever been in? Tell us in the comments with one of today's expressions: Was it <b>like watching paint dry</b>? Were you <b>bored stiff</b> – or <b>bored to tears</b>? 🐄</div>
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
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: b – 12 out of 18 men pressed it at least once (and 6 out of 24 women). · Predict: <b>bicycle</b> 🚲 isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 c · 2 h · 3 a · 4 f · 5 j · 6 b · 7 i · 8 d · 9 g · 10 e<br>Big idea: a (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 a · 2 c · 3 b · 4 c · 5 a · 6 b · 7 a · 8 b · 9 c · 10 b</p></div>
    <div class="k"><h3>4 · True or false?</h3><p>1 T · 2 F (Jack looked away first) · 3 F (most found it unpleasant) · 4 T · 5 T · 6 F (it was a small study – it doesn't prove that)</p></div>
    <div class="k"><h3>5 · Two studies and a train · 6 · Bored or boring?</h3><p>5: 1 B · 2 A · 3 C · 4 A · 5 C · 6 B<br>6: 1 boring · 2 bored · 3 interested · 4 interesting · 5 surprised · 6 tiring</p></div>
    <div class="k"><h3>7 · "That's the power gone!"</h3><p>1 power · 2 supposed · 3 stiff · 4 bad · 5 questions · 6 eat · 7 end · 8 carried · A cut · B scrolling</p></div>
    <div class="k"><h3>8 · Phrases to steal · 9 · So boring!</h3><p>8: 1 c · 2 d · 3 a · 4 b<br>9: 1 tears · 2 paint · 3 thumbs · 4 dragged · 5 flew · 6 stiff</p></div>
   </div>
   <div>
    <div class="k"><h3>10 · What do you do with time?</h3><p>1 spent · 2 kill · 3 waste · 4 save · 5 make · 6 take</p></div>
    <div class="k"><h3>11 · Say it better (2 points each)</h3><p>1 I'm bored. · 2 Time is going so slowly. / The day is really dragging. · 3 I did nothing all weekend. · 4 I'm bored of waiting. / I'm tired of waiting. · 5 My phone always distracts me. / I'm always getting distracted by my phone.<br><i>Bored in a good way?</i> helps: 1, 3, 5, 6 · doesn't help: 2, 4</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Crossword</h3><p>{{CW_KEY}}</p></div>{{CW_GRID}}</div>
    <div class="k"><h3>13 · The train story · 14 · Your turn</h3><p>1 🔋 three percent · 2 🐄 the cow · 3 🤫 mind went quiet · 4 📱 phone first thing · 5 🫖 twenty minutes · 6 💡 calmer, more ideas<br>14: your own answers – 2 points per good sentence.</p></div>
    <div class="k"><h3>Your score</h3><p>90–100 🏆 <b>Time flew!</b> · 70–89 ✨ <b>Not bored at all</b> · 50–69 🫖 <b>Planned boredom</b> · 0–49 🐄 <b>Stuck on the train – listen again!</b></p></div>
   </div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy every week. Next time you're stuck with nothing to do, don't panic: your mind might be getting ready to surprise you! 💡<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
    <img class="char" src="img/f/68-duo-coffee-night.jpg" style="width:40mm">
  </div>
  {foot(10)}
</section>

</body>
</html>
"""
across = " · ".join(f'{e["num"]} {e["word"].lower()}' for e in sorted([e for e in cw["entries"] if e["dir"] == "A"], key=lambda e: e["num"]))
down = " · ".join(f'{e["num"]} {e["word"].lower()}' for e in sorted([e for e in cw["entries"] if e["dir"] == "D"], key=lambda e: e["num"]))
assert "{CW_KEY}" in body and "{CW_GRID}" in body
body = body.replace("{CW_KEY}", f"<b>Across:</b> {across}<br><b>Down:</b> {down}").replace(
    "{CW_GRID}", X.grid_html(cw, 3.4, solved=True, cls="cw cwk"))
html = head + EXTRA + "</style>\n</head>\n<body>\n" + body
(HERE / "template.html").write_text(html)
pts = [int(x) for x in re.findall(r'tag pts">(\d+) points', html)]
print("points", sum(pts), pts)
