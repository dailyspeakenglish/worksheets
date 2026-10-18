"""Writes template.html for the talk-to-yourself worksheet (Podcast 60).
CSS design system copied from messy-room (which includes why-we-laugh, time-flies and build-a-habit).
Word search from ws.json (built by _source/tools/wordsearch.py). Timestamps: video time = NoteGPT time + 5 s."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import wordsearch as W

src = (HERE.parent / "messy-room" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Messy Room Worksheet", "Talk to Yourself Worksheet")
ws = json.loads((HERE / "ws.json").read_text())
W.check(ws)

EXTRA = """
/* ---- new in talk-to-yourself ---- */
.claim.chal{background:#DDF1E3;color:#1E7B45;border:1.2px solid #8FCBA3}.claim.chal .box{border-color:#1E7B45}
.claim.thr{background:#FBE1DE;color:#C0392B;border:1.2px solid #EDA59D}.claim.thr .box{border-color:#C0392B}
.ways{display:grid;grid-template-columns:1fr 1.5fr;gap:2.4mm 5mm;align-items:start}
.ways .ex{font-size:8.8pt;line-height:1.5}
.ways .ex div{margin-bottom:1.1mm}
.friend td{padding:1.8mm 1mm;font-size:9.2pt;vertical-align:bottom}
.friend td.i{width:52%;color:#C0392B}
.pep{display:grid;grid-template-columns:.8fr 1.1fr 1fr 1.25fr;gap:1.6mm 2.4mm;margin-top:1.6mm}
.pep>div{border-radius:3mm;padding:1.8mm 2.6mm;font-size:9.4pt;color:var(--night)}
.pep .lb{display:block;font-size:6.8pt;font-weight:800;letter-spacing:.3pt;margin-bottom:.4mm}
.pep .me{background:none;padding:2.4mm 1mm 0}
.ws td{width:7mm;height:7mm;font-size:10.2pt}
.clues{font-size:8.8pt;gap:1.7mm}
.hero2{background:var(--lav);border-radius:6mm;height:55mm;position:relative;overflow:hidden;border:1px solid var(--lav2)}
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
 ("JACK", "16-jack-surprised-left", f"Lucy? Are you okay? Who are you talking {gap(1)}?"),
 ("LUCY", "36-lucy-surprised-right", f"Oh! Sorry. Nobody. I was just thinking out {gap(2)}."),
 ("JACK", "15-jack-shrug-left", "It sounded like you were having a serious argument."),
 ("LUCY", "38-lucy-explaining-right", f"I was {gap(3)} what I'm going to say in the meeting this afternoon. I always get {gap(4)}, so I practise first."),
 ("JACK", "14-jack-listening-left", "That's actually a really good idea. Does it help?"),
 ("LUCY", "09-lucy-talking-right", f"It really does. By the time I'm in the meeting, I've already said it three times, so it comes {gap(5)} more naturally."),
 ("JACK", "44-jack-embarrassed-left", f"Maybe I should try that. I always go {gap(6)} in meetings."),
 ("LUCY", "40-lucy-excited-right", f"Try it. And give yourself a little {gap(7)} talk before you go in. “Come on, Jack, you've {gap(8)} this.”"),
 ("JACK", "13-jack-talking-left", "In the toilets, maybe. Not in the middle of the office."),
 ("LUCY", "39-lucy-caring-right", "Wherever works for you. Honestly, nobody really notices."),
 ("JACK", "41-jack-laughing-left", "Well, I noticed."),
 ("LUCY", "12-lucy-laughing-right", "Okay, almost nobody."),
])

def chip_pair(i, text):
    return (f'<div class="sit"><div class="t" style="min-height:0"><b>{i}.</b> {text}</div><div class="ch" style="gap:2mm">'
            f'<span class="claim chal"><span class="box"></span>💪 CHALLENGE</span>'
            f'<span class="claim thr"><span class="box"></span>⚠️ THREAT</span></div></div>')
CHAL = "".join(chip_pair(i, t) for i, t in enumerate([
    "“This is hard, but I can do it.”",
    "“This is going to destroy me.”",
    "“I'm going to let everyone down.”",
    "“Jack, you've practised. You're ready.”"], 1))

clues = [
 ("REHEARSE", "Actors {} before a play."),
 ("LENTILS", "Lucy: “Where are you, {}?”"),
 ("GLASSES", "Jack's mum's {} are always on her head!"),
 ("PRONOUN", "Kross changed the {}: “I” → “you”."),
 ("NARRATE", "Like a commentator, {} your day."),
 ("TEAPOT", "People had to find an object like a {}."),
 ("SHOWER", "Jack argues with nobody in the {}!"),
 ("MUTTER", "To speak quietly, so others can't hear: to {}."),
 ("PEELER", "“The thing for the potatoes?” “It's a {}!”"),
 ("COACH", "Mr Davies was Jack's football {}."),
]
assert sorted(w for w, _ in clues) == sorted(ws["pos"])
def nw(t):  # keep the letter slots and the punctuation after them on one line
    return re.sub(r"\{\}(\S*)", lambda m: '<span style="white-space:nowrap">{}' + m.group(1) + '</span>', t)
CLUES = "".join(f'      <div><span class="n">{i}</span><span>{nw(t).format(W.slots(w))}</span></div>\n'
                for i, (w, t) in enumerate(clues, 1))
WS_KEY = " · ".join(f"{i} {w.lower()}" for i, (w, _) in enumerate(clues, 1))

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
      <h1>Why Talking to Yourself Is Actually Smart</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">How saying a word out loud helps you find things, the tiny self-talk trick that calms you down, five ways to practise English on your own – and Jack's football coach.</p>
      <div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div class="hero2">
      <div style="position:absolute;z-index:2;top:3.4mm;left:3.4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">"Where are you, lentils?!" 🫘</div>
      <img class="char" src="img/f/71-lucy-embarrassed-lav.jpg" style="position:absolute;bottom:0;left:3mm;width:36mm">
      <img class="char" src="img/f/41-jack-laughing-left-lav.jpg" style="position:absolute;bottom:0;right:2mm;width:35mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · After you listen 💬</div><div class="s">Find the secret message, write your own pep talk – and read your answers out loud!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: My self-talk check <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Be honest! Tick everything that is true for you. 😄</p>
    <div style="display:grid;grid-template-columns:1.42fr .58fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:1.8mm;justify-content:center;padding:2.6mm 3.6mm">
        <div class="conf" style="grid-template-columns:1fr 1fr;justify-content:stretch;font-size:8.7pt">
          <div><span class="box sm"></span>🔍 I say things' names to find them</div>
          <div><span class="box sm"></span>🚿 I talk in the shower</div>
          <div><span class="box sm"></span>📞 I practise before phone calls</div>
          <div><span class="box sm"></span>😤 I mutter when I'm annoyed</div>
          <div><span class="box sm"></span>💪 I give myself pep talks</div>
          <div><span class="box sm"></span>🙈 I've been caught talking to myself</div>
        </div>
        <div style="font-size:9pt"><b style="color:var(--night)">My self-talk score:</b> <span class="blank s"></span> / 6</div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> People looked for a teapot in a picture. Saying <i>"teapot"</i> out loud…</div>
        <div style="display:flex;gap:3.4mm;font-size:8.7pt;white-space:nowrap"><span><span class="circ">a</span> made them slower</span><span><span class="circ">b</span> helped them find it faster</span><span><span class="circ">c</span> didn't change anything</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 2:16</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:1.8mm 2.4mm;font-size:8.1pt;border:1.2px solid #F4D2C2;line-height:1.36"><b style="color:var(--night)">Jack:</b> "I argue in the shower – and I always win!" 🚿</div>
        <img class="char" src="img/f/55-jack-thumbs-up-peach.jpg" style="width:30mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – yes, to yourself! – or write them in your notebook.</p>
    <div class="grid2" style="gap:2.4mm">
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>1.</b> Do you ever talk to yourself? When and where?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>2.</b> What do you usually say to yourself when you're nervous?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>3.</b> How do you practise speaking English when you're alone?</div>
      <div class="card teal" style="padding:2.2mm 3.6mm"><b>4.</b> What's the best advice a teacher or coach ever gave you?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Then check at ⏱ 12:54 and ⏱ 13:48</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> to think out loud</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> to rehearse</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> to narrate</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> a pep talk</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> to mutter</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> your inner voice</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> to go blank</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> to go over something</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> on my own</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> a challenge</td></tr>
      </table>
      <div class="card" style="font-size:9.1pt;line-height:1.62">
        <b>a)</b> to describe what is happening while it happens, like a commentator<br>
        <b>b)</b> when your mind suddenly becomes empty<br>
        <b>c)</b> to speak quietly, so other people can't really hear<br>
        <b>d)</b> to say your thoughts aloud while you decide or solve something<br>
        <b>e)</b> alone, without other people<br>
        <b>f)</b> the voice in your head that you hear when you think<br>
        <b>g)</b> something difficult, but possible<br>
        <b>h)</b> to practise something before you do it for real<br>
        <b>i)</b> to check or review something carefully<br>
        <b>j)</b> a short speech to encourage someone
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/53-jack-listen-carefully-w.jpg" style="width:24mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> <b style="color:var(--peach-d)">MUT</b>-ter · re-<b style="color:var(--peach-d)">HEARSE</b> (/rɪˈhɜːs/) · re-<b style="color:var(--peach-d)">HEAR</b>-sal · nar-<b style="color:var(--peach-d)">RATE</b> · <b style="color:var(--peach-d)">PEP</b> talk · <span style="white-space:nowrap"><b style="color:var(--peach-d)">IN</b>-ner <b style="color:var(--peach-d)">VOICE</b>.</span> Say it out loud – to yourself: <i>"Come on, you've got this!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>Talking to yourself is a bad sign, so it's better to stop doing it.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>Only famous athletes should talk about themselves using their own name.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>Talking to yourself – kindly, and in English – can help you find things, stay calm and practise speaking.</div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <div class="ava" style="width:22mm;height:22mm"><img src="img/f/10-lucy-listening-right-lav.jpg" style="height:140%"></div>
      <div class="txt"><b>Lucy's tip:</b> First listen = the <b>big picture</b>. Don't stop the video and don't worry about every word. Second listen = the <b>details</b>. That's when you answer the 🎧 questions.</div>
    </div>
  </div>

  <div class="sec">
    <div class="card sage">
      <b style="color:var(--night)">🔮 Predict before you listen!</b> <span class="small">(no points)</span> Seven of these words are in the episode. One is <b>not</b>. Circle the one you think you <b>won't</b> hear – then check while you listen.
      <div class="chips predict-chips" style="margin-top:2mm;justify-content:center;gap:1.4mm"><span>lentils</span><span>teapot</span><span>cola</span><span>onions</span><span>peeler</span><span>piano</span><span>football</span><span>wedding</span></div>
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
    <div class="mcq"><div class="qq">1. If you "mutter", you…</div><div class="opt"><span class="c">a</span>speak quietly, so others can't really hear</div><div class="opt"><span class="c">b</span>shout at someone</div><div class="opt"><span class="c">c</span>sing very loudly</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">2. "Who are you talking ______?"</div><div class="opt"><span class="c">a</span>with</div><div class="opt"><span class="c">b</span>to</div><div class="opt"><span class="c">c</span>at</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">3. "I said to ______, 'Don't worry.'"</div><div class="opt"><span class="c">a</span>me</div><div class="opt"><span class="c">b</span>myself</div><div class="opt"><span class="c">c</span>mine</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">4. A "pep talk" is…</div><div class="opt"><span class="c">a</span>a long, boring lecture</div><div class="opt"><span class="c">b</span>an argument with a friend</div><div class="opt"><span class="c">c</span>a short speech to encourage someone</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">5. "Come on, you've got this!" means…</div><div class="opt"><span class="c">a</span>You can do it!</div><div class="opt"><span class="c">b</span>It's in your bag.</div><div class="opt"><span class="c">c</span>Give it to me.</div><div class="hint">🧠 Everyday English</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. What was Lucy looking for in the supermarket?</div><div class="opt"><span class="c">a</span>lentils</div><div class="opt"><span class="c">b</span>butter</div><div class="opt"><span class="c">c</span>a teapot</div><div class="hint">🎧 ⏱ 0:05</div></div>
    <div class="mcq"><div class="qq">7. When people said the name of a product they <b>didn't</b> know well, it…</div><div class="opt"><span class="c">a</span>helped a lot</div><div class="opt"><span class="c">b</span>slowed them down</div><div class="opt"><span class="c">c</span>made them laugh</div><div class="hint">🎧 ⏱ 2:16</div></div>
    <div class="mcq"><div class="qq">8. About how many people took part in Ethan Kross's seven studies?</div><div class="opt"><span class="c">a</span>sixty</div><div class="opt"><span class="c">b</span>six thousand</div><div class="opt"><span class="c">c</span>nearly six hundred</div><div class="hint">🎧 ⏱ 4:31</div></div>
    <div class="mcq"><div class="qq">9. What does Lucy usually say to herself when she's nervous?</div><div class="opt"><span class="c">a</span>"Why do you always do this?"</div><div class="opt"><span class="c">b</span>"Lucy, you've got this."</div><div class="opt"><span class="c">c</span>"Lucy, don't mess this up."</div><div class="hint">🎧 ⏱ 7:46</div></div>
    <div class="mcq"><div class="qq">10. How old was Jack when he learned his special sentence?</div><div class="opt"><span class="c">a</span>twelve</div><div class="opt"><span class="c">b</span>sixteen</div><div class="opt"><span class="c">c</span>twenty-one</div><div class="hint">🎧 ⏱ 17:32</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">👓</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> Jack's mum mutters <i>"Glasses, glasses…"</i> when she looks for her glasses – and they're always on her head!</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">4</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>Lucy pretended to be on the phone – but she wasn't holding a phone.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>Jack has arguments in the shower, and he always loses.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">3</td><td>People who said the word out loud found the object faster.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:16</td></tr>
      <tr><td class="n">4</td><td>Saying a name helps most when you know what the thing looks like.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:16</td></tr>
      <tr><td class="n">5</td><td>Kross was mainly interested in <i>whether</i> people talk to themselves.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 4:31</td></tr>
      <tr><td class="n">6</td><td>Talking to yourself always helps, whatever you say.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 7:46</td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">5</span>Two studies and a coach 🔍 <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Who or what is each sentence about? Write <b>A</b>, <b>B</b> or <b>C</b>. ⏱ 2:16 · 4:31 · 17:32</p>
      </div>
      <img class="char" src="img/f/46-lucy-magnifying-glass-w.jpg" style="width:19mm;flex:none">
    </div>
    <div class="studies" style="margin-top:2mm">
      <div style="background:var(--peach-l)"><b class="h" style="color:var(--peach-d)">A · Finding things 🫖</b>2012 · Lupyan &amp; Swingley · saying names out loud</div>
      <div style="background:var(--lav)"><b class="h" style="color:var(--mauve-d)">B · Stress 😰</b>2014 · Ethan Kross, University of Michigan · "I" or your name?</div>
      <div style="background:var(--sage)"><b class="h" style="color:var(--sage-d)">C · Mr Davies ⚽</b>Jack's football coach, when Jack was twelve</div>
    </div>
    <table class="tf" style="margin-top:1.6mm">
      <tr><td class="n">1</td><td>People prepared a short speech with very little time.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">2</td><td>People looked for one object, like a teapot, among lots of pictures.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">3</td><td>He sat down next to Jack in the changing room.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">4</td><td>Saying the name of a familiar product, like cola, helped people find it.</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">5</td><td>He asked, "What are you saying to yourself?"</td><td class="ck"><span class="box"></span></td></tr>
      <tr><td class="n">6</td><td>People who used their own name felt less anxious, and their speeches were rated as better.</td><td class="ck"><span class="box"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">6</span>Challenge or threat? <span class="tag">new! think about it</span><span class="tag pts">4 points</span></h2>
        <p class="instr" style="margin-bottom:0">A <b>challenge</b> is difficult, but possible. A <b>threat</b> is something dangerous. How does each sentence see the situation? ⏱ 4:31</p>
      </div>
      <img class="char" src="img/f/34-lucy-shy-but-brave-w.jpg" style="width:18mm;flex:none">
    </div>
    <div class="grid2" style="margin-top:2mm;gap:2.2mm">{CHAL}</div>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>"Who are you talking to?" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">A colleague catches Lucy talking to herself in the office. Listen at ⏱ 11:54 and write <b>one word</b> in each gap (1–8). Then answer A and B. The breakdown at ⏱ 12:54 can help.</p>
    </div>
    <img class="char" src="img/f/63-jack-at-work-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat wide" style="margin-top:2.4mm;gap:.9mm">
{CHAT}
  </div>
  <div class="grid2" style="margin-top:2.6mm;gap:3mm">
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">A.</b> Very formal: "<span class="blank" style="min-width:14mm"></span> whom are you talking?"</div>
    <div class="card" style="padding:2.2mm 4mm;font-size:9.2pt"><b style="color:var(--night)">B.</b> Jack's pep talk place: in the <span class="blank" style="min-width:24mm"></span></div>
  </div>

  <div class="sec" style="margin-top:4mm">
    <h2><span class="num">🎭</span>Your turn to rehearse <span class="tag fun">speak · no points</span></h2>
    <p class="instr">Think of a conversation <b>you</b> will have this week (a phone call, a meeting…). Write two lines for each person – then say <b>both parts</b> out loud, like Lucy!</p>
    <div class="card white" style="padding:1mm 4mm 2.2mm;display:grid;grid-template-columns:auto 1fr auto 1fr;gap:0 3mm;align-items:end;font-size:9pt">
      <b style="color:var(--peach-d)">Me:</b><div class="lines"></div><b style="color:var(--mauve-d)">Them:</b><div class="lines"></div>
      <b style="color:var(--peach-d)">Me:</b><div class="lines"></div><b style="color:var(--mauve-d)">Them:</b><div class="lines"></div>
    </div>
  </div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">8</span>Phrases to steal <span class="tag">expressions</span><span class="tag pts">4 points</span></h2>
    <p class="instr">Match each phrase (1–4) to its meaning (a–d). ⏱ 0:05 · 12:54</p>
    <div class="grid2" style="gap:4mm;align-items:start">
      <table class="match" style="font-size:9.2pt">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> "You've got this!"</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> "Wherever works for you."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> "It comes out more naturally."</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> "They can't answer back."</td></tr>
      </table>
      <div class="card" style="font-size:8.9pt;line-height:1.62">
        <b>a)</b> In any place that's good for you.<br>
        <b>b)</b> They can't reply or argue with you.<br>
        <b>c)</b> You can do it!<br>
        <b>d)</b> It sounds more natural when you say it.
      </div>
    </div>
  </div>
  <div class="sec" style="display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">9</span>Myself, yourself… or each other? <span class="tag">new! reflexive pronouns</span><span class="tag pts">8 points</span></h2>
      <p class="instr" style="margin-bottom:0">Complete each sentence with a word from the box. One word is used twice.</p>
    </div>
    <img class="char" src="img/f/48-lucy-holding-blank-card-w.jpg" style="width:18mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chips" style="margin:1.6mm 0 2mm 10.8mm"><span>myself</span><span>yourself</span><span>himself</span><span>herself</span><span>ourselves</span><span>themselves</span><span>each other</span></div>
  <table class="coll" style="margin-left:2mm">
    <tr><td>1. I often talk to <span class="blank"></span> in the shower. 🚿</td></tr>
    <tr><td>2. "Lucy, give <span class="blank"></span> a pep talk before the meeting!"</td></tr>
    <tr><td>3. Jack's mum muttered to <span class="blank"></span>: "Glasses, glasses…" 👓</td></tr>
    <tr><td>4. Before every important moment, Jack says the sentence to <span class="blank"></span>.</td></tr>
    <tr><td>5. Lucy and Jack agree: "We need to talk to <span class="blank"></span> more nicely."</td></tr>
    <tr><td>6. Some athletes talk about <span class="blank"></span> using their own name.</td></tr>
    <tr><td>7. Every week on the podcast, Jack and Lucy talk to <span class="blank"></span>. 🎙️</td></tr>
    <tr><td>8. I practise speaking on my own = I practise speaking by <span class="blank"></span>.</td></tr>
  </table>
  <div class="bub" style="margin-top:2.2mm">
    <img class="char" src="img/f/02-jack-lightbulb-idea-w.jpg" style="width:17mm;flex:none">
    <div class="txt"><b>Jack's tip:</b> <b>by myself</b> = <b>on my own</b> = alone. And look at the difference: two people talk to <b>each other</b> 👫 – but when you're alone, you talk to <b>yourself</b> 🙋.</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">10</span>Small word at the end <span class="tag">new! questions</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">In everyday questions, the preposition goes at the <b>end</b>. Complete each question with <b>to</b>, <b>for</b>, <b>about</b>, <b>at</b>, <b>from</b> or <b>with</b>. ⏱ 12:54</p>
      </div>
      <img class="char" src="img/f/72-jack-confused-w.jpg" style="width:18mm;flex:none">
    </div>
    <div class="grid2" style="margin-top:2mm;gap:3mm">
      <table class="coll">
        <tr><td>1. 🗣️ Who are you talking <span class="blank s"></span>?</td></tr>
        <tr><td>2. 🔍 What are you looking <span class="blank s"></span>?</td></tr>
        <tr><td>3. 💭 What are you thinking <span class="blank s"></span>?</td></tr>
      </table>
      <table class="coll">
        <tr><td>4. ⚽ Who did you learn that <span class="blank s"></span>?</td></tr>
        <tr><td>5. 😂 What are you laughing <span class="blank s"></span>?</td></tr>
        <tr><td>6. 💬 Who do you practise English <span class="blank s"></span>?</td></tr>
      </table>
    </div>
    <div class="bub" style="margin-top:2.2mm">
      <img class="char" src="img/f/01-lucy-thumbs-up-w.jpg" style="width:17mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> <i>"Who are you talking to?"</i> ✓ is natural, everyday English. <i>"To whom are you talking?"</i> is correct too – but it sounds very formal, like an old book. 📜</div>
    </div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">11</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 15:47</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "I speak with myself."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "I was thinking with a loud voice."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "I said to me, 'Don't worry.'"</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "Come on, you can!"</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "I make practice of speaking alone."</td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/07-lucy-great-job-w.jpg" style="width:18mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> <b>"Go over"</b> means to check or review something carefully: <i>"Before the interview, I go over it in my head."</i> Very useful!</div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">🏠</span>Five ways to practise on your own <span class="tag fun">match · no points</span></h2>
        <p class="instr" style="margin-bottom:0">Match each way (1–5) to an example (a–e). Then choose one to try today! ⏱ 8:52</p>
      </div>
      <img class="char" src="img/f/66-duo-podcast-w.jpg" style="width:26mm;flex:none">
    </div>
    <div class="ways card white" style="margin-top:2mm;padding:2.6mm 4mm">
      <table class="match" style="font-size:9.1pt">
        <tr><td class="ans"><span class="box sm"></span></td><td><b style="color:var(--night)">1.</b> 🍳 narrate your day</td></tr>
        <tr><td class="ans"><span class="box sm"></span></td><td><b style="color:var(--night)">2.</b> 📞 rehearse a conversation</td></tr>
        <tr><td class="ans"><span class="box sm"></span></td><td><b style="color:var(--night)">3.</b> 🤔 think out loud</td></tr>
        <tr><td class="ans"><span class="box sm"></span></td><td><b style="color:var(--night)">4.</b> 💪 give yourself a pep talk</td></tr>
        <tr><td class="ans"><span class="box sm"></span></td><td><b style="color:var(--night)">5.</b> 🎙️ record yourself</td></tr>
      </table>
      <div class="ex">
        <div><b>a)</b> "Hello, I'd like to make an appointment." "Of course, what's your name?"</div>
        <div><b>b)</b> "Okay, Jack. You've prepared. Speak slowly and you'll be fine."</div>
        <div><b>c)</b> "Okay, now I'm cutting the onions. I need a bigger pan."</div>
        <div><b>d)</b> Talk for two minutes on your phone, then listen back.</div>
        <div><b>e)</b> "Should I go to the shop first or the post office? Hmm…"</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">💜</span>Be your own friend <span class="tag fun">write · no points</span></h2>
        <p class="instr" style="margin-bottom:0">Change the harsh <b>"I" voice</b> into a kind friend's voice. Use <b>your name</b> and <b>"you"</b>. ⏱ 4:31 · 7:46</p>
      </div>
      <img class="char" src="img/f/39-lucy-caring-right-w.jpg" style="width:18mm;flex:none">
    </div>
    <table class="friend" style="margin-top:1.6mm">
      <tr><td class="i">😣 "I'm so stupid. I'll never learn English."</td><td>💜 <span class="blank s"></span>, you <span class="blank l" style="min-width:52mm"></span></td></tr>
      <tr><td class="i">😣 "I'm going to fail this interview."</td><td>💜 <span class="blank s"></span>, you <span class="blank l" style="min-width:52mm"></span></td></tr>
      <tr><td class="i">😣 "Why do I always do this?"</td><td>💜 <span class="blank s"></span>, you <span class="blank l" style="min-width:52mm"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <h2><span class="num">⚽</span>Build a pep talk like Mr Davies <span class="tag fun">speak · no points</span></h2>
    <p class="instr">Jack's coach gave him a sentence in four parts. Build your own, then say it out loud three times! ⏱ 17:32</p>
    <div class="pep">
      <div style="background:var(--peach-l)"><span class="lb" style="color:var(--peach-d)">1 · YOUR NAME</span><b>"Jack,</b></div>
      <div style="background:var(--lav)"><span class="lb" style="color:var(--mauve-d)">2 · WHAT YOU DID</span><b>you've practised.</b></div>
      <div style="background:var(--sage)"><span class="lb" style="color:var(--sage-d)">3 · HOW YOU ARE</span><b>You're ready.</b></div>
      <div style="background:var(--teal-l)"><span class="lb" style="color:var(--teal-d)">4 · ONE SMALL ACTION</span><b>Breathe out, and go."</b></div>
      <div class="me"><span class="blank xl"></span></div><div class="me"><span class="blank xl"></span></div><div class="me"><span class="blank xl"></span></div><div class="me"><span class="blank xl"></span></div>
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
  <div style="display:grid;grid-template-columns:1fr auto;gap:3.4mm;margin-top:2.2mm;align-items:center">
    <div class="card white clues" style="padding:2.4mm 3.2mm">
{CLUES}    </div>
    <div>{W.grid_html(ws)}</div>
  </div>
  <div class="card sage" style="margin-top:2.6mm;padding:2.6mm 4mm">
    <b style="color:var(--night)">🤫 Step 3 – the secret message</b> <span class="small">(no points)</span> Cross out the 10 words. Then write the letters that are left, row by row, from left to right. It's Jack's last piece of advice in the episode!
    <div class="msgrow" style="margin-top:2.6mm">{W.message_slots(ws['message'])}</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">13</span>Jack and the football coach ⚽ <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 17:32. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/57-jack-exercise-w.jpg" style="width:17mm;flex:none">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">😰</span><span>In the changing room, he told himself, "I'm going to let everyone down."</span></div>
      <div class="ev"><span class="box"></span><span class="e">⚽</span><span>At twelve, Jack played in a small local football team.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🗣️</span><span>He said the new sentence out loud three times.</span></div>
      <div class="ev"><span class="box"></span><span class="e">😬</span><span>Before an important match, he couldn't stop shaking.</span></div>
      <div class="ev"><span class="box"></span><span class="e">😊</span><span>He didn't score, but he didn't shake – and he enjoyed the game.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🧓</span><span>Mr Davies sat down next to him: "What are you saying to yourself?"</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> When does Jack still say his sentence today? Write two moments.<div class="lines"></div><div class="lines"></div></div>
  </div>
  {foot(8)}
</section>

<!-- ================= PAGE 9 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">14</span>Your turn <span class="tag">writing</span><span class="tag pts">8 points</span></h2>
      <p class="instr" style="margin-bottom:0">2 points for each good sentence. Then read your sentences out loud!</p>
    </div>
    <img class="char" src="img/f/05-lucy-writing-w.jpg" style="width:17mm;flex:none;margin-top:-3mm">
  </div>
  <div class="grid2" style="margin-top:2.2mm;gap:3mm;align-items:stretch">
    <div class="card" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">A. Caught! 🙈</b>
      <div class="small" style="margin-top:1mm">When do you talk to yourself? Were you ever caught? <i>e.g. "I always mutter when I'm looking for my phone."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. Narrate it 🎙️</b>
      <div class="small" style="margin-top:1mm">Describe what you're doing right now, like a commentator. <i>e.g. "Right now I'm sitting at my desk and drinking tea."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">⏱</span>My talk-to-myself week <span class="tag fun">your 7-day mission</span></h2>
        <p class="instr" style="margin-bottom:0">Talk to yourself in English for five minutes every day. Nobody is listening – so relax!</p>
      </div>
      <img class="char" src="img/f/59-jack-phone-w.jpg" style="width:16mm;flex:none">
    </div>
    <table class="log week" style="margin-top:2mm">
      <tr><th>Day</th><th>Mission</th><th>A new word or phrase I needed</th><th>Done?</th></tr>
      <tr><td class="d">1</td><td class="a">🍳 narrate your cooking</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">2</td><td class="a">📞 rehearse a phone call</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">3</td><td class="a">🗓️ plan your day out loud</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">4</td><td class="a">🎙️ record yourself: 2 minutes</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">5</td><td class="a">💪 a pep talk with your name</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">6</td><td class="a">🎬 describe a film</td><td></td><td class="c"><span class="box sm"></span></td></tr>
      <tr><td class="d">7</td><td class="a">🎧 listen back to Day 4</td><td></td><td class="c"><span class="box sm"></span></td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:var(--sage-d)">🗣️ THINK OUT LOUD</b>I'm just thinking out loud.<br>I talk to myself.<br>I said to myself…</div>
        <div><b style="color:var(--peach-d)">💪 PEP TALK</b>Come on, you've got this!<br>You can do it!<br>[Name], you're ready.</div>
        <div><b style="color:var(--mauve-d)">🎭 REHEARSE</b>I rehearse what I'll say.<br>I go over it in my head.<br>I always go blank!</div>
        <div><b style="color:#C0392B">💜 BE KIND</b>Use your name or "you".<br>Talk like a friend.<br>A challenge, not a threat.</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain why saying a word out loud can help you find something.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>give myself a short pep talk using my name.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use think out loud, rehearse, narrate and go blank.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use myself / each other and end questions with "to" or "for".</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/52-lucy-phone-comment-w.jpg" style="width:19mm;flex:none">
      <div class="txt"><b>Share it with us!</b> Write your own pep talk in the comments – with your name: <b>"Maria, you've practised, you're ready."</b> And tell us: have you ever been caught talking to yourself? 🫘😅</div>
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
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: b – people who said the word out loud found it faster. · Predict: <b>piano</b> 🎹 isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 d · 2 h · 3 a · 4 j · 5 c · 6 f · 7 b · 8 i · 9 e · 10 g<br>Big idea: c (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 a · 2 b · 3 b · 4 c · 5 a · 6 a · 7 b · 8 c · 9 c · 10 a</p></div>
    <div class="k"><h3>4 · True or false?</h3><p>1 T · 2 F (he always wins) · 3 T · 4 T · 5 F (he was interested in <i>how</i> – which words we use) · 6 F (it depends on what you say)</p></div>
    <div class="k"><h3>5 · Two studies and a coach · 6 · Challenge or threat?</h3><p>5: 1 B · 2 A · 3 C · 4 A · 5 C · 6 B<br>6: 1 challenge · 2 threat · 3 threat · 4 challenge</p></div>
    <div class="k"><h3>7 · "Who are you talking to?"</h3><p>1 to · 2 loud · 3 rehearsing · 4 nervous · 5 out · 6 blank · 7 pep · 8 got · A To · B toilets</p></div>
    <div class="k"><h3>8 · Phrases to steal</h3><p>1 c · 2 a · 3 d · 4 b</p></div>
    <div class="k"><h3>9 · Myself, yourself… · 10 · Small word at the end</h3><p>9: 1 myself · 2 yourself · 3 herself · 4 himself · 5 ourselves · 6 themselves · 7 each other · 8 myself<br>10: 1 to · 2 for · 3 about · 4 from · 5 at · 6 with</p></div>
   </div>
   <div>
    <div class="k"><h3>11 · Say it better (2 points each)</h3><p>1 I talk to myself. · 2 I was thinking out loud. / I was thinking aloud. · 3 I said to myself, "Don't worry." / I told myself not to worry. · 4 Come on, you can do it! / Come on, you've got this! · 5 I practise speaking on my own.<br><i>Five ways:</i> 1 c · 2 a · 3 e · 4 b · 5 d · <i>Be your own friend, e.g.:</i> "Ali, you've learned so much already." · "Ali, you've prepared. You're ready."</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Word search (1 point per word)</h3><p>{WS_KEY}<br><b>Secret:</b> The person you talk to most every day is you.</p></div>{W.key_svg(ws, 36)}</div>
    <div class="k"><h3>13 · The coach story · 14 · Your turn</h3><p>1 ⚽ local team · 2 😬 shaking · 3 😰 "let everyone down" · 4 🧓 Mr Davies · 5 🗣️ three times · 6 😊 enjoyed the game<br><i>Think about it:</i> before exams, job interviews, his brother's wedding speech, the first episode of the podcast.<br>14: your own answers – 2 points per good sentence.</p></div>
    <div class="k"><h3>Your score</h3><p>90–100 🏆 <b>You've got this!</b> · 70–89 ✨ <b>Great pep talk</b> · 50–69 🎭 <b>Still rehearsing</b> · 0–49 🫘 <b>Lost in the lentils – listen again!</b></p></div>
   </div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy every week. And remember: the person you talk to most is you – so make it a kind conversation! 💜<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
    <img class="char" src="img/f/30-duo-waving-night.jpg" style="width:40mm">
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
