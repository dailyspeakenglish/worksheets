"""Crossword generator, strict checker and HTML renderer for worksheets.

Guarantees (checked by `check`, so a broken puzzle can never be published):
  * every word is placed exactly once, across or down, and all words are connected;
  * every horizontal / vertical run of 2+ letters in the grid is one of the placed words
    (no accidental "words" made by neighbouring letters);
  * numbering follows normal crossword rules (left-to-right, top-to-bottom);
  * the grid fits inside max_cols x max_rows.

Usage (from the repo root):
  python3 _source/tools/crossword.py _source/<slug>/cw_spec.json
cw_spec.json: {"max_cols": 15, "max_rows": 13, "seed": 1,
               "words": [["HOLIDAY", "On a great h…, time flies."], ...]}
Writes _source/<slug>/cw.json. In Python: from crossword import grid_html, clues_html
"""
import json, random, sys, pathlib


def _cells(word, r, c, d):
    dr, dc = (0, 1) if d == "A" else (1, 0)
    return [(r + dr * i, c + dc * i, ch) for i, ch in enumerate(word)]


def _can_place(grid, word, r, c, d):
    """Standard crossword placement rules on an unbounded dict grid."""
    dr, dc = (0, 1) if d == "A" else (1, 0)
    pr, pc = (1, 0) if d == "A" else (0, 1)          # perpendicular step
    if grid.get((r - dr, c - dc)) or grid.get((r + dr * len(word), c + dc * len(word))):
        return -1                                      # touching end-to-end
    inter = 0
    for rr, cc, ch in _cells(word, r, c, d):
        cur = grid.get((rr, cc))
        if cur:
            if cur != ch:
                return -1
            inter += 1
        else:
            if grid.get((rr + pr, cc + pc)) or grid.get((rr - pr, cc - pc)):
                return -1                              # side-by-side with another word
    if inter == len(word):
        return -1
    return inter


def generate(words, max_cols=15, max_rows=13, seed=1, tries=4000):
    rng = random.Random(seed)
    words = [w.upper() for w in words]
    best = None
    for _ in range(tries):
        order = sorted(words, key=lambda w: (-len(w), rng.random()))
        first, rest = order[0], order[1:]
        grid, placed = {}, []
        for rr, cc, ch in _cells(first, 0, 0, "A"):
            grid[(rr, cc)] = ch
        placed.append((first, 0, 0, "A"))
        pending = rest[:]
        stuck = 0
        while pending and stuck < len(pending) + 2:
            w = pending.pop(0)
            opts = []
            for (gr, gc), gch in list(grid.items()):
                for i, ch in enumerate(w):
                    if ch != gch:
                        continue
                    for d in "AD":
                        r, c = (gr, gc - i) if d == "A" else (gr - i, gc)
                        k = _can_place(grid, w, r, c, d)
                        if k > 0:
                            cells = list(grid) + [(x, y) for x, y, _ in _cells(w, r, c, d)]
                            rows = max(x for x, _ in cells) - min(x for x, _ in cells) + 1
                            cols = max(y for _, y in cells) - min(y for _, y in cells) + 1
                            if rows <= max_rows and cols <= max_cols:
                                opts.append((k, -rows * cols, rng.random(), r, c, d))
            if not opts:
                pending.append(w)
                stuck += 1
                continue
            stuck = 0
            opts.sort(reverse=True)
            k, _, _, r, c, d = opts[0] if rng.random() < .7 else rng.choice(opts[:4])
            for rr, cc, ch in _cells(w, r, c, d):
                grid[(rr, cc)] = ch
            placed.append((w, r, c, d))
        if pending:
            continue
        r0 = min(x for x, _ in grid); c0 = min(y for _, y in grid)
        try:
            check(number([(w, r - r0, c - c0, d) for w, r, c, d in placed]))
        except AssertionError:
            continue
        rows = max(x for x, _ in grid) - r0 + 1
        cols = max(y for _, y in grid) - c0 + 1
        n_down = sum(1 for p in placed if p[3] == "D")
        balance = abs(n_down - (len(placed) - n_down))
        score = (rows * cols, balance)
        if best is None or score < best[0]:
            best = (score, placed)
    if best is None:
        raise SystemExit("could not place every word – try another seed or a bigger size")
    placed = best[1]
    r0 = min(min(r, r + (len(w) - 1) * (d == "D")) for w, r, c, d in placed)
    c0 = min(min(c, c + (len(w) - 1) * (d == "A")) for w, r, c, d in placed)
    placed = [(w, r - r0, c - c0, d) for w, r, c, d in placed]
    return number(placed)


def number(placed):
    starts = sorted({(r, c) for _, r, c, _ in placed})
    num = {rc: i + 1 for i, rc in enumerate(starts)}
    entries = [{"word": w, "row": r, "col": c, "dir": d, "num": num[(r, c)]} for w, r, c, d in placed]
    rows = max(e["row"] + (len(e["word"]) - 1) * (e["dir"] == "D") for e in entries) + 1
    cols = max(e["col"] + (len(e["word"]) - 1) * (e["dir"] == "A") for e in entries) + 1
    return {"rows": rows, "cols": cols, "entries": sorted(entries, key=lambda e: (e["dir"], e["num"]))}


def letters_grid(cw):
    g = [[None] * cw["cols"] for _ in range(cw["rows"])]
    for e in cw["entries"]:
        for rr, cc, ch in _cells(e["word"], e["row"], e["col"], e["dir"]):
            assert g[rr][cc] in (None, ch), f"letter clash at {(rr, cc)}"
            g[rr][cc] = ch
    return g


def check(cw):
    g = letters_grid(cw)
    R, C = cw["rows"], cw["cols"]
    placed = {(e["row"], e["col"], e["dir"]): e["word"] for e in cw["entries"]}
    runs = []
    for r in range(R):
        c = 0
        while c < C:
            if g[r][c]:
                s = c
                while c < C and g[r][c]:
                    c += 1
                if c - s >= 2:
                    runs.append(((r, s, "A"), "".join(g[r][s:c])))
            else:
                c += 1
    for c in range(C):
        r = 0
        while r < R:
            if g[r][c]:
                s = r
                while r < R and g[r][c]:
                    r += 1
                if r - s >= 2:
                    runs.append(((s, c, "D"), "".join(g[x][c] for x in range(s, r))))
            else:
                r += 1
    assert len(runs) == len(placed), f"{len(runs)} letter runs but {len(placed)} words – accidental word?"
    for key, w in runs:
        assert placed.get(key) == w, f"unexpected run {w} at {key}"
    words = [e["word"] for e in cw["entries"]]
    assert len(set(words)) == len(words), "duplicate word"
    # connectivity
    cellsets = [set((x, y) for x, y, _ in _cells(e["word"], e["row"], e["col"], e["dir"])) for e in cw["entries"]]
    seen, todo = {0}, [0]
    while todo:
        i = todo.pop()
        for j in range(len(cellsets)):
            if j not in seen and cellsets[i] & cellsets[j]:
                seen.add(j)
                todo.append(j)
    assert len(seen) == len(cellsets), "not all words are connected"
    # numbering
    starts = sorted({(e["row"], e["col"]) for e in cw["entries"]})
    for e in cw["entries"]:
        assert e["num"] == starts.index((e["row"], e["col"])) + 1, "bad numbering"
    return True


def grid_html(cw, cell_mm=6.2, solved=False, cls="cw"):
    g = letters_grid(cw)
    nums = {(e["row"], e["col"]): e["num"] for e in cw["entries"]}
    rows = []
    for r in range(cw["rows"]):
        tds = []
        for c in range(cw["cols"]):
            if not g[r][c]:
                tds.append('<td class="x"></td>')
                continue
            n = f'<span class="cn">{nums[(r, c)]}</span>' if (r, c) in nums else ""
            letter = f'<span class="cl">{g[r][c]}</span>' if solved else ""
            tds.append(f'<td class="o">{n}{letter}</td>')
        rows.append("<tr>" + "".join(tds) + "</tr>")
    return (f'<table class="{cls}" style="--cell:{cell_mm}mm">' + "".join(rows) + "</table>")


def clues_html(cw, clues):
    """clues: {WORD: clue text}. Returns (across_html, down_html)."""
    out = {}
    for d in "AD":
        items = [e for e in cw["entries"] if e["dir"] == d]
        out[d] = "".join(
            f'<div><span class="n">{e["num"]}</span><span>{clues[e["word"]]} <span class="len">({len(e["word"])})</span></span></div>'
            for e in sorted(items, key=lambda e: e["num"]))
    return out["A"], out["D"]


if __name__ == "__main__":
    spec_path = pathlib.Path(sys.argv[1])
    spec = json.loads(spec_path.read_text())
    words = [w for w, _ in spec["words"]]
    cw = generate(words, spec.get("max_cols", 15), spec.get("max_rows", 13), spec.get("seed", 1))
    check(cw)
    (spec_path.parent / "cw.json").write_text(json.dumps(cw))
    for row in letters_grid(cw):
        print(" ".join(ch or "·" for ch in row))
    for e in cw["entries"]:
        print(e["num"], e["dir"], e["word"])
