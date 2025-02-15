#!/usr/bin/env python
"""
Main pipeline to build and visualize a stock correlation network.

Steps:
  1. Load ticker list from 'tickers.csv' (if present) or use defaults.
  2. Download raw data for each ticker.
  3. Compute daily returns & correlation matrix.
  4. Save processed data.
  5. Build correlation network & detect communities.
  6. Save network, community mapping, and launch Dash app for visualization.
"""

import pandas as pd
from time import sleep

from data.data_loader import download_and_save_multiple_tickers
from data.data_processor import aggregate_daily_returns, compute_correlation_matrix, save_dataframe_to_csv
from network.network_builder import build_correlation_network, save_network
from src.network.community_builder import detect_communities, save_communities
from visualization.graph_plotter import generate_3d_network_figure

# Project config & defaults
from config import DIRECTORY_CONFIG, DATA_CONFIG


def main():
    """Sample pipeline, uses config args for cases like file directories and more."""

    STEP_DELAY: float = 0.1

    # Load tickers
    ticker_csv = DIRECTORY_CONFIG.SAMPLE_DATA_DIR / "sample_tickers_A.csv"

    tickers_df = pd.read_csv(ticker_csv)
    tickers = tickers_df["Ticker"].tolist()
    print(f"Loaded {len(tickers)} tickers from {ticker_csv}.")

    # Download raw data
    print("Downloading data...")
    sleep(STEP_DELAY)
    download_and_save_multiple_tickers(tickers)
    print("Downloaded data saved.\n")

    # Process data: daily returns & correlation matrix
    print("Processing data...")
    sleep(STEP_DELAY)
    returns_df = aggregate_daily_returns(tickers)
    corr_matrix = compute_correlation_matrix(returns_df)

    # Save processed data
    daily_returns_file_name = "daily_returns.csv"
    corr_matrix_file_name = "correlation_matrix.csv"
    save_dataframe_to_csv(returns_df, daily_returns_file_name)
    save_dataframe_to_csv(corr_matrix, corr_matrix_file_name)
    print("Processed data saved.\n")

    # Build correlation network
    threshold = DATA_CONFIG.CORRELATION_THRESHOLD
    G = build_correlation_network(corr_matrix, threshold)

    # Detect communities
    print("Detecting communities...")
    sleep(STEP_DELAY)
    communities = detect_communities(G)
    communities_file_name = "communities.json"
    save_communities(communities, communities_file_name)
    print("Communities saved.\n")

    # Save network and launch Dash app
    network_file_name = "network.gexf"
    save_network(G, network_file_name)

    fig = generate_3d_network_figure(G, communities)
    fig.show()

    # Final
    print("Pipeline complete.")


if __name__ == "__main__":
    main()
