import pandas as pd
import numpy as np
import streamlit as st
from config.settings import (
    DATA_PATH, HIGH_RISK_DAYS, MEDIUM_RISK_DAYS,
    DEAD_INVENTORY_DAYS, ABC_A_THRESHOLD, ABC_B_THRESHOLD
)

@st.cache_data
def load_all_data():
    xl          = pd.ExcelFile(DATA_PATH)
    products    = xl.parse("product_catalogue")
    orders      = xl.parse("orders")
    order_items = xl.parse("order_items")
    return products, orders, order_items

@st.cache_data
def compute_sku_metrics():
    products, orders, order_items = load_all_data()

    # ── Only completed orders ─────────────────────────────────────────────
    completed = order_items[order_items["order_state"] == "complete"].copy()
    completed["order_date"] = pd.to_datetime(completed["order_date"])

    # ── Sales metrics per SKU ─────────────────────────────────────────────
    sales = completed.groupby("product_id").agg(
        total_qty_sold  = ("qty_ordered",  "sum"),
        total_revenue   = ("row_total",    "sum"),
        order_count     = ("order_id",     "nunique"),
        first_sale_date = ("order_date",   "min"),
        last_sale_date  = ("order_date",   "max"),
    ).reset_index()

    # ── Sales velocity (units/day) ────────────────────────────────────────
    ref_date = pd.Timestamp("2026-03-31")
    sales["days_active"]    = (ref_date - sales["first_sale_date"]).dt.days.clip(lower=1)
    sales["sales_velocity"] = sales["total_qty_sold"] / sales["days_active"]

    # ── Merge with product catalogue ──────────────────────────────────────
    df = products.merge(sales, on="product_id", how="left")
    df["total_qty_sold"]  = df["total_qty_sold"].fillna(0)
    df["total_revenue"]   = df["total_revenue"].fillna(0)
    df["order_count"]     = df["order_count"].fillna(0)
    df["sales_velocity"]  = df["sales_velocity"].fillna(0)

    # ── Days of stock remaining ───────────────────────────────────────────
    raw_days            = np.where(df["sales_velocity"] > 0,
                                   df["quantity"] / df["sales_velocity"], 9999)
    df["days_of_stock"] = np.clip(raw_days, 0, 9999)

    # ── Clearance risk ────────────────────────────────────────────────────
    df["clearance_risk"] = np.where(
        df["days_of_stock"] >= HIGH_RISK_DAYS,   "HIGH",
        np.where(df["days_of_stock"] >= MEDIUM_RISK_DAYS, "MEDIUM", "LOW")
    )

    # ── Dead inventory flag ───────────────────────────────────────────────
    df["is_dead_inventory"] = df["days_of_stock"] >= DEAD_INVENTORY_DAYS

    # ── Sell-through rate ─────────────────────────────────────────────────
    raw_str = np.where(
        (df["total_qty_sold"] + df["quantity"]) > 0,
        df["total_qty_sold"] / (df["total_qty_sold"] + df["quantity"]) * 100, 0
    )
    df["sell_through_rate"] = np.clip(raw_str, 0, 100)

    # ── ABC Classification ────────────────────────────────────────────────
    df_sorted = df.sort_values("total_revenue", ascending=False).copy()
    total_rev = df_sorted["total_revenue"].sum()
    df_sorted["cum_revenue_pct"] = df_sorted["total_revenue"].cumsum() / (total_rev if total_rev > 0 else 1)
    df_sorted["abc_class"] = np.where(
        df_sorted["cum_revenue_pct"] <= ABC_A_THRESHOLD, "A",
        np.where(df_sorted["cum_revenue_pct"] <= ABC_B_THRESHOLD, "B", "C")
    )
    df = df.merge(
        df_sorted[["product_id", "abc_class", "cum_revenue_pct"]],
        on="product_id", how="left"
    )

    return df

def get_sku(df: pd.DataFrame, product_id: str) -> pd.Series:
    """Return a single SKU row as a Series."""
    row = df[df["product_id"] == product_id]
    if row.empty:
        raise ValueError(f"SKU {product_id} not found")
    return row.iloc[0]