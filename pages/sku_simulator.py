

# import streamlit as st
# import plotly.graph_objects as go
# import pandas as pd
# from utils.data_loader import compute_sku_metrics, get_sku
# from agents.coordinator_agent import run_coordinator
# from pages.competitor_section import render_competitor_section

# PLOT_LAYOUT = dict(
#     paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
#     font=dict(color="#cbd5e1", family="'Space Grotesk', sans-serif"),
#     margin=dict(t=40, b=40, l=40, r=40),
#     xaxis=dict(gridcolor="#1e293b", zerolinecolor="#1e293b"),
#     yaxis=dict(gridcolor="#1e293b", zerolinecolor="#1e293b"),
# )

# def render():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Bricolage+Grotesque:wght@800;900&display=swap');

#     *, *::before, *::after { box-sizing: border-box; }

#     html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
#         background: #020817 !important;
#         font-family: 'Space Grotesk', sans-serif !important;
#         color: #e2e8f0 !important;
#     }
#     [data-testid="stHeader"] { background: transparent !important; }
#     [data-testid="stSidebar"] { background: #0a0f1e !important; border-right: 1px solid #1e293b !important; }
#     [data-testid="stMainBlockContainer"] { padding-top: 2rem !important; }

#     /* Animated grid background */
#     [data-testid="stAppViewContainer"]::before {
#         content: '';
#         position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0;
#         background-image:
#             linear-gradient(rgba(56,189,248,0.03) 1px, transparent 1px),
#             linear-gradient(90deg, rgba(56,189,248,0.03) 1px, transparent 1px);
#         background-size: 40px 40px;
#         pointer-events: none;
#     }

#     /* Glowing orbs */
#     [data-testid="stAppViewContainer"]::after {
#         content: '';
#         position: fixed; top: -20%; left: -10%; width: 60%; height: 60%; z-index: 0;
#         background: radial-gradient(ellipse, rgba(56,189,248,0.06) 0%, transparent 60%);
#         pointer-events: none;
#     }

#     /* Metric cards */
#     [data-testid="metric-container"] {
#         background: linear-gradient(135deg, #0f172a 0%, #0a0f1e 100%) !important;
#         border: 1px solid #1e293b !important;
#         border-radius: 12px !important;
#         padding: 18px !important;
#         transition: border-color 0.3s, transform 0.2s !important;
#         position: relative !important;
#         overflow: hidden !important;
#     }
#     [data-testid="metric-container"]:hover {
#         border-color: #38bdf8 !important;
#         transform: translateY(-2px) !important;
#     }
#     [data-testid="metric-container"]::before {
#         content: '';
#         position: absolute; top: 0; left: 0; right: 0; height: 2px;
#         background: linear-gradient(90deg, #38bdf8, #818cf8);
#         opacity: 0.6;
#     }
#     [data-testid="stMetricLabel"] {
#         color: #64748b !important;
#         font-size: 0.68rem !important;
#         text-transform: uppercase !important;
#         letter-spacing: 0.12em !important;
#         font-family: 'JetBrains Mono', monospace !important;
#     }
#     [data-testid="stMetricValue"] {
#         color: #f8fafc !important;
#         font-family: 'Bricolage Grotesque', sans-serif !important;
#         font-size: 1.6rem !important;
#         font-weight: 800 !important;
#     }
#     [data-testid="stMetricDelta"] { font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; }

#     /* Buttons */
#     .stButton > button {
#         background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
#         color: white !important; border: none !important;
#         border-radius: 8px !important;
#         font-family: 'Space Grotesk', sans-serif !important;
#         font-weight: 600 !important; font-size: 0.9rem !important;
#         padding: 12px 32px !important;
#         box-shadow: 0 0 20px rgba(14,165,233,0.3), 0 0 40px rgba(14,165,233,0.1) !important;
#         transition: all 0.3s !important;
#         letter-spacing: 0.02em !important;
#         position: relative !important;
#         overflow: hidden !important;
#     }
#     .stButton > button:hover {
#         box-shadow: 0 0 30px rgba(14,165,233,0.5), 0 0 60px rgba(14,165,233,0.2) !important;
#         transform: translateY(-1px) !important;
#     }

#     /* Selectboxes */
#     .stSelectbox > div > div {
#         background: #0f172a !important;
#         border: 1px solid #1e293b !important;
#         border-radius: 8px !important;
#         color: #e2e8f0 !important;
#         font-family: 'Space Grotesk', sans-serif !important;
#     }
#     .stSelectbox label { color: #64748b !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.08em; font-family: 'JetBrains Mono', monospace !important; }

#     /* Alerts */
#     .stInfo    { background: rgba(14,165,233,0.08) !important; border: 1px solid rgba(14,165,233,0.2) !important; border-radius: 8px !important; }
#     .stSuccess { background: rgba(16,185,129,0.08) !important; border: 1px solid rgba(16,185,129,0.2) !important; border-radius: 8px !important; }
#     .stWarning { background: rgba(245,158,11,0.08) !important; border: 1px solid rgba(245,158,11,0.2) !important; border-radius: 8px !important; }
#     .stError   { background: rgba(239,68,68,0.08)  !important; border: 1px solid rgba(239,68,68,0.2)  !important; border-radius: 8px !important; }

#     /* Expanders */
#     .streamlit-expanderHeader {
#         background: #0f172a !important; border: 1px solid #1e293b !important;
#         border-radius: 8px !important; color: #94a3b8 !important;
#         font-family: 'JetBrains Mono', monospace !important; font-size: 0.8rem !important;
#     }
#     .streamlit-expanderContent { background: #0a0f1e !important; border: 1px solid #1e293b !important; border-radius: 0 0 8px 8px !important; }

#     hr { border-color: #1e293b !important; margin: 2rem 0 !important; }

#     /* Spinner */
#     .stSpinner > div { border-top-color: #38bdf8 !important; }

#     /* Dataframe */
#     [data-testid="stDataFrame"] { border: 1px solid #1e293b !important; border-radius: 10px !important; overflow: hidden !important; }

#     /* Live dot animation */
#     @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.8)} }
#     @keyframes fadeSlideIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
#     @keyframes shimmer { 0%{background-position:-200% center} 100%{background-position:200% center} }
#     @keyframes glow { 0%,100%{box-shadow:0 0 10px rgba(14,165,233,0.3)} 50%{box-shadow:0 0 25px rgba(14,165,233,0.6)} }
#     </style>
#     """, unsafe_allow_html=True)

#     # ── Header ─────────────────────────────────────────────────────────────
#     st.markdown("""
#     <div style="margin-bottom:2rem; animation: fadeSlideIn 0.6s ease;">
#         <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
#             <div style="width:8px;height:8px;border-radius:50%;background:#10b981;
#                  animation:pulse 2s infinite; box-shadow:0 0 8px #10b981;"></div>
#             <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem;
#                   color:#10b981; letter-spacing:0.15em; text-transform:uppercase;">LIVE SYSTEM</span>
#         </div>
#         <h1 style="font-family:'Bricolage Grotesque',sans-serif; font-size:2.4rem;
#              font-weight:900; margin:0; line-height:1.1;
#              background: linear-gradient(135deg, #f8fafc 0%, #38bdf8 50%, #818cf8 100%);
#              -webkit-background-clip:text; -webkit-text-fill-color:transparent;
#              background-size:200% auto; animation:shimmer 4s linear infinite;">
#             RetailAI — Markdown Intelligence
#         </h1>
#         <p style="color:#475569; font-size:0.9rem; margin-top:8px; font-family:'Space Grotesk',sans-serif;">
#             AI-powered pricing decisions · Real-time competitor intelligence · Multi-agent analysis
#         </p>
#     </div>
#     """, unsafe_allow_html=True)

#     # ── Load Data ──────────────────────────────────────────────────────────
#     with st.spinner("Connecting to data pipeline..."):
#         df = compute_sku_metrics()

#     # ── Filters ────────────────────────────────────────────────────────────
#     st.markdown("""
#     <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#38bdf8;
#          text-transform:uppercase; letter-spacing:0.15em; margin-bottom:8px;">
#         ▸ Filter SKUs
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns(3)
#     with col1:
#         cat = st.selectbox("Category", ["All"] + sorted(df["main_category"].unique().tolist()))
#     filtered = df if cat == "All" else df[df["main_category"] == cat]
#     with col2:
#         risk = st.selectbox("Risk Level", ["All", "HIGH", "MEDIUM", "LOW"])
#     if risk != "All":
#         filtered = filtered[filtered["clearance_risk"] == risk]
#     with col3:
#         abc = st.selectbox("ABC Class", ["All", "A", "B", "C"])
#     if abc != "All":
#         filtered = filtered[filtered["abc_class"] == abc]

#     selected_id = st.selectbox("Select SKU",
#         filtered["product_id"].tolist(),
#         format_func=lambda x: f"{x}  ·  {filtered[filtered['product_id']==x]['product_name'].values[0]}  ·  ${filtered[filtered['product_id']==x]['price'].values[0]:.2f}"
#     )
#     sku = get_sku(df, selected_id)

#     # ── SKU Overview ───────────────────────────────────────────────────────
#     st.markdown("""
#     <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#38bdf8;
#          text-transform:uppercase; letter-spacing:0.15em; margin:1.5rem 0 0.8rem 0;">
#         ▸ SKU Snapshot
#     </div>
#     """, unsafe_allow_html=True)

#     risk_color = {"HIGH": "#ef4444", "MEDIUM": "#f59e0b", "LOW": "#10b981"}.get(sku.get("clearance_risk","LOW"), "#64748b")
#     abc_color  = {"A": "#10b981", "B": "#f59e0b", "C": "#ef4444"}.get(sku.get("abc_class","C"), "#64748b")

#     st.markdown(f"""
#     <div style="background:linear-gradient(135deg,#0f172a,#0a0f1e);
#          border:1px solid #1e293b; border-radius:14px; padding:20px 24px;
#          margin-bottom:1rem; position:relative; overflow:hidden;
#          animation: fadeSlideIn 0.5s ease;">
#         <div style="position:absolute;top:0;left:0;right:0;height:2px;
#              background:linear-gradient(90deg,#38bdf8,#818cf8,#10b981);"></div>
#         <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
#             <span style="font-family:'Bricolage Grotesque',sans-serif;font-size:1.15rem;
#                   font-weight:800;color:#f8fafc;">{sku.get('product_name','—')}</span>
#             <span style="background:{risk_color}22;color:{risk_color};border:1px solid {risk_color}44;
#                   border-radius:4px;padding:2px 8px;font-size:0.68rem;font-family:'JetBrains Mono',monospace;
#                   text-transform:uppercase;letter-spacing:0.1em;">{sku.get('clearance_risk','—')} RISK</span>
#             <span style="background:{abc_color}22;color:{abc_color};border:1px solid {abc_color}44;
#                   border-radius:4px;padding:2px 8px;font-size:0.68rem;font-family:'JetBrains Mono',monospace;">CLASS {sku.get('abc_class','—')}</span>
#         </div>
#         <div style="color:#475569;font-size:0.8rem;font-family:'JetBrains Mono',monospace;">
#             ID: {sku.get('product_id','—')} &nbsp;·&nbsp; {sku.get('main_category','—')}
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     c1,c2,c3,c4,c5,c6 = st.columns(6)
#     c1.metric("Price",        f"${sku['price']:.2f}")
#     c2.metric("Stock",        f"{int(sku['quantity'])} units")
#     c3.metric("Velocity",     f"{sku['sales_velocity']:.4f}/day")
#     c4.metric("ABC Class",    sku["abc_class"])
#     c5.metric("Risk",         sku["clearance_risk"])
#     c6.metric("Sell-Through", f"{sku['sell_through_rate']:.1f}%")

#     # ── AI Markdown Section ────────────────────────────────────────────────
#     st.markdown("""<div style="height:1.5rem;"></div>""", unsafe_allow_html=True)
#     st.markdown("""
#     <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#818cf8;
#          text-transform:uppercase; letter-spacing:0.15em; margin-bottom:12px;">
#         ▸ AI Markdown Engine
#     </div>
#     """, unsafe_allow_html=True)

#     col_btn, col_info = st.columns([2, 3])
#     with col_btn:
#         run_md = st.button("⚡ Run AI Markdown Analysis", type="primary", use_container_width=True)
#     with col_info:
#         st.markdown("""
#         <div style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;
#              padding:10px 14px;display:flex;align-items:center;gap:10px;">
#             <div style="width:6px;height:6px;border-radius:50%;background:#818cf8;
#                  animation:pulse 2s infinite;flex-shrink:0;"></div>
#             <span style="color:#64748b;font-size:0.78rem;font-family:'Space Grotesk',sans-serif;">
#                 Gemini AI analyzes stock risk, velocity & margins to recommend the optimal discount
#             </span>
#         </div>
#         """, unsafe_allow_html=True)

#     if run_md:
#         with st.spinner("AI agents processing..."):
#             st.session_state["markdown_result"] = run_coordinator(sku)
#             st.session_state["markdown_sku_id"] = selected_id
#             from utils.history_manager import save_decision
#             save_decision(dict(sku), st.session_state["markdown_result"])
            

#     if st.session_state.get("markdown_result") and st.session_state.get("markdown_sku_id") == selected_id:
#         result       = st.session_state["markdown_result"]
#         markdown_pct = result["recommended_markdown"]
#         new_price    = result["new_price"]
#         strategy     = result["strategy"]
#         confidence   = result["confidence"]
#         reasoning    = result["reasoning"]
#         risk_level   = result["risk_level"]
#         pricing      = result["pricing"]
#         inventory    = result["inventory"]
#         demand       = result["demand"]

#         md_color = "#10b981" if markdown_pct < 15 else "#f59e0b" if markdown_pct < 30 else "#ef4444"

#         # Decision card
#         st.markdown(f"""
#         <div style="background:linear-gradient(135deg,rgba(14,165,233,0.08),rgba(99,102,241,0.08));
#              border:1px solid rgba(14,165,233,0.25); border-radius:16px;
#              padding:28px 32px; margin:1rem 0; position:relative; overflow:hidden;
#              animation: fadeSlideIn 0.5s ease;">
#             <div style="position:absolute;top:0;left:0;right:0;height:3px;
#                  background:linear-gradient(90deg,#0ea5e9,#6366f1);"></div>
#             <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;
#                  border-radius:50%;background:radial-gradient(circle,rgba(14,165,233,0.08),transparent);"></div>
#             <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:16px;">
#                 <div>
#                     <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
#                          color:#38bdf8;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:8px;">
#                         ● GEMINI DECISION · LIVE
#                     </div>
#                     <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:2rem;
#                          font-weight:900;color:#f8fafc;line-height:1.1;">
#                         <span style="color:{md_color};">{markdown_pct:.0f}% Markdown</span>
#                         <span style="color:#475569;font-size:1.2rem;"> → </span>
#                         <span style="color:#38bdf8;">${new_price:.2f}</span>
#                     </div>
#                     <div style="margin-top:10px;display:flex;gap:16px;flex-wrap:wrap;">
#                         <span style="background:#1e293b;border-radius:6px;padding:4px 10px;
#                               font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#94a3b8;">
#                             Strategy: <b style="color:#e2e8f0;">{strategy}</b>
#                         </span>
#                         <span style="background:#1e293b;border-radius:6px;padding:4px 10px;
#                               font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#94a3b8;">
#                             Confidence: <b style="color:#10b981;">{confidence:.0f}%</b>
#                         </span>
#                         <span style="background:#1e293b;border-radius:6px;padding:4px 10px;
#                               font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#94a3b8;">
#                             Risk: <b style="color:{md_color};">{risk_level}</b>
#                         </span>
#                     </div>
#                 </div>
#             </div>
#             <div style="margin-top:18px;padding:14px 16px;
#                  background:rgba(255,255,255,0.03);border-radius:8px;
#                  border-left:3px solid #6366f1;">
#                 <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
#                      color:#64748b;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:6px;">
#                     AI Reasoning
#                 </div>
#                 <div style="color:#cbd5e1;font-size:0.88rem;line-height:1.7;">{reasoning}</div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         # Impact metrics
#         st.markdown("""
#         <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#10b981;
#              text-transform:uppercase; letter-spacing:0.15em; margin:1.2rem 0 0.6rem 0;">
#             ▸ Impact Analysis
#         </div>
#         """, unsafe_allow_html=True)
#         c1,c2,c3,c4,c5 = st.columns(5)
#         c1.metric("Original Price",  f"${sku['price']:.2f}")
#         c2.metric("New Price",       f"${new_price:.2f}",              f"-${sku['price']-new_price:.2f}")
#         c3.metric("Margin After",    f"{pricing['margin_after']:.1f}%",f"-{pricing['margin_loss']:.1f}pp", delta_color="inverse")
#         c4.metric("Units / Week",    f"{inventory['units_sold_7days']}")
#         c5.metric("Revenue / Week",  f"${demand['revenue_forecast']:,.2f}")

#         # Agent cards
#         st.markdown("""
#         <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#10b981;
#              text-transform:uppercase; letter-spacing:0.15em; margin:1.2rem 0 0.6rem 0;">
#             ▸ Agent Breakdown
#         </div>
#         """, unsafe_allow_html=True)

#         col1, col2, col3 = st.columns(3)
#         agents = [
#             {
#                 "icon": "💰", "label": "Pricing Agent", "color": "#38bdf8",
#                 "rows": [
#                     ("Margin Before", f"{pricing['margin_before']:.1f}%", "#e2e8f0"),
#                     ("Margin After",  f"{pricing['margin_after']:.1f}%",  "#e2e8f0"),
#                     ("Acceptable",    pricing['acceptable'], "#10b981" if pricing['acceptable']=="Yes" else "#ef4444"),
#                 ],
#                 "summary": pricing['summary']
#             },
#             {
#                 "icon": "📦", "label": "Inventory Agent", "color": "#818cf8",
#                 "rows": [
#                     ("Units Sold / 7d",  str(inventory['units_sold_7days']),  "#e2e8f0"),
#                     ("Stock Remaining",  str(inventory['stock_remaining']),   "#e2e8f0"),
#                     ("Days to Clear",    str(inventory['days_to_clear']),     "#f59e0b"),
#                 ],
#                 "summary": inventory['summary']
#             },
#             {
#                 "icon": "📈", "label": "Demand Agent", "color": "#10b981",
#                 "rows": [
#                     ("Demand Uplift",    f"{demand['demand_uplift']:.1f}%",   "#10b981"),
#                     ("Weekly Revenue",   f"${demand['revenue_forecast']:,.2f}", "#e2e8f0"),
#                     ("Revenue Δ",        f"{'+'if demand['revenue_change']>=0 else ''}{demand['revenue_change']:,.2f}",
#                                          "#10b981" if demand['revenue_change']>=0 else "#ef4444"),
#                 ],
#                 "summary": demand['summary']
#             },
#         ]

#         for col, agent in zip([col1,col2,col3], agents):
#             rows_html = "".join([
#                 f"""<div style="display:flex;justify-content:space-between;align-items:center;
#                      padding:7px 0;border-bottom:1px solid #1e293b;">
#                     <span style="color:#64748b;font-size:0.75rem;font-family:'JetBrains Mono',monospace;">{r[0]}</span>
#                     <span style="color:{r[2]};font-weight:700;font-size:0.88rem;font-family:'Space Grotesk',sans-serif;">{r[1]}</span>
#                 </div>"""
#                 for r in agent["rows"]
#             ])
#             col.markdown(f"""
#             <div style="background:linear-gradient(135deg,#0f172a,#0a0f1e);
#                  border:1px solid #1e293b; border-radius:12px; padding:18px;
#                  position:relative; overflow:hidden; height:100%;">
#                 <div style="position:absolute;top:0;left:0;right:0;height:2px;
#                      background:{agent['color']};opacity:0.6;"></div>
#                 <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
#                     <span style="font-size:1rem;">{agent['icon']}</span>
#                     <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
#                           color:{agent['color']};text-transform:uppercase;letter-spacing:0.1em;">
#                         {agent['label']}
#                     </span>
#                 </div>
#                 {rows_html}
#                 <div style="color:#475569;font-size:0.75rem;line-height:1.5;
#                      margin-top:12px;font-style:italic;">{agent['summary']}</div>
#             </div>
#             """, unsafe_allow_html=True)

#         with st.expander("🔍 Raw Gemini Response"):
#             st.code(result["decision_response"], language="text")

#     # ── Competitor Intelligence ────────────────────────────────────────────
#     render_competitor_section(sku)





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
from pages.competitor_section import render_competitor_section

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cbd5e1", family="'Space Grotesk', sans-serif"),
    margin=dict(t=40, b=40, l=40, r=40),
    xaxis=dict(gridcolor="#1e293b", zerolinecolor="#1e293b"),
    yaxis=dict(gridcolor="#1e293b", zerolinecolor="#1e293b"),
)

def render():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Bricolage+Grotesque:wght@800;900&display=swap');

    *, *::before, *::after { box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: #020817 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stSidebar"] { background: #0a0f1e !important; border-right: 1px solid #1e293b !important; }
    [data-testid="stMainBlockContainer"] { padding-top: 2rem !important; }

    /* Animated grid background */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0;
        background-image:
            linear-gradient(rgba(56,189,248,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56,189,248,0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
    }

    /* Glowing orbs */
    [data-testid="stAppViewContainer"]::after {
        content: '';
        position: fixed; top: -20%; left: -10%; width: 60%; height: 60%; z-index: 0;
        background: radial-gradient(ellipse, rgba(56,189,248,0.06) 0%, transparent 60%);
        pointer-events: none;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #0f172a 0%, #0a0f1e 100%) !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        padding: 18px !important;
        transition: border-color 0.3s, transform 0.2s !important;
        position: relative !important;
        overflow: hidden !important;
    }
    [data-testid="metric-container"]:hover {
        border-color: #38bdf8 !important;
        transform: translateY(-2px) !important;
    }
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        opacity: 0.6;
    }
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 0.68rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-family: 'Bricolage Grotesque', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricDelta"] { font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
        color: white !important; border: none !important;
        border-radius: 8px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important; font-size: 0.9rem !important;
        padding: 12px 32px !important;
        box-shadow: 0 0 20px rgba(14,165,233,0.3), 0 0 40px rgba(14,165,233,0.1) !important;
        transition: all 0.3s !important;
        letter-spacing: 0.02em !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .stButton > button:hover {
        box-shadow: 0 0 30px rgba(14,165,233,0.5), 0 0 60px rgba(14,165,233,0.2) !important;
        transform: translateY(-1px) !important;
    }

    /* Selectboxes */
    .stSelectbox > div > div {
        background: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    .stSelectbox label { color: #64748b !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.08em; font-family: 'JetBrains Mono', monospace !important; }

    /* Alerts */
    .stInfo    { background: rgba(14,165,233,0.08) !important; border: 1px solid rgba(14,165,233,0.2) !important; border-radius: 8px !important; }
    .stSuccess { background: rgba(16,185,129,0.08) !important; border: 1px solid rgba(16,185,129,0.2) !important; border-radius: 8px !important; }
    .stWarning { background: rgba(245,158,11,0.08) !important; border: 1px solid rgba(245,158,11,0.2) !important; border-radius: 8px !important; }
    .stError   { background: rgba(239,68,68,0.08)  !important; border: 1px solid rgba(239,68,68,0.2)  !important; border-radius: 8px !important; }

    /* Expanders */
    .streamlit-expanderHeader {
        background: #0f172a !important; border: 1px solid #1e293b !important;
        border-radius: 8px !important; color: #94a3b8 !important;
        font-family: 'JetBrains Mono', monospace !important; font-size: 0.8rem !important;
    }
    .streamlit-expanderContent { background: #0a0f1e !important; border: 1px solid #1e293b !important; border-radius: 0 0 8px 8px !important; }

    hr { border-color: #1e293b !important; margin: 2rem 0 !important; }

    /* Spinner */
    .stSpinner > div { border-top-color: #38bdf8 !important; }

    /* Dataframe */
    [data-testid="stDataFrame"] { border: 1px solid #1e293b !important; border-radius: 10px !important; overflow: hidden !important; }

    /* Live dot animation */
    @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.8)} }
    @keyframes fadeSlideIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
    @keyframes shimmer { 0%{background-position:-200% center} 100%{background-position:200% center} }
    @keyframes glow { 0%,100%{box-shadow:0 0 10px rgba(14,165,233,0.3)} 50%{box-shadow:0 0 25px rgba(14,165,233,0.6)} }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:2rem; animation: fadeSlideIn 0.6s ease;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#10b981;
                 animation:pulse 2s infinite; box-shadow:0 0 8px #10b981;"></div>
            <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem;
                  color:#10b981; letter-spacing:0.15em; text-transform:uppercase;">LIVE SYSTEM</span>
        </div>
        <h1 style="font-family:'Bricolage Grotesque',sans-serif; font-size:2.4rem;
             font-weight:900; margin:0; line-height:1.1;
             background: linear-gradient(135deg, #f8fafc 0%, #38bdf8 50%, #818cf8 100%);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent;
             background-size:200% auto; animation:shimmer 4s linear infinite;">
            RetailAI — Markdown Intelligence
        </h1>
        <p style="color:#475569; font-size:0.9rem; margin-top:8px; font-family:'Space Grotesk',sans-serif;">
            AI-powered pricing decisions · Real-time competitor intelligence · Multi-agent analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Load Data ──────────────────────────────────────────────────────────
    with st.spinner("Connecting to data pipeline..."):
        df = compute_sku_metrics()

    # ── Filters ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#38bdf8;
         text-transform:uppercase; letter-spacing:0.15em; margin-bottom:8px;">
        ▸ Filter SKUs
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        cat = st.selectbox("Category", ["All"] + sorted(df["main_category"].unique().tolist()))
    filtered = df if cat == "All" else df[df["main_category"] == cat]
    with col2:
        risk = st.selectbox("Risk Level", ["All", "HIGH", "MEDIUM", "LOW"])
    if risk != "All":
        filtered = filtered[filtered["clearance_risk"] == risk]
    with col3:
        abc = st.selectbox("ABC Class", ["All", "A", "B", "C"])
    if abc != "All":
        filtered = filtered[filtered["abc_class"] == abc]

    selected_id = st.selectbox("Select SKU",
        filtered["product_id"].tolist(),
        format_func=lambda x: f"{x}  ·  {filtered[filtered['product_id']==x]['product_name'].values[0]}  ·  ${filtered[filtered['product_id']==x]['price'].values[0]:.2f}"
    )
    sku = get_sku(df, selected_id)

    # ── SKU Overview ───────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#38bdf8;
         text-transform:uppercase; letter-spacing:0.15em; margin:1.5rem 0 0.8rem 0;">
        ▸ SKU Snapshot
    </div>
    """, unsafe_allow_html=True)

    risk_color = {"HIGH": "#ef4444", "MEDIUM": "#f59e0b", "LOW": "#10b981"}.get(sku.get("clearance_risk","LOW"), "#64748b")
    abc_color  = {"A": "#10b981", "B": "#f59e0b", "C": "#ef4444"}.get(sku.get("abc_class","C"), "#64748b")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,#0a0f1e);
         border:1px solid #1e293b; border-radius:14px; padding:20px 24px;
         margin-bottom:1rem; position:relative; overflow:hidden;
         animation: fadeSlideIn 0.5s ease;">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
             background:linear-gradient(90deg,#38bdf8,#818cf8,#10b981);"></div>
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <span style="font-family:'Bricolage Grotesque',sans-serif;font-size:1.15rem;
                  font-weight:800;color:#f8fafc;">{sku.get('product_name','—')}</span>
            <span style="background:{risk_color}22;color:{risk_color};border:1px solid {risk_color}44;
                  border-radius:4px;padding:2px 8px;font-size:0.68rem;font-family:'JetBrains Mono',monospace;
                  text-transform:uppercase;letter-spacing:0.1em;">{sku.get('clearance_risk','—')} RISK</span>
            <span style="background:{abc_color}22;color:{abc_color};border:1px solid {abc_color}44;
                  border-radius:4px;padding:2px 8px;font-size:0.68rem;font-family:'JetBrains Mono',monospace;">CLASS {sku.get('abc_class','—')}</span>
        </div>
        <div style="color:#475569;font-size:0.8rem;font-family:'JetBrains Mono',monospace;">
            ID: {sku.get('product_id','—')} &nbsp;·&nbsp; {sku.get('main_category','—')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Price",        f"${sku['price']:.2f}")
    c2.metric("Stock",        f"{int(sku['quantity'])} units")
    c3.metric("Velocity",     f"{sku['sales_velocity']:.4f}/day")
    c4.metric("ABC Class",    sku["abc_class"])
    c5.metric("Risk",         sku["clearance_risk"])
    c6.metric("Sell-Through", f"{sku['sell_through_rate']:.1f}%")

    # ── AI Markdown Section ────────────────────────────────────────────────
    st.markdown("""<div style="height:1.5rem;"></div>""", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#818cf8;
         text-transform:uppercase; letter-spacing:0.15em; margin-bottom:12px;">
        ▸ AI Markdown Engine
    </div>
    """, unsafe_allow_html=True)

    col_btn, col_info = st.columns([2, 3])
    with col_btn:
        run_md = st.button("⚡ Run AI Markdown Analysis", type="primary", use_container_width=True)
    with col_info:
        st.markdown("""
        <div style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;
             padding:10px 14px;display:flex;align-items:center;gap:10px;">
            <div style="width:6px;height:6px;border-radius:50%;background:#818cf8;
                 animation:pulse 2s infinite;flex-shrink:0;"></div>
            <span style="color:#64748b;font-size:0.78rem;font-family:'Space Grotesk',sans-serif;">
                Gemini AI analyzes stock risk, velocity & margins to recommend the optimal discount
            </span>
        </div>
        """, unsafe_allow_html=True)

    if run_md:
        with st.spinner("AI agents processing..."):
            st.session_state["markdown_result"] = run_coordinator(sku)
            st.session_state["markdown_sku_id"] = selected_id
            from utils.history_manager import save_decision
            save_decision(dict(sku), st.session_state["markdown_result"])
            

    if st.session_state.get("markdown_result") and st.session_state.get("markdown_sku_id") == selected_id:
        result       = st.session_state["markdown_result"]
        markdown_pct = result["recommended_markdown"]
        new_price    = result["new_price"]
        strategy     = result["strategy"]
        confidence   = result["confidence"]
        reasoning    = result["reasoning"]
        risk_level   = result["risk_level"]
        pricing      = result["pricing"]
        inventory    = result["inventory"]
        demand       = result["demand"]

        md_color = "#10b981" if markdown_pct < 15 else "#f59e0b" if markdown_pct < 30 else "#ef4444"

        # Decision card
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(14,165,233,0.08),rgba(99,102,241,0.08));
             border:1px solid rgba(14,165,233,0.25); border-radius:16px;
             padding:28px 32px; margin:1rem 0; position:relative; overflow:hidden;
             animation: fadeSlideIn 0.5s ease;">
            <div style="position:absolute;top:0;left:0;right:0;height:3px;
                 background:linear-gradient(90deg,#0ea5e9,#6366f1);"></div>
            <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;
                 border-radius:50%;background:radial-gradient(circle,rgba(14,165,233,0.08),transparent);"></div>
            <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:16px;">
                <div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                         color:#38bdf8;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:8px;">
                        ● GEMINI DECISION · LIVE
                    </div>
                    <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:2rem;
                         font-weight:900;color:#f8fafc;line-height:1.1;">
                        <span style="color:{md_color};">{markdown_pct:.0f}% Markdown</span>
                        <span style="color:#475569;font-size:1.2rem;"> → </span>
                        <span style="color:#38bdf8;">${new_price:.2f}</span>
                    </div>
                    <div style="margin-top:10px;display:flex;gap:16px;flex-wrap:wrap;">
                        <span style="background:#1e293b;border-radius:6px;padding:4px 10px;
                              font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#94a3b8;">
                            Strategy: <b style="color:#e2e8f0;">{strategy}</b>
                        </span>
                        <span style="background:#1e293b;border-radius:6px;padding:4px 10px;
                              font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#94a3b8;">
                            Confidence: <b style="color:#10b981;">{confidence:.0f}%</b>
                        </span>
                        <span style="background:#1e293b;border-radius:6px;padding:4px 10px;
                              font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#94a3b8;">
                            Risk: <b style="color:{md_color};">{risk_level}</b>
                        </span>
                    </div>
                </div>
            </div>
            <div style="margin-top:18px;padding:14px 16px;
                 background:rgba(255,255,255,0.03);border-radius:8px;
                 border-left:3px solid #6366f1;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                     color:#64748b;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:6px;">
                    AI Reasoning
                </div>
                <div style="color:#cbd5e1;font-size:0.88rem;line-height:1.7;">{reasoning}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Confidence Meter ───────────────────────────────────────────────
        conf_color  = "#10b981" if confidence >= 70 else "#f59e0b" if confidence >= 50 else "#ef4444"
        conf_label  = "HIGH CONFIDENCE" if confidence >= 70 else "MODERATE CONFIDENCE" if confidence >= 50 else "LOW CONFIDENCE"
        conf_icon   = "🟢" if confidence >= 70 else "🟡" if confidence >= 50 else "🔴"
        conf_tip    = (
            "Gemini is highly confident — strong signal to act on this recommendation."
            if confidence >= 70 else
            "Moderate confidence — review reasoning carefully before applying markdown."
            if confidence >= 50 else
            "Low confidence — treat as a suggestion only. Manual review strongly recommended."
        )
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#0a0f1e);
             border:1px solid #1e293b; border-radius:12px; padding:18px 22px;
             margin:1rem 0; position:relative; overflow:hidden;">
            <div style="position:absolute;top:0;left:0;right:0;height:2px;
                 background:linear-gradient(90deg,{conf_color},transparent);"></div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <div>
                    <span style="font-family:'JetBrains Mono',monospace; font-size:0.65rem;
                          color:#64748b; text-transform:uppercase; letter-spacing:0.12em;">
                        AI Confidence Meter
                    </span>
                    <span style="margin-left:10px; font-family:'JetBrains Mono',monospace;
                          font-size:0.68rem; color:{conf_color}; font-weight:700;">
                        {conf_icon} {conf_label}
                    </span>
                </div>
                <span style="font-family:'Bricolage Grotesque',sans-serif;
                      font-size:1.8rem; font-weight:900; color:{conf_color};">
                    {confidence:.0f}%
                </span>
            </div>
            <!-- Progress bar track -->
            <div style="background:#1e293b; border-radius:999px; height:10px; overflow:hidden;">
                <div style="width:{confidence:.0f}%;height:100%;border-radius:999px;
                     background:linear-gradient(90deg,{conf_color}88,{conf_color});
                     transition:width 1s ease;
                     box-shadow:0 0 8px {conf_color}66;">
                </div>
            </div>
            <!-- Markers -->
            <div style="display:flex; justify-content:space-between;
                 font-family:'JetBrains Mono',monospace; font-size:0.6rem;
                 color:#334155; margin-top:5px;">
                <span>0%</span>
                <span style="color:#ef4444;">50% Low</span>
                <span style="color:#f59e0b;">70% Moderate</span>
                <span style="color:#10b981;">100% High</span>
            </div>
            <div style="margin-top:10px; color:#475569; font-size:0.78rem;
                 font-style:italic; line-height:1.4;">{conf_tip}</div>
        </div>
        """, unsafe_allow_html=True)

        # Impact metrics
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#10b981;
             text-transform:uppercase; letter-spacing:0.15em; margin:1.2rem 0 0.6rem 0;">
            ▸ Impact Analysis
        </div>
        """, unsafe_allow_html=True)
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Original Price",  f"${sku['price']:.2f}")
        c2.metric("New Price",       f"${new_price:.2f}",              f"-${sku['price']-new_price:.2f}")
        c3.metric("Margin After",    f"{pricing['margin_after']:.1f}%",f"-{pricing['margin_loss']:.1f}pp", delta_color="inverse")
        c4.metric("Units / Week",    f"{inventory['units_sold_7days']}")
        c5.metric("Revenue / Week",  f"${demand['revenue_forecast']:,.2f}")

        # Agent cards
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#10b981;
             text-transform:uppercase; letter-spacing:0.15em; margin:1.2rem 0 0.6rem 0;">
            ▸ Agent Breakdown
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        agents = [
            {
                "icon": "💰", "label": "Pricing Agent", "color": "#38bdf8",
                "rows": [
                    ("Margin Before", f"{pricing['margin_before']:.1f}%", "#e2e8f0"),
                    ("Margin After",  f"{pricing['margin_after']:.1f}%",  "#e2e8f0"),
                    ("Acceptable",    pricing['acceptable'], "#10b981" if pricing['acceptable']=="Yes" else "#ef4444"),
                ],
                "summary": pricing['summary']
            },
            {
                "icon": "📦", "label": "Inventory Agent", "color": "#818cf8",
                "rows": [
                    ("Units Sold / 7d",  str(inventory['units_sold_7days']),  "#e2e8f0"),
                    ("Stock Remaining",  str(inventory['stock_remaining']),   "#e2e8f0"),
                    ("Days to Clear",    str(inventory['days_to_clear']),     "#f59e0b"),
                ],
                "summary": inventory['summary']
            },
            {
                "icon": "📈", "label": "Demand Agent", "color": "#10b981",
                "rows": [
                    ("Demand Uplift",    f"{demand['demand_uplift']:.1f}%",   "#10b981"),
                    ("Weekly Revenue",   f"${demand['revenue_forecast']:,.2f}", "#e2e8f0"),
                    ("Revenue Δ",        f"{'+'if demand['revenue_change']>=0 else ''}{demand['revenue_change']:,.2f}",
                                         "#10b981" if demand['revenue_change']>=0 else "#ef4444"),
                ],
                "summary": demand['summary']
            },
        ]

        for col, agent in zip([col1,col2,col3], agents):
            rows_html = "".join([
                f"""<div style="display:flex;justify-content:space-between;align-items:center;
                     padding:7px 0;border-bottom:1px solid #1e293b;">
                    <span style="color:#64748b;font-size:0.75rem;font-family:'JetBrains Mono',monospace;">{r[0]}</span>
                    <span style="color:{r[2]};font-weight:700;font-size:0.88rem;font-family:'Space Grotesk',sans-serif;">{r[1]}</span>
                </div>"""
                for r in agent["rows"]
            ])
            col.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,#0a0f1e);
                 border:1px solid #1e293b; border-radius:12px; padding:18px;
                 position:relative; overflow:hidden; height:100%;">
                <div style="position:absolute;top:0;left:0;right:0;height:2px;
                     background:{agent['color']};opacity:0.6;"></div>
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
                    <span style="font-size:1rem;">{agent['icon']}</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                          color:{agent['color']};text-transform:uppercase;letter-spacing:0.1em;">
                        {agent['label']}
                    </span>
                </div>
                {rows_html}
                <div style="color:#475569;font-size:0.75rem;line-height:1.5;
                     margin-top:12px;font-style:italic;">{agent['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("🔍 Raw Gemini Response"):
            st.code(result["decision_response"], language="text")

        # ══════════════════════════════════════════════════════════════════
        # 🔔 ALERT SYSTEM
        # ══════════════════════════════════════════════════════════════════
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#ef4444;
             text-transform:uppercase; letter-spacing:0.15em; margin:1.5rem 0 0.8rem 0;">
            ▸ Smart Alerts
        </div>
        """, unsafe_allow_html=True)

        alerts = []

        # Margin alert — below 15%
        margin_after_val = pricing.get("margin_after", 0)
        if margin_after_val < 15:
            alerts.append({
                "type": "error",
                "icon": "⛔",
                "title": "MARGIN ALERT",
                "msg": f"Margin dropped to {margin_after_val:.1f}% after markdown — below the 15% minimum threshold. Consider a smaller discount."
            })

        # Stockout alert — less than 14 days to clear
        days_to_clear_val = inventory.get("days_to_clear", 9999)
        stock_rem_val     = inventory.get("stock_remaining", 0)
        if days_to_clear_val < 14 and stock_rem_val > 0:
            alerts.append({
                "type": "warning",
                "icon": "⚠️",
                "title": "STOCKOUT ALERT",
                "msg": f"Stock will run out in {days_to_clear_val} days at this markdown rate. Risk of lost sales — consider replenishment or phased markdown."
            })

        # Already out of stock
        if stock_rem_val == 0:
            alerts.append({
                "type": "warning",
                "icon": "📦",
                "title": "STOCK CLEARED",
                "msg": "All stock expected to clear within 7 days at this markdown. No further markdown needed."
            })

        # Revenue drop alert
        revenue_change_val = demand.get("revenue_change", 0)
        if revenue_change_val < -50:
            alerts.append({
                "type": "warning",
                "icon": "📉",
                "title": "REVENUE DROP ALERT",
                "msg": f"Weekly revenue is expected to drop by ${abs(revenue_change_val):,.2f} compared to baseline. Evaluate if stock clearance justifies the loss."
            })

        # All good
        if not alerts:
            alerts.append({
                "type": "success",
                "icon": "✅",
                "title": "ALL SYSTEMS HEALTHY",
                "msg": f"Margin at {margin_after_val:.1f}% (above 15% threshold). Stock clears in {days_to_clear_val} days. Revenue impact is acceptable."
            })

        for alert in alerts:
            color_map = {
                "error":   ("#ef4444", "rgba(239,68,68,0.08)",   "rgba(239,68,68,0.2)"),
                "warning": ("#f59e0b", "rgba(245,158,11,0.08)",  "rgba(245,158,11,0.2)"),
                "success": ("#10b981", "rgba(16,185,129,0.08)",  "rgba(16,185,129,0.2)"),
            }
            clr, bg, border = color_map[alert["type"]]
            st.markdown(f"""
            <div style="background:{bg}; border:1px solid {border}; border-left:4px solid {clr};
                 border-radius:8px; padding:12px 16px; margin-bottom:8px;
                 display:flex; align-items:flex-start; gap:12px;">
                <span style="font-size:1.1rem;">{alert['icon']}</span>
                <div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem;
                         color:{clr}; text-transform:uppercase; letter-spacing:0.1em;
                         font-weight:700; margin-bottom:3px;">{alert['title']}</div>
                    <div style="color:#cbd5e1; font-size:0.82rem; line-height:1.5;">{alert['msg']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════
        # 📊 4-WEEK SIMULATION TABLE
        # ══════════════════════════════════════════════════════════════════
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#f59e0b;
             text-transform:uppercase; letter-spacing:0.15em; margin:1.5rem 0 0.8rem 0;">
            ▸ 4-Week Markdown Simulation Plan
        </div>
        """, unsafe_allow_html=True)

        from config.settings import WEEK_DISCOUNTS, COST_MULTIPLIER, MIN_ACCEPTABLE_MARGIN

        price_val    = float(sku.get("price", 0))
        velocity_val = float(sku.get("sales_velocity", 0))
        stock_val    = float(sku.get("quantity", 0))
        cost_val     = price_val * COST_MULTIPLIER

        # Build 4-week simulation locally (no extra API calls)
        week_rows   = []
        stock_left  = stock_val
        base_rev    = velocity_val * 7 * price_val   # baseline weekly revenue

        for i, disc in enumerate(WEEK_DISCOUNTS):
            week_num       = i + 1
            new_p          = round(price_val * (1 - disc / 100), 2)
            demand_uplift  = disc * 2.0              # 2% uplift per 1% markdown
            new_vel        = velocity_val * (1 + demand_uplift / 100)
            units_sold     = max(1, round(new_vel * 7)) if new_vel > 0 else 0
            units_sold     = min(units_sold, int(stock_left))   # can't sell more than stock
            stock_left     = max(0, stock_left - units_sold)
            revenue        = round(units_sold * new_p, 2)
            margin_pct     = round((new_p - cost_val) / new_p * 100, 1) if new_p > 0 else 0
            rev_vs_base    = round(revenue - base_rev, 2)
            is_best        = (disc == markdown_pct)             # highlight AI-recommended week

            week_rows.append({
                "Week":           f"Week {week_num}",
                "Markdown":       f"{disc}%",
                "New Price":      f"${new_p:.2f}",
                "Units Sold":     units_sold,
                "Revenue":        f"${revenue:,.2f}",
                "vs Baseline":    f"{'+'if rev_vs_base>=0 else ''}{rev_vs_base:,.2f}",
                "Margin %":       f"{margin_pct:.1f}%",
                "Stock Left":     int(stock_left),
                "Status":         "⭐ AI Pick" if is_best else ("✅ Healthy" if margin_pct >= MIN_ACCEPTABLE_MARGIN else "⚠️ Low Margin"),
            })

        sim_df = pd.DataFrame(week_rows)
        st.dataframe(sim_df, use_container_width=True, hide_index=True)

        st.caption(
            f"⭐ AI Pick = Week recommended by Gemini  |  "
            f"Stock starts at {int(stock_val)} units  |  "
            f"Baseline weekly revenue (no markdown): ${base_rev:,.2f}  |  "
            f"Margin floor: {MIN_ACCEPTABLE_MARGIN}%"
        )

        # ── Export CSV ─────────────────────────────────────────────────────
        import io
        export_df = sim_df.copy()

        # Add product info columns at the front
        export_df.insert(0, "Product",  sku.get("product_name", ""))
        export_df.insert(1, "SKU ID",   sku.get("product_id",   ""))
        export_df.insert(2, "Category", sku.get("main_category",""))
        export_df.insert(3, "Original Price", f"${price_val:.2f}")
        export_df.insert(4, "AI Recommended Markdown", f"{markdown_pct:.0f}%")
        export_df.insert(5, "AI Strategy",  strategy)
        export_df.insert(6, "AI Confidence", f"{confidence:.0f}%")
        export_df.insert(7, "AI Reasoning", reasoning)

        csv_buffer = io.StringIO()
        export_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        product_name_clean = sku.get("product_name", "product").replace(" ", "_").replace("/", "-")[:30]

        st.download_button(
            label="⬇️ Download 4-Week Decision Report (CSV)",
            data=csv_data,
            file_name=f"markdown_decision_{product_name_clean}.csv",
            mime="text/csv",
            use_container_width=True,
        )

        # ══════════════════════════════════════════════════════════════════
        # 📈 CHARTS AFTER AI DECISION
        # ══════════════════════════════════════════════════════════════════
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#818cf8;
             text-transform:uppercase; letter-spacing:0.15em; margin:1.5rem 0 0.8rem 0;">
            ▸ Visual Impact Analysis
        </div>
        """, unsafe_allow_html=True)

        chart_col1, chart_col2, chart_col3 = st.columns(3)

        # Pull numeric values from week_rows for charts
        weeks_labels = [r["Week"] for r in week_rows]
        revenues_num = [float(r["Revenue"].replace("$","").replace(",","")) for r in week_rows]
        margins_num  = [float(r["Margin %"].replace("%","")) for r in week_rows]
        stock_num    = [r["Stock Left"] for r in week_rows]

        # Chart 1 — Revenue before vs after per week (bar)
        with chart_col1:
            st.markdown("<div style='color:#94a3b8;font-size:0.78rem;margin-bottom:6px;'>💵 Revenue by Week</div>", unsafe_allow_html=True)
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                name="Baseline", x=weeks_labels,
                y=[round(base_rev, 2)] * 4,
                marker_color="rgba(100,116,139,0.4)",
                text=[f"${base_rev:,.0f}"] * 4, textposition="outside"
            ))
            fig1.add_trace(go.Bar(
                name="With Markdown", x=weeks_labels,
                y=revenues_num,
                marker_color=["#0ea5e9" if r["Status"] != "⭐ AI Pick" else "#10b981" for r in week_rows],
                text=[f"${v:,.0f}" for v in revenues_num], textposition="outside"
            ))
            fig1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5e1"),
                barmode="group", height=280,
                showlegend=True,
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
                margin=dict(t=20, b=30, l=0, r=0),
                xaxis=dict(gridcolor="#1e293b"),
                yaxis=dict(title="Revenue ($)", gridcolor="#1e293b"),
            )
            st.plotly_chart(fig1, use_container_width=True)

        # Chart 2 — Margin % trend line across 4 weeks
        with chart_col2:
            st.markdown("<div style='color:#94a3b8;font-size:0.78rem;margin-bottom:6px;'>📉 Margin % Trend</div>", unsafe_allow_html=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=weeks_labels, y=margins_num,
                mode="lines+markers+text",
                line=dict(color="#818cf8", width=2.5),
                marker=dict(size=8, color=["#10b981" if m >= MIN_ACCEPTABLE_MARGIN else "#ef4444" for m in margins_num]),
                text=[f"{m:.1f}%" for m in margins_num],
                textposition="top center",
                name="Margin %"
            ))
            # Margin floor line
            fig2.add_hline(
                y=MIN_ACCEPTABLE_MARGIN,
                line_dash="dash", line_color="#ef4444",
                annotation_text=f"Min {MIN_ACCEPTABLE_MARGIN}%",
                annotation_font_color="#ef4444", annotation_font_size=10
            )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5e1"),
                height=280,
                margin=dict(t=20, b=30, l=0, r=0),
                xaxis=dict(gridcolor="#1e293b"),
                yaxis=dict(title="Margin %", gridcolor="#1e293b", range=[0, max(margins_num) + 10]),
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Chart 3 — Stock clearance projection (area chart)
        with chart_col3:
            st.markdown("<div style='color:#94a3b8;font-size:0.78rem;margin-bottom:6px;'>📦 Stock Clearance</div>", unsafe_allow_html=True)
            # Include week 0 (starting stock)
            stock_with_start = [int(stock_val)] + stock_num
            weeks_with_start = ["Start"] + weeks_labels
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=weeks_with_start, y=stock_with_start,
                mode="lines+markers+text",
                fill="tozeroy",
                fillcolor="rgba(14,165,233,0.1)",
                line=dict(color="#0ea5e9", width=2.5),
                marker=dict(size=7, color="#38bdf8"),
                text=[f"{s}" for s in stock_with_start],
                textposition="top center",
                name="Stock Left"
            ))
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5e1"),
                height=280,
                margin=dict(t=20, b=30, l=0, r=0),
                xaxis=dict(gridcolor="#1e293b"),
                yaxis=dict(title="Units Remaining", gridcolor="#1e293b"),
                showlegend=False
            )
            st.plotly_chart(fig3, use_container_width=True)

        st.caption("🟢 Green bars = AI recommended week  |  🔴 Red dots = margin below floor  |  Area chart shows stock depleting week by week")

    # ── Competitor Intelligence ────────────────────────────────────────────
    render_competitor_section(sku)