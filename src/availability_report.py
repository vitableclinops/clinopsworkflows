"""
Daily Appointment Availability Report.

Triggered by GitHub Actions every weekday morning.
Steps:
  1. Fetch today's available appointment slots from the scheduling API.
  2. Format a human-readable summary.
  3. Post the summary to Slack #appointment-availability-update.
"""

import logging
import os
import sys

from availability_fetcher import format_availability, get_todays_availability
from slack_client import post_availability_report

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def main() -> None:
    target_date = os.environ.get("WORKFLOW_DATE") or None
    log.info(
        "Starting daily availability report (date=%s)", target_date or "today"
    )

    log.info("Fetching appointment availability...")
    report = get_todays_availability(target_date)
    slot_count = len(report["slots"])
    log.info("Found %d available slot(s) for %s", slot_count, report["date"])

    summary = format_availability(report)

    log.info("Posting availability report to Slack...")
    post_availability_report(report, summary)
    log.info("Posted to #appointment-availability-update")

    log.info("Done.")


if __name__ == "__main__":
    main()
