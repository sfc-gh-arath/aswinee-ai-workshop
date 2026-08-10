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
    session_num=7,
    title="Cortex Search & Knowledge Base",
    time_range="2:45 - 3:05",
    duration="20 min",
    building="Searchable knowledge base over inventory policies and procedures",
)

render_technologies_used([
    {"name": "Cortex Search Service", "description": "A managed hybrid search engine (vector + keyword + reranking) that you create with a single DDL statement. Indexes text data and returns semantically relevant results.", "icon": "manage_search"},
    {"name": "Embedding Model", "description": "snowflake-arctic-embed-l-v2.0 converts text into high-dimensional vectors that capture semantic meaning. 'Reorder policy' and 'when to place a new order' become nearby vectors.", "icon": "hub"},
    {"name": "Hybrid Search", "description": "Combines keyword matching (exact terms) with semantic search (meaning similarity) and a neural reranker. Better than either approach alone.", "icon": "join_inner"},
])


PROMPT_7_1 = """Create a unified knowledge base table called ROSS_INVENTORY_LAB.RAW.INVENTORY_KNOWLEDGE_BASE that combines:

1. All rows from REPLENISHMENT_POLICIES (use policy_title as title, policy_text as content, category as metadata)
2. Add 20 additional FAQ-style entries with realistic inventory management Q&A. Generate these as INSERT statements with columns:
   - doc_id (NUMBER)
   - title (VARCHAR - the question or topic)
   - content (VARCHAR - 100-300 word detailed answer)
   - category (VARCHAR - one of: reorder_process, seasonal_planning, stockout_response, clearance, receiving, transfers, new_store, holiday_prep, pack_and_hold, allocation)
   - doc_type (VARCHAR - 'policy' for originals, 'faq' for new entries)

Example FAQ topics to include:
- "How do I request an emergency reorder?"
- "What triggers a pack-and-hold decision?"
- "When should I escalate a late delivery to the buyer?"
- "How are allocation quantities determined for new stores?"
- "What's the markdown cadence for clearance items?"
- "How do I handle damaged goods in receiving?"
- "What's the process for inter-store transfers?"
- "When does seasonal merchandise arrive at stores?"

Make the content detailed and realistic — these should read like actual internal process documents.

Execute and verify the total row count."""

render_prompt("Prompt 7.1", "Build the Knowledge Base", PROMPT_7_1)

render_explanation("What this prompt does", """
Creates a **unified knowledge base** by combining existing policy documents with new FAQ content:

**Why a knowledge base?**
- Analysts often have questions that aren't answered by data — they need to know the *process*
- "What's the reorder procedure?" isn't a SQL query — it's a document retrieval problem
- Cortex Search will make this content queryable in natural language

**Design decisions**:
- **Unified table**: Policies and FAQs in one table so a single search service covers both
- **Category metadata**: Allows filtering searches to specific topics
- **doc_type column**: Distinguishes source material for provenance
- **Realistic content**: The value of the knowledge base depends on content quality

**This becomes one of the Agent's tools** in Session 8 — when a user asks a process question, the Agent retrieves relevant policies instead of trying to generate an answer from nothing.
""")


PROMPT_7_2 = """Create a Cortex Search service called ROSS_INVENTORY_LAB.RAW.INVENTORY_POLICY_SEARCH with these settings:

- ON: content (the searchable text column)
- ATTRIBUTES: category, doc_type, title (filterable metadata)
- WAREHOUSE: INVENTORY_LAB_WH
- TARGET_LAG: '1 hour'
- EMBEDDING_MODEL: 'snowflake-arctic-embed-l-v2.0'
- SOURCE: ROSS_INVENTORY_LAB.RAW.INVENTORY_KNOWLEDGE_BASE

After creation, test it with these search queries:
1. Basic keyword: "reorder point"
2. Semantic: "what should I do when a product runs out of stock"
3. Filtered: search for "seasonal" but only in category = 'seasonal_planning'
4. Concept search: "how to handle excess inventory after the holidays"

Show the top 3 results for each with their relevance scores."""

render_prompt("Prompt 7.2", "Create Cortex Search Service", PROMPT_7_2)

render_explanation("What this prompt does", """
Creates a **managed search service** with a single DDL statement:

**What Snowflake does automatically**:
1. Reads all rows from INVENTORY_KNOWLEDGE_BASE
2. Generates vector embeddings using snowflake-arctic-embed-l-v2.0
3. Builds a hybrid index (keyword + vector)
4. Sets up automatic refresh (within 1 hour of source changes)
5. Provides a query API that handles retrieval + reranking

**The four test queries demonstrate different search modes**:
1. **Keyword**: "reorder point" — exact term matching
2. **Semantic**: "what should I do when a product runs out" — meaning-based (no exact keyword match needed)
3. **Filtered**: Restricts search to a specific category — reduces noise
4. **Concept**: Abstract question — tests whether the system understands intent

**Hybrid advantage**: Pure keyword search would miss "stockout response procedure" when you search for "out of stock." Pure vector search might rank vaguely related content too high. Hybrid combines both for better precision.
""")


PROMPT_7_3 = """Now build a RAG (Retrieval Augmented Generation) query that:

1. Takes a user question: "A buyer is asking about our pack-and-hold strategy. When do we use it, what are the holding costs, and what categories does it apply to?"
2. Searches INVENTORY_POLICY_SEARCH for the top 5 relevant documents
3. Passes the retrieved documents as context to SNOWFLAKE.CORTEX.COMPLETE('claude-sonnet-5', ...) with a prompt that says:
   "You are an inventory management expert at Ross Stores. Answer the following question using ONLY the provided context documents. If the context doesn't contain enough information, say so. Cite which documents you're drawing from."
4. Returns the LLM's grounded answer

Write this as a single CTE-based SQL query. Execute it and show the result.

Then try a second question through the same pattern: "What's the escalation process when a supplier is consistently delivering late?"

Show both answers."""

render_prompt("Prompt 7.3", "RAG Pipeline", PROMPT_7_3)

render_explanation("What this prompt does", """
Implements a **Retrieval Augmented Generation (RAG)** pipeline in pure SQL:

**The RAG pattern**:
1. **Retrieve**: Search the knowledge base for relevant documents
2. **Augment**: Inject those documents into the LLM prompt as context
3. **Generate**: LLM synthesizes an answer grounded in the retrieved content

**Why RAG instead of just asking the LLM directly?**
- LLMs don't know your company's specific policies
- RAG grounds the answer in your actual documents — no hallucination
- You can verify the answer by checking the cited sources
- When policies change, the answer updates automatically (search service refreshes)

**The CTE structure**:
```
WITH search_results AS (... search query ...),
     context AS (... aggregate documents into a single string ...),
     answer AS (... CORTEX.COMPLETE with context ...)
SELECT * FROM answer;
```

**This becomes the Agent's second tool** in Session 8 — process/policy questions route to search + RAG rather than trying to query structured data.
""")


render_key_concepts([
    {"term": "Cortex Search Service", "definition": "A managed, auto-refreshing search engine created with a single DDL statement. Combines keyword search, vector search (via embeddings), and neural reranking. Handles indexing, refresh, and query serving."},
    {"term": "RAG (Retrieval Augmented Generation)", "definition": "A pattern that retrieves relevant documents from a search index and provides them as context to an LLM, grounding the LLM's answer in your actual data/documents rather than its general training knowledge."},
    {"term": "Embedding Model", "definition": "A neural network that converts text into high-dimensional vectors (numbers) that capture semantic meaning. Similar text gets similar vectors. snowflake-arctic-embed-l-v2.0 is Snowflake's built-in embedding model."},
])

render_domain_glossary([
    {"term": "Pack-and-Hold", "definition": "Purchasing excess inventory at deep discounts (often end-of-season clearance from brands) and holding it in distribution centers until the appropriate selling season. A key off-price retail strategy — buy winter coats in March, sell them in October."},
    {"term": "Allocation", "definition": "The process of distributing inventory from distribution centers to individual stores based on their sales patterns, size, demographics, and capacity. Getting allocation right means each store gets what it can sell."},
])

render_what_you_built([
    "INVENTORY_KNOWLEDGE_BASE table with ~70 policy/FAQ documents",
    "INVENTORY_POLICY_SEARCH Cortex Search service with hybrid retrieval",
    "Tested 4 search patterns: keyword, semantic, filtered, concept",
    "Full RAG pipeline: search → context → LLM-generated grounded answer",
])
