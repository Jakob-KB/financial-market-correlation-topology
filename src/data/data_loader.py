#!/usr/bin/env python
"""
Module: data_loader.py

This module provides functions to download historical stock data using yfinance
and save the results as CSV files. It includes robust error handling, logging,
and a command-line interface to facilitate batch downloads.
"""

import os
from typing import List, Optional

import pandas as pd
import yfinance as yf
from tqdm import tqdm

from src.utils.setup_logger import setup_logger

# Configure module-level logger
logger = setup_logger(__name__, log_to_console=False)


def download_stock_data(
    ticker: str, start_date: str, end_date: str, interval: str = "1d"
) -> Optional[pd.DataFrame]:
    """
    Download historical stock data for a given ticker using yfinance.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        interval (str): Data interval (default is "1d").

    Returns:
        Optional[pd.DataFrame]: DataFrame containing historical data if successful; otherwise, None.
    """
    try:
        logger.info(
            f"Downloading data for {ticker} from {start_date} to {end_date} with interval {interval}"
        )
        df = yf.download(
            ticker, start=start_date, end=end_date, interval=interval, progress=False
        )
        if df.empty:
            logger.warning(f"No data returned for ticker {ticker}")
            return None
        logger.info(f"Successfully downloaded {len(df)} rows for {ticker}")
        return df
    except Exception as e:
        logger.exception(f"Error downloading data for ticker {ticker}: {e}")
        return None


def save_data_to_csv(df: pd.DataFrame, file_path: str) -> None:
    """
    Save a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to be saved.
        file_path (str): Path (including filename) where the CSV will be saved.
    """
    try:
        if df.index.name is None:
            df.index.name = "Date"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path)
        logger.info(f"Data saved to {file_path}")
    except Exception as e:
        logger.exception(f"Failed to save data to {file_path}: {e}")


def download_and_save_ticker_data(
    ticker: str, start_date: str, end_date: str, output_dir: str, interval: str = "1d"
) -> bool:
    """
    Download stock data for a single ticker and save it as a CSV file.

    Args:
        ticker (str): Stock ticker symbol.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        output_dir (str): Directory where the CSV file will be stored.
        interval (str): Data interval (default is "1d").

    Returns:
        bool: True if the data was downloaded and saved successfully; False otherwise.
    """
    df = download_stock_data(ticker, start_date, end_date, interval)
    if df is None:
        logger.error(f"Data for ticker {ticker} could not be downloaded.")
        return False

    file_path = os.path.join(output_dir, f"{ticker}.csv")
    save_data_to_csv(df, file_path)
    return True


def download_multiple_tickers(
    tickers: List[str], start_date: str, end_date: str, output_dir: str, interval: str = "1d"
) -> None:
    """
    Download and save stock data for multiple tickers.

    Args:
        tickers (List[str]): List of stock ticker symbols.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        output_dir (str): Directory where CSV files will be stored.
        interval (str): Data interval (default is "1d").
    """
    failed_tickers, total_tickers = 0, len(tickers)
    for ticker in tqdm(tickers, desc="Downloading raw data for tickers"):
        success = download_and_save_ticker_data(ticker, start_date, end_date, output_dir, interval)
        if not success:
            failed_tickers += 1
    logger.info(f'Successfully downloaded data for {total_tickers - failed_tickers}/{total_tickers} tickers')
