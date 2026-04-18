import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(
    session_num=3,
    title="Security and Governance for AI Workloads",
    time_range="10:15 - 10:40 AM",
    duration="25 min",
    building="4 roles, masking policies, and sensitivity tags",
)

render_technologies_used([
    {"name": "Role-Based Access Control", "description": "Snowflake's RBAC model uses roles as the primary access control mechanism. Privileges are granted to roles, and roles are granted to users. Supports hierarchical role inheritance.", "icon": "admin_panel_settings"},
    {"name": "Dynamic Data Masking", "description": "Column-level security policies that transform data at query time based on the querying user's role. The underlying data is never modified - masking happens on-the-fly.", "icon": "visibility_off"},
    {"name": "Object Tagging", "description": "Metadata tags that can be applied to databases, schemas, tables, and columns. Tags enable data classification, lineage tracking, and policy-based governance at scale.", "icon": "label"},
])


PROMPT_3_1 = """In RETAIL_AI_DEMO, create the following roles and grant structure to demonstrate governance for AI workloads:

1. Create roles: RETAIL_DATA_ENGINEER, RETAIL_DATA_SCIENTIST, RETAIL_MERCHANDISER, FINANCE_ANALYST
2. Grant the following access pattern:
   - RETAIL_DATA_ENGINEER: full access to RETAIL_OPS schema (all privileges on all tables, CREATE privileges on schema)
   - RETAIL_DATA_SCIENTIST: SELECT on all tables in RETAIL_OPS, plus USAGE on RETAIL_AI_WH, plus ability to use Cortex functions (grant SNOWFLAKE.CORTEX_USER database role)
   - RETAIL_MERCHANDISER: SELECT on SALES_TRANSACTIONS, INVENTORY_LEVELS, PRODUCTS, STORES, PURCHASE_ORDERS only (no access to SUPPORT_TICKETS, CUSTOMER_REVIEWS, or financial detail columns)
   - FINANCE_ANALYST: SELECT on SALES_TRANSACTIONS, PURCHASE_ORDERS, DAILY_SALES_METRICS only (cost and margin data access for financial reporting)

3. Grant all roles to my current user so I can test them.

Execute all the SQL and show me a summary of what was granted."""

render_prompt("Prompt 3.1", "RBAC for Retail Operations", PROMPT_3_1)

render_explanation("What this prompt does", """
This creates a realistic **Role-Based Access Control (RBAC)** hierarchy for a retail organization:

**RETAIL_DATA_ENGINEER** - Full access. Can create, modify, and delete objects. This is the "builder" role responsible for data pipelines and infrastructure.

**RETAIL_DATA_SCIENTIST** - Read access to all data plus Cortex AI function access. The `SNOWFLAKE.CORTEX_USER` database role is critical - it grants access to all Cortex LLM functions (COMPLETE, SENTIMENT, TRANSLATE, etc.). Without this role, Cortex calls fail.

**RETAIL_MERCHANDISER** - Limited to operational and inventory data. Can see what's selling, what's in stock, and what's on order - but cannot access customer service tickets, reviews, or financial cost/margin data. This reflects the real separation between merchandising and finance in retail organizations.

**FINANCE_ANALYST** - Focused on financial data: sales revenue, purchase costs, and daily metrics. Cannot see customer reviews, support tickets, or supplier communications. Needs access to cost columns that other roles shouldn't see.

**Key SQL patterns**:
```sql
CREATE ROLE RETAIL_DATA_SCIENTIST;
GRANT USAGE ON DATABASE RETAIL_AI_DEMO TO ROLE RETAIL_DATA_SCIENTIST;
GRANT USAGE ON SCHEMA RETAIL_AI_DEMO.RETAIL_OPS TO ROLE RETAIL_DATA_SCIENTIST;
GRANT SELECT ON ALL TABLES IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS TO ROLE RETAIL_DATA_SCIENTIST;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE RETAIL_DATA_SCIENTIST;
```

**Why this matters for AI**: AI workloads access more data than traditional BI. A single Cortex Agent might query across all tables. Proper RBAC ensures that even AI-powered applications respect data boundaries. A merchandiser's AI assistant shouldn't surface customer complaint details, and a finance analyst's dashboard shouldn't expose supplier negotiation emails.
""")


PROMPT_3_2 = """In RETAIL_AI_DEMO.RETAIL_OPS, implement the following governance controls:

1. Create a tag called SENSITIVITY_LEVEL with allowed values: 'PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED'.

2. Apply tags to these columns:
   - PRODUCTS.unit_cost -> CONFIDENTIAL
   - PRODUCTS.margin_pct -> CONFIDENTIAL
   - PURCHASE_ORDERS.unit_cost -> RESTRICTED
   - PURCHASE_ORDERS.total_cost -> RESTRICTED
   - SALES_TRANSACTIONS.discount_pct -> INTERNAL

3. Create a dynamic masking policy called MASK_COST_DATA (for STRING/TEXT values) that:
   - Shows full values for RETAIL_DATA_ENGINEER and FINANCE_ANALYST roles
   - Shows '***MASKED***' for all other roles

4. Create a masking policy called MASK_DOLLAR_VALUES (for NUMERIC values) that:
   - Shows full values for RETAIL_DATA_ENGINEER and FINANCE_ANALYST roles
   - Shows 0.00 for all other roles
   Apply MASK_DOLLAR_VALUES to PRODUCTS.unit_cost and PURCHASE_ORDERS.unit_cost.

Execute all SQL. Then demonstrate the masking by querying PRODUCTS as the current role and show the tag assignments."""

render_prompt("Prompt 3.2", "Data Masking and Tagging", PROMPT_3_2)

render_explanation("What this prompt does", """
This implements two critical governance features:

**Object Tagging** (`CREATE TAG`): Tags are key-value metadata attached to Snowflake objects. They're used for:
- Data classification (PII, confidential, public)
- Regulatory compliance tracking
- Automated policy enforcement via tag-based masking
- Data catalog enrichment

```sql
CREATE OR REPLACE TAG RETAIL_AI_DEMO.RETAIL_OPS.SENSITIVITY_LEVEL
  ALLOWED_VALUES 'PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED';

ALTER TABLE PRODUCTS MODIFY COLUMN unit_cost
  SET TAG SENSITIVITY_LEVEL = 'CONFIDENTIAL';
```

**Dynamic Data Masking** (`CREATE MASKING POLICY`): Masking policies use conditional logic based on `CURRENT_ROLE()` to decide what the user sees:

```sql
CREATE OR REPLACE MASKING POLICY MASK_DOLLAR_VALUES AS (val NUMBER)
  RETURNS NUMBER ->
    CASE
      WHEN CURRENT_ROLE() IN ('RETAIL_DATA_ENGINEER', 'FINANCE_ANALYST') THEN val
      ELSE 0.00
    END;
```

The policy is then attached to a column. **The underlying data is never changed** - masking happens at query time. This means the same query returns different results for different roles.

**Why cost data is sensitive in retail**: Unit cost and margin data reveal Alpine & Co.'s negotiated prices with suppliers. If a merchandiser sees that a Nike shoe costs $45 and retails for $120, that margin intelligence could leak to competitors or be used inappropriately in vendor negotiations. Only finance and engineering roles need this data.
""")


PROMPT_3_3 = """Run these governance verification queries in RETAIL_AI_DEMO.RETAIL_OPS:

1. Show all tag references on the RETAIL_OPS schema using INFORMATION_SCHEMA.TAG_REFERENCES for our SENSITIVITY_LEVEL tag
2. Show all masking policies applied using INFORMATION_SCHEMA.POLICY_REFERENCES
3. Query 5 rows from PRODUCTS to show which columns are masked for the current role

Show the results."""

render_prompt("Prompt 3.3", "Verify Governance", PROMPT_3_3)

render_explanation("What this prompt does", """
Verification queries using Snowflake's **INFORMATION_SCHEMA** governance views:

- **TAG_REFERENCES**: Shows every object and column that has a tag applied, along with the tag value. This is how you audit data classification across your account.

- **POLICY_REFERENCES**: Shows which masking (and row access) policies are attached to which columns. Critical for compliance auditing.

- **Querying masked data**: When you query `PRODUCTS` as `ACCOUNTADMIN`, you'll see the raw `unit_cost` values. If you `USE ROLE RETAIL_MERCHANDISER` first, the `unit_cost` column will show `0.00` because the masking policy blocks non-finance roles from seeing cost data.

These views are part of Snowflake's **Horizon** governance framework, which provides centralized visibility into data access, classification, and policy enforcement.
""")


render_key_concepts([
    {"term": "RBAC (Role-Based Access Control)", "definition": "Snowflake's security model where all access is mediated through roles. Users are granted roles, roles are granted privileges on objects, and roles can be granted to other roles (hierarchy). ACCOUNTADMIN is the top-level role."},
    {"term": "Dynamic Data Masking", "definition": "A column-level security feature that uses masking policies to conditionally replace column values at query time. The policy is a SQL function that receives the column value and returns either the real value or a masked version based on CURRENT_ROLE() or other context functions."},
    {"term": "Object Tagging", "definition": "Key-value metadata that can be applied to any Snowflake object (database, schema, table, column, warehouse, user, etc.). Tags enable classification, governance automation, and cost attribution. Tags propagate through lineage - a tag on a source column can be tracked to downstream objects."},
    {"term": "SNOWFLAKE.CORTEX_USER", "definition": "A database role that grants access to Snowflake Cortex AI functions. Without this role, users cannot call functions like COMPLETE(), SENTIMENT(), TRANSLATE(), or EMBED_TEXT(). It must be explicitly granted to user roles."},
])

render_domain_glossary([
    {"term": "Principle of Least Privilege", "definition": "A security best practice where users are granted only the minimum access required for their job function. RETAIL_MERCHANDISER can see inventory and sales data but not cost/margin data; FINANCE_ANALYST can see financial data but not customer complaints."},
    {"term": "Cost vs Retail Price", "definition": "Unit cost is what Alpine & Co. pays the supplier. Retail price is what the customer pays. The difference is gross margin. Cost data is among the most sensitive information in retail - it reveals negotiating power and competitive position."},
    {"term": "Margin Data", "definition": "Margin percentage = (retail_price - unit_cost) / retail_price x 100. Private-label products (Summit, Basecamp) typically achieve 55-65% margins vs. 30-45% for branded products. Margin data drives assortment planning, markdown decisions, and supplier negotiations."},
])

render_what_you_built([
    "4 custom roles: RETAIL_DATA_ENGINEER, RETAIL_DATA_SCIENTIST, RETAIL_MERCHANDISER, FINANCE_ANALYST",
    "SENSITIVITY_LEVEL tag with 4 classification levels (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED)",
    "5 tag assignments across sensitive cost and margin columns",
    "MASK_COST_DATA masking policy for text columns",
    "MASK_DOLLAR_VALUES masking policy for numeric cost columns",
])
