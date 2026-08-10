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
    title="Data Discovery with Cortex Code",
    time_range="0:30 - 0:50",
    duration="20 min",
    building="Exploratory analysis — understanding data quality, relationships, and patterns",
)

render_technologies_used([
    {"name": "Cortex Code", "description": "Snowflake's AI coding assistant in Snowsight. Ask natural language questions about your data and it generates + executes SQL. The primary tool for this entire lab.", "icon": "psychology"},
    {"name": "INFORMATION_SCHEMA", "description": "Snowflake's metadata layer. Query it to discover tables, columns, data types, row counts, and more without touching the actual data.", "icon": "info"},
    {"name": "Data Profiling", "description": "Techniques for understanding data distributions: COUNT DISTINCT, NULL rates, MIN/MAX, histograms. Essential before building analytics.", "icon": "analytics"},
])


PROMPT_2_1 = """I'm an inventory analyst looking at ROSS_INVENTORY_LAB.RAW. Help me understand this data:

1. Show me all tables in this schema with their row counts and column counts
2. For each table, list the columns with their data types
3. What are the natural join keys between these tables? Show me an ER-diagram-style description of how they relate

Present this as a clear summary I can reference throughout the lab."""

render_prompt("Prompt 2.1", "Discover Schema & Relationships", PROMPT_2_1)

render_explanation("What this prompt does", """
Uses Cortex Code as a **data discovery** tool. Instead of manually querying INFORMATION_SCHEMA, you describe what you need in plain English.

Cortex Code will:
1. Query `INFORMATION_SCHEMA.TABLES` for row counts
2. Query `INFORMATION_SCHEMA.COLUMNS` for column metadata
3. Identify join keys by matching column names (store_id, product_id, etc.)
4. Present a relationship map

**This is how analysts should explore unfamiliar data** — ask questions, not write SQL from scratch. Cortex Code handles the mechanical query-writing so you can focus on understanding the business meaning.
""")


PROMPT_2_2 = """Run a data quality check on ROSS_INVENTORY_LAB.RAW. For each fact table (DAILY_SALES, INVENTORY_SNAPSHOTS, PURCHASE_ORDERS, STOCKOUT_EVENTS), tell me:

1. Are there any NULL values in key columns (store_id, product_id, dates)?
2. Are all store_ids and product_ids valid (exist in the dimension tables)?
3. What's the date range coverage?
4. Any obvious outliers? (e.g., negative quantities, revenue > $10000 for a single transaction, discount_pct > 100)
5. For INVENTORY_SNAPSHOTS: how many rows have on_hand_qty = 0 (stockouts)?

Summarize findings as a data quality report."""

render_prompt("Prompt 2.2", "Data Quality Assessment", PROMPT_2_2)

render_explanation("What this prompt does", """
Performs a comprehensive **data quality assessment** — something every analyst should do before building on top of raw data:

- **Referential integrity**: Do foreign keys actually point to valid dimension rows?
- **Completeness**: Are required fields populated?
- **Range checks**: Are numeric values within reasonable business bounds?
- **Temporal coverage**: Does the data span the expected time period?
- **Business validation**: Stockout frequency as a sanity check

**Why this matters**: If you build views and dashboards on dirty data, you get wrong answers. Discovery catches issues early. In production, these checks would become Data Quality Monitors (DMFs).
""")


PROMPT_2_3 = """Now help me understand the business patterns in ROSS_INVENTORY_LAB.RAW:

1. What are the top 5 product categories by total revenue?
2. Which stores have the most stockout events? Show top 5 with their regions.
3. What's the average days-of-supply across all inventory snapshots? (Calculate as on_hand_qty divided by the average daily units sold for that product at that store)
4. Show me monthly sales trends — is there clear seasonality?
5. What are the most common root causes for stockouts, and which categories are most affected?

Show the results as tables and describe what you see."""

render_prompt("Prompt 2.3", "Business Pattern Analysis", PROMPT_2_3)

render_explanation("What this prompt does", """
Transitions from technical profiling to **business-level understanding**:

1. **Revenue by category**: Establishes which product lines drive the business
2. **Stockout hotspots**: Identifies problem stores for targeted intervention
3. **Days of supply**: The core inventory health metric — are we over or under-stocked?
4. **Seasonality**: Validates that our synthetic data has realistic peaks and valleys
5. **Root cause analysis**: What's causing stockouts — is it demand, supply, or process?

**Key insight**: This is the exact discovery workflow an analyst would follow when handed a new dataset. Cortex Code makes it conversational rather than requiring you to write complex SQL from memory.
""")


render_key_concepts([
    {"term": "Data Profiling", "definition": "The process of examining data to understand its structure, content, relationships, and quality. Includes checking distributions, NULLs, uniqueness, and referential integrity."},
    {"term": "Referential Integrity", "definition": "The guarantee that foreign key values in a fact table always point to a valid row in the corresponding dimension table. Broken references cause incorrect JOIN results."},
    {"term": "Cortex Code for Discovery", "definition": "Using Cortex Code as an interactive data exploration tool. Instead of writing SQL manually, describe what you want to understand and let it generate the appropriate queries. Faster iteration, lower barrier to entry."},
])

render_domain_glossary([
    {"term": "Fill Rate", "definition": "The percentage of customer demand that is met from available stock. A 95% fill rate means 5% of demand goes unfilled (stockouts). Off-price retailers typically target 90-95%."},
    {"term": "Inventory Turnover", "definition": "How many times inventory is sold and replaced in a period. Calculated as COGS / Average Inventory. Higher turnover = more efficient use of capital. Ross targets 12-14x annual turns."},
    {"term": "Root Cause (Stockout)", "definition": "The underlying reason a product went out of stock: demand_spike (sold faster than expected), late_delivery (supplier delay), forecast_error (planned wrong), receiving_delay (arrived but not shelved), allocation_error (sent to wrong store)."},
])

render_what_you_built([
    "Schema and relationship map of all 9 tables",
    "Data quality report identifying any issues in fact tables",
    "Business pattern analysis: revenue, stockouts, seasonality, root causes",
])
