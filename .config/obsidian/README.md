# Obsidian

Shared config for all vaults. `link.sh <vault>` symlinks these files into a vault. Existing non-symlink files are moved to `<name>.bak`.

```sh
~/.config/obsidian/link.sh ~/Vaults/knowledge
```

## Files

| File here | Vault path | Purpose |
| --- | --- | --- |
| `vimrc` | `.obsidian.vimrc` | Vim keymaps, loaded by Vimrc Support |
| `vimrc-preview-link.js` | `.obsidian/vimrc-preview-link.js` | `K` opens page preview for link under cursor |
| `app.json` | `.obsidian/app.json` | Vim mode on, attachment folder `assets` |
| `appearance.json` | `.obsidian/appearance.json` | Theme `moonstone` |
| `core-plugins.json` | `.obsidian/core-plugins.json` | Enabled core plugins |
| `community-plugins.json` | `.obsidian/community-plugins.json` | Enabled community plugins |
| `hotkeys.json` | `.obsidian/hotkeys.json` | Custom hotkeys |
| `plugins/<id>/data.json` | `.obsidian/plugins/<id>/data.json` | Plugin settings |

Vault specific files (`workspace.json`, `graph.json`, `daily-notes.json`, `templates.json`, `types.json`) stay in each vault. Plugin code (`main.js`, `manifest.json`, `styles.css`) is not tracked.

Settings changed in any linked vault write through the symlink, so every vault shares them.

## Manual setup for a new vault

1. Run `link.sh <vault>`.
2. Settings → Community plugins → turn off Restricted mode.
3. Install and enable:

   | Plugin | ID | Version at export |
   | --- | --- | --- |
   | Vimrc Support | `obsidian-vimrc-support` | 0.10.2 |
   | PDF++ | `pdf-plus` | 0.40.27 |
   | Pandoc Plugin | `obsidian-pandoc` | 0.4.1 |
   | Tasks | `obsidian-tasks-plugin` | 7.23.1 |

   Installing does not overwrite an existing `data.json`. If a plugin was installed before linking, rerun `link.sh`.
4. Vimrc Support: "Support JS commands" must be on (`supportJsCommands: true`). `K` (`:jsfile`) fails without it.
5. Pandoc Plugin needs the binary: `brew install pandoc`. PDF export also needs a LaTeX engine (`brew install --cask basictex`).
6. Settings → Hotkeys: unbind any default on `Ctrl+O` / `Ctrl+I` so the vimrc back/forward maps work.
7. Theme `moonstone` is built in.
8. Restart Obsidian so the vimrc reloads.

## Caveats

Obsidian Sync does not reliably sync symlinked files. Mobile devices get config from Sync, so changes here may not reach them.

## Adding a plugin

1. Install it in a vault.
2. Move its `data.json` here: `mkdir -p plugins/<id> && mv <vault>/.obsidian/plugins/<id>/data.json plugins/<id>/`
3. Rerun `link.sh` for each vault.
4. Add it to the plugin table and `dotfiles add ~/.config/obsidian`.
