import streamlit as st

st.title("Retail AI Workshop")
st.markdown("Building an AI-Powered Platform for a National Apparel & Footwear Retailer with Snowflake")

st.space("small")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Annual revenue", "$2B+", help="Annual retail revenue across all channels")
col2.metric("Sessions", "14", help="Hands-on lab sessions")
col3.metric("Prompts", "~40", help="Total Cortex Code prompts")
col4.metric("Duration", "~6 hrs", help="Total hands-on content time")

st.space("medium")

st.markdown("#### How this workshop works")

st.markdown("""
Each session has **numbered prompts** that you copy and paste directly into **Cortex Code**.
Cortex Code interprets your natural language instruction and executes the appropriate
SQL, Python, or configuration against your Snowflake account.

All prompts build on each other sequentially — run them in order throughout the day.
""")

st.space("small")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
**Alpine & Co.** is a national apparel and footwear retailer operating **120+ stores** across
the United States and a fast-growing e-commerce channel. The company sells a curated mix of
branded and private-label clothing, shoes, and accessories — from casual everyday wear to
performance athletic gear.

We'll build a complete AI platform covering:

| Data type | Examples |
|-----------|---------|
| **Structured** | Sales transactions, inventory levels, purchase orders, customer profiles, product catalog |
| **Unstructured** | Customer reviews, support tickets, supplier contracts, marketing campaign briefs |
| **Time series** | Hourly foot traffic, daily sales by store, inventory snapshots, website clickstream |
| **Geospatial** | Store locations, distribution center coordinates, delivery zone mapping |
""")

st.space("small")

st.markdown("#### Scenario deep dive")

st.markdown("""
Alpine & Co. operates across three channels: **brick-and-mortar stores** (flagship, mall, and outlet formats), **e-commerce** (web and mobile app), and **wholesale** partnerships with department stores. The product catalog spans 5,000+ SKUs across apparel categories (tops, bottoms, outerwear, activewear) and footwear (sneakers, boots, sandals, dress shoes). Private-label brands — *Summit* for activewear and *Basecamp* for casual basics — generate the highest margins.
""")

with st.container(border=True):
    st.markdown("##### The operational challenge")
    st.markdown("""
On any given day, the merchandising and operations teams must coordinate:

- **120+ stores** with varying foot traffic patterns, regional preferences, and seasonal demand cycles
- **5,000+ SKUs** across sizes, colors, and categories — each with different lead times, markdown schedules, and reorder points
- **Omnichannel fulfillment**: buy-online-pickup-in-store (BOPIS), ship-from-store, and warehouse direct
- **Supplier management** across 80+ domestic and international vendors with varying reliability
- **Customer engagement** through loyalty programs, targeted promotions, and personalized recommendations

When inventory is misallocated — too many winter coats in Phoenix, not enough running shoes in Portland — the ripple effects cascade: markdowns erode margin, stockouts lose sales, and excess inventory ties up working capital. A single missed trend during back-to-school season can cost **$5-10 million** in lost revenue and forced markdowns.
""")

with st.container(border=True):
    st.markdown("##### What we're building and why")
    st.markdown("""
Throughout this workshop, we build a complete AI-powered retail operations platform that addresses real challenges faced by merchandisers, store managers, and e-commerce teams:

**Predicting stockouts before they happen** (Sessions 4-5)
We train ML models to predict which SKU-store combinations will run out of stock within the next 7 days, using features like current inventory levels, trailing sales velocity, seasonality, and promotion schedules. The best model is registered in Snowflake's Model Registry and deployed as a SQL function. A Dynamic Table continuously re-scores as new sales data arrives, giving the supply chain team a live stockout risk feed.

**Understanding customer sentiment and product feedback** (Sessions 6-9)
Retailers generate enormous volumes of unstructured data: product reviews, support chat transcripts, supplier contract terms, and marketing briefs. We use Cortex LLM functions to analyze review sentiment, extract product defect themes from support tickets, build a searchable knowledge base over customer feedback, and create vector embeddings for semantic product search. This transforms scattered feedback into actionable product intelligence.

**Natural language access to retail data** (Sessions 10-11)
Store managers and buyers shouldn't need SQL to answer questions like "What were the top-selling sneakers last weekend?" or "Which stores have excess winter inventory?" We build a Semantic View over eight operational tables and connect it to Cortex Analyst for text-to-SQL. Then we build a Cortex Agent that combines structured sales queries with customer feedback search — a single assistant that can answer both "What is our sell-through rate on Summit activewear?" and "What are customers saying about the new Basecamp hoodie quality?"

**A retail dashboard accessible to everyone** (Session 12)
We deploy a Streamlit app inside Snowflake with live KPIs, store performance maps, a chat interface powered by Cortex, and a customer feedback tracker. Because it runs on Snowflake's container runtime, it inherits all the security policies we set up earlier — masking sensitive cost data, restricting access by role — without any additional configuration.

**Governance and security from day one** (Session 3)
Before building any AI, we establish RBAC roles (RETAIL_MERCHANDISER, RETAIL_ANALYST, STORE_MANAGER, FINANCE_ANALYST) with appropriate privilege hierarchies, column-level masking on sensitive cost and margin data, and tagging policies. Every model, dashboard, and agent respects these boundaries automatically.
""")

with st.container(border=True):
    st.markdown("##### Why this scenario matters")
    st.markdown("""
This isn't just a demo — it models a real pattern that applies across industries:

- **Multi-source data integration**: Structured transactions, product reviews, time-series sensors, and store coordinates — all in one platform
- **ML that operations teams can actually use**: Models registered as SQL functions, not locked inside data science notebooks
- **AI assistants grounded in your data**: Agents that combine structured queries with document search, not generic chatbots
- **Security that scales**: Governance policies set once and enforced everywhere — in dashboards, agents, and ad-hoc queries
- **Zero infrastructure management**: Feature stores, model registries, search services, and apps all running inside Snowflake with no external services to maintain

The retail scenario makes these patterns tangible: every table, model, and agent maps to a real operational need. By the end of the day, you'll have built the same architecture that applies to healthcare operations, financial services, manufacturing, logistics, or any domain with complex, multi-modal data.
""")

st.space("small")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- Snowflake account with **ACCOUNTADMIN** role — see **Getting Started** in the sidebar to provision a free trial
- **Cortex Code** open in Snowsight and connected to your account
- Cross-region inference enabled (for Cortex LLM functions)
""")

st.space("medium")
st.caption("Built for the Retail AI Workshop  :material/location_on:  Snowflake")
