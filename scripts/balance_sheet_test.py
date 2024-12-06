# Standalone testing script (balance_sheet_test.py)

from scripts.data_preprocessing.financial_statement_transformer import FinancialStatementTransformer

# Initialize transformer with testing mode
transformer = FinancialStatementTransformer("balance_sheet")

# Load, transform, and display data without saving files
transformer.load_data()
transformer.transform_data()
print("Transformed Data:")
print(transformer.df)
