import os
import logging
import pandas as pd
from fuzzywuzzy import process
from datetime import datetime
from scripts.utilities.data_transformation_utils import (
    configure_logging,
    get_data_paths,
    tag_line_item_indices,
    line_item_dict,
)

# Configure logging
def configure_logging():
    logger = logging.getLogger("FinancialModeling")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = configure_logging()

def get_data_paths():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    data_dir = os.path.join(project_root, "data")
    raw_data_dir = os.path.join(data_dir, "raw")
    processed_data_dir = os.path.join(data_dir, "processed")
    return raw_data_dir, processed_data_dir

def disable_scientific_notation():
    pd.options.display.float_format = "{:,.0f}".format

# Full expanded line item dictionary for fuzzy matching
line_item_dict = {
    "Revenue": ["Revenue", "Total Revenue", "Net Revenue", "Sales"],
    "Cost of Goods Sold": ["Cost of Goods Sold", "COGS", "Cost of Sales", "Cost of Revenue"],
    "Gross Profit": ["Gross Profit", "Gross Income", "Gross Margin"],
    "Operating Expenses": ["Operating Expenses", "OPEX", "Total Operating Expenses"],
    "Operating Income": ["Operating Income", "Operating Profit", "EBIT"],
    "Net Income": ["Net Income", "Net Profit", "Income After Tax", "Earnings"],
    "Research and Development": ["Research and Development", "R&D Expenses", "Research & Development"],
    "Selling General and Administrative": [
        "Selling General and Administrative",
        "SG&A",
        "Selling, General & Administrative",
    ],
    "Interest Expense": ["Interest Expense", "Finance Costs", "Interest and Other Expenses"],
    "Income Tax Expense": ["Income Tax Expense", "Taxes", "Provision for Income Taxes"],
    "Other Income/Expense": ["Other Income/Expense", "Other Income", "Other Expense"],
    "Total Operating Income": ["Total Operating Income", "Income from Operations"],
    "Total Assets": ["Total Assets", "Assets"],
    "Total Liabilities": ["Total Liabilities", "Liabilities"],
    "Total Equity": ["Total Equity", "Shareholders' Equity", "Stockholders' Equity"],
    "Cash and Cash Equivalents": ["Cash and Cash Equivalents", "Cash", "Cash Equivalents"],
    "Short-Term Investments": ["Short-Term Investments", "Marketable Securities"],
    "Accounts Receivable": ["Accounts Receivable", "Receivables", "Trade Receivables"],
    "Inventory": ["Inventory", "Inventories"],
    "Other Current Assets": ["Other Current Assets", "Prepaid Expenses"],
    "Long-Term Investments": ["Long-Term Investments", "Non-Current Investments"],
    "Property Plant and Equipment": ["Property, Plant & Equipment", "PP&E", "Fixed Assets"],
    "Goodwill": ["Goodwill"],
    "Intangible Assets": ["Intangible Assets", "Intangibles"],
    "Other Assets": ["Other Assets", "Miscellaneous Assets"],
    "Accounts Payable": ["Accounts Payable", "Payables", "Trade Payables"],
    "Short-Term Debt": ["Short-Term Debt", "Current Portion of Long-Term Debt"],
    "Other Current Liabilities": ["Other Current Liabilities", "Accrued Liabilities"],
    "Long-Term Debt": ["Long-Term Debt", "Non-Current Debt"],
    "Deferred Tax Liabilities": ["Deferred Tax Liabilities", "DTL"],
    "Deferred Tax Assets": ["Deferred Tax Assets", "DTA"],
    "Other Liabilities": ["Other Liabilities", "Miscellaneous Liabilities"],
    "Common Stock": ["Common Stock", "Ordinary Shares"],
    "Retained Earnings": ["Retained Earnings", "Accumulated Earnings"],
    "Accumulated Other Comprehensive Income": [
        "Accumulated Other Comprehensive Income",
        "AOCI",
    ],
    "Treasury Stock": ["Treasury Stock", "Treasury Shares"],
    "Allowance for Doubtful Accounts": [
        "Allowance for Doubtful Accounts",
        "Bad Debt Allowance",
        "Provision for Credit Losses",
    ],
    "Net Cash Provided by Operating Activities": [
        "Net Cash Provided by Operating Activities",
        "Cash from Operating Activities",
        "Operating Cash Flow",
        "Net Cash from Operating Activities",
    ],
    "Net Cash Used in Investing Activities": [
        "Net Cash Used in Investing Activities",
        "Cash from Investing Activities",
        "Investing Cash Flow",
        "Net Cash from Investing Activities",
    ],
    "Net Cash Provided by Financing Activities": [
        "Net Cash Provided by Financing Activities",
        "Cash from Financing Activities",
        "Financing Cash Flow",
        "Net Cash from Financing Activities",
    ],
    "Net Change in Cash": ["Net Change in Cash", "Change in Cash and Cash Equivalents"],
    "Capital Expenditure": ["Capital Expenditure", "CapEx", "Purchases of Property, Plant & Equipment"],
    "Depreciation and Amortization": ["Depreciation & Amortization", "D&A", "Depreciation", "Amortization"],
    "Free Cash Flow": ["Free Cash Flow", "FCF"],
    "Dividends Paid": ["Dividends Paid", "Dividends"],
    "Stock Based Compensation": ["Stock-Based Compensation", "Share-Based Compensation"],
    "Change in Working Capital": ["Change in Working Capital", "Working Capital Changes"],
    "Other Non-Cash Items": ["Other Non-Cash Items", "Non-Cash Adjustments"],
    # Add more as needed
}

def tag_line_item_indices(dataframe, dictionary):
    """Apply mapping to line items using fuzzy matching."""
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    def map_item(item):
        
        if not isinstance(item, str):
            return item
        # Find the best match from the dictionary
        matches = [(key, process.extractOne(item, dictionary[key])) for key in dictionary]
        best_match, (best_item, score) = max(matches, key=lambda x: x[1][1])
        return best_match if score >= 80 else item  # Threshold is 80

    # Check for the "Category" column
    if "Category" in dataframe.columns:
        dataframe["Category"] = dataframe["Category"].apply(map_item)
    else:
        raise KeyError("Column 'Category' not found in the DataFrame.")
    return dataframe