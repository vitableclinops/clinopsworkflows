---
name: daily-availability-report
description: Pull today's appointment availability data from Jotform, compile a structured report, and post it to the #appointment-availability-update Slack channel.
usage: /daily-availability-report
examples:
  - /daily-availability-report
prerequisites:
  - Jotform MCP server
  - Slack MCP server
---

# Daily Availability Report Workflow

Pull today's appointment availability data from Jotform, compile a structured report, and post it to the #appointment-availability-update Slack channel.

**Usage:** `/daily-availability-report`

---

## Prerequisites

| MCP Server | Why |
|---|---|
| **Jotform** | Pulls appointment availability submissions |
| **Slack** | Posts the daily report |

Check connected servers with `/mcp`. To add one, go to **Settings → MCP Servers** in Claude Code.

---

## Steps

### 1. Find the availability form in Jotform

Use `mcp__Jotform__search` to find the appointment availability form. Search for terms like "availability", "appointment", or "scheduling". Pick the form most closely matching a daily availability or scheduling intake form.

If multiple forms are found, prefer the one most recently active.

If no form is found, tell the user and stop.

### 2. Pull today's submissions

Use `mcp__Jotform__list_submissions` for the form found in step 1. Filter to submissions created today (use today's date in YYYY-MM-DD format).

If there are no submissions today, note that in the report rather than stopping.

### 3. Analyze availability data

Use `mcp__Jotform__analyze_submissions` to identify patterns in today's submissions:

- Total number of availability submissions received
- Breakdown by time slot (morning / afternoon / evening) if the data includes time preferences
- Breakdown by provider or location if applicable
- Any slots marked as fully booked or unavailable
- Any urgent or priority requests

### 4. Find the Slack channel

Use `mcp__Slack__slack_search_channels` with `channel_types: "public_channel,private_channel"` to find `#appointment-availability-update`. If not found by exact name, search for "availability" or "appointment".

### 5. Compile and post the report

Use `mcp__Slack__slack_send_message` to post to the channel found in step 4.

Format:
```
*Daily Appointment Availability Report — [DATE]*

*Total Submissions Today:* [N]

---

*Availability by Time Slot*
• Morning (8 AM–12 PM): [N] open / [N] requested
• Afternoon (12 PM–5 PM): [N] open / [N] requested
• Evening (5 PM–8 PM): [N] open / [N] requested

*By Provider / Location* _(if applicable)_
• [Provider/Location]: [summary]

---

*Flags & Notes*
• [Any fully booked slots, urgent requests, or anomalies]

---
_Report generated at [TIME] CDT. Source: Jotform availability form._
```

If there are no submissions today, post:
```
*Daily Appointment Availability Report — [DATE]*

No availability submissions received today as of [TIME] CDT.
```

---

## Tips

- **Form not found?** Ask the user for the Jotform form name or ID before proceeding.
- **No data yet today?** Run again later in the day — submissions may still be coming in.
- **Channel access denied?** Ask the user to confirm the channel name or have a channel admin add the bot.
- **Time zone:** All times in the report should use CDT/CST (US Central), not UTC.
