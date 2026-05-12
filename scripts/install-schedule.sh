#!/bin/bash
# Installs the launchd agent that runs /meeting-summary every Tuesday at 12:45 PM.
# Run once from your local clone of this repo:
#   bash scripts/install-schedule.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PLIST_NAME="com.vitablehealth.clinops-meeting-summary.plist"
PLIST_SRC="$REPO_DIR/scripts/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"
SCRIPT="$REPO_DIR/scripts/run-meeting-summary.sh"

# Verify claude CLI is available
if ! command -v claude &>/dev/null; then
    echo "Error: 'claude' CLI not found. Install Claude Code first: https://claude.ai/code"
    exit 1
fi

chmod +x "$SCRIPT"

# Stamp the real repo path into the plist
sed "s|REPO_DIR_PLACEHOLDER|$REPO_DIR|g" "$PLIST_SRC" > "$PLIST_DEST"

# Reload the agent
launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"

echo "✓ Scheduled: ClinOps meeting summary will run every Tuesday at 12:45 PM"
echo "  Repo:   $REPO_DIR"
echo "  Log:    $HOME/.clinops-meeting-summary.log"
echo ""
echo "To test immediately:"
echo "  bash $SCRIPT"
echo ""
echo "To uninstall:"
echo "  launchctl unload $PLIST_DEST && rm $PLIST_DEST"
