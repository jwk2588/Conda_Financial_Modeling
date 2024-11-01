import os
import pandas as pd
from scripts.data_ingestion.data_retrieval import get_financial_data
from scripts.data_preprocessing.data_transformation import transform_financial_data
from scripts.models.financial_forecast import generate_forecast
from scripts.models.depreciation_schedule import generate_depreciation_schedule

def integrate_to_excel(ticker_symbol, financial_data, forecast_data, depreciation_data, output_dir="."):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, f'{ticker_symbol}_financial_model.xlsx')
    
    with pd.ExcelWriter(output_path) as writer:
        financial_data['income_statement'].to_excel(writer, sheet_name='Income Statement', index=False)
        financial_data['balance_sheet'].to_excel(writer, sheet_name='Balance Sheet', index=False)
        financial_data['cash_flow'].to_excel(writer, sheet_name='Cash Flow Statement', index=False)
        
        forecast_data['income_statement'].to_excel(writer, sheet_name='Forecast Income Statement', index=False)
        forecast_data['balance_sheet'].to_excel(writer, sheet_name='Forecast Balance Sheet', index=False)
        forecast_data['cash_flow'].to_excel(writer, sheet_name='Forecast Cash Flow', index=False)
        
        depreciation_data.to_excel(writer, sheet_name='Depreciation Schedule', index=False)

    print(f'{output_path} has been created successfully.')

# Run Integration
if __name__ == "__main__":
    ticker_symbol = 'GM'
    financial_data = get_financial_data(ticker_symbol)
    transformed_financial_data = transform_financial_data(financial_data)
    forecast_data = generate_forecast(transformed_financial_data, forecast_years=3)
    initial_capex = 1000000
    useful_life = 5
    depreciation_data = generate_depreciation_schedule(initial_capex, useful_life)

    output_directory = "./financial_models"
    integrate_to_excel(ticker_symbol, transformed_financial_data, forecast_data, depreciation_data, output_dir=output_directory)
