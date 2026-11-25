# Agent setup preferences

Configure yourself (your own harness config, hooks, status line) to match the preferences below. Platform is macOS. If your harness does not support a setting, skip it and report which ones were skipped.

* **Finish notification**: when a task/turn finishes, play a sound and show a macOS notification
  * `afplay /System/Library/Sounds/Glass.aiff & osascript -e 'display notification "Task finished" with title "Agent"'`
* **Status line** in the prompt session, all segments dimmed and separated by `|`:
  * `<cwd basename> | <model> | 5h: N% (resets Ddd HH:MM) | 7d: N% (resets Ddd HH:MM)`
  * Usage segments show the used percentage of the short window (e.g. 5 hourly) and weekly rate limits, plus reset time formatted as `date "+%a %H:%M"`
  * Omit usage segments if no rate limit data is available
* **External/auto memory**: disabled
* **Voice input**: enabled, push to talk (hold mode)
* **Theme**: auto (follows system light/dark)
* **Skills**: shared skills live in `~/.agents/skills` (one folder per skill, each with a `SKILL.md`). Use them as your global skills. If your harness does not read that directory natively, symlink each skill folder into your own skills directory instead of copying, so updates stay in sync
