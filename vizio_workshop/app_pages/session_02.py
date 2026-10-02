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
    session_num=2,
    title="Data Discovery with Cortex Code",
    time_range="0:20 - 0:35",
    duration="15 min",
    building="Exploratory analysis — schema, data quality, business patterns across 2 databases",
)

render_technologies_used([
    {"name": "Cortex Code", "description": "Snowflake's AI coding assistant. Ask natural language questions about your data and it generates + executes SQL. The primary discovery tool.", "icon": "psychology"},
    {"name": "Cross-Database Queries", "description": "Snowflake can query across databases in a single statement using fully qualified names (DATABASE.SCHEMA.TABLE). Essential when data spans multiple databases.", "icon": "join_inner"},
    {"name": "Data Profiling", "description": "Techniques for understanding distributions: COUNT DISTINCT, NULL rates, MIN/MAX, date ranges. Essential before building analytics.", "icon": "analytics"},
])


PROMPT_2_1 = """I'm a VIZIO platform analyst. I need to understand the data across these 2 databases: VIZIO_STREAMING and VIZIO_DEVICES.

1. List all tables across both databases with their row counts and column counts
2. For each database, summarize what kind of data it holds (based on table/column names)
3. Identify the common join keys across databases (e.g., which columns appear in multiple tables like OEM_BRAND, DATE, MODEL_NAME, SERIES, CHIPSET)
4. What date range does each table cover?

Present this as a clear data catalog I can reference throughout the lab."""

render_prompt("Prompt 2.1", "Discover the Data Landscape", PROMPT_2_1)

render_fallback_sql("List all tables", """SELECT table_catalog as database_name, table_schema, table_name, row_count, column_count
FROM VIZIO_STREAMING.INFORMATION_SCHEMA.TABLES WHERE table_schema != 'INFORMATION_SCHEMA'
UNION ALL
SELECT table_catalog, table_schema, table_name, row_count, column_count
FROM VIZIO_DEVICES.INFORMATION_SCHEMA.TABLES WHERE table_schema != 'INFORMATION_SCHEMA'
ORDER BY 1, 2, 3;""")

render_explanation("What this prompt does", """
Uses Cortex Code as a **data discovery** tool across two databases. Instead of manually querying each INFORMATION_SCHEMA, you describe what you need and Cortex Code handles it.

**Key insight**: VIZIO_STREAMING covers the WatchFree+ business, VIZIO_DEVICES covers the TV fleet. The join keys (OEM_BRAND, SERIES, CHIPSET, MODEL_NAME, date columns) connect them. Understanding these joins is essential before building cross-database views.
""")


PROMPT_2_2 = """Run a data quality check across the VIZIO databases. For the key tables, tell me:

1. VIZIO_STREAMING.WFP.AGG_WFP_GLOBAL_KPIS_ROLLING_30_DAY: date range, any NULL dates, min/max WFP_TOKENS
2. VIZIO_STREAMING.WFP.AGG_WFP_LIVE_AND_AVOD_REVENUE_ROLLING_30_DAYS: date range, min/max revenue values, any negative revenue rows?
3. VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES: date range, distinct MODEL_NAMEs, any models with GROSS_CHURN_RATE1M > 0.10 (high churn)?
4. VIZIO_DEVICES.FLEET.AGG_TV_ATTRIBUTE_CURRENT_MV: distinct SERIES values, OEM_BRAND distribution, distinct FIRMWARE versions
5. VIZIO_DEVICES.APPS.AGG_APP_DEVICES_LAUNCHES_SOURCES: top 10 apps by total LAUNCHES, distinct SOURCEs

Summarize as a data quality report."""

render_prompt("Prompt 2.2", "Data Quality Assessment", PROMPT_2_2)

render_fallback_sql("Quick quality checks", """-- KPI date range and token range
SELECT MIN(date), MAX(date), MIN(wfp_tokens), MAX(wfp_tokens)
FROM VIZIO_STREAMING.WFP.AGG_WFP_GLOBAL_KPIS_ROLLING_30_DAY;

-- Revenue range
SELECT MIN(event_date), MAX(event_date), MIN(wfp_live_revenue), MAX(wfp_live_revenue)
FROM VIZIO_STREAMING.WFP.AGG_WFP_LIVE_AND_AVOD_REVENUE_ROLLING_30_DAYS;

-- High-churn models
SELECT model_name, series, AVG(gross_churn_rate1m) as avg_churn
FROM VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES
GROUP BY 1, 2 HAVING avg_churn > 0.08 ORDER BY avg_churn DESC;

-- Fleet composition
SELECT series, oem_brand, COUNT(*) as device_count
FROM VIZIO_DEVICES.FLEET.AGG_TV_ATTRIBUTE_CURRENT_MV
GROUP BY 1, 2 ORDER BY 3 DESC;

-- Top apps
SELECT app, SUM(launches) as total_launches
FROM VIZIO_DEVICES.APPS.AGG_APP_DEVICES_LAUNCHES_SOURCES
GROUP BY 1 ORDER BY 2 DESC LIMIT 10;""")

render_explanation("What this prompt does", """
Checks data quality across the most important tables:

- **Completeness**: Are dates continuous? Any NULLs in key columns?
- **Reasonableness**: Are token counts, revenue, and churn rates in expected ranges?
- **Distribution**: What's the app landscape? Which models have problems?
- **Trends**: Are active accounts growing as expected?

**Why this matters**: Building analytics on unreliable data gives wrong answers. Discovery catches issues before they propagate into views and dashboards.
""")


PROMPT_2_3 = """Help me understand the business patterns across WatchFree+ and the device fleet:

1. What are the top 5 WatchFree+ live channels by total session length? (VIZIO_STREAMING.WFP.AGG_WFP_LIVE_CHANNEL_SUMMARY_WITH_CHANNEL_NAMES)
2. How has WFP revenue trended monthly — show total of live + AVOD revenue by month? (VIZIO_STREAMING.WFP.AGG_WFP_LIVE_AND_AVOD_REVENUE_ROLLING_30_DAYS)
3. Which TV series (V, M, P, Quantum, OLED) has the most active devices? Which has the highest churn? (VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES)
4. What's the VIZIO vs ONN brand split in the device fleet? (VIZIO_DEVICES.FLEET.AGG_TV_ATTRIBUTE_CURRENT_MV)
5. Top 3 AVOD genres by total viewing minutes? (VIZIO_STREAMING.WFP.AGG_WFP_AVOD_CONTENT_SUMMARY_WITH_METADATA_V2)

Show results as tables and describe what you see."""

render_prompt("Prompt 2.3", "Business Pattern Analysis", PROMPT_2_3)

render_fallback_sql("Business patterns", """-- Top WFP channels
SELECT epg_channel_name, ROUND(SUM(channel_session_length) / 60, 1) as viewing_hours
FROM VIZIO_STREAMING.WFP.AGG_WFP_LIVE_CHANNEL_SUMMARY_WITH_CHANNEL_NAMES
GROUP BY 1 ORDER BY 2 DESC LIMIT 5;

-- Monthly WFP revenue
SELECT DATE_TRUNC('month', event_date) AS month,
       ROUND(SUM(wfp_live_revenue + wfp_avod_revenue), 2) AS total_revenue
FROM VIZIO_STREAMING.WFP.AGG_WFP_LIVE_AND_AVOD_REVENUE_ROLLING_30_DAYS
GROUP BY 1 ORDER BY 1;

-- Series device count and churn
SELECT series, SUM(active_devices) as total_active, ROUND(AVG(gross_churn_rate1m), 4) as avg_churn
FROM VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES
WHERE month = (SELECT MAX(month) FROM VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES)
GROUP BY 1 ORDER BY 2 DESC;

-- Brand split
SELECT oem_brand, COUNT(*) as devices
FROM VIZIO_DEVICES.FLEET.AGG_TV_ATTRIBUTE_CURRENT_MV
GROUP BY 1;

-- AVOD genres
SELECT genre, ROUND(SUM(duration_mins), 0) as total_mins
FROM VIZIO_STREAMING.WFP.AGG_WFP_AVOD_CONTENT_SUMMARY_WITH_METADATA_V2
GROUP BY 1 ORDER BY 2 DESC LIMIT 3;""")

render_explanation("What this prompt does", """
Transitions from technical profiling to **business-level understanding**:

1. **Channel popularity**: Which content drives WFP engagement?
2. **Revenue trend**: Is the platform business growing?
3. **Series performance**: Which product lines are healthy vs at-risk?
4. **Brand mix**: How big is ONN relative to VIZIO?
5. **Content preferences**: What do viewers want to watch?

This is the discovery workflow an analyst follows when working with a new dataset — ask questions first, build queries later.
""")


render_key_concepts([
    {"term": "Cross-Database Discovery", "definition": "Querying INFORMATION_SCHEMA across multiple databases to build a unified data catalog. Snowflake's fully qualified naming (DATABASE.SCHEMA.TABLE) makes this seamless."},
    {"term": "Data Profiling", "definition": "Examining data to understand distributions, completeness, and quality before building analytics. Includes NULL checks, range validation, and pattern discovery."},
])

render_domain_glossary([
    {"term": "Rolling 30-Day Metric", "definition": "A metric calculated over a sliding 30-day window. Each day's value represents the sum/average of the preceding 30 days. Smooths daily noise while staying responsive to trends."},
    {"term": "FAST Channels", "definition": "Free Ad-Supported Streaming Television. Live linear channels (like traditional cable) delivered over the internet for free with ads. WatchFree+ is VIZIO's FAST service."},
])

render_what_you_built([
    "Data catalog across both databases — tables, row counts, join keys",
    "Data quality report identifying issues and validating ranges",
    "Business pattern analysis: top channels, revenue trends, series performance, content preferences",
])
