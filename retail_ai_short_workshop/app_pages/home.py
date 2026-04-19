import streamlit as st

st.title("Retail AI Workshop")
st.markdown("Building an AI-Powered Platform for a National Apparel & Footwear Retailer with Snowflake")
st.caption("90-minute edition — setup + Cortex AI features")

st.space("small")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Annual revenue", "$2B+", help="Annual retail revenue across all channels")
col2.metric("Sessions", "7", help="Hands-on lab sessions")
col3.metric("Prompts", "~20", help="Total Cortex Code prompts")
col4.metric("Duration", "~90 min", help="Total hands-on content time")

st.space("medium")

st.markdown("#### How this workshop works")

st.markdown("""
Each session has **numbered prompts** that you copy and paste directly into **Cortex Code**.
Cortex Code interprets your natural language instruction and executes the appropriate
SQL, Python, or configuration against your Snowflake account.

All prompts build on each other sequentially — run them in order.
""")

st.space("small")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
**Alpine & Co.** is a national apparel and footwear retailer operating **120+ stores** across
the United States with a growing e-commerce presence. The company generates over **$2 billion
in annual revenue** and manages a catalog of **5,000+ SKUs** spanning branded products
(Nike, Adidas, Levi's, The North Face) and two private-label lines (Summit activewear,
Basecamp casual basics).

In this workshop, you'll build an AI-powered analytics platform for Alpine & Co. using
Snowflake's native AI capabilities — all from natural language prompts in Cortex Code.
""")

st.space("small")

st.markdown("#### What we'll cover")
with st.container(border=True):
    st.markdown("""
This 90-minute workshop focuses on **data setup and Cortex AI features**:

1. **Foundation & Data** — Create the database, warehouse, and 15 realistic data tables
2. **Cortex LLM Functions** — Sentiment analysis, translation, summarization, and model comparison
3. **Cortex Search & RAG** — Build a search service and a retrieval-augmented generation pipeline
4. **Semantic Views & Cortex Analyst** — Natural language to SQL with business-aware metadata
5. **Cortex Agents** — An orchestrating AI that combines structured data, search, and custom tools
""")

st.space("small")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- A Snowflake account (free trial works — see **Getting Started**)
- **ACCOUNTADMIN** role (default on trial accounts)
- **Cortex Code** open in Snowsight
- Cross-region inference enabled (covered in Getting Started)
""")
