"""Builds light.svg and dark.svg (terminal-style profile card) from portrait.txt."""
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
ASCII = [l.rstrip("\n") for l in (HERE / "portrait.txt").read_text().splitlines() if l.strip()]

INFO = [
    ("head", "hammad@devos"),
    ("kv", "Subject", "Hammad"),
    ("kv", "Role", "Agentic AI Developer"),
    ("kv", "Focus", "AI Agents · RAG · Automation"),
    ("kv", "Status", "Building • Learning • Shipping"),
    ("gap",),
    ("kv", "Core Lang", "Python"),
    ("kv", "Core Agents", "LangChain, LangGraph"),
    ("kv", "Core Backend", "FastAPI, REST APIs"),
    ("kv", "Core AI", "RAG, Chunking, Retrieval"),
    ("kv", "Core Patterns", "Human-in-the-loop, Fan-in/out"),
    ("kv", "Core Observe", "LangSmith"),
    ("gap",),
    ("sec", "Contact"),
    ("kv", "Grid Github", "hammad-cloud"),
    ("gap",),
    ("sec", "Live Stats"),
    ("cursor", "See live GitHub activity below ↓"),
]

THEMES = {
    "dark": dict(bg="#070b14", panel="#0b1220", border="#22d3ee", border2="#1e3a5f",
                 text="#e2e8f0", key="#38bdf8", dim="#475569", head="#a78bfa",
                 ascii="#93c5fd", accent="#22d3ee", red="#f43f5e", title="#64748b"),
    "light": dict(bg="#f8fafc", panel="#ffffff", border="#0891b2", border2="#cbd5e1",
                  text="#0f172a", key="#0369a1", dim="#94a3b8", head="#7c3aed",
                  ascii="#1e40af", accent="#0891b2", red="#e11d48", title="#64748b"),
}

W, H = 1000, 460
LX, LY, LW, LH = 18, 52, 430, 390     # left panel
RX, RY, RW, RH = 462, 52, 520, 390    # right panel


def build(theme: str) -> str:
    t = THEMES[theme]
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">')
    o.append(f"""<style>
.k{{fill:{t['key']}}} .v{{fill:{t['text']}}} .d{{fill:{t['dim']}}} .h{{fill:{t['head']};font-weight:700}}
.ln{{opacity:0;animation:fade .35s ease forwards}}
@keyframes fade{{to{{opacity:1}}}}
@keyframes reveal{{from{{height:0}}to{{height:{LH}px}}}}
@keyframes scan{{0%{{transform:translateY(0)}}100%{{transform:translateY({LH - 30}px)}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes pulse{{50%{{opacity:.25}}}}
#rv{{animation:reveal 3.2s steps(44) forwards}}
.scan{{animation:scan 3.2s linear infinite alternate}}
.cur{{animation:blink 1s step-end infinite}}
.dot{{animation:pulse 1.4s ease-in-out infinite}}
</style>""")
    o.append(f'<defs><clipPath id="cp"><rect id="rv" x="{LX}" y="{LY}" width="{LW}" height="0"/></clipPath>'
             f'<linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="{t["accent"]}" stop-opacity=".9"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></linearGradient></defs>')
    # window
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>')
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        o.append(f'<circle cx="{22 + i*16}" cy="22" r="5" fill="{c}"/>')
    o.append(f'<text x="{W/2}" y="26" text-anchor="middle" font-size="11" fill="{t["title"]}">hammad@devos ~ $ ./profile.sh --live</text>')
    o.append(f'<circle class="dot" cx="{W-92}" cy="22" r="3.5" fill="{t["red"]}"/>')
    o.append(f'<text x="{W-84}" y="26" font-size="10" fill="{t["red"]}" letter-spacing="1">SCANNING</text>')
    # panels
    for x, y, w, h, label in [(LX, LY, LW, LH, "VISUAL.MAP"), (RX, RY, RW, RH, "SYSTEM.INFO")]:
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{t["panel"]}" stroke="{t["border2"]}"/>')
        o.append(f'<text x="{x+10}" y="{y-6}" font-size="9" letter-spacing="2" fill="{t["accent"]}">{label}</text>')
    # ascii portrait
    fs, lh = 8.6, 8.6
    cols = 76
    char_w = fs * 0.6
    ax = LX + (LW - cols * char_w) / 2
    ay = LY + (LH - len(ASCII) * lh) / 2 + lh
    o.append(f'<g clip-path="url(#cp)"><text font-size="{fs}" fill="{t["ascii"]}" xml:space="preserve">')
    for i, line in enumerate(ASCII):
        o.append(f'<tspan x="{ax:.1f}" y="{ay + i*lh:.1f}">{escape(line)}</tspan>')
    o.append('</text></g>')
    o.append(f'<rect class="scan" x="{LX+6}" y="{LY+15}" width="{LW-12}" height="2" fill="url(#sg)"/>')
    # info lines
    y = RY + 26
    x = RX + 16
    delay = 0.4
    for item in INFO:
        kind = item[0]
        if kind == "gap":
            y += 10
            continue
        style = f'style="animation-delay:{delay:.2f}s"'
        if kind == "head":
            o.append(f'<text class="ln" {style} x="{x}" y="{y}" font-size="13"><tspan class="h">{escape(item[1])}</tspan>'
                     f'<tspan class="d"> {"─"*44}</tspan></text>')
        elif kind == "sec":
            o.append(f'<text class="ln" {style} x="{x}" y="{y}" font-size="12"><tspan class="d">- </tspan>'
                     f'<tspan class="k">{escape(item[1])}</tspan><tspan class="d"> {"─"*40}</tspan></text>')
        elif kind == "kv":
            k, v = item[1], item[2]
            dots = "." * max(3, 26 - len(k))
            o.append(f'<text class="ln" {style} x="{x}" y="{y}" font-size="12"><tspan class="d">. </tspan>'
                     f'<tspan class="k">{escape(k)}</tspan><tspan class="d">: {dots} </tspan>'
                     f'<tspan class="v">{escape(v)}</tspan></text>')
        elif kind == "cursor":
            o.append(f'<g class="ln" {style}><rect class="cur" x="{x}" y="{y-10}" width="7" height="13" fill="{t["accent"]}"/>'
                     f'<text x="{x+12}" y="{y}" font-size="12" class="v">{escape(item[1])}</text></g>')
        y += 19
        delay += 0.18
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    for th in THEMES:
        (HERE / f"{th}.svg").write_text(build(th), encoding="utf-8")
    print("ok")
