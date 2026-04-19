import streamlit as st
from components import render_session_header, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(7, "Free-form Exploration", "remaining time", "~remaining", "Open-ended experimentation with everything you've built")

render_technologies_used([
    {"name": "Cortex Code", "description": "Use natural language prompts to explore, extend, and experiment with all the objects you've built. This is your sandbox time.", "icon": "code"},
    {"name": "Everything You Built", "description": "Tables, search services, semantic views, agents, and LLM functions — all available to combine in new ways.", "icon": "construction"},
    {"name": "Your Own Questions", "description": "No scripts, no prompts to copy. Ask Cortex Code whatever you're curious about and see what it can do with your data.", "icon": "explore"},
])

st.markdown("#### This session is unstructured")

st.markdown("""
You've built a complete AI platform for Alpine & Co. over the past 6 sessions. Now it's your turn to explore freely.
Use Cortex Code to ask your own questions, extend what you've built, or try things that caught your attention earlier.
""")

st.markdown("#### Ideas to try")

with st.container(border=True):
    st.markdown("""
**Push the AI further**
- Ask the Cortex Agent complex multi-step questions that require both structured sales data and customer feedback
- Try breaking the semantic view — ask questions it can't answer and see what happens
- Compare different LLM models on the same prompt and evaluate quality vs speed vs cost
- Ask the Agent in different languages (Spanish, French, Mandarin) and compare tool routing

**Extend the data**
- Add weather data to correlate store foot traffic with local conditions
- Add competitor pricing data and analyze price positioning by category
- Generate more synthetic data for a specific scenario you want to test

**Build something new**
- Build a new Cortex Search service over marketing campaign briefs
- Add a new custom tool to the Agent (e.g., markdown-to-email formatter, promotion recommender)
- Use CORTEX.COMPLETE to extract structured fields from all support tickets into a new table
- Create a full RAG pipeline for a different question domain

**Add governance**
- Create roles and masking policies to restrict who sees cost/margin data
- Add sensitivity tags to classify columns by confidentiality level
- Test what different roles can and can't see
""")

st.space("small")

st.markdown("#### What you've built today")
with st.container(border=True):
    st.markdown("""
```
Reference Data + Operational Tables + Text Data
        |                |                |
        v                v                v
  Semantic View    Search Service    LLM Functions
        |                |          (Sentiment, Translate,
        v                v           Summarize, Complete)
  Cortex Analyst    RAG Pipeline
        \\              /
         v            v
       Cortex Agent (3 tools)
```
""")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tables", "~15")
col2.metric("AI services", "4+", help="Search, Analyst, Agent, LLM functions")
col3.metric("Custom tools", "1", help="CALCULATE_STOCKOUT_RISK UDF")
col4.metric("Prompts completed", "~20")

render_key_concepts([
    {"term": "Iterative Development with Cortex Code", "definition": "Cortex Code is most powerful when you iterate: try a prompt, see the result, refine, and try again. The objects you've built today form a foundation — the real value comes from extending them to fit your specific use cases."},
    {"term": "Composability", "definition": "Snowflake's AI features are designed to compose together. A semantic view feeds Cortex Analyst, which becomes a tool for an Agent. Each piece works alone but becomes more powerful in combination."},
])

render_what_you_built([
    "Whatever you explored during this free-form session",
])
