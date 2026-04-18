import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_domain_glossary, render_what_you_built

render_session_header(
    session_num=4,
    title="Snowpark ML & Model Development",
    time_range="10:55 - 11:25 AM",
    duration="30 min",
    building="Feature engineering, ML classification, Snowflake Notebook with Feature Store & Model Registry",
)

render_technologies_used([
    {"name": "Snowflake ML Classification", "description": "Built-in AutoML that trains, tunes, and evaluates classification models entirely within Snowflake. No external tools or data movement required.", "icon": "model_training"},
    {"name": "Feature Engineering Views", "description": "SQL views that transform raw operational data into ML-ready features. Views are computed on-the-fly so features always reflect the latest data.", "icon": "transform"},
    {"name": "Model Registry", "description": "Snowflake's native model registry stores trained models as first-class objects. Models can be called with SQL (MODEL!PREDICT) for inference.", "icon": "inventory_2"},
    {"name": "Feature Store", "description": "Centralized feature management for ML. Register entities, create managed feature views backed by Dynamic Tables, and generate point-in-time correct training datasets.", "icon": "hub"},
    {"name": "Snowflake Notebooks", "description": "Interactive Python/SQL notebooks that run inside Snowflake. Support Snowpark, ML libraries, and can be created programmatically via Cortex Code.", "icon": "description"},
])


PROMPT_4_1 = """In RETAIL_AI_DEMO.RETAIL_OPS, create a view called STOCKOUT_FEATURES that joins INVENTORY_LEVELS with PRODUCTS and STORES to build features for predicting stockouts. Include these features:

- quantity_on_hand, days_of_supply, reorder_point (from INVENTORY_LEVELS)
- retail_price, unit_cost, category (from PRODUCTS)
- store_type, square_footage (from STORES)
- EXTRACT(MONTH FROM snapshot_date) AS snapshot_month
- DAYOFWEEK(snapshot_date) AS snapshot_day_of_week
- CASE WHEN EXTRACT(MONTH FROM snapshot_date) IN (11,12) THEN 1 ELSE 0 END AS is_holiday_season
- status (from INVENTORY_LEVELS)
- A target column called IS_STOCKOUT: 1 if quantity_on_hand <= reorder_point * 0.3, else 0

Only include rows where quantity_on_hand is not null. Execute the SQL, then show me the feature distribution: count of stockout vs not-stockout, and the average values of key features for each class."""

render_prompt("Prompt 4.1", "Feature Engineering View", PROMPT_4_1)

render_explanation("What this prompt does", """
This creates a **feature engineering view** - the bridge between raw operational data and ML model training:

**Feature selection rationale**:
- `quantity_on_hand`, `days_of_supply`, `reorder_point` - Direct inventory health signals. Low quantity relative to reorder point is the strongest predictor.
- `retail_price`, `unit_cost` - Higher-priced items tend to have tighter inventory management (less tolerance for overstock or stockout).
- `category` - Different categories have different velocity patterns. Sneakers turn faster than outerwear; accessories are impulse buys.
- `store_type` - Flagship stores carry deeper inventory. Outlet stores have thinner margins and faster turns.
- `square_footage` - Larger stores can physically hold more inventory and typically maintain higher safety stock.
- `snapshot_month`, `is_holiday_season` - Seasonal demand patterns. November and December see 2-3x normal sell-through velocity for apparel, making stockouts more likely if not proactively managed.
- `snapshot_day_of_week` - Weekend vs weekday selling patterns differ significantly.

**Target variable**: `IS_STOCKOUT` is a binary classification label. We define a stockout risk as quantity on hand falling below 30% of the reorder point. This is a **supervised learning** problem.

**Why a view instead of a table**: Views are dynamic - they always reflect the current data. If new inventory snapshots are loaded, the view automatically includes them. This is important for the dynamic table scoring pipeline we build in later sessions.

**Feature engineering patterns in SQL**:
```sql
EXTRACT(MONTH FROM snapshot_date) AS snapshot_month,
DAYOFWEEK(snapshot_date) AS snapshot_day_of_week,
CASE WHEN EXTRACT(MONTH FROM snapshot_date) IN (11,12) THEN 1 ELSE 0 END AS is_holiday_season
```
""")


PROMPT_4_2 = """In RETAIL_AI_DEMO.RETAIL_OPS, use Snowpark ML to train a classification model to predict IS_STOCKOUT from our STOCKOUT_FEATURES view. Write and execute a Snowflake SQL script that:

1. Creates a STOCKOUT_FEATURES_TRAIN and STOCKOUT_FEATURES_TEST split (80/20) from STOCKOUT_FEATURES using a random seed
2. Uses Snowflake's built-in ML Classification:
   
   CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION STOCKOUT_PREDICTION_MODEL(
     INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'STOCKOUT_FEATURES_TRAIN'),
     TARGET_COLNAME => 'IS_STOCKOUT',
     CONFIG_OBJECT => {'on_error': 'skip'}
   );

First create the train/test views, then train the model, then run predictions on the test set and show the confusion matrix results (predicted vs actual counts). Also show the feature importances if available."""

render_prompt("Prompt 4.2", "Train a Classification Model", PROMPT_4_2)

render_explanation("What this prompt does", """
This trains a **classification model** using Snowflake's built-in ML:

**Train/Test Split**: We create two views that randomly partition the data:
```sql
CREATE VIEW STOCKOUT_FEATURES_TRAIN AS
  SELECT * FROM STOCKOUT_FEATURES SAMPLE (80) SEED(42);
CREATE VIEW STOCKOUT_FEATURES_TEST AS
  SELECT * FROM STOCKOUT_FEATURES
  WHERE snapshot_id NOT IN (SELECT snapshot_id FROM STOCKOUT_FEATURES_TRAIN);
```

**Snowflake ML Classification**: This is Snowflake's AutoML offering:
- Automatically handles categorical encoding (one-hot for category, store_type, etc.)
- Tries multiple algorithms (gradient boosting, random forest, etc.)
- Performs hyperparameter tuning
- Stores the best model as a first-class Snowflake object

**`SYSTEM$REFERENCE`**: This function creates a secure reference to a database object. It's required when passing tables/views to ML functions to ensure proper access control.

**Model as an object**: After training, `STOCKOUT_PREDICTION_MODEL` becomes a callable object in Snowflake. You invoke it with `STOCKOUT_PREDICTION_MODEL!PREDICT(...)`. This is fundamentally different from traditional ML where you need to export models, deploy them to serving infrastructure, and manage versioning separately.
""")


PROMPT_4_3 = """Using the STOCKOUT_PREDICTION_MODEL we just trained in RETAIL_AI_DEMO.RETAIL_OPS:

1. Run predictions on the test data view and store results in a table called STOCKOUT_PREDICTIONS
2. Calculate and display:
   - Overall accuracy
   - Precision and recall for the stockout class (IS_STOCKOUT = 1)
   - A confusion matrix showing TP, FP, TN, FN counts
3. Show the evaluation metrics from the model object itself using STOCKOUT_PREDICTION_MODEL!SHOW_EVALUATION_METRICS()
4. Show feature importances using STOCKOUT_PREDICTION_MODEL!SHOW_FEATURE_IMPORTANCE()

Execute all SQL and show results."""

render_prompt("Prompt 4.3", "Evaluate the Model", PROMPT_4_3)

render_explanation("What this prompt does", """
Model evaluation using both manual SQL calculations and built-in model methods:

**Manual evaluation** builds a confusion matrix:
- **True Positives (TP)**: Correctly predicted stockout risk
- **False Positives (FP)**: Predicted stockout but inventory was fine (false alarm)
- **True Negatives (TN)**: Correctly predicted no stockout
- **False Negatives (FN)**: Missed an actual stockout (dangerous)

**Accuracy** = (TP + TN) / Total. But accuracy alone is misleading if classes are imbalanced.

**Precision** = TP / (TP + FP). "Of all predicted stockout alerts, how many were real?"

**Recall** = TP / (TP + FN). "Of all actual stockouts, how many did we catch?"

For retail operations, **recall is more important** than precision - missing a stockout (FN) means:
- Lost sales (customers can't buy what they want)
- Customer churn (frustrated shoppers go to competitors)
- Broken size runs (a store has S and XL but not M or L, making the remaining stock unsellable)

A false alarm (FP) just means we order a little extra safety stock - a much cheaper mistake.

**Built-in methods**:
- `MODEL!SHOW_EVALUATION_METRICS()` - Returns AUC, F1, log loss, and more
- `MODEL!SHOW_FEATURE_IMPORTANCE()` - Shows which features the model relies on most
""")


st.divider()
st.markdown("#### Snowpark ML Continued — Feature Store, Model Registry & Notebooks")
st.caption("Now we'll build the same stockout prediction problem as a full ML pipeline inside a Snowflake Notebook, using Feature Store for feature management and Model Registry for versioning.")

st.warning("**Before continuing:** Open **Workspaces** in Snowflake (Snowsight) before running the next prompt. Cortex Code needs Workspaces enabled to create and manage Snowflake Notebooks.", icon=":material/warning:")

PROMPT_4_4 = """In RETAIL_AI_DEMO.RETAIL_OPS, create a Snowflake Notebook called STOCKOUT_ML_NOTEBOOK that builds an end-to-end ML pipeline using Snowflake's Feature Store and Model Registry. The notebook should have these sections:

SECTION 1 - Setup & Feature Store:
- Import snowflake.ml.feature_store (FeatureStore, FeatureView, Entity, CreationMode)
- Create a Feature Store in the RETAIL_OPS schema using the RETAIL_AI_WH warehouse
- Register a PRODUCT entity with PRODUCT_ID and STORE_ID as compound join keys
- Create a managed Feature View called STOCKOUT_FEATURE_VIEW that:
  - Queries INVENTORY_LEVELS joined with PRODUCTS and STORES
  - Includes the same features as our STOCKOUT_FEATURES view (quantity_on_hand, days_of_supply, reorder_point, retail_price, unit_cost, category, store_type, square_footage, snapshot_month, snapshot_day_of_week, is_holiday_season)
  - Includes IS_STOCKOUT as the label
  - Uses a 1-hour refresh frequency so features stay current
  - Has a timestamp_col for point-in-time correctness

SECTION 2 - Training Dataset Generation:
- Use fs.generate_dataset() with a spine DataFrame to create a point-in-time correct training dataset
- Split into train (80%) and test (20%) sets

SECTION 3 - Train Multiple Models:
- Train three traditional ML models on the same training data:
  1. XGBoost classifier (xgboost.XGBClassifier)
  2. Random Forest (sklearn.ensemble.RandomForestClassifier)
  3. Logistic Regression (sklearn.linear_model.LogisticRegression)
- For each model, calculate accuracy, precision, recall, and F1 score on the test set
- Display a comparison table of all three models side by side

SECTION 4 - Register Best Model:
- Identify which model performed best by F1 score
- Use snowflake.ml.registry.Registry to register the best model with log_model()
- Name it STOCKOUT_PREDICTOR, version V1
- Include sample_input_data for schema inference and explainability
- Set target_platforms to WAREHOUSE so it can be called via SQL
- Log the evaluation metrics on the model version

SECTION 5 - Validate Registered Model:
- Run SHOW MODELS in the schema to confirm registration
- Test the registered model by calling MODEL(RETAIL_AI_DEMO.RETAIL_OPS.STOCKOUT_PREDICTOR, V1)!PREDICT() on sample data from the test set
- Compare the registered model's predictions with the in-memory predictions to confirm they match

Make the notebook well-documented with markdown cells explaining each section.

Do NOT run the notebook — just create it. We will run it in the next step."""

render_prompt("Prompt 4.4", "Create ML Pipeline Notebook", PROMPT_4_4)

render_explanation("What this prompt does", """
Creates a **Snowflake Notebook** with a complete ML pipeline that uses three key Snowflake ML services:

**Feature Store** (`snowflake.ml.feature_store`):
```python
fs = FeatureStore(
    session=session,
    database="RETAIL_AI_DEMO",
    name="RETAIL_OPS",
    default_warehouse="RETAIL_AI_WH",
    creation_mode=CreationMode.CREATE_IF_NOT_EXIST
)

entity = Entity(name="PRODUCT", join_keys=["PRODUCT_ID", "STORE_ID"])
fs.register_entity(entity)

fv = FeatureView(
    name="STOCKOUT_FEATURE_VIEW",
    entities=[entity],
    feature_df=feature_query_df,
    timestamp_col="SNAPSHOT_DATE",
    refresh_freq="1 hour"
)
fv = fs.register_feature_view(fv, version="V1")
```
Feature views are backed by **Dynamic Tables** — Snowflake automatically keeps them refreshed.

**Training dataset with point-in-time correctness**:
```python
dataset = fs.generate_dataset(
    name="STOCKOUT_TRAINING_DATA",
    spine_df=spine_df,
    features=[fv],
    spine_timestamp_col="SNAPSHOT_DATE",
    spine_label_cols=["IS_STOCKOUT"]
)
```
This prevents **data leakage** — each row only sees features available at the time of that inventory snapshot.

**Model comparison** trains three classifiers and picks the best:
- **XGBoost**: Gradient boosted trees — typically best for tabular data
- **Random Forest**: Ensemble of decision trees — robust, less prone to overfitting
- **Logistic Regression**: Linear model — fast, interpretable baseline

**Model Registry** (`snowflake.ml.registry.Registry`):
```python
reg = Registry(session=session, database_name="RETAIL_AI_DEMO", schema_name="RETAIL_OPS")
mv = reg.log_model(
    best_model,
    model_name="STOCKOUT_PREDICTOR",
    version_name="V1",
    sample_input_data=X_test.head(5),
    target_platforms=["WAREHOUSE"],
    metrics={"f1": best_f1, "accuracy": best_acc}
)
```
Once registered, the model becomes a SQL-callable Snowflake object.

**Why this matters**: Prompts 4.1-4.3 used Snowflake's built-in AutoML (zero code). This notebook shows the alternative — training your own models with full control over algorithm choice, hyperparameters, and evaluation. Both approaches register models as first-class Snowflake objects.
""")


PROMPT_4_5 = """Open the STOCKOUT_ML_NOTEBOOK in Snowsight and run all cells. After execution completes, show me:

1. The feature store entities and feature views: list them with SQL (SHOW FEATURE VIEWS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS)
2. The model comparison results — which model won and by how much?
3. The registered model: SHOW MODELS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS and SHOW FUNCTIONS IN MODEL RETAIL_AI_DEMO.RETAIL_OPS.STOCKOUT_PREDICTOR
4. A SQL query that uses the registered model for inference:
   SELECT SNAPSHOT_ID, PRODUCT_ID, STORE_ID,
          MODEL(RETAIL_AI_DEMO.RETAIL_OPS.STOCKOUT_PREDICTOR, V1)!PREDICT(quantity_on_hand, days_of_supply, reorder_point, retail_price, unit_cost, category, store_type, square_footage, snapshot_month, snapshot_day_of_week, is_holiday_season) AS prediction
   FROM STOCKOUT_FEATURES
   LIMIT 10;"""

render_prompt("Prompt 4.5", "Run Notebook & Verify", PROMPT_4_5)

render_explanation("What this prompt does", """
Runs the notebook end-to-end and verifies all artifacts were created:

**Feature Store verification**:
- `SHOW FEATURE VIEWS` lists managed feature views with their backing Dynamic Table, refresh frequency, and status
- Feature views marked as `ACTIVE` are being refreshed automatically by Snowflake

**Model comparison**: The notebook prints a side-by-side table like:
| Model | Accuracy | Precision | Recall | F1 |
|-------|----------|-----------|--------|----|
| XGBoost | 0.85 | 0.82 | 0.79 | 0.80 |
| Random Forest | 0.83 | 0.80 | 0.76 | 0.78 |
| Logistic Regression | 0.78 | 0.74 | 0.71 | 0.72 |

**Model Registry verification**:
- `SHOW MODELS` confirms the model object exists
- `SHOW FUNCTIONS IN MODEL` lists callable methods (PREDICT, PREDICT_PROBA)

**SQL inference**: The `MODEL(name, version)!PREDICT()` syntax calls the registered model directly from SQL — no Python needed. This is what makes Snowflake ML unique: models trained in Python become SQL functions accessible to any analyst. A merchandiser can run stockout predictions without writing a single line of Python.
""")


render_key_concepts([
    {"term": "Snowflake ML Classification", "definition": "Snowflake's built-in AutoML for binary and multi-class classification. It automatically handles feature encoding, model selection, hyperparameter tuning, and evaluation. Models are stored as first-class Snowflake objects."},
    {"term": "Feature Engineering", "definition": "The process of transforming raw data into features that better represent the underlying problem for ML models. Good features are often more important than complex algorithms."},
    {"term": "SYSTEM$REFERENCE", "definition": "A Snowflake system function that creates a secure, permissions-aware reference to a database object. Required when passing tables or views to ML training functions."},
    {"term": "Confusion Matrix", "definition": "A 2x2 table showing True Positives, False Positives, True Negatives, and False Negatives. The foundation for calculating precision, recall, F1 score, and other classification metrics."},
    {"term": "Feature Store", "definition": "A centralized repository for ML features (snowflake.ml.feature_store). You register Entities (join keys like PRODUCT_ID + STORE_ID), then create Feature Views — managed (backed by Dynamic Tables with automatic refresh) or external (backed by views). The store provides generate_dataset() for point-in-time correct training data and retrieve_feature_values() for inference."},
    {"term": "Model Registry", "definition": "Snowflake's native model versioning system (snowflake.ml.registry.Registry). Use log_model() to register any Python model (sklearn, XGBoost, etc.) as a first-class Snowflake object. Registered models can be called via SQL with MODEL(name, version)!PREDICT() and support explainability via SHAP."},
    {"term": "Snowflake Notebook", "definition": "An interactive notebook that runs inside Snowflake with access to Snowpark, snowflake-ml-python, and other libraries. Notebooks can mix SQL and Python cells, and are created as Snowflake objects that can be shared via RBAC."},
])

render_domain_glossary([
    {"term": "Stockout", "definition": "When a product is completely out of stock at a store or online. Stockouts in apparel are especially damaging because customers rarely wait — they buy from a competitor or substitute a different product, often permanently shifting loyalty."},
    {"term": "Safety Stock", "definition": "Extra inventory held as a buffer against demand variability and supply delays. Calculated based on demand forecast accuracy, supplier lead time variability, and desired service level (e.g., 95% in-stock rate)."},
    {"term": "Reorder Point", "definition": "The inventory level that triggers a new purchase order. Calculated as (average daily demand x lead time in days) + safety stock. When quantity on hand falls below the reorder point, it's time to reorder."},
    {"term": "Holiday Season", "definition": "November and December account for 20-30% of annual retail revenue. Apparel retailers plan holiday inventory 6-9 months in advance. Stockouts during this period are the most costly because demand peaks and restocking lead times make recovery impossible."},
])

render_what_you_built([
    "STOCKOUT_FEATURES view with 11+ engineered features",
    "Train/test data split views (80/20)",
    "STOCKOUT_PREDICTION_MODEL - trained classification model",
    "STOCKOUT_PREDICTIONS table with scored test data",
    "Evaluation metrics: accuracy, precision, recall, confusion matrix",
    "Snowflake Notebook with end-to-end ML pipeline",
    "Feature Store with PRODUCT entity and STOCKOUT_FEATURE_VIEW",
    "XGBoost, Random Forest, and Logistic Regression models compared",
    "Best model registered as STOCKOUT_PREDICTOR V1 in Snowflake Model Registry",
])
