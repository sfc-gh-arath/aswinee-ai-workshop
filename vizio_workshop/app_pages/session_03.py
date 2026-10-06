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
    session_num=3,
    title="Analytics-Ready Views",
    time_range="0:35 - 0:55",
    duration="20 min",
    building="Three cross-database views: WFP engagement, device health scorecard, app performance",
)

render_technologies_used([
    {"name": "CREATE VIEW", "description": "A named SQL query stored in Snowflake. Views don't store data — they compute on-the-fly. Ideal for joining across databases and applying business logic.", "icon": "view_quilt"},
    {"name": "Cross-Database Joins", "description": "Snowflake views can reference tables from any database. We join STREAMING + DEVICES + REVENUE + ENGAGEMENT in a single view.", "icon": "join_inner"},
    {"name": "Window Functions", "description": "LAG, rolling averages, and rankings computed across partitions. Essential for trend analysis and period-over-period comparisons.", "icon": "window"},
])

render_what_you_will_build([
    "WFP_ENGAGEMENT_DAILY — unified WatchFree+ daily KPIs with revenue and trend calculations",
    "DEVICE_HEALTH_SCORECARD — per-model health status: churn, engagement, app usage",
    "APP_PERFORMANCE_SUMMARY — per-app metrics with discovery source and metadata enrichment",
])


PROMPT_3_1 = """Create a view called VIZIO_ANALYTICS_LAB.ANALYTICS.WFP_ENGAGEMENT_DAILY that provides a unified daily view of WatchFree+ performance. Join data from multiple tables:

From VIZIO_STREAMING.WFP.AGG_WFP_GLOBAL_KPIS_ROLLING_30_DAY:
- DATE, WFP_TOKENS, AVOD_TOKENS, WFP_SESSIONS, AVOD_SESSIONS, WFP_VIEWING_HOURS, AVOD_VIEWING_HOURS, BACKEND_APP_TYPE

From VIZIO_STREAMING.WFP.AGG_WFP_LIVE_AND_AVOD_REVENUE_ROLLING_30_DAYS (join on date = event_date):
- WFP_LIVE_REVENUE, WFP_AVOD_REVENUE

Add calculated columns:
- total_revenue: WFP_LIVE_REVENUE + WFP_AVOD_REVENUE
- viewing_hours_per_token: WFP_VIEWING_HOURS / NULLIF(WFP_TOKENS, 0)
- revenue_per_viewing_hour: total_revenue / NULLIF(WFP_VIEWING_HOURS, 0)
- sessions_per_token: WFP_SESSIONS / NULLIF(WFP_TOKENS, 0)
- wow_token_change_pct: (WFP_TOKENS - LAG(WFP_TOKENS, 7) OVER (ORDER BY DATE)) / NULLIF(LAG(WFP_TOKENS, 7) OVER (ORDER BY DATE), 0) * 100
- rolling_7day_avg_revenue: AVG(total_revenue) OVER (ORDER BY DATE ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)

Add a COMMENT on the view. Execute and show the last 7 days to verify."""

render_prompt("Prompt 3.1", "WFP Engagement Daily View", PROMPT_3_1)

render_fallback_sql("WFP engagement view", """CREATE OR REPLACE VIEW VIZIO_ANALYTICS_LAB.ANALYTICS.WFP_ENGAGEMENT_DAILY
COMMENT = 'Unified daily WatchFree+ engagement and revenue metrics'
AS
SELECT
    k.DATE,
    k.WFP_TOKENS,
    k.AVOD_TOKENS,
    k.WFP_SESSIONS,
    k.AVOD_SESSIONS,
    k.WFP_VIEWING_HOURS,
    k.AVOD_VIEWING_HOURS,
    k.BACKEND_APP_TYPE,
    COALESCE(r.WFP_LIVE_REVENUE, 0) AS WFP_LIVE_REVENUE,
    COALESCE(r.WFP_AVOD_REVENUE, 0) AS WFP_AVOD_REVENUE,
    COALESCE(r.WFP_LIVE_REVENUE, 0) + COALESCE(r.WFP_AVOD_REVENUE, 0) AS TOTAL_REVENUE,
    k.WFP_VIEWING_HOURS / NULLIF(k.WFP_TOKENS, 0) AS VIEWING_HOURS_PER_TOKEN,
    (COALESCE(r.WFP_LIVE_REVENUE, 0) + COALESCE(r.WFP_AVOD_REVENUE, 0))
        / NULLIF(k.WFP_VIEWING_HOURS, 0) AS REVENUE_PER_VIEWING_HOUR,
    k.WFP_SESSIONS / NULLIF(k.WFP_TOKENS, 0) AS SESSIONS_PER_TOKEN,
    (k.WFP_TOKENS - LAG(k.WFP_TOKENS, 7) OVER (PARTITION BY k.BACKEND_APP_TYPE ORDER BY k.DATE))
        / NULLIF(LAG(k.WFP_TOKENS, 7) OVER (PARTITION BY k.BACKEND_APP_TYPE ORDER BY k.DATE), 0) * 100
        AS WOW_TOKEN_CHANGE_PCT,
    AVG(COALESCE(r.WFP_LIVE_REVENUE, 0) + COALESCE(r.WFP_AVOD_REVENUE, 0))
        OVER (PARTITION BY k.BACKEND_APP_TYPE ORDER BY k.DATE ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
        AS ROLLING_7DAY_AVG_REVENUE
FROM VIZIO_STREAMING.WFP.AGG_WFP_GLOBAL_KPIS_ROLLING_30_DAY k
LEFT JOIN VIZIO_STREAMING.WFP.AGG_WFP_LIVE_AND_AVOD_REVENUE_ROLLING_30_DAYS r
    ON k.DATE = r.EVENT_DATE;

SELECT * FROM VIZIO_ANALYTICS_LAB.ANALYTICS.WFP_ENGAGEMENT_DAILY
ORDER BY DATE DESC LIMIT 7;""")

render_explanation("What this prompt does", """
Creates a **unified WatchFree+ dashboard view** joining KPIs with revenue:

- **viewing_hours_per_token**: Engagement intensity — are viewers watching more or less?
- **revenue_per_viewing_hour**: Monetization efficiency — how much does each hour of viewing generate?
- **sessions_per_token**: Session frequency — how often do viewers come back?
- **wow_token_change_pct**: Week-over-week growth signal
- **rolling_7day_avg_revenue**: Smoothed revenue trend
""")


PROMPT_3_2 = """Create a view called VIZIO_ANALYTICS_LAB.ANALYTICS.DEVICE_HEALTH_SCORECARD that provides a per-model health snapshot. For each distinct (MODEL_NAME, SERIES, SIZE) combination, calculate:

From VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES (latest month):
- active_devices, new_devices, churned_1m_devices, gross_churn_rate1m, net_churn1m, return_rate

From VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_SUMMARY_WITH_TV_ATTRIBUTES (latest month):
- avg_viewing_minutes, median_viewing_minutes

From VIZIO_DEVICES.APPS.AGG_APP_DEVICES_LAUNCHES_SOURCES (last 30 days):
- total_app_launches, distinct_apps_used (COUNT DISTINCT APP), avg_launches_per_device

Add a health_status classification:
- 'HEALTHY': gross_churn_rate1m < 0.05 AND avg_viewing_minutes > 60
- 'AT_RISK': gross_churn_rate1m >= 0.05 AND gross_churn_rate1m < 0.10
- 'CRITICAL': gross_churn_rate1m >= 0.10 OR avg_viewing_minutes < 20

Add OEM_BRAND from the NRC table. COMMENT the view.
Execute and show all models sorted by gross_churn_rate1m descending (worst first)."""

render_prompt("Prompt 3.2", "Device Health Scorecard", PROMPT_3_2)

render_fallback_sql("Device health scorecard", """CREATE OR REPLACE VIEW VIZIO_ANALYTICS_LAB.ANALYTICS.DEVICE_HEALTH_SCORECARD
COMMENT = 'Per-model device health: churn, engagement, app usage, health classification'
AS
WITH latest_nrc AS (
    SELECT * FROM VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES
    WHERE MONTH = (SELECT MAX(MONTH) FROM VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES)
),
latest_hs AS (
    SELECT MODEL_NAME, SERIES, SIZE, AVG(AVG_VIEWING_MINUTES) AS AVG_VIEWING_MINUTES,
           AVG(MEDIAN_VIEWING_MINUTES) AS MEDIAN_VIEWING_MINUTES
    FROM VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_SUMMARY_WITH_TV_ATTRIBUTES
    WHERE DATE >= DATEADD('day', -30, CURRENT_DATE())
    GROUP BY 1, 2, 3
),
app_usage AS (
    SELECT MODEL_NAME, SERIES, SIZE,
           SUM(LAUNCHES) AS TOTAL_APP_LAUNCHES,
           COUNT(DISTINCT APP) AS DISTINCT_APPS_USED,
           SUM(LAUNCHES) / NULLIF(SUM(DEVICES), 0) AS AVG_LAUNCHES_PER_DEVICE
    FROM VIZIO_DEVICES.APPS.AGG_APP_DEVICES_LAUNCHES_SOURCES
    WHERE ACTIVITY_DATE >= DATEADD('day', -30, CURRENT_DATE())
    GROUP BY 1, 2, 3
)
SELECT
    n.MODEL_NAME, n.SERIES, n.SIZE, n.OEM_BRAND,
    n.ACTIVE_DEVICES, n.NEW_DEVICES, n.CHURN_1M_DEVICES,
    n.GROSS_CHURN_RATE1M, n.NET_CHURN1M, n.RETURN_RATE,
    h.AVG_VIEWING_MINUTES, h.MEDIAN_VIEWING_MINUTES,
    a.TOTAL_APP_LAUNCHES, a.DISTINCT_APPS_USED, a.AVG_LAUNCHES_PER_DEVICE,
    CASE
        WHEN n.GROSS_CHURN_RATE1M >= 0.10 OR h.AVG_VIEWING_MINUTES < 20 THEN 'CRITICAL'
        WHEN n.GROSS_CHURN_RATE1M >= 0.05 THEN 'AT_RISK'
        ELSE 'HEALTHY'
    END AS HEALTH_STATUS
FROM latest_nrc n
LEFT JOIN latest_hs h ON n.MODEL_NAME = h.MODEL_NAME AND n.SERIES = h.SERIES AND n.SIZE = h.SIZE
LEFT JOIN app_usage a ON n.MODEL_NAME = a.MODEL_NAME AND n.SERIES = a.SERIES AND n.SIZE = a.SIZE;

SELECT * FROM VIZIO_ANALYTICS_LAB.ANALYTICS.DEVICE_HEALTH_SCORECARD
ORDER BY GROSS_CHURN_RATE1M DESC;""")

render_explanation("What this prompt does", """
Creates a **device scorecard** — one row per model with health classification:

**Three data sources joined**:
1. NRC (churn/retention) — how many devices are active, churning, returning?
2. Homescreen engagement — how much are they watching?
3. App usage — how actively are they using apps?

**Health classification**: CRITICAL models (high churn or very low engagement) need immediate attention. AT_RISK models are trending negative. HEALTHY models are performing well.

**Cross-database join**: Combines DEVICES.ENGAGEMENT + DEVICES.APPS in a single view — something that would be cumbersome without Snowflake's cross-database capability.
""")


PROMPT_3_3 = """Create a view called VIZIO_ANALYTICS_LAB.ANALYTICS.APP_PERFORMANCE_SUMMARY that aggregates app-level metrics. For each APP (from VIZIO_DEVICES.APPS.AGG_APP_DEVICES_LAUNCHES_SOURCES), calculate over the last 30 days:

- total_devices: SUM(DEVICES)
- total_launches: SUM(LAUNCHES)
- launches_per_device: total_launches / NULLIF(total_devices, 0)
- top_source: the SOURCE with the most launches for that app (use a subquery or window function)
- top_series: the SERIES with the most devices for that app
- vizio_share_pct: % of devices that are OEM_BRAND = 'VIZIO' (vs ONN or other)
- launch_rank: RANK() ordered by total_launches descending

Join with VIZIO_DEVICES.APPS.MAPPING_APP_METADATA to add:
- VOD_TYPE, MONETIZATION_TYPE from the metadata table (match on APP = CURATED_APP_NAME where CURRENT_ROW = TRUE)

COMMENT the view. Execute and show the top 15 apps by launches."""

render_prompt("Prompt 3.3", "App Performance Summary", PROMPT_3_3)

render_fallback_sql("App performance summary", """CREATE OR REPLACE VIEW VIZIO_ANALYTICS_LAB.ANALYTICS.APP_PERFORMANCE_SUMMARY
COMMENT = 'Per-app performance: launches, devices, top source/series, metadata'
AS
WITH app_stats AS (
    SELECT
        APP,
        SUM(DEVICES) AS TOTAL_DEVICES,
        SUM(LAUNCHES) AS TOTAL_LAUNCHES,
        SUM(LAUNCHES) / NULLIF(SUM(DEVICES), 0) AS LAUNCHES_PER_DEVICE,
        SUM(CASE WHEN OEM_BRAND = 'VIZIO' THEN DEVICES ELSE 0 END) * 100.0
            / NULLIF(SUM(DEVICES), 0) AS VIZIO_SHARE_PCT,
        RANK() OVER (ORDER BY SUM(LAUNCHES) DESC) AS LAUNCH_RANK
    FROM VIZIO_DEVICES.APPS.AGG_APP_DEVICES_LAUNCHES_SOURCES
    WHERE ACTIVITY_DATE >= DATEADD('day', -30, CURRENT_DATE())
    GROUP BY APP
),
top_sources AS (
    SELECT APP, SOURCE AS TOP_SOURCE
    FROM (
        SELECT APP, SOURCE, SUM(LAUNCHES) AS src_launches,
               ROW_NUMBER() OVER (PARTITION BY APP ORDER BY SUM(LAUNCHES) DESC) AS rn
        FROM VIZIO_DEVICES.APPS.AGG_APP_DEVICES_LAUNCHES_SOURCES
        WHERE ACTIVITY_DATE >= DATEADD('day', -30, CURRENT_DATE())
        GROUP BY APP, SOURCE
    ) WHERE rn = 1
),
top_series AS (
    SELECT APP, SERIES AS TOP_SERIES
    FROM (
        SELECT APP, SERIES, SUM(DEVICES) AS ser_devices,
               ROW_NUMBER() OVER (PARTITION BY APP ORDER BY SUM(DEVICES) DESC) AS rn
        FROM VIZIO_DEVICES.APPS.AGG_APP_DEVICES_LAUNCHES_SOURCES
        WHERE ACTIVITY_DATE >= DATEADD('day', -30, CURRENT_DATE())
        GROUP BY APP, SERIES
    ) WHERE rn = 1
)
SELECT a.*, s.TOP_SOURCE, t.TOP_SERIES,
       m.VOD_TYPE, m.MONETIZATION_TYPE
FROM app_stats a
LEFT JOIN top_sources s ON a.APP = s.APP
LEFT JOIN top_series t ON a.APP = t.APP
LEFT JOIN VIZIO_DEVICES.APPS.MAPPING_APP_METADATA m
    ON a.APP = m.CURATED_APP_NAME AND m.CURRENT_ROW = TRUE;

SELECT * FROM VIZIO_ANALYTICS_LAB.ANALYTICS.APP_PERFORMANCE_SUMMARY
ORDER BY LAUNCH_RANK LIMIT 15;""")

render_explanation("What this prompt does", """
Creates an **app ecosystem scorecard**:

- **launches_per_device**: App stickiness — Netflix might have fewer total devices but more launches per device than YouTube
- **top_source**: How are users discovering this app? Homescreen, voice, casting?
- **vizio_share_pct**: VIZIO vs ONN brand distribution per app
- **Metadata enrichment**: Adds VOD type (SVOD/AVOD/TVOD) and monetization type from the app catalog

This is the view that answers: "Which apps drive the most engagement on our platform?"
""")


render_key_concepts([
    {"term": "Cross-Database Views", "definition": "Snowflake views can reference tables from any database the user has access to. A single view can join VIZIO_STREAMING and VIZIO_DEVICES data — no ETL needed."},
    {"term": "CTE Pattern", "definition": "Common Table Expressions (WITH clauses) break complex queries into logical steps. We use CTEs to calculate app stats, find top sources, and find top series separately, then join them."},
    {"term": "Health Classification", "definition": "Business rules encoded as CASE expressions that classify entities (devices, apps, models) into actionable categories. The DEVICE_HEALTH_SCORECARD uses churn + engagement to flag CRITICAL, AT_RISK, and HEALTHY models."},
])

render_domain_glossary([
    {"term": "Token", "definition": "A unique identifier for a VIZIO/ONN device. One token = one TV. Used to count unique devices across engagement metrics. Not the same as a user account (one account can have multiple tokens/TVs)."},
    {"term": "Gross Churn Rate", "definition": "Percentage of devices that were active last month but are NOT active this month. Does not account for returning devices. A 5% gross churn means 5 out of every 100 devices stopped being used."},
    {"term": "Net Churn", "definition": "Gross churn minus returning devices. Can be negative (more devices returning than leaving). Net churn < 0 means the active fleet is growing."},
])

render_what_you_built([
    "WFP_ENGAGEMENT_DAILY — unified WatchFree+ daily KPIs with revenue and trend calculations",
    "DEVICE_HEALTH_SCORECARD — per-model health status: churn, engagement, app usage",
    "APP_PERFORMANCE_SUMMARY — per-app metrics with discovery source and metadata enrichment",
])
