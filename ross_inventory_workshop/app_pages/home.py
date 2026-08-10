import streamlit as st

st.title("Store Inventory Optimization")
st.markdown("A Hands-On Lab for Ross Stores Analysts — Powered by Snowflake")
st.caption("3-hour edition — from raw data to conversational BI")

st.space("small")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Participants", "30", help="Ross Stores analysts")
col2.metric("Sessions", "8", help="Hands-on lab sessions")
col3.metric("Prompts", "~26", help="Total Cortex Code prompts")
col4.metric("Duration", "~3 hrs", help="Total hands-on content time")

st.space("medium")

st.markdown("#### How this workshop works")

st.markdown("""
Each session has **numbered prompts** that you copy and paste directly into **Cortex Code** in Snowsight.
Cortex Code interprets your natural language instruction and executes the appropriate
SQL, Python, or configuration against your Snowflake account.

All prompts build on each other sequentially — run them in order.
""")

st.space("small")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
You are an **inventory analyst** at Ross Stores responsible for optimizing store-level
inventory. Your challenge: **reduce stockouts while minimizing overstock** across a network
of stores with varying demand patterns, seasonal peaks, and different product categories.

You have raw data — sales transactions, inventory snapshots, purchase orders, product catalogs,
store locations, a calendar with seasonality flags, and employee assignments. Your job is to
turn this into actionable intelligence using Snowflake's native capabilities.

By the end of this lab, you'll have built a complete inventory optimization platform:
from analytics-ready datasets to a conversational AI agent that can answer questions about
your inventory in natural language.
""")

st.space("small")

st.markdown("#### What we'll build")
with st.container(border=True):
    st.markdown("""
| Phase | What you'll do |
|-------|----------------|
| **1. Data Foundation** | Create the database, warehouse, and 9 realistic data tables |
| **2. Data Discovery** | Use Cortex Code to explore and understand the data |
| **3. Analytics Views** | Build business-logic views (inventory health, sales w/ seasonality, store KPIs) |
| **4. Dynamic Tables** | Auto-refreshing replenishment signals and stockout risk scores |
| **5. Streamlit App** | What-if scenario planner with save-to-Snowflake capability |
| **6. Semantic View** | Business-aware metadata for natural language queries |
| **7. Cortex Search** | Knowledge base over inventory policies and procedures |
| **8. Cortex Agent** | Multi-tool AI agent for CoWork conversational BI |
| **9. Try It Yourself** | Extend the Streamlit app with regional and store reports |
""")

st.space("small")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- A Snowflake account (provided for this lab)
- **ACCOUNTADMIN** role (or a role with sufficient privileges)
- **Cortex Code** open in Snowsight
- Cross-region inference enabled (covered in Getting Started)
""")
