# Claude Code setup

`settings.json` is not tracked. Add the following keys to `~/.claude/settings.json` by hand.

## Status line

Shows directory, model, and 5h/7d rate limit usage with reset times. Requires `jq`.

```json
"statusLine": {
  "type": "command",
  "command": "bash ~/.claude/statusline-command.sh"
}
```

## Notification sound

Plays a sound and shows a macOS notification when Claude finishes a task.

```json
"hooks": {
  "Stop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "afplay /System/Library/Sounds/Glass.aiff & osascript -e 'display notification \"Task finished\" with title \"Claude Code\"'"
        }
      ]
    }
  ]
}
```

Run `/hooks` in Claude Code afterwards to confirm the hook is loaded.
