"""
Daily Availability Report — invoke the send-ops-dashboard-slack Supabase edge function.

Triggered by GitHub Actions every weekday at 8:00 AM America/Chicago.
Steps:
  1. POST to send-ops-dashboard-slack edge function.
  2. Log the coverage counts and attention states.
  3. Exit non-zero on any failure so GitHub Actions marks the run red.
"""

import json
import logging
import os
import sys

import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

FUNCTION_NAME = "send-ops-dashboard-slack"


def main() -> None:
    supabase_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    supabase_anon_key = os.environ.get("SUPABASE_ANON_KEY", "")
    dry_run = os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes")
    override_date = os.environ.get("REPORT_DATE") or None

    if not supabase_url:
        log.error("SUPABASE_URL is not set.")
        sys.exit(1)
    if not supabase_anon_key:
        log.error("SUPABASE_ANON_KEY is not set.")
        sys.exit(1)

    endpoint = f"{supabase_url}/functions/v1/{FUNCTION_NAME}"
    payload: dict = {}
    if dry_run:
        payload["dry_run"] = True
    if override_date:
        payload["date"] = override_date

    log.info("Invoking %s (dry_run=%s, date=%s)", FUNCTION_NAME, dry_run, override_date or "today")

    resp = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {supabase_anon_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )

    try:
        data = resp.json()
    except Exception:
        log.error("Non-JSON response (HTTP %s): %s", resp.status_code, resp.text[:500])
        sys.exit(1)

    if not resp.ok or not data.get("success"):
        log.error("Function returned error (HTTP %s): %s", resp.status_code, json.dumps(data))
        sys.exit(1)

    counts = data.get("counts", {})
    log.info(
        "Report sent. %d active states — 🟢 %d OK · 🟡 %d LOW · 🟠 %d CRITICAL · 🔴 %d ZERO · ⚪ %d NO DATA",
        counts.get("total", "?"),
        counts.get("ok", "?"),
        counts.get("low", "?"),
        counts.get("critical", "?"),
        counts.get("zero", "?"),
        counts.get("noData", "?"),
    )
    if data.get("attention_count", 0) > 0:
        log.info("%d state(s) need attention today.", data["attention_count"])
    if dry_run:
        log.info("DRY RUN — Slack message was NOT posted.")
    else:
        log.info("Slack message posted (ts=%s).", data.get("message_ts", "unknown"))

    log.info("Done.")


if __name__ == "__main__":
    main()
