"""
agents/advisor.py
Sub-agent #4 — synthesizes all agent outputs into a human-readable brief.

Uses Google Gemini (gemini-2.5-flash) to generate the narrative.

Responsibility:
  - Receive outputs from Signal Watcher, OKR Tracker, Risk Spotter
  - Use Gemini to write a Situation Brief narrative
  - Produce a prioritized action list
  - Return the final brief to the Orchestrator
"""

import os
from google import genai
from google.genai import types


SYSTEM_PROMPT = """You are the AI Chief of Staff for a startup founder.
You receive structured data from three monitoring agents and produce a concise,
no-fluff Situation Brief — like a morning debrief from a trusted advisor.

Your output format MUST be:

## Situation Brief

### Overall health: [RED / AMBER / GREEN]
One sentence on the overall state of the business right now.

### Top risks (prioritized)
1. [Risk title] — [1-sentence why it matters + specific number/deadline]
2. ...

### OKR pulse
- [KR name]: [X]% — [on track / at risk / off track] ([N] days left)
- ...

### Signals from inbox
- [sender / subject]: [1-line summary]
- ...

### Recommended actions (this week)
1. [Specific action — owner — deadline]
2. ...

Keep each section tight. No filler. Founders are busy."""


async def run(context: dict) -> dict:
    """
    Entry point called by the Orchestrator.
    context must contain: signal_data, okr_data, risk_data, query
    """
    signal_data = context.get("signal_data", {})
    okr_data = context.get("okr_data", {})
    risk_data = context.get("risk_data", {})
    query = context.get("query", "Give me the situation brief.")

    print("[Senior Synthesizer] Generating intelligence brief...")

    # Build the data payload for Gemini
    data_summary = f"""
FOUNDER'S QUERY: {query}

--- SIGNAL WATCHER OUTPUT ---
{signal_data.get('summary', 'No signals.')}

--- OKR TRACKER OUTPUT ---
{okr_data.get('summary', 'No OKR data.')}

--- RISK SPOTTER OUTPUT ---
{risk_data.get('summary', 'No risks.')}

Calendar events in next 30 days:
{_format_events(risk_data.get('calendar_events', []))}
"""

    api_key = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=data_summary,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=1500,
                temperature=0.7,
            ),
        )

        brief_text = response.text
        input_tokens = getattr(response.usage_metadata, 'prompt_token_count', 0) if response.usage_metadata else 0
        output_tokens = getattr(response.usage_metadata, 'candidates_token_count', 0) if response.usage_metadata else 0

        print(f"[Senior Synthesizer] Brief synthesized ({input_tokens} in, {output_tokens} out tokens)")

    except Exception as e:
        print(f"[Senior Synthesizer] Gemini API error: {e}. Using fallback brief.")
        brief_text = _generate_fallback_brief(signal_data, okr_data, risk_data)
        input_tokens = 0
        output_tokens = 0

    return {
        "agent": "advisor",
        "brief": brief_text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


def _generate_fallback_brief(signal_data: dict, okr_data: dict, risk_data: dict) -> str:
    """Generate a structured brief without LLM when API is unavailable."""
    lines = [
        "## Situation Brief\n",
        "### Overall health: AMBER",
        "Multiple items require attention based on current signals and OKR progress.\n",
        "### Top risks (prioritized)",
    ]

    for i, risk in enumerate(risk_data.get("risks", [])[:5], 1):
        lines.append(f"{i}. **{risk['title']}** — {risk.get('description', 'No details')[:100]}")

    lines.append("\n### OKR pulse")
    for okr in okr_data.get("okrs", []):
        lines.append(f"- {okr['key_result']}: {okr['progress_pct']}% — {okr['status']} ({okr['days_left']}d left)")

    lines.append("\n### Signals from inbox")
    for sig in signal_data.get("signals", [])[:5]:
        lines.append(f"- [{sig['sender']}] {sig['subject']}: {sig.get('summary', '')[:80]}")

    lines.append("\n### Recommended actions (this week)")
    lines.append("1. Review high-severity risks and assign owners")
    lines.append("2. Address off-track OKRs with corrective action plans")
    lines.append("3. Respond to unanswered client threads within 24 hours")

    return "\n".join(lines)


def _format_events(events: list) -> str:
    if not events:
        return "  None"
    lines = []
    for e in events:
        lines.append(f"  • {e.get('title')} on {e.get('start_time', '')[:10]}"
                     + (f" — {e.get('note', '')}" if e.get("note") else ""))
    return "\n".join(lines)
