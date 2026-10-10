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
from fallback_sql import FB_6_1, FB_6_2, FB_6_3

render_session_header(
    session_num=6,
    title="Cortex AI Functions & Model Comparison",
    time_range="11:45 AM - 12:10 PM",
    duration="25 min",
    building="Sentiment, summarization, translation, classification, extraction, filtering, and model comparison with AI_* functions",
)

render_what_you_will_build([
    "Aspect-based sentiment (fit, quality, comfort, price) on every customer review with AI_SENTIMENT",
    "Ticket summaries with AI_SUMMARIZE and a cross-ticket summary with AI_SUMMARIZE_AGG",
    "Spanish-to-English translation of supplier emails with AI_TRANSLATE",
    "A side-by-side Claude vs Llama comparison with AI_COMPLETE",
    "Return-reason classification (AI_CLASSIFY), structured review fields (AI_EXTRACT), a natural-language WHERE clause (AI_FILTER), and multi-row insights (AI_AGG)",
])

render_technologies_used([
    {"name": "AI_SENTIMENT()", "description": "Returns overall sentiment plus optional aspect-based sentiment (positive, negative, neutral, mixed, unknown) for categories you choose, such as fit or price.", "icon": "sentiment_satisfied"},
    {"name": "AI_SUMMARIZE() / AI_SUMMARIZE_AGG()", "description": "Summarize a single text value, or aggregate an entire column into one summary without context-window limits.", "icon": "summarize"},
    {"name": "AI_TRANSLATE()", "description": "Translates text between supported languages. Pass the source language, or an empty string to auto-detect.", "icon": "translate"},
    {"name": "AI_COMPLETE()", "description": "General-purpose LLM function. Choose a model per call (for example claude-sonnet-4-5 or llama3.3-70b) and optionally enforce a JSON schema on the output.", "icon": "psychology"},
    {"name": "AI_CLASSIFY() / AI_EXTRACT()", "description": "Purpose-built functions for labeling text into your categories and pulling named fields out of text, with no prompt engineering.", "icon": "label"},
    {"name": "AI_FILTER() / AI_AGG()", "description": "AI_FILTER returns TRUE/FALSE for a natural-language condition (use it in WHERE or JOIN). AI_AGG answers a question across many rows at once.", "icon": "filter_alt"},
])

st.info(
    "This session uses the current **AI_\\*** functions "
    "([docs](https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql#label-cortex-llm-ai-function)). "
    "They replace the older SNOWFLAKE.CORTEX.SENTIMENT / SUMMARIZE / TRANSLATE / COMPLETE functions.",
    icon=":material/info:",
)


PROMPT_6_1 = """In RETAIL_AI_DEMO.RETAIL_OPS, run the following Cortex AI function queries. Use the AI_* functions (not the older SNOWFLAKE.CORTEX.* functions):

1. SENTIMENT ANALYSIS: Run AI_SENTIMENT(review_text, ['fit', 'quality', 'comfort', 'price']) on CUSTOMER_REVIEWS. AI_SENTIMENT returns an object with a "categories" array of {name, sentiment}; the aspects are returned in alphabetical order, so look each one up by name (for example with FILTER(...)) rather than by array position. Show review_id, product_id, rating, the overall sentiment, and the sentiment for each aspect. Order with the most negative reviews first.

2. SUMMARIZATION: Run AI_SUMMARIZE(description_text) on the 5 longest SUPPORT_TICKETS. Show ticket_id, priority, category, and the summary. Then use AI_SUMMARIZE_AGG(description_text) to produce ONE summary across all urgent and high priority tickets.

3. TRANSLATION: Find all Spanish supplier communications in SUPPLIER_COMMUNICATIONS (where language = 'es') and use AI_TRANSLATE(message_body, 'es', 'en') to translate them to English. Show subject, the first 200 characters of the original message_body, and the translation.

Execute all queries and show results."""

render_prompt("Prompt 6.1", "Sentiment, Summarize, Translate", PROMPT_6_1)
render_fallback_sql("Sentiment, summarize, translate", FB_6_1)

render_explanation("What this prompt does", """
Three families of Cortex AI functions in action:

**AI_SENTIMENT()** - overall and aspect-based sentiment:
```sql
SELECT review_id, rating,
       AI_SENTIMENT(review_text, ['fit', 'quality', 'comfort', 'price']) AS s
FROM CUSTOMER_REVIEWS;
-- s = {"categories": [{"name": "overall", "sentiment": "mixed"},
--                     {"name": "comfort", "sentiment": "positive"}, ...]}
```
- Returns labels (positive, negative, neutral, mixed, unknown) instead of a single number, so you learn *what* customers like or dislike
- Up to 10 aspects per call; `unknown` means the review never mentions that aspect
- Compare the overall label with the star rating to find mismatches (5 stars but negative text = suspicious or nuanced review)

**AI_SUMMARIZE() and AI_SUMMARIZE_AGG()**:
```sql
SELECT ticket_id, AI_SUMMARIZE(description_text) FROM SUPPORT_TICKETS;
SELECT AI_SUMMARIZE_AGG(description_text) FROM SUPPORT_TICKETS WHERE priority IN ('urgent', 'high');
```
- AI_SUMMARIZE condenses one value; AI_SUMMARIZE_AGG is an **aggregate function** that summarizes a whole column, with no context-window limit
- Great for executive briefings: "what is the support queue about today?" in one row

**AI_TRANSLATE()**:
```sql
SELECT AI_TRANSLATE(message_body, 'es', 'en') FROM SUPPLIER_COMMUNICATIONS WHERE language = 'es';
```
- Alpine & Co. sources from Mexican suppliers who write in Spanish
- Pass `''` as the source language to auto-detect

**Key advantage**: these are plain SQL functions - use them in views, dynamic tables, WHERE clauses, and JOINs. No external API calls, and no data leaves Snowflake.
""")


PROMPT_6_2 = """In RETAIL_AI_DEMO.RETAIL_OPS, demonstrate AI_COMPLETE() with a model comparison:

1. Take the 3 most critical (priority = 'urgent' first, then 'high') support tickets from SUPPORT_TICKETS. For each, use AI_COMPLETE with TWO different models to generate a customer experience analysis:
   - Model A: 'claude-sonnet-4-5'
   - Model B: 'llama3.3-70b'

   Use this prompt template for each ticket:
   "You are a retail customer experience analyst at Alpine & Co. Analyze this support ticket and provide: 1) Root cause assessment 2) Customer impact analysis 3) Three recommended resolution actions. Keep it under 150 words. Ticket: {description_text}"

2. Cast each response to STRING and show the results side-by-side: ticket_id, priority, model_a_response, model_b_response

Execute the query and show the comparison."""

render_prompt("Prompt 6.2", "AI_COMPLETE and Model Comparison", PROMPT_6_2)
render_fallback_sql("Model comparison", FB_6_2)

render_explanation("What this prompt does", """
**AI_COMPLETE()** is the most flexible AI function - you pick the model per call:

```sql
SELECT ticket_id, priority,
  AI_COMPLETE('claude-sonnet-4-5', prompt)::STRING AS model_a_response,
  AI_COMPLETE('llama3.3-70b', prompt)::STRING      AS model_b_response
FROM (
  SELECT *, 'You are a retail customer experience analyst at Alpine & Co...' || description_text AS prompt
  FROM SUPPORT_TICKETS WHERE priority IN ('urgent', 'high') LIMIT 3
);
```

**Choosing a model** (availability depends on region and cross-region inference):
| Model | Provider | Strengths | Relative cost |
|-------|----------|-----------|------|
| claude-sonnet-4-5 | Anthropic | Strong reasoning, instruction following | Higher |
| llama3.3-70b | Meta | Good general performance, open weights | Lower |
| mistral-large2 | Mistral | Strong multilingual support | Medium |
| llama3.1-8b | Meta | Fast, good for simple tasks | Lowest |

**Why compare models**: nuanced root-cause analysis benefits from strong reasoning; simple tagging can use a smaller, cheaper model.

**Cost**: AI_COMPLETE is billed per input + output token. Running the same prompt through two models doubles the cost - in production you pick one model per use case after comparing.

**Try it without SQL**: the Cortex Playground (see the Pro Tip below) runs the same comparison side by side in the UI.
""")


PROMPT_6_3 = """In RETAIL_AI_DEMO.RETAIL_OPS, use the purpose-built AI functions:

1. AI_CLASSIFY: classify each PRODUCT_RETURN_NOTES return_reason_text into exactly one of ['Sizing Issue', 'Quality Defect', 'Not As Described', 'Changed Mind', 'Shipping Damage']. AI_CLASSIFY returns an object with a "labels" array - show labels[0] as ai_classification next to note_id and product_condition.

2. AI_EXTRACT: for 5 CUSTOMER_REVIEWS, use AI_EXTRACT(text => review_text, responseFormat => {...}) to extract: product_mentioned, sentiment (positive/neutral/negative), fit_feedback (too_small/true_to_size/too_large/not_mentioned), quality_feedback (1-5), would_recommend (true/false). The fields are returned under the "response" key.

3. AI_FILTER: return only the reviews where AI_FILTER(PROMPT('Does this review complain that the product runs small or tight? {0}', review_text)) is TRUE.

4. AI_AGG: across all reviews with rating <= 2, use AI_AGG(review_text, 'List the top 3 product problems customers mention, with a one-line recommendation for the product team for each.')

Execute and show results."""

render_prompt("Prompt 6.3", "Classify, Extract, Filter, Aggregate", PROMPT_6_3)
render_fallback_sql("Classify, extract, filter, aggregate", FB_6_3)

render_explanation("What this prompt does", """
Four task-specific AI functions that need **no prompt engineering**:

**AI_CLASSIFY** - zero-shot classification into your labels:
```sql
AI_CLASSIFY(return_reason_text,
  ['Sizing Issue', 'Quality Defect', 'Not As Described', 'Changed Mind', 'Shipping Damage']):labels[0]::STRING
```
The output is always one of your labels - no free-text answers to clean up.

**AI_EXTRACT** - named fields out of free text:
```sql
AI_EXTRACT(text => review_text, responseFormat => {
  'fit_feedback': 'Fit: too_small, true_to_size, too_large, or not_mentioned?',
  'would_recommend': 'Would the reviewer recommend the product: true or false?'}):response
```
Each key is a field name; each value is the question to answer. This is a precursor to the document extraction in Session 7.

**AI_FILTER** - a natural-language boolean you can put in WHERE or JOIN ON:
```sql
WHERE AI_FILTER(PROMPT('Does this review complain that the product runs small or tight? {0}', review_text))
```

**AI_AGG** - one answer across many rows (no context-window limit):
```sql
SELECT AI_AGG(review_text, 'List the top 3 product problems...') FROM CUSTOMER_REVIEWS WHERE rating <= 2;
```

**Why this matters for retail**: return reasons are free-text notes from store associates. Classifying them reveals patterns - if "Sizing Issue" dominates returns for one brand, the buying team can fix the size guide or talk to the supplier. AI_AGG turns hundreds of reviews into a prioritized to-do list for the product team.
""")


render_pro_tip("Compare models and track AI usage in Snowsight", """
- **Cortex Playground**: go to **AI & ML » AI Studio** and select **Try** on the Cortex Playground. Pick `claude-sonnet-4-5`, select **Compare**, choose `llama3.3-70b` on the other side, and paste a support ticket. Select **+ Connect your data** to run prompts directly against `SUPPORT_TICKETS`, and **View Code** to copy the generated SQL.
- **Query history**: go to **Monitoring » Query History** and filter on `AI_` to see each AI function query, its duration, and the warehouse it used.
""")

render_key_concepts([
    {"term": "Cortex AI Functions (AI_*)", "definition": "SQL-callable AI functions that run LLMs inside Snowflake. Task-specific functions (AI_SENTIMENT, AI_CLASSIFY, AI_EXTRACT, AI_TRANSLATE, AI_SUMMARIZE, AI_FILTER) need no prompt; AI_COMPLETE is general-purpose; AI_AGG and AI_SUMMARIZE_AGG are aggregate functions. Data never leaves Snowflake's security perimeter."},
    {"term": "Aspect-based Sentiment", "definition": "Sentiment for specific topics in the text (fit, price, quality) instead of a single overall score. AI_SENTIMENT returns a label for each aspect you pass, and 'unknown' when an aspect is not mentioned."},
    {"term": "Zero-shot Classification", "definition": "Classifying text into categories without training examples. AI_CLASSIFY constrains the output to your label list; you can add label descriptions or examples to improve accuracy for domain-specific categories."},
    {"term": "Aggregate AI Functions", "definition": "AI_AGG and AI_SUMMARIZE_AGG reduce many rows to one answer, like SUM or LISTAGG but with an LLM. They are not limited by a model's context window, so they work over large columns."},
    {"term": "Cross-region Inference", "definition": "Account parameter (CORTEX_ENABLED_CROSS_REGION) that lets AI functions route to models hosted in other regions. Required when a model is not available in your account's region."},
])

render_domain_glossary([
    {"term": "Customer Lifetime Value (CLV)", "definition": "The total revenue a customer is expected to generate over their entire relationship with Alpine & Co. High-CLV customers (frequent shoppers, full-price buyers) warrant premium support treatment. Typical apparel CLV ranges from $500-$5,000 over 3-5 years."},
    {"term": "NPS / CSAT", "definition": "Net Promoter Score measures customer loyalty ('How likely are you to recommend Alpine & Co.?', scored 0-10). Customer Satisfaction Score measures transactional satisfaction. Aspect-based sentiment on reviews can proxy these metrics at scale - and tells you which aspect is driving the score."},
])

render_what_you_built([
    "Aspect-based sentiment across all customer reviews (AI_SENTIMENT)",
    "Per-ticket and cross-ticket summaries (AI_SUMMARIZE, AI_SUMMARIZE_AGG)",
    "Spanish-to-English translation of supplier communications (AI_TRANSLATE)",
    "Side-by-side model comparison: Claude vs Llama (AI_COMPLETE)",
    "Return-reason classification (AI_CLASSIFY) and structured review fields (AI_EXTRACT)",
    "Natural-language filtering (AI_FILTER) and multi-row insights (AI_AGG)",
])
