-- Enable foreign keys
PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS product_category_name_translation (
    product_category_name TEXT PRIMARY KEY,
    product_category_name_english TEXT
);

CREATE TABLE IF NOT EXISTS olist_geolocation (
    olist_geo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    geolocation_zip_code_prefix TEXT,
    geolocation_lat REAL,
    geolocation_lng REAL,
    geolocation_city TEXT,
    geolocation_state TEXT,
    UNIQUE(geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state)
);

CREATE TABLE IF NOT EXISTS olist_sellers (
    seller_id TEXT PRIMARY KEY,
    seller_zip_code_prefix TEXT,
    seller_city TEXT,
    seller_state TEXT
);

CREATE TABLE IF NOT EXISTS olist_products (
    product_id TEXT PRIMARY KEY,
    product_category_name TEXT,
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,
    product_weight_g REAL,
    product_length_cm REAL,
    product_height_cm REAL,
    product_width_cm REAL,
    FOREIGN KEY(product_category_name)
        REFERENCES product_category_name_translation(product_category_name)
        ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS olist_customers (
    customer_id TEXT PRIMARY KEY,
    customer_unique_id TEXT,
    customer_zip_code_prefix TEXT,
    customer_city TEXT,
    customer_state TEXT,
    FOREIGN KEY(customer_zip_code_prefix)
        REFERENCES olist_geolocation(geolocation_zip_code_prefix)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS olist_orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    order_status TEXT,
    order_purchase_timestamp TEXT,
    order_approved_at TEXT,
    order_delivered_carrier_date TEXT,
    order_delivered_customer_date TEXT,
    order_estimated_delivery_date TEXT,
    FOREIGN KEY(customer_id)
        REFERENCES olist_customers(customer_id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS olist_order_items (
    olist_order_items_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,
    order_item_id INTEGER NOT NULL,
    product_id TEXT,
    seller_id TEXT,
    shipping_limit_date TEXT,
    price REAL,
    freight_value REAL,
    UNIQUE(order_id, order_item_id),
    FOREIGN KEY(order_id)
        REFERENCES olist_orders(order_id)
        ON DELETE CASCADE,
    FOREIGN KEY(product_id)
        REFERENCES olist_products(product_id)
        ON DELETE SET NULL,
    FOREIGN KEY(seller_id)
        REFERENCES olist_sellers(seller_id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS olist_order_payments (
    olist_payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,
    payment_sequential INTEGER,
    payment_type TEXT,
    payment_installments INTEGER,
    payment_value REAL,
    UNIQUE(order_id, payment_sequential),
    FOREIGN KEY(order_id)
        REFERENCES olist_orders(order_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS olist_order_reviews (
    review_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TEXT,
    review_answer_timestamp TEXT,
    FOREIGN KEY(order_id)
        REFERENCES olist_orders(order_id)
        ON DELETE CASCADE
);
