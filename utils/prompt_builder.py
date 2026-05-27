# """
# prompt_builder.py — FIXED
# Bug fixed:
#   - Coordinator prompt had bracket hints like [1, 2, 3, or 4] which Gemini
#     echoes back literally, causing parse_field to return 0.0
#   - All bracket examples removed — clean number-only instructions
#   - Inventory prompt now tells Gemini the correct elasticity formula,
#     not "proportional to discount size" (which it ignores anyway)
#   - Demand prompt now includes explicit units/week baseline
# """
# import pandas as pd


# def build_pricing_prompt(sku: pd.Series, discount_pct: float, week: int) -> str:
#     price     = float(sku.get("price", 0))
#     new_price = round(price * (1 - discount_pct / 100), 2)
#     cost      = round(price * 0.55, 2)

#     margin_before = round((price - cost) / price * 100, 1) if price > 0 else 0
#     margin_after  = round((new_price - cost) / new_price * 100, 1) if new_price > 0 else 0
#     margin_loss   = round(margin_before - margin_after, 1)

#     return f"""You are a Pricing Agent in a retail markdown optimization system.

# PRODUCT DATA:
# - SKU ID:         {sku.get('product_id')}
# - Product Name:   {sku.get('product_name')}
# - Category:       {sku.get('main_category')}
# - Original Price: ${price:.2f}
# - Cost Price:     ${cost:.2f}
# - ABC Class:      {sku.get('abc_class', 'C')}
# - Clearance Risk: {sku.get('clearance_risk', 'LOW')}

# WEEK {week} SIMULATION:
# - Discount Applied: {discount_pct}%
# - New Price After Discount: ${new_price:.2f}

# Pre-calculated for your reference:
# - Margin Before Discount: {margin_before}%
# - Margin After Discount:  {margin_after}%
# - Margin Loss:            {margin_loss} percentage points

# YOUR TASK:
# Confirm or refine the margin analysis. Respond ONLY in this exact format
# (output numbers only — no % symbols, no $ signs, no extra text):

# NEW_PRICE: {new_price}
# MARGIN_BEFORE: {margin_before}
# MARGIN_AFTER: {margin_after}
# MARGIN_LOSS: {margin_loss}
# SUMMARY: one sentence about whether this margin impact is acceptable
# """


# def build_inventory_prompt(sku: pd.Series, discount_pct: float, week: int) -> str:
#     price         = float(sku.get("price", 0))
#     stock         = float(sku.get("quantity", 0))
#     velocity      = float(sku.get("sales_velocity", 0))

#     # Pre-compute so Gemini just confirms/refines rather than inventing
#     import math
#     uplift_factor       = 1 + (discount_pct / 100) * 2
#     new_velocity        = round(velocity * uplift_factor, 6)
#     units_7d_raw        = velocity * 7 * uplift_factor
#     # Use ceil so 0.023 → 1 unit, not 0
#     units_7d            = math.ceil(units_7d_raw) if units_7d_raw > 0 else 0
#     stock_after         = max(0, stock - units_7d)
#     days_clear          = round(stock_after / new_velocity, 0) if new_velocity > 0 else 9999

#     return f"""You are an Inventory Agent in a retail markdown optimization system.

# PRODUCT DATA:
# - SKU ID:         {sku.get('product_id')}
# - Product Name:   {sku.get('product_name')}
# - Category:       {sku.get('main_category')}
# - Current Stock:  {stock:.0f} units
# - Current Price:  ${price:.2f}
# - Sales Velocity: {velocity:.6f} units/day (current, before discount)
# - Days of Stock:  {min(sku.get('days_of_stock', 9999), 9999):.0f} days
# - Clearance Risk: {sku.get('clearance_risk', 'LOW')}

# WEEK {week} SIMULATION — {discount_pct}% DISCOUNT:
# Pre-calculated values for your reference:
# - Demand uplift factor:  {uplift_factor:.2f}x (discount increases demand)
# - New velocity:          {new_velocity:.6f} units/day
# - Units sold in 7 days:  {units_7d} units
# - Stock remaining:       {stock_after:.0f} units
# - Days to clear stock:   {days_clear:.0f} days

# YOUR TASK:
# Review these calculations and provide your assessment.
# Respond ONLY in this exact format (numbers only, no units or symbols):

# UNITS_SOLD_FORECAST: {units_7d}
# STOCK_REMAINING: {int(stock_after)}
# DAYS_TO_CLEAR: {int(min(days_clear, 9999))}
# VELOCITY_CHANGE: {new_velocity}
# SUMMARY: one sentence about whether this stock movement is sufficient
# """


# def build_demand_prompt(sku: pd.Series, discount_pct: float, week: int) -> str:
#     price     = float(sku.get("price", 0))
#     new_price = round(price * (1 - discount_pct / 100), 2)
#     velocity  = float(sku.get("sales_velocity", 0))

#     # Pre-compute
#     import math
#     uplift_factor    = 1 + (discount_pct / 100) * 2
#     new_velocity     = round(velocity * uplift_factor, 6)
#     units_7d_raw     = velocity * 7 * uplift_factor
#     units_7d         = math.ceil(units_7d_raw) if units_7d_raw > 0 else 0
#     revenue_forecast = round(units_7d * new_price, 2)
#     baseline_revenue = round(math.ceil(velocity * 7) * price, 2)
#     revenue_change   = round(revenue_forecast - baseline_revenue, 2)
#     demand_uplift_pct= round((uplift_factor - 1) * 100, 1)

#     return f"""You are a Demand Forecasting Agent in a retail markdown optimization system.

# PRODUCT DATA:
# - SKU ID:         {sku.get('product_id')}
# - Product Name:   {sku.get('product_name')}
# - Category:       {sku.get('main_category')}
# - Original Price: ${price:.2f}
# - Sales Velocity: {velocity:.6f} units/day
# - Sell-Through:   {sku.get('sell_through_rate', 0):.1f}%
# - ABC Class:      {sku.get('abc_class', 'C')}

# WEEK {week} SIMULATION — {discount_pct}% DISCOUNT:
# Pre-calculated values for your reference:
# - New Price:          ${new_price:.2f}
# - Demand uplift:      {demand_uplift_pct}%
# - New velocity:       {new_velocity:.6f} units/day
# - Units in 7 days:    {units_7d} units
# - Revenue forecast:   ${revenue_forecast:.2f}
# - Baseline revenue:   ${baseline_revenue:.2f}
# - Revenue change:     ${revenue_change:.2f}

# YOUR TASK:
# Review and confirm these demand calculations.
# Respond ONLY in this exact format (numbers only, no $ or % signs):

# REVENUE_FORECAST: {revenue_forecast}
# DEMAND_UPLIFT: {demand_uplift_pct}
# VELOCITY_NEW: {new_velocity}
# REVENUE_CHANGE: {revenue_change}
# SUMMARY: one sentence about whether this revenue change is positive for the business
# """


# def build_coordinator_prompt(sku: pd.Series, all_weeks: list) -> str:
#     weeks_text = ""
#     for w in all_weeks:
#         weeks_text += f"""
# Week {w['week']} — {w['discount_pct']}% Discount:
#   New Price:      ${w.get('new_price', 0):.2f}
#   Units Forecast: {w.get('units_sold_forecast', 0)} units
#   Revenue:        ${w.get('revenue_forecast', 0):.2f}
#   Margin After:   {w.get('margin_after', 0):.1f}%
#   Stock Remaining:{w.get('stock_remaining', 0)} units
#   Days to Clear:  {w.get('days_to_clear', 0)} days
# """

#     # Find the best week pre-computed (highest revenue with margin >= 15%)
#     valid = [w for w in all_weeks if w.get("margin_after", 0) >= 15]
#     if not valid:
#         valid = all_weeks
#     best = max(valid, key=lambda x: x.get("revenue_forecast", 0))

#     return f"""You are the Coordinator Agent in a retail markdown optimization system.
# You have received 4-week simulation results. Pick the BEST week.

# PRODUCT:
# - SKU: {sku.get('product_id')} | {sku.get('product_name')}
# - Category: {sku.get('main_category')} | ABC Class: {sku.get('abc_class')}
# - Clearance Risk: {sku.get('clearance_risk')} | Stock: {sku.get('quantity', 0):.0f} units

# 4-WEEK RESULTS:
# {weeks_text}

# Pre-computed recommendation (you may agree or override with reasoning):
# - Best week by revenue with margin >= 15%: Week {best['week']} ({best['discount_pct']}% discount)

# YOUR TASK:
# Pick the optimal week. Respond ONLY in this exact format.
# Write ONLY the number or value after each colon — no brackets, no extra text:

# BEST_WEEK: {best['week']}
# BEST_DISCOUNT: {best['discount_pct']}
# BEST_PRICE: {best.get('new_price', 0):.2f}
# REASON: two sentences explaining why this week is optimal given revenue and margin
# REVENUE_IMPACT: {best.get('revenue_forecast', 0):.2f}
# MARGIN_IMPACT: {best.get('margin_after', 0):.1f}
# RISK_ASSESSMENT: Medium
# """




import pandas as pd

def build_markdown_decision_prompt(sku: pd.Series) -> str:
    price    = sku.get("price", 0)
    cost     = round(price * 0.55, 2)
    stock    = int(sku.get("quantity", 0))
    velocity = float(sku.get("sales_velocity", 0))
    days     = min(float(sku.get("days_of_stock", 9999)), 9999)

    return f"""You are a senior retail pricing analyst AI. Your job is to decide the optimal markdown for this product.

PRODUCT DATA:
- SKU ID:            {sku.get('product_id')}
- Product Name:      {sku.get('product_name')}
- Category:          {sku.get('main_category')}
- ABC Class:         {sku.get('abc_class', 'C')}  (A=top revenue, B=mid, C=low)
- Current Price:     ${price:.2f}
- Cost Price:        ${cost:.2f}
- Current Margin:    {round((price-cost)/price*100,1) if price>0 else 0}%
- Stock:             {stock} units
- Sales Velocity:    {velocity:.6f} units/day
- Days of Stock:     {days:.0f} days  (9999 = dead inventory)
- Clearance Risk:    {sku.get('clearance_risk', 'LOW')}
- Sell-Through Rate: {sku.get('sell_through_rate', 0):.1f}%
- Dead Inventory:    {sku.get('is_dead_inventory', False)}

YOUR DECISION:
Based on all the signals above, decide:
1. What markdown % should be applied? (0 to 60%)
2. What is the new price after markdown?
3. Which strategy fits best?
4. Why did you choose this?

STRATEGY OPTIONS:
- No Action Needed       → LOW risk, healthy velocity
- Price Optimization     → LOW risk, high elasticity, small tweak needed
- Moderate Markdown      → MEDIUM risk, velocity needs boost
- Bundle Promotion       → MEDIUM risk, pair with fast mover
- Flash Sale             → HIGH risk, price sensitive product
- Loyalty Member Exclusive → ABC Class A, LOW risk, protect margin
- Clearance Markdown     → HIGH risk, dead/slow inventory, aggressive discount

RULES TO FOLLOW:
- If ABC Class A AND risk LOW → protect margin, max 10% markdown
- If risk HIGH AND days > 365 → aggressive markdown 25-45%
- If velocity < 0.01 AND stock > 100 → treat as dead inventory
- Margin must stay above 15% if possible
- If elasticity signals price sensitivity → increase markdown

Respond ONLY in this exact format:
RECOMMENDED_MARKDOWN: [number between 0 and 60, no % sign]
NEW_PRICE: [price after markdown, 2 decimal places]
STRATEGY: [one of the 7 strategies above]
CONFIDENCE: [0 to 100]
REASONING: [3-4 sentences explaining your decision based on the data]
MARGIN_AFTER: [margin % after markdown]
RISK_LEVEL: [Low / Medium / High / Critical]
"""

def build_pricing_agent_prompt(sku: pd.Series, markdown_pct: float) -> str:
    price     = sku.get("price", 0)
    new_price = round(price * (1 - markdown_pct / 100), 2)
    cost      = round(price * 0.55, 2)
    return f"""You are a Pricing Agent. A {markdown_pct}% markdown has been decided for this product.

Product: {sku.get('product_name')} | Price: ${price:.2f} → ${new_price:.2f}
Cost: ${cost:.2f} | ABC Class: {sku.get('abc_class')} | Risk: {sku.get('clearance_risk')}

Analyze the margin impact of this markdown decision.

Respond ONLY in this format:
MARGIN_BEFORE: [margin % before]
MARGIN_AFTER: [margin % after]
MARGIN_LOSS: [pp dropped]
ACCEPTABLE: [Yes / No — is this margin acceptable?]
SUMMARY: [1 sentence expert analysis]
"""

def build_inventory_agent_prompt(sku: pd.Series, markdown_pct: float) -> str:
    stock        = int(sku.get("quantity", 0))
    velocity     = max(float(sku.get("sales_velocity", 0)), 0.001)
    uplift       = 1 + (markdown_pct / 100) * 2.5
    new_velocity = round(velocity * uplift, 6)
    units_7days  = max(1, round(new_velocity * 7))
    stock_rem    = max(0, stock - units_7days)
    days_clear   = round(stock_rem / new_velocity) if new_velocity > 0 else 9999

    return f"""You are an Inventory Agent. A {markdown_pct}% markdown has been decided for this product.

PRODUCT DATA:
- Product: {sku.get('product_name')}
- Stock: {stock} units
- Current Velocity: {velocity:.6f} units/day (BEFORE markdown)
- Markdown Applied: {markdown_pct}%
- Risk: {sku.get('clearance_risk')}

CALCULATED PROJECTIONS (verify and confirm):
- Demand uplift from {markdown_pct}% discount: {round((uplift-1)*100)}%
- New velocity after markdown: {new_velocity:.6f} units/day
- Units to sell in 7 days: {units_7days}
- Stock remaining after 7 days: {stock_rem}
- Days to clear all stock: {days_clear}

Verify these projections make sense and provide your expert assessment.

Respond ONLY in this exact format (use the calculated numbers above):
UNITS_SOLD_7DAYS: {units_7days}
STOCK_REMAINING: {stock_rem}
DAYS_TO_CLEAR: {days_clear}
NEW_VELOCITY: {new_velocity}
SUMMARY: [1 sentence — your expert assessment of stock movement at this markdown]
"""

def build_demand_agent_prompt(sku: pd.Series, markdown_pct: float) -> str:
    price          = sku.get("price", 0)
    new_price      = round(price * (1 - markdown_pct / 100), 2)
    velocity       = max(float(sku.get("sales_velocity", 0)), 0.001)
    uplift         = 1 + (markdown_pct / 100) * 2.0
    new_velocity   = round(velocity * uplift, 6)
    units_week     = max(1, round(new_velocity * 7))
    revenue        = round(units_week * new_price, 2)
    baseline_rev   = round(velocity * 7 * price, 4)
    rev_change     = round(revenue - baseline_rev, 2)
    demand_uplift  = round((uplift - 1) * 100, 1)

    return f"""You are a Demand Forecasting Agent. A {markdown_pct}% markdown has been decided for this product.

PRODUCT DATA:
- Product: {sku.get('product_name')}
- Original Price: ${price:.2f} | New Price: ${new_price:.2f}
- Current Velocity: {velocity:.6f} units/day (BEFORE markdown)
- Sell-Through: {sku.get('sell_through_rate', 0):.1f}%

CALCULATED PROJECTIONS (verify and confirm):
- Demand uplift: {demand_uplift}%
- New velocity: {new_velocity:.6f} units/day
- Units per week: {units_week}
- Weekly revenue: ${revenue:.2f}
- Revenue change vs baseline: ${rev_change:.2f}

Verify these projections and provide your expert assessment.

Respond ONLY in this exact format (use the calculated numbers above):
DEMAND_UPLIFT: {demand_uplift}
NEW_VELOCITY: {new_velocity}
UNITS_WEEK: {units_week}
REVENUE_FORECAST: {revenue}
REVENUE_CHANGE: {rev_change}
SUMMARY: [1 sentence — your expert assessment of demand and revenue impact]
"""