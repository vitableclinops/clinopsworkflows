#!/bin/bash
# Runs the /tddaily-availability-report skill and posts results to #appointment-availability-update.
# Invoked by launchd daily — see install-availability-schedule.sh.

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$HOME/.clinops-tddaily-availability-report.log"

echo "$(date): starting daily availability report" >> "$LOG"
cd "$REPO_DIR"
claude --dangerously-skip-permissions -p "/tddaily-availability-report" >> "$LOG" 2>&1
echo "$(date): done (exit $?)" >> "$LOG"
