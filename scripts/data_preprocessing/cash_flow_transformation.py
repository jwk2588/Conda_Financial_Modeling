# scripts/data_preprocessing/cash_flow_transformation.py

from scripts.data_preprocessing.financial_statement_transformer import FinancialStatementTransformer

class CashFlowTransformer(FinancialStatementTransformer):
    def __init__(self):
        super().__init__('cash_flow')

if __name__ == "__main__":
    transformer = CashFlowTransformer()
    transformer.transform()
