import streamlit as st
from agents.competitor_agent import run_competitor_agent

def render_competitor_section(sku):

    st.markdown("""
    <div style="height:1rem;"></div>
    <hr style="border-color:#1e293b; margin:0 0 1.5rem 0;">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
        <div style="width:6px;height:6px;border-radius:50%;background:#38bdf8;
             animation:pulse 2s infinite;box-shadow:0 0 8px #38bdf8;"></div>
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
              color:#38bdf8;text-transform:uppercase;letter-spacing:0.15em;">
            Competitor Intelligence · Live Web Search
        </span>
    </div>
    <p style="color:#475569;font-size:0.82rem;margin:4px 0 16px 16px;
       font-family:'Space Grotesk',sans-serif;">
        Real-time prices fetched via Tavily Search API · Analyzed by Gemini AI
    </p>
    """, unsafe_allow_html=True)

    col_btn, col_tog = st.columns([3, 1])
    with col_btn:
        run_comp = st.button("🌐 Search Competitor Prices", key="run_competitor", use_container_width=True)
    with col_tog:
        show_backend = st.checkbox("Show backend", value=False, key="comp_backend")

    if run_comp:
        with st.spinner("Scanning web for competitor prices..."):
            try:
                st.session_state["comp_result"] = run_competitor_agent(sku)
                st.session_state["comp_sku_id"] = sku.get("product_id")
            except Exception as e:
                import traceback
                st.error(f"❌ {type(e).__name__}: {e}")
                st.code(traceback.format_exc())
                return

    result = st.session_state.get("comp_result")

    if result is None:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0f172a,#0a0f1e);
             border:1px dashed #1e293b; border-radius:14px;
             padding:36px; text-align:center; margin-top:8px;">
            <div style="font-size:2rem;margin-bottom:12px;opacity:0.4;">🌐</div>
            <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:1rem;
                 font-weight:800;color:#334155;margin-bottom:6px;">
                Competitor Data Not Loaded
            </div>
            <div style="color:#1e293b;font-size:0.82rem;max-width:380px;margin:0 auto;
                 font-family:'Space Grotesk',sans-serif;">
                Click <strong style="color:#38bdf8;">Search Competitor Prices</strong>
                to fetch live market data and get AI positioning analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Warning if simulated
    if result.get("is_simulated") or result.get("search_error"):
        err = result.get("search_error", "")
        if "not set" in str(err):
            st.warning("⚠️ Tavily key not configured — showing simulated prices. Add key to `config/settings.py`")
        elif "not installed" in str(err):
            st.warning("⚠️ Run `pip install tavily-python` to enable live search")
        else:
            st.info(f"ℹ️ Simulated prices shown — {err or 'no live results found'}")

    pos       = result.get("positioning", "Unknown")
    gap       = result.get("price_gap_pct", 0.0)
    our_price = result.get("our_price", 0)
    avg_price = result.get("avg_competitor_price", 0)
    min_price = result.get("min_competitor_price", 0)
    max_price = result.get("max_competitor_price", 0)
    md_pct    = result.get("suggested_markdown", 0)
    conf      = result.get("confidence", 0)
    reasoning = result.get("reasoning", "")
    action    = result.get("action", "")

    pos_color = {"Overpriced": "#ef4444", "Competitive": "#10b981", "Underpriced": "#3b82f6"}.get(pos, "#64748b")
    pos_bg    = {"Overpriced": "rgba(239,68,68,0.06)", "Competitive": "rgba(16,185,129,0.06)", "Underpriced": "rgba(59,130,246,0.06)"}.get(pos, "rgba(100,116,139,0.06)")
    pos_icon  = {"Overpriced": "↑", "Competitive": "✓", "Underpriced": "↓"}.get(pos, "·")

    # Main positioning card
    st.markdown(f"""
    <div style="background:{pos_bg};border:1.5px solid {pos_color}44;
         border-radius:14px;padding:24px 28px;margin:14px 0;
         position:relative;overflow:hidden;animation:fadeSlideIn 0.5s ease;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
             background:linear-gradient(90deg,{pos_color},{pos_color}44);"></div>
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
            <div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                     color:{pos_color};text-transform:uppercase;letter-spacing:0.15em;margin-bottom:6px;">
                    ● MARKET POSITION
                </div>
                <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:1.8rem;
                     font-weight:900;color:#f8fafc;">
                    {pos_icon} {pos}
                </div>
                <div style="color:#64748b;font-size:0.8rem;margin-top:4px;
                     font-family:'Space Grotesk',sans-serif;">
                    We are <strong style="color:{pos_color};">{gap:+.1f}%</strong>
                    vs market avg of <strong style="color:#e2e8f0;">${avg_price:.2f}</strong>
                </div>
            </div>
            <div style="display:flex;gap:10px;flex-wrap:wrap;">
                <div style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;
                     padding:10px 16px;text-align:center;">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                         color:#64748b;text-transform:uppercase;letter-spacing:0.1em;">Action</div>
                    <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:0.95rem;
                         font-weight:800;color:{pos_color};margin-top:2px;">{action}</div>
                </div>
                <div style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;
                     padding:10px 16px;text-align:center;">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                         color:#64748b;text-transform:uppercase;letter-spacing:0.1em;">Suggested Cut</div>
                    <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:0.95rem;
                         font-weight:800;color:#38bdf8;margin-top:2px;">{md_pct:.1f}%</div>
                </div>
                <div style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;
                     padding:10px 16px;text-align:center;">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                         color:#64748b;text-transform:uppercase;letter-spacing:0.1em;">Confidence</div>
                    <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:0.95rem;
                         font-weight:800;color:#10b981;margin-top:2px;">{conf:.0f}%</div>
                </div>
            </div>
        </div>
        <div style="margin-top:16px;padding:12px 14px;
             background:rgba(255,255,255,0.02);border-radius:8px;
             border-left:3px solid #6366f1;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                 color:#64748b;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:5px;">
                Gemini Analysis
            </div>
            <div style="color:#94a3b8;font-size:0.82rem;line-height:1.7;
                 font-family:'Space Grotesk',sans-serif;">{reasoning}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Price comparison metrics
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#38bdf8;
         text-transform:uppercase; letter-spacing:0.15em; margin:1rem 0 0.5rem 0;">
        ▸ Price Comparison
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Our Price",         f"${our_price:.2f}")
    col2.metric("Market Average",    f"${avg_price:.2f}",  f"{gap:+.1f}% gap")
    col3.metric("Lowest in Market",  f"${min_price:.2f}")
    col4.metric("Highest in Market", f"${max_price:.2f}")

    # Competitor table
    competitor_results = result.get("competitor_results", [])
    if competitor_results:
        import pandas as pd
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#38bdf8;
             text-transform:uppercase; letter-spacing:0.15em; margin:1.2rem 0 0.5rem 0;">
            ▸ Competitor Breakdown
        </div>
        """, unsafe_allow_html=True)

        rows = []
        for r in competitor_results:
            price     = r["price"]
            diff      = round(price - our_price, 2)
            diff_pct  = round(diff / our_price * 100, 1) if our_price else 0
            diff_label= f"+${diff:.2f} ({diff_pct:+.1f}%)" if diff > 0 else f"-${abs(diff):.2f} ({diff_pct:.1f}%)"
            status    = "💚 Cheaper" if price < our_price * 0.95 else "🔴 Pricier" if price > our_price * 1.05 else "🟡 Similar"
            rows.append({
                "Competitor"  : r["source"],
                "Their Price" : f"${price:.2f}",
                "vs Ours"     : diff_label,
                "Status"      : status,
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No competitor results returned.")

    if show_backend:
        with st.expander("📤 Prompt sent to Gemini"):
            st.code(result.get("prompt_sent", ""), language="text")
        with st.expander("📥 Gemini Raw Response"):
            st.code(result.get("raw_response", ""), language="text")