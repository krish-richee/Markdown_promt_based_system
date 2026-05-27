# ── Groq API ──────────────────────────────────────────────────────────────
GROQ_API_KEY = "OPENAI_API_KEY"   # ← Paste your gsk_... key here
GROQ_MODEL   = "llama-3.3-70b-versatile"  # Free, fast, very capable

# ── Data Path ─────────────────────────────────────────────────────────────
DATA_PATH = "data/synthetic_retail_data.xlsx"

# ── Markdown Simulation ───────────────────────────────────────────────────
WEEK_DISCOUNTS = [5, 10, 15, 20]

# ── Inventory Thresholds ──────────────────────────────────────────────────
HIGH_RISK_DAYS      = 180
MEDIUM_RISK_DAYS    = 90
DEAD_INVENTORY_DAYS = 365

# ── ABC Classification ────────────────────────────────────────────────────
ABC_A_THRESHOLD = 0.80
ABC_B_THRESHOLD = 0.95

# ── Margin ────────────────────────────────────────────────────────────────
COST_MULTIPLIER       = 0.55
MIN_ACCEPTABLE_MARGIN = 15.0