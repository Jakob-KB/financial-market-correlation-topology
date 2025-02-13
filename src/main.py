#!/usr/bin/env python
"""
Main file to run the entire stock correlation network pipeline.

This script:
  1. Loads a ticker list from 'tickers.csv' (if it exists) or uses default tickers.
  2. Downloads raw data for each ticker.
  3. Processes the raw data to compute daily returns and a correlation matrix.
  4. Saves the processed data.
  5. Builds a correlation network from the matrix.
  6. Detects communities (clusters) in the network.
  7. Saves the network and community mapping.
  8. Generates and displays an interactive Plotly figure of the network.


TODO: This basically needs do become a notebook
"""

import os
import pandas as pd

# Import modules
from data.data_loader import download_multiple_tickers
from data.data_processor import aggregate_daily_returns, compute_correlation_matrix, save_dataframe_to_csv
from network.network_builder import build_correlation_network, save_network
from src.network.community_builder import detect_communities, save_communities
from src.visualization.app import run_native_app
from time import sleep

# Import configuration defaults
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, SAMPLE_DATA_DIR, DEFAULT_ARGUMENTS


def main():
    # 1. Load ticker list from CSV (if available); otherwise use defaults.
    ticker_csv = SAMPLE_DATA_DIR / "sample_tickers_A.csv"
    if ticker_csv.exists():
        tickers_df = pd.read_csv(ticker_csv)
        tickers = tickers_df["Ticker"].tolist()
        print(f"Loaded {len(tickers)} tickers from {ticker_csv}")
    else:
        tickers = DEFAULT_ARGUMENTS.DEFAULT_TICKERS
        print("Using default ticker list from configuration.")

    # 2. Download raw stock data for each ticker.
    start_date = DEFAULT_ARGUMENTS.DEFAULT_START_DATE
    end_date = DEFAULT_ARGUMENTS.DEFAULT_END_DATE
    interval = DEFAULT_ARGUMENTS.DEFAULT_INTERVAL
    download_multiple_tickers(tickers, start_date, end_date, str(RAW_DATA_DIR), interval)

    # 3. Process raw data: Aggregate daily returns and compute correlation matrix.
    sleep(0.5)
    returns_df = aggregate_daily_returns(tickers, str(RAW_DATA_DIR))
    corr_matrix = compute_correlation_matrix(returns_df)

    # 4. Save processed data.
    os.makedirs(str(PROCESSED_DATA_DIR), exist_ok=True)
    daily_returns_file = os.path.join(str(PROCESSED_DATA_DIR), "daily_returns.csv")
    corr_matrix_file = os.path.join(str(PROCESSED_DATA_DIR), "correlation_matrix.csv")
    save_dataframe_to_csv(returns_df, daily_returns_file)
    save_dataframe_to_csv(corr_matrix, corr_matrix_file)
    print("Processed data saved.")

    # 5. Build the correlation network.
    threshold = DEFAULT_ARGUMENTS.DEFAULT_CORRELATION_THRESHOLD
    print(f"Building network with threshold {threshold}...")
    G = build_correlation_network(corr_matrix, threshold)
    network_file = str(PROCESSED_DATA_DIR / "network.gexf")
    save_network(G, network_file)

    # 6. Detect communities (clusters) in the network.
    print("Detecting communities...")
    communities = detect_communities(G)
    if communities is not None:
        communities_file = str(PROCESSED_DATA_DIR / "communities.json")
        save_communities(communities, communities_file)
    else:
        print("No communities detected.")

    # Run the graph in browser
    run_native_app()

    # 8.Print summary.
    print("Pipeline complete.")
    # print("Network nodes:", list(G.nodes()))
    # print("Network edges:", list(G.edges(data=True)))
    # print("Detected communities:", communities)


if __name__ == "__main__":
    main()
