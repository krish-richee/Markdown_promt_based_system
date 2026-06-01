"""
pages/watchlist_page.py
SKU Watchlist — bookmark SKUs and monitor their risk status.
"""
import streamlit as st
import pandas as pd
import json
import os
from utils.data_loader import compute_sku_metrics

WATCHLIST_FILE = "data/watchlist.json"

def load_watchlist() -> list:
    if not os.path.exists(WATCHLIST_FILE):
        return []
    try:
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_watchlist(watchlist: list):
    os.makedirs("data", exist_ok=True)
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(watchlist, f, indent=2)

def add_to_watchlist(product_id: str, product_name: str, category: str, note: str = ""):
    wl = load_watchlist()
    ids = [w["product_id"] for w in wl]
    if product_id not in ids:
        wl.append({
            "product_id":   product_id,
            "product_name": product_name,
            "category":     category,
            "note":         note,
            "added_on":     pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
        })
        save_watchlist(wl)
        return True
    return False

def remove_from_watchlist(product_id: str):
    wl = [w for w in load_watchlist() if w["product_id"] != product_id]
    save_watchlist(wl)

def render():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Bricolage+Grotesque:wght@800;900&display=swap');
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background:#020817 !important; font-family:'Space Grotesk',sans-serif !important; color:#e2e8f0 !important;
    }
    [data-testid="stHeader"] { background:transparent !important; }
    [data-testid="stAppViewContainer"]::before {
        content:''; position:fixed; top:0; left:0; width:100%; height:100%; z-index:0;
        background-image: linear-gradient(rgba(56,189,248,0.03) 1px,transparent 1px), linear-gradient(90deg,rgba(56,189,248,0.03) 1px,transparent 1px);
        background-size:40px 40px; pointer-events:none;
    }
    [data-testid="metric-container"] {
        background:linear-gradient(135deg,#0f172a,#0a0f1e) !important;
        border:1px solid #1e293b !important; border-radius:12px !important; padding:18px !important;
        position:relative !important; overflow:hidden !important;
        transition:border-color 0.3s,transform 0.2s !important;
    }
    [data-testid="metric-container"]:hover { border-color:#f59e0b !important; transform:translateY(-2px) !important; }
    [data-testid="metric-container"]::before {
        content:''; position:absolute; top:0; left:0; right:0; height:2px;
        background:linear-gradient(90deg,#f59e0b,#f97316); opacity:0.7;
    }
    [data-testid="stMetricLabel"] { color:#64748b !important; font-size:0.68rem !important; text-transform:uppercase !important; letter-spacing:0.12em !important; font-family:'JetBrains Mono',monospace !important; }
    [data-testid="stMetricValue"] { color:#f8fafc !important; font-family:'Bricolage Grotesque',sans-serif !important; font-size:1.5rem !important; font-weight:800 !important; }
    .stButton > button {
        background:linear-gradient(135deg,#f59e0b,#f97316) !important;
        color:white !important; border:none !important; border-radius:8px !important;
        font-family:'Space Grotesk',sans-serif !important; font-weight:600 !important; padding:10px 24px !important;
        transition:all 0.3s !important;
    }
    .stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 0 20px rgba(245,158,11,0.4) !important; }
    .stSelectbox > div > div { background:#0f172a !important; border:1px solid #1e293b !important; border-radius:8px !important; }
    .stTextInput > div > div > input { background:#0f172a !important; border:1px solid #1e293b !important; border-radius:8px !important; color:#e2e8f0 !important; font-family:'Space Grotesk',sans-serif !important; }
    [data-testid="stDataFrame"] { border:1px solid #1e293b !important; border-radius:10px !important; }
    hr { border-color:#1e293b !important; }
    @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.8)} }
    @keyframes fadeSlideIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
    @keyframes alertPulse { 0%,100%{box-shadow:0 0 0 0 rgba(239,68,68,0.4)} 70%{box-shadow:0 0 0 8px rgba(239,68,68,0)} }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.5rem;animation:fadeSlideIn 0.6s ease;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#f59e0b;
                 animation:pulse 2s infinite;box-shadow:0 0 8px #f59e0b;"></div>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                  color:#f59e0b;text-transform:uppercase;letter-spacing:0.15em;">SKU Monitor</span>
        </div>
        <h1 style="font-family:'Bricolage Grotesque',sans-serif;font-size:2.2rem;
             font-weight:900;margin:0;
             background:linear-gradient(135deg,#f8fafc,#f59e0b,#f97316);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            SKU Watchlist
        </h1>
        <p style="color:#475569;font-size:0.88rem;margin-top:6px;">
            Bookmark SKUs to monitor · Get instant alerts when risk level changes to HIGH
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Load data ─────────────────────────────────────────────────────────
    with st.spinner("Loading SKU data..."):
        df = compute_sku_metrics()

    watchlist = load_watchlist()
    wl_ids    = [w["product_id"] for w in watchlist]

    # ── Add SKU section ───────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#f59e0b;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
        ▸ Add SKU to Watchlist
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        cat_opts = ["All"] + sorted(df["main_category"].dropna().unique().tolist())
        add_cat  = st.selectbox("Filter by Category", cat_opts, key="add_cat")
    filtered_add = df if add_cat == "All" else df[df["main_category"] == add_cat]
    not_watched  = filtered_add[~filtered_add["product_id"].isin(wl_ids)]
    with col2:
        if len(not_watched) > 0:
            selected_add = st.selectbox(
                "Select SKU to Watch",
                not_watched["product_id"].tolist(),
                format_func=lambda x: f"{x} · {not_watched[not_watched['product_id']==x]['product_name'].values[0]}"
            )
        else:
            st.info("All SKUs in this category are already watched.")
            selected_add = None
    with col3:
        note = st.text_input("Note (optional)", placeholder="e.g. check weekly")

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("🔖 Add to Watchlist", use_container_width=True) and selected_add:
            row = df[df["product_id"] == selected_add].iloc[0]
            added = add_to_watchlist(
                selected_add,
                row["product_name"],
                row["main_category"],
                note
            )
            if added:
                st.success(f"✅ Added **{row['product_name']}** to watchlist")
                st.rerun()
            else:
                st.warning("Already in watchlist")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Watchlist display ─────────────────────────────────────────────────
    watchlist = load_watchlist()

    if not watchlist:
        st.markdown("""
        <div style="background:#0f172a;border:1px dashed #1e293b;border-radius:14px;
             padding:40px;text-align:center;">
            <div style="font-size:2rem;margin-bottom:10px;opacity:0.3;">🔖</div>
            <div style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
                 color:#334155;font-size:1rem;margin-bottom:4px;">Watchlist is Empty</div>
            <div style="color:#1e293b;font-size:0.82rem;">
                Use the form above to add SKUs you want to monitor
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Merge watchlist with live SKU data
    wl_df    = pd.DataFrame(watchlist)
    live_wl  = wl_df.merge(
        df[["product_id","price","quantity","sales_velocity",
            "sell_through_rate","clearance_risk","abc_class","days_of_stock"]],
        on="product_id", how="left"
    )

    # ── Summary KPIs ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#f59e0b;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
        ▸ Watchlist Summary
    </div>
    """, unsafe_allow_html=True)

    total_watched = len(live_wl)
    high_watched  = len(live_wl[live_wl["clearance_risk"] == "HIGH"])
    med_watched   = len(live_wl[live_wl["clearance_risk"] == "MEDIUM"])
    low_watched   = len(live_wl[live_wl["clearance_risk"] == "LOW"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👀 Watching",     total_watched)
    c2.metric("🔴 HIGH Alert",   high_watched,  delta="Needs action" if high_watched > 0 else "None", delta_color="inverse" if high_watched > 0 else "off")
    c3.metric("🟡 MEDIUM Risk",  med_watched)
    c4.metric("🟢 LOW Risk",     low_watched)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── HIGH risk alerts ──────────────────────────────────────────────────
    high_alerts = live_wl[live_wl["clearance_risk"] == "HIGH"]
    if len(high_alerts) > 0:
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#ef4444;
             text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
            ⚠️ HIGH Risk Alerts
        </div>
        """, unsafe_allow_html=True)

        for _, row in high_alerts.iterrows():
            st.markdown(f"""
            <div style="background:rgba(239,68,68,0.06);border:1.5px solid rgba(239,68,68,0.3);
                 border-radius:12px;padding:16px 20px;margin-bottom:10px;
                 animation:alertPulse 2s infinite;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
                    <div>
                        <div style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
                              color:#f8fafc;font-size:1rem;">{row['product_name']}</div>
                        <div style="color:#64748b;font-size:0.72rem;font-family:'JetBrains Mono',monospace;margin-top:2px;">
                            {row['product_id']} · {row['category']}
                        </div>
                    </div>
                    <div style="display:flex;gap:8px;flex-wrap:wrap;">
                        <span style="background:#ef444422;color:#ef4444;border:1px solid #ef444444;
                              border-radius:4px;padding:3px 10px;font-family:'JetBrains Mono',monospace;font-size:0.72rem;">
                            🔴 HIGH RISK
                        </span>
                        <span style="background:#1e293b;color:#94a3b8;border-radius:4px;
                              padding:3px 10px;font-family:'JetBrains Mono',monospace;font-size:0.72rem;">
                            Stock: {int(row['quantity'])} units
                        </span>
                        <span style="background:#1e293b;color:#94a3b8;border-radius:4px;
                              padding:3px 10px;font-family:'JetBrains Mono',monospace;font-size:0.72rem;">
                            {row['sell_through_rate']:.1f}% sold
                        </span>
                        <span style="background:#1e293b;color:#f59e0b;border-radius:4px;
                              padding:3px 10px;font-family:'JetBrains Mono',monospace;font-size:0.72rem;">
                            💡 Go to SKU Simulator
                        </span>
                    </div>
                </div>
                {f'<div style="color:#475569;font-size:0.75rem;margin-top:8px;font-style:italic;">Note: {row["note"]}</div>' if row.get("note") else ""}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── Full watchlist table ───────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#f59e0b;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
        ▸ All Watched SKUs
    </div>
    """, unsafe_allow_html=True)

    for _, row in live_wl.iterrows():
        risk        = row.get("clearance_risk", "—")
        risk_color  = {"HIGH":"#ef4444","MEDIUM":"#f59e0b","LOW":"#10b981"}.get(risk,"#64748b")
        risk_bg     = {"HIGH":"rgba(239,68,68,0.08)","MEDIUM":"rgba(245,158,11,0.08)","LOW":"rgba(16,185,129,0.08)"}.get(risk,"rgba(100,116,139,0.08)")
        abc         = row.get("abc_class","—")
        abc_color   = {"A":"#10b981","B":"#f59e0b","C":"#ef4444"}.get(abc,"#64748b")
        days        = int(row["days_of_stock"]) if row["days_of_stock"] < 9000 else 9999

        col_card, col_remove = st.columns([9, 1])
        with col_card:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;
                 padding:16px 20px;margin-bottom:8px;
                 border-left:3px solid {risk_color};">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
                    <div style="flex:1;min-width:200px;">
                        <div style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
                              color:#f8fafc;font-size:0.95rem;">{row['product_name']}</div>
                        <div style="color:#475569;font-size:0.7rem;font-family:'JetBrains Mono',monospace;margin-top:2px;">
                            {row['product_id']} · {row['category']} · Added {row['added_on']}
                        </div>
                        {f'<div style="color:#64748b;font-size:0.72rem;margin-top:4px;font-style:italic;">📝 {row["note"]}</div>' if row.get("note") else ""}
                    </div>
                    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
                        <span style="background:{risk_color}22;color:{risk_color};border:1px solid {risk_color}44;
                              border-radius:4px;padding:3px 10px;font-family:'JetBrains Mono',monospace;font-size:0.7rem;">
                            {risk} RISK
                        </span>
                        <span style="background:{abc_color}22;color:{abc_color};border:1px solid {abc_color}44;
                              border-radius:4px;padding:3px 10px;font-family:'JetBrains Mono',monospace;font-size:0.7rem;">
                            CLASS {abc}
                        </span>
                        <div style="display:flex;gap:12px;">
                            <div style="text-align:center;">
                                <div style="color:#64748b;font-size:0.6rem;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Price</div>
                                <div style="color:#f8fafc;font-weight:700;font-size:0.88rem;">${row['price']:.2f}</div>
                            </div>
                            <div style="text-align:center;">
                                <div style="color:#64748b;font-size:0.6rem;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Stock</div>
                                <div style="color:#f8fafc;font-weight:700;font-size:0.88rem;">{int(row['quantity'])}</div>
                            </div>
                            <div style="text-align:center;">
                                <div style="color:#64748b;font-size:0.6rem;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Sell-Thru</div>
                                <div style="color:#f8fafc;font-weight:700;font-size:0.88rem;">{row['sell_through_rate']:.1f}%</div>
                            </div>
                            <div style="text-align:center;">
                                <div style="color:#64748b;font-size:0.6rem;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Days Stock</div>
                                <div style="color:{risk_color};font-weight:700;font-size:0.88rem;">{days}d</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_remove:
            if st.button("✕", key=f"remove_{row['product_id']}", help="Remove from watchlist"):
                remove_from_watchlist(row["product_id"])
                st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Clear all ─────────────────────────────────────────────────────────
    col1, _ = st.columns([1, 4])
    with col1:
        if st.button("🗑️ Clear Entire Watchlist"):
            save_watchlist([])
            st.success("Watchlist cleared.")
            st.rerun()