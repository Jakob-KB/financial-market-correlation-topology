#!/usr/bin/env python
"""
Module: data_processor.py

This module processes historical stock data by computing daily returns and
aggregating them to form a correlation matrix. It reads raw CSV files (generated
by data_loader.py) containing stock data with a nonstandard header.
"""

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from tqdm import tqdm

from config import DIRECTORY_CONFIG
from src.utils.setup_logger import setup_logger

# Configure module-level logger
logger = setup_logger(__name__)


def compute_daily_returns(df: pd.DataFrame) -> pd.Series:
    """
    Compute daily returns from the 'Close' column.

    Args:
        df (pd.DataFrame): DataFrame containing historical stock data with a 'Close' column.

    Returns:
        pd.Series: Daily returns, computed as percentage changes.

    Raises:
        ValueError: If the 'Close' column is missing.
    """
    if "Close" not in df.columns:
        logger.error("DataFrame is missing 'Close' column. Found columns: %s", df.columns.tolist())
        raise ValueError("DataFrame must include a 'Close' column.")

    returns = df["Close"].pct_change().dropna()
    logger.debug("Computed daily returns (%d entries).", len(returns))
    return returns


def load_stock_data(
    ticker: str,
    input_dir: Path = DIRECTORY_CONFIG.RAW_DATA_DIR
) -> Optional[pd.DataFrame]:
    """
    Load historical stock data from a CSV file with a nonstandard header format.

    The CSV is expected to have:
      - Row 0: Column names for numeric data (e.g., 'Price,Close,High,Low,Open,Volume')
      - Row 1: Ticker info (skipped)
      - Row 2: The label for the first column ('Date')
      - Row 3 onward: Data rows

    The function skips the first two rows, then assigns:
        ["Date", "Close", "High", "Low", "Open", "Volume"]
    and parses the "Date" column as a datetime index.

    Args:
        ticker (str): Stock ticker symbol.
        input_dir (Path): Directory containing raw CSV files.

    Returns:
        Optional[pd.DataFrame]: Processed DataFrame, or None if file not found or load fails.
    """
    file_path = input_dir / f"{ticker}.csv"
    if not file_path.exists():
        logger.error("CSV file for %s not found at %s", ticker, file_path)
        return None

    try:
        df = pd.read_csv(file_path, header=None, skiprows=2)
        df.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
        df.set_index("Date", inplace=True)

        logger.info("Loaded %d rows for %s.", len(df), ticker)
        return df
    except Exception as e:
        logger.exception("Failed to load data for %s: %s", ticker, e)
        return None


def aggregate_daily_returns(
    tickers: List[str],
    input_dir: Path = DIRECTORY_CONFIG.RAW_DATA_DIR
) -> pd.DataFrame:
    """
    Aggregate daily returns for multiple tickers into a single DataFrame.

    Args:
        tickers (List[str]): List of ticker symbols.
        input_dir (Path): Directory containing raw CSV files.

    Returns:
        pd.DataFrame: DataFrame where each column represents daily returns for a ticker.

    Raises:
        ValueError: If no valid return series are found.
    """
    returns_dict: Dict[str, pd.Series] = {}
    failed_tickers = 0

    for ticker in tqdm(tickers, desc="Processing raw CSV data"):
        df = load_stock_data(ticker, input_dir)
        if df is not None:
            try:
                daily_returns = compute_daily_returns(df)
                returns_dict[ticker] = daily_returns
                logger.debug("Added returns for %s (%d entries).", ticker, len(daily_returns))
            except Exception as e:
                logger.error("Skipping %s due to error: %s", ticker, e)
                failed_tickers += 1

    if not returns_dict:
        logger.error("No valid return data to aggregate.")
        raise ValueError("No valid return data found.")

    returns_df = pd.DataFrame(returns_dict).dropna()
    logger.info("Processed %d/%d tickers successfully.", len(returns_dict), len(tickers))
    logger.info("Aggregated daily returns shape: %s", returns_df.shape)
    return returns_df


def compute_correlation_matrix(returns_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the correlation matrix from aggregated daily returns.

    Args:
        returns_df (pd.DataFrame): DataFrame containing daily returns.

    Returns:
        pd.DataFrame: Correlation matrix of daily returns.
    """
    corr_matrix = returns_df.corr()
    logger.info("Computed correlation matrix with shape %s.", corr_matrix.shape)
    return corr_matrix


def save_dataframe_to_csv(
    df: pd.DataFrame,
    file_name: str,
    output_dir: Path = DIRECTORY_CONFIG.PROCESSED_DATA_DIR
) -> None:
    """
    Save a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to be saved.
        file_name (str): Output CSV filename.
        output_dir (Path): Directory where CSV will be stored.

    Returns:
        None
    """
    output_file = output_dir / file_name
    try:
        df.to_csv(output_file)
        logger.info("Saved DataFrame to %s", output_file)
    except Exception as e:
        logger.exception("Error saving DataFrame to %s: %s", output_file, e)
