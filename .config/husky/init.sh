# Sourced by Husky (.husky/_/h) before every hook. $n holds the hook name.
# Plays a sound once pre-commit (the slow test suite) finishes.
if [ "$n" = "pre-commit" ] && command -v afplay >/dev/null 2>&1; then
	trap 'status=$?
	if [ $status = 0 ]; then
		afplay /System/Library/Sounds/Hero.aiff &
		osascript -e "display notification \"Commit hooks passed\" with title \"git commit\"" &
	else
		afplay /System/Library/Sounds/Basso.aiff &
		osascript -e "display notification \"Commit hooks failed\" with title \"git commit\"" &
	fi' EXIT
fi
