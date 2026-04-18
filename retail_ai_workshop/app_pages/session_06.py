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
    session_num=6,
    title="Cortex LLM Functions & Model Comparison",
    time_range="11:45 AM - 12:10 PM",
    duration="25 min",
    building="Sentiment analysis, translation, summarization, classification, and model comparison",
)

render_technologies_used([
    {"name": "CORTEX.SENTIMENT()", "description": "Returns a sentiment score between -1 (negative) and 1 (positive) for text input. Runs as a simple SQL function - no model deployment needed.", "icon": "sentiment_satisfied"},
    {"name": "CORTEX.SUMMARIZE()", "description": "Generates concise summaries of long text. Useful for reducing verbose support tickets or customer feedback to key points.", "icon": "summarize"},
    {"name": "CORTEX.TRANSLATE()", "description": "Translates text between languages. Supports 12+ languages. Useful for processing international supplier communications.", "icon": "translate"},
    {"name": "CORTEX.COMPLETE()", "description": "The most flexible Cortex function. Sends a prompt to any supported LLM model and returns the response. Supports model selection for quality/cost tradeoffs.", "icon": "psychology"},
])


PROMPT_6_1 = """In RETAIL_AI_DEMO.RETAIL_OPS, run the following Cortex LLM function queries:

1. SENTIMENT ANALYSIS: Run SNOWFLAKE.CORTEX.SENTIMENT() on the review_text column of CUSTOMER_REVIEWS. Show the review rating, product_id, and sentiment score for all rows. Order by sentiment score ascending (most negative first).

2. SUMMARIZATION: Run SNOWFLAKE.CORTEX.SUMMARIZE() on the 5 longest SUPPORT_TICKETS description_text entries. Show ticket_id, priority, category, and the summarized text.

3. TRANSLATION: Find all Spanish supplier communications in SUPPLIER_COMMUNICATIONS (where language='es') and use SNOWFLAKE.CORTEX.TRANSLATE(body, 'es', 'en') to translate them to English. Show original subject, original body (first 200 chars), and translated text.

Execute all three queries and show results."""

render_prompt("Prompt 6.1", "Sentiment, Summarize, Translate", PROMPT_6_1)

render_explanation("What this prompt does", """
Three Cortex AI SQL functions in action:

**SENTIMENT()** - Analyzes emotional tone of text:
```sql
SELECT review_id, product_id, rating,
       SNOWFLAKE.CORTEX.SENTIMENT(review_text) AS sentiment_score
FROM CUSTOMER_REVIEWS
ORDER BY sentiment_score ASC;
```
- Score range: -1.0 (very negative) to +1.0 (very positive)
- Useful for: detecting unhappy customers, flagging product quality issues, monitoring brand perception
- **No model selection needed** - Snowflake uses an optimized model automatically
- Compare sentiment score vs. numeric rating to find mismatches (e.g., 5-star rating but negative text = suspicious review)

**SUMMARIZE()** - Condenses long text:
```sql
SELECT ticket_id, priority, category,
       SNOWFLAKE.CORTEX.SUMMARIZE(description_text) AS summary
FROM SUPPORT_TICKETS
ORDER BY LENGTH(description_text) DESC LIMIT 5;
```
- Produces 2-3 sentence summaries of multi-paragraph text
- Great for: executive dashboards, alert notifications, quick triage of support queues

**TRANSLATE()** - Machine translation:
```sql
SELECT subject, LEFT(body, 200) AS original_snippet,
       SNOWFLAKE.CORTEX.TRANSLATE(body, 'es', 'en') AS english_translation
FROM SUPPLIER_COMMUNICATIONS WHERE language = 'es';
```
- Alpine & Co. sources from suppliers in Mexico and Spain, requiring Spanish-to-English translation
- Supports: en, fr, de, es, it, ja, ko, pl, pt, ru, sv, zh

**Key advantage**: All three functions run as SQL - they can be embedded in views, dynamic tables, WHERE clauses, and JOINs. No external API calls, no data leaving Snowflake.
""")


PROMPT_6_2 = """In RETAIL_AI_DEMO.RETAIL_OPS, demonstrate SNOWFLAKE.CORTEX.COMPLETE() with a model comparison:

1. Take the 3 most critical (priority='urgent' or 'high') support tickets from SUPPORT_TICKETS. For each, use COMPLETE() with TWO different models to generate a customer experience analysis:
   - Model A: 'claude-3-5-sonnet'
   - Model B: 'llama3.1-70b'
   
   Use this prompt template for each ticket:
   "You are a retail customer experience analyst at Alpine & Co. Analyze this support ticket and provide: 1) Root cause assessment 2) Customer impact analysis 3) Three recommended resolution actions. Ticket: {description_text}"

2. Show the results side-by-side: ticket_id, priority, model_a_response, model_b_response

Execute the query and show the comparison."""

render_prompt("Prompt 6.2", "AI Complete for Analysis and Model Comparison", PROMPT_6_2)

render_explanation("What this prompt does", """
This demonstrates **CORTEX.COMPLETE()** - the most versatile Cortex function - with a side-by-side model comparison:

```sql
SELECT
  ticket_id, priority,
  SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet', prompt) AS model_a_response,
  SNOWFLAKE.CORTEX.COMPLETE('llama3.1-70b', prompt) AS model_b_response
FROM (
  SELECT *, 'You are a retail customer experience analyst at Alpine & Co...' || description_text AS prompt
  FROM SUPPORT_TICKETS
  WHERE priority IN ('urgent', 'high')
  LIMIT 3
);
```

**Available models in Snowflake Cortex** (as of early 2025):
| Model | Provider | Strengths | Cost |
|-------|----------|-----------|------|
| claude-3-5-sonnet | Anthropic | Strong reasoning, instruction following | Higher |
| llama3.1-70b | Meta | Good general performance, open weights | Lower |
| mistral-large2 | Mistral | European language support | Medium |
| llama3.1-8b | Meta | Fast, good for simple tasks | Lowest |

**Why compare models**: Different models excel at different tasks. For nuanced customer experience analysis, you want strong reasoning. For simple classification or tagging, a smaller model may suffice at lower cost.

**Cost implications**: Each COMPLETE() call is billed per token (input + output). Running the same prompt through two models doubles the cost. In production, you'd pick one model per use case after comparison.

**Retail application**: This pattern is powerful for automating support ticket triage. Instead of a human reading each ticket, the LLM provides instant root cause assessment and recommended actions - enabling faster resolution and better customer satisfaction scores.
""")


PROMPT_6_3 = """In RETAIL_AI_DEMO.RETAIL_OPS:

1. Use SNOWFLAKE.CORTEX.COMPLETE() to zero-shot classify each PRODUCT_RETURN_NOTES return_reason_text into exactly one category: 'Sizing Issue', 'Quality Defect', 'Not As Described', 'Changed Mind', or 'Shipping Damage'. Return ONLY the category name.

   SELECT note_id, product_id,
          SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet',
            'Classify this product return reason into exactly one category: Sizing Issue, Quality Defect, Not As Described, Changed Mind, or Shipping Damage. Return ONLY the category name. Return reason: ' || return_reason_text
          ) AS ai_classification,
          product_condition
   FROM PRODUCT_RETURN_NOTES;

2. Use CORTEX.COMPLETE to extract structured entities from 5 CUSTOMER_REVIEWS. Extract: product_mentioned, sentiment (positive/neutral/negative), fit_feedback (too_small/true_to_size/too_large/not_mentioned), quality_feedback (1-5 rating), would_recommend (true/false) as a JSON object.

Execute and show results."""

render_prompt("Prompt 6.3", "Classify and Extract", PROMPT_6_3)

render_explanation("What this prompt does", """
Two advanced LLM patterns using CORTEX.COMPLETE():

**Zero-shot classification**: We ask the LLM to categorize return reasons without any training examples. The prompt constrains the output to exactly one of five categories. This is called "zero-shot" because the model hasn't been fine-tuned on Alpine & Co.'s specific categories.

**Structured extraction**: We ask the LLM to extract specific fields from unstructured review text and return them as JSON. This is a precursor to the more formal document extraction in Session 7.

**Prompt engineering tips shown here**:
- "Return ONLY the category name" - Constrains output format
- Listing the exact categories - Prevents the model from inventing new ones
- "as a JSON object" - Requests structured output for programmatic parsing

**The extraction pattern** is particularly powerful:
```sql
PARSE_JSON(
  SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet',
    'Extract these fields as JSON: product_mentioned, sentiment... Text: ' || review_text
  )
) AS extracted
```

This turns unstructured customer reviews into queryable structured data, all within SQL. In retail, this enables automated tracking of fit issues by product, quality defects by supplier, and recommendation rates by brand.

**Why this matters for retail**: Product return reasons are often free-text notes from store associates. Classifying them automatically reveals patterns - if "Sizing Issue" dominates returns for a specific brand, the buying team can adjust size guides or negotiate with the supplier.
""")


render_key_concepts([
    {"term": "Cortex AI SQL Functions", "definition": "SQL-callable AI functions that run LLMs within Snowflake. SENTIMENT, SUMMARIZE, TRANSLATE are task-specific; COMPLETE is general-purpose. All process data without it leaving Snowflake's security perimeter."},
    {"term": "Zero-shot Classification", "definition": "Using an LLM to classify text into categories without any training examples. The categories are specified in the prompt. Works well for common classification tasks but less reliable for highly domain-specific categories."},
    {"term": "Prompt Engineering", "definition": "The art of crafting inputs to LLMs to get desired outputs. Key techniques: role setting ('You are a retail customer experience analyst'), output constraints ('Return ONLY...'), structured output requests ('as JSON'), and few-shot examples."},
    {"term": "Cross-region Inference", "definition": "Snowflake account parameter that allows Cortex functions to route to models hosted in other regions. Required when a specific model isn't available in your account's region."},
])

render_domain_glossary([
    {"term": "Customer Lifetime Value (CLV)", "definition": "The total revenue a customer is expected to generate over their entire relationship with Alpine & Co. High-CLV customers (frequent shoppers, full-price buyers) warrant premium support treatment. Typical apparel CLV ranges from $500-$5,000 over 3-5 years."},
    {"term": "NPS / CSAT", "definition": "Net Promoter Score measures customer loyalty ('How likely are you to recommend Alpine & Co.?', scored 0-10). Customer Satisfaction Score measures transactional satisfaction ('How satisfied were you with this purchase?'). Sentiment analysis on reviews can proxy these metrics at scale."},
])

render_what_you_built([
    "Sentiment analysis across all customer reviews",
    "Automated summarization of support tickets",
    "Spanish-to-English translation of supplier communications",
    "Side-by-side model comparison (Claude vs Llama)",
    "Zero-shot classification of product return reasons",
    "Structured entity extraction from customer reviews",
])
