"""Writes template.html for the time-flies worksheet (Podcast 57).
CSS design system copied from build-a-habit; crossword from cw.json (see _source/tools/crossword.py)."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import crossword as X

src = (HERE.parent / "build-a-habit" / "template.html").read_text()
head = src[:src.index("</style>")].replace("Build a Habit Worksheet", "Time Flies Worksheet")
cw = json.loads((HERE / "cw.json").read_text())
X.check(cw)
spec = json.loads((HERE / "cw_spec.json").read_text())
CLUES = {w.upper(): c for w, c in spec["words"]}
ACROSS, DOWN = X.clues_html(cw, CLUES)

EXTRA = """
/* ---- new in time-flies ---- */
.graphs{display:grid;grid-template-columns:repeat(3,1fr);gap:2.6mm}
.graph{background:#fff;border:1.3px solid var(--line);border-radius:3.4mm;padding:2mm 2.4mm;text-align:center}
.graph .gl{display:inline-flex;width:6mm;height:6mm;border-radius:50%;border:1.3px solid var(--night);align-items:center;justify-content:center;font-weight:800;color:var(--night);font-size:9pt;margin-bottom:1mm}
.gq{display:grid;grid-template-columns:1fr auto;gap:1.4mm 3mm;font-size:9.2pt;align-items:center}
.gq .bx{display:inline-block;width:10mm;height:6.4mm;border:1.4px solid var(--night);border-radius:1.4mm;background:var(--lav)}
.clock{display:inline-flex;align-items:center;gap:1.2mm;padding:.5mm 2.2mm .5mm 1mm;border-radius:10mm;font-size:7.6pt;font-weight:700;white-space:nowrap}
.clock.now{background:var(--night);color:#F8E3C4}
.clock.back{background:#FBE1D6;color:var(--peach-d);border:1.2px solid #EBB49C}
.clock .box{width:4.2mm;height:4.2mm;border-radius:1mm;border-width:1.2px}
.clock.now .box{border-color:#F8E3C4;background:transparent}
.sorter{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:2.4mm}
.sorter .col{border-radius:4mm;padding:2.6mm 3mm;text-align:center}
.sorter .col .h{font-weight:800;font-size:11pt;letter-spacing:.4pt}
.sorter .col .s{font-size:7.8pt;margin-bottom:2mm}
.sorter .slots{display:flex;justify-content:center;gap:2mm}
.sorter .fast{background:#FDE3D6;color:#B5401C;border:1.3px solid #F2B39A}
.sorter .slow{background:#DCEFF3;color:#1F5F70;border:1.3px solid #A9D3DD}
.timeline{display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm}
.timeline div{border-radius:3mm;padding:2.2mm 2.8mm;font-size:8.4pt;line-height:1.4}
.timeline b.h{display:block;font-size:10pt;margin-bottom:.4mm}
.cw{border-collapse:separate;border-spacing:.7mm;margin:0 auto;width:auto;table-layout:fixed}
.cw td{width:var(--cell);min-width:var(--cell);max-width:var(--cell);height:var(--cell);padding:0;position:relative;box-sizing:border-box}
.cw td.o{background:#fff;border:1.4px solid var(--night);border-radius:1.2mm}
.cw td.x{border:none;background:transparent}
.cw .cn{position:absolute;top:.15mm;left:.45mm;font-size:5.4pt;font-weight:700;color:var(--mauve);line-height:1}
.cw .cl{display:flex;height:100%;align-items:center;justify-content:center;font-weight:700;font-size:8.6pt;color:var(--night)}
.cwk{border-spacing:.35mm}
.cwk td.o{border-width:.9px;border-radius:.6mm}
.cwk .cn{font-size:3.6pt;top:.1mm;left:.25mm}
.cwk .cl{font-size:6.2pt}
.cclues{font-size:8.5pt;line-height:1.36}
.cclues h4{margin:0 0 1mm;font-size:9.4pt;color:var(--night)}
.cclues .card > div{display:flex;gap:1.6mm;align-items:baseline;margin-bottom:1mm}
.cclues .n{font-weight:800;color:var(--mauve);width:4.4mm;flex:none}
.cclues .len{color:var(--muted);font-size:7.6pt}
.slips{display:grid;grid-template-columns:repeat(4,1fr);gap:2.2mm}
.slip{border:1.4px dashed var(--mauve);border-radius:2.6mm;padding:1.8mm 2.2mm;background:#FFFCF6;font-size:7.8pt;color:var(--mauve-d);min-height:15mm;display:flex;flex-direction:column;justify-content:space-between}
.predict-chips span{font-size:8.2pt}
.slip .ln{border-bottom:1px solid #D9CCE6;height:4.2mm}
"""

def foot(n): return "{{FOOT%d}}" % n

def graph(kind):
    # x: age 14 → 94 ; y: "feels faster" ↑
    W, H, L, B, T, R = 120, 70, 16, 56, 8, 112
    if kind == "flat":
        pts = f"{L},{(T + B) / 2 + 6} {R},{(T + B) / 2 + 6}"
    elif kind == "rise":
        pts = f"{L},{B - 4} {R},{T + 2}"
    else:  # rise then flat at 50
        x50 = L + (R - L) * (50 - 14) / 80
        pts = f"{L},{B - 4} {x50:.1f},{T + 8} {R},{T + 8}"
    x50 = L + (R - L) * (50 - 14) / 80
    return (f'<svg viewBox="0 0 {W} {H + 10}" style="width:100%;height:27mm;display:block">'
            f'<line x1="{L}" y1="{B}" x2="{R + 2}" y2="{B}" stroke="#61647E" stroke-width="1"/>'
            f'<line x1="{L}" y1="{B}" x2="{L}" y2="{T - 2}" stroke="#61647E" stroke-width="1"/>'
            f'<polyline points="{pts}" fill="none" stroke="#6E5D8C" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text x="{L}" y="{B + 9}" font-size="7" text-anchor="middle" fill="#61647E" font-family="Poppins">14</text>'
            f'<text x="{x50:.1f}" y="{B + 9}" font-size="7" text-anchor="middle" fill="#61647E" font-family="Poppins">50</text>'
            f'<text x="{R}" y="{B + 9}" font-size="7" text-anchor="middle" fill="#61647E" font-family="Poppins">94</text>'
            f'<text x="{(L + R) / 2}" y="{B + 18}" font-size="6.6" text-anchor="middle" fill="#61647E" font-family="Poppins">age</text>'
            f'<text x="6" y="{(T + B) / 2}" font-size="6.4" text-anchor="middle" fill="#61647E" font-family="Poppins" transform="rotate(-90 6 {(T + B) / 2})">feels faster →</text>'
            f'</svg>')

def chat(rows):
    out = []
    for who, img, text in rows:
        side = "l" if who == "LUCY" else "j"
        out.append(f'    <div class="msg {side}"><div class="ava"><img src="img/f/{img}-lav.jpg"></div>'
                   f'<div class="b"><span class="who">{who}</span>{text}</div></div>')
    return "\n".join(out)

def gap(n): return f'<span class="gap">{n}</span>'

CHAT = chat([
 ("LUCY", "32-lucy-coffee-chat-right", "Jack! Finally! I was starting to think you'd forgotten."),
 ("JACK", "16-jack-surprised-left", f"Sorry, sorry! I lost {gap(1)} of time. Wow, it's so good to see you. How long has it been?"),
 ("LUCY", "09-lucy-talking-right", "Almost a year, can you believe it? The last time we met was at the end of last summer."),
 ("JACK", "13-jack-talking-left", f"No way. It feels like only {gap(2)}. This year has {gap(3)} by."),
 ("LUCY", "12-lucy-laughing-right", f"Tell me about it. I {gap(4)}, and suddenly it's October."),
 ("JACK", "14-jack-listening-left", f"So what have you been {gap(5)} to?"),
 ("LUCY", "11-lucy-asking-right", f"Well, actually, I've been doing something new every month. Last month I took a pottery class. It was a disaster, but I had the time of my <span style='white-space:nowrap'>{gap(6)}.</span>"),
 ("JACK", "15-jack-shrug-left", f"That sounds amazing. My year's been a bit of a {gap(7)}. Work, home, work, home."),
 ("LUCY", "10-lucy-listening-right", "Then let's change that. Are you free next Saturday? There's a market in a town I've never visited."),
 ("JACK", "13-jack-talking-left", f"You know what? I'll make time for it. Count me {gap(8)}."),
 ("LUCY", "32-lucy-coffee-chat-right", "Perfect. I'll send you the details tonight."),
])

PHRASES = [("a", "The weekend flew by."), ("b", "I waited ages for the bus."), ("c", "This queue is taking forever."),
           ("d", "Time flies!"), ("e", "We'll be there in no time."), ("f", "The last hour of work dragged."),
           ("g", "I haven't seen you for ages!"), ("h", "My year's been a bit of a blur.")]
PHR = "".join(f'<div><b>{l}</b>{t}</div>' for l, t in PHRASES)

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
      <h1>Why Time Goes Faster as We Get Older</h1>
      <p style="margin:2.4mm 0 0;font-size:9.6pt;color:var(--muted)">Why our years seem to disappear, what really makes time feel longer, lots of useful time expressions – and Lucy's mum's "firsts jar".</p>
      <div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;font-size:9.3pt;align-items:end">
        <b style="color:var(--night)">Name:</b><span class="blank xl"></span>
        <b style="color:var(--night)">Date:</b><span class="blank xl"></span>
        <b style="color:var(--night)">My score:</b><span><span class="blank s"></span> / 100 ⭐</span>
      </div>
    </div>
    <div style="background:var(--lav);border-radius:6mm;height:60mm;position:relative;overflow:hidden;border:1px solid var(--lav2)">
      <div style="position:absolute;z-index:2;top:3.4mm;left:4mm;background:#fff;border-radius:4mm;padding:1mm 3mm;font-size:8.6pt;font-weight:700;color:var(--night);box-shadow:0 1px 0 var(--lav2)">Wait… it's October already?! 😱</div>
      <img class="char" src="img/f/30-duo-waving-lav.jpg" style="position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:76mm">
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">★</span>How to use this worksheet</h2>
    <div class="steps" style="margin-top:2.4mm">
      <div class="step"><div class="h">1 · Before you listen 🧠</div><div class="s">Do the warm-up and learn the key words. Questions with 🧠 can be answered before listening.</div></div>
      <div class="step"><div class="h">2 · While you listen 🎧</div><div class="s">Answer the 🎧 questions. The ⏱ times show where to find each part of the video.</div></div>
      <div class="step"><div class="h">3 · After you listen 💬</div><div class="s">Solve the crossword, start your own firsts jar and share a "first" in the comments!</div></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">0</span>Warm-up: My firsts this year <span class="tag fun">fun · no points</span></h2>
    <p class="instr">Tick everything you did <b>for the first time</b> this year. Then count your ticks!</p>
    <div style="display:grid;grid-template-columns:1.3fr .7fr;gap:4mm;align-items:stretch">
      <div class="card white" style="display:flex;flex-direction:column;gap:2mm;justify-content:center">
        <div class="conf" style="grid-template-columns:1fr 1fr;justify-content:stretch">
          <div><span class="box sm"></span>🍣 tried a new food</div>
          <div><span class="box sm"></span>🗺️ visited a new place</div>
          <div><span class="box sm"></span>🎨 learned a new skill</div>
          <div><span class="box sm"></span>🤝 made a new friend</div>
          <div><span class="box sm"></span>🎬 watched a film in English</div>
          <div><span class="box sm"></span>🚶 took a new way home</div>
        </div>
        <div style="font-size:9pt"><b style="color:var(--night)">My firsts this year:</b> <span class="blank s"></span></div>
        <div style="border-top:1px dashed var(--lav2);padding-top:2mm;font-size:8.9pt"><b style="color:var(--night)">Guess!</b> In a study of 499 people, did older people feel that the last <b>week</b> passed faster than young people did?</div>
        <div style="display:flex;gap:4mm;font-size:8.9pt;flex-wrap:wrap"><span><span class="circ">a</span> yes, much faster</span><span><span class="circ">b</span> no – about the same</span></div>
        <div class="hint">🎧 Check your guess at ⏱ 2:19</div>
      </div>
      <div class="card peach" style="display:flex;flex-direction:column;align-items:center;gap:1.4mm;padding:2.6mm 3mm 0;justify-content:space-between">
        <div style="background:#fff;border-radius:4mm;padding:2mm 2.8mm;font-size:8.5pt;border:1.2px solid #F4D2C2;line-height:1.4"><b style="color:var(--night)">Jack:</b> "Where did this year go? It feels like it was January about five minutes ago!" 🗓️</div>
        <img class="char" src="img/f/15-jack-shrug-left-peach.jpg" style="width:30mm">
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">💬</span>Let's talk</h2>
    <p class="instr">Say your answers out loud – or write them in your notebook.</p>
    <div class="grid2" style="gap:3mm">
      <div class="card teal"><b>1.</b> Does time feel faster now than when you were a child?</div>
      <div class="card teal"><b>2.</b> What's your most vivid memory from childhood?</div>
      <div class="card teal"><b>3.</b> What did you do last Tuesday? Can you remember? 😅</div>
      <div class="card teal"><b>4.</b> What's something you did for the first time this year?</div>
    </div>
  </div>
  {foot(1)}
</section>

<!-- ================= PAGE 2 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm">
    <h2><span class="num">1</span>Key words <span class="tag">vocabulary</span><span class="tag pts">10 points</span></h2>
    <p class="instr">Match each word or phrase (1–10) to its meaning (a–j). Write the letter in the box. 🧠 Check in the Word Tour at ⏱ 14:10</p>
    <div class="grid2" style="gap:5mm;align-items:start">
      <table class="match">
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">1.</b> to fly by</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">2.</b> to drag</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">3.</b> a routine</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">4.</b> novelty</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">5.</b> to look back</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">6.</b> vivid</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">7.</b> a paradox</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">8.</b> to reminisce</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">9.</b> to lose track of time</td></tr>
        <tr><td class="ans"><span class="box"></span></td><td><b style="color:var(--night)">10.</b> a blur</td></tr>
      </table>
      <div class="card" style="font-size:9.1pt;line-height:1.62">
        <b>a)</b> to seem to pass very slowly, usually because you're bored<br>
        <b>b)</b> very clear, bright or detailed<br>
        <b>c)</b> the quality of being new or unusual<br>
        <b>d)</b> to think about something in the past<br>
        <b>e)</b> something that seems impossible, because two opposite things are both true<br>
        <b>f)</b> your usual way of doing things, in the usual order<br>
        <b>g)</b> to pass very quickly<br>
        <b>h)</b> to remember and talk about the past, usually with pleasure<br>
        <b>i)</b> a time you can't remember clearly because it went so fast<br>
        <b>j)</b> to not notice how much time has passed
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/19-lucy-glasses-book-w.jpg" style="width:24mm;flex:none">
      <div class="txt"><b>Pronunciation corner 🔊</b> <b style="color:var(--peach-d)">NOV</b>-el-ty · <b style="color:var(--peach-d)">VIV</b>-id · <b style="color:var(--peach-d)">PAR</b>-a-dox · rou-<b style="color:var(--peach-d)">TINE</b> · rem-i-<b style="color:var(--peach-d)">NISCE</b>. And the irregular verb: fly → <b>flew</b> → <b>flown</b>. Say it out loud: <i>"Looking back, that year flew by!"</i></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">2</span>First listen: the big idea <span class="tag">listening</span><span class="tag pts">2 points</span></h2>
    <p class="instr">Watch the whole episode once without stopping. Which sentence is the <b>main message</b>? 🎧</p>
    <div class="card white">
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">a</span>Time really moves faster for older people, and nothing can change it.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">b</span>Years feel short when they leave few new memories – so small new experiences make time feel fuller.</div>
      <div class="opt" style="font-size:9.6pt;margin:1.2mm 0"><span class="c">c</span>The best way to slow down time is to have the same routine every day.</div>
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
      <div class="chips predict-chips" style="margin-top:2mm;justify-content:center;gap:1.4mm"><span>supermarket</span><span>dentist</span><span>mountains</span><span>pasta</span><span>bakery</span><span>piano</span><span>crossword</span><span>pottery</span></div>
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
    <div class="mcq"><div class="qq">1. If time "drags", it feels…</div><div class="opt"><span class="c">a</span>very fast</div><div class="opt"><span class="c">b</span>very slow</div><div class="opt"><span class="c">c</span>very exciting</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">2. "I moved here two years ______."</div><div class="opt"><span class="c">a</span>before</div><div class="opt"><span class="c">b</span>since</div><div class="opt"><span class="c">c</span>ago</div><div class="hint">🧠 Grammar you know</div></div>
    <div class="mcq"><div class="qq">3. "Tell me about it!" usually means…</div><div class="opt"><span class="c">a</span>I completely agree</div><div class="opt"><span class="c">b</span>please tell me more</div><div class="opt"><span class="c">c</span>I don't believe you</div><div class="hint">🧠 Tricky – think about it!</div></div>
    <div class="mcq"><div class="qq">4. A "routine" is…</div><div class="opt"><span class="c">a</span>a long holiday</div><div class="opt"><span class="c">b</span>something you do for the first time</div><div class="opt"><span class="c">c</span>your usual way of doing things</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq"><div class="qq">5. A "vivid" memory is…</div><div class="opt"><span class="c">a</span>very clear and detailed</div><div class="opt"><span class="c">b</span>very old</div><div class="opt"><span class="c">c</span>very boring</div><div class="hint">🧠 Look at Exercise 1</div></div>
    <div class="mcq" style="background:var(--sage);border-color:#BFD7C8;display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🎉</span><span style="font-size:9.1pt"><b style="color:var(--night)">How many did you know?</b><br>Now press play and test your ears!</span></div>
  </div>
  <div class="small" style="margin:3.4mm 0 1.6mm 10.8mm;font-weight:700;color:var(--peach-d)">🎧 LISTEN AND FIND OUT</div>
  <div class="mc">
    <div class="mcq"><div class="qq">6. How many people took part in the Munich study?</div><div class="opt"><span class="c">a</span>99</div><div class="opt"><span class="c">b</span>499</div><div class="opt"><span class="c">c</span>4,900</div><div class="hint">🎧 ⏱ 2:19</div></div>
    <div class="mcq"><div class="qq">7. For the last hour or week, younger and older people…</div><div class="opt"><span class="c">a</span>felt very different speeds</div><div class="opt"><span class="c">b</span>felt about the same speed</div><div class="opt"><span class="c">c</span>couldn't answer</div><div class="hint">🎧 ⏱ 2:19</div></div>
    <div class="mcq"><div class="qq">8. When we look back, our brain measures time by counting…</div><div class="opt"><span class="c">a</span>birthdays</div><div class="opt"><span class="c">b</span>days on the calendar</div><div class="opt"><span class="c">c</span>memories</div><div class="hint">🎧 ⏱ 4:10</div></div>
    <div class="mcq"><div class="qq">9. On his new way to work, Jack saw a dog wearing…</div><div class="opt"><span class="c">a</span>a little scarf</div><div class="opt"><span class="c">b</span>sunglasses</div><div class="opt"><span class="c">c</span>a hat</div><div class="hint">🎧 ⏱ 8:29</div></div>
    <div class="mcq"><div class="qq">10. After the first year, how many papers were in the jar?</div><div class="opt"><span class="c">a</span>28</div><div class="opt"><span class="c">b</span>51</div><div class="opt"><span class="c">c</span>43</div><div class="hint">🎧 ⏱ 19:17</div></div>
    <div class="mcq" style="background:var(--lav);border-color:var(--lav2);display:flex;align-items:center;gap:3mm"><span style="font-size:18pt">🧩</span><span style="font-size:9.1pt"><b style="color:var(--night)">Fun fact:</b> The people in the Munich study were aged from <b>14 to 94</b> – that's 80 years between the youngest and the oldest!</span></div>
  </div>
  {foot(3)}
</section>

<!-- ================= PAGE 4 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">4</span>Read the research 📊 <span class="tag">new! graphs</span><span class="tag pts">4 points</span></h2>
      <p class="instr" style="margin-bottom:0">In the Munich study, people of different ages said how fast time felt. Listen at ⏱ 2:19, then choose the right graph (2 points each).</p>
    </div>
    <img class="char" src="img/f/20-jack-glasses-laptop-w.jpg" style="width:22mm;flex:none;margin-top:-3mm">
  </div>
  <div class="graphs" style="margin-top:2.4mm">
    <div class="graph"><span class="gl">a</span>{graph("flat")}</div>
    <div class="graph"><span class="gl">b</span>{graph("rise")}</div>
    <div class="graph"><span class="gl">c</span>{graph("bend")}</div>
  </div>
  <div class="card white gq" style="margin-top:2mm;padding:2mm 4mm">
    <span><b>1.</b> Which graph shows how fast <b>the last week</b> felt?</span><span class="bx"></span>
    <span><b>2.</b> Which graph shows how fast <b>the last ten years</b> felt?</span><span class="bx"></span>
    <span class="small"><b>Bonus</b> (no points): the "maths theory" says a year is a smaller part of your life when you're older. Which graph does it predict for <b>the last week</b>? ⏱ 7:09</span><span class="bx" style="background:#fff"></span>
  </div>

  <div class="sec">
    <h2><span class="num">5</span>True or false? <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Listen and circle <b>T</b> (true) or <b>F</b> (false). The ⏱ times help you find the answer.</p>
    <table class="tf">
      <tr><td class="n">1</td><td>Last week, Lucy saw Christmas decorations in a supermarket.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 0:05</td></tr>
      <tr><td class="n">2</td><td>In the Munich study, the last ten years felt faster and faster after the age of 50.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 2:19</td></tr>
      <tr><td class="n">3</td><td>In the study from Israel, routine made time feel <b>longer</b> in memory.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 4:48</td></tr>
      <tr><td class="n">4</td><td>We remember a lot from about the ages of 15 to 25.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 6:08</td></tr>
      <tr><td class="n">5</td><td>Claudia Hammond thinks the "maths theory" explains time very well.</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 7:09</td></tr>
      <tr><td class="n">6</td><td>Lucy says learning English is "a machine for making new memories".</td><td class="ck"><span class="circ">T</span> <span class="circ">F</span></td><td class="tm">⏱ 8:29</td></tr>
    </table>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">6</span>Two clocks in your head <span class="tag">think</span><span class="tag pts">4 points</span></h2>
        <p class="instr" style="margin-bottom:0">Is the person measuring time <b>while it's happening</b>, or <b>looking back</b>? Tick one. ⏱ 3:35</p>
      </div>
      <img class="char" src="img/f/28-lucy-travel-w.jpg" style="width:19mm;flex:none">
    </div>
    <div class="grid2" style="margin-top:2.2mm;gap:2.4mm">
      <div class="sit"><div class="t" style="min-height:0"><b>1.</b> "This meeting is taking forever!" 😩</div><div class="ch" style="gap:2mm"><span class="clock now"><span class="box"></span>⏱ WHILE IT'S HAPPENING</span><span class="clock back"><span class="box"></span>🔙 LOOKING BACK</span></div></div>
      <div class="sit"><div class="t" style="min-height:0"><b>2.</b> "How long ago was that holiday?" 🤔</div><div class="ch" style="gap:2mm"><span class="clock now"><span class="box"></span>⏱ WHILE IT'S HAPPENING</span><span class="clock back"><span class="box"></span>🔙 LOOKING BACK</span></div></div>
      <div class="sit"><div class="t" style="min-height:0"><b>3.</b> "When I think about the mountains now, it feels like a month." 🏔️</div><div class="ch" style="gap:2mm"><span class="clock now"><span class="box"></span>⏱ WHILE IT'S HAPPENING</span><span class="clock back"><span class="box"></span>🔙 LOOKING BACK</span></div></div>
      <div class="sit"><div class="t" style="min-height:0"><b>4.</b> "This holiday is flying by – it's Friday already!" 🏖️</div><div class="ch" style="gap:2mm"><span class="clock now"><span class="box"></span>⏱ WHILE IT'S HAPPENING</span><span class="clock back"><span class="box"></span>🔙 LOOKING BACK</span></div></div>
    </div>
    <div class="small" style="margin:1.8mm 0 0 1mm">🏖️ <b>The holiday paradox:</b> a great holiday flies by while you're there – but when you look back, it feels long, because it's full of new memories.</div>
  </div>
  {foot(4)}
</section>

<!-- ================= PAGE 5 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">7</span>"How long has it been?" <span class="tag">listening</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Two old friends meet for coffee after a long time. Listen at ⏱ 11:50 and write <b>one word</b> in each gap (1–8). Then answer A and B. The breakdown at ⏱ 12:56 can help.</p>
    </div>
    <img class="char" src="img/f/23-jack-hot-chocolate-w.jpg" style="width:24mm;flex:none;margin-top:-3mm">
  </div>
  <div class="chat" style="margin-top:2.6mm;gap:1.3mm">
{CHAT}
  </div>
  <div class="grid2" style="margin-top:2.8mm;gap:3mm">
    <div class="card" style="padding:2.4mm 4mm"><b style="color:var(--night)">A.</b> Which phrase means <b>"I completely agree"</b>? Careful – it's a trick!<div class="lines"></div></div>
    <div class="card" style="padding:2.4mm 4mm"><b style="color:var(--night)">B.</b> Which phrase means <b>"Yes, I'll join you"</b>?<div class="lines"></div></div>
  </div>
  <div class="small" style="margin-top:2mm;text-align:center">🎭 <b>Say it out loud!</b> Play both parts – and talk about something <b>you</b> did for the first time this month.</div>
  {foot(5)}
</section>

<!-- ================= PAGE 6 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">8</span>Fast or slow? <span class="tag">time expressions</span><span class="tag pts">8 points</span></h2>
      <p class="instr" style="margin-bottom:0">Does each sentence describe time going <b>fast</b> ⚡ or time feeling <b>slow / long</b> 🐢? Write the letters (a–h) in the right box. ⏱ 14:10</p>
    </div>
    <img class="char" src="img/f/26-jack-sleepy-morning-w.jpg" style="width:20mm;flex:none;margin-top:-3mm">
  </div>
  <div class="card white bank" style="margin-top:2.4mm">{PHR}</div>
  <div class="sorter">
    <div class="col fast"><div class="h">⚡ FAST</div><div class="s">time passes quickly</div><div class="slots"><span class="box"></span><span class="box"></span><span class="box"></span><span class="box"></span></div></div>
    <div class="col slow"><div class="h">🐢 SLOW / LONG</div><div class="s">time passes slowly, or a long time</div><div class="slots"><span class="box"></span><span class="box"></span><span class="box"></span><span class="box"></span></div></div>
  </div>
  <div class="bub" style="margin-top:2.6mm">
    <img class="char" src="img/f/03-lucy-did-you-know-w.jpg" style="width:18mm;flex:none">
    <div class="txt"><b>Did you know?</b> <b>"Ages"</b> is informal English for <b>a very long time</b>: <i>"I haven't seen you for ages!"</i> And <b>"in no time"</b> means <b>very quickly</b>: <i>"We'll be there in no time."</i></div>
  </div>

  <div class="sec">
    <h2><span class="num">9</span>What do we do with time? <span class="tag">new! collocations</span><span class="tag pts">6 points</span></h2>
    <p class="instr">Complete each sentence with a verb from the box. Change the form if you need to.</p>
    <div class="chips" style="margin:0 0 2mm 10.8mm"><span>have</span><span>kill</span><span>lose</span><span>make</span><span>spend</span><span>waste</span></div>
    <table class="coll" style="margin-left:2mm">
      <tr><td>1. I always <span class="blank"></span> track of time when I'm reading a good book.</td></tr>
      <tr><td>2. Yesterday I <span class="blank"></span> time at the airport by doing a crossword.</td></tr>
      <tr><td>3. I'm very busy this week, but I'll <span class="blank"></span> time for your party.</td></tr>
      <tr><td>4. Last Sunday we <span class="blank"></span> the whole afternoon walking in the park.</td></tr>
      <tr><td>5. Don't <span class="blank"></span> time worrying about small things!</td></tr>
      <tr><td>6. The pottery class was a disaster, but Lucy <span class="blank"></span> the time of her life.</td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/02-jack-lightbulb-idea-w.jpg" style="width:17mm;flex:none">
      <div class="txt"><b>Jack's tip:</b> We <b>have</b> a good time – we don't "spend" a good time. But we <b>spend</b> time doing something: <i>"I spent the evening reading."</i></div>
    </div>
  </div>
  {foot(6)}
</section>

<!-- ================= PAGE 7 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">10</span>for · since · ago <span class="tag">new! grammar</span><span class="tag pts">6 points</span></h2>
      <p class="instr" style="margin-bottom:0">Three little words, three different jobs. ⏱ 17:02</p>
    </div>
    <img class="char" src="img/f/04-jack-thinking-w.jpg" style="width:19mm;flex:none;margin-top:-3mm">
  </div>
  <div class="timeline" style="margin-top:2.2mm">
    <div style="background:var(--lav)"><b class="h" style="color:var(--mauve-d)">for + a period</b>how long?<br><i>"for an hour", "for ages", "for two years"</i></div>
    <div style="background:var(--sage)"><b class="h" style="color:var(--sage-d)">since + a starting point</b>from when?<br><i>"since Monday", "since 2019", "since I was a child"</i></div>
    <div style="background:var(--peach-l)"><b class="h" style="color:var(--peach-d)">period + ago</b>how far back in the past?<br><i>"two years ago" – <b>ago</b> comes <b>after</b> the time!</i></div>
  </div>
  <div class="card white" style="margin-top:2.6mm;font-size:9.3pt;line-height:2.05">
    1. I moved to London two years <span class="blank s"></span>.<br>
    2. I've been waiting for you <span class="blank s"></span> an hour!<br>
    3. Lucy's mum has kept a firsts jar every year <span class="blank s"></span> she turned sixty.<br>
    4. We haven't seen each other <span class="blank s"></span> ages!<br>
    5. Jack started walking a new way to work a month <span class="blank s"></span>.<br>
    6. I've known my best friend <span class="blank s"></span> 2015.
  </div>
  <div class="small" style="margin:1.6mm 0 0 1mm">💡 With <b>for</b> and <b>since</b>, we often use the present perfect: <i>"I've lived here for two years."</i> With <b>ago</b>, we use the past simple: <i>"I moved here two years ago."</i></div>

  <div class="sec">
    <h2><span class="num">11</span>Say it better <span class="tag">common mistakes</span><span class="tag pts">10 points</span></h2>
    <p class="instr">These sentences sound unnatural. Write a more natural version (2 points each). ⏱ 17:02</p>
    <table style="font-size:9.4pt">
      <tr><td style="width:49%;padding:1.7mm 0">😐 1. "The time is passing very fast."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 2. "I spent a very good time at the party."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 3. "I have no time for to study."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 4. "Every day is same, it is boring."</td><td>😊 <span class="blank l"></span></td></tr>
      <tr><td style="padding:1.7mm 0">😐 5. "What are you doing recently?" <span class="small">(to an old friend)</span></td><td>😊 <span class="blank l"></span></td></tr>
    </table>
    <div class="bub" style="margin-top:2.4mm">
      <img class="char" src="img/f/01-lucy-thumbs-up-w.jpg" style="width:18mm;flex:none">
      <div class="txt"><b>Lucy's tip:</b> <b>"the same"</b> always needs <b>"the"</b>: <i>"Every day feels the same."</i> And we usually say <b>"Time flies!"</b> – not "the time flies".</div>
    </div>
  </div>
  <div class="sec">
    <div class="card teal" style="padding:2.8mm 4.6mm">
      <b style="color:var(--night)">🪞 Now talk about you!</b> <span class="small">(no points)</span> Finish the sentences with <b>for</b>, <b>since</b> or <b>ago</b> – then say them out loud.
      <div style="font-size:9.3pt;line-height:2.2;margin-top:1mm">
        I've lived in my home <span class="blank l"></span>.<br>
        I started learning English <span class="blank l"></span>.<br>
        I haven't been on holiday <span class="blank l"></span>.
      </div>
    </div>
  </div>
  {foot(7)}
</section>

<!-- ================= PAGE 8 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-start;gap:4mm">
    <div>
      <h2><span class="num">12</span>Time crossword 🧩 <span class="tag">new! puzzle</span><span class="tag pts">10 points</span></h2>
      <p class="instr" style="margin-bottom:0">Read the clues and write the words in the grid (1 point each). The number in brackets is the number of letters. Letters that cross help you!</p>
    </div>
    <img class="char" src="img/f/05-lucy-writing-w.jpg" style="width:19mm;flex:none;margin-top:-3mm">
  </div>
  <div style="margin-top:2.6mm">{X.grid_html(cw, 7.2)}</div>
  <div class="grid2 cclues" style="margin-top:2.6mm;gap:4mm">
    <div class="card white" style="padding:2.4mm 3.4mm"><h4>➡️ Across</h4>{ACROSS}</div>
    <div class="card white" style="padding:2.4mm 3.4mm"><h4>⬇️ Down</h4>{DOWN}</div>
  </div>

  <div class="sec">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
      <div>
        <h2><span class="num">13</span>Lucy's mum's firsts jar <span class="tag">listening</span><span class="tag pts">6 points</span></h2>
        <p class="instr" style="margin-bottom:0">Listen at ⏱ 19:17. Put the events in the right order. Write 1–6 in the boxes.</p>
      </div>
      <img class="char" src="img/f/17-lucy-winter-tea-w.jpg" style="width:18mm;flex:none">
    </div>
    <div class="story" style="margin-top:2mm">
      <div class="ev"><span class="box"></span><span class="e">🍯</span><span>On New Year's Day, she put an empty glass jar on the kitchen shelf.</span></div>
      <div class="ev"><span class="box"></span><span class="e">📖</span><span>The next New Year's Day, she read all the papers to the family.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🎂</span><span>Lucy's mum turned sixty and said the years were going so fast.</span></div>
      <div class="ev"><span class="box"></span><span class="e">🌟</span><span>This year, Lucy started her own jar.</span></div>
      <div class="ev"><span class="box"></span><span class="e">✍️</span><span>Every time she did something for the first time, she wrote it down.</span></div>
      <div class="ev"><span class="box"></span><span class="e">💬</span><span>She said, "That was the longest year I've had in a very long time."</span></div>
    </div>
    <div class="card teal" style="margin-top:2.4mm;padding:2.4mm 4mm"><b style="color:var(--night)">Think about it 💭</b> <span class="small">(no points)</span> Why did that year feel so long – in the best way?<div class="lines"></div></div>
  </div>
  {foot(8)}
</section>

<!-- ================= PAGE 9 ================= -->
<section class="page">
  <div class="sec" style="margin-top:3mm;display:flex;justify-content:space-between;align-items:flex-end;gap:4mm">
    <div>
      <h2><span class="num">14</span>Your turn: your firsts <span class="tag">writing</span><span class="tag pts">8 points</span></h2>
      <p class="instr" style="margin-bottom:0">2 points for each good sentence.</p>
    </div>
    <img class="char" src="img/f/22-lucy-eating-apple-w.jpg" style="width:18mm;flex:none">
  </div>
  <div class="grid2" style="margin-top:2.2mm;gap:3mm;align-items:stretch">
    <div class="card" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">A. This week, for the first time, I… 🌟</b>
      <div class="small" style="margin-top:1mm">Write two sentences in the <b>past simple</b>. <i>e.g. "This week, for the first time, I cooked a Thai curry."</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
    <div class="card peach" style="padding:2.6mm 4mm">
      <b style="color:var(--night);font-size:9.2pt">B. It's the first time I've… 🎉</b>
      <div class="small" style="margin-top:1mm">Imagine you're doing something new <b>right now</b>. Use <b>It's the first time I've + past participle</b>. <i>e.g. "It's the first time I've swum in the sea in October!"</i></div>
      <div class="lines"></div><div class="lines"></div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">🍯</span>Start your own firsts jar <span class="tag fun">your mission</span></h2>
    <p class="instr">Cut out the slips. Every time you do something for the first time, write it – in English! – and put it in a jar. Open it on New Year's Day. ✂️</p>
    <div class="slips">
      <div class="slip">🌟 First time I…<span class="ln"></span><span class="ln"></span><span>Date: ______</span></div>
      <div class="slip">🌟 First time I…<span class="ln"></span><span class="ln"></span><span>Date: ______</span></div>
      <div class="slip">🌟 First time I…<span class="ln"></span><span class="ln"></span><span>Date: ______</span></div>
      <div class="slip">🌟 First time I…<span class="ln"></span><span class="ln"></span><span>Date: ______</span></div>
      <div class="slip">🌟 First time I…<span class="ln"></span><span class="ln"></span><span>Date: ______</span></div>
      <div class="slip">🌟 First time I…<span class="ln"></span><span class="ln"></span><span>Date: ______</span></div>
      <div class="slip">🌟 First time I…<span class="ln"></span><span class="ln"></span><span>Date: ______</span></div>
      <div class="slip">🌟 First time I…<span class="ln"></span><span class="ln"></span><span>Date: ______</span></div>
    </div>
    <div class="small" style="margin:1.6mm 0 0 1mm">💡 Ideas: a new street, a new food, a new café, a new word you actually used, your first film in English without subtitles…</div>
  </div>

  <div class="sec">
    <div class="pocket">
      <span class="sc">✂️ Cut out and keep in your pocket</span>
      <div class="pc">
        <div><b style="color:#B5401C">⚡ FAST</b>Time flies!<br>The weekend flew by.<br>We'll be there in no time.</div>
        <div><b style="color:#1F5F70">🐢 SLOW</b>It's taking forever.<br>The last hour dragged.<br>I haven't seen you for ages!</div>
        <div><b style="color:var(--mauve-d)">👋 CATCH UP</b>How long has it been?<br>What have you been up to?</div>
        <div><b style="color:var(--sage-d)">✅ AGREE</b>Tell me about it!<br>Count me in!</div>
      </div>
    </div>
  </div>

  <div class="sec">
    <h2><span class="num">✓</span>Can you do it now?</h2>
    <table class="cando" style="margin-top:1.4mm">
      <tr><th style="text-align:left">I can…</th><th>Not yet</th><th>Almost</th><th>Yes!</th></tr>
      <tr><td>explain why years seem to go faster when we look back.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use time expressions like fly by, drag and in no time.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>use for, since and ago correctly.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
      <tr><td>plan small new things to make my year fuller.</td><td class="f">😟</td><td class="f">🙂</td><td class="f">😄</td></tr>
    </table>
  </div>

  <div class="sec">
    <div class="bub">
      <img class="char" src="img/f/08-jack-waving-w.jpg" style="width:20mm;flex:none">
      <div class="txt"><b>Share it with us!</b> Tell us in the comments – start with <b>"This week, for the first time, I…"</b> And if you start your own jar, tell us how many firsts you've got! 💜</div>
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
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:2mm;margin-top:2.6mm">
    <div class="k"><h3>0 · Warm-up &amp; predict</h3><p>Guess: b – for short periods there was almost no difference between ages. · Predict: <b>piano</b> 🎹 isn't in the episode.</p></div>
    <div class="k"><h3>1 · Key words · 2 · The big idea</h3><p>1 g · 2 a · 3 f · 4 c · 5 d · 6 b · 7 e · 8 h · 9 j · 10 i<br>Big idea: b (2 points)</p></div>
    <div class="k"><h3>3 · Know it or hear it?</h3><p>1 b · 2 c · 3 a · 4 c · 5 a · 6 b · 7 b · 8 c · 9 a · 10 c</p></div>
    <div class="k"><h3>4 · Read the research (2 points each)</h3><p>1 a (flat – about the same for all ages) · 2 c (faster and faster until about 50, then the same)<br><i>Bonus:</i> b – but the real results don't match it!</p></div>
    <div class="k"><h3>5 · True or false?</h3><p>1 T · 2 F (after 50 it stayed about the same) · 3 F (shorter) · 4 T · 5 F (the memory explanation fits better) · 6 T</p></div>
    <div class="k"><h3>6 · Two clocks in your head</h3><p>1 while it's happening · 2 looking back · 3 looking back · 4 while it's happening</p></div>
    <div class="k"><h3>7 · "How long has it been?"</h3><p>1 track · 2 yesterday · 3 flown · 4 blinked · 5 up · 6 life · 7 blur · 8 in · A "Tell me about it." · B "Count me in."</p></div>
    <div class="k"><h3>8 · Fast or slow?</h3><p>⚡ FAST: a, d, e, h · 🐢 SLOW / LONG: b, c, f, g</p></div>
    <div class="k"><h3>9 · What do we do with time?</h3><p>1 lose · 2 killed · 3 make · 4 spent · 5 waste · 6 had</p></div>
    <div class="k"><h3>10 · for · since · ago</h3><p>1 ago · 2 for · 3 since · 4 for · 5 ago · 6 since</p></div>
    <div class="k"><h3>11 · Say it better (2 points each)</h3><p>1 Time flies! / Where has the time gone? · 2 I had a great time at the party. · 3 I don't have time to study. / I can't find the time to study. · 4 Every day feels the same. / I'm stuck in a bit of a routine. · 5 What have you been up to?</p></div>
    <div class="k" style="display:grid;grid-template-columns:1fr auto;gap:2.4mm;align-items:center"><div><h3>12 · Crossword</h3><p>{{CW_KEY}}</p></div>{{CW_GRID}}</div>
    <div class="k"><h3>13 · The firsts jar · 14 · Your turn</h3><p>1 🎂 turned sixty · 2 🍯 empty jar · 3 ✍️ wrote it down · 4 📖 read the papers · 5 💬 "the longest year" · 6 🌟 Lucy's own jar<br><i>Think about it:</i> 43 firsts = lots of new memories, so the year felt full.<br>14: your own answers – 2 points per good sentence.</p></div>
    <div class="k"><h3>Your score</h3><p>90–100 🏆 <b>Time master!</b> · 70–89 ⚡ <b>Flying by</b> · 50–69 🗓️ <b>Making the most of it</b> · 0–49 🐢 <b>Take your time – listen again!</b></p></div>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr auto;gap:4mm;align-items:center;margin-top:2.6mm;background:var(--night);border-radius:5mm;padding:3.2mm 4.6mm;color:#F8E3C4">
    <img src="img/qr.png" style="width:24mm;height:24mm;border-radius:2mm;background:#fff;padding:1mm">
    <div style="font-size:8.8pt;line-height:1.5"><b style="font-size:11pt;color:var(--peach)">Enjoyed this worksheet? 🎉</b><br>Scan to subscribe to <b>Daily Speak English</b> – new episodes with Jack and Lucy every week. Your next "first"?<br>More free worksheets: <b style="color:#fff">dailyspeakenglish.github.io/worksheets</b></div>
    <img class="char" src="img/f/29-duo-high-five-night.jpg" style="width:37mm">
  </div>
  {foot(10)}
</section>

</body>
</html>
"""
across = " · ".join(f'{e["num"]} {e["word"].lower()}' for e in sorted([e for e in cw["entries"] if e["dir"] == "A"], key=lambda e: e["num"]))
down = " · ".join(f'{e["num"]} {e["word"].lower()}' for e in sorted([e for e in cw["entries"] if e["dir"] == "D"], key=lambda e: e["num"]))
body = body.replace("{CW_KEY}", f"<b>Across:</b> {across}<br><b>Down:</b> {down}").replace(
    "{CW_GRID}", X.grid_html(cw, 3.6, solved=True, cls="cw cwk"))
html = head + EXTRA + "</style>\n</head>\n<body>\n" + body
(HERE / "template.html").write_text(html)
pts = [int(x) for x in re.findall(r'tag pts">(\d+) points', html)]
print("points", sum(pts), pts)
