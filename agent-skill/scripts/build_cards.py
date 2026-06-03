#!/usr/bin/env python3
"""Split the carousel HTML into 7 standalone 1080×1080 PNGs for LinkedIn upload."""
import re, subprocess, pathlib

SRC = pathlib.Path(__file__).parent / "card-xiaohongshu-bcg-linear.html"
OUT = SRC.parent / "cards"
OUT.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

html = SRC.read_text(encoding="utf-8")
head = html[: html.index("</head>")]  # <!doctype>…<head>…<style>…</style>
override = (
    "<style>html,body{margin:0!important;padding:0!important;background:#010102}"
    ".deck{gap:0!important}.card{max-width:none!important;border-radius:0!important}</style>"
)

region = html[html.index("<!-- 01") : html.index("</body>")]
parts = [p for p in re.split(r"(?=<!-- 0\d ·)", region) if p.strip().startswith("<!--")]
assert len(parts) == 7, f"expected 7 cards, got {len(parts)}"

for i, part in enumerate(parts, 1):
    card = part.rstrip()
    if i == 7:  # last chunk carries the deck-closing </div>
        card = card[: card.rfind("</div>")].rstrip()
    doc = f'{head}{override}</head><body><div class="deck">{card}</div></body></html>'
    tmp = OUT / f"_card-{i:02d}.html"
    tmp.write_text(doc, encoding="utf-8")
    out_png = OUT / f"card-{i:02d}.png"
    subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=2",
            "--window-size=1080,1080",
            f"--screenshot={out_png}",
            tmp.as_uri(),
        ],
        capture_output=True,
    )
    tmp.unlink()
    print(f"✓ {out_png.name}")

print(f"\n{len(parts)} PNG → {OUT}")
