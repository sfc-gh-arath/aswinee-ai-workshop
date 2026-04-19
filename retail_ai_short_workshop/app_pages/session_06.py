import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(6, "Building Agentic Systems with Cortex Agent API", "1:15 - 1:30", "15 min", "Cortex Agent with Analyst + Search + custom tools")

render_technologies_used([
    {"name": "Cortex Agent (CREATE AGENT)", "description": "An orchestrating AI that plans tasks, selects tools (Analyst, Search, custom), executes them, reflects on results, and generates responses. Created as a first-class Snowflake object.", "icon": "smart_toy"},
    {"name": "Tool Orchestration", "description": "The Agent automatically routes questions to the right tool: Cortex Analyst for structured data, Cortex Search for unstructured documents, custom UDFs for business logic.", "icon": "route"},
    {"name": "Custom Tools (UDFs)", "description": "User-defined functions that extend Agent capabilities. The Agent can call any SQL UDF or stored procedure as a tool, enabling custom business logic, calculations, or external integrations.", "icon": "build"},
])


PROMPT_6_1 = """In RETAIL_AI_DEMO.RETAIL_OPS, create a Cortex Agent called RETAIL_OPS_AGENT that store operations staff can use to ask questions about both structured data and customer feedback.

It should:
- Use claude-sonnet-4-6 as the orchestration model
- Have two tools: the RETAIL_OPERATIONS_VIEW semantic view (for structured data queries) and the customer_feedback_search Cortex Search service (for customer reviews and feedback)
- Include instructions that define it as the "Alpine & Co. Retail Operations Assistant", guiding it to use the right tool for the question type — structured data tool for sales/inventory/supplier metrics, search tool for customer reviews/feedback/complaints
- Mention key domain context in the instructions: national apparel and footwear retailer with 120+ stores, peak seasons are Nov-Dec (holiday) and August (back-to-school), private labels Summit (activewear) and Basecamp (casual basics), and support for English and Spanish
- Include 3-4 sample questions that span both tools (e.g. sales by category, customer feedback on Summit products, inventory levels, complaint trends)

Execute and show confirmation."""

render_prompt("Prompt 6.1", "Create the Cortex Agent", PROMPT_6_1)

render_explanation("What this prompt does", """
Creates a **Cortex Agent** — an AI orchestrator that combines multiple data tools:

**CREATE AGENT anatomy**:
- **MODEL**: The LLM used for orchestration (`claude-sonnet-4-6`)
- **TOOLS**: Cortex Search (for feedback) + Semantic View (for structured SQL queries)
- **INSTRUCTIONS**: System prompt shaping behavior, tool routing, and domain context
- **SAMPLE_QUESTIONS**: Seed questions shown to users in the UI

**How the Agent orchestrates**:
1. **Planning**: Receives user question, decides which tool(s) to use
2. **Tool execution**: Calls Analyst (generates + runs SQL) or Search (retrieves reviews)
3. **Reflection**: Evaluates results — are they sufficient? Need another tool?
4. **Response**: Synthesizes a natural language answer from tool outputs

**Agent vs. RAG**: The RAG pipeline from Session 4 was a single retrieve-then-generate pipeline. An Agent is smarter — it can decide to use Search, then Analyst, then Search again based on the question.
""")


PROMPT_6_2 = """Test our RETAIL_OPS_AGENT by running queries through SNOWFLAKE.CORTEX.DATA_AGENT_RUN(). This function lets us call the agent via SQL and get a JSON response.

Run these four queries one at a time, parsing the response with TRY_PARSE_JSON:

1. Structured data query: "What are the top-selling product categories this quarter and which stores are driving the most revenue?"
2. Unstructured search query: "What are customers saying about the quality of Summit activewear products?"
3. Mixed query (should use both tools): "Which product categories have both the highest sales AND the most customer complaints? Is there a correlation?"
4. Spanish query: "Cuales son los productos mas vendidos en las tiendas de California?"

For each, show the full response including which tools the agent chose to use."""

render_prompt("Prompt 6.2", "Test the Agent", PROMPT_6_2)

render_explanation("What this prompt does", """
Tests the Agent via `SNOWFLAKE.CORTEX.DATA_AGENT_RUN()` — a SQL function that runs an existing agent object and returns JSON:

```sql
SELECT TRY_PARSE_JSON(
  SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'RETAIL_AI_DEMO.RETAIL_OPS.RETAIL_OPS_AGENT',
    $${ "messages": [{ "role": "user", "content": [{ "type": "text", "text": "your question here" }] }] }$$
  )
) AS resp;
```

**Four question types test different tool routing**:
1. **Pure structured** — routes to Cortex Analyst, generates SQL
2. **Pure unstructured** — routes to Cortex Search, retrieves reviews
3. **Mixed** — requires BOTH tools: Analyst for sales data, Search for complaints
4. **Bilingual** — Spanish question routed to English-language tools, response in Spanish
""")


PROMPT_6_3 = """In RETAIL_AI_DEMO.RETAIL_OPS, enhance our agent by adding a custom tool.

1. Create a UDF that calculates estimated stockout risk:

CREATE OR REPLACE FUNCTION RETAIL_AI_DEMO.RETAIL_OPS.CALCULATE_STOCKOUT_RISK(
    product_category VARCHAR,
    current_inventory NUMBER,
    avg_daily_sales NUMBER
)
RETURNS VARIANT
LANGUAGE SQL
AS
$$
    SELECT OBJECT_CONSTRUCT(
        'category', product_category,
        'current_inventory', current_inventory,
        'avg_daily_sales', avg_daily_sales,
        'days_of_supply', CASE WHEN avg_daily_sales > 0 THEN current_inventory / avg_daily_sales ELSE 999 END,
        'risk_level',
            CASE
                WHEN avg_daily_sales > 0 AND (current_inventory / avg_daily_sales) < 3 THEN 'HIGH'
                WHEN avg_daily_sales > 0 AND (current_inventory / avg_daily_sales) < 7 THEN 'MEDIUM'
                ELSE 'LOW'
            END,
        'recommendation',
            CASE
                WHEN avg_daily_sales > 0 AND (current_inventory / avg_daily_sales) < 3 THEN 'Immediate reorder required — contact supplier for expedited shipment and consider cross-store transfers'
                WHEN avg_daily_sales > 0 AND (current_inventory / avg_daily_sales) < 7 THEN 'Place standard reorder — monitor sell-through rate and adjust quantities for upcoming promotions'
                ELSE 'Adequate inventory — review reorder point and consider markdowns if days of supply exceeds 30'
            END
    )
$$;

2. Test the UDF with sample inputs.

3. Recreate RETAIL_OPS_AGENT to include CALCULATE_STOCKOUT_RISK as an additional tool alongside the existing Analyst and Search tools."""

render_prompt("Prompt 6.3", "Agent with Custom Tool", PROMPT_6_3)

render_explanation("What this prompt does", """
Extends the Agent with a **custom UDF tool**:

**The UDF** implements a rule-based stockout risk calculator:
- **HIGH risk**: Less than 3 days of supply
- **MEDIUM risk**: 3-7 days of supply
- **LOW risk**: 7+ days of supply

Each risk level comes with an actionable recommendation.

**How the Agent uses custom tools**: When the user asks about stockout risk, the Agent:
1. Recognizes this matches the CALCULATE_STOCKOUT_RISK function
2. Extracts parameters from the question
3. Calls the UDF with those parameters
4. Incorporates the result into its response

**This is the "agentic" pattern**: The Agent doesn't just retrieve data — it takes actions, calls functions, and orchestrates workflows. Custom tools are what make Agents truly powerful for enterprise use cases.
""")

PROMPT_6_4 = """Test the enhanced RETAIL_OPS_AGENT (now with 3 tools) using SNOWFLAKE.CORTEX.DATA_AGENT_RUN(). Run these queries that exercise the new custom tool:

1. "What is the stockout risk for sneakers if we have 50 units and sell 12 per day?"
2. "What are the current inventory levels for each category and what would the stockout risk be during holiday season with doubled demand?"
3. "For our Portland store, show me current sales performance, any customer complaints, and the stockout risk assessment for activewear."

Show the parsed JSON responses and note which tools the agent selected for each."""

render_prompt("Prompt 6.4", "Test the Enhanced Agent", PROMPT_6_4)

render_explanation("What this prompt does", """
Tests the enhanced Agent's ability to use the **new custom tool** alongside Analyst and Search:

**Query 1 - Custom tool only**: Extract parameters (category=sneakers, inventory=50, daily_sales=12) and call CALCULATE_STOCKOUT_RISK. Days of supply = 50/12 ~ 4.2 days = MEDIUM risk.

**Query 2 - Custom + Analyst**: First query current inventory levels via Analyst, then call the stockout risk UDF with doubled daily sales for each category.

**Query 3 - All three tools**: Orchestrate all three tools:
1. Analyst for Portland store sales performance
2. Search for customer complaints related to Portland
3. Custom UDF for stockout risk scoring on activewear

Watch the `tool_use` entries in the JSON response to see how the Agent plans and sequences tool calls.
""")


render_key_concepts([
    {"term": "Cortex Agent", "definition": "A first-class Snowflake object that orchestrates LLMs, Cortex Analyst, Cortex Search, and custom tools to answer complex questions. Supports planning, tool use, reflection, and multi-turn conversations."},
    {"term": "Tool Routing", "definition": "The Agent's ability to select the appropriate tool for each question or sub-task. Structured data queries -> Analyst, unstructured search -> Search, calculations -> custom UDFs."},
    {"term": "Custom Tools", "definition": "SQL UDFs or stored procedures registered as Agent tools. The Agent can call them with extracted parameters. Enables custom business logic, external integrations, and workflow automation."},
])

render_domain_glossary([
    {"term": "Store Operations Staff", "definition": "Includes store managers, merchandisers, inventory analysts, and district managers. The Agent serves all these personas with different question types."},
    {"term": "Stockout Risk Assessment", "definition": "The custom UDF models a simplified version of how inventory planners assess risk: low days of supply + high demand = high risk. Real systems use ML models incorporating lead times, supplier reliability, and seasonality."},
])

render_what_you_built([
    "RETAIL_OPS_AGENT - Cortex Agent with Analyst + Search tools",
    "Tested structured, unstructured, mixed, and bilingual queries",
    "CALCULATE_STOCKOUT_RISK UDF as a custom tool",
    "Enhanced agent with three tool types (Analyst + Search + custom)",
])
