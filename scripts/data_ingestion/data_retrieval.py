import yfinance as yf  # type: ignore
import pandas as pd
import os
from typing import Dict

# Function to retrieve financial data from Yahoo Finance
def get_financial_data_yfinance(ticker_symbol: str) -> Dict[str, pd.DataFrame]:
    try:
        # Create the ticker object
        ticker = yf.Ticker(ticker_symbol)

        # Fetch financial statements for the past 4 years (most recent)
        income_statement = ticker.financials.T.head(4)  # Transposed to get years as rows
        balance_sheet = ticker.balance_sheet.T.head(4)
        cash_flow = ticker.cashflow.T.head(4)

        # Return the financial data as a dictionary of DataFrames
        return {
            'income_statement': income_statement,
            'balance_sheet': balance_sheet,
            'cash_flow': cash_flow
        }
    except Exception as e:
        print(f"An error occurred while fetching data for {ticker_symbol} from Yahoo Finance: {e}")
        return None

# Placeholder function for another data provider (e.g., Alpha Vantage)
def get_financial_data_other(ticker_symbol: str) -> Dict[str, pd.DataFrame]:
    print(f"Fetching data for {ticker_symbol} from another provider...")
    # Implement the other API logic here
    return None

# Function to save the financial data to an Excel file
def save_financial_data_to_excel(financial_data: Dict[str, pd.DataFrame], output_path='./data/financial_statements.xlsx'):
    """
    Saves the financial data to separate sheets in an Excel file.

    Parameters:
    - financial_data (dict): A dictionary containing DataFrames (income_statement, balance_sheet, cash_flow).
    - output_path (str): The path to save the Excel file.
    """
    if financial_data is None:
        print("No financial data available to save.")
        return

    try:
        # Save each DataFrame to a separate sheet in an Excel file
        with pd.ExcelWriter(output_path) as writer:
            for key, df in financial_data.items():
                df.to_excel(writer, sheet_name=key.replace('_', ' ').title(), index=True)
        
        print(f"Financial data saved successfully to {output_path}.")
    except Exception as e:
        print(f"An error occurred while saving financial data: {e}")

# Main block for testing
def main():
    # Define the ticker symbol
    ticker_symbol = input("Enter the ticker symbol (e.g., GM): ")
    
    # Ask user to select the data provider
    provider = input("Select data provider (yfinance/other): ").strip().lower()
    
    # Retrieve financial data based on selected provider
    if provider == 'yfinance':
        financial_data = get_financial_data_yfinance(ticker_symbol)
    elif provider == 'other':
        financial_data = get_financial_data_other(ticker_symbol)
    else:
        print("Invalid provider. Currently, only yfinance or other is supported.")
        return

    # Print the retrieved data (optional)
    if financial_data:
        for key, df in financial_data.items():
            print(f"{key}:\n{df}\n")

    # Save the data to an Excel file with separate sheets
    save_financial_data_to_excel(financial_data)

if __name__ == "__main__":
    main()
