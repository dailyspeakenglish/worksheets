"""Clue word search with a secret message – generator, checker and HTML/SVG renderer.

Rules it enforces (learned from the build-a-habit feedback):
  * words never share a cell (no crossings), so the answer key shows clean, separate lines;
  * every word appears exactly ONCE in the grid, in all 8 directions (no accidental duplicates);
  * the unused cells, read row by row from left to right, spell the secret message exactly;
  * directions are reader-friendly: → ↓ ↘ ↗ (never backwards);
  * at least one word in each direction; no two words start in the same cell, and words with the
    same first letter never start next to each other; at most `max_diag` diagonal words.

Usage (from the repo root):
  python3 _source/tools/wordsearch.py _source/<slug>/ws_spec.json
ws_spec.json: {"size": 11, "words": ["AUTOMATIC", ...], "message": "THE GRASS DOESN'T GROW BACK OVERNIGHT", "seed": 1}
Writes _source/<slug>/ws.json (grid + positions). Then, in Python:
  from wordsearch import grid_html, key_svg, message_slots
"""
import json, random, sys, pathlib

DIRS = [(0, 1), (1, 0), (1, 1), (-1, 1)]          # → ↓ ↘ ↗
ALL8 = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]


def letters(s):
    return "".join(ch for ch in s.upper() if ch.isalpha())


def count_occurrences(grid, word):
    n, hits = len(grid), 0
    for r in range(n):
        for c in range(n):
            for dr, dc in ALL8:
                ok = True
                for i, ch in enumerate(word):
                    rr, cc = r + dr * i, c + dc * i
                    if not (0 <= rr < n and 0 <= cc < n) or grid[rr][cc] != ch:
                        ok = False
                        break
                if ok:
                    hits += 1
    return hits // (2 if word == word[::-1] else 1)


def generate(size, words, message, seed=1, tries=400000, max_diag=4):
    """Depth-first search with random ordering. `tries` limits the number of placements tried."""
    msg = letters(message)
    words = [w.upper() for w in words]
    assert sum(map(len, words)) + len(msg) == size * size, (
        f"letters {sum(map(len, words))} + message {len(msg)} must equal {size * size}")
    rng = random.Random(seed)
    order = sorted(words, key=len, reverse=True)
    g = [[None] * size for _ in range(size)]
    pos, budget, result = {}, [tries], []

    def options(w, ndiag):
        # no shared start cell, and words with the same first letter never start next to each other
        starts = [(p[0], p[1], ww[0]) for ww, p in pos.items()]
        opts = []
        for dr, dc in DIRS:
            if dr and dc and ndiag >= max_diag:
                continue
            for r in range(size):
                for c in range(size):
                    er, ec = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
                    if not (0 <= er < size and 0 <= ec < size):
                        continue
                    if any((r, c) == (a, b) or (ch0 == w[0] and abs(r - a) <= 1 and abs(c - b) <= 1)
                           for a, b, ch0 in starts):
                        continue
                    if all(g[r + dr * i][c + dc * i] is None for i in range(len(w))):
                        opts.append((r, c, dr, dc))
        rng.shuffle(opts)
        return opts

    def finish():
        if len({(p[2], p[3]) for p in pos.values()}) < 4:
            return None
        gg = [row[:] for row in g]
        empty = [(r, c) for r in range(size) for c in range(size) if gg[r][c] is None]
        for (r, c), ch in zip(empty, msg):
            gg[r][c] = ch
        if all(count_occurrences(gg, w) == 1 for w in words):
            return {"grid": gg, "pos": {w: list(pos[w]) for w in pos}, "message": message}
        return None

    def dfs(k, ndiag):
        if k == len(order):
            res = finish()
            if res:
                result.append(res)
            return bool(res)
        w = order[k]
        for r, c, dr, dc in options(w, ndiag)[:12]:
            budget[0] -= 1
            if budget[0] < 0:
                return False
            for i, ch in enumerate(w):
                g[r + dr * i][c + dc * i] = ch
            pos[w] = (r, c, dr, dc)
            if dfs(k + 1, ndiag + (1 if dr and dc else 0)):
                return True
            for i in range(len(w)):
                g[r + dr * i][c + dc * i] = None
            del pos[w]
        return False

    if dfs(0, 0):
        return result[0]
    raise SystemExit("no valid grid found – try another seed")


def check(ws):
    """Re-verifies a saved puzzle. Raises AssertionError with a clear reason."""
    g, pos = ws["grid"], ws["pos"]
    n = len(g)
    used = {}
    for w, (r, c, dr, dc) in pos.items():
        for i, ch in enumerate(w):
            cell = (r + dr * i, c + dc * i)
            assert g[cell[0]][cell[1]] == ch, f"{w}: wrong letter at {cell}"
            assert cell not in used, f"{w} crosses {used.get(cell)} at {cell}"
            used[cell] = w
        assert count_occurrences(g, w) == 1, f"{w} appears {count_occurrences(g, w)} times"
    left = "".join(g[r][c] for r in range(n) for c in range(n) if (r, c) not in used)
    assert left == letters(ws["message"]), f"leftover letters spell {left}"
    return True


def grid_html(ws, cls="ws"):
    g = ws["grid"]
    return f'<table class="{cls}">' + "".join(
        "<tr>" + "".join(f"<td>{ch}</td>" for ch in row) + "</tr>" for row in g) + "</table>"


def key_svg(ws, width_mm=46):
    """Answer key: the grid with one coloured capsule per word, plus the word's number."""
    g, pos = ws["grid"], ws["pos"]
    n, u = len(g), 10
    cols = ["#F2AE94", "#9ECBB4", "#B9A9DA", "#9CCAD6", "#F5CF7A"]
    order = list(pos)
    caps, txt = [], []
    for k, w in enumerate(order):
        r, c, dr, dc = pos[w]
        x1, y1 = c * u + u / 2, r * u + u / 2
        x2, y2 = (c + dc * (len(w) - 1)) * u + u / 2, (r + dr * (len(w) - 1)) * u + u / 2
        caps.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{cols[k % len(cols)]}" '
                    f'stroke-width="8.2" stroke-linecap="round" opacity=".85"/>')
    used = {(pos[w][0] + pos[w][2] * i, pos[w][1] + pos[w][3] * i) for w in pos for i in range(len(w))}
    for r in range(n):
        for c in range(n):
            col = "#1B2147" if (r, c) in used else "#A99BC2"
            wt = 700 if (r, c) in used else 500
            txt.append(f'<text x="{c * u + u / 2}" y="{r * u + u / 2 + 2.3}" text-anchor="middle" '
                       f'font-size="6.2" font-weight="{wt}" fill="{col}">{g[r][c]}</text>')
    return (f'<svg viewBox="0 0 {n * u} {n * u}" style="width:{width_mm}mm;height:{width_mm}mm;'
            f'font-family:Poppins,sans-serif;display:block">'
            f'<rect width="{n * u}" height="{n * u}" rx="3" fill="#fff"/>{"".join(caps)}{"".join(txt)}</svg>')


def slots(word, first=True):
    """Letter slots for a clue: first letter shown, one short line per remaining letter."""
    w = word.upper()
    head = '<b class="sl1">' + w[0].lower() + '</b>' if first else '<span class="sl"></span>'
    return '<span class="slots">' + head + '<span class="sl"></span>' * (len(w) - 1) + '</span>'


def message_slots(message):
    """Blank boxes for the secret message, word by word (apostrophes shown)."""
    out = []
    for word in message.split():
        out.append('<span class="mw">' + "".join(
            '<span class="ap">\'</span>' if ch == "'" else '<span class="mb"></span>' for ch in word) + "</span>")
    return "".join(out)


if __name__ == "__main__":
    spec_path = pathlib.Path(sys.argv[1])
    spec = json.loads(spec_path.read_text())
    ws = generate(spec["size"], spec["words"], spec["message"], spec.get("seed", 1), max_diag=spec.get("max_diag", 4))
    check(ws)
    (spec_path.parent / "ws.json").write_text(json.dumps(ws))
    for row in ws["grid"]:
        print(" ".join(row))
    for w, p in ws["pos"].items():
        print(w, p)
