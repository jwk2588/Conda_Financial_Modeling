from scripts.data_preprocessing.financial_statement_transformer import BalanceSheetTransformer

if __name__ == "__main__":
    transformer = BalanceSheetTransformer()
    transformer.transform()
