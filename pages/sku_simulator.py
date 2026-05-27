
# import streamlit as st
# import plotly.graph_objects as go
# import pandas as pd
# from utils.data_loader import compute_sku_metrics, get_sku
# from agents.coordinator_agent import run_coordinator

# PLOT_LAYOUT = dict(
#     paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
#     font=dict(color="#f1f0f5", family="DM Sans"),
#     margin=dict(t=40, b=40, l=40, r=40),
#     xaxis=dict(gridcolor="#2d2650", zerolinecolor="#2d2650"),
#     yaxis=dict(gridcolor="#2d2650", zerolinecolor="#2d2650"),
# )

# def render():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
#     html, body, [data-testid="stAppViewContainer"] {
#         background: #0d0b14 !important; font-family: 'DM Sans', sans-serif; color: #f1f0f5;
#     }
#     [data-testid="stHeader"]  { background: transparent !important; }
#     [data-testid="stSidebar"] { background: #13101f !important; border-right: 1px solid #2d2650 !important; }
#     h1 { font-family: 'Syne', sans-serif !important; font-size: 2rem !important; font-weight: 800 !important;
#          background: linear-gradient(135deg,#fff,#c084fc); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
#     h2, h3 { font-family: 'Syne', sans-serif !important; color: #f1f0f5 !important; }
#     [data-testid="metric-container"] {
#         background: #1a1530 !important; border: 1px solid #2d2650 !important;
#         border-radius: 14px !important; padding: 20px !important;
#     }
#     [data-testid="stMetricLabel"] { color: #a09abf !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.1em; }
#     [data-testid="stMetricValue"] { color: #f1f0f5 !important; font-family: 'Syne',sans-serif !important; font-size: 1.7rem !important; font-weight: 700 !important; }
#     .stButton > button {
#         background: linear-gradient(135deg,#7c3aed,#a855f7) !important; color: white !important;
#         border: none !important; border-radius: 10px !important; font-family: 'Syne',sans-serif !important;
#         font-weight: 600 !important; padding: 12px 28px !important;
#         box-shadow: 0 4px 20px rgba(124,58,237,0.35) !important;
#     }
#     .stButton > button:hover { transform: translateY(-2px) !important; }
#     .stSelectbox > div > div { background: #1a1530 !important; border: 1px solid #2d2650 !important; border-radius: 10px !important; }
#     .stProgress > div > div { background: linear-gradient(90deg,#7c3aed,#a855f7) !important; border-radius:10px !important; }
#     .stInfo    { background: rgba(124,58,237,0.1) !important; border-left: 3px solid #7c3aed !important; border-radius: 10px !important; }
#     .stSuccess { background: rgba(34,197,94,0.1)  !important; border-left: 3px solid #22c55e !important; border-radius: 10px !important; }
#     .stWarning { background: rgba(245,158,11,0.1) !important; border-left: 3px solid #f59e0b !important; border-radius: 10px !important; }
#     .stError   { background: rgba(239,68,68,0.1)  !important; border-left: 3px solid #ef4444 !important; border-radius: 10px !important; }
#     hr { border-color: #2d2650 !important; }
#     .streamlit-expanderHeader { background: #1a1530 !important; border: 1px solid #2d2650 !important; border-radius: 10px !important; color: #f1f0f5 !important; }
#     .streamlit-expanderContent { background: #13101f !important; border: 1px solid #2d2650 !important; }
#     </style>
#     """, unsafe_allow_html=True)

#     st.markdown("# 🛍️ RetailAI — AI Markdown Decision Engine")
#     st.markdown("<p style='color:#a09abf; margin-top:-12px;'>Gemini AI analyzes each SKU and decides the optimal markdown price and strategy</p>", unsafe_allow_html=True)
#     st.divider()

#     # ── Load Data ──────────────────────────────────────────────────────────
#     with st.spinner("Loading product data..."):
#         df = compute_sku_metrics()

#     # ── Filters ────────────────────────────────────────────────────────────
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         cat = st.selectbox("Category", ["All"] + sorted(df["main_category"].unique().tolist()))
#     filtered = df if cat == "All" else df[df["main_category"] == cat]
#     with col2:
#         risk = st.selectbox("Risk", ["All", "HIGH", "MEDIUM", "LOW"])
#     if risk != "All":
#         filtered = filtered[filtered["clearance_risk"] == risk]
#     with col3:
#         abc = st.selectbox("ABC Class", ["All", "A", "B", "C"])
#     if abc != "All":
#         filtered = filtered[filtered["abc_class"] == abc]

#     selected_id = st.selectbox("Select SKU",
#         filtered["product_id"].tolist(),
#         format_func=lambda x: f"{x} — {filtered[filtered['product_id']==x]['product_name'].values[0]} (${filtered[filtered['product_id']==x]['price'].values[0]:.2f})"
#     )
#     sku = get_sku(df, selected_id)

#     # ── SKU Overview ───────────────────────────────────────────────────────
#     st.markdown("### 📋 SKU Overview")
#     c1,c2,c3,c4,c5,c6 = st.columns(6)
#     c1.metric("Price",        f"${sku['price']:.2f}")
#     c2.metric("Stock",        f"{int(sku['quantity'])} units")
#     c3.metric("Velocity",     f"{sku['sales_velocity']:.4f}/day")
#     c4.metric("ABC Class",    sku["abc_class"])
#     c5.metric("Risk",         sku["clearance_risk"])
#     c6.metric("Sell-Through", f"{sku['sell_through_rate']:.1f}%")

#     st.divider()

#     # ── How It Works ───────────────────────────────────────────────────────
#     st.markdown("### 🤖 How Gemini AI Decides")
#     st.markdown("""
#     <div style='background:#1a1530; border:1px solid #2d2650; border-radius:14px; padding:20px; margin-bottom:20px;'>
#         <div style='display:flex; gap:16px; align-items:center; flex-wrap:wrap;'>
#             <div style='background:#2d2650; border-radius:10px; padding:12px 16px; text-align:center;'>
#                 <div style='color:#c084fc; font-size:1.2rem;'>1️⃣</div>
#                 <div style='color:#f1f0f5; font-size:0.8rem; margin-top:4px;'>Product data<br>sent to Gemini</div>
#             </div>
#             <div style='color:#6b6485; font-size:1.5rem;'>→</div>
#             <div style='background:#2d2650; border-radius:10px; padding:12px 16px; text-align:center;'>
#                 <div style='color:#c084fc; font-size:1.2rem;'>2️⃣</div>
#                 <div style='color:#f1f0f5; font-size:0.8rem; margin-top:4px;'>Gemini reasons<br>& decides %</div>
#             </div>
#             <div style='color:#6b6485; font-size:1.5rem;'>→</div>
#             <div style='background:#2d2650; border-radius:10px; padding:12px 16px; text-align:center;'>
#                 <div style='color:#c084fc; font-size:1.2rem;'>3️⃣</div>
#                 <div style='color:#f1f0f5; font-size:0.8rem; margin-top:4px;'>3 agents analyze<br>the impact</div>
#             </div>
#             <div style='color:#6b6485; font-size:1.5rem;'>→</div>
#             <div style='background:#2d2650; border-radius:10px; padding:12px 16px; text-align:center;'>
#                 <div style='color:#c084fc; font-size:1.2rem;'>4️⃣</div>
#                 <div style='color:#f1f0f5; font-size:0.8rem; margin-top:4px;'>Dashboard<br>shows result</div>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     if st.button("🚀 Ask Gemini AI to Decide Markdown", type="primary"):
#         with st.spinner("Gemini AI is analyzing this product and deciding the optimal markdown..."):
#             result = run_coordinator(sku)

#         markdown_pct = result["recommended_markdown"]
#         new_price    = result["new_price"]
#         strategy     = result["strategy"]
#         confidence   = result["confidence"]
#         reasoning    = result["reasoning"]
#         risk_level   = result["risk_level"]
#         pricing      = result["pricing"]
#         inventory    = result["inventory"]
#         demand       = result["demand"]

#         # ── Gemini Decision Banner ─────────────────────────────────────────
#         color = "#22c55e" if markdown_pct < 15 else "#f59e0b" if markdown_pct < 30 else "#ef4444"
#         st.markdown(f"""
#         <div style='background:linear-gradient(135deg,rgba(124,58,237,0.2),rgba(168,85,247,0.1));
#                     border:1px solid #7c3aed; border-radius:16px; padding:28px; margin:16px 0;'>
#             <div style='font-family:Syne,sans-serif; font-size:0.75rem; color:#a09abf; text-transform:uppercase; letter-spacing:0.1em;'>
#                 GEMINI AI DECISION
#             </div>
#             <div style='font-family:Syne,sans-serif; font-size:1.8rem; font-weight:800; color:#f1f0f5; margin-top:8px;'>
#                 Apply <span style='color:{color};'>{markdown_pct:.0f}% Markdown</span> → New Price: <span style='color:#c084fc;'>${new_price:.2f}</span>
#             </div>
#             <div style='color:#a09abf; font-size:0.9rem; margin-top:6px;'>
#                 Strategy: <b style='color:#f1f0f5;'>{strategy}</b> &nbsp;|&nbsp;
#                 Confidence: <b style='color:#f1f0f5;'>{confidence:.0f}%</b> &nbsp;|&nbsp;
#                 Risk: <b style='color:#f1f0f5;'>{risk_level}</b>
#             </div>
#             <div style='background:rgba(255,255,255,0.05); border-radius:10px; padding:14px; margin-top:16px;'>
#                 <div style='color:#a09abf; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em;'>AI REASONING</div>
#                 <div style='color:#f1f0f5; font-size:0.9rem; margin-top:6px; line-height:1.6;'>{reasoning}</div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         # ── Impact Metrics ─────────────────────────────────────────────────
#         st.markdown("### 📊 Impact Analysis")
#         c1,c2,c3,c4,c5 = st.columns(5)
#         c1.metric("Original Price",   f"${sku['price']:.2f}")
#         c2.metric("New Price",        f"${new_price:.2f}", f"-${sku['price']-new_price:.2f}")
#         c3.metric("Margin After",     f"{pricing['margin_after']:.1f}%", f"-{pricing['margin_loss']:.1f}pp", delta_color="inverse")
#         c4.metric("Units/Week",       f"{inventory['units_sold_7days']}")
#         c5.metric("Revenue/Week",     f"${demand['revenue_forecast']:,.2f}")

#         # ── Agent Analyses ─────────────────────────────────────────────────
#         st.markdown("### 🤖 Agent Analyses")
#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.markdown(f"""
#             <div style='background:#1a1530; border:1px solid #2d2650; border-radius:14px; padding:20px;'>
#                 <div style='color:#c084fc; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em;'>💰 Pricing Agent</div>
#                 <div style='margin-top:12px;'>
#                     <div style='color:#a09abf; font-size:0.75rem;'>Margin Before</div>
#                     <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{pricing['margin_before']:.1f}%</div>
#                 </div>
#                 <div style='margin-top:8px;'>
#                     <div style='color:#a09abf; font-size:0.75rem;'>Margin After</div>
#                     <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{pricing['margin_after']:.1f}%</div>
#                 </div>
#                 <div style='margin-top:8px;'>
#                     <div style='color:#a09abf; font-size:0.75rem;'>Acceptable?</div>
#                     <div style='color:{"#22c55e" if pricing["acceptable"]=="Yes" else "#ef4444"}; font-size:1rem; font-weight:700;'>{pricing['acceptable']}</div>
#                 </div>
#                 <div style='margin-top:12px; color:#a09abf; font-size:0.82rem; line-height:1.5;'>{pricing['summary']}</div>
#             </div>
#             """, unsafe_allow_html=True)

#         with col2:
#             st.markdown(f"""
#             <div style='background:#1a1530; border:1px solid #2d2650; border-radius:14px; padding:20px;'>
#                 <div style='color:#c084fc; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em;'>📦 Inventory Agent</div>
#                 <div style='margin-top:12px;'>
#                     <div style='color:#a09abf; font-size:0.75rem;'>Units Sold (7 days)</div>
#                     <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{inventory['units_sold_7days']}</div>
#                 </div>
#                 <div style='margin-top:8px;'>
#                     <div style='color:#a09abf; font-size:0.75rem;'>Stock Remaining</div>
#                     <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{inventory['stock_remaining']}</div>
#                 </div>
#                 <div style='margin-top:8px;'>
#                     <div style='color:#a09abf; font-size:0.75rem;'>Days to Clear</div>
#                     <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{inventory['days_to_clear']}</div>
#                 </div>
#                 <div style='margin-top:12px; color:#a09abf; font-size:0.82rem; line-height:1.5;'>{inventory['summary']}</div>
#             </div>
#             """, unsafe_allow_html=True)

#         with col3:
#             st.markdown(f"""
#             <div style='background:#1a1530; border:1px solid #2d2650; border-radius:14px; padding:20px;'>
#                 <div style='color:#c084fc; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em;'>📈 Demand Agent</div>
#                 <div style='margin-top:12px;'>
#                     <div style='color:#a09abf; font-size:0.75rem;'>Demand Uplift</div>
#                     <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{demand['demand_uplift']:.1f}%</div>
#                 </div>
#                 <div style='margin-top:8px;'>
#                     <div style='color:#a09abf; font-size:0.75rem;'>Weekly Revenue</div>
#                     <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>${demand['revenue_forecast']:,.2f}</div>
#                 </div>
#                 <div style='margin-top:8px;'>
#                     <div style='color:#a09abf; font-size:0.75rem;'>Revenue Change</div>
#                     <div style='color:{"#22c55e" if demand["revenue_change"]>=0 else "#ef4444"}; font-size:1rem; font-weight:700;'>
#                         {"+" if demand["revenue_change"]>=0 else ""}{demand["revenue_change"]:,.2f}
#                     </div>
#                 </div>
#                 <div style='margin-top:12px; color:#a09abf; font-size:0.82rem; line-height:1.5;'>{demand['summary']}</div>
#             </div>
#             """, unsafe_allow_html=True)

#         # ── Visual Chart ───────────────────────────────────────────────────
#         st.markdown("### 📈 Before vs After")
#         fig = go.Figure()
#         fig.add_trace(go.Bar(
#             name="Before Markdown",
#             x=["Price", "Margin %", "Weekly Revenue ($)"],
#             y=[sku["price"], pricing["margin_before"], round(max(float(sku.get("sales_velocity",0)),0.01)*7*sku["price"],2)],
#             marker_color="#4c3d8f",
#         ))
#         fig.add_trace(go.Bar(
#             name="After Markdown",
#             x=["Price", "Margin %", "Weekly Revenue ($)"],
#             y=[new_price, pricing["margin_after"], demand["revenue_forecast"]],
#             marker_color="#7c3aed",
#         ))
#         fig.update_layout(**PLOT_LAYOUT, barmode="group",
#                           title="Impact of Gemini's Markdown Decision",
#                           legend=dict(bgcolor="rgba(0,0,0,0)"))
#         st.plotly_chart(fig, use_container_width=True)

#         # ── Raw Gemini Response ────────────────────────────────────────────
#         with st.expander("🔍 View Raw Gemini Decision Response"):
#             st.code(result["decision_response"], language="text")




import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import compute_sku_metrics, get_sku
from agents.coordinator_agent import run_coordinator

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#f1f0f5", family="DM Sans"),
    margin=dict(t=40, b=40, l=40, r=40),
    xaxis=dict(gridcolor="#2d2650", zerolinecolor="#2d2650"),
    yaxis=dict(gridcolor="#2d2650", zerolinecolor="#2d2650"),
)

def render():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background: #0d0b14 !important; font-family: 'DM Sans', sans-serif; color: #f1f0f5;
    }
    [data-testid="stHeader"]  { background: transparent !important; }
    [data-testid="stSidebar"] { background: #13101f !important; border-right: 1px solid #2d2650 !important; }
    h1 { font-family: 'Syne', sans-serif !important; font-size: 2rem !important; font-weight: 800 !important;
         background: linear-gradient(135deg,#fff,#c084fc); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    h2, h3 { font-family: 'Syne', sans-serif !important; color: #f1f0f5 !important; }
    [data-testid="metric-container"] {
        background: #1a1530 !important; border: 1px solid #2d2650 !important;
        border-radius: 14px !important; padding: 20px !important;
    }
    [data-testid="stMetricLabel"] { color: #a09abf !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.1em; }
    [data-testid="stMetricValue"] { color: #f1f0f5 !important; font-family: 'Syne',sans-serif !important; font-size: 1.7rem !important; font-weight: 700 !important; }
    .stButton > button {
        background: linear-gradient(135deg,#7c3aed,#a855f7) !important; color: white !important;
        border: none !important; border-radius: 10px !important; font-family: 'Syne',sans-serif !important;
        font-weight: 600 !important; padding: 12px 28px !important;
        box-shadow: 0 4px 20px rgba(124,58,237,0.35) !important;
    }
    .stButton > button:hover { transform: translateY(-2px) !important; }
    .stSelectbox > div > div { background: #1a1530 !important; border: 1px solid #2d2650 !important; border-radius: 10px !important; }
    .stProgress > div > div { background: linear-gradient(90deg,#7c3aed,#a855f7) !important; border-radius:10px !important; }
    .stInfo    { background: rgba(124,58,237,0.1) !important; border-left: 3px solid #7c3aed !important; border-radius: 10px !important; }
    .stSuccess { background: rgba(34,197,94,0.1)  !important; border-left: 3px solid #22c55e !important; border-radius: 10px !important; }
    .stWarning { background: rgba(245,158,11,0.1) !important; border-left: 3px solid #f59e0b !important; border-radius: 10px !important; }
    .stError   { background: rgba(239,68,68,0.1)  !important; border-left: 3px solid #ef4444 !important; border-radius: 10px !important; }
    hr { border-color: #2d2650 !important; }
    .streamlit-expanderHeader { background: #1a1530 !important; border: 1px solid #2d2650 !important; border-radius: 10px !important; color: #f1f0f5 !important; }
    .streamlit-expanderContent { background: #13101f !important; border: 1px solid #2d2650 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("# 🛍️ RetailAI — AI Markdown Decision Engine")
    st.markdown("<p style='color:#a09abf; margin-top:-12px;'>Gemini AI analyzes each SKU and decides the optimal markdown price and strategy</p>", unsafe_allow_html=True)
    st.divider()

    # ── Load Data ──────────────────────────────────────────────────────────
    with st.spinner("Loading product data..."):
        df = compute_sku_metrics()

    # ── Filters ────────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        cat = st.selectbox("Category", ["All"] + sorted(df["main_category"].unique().tolist()))
    filtered = df if cat == "All" else df[df["main_category"] == cat]
    with col2:
        risk = st.selectbox("Risk", ["All", "HIGH", "MEDIUM", "LOW"])
    if risk != "All":
        filtered = filtered[filtered["clearance_risk"] == risk]
    with col3:
        abc = st.selectbox("ABC Class", ["All", "A", "B", "C"])
    if abc != "All":
        filtered = filtered[filtered["abc_class"] == abc]

    selected_id = st.selectbox("Select SKU",
        filtered["product_id"].tolist(),
        format_func=lambda x: f"{x} — {filtered[filtered['product_id']==x]['product_name'].values[0]} (${filtered[filtered['product_id']==x]['price'].values[0]:.2f})"
    )
    sku = get_sku(df, selected_id)

    # ── SKU Overview ───────────────────────────────────────────────────────
    st.markdown("### 📋 SKU Overview")
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Price",        f"${sku['price']:.2f}")
    c2.metric("Stock",        f"{int(sku['quantity'])} units")
    c3.metric("Velocity",     f"{sku['sales_velocity']:.4f}/day")
    c4.metric("ABC Class",    sku["abc_class"])
    c5.metric("Risk",         sku["clearance_risk"])
    c6.metric("Sell-Through", f"{sku['sell_through_rate']:.1f}%")

    st.divider()

    # ── How It Works ───────────────────────────────────────────────────────
    st.markdown("### 🤖 How Gemini AI Decides")
    st.markdown("""
    <div style='background:#1a1530; border:1px solid #2d2650; border-radius:14px; padding:20px; margin-bottom:20px;'>
        <div style='display:flex; gap:16px; align-items:center; flex-wrap:wrap;'>
            <div style='background:#2d2650; border-radius:10px; padding:12px 16px; text-align:center;'>
                <div style='color:#c084fc; font-size:1.2rem;'>1️⃣</div>
                <div style='color:#f1f0f5; font-size:0.8rem; margin-top:4px;'>Product data<br>sent to Gemini</div>
            </div>
            <div style='color:#6b6485; font-size:1.5rem;'>→</div>
            <div style='background:#2d2650; border-radius:10px; padding:12px 16px; text-align:center;'>
                <div style='color:#c084fc; font-size:1.2rem;'>2️⃣</div>
                <div style='color:#f1f0f5; font-size:0.8rem; margin-top:4px;'>Gemini reasons<br>& decides %</div>
            </div>
            <div style='color:#6b6485; font-size:1.5rem;'>→</div>
            <div style='background:#2d2650; border-radius:10px; padding:12px 16px; text-align:center;'>
                <div style='color:#c084fc; font-size:1.2rem;'>3️⃣</div>
                <div style='color:#f1f0f5; font-size:0.8rem; margin-top:4px;'>3 agents analyze<br>the impact</div>
            </div>
            <div style='color:#6b6485; font-size:1.5rem;'>→</div>
            <div style='background:#2d2650; border-radius:10px; padding:12px 16px; text-align:center;'>
                <div style='color:#c084fc; font-size:1.2rem;'>4️⃣</div>
                <div style='color:#f1f0f5; font-size:0.8rem; margin-top:4px;'>Dashboard<br>shows result</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Ask Gemini AI to Decide Markdown", type="primary"):
        with st.spinner("Gemini AI is analyzing this product and deciding the optimal markdown..."):
            result = run_coordinator(sku)

        markdown_pct = result["recommended_markdown"]
        new_price    = result["new_price"]
        strategy     = result["strategy"]
        confidence   = result["confidence"]
        reasoning    = result["reasoning"]
        risk_level   = result["risk_level"]
        pricing      = result["pricing"]
        inventory    = result["inventory"]
        demand       = result["demand"]

        # ── Gemini Decision Banner ─────────────────────────────────────────
        color = "#22c55e" if markdown_pct < 15 else "#f59e0b" if markdown_pct < 30 else "#ef4444"
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,rgba(124,58,237,0.2),rgba(168,85,247,0.1));
                    border:1px solid #7c3aed; border-radius:16px; padding:28px; margin:16px 0;'>
            <div style='font-family:Syne,sans-serif; font-size:0.75rem; color:#a09abf; text-transform:uppercase; letter-spacing:0.1em;'>
                GEMINI AI DECISION
            </div>
            <div style='font-family:Syne,sans-serif; font-size:1.8rem; font-weight:800; color:#f1f0f5; margin-top:8px;'>
                Apply <span style='color:{color};'>{markdown_pct:.0f}% Markdown</span> → New Price: <span style='color:#c084fc;'>${new_price:.2f}</span>
            </div>
            <div style='color:#a09abf; font-size:0.9rem; margin-top:6px;'>
                Strategy: <b style='color:#f1f0f5;'>{strategy}</b> &nbsp;|&nbsp;
                Confidence: <b style='color:#f1f0f5;'>{confidence:.0f}%</b> &nbsp;|&nbsp;
                Risk: <b style='color:#f1f0f5;'>{risk_level}</b>
            </div>
            <div style='background:rgba(255,255,255,0.05); border-radius:10px; padding:14px; margin-top:16px;'>
                <div style='color:#a09abf; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em;'>AI REASONING</div>
                <div style='color:#f1f0f5; font-size:0.9rem; margin-top:6px; line-height:1.6;'>{reasoning}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Impact Metrics ─────────────────────────────────────────────────
        st.markdown("### 📊 Impact Analysis")
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Original Price",   f"${sku['price']:.2f}")
        c2.metric("New Price",        f"${new_price:.2f}", f"-${sku['price']-new_price:.2f}")
        c3.metric("Margin After",     f"{pricing['margin_after']:.1f}%", f"-{pricing['margin_loss']:.1f}pp", delta_color="inverse")
        c4.metric("Units/Week",       f"{inventory['units_sold_7days']}")
        c5.metric("Revenue/Week",     f"${demand['revenue_forecast']:,.2f}")

        # ── Agent Analyses ─────────────────────────────────────────────────
        st.markdown("### 🤖 Agent Analyses")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style='background:#1a1530; border:1px solid #2d2650; border-radius:14px; padding:20px;'>
                <div style='color:#c084fc; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em;'>💰 Pricing Agent</div>
                <div style='margin-top:12px;'>
                    <div style='color:#a09abf; font-size:0.75rem;'>Margin Before</div>
                    <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{pricing['margin_before']:.1f}%</div>
                </div>
                <div style='margin-top:8px;'>
                    <div style='color:#a09abf; font-size:0.75rem;'>Margin After</div>
                    <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{pricing['margin_after']:.1f}%</div>
                </div>
                <div style='margin-top:8px;'>
                    <div style='color:#a09abf; font-size:0.75rem;'>Acceptable?</div>
                    <div style='color:{"#22c55e" if pricing["acceptable"]=="Yes" else "#ef4444"}; font-size:1rem; font-weight:700;'>{pricing['acceptable']}</div>
                </div>
                <div style='margin-top:12px; color:#a09abf; font-size:0.82rem; line-height:1.5;'>{pricing['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background:#1a1530; border:1px solid #2d2650; border-radius:14px; padding:20px;'>
                <div style='color:#c084fc; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em;'>📦 Inventory Agent</div>
                <div style='margin-top:12px;'>
                    <div style='color:#a09abf; font-size:0.75rem;'>Units Sold (7 days)</div>
                    <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{inventory['units_sold_7days']}</div>
                </div>
                <div style='margin-top:8px;'>
                    <div style='color:#a09abf; font-size:0.75rem;'>Stock Remaining</div>
                    <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{inventory['stock_remaining']}</div>
                </div>
                <div style='margin-top:8px;'>
                    <div style='color:#a09abf; font-size:0.75rem;'>Days to Clear</div>
                    <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{inventory['days_to_clear']}</div>
                </div>
                <div style='margin-top:12px; color:#a09abf; font-size:0.82rem; line-height:1.5;'>{inventory['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style='background:#1a1530; border:1px solid #2d2650; border-radius:14px; padding:20px;'>
                <div style='color:#c084fc; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em;'>📈 Demand Agent</div>
                <div style='margin-top:12px;'>
                    <div style='color:#a09abf; font-size:0.75rem;'>Demand Uplift</div>
                    <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>{demand['demand_uplift']:.1f}%</div>
                </div>
                <div style='margin-top:8px;'>
                    <div style='color:#a09abf; font-size:0.75rem;'>Weekly Revenue</div>
                    <div style='color:#f1f0f5; font-size:1.3rem; font-weight:700;'>${demand['revenue_forecast']:,.2f}</div>
                </div>
                <div style='margin-top:8px;'>
                    <div style='color:#a09abf; font-size:0.75rem;'>Revenue Change</div>
                    <div style='color:{"#22c55e" if demand["revenue_change"]>=0 else "#ef4444"}; font-size:1rem; font-weight:700;'>
                        {"+" if demand["revenue_change"]>=0 else ""}{demand["revenue_change"]:,.2f}
                    </div>
                </div>
                <div style='margin-top:12px; color:#a09abf; font-size:0.82rem; line-height:1.5;'>{demand['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Visual Chart ───────────────────────────────────────────────────
        st.markdown("### 📈 Before vs After")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Before Markdown",
            x=["Price", "Margin %", "Weekly Revenue ($)"],
            y=[sku["price"], pricing["margin_before"], round(max(float(sku.get("sales_velocity",0)),0.01)*7*sku["price"],2)],
            marker_color="#4c3d8f",
        ))
        fig.add_trace(go.Bar(
            name="After Markdown",
            x=["Price", "Margin %", "Weekly Revenue ($)"],
            y=[new_price, pricing["margin_after"], demand["revenue_forecast"]],
            marker_color="#7c3aed",
        ))
        fig.update_layout(**PLOT_LAYOUT, barmode="group",
                          title="Impact of Gemini's Markdown Decision",
                          legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)

        # ── Raw Gemini Response ────────────────────────────────────────────
        with st.expander("🔍 View Raw Gemini Decision Response"):
            st.code(result["decision_response"], language="text")