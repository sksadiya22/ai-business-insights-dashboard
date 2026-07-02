from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / 'python'))
from retail_data_pipeline import clean_sales_data, create_sample_dataset, load_csv_to_dataframe, load_sales_data_to_mysql


def main() -> None:
    csv_path = create_sample_dataset()
    df = load_csv_to_dataframe(csv_path)
    cleaned = clean_sales_data(df)
    try:
        load_sales_data_to_mysql(cleaned)
        print('Loaded cleaned data into MySQL successfully.')
    except Exception as exc:
        print(f'MySQL load skipped: {exc}')


if __name__ == '__main__':
    main()
