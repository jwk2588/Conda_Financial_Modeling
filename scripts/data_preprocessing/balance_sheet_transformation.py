from scripts.data_preprocessing.financial_statement_transformer import FinancialStatementTransformer

class BalanceSheetTransformer(FinancialStatementTransformer):
    def __init__(self):
        super().__init__("balance_sheet")

if __name__ == "__main__":
    transformer = BalanceSheetTransformer()
    transformer.transform()
