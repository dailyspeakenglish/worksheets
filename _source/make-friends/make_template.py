"""Writes template.html for the make-friends worksheet (Podcast 65).
CSS design system copied from reading-books (which includes all earlier worksheets).
Crossword from cw.json (built by _source/tools/crossword.py). Timestamps: video time = NoteGPT time + 5 s."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import crossword as X

src = (HERE.parent / "reading-books" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Reading Books Worksheet", "Make Friends Worksheet")
cw = json.loads((HERE / "cw.json").read_text())
X.check(cw)
spec = json.loads((HERE / "cw_spec.json").read_text())
CLUES = {w.upper(): c for w, c in spec["words"]}
ACROSS, DOWN = X.clues_html(cw, CLUES)

EXTRA = """
/* ---- new in make-friends ---- */
.ladder{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm;align-items:end}
.ladder div{border-radius:3mm 3mm 0 0;padding:1.8mm 2mm;text-align:center;font-size:8.4pt;line-height:1.35;color:var(--night)}
.ladder div b{display:block;font-size:9.2pt}
.ladder div .e{display:block;font-size:14pt;line-height:1.2}
.sorter3{display:grid;grid-template-columns:1fr auto;gap:1.2mm 3mm;align-items:center;font-size:9pt}
.sorter3 .ph{padding:1.1mm 0;border-bottom:1px dashed var(--line)}
.key3{display:flex;gap:2mm;margin:1.6mm 0 2mm}
.key3 span{border-radius:2.4mm;padding:1mm 2.6mm;font-size:8.4pt;font-weight:700}
.inv{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm;margin-top:1.6mm}
.inv div{border-radius:3mm;padding:1.6mm 2.4mm;font-size:8.4pt;text-align:center}
.inv div b{display:block;font-size:12pt}
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
 ("LUCY", "09-lucy-talking-right", f"Morning, Jack. Good {gap(1)}?"),
 ("JACK", "13-jack-talking-left", f"Yeah, not bad, thanks. Actually, I wanted to ask you something. A few of us from the office go for a walk along the {gap(2)} every Saturday morning, with our families. Then we usually have breakfast together. Do you {gap(3)} joining us this week?"),
 ("LUCY", "40-lucy-excited-right", f"Oh, that sounds lovely. I'd {gap(4)} to. What time do you usually meet?"),
 ("JACK", "43-jack-explaining-left", "About nine, by the old bridge. It's very relaxed. Just walking and chatting."),
 ("LUCY", "38-lucy-explaining-right", f"{gap(5)} me in. I've been {gap(6)} to explore that part of town since I moved here."),
 ("JACK", "45-jack-agreeing-left", f"Great. Let's {gap(7)} numbers, and I'll send you the details."),
 ("LUCY", "36-lucy-surprised-right", "Perfect. To be honest, I was worried you'd think I was a bit boring. I've been so quiet since I started."),
 ("JACK", "16-jack-surprised-left", f"Not at all! Everyone in the team likes you. We just didn't want to {gap(8)} you."),
 ("LUCY", "12-lucy-laughing-right", "That's funny. I thought the same about you."),
 ("JACK", "41-jack-laughing-left", "Well, now we know. See you on Saturday, then."),
 ("LUCY", "39-lucy-caring-right", "See you there. I'll bring some fresh bread from the bakery."),
])

AL = ["I love being ______ on Sunday mornings. It's so peaceful. ☕",
      "After she moved, she felt ______ for months. 🏙️",
      "Jack walked home ______ – and he enjoyed the quiet. 🌙",
      "Without his friends, he felt really ______. 😔",
      "You can be ______ in a room full of people. 🎉",
      "I sometimes have lunch ______ – it's relaxing. 🥪"]
ALS = "".join(f'      <div class="tm2" style="grid-template-columns:1fr 22mm 23mm"><span>{i}. {t}</span><span class="claim ed"><span class="box"></span>😌 alone</span><span class="claim ing"><span class="box"></span>😢 lonely</span></div>\n' for i, t in enumerate(AL, 1))

SORT = [("“Count me in!”", "A"), ("“I'd love to, but I'm working on Saturday.”", "D"), ("“How about next Friday instead?”", "S"),
        ("“Sounds great – what time?”", "A"), ("“I'm afraid I can't this week. Thanks for asking!”", "D"), ("“What about a coffee on Sunday?”", "S")]
SORTS = "".join(f'      <div class="ph"><b style="color:var(--night)">{i}.</b> {t}</div><span class="box"></span>\n' for i, (t, _) in enumerate(SORT, 1))
SORT_KEY = " · ".join(f"{i} {k}" for i, (_, k) in enumerate(SORT, 1))

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
      <h1>How to Make Friends as an Adult</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">How many hours it takes to turn a stranger into a friend, why people probably like you more than you think, natural English for inviting people and keeping in touch – and "the waving man".</p>
      <div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div class="hero2">
      <div style="position:absolute;z-index:2;top:3.4mm;left:3.4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">"Nice to meet you anyway!" 👋</div>
      <img class="char" src="img/f/30-duo-waving-lav.jpg" style="position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:66mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · After you listen 💬</div><div class="s">Solve the crossword, write a specific invitation – and send that message to an old friend!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: My friendship check <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Be honest! Tick everything that is true for you. 😊</p>
    <div style="display:grid;grid-template-columns:1.42fr .58fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:1.8mm;justify-content:center;padding:2.6mm 3.6mm">
        <div class="conf" style="grid-template-columns:1fr 1fr;justify-content:stretch;font-size:8.7pt">
          <div><span class="box sm"></span>🏙️ I've moved to a new city</div>
          <div><span class="box sm"></span>☕ I'm a regular somewhere</div>
          <div><span class="box sm"></span>📵 I've lost touch with a friend</div>
          <div><span class="box sm"></span>⏳ I wait for others to invite me</div>
          <div><span class="box sm"></span>⚽ I go to a weekly class or club</div>
          <div><span class="box sm"></span>👋 I've waved at the wrong person!</div>
        </div>
        <div style="font-size:9pt"><b style="color:var(--night)">My friendship score:</b> <span class="blank s"></span> / 6</div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> How many hours together does it take to turn an acquaintance into a casual friend?</div>
        <div style="display:flex;gap:3.4mm;font-size:8.7pt;white-space:nowrap"><span><span class="circ">a</span> about 5 hours</span><span><span class="circ">b</span> about 50 hours</span><span><span class="circ">c</span> about 500 hours</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 2:58</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:1.8mm 2.4mm;font-size:8.1pt;border:1.2px solid #F4D2C2;line-height:1.36"><b style="color:var(--night)">Jack:</b> "I waved back with my whole arm…" 🙈</div>
        <img class="char" src="img/f/08-jack-waving-peach.jpg" style="width:29mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – or write them in your notebook.</p>
    <div class="grid2" style="gap:2.4mm">
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>1.</b> How did you meet your best friend?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>2.</b> Is it harder to make friends as an adult? Why?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>3.</b> Who is a friend you'd love to hear from again?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>4.</b> Where could you meet new people in your town?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Then check at ⏱ 13:10 and ⏱ 14:08</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> an acquaintance</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> to hit it off</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> to drift apart</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> to keep in touch</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> to break the ice</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> to belong</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> lonely</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> a regular</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> to swap</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> the liking gap</td></tr>
      </table>
      <div class="card" style="font-size:9pt;line-height:1.55">
        <b>a)</b> to continue to contact someone – messages, calls, visits<br>
        <b>b)</b> someone who goes to the same café or shop again and again<br>
        <b>c)</b> someone you know a little, but not well<br>
        <b>d)</b> to exchange: give one thing and get another<br>
        <b>e)</b> to slowly become less close, usually without an argument<br>
        <b>f)</b> sad because you don't have friends or people around you<br>
        <b>g)</b> to like each other and get on well very quickly<br>
        <b>h)</b> people like us more than we think they do<br>
        <b>i)</b> to feel happy and comfortable in a place or group<br>
        <b>j)</b> to make people feel relaxed at the start of a meeting
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/03-lucy-did-you-know-w.jpg" style="width:20mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> ac-<b style="color:var(--peach-d)">QUAIN</b>-tance (/əˈkweɪntəns/ – stress in the middle!) · be-<b style="color:var(--peach-d)">LONG</b> · <b style="color:var(--peach-d)">LONE</b>-ly · <b style="color:var(--peach-d)">REG</b>-u-lar · <span style="white-space:nowrap">friend (/frend/ – the <b>i</b> is silent!)</span>. Say it: <i>"We hit it off straight away!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>Adults can't really make new friends – real friendships only start at school.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>Friendship takes time and a little courage – people probably like you more than you think, so be the one who asks.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>One great conversation is all you need to become best friends.</div>
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
      <div class="chips predict-chips" style="margin-top:2mm;justify-content:center;gap:1.4mm"><span>crayons</span><span>football boots</span><span>food bank</span><span>bridge</span><span>soup</span><span>emoji</span><span>cinema</span><span>bakery</span></div>
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
    <div class="mcq"><div class="qq">1. "Last year, I made ______ with my neighbour."</div><div class="opt"><span class="c">a</span>a friendship</div><div class="opt"><span class="c">b</span>friends</div><div class="opt"><span class="c">c</span>friend</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">2. "I don't have any friends here. I feel a bit ______."</div><div class="opt"><span class="c">a</span>alone</div><div class="opt"><span class="c">b</span>only</div><div class="opt"><span class="c">c</span>lonely</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">3. "Do you ______ a cup of tea?" (= would you like)</div><div class="opt"><span class="c">a</span>fancy</div><div class="opt"><span class="c">b</span>like to</div><div class="opt"><span class="c">c</span>want of</div><div class="hint">🧠 Everyday British English</div></div>
    <div class="mcq"><div class="qq">4. "We ______ touch when she moved abroad."</div><div class="opt"><span class="c">a</span>broke</div><div class="opt"><span class="c">b</span>lost</div><div class="opt"><span class="c">c</span>missed</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">5. "Count me in!" means…</div><div class="opt"><span class="c">a</span>Count my money.</div><div class="opt"><span class="c">b</span>I don't want to come.</div><div class="opt"><span class="c">c</span>Include me – I want to come!</div><div class="hint">🧠 Everyday English</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. Who was the man on the other side of the road waving at?</div><div class="opt"><span class="c">a</span>Jack</div><div class="opt"><span class="c">b</span>a bus driver</div><div class="opt"><span class="c">c</span>his friend, behind Jack</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">7. In Hall's first study, people had moved to a new place in the last…</div><div class="opt"><span class="c">a</span>six months</div><div class="opt"><span class="c">b</span>six weeks</div><div class="opt"><span class="c">c</span>six years</div><div class="hint">🎧 ⏱ 2:58</div></div>
    <div class="mcq"><div class="qq">8. In the liking gap study, strangers first talked for…</div><div class="opt"><span class="c">a</span>an hour</div><div class="opt"><span class="c">b</span>five minutes</div><div class="opt"><span class="c">c</span>a whole day</div><div class="hint">🎧 ⏱ 5:18</div></div>
    <div class="mcq"><div class="qq">9. How many studies did Holt-Lunstad's team look at?</div><div class="opt"><span class="c">a</span>48</div><div class="opt"><span class="c">b</span>148</div><div class="opt"><span class="c">c</span>1,048</div><div class="hint">🎧 ⏱ 7:45</div></div>
    <div class="mcq"><div class="qq">10. What did Tom shout when he saw Jack at football?</div><div class="opt"><span class="c">a</span>"It's the waving man!"</div><div class="opt"><span class="c">b</span>"Welcome to the team!"</div><div class="opt"><span class="c">c</span>"Nice to see you again!"</div><div class="hint">🎧 ⏱ 20:05</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">👋</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> Every year, on the day they met, Tom sends Jack the same message: just a waving hand emoji!</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">4</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>Jack started crossing the road, still waving and smiling.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>Tom was angry when he met Jack in the middle of the road.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">3</td><td>Time spent working together counted as much as time spent having fun.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:58</td></tr>
      <tr><td class="n">4</td><td>Most people thought their partner liked them <i>more</i> than they really did.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:18</td></tr>
      <tr><td class="n">5</td><td>Shyer people tended to have a bigger liking gap.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:18</td></tr>
      <tr><td class="n">6</td><td>The 2010 review proves that friends make you live longer.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 7:45</td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">5</span>Three friendship studies 🔍 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Which study is each sentence about? Write <b>A</b>, <b>B</b> or <b>C</b>. ⏱ 2:58 · 5:18 · 7:45</p>
      </div>
      <img class="char" src="img/f/19-lucy-glasses-book-w.jpg" style="width:16mm;flex:none;margin-top:-4mm">
    </div>
    <div class="studies" style="margin-top:2mm">
      <div style="background:var(--peach-l)"><b class="h" style="color:var(--peach-d)">A · Hours to a friend ⏱️</b>2018 · Jeffrey Hall, University of Kansas</div>
      <div style="background:var(--lav)"><b class="h" style="color:var(--mauve-d)">B · The liking gap 💭</b>2018 · Erica Boothby, Gus Cooney and team</div>
      <div style="background:var(--sage)"><b class="h" style="color:var(--sage-d)">C · Friends and health ❤️</b>2010 · Julianne Holt-Lunstad, Brigham Young Univ.</div>
    </div>
    <table class="tf" style="margin-top:1.6mm">
      <tr><td class="n">1</td><td>It looked at 148 studies with more than 300,000 people.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">2</td><td>More than 350 adults who had just moved were trying to make new friends.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">3</td><td>Strangers had a short conversation and then answered two questions.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">4</td><td>It took more than 200 hours to become close friends.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">5</td><td>Students sharing accommodation kept underestimating for months.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">6</td><td>Stronger relationships were linked to about a 50% higher chance of surviving.</td><td class="ck"><span class="box"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">6</span>The friendship ladder <span class="tag">new! hours and maths</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0"><b>A.</b> Listen at ⏱ 2:58 and write the hours on each step (1 point each). <b>B.</b> Do the maths (1 point each).</p>
      </div>
      <img class="char" src="img/f/51-jack-stopwatch-w.jpg" style="width:15mm;flex:none;margin-top:-4mm">
    </div>
    <div class="ladder" style="margin-top:2mm">
      <div style="background:#EEE9F6;height:19mm"><span class="e">🙂</span><b>acquaintance</b>you know them a little</div>
      <div style="background:#DCEFF3;height:24mm"><span class="e">😊</span><b>casual friend</b>about <span class="blank s" style="min-width:10mm"></span> hours</div>
      <div style="background:#FDE3D3;height:29mm"><span class="e">😄</span><b>friend</b>around <span class="blank s" style="min-width:10mm"></span> hours</div>
      <div style="background:#DDF1E3;height:34mm"><span class="e">🤗</span><b>close friend</b>more than <span class="blank s" style="min-width:10mm"></span> hours</div>
    </div>
    <div class="card white" style="margin-top:0;border-radius:0 0 3mm 3mm;padding:2mm 4mm;font-size:9pt;line-height:1.9">
      🗓️ You see someone for <b>two hours every weekend</b>. How many weeks until you reach…<br>
      4. 50 hours? <span class="blank s"></span> weeks &nbsp;·&nbsp; 5. 90 hours? <span class="blank s"></span> weeks &nbsp;·&nbsp; 6. 200 hours? <span class="blank s"></span> weeks (about two years!)
    </div>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>"Do you fancy joining us?" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Two colleagues have been chatting at work for a few weeks. Finally, Jack invites Lucy to something. Listen at ⏱ 12:01 and write <b>one word</b> in each gap (1–8). Then answer A and B. The breakdown at ⏱ 13:10 can help.</p>
    </div>
    <img class="char" src="img/f/32-lucy-coffee-chat-right-w.jpg" style="width:18mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat wide" style="margin-top:2mm;gap:.4mm">
{CHAT}
  </div>
  <div class="grid2" style="margin-top:2.4mm;gap:3mm">
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">A.</b> They meet at nine, by the old <span class="blank" style="min-width:24mm"></span>.</div>
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">B.</b> Lucy will bring fresh <span class="blank" style="min-width:24mm"></span>.</div>
  </div>

  <div class="sec" style="margin-top:3.6mm">
    <h2><span class="num">8</span>Phrases to steal <span class="tag">expressions</span><span class="tag pts">4 points</span></h2>
    <p class="instr">Match each phrase from the chat (1–4) to its meaning (a–d). ⏱ 13:10</p>
    <div class="grid2" style="gap:4mm;align-items:start">
      <table class="match" style="font-size:9.2pt">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> "Good weekend?"</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> "I'd love to."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> "I've been meaning to…"</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> "Let's swap numbers."</td></tr>
      </table>
      <div class="card" style="font-size:8.9pt;line-height:1.62">
        <b>a)</b> I've wanted to do it for a while, but I haven't yet.<br>
        <b>b)</b> Let's give each other our phone numbers.<br>
        <b>c)</b> Did you have a good weekend?<br>
        <b>d)</b> Yes, please! (a warm way to accept)
      </div>
    </div>
  </div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">9</span>Friendship idioms <span class="tag">idioms</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">Complete each sentence with a word from the box. ⏱ 14:08</p>
    </div>
    <img class="char" src="img/f/47-jack-pointing-right-w.jpg" style="width:17mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chips" style="margin:1.6mm 0 2mm 10.8mm"><span>fair-weather</span><span>ice</span><span>indeed</span><span>off</span><span>pod</span><span>way</span></div>
  <table class="coll" style="margin-left:2mm">
    <tr><td>1. 🍲 Tom brought soup when Jack was ill. A friend in need is a friend <span class="blank s"></span>!</td></tr>
    <tr><td>2. ☀️ She only calls when life is fun. She's a <span class="blank s"></span> friend.</td></tr>
    <tr><td>3. 👧 Sarah and I met when we were six. We go back a long <span class="blank s"></span>.</td></tr>
    <tr><td>4. 🫛 They even laugh the same way – they're like two peas in a <span class="blank s"></span>.</td></tr>
    <tr><td>5. 😂 He told a funny story to break the <span class="blank s"></span>.</td></tr>
    <tr><td>6. 🗣️ We hit it <span class="blank s"></span> straight away – we talked for three hours!</td></tr>
  </table>
  <div class="bub" style="margin-top:2.2mm">
    <img class="char" src="img/f/02-jack-lightbulb-idea-w.jpg" style="width:17mm;flex:none">
    <div class="txt"><b>Jack's tip:</b> <b>"Hit it off"</b> doesn't mean hitting anyone – don't worry! 😄 And a boat <b>drifts</b> when it moves slowly with the water, with nobody steering it – that's how friends <b>drift apart</b>. 🛶</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">10</span>Yes, no or another time? <span class="tag">new! replying to invitations</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Someone invites you to something. Is each reply <b>A</b> (accept), <b>D</b> (decline politely) or <b>S</b> (suggest another time)?</p>
      </div>
      <img class="char" src="img/f/48-lucy-holding-blank-card-w.jpg" style="width:15mm;flex:none;margin-top:-4mm">
    </div>
    <div class="key3"><span style="background:#DDF1E3;color:#1E7B45">✅ A = accept</span><span style="background:#FBE1DE;color:#C0392B">🙏 D = decline politely</span><span style="background:#DCEFF3;color:#1F5F70">📅 S = suggest another time</span></div>
    <div class="card white sorter3" style="padding:1.6mm 4mm 2mm">
{SORTS}    </div>
    <div class="bub" style="margin-top:2.2mm">
      <img class="char" src="img/f/01-lucy-thumbs-up-w.jpg" style="width:16mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> A polite "no" = <b>show interest</b> + <b>but</b> + <b>a reason</b>: <i>"Oh, I'd love to, but I'm visiting my mum."</i> Add another time and the door stays open: <i>"How about next week?"</i> 🚪</div>
    </div>
  </div>
  <div class="sec">
    <div class="card sage" style="padding:2.4mm 4mm">
      <b style="color:var(--night);font-size:9.6pt">📅 Invite like a pro!</b> <span class="small">(no points) "We should meet up sometime" = never. A good invitation has three parts. ⏱ 9:30</span>
      <div class="inv">
        <div style="background:#fff"><b>🚶</b><b style="font-size:8.6pt;color:var(--night)">WHAT</b>a walk, a coffee, a class…</div>
        <div style="background:#fff"><b>🗓️</b><b style="font-size:8.6pt;color:var(--night)">WHEN</b>Saturday morning, after work…</div>
        <div style="background:#fff"><b>📍</b><b style="font-size:8.6pt;color:var(--night)">WHERE</b>the park, the old bridge…</div>
      </div>
      <div style="font-size:9pt;margin-top:1.8mm">"I'm going to <span class="blank" style="min-width:34mm"></span> on <span class="blank" style="min-width:28mm"></span> at <span class="blank" style="min-width:28mm"></span>. Would you like to come?"</div>
    </div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">11</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 17:19</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "I made a friendship with my neighbour."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "I am alone in this city." <span class="small">(you feel sad)</span></td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "Do you want to go out with me?" <span class="small">(to a new friend)</span></td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "Let's meet one day."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "I'm missing you, my friend."</td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/07-lucy-great-job-w.jpg" style="width:18mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> Careful! <b>"Go out with someone"</b> can sound like a date. 💘 For friends, say <i>"Do you want to hang out?"</i> And <i>"He's a close friend <b>of mine</b>"</i> sounds more natural than <i>"He is my close friend."</i></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">😌</span>Alone or lonely? <span class="tag fun">tick · no points</span></h2>
        <p class="instr" style="margin-bottom:0"><b>Alone</b> = without other people (it can be happy!). <b>Lonely</b> = sad because you don't have friends around you. ⏱ 17:19</p>
      </div>
      <img class="char" src="img/f/73-lucy-calm-w.jpg" style="width:15mm;flex:none;margin-top:-3mm">
    </div>
    <div style="margin-top:1.6mm">
{ALS}    </div>
  </div>

  <div class="sec">
    <div class="card teal" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.6pt">💭 Mind the liking gap!</b> <span class="small">(no points)</span> After a conversation, our worries are usually wrong. Rewrite each worry as a kinder, more realistic thought. ⏱ 5:18
      <div style="display:grid;grid-template-columns:auto 1fr;gap:0 3mm;align-items:end;font-size:9pt;margin-top:1.2mm">
        <span style="color:#C0392B">😟 "They probably think I'm boring."</span><span>💜 <i>"They probably liked me more than I think."</i></span>
        <span style="color:#C0392B;padding-top:2mm">😟 "I talked too much. They hated it."</span><div class="lines"></div>
        <span style="color:#C0392B;padding-top:2mm">😟 "They won't want to meet up with me."</span><div class="lines"></div>
      </div>
    </div>
  </div>
  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">🗓️</span>Where will your 50 hours come from? <span class="tag fun">plan · no points</span></h2>
        <p class="instr" style="margin-bottom:0">Jack's tip: do something regularly, with the same people – then the hours add up by themselves! Circle one idea, then complete the sentence. ⏱ 9:30</p>
      </div>
      <img class="char" src="img/f/65-jack-hiking-w.jpg" style="width:15mm;flex:none;margin-top:-3mm">
    </div>
    <div class="chips" style="margin-top:1.8mm;gap:1.4mm;justify-content:center"><span>🎨 a weekly class</span><span>⚽ a sports team</span><span>🚶 a walking group</span><span>🥫 volunteering</span><span>📚 a book club</span><span>☕ being a regular</span></div>
    <div style="font-size:9pt;margin-top:2mm">"Every <span class="blank" style="min-width:26mm"></span>, I'm going to <span class="blank" style="min-width:70mm"></span>."</div>
  </div>
  {foot(7)}
</section>

<!-- ================= PAGE 8 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">12</span>Friendship crossword 🧩 <span class="tag">puzzle</span><span class="tag pts">10 points</span></h2>
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
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
      <div>
        <h2><span class="num">13</span>The waving man ⚽ <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 0:05 and ⏱ 20:05. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/57-jack-exercise-w.jpg" style="width:15mm;flex:none;margin-top:-3mm">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">⚽</span><span>Two weeks later, Jack joined a five-a-side football team.</span></div>
      <div class="ev"><span class="box"></span><span class="e">👋</span><span>Jack waved back at a man on the other side of the road.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🍲</span><span>When Jack was ill, Tom brought him soup and medicine.</span></div>
      <div class="ev"><span class="box"></span><span class="e">📣</span><span>Tom shouted, "It's the waving man!" – and everyone laughed.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🛣️</span><span>They met in the middle of the road: "Well, I'm Tom."</span></div>
      <div class="ev"><span class="box"></span><span class="e">🍽️</span><span>After football, they started eating together – then dinners and Sunday walks.</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> Why was "the waving man" story actually the best thing that could happen to Jack?<div class="lines"></div></div>
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
      <b style="color:var(--night);font-size:9.2pt">A. How I met my best friend 🤝</b>
      <div class="small" style="margin-top:1mm">Use <b>hit it off</b>, <b>go back a long way</b> or <b>keep in touch</b>. <i>e.g. "We met at a dance class and hit it off straight away."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. My specific invitation 📅</b>
      <div class="small" style="margin-top:1mm">"Sometime" means never! Invite someone with an activity, a day and a place. <i>e.g. "I'm going for a walk in the park on Saturday morning. Would you like to come?"</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">⏱</span>My friendship week <span class="tag fun">your 7-day mission</span></h2>
        <p class="instr" style="margin-bottom:0">One small, brave step every day. Remember: they probably like you more than you think!</p>
      </div>
      <img class="char" src="img/f/59-jack-phone-w.jpg" style="width:15mm;flex:none">
    </div>
    <table class="log week" style="margin-top:2mm">
      <tr><th>Day</th><th>Small step</th><th>What happened?</th><th>Done?</th></tr>
      <tr><td class="d">1</td><td class="a">💬 message an old friend</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">2</td><td class="a">👋 say hello to a neighbour</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">3</td><td class="a">☕ be a regular somewhere</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">4</td><td class="a">⚽ find a weekly group</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">5</td><td class="a">📅 invite someone</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">6</td><td class="a">✅ say yes to an invitation</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">7</td><td class="a">🎙️ send a voice note</td><td></td><td class="c"><span class="box sm"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:var(--peach-d)">👋 MEET</b>Nice to meet you!<br>Good weekend?<br>Let's swap numbers.</div>
        <div><b style="color:var(--mauve-d)">📅 INVITE</b>Do you fancy…?<br>Are you free on Saturday?<br>Would you like to come?</div>
        <div><b style="color:var(--sage-d)">✅ REPLY</b>I'd love to!<br>Count me in.<br>I'd love to, but…</div>
        <div><b style="color:#C0392B">💌 KEEP IN TOUCH</b>I was thinking about you.<br>Let's keep in touch!<br>I've missed you!</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain how many hours it takes to make a friend.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>explain the liking gap – and why it's good news.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>invite someone, and accept or decline politely.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use alone / lonely and "hang out" instead of "go out with".</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/52-lucy-phone-comment-w.jpg" style="width:19mm;flex:none">
      <div class="txt"><b>Share it with us!</b> Tell us in the comments how you met your best friend. Did you <b>hit it off</b> straight away? Do you <b>go back a long way</b>? And have you ever waved at someone who wasn't waving at you? 👋😅</div>
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
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: b – about 50 hours. · Predict: <b>cinema</b> 🎬 isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 c · 2 g · 3 e · 4 a · 5 j · 6 i · 7 f · 8 b · 9 d · 10 h<br>Big idea: b (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 b · 2 c · 3 a · 4 b · 5 c · 6 c · 7 a · 8 b · 9 b · 10 a</p></div>
    <div class="k"><h3>4 · True or false?</h3><p>1 T · 2 F (he laughed: "Nice to meet you anyway") · 3 F (time having fun counted more) · 4 F (they thought they were liked <i>less</i>) · 5 T · 6 F (it's a link, not proof)</p></div>
    <div class="k"><h3>5 · Three studies · 6 · The friendship ladder</h3><p>5: 1 C · 2 A · 3 B · 4 A · 5 B · 6 C<br>6: casual friend about 50 · friend around 90 · close friend more than 200 · 4 25 weeks · 5 45 weeks · 6 100 weeks</p></div>
    <div class="k"><h3>7 · "Do you fancy joining us?"</h3><p>1 weekend · 2 river · 3 fancy · 4 love · 5 Count · 6 meaning · 7 swap · 8 bother · A bridge · B bread</p></div>
    <div class="k"><h3>8 · Phrases to steal</h3><p>1 c · 2 d · 3 a · 4 b</p></div>
   </div>
   <div>
    <div class="k"><h3>9 · Idioms · 10 · Yes, no or another time?</h3><p>9: 1 indeed · 2 fair-weather · 3 way · 4 pod · 5 ice · 6 off<br>10: {SORT_KEY}</p></div>
    <div class="k"><h3>11 · Say it better (2 points each)</h3><p>1 I made friends with my neighbour. / My neighbour and I became friends. · 2 I feel a bit lonely in this city. · 3 Do you want to hang out this weekend? / Would you like to meet up on Saturday? · 4 We should meet up sometime. / Are you free on Saturday morning? · 5 I miss you! / I've missed you!<br><i>Alone or lonely?</i> 1 alone · 2 lonely · 3 alone · 4 lonely · 5 lonely · 6 alone</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Crossword</h3><p>{{CW_KEY}}</p></div>{{CW_GRID}}</div>
    <div class="k"><h3>13 · The waving man · 14 · Your turn</h3><p>1 👋 waved back · 2 🛣️ "Well, I'm Tom." · 3 ⚽ joined football · 4 📣 "It's the waving man!" · 5 🍽️ eating together, dinners, walks · 6 🍲 soup and medicine<br><i>Think about it:</i> it broke the ice – everyone laughed, and he wasn't the new guy anymore.<br>14: your own answers – 2 points per good sentence.</p></div>
    <div class="k"><h3>Your score</h3><p>90–100 🏆 <b>A friend indeed!</b> · 70–89 🤝 <b>You hit it off</b> · 50–69 🧊 <b>Breaking the ice</b> · 0–49 👋 <b>Waving at the wrong person – listen again!</b></p></div>
   </div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy. And remember: the person you're too shy to talk to might be hoping you'll say hello! 👋💜<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
    <img class="char" src="img/f/29-duo-high-five-night.jpg" style="width:38mm">
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
    "{CW_GRID}", X.grid_html(cw, 3.0, solved=True, cls="cw cwk"))
html = head + EXTRA + "</style>\n</head>\n<body>\n" + body
(HERE / "template.html").write_text(html)
pts = [int(x) for x in re.findall(r'tag pts">(\d+) points', html)]
print("points", sum(pts), pts)
