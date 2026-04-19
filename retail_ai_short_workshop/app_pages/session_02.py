import streamlit as st
from components import (
    render_session_header,
    render_prompt,
    render_explanation,
    render_technologies_used,
    render_key_concepts,
    render_domain_glossary,
    render_what_you_built,
)

render_session_header(
    session_num=2,
    title="Preparing Data for AI & Feature Engineering",
    time_range="0:15 - 0:30",
    duration="15 min",
    building="12 operational data tables covering structured, time-series, unstructured, and geospatial data",
)

render_technologies_used([
    {"name": "Structured Data Tables", "description": "Traditional relational tables with typed columns, foreign keys, and constraints. These are the backbone of operational analytics.", "icon": "table_chart"},
    {"name": "Time-Series Data", "description": "Foot traffic counts, daily sales metrics, and clickstream events with timestamps. Snowflake handles time-series natively with TIMESTAMP types and window functions.", "icon": "timeline"},
    {"name": "Semi-Structured Text", "description": "Long-form text stored in VARCHAR columns. This unstructured data will be processed by Cortex LLM functions and Cortex Search in later sessions.", "icon": "article"},
])


PROMPT_2_1 = """In RETAIL_AI_DEMO.RETAIL_OPS, create and populate these structured operational tables with realistic synthetic data:

1. SALES_TRANSACTIONS - 200 rows of point-of-sale and e-commerce transactions. Columns: transaction_id, store_id (FK to STORES), product_id (FK to PRODUCTS), customer_id, transaction_date (between 2025-01-01 and 2026-04-06, with heavier volume in Nov-Dec holiday season and August back-to-school), quantity, unit_price, discount_pct, total_amount, payment_method (credit_card, debit, cash, mobile_pay, gift_card), channel (in_store, online, bopis), loyalty_member BOOLEAN. Make sure discount_pct is higher during Nov-Dec (holiday promotions) and for outlet store transactions.

2. PURCHASE_ORDERS - 300 rows of supplier purchase orders. Columns: po_id, supplier_id (FK to SUPPLIERS), product_id (FK to PRODUCTS), order_date, expected_delivery_date, actual_delivery_date, quantity_ordered, quantity_received, unit_cost, total_cost, status (ordered, shipped, received, partial, cancelled), destination_store_id. Include some orders where quantity_received < quantity_ordered (partial shipments) and some where actual_delivery_date > expected_delivery_date (late deliveries).

3. INVENTORY_LEVELS - 150 rows of current inventory positions. Columns: snapshot_id, store_id (FK), product_id (FK), snapshot_date, quantity_on_hand, quantity_reserved, quantity_on_order, reorder_point, days_of_supply, status (in_stock, low_stock, out_of_stock, overstock). Include realistic patterns: seasonal items (sandals, outerwear) should show overstock in off-seasons and low stock in peak seasons.

Execute all SQL to create and populate these tables."""

render_prompt("Prompt 2.1", "Structured Operational Data", PROMPT_2_1)

render_explanation("What this prompt does", """
This creates three core **fact tables** that represent the operational heart of retail:

- **SALES_TRANSACTIONS**: The central fact table. Each row is a sale at a specific store or online. The `store_id` and `product_id` columns create relationships to our Session 1 dimension tables.

- **PURCHASE_ORDERS**: The supply chain backbone. Tracks orders placed with suppliers through delivery.

- **INVENTORY_LEVELS**: Point-in-time inventory snapshots per store per product. The `days_of_supply` metric is critical for retail operations.

**Data modeling pattern**: This follows a **star schema** design — SALES_TRANSACTIONS is the central fact table, with PRODUCTS, STORES, and SUPPLIERS as dimension tables.
""")


PROMPT_2_2 = """In RETAIL_AI_DEMO.RETAIL_OPS, create and populate these time-series tables:

1. STORE_FOOT_TRAFFIC - 500 rows of in-store traffic data. Columns: traffic_id, store_id (FK), timestamp (hourly intervals over the past 30 days), visitor_count, conversion_rate_pct, avg_basket_size, weather_condition (sunny, cloudy, rain, snow), is_weekend BOOLEAN, is_holiday BOOLEAN. Make weekend and holiday traffic 30-40% higher than weekday traffic. Flagship stores should have the highest visitor counts.

2. DAILY_SALES_METRICS - 400 rows of aggregated daily store performance. Columns: metric_id, store_id (FK), date, total_revenue, transaction_count, avg_transaction_value, units_sold, returns_count, returns_value, online_orders_fulfilled. Include realistic patterns: weekends higher than weekdays, outlet stores have more transactions but lower avg_transaction_value.

3. WEBSITE_CLICKSTREAM - 300 rows of e-commerce browsing behavior. Columns: click_id, session_id, timestamp, page_type (home, category, product, cart, checkout, search), product_id (FK, nullable - only populated for product pages), device_type (desktop, mobile, tablet), referral_source (direct, search, social, email), time_on_page_seconds. Include realistic funnel drop-off: many home/category views, fewer product views, even fewer cart/checkout.

4. INVENTORY_SNAPSHOTS - 200 rows of inventory change tracking over time. Columns: snapshot_id, product_id (FK), store_id (FK), timestamp, quantity_available, quantity_sold_today, projected_stockout_date, replenishment_status (adequate, ordered, urgent, critical). Some rows should have projected_stockout_date within the next 7 days to create urgency signals.

Execute all SQL."""

render_prompt("Prompt 2.2", "Time-Series Data", PROMPT_2_2)

render_explanation("What this prompt does", """
This creates four **time-series tables** representing operational metrics and customer behavior data:

- **STORE_FOOT_TRAFFIC**: In-store traffic from people counters. Visitor count combined with conversion rate tells you how effectively the store converts browsers into buyers.

- **DAILY_SALES_METRICS**: Aggregated daily KPIs per store. This is the data that store managers review every morning.

- **WEBSITE_CLICKSTREAM**: E-commerce browsing behavior. The `page_type` column represents the conversion funnel: home -> category -> product -> cart -> checkout.

- **INVENTORY_SNAPSHOTS**: Time-stamped inventory positions. The `projected_stockout_date` is calculated from current velocity and on-hand quantity.
""")


PROMPT_2_3 = """In RETAIL_AI_DEMO.RETAIL_OPS, create and populate these unstructured/text data tables:

1. CUSTOMER_REVIEWS - 30 rows of product reviews. Columns: review_id, product_id (FK), customer_id, review_date, rating (1-5), review_text (generate detailed multi-paragraph reviews, at least 100 words each, about fit, quality, comfort, style, value, durability - include both positive and negative reviews across the rating spectrum), verified_purchase BOOLEAN, helpful_votes. Include reviews that mention sizing issues, fabric quality, comparison to competitors, and return experiences.

2. SUPPORT_TICKETS - 25 rows of customer service interactions. Columns: ticket_id, customer_id, created_date, channel (email, chat, phone, social), category (return_request, product_defect, shipping_issue, size_exchange, billing, general_inquiry), description_text (detailed paragraph describing the customer's issue - sizing problems, damaged items, late shipments, wrong items sent, loyalty point disputes), priority (low, medium, high, urgent), status (open, in_progress, resolved, escalated), resolution_text.

3. MARKETING_CAMPAIGNS - 40 rows of campaign records. Columns: campaign_id, campaign_name, start_date, end_date, channel (email, social, display, sms, in_store), target_segment, campaign_brief_text (detailed paragraph about campaign goals, messaging strategy, target audience, creative direction, and expected ROI - at least 100 words each), budget_usd, actual_spend_usd, impressions, conversions.

4. SUPPLIER_COMMUNICATIONS - 35 rows of email correspondence with suppliers. Columns: comm_id, supplier_id (FK), from_party, to_party, subject, message_body (realistic email text about shipment delays, fabric quality issues, price negotiations, seasonal planning, MOQ discussions, lead time changes - some in English, some in Spanish for international suppliers in Latin America), sent_date, category (logistics, quality, pricing, planning, urgent_alert), language (en, es).

5. PRODUCT_RETURN_NOTES - 20 rows of detailed return inspection records. Columns: note_id, transaction_id, return_date, return_reason_text (detailed narrative about why the product was returned - sizing ran small/large, color didn't match website, fabric pilling after one wash, seam came apart, changed mind, bought wrong size), product_condition (new_with_tags, worn, defective, damaged), recommended_action, disposition (restock, markdown, donate, destroy).

Make sure all text fields contain substantial, realistic content (at least 100 words for review_text, campaign_brief_text, and description fields). Execute all SQL."""

render_prompt("Prompt 2.3", "Unstructured Text Data for AI", PROMPT_2_3)

render_explanation("What this prompt does", """
This creates five tables of **unstructured text data** — the raw material for Cortex LLM functions, Cortex Search, and RAG pipelines:

- **CUSTOMER_REVIEWS**: Product review text for sentiment analysis, entity extraction, and summarization.
- **SUPPORT_TICKETS**: Customer service interactions for classification and extraction.
- **MARKETING_CAMPAIGNS**: Campaign briefs with performance data.
- **SUPPLIER_COMMUNICATIONS**: Includes **bilingual content** (English/Spanish) for translation demos.
- **PRODUCT_RETURN_NOTES**: Return inspection narratives for root-cause analysis.

**Why text data matters for AI**: Traditional BI only works with structured data. Modern AI can extract insights from text, classify documents, answer questions from document collections, and detect sentiment — all capabilities we'll build in Sessions 3-6.
""")


PROMPT_2_4 = """Run a query in RETAIL_AI_DEMO.RETAIL_OPS that shows every table name and its row count, ordered by row count descending. Use INFORMATION_SCHEMA.TABLES. Format it nicely."""

render_prompt("Prompt 2.4", "Verify All Data Tables", PROMPT_2_4)

render_explanation("What this prompt does", """
A quick verification query using `INFORMATION_SCHEMA.TABLES`. You should see approximately **2,200+ total rows** across 15 tables (3 from Session 1 + 12 from this session).
""")


render_key_concepts([
    {"term": "Star Schema", "definition": "A data modeling pattern with a central fact table (SALES_TRANSACTIONS) surrounded by dimension tables (PRODUCTS, STORES, SUPPLIERS). Fact tables contain measures and foreign keys; dimension tables contain descriptive attributes."},
    {"term": "INFORMATION_SCHEMA.TABLES", "definition": "A standard SQL view available in every Snowflake database that provides metadata about all objects — row counts, creation dates, byte sizes, and more."},
])

render_domain_glossary([
    {"term": "BOPIS (Buy Online, Pick Up In Store)", "definition": "An omnichannel fulfillment method where customers purchase online and collect at a physical store. BOPIS drives foot traffic and reduces shipping costs."},
    {"term": "Days of Supply", "definition": "How many days the current inventory will last at the current rate of sale. Calculated as quantity_on_hand / avg_daily_units_sold. Below the reorder point triggers a replenishment order."},
])

render_what_you_built([
    "SALES_TRANSACTIONS - 200 POS/e-commerce transactions with seasonal patterns",
    "PURCHASE_ORDERS - 300 supplier purchase orders with delivery tracking",
    "INVENTORY_LEVELS - 150 current inventory positions by store and product",
    "STORE_FOOT_TRAFFIC - 500 hourly in-store traffic measurements",
    "DAILY_SALES_METRICS - 400 aggregated daily store performance metrics",
    "WEBSITE_CLICKSTREAM - 300 e-commerce browsing events with funnel data",
    "INVENTORY_SNAPSHOTS - 200 time-stamped inventory change records",
    "CUSTOMER_REVIEWS - 30 detailed product reviews with ratings",
    "SUPPORT_TICKETS - 25 customer service interactions",
    "MARKETING_CAMPAIGNS - 40 campaign records with briefs and performance",
    "SUPPLIER_COMMUNICATIONS - 35 bilingual supplier email correspondence",
    "PRODUCT_RETURN_NOTES - 20 detailed return inspection narratives",
])
