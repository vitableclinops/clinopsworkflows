---
name: meeting-summary
description: After a team's recurring sync, pull the meeting notes from Granola, synthesize a summary with per-person action items, post it to the team's Slack channel, and file each action item in the team's Linear Triage queue.
usage: /meeting-summary <meeting name>
examples:
  - /meeting-summary ClinOps Weekly Sync
  - /meeting-summary Sales Weekly Sync
  - /meeting-summary Engineering Weekly
  - /meeting-summary Product Sync
prerequisites:
  - Granola MCP server
  - Slack MCP server
  - Linear MCP server
---

# Meeting Summary Workflow

After a team's recurring sync, pull the meeting notes from Granola, synthesize a summary with per-person action items, post it to the team's Slack channel, and file each action item in the team's Linear Triage queue.

**Usage:** `/meeting-summary <meeting name>`

**Examples:**
- `/meeting-summary ClinOps Weekly Sync`
- `/meeting-summary Sales Weekly Sync`
- `/meeting-summary Engineering Weekly`
- `/meeting-summary Product Sync`

---

## Prerequisites

You need three MCP servers connected in your Claude Code session:

| MCP Server | Why |
|---|---|
| **Granola** | Pulls meeting notes |
| **Slack** | Posts the summary |
| **Linear** | Creates Triage issues |

Check connected servers with `/mcp`. To add one, go to **Settings → MCP Servers** in Claude Code or edit `~/.claude/mcp.json`. Ask your workspace admin if you need API credentials.

---

## Steps

### 1. Find the meeting in Granola

Search for a meeting whose title matches (or closely matches) the argument provided: **$ARGUMENTS**

Use `mcp__Granola__list_meetings` with `time_range: "this_week"`. If not found, try `last_week`.

If still not found, tell the user and stop.

### 2. Pull the full notes

Use `mcp__Granola__get_meetings` with the meeting ID to get the full summary and any private notes.

### 3. Identify the team

Infer the team name from the meeting title (e.g. "ClinOps Weekly Sync" → ClinOps / Clinical, "Sales Weekly Sync" → Sales, "Engineering Weekly" → Engineering). Use this to find the right Slack channel and Linear team in the steps below.

### 4. Find the Slack channel

Use `mcp__Slack__slack_search_channels` with `channel_types: "public_channel,private_channel"` to find the team's primary meeting or general channel. Good search terms: the team name + "meeting", "sync", "general", or "standup". Pick the most relevant result — prefer a dedicated meeting-notes or process-improvement channel over a general one if one exists.

If multiple plausible channels are found, pick the most specific one and note your choice in the message.

### 5. Find the Linear team

Use `mcp__Linear__list_teams` and match on the inferred team name. If the exact name isn't found, pick the closest match and tell the user.

Use `mcp__Linear__list_issue_statuses` with that team to confirm a "Triage" state exists. If there's no Triage state, use the earliest unstarted state instead.

### 6. Synthesize the content

From the meeting notes produce:

**a) Structured summary** — one section per major topic with bullet points covering what was discussed, decisions made, and open questions/blockers.

**b) Per-person action items** — scan the summary and next-steps for every concrete action item. Group by owner (full first name). Items with no clear owner go under "Team."

### 7. Post to Slack

Use `mcp__Slack__slack_send_message` to post to the channel found in step 4.

Format:
**[Meeting Title] — Summary ([date])**

**Attendees:** [comma-separated first names]

---

**[Topic 1]**
- bullet
- bullet

**[Topic 2]**
...

---

**Action Items**

**[Person]**
- [ ] item

**[Person]**
...

---
_Action items have been added to [Team] Triage in Linear._

### 8. Create Linear issues

For each action item, call `mcp__Linear__save_issue` with:
- `team`: the team name from step 5
- `state`: `Triage` (or the fallback from step 5)
- `assignee`: the person's name or email (use `mcp__Linear__list_users` to look up by name if needed)
- `title`: concise action item text
- `description`: 2–3 sentences of context from the meeting

Create all issues in parallel (single message, multiple tool calls).

---

## Tips

- **Meeting not in Granola yet?** Notes typically appear 5–10 minutes after the meeting ends. Wait and retry.
- **Can't find the right Slack channel?** Ask the user which channel to post to before proceeding.
- **No Triage state in Linear?** Use the first available backlog or unstarted state, and tell the user.
- **Assignee not in Linear?** Use `mcp__Linear__list_users` to search by first name rather than guessing an email.
- **Private Slack channel access denied?** Ask the user to confirm the channel name or have a channel admin add the bot.
