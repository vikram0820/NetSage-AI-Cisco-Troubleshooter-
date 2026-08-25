from dotenv import load_dotenv
load_dotenv()

import os
import json

MODEL = os.getenv("NETSAGE_MODEL", "gemini-3.5-flash-lite")

def ai_available():
    return bool(os.getenv("GEMINI_API_KEY"))

def ai_diagnose(case):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
You are NetSage AI, an evidence-grounded Cisco network troubleshooting assistant.

Analyze ONLY the supplied Cisco Packet Tracer/lab evidence.

CASE ID:
{case["case_id"]}

SYMPTOM:
{case["symptom"]}

TOPOLOGY NOTE:
{case["topology_note"]}

SHOW-COMMAND OUTPUT:
{case["show_outputs"]}

EXPECTED FAULT FOR INTERNAL EVALUATION:
{case["expected_fault"]}

TASK:
1. Identify the most likely root cause.
2. Map it to the OSI layer.
3. Give a confidence level.
4. Quote or reference actual supplied evidence.
5. Give the safest next diagnostic command.
6. Give proposed Cisco CLI fix steps only when evidence supports them.

SAFETY:
- Never invent evidence.
- Never claim a command was executed.
- Never connect to or modify a real device.
- If evidence is insufficient, explicitly say so.
- Human review is mandatory before accepting any fix.
"""

    schema = {
        "type": "OBJECT",
        "properties": {
            "root_cause": {"type": "STRING"},
            "osi_layer": {"type": "STRING"},
            "confidence": {"type": "STRING"},
            "evidence": {"type": "ARRAY", "items": {"type": "STRING"}},
            "next_command": {"type": "STRING"},
            "fix_steps": {"type": "ARRAY", "items": {"type": "STRING"}}
        },
        "required": [
            "root_cause", "osi_layer", "confidence",
            "evidence", "next_command", "fix_steps"
        ]
    }

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0.2
        )
    )

    return json.loads(response.text)
