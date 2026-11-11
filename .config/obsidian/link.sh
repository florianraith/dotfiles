#!/usr/bin/env bash
# Symlink shared Obsidian config into a vault.
# Usage: link.sh <vault-path>
# Existing files are moved to <name>.bak first.
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)"
vault="${1:?usage: link.sh <vault-path>}"
mkdir -p "$vault/.obsidian"

link() {
  local from="$1" to="$2"
  mkdir -p "$(dirname "$to")"
  if [[ -e "$to" && ! -L "$to" ]]; then mv "$to" "$to.bak"; fi
  ln -sfn "$from" "$to"
  echo "$to -> $from"
}

link "$src/vimrc" "$vault/.obsidian.vimrc"
link "$src/vimrc-preview-link.js" "$vault/.obsidian/vimrc-preview-link.js"
for f in app appearance core-plugins community-plugins hotkeys; do
  link "$src/$f.json" "$vault/.obsidian/$f.json"
done
for d in "$src"/plugins/*; do
  id="$(basename "$d")"
  link "$d/data.json" "$vault/.obsidian/plugins/$id/data.json"
done
