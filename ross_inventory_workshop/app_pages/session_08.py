import streamlit as st
from components import (
    render_session_header,
    render_prompt,
    render_explanation,
    render_technologies_used,
    render_key_concepts,
    render_domain_glossary,
    render_what_you_built,
)

render_session_header(
    session_num=8,
    title="Cortex Agent & CoWork",
    time_range="3:05 - 3:30",
    duration="25 min",
    building="Multi-tool AI agent combining structured queries, search, and custom logic for conversational BI",
)

render_technologies_used([
    {"name": "Cortex Agent", "description": "An AI orchestrator that decides which tools to use based on the user's question. Routes structured data questions to Analyst, policy questions to Search, and calculations to custom UDFs.", "icon": "smart_toy"},
    {"name": "CREATE AGENT", "description": "DDL to define an agent with: model (which LLM), tools (what it can use), instructions (domain context and routing guidance), and sample_questions (for CoWork UI).", "icon": "engineering"},
    {"name": "CoWork", "description": "The conversational BI interface in Snowsight where the agent lives. Users type questions and get answers — no SQL required. The agent appears as an available assistant.", "icon": "forum"},
])


PROMPT_8_1 = """Create a SQL UDF called ROSS_INVENTORY_LAB.ANALYTICS.CALCULATE_REORDER_QUANTITY that takes store_id (NUMBER) and product_id (NUMBER) as inputs and returns a VARIANT with:

- recommended_order_qty: calculated as CEIL((avg_daily_demand * (lead_time_days + safety_stock_days) - current_on_hand) / pack_size) * pack_size
  where avg_daily_demand is from last 28 days of DAILY_SALES, lead_time_days and pack_size from PRODUCTS, current_on_hand from latest INVENTORY_SNAPSHOTS, safety_stock_days = 14
- estimated_cost: recommended_order_qty * unit_cost
- estimated_days_until_stockout: current_on_hand / NULLIF(avg_daily_demand, 0)
- urgency: 'EMERGENCY' if days_until_stockout <= lead_time, 'URGENT' if <= lead_time + 7, 'STANDARD' otherwise
- current_on_hand: the current inventory quantity
- avg_daily_demand: the calculated demand rate
- store_name: from STORES
- product_name: from PRODUCTS

Use OBJECT_CONSTRUCT() to build the return value. Handle edge cases: if no sales data exists, use 0 for demand; if no inventory snapshot, flag as 'NO_DATA'.

Execute and test with: SELECT CALCULATE_REORDER_QUANTITY(1, 1);"""

render_prompt("Prompt 8.1", "Create Custom Calculation Tool", PROMPT_8_1)

render_explanation("What this prompt does", """
Creates a **custom tool** that the Agent can invoke for specific calculations:

**Why a UDF instead of just SQL in the semantic view?**
- The reorder calculation has complex business logic (safety stock, pack size rounding, urgency classification)
- It takes specific inputs (store + product) and returns a structured recommendation
- The Agent can call it when someone asks "how much should I order for product X at store Y?"
- It encapsulates domain expertise in reusable code

**VARIANT return type**: Returns a JSON-like structure with multiple fields. The Agent can extract what it needs from the response.

**Business logic**:
- Order enough for lead time + 14 days safety stock
- Round up to full packs (you can't order partial cases)
- Urgency classification guides prioritization
- Edge case handling prevents divide-by-zero errors
""")


PROMPT_8_2 = """Create a Cortex Agent called ROSS_INVENTORY_LAB.ANALYTICS.INVENTORY_OPS_AGENT with:

MODEL: 'claude-sonnet-4-6'

TOOLS:
1. The semantic view ROSS_INVENTORY_LAB.ANALYTICS.INVENTORY_OPTIMIZATION_SV (for Cortex Analyst - structured data questions)
2. The Cortex Search service ROSS_INVENTORY_LAB.RAW.INVENTORY_POLICY_SEARCH (for policy/process questions)
3. The UDF ROSS_INVENTORY_LAB.ANALYTICS.CALCULATE_REORDER_QUANTITY (for reorder calculations)

INSTRUCTIONS: "You are an inventory optimization assistant for Ross Stores. You help analysts understand inventory health, identify risks, and make replenishment decisions.

Tool routing:
- For questions about current inventory levels, sales trends, store performance, stockout risk, or any data query: use the semantic view (Cortex Analyst)
- For questions about policies, procedures, processes, guidelines, or 'how do I...': use the search service
- For questions asking 'how much should I order' or 'what's the reorder quantity' for a specific store and product: use the CALCULATE_REORDER_QUANTITY function
- For questions that need both data AND context: use multiple tools and synthesize the answer

Domain context:
- Ross Stores is an off-price retailer with ~1800 US stores
- Key metrics: Days of Supply (DOS), fill rate (target 93%), inventory turnover (target 13x)
- Seasons: holiday (Nov-Dec), back-to-school (Jul-Aug), spring reset (Mar-Apr)
- DOS below 7 days is concerning; below 3 is critical
- Always include store name and product details in answers when relevant"

SAMPLE_QUESTIONS:
- "Which stores have the most critical stockout risk right now?"
- "What's the reorder policy for seasonal merchandise?"
- "How much should I order for store 5, product 12?"
- "Show me the top categories by lost revenue from stockouts"
- "What's the process for emergency reorders?"
- "Compare fill rates across regions"

Execute and confirm the agent is created."""

render_prompt("Prompt 8.2", "Create the Cortex Agent", PROMPT_8_2)

render_explanation("What this prompt does", """
Creates a **multi-tool Cortex Agent** — the capstone of the entire lab:

**Three tools, three capabilities**:
1. **Semantic View (Analyst)**: Answers data questions by generating SQL → "what's our fill rate in the West?"
2. **Cortex Search**: Answers process questions by retrieving documents → "how do emergency reorders work?"
3. **Custom UDF**: Performs specific calculations → "how much product X should store Y order?"

**The INSTRUCTIONS** are critical — they tell the Agent HOW to route:
- Data questions → Analyst (structured SQL)
- Process questions → Search (document retrieval)
- Calculation requests → UDF (custom logic)
- Complex questions → Multiple tools combined

**SAMPLE_QUESTIONS** appear in the CoWork UI as suggestions, helping users understand what they can ask.

**This is the production pattern**: In a real deployment, this agent would be the primary interface for Ross inventory analysts. They open CoWork, ask a question, and get an answer that combines data, policies, and calculations — without knowing which tool was used.
""")


PROMPT_8_3 = """Test the INVENTORY_OPS_AGENT with these queries using SNOWFLAKE.CORTEX.DATA_AGENT_RUN():

1. Structured data query: "Which 5 stores have the worst fill rate and what are their top stockout categories?"
2. Policy/process query: "What's the procedure for handling a supplier that's consistently late with deliveries?"
3. Calculation query: "Calculate the reorder quantity for store 5, product 10"
4. Multi-tool query: "Store 3 has a lot of stockouts in shoes. What's the current inventory situation, how much should we order, and what does our reorder policy say about this category?"

For each, show:
- The agent's response
- Which tool(s) it used (if visible in the response)

The multi-tool query (4) should demonstrate the agent combining all three tools in a single answer."""

render_prompt("Prompt 8.3", "Test the Agent", PROMPT_8_3)

render_explanation("What this prompt does", """
Validates that the agent correctly **routes to the right tool** and handles multi-tool orchestration:

1. **Structured → Analyst**: Should generate SQL against the semantic view, return data with store names and categories
2. **Process → Search**: Should retrieve policy documents about late suppliers, synthesize a clear answer
3. **Calculation → UDF**: Should call CALCULATE_REORDER_QUANTITY and format the recommendation
4. **Multi-tool → All three**: The most impressive — combines:
   - Analyst: current inventory/stockout data for store 3 shoes
   - UDF: recommended order quantity
   - Search: relevant reorder policies for that category

**This is the 'aha moment'** of the lab: a single natural language question triggers a coordinated response drawing from structured data, unstructured documents, and custom calculations. The analyst didn't need to know which tables, views, or functions to use.
""")


PROMPT_8_4 = """Now let's see this in CoWork:

1. Open CoWork in Snowsight and find the INVENTORY_OPS_AGENT
2. Try asking conversationally:
   - "Good morning! How's our inventory looking today?"
   - "Anything I should worry about?"
   - "Tell me more about the stores with problems"
   - "What should we do about it?"

3. Then try a scenario an analyst might actually encounter:
   - "I just heard we're expecting a demand spike for shoes next month due to a back-to-school promotion. Which stores are already low on shoe inventory and what should we order?"

4. Explain how this agent would be shared with the 30 analysts on the team — what roles/permissions are needed?

Show me how to access this in Snowsight and describe the user experience."""

render_prompt("Prompt 8.4", "CoWork Experience & Deployment", PROMPT_8_4)

render_explanation("What this prompt does", """
Demonstrates the **production end-user experience** in CoWork:

**Conversational flow**: The first set of questions mimics how an analyst would actually start their day — open and exploratory, then drilling down based on what the agent surfaces.

**Real scenario**: The back-to-school promotion question requires the agent to:
- Understand temporal context (next month = upcoming season)
- Query current inventory for shoes specifically
- Assess which stores are at risk
- Calculate recommended orders
- Potentially reference seasonal policies

**Deployment for the team**: Covers the practical "now what?" —
- How do other analysts access this agent?
- What roles/grants are needed?
- How does the semantic view scope what they can see?
- Can different analysts have different permissions?

**This is the payoff**: Everything built in Sessions 1-7 culminates in a conversational interface that combines data, documents, and calculations. An analyst can ask a natural language question and get a comprehensive, actionable answer.
""")


render_key_concepts([
    {"term": "Cortex Agent", "definition": "A Snowflake object that orchestrates multiple tools (Analyst, Search, UDFs) to answer complex questions. It decides which tool(s) to use based on the question and its instructions. Created with CREATE AGENT DDL."},
    {"term": "Tool Routing", "definition": "The agent's ability to determine which tool is appropriate for each question. Data questions → Analyst, process questions → Search, calculations → UDF. Multi-tool queries may use several tools and synthesize results."},
    {"term": "CoWork", "definition": "The conversational BI interface in Snowsight where agents are accessible. Users type natural language questions and get answers. Supports follow-up questions, conversation history, and suggested questions."},
    {"term": "DATA_AGENT_RUN()", "definition": "The SQL function to invoke an agent programmatically. Useful for testing and for embedding agent calls in other workflows (stored procedures, Streamlit apps, etc.)."},
])

render_domain_glossary([
    {"term": "Demand Spike", "definition": "A sudden increase in sales velocity beyond normal patterns. Can be caused by promotions, seasonal events, viral social media, or competitor stockouts. Requires rapid inventory response to avoid missing the opportunity."},
    {"term": "Allocation Planning", "definition": "The process of distributing limited inventory across stores based on expected demand, store capacity, historical performance, and promotional plans. Critical during high-demand events when supply is constrained."},
])

render_what_you_built([
    "CALCULATE_REORDER_QUANTITY UDF — custom business logic tool for the agent",
    "INVENTORY_OPS_AGENT — multi-tool Cortex Agent with Analyst + Search + UDF",
    "Tested routing: structured queries, policy retrieval, calculations, and multi-tool orchestration",
    "Demonstrated CoWork conversational BI experience for daily analyst workflow",
])
