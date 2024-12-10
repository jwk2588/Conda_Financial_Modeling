import yfinance as yf
import pandas as pd
import os
from typing import Dict
from scripts.utilities.data_transformation_utils import get_data_paths, logger

def get_financial_data_yfinance(ticker_symbol: str) -> Dict[str, pd.DataFrame]:
    """
    Fetches financial statements for the given ticker symbol using yfinance.

    Args:
        ticker_symbol (str): The ticker symbol of the company (e.g., "GM").

    Returns:
        Dict[str, pd.DataFrame]: A dictionary containing financial statements
        as DataFrames for income statement, balance sheet, and cash flow.
    """
    try:
        logger.info(f"Fetching financial data for ticker: {ticker_symbol}")
        ticker = yf.Ticker(ticker_symbol)

        # Fetch financial statements
        income_statement = ticker.financials
        balance_sheet = ticker.balance_sheet
        cash_flow = ticker.cashflow

        if income_statement.empty or balance_sheet.empty or cash_flow.empty:
            logger.warning(f"No financial data found for ticker: {ticker_symbol}")
            return {}

        logger.info(f"Successfully fetched financial data for {ticker_symbol}")
        return {
            'income_statement': income_statement,
            'balance_sheet': balance_sheet,
            'cash_flow': cash_flow
        }
    except Exception as e:
        logger.error(f"An error occurred while fetching financial data for {ticker_symbol}: {e}")
        return {}

def save_financial_data_to_csv(financial_data: Dict[str, pd.DataFrame]):
    """
    Saves the financial data to separate CSV files in the 'raw' subfolder.

    Args:
        financial_data (Dict[str, pd.DataFrame]): Dictionary of DataFrames to save.
    """
    if not financial_data:
        logger.error("No financial data available to save.")
        return

    try:
        raw_data_dir, _ = get_data_paths()
        raw_data_dir = os.path.abspath(raw_data_dir)
        os.makedirs(raw_data_dir, exist_ok=True)
        logger.info(f"Saving financial data to directory: {raw_data_dir}")

        for statement_type, df in financial_data.items():
            if df.empty:
                logger.warning(f"{statement_type} DataFrame is empty. Skipping save.")
                continue

            csv_path = os.path.join(raw_data_dir, f"{statement_type}.csv")
            df.to_csv(csv_path, index=True)
            logger.info(f"Saved {statement_type} data to {csv_path}")

        logger.info("Financial data saved successfully.")
    except Exception as e:
        logger.error(f"An error occurred while saving financial data: {e}")

def main(ticker_symbol=None):
    """
    Main function to retrieve and save financial data for a given ticker symbol.
    """
    if ticker_symbol is None:
        ticker_symbol = input("Enter the ticker symbol (e.g., GM): ").strip().upper()
    else:
        ticker_symbol = ticker_symbol.strip().upper()

    if not ticker_symbol:
        logger.error("No ticker symbol provided. Exiting.")
        return

    financial_data = get_financial_data_yfinance(ticker_symbol)
    if financial_data:
        save_financial_data_to_csv(financial_data)

if __name__ == "__main__":
    main()
