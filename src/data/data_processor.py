#!/usr/bin/env python
"""
Module: data_processor.py

This module processes historical stock data by computing daily returns and
aggregating them to form a correlation matrix. It reads raw CSV files (generated
by data_loader.py) containing stock data with a nonstandard header.
"""

import os
from typing import Dict, List, Optional

import pandas as pd
from tqdm import tqdm

from src.utils.setup_logger import setup_logger

# Configure module-level logger
logger = setup_logger(__name__, add_console=False)


def compute_daily_returns(df: pd.DataFrame) -> pd.Series:
    """
    Compute the daily returns from the 'Close' column.

    Args:
        df (pd.DataFrame): DataFrame containing historical stock data with a 'Close' column.

    Returns:
        pd.Series: Daily returns computed as percentage changes.

    Raises:
        ValueError: If the 'Close' column is missing.
    """
    if "Close" not in df.columns:
        logger.error("DataFrame does not contain 'Close' column. Columns found: %s", df.columns.tolist())
        raise ValueError("DataFrame must include a 'Close' column.")
    returns = df["Close"].pct_change().dropna()
    logger.debug("Computed daily returns.")
    return returns


def load_stock_data(ticker: str, input_dir: str) -> Optional[pd.DataFrame]:
    """
    Load historical stock data from a CSV file with a nonstandard header format.

    The CSV file is expected to have:
      - Row 0: Column names for numeric data (e.g., "Price,Close,High,Low,Open,Volume")
      - Row 1: Ticker information (to be skipped)
      - Row 2: Provides the label for the first column ("Date")
      - Row 3 onward: Data rows

    The function skips the first two rows, then assigns the header:
        ["Date", "Close", "High", "Low", "Open", "Volume"]
    and parses the "Date" column as datetime and sets it as the index.

    Args:
        ticker (str): Stock ticker symbol.
        input_dir (str): Directory containing raw CSV files.

    Returns:
        Optional[pd.DataFrame]: Processed DataFrame if successful; otherwise, None.
    """
    file_path = os.path.join(input_dir, f"{ticker}.csv")
    if not os.path.exists(file_path):
        logger.error("CSV file for %s not found at %s", ticker, file_path)
        return None
    try:
        df = pd.read_csv(file_path, header=None, skiprows=2)
        new_columns = ["Date", "Close", "High", "Low", "Open", "Volume"]
        df.columns = new_columns
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
        df.set_index("Date", inplace=True)
        logger.info("Loaded data for %s with %d rows.", ticker, len(df))
        return df
    except Exception as e:
        logger.exception("Failed to load data for %s: %s", ticker, e)
        return None


def aggregate_daily_returns(tickers: List[str], input_dir: str) -> pd.DataFrame:
    """
    Aggregate daily returns for a list of tickers into a single DataFrame.

    Args:
        tickers (List[str]): List of ticker symbols.
        input_dir (str): Directory containing raw CSV files.

    Returns:
        pd.DataFrame: A DataFrame where each column represents the daily returns for a ticker.

    Raises:
        ValueError: If no valid return series can be aggregated.
    """
    returns_dict: Dict[str, pd.Series] = {}
    failed_tickers, total_tickers = 0, len(tickers)
    for ticker in tqdm(tickers, desc="Processing raw data for tickers"):
        df = load_stock_data(ticker, input_dir)
        if df is not None:
            try:
                returns = compute_daily_returns(df)
                returns_dict[ticker] = returns
            except Exception as e:
                logger.error("Skipping %s due to error: %s", ticker, e)
    if not returns_dict:
        logger.error("No valid return data available for aggregation.")
        raise ValueError("No valid return data found.")
    else:
        logger.info(f"Successfully processed data for {total_tickers - failed_tickers}/{total_tickers} tickers")

    returns_df = pd.DataFrame(returns_dict)
    returns_df.dropna(inplace=True)
    logger.info("Aggregated daily returns DataFrame shape: %s", returns_df.shape)
    return returns_df


def compute_correlation_matrix(returns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the correlation matrix from aggregated daily returns.

    Args:
        returns_df (pd.DataFrame): DataFrame containing daily returns.

    Returns:
        pd.DataFrame: Correlation matrix of the daily returns.
    """
    corr_matrix = returns_df.corr()
    logger.info("Correlation matrix computed successfully.")
    return corr_matrix


def save_dataframe_to_csv(df: pd.DataFrame, output_file: str) -> None:
    """
    Save a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to be saved.
        output_file (str): Path (including filename) where the CSV will be stored.
    """
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file)
        logger.info("DataFrame saved to %s", os.path.basename(output_file))
    except Exception as e:
        logger.exception("Error saving DataFrame to %s: %s", output_file, e)
