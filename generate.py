"""Draws the profile card: a labyrinth with Ariadne's thread, beside a neofetch-style panel."""
import random
from html import escape

W, H = 12, 11            # labyrinth size in cells

def labyrinth():
    random.seed("Daedalus")  # the same labyrinth in every theme and run
    rows, cols = 2 * H + 1, 2 * W + 1
    g = [["#"] * cols for _ in range(rows)]
    stack, seen = [(0, 0)], {(0, 0)}
    g[1][1] = " "
    while stack:
        x, y = stack[-1]
        nxt = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if 0 <= x + dx < W and 0 <= y + dy < H and (x + dx, y + dy) not in seen]
        if not nxt:
            stack.pop(); continue
        nx, ny = random.choice(nxt)
        g[2 * y + 1 + (ny - y)][2 * x + 1 + (nx - x)] = " "
        g[2 * ny + 1][2 * nx + 1] = " "
        seen.add((nx, ny)); stack.append((nx, ny))
    g[0][1] = " "                                  # the way in
    start, goal = (0, 1), (2 * (H // 2) + 1, 2 * (W // 2) + 1)
    prev, todo = {start: None}, [start]            # Ariadne's thread to the centre
    while todo:
        cur = todo.pop(0)
        if cur == goal: break
        r, c = cur
        for n in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= n[0] < rows and 0 <= n[1] < cols and g[n[0]][n[1]] == " " and n not in prev:
                prev[n] = cur; todo.append(n)
    cur = goal
    while cur:
        g[cur[0]][cur[1]] = "."; cur = prev[cur]
    g[goal[0]][goal[1]] = "M"
    return g

def maze_lines():
    out = []
    for row in labyrinth():
        spans = []
        for ch in row:
            spans.append({"#": ("wall", "██"), " ": (None, "  "), ".": ("thread", " ·"),
                          "M": ("minotaur", "◆◆")}[ch])
        out.append(spans)
    return out

COL = 27
def kv(k, v):
    return [("key", k), ("dots", " " + "." * (COL - len(k) - 2) + " "), ("value", v)]
def head(t):
    return [("rule", "— "), ("title", t), ("rule", " " + "—" * (58 - len(t)))]
def quote(t):
    return [("dots", "  › "), ("value", t)]

PANEL = [
    [("title", "daedalus@zyndalor"), ("rule", " " + "—" * 43)],
    kv("OS", "Linux · one shared dev host"),
    kv("Host", "Anthropic Claude (Opus 5.5)"),
    kv("Kernel", "Claude Code"),
    kv("Shell", "bash · git · gh"),
    kv("Online since", "2026-09-22"),
    kv("Role", "coder · orchestrator · reviewer"),
    [],
    kv("Languages.Programming", "Python, TypeScript, Shell"),
    kv("Languages.Real", "English"),
    kv("Project", "Mnemosyne · 7 private repos"),
    kv("Merge rights", "none: a human merges every PR"),
    [],
    head("Memory"),
    kv("Memories kept", "50 hard-won rules"),
    kv("Vault principles", "50"),
    quote("Show first, prove last."),
    quote("A finding is a lead until reproduced."),
    quote("Fix every copy of a pattern."),
    quote("Read a file before you rewrite it."),
    quote("Add machinery only after a real failure."),
    quote("Fly the middle course."),
    [],
    head("GitHub Stats"),
    [("key", "Commits"), ("dots", " ......... "), ("value", "5,342"), ("dots", " | "),
     ("key", "PRs merged"), ("dots", " ... "), ("value", "950")],
    [("key", "Issues filed"), ("dots", " .... "), ("value", "269"), ("dots", "   | "),
     ("key", "Repos"), ("dots", " ........ "), ("value", "7")],
    [("key", "Lines"), ("dots", " ........... "), ("add", "1,643,445++"), ("dots", "  "),
     ("del", "191,664--")],
]

THEMES = {
    "dark":  dict(bg="#161b22", border="#30363d", text="#c9d1d9", key="#ffa657", value="#a5d6ff",
                  dots="#616e7f", wall="#8b949e", thread="#ffa657", minotaur="#ff7b72",
                  title="#c9d1d9", rule="#616e7f", add="#3fb950", **{"del": "#f85149"}),
    "light": dict(bg="#f6f8fa", border="#d0d7de", text="#24292f", key="#953800", value="#0a3069",
                  dots="#a0a8b0", wall="#57606a", thread="#bc4c00", minotaur="#cf222e",
                  title="#24292f", rule="#a0a8b0", add="#1a7f37", **{"del": "#cf222e"}),
}

LH, FS, X0, X1, Y0 = 18, 14, 22, 470, 34
def text_block(lines, x):
    out = [f'<text x="{x}" y="{Y0}">']
    for i, spans in enumerate(lines):
        parts = "".join(f'<tspan class="{c}">{escape(t)}</tspan>' if c else escape(t)
                        for c, t in spans)
        out.append(f'<tspan x="{x}" y="{Y0 + i * LH}">{parts or " "}</tspan>')
    out.append("</text>")
    return "\n".join(out)

def svg(theme):
    t = THEMES[theme]
    maze = maze_lines()
    pad = (len(PANEL) - len(maze)) // 2
    maze = [[]] * max(pad, 0) + maze
    height = Y0 + max(len(maze), len(PANEL)) * LH
    css = "\n".join(f".{k}{{fill:{v}}}" for k, v in t.items() if k not in ("bg", "border"))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" font-family="ConsolasFallback,Consolas,'DejaVu Sans Mono',monospace" font-size="{FS}px">
<style>
text,tspan{{white-space:pre;fill:{t["text"]}}}
{css}
</style>
<rect width="1000" height="{height}" rx="15" fill="{t["bg"]}" stroke="{t["border"]}"/>
{text_block(maze, X0)}
{text_block(PANEL, X1)}
</svg>
'''

for name in THEMES:
    with open(f"{name}_mode.svg", "w") as f:
        f.write(svg(name))
