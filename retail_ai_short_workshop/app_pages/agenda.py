import streamlit as st

st.title("Agenda")
st.markdown("90-minute workshop schedule")

st.space("small")

schedule = [
    ("", "Getting Started", "5 min", "Account setup, Cortex Code, cross-region inference"),
    ("Session 1", "Foundation & Reference Data", "10 min", "Database, schema, warehouse, 3 reference tables"),
    ("Session 2", "Data Prep & Features", "15 min", "12 operational tables: structured, time-series, unstructured text"),
    ("Session 3", "Cortex LLM Functions", "15 min", "Sentiment, translation, summarization, model comparison, classification"),
    ("Session 4", "Cortex Search & RAG", "15 min", "Knowledge base, Cortex Search service, RAG query pattern"),
    ("Session 5", "Semantic Views & Analyst", "15 min", "Semantic view, natural language to SQL, AI-assisted expansion"),
    ("Session 6", "Cortex Agents", "15 min", "Agent with Analyst + Search + custom tool orchestration"),
    ("Session 7", "Free-form Exploration", "~remaining", "Open-ended experimentation with everything you've built"),
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

st.markdown("#### What you'll build")

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
| Object type | Count |
|-------------|-------|
| Tables | ~15 |
| Cortex Search service | 1 |
| Semantic view | 1 |
| Cortex Agent | 1 |
| Custom UDF | 1 |
""")
    with col2:
        st.markdown("""
| AI capability | Sessions |
|---------------|----------|
| Sentiment / Summarize / Translate | 3 |
| LLM model comparison | 3 |
| Zero-shot classification | 3 |
| Hybrid search + RAG | 4 |
| Text-to-SQL (Analyst) | 5 |
| Multi-tool orchestration | 6 |
""")
