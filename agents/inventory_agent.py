# """
# inventory_agent.py — FIXED
# Bug fixed: round(tiny_float, 0) → 0 for slow-moving products
#            use math.ceil so even 0.001 velocity products get at least 1 unit
# """
# import math
# import pandas as pd
# from agents.llm_caller import call_gemini, parse_field
# from utils.prompt_builder import build_inventory_prompt


# def run_inventory_agent(sku: pd.Series, discount_pct: float, week: int) -> dict:
#     prompt   = build_inventory_prompt(sku, discount_pct, week)
#     response = call_gemini(prompt)

#     stock    = float(sku.get("quantity", 0))
#     velocity = float(sku.get("sales_velocity", 0))

#     # Parse Gemini response
#     units_sold_forecast = parse_field(response, "UNITS_SOLD_FORECAST", as_float=True)
#     stock_remaining     = parse_field(response, "STOCK_REMAINING",     as_float=True)
#     days_to_clear       = parse_field(response, "DAYS_TO_CLEAR",       as_float=True)
#     velocity_change     = parse_field(response, "VELOCITY_CHANGE",     as_float=True)
#     summary             = parse_field(response, "SUMMARY",             as_float=False)

#     # ── BUG FIX: use math.ceil so slow products always get > 0 units ──────
#     # Old code: round(velocity * 7 * uplift, 0) → 0.0 for velocities < 0.07
#     # New code: math.ceil ensures minimum 1 unit if velocity > 0
#     if units_sold_forecast == 0.0 or units_sold_forecast < 0.5:
#         uplift_factor       = 1 + (discount_pct / 100) * 2   # e.g. 5% disc → 1.10x
#         raw_units           = velocity * 7 * uplift_factor
#         # ceil: 0.023 → 1, 1.4 → 2, 5.7 → 6  (always at least 1 if velocity>0)
#         units_sold_forecast = math.ceil(raw_units) if raw_units > 0 else 0

#     if velocity_change == 0.0 or velocity_change < 1e-6:
#         uplift_factor   = 1 + (discount_pct / 100) * 2
#         velocity_change = round(velocity * uplift_factor, 6)

#     if stock_remaining == 0.0:
#         stock_remaining = max(0, stock - units_sold_forecast)

#     if days_to_clear == 0.0:
#         days_to_clear = (
#             round(stock_remaining / velocity_change, 0)
#             if velocity_change > 0 else 9999
#         )

#     return {
#         "week"               : week,
#         "discount_pct"       : discount_pct,
#         "units_sold_forecast": int(units_sold_forecast),
#         "stock_remaining"    : int(max(0, stock_remaining)),
#         "days_to_clear"      : int(min(days_to_clear, 9999)),
#         "velocity_change"    : round(velocity_change, 6),
#         "summary"            : summary,
#         "raw_response"       : response,
#     }




import pandas as pd
from agents.llm_caller import call_gemini, parse_field

def run_inventory_agent(sku: pd.Series, markdown_pct: float) -> dict:
    price    = sku.get("price", 0)
    new_price = round(price * (1 - markdown_pct / 100), 2)
    stock    = int(sku.get("quantity", 0))
    velocity = float(sku.get("sales_velocity", 0))
    days_of_stock = min(float(sku.get("days_of_stock", 9999)), 9999)

    prompt = f"""You are an Inventory Agent in a retail markdown optimization system.

PRODUCT DATA:
- SKU: {sku.get('product_id')} | {sku.get('product_name')}
- Category: {sku.get('main_category')}
- Current Stock: {stock} units
- Current Price: ${price:.2f} → New Price after markdown: ${new_price:.2f}
- Markdown Applied: {markdown_pct}%
- Current Sales Velocity: {velocity:.6f} units/day (BEFORE markdown)
- Days of Stock at Current Rate: {days_of_stock:.0f} days
- Clearance Risk: {sku.get('clearance_risk', 'LOW')}
- Dead Inventory: {sku.get('is_dead_inventory', False)}
- Sell-Through Rate: {sku.get('sell_through_rate', 0):.1f}%

YOUR TASK:
Based on the {markdown_pct}% markdown applied, forecast realistic inventory movement for 7 days.
Consider: how much will demand increase due to this price drop? How many units will actually sell?
Be realistic — if velocity is very low, a small markdown won't move hundreds of units.

Respond ONLY in this exact format (integers only, no units or symbols):
UNITS_SOLD_7DAYS: [realistic integer — how many units will sell in 7 days at new price]
STOCK_REMAINING: [stock after 7 days sales]
DAYS_TO_CLEAR: [days to clear ALL remaining stock at new velocity]
NEW_VELOCITY: [new units per day after markdown as decimal]
SUMMARY: [1 sentence — your expert assessment of stock movement at this markdown]
"""

    response = call_gemini(prompt)

    units_sold    = parse_field(response, "UNITS_SOLD_7DAYS", as_float=True)
    stock_rem     = parse_field(response, "STOCK_REMAINING",  as_float=True)
    days_to_clear = parse_field(response, "DAYS_TO_CLEAR",    as_float=True)
    new_velocity  = parse_field(response, "NEW_VELOCITY",     as_float=True)
    summary       = parse_field(response, "SUMMARY",          as_float=False)

    # Only fallback if Groq completely fails
    if units_sold == 0.0:
        uplift     = 1 + (markdown_pct / 100) * 2.5
        units_sold = max(1, round(velocity * 7 * uplift)) if velocity > 0 else 1

    if new_velocity == 0.0:
        new_velocity = round(units_sold / 7, 6)

    if stock_rem == 0.0:
        stock_rem = max(0, stock - int(units_sold))

    if days_to_clear == 0.0:
        days_to_clear = round(stock_rem / new_velocity) if new_velocity > 0 else 9999

    if not summary:
        summary = f"At {markdown_pct}% markdown, {int(units_sold)} units sell in 7 days leaving {int(stock_rem)} in stock."

    return {
        "units_sold_7days": int(units_sold),
        "stock_remaining":  int(max(0, stock_rem)),
        "days_to_clear":    int(min(days_to_clear, 9999)),
        "new_velocity":     round(new_velocity, 6),
        "summary":          summary,
        "raw_response":     response,
    }