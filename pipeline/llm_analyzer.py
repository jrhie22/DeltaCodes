from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_diff(diff: dict, old_text: str, new_text: str) -> dict:
    """
    Send the diff + surrounding policy context to Gemini.
    Claude classifies changes, flags ambiguities, writes a summary.
    """
    prompt = f"""
You are a healthcare policy analyst reviewing CPT/CMS policy changes.

Here is a structured diff between two policy versions:
{json.dumps(diff, indent=2)}

Here is a snippet of the OLD policy text (first 3000 chars):
{old_text}

Here is a snippet of the NEW policy text (first 3000 chars):
{new_text}

Return a JSON object with this exact structure:
{{
  "summary": "2-3 sentence plain English summary of what changed",
  "classified_changes": [
    {{
      "code": "string or null",
      "change_type": "added|deleted|unit_limit_changed|payment_rate_changed|coverage_language_changed|effective_date_changed|modifier_changed",
      "description": "plain English description",
      "confidence": "high|medium|low",
      "impact": "high|medium|low"
    }}
  ],
  "ambiguities": [
    {{
      "text": "the ambiguous clause",
      "reason": "why a human must review this"
    }}
  ],
  "review_status": "auto_approved|human_review_required|escalate_immediately",
  "analyst_notes": "anything the reviewing analyst should pay special attention to"
}}

Return ONLY valid JSON. No preamble, no markdown fences.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,          
            response_mime_type="application/json",  
            max_output_tokens=1500,
        )
    )

    
    raw = response.text
    return json.loads(raw)