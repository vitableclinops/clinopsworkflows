#!/bin/bash
# Runs the /daily-availability-report skill and posts to #appointment-availability-update.
# Invoked by launchd every weekday at 8:00 AM — see install-availability-schedule.sh.

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$HOME/.clinops-daily-availability-report.log"

echo "$(date): starting daily availability report" >> "$LOG"
cd "$REPO_DIR"
claude --dangerously-skip-permissions -p "/daily-availability-report" >> "$LOG" 2>&1
echo "$(date): done (exit $?)" >> "$LOG"
