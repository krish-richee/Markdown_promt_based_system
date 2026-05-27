# import pandas as pd
# from agents.llm_caller import call_gemini, parse_field
# from utils.prompt_builder import build_pricing_prompt
# from config.settings import COST_MULTIPLIER

# def run_pricing_agent(sku: pd.Series, discount_pct: float, week: int) -> dict:
#     """
#     Call Gemini with pricing prompt for one week simulation.
#     Returns margin before/after/loss and new price.
#     """
#     prompt   = build_pricing_prompt(sku, discount_pct, week)
#     response = call_gemini(prompt)

#     price     = sku.get("price", 0)
#     cost      = price * COST_MULTIPLIER
#     new_price = round(price * (1 - discount_pct / 100), 2)

#     # ── Parse Gemini response ──────────────────────────────────────────────
#     margin_before = parse_field(response, "MARGIN_BEFORE", as_float=True)
#     margin_after  = parse_field(response, "MARGIN_AFTER",  as_float=True)
#     margin_loss   = parse_field(response, "MARGIN_LOSS",   as_float=True)
#     summary       = parse_field(response, "SUMMARY",       as_float=False)

#     # ── Fallback calculation if Gemini gives 0 ─────────────────────────────
#     if margin_before == 0.0 and price > 0:
#         margin_before = round((price - cost) / price * 100, 1)
#     if margin_after == 0.0 and new_price > 0:
#         margin_after  = round((new_price - cost) / new_price * 100, 1)
#     if margin_loss == 0.0:
#         margin_loss   = round(margin_before - margin_after, 1)

#     return {
#         "week":          week,
#         "discount_pct":  discount_pct,
#         "new_price":     new_price,
#         "cost":          round(cost, 2),
#         "margin_before": margin_before,
#         "margin_after":  margin_after,
#         "margin_loss":   margin_loss,
#         "summary":       summary,
#         "raw_response":  response,
#     }






import pandas as pd
from agents.llm_caller import call_gemini, parse_field
from utils.prompt_builder import build_pricing_agent_prompt
from config.settings import COST_MULTIPLIER

def run_pricing_agent(sku: pd.Series, markdown_pct: float) -> dict:
    price     = sku.get("price", 0)
    cost      = price * COST_MULTIPLIER
    new_price = round(price * (1 - markdown_pct / 100), 2)

    prompt   = build_pricing_agent_prompt(sku, markdown_pct)
    response = call_gemini(prompt)

    margin_before = parse_field(response, "MARGIN_BEFORE", as_float=True)
    margin_after  = parse_field(response, "MARGIN_AFTER",  as_float=True)
    margin_loss   = parse_field(response, "MARGIN_LOSS",   as_float=True)
    acceptable    = parse_field(response, "ACCEPTABLE",    as_float=False)
    summary       = parse_field(response, "SUMMARY",       as_float=False)

    # Fallback only if Gemini completely fails
    if margin_before == 0.0:
        margin_before = round((price - cost) / price * 100, 1) if price > 0 else 0
    if margin_after == 0.0:
        margin_after  = round((new_price - cost) / new_price * 100, 1) if new_price > 0 else 0
    if margin_loss == 0.0:
        margin_loss   = round(margin_before - margin_after, 1)

    return {
        "new_price":     new_price,
        "margin_before": margin_before,
        "margin_after":  margin_after,
        "margin_loss":   margin_loss,
        "acceptable":    acceptable,
        "summary":       summary,
        "raw_response":  response,
    }