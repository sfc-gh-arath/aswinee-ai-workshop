import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(10, "Cortex Analyst & Semantic Views", "2:30 - 2:50 PM", "20 min", "Semantic view creation, AI-assisted expansion, and natural language queries")

render_technologies_used([
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL queries. Uses a semantic view to understand your data's business meaning, relationships, and metrics.", "icon": "chat"},
    {"name": "Semantic View", "description": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that describes your data in business terms: tables, relationships, facts, dimensions, metrics, and synonyms. The bridge between natural language and SQL.", "icon": "description"},
    {"name": "AI_SQL_GENERATION", "description": "Custom instructions embedded in the semantic view that guide how Cortex Analyst generates SQL. Provides domain context, business rules, and disambiguation hints for Alpine & Co. retail data.", "icon": "auto_fix_high"},
])


PROMPT_10_1 = """In RETAIL_AI_DEMO.RETAIL_OPS, create a semantic view called RETAIL_OPERATIONS_VIEW for use with Cortex Analyst. It should cover these 6 tables: SALES_TRANSACTIONS, PURCHASE_ORDERS, INVENTORY_LEVELS, PRODUCTS, STORES, SUPPLIERS.

Include:
- Proper relationships between the tables:
  - SALES_TRANSACTIONS joins PRODUCTS via product_id
  - SALES_TRANSACTIONS joins STORES via store_id
  - PURCHASE_ORDERS joins SUPPLIERS via supplier_id
  - PURCHASE_ORDERS joins PRODUCTS via product_id
  - INVENTORY_LEVELS joins STORES via store_id AND PRODUCTS via product_id
- Facts for all key numeric columns: quantity, unit_price, discount_pct, total_amount (from SALES_TRANSACTIONS), quantity_ordered, quantity_received, unit_cost, total_cost (from PURCHASE_ORDERS), quantity_on_hand, days_of_supply (from INVENTORY_LEVELS), retail_price, margin_pct (from PRODUCTS)
- Dimensions for categorical columns: category, subcategory, brand, season, gender (from PRODUCTS), store_name, city, state, store_type (from STORES), payment_method, channel (from SALES_TRANSACTIONS), company_name, country (from SUPPLIERS), all status columns, and all date/time columns
- Add useful SYNONYMS on dimensions where users might use different terms:
  - category WITH SYNONYMS = ('department', 'product type')
  - brand WITH SYNONYMS = ('label', 'maker')
  - store_name WITH SYNONYMS = ('location', 'branch')
  - channel WITH SYNONYMS = ('sales channel')
- Metrics with pre-aggregated calculations:
  - total_revenue: SUM(total_amount)
  - total_units_sold: SUM(quantity)
  - avg_transaction_value: AVG(total_amount)
  - total_cost: SUM(total_cost) from PURCHASE_ORDERS
  - avg_days_of_supply: AVG(days_of_supply)
  - inventory_value: SUM(quantity_on_hand * retail_price)
- Descriptive COMMENTs on every table, fact, dimension, and metric explaining the business meaning
- An AI_SQL_GENERATION instruction that provides domain context: this is Alpine & Co. retail data, a national apparel and footwear retailer with 120+ stores, peak seasons are Nov-Dec (holiday) and August (back-to-school), private labels are Summit (activewear) and Basecamp (casual basics)

Execute the SQL and confirm with DESCRIBE SEMANTIC VIEW."""

render_prompt("Prompt 10.1", "Create the Semantic View", PROMPT_10_1)

render_explanation("What this prompt does", """
Creates a **semantic view** - a first-class Snowflake object that enables natural language to SQL:

**Key components of a semantic view**:

- **TABLES**: Logical tables with aliases, primary keys, and comments
- **RELATIONSHIPS**: Foreign key joins between tables (e.g., transactions -> products, transactions -> stores)
- **FACTS**: Raw numeric columns available for computation (quantity, unit_price, total_amount)
- **DIMENSIONS**: Categorical and temporal columns for grouping/filtering, with optional synonyms
- **METRICS**: Pre-defined aggregations (SUM, AVG, COUNT) that Cortex Analyst can use directly
- **AI_SQL_GENERATION**: Custom instructions that guide how Analyst generates SQL

**Synonyms** help Cortex Analyst understand different ways users refer to the same concept:
```sql
t.category ... WITH SYNONYMS = ('department', 'product type')
```
A user asking about "departments" will be matched to the category dimension.

**Facts vs Metrics**:
- Facts are raw columns (e.g., `total_amount`) — building blocks
- Metrics are pre-defined aggregations (e.g., `SUM(total_amount)`) — ready-to-use calculations

**Why 6 tables**: The semantic view connects the star schema — PRODUCTS, STORES, and SUPPLIERS are dimension tables; SALES_TRANSACTIONS and PURCHASE_ORDERS are fact tables; INVENTORY_LEVELS bridges both. Cortex Analyst uses these relationships to generate multi-table JOINs from simple English questions.
""")


PROMPT_10_2 = """Ask Cortex Analyst these two questions using RETAIL_AI_DEMO.RETAIL_OPS.RETAIL_OPERATIONS_VIEW:

1. "What are the top 5 stores by total revenue?"
2. "What is the average foot traffic by store on weekends?"

Show the generated SQL and results for each."""

render_prompt("Prompt 10.2", "Test the Semantic View", PROMPT_10_2)

render_explanation("What this prompt does", """
Tests the semantic view with two deliberately chosen questions:

**Question 1 should work well** — "Top 5 stores by total revenue" maps cleanly to the `total_revenue` metric and `store_name` dimension we defined. Analyst has everything it needs: the metric, the dimension, and the relationship between transactions and stores.

**Question 2 should fall short** — "Average foot traffic by store on weekends" references data in the STORE_FOOT_TRAFFIC table, which **isn't in our semantic view yet**. Analyst may:
- Return an error saying it can't answer the question
- Attempt an answer using only the tables it knows about, producing incorrect or misleading results
- Hallucinate a plausible-looking but wrong query

**This is the key insight**: A semantic view is only as good as the tables and definitions it contains. When users ask questions outside the view's scope, Analyst can't help — and the failure mode matters. In the next prompt, we'll expand the view to cover this gap.
""")


PROMPT_10_3 = """Now expand our RETAIL_OPERATIONS_VIEW semantic view in RETAIL_AI_DEMO.RETAIL_OPS to include two more tables: STORE_FOOT_TRAFFIC and DAILY_SALES_METRICS.

1. Query INFORMATION_SCHEMA.COLUMNS to get the full schema of STORE_FOOT_TRAFFIC and DAILY_SALES_METRICS
2. Use SNOWFLAKE.CORTEX.COMPLETE() to generate the additional facts, dimensions, and metrics definitions from those schemas — have it suggest useful synonyms and descriptive comments
3. Recreate RETAIL_OPERATIONS_VIEW with all original definitions plus the new tables, relationships to STORES via store_id, and the AI-generated definitions

Execute and verify with DESCRIBE SEMANTIC VIEW."""

render_prompt("Prompt 10.3", "Expand the Semantic View with AI", PROMPT_10_3)

render_explanation("What this prompt does", """
Uses an LLM to **expand** the semantic view with additional tables:

**Schema extraction** from INFORMATION_SCHEMA gives the LLM the raw column names and types for STORE_FOOT_TRAFFIC and DAILY_SALES_METRICS.

**LLM generation** via CORTEX.COMPLETE():
- Infers business meaning from column names (e.g., `visitor_count` -> "Number of visitors entering the store")
- Generates appropriate SYNONYMS (e.g., `visitor_count` WITH SYNONYMS = ('foot traffic', 'footfall', 'walk-ins'))
- Creates METRICS with useful aggregations (AVG daily foot traffic, conversion rate)
- Suggests RELATIONSHIPS to existing tables

**Why this pattern is powerful**:
- Bootstraps semantic view definitions in seconds vs. hours of manual work
- LLM understands naming conventions and infers domain meaning
- Always review the output — join paths and aggregation types may need adjustment

This demonstrates the **iterative semantic view development cycle**: create a base view, expand with AI assistance, test, and refine.
""")


PROMPT_10_4 = """Using the expanded semantic view RETAIL_AI_DEMO.RETAIL_OPS.RETAIL_OPERATIONS_VIEW (now with 8 tables), ask Cortex Analyst these natural language questions and show both the generated SQL and the results:

1. "What is the average foot traffic by store on weekends?"
2. "What percentage of sales are online vs in-store by product category?"
3. "Which stores have the highest return rates?"
4. "What are the top-selling brands during holiday season?"

Re-ask the foot traffic question from Prompt 10.2 and compare the result now that the table is included."""

render_prompt("Prompt 10.4", "Query with Natural Language", PROMPT_10_4)

render_explanation("What this prompt does", """
Tests Cortex Analyst across both the **original and newly added** tables:

**What to observe for each question**:

1. **"Average foot traffic by store on weekends"** - The same question that failed in Prompt 10.2 — now it should work because STORE_FOOT_TRAFFIC is in the view
2. **"% online vs in-store by category"** - Conditional aggregation on the `channel` dimension, grouped by `category` (original tables)
3. **"Highest return rates"** - Tests whether DAILY_SALES_METRICS has return data or if Analyst attempts to derive it from transactions
4. **"Top-selling brands during holiday season"** - Tests the AI_SQL_GENERATION instruction about Nov-Dec being holiday season, combined with the `brand` dimension and `total_units_sold` metric

**The before/after on the foot traffic question** is the payoff — it demonstrates that expanding the semantic view directly improves what Analyst can answer.

**Synonyms in action**: Try asking about "departments" instead of "categories" or "labels" instead of "brands" — Analyst routes to the correct dimension because of the synonym definitions.
""")


render_key_concepts([
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Takes natural language questions and generates SQL queries using a semantic view for context. Supports aggregations, joins, filtering, time-series analysis, and more."},
    {"term": "Semantic View", "definition": "A first-class Snowflake object (CREATE SEMANTIC VIEW) that maps database tables to business concepts. Contains table definitions, relationships, facts, dimensions, metrics, synonyms, and AI instructions. Replaces the legacy YAML semantic model approach."},
    {"term": "Fact vs Dimension vs Metric", "definition": "Facts are raw numeric columns (total_amount, quantity). Dimensions are categorical/temporal columns for grouping and filtering (category, store_name, transaction_date). Metrics are pre-defined aggregations over facts (SUM(total_amount), AVG(days_of_supply))."},
    {"term": "AI_SQL_GENERATION", "definition": "Custom instructions embedded in the semantic view that guide how Cortex Analyst generates SQL. Use this to provide domain-specific context, define business rules (e.g., holiday season = Nov-Dec), and clarify ambiguous terms (e.g., private labels)."},
])

render_domain_glossary([
    {"term": "Operational KPIs (Retail)", "definition": "Key Performance Indicators for retail operations: revenue per store, units per transaction (UPT), average transaction value (ATV), sell-through rate, inventory turnover, days of supply, gross margin %, and conversion rate. These are the metrics store managers and merchandisers track daily."},
    {"term": "Omnichannel", "definition": "Selling through multiple channels — brick-and-mortar stores, e-commerce, mobile app — with a unified customer experience. Alpine & Co. tracks channel as a dimension on every transaction so analysts can compare online vs in-store performance by category, brand, and region."},
])

render_what_you_built([
    "RETAIL_OPERATIONS_VIEW semantic view with 6 tables, relationships, and AI instructions",
    "Tested Analyst on a question it handles well vs one outside the view's scope",
    "AI-expanded view with STORE_FOOT_TRAFFIC and DAILY_SALES_METRICS (8 tables total)",
    "4 natural language queries — including a before/after comparison on foot traffic data",
])
