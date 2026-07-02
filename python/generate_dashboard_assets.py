from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / 'python'))
from retail_data_pipeline import create_sample_dataset, clean_sales_data, load_csv_to_dataframe, load_sales_data_to_mysql


def main() -> None:
    csv_path = create_sample_dataset()
    df = load_csv_to_dataframe(csv_path)
    cleaned = clean_sales_data(df)
    cleaned.to_csv(Path(__file__).resolve().parents[1] / 'data' / 'cleaned_retail_sales.csv', index=False)
    print('Generated sample dataset and cleaned CSV.')


if __name__ == '__main__':
    main()
