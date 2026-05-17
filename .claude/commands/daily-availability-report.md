---
name: daily-availability-report
description: Each morning, pull today's appointment availability across providers and post a structured summary to #appointment-availability-update in Slack.
usage: /daily-availability-report
examples:
  - /daily-availability-report
prerequisites:
  - Slack MCP server
---

# Daily Appointment Availability Report

Each morning, pull today's appointment availability across providers and post a structured summary to **#appointment-availability-update** in Slack.

**Usage:** `/daily-availability-report`

---

## Prerequisites

| MCP Server | Why |
|---|---|
| **Slack** | Posts the report |

Check connected servers with `/mcp`.

---

## Steps

### 1. Determine today's date

Use today's date in `YYYY-MM-DD` format (e.g. `2026-05-17`). This is the reporting date for the availability summary.

### 2. Pull appointment availability data

Search available tools and data sources for today's appointment availability. Depending on what is connected in the session, try in this order:

- If a scheduling or calendar MCP tool is available, use it to list open and booked appointment slots for today.
- If a Google Calendar MCP tool is available, query calendars for providers or clinic resources to find availability.
- If no scheduling tool is connected, report that no scheduling data source is available and stop.

Collect: provider or resource names, total slots, booked slots, open slots, any notable gaps (e.g. no availability after 2 PM) or surpluses.

### 3. Find the Slack channel

Use `mcp__Slack__slack_search_channels` with query `appointment-availability-update` and `channel_types: "public_channel,private_channel"`. Select the channel whose name is `appointment-availability-update`. If not found, try `appointment-availability`.

### 4. Synthesize the report

Produce a concise daily availability snapshot:

- **Headline metric:** overall fill rate for today (booked ÷ total, as a %)
- **Per-provider / per-resource table** (if ≤ 10 entries, inline; otherwise top 5 + bottom 5 by fill rate)
- **Highlights:** any providers fully booked, any with >50% open slots, any last-minute cancellations if detectable
- **Recommendation:** one-line action if warranted (e.g. "3 open slots this afternoon — consider outreach")

If there is no availability data at all (e.g. holiday, no appointments scheduled), say so clearly.

### 5. Post to Slack

Use `mcp__Slack__slack_send_message` to post to the channel found in step 3.

Format:

```
*Appointment Availability — [Day, Month D]* 📅

*Overall fill rate: X%* ([booked] booked / [total] total slots)

---

*Provider / Resource Availability*
| Provider | Open | Booked | Fill % |
|---|---|---|---|
| Name | N | N | N% |
...

---

*Highlights*
- bullet
- bullet

*Recommendation:* one-line suggestion or "No action needed."
```

Keep it scannable — clinic staff should be able to act on it in under 30 seconds.

---

## Tips

- **No scheduling tool connected?** Connect a calendar or scheduling MCP server, or update this skill to pull from your specific data source (e.g. a database query or API call via Bash).
- **Too many providers to list?** Show the 5 most-open and 5 most-booked, with a note of how many total providers were included.
- **Weekend or holiday?** If today has zero slots across all providers, post a brief note rather than an empty table.
