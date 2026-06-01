"""
pages/history_page.py
Decision History — all past AI markdown decisions in one place.
"""
import streamlit as st
import pandas as pd
from utils.history_manager import load_all, clear_history

def render():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Bricolage+Grotesque:wght@800;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background: #020817 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #0f172a, #0a0f1e) !important;
        border: 1px solid #1e293b !important; border-radius: 12px !important;
        padding: 18px !important; position: relative !important; overflow: hidden !important;
    }
    [data-testid="metric-container"]::before {
        content:''; position:absolute; top:0; left:0; right:0; height:2px;
        background: linear-gradient(90deg,#38bdf8,#818cf8); opacity:0.6;
    }
    [data-testid="stMetricLabel"] { color:#64748b !important; font-size:0.68rem !important; text-transform:uppercase !important; letter-spacing:0.12em !important; font-family:'JetBrains Mono',monospace !important; }
    [data-testid="stMetricValue"] { color:#f8fafc !important; font-family:'Bricolage Grotesque',sans-serif !important; font-size:1.5rem !important; font-weight:800 !important; }
    .stButton > button {
        background: linear-gradient(135deg,#0ea5e9,#6366f1) !important;
        color:white !important; border:none !important; border-radius:8px !important;
        font-family:'Space Grotesk',sans-serif !important; font-weight:600 !important;
        padding:10px 24px !important;
    }
    [data-testid="stDataFrame"] { border:1px solid #1e293b !important; border-radius:10px !important; }
    hr { border-color:#1e293b !important; }
    @keyframes fadeSlideIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.5rem; animation:fadeSlideIn 0.5s ease;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <div style="width:7px;height:7px;border-radius:50%;background:#818cf8;
                 animation:pulse 2s infinite;box-shadow:0 0 8px #818cf8;"></div>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                  color:#818cf8;text-transform:uppercase;letter-spacing:0.15em;">Decision Log</span>
        </div>
        <h1 style="font-family:'Bricolage Grotesque',sans-serif;font-size:2rem;
             font-weight:900;margin:0;
             background:linear-gradient(135deg,#f8fafc,#818cf8);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            AI Markdown History
        </h1>
        <p style="color:#475569;font-size:0.85rem;margin-top:6px;">
            Every AI markdown decision made — saved automatically, persists across sessions
        </p>
    </div>
    """, unsafe_allow_html=True)

    history = load_all()

    if not history:
        st.markdown("""
        <div style="background:#0f172a;border:1px dashed #1e293b;border-radius:14px;
             padding:48px;text-align:center;margin-top:1rem;">
            <div style="font-size:2.5rem;margin-bottom:12px;opacity:0.3;">🕐</div>
            <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:1rem;
                 font-weight:800;color:#334155;margin-bottom:6px;">No Decisions Yet</div>
            <div style="color:#1e293b;font-size:0.82rem;">
                Go to the <strong style="color:#38bdf8;">SKU Simulator</strong>
                and run an AI analysis — it will appear here automatically
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Summary KPIs ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#818cf8;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
        ▸ Summary
    </div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame(history)
    total          = len(df)
    avg_markdown   = df["recommended_markdown"].mean()
    avg_confidence = df["confidence"].mean()
    avg_revenue    = df["revenue_forecast"].mean()
    unique_skus    = df["product_id"].nunique()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Decisions",   total)
    c2.metric("Unique SKUs",       unique_skus)
    c3.metric("Avg Markdown",      f"{avg_markdown:.1f}%")
    c4.metric("Avg Confidence",    f"{avg_confidence:.0f}%")
    c5.metric("Avg Rev Forecast",  f"${avg_revenue:,.0f}")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Filters ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#818cf8;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
        ▸ Filter & Search
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("Search product name", placeholder="Type to search...")
    with col2:
        cats = ["All"] + sorted(df["category"].dropna().unique().tolist())
        cat_filter = st.selectbox("Category", cats)
    with col3:
        risk_opts = ["All"] + sorted(df["risk_level"].dropna().unique().tolist())
        risk_filter = st.selectbox("Risk Level", risk_opts)

    filtered = df.copy()
    if search:
        filtered = filtered[filtered["product_name"].str.contains(search, case=False, na=False)]
    if cat_filter != "All":
        filtered = filtered[filtered["category"] == cat_filter]
    if risk_filter != "All":
        filtered = filtered[filtered["risk_level"] == risk_filter]

    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
         color:#475569;margin:6px 0 12px 0;">
        Showing {len(filtered)} of {total} decisions
    </div>
    """, unsafe_allow_html=True)

    # ── History table ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#818cf8;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
        ▸ Decision Log
    </div>
    """, unsafe_allow_html=True)

    display = filtered[[
        "timestamp", "product_name", "category",
        "original_price", "recommended_markdown", "new_price",
        "strategy", "confidence", "risk_level",
        "margin_after", "revenue_forecast", "days_to_clear"
    ]].copy().sort_values("timestamp", ascending=False)

    display["original_price"]       = display["original_price"].map("${:.2f}".format)
    display["new_price"]            = display["new_price"].map("${:.2f}".format)
    display["recommended_markdown"] = display["recommended_markdown"].map("{:.0f}%".format)
    display["confidence"]           = display["confidence"].map("{:.0f}%".format)
    display["margin_after"]         = display["margin_after"].map("{:.1f}%".format)
    display["revenue_forecast"]     = display["revenue_forecast"].map("${:,.0f}".format)

    display.columns = [
        "Time", "Product", "Category",
        "Original $", "Markdown %", "New Price",
        "Strategy", "Confidence", "Risk",
        "Margin After", "Rev Forecast", "Days to Clear"
    ]

    st.dataframe(display, use_container_width=True, hide_index=True)

    # ── Detail expander ───────────────────────────────────────────────────
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    with st.expander("📖 View AI Reasoning for Each Decision"):
        for _, row in filtered.sort_values("timestamp", ascending=False).iterrows():
            md_color = "#10b981" if row["recommended_markdown"] < 15 else "#f59e0b" if row["recommended_markdown"] < 30 else "#ef4444"
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:10px;
                 padding:14px 18px;margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                    <div>
                        <span style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
                              color:#f8fafc;font-size:0.95rem;">{row['product_name']}</span>
                        <span style="color:#475569;font-size:0.75rem;margin-left:8px;">{row['timestamp']}</span>
                    </div>
                    <span style="background:{md_color}22;color:{md_color};border:1px solid {md_color}44;
                          border-radius:4px;padding:2px 10px;font-family:'JetBrains Mono',monospace;
                          font-size:0.72rem;">{row['recommended_markdown']:.0f}% markdown</span>
                </div>
                <div style="color:#64748b;font-size:0.8rem;line-height:1.6;margin-top:8px;
                     font-family:'Space Grotesk',sans-serif;">{row['reasoning']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Download + Clear ──────────────────────────────────────────────────
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        csv = df.to_csv(index=False)
        st.download_button("📥 Export Full History as CSV", csv,
                           "markdown_decision_history.csv", "text/csv")
    with col2:
        if st.button("🗑️ Clear All History", type="secondary"):
            clear_history()
            st.success("History cleared.")
            st.rerun()