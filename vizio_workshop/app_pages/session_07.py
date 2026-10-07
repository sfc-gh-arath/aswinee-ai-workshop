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
    render_what_you_will_build,
)

render_session_header(
    session_num=7,
    title="Cortex Agent & CoWork",
    time_range="1:55 - 2:10",
    duration="15 min",
    building="Multi-tool AI agent for conversational BI in Snowsight",
)

render_technologies_used([
    {"name": "Cortex Agent", "description": "An AI orchestrator that routes questions to the right tool: Analyst for structured data, Search for policies, custom UDFs for calculations.", "icon": "smart_toy"},
    {"name": "CREATE AGENT", "description": "DDL to define an agent with: model (LLM), tools (what it can use), instructions (routing logic and domain context), sample_questions (CoWork UI).", "icon": "engineering"},
    {"name": "CoWork", "description": "The conversational BI interface in Snowsight where agents live. Users type questions and get answers — no SQL required.", "icon": "forum"},
])

render_what_you_will_build([
    "CALCULATE_ENGAGEMENT_SCORE UDF — composite scoring tool for the agent",
    "SMARTCAST_AGENT — multi-tool Cortex Agent with Analyst + Search + UDF",
    "Publish the agent and use it in CoWork for conversational BI",
    "Test all tool routes: structured, policy, scoring, and multi-tool queries",
    "Generate visualizations (charts) through conversational questions in CoWork",
])


PROMPT_7_1 = """Create a SQL UDF called VIZIO_ANALYTICS_LAB.AI_OBJECTS.CALCULATE_ENGAGEMENT_SCORE that takes a SERIES (VARCHAR) as input and returns a VARIANT with a composite engagement score.

The function should:
1. Query DEVICE_HEALTH_SCORECARD for that series and calculate:
   - churn_score (0-30 points): 30 - (avg gross_churn_rate1m * 300). Lower churn = higher score.
   - viewing_score (0-30 points): MIN(avg_viewing_minutes / 3, 30). More viewing = higher score.
   - app_score (0-20 points): MIN(avg distinct_apps_used * 4, 20). More app diversity = higher score.
   - retention_score (0-20 points): avg return_rate * 100, capped at 20. Higher return rate = higher score.
2. Calculate total_engagement_score = churn_score + viewing_score + app_score + retention_score (0-100)
3. Classify: 'EXCELLENT' (>= 80), 'GOOD' (>= 60), 'FAIR' (>= 40), 'POOR' (< 40)

Return OBJECT_CONSTRUCT with: series, total_engagement_score, classification, churn_score, viewing_score, app_score, retention_score, active_devices (total for series), avg_churn_rate.

Execute and test with: SELECT CALCULATE_ENGAGEMENT_SCORE('V-Series');
Then test all series."""

render_prompt("Prompt 7.1", "Create Engagement Score UDF", PROMPT_7_1)

render_fallback_sql("Engagement score UDF", """CREATE OR REPLACE FUNCTION VIZIO_ANALYTICS_LAB.AI_OBJECTS.CALCULATE_ENGAGEMENT_SCORE(P_SERIES VARCHAR)
    RETURNS VARIANT
    LANGUAGE SQL
AS
$$
    SELECT OBJECT_CONSTRUCT(
        'series', P_SERIES,
        'active_devices', SUM(ACTIVE_DEVICES),
        'avg_churn_rate', ROUND(AVG(GROSS_CHURN_RATE1M), 4),
        'churn_score', ROUND(GREATEST(30 - AVG(GROSS_CHURN_RATE1M) * 300, 0), 1),
        'viewing_score', ROUND(LEAST(AVG(AVG_VIEWING_MINUTES) / 3, 30), 1),
        'app_score', ROUND(LEAST(AVG(DISTINCT_APPS_USED) * 4, 20), 1),
        'retention_score', ROUND(LEAST(AVG(RETURN_RATE) * 100, 20), 1),
        'total_engagement_score', ROUND(
            GREATEST(30 - AVG(GROSS_CHURN_RATE1M) * 300, 0) +
            LEAST(AVG(AVG_VIEWING_MINUTES) / 3, 30) +
            LEAST(AVG(DISTINCT_APPS_USED) * 4, 20) +
            LEAST(AVG(RETURN_RATE) * 100, 20), 1),
        'classification', CASE
            WHEN GREATEST(30 - AVG(GROSS_CHURN_RATE1M) * 300, 0) +
                 LEAST(AVG(AVG_VIEWING_MINUTES) / 3, 30) +
                 LEAST(AVG(DISTINCT_APPS_USED) * 4, 20) +
                 LEAST(AVG(RETURN_RATE) * 100, 20) >= 80 THEN 'EXCELLENT'
            WHEN GREATEST(30 - AVG(GROSS_CHURN_RATE1M) * 300, 0) +
                 LEAST(AVG(AVG_VIEWING_MINUTES) / 3, 30) +
                 LEAST(AVG(DISTINCT_APPS_USED) * 4, 20) +
                 LEAST(AVG(RETURN_RATE) * 100, 20) >= 60 THEN 'GOOD'
            WHEN GREATEST(30 - AVG(GROSS_CHURN_RATE1M) * 300, 0) +
                 LEAST(AVG(AVG_VIEWING_MINUTES) / 3, 30) +
                 LEAST(AVG(DISTINCT_APPS_USED) * 4, 20) +
                 LEAST(AVG(RETURN_RATE) * 100, 20) >= 40 THEN 'FAIR'
            ELSE 'POOR'
        END
    )
    FROM VIZIO_ANALYTICS_LAB.ANALYTICS.DEVICE_HEALTH_SCORECARD
    WHERE SERIES = P_SERIES
$$;

-- Test
SELECT CALCULATE_ENGAGEMENT_SCORE('V-Series');
SELECT CALCULATE_ENGAGEMENT_SCORE('M-Series');
SELECT CALCULATE_ENGAGEMENT_SCORE('P-Series');""")

render_explanation("What this prompt does", """
Creates a **custom tool** the Agent can invoke for composite engagement scoring:

**Four scoring dimensions**:
- **Churn** (30pts): Low churn = high score
- **Viewing** (30pts): More minutes watched = higher score
- **App diversity** (20pts): Using more apps = more engaged
- **Retention** (20pts): High return rate = strong loyalty

The Agent calls this when someone asks "How engaged are V-Series users?" — instead of running complex SQL, it gets a pre-scored summary.
""")


PROMPT_7_2 = """Create a Cortex Agent called VIZIO_ANALYTICS_LAB.AI_OBJECTS.SMARTCAST_AGENT with:

MODEL: Set to AUTO (let Snowflake select the best available model automatically)

TOOLS:
1. Semantic view VIZIO_ANALYTICS_LAB.AI_OBJECTS.SMARTCAST_ANALYTICS_SV (for Cortex Analyst — structured data)
2. Cortex Search service VIZIO_ANALYTICS_LAB.AI_OBJECTS.VIZIO_POLICY_SEARCH (for policy/process questions)
3. UDF VIZIO_ANALYTICS_LAB.AI_OBJECTS.CALCULATE_ENGAGEMENT_SCORE (for engagement scoring)

IMPORTANT — Correct syntax for UDF tools in agent YAML:
- Do NOT use tool type "function" — that is invalid in the agent spec
- For UDF-based custom tools, use:
  - In the tools section: type = "generic" with an input_schema that describes the parameters
  - In the tool_resources section: type = "function" with the fully qualified function identifier and execution_environment = "sandbox"

Example of correct UDF tool syntax in the agent YAML:
```
tools:
  - tool_type: generic
    name: calculate_engagement_score
    description: "Calculates a composite engagement score for a TV series"
    input_schema:
      type: object
      properties:
        series:
          type: string
          description: "TV series name (e.g., V-Series, M-Series, P-Series)"
      required:
        - series
tool_resources:
  - tool_type: function
    name: calculate_engagement_score
    identifier: VIZIO_ANALYTICS_LAB.AI_OBJECTS.CALCULATE_ENGAGEMENT_SCORE
    execution_environment: sandbox
```

INSTRUCTIONS: "You are a platform analytics assistant for VIZIO's SmartCast team. You help analysts understand device engagement, WatchFree+ performance, app ecosystem health, and content trends.

Tool routing:
- For questions about device health, WFP metrics, app performance, churn, revenue, or any data query: use the semantic view (Cortex Analyst)
- For questions about policies, processes, guidelines, or 'how do we...': use the search service
- For questions asking about engagement score or health score for a specific TV series: use calculate_engagement_score with the series name
- For complex questions needing both data AND context: use multiple tools and synthesize

Domain context:
- VIZIO sells TVs under VIZIO (premium) and ONN (Walmart budget) brands
- Product lines: V-Series (budget), M-Series (mid-range), P-Series (premium), Quantum (high-end), OLED (flagship)
- WatchFree+ (WFP) is the free ad-supported streaming service — key revenue driver
- Key metrics: active tokens (devices), churn rate (target < 5%), viewing hours per token, WFP revenue
- Churn > 10% is critical. Health status: HEALTHY/AT_RISK/CRITICAL from device scorecard"

SAMPLE_QUESTIONS:
- "How many active WatchFree+ viewers do we have?"
- "Which device models are at critical health risk?"
- "What's the engagement score for P-Series?"
- "What are the top streaming apps on our platform?"
- "What's the WFP channel onboarding process?"
- "How has ad revenue trended this quarter?"

Execute and confirm the agent is created."""

render_prompt("Prompt 7.2", "Create the Cortex Agent", PROMPT_7_2)

render_fallback_sql("Create agent", """-- The CREATE AGENT DDL is complex. Key points:
-- 1. MODEL = 'AUTO' (Snowflake picks the best model)
-- 2. Semantic view and search tools use their standard types
-- 3. UDF tools use type "generic" (NOT "function") in the tools section
--    and type "function" with identifier in tool_resources
--
-- Use Cortex Code to generate the full DDL from the prompt above.
-- Verify after creation:
SHOW AGENTS IN SCHEMA VIZIO_ANALYTICS_LAB.AI_OBJECTS;""")

render_explanation("What this prompt does", """
Creates the **capstone** of the entire lab — a multi-tool Cortex Agent:

**Model = AUTO**: Snowflake automatically selects the best available model for the agent. No need to pick a specific model — it adapts as new models become available.

**Three tools, three capabilities**:
1. **Analyst** (semantic view): Data queries → "how many viewers?", "churn by model?"
2. **Search** (knowledge base): Policy questions → "what's the firmware update process?"
3. **UDF** (custom logic): Engagement scoring → "rate the V-Series"

**UDF tool syntax gotcha**: Custom function tools use `type: generic` (not `function`) in the tools section, with an `input_schema` describing the parameters. The `tool_resources` section then maps the generic tool to the actual UDF with `type: function` and the fully qualified identifier. Getting this wrong gives the error "Tool type function is not valid."

**SAMPLE_QUESTIONS** appear in CoWork as suggested starting points.
""")

st.markdown("---")
st.markdown("#### :material/publish: Publishing the Agent to CoWork")
with st.container(border=True):
    st.markdown("""
After the agent is created, you need to **publish it** to make it available in CoWork:

1. In Snowsight, go to **AI & ML → Cortex Agents** (or search for "Agents" in the left nav)
2. Find **SMARTCAST_AGENT** in the list under `VIZIO_ANALYTICS_LAB.AI_OBJECTS`
3. Click on the agent to open its detail page
4. Click **Publish** — this makes the agent available in CoWork
5. To access it: click **CoWork** in the Snowsight left navigation panel
6. In CoWork, select **SMARTCAST_AGENT** from the agent dropdown at the top
7. Start typing questions — the agent handles tool selection automatically

:material/info: **Permissions**: Other users need USAGE on the agent and its underlying tools (semantic view, search service, UDF) to use it in CoWork. For this lab, ACCOUNTADMIN has full access.
""")


PROMPT_7_3 = """Test the SMARTCAST_AGENT:

1. Structured query: "Which 3 device models have the worst churn rate and what's their health status?"
2. Policy query: "What are VIZIO's privacy policies around ACR data collection?"
3. Scoring query: "What's the engagement score for the M-Series?"
4. Multi-tool: "The V-Series 32 inch seems to be struggling. What's the engagement score, what does the data show about its churn, and do we have any policies about supporting end-of-life models?"

Use SNOWFLAKE.CORTEX.DATA_AGENT_RUN() to test each.

Then open CoWork in Snowsight (left nav → CoWork → select SMARTCAST_AGENT) and try these conversational questions:
- "How's the platform doing today?"
- "Anything I should worry about?"

Now try questions that generate visualizations in CoWork:
- "Show me a bar chart of churn rate by TV series"
- "Chart the WFP viewing hours trend over the last 6 months"
- "Compare app launches across the top 10 apps as a bar chart"
- "Show me a breakdown of device health status as a pie chart"

CoWork can generate charts automatically when the question implies a visual. Try asking for specific chart types (bar, line, pie) to see how the agent responds."""

render_prompt("Prompt 7.3", "Test the Agent & CoWork", PROMPT_7_3)

render_fallback_sql("Test agent", """-- Test structured query
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'VIZIO_ANALYTICS_LAB.AI_OBJECTS.SMARTCAST_AGENT',
    'Which 3 device models have the worst churn rate and their health status?'
);

-- Test scoring
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'VIZIO_ANALYTICS_LAB.AI_OBJECTS.SMARTCAST_AGENT',
    'What is the engagement score for the M-Series?'
);

-- To access in CoWork:
-- Snowsight → CoWork (left nav) → Select SMARTCAST_AGENT""")

render_explanation("What this prompt does", """
The **culmination** of the lab — testing all three tools through a single interface:

1. **Structured → Analyst**: Generates SQL from the semantic view
2. **Policy → Search**: Retrieves and synthesizes from the knowledge base
3. **Scoring → UDF**: Calls the custom function
4. **Multi-tool**: Combines all three for a comprehensive answer about V-Series 32"
5. **Visualizations**: CoWork can generate bar charts, line charts, and pie charts when asked

**Accessing CoWork**: Snowsight left nav → **CoWork** → select **SMARTCAST_AGENT** from the dropdown. Type questions naturally — the agent handles everything.

**Visualization tips**: When you ask for a "chart" or "trend" or "comparison," CoWork will render the data as a visual. Try specifying chart types ("bar chart of...") or let CoWork pick automatically ("show me the trend of...").
""")


render_key_concepts([
    {"term": "Cortex Agent", "definition": "A Snowflake object that orchestrates multiple tools (Analyst, Search, UDFs) based on the user's question. Created with CREATE AGENT DDL. Accessible via DATA_AGENT_RUN() or CoWork UI."},
    {"term": "Tool Routing", "definition": "The agent's ability to select the appropriate tool for each question. Instructions guide this: data → Analyst, policies → Search, calculations → UDF."},
    {"term": "CoWork", "definition": "Snowsight's conversational BI interface. Users type natural language questions and get answers from agents. Supports follow-up questions and conversation history."},
])

render_domain_glossary([
    {"term": "Platform Analytics", "definition": "The team responsible for understanding how the SmartCast platform performs: device engagement, app usage, content consumption, churn, and monetization. This agent is built for them."},
    {"term": "Conversational BI", "definition": "Business intelligence through natural language conversation rather than dashboards or SQL. The user asks a question; the system generates the answer by querying data, retrieving documents, or running calculations."},
])

render_what_you_built([
    "CALCULATE_ENGAGEMENT_SCORE UDF — composite scoring tool for the agent",
    "SMARTCAST_AGENT — multi-tool Cortex Agent with Analyst + Search + UDF",
    "Published the agent and accessed it via CoWork",
    "Tested all tool routes: structured, policy, scoring, and multi-tool queries",
    "Generated visualizations (bar charts, line charts) through conversational questions",
])
