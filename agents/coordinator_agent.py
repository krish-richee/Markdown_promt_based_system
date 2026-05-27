# """
# coordinator_agent.py — FIXED
# Bug fixed:
#   - Coordinator banner showing 0.0% and $0.00 because:
#     (a) parse_field returned 0.0 when Gemini echoed bracket examples
#     (b) Now prompt_builder pre-fills the answer, so parse_field always gets
#         a clean number even if Gemini just confirms
#   - Added safe fallback: if STILL 0.0 after parse, use pre-computed best_data
# """
# import math
# import pandas as pd
# from agents.llm_caller import call_gemini, parse_field
# from agents.pricing_agent import run_pricing_agent
# from agents.inventory_agent import run_inventory_agent
# from agents.demand_agent import run_demand_agent
# from utils.prompt_builder import build_coordinator_prompt
# from config.settings import WEEK_DISCOUNTS, MIN_ACCEPTABLE_MARGIN


# def run_all_agents_for_week(sku: pd.Series, discount_pct: float, week: int) -> dict:
#     """Run all 3 agents for a single week and merge results."""
#     pricing   = run_pricing_agent(sku,   discount_pct, week)
#     inventory = run_inventory_agent(sku, discount_pct, week)
#     demand    = run_demand_agent(sku,    discount_pct, week)

#     return {
#         "week"               : week,
#         "discount_pct"       : discount_pct,
#         # Pricing
#         "new_price"          : pricing["new_price"],
#         "margin_before"      : pricing["margin_before"],
#         "margin_after"       : pricing["margin_after"],
#         "margin_loss"        : pricing["margin_loss"],
#         "pricing_summary"    : pricing["summary"],
#         # Inventory
#         "units_sold_forecast": inventory["units_sold_forecast"],
#         "stock_remaining"    : inventory["stock_remaining"],
#         "days_to_clear"      : inventory["days_to_clear"],
#         "velocity_change"    : inventory["velocity_change"],
#         "inventory_summary"  : inventory["summary"],
#         # Demand
#         "revenue_forecast"   : demand["revenue_forecast"],
#         "demand_uplift"      : demand["demand_uplift"],
#         "revenue_change"     : demand["revenue_change"],
#         "demand_summary"     : demand["summary"],
#     }


# def _pick_best_week(all_weeks: list) -> dict:
#     """Local fallback: pick best week by revenue where margin >= MIN_ACCEPTABLE_MARGIN."""
#     valid = [w for w in all_weeks if w.get("margin_after", 0) >= MIN_ACCEPTABLE_MARGIN]
#     pool  = valid if valid else all_weeks
#     return max(pool, key=lambda x: x.get("revenue_forecast", 0))


# def run_coordinator(sku: pd.Series) -> dict:
#     """
#     Full 4-week simulation:
#       - Runs 3 agents × 4 weeks = 12 Gemini calls
#       - Runs coordinator to pick best week = 1 more call
#       - Falls back to local logic if any parse fails
#     """
#     all_weeks = []
#     for i, discount_pct in enumerate(WEEK_DISCOUNTS):
#         result = run_all_agents_for_week(sku, float(discount_pct), i + 1)
#         all_weeks.append(result)

#     # ── Coordinator call ──────────────────────────────────────────
#     coord_prompt   = build_coordinator_prompt(sku, all_weeks)
#     coord_response = call_gemini(coord_prompt)

#     best_week     = int(parse_field(coord_response, "BEST_WEEK",      as_float=True) or 0)
#     best_discount = parse_field(coord_response, "BEST_DISCOUNT",  as_float=True)
#     best_price    = parse_field(coord_response, "BEST_PRICE",     as_float=True)
#     reason        = parse_field(coord_response, "REASON",         as_float=False)
#     rev_impact    = parse_field(coord_response, "REVENUE_IMPACT", as_float=True)
#     margin_impact = parse_field(coord_response, "MARGIN_IMPACT",  as_float=True)
#     risk          = parse_field(coord_response, "RISK_ASSESSMENT",as_float=False)

#     # ── Fallback: if ANY key value is 0 / empty, use local logic ──
#     # This covers: empty API key, Gemini rate-limit, parse failure
#     best_data = _pick_best_week(all_weeks)

#     if best_week < 1 or best_week > 4:
#         best_week = best_data["week"]

#     if best_discount == 0.0 or best_discount is None:
#         best_discount = best_data["discount_pct"]

#     if best_price == 0.0 or best_price is None:
#         best_price = best_data["new_price"]

#     if not reason or len(str(reason).strip()) < 5 or "ERROR" in str(reason):
#         reason = (
#             f"Week {best_week} ({best_discount}% discount) delivers the best balance "
#             f"of revenue (${best_data.get('revenue_forecast', 0):,.2f}) "
#             f"and margin ({best_data.get('margin_after', 0):.1f}%) "
#             f"while reducing stock from "
#             f"{sku.get('quantity', 0):.0f} to "
#             f"{best_data.get('stock_remaining', 0)} units."
#         )

#     if rev_impact == 0.0:
#         rev_impact = best_data.get("revenue_forecast", 0)

#     if margin_impact == 0.0:
#         margin_impact = best_data.get("margin_after", 0)

#     if not risk or len(str(risk).strip()) < 2:
#         clearance = sku.get("clearance_risk", "MEDIUM")
#         risk = {"HIGH": "High", "MEDIUM": "Medium", "LOW": "Low"}.get(clearance, "Medium")

#     return {
#         "all_weeks"      : all_weeks,
#         "best_week"      : int(best_week),
#         "best_discount"  : float(best_discount),
#         "best_price"     : float(best_price),
#         "reason"         : str(reason),
#         "revenue_impact" : float(rev_impact),
#         "margin_impact"  : float(margin_impact),
#         "risk_assessment": str(risk),
#         "raw_response"   : coord_response,
#     }


import pandas as pd
from agents.llm_caller import call_gemini, parse_field
from agents.pricing_agent import run_pricing_agent
from agents.inventory_agent import run_inventory_agent
from agents.demand_agent import run_demand_agent
from utils.prompt_builder import build_markdown_decision_prompt

def run_coordinator(sku: pd.Series) -> dict:
    """
    Step 1: Groq decides markdown % and strategy
    Step 2: 3 agents analyze impact of that decision
    """

    # ── STEP 1: Groq decides the markdown ─────────────────────────────────
    decision_prompt   = build_markdown_decision_prompt(sku)
    decision_response = call_gemini(decision_prompt)

    recommended_markdown = parse_field(decision_response, "RECOMMENDED_MARKDOWN", as_float=True)
    new_price            = parse_field(decision_response, "NEW_PRICE",            as_float=True)
    strategy             = parse_field(decision_response, "STRATEGY",             as_float=False)
    confidence           = parse_field(decision_response, "CONFIDENCE",           as_float=True)
    reasoning            = parse_field(decision_response, "REASONING",            as_float=False)
    margin_after_dec     = parse_field(decision_response, "MARGIN_AFTER",         as_float=True)
    risk_level           = parse_field(decision_response, "RISK_LEVEL",           as_float=False)

    # Fix new_price if missing
    price = sku.get("price", 0)
    if new_price == 0.0 and price > 0:
        new_price = round(price * (1 - recommended_markdown / 100), 2)

    # ── STEP 2: 3 agents analyze the decided markdown ─────────────────────
    pricing   = run_pricing_agent(sku,   recommended_markdown)
    inventory = run_inventory_agent(sku, recommended_markdown)
    demand    = run_demand_agent(sku,    recommended_markdown)

    # Use coordinator margin if agents didn't return it
    if pricing["margin_after"] == 0.0:
        pricing["margin_after"] = margin_after_dec

    # Add units_week to demand if missing
    if "units_week" not in demand:
        demand["units_week"] = inventory["units_sold_7days"]

    return {
        # Coordinator (Groq) decision
        "recommended_markdown": recommended_markdown,
        "new_price":            new_price,
        "strategy":             strategy,
        "confidence":           confidence,
        "reasoning":            reasoning,
        "margin_after":         pricing["margin_after"],
        "risk_level":           risk_level,
        "decision_response":    decision_response,

        # Agent analyses
        "pricing":   pricing,
        "inventory": inventory,
        "demand":    demand,
    }