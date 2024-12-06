import pandas as pd

# Define paths to tagged files
processed_dir = './data/processed'
files = ['tagged_balance_sheet.csv', 'tagged_income_statement.csv', 'tagged_cash_flow.csv']

# Load and inspect each file
for file in files:
    file_path = f"{processed_dir}/{file}"
    try:
        df = pd.read_csv(file_path)
        print(f"Preview of {file}:")
        print(df.head())
        print("\nColumn Names:", df.columns.tolist())
    except Exception as e:
        print(f"Error loading {file}: {e}")
