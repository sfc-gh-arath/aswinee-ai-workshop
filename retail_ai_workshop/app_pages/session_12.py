import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built, render_what_you_will_build, render_fallback_sql, render_pro_tip
from fallback_sql import FB_12_1, FB_12_2, FB_12_3, FB_12_4

render_session_header(12, "Build Apps", "3:20 - 3:40 PM", "20 min", "Streamlit retail dashboard plus a React (Next.js) web app on Snowflake")

render_what_you_will_build([
    "RETAIL_DASHBOARD - a 3-page Streamlit app on the container runtime: sales KPIs and store map, an AI chat, and customer insights",
    "A compute pool and package access through Snowflake's built-in PyPI repository (works on trial accounts)",
    "A React (Next.js) inventory app built with Cortex Code and deployed to Snowflake App Runtime at a live URL",
    "A side-by-side understanding of when to choose Streamlit vs React for a Snowflake app",
])

render_technologies_used([
    {"name": "Streamlit in Snowflake (SiS)", "description": "Deploy Python-based data apps directly within Snowflake. Apps run on the container runtime, access data natively via Snowpark, and inherit Snowflake's security model.", "icon": "web"},
    {"name": "Compute Pool", "description": "A managed pool of container nodes that powers SiS apps on the container runtime. You choose the instance family and node count; Snowflake handles provisioning.", "icon": "memory"},
    {"name": "Artifact Repository (PyPI)", "description": "snowflake.snowpark.pypi_shared_repository is Snowflake's built-in PyPI mirror. Attach it to an app to pip-install packages without an external access integration.", "icon": "inventory_2"},
    {"name": "st.connection(\"snowflake\")", "description": "The Streamlit connection API for the container runtime. .session() returns a Snowpark session that inherits the viewer's login - no credentials in code.", "icon": "terminal"},
    {"name": "Snowflake App Runtime", "description": "Runs full-stack Node.js web apps (focused on Next.js / React) inside Snowflake as an Application Service with a live, authenticated URL.", "icon": "rocket_launch"},
    {"name": "Cortex Code + snowflake-apps skill", "description": "In Cortex Code Desktop or CLI, the snowflake-apps skill scaffolds a Next.js project, wires up Snowflake data access, tests locally, and deploys with snow app deploy.", "icon": "code"},
])


st.markdown("#### :material/web: Part 1 - Streamlit app")
st.caption("Python-first data apps for dashboards and analyst tools. Built entirely from Snowsight.")

PROMPT_12_1 = """In RETAIL_AI_DEMO.RETAIL_OPS, create a Streamlit app called RETAIL_DASHBOARD that runs on the container runtime (not the legacy warehouse runtime).

First, create a compute pool for the app:
- Name: RETAIL_AI_COMPUTE_POOL
- Use the CPU_X64_S instance family
- Min and max nodes of 1

Then create the Streamlit app on that compute pool with these 3 pages:

PAGE 1 - Sales Dashboard:
- KPI cards at the top showing: Total Revenue for the latest month of data, Total Units Sold, Avg Transaction Value, Online Sales % (from SALES_TRANSACTIONS)
- A map of store locations with markers sized by revenue. Use st.pydeck_chart with a ScatterplotLayer and the latitude/longitude columns from STORES
- A bar chart of revenue by product category
- A line chart showing daily sales over the last 90 days of data
- A table of the top 10 highest stockout risk scores from LIVE_STOCKOUT_SCORES

PAGE 2 - Retail Intelligence Chat:
- A chat interface where users can type natural language questions
- Uses AI_COMPLETE() to answer questions with context from our data (cast the result to STRING)
- Shows top-selling products for the latest week in a sidebar
- Has a dropdown to select which LLM model to use (claude-sonnet-4-5, llama3.3-70b, mistral-large2)

PAGE 3 - Customer Insights:
- Summary cards: Total Reviews in the last 30 days, Avg Rating, Open Support Tickets
- A table of recent SUPPORT_TICKETS with priority color coding (urgent = red, high = orange, medium = yellow, low = green)
- A pie chart of support tickets by category

Important for container runtime:
- Package access: do NOT create an external access integration (trial accounts do not support them). Instead grant DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER to my role and set ARTIFACT_REPOSITORIES = (snowflake.snowpark.pypi_shared_repository) on the Streamlit app
- Do NOT use ROOT_LOCATION - create the app with CREATE STREAMLIT ... FROM '@stage' MAIN_FILE = 'streamlit_app.py' RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11' COMPUTE_POOL = ... QUERY_WAREHOUSE = RETAIL_AI_WH
- Create the stage with ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE') and write files to it using COPY INTO with a SELECT, for example: COPY INTO @stage/file.toml FROM (SELECT $$...$$) FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE FIELD_DELIMITER = NONE RECORD_DELIMITER = NONE ESCAPE_UNENCLOSED_FIELD = NONE FIELD_OPTIONALLY_ENCLOSED_BY = NONE) HEADER = FALSE SINGLE = TRUE OVERWRITE = TRUE
- Include a pyproject.toml in the stage with this exact structure:
  [project]
  name = "retail-ai-dashboard"
  version = "1.0.0"
  requires-python = ">=3.11"
  dependencies = ["streamlit[snowflake]>=1.50.0", "pydeck", "plotly"]
- Use st.connection("snowflake").session() for the Snowflake connection (not get_active_session)

Make it visually clean with st.columns for layout."""

render_prompt("Prompt 12.1", "Create the Streamlit App", PROMPT_12_1)
render_fallback_sql("Deploy the Streamlit app", FB_12_1)

render_explanation("What this prompt does", """
Creates a full **Streamlit in Snowflake (SiS)** application running on the **container runtime**:

**Container runtime vs warehouse runtime**:
- **Container runtime** (current): runs on a compute pool, installs packages with uv from PyPI (through an artifact repository), Python 3.11, Streamlit 1.50+
- **Warehouse runtime** (legacy): limited to the Snowflake Anaconda channel and a fixed set of Streamlit versions

**Step 1 - Compute pool**:
```sql
CREATE COMPUTE POOL RETAIL_AI_COMPUTE_POOL
  MIN_NODES = 1 MAX_NODES = 1 INSTANCE_FAMILY = CPU_X64_S;
```

**Step 2 - Package access without internet egress**: Snowflake ships a shared PyPI mirror. Grant access once and attach it to the app:
```sql
GRANT DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER TO ROLE ACCOUNTADMIN;
-- ... ARTIFACT_REPOSITORIES = (snowflake.snowpark.pypi_shared_repository)
```
External access integrations (network rule + EAI to pypi.org) also work on paid accounts, but **trial accounts reject them** with *"External access is not supported for trial accounts"*.

**Step 3 - Write files to the stage** using `COPY INTO` with a `$$`-quoted SELECT. The file format options (`FIELD_DELIMITER = NONE`, `RECORD_DELIMITER = NONE`, `ESCAPE_UNENCLOSED_FIELD = NONE`, `SINGLE = TRUE`) write the text byte-for-byte as a single file.

**Step 4 - Deploy with versioned stage syntax** (the container runtime does not support ROOT_LOCATION):
```sql
CREATE OR REPLACE STREAMLIT RETAIL_AI_DEMO.RETAIL_OPS.RETAIL_DASHBOARD
  FROM '@RETAIL_AI_DEMO.RETAIL_OPS.STREAMLIT_STAGE'
  MAIN_FILE = 'streamlit_app.py'
  RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL = RETAIL_AI_COMPUTE_POOL
  QUERY_WAREHOUSE = RETAIL_AI_WH
  ARTIFACT_REPOSITORIES = (snowflake.snowpark.pypi_shared_repository);
```

**Page 1 - Sales Dashboard** pattern:
```python
session = st.connection("snowflake").session()

@st.cache_data(ttl=600)
def q(sql):
    return session.sql(sql).to_pandas()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"${kpi.REV:,.0f}")
```

**Page 2 - Chat** uses `st.chat_input` / `st.chat_message` and calls `AI_COMPLETE(?, ?)` with bound parameters for the model and prompt.

**Page 3 - Customer Insights** colors the priority column with a pandas Styler.

**Key SiS advantages**: no data movement, inherits the viewer's role (including the masking policies from Session 3), share with `GRANT USAGE ON STREAMLIT`, and no infrastructure to manage.
""")


PROMPT_12_2 = """Show me the SQL to verify the Streamlit app and compute pool were created:

1. SHOW COMPUTE POOLS LIKE 'RETAIL_AI_COMPUTE_POOL';
2. SHOW STREAMLITS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;
3. Describe the streamlit RETAIL_DASHBOARD;

Also provide me with the direct URL to open the Streamlit app in Snowsight."""

render_prompt("Prompt 12.2", "Test the Streamlit App", PROMPT_12_2)
render_fallback_sql("Verify the Streamlit app", FB_12_2)

render_explanation("What this prompt does", """
Verification and access:

- **SHOW COMPUTE POOLS** - state (STARTING / ACTIVE / IDLE / SUSPENDED), instance family, node counts, auto-suspend
- **SHOW STREAMLITS** - every app in the schema, its owner, compute pool, and attached artifact repositories
- **DESCRIBE STREAMLIT** - main file, source location, runtime name, compute pool (not a warehouse - this confirms container runtime)

**First launch takes a few minutes** while the compute pool starts and the container installs packages; later launches are fast.

**Sharing the app**:
```sql
GRANT USAGE ON STREAMLIT RETAIL_DASHBOARD TO ROLE RETAIL_MERCHANDISER;
```
The merchandiser sees the same dashboard, but cost columns come back masked because the app runs queries as the viewer.
""")

render_pro_tip("Open, edit, and share your Streamlit app", """
- Go to **Projects » Streamlit** and select **RETAIL_DASHBOARD** to open it. The first load can take a few minutes while the container starts.
- Select **Edit** to change the code in the browser and see the app re-run instantly.
- Use the **⋮ » App settings** menu to review the compute pool, query warehouse, and artifact repository; **Share** grants other roles access.
- Go to **Compute » Compute pools** to watch **RETAIL_AI_COMPUTE_POOL** move from STARTING to ACTIVE, and suspend it after the lab to stop credit use.
""")


st.divider()
st.markdown("#### :material/rocket_launch: Part 2 - React (Next.js) app")
st.caption("Full web apps with custom UI and multi-step workflows, built with Cortex Code and deployed to Snowflake App Runtime.")

st.warning(
    "**Before you start:** React apps run on **Snowflake App Runtime**, which you build from **Cortex Code Desktop or Cortex Code CLI** "
    "(not the Snowsight Cortex Code panel). You also need Node.js 20+ and Snowflake CLI installed locally. "
    "Snowflake App Runtime is **not available on trial accounts** - if you are on a trial, follow along with the facilitator's demo.",
    icon=":material/warning:",
)

with st.container(border=True):
    st.markdown("""
**Streamlit or React?**

| | Streamlit | React (Snowflake App Runtime) |
|---|---|---|
| Language | Python | TypeScript / JavaScript |
| Best for | Dashboards, data exploration, analyst tools | Custom UI, forms, multi-step workflows, customer-facing apps |
| Built from | Snowsight, Workspaces, or any editor | Cortex Code Desktop / CLI (`snowflake-apps` skill) |
| Runs as | Streamlit object on a compute pool | Application Service with a `*.snowflakecomputing.app` URL |
| Security | Inherits Snowflake RBAC | Inherits Snowflake RBAC and SSO |
""")

PROMPT_12_3 = """/snowflake-apps Build me a React (Next.js) web app called alpine-inventory-planner for Alpine & Co. store managers, using data in RETAIL_AI_DEMO.RETAIL_OPS and the RETAIL_AI_WH warehouse.

Pages:
1. Inventory Overview - KPI cards (SKU-store combinations at risk, average days of supply, total inventory value at retail price) and a sortable, filterable table from LIVE_STOCKOUT_SCORES (store, product, category, quantity on hand, days of supply, stockout probability) with red/amber/green risk badges
2. Store Detail - a store selector (from STORES); for the selected store show revenue by category as a bar chart (SALES_TRANSACTIONS joined to PRODUCTS) and its lowest days-of-supply products
3. Reorder Assistant - a form with product category, current inventory and average daily sales that calls RETAIL_AI_DEMO.RETAIL_OPS.CALCULATE_STOCKOUT_RISK and shows the risk level and recommendation

Use the Next.js App Router with TypeScript and Tailwind, query Snowflake from server-side API routes only, and use a clean Alpine & Co. look with a navy and white theme.
Test it locally first, then deploy it to Snowflake App Runtime in RETAIL_AI_DEMO.RETAIL_OPS and give me the live URL."""

render_prompt("Prompt 12.3", "Build and Deploy a React App with Cortex Code", PROMPT_12_3)
render_fallback_sql("Scaffold and deploy from the CLI", FB_12_3, language="bash")

render_explanation("What this prompt does", """
Runs the **snowflake-apps** skill in Cortex Code Desktop or CLI (type `/` in Desktop and pick `snowflake-apps`; in the CLI use `$snowflake-apps`). The agent:

1. **Scaffolds** a Next.js project (React, TypeScript, Tailwind, App Router)
2. **Wires up Snowflake data access** in server-side API routes, so credentials never reach the browser
3. **Builds the three pages** - overview table, store detail chart, and the reorder form that calls your Session 11 UDF
4. **Tests locally** with `npm run dev`
5. **Deploys** with `snow app setup` (writes the `app.yml` manifest) and `snow app deploy`, which uploads the source, builds it remotely, and creates an **Application Service** with a stable live URL

**How the deploy works**:
| Phase | What happens |
|---|---|
| Upload | Syncs your project (minus `node_modules`, `.next`) to a workspace or stage |
| Build | A short-lived container job runs `npm install` / `npm run build`; npm registry access is allowed by default during the build |
| Deploy | Creates or alters the Application Service from the built package; the URL does not change on redeploy |

**Why React here**: the Reorder Assistant is a multi-step form with custom validation and layout - exactly the kind of interaction that is easier in React than in Streamlit.
""")

PROMPT_12_4 = """Show me the Application Service for alpine-inventory-planner in RETAIL_AI_DEMO.RETAIL_OPS: run SHOW APPLICATION SERVICES IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS, report its status and URL, and show me the app logs if it is not running."""

render_prompt("Prompt 12.4", "Verify the React App", PROMPT_12_4)
render_fallback_sql("Verify the Application Service", FB_12_4)

render_explanation("What this prompt does", """
Confirms the deployment:

- **SHOW APPLICATION SERVICES** lists the service, its status, compute pool, query warehouse, and **URL**
- Open the URL in a browser - users sign in with their Snowflake identity, and the app's queries respect their roles
- To redeploy after changes, run `snow app deploy` again (or ask Cortex Code); the URL stays the same
""")

render_pro_tip("Find your apps in Snowsight", """
- **Streamlit**: **Projects » Streamlit » RETAIL_DASHBOARD**.
- **React / App Runtime**: deployed apps surface in the same Snowflake Apps catalog as Streamlit apps - look under **Catalog » Apps**, or run `SHOW APPLICATION SERVICES` to get the live URL.
- **Containers**: go to **Monitoring » Services & jobs** to see the Application Service and the build jobs that produced it, including logs.
""")


render_key_concepts([
    {"term": "Container Runtime", "definition": "The current SiS execution environment. Apps run on a compute pool (managed container nodes) instead of a warehouse, use Python 3.11 and Streamlit 1.50+, and install packages with uv. Uses versioned stage syntax (FROM '@stage') instead of the legacy ROOT_LOCATION."},
    {"term": "Compute Pool", "definition": "A managed pool of container nodes (CREATE COMPUTE POOL). You choose an instance family (CPU_X64_S, GPU_NV_S, etc.) and min/max nodes; Snowflake handles provisioning. Multiple apps and services can share a pool."},
    {"term": "Artifact Repository", "definition": "A Snowflake-managed package source. snowflake.snowpark.pypi_shared_repository mirrors PyPI, so container-runtime apps can install packages without internet egress. Requires the SNOWFLAKE.PYPI_REPOSITORY_USER database role."},
    {"term": "pyproject.toml", "definition": "Recommended dependency file for container-runtime SiS apps: a [project] section with name, version, requires-python, and dependencies. uv generates a uv.lock file from it to pin versions."},
    {"term": "Snowflake App Runtime", "definition": "Runs Node.js web apps (focused on Next.js / React) as Application Services inside Snowflake. Deployed with snow app deploy from an app.yml manifest; end users authenticate with their Snowflake identity. Not available on trial or government-region accounts."},
    {"term": "Application Service", "definition": "The long-running Snowflake object that serves a Snowflake App Runtime app at a stable *.snowflakecomputing.app URL. Each deploy loads a new immutable package version from the app's artifact repository."},
])

render_what_you_built([
    "RETAIL_AI_COMPUTE_POOL - compute pool for container runtime apps",
    "RETAIL_DASHBOARD - 3-page Streamlit app with packages from Snowflake's PyPI repository",
    "Sales Dashboard with KPIs, store map, charts, and stockout scores",
    "AI-powered Retail Intelligence chat with model selection",
    "Customer Insights page with color-coded support tickets",
    "alpine-inventory-planner - a React (Next.js) app on Snowflake App Runtime with a live URL",
])
