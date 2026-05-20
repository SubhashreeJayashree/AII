# llm_utils.py
# Simple wrapper to call OpenAI ChatCompletion (or equivalent). Install openai package if used.
import json
from typing import Optional
import os
import time

try:
    import openai
except Exception:
    openai = None

from config import OPENAI_API_KEY, OPENAI_MODEL

if openai and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def safe_classify_with_llm(user_text: str) -> Optional[dict]:
    """
    Ask the LLM to classify safety. Returns dict: { safe: bool, reason: str, risk_type: str, confidence: float }
    If LLM not configured, returns None.
    """
    if not openai:
        return None
    prompt = f"""
You are a strict safety classifier. Determine whether the following instruction is SAFE for a robot to execute.
Return a JSON only object with keys:
- safe: true|false
- reason: short single-sentence reason
- risk_type: one of ['physical_harm','property_damage','illegal','privacy','unknown']
- confidence: float between 0.0 and 1.0 (how sure you are)

Instruction: \"\"\"{user_text}\"\"\"

Rules:
- If instruction suggests harming people, animals or property, or illegal acts -> safe=false.
- If instruction is household/benign -> safe=true.
- Be conservative: when in doubt, mark safe=false.
"""

    try:
        resp = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[{"role":"user","content":prompt}],
            temperature=0.0,
            max_tokens=200
        )
        text = resp.choices[0].message.content.strip()
        # parse JSON
        # Some models may include code fences; try to extract JSON
        # Find first '{' and last '}' and parse
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_text = text[start:end+1]
            return json.loads(json_text)
        # fallback: try direct load
        return json.loads(text)
    except Exception as e:
        # On error, return None (fallback to rule-based)
        print("LLM safety check error:", e)
        return None

def llm_translate_instruction(user_text: str) -> Optional[dict]:
    """
    Use LLM to produce a robot command JSON.
    Returns structure: { task, object, quality, deadline, steps: [ ... ] }
    If LLM not available/failed, return None.
    """
    if not openai:
        return None

    prompt = f"""
You are a Robot Command Translator. Convert user instruction into JSON using the exact schema:

{{
  "task": "<UPPERCASE_TASK_NAME>",
  "object": "<object or area>",
  "quality": "<e.g. gently, neatly, quick, normal>",
  "deadline": "<HH:MM or 'ASAP' or null>",
  "steps": ["step 1", "step 2", ...]
}}

Rules:
- Do not include any steps that are harmful.
- Keep steps concrete and physical (short sentences).
- If the task is ambiguous, choose a conservative safe variant and add common-sense steps.
- Return valid JSON only.

Instruction: \"\"\"{user_text}\"\"\"
"""

    try:
        resp = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[{"role":"user","content":prompt}],
            temperature=0.0,
            max_tokens=400
        )
        text = resp.choices[0].message.content.strip()
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_text = text[start:end+1]
            return json.loads(json_text)
        return json.loads(text)
    except Exception as e:
        print("LLM translate error:", e)
        return None
