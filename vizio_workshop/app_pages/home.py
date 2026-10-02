import streamlit as st

st.title("VIZIO SmartCast Analytics Lab")
st.markdown("Hands-On Lab — Snowflake AI for Connected TV Analytics")
st.caption("2-hour edition — from raw data to conversational BI")

st.space("small")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Databases", "2", help="VIZIO source databases")
col2.metric("Sessions", "7", help="Hands-on lab sessions")
col3.metric("Prompts", "~21", help="Total Cortex Code prompts")
col4.metric("Duration", "~2 hrs", help="Total hands-on content time")

st.space("medium")

st.markdown("#### How this workshop works")

st.markdown("""
Each session has **numbered prompts** that you copy and paste directly into **Cortex Code** in Snowsight.
Cortex Code interprets your natural language instruction and executes the appropriate
SQL, Python, or configuration against your Snowflake account.

Each session also includes a **Fallback SQL** section — pre-written SQL you can run directly
in a worksheet if you're short on time or if Cortex Code generates something unexpected.

All prompts build on each other sequentially — run them in order.
""")

st.space("small")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
You are a **data analyst** on VIZIO's Platform Analytics team. Your job is to understand
how customers engage with SmartCast — the apps they use, the WatchFree+ content they watch,
how devices perform across models and firmware versions, and where the business is growing or at risk.

You have data across **2 source databases** covering streaming (WatchFree+) and the device/TV fleet. Your challenge: build a unified analytics layer and then
make it queryable in natural language through a Cortex Agent.

By the end of this lab, you'll have built analytics views, auto-refreshing dynamic tables,
AI-powered text analysis, and a conversational BI agent accessible via CoWork.
""")

st.space("small")

st.markdown("#### What we'll build")
with st.container(border=True):
    st.markdown("""
| Phase | What you'll do |
|-------|----------------|
| **1. Foundation** | Create 2 source databases with 11 tables + analytics workspace + text data |
| **2. Data Discovery** | Explore streaming and device databases with Cortex Code |
| **3. Analytics Views** | WFP engagement, device health scorecard, app performance |
| **4. Dynamic Tables** | Auto-refreshing churn signals and content trend tracker |
| **5. Cortex LLM Functions** | Sentiment, topic classification, feature extraction on customer feedback |
| **6. Semantic View + Search** | Natural language queries + knowledge base over policies |
| **7. Cortex Agent & CoWork** | Multi-tool agent for conversational BI |
""")

st.space("small")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- A Snowflake account (provided for this lab)
- **ACCOUNTADMIN** role
- **Cortex Code** open in Snowsight
- Cross-region inference enabled (covered in Getting Started)
""")
