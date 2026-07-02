from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import pandas as pd
import mysql.connector
from mysql.connector import Error


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [col.strip().replace(' ', ' ') for col in cleaned.columns]

    required_columns = {
        'Order ID': 'Order ID',
        'Date': 'Date',
        'Product': 'Product',
        'Category': 'Category',
        'Region': 'Region',
        'Customer': 'Customer',
        'Sales': 'Sales',
        'Profit': 'Profit',
        'Quantity': 'Quantity',
    }

    for expected, actual in required_columns.items():
        if expected not in cleaned.columns:
            cleaned[expected] = pd.NA

    cleaned = cleaned.dropna(subset=['Order ID', 'Date', 'Product', 'Category', 'Region', 'Customer'])
    cleaned = cleaned.drop_duplicates(subset=['Order ID'])

    cleaned['Order Date'] = pd.to_datetime(cleaned['Date'], errors='coerce')
    cleaned = cleaned.dropna(subset=['Order Date'])

    cleaned['Sales'] = pd.to_numeric(cleaned['Sales'], errors='coerce')
    cleaned['Profit'] = pd.to_numeric(cleaned['Profit'], errors='coerce')
    cleaned['Quantity'] = pd.to_numeric(cleaned['Quantity'], errors='coerce')
    cleaned = cleaned.dropna(subset=['Sales', 'Profit', 'Quantity'])

    cleaned['Order Month'] = cleaned['Order Date'].dt.to_period('M').astype(str)
    cleaned['Order Year'] = cleaned['Order Date'].dt.year.astype(int)
    cleaned['Sales Margin'] = ((cleaned['Profit'] / cleaned['Sales']) * 100).fillna(0)
    cleaned['Revenue'] = cleaned['Sales']

    cleaned = cleaned.reset_index(drop=True)
    return cleaned


def load_sales_data_to_mysql(df: pd.DataFrame, host: str = 'localhost', user: str = 'root', password: str = '', database: str = 'retail_business') -> None:
    if password == '':
        password = ''

    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, autocommit=True)
    cursor = connection.cursor()

    cursor.execute(
        f"""
        CREATE DATABASE IF NOT EXISTS `{database}`
        """
    )
    cursor.execute(f"USE `{database}`")
    cursor.execute(
        """
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
        )
        """
    )

    cursor.execute("DELETE FROM retail_sales")
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO retail_sales (
                order_id, order_date, product, category, region, customer, sales, profit, quantity, order_month, order_year, sales_margin, revenue
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row['Order ID'],
                row['Order Date'].date().strftime('%Y-%m-%d'),
                row['Product'],
                row['Category'],
                row['Region'],
                row['Customer'],
                float(row['Sales']),
                float(row['Profit']),
                int(row['Quantity']),
                row['Order Month'],
                int(row['Order Year']),
                float(row['Sales Margin']),
                float(row['Revenue']),
            ),
        )

    cursor.close()
    connection.close()


def create_sample_dataset(output_path: Optional[str] = None) -> str:
    data_dir = Path(output_path) if output_path else Path(__file__).resolve().parents[1] / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    output_file = data_dir / 'retail_sales.csv'

    if output_file.exists():
        return str(output_file)

    import numpy as np

    rng = np.random.default_rng(42)
    dates = pd.date_range('2024-01-01', periods=120, freq='D')
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Tablet', 'Headphones', 'Webcam', 'Printer']
    categories = ['Electronics', 'Accessories', 'Office Supplies']
    regions = ['North', 'South', 'East', 'West']
    customers = ['Asha', 'Bharat', 'Chandra', 'Disha', 'Ethan', 'Farah', 'Gaurav']

    rows = []
    for i in range(120):
        date = dates[i]
        product = products[i % len(products)]
        category = categories[(i + 1) % len(categories)]
        region = regions[i % len(regions)]
        customer = customers[i % len(customers)]
        quantity = int(rng.integers(1, 5))
        unit_price = float(rng.integers(50, 250))
        sales = round(quantity * unit_price, 2)
        profit = round(sales * (0.2 + rng.random() * 0.15), 2)
        rows.append({
            'Order ID': f'ORD-{i + 1:03d}',
            'Date': date.strftime('%Y-%m-%d'),
            'Product': product,
            'Category': category,
            'Region': region,
            'Customer': customer,
            'Sales': sales,
            'Profit': profit,
            'Quantity': quantity,
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)
    return str(output_file)


def load_csv_to_dataframe(input_path: str) -> pd.DataFrame:
    return pd.read_csv(input_path)
