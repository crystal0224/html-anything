#!/usr/bin/env python3
"""Regenerate references/catalog.md from the 78 template SKILL.md frontmatters.

Run after pulling new templates from upstream (nexu-io/html-anything):
    python3 scripts/build_catalog.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "references" / "skills"
OUT = ROOT / "references" / "catalog.md"

# Surface mode grouping (category -> human label + emoji), ordered.
GROUPS = [
    ("slides", "🎬 Deck / Slides"),
    ("prototype", "🛠️ Web Prototype"),
    ("dashboard", "📊 Dashboard"),
    ("data", "📈 Data Report"),
    ("doc", "📄 Document"),
    ("article", "📖 Magazine / Article"),
    ("poster", "🖼️ Poster"),
    ("card", "📱 Social Card (XHS / Tweet / etc.)"),
    ("video", "🎞️ Video Frame (Hyperframes / Remotion)"),
    ("mobile", "📲 Mobile App"),
    ("finance", "💰 Finance"),
    ("resume", "🧑 Résumé"),
    ("email", "✉️ Email"),
]


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def main():
    rows = []
    for d in sorted(SKILLS.iterdir()):
        sk = d / "SKILL.md"
        if not sk.is_file():
            continue
        fm = parse_frontmatter(sk.read_text(encoding="utf-8"))
        rows.append(
            {
                "name": fm.get("name", d.name),
                "emoji": fm.get("emoji", ""),
                "en": fm.get("en_name", ""),
                "desc": fm.get("description", ""),
                "category": fm.get("category", "other"),
                "scenario": fm.get("scenario", ""),
                "recommended": fm.get("recommended", ""),
                "has_example": (d / "example.html").is_file(),
            }
        )

    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r)

    lines = [
        "# html-anything · Template Catalog",
        "",
        f"{len(rows)} ship-ready HTML design templates across {len(by_cat)} surface categories.",
        "Each row: `name` — pick one, then read `references/skills/<name>/SKILL.md` (design prompt + hard constraints) and `example.html` (reference output) before generating.",
        "",
        "`scenario`: design / marketing / engineering / product / personal. `★` = upstream-recommended (lower number = higher).",
        "",
    ]

    seen = set()
    ordered = GROUPS + [(c, f"📦 {c}") for c in sorted(by_cat) if c not in dict(GROUPS)]
    for cat, label in ordered:
        items = by_cat.get(cat)
        if not items:
            continue
        seen.add(cat)

        # sort: recommended first (numeric), then name
        def sortkey(r):
            rec = r["recommended"]
            return (0, int(rec)) if rec.isdigit() else (1, 0), r["name"]

        items = sorted(
            items,
            key=lambda r: (
                (0, int(r["recommended"])) if r["recommended"].isdigit() else (1, 999),
                r["name"],
            ),
        )
        lines.append(f"## {label}  ({len(items)})")
        lines.append("")
        lines.append("| name | scenario | what it produces |")
        lines.append("|---|---|---|")
        for r in items:
            star = f"★{r['recommended']} " if r["recommended"].isdigit() else ""
            ex = "" if r["has_example"] else " *(no example.html)*"
            desc = r["desc"].replace("|", "\\|")
            lines.append(
                f"| `{r['name']}` | {r['scenario']} | {star}{r['emoji']} {desc}{ex} |"
            )
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} — {len(rows)} templates, {len(by_cat)} categories")


if __name__ == "__main__":
    main()
