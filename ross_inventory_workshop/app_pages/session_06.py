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
    session_num=6,
    title="Semantic View & Cortex Analyst",
    time_range="2:20 - 2:45",
    duration="25 min",
    building="Natural language to SQL with business-aware metadata",
)

render_technologies_used([
    {"name": "Semantic View", "description": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that describes your data in business terms: tables, relationships, facts, dimensions, metrics, and synonyms. The bridge between natural language and SQL.", "icon": "description"},
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL queries. Uses a semantic view to understand your data's business meaning, relationships, and metrics.", "icon": "chat"},
    {"name": "AI_SQL_GENERATION", "description": "Custom instructions embedded in the semantic view that guide how Cortex Analyst generates SQL. Provides domain context and disambiguation hints specific to inventory management.", "icon": "auto_fix_high"},
])


PROMPT_6_1 = """Create a semantic view called ROSS_INVENTORY_LAB.ANALYTICS.INVENTORY_OPTIMIZATION_SV for use with Cortex Analyst. It should cover these tables from the ANALYTICS schema:
- INVENTORY_HEALTH
- SALES_WITH_SEASONALITY
- STORE_PERFORMANCE_SUMMARY
And these from RAW:
- PRODUCTS
- STORES
- CALENDAR

Include:
- RELATIONSHIPS:
  - INVENTORY_HEALTH joins PRODUCTS via product_id (through the view's embedded product data)
  - INVENTORY_HEALTH joins STORES via store_id
  - SALES_WITH_SEASONALITY joins PRODUCTS via product_id
  - SALES_WITH_SEASONALITY joins STORES via store_id
  - SALES_WITH_SEASONALITY joins CALENDAR via sale_date = cal_date
  - STORE_PERFORMANCE_SUMMARY joins STORES via store_id

- FACTS for key numeric columns:
  - From INVENTORY_HEALTH: on_hand_qty, on_order_qty, in_transit_qty, days_of_supply, weeks_of_cover
  - From SALES_WITH_SEASONALITY: units_sold, revenue, discount_pct, rolling_7day_avg_units, rolling_7day_avg_revenue
  - From STORE_PERFORMANCE_SUMMARY: total_revenue, total_units_sold, total_stockout_events, total_lost_revenue, fill_rate_pct, inventory_turnover, revenue_per_sqft

- DIMENSIONS:
  - category, subcategory, brand, product_name (from products/views)
  - store_name, city, state, region, district, format (from stores/views)
  - season, month_name, quarter, fiscal_period, event_name, day_of_week (from calendar/views)
  - stockout_risk, overstock_flag, reorder_needed (from INVENTORY_HEALTH)

- SYNONYMS:
  - category WITH SYNONYMS = ('department', 'product type', 'merchandise class')
  - days_of_supply WITH SYNONYMS = ('DOS', 'days of cover', 'stock cover')
  - stockout_risk WITH SYNONYMS = ('OOS risk', 'out of stock risk', 'availability risk')
  - fill_rate_pct WITH SYNONYMS = ('service level', 'in-stock rate', 'availability')
  - region WITH SYNONYMS = ('area', 'territory', 'geography')
  - revenue WITH SYNONYMS = ('sales', 'sales dollars')
  - units_sold WITH SYNONYMS = ('volume', 'quantity sold', 'pieces')

- METRICS:
  - total_revenue: SUM(revenue)
  - total_units: SUM(units_sold)
  - avg_days_of_supply: AVG(days_of_supply)
  - stockout_rate: COUNT_IF(stockout_risk = 'CRITICAL') / COUNT(*)
  - avg_fill_rate: AVG(fill_rate_pct)
  - total_lost_sales: SUM(total_lost_revenue)
  - avg_inventory_turnover: AVG(inventory_turnover)

- AI_SQL_GENERATION instruction: "This is Ross Stores inventory data. Ross is an off-price retailer with ~1800 stores. Key business context: holiday season is Nov-Dec, back-to-school is July-Aug. DOS (days of supply) below 7 is concerning. Fill rate target is 93%. Inventory turnover target is 13x annually. When asked about 'risk' or 'at risk' items, use the stockout_risk dimension. When asked about store performance, use STORE_PERFORMANCE_SUMMARY. Fiscal periods follow a 4-5-4 retail calendar."

- Descriptive COMMENTs on every table, fact, dimension, and metric.

Execute and verify with DESCRIBE SEMANTIC VIEW."""

render_prompt("Prompt 6.1", "Create the Semantic View", PROMPT_6_1)

render_explanation("What this prompt does", """
Creates a comprehensive **semantic view** that enables natural language queries over our entire analytics layer:

**What's included**:
- 6 tables (3 analytics views + 3 raw dimensions)
- Proper relationships (how tables join)
- Facts (raw numeric columns for computation)
- Dimensions (categorical columns for filtering/grouping)
- Metrics (pre-defined aggregations ready to use)
- Synonyms (alternative terms users might say)
- AI instructions (domain context for better SQL generation)

**Why synonyms matter**: An analyst asking about "DOS" or "stock cover" means the same thing as "days_of_supply." Without synonyms, Cortex Analyst might not map the question correctly.

**Why AI_SQL_GENERATION matters**: It provides business context that column names alone don't convey — like what "at risk" means, what the targets are, and which calendar system Ross uses.
""")


PROMPT_6_2 = """Ask Cortex Analyst these questions using ROSS_INVENTORY_LAB.ANALYTICS.INVENTORY_OPTIMIZATION_SV. Show both the generated SQL and results for each:

1. "Which stores have the lowest fill rate?"
2. "Show me all critical stockout risk items in the West region"
3. "What's the average DOS by product category?"
4. "Which categories had the biggest revenue drop during back-to-school vs holiday?"

These test different aspects: metrics, dimension filtering, aggregation, and time-based comparison."""

render_prompt("Prompt 6.2", "Test Basic Queries", PROMPT_6_2)

render_explanation("What this prompt does", """
Tests Cortex Analyst with four deliberately different question types:

1. **"Lowest fill rate"** — Tests the fill_rate metric + ranking (uses STORE_PERFORMANCE_SUMMARY)
2. **"Critical stockout risk in West"** — Tests dimension filtering on both stockout_risk AND region
3. **"Average DOS by category"** — Tests metric aggregation grouped by dimension
4. **"Revenue drop BTS vs holiday"** — Tests time-based comparison using the AI_SQL_GENERATION context about seasons

**What to watch for**: Does Analyst pick the right tables? Does it interpret "DOS" correctly via synonyms? Does it know that "back-to-school" means July-August from the AI instructions?
""")


PROMPT_6_3 = """Now test Cortex Analyst with more complex questions that require joins across multiple tables:

1. "What's the total lost revenue from stockouts at stores with fill rate below 90%?"
2. "Show me the top 5 brands by units sold during the holiday season at flagship stores"
3. "For products with critical stockout risk, what was their average weekly sales velocity last month?"
4. "Compare inventory turnover between superstore and standard format stores"

Show the SQL and results. If any question fails or gives a wrong answer, explain why and what we could add to the semantic view to fix it."""

render_prompt("Prompt 6.3", "Test Complex Multi-Table Queries", PROMPT_6_3)

render_explanation("What this prompt does", """
Pushes Cortex Analyst harder with **multi-table, multi-concept questions**:

1. **Lost revenue + fill rate filter**: Requires joining STOCKOUT data with STORE_PERFORMANCE
2. **Brand + season + format**: Three-way filter across different dimensions
3. **Risk status + sales velocity**: Combines current risk classification with historical demand
4. **Format comparison**: Tests that "superstore" and "standard" are understood as store format values

**The 'fix it' instruction**: If a question fails, that's pedagogically valuable. It shows that semantic views are iterative — you build, test, identify gaps, and expand. Common fixes include adding missing synonyms, metrics, or relationships.
""")





render_key_concepts([
    {"term": "Semantic View", "definition": "A first-class Snowflake object that maps database tables to business concepts. Contains table definitions, relationships, facts, dimensions, metrics, synonyms, and AI instructions. The 'understanding layer' between natural language and SQL."},
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Takes natural language questions and generates SQL using the semantic view for context. Can be invoked programmatically or via CoWork (once an agent is created in Session 8)."},
    {"term": "Facts vs Dimensions vs Metrics", "definition": "Facts are raw numeric columns (on_hand_qty). Dimensions are categorical/temporal columns for grouping and filtering (region, season). Metrics are pre-defined aggregations (AVG days_of_supply). All three are defined in the semantic view."},
])

render_domain_glossary([
    {"term": "Text-to-SQL", "definition": "The AI capability of converting a natural language question into a valid SQL query. The semantic view provides the business context needed to generate correct queries (which tables to use, how to join them, what metrics mean)."},
    {"term": "Service Level Agreement (SLA)", "definition": "In inventory management, the target fill rate. Ross's 93% target means accepting that 7% of demand may go unfilled — a deliberate trade-off between inventory cost and availability in off-price retail."},
])

render_what_you_built([
    "INVENTORY_OPTIMIZATION_SV semantic view covering 6 tables with relationships, metrics, and AI instructions",
    "Tested 4 basic queries validating dimension filtering, metrics, and seasonal logic",
    "Tested 4 complex multi-table queries identifying any semantic view gaps",
])
