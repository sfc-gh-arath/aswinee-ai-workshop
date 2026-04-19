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
    session_num=4,
    title="Cortex Search & RAG Architecture Patterns",
    time_range="0:45 - 1:00",
    duration="15 min",
    building="Knowledge base, Cortex Search service, and RAG query pattern",
)

render_technologies_used([
    {"name": "Cortex Search Service", "description": "A managed hybrid search engine combining vector (semantic) and keyword search with automatic reranking. Created with a single SQL statement; handles embedding, indexing, and serving automatically.", "icon": "search"},
    {"name": "RAG (Retrieval Augmented Generation)", "description": "A pattern that retrieves relevant documents first, then passes them as context to an LLM for grounded answer generation. Reduces hallucination by anchoring responses in actual data.", "icon": "hub"},
    {"name": "SEARCH_PREVIEW", "description": "SQL function to query a Cortex Search Service. Supports text queries, column selection, filtering, and result limits. Returns JSON with ranked results.", "icon": "preview"},
])


PROMPT_4_1 = """In RETAIL_AI_DEMO.RETAIL_OPS:

1. First, create a unified text table for search called CUSTOMER_KNOWLEDGE_BASE that combines:
   - CUSTOMER_REVIEWS: review_id as doc_id, 'product_review' as doc_type, review_text as content, rating as metadata_rating
   - SUPPORT_TICKETS: ticket_id as doc_id, 'support_ticket' as doc_type, description_text as content, priority as metadata_priority
   - PRODUCT_RETURN_NOTES: note_id as doc_id, 'return_note' as doc_type, return_reason_text as content, product_condition as metadata_condition

2. Then create a Cortex Search Service:
   CREATE OR REPLACE CORTEX SEARCH SERVICE customer_feedback_search
     ON content
     ATTRIBUTES metadata_rating, metadata_priority, metadata_condition, doc_type
     WAREHOUSE = RETAIL_AI_WH
     TARGET_LAG = '1 hour'
     EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
     AS (
       SELECT doc_id, doc_type, content, metadata_rating, metadata_priority, metadata_condition
       FROM CUSTOMER_KNOWLEDGE_BASE
     );

Execute all SQL. Then verify the service is created by running SHOW CORTEX SEARCH SERVICES."""

render_prompt("Prompt 4.1", "Create Cortex Search Service", PROMPT_4_1)

render_explanation("What this prompt does", """
Two major steps: building a unified knowledge base and creating a search service.

**Step 1 - CUSTOMER_KNOWLEDGE_BASE**: A UNION ALL table that combines three customer feedback sources into a common schema. This is the **corpus** for our search engine.

**Step 2 - CREATE CORTEX SEARCH SERVICE**: This single SQL statement:
1. **Embeds** every row's content using `snowflake-arctic-embed-l-v2.0` (1024-dimension vectors)
2. **Indexes** both vector (for semantic search) and keyword (for lexical search)
3. **Serves** a low-latency endpoint that handles queries
4. **Auto-refreshes** when source data changes (within TARGET_LAG)

No infrastructure to manage — Snowflake handles embedding generation, index building, and serving automatically.
""")


PROMPT_4_2 = """In RETAIL_AI_DEMO.RETAIL_OPS, run these search queries against our customer_feedback_search service:

1. Basic keyword search: "sizing problems with shoes"
2. Semantic search: "customers who love the quality but find the fit too tight"
3. Filtered search: Search for "defective" but only in doc_type = 'support_ticket'
4. Subjective concept search: "frustration with online orders"

Use SNOWFLAKE.CORTEX.SEARCH_PREVIEW() for each, returning doc_id, doc_type, content, and the score. Show 5 results per query.

Execute all four searches and compare the results."""

render_prompt("Prompt 4.2", "Search the Knowledge Base", PROMPT_4_2)

render_explanation("What this prompt does", """
Tests four search patterns via `SEARCH_PREVIEW()`:

```sql
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'RETAIL_AI_DEMO.RETAIL_OPS.CUSTOMER_FEEDBACK_SEARCH',
    '{  "query": "sizing problems with shoes",
        "columns": ["doc_id", "doc_type", "content"],
        "limit": 5  }'
  )
);
```

**Four query types test different capabilities**:
1. **Keyword search** — matches documents containing "sizing", "problems", "shoes"
2. **Semantic search** — finds documents about fit issues even if the exact words differ (e.g., "runs small" matches "fit too tight")
3. **Filtered search** — combines semantic matching with metadata filters
4. **Concept search** — "frustration" is a concept, not a keyword. Semantic search understands emotional tone.

**Hybrid search**: Cortex Search automatically combines keyword and vector search, then reranks results for optimal relevance.
""")


PROMPT_4_3 = """In RETAIL_AI_DEMO.RETAIL_OPS, build a complete RAG (Retrieval Augmented Generation) pipeline in a single SQL query:

1. First, retrieve the top 5 most relevant documents from customer_feedback_search for the question: "What are the most common quality issues with Alpine & Co. products?"
2. Flatten the search results using LATERAL FLATTEN
3. Aggregate the retrieved documents into a context string using LISTAGG
4. Pass the context + question to SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet', ...) with instructions to:
   - Answer based ONLY on the provided context
   - Cite specific documents by doc_id
   - Identify patterns across multiple feedback sources
   - Provide 3 actionable recommendations

Build this as a single CTE-based query that chains: search -> flatten -> aggregate -> generate.

Execute and show both the retrieved context documents and the final AI-generated answer."""

render_prompt("Prompt 4.3", "Build a RAG Pipeline", PROMPT_4_3)

render_explanation("What this prompt does", """
Implements the full **RAG (Retrieval Augmented Generation)** pattern in a single SQL query:

```
Search (retrieve) → Flatten → Aggregate context → LLM Generate (with grounding)
```

**Why RAG matters**: Without RAG, an LLM has no access to Alpine & Co.'s actual customer feedback. It would hallucinate answers about product quality. RAG grounds the response in real documents.

**The grounding instruction** is critical:
- "Answer based ONLY on the provided context" — prevents hallucination
- "Cite specific documents by doc_id" — enables verification
- "Identify patterns across multiple feedback sources" — drives cross-document synthesis

**The CTE pattern** chains four steps:
1. `search_results` — calls SEARCH_PREVIEW to retrieve relevant docs
2. `flattened` — uses LATERAL FLATTEN to turn JSON array into rows
3. `context` — LISTAGG combines all retrieved doc content into one string
4. `answer` — CORTEX.COMPLETE generates a grounded response

This is production-ready RAG — it runs entirely within Snowflake, uses real customer data, and produces cited, verifiable answers.
""")


render_key_concepts([
    {"term": "Cortex Search Service", "definition": "A managed hybrid search engine. Combines semantic (vector) search with keyword search and automatic reranking. Created with SQL, auto-refreshes from source data, and handles embedding/indexing/serving automatically."},
    {"term": "RAG (Retrieval Augmented Generation)", "definition": "A pattern that retrieves relevant documents first, then passes them as context to an LLM. Reduces hallucination by anchoring responses in actual data. The key AI architecture pattern for enterprise applications."},
    {"term": "Hybrid Search", "definition": "Combining keyword (lexical) search with vector (semantic) search. Keywords catch exact matches; vectors catch meaning. Cortex Search does both automatically and reranks the combined results."},
    {"term": "Grounding", "definition": "Constraining an LLM to answer based on provided context rather than its training data. Implemented via system prompts like 'Answer ONLY from the provided documents.' Essential for enterprise AI to prevent hallucination."},
])

render_domain_glossary([
    {"term": "Voice of Customer (VoC)", "definition": "A systematic approach to capturing customer expectations, preferences, and aversions. In retail, VoC data comes from reviews, support tickets, surveys, social media, and return reasons. RAG enables natural language querying across all these sources."},
])

render_what_you_built([
    "CUSTOMER_KNOWLEDGE_BASE - unified text table combining 3 feedback sources",
    "customer_feedback_search - Cortex Search service with hybrid search",
    "4 search query patterns (keyword, semantic, filtered, concept)",
    "Full RAG pipeline: retrieve -> flatten -> aggregate -> generate with citations",
])
