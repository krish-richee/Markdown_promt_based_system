import streamlit as st

st.set_page_config(
    page_title="RetailAI — SKU Markdown Simulator",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono&display=swap');
[data-testid="stSidebarNav"] { display:none !important; }
[data-testid="stSidebar"] { background:#0a0f1e !important; border-right:1px solid #1e293b !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:8px 0 24px 0;">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.2rem;font-weight:900;
             background:linear-gradient(135deg,#38bdf8,#818cf8);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            🛍️ RetailAI
        </div>
        <div style="color:#334155;font-size:0.68rem;margin-top:2px;
             font-family:'JetBrains Mono',monospace;">AI Markdown Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠 Home", "⚡ SKU Simulator", "🔴 Bulk Analysis", "🔖 Watchlist", "🕐 Decision History"],
        label_visibility="collapsed"
    )

if page == "🏠 Home":
    from pages.home_page import render
    render()
elif page == "⚡ SKU Simulator":
    from pages.sku_simulator import render
    render()
elif page == "🔴 Bulk Analysis":
    from pages.bulk_analysis_page import render
    render()
elif page == "🔖 Watchlist":
    from pages.watchlist_page import render
    render()
elif page == "🕐 Decision History":
    from pages.history_page import render
    render()