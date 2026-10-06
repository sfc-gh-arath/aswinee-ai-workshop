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
    session_num=4,
    title="Dynamic Tables",
    time_range="0:55 - 1:15",
    duration="20 min",
    building="Auto-refreshing churn risk signals and content trend tracker",
)

render_technologies_used([
    {"name": "Dynamic Tables", "description": "Snowflake objects that automatically refresh their contents based on a declarative SQL query and a target lag. Define WHAT you want; Snowflake handles WHEN and HOW to refresh.", "icon": "autorenew"},
    {"name": "TARGET_LAG", "description": "Maximum staleness you'll accept. '1 hour' means the table is never more than 1 hour behind source data. DOWNSTREAM means it refreshes when upstream refreshes.", "icon": "timer"},
    {"name": "Pipeline Chaining", "description": "Dynamic tables can reference other dynamic tables, forming a DAG. Snowflake manages refresh order automatically.", "icon": "bolt"},
])

render_what_you_will_build([
    "DT_CHURN_RISK_SIGNALS — auto-refreshing table flagging device models with deteriorating health",
    "DT_CONTENT_TREND_TRACKER — genre-level content trend classification (surging to falling)",
    "Verified the pipeline: refresh status, risk distributions, and content trends",
])


PROMPT_4_1 = """Create a dynamic table called VIZIO_ANALYTICS_LAB.ANALYTICS.DT_CHURN_RISK_SIGNALS with TARGET_LAG = '1 hour' and WAREHOUSE = VIZIO_LAB_WH.

This table flags device models that show deteriorating health. The query should:

1. Start from VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES
2. For each (MODEL_NAME, SERIES, SIZE, OEM_BRAND), compare the most recent month to the prior month:
   - churn_change: current gross_churn_rate1m - previous gross_churn_rate1m
   - active_device_change: current active_devices - previous active_devices
   - active_device_change_pct: percentage change in active devices
3. Join with the latest month of VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_SUMMARY_WITH_TV_ATTRIBUTES to get avg_viewing_minutes
4. Calculate a risk_signal:
   - 'CHURN_SPIKE': churn_change > 0.02 (churn rate jumped 2+ percentage points)
   - 'DECLINING_ENGAGEMENT': avg_viewing_minutes < 30
   - 'DEVICE_LOSS': active_device_change_pct < -5 (losing >5% of devices)
   - 'MULTIPLE_RISK': more than one of the above conditions is true
   - 'STABLE': none of the above
5. Only include rows where risk_signal != 'STABLE'

Include: model_name, series, size, oem_brand, current active_devices, gross_churn_rate1m, churn_change, avg_viewing_minutes, active_device_change_pct, risk_signal.

Add a COMMENT. Execute and show all flagged models."""

render_prompt("Prompt 4.1", "Churn Risk Signals", PROMPT_4_1)

render_fallback_sql("Churn risk signals", """CREATE OR REPLACE DYNAMIC TABLE VIZIO_ANALYTICS_LAB.ANALYTICS.DT_CHURN_RISK_SIGNALS
    TARGET_LAG = '1 hour'
    WAREHOUSE = VIZIO_LAB_WH
    COMMENT = 'Auto-refreshing churn risk signals - flags models with deteriorating health'
AS
WITH monthly_data AS (
    SELECT
        MODEL_NAME, SERIES, SIZE, OEM_BRAND, MONTH,
        ACTIVE_DEVICES, GROSS_CHURN_RATE1M,
        LAG(GROSS_CHURN_RATE1M) OVER (PARTITION BY MODEL_NAME, SERIES, SIZE ORDER BY MONTH) AS PREV_CHURN,
        LAG(ACTIVE_DEVICES) OVER (PARTITION BY MODEL_NAME, SERIES, SIZE ORDER BY MONTH) AS PREV_ACTIVE
    FROM VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES
),
latest AS (
    SELECT * FROM monthly_data
    WHERE MONTH = (SELECT MAX(MONTH) FROM VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES)
),
engagement AS (
    SELECT MODEL_NAME, SERIES, SIZE, AVG(AVG_VIEWING_MINUTES) AS AVG_VIEWING_MINUTES
    FROM VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_SUMMARY_WITH_TV_ATTRIBUTES
    WHERE DATE >= DATEADD('day', -30, CURRENT_DATE())
    GROUP BY 1, 2, 3
),
scored AS (
    SELECT
        l.MODEL_NAME, l.SERIES, l.SIZE, l.OEM_BRAND,
        l.ACTIVE_DEVICES, l.GROSS_CHURN_RATE1M,
        l.GROSS_CHURN_RATE1M - COALESCE(l.PREV_CHURN, l.GROSS_CHURN_RATE1M) AS CHURN_CHANGE,
        e.AVG_VIEWING_MINUTES,
        (l.ACTIVE_DEVICES - COALESCE(l.PREV_ACTIVE, l.ACTIVE_DEVICES)) * 100.0
            / NULLIF(l.PREV_ACTIVE, 0) AS ACTIVE_DEVICE_CHANGE_PCT,
        CASE
            WHEN (l.GROSS_CHURN_RATE1M - COALESCE(l.PREV_CHURN, l.GROSS_CHURN_RATE1M)) > 0.02
                 AND e.AVG_VIEWING_MINUTES < 30 THEN 'MULTIPLE_RISK'
            WHEN (l.GROSS_CHURN_RATE1M - COALESCE(l.PREV_CHURN, l.GROSS_CHURN_RATE1M)) > 0.02 THEN 'CHURN_SPIKE'
            WHEN e.AVG_VIEWING_MINUTES < 30 THEN 'DECLINING_ENGAGEMENT'
            WHEN (l.ACTIVE_DEVICES - COALESCE(l.PREV_ACTIVE, l.ACTIVE_DEVICES)) * 100.0
                 / NULLIF(l.PREV_ACTIVE, 0) < -5 THEN 'DEVICE_LOSS'
            ELSE 'STABLE'
        END AS RISK_SIGNAL
    FROM latest l
    LEFT JOIN engagement e ON l.MODEL_NAME = e.MODEL_NAME AND l.SERIES = e.SERIES AND l.SIZE = e.SIZE
)
SELECT * FROM scored WHERE RISK_SIGNAL != 'STABLE';

SELECT * FROM VIZIO_ANALYTICS_LAB.ANALYTICS.DT_CHURN_RISK_SIGNALS ORDER BY CHURN_CHANGE DESC;""")

render_explanation("What this prompt does", """
Creates a **dynamic table** that automatically identifies device models with deteriorating health:

**Why a dynamic table?**
- Views recompute every query — fine for ad-hoc but expensive for dashboards
- Dynamic tables pre-compute and auto-refresh within the target lag
- This table stays within 1 hour of source data without manual scheduling

**Risk signals**:
- **CHURN_SPIKE**: Churn rate jumped >2 percentage points month-over-month
- **DECLINING_ENGAGEMENT**: Average viewing under 30 minutes (users aren't watching)
- **DEVICE_LOSS**: Lost >5% of active devices
- **MULTIPLE_RISK**: More than one flag — most urgent
""")


PROMPT_4_2 = """Create a second dynamic table called VIZIO_ANALYTICS_LAB.ANALYTICS.DT_CONTENT_TREND_TRACKER with TARGET_LAG = 'DOWNSTREAM' and WAREHOUSE = VIZIO_LAB_WH.

This table tracks WatchFree+ AVOD content performance trends. The query should:

1. From VIZIO_STREAMING.WFP.AGG_WFP_AVOD_CONTENT_SUMMARY_WITH_METADATA_V2, for each GENRE:
   - Calculate total_sessions, total_duration_mins, total_devices for the last 30 days
   - Calculate the same for the prior 30 days (30-60 days ago)
   - Compute mom_session_change_pct: month-over-month % change in sessions
   - Compute mom_duration_change_pct: month-over-month % change in viewing duration
2. From VIZIO_STREAMING.WFP.AGG_WFP_AVOD_STUDIO_SUMMARY, get the top studio per genre (by duration)
3. Classify trend:
   - 'SURGING': mom_session_change_pct > 20
   - 'GROWING': mom_session_change_pct > 5
   - 'STABLE': between -5 and 5
   - 'DECLINING': mom_session_change_pct < -5
   - 'FALLING': mom_session_change_pct < -20
4. Include: genre, total_sessions, total_duration_mins, total_devices, top_studio, mom_session_change_pct, mom_duration_change_pct, trend

Add a COMMENT. Execute and show results sorted by mom_session_change_pct descending."""

render_prompt("Prompt 4.2", "Content Trend Tracker", PROMPT_4_2)

render_fallback_sql("Content trend tracker", """CREATE OR REPLACE DYNAMIC TABLE VIZIO_ANALYTICS_LAB.ANALYTICS.DT_CONTENT_TREND_TRACKER
    TARGET_LAG = 'DOWNSTREAM'
    WAREHOUSE = VIZIO_LAB_WH
    COMMENT = 'Auto-refreshing WFP content genre trends with MoM changes'
AS
WITH current_period AS (
    SELECT GENRE,
        SUM(AVOD_SESSIONS) AS TOTAL_SESSIONS,
        SUM(DURATION_MINS) AS TOTAL_DURATION_MINS,
        SUM(DEVICES) AS TOTAL_DEVICES
    FROM VIZIO_STREAMING.WFP.AGG_WFP_AVOD_CONTENT_SUMMARY_WITH_METADATA_V2
    WHERE DATE >= DATEADD('day', -30, CURRENT_DATE())
    GROUP BY GENRE
),
prior_period AS (
    SELECT GENRE,
        SUM(AVOD_SESSIONS) AS PREV_SESSIONS,
        SUM(DURATION_MINS) AS PREV_DURATION
    FROM VIZIO_STREAMING.WFP.AGG_WFP_AVOD_CONTENT_SUMMARY_WITH_METADATA_V2
    WHERE DATE >= DATEADD('day', -60, CURRENT_DATE()) AND DATE < DATEADD('day', -30, CURRENT_DATE())
    GROUP BY GENRE
),
top_studios AS (
    SELECT GENRE, STUDIO AS TOP_STUDIO FROM (
        SELECT c.GENRE, s.STUDIO, SUM(s.DURATION_MINS) AS dur,
               ROW_NUMBER() OVER (PARTITION BY c.GENRE ORDER BY SUM(s.DURATION_MINS) DESC) AS rn
        FROM VIZIO_STREAMING.WFP.AGG_WFP_AVOD_CONTENT_SUMMARY_WITH_METADATA_V2 c
        JOIN VIZIO_STREAMING.WFP.AGG_WFP_AVOD_STUDIO_SUMMARY s ON c.DATE = s.DATE
        WHERE c.DATE >= DATEADD('day', -30, CURRENT_DATE())
        GROUP BY c.GENRE, s.STUDIO
    ) WHERE rn = 1
)
SELECT
    c.GENRE, c.TOTAL_SESSIONS, c.TOTAL_DURATION_MINS, c.TOTAL_DEVICES,
    ts.TOP_STUDIO,
    (c.TOTAL_SESSIONS - p.PREV_SESSIONS) * 100.0 / NULLIF(p.PREV_SESSIONS, 0) AS MOM_SESSION_CHANGE_PCT,
    (c.TOTAL_DURATION_MINS - p.PREV_DURATION) * 100.0 / NULLIF(p.PREV_DURATION, 0) AS MOM_DURATION_CHANGE_PCT,
    CASE
        WHEN (c.TOTAL_SESSIONS - p.PREV_SESSIONS) * 100.0 / NULLIF(p.PREV_SESSIONS, 0) > 20 THEN 'SURGING'
        WHEN (c.TOTAL_SESSIONS - p.PREV_SESSIONS) * 100.0 / NULLIF(p.PREV_SESSIONS, 0) > 5 THEN 'GROWING'
        WHEN (c.TOTAL_SESSIONS - p.PREV_SESSIONS) * 100.0 / NULLIF(p.PREV_SESSIONS, 0) < -20 THEN 'FALLING'
        WHEN (c.TOTAL_SESSIONS - p.PREV_SESSIONS) * 100.0 / NULLIF(p.PREV_SESSIONS, 0) < -5 THEN 'DECLINING'
        ELSE 'STABLE'
    END AS TREND
FROM current_period c
LEFT JOIN prior_period p ON c.GENRE = p.GENRE
LEFT JOIN top_studios ts ON c.GENRE = ts.GENRE;

SELECT * FROM VIZIO_ANALYTICS_LAB.ANALYTICS.DT_CONTENT_TREND_TRACKER
ORDER BY MOM_SESSION_CHANGE_PCT DESC;""")

render_explanation("What this prompt does", """
Creates a **downstream dynamic table** tracking content genre trends:

**TARGET_LAG = 'DOWNSTREAM'**: Refreshes automatically when source data changes — no separate schedule needed.

**What it tracks**: For each genre (Drama, Comedy, Action, etc.):
- How many sessions, minutes, and devices in the last 30 days?
- How does that compare to the prior 30 days?
- Which studio drives the most viewing in this genre?
- Is the genre SURGING, GROWING, STABLE, DECLINING, or FALLING?

**Business use**: Content acquisition teams use this to decide what to license next for WatchFree+. Surging genres get more investment; falling genres get reviewed.
""")


PROMPT_4_3 = """Show me the status of both dynamic tables in VIZIO_ANALYTICS_LAB.ANALYTICS:

1. Run DESCRIBE DYNAMIC TABLE for each
2. Query DT_CHURN_RISK_SIGNALS and show the count of models in each risk_signal category
3. Query DT_CONTENT_TREND_TRACKER and show genres by trend status
4. Which device models have MULTIPLE_RISK? Which content genres are SURGING?"""

render_prompt("Prompt 4.3", "Verify the Pipeline", PROMPT_4_3)

render_fallback_sql("Verify dynamic tables", """DESCRIBE DYNAMIC TABLE VIZIO_ANALYTICS_LAB.ANALYTICS.DT_CHURN_RISK_SIGNALS;
DESCRIBE DYNAMIC TABLE VIZIO_ANALYTICS_LAB.ANALYTICS.DT_CONTENT_TREND_TRACKER;

SELECT RISK_SIGNAL, COUNT(*) AS MODEL_COUNT
FROM VIZIO_ANALYTICS_LAB.ANALYTICS.DT_CHURN_RISK_SIGNALS
GROUP BY 1 ORDER BY 2 DESC;

SELECT TREND, COUNT(*) AS GENRE_COUNT
FROM VIZIO_ANALYTICS_LAB.ANALYTICS.DT_CONTENT_TREND_TRACKER
GROUP BY 1 ORDER BY 2 DESC;""")

render_explanation("What this prompt does", """
Validates that the dynamic table pipeline is working correctly and the business logic produces meaningful results.
""")


render_key_concepts([
    {"term": "Dynamic Table", "definition": "A Snowflake object defined by a SELECT query and a TARGET_LAG. Automatically materializes and incrementally refreshes results. Combines view freshness with table performance."},
    {"term": "DOWNSTREAM lag", "definition": "The dynamic table refreshes whenever its upstream sources change. No explicit schedule — Snowflake manages the dependency chain automatically."},
])

render_domain_glossary([
    {"term": "MoM (Month-over-Month)", "definition": "Comparison of a metric between the current period and the same-length prior period. A 10% MoM increase in sessions means 10% more sessions this month than last month."},
    {"term": "Churn Spike", "definition": "A sudden increase in the rate at which devices become inactive. Often caused by firmware issues, competitive launches, or seasonal patterns (e.g., devices gifted at holiday that go inactive by March)."},
])

render_what_you_built([
    "DT_CHURN_RISK_SIGNALS — auto-refreshing table flagging device models with deteriorating health",
    "DT_CONTENT_TREND_TRACKER — genre-level content trend classification (surging to falling)",
    "Verified the pipeline: refresh status, risk distributions, and content trends",
])
