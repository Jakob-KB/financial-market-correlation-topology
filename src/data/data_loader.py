#!/usr/bin/env python
"""
Module: data_loader.py

This module provides functions to download historical stock data using yfinance
and save the results as CSV files. It includes robust error handling, logging,
and a command-line interface to facilitate batch downloads.
"""

from pathlib import Path
from typing import List, Optional

import pandas as pd
import yfinance as yf
from tqdm import tqdm

from config import DATA_CONFIG, DIRECTORY_CONFIG
from src.utils.setup_logger import setup_logger

# Configure module-level logger
logger = setup_logger(__name__)


def download_ticker_data(
        ticker: str,
        start_date: str = DATA_CONFIG.START_DATE,
        end_date: str = DATA_CONFIG.END_DATE,
        interval: str = DATA_CONFIG.INTERVAL
) -> Optional[pd.DataFrame]:
    """
    Download historical stock data for a given ticker using yfinance.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        interval (str): Data interval.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing historical data if successful; otherwise, None.
    """
    try:
        logger.info(f"Downloading {ticker}: {start_date} → {end_date} (Interval: {interval})")
        df = yf.download(ticker, start=start_date, end=end_date, interval=interval, progress=False)

        if df.empty:
            logger.warning(f"No data returned for {ticker}.")
            return None

        logger.info(f"Downloaded {len(df)} rows for {ticker}.")
        return df
    except Exception as e:
        logger.exception(f"Failed to download {ticker}: {e}")
        return None


def save_data_to_csv(df: pd.DataFrame, output_dir: Path, file_name: str) -> None:
    """
    Save a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to be saved.
        output_dir (Path): Directory where the CSV will be saved.
        file_name (str): Name of the CSV file.

    Returns:
        None
    """
    file_path = output_dir / file_name
    try:
        if df.empty:
            logger.warning(f"Skipping save: DataFrame for {file_name} is empty.")
            return

        if df.index.name is None:
            df.index.name = "Date"

        df.to_csv(file_path)
        logger.info(f"Data saved to {file_path}")
    except Exception as e:
        logger.exception(f"Failed to save data to {file_path}: {e}")


def download_and_save_ticker_data(
        ticker: str,
        start_date: str = DATA_CONFIG.START_DATE,
        end_date: str = DATA_CONFIG.END_DATE,
        interval: str = DATA_CONFIG.INTERVAL,
        output_dir: Path = DIRECTORY_CONFIG.RAW_DATA_DIR,
        overwrite: bool = False
) -> bool:
    """
    Download stock data for a single ticker and save it as a CSV file.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        interval (str): Data interval.
        output_dir (Path): Directory where the CSV file will be stored.
        overwrite (bool): If False, will skip download if file already exists.

    Returns:
        bool: True if the data was downloaded and saved successfully; False otherwise.
    """
    file_path = output_dir / f"{ticker}.csv"
    if not overwrite and file_path.exists():
        logger.info(f"Skipping {ticker}: Data already exists at {file_path}.")
        return True

    df = download_ticker_data(ticker, start_date, end_date, interval)
    if df is None:
        logger.error(f"Data for {ticker} could not be downloaded.")
        return False

    save_data_to_csv(df, output_dir, f"{ticker}.csv")
    return True


def download_and_save_multiple_tickers(
        tickers: List[str],
        start_date: str = DATA_CONFIG.START_DATE,
        end_date: str = DATA_CONFIG.END_DATE,
        interval: str = DATA_CONFIG.INTERVAL,
        output_dir: Path = DIRECTORY_CONFIG.RAW_DATA_DIR,
        overwrite: bool = False
) -> None:
    """
    Download and save stock data for multiple tickers.

    Args:
        tickers (List[str]): List of stock ticker symbols.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        interval (str): Data interval.
        output_dir (Path): Directory where CSV files will be stored.
        overwrite (bool): If False, will skip downloading if the file already exists.

    Returns:
        None
    """
    failed_tickers, total_tickers = 0, len(tickers)

    for ticker in tqdm(tickers, desc="Downloading stock data"):
        success = download_and_save_ticker_data(ticker, start_date, end_date, interval, output_dir, overwrite)
        if not success:
            failed_tickers += 1

    logger.info(f"Downloaded data for {total_tickers - failed_tickers}/{total_tickers} tickers.")
