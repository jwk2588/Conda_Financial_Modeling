import os
import sys

# Add the project root to the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
if project_root not in sys.path:
    sys.path.append(project_root)

from scripts.data_ingestion.data_retrieval import main as data_retrieval_main
from scripts.data_preprocessing.balance_sheet_transformation import BalanceSheetTransformer
from scripts.data_preprocessing.income_statement_transformation import IncomeStatementTransformer
from scripts.data_preprocessing.cash_flow_transformation import CashFlowTransformer
from scripts.generate_scripts import main as generate_scripts_main
from scripts.utilities.data_transformation_utils import (
    get_data_paths,
    archive_files,
    prune_archives,
    logger
)

def validate_and_archive_folders():
    """Validates the folder structure and archives existing files."""
    raw_data_dir, processed_data_dir = get_data_paths()

    # Define archive folders
    raw_archive_dir = os.path.join(raw_data_dir, 'archive')
    processed_archive_dir = os.path.join(processed_data_dir, 'archive')

    # Ensure directories exist
    for directory in [raw_data_dir, processed_data_dir, raw_archive_dir, processed_archive_dir]:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Validated or created directory: {directory}")

def run_data_ingestion():
    """Runs the data ingestion process."""
    ticker_symbol = 'GM'  # Replace with desired default ticker symbol
    data_retrieval_main(ticker_symbol)

def run_data_preprocessing():
    """Runs the data preprocessing steps."""

    # Process balance sheet data
    balance_sheet_transformer = BalanceSheetTransformer()
    balance_sheet_transformer.transform()

    # Process income statement data
    income_statement_transformer = IncomeStatementTransformer()
    income_statement_transformer.transform()

    # Process cash flow data
    cash_flow_transformer = CashFlowTransformer()
    cash_flow_transformer.transform()

    # Generate baseline values
    generate_scripts_main()

def main():
    """Main function to run the data processing pipeline."""
    try:
        validate_and_archive_folders()

        # Run processes
        run_data_ingestion()
        run_data_preprocessing()

        logger.info("Main workflow completed successfully.")
    except Exception as e:
        logger.exception(f"An error occurred in the main execution: {e}")

if __name__ == "__main__":
    main()