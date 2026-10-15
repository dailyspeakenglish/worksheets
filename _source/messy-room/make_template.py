"""Writes template.html for the messy-room worksheet (Podcast 59).
CSS design system copied from why-we-laugh (which includes time-flies' and build-a-habit's); crossword from cw.json.
Timestamps: from this episode the audio plays at normal speed, so video time = NoteGPT time + 5 s."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import crossword as X

src = (HERE.parent / "why-we-laugh" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Why We Laugh Worksheet", "Messy Room Worksheet")
cw = json.loads((HERE / "cw.json").read_text())
X.check(cw)
spec = json.loads((HERE / "cw_spec.json").read_text())
CLUES = {w.upper(): c for w, c in spec["words"]}
ACROSS, DOWN = X.clues_html(cw, CLUES)

EXTRA = """
/* ---- new in messy-room ---- */
.claim{display:inline-flex;align-items:center;gap:1.2mm;padding:.5mm 2.2mm .5mm 1mm;border-radius:10mm;font-size:7.6pt;font-weight:700;white-space:nowrap}
.claim.fair{background:#DDF1E3;color:#1E7B45;border:1.2px solid #8FCBA3}
.claim.strong{background:#FBE1DE;color:#C0392B;border:1.2px solid #EDA59D}
.claim .box{width:4.2mm;height:4.2mm;border-radius:1mm;border-width:1.2px}
.claim.fair .box{border-color:#1E7B45}.claim.strong .box{border-color:#C0392B}
.sort{border-collapse:separate;border-spacing:0 1.1mm;width:100%}
.sort th{font-size:8.3pt;font-weight:800;padding:1.4mm 1mm;text-align:center}
.sort th.it{text-align:left;color:var(--night);padding-left:1mm}
.sort th.keep{background:#DDF1E3;color:#1E7B45;border-radius:2.4mm 0 0 2.4mm}
.sort th.give{background:#DCEFF3;color:#1F5F70}
.sort th.out{background:#FBE1DE;color:#C0392B;border-radius:0 2.4mm 2.4mm 0}
.sort td{font-size:8.9pt;padding:.9mm 1mm;border-bottom:1px dashed var(--line)}
.sort td.c{text-align:center;width:27mm}
.sort td.k .box{border-color:#1E7B45}.sort td.g .box{border-color:#1F5F70}.sort td.o .box{border-color:#C0392B}
.studies{display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm}
.studies div{border-radius:3mm;padding:2mm 3mm;font-size:8.3pt;line-height:1.35;color:var(--ink)}
.studies .h{display:block;font-size:9.3pt;margin-bottom:.3mm}
.puts{display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm;margin-top:1.6mm}
.puts div{border-radius:3mm;padding:2mm 3mm;font-size:8.5pt;line-height:1.38;text-align:center}
.puts .e{display:block;font-size:15pt;line-height:1.2}
.puts b{display:block;color:var(--night);font-size:9.3pt}
.chat.wide .msg .b{max-width:154mm;padding:1.4mm 3.6mm}
.claim.calm{background:#DCEFF3;color:#1F5F70;border:1.2px solid #9CCAD6}.claim.calm .box{border-color:#1F5F70}
.claim.mess{background:#FDE3D3;color:#B9542B;border:1.2px solid #F2B796}.claim.mess .box{border-color:#B9542B}
.tm2{display:grid;grid-template-columns:1fr auto auto;gap:1.4mm;align-items:center;font-size:8.6pt;padding:.8mm 0;white-space:nowrap;border-bottom:1px dashed var(--line)}
.wf .blank{min-width:19mm}
.wf{display:grid;grid-template-columns:1fr 1fr;gap:1.8mm 5mm;font-size:9.1pt}
.keycols{display:grid;grid-template-columns:1fr 1fr;gap:2mm;margin-top:2.6mm;align-items:start}
.keycols>div{display:flex;flex-direction:column;gap:2mm}
.week td{height:6.4mm}
.week td.a{width:50mm;font-weight:600;color:var(--night)}
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
 ("JACK", "16-jack-surprised-left", f"Morning. What's all this? Why are there {gap(1)} bags everywhere?"),
 ("LUCY", "40-lucy-excited-right", f"I've decided. Today we're going to {gap(2)} up the living room. It's a <span style='white-space:nowrap'>complete {gap(3)}.</span>"),
 ("JACK", "15-jack-shrug-left", "Today? But it's Saturday."),
 ("LUCY", "38-lucy-explaining-right", f"I know, but I can't relax with all this clutter. There's {gap(4)} everywhere. Look at that pile of magazines."),
 ("JACK", "43-jack-explaining-left", f"Fair enough. Those are mine, I suppose. I'll go {gap(5)} them and get {gap(6)} of the old ones."),
 ("LUCY", "11-lucy-asking-right", f"Great. And can you put your shoes <span style='white-space:nowrap'>{gap(7)}?</span> They're in the middle of the floor again."),
 ("JACK", "13-jack-talking-left", "Okay, okay. What about all these cables?"),
 ("LUCY", "09-lucy-talking-right", f"Let's {gap(8)} them out. If we don't know what they're for, we throw them out."),
 ("JACK", "44-jack-embarrassed-left", "Wait, that one's important. I think."),
 ("LUCY", "12-lucy-laughing-right", "You said that last time. Okay, let's give it twenty minutes and then have a coffee."),
 ("JACK", "45-jack-agreeing-left", "Deal. Actually, this already feels better."),
])

def claim(i, text):
    return (f'<div class="sit"><div class="t" style="min-height:0"><b>{i}.</b> {text}</div><div class="ch" style="gap:2mm">'
            f'<span class="claim fair"><span class="box"></span>✓ FAIR TO SAY</span>'
            f'<span class="claim strong"><span class="box"></span>✗ TOO STRONG</span></div></div>')
CLAIMS = "".join(claim(i, t) for i, t in enumerate([
    "“Clutter causes stress – science has proved it!”",
    "“Clutter and stress seem to be connected.”",
    "“Everyone with a messy home is stressed.”",
    "“Maybe stressed people find it harder to tidy.”"], 1))

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
      <h1>What Your Messy Room Is Doing to Your Mind</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">What clutter does to stress and focus, when a bit of mess helps creativity, easy tidying tricks and phrasal verbs – and what Lucy found under "the chair".</p>
      <div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div style="background:var(--lav);border-radius:6mm;height:55mm;position:relative;overflow:hidden;border:1px solid var(--lav2)">
      <div style="position:absolute;z-index:2;top:3.4mm;left:4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">The keys were in the fridge?! 🔑</div>
      <img class="char" src="img/f/70-duo-surprised-lav.jpg" style="position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:63mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · After you listen 💬</div><div class="s">Solve the crossword, try the five-minute week and tell us what you found!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: My clutter check <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Be honest! Tick everything that is true for you right now. 😅</p>
    <div style="display:grid;grid-template-columns:1.42fr .58fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:1.8mm;justify-content:center;padding:2.6mm 3.6mm">
        <div class="conf" style="grid-template-columns:1fr 1fr;justify-content:stretch">
          <div><span class="box sm"></span>🪑 I have "the chair"</div>
          <div><span class="box sm"></span>✉️ I have a pile of letters</div>
          <div><span class="box sm"></span>🔌 I have too many chargers</div>
          <div><span class="box sm"></span>💻 10+ tabs are open now</div>
          <div><span class="box sm"></span>📱 I have apps I never use</div>
          <div><span class="box sm"></span>🔑 I lost my keys this month</div>
        </div>
        <div style="font-size:9pt"><b style="color:var(--night)">My clutter score:</b> <span class="blank s"></span> / 6</div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> Can a messy room ever be <b>good</b> for you?</div>
        <div style="display:flex;gap:3.4mm;font-size:8.7pt;white-space:nowrap"><span><span class="circ">a</span> no, never</span><span><span class="circ">b</span> yes – for creativity</span><span><span class="circ">c</span> only on Sundays</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 5:34</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:1.8mm 2.6mm;font-size:8.3pt;border:1.2px solid #F4D2C2;line-height:1.38"><b style="color:var(--night)">Jack:</b> "I lost my keys for forty minutes. They were in the fridge!" 🥛</div>
        <img class="char" src="img/f/72-jack-confused-peach.jpg" style="width:31mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – or write them in your notebook.</p>
    <div class="grid2" style="gap:2.4mm">
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>1.</b> Are you a tidy person or a messy person?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>2.</b> What's the messiest place in your home right now?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>3.</b> Can you study well at a messy desk?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>4.</b> What's something you should get rid of, but never do?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Then check at ⏱ 12:56 and ⏱ 13:51</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> clutter</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> to declutter</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> messy</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> tidy</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> to get rid of</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> overwhelming</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> stuff</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> to go through</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> to sort out</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> cortisol</td></tr>
      </table>
      <div class="card" style="font-size:9.1pt;line-height:1.62">
        <b>a)</b> to look at each item carefully<br>
        <b>b)</b> an informal word for "things"<br>
        <b>c)</b> a lot of things in one place, in an untidy way<br>
        <b>d)</b> to throw away, sell or give away something you don't want<br>
        <b>e)</b> organised, with everything in its place<br>
        <b>f)</b> a stress hormone in your body<br>
        <b>g)</b> to remove things you don't need, to make a space tidier<br>
        <b>h)</b> so big or so much that you feel you can't deal with it<br>
        <b>i)</b> to organise something, or solve a problem with it<br>
        <b>j)</b> untidy, with things in the wrong places
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/03-lucy-did-you-know-w.jpg" style="width:24mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> <b style="color:var(--peach-d)">CLUT</b>-ter · de-<b style="color:var(--peach-d)">CLUT</b>-ter · o-ver-<b style="color:var(--peach-d)">WHELM</b>-ing · <b style="color:var(--peach-d)">COR</b>-ti-sol · <span style="white-space:nowrap"><b style="color:var(--peach-d)">TI</b>-dy (/ˈtaɪdi/).</span> Say it out loud: <i>"Your bedroom looks like a bomb's hit it!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>You need a perfect, empty home to be happy and creative.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>Clutter can affect stress and focus, a little mess can help creativity – and small, easy steps make a space calmer.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>Mess has no effect on our brain at all, so there's no reason to tidy.</div>
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
      <div class="chips predict-chips" style="margin-top:2mm;justify-content:center;gap:1.4mm"><span>fridge</span><span>chargers</span><span>ping pong balls</span><span>chess</span><span>umbrella</span><span>voucher</span><span>envelope</span><span>magazines</span></div>
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
    <div class="mcq"><div class="qq">1. "Clutter" is…</div><div class="opt"><span class="c">a</span>a lot of things in an untidy way</div><div class="opt"><span class="c">b</span>a type of cleaning spray</div><div class="opt"><span class="c">c</span>a very tidy room</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">2. Your desk has too many papers on it, but it isn't dirty. You need to ______ it.</div><div class="opt"><span class="c">a</span>clean</div><div class="opt"><span class="c">b</span>tidy</div><div class="opt"><span class="c">c</span>wash</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">3. "I threw ______ my old clothes."</div><div class="opt"><span class="c">a</span>at</div><div class="opt"><span class="c">b</span>on</div><div class="opt"><span class="c">c</span>away</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">4. The opposite of "messy" is…</div><div class="opt"><span class="c">a</span>tidy</div><div class="opt"><span class="c">b</span>busy</div><div class="opt"><span class="c">c</span>quiet</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">5. "Stuff" is an informal word for…</div><div class="opt"><span class="c">a</span>people</div><div class="opt"><span class="c">b</span>things</div><div class="opt"><span class="c">c</span>places</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. Where did Jack find his keys?</div><div class="opt"><span class="c">a</span>in an old coat</div><div class="opt"><span class="c">b</span>in the fridge</div><div class="opt"><span class="c">c</span>under a pile of papers</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">7. In the Los Angeles study, people gave the researchers…</div><div class="opt"><span class="c">a</span>a video tour of their home</div><div class="opt"><span class="c">b</span>photos of their kitchen</div><div class="opt"><span class="c">c</span>a cleaning diary</div><div class="hint">🎧 ⏱ 2:38</div></div>
    <div class="mcq"><div class="qq">8. In the Minnesota study, people in the messy room…</div><div class="opt"><span class="c">a</span>chose more apples</div><div class="opt"><span class="c">b</span>had more creative ideas</div><div class="opt"><span class="c">c</span>gave more money to charity</div><div class="hint">🎧 ⏱ 5:34</div></div>
    <div class="mcq"><div class="qq">9. How many apps did Jack delete from his phone?</div><div class="opt"><span class="c">a</span>3</div><div class="opt"><span class="c">b</span>31</div><div class="opt"><span class="c">c</span>23</div><div class="hint">🎧 ⏱ 10:09</div></div>
    <div class="mcq"><div class="qq">10. What was in the envelope under Lucy's chair?</div><div class="opt"><span class="c">a</span>a bill</div><div class="opt"><span class="c">b</span>a voucher for a cooking class</div><div class="opt"><span class="c">c</span>an old train ticket</div><div class="hint">🎧 ⏱ 18:39</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🧩</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> Jack had <b>31 tabs</b> open, about <b>4,000</b> unread emails – and three chess apps. He doesn't play chess! ♟️</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">4</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>Jack's keys were next to the milk.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>The Los Angeles study looked mainly at how messy the homes really were.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:38</td></tr>
      <tr><td class="n">3</td><td>Normally, cortisol is higher in the morning and goes down during the day.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 3:48</td></tr>
      <tr><td class="n">4</td><td>People from the tidy room were more likely to choose an apple.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:34</td></tr>
      <tr><td class="n">5</td><td>Lucy says a perfect, magazine-style home is the goal.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 6:52</td></tr>
      <tr><td class="n">6</td><td>Jack says a messy home always means a person is lazy.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 6:52</td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">5</span>Three studies 🔍 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Which study is each sentence about? Write <b>A</b>, <b>B</b> or <b>C</b>. ⏱ 2:38 · 4:48 · 5:34</p>
      </div>
      <img class="char" src="img/f/46-lucy-magnifying-glass-w.jpg" style="width:19mm;flex:none">
    </div>
    <div class="studies" style="margin-top:2mm">
      <div style="background:var(--peach-l)"><b class="h" style="color:var(--peach-d)">A · Los Angeles 🏠</b>2010 · homes, words and stress hormones</div>
      <div style="background:var(--lav)"><b class="h" style="color:var(--mauve-d)">B · Princeton 🧠</b>brain scientists · objects and attention</div>
      <div style="background:var(--sage)"><b class="h" style="color:var(--sage-d)">C · Minnesota 🏓</b>2013 · tidy room vs messy room</div>
    </div>
    <table class="tf" style="margin-top:1.6mm">
      <tr><td class="n">1</td><td>People in a messy room had more creative ideas for ping pong balls.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">2</td><td>Lots of objects in front of us compete for our attention.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">3</td><td>Women who described their homes as cluttered had a flatter cortisol pattern.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">4</td><td>People from a tidy room were more likely to give money to charity.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">5</td><td>Researchers studied the words people used on a video tour of their home.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">6</td><td>A messy desk is like trying to listen to someone in a noisy room.</td><td class="ck"><span class="box"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">6</span>Link or proof? <span class="tag">new! think like a scientist</span><span class="tag pts">4 points</span></h2>
        <p class="instr" style="margin-bottom:0">The Los Angeles study found a <b>link</b> between clutter and stress – not <b>proof</b>. Is each sentence fair to say, or too strong? ⏱ 3:48</p>
      </div>
      <img class="char" src="img/f/20-jack-glasses-laptop-w.jpg" style="width:19mm;flex:none">
    </div>
    <div class="grid2" style="margin-top:2mm;gap:2.2mm">{CLAIMS}</div>
    <div class="small" style="margin:1.8mm 0 0 1mm">✏️ <b>Bonus</b> (no points): make this headline fair. <i>"MESSY HOMES MAKE YOU ILL!"</i> → <span class="blank l"></span></div>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>"It's a complete mess!" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Two flatmates on a Saturday morning. Listen at ⏱ 11:53 and write <b>one word</b> in each gap (1–8). Then answer A and B. The breakdown at ⏱ 12:56 can help.</p>
    </div>
    <img class="char" src="img/f/27-lucy-morning-stretch-w.jpg" style="width:22mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat wide" style="margin-top:2.6mm;gap:1.2mm">
{CHAT}
  </div>
  <div class="grid2" style="margin-top:2.6mm;gap:3mm">
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">A.</b> Jack's <b>one word</b> for "OK, I agree!": <span class="blank" style="min-width:22mm"></span></div>
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">B.</b> Americans call <b>bin bags</b>… <span class="blank" style="min-width:28mm"></span></div>
  </div>
  <div class="sec" style="margin-top:3.6mm">
    <h2><span class="num">💡</span>Away, down or on? <span class="tag fun">small words · no points</span></h2>
    <p class="instr" style="margin-bottom:0">One verb, three meanings! Listen for these at ⏱ 12:56 and ⏱ 16:15.</p>
    <div class="puts">
      <div style="background:var(--sage)"><span class="e">👟 ➜ 🗄️</span><b>Put your shoes away.</b>Put them in their proper place.</div>
      <div style="background:var(--lav)"><span class="e">👟 ⬇️</span><b>Put your shoes down.</b>Just place them somewhere.</div>
      <div style="background:var(--peach-l)"><span class="e">👟 🚶</span><b>Put your shoes on.</b>Wear them – we're going out!</div>
    </div>
  </div>
  <div class="small" style="margin-top:2.4mm;text-align:center">🎭 <b>Say it out loud!</b> Play both parts – then talk about <b>your</b> living room: what would you sort out first?</div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">8</span>Tidying phrasal verbs <span class="tag">new! small words, big difference</span><span class="tag pts">8 points</span></h2>
      <p class="instr" style="margin-bottom:0">Complete each sentence with a word from the box. Some are used twice. <span style="white-space:nowrap">⏱ 12:56 · 16:15</span></p>
    </div>
    <img class="char" src="img/f/47-jack-pointing-right-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chips" style="margin:1.6mm 0 2mm 10.8mm"><span>away</span><span>on</span><span>out</span><span>rid</span><span>through</span><span>up</span></div>
  <table class="coll" style="margin-left:2mm">
    <tr><td>1. Let's tidy <span class="blank s"></span> the living room before our friends arrive.</td></tr>
    <tr><td>2. Can you put your shoes <span class="blank s"></span>? They're in the middle of the floor.</td></tr>
    <tr><td>3. I'll go <span class="blank s"></span> these old magazines and keep the good ones.</td></tr>
    <tr><td>4. I finally got <span class="blank s"></span> of my old sofa.</td></tr>
    <tr><td>5. We don't know what these cables are for. Let's throw them <span class="blank s"></span>.</td></tr>
    <tr><td>6. Don't throw your old books in the bin – give them <span class="blank s"></span> to someone who needs them.</td></tr>
    <tr><td>7. These cables are a mess. Let's sort them <span class="blank s"></span>.</td></tr>
    <tr><td>8. Put your shoes <span class="blank s"></span> – it's raining and we're going out!</td></tr>
  </table>
  <div class="bub" style="margin-top:2.2mm">
    <img class="char" src="img/f/02-jack-lightbulb-idea-w.jpg" style="width:17mm;flex:none">
    <div class="txt"><b>Jack's tip:</b> With <b>it</b> or <b>them</b>, the small word goes at the <b>end</b>: <i>"Throw it away."</i> ✓ · <i>"Put them away."</i> ✓ – not <i>"throw away it"</i> ✗.</div>
  </div>

  <div class="sec">
    <h2><span class="num">9</span>Clean or tidy? + home jobs <span class="tag">new! collocations</span><span class="tag pts">6 points</span></h2>
    <p class="instr" style="margin-bottom:0"><b>Clean</b> = remove dirt and dust. <b>Tidy</b> = put things in order. Write <b>clean</b> or <b>tidy</b> (1–3), then <b>make</b>, <b>do</b> or <b>take</b> (4–6). ⏱ 16:15</p>
    <div class="grid2" style="margin-top:2mm;gap:3mm;grid-template-columns:1.12fr .88fr">
      <table class="coll">
        <tr><td>1. 📄 Papers everywhere? I need to <span class="blank s"></span> my desk.</td></tr>
        <tr><td>2. 🧽 The floor is sticky. I need to <span class="blank s"></span> it.</td></tr>
        <tr><td>3. 🪶 Dust on every shelf? Time to <span class="blank s"></span> them!</td></tr>
      </table>
      <table class="coll">
        <tr><td>4. 🛏️ Every morning I <span class="blank s"></span> the bed.</td></tr>
        <tr><td>5. 🍽️ We <span class="blank s"></span> the washing-up.</td></tr>
        <tr><td>6. 🗑️ Can you <span class="blank s"></span> out the rubbish?</td></tr>
      </table>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">🌳</span>Word family <span class="tag fun">bonus · no points</span></h2>
    <p class="instr">Change the word in CAPITALS so it fits the sentence. ⏱ 13:51</p>
    <div class="card white wf" style="padding:2.6mm 4mm">
      <div>a) My desk is very <span class="blank"></span>. <b style="color:var(--mauve)">(CLUTTER)</b></div>
      <div>b) His room is always <span class="blank"></span>. <b style="color:var(--mauve)">(MESS)</b></div>
      <div>c) My plans are a <span class="blank"></span>. <b style="color:var(--mauve)">(MESSY)</b></div>
      <div>d) There are books about <span class="blank"></span>. <b style="color:var(--mauve)">(DECLUTTER)</b></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">🎨</span>Tidy desk or a bit of mess? <span class="tag fun">think · no points</span></h2>
    <p class="instr">It depends on what you need! Tick the better space for each job. ⏱ 5:34 · 6:52</p>
    <div class="grid2" style="gap:0 6mm">
      <div class="tm2"><span>1. 📖 studying for a test</span><span class="claim calm"><span class="box"></span>🧘 tidy</span><span class="claim mess"><span class="box"></span>🎨 messy</span></div>
      <div class="tm2"><span>2. 💡 brainstorming ideas</span><span class="claim calm"><span class="box"></span>🧘 tidy</span><span class="claim mess"><span class="box"></span>🎨 messy</span></div>
      <div class="tm2"><span>3. ⏰ a new morning routine</span><span class="claim calm"><span class="box"></span>🧘 tidy</span><span class="claim mess"><span class="box"></span>🎨 messy</span></div>
      <div class="tm2"><span>4. 🖌️ painting a picture</span><span class="claim calm"><span class="box"></span>🧘 tidy</span><span class="claim mess"><span class="box"></span>🎨 messy</span></div>
      <div class="tm2"><span>5. 🍎 choosing a healthy snack</span><span class="claim calm"><span class="box"></span>🧘 tidy</span><span class="claim mess"><span class="box"></span>🎨 messy</span></div>
      <div class="tm2"><span>6. ♻️ new uses for old things</span><span class="claim calm"><span class="box"></span>🧘 tidy</span><span class="claim mess"><span class="box"></span>🎨 messy</span></div>
    </div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">10</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 16:15</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "I will collect my room."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "My room is very complex."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "I threw the old clothes." <span class="small">(into the bin)</span></td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "Put your shoes." <span class="small">(in the cupboard)</span></td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "There are many things everywhere."</td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/01-lucy-thumbs-up-w.jpg" style="width:18mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> "Tidy" is very British. In American English, people often say <b>"neat"</b> (a neat room) or <b>"clean up"</b> (clean up your room). Both are fine!</div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">11</span>Tidy sayings <span class="tag">expressions</span><span class="tag pts">4 points</span></h2>
        <p class="instr" style="margin-bottom:0">Match each expression (1–4) to its meaning (a–d). ⏱ 8:01 · 13:51</p>
      </div>
      <img class="char" src="img/f/71-lucy-embarrassed-w.jpg" style="width:18mm;flex:none">
    </div>
    <div class="grid2" style="margin-top:2mm;gap:4mm;align-items:start">
      <table class="match" style="font-size:9.2pt">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> "It looks like a bomb's hit it!"</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> "A place for everything, and everything in its place."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> "One in, one out."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> the five-minute rule</td></tr>
      </table>
      <div class="card" style="font-size:8.9pt;line-height:1.6">
        <b>a)</b> an old saying about being organised<br>
        <b>b)</b> tidy one small area for five minutes – then you can stop<br>
        <b>c)</b> a place is extremely messy<br>
        <b>d)</b> when something new comes home, an old thing goes
      </div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">🗂️</span>Keep, give away or throw out? <span class="tag fun">your choice · no points</span></h2>
        <p class="instr" style="margin-bottom:0">There's no wrong answer! Decide, then say it out loud: <i>"I'd keep the book." · "I'd give away the jumper."</i></p>
      </div>
      <img class="char" src="img/f/61-jack-shopping-w.jpg" style="width:18mm;flex:none">
    </div>
    <div class="card white" style="margin-top:2mm;padding:1.6mm 3.4mm 2.2mm">
      <table class="sort">
        <tr><th class="it">Tick one box for each thing</th><th class="keep">💚 KEEP</th><th class="give">💙 GIVE AWAY</th><th class="out">🗑️ THROW OUT</th></tr>
        <tr><td>👕 a jumper you haven't worn for three years</td><td class="c k"><span class="box sm"></span></td><td class="c g"><span class="box sm"></span></td><td class="c o"><span class="box sm"></span></td></tr>
        <tr><td>🔌 a cable – nobody knows what it's for</td><td class="c k"><span class="box sm"></span></td><td class="c g"><span class="box sm"></span></td><td class="c o"><span class="box sm"></span></td></tr>
        <tr><td>📚 a book you loved, but won't read again</td><td class="c k"><span class="box sm"></span></td><td class="c g"><span class="box sm"></span></td><td class="c o"><span class="box sm"></span></td></tr>
        <tr><td>🧸 a toy from your childhood</td><td class="c k"><span class="box sm"></span></td><td class="c g"><span class="box sm"></span></td><td class="c o"><span class="box sm"></span></td></tr>
        <tr><td>🎫 two old train tickets</td><td class="c k"><span class="box sm"></span></td><td class="c g"><span class="box sm"></span></td><td class="c o"><span class="box sm"></span></td></tr>
        <tr><td>🎂 a birthday card from your best friend</td><td class="c k"><span class="box sm"></span></td><td class="c g"><span class="box sm"></span></td><td class="c o"><span class="box sm"></span></td></tr>
      </table>
    </div>
  </div>
  {foot(7)}
</section>

<!-- ================= PAGE 8 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">12</span>Tidy-up crossword 🧩 <span class="tag">puzzle</span><span class="tag pts">10 points</span></h2>
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
        <h2><span class="num">13</span>The chair story 🪑 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 18:39. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/56-lucy-cooking-w.jpg" style="width:18mm;flex:none">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">💌</span><span>At the very bottom, she found an unopened envelope.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🎂</span><span>At a busy birthday dinner in August, Lucy's brother gave her an envelope.</span></div>
      <div class="ev"><span class="box"></span><span class="e">📞</span><span>She called her brother to say thank you.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🧥</span><span>She put it in her jacket pocket, and the jacket went on the chair.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🍝</span><span>She booked the cooking class – it expired the next Saturday!</span></div>
      <div class="ev"><span class="box"></span><span class="e">🪑</span><span>Last Saturday, Lucy finally cleared the chair.</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> Why did Lucy's brother think she hated his present?<div class="lines"></div></div>
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
      <b style="color:var(--night);font-size:9.2pt">A. Five minutes later… 🔍</b>
      <div class="small" style="margin-top:1mm">Tidy one drawer or shelf for five minutes. What did you find? What did you get rid of? <i>e.g. "I found two old train tickets in the back of a drawer."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. My study space plan 📚</b>
      <div class="small" style="margin-top:1mm">How will you get your desk ready in two minutes? <i>e.g. "Before I study, I'll put everything else in a box."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">⏱</span>My five-minute week <span class="tag fun">your 7-day mission</span></h2>
        <p class="instr" style="margin-bottom:0">Set a timer for five minutes each day. When it stops, you can stop!</p>
      </div>
      <img class="char" src="img/f/51-jack-stopwatch-w.jpg" style="width:17mm;flex:none">
    </div>
    <table class="log week" style="margin-top:2mm">
      <tr><th>Day</th><th>Area</th><th>What I found or got rid of</th><th>Done?</th></tr>
      <tr><td class="d">1</td><td class="a">🗄️ one drawer</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">2</td><td class="a">🖥️ my desk</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">3</td><td class="a">📱 my phone's home screen</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">4</td><td class="a">🪑 "the chair"</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">5</td><td class="a">👜 my bag</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">6</td><td class="a">📚 one shelf</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">7</td><td class="a">✉️ the letter pile</td><td></td><td class="c"><span class="box sm"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:var(--sage-d)">🧹 TIDY UP</b>Let's tidy up.<br>Put it away, please.<br>Let's sort it out.</div>
        <div><b style="color:#C0392B">🗑️ GET RID OF</b>throw it away / out<br>give it away<br>I got rid of…</div>
        <div><b style="color:var(--peach-d)">😱 WHAT A MESS!</b>It's a complete mess.<br>There's stuff everywhere.<br>A bomb's hit it!</div>
        <div><b style="color:var(--mauve-d)">✨ RULES</b>the five-minute rule<br>a place for everything<br>one in, one out</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain what clutter can do to stress and focus.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use tidy up, put away, get rid of and sort out.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>explain the difference between clean and tidy.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>say when a study shows a link, not proof.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/52-lucy-phone-comment-w.jpg" style="width:19mm;flex:none">
      <div class="txt"><b>Share it with us!</b> Give one small area five minutes – then tell us in the comments what you found! Use <b>"I finally got rid of…"</b> or <b>"I found… in the back of a drawer."</b> And do you have "the chair" too? 🪑💜</div>
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
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: b – in one study, people in a messy room had more creative ideas. · Predict: <b>umbrella</b> ☂️ isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 c · 2 g · 3 j · 4 e · 5 d · 6 h · 7 b · 8 a · 9 i · 10 f<br>Big idea: b (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 a · 2 b · 3 c · 4 a · 5 b · 6 b · 7 a · 8 b · 9 c · 10 b</p></div>
    <div class="k"><h3>4 · True or false?</h3><p>1 T · 2 F (how people described their homes) · 3 T · 4 T · 5 F (a perfect home isn't the goal) · 6 F (it's not because people are lazy)</p></div>
    <div class="k"><h3>5 · Three studies · 6 · Link or proof?</h3><p>5: 1 C · 2 B · 3 A · 4 C · 5 A · 6 B<br>6: 1 too strong · 2 fair to say · 3 too strong · 4 fair to say<br><i>Bonus, e.g.:</i> "Messy homes may be linked to stress."</p></div>
    <div class="k"><h3>7 · "It's a complete mess!"</h3><p>1 bin · 2 tidy · 3 mess · 4 stuff · 5 through · 6 rid · 7 away · 8 sort · A Deal! · B trash bags</p></div>
    <div class="k"><h3>8 · Tidying phrasal verbs</h3><p>1 up · 2 away · 3 through · 4 rid · 5 out (away is also correct) · 6 away · 7 out · 8 on</p></div>
    <div class="k"><h3>11 · Tidy sayings</h3><p>1 c · 2 a · 3 d · 4 b</p></div>
   </div>
   <div>
    <div class="k"><h3>9 · Clean or tidy? + home jobs</h3><p>1 tidy · 2 clean · 3 clean · 4 make · 5 do · 6 take<br><i>Word family:</i> a cluttered · b messy · c mess · d decluttering<br><i>Tidy or mess?</i> 1 tidy · 2 mess · 3 tidy · 4 mess · 5 tidy · 6 mess</p></div>
    <div class="k"><h3>10 · Say it better (2 points each)</h3><p>1 I'm going to tidy my room. / I'm going to tidy up. · 2 My room is really messy / untidy. · 3 I threw away my old clothes. / I threw out… / I gave away… · 4 Put your shoes away. · 5 There's stuff everywhere.</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Crossword</h3><p>{{CW_KEY}}</p></div>{{CW_GRID}}</div>
    <div class="k"><h3>13 · The chair story · 14 · Your turn</h3><p>1 🎂 birthday dinner · 2 🧥 jacket on the chair · 3 🪑 cleared the chair · 4 💌 the envelope · 5 🍝 booked the class · 6 📞 called her brother<br><i>Think about it:</i> she never mentioned it for two months – the envelope was lost on the chair!<br>14: your own answers – 2 points per good sentence.</p></div>
    <div class="k"><h3>Your score</h3><p>90–100 🏆 <b>Tidy genius!</b> · 70–89 ✨ <b>Everything in its place</b> · 50–69 🧹 <b>Tidying up</b> · 0–49 🪑 <b>Still under the chair – listen again!</b></p></div>
   </div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy every week. And give one small corner five minutes this week! 🧹<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
    <img class="char" src="img/f/29-duo-high-five-night.jpg" style="width:37mm">
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
    "{CW_GRID}", X.grid_html(cw, 3.6, solved=True, cls="cw cwk"))
html = head + EXTRA + "</style>\n</head>\n<body>\n" + body
(HERE / "template.html").write_text(html)
pts = [int(x) for x in re.findall(r'tag pts">(\d+) points', html)]
print("points", sum(pts), pts)
