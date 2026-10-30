#!/bin/bash

input=$(cat)

model=$(echo "$input" | jq -r '.model.display_name')
dir=$(echo "$input" | jq -r '.workspace.current_dir')
dir_name=$(basename "$dir")

five_pct=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
five_reset=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')
week_pct=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
week_reset=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at // empty')

fmt_reset() {
  local ts="$1"
  [ -z "$ts" ] && return
  date -r "$ts" "+%a %H:%M" 2>/dev/null
}

usage=""
if [ -n "$five_pct" ]; then
  reset=$(fmt_reset "$five_reset")
  usage="5h: $(printf '%.0f' "$five_pct")%"
  [ -n "$reset" ] && usage="$usage (resets $reset)"
fi
if [ -n "$week_pct" ]; then
  reset=$(fmt_reset "$week_reset")
  seg="7d: $(printf '%.0f' "$week_pct")%"
  [ -n "$reset" ] && seg="$seg (resets $reset)"
  if [ -n "$usage" ]; then
    usage="$usage | $seg"
  else
    usage="$seg"
  fi
fi

printf "\033[2m%s\033[0m \033[2m|\033[0m \033[2m%s\033[0m" "$dir_name" "$model"
[ -n "$usage" ] && printf " \033[2m|\033[0m \033[2m%s\033[0m" "$usage"
