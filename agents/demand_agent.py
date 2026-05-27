# import pandas as pd
# from agents.llm_caller import call_gemini, parse_field
# from utils.prompt_builder import build_demand_prompt

# def run_demand_agent(sku: pd.Series, discount_pct: float, week: int) -> dict:
#     """
#     Call Gemini with demand prompt for one week simulation.
#     Returns revenue forecast, demand uplift, velocity change.
#     """
#     prompt   = build_demand_prompt(sku, discount_pct, week)
#     response = call_gemini(prompt)

#     price     = sku.get("price", 0)
#     new_price = round(price * (1 - discount_pct / 100), 2)
#     velocity  = sku.get("sales_velocity", 0)

#     # ── Parse Gemini response ──────────────────────────────────────────────
#     revenue_forecast = parse_field(response, "REVENUE_FORECAST", as_float=True)
#     demand_uplift    = parse_field(response, "DEMAND_UPLIFT",    as_float=True)
#     velocity_new     = parse_field(response, "VELOCITY_NEW",     as_float=True)
#     revenue_change   = parse_field(response, "REVENUE_CHANGE",   as_float=True)
#     summary          = parse_field(response, "SUMMARY",          as_float=False)

#     # ── Fallback calculation if Gemini gives 0 ────────────────────────────
#     if demand_uplift == 0.0:
#         demand_uplift = round(discount_pct * 1.5, 1)  # 1.5x uplift per % discount

#     if velocity_new == 0.0:
#         uplift_factor = 1 + (demand_uplift / 100)
#         velocity_new  = round(velocity * uplift_factor, 4)

#     if revenue_forecast == 0.0:
#         units_per_week   = velocity_new * 7
#         revenue_forecast = round(units_per_week * new_price, 2)

#     if revenue_change == 0.0:
#         baseline_revenue = round(velocity * 7 * price, 2)
#         revenue_change   = round(revenue_forecast - baseline_revenue, 2)

#     return {
#         "week":             week,
#         "discount_pct":     discount_pct,
#         "new_price":        new_price,
#         "revenue_forecast": round(revenue_forecast, 2),
#         "demand_uplift":    round(demand_uplift, 1),
#         "velocity_new":     round(velocity_new, 4),
#         "revenue_change":   round(revenue_change, 2),
#         "summary":          summary,
#         "raw_response":     response,
#     }



import pandas as pd
from agents.llm_caller import call_gemini, parse_field

def run_demand_agent(sku: pd.Series, markdown_pct: float) -> dict:
    price     = sku.get("price", 0)
    new_price = round(price * (1 - markdown_pct / 100), 2)
    velocity  = float(sku.get("sales_velocity", 0))
    baseline_revenue = round(velocity * 7 * price, 4)

    prompt = f"""You are a Demand Forecasting Agent in a retail markdown optimization system.

PRODUCT DATA:
- SKU: {sku.get('product_id')} | {sku.get('product_name')}
- Category: {sku.get('main_category')} | ABC Class: {sku.get('abc_class', 'C')}
- Original Price: ${price:.2f} | New Price after {markdown_pct}% markdown: ${new_price:.2f}
- Current Sales Velocity: {velocity:.6f} units/day (BEFORE markdown)
- Baseline Weekly Revenue (no markdown): ${baseline_revenue:.4f}
- Sell-Through Rate: {sku.get('sell_through_rate', 0):.1f}%
- Clearance Risk: {sku.get('clearance_risk', 'LOW')}

YOUR TASK:
Forecast demand and revenue impact of this {markdown_pct}% markdown for the next 7 days.
Consider price elasticity — how much will demand realistically increase?
Be specific with numbers based on the actual velocity and price data given.

Respond ONLY in this exact format:
DEMAND_UPLIFT: [% increase in demand due to markdown — realistic number]
NEW_VELOCITY: [new units per day after markdown as decimal]
UNITS_WEEK: [units expected to sell in 7 days]
REVENUE_FORECAST: [weekly revenue in dollars at new price]
REVENUE_CHANGE: [revenue change vs baseline — can be negative]
SUMMARY: [1 sentence — your expert assessment of revenue impact]
"""

    response = call_gemini(prompt)

    demand_uplift    = parse_field(response, "DEMAND_UPLIFT",    as_float=True)
    new_velocity     = parse_field(response, "NEW_VELOCITY",     as_float=True)
    units_week       = parse_field(response, "UNITS_WEEK",       as_float=True)
    revenue_forecast = parse_field(response, "REVENUE_FORECAST", as_float=True)
    revenue_change   = parse_field(response, "REVENUE_CHANGE",   as_float=True)
    summary          = parse_field(response, "SUMMARY",          as_float=False)

    # Only fallback if Groq completely fails
    if demand_uplift == 0.0:
        demand_uplift = round(markdown_pct * 2.0, 1)
    if new_velocity == 0.0:
        new_velocity = round(velocity * (1 + demand_uplift / 100), 6)
    if units_week == 0.0:
        units_week = max(1, round(new_velocity * 7))
    if revenue_forecast == 0.0:
        revenue_forecast = round(units_week * new_price, 2)
    if revenue_change == 0.0:
        revenue_change = round(revenue_forecast - baseline_revenue, 4)
    if not summary:
        summary = f"At {markdown_pct}% markdown, weekly revenue is ${revenue_forecast:.2f} vs baseline ${baseline_revenue:.4f}."

    return {
        "demand_uplift":    round(demand_uplift, 1),
        "new_velocity":     round(new_velocity, 6),
        "units_week":       int(units_week),
        "revenue_forecast": round(revenue_forecast, 2),
        "revenue_change":   round(revenue_change, 2),
        "summary":          summary,
        "raw_response":     response,
    }