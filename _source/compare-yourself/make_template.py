"""Writes template.html for the compare-yourself worksheet (Podcast 67).
CSS design system copied from put-things-off (which includes all earlier worksheets).
Crossword from cw.json (built by _source/tools/crossword.py). Timestamps: video time = NoteGPT time + 5 s."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import crossword as X

src = (HERE.parent / "put-things-off" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Put Things Off Worksheet", "Compare Yourself Worksheet")
cw = json.loads((HERE / "cw.json").read_text())
X.check(cw)
spec = json.loads((HERE / "cw_spec.json").read_text())
CLUES = {w.upper(): c for w, c in spec["words"]}
ACROSS, DOWN = X.clues_html(cw, CLUES)

EXTRA = """
/* ---- new in compare-yourself ---- */
.podwrap{display:grid;grid-template-columns:60mm 1fr;gap:4mm;align-items:center;margin-top:1.8mm}
.podium{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2mm;align-items:end;background:var(--lav);border-radius:4mm;padding:2.4mm 2.4mm 0}
.podium .st{border-radius:2mm 2mm 0 0;text-align:center;color:var(--night);font-weight:800;font-size:13pt;padding-top:1mm}
.podium .th{background:#fff;border:1.2px solid var(--line);border-radius:2.4mm;padding:1.1mm 1.2mm;font-size:7.3pt;line-height:1.3;text-align:center;margin-bottom:1.2mm}
.podium .th b{display:block;font-size:7.8pt}
.podwrap .tm2{grid-template-columns:1fr auto auto;white-space:normal;padding:1mm 0;font-size:8.5pt}
.podwrap .tm2 .claim{white-space:nowrap}
.claim.up{background:#FDE3D3;color:#B9542B;border:1.2px solid #F2B796}.claim.up .box{border-color:#B9542B}
.claim.dn{background:#DCEFF3;color:#1F5F70;border:1.2px solid #9CCAD6}.claim.dn .box{border-color:#1F5F70}
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
 ("LUCY", "11-lucy-asking-right", f"Hi, Uncle Jack. Can I ask you something? Do you think my English is {gap(1)}?"),
 ("JACK", "16-jack-surprised-left", "Bad? Not at all. Why do you ask?"),
 ("LUCY", "37-lucy-thinking-right", f"I've just been watching a girl my age online. Her English is {gap(2)}. She sounds like a native speaker. {gap(3)} to her, I sound terrible."),
 ("JACK", "43-jack-explaining-left", f"{gap(4)} on. How long has she been learning?"),
 ("LUCY", "38-lucy-explaining-right", "I don't know. Maybe she grew up abroad."),
 ("JACK", "13-jack-talking-left", f"Exactly. You don't know her story. And I {gap(5)} she didn't get it right the first time either."),
 ("LUCY", "09-lucy-talking-right", f"I suppose so. But I just don't {gap(6)} up."),
 ("JACK", "14-jack-listening-left", f"Listen. Do you remember the message you sent me in English last {gap(7)}?"),
 ("LUCY", "12-lucy-laughing-right", f"Oh, don't {gap(8)} me. It was full of mistakes."),
 ("JACK", "45-jack-agreeing-left", "And today you're explaining your feelings to me in English, without even thinking about it. That's real progress."),
 ("LUCY", "40-lucy-excited-right", "Hmm. When you put it like that, I feel a bit better."),
 ("JACK", "41-jack-laughing-left", f"The grass is always {gap(9)}, you know. Keep your eyes on your own {gap(10)}."),
 ("LUCY", "39-lucy-caring-right", "Thanks. I needed to hear that."),
])

UD = [("🥈 “I was so close to gold!”", "up"), ("🥉 “Wow – at least I got a medal!”", "dn"),
      ("🍅 “My neighbour grew a whole basket.”", "up"), ("😏 “At least I'm not as bad as him.”", "dn"),
      ("📱 “She sounds like a native speaker. I sound terrible.”", "up"), ("🏃 “Some runners didn't even finish the race.”", "dn")]
UDS = "".join(f'      <div class="tm2"><span>{i}. {t}</span><span class="claim up"><span class="box"></span>⬆️ upward</span><span class="claim dn"><span class="box"></span>⬇️ downward</span></div>\n' for i, (t, _) in enumerate(UD, 1))
UD_KEY = " · ".join(f"{i} {'upward' if k == 'up' else 'downward'}" for i, (_, k) in enumerate(UD, 1))

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
      <h1>Why We Compare Ourselves to Others (And How to Stop)</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">Why your brain compares, why bronze medal winners look happier than silver, what happened when students cut social media, comparatives and natural English for envy and progress – and Jack's five tomatoes.</p>
      <div style="margin-top:3.4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div class="hero2">
      <div style="position:absolute;z-index:2;top:3.4mm;left:3.4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">"Five perfect tomatoes!" 🍅🍅🍅🍅🍅</div>
      <img class="char" src="img/f/36-lucy-surprised-right-lav.jpg" style="position:absolute;bottom:0;left:2mm;width:35mm">
      <img class="char" src="img/f/55-jack-thumbs-up-lav.jpg" style="position:absolute;bottom:0;right:1mm;width:36mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · After you listen 🥉</div><div class="s">Jack's tip: the only person you should compare your answers with is yourself!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: My comparison check <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Be honest! Tick everything that is true for you. 😊</p>
    <div style="display:grid;grid-template-columns:1.42fr .58fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:1.8mm;justify-content:center;padding:2.6mm 3.6mm">
        <div class="conf" style="grid-template-columns:1fr 1fr;justify-content:stretch;font-size:8.7pt">
          <div><span class="box sm"></span>📱 I feel worse after scrolling</div>
          <div><span class="box sm"></span>🗣️ I compare my English a lot</div>
          <div><span class="box sm"></span>👨‍👧 I compare myself to family</div>
          <div><span class="box sm"></span>🏠 I compare homes or salaries</div>
          <div><span class="box sm"></span>🎉 I'm happy for friends' success</div>
          <div><span class="box sm"></span>🔁 I compare with my past self</div>
        </div>
        <div style="font-size:9pt"><b style="color:var(--night)">My comparison score:</b> <span class="blank s"></span> / 6</div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> At the Olympics, who looked happier just after winning a medal?</div>
        <div style="display:flex;gap:3.4mm;font-size:8.7pt;white-space:nowrap"><span><span class="circ">a</span> 🥈 silver winners</span><span><span class="circ">b</span> 🥉 bronze winners</span><span><span class="circ">c</span> they looked the same</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 4:46</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:1.8mm 2.4mm;font-size:8.1pt;border:1.2px solid #F4D2C2;line-height:1.36"><b style="color:var(--night)">Lucy:</b> "Jack, you were a bronze medal gardener!" 🥉</div>
        <img class="char" src="img/f/64-lucy-plant-peach.jpg" style="width:28mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – or write them in your notebook.</p>
    <div class="grid2" style="gap:2.4mm">
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>1.</b> Who do you compare yourself to most often?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>2.</b> Does comparing make you feel inspired or worse?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>3.</b> How is your English better than a year ago?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>4.</b> Why do people only post their best moments?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Then check at ⏱ 1:41 · 4:46 · 14:43</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> to compare</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> envious</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> to show off</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> a highlight reel</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> to measure up</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> progress</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> upward comparison</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> downward comparison</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> agony</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> ecstasy</td></tr>
      </table>
      <div class="card" style="font-size:9pt;line-height:1.55">
        <b>a)</b> moving forward and getting better over time<br>
        <b>b)</b> terrible pain<br>
        <b>c)</b> to be as good as someone or something expects<br>
        <b>d)</b> wanting something that another person has<br>
        <b>e)</b> comparing yourself to someone who seems better off<br>
        <b>f)</b> extreme happiness<br>
        <b>g)</b> to look at two things to see how they're similar or different<br>
        <b>h)</b> a short video of only the best moments<br>
        <b>i)</b> comparing yourself to someone who seems worse off<br>
        <b>j)</b> to try to make people notice how good, rich or clever you are
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/03-lucy-did-you-know-w.jpg" style="width:20mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> com-<b style="color:var(--peach-d)">PARE</b> · com-<b style="color:var(--peach-d)">PAR</b>-i-son · <b style="color:var(--peach-d)">EN</b>-vi-ous · <b style="color:var(--peach-d)">PRO</b>-gress (noun) · <span style="white-space:nowrap"><b style="color:var(--peach-d)">EC</b>-sta-sy.</span> Say it: <i>"I'm not as fluent as her – yet!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>Comparing is natural, but how we feel depends on who we compare with – so compare with your past self and celebrate your progress.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>You should always compare yourself with the best people in the world.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>Comparing yourself with others is always good for you.</div>
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
      <div class="chips predict-chips" style="margin-top:2mm;justify-content:center;gap:1.4mm"><span>tomatoes</span><span>basket</span><span>medal</span><span>corner shop</span><span>seeds</span><span>birds</span><span>swimming pool</span><span>notebook</span></div>
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
    <div class="mcq"><div class="qq">1. "He's ______ than me at football."</div><div class="opt"><span class="c">a</span>more better</div><div class="opt"><span class="c">b</span>more good</div><div class="opt"><span class="c">c</span>better</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">2. "She's ______ than her sister."</div><div class="opt"><span class="c">a</span>taller</div><div class="opt"><span class="c">b</span>more tall</div><div class="opt"><span class="c">c</span>tallest</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">3. "I'm not ______ good ______ her – yet!"</div><div class="opt"><span class="c">a</span>so … that</div><div class="opt"><span class="c">b</span>as … as</div><div class="opt"><span class="c">c</span>more … than</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">4. "I've made a lot of ______ this year."</div><div class="opt"><span class="c">a</span>progresses</div><div class="opt"><span class="c">b</span>progress</div><div class="opt"><span class="c">c</span>a progress</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">5. "Comparison is the thief of joy." A thief is someone who…</div><div class="opt"><span class="c">a</span>steals</div><div class="opt"><span class="c">b</span>teaches</div><div class="opt"><span class="c">c</span>sings</div><div class="hint">🧠 Everyday English</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. How long did it take before Jack had tomatoes?</div><div class="opt"><span class="c">a</span>about two weeks</div><div class="opt"><span class="c">b</span>about two months</div><div class="opt"><span class="c">c</span>about a year</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">7. Who wrote about "social comparison" in 1954?</div><div class="opt"><span class="c">a</span>Leon Festinger</div><div class="opt"><span class="c">b</span>Thomas Gilovich</div><div class="opt"><span class="c">c</span>Melissa Hunt</div><div class="hint">🎧 ⏱ 1:41</div></div>
    <div class="mcq"><div class="qq">8. The medal study used TV footage from the Olympics in…</div><div class="opt"><span class="c">a</span>Sydney, 2000</div><div class="opt"><span class="c">b</span>London, 2012</div><div class="opt"><span class="c">c</span>Barcelona, 1992</div><div class="hint">🎧 ⏱ 4:46</div></div>
    <div class="mcq"><div class="qq">9. In Hunt's study, students limited three apps to…</div><div class="opt"><span class="c">a</span>ten minutes each per day</div><div class="opt"><span class="c">b</span>one hour each per day</div><div class="opt"><span class="c">c</span>ten minutes per week</div><div class="hint">🎧 ⏱ 7:24</div></div>
    <div class="mcq"><div class="qq">10. Who does Jack compare himself to most often?</div><div class="opt"><span class="c">a</span>his neighbour</div><div class="opt"><span class="c">b</span>his older brother</div><div class="opt"><span class="c">c</span>other podcasters</div><div class="hint">🎧 ⏱ 9:34</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🍅</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> Jack was so proud of his tomatoes that he showed them to his mum – and to the man at the corner shop!</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">4</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>Jack watered his tomato plant every morning before work.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>Festinger said we usually compare ourselves with people who are very different from us.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 1:41</td></tr>
      <tr><td class="n">3</td><td>The students knew which medal each athlete had won.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 4:46</td></tr>
      <tr><td class="n">4</td><td>Silver medal winners often compare themselves with the gold medal winner.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 4:46</td></tr>
      <tr><td class="n">5</td><td>In Hunt's study, the students were put into two groups randomly.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 7:24</td></tr>
      <tr><td class="n">6</td><td>The researchers knew exactly why using less social media helped.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 7:24</td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">5</span>Three comparison studies 🔍 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Which study is each sentence about? Write <b>A</b>, <b>B</b> or <b>C</b>. ⏱ 1:41 · 4:46 · 7:24</p>
      </div>
      <img class="char" src="img/f/46-lucy-magnifying-glass-w.jpg" style="width:16mm;flex:none;margin-top:-4mm">
    </div>
    <div class="studies" style="margin-top:2mm">
      <div style="background:var(--peach-l)"><b class="h" style="color:var(--peach-d)">A · Social comparison 📏</b>1954 · Leon Festinger, American psychologist</div>
      <div style="background:var(--lav)"><b class="h" style="color:var(--mauve-d)">B · Silver vs bronze 🥈🥉</b>1995 · Medvec, Madey &amp; Gilovich, Cornell</div>
      <div style="background:var(--sage)"><b class="h" style="color:var(--sage-d)">C · Less social media 📱</b>2018 · Melissa Hunt and colleagues, Univ. of Pennsylvania</div>
    </div>
    <table class="tf" style="margin-top:1.6mm">
      <tr><td class="n">1</td><td>Students rated athletes' faces from agony to ecstasy.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">2</td><td>People have a natural need to know how they're doing.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">3</td><td>143 university students took part for three weeks.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">4</td><td>The biggest improvements were in the students who felt worst at the start.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">5</td><td>Third place looked happier than second place.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">6</td><td>We usually compare ourselves with people who are similar to us.</td><td class="ck"><span class="box"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">6</span>Looking up or looking down? <span class="tag">new! upward or downward</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Is each thought an <b>upward</b> comparison (with someone better off) or a <b>downward</b> one (with someone worse off)? ⏱ 1:41 · 4:46</p>
      </div>
      <img class="char" src="img/f/74-jack-certificate-w.jpg" style="width:14mm;flex:none;margin-top:-4mm">
    </div>
    <div class="podwrap">
    <div class="podium">
      <div><div class="th"><b>🥈 silver</b>"So close to gold…" 😞</div><div class="st" style="background:#E3E6EC;height:14mm">2</div></div>
      <div><div class="th"><b>🥇 gold</b>"I'm the champion!" 🤩</div><div class="st" style="background:#FBE7B5;height:20mm">1</div></div>
      <div><div class="th"><b>🥉 bronze</b>"I'm on the podium!" 😄</div><div class="st" style="background:#F6D2BA;height:9mm">3</div></div>
    </div>
    <div>
{UDS}    </div>
    </div>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>"I just don't measure up!" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">A niece is learning English, and she feels a bit down after watching videos online. Listen at ⏱ 12:20 and write <b>one word</b> in each gap (1–10). The breakdown at ⏱ 13:30 can help.</p>
    </div>
    <img class="char" src="img/f/67-duo-chatting-w.jpg" style="width:24mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat wide" style="margin-top:2mm;gap:.4mm">
{CHAT}
  </div>

  <div class="sec" style="margin-top:2.6mm">
    <h2><span class="num">8</span>Phrases to steal <span class="tag">expressions</span><span class="tag pts">4 points</span></h2>
    <p class="instr">Match each phrase from the chat (1–4) to its meaning (a–d). ⏱ 13:30</p>
    <div class="grid2" style="gap:4mm;align-items:start">
      <table class="match" style="font-size:9.2pt">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> "Hang on."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> "I bet…"</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> "Don't remind me!"</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> "When you put it like that…"</td></tr>
      </table>
      <div class="card" style="font-size:8.9pt;line-height:1.62">
        <b>a)</b> I'm almost sure…<br>
        <b>b)</b> When you explain it in that way…<br>
        <b>c)</b> Wait a moment.<br>
        <b>d)</b> That's embarrassing – I'd prefer to forget it!
      </div>
    </div>
  </div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">9</span>Comparison idioms <span class="tag">idioms</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">Complete each sentence with a word from the box. ⏱ 14:43 · 17:06</p>
    </div>
    <img class="char" src="img/f/47-jack-pointing-right-w.jpg" style="width:17mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chips" style="margin:1.6mm 0 2mm 10.8mm"><span>apples</span><span>envy</span><span>greener</span><span>Joneses</span><span>show-off</span><span>thief</span></div>
  <table class="coll" style="margin-left:2mm">
    <tr><td>1. 🌱 Other people's lives always look better. The grass is always <span class="blank s"></span>.</td></tr>
    <tr><td>2. 🚗 They bought a new car just to keep up with the <span class="blank s"></span>.</td></tr>
    <tr><td>3. 🍎 A small village café and a famous restaurant? That's comparing <span class="blank s"></span> and oranges.</td></tr>
    <tr><td>4. 😢 Comparing yourself all the time steals your happiness. Comparison is the <span class="blank s"></span> of joy.</td></tr>
    <tr><td>5. 💚 When she saw my new bike, she was green with <span class="blank s"></span>.</td></tr>
    <tr><td>6. 💰 He always talks about his money and his car. He's such a <span class="blank s"></span>.</td></tr>
  </table>
  <div class="bub" style="margin-top:2.2mm">
    <img class="char" src="img/f/02-jack-lightbulb-idea-w.jpg" style="width:17mm;flex:none">
    <div class="txt"><b>Jack's tip:</b> <b>Envious</b> = you want what someone else has. <b>Jealous</b> can mean the same in everyday English (<i>"I'm so jealous of your holiday!"</i>) – but it can also mean afraid of losing someone you love to another person. 💚</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">10</span>Compare it right! <span class="tag">new! comparatives</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Write the correct form of the word in brackets. ⏱ 18:07</p>
      </div>
      <img class="char" src="img/f/48-lucy-holding-blank-card-w.jpg" style="width:15mm;flex:none;margin-top:-4mm">
    </div>
    <div class="edrule">
      <div style="background:#DCEFF3"><b style="color:#1F5F70">📏 short words + -er:</b> tall → taller · big → bigger<br><b style="color:#1F5F70">good → better</b> (never "more better"!)</div>
      <div style="background:#FDE3D3"><b style="color:#B9542B">📐 long words: more + word:</b> more confident<br><b style="color:#B9542B">⚖️ not as + word + as:</b> not as fast as</div>
    </div>
    <table class="coll" style="margin-left:2mm">
      <tr><td>1. 🍅 Five tomatoes? That's much <span class="blank"></span> than none! <b style="color:var(--mauve)">(good)</b></td></tr>
      <tr><td>2. 🧺 My neighbour's basket was <span class="blank"></span> than mine. <b style="color:var(--mauve)">(big)</b></td></tr>
      <tr><td>3. 🗣️ She's <span class="blank" style="min-width:34mm"></span> than she was last year. <b style="color:var(--mauve)">(confident)</b></td></tr>
      <tr><td>4. 🏃 I'm not <span class="blank" style="min-width:30mm"></span> my brother. <b style="color:var(--mauve)">(as / fast)</b></td></tr>
      <tr><td>5. 🌍 My English isn't <span class="blank" style="min-width:30mm"></span> hers – yet! <b style="color:var(--mauve)">(as / fluent)</b></td></tr>
      <tr><td>6. 📅 <span class="blank"></span> with last year, my English is much better. <b style="color:var(--mauve)">(compare)</b></td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="card peach" style="padding:2.6mm 4mm">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:3mm">
        <div><b style="color:var(--night);font-size:9.8pt">🥈 ➜ 🥉 Think like a bronze medal winner!</b> <span class="small">(no points)</span><br><span class="small">Lucy's third tip: don't only think "I'm not as good as them" – think about how far you've come and what you already have. Turn each silver thought into a bronze thought. ⏱ 10:03</span></div>
      </div>
      <table class="friend" style="margin-top:1.6mm;background:#fff;border-radius:3mm">
        <tr><td class="i" style="color:var(--night);width:47%">🥈 "I only grew five tomatoes."</td><td>🥉 <i>"I grew five tomatoes in my very first year – on a balcony!"</i></td></tr>
        <tr><td class="i" style="color:var(--night)">🥈 "I still make mistakes when I speak."</td><td style="white-space:nowrap">🥉 <span class="blank" style="min-width:70mm"></span></td></tr>
        <tr><td class="i" style="color:var(--night)">🥈 "My friend runs faster than me."</td><td style="white-space:nowrap">🥉 <span class="blank" style="min-width:70mm"></span></td></tr>
        <tr><td class="i" style="color:var(--night)">🥈 "I can't understand every word of this episode."</td><td style="white-space:nowrap">🥉 <span class="blank" style="min-width:70mm"></span></td></tr>
      </table>
    </div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">11</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 18:07</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "He is more better than me."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "I am not good like her."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "Compare with him, I am bad at football."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "I made a lot of progresses this year."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "My English is very bad."</td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/07-lucy-great-job-w.jpg" style="width:18mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> <b>"Yet"</b> is a very powerful word for learners: <i>"My English isn't as fluent as hers – <b>yet</b>."</i> And <b>progress</b> is uncountable: <i>some progress, a lot of progress, great progress</i> – never "a progress". ✨</div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">🔁</span>Then and now <span class="tag fun">compare with your past self · no points</span></h2>
        <p class="instr" style="margin-bottom:0">Jack's first tip: don't ask "Am I as good as her?" – ask "Am I better than I was six months ago?" Write three things. ⏱ 10:03</p>
      </div>
      <img class="char" src="img/f/04-jack-thinking-w.jpg" style="width:14mm;flex:none;margin-top:-3mm">
    </div>
    <table class="friend" style="margin-top:1.4mm">
      <tr><td class="i" style="color:var(--night);width:48%">⏮️ A year ago, I couldn't <i>understand a podcast in English.</i></td><td>⏭️ Now I can <i>understand most of this episode!</i></td></tr>
      <tr><td class="i" style="color:var(--night)">⏮️ A year ago, I couldn't <span class="blank" style="min-width:38mm"></span></td><td>⏭️ Now I can <span class="blank" style="min-width:58mm"></span></td></tr>
      <tr><td class="i" style="color:var(--night)">⏮️ A year ago, I couldn't <span class="blank" style="min-width:38mm"></span></td><td>⏭️ Now I can <span class="blank" style="min-width:58mm"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="card teal" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.6pt">💚 Turn envy into information</b> <span class="small">(no points) Jack's second tip: when you feel envious, ask "What exactly do I want?" Then the feeling becomes a signal, not a punishment. ⏱ 10:03</span>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2mm;margin-top:1.8mm;font-size:8.6pt">
        <div style="background:#fff;border-radius:3mm;padding:1.8mm 2.4mm"><b style="color:var(--night)">😒 I'm envious of…</b><br><i>my friend's fitness</i><div class="lines" style="height:6mm"></div></div>
        <div style="background:#fff;border-radius:3mm;padding:1.8mm 2.4mm"><b style="color:var(--night)">🤔 What I really want is…</b><br><i>to be more active</i><div class="lines" style="height:6mm"></div></div>
        <div style="background:#fff;border-radius:3mm;padding:1.8mm 2.4mm"><b style="color:var(--night)">👣 One small step:</b><br><i>a 15-minute walk every day</i><div class="lines" style="height:6mm"></div></div>
      </div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">🎉</span>Be happy for them! <span class="tag fun">Jack's third tip · no points</span></h2>
        <p class="instr" style="margin-bottom:0">When a friend does well, say "Congratulations, you deserve it!" – and mean it. Their success doesn't take anything away from you. Write a kind reply to each message. ⏱ 10:03</p>
      </div>
      <img class="char" src="img/f/29-duo-high-five-w.jpg" style="width:26mm;flex:none;margin-top:-3mm">
    </div>
    <div class="chips" style="margin:1.6mm 0 1.4mm 10.8mm;gap:1.4mm"><span>Congratulations – you deserve it!</span><span>That's brilliant news!</span><span>I'm so happy for you!</span><span>Well done – you worked so hard for it!</span></div>
    <table class="friend">
      <tr><td class="i" style="color:var(--night);width:47%">📩 "I passed my driving test!"</td><td style="white-space:nowrap">💬 <i>"Congratulations – you deserve it!"</i></td></tr>
      <tr><td class="i" style="color:var(--night)">📩 "I got the job!"</td><td style="white-space:nowrap">💬 <span class="blank" style="min-width:76mm"></span></td></tr>
      <tr><td class="i" style="color:var(--night)">📩 "I finished my first 10 km race!"</td><td style="white-space:nowrap">💬 <span class="blank" style="min-width:76mm"></span></td></tr>
      <tr><td class="i" style="color:var(--night)">📩 "My teacher says my English is much better now!"</td><td style="white-space:nowrap">💬 <span class="blank" style="min-width:76mm"></span></td></tr>
    </table>
  </div>
  {foot(7)}
</section>

<!-- ================= PAGE 8 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">12</span>Garden &amp; medals crossword 🧩 <span class="tag">puzzle</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Read the clues and write the words in the grid (1 point each). The number in brackets is the number of letters. Letters that cross help you!</p>
    </div>
    <img class="char" src="img/f/50-lucy-puzzle-piece-w.jpg" style="width:19mm;flex:none;margin-top:-3mm">
  </div>
  <div style="margin-top:2.6mm">{X.grid_html(cw, 7.5)}</div>
  <div class="grid2 cclues" style="margin-top:2.6mm;gap:4mm">
    <div class="card white" style="padding:2.4mm 3.4mm"><h4>➡️ Across</h4>{ACROSS}</div>
    <div class="card white" style="padding:2.4mm 3.4mm"><h4>⬇️ Down</h4>{DOWN}</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">13</span>Jack's tomatoes 🍅 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 0:05 and ⏱ 20:39. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/65-jack-hiking-w.jpg" style="width:15mm;flex:none;margin-top:-3mm">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">✍️</span><span>The neighbour showed Jack where he writes down all his mistakes.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🍅</span><span>Jack's plant finally gave him five small, red, perfect ones – he was so proud.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🌱</span><span>He gave Jack something to plant – and Jack plans to grow eight next year.</span></div>
      <div class="ev"><span class="box"></span><span class="e">📱</span><span>That evening, he saw his neighbour's amazing garden photo.</span></div>
      <div class="ev"><span class="box"></span><span class="e">0️⃣</span><span>"In my first year, I grew none – not a single one!"</span></div>
      <div class="ev"><span class="box"></span><span class="e">🗑️</span><span>Taking his rubbish downstairs, Jack met the neighbour in the garden.</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> Why wasn't Jack's comparison fair? Use <b>apples and oranges</b> or <b>highlight reel</b>.<div class="lines"></div><div class="lines"></div></div>
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
      <b style="color:var(--night);font-size:9.2pt">A. Who I compare myself to 🤔</b>
      <div class="small" style="margin-top:1mm">Who is it, and how does it make you feel? <i>e.g. "I sometimes compare myself to my cousin, because she's more confident than me."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. My progress 🌱</b>
      <div class="small" style="margin-top:1mm">Compare your English today with a year ago. <i>e.g. "Compared with last year, I'm much more confident. I'm not as fluent as I want to be – yet!"</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">⏱</span>My past-self week <span class="tag fun">your 7-day mission</span></h2>
        <p class="instr" style="margin-bottom:0">One small step every day. The only person you need to be better than is the person you were yesterday!</p>
      </div>
      <img class="char" src="img/f/35-jack-reading-card-w.jpg" style="width:15mm;flex:none">
    </div>
    <table class="log week" style="margin-top:2mm">
      <tr><th>Day</th><th>Small step</th><th>What I noticed</th><th>Done?</th></tr>
      <tr><td class="d">1</td><td class="a">📩 find an old English message</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">2</td><td class="a">🎙️ record one minute in English</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">3</td><td class="a">📝 rewrite the old message</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">4</td><td class="a">🔕 mute one account</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">5</td><td class="a">🎉 congratulate a friend</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">6</td><td class="a">🥉 three things I already have</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">7</td><td class="a">🔁 listen to Day 2 again</td><td></td><td class="c"><span class="box sm"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:var(--peach-d)">📏 COMPARE</b>Compared to last year…<br>I'm not as … as … yet.<br>He's better than me.</div>
        <div><b style="color:var(--mauve-d)">💚 FEELINGS</b>I'm a bit envious.<br>I don't measure up.<br>green with envy</div>
        <div><b style="color:var(--sage-d)">🌱 PERSPECTIVE</b>The grass is always greener.<br>apples and oranges<br>just a highlight reel</div>
        <div><b style="color:#C0392B">🎉 BE KIND</b>Congratulations – you deserve it!<br>I've made a lot of progress.<br>I'm still learning.</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain upward and downward comparison.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>explain why bronze winners can feel happier than silver winners.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use comparatives: better, taller, more confident, not as … as.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>talk about my progress without saying "My English is very bad".</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/52-lucy-phone-comment-w.jpg" style="width:19mm;flex:none">
      <div class="txt"><b>Share it with us!</b> Find something old you made in English, compare it with today – and tell us in the comments! Have you made <b>a lot of progress</b>? Is <b>the grass always greener</b>? And if you know how to stop birds eating tomatoes, Jack needs your help! 🐦🍅</div>
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
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: b – bronze winners looked clearly happier. · Predict: <b>swimming pool</b> 🏊 isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 g · 2 d · 3 j · 4 h · 5 c · 6 a · 7 e · 8 i · 9 b · 10 f<br>Big idea: a (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 c · 2 a · 3 b · 4 b · 5 a · 6 b · 7 a · 8 c · 9 a · 10 b</p></div>
    <div class="k"><h3>4 · True or false?</h3><p>1 T · 2 F (people who are similar to us) · 3 F (they didn't know) · 4 T · 5 T · 6 F (they couldn't say exactly why)</p></div>
    <div class="k"><h3>5 · Three studies · 6 · Up or down?</h3><p>5: 1 B · 2 A · 3 C · 4 C · 5 B · 6 A<br>6: {UD_KEY}</p></div>
    <div class="k"><h3>7 · "I just don't measure up!"</h3><p>1 bad · 2 perfect · 3 Compared · 4 Hang · 5 bet · 6 measure · 7 year · 8 remind · 9 greener · 10 path</p></div>
    <div class="k"><h3>8 · Phrases to steal</h3><p>1 c · 2 a · 3 d · 4 b</p></div>
   </div>
   <div>
    <div class="k"><h3>9 · Idioms · 10 · Compare it right!</h3><p>9: 1 greener · 2 Joneses · 3 apples · 4 thief · 5 envy · 6 show-off<br>10: 1 better · 2 bigger · 3 more confident · 4 as fast as · 5 as fluent as · 6 Compared</p></div>
    <div class="k"><h3>11 · Say it better (2 points each)</h3><p>1 He's better than me. / He's better than I am. · 2 I'm not as good as her. · 3 Compared with him, I'm not very good at football. / He's much better at football than me. · 4 I've made a lot of progress this year. · 5 I'm still learning. / My English is getting better every day.</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Crossword</h3><p>{{CW_KEY}}</p></div>{{CW_GRID}}</div>
    <div class="k"><h3>13 · Jack's tomatoes · 14 · Your turn</h3><p>1 🍅 five tomatoes · 2 📱 the basket photo · 3 🗑️ met the neighbour · 4 0️⃣ "I grew none" · 5 ✍️ the notebook · 6 🌱 seeds – eight next year<br><i>Think about it, e.g.:</i> he compared his first year with his neighbour's twelfth – apples and oranges. The basket was the neighbour's highlight reel.<br>14: your own answers – 2 points per good sentence.</p></div>
    <div class="k"><h3>Your score</h3><p>90–100 🏆 <b>Gold medal!</b> · 70–89 🥉 <b>On the podium!</b> · 50–69 🍅 <b>Five perfect tomatoes</b> · 0–49 🌱 <b>Keep growing – try again!</b></p></div>
   </div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy. And remember: the only person you really need to be better than is the person you were yesterday. Be proud of your five tomatoes! 🍅💜<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
    <img class="char" src="img/f/69-duo-thumbs-up-night.jpg" style="width:40mm">
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
    "{CW_GRID}", X.grid_html(cw, 2.7, solved=True, cls="cw cwk"))
html = head + EXTRA + "</style>\n</head>\n<body>\n" + body
(HERE / "template.html").write_text(html)
pts = [int(x) for x in re.findall(r'tag pts">(\d+) points', html)]
print("points", sum(pts), pts)
