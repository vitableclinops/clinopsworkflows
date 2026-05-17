#!/bin/bash
# Runs the /daily-availability-report skill each weekday morning.
# Invoked by launchd every weekday at 8:00 AM — see install-availability-schedule.sh.

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$HOME/.clinops-availability-report.log"

echo "$(date): starting availability report" >> "$LOG"
cd "$REPO_DIR"
claude --dangerously-skip-permissions -p "/daily-availability-report" >> "$LOG" 2>&1
echo "$(date): done (exit $?)" >> "$LOG"
