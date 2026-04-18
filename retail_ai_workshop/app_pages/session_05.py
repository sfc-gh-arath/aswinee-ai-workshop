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
    session_num=5,
    title="Real-time Inference with Dynamic Tables",
    time_range="11:25 - 11:45 AM",
    duration="20 min",
    building="Dynamic table for live stockout scoring",
)

render_technologies_used([
    {"name": "Dynamic Tables", "description": "Declarative data pipelines that automatically refresh when upstream data changes. Define the transformation as a query and Snowflake handles the rest - scheduling, incremental refresh, and dependency management.", "icon": "sync"},
    {"name": "Model Inference (PREDICT)", "description": "Calling a trained model's PREDICT method directly in SQL. The model runs inside Snowflake's compute layer - no external serving infrastructure needed.", "icon": "bolt"},
    {"name": "TARGET_LAG", "description": "The maximum acceptable staleness for a dynamic table. Snowflake automatically determines when to refresh based on upstream changes and this lag setting.", "icon": "timer"},
])


PROMPT_5_1 = """In RETAIL_AI_DEMO.RETAIL_OPS, create a dynamic table called LIVE_STOCKOUT_SCORES that:

1. Uses a TARGET_LAG of '1 minute' and the RETAIL_AI_WH warehouse
2. Joins INVENTORY_LEVELS with PRODUCTS and STORES (same joins as STOCKOUT_FEATURES)
3. Computes the same features as our STOCKOUT_FEATURES view
4. Calls STOCKOUT_PREDICTION_MODEL!PREDICT() to score every SKU-store combination
5. Includes columns: product_id, store_id, store_name, product_name, category, snapshot_date, predicted_stockout_class, predicted_stockout_probability, quantity_on_hand, days_of_supply, reorder_point

Execute the CREATE DYNAMIC TABLE statement, then query it to show the top 10 highest-risk SKU-store combinations (sorted by predicted_stockout_probability descending)."""

render_prompt("Prompt 5.1", "Create Dynamic Table for Live Scoring", PROMPT_5_1)

render_explanation("What this prompt does", """
This creates a **dynamic table** that operationalizes our ML model:

```sql
CREATE OR REPLACE DYNAMIC TABLE LIVE_STOCKOUT_SCORES
  TARGET_LAG = '1 minute'
  WAREHOUSE = RETAIL_AI_WH
AS
  SELECT
    i.product_id,
    i.store_id,
    s.store_name,
    p.product_name,
    p.category,
    i.snapshot_date,
    STOCKOUT_PREDICTION_MODEL!PREDICT(...) AS prediction,
    i.quantity_on_hand,
    i.days_of_supply,
    i.reorder_point
  FROM INVENTORY_LEVELS i
  JOIN PRODUCTS p ON i.product_id = p.product_id
  JOIN STORES s ON i.store_id = s.store_id;
```

**Dynamic Tables vs. Traditional ETL**:

| Traditional | Dynamic Tables |
|-------------|---------------|
| Write scheduled tasks/stored procedures | Declare the desired state as SQL |
| Manage dependencies manually | Auto-detects upstream changes |
| Full refresh or complex incremental logic | Automatic incremental refresh |
| Separate monitoring/alerting | Built-in refresh history & health |

**TARGET_LAG = '1 minute'**: This means the dynamic table will never be more than 1 minute behind its source data. When new rows are inserted into INVENTORY_LEVELS, Snowflake detects the change and triggers a refresh within 1 minute.

**Why this is powerful for retail**: The entire pipeline - feature engineering + stockout prediction - runs automatically. There's no Airflow DAG, no cron job, no orchestrator. When a store's inventory drops, the risk score updates within a minute. Replenishment planners always see current data.

**Cost consideration**: A 1-minute lag means the warehouse stays active for frequent refreshes. In production, you'd typically set this to 5-15 minutes depending on your freshness requirements. For overnight replenishment cycles, '1 hour' may be sufficient.
""")


PROMPT_5_2 = """In RETAIL_AI_DEMO.RETAIL_OPS:

1. Insert 5 new rows into INVENTORY_LEVELS with snapshot_date = CURRENT_DATE, representing today's inventory snapshots with varying risk levels:
   - 2 high-risk: low quantity_on_hand (below reorder_point), low days_of_supply (< 3 days) — these should trigger stockout alerts
   - 1 moderate: quantity near reorder_point, days_of_supply around 5-7
   - 2 healthy: well above reorder_point, days_of_supply > 14
   
2. Wait a moment, then query LIVE_STOCKOUT_SCORES to show these 5 new records are now scored with predictions

3. Also show the DYNAMIC_TABLE_REFRESH_HISTORY for LIVE_STOCKOUT_SCORES to demonstrate the automatic refresh

Execute all SQL and show results."""

render_prompt("Prompt 5.2", "Simulate New Data and Watch Refresh", PROMPT_5_2)

render_explanation("What this prompt does", """
This demonstrates the **real-time nature** of dynamic tables:

1. **Insert new data**: We add 5 new inventory snapshots representing today's stock levels across different stores and products.

2. **Observe auto-refresh**: Within ~1 minute, the LIVE_STOCKOUT_SCORES table automatically refreshes and scores the new inventory records.

3. **Refresh history**: The `DYNAMIC_TABLE_REFRESH_HISTORY` function shows:
   - When each refresh started and completed
   - Whether it was incremental or full
   - How many rows were added/updated
   - Compute resources consumed

```sql
SELECT *
FROM TABLE(INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME => 'RETAIL_AI_DEMO.RETAIL_OPS.LIVE_STOCKOUT_SCORES'
))
ORDER BY refresh_start_time DESC
LIMIT 5;
```

**This is the "aha moment"**: You insert new inventory data and downstream stockout scoring happens automatically with no code, no scheduling, no orchestration. A store receives a shipment, the POS system updates inventory, and within a minute the ML model re-scores every SKU. This is what "declarative data pipelines" means in practice.

**Real-world retail application**: In a live deployment, INVENTORY_LEVELS would be fed by POS transactions, warehouse management systems, and e-commerce order feeds. The dynamic table ensures stockout predictions are always current, enabling automated alerts to store managers and replenishment planners.
""")


render_key_concepts([
    {"term": "Dynamic Tables", "definition": "A Snowflake table type defined by a SQL query that automatically maintains its contents as source data changes. Think of it as a materialized view that Snowflake keeps up-to-date for you, with configurable freshness guarantees."},
    {"term": "TARGET_LAG", "definition": "The maximum acceptable time between when source data changes and when the dynamic table reflects those changes. Set to '1 minute' for near-real-time, or '1 hour' / '1 day' for less time-sensitive pipelines."},
    {"term": "Incremental Refresh", "definition": "Dynamic tables can detect which source rows changed and only process the delta, rather than reprocessing the entire dataset. This is dramatically more efficient for large tables with small change volumes."},
])

render_domain_glossary([
    {"term": "Stockout", "definition": "When a product is completely out of stock at a location. Stockouts in apparel retail are costly - customers rarely wait and instead buy from competitors or substitute products. Industry estimates suggest stockouts cause 4-8% revenue loss annually."},
    {"term": "Days of Supply", "definition": "How many days current inventory will last at the current sales velocity. Calculated as (quantity on hand / average daily sales). Below 3 days is typically critical for fast-moving apparel categories."},
    {"term": "Reorder Point", "definition": "The inventory level at which a new purchase order should be triggered. Calculated based on lead time, average daily demand, and safety stock. When quantity on hand drops below the reorder point, replenishment is needed."},
])

render_what_you_built([
    "LIVE_STOCKOUT_SCORES dynamic table with 1-minute lag",
    "Automated ML scoring pipeline (no orchestrator needed)",
    "5 new test records showing real-time scoring",
])
