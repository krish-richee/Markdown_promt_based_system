"""
utils/history_manager.py
Saves and loads markdown decisions to/from a local JSON file.
"""
import json
import os
from datetime import datetime

HISTORY_FILE = "data/decision_history.json"

def save_decision(sku: dict, result: dict):
    """Save one markdown decision to history."""
    os.makedirs("data", exist_ok=True)

    record = {
        "timestamp"         : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "product_id"        : str(sku.get("product_id", "")),
        "product_name"      : str(sku.get("product_name", "")),
        "category"          : str(sku.get("main_category", "")),
        "original_price"    : float(sku.get("price", 0)),
        "recommended_markdown": float(result.get("recommended_markdown", 0)),
        "new_price"         : float(result.get("new_price", 0)),
        "strategy"          : str(result.get("strategy", "")),
        "confidence"        : float(result.get("confidence", 0)),
        "risk_level"        : str(result.get("risk_level", "")),
        "reasoning"         : str(result.get("reasoning", "")),
        "margin_after"      : float(result.get("pricing", {}).get("margin_after", 0)),
        "revenue_forecast"  : float(result.get("demand", {}).get("revenue_forecast", 0)),
        "days_to_clear"     : str(result.get("inventory", {}).get("days_to_clear", "")),
    }

    history = load_all()
    # Avoid duplicate — if same product decided in last 5 min, skip
    if history:
        last = history[-1]
        if last["product_id"] == record["product_id"] and last["timestamp"][:16] == record["timestamp"][:16]:
            return

    history.append(record)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def load_all() -> list:
    """Load all saved decisions."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def clear_history():
    """Delete all history."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)