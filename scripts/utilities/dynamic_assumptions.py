import pandas as pd
import os
import logging
from scripts.utilities.data_transformation_utils import get_data_paths, line_item_dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_baselines(tagged_data_dir):
    """
    Calculate baselines for all tagged financial statements.
    """
    baselines = {}

    # Load tagged data
    for file_name in ["tagged_balance_sheet.csv", "tagged_income_statement.csv", "tagged_cash_flow.csv"]:
        file_path = os.path.join(tagged_data_dir, file_name)
        if os.path.exists(file_path):
            logger.info(f"Processing file: {file_name}")
            data = pd.read_csv(file_path, index_col=0)

            # Calculate baselines for numeric columns
            for column in data.columns:
                try:
                    if data[column].dtype in ['float64', 'int64']:
                        baseline_value = data[column].mean()
                        baselines[column] = baseline_value
                except Exception as e:
                    logger.error(f"Error calculating baseline for column {column}: {e}")

    return baselines

def generate_scenarios(baselines, thresholds):
    """
    Generate weak, base, and strong scenarios based on baselines and thresholds.
    """
    scenarios = []
    for metric, baseline_value in baselines.items():
        threshold = thresholds.get(metric, 0.05)  # Default threshold of 5% if not specified
        scenarios.append({
            "Metric": metric,
            "Weak": baseline_value * (1 - threshold),
            "Base": baseline_value,
            "Strong": baseline_value * (1 + threshold)
        })
    return pd.DataFrame(scenarios)

def save_scenarios(scenarios):
    """
    Save generated scenarios to CSV.
    """
    output_file = "./data/outputs/dynamic_scenarios.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    scenarios.to_csv(output_file, index=False)
    logger.info(f"Scenarios saved to {output_file}")

def main():
    """
    Main function to calculate baselines and generate scenarios.
    """
    _, tagged_data_dir = get_data_paths()

    # Step 1: Calculate baselines
    baselines = calculate_baselines(tagged_data_dir)
    logger.info(f"Baselines calculated: {baselines}")

    # Step 2: Generate scenarios
    thresholds = {
        "Revenue Growth Rate": 0.02,
        "COGS % Revenue": 0.05,
        "CapEx Growth Rate": 0.01
    }
    scenarios = generate_scenarios(baselines, thresholds)

    # Step 3: Save scenarios
    save_scenarios(scenarios)

if __name__ == "__main__":
    main()
