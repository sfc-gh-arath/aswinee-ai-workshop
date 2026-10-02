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
    title="Cortex LLM Functions",
    time_range="1:15 - 1:35",
    duration="20 min",
    building="Sentiment analysis, topic classification, and feature extraction on customer feedback",
)

render_technologies_used([
    {"name": "CORTEX.SENTIMENT()", "description": "Analyzes text and returns a score from -1 (negative) to +1 (positive). Works directly in SQL on any text column.", "icon": "thumb_up"},
    {"name": "CORTEX.COMPLETE()", "description": "General-purpose LLM inference. Use for classification, extraction, summarization, and any text-to-text task with a custom prompt.", "icon": "psychology"},
    {"name": "Prompt Engineering", "description": "Crafting precise instructions for the LLM: role setting, output format constraints, few-shot examples. The quality of the prompt determines the quality of the output.", "icon": "auto_fix_high"},
])


PROMPT_5_1 = """Run sentiment analysis on VIZIO customer feedback and compare results across device series:

1. Use SNOWFLAKE.CORTEX.SENTIMENT() on the feedback_text column from VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
2. Show a summary: for each device_series, calculate avg_sentiment, count of positive (score > 0.3), neutral (-0.3 to 0.3), and negative (< -0.3) reviews
3. Show the 5 most negative reviews (lowest sentiment score) with their device_series, rating, and feedback_text
4. Show the 5 most positive reviews

Does sentiment correlate with star rating? Show the average sentiment score per rating (1-5)."""

render_prompt("Prompt 5.1", "Sentiment Analysis", PROMPT_5_1)

render_fallback_sql("Sentiment analysis", """-- Sentiment by device series
SELECT
    device_series,
    COUNT(*) AS total_reviews,
    ROUND(AVG(SNOWFLAKE.CORTEX.SENTIMENT(feedback_text)), 3) AS avg_sentiment,
    COUNT_IF(SNOWFLAKE.CORTEX.SENTIMENT(feedback_text) > 0.3) AS positive,
    COUNT_IF(SNOWFLAKE.CORTEX.SENTIMENT(feedback_text) BETWEEN -0.3 AND 0.3) AS neutral,
    COUNT_IF(SNOWFLAKE.CORTEX.SENTIMENT(feedback_text) < -0.3) AS negative
FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
GROUP BY device_series
ORDER BY avg_sentiment;

-- Most negative
SELECT device_series, rating, SNOWFLAKE.CORTEX.SENTIMENT(feedback_text) AS sentiment, feedback_text
FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
ORDER BY sentiment LIMIT 5;

-- Sentiment vs rating correlation
SELECT rating, ROUND(AVG(SNOWFLAKE.CORTEX.SENTIMENT(feedback_text)), 3) AS avg_sentiment
FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
GROUP BY rating ORDER BY rating;""")

render_explanation("What this prompt does", """
Applies **CORTEX.SENTIMENT()** — a built-in AI function that scores text from -1 to +1:

- **Per-series breakdown**: Which device lines have the happiest/unhappiest customers?
- **Extreme reviews**: What are the strongest negative/positive signals?
- **Sentiment vs rating**: Do star ratings and AI sentiment agree? (They usually correlate but diverge on sarcastic or mixed reviews.)

**Key insight**: SENTIMENT() is a SQL function — you can use it in WHERE, GROUP BY, window functions, and views just like any other function. No Python, no API calls.
""")


PROMPT_5_2 = """Use SNOWFLAKE.CORTEX.COMPLETE() to classify customer feedback into topics. For each review in VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK:

1. Call CORTEX.COMPLETE('claude-sonnet-5', prompt) where the prompt asks the model to classify the feedback into exactly ONE of these topics:
   - picture_quality
   - audio_quality
   - smartcast_ui
   - wifi_connectivity
   - remote_control
   - app_performance
   - watchfree_plus
   - setup_experience
   - firmware_update
   - value_for_money
   - other

   The prompt should say: "Classify this VIZIO TV customer feedback into exactly one topic. Return ONLY the topic name, nothing else. Topics: picture_quality, audio_quality, smartcast_ui, wifi_connectivity, remote_control, app_performance, watchfree_plus, setup_experience, firmware_update, value_for_money, other. Feedback: {text}"

2. Show the distribution: how many reviews per topic?
3. For the top 3 topics, show the average sentiment score and average star rating
4. Show the top 3 most negative reviews for the wifi_connectivity topic

Limit to 50 reviews to manage cost."""

render_prompt("Prompt 5.2", "Topic Classification", PROMPT_5_2)

render_fallback_sql("Topic classification", """-- Classify feedback topics (limit 50 for cost)
WITH classified AS (
    SELECT *,
        TRIM(SNOWFLAKE.CORTEX.COMPLETE('claude-sonnet-5',
            'Classify this VIZIO TV customer feedback into exactly one topic. Return ONLY the topic name, nothing else. Topics: picture_quality, audio_quality, smartcast_ui, wifi_connectivity, remote_control, app_performance, watchfree_plus, setup_experience, firmware_update, value_for_money, other. Feedback: ' || feedback_text
        )) AS topic,
        SNOWFLAKE.CORTEX.SENTIMENT(feedback_text) AS sentiment
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
Uses **CORTEX.COMPLETE()** for **zero-shot text classification** — the model classifies feedback without any training data:

**Why this matters for VIZIO**:
- Product teams need to know what customers are talking about
- Manual review of thousands of feedbacks is impractical
- AI classification instantly surfaces: "42% of negative reviews mention wifi_connectivity"

**Prompt engineering**:
- Constrained output ("return ONLY the topic name") prevents verbose responses
- Fixed topic list ensures consistent, analyzable results
- Each topic maps to a VIZIO team (wifi → connectivity team, smartcast_ui → platform UX team)
""")


PROMPT_5_3 = """Use CORTEX.COMPLETE() to extract structured feature requests from customer feedback. For reviews where feedback_type = 'feature_request' in VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK:

1. Call CORTEX.COMPLETE('claude-sonnet-5', prompt) with a prompt that extracts a JSON object with:
   - feature_requested: what the customer wants (brief description)
   - category: which product area (smartcast, remote, picture, audio, apps, watchfree, other)
   - priority_signal: 'high' if the customer expresses frustration or says they'll switch brands, 'medium' if they suggest it would be nice, 'low' if it's a casual mention
   - competing_product_mentioned: any competitor mentioned (Roku, Fire TV, Apple TV, Samsung, LG, null if none)

2. Parse the JSON output and show a summary table of extracted feature requests
3. Which features are requested most often? Which have the most 'high' priority signals?
4. Which competing products are mentioned most in feature requests?

Limit to 30 reviews."""

render_prompt("Prompt 5.3", "Structured Feature Extraction", PROMPT_5_3)

render_fallback_sql("Feature extraction", """WITH requests AS (
    SELECT feedback_id, device_series, rating, feedback_text,
        SNOWFLAKE.CORTEX.COMPLETE('claude-sonnet-5',
            'Extract a JSON object from this VIZIO TV feature request. Fields: feature_requested (brief description), category (smartcast/remote/picture/audio/apps/watchfree/other), priority_signal (high if frustrated or will switch brands, medium if nice-to-have, low if casual), competing_product_mentioned (Roku/Fire TV/Apple TV/Samsung/LG/null). Return ONLY valid JSON. Feedback: ' || feedback_text
        ) AS extraction_raw
    FROM VIZIO_ANALYTICS_LAB.AI_OBJECTS.CUSTOMER_FEEDBACK
    WHERE feedback_type = 'feature_request'
    LIMIT 30
)
SELECT feedback_id, device_series, rating,
    TRY_PARSE_JSON(extraction_raw):feature_requested::VARCHAR AS feature_requested,
    TRY_PARSE_JSON(extraction_raw):category::VARCHAR AS category,
    TRY_PARSE_JSON(extraction_raw):priority_signal::VARCHAR AS priority_signal,
    TRY_PARSE_JSON(extraction_raw):competing_product_mentioned::VARCHAR AS competing_product
FROM requests;""")

render_explanation("What this prompt does", """
**Structured entity extraction** — turns unstructured text into queryable data:

- **feature_requested**: What do customers actually want?
- **priority_signal**: Which requests come from frustrated customers (churn risk)?
- **competing_product_mentioned**: Which competitors are winning mindshare?

**The JSON output pattern**: Ask the LLM to return valid JSON, then parse it with TRY_PARSE_JSON(). This lets you query AI-extracted fields with regular SQL.

**Business value**: Product managers can now query: "What are the top 5 high-priority feature requests where customers mention Roku?" — impossible without AI extraction.
""")


render_key_concepts([
    {"term": "CORTEX.SENTIMENT()", "definition": "Built-in function returning -1 to +1 sentiment score. Use directly in SQL like any function — in SELECT, WHERE, GROUP BY, window functions, views."},
    {"term": "CORTEX.COMPLETE()", "definition": "General-purpose LLM function. Takes a model name and prompt, returns text. Use for classification, extraction, summarization — any text-to-text task."},
    {"term": "Zero-Shot Classification", "definition": "Classifying text into categories without training data. The prompt provides the categories; the LLM uses its general knowledge to assign labels."},
    {"term": "Structured Extraction", "definition": "Using an LLM to extract structured data (JSON) from unstructured text. TRY_PARSE_JSON() then makes the extracted fields queryable in SQL."},
])

render_domain_glossary([
    {"term": "ACR (Automatic Content Recognition)", "definition": "VIZIO's Inscape technology that identifies what's playing on screen (including cable/satellite). Used for audience measurement. Privacy-regulated — users must opt in."},
    {"term": "OTT (Over-The-Top)", "definition": "Content delivered via the internet rather than cable/satellite. Netflix, Hulu, WatchFree+ are all OTT services. VIZIO's smart TV platform is an OTT delivery mechanism."},
])

render_what_you_built([
    "Sentiment analysis across all device series with star-rating correlation",
    "Zero-shot topic classification into 11 VIZIO-specific categories",
    "Structured feature request extraction with priority signals and competitor mentions",
])
