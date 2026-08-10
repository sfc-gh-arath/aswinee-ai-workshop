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
    session_num=3,
    title="Analytics-Ready Views",
    time_range="0:50 - 1:15",
    duration="25 min",
    building="Three curated views with business logic for inventory health, seasonal sales, and store KPIs",
)

render_technologies_used([
    {"name": "CREATE VIEW", "description": "A named SQL query stored in Snowflake. Views don't store data — they compute results on-the-fly when queried. Ideal for applying business logic without duplicating data.", "icon": "view_quilt"},
    {"name": "Window Functions", "description": "SQL functions that compute values across a set of rows related to the current row (LAG, LEAD, AVG OVER, ROW_NUMBER). Essential for time-series calculations like rolling averages and trends.", "icon": "window"},
    {"name": "CASE Expressions", "description": "Conditional logic in SQL. Used to classify inventory health status, flag risk levels, and apply business rules inline.", "icon": "rule"},
])


PROMPT_3_1 = """Create a view called ROSS_INVENTORY_LAB.ANALYTICS.INVENTORY_HEALTH that joins INVENTORY_SNAPSHOTS with PRODUCTS and STORES, and calculates these business metrics for each row:

- days_of_supply: on_hand_qty / NULLIF(avg_daily_units_sold, 0) where avg_daily_units_sold comes from DAILY_SALES averaged over the last 30 days relative to the snapshot_date
- stockout_risk: a CASE expression that classifies as 'CRITICAL' (on_hand_qty = 0), 'HIGH' (days_of_supply < 3), 'MEDIUM' (days_of_supply < 7), 'LOW' (days_of_supply < 14), 'HEALTHY' (>= 14)
- overstock_flag: TRUE when days_of_supply > 60
- reorder_needed: TRUE when on_hand_qty <= reorder_point (from PRODUCTS)
- weeks_of_cover: days_of_supply / 7

Include these columns from dimensions: product_name, category, brand, store_name, city, region, square_footage.

Make sure to add a COMMENT on the view explaining its purpose.

Execute and then SELECT * LIMIT 10 to verify."""

render_prompt("Prompt 3.1", "Inventory Health View", PROMPT_3_1)

render_explanation("What this prompt does", """
Creates the core **inventory health** view that answers: "How healthy is our inventory position right now?"

**Key calculations**:
- **Days of Supply (DOS)**: The universal inventory metric — how long will current stock last?
- **Stockout Risk Classification**: Turns a continuous metric into actionable categories
- **Overstock Flag**: Identifies excess inventory tying up capital
- **Reorder Needed**: Compares current stock to the product's reorder point

**Design decisions**:
- Uses a 30-day trailing average for demand (smooths out daily noise)
- NULLIF prevents division-by-zero for products with no recent sales
- Risk thresholds (3/7/14 days) are typical for off-price retail
- View doesn't store data — always reflects the latest snapshot
""")


PROMPT_3_2 = """Create a view called ROSS_INVENTORY_LAB.ANALYTICS.SALES_WITH_SEASONALITY that joins DAILY_SALES with PRODUCTS, STORES, and CALENDAR, including these calculated fields:

- All base columns from DAILY_SALES
- product_name, category, brand from PRODUCTS
- store_name, region from STORES
- day_of_week, month_name, fiscal_quarter, season, event_name, is_holiday, fiscal_period, fiscal_year from CALENDAR
- revenue_per_unit: revenue / NULLIF(units_sold, 0)
- is_weekend: TRUE when day_num IN (6, 7)
- fiscal_quarter: from CALENDAR (Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan)
- rolling_7day_avg_units: AVG(units_sold) OVER (PARTITION BY store_id, product_id ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
- rolling_7day_avg_revenue: same pattern for revenue
- wow_units_change_pct: percentage change in units_sold vs same day last week using LAG(..., 7)
- yoy_comparison_flag: TRUE when the same (store_id, product_id, day_of_week, week_num) exists in the prior fiscal year (fiscal year starts Feb 1)

Note: The fiscal year starts February 1st. Fiscal quarters are Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan. Holiday season spans Nov-Jan (fiscal Q4).

Add a COMMENT on the view. Execute and verify with a sample query showing sales during the holiday season (fiscal Q4)."""

render_prompt("Prompt 3.2", "Sales with Seasonality View", PROMPT_3_2)

render_explanation("What this prompt does", """
Creates a **denormalized sales view** enriched with time intelligence:

**Why this view exists**: Analysts frequently need to analyze sales in the context of seasonality, holidays, and trends. Instead of writing these JOINs and window functions repeatedly, we codify them once.

**Window functions**:
- **Rolling 7-day average**: Smooths daily noise to show true trends
- **Week-over-week change**: Flags acceleration or deceleration in demand
- Both are PARTITION BY (store, product) so each combination gets its own calculation

**Calendar enrichment**: Attaching season, events, and fiscal period allows filtering like "show me all Back-to-School sales" or "compare fiscal period 8 vs 9." The fiscal year starts Feb 1, so Q1 is Feb-Apr and holiday season (Q4) spans Nov-Jan.
""")


PROMPT_3_3 = """Create a view called ROSS_INVENTORY_LAB.ANALYTICS.STORE_PERFORMANCE_SUMMARY that aggregates store-level KPIs. For each store, calculate:

- total_revenue: SUM of all revenue from DAILY_SALES
- total_units_sold: SUM of units_sold
- avg_transaction_revenue: AVG revenue per sale row
- total_stockout_events: COUNT from STOCKOUT_EVENTS
- total_lost_revenue: SUM of estimated_lost_revenue from STOCKOUT_EVENTS
- avg_days_of_supply: AVG on_hand_qty / NULLIF(avg daily demand, 0) across most recent inventory snapshot
- fill_rate_pct: 1 - (total_stockout_days / total_possible_days) * 100 — approximate using stockout_events
- inventory_turnover: total_units_sold / AVG(on_hand_qty) — annualized
- revenue_per_sqft: total_revenue / square_footage
- top_stockout_category: the category with the most stockout events at that store (use a subquery or lateral)

Include store dimensions: store_name, city, state, region, district, square_footage, format.

GROUP BY store. Add a COMMENT. Execute and show all 25 stores ranked by fill_rate_pct ascending (worst first)."""

render_prompt("Prompt 3.3", "Store Performance Summary", PROMPT_3_3)

render_explanation("What this prompt does", """
Creates a **store scorecard** view — one row per store with all key performance indicators:

**Revenue metrics**: How much is each store selling?
**Inventory efficiency**: Turnover rate, days of supply
**Service level**: Fill rate, stockout frequency, lost revenue
**Space productivity**: Revenue per square foot

**Why rank by worst fill rate**: This immediately surfaces the stores that need attention. An analyst opens this view and sees: "Store #1234 in Houston has a 87% fill rate with $45K in lost revenue — top stockout category is shoes."

**Design pattern**: This is a classic "executive summary" view that rolls up detail into decision-ready KPIs. It sits in ANALYTICS schema because it applies business logic (fill rate formula, turnover calculation) to raw facts.
""")


render_key_concepts([
    {"term": "Views vs Tables", "definition": "Views store a SQL query, not data. Every time you SELECT from a view, it re-executes the underlying query against current data. Zero storage cost, always fresh, but compute cost on each read. Use views when the logic is simple enough to run on-demand."},
    {"term": "Window Functions", "definition": "Functions that operate across a 'window' of rows related to the current row. PARTITION BY defines the groups, ORDER BY defines the sequence, and ROWS/RANGE defines the frame. Essential for rolling averages, rankings, and period-over-period comparisons."},
    {"term": "Denormalization", "definition": "Joining dimension attributes into a fact table (or view) so downstream consumers don't need to write JOINs. Trades some redundancy for query simplicity. Views are perfect for this since they don't actually duplicate storage."},
])

render_domain_glossary([
    {"term": "Fill Rate", "definition": "Percentage of demand met from available inventory. 100% means every customer found what they wanted. Ross targets ~92-95% — slightly lower than traditional retail because the treasure-hunt model means not every item is always in stock."},
    {"term": "Revenue per Square Foot", "definition": "A space productivity metric: total revenue / store square footage. Ross averages ~$380-420/sqft annually. Helps compare stores of different sizes on an equal footing."},
    {"term": "Inventory Turnover", "definition": "How many times inventory cycles through in a year. Calculated as annual units sold / average inventory. Higher is better (less capital tied up). Off-price retail targets 12-14x vs. 4-6x for department stores."},
])

render_what_you_built([
    "INVENTORY_HEALTH view — real-time stockout risk classification for every store/product",
    "SALES_WITH_SEASONALITY view — denormalized sales with rolling averages and calendar context",
    "STORE_PERFORMANCE_SUMMARY view — store-level KPI scorecard with fill rate, turnover, lost revenue",
])
