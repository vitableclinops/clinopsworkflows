#!/bin/bash
# Runs the /meeting-summary skill for ClinOps Weekly Sync.
# Invoked by launchd every Tuesday at 12:45 PM — see install-schedule.sh.

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$HOME/.clinops-meeting-summary.log"

echo "$(date): starting meeting summary" >> "$LOG"
cd "$REPO_DIR"
claude --dangerously-skip-permissions -p "/meeting-summary ClinOps Weekly Sync" >> "$LOG" 2>&1
echo "$(date): done (exit $?)" >> "$LOG"
