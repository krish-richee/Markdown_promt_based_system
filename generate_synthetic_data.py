import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# ── Based on your real data patterns ──────────────────────────────────────

CATEGORIES = [
    "Climbing", "Footwear", "Gift Cards", "Hiking & Camping",
    "Kids", "Mens", "Packs", "Technology", "Travel", "Womens"
]

PAYMENT_METHODS = [
    "braintree", "braintree_paypal", "payment_services_paypal_google_pay",
    "payment_services_paypal_apple_pay", "payment_services_paypal_smart_buttons"
]

RISK_LEVELS    = ["HIGH", "MEDIUM", "LOW"]
ABC_CLASSES    = ["A", "B", "C"]
EVENT_TYPES    = ["session_start", "view_item", "add_to_cart",
                  "begin_checkout", "purchase", "remove_from_cart",
                  "view_item_list", "select_item"]
PLATFORMS      = ["WEB", "IOS", "ANDROID"]
STATES         = ["Maharashtra", "Gujarat", "Karnataka", "Delhi",
                  "Tamil Nadu", "Rajasthan", "West Bengal"]

# ── 1. Generate Products ───────────────────────────────────────────────────
def generate_products(n=10000):
    print(f"Generating {n} products...")
    products = []
    for i in range(n):
        category    = random.choice(CATEGORIES)
        price       = round(random.uniform(10, 500), 2)
        discount    = random.uniform(0, 0.5)
        special     = round(price * (1 - discount), 2)
        quantity    = random.randint(0, 1000)
        products.append({
            "product_id":       f"PROD_{i+1:05d}",
            "product_name":     f"{category} Product {i+1}",
            "main_category":    category,
            "price":            price,
            "special_price":    special,
            "quantity":         quantity,
            "discount_pct":     round(discount * 100, 1),
        })
    return pd.DataFrame(products)

# ── 2. Generate Orders ─────────────────────────────────────────────────────
def generate_orders(n=80000):
    print(f"Generating {n} orders...")
    start_date = datetime(2023, 1, 1)
    end_date   = datetime(2026, 3, 31)
    date_range = (end_date - start_date).days

    orders = []
    for i in range(n):
        order_date      = start_date + timedelta(days=random.randint(0, date_range))
        grand_total     = round(random.uniform(20, 800), 2)
        discount_amount = round(grand_total * random.uniform(0, 0.4), 2)
        qty             = random.randint(1, 10)
        is_guest        = random.choice([0, 1])
        state           = random.choice(["complete", "complete", "complete",
                                         "pending", "canceled"])
        orders.append({
            "order_id":           f"ORD_{i+1:06d}",
            "order_date":          order_date,
            "state":               state,
            "grand_total":         grand_total,
            "discount_amount":     discount_amount,
            "total_qty_ordered":   qty,
            "payment_method":      random.choice(PAYMENT_METHODS),
            "customer_is_guest":   is_guest,
        })
    return pd.DataFrame(orders)

# ── 3. Generate Order Items ────────────────────────────────────────────────
def generate_order_items(orders_df, products_df, avg_items=2):
    print("Generating order items...")
    items = []
    completed = orders_df[orders_df["state"] == "complete"]

    for _, order in completed.iterrows():
        n_items = random.randint(1, avg_items + 2)
        prods   = products_df.sample(n_items)
        for _, prod in prods.iterrows():
            qty        = random.randint(1, 5)
            price      = prod["price"]
            discount   = round(price * random.uniform(0, 0.3), 2)
            row_total  = round((price - discount) * qty, 2)
            items.append({
                "order_id":             order["order_id"],
                "product_id":           prod["product_id"],
                "item_name":            prod["product_name"],
                "product_main_category":prod["main_category"],
                "qty_ordered":          qty,
                "price":                price,
                "discount_amount":      discount,
                "row_total":            row_total,
                "line_total_after_discount": row_total,
                "order_state":          order["state"],
                "order_date":           order["order_date"],
            })
    return pd.DataFrame(items)

# ── 4. Generate Customers ──────────────────────────────────────────────────
def generate_customers(n=30000):
    print(f"Generating {n} customers...")
    start_date = datetime(2022, 1, 1)
    customers  = []
    for i in range(n):
        created = start_date + timedelta(days=random.randint(0, 1500))
        customers.append({
            "customer_id":          f"CUST_{i+1:06d}",
            "customer_created_date": created,
            "customer_is_guest":     random.choice([0, 1]),
        })
    return pd.DataFrame(customers)

# ── 5. Generate BQ Events ─────────────────────────────────────────────────
def generate_bq_events(products_df, n=250000):
    print(f"Generating {n} events...")
    start_date = datetime(2024, 1, 1)
    end_date   = datetime(2026, 3, 31)
    date_range = (end_date - start_date).days

    events = []
    for i in range(n):
        event_date = start_date + timedelta(days=random.randint(0, date_range))
        event_name = random.choices(
            EVENT_TYPES,
            weights=[20, 30, 15, 8, 5, 5, 10, 7]
        )[0]
        prod = products_df.sample(1).iloc[0]
        events.append({
            "event_date":       event_date,
            "event_name":       event_name,
            "ga_session_id":    f"SESSION_{random.randint(1, 50000)}",
            "user_pseudo_id":   f"USER_{random.randint(1, 30000)}",
            "item_name":        prod["product_name"] if event_name not in ["session_start"] else None,
            "platform":         random.choice(PLATFORMS),
            "event_value_in_usd": round(random.uniform(0, 500), 2) if event_name == "purchase" else 0,
        })
    return pd.DataFrame(events)

# ── 6. Generate Invoices ───────────────────────────────────────────────────
def generate_invoices(orders_df):
    print("Generating invoices...")
    completed = orders_df[orders_df["state"] == "complete"].copy()
    invoices  = []
    for i, (_, order) in enumerate(completed.iterrows()):
        invoices.append({
            "invoice_id":   f"INV_{i+1:06d}",
            "order_id":     order["order_id"],
            "invoice_date": order["order_date"] + timedelta(days=random.randint(0, 2)),
            "grand_total":  order["grand_total"],
        })
    return pd.DataFrame(invoices)

# ── MAIN ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Generating synthetic retail data based on real patterns...\n")

    products   = generate_products(10000)
    orders     = generate_orders(80000)
    order_items= generate_order_items(orders, products)
    customers  = generate_customers(30000)
    bq_events  = generate_bq_events(products, 250000)
    invoices   = generate_invoices(orders)

    print("\n📊 Dataset Summary:")
    print(f"  Products:    {len(products):,}")
    print(f"  Orders:      {len(orders):,}")
    print(f"  Order Items: {len(order_items):,}")
    print(f"  Customers:   {len(customers):,}")
    print(f"  BQ Events:   {len(bq_events):,}")
    print(f"  Invoices:    {len(invoices):,}")

    print("\n💾 Saving to Excel...")
    with pd.ExcelWriter("data/synthetic_retail_data.xlsx", engine="openpyxl") as writer:
        products.to_excel(writer,    sheet_name="product_catalogue", index=False)
        orders.to_excel(writer,      sheet_name="orders",            index=False)
        order_items.to_excel(writer, sheet_name="order_items",       index=False)
        customers.to_excel(writer,   sheet_name="customers",         index=False)
        bq_events.to_excel(writer,   sheet_name="bq_events",         index=False)
        invoices.to_excel(writer,    sheet_name="invoices",          index=False)

    print("✅ Done! File saved to data/synthetic_retail_data.xlsx")
    print("\nNow update DATA_PATH in utils/data_loader.py to use this file.")