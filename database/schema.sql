CREATE DATABASE IF NOT EXISTS retail_business;

USE retail_business;

CREATE TABLE IF NOT EXISTS retail_sales (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date DATE,
    product VARCHAR(100),
    category VARCHAR(100),
    region VARCHAR(100),
    customer VARCHAR(100),
    sales DECIMAL(12,2),
    profit DECIMAL(12,2),
    quantity INT,
    order_month VARCHAR(20),
    order_year INT,
    sales_margin DECIMAL(10,2),
    revenue DECIMAL(12,2)
);
