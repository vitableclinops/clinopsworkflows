#!/bin/bash
# Runs the /tddaily-availability-report skill each morning.
# Invoked by launchd every weekday at 8:00 AM — see install-availability-report-schedule.sh.

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$HOME/.clinops-availability-report.log"

echo "$(date): starting availability report" >> "$LOG"
cd "$REPO_DIR"
claude --dangerously-skip-permissions -p "/tddaily-availability-report" >> "$LOG" 2>&1
echo "$(date): done (exit $?)" >> "$LOG"
