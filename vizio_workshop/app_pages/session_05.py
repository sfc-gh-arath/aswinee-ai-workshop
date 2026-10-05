import streamlit as st
from components import (
    render_session_header,
    render_prompt,
    render_fallback_sql,
    render_explanation,
    render_technologies_used,
    render_key_concepts,
    render_domain_glossary,
    render_what_you_built,
)

render_session_header(
    session_num=5,
    title="Cortex AI Functions",
    time_range="1:15 - 1:35",
    duration="20 min",
    building="Sentiment analysis, topic classification, and feature extraction on customer feedback",
)

render_technologies_used([
    {"name": "AI_SENTIMENT()", "description": "Analyzes text and returns a sentiment score from -1 (negative) to +1 (positive). Works directly in SQL on any text column.", "icon": "thumb_up"},
    {"name": "AI_CLASSIFY()", "description": "Classifies text into user-defined categories using a managed model. No prompt engineering needed — just provide the text and the category list.", "icon": "label"},
    {"name": "AI_EXTRACT()", "description": "Extracts structured information (entities, fields) from text. Returns a JSON object with the extracted values. Supports multiple languages.", "icon": "data_object"},
])


PROMPT_5_1 = """Run sentiment analysis on VIZIO customer feedback using the AI_SENTIMENT() function and compare results across device series:

1. Use AI_SENTIMENT(feedback_text) on the VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK table
2. Show a summary: for each device_series, calculate avg_sentiment, count of positive (score > 0.3), neutral (-0.3 to 0.3), and negative (< -0.3) reviews
3. Show the 5 most negative reviews (lowest sentiment score) with their device_series, rating, and feedback_text
4. Show the 5 most positive reviews

Does sentiment correlate with star rating? Show the average sentiment score per rating (1-5)."""

render_prompt("Prompt 5.1", "Sentiment Analysis with AI_SENTIMENT", PROMPT_5_1)

render_fallback_sql("Sentiment analysis", """-- Sentiment by device series
SELECT
    device_series,
    COUNT(*) AS total_reviews,
    ROUND(AVG(AI_SENTIMENT(feedback_text)), 3) AS avg_sentiment,
    COUNT_IF(AI_SENTIMENT(feedback_text) > 0.3) AS positive,
    COUNT_IF(AI_SENTIMENT(feedback_text) BETWEEN -0.3 AND 0.3) AS neutral,
    COUNT_IF(AI_SENTIMENT(feedback_text) < -0.3) AS negative
FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
GROUP BY device_series
ORDER BY avg_sentiment;

-- Most negative
SELECT device_series, rating, AI_SENTIMENT(feedback_text) AS sentiment, feedback_text
FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
ORDER BY sentiment LIMIT 5;

-- Sentiment vs rating correlation
SELECT rating, ROUND(AVG(AI_SENTIMENT(feedback_text)), 3) AS avg_sentiment
FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
GROUP BY rating ORDER BY rating;""")

render_explanation("What this prompt does", """
Applies **AI_SENTIMENT()** — a Cortex AI function that scores text from -1 to +1:

- **Per-series breakdown**: Which device lines have the happiest/unhappiest customers?
- **Extreme reviews**: What are the strongest negative/positive signals?
- **Sentiment vs rating**: Do star ratings and AI sentiment agree? (They usually correlate but diverge on sarcastic or mixed reviews.)

**Key insight**: AI_SENTIMENT() is a SQL function — you can use it in WHERE, GROUP BY, window functions, and views just like any other function. No Python, no API calls, no prompt engineering.
""")


PROMPT_5_2 = """Use AI_CLASSIFY() to classify customer feedback into topics. For each review in VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK:

1. Use AI_CLASSIFY(feedback_text, ['picture_quality', 'audio_quality', 'smartcast_ui', 'wifi_connectivity', 'remote_control', 'app_performance', 'watchfree_plus', 'setup_experience', 'firmware_update', 'value_for_money']) to classify each review

2. Show the distribution: how many reviews per classified topic?
3. For the top 3 topics, show the average sentiment score (using AI_SENTIMENT) and average star rating
4. Show the top 3 most negative reviews for the wifi_connectivity topic

Limit to 50 reviews to manage cost."""

render_prompt("Prompt 5.2", "Topic Classification with AI_CLASSIFY", PROMPT_5_2)

render_fallback_sql("Topic classification", """-- Classify feedback topics (limit 50 for cost)
WITH classified AS (
    SELECT *,
        AI_CLASSIFY(feedback_text,
            ['picture_quality', 'audio_quality', 'smartcast_ui', 'wifi_connectivity',
             'remote_control', 'app_performance', 'watchfree_plus', 'setup_experience',
             'firmware_update', 'value_for_money']
        ) AS topic,
        AI_SENTIMENT(feedback_text) AS sentiment
    FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
    LIMIT 50
)
SELECT topic, COUNT(*) AS review_count,
       ROUND(AVG(sentiment), 3) AS avg_sentiment,
       ROUND(AVG(rating), 1) AS avg_rating
FROM classified
GROUP BY topic
ORDER BY review_count DESC;""")

render_explanation("What this prompt does", """
Uses **AI_CLASSIFY()** for text classification — no prompt engineering needed:

**AI_CLASSIFY vs AI_COMPLETE for classification**:
- **AI_CLASSIFY**: Purpose-built for classification. Just pass text + category list. The model is managed by Snowflake.
- **AI_COMPLETE**: General-purpose LLM. You'd need to craft a prompt with instructions. More flexible but more work.

**Why AI_CLASSIFY is better here**:
- Simpler syntax — no prompt to write or debug
- Consistent output format — always returns one of your categories
- Optimized for classification workloads

**Why this matters for VIZIO**: Product teams instantly see "42% of negative reviews mention wifi_connectivity" — without anyone writing prompts.
""")


PROMPT_5_3 = """Use AI_EXTRACT() to pull structured information from customer feedback. For reviews where feedback_type = 'feature_request' in VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK:

1. Use AI_EXTRACT(feedback_text, ['feature_requested', 'product_area', 'competing_product_mentioned', 'customer_frustration_level']) to extract structured fields from each review

2. Show the extracted results as a table with: feedback_id, device_series, rating, and the extracted fields
3. Which features are requested most often?
4. Which competing products (Roku, Fire TV, Apple TV, Samsung, LG) are mentioned most?
5. Which device_series has the highest customer_frustration_level?

Limit to 30 reviews."""

render_prompt("Prompt 5.3", "Structured Extraction with AI_EXTRACT", PROMPT_5_3)

render_fallback_sql("Feature extraction", """-- Extract structured data from feature requests
WITH requests AS (
    SELECT feedback_id, device_series, rating, feedback_text,
        AI_EXTRACT(feedback_text,
            ['feature_requested', 'product_area', 'competing_product_mentioned', 'customer_frustration_level']
        ) AS extracted
    FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
    WHERE feedback_type = 'feature_request'
    LIMIT 30
)
SELECT feedback_id, device_series, rating,
    extracted:feature_requested::VARCHAR AS feature_requested,
    extracted:product_area::VARCHAR AS product_area,
    extracted:competing_product_mentioned::VARCHAR AS competing_product,
    extracted:customer_frustration_level::VARCHAR AS frustration_level
FROM requests;

-- Top requested features
SELECT extracted:feature_requested::VARCHAR AS feature, COUNT(*) AS cnt
FROM (
    SELECT AI_EXTRACT(feedback_text,
        ['feature_requested', 'product_area', 'competing_product_mentioned', 'customer_frustration_level']
    ) AS extracted
    FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
    WHERE feedback_type = 'feature_request'
    LIMIT 30
)
GROUP BY 1 ORDER BY 2 DESC;""")

render_explanation("What this prompt does", """
**AI_EXTRACT()** turns unstructured text into structured, queryable data:

**AI_EXTRACT vs AI_COMPLETE for extraction**:
- **AI_EXTRACT**: Purpose-built. Pass text + field names. Returns a structured object. Optimized for extraction.
- **AI_COMPLETE**: You'd need to write a prompt asking for JSON output, then parse with TRY_PARSE_JSON(). More flexible but more fragile.

**What gets extracted**:
- **feature_requested**: What the customer actually wants
- **product_area**: Which part of the product (smartcast, remote, picture, etc.)
- **competing_product_mentioned**: Which competitors customers are comparing to
- **customer_frustration_level**: How urgent is this request?

**Business value**: Product managers can now query: "What are the top feature requests where customers mention Roku?" — impossible without AI extraction.
""")


render_key_concepts([
    {"term": "AI_SENTIMENT()", "definition": "Cortex AI function returning -1 to +1 sentiment score. Use directly in SQL — SELECT, WHERE, GROUP BY, window functions, views. No prompt needed."},
    {"term": "AI_CLASSIFY(text, categories)", "definition": "Classifies text into one of the provided categories. Returns the best-matching category name. Purpose-built and simpler than writing classification prompts with AI_COMPLETE."},
    {"term": "AI_EXTRACT(text, fields)", "definition": "Extracts structured fields from unstructured text. Returns a JSON-like object with the requested field values. Purpose-built for entity and information extraction."},
    {"term": "AI_COMPLETE(model, prompt)", "definition": "General-purpose LLM function for tasks that AI_CLASSIFY/AI_EXTRACT/AI_SENTIMENT don't cover. Takes a model name and prompt, returns text. Use for custom summarization, generation, or complex reasoning."},
])

render_domain_glossary([
    {"term": "ACR (Automatic Content Recognition)", "definition": "VIZIO's Inscape technology that identifies what's playing on screen (including cable/satellite). Used for audience measurement. Privacy-regulated — users must opt in."},
    {"term": "OTT (Over-The-Top)", "definition": "Content delivered via the internet rather than cable/satellite. Netflix, Hulu, WatchFree+ are all OTT services. VIZIO's smart TV platform is an OTT delivery mechanism."},
])

render_what_you_built([
    "Sentiment analysis with AI_SENTIMENT across all device series with star-rating correlation",
    "Topic classification with AI_CLASSIFY into 10 VIZIO-specific categories",
    "Structured feature extraction with AI_EXTRACT — fields, competitors, frustration levels",
])
