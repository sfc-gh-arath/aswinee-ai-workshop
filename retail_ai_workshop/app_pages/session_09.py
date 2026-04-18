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
    session_num=9,
    title="Vector Embeddings Deep Dive",
    time_range="1:55 - 2:15 PM",
    duration="20 min",
    building="Custom embeddings, similarity search, and vector vs keyword comparison",
)

render_technologies_used([
    {"name": "EMBED_TEXT_1024()", "description": "Generates a 1024-dimensional vector embedding for text input using a specified model. The embedding captures the semantic meaning of the text as a point in high-dimensional space.", "icon": "scatter_plot"},
    {"name": "VECTOR Data Type", "description": "Snowflake's native vector data type. VECTOR(FLOAT, 1024) stores 1024 floating-point numbers. Supports similarity operations directly in SQL.", "icon": "data_array"},
    {"name": "VECTOR_COSINE_SIMILARITY()", "description": "Computes the cosine similarity between two vectors. Returns a value between -1 and 1, where 1 means identical direction (most similar) and 0 means orthogonal (unrelated).", "icon": "compare"},
])


PROMPT_9_1 = """In RETAIL_AI_DEMO.RETAIL_OPS:

1. Generate vector embeddings for 18 sample texts using SNOWFLAKE.CORTEX.EMBED_TEXT_1024('snowflake-arctic-embed-l-v2.0', text). Include deliberately similar pairs so we can see high cosine similarity scores:

   Sizing feedback (similar pair):
   - 'Running shoes feel too tight around the toe box'
   - 'Athletic sneakers are uncomfortably narrow in the front'

   Quality defects (similar pair):
   - 'Winter coat zipper broke after two weeks'
   - 'Outerwear jacket zipper failed within first month of use'

   Product praise (similar pair):
   - 'Love the Summit activewear leggings for yoga'
   - 'Summit brand yoga pants are my favorite workout gear'

   Sizing complaints (similar pair):
   - 'Ordered medium but fits like a small, very disappointed'
   - 'Size medium runs way too small, need to exchange for large'

   Fabric issues (similar pair):
   - 'Basecamp hoodie fabric pills after washing'
   - 'Basecamp casual hoodie material deteriorates in the wash'

   Dissimilar texts (no close match to the above):
   - 'Great boots for hiking in the rain'
   - 'Looking for dress shoes for a wedding'
   - 'Kids sneakers wore out in two months'
   - 'Excellent customer service helped with my return'
   - 'Sale prices on summer sandals are unbeatable'
   - 'The new fall collection colors are stunning'
   - 'Shipping took longer than expected but product is fine'
   - 'Loyalty rewards program needs better redemption options'

2. Store these in a table called EMBEDDING_EXAMPLES with columns: text_id, text_content, embedding (VECTOR(FLOAT, 1024)), category (sizing, quality, praise, complaint, fabric, footwear, occasion, kids, service, promotion, style, shipping, loyalty)

3. Then compute the cosine similarity between ALL pairs and show the top 10 most similar pairs and the top 5 least similar pairs using VECTOR_COSINE_SIMILARITY().

Execute all SQL and show results."""

render_prompt("Prompt 9.1", "Generate and Compare Embeddings", PROMPT_9_1)

render_explanation("What this prompt does", """
This hands-on exercise builds **intuition for how vector embeddings work**:

**Generating embeddings**:
```sql
SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_1024(
  'snowflake-arctic-embed-l-v2.0',
  'Running shoes feel too tight around the toe box'
) AS embedding;
```
This returns a VECTOR(FLOAT, 1024) - an array of 1024 floating-point numbers that encodes the semantic meaning of the text.

**What makes embeddings powerful**: Texts with similar meanings get similar vectors, even if they use completely different words. For example:
- "Running shoes feel too tight around the toe box" and "Athletic sneakers are uncomfortably narrow in the front" would have HIGH similarity
- "Running shoes feel too tight" and "Loyalty rewards program needs better redemption options" would have LOW similarity

**Pairwise comparison** with VECTOR_COSINE_SIMILARITY:
```sql
SELECT
  a.text_content AS text_a,
  b.text_content AS text_b,
  VECTOR_COSINE_SIMILARITY(a.embedding, b.embedding) AS similarity
FROM EMBEDDING_EXAMPLES a
CROSS JOIN EMBEDDING_EXAMPLES b
WHERE a.text_id < b.text_id
ORDER BY similarity DESC
LIMIT 10;
```

**Expected high-similarity pairs** (these are the deliberately paired texts):
- Sizing pair (~0.95+): "Running shoes feel too tight around the toe box" vs "Athletic sneakers are uncomfortably narrow in the front"
- Zipper defect pair (~0.93+): "Winter coat zipper broke after two weeks" vs "Outerwear jacket zipper failed within first month..."
- Summit praise pair (~0.92+): "Love the Summit activewear leggings for yoga" vs "Summit brand yoga pants are my favorite workout gear"
- Size mismatch pair (~0.94+): "Ordered medium but fits like a small..." vs "Size medium runs way too small..."
- Basecamp fabric pair (~0.93+): "Basecamp hoodie fabric pills after washing" vs "Basecamp casual hoodie material deteriorates..."

**Expected moderate-similarity pairs**:
- Cross-category matches like sizing complaint + sizing feedback (both about fit issues, ~0.6-0.7)

**Expected low-similarity pairs**:
- "Loyalty rewards program needs better redemption options" vs "Winter coat zipper broke after two weeks" (~0.3 or lower)
- Customer service praise vs fabric complaints (completely different topics)

This exercise demonstrates that embeddings capture **semantic relationships**, not just lexical overlap. Paraphrased sentences score nearly as high as identical text.
""")


PROMPT_9_2 = """In RETAIL_AI_DEMO.RETAIL_OPS, build a custom semantic search using our embeddings:

1. Generate embeddings for all CUSTOMER_REVIEWS review_text entries and store in a table called REVIEW_EMBEDDINGS (review_id, review_text, embedding VECTOR(FLOAT, 1024))

2. Write a semantic search query that takes the user query "What reviews mention poor stitching quality or fabric defects?" and:
   - Generates an embedding for the query text
   - Computes cosine similarity against all review embeddings
   - Returns the top 5 most semantically similar reviews with their similarity scores

3. Compare this to a simple ILIKE keyword search for '%stitch%' OR '%defect%' OR '%quality%' on the same data. Show which reviews the vector search found that keyword search missed, and vice versa.

Execute all SQL and show the comparison."""

render_prompt("Prompt 9.2", "Semantic Search with Custom Embeddings", PROMPT_9_2)

render_explanation("What this prompt does", """
A direct comparison between **semantic (vector) search** and **keyword search**:

**Custom semantic search**:
```sql
WITH query_embedding AS (
  SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_1024(
    'snowflake-arctic-embed-l-v2.0',
    'What reviews mention poor stitching quality or fabric defects?'
  ) AS qe
)
SELECT
  r.review_id, r.review_text,
  VECTOR_COSINE_SIMILARITY(r.embedding, q.qe) AS similarity
FROM REVIEW_EMBEDDINGS r, query_embedding q
ORDER BY similarity DESC LIMIT 5;
```

**Keyword search**:
```sql
SELECT review_id, review_text
FROM CUSTOMER_REVIEWS
WHERE review_text ILIKE '%stitch%'
   OR review_text ILIKE '%defect%'
   OR review_text ILIKE '%quality%';
```

**What the comparison reveals**:
- **Vector search finds**: Reviews about "seams coming apart," "thread unraveling," "fabric fraying," "construction issues" that don't contain the keywords "stitch" or "defect"
- **Keyword search finds**: Every mention of those exact words, including false positives (e.g., "the quality is outstanding" matches '%quality%' but isn't a defect)
- **Overlap**: Reviews that both methods find

This is precisely why Cortex Search uses **hybrid search** - combining both approaches gets the best results.

**This is the foundation of Session 8**: Cortex Search does all of this automatically. This session shows you what's happening under the hood. Understanding embeddings and similarity helps you debug search quality issues, choose the right embedding model, and design better knowledge bases.
""")


render_key_concepts([
    {"term": "Vector Embedding", "definition": "A fixed-size array of floating-point numbers that represents text in a high-dimensional space. Semantically similar texts are mapped to nearby points. Created by embedding models trained on large text corpora."},
    {"term": "Cosine Similarity", "definition": "Measures the angle between two vectors. Values range from -1 to 1. Score of 1.0 = identical direction (maximally similar), 0.0 = orthogonal (unrelated), -1.0 = opposite direction. The standard metric for comparing text embeddings."},
    {"term": "VECTOR(FLOAT, 1024)", "definition": "Snowflake's native vector data type storing 1024 floating-point dimensions. First-class data type that supports similarity functions, storage, and indexing natively in the database."},
    {"term": "Semantic vs Keyword Search", "definition": "Keyword search matches exact text patterns (LIKE/ILIKE). Semantic search matches meaning by comparing vector embeddings. Keyword catches exact terms; semantic catches synonyms and related concepts. Hybrid search combines both."},
])

render_domain_glossary([
    {"term": "Product Discovery", "definition": "How customers find products they want to buy. Traditional retail search uses keyword matching ('blue running shoes'), which misses intent-based queries ('shoes for a 5K in the rain'). Semantic search enables natural-language product discovery that understands customer intent."},
    {"term": "Recommendation Systems", "definition": "Algorithms that suggest products based on similarity. Embeddings power content-based recommendations: if a customer likes a product, recommend products with similar embeddings. Alpine & Co. could use review embeddings to find 'products customers describe similarly' - a powerful signal for cross-selling."},
])

render_what_you_built([
    "EMBEDDING_EXAMPLES table with 18 domain-specific embeddings",
    "Pairwise similarity matrix showing semantic relationships",
    "REVIEW_EMBEDDINGS table for all customer reviews",
    "Custom semantic search implementation from scratch",
    "Side-by-side comparison of vector vs keyword search results",
])
