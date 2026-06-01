# ── Groq API ──────────────────────────────────────────────────────────────
GROQ_API_KEY = "OPENAI_API_KEY"   # ← Paste your gsk_... key here
TAVILY_API_KEY = "TAVILY_API_KEY"  # ← paste your Tavily key here
GROQ_MODEL = "llama-3.3-70b-versatile"  # ← best for reasoning# Free, fast, very capable

# ── Data Path ─────────────────────────────────────────────────────────────
DATA_PATH = "data/synthetic_retail_data.xlsx"

# ── Markdown Simulation ───────────────────────────────────────────────────
WEEK_DISCOUNTS = [5, 10, 15, 20]

# ── Inventory Thresholds ──────────────────────────────────────────────────
# Better — more realistic distribution
HIGH_RISK_DAYS   = 730   # 2 years of stock = HIGH
MEDIUM_RISK_DAYS = 365   # 1 year of stock = MEDIUM
DEAD_INVENTORY_DAYS = 365

# ── ABC Classification ────────────────────────────────────────────────────
ABC_A_THRESHOLD = 0.80
ABC_B_THRESHOLD = 0.95

# ── Margin ────────────────────────────────────────────────────────────────
COST_MULTIPLIER       = 0.55
MIN_ACCEPTABLE_MARGIN = 15.0