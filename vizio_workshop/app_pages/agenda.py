import streamlit as st

st.title("Agenda")
st.markdown("2-hour hands-on lab schedule")

st.space("small")

schedule = [
    ("", "Getting Started", "5 min", "Account access, Cortex Code, cross-region inference"),
    ("Session 1", "Foundation & Data Setup", "15 min", "2 source databases, 11 tables, analytics workspace, customer feedback"),
    ("Session 2", "Data Discovery", "15 min", "Explore data with Cortex Code — profiling, relationships, patterns"),
    ("Session 3", "Analytics-Ready Views", "20 min", "WFP engagement, device health scorecard, app performance summary"),
    ("Session 4", "Dynamic Tables", "20 min", "Auto-refreshing churn signals and content trend tracker"),
    ("Session 5", "Cortex AI Functions", "20 min", "AI_SENTIMENT, AI_CLASSIFY, AI_EXTRACT on customer feedback"),
    ("Session 6", "Semantic View & Search", "20 min", "Natural language to SQL + knowledge base over policies"),
    ("Session 7", "Cortex Agent & CoWork", "15 min", "Multi-tool agent for conversational BI in Snowsight"),
]

st.markdown("#### Schedule")

for session, title, duration, description in schedule:
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 2, 4])
        with col1:
            st.markdown(f"**{session}**" if session else ":material/rocket_launch:")
        with col2:
            st.markdown(f"**{title}** ({duration})")
        with col3:
            st.caption(description)

st.space("small")

st.markdown("#### Source databases")

with st.container(border=True):
    st.markdown("""
| Database | Schema(s) | Focus |
|----------|-----------|-------|
| VIZIO_STREAMING | WFP | WatchFree+ live channels, AVOD content, global KPIs, revenue |
| VIZIO_DEVICES | FLEET, ENGAGEMENT, APPS, OEM | TV fleet attributes, homescreen, app launches, OEM |
""")

st.space("small")

st.markdown("#### What you'll build on top")

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
| Object type | Count |
|-------------|-------|
| Analytics database | 1 |
| Analytics views | 3 |
| Dynamic tables | 2 |
| Customer feedback table | 1 |
| Policy knowledge base | 1 |
| Semantic view | 1 |
| Cortex Search service | 1 |
| Cortex Agent | 1 |
| Custom UDF | 1 |
""")
    with col2:
        st.markdown("""
| Snowflake capability | Session |
|---------------------|---------|
| Cortex Code for discovery | 2 |
| Views with business logic | 3 |
| Dynamic Tables (auto-refresh) | 4 |
| Cortex AI Functions | 5 |
| Semantic View + Cortex Analyst | 6 |
| Cortex Search (hybrid) | 6 |
| Cortex Agent + CoWork | 7 |
""")
