"""
pages/home_page.py
Executive Dashboard — the first thing you see when you open RetailAI.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_loader import compute_sku_metrics
from utils.history_manager import load_all

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
        background-size: 40px 40px; pointer-events:none;
    }
    [data-testid="metric-container"] {
        background: linear-gradient(135deg,#0f172a,#0a0f1e) !important;
        border: 1px solid #1e293b !important; border-radius:12px !important;
        padding:18px !important; position:relative !important; overflow:hidden !important;
        transition: border-color 0.3s, transform 0.2s !important;
    }
    [data-testid="metric-container"]:hover { border-color:#38bdf8 !important; transform:translateY(-2px) !important; }
    [data-testid="metric-container"]::before {
        content:''; position:absolute; top:0; left:0; right:0; height:2px;
        background:linear-gradient(90deg,#38bdf8,#818cf8); opacity:0.6;
    }
    [data-testid="stMetricLabel"] { color:#64748b !important; font-size:0.68rem !important; text-transform:uppercase !important; letter-spacing:0.12em !important; font-family:'JetBrains Mono',monospace !important; }
    [data-testid="stMetricValue"] { color:#f8fafc !important; font-family:'Bricolage Grotesque',sans-serif !important; font-size:1.6rem !important; font-weight:800 !important; }
    [data-testid="stDataFrame"] { border:1px solid #1e293b !important; border-radius:10px !important; }
    hr { border-color:#1e293b !important; margin:2rem 0 !important; }
    @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.8)} }
    @keyframes fadeSlideIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
    @keyframes shimmer { 0%{background-position:-200% center} 100%{background-position:200% center} }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:2rem;animation:fadeSlideIn 0.6s ease;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#10b981;
                 animation:pulse 2s infinite;box-shadow:0 0 8px #10b981;"></div>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                  color:#10b981;text-transform:uppercase;letter-spacing:0.15em;">LIVE · EXECUTIVE OVERVIEW</span>
        </div>
        <h1 style="font-family:'Bricolage Grotesque',sans-serif;font-size:2.4rem;
             font-weight:900;margin:0;line-height:1.1;
             background:linear-gradient(135deg,#f8fafc 0%,#38bdf8 50%,#818cf8 100%);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             background-size:200% auto;animation:shimmer 4s linear infinite;">
            RetailAI Command Center
        </h1>
        <p style="color:#475569;font-size:0.88rem;margin-top:6px;">
            Real-time inventory health · Risk exposure · AI decision history
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Load data ─────────────────────────────────────────────────────────
    with st.spinner("Loading live data..."):
        df      = compute_sku_metrics()
        history = load_all()

    total_skus    = len(df)
    high_risk     = len(df[df["clearance_risk"] == "HIGH"])
    medium_risk   = len(df[df["clearance_risk"] == "MEDIUM"])
    low_risk      = len(df[df["clearance_risk"] == "LOW"])
    dead_inv      = int(df["is_dead_inventory"].sum())
    revenue_at_risk = df[df["clearance_risk"] == "HIGH"]["total_revenue"].sum()
    total_stock_val = (df["quantity"] * df["price"]).sum()
    avg_sell_through = df["sell_through_rate"].mean()
    decisions_made  = len(history)

    # ── Top KPI row ───────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#38bdf8;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
        ▸ Inventory Health Snapshot
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Total SKUs",        total_skus)
    c2.metric("🔴 High Risk",      high_risk,   delta=f"{high_risk/total_skus*100:.0f}% of catalog", delta_color="inverse")
    c3.metric("🟡 Medium Risk",    medium_risk)
    c4.metric("🟢 Low Risk",       low_risk)
    c5.metric("💀 Dead Inventory", dead_inv,    delta="No movement", delta_color="inverse")
    c6.metric("AI Decisions Made", decisions_made)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    c1.metric("📦 Total Stock Value",   f"${total_stock_val:,.0f}")
    c2.metric("🔥 Revenue at Risk",     f"${revenue_at_risk:,.0f}", delta="High risk SKUs only", delta_color="inverse")
    c3.metric("📊 Avg Sell-Through",    f"{avg_sell_through:.1f}%")

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Two charts side by side ───────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#38bdf8;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.8rem;">
        ▸ Risk & Category Breakdown
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Risk donut chart
        risk_counts = df["clearance_risk"].value_counts()
        fig = go.Figure(go.Pie(
            labels=risk_counts.index.tolist(),
            values=risk_counts.values.tolist(),
            hole=0.65,
            marker_colors=["#ef4444","#f59e0b","#10b981"],
            textinfo="label+percent",
            textfont=dict(family="JetBrains Mono", size=11, color="#e2e8f0"),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10,b=10,l=10,r=10),
            height=260,
            showlegend=False,
            annotations=[dict(
                text=f"<b>{total_skus}</b><br><span style='font-size:10px'>SKUs</span>",
                x=0.5, y=0.5, font_size=18, font_color="#f8fafc",
                showarrow=False
            )]
        )
        st.markdown("""
        <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:16px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#64748b;
                 text-transform:uppercase;letter-spacing:0.12em;margin-bottom:4px;">Risk Distribution</div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Category bar chart
        cat_risk = df.groupby(["main_category","clearance_risk"]).size().reset_index(name="count")
        fig2 = px.bar(
            cat_risk, x="main_category", y="count", color="clearance_risk",
            color_discrete_map={"HIGH":"#ef4444","MEDIUM":"#f59e0b","LOW":"#10b981"},
            barmode="stack",
            labels={"main_category":"","count":"SKUs","clearance_risk":"Risk"}
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", family="Space Grotesk"),
            height=260, margin=dict(t=10,b=40,l=0,r=0),
            xaxis=dict(tickangle=-20, gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b"),
            legend=dict(title="", font=dict(color="#94a3b8",size=10),
                        orientation="h", yanchor="bottom", y=1.02),
        )
        st.markdown("""
        <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:16px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#64748b;
                 text-transform:uppercase;letter-spacing:0.12em;margin-bottom:4px;">Risk by Category</div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Top 10 HIGH risk SKUs ─────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#ef4444;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.6rem;">
        ▸ 🔴 Top 10 SKUs Needing Immediate Markdown
    </div>
    """, unsafe_allow_html=True)

    urgent = df[df["clearance_risk"] == "HIGH"].nlargest(10, "quantity")[[
        "product_name","main_category","price","quantity",
        "sales_velocity","days_of_stock","sell_through_rate","abc_class"
    ]].copy()

    urgent["days_of_stock"]    = urgent["days_of_stock"].clip(upper=9999).astype(int)
    urgent["sell_through_rate"]= urgent["sell_through_rate"].map("{:.1f}%".format)
    urgent["sales_velocity"]   = urgent["sales_velocity"].map("{:.4f}/day".format)
    urgent["price"]            = urgent["price"].map("${:.2f}".format)
    urgent["quantity"]         = urgent["quantity"].astype(int)
    urgent.columns = ["Product","Category","Price","Stock","Velocity","Days of Stock","Sell-Through","ABC"]

    st.dataframe(urgent, use_container_width=True, hide_index=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Recent AI decisions ───────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#818cf8;
         text-transform:uppercase;letter-spacing:0.15em;margin-bottom:0.8rem;">
        ▸ Recent AI Decisions
    </div>
    """, unsafe_allow_html=True)

    if not history:
        st.markdown("""
        <div style="background:#0f172a;border:1px dashed #1e293b;border-radius:10px;
             padding:24px;text-align:center;">
            <div style="color:#334155;font-size:0.85rem;">
                No decisions yet — go to <strong style="color:#818cf8;">SKU Simulator</strong>
                and run your first AI analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        recent = pd.DataFrame(history).tail(5).sort_values("timestamp", ascending=False)
        for _, row in recent.iterrows():
            md   = row["recommended_markdown"]
            mc   = "#10b981" if md < 15 else "#f59e0b" if md < 30 else "#ef4444"
            rc   = "#10b981" if row["risk_level"] == "LOW" else "#f59e0b" if row["risk_level"] == "MEDIUM" else "#ef4444"
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:10px;
                 padding:14px 18px;margin-bottom:8px;display:flex;
                 align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
                <div>
                    <span style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
                          color:#f8fafc;font-size:0.95rem;">{row['product_name']}</span>
                    <span style="color:#475569;font-size:0.72rem;margin-left:10px;
                          font-family:'JetBrains Mono',monospace;">{row['timestamp']}</span>
                </div>
                <div style="display:flex;gap:8px;align-items:center;">
                    <span style="background:{mc}22;color:{mc};border:1px solid {mc}44;
                          border-radius:4px;padding:2px 10px;font-family:'JetBrains Mono',monospace;
                          font-size:0.72rem;">{md:.0f}% markdown</span>
                    <span style="background:{rc}22;color:{rc};border:1px solid {rc}44;
                          border-radius:4px;padding:2px 10px;font-family:'JetBrains Mono',monospace;
                          font-size:0.72rem;">{row['risk_level']} risk</span>
                    <span style="color:#475569;font-size:0.78rem;
                          font-family:'Space Grotesk',sans-serif;">
                          ${row['new_price']:.2f} new price
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)