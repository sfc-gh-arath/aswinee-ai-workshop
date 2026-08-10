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
    title="Streamlit What-If App",
    time_range="1:50 - 2:20",
    duration="30 min",
    building="Interactive inventory scenario planner deployed from Workspace",
)

render_technologies_used([
    {"name": "Streamlit in Snowflake", "description": "Build and deploy interactive Python apps directly in Snowsight. Apps run on your warehouse using get_active_session() for data access. No external network needed.", "icon": "dashboard"},
    {"name": "Snowflake Workspace", "description": "The built-in IDE in Snowsight where you write and edit Streamlit app code. Files are saved to a stage and deployed to run on a warehouse.", "icon": "code"},
    {"name": "get_active_session()", "description": "The function from snowflake.snowpark.context that provides the current Snowpark session inside a Streamlit app running on a warehouse. Use session.sql() to query data.", "icon": "link"},
])

st.markdown("---")
st.markdown("#### :material/info: Important: Streamlit App Deployment")
with st.container(border=True):
    st.markdown("""
**Trial accounts do not support running Streamlit apps on containers.** After Cortex Code
creates and deploys the app (which defaults to container mode), you must switch it to **Run on Warehouse**.

**Deployment flow (do this every time Cortex Code deploys the app):**
1. Cortex Code will create the Streamlit app in your Workspace and deploy it
2. **Open the app** in Snowsight (Projects → Streamlit → click the app name)
3. You'll see an error or the app won't load (because container mode isn't available on trial)
4. Click the **⋮ (three dots menu)** in the top-right of the app → **App Settings**
5. Under **Run on**, change from **Container** to **Warehouse**
6. Select warehouse: **INVENTORY_LAB_WH**
7. Click **Save** — the app will reload and work correctly

**You must repeat step 4-7 every time the app is redeployed by Cortex Code.**

**Code requirements for warehouse mode:**
- Use **`get_active_session()`** from `snowflake.snowpark.context` (NOT `st.connection()`)
- All queries use **`session.sql("...")`** to execute SQL
- `st.connection('snowflake')` requires external access which trial accounts don't have
""")


PROMPT_5_1 = """Create a table ROSS_INVENTORY_LAB.APPS.SAVED_SCENARIOS to store what-if analysis results. Columns:

- scenario_id (NUMBER AUTOINCREMENT)
- created_at (TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP())
- created_by (VARCHAR DEFAULT CURRENT_USER())
- store_id (NUMBER)
- product_id (NUMBER)
- scenario_name (VARCHAR)
- current_reorder_point (NUMBER)
- new_reorder_point (NUMBER)
- current_safety_stock_days (NUMBER)
- new_safety_stock_days (NUMBER)
- lead_time_override_days (NUMBER)
- seasonal_demand_factor (FLOAT — multiplier like 1.5 for 50% increase)
- projected_dos_current (FLOAT)
- projected_dos_new (FLOAT)
- projected_stockout_prob_current (FLOAT)
- projected_stockout_prob_new (FLOAT)
- projected_annual_carrying_cost_current (FLOAT)
- projected_annual_carrying_cost_new (FLOAT)
- notes (VARCHAR)

Execute the CREATE TABLE."""

render_prompt("Prompt 5.1", "Create Saved Scenarios Table", PROMPT_5_1)

render_explanation("What this prompt does", """
Creates the **persistence layer** for the Streamlit app. When users run what-if scenarios,
they can save the results to this table for:

- **Audit trail**: Who ran what scenario, when?
- **Collaboration**: Share scenario results with buyers and planners
- **Decision support**: Compare multiple scenarios side-by-side later
- **Implementation**: Approved scenarios become actual parameter changes

**AUTOINCREMENT** handles ID generation. **DEFAULT CURRENT_TIMESTAMP()** and **DEFAULT CURRENT_USER()** automatically capture who saved and when, without the app needing to pass these explicitly.
""")


PROMPT_5_2 = """Create a Streamlit in Snowflake app called INVENTORY_WHATIF_PLANNER in database ROSS_INVENTORY_LAB, schema APPS, using warehouse INVENTORY_LAB_WH.

This app will run on a WAREHOUSE (not container) so it MUST use get_active_session() for data access.

IMPORTANT REQUIREMENTS:
- Import: from snowflake.snowpark.context import get_active_session
- Get session: session = get_active_session()
- All data access via: session.sql("SELECT ...").to_pandas()
- Write data via: session.sql("INSERT INTO ...")
- Do NOT use st.connection('snowflake') — that requires external access which trial accounts don't have

The app layout:

TITLE: "Inventory What-If Planner"
SUBTITLE: "Simulate reorder policy changes and compare projected outcomes"

SIDEBAR:
- Store selector (dropdown from ROSS_INVENTORY_LAB.RAW.STORES table - show store_name)
- Product category filter (multiselect from distinct categories in ROSS_INVENTORY_LAB.RAW.PRODUCTS)
- Product selector (dropdown filtered by category, from PRODUCTS - show product_name)

MAIN AREA:

Section 1: "Current State" (read-only metrics)
- Show current on_hand_qty, avg_daily_demand (last 28 days from DAILY_SALES), current days_of_supply, reorder_point, lead_time_days for the selected store/product
- Display as st.metric cards in a row

Section 2: "Scenario Parameters" (interactive)
- Slider: New Reorder Point (range: 0 to 500, default = current reorder_point)
- Slider: Safety Stock Days (range: 0 to 30, default = 14)
- Number input: Lead Time Override (default = current lead_time_days)
- Slider: Seasonal Demand Factor (range: 0.5 to 3.0, step 0.1, default = 1.0)
- Text input: Scenario Name

Section 3: "Projected Comparison" (calculated)
Show a two-column comparison (Current vs Proposed):
- Projected Days of Supply
- Estimated Stockout Probability (simple model: if DOS < lead_time then high, etc.)
- Annual Carrying Cost estimate (on_hand * unit_cost * 0.25 holding cost rate)
- Suggested Order Quantity (using new parameters)

Section 4: "8-Week Projection Chart"
- Line chart showing projected inventory levels over the next 8 weeks under BOTH current and proposed policies
- X-axis: weeks, Y-axis: projected on-hand quantity
- Two lines: "Current Policy" and "Proposed Policy"
- Apply the seasonal demand factor to the demand forecast

Section 5: "Save Scenario"
- Button: "Save to Snowflake"
- On click: INSERT into ROSS_INVENTORY_LAB.APPS.SAVED_SCENARIOS with all current parameters and projected values using session.sql()
- Show st.success("Scenario saved!") on success
- Below the button: show a table of previously saved scenarios for this store/product

Create and deploy the app. After deployment, I will open the app and switch it from Container to Warehouse mode in App Settings."""

render_prompt("Prompt 5.2", "Generate the Streamlit App Code", PROMPT_5_2)

render_explanation("What this prompt does", """
Cortex Code will create and deploy the Streamlit app directly in your Workspace.

**After Cortex Code deploys the app**:
1. Open the app in Snowsight (Projects → Streamlit → INVENTORY_WHATIF_PLANNER)
2. It will fail to load (default is container mode, which trial accounts don't support)
3. Click **⋮ menu → App Settings → Run on: Warehouse → Save**
4. The app reloads and works

**Key pattern — get_active_session()**:
```python
from snowflake.snowpark.context import get_active_session
session = get_active_session()

# Query data
df = session.sql("SELECT * FROM ROSS_INVENTORY_LAB.RAW.STORES").to_pandas()

# Write data
session.sql(f"INSERT INTO ... VALUES (...)").collect()
```

**Why NOT st.connection('snowflake')**:
- `st.connection()` requires external access integration
- Trial accounts don't have this enabled
- `get_active_session()` works natively when running on warehouse
""")


PROMPT_5_3 = """The app was deployed but it's running on container mode by default. Walk me through switching it to warehouse mode:

1. How do I find and open the app in Snowsight?
2. How do I change the Run on setting from Container to Warehouse?
3. After switching, verify the app loads correctly

Also show me the key SQL queries the app uses so I understand what's happening:
- Fetch the current state for a given store_id and product_id
- Calculate the 8-week projection
- INSERT a saved scenario

If the app shows errors about packages, explain how to add packages in the Workspace editor (Packages panel on the left)."""

render_prompt("Prompt 5.3", "Switch to Warehouse Mode & Test", PROMPT_5_3)

render_explanation("What this prompt does", """
Guides you through switching the app from container to warehouse mode:

**Steps to switch**:
1. In Snowsight → **Projects → Streamlit** → click **INVENTORY_WHATIF_PLANNER**
2. Click the **⋮ (three dots)** menu in the top-right corner
3. Select **App Settings**
4. Under **Run on**, change from **Container** to **Warehouse**
5. Select **INVENTORY_LAB_WH** as the warehouse
6. Click **Save**

**You must do this every time the app is redeployed** (e.g., after Prompt 5.4 when we enhance it).

**Adding packages**: If the app fails due to missing imports (pandas, numpy), open the app in Workspace mode (Edit button), find the Packages panel on the left sidebar, and add them.

**SQL transparency**: Shows the actual queries so you understand the logic and can debug issues independently.
""")


PROMPT_5_4 = """Enhance the INVENTORY_WHATIF_PLANNER app code with a second tab. Use st.tabs to organize the app:

Tab 1: "What-If Simulator" (existing functionality)

Tab 2: "Inventory Health Overview" — a store-level dashboard that shows:

TOP SECTION: Summary metrics across all stores
- Total products at CRITICAL risk (on_hand_qty = 0)
- Total products at HIGH risk (days_of_supply < 3)
- Total estimated lost revenue (from ROSS_INVENTORY_LAB.RAW.STOCKOUT_EVENTS where stockout_end_date IS NULL — active stockouts)
- Average days of supply across all inventory

MIDDLE SECTION: Store selector
- A selectbox to pick a store (from STORES table)
- Once selected, show a table of all products at that store from ROSS_INVENTORY_LAB.ANALYTICS.INVENTORY_HEALTH where stockout_risk IN ('CRITICAL', 'HIGH', 'MEDIUM')
- Columns: product_name, category, brand, on_hand_qty, days_of_supply, stockout_risk, reorder_needed
- Color-code the stockout_risk column using conditional formatting (st.dataframe with column_config or highlight logic)
- Sort by days_of_supply ascending (most urgent first)

BOTTOM SECTION: Visualizations
- Bar chart: count of products in each stockout_risk level for the selected store
- Add a "Download Store Report" button (st.download_button) that exports the filtered table as CSV

REMEMBER: Use session = get_active_session() and session.sql() for all data access. Use fully qualified table names.

Update the app and deploy it. After deployment, I will switch it back to Warehouse mode in App Settings."""

render_prompt("Prompt 5.4", "Add Inventory Health Overview Tab", PROMPT_5_4)

render_explanation("What this prompt does", """
Extends the app with a **store-level inventory health dashboard**:

**Tab 1 (What-If Simulator)**: Single item analysis with scenario simulation — already built
**Tab 2 (Inventory Health Overview)**: See at a glance which products need attention

**Why this is better than querying the dynamic table directly**:
- Uses the **INVENTORY_HEALTH view** from Session 3 — guaranteed to have data with CRITICAL/HIGH classifications
- Uses **STOCKOUT_EVENTS with NULL end_date** — the active stockouts we specifically built into the sample data
- No dependency on dynamic table refresh timing

**New Streamlit features**:
- **st.tabs**: Organizes the app into focused views
- **st.dataframe with column_config**: Conditional formatting on risk levels
- **st.download_button**: Export filtered data for offline sharing
- **st.bar_chart**: Visual distribution of risk levels

**Deployment note**: After Cortex Code redeploys the updated app, remember to switch it back to **Warehouse** mode in App Settings (⋮ → App Settings → Run on: Warehouse → Save). You must do this after every redeployment.
""")


render_key_concepts([
    {"term": "Streamlit in Snowflake (Warehouse mode)", "definition": "Apps run directly on your virtual warehouse. Use get_active_session() for data access. Cortex Code deploys apps in container mode by default — you must switch to Warehouse via App Settings after each deployment on trial accounts."},
    {"term": "get_active_session()", "definition": "From snowflake.snowpark.context — provides the current Snowpark session inside a Streamlit app. Use session.sql() to run queries and session.sql().to_pandas() to get DataFrames. This is the standard pattern for warehouse-mode Streamlit apps."},
    {"term": "Workspace", "definition": "The built-in code editor in Snowsight for Streamlit apps. Cortex Code creates and deploys apps here. You can also edit code directly by clicking Edit on any deployed app. Code is saved to a Snowflake stage."},
    {"term": "Write-back Pattern", "definition": "An app that both reads AND writes Snowflake data via session.sql(). The What-If Planner reads inventory state and writes saved scenarios. Turns passive dashboards into active tools."},
])

render_domain_glossary([
    {"term": "Carrying Cost (Holding Cost)", "definition": "The cost of holding inventory over time. Typically 20-30% of item cost per year, covering storage, insurance, obsolescence risk, and opportunity cost of capital. A $10 item costs ~$2.50/year to hold in inventory."},
    {"term": "Service Level vs Cost Trade-off", "definition": "Higher reorder points mean fewer stockouts (better service) but more inventory (higher cost). The what-if simulator helps find the sweet spot where increasing stock no longer meaningfully reduces stockout risk."},
])

render_what_you_built([
    "SAVED_SCENARIOS table for persisting what-if analysis results",
    "INVENTORY_WHATIF_PLANNER Streamlit app code (generated via Cortex Code)",
    "Deployed app in Workspace running on warehouse with get_active_session()",
    "8-week projection chart comparing current vs. proposed policies",
    "Save-to-Snowflake capability for audit trail and collaboration",
    "Inventory Health Overview tab showing CRITICAL/HIGH risk products per store with export",
])
