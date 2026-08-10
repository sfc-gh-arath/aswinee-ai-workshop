import streamlit as st
from components import (
    render_session_header,
    render_prompt,
    render_explanation,
    render_technologies_used,
    render_what_you_built,
)

render_session_header(
    session_num=9,
    title="Try It Yourself",
    time_range="Remaining time",
    duration="Open-ended",
    building="Extend the Streamlit app with regional and store-level reports",
)

render_technologies_used([
    {"name": "Streamlit Enhancements", "description": "Add new tabs, charts, and aggregations to your existing app. Practice the get_active_session() + session.sql() pattern on your own.", "icon": "extension"},
    {"name": "Self-Directed Learning", "description": "Apply what you learned in Sessions 1-8 to build something new without step-by-step prompts. Use Cortex Code to help generate the code.", "icon": "school"},
    {"name": "Regional Analytics", "description": "Aggregate inventory and sales data by region and store to produce executive-ready summary reports inside your Streamlit app.", "icon": "map"},
])

st.markdown("---")
st.markdown("#### Challenge: Add Regional & Store Reports to Your App")

with st.container(border=True):
    st.markdown("""
Now that you've built the What-If Planner with a Batch Analysis tab, try adding a
**third tab** with overall inventory reports broken down by **region** and **store**.

Here's what to aim for:

**Tab 3: "Reports"**

1. **Region Summary** — A table showing for each region:
   - Number of stores
   - Total items at CRITICAL/HIGH stockout risk
   - Average days of supply
   - Total estimated lost revenue from stockouts
   - Fill rate average

2. **Store Drilldown** — A selectbox to pick a region, then show a per-store breakdown:
   - Store name, city, state
   - Items needing reorder (from DT_REPLENISHMENT_SIGNALS)
   - Total EMERGENCY + URGENT items
   - Revenue per sqft (from STORE_PERFORMANCE_SUMMARY)

3. **Visualizations**:
   - Bar chart: stockout risk items by region
   - Bar chart: lost revenue by category for the selected region

This is open-ended — use your judgment on layout and exactly which metrics to include.
""")

st.space("small")

st.markdown("#### Example prompt to get started")

with st.container(border=True):
    st.code("""Add a third tab called "Reports" to my INVENTORY_WHATIF_PLANNER app. This tab should show:

1. A region-level summary table with columns: region, num_stores, critical_risk_items, avg_days_of_supply, total_lost_revenue, avg_fill_rate. Query from ROSS_INVENTORY_LAB.ANALYTICS.DT_STOCKOUT_RISK_SCORE joined with ROSS_INVENTORY_LAB.ANALYTICS.STORE_PERFORMANCE_SUMMARY.

2. Below that, a selectbox to pick a region, and then a store-level detail table filtered to that region showing: store_name, city, emergency_items, urgent_items, avg_days_of_supply, revenue_per_sqft. Query from DT_REPLENISHMENT_SIGNALS grouped by store.

3. Two bar charts side by side:
   - Left: count of CRITICAL + HIGH risk items by region (all regions)
   - Right: total estimated lost revenue by product category for the selected region

REMEMBER: Use session = get_active_session() and session.sql().to_pandas() for all data. Use fully qualified table names. Generate the complete updated app code.""", language="text", wrap_lines=True)

st.space("small")

st.markdown("#### Other ideas to explore")

with st.container(border=True):
    st.markdown("""
If you finish the reports tab early, here are more things to try:

- **Ask the Agent** (from Session 8): "Which regions need the most attention this week?" and compare its answer to your Reports tab
- **Add a trend chart**: Show how fill rate has changed over the past 12 weeks per region
- **Add an alert summary**: Show all EMERGENCY items that have been in stockout for more than 7 days
- **Export to PDF**: Use st.download_button with a formatted string to create a simple text report
- **Enhance the What-If tab**: Add a comparison mode where you can simulate the same scenario across multiple stores at once
- **Ask Cortex Code**: "What other visualizations would be useful for an inventory analyst looking at this data?"
""")

st.space("small")

st.markdown("#### Tips")

with st.container(border=True):
    st.markdown("""
- Use **Cortex Code** to generate the code — describe what you want in plain English
- Remember to use **`session = get_active_session()`** and **`session.sql()`** (not st.connection)
- Use **fully qualified table names** (e.g., `ROSS_INVENTORY_LAB.ANALYTICS.DT_STOCKOUT_RISK_SCORE`)
- If you get errors, paste the error back into Cortex Code and ask it to fix the issue
- Paste the updated code into the **Workspace editor** and click Run to see changes instantly
""")

render_what_you_built([
    "Extended the Streamlit app with regional and store-level inventory reports",
    "Practiced self-directed development using Cortex Code for code generation",
    "Built executive-ready visualizations from the analytics layer created earlier",
])
