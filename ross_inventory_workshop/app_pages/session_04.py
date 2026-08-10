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
    session_num=4,
    title="Dynamic Tables",
    time_range="1:15 - 1:40",
    duration="25 min",
    building="Auto-refreshing replenishment signals and stockout risk scores",
)

render_technologies_used([
    {"name": "Dynamic Tables", "description": "Snowflake objects that automatically refresh their contents based on a declarative SQL query and a target lag. You define WHAT you want; Snowflake handles WHEN and HOW to refresh it.", "icon": "autorenew"},
    {"name": "TARGET_LAG", "description": "The maximum staleness you'll accept. Set to '1 hour' and Snowflake ensures the dynamic table is never more than 1 hour behind its source data. Can be minutes, hours, or downstream (match upstream).", "icon": "timer"},
    {"name": "Incremental Refresh", "description": "Dynamic tables detect what changed in source data and only process the delta. Much cheaper than rebuilding the entire table on a schedule.", "icon": "bolt"},
])


PROMPT_4_1 = """Create a dynamic table called ROSS_INVENTORY_LAB.ANALYTICS.DT_REPLENISHMENT_SIGNALS with TARGET_LAG = '1 hour' and WAREHOUSE = INVENTORY_LAB_WH.

This table should identify store/product combinations that need replenishment action RIGHT NOW. The query should:

1. Start from the most recent INVENTORY_SNAPSHOTS (latest snapshot_date per store/product)
2. JOIN with PRODUCTS to get reorder_point, lead_time_days, pack_size
3. JOIN with STORES to get store_name, region
4. Calculate avg_daily_demand from DAILY_SALES (last 28 days)
5. Calculate:
   - days_of_supply: on_hand_qty / NULLIF(avg_daily_demand, 0)
   - projected_stockout_date: CURRENT_DATE + days_of_supply
   - needs_reorder: on_hand_qty <= reorder_point
   - suggested_order_qty: CEIL((avg_daily_demand * (lead_time_days + 14) - on_hand_qty) / pack_size) * pack_size
     (order enough for lead time + 2 weeks safety stock, rounded up to full packs)
   - urgency: CASE when days_of_supply <= lead_time_days THEN 'EMERGENCY' when days_of_supply <= lead_time_days + 7 THEN 'URGENT' when needs_reorder THEN 'STANDARD' ELSE 'NO_ACTION' END
6. Only include rows where needs_reorder = TRUE or days_of_supply < 21

Add a COMMENT: 'Auto-refreshing replenishment signals - identifies items needing reorder'.

Execute, then query it: show me the top 10 EMERGENCY items sorted by estimated_lost_revenue potential (avg_daily_demand * retail_price * lead_time_days)."""

render_prompt("Prompt 4.1", "Replenishment Signals Dynamic Table", PROMPT_4_1)

render_explanation("What this prompt does", """
Creates a **dynamic table** that automatically identifies what needs to be reordered:

**Why a dynamic table instead of a view?**
- Views recompute every time they're queried — fine for ad-hoc analysis
- Dynamic tables pre-compute and store results — better for operational dashboards, downstream consumers, and when the query is expensive
- The TARGET_LAG of 1 hour means this table is always within 1 hour of reality

**The replenishment logic**:
- **Suggested order quantity**: Covers lead time + 2 weeks safety stock, rounded to full packs (you can't order 13 units if pack_size is 12)
- **Urgency levels**: EMERGENCY means you'll stock out before the next delivery can arrive. URGENT means you're cutting it close. STANDARD means reorder point was hit but there's buffer.
- **Filter to actionable rows**: Only shows items that need attention — not the full inventory

**In production**: This table would feed an alert system or a replenishment dashboard that buyers check every morning.
""")


PROMPT_4_2 = """Create a second dynamic table called ROSS_INVENTORY_LAB.ANALYTICS.DT_STOCKOUT_RISK_SCORE with TARGET_LAG = 'DOWNSTREAM' and WAREHOUSE = INVENTORY_LAB_WH.

This table scores every active store/product combination on stockout probability using multiple risk factors. The query should:

1. Start from DT_REPLENISHMENT_SIGNALS (our first dynamic table — this creates a pipeline)
2. JOIN with STOCKOUT_EVENTS to get historical stockout frequency for each store/product
3. JOIN with PURCHASE_ORDERS to check if there are any pending/in_transit orders
4. Calculate a composite risk_score (0-100) based on:
   - inventory_factor (40 points): Scale based on days_of_supply (0 DOS = 40pts, 30+ DOS = 0pts)
   - history_factor (25 points): Based on number of past stockout events (3+ events = 25pts, 0 = 0pts)
   - supply_factor (20 points): 20pts if no pending PO exists, 0pts if resupply is in transit
   - seasonality_factor (15 points): 15pts if current month is in a peak season for this category, 0 otherwise
5. Classify risk_tier: 'CRITICAL' (score >= 75), 'HIGH' (>= 50), 'MODERATE' (>= 25), 'LOW' (< 25)
6. Include: store_name, region, product_name, category, brand, days_of_supply, risk_score, risk_tier, all individual factors, has_pending_order (BOOLEAN)

Add a COMMENT. Execute, then show me the distribution of risk_tier across all rows, and the top 5 CRITICAL risk items."""

render_prompt("Prompt 4.2", "Stockout Risk Score Dynamic Table", PROMPT_4_2)

render_explanation("What this prompt does", """
Creates a **downstream dynamic table** that builds on the first one — forming a data pipeline:

**TARGET_LAG = 'DOWNSTREAM'**: This table refreshes automatically whenever DT_REPLENISHMENT_SIGNALS refreshes. No need to specify a separate schedule — it inherits from upstream.

**The scoring model** combines four risk factors:
1. **Inventory factor (40%)**: How much stock do you have relative to demand?
2. **History factor (25%)**: Has this store/product stocked out before? Past behavior predicts future risk.
3. **Supply factor (20%)**: Is there a purchase order on the way? Pending supply reduces risk.
4. **Seasonality factor (15%)**: Are we entering a peak demand period for this category?

**Why a composite score**: Single metrics (like days_of_supply alone) miss context. A product with 5 DOS but a delivery arriving tomorrow is different from one with 5 DOS and no order placed. The composite score captures this.

**Pipeline pattern**: DT_REPLENISHMENT_SIGNALS → DT_STOCKOUT_RISK_SCORE demonstrates how dynamic tables can be chained. Snowflake manages the refresh order automatically.
""")


PROMPT_4_3 = """Show me the status of both dynamic tables in ROSS_INVENTORY_LAB.ANALYTICS:

1. Run DESCRIBE DYNAMIC TABLE for each
2. Show the refresh history (any refreshes that have happened)
3. Query DT_STOCKOUT_RISK_SCORE and show:
   - Count of items in each risk_tier
   - Average risk_score by region
   - The category with the highest average risk_score
4. Explain how these tables will stay fresh as new data arrives in the RAW schema

Also show me: if I INSERT a new row into RAW.INVENTORY_SNAPSHOTS with on_hand_qty = 0 for a specific product, how long until it appears in DT_STOCKOUT_RISK_SCORE as CRITICAL?"""

render_prompt("Prompt 4.3", "Monitor & Understand the Pipeline", PROMPT_4_3)

render_explanation("What this prompt does", """
Explores the **operational characteristics** of dynamic tables:

- **DESCRIBE DYNAMIC TABLE**: Shows the definition, target lag, warehouse, and current state
- **Refresh history**: Confirms that Snowflake has refreshed the tables (or is about to)
- **Business queries**: Validates the risk scores make business sense (are the right things flagged?)
- **Freshness demonstration**: Illustrates the end-to-end latency from raw data change to materialized insight

**Key takeaway for analysts**: You defined the business logic once. Snowflake handles:
- When to refresh (based on target lag)
- What to refresh (incremental changes only)
- Dependency ordering (downstream waits for upstream)
- Compute scaling (uses your warehouse only when refreshing)

**Compared to traditional approaches**: No cron jobs, no stored procedures, no orchestration tools. The equivalent before dynamic tables would be a Task + Stored Procedure combination with manual dependency management.
""")


render_key_concepts([
    {"term": "Dynamic Table", "definition": "A Snowflake object defined by a SELECT query and a TARGET_LAG. Snowflake automatically materializes and incrementally refreshes the results. Combines the freshness of a view with the performance of a table."},
    {"term": "TARGET_LAG", "definition": "Maximum acceptable staleness. '1 hour' means the table may be up to 1 hour behind source data. 'DOWNSTREAM' means it refreshes whenever its upstream source refreshes. Shorter lag = more frequent refresh = more compute cost."},
    {"term": "Pipeline (DT chaining)", "definition": "Dynamic tables can reference other dynamic tables, forming a DAG (directed acyclic graph). Snowflake handles the refresh order automatically. Change propagates through the pipeline within the defined lag constraints."},
])

render_domain_glossary([
    {"term": "Safety Stock", "definition": "Extra inventory held as a buffer against demand variability and supply uncertainty. Typically 1-2 weeks of average demand for off-price retail. The 'insurance policy' against stockouts."},
    {"term": "Lead Time", "definition": "The time between placing a purchase order and receiving the goods. Includes supplier processing, manufacturing (if needed), shipping, and receiving. Domestic: 3-7 days. International: 14-45 days."},
    {"term": "Pack Size", "definition": "The minimum order quantity from a supplier, typically one case/carton. If pack_size is 12, you must order in multiples of 12 — you can't order 7 units."},
])

render_what_you_built([
    "DT_REPLENISHMENT_SIGNALS — auto-refreshing table identifying items needing reorder with urgency levels",
    "DT_STOCKOUT_RISK_SCORE — composite risk scoring pipeline (downstream of replenishment signals)",
    "Verified the dynamic table pipeline: refresh status, lag behavior, and business validation",
])
