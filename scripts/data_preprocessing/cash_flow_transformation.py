# scripts/data_preprocessing/cash_flow_transformation.py

from scripts.data_preprocessing.financial_statement_transformer import CashFlowTransformer

if __name__ == "__main__":
    transformer = CashFlowTransformer()
    transformer.transform()
