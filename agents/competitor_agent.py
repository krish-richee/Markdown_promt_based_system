"""
agents/competitor_agent.py
Runs the Competitor Agent:
  1. Searches web via Tavily for real competitor prices
  2. Passes those prices to Gemini for analysis
  3. Returns competitive positioning + markdown suggestion
"""

import pandas as pd
from agents.llm_caller import call_gemini, parse_field
from utils.competitor_search import search_competitor_prices


def run_competitor_agent(sku: pd.Series) -> dict:
    """
    Full competitor analysis for one product.

    Returns:
        {
            "our_price"             : float,
            "avg_competitor_price"  : float,
            "min_competitor_price"  : float,
            "max_competitor_price"  : float,
            "price_gap_pct"         : float,
            "competitor_results"    : list,
            "positioning"           : str,   # "Overpriced" / "Competitive" / "Underpriced"
            "suggested_markdown"    : float,
            "confidence"            : float,
            "reasoning"             : str,
            "action"                : str,
            "is_simulated"          : bool,
            "raw_response"          : str,   # Gemini raw
            "prompt_sent"           : str,   # for backend visibility
        }
    """
    product_name = str(sku.get("product_name", "Unknown Product"))
    category     = str(sku.get("main_category", "General"))
    our_price    = float(sku.get("price", 0))

    # ── Step 1: Search competitor prices ─────────────────────────
    search_data = search_competitor_prices(product_name, category, our_price)

    avg_comp  = search_data["avg_price"]
    min_comp  = search_data["min_price"]
    max_comp  = search_data["max_price"]
    gap_pct   = search_data["price_gap_pct"]
    results   = search_data["results"]
    is_sim    = search_data.get("is_simulated", False)
    src_err   = search_data.get("error")

    # Build competitor list text for prompt
    comp_lines = "\n".join([
        f"  - {r['source']}: ${r['price']:.2f}"
        for r in results[:5]
    ]) if results else "  No competitor prices found."

    # ── Step 2: Build prompt ──────────────────────────────────────
    prompt = f"""You are a Competitor Intelligence Agent for a retail pricing system.

PRODUCT:
- Name:          {product_name}
- Category:      {category}
- Our Price:     ${our_price:.2f}
- ABC Class:     {sku.get('abc_class', 'C')}
- Clearance Risk:{sku.get('clearance_risk', 'LOW')}
- Stock Left:    {sku.get('quantity', 0):.0f} units

REAL COMPETITOR PRICES (from web search):
{comp_lines}

MARKET SUMMARY:
- Competitor Average Price: ${avg_comp:.2f}
- Competitor Min Price:     ${min_comp:.2f}
- Competitor Max Price:     ${max_comp:.2f}
- Our Price Gap:            {gap_pct:+.1f}% vs competitor average
  (positive = we are MORE expensive, negative = we are CHEAPER)

YOUR TASK:
Analyse our competitive position and recommend a markdown if needed.

Respond ONLY in this exact format (numbers only for number fields):

POSITIONING: [write exactly one of: Overpriced, Competitive, or Underpriced]
SUGGESTED_MARKDOWN: [0 to 40, just the number — how much % to discount to match market]
CONFIDENCE: [50 to 95, just the number]
REASONING: [two sentences: explain our position and what we should do]
ACTION: [write exactly one of: Apply Markdown, Hold Price, or Reduce Discount]
"""

    # ── Step 3: Gemini call ───────────────────────────────────────
    raw_response = call_gemini(prompt)

    # ── Step 4: Parse ─────────────────────────────────────────────
    positioning       = parse_field(raw_response, "POSITIONING",        as_float=False)
    suggested_markdown= parse_field(raw_response, "SUGGESTED_MARKDOWN", as_float=True)
    confidence        = parse_field(raw_response, "CONFIDENCE",         as_float=True)
    reasoning         = parse_field(raw_response, "REASONING",          as_float=False)
    action            = parse_field(raw_response, "ACTION",             as_float=False)

    # ── Fallbacks ─────────────────────────────────────────────────
    if not positioning or positioning.strip() == "":
        if   gap_pct > 10:  positioning = "Overpriced"
        elif gap_pct < -10: positioning = "Underpriced"
        else:               positioning = "Competitive"

    if suggested_markdown == 0.0 and gap_pct > 5:
        suggested_markdown = min(round(gap_pct * 0.7, 1), 40)

    if confidence == 0.0:
        confidence = 75.0 if not is_sim else 55.0

    if not reasoning or len(str(reasoning).strip()) < 5 or "ERROR" in str(reasoning):
        if gap_pct > 10:
            reasoning = (f"Our price (${our_price:.2f}) is {gap_pct:.1f}% above the "
                         f"competitor average (${avg_comp:.2f}). "
                         f"A {suggested_markdown:.0f}% markdown would bring us in line with the market.")
        elif gap_pct < -10:
            reasoning = (f"Our price (${our_price:.2f}) is {abs(gap_pct):.1f}% below "
                         f"competitor average (${avg_comp:.2f}). "
                         f"We are well-positioned — no markdown needed on pricing grounds.")
        else:
            reasoning = (f"Our price (${our_price:.2f}) is within {abs(gap_pct):.1f}% of "
                         f"the competitor average (${avg_comp:.2f}). "
                         f"Pricing is competitive — markdown decision should be driven by inventory.")

    if not action or action.strip() == "":
        if   positioning == "Overpriced":   action = "Apply Markdown"
        elif positioning == "Underpriced":  action = "Hold Price"
        else:                               action = "Hold Price"

    return {
        "our_price"            : our_price,
        "avg_competitor_price" : avg_comp,
        "min_competitor_price" : min_comp,
        "max_competitor_price" : max_comp,
        "price_gap_pct"        : gap_pct,
        "competitor_results"   : results,
        "positioning"          : str(positioning).strip(),
        "suggested_markdown"   : float(suggested_markdown),
        "confidence"           : float(confidence),
        "reasoning"            : str(reasoning).strip(),
        "action"               : str(action).strip(),
        "is_simulated"         : is_sim,
        "search_error"         : src_err,
        "raw_response"         : raw_response,
        "prompt_sent"          : prompt,
    }