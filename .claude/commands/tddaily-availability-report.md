---
name: tddaily-availability-report
description: Pull today's appointment availability data from Jotform, summarize open and booked slots, and post a daily availability update to #appointment-availability-update in Slack.
usage: /tddaily-availability-report
examples:
  - /tddaily-availability-report
prerequisites:
  - Jotform MCP server
  - Slack MCP server
---

# Daily Appointment Availability Report

Pull today's appointment availability data from Jotform, summarize open and booked slots, and post a concise daily update to the `#appointment-availability-update` Slack channel.

**Usage:** `/tddaily-availability-report`

---

## Prerequisites

| MCP Server | Why |
|---|---|
| **Jotform** | Reads appointment form submissions and availability |
| **Slack** | Posts the daily availability update |

---

## Steps

### 1. Find the appointment forms in Jotform

Use `mcp__Jotform__search` to locate appointment scheduling forms. Good search terms: "appointment", "scheduling", "availability", "booking". If multiple forms are found, include all that appear to be active appointment intake or scheduling forms.

### 2. Pull today's submissions

For each form found in step 1, use `mcp__Jotform__list_submissions` to retrieve submissions. Filter to today's date only.

Count:
- **Total submissions today** — all entries regardless of status
- **New / pending** — submissions awaiting confirmation or review
- **Confirmed / booked** — appointments that have been accepted
- **Cancelled / declined** — any that were cancelled today

If date filtering is not available on the submissions endpoint, fetch recent submissions and filter by submission date in the results.

### 3. Check overall availability

Identify if any forms expose available slot counts (e.g., via form fields or metadata). If slot data is available, note:
- Total slots available for today
- Slots remaining
- Any forms/clinics at capacity

If slot-level data is not available from Jotform, report on submission volume and status breakdown only.

### 4. Find the Slack channel

Use `mcp__Slack__slack_search_channels` with query `appointment-availability-update` and `channel_types: "public_channel,private_channel"`. Use the exact channel `#appointment-availability-update`.

### 5. Format the daily report

Compose a concise Slack message in the following format:

```
📅 *Daily Appointment Availability Update — [Today's Date]*

*Submissions Today*
• Total: [N]
• New / Pending: [N]
• Confirmed: [N]
• Cancelled: [N]

*By Form / Clinic*
[For each appointment form:]
• [Form Name]: [N confirmed] booked, [N pending] pending[, [N] slots remaining if available]

[If any form is at capacity:]
⚠️ *[Form Name]* is at capacity for today.

[If no submissions:]
No appointment submissions recorded for today.
```

Keep the message factual and brief. Do not include personally identifiable information from submissions.

### 6. Post to Slack

Use `mcp__Slack__slack_send_message` to post the formatted message to `#appointment-availability-update`.

---

## Tips

- **No submissions today?** Post the update anyway noting zero activity — the absence of data is itself useful signal.
- **Multiple appointment forms?** Aggregate into a single message with a per-form breakdown.
- **Can't access the channel?** Check that the Slack bot has been added to `#appointment-availability-update`. Ask a channel admin to invite it with `/invite @[bot-name]`.
- **Jotform API errors?** Retry once. If still failing, post to Slack noting the data source is unavailable so the team knows the report couldn't run.
