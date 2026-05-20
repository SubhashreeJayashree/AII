# config.py -- project configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Toggle whether to use the LLM translator / LLM safety check
USE_LLM_TRANSLATOR = os.getenv("USE_LLM_TRANSLATOR", "false").lower() in ("1","true","yes")
USE_LLM_SAFETY = os.getenv("USE_LLM_SAFETY", "false").lower() in ("1","true","yes")

# OpenAI / LLM config (if used)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # change to model you have access to

# Safety thresholds (tunable)
SAFETY_SCORE_THRESHOLD = float(os.getenv("SAFETY_SCORE_THRESHOLD", "2.0"))

# Database path (optional logging)
DB_PATH = os.getenv("DB_PATH", "commands.db")
