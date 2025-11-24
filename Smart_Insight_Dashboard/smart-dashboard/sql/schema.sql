CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    category TEXT,
    sub_category TEXT,
    product_name TEXT
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT,
    segment TEXT,
    region TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT
);

CREATE TABLE IF NOT EXISTS sales (
    order_id TEXT,
    order_date DATE,
    ship_date DATE,
    ship_mode TEXT,
    customer_id TEXT,
    product_id TEXT,
    sales REAL,
    quantity INTEGER,
    discount REAL,
    profit REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS forecast_results (
    forecast_date DATE,
    metric TEXT,
    predicted_value REAL,
    lower_ci REAL,
    upper_ci REAL,
    model_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
