---
name: daily-availability-report
description: Pulls today's appointment availability data and posts a summary to #appointment-availability-update in Slack.
usage: /daily-availability-report
---

# Daily Appointment Availability Report

<!--
  PASTE THE BODY OF tddaily-availability-report.skill BELOW THIS LINE.
  Replace everything between the two comment markers with the skill content.
-->

<!-- SKILL BODY START -->

<!-- SKILL BODY END -->

---

## Final step: Post to Slack

After completing the steps above, use `mcp__Slack__slack_search_channels` to locate the
`#appointment-availability-update` channel, then post the availability summary using
`mcp__Slack__slack_send_message`.

Format the message as:

**Appointment Availability Update — [today's date]**

[Availability summary content from the skill steps above]

---
_This report runs automatically every weekday at 8 AM CT._
