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
    session_num=1,
    title="Foundation & Data Setup",
    time_range="0:10 - 0:30",
    duration="20 min",
    building="Database, schemas, warehouse, and 9 raw data tables",
)

render_technologies_used([
    {"name": "CREATE DATABASE / SCHEMA", "description": "Snowflake's logical containers. We create 3 schemas: RAW (source data), ANALYTICS (transformed views/tables), APPS (Streamlit artifacts).", "icon": "database"},
    {"name": "Virtual Warehouses", "description": "Named compute clusters that execute queries. Auto-suspend and auto-resume. We use MEDIUM for this lab.", "icon": "memory"},
    {"name": "CREATE TABLE + INSERT", "description": "DDL/DML for defining and populating structured tables with synthetic but realistic inventory data.", "icon": "table_chart"},
])


PROMPT_1_1 = """Create a Snowflake database called ROSS_INVENTORY_LAB with three schemas: RAW, ANALYTICS, and APPS. Create a warehouse called INVENTORY_LAB_WH (size MEDIUM, auto_suspend = 300, auto_resume = true). Add a comment on the database: "Store Inventory Optimization Lab - Ross Stores".

Then USE the database, RAW schema, and warehouse.

Now create the following dimension/reference tables in the RAW schema with realistic sample data:

1. PRODUCTS - 50 rows of off-price retail products. Columns: product_id (NUMBER), product_name (VARCHAR), category (one of: apparel_womens, apparel_mens, shoes, home_basics, accessories, kids), subcategory (VARCHAR), brand (VARCHAR - use realistic brands like Nike, Levi's, Calvin Klein, Michael Kors, Adidas, plus store brands), unit_cost (NUMBER, 2 decimals), retail_price (NUMBER, 2 decimals), pack_size (NUMBER - units per case, typically 6-24), reorder_point (NUMBER - min qty before reorder), lead_time_days (NUMBER - 3 to 21 depending on source), is_seasonal (BOOLEAN). Mix of branded and private-label products.

2. STORES - 25 rows representing Ross store locations. Columns: store_id (NUMBER), store_name (VARCHAR like "Ross #1234"), city (VARCHAR), state (VARCHAR - 2 letter), region (one of: West, Southwest, Southeast, Midwest, Northeast), district (VARCHAR), square_footage (NUMBER - 20000 to 35000), format (one of: standard, small, superstore), open_date (DATE). Use real US cities spread across regions.

3. EMPLOYEES - 40 rows. Columns: employee_id (NUMBER), first_name (VARCHAR), last_name (VARCHAR), role (one of: store_manager, asst_manager, inventory_lead, receiving_clerk, buyer, dc_planner, district_manager), store_id (NUMBER, NULL for buyers/dc_planners/district_managers), hire_date (DATE), is_active (BOOLEAN - all true).

4. CALENDAR - 730 rows covering 2024-02-01 through 2026-01-31 (two full fiscal years). The fiscal year starts on February 1st. Columns: cal_date (DATE), day_of_week (VARCHAR - Mon/Tue/etc), day_num (NUMBER 1-7), week_num (NUMBER - week of fiscal year, 1-52), month_num (NUMBER - fiscal month where Feb=1, Jan=12), month_name (VARCHAR), fiscal_quarter (NUMBER - Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan), fiscal_period (NUMBER 1-13, 4-5-4 calendar starting Feb 1), fiscal_year (NUMBER - the year the fiscal year started, e.g. 2024 for Feb 2024-Jan 2025), calendar_year (NUMBER), is_holiday (BOOLEAN), season (one of: spring, summer, fall, winter, holiday — where holiday = Nov-Dec-Jan to capture full holiday selling + post-holiday clearance), event_name (VARCHAR, NULL unless there's a key retail event like Back-to-School, Black Friday, Easter, Memorial Day, Labor Day, Christmas, New Year, Post-Holiday Clearance).

IMPORTANT: The fiscal year starts February 1st. Quarter 1 = Feb/Mar/Apr. Seasons align to fiscal calendar: spring (Feb-Apr), summer (May-Jul), fall/back-to-school (Aug-Oct), holiday (Nov-Jan). Make sure event_name includes Back-to-School (Aug), Black Friday (Nov), Christmas (Dec), and Post-Holiday Clearance (Jan).

Execute all SQL and confirm the tables are created."""

render_prompt("Prompt 1.1", "Create Foundation & Dimension Tables", PROMPT_1_1)

render_explanation("What this prompt does", """
Creates the entire environment and four dimension/reference tables:

1. **Database + 3 schemas**: RAW for source data, ANALYTICS for business logic, APPS for Streamlit objects
2. **Warehouse**: MEDIUM size, auto-suspends after 5 minutes
3. **PRODUCTS**: Product catalog with off-price retail attributes (pack sizes, reorder points, lead times)
4. **STORES**: Store network with geographic and format details
5. **EMPLOYEES**: Staff roster with roles relevant to inventory operations
6. **CALENDAR**: Date dimension with Ross's 4-5-4 fiscal calendar and retail events

**Why 3 schemas**: This mirrors how production data is organized — raw/staged data is separate from curated analytics, which is separate from application objects. This is a common data engineering pattern.
""")


PROMPT_1_2 = """Now create the fact tables in ROSS_INVENTORY_LAB.RAW. These contain the transactional and operational data:

1. DAILY_SALES - 5000 rows. Columns: sale_id (NUMBER), store_id (NUMBER), product_id (NUMBER), sale_date (DATE - spread across 2024-2025), units_sold (NUMBER 1-50), revenue (NUMBER with 2 decimals), discount_pct (NUMBER 0-70, off-price retail uses deep discounts), is_clearance (BOOLEAN). Ensure sales patterns reflect seasonality: higher volumes in Nov-Dec (holiday), Aug (back-to-school), and lower in Jan-Feb.

2. INVENTORY_SNAPSHOTS - 3000 rows. Columns: snapshot_id (NUMBER), store_id (NUMBER), product_id (NUMBER), snapshot_date (DATE - weekly snapshots), on_hand_qty (NUMBER 0-500), on_order_qty (NUMBER 0-200), in_transit_qty (NUMBER 0-100), backroom_qty (NUMBER), floor_qty (NUMBER - backroom + floor = on_hand). IMPORTANT: Include at least 30 rows with on_hand_qty = 0 (active stockouts) and at least 50 rows with on_hand_qty < 10 (critically low), spread across multiple stores and categories. These will trigger EMERGENCY and URGENT replenishment signals in Session 4.

3. PURCHASE_ORDERS - 500 rows. Columns: po_id (NUMBER), store_id (NUMBER), product_id (NUMBER), order_date (DATE), expected_delivery_date (DATE - order_date + lead_time_days from PRODUCTS), actual_delivery_date (DATE - sometimes NULL for pending, sometimes 1-5 days late), qty_ordered (NUMBER), qty_received (NUMBER - sometimes less than ordered), status (one of: pending, in_transit, delivered, partial, cancelled), supplier (VARCHAR).

4. STOCKOUT_EVENTS - 200 rows. Columns: event_id (NUMBER), store_id (NUMBER), product_id (NUMBER), stockout_start_date (DATE), stockout_end_date (DATE - 1 to 14 days later, NULL for ongoing stockouts), days_out_of_stock (NUMBER), estimated_lost_units (NUMBER), estimated_lost_revenue (NUMBER with 2 decimals), root_cause (one of: demand_spike, late_delivery, forecast_error, receiving_delay, allocation_error). IMPORTANT: Include at least 20 events with stockout_end_date = NULL (still active/ongoing) to represent current emergencies. Concentrate some stockouts on the same store/product combos to show repeat offenders.

5. REPLENISHMENT_POLICIES - 50 rows of text-based policy documents. Columns: policy_id (NUMBER), category (VARCHAR matching product categories), policy_title (VARCHAR), policy_text (VARCHAR - 200-500 word descriptions of replenishment rules, seasonal adjustments, min/max thresholds, emergency reorder procedures, clearance markdown timing). Write realistic inventory management policy content. Include policies for: standard reorder procedures, seasonal buildup rules, clearance/markdown timing, emergency out-of-stock response, new store opening inventory, holiday season preparation, pack-and-hold strategies.

Execute all SQL."""

render_prompt("Prompt 1.2", "Create Fact Tables", PROMPT_1_2)

render_explanation("What this prompt does", """
Creates five fact tables that represent operational reality:

- **DAILY_SALES**: Transaction-level sales with seasonal patterns built in
- **INVENTORY_SNAPSHOTS**: Point-in-time inventory positions (weekly cadence)
- **PURCHASE_ORDERS**: The supply side — what's been ordered, what arrived, what's late
- **STOCKOUT_EVENTS**: When shelves went empty and why — key for analysis
- **REPLENISHMENT_POLICIES**: Unstructured text describing how inventory should be managed — this becomes the knowledge base for Cortex Search later

**Key design choices**:
- Sales have seasonal weighting (holiday/BTS peaks aligned to Feb 1 fiscal year)
- Inventory snapshots include both backroom and floor splits
- **Stockout events and inventory levels are designed to trigger EMERGENCY and URGENT conditions** — ensure several products have on_hand_qty = 0 or very low (< 5), and some with days_of_supply < lead_time_days
- Policies are natural language text (not structured rules) — designed for AI retrieval
""")


PROMPT_1_3 = """Show me the row counts for all 9 tables in ROSS_INVENTORY_LAB.RAW, and show a sample of 3 rows from DAILY_SALES, INVENTORY_SNAPSHOTS, and REPLENISHMENT_POLICIES so I can verify the data looks right. Also show the date range covered in DAILY_SALES and CALENDAR."""

render_prompt("Prompt 1.3", "Verify the Data", PROMPT_1_3)

render_explanation("What this prompt does", """
Verification step to confirm all tables were created correctly:

- **Row counts**: Ensures each table has approximately the expected number of rows
- **Sample rows**: Spot-check that the data is realistic and correctly typed
- **Date ranges**: Confirms temporal coverage spans the expected 2024-2025 period

This is a habit worth building — always verify after bulk data creation.
""")


render_key_concepts([
    {"term": "Star Schema", "definition": "A data modeling pattern where a central fact table (transactions, events) connects to dimension tables (products, stores, calendar) via foreign keys. Our design has DAILY_SALES and INVENTORY_SNAPSHOTS as facts, with PRODUCTS, STORES, CALENDAR as shared dimensions."},
    {"term": "Schema Separation (RAW / ANALYTICS / APPS)", "definition": "Organizing data by transformation stage. RAW holds source-of-truth data. ANALYTICS holds curated views and dynamic tables with business logic applied. APPS holds Streamlit and agent artifacts."},
    {"term": "4-5-4 Fiscal Calendar (Feb 1 start)", "definition": "A retail accounting calendar starting February 1st that divides the year into 13 four-week periods grouped as 4-5-4 within each quarter. Q1 = Feb-Apr, Q2 = May-Jul, Q3 = Aug-Oct, Q4 = Nov-Jan. Ross uses this instead of calendar months for consistent week-over-week comparisons."},
])

render_domain_glossary([
    {"term": "Reorder Point (ROP)", "definition": "The inventory level at which a new purchase order should be triggered. Typically calculated as (average daily demand x lead time) + safety stock. When on-hand drops below ROP, it's time to reorder."},
    {"term": "Days of Supply (DOS)", "definition": "How many days current inventory will last at the current sales rate. Calculated as on_hand_qty / avg_daily_units_sold. A DOS of 14 means you have two weeks of stock."},
    {"term": "Pack-and-Hold", "definition": "An off-price retail strategy where excess inventory is purchased at deep discount and held in distribution centers until the right selling season. Common at Ross for seasonal merchandise."},
    {"term": "Stockout", "definition": "When a product has zero available units on the sales floor. Results in lost sales and customer dissatisfaction. Off-price retailers accept higher stockout rates than traditional retail due to the treasure-hunt shopping model."},
])

render_what_you_built([
    "ROSS_INVENTORY_LAB database with RAW, ANALYTICS, APPS schemas",
    "INVENTORY_LAB_WH warehouse (MEDIUM size)",
    "4 dimension tables: PRODUCTS (50), STORES (25), EMPLOYEES (40), CALENDAR (730)",
    "5 fact tables: DAILY_SALES (5000), INVENTORY_SNAPSHOTS (3000), PURCHASE_ORDERS (500), STOCKOUT_EVENTS (200), REPLENISHMENT_POLICIES (50)",
])
