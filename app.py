import streamlit as st

st.set_page_config(
    page_title="RetailAI — SKU Markdown Simulator",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from pages.sku_simulator import render
render()