import pandas as pd

def transform_financial_data(financial_data):
    transformed_data = {}
    for key, df in financial_data.items():
        # Transpose the dataframe to get financial metrics as rows and years as columns
        df = df.T
        # Sort the columns in ascending order to get the years from oldest to most recent
        df = df[df.columns[::-1]]
        # Set the first row as the header and drop the original first row
        df.columns = df.iloc[0]
        df = df[1:]
        transformed_data[key] = df
    return transformed_data

# Test transformation
if __name__ == "__main__":
    # Placeholder example, replace with actual fetched data
    financial_data = {
        "income_statement": pd.DataFrame({'2023': [100, 200], '2022': [150, 180]}),
        "balance_sheet": pd.DataFrame({'2023': [300, 400], '2022': [250, 380]}),
    }
    transformed_data = transform_financial_data(financial_data)
    print(transformed_data['income_statement'])
