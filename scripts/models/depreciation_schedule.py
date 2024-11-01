import pandas as pd  # Ensure this path is correctly set based on environment configuration
import yfinance as yf
import os

# Import necessary functions from other modules
from scripts.data_retrieval.data_retrieval import get_financial_data
from scripts.data_transformation.data_transformation import transform_financial_data
from scripts.financial_forecast.financial_forecast import generate_forecast

# Step 5: Create a Depreciation Schedule
# This function creates a depreciation schedule using the straight-line method
def create_depreciation_schedule(initial_capex, useful_life, depreciation_method="straight-line"):
    if depreciation_method != "straight-line":
        raise NotImplementedError("Only straight-line depreciation is currently implemented.")

    # Calculate annual depreciation
    annual_depreciation = initial_capex / useful_life
    depreciation_schedule = pd.DataFrame({
        "Year": list(range(1, useful_life + 1)),
        "Depreciation Expense": [annual_depreciation] * useful_life
    })
    return depreciation_schedule

# Step 6: Integrate Depreciation into Excel Output
# Extend the function to include the depreciation schedule in the output
def integrate_to_excel(ticker_symbol, financial_data, forecast_data, depreciation_schedule, output_dir="."):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, f'{ticker_symbol}_financial_model.xlsx')
    
    with pd.ExcelWriter(output_path) as writer:
        # Write the income statement, balance sheet, and cash flow statement to separate sheets
        financial_data['income_statement'].to_excel(writer, sheet_name='Income Statement')
        financial_data['balance_sheet'].to_excel(writer, sheet_name='Balance Sheet')
        financial_data['cash_flow'].to_excel(writer, sheet_name='Cash Flow Statement')
        
        # Write the forecast data to separate sheets
        forecast_data['income_statement'].to_excel(writer, sheet_name='Forecast Income Statement')
        forecast_data['balance_sheet'].to_excel(writer, sheet_name='Forecast Balance Sheet')
        forecast_data['cash_flow'].to_excel(writer, sheet_name='Forecast Cash Flow')

        # Write the depreciation schedule to a separate sheet
        depreciation_schedule.to_excel(writer, sheet_name='Depreciation Schedule')

    print(f'{output_path} has been created successfully.')

# Main Script
if __name__ == "__main__":
    # Define the ticker symbol
    ticker_symbol = 'GM'
    
    # Step 1: Get Financial Data from Yahoo Finance
    financial_data = get_financial_data(ticker_symbol)
    
    # Step 2: Transform Financial Data
    transformed_financial_data = transform_financial_data(financial_data)
    
    # Step 3: Generate Forecast for 3 years
    forecast_data = generate_forecast(transformed_financial_data, forecast_years=3)
    
    # Step 4: Create Depreciation Schedule
    initial_capex = 1000000  # Example CapEx in dollars
    useful_life = 5  # Useful life in years
    depreciation_schedule = create_depreciation_schedule(initial_capex, useful_life)
    
    # Step 5: Export to Excel
    output_directory = "./financial_models"  # Change this to your desired output directory
    integrate_to_excel(ticker_symbol, transformed_financial_data, forecast_data, depreciation_schedule, output_dir=output_directory)
