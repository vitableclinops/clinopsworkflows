---
name: tddaily-availability-report
description: Pull daily appointment availability data and post a summary report to the #appointment-availability-update Slack channel.
usage: /tddaily-availability-report
prerequisites:
  - Slack MCP server
---

# TD Daily Availability Report

Pull daily appointment availability data and post a summary report to the #appointment-availability-update Slack channel (ID: C08A03ET7C3).

**Usage:** `/tddaily-availability-report`

---

<!-- TODO: Replace the Steps section below with the content from tddaily-availability-report.skill -->

## Steps

### 1. Gather availability data

_[Add data-gathering steps from your .skill file here]_

### 2. Post to Slack

Use `mcp__Slack__slack_send_message` to post the report to `#appointment-availability-update` (channel ID: `C08A03ET7C3`).
