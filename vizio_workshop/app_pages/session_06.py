import streamlit as st
from components import (
    render_session_header,
    render_prompt,
    render_fallback_sql,
    render_explanation,
    render_technologies_used,
    render_key_concepts,
    render_domain_glossary,
    render_what_you_built,
)

render_session_header(
    session_num=6,
    title="Semantic View & Cortex Search",
    time_range="1:35 - 1:55",
    duration="20 min",
    building="Natural language to SQL + searchable knowledge base over VIZIO policies",
)

render_technologies_used([
    {"name": "Semantic View", "description": "A first-class Snowflake object that describes data in business terms: tables, relationships, facts, dimensions, metrics, synonyms. The bridge between natural language and SQL.", "icon": "description"},
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine. Converts natural language questions into SQL using the semantic view for context.", "icon": "chat"},
    {"name": "Cortex Search Service", "description": "Managed hybrid search (vector + keyword + reranking). Indexes text and returns semantically relevant results.", "icon": "manage_search"},
])

st.markdown("---")
st.markdown("#### :material/bolt: Quick Setup Option — Pre-built Semantic View")
with st.container(border=True):
    st.markdown("""
If you want to **skip Prompt 6.1** (creating the semantic view from scratch) and use a pre-built one:

1. **Download** the YAML file: [SMARTCAST_ANALYTICS_SV.sv.yaml](https://github.com/sfc-gh-arath/aswinee-ai-workshop/blob/main/vizio_workshop/SMARTCAST_ANALYTICS_SV.sv.yaml)
   - Click the **Download raw file** button (↓ icon) on the GitHub page
2. In Snowsight, go to **Projects → Workspaces**
3. **Upload** the `.sv.yaml` file into your Workspace
4. Open the file — it will display the semantic view editor
5. Click **Publish** and select the target location: **VIZIO_ANALYTICS_LAB.AI_OBJECTS**
6. The semantic view is now live — skip to **Prompt 6.2** to test it

This is faster than having Cortex Code generate the view from scratch.
""")

st.markdown("---")


PROMPT_6_1 = """Create a semantic view called VIZIO_ANALYTICS_LAB.AI_OBJECTS.SMARTCAST_ANALYTICS_SV for use with Cortex Analyst. Cover these tables:

From VIZIO_ANALYTICS_LAB.ANALYTICS:
- WFP_ENGAGEMENT_DAILY
- DEVICE_HEALTH_SCORECARD
- APP_PERFORMANCE_SUMMARY

Include:
- RELATIONSHIPS:
  - WFP_ENGAGEMENT_DAILY is standalone (daily grain, no join key to other views)
  - DEVICE_HEALTH_SCORECARD and APP_PERFORMANCE_SUMMARY can join on SERIES

- FACTS:
  - From WFP_ENGAGEMENT_DAILY: WFP_TOKENS, AVOD_TOKENS, WFP_SESSIONS, AVOD_SESSIONS, WFP_VIEWING_HOURS, AVOD_VIEWING_HOURS, TOTAL_REVENUE, WFP_LIVE_REVENUE, WFP_AVOD_REVENUE, VIEWING_HOURS_PER_TOKEN, REVENUE_PER_VIEWING_HOUR, SESSIONS_PER_TOKEN, WOW_TOKEN_CHANGE_PCT, ROLLING_7DAY_AVG_REVENUE
  - From DEVICE_HEALTH_SCORECARD: ACTIVE_DEVICES, NEW_DEVICES, CHURN_1M_DEVICES, GROSS_CHURN_RATE1M, NET_CHURN1M, RETURN_RATE, AVG_VIEWING_MINUTES, TOTAL_APP_LAUNCHES, DISTINCT_APPS_USED
  - From APP_PERFORMANCE_SUMMARY: TOTAL_DEVICES, TOTAL_LAUNCHES, LAUNCHES_PER_DEVICE, VIZIO_SHARE_PCT

- DIMENSIONS:
  - From WFP_ENGAGEMENT_DAILY: DATE, BACKEND_APP_TYPE
  - From DEVICE_HEALTH_SCORECARD: MODEL_NAME, SERIES, SIZE, OEM_BRAND, HEALTH_STATUS
  - From APP_PERFORMANCE_SUMMARY: APP, TOP_SOURCE, TOP_SERIES, VOD_TYPE, MONETIZATION_TYPE, LAUNCH_RANK

- SYNONYMS:
  - WFP_TOKENS WITH SYNONYMS = ('viewers', 'unique viewers', 'WatchFree users', 'WFP users')
  - WFP_VIEWING_HOURS WITH SYNONYMS = ('watch time', 'viewing time', 'hours watched')
  - GROSS_CHURN_RATE1M WITH SYNONYMS = ('churn rate', 'churn', 'device churn')
  - TOTAL_REVENUE WITH SYNONYMS = ('revenue', 'ad revenue', 'WFP revenue')
  - SERIES WITH SYNONYMS = ('TV series', 'product line', 'model line')
  - APP WITH SYNONYMS = ('application', 'streaming app', 'service')
  - HEALTH_STATUS WITH SYNONYMS = ('device health', 'model health', 'risk status')
  - ACTIVE_DEVICES WITH SYNONYMS = ('active TVs', 'active fleet', 'fleet size')

- METRICS:
  - total_wfp_viewers: SUM(WFP_TOKENS)
  - total_wfp_revenue: SUM(TOTAL_REVENUE)
  - avg_churn_rate: AVG(GROSS_CHURN_RATE1M)
  - avg_viewing_hours_per_token: AVG(VIEWING_HOURS_PER_TOKEN)
  - total_active_devices: SUM(ACTIVE_DEVICES)
  - total_app_launches: SUM(TOTAL_LAUNCHES)

- AI_SQL_GENERATION instruction: "This is VIZIO SmartCast platform data. VIZIO sells smart TVs under two brands: VIZIO (premium) and ONN (Walmart budget). Key product lines: V-Series (budget), M-Series (mid-range), P-Series (premium), Quantum (high-end), OLED (flagship). WatchFree+ (WFP) is VIZIO's free ad-supported streaming service with live channels and AVOD content. When asked about 'viewers' or 'users', use WFP_TOKENS. When asked about 'health' or 'risk', use HEALTH_STATUS from DEVICE_HEALTH_SCORECARD. Churn rate > 5% is concerning; > 10% is critical."

- COMMENTs on all objects.

Execute and verify with DESCRIBE SEMANTIC VIEW."""

render_prompt("Prompt 6.1", "Create the Semantic View", PROMPT_6_1)

render_fallback_sql("Create semantic view", """-- This is a complex DDL — use Cortex Code to generate it.
-- The semantic view covers 3 analytics views with:
-- - Facts: tokens, sessions, viewing hours, revenue, churn, app launches
-- - Dimensions: date, model, series, size, brand, health status, app, source
-- - Metrics: pre-aggregated KPIs
-- - Synonyms: VIZIO-specific terminology
-- - AI instructions: business context for SQL generation
--
-- After creation, verify with:
DESCRIBE SEMANTIC VIEW VIZIO_ANALYTICS_LAB.AI_OBJECTS.SMARTCAST_ANALYTICS_SV;""")

render_explanation("What this prompt does", """
Creates a **semantic view** that maps VIZIO's data to business language:

**Synonyms are critical**: An analyst asking about "churn" needs to map to GROSS_CHURN_RATE1M. "Viewers" maps to WFP_TOKENS. Without synonyms, Cortex Analyst may not understand the question.

**AI_SQL_GENERATION** provides context the column names don't convey: what "V-Series" means, that WFP is an ad-supported service, what churn thresholds are concerning.
""")


PROMPT_6_2 = """Test Cortex Analyst with these questions using VIZIO_ANALYTICS_LAB.AI_OBJECTS.SMARTCAST_ANALYTICS_SV:

1. "How many WatchFree+ viewers do we have?"
2. "Which device models have critical health status?"
3. "What are the top 5 apps by launches?"
4. "What's the average churn rate by TV series?"
5. "How has WFP revenue trended over the last 6 months?"

Show both the generated SQL and the results for each."""

render_prompt("Prompt 6.2", "Test Natural Language Queries", PROMPT_6_2)

render_fallback_sql("Test queries manually", """-- Q1: WFP viewers
SELECT SUM(WFP_TOKENS) AS total_wfp_viewers
FROM VIZIO_ANALYTICS_LAB.ANALYTICS.WFP_ENGAGEMENT_DAILY
WHERE DATE = (SELECT MAX(DATE) FROM VIZIO_ANALYTICS_LAB.ANALYTICS.WFP_ENGAGEMENT_DAILY);

-- Q2: Critical devices
SELECT MODEL_NAME, SERIES, SIZE, OEM_BRAND, GROSS_CHURN_RATE1M, AVG_VIEWING_MINUTES
FROM VIZIO_ANALYTICS_LAB.ANALYTICS.DEVICE_HEALTH_SCORECARD
WHERE HEALTH_STATUS = 'CRITICAL';

-- Q3: Top apps
SELECT APP, TOTAL_LAUNCHES, LAUNCHES_PER_DEVICE
FROM VIZIO_ANALYTICS_LAB.ANALYTICS.APP_PERFORMANCE_SUMMARY
ORDER BY TOTAL_LAUNCHES DESC LIMIT 5;

-- Q4: Churn by series
SELECT SERIES, AVG(GROSS_CHURN_RATE1M) AS AVG_CHURN
FROM VIZIO_ANALYTICS_LAB.ANALYTICS.DEVICE_HEALTH_SCORECARD
GROUP BY SERIES ORDER BY AVG_CHURN DESC;""")

render_explanation("What this prompt does", """
Tests the semantic view across different question types:

1. **"WFP viewers"** — Tests synonym mapping (viewers → WFP_TOKENS)
2. **"Critical health"** — Tests dimension filtering on HEALTH_STATUS
3. **"Top apps by launches"** — Tests ranking from APP_PERFORMANCE_SUMMARY
4. **"Churn by series"** — Tests aggregation grouped by dimension
5. **"Revenue trend"** — Tests time-series from WFP_ENGAGEMENT_DAILY
""")


PROMPT_6_3 = """Now create a Cortex Search service for the knowledge base.

1. Create the search service called VIZIO_ANALYTICS_LAB.AI_OBJECTS.VIZIO_POLICY_SEARCH with:
   - ON: content (searchable text)
   - ATTRIBUTES: category, title (filterable metadata)
   - WAREHOUSE: VIZIO_LAB_WH
   - TARGET_LAG: '1 hour'
   - EMBEDDING_MODEL: 'snowflake-arctic-embed-l-v2.0'
   - SOURCE: VIZIO_ANALYTICS_LAB.AI_OBJECTS.VIZIO_KNOWLEDGE_BASE

2. Test with these searches:
   - "WatchFree+ channel onboarding process"
   - "firmware update schedule"
   - "viewer privacy and data collection policies"
   - Search for "advertising" filtered to category = 'advertising'

3. Build a quick RAG query: use CORTEX.SEARCH_PREVIEW() to find the top 3 documents about "ACR opt-out policy", then pass them to AI_COMPLETE('claude-sonnet-5', ...) to generate a grounded answer.

Show results for each."""

render_prompt("Prompt 6.3", "Create Cortex Search + RAG Test", PROMPT_6_3)

render_fallback_sql("Create search service", """CREATE OR REPLACE CORTEX SEARCH SERVICE VIZIO_ANALYTICS_LAB.AI_OBJECTS.VIZIO_POLICY_SEARCH
    ON content
    ATTRIBUTES category, title
    WAREHOUSE = VIZIO_LAB_WH
    TARGET_LAG = '1 hour'
    EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
    AS (
        SELECT doc_id, title, content, category
        FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.VIZIO_KNOWLEDGE_BASE
    );

-- Verify
SHOW CORTEX SEARCH SERVICES IN SCHEMA VIZIO_ANALYTICS_LAB.AI_OBJECTS;

-- Test search (example)
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'VIZIO_ANALYTICS_LAB.AI_OBJECTS.VIZIO_POLICY_SEARCH',
    '{\"query\": \"firmware update schedule\", \"columns\": [\"title\", \"content\", \"category\"], \"limit\": 3}'
);""")

render_explanation("What this prompt does", """
Creates a **managed search service** and tests it with a RAG pattern:

**Search service**: One DDL creates a hybrid search engine over your knowledge base. Snowflake handles embedding generation, indexing, and refresh.

**Four search tests**: Keyword, semantic, conceptual, and filtered — demonstrating different retrieval modes.

**RAG test**: Search → retrieve top documents → feed as context to an LLM → get a grounded answer. This becomes the Agent's second tool in Session 7.
""")


render_key_concepts([
    {"term": "Semantic View", "definition": "Maps database tables to business concepts: facts, dimensions, metrics, synonyms, and AI instructions. Enables natural language to SQL via Cortex Analyst."},
    {"term": "Cortex Search", "definition": "Managed hybrid search combining keyword matching, vector similarity, and neural reranking. Created with a single DDL statement. Auto-refreshes within the target lag."},
    {"term": "RAG", "definition": "Retrieval Augmented Generation — search for relevant documents, inject them as context into an LLM prompt, get a grounded answer. Prevents hallucination by anchoring in actual content."},
])

render_what_you_built([
    "SMARTCAST_ANALYTICS_SV semantic view with VIZIO-specific synonyms and AI instructions",
    "Tested 5 natural language queries via Cortex Analyst",
    "VIZIO_POLICY_SEARCH Cortex Search service over the knowledge base",
    "RAG pipeline: search → context → grounded LLM answer",
])
