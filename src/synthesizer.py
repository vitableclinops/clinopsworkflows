"""Uses Claude to parse Granola's meeting summary into structured action items."""

import json
import os

import anthropic

MODEL = "claude-sonnet-4-6"

# Stable system prompt — cached to save tokens on repeated Tuesday runs.
_SYSTEM = """\
You are a clinical operations assistant. You will receive the AI-generated summary \
from a Granola meeting note for a ClinOps Weekly Sync.

Your job:
1. Write a 2–4 sentence high-level recap of the key topics discussed and decisions made.
2. Extract every action item from the "Next Steps" section (or equivalent) and group them \
by the person responsible. Use the exact first name or full name as it appears in the notes.
   - If an item is assigned to the whole team, use "Team" as the key.
   - Each action item must start with an action verb.

Return ONLY valid JSON — no markdown fences, no extra text:
{
  "summary": "<2-4 sentence recap>",
  "action_items": {
    "Person Name": ["Do X by Friday", "Follow up with Y"],
    "Another Person": ["Schedule Z call"]
  }
}"""


def extract_action_items(meeting: dict) -> dict:
    """
    Parse meeting['summary'] with Claude.
    Returns {"summary": str, "action_items": {name: [str]}}.
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": _SYSTEM,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    f"Meeting: {meeting['title']}\n"
                    f"Date: {meeting['date']}\n\n"
                    f"{meeting['summary']}"
                ),
            }
        ],
    )

    raw = response.content[0].text.strip()
    return json.loads(raw)
