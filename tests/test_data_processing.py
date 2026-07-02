import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / 'python'))

from retail_data_pipeline import clean_sales_data


def test_clean_sales_data_removes_nulls_and_duplicates():
    df = pd.DataFrame(
        {
            'Order ID': ['A1', 'A1', 'A2', 'A3'],
            'Date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-03'],
            'Product': ['Laptop', 'Laptop', 'Mouse', 'Keyboard'],
            'Category': ['Electronics', 'Electronics', 'Accessories', 'Accessories'],
            'Region': ['North', 'North', 'South', 'West'],
            'Customer': ['Ana', 'Ana', 'Ben', 'Cara'],
            'Sales': [1000.0, 1000.0, 25.0, 80.0],
            'Profit': [200.0, 200.0, 5.0, 20.0],
            'Quantity': [1, 1, 2, 1],
        }
    )

    cleaned = clean_sales_data(df)

    assert cleaned['Sales'].dtype.kind in 'ifc'
    assert cleaned['Profit'].dtype.kind in 'ifc'
    assert cleaned['Quantity'].dtype.kind in 'ifc'
    assert cleaned['Order Date'].dtype == 'datetime64[ns]'
    assert cleaned.shape[0] == 3
    assert cleaned['Order ID'].is_unique
