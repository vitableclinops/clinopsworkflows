---
name: daily-availability-report
description: Check today's appointment availability across HubSpot and post a formatted status update to the #appointment-availability-update Slack channel.
usage: /daily-availability-report
examples:
  - /daily-availability-report
prerequisites:
  - HubSpot MCP server
  - Slack MCP server
---

# Daily Appointment Availability Report

Check today's appointment availability and post a formatted status update to #appointment-availability-update in Slack.

**Usage:** `/daily-availability-report`

---

## Prerequisites

| MCP Server | Why |
|---|---|
| **HubSpot** | Pulls today's scheduled appointments and open slots |
| **Slack** | Posts the availability update |

Check connected servers with `/mcp`. To add one, go to **Settings → MCP Servers** in Claude Code or edit `~/.claude/mcp.json`.

---

## Steps

### 1. Fetch today's appointments from HubSpot

Use `mcp__HubSpot__search_crm_objects` to find all meetings/appointments scheduled for today.

- Object type: `meetings` (or `appointments` if configured)
- Filter: `hs_meeting_start_time` between start-of-today and end-of-today (ISO 8601 UTC)
- Properties to retrieve: `hs_meeting_title`, `hs_meeting_start_time`, `hs_meeting_end_time`, `hs_attendee_owner_ids`, `hs_meeting_outcome`, `hubspot_owner_id`

If the search returns no results, also try `mcp__HubSpot__get_crm_objects` with the same date filter.

### 2. Fetch owner / provider names

For each unique `hubspot_owner_id` returned, call `mcp__HubSpot__search_owners` to resolve the owner's full name. Deduplicate — only look up each owner once.

### 3. Classify availability

Group the appointments into three buckets:

| Bucket | Criteria |
|---|---|
| **Booked** | `hs_meeting_outcome` is `SCHEDULED` or `COMPLETED` |
| **Cancelled / Open** | `hs_meeting_outcome` is `CANCELLED`, `NO_SHOW`, or outcome is empty/null |
| **Pending Confirmation** | `hs_meeting_outcome` is `RESCHEDULED` or contains "pending" |

Compute:
- Total slots today
- Slots booked
- Slots open (cancelled + unset)
- Fill rate: `booked / total × 100` (round to nearest integer)

### 4. Find the Slack channel

Use `mcp__Slack__slack_search_channels` with query `appointment-availability-update`, type `public_channel,private_channel`. Pick the exact match `#appointment-availability-update`.

### 5. Post the update to Slack

Use `mcp__Slack__slack_send_message` to post to `#appointment-availability-update`.

Format:

```
*Daily Appointment Availability — [Weekday, Month D]*

*Fill Rate:* [N]% ([booked] booked / [total] total slots)

*Open Slots ([count])*
- [Time] — [Provider Name] _(cancelled / no-show / unconfirmed)_
- ...

*Booked ([count])*
- [Time] — [Provider Name]
- ...

*Pending Confirmation ([count])*
- [Time] — [Provider Name]
- ...
```

If there are zero open slots, lead with:
`:white_check_mark: *Fully booked!* All [N] slots are filled for today.`

If total slots is zero (no appointments found), post:
`:information_source: No appointments found in HubSpot for today ([date]). Verify the HubSpot pipeline or check if appointments are tracked under a different object type.`

---

## Tips

- **No meetings object in HubSpot?** The org may use `deals` or a custom object for appointments. Ask the workspace admin which object type tracks patient/client appointments and update step 1.
- **Owner IDs not resolving?** Use `mcp__HubSpot__get_user_details` as a fallback to look up by user ID.
- **Private channel access denied?** Have a Slack admin add the bot to `#appointment-availability-update`.
- **Running in CI (no interactive session)?** The GitHub Actions workflow passes `--dangerously-skip-permissions`; ensure the HubSpot and Slack tokens are set as repo secrets `HUBSPOT_ACCESS_TOKEN` and `SLACK_BOT_TOKEN`.
