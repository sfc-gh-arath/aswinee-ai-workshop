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
    title="Foundation & Reference Data",
    time_range="9:15 - 9:45 AM",
    duration="30 min",
    building="Database, schema, warehouse, and core reference tables",
)

render_technologies_used([
    {"name": "CREATE DATABASE / SCHEMA", "description": "Snowflake's logical containers for organizing objects. Databases are the top level; schemas group related tables, views, and other objects.", "icon": "database"},
    {"name": "Virtual Warehouses", "description": "Named compute clusters that execute queries. Size (XS to 6XL) determines how many nodes are provisioned. They auto-suspend and auto-resume.", "icon": "memory"},
    {"name": "CREATE TABLE + INSERT", "description": "DDL/DML for defining and populating structured tables. Snowflake uses columnar storage with automatic micro-partitioning.", "icon": "table_chart"},
])


PROMPT_1_1 = """Create a Snowflake database called RETAIL_AI_DEMO with a schema called RETAIL_OPS and a warehouse called RETAIL_AI_WH (size MEDIUM). Add a brief comment on the database: "Retail AI/ML Workshop - Apparel & Footwear Operations". Then create the following reference/lookup tables with realistic sample data:

1. PRODUCTS - 25 rows of apparel and footwear products. Columns: product_id, product_name, category (tops, bottoms, outerwear, activewear, sneakers, boots, sandals, dress_shoes, accessories), subcategory, brand (Nike, Adidas, Levi's, The North Face, New Balance, Under Armour, Columbia, plus private labels Summit and Basecamp), size_range, color, unit_cost, retail_price, margin_pct, season (spring, summer, fall, winter, year_round), gender (mens, womens, unisex, kids). Include a mix of branded and private-label products across all categories.

2. STORES - 8 rows representing Alpine & Co. retail locations. Columns: store_id, store_name, city, state, store_type (flagship, mall, outlet), latitude, longitude (use real coordinates), square_footage, annual_revenue_millions. Use these real US cities: New York, Los Angeles, Chicago, Houston, Portland, Denver, Miami, Seattle.

3. SUPPLIERS - 15 rows of domestic and international apparel/footwear suppliers. Columns: supplier_id, company_name, country, region (Domestic, Asia-Pacific, Europe), primary_category, lead_time_days, reliability_score (1-10), annual_volume_units, payment_terms. Include a mix of domestic (USA), Asian (Vietnam, China, Bangladesh, Indonesia), and European (Italy, Portugal) suppliers.

Make sure to USE the database and schema after creation. Execute all the SQL."""

render_prompt("Prompt 1.1", "Create the Foundation", PROMPT_1_1)

render_explanation("What this prompt does", """
This prompt instructs Cortex Code to generate and execute multiple SQL statements that set up the entire environment:

1. **`CREATE DATABASE RETAIL_AI_DEMO`** - Creates a new database. In Snowflake, a database is the highest-level container for data. The `COMMENT` clause attaches metadata that helps with discovery and documentation.

2. **`CREATE SCHEMA RETAIL_OPS`** - Creates a schema inside the database. Schemas are the primary way to organize tables, views, stages, and other objects into logical groups.

3. **`CREATE WAREHOUSE RETAIL_AI_WH WITH WAREHOUSE_SIZE = 'MEDIUM'`** - Provisions a compute cluster. A MEDIUM warehouse has 4 nodes and costs 4 credits/hour. It auto-suspends after 5 minutes of inactivity by default.

4. **`CREATE TABLE` + `INSERT INTO`** - Defines table structures with typed columns and populates them with synthetic but realistic data. Cortex Code generates the INSERT statements with domain-appropriate values.

**Why we start here**: Every subsequent session depends on these foundational objects. The reference tables (PRODUCTS, STORES, SUPPLIERS) serve as dimension tables that will be joined to fact tables created in Session 2.
""")

render_explanation("Deep dive: Snowflake architecture", """
Snowflake uses a **three-layer architecture**:

- **Cloud Services Layer**: Handles authentication, metadata, query optimization, and transaction management. This is always running.
- **Compute Layer (Virtual Warehouses)**: Executes queries. Warehouses are independent clusters that can be created, resized, suspended, and resumed on demand. Multiple warehouses can access the same data simultaneously.
- **Storage Layer**: Stores data in a proprietary columnar format with automatic compression and micro-partitioning. Data is stored in cloud object storage (S3, Azure Blob, GCS).

**Key concept - Separation of Storage and Compute**: Unlike traditional databases, you can scale compute independently of storage. This means you can have a small warehouse for light queries and a large one for heavy ML training - both reading the same data.

**Micro-partitioning**: Snowflake automatically divides tables into immutable micro-partitions of 50-500 MB. Each partition stores metadata about the min/max values in each column, enabling efficient pruning during queries.
""")

render_explanation("Deep dive: Star schema for retail analytics", """
The tables we're building follow a **star schema** design pattern:

- **Dimension tables** (PRODUCTS, STORES, SUPPLIERS) contain descriptive attributes that don't change frequently - product names, store locations, supplier details.
- **Fact tables** (created in Session 2) contain transactional measures - sales amounts, quantities, timestamps. They reference dimension tables through foreign keys.

**Why star schema for retail**:
- A single `SALES_TRANSACTIONS` fact row links to PRODUCTS (what was sold), STORES (where), and implicitly to SUPPLIERS (who supplied it)
- Analysts can slice-and-dice: "Show me Summit activewear sales at flagship stores in Q4" requires joining the fact table to two dimensions
- Snowflake's columnar storage and micro-partitioning make star schema joins extremely efficient

**Private labels (Summit, Basecamp)**: These are Alpine & Co.'s own brands manufactured by contract suppliers. Private labels typically carry higher margins (50-60%) than branded products (30-40%) because there's no brand licensing cost. Tracking private-label performance vs. branded products is a key retail analytics use case.
""")


PROMPT_1_2 = """Show me the row counts for all three tables we just created (PRODUCTS, STORES, SUPPLIERS) in RETAIL_AI_DEMO.RETAIL_OPS, and show a sample of 3 rows from each table so I can verify the data looks right."""

render_prompt("Prompt 1.2", "Verify and Explore the Foundation", PROMPT_1_2)

render_explanation("What this prompt does", """
This is a verification step. Cortex Code will generate queries like:

```sql
SELECT 'PRODUCTS' AS table_name, COUNT(*) AS row_count FROM RETAIL_AI_DEMO.RETAIL_OPS.PRODUCTS
UNION ALL
SELECT 'STORES', COUNT(*) FROM RETAIL_AI_DEMO.RETAIL_OPS.STORES
UNION ALL
SELECT 'SUPPLIERS', COUNT(*) FROM RETAIL_AI_DEMO.RETAIL_OPS.SUPPLIERS;

SELECT * FROM RETAIL_AI_DEMO.RETAIL_OPS.PRODUCTS LIMIT 3;
```

**Why verify**: It's good practice to confirm that Cortex Code generated the expected number of rows and that the data quality looks right. Since Cortex Code generates synthetic data, you should spot-check that product categories, store locations, and supplier details are realistic. Pay attention to margin percentages - private-label products (Summit, Basecamp) should have higher margins than branded products.
""")


render_key_concepts([
    {"term": "Virtual Warehouse", "definition": "A named compute cluster in Snowflake. Sizes range from X-Small (1 node, 1 credit/hr) to 6X-Large (512 nodes, 512 credits/hr). Warehouses auto-suspend when idle and auto-resume on query. You can have unlimited warehouses running concurrently."},
    {"term": "Database & Schema", "definition": "Databases are the top-level namespace. Schemas sit inside databases and contain tables, views, stages, functions, and other objects. The fully-qualified name is `DATABASE.SCHEMA.OBJECT`."},
    {"term": "Micro-partitioning", "definition": "Snowflake automatically splits table data into immutable chunks of 50-500 MB called micro-partitions. Each partition has metadata (min/max values, null counts) that enables the query optimizer to skip irrelevant partitions, dramatically speeding up filtered queries."},
])

render_domain_glossary([
    {"term": "Alpine & Co.", "definition": "A national apparel and footwear retailer with 120+ stores and an e-commerce presence. Sells a mix of branded products (Nike, Adidas, Levi's, etc.) and two private-label lines: Summit (activewear) and Basecamp (casual basics)."},
    {"term": "SKU (Stock Keeping Unit)", "definition": "A unique identifier for each distinct product variant (style + color + size). A single product like 'Summit Performance Tee' might have 20+ SKUs across sizes S-XXL and 4 colors. SKU proliferation is a key challenge in apparel retail."},
    {"term": "Sell-through Rate", "definition": "The percentage of inventory received that has been sold in a given period. Calculated as (units sold / units received) x 100. A healthy sell-through for apparel is 60-70% at full price. Below 50% typically triggers markdowns."},
])

render_what_you_built([
    "RETAIL_AI_DEMO database with RETAIL_OPS schema",
    "RETAIL_AI_WH warehouse (MEDIUM size)",
    "PRODUCTS table - 25 apparel/footwear items with branded and private-label products",
    "STORES table - 8 Alpine & Co. retail locations across the US",
    "SUPPLIERS table - 15 domestic and international apparel/footwear suppliers",
])
