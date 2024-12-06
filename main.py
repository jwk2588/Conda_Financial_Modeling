import os
import sys
import logging
from scripts.data_ingestion.data_retrieval import main as data_retrieval_main
from scripts.data_preprocessing.balance_sheet_transformation import BalanceSheetTransformer
from scripts.data_preprocessing.income_statement_transformation import IncomeStatementTransformer
from scripts.data_preprocessing.cash_flow_transformation import CashFlowTransformer
from scripts.generate_scripts import main as generate_scripts_main
from scripts.utilities.data_transformation_utils import (
    configure_logging,
    get_data_paths,
    archive_files,
    prune_archives,
)

# Configure logging
logger = configure_logging()

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

    # Archive old files
    archive_files(raw_data_dir, raw_archive_dir)
    archive_files(processed_data_dir, processed_archive_dir)

    # Prune old files
    prune_archives(raw_archive_dir)
    prune_archives(processed_archive_dir)

def run_data_ingestion():
    """Run the data ingestion process."""
    logger.info("Starting data ingestion...")
    data_retrieval_main()
    logger.info("Data ingestion completed.")

def run_data_preprocessing():
    """Run the data preprocessing for each financial statement."""
    logger.info("Starting data preprocessing...")
    BalanceSheetTransformer().transform()
    IncomeStatementTransformer().transform()
    CashFlowTransformer().transform()
    logger.info("Data preprocessing completed.")

    # Generate baseline values
    generate_scripts_main()
    logger.info("Baseline values calculated and saved.")

def main():
    """Main execution workflow."""
    try:
        # Validate folder structure and archive old data
        validate_and_archive_folders()

        # Run processes
        run_data_ingestion()
        run_data_preprocessing()

        logger.info("Main workflow completed successfully.")
    except Exception as e:
        logger.exception(f"An error occurred in the main execution: {e}")

if __name__ == "__main__":
    main()
