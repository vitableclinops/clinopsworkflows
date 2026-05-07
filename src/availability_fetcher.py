"""
Fetches daily appointment availability from the configured scheduling source.

Set SCHEDULING_API_URL and SCHEDULING_API_TOKEN in the environment to point
this at your scheduling system.  The endpoint should accept a `date` query
parameter (YYYY-MM-DD) and return JSON.  The key inside the response that
holds the list of available slots is controlled by SCHEDULING_SLOTS_KEY
(default: "slots").

Replace this module's body with the logic from tddaily-availability-report.skill
once that file is available in the repo.
"""

import os
from datetime import date as date_type

import requests


def get_todays_availability(target_date: str | None = None) -> dict:
    """
    Return today's appointment availability.

    Returns a dict with keys:
      date     – ISO date string (YYYY-MM-DD)
      slots    – list of available slot dicts (shape depends on the API)
      raw      – full parsed JSON response from the scheduling API
    """
    today = target_date or date_type.today().isoformat()
    api_url = os.environ.get("SCHEDULING_API_URL")

    if not api_url:
        raise EnvironmentError(
            "SCHEDULING_API_URL is not configured. "
            "Add it to your GitHub Actions repository variables or secrets."
        )

    token = os.environ.get("SCHEDULING_API_TOKEN", "")
    slots_key = os.environ.get("SCHEDULING_SLOTS_KEY", "slots")

    headers: dict[str, str] = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(
        api_url,
        headers=headers,
        params={"date": today},
        timeout=30,
    )
    resp.raise_for_status()

    data = resp.json()
    slots = data.get(slots_key, [])

    return {"date": today, "slots": slots, "raw": data}


def format_availability(report: dict) -> str:
    """
    Convert the raw availability dict into a human-readable summary string.

    Adapt this to match the shape of your scheduling API's slot objects.
    """
    slots = report["slots"]
    if not slots:
        return "No available appointment slots found for today."

    lines = [f"*{len(slots)} slot(s) available on {report['date']}*", ""]
    for slot in slots:
        if isinstance(slot, dict):
            time = slot.get("time") or slot.get("start_time") or slot.get("datetime", "")
            site = slot.get("site") or slot.get("location") or slot.get("provider", "")
            label = f"• {time}" + (f" — {site}" if site else "")
        else:
            label = f"• {slot}"
        lines.append(label)

    return "\n".join(lines)
