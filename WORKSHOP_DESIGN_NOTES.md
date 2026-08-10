# Ross Inventory Workshop — Design & Decision Log

## Overview

Built a 3-hour hands-on lab for 30 Ross Stores analysts focused on **Store Inventory Optimization**.  
Format: Streamlit guide app with numbered prompts for Cortex Code (same as `retail_ai_short_workshop`).  
Location: `ross_inventory_workshop/`

---

## Initial Scoping

### Audience
- 30 analysts from Ross Stores who work for Ross Stires
- Use Snowflake daily but may not know which features to use for what
- Goal: expose them to Cortex Code, Dynamic Tables, Streamlit, Semantic Views, Cortex Search, and Cortex Agents via CoWork

### Baseline Reference
Used `retail_ai_short_workshop` (90-min, 7 sessions, Cortex AI focus) as the structural template.

### Features Chosen for Workshop
1. **Cortex Code** (Snowsight UI) for data discovery
2. **Analytics-ready datasets** (views, dynamic tables)
3. **Streamlit app** with what-if scenarios and save-to-Snowflake
4. **Semantic View, Cortex Search, and Agent** for CoWork conversational BI

---

## Workshop Structure (9 Sessions)

| # | Session | Duration | What's Built |
|---|---------|----------|--------------|
| 1 | Foundation & Data Setup | 20 min | DB, schemas, WH, 9 raw tables |
| 2 | Data Discovery | 20 min | Exploratory analysis via Cortex Code |
| 3 | Analytics-Ready Views | 25 min | Inventory health, seasonal sales, store KPIs |
| 4 | Dynamic Tables | 25 min | Replenishment signals + stockout risk (chained pipeline) |
| — | Break | 10 min | — |
| 5 | Streamlit What-If App | 30 min | Scenario planner with save + health overview tab |
| 6 | Semantic View & Analyst | 25 min | Natural language to SQL |
| 7 | Cortex Search | 20 min | Knowledge base + RAG pipeline |
| 8 | Cortex Agent & CoWork | 25 min | Multi-tool agent (Analyst + Search + UDF) |
| 9 | Try It Yourself | Remaining | Extend Streamlit app with regional reports |

---

## Key Design Decisions

### Fiscal Calendar (Feb 1 start)
- Ross Stores fiscal year starts February 1st
- Q1 = Feb-Apr, Q2 = May-Jul, Q3 = Aug-Oct, Q4 = Nov-Jan
- Seasons: spring (Feb-Apr), summer (May-Jul), fall/BTS (Aug-Oct), holiday (Nov-Jan)
- Calendar table covers 2024-02-01 through 2026-01-31

### Sample Data — EMERGENCY/URGENT Signals
- Inventory snapshots: 30+ rows with on_hand_qty = 0, 50+ rows with on_hand_qty < 10
- Stockout events: 20 active (NULL end_date), repeat offenders on same store/product
- Ensures dynamic tables and views show CRITICAL/HIGH/EMERGENCY items without luck

### Streamlit App — Warehouse Mode (Trial Account Limitation)
- Trial accounts don't support container mode for Streamlit
- Cortex Code deploys apps defaulting to container mode
- **User must manually switch** to Warehouse mode after every deployment:
  - Open app → ⋮ menu → App Settings → Run on: Warehouse → Save
- Code pattern: `get_active_session()` + `session.sql()` (NOT `st.connection()`)

### Prompt 6.4 (CoWork) Removed
- Original design had CoWork demo in Session 6 (Semantic View)
- Removed because Agent doesn't exist yet at that point
- CoWork is demonstrated in Session 8 after the agent is created

### RAG Model Choice
- Prompt 7.3 uses `claude-sonnet-5` for RAG generation

### Session 9 — Try It Yourself
- Open-ended challenge: add regional/store reports tab to Streamlit app
- Provides example prompt but no step-by-step
- Includes other exploration ideas (trend charts, alert summaries, multi-store simulation)

---

## Data Model

### Dimension Tables (RAW schema)
| Table | Rows | Key Columns |
|-------|------|-------------|
| PRODUCTS | 50 | product_id, category, brand, unit_cost, retail_price, pack_size, reorder_point, lead_time_days |
| STORES | 25 | store_id, store_name, city, state, region, district, format |
| EMPLOYEES | 40 | employee_id, role, store_id |
| CALENDAR | 730 | cal_date, fiscal_quarter, fiscal_period, fiscal_year, season, event_name |

### Fact Tables (RAW schema)
| Table | Rows | Purpose |
|-------|------|---------|
| DAILY_SALES | 5000 | Transaction-level with seasonal patterns |
| INVENTORY_SNAPSHOTS | 3000 | Weekly point-in-time stock levels |
| PURCHASE_ORDERS | 500 | Supply side — orders, deliveries, status |
| STOCKOUT_EVENTS | 200 | When/why shelves went empty |
| REPLENISHMENT_POLICIES | 50 | Text policy documents (for Search) |

### Analytics Layer (ANALYTICS schema)
- `INVENTORY_HEALTH` — view with days_of_supply, stockout_risk classification
- `SALES_WITH_SEASONALITY` — view with rolling averages, calendar context
- `STORE_PERFORMANCE_SUMMARY` — view with store-level KPIs
- `DT_REPLENISHMENT_SIGNALS` — dynamic table (TARGET_LAG = 1 hour)
- `DT_STOCKOUT_RISK_SCORE` — dynamic table (TARGET_LAG = DOWNSTREAM)
- `INVENTORY_OPTIMIZATION_SV` — semantic view for Cortex Analyst
- `CALCULATE_REORDER_QUANTITY` — UDF (agent tool)
- `INVENTORY_OPS_AGENT` — Cortex Agent

### Apps Layer (APPS schema)
- `SAVED_SCENARIOS` — table for what-if results
- `INVENTORY_WHATIF_PLANNER` — Streamlit app

---

## Files Created

```
ross_inventory_workshop/
├── .streamlit/config.toml
├── static/ (fonts + logos)
├── components.py
├── streamlit_app.py
├── requirements.txt
└── app_pages/
    ├── home.py
    ├── getting_started.py
    ├── agenda.py
    ├── session_01.py  (Foundation & Data Setup)
    ├── session_02.py  (Data Discovery)
    ├── session_03.py  (Analytics-Ready Views)
    ├── session_04.py  (Dynamic Tables)
    ├── session_05.py  (Streamlit What-If App)
    ├── session_06.py  (Semantic View & Analyst)
    ├── session_07.py  (Cortex Search)
    ├── session_08.py  (Cortex Agent & CoWork)
    └── session_09.py  (Try It Yourself)
```

## Running the Guide App

```bash
cd aswinee-ai-workshop/ross_inventory_workshop
streamlit run streamlit_app.py
```

---

## Revision History

- **v1**: Initial build — 8 sessions, all features
- **v2**: Calendar year starts Feb 1, Streamlit workspace deploy + warehouse mode, ensure EMERGENCY data, remove Prompt 6.4, claude-sonnet-5 for RAG, add Session 9 (Try It Yourself)
- **v3**: Streamlit deploy flow corrected — Cortex Code deploys (defaults to container), user switches to warehouse in App Settings after each deployment
- **v4**: Prompt 5.4 changed from DT_REPLENISHMENT_SIGNALS batch query to INVENTORY_HEALTH view-based "Inventory Health Overview" tab (more reliable data availability)
