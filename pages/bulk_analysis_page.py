"""
pages/bulk_analysis_page.py
Bulk AI Analysis — run Gemini on all HIGH risk SKUs at once.
"""
import streamlit as st
import pandas as pd
import time
from utils.data_loader import compute_sku_metrics, get_sku
from agents.coordinator_agent import run_coordinator
from utils.history_manager import save_decision

def render():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Bricolage+Grotesque:wght@800;900&display=swap');
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: #020817 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stAppViewContainer"]::before {
        content:''; position:fixed; top:0; left:0; width:100%; height:100%; z-index:0;
        background-image:
            linear-gradient(rgba(56,189,248,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56,189,248,0.03) 1px, transparent 1px);
        background-size:40px 40px; pointer-events:none;
    }
    [data-testid="metric-container"] {
        background:linear-gradient(135deg,#0f172a,#0a0f1e) !important;
        border:1px solid #1e293b !important; border-radius:12px !important;
        padding:18px !important; position:relative !important; overflow:hidden !important;
    }
    [data-testid="metric-container"]::before {
        content:''; position:absolute; top:0; left:0; right:0; height:2px;
        background:linear-gradient(90deg,#ef4444,#f59e0b); opacity:0.7;
    }
    [data-testid="stMetricLabel"] { color:#64748b !important; font-size:0.68rem !important; text-transform:uppercase !important; letter-spacing:0.12em !important; font-family:'JetBrains Mono',monospace !important; }
    [data-testid="stMetricValue"] { color:#f8fafc !important; font-family:'Bricolage Grotesque',sans-serif !important; font-size:1.5rem !important; font-weight:800 !important; }
    .stButton > button {
        background:linear-gradient(135deg,#ef4444,#f59e0b) !important;
        color:white !important; border:none !important; border-radius:8px !important;
        font-family:'Space Grotesk',sans-serif !important; font-weight:600 !important;
        padding:12px 28px !important;
        box-shadow:0 0 20px rgba(239,68,68,0.3) !important;
    }
    .stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 0 30px rgba(239,68,68,0.5) !important; }
    [data-testid="stDataFrame"] { border:1px solid #1e293b !important; border-radius:10px !important; }
    .stProgress > div > div > div { background:linear-gradient(90deg,#ef4444,#f59e0b) !important; }
    hr { border-color:#1e293b !important; }
    @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.8)} }
    @keyframes fadeSlideIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.5rem;animation:fadeSlideIn 0.6s ease;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#ef4444;
                 animation:pulse 2s infinite;box-shadow:0 0 8px #ef4444;"></div>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                  color:#ef4444;text-transform:uppercase;letter-spacing:0.15em;">Bulk AI Engine</span>
        </div>
        <h1 style="font-family:'Bricolage Grotesque',sans-serif;font-size:2.2rem;
             font-weight:900;margin:0;
             background:linear-gradient(135deg,#f8fafc,#ef4444,#f59e0b);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            Bulk Markdown Analysis
        </h1>
        <p style="color:#475569;font-size:0.88rem;margin-top:6px;">
            Run Gemini AI on multiple HIGH risk SKUs at once · Results saved to history automatically
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Load data ─────────────────────────────────────────────────────────
    with st.spinner("Loading SKU data..."):
        df = compute_sku_metrics()

    high_risk_df = df[df["clearance_risk"] == "HIGH"].copy()
    total_high   = len(high_risk_df)

    # ── Summary bar ───────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#ef4444;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
        ▸ High Risk Inventory Overview
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 High Risk SKUs",    total_high)
    c2.metric("📦 Total Stock at Risk", f"{int(high_risk_df['quantity'].sum()):,}")
    c3.metric("💰 Revenue at Risk",    f"${high_risk_df['total_revenue'].sum():,.0f}")
    c4.metric("📊 Avg Sell-Through",   f"{high_risk_df['sell_through_rate'].mean():.1f}%")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Config ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#ef4444;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
        ▸ Configure Batch
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        cats = ["All"] + sorted(high_risk_df["main_category"].dropna().unique().tolist())
        cat_filter = st.selectbox("Filter by Category", cats)
    with col2:
        abc_filter = st.selectbox("Filter by ABC Class", ["All", "A", "B", "C"])
    with col3:
        batch_size = st.slider("Max SKUs to analyze", min_value=1, max_value=min(20, total_high), value=min(5, total_high))

    # Apply filters
    batch_df = high_risk_df.copy()
    if cat_filter != "All":
        batch_df = batch_df[batch_df["main_category"] == cat_filter]
    if abc_filter != "All":
        batch_df = batch_df[batch_df["abc_class"] == abc_filter]

    # Sort by worst first — highest stock, lowest velocity
    batch_df = batch_df.sort_values(["quantity", "sales_velocity"], ascending=[False, True])
    batch_df = batch_df.head(batch_size)

    # ── Preview table ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#ef4444;
         text-transform:uppercase;letter-spacing:0.15em;margin:1rem 0 0.6rem 0;">
        ▸ SKUs Queued for Analysis ({len(batch_df)})
    </div>
    """, unsafe_allow_html=True)

    preview = batch_df[["product_name","main_category","price","quantity","sales_velocity","sell_through_rate","abc_class"]].copy()
    preview["price"]            = preview["price"].map("${:.2f}".format)
    preview["quantity"]         = preview["quantity"].astype(int)
    preview["sales_velocity"]   = preview["sales_velocity"].map("{:.4f}/day".format)
    preview["sell_through_rate"]= preview["sell_through_rate"].map("{:.1f}%".format)
    preview.columns             = ["Product","Category","Price","Stock","Velocity","Sell-Through","ABC"]
    st.dataframe(preview, use_container_width=True, hide_index=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Run button ────────────────────────────────────────────────────────
    col_btn, col_warn = st.columns([2, 3])
    with col_btn:
        run_bulk = st.button(f"⚡ Run AI on {len(batch_df)} SKUs", type="primary", use_container_width=True)
    with col_warn:
        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;
             padding:10px 14px;display:flex;align-items:center;gap:10px;margin-top:4px;">
            <span style="color:#f59e0b;font-size:1rem;">⚠️</span>
            <span style="color:#64748b;font-size:0.78rem;">
                This will make <strong style="color:#e2e8f0;">{len(batch_df)} AI API calls</strong>.
                Each takes ~5–10 seconds. Total ~{len(batch_df)*7}–{len(batch_df)*10}s.
            </span>
        </div>
        """, unsafe_allow_html=True)

    # ── Run bulk analysis ─────────────────────────────────────────────────
    if run_bulk:
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#f59e0b;
             text-transform:uppercase;letter-spacing:0.15em;margin:1rem 0 0.6rem 0;">
            ▸ Processing...
        </div>
        """, unsafe_allow_html=True)

        results   = []
        progress  = st.progress(0)
        status    = st.empty()
        live_feed = st.empty()

        for i, (_, row) in enumerate(batch_df.iterrows()):
            sku = row
            pct = (i + 1) / len(batch_df)
            status.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.8rem;color:#38bdf8;">
                Analyzing {i+1}/{len(batch_df)}: <b style="color:#f8fafc;">{sku['product_name']}</b>
            </div>
            """, unsafe_allow_html=True)

            try:
                result = run_coordinator(sku)
                save_decision(dict(sku), result)

                results.append({
                    "product_name"        : sku["product_name"],
                    "category"            : sku.get("main_category",""),
                    "original_price"      : sku["price"],
                    "recommended_markdown": result["recommended_markdown"],
                    "new_price"           : result["new_price"],
                    "strategy"            : result["strategy"],
                    "confidence"          : result["confidence"],
                    "risk_level"          : result["risk_level"],
                    "margin_after"        : result["pricing"]["margin_after"],
                    "revenue_forecast"    : result["demand"]["revenue_forecast"],
                    "days_to_clear"       : result["inventory"]["days_to_clear"],
                    "reasoning"           : result["reasoning"],
                    "status"              : "✅ Done",
                })
            except Exception as e:
                results.append({
                    "product_name"        : sku["product_name"],
                    "category"            : sku.get("main_category",""),
                    "original_price"      : sku["price"],
                    "recommended_markdown": 0,
                    "new_price"           : sku["price"],
                    "strategy"            : "Error",
                    "confidence"          : 0,
                    "risk_level"          : "—",
                    "margin_after"        : 0,
                    "revenue_forecast"    : 0,
                    "days_to_clear"       : "—",
                    "reasoning"           : str(e),
                    "status"              : "❌ Failed",
                })

            # Live results table
            live_df = pd.DataFrame(results)
            live_feed.dataframe(
                live_df[["product_name","recommended_markdown","new_price","strategy","confidence","status"]].rename(columns={
                    "product_name":"Product","recommended_markdown":"Markdown %",
                    "new_price":"New Price","strategy":"Strategy",
                    "confidence":"Confidence","status":"Status"
                }),
                use_container_width=True, hide_index=True
            )
            progress.progress(pct)
            time.sleep(0.3)

        progress.progress(1.0)
        status.empty()
        st.session_state["bulk_results"] = results
        st.success(f"✅ Completed {len(results)} SKUs — {sum(1 for r in results if r['status']=='✅ Done')} succeeded, {sum(1 for r in results if '❌' in r['status'])} failed")

    # ── Show saved results ────────────────────────────────────────────────
    if st.session_state.get("bulk_results"):
        results = st.session_state["bulk_results"]
        res_df  = pd.DataFrame(results)
        done_df = res_df[res_df["status"] == "✅ Done"]

        if len(done_df) > 0:
            st.markdown("""
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#10b981;
                 text-transform:uppercase;letter-spacing:0.15em;margin:1.5rem 0 0.6rem 0;">
                ▸ Batch Summary
            </div>
            """, unsafe_allow_html=True)

            c1,c2,c3,c4 = st.columns(4)
            c1.metric("SKUs Analyzed",      len(done_df))
            c2.metric("Avg Markdown",        f"{done_df['recommended_markdown'].mean():.1f}%")
            c3.metric("Avg Confidence",      f"{done_df['confidence'].mean():.0f}%")
            c4.metric("Avg Rev Forecast",    f"${done_df['revenue_forecast'].mean():,.0f}")

            st.markdown("""
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#10b981;
                 text-transform:uppercase;letter-spacing:0.15em;margin:1rem 0 0.6rem 0;">
                ▸ Full Results
            </div>
            """, unsafe_allow_html=True)

            display = done_df[[
                "product_name","category","original_price","recommended_markdown",
                "new_price","strategy","confidence","risk_level","margin_after",
                "revenue_forecast","days_to_clear"
            ]].copy()
            display["original_price"]       = display["original_price"].map("${:.2f}".format)
            display["new_price"]            = display["new_price"].map("${:.2f}".format)
            display["recommended_markdown"] = display["recommended_markdown"].map("{:.0f}%".format)
            display["confidence"]           = display["confidence"].map("{:.0f}%".format)
            display["margin_after"]         = display["margin_after"].map("{:.1f}%".format)
            display["revenue_forecast"]     = display["revenue_forecast"].map("${:,.0f}".format)
            display.columns = [
                "Product","Category","Original $","Markdown %","New Price",
                "Strategy","Confidence","Risk","Margin After","Rev Forecast","Days to Clear"
            ]
            st.dataframe(display, use_container_width=True, hide_index=True)

            # Reasoning expander
            with st.expander("📖 View AI Reasoning for Each SKU"):
                for _, row in done_df.iterrows():
                    mc = "#10b981" if row["recommended_markdown"] < 15 else "#f59e0b" if row["recommended_markdown"] < 30 else "#ef4444"
                    st.markdown(f"""
                    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:10px;
                         padding:14px 18px;margin-bottom:10px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:8px;">
                            <span style="font-family:'Bricolage Grotesque',sans-serif;
                                  font-weight:800;color:#f8fafc;">{row['product_name']}</span>
                            <span style="background:{mc}22;color:{mc};border:1px solid {mc}44;
                                  border-radius:4px;padding:2px 10px;font-family:'JetBrains Mono',monospace;
                                  font-size:0.72rem;">{row['recommended_markdown']:.0f}% markdown → ${row['new_price']:.2f}</span>
                        </div>
                        <div style="color:#64748b;font-size:0.8rem;line-height:1.6;">{row['reasoning']}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Download
            csv = res_df.to_csv(index=False)
            st.download_button("📥 Download Bulk Results CSV", csv, "bulk_analysis_results.csv", "text/csv")