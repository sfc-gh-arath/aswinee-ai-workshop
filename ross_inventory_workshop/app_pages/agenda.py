import streamlit as st

st.title("Agenda")
st.markdown("3-hour hands-on lab schedule")

st.space("small")

schedule = [
    ("", "Getting Started", "10 min", "Account access, Cortex Code, cross-region inference"),
    ("Session 1", "Foundation & Data Setup", "20 min", "Database, schemas, warehouse, 9 raw data tables"),
    ("Session 2", "Data Discovery", "20 min", "Explore data with Cortex Code — profiling, relationships, quality"),
    ("Session 3", "Analytics-Ready Views", "25 min", "Inventory health, seasonal sales, store performance views"),
    ("Session 4", "Dynamic Tables", "25 min", "Auto-refreshing replenishment signals and stockout risk scores"),
    ("", "Break", "10 min", "Stretch, grab a coffee"),
    ("Session 5", "Streamlit What-If App", "30 min", "Interactive scenario planner with save-to-Snowflake"),
    ("Session 6", "Semantic View & Analyst", "25 min", "Natural language to SQL with business-aware metadata"),
    ("Session 7", "Cortex Search", "20 min", "Knowledge base and hybrid search over inventory policies"),
    ("Session 8", "Cortex Agent & CoWork", "25 min", "Multi-tool agent for conversational BI in Snowsight"),
    ("Session 9", "Try It Yourself", "~remaining", "Extend the Streamlit app with regional/store reports"),
]

st.markdown("#### Schedule")

for session, title, duration, description in schedule:
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 2, 4])
        with col1:
            if session:
                st.markdown(f"**{session}**")
            elif title == "Break":
                st.markdown(":material/coffee:")
            else:
                st.markdown(":material/rocket_launch:")
        with col2:
            st.markdown(f"**{title}** ({duration})")
        with col3:
            st.caption(description)

st.space("small")

st.markdown("#### What you'll build")

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
| Object type | Count |
|-------------|-------|
| Database & Schemas | 1 + 3 |
| Raw data tables | 9 |
| Analytics views | 3 |
| Dynamic tables | 2 |
| Streamlit app | 1 |
| Semantic view | 1 |
| Cortex Search service | 1 |
| Cortex Agent | 1 |
| Custom UDF | 1 |
| Saved scenarios table | 1 |
""")
    with col2:
        st.markdown("""
| Snowflake capability | Session |
|---------------------|---------|
| Cortex Code for discovery | 2 |
| Views with business logic | 3 |
| Dynamic Tables (auto-refresh) | 4 |
| Streamlit in Snowflake | 5 |
| Semantic View + Cortex Analyst | 6 |
| Cortex Search (hybrid) | 7 |
| Cortex Agent + CoWork | 8 |
""")
