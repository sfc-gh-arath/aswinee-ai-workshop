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
    session_num=1,
    title="Foundation & Data Setup",
    time_range="0:05 - 0:20",
    duration="15 min",
    building="2 source databases (11 tables), analytics workspace, customer feedback & policy data",
)

render_technologies_used([
    {"name": "Source Databases", "description": "Two VIZIO databases: VIZIO_STREAMING (WatchFree+ live/AVOD, KPIs, revenue, studios) and VIZIO_DEVICES (TV fleet, homescreen, NRC churn, app launches, OEM).", "icon": "database"},
    {"name": "Virtual Warehouses", "description": "Named compute clusters. We create a MEDIUM warehouse for this lab. Auto-suspends when idle.", "icon": "memory"},
    {"name": "Synthetic Data", "description": "We populate 11 source tables with realistic data and add customer feedback + policy documents for AI sessions.", "icon": "table_chart"},
])

st.markdown("---")
st.markdown("#### :material/bolt: Quick Setup Option — Pre-built Notebook")
with st.container(border=True):
    st.markdown("""
If you want to **skip the Cortex Code prompts** for data setup and get straight to the analytics sessions, you can use the pre-built setup notebook:

1. **Download** the notebook: [VIZIO_Lab_Setup.ipynb](https://github.com/sfc-gh-arath/aswinee-ai-workshop/blob/main/vizio_workshop/VIZIO_Lab_Setup.ipynb)
   - Click the **Download raw file** button (↓ icon) on the GitHub page
2. In Snowsight, go to **Projects → Workspaces**
3. Open your Workspace (or create one if needed)
4. **Upload** the downloaded `.ipynb` file into your Workspace
5. Open the notebook and set the warehouse to **VIZIO_LAB_WH** (or any MEDIUM+ warehouse)
6. Click **Run All** — this creates all databases, tables, and synthetic data in one go

:material/info: **First-time notebook users**: If this is your first time running a notebook in this account, Snowsight may prompt you to **create a Notebook Service**. Follow the on-screen instructions to provision it — this is a one-time setup that takes a minute or two.

After the notebook finishes, **skip to Session 2** (Data Discovery). The notebook handles everything in Prompts 1.1, 1.2, and 1.3.
""")

st.markdown("---")


PROMPT_1_1 = """Create the VIZIO source databases and tables for this lab. We need two databases focused on WatchFree+ Streaming and Device/TV Analytics.

Run the following SQL to create the structure, then confirm all tables exist:

-- DATABASE 1: VIZIO_STREAMING (WatchFree+ live channels, AVOD content, KPIs, revenue, studios)
USE ROLE ACCOUNTADMIN;
CREATE DATABASE IF NOT EXISTS VIZIO_STREAMING;
CREATE SCHEMA IF NOT EXISTS VIZIO_STREAMING.WFP;

-- DATABASE 2: VIZIO_DEVICES (TV fleet, homescreen, apps, OEM)
CREATE DATABASE IF NOT EXISTS VIZIO_DEVICES;
CREATE SCHEMA IF NOT EXISTS VIZIO_DEVICES.FLEET;
CREATE SCHEMA IF NOT EXISTS VIZIO_DEVICES.ENGAGEMENT;
CREATE SCHEMA IF NOT EXISTS VIZIO_DEVICES.APPS;
CREATE SCHEMA IF NOT EXISTS VIZIO_DEVICES.OEM;

-- Table 1: WFP Live Channel Summary
CREATE OR REPLACE TABLE VIZIO_STREAMING.WFP.AGG_WFP_LIVE_CHANNEL_SUMMARY_WITH_CHANNEL_NAMES (
    TIME_GRAIN VARCHAR(20), DATE DATE, CHANNEL_SESSION_LENGTH NUMBER(18,2),
    OS_VERSION VARCHAR(100), OEM_BRAND VARCHAR(100), BACKEND_APP_TYPE VARCHAR(100),
    CHANNEL_TYPE VARCHAR(100), AIRINGS_KEY VARCHAR(200), EPG_CHANNEL_NAME VARCHAR(500),
    IS_OTA BOOLEAN, EPG_CHANNEL_CATEGORY VARCHAR(200), EPG_CHANNEL_CATEGORY_ID VARCHAR(50),
    AFFILIATES VARCHAR(500)
);

-- Table 2: WFP AVOD Content Summary
CREATE OR REPLACE TABLE VIZIO_STREAMING.WFP.AGG_WFP_AVOD_CONTENT_SUMMARY_WITH_METADATA_V2 (
    TIME_GRAIN VARCHAR(20), DATE DATE, PLAYER_TYPE VARCHAR(100), OS_VERSION VARCHAR(100),
    MEDIA_ID VARCHAR(100), CONTENT_TITLE VARCHAR(1000), EPISODE_TITLE VARCHAR(1000),
    SEASON_EPISODE VARCHAR(100), PRODUCTION_TYPE VARCHAR(100), GENRE VARCHAR(200),
    STUDIO VARCHAR(500), SERIES_NAME VARCHAR(500), PUBLISH_DATE DATE, RATING VARCHAR(50),
    LANGUAGE VARCHAR(50), DEVICES NUMBER(18,0), DURATION_MINS NUMBER(18,2),
    AVOD_SESSIONS NUMBER(18,0), SESSION_DURATION_PER_AVOD_SESSION NUMBER(18,2),
    SESSION_DURATION_PER_TOKEN NUMBER(18,2), LAUNCHES NUMBER(18,0),
    SESSION_LENGTH NUMBER(18,2), OEM_BRAND VARCHAR(100), BACKEND_APP_TYPE VARCHAR(100)
);

-- Table 3: WFP Global KPIs Rolling 30 Day
CREATE OR REPLACE TABLE VIZIO_STREAMING.WFP.AGG_WFP_GLOBAL_KPIS_ROLLING_30_DAY (
    DATE DATE, WFP_TOKENS NUMBER(18,0), AVOD_TOKENS NUMBER(18,0),
    WFP_AND_AVOD_TOKENS NUMBER(18,0), WFP_SESSIONS NUMBER(18,0),
    AVOD_SESSIONS NUMBER(18,0), WFP_AND_AVOD_SESSIONS NUMBER(18,0),
    WFP_VIEWING_HOURS NUMBER(18,2), WFP_APP_HOURS NUMBER(18,2),
    AVOD_VIEWING_HOURS NUMBER(18,2), WFP_AND_AVOD_VIEWING_HOURS NUMBER(18,2),
    WFP_AND_AVOD_APP_HOURS NUMBER(18,2), BACKEND_APP_TYPE VARCHAR(100)
);

-- Table 4: WFP Revenue Rolling 30 Days
CREATE OR REPLACE TABLE VIZIO_STREAMING.WFP.AGG_WFP_LIVE_AND_AVOD_REVENUE_ROLLING_30_DAYS (
    EVENT_DATE DATE, WFP_LIVE_REVENUE NUMBER(18,2), WFP_AVOD_REVENUE NUMBER(18,2)
);

-- Table 5: WFP AVOD Studio Summary
CREATE OR REPLACE TABLE VIZIO_STREAMING.WFP.AGG_WFP_AVOD_STUDIO_SUMMARY (
    TIME_GRAIN VARCHAR(20), DATE DATE, STUDIO VARCHAR(500),
    DEVICES NUMBER(18,0), AVOD_SESSIONS NUMBER(18,0),
    DURATION_MINS NUMBER(18,2), LAUNCHES NUMBER(18,0)
);

-- Table 6: TV Attributes Current
CREATE OR REPLACE TABLE VIZIO_DEVICES.FLEET.AGG_TV_ATTRIBUTE_CURRENT_MV (
    ESN VARCHAR(100), DIID VARCHAR(100), SOC VARCHAR(50), CHIPSET VARCHAR(50),
    MODEL_NAME VARCHAR(200), RJ45_MAC VARCHAR(50), FIRMWARE VARCHAR(200),
    SERIES VARCHAR(100), SIZE VARCHAR(20), TOKEN VARCHAR(200),
    OEM_BRAND VARCHAR(100), VIEWING VARCHAR(50), IP_ADDRESS VARCHAR(50),
    VERSION_SCPL VARCHAR(100), CONFIG VARCHAR(200), BINARY_ACR VARCHAR(20),
    BINARY_AIRPLAY VARCHAR(20), BINARY_APPLETV VARCHAR(20),
    BINARY_BLUETOOTH VARCHAR(20), BINARY_COBALT VARCHAR(20),
    BINARY_CONJURE VARCHAR(20), BINARY_DAI VARCHAR(20),
    BINARY_VIZIOOS VARCHAR(20), BINARY_VIZIONDK VARCHAR(20),
    BINARY_SCPL VARCHAR(20), RETAILER_CODE VARCHAR(50),
    RETAILER_NAME VARCHAR(200), DNDELIVERYCUSTOMERCOMPLETED VARCHAR(50),
    OS_VERSION VARCHAR(100)
);

-- Table 7: Homescreen Summary with TV Attributes
CREATE OR REPLACE TABLE VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_SUMMARY_WITH_TV_ATTRIBUTES (
    TIME_GRAIN VARCHAR(20), DATE DATE, CLIENTTYPE VARCHAR(100),
    SOC VARCHAR(50), CHIPSET VARCHAR(50), MODEL_NAME VARCHAR(200),
    SERIES VARCHAR(100), SIZE VARCHAR(20), LAUNCH_YEAR INTEGER,
    DEVICES NUMBER(18,0), VIEWING_MINUTES NUMBER(18,2),
    AVG_VIEWING_MINUTES NUMBER(18,2), MEDIAN_VIEWING_MINUTES NUMBER(18,2),
    OEM_BRAND VARCHAR(100)
);

-- Table 8: Homescreen NRC (New/Recurring/Churn) with TV Attributes
CREATE OR REPLACE TABLE VIZIO_DEVICES.ENGAGEMENT.AGG_HOMESCREEN_NRC_WITH_TV_ATTRIBUTES (
    MONTH DATE, SOC VARCHAR(50), CHIPSET VARCHAR(50), MODEL_NAME VARCHAR(200),
    SERIES VARCHAR(100), SIZE VARCHAR(20), LAUNCH_YEAR INTEGER,
    DISPLAY_TECHNOLOGY VARCHAR(100), ACTIVE_DEVICES NUMBER(18,0),
    NEW_DEVICES NUMBER(18,0), RECURRING_DEVICES NUMBER(18,0),
    RETURNING_DEVICES NUMBER(18,0), CHURN_1M_DEVICES NUMBER(18,0),
    CHURN_6M_DEVICES NUMBER(18,0), ACTIVE_VIEWING_MINUTES NUMBER(18,2),
    NEW_VIEWING_MINUTES NUMBER(18,2), RECURRING_VIEWING_MINUTES NUMBER(18,2),
    RETURNING_VIEWING_MINUTES NUMBER(18,2), PREVIOUS_MONTH_ACTIVE NUMBER(18,0),
    GROSS_CHURN_RATE1M NUMBER(18,6), RETURN_RATE NUMBER(18,6),
    NET_CHURN1M NUMBER(18,6), OEM_BRAND VARCHAR(100)
);

-- Table 9: App Devices Launches Sources
CREATE OR REPLACE TABLE VIZIO_DEVICES.APPS.AGG_APP_DEVICES_LAUNCHES_SOURCES (
    TIME_GRAIN VARCHAR(20), ACTIVITY_DATE DATE, CLIENTTYPE VARCHAR(100),
    SOURCE VARCHAR(200), APP VARCHAR(500), SOC VARCHAR(50), CHIPSET VARCHAR(50),
    MODEL_NAME VARCHAR(200), SERIES VARCHAR(100), SIZE VARCHAR(20),
    VOD_TYPE VARCHAR(100), MONETIZATION_TYPE VARCHAR(100),
    DEVICES NUMBER(18,0), LAUNCHES NUMBER(18,0), OEM_BRAND VARCHAR(100)
);

-- Table 10: OEM Launch Devices Cumulative
CREATE OR REPLACE TABLE VIZIO_DEVICES.OEM.AGG_OEM_LAUNCH_DEVICES_CUMULATIVE (
    ACTIVITY_DATE DATE, OEM_BRAND VARCHAR(100),
    SCTV_NEW_USERS NUMBER(18,0), WFP_NEW_USERS NUMBER(18,0),
    AVOD_NEW_USERS NUMBER(18,0), AUDIT_UPDATE_TS TIMESTAMP_NTZ,
    MODEL VARCHAR(200)
);

-- Table 11: App Metadata (Lookup)
CREATE OR REPLACE TABLE VIZIO_DEVICES.APPS.MAPPING_APP_METADATA (
    CURATED_APP_NAME VARCHAR(500), ALIAS_APP_NAME VARCHAR(500),
    APP_ID VARCHAR(100), NAME_SPACE VARCHAR(200), VOD_TYPE VARCHAR(100),
    MONETIZATION_TYPE VARCHAR(100), DEPRECATED BOOLEAN, IR_CODE VARCHAR(50),
    CURRENT_ROW BOOLEAN, LAUNCH_DATE DATE, EFFECTIVE_DATE DATE, END_DATE DATE
);

-- Grant access
GRANT USAGE ON DATABASE VIZIO_STREAMING TO ROLE PUBLIC;
GRANT USAGE ON ALL SCHEMAS IN DATABASE VIZIO_STREAMING TO ROLE PUBLIC;
GRANT SELECT ON ALL TABLES IN DATABASE VIZIO_STREAMING TO ROLE PUBLIC;
GRANT USAGE ON DATABASE VIZIO_DEVICES TO ROLE PUBLIC;
GRANT USAGE ON ALL SCHEMAS IN DATABASE VIZIO_DEVICES TO ROLE PUBLIC;
GRANT SELECT ON ALL TABLES IN DATABASE VIZIO_DEVICES TO ROLE PUBLIC;

After running, list all tables in both databases with row counts to confirm."""

render_prompt("Prompt 1.1", "Create Source Databases & Tables", PROMPT_1_1)

render_fallback_sql("Create source databases", """-- The full DDL is in the prompt above.
-- Copy the entire SQL block from Prompt 1.1 and run it in a worksheet.
-- Verify with:
SELECT 'VIZIO_STREAMING' AS db, table_schema, table_name
FROM VIZIO_STREAMING.INFORMATION_SCHEMA.TABLES WHERE table_schema != 'INFORMATION_SCHEMA'
UNION ALL
SELECT 'VIZIO_DEVICES', table_schema, table_name
FROM VIZIO_DEVICES.INFORMATION_SCHEMA.TABLES WHERE table_schema != 'INFORMATION_SCHEMA'
ORDER BY 1, 2, 3;""")

render_explanation("What this prompt does", """
Creates VIZIO's data structure focused on two domains:

| Database | Schema(s) | Tables | Focus |
|----------|-----------|--------|-------|
| **VIZIO_STREAMING** | WFP | 5 | WatchFree+ live channels, AVOD content, global KPIs, revenue, studio summary |
| **VIZIO_DEVICES** | FLEET, ENGAGEMENT, APPS, OEM | 6 | TV fleet attributes, homescreen engagement, NRC churn, app launches, OEM cumulative, app metadata |

**Total: 11 tables across 2 databases and 5 schemas.**
""")


PROMPT_1_2 = """Now create an analytics workspace and populate the source tables with synthetic data:

1. Create database VIZIO_ANALYTICS_LAB with schemas: ANALYTICS and AI_OBJECTS
2. Create warehouse VIZIO_LAB_WH (size MEDIUM, auto_suspend = 300, auto_resume = true)

3. Populate ALL 11 source tables with realistic synthetic data. Key requirements:
   - Date ranges: 2024-01-01 through 2025-09-30

   VIZIO_STREAMING tables:
   - AGG_WFP_LIVE_CHANNEL_SUMMARY: 2000 rows. Channels: NBC, CBS, ABC, Fox, CNN, ESPN, HGTV, Comedy Central, Food Network, Discovery, TLC, Hallmark, BET, Nickelodeon, MTV. OEM_BRAND: 'VIZIO' and 'ONN'. TIME_GRAIN = 'daily'. CHANNEL_SESSION_LENGTH between 5 and 180 minutes. EPG_CHANNEL_CATEGORY: News, Sports, Entertainment, Lifestyle, Kids.
   - AGG_WFP_AVOD_CONTENT_SUMMARY: 1500 rows. Real-sounding titles. Genres: Drama, Comedy, Action, Documentary, Kids, Horror, Thriller, Romance, Sci-Fi. Studios: Lionsgate, MGM, Paramount, Sony, A24, indie, Magnolia. AVOD_SESSIONS and DURATION_MINS should be proportional. Include OEM_BRAND mix.
   - AGG_WFP_GLOBAL_KPIS_ROLLING_30_DAY: 600 rows daily. WFP_TOKENS growing from ~8M to ~11M. WFP_VIEWING_HOURS growing proportionally. Include BACKEND_APP_TYPE values.
   - AGG_WFP_LIVE_AND_AVOD_REVENUE: 600 rows daily. WFP_LIVE_REVENUE ~$50K-$120K/day. WFP_AVOD_REVENUE ~$30K-$80K/day. Show growth trend.
   - AGG_WFP_AVOD_STUDIO_SUMMARY: 500 rows. Top studios by duration and sessions.

   VIZIO_DEVICES tables:
   - FLEET.AGG_TV_ATTRIBUTE_CURRENT: 500 rows. Series: V-Series, M-Series, P-Series, Quantum, OLED. Sizes: 32, 40, 43, 50, 55, 65, 75. Mix of VIZIO and ONN brands. Include realistic FIRMWARE versions and BINARY_* feature flags (TRUE/FALSE).
   - ENGAGEMENT.AGG_HOMESCREEN_SUMMARY: 800 rows. Daily grain. VIEWING_MINUTES between 10 and 300. Higher for larger screens.
   - ENGAGEMENT.AGG_HOMESCREEN_NRC: 400 rows monthly. GROSS_CHURN_RATE1M between 0.02 and 0.15. V-Series 32" should show HIGHER churn (~0.10-0.15). P-Series 65" should show LOWER churn (~0.02-0.04). Include realistic NRC breakdowns.
   - APPS.AGG_APP_DEVICES_LAUNCHES_SOURCES: 3000 rows. Apps: Netflix, Hulu, Disney+, Max, Peacock, Paramount+, YouTube, Apple TV+, Amazon Prime, Tubi, Pluto TV, WatchFree+. Sources: homescreen, voice, search, deep_link, cast. Netflix and YouTube should dominate.
   - OEM.AGG_OEM_LAUNCH_DEVICES_CUMULATIVE: 300 rows daily. Cumulative new users growing.
   - APPS.MAPPING_APP_METADATA: 30 rows. One row per app with VOD_TYPE (SVOD/AVOD/TVOD/FAST) and MONETIZATION_TYPE. CURRENT_ROW = TRUE.

Execute all INSERTs and show row counts for all 11 tables."""

render_prompt("Prompt 1.2", "Populate Source Data & Create Analytics Workspace", PROMPT_1_2)

render_fallback_sql("Create analytics workspace", """CREATE DATABASE IF NOT EXISTS VIZIO_ANALYTICS_LAB;
CREATE SCHEMA IF NOT EXISTS VIZIO_ANALYTICS_LAB.ANALYTICS;
CREATE SCHEMA IF NOT EXISTS VIZIO_ANALYTICS_LAB.AI_OBJECTS;
CREATE WAREHOUSE IF NOT EXISTS VIZIO_LAB_WH
    WITH WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

-- Data population requires many INSERT statements.
-- Use Cortex Code to generate them, or ask your facilitator for a pre-populated script.""")

render_explanation("What this prompt does", """
Two things happen here:

1. **Analytics workspace**: VIZIO_ANALYTICS_LAB database with ANALYTICS and AI_OBJECTS schemas
2. **Synthetic data**: Fills all 11 tables with realistic data reflecting key patterns:
   - **WFP growth**: Tokens and revenue trending upward (~8M to ~11M active viewers)
   - **Churn variation**: V-Series 32" has high churn (budget customers), P-Series 65" has low churn (premium loyal)
   - **App ecosystem**: Netflix and YouTube dominate, with a long tail of other services
   - **OEM mix**: Both VIZIO and ONN branded devices
""")


PROMPT_1_3 = """Now create two additional tables for the AI sessions:

1. VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK — 150 rows of product reviews. Columns:
   - feedback_id (NUMBER)
   - feedback_date (DATE)
   - source (VARCHAR: amazon, bestbuy, vizio_com, reddit, twitter)
   - device_series (VARCHAR: V-Series, M-Series, P-Series, Quantum, OLED)
   - device_size (VARCHAR: 32, 43, 50, 55, 65, 75)
   - rating (NUMBER 1-5)
   - feedback_text (VARCHAR 100-400 words)
   - feedback_type (VARCHAR: review, complaint, feature_request, praise)
   Include: ~40% positive (great picture, love WatchFree+, easy setup), ~30% negative (WiFi drops, remote lag, app crashes, WFP buffering), ~20% feature requests (better voice search, more WFP channels, Dolby Vision support), ~10% mixed.

2. VIZIO_ANALYTICS_LAB.AI_OBJECTS.VIZIO_KNOWLEDGE_BASE — 40 rows of policy/FAQ docs. Columns:
   - doc_id (NUMBER)
   - title (VARCHAR)
   - content (VARCHAR 200-500 words)
   - category (VARCHAR: watchfree_plus, device_specs, troubleshooting, smartcast_platform, firmware, app_ecosystem, privacy)
   Cover: WFP channel onboarding, firmware update cadence, app certification, homescreen curation, ACR opt-out, device warranty, SmartCast OS versions, OEM partnership guidelines.

Execute and verify row counts."""

render_prompt("Prompt 1.3", "Create Feedback & Knowledge Base Tables", PROMPT_1_3)

render_fallback_sql("Create text data tables", """CREATE OR REPLACE TABLE VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK (
    feedback_id NUMBER, feedback_date DATE, source VARCHAR(100),
    device_series VARCHAR(100), device_size VARCHAR(20),
    rating NUMBER, feedback_text VARCHAR(5000), feedback_type VARCHAR(50)
);

CREATE OR REPLACE TABLE VIZIO_ANALYTICS_LAB.AI_OBJECTS.VIZIO_KNOWLEDGE_BASE (
    doc_id NUMBER, title VARCHAR(500),
    content VARCHAR(10000), category VARCHAR(100)
);

-- Use Cortex Code to populate with realistic synthetic data""")

render_explanation("What this prompt does", """
Creates text-heavy tables for AI sessions:

- **CUSTOMER_FEEDBACK**: Product reviews for sentiment analysis, topic classification, and feature extraction (Session 5)
- **VIZIO_KNOWLEDGE_BASE**: Internal policy documents for Cortex Search and RAG (Session 6). Becomes one of the Agent's tools in Session 7.
""")


render_key_concepts([
    {"term": "Two-Database Architecture", "definition": "VIZIO_STREAMING covers the WatchFree+ business (content, channels, KPIs, revenue). VIZIO_DEVICES covers the hardware fleet (TV attributes, engagement, apps, OEM). The ANALYTICS workspace joins across both."},
    {"term": "OEM Brand Dimension", "definition": "VIZIO sells TVs under VIZIO (premium) and ONN (Walmart budget). OEM_BRAND appears across most tables and is critical for segmented analysis."},
    {"term": "Token vs Account", "definition": "A token = a unique device. An account = a user (may own multiple TVs). WFP_TOKENS measures device-level engagement; useful for platform analytics."},
])

render_domain_glossary([
    {"term": "WatchFree+ (WFP)", "definition": "VIZIO's free ad-supported streaming service. Includes live linear channels (like cable) and AVOD (ad-supported video on demand). Major revenue driver for the platform business."},
    {"term": "SmartCast", "definition": "VIZIO's smart TV operating system. Provides the homescreen, built-in apps, casting (Chromecast, AirPlay), and the WatchFree+ service."},
    {"term": "NRC (New/Recurring/Churn)", "definition": "Cohort analysis: each month, devices are New (first seen), Recurring (active again), Returning (came back after absence), or Churned (stopped). Key for device lifecycle understanding."},
    {"term": "AVOD", "definition": "Ad-Supported Video On Demand. Free content funded by ads. Contrasted with SVOD (subscription, like Netflix) and TVOD (transactional, pay-per-view)."},
    {"term": "Inscape / ACR", "definition": "Automatic Content Recognition — identifies what's playing on screen (including cable). Used for audience measurement. Privacy-regulated with opt-in/opt-out."},
])

render_what_you_built([
    "VIZIO_STREAMING database — 5 WatchFree+ tables with synthetic data",
    "VIZIO_DEVICES database — 6 device/TV analytics tables with synthetic data",
    "VIZIO_ANALYTICS_LAB database with ANALYTICS and AI_OBJECTS schemas",
    "VIZIO_LAB_WH warehouse (MEDIUM size)",
    "CUSTOMER_FEEDBACK table (150 reviews) and VIZIO_KNOWLEDGE_BASE (40 policy docs)",
])
