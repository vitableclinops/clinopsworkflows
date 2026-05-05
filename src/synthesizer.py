"""
Uses the Claude API to synthesize Granola meeting notes into a structured
summary and per-person action items.

Prompt caching is applied to the static system prompt so repeated runs
(e.g. retries) don't re-bill the same tokens.
"""

import json
import logging
import os
import re

import anthropic

log = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-6"

_SYSTEM = """\
You are an assistant that processes clinical operations meeting notes.
Given raw meeting notes, produce:
1. A concise narrative summary (2–4 sentences) of what was discussed.
2. A list of action items grouped by the person responsible.

Return ONLY a JSON object with this exact shape — no prose, no markdown fences:
{
  "summary": "<narrative summary>",
  "action_items": {
    "<Person Name>": ["<action item>", ...],
    ...
  }
}

Rules:
- Include only people who have at least one action item.
- If an action item has no clear owner, use the key "Team".
- Action items must be complete, self-contained sentences.
- Do not invent information not present in the notes.
"""


def extract_action_items(meeting: dict) -> dict:
    """
    Call Claude to synthesize meeting['summary'] into:
      {"summary": str, "action_items": {name: [str]}}
    """
    raw = meeting.get("summary", "").strip()
    if not raw:
        return {"summary": "", "action_items": {}}

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
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
                    f"Meeting: {meeting.get('title', 'ClinOps Weekly Sync')}\n"
                    f"Date: {meeting.get('date', '')}\n"
                    f"Participants: {', '.join(meeting.get('participants', []))}\n\n"
                    f"Notes:\n{raw}"
                ),
            }
        ],
    )

    text = message.content[0].text.strip()

    # Strip markdown code fences if the model adds them despite instructions
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        log.error("Claude returned non-JSON: %s", text[:200])
        raise RuntimeError(f"Synthesis failed — bad JSON from Claude: {exc}") from exc

    return {
        "summary": parsed.get("summary", ""),
        "action_items": parsed.get("action_items", {}),
    }
