# scripts/generate_scripts.py

import os
import pandas as pd
from scripts.utilities.data_transformation_utils import (
    get_data_paths,
    archive_files,
    prune_archives,
    logger
)

def load_historical_data():
    """Loads the transformed and tagged financial statements."""
    try:
        _, processed_data_dir = get_data_paths()
        balance_sheet_path = os.path.join(processed_data_dir, 'tagged_balance_sheet.csv')
        income_statement_path = os.path.join(processed_data_dir, 'tagged_income_statement.csv')
        cash_flow_path = os.path.join(processed_data_dir, 'tagged_cash_flow.csv')

        logger.info("Loading processed financial statements...")

        balance_sheet = pd.read_csv(balance_sheet_path, index_col='Category')
        income_statement = pd.read_csv(income_statement_path, index_col='Category')
        cash_flow = pd.read_csv(cash_flow_path, index_col='Category')

        logger.info("Financial statements loaded successfully.")
        return balance_sheet, income_statement, cash_flow
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except Exception as e:
        logger.error(f"An error occurred while loading data: {e}")
        raise

def combine_statements(balance_sheet, income_statement, cash_flow):
    """Combines the financial statements into a single DataFrame."""
    try:
        balance_sheet['Statement Type'] = 'Balance Sheet'
        income_statement['Statement Type'] = 'Income Statement'
        cash_flow['Statement Type'] = 'Cash Flow Statement'

        balance_sheet.reset_index(inplace=True)
        income_statement.reset_index(inplace=True)
        cash_flow.reset_index(inplace=True)

        balance_sheet_melted = balance_sheet.melt(
            id_vars=['Category', 'Statement Type'],
            var_name='Period',
            value_name='Amount'
        )
        income_statement_melted = income_statement.melt(
            id_vars=['Category', 'Statement Type'],
            var_name='Period',
            value_name='Amount'
        )
        cash_flow_melted = cash_flow.melt(
            id_vars=['Category', 'Statement Type'],
            var_name='Period',
            value_name='Amount'
        )

        combined_df = pd.concat(
            [balance_sheet_melted, income_statement_melted, cash_flow_melted],
            ignore_index=True
        )

        logger.info("Financial statements combined successfully.")
        return combined_df
    except Exception as e:
        logger.error(f"An error occurred while combining statements: {e}")
        raise

def calculate_baseline(dataframe):
    """Calculates baseline values for selected line items."""
    logger.info("Calculating baseline values for selected line items...")
    try:
        selected_line_items = {
            'Income Statement': [
                'Revenue', 'Cost of Goods Sold', 'Gross Profit',
                'Operating Expenses', 'Operating Income', 'Net Income'
            ],
            'Cash Flow Statement': [
                'Net Cash Provided by Operating Activities',
                'Net Cash Used in Investing Activities',
                'Net Cash Used in Financing Activities',
                'Free Cash Flow'
            ],
            'Balance Sheet': [
                'Total Assets', 'Total Liabilities', 'Total Equity',
                'Cash and Cash Equivalents', 'Accounts Receivable',
                'Inventory', 'Accounts Payable',
                'Allowance for Doubtful Accounts',
                'Deferred Tax Assets', 'Deferred Tax Liabilities'
            ]
        }

        dataframe['Amount'] = pd.to_numeric(dataframe['Amount'], errors='coerce')
        dataframe = dataframe.dropna(subset=['Amount'])

        baseline_list = []

        for statement_type, line_items in selected_line_items.items():
            df_statement = dataframe[dataframe['Statement Type'] == statement_type]
            df_selected = df_statement[df_statement['Category'].isin(line_items)]

            if statement_type in ['Income Statement', 'Cash Flow Statement']:
                baseline = df_selected.groupby(['Category'])['Amount'].mean().reset_index()
            elif statement_type == 'Balance Sheet':
                latest_period = df_selected['Period'].max()
                baseline = df_selected[df_selected['Period'] == latest_period][['Category', 'Amount']]
            else:
                continue

            baseline['Statement Type'] = statement_type
            baseline_list.append(baseline)

        baseline_combined = pd.concat(baseline_list, ignore_index=True)
        baseline_combined = baseline_combined[['Category', 'Statement Type', 'Amount']]

        logger.info(f"Baseline calculated successfully:\n{baseline_combined.head()}")
        return baseline_combined
    except Exception as e:
        logger.error(f"Error while calculating baseline: {e}")
        raise

def save_baseline_to_csv(baseline, output_path):
    """Saves the baseline values to a CSV file."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        baseline.to_csv(output_path, index=False)
        logger.info(f"Baseline saved to {output_path}")
    except Exception as e:
        logger.error(f"Error while saving baseline: {e}")
        raise

def main():
    try:
        _, processed_data_dir = get_data_paths()
        archive_dir = os.path.join(processed_data_dir, 'archive')

        # Load the transformed and tagged financial statements before archiving
        balance_sheet, income_statement, cash_flow = load_historical_data()

        # Archive old files after loading
        archive_files(processed_data_dir, archive_dir)

        # Combine the statements
        combined_df = combine_statements(balance_sheet, income_statement, cash_flow)
        combined_filepath = os.path.join(processed_data_dir, 'combined_statements.csv')
        combined_df.to_csv(combined_filepath, index=False)
        logger.info(f"Combined statements saved to {combined_filepath}")

        # Calculate the baseline
        baseline_values = calculate_baseline(combined_df)
        baseline_filepath = os.path.join(processed_data_dir, 'baseline_values.csv')
        save_baseline_to_csv(baseline_values, baseline_filepath)

        # Prune archives
        prune_archives(archive_dir, retention_days=30, max_versions=5)

    except Exception as e:
        logger.error(f"An error occurred in the script: {e}")
        raise

if __name__ == "__main__":
    main()
