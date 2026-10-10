import streamlit as st
from components import (
    render_session_header,
    render_prompt,
    render_explanation,
    render_technologies_used,
    render_key_concepts,
    render_domain_glossary,
    render_what_you_built,
    render_what_you_will_build,
    render_fallback_sql,
    render_pro_tip,
)
from fallback_sql import FB_7_1, FB_7_2, FB_7_3

render_session_header(
    session_num=7,
    title="Unstructured Data Extraction with Document AI",
    time_range="12:55 - 1:25 PM",
    duration="30 min",
    building="Structured extraction pipelines from unstructured documents",
)

render_what_you_will_build([
    "An LLM extraction query that turns each customer review into 10 typed fields (sentiment, fit, ratings, pros/cons, value)",
    "An EXTRACTED_REVIEW_DATA table that materializes those fields, plus a cross-check of AI sentiment vs star rating",
    "An EXTRACTED_TICKET_FINDINGS table with root cause, emotion, urgency, complexity, and recommended actions per support ticket",
])

render_technologies_used([
    {"name": "AI_COMPLETE() + response_format", "description": "AI_COMPLETE with a JSON schema in response_format forces the LLM to return valid, typed JSON - no parsing failures.", "icon": "data_object"},
    {"name": "PARSE_JSON / TRY_PARSE_JSON", "description": "Snowflake functions to convert JSON strings into queryable VARIANT objects. TRY_PARSE_JSON handles malformed JSON gracefully by returning NULL.", "icon": "code"},
    {"name": "CTAS (CREATE TABLE AS SELECT)", "description": "Creates a table and populates it in one statement. Used here to materialize extraction results into a persistent, queryable table.", "icon": "add_circle"},
])


PROMPT_7_1 = """In RETAIL_AI_DEMO.RETAIL_OPS, use AI_COMPLETE() with structured output to extract structured data from our CUSTOMER_REVIEWS table. For each of the first 10 reviews:

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

Use AI_COMPLETE with named arguments and a JSON schema so the output is always valid JSON:
SELECT
    review_id,
    product_id,
    rating,
    AI_COMPLETE(
        model => 'claude-sonnet-4-5',
        prompt => 'Extract structured fields from this product review. All *_rating fields are integers from 1 to 5. Review: ' || review_text,
        response_format => {'type': 'json', 'schema': {'type': 'object', 'properties': {
            'product_name': {'type': 'string'},
            'overall_sentiment': {'type': 'string', 'enum': ['positive', 'neutral', 'negative']},
            ... one property per field above (arrays use {'type': 'array', 'items': {'type': 'string'}}) ...
        }, 'required': [all field names]}}
    ) AS extracted_data
FROM CUSTOMER_REVIEWS
ORDER BY review_id
LIMIT 10;

Execute and show the extracted structured data."""

render_prompt("Prompt 7.1", "Extract Structured Data from Customer Reviews", PROMPT_7_1)
render_fallback_sql("Extract review fields", FB_7_1)

render_explanation("What this prompt does", """
This demonstrates **document intelligence** - turning unstructured review text into structured, queryable data:

The pattern has three layers:
1. **AI_COMPLETE()** sends the review text + extraction instructions to the LLM
2. **response_format** supplies a JSON schema, so the model must return valid JSON with exactly those fields and types (enums for categorical fields, arrays for pros/cons)
3. Individual fields are accessed with **colon notation**: `extracted_data:overall_sentiment::STRING`

**Other extraction options**:
- `AI_PARSE_DOCUMENT(TO_FILE('@stage', 'file.pdf'), {'mode': 'LAYOUT'})` - Extracts text from actual PDF/image files on a Snowflake stage
- `AI_EXTRACT(text => ..., responseFormat => {...})` - Extracts named fields with no prompt (you used it in Session 6)

We use AI_COMPLETE with a schema here because we want typed integers and arrays in one call; the pattern is identical for text extracted from PDFs.

**Why 10 fields?** Each captures a different dimension of customer feedback:
- **fit_rating**: Critical for apparel - the #1 reason for online returns
- **quality_rating / comfort_rating / style_rating**: Maps to product development priorities
- **pros / cons arrays**: Enable aggregation across many reviews ("What do customers love/hate about this product?")
- **recommended_for**: Reveals how customers actually use the product vs. how it's marketed
- **price_value_assessment**: Directly informs pricing strategy and markdown decisions

Automating this extraction across thousands of reviews transforms qualitative feedback into quantitative analytics.
""")


PROMPT_7_2 = """In RETAIL_AI_DEMO.RETAIL_OPS:

1. Create a table called EXTRACTED_REVIEW_DATA that stores the flattened extracted fields from our customer review extraction (use the same AI_COMPLETE + response_format pattern as Prompt 7.1). Use a CREATE TABLE AS SELECT that:
   - Runs the extraction on ALL CUSTOMER_REVIEWS rows
   - Flattens the JSON into individual columns: review_id, product_id, rating, product_name, overall_sentiment, fit_rating, quality_rating, comfort_rating, style_rating, pros, cons, recommended_for, price_value_assessment, extraction_timestamp (CURRENT_TIMESTAMP)

2. Then cross-validate the AI-extracted sentiment against the original numeric rating. Show any reviews where there's a mismatch (e.g., rating >= 4 but overall_sentiment = 'negative', or rating <= 2 but overall_sentiment = 'positive'). These could indicate sarcastic reviews, rating errors, or nuanced feedback.

Execute all SQL and show 10 rows from EXTRACTED_REVIEW_DATA plus the cross-validation results."""

render_prompt("Prompt 7.2", "Build an Extraction Pipeline Table", PROMPT_7_2)
render_fallback_sql("Extraction pipeline table", FB_7_2)

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
  SELECT *, AI_COMPLETE(model => 'claude-sonnet-4-5', prompt => ..., response_format => {...}) AS extracted
  FROM CUSTOMER_REVIEWS
);
```

**Step 2 - Cross-validation**: Comparing AI-extracted sentiment against the numeric star rating to find mismatches. This is a critical pattern in AI extraction - you always want to validate AI output against known structured data.

Common mismatch types in retail reviews:
- **High rating + negative sentiment**: Customer gave 5 stars but the text complains ("Great store but this shirt runs tiny") - the rating may reflect the store, not the product
- **Low rating + positive sentiment**: Customer loves the product but had a shipping issue ("Amazing jacket but arrived a week late") - the rating reflects the experience, not the product
- **Sarcastic reviews**: "Oh sure, love paying $80 for a hoodie that pills after one wash" with a 5-star rating

**Why materialize (table) vs. view**: Extraction via AI_COMPLETE() is expensive (LLM tokens). A materialized table runs the extraction once and stores results. A view would re-extract on every query. For document processing, tables are almost always the right choice.
""")


PROMPT_7_3 = """In RETAIL_AI_DEMO.RETAIL_OPS, create a table called EXTRACTED_TICKET_FINDINGS from SUPPORT_TICKETS using AI_COMPLETE('claude-sonnet-4-5') with a response_format JSON schema to extract:

- ticket_id
- category
- root_cause (brief description of the underlying issue)
- affected_product (product name or 'general' if not product-specific)
- customer_emotion (frustrated, neutral, satisfied)
- urgency_level (low, medium, high, critical)
- resolution_complexity (simple, moderate, complex)
- recommended_actions (array of 2-3 suggested actions)

Store these as properly typed columns (use enums in the schema for the categorical fields and an array for recommended_actions). Then run a summary query showing the distribution of customer_emotion, urgency_level, and resolution_complexity across all tickets.

Execute all SQL and show results."""

render_prompt("Prompt 7.3", "Support Ticket Extraction", PROMPT_7_3)
render_fallback_sql("Support ticket extraction", FB_7_3)

render_explanation("What this prompt does", """
Applies the same extraction pattern to support tickets, but with **array and nested types**:

**Structured output vs. parsing free text**: without a schema you would wrap the LLM call in TRY_PARSE_JSON, because free-form output can be malformed:
```sql
TRY_PARSE_JSON(AI_COMPLETE('claude-sonnet-4-5', 'Return ONLY JSON ...'))  -- NULL if the JSON is invalid
```
With `response_format`, the output is guaranteed to match the schema, and enums keep categorical values (frustrated / neutral / satisfied) consistent for GROUP BY.

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


render_pro_tip("Inspect extracted data and try the Document Processing Playground", """
- **Results**: go to **Catalog » Explorer » RETAIL_AI_DEMO » RETAIL_OPS » Tables » EXTRACTED_REVIEW_DATA » Data Preview**. Select the `PROS` or `CONS` cell to see the extracted arrays.
- **Real documents**: go to **AI & ML » AI Studio** and open the **Document Processing Playground** to upload a PDF (for example a supplier invoice) and try AI_EXTRACT and AI_PARSE_DOCUMENT without writing SQL.
""")


render_key_concepts([
    {"term": "Document AI / AI_PARSE_DOCUMENT", "definition": "Snowflake's native capability to extract text and structure from PDFs, images, and other document formats stored on stages. Combines OCR with layout understanding. For already-extracted text, AI_COMPLETE with a response_format schema (or AI_EXTRACT) achieves similar results."},
    {"term": "PARSE_JSON vs TRY_PARSE_JSON", "definition": "PARSE_JSON converts a JSON string to a VARIANT but throws an error on invalid JSON. TRY_PARSE_JSON returns NULL on invalid input. Always use TRY_PARSE_JSON when processing LLM output, which may occasionally produce malformed JSON."},
    {"term": "VARIANT Data Type", "definition": "Snowflake's semi-structured data type that can hold JSON, Avro, or Parquet data. Access nested fields with colon notation (data:field:subfield). Can contain objects, arrays, strings, numbers, and booleans."},
    {"term": "CTAS (CREATE TABLE AS SELECT)", "definition": "Creates a new table and populates it from a query in one statement. In this session, CTAS materializes LLM extraction results so the expensive AI_COMPLETE() calls only run once."},
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
