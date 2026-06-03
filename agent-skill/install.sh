#!/usr/bin/env bash
# Install html-anything as a global agent skill for Claude Code AND Codex.
# Builds a self-contained skill: wrapper SKILL.md + 78 templates (copied from
# this repo) + generated catalog. Re-run after `git pull` to refresh templates.
#
#   ./agent-skill/install.sh                 # → ~/.claude/skills/html-anything + codex symlink
#   ./agent-skill/install.sh /custom/path    # → custom Claude skill dir
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"          # agent-skill/
REPO="$(cd "$HERE/.." && pwd)"
SRC="$REPO/next/src/lib/templates/skills"
DEST="${1:-$HOME/.claude/skills/html-anything}"

[ -d "$SRC" ] || { echo "fatal: templates not found at $SRC (run from inside the repo)"; exit 1; }

mkdir -p "$DEST/references" "$DEST/scripts"
cp "$HERE/SKILL.md"                    "$DEST/SKILL.md"
cp "$HERE/scripts/build_catalog.py"    "$DEST/scripts/build_catalog.py"
cp "$HERE/scripts/build_cards.py"      "$DEST/scripts/build_cards.py"      # per-card PNG splitter
cp "$HERE/example-ko-card-linear.html" "$DEST/references/example-ko-card-linear.html"  # gold KO example
rm -rf "$DEST/references/skills"
cp -R "$SRC" "$DEST/references/skills"

python3 "$DEST/scripts/build_catalog.py"

# Codex uses the identical SKILL.md format — register via symlink (single source).
if [ -d "$HOME/.codex/skills" ]; then
  ln -sfn "$DEST" "$HOME/.codex/skills/html-anything"
  echo "codex   → ~/.codex/skills/html-anything (symlink)"
fi

n=$(find "$DEST/references/skills" -name SKILL.md | wc -l | tr -d ' ')
echo "claude  → $DEST"
echo "done: $n templates installed. Restart the agent session to pick up the new skill."
