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
    title="Unstructured Data Extraction with Document AI",
    time_range="12:55 - 1:25 PM",
    duration="30 min",
    building="Structured extraction pipelines from unstructured documents",
)

render_technologies_used([
    {"name": "LLM-based Extraction", "description": "Using CORTEX.COMPLETE() with structured output prompts to extract key fields from unstructured text. Returns JSON that can be parsed into columns.", "icon": "data_object"},
    {"name": "PARSE_JSON / TRY_PARSE_JSON", "description": "Snowflake functions to convert JSON strings into queryable VARIANT objects. TRY_PARSE_JSON handles malformed JSON gracefully by returning NULL.", "icon": "code"},
    {"name": "CTAS (CREATE TABLE AS SELECT)", "description": "Creates a table and populates it in one statement. Used here to materialize extraction results into a persistent, queryable table.", "icon": "add_circle"},
])


PROMPT_7_1 = """In RETAIL_AI_DEMO.RETAIL_OPS, use SNOWFLAKE.CORTEX.COMPLETE() to extract structured data from our CUSTOMER_REVIEWS table. For each of the first 10 reviews:

Extract the following fields from the review_text into a structured JSON format:
- product_name
- overall_sentiment (positive, neutral, negative)
- fit_rating (too_small, true_to_size, too_large, not_mentioned)
- quality_rating (1-5 scale)
- comfort_rating (1-5 scale)
- style_rating (1-5 scale)
- pros (array of positive aspects)
- cons (array of negative aspects)
- recommended_for (array of use cases, e.g. "everyday wear", "running", "office")
- price_value_assessment (excellent_value, fair_price, overpriced, not_mentioned)

Use this query pattern:
SELECT
    review_id,
    product_id,
    rating,
    PARSE_JSON(
        SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet',
            'Extract the following fields from this product review and return ONLY a valid JSON object with these keys: product_name, overall_sentiment (positive/neutral/negative), fit_rating (too_small/true_to_size/too_large/not_mentioned), quality_rating (1-5), comfort_rating (1-5), style_rating (1-5), pros (array), cons (array), recommended_for (array of use cases), price_value_assessment (excellent_value/fair_price/overpriced/not_mentioned). Review: ' || review_text
        )
    ) AS extracted_data
FROM CUSTOMER_REVIEWS
LIMIT 10;

Execute and show the extracted structured data."""

render_prompt("Prompt 7.1", "Extract Structured Data from Customer Reviews", PROMPT_7_1)

render_explanation("What this prompt does", """
This demonstrates **document intelligence** - turning unstructured review text into structured, queryable data:

The pattern has three layers:
1. **CORTEX.COMPLETE()** sends the review text + extraction instructions to the LLM
2. **PARSE_JSON()** converts the LLM's JSON string response into a Snowflake VARIANT
3. Individual fields are accessed with **dot notation**: `extracted_data:overall_sentiment::STRING`

**In production, you'd use AI_PARSE_DOCUMENT or AI_EXTRACT**:
- `AI_PARSE_DOCUMENT(stage_file, 'layout')` - Extracts text from actual PDF/image files on a Snowflake stage
- `AI_EXTRACT(text, instructions)` - Extracts specific fields from text using schema-based prompts

We use CORTEX.COMPLETE() here because our reviews are already text (not PDFs on a stage), but the extraction pattern is identical.

**Why 10 fields?** Each captures a different dimension of customer feedback:
- **fit_rating**: Critical for apparel - the #1 reason for online returns
- **quality_rating / comfort_rating / style_rating**: Maps to product development priorities
- **pros / cons arrays**: Enable aggregation across many reviews ("What do customers love/hate about this product?")
- **recommended_for**: Reveals how customers actually use the product vs. how it's marketed
- **price_value_assessment**: Directly informs pricing strategy and markdown decisions

Automating this extraction across thousands of reviews transforms qualitative feedback into quantitative analytics.
""")


PROMPT_7_2 = """In RETAIL_AI_DEMO.RETAIL_OPS:

1. Create a table called EXTRACTED_REVIEW_DATA that stores the flattened extracted fields from our customer review extraction. Use a CREATE TABLE AS SELECT that:
   - Runs the extraction on ALL CUSTOMER_REVIEWS rows
   - Flattens the JSON into individual columns: review_id, product_id, rating, product_name, overall_sentiment, fit_rating, quality_rating, comfort_rating, style_rating, pros, cons, recommended_for, price_value_assessment, extraction_timestamp (CURRENT_TIMESTAMP)

2. Then cross-validate the AI-extracted sentiment against the original numeric rating. Show any reviews where there's a mismatch (e.g., rating >= 4 but overall_sentiment = 'negative', or rating <= 2 but overall_sentiment = 'positive'). These could indicate sarcastic reviews, rating errors, or nuanced feedback.

Execute all SQL and show 10 rows from EXTRACTED_REVIEW_DATA plus the cross-validation results."""

render_prompt("Prompt 7.2", "Build an Extraction Pipeline Table", PROMPT_7_2)

render_explanation("What this prompt does", """
This builds a **materialized extraction pipeline** and validates its output:

**Step 1 - CTAS with extraction**:
```sql
CREATE TABLE EXTRACTED_REVIEW_DATA AS
SELECT
  review_id, product_id, rating,
  extracted:product_name::STRING AS product_name,
  extracted:overall_sentiment::STRING AS overall_sentiment,
  extracted:fit_rating::STRING AS fit_rating,
  extracted:quality_rating::NUMBER AS quality_rating,
  ...
FROM (
  SELECT *, PARSE_JSON(SNOWFLAKE.CORTEX.COMPLETE(...)) AS extracted
  FROM CUSTOMER_REVIEWS
);
```

**Step 2 - Cross-validation**: Comparing AI-extracted sentiment against the numeric star rating to find mismatches. This is a critical pattern in AI extraction - you always want to validate AI output against known structured data.

Common mismatch types in retail reviews:
- **High rating + negative sentiment**: Customer gave 5 stars but the text complains ("Great store but this shirt runs tiny") - the rating may reflect the store, not the product
- **Low rating + positive sentiment**: Customer loves the product but had a shipping issue ("Amazing jacket but arrived a week late") - the rating reflects the experience, not the product
- **Sarcastic reviews**: "Oh sure, love paying $80 for a hoodie that pills after one wash" with a 5-star rating

**Why materialize (table) vs. view**: Extraction via CORTEX.COMPLETE() is expensive (LLM tokens). A materialized table runs the extraction once and stores results. A view would re-extract on every query. For document processing, tables are almost always the right choice.
""")


PROMPT_7_3 = """In RETAIL_AI_DEMO.RETAIL_OPS, create a table called EXTRACTED_TICKET_FINDINGS from SUPPORT_TICKETS using SNOWFLAKE.CORTEX.COMPLETE to extract:

- ticket_id
- category
- root_cause (brief description of the underlying issue)
- affected_product (product name or 'general' if not product-specific)
- customer_emotion (frustrated, neutral, satisfied)
- urgency_level (low, medium, high, critical)
- resolution_complexity (simple, moderate, complex)
- recommended_actions (array of 2-3 suggested actions)

Store these as properly typed columns (using TRY_PARSE_JSON where needed). Then run a summary query showing the distribution of customer_emotion, urgency_level, and resolution_complexity across all tickets.

Execute all SQL and show results."""

render_prompt("Prompt 7.3", "Support Ticket Extraction", PROMPT_7_3)

render_explanation("What this prompt does", """
Applies the same extraction pattern to support tickets, but with **array and nested types**:

**TRY_PARSE_JSON** is used instead of PARSE_JSON because LLM output can sometimes be malformed:
```sql
TRY_PARSE_JSON(SNOWFLAKE.CORTEX.COMPLETE(...)) AS extracted
```
If the LLM returns invalid JSON, TRY_PARSE_JSON returns NULL instead of throwing an error. This makes the pipeline resilient.

**Array extraction**: Fields like `recommended_actions` are JSON arrays. In Snowflake, you can:
```sql
extracted:recommended_actions::ARRAY AS recommended_actions,
ARRAY_SIZE(extracted:recommended_actions) AS num_actions
```

**The summary query** provides an analytical view of support operations, enabling questions like:
- What percentage of tickets have frustrated customers?
- Which urgency levels dominate the support queue?
- What's the distribution of resolution complexity (drives staffing decisions)?

**Why this matters for retail operations**:
- **customer_emotion** enables priority routing - frustrated customers go to senior agents
- **urgency_level** drives SLA management and escalation triggers
- **resolution_complexity** informs staffing models - if 60% of tickets are "simple," self-service tools could deflect them
- **recommended_actions** can be surfaced to agents as AI-assisted suggestions, reducing resolution time

This transforms unstructured support ticket text into actionable operational analytics.
""")


render_key_concepts([
    {"term": "Document AI / AI_PARSE_DOCUMENT", "definition": "Snowflake's native capability to extract text and structure from PDFs, images, and other document formats stored on stages. Combines OCR with layout understanding. For already-extracted text, CORTEX.COMPLETE() with structured prompts achieves similar results."},
    {"term": "PARSE_JSON vs TRY_PARSE_JSON", "definition": "PARSE_JSON converts a JSON string to a VARIANT but throws an error on invalid JSON. TRY_PARSE_JSON returns NULL on invalid input. Always use TRY_PARSE_JSON when processing LLM output, which may occasionally produce malformed JSON."},
    {"term": "VARIANT Data Type", "definition": "Snowflake's semi-structured data type that can hold JSON, Avro, or Parquet data. Access nested fields with colon notation (data:field:subfield). Can contain objects, arrays, strings, numbers, and booleans."},
    {"term": "CTAS (CREATE TABLE AS SELECT)", "definition": "Creates a new table and populates it from a query in one statement. In this session, CTAS materializes LLM extraction results so the expensive CORTEX.COMPLETE() calls only run once."},
])

render_domain_glossary([
    {"term": "Product Review Mining", "definition": "The practice of extracting structured insights from unstructured customer reviews at scale. Key dimensions include fit feedback (critical for apparel), quality signals, style perception, and price-value assessment. Manual review analysis doesn't scale beyond a few hundred reviews; AI extraction enables analysis across thousands."},
    {"term": "Voice of Customer (VoC)", "definition": "A systematic approach to capturing customer expectations, preferences, and aversions. In retail, VoC data comes from reviews, support tickets, surveys, social media, and return reasons. AI extraction consolidates these sources into a unified, queryable dataset."},
    {"term": "Return Reason Analysis", "definition": "Understanding why products are returned is critical for profitability. Apparel has the highest return rate of any retail category (25-40% for online orders). The top reasons are sizing issues (too small/too large), quality defects, and 'not as described'. Each reason requires a different remediation strategy."},
])

render_what_you_built([
    "LLM-based extraction of 10 structured fields from customer reviews",
    "EXTRACTED_REVIEW_DATA table with flattened, typed columns",
    "Cross-validation pipeline comparing AI sentiment vs numeric ratings",
    "EXTRACTED_TICKET_FINDINGS with emotion, urgency, and action arrays",
    "Operational analytics summary across all support tickets",
])
