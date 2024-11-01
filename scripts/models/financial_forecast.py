import pandas as pd

def generate_forecast(financial_data, forecast_years=3):
    forecast = {}
    for key, df in financial_data.items():
        # Calculate mean values of each column to use for forecasts
        forecast_values = df.mean(axis=0)
        # Repeat the forecast values for the given number of forecast years
        forecast[key] = pd.DataFrame([forecast_values] * forecast_years)
        forecast[key].columns = df.columns  # Ensure forecast DataFrame has the same columns as the original
    return forecast
