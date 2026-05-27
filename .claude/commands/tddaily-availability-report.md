---
name: tddaily-availability-report
description: Each morning, pull today's appointment availability data and post a structured availability update to the #appointment-availability-update Slack channel.
usage: /tddaily-availability-report
examples:
  - /tddaily-availability-report
prerequisites:
  - Slack MCP server
---

# Today's Daily Appointment Availability Report

Pull today's appointment availability data and post a structured update to #appointment-availability-update in Slack.

**Usage:** `/tddaily-availability-report`

---

## Prerequisites

| MCP Server | Why |
|---|---|
| **Slack** | Posts the availability update |

---

## Steps

### 1. Determine today's date

Use the current date (YYYY-MM-DD). This report covers **today only** unless explicitly told otherwise.

### 2. Find the #appointment-availability-update channel

Use `mcp__Slack__slack_search_channels` with query `appointment-availability-update` and `channel_types: "public_channel,private_channel"`.

If not found, stop and tell the user the channel could not be located.

### 3. Gather availability data

Check whatever appointment/scheduling data source is configured for this workflow. If no external data source is wired up yet, note that in the message and post a placeholder report.

Sources to check in order:
1. Any appointment scheduling system accessible via configured MCP tools
2. HubSpot CRM (`mcp__HubSpot__get_crm_objects`) if appointments are tracked there
3. Jotform submissions (`mcp__Jotform__list_submissions`) if booking forms are used

Collect:
- Total available slots for today
- Total booked/confirmed slots
- Any open slots with no booking
- Upcoming slots in the next 24 hours that are still unbooked

### 4. Post the report to Slack

Use `mcp__Slack__slack_send_message` to post to the channel found in step 2.

Format:

```
📅 *Appointment Availability — [Day, Month DD YYYY]*

*Available:* X slots
*Booked:* Y slots
*Open (unbooked):* Z slots

*Open slots today:*
• [Time] — [Provider/Location if known]
• [Time] — [Provider/Location if known]

*Next 24 hrs with no bookings:* [list or "None — fully booked"]

---
_Report generated automatically by ClinOps Workflows._
```

If data could not be retrieved, post:

```
⚠️ *Appointment Availability — [Day, Month DD YYYY]*

Could not retrieve availability data. Please check the scheduling system manually.

---
_Report generated automatically by ClinOps Workflows._
```

---

## Tips

- **No scheduling system connected?** Update this command with the correct MCP tool or API call for your booking system, then re-run.
- **Channel not found?** Confirm the bot has been invited: `/invite @clinops-bot` in the channel.
- **Running for a different date?** Pass the date as an argument: `/tddaily-availability-report 2026-06-01`
