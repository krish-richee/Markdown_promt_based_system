import requests
import time
import re
from config.settings import GROQ_API_KEY, GROQ_MODEL

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_gemini(prompt: str, retries: int = 3) -> str:
    """
    Call Groq API (same function name kept so no other files need changing).
    Uses OpenAI-compatible format.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model":       GROQ_MODEL,
        "messages":    [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens":  1024,
    }

    for attempt in range(retries):
        try:
            response = requests.post(GROQ_URL, headers=headers,
                                     json=payload, timeout=30)

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]

            elif response.status_code == 429:
                wait_time = 10 * (attempt + 1)
                print(f"Rate limit. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            else:
                if attempt < retries - 1:
                    time.sleep(3)
                    continue
                return f"ERROR: HTTP {response.status_code} — {response.text[:200]}"

        except requests.exceptions.Timeout:
            if attempt < retries - 1:
                time.sleep(3)
            else:
                return "ERROR: Request timed out"

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(3)
            else:
                return f"ERROR: {str(e)}"

    return "ERROR: Max retries exceeded"


def parse_field(text: str, field: str, as_float: bool = False):
    """
    Extract field from LLM response.
    Handles bold (**FIELD:**), normal (FIELD:), and extra spaces.
    """
    pattern = rf"\*{{0,2}}{field}\*{{0,2}}\s*:?\*{{0,2}}\s*([^\n]+)"
    match   = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return 0.0 if as_float else ""

    raw = match.group(1).strip()
    raw = raw.replace("**", "").replace("$", "").replace("%", "")
    raw = raw.replace(",", "").replace("*", "").strip()
    raw = raw.split()[0] if raw.split() else raw

    if as_float:
        try:
            return float(raw)
        except ValueError:
            return 0.0
    return raw