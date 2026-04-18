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
    title="Cortex Search & RAG Architecture Patterns",
    time_range="1:25 - 1:55 PM",
    duration="30 min",
    building="Knowledge base, Cortex Search service, and RAG query pattern",
)

render_technologies_used([
    {"name": "Cortex Search Service", "description": "A managed hybrid search engine combining vector (semantic) and keyword search with automatic reranking. Created with a single SQL statement; handles embedding, indexing, and serving automatically.", "icon": "search"},
    {"name": "RAG (Retrieval Augmented Generation)", "description": "A pattern that retrieves relevant documents first, then passes them as context to an LLM for grounded answer generation. Reduces hallucination by anchoring responses in actual data.", "icon": "hub"},
    {"name": "SEARCH_PREVIEW", "description": "SQL function to query a Cortex Search Service. Supports text queries, column selection, filtering, and result limits. Returns JSON with ranked results.", "icon": "preview"},
])


PROMPT_8_1 = """In RETAIL_AI_DEMO.RETAIL_OPS:

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

render_prompt("Prompt 8.1", "Create Cortex Search Service", PROMPT_8_1)

render_explanation("What this prompt does", """
Two major steps: building a unified knowledge base and creating a search service.

**Step 1 - CUSTOMER_KNOWLEDGE_BASE**: A UNION ALL table that combines three customer feedback sources into a common schema. This is the **corpus** for our search engine. Key design decisions:
- `doc_type` enables filtering by source (reviews vs. support tickets vs. return notes)
- `metadata_rating`, `metadata_priority`, `metadata_condition` become filter attributes
- Each source contributes its most relevant text content

**Step 2 - CREATE CORTEX SEARCH SERVICE**: This single SQL statement does an enormous amount:

1. **Embedding**: Generates vector embeddings for every row's `content` column using `snowflake-arctic-embed-l-v2.0` (a multilingual, 1024-dimension model)
2. **Indexing**: Builds both a vector index (for semantic search) and a keyword index (for lexical search)
3. **Serving**: Deploys a low-latency serving endpoint that handles queries
4. **Auto-refresh**: Monitors the source query and refreshes when data changes (within TARGET_LAG)

**ON content**: The column to search against (embed and index).

**ATTRIBUTES**: Columns that can be returned in results AND used as filters. Without listing a column here, you can't filter on it.

**EMBEDDING_MODEL**: `snowflake-arctic-embed-l-v2.0` is Snowflake's multilingual model with 1024-dimension vectors. Optimized for retrieval quality across diverse text types.

**How search works under the hood**:
1. Query text is embedded into the same vector space
2. Vector similarity finds semantically similar documents
3. Keyword search finds lexically matching documents
4. A reranker combines and re-scores results
5. Top-K results are returned
""")


PROMPT_8_2 = """In RETAIL_AI_DEMO.RETAIL_OPS, query our customer_feedback_search service using SEARCH_PREVIEW with these searches:

1. Search: "sizing issues running shoes" - show top 3 results
2. Search: "quality defect stitching" - show top 3 results
3. Search: "shipping damage" filtered to doc_type = 'return_note' - show top 3 results
4. Search: "comfortable everyday wear recommendation" - show top 3 results

Use this pattern for each:
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'RETAIL_AI_DEMO.RETAIL_OPS.customer_feedback_search',
    '{
      "query": "<search_query>",
      "columns": ["doc_id", "doc_type", "content", "metadata_rating"],
      "limit": 3
    }'
  )
)['results'] as results;

Execute all 4 searches and show results."""

render_prompt("Prompt 8.2", "Query the Search Service", PROMPT_8_2)

render_explanation("What this prompt does", """
Four search queries demonstrating different capabilities:

1. **"sizing issues running shoes"** - Tests keyword + semantic overlap. Should find reviews mentioning fit problems with athletic footwear even if they don't use the exact phrase "sizing issues" (e.g., "these sneakers run a full size small").

2. **"quality defect stitching"** - Tests semantic search. Should find product quality complaints about construction issues that may describe "seams coming apart," "thread unraveling," or "poor sewing" without using "stitching."

3. **"shipping damage" filtered** - Tests **attribute filtering**:
```json
{
  "query": "shipping damage",
  "columns": ["doc_id", "doc_type", "content"],
  "filter": {"@eq": {"doc_type": "return_note"}},
  "limit": 3
}
```
Filtering restricts results to only return notes, even if reviews or tickets also mention shipping damage.

4. **"comfortable everyday wear recommendation"** - Tests semantic matching on subjective concepts. Should find positive reviews describing comfort for casual use, even if they say "perfect for errands" or "great for weekends" rather than "everyday wear."

**SEARCH_PREVIEW** is the SQL-callable interface. In applications, you'd typically use the Python SDK:
```python
service.search(query="...", columns=[...], filter={...}, limit=3)
```

**Why hybrid search matters**: Pure keyword search misses synonyms ("stitching" vs "sewing"). Pure vector search can return semantically similar but factually irrelevant results. Cortex Search combines both with reranking for best results.
""")


PROMPT_8_3 = """In RETAIL_AI_DEMO.RETAIL_OPS, implement a RAG pattern that:

1. Takes a user question: "What are the most common product quality issues reported by Alpine & Co. customers and what improvements should the product team prioritize?"

2. First retrieves the top 5 most relevant documents from customer_feedback_search using SEARCH_PREVIEW

3. Then passes the retrieved context + question to SNOWFLAKE.CORTEX.COMPLETE() to generate a grounded answer:

WITH search_results AS (
    SELECT PARSE_JSON(
        SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
            'RETAIL_AI_DEMO.RETAIL_OPS.customer_feedback_search',
            '{
                "query": "product quality issues defects improvements",
                "columns": ["doc_id", "doc_type", "content", "metadata_rating"],
                "limit": 5
            }'
        )
    )['results'] AS results
),
context AS (
    SELECT LISTAGG(r.value:content::STRING, '\\n\\n---\\n\\n') AS combined_context
    FROM search_results, LATERAL FLATTEN(input => results) r
)
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'claude-3-5-sonnet',
    'You are a product quality analyst at Alpine & Co., a national apparel and footwear retailer. Based ONLY on the following customer feedback documents, answer the user question. Cite specific documents by their doc_id when referencing findings. If the documents do not contain enough information, say so.

SOURCE DOCUMENTS:
' || combined_context || '

USER QUESTION: What are the most common product quality issues reported by Alpine & Co. customers and what improvements should the product team prioritize?

Provide a structured answer with: 1) Common quality issues by category, 2) Most affected product lines, 3) Recommended improvements, 4) Priority ranking.'
) AS rag_response
FROM context;

Execute and show the RAG response."""

render_prompt("Prompt 8.3", "RAG Pattern: Search + Generate", PROMPT_8_3)

render_explanation("What this prompt does", """
This implements the full **RAG (Retrieval Augmented Generation)** pattern in a single SQL query:

**Step 1 - Retrieve**: SEARCH_PREVIEW finds the 5 most relevant customer feedback documents for the question.

**Step 2 - Augment**: LATERAL FLATTEN + LISTAGG combines the retrieved documents into a single context string, separated by `---` delimiters.

**Step 3 - Generate**: CORTEX.COMPLETE() receives the context + question and generates a grounded answer.

**RAG architecture diagram**:
```
User Question
     |
     v
[Cortex Search] --> Top 5 documents
     |
     v
[Context Assembly] --> "SOURCE DOCUMENTS: doc1... doc2..."
     |
     v
[LLM (COMPLETE)] --> Grounded answer with citations
```

**Why RAG works better than raw LLM**:
- **Reduces hallucination**: The LLM is instructed to answer "ONLY" from provided documents
- **Provides citations**: "Cite specific documents by their doc_id" enables traceability
- **Fresh data**: Search service reflects latest customer feedback; LLM knowledge is static
- **Domain-specific**: Alpine & Co.'s product reviews aren't in the LLM's training set

**LATERAL FLATTEN**: A Snowflake function that expands a JSON array into rows. Combined with LISTAGG, it converts the array of search results into a single concatenated string for the LLM prompt.

**Retail application**: This exact pattern powers customer insight tools. A product manager asks a natural-language question about their product line, and the system retrieves relevant customer feedback and generates an actionable summary - grounded in actual customer data, not LLM imagination.
""")


render_key_concepts([
    {"term": "Cortex Search Service", "definition": "A managed hybrid search engine created with SQL. It automatically handles embedding, indexing (vector + keyword), reranking, and auto-refresh. Think of it as Elasticsearch-as-a-SQL-statement."},
    {"term": "RAG (Retrieval Augmented Generation)", "definition": "An AI architecture pattern: (1) retrieve relevant documents from a knowledge base, (2) include them as context in an LLM prompt, (3) generate an answer grounded in the retrieved data. This is the standard pattern for enterprise AI chatbots."},
    {"term": "Hybrid Search", "definition": "Combining vector search (semantic similarity) with keyword search (exact/fuzzy text matching). Better than either alone because vector search catches synonyms while keyword search catches specific terms."},
    {"term": "LATERAL FLATTEN + LISTAGG", "definition": "LATERAL FLATTEN expands a JSON array into rows. LISTAGG concatenates multiple row values back into a single string. Together, they convert search result arrays into a context string for LLM prompts."},
])

render_domain_glossary([
    {"term": "Knowledge Base", "definition": "In this scenario, the CUSTOMER_KNOWLEDGE_BASE table unifies three feedback sources (product reviews, support tickets, return notes) into a common schema - enabling cross-source search across all customer feedback channels."},
    {"term": "snowflake-arctic-embed-l-v2.0", "definition": "Snowflake's multilingual embedding model producing 1024-dimensional vectors. Supports 100+ languages with a 512-token context window. Used by Cortex Search for automatic document embedding."},
])

render_what_you_built([
    "CUSTOMER_KNOWLEDGE_BASE - unified feedback table from 3 sources",
    "customer_feedback_search - Cortex Search service with hybrid search",
    "4 search queries demonstrating keyword, semantic, and filtered search",
    "Full RAG pipeline: retrieve + augment + generate in a single SQL query",
])
