"""Pre-built fallback SQL for every workshop prompt.

Each constant mirrors a prompt (FB_<session>_<prompt>). Run the SQL in a Snowsight
worksheet when short on time. Fallbacks are designed to run in order and build on
each other, exactly like the prompts. Synthetic data is deterministic (HASH-based)
so every participant gets the same rows.
"""

# ---------------------------------------------------------------------------
# Session 1 - Foundation & Reference Data
# ---------------------------------------------------------------------------

FB_1_1 = """CREATE DATABASE IF NOT EXISTS RETAIL_AI_DEMO
  COMMENT = 'Retail AI/ML Workshop - Apparel & Footwear Operations';
CREATE SCHEMA IF NOT EXISTS RETAIL_AI_DEMO.RETAIL_OPS;
CREATE WAREHOUSE IF NOT EXISTS RETAIL_AI_WH
  WAREHOUSE_SIZE = 'MEDIUM' AUTO_SUSPEND = 300 AUTO_RESUME = TRUE;

USE WAREHOUSE RETAIL_AI_WH;
USE DATABASE RETAIL_AI_DEMO;
USE SCHEMA RETAIL_OPS;

CREATE OR REPLACE TABLE PRODUCTS (
  product_id INTEGER, product_name VARCHAR, category VARCHAR, subcategory VARCHAR,
  brand VARCHAR, size_range VARCHAR, color VARCHAR, unit_cost NUMBER(10,2),
  retail_price NUMBER(10,2), margin_pct NUMBER(5,1), season VARCHAR, gender VARCHAR
);

INSERT INTO PRODUCTS
SELECT column1, column2, column3, column4, column5, column6, column7, column8, column9,
       ROUND((column9 - column8) / column9 * 100, 1), column10, column11
FROM VALUES
  (1,  'Nike Air Zoom Pegasus 41',              'sneakers',    'running',      'Nike',           '7-13',     'Black/White',      62.00, 140.00, 'year_round', 'mens'),
  (2,  'Adidas Ultraboost Light',               'sneakers',    'running',      'Adidas',         '5-11',     'Cloud White',      85.00, 190.00, 'year_round', 'womens'),
  (3,  'New Balance 990v6',                     'sneakers',    'lifestyle',    'New Balance',    '7-14',     'Grey',             90.00, 200.00, 'year_round', 'unisex'),
  (4,  'Summit Performance Tee',                'activewear',  'tops',         'Summit',         'XS-XXL',   'Navy',              7.50,  28.00, 'year_round', 'mens'),
  (5,  'Summit Flex Leggings',                  'activewear',  'bottoms',      'Summit',         'XS-XL',    'Black',            11.00,  48.00, 'year_round', 'womens'),
  (6,  'Summit Trail Running Shorts',           'activewear',  'shorts',       'Summit',         'S-XXL',    'Olive',             8.00,  34.00, 'summer',     'mens'),
  (7,  'Basecamp Fleece Hoodie',                'tops',        'hoodies',      'Basecamp',       'XS-XXL',   'Heather Grey',     12.00,  45.00, 'fall',       'unisex'),
  (8,  'Basecamp Everyday Chino',               'bottoms',     'pants',        'Basecamp',       '28-40',    'Khaki',            10.00,  40.00, 'year_round', 'mens'),
  (9,  'Basecamp Crew Socks 3-Pack',            'accessories', 'socks',        'Basecamp',       'S-L',      'White',             3.00,  14.00, 'year_round', 'unisex'),
  (10, 'Levi''s 501 Original Jeans',            'bottoms',     'denim',        'Levi''s',        '28-40',    'Medium Stonewash', 32.00,  79.50, 'year_round', 'mens'),
  (11, 'Levi''s Wedgie Straight Jeans',         'bottoms',     'denim',        'Levi''s',        '24-32',    'Light Indigo',     34.00,  89.50, 'year_round', 'womens'),
  (12, 'The North Face Nuptse Puffer Jacket',   'outerwear',   'insulated',    'The North Face', 'XS-XXL',   'Black',           140.00, 320.00, 'winter',     'unisex'),
  (13, 'The North Face Venture 2 Rain Jacket',  'outerwear',   'rain',         'The North Face', 'S-XXL',    'Shady Blue',       48.00, 110.00, 'spring',     'mens'),
  (14, 'Columbia Bugaboot III',                 'boots',       'winter_boots', 'Columbia',       '7-13',     'Brown',            45.00, 110.00, 'winter',     'mens'),
  (15, 'Columbia Newton Ridge Hiking Boot',     'boots',       'hiking',       'Columbia',       '5-11',     'Dark Grey',        38.00,  90.00, 'fall',       'womens'),
  (16, 'Under Armour HeatGear Compression Shirt','activewear', 'tops',         'Under Armour',   'S-XXL',    'Red',              13.00,  35.00, 'summer',     'mens'),
  (17, 'Under Armour Charged Assert 10',        'sneakers',    'training',     'Under Armour',   '7-13',     'Black',            32.00,  75.00, 'year_round', 'mens'),
  (18, 'Nike Kids Revolution 7',                'sneakers',    'kids',         'Nike',           '10C-7Y',   'Blue/Volt',        22.00,  50.00, 'year_round', 'kids'),
  (19, 'Adidas Adilette Slides',                'sandals',     'slides',       'Adidas',         '4-14',     'Black/White',      12.00,  35.00, 'summer',     'unisex'),
  (20, 'Summit Recovery Sandal',                'sandals',     'sport',        'Summit',         '5-13',     'Charcoal',          9.00,  38.00, 'summer',     'unisex'),
  (21, 'Basecamp Leather Oxford',               'dress_shoes', 'oxfords',      'Basecamp',       '7-13',     'Cognac',           28.00,  95.00, 'year_round', 'mens'),
  (22, 'Basecamp Block Heel Pump',              'dress_shoes', 'heels',        'Basecamp',       '5-10',     'Black Patent',     24.00,  85.00, 'year_round', 'womens'),
  (23, 'Columbia Bugaboo Kids Snow Jacket',     'outerwear',   'insulated',    'Columbia',       '4-16',     'Pink',             30.00,  75.00, 'winter',     'kids'),
  (24, 'Summit Packable Windbreaker',           'outerwear',   'shell',        'Summit',         'XS-XXL',   'Teal',             14.00,  59.00, 'spring',     'womens'),
  (25, 'The North Face Borealis Backpack',      'accessories', 'bags',         'The North Face', 'One Size', 'Black',            42.00,  99.00, 'year_round', 'unisex');

CREATE OR REPLACE TABLE STORES (
  store_id INTEGER, store_name VARCHAR, city VARCHAR, state VARCHAR, store_type VARCHAR,
  latitude FLOAT, longitude FLOAT, square_footage INTEGER, annual_revenue_millions NUMBER(6,1)
);

INSERT INTO STORES VALUES
  (1, 'Alpine & Co. Fifth Avenue',      'New York',    'NY', 'flagship', 40.7580,  -73.9855, 42000, 68.5),
  (2, 'Alpine & Co. The Grove',         'Los Angeles', 'CA', 'mall',     34.0719, -118.3576, 24000, 31.2),
  (3, 'Alpine & Co. Magnificent Mile',  'Chicago',     'IL', 'flagship', 41.8947,  -87.6246, 36000, 52.4),
  (4, 'Alpine & Co. Katy Mills Outlet', 'Houston',     'TX', 'outlet',   29.7752,  -95.8085, 18000, 14.8),
  (5, 'Alpine & Co. Pioneer Place',     'Portland',    'OR', 'mall',     45.5187, -122.6774, 21000, 22.6),
  (6, 'Alpine & Co. Cherry Creek',      'Denver',      'CO', 'mall',     39.7171, -104.9530, 23000, 26.9),
  (7, 'Alpine & Co. Dolphin Outlet',    'Miami',       'FL', 'outlet',   25.7880,  -80.3800, 19500, 17.3),
  (8, 'Alpine & Co. Pike Place',        'Seattle',     'WA', 'flagship', 47.6097, -122.3422, 33000, 47.1);

CREATE OR REPLACE TABLE SUPPLIERS (
  supplier_id INTEGER, company_name VARCHAR, country VARCHAR, region VARCHAR,
  primary_category VARCHAR, lead_time_days INTEGER, reliability_score INTEGER,
  annual_volume_units INTEGER, payment_terms VARCHAR
);

INSERT INTO SUPPLIERS VALUES
  (1,  'Carolina Knitworks',                'USA',        'Domestic',     'activewear',  14, 9, 180000, 'Net 30'),
  (2,  'Pacific Denim Mills',               'USA',        'Domestic',     'bottoms',     21, 8, 120000, 'Net 45'),
  (3,  'Rocky Mountain Leather Co.',        'USA',        'Domestic',     'boots',       28, 8,  45000, 'Net 30'),
  (4,  'Saigon Apparel Group',              'Vietnam',    'Asia-Pacific', 'tops',        60, 7, 650000, 'Net 60'),
  (5,  'Mekong Footwear Ltd.',              'Vietnam',    'Asia-Pacific', 'sneakers',    75, 8, 420000, 'Net 60'),
  (6,  'Guangzhou Outerwear Manufacturing', 'China',      'Asia-Pacific', 'outerwear',   70, 6, 310000, 'Net 60'),
  (7,  'Dongguan Sole Technologies',        'China',      'Asia-Pacific', 'sneakers',    65, 7, 520000, 'Net 75'),
  (8,  'Dhaka Garment Works',               'Bangladesh', 'Asia-Pacific', 'tops',        80, 5, 900000, 'Net 90'),
  (9,  'Chittagong Knit Exports',           'Bangladesh', 'Asia-Pacific', 'activewear',  85, 6, 700000, 'Net 90'),
  (10, 'Jakarta Textile Industries',        'Indonesia',  'Asia-Pacific', 'bottoms',     72, 7, 380000, 'Net 60'),
  (11, 'Textiles del Bajio S.A. de C.V.',   'Mexico',     'Americas',     'bottoms',     25, 7, 200000, 'Net 45'),
  (12, 'Calzaturificio Marche',             'Italy',      'Europe',       'dress_shoes', 45, 9,  60000, 'Net 45'),
  (13, 'Tessuti Biella S.p.A.',             'Italy',      'Europe',       'outerwear',   50, 9,  40000, 'Net 45'),
  (14, 'Porto Shoe Factory',                'Portugal',   'Europe',       'dress_shoes', 40, 8,  85000, 'Net 45'),
  (15, 'Calzado Leon S.A.',                 'Mexico',     'Americas',     'boots',       30, 7,  90000, 'Net 45');"""

FB_1_2 = """SELECT 'PRODUCTS' AS table_name, COUNT(*) AS row_count FROM RETAIL_AI_DEMO.RETAIL_OPS.PRODUCTS
UNION ALL SELECT 'STORES', COUNT(*) FROM RETAIL_AI_DEMO.RETAIL_OPS.STORES
UNION ALL SELECT 'SUPPLIERS', COUNT(*) FROM RETAIL_AI_DEMO.RETAIL_OPS.SUPPLIERS;

SELECT * FROM RETAIL_AI_DEMO.RETAIL_OPS.PRODUCTS LIMIT 3;
SELECT * FROM RETAIL_AI_DEMO.RETAIL_OPS.STORES LIMIT 3;
SELECT * FROM RETAIL_AI_DEMO.RETAIL_OPS.SUPPLIERS LIMIT 3;"""

# ---------------------------------------------------------------------------
# Session 2 - Preparing Data for AI
# ---------------------------------------------------------------------------

FB_2_1 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- SALES_TRANSACTIONS: 200 rows, skewed to Nov-Dec (holiday) and August (back-to-school)
CREATE OR REPLACE TABLE SALES_TRANSACTIONS AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 200))
), b AS (
  SELECT n,
    UNIFORM(1, 8, HASH(n, 'store')) AS store_id,
    UNIFORM(1, 25, HASH(n, 'product')) AS product_id,
    UNIFORM(0::FLOAT, 1::FLOAT, HASH(n, 'season')) AS r_season,
    UNIFORM(0::FLOAT, 1::FLOAT, HASH(n, 'channel')) AS r_channel
  FROM g
), d AS (
  SELECT b.*,
    CASE WHEN r_season < 0.30 THEN DATEADD(day, UNIFORM(0, 60, HASH(n, 'd1')), '2025-11-01'::DATE)
         WHEN r_season < 0.42 THEN DATEADD(day, UNIFORM(0, 30, HASH(n, 'd2')), '2025-08-01'::DATE)
         ELSE DATEADD(day, UNIFORM(0, 460, HASH(n, 'd3')), '2025-01-01'::DATE) END AS transaction_date
  FROM b
), x AS (
  SELECT d.*, p.retail_price, s.store_type,
    CASE WHEN MONTH(transaction_date) IN (11, 12) THEN UNIFORM(15, 40, HASH(n, 'disc'))
         WHEN s.store_type = 'outlet' THEN UNIFORM(20, 35, HASH(n, 'disc'))
         WHEN UNIFORM(0, 9, HASH(n, 'promo')) < 3 THEN UNIFORM(5, 15, HASH(n, 'disc'))
         ELSE 0 END AS discount_pct,
    UNIFORM(1, 4, HASH(n, 'qty')) AS quantity
  FROM d JOIN PRODUCTS p ON p.product_id = d.product_id JOIN STORES s ON s.store_id = d.store_id
)
SELECT n AS transaction_id, store_id, product_id,
  'C' || LPAD(UNIFORM(1, 120, HASH(n, 'cust'))::VARCHAR, 5, '0') AS customer_id,
  transaction_date, quantity, retail_price AS unit_price, discount_pct::NUMBER(5,1) AS discount_pct,
  ROUND(quantity * retail_price * (1 - discount_pct / 100), 2)::NUMBER(10,2) AS total_amount,
  ARRAY_CONSTRUCT('credit_card', 'credit_card', 'debit', 'cash', 'mobile_pay', 'gift_card')[UNIFORM(0, 5, HASH(n, 'pay'))]::VARCHAR AS payment_method,
  CASE WHEN r_channel < 0.55 THEN 'in_store' WHEN r_channel < 0.90 THEN 'online' ELSE 'bopis' END AS channel,
  UNIFORM(0, 99, HASH(n, 'loyal')) < 55 AS loyalty_member
FROM x;

-- PURCHASE_ORDERS: 300 rows with partial shipments and late deliveries
CREATE OR REPLACE TABLE PURCHASE_ORDERS AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 300))
), b AS (
  SELECT n,
    UNIFORM(1, 15, HASH(n, 'sup')) AS supplier_id,
    UNIFORM(1, 25, HASH(n, 'prod')) AS product_id,
    DATEADD(day, UNIFORM(0, 450, HASH(n, 'od')), '2025-01-01'::DATE) AS order_date,
    UNIFORM(2, 40, HASH(n, 'qo')) * 50 AS quantity_ordered,
    UNIFORM(0, 99, HASH(n, 'status')) AS r_status,
    UNIFORM(0, 99, HASH(n, 'late')) AS r_late
  FROM g
), x AS (
  SELECT b.*, s.lead_time_days, p.unit_cost AS base_cost,
    CASE WHEN r_status < 65 THEN 'received' WHEN r_status < 77 THEN 'partial'
         WHEN r_status < 87 THEN 'shipped'  WHEN r_status < 95 THEN 'ordered' ELSE 'cancelled' END AS status
  FROM b JOIN SUPPLIERS s ON s.supplier_id = b.supplier_id JOIN PRODUCTS p ON p.product_id = b.product_id
)
SELECT n AS po_id, supplier_id, product_id, order_date,
  DATEADD(day, lead_time_days, order_date) AS expected_delivery_date,
  CASE WHEN status IN ('received', 'partial')
       THEN DATEADD(day, lead_time_days + IFF(r_late < 28, UNIFORM(3, 20, HASH(n, 'delay')), UNIFORM(-3, 0, HASH(n, 'delay'))), order_date)
  END AS actual_delivery_date,
  quantity_ordered,
  CASE WHEN status = 'received' THEN quantity_ordered
       WHEN status = 'partial'  THEN ROUND(quantity_ordered * UNIFORM(60, 95, HASH(n, 'pct')) / 100)
       ELSE 0 END AS quantity_received,
  ROUND(base_cost * UNIFORM(95, 105, HASH(n, 'cost')) / 100, 2)::NUMBER(10,2) AS unit_cost,
  ROUND(quantity_ordered * base_cost * UNIFORM(95, 105, HASH(n, 'cost')) / 100, 2)::NUMBER(12,2) AS total_cost,
  status,
  UNIFORM(1, 8, HASH(n, 'dest')) AS destination_store_id
FROM x;

-- INVENTORY_LEVELS: 150 rows; seasonal items run low in peak season, overstock off-season
CREATE OR REPLACE TABLE INVENTORY_LEVELS AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 150))
), b AS (
  SELECT n,
    UNIFORM(1, 8, HASH(n, 'store')) AS store_id,
    UNIFORM(1, 25, HASH(n, 'prod')) AS product_id,
    DATEADD(day, -UNIFORM(0, 365, HASH(n, 'date')), CURRENT_DATE()) AS snapshot_date,
    UNIFORM(20, 60, HASH(n, 'rop')) AS reorder_point,
    UNIFORM(2, 12, HASH(n, 'rate')) AS daily_rate,
    UNIFORM(0::FLOAT, 1::FLOAT, HASH(n, 'risk')) AS r_risk
  FROM g
), s AS (
  SELECT b.*, p.category,
    (p.category IN ('outerwear', 'boots') AND MONTH(snapshot_date) IN (11, 12, 1, 2))
      OR (p.category = 'sandals' AND MONTH(snapshot_date) IN (5, 6, 7, 8))
      OR MONTH(snapshot_date) IN (11, 12) AS in_peak,
    (p.category IN ('outerwear', 'boots') AND MONTH(snapshot_date) IN (5, 6, 7, 8))
      OR (p.category = 'sandals' AND MONTH(snapshot_date) IN (11, 12, 1, 2)) AS off_season
  FROM b JOIN PRODUCTS p ON p.product_id = b.product_id
), q AS (
  SELECT s.*,
    CASE WHEN r_risk < IFF(in_peak, 0.45, 0.18) THEN ROUND(reorder_point * GREATEST(0, UNIFORM(-10, 45, HASH(n, 'low'))) / 100)
         WHEN off_season THEN ROUND(reorder_point * UNIFORM(350, 600, HASH(n, 'over')) / 100)
         ELSE ROUND(reorder_point * UNIFORM(60, 400, HASH(n, 'ok')) / 100) END AS quantity_on_hand
  FROM s
)
SELECT n AS snapshot_id, store_id, product_id, snapshot_date, quantity_on_hand::INTEGER AS quantity_on_hand,
  LEAST(quantity_on_hand, UNIFORM(0, 8, HASH(n, 'res')))::INTEGER AS quantity_reserved,
  IFF(quantity_on_hand <= reorder_point, UNIFORM(50, 300, HASH(n, 'oo')), 0)::INTEGER AS quantity_on_order,
  reorder_point,
  ROUND(quantity_on_hand / daily_rate, 1) AS days_of_supply,
  CASE WHEN quantity_on_hand = 0 THEN 'out_of_stock'
       WHEN quantity_on_hand <= reorder_point THEN 'low_stock'
       WHEN quantity_on_hand > reorder_point * 3.5 THEN 'overstock'
       ELSE 'in_stock' END AS status
FROM q;

SELECT 'SALES_TRANSACTIONS' t, COUNT(*) c FROM SALES_TRANSACTIONS
UNION ALL SELECT 'PURCHASE_ORDERS', COUNT(*) FROM PURCHASE_ORDERS
UNION ALL SELECT 'INVENTORY_LEVELS', COUNT(*) FROM INVENTORY_LEVELS;"""

FB_2_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- STORE_FOOT_TRAFFIC: 500 hourly readings over the past 30 days (store hours 10am-9pm)
CREATE OR REPLACE TABLE STORE_FOOT_TRAFFIC AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 500))
), b AS (
  SELECT n, UNIFORM(1, 8, HASH(n, 'store')) AS store_id,
    DATEADD(day, -UNIFORM(0, 29, HASH(n, 'day')), CURRENT_DATE()) AS d,
    UNIFORM(10, 21, HASH(n, 'hour')) AS h
  FROM g
), x AS (
  SELECT b.*, s.store_type,
    DAYOFWEEKISO(d) IN (6, 7) AS is_weekend,
    MOD(ABS(HASH(d)), 12) = 0 AS is_holiday
  FROM b JOIN STORES s ON s.store_id = b.store_id
)
SELECT n AS traffic_id, store_id,
  DATEADD(hour, h, d::TIMESTAMP_NTZ) AS timestamp,
  ROUND(DECODE(store_type, 'flagship', 180, 'outlet', 130, 110)
        * IFF(h BETWEEN 12 AND 18, 1.25, 0.8)
        * IFF(is_weekend OR is_holiday, 1.35, 1.0)
        * UNIFORM(80, 120, HASH(n, 'noise')) / 100)::INTEGER AS visitor_count,
  UNIFORM(120, 350, HASH(n, 'conv')) / 10 AS conversion_rate_pct,
  ROUND(DECODE(store_type, 'flagship', 110, 'outlet', 62, 85) * UNIFORM(80, 125, HASH(n, 'basket')) / 100, 2) AS avg_basket_size,
  ARRAY_CONSTRUCT('sunny', 'sunny', 'cloudy', 'rain', 'snow')[UNIFORM(0, 4, HASH(d, store_id, 'wx'))]::VARCHAR AS weather_condition,
  is_weekend, is_holiday
FROM x;

-- DAILY_SALES_METRICS: 8 stores x 50 days = 400 rows
CREATE OR REPLACE TABLE DAILY_SALES_METRICS AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 400))
), b AS (
  SELECT n, MOD(n - 1, 8) + 1 AS store_id, DATEADD(day, -FLOOR((n - 1) / 8), CURRENT_DATE()) AS date FROM g
), x AS (
  SELECT b.*, s.store_type, s.annual_revenue_millions,
    DECODE(s.store_type, 'flagship', 95, 'outlet', 55, 80) AS atv,
    ROUND(s.annual_revenue_millions * 1000000 / 365
          * IFF(DAYOFWEEKISO(date) IN (6, 7), 1.3, 0.9)
          * UNIFORM(85, 115, HASH(n, 'rev')) / 100, 2) AS total_revenue
  FROM b JOIN STORES s ON s.store_id = b.store_id
)
SELECT n AS metric_id, store_id, date, total_revenue,
  ROUND(total_revenue / atv)::INTEGER AS transaction_count,
  ROUND(atv * UNIFORM(92, 108, HASH(n, 'atv')) / 100, 2) AS avg_transaction_value,
  ROUND(total_revenue / atv * 2.1)::INTEGER AS units_sold,
  ROUND(total_revenue / atv * UNIFORM(4, 12, HASH(n, 'ret')) / 100)::INTEGER AS returns_count,
  ROUND(total_revenue * UNIFORM(4, 12, HASH(n, 'ret')) / 100 * 0.9, 2) AS returns_value,
  UNIFORM(10, 80, HASH(n, 'online'))::INTEGER AS online_orders_fulfilled
FROM x;

-- WEBSITE_CLICKSTREAM: 300 events with funnel drop-off
CREATE OR REPLACE TABLE WEBSITE_CLICKSTREAM AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 300))
), b AS (
  SELECT n, UNIFORM(0, 99, HASH(n, 'page')) AS r_page, UNIFORM(0, 99, HASH(n, 'dev')) AS r_dev FROM g
), x AS (
  SELECT b.*,
    CASE WHEN r_page < 30 THEN 'home' WHEN r_page < 57 THEN 'category' WHEN r_page < 70 THEN 'search'
         WHEN r_page < 88 THEN 'product' WHEN r_page < 96 THEN 'cart' ELSE 'checkout' END AS page_type
  FROM b
)
SELECT n AS click_id,
  'S' || LPAD(UNIFORM(1, 90, HASH(n, 'sess'))::VARCHAR, 4, '0') AS session_id,
  DATEADD(second, -UNIFORM(0, 2592000, HASH(n, 'ts')), DATE_TRUNC('hour', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ) AS timestamp,
  page_type,
  IFF(page_type = 'product', UNIFORM(1, 25, HASH(n, 'prod')), NULL) AS product_id,
  CASE WHEN r_dev < 58 THEN 'mobile' WHEN r_dev < 92 THEN 'desktop' ELSE 'tablet' END AS device_type,
  ARRAY_CONSTRUCT('direct', 'search', 'search', 'social', 'email')[UNIFORM(0, 4, HASH(n, 'ref'))]::VARCHAR AS referral_source,
  UNIFORM(5, 300, HASH(n, 'top')) AS time_on_page_seconds
FROM x;

-- INVENTORY_SNAPSHOTS: 200 rows; some projected to stock out within 7 days
CREATE OR REPLACE TABLE INVENTORY_SNAPSHOTS AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 200))
), b AS (
  SELECT n,
    UNIFORM(1, 25, HASH(n, 'prod')) AS product_id,
    UNIFORM(1, 8, HASH(n, 'store')) AS store_id,
    DATEADD(minute, -UNIFORM(0, 20160, HASH(n, 'ts')), DATE_TRUNC('hour', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ) AS timestamp,
    IFF(UNIFORM(0, 99, HASH(n, 'low')) < 22, UNIFORM(0, 15, HASH(n, 'qa')), UNIFORM(16, 300, HASH(n, 'qa'))) AS quantity_available,
    UNIFORM(1, 25, HASH(n, 'sold')) AS quantity_sold_today
  FROM g
)
SELECT n AS snapshot_id, product_id, store_id, timestamp, quantity_available, quantity_sold_today,
  DATEADD(day, FLOOR(quantity_available / quantity_sold_today), timestamp::DATE) AS projected_stockout_date,
  CASE WHEN quantity_available / quantity_sold_today <= 3 THEN 'critical'
       WHEN quantity_available / quantity_sold_today <= 7 THEN 'urgent'
       WHEN quantity_available / quantity_sold_today <= 14 THEN 'ordered'
       ELSE 'adequate' END AS replenishment_status
FROM b;"""

FB_2_3 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- CUSTOMER_REVIEWS: 30 detailed reviews assembled from fit / quality / comfort / value themes
CREATE OR REPLACE TABLE CUSTOMER_REVIEWS AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 30))
), b AS (
  SELECT n, MOD(n * 7, 25) + 1 AS product_id,
    ARRAY_CONSTRUCT(5,4,2,5,1,3,4,5,2,4,3,1,5,4,2,5,3,4,1,5,2,4,5,3,1,4,5,2,3,4)[n - 1]::INTEGER AS rating
  FROM g
), t AS (
  SELECT b.*, p.product_name,
    p.category IN ('sneakers', 'boots', 'sandals', 'dress_shoes') AS is_footwear,
    IFF(rating >= 4, 'pos', IFF(rating = 3, 'mid', 'neg')) AS band
  FROM b JOIN PRODUCTS p ON p.product_id = b.product_id
)
SELECT n AS review_id, product_id,
  'C' || LPAD(UNIFORM(1, 120, HASH(n, 'cust'))::VARCHAR, 5, '0') AS customer_id,
  DATEADD(day, -UNIFORM(1, 300, HASH(n, 'date')), CURRENT_DATE()) AS review_date,
  rating,
  REPLACE(
    DECODE(band,
      'pos', ARRAY_CONSTRUCT(
        'I picked up the {p} about a month ago and have worn it at least three times a week since, so I feel like I can give a fair review.',
        'After reading a lot of reviews I finally bought the {p} from Alpine & Co. and I am really glad I did.',
        'This is my second purchase of the {p} and it has quickly become a staple in my weekly rotation.')[MOD(n, 3)],
      'mid', ARRAY_CONSTRUCT(
        'I have mixed feelings about the {p} after wearing it for a few weeks.',
        'The {p} is decent overall, but there are a few things that keep me from loving it.')[MOD(n, 2)],
      ARRAY_CONSTRUCT(
        'I really wanted to like the {p}, but my experience has been disappointing from the start.',
        'I am returning the {p} and wanted to share why so other shoppers can make an informed decision.',
        'Unfortunately the {p} did not live up to the price tag or the description on the website.')[MOD(n, 3)])
    || ' ' || IFF(is_footwear,
      ARRAY_CONSTRUCT(
        'Sizing runs a half size small, so I had to exchange for a larger size at the store.',
        'The fit is true to size with plenty of room in the toe box and a secure heel.',
        'The toe box feels narrow and tight for the first week, though it loosened up a bit with wear.')[MOD(n * 5, 3)],
      ARRAY_CONSTRUCT(
        'Sizing runs a full size small, so I had to exchange my usual medium for a large at the store.',
        'The fit is true to size and the length is exactly what the size chart on the website describes.',
        'It runs large through the shoulders and waist, so I would recommend sizing down if you are between sizes.',
        'I ordered my normal size online and it fit perfectly, which saved me a trip for an exchange.')[MOD(n * 5, 4)])
    || ' ' || DECODE(band,
      'pos', ARRAY_CONSTRUCT(
        'The materials feel premium and have held up through weeks of daily use with no fading or wear.',
        'Stitching is clean and even, and the seams feel reinforced in all the high-stress areas.',
        'The materials feel durable and the zipper and hardware are noticeably better than cheaper competitors.')[MOD(n, 3)],
      'mid', ARRAY_CONSTRUCT(
        'Quality is acceptable, although I noticed a few loose threads and some light wear after a few weeks.',
        'The material is fine for casual use, but it feels thinner than the version I bought two years ago.')[MOD(n, 2)],
      IFF(is_footwear,
        ARRAY_CONSTRUCT(
          'The sole started separating from the upper after less than a month of normal walking.',
          'The stitching along the side of the upper came apart after the third wear and looks loose in other places.',
          'The insole flattened out within two weeks and the heel cushioning is already gone.')[MOD(n, 3)],
        ARRAY_CONSTRUCT(
          'After only two washes the fabric started pilling badly and the color faded noticeably.',
          'A seam along the side came apart after the third wear and the stitching looks loose in other places.',
          'The zipper broke within the first two weeks, which is unacceptable at this price point.')[MOD(n, 3)]))
    || ' ' || IFF(band = 'neg',
      ARRAY_CONSTRUCT(
        'Comfort was poor, with rubbing at the heel and seams that irritated my skin after an hour or two.',
        'It feels stiff and uncomfortable, and I never got it to break in even after several weeks.')[MOD(n, 2)],
      ARRAY_CONSTRUCT(
        'Comfort is excellent for long days on my feet, errands, and weekend hikes, and it breathes well during workouts.',
        'It is comfortable enough for everyday wear and I have even worn it on a few long runs without any chafing.')[MOD(n, 2)])
    || ' ' || IFF(band = 'pos',
      ARRAY_CONSTRUCT(
        'Style wise it looks great, the color matches the website photos, and I get compliments every time I wear it. For the price it is an excellent value compared to similar products from other brands I have tried.',
        'The design is clean and versatile enough for the office or the gym, and compared to Nike and Lululemon options it is a much better value.')[MOD(n, 2)],
      ARRAY_CONSTRUCT(
        'The color looked different in person than on the website, and honestly it feels overpriced for what you get compared to competitors like Target or Old Navy.',
        'Considering the price, I expected much better construction, and I would rather spend the money on a competitor brand next time.')[MOD(n, 2)])
    || ' ' || DECODE(band,
      'pos', ARRAY_CONSTRUCT(
        'I would definitely recommend it and plan to buy another color before the holiday season.',
        'Highly recommend for anyone looking for reliable everyday gear from Alpine & Co.')[MOD(n, 2)],
      'mid', 'I might keep it for casual weekends, but I would wait for a sale before buying another.',
      ARRAY_CONSTRUCT(
        'I would not recommend it, and I have already started the return process at my local store.',
        'Customer service was helpful with the exchange, but I will not be buying this product again.')[MOD(n, 2)]),
    '{p}', product_name)::VARCHAR AS review_text,
  UNIFORM(0, 9, HASH(n, 'verified')) < 8 AS verified_purchase,
  UNIFORM(0, 60, HASH(n, 'votes')) AS helpful_votes
FROM t;

-- SUPPORT_TICKETS: 25 customer service interactions
CREATE OR REPLACE TABLE SUPPORT_TICKETS AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 25))
), b AS (
  SELECT n, MOD(n - 1, 6) AS c, MOD(FLOOR((n - 1) / 6), 2) AS v, p.product_name
  FROM g JOIN PRODUCTS p ON p.product_id = MOD(n * 3, 25) + 1
)
SELECT n AS ticket_id,
  'C' || LPAD(UNIFORM(1, 120, HASH(n, 'cust'))::VARCHAR, 5, '0') AS customer_id,
  DATEADD(day, -UNIFORM(0, 90, HASH(n, 'date')), CURRENT_DATE()) AS created_date,
  ARRAY_CONSTRUCT('email', 'chat', 'phone', 'social')[UNIFORM(0, 3, HASH(n, 'ch'))]::VARCHAR AS channel,
  ARRAY_CONSTRUCT('return_request', 'product_defect', 'shipping_issue', 'size_exchange', 'billing', 'general_inquiry')[c]::VARCHAR AS category,
  REPLACE(ARRAY_CONSTRUCT(
    ARRAY_CONSTRUCT(
      'I bought the {p} online three weeks ago and I would like to return it. The color is much darker than the photos on the website and it does not go with anything I own. I still have the tags and the original packaging. Can you send me a prepaid return label, and how long will the refund take to reach my credit card?',
      'I am trying to return the {p} I purchased in store as a gift, but I do not have the receipt. The store associate told me I could only get store credit, but I paid with my loyalty account so the purchase should be on file. Please help me get a full refund instead of store credit.'),
    ARRAY_CONSTRUCT(
      'The {p} I purchased last month is falling apart. A seam along the side has completely split and the stitching is unraveling after only four or five wears. I followed the care instructions exactly. This is the second item from this line with the same problem and I am very frustrated with the quality.',
      'The zipper on my {p} broke the first time I tried to close it on a cold morning. The pull came off in my hand and now it will not close at all. I need a replacement before my ski trip next week. This is unacceptable for such an expensive product.'),
    ARRAY_CONSTRUCT(
      'My order containing the {p} was supposed to arrive five days ago. The tracking number has not updated in a week and still says label created. I needed this for an event this weekend. Can you tell me where my package is or send a replacement with expedited shipping?',
      'The box with my {p} arrived crushed and soaking wet. The item inside is damaged and the shoe box was torn open. I have photos of the packaging. I would like a replacement shipped right away and I do not want to pay for return shipping on a damaged delivery.'),
    ARRAY_CONSTRUCT(
      'The {p} runs much smaller than the size chart says. I ordered a medium based on my measurements and it fits like a small. I would like to exchange it for a large, but the large is showing out of stock online. Can you check if any store near Chicago has my size?',
      'I need to exchange the {p} for one size up. It is too tight and became uncomfortable after only an hour of wear. I bought it at the outlet and the store says outlet purchases are final sale, but nobody told me that at checkout. Please help me exchange it.'),
    ARRAY_CONSTRUCT(
      'I was charged twice for my order of the {p}. My bank statement shows two identical charges on the same day, but I only received one order confirmation email. Please refund the duplicate charge as soon as possible.',
      'My loyalty points did not post after I bought the {p} during the double points event. I should have earned about 400 points but my account shows zero for that purchase. I have the receipt and the promotion email. Please add the missing points to my account.'),
    ARRAY_CONSTRUCT(
      'Do you know when the {p} will be restocked in my size? I have been checking the website every day for two weeks. Also, can I place a hold on one at my local store so I can try it on before buying?',
      'I am looking for recommendations on cold weather gear for a family trip to Colorado. My kids need jackets and boots, and I was looking at the {p}. Does it come in kids sizes and is it warm enough for temperatures below zero?')
  )[c][v]::VARCHAR, '{p}', product_name) AS description_text,
  ARRAY_CONSTRUCT('urgent','high','medium','low','high','medium','urgent','medium','low','high','medium','low','high','medium','low','urgent','medium','low','high','medium','low','medium','high','low','medium')[n - 1]::VARCHAR AS priority,
  ARRAY_CONSTRUCT('open', 'in_progress', 'resolved', 'resolved', 'escalated')[UNIFORM(0, 4, HASH(n, 'st'))]::VARCHAR AS status,
  ARRAY_CONSTRUCT(
    'Issued prepaid return label and processed refund to original payment method.',
    'Shipped a free replacement and filed a quality report with the product team.',
    'Opened a carrier trace and sent a replacement with expedited shipping.',
    'Located the requested size at a nearby store and placed a 48-hour hold.',
    'Reversed the duplicate charge and credited the missing loyalty points.',
    'Shared restock date and product recommendations with the customer.')[c]::VARCHAR AS resolution_text
FROM b;

-- MARKETING_CAMPAIGNS: 40 campaigns (10 themes x 4 channels)
CREATE OR REPLACE TABLE MARKETING_CAMPAIGNS AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 40))
), b AS (
  SELECT n, MOD(n - 1, 10) AS th, FLOOR((n - 1) / 10) AS ch FROM g
), x AS (
  SELECT b.*,
    ARRAY_CONSTRUCT('Holiday Gift Guide', 'Back-to-School Essentials', 'Summit Activewear Launch', 'Basecamp Basics Refresh',
      'Spring Rain Ready', 'Winter Outerwear Event', 'Sneaker Week', 'Loyalty Double Points', 'Summer Sandal Sale', 'Black Friday Doorbusters')[th]::VARCHAR AS theme,
    ARRAY_CONSTRUCT('email', 'social', 'display', 'sms', 'in_store')[MOD(th + ch, 5)]::VARCHAR AS channel,
    ARRAY_CONSTRUCT('loyalty_members', 'gen_z_shoppers', 'active_lifestyle', 'value_seekers', 'families_with_kids', 'outdoor_enthusiasts')[MOD(th * 3 + ch, 6)]::VARCHAR AS target_segment,
    ARRAY_CONSTRUCT(
      'Drive gift purchases in November and December by curating best-selling items under $50, $100, and $200.',
      'Capture August back-to-school demand for sneakers, denim, backpacks, and kids outerwear.',
      'Introduce the new Summit activewear collection and grow private-label share against national brands.',
      'Reposition Basecamp basics as the everyday wardrobe essential with a refreshed color palette.',
      'Sell through spring rain jackets and windbreakers before the April weather window closes.',
      'Lift full-price sell-through of insulated jackets and winter boots ahead of the first cold snap.',
      'Build traffic around new sneaker drops from Nike, Adidas, and New Balance with limited releases.',
      'Re-engage lapsed loyalty members with a two-week double points window on all categories.',
      'Clear summer sandal inventory while protecting margin with tiered promotional pricing.',
      'Win the Black Friday weekend with doorbuster pricing on outerwear and footwear.')[th]::VARCHAR AS goal
  FROM b
)
SELECT n AS campaign_id,
  theme || ' - ' || INITCAP(REPLACE(channel, '_', ' ')) || ' ' || (2025 + MOD(ch, 2))::VARCHAR AS campaign_name,
  DATEADD(day, th * 30 + ch * 7, '2025-01-15'::DATE) AS start_date,
  DATEADD(day, th * 30 + ch * 7 + UNIFORM(10, 30, HASH(n, 'len')), '2025-01-15'::DATE) AS end_date,
  channel, target_segment,
  'Campaign goal: ' || goal || ' The primary audience is ' || REPLACE(target_segment, '_', ' ')
    || ', who respond best to clear value messaging and authentic lifestyle imagery. Messaging strategy will lead with product benefits such as comfort, durability, and fit confidence, '
    || 'supported by customer reviews and Alpine & Co. loyalty perks. The ' || REPLACE(channel, '_', ' ')
    || ' creative direction uses bright seasonal photography, short headlines, and a single call to action that links to a curated landing page or in-store display. '
    || 'We will A/B test two subject lines or headlines and retarget engaged shoppers within seven days. Success will be measured by conversion rate, incremental revenue, and new loyalty sign-ups, '
    || 'with an expected return on ad spend of ' || UNIFORM(25, 60, HASH(n, 'roi')) / 10 || 'x based on prior seasonal benchmarks.' AS campaign_brief_text,
  UNIFORM(10, 150, HASH(n, 'budget')) * 1000 AS budget_usd,
  ROUND(UNIFORM(10, 150, HASH(n, 'budget')) * 1000 * UNIFORM(80, 110, HASH(n, 'spend')) / 100, 2) AS actual_spend_usd,
  UNIFORM(50, 2000, HASH(n, 'imp')) * 1000 AS impressions,
  UNIFORM(300, 9000, HASH(n, 'conv')) AS conversions
FROM x;

-- SUPPLIER_COMMUNICATIONS: 35 emails; Mexican suppliers write in Spanish
CREATE OR REPLACE TABLE SUPPLIER_COMMUNICATIONS AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 35))
), b AS (
  SELECT n, MOD(n, 4) = 0 AS is_es, MOD(n, 6) AS en_i, MOD(FLOOR(n / 4), 4) AS es_i FROM g
), x AS (
  SELECT b.*,
    IFF(is_es, IFF(MOD(n, 8) = 0, 11, 15), ARRAY_CONSTRUCT(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14)[MOD(n * 5, 13)]) AS supplier_id
  FROM b
)
SELECT n AS comm_id, x.supplier_id,
  IFF(MOD(n, 3) = 0, 'buying@alpineandco.com', s.company_name) AS from_party,
  IFF(MOD(n, 3) = 0, s.company_name, 'buying@alpineandco.com') AS to_party,
  IFF(is_es,
    ARRAY_CONSTRUCT('Retraso en el envio de la orden de compra', 'Problema de calidad en la tela', 'Propuesta de ajuste de precios', 'Planificacion de la temporada de otono')[es_i]::VARCHAR,
    ARRAY_CONSTRUCT('Shipment delay on spring purchase order', 'Fabric quality issue on recent production run', 'Price negotiation for next season', 'Holiday season planning and capacity', 'Minimum order quantity discussion', 'Lead time change notice')[en_i]::VARCHAR) AS subject,
  IFF(is_es,
    ARRAY_CONSTRUCT(
      'Estimado equipo de compras: Les informamos que la orden de compra para la temporada de primavera tendra un retraso de aproximadamente dos semanas debido a la congestion en el puerto de Manzanillo. Estamos priorizando las tallas de mayor demanda y podemos enviar un embarque parcial la proxima semana. Por favor confirmen si prefieren el envio parcial o esperar el pedido completo.',
      'Hola, durante la inspeccion final detectamos que un lote de tela de mezclilla presenta variaciones de color entre rollos. Hemos separado el material afectado y proponemos reemplazarlo sin costo adicional, aunque esto podria agregar diez dias al tiempo de entrega. Quedamos atentos a su decision.',
      'Buenos dias. Debido al aumento en el costo del algodon y del transporte, necesitamos revisar los precios para la proxima temporada. Proponemos un incremento del cuatro por ciento, pero podemos mantener el precio actual si aumentan el volumen minimo de pedido a cinco mil unidades por estilo.',
      'Estimados, para la temporada de otono e invierno podemos reservar capacidad adicional en nuestra planta de Leon para botas y calzado de trabajo. Necesitamos la proyeccion de unidades por estilo antes del fin de mes para asegurar los materiales y cumplir con las fechas de entrega.')[es_i],
    ARRAY_CONSTRUCT(
      'Hello team, we regret to inform you that the spring purchase order will ship approximately 12 days late due to a container shortage at our origin port. We can air-freight the top three sizes at shared cost so stores are not out of stock for the launch. Please confirm how you would like to proceed by Friday.',
      'During final inspection we found pilling on a portion of the fleece fabric in the latest production run. We have quarantined about 1,800 units and are re-running the fabric with a different finishing process. We will send updated lab test results and photos before shipping.',
      'Thank you for the forecast for next season. Given current yarn and freight costs we would like to propose a 3 percent price increase. We are open to holding prices flat if Alpine & Co. can commit to a 20 percent higher volume and Net 45 payment terms.',
      'We are planning factory capacity for the holiday season and want to secure your peak volumes now. Please share final unit projections for outerwear and sneakers by September 15 so we can book materials and avoid late deliveries in November.',
      'Regarding the minimum order quantity for the new colorways, our MOQ is 1,200 units per style per color. We understand the smaller test quantities you requested, and we can offer 600 units for a 6 percent upcharge on the first order only.',
      'Please note that our standard lead time will increase from 60 to 75 days starting next quarter due to new compliance audits and longer fabric sourcing. We recommend placing holiday orders at least two weeks earlier than last year.')[en_i])::VARCHAR AS message_body,
  DATEADD(day, -UNIFORM(0, 200, HASH(n, 'sent')), CURRENT_DATE()) AS sent_date,
  IFF(is_es,
    ARRAY_CONSTRUCT('logistics', 'quality', 'pricing', 'planning')[es_i],
    ARRAY_CONSTRUCT('urgent_alert', 'quality', 'pricing', 'planning', 'planning', 'logistics')[en_i])::VARCHAR AS category,
  IFF(is_es, 'es', 'en') AS language
FROM x JOIN SUPPLIERS s ON s.supplier_id = x.supplier_id;

-- PRODUCT_RETURN_NOTES: 20 return inspection narratives
CREATE OR REPLACE TABLE PRODUCT_RETURN_NOTES AS
WITH g AS (
  SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS n FROM TABLE(GENERATOR(ROWCOUNT => 20))
), b AS (
  SELECT n, MOD(n - 1, 10) AS i, n * 9 AS transaction_id FROM g
)
SELECT n AS note_id, b.transaction_id,
  DATEADD(day, UNIFORM(3, 30, HASH(n, 'ret')), t.transaction_date) AS return_date,
  REPLACE(ARRAY_CONSTRUCT(
    'Customer returned the {p} because it runs small. They ordered their usual size but the fit was tight, and they said the size chart online was misleading. Item is unworn with tags attached.',
    'Customer reported the {p} ran large and still felt loose even after trying a size down in store. They preferred a refund over another exchange. No signs of wear.',
    'Customer said the color of the {p} did not match the website photos. The navy looked almost black in person. Item is new with tags and original packaging.',
    'The material on the {p} started pilling and fraying after very light use. Wear is clearly visible and the customer followed the care instructions.',
    'A seam on the {p} came apart after two wears. Stitching appears loose and thread is fraying in other areas. Flagged as a construction defect.',
    'Customer changed their mind about the {p} and found a style they liked better. Item is unworn, tags attached, and within the 30-day return window.',
    'Customer bought the wrong size of the {p} as a gift and needs a different size. Item never worn. Customer requested an exchange but the size was out of stock, so a refund was issued.',
    'The {p} arrived with shipping damage. The box was crushed in transit and the item has a scuff and a bent component. Carrier damage claim attached.',
    'The hardware on the {p} failed on the second use. A closure piece snapped off and the remaining parts are misaligned. Defective hardware, not caused by customer misuse.',
    'Customer said the {p} was not as described. The website listed it as waterproof but water soaked through during light rain. Customer is disappointed with the product claims.')[i]::VARCHAR,
    '{p}', p.product_name) AS return_reason_text,
  ARRAY_CONSTRUCT('new_with_tags', 'new_with_tags', 'new_with_tags', 'worn', 'defective', 'new_with_tags', 'new_with_tags', 'damaged', 'defective', 'worn')[i]::VARCHAR AS product_condition,
  ARRAY_CONSTRUCT('Update size chart', 'Update size chart', 'Reshoot product photos', 'Escalate fabric quality to supplier', 'Escalate construction defect to supplier',
    'Restock to sales floor', 'Restock to sales floor', 'File carrier damage claim', 'Escalate hardware defect to supplier', 'Review product description claims')[i]::VARCHAR AS recommended_action,
  ARRAY_CONSTRUCT('restock', 'restock', 'restock', 'markdown', 'destroy', 'restock', 'restock', 'donate', 'destroy', 'markdown')[i]::VARCHAR AS disposition
FROM b
JOIN SALES_TRANSACTIONS t ON t.transaction_id = b.transaction_id
JOIN PRODUCTS p ON p.product_id = t.product_id;"""

FB_2_4 = """SELECT table_name, row_count
FROM RETAIL_AI_DEMO.INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'RETAIL_OPS' AND table_type = 'BASE TABLE'
ORDER BY row_count DESC;"""

# ---------------------------------------------------------------------------
# Session 3 - Security & Governance
# ---------------------------------------------------------------------------

FB_3_1 = """USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS RETAIL_DATA_ENGINEER;
CREATE ROLE IF NOT EXISTS RETAIL_DATA_SCIENTIST;
CREATE ROLE IF NOT EXISTS RETAIL_MERCHANDISER;
CREATE ROLE IF NOT EXISTS FINANCE_ANALYST;

-- Everyone needs to reach the database, schema and warehouse
GRANT USAGE ON DATABASE RETAIL_AI_DEMO TO ROLE RETAIL_DATA_ENGINEER;
GRANT USAGE ON DATABASE RETAIL_AI_DEMO TO ROLE RETAIL_DATA_SCIENTIST;
GRANT USAGE ON DATABASE RETAIL_AI_DEMO TO ROLE RETAIL_MERCHANDISER;
GRANT USAGE ON DATABASE RETAIL_AI_DEMO TO ROLE FINANCE_ANALYST;
GRANT USAGE ON SCHEMA RETAIL_AI_DEMO.RETAIL_OPS TO ROLE RETAIL_DATA_SCIENTIST;
GRANT USAGE ON SCHEMA RETAIL_AI_DEMO.RETAIL_OPS TO ROLE RETAIL_MERCHANDISER;
GRANT USAGE ON SCHEMA RETAIL_AI_DEMO.RETAIL_OPS TO ROLE FINANCE_ANALYST;
GRANT USAGE ON WAREHOUSE RETAIL_AI_WH TO ROLE RETAIL_DATA_ENGINEER;
GRANT USAGE ON WAREHOUSE RETAIL_AI_WH TO ROLE RETAIL_DATA_SCIENTIST;
GRANT USAGE ON WAREHOUSE RETAIL_AI_WH TO ROLE RETAIL_MERCHANDISER;
GRANT USAGE ON WAREHOUSE RETAIL_AI_WH TO ROLE FINANCE_ANALYST;

-- RETAIL_DATA_ENGINEER: full access to the schema
GRANT ALL PRIVILEGES ON SCHEMA RETAIL_AI_DEMO.RETAIL_OPS TO ROLE RETAIL_DATA_ENGINEER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS TO ROLE RETAIL_DATA_ENGINEER;

-- RETAIL_DATA_SCIENTIST: read everything + Cortex AI functions
GRANT SELECT ON ALL TABLES IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS TO ROLE RETAIL_DATA_SCIENTIST;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE RETAIL_DATA_SCIENTIST;

-- RETAIL_MERCHANDISER: operational + inventory tables only
GRANT SELECT ON TABLE RETAIL_AI_DEMO.RETAIL_OPS.SALES_TRANSACTIONS TO ROLE RETAIL_MERCHANDISER;
GRANT SELECT ON TABLE RETAIL_AI_DEMO.RETAIL_OPS.INVENTORY_LEVELS   TO ROLE RETAIL_MERCHANDISER;
GRANT SELECT ON TABLE RETAIL_AI_DEMO.RETAIL_OPS.PRODUCTS           TO ROLE RETAIL_MERCHANDISER;
GRANT SELECT ON TABLE RETAIL_AI_DEMO.RETAIL_OPS.STORES             TO ROLE RETAIL_MERCHANDISER;
GRANT SELECT ON TABLE RETAIL_AI_DEMO.RETAIL_OPS.PURCHASE_ORDERS    TO ROLE RETAIL_MERCHANDISER;

-- FINANCE_ANALYST: financial tables only
GRANT SELECT ON TABLE RETAIL_AI_DEMO.RETAIL_OPS.SALES_TRANSACTIONS  TO ROLE FINANCE_ANALYST;
GRANT SELECT ON TABLE RETAIL_AI_DEMO.RETAIL_OPS.PURCHASE_ORDERS     TO ROLE FINANCE_ANALYST;
GRANT SELECT ON TABLE RETAIL_AI_DEMO.RETAIL_OPS.DAILY_SALES_METRICS TO ROLE FINANCE_ANALYST;

-- Grant all four roles to the current user for testing
SET my_user = CURRENT_USER();
GRANT ROLE RETAIL_DATA_ENGINEER  TO USER IDENTIFIER($my_user);
GRANT ROLE RETAIL_DATA_SCIENTIST TO USER IDENTIFIER($my_user);
GRANT ROLE RETAIL_MERCHANDISER   TO USER IDENTIFIER($my_user);
GRANT ROLE FINANCE_ANALYST       TO USER IDENTIFIER($my_user);

SHOW GRANTS TO ROLE RETAIL_MERCHANDISER;"""

FB_3_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE TAG SENSITIVITY_LEVEL
  ALLOWED_VALUES 'PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED';

ALTER TABLE PRODUCTS MODIFY COLUMN unit_cost SET TAG SENSITIVITY_LEVEL = 'CONFIDENTIAL';
ALTER TABLE PRODUCTS MODIFY COLUMN margin_pct SET TAG SENSITIVITY_LEVEL = 'CONFIDENTIAL';
ALTER TABLE PURCHASE_ORDERS MODIFY COLUMN unit_cost SET TAG SENSITIVITY_LEVEL = 'RESTRICTED';
ALTER TABLE PURCHASE_ORDERS MODIFY COLUMN total_cost SET TAG SENSITIVITY_LEVEL = 'RESTRICTED';
ALTER TABLE SALES_TRANSACTIONS MODIFY COLUMN discount_pct SET TAG SENSITIVITY_LEVEL = 'INTERNAL';

-- ACCOUNTADMIN is included so the lab owner keeps seeing real costs in later sessions
CREATE OR REPLACE MASKING POLICY MASK_COST_DATA AS (val STRING) RETURNS STRING ->
  CASE WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN', 'RETAIL_DATA_ENGINEER', 'FINANCE_ANALYST') THEN val
       ELSE '***MASKED***' END;

CREATE OR REPLACE MASKING POLICY MASK_DOLLAR_VALUES AS (val NUMBER(10,2)) RETURNS NUMBER(10,2) ->
  CASE WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN', 'RETAIL_DATA_ENGINEER', 'FINANCE_ANALYST') THEN val
       ELSE 0.00 END;

ALTER TABLE PRODUCTS MODIFY COLUMN unit_cost SET MASKING POLICY MASK_DOLLAR_VALUES;
ALTER TABLE PURCHASE_ORDERS MODIFY COLUMN unit_cost SET MASKING POLICY MASK_DOLLAR_VALUES;

-- Compare what two roles see
SELECT product_name, unit_cost, retail_price FROM PRODUCTS LIMIT 5;
USE ROLE RETAIL_MERCHANDISER;
SELECT product_name, unit_cost, retail_price FROM RETAIL_AI_DEMO.RETAIL_OPS.PRODUCTS LIMIT 5;
USE ROLE ACCOUNTADMIN;"""

FB_3_3 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

SELECT * FROM TABLE(RETAIL_AI_DEMO.INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS('RETAIL_AI_DEMO.RETAIL_OPS.PRODUCTS', 'table'))
UNION ALL
SELECT * FROM TABLE(RETAIL_AI_DEMO.INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS('RETAIL_AI_DEMO.RETAIL_OPS.PURCHASE_ORDERS', 'table'))
UNION ALL
SELECT * FROM TABLE(RETAIL_AI_DEMO.INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS('RETAIL_AI_DEMO.RETAIL_OPS.SALES_TRANSACTIONS', 'table'));

SELECT policy_name, policy_kind, ref_entity_name, ref_column_name
FROM TABLE(RETAIL_AI_DEMO.INFORMATION_SCHEMA.POLICY_REFERENCES(REF_ENTITY_NAME => 'RETAIL_AI_DEMO.RETAIL_OPS.PRODUCTS', REF_ENTITY_DOMAIN => 'table'))
UNION ALL
SELECT policy_name, policy_kind, ref_entity_name, ref_column_name
FROM TABLE(RETAIL_AI_DEMO.INFORMATION_SCHEMA.POLICY_REFERENCES(REF_ENTITY_NAME => 'RETAIL_AI_DEMO.RETAIL_OPS.PURCHASE_ORDERS', REF_ENTITY_DOMAIN => 'table'));

SELECT product_id, product_name, unit_cost, margin_pct, retail_price FROM PRODUCTS LIMIT 5;"""

# ---------------------------------------------------------------------------
# Session 4 - Snowpark ML & Model Development
# ---------------------------------------------------------------------------

FB_4_1 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE VIEW STOCKOUT_FEATURES AS
SELECT
  i.snapshot_id, i.product_id, i.store_id, i.snapshot_date,
  i.quantity_on_hand, i.days_of_supply, i.reorder_point,
  p.retail_price, p.unit_cost, p.category,
  s.store_type, s.square_footage,
  EXTRACT(MONTH FROM i.snapshot_date) AS snapshot_month,
  DAYOFWEEK(i.snapshot_date) AS snapshot_day_of_week,
  CASE WHEN EXTRACT(MONTH FROM i.snapshot_date) IN (11, 12) THEN 1 ELSE 0 END AS is_holiday_season,
  i.status,
  CASE WHEN i.quantity_on_hand <= i.reorder_point * 0.3 THEN 1 ELSE 0 END AS is_stockout
FROM INVENTORY_LEVELS i
JOIN PRODUCTS p ON p.product_id = i.product_id
JOIN STORES s ON s.store_id = i.store_id
WHERE i.quantity_on_hand IS NOT NULL;

-- Class balance and average feature values per class
SELECT is_stockout, COUNT(*) AS row_count,
  ROUND(AVG(quantity_on_hand), 1) AS avg_qty_on_hand,
  ROUND(AVG(days_of_supply), 1) AS avg_days_of_supply,
  ROUND(AVG(reorder_point), 1) AS avg_reorder_point,
  ROUND(AVG(retail_price), 2) AS avg_retail_price,
  ROUND(AVG(is_holiday_season), 2) AS pct_holiday
FROM STOCKOUT_FEATURES
GROUP BY is_stockout ORDER BY is_stockout;"""

FB_4_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- Deterministic 80/20 split on snapshot_id (HASH keeps the split stable across queries)
CREATE OR REPLACE VIEW STOCKOUT_FEATURES_TRAIN AS
SELECT quantity_on_hand, days_of_supply, reorder_point, retail_price, unit_cost, category,
       store_type, square_footage, snapshot_month, snapshot_day_of_week, is_holiday_season, status, is_stockout
FROM STOCKOUT_FEATURES
WHERE MOD(ABS(HASH(snapshot_id)), 10) < 8;

CREATE OR REPLACE VIEW STOCKOUT_FEATURES_TEST AS
SELECT snapshot_id, quantity_on_hand, days_of_supply, reorder_point, retail_price, unit_cost, category,
       store_type, square_footage, snapshot_month, snapshot_day_of_week, is_holiday_season, status, is_stockout
FROM STOCKOUT_FEATURES
WHERE MOD(ABS(HASH(snapshot_id)), 10) >= 8;

-- Train with Snowflake ML Classification (AutoML) - takes about 1 minute
CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION STOCKOUT_PREDICTION_MODEL(
  INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'STOCKOUT_FEATURES_TRAIN'),
  TARGET_COLNAME => 'IS_STOCKOUT',
  CONFIG_OBJECT => {'on_error': 'skip'}
);

-- Confusion matrix on the test set
WITH scored AS (
  SELECT is_stockout,
    STOCKOUT_PREDICTION_MODEL!PREDICT(INPUT_DATA => OBJECT_CONSTRUCT(* EXCLUDE (snapshot_id, is_stockout))):class::INTEGER AS predicted
  FROM STOCKOUT_FEATURES_TEST
)
SELECT is_stockout AS actual, predicted, COUNT(*) AS row_count
FROM scored GROUP BY 1, 2 ORDER BY 1, 2;

CALL STOCKOUT_PREDICTION_MODEL!SHOW_FEATURE_IMPORTANCE();"""

FB_4_3 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE TABLE STOCKOUT_PREDICTIONS AS
SELECT t.*,
  STOCKOUT_PREDICTION_MODEL!PREDICT(INPUT_DATA => OBJECT_CONSTRUCT(t.* EXCLUDE (snapshot_id, is_stockout))) AS prediction,
  prediction:class::INTEGER AS predicted_stockout,
  ROUND(prediction:probability:"1"::FLOAT, 3) AS stockout_probability
FROM STOCKOUT_FEATURES_TEST t;

-- Accuracy, precision, recall, and confusion matrix counts
SELECT
  COUNT_IF(is_stockout = 1 AND predicted_stockout = 1) AS tp,
  COUNT_IF(is_stockout = 0 AND predicted_stockout = 1) AS fp,
  COUNT_IF(is_stockout = 0 AND predicted_stockout = 0) AS tn,
  COUNT_IF(is_stockout = 1 AND predicted_stockout = 0) AS fn,
  ROUND((tp + tn) / COUNT(*), 3) AS accuracy,
  ROUND(tp / NULLIF(tp + fp, 0), 3) AS precision_stockout,
  ROUND(tp / NULLIF(tp + fn, 0), 3) AS recall_stockout
FROM STOCKOUT_PREDICTIONS;

CALL STOCKOUT_PREDICTION_MODEL!SHOW_EVALUATION_METRICS();
CALL STOCKOUT_PREDICTION_MODEL!SHOW_FEATURE_IMPORTANCE();"""

# Python fallback: paste into a Snowflake Notebook (Projects > Notebooks > + Notebook)
FB_4_4 = '''# Paste into a single Python cell of a new Snowflake Notebook
# (Projects > Notebooks > + Notebook, database RETAIL_AI_DEMO, schema RETAIL_OPS, warehouse RETAIL_AI_WH)
# Add packages if prompted: snowflake-ml-python, xgboost, scikit-learn
from snowflake.snowpark.context import get_active_session
from snowflake.ml.feature_store import FeatureStore, FeatureView, Entity, CreationMode
from snowflake.ml.registry import Registry
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
import pandas as pd

session = get_active_session()
session.use_warehouse("RETAIL_AI_WH")
session.use_database("RETAIL_AI_DEMO")
session.use_schema("RETAIL_OPS")

# --- SECTION 1: Feature Store ---
fs = FeatureStore(session=session, database="RETAIL_AI_DEMO", name="RETAIL_OPS",
                  default_warehouse="RETAIL_AI_WH", creation_mode=CreationMode.CREATE_IF_NOT_EXIST)
entity = Entity(name="PRODUCT", join_keys=["PRODUCT_ID", "STORE_ID"])
fs.register_entity(entity)

feature_df = session.sql("""
    SELECT i.product_id, i.store_id, i.snapshot_date::TIMESTAMP_NTZ AS snapshot_date,
           i.quantity_on_hand, i.days_of_supply, i.reorder_point,
           p.retail_price, p.unit_cost, p.category, s.store_type, s.square_footage,
           MONTH(i.snapshot_date) AS snapshot_month, DAYOFWEEK(i.snapshot_date) AS snapshot_day_of_week,
           IFF(MONTH(i.snapshot_date) IN (11, 12), 1, 0) AS is_holiday_season,
           IFF(i.quantity_on_hand <= i.reorder_point * 0.3, 1, 0) AS is_stockout
    FROM RETAIL_AI_DEMO.RETAIL_OPS.INVENTORY_LEVELS i
    JOIN RETAIL_AI_DEMO.RETAIL_OPS.PRODUCTS p ON p.product_id = i.product_id
    JOIN RETAIL_AI_DEMO.RETAIL_OPS.STORES s ON s.store_id = i.store_id
""")
fv = FeatureView(name="STOCKOUT_FEATURE_VIEW", entities=[entity], feature_df=feature_df,
                 timestamp_col="SNAPSHOT_DATE", refresh_freq="1 hour")
fv = fs.register_feature_view(fv, version="V1", overwrite=True)

# --- SECTION 2: Point-in-time training dataset ---
spine_df = feature_df.select("PRODUCT_ID", "STORE_ID", "SNAPSHOT_DATE")
session.sql("DROP DATASET IF EXISTS STOCKOUT_TRAINING_DATA").collect()  # safe to re-run
dataset = fs.generate_dataset(name="STOCKOUT_TRAINING_DATA", version="V1", spine_df=spine_df,
                              features=[fv], spine_timestamp_col="SNAPSHOT_DATE")
df = dataset.read.to_pandas()
features = ["QUANTITY_ON_HAND", "DAYS_OF_SUPPLY", "REORDER_POINT", "RETAIL_PRICE", "UNIT_COST",
            "SQUARE_FOOTAGE", "SNAPSHOT_MONTH", "SNAPSHOT_DAY_OF_WEEK", "IS_HOLIDAY_SEASON",
            "CATEGORY", "STORE_TYPE"]
X = pd.get_dummies(df[features], columns=["CATEGORY", "STORE_TYPE"], dtype=int).astype(float)
y = df["IS_STOCKOUT"].astype(int)
train = df.sample(frac=0.8, random_state=42).index
X_train, X_test, y_train, y_test = X.loc[train], X.drop(train), y.loc[train], y.drop(train)

# --- SECTION 3: Train and compare three models ---
models = {
    "XGBoost": XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.1),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=2000),
}
results = []
for name, m in models.items():
    m.fit(X_train, y_train)
    p = m.predict(X_test)
    results.append({"model": name, "accuracy": accuracy_score(y_test, p),
                    "precision": precision_score(y_test, p, zero_division=0),
                    "recall": recall_score(y_test, p, zero_division=0),
                    "f1": f1_score(y_test, p, zero_division=0)})
comparison = pd.DataFrame(results).sort_values("f1", ascending=False)
comparison

# --- SECTION 4: Register the best model ---
best = comparison.iloc[0]
best_model = models[best["model"]]
reg = Registry(session=session, database_name="RETAIL_AI_DEMO", schema_name="RETAIL_OPS")
mv = reg.log_model(best_model, model_name="STOCKOUT_PREDICTOR", version_name="V1",
                   sample_input_data=X_test.head(5), target_platforms=["WAREHOUSE"],
                   metrics={"f1": float(best["f1"]), "accuracy": float(best["accuracy"]), "algorithm": best["model"]})

# --- SECTION 5: Validate the registered model ---
session.sql("SHOW MODELS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS").show()
registered = mv.run(X_test.head(10), function_name="predict")
registered
'''

FB_4_5 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- Feature views are stored as dynamic tables named <FEATURE_VIEW>$<VERSION>
SHOW DYNAMIC TABLES LIKE 'STOCKOUT_FEATURE_VIEW%' IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;
SHOW MODELS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;
SHOW VERSIONS IN MODEL RETAIL_AI_DEMO.RETAIL_OPS.STOCKOUT_PREDICTOR;
SHOW FUNCTIONS IN MODEL RETAIL_AI_DEMO.RETAIL_OPS.STOCKOUT_PREDICTOR;"""

# ---------------------------------------------------------------------------
# Session 5 - Real-time Inference with Dynamic Tables
# ---------------------------------------------------------------------------

FB_5_1 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE DYNAMIC TABLE LIVE_STOCKOUT_SCORES
  TARGET_LAG = '1 minute'
  WAREHOUSE = RETAIL_AI_WH
AS
WITH f AS (
  SELECT i.snapshot_id, i.product_id, i.store_id, s.store_name, p.product_name, i.snapshot_date,
    i.quantity_on_hand, i.days_of_supply, i.reorder_point, p.retail_price, p.unit_cost, p.category,
    s.store_type, s.square_footage,
    EXTRACT(MONTH FROM i.snapshot_date) AS snapshot_month,
    DAYOFWEEK(i.snapshot_date) AS snapshot_day_of_week,
    CASE WHEN EXTRACT(MONTH FROM i.snapshot_date) IN (11, 12) THEN 1 ELSE 0 END AS is_holiday_season,
    i.status
  FROM INVENTORY_LEVELS i
  JOIN PRODUCTS p ON p.product_id = i.product_id
  JOIN STORES s ON s.store_id = i.store_id
), scored AS (
  SELECT f.*,
    STOCKOUT_PREDICTION_MODEL!PREDICT(INPUT_DATA => OBJECT_CONSTRUCT(
      'QUANTITY_ON_HAND', quantity_on_hand, 'DAYS_OF_SUPPLY', days_of_supply, 'REORDER_POINT', reorder_point,
      'RETAIL_PRICE', retail_price, 'UNIT_COST', unit_cost, 'CATEGORY', category, 'STORE_TYPE', store_type,
      'SQUARE_FOOTAGE', square_footage, 'SNAPSHOT_MONTH', snapshot_month, 'SNAPSHOT_DAY_OF_WEEK', snapshot_day_of_week,
      'IS_HOLIDAY_SEASON', is_holiday_season, 'STATUS', status)) AS prediction
  FROM f
)
SELECT snapshot_id, product_id, store_id, store_name, product_name, category, snapshot_date,
  prediction:class::INTEGER AS predicted_stockout_class,
  ROUND(prediction:probability:"1"::FLOAT, 3) AS predicted_stockout_probability,
  quantity_on_hand, days_of_supply, reorder_point
FROM scored;

SELECT store_name, product_name, category, quantity_on_hand, reorder_point, days_of_supply,
       predicted_stockout_class, predicted_stockout_probability
FROM LIVE_STOCKOUT_SCORES
ORDER BY predicted_stockout_probability DESC
LIMIT 10;"""

FB_5_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- 2 high-risk, 1 moderate, 2 healthy snapshots for today
INSERT INTO INVENTORY_LEVELS
SELECT (SELECT MAX(snapshot_id) FROM INVENTORY_LEVELS) + column1, column2, column3, CURRENT_DATE(),
       column4, column5, column6, column7, column8, column9
FROM VALUES
  (1, 1, 12,   4, 0, 200, 40,  1.0, 'low_stock'),
  (2, 3,  5,   6, 1, 150, 45,  2.0, 'low_stock'),
  (3, 5,  1,  38, 2, 100, 40,  6.0, 'low_stock'),
  (4, 2,  7, 160, 3,   0, 35, 22.0, 'in_stock'),
  (5, 8, 19, 210, 4,   0, 30, 30.0, 'in_stock');

-- Force an immediate refresh instead of waiting for the 1-minute lag
ALTER DYNAMIC TABLE LIVE_STOCKOUT_SCORES REFRESH;

SELECT store_name, product_name, quantity_on_hand, reorder_point, days_of_supply,
       predicted_stockout_class, predicted_stockout_probability
FROM LIVE_STOCKOUT_SCORES
WHERE snapshot_date = CURRENT_DATE()
ORDER BY predicted_stockout_probability DESC;

SELECT name, state, refresh_action, refresh_trigger, refresh_start_time, refresh_end_time
FROM TABLE(RETAIL_AI_DEMO.INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY(
  NAME => 'RETAIL_AI_DEMO.RETAIL_OPS.LIVE_STOCKOUT_SCORES'))
ORDER BY refresh_start_time DESC
LIMIT 5;"""

# ---------------------------------------------------------------------------
# Session 6 - Cortex AI Functions (AI_*)
# ---------------------------------------------------------------------------

FB_6_1 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- 1. AI_SENTIMENT: overall + aspect-based sentiment (most negative first)
--    Aspects come back in alphabetical order, so look each one up by name
SELECT review_id, product_id, rating,
  FILTER(s:categories::ARRAY, c -> c:name::STRING = 'overall')[0]:sentiment::STRING AS overall_sentiment,
  FILTER(s:categories::ARRAY, c -> c:name::STRING = 'fit')[0]:sentiment::STRING AS fit_sentiment,
  FILTER(s:categories::ARRAY, c -> c:name::STRING = 'quality')[0]:sentiment::STRING AS quality_sentiment,
  FILTER(s:categories::ARRAY, c -> c:name::STRING = 'comfort')[0]:sentiment::STRING AS comfort_sentiment,
  FILTER(s:categories::ARRAY, c -> c:name::STRING = 'price')[0]:sentiment::STRING AS price_sentiment
FROM (
  SELECT review_id, product_id, rating,
         AI_SENTIMENT(review_text, ['fit', 'quality', 'comfort', 'price']) AS s
  FROM CUSTOMER_REVIEWS
)
ORDER BY DECODE(overall_sentiment, 'negative', 1, 'mixed', 2, 'neutral', 3, 'positive', 4, 5), rating;

-- 2. AI_SUMMARIZE: the 5 longest support tickets
SELECT ticket_id, priority, category, AI_SUMMARIZE(description_text) AS summary
FROM SUPPORT_TICKETS
ORDER BY LENGTH(description_text) DESC
LIMIT 5;

-- 2b. AI_SUMMARIZE_AGG: one summary across ALL urgent/high tickets
SELECT AI_SUMMARIZE_AGG(description_text) AS urgent_ticket_summary
FROM SUPPORT_TICKETS
WHERE priority IN ('urgent', 'high');

-- 3. AI_TRANSLATE: Spanish supplier emails to English
SELECT subject, LEFT(message_body, 200) AS original_snippet,
       AI_TRANSLATE(message_body, 'es', 'en') AS english_translation
FROM SUPPLIER_COMMUNICATIONS
WHERE language = 'es';"""

FB_6_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

WITH tickets AS (
  SELECT ticket_id, priority,
    'You are a retail customer experience analyst at Alpine & Co. Analyze this support ticket and provide: '
    || '1) Root cause assessment 2) Customer impact analysis 3) Three recommended resolution actions. Keep it under 150 words. Ticket: '
    || description_text AS prompt
  FROM SUPPORT_TICKETS
  WHERE priority IN ('urgent', 'high')
  ORDER BY DECODE(priority, 'urgent', 1, 2), ticket_id
  LIMIT 3
)
SELECT ticket_id, priority,
  AI_COMPLETE('claude-sonnet-4-5', prompt)::STRING AS model_a_claude,
  AI_COMPLETE('llama3.3-70b', prompt)::STRING AS model_b_llama
FROM tickets;"""

FB_6_3 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- 1. AI_CLASSIFY: return reasons into exactly one category
SELECT note_id, product_condition,
  AI_CLASSIFY(return_reason_text,
    ['Sizing Issue', 'Quality Defect', 'Not As Described', 'Changed Mind', 'Shipping Damage']):labels[0]::STRING AS ai_classification,
  return_reason_text
FROM PRODUCT_RETURN_NOTES;

-- 2. AI_EXTRACT: structured fields from 5 customer reviews
SELECT review_id, rating,
  e:response:product_mentioned::STRING AS product_mentioned,
  e:response:sentiment::STRING AS sentiment,
  e:response:fit_feedback::STRING AS fit_feedback,
  e:response:quality_feedback::STRING AS quality_feedback,
  e:response:would_recommend::STRING AS would_recommend
FROM (
  SELECT review_id, rating,
    AI_EXTRACT(text => review_text, responseFormat => {
      'product_mentioned': 'Which product is the review about?',
      'sentiment': 'Overall sentiment: positive, neutral, or negative?',
      'fit_feedback': 'Fit: too_small, true_to_size, too_large, or not_mentioned?',
      'quality_feedback': 'Quality rating from 1 to 5 based on the text',
      'would_recommend': 'Would the reviewer recommend the product: true or false?'}) AS e
  FROM CUSTOMER_REVIEWS
  ORDER BY review_id
  LIMIT 5
);

-- 3. AI_FILTER: natural-language WHERE clause
SELECT review_id, rating, LEFT(review_text, 160) AS snippet
FROM CUSTOMER_REVIEWS
WHERE AI_FILTER(PROMPT('Does this review complain that the product runs small or tight? {0}', review_text));

-- 4. AI_AGG: insights across many rows in one call
SELECT AI_AGG(review_text,
  'List the top 3 product problems customers mention, with a one-line recommendation for the product team for each.') AS top_issues
FROM CUSTOMER_REVIEWS
WHERE rating <= 2;"""

# ---------------------------------------------------------------------------
# Session 7 - Unstructured Data Extraction
# ---------------------------------------------------------------------------

FB_7_1 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- response_format enforces a JSON schema, so the output is always valid, typed JSON
SELECT review_id, product_id, rating,
  AI_COMPLETE(
    model => 'claude-sonnet-4-5',
    prompt => 'Extract structured fields from this product review. All *_rating fields are integers from 1 to 5. Review: ' || review_text,
    response_format => {'type': 'json', 'schema': {'type': 'object', 'properties': {
      'product_name': {'type': 'string'},
      'overall_sentiment': {'type': 'string', 'enum': ['positive', 'neutral', 'negative']},
      'fit_rating': {'type': 'string', 'enum': ['too_small', 'true_to_size', 'too_large', 'not_mentioned']},
      'quality_rating': {'type': 'integer'}, 'comfort_rating': {'type': 'integer'}, 'style_rating': {'type': 'integer'},
      'pros': {'type': 'array', 'items': {'type': 'string'}},
      'cons': {'type': 'array', 'items': {'type': 'string'}},
      'recommended_for': {'type': 'array', 'items': {'type': 'string'}},
      'price_value_assessment': {'type': 'string', 'enum': ['excellent_value', 'fair_price', 'overpriced', 'not_mentioned']}},
      'required': ['product_name', 'overall_sentiment', 'fit_rating', 'quality_rating', 'comfort_rating', 'style_rating',
                   'pros', 'cons', 'recommended_for', 'price_value_assessment']}}
  ) AS extracted_data
FROM CUSTOMER_REVIEWS
ORDER BY review_id
LIMIT 10;"""

FB_7_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE TABLE EXTRACTED_REVIEW_DATA AS
SELECT review_id, product_id, rating,
  x:product_name::STRING AS product_name,
  x:overall_sentiment::STRING AS overall_sentiment,
  x:fit_rating::STRING AS fit_rating,
  x:quality_rating::INTEGER AS quality_rating,
  x:comfort_rating::INTEGER AS comfort_rating,
  x:style_rating::INTEGER AS style_rating,
  x:pros::ARRAY AS pros,
  x:cons::ARRAY AS cons,
  x:recommended_for::ARRAY AS recommended_for,
  x:price_value_assessment::STRING AS price_value_assessment,
  CURRENT_TIMESTAMP() AS extraction_timestamp
FROM (
  SELECT review_id, product_id, rating,
    AI_COMPLETE(
      model => 'claude-sonnet-4-5',
      prompt => 'Extract structured fields from this product review. All *_rating fields are integers from 1 to 5. Review: ' || review_text,
      response_format => {'type': 'json', 'schema': {'type': 'object', 'properties': {
        'product_name': {'type': 'string'},
        'overall_sentiment': {'type': 'string', 'enum': ['positive', 'neutral', 'negative']},
        'fit_rating': {'type': 'string', 'enum': ['too_small', 'true_to_size', 'too_large', 'not_mentioned']},
        'quality_rating': {'type': 'integer'}, 'comfort_rating': {'type': 'integer'}, 'style_rating': {'type': 'integer'},
        'pros': {'type': 'array', 'items': {'type': 'string'}},
        'cons': {'type': 'array', 'items': {'type': 'string'}},
        'recommended_for': {'type': 'array', 'items': {'type': 'string'}},
        'price_value_assessment': {'type': 'string', 'enum': ['excellent_value', 'fair_price', 'overpriced', 'not_mentioned']}},
        'required': ['product_name', 'overall_sentiment', 'fit_rating', 'quality_rating', 'comfort_rating', 'style_rating',
                     'pros', 'cons', 'recommended_for', 'price_value_assessment']}}
    ) AS x
  FROM CUSTOMER_REVIEWS
);

SELECT * FROM EXTRACTED_REVIEW_DATA ORDER BY review_id LIMIT 10;

-- Cross-validate AI sentiment against the star rating
SELECT review_id, rating, overall_sentiment, product_name
FROM EXTRACTED_REVIEW_DATA
WHERE (rating >= 4 AND overall_sentiment = 'negative')
   OR (rating <= 2 AND overall_sentiment = 'positive')
   OR (rating = 3 AND overall_sentiment <> 'neutral');"""

FB_7_3 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE TABLE EXTRACTED_TICKET_FINDINGS AS
SELECT ticket_id, category,
  x:root_cause::STRING AS root_cause,
  x:affected_product::STRING AS affected_product,
  x:customer_emotion::STRING AS customer_emotion,
  x:urgency_level::STRING AS urgency_level,
  x:resolution_complexity::STRING AS resolution_complexity,
  x:recommended_actions::ARRAY AS recommended_actions
FROM (
  SELECT ticket_id, category,
    AI_COMPLETE(
      model => 'claude-sonnet-4-5',
      prompt => 'Analyze this Alpine & Co. customer support ticket. Ticket: ' || description_text,
      response_format => {'type': 'json', 'schema': {'type': 'object', 'properties': {
        'root_cause': {'type': 'string'},
        'affected_product': {'type': 'string'},
        'customer_emotion': {'type': 'string', 'enum': ['frustrated', 'neutral', 'satisfied']},
        'urgency_level': {'type': 'string', 'enum': ['low', 'medium', 'high', 'critical']},
        'resolution_complexity': {'type': 'string', 'enum': ['simple', 'moderate', 'complex']},
        'recommended_actions': {'type': 'array', 'items': {'type': 'string'}}},
        'required': ['root_cause', 'affected_product', 'customer_emotion', 'urgency_level',
                     'resolution_complexity', 'recommended_actions']}}
    ) AS x
  FROM SUPPORT_TICKETS
);

SELECT 'customer_emotion' AS dimension, customer_emotion AS value, COUNT(*) AS tickets FROM EXTRACTED_TICKET_FINDINGS GROUP BY 1, 2
UNION ALL SELECT 'urgency_level', urgency_level, COUNT(*) FROM EXTRACTED_TICKET_FINDINGS GROUP BY 1, 2
UNION ALL SELECT 'resolution_complexity', resolution_complexity, COUNT(*) FROM EXTRACTED_TICKET_FINDINGS GROUP BY 1, 2
ORDER BY dimension, tickets DESC;"""

# ---------------------------------------------------------------------------
# Session 8 - Cortex Search & RAG
# ---------------------------------------------------------------------------

FB_8_1 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE TABLE CUSTOMER_KNOWLEDGE_BASE AS
SELECT 'REV-' || review_id AS doc_id, 'product_review' AS doc_type, review_text AS content,
       rating::VARCHAR AS metadata_rating, NULL::VARCHAR AS metadata_priority, NULL::VARCHAR AS metadata_condition
FROM CUSTOMER_REVIEWS
UNION ALL
SELECT 'TKT-' || ticket_id, 'support_ticket', description_text, NULL, priority, NULL
FROM SUPPORT_TICKETS
UNION ALL
SELECT 'RET-' || note_id, 'return_note', return_reason_text, NULL, NULL, product_condition
FROM PRODUCT_RETURN_NOTES;

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

SHOW CORTEX SEARCH SERVICES IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;"""

FB_8_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

SELECT 'sizing issues running shoes' AS query, r.value:doc_id::STRING AS doc_id, r.value:doc_type::STRING AS doc_type, LEFT(r.value:content::STRING, 200) AS snippet
FROM LATERAL FLATTEN(input => PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW('RETAIL_AI_DEMO.RETAIL_OPS.customer_feedback_search',
  '{"query": "sizing issues running shoes", "columns": ["doc_id", "doc_type", "content", "metadata_rating"], "limit": 3}'))['results']) r
UNION ALL
SELECT 'quality defect stitching', r.value:doc_id::STRING, r.value:doc_type::STRING, LEFT(r.value:content::STRING, 200)
FROM LATERAL FLATTEN(input => PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW('RETAIL_AI_DEMO.RETAIL_OPS.customer_feedback_search',
  '{"query": "quality defect stitching", "columns": ["doc_id", "doc_type", "content", "metadata_rating"], "limit": 3}'))['results']) r
UNION ALL
SELECT 'shipping damage (return notes only)', r.value:doc_id::STRING, r.value:doc_type::STRING, LEFT(r.value:content::STRING, 200)
FROM LATERAL FLATTEN(input => PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW('RETAIL_AI_DEMO.RETAIL_OPS.customer_feedback_search',
  '{"query": "shipping damage", "columns": ["doc_id", "doc_type", "content"], "filter": {"@eq": {"doc_type": "return_note"}}, "limit": 3}'))['results']) r
UNION ALL
SELECT 'comfortable everyday wear recommendation', r.value:doc_id::STRING, r.value:doc_type::STRING, LEFT(r.value:content::STRING, 200)
FROM LATERAL FLATTEN(input => PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW('RETAIL_AI_DEMO.RETAIL_OPS.customer_feedback_search',
  '{"query": "comfortable everyday wear recommendation", "columns": ["doc_id", "doc_type", "content", "metadata_rating"], "limit": 3}'))['results']) r;"""

FB_8_3 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

WITH search_results AS (
  SELECT PARSE_JSON(SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'RETAIL_AI_DEMO.RETAIL_OPS.customer_feedback_search',
    '{"query": "product quality issues defects improvements", "columns": ["doc_id", "doc_type", "content", "metadata_rating"], "limit": 5}'
  ))['results'] AS results
),
context AS (
  SELECT LISTAGG('[' || r.value:doc_id::STRING || '] ' || r.value:content::STRING, '\\n\\n---\\n\\n') AS combined_context
  FROM search_results, LATERAL FLATTEN(input => results) r
)
SELECT AI_COMPLETE('claude-sonnet-4-5',
  'You are a product quality analyst at Alpine & Co., a national apparel and footwear retailer. '
  || 'Based ONLY on the following customer feedback documents, answer the user question. Cite documents by their doc_id in square brackets. '
  || 'If the documents do not contain enough information, say so.\\n\\nSOURCE DOCUMENTS:\\n' || combined_context
  || '\\n\\nUSER QUESTION: What are the most common product quality issues reported by Alpine & Co. customers and what improvements should the product team prioritize?'
  || '\\n\\nProvide a structured answer with: 1) Common quality issues by category, 2) Most affected product lines, 3) Recommended improvements, 4) Priority ranking.'
)::STRING AS rag_response
FROM context;"""

# ---------------------------------------------------------------------------
# Session 9 - Vector Embeddings
# ---------------------------------------------------------------------------

FB_9_1 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE TABLE EMBEDDING_EXAMPLES AS
SELECT column1 AS text_id, column2 AS text_content, column3 AS category,
       AI_EMBED('snowflake-arctic-embed-l-v2.0', column2)::VECTOR(FLOAT, 1024) AS embedding
FROM VALUES
  (1,  'Running shoes feel too tight around the toe box', 'sizing'),
  (2,  'Athletic sneakers are uncomfortably narrow in the front', 'sizing'),
  (3,  'Winter coat zipper broke after two weeks', 'quality'),
  (4,  'Outerwear jacket zipper failed within first month of use', 'quality'),
  (5,  'Love the Summit activewear leggings for yoga', 'praise'),
  (6,  'Summit brand yoga pants are my favorite workout gear', 'praise'),
  (7,  'Ordered medium but fits like a small, very disappointed', 'complaint'),
  (8,  'Size medium runs way too small, need to exchange for large', 'complaint'),
  (9,  'Basecamp hoodie fabric pills after washing', 'fabric'),
  (10, 'Basecamp casual hoodie material deteriorates in the wash', 'fabric'),
  (11, 'Great boots for hiking in the rain', 'footwear'),
  (12, 'Looking for dress shoes for a wedding', 'occasion'),
  (13, 'Kids sneakers wore out in two months', 'kids'),
  (14, 'Excellent customer service helped with my return', 'service'),
  (15, 'Sale prices on summer sandals are unbeatable', 'promotion'),
  (16, 'The new fall collection colors are stunning', 'style'),
  (17, 'Shipping took longer than expected but product is fine', 'shipping'),
  (18, 'Loyalty rewards program needs better redemption options', 'loyalty');

-- Top 10 most similar pairs
SELECT a.text_content AS text_a, b.text_content AS text_b,
       ROUND(VECTOR_COSINE_SIMILARITY(a.embedding, b.embedding), 4) AS similarity
FROM EMBEDDING_EXAMPLES a JOIN EMBEDDING_EXAMPLES b ON a.text_id < b.text_id
ORDER BY similarity DESC LIMIT 10;

-- Top 5 least similar pairs
SELECT a.text_content AS text_a, b.text_content AS text_b,
       ROUND(VECTOR_COSINE_SIMILARITY(a.embedding, b.embedding), 4) AS similarity
FROM EMBEDDING_EXAMPLES a JOIN EMBEDDING_EXAMPLES b ON a.text_id < b.text_id
ORDER BY similarity ASC LIMIT 5;"""

FB_9_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE TABLE REVIEW_EMBEDDINGS AS
SELECT review_id, review_text,
       AI_EMBED('snowflake-arctic-embed-l-v2.0', review_text)::VECTOR(FLOAT, 1024) AS embedding
FROM CUSTOMER_REVIEWS;

-- Vector search vs keyword search, side by side
WITH q AS (
  SELECT AI_EMBED('snowflake-arctic-embed-l-v2.0', 'What reviews mention poor stitching quality or fabric defects?')::VECTOR(FLOAT, 1024) AS qe
),
vector_hits AS (
  SELECT r.review_id, ROUND(VECTOR_COSINE_SIMILARITY(r.embedding, q.qe), 4) AS similarity
  FROM REVIEW_EMBEDDINGS r, q
  ORDER BY similarity DESC LIMIT 5
),
keyword_hits AS (
  SELECT review_id FROM CUSTOMER_REVIEWS
  WHERE review_text ILIKE '%stitch%' OR review_text ILIKE '%defect%' OR review_text ILIKE '%quality%'
)
SELECT c.review_id, v.similarity,
  CASE WHEN v.review_id IS NOT NULL AND k.review_id IS NOT NULL THEN 'both'
       WHEN v.review_id IS NOT NULL THEN 'vector only'
       ELSE 'keyword only' END AS found_by,
  LEFT(c.review_text, 160) AS snippet
FROM CUSTOMER_REVIEWS c
LEFT JOIN vector_hits v ON v.review_id = c.review_id
LEFT JOIN keyword_hits k ON k.review_id = c.review_id
WHERE v.review_id IS NOT NULL OR k.review_id IS NOT NULL
ORDER BY v.similarity DESC NULLS LAST, c.review_id;"""

# ---------------------------------------------------------------------------
# Session 10 - Cortex Analyst & Semantic Views
# ---------------------------------------------------------------------------

_SV_BASE_TABLES = """    sales AS RETAIL_AI_DEMO.RETAIL_OPS.SALES_TRANSACTIONS PRIMARY KEY (transaction_id)
      WITH SYNONYMS = ('transactions', 'orders') COMMENT = 'Point-of-sale and e-commerce sales transactions, one row per sale',
    purchase_orders AS RETAIL_AI_DEMO.RETAIL_OPS.PURCHASE_ORDERS PRIMARY KEY (po_id)
      WITH SYNONYMS = ('POs', 'supplier orders') COMMENT = 'Purchase orders placed with suppliers and their delivery status',
    inventory AS RETAIL_AI_DEMO.RETAIL_OPS.INVENTORY_LEVELS PRIMARY KEY (snapshot_id)
      WITH SYNONYMS = ('stock', 'inventory levels') COMMENT = 'Point-in-time inventory position per store and product',
    products AS RETAIL_AI_DEMO.RETAIL_OPS.PRODUCTS PRIMARY KEY (product_id)
      COMMENT = 'Apparel and footwear product catalog, branded and private label (Summit, Basecamp)',
    stores AS RETAIL_AI_DEMO.RETAIL_OPS.STORES PRIMARY KEY (store_id)
      COMMENT = 'Alpine & Co. store locations (flagship, mall, outlet)',
    suppliers AS RETAIL_AI_DEMO.RETAIL_OPS.SUPPLIERS PRIMARY KEY (supplier_id)
      COMMENT = 'Domestic and international apparel and footwear suppliers'"""

_SV_BASE_RELATIONSHIPS = """    sales_to_products AS sales (product_id) REFERENCES products,
    sales_to_stores AS sales (store_id) REFERENCES stores,
    po_to_suppliers AS purchase_orders (supplier_id) REFERENCES suppliers,
    po_to_products AS purchase_orders (product_id) REFERENCES products,
    inventory_to_stores AS inventory (store_id) REFERENCES stores,
    inventory_to_products AS inventory (product_id) REFERENCES products"""

_SV_BASE_FACTS = """    sales.quantity AS quantity COMMENT = 'Units sold in the transaction',
    sales.unit_price AS unit_price COMMENT = 'Retail price per unit before discount',
    sales.discount_pct AS discount_pct COMMENT = 'Discount percent applied (higher in Nov-Dec and at outlets)',
    sales.total_amount AS total_amount COMMENT = 'Net sale amount after discount in USD',
    purchase_orders.quantity_ordered AS quantity_ordered COMMENT = 'Units ordered from the supplier',
    purchase_orders.quantity_received AS quantity_received COMMENT = 'Units actually received',
    purchase_orders.po_unit_cost AS unit_cost COMMENT = 'Negotiated cost per unit on the purchase order',
    purchase_orders.po_total_cost AS total_cost COMMENT = 'Total purchase order cost in USD',
    inventory.quantity_on_hand AS quantity_on_hand COMMENT = 'Units physically on hand',
    inventory.days_of_supply AS days_of_supply COMMENT = 'Days the on-hand stock will last at the current sales rate',
    inventory.stock_retail_value AS quantity_on_hand * products.retail_price COMMENT = 'On-hand units valued at retail price',
    products.retail_price AS retail_price COMMENT = 'Full retail price in USD',
    products.margin_pct AS margin_pct COMMENT = 'Gross margin percent at full price'"""

_SV_BASE_DIMENSIONS = """    products.category AS category WITH SYNONYMS = ('department', 'product type') COMMENT = 'Product category such as sneakers, outerwear, activewear',
    products.subcategory AS subcategory COMMENT = 'Product subcategory',
    products.brand AS brand WITH SYNONYMS = ('label', 'maker') COMMENT = 'Brand; Summit and Basecamp are Alpine & Co. private labels',
    products.season AS season COMMENT = 'Selling season of the product',
    products.gender AS gender COMMENT = 'Target gender: mens, womens, unisex, kids',
    products.product_name AS product_name COMMENT = 'Product name',
    stores.store_name AS store_name WITH SYNONYMS = ('location', 'branch') COMMENT = 'Store name',
    stores.city AS city COMMENT = 'Store city',
    stores.state AS state COMMENT = 'Store state',
    stores.store_type AS store_type COMMENT = 'Store format: flagship, mall, or outlet',
    sales.payment_method AS payment_method COMMENT = 'Payment method used',
    sales.channel AS channel WITH SYNONYMS = ('sales channel') COMMENT = 'in_store, online, or bopis (buy online pick up in store)',
    sales.transaction_date AS transaction_date COMMENT = 'Date of the sale',
    sales.transaction_month AS MONTH(transaction_date) COMMENT = 'Month number of the sale (11-12 = holiday season, 8 = back-to-school)',
    suppliers.company_name AS company_name WITH SYNONYMS = ('supplier', 'vendor') COMMENT = 'Supplier company name',
    suppliers.country AS country COMMENT = 'Supplier country',
    purchase_orders.po_status AS status COMMENT = 'PO status: ordered, shipped, received, partial, cancelled',
    purchase_orders.order_date AS order_date COMMENT = 'Date the PO was placed',
    purchase_orders.expected_delivery_date AS expected_delivery_date COMMENT = 'Promised delivery date',
    purchase_orders.actual_delivery_date AS actual_delivery_date COMMENT = 'Actual delivery date (null if not delivered)',
    inventory.inventory_status AS status COMMENT = 'Stock status: in_stock, low_stock, out_of_stock, overstock',
    inventory.snapshot_date AS snapshot_date COMMENT = 'Date of the inventory snapshot'"""

_SV_BASE_METRICS = """    sales.total_revenue AS SUM(sales.total_amount) COMMENT = 'Total net sales revenue in USD',
    sales.total_units_sold AS SUM(sales.quantity) COMMENT = 'Total units sold',
    sales.avg_transaction_value AS AVG(sales.total_amount) COMMENT = 'Average net amount per transaction',
    purchase_orders.total_purchase_cost AS SUM(purchase_orders.po_total_cost) COMMENT = 'Total purchase order cost (metric name differs from the TOTAL_COST column to avoid a name clash)',
    inventory.avg_days_of_supply AS AVG(inventory.days_of_supply) COMMENT = 'Average days of supply',
    inventory.inventory_value AS SUM(inventory.stock_retail_value) COMMENT = 'On-hand inventory valued at retail price'"""

_SV_AI_SQL = """  AI_SQL_GENERATION 'This is Alpine & Co. retail data. Alpine & Co. is a national apparel and footwear retailer with 120+ stores. Peak seasons are November-December (holiday) and August (back-to-school); "holiday season" means transaction_month IN (11, 12). Private labels are Summit (activewear) and Basecamp (casual basics). Revenue means net revenue (total_amount after discount).'"""

FB_10_1 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE SEMANTIC VIEW RETAIL_OPERATIONS_VIEW
  TABLES (
""" + _SV_BASE_TABLES + """
  )
  RELATIONSHIPS (
""" + _SV_BASE_RELATIONSHIPS + """
  )
  FACTS (
""" + _SV_BASE_FACTS + """
  )
  DIMENSIONS (
""" + _SV_BASE_DIMENSIONS + """
  )
  METRICS (
""" + _SV_BASE_METRICS + """
  )
  COMMENT = 'Alpine & Co. retail operations: sales, purchasing, and inventory'
""" + _SV_AI_SQL + """;

DESCRIBE SEMANTIC VIEW RETAIL_OPERATIONS_VIEW;"""

FB_10_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- Q2 "What is the average foot traffic by store on weekends?" cannot be answered yet:
-- STORE_FOOT_TRAFFIC is not part of RETAIL_OPERATIONS_VIEW. Try it in the Cortex Analyst
-- playground (AI & ML > Cortex Analyst > RETAIL_OPERATIONS_VIEW) to see how Analyst responds.

-- Q1 "What are the top 5 stores by total revenue?" - the SQL Cortex Analyst generates is equivalent to:
SELECT * FROM SEMANTIC_VIEW(
  RETAIL_OPERATIONS_VIEW
  DIMENSIONS stores.store_name
  METRICS sales.total_revenue
)
ORDER BY total_revenue DESC
LIMIT 5;"""

FB_10_3 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- Optional: ask an LLM to draft definitions from the new tables' schemas
SELECT AI_COMPLETE('claude-sonnet-4-5',
  'Suggest semantic view facts, dimensions (with synonyms) and metrics with short business comments for these Snowflake tables: '
  || LISTAGG(table_name || '.' || column_name || ' ' || data_type, ', '))::STRING AS suggestions
FROM RETAIL_AI_DEMO.INFORMATION_SCHEMA.COLUMNS
WHERE table_schema = 'RETAIL_OPS' AND table_name IN ('STORE_FOOT_TRAFFIC', 'DAILY_SALES_METRICS');

-- Recreate the view with the two new tables (8 tables total)
CREATE OR REPLACE SEMANTIC VIEW RETAIL_OPERATIONS_VIEW
  TABLES (
""" + _SV_BASE_TABLES + """,
    foot_traffic AS RETAIL_AI_DEMO.RETAIL_OPS.STORE_FOOT_TRAFFIC PRIMARY KEY (traffic_id)
      WITH SYNONYMS = ('footfall', 'store traffic') COMMENT = 'Hourly in-store visitor counts from door sensors',
    daily_metrics AS RETAIL_AI_DEMO.RETAIL_OPS.DAILY_SALES_METRICS PRIMARY KEY (metric_id)
      WITH SYNONYMS = ('daily KPIs', 'store performance') COMMENT = 'Daily store KPIs including returns'
  )
  RELATIONSHIPS (
""" + _SV_BASE_RELATIONSHIPS + """,
    traffic_to_stores AS foot_traffic (store_id) REFERENCES stores,
    daily_metrics_to_stores AS daily_metrics (store_id) REFERENCES stores
  )
  FACTS (
""" + _SV_BASE_FACTS + """,
    foot_traffic.visitor_count AS visitor_count WITH SYNONYMS = ('foot traffic', 'walk-ins', 'visitors') COMMENT = 'Visitors entering the store in the hour',
    foot_traffic.conversion_rate_pct AS conversion_rate_pct COMMENT = 'Percent of visitors who made a purchase',
    foot_traffic.avg_basket_size AS avg_basket_size COMMENT = 'Average basket value in USD',
    daily_metrics.daily_revenue AS total_revenue COMMENT = 'Daily store revenue in USD',
    daily_metrics.transaction_count AS transaction_count COMMENT = 'Number of transactions that day',
    daily_metrics.units_sold AS units_sold COMMENT = 'Units sold that day',
    daily_metrics.returns_count AS returns_count COMMENT = 'Number of returns that day',
    daily_metrics.returns_value AS returns_value COMMENT = 'Value of returns in USD',
    daily_metrics.online_orders_fulfilled AS online_orders_fulfilled COMMENT = 'Online orders fulfilled by the store'
  )
  DIMENSIONS (
""" + _SV_BASE_DIMENSIONS + """,
    foot_traffic.traffic_timestamp AS "TIMESTAMP" COMMENT = 'Hour of the traffic reading',
    foot_traffic.weather_condition AS weather_condition COMMENT = 'Weather during the hour: sunny, cloudy, rain, snow',
    foot_traffic.is_weekend AS is_weekend COMMENT = 'TRUE on Saturday and Sunday',
    foot_traffic.is_holiday AS is_holiday COMMENT = 'TRUE on public holidays',
    daily_metrics.metric_date AS "DATE" COMMENT = 'Business date of the daily KPIs'
  )
  METRICS (
""" + _SV_BASE_METRICS + """,
    foot_traffic.avg_foot_traffic AS AVG(foot_traffic.visitor_count) COMMENT = 'Average hourly visitors',
    foot_traffic.total_visitors AS SUM(foot_traffic.visitor_count) COMMENT = 'Total visitors',
    foot_traffic.avg_conversion_rate AS AVG(foot_traffic.conversion_rate_pct) COMMENT = 'Average conversion rate percent',
    daily_metrics.total_returns AS SUM(daily_metrics.returns_count) COMMENT = 'Total number of returns',
    daily_metrics.return_rate AS SUM(daily_metrics.returns_count) / NULLIF(SUM(daily_metrics.transaction_count), 0)
      COMMENT = 'Returns as a share of transactions'
  )
  COMMENT = 'Alpine & Co. retail operations: sales, purchasing, inventory, foot traffic, and daily store KPIs'
""" + _SV_AI_SQL + """;

DESCRIBE SEMANTIC VIEW RETAIL_OPERATIONS_VIEW;"""

FB_10_4 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- 1. Average foot traffic by store on weekends (failed in 10.2, works now)
SELECT * FROM SEMANTIC_VIEW(
  RETAIL_OPERATIONS_VIEW
  DIMENSIONS stores.store_name
  METRICS foot_traffic.avg_foot_traffic
  WHERE foot_traffic.is_weekend = TRUE
)
ORDER BY avg_foot_traffic DESC;

-- 2. Share of revenue online vs in-store by category
SELECT category, channel, total_revenue,
       ROUND(100 * total_revenue / SUM(total_revenue) OVER (PARTITION BY category), 1) AS pct_of_category
FROM SEMANTIC_VIEW(
  RETAIL_OPERATIONS_VIEW
  DIMENSIONS products.category, sales.channel
  METRICS sales.total_revenue
)
ORDER BY category, channel;

-- 3. Stores with the highest return rates
SELECT * FROM SEMANTIC_VIEW(
  RETAIL_OPERATIONS_VIEW
  DIMENSIONS stores.store_name
  METRICS daily_metrics.return_rate, daily_metrics.total_returns
)
ORDER BY return_rate DESC;

-- 4. Top-selling brands during holiday season (Nov-Dec)
SELECT * FROM SEMANTIC_VIEW(
  RETAIL_OPERATIONS_VIEW
  DIMENSIONS products.brand
  METRICS sales.total_units_sold, sales.total_revenue
  WHERE sales.transaction_month IN (11, 12)
)
ORDER BY total_units_sold DESC
LIMIT 5;"""

# ---------------------------------------------------------------------------
# Session 11 - Cortex Agents
# ---------------------------------------------------------------------------

_AGENT_INSTRUCTIONS = """  instructions:
    response: "You are the Alpine & Co. Retail Operations Assistant. Be concise and actionable, cite numbers from the data, and answer in the same language as the question (English or Spanish)."
    orchestration: "Alpine & Co. is a national apparel and footwear retailer with 120+ stores. Peak seasons are Nov-Dec (holiday) and August (back-to-school). Private labels are Summit (activewear) and Basecamp (casual basics). Use retail_analytics for sales, revenue, inventory, purchase order, supplier, foot traffic and returns metrics. Use customer_feedback for customer reviews, support tickets, complaints and return reasons. Use both and combine the results when a question mixes metrics and customer feedback."
    sample_questions:
      - question: "What are the top 5 product categories by revenue?"
      - question: "What are customers saying about Summit activewear quality?"
      - question: "Which stores have the lowest days of supply right now?"
      - question: "What are the most common complaints in support tickets?"
"""

_AGENT_BASE_TOOLS = """    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "retail_analytics"
        description: "Answers questions about Alpine & Co. sales, revenue, units, channels, inventory levels, days of supply, purchase orders, suppliers, store foot traffic and return rates using the RETAIL_OPERATIONS_VIEW semantic view. Do not use for review or complaint text."
    - tool_spec:
        type: "cortex_search"
        name: "customer_feedback"
        description: "Searches customer reviews, support tickets and product return notes. Use for what customers say, complaints, quality issues, sizing feedback and return reasons. Filter with doc_type = product_review, support_ticket or return_note."
"""

_AGENT_BASE_RESOURCES = """    retail_analytics:
      semantic_view: "RETAIL_AI_DEMO.RETAIL_OPS.RETAIL_OPERATIONS_VIEW"
      execution_environment:
        type: "warehouse"
        warehouse: "RETAIL_AI_WH"
    customer_feedback:
      search_service: "RETAIL_AI_DEMO.RETAIL_OPS.CUSTOMER_FEEDBACK_SEARCH"
      id_column: "DOC_ID"
      max_results: 5
"""

FB_11_1 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE AGENT RETAIL_OPS_AGENT
  COMMENT = 'Alpine & Co. Retail Operations Assistant'
  PROFILE = '{"display_name": "Alpine & Co. Retail Ops Assistant", "color": "blue"}'
  FROM SPECIFICATION
$$
  models:
    orchestration: auto

""" + _AGENT_INSTRUCTIONS + """
  tools:
""" + _AGENT_BASE_TOOLS + """
  tool_resources:
""" + _AGENT_BASE_RESOURCES + """$$;

SHOW AGENTS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;"""

_AGENT_RUN = """SELECT '{q}' AS question,
  LISTAGG(IFF(c.value:type::STRING = 'text', c.value:text::STRING, NULL), '\\n') AS answer,
  ARRAY_UNIQUE_AGG(IFF(c.value:type::STRING = 'tool_use', c.value:tool_use:name::STRING, NULL)) AS tools_used
FROM (
  SELECT TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    'RETAIL_AI_DEMO.RETAIL_OPS.RETAIL_OPS_AGENT',
    $${"messages": [{"role": "user", "content": [{"type": "text", "text": "{q}"}]}]}$$
  )) AS resp
) r, TABLE(FLATTEN(r.resp:content)) c;"""

FB_11_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- Each query takes 10-60 seconds. Run them one at a time.
""" + "\n\n".join(_AGENT_RUN.replace("{q}", q) for q in [
    "What are the top-selling product categories and which stores are driving the most revenue?",
    "What are customers saying about the quality of Summit activewear products?",
    "Which product categories have both the highest sales AND the most customer complaints? Is there a correlation?",
    "Cuales son los productos mas vendidos en las tiendas de California?",
])

FB_11_3 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

CREATE OR REPLACE FUNCTION RETAIL_AI_DEMO.RETAIL_OPS.CALCULATE_STOCKOUT_RISK(
    product_category VARCHAR, current_inventory NUMBER, avg_daily_sales NUMBER)
RETURNS OBJECT
LANGUAGE SQL
AS
$$
  SELECT OBJECT_CONSTRUCT(
    'category', product_category,
    'current_inventory', current_inventory,
    'avg_daily_sales', avg_daily_sales,
    'days_of_supply', CASE WHEN avg_daily_sales > 0 THEN ROUND(current_inventory / avg_daily_sales, 1) ELSE 999 END,
    'risk_level', CASE
        WHEN avg_daily_sales > 0 AND (current_inventory / avg_daily_sales) < 3 THEN 'HIGH'
        WHEN avg_daily_sales > 0 AND (current_inventory / avg_daily_sales) < 7 THEN 'MEDIUM'
        ELSE 'LOW' END,
    'recommendation', CASE
        WHEN avg_daily_sales > 0 AND (current_inventory / avg_daily_sales) < 3
          THEN 'Immediate reorder required - contact supplier for expedited shipment and consider cross-store transfers'
        WHEN avg_daily_sales > 0 AND (current_inventory / avg_daily_sales) < 7
          THEN 'Place standard reorder - monitor sell-through rate and adjust quantities for upcoming promotions'
        ELSE 'Adequate inventory - review reorder point and consider markdowns if days of supply exceeds 30' END
  )
$$;

SELECT CALCULATE_STOCKOUT_RISK('sneakers', 50, 12) AS medium_risk,
       CALCULATE_STOCKOUT_RISK('outerwear', 10, 8) AS high_risk,
       CALCULATE_STOCKOUT_RISK('accessories', 400, 5) AS low_risk;

-- Recreate the agent with the UDF as a third (custom) tool
CREATE OR REPLACE AGENT RETAIL_OPS_AGENT
  COMMENT = 'Alpine & Co. Retail Operations Assistant'
  PROFILE = '{"display_name": "Alpine & Co. Retail Ops Assistant", "color": "blue"}'
  FROM SPECIFICATION
$$
  models:
    orchestration: auto

""" + _AGENT_INSTRUCTIONS.replace(
    "Use both and combine",
    "Use calculate_stockout_risk when asked for stockout risk given a category, inventory units and daily sales (get inventory from retail_analytics first if needed). Use all relevant tools and combine",
) + """
  tools:
""" + _AGENT_BASE_TOOLS + """    - tool_spec:
        type: "generic"
        name: "calculate_stockout_risk"
        description: "Calculates days of supply, stockout risk level (HIGH/MEDIUM/LOW) and a replenishment recommendation for a product category."
        input_schema:
          type: "object"
          properties:
            product_category:
              type: "string"
              description: "Product category, e.g. sneakers, outerwear, activewear"
            current_inventory:
              type: "number"
              description: "Units currently on hand"
            avg_daily_sales:
              type: "number"
              description: "Average units sold per day"
          required: ["product_category", "current_inventory", "avg_daily_sales"]

  tool_resources:
""" + _AGENT_BASE_RESOURCES + """    calculate_stockout_risk:
      type: "function"
      identifier: "RETAIL_AI_DEMO.RETAIL_OPS.CALCULATE_STOCKOUT_RISK"
      execution_environment:
        type: "warehouse"
        warehouse: "RETAIL_AI_WH"
$$;

DESCRIBE AGENT RETAIL_OPS_AGENT;"""

FB_11_4 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- Each query takes 10-90 seconds. Run them one at a time.
""" + "\n\n".join(_AGENT_RUN.replace("{q}", q) for q in [
    "What is the stockout risk for sneakers if we have 50 units and sell 12 per day?",
    "What are the current inventory levels for each category and what would the stockout risk be during holiday season with doubled demand?",
    "For our Portland store, show me current sales performance, any customer complaints, and the stockout risk assessment for activewear.",
])

# ---------------------------------------------------------------------------
# Session 12 - Build Apps (Streamlit + React)
# ---------------------------------------------------------------------------

# Streamlit app source. Kept free of $$, triple quotes and backslashes so it can be
# embedded verbatim in a $$-quoted SQL string literal.
_STREAMLIT_APP = '''import streamlit as st
import pydeck as pdk
import plotly.express as px

st.set_page_config(page_title="Alpine & Co. Retail Dashboard", page_icon=":material/storefront:", layout="wide")

DB = "RETAIL_AI_DEMO.RETAIL_OPS"
session = st.connection("snowflake").session()


@st.cache_data(ttl=600, show_spinner=False)
def q(sql):
    return session.sql(sql).to_pandas()


def sales_dashboard():
    st.title(":material/monitoring: Sales Dashboard")
    kpi = q(f"""SELECT SUM(total_amount) AS rev, SUM(quantity) AS units, AVG(total_amount) AS atv,
        100 * SUM(IFF(channel = 'online', total_amount, 0)) / NULLIF(SUM(total_amount), 0) AS online_pct
        FROM {DB}.SALES_TRANSACTIONS
        WHERE transaction_date > DATEADD(month, -1, (SELECT MAX(transaction_date) FROM {DB}.SALES_TRANSACTIONS))""").iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue (latest month)", f"${kpi.REV:,.0f}")
    c2.metric("Units sold", f"{kpi.UNITS:,.0f}")
    c3.metric("Avg transaction value", f"${kpi.ATV:,.2f}")
    c4.metric("Online sales %", f"{kpi.ONLINE_PCT:.1f}%")

    left, right = st.columns(2)
    with left:
        st.subheader("Revenue by store")
        stores = q(f"""SELECT s.store_name, s.latitude, s.longitude, SUM(t.total_amount) AS revenue
            FROM {DB}.STORES s JOIN {DB}.SALES_TRANSACTIONS t ON t.store_id = s.store_id GROUP BY 1, 2, 3""")
        layer = pdk.Layer("ScatterplotLayer", data=stores, get_position="[LONGITUDE, LATITUDE]",
                          get_radius="REVENUE * 25", get_fill_color=[41, 181, 232, 160], pickable=True)
        view = pdk.ViewState(latitude=39.5, longitude=-98.35, zoom=3)
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, tooltip={"text": "{STORE_NAME}"}))
    with right:
        st.subheader("Revenue by category")
        cat = q(f"""SELECT p.category, SUM(t.total_amount) AS revenue
            FROM {DB}.SALES_TRANSACTIONS t JOIN {DB}.PRODUCTS p ON p.product_id = t.product_id
            GROUP BY 1 ORDER BY 2 DESC""")
        st.plotly_chart(px.bar(cat, x="CATEGORY", y="REVENUE"), width="stretch")

    st.subheader("Daily sales (last 90 days of data)")
    daily = q(f"""SELECT transaction_date, SUM(total_amount) AS revenue FROM {DB}.SALES_TRANSACTIONS
        WHERE transaction_date > DATEADD(day, -90, (SELECT MAX(transaction_date) FROM {DB}.SALES_TRANSACTIONS))
        GROUP BY 1 ORDER BY 1""")
    st.plotly_chart(px.line(daily, x="TRANSACTION_DATE", y="REVENUE"), width="stretch")

    st.subheader("Top 10 stockout risks")
    st.dataframe(q(f"""SELECT store_name, product_name, category, quantity_on_hand, days_of_supply,
        predicted_stockout_probability FROM {DB}.LIVE_STOCKOUT_SCORES
        ORDER BY predicted_stockout_probability DESC, days_of_supply LIMIT 10"""), hide_index=True)


def retail_chat():
    st.title(":material/chat: Retail Intelligence Chat")
    with st.sidebar:
        model = st.selectbox("LLM model", ["claude-sonnet-4-5", "llama3.3-70b", "mistral-large2"])
        st.markdown("**Top sellers (latest week)**")
        st.dataframe(q(f"""SELECT p.product_name, SUM(t.quantity) AS units
            FROM {DB}.SALES_TRANSACTIONS t JOIN {DB}.PRODUCTS p ON p.product_id = t.product_id
            WHERE t.transaction_date > DATEADD(day, -7, (SELECT MAX(transaction_date) FROM {DB}.SALES_TRANSACTIONS))
            GROUP BY 1 ORDER BY 2 DESC LIMIT 5"""), hide_index=True)

    context = q(f"""SELECT LISTAGG(category || ': $' || ROUND(rev) || ' revenue, ' || units || ' units', '; ') AS ctx
        FROM (SELECT p.category, SUM(t.total_amount) AS rev, SUM(t.quantity) AS units
              FROM {DB}.SALES_TRANSACTIONS t JOIN {DB}.PRODUCTS p ON p.product_id = t.product_id GROUP BY 1)""").iloc[0].CTX

    if "messages" not in st.session_state:
        st.session_state.messages = []
    for m in st.session_state.messages:
        st.chat_message(m["role"]).markdown(m["content"])
    if question := st.chat_input("Ask about Alpine & Co. sales, products or customers"):
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").markdown(question)
        prompt = ("You are a retail analyst for Alpine & Co., an apparel and footwear retailer. "
                  f"Sales by category: {context}. Answer concisely. Question: {question}")
        with st.chat_message("assistant"), st.spinner("Thinking..."):
            answer = session.sql("SELECT AI_COMPLETE(?, ?)::STRING", params=[model, prompt]).collect()[0][0]
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})


def customer_insights():
    st.title(":material/groups: Customer Insights")
    k = q(f"""SELECT (SELECT COUNT(*) FROM {DB}.CUSTOMER_REVIEWS WHERE review_date > DATEADD(day, -30, CURRENT_DATE())) AS reviews,
        (SELECT AVG(rating) FROM {DB}.CUSTOMER_REVIEWS) AS avg_rating,
        (SELECT COUNT(*) FROM {DB}.SUPPORT_TICKETS WHERE status IN ('open', 'in_progress', 'escalated')) AS open_tickets""").iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Reviews (last 30 days)", int(k.REVIEWS))
    c2.metric("Average rating", f"{k.AVG_RATING:.2f}")
    c3.metric("Open support tickets", int(k.OPEN_TICKETS))

    tickets = q(f"""SELECT ticket_id, created_date, priority, category, status, LEFT(description_text, 120) AS summary
        FROM {DB}.SUPPORT_TICKETS ORDER BY created_date DESC""")
    colors = {"urgent": "#ff4b4b", "high": "#ffa421", "medium": "#ffe312", "low": "#21c354"}
    left, right = st.columns([2, 1])
    with left:
        st.subheader("Recent support tickets")
        styled = tickets.style.map(lambda v: f"background-color: {colors.get(v, '')}; color: black" if v in colors else "",
                                   subset=["PRIORITY"])
        st.dataframe(styled, hide_index=True)
    with right:
        st.subheader("Tickets by category")
        by_cat = tickets.groupby("CATEGORY").size().reset_index(name="TICKETS")
        st.plotly_chart(px.pie(by_cat, names="CATEGORY", values="TICKETS", hole=0.4), width="stretch")


page = st.navigation([
    st.Page(sales_dashboard, title="Sales Dashboard", icon=":material/monitoring:"),
    st.Page(retail_chat, title="Retail Intelligence Chat", icon=":material/chat:"),
    st.Page(customer_insights, title="Customer Insights", icon=":material/groups:"),
])
page.run()
'''

_PYPROJECT = '''[project]
name = "retail-ai-dashboard"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = ["streamlit[snowflake]>=1.50.0", "pydeck", "plotly"]
'''

_RAW_FILE_FORMAT = """FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE FIELD_DELIMITER = NONE RECORD_DELIMITER = NONE
                 ESCAPE_UNENCLOSED_FIELD = NONE FIELD_OPTIONALLY_ENCLOSED_BY = NONE)
  HEADER = FALSE SINGLE = TRUE OVERWRITE = TRUE"""

FB_12_1 = """USE ROLE ACCOUNTADMIN;
USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- 1. Compute pool for the container runtime
CREATE COMPUTE POOL IF NOT EXISTS RETAIL_AI_COMPUTE_POOL
  MIN_NODES = 1 MAX_NODES = 1 INSTANCE_FAMILY = CPU_X64_S AUTO_SUSPEND_SECS = 600;

-- 2. Package access: Snowflake's built-in PyPI mirror (works on trial accounts,
--    which do not support external access integrations)
GRANT DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER TO ROLE ACCOUNTADMIN;

-- 3. Stage holding the app source
CREATE STAGE IF NOT EXISTS STREAMLIT_STAGE ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

COPY INTO @STREAMLIT_STAGE/pyproject.toml FROM (SELECT $$""" + _PYPROJECT + """$$)
  """ + _RAW_FILE_FORMAT + """;

COPY INTO @STREAMLIT_STAGE/streamlit_app.py FROM (SELECT $$""" + _STREAMLIT_APP + """$$)
  """ + _RAW_FILE_FORMAT + """;

-- 4. The Streamlit app on the container runtime
CREATE OR REPLACE STREAMLIT RETAIL_DASHBOARD
  FROM '@RETAIL_AI_DEMO.RETAIL_OPS.STREAMLIT_STAGE'
  MAIN_FILE = 'streamlit_app.py'
  RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL = RETAIL_AI_COMPUTE_POOL
  QUERY_WAREHOUSE = RETAIL_AI_WH
  ARTIFACT_REPOSITORIES = (snowflake.snowpark.pypi_shared_repository)
  TITLE = 'Alpine & Co. Retail Dashboard';

LIST @STREAMLIT_STAGE;"""

FB_12_2 = """SHOW COMPUTE POOLS LIKE 'RETAIL_AI_COMPUTE_POOL';
SHOW STREAMLITS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;
DESCRIBE STREAMLIT RETAIL_AI_DEMO.RETAIL_OPS.RETAIL_DASHBOARD;

-- Direct link: Snowsight > Projects > Streamlit > RETAIL_DASHBOARD, or build it from this:
SELECT 'https://app.snowflake.com/' || LOWER(CURRENT_ORGANIZATION_NAME()) || '/' || LOWER(CURRENT_ACCOUNT_NAME())
       || '/#/streamlit-apps/RETAIL_AI_DEMO.RETAIL_OPS.RETAIL_DASHBOARD' AS app_url;"""

# React / Next.js apps run on Snowflake App Runtime and are built from Cortex Code Desktop or CLI.
FB_12_3 = """# Run from a terminal with Snowflake CLI 3.x and Node.js 20+ installed.
# Not available on trial accounts.

# 1. Scaffold a Next.js (React) app
npx create-next-app@latest retail-react-app --ts --tailwind --app --eslint --use-npm --no-src-dir --import-alias "@/*"
cd retail-react-app
npm install snowflake-sdk

# 2. Generate the app.yml deployment manifest (pick database RETAIL_AI_DEMO, schema RETAIL_OPS,
#    warehouse RETAIL_AI_WH when prompted)
snow app setup

# 3. Build remotely and deploy - prints the live *.snowflakecomputing.app URL
snow app deploy"""

FB_12_4 = """SHOW APPLICATION SERVICES IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;"""

# ---------------------------------------------------------------------------
# Session 13 - Observability & Cost
# ---------------------------------------------------------------------------

FB_13_1 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- ACCOUNT_USAGE views lag by up to a few hours; very recent calls may not appear yet.

-- 1. AI function calls, tokens and credits by function and model (last 2 days)
SELECT function_name, model_name, COUNT(*) AS usage_rows, SUM(tokens) AS tokens, ROUND(SUM(token_credits), 4) AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_USAGE_HISTORY
WHERE start_time >= DATEADD(day, -2, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY credits DESC;

-- 2. Credits by service type: warehouses vs AI services, search, agents, containers
SELECT service_type, ROUND(SUM(credits_used), 3) AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
WHERE usage_date >= DATEADD(day, -2, CURRENT_DATE())
GROUP BY 1
ORDER BY credits DESC;

SELECT warehouse_name, ROUND(SUM(credits_used), 3) AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE warehouse_name = 'RETAIL_AI_WH' AND start_time >= DATEADD(day, -2, CURRENT_TIMESTAMP())
GROUP BY 1;

-- 3. Cortex Search service health
DESCRIBE CORTEX SEARCH SERVICE customer_feedback_search;

-- 4. The most expensive AI queries of the workshop
SELECT q.query_id, LEFT(q.query_text, 80) AS query_snippet, q.total_elapsed_time / 1000 AS seconds,
       u.function_name, u.model_name, u.tokens, ROUND(u.token_credits, 5) AS token_credits
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_QUERY_USAGE_HISTORY u
JOIN SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY q ON q.query_id = u.query_id
WHERE q.start_time >= DATEADD(day, -2, CURRENT_TIMESTAMP())
ORDER BY u.token_credits DESC
LIMIT 20;"""

FB_13_2 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- 1. Workshop cost breakdown by component
SELECT CASE
         WHEN service_type = 'WAREHOUSE_METERING' THEN 'Warehouse compute (' || name || ')'
         WHEN service_type IN ('AI_SERVICES', 'AI_FUNCTIONS') THEN 'Cortex AI functions'
         WHEN service_type = 'CORTEX_SEARCH' THEN 'Cortex Search serving'
         WHEN service_type = 'CORTEX_AGENTS' THEN 'Cortex Agents'
         WHEN service_type = 'SNOWPARK_CONTAINER_SERVICES' THEN 'Containers (Streamlit / notebooks)'
         ELSE service_type END AS component,
       ROUND(SUM(credits_used), 3) AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY
WHERE start_time >= DATEADD(day, -2, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY credits DESC;

-- 2. Let an LLM recommend production optimizations from the actual usage
WITH usage AS (
  SELECT LISTAGG(service_type || '=' || ROUND(credits, 3), ', ') AS usage_summary
  FROM (SELECT service_type, SUM(credits_used) AS credits
        FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
        WHERE usage_date >= DATEADD(day, -2, CURRENT_DATE()) GROUP BY 1)
)
SELECT AI_COMPLETE('claude-sonnet-4-5',
  'You are a Snowflake cost optimization expert. A retail AI workshop used these credits: ' || usage_summary
  || '. Workloads: AI_SENTIMENT/AI_CLASSIFY/AI_EXTRACT on ~100 text rows, AI_COMPLETE with claude-sonnet-4-5 and llama3.3-70b, '
  || 'a Cortex Search service with TARGET_LAG 1 hour, a dynamic table with TARGET_LAG 1 minute scoring an ML model, '
  || 'a MEDIUM warehouse, a Cortex Agent and a Streamlit app on a compute pool. Recommend: 1) which LLM to use for each use case, '
  || '2) warehouse sizing per workload, 3) Cortex Search TARGET_LAG, 4) dynamic tables vs scheduled tasks for stockout scoring. Use a short table.'
)::STRING AS recommendations
FROM usage;"""

FB_13_3 = """USE SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- 1. Object inventory
SELECT table_type AS object_type, table_name AS object_name, row_count, created
FROM RETAIL_AI_DEMO.INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'RETAIL_OPS'
UNION ALL SELECT 'FUNCTION', function_name, NULL, created FROM RETAIL_AI_DEMO.INFORMATION_SCHEMA.FUNCTIONS WHERE function_schema = 'RETAIL_OPS'
UNION ALL SELECT 'STAGE', stage_name, NULL, created FROM RETAIL_AI_DEMO.INFORMATION_SCHEMA.STAGES WHERE stage_schema = 'RETAIL_OPS'
ORDER BY created;

SHOW DYNAMIC TABLES IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;
SHOW SNOWFLAKE.ML.CLASSIFICATION IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;
SHOW MODELS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;
SHOW CORTEX SEARCH SERVICES IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;
SHOW SEMANTIC VIEWS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;
SHOW AGENTS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;
SHOW STREAMLITS IN SCHEMA RETAIL_AI_DEMO.RETAIL_OPS;

-- 2 + 3. Creation timeline and an AI-written summary of what was built
WITH objs AS (
  SELECT table_type AS object_type, table_name AS object_name, created
  FROM RETAIL_AI_DEMO.INFORMATION_SCHEMA.TABLES WHERE table_schema = 'RETAIL_OPS'
  UNION ALL SELECT 'FUNCTION', function_name, created FROM RETAIL_AI_DEMO.INFORMATION_SCHEMA.FUNCTIONS WHERE function_schema = 'RETAIL_OPS'
)
SELECT AI_COMPLETE('claude-sonnet-4-5',
  'In 8 bullet points, summarize the end-to-end AI pipeline a retail team built today in Snowflake, from raw data to deployed apps. '
  || 'Objects in creation order: ' || LISTAGG(object_type || ' ' || object_name, ', ') WITHIN GROUP (ORDER BY created)
  || ', plus a Snowflake ML classification model, a registered STOCKOUT_PREDICTOR model, the CUSTOMER_FEEDBACK_SEARCH Cortex Search service, '
  || 'the RETAIL_OPERATIONS_VIEW semantic view, the RETAIL_OPS_AGENT Cortex Agent and the RETAIL_DASHBOARD Streamlit app.'
)::STRING AS workshop_summary
FROM objs;"""

