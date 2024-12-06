# scripts/data_preprocessing/income_statement_transformation.py

from scripts.data_preprocessing.financial_statement_transformer import FinancialStatementTransformer

class IncomeStatementTransformer(FinancialStatementTransformer):
    def __init__(self):
        super().__init__('income_statement')

if __name__ == "__main__":
    transformer = IncomeStatementTransformer()
    transformer.transform()
