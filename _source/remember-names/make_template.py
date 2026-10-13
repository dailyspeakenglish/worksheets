"""Writes template.html for the remember-names worksheet.
The CSS design system is copied from build-a-habit; the word search comes from ws.json (see _source/tools/wordsearch.py)."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import wordsearch as W

src = (HERE.parent / "build-a-habit" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Build a Habit Worksheet", "Remember Names Worksheet")
ws = json.loads((HERE / "ws.json").read_text())
W.check(ws)

EXTRA = """
/* ---- new in remember-names ---- */
.reasons{display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm}
.reasons div{border-radius:3.4mm;padding:2.4mm 3mm;font-size:8.4pt;line-height:1.38}
.reasons b.h{display:block;font-size:9.6pt;margin-bottom:.4mm}
.party{display:grid;grid-template-columns:repeat(6,1fr);gap:2.2mm}
.guest{background:#fff;border:1.3px solid var(--line);border-radius:3.4mm;padding:2mm 1.6mm;text-align:center;display:flex;flex-direction:column;align-items:center;gap:.8mm}
.guest .f{font-size:22pt;line-height:1.1}
.guest .nm{font-weight:800;color:var(--night);font-size:10.5pt}
.guest .hk{font-size:7.6pt;color:var(--muted);line-height:1.3}
.guest .wr{width:100%;height:6.4mm;border-bottom:1.3px solid var(--night)}
.abc{display:grid;grid-template-columns:repeat(7,1fr);gap:1.6mm}
.abc div{border-radius:2.6mm;padding:1.6mm 1mm;text-align:center;font-size:7.4pt;line-height:1.3}
.abc b{display:block;font-size:10pt;letter-spacing:.6mm;color:var(--night)}
.odd{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm 3mm;font-size:9.4pt}
.odd div{background:#fff;border:1.2px solid var(--line);border-radius:2.6mm;padding:1.8mm 3mm;display:flex;gap:2.4mm;align-items:center}
.odd .l{display:inline-flex;width:6.4mm;height:6.4mm;border-radius:50%;border:1.3px solid var(--night);align-items:center;justify-content:center;font-weight:800;color:var(--night);font-size:9.4pt}
.say td{padding:1.3mm 1.6mm;font-size:9pt;vertical-align:top;border-bottom:1px solid #EEE8F4}
.say td.s{width:44%;font-weight:600;color:var(--night)}
.say .o{display:flex;gap:1.6mm;align-items:center;margin:.3mm 0}
.collect th{background:var(--night);color:#F8E3C4;font-size:8.2pt;font-weight:600;padding:1.8mm 2mm;text-align:left}
.collect th:first-child{border-radius:3mm 0 0 0}.collect th:last-child{border-radius:0 3mm 0 0;text-align:center}
.collect td{border:1px solid #E6DFEE;height:7.6mm;font-size:8.4pt;padding:0 2mm;vertical-align:middle}
.collect td.d{font-weight:700;color:var(--night);background:var(--lav);width:12mm;text-align:center}
.collect td.c{text-align:center;width:20mm}
"""

def foot(n): return "{{FOOT%d}}" % n

clues = [
 ("REMEMBER", "Lucy couldn't {} Helen's name at the wedding."),
 ("MEMORABLE", "She has a very {} laugh – it's easy to remember."),
 ("INTRODUCE", "“Let me {} you to my sister.”"),
 ("BAKER", "People remember “he's a {}” better than “his name is Mr Baker”."),
 ("NEIGHBOUR", "For eight months, Jack didn't know his {}'s name."),
 ("NICKNAME", "“Bob” is a {} for Robert."),
 ("COLLEAGUE", "Priya is Jack's new {} at work."),
 ("WEDDING", "Lucy called Helen “Rachel” at a {}."),
 ("BISCUIT", "Jack always knew the cat's name: {}!"),
 ("COUSIN", "Helen was the bride's {}."),
]
assert sorted(w for w, _ in clues) == sorted(ws["pos"])
CLUES = "".join(f'      <div><span class="n">{i}</span><span>{t.format(W.slots(w))}</span></div>\n'
                for i, (w, t) in enumerate(clues, 1))

def chat(rows):
    out = []
    for who, img, text in rows:
        side = "l" if who == "LUCY" else "j"
        out.append(f'    <div class="msg {side}"><div class="ava"><img src="img/f/{img}-lav.jpg"></div>'
                   f'<div class="b"><span class="who">{who}</span>{text}</div></div>')
    return "\n".join(out)

def gap(n): return f'<span class="gap">{n}</span>'

CHAT = chat([
 ("LUCY", "09-lucy-talking-right", f"Hi, we met on {gap(1)}, didn't we? In the kitchen?"),
 ("JACK", "16-jack-surprised-left", f"Yes! Hi! Sorry, this is so {gap(2)}, but I'm terrible with names. What was your name {gap(3)}?"),
 ("LUCY", "12-lucy-laughing-right", "Don't worry, it happens to everyone! It's Priya."),
 ("JACK", "13-jack-talking-left", "Priya. That's a lovely name. Is it P-R-I-Y-A?"),
 ("LUCY", "11-lucy-asking-right", "Exactly. And you're Jack, right?"),
 ("JACK", "15-jack-shrug-left", f"That's right. Wow, you remembered. Now I feel even {gap(4)}."),
 ("LUCY", "32-lucy-coffee-chat-right", f"Don't. I only remembered because you told me you'd just moved here from the {gap(5)}, and I thought of jacks on a ship. You know, sailors."),
 ("JACK", "14-jack-listening-left", f"That's a great {gap(6)}. So, Priya, how are you {gap(7)} the job so far?"),
 ("LUCY", "10-lucy-listening-right", f"Good, but there are so many new faces. My head's {gap(8)}."),
 ("JACK", "13-jack-talking-left", "Same here. Hey, maybe we should make a list together."),
 ("LUCY", "09-lucy-talking-right", "Good idea. We can help each other out."),
])

GUESTS = [("👩‍🦰", "Rose", "a big red rose 🌹 behind her ear"),
          ("👨‍🦱", "Mark", "draws a mark ✏️ on his forehead"),
          ("👵", "Daisy", "a daisy 🌼 in her hat"),
          ("🧔", "Bill", "a duck's bill 🦆 – that's its mouth!"),
          ("👱‍♀️", "Sunny", "always smiling, like the sun ☀️"),
          ("👨‍🦲", "Robin", "a robin 🐦 sits on his head")]
PARTY_A = "".join(f'<div class="guest"><span class="f">{f}</span><span class="nm">{n}</span><span class="hk">{h}</span></div>' for f, n, h in GUESTS)
ORDER_B = [4, 0, 5, 2, 1, 3]   # Sunny, Rose, Robin, Daisy, Mark, Bill
PARTY_B = "".join(f'<div class="guest"><span class="f">{GUESTS[i][0]}</span><span class="small" style="font-weight:700;color:var(--mauve)">{k}</span><span class="wr"></span></div>' for k, i in enumerate(ORDER_B, 1))
KEY_B = " · ".join(f"{k} {GUESTS[i][1]}" for k, i in enumerate(ORDER_B, 1))

def opt(letter, text): return f'<div class="o"><span class="circ" style="width:5mm;height:5mm;font-size:7pt">{letter}</span>{text}</div>'
SAY = [
 ("1. It's noisy and you didn't hear a new person's name.", ["Sorry, I didn't catch your name.", "Sorry, I mixed you up.", "Have you two met?"]),
 ("2. You met someone this morning. Now it's 4 p.m. and you can't remember her name.", ["What is your name?", "Sorry, what was your name again?", "Nice to meet you!"]),
 ("3. You know the name… you can almost say it… but it won't come out!", ["It rings a bell.", "I'm terrible at names.", "It's on the tip of my tongue."]),
 ("4. Your friend Tom and your colleague Maria meet for the first time.", ["Tom, this is my colleague Maria.", "Maria is she my colleague.", "Remember Maria!"]),
 ("5. A new colleague always says your name wrong.", ["Say nothing for years.", "That's wrong!", "Actually, it's pronounced… But don't worry, everyone gets it wrong at first."]),
 ("6. You're not sure how to say someone's name.", ["Avoid using it.", "Am I saying that right?", "Can I call you Bob?"]),
]
SAY_KEY = "1 a · 2 b · 3 c · 4 a · 5 c · 6 b"
SAYROWS = "".join(f'<tr><td class="s">{s}</td><td>{"".join(opt(l, t) for l, t in zip("abc", o))}</td></tr>' for s, o in SAY)

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
      <h1>Why You Forget Names So Quickly</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">Three surprising reasons names slip away, simple tricks to remember them, polite English for when you forget – and Jack's eight-month neighbour mystery.</p>
      <div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div style="background:var(--lav);border-radius:6mm;height:60mm;position:relative;overflow:hidden;border:1px solid var(--lav2)">
      <div style="position:absolute;z-index:2;top:3.4mm;left:4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">Hi! I'm… wait, who are you? 😅</div>
      <img class="char" src="img/f/30-duo-waving-lav.jpg" style="position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:76mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · After you listen 💬</div><div class="s">Play the memory game, solve the word search and share your name disaster in the comments!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: Name disaster check <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Be honest! Tick everything that has happened to you. 🙈</p>
    <div style="display:grid;grid-template-columns:1.3fr .7fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:2mm;justify-content:center">
        <div style="display:flex;gap:2.4mm;align-items:center;font-size:9.2pt"><span class="box sm"></span>😳 I've called someone by the wrong name.</div>
        <div style="display:flex;gap:2.4mm;align-items:center;font-size:9.2pt"><span class="box sm"></span>💨 I forgot a name seconds after I heard it.</div>
        <div style="display:flex;gap:2.4mm;align-items:center;font-size:9.2pt"><span class="box sm"></span>🐱 I know someone's pet's name, but not theirs!</div>
        <div style="display:flex;gap:2.4mm;align-items:center;font-size:9.2pt"><span class="box sm"></span>🙈 I avoided someone because I forgot their name.</div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> Which is easier to remember about a new person?</div>
        <div style="display:flex;gap:4mm;font-size:8.9pt;flex-wrap:wrap"><span><span class="circ">a</span> "He's a baker."</span><span><span class="circ">b</span> "His name is Mr Baker."</span><span><span class="circ">c</span> the same</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 2:37</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:2mm 2.8mm;font-size:8.5pt;border:1.2px solid #F4D2C2;line-height:1.4"><b style="color:var(--night)">Lucy:</b> "At a wedding, I said, 'It was so nice to meet you, Rachel!' Her name was Helen." 🫣</div>
        <img class="char" src="img/f/34-lucy-shy-but-brave-peach.jpg" style="width:26mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – or write them in your notebook.</p>
    <div class="grid2" style="gap:3mm">
      <div class="card teal"><b>1.</b> Are you better with names or with faces?</div>
      <div class="card teal"><b>2.</b> Does your name have a short version or a nickname?</div>
      <div class="card teal"><b>3.</b> Do people ever say or spell your name wrong?</div>
      <div class="card teal"><b>4.</b> What do you usually do when you forget someone's name?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Check in the Word Tour at ⏱ 15:14</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> to recall</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> to mix up</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> on the tip of my tongue</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> to ring a bell</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> to introduce</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> memorable</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> to catch (a name)</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> embarrassing</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> a nickname</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> a colleague</td></tr>
      </table>
      <div class="card" style="font-size:9.1pt;line-height:1.62">
        <b>a)</b> to seem familiar, but you're not completely sure<br>
        <b>b)</b> a person you work with<br>
        <b>c)</b> to hear something clearly<br>
        <b>d)</b> to bring something back into your mind<br>
        <b>e)</b> easy to remember, because it's special or unusual<br>
        <b>f)</b> a short or friendly name, like Bob or Liz<br>
        <b>g)</b> to confuse two people or things<br>
        <b>h)</b> making you feel silly or uncomfortable<br>
        <b>i)</b> you know it, but you can't say it right now<br>
        <b>j)</b> to tell people each other's names when they first meet
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/19-lucy-glasses-book-w.jpg" style="width:24mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> <b style="color:var(--peach-d)">COL</b>-league · <b style="color:var(--peach-d)">NEIGH</b>-bour (the "gh" is silent!) · <b style="color:var(--peach-d)">MEM</b>-o-ra-ble · in-tro-<b style="color:var(--peach-d)">DUCE</b> · em-<b style="color:var(--peach-d)">BAR</b>-rass-ing. Say it out loud: <i>"Sorry, it's on the tip of my tongue!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>Forgetting names is normal – and simple tricks and polite phrases can help.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>People forget names because they don't care about other people.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>If you forget a name, it's always too late to ask again.</div>
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
      <div class="chips" style="margin-top:2.4mm;justify-content:center"><span>wedding</span><span>cake</span><span>flour</span><span>sailors</span><span>bike</span><span>passport</span><span>stairs</span><span>cat basket</span></div>
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
    <div class="mcq"><div class="qq">1. "It's on the tip of my tongue" means…</div><div class="opt"><span class="c">a</span>I said it too quickly</div><div class="opt"><span class="c">b</span>I almost remember it</div><div class="opt"><span class="c">c</span>it tastes strange</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">2. "Sorry, what ______ your name again?"</div><div class="opt"><span class="c">a</span>was</div><div class="opt"><span class="c">b</span>were</div><div class="opt"><span class="c">c</span>be</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">3. To "mix up" two people means to…</div><div class="opt"><span class="c">a</span>introduce them</div><div class="opt"><span class="c">b</span>take a photo of them</div><div class="opt"><span class="c">c</span>confuse them</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">4. You didn't hear a name. The most polite reply is…</div><div class="opt"><span class="c">a</span>"Say again your name."</div><div class="opt"><span class="c">b</span>"Sorry, I didn't catch your name."</div><div class="opt"><span class="c">c</span>"What?"</div><div class="hint">🧠 Think about it</div></div>
    <div class="mcq"><div class="qq">5. "Have you two met?" is a question we use to…</div><div class="opt"><span class="c">a</span>introduce two people</div><div class="opt"><span class="c">b</span>say goodbye</div><div class="opt"><span class="c">c</span>ask for directions</div><div class="hint">🧠 Common sense</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. What name did Lucy call the bride's cousin?</div><div class="opt"><span class="c">a</span>Helen</div><div class="opt"><span class="c">b</span>Claire</div><div class="opt"><span class="c">c</span>Rachel</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">7. People remembered the word better when "Baker" was…</div><div class="opt"><span class="c">a</span>the man's job</div><div class="opt"><span class="c">b</span>the man's name</div><div class="opt"><span class="c">c</span>the man's town</div><div class="hint">🎧 ⏱ 2:37</div></div>
    <div class="mcq"><div class="qq">8. With the next-in-line effect, we don't store what we hear just before…</div><div class="opt"><span class="c">a</span>we go to sleep</div><div class="opt"><span class="c">b</span>our own turn to speak</div><div class="opt"><span class="c">c</span>we eat lunch</div><div class="hint">🎧 ⏱ 5:25</div></div>
    <div class="mcq"><div class="qq">9. Lucy's first tip: when someone tells you their name…</div><div class="opt"><span class="c">a</span>write it on your hand</div><div class="opt"><span class="c">b</span>ask for their phone number</div><div class="opt"><span class="c">c</span>say it back immediately</div><div class="hint">🎧 ⏱ 7:38</div></div>
    <div class="mcq"><div class="qq">10. For eight months, Claire called Jack…</div><div class="opt"><span class="c">a</span>"the man with the bike"</div><div class="opt"><span class="c">b</span>"the man with the cat"</div><div class="opt"><span class="c">c</span>"the man next door"</div><div class="hint">🎧 ⏱ 19:37</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🧩</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> In the 1973 study, people forgot what they heard in the <b>9 seconds</b> before their own turn to speak.</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">4</span>Three reasons we forget names <span class="tag">think + listen</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">Read about the three reasons. Then write <b>A</b>, <b>B</b> or <b>C</b> next to each sentence (1–6). 🎧 ⏱ 2:37 · 5:25 · 6:46</p>
    </div>
    <img class="char" src="img/f/03-lucy-did-you-know-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <div class="reasons" style="margin-top:2.4mm">
    <div style="background:var(--peach-l)"><b class="h" style="color:var(--peach-d)">A · Baker-baker paradox 🥖</b>A job makes lots of connections in your brain. A name is just a sound – it has <b>no hooks</b>.<br><i>Fix: give the name a hook.</i></div>
    <div style="background:var(--lav)"><b class="h" style="color:var(--mauve-d)">B · The next-in-line effect 🙋</b>You're busy preparing what <b>you</b> will say, so the name never really arrives.<br><i>Fix: listen, then say it back.</i></div>
    <div style="background:var(--sage)"><b class="h" style="color:var(--sage-d)">C · The forgetting curve 📉</b>We forget new information <b>very quickly</b>, especially in the first hours.<br><i>Fix: write it down later.</i></div>
  </div>
  <table class="tf" style="margin-top:2.2mm">
    <tr><td class="n">1</td><td>"I was thinking about what to say, so I didn't really hear her name."</td><td class="ck"><span class="box"></span></td></tr>
    <tr><td class="n">2</td><td>"I remember he's a nurse with two dogs, but not his name."</td><td class="ck"><span class="box"></span></td></tr>
    <tr><td class="n">3</td><td>"I knew her name at lunchtime, but by the evening it was gone."</td><td class="ck"><span class="box"></span></td></tr>
    <tr><td class="n">4</td><td>"I was worried about my sweaty hand when he said, 'Hi, I'm Daniel.'"</td><td class="ck"><span class="box"></span></td></tr>
    <tr><td class="n">5</td><td>"I heard his name once and never used it again."</td><td class="ck"><span class="box"></span></td></tr>
    <tr><td class="n">6</td><td>"A name like 'Smith' doesn't connect to anything I know about her."</td><td class="ck"><span class="box"></span></td></tr>
  </table>

  <div class="sec">
    <h2><span class="num">5</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>Lucy talked to the bride's cousin for about twenty minutes.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>Jack doesn't know the name of his neighbour's cat.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 4:15</td></tr>
      <tr><td class="n">3</td><td>When people were told to pay attention before their turn, the problem disappeared.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 5:25</td></tr>
      <tr><td class="n">4</td><td>Ebbinghaus found that we forget new information slowly, over many years.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 6:46</td></tr>
      <tr><td class="n">5</td><td>In many English-speaking workplaces, people use first names quickly – even with the boss.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 10:03</td></tr>
      <tr><td class="n">6</td><td>In the end, Jack asked Claire for her name directly.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 19:37</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="card peach" style="padding:2.8mm 4mm">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:3mm">
        <div><b style="color:var(--night)">🧠 Memory game – part A</b> <span class="small">(the test is on page 7!)</span><br><span style="font-size:8.6pt">You're at a party. Meet six people. Read each name and <b>see the hook in your mind</b> for 1 minute. Then cover this box!</span></div>
        <img class="char" src="img/f/02-jack-lightbulb-idea-peach.jpg" style="width:17mm;flex:none">
      </div>
      <div class="party" style="margin-top:2mm">{PARTY_A}</div>
    </div>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">6</span>"What was your name again?" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Two new colleagues meet again in their first week. Listen at ⏱ 13:21 and write <b>one word</b> in each gap (1–8). Then answer A and B. The breakdown at ⏱ 14:27 can help.</p>
    </div>
    <img class="char" src="img/f/20-jack-glasses-laptop-w.jpg" style="width:25mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat" style="margin-top:2.6mm;gap:1.3mm">
{CHAT}
  </div>
  <div class="grid2" style="margin-top:2.8mm;gap:3mm">
    <div class="card" style="padding:2.4mm 4mm"><b style="color:var(--night)">A.</b> Which little <b>question tag</b> makes Lucy's first line friendly?<div class="lines"></div></div>
    <div class="card" style="padding:2.4mm 4mm"><b style="color:var(--night)">B.</b> Find the phrase that means <b>"support each other"</b>:<div class="lines"></div></div>
  </div>
  <div class="small" style="margin-top:2mm;text-align:center">🎭 <b>Say it out loud!</b> Play both parts – and use <b>your own name</b> instead of Jack's.</div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>What would you say? <span class="tag">polite phrases</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">Circle the best thing to say in each situation. 🎧 Help at ⏱ 12:20</p>
    </div>
    <img class="char" src="img/f/01-lucy-thumbs-up-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <table class="say" style="margin-top:2mm">{SAYROWS}</table>
  <div class="bub" style="margin-top:2.4mm">
    <img class="char" src="img/f/16-jack-surprised-left-w.jpg" style="width:18mm;flex:none">
    <div class="txt"><b>Jack's tip – don't wait!</b> The word <b>"again"</b> shows you know they told you before. And ask quickly: on day two, it's nothing. After eight months… it's very hard! 😬</div>
  </div>

  <div class="sec">
    <h2><span class="num">8</span>Spell it out! 🔤 <span class="tag">new! pronunciation</span><span class="tag pts">6 points</span></h2>
    <p class="instr">"Is it P-R-I-Y-A?" To spell names, you need the <b>names of the letters</b>. Letters in the same box share the same vowel sound.</p>
    <div class="abc">
      <div style="background:var(--peach-l)"><b>AHJK</b>/eɪ/ – d<b style="display:inline;font-size:7.4pt;letter-spacing:0">ay</b></div>
      <div style="background:var(--lav)"><b>BCDEG<br>PTV</b>/iː/ – s<b style="display:inline;font-size:7.4pt;letter-spacing:0">ee</b></div>
      <div style="background:var(--sage)"><b>FLMN<br>SXZ</b>/e/ – r<b style="display:inline;font-size:7.4pt;letter-spacing:0">e</b>d</div>
      <div style="background:var(--teal-l)"><b>IY</b>/aɪ/ – m<b style="display:inline;font-size:7.4pt;letter-spacing:0">y</b></div>
      <div style="background:var(--peach-l)"><b>O</b>/əʊ/ – g<b style="display:inline;font-size:7.4pt;letter-spacing:0">o</b></div>
      <div style="background:var(--lav)"><b>QUW</b>/uː/ – y<b style="display:inline;font-size:7.4pt;letter-spacing:0">ou</b></div>
      <div style="background:var(--sage)"><b>R</b>/ɑː/ – c<b style="display:inline;font-size:7.4pt;letter-spacing:0">ar</b></div>
    </div>
    <div class="small" style="margin:1.4mm 0 2.4mm 1mm">Z is "zed" in British English and "zee" in American English. Both are correct!</div>
    <p class="instr" style="margin:0 0 2mm 1mm"><b>Odd one out:</b> circle the letter with a <b>different</b> vowel sound.</p>
    <div class="odd">
      <div><b>1.</b><span class="l">A</span><span class="l">J</span><span class="l">E</span><span class="l">K</span></div>
      <div><b>2.</b><span class="l">B</span><span class="l">F</span><span class="l">P</span><span class="l">G</span></div>
      <div><b>3.</b><span class="l">M</span><span class="l">N</span><span class="l">L</span><span class="l">I</span></div>
      <div><b>4.</b><span class="l">Q</span><span class="l">O</span><span class="l">U</span><span class="l">W</span></div>
      <div><b>5.</b><span class="l">C</span><span class="l">D</span><span class="l">Y</span><span class="l">T</span></div>
      <div><b>6.</b><span class="l">S</span><span class="l">X</span><span class="l">F</span><span class="l">R</span></div>
    </div>
    <div class="card sage" style="margin-top:2.4mm;font-size:8.8pt;padding:2.4mm 4mm">🗣️ <b style="color:var(--night)">Your turn</b> <span class="small">(no points)</span>: Spell these names out loud: <b>PRIYA · CLAIRE · HELEN · YUSUF</b> – and then <b>your own name</b>. Which letters are tricky for you?</div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">9</span>Memory game – part B: Who's who? <span class="tag">new! memory hooks</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">Remember the party on page 4? <b>Don't look back!</b> Write each person's name. Think of the hook first. 🪝</p>
    </div>
    <img class="char" src="img/f/04-jack-thinking-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <div class="party" style="margin-top:2.4mm">{PARTY_B}</div>
  <div class="small" style="margin:1.8mm 0 0 1mm">💡 Did the hooks help? That's the Baker trick: you turned <b>Mr Baker</b> into <b>a baker</b>!</div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">10</span>Short names <span class="tag">culture</span><span class="tag pts">4 points</span></h2>
        <p class="instr" style="margin-bottom:0">Many English names have a short version. Match the names (1–4) to their short forms (a–d). ⏱ 10:03</p>
      </div>
    </div>
    <div class="grid2" style="margin-top:2mm;gap:4mm;align-items:center">
      <table class="match" style="font-size:9.3pt">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> Robert</td><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> Elizabeth</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> David</td><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> William</td></tr>
      </table>
      <div class="chips" style="justify-content:center"><span>a) Dave</span><span>b) Liz</span><span>c) Bill</span><span>d) Bob</span></div>
    </div>
    <div class="small" style="margin:1.8mm 0 0 1mm">😄 So if a colleague says <b>"Call me Dave"</b>, it's a friendly invitation – not a test!</div>
  </div>

  <div class="sec">
    <h2><span class="num">11</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 17:38</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "I don't remember your name, what is your name?"</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "I didn't hear your name good."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "My memory for names is very bad."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "I confused your name with another person."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "This is Maria, she is my friend, Maria this is Tom."</td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/07-lucy-great-job-w.jpg" style="width:18mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> <b>"I'm terrible with names"</b> is a little honest joke about yourself. It works because almost everyone feels the same. The answer is often: <i>"Oh, me too!"</i> 😄</div>
    </div>
  </div>
  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/08-jack-waving-w.jpg" style="width:20mm;flex:none">
      <div class="txt"><b>Share it with us!</b> Tell us your best <b>name disaster</b> in the comments – and one name you remember perfectly, and the trick that helped you. 💜</div>
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
    <img class="char" src="img/f/05-lucy-writing-w.jpg" style="width:19mm;flex:none;margin-top:-3mm">
  </div>
  <div style="display:grid;grid-template-columns:1fr auto;gap:3.4mm;margin-top:2.2mm;align-items:center">
    <div class="card white clues" style="padding:2.4mm 3.2mm">
{CLUES}    </div>
    <div>{W.grid_html(ws)}</div>
  </div>
  <div class="card sage" style="margin-top:2.6mm;padding:2.6mm 4mm">
    <b style="color:var(--night)">🤫 Step 3 – the secret message</b> <span class="small">(no points)</span> Cross out the 10 words. Then write the letters that are left, row by row, from left to right. You'll find two very useful sentences!
    <div class="msgrow" style="margin-top:2.6mm">{W.message_slots(ws['message'])}</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">13</span>Jack's neighbour mystery <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 19:37. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/33-jack-blue-scarf-good-morning-w.jpg" style="width:19mm;flex:none">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">🪜</span><span>On the stairs, Jack said, "Have you two met? This is my friend Sam."</span></div>
      <div class="ev"><span class="box"></span><span class="e">🙂</span><span>For eight months, they just smiled and said "Hi!"</span></div>
      <div class="ev"><span class="box"></span><span class="e">🤝</span><span>She shook Sam's hand and said, "Hi, I'm Claire."</span></div>
      <div class="ev"><span class="box"></span><span class="e">🏠</span><span>On the first day, she told Jack her name – and he forgot it.</span></div>
      <div class="ev"><span class="box"></span><span class="e">😂</span><span>The next day, Jack told Claire the truth. She laughed.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🚪</span><span>Jack's friend Sam came to visit.</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> What was the funny surprise at the end of the story?<div class="lines"></div></div>
  </div>
  {foot(8)}
</section>

<!-- ================= PAGE 9 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
    <div>
      <h2><span class="num">14</span>Your turn <span class="tag">writing</span><span class="tag pts">8 points</span></h2>
      <p class="instr" style="margin-bottom:0">Write two sentences in each box (2 points for each good sentence).</p>
    </div>
    <img class="char" src="img/f/05-lucy-writing-w.jpg" style="width:19mm;flex:none">
  </div>
  <div class="grid2" style="margin-top:2.4mm;gap:3mm;align-items:stretch">
    <div class="card" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">A. Give your name a hook 🪝</b>
      <div class="small" style="margin-top:1mm">Help people remember you! <i>e.g. "I'm Thiago. It's like Diego, but with a T." · "I'm Yusuf, but most people call me Joe."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. My name disaster 🙈</b>
      <div class="small" style="margin-top:1mm">Use <b>mix up</b>, <b>on the tip of my tongue</b> or <b>embarrassing</b>. <i>e.g. "Once, I mixed up two colleagues…"</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">📇</span>My name collector <span class="tag fun">your 7-day mission</span></h2>
    <p class="instr">Every time you meet someone new this week: say their name back, give it a hook – and write it here before it disappears! (That's how you beat the forgetting curve.)</p>
    <table class="collect">
      <tr><th>Day</th><th>Name</th><th>Hook or note <span style="font-weight:400">(e.g. Daniel – accounts – loves cycling 🚲)</span></th><th>Said it back?</th></tr>
      <tr><td class="d">1</td><td></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">2</td><td></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">3</td><td></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">4</td><td></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">5</td><td></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">6</td><td></td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">7</td><td></td><td></td><td class="c"><span class="box sm"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:var(--teal-d)">🙉 DIDN'T HEAR</b>Sorry, I didn't catch your name.<br>Could you tell me your name again?</div>
        <div><b style="color:var(--mauve-d)">🤔 FORGOT</b>Sorry, what was your name again?<br>Remind me of your name?</div>
        <div><b style="color:var(--peach-d)">😅 BE HONEST</b>I'm terrible with names, sorry!<br>I mixed you up with someone else.</div>
        <div><b style="color:var(--sage-d)">🤝 INTRODUCE</b>Have you two met?<br>Tom, this is my friend Maria.</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain three reasons why we forget names.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>ask politely when I didn't catch or forgot a name.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>spell my name clearly with English letter names.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>introduce two people: "Have you two met?"</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
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
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: a – a job is easier to remember than the same word as a name. · Predict: <b>passport</b> 🛂 isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 d · 2 g · 3 i · 4 a · 5 j · 6 e · 7 c · 8 h · 9 f · 10 b<br>Big idea: a (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 b · 2 a · 3 c · 4 b · 5 a · 6 c · 7 a · 8 b · 9 c · 10 a</p></div>
    <div class="k"><h3>4 · Three reasons we forget names</h3><p>1 B · 2 A · 3 C · 4 B · 5 C · 6 A</p></div>
    <div class="k"><h3>5 · True or false?</h3><p>1 T · 2 F (her name is Biscuit) · 3 T · 4 F (we forget quickly, especially in the first hours) · 5 T · 6 F (he introduced his friend Sam)</p></div>
    <div class="k"><h3>6 · "What was your name again?"</h3><p>1 Monday · 2 embarrassing · 3 again · 4 worse · 5 coast · 6 trick · 7 finding · 8 spinning · A didn't we · B help each other out</p></div>
    <div class="k"><h3>7 · What would you say?</h3><p>{SAY_KEY}</p></div>
    <div class="k"><h3>8 · Spell it out!</h3><p>1 E (/iː/) · 2 F (/e/) · 3 I (/aɪ/) · 4 O (/əʊ/) · 5 Y (/aɪ/) · 6 R (/ɑː/)</p></div>
    <div class="k"><h3>9 · Who's who? · 10 · Short names</h3><p>9: {KEY_B}<br>10: 1 d (Bob) · 2 b (Liz) · 3 a (Dave) · 4 c (Bill)</p></div>
    <div class="k"><h3>11 · Say it better (2 points each)</h3><p>1 Sorry, what was your name again? / Remind me of your name? · 2 Sorry, I didn't catch your name. · 3 I'm terrible (hopeless) with names. · 4 Sorry, I mixed you up with someone else. · 5 Tom, this is my friend Maria. Maria, this is Tom. / Have you two met?</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Word search (1 point per word)</h3><p>1 remember · 2 memorable · 3 introduce · 4 baker · 5 neighbour · 6 nickname · 7 colleague · 8 wedding · 9 biscuit · 10 cousin<br><b>Secret:</b> Sorry, I'm terrible with names. What was your name again?</p></div>{W.key_svg(ws, 40)}</div>
    <div class="k"><h3>13 · Neighbour mystery · 14 · Your turn</h3><p>1 🏠 first day · 2 🙂 eight months · 3 🚪 Sam visits · 4 🪜 "Have you two met?" · 5 🤝 "I'm Claire." · 6 😂 the truth<br><i>Surprise:</i> Claire didn't know Jack's name either!<br>14: your own answers – 2 points per good sentence.</p></div>
  </div>
  <div class="bands">
    <div><b>90–100 🏆</b>Name master!</div>
    <div><b>70–89 🪝</b>Hook pro</div>
    <div><b>50–69 🔔</b>It rings a bell</div>
    <div><b>0–49 👅</b>On the tip of your tongue – listen again!</div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy every week. (Our names are easy to remember. 😉)<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
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
