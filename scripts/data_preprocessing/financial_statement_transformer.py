import os
import pandas as pd
from scripts.utilities.data_transformation_utils import (
    get_data_paths,
    tag_line_item_indices,
    line_item_dict,
    logger
)

class FinancialStatementTransformer:
    """Base class for transforming financial statements with validation and testing entry points."""

    def __init__(self, statement_type: str):
        self.statement_type = statement_type  # e.g., 'balance_sheet', 'income_statement', or 'cash_flow'
        self.raw_file, self.processed_file, self.tagged_file = self.get_file_paths()
        self.df = None  # Placeholder for the loaded DataFrame

    def get_file_paths(self):
        """Constructs file paths for raw, processed, and tagged files."""
        raw_dir, processed_dir = get_data_paths()
        raw_file = os.path.join(raw_dir, f'{self.statement_type}.csv')
        processed_file = os.path.join(processed_dir, f'processed_{self.statement_type}.csv')
        tagged_file = os.path.join(processed_dir, f'tagged_{self.statement_type}.csv')
        return raw_file, processed_file, tagged_file

    def load_data(self):
        """Loads raw financial statement data."""
        if not os.path.exists(self.raw_file):
            raise FileNotFoundError(f"Raw file not found: {self.raw_file}")
        self.df = pd.read_csv(self.raw_file)
        logger.info(f"Loaded {self.statement_type} data:\n{self.df.head()}")

    def validate_data(self):
        """
        Validates the raw data to ensure it can proceed with transformations.
        Example checks: non-empty DataFrame, numeric values, and appropriate structure.
        """
        if self.df is None or self.df.empty:
            raise ValueError(f"The raw data for {self.statement_type} is empty. Please check the source file.")

        # Example validation: Ensure the first column exists
        first_column_name = self.df.columns[0]
        if first_column_name == '':
            raise ValueError(f"The first column in the {self.statement_type} data is unnamed or blank.")

        # Example validation: Ensure at least one numeric column exists
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        if numeric_cols.empty:
            raise ValueError(f"No numeric columns found in {self.statement_type} data for calculations.")

        logger.info(f"{self.statement_type} data passed validation checks.")

    def transform_data(self):
        """Applies necessary transformations to the financial statement."""
        try:
            self.validate_data()

            # Step 1: Reset index if any
            if self.df.index.name:
                self.df.reset_index(inplace=True)

            # Step 2: Set the first column as 'Category' if it's unnamed
            if 'Unnamed: 0' in self.df.columns:
                self.df.rename(columns={'Unnamed: 0': 'Category'}, inplace=True)
            elif self.df.columns[0] != 'Category':
                self.df.rename(columns={self.df.columns[0]: 'Category'}, inplace=True)

            # Step 3: Sort columns (dates) in chronological order
            date_columns = [col for col in self.df.columns if col != 'Category']
            date_columns = sorted(date_columns, reverse=True)  # Sort dates in descending order
            column_order = ['Category'] + date_columns
            self.df = self.df[column_order]

            # Step 4: Remove any rows where Category is NaN or empty
            self.df = self.df[self.df['Category'].notna()]
            self.df = self.df[self.df['Category'] != '']

            # Step 5: Apply statement-specific transformations
            if self.statement_type == 'income_statement':
                # For income statement, keep natural order (Revenue at top, Net Income at bottom)
                self.df = self.df.iloc[::-1]
            elif self.statement_type == 'cash_flow':
                # For cash flow, maintain operating/investing/financing sections
                self.df = self.df.iloc[::-1]
            elif self.statement_type == 'balance_sheet':
                # For balance sheet, maintain Assets -> Liabilities -> Equity order
                self.df = self.df.iloc[::-1]  # Reverse to get Assets at top

            # Step 6: Replace any NaN values with empty string
            self.df = self.df.fillna('')

            logger.info(f"Transformed {self.statement_type} data:\n{self.df.head()}")

        except Exception as e:
            logger.error(f"Error during transformation of {self.statement_type}: {e}")
            raise

    def tag_data(self):
        """Tags line items using the predefined dictionary."""
        if 'LineItem' not in self.df.columns:
            logger.warning(f"Column 'LineItem' not found in {self.statement_type} data.")
            return
        self.df = tag_line_item_indices(self.df, line_item_dict)
        logger.info(f"Tagged {self.statement_type} data:\n{self.df.head()}")

    def save_data(self, filename: str, data: pd.DataFrame):
        """Saves DataFrame to a specified file."""
        _, processed_dir = get_data_paths()
        output_path = os.path.join(processed_dir, filename)
        data.to_csv(output_path, index=False)
        logger.info(f"Saved data to {output_path}")

    def transform(self):
        """
        Executes the full transformation pipeline.
        Can be stopped or rerun from specific steps during testing.
        """
        try:
            self.load_data()
            self.transform_data()

            # Save intermediate data for inspection
            self.save_data(f'processed_{self.statement_type}.csv', self.df)

            # Tag and save tagged data
            self.tag_data()
            self.save_data(f'tagged_{self.statement_type}.csv', self.df)

        except Exception as e:
            logger.error(f"Error transforming {self.statement_type}: {e}")

# Child classes for specific financial statements
class BalanceSheetTransformer(FinancialStatementTransformer):
    def __init__(self):
        super().__init__('balance_sheet')

class IncomeStatementTransformer(FinancialStatementTransformer):
    def __init__(self):
        super().__init__('income_statement')

class CashFlowTransformer(FinancialStatementTransformer):
    def __init__(self):
        super().__init__('cash_flow')

if __name__ == "__main__":
    # Entry points for testing transformations
    logger.info("Starting transformations for selected statements...")
    for Transformer in [BalanceSheetTransformer, IncomeStatementTransformer, CashFlowTransformer]:
        transformer = Transformer()
        transformer.transform()
